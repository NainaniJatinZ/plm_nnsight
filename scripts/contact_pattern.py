# %% [markdown]
# # Contact Pattern: Head-Level Attribution + Sufficiency
#
# Pipeline:
#   1. Setup: load model + data, compute baselines, cache attention
#   2. Gradient attribution: one forward+backward to score every head
#   3. Sufficiency: protect top-K positive-attr heads, corrupt rest
#      → find minimum K to reach 70% faithfulness
#   4. Motif extraction for the identified circuit heads
#
# Run as: `uv run python -u contact_pattern.py [--protein 2B61A] [--model ...]`
# Or run individual `# %%` cells in VS Code / Jupyter.

# %% ── Imports ──────────────────────────────────────────────────────────────

from __future__ import annotations

import gc
import json
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from turtle import mode

import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

# %% ── Configuration ─────────────────────────────────────────────────────────
# Edit defaults here, or pass --protein / --model on the command line.
# parse_known_args so IDE cell runners don't break on unknown args.

import argparse as _ap

PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}

if False:
    _p = _ap.ArgumentParser()
    _p.add_argument("--protein", default="2B61A",                        choices=list(PROTEINS))
    _p.add_argument("--model",   default="facebook/esm2_t33_650M_UR50D", help="HuggingFace model name")
    _p.add_argument("--data",    default="data/full_seq_dict.json")
    _p.add_argument("--faith-target", type=float, default=0.70,          help="Faithfulness target (0–1)")
    _args, _ = _p.parse_known_args()
    PROTEIN        = _args.protein
    MODEL_NAME     = _args.model
    DATA_PATH      = _args.data
    FAITH_TARGET   = _args.faith_target
    SEGMENT_RADIUS = 5
else:
    PROTEIN = "2B61A"
    MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
    DATA_PATH = "data/full_seq_dict.json"
    FAITH_TARGET = 0.70
    SEGMENT_RADIUS = 5

config = PROTEINS[PROTEIN]
print(f"Config: protein={PROTEIN}  model={MODEL_NAME}  faith_target={FAITH_TARGET:.0%}")

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

def contact_metric_differentiable(
    attn_proxies_LBHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor, attention_mask_BL: torch.Tensor,
    eos_idx: int,
    reg_weight: torch.Tensor,   # (1, Nl*H)
    reg_bias:   torch.Tensor,   # (1,)
    orig_seg_AA: torch.Tensor,
    seg: ContactSegment,
) -> torch.Tensor:
    """Differentiable contact metric (mirrors ESM contact head) for backward pass."""
    attns_BLHLL = torch.stack(attn_proxies_LBHLL, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]

    eos_mask_BL  = tokens_BL.ne(eos_idx).float()
    eos_mask_BLL = eos_mask_BL[:, :, None] * eos_mask_BL[:, None, :]
    attns_BLHLL  = attns_BLHLL * eos_mask_BLL[:, None, None, :, :]

    attns_BLHLL  = attns_BLHLL[..., :-1, :-1][..., 1:, 1:]       # trim BOS/EOS

    B, Nl, H, A, _ = attns_BLHLL.shape
    attns_BFAA   = attns_BLHLL.reshape(B, Nl * H, A, A)
    attns_BFAA   = attns_BFAA + attns_BFAA.transpose(-1, -2)      # symmetrize

    # APC normalisation
    a1  = attns_BFAA.sum(-1, keepdim=True)
    a2  = attns_BFAA.sum(-2, keepdim=True)
    a12 = attns_BFAA.sum(dim=(-1, -2), keepdim=True)
    attns_BFAA = attns_BFAA - a1 * a2 / a12

    attns_BAAF   = attns_BFAA.permute(0, 2, 3, 1)                 # (B, A, A, F)
    contacts_BAA = torch.sigmoid(
        torch.nn.functional.linear(attns_BAAF, reg_weight, reg_bias)
    ).squeeze(-1)

    pred_seg = contacts_BAA[0, seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    return (pred_seg * orig_seg_AA).sum() / (orig_seg_AA * orig_seg_AA).sum()

def classify_pos(pos: int, seg: ContactSegment, flank: int) -> str:
    if seg.ss1_start <= pos < seg.ss1_end: return "ss1"
    if seg.ss2_start <= pos < seg.ss2_end: return "ss2"
    if max(0, seg.ss1_start - flank) <= pos < seg.ss1_start: return "flkL"
    if seg.ss2_end <= pos < seg.ss2_end + flank: return "flkR"
    return "other"

# %% ── Model + Data Setup ────────────────────────────────────────────────────

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
seg           = ContactSegment.from_contact_pair(*config["contact_pair"])
clean_seq_S   = mask_with_flanks(sequence_S, seg, config["clean_flank"])
corrupt_seq_S = mask_with_flanks(sequence_S, seg, config["corrupt_flank"])

print(f"\nProtein : {PROTEIN}  (len={len(sequence_S)})")
print(f"Segment : ss1=[{seg.ss1_start}:{seg.ss1_end}]  ss2=[{seg.ss2_start}:{seg.ss2_end}]")
print(f"Flanks  : clean={config['clean_flank']}  corrupt={config['corrupt_flank']}")

# %% ── Baselines ──────────────────────────────────────────────────────────────

print("\nComputing contact-map baselines...")
orig_contacts_AA    = compute_contact_map(esm_model, tokenizer, sequence_S,    device)
clean_contacts_AA   = compute_contact_map(esm_model, tokenizer, clean_seq_S,   device)
corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, device)

