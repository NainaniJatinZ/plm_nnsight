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
# Run as: `.plm_nn/bin/python -u contact_pattern.py [--protein 2B61A] [--model ...]`
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
    PROTEIN = "1PVGA" # "2B61A"
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

indirect_effects_LH = torch.zeros(NUM_LAYERS, NUM_HEADS)

for layer_idx in range(NUM_LAYERS):
    for head_idx in range(NUM_HEADS):
        # Get corrupt attention for just this head
        corrupt_head_attn_LL = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]

        # Single trace: access V, patch attention, set output[0], capture downstream
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

        # The patched layer itself
        patched_layer_attn = clean_attn_LBHLL[layer_idx].clone()
        patched_layer_attn[:, head_idx, :, :] = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]
        patched_full_attn.append(patched_layer_attn)

        # Downstream layers from the intervention
        patched_full_attn.extend(downstream_attn)

        # Compute contacts with the full (indirectly patched) attention
        indirect_contacts_AA = compute_contacts_from_attention(
            patched_full_attn,
            clean_inputs_BL['input_ids'],
            clean_inputs_BL['attention_mask'],
            esm_model.esm.contact_head,
            device=device,
        )[0].detach().cpu()

        # Normalized effect
        indirect_metric = patching_metric(indirect_contacts_AA, orig_contacts_AA, seg)
        if abs(corrupt_metric - clean_metric) > 1e-6:
            effect = (indirect_metric - clean_metric) / (corrupt_metric - clean_metric)
        else:
            effect = 0.0
        indirect_effects_LH[layer_idx, head_idx] = effect

    if (layer_idx + 1) % 5 == 0:
        print(f"    Processed layer {layer_idx + 1}/{NUM_LAYERS}")

# %%


indirect_flat = indirect_effects_LH.flatten()
total_heads = NUM_LAYERS * NUM_HEADS  # 660

