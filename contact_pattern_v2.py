# %% [markdown]
# # Contact Pattern: Head-Level Attribution + Sufficiency
#
# Pipeline:
#   1. Setup: load model + data, compute baselines, cache attention
#   2. Indirect effects: 660-trace patching to rank heads
#   3. Circuit discovery: greedy unpatching sweep
#   4. Gradient attribution: one forward+backward to score every cell
#   5. Sufficiency: protect top-K cells, corrupt rest
#   6. Motif extraction for the identified circuit heads
#   7. Markdown report
#
# Run as: `uv run python contact_pattern_v2.py --protein 2B61A`
# Or:    `uv run python contact_pattern_v2.py --protein 2B61A --config configs/override.json`
# Or run individual `# %%` cells in VS Code / Jupyter.

# %% ── Imports ──────────────────────────────────────────────────────────────

from __future__ import annotations

import csv
import gc
import hashlib
import json
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

# %% ── Configuration ─────────────────────────────────────────────────────────

import argparse as _ap

_SCRIPT_DIR = Path(__file__).resolve().parent
_COMMON_CFG  = _SCRIPT_DIR / "configs" / "common.json"
_PROTEINS_CFG = _SCRIPT_DIR / "configs" / "proteins.json"

with open(_PROTEINS_CFG) as _f:
    PROTEINS: dict = json.load(_f)


def load_config(protein: str, config_path: str | None) -> dict:
    """Layer: common.json → PROTEINS[protein] → optional --config override."""
    cfg: dict = {}

    # 1. shared defaults
    with open(_COMMON_CFG) as f:
        cfg.update(json.load(f))

    # 2. protein-specific data (contact_pair, clean_flank, corrupt_flank)
    if protein not in PROTEINS:
        raise KeyError(
            f"Protein '{protein}' not found in configs/proteins.json. "
            f"Re-run scripts/build_proteins_config.py to rebuild."
        )
    cfg.update(PROTEINS[protein])

    # 3. explicit --config override (e.g. sweep-specific settings)
    if config_path is not None:
        with open(config_path) as f:
            cfg.update(json.load(f))

    return cfg


_p = _ap.ArgumentParser()
_p.add_argument("--protein", default="1PVGA")
_p.add_argument("--config", default=None)    # optional extra overrides
_args, _ = _p.parse_known_args()             # parse_known_args for notebook compat
cfg = load_config(_args.protein, _args.config)

PROTEIN        = _args.protein
MODEL_NAME     = cfg.get("model", "facebook/esm2_t33_650M_UR50D")
DATA_PATH      = cfg.get("data_path", "data/full_seq_dict.json")
FAITH_TARGET   = cfg["faith_target"]
SEGMENT_RADIUS = cfg["segment_radius"]

CLEAN_FLANK   = cfg["clean_flank"]
CORRUPT_FLANK = cfg["corrupt_flank"]
CONTACT_PAIR  = tuple(cfg["contact_pair"])

CONC_N    = cfg["conc_n"]
CONC_MASS = cfg["conc_mass"]

CACHE_DIR  = Path(cfg["cache_dir"]) / PROTEIN
REPORT_DIR = Path(cfg["report_dir"]) / PROTEIN
CACHE_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Config: protein={PROTEIN}  model={MODEL_NAME}  faith_target={FAITH_TARGET:.0%}")
print(f"Cache dir: {CACHE_DIR}")


# ── Cache helpers ──────────────────────────────────────────────────────────

def _cfg_hash(d: dict) -> str:
    return hashlib.md5(json.dumps(d, sort_keys=True).encode()).hexdigest()[:10]


def _cache_valid(path: Path, key: dict, force: bool) -> bool:
    if force or not path.exists():
        return False
    try:
        data = torch.load(path, map_location="cpu", weights_only=False)
        return data.get("cfg_hash") == _cfg_hash(key)
    except Exception:
        return False


def _cache_save(path: Path, payload: dict, key: dict) -> None:
    payload["cfg_hash"] = _cfg_hash(key)
    torch.save(payload, path)


_BASE_KEY = {
    "protein": PROTEIN, "model": MODEL_NAME,
    "contact_pair": list(CONTACT_PAIR),
    "clean_flank": CLEAN_FLANK, "corrupt_flank": CORRUPT_FLANK,
    "segment_radius": SEGMENT_RADIUS,
}

# %% ── Helpers ────────────────────────────────────────────────────────────────

def log_memory(label: str = "") -> None:
    if torch.cuda.is_available():
        alloc = torch.cuda.memory_allocated() / 1e9
        resv  = torch.cuda.memory_reserved()  / 1e9
        print(f"[Memory {label}] alloc={alloc:.2f}GB  resv={resv:.2f}GB")


def clear_memory() -> None:
    gc.collect()
    torch.cuda.empty_cache()


@dataclass
class ContactSegment:
    ss1_start: int; ss1_end: int
    ss2_start: int; ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int = SEGMENT_RADIUS):
        return cls(pos1 - radius, pos1 + radius + 1,
                   pos2 - radius, pos2 + radius + 1)