clean_metric   = patching_metric(clean_contacts_AA,   orig_contacts_AA, seg)
corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)
print(f"Clean metric   : {clean_metric:.4f}")
print(f"Corrupt metric : {corrupt_metric:.4f}")
print(f"Gap            : {clean_metric - corrupt_metric:.4f}")

# %% ── Cache Attention ────────────────────────────────────────────────────────

print("\nCaching attention for clean + corrupt sequences...")
clean_attn_LBHLL,   clean_inputs_BL   = cache_attention_all_layers(
    model, tokenizer, clean_seq_S,   device, NUM_LAYERS)
corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention_all_layers(
    model, tokenizer, corrupt_seq_S, device, NUM_LAYERS)

B = clean_attn_LBHLL[0].shape[0]    # batch size (1)
L = clean_attn_LBHLL[0].shape[-1]   # seq len with special tokens
print(f"L={L}  attention per layer: ({B}, {NUM_HEADS}, {L}, {L})")

# %% ── Gradient Attribution (head level) ─────────────────────────────────────
# One forward + backward through clean input.
#
# For head (l, h):
#   indirect_attr = sum_{q,k} diff[q,k] * dot(V_h[k], grad_ctx[q, h_slice])
#                 = (diff_LL * (grad_ctx_HLD @ V_h^T)).sum()   ← bmm over heads
#   direct_attr   = sum_{q,k} diff[q,k] * grad_attn[q,k]
#   total_attr    = indirect_attr + direct_attr
#
# Layer 32 (last): grad_ctx is None → only direct_attr.
# All other layers: both terms contribute.

print("\nRunning gradient attribution (forward + backward on clean input)...")

_ch      = esm_model.esm.contact_head
EOS_IDX  = _ch.eos_idx
REG_W    = _ch.regression.weight.detach()   # (1, Nl*H)
REG_B    = _ch.regression.bias.detach()     # (1,)
ORIG_SEG_AA = orig_contacts_AA[
    seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end
].to(device)

# Register hooks: V, ctx (output[0]), attn weights (output[1])
_saved: dict[str, torch.Tensor] = {}
_hooks = []
for l in range(NUM_LAYERS):
    def _v_hook(module, inp, out, _l=l):
        out.retain_grad(); _saved[f"v_{_l}"] = out
    def _self_hook(module, inp, out, _l=l):
        ctx, attn_w = out
        ctx.retain_grad(); attn_w.retain_grad()
        _saved[f"ctx_{_l}"] = ctx; _saved[f"attn_{_l}"] = attn_w
    _hooks.append(esm_model.esm.encoder.layer[l].attention.self.value.register_forward_hook(_v_hook))
    _hooks.append(esm_model.esm.encoder.layer[l].attention.self.register_forward_hook(_self_hook))

esm_model(**clean_inputs_BL, output_attentions=True)

# Differentiable metric → backward
metric_tensor = contact_metric_differentiable(
    [_saved[f"attn_{l}"] for l in range(NUM_LAYERS)],
    clean_inputs_BL["input_ids"], clean_inputs_BL["attention_mask"],
    EOS_IDX, REG_W, REG_B, ORIG_SEG_AA, seg,
)
print(f"Clean metric (differentiable): {metric_tensor.item():.4f}")
metric_tensor.backward()

for h in _hooks:
    h.remove()

# Compute head-level attributions — one layer at a time
head_attr_NH  = torch.zeros(NUM_LAYERS, NUM_HEADS)  # total attribution per head
head_indir_NH = torch.zeros(NUM_LAYERS, NUM_HEADS)  # indirect component
head_dir_NH   = torch.zeros(NUM_LAYERS, NUM_HEADS)  # direct component

