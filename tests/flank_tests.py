# %%


from __future__ import annotations

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

# %%


PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}

cfg = {
    "protein": "2B61A",
    "model": "facebook/esm2_t33_650M_UR50D",
    "data_path": "../data/full_seq_dict.json",
    "faith_target": 0.70,
    "segment_radius": 5,
    "force_recalc": False,
    "path_top_n": 400,
    "topk_cell": 1000,
    "topk_heads": 30,
    "anchor_t1": 0.60, "anchor_t2": 0.70, "anchor_t3": 0.80,
    "positional_t": 0.50,
    "attr_thresholds": [0, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000],
    "report_dir": "reports/outputs",
    "cache_dir": "reports/cache",
}

PROTEIN        = cfg["protein"]
MODEL_NAME     = cfg["model"]
DATA_PATH      = cfg["data_path"]
FAITH_TARGET   = cfg["faith_target"]
SEGMENT_RADIUS = cfg["segment_radius"]

_prot_cfg     = PROTEINS[PROTEIN]
CLEAN_FLANK   = _prot_cfg["clean_flank"]
CORRUPT_FLANK = _prot_cfg["corrupt_flank"]
CONTACT_PAIR  = tuple(_prot_cfg["contact_pair"])

# %%


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


def _seq_to_list(seq_S: str) -> list[str]:
    """Parse a masked sequence string back to a per-position list.

    mask_with_flanks joins a list where each slot is either a single AA char
    or the 6-char string '<mask>'.  This inverts that join.
    """
    result: list[str] = []
    i = 0
    while i < len(seq_S):
        if seq_S[i:i+6] == "<mask>":
            result.append("<mask>")
            i += 6
        else:
            result.append(seq_S[i])
            i += 1
    return result


def apply_additional_masks(
    clean_seq_S: str,
    original_seq_S: str,
    mask_indices: list[str],
    tokenizer: EsmTokenizer,
) -> str:
    """Mask extra positions on top of an already-masked clean sequence.

    Args:
        clean_seq_S:    Pre-masked sequence (output of mask_with_flanks).
        original_seq_S: Original unmasked protein sequence.
        mask_indices:   e.g. ["G159", "H355"].  Single-letter AA + 0-indexed
                        position in the *original* sequence (no BOS/EOS).
        tokenizer:      ESM tokenizer used to verify AA identity.

    Returns:
        New sequence string with the specified positions additionally masked.
    """
    tokens = tokenizer(original_seq_S, return_tensors="pt")["input_ids"][0]
    masked = _seq_to_list(clean_seq_S)
    assert len(masked) == len(original_seq_S)

    for idx_str in mask_indices:
        aa      = idx_str[0]
        seq_pos = int(idx_str[1:])

        # Verify against original sequence
        actual_aa = original_seq_S[seq_pos]
        if actual_aa != aa:
            raise ValueError(
                f"{idx_str}: expected '{aa}' at position {seq_pos}, "
                f"but original sequence has '{actual_aa}'"
            )

        # Verify against tokenized sequence (tok pos = seq_pos + 1 for BOS)
        tok_pos   = seq_pos + 1
        token_str = tokenizer.convert_ids_to_tokens([tokens[tok_pos].item()])[0]
        if token_str != aa:
            raise ValueError(
                f"{idx_str}: tokenizer mismatch at token pos {tok_pos}: "
                f"expected '{aa}', got '{token_str}'"
            )

        masked[seq_pos] = "<mask>"

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
    """Return 'AA@pos' label(s) for SINGLE/DUAL anchor types."""
    if anchor == "SINGLE-ANCHOR" and sorted_items:
        pos = sorted_items[0][0]
        aa = seq[pos - 1] if 0 < pos <= len(seq) else "?"
        return f"{aa}{pos}"
    elif anchor == "DUAL-ANCHOR" and len(sorted_items) >= 2:
        p1, p2 = sorted_items[0][0], sorted_items[1][0]
        a1 = seq[p1 - 1] if 0 < p1 <= len(seq) else "?"
        a2 = seq[p2 - 1] if 0 < p2 <= len(seq) else "?"
        return f"{a1}{p1}/{a2}{p2}"
    return ""


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
# %%
sequence_S
# %%
clean_seq_S
# %%
sequence_S_tokens = tokenizer(sequence_S, return_tensors="pt").to(device)
# %%
clean_seq_S_tokens = tokenizer(clean_seq_S, return_tensors="pt").to(device)
# %%
corrupt_seq_S_tokens = tokenizer(corrupt_seq_S, return_tensors="pt").to(device)

# %%
# Clean (larger flank - higher metric)
orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)

clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_seq_S, device)


corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, device)

# =============================================================================
# Results
# =============================================================================
# %%
print(f"\nPatching Metrics (flank size -> metric):")
print(f"  Original (full):     1.000")
print(f"  Clean (flank={CLEAN_FLANK}):   {patching_metric(clean_contacts_AA, orig_contacts_AA, seg):.4f}")
print(f"  Corrupt (flank={CORRUPT_FLANK}): {patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg):.4f}")

# %%
# Extract contact head params (for differentiable metric)
contact_head_module = esm_model.esm.contact_head
EOS_IDX             = contact_head_module.eos_idx
REGRESSION_WEIGHT   = contact_head_module.regression.weight.detach()  # (1, NUM_LAYERS*NUM_HEADS)
REGRESSION_BIAS     = contact_head_module.regression.bias.detach()    # (1,)

# %% ── Additional masking ──────────────────────────────────────────────────────
# Mask extra positions on top of clean_seq_S and compare contacts.
# Positions are 0-indexed in the original sequence (no BOS/EOS).

extra_indices = ["L146"]#"G159"]   # <-- edit this list as needed

extra_masked_seq_S  = apply_additional_masks(clean_seq_S, sequence_S, extra_indices, tokenizer)
extra_contacts_AA   = compute_contact_map(esm_model, tokenizer, extra_masked_seq_S, device)
extra_metric        = patching_metric(extra_contacts_AA, orig_contacts_AA, seg)

print(f"\nAdditional masks: {extra_indices}")
print(f"  Original (full seq):          {patching_metric(orig_contacts_AA,    orig_contacts_AA, seg):.4f}")
print(f"  Clean    (flank={CLEAN_FLANK}):        {patching_metric(clean_contacts_AA,  orig_contacts_AA, seg):.4f}")
print(f"  Extra-masked (clean + {extra_indices}): {extra_metric:.4f}")
print(f"  Corrupt  (flank={CORRUPT_FLANK}):       {patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg):.4f}")
# %%
