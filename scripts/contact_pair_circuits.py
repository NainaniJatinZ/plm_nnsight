from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import hashlib

import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _SCRIPT_DIR.parent
_COMMON_CFG = _ROOT_DIR / "configs" / "common.json"
_PROTEINS_CFG = _ROOT_DIR / "configs" / "proteins.json"


def load_config(protein: str, config_path: str | None) -> dict:
    """Layer: common.json -> PROTEINS[protein] -> optional --config override."""
    cfg: dict = {}
    with open(_COMMON_CFG) as f:
        cfg.update(json.load(f))

    with open(_PROTEINS_CFG) as f:
        proteins = json.load(f)

    if protein not in proteins:
        raise KeyError(
            f"Protein '{protein}' not found in configs/proteins.json. "
            "Re-run scripts/build_proteins_config.py to rebuild."
        )
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
    masked[seg.ss1_start:seg.ss1_end] = list(seq_S[seg.ss1_start:seg.ss1_end])
    masked[seg.ss2_start:seg.ss2_end] = list(seq_S[seg.ss2_start:seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
        masked[i] = seq_S[i]
    return "".join(masked)


def compute_contact_map(
    esm_model: EsmForMaskedLM, tokenizer: EsmTokenizer, sequence_S: str, device: str
) -> torch.Tensor:
    inputs = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        return esm_model.predict_contacts(inputs["input_ids"], inputs["attention_mask"])[0].cpu()


def compute_contacts_from_attention(
    attn_list_LBHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor,
    attention_mask_BL: torch.Tensor,
    contact_head,
    device: str,
) -> torch.Tensor:
    attn_stack = [a.to(device) for a in attn_list_LBHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_stack, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]
    return contact_head(tokens_BL, attns_BLHLL)


def cache_attention_all_layers(
    model: NNsight,
    tokenizer: EsmTokenizer,
    sequence_S: str,
    device: str,
    num_layers: int,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )
    attn_LBHLL: list[torch.Tensor] = []
    for i in range(num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_LBHLL, inputs_BL


def faithfulness(score: float, clean_val: float, corrupt_val: float) -> float:
    gap = clean_val - corrupt_val
    if abs(gap) < 1e-6:
        return 0.0
    return (score - corrupt_val) / gap


def iter_contact_pairs(seg: ContactSegment, contact_mask: torch.Tensor) -> Iterable[tuple[int, int]]:
    rows, cols = torch.where(contact_mask)
    for r, c in zip(rows.tolist(), cols.tolist()):
        yield seg.ss1_start + r, seg.ss2_start + c


def indirect_effect_single_head(
    model: NNsight,
    clean_inputs_BL: dict,
    corrupt_head_attn_LL: torch.Tensor,
    patch_layer: int,
    patch_head: int,
    device: str,
    num_layers: int,
    num_heads: int,
    head_dim: int,
) -> list[torch.Tensor]:
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


def build_k_values(total_heads: int) -> list[int]:
    k_values = list(range(0, min(31, total_heads)))
    k_values += list(range(35, min(150, total_heads), 5))
    k_values += list(range(150, total_heads, 50))
    k_values.append(total_heads)
    return sorted(set(k_values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protein", default="1PVGA")
    parser.add_argument("--config", default=None)
    parser.add_argument("--contact_thresh", type=float, default=0.5)
    parser.add_argument("--max_contacts", type=int, default=None)
    parser.add_argument("--max_k", type=int, default=None)
    parser.add_argument("--device", default=None)
    args = parser.parse_args()

    cfg = load_config(args.protein, args.config)

    protein = args.protein
    model_name = cfg.get("model", "facebook/esm2_t33_650M_UR50D")
    data_path = cfg.get("data_path", "data/full_seq_dict.json")
    segment_radius = cfg["segment_radius"]
    clean_flank = cfg["clean_flank"]
    corrupt_flank = cfg["corrupt_flank"]
    faith_target = cfg["faith_target"]

    cache_dir = Path(cfg["cache_dir"]) / protein
    report_dir = Path(cfg["report_dir"]) / protein
    cache_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Config: protein={protein} model={model_name} faith_target={faith_target:.0%}")
    print(f"Device: {device}")

    esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device)
    tokenizer = EsmTokenizer.from_pretrained(model_name)
    model = NNsight(esm_model)

    num_layers = esm_model.config.num_hidden_layers
    num_heads = esm_model.config.num_attention_heads
    head_dim = esm_model.config.hidden_size // num_heads

    with open(data_path) as f:
        seq_dict = json.load(f)

    sequence_S = seq_dict[protein]
    contact_pair = tuple(cfg["contact_pair"])
    seg = ContactSegment.from_contact_pair(*contact_pair, radius=segment_radius)

    clean_seq_S = mask_with_flanks(sequence_S, seg, clean_flank)
    corrupt_seq_S = mask_with_flanks(sequence_S, seg, corrupt_flank)

    print(f"Protein len={len(sequence_S)}")
    print(f"Segment: ss1=[{seg.ss1_start}:{seg.ss1_end}] ss2=[{seg.ss2_start}:{seg.ss2_end}]")

    # Baseline contact maps
    orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)

    clean_attn_LBHLL, clean_inputs_BL = cache_attention_all_layers(
        model, tokenizer, clean_seq_S, device, num_layers
    )
    corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention_all_layers(
        model, tokenizer, corrupt_seq_S, device, num_layers
    )

    clean_contacts_AA = compute_contacts_from_attention(
        clean_attn_LBHLL,
        clean_inputs_BL["input_ids"],
        clean_inputs_BL["attention_mask"],
        esm_model.esm.contact_head,
        device=device,
    )[0].detach().cpu()

    corrupt_contacts_AA = compute_contacts_from_attention(
        corrupt_attn_LBHLL,
        corrupt_inputs_BL["input_ids"],
        corrupt_inputs_BL["attention_mask"],
        esm_model.esm.contact_head,
        device=device,
    )[0].detach().cpu()

    orig_seg = orig_contacts_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    clean_seg = clean_contacts_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    corrupt_seg = corrupt_contacts_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]

    # Use clean contacts for selection, not full-sequence contacts.
    contact_mask = clean_seg >= args.contact_thresh
    contact_pairs = list(iter_contact_pairs(seg, contact_mask))

    if args.max_contacts is not None:
        contact_pairs = contact_pairs[: args.max_contacts]

    print(f"Contacts in segment (threshold={args.contact_thresh}): {len(contact_pairs)}")

    if not contact_pairs:
        print("No contacts above threshold. Exiting.")
        return

    # Indirect effects cache
    ie_cache = cache_dir / "indirect_contact_preds.pt"
    ie_key = {
        "protein": protein,
        "model": model_name,
        "contact_pair": list(contact_pair),
        "clean_flank": clean_flank,
        "corrupt_flank": corrupt_flank,
        "segment_radius": segment_radius,
    }

    def cfg_hash(d: dict) -> str:
        key = json.dumps(d, sort_keys=True).encode()
        return hashlib.md5(key).hexdigest()

    indirect_preds_LH = None
    if ie_cache.exists():
        payload = torch.load(ie_cache, map_location="cpu", weights_only=False)
        if payload.get("cfg_hash") == cfg_hash(ie_key):
            indirect_preds_LH = payload["indirect_preds_LH"]

    if indirect_preds_LH is None:
        print("Computing indirect effects (660 traces)...")
        seg_len = seg.ss1_end - seg.ss1_start
        indirect_preds_LH = torch.empty(num_layers, num_heads, seg_len, seg_len)

        start = time.time()
        for layer_idx in range(num_layers):
            for head_idx in range(num_heads):
                corrupt_head_attn_LL = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]

                downstream_attn = indirect_effect_single_head(
                    model,
                    clean_inputs_BL,
                    corrupt_head_attn_LL,
                    layer_idx,
                    head_idx,
                    device,
                    num_layers,
                    num_heads,
                    head_dim,
                )

                patched_full_attn = list(clean_attn_LBHLL[:layer_idx])
                patched_layer_attn = clean_attn_LBHLL[layer_idx].clone()
                patched_layer_attn[:, head_idx, :, :] = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]
                patched_full_attn.append(patched_layer_attn)
                patched_full_attn.extend(downstream_attn)

                indirect_contacts_AA = compute_contacts_from_attention(
                    patched_full_attn,
                    clean_inputs_BL["input_ids"],
                    clean_inputs_BL["attention_mask"],
                    esm_model.esm.contact_head,
                    device=device,
                )[0].detach().cpu()

                indirect_preds_LH[layer_idx, head_idx] = indirect_contacts_AA[
                    seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end
                ]

            if (layer_idx + 1) % 5 == 0:
                elapsed = time.time() - start
                print(f"  Layer {layer_idx + 1}/{num_layers} done ({elapsed:.1f}s)")

        torch.save({"cfg_hash": cfg_hash(ie_key), "indirect_preds_LH": indirect_preds_LH}, ie_cache)

    total_heads = num_layers * num_heads
    k_values = build_k_values(total_heads)
    if args.max_k is not None:
        k_values = [k for k in k_values if k <= args.max_k]

    results = []
    circuits = []

    print(f"Running per-contact circuits (k-values={len(k_values)})")

    for pair_idx, (q_pos, k_pos) in enumerate(contact_pairs, 1):
        q_off = q_pos - seg.ss1_start
        k_off = k_pos - seg.ss2_start

        clean_val = clean_seg[q_off, k_off].item()
        corrupt_val = corrupt_seg[q_off, k_off].item()
        orig_val = orig_seg[q_off, k_off].item()

        gap = clean_val - corrupt_val

        indirect_vals = indirect_preds_LH[:, :, q_off, k_off].flatten()
        if abs(gap) > 1e-6:
            effects = (indirect_vals - clean_val) / gap
        else:
            effects = torch.zeros_like(indirect_vals)

        sorted_indices = effects.argsort(descending=True)
        sorted_heads = [(idx.item() // num_heads, idx.item() % num_heads) for idx in sorted_indices]

        crossed_k = None
        crossed_faith = None
        crossed_heads = None

        for k in k_values:
            unpatched_set = set(sorted_heads[:k])

            with model.trace() as tracer:
                with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
                    attn_cache = tracer.cache(
                        modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
                    )

                    for layer_idx in range(num_layers):
                        heads_to_patch = [
                            h for h in range(num_heads) if (layer_idx, h) not in unpatched_set
                        ]
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
                attn_list,
                clean_inputs_BL["input_ids"],
                clean_inputs_BL["attention_mask"],
                esm_model.esm.contact_head,
                device=device,
            )[0].detach().cpu()

            score = contacts_AA[q_pos, k_pos].item()
            faith = faithfulness(score, clean_val, corrupt_val)

            # Target is 70% of the clean score for this pair.
            if score >= clean_val * faith_target:
                crossed_k = k
                crossed_faith = faith
                crossed_heads = sorted_heads[:k]
                break

        results.append(
            {
                "pair_index": pair_idx,
                "q_pos": q_pos,
                "k_pos": k_pos,
                "orig": orig_val,
                "clean": clean_val,
                "corrupt": corrupt_val,
                "gap": gap,
                "k_70": crossed_k,
                "faith": crossed_faith,
            }
        )
        circuits.append(
            {
                "pair_index": pair_idx,
                "q_pos": q_pos,
                "k_pos": k_pos,
                "heads": crossed_heads,
            }
        )

        print(
            f"  Pair {pair_idx:02d} ({q_pos},{k_pos}) "
            f"orig={orig_val:.3f} clean={clean_val:.3f} corrupt={corrupt_val:.3f} "
            f"k70={crossed_k}"
        )

    # Circuit overlap summary
    head_sets = [set(c["heads"] or []) for c in circuits]
    union_heads = set().union(*head_sets) if head_sets else set()

    jaccards = []
    for i in range(len(head_sets)):
        for j in range(i + 1, len(head_sets)):
            a = head_sets[i]
            b = head_sets[j]
            if not a and not b:
                continue
            jaccards.append(len(a & b) / max(1, len(a | b)))

    summary = {
        "protein": protein,
        "contact_pair": contact_pair,
        "segment_radius": segment_radius,
        "contact_thresh": args.contact_thresh,
        "faith_target": faith_target,
        "num_contacts": len(contact_pairs),
        "union_heads": len(union_heads),
        "mean_jaccard": float(sum(jaccards) / len(jaccards)) if jaccards else None,
        "min_jaccard": float(min(jaccards)) if jaccards else None,
        "max_jaccard": float(max(jaccards)) if jaccards else None,
    }

    out_json = report_dir / f"{protein}_contact_pair_circuits.json"
    out_csv = report_dir / f"{protein}_contact_pair_circuits.csv"

    with open(out_json, "w") as f:
        json.dump({"summary": summary, "results": results, "circuits": circuits}, f, indent=2)

    # CSV with compact head list
    with open(out_csv, "w") as f:
        f.write(",".join([
            "pair_index",
            "q_pos",
            "k_pos",
            "orig",
            "clean",
            "corrupt",
            "gap",
            "k_70",
            "faith",
            "heads",
        ]) + "\n")
        for r, c in zip(results, circuits):
            heads = c["heads"] or []
            head_str = " ".join([f"L{l}H{h}" for l, h in heads])
            f.write(",".join([
                str(r["pair_index"]),
                str(r["q_pos"]),
                str(r["k_pos"]),
                f"{r['orig']:.6f}",
                f"{r['clean']:.6f}",
                f"{r['corrupt']:.6f}",
                f"{r['gap']:.6f}",
                "" if r["k_70"] is None else str(r["k_70"]),
                "" if r["faith"] is None else f"{r['faith']:.6f}",
                f"\"{head_str}\"",
            ]) + "\n")

    print(f"Wrote {out_json}")
    print(f"Wrote {out_csv}")
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()