print("Computing head attributions (one layer at a time)...")
for layer in range(NUM_LAYERS):
    v_HLD = (
        _saved[f"v_{layer}"].detach()
        .reshape(B, L, NUM_HEADS, HEAD_DIM)
        .transpose(1, 2)
    )[0]                                                        # (H, L, HD)

    grad_ctx_BLd   = _saved[f"ctx_{layer}"].grad               # (B, L, hidden) or None
    grad_attn_BHLL = _saved[f"attn_{layer}"].grad              # (B, H, L, L) or None

    # Indirect: (H, L, HD) @ (H, HD, L) → (H, L, L)
    if grad_ctx_BLd is not None:
        grad_ctx_HLD = (
            grad_ctx_BLd[0]
            .reshape(L, NUM_HEADS, HEAD_DIM)
            .permute(1, 0, 2)
        )                                                       # (H, L, HD)
        indirect_HLL = torch.bmm(grad_ctx_HLD, v_HLD.transpose(1, 2))  # (H, L, L)
    else:
        indirect_HLL = torch.zeros(NUM_HEADS, L, L, device=device)

    # Direct: grad of attn weights through contact head
    direct_HLL = (
        grad_attn_BHLL[0] if grad_attn_BHLL is not None
        else torch.zeros(NUM_HEADS, L, L, device=device)
    )                                                           # (H, L, L)

    # diff (clean − corrupt)
    diff_HLL = (
        clean_attn_LBHLL[layer][0].to(device) -
        corrupt_attn_LBHLL[layer][0].to(device)
    )                                                           # (H, L, L)

    # Aggregate over (q, k) → scalar per head
    indir_H = (diff_HLL * indirect_HLL).sum(dim=(-1, -2)).cpu()   # (H,)
    dir_H   = (diff_HLL * direct_HLL  ).sum(dim=(-1, -2)).cpu()   # (H,)

    head_indir_NH[layer] = indir_H
    head_dir_NH[layer]   = dir_H
    head_attr_NH[layer]  = indir_H + dir_H

    print(f"  Layer {layer:2d}/{NUM_LAYERS-1}"
          f"  indirect: [{indir_H.min():+.4f}, {indir_H.max():+.4f}]"
          f"  direct: [{dir_H.min():+.4f}, {dir_H.max():+.4f}]")

# NOTE: _saved is intentionally kept alive here — reused for cell-level
#       attribution below (after circuit heads are identified).

# %% ── Attribution Summary ────────────────────────────────────────────────────

# Flatten to (Nl*H,) sorted list of (layer, head, attr, indir, dir)
flat_attrs: list[tuple] = []
for l in range(NUM_LAYERS):
    for h in range(NUM_HEADS):
        flat_attrs.append((l, h,
                           head_attr_NH[l, h].item(),
                           head_indir_NH[l, h].item(),
                           head_dir_NH[l, h].item()))

flat_attrs.sort(key=lambda x: x[2], reverse=True)   # descending by total attr

positive_heads = [(l, h, a, ind, d) for l, h, a, ind, d in flat_attrs if a > 0]
negative_heads = [(l, h, a, ind, d) for l, h, a, ind, d in flat_attrs if a <= 0]

print(f"\n{'='*65}")
print(f"HEAD-LEVEL ATTRIBUTION SUMMARY")
print(f"{'='*65}")
print(f"  Total heads   : {NUM_LAYERS * NUM_HEADS}")
print(f"  Positive attr : {len(positive_heads)}")
print(f"  Negative attr : {len(negative_heads)}")

print(f"\nTop 30 heads by attribution:")
print(f"  {'L':>3} {'H':>3} {'total':>10} {'indirect':>10} {'direct':>10}")
print("  " + "-" * 45)
for l, h, a, ind, d in flat_attrs[:30]:
    print(f"  L{l:2d} H{h:2d}  {a:>+9.4f}  {ind:>+9.4f}  {d:>+9.4f}")

# %% ── Save Head Attributions ─────────────────────────────────────────────────

torch.save({
    "head_attr_NH":  head_attr_NH,
    "head_indir_NH": head_indir_NH,
    "head_dir_NH":   head_dir_NH,
    "flat_attrs":    flat_attrs,
    "clean_metric":  clean_metric,
    "corrupt_metric": corrupt_metric,
    "protein":       PROTEIN,
}, f"reports/outputs/{PROTEIN}_head_attr.pt")
print(f"\nSaved to reports/outputs/{PROTEIN}_head_attr.pt")