# Three sort orders
sort_configs = {
    "abs": indirect_flat.abs().argsort(descending=True),
    "pos": indirect_flat.argsort(descending=True),
    "neg": indirect_flat.argsort(descending=False),
}
sorted_heads_by_config = {}
for name, indices in sort_configs.items():
    sorted_heads_by_config[name] = [(idx.item() // NUM_HEADS, idx.item() % NUM_HEADS) for idx in indices]

# k values: fine near start and around expected threshold (100-300), coarser at tail
k_values = list(range(0, min(31, total_heads)))           # 0..30 by 1
k_values += list(range(35, min(101, total_heads), 5))     # 35,40,...,100
k_values += list(range(102, min(351, total_heads), 5))    # 102,105,...,350 (fine around threshold)
k_values += list(range(360, total_heads, 20))             # 360,380,...
k_values.append(total_heads)
k_values = sorted(set(k_values))

FORCE_CIRCUIT_RECALC = True


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
            faith = (score - corrupt_metric) / (clean_metric - corrupt_metric) if abs(clean_metric - corrupt_metric) > 1e-6 else 0.0
            print(f"    k={k:4d}: faithfulness={faith:.2%}")

    print(f"    Done!")
    return list(k_values), scores


# Run all three experiments
print(f"Circuit discovery: {len(k_values)} k-values, 3 sort orders")
print(f"  Baseline: clean={clean_metric:.4f}, corrupt={corrupt_metric:.4f}, gap={clean_metric - corrupt_metric:.4f}")

circuit_results = {}
for sort_name, sort_label in [("abs", "|indirect|"), ("pos", "positive IE"), ("neg", "negative IE")]:
    kv, sc = run_circuit_experiment(sorted_heads_by_config[sort_name], sort_label)
    faith = [(s - corrupt_metric) / (clean_metric - corrupt_metric) if abs(clean_metric - corrupt_metric) > 1e-6 else 0.0 for s in sc]
    crossed = None
    for k_val, f_val in zip(kv, faith):
        if f_val >= 0.7:
            crossed = k_val
            break
    circuit_results[sort_name] = {"k": kv, "scores": sc, "faith": faith, "crossed_k": crossed}



# %%
top_ie_heads = sorted_heads_by_config["pos"][:circuit_results["pos"]["crossed_k"]]


# %%

# Reimplement contact head as differentiable ops (from attr_patching_nnsight.py)
contact_head_module = esm_model.esm.contact_head
EOS_IDX = contact_head_module.eos_idx
REGRESSION_WEIGHT = contact_head_module.regression.weight.detach()  # (1, 660)
REGRESSION_BIAS = contact_head_module.regression.bias.detach()      # (1,)
ORIG_SEG = orig_contacts_AA[
    seg.ss1_start:seg.ss1_end,
    seg.ss2_start:seg.ss2_end,
].to(device)

def contact_metric_from_attn_proxies(
    attn_proxies, tokens_BL, attention_mask_BL,
    eos_idx, regression_weight, regression_bias, orig_seg, segment,
):
    """Differentiable contact metric from attention weights (from attr_patching_nnsight.py)."""
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

    a1 = attns.sum(-1, keepdim=True)
    a2 = attns.sum(-2, keepdim=True)
    a12 = attns.sum(dim=(-1, -2), keepdim=True)
    avg = a1 * a2 / a12
    attns = attns - avg

    attns = attns.permute(0, 2, 3, 1)
    contacts = torch.sigmoid(torch.nn.functional.linear(attns, regression_weight, regression_bias))
    contacts = contacts.squeeze(3)

    pred_seg = contacts[0, segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    metric = (pred_seg * orig_seg).sum() / (orig_seg * orig_seg).sum()
    return metric

# --- Step 1: Forward pass through FULL model, capture output[0], V, output[1] ---
print("Running corrupt forward pass with hooks...")
saved_hooks = {}
hooks = []

for l in range(NUM_LAYERS):
    # Capture V (value projection output)
    def v_hook(module, input, output, l=l):
        output.retain_grad()
        saved_hooks[f'v_{l}'] = output
    hooks.append(esm_model.esm.encoder.layer[l].attention.self.value.register_forward_hook(v_hook))

    # Capture output[0] (context vector) and output[1] (attention weights)
    def self_hook(module, input, output, l=l):
        context, attn_weights = output
        context.retain_grad()
        attn_weights.retain_grad()
        saved_hooks[f'ctx_{l}'] = context
        saved_hooks[f'attn_{l}'] = attn_weights
    hooks.append(esm_model.esm.encoder.layer[l].attention.self.register_forward_hook(self_hook))

# Forward pass (corrupt inputs, gradients enabled)
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
    v_full = saved_hooks[f'v_{layer}'].detach()  # (B, L, hidden)
    v_heads = v_full.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)  # (B, H, L, HD)
    v_h = v_heads[0, head]  # (L, HD)

    # --- Indirect sensitivity: through ctx → residual → downstream attn ---
    # grad_ctx[l] is non-zero only if ctx[l] has downstream path to metric.
    # For the last layer (layer 32), no downstream layers exist → grad_ctx is None.
    grad_ctx = saved_hooks[f'ctx_{layer}'].grad  # (B, L, hidden)
    if grad_ctx is None:
        indirect_sensitivity_LL = torch.zeros(L, L, device=device)
    else:
        grad_h = grad_ctx[0, :, head * HEAD_DIM:(head + 1) * HEAD_DIM]  # (L, HD)
        indirect_sensitivity_LL = grad_h @ v_h.T  # (L, L)

    # --- Direct sensitivity: attn[l,h] → contact head → metric ---
    # All layers have this path. For layer 32 it's the ONLY path.
    # attn_weights.retain_grad() was already called so this is always populated.
    grad_attn = saved_hooks[f'attn_{layer}'].grad  # (B, H, L, L)
    if grad_attn is not None:
        direct_sensitivity_LL = grad_attn[0, head]  # (L, L)
    else:
        direct_sensitivity_LL = torch.zeros(L, L, device=device)

    # Total attribution = indirect + direct
    # Indirect dominates for internal layers; only direct exists for the last layer.
    sensitivity_LL = indirect_sensitivity_LL + direct_sensitivity_LL

    # Diff and attribution
    clean_LL = clean_attn_LBHLL[layer][0, head].to(device)
    corrupt_LL = corrupt_attn_LBHLL[layer][0, head].to(device)
    diff_LL = clean_LL - corrupt_LL
    attr_LL = (diff_LL * sensitivity_LL).cpu()
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

# Sort by attribution (positive = helpful for metric, protect these first)
cell_attr_sorted = sorted(cell_attributions, key=lambda x: x[4], reverse=True)

print(f"\nTotal cells with attribution: {len(cell_attr_sorted):,d}")
print(f"\nTop 20 cells by attribution (positive = helpful):")
print(f"  (= indirect via residual stream + direct via contact head)")
print(f"{'Layer':>5} {'Head':>4} {'q':>5} {'k':>5} {'attr':>12} {'|diff|':>10}")
print("-" * 50)
for layer, head, q, k, attr, adiff in cell_attr_sorted[:20]:
    print(f"  L{layer:2d}  H{head:2d}  {q:>4d}  {k:>4d}  {attr:>+11.6f}  {adiff:>10.6f}")

print(f"\nBottom 20 cells (negative = harmful):")
for layer, head, q, k, attr, adiff in cell_attr_sorted[-20:]:
    print(f"  L{layer:2d}  H{head:2d}  {q:>4d}  {k:>4d}  {attr:>+11.6f}  {adiff:>10.6f}")

# Attribution distribution
all_attrs = torch.tensor([c[4] for c in cell_attr_sorted])
print(f"\nAttribution distribution (indirect + direct):")
print(f"  Positive: {(all_attrs > 0).sum().item():,d} cells")
print(f"  Negative: {(all_attrs < 0).sum().item():,d} cells")
for pct in [90, 95, 99, 99.5, 99.9]:
    val = torch.quantile(all_attrs, pct / 100).item()
    n_above = (all_attrs >= val).sum().item()
    print(f"  {pct}th percentile: {val:+.8f}  ({n_above:,d} cells above)")
# %%
# Protect top-K cells by INDIRECT attribution (most helpful for metric
# through the residual stream path), corrupt everything else.

print(f"\n{'='*60}")
print("INDIRECT ATTRIBUTION-RANKED SUFFICIENCY TEST")
print(f"{'='*60}")

attr_thresholds = [0, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
attr_thresholds = [t for t in attr_thresholds if t <= len(cell_attr_sorted)]
attr_sufficiency_results = []

for k in attr_thresholds:
    # Top-K by attribution are protected
    protected_cells = set()
    for layer, head, q, kk, attr, adiff in cell_attr_sorted[:k]:
        protected_cells.add((layer, head, q, kk))

    # Forward pass: corrupt everything, protect top-K cells
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

    metric = patching_metric(contacts, orig_contacts_AA, seg)
    faithfulness = (metric - corrupt_metric) / (clean_metric - corrupt_metric) \
        if abs(clean_metric - corrupt_metric) > 1e-6 else 0.0

    n_heads = len(set((l, h) for l, h, q, kk in protected_cells))
    attr_sufficiency_results.append({
        'k': k, 'n_protected': len(protected_cells),
        'n_heads': n_heads,
        'metric': metric, 'faithfulness': faithfulness,
    })
    print(f"  Top {k:5d} protected ({len(protected_cells):,d} cells) → "
          f"metric={metric:.4f}, faithfulness={faithfulness:.2%}")

# %%

# =============================================================================
# Motif Extraction: per-head key/query mass, anchor + positional classification
# =============================================================================
from collections import defaultdict

topk_cell = 1000
topk_heads = 30
ie_circuit_cells = cell_attr_sorted[:topk_cell]

# IE rank lookup (original attribution-ranking order)
ie_rank = {(l, h): i + 1 for i, (l, h) in enumerate(top_ie_heads[:topk_heads])}

# Display in (layer, head) order
heads_sorted = sorted(top_ie_heads[:topk_heads], key=lambda x: (x[0], x[1]))

# Regions (same indexing as q/k values in cells)
SS1     = set(range(seg.ss1_start, seg.ss1_end))
SS2     = set(range(seg.ss2_start, seg.ss2_end))
FLANK_L = set(range(max(0, seg.ss1_start - config["clean_flank"]), seg.ss1_start))
FLANK_R = set(range(seg.ss2_end, seg.ss2_end + config["clean_flank"]))
SSE_GAP = seg.ss2_start - seg.ss1_start  # offset between the two contact residues

def classify_pos(pos):
    if pos in SS1:     return "ss1"
    if pos in SS2:     return "ss2"
    if pos in FLANK_L: return "flkL"
    if pos in FLANK_R: return "flkR"
    return "other"

# Classification thresholds
ANCHOR_T1    = 0.60
ANCHOR_T2    = 0.70
ANCHOR_T3    = 0.80
POSITIONAL_T = 0.50

# --- Load path patching data ---
PATH_TOP_N = 400
path_pt = f'reports/outputs/{PROTEIN}_path_patching_full.pt'
path_srcdst = {}  # (l, h) -> {'as_src': [(dl, dh, ch, eff), ...], 'as_dst': [...]}

if os.path.exists(path_pt):
    path_data  = torch.load(path_pt, map_location='cpu', weights_only=False)
    pass_d_all = path_data['pass_d_results']
    top_paths  = sorted(pass_d_all, key=lambda x: abs(x['pass_d_effect']), reverse=True)[:PATH_TOP_N]
    print(f"Loaded {len(pass_d_all)} paths, using top {PATH_TOP_N}")
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
print(f"MOTIF ANALYSIS — top {topk_cell} cells by attribution")
print(f"{'='*70}")
print(f"  ss1={seg.ss1_start}–{seg.ss1_end-1}  "
      f"ss2={seg.ss2_start}–{seg.ss2_end-1}  "
      f"flkL={seg.ss1_start - config['clean_flank']}–{seg.ss1_start-1}  "
      f"flkR={seg.ss2_end}–{seg.ss2_end + config['clean_flank']-1}  "
      f"SSE_GAP={SSE_GAP}")
print()

summary_rows = []

for l, h in heads_sorted:
    rank = ie_rank[(l, h)]
    head_cells = [(q, k, attr, adiff)
                  for (ll, hh, q, k, attr, adiff) in ie_circuit_cells
                  if ll == l and hh == h]
    n_cells    = len(head_cells)
    total_attr = sum(a for _, _, a, _ in head_cells)

    if n_cells == 0:
        summary_rows.append((rank, l, h, 0, 0.0, "—", ""))
        print(f"  L{l:2d} H{h:2d} [rank#{rank:2d}]: 0 cells in top-{topk_cell}")
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

    # Offset distribution (q - k), weighted by abs(attr)
    off_mass = defaultdict(float)
    for q, k, attr, _ in head_cells:
        off_mass[q - k] += abs(attr)
    off_sorted  = sorted(off_mass.items(), key=lambda x: x[1], reverse=True)
    total_off   = sum(off_mass.values())

    # Anchor classification
    t1 = abs(key_sorted[0][1]) / total_abs_k if total_abs_k else 0
    t2 = sum(abs(key_sorted[i][1]) for i in range(min(2, len(key_sorted)))) / total_abs_k if total_abs_k else 0
    t3 = sum(abs(key_sorted[i][1]) for i in range(min(3, len(key_sorted)))) / total_abs_k if total_abs_k else 0
    anchor = ("SINGLE-ANCHOR" if t1 >= ANCHOR_T1 else
              "DUAL-ANCHOR"   if t2 >= ANCHOR_T2 else
              "MULTI-ANCHOR"  if t3 >= ANCHOR_T3 else
              "DISTRIBUTED")

    # Positional classification (distinguish cross-SSE offset from local positional)
    top2_off_frac = sum(v for _, v in off_sorted[:2]) / total_off if total_off else 0
    top_offset    = off_sorted[0][0] if off_sorted else 0
    is_cross_sse  = abs(abs(top_offset) - SSE_GAP) <= 3
    if is_cross_sse and top2_off_frac >= POSITIONAL_T:
        pos_tag = "CROSS_SSE"
    elif top2_off_frac >= POSITIONAL_T and abs(top_offset) <= 10:
        pos_tag = "POSITIONAL"
    else:
        pos_tag = ""

    tags = anchor + (f" | {pos_tag}" if pos_tag else "")
    summary_rows.append((rank, l, h, n_cells, total_attr, anchor, pos_tag))
    print(f"  L{l:2d} H{h:2d} [rank#{rank:2d}]: {n_cells} cells | attr={total_attr:+.4f} | {tags}")

    # Key mass
    print(f"       Keys  (top-1={t1:.0%}, top-2={t2:.0%}, top-3={t3:.0%}):")
    for k_pos, k_attr in key_sorted[:5]:
        frac = abs(k_attr) / total_abs_k * 100
        bar  = "█" * int(frac / 5)
        print(f"         k={k_pos:>4d} [{classify_pos(k_pos):5s}]  {k_attr:>+7.4f}  {frac:>5.1f}%  {bar}")
    if len(key_sorted) > 5:
        rest_pct = sum(abs(v) for _, v in key_sorted[5:]) / total_abs_k * 100
        print(f"         … {len(key_sorted)-5} more keys  ({rest_pct:.1f}% of mass)")

    # Query mass
    print(f"       Queries:")
    for q_pos, q_attr in qry_sorted[:5]:
        frac = abs(q_attr) / total_abs_q * 100
        print(f"         q={q_pos:>4d} [{classify_pos(q_pos):5s}]  {q_attr:>+7.4f}  {frac:>5.1f}%")
    if len(qry_sorted) > 5:
        print(f"         … {len(qry_sorted)-5} more queries")

    # Offset distribution
    dom_offsets = ", ".join(f"{o:+d}" for o, _ in off_sorted[:2])
    print(f"       Offsets (q−k), top-2 coverage={top2_off_frac:.0%}  [{dom_offsets}]:")
    for offset, o_mass in off_sorted[:5]:
        frac = o_mass / total_off * 100
        note = (" ← self"        if offset == 0 else
                " ← attend-prev" if offset == 1 else
                " ← attend-next" if offset == -1 else
                f" ← ±{abs(offset)} pos" if abs(offset) <= 5 else
                f" ← ~SSE_GAP"   if abs(abs(offset) - SSE_GAP) <= 3 else "")
        print(f"         Δ={offset:>+6d}  {frac:>5.1f}%{note}")

    # Top 5 cells
    cells_by_attr = sorted(head_cells, key=lambda x: x[2], reverse=True)
    print(f"       Top 5 cells (by attribution):")
    for q, k, attr, adiff in cells_by_attr[:5]:
        print(f"         q={q:>4d}[{classify_pos(q):5s}]  k={k:>4d}[{classify_pos(k):5s}]  "
              f"attr={attr:>+7.4f}  |diff|={adiff:.4f}")

    # Path patching connections
    paths_info = path_srcdst.get((l, h), {'as_src': [], 'as_dst': []})
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

# Compact summary table (also sorted by layer/head)
print(f"\n{'='*70}")
print(f"SUMMARY  (top-{topk_cell} cells, ordered by layer/head)")
print(f"{'='*70}")
print(f"{'rank':>5} {'L':>3} {'H':>3} {'cells':>6} {'total_attr':>11}  {'anchor':>14}  {'pos_type':>10}")
print("-" * 62)
for rank, l, h, n, attr, anchor, pos_tag in sorted(summary_rows, key=lambda x: (x[1], x[2])):
    print(f" #{rank:2d}   L{l:2d} H{h:2d}  {n:>5d}  {attr:>+10.4f}  {anchor:>14}  {pos_tag}")




# %%