def mask_with_flanks(seq_S: str, seg: ContactSegment, flank: int) -> str:
    n = len(seq_S)
    masked: list[str] = ["<mask>"] * n
    masked[seg.ss1_start:seg.ss1_end] = list(seq_S[seg.ss1_start:seg.ss1_end])
    masked[seg.ss2_start:seg.ss2_end] = list(seq_S[seg.ss2_start:seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
        masked[i] = seq_S[i]
    return "".join(masked)


def compute_contact_map(
    esm_model: EsmForMaskedLM, tokenizer: EsmTokenizer,
    sequence_S: str, device: str,
) -> torch.Tensor:
    """Returns (A, A) contact map on CPU."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        return esm_model.predict_contacts(
            inputs_BL["input_ids"], inputs_BL["attention_mask"]
        )[0].cpu()


def patching_metric(
    pred_AA: torch.Tensor, orig_AA: torch.Tensor, seg: ContactSegment,
) -> float:
    pred = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = (orig * orig).sum()
    return ((pred * orig).sum() / denom).item() if denom > 1e-12 else 0.0


def faithfulness(metric: float, clean_m: float, corrupt_m: float) -> float:
    gap = clean_m - corrupt_m
    return (metric - corrupt_m) / gap if abs(gap) > 1e-6 else 0.0


def compute_contacts_from_attention(
    attn_list_LBHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor,
    attention_mask_BL: torch.Tensor,
    contact_head,
    device: str = "cuda",
) -> torch.Tensor:
    """Re-run ESM contact head from a list of (B,H,L,L) tensors. Returns (B,A,A)."""
    attn_stack = [a.to(device) for a in attn_list_LBHLL]
    tokens_BL         = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_stack, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]
    return contact_head(tokens_BL, attns_BLHLL)


def cache_attention_all_layers(
    model: NNsight, tokenizer: EsmTokenizer,
    sequence_S: str, device: str, num_layers: int,
) -> tuple[list[torch.Tensor], dict]:
    """Traced forward; returns (list of (B,H,L,L) per layer on CPU, tokenizer inputs)."""
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


def contact_metric_from_attn_proxies(
    attn_proxies, tokens_BL, attention_mask_BL,
    eos_idx, regression_weight, regression_bias, orig_seg, segment,
):
    """Differentiable contact metric from attention weights."""
    attns = torch.stack(attn_proxies, dim=1)  # (B, num_layers, H, L, L)
    attns = attns * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns = attns * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)

    eos_mask = tokens_BL.ne(eos_idx).float()
    eos_mask_2d = eos_mask.unsqueeze(1) * eos_mask.unsqueeze(2)
    attns = attns * eos_mask_2d[:, None, None, :, :]

    attns = attns[..., :-1, :-1]
    attns = attns[..., 1:, 1:]

    batch_size, layers, heads, seqlen, _ = attns.shape
    attns = attns.reshape(batch_size, layers * heads, seqlen, seqlen)

    attns = attns + attns.transpose(-1, -2)

    a1  = attns.sum(-1, keepdim=True)
    a2  = attns.sum(-2, keepdim=True)
    a12 = attns.sum(dim=(-1, -2), keepdim=True)
    avg = a1 * a2 / a12
    attns = attns - avg

    attns = attns.permute(0, 2, 3, 1)
    contacts = torch.sigmoid(torch.nn.functional.linear(attns, regression_weight, regression_bias))
    contacts = contacts.squeeze(3)

    pred_seg = contacts[0, segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    metric = (pred_seg * orig_seg).sum() / (orig_seg * orig_seg).sum()
    return metric


def make_classify_pos(seg: ContactSegment, flank: int):
    """Returns a pos-classifier closure for the given segment and flank size."""
    ss1   = set(range(seg.ss1_start, seg.ss1_end))
    ss2   = set(range(seg.ss2_start, seg.ss2_end))
    flk_l = set(range(max(0, seg.ss1_start - flank), seg.ss1_start))
    flk_r = set(range(seg.ss2_end, seg.ss2_end + flank))

    def _classify(pos: int) -> str:
        if pos in ss1:   return "ss1"
        if pos in ss2:   return "ss2"
        if pos in flk_l: return "flkL"
        if pos in flk_r: return "flkR"
        return "other"

    return _classify


def _anchor_label(anchor: str, sorted_items: list, seq: str) -> str:
    """Return 'AA<pos>' label(s) for SINGLE/DUAL anchor types.

    sorted_items contains token indices (BOS=0).  We display positions as
    0-indexed sequence positions (token - 1) to match CONTACT_PAIR indexing,
    so 'V182' means seq_S[182] — the same '182' as in CONTACT_PAIR=(182,316).
    """
    if anchor == "SINGLE-ANCHOR" and sorted_items:
        tok = sorted_items[0][0]
        seq_pos = tok - 1                      # 0-indexed sequence position
        aa = seq[seq_pos] if 0 <= seq_pos < len(seq) else "?"
        return f"{aa}{seq_pos}"
    elif anchor == "DUAL-ANCHOR" and len(sorted_items) >= 2:
        tok1, tok2 = sorted_items[0][0], sorted_items[1][0]
        p1, p2 = tok1 - 1, tok2 - 1
        a1 = seq[p1] if 0 <= p1 < len(seq) else "?"
        a2 = seq[p2] if 0 <= p2 < len(seq) else "?"
        return f"{a1}{p1}/{a2}{p2}"
    return ""


def _distr_label(mass_dict: dict, total_abs: float, seq: str,
                 max_n: int = None, mass_t: float = None) -> str:
    """For a DISTRIBUTED pattern, return a '/'-joined label of the top positions
    by abs mass that together cover *mass_t* of the total.  Returns '' if more
    than *max_n* positions are needed (truly distributed).

    Token indices (BOS=0) are converted to 0-indexed seq positions for display,
    matching the CONTACT_PAIR convention.
    """
    if max_n  is None: max_n  = CONC_N
    if mass_t is None: mass_t = CONC_MASS
    if not mass_dict or total_abs < 1e-9:
        return ""
    by_abs = sorted(mass_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    cum, n_min = 0.0, len(by_abs)
    for i, (_, v) in enumerate(by_abs):
        cum += abs(v)
        if cum / total_abs >= mass_t:
            n_min = i + 1
            break
    if n_min > max_n:
        return ""
    labels = []
    for tok, _ in by_abs[:n_min]:
        p = tok - 1
        aa = seq[p] if 0 <= p < len(seq) else "?"
        labels.append(f"{aa}{p}")
    return "/".join(labels)


# %% ── Model + Data Loading ───────────────────────────────────────────────────

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"\nDevice: {device}")

esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
model     = NNsight(esm_model)

NUM_LAYERS = esm_model.config.num_hidden_layers    # 33 for 650M
NUM_HEADS  = esm_model.config.num_attention_heads   # 20 for 650M
HEAD_DIM   = esm_model.config.hidden_size // NUM_HEADS

print(f"Model : {MODEL_NAME}  ({NUM_LAYERS}L × {NUM_HEADS}H, head_dim={HEAD_DIM})")
log_memory("after model load")

with open(DATA_PATH) as f:
    seq_dict = json.load(f)

sequence_S    = seq_dict[PROTEIN]
seg           = ContactSegment.from_contact_pair(*CONTACT_PAIR)
clean_seq_S   = mask_with_flanks(sequence_S, seg, CLEAN_FLANK)
corrupt_seq_S = mask_with_flanks(sequence_S, seg, CORRUPT_FLANK)

print(f"\nProtein : {PROTEIN}  (len={len(sequence_S)})")
print(f"Segment : ss1=[{seg.ss1_start}:{seg.ss1_end}]  ss2=[{seg.ss2_start}:{seg.ss2_end}]")
print(f"Flanks  : clean={CLEAN_FLANK}  corrupt={CORRUPT_FLANK}")

classify_pos = make_classify_pos(seg, CLEAN_FLANK)

def _cpos(tok: int) -> str:
    """Classify a raw attention token index into a region name.

    Cell attributions store token indices where BOS=0 and first amino acid=1,
    so token i corresponds to seq_S[i-1].  classify_pos expects 0-indexed
    sequence positions, so we subtract 1 before dispatching.
    """
    return classify_pos(tok - 1) if tok > 0 else "other"

# Extract contact head params (for differentiable metric)
contact_head_module = esm_model.esm.contact_head
EOS_IDX             = contact_head_module.eos_idx
REGRESSION_WEIGHT   = contact_head_module.regression.weight.detach()  # (1, NUM_LAYERS*NUM_HEADS)
REGRESSION_BIAS     = contact_head_module.regression.bias.detach()    # (1,)

# %% ── Baselines (cached) ─────────────────────────────────────────────────────

_baselines_pt = CACHE_DIR / "baselines.pt"
_force        = cfg["force_recalc"]

if _cache_valid(_baselines_pt, _BASE_KEY, _force):
    print("Loading baselines from cache...")
    _bd = torch.load(_baselines_pt, map_location="cpu", weights_only=False)
    orig_contacts_AA    = _bd["orig_contacts_AA"]
    clean_contacts_AA   = _bd["clean_contacts_AA"]
    corrupt_contacts_AA = _bd["corrupt_contacts_AA"]
    clean_metric        = _bd["clean_metric"]
    corrupt_metric      = _bd["corrupt_metric"]
else:
    print("Computing contact-map baselines...")
    orig_contacts_AA    = compute_contact_map(esm_model, tokenizer, sequence_S,    device)
    clean_contacts_AA   = compute_contact_map(esm_model, tokenizer, clean_seq_S,   device)
    corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, device)
    clean_metric   = patching_metric(clean_contacts_AA,   orig_contacts_AA, seg)
    corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)
    _cache_save(_baselines_pt, {
        "orig_contacts_AA":    orig_contacts_AA,
        "clean_contacts_AA":   clean_contacts_AA,
        "corrupt_contacts_AA": corrupt_contacts_AA,
        "clean_metric":        clean_metric,
        "corrupt_metric":      corrupt_metric,
    }, _BASE_KEY)

print(f"Clean metric   : {clean_metric:.4f}")
print(f"Corrupt metric : {corrupt_metric:.4f}")
print(f"Gap            : {clean_metric - corrupt_metric:.4f}")

ORIG_SEG = orig_contacts_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end].to(device)

# %% ── Attention Cache (cached) ───────────────────────────────────────────────

_attn_pt = CACHE_DIR / "attn_cache.pt"

if _cache_valid(_attn_pt, _BASE_KEY, _force):
    print("Loading attention cache from disk...")
    _ad = torch.load(_attn_pt, map_location="cpu", weights_only=False)
    clean_attn_LBHLL   = list(_ad["clean_attn_LBHLL"])
    corrupt_attn_LBHLL = list(_ad["corrupt_attn_LBHLL"])
    clean_inputs_BL    = {k: v.to(device) for k, v in _ad["clean_inputs_cpu"].items()}
    corrupt_inputs_BL  = {k: v.to(device) for k, v in _ad["corrupt_inputs_cpu"].items()}
else:
    print("Caching attention for clean + corrupt sequences...")
    clean_attn_LBHLL,   clean_inputs_BL   = cache_attention_all_layers(
        model, tokenizer, clean_seq_S,   device, NUM_LAYERS)
    corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention_all_layers(
        model, tokenizer, corrupt_seq_S, device, NUM_LAYERS)
    _cache_save(_attn_pt, {
        "clean_attn_LBHLL":   clean_attn_LBHLL,
        "corrupt_attn_LBHLL": corrupt_attn_LBHLL,
        "clean_inputs_cpu":   {k: v.cpu() for k, v in clean_inputs_BL.items()},
        "corrupt_inputs_cpu": {k: v.cpu() for k, v in corrupt_inputs_BL.items()},
    }, _BASE_KEY)

B = clean_attn_LBHLL[0].shape[0]    # batch size (1)
L = clean_attn_LBHLL[0].shape[-1]   # seq len with special tokens
print(f"L={L}  attention per layer: ({B}, {NUM_HEADS}, {L}, {L})")

# %% ── Indirect Effects (cached) ──────────────────────────────────────────────

_ie_pt = CACHE_DIR / "indirect_effects.pt"


def indirect_effect_single_head(
    model,
    clean_inputs_BL: dict,
    corrupt_head_attn_LL: torch.Tensor,
    patch_layer: int,
    patch_head: int,
    device: str,
) -> list[torch.Tensor]:
    """
    Perform indirect effect patching for a single head in a single trace.

    Accesses V (child) and attention probs (parent) in the same trace,
    patches one head, recomputes context, and captures downstream attention.
    Uses tracer.cache() which works reliably even in complex traces
    (unlike .save() loops — see test_nnsight_gotcha.py).

    Args:
        corrupt_head_attn_LL: Corrupt attention for the target head, shape (1, L, L)
        patch_layer: Layer to intervene at
        patch_head: Head to replace with corrupt attention

    Returns:
        downstream_attn: list of attention tensors for layers patch_layer+1..end
    """
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            # Child module first: get V (value projection)
            v_raw = model.esm.encoder.layer[patch_layer].attention.self.value.output
            v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

            # Parent module: get live attention probs, patch one head
            orig_attn = model.esm.encoder.layer[patch_layer].attention.self.output[1]
            patched_attn = orig_attn.clone()
            patched_attn[:, patch_head, :, :] = corrupt_head_attn_LL.to(device)

            # Recompute context with patched attention
            new_ctx = torch.matmul(patched_attn, v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)

            # Set context vector — this propagates through the residual stream
            model.esm.encoder.layer[patch_layer].attention.self.output[0][:] = new_ctx

            # Capture all downstream attention
            downstream_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self
                         for i in range(patch_layer + 1, NUM_LAYERS)]
            )

    downstream_attn = []
    for i in range(patch_layer + 1, NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        downstream_attn.append(downstream_cache[key].output[1].detach().cpu())

    return downstream_attn


if _cache_valid(_ie_pt, _BASE_KEY, _force):
    print("Loading indirect effects from cache...")
    _ied = torch.load(_ie_pt, map_location="cpu", weights_only=False)
    indirect_effects_LH = _ied["indirect_effects_LH"]
else:
    print("Computing indirect effects (660 traces)...")
    indirect_effects_LH = torch.zeros(NUM_LAYERS, NUM_HEADS)

    for layer_idx in range(NUM_LAYERS):
        for head_idx in range(NUM_HEADS):
            corrupt_head_attn_LL = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]

            downstream_attn = indirect_effect_single_head(
                model, clean_inputs_BL,
                corrupt_head_attn_LL,
                layer_idx, head_idx, device,
            )

            # Build full attention list for contact prediction:
            # - Layers 0..patch_layer: clean attention (unaffected)
            # - Layer patch_layer: patched attention (clean with one corrupt head)
            # - Layers patch_layer+1..end: downstream attention (from intervention)
            patched_full_attn = list(clean_attn_LBHLL[:layer_idx])

            patched_layer_attn = clean_attn_LBHLL[layer_idx].clone()
            patched_layer_attn[:, head_idx, :, :] = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]
            patched_full_attn.append(patched_layer_attn)

            patched_full_attn.extend(downstream_attn)

            indirect_contacts_AA = compute_contacts_from_attention(
                patched_full_attn,
                clean_inputs_BL['input_ids'],
                clean_inputs_BL['attention_mask'],
                esm_model.esm.contact_head,
                device=device,
            )[0].detach().cpu()

            indirect_metric = patching_metric(indirect_contacts_AA, orig_contacts_AA, seg)
            if abs(corrupt_metric - clean_metric) > 1e-6:
                effect = (indirect_metric - clean_metric) / (corrupt_metric - clean_metric)
            else:
                effect = 0.0
            indirect_effects_LH[layer_idx, head_idx] = effect

        if (layer_idx + 1) % 5 == 0:
            print(f"    Processed layer {layer_idx + 1}/{NUM_LAYERS}")

    _cache_save(_ie_pt, {"indirect_effects_LH": indirect_effects_LH}, _BASE_KEY)

# %% ── Circuit Discovery (cached) ─────────────────────────────────────────────

indirect_flat = indirect_effects_LH.flatten()
total_heads   = NUM_LAYERS * NUM_HEADS  # 660

# Three sort orders
sort_configs = {
    "abs": indirect_flat.abs().argsort(descending=True),
    "pos": indirect_flat.argsort(descending=True),
    "neg": indirect_flat.argsort(descending=False),
}
sorted_heads_by_config = {}
for name, indices in sort_configs.items():
    sorted_heads_by_config[name] = [
        (idx.item() // NUM_HEADS, idx.item() % NUM_HEADS) for idx in indices
    ]

# k values: fine near start and around expected threshold (100-300), coarser at tail
k_values = list(range(0, min(31, total_heads)))
k_values += list(range(35, min(150, total_heads), 5))
# k_values += list(range(101552, min(351, total_heads), 5))
k_values += list(range(150, total_heads, 50))
k_values.append(total_heads)
k_values = sorted(set(k_values))

_circuit_pt = CACHE_DIR / "circuit_results.pt"


def run_circuit_experiment(sorted_heads_list, label):
    """Run greedy unpatching experiment for a given head ordering."""
    print(f"\n  [{label}] Running {len(k_values)} k-values...")
    scores = []

    for k_idx, k in enumerate(k_values):
        unpatched_set = set(sorted_heads_list[:k])

        with model.trace() as tracer:
            with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
                # Cache BEFORE interventions (tracer.cache skips already-hooked modules)
                attn_cache = tracer.cache(
                    modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
                )

                for layer_idx in range(NUM_LAYERS):
                    heads_to_patch = [h for h in range(NUM_HEADS) if (layer_idx, h) not in unpatched_set]

                    if not heads_to_patch:
                        continue

                    v_raw = model.esm.encoder.layer[layer_idx].attention.self.value.output
                    v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                    attn_probs = model.esm.encoder.layer[layer_idx].attention.self.output[1]
                    patched_attn = attn_probs.clone()
                    for h in heads_to_patch:
                        patched_attn[:, h, :, :] = corrupt_attn_LBHLL[layer_idx][:, h, :, :].to(device)

                    new_ctx = torch.matmul(patched_attn, v_heads)
                    new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)
                    model.esm.encoder.layer[layer_idx].attention.self.output[0][:] = new_ctx

        attn_list = []
        for i in range(NUM_LAYERS):
            key = f"model.esm.encoder.layer.{i}.attention.self"
            layer_attn = attn_cache[key].output[1].detach().cpu()
            heads_patched = [h for h in range(NUM_HEADS) if (i, h) not in unpatched_set]
            for h in heads_patched:
                layer_attn[:, h, :, :] = corrupt_attn_LBHLL[i][:, h, :, :]
            attn_list.append(layer_attn)

        contacts_AA = compute_contacts_from_attention(
            attn_list, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
            esm_model.esm.contact_head, device=device,
        )[0].detach().cpu()

        score = patching_metric(contacts_AA, orig_contacts_AA, seg)
        scores.append(score)

        if k <= 10 or k_idx % 20 == 0:
            faith = faithfulness(score, clean_metric, corrupt_metric)
            print(f"    k={k:4d}: faithfulness={faith:.2%}")

    print(f"    Done!")
    return list(k_values), scores


if _cache_valid(_circuit_pt, _BASE_KEY, _force):
    print("Loading circuit results from cache...")
    _cd = torch.load(_circuit_pt, map_location="cpu", weights_only=False)
    circuit_results = _cd["circuit_results"]
    # Recompute crossed_k using current FAITH_TARGET (cached value may be stale)
    for _sname in circuit_results:
        _cr = circuit_results[_sname]
        _crossed = None
        for _kv, _fv in zip(_cr["k"], _cr["faith"]):
            if _fv >= FAITH_TARGET:
                _crossed = _kv
                break
        _cr["crossed_k"] = _crossed
else:
    print(f"Circuit discovery: {len(k_values)} k-values, 3 sort orders")
    print(f"  Baseline: clean={clean_metric:.4f}, corrupt={corrupt_metric:.4f}, "
          f"gap={clean_metric - corrupt_metric:.4f}")
    circuit_results = {}
    for sort_name, sort_label in [("abs", "|indirect|"), ("pos", "positive IE"), ("neg", "negative IE")]:
        kv, sc = run_circuit_experiment(sorted_heads_by_config[sort_name], sort_label)
        faith = [faithfulness(s, clean_metric, corrupt_metric) for s in sc]
        crossed = None
        for k_val, f_val in zip(kv, faith):
            if f_val >= FAITH_TARGET:
                crossed = k_val
                break
        circuit_results[sort_name] = {"k": kv, "scores": sc, "faith": faith, "crossed_k": crossed}
    _cache_save(_circuit_pt, {"circuit_results": circuit_results}, _BASE_KEY)

crossed_k = circuit_results["pos"]["crossed_k"]
if crossed_k is None:
    import warnings
    warnings.warn(
        f"Faithfulness target {FAITH_TARGET:.0%} never reached for positive IE sort; "
        f"using topk_heads={cfg['topk_heads']} as fallback."
    )
    crossed_k = cfg["topk_heads"]

top_ie_heads = sorted_heads_by_config["pos"][:crossed_k]
print(f"\nCrossed faithfulness target at k={crossed_k}")

# %% ── Cell Attribution / Gradient (cached) ──────────────────────────────────

_CELL_KEY = {**_BASE_KEY, "crossed_k": crossed_k}
_cell_pt  = CACHE_DIR / "cell_attr.pt"

if _cache_valid(_cell_pt, _CELL_KEY, _force):
    print("Loading cell attributions from cache...")
    _cacd            = torch.load(_cell_pt, map_location="cpu", weights_only=False)
    cell_attributions = _cacd["cell_attributions"]
    cell_attr_sorted  = _cacd["cell_attr_sorted"]
    all_attrs         = _cacd["all_attrs"]
else:
    # --- Step 1: Forward pass through FULL model, capture output[0], V, output[1] ---
    print("Running forward pass with hooks...")
    saved_hooks: dict = {}
    hooks = []

    for l in range(NUM_LAYERS):
        def v_hook(module, input, output, l=l):
            output.retain_grad()
            saved_hooks[f'v_{l}'] = output
        hooks.append(esm_model.esm.encoder.layer[l].attention.self.value.register_forward_hook(v_hook))

        def self_hook(module, input, output, l=l):
            context, attn_weights = output
            context.retain_grad()
            attn_weights.retain_grad()
            saved_hooks[f'ctx_{l}'] = context
            saved_hooks[f'attn_{l}'] = attn_weights
        hooks.append(esm_model.esm.encoder.layer[l].attention.self.register_forward_hook(self_hook))

    # Forward pass (clean inputs, gradients enabled)
    esm_model(**{**clean_inputs_BL, "output_attentions": True})

    # --- Step 2: Compute metric from captured attention weights (in autograd graph) ---
    attn_from_hooks = [saved_hooks[f'attn_{l}'] for l in range(NUM_LAYERS)]
    ie_attr_metric = contact_metric_from_attn_proxies(
        attn_from_hooks,
        clean_inputs_BL['input_ids'],
        clean_inputs_BL['attention_mask'],
        EOS_IDX, REGRESSION_WEIGHT, REGRESSION_BIAS, ORIG_SEG, seg,
    )
    print(f"Clean metric (from hooks): {ie_attr_metric.item():.4f}")

    # --- Step 3: Backward through FULL model ---
    ie_attr_metric.backward()

    # Remove hooks
    for h in hooks:
        h.remove()

    print("Backward complete. Computing indirect attributions...")

    # --- Step 4: Compute per-cell indirect attribution ---
    # For cell (l, h, q, k) with diff d = (clean - corrupt)[l,h,q,k]:
    #   delta_ctx[q, h*HD:(h+1)*HD] = d * V_heads[h, k, :]
    #   indirect_attr = d * dot(V_heads[h, k, :], grad_ctx[q, h_slice])
    #
    # Vectorized per (layer, head):
    #   V_h = V_heads[h, :, :]  shape (L, HD)
    #   grad_h = grad_ctx[:, h*HD:(h+1)*HD]  shape (L, HD)
    #   sensitivity = grad_h @ V_h.T  shape (L_q, L_k)
    #   attr = diff[h] * sensitivity

    cell_attributions = []  # (layer, head, q, k, total_attr, abs_diff)

    for layer, head in top_ie_heads:
        # V reshaped to heads: (B, L, hidden) → (B, num_heads, L, head_dim)
        v_full  = saved_hooks[f'v_{layer}'].detach()  # (B, L, hidden)
        v_heads = v_full.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)  # (B, H, L, HD)
        v_h     = v_heads[0, head]  # (L, HD)

        # --- Indirect sensitivity: through ctx → residual → downstream attn ---
        grad_ctx = saved_hooks[f'ctx_{layer}'].grad  # (B, L, hidden)
        if grad_ctx is None:
            indirect_sensitivity_LL = torch.zeros(L, L, device=device)
        else:
            grad_h = grad_ctx[0, :, head * HEAD_DIM:(head + 1) * HEAD_DIM]  # (L, HD)
            indirect_sensitivity_LL = grad_h @ v_h.T  # (L, L)

        # --- Direct sensitivity: attn[l,h] → contact head → metric ---
        grad_attn = saved_hooks[f'attn_{layer}'].grad  # (B, H, L, L)
        if grad_attn is not None:
            direct_sensitivity_LL = grad_attn[0, head]  # (L, L)
        else:
            direct_sensitivity_LL = torch.zeros(L, L, device=device)

        # Total attribution = indirect + direct
        sensitivity_LL = indirect_sensitivity_LL + direct_sensitivity_LL

        clean_LL   = clean_attn_LBHLL[layer][0, head].to(device)
        corrupt_LL = corrupt_attn_LBHLL[layer][0, head].to(device)
        diff_LL    = clean_LL - corrupt_LL
        attr_LL    = (diff_LL * sensitivity_LL).cpu()
        abs_diff_LL = diff_LL.abs().cpu()

        # Collect nonzero cells
        nonzero_mask = abs_diff_LL > 1e-6
        qs, ks = torch.where(nonzero_mask)
        for q, k in zip(qs.tolist(), ks.tolist()):
            cell_attributions.append((
                layer, head, q, k,
                attr_LL[q, k].item(),
                abs_diff_LL[q, k].item(),
            ))

    del saved_hooks
    clear_memory()

    cell_attr_sorted = sorted(cell_attributions, key=lambda x: x[4], reverse=True)
    all_attrs = torch.tensor([c[4] for c in cell_attr_sorted])

    _cache_save(_cell_pt, {
        "cell_attributions": cell_attributions,
        "cell_attr_sorted":  cell_attr_sorted,
        "all_attrs":         all_attrs,
    }, _CELL_KEY)

# Print distribution stats
print(f"\nTotal cells with attribution: {len(cell_attr_sorted):,d}")
print(f"\nTop 20 cells by attribution (positive = helpful):")
print(f"  (= indirect via residual stream + direct via contact head)")
print(f"{'Layer':>5} {'Head':>4} {'q(0-idx)':>9} {'k(0-idx)':>9} {'attr':>12} {'|diff|':>10}")
print("-" * 58)
for layer, head, q, k, attr, adiff in cell_attr_sorted[:20]:
    print(f"  L{layer:2d}  H{head:2d}  {q-1:>8d}  {k-1:>8d}  {attr:>+11.6f}  {adiff:>10.6f}")

print(f"\nBottom 20 cells (negative = harmful):")
for layer, head, q, k, attr, adiff in cell_attr_sorted[-20:]:
    print(f"  L{layer:2d}  H{head:2d}  {q-1:>8d}  {k-1:>8d}  {attr:>+11.6f}  {adiff:>10.6f}")

print(f"\nAttribution distribution (indirect + direct):")
print(f"  Positive: {(all_attrs > 0).sum().item():,d} cells")
print(f"  Negative: {(all_attrs < 0).sum().item():,d} cells")
for pct in [90, 95, 99, 99.5, 99.9]:
    val     = torch.quantile(all_attrs, pct / 100).item()
    n_above = (all_attrs >= val).sum().item()
    print(f"  {pct}th percentile: {val:+.8f}  ({n_above:,d} cells above)")

# %% ── Sufficiency Test ────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print("INDIRECT ATTRIBUTION-RANKED SUFFICIENCY TEST")
print(f"{'='*60}")

attr_thresholds = [t for t in cfg["attr_thresholds"] if t <= len(cell_attr_sorted)]
attr_sufficiency_results = []

for k in attr_thresholds:
    # Top-K by attribution are protected
    protected_cells: set = set()
    for layer, head, q, kk, attr, adiff in cell_attr_sorted[:k]:
        protected_cells.add((layer, head, q, kk))

    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
            )

            for layer_idx in range(NUM_LAYERS):
                v_raw = model.esm.encoder.layer[layer_idx].attention.self.value.output
                v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                attn_probs = model.esm.encoder.layer[layer_idx].attention.self.output[1]

                patched_attn = corrupt_attn_LBHLL[layer_idx].to(device).clone()

                for head, q, kk in [(h, q, kk) for (l, h, q, kk) in protected_cells if l == layer_idx]:
                    patched_attn[:, head, q, kk] = attn_probs[:, head, q, kk]

                new_ctx = torch.matmul(patched_attn, v_heads)
                new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)
                model.esm.encoder.layer[layer_idx].attention.self.output[0][:] = new_ctx

    attn_list = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        corrupt_layer = corrupt_attn_LBHLL[i].clone()
        for head, q, kk in [(h, q, kk) for (l, h, q, kk) in protected_cells if l == i]:
            corrupt_layer[:, head, q, kk] = layer_attn[:, head, q, kk]
        attn_list.append(corrupt_layer)

    contacts = compute_contacts_from_attention(
        attn_list, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()

    metric      = patching_metric(contacts, orig_contacts_AA, seg)
    faith_score = faithfulness(metric, clean_metric, corrupt_metric)

    n_heads = len(set((l, h) for l, h, q, kk in protected_cells))
    attr_sufficiency_results.append({
        'k': k, 'n_protected': len(protected_cells),
        'n_heads': n_heads,
        'metric': metric, 'faithfulness': faith_score,
    })
    print(f"  Top {k:5d} protected ({len(protected_cells):,d} cells) → "
          f"metric={metric:.4f}, faithfulness={faith_score:.2%}")

# %% ── Motif Analysis ──────────────────────────────────────────────────────────

TOPK_CELL  = cfg["topk_cell"]
TOPK_HEADS = cfg["topk_heads"]
ie_circuit_cells = cell_attr_sorted[:TOPK_CELL]

# IE rank lookup (original attribution-ranking order)
ie_rank = {(l, h): i + 1 for i, (l, h) in enumerate(top_ie_heads[:TOPK_HEADS])}

# Display in (layer, head) order
heads_sorted = sorted(top_ie_heads[:TOPK_HEADS], key=lambda x: (x[0], x[1]))

# Regions (same indexing as q/k values in cells)
SS1     = set(range(seg.ss1_start, seg.ss1_end))
SS2     = set(range(seg.ss2_start, seg.ss2_end))
FLANK_L = set(range(max(0, seg.ss1_start - CLEAN_FLANK), seg.ss1_start))
FLANK_R = set(range(seg.ss2_end, seg.ss2_end + CLEAN_FLANK))
SSE_GAP = seg.ss2_start - seg.ss1_start  # offset between the two contact residues

# Classification thresholds (from config)
ANCHOR_T1    = cfg["anchor_t1"]
ANCHOR_T2    = cfg["anchor_t2"]
ANCHOR_T3    = cfg["anchor_t3"]
POSITIONAL_T = cfg["positional_t"]
# Regions on each "side" of the contact pair (for cross-region tagging)
LEFT_REGIONS  = {"ss1", "flkL"}
RIGHT_REGIONS = {"ss2", "flkR"}
RPAIR_T = 0.40  # min fraction for a region pair to be called "dominant"

# --- Load path patching data ---
path_pt = REPORT_DIR / f"{PROTEIN}_path_patching_full.pt"
path_srcdst: dict = {}

if path_pt.exists():
    path_data  = torch.load(path_pt, map_location='cpu', weights_only=False)
    pass_d_all = path_data['pass_d_results']
    top_paths  = sorted(pass_d_all, key=lambda x: abs(x['pass_d_effect']), reverse=True)[:cfg["path_top_n"]]
    print(f"Loaded {len(pass_d_all)} paths, using top {cfg['path_top_n']}")
    for r in top_paths:
        sl, sh = int(r['source'][0]), int(r['source'][1])
        dl, dh = int(r['dest'][0]),   int(r['dest'][1])
        ch, eff = r['channel'], r['pass_d_effect']
        path_srcdst.setdefault((sl, sh), {'as_src': [], 'as_dst': []})['as_src'].append((dl, dh, ch, eff))
        path_srcdst.setdefault((dl, dh), {'as_src': [], 'as_dst': []})['as_dst'].append((sl, sh, ch, eff))
    for info in path_srcdst.values():
        info['as_src'].sort(key=lambda x: abs(x[3]), reverse=True)
        info['as_dst'].sort(key=lambda x: abs(x[3]), reverse=True)
else:
    print(f"Warning: no path patching file at {path_pt}")

print(f"\n{'='*70}")
print(f"MOTIF ANALYSIS — top {TOPK_CELL} cells by attribution")
print(f"  All positions are 0-indexed sequence positions (same as CONTACT_PAIR).")
print(f"  Internally cells store token indices (BOS=0); displayed as tok-1.")
print(f"{'='*70}")
print(f"  ss1={seg.ss1_start}–{seg.ss1_end-1}  "
      f"ss2={seg.ss2_start}–{seg.ss2_end-1}  "
      f"flkL={seg.ss1_start - CLEAN_FLANK}–{seg.ss1_start-1}  "
      f"flkR={seg.ss2_end}–{seg.ss2_end + CLEAN_FLANK-1}  "
      f"SSE_GAP={SSE_GAP}")
print()

summary_rows = []
motif_data   = []

for l, h in heads_sorted:
    rank = ie_rank[(l, h)]
    head_cells = [(q, k, attr, adiff)
                  for (ll, hh, q, k, attr, adiff) in ie_circuit_cells
                  if ll == l and hh == h]
    n_cells    = len(head_cells)
    total_attr = sum(a for _, _, a, _ in head_cells)

    if n_cells == 0:
        summary_rows.append((rank, l, h, 0, 0.0, "—", "", "—", ""))
        motif_data.append({
            "rank": rank, "layer": l, "head": h, "n_cells": 0,
            "total_attr": 0.0, "anchor": "—", "pos_tag": "",
            "t1": 0.0, "t2": 0.0, "t3": 0.0,
            "q_anchor": "—", "qt1": 0.0, "qt2": 0.0, "qt3": 0.0,
            "k_conc_lbl": "", "q_conc_lbl": "",
            "key_sorted": [], "qry_sorted": [], "off_sorted": [],
            "top_cells": [], "top2_off_frac": 0.0,
            "rpair_sorted": [], "top_rpair_frac": 0.0, "region_tag": "",
            "paths": {"as_src": [], "as_dst": []},
        })
        print(f"  L{l:2d} H{h:2d} [rank#{rank:2d}]: 0 cells in top-{TOPK_CELL}")
        continue

    # Key mass: signed sum per key position
    key_mass = defaultdict(float)
    for q, k, attr, _ in head_cells:
        key_mass[k] += attr
    key_sorted  = sorted(key_mass.items(), key=lambda x: x[1], reverse=True)
    total_abs_k = sum(abs(v) for v in key_mass.values())

    # Query mass: signed sum per query position
    qry_mass = defaultdict(float)
    for q, k, attr, _ in head_cells:
        qry_mass[q] += attr
    qry_sorted  = sorted(qry_mass.items(), key=lambda x: x[1], reverse=True)
    total_abs_q = sum(abs(v) for v in qry_mass.values())

    # Query anchor classification (mirrors key anchor)
    qt1 = abs(qry_sorted[0][1]) / total_abs_q if total_abs_q and qry_sorted else 0.0
    qt2 = sum(abs(qry_sorted[i][1]) for i in range(min(2, len(qry_sorted)))) / total_abs_q if total_abs_q else 0.0
    qt3 = sum(abs(qry_sorted[i][1]) for i in range(min(3, len(qry_sorted)))) / total_abs_q if total_abs_q else 0.0
    q_anchor = ("SINGLE-ANCHOR" if qt1 >= ANCHOR_T1 else
                "DUAL-ANCHOR"   if qt2 >= ANCHOR_T2 else
                "MULTI-ANCHOR"  if qt3 >= ANCHOR_T3 else
                "DISTRIBUTED")

    # Offset distribution (q - k), frequency-based (each cell counts once)
    off_count = defaultdict(int)
    for q, k, attr, _ in head_cells:
        off_count[q - k] += 1
    off_sorted = sorted(off_count.items(), key=lambda x: x[1], reverse=True)
    total_off  = sum(off_count.values())

    # Anchor classification
    t1 = abs(key_sorted[0][1]) / total_abs_k if total_abs_k else 0.0
    t2 = sum(abs(key_sorted[i][1]) for i in range(min(2, len(key_sorted)))) / total_abs_k if total_abs_k else 0.0
    t3 = sum(abs(key_sorted[i][1]) for i in range(min(3, len(key_sorted)))) / total_abs_k if total_abs_k else 0.0
    anchor = ("SINGLE-ANCHOR" if t1 >= ANCHOR_T1 else
              "DUAL-ANCHOR"   if t2 >= ANCHOR_T2 else
              "MULTI-ANCHOR"  if t3 >= ANCHOR_T3 else
              "DISTRIBUTED")

    # Concentrated-label for DISTRIBUTED dimensions: list top positions by abs mass
    k_conc_lbl = (_distr_label(key_mass, total_abs_k, sequence_S)
                  if anchor == "DISTRIBUTED" else "")
    q_conc_lbl = (_distr_label(qry_mass, total_abs_q, sequence_S)
                  if q_anchor == "DISTRIBUTED" else "")

    # Region-pair profile (q_region → k_region), frequency-based
    rpair_count = defaultdict(int)
    for q, k, attr, _ in head_cells:
        rpair_count[(_cpos(q), _cpos(k))] += 1
    rpair_sorted   = sorted(rpair_count.items(), key=lambda x: x[1], reverse=True)
    top_rpair_frac = rpair_sorted[0][1] / n_cells if rpair_sorted else 0.0

    # Region-pair tag: label the dominant cross-region pattern
    _qr0, _kr0 = rpair_sorted[0][0] if rpair_sorted else ("other", "other")
    if top_rpair_frac >= RPAIR_T and _qr0 != "other" and _kr0 != "other":
        _q_left = _qr0 in LEFT_REGIONS
        _k_left = _kr0 in LEFT_REGIONS
        if _q_left != _k_left:         # q and k on opposite sides of the contact
            region_tag = f"CROSS:{_qr0}→{_kr0}"
        elif _qr0 == _kr0:
            region_tag = f"INTRA:{_qr0}"
        else:
            region_tag = f"{_qr0}→{_kr0}"
    else:
        region_tag = ""

    # Positional classification
    top2_off_frac = sum(v for _, v in off_sorted[:2]) / total_off if total_off else 0.0
    top_offset    = off_sorted[0][0] if off_sorted else 0
    is_cross_sse  = abs(abs(top_offset) - SSE_GAP) <= 3
    if is_cross_sse and top2_off_frac >= POSITIONAL_T:
        pos_tag = "CROSS_SSE"
    elif (top2_off_frac >= POSITIONAL_T and abs(top_offset) <= 10
          and q_anchor not in ("SINGLE-ANCHOR", "DUAL-ANCHOR")):
        pos_tag = "POSITIONAL"
    else:
        pos_tag = ""

    k_disp = f"{anchor}({k_conc_lbl})" if k_conc_lbl else anchor
    q_disp = f"{q_anchor}({q_conc_lbl})" if q_conc_lbl else q_anchor
    tags = (f"k:{k_disp} / q:{q_disp}"
            + (f" | {pos_tag}" if pos_tag else "")
            + (f" | {region_tag}" if region_tag else ""))
    summary_rows.append((rank, l, h, n_cells, total_attr, anchor, pos_tag, q_anchor, region_tag))

    cells_by_attr = sorted(head_cells, key=lambda x: x[2], reverse=True)
    paths_info    = path_srcdst.get((l, h), {'as_src': [], 'as_dst': []})

    motif_data.append({
        "rank": rank, "layer": l, "head": h,
        "n_cells": n_cells, "total_attr": total_attr,
        "anchor": anchor, "pos_tag": pos_tag,
        "t1": t1, "t2": t2, "t3": t3,
        "q_anchor": q_anchor, "qt1": qt1, "qt2": qt2, "qt3": qt3,
        "k_conc_lbl": k_conc_lbl, "q_conc_lbl": q_conc_lbl,
        "key_sorted": key_sorted, "qry_sorted": qry_sorted, "off_sorted": off_sorted,
        "top_cells": cells_by_attr[:5],
        "top2_off_frac": top2_off_frac,
        "rpair_sorted": rpair_sorted, "top_rpair_frac": top_rpair_frac, "region_tag": region_tag,
        "paths": paths_info,
    })

    print(f"  L{l:2d} H{h:2d} [rank#{rank:2d}]: {n_cells} cells | attr={total_attr:+.4f} | {tags}")

    # Key mass
    print(f"       Keys  (top-1={t1:.0%}, top-2={t2:.0%}, top-3={t3:.0%}) [{k_disp}]:")
    for k_pos, k_attr in key_sorted[:5]:
        frac = abs(k_attr) / total_abs_k * 100
        bar  = "█" * int(frac / 5)
        print(f"         k={k_pos-1:>4d} [{_cpos(k_pos):5s}]  {k_attr:>+7.4f}  {frac:>5.1f}%  {bar}")
    if len(key_sorted) > 5:
        rest_pct = sum(abs(v) for _, v in key_sorted[5:]) / total_abs_k * 100
        print(f"         … {len(key_sorted)-5} more keys  ({rest_pct:.1f}% of mass)")

    # Query mass
    print(f"       Queries (top-1={qt1:.0%}, top-2={qt2:.0%}, top-3={qt3:.0%})  [{q_disp}]:")
    for q_pos, q_attr in qry_sorted[:5]:
        frac = abs(q_attr) / total_abs_q * 100
        bar  = "█" * int(frac / 5)
        print(f"         q={q_pos-1:>4d} [{_cpos(q_pos):5s}]  {q_attr:>+7.4f}  {frac:>5.1f}%  {bar}")
    if len(qry_sorted) > 5:
        rest_pct = sum(abs(v) for _, v in qry_sorted[5:]) / total_abs_q * 100
        print(f"         … {len(qry_sorted)-5} more queries  ({rest_pct:.1f}% of mass)")

    # Offset distribution
    dom_offsets = ", ".join(f"{o:+d}" for o, _ in off_sorted[:2])
    print(f"       Offsets (q−k) [freq], top-2 coverage={top2_off_frac:.0%}  [{dom_offsets}]:")
    for offset, o_count in off_sorted[:5]:
        frac = o_count / total_off * 100
        note = (" ← self"        if offset == 0 else
                " ← attend-prev" if offset == 1 else
                " ← attend-next" if offset == -1 else
                f" ← ±{abs(offset)} pos" if abs(offset) <= 5 else
                f" ← ~SSE_GAP"   if abs(abs(offset) - SSE_GAP) <= 3 else "")
        print(f"         Δ={offset:>+6d}  {frac:>5.1f}%{note}")

    # Region-pair profile
    print(f"       Region pairs (q→k) [freq]  [top={top_rpair_frac:.0%}]" +
          (f"  {region_tag}" if region_tag else "") + ":")
    for (qr, kr), cnt in rpair_sorted[:5]:
        frac = cnt / n_cells * 100
        print(f"         {qr:5s}→{kr:5s}  {cnt:3d} cells  {frac:>5.1f}%")

    # Top 5 cells
    print(f"       Top 5 cells (by attribution):")
    for q, k, attr, adiff in cells_by_attr[:5]:
        print(f"         q={q-1:>4d}[{_cpos(q):5s}]  k={k-1:>4d}[{_cpos(k):5s}]  "
              f"attr={attr:>+7.4f}  |diff|={adiff:.4f}")

    # Path patching connections
    if paths_info['as_dst']:
        print(f"       Receives from (top 5 src heads):")
        for sl, sh, ch, eff in paths_info['as_dst'][:5]:
            sl_rank = ie_rank.get((sl, sh), "–")
            print(f"         L{sl:2d}H{sh:2d} [rank#{sl_rank}] via {ch}  eff={eff:>+7.4f}")
    if paths_info['as_src']:
        print(f"       Sends to (top 5 dst heads):")
        for dl, dh, ch, eff in paths_info['as_src'][:5]:
            dl_rank = ie_rank.get((dl, dh), "–")
            print(f"         L{dl:2d}H{dh:2d} [rank#{dl_rank}] via {ch}  eff={eff:>+7.4f}")
    print()

# Compact summary table
print(f"\n{'='*70}")
print(f"SUMMARY  (top-{TOPK_CELL} cells, ordered by layer/head)")
print(f"{'='*70}")
print(f"{'rank':>5} {'L':>3} {'H':>3} {'cells':>6} {'total_attr':>11}  {'k_anchor(label)':>22} / {'q_anchor(label)':>22}  {'pos':>10}  {'region'}")
print("-" * 100)
for rank, l, h, n, attr, anchor, pos_tag, q_anchor, region_tag in sorted(summary_rows, key=lambda x: (x[1], x[2])):
    # Find matching motif entry for anchor labels
    _md = next((m for m in motif_data if m["layer"] == l and m["head"] == h), {})
    if anchor == "DISTRIBUTED":
        _kl = _md.get("k_conc_lbl", "")
        k_str = f"DISTR({_kl})" if _kl else "DISTRIBUTED"
    else:
        _kl = _anchor_label(anchor, _md.get("key_sorted", []), sequence_S)
        k_str = f"{anchor}({_kl})" if _kl else anchor
    if q_anchor == "DISTRIBUTED":
        _ql = _md.get("q_conc_lbl", "")
        q_str = f"DISTR({_ql})" if _ql else "DISTRIBUTED"
    else:
        _ql = _anchor_label(q_anchor, _md.get("qry_sorted", []), sequence_S)
        q_str = f"{q_anchor}({_ql})" if _ql else q_anchor
    print(f" #{rank:2d}   L{l:2d} H{h:2d}  {n:>5d}  {attr:>+10.4f}  {k_str:>22} / {q_str:>22}  {pos_tag:>10}  {region_tag}")

# %% ── Report Generation ───────────────────────────────────────────────────────


def _make_report() -> str:
    lines: list[str] = []
    a = lines.append

    a(f"# Contact Pattern Analysis: {PROTEIN}")
    a(f"")
    a(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   Model: {MODEL_NAME}")
    a(f"")
    a(f"> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,")
    a(f"> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.")
    a(f"")

    # ── Configuration ──────────────────────────────────────────────────────
    a(f"## Configuration")
    a(f"")
    a(f"| Parameter | Value |")
    a(f"|-----------|-------|")
    a(f"| Protein | {PROTEIN} |")
    a(f"| Contact pair | {CONTACT_PAIR} |")
    a(f"| ss1 | [{seg.ss1_start}, {seg.ss1_end}) |")
    a(f"| ss2 | [{seg.ss2_start}, {seg.ss2_end}) |")
    a(f"| Clean flank | {CLEAN_FLANK} |")
    a(f"| Corrupt flank | {CORRUPT_FLANK} |")
    a(f"| Segment radius | {SEGMENT_RADIUS} |")
    a(f"| Faith target | {FAITH_TARGET:.0%} |")
    a(f"| Model dims | {NUM_LAYERS}L × {NUM_HEADS}H, head_dim={HEAD_DIM} |")
    a(f"| topk_cell | {TOPK_CELL} |")
    a(f"| topk_heads | {TOPK_HEADS} |")
    a(f"")

    # ── Baselines ──────────────────────────────────────────────────────────
    a(f"## Baselines")
    a(f"")
    a(f"| Metric | Value |")
    a(f"|--------|-------|")
    a(f"| Clean metric | {clean_metric:.4f} |")
    a(f"| Corrupt metric | {corrupt_metric:.4f} |")
    a(f"| Gap | {clean_metric - corrupt_metric:.4f} |")
    a(f"")

    # ── Circuit Discovery ──────────────────────────────────────────────────
    a(f"## Circuit Discovery")
    a(f"")
    a(f"### Minimum K to Reach Faithfulness Target ({FAITH_TARGET:.0%})")
    a(f"")
    a(f"| Sort order | min_K | faithfulness_at_K |")
    a(f"|------------|-------|-------------------|")
    for sname, slabel in [("abs", "|indirect|"), ("pos", "positive IE"), ("neg", "negative IE")]:
        cr = circuit_results[sname]
        ck = cr["crossed_k"]
        if ck is not None:
            idx = cr["k"].index(ck)
            fv  = cr["faith"][idx]
            a(f"| {slabel} | {ck} | {fv:.2%} |")
        else:
            a(f"| {slabel} | — | never reached |")
    a(f"")

    a(f"### Top Indirect Effect Heads (by positive IE)")
    a(f"")
    a(f"| Rank | Layer | Head | IE score |")
    a(f"|------|-------|------|----------|")
    for rank_i, (li, hi) in enumerate(sorted_heads_by_config["pos"][:TOPK_HEADS], 1):
        ie_val = indirect_effects_LH[li, hi].item()
        a(f"| {rank_i} | L{li} | H{hi} | {ie_val:+.4f} |")
    a(f"")

    a(f"### Faithfulness Sweep (Positive IE)")
    a(f"")
    a(f"| k | faithfulness |")
    a(f"|---|--------------|")
    cr_pos = circuit_results["pos"]
    kv, fv = cr_pos["k"], cr_pos["faith"]
    shown: set = set()
    for i, k in enumerate(kv):
        if k <= 10 or i % 20 == 0:
            shown.add(i)
    for i in sorted(shown):
        a(f"| {kv[i]} | {fv[i]:.2%} |")
    a(f"")

    # ── Cell Attribution ───────────────────────────────────────────────────
    a(f"## Cell Attribution Analysis")
    a(f"")
    a(f"Total cells: {len(cell_attr_sorted):,}")
    a(f"")
    a(f"- Positive: {(all_attrs > 0).sum().item():,}")
    a(f"- Negative: {(all_attrs < 0).sum().item():,}")
    a(f"")
    a(f"**Percentile table:**")
    a(f"")
    a(f"| Percentile | Value | Cells above |")
    a(f"|------------|-------|-------------|")
    for pct in [90, 95, 99, 99.5, 99.9]:
        val     = torch.quantile(all_attrs, pct / 100).item()
        n_above = (all_attrs >= val).sum().item()
        a(f"| {pct}th | {val:+.8f} | {n_above:,} |")
    a(f"")

    a(f"**Top 20 positive cells:**")
    a(f"")
    a(f"| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |")
    a(f"|-------|------|---|----------|---|----------|------|--------|")
    for layer, head, q, k, attr, adiff in cell_attr_sorted[:20]:
        a(f"| L{layer} | H{head} | {q-1} | {_cpos(q)} | {k-1} | {_cpos(k)} "
          f"| {attr:+.6f} | {adiff:.6f} |")
    a(f"")

    a(f"**Top 20 negative cells:**")
    a(f"")
    a(f"| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |")
    a(f"|-------|------|---|----------|---|----------|------|--------|")
    for layer, head, q, k, attr, adiff in cell_attr_sorted[-20:]:
        a(f"| L{layer} | H{head} | {q-1} | {_cpos(q)} | {k-1} | {_cpos(k)} "
          f"| {attr:+.6f} | {adiff:.6f} |")
    a(f"")

    # ── Attribution Sufficiency ────────────────────────────────────────────
    a(f"## Attribution Sufficiency Test")
    a(f"")
    a(f"| K | cells | heads | metric | faithfulness |")
    a(f"|---|-------|-------|--------|--------------|")
    for r in attr_sufficiency_results:
        a(f"| {r['k']} | {r['n_protected']:,} | {r['n_heads']} "
          f"| {r['metric']:.4f} | {r['faithfulness']:.2%} |")
    a(f"")

    # ── Motif Analysis ─────────────────────────────────────────────────────
    a(f"## Motif Analysis")
    a(f"")
    for md in motif_data:
        li, hi, rank = md["layer"], md["head"], md["rank"]
        a(f"### L{li} H{hi} — Rank #{rank}")
        a(f"")
        tags = (f"k:{md['anchor']} / q:{md['q_anchor']}"
                + (f" | {md['pos_tag']}" if md["pos_tag"] else "")
                + (f" | {md['region_tag']}" if md["region_tag"] else ""))
        a(f"**Tags:** {tags}  |  cells: {md['n_cells']}  |  total attr: {md['total_attr']:+.4f}")
        a(f"")
        if md["n_cells"] == 0:
            a(f"_No cells in top-{TOPK_CELL}_")
            a(f"")
            continue

        total_abs_k = sum(abs(v) for _, v in md["key_sorted"])
        _k_hdr = (f"DISTR({md['k_conc_lbl']})" if md["anchor"] == "DISTRIBUTED" and md.get("k_conc_lbl")
                  else md["anchor"])
        a(f"**Key mass** (top-1={md['t1']:.0%}, top-2={md['t2']:.0%}, top-3={md['t3']:.0%})  [{_k_hdr}]:")
        a(f"")
        a(f"| k pos | region | attr | fraction |")
        a(f"|-------|--------|------|----------|")
        for k_pos, k_attr in md["key_sorted"][:5]:
            frac = abs(k_attr) / total_abs_k * 100 if total_abs_k else 0.0
            a(f"| {k_pos-1} | {_cpos(k_pos)} | {k_attr:+.4f} | {frac:.1f}% |")
        a(f"")

        total_abs_q = sum(abs(v) for _, v in md["qry_sorted"])
        _q_hdr = (f"DISTR({md['q_conc_lbl']})" if md["q_anchor"] == "DISTRIBUTED" and md.get("q_conc_lbl")
                  else md["q_anchor"])
        a(f"**Query mass** (top-1={md['qt1']:.0%}, top-2={md['qt2']:.0%}, top-3={md['qt3']:.0%})  [{_q_hdr}]:")
        a(f"")
        a(f"| q pos | region | attr | fraction |")
        a(f"|-------|--------|------|----------|")
        for q_pos, q_attr in md["qry_sorted"][:5]:
            frac = abs(q_attr) / total_abs_q * 100 if total_abs_q else 0.0
            a(f"| {q_pos-1} | {_cpos(q_pos)} | {q_attr:+.4f} | {frac:.1f}% |")
        a(f"")

        total_off = sum(v for _, v in md["off_sorted"])
        a(f"**Offset distribution [frequency]** (top-2 coverage: {md['top2_off_frac']:.0%}):")
        a(f"")
        a(f"| offset (q−k) | count | fraction |")
        a(f"|--------------|-------|----------|")
        for offset, o_count in md["off_sorted"][:5]:
            frac = o_count / total_off * 100 if total_off else 0.0
            a(f"| {offset:+d} | {o_count} | {frac:.1f}% |")
        a(f"")

        _total_rp = sum(v for _, v in md["rpair_sorted"])
        _rt = (f"  [{md['region_tag']}]" if md["region_tag"] else "")
        a(f"**Region-pair profile** (q→k){_rt}  (top={md['top_rpair_frac']:.0%}):")
        a(f"")
        a(f"| q region | k region | count | fraction |")
        a(f"|----------|----------|-------|----------|")
        for (qr, kr), cnt in md["rpair_sorted"][:5]:
            frac = cnt / _total_rp * 100 if _total_rp else 0.0
            a(f"| {qr} | {kr} | {cnt} | {frac:.1f}% |")
        a(f"")

        a(f"**Top 5 cells:**")
        a(f"")
        a(f"| q | q-region | k | k-region | attr | \|diff\| |")
        a(f"|---|----------|---|----------|------|--------|")
        for q, k, attr, adiff in md["top_cells"]:
            a(f"| {q-1} | {_cpos(q)} | {k-1} | {_cpos(k)} "
              f"| {attr:+.4f} | {adiff:.4f} |")
        a(f"")

        paths = md["paths"]
        if paths["as_dst"] or paths["as_src"]:
            a(f"**Path patching connections:**")
            a(f"")
            if paths["as_dst"]:
                a(f"Receives from:")
                a(f"")
                a(f"| src | rank | channel | effect |")
                a(f"|-----|------|---------|--------|")
                for sl, sh, ch, eff in paths["as_dst"][:5]:
                    sl_rank = ie_rank.get((sl, sh), "–")
                    a(f"| L{sl}H{sh} | #{sl_rank} | {ch} | {eff:+.4f} |")
                a(f"")
            if paths["as_src"]:
                a(f"Sends to:")
                a(f"")
                a(f"| dst | rank | channel | effect |")
                a(f"|-----|------|---------|--------|")
                for dl, dh, ch, eff in paths["as_src"][:5]:
                    dl_rank = ie_rank.get((dl, dh), "–")
                    a(f"| L{dl}H{dh} | #{dl_rank} | {ch} | {eff:+.4f} |")
                a(f"")

    # ── Summary Table ──────────────────────────────────────────────────────
    a(f"## Summary Table")
    a(f"")
    a(f"| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |")
    a(f"|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|")
    for rank, l, h, n, attr, anchor, pos_tag, q_anchor, region_tag in sorted(summary_rows, key=lambda x: (x[1], x[2])):
        _md = next((m for m in motif_data if m["layer"] == l and m["head"] == h), {})
        k_lbl = (_md.get("k_conc_lbl", "") if anchor == "DISTRIBUTED"
                 else _anchor_label(anchor, _md.get("key_sorted", []), sequence_S))
        q_lbl = (_md.get("q_conc_lbl", "") if q_anchor == "DISTRIBUTED"
                 else _anchor_label(q_anchor, _md.get("qry_sorted", []), sequence_S))
        a(f"| #{rank} | L{l} | H{h} | {n} | {attr:+.4f} | {anchor} | {k_lbl} | {q_anchor} | {q_lbl} | {pos_tag} | {region_tag} |")
    a(f"")

    return "\n".join(lines)


report_path = REPORT_DIR / f"{PROTEIN}_contact_report.md"
report_path.write_text(_make_report())
print(f"\nReport written to: {report_path}")

# ── CSV summary table ───────────────────────────────────────────────────────
csv_path = REPORT_DIR / f"{PROTEIN}_summary.csv"
with open(csv_path, "w", newline="") as _csv_f:
    _writer = csv.writer(_csv_f)
    _writer.writerow(["rank", "layer", "head", "n_cells", "total_attr",
                       "k_anchor", "k_label", "q_anchor", "q_label",
                       "pos_type", "region"])
    for rank, l, h, n, attr, anchor, pos_tag, q_anchor, region_tag in sorted(
        summary_rows, key=lambda x: (x[1], x[2])
    ):
        _md = next((m for m in motif_data if m["layer"] == l and m["head"] == h), {})
        k_lbl = (_md.get("k_conc_lbl", "") if anchor == "DISTRIBUTED"
                 else _anchor_label(anchor, _md.get("key_sorted", []), sequence_S))
        q_lbl = (_md.get("q_conc_lbl", "") if q_anchor == "DISTRIBUTED"
                 else _anchor_label(q_anchor, _md.get("qry_sorted", []), sequence_S))
        _writer.writerow([rank, l, h, n, f"{attr:.6f}",
                          anchor, k_lbl, q_anchor, q_lbl, pos_tag, region_tag])
print(f"CSV summary written to: {csv_path}")