# %% ── Sufficiency Test ───────────────────────────────────────────────────────
# Protect top-K positive-attribution heads (keep their clean attn),
# corrupt everything else → faithfulness should rise toward clean.
#
# At K=0 → fully corrupt.  Stop when faith ≥ FAITH_TARGET.

print(f"\n{'='*60}")
print(f"SUFFICIENCY TEST  (target faithfulness: {FAITH_TARGET:.0%})")
print(f"{'='*60}")

_contact_head = esm_model.esm.contact_head

# Only sweep over positive-attr heads (negative ones hurt the metric)
pos_heads_ordered = [(l, h) for l, h, *_ in flat_attrs if _ [0] > 0]  # total > 0

# Sweep: K = 0, 1, 2, ... up to all positive heads (or until target reached)
sufficiency_results = []
circuit_heads: list[tuple[int,int]] = []   # will be filled when target is hit

# Always test K=0 first (fully corrupt baseline check)
ks_to_test = [0] + list(range(1, len(pos_heads_ordered) + 1))

for k in ks_to_test:
    protected_lh = set(pos_heads_ordered[:k])   # top-k by attribution

    # Sufficiency: start from CLEAN attention (top-K heads untouched),
    # patch corrupt attention into every head NOT in the top-K.
    attn_list_LBHLL: list[torch.Tensor] = []
    for layer_idx in range(NUM_LAYERS):
        base_BHLL = clean_attn_LBHLL[layer_idx].clone()            # (B, H, L, L) — start clean
        for hn in range(NUM_HEADS):
            if (layer_idx, hn) not in protected_lh:
                base_BHLL[:, hn] = corrupt_attn_LBHLL[layer_idx][:, hn]  # corrupt non-top-K
        attn_list_LBHLL.append(base_BHLL)

    contacts_BAA = compute_contacts_from_attention(
        attn_list_LBHLL,
        clean_inputs_BL["input_ids"],
        clean_inputs_BL["attention_mask"],
        _contact_head, device=device,
    )
    metric = patching_metric(contacts_BAA[0].detach().cpu(), orig_contacts_AA, seg)
    faith  = faithfulness(metric, clean_metric, corrupt_metric)

    sufficiency_results.append({"k": k, "heads": list(protected_lh),
                                 "metric": metric, "faithfulness": faith})

    n_layers = len({ln for ln, _ in protected_lh})
    print(f"  K={k:3d}  ({n_layers} layers touched)"
          f"  metric={metric:.4f}  faith={faith:.1%}")

    if faith >= FAITH_TARGET and not circuit_heads:
        circuit_heads = list(pos_heads_ordered[:k])
        print(f"  *** Target {FAITH_TARGET:.0%} reached at K={k} ***")
        # Keep going a few more steps to see the curve
        ks_to_test = list(range(k + 1, min(k + 6, len(pos_heads_ordered) + 1)))

    if k > 0 and len(circuit_heads) > 0 and k >= circuit_heads.__len__() + 5:
        break

print(f"\nBaselines: clean={clean_metric:.4f}  corrupt={corrupt_metric:.4f}")
if circuit_heads:
    print(f"Circuit: {len(circuit_heads)} heads reach {FAITH_TARGET:.0%} faithfulness")
else:
    print(f"Target {FAITH_TARGET:.0%} not reached with positive-attr heads alone.")

torch.save({
    "sufficiency_results": sufficiency_results,
    "circuit_heads":       circuit_heads,
    "clean_metric":        clean_metric,
    "corrupt_metric":      corrupt_metric,
    "protein":             PROTEIN,
    "faith_target":        FAITH_TARGET,
}, f"reports/outputs/{PROTEIN}_head_sufficiency.pt")
print(f"Saved to reports/outputs/{PROTEIN}_head_sufficiency.pt")

# %% ── Cell-Level Attribution (circuit heads only) ───────────────────────────
# Now that we know which heads form the circuit, zoom in to the cell level.
# Reuses the _saved gradient tensors from the earlier backward pass.
#
# For cell (l, h, q, k) where (l,h) ∈ circuit_heads:
#   attr[q,k] = diff[q,k] * (indirect[q,k] + direct[q,k])
#
# Scoped to circuit_heads only: ~K_circ × L² cells (e.g. 27 × 379² ≈ 3.9M max)
# vs all 660 heads (~94M). torch.quantile works fine at this size.

