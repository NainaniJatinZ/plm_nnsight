"""Single-contact circuit discovery with full-segment comparison.

Compares the "full-segment" circuit (patching metric averaged over the 11x11
segment) with per-contact circuits (one cell at a time).  Uses top-k contact
selection (same logic as mutation_effect.py) instead of threshold-based.

Circuit discovery matches contact_pattern_v2.py:
  - Effect sign: (metric - clean) / (corrupt - clean), so important heads are positive
  - Three sort orders: abs, pos (primary), neg
  - Threshold: faithfulness >= faith_target

Usage:
    uv run python scripts/single_contact_circuit.py --protein 2B61A
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path

import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _SCRIPT_DIR.parent
_COMMON_CFG = _ROOT_DIR / "configs" / "common.json"
_PROTEINS_CFG = _ROOT_DIR / "configs" / "proteins.json"


def load_config(protein: str, config_path: str | None) -> dict:
    cfg: dict = {}
    with open(_COMMON_CFG) as f:
        cfg.update(json.load(f))
    with open(_PROTEINS_CFG) as f:
        proteins = json.load(f)
    if protein not in proteins:
        raise KeyError(f"Protein '{protein}' not found in configs/proteins.json.")
    cfg.update(proteins[protein])
    if config_path is not None:
        with open(config_path) as f:
            cfg.update(json.load(f))
    return cfg


@dataclass
class ContactSegment:
    ss1_start: int
    ss1_end: int
    ss2_start: int
    ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int):
        return cls(pos1 - radius, pos1 + radius + 1, pos2 - radius, pos2 + radius + 1)


def mask_with_flanks(seq_S: str, seg: ContactSegment, flank: int) -> str:
    n = len(seq_S)
    masked = ["<mask>"] * n
    masked[seg.ss1_start : seg.ss1_end] = list(seq_S[seg.ss1_start : seg.ss1_end])
    masked[seg.ss2_start : seg.ss2_end] = list(seq_S[seg.ss2_start : seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
        masked[i] = seq_S[i]
    return "".join(masked)


def compute_contact_map(esm_model, tokenizer, sequence_S, device):
    inputs = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        return esm_model.predict_contacts(inputs["input_ids"], inputs["attention_mask"])[0].cpu()


def compute_contacts_from_attention(attn_list_LBHLL, tokens_BL, attention_mask_BL, contact_head, device):
    attn_stack = [a.to(device) for a in attn_list_LBHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_stack, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]
    return contact_head(tokens_BL, attns_BLHLL)


def cache_attention_all_layers(model, tokenizer, sequence_S, device, num_layers):
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )
    attn_LBHLL = []
    for i in range(num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_LBHLL, inputs_BL


def faithfulness(score, clean_val, corrupt_val):
    gap = clean_val - corrupt_val
    if abs(gap) < 1e-6:
        return 0.0
    return (score - corrupt_val) / gap


def indirect_effect_single_head(model, clean_inputs_BL, corrupt_head_attn_LL, patch_layer, patch_head, device, num_layers, num_heads, head_dim):
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            v_raw = model.esm.encoder.layer[patch_layer].attention.self.value.output
            bsz, seqlen = v_raw.shape[0], v_raw.shape[1]
            v_heads = v_raw.reshape(bsz, seqlen, num_heads, head_dim).transpose(1, 2)

            orig_attn = model.esm.encoder.layer[patch_layer].attention.self.output[1]
            patched_attn = orig_attn.clone()
            patched_attn[:, patch_head, :, :] = corrupt_head_attn_LL.to(device)

            new_ctx = torch.matmul(patched_attn, v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(bsz, seqlen, -1)
            model.esm.encoder.layer[patch_layer].attention.self.output[0][:] = new_ctx

            downstream_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(patch_layer + 1, num_layers)]
            )

    downstream_attn = []
    for i in range(patch_layer + 1, num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        downstream_attn.append(downstream_cache[key].output[1].detach().cpu())
    return downstream_attn


def select_top_contacts(contact_map_AA, seg, top_k):
    """Top-k contacts by value in the segment (same logic as mutation_effect.py)."""
    seg_map = contact_map_AA[seg.ss1_start : seg.ss1_end, seg.ss2_start : seg.ss2_end]
    flat = seg_map.flatten()
    k = min(top_k, flat.numel())
    values, indices = torch.topk(flat, k=k)
    contacts = []
    width = seg_map.shape[1]
    for v, idx in zip(values.tolist(), indices.tolist()):
        r = idx // width
        c = idx % width
        contacts.append((seg.ss1_start + r, seg.ss2_start + c, float(v)))
    return contacts


def segment_metric(pred_seg, orig_seg, denom):
    if denom < 1e-12:
        return 0.0
    return ((pred_seg * orig_seg).sum() / denom).item()


def build_k_values(total_heads):
    """Coarser grid than contact_pattern_v2.py for speed; fine near start, coarser at tail."""
    k_values = list(range(0, min(31, total_heads)))
    k_values += list(range(35, min(101, total_heads), 5))
    k_values += list(range(110, min(201, total_heads), 10))
    k_values += list(range(250, total_heads, 50))
    k_values.append(total_heads)
    return sorted(set(k_values))


def _cfg_hash(d):
    key = json.dumps(d, sort_keys=True).encode()
    return hashlib.md5(key).hexdigest()


def run_patching_trace(model, esm_model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL, unpatched_set, num_layers, num_heads, head_dim, device):
    """Run one multi-head patching trace and return the full contacts_AA tensor."""
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )
            for layer_idx in range(num_layers):
                heads_to_patch = [h for h in range(num_heads) if (layer_idx, h) not in unpatched_set]
                if not heads_to_patch:
                    continue
                v_raw = model.esm.encoder.layer[layer_idx].attention.self.value.output
                v_heads = v_raw.reshape(1, v_raw.shape[1], num_heads, head_dim).transpose(1, 2)
                attn_probs = model.esm.encoder.layer[layer_idx].attention.self.output[1]
                patched_attn = attn_probs.clone()
                for h in heads_to_patch:
                    patched_attn[:, h, :, :] = corrupt_attn_LBHLL[layer_idx][:, h, :, :].to(device)
                new_ctx = torch.matmul(patched_attn, v_heads)
                new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(1, v_raw.shape[1], -1)
                model.esm.encoder.layer[layer_idx].attention.self.output[0][:] = new_ctx

    attn_list = []
    for i in range(num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        heads_patched = [h for h in range(num_heads) if (i, h) not in unpatched_set]
        for h in heads_patched:
            layer_attn[:, h, :, :] = corrupt_attn_LBHLL[i][:, h, :, :]
        attn_list.append(layer_attn)

    contacts_AA = compute_contacts_from_attention(
        attn_list, clean_inputs_BL["input_ids"], clean_inputs_BL["attention_mask"],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()
    return contacts_AA


def greedy_circuit(model, esm_model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL, sorted_heads, k_values, score_fn, faith_target, clean_val, corrupt_val, num_layers, num_heads, head_dim, device):
    """Greedy unpatching loop. Threshold: faithfulness >= faith_target."""
    curve = []
    crossed_k = None
    crossed_faith = None
    crossed_heads = None

    for k in k_values:
        unpatched_set = set(sorted_heads[:k])
        contacts_AA = run_patching_trace(
            model, esm_model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL,
            unpatched_set, num_layers, num_heads, head_dim, device,
        )
        score = score_fn(contacts_AA)
        faith = faithfulness(score, clean_val, corrupt_val)
        curve.append({"k": k, "score": float(score), "faith": float(faith)})

        if crossed_k is None and faith >= faith_target:
            crossed_k = k
            crossed_faith = faith
            crossed_heads = sorted_heads[:k]
            break

    return crossed_k, crossed_faith, crossed_heads, curve


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    return len(set_a & set_b) / max(1, len(set_a | set_b))


def compute_effects_and_sorts(effects_flat, num_heads):
    """Compute three sort orders from a flat effects tensor, matching contact_pattern_v2.py."""
    sort_configs = {
        "abs": effects_flat.abs().argsort(descending=True),
        "pos": effects_flat.argsort(descending=True),
        "neg": effects_flat.argsort(descending=False),
    }
    sorted_heads = {}
    for name, indices in sort_configs.items():
        sorted_heads[name] = [(idx.item() // num_heads, idx.item() % num_heads) for idx in indices]
    return sorted_heads


def main():
    parser = argparse.ArgumentParser(description="Single-contact circuit discovery with full-segment comparison")
    parser.add_argument("--protein", default="2B61A")
    parser.add_argument("--config", default=None)
    parser.add_argument("--top-contact-k", type=int, default=4, help="Number of top contacts to analyze individually")
    parser.add_argument("--max-k", type=int, default=None)
    parser.add_argument("--device", default=None)
    parser.add_argument("--sort", default="pos", choices=["abs", "pos", "neg", "all"], help="Sort order for circuit discovery (default: pos, matching contact_pattern_v2.py)")
    args = parser.parse_args()

    cfg = load_config(args.protein, args.config)

    protein = args.protein
    model_name = cfg.get("model", "facebook/esm2_t33_650M_UR50D")
    data_path = Path(cfg.get("data_path", "data/full_seq_dict.json"))
    if not data_path.is_absolute():
        data_path = _ROOT_DIR / data_path
    segment_radius = cfg["segment_radius"]
    clean_flank = cfg["clean_flank"]
    corrupt_flank = cfg["corrupt_flank"]
    faith_target = cfg["faith_target"]

    cache_dir = _ROOT_DIR / cfg["cache_dir"] / protein
    report_dir = _ROOT_DIR / cfg["report_dir"] / protein
    cache_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    sort_orders = ["abs", "pos", "neg"] if args.sort == "all" else [args.sort]

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Config: protein={protein} model={model_name} faith_target={faith_target:.0%}")
    print(f"Device: {device}")
    print(f"Sort orders: {sort_orders}")

    esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device)
    tokenizer = EsmTokenizer.from_pretrained(model_name)
    model = NNsight(esm_model)

    num_layers = esm_model.config.num_hidden_layers
    num_heads = esm_model.config.num_attention_heads
    head_dim = esm_model.config.hidden_size // num_heads
    total_heads = num_layers * num_heads

    with open(data_path) as f:
        seq_dict = json.load(f)
    sequence_S = seq_dict[protein]
    contact_pair = tuple(cfg["contact_pair"])
    seg = ContactSegment.from_contact_pair(*contact_pair, radius=segment_radius)

    clean_seq_S = mask_with_flanks(sequence_S, seg, clean_flank)
    corrupt_seq_S = mask_with_flanks(sequence_S, seg, corrupt_flank)

    print(f"Protein len={len(sequence_S)}")
    print(f"Segment: ss1=[{seg.ss1_start}:{seg.ss1_end}] ss2=[{seg.ss2_start}:{seg.ss2_end}]")

    # ---- Baseline contact maps ----
    orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)

    clean_attn_LBHLL, clean_inputs_BL = cache_attention_all_layers(model, tokenizer, clean_seq_S, device, num_layers)
    corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention_all_layers(model, tokenizer, corrupt_seq_S, device, num_layers)

    clean_contacts_AA = compute_contacts_from_attention(
        clean_attn_LBHLL, clean_inputs_BL["input_ids"], clean_inputs_BL["attention_mask"],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()

    corrupt_contacts_AA = compute_contacts_from_attention(
        corrupt_attn_LBHLL, corrupt_inputs_BL["input_ids"], corrupt_inputs_BL["attention_mask"],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()

    orig_seg = orig_contacts_AA[seg.ss1_start : seg.ss1_end, seg.ss2_start : seg.ss2_end]
    clean_seg = clean_contacts_AA[seg.ss1_start : seg.ss1_end, seg.ss2_start : seg.ss2_end]
    corrupt_seg = corrupt_contacts_AA[seg.ss1_start : seg.ss1_end, seg.ss2_start : seg.ss2_end]

    seg_denom = (orig_seg * orig_seg).sum().item()
    clean_seg_metric = segment_metric(clean_seg, orig_seg, seg_denom)
    corrupt_seg_metric = segment_metric(corrupt_seg, orig_seg, seg_denom)
    seg_gap = clean_seg_metric - corrupt_seg_metric

    print(f"Full-segment metrics: clean={clean_seg_metric:.4f} corrupt={corrupt_seg_metric:.4f} gap={seg_gap:.4f}")

    # ---- Select top contacts (top-k by clean contact value, same as mutation_effect.py) ----
    top_contacts = select_top_contacts(clean_contacts_AA, seg, args.top_contact_k)
    print(f"Top {len(top_contacts)} contacts (by clean map value):")
    for q, k_pos, val in top_contacts:
        orig_val = orig_contacts_AA[q, k_pos].item()
        cv = corrupt_contacts_AA[q, k_pos].item()
        print(f"  ({q},{k_pos}) clean={val:.4f} orig={orig_val:.4f} corrupt={cv:.4f}")

    # ---- Indirect effects (660 traces, cached) ----
    ie_key = {
        "protein": protein, "model": model_name,
        "contact_pair": list(contact_pair),
        "clean_flank": clean_flank, "corrupt_flank": corrupt_flank,
        "segment_radius": segment_radius,
    }
    ie_cache = cache_dir / "indirect_contact_preds.pt"
    indirect_preds_LH = None
    if ie_cache.exists():
        payload = torch.load(ie_cache, map_location="cpu", weights_only=False)
        if payload.get("cfg_hash") == _cfg_hash(ie_key):
            indirect_preds_LH = payload["indirect_preds_LH"]
            print("Loaded indirect effects from cache.")

    if indirect_preds_LH is None:
        print("Computing indirect effects (660 traces)...")
        seg_len = seg.ss1_end - seg.ss1_start
        indirect_preds_LH = torch.empty(num_layers, num_heads, seg_len, seg_len)
        start = time.time()
        for layer_idx in range(num_layers):
            for head_idx in range(num_heads):
                corrupt_head_attn_LL = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]
                downstream_attn = indirect_effect_single_head(
                    model, clean_inputs_BL, corrupt_head_attn_LL,
                    layer_idx, head_idx, device, num_layers, num_heads, head_dim,
                )
                patched_full_attn = list(clean_attn_LBHLL[:layer_idx])
                patched_layer_attn = clean_attn_LBHLL[layer_idx].clone()
                patched_layer_attn[:, head_idx, :, :] = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]
                patched_full_attn.append(patched_layer_attn)
                patched_full_attn.extend(downstream_attn)
                indirect_contacts_AA = compute_contacts_from_attention(
                    patched_full_attn, clean_inputs_BL["input_ids"], clean_inputs_BL["attention_mask"],
                    esm_model.esm.contact_head, device=device,
                )[0].detach().cpu()
                indirect_preds_LH[layer_idx, head_idx] = indirect_contacts_AA[seg.ss1_start : seg.ss1_end, seg.ss2_start : seg.ss2_end]
            if (layer_idx + 1) % 5 == 0:
                print(f"  Layer {layer_idx + 1}/{num_layers} done ({time.time() - start:.1f}s)")
        torch.save({"cfg_hash": _cfg_hash(ie_key), "indirect_preds_LH": indirect_preds_LH}, ie_cache)

    k_values = build_k_values(total_heads)
    if args.max_k is not None:
        k_values = [k for k in k_values if k <= args.max_k]

    # ==== Phase 1: Full-segment circuit ====
    print("\n=== Full-segment circuit ===")

    # Compute per-head segment effects with contact_pattern_v2.py sign convention:
    # effect = (metric - clean) / (corrupt - clean)
    # Important heads → positive effect (patching them drops metric toward corrupt)
    seg_effects = torch.empty(total_heads)
    denom_seg = corrupt_seg_metric - clean_seg_metric  # negative
    for flat_idx in range(total_heads):
        L = flat_idx // num_heads
        H = flat_idx % num_heads
        m = segment_metric(indirect_preds_LH[L, H], orig_seg, seg_denom)
        if abs(denom_seg) > 1e-6:
            seg_effects[flat_idx] = (m - clean_seg_metric) / denom_seg
        else:
            seg_effects[flat_idx] = 0.0

    seg_sorted_by = compute_effects_and_sorts(seg_effects, num_heads)

    # Sanity check: print effect stats to compare with contact_pattern_v2.py
    print(f"Segment effect stats: min={seg_effects.min():.4f} max={seg_effects.max():.4f} mean={seg_effects.mean():.4f}")
    print(f"  positive: {(seg_effects > 0).sum().item()} heads, negative: {(seg_effects < 0).sum().item()} heads")

    def seg_score_fn(contacts_AA):
        pred = contacts_AA[seg.ss1_start : seg.ss1_end, seg.ss2_start : seg.ss2_end]
        return segment_metric(pred, orig_seg, seg_denom)

    seg_circuit_results = {}
    for sort_name in sort_orders:
        sorted_heads_list = seg_sorted_by[sort_name]
        sk70, sfaith, sheads, scurve = greedy_circuit(
            model, esm_model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL,
            sorted_heads_list, k_values, seg_score_fn, faith_target, clean_seg_metric, corrupt_seg_metric,
            num_layers, num_heads, head_dim, device,
        )
        seg_circuit_results[sort_name] = {"k_70": sk70, "faith": sfaith, "heads": sheads, "curve": scurve}
        faith_str = f"{sfaith:.4f}" if sfaith is not None else "N/A"
        size = len(sheads) if sheads else 0
        print(f"  [{sort_name}] k70={sk70} faith={faith_str} circuit_size={size}")

    # Use "pos" sort as the primary full-segment circuit (matching contact_pattern_v2.py)
    primary_sort = "pos" if "pos" in sort_orders else sort_orders[0]
    seg_primary = seg_circuit_results[primary_sort]
    seg_circuit_set = set(seg_primary["heads"]) if seg_primary["heads"] else set()

    # ==== Phase 2: Per-contact circuits ====
    print("\n=== Per-contact circuits ===")

    contact_results = []
    contact_circuits = []

    for ci, (q_pos, k_pos, contact_val) in enumerate(top_contacts, 1):
        q_off = q_pos - seg.ss1_start
        k_off = k_pos - seg.ss2_start

        clean_val = clean_seg[q_off, k_off].item()
        corrupt_val = corrupt_seg[q_off, k_off].item()
        orig_val = orig_seg[q_off, k_off].item()
        gap = clean_val - corrupt_val

        # Effect with contact_pattern_v2.py sign convention
        indirect_vals = indirect_preds_LH[:, :, q_off, k_off].flatten()
        denom_c = corrupt_val - clean_val  # negative
        if abs(denom_c) > 1e-6:
            effects = (indirect_vals - clean_val) / denom_c
        else:
            effects = torch.zeros_like(indirect_vals)

        contact_sorted_by = compute_effects_and_sorts(effects, num_heads)

        def contact_score_fn(contacts_AA, _q=q_pos, _k=k_pos):
            return contacts_AA[_q, _k].item()

        # Run circuit discovery for each requested sort order
        contact_sort_results = {}
        for sort_name in sort_orders:
            ck70, cfaith, cheads, ccurve = greedy_circuit(
                model, esm_model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL,
                contact_sorted_by[sort_name], k_values, contact_score_fn, faith_target, clean_val, corrupt_val,
                num_layers, num_heads, head_dim, device,
            )
            contact_sort_results[sort_name] = {"k_70": ck70, "faith": cfaith, "heads": cheads, "curve": ccurve}

        # Use primary sort for overlap analysis
        primary_result = contact_sort_results[primary_sort]

        contact_results.append({
            "contact_index": ci,
            "q_pos": q_pos, "k_pos": k_pos,
            "orig": orig_val, "clean": clean_val, "corrupt": corrupt_val, "gap": gap,
            "sort_results": {sn: {"k_70": sr["k_70"], "faith": sr["faith"]} for sn, sr in contact_sort_results.items()},
        })
        contact_circuits.append({
            "contact_index": ci, "q_pos": q_pos, "k_pos": k_pos,
            "heads": primary_result["heads"],
            "sort_results": contact_sort_results,
        })

        for sort_name in sort_orders:
            sr = contact_sort_results[sort_name]
            f_str = f"{sr['faith']:.4f}" if sr["faith"] is not None else "N/A"
            sz = len(sr["heads"]) if sr["heads"] else 0
            print(f"  Contact {ci} ({q_pos},{k_pos}) [{sort_name}] clean={clean_val:.4f} corrupt={corrupt_val:.4f} gap={gap:.4f} k70={sr['k_70']} faith={f_str} size={sz}")

    # ==== Phase 3: Overlap analysis (using primary sort) ====
    print(f"\n=== Overlap analysis (sort={primary_sort}) ===")

    contact_head_sets = [set(c["heads"] or []) for c in contact_circuits]

    pairwise_jaccards = []
    for i in range(len(contact_head_sets)):
        for j in range(i + 1, len(contact_head_sets)):
            j_val = jaccard(contact_head_sets[i], contact_head_sets[j])
            pairwise_jaccards.append({
                "i": i + 1, "j": j + 1,
                "jaccard": j_val,
                "intersection": len(contact_head_sets[i] & contact_head_sets[j]),
                "union": len(contact_head_sets[i] | contact_head_sets[j]),
            })

    vs_full = []
    for i, hs in enumerate(contact_head_sets):
        j_val = jaccard(hs, seg_circuit_set)
        vs_full.append({
            "contact_index": i + 1,
            "jaccard_vs_full": j_val,
            "contact_size": len(hs),
            "full_size": len(seg_circuit_set),
            "intersection": len(hs & seg_circuit_set),
            "contact_only": len(hs - seg_circuit_set),
            "full_only": len(seg_circuit_set - hs),
        })

    all_contact_union = set().union(*contact_head_sets) if contact_head_sets else set()
    all_contact_intersection = set.intersection(*contact_head_sets) if contact_head_sets and all(contact_head_sets) else set()

    mean_pw_jaccard = sum(p["jaccard"] for p in pairwise_jaccards) / len(pairwise_jaccards) if pairwise_jaccards else None

    overlap_summary = {
        "num_contacts": len(top_contacts),
        "full_circuit_size": len(seg_circuit_set),
        "per_contact_sizes": [len(s) for s in contact_head_sets],
        "contact_union_size": len(all_contact_union),
        "contact_intersection_size": len(all_contact_intersection),
        "union_vs_full_jaccard": jaccard(all_contact_union, seg_circuit_set),
        "mean_pairwise_jaccard": mean_pw_jaccard,
        "pairwise_jaccards": pairwise_jaccards,
        "vs_full": vs_full,
    }

    for item in vs_full:
        ci = item["contact_index"]
        print(f"  Contact {ci}: size={item['contact_size']} jaccard_vs_full={item['jaccard_vs_full']:.3f} intersection={item['intersection']} contact_only={item['contact_only']} full_only={item['full_only']}")
    if mean_pw_jaccard is not None:
        print(f"  Mean pairwise Jaccard: {mean_pw_jaccard:.3f}")
    print(f"  Union of contact circuits: {len(all_contact_union)} heads")
    print(f"  Intersection of contact circuits: {len(all_contact_intersection)} heads")
    print(f"  Full-segment circuit: {len(seg_circuit_set)} heads")
    print(f"  Union vs full Jaccard: {overlap_summary['union_vs_full_jaccard']:.3f}")

    # ==== Save results ====
    output = {
        "protein": protein,
        "contact_pair": contact_pair,
        "segment_radius": segment_radius,
        "faith_target": faith_target,
        "top_contact_k": args.top_contact_k,
        "sort_orders": sort_orders,
        "primary_sort": primary_sort,
        "full_segment": {
            "clean_metric": clean_seg_metric,
            "corrupt_metric": corrupt_seg_metric,
            "gap": seg_gap,
            "sort_results": {sn: {"k_70": sr["k_70"], "faith": sr["faith"], "circuit_heads": [(L, H) for L, H in (sr["heads"] or [])], "curve": sr["curve"]} for sn, sr in seg_circuit_results.items()},
        },
        "contact_results": contact_results,
        "contact_circuits": [
            {"contact_index": c["contact_index"], "q_pos": c["q_pos"], "k_pos": c["k_pos"], "heads": [(L, H) for L, H in (c["heads"] or [])], "sort_results": {sn: {"k_70": sr["k_70"], "faith": sr["faith"], "circuit_heads": [(L, H) for L, H in (sr["heads"] or [])]} for sn, sr in c["sort_results"].items()}}
            for c in contact_circuits
        ],
        "overlap": overlap_summary,
    }

    out_json = report_dir / f"{protein}_single_contact_circuits.json"
    with open(out_json, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nWrote {out_json}")

    txt_path = report_dir / f"{protein}_single_contact_circuits.txt"
    with open(txt_path, "w") as f:
        f.write(f"Single-contact circuit analysis: {protein}\n")
        f.write(f"Contact pair: {contact_pair}\n")
        f.write(f"Faith target: {faith_target:.0%}\n")
        f.write(f"Sort orders: {sort_orders}, primary: {primary_sort}\n\n")
        f.write(f"Full-segment circuit:\n")
        f.write(f"  clean={clean_seg_metric:.4f} corrupt={corrupt_seg_metric:.4f} gap={seg_gap:.4f}\n")
        for sn, sr in seg_circuit_results.items():
            f_str = f"{sr['faith']:.4f}" if sr["faith"] is not None else "N/A"
            sz = len(sr["heads"]) if sr["heads"] else 0
            f.write(f"  [{sn}] k_70={sr['k_70']} faith={f_str} size={sz}\n")
        primary_heads = seg_primary["heads"] or []
        if primary_heads:
            head_str = " ".join([f"L{l}H{h}" for l, h in primary_heads])
            f.write(f"  [{primary_sort}] heads: {head_str}\n")
        f.write(f"\nPer-contact circuits (top {args.top_contact_k}):\n")
        for r, c in zip(contact_results, contact_circuits):
            for sn in sort_orders:
                sr = r["sort_results"][sn]
                heads = c["sort_results"][sn]["heads"] or []
                f_str = f"{sr['faith']:.4f}" if sr["faith"] is not None else "N/A"
                f.write(f"  ({r['q_pos']},{r['k_pos']}) [{sn}] clean={r['clean']:.4f} corrupt={r['corrupt']:.4f} gap={r['gap']:.4f} k70={sr['k_70']} faith={f_str} size={len(heads)}\n")
                if sn == primary_sort and heads:
                    head_str = " ".join([f"L{l}H{h}" for l, h in heads])
                    f.write(f"    heads: {head_str}\n")
        f.write(f"\nOverlap analysis (sort={primary_sort}):\n")
        for item in vs_full:
            f.write(f"  Contact {item['contact_index']}: jaccard_vs_full={item['jaccard_vs_full']:.3f} intersection={item['intersection']} contact_only={item['contact_only']} full_only={item['full_only']}\n")
        if mean_pw_jaccard is not None:
            f.write(f"  Mean pairwise Jaccard: {mean_pw_jaccard:.3f}\n")
        f.write(f"  Union: {len(all_contact_union)} heads, Intersection: {len(all_contact_intersection)} heads\n")
        f.write(f"  Union vs full Jaccard: {overlap_summary['union_vs_full_jaccard']:.3f}\n")
    print(f"Wrote {txt_path}")


if __name__ == "__main__":
    main()