if not circuit_heads:
    print("\nNo circuit heads — skipping cell-level attribution.")
    cell_nz_layers  = torch.tensor([], dtype=torch.long)
    cell_nz_heads   = torch.tensor([], dtype=torch.long)
    cell_nz_qs      = torch.tensor([], dtype=torch.long)
    cell_nz_ks      = torch.tensor([], dtype=torch.long)
    cell_nz_attrs   = torch.tensor([])
    cell_nz_absdiffs = torch.tensor([])
else:
    print(f"\nCell-level attribution on {len(circuit_heads)} circuit heads...")
    circuit_set = set(circuit_heads)

    c_layers_list: list[torch.Tensor] = []
    c_heads_list:  list[torch.Tensor] = []
    c_qs_list:     list[torch.Tensor] = []
    c_ks_list:     list[torch.Tensor] = []
    c_attrs_list:  list[torch.Tensor] = []
    c_absdiffs_list: list[torch.Tensor] = []

    for layer in range(NUM_LAYERS):
        heads_this_layer = [h for (l, h) in circuit_set if l == layer]
        if not heads_this_layer:
            continue

        v_HLD = (
            _saved[f"v_{layer}"].detach()
            .reshape(B, L, NUM_HEADS, HEAD_DIM)
            .transpose(1, 2)
        )[0]                                                        # (H, L, HD)

        grad_ctx_BLd   = _saved[f"ctx_{layer}"].grad               # (B, L, hidden) or None
        grad_attn_BHLL = _saved[f"attn_{layer}"].grad              # (B, H, L, L) or None

        if grad_ctx_BLd is not None:
            grad_ctx_HLD = (
                grad_ctx_BLd[0]
                .reshape(L, NUM_HEADS, HEAD_DIM)
                .permute(1, 0, 2)
            )                                                       # (H, L, HD)
            indirect_HLL = torch.bmm(grad_ctx_HLD, v_HLD.transpose(1, 2))   # (H, L, L)
        else:
            indirect_HLL = torch.zeros(NUM_HEADS, L, L, device=device)

        direct_HLL = (
            grad_attn_BHLL[0] if grad_attn_BHLL is not None
            else torch.zeros(NUM_HEADS, L, L, device=device)
        )                                                           # (H, L, L)

        sensitivity_HLL = indirect_HLL + direct_HLL                # (H, L, L)

        diff_HLL    = (
            clean_attn_LBHLL[layer][0].to(device) -
            corrupt_attn_LBHLL[layer][0].to(device)
        )                                                           # (H, L, L)
        attr_HLL    = (diff_HLL * sensitivity_HLL).cpu()
        absdiff_HLL = diff_HLL.abs().cpu()                         # (H, L, L)

        for head in heads_this_layer:
            nz_q, nz_k = torch.where(absdiff_HLL[head] > 1e-6)    # nonzero-diff cells
            n_nz = nz_q.numel()
            print(f"  L{layer:2d} H{head:2d}  nonzero cells: {n_nz:>8,d}")
            if n_nz == 0:
                continue
            c_layers_list.append(torch.full((n_nz,), layer, dtype=torch.long))
            c_heads_list.append(torch.full((n_nz,), head,  dtype=torch.long))
            c_qs_list.append(nz_q)
            c_ks_list.append(nz_k)
            c_attrs_list.append(attr_HLL[head][nz_q, nz_k])
            c_absdiffs_list.append(absdiff_HLL[head][nz_q, nz_k])

    cell_nz_layers   = torch.cat(c_layers_list)
    cell_nz_heads    = torch.cat(c_heads_list)
    cell_nz_qs       = torch.cat(c_qs_list)
    cell_nz_ks       = torch.cat(c_ks_list)
    cell_nz_attrs    = torch.cat(c_attrs_list)
    cell_nz_absdiffs = torch.cat(c_absdiffs_list)

    # Sort by attribution descending
    sort_idx         = torch.argsort(cell_nz_attrs, descending=True)
    cell_nz_layers   = cell_nz_layers[sort_idx]
    cell_nz_heads    = cell_nz_heads[sort_idx]
    cell_nz_qs       = cell_nz_qs[sort_idx]
    cell_nz_ks       = cell_nz_ks[sort_idx]
    cell_nz_attrs    = cell_nz_attrs[sort_idx]
    cell_nz_absdiffs = cell_nz_absdiffs[sort_idx]

    N_CELLS = len(cell_nz_attrs)
    print(f"\nTotal nonzero-diff cells in circuit heads: {N_CELLS:,d}")
    print(f"\nTop 20 cells by attribution:")
    print(f"  {'L':>3} {'H':>3} {'q':>5} {'k':>5} {'attr':>12} {'|diff|':>10}")
    print("  " + "-" * 45)
    for i in range(min(20, N_CELLS)):
        print(f"  L{cell_nz_layers[i]:2d} H{cell_nz_heads[i]:2d}"
              f" {cell_nz_qs[i]:>5d} {cell_nz_ks[i]:>5d}"
              f" {cell_nz_attrs[i]:>+11.6f} {cell_nz_absdiffs[i]:>10.6f}")

    print(f"\nCell attribution distribution:")
    print(f"  Positive: {(cell_nz_attrs > 0).sum().item():,d}  Negative: {(cell_nz_attrs < 0).sum().item():,d}")
    for pct in [90, 95, 99, 99.9]:
        val     = torch.quantile(cell_nz_attrs, pct / 100).item()
        n_above = (cell_nz_attrs >= val).sum().item()
        print(f"  {pct}th pct: {val:+.6f}  ({n_above:,d} cells above)")

# Free gradient tensors now that we're done with them
del _saved
clear_memory()

# %% ── Save Cell Attributions ────────────────────────────────────────────────

torch.save({
    "cell_nz_layers":   cell_nz_layers,
    "cell_nz_heads":    cell_nz_heads,
    "cell_nz_qs":       cell_nz_qs,
    "cell_nz_ks":       cell_nz_ks,
    "cell_nz_attrs":    cell_nz_attrs,
    "cell_nz_absdiffs": cell_nz_absdiffs,
    "circuit_heads":    circuit_heads,
    "clean_metric":     clean_metric,
    "corrupt_metric":   corrupt_metric,
    "protein":          PROTEIN,
    "L":                L,
}, f"reports/outputs/{PROTEIN}_cell_attr_circuit.pt")
print(f"\nSaved to reports/outputs/{PROTEIN}_cell_attr_circuit.pt")

# %% ── Cell-Level Sufficiency Test ───────────────────────────────────────────
# Protect top-K positive-attribution cells within circuit heads.
# Non-circuit heads always stay corrupt.
# → How many cells does it take to reconstruct the circuit metric?

if circuit_heads:
    print(f"\n{'='*60}")
    print("CELL-LEVEL SUFFICIENCY  (circuit heads, protect top-K cells)")
    print(f"{'='*60}")

    pos_cell_mask   = cell_nz_attrs > 0
    N_POS_CELLS     = pos_cell_mask.sum().item()
    print(f"  Positive-attr cells in circuit: {N_POS_CELLS:,d}")

    # Thresholds: fine-grained at small K, coarser at large K
    def _cell_ks(n_max: int) -> list[int]:
        ks = [0]
        for exp in range(0, 20):
            for m in [1, 2, 5]:
                v = m * (10 ** exp)
                if 0 < v <= n_max:
                    ks.append(v)
        return sorted(set(ks))

    cell_ks = _cell_ks(N_POS_CELLS)

    cell_suff_results = []
    cell_circuit_k    = None   # first K that hits FAITH_TARGET

    for k in cell_ks:
        # Protected set: top-k positive cells (as (layer, head, q, key) tuples)
        # Stored as per-layer dict for fast lookup during patching
        protected_by_layer: dict[int, list[tuple]] = defaultdict(list)
        for i in range(k):
            if cell_nz_attrs[i].item() <= 0:
                break
            l = cell_nz_layers[i].item()
            h = cell_nz_heads[i].item()
            q = cell_nz_qs[i].item()
            kk = cell_nz_ks[i].item()
            protected_by_layer[l].append((h, q, kk))

        # Sufficiency: start from CLEAN attention (top-K cells untouched).
        # Patch corrupt into every component NOT in the protected set:
        #   - non-circuit heads: always corrupt (full head)
        #   - circuit heads: corrupt every cell EXCEPT the top-K protected cells
        attn_list_LBHLL: list[torch.Tensor] = []
        for layer_idx in range(NUM_LAYERS):
            base_BHLL = clean_attn_LBHLL[layer_idx].clone()           # (B, H, L, L) — start clean
            for hn in range(NUM_HEADS):
                if (layer_idx, hn) not in circuit_set:
                    base_BHLL[:, hn] = corrupt_attn_LBHLL[layer_idx][:, hn]  # non-circuit: corrupt
                else:
                    # Circuit head: corrupt every cell, then restore top-K clean cells
                    base_BHLL[:, hn] = corrupt_attn_LBHLL[layer_idx][:, hn]
                    for (h, q, kk) in protected_by_layer.get(layer_idx, []):
                        if h == hn:
                            base_BHLL[:, hn, q, kk] = clean_attn_LBHLL[layer_idx][:, hn, q, kk]
            attn_list_LBHLL.append(base_BHLL)

        contacts_BAA = compute_contacts_from_attention(
            attn_list_LBHLL,
            clean_inputs_BL["input_ids"],
            clean_inputs_BL["attention_mask"],
            _contact_head, device=device,
        )
        metric = patching_metric(contacts_BAA[0].detach().cpu(), orig_contacts_AA, seg)
        faith  = faithfulness(metric, clean_metric, corrupt_metric)

        n_heads_touched = len(protected_by_layer)
        cell_suff_results.append({"k": k, "metric": metric, "faithfulness": faith,
                                   "n_heads": n_heads_touched})
        print(f"  K={k:6d}  ({n_heads_touched:2d} heads) → metric={metric:.4f}  faith={faith:.1%}")

        if faith >= FAITH_TARGET and cell_circuit_k is None:
            cell_circuit_k = k
            print(f"  *** Target {FAITH_TARGET:.0%} reached at K={k} cells ***")

    print(f"\nBaselines: clean={clean_metric:.4f}  corrupt={corrupt_metric:.4f}")
    if cell_circuit_k is not None:
        print(f"Circuit: {cell_circuit_k} cells (within {len(circuit_heads)} heads) → {FAITH_TARGET:.0%} faithfulness")
    else:
        print(f"Target not reached within {N_POS_CELLS:,d} positive cells.")

    torch.save({
        "cell_suff_results": cell_suff_results,
        "circuit_heads":     circuit_heads,
        "cell_circuit_k":    cell_circuit_k,
        "clean_metric":      clean_metric,
        "corrupt_metric":    corrupt_metric,
        "protein":           PROTEIN,
        "faith_target":      FAITH_TARGET,
    }, f"reports/outputs/{PROTEIN}_cell_sufficiency_circuit.pt")
    print(f"Saved to reports/outputs/{PROTEIN}_cell_sufficiency_circuit.pt")

# %% ── Motif Extraction (circuit heads only) ──────────────────────────────────
# For each circuit head: what positions do it attend to?
# Key mass, query mass, offset distribution, anchor/positional classification.

if not circuit_heads:
    print("\nNo circuit heads to analyse — skipping motif extraction.")
else:
    print(f"\n{'='*70}")
    print(f"MOTIF EXTRACTION — {len(circuit_heads)} circuit heads")
    print(f"{'='*70}")

    SSE_GAP      = seg.ss2_start - seg.ss1_start
    ANCHOR_T1    = 0.60
    ANCHOR_T2    = 0.70
    ANCHOR_T3    = 0.80
    POSITIONAL_T = 0.50

    # Attr rank for display
    attr_rank = {(l, h): i + 1 for i, (l, h, *_) in enumerate(flat_attrs)}

    print(f"  ss1=[{seg.ss1_start}..{seg.ss1_end-1}]  "
          f"ss2=[{seg.ss2_start}..{seg.ss2_end-1}]  "
          f"flkL=[{seg.ss1_start - config['clean_flank']}..{seg.ss1_start-1}]  "
          f"flkR=[{seg.ss2_end}..{seg.ss2_end + config['clean_flank'] - 1}]  "
          f"SSE_GAP={SSE_GAP}\n")

    summary_rows = []

    for (l, h) in sorted(circuit_heads):
        rank         = attr_rank.get((l, h), "–")
        total_attr   = head_attr_NH[l, h].item()
        indir_attr   = head_indir_NH[l, h].item()
        dir_attr     = head_dir_NH[l, h].item()

        # Pull this head's cells from the sorted cell-level tensor
        head_mask    = (cell_nz_layers == l) & (cell_nz_heads == h)
        head_qs_N    = cell_nz_qs[head_mask].tolist()       # (N,)
        head_ks_N    = cell_nz_ks[head_mask].tolist()       # (N,)
        head_attrs_N = cell_nz_attrs[head_mask].tolist()    # (N,)  ← signed attribution

        # Weight cells by attribution (positive = helps metric, negative = hurts)
        # Use abs(attr) as mass so both helpful and harmful cells show up in motif
        key_mass: dict[int, float] = defaultdict(float)
        qry_mass: dict[int, float] = defaultdict(float)
        off_mass: dict[int, float] = defaultdict(float)

        for q, k, a in zip(head_qs_N, head_ks_N, head_attrs_N):
            w = abs(a)
            key_mass[k] += w
            qry_mass[q] += w
            off_mass[q - k] += w

        total_abs_k = sum(key_mass.values()) or 1.0
        total_abs_q = sum(qry_mass.values()) or 1.0
        total_off   = sum(off_mass.values()) or 1.0

        key_sorted = sorted(key_mass.items(), key=lambda x: x[1], reverse=True)
        qry_sorted = sorted(qry_mass.items(), key=lambda x: x[1], reverse=True)
        off_sorted = sorted(off_mass.items(), key=lambda x: x[1], reverse=True)

        # Anchor classification (by key concentration)
        t1 = key_sorted[0][1] / total_abs_k
        t2 = sum(v for _, v in key_sorted[:2]) / total_abs_k
        t3 = sum(v for _, v in key_sorted[:3]) / total_abs_k
        anchor = ("SINGLE-ANCHOR" if t1 >= ANCHOR_T1 else
                  "DUAL-ANCHOR"   if t2 >= ANCHOR_T2 else
                  "MULTI-ANCHOR"  if t3 >= ANCHOR_T3 else
                  "DISTRIBUTED")

        # Positional classification (by offset concentration)
        top2_off_frac = sum(v for _, v in off_sorted[:2]) / total_off
        top_offset    = off_sorted[0][0] if off_sorted else 0
        is_cross_sse  = abs(abs(top_offset) - SSE_GAP) <= 3
        if   is_cross_sse and top2_off_frac >= POSITIONAL_T: pos_tag = "CROSS_SSE"
        elif top2_off_frac >= POSITIONAL_T and abs(top_offset) <= 10: pos_tag = "LOCAL"
        else:                                                          pos_tag = ""

        tags = anchor + (f" | {pos_tag}" if pos_tag else "")
        print(f"  L{l:2d} H{h:2d} [attr_rank#{rank}]"
              f"  attr={total_attr:+.4f} (indir={indir_attr:+.4f} dir={dir_attr:+.4f})"
              f"  | {tags}")

        # Key mass
        print(f"       Keys  (top-1={t1:.0%} top-2={t2:.0%} top-3={t3:.0%}):")
        for k_pos, k_w in key_sorted[:5]:
            frac = k_w / total_abs_k * 100
            bar  = "█" * int(frac / 5)
            print(f"         k={k_pos:>4d} [{classify_pos(k_pos, seg, config['clean_flank']):5s}]"
                  f"  {k_w:>7.4f}  {frac:>5.1f}%  {bar}")
        if len(key_sorted) > 5:
            print(f"         … {len(key_sorted)-5} more keys"
                  f"  ({sum(v for _,v in key_sorted[5:])/total_abs_k:.0%} of mass)")

        # Query mass
        print(f"       Queries:")
        for q_pos, q_w in qry_sorted[:5]:
            frac = q_w / total_abs_q * 100
            print(f"         q={q_pos:>4d} [{classify_pos(q_pos, seg, config['clean_flank']):5s}]"
                  f"  {q_w:>7.4f}  {frac:>5.1f}%")
        if len(qry_sorted) > 5:
            print(f"         … {len(qry_sorted)-5} more queries")

        # Offset distribution
        dom = ", ".join(f"{o:+d}" for o, _ in off_sorted[:2])
        print(f"       Offsets (q−k), top-2={top2_off_frac:.0%}  [{dom}]:")
        for offset, o_w in off_sorted[:5]:
            frac = o_w / total_off * 100
            note = (
                " ← self"        if offset == 0  else
                " ← attend-prev" if offset == 1  else
                " ← attend-next" if offset == -1 else
                f" ← ±{abs(offset)}"  if abs(offset) <= 5 else
                " ← ~SSE_GAP"    if abs(abs(offset) - SSE_GAP) <= 3 else ""
            )
            print(f"         Δ={offset:>+6d}  {frac:>5.1f}%{note}")
        print()

        summary_rows.append((l, h, rank, total_attr, indir_attr, dir_attr, anchor, pos_tag))

    # Summary table
    print(f"\n{'='*70}")
    print(f"CIRCUIT SUMMARY  ({len(circuit_heads)} heads → {FAITH_TARGET:.0%} faithfulness)")
    print(f"{'='*70}")
    print(f"  {'L':>3} {'H':>3} {'rank':>6} {'total':>10} {'indirect':>10} {'direct':>8}  anchor         pos")
    print("  " + "-" * 68)
    for (l, h, rank, tot, ind, d, anchor, pos_tag) in sorted(summary_rows, key=lambda x: (x[0], x[1])):
        print(f"  L{l:2d} H{h:2d}  #{rank:>3}  {tot:>+9.4f}  {ind:>+9.4f}  {d:>+7.4f}  {anchor:<14} {pos_tag}")

print("\nDone.")
