# %% [markdown]
# # Cell-Level Indirect Effect Patching
#
# For each of the top 45 IE heads, we diff the attention patterns (clean - corrupt).
# For each (q, k) cell where diff > 0, we run the indirect effect patching experiment
# but only patch that single cell instead of the full head.
#
# This script first counts how many experiments that would be, then runs them.

# %%
from __future__ import annotations
import gc
import json
import os
import time
import torch
from dataclasses import dataclass
from transformers import EsmForMaskedLM, EsmTokenizer
from nnsight import NNsight

# =============================================================================
# Configuration (copied from contact_jump.py — can't import without executing)
# =============================================================================
DATA_PATH = 'data/full_seq_dict.json'
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
SEGMENT_RADIUS = 5

PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}

protein = "2B61A"
config = PROTEINS[protein]
TOP_K_HEADS = 45  # number of top IE heads to analyze

# =============================================================================
# Core definitions (copied from contact_jump.py)
# =============================================================================
def log_memory(label=""):
    if torch.cuda.is_available():
        alloc = torch.cuda.memory_allocated() / 1e9
        resv = torch.cuda.memory_reserved() / 1e9
        print(f"[Memory - {label}] Allocated: {alloc:.2f} GB, Reserved: {resv:.2f} GB")

def clear_memory():
    gc.collect()
    torch.cuda.empty_cache()

@dataclass
class ContactSegment:
    ss1_start: int
    ss1_end: int
    ss2_start: int
    ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int = SEGMENT_RADIUS):
        return cls(pos1 - radius, pos1 + radius + 1, pos2 - radius, pos2 + radius + 1)

def mask_with_flanks(seq_S: str, segment: ContactSegment, flank_size: int) -> str:
    seq_len = len(seq_S)
    masked_L: list[str] = ["<mask>"] * seq_len
    masked_L[segment.ss1_start:segment.ss1_end] = list(seq_S[segment.ss1_start:segment.ss1_end])
    masked_L[segment.ss2_start:segment.ss2_end] = list(seq_S[segment.ss2_start:segment.ss2_end])
    left_flank_idxs = range(max(0, segment.ss1_start - flank_size), segment.ss1_start)
    right_flank_idxs = range(segment.ss2_end, min(seq_len, segment.ss2_end + flank_size))
    for i in left_flank_idxs:
        masked_L[i] = seq_S[i]
    for i in right_flank_idxs:
        masked_L[i] = seq_S[i]
    return "".join(masked_L)

def compute_contact_map(model, tokenizer, sequence_S: str, device: str) -> torch.Tensor:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        contacts_AA = model.predict_contacts(inputs_BL['input_ids'], inputs_BL['attention_mask'])[0].cpu()
    return contacts_AA

def patching_metric(pred_contacts_AA: torch.Tensor, orig_contacts_AA: torch.Tensor, segment: ContactSegment) -> float:
    pred_seg = pred_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    orig_seg = orig_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

def compute_contacts_from_attention(
    attn_list_BHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor,
    attention_mask_BL: torch.Tensor,
    contact_head,
    device: str = "cuda",
) -> torch.Tensor:
    attn_list_BHLL = [a.to(device) for a in attn_list_BHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_list_BHLL, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)
    return contact_head(tokens_BL, attns_BLHLL)

def cache_attention(model, tokenizer, sequence_S: str, device: str, num_layers: int) -> tuple:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    inputs_with_attn = {**inputs_BL, "output_attentions": True}
    with model.trace() as tracer:
        with tracer.invoke(**inputs_with_attn):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )
    attn_list_BHLL = []
    for layer_idx in range(num_layers):
        key = f"model.esm.encoder.layer.{layer_idx}.attention.self"
        attn_list_BHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_list_BHLL, inputs_BL

# %%
# =============================================================================
# Model + Data Setup
# =============================================================================
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
model = NNsight(esm_model)

NUM_LAYERS = esm_model.config.num_hidden_layers  # 33
NUM_HEADS = esm_model.config.num_attention_heads  # 20
HEAD_DIM = esm_model.config.hidden_size // NUM_HEADS

print(f"Loaded {MODEL_NAME}: {NUM_LAYERS} layers, {NUM_HEADS} heads, head_dim={HEAD_DIM}")
log_memory("after model load")

# %%
with open(DATA_PATH, "r") as f:
    seq_dict = json.load(f)

sequence_S = seq_dict[protein]
segment = ContactSegment.from_contact_pair(*config["contact_pair"])

clean_seq_S = mask_with_flanks(sequence_S, segment, config["clean_flank"])
corrupt_seq_S = mask_with_flanks(sequence_S, segment, config["corrupt_flank"])

print(f"Protein: {protein}, Length: {len(sequence_S)}")
print(f"Contact segment: [{segment.ss1_start}:{segment.ss1_end}] x [{segment.ss2_start}:{segment.ss2_end}]")

# %%
# =============================================================================
# Compute Baselines + Cache Attention
# =============================================================================
orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)
clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_seq_S, device)
corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, device)

clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, segment)
corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment)
print(f"Clean metric:   {clean_metric:.4f}")
print(f"Corrupt metric: {corrupt_metric:.4f}")
print(f"Gap:            {clean_metric - corrupt_metric:.4f}")

# %%
print("Caching attention for clean and corrupt sequences...")
clean_attn_LBHLL, clean_inputs_BL = cache_attention(model, tokenizer, clean_seq_S, device, NUM_LAYERS)
corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention(model, tokenizer, corrupt_seq_S, device, NUM_LAYERS)

B = clean_attn_LBHLL[0].shape[0]  # 1
L = clean_attn_LBHLL[0].shape[-1]  # seq_len with special tokens
print(f"Attention shape per layer: ({B}, {NUM_HEADS}, {L}, {L})")

# %%
# =============================================================================
# Load Top IE Heads
# =============================================================================
saved = torch.load(f'reports/outputs/{protein}_path_patching_full.pt', map_location='cpu')
ie_circuit_heads = [(int(l), int(h)) for l, h in saved['ie_circuit_heads'][:TOP_K_HEADS]]
print(f"\nTop {TOP_K_HEADS} IE heads:")
for i, (l, h) in enumerate(ie_circuit_heads):
    print(f"  {i+1:2d}. Layer {l:2d}, Head {h:2d}")

# %%
# =============================================================================
# Count Cell-Level Experiments
# =============================================================================
# For each head: diff = |clean_attn - corrupt_attn|
# Any cell with nonzero diff means clean and corrupt disagree there
print(f"\n{'='*70}")
print(f"COUNTING CELL-LEVEL EXPERIMENTS (|diff| > threshold)")
print(f"{'='*70}")

cell_counts = []  # (layer, head, n_nonzero, n_total, frac, mean_absdiff, max_absdiff)
all_cells = []    # (layer, head, q, k, abs_diff_value) for all nonzero cells

for layer, head in ie_circuit_heads:
    clean_attn_LL = clean_attn_LBHLL[layer][0, head]   # (L, L)
    corrupt_attn_LL = corrupt_attn_LBHLL[layer][0, head]  # (L, L)
    abs_diff_LL = (clean_attn_LL - corrupt_attn_LL).abs()

    nonzero_mask = abs_diff_LL > 1e-6
    n_nonzero = nonzero_mask.sum().item()
    n_total = L * L
    frac = n_nonzero / n_total

    nz_diffs = abs_diff_LL[nonzero_mask]
    mean_diff = nz_diffs.mean().item() if n_nonzero > 0 else 0.0
    max_diff = nz_diffs.max().item() if n_nonzero > 0 else 0.0

    cell_counts.append((layer, head, n_nonzero, n_total, frac, mean_diff, max_diff))

    # Collect individual cells with absolute diff
    qs, ks = torch.where(nonzero_mask)
    for q, k in zip(qs.tolist(), ks.tolist()):
        all_cells.append((layer, head, q, k, abs_diff_LL[q, k].item()))

total_experiments = sum(c[2] for c in cell_counts)

print(f"\nPer-head breakdown:")
print(f"{'Layer':>5} {'Head':>4} {'#cells':>10} {'/ total':>10} {'frac':>8} {'mean|diff|':>11} {'max|diff|':>10}")
print("-" * 65)
for layer, head, n_nz, n_total, frac, mean_d, max_d in cell_counts:
    print(f"  L{layer:2d}  H{head:2d}  {n_nz:>8,d}  / {n_total:>7,d}  {frac:>7.1%}  {mean_d:>11.6f}  {max_d:>10.6f}")

print(f"\n{'='*70}")
print(f"TOTAL cell-level experiments: {total_experiments:,d}")
print(f"  ({TOP_K_HEADS} heads x ~{total_experiments // TOP_K_HEADS:,d} cells/head average)")
print(f"  Seq length L = {L}, so L*L = {L*L:,d} cells per head")
print(f"{'='*70}")

# %%
# =============================================================================
# Distribution Analysis: Do we need all of them?
# =============================================================================
all_abs_diffs = torch.tensor([c[4] for c in all_cells])  # already absolute
print(f"\n|Diff| distribution across {len(all_cells):,d} cells:")
for pct in [50, 75, 90, 95, 99]:
    val = torch.quantile(all_abs_diffs, pct / 100).item()
    n_above = (all_abs_diffs >= val).sum().item()
    print(f"  {pct}th percentile: {val:.6f}  ({n_above:,d} cells above)")

# Threshold analysis
print(f"\nThreshold analysis (|diff|):")
print(f"{'threshold':>12} {'#cells':>10} {'% of total':>12}")
print("-" * 40)
for thresh in [0.0, 1e-5, 1e-4, 1e-3, 5e-3, 0.01, 0.02, 0.05, 0.1]:
    n = (all_abs_diffs > thresh).sum().item()
    pct = n / len(all_abs_diffs) * 100
    print(f"  > {thresh:<8.5f}  {n:>8,d}  {pct:>10.1f}%")

# %%
# =============================================================================
# Sort cells by diff magnitude for prioritized patching
# =============================================================================
all_cells_sorted = sorted(all_cells, key=lambda x: x[4], reverse=True)  # by |diff| descending
print(f"\nTop 20 cells by |diff|:")
print(f"{'Layer':>5} {'Head':>4} {'q':>5} {'k':>5} {'|diff|':>10}")
print("-" * 35)
for layer, head, q, k, abs_diff in all_cells_sorted[:20]:
    print(f"  L{layer:2d}  H{head:2d}  {q:>4d}  {k:>4d}  {abs_diff:>10.6f}")

# %%
# =============================================================================
# Cell-Level INDIRECT Attribution Patching
# =============================================================================
# The indirect effect for cell (l, h, q, k) flows through the residual stream:
#   cell change → delta output[0] → residual → downstream Q/K → downstream attn → metric
#
# For attribution, we need:
#   1. grad of metric w.r.t. output[0] at each layer (via full model backward)
#   2. How each cell changes output[0]: delta_ctx[q, h_slice] = diff[h,q,k] * V[h,k,:]
#   3. Indirect attr = diff[h,q,k] * dot(V[h, k, :], grad_ctx[q, h_slice])
#
# Vectorized per head: sensitivity_qk = grad_ctx[:, h_slice] @ V[h].T  →  attr = diff * sensitivity
#
# One forward+backward through the FULL MODEL gives all ~6M attributions.

print(f"\n{'='*70}")
print("CELL-LEVEL INDIRECT ATTRIBUTION PATCHING")
print(f"{'='*70}")

# Reimplement contact head as differentiable ops (from attr_patching_nnsight.py)
contact_head_module = esm_model.esm.contact_head
EOS_IDX = contact_head_module.eos_idx
REGRESSION_WEIGHT = contact_head_module.regression.weight.detach()  # (1, 660)
REGRESSION_BIAS = contact_head_module.regression.bias.detach()      # (1,)
ORIG_SEG = orig_contacts_AA[
    segment.ss1_start:segment.ss1_end,
    segment.ss2_start:segment.ss2_end,
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
    EOS_IDX, REGRESSION_WEIGHT, REGRESSION_BIAS, ORIG_SEG, segment,
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

cell_attributions = []  # (layer, head, q, k, indirect_attr, abs_diff)

for layer, head in ie_circuit_heads:
    # V reshaped to heads: (B, L, hidden) → (B, num_heads, L, head_dim)
    v_full = saved_hooks[f'v_{layer}'].detach()  # (B, L, hidden)
    v_heads = v_full.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)  # (B, H, L, HD)
    v_h = v_heads[0, head]  # (L, HD)

    # Gradient of metric w.r.t. context vector at this layer
    grad_ctx = saved_hooks[f'ctx_{layer}'].grad  # (B, L, hidden)
    if grad_ctx is None:
        # Last layer may not have gradient flowing back through output[0]
        # (metric depends on output[1] directly at this layer, not output[0])
        print(f"  Warning: no grad for ctx at layer {layer}, using zeros")
        grad_ctx = torch.zeros(B, L, NUM_HEADS * HEAD_DIM, device=device)
    grad_h = grad_ctx[0, :, head * HEAD_DIM:(head + 1) * HEAD_DIM]  # (L, HD)

    # Sensitivity matrix: how much metric changes per unit attn change at (q, k)
    # sensitivity[q, k] = dot(grad_ctx[q, h_slice], V[h, k, :])
    sensitivity_LL = grad_h @ v_h.T  # (L, L)

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

print(f"\nTotal cells with indirect attribution: {len(cell_attr_sorted):,d}")
print(f"\nTop 20 cells by INDIRECT attribution (positive = helpful):")
print(f"{'Layer':>5} {'Head':>4} {'q':>5} {'k':>5} {'ind_attr':>12} {'|diff|':>10}")
print("-" * 50)
for layer, head, q, k, attr, adiff in cell_attr_sorted[:20]:
    print(f"  L{layer:2d}  H{head:2d}  {q:>4d}  {k:>4d}  {attr:>+11.6f}  {adiff:>10.6f}")

print(f"\nBottom 20 cells (negative = harmful):")
for layer, head, q, k, attr, adiff in cell_attr_sorted[-20:]:
    print(f"  L{layer:2d}  H{head:2d}  {q:>4d}  {k:>4d}  {attr:>+11.6f}  {adiff:>10.6f}")

# Attribution distribution
all_attrs = torch.tensor([c[4] for c in cell_attr_sorted])
print(f"\nIndirect attribution distribution:")
print(f"  Positive: {(all_attrs > 0).sum().item():,d} cells")
print(f"  Negative: {(all_attrs < 0).sum().item():,d} cells")
for pct in [90, 95, 99, 99.5, 99.9]:
    val = torch.quantile(all_attrs, pct / 100).item()
    n_above = (all_attrs >= val).sum().item()
    print(f"  {pct}th percentile: {val:+.8f}  ({n_above:,d} cells above)")

# %%
# =============================================================================
# INDIRECT ATTRIBUTION-RANKED SUFFICIENCY TEST
# =============================================================================
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

    metric = patching_metric(contacts, orig_contacts_AA, segment)
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

print(f"\nBaselines:")
print(f"  Clean: {clean_metric:.4f}, Corrupt: {corrupt_metric:.4f}")
print(f"  Head-level IE circuit (45 heads): ~70% faithfulness")
print(f"  IE-ranked cells (1500): ~19% faithfulness")

# Save indirect attribution results
torch.save({
    'cell_attr_sorted': cell_attr_sorted,
    'attr_sufficiency_results': attr_sufficiency_results,
    'ie_circuit_heads': ie_circuit_heads,
    'clean_metric': clean_metric,
    'corrupt_metric': corrupt_metric,
    'protein': protein,
}, f'reports/outputs/{protein}_cell_indirect_attr_results.pt')
print(f"Saved to reports/outputs/{protein}_cell_indirect_attr_results.pt")

# %%
# =============================================================================
# Cell-Level Indirect Effect Patching
# =============================================================================
# For each (layer, head, q, k) cell: patch only that cell from clean→corrupt,
# recompute context, measure downstream effect on contacts.
#
# This is the same as indirect_effect_single_head but modifying a single cell
# instead of the full head's attention pattern.

def indirect_effect_single_cell(
    model,
    clean_inputs_BL: dict,
    clean_attn_head_LL: torch.Tensor,   # (1, L, L) clean attention for this head
    corrupt_cell_value: float,           # corrupt attention value at (q, k)
    patch_layer: int,
    patch_head: int,
    q_pos: int,
    k_pos: int,
    device: str,
) -> list[torch.Tensor]:
    """
    Indirect effect patching for a single attention cell.

    Same as indirect_effect_single_head, but only patches A[q_pos, k_pos]
    instead of the full head pattern. The attention row for q_pos won't
    sum to 1 after patching — this is intentional (perturbation analysis).

    The effect on context is:
      delta_context[q_pos] = (corrupt_val - clean_val) * V[k_pos]

    Returns:
        downstream_attn: list of attention tensors for layers patch_layer+1..end
    """
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            # Child module: get V
            v_raw = model.esm.encoder.layer[patch_layer].attention.self.value.output
            v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

            # Parent module: get attention probs, patch ONE cell
            orig_attn = model.esm.encoder.layer[patch_layer].attention.self.output[1]
            patched_attn = orig_attn.clone()
            patched_attn[:, patch_head, q_pos, k_pos] = corrupt_cell_value

            # Recompute context
            new_ctx = torch.matmul(patched_attn, v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)

            # Set context vector — propagates through residual stream
            model.esm.encoder.layer[patch_layer].attention.self.output[0][:] = new_ctx

            # Capture downstream attention
            downstream_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self
                         for i in range(patch_layer + 1, NUM_LAYERS)]
            )

    downstream_attn = []
    for i in range(patch_layer + 1, NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        downstream_attn.append(downstream_cache[key].output[1].detach().cpu())

    return downstream_attn


def run_cell_patching_experiment(
    cell_list: list[tuple],  # [(layer, head, q, k, diff_val), ...]
    tag: str = "",
) -> list[dict]:
    """
    Run cell-level indirect effect patching for a list of cells.

    Returns list of result dicts with keys:
        layer, head, q, k, diff, metric, effect
    """
    results = []
    n = len(cell_list)
    start_time = time.time()
    print(f"Running {n:,d} cell-level patching experiments{' (' + tag + ')' if tag else ''}...")

    for i, (layer, head, q, k, diff_val) in enumerate(cell_list):
        corrupt_val = corrupt_attn_LBHLL[layer][0, head, q, k].item()

        # Run single-cell indirect effect
        downstream_attn = indirect_effect_single_cell(
            model, clean_inputs_BL,
            clean_attn_LBHLL[layer][:, head, :, :],
            corrupt_val,
            layer, head, q, k, device,
        )

        # Build full attention stack
        patched_full_attn = list(clean_attn_LBHLL[:layer])

        # Patched layer: clean with one cell changed
        patched_layer_attn = clean_attn_LBHLL[layer].clone()
        patched_layer_attn[:, head, q, k] = corrupt_val
        patched_full_attn.append(patched_layer_attn)

        # Downstream from intervention
        patched_full_attn.extend(downstream_attn)

        # Compute contacts
        contacts_AA = compute_contacts_from_attention(
            patched_full_attn,
            clean_inputs_BL['input_ids'],
            clean_inputs_BL['attention_mask'],
            esm_model.esm.contact_head,
            device=device,
        )[0].detach().cpu()

        metric = patching_metric(contacts_AA, orig_contacts_AA, segment)
        if abs(corrupt_metric - clean_metric) > 1e-6:
            effect = (metric - clean_metric) / (corrupt_metric - clean_metric)
        else:
            effect = 0.0

        results.append({
            'layer': layer, 'head': head, 'q': q, 'k': k,
            'diff': diff_val, 'metric': metric, 'effect': effect,
        })

        if (i + 1) % 100 == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            remaining = (n - i - 1) / rate
            print(f"  {i+1:,d}/{n:,d} | {elapsed:.0f}s elapsed | ~{remaining:.0f}s remaining"
                  f" | last effect={effect:+.4f}")

        # Checkpoint every 1000
        if (i + 1) % 1000 == 0:
            torch.save({
                'results': results,
                'clean_metric': clean_metric,
                'corrupt_metric': corrupt_metric,
                'n_completed': i + 1,
                'n_total': n,
                'tag': tag,
            }, f'reports/outputs/{protein}_cell_patching_checkpoint.pt')
            print(f"    Checkpoint saved ({i+1} cells)")

    elapsed = time.time() - start_time
    print(f"Done! {n:,d} cells in {elapsed:.0f}s ({elapsed/n:.2f}s/cell)")
    return results


# %%
# =============================================================================
# Run on top cells by diff magnitude
# =============================================================================
# Start with top N cells to get a sense of timing and effects
# Adjust N based on the counting results above
N_CELLS = 4000  # start with top 500; increase to 1000+ as needed
cells_to_patch = all_cells_sorted[:N_CELLS]

print(f"\nPatching top {N_CELLS} cells by |diff|")
print(f"|Diff| range: [{cells_to_patch[-1][4]:.6f}, {cells_to_patch[0][4]:.6f}]")

cell_results = run_cell_patching_experiment(cells_to_patch, tag=f"top_{N_CELLS}")

# %%
# =============================================================================
# Analysis
# =============================================================================
print(f"\n{'='*70}")
print(f"CELL-LEVEL PATCHING RESULTS")
print(f"{'='*70}")
print(f"Baselines: clean={clean_metric:.4f}, corrupt={corrupt_metric:.4f}")

# Sort by effect magnitude
cell_results_sorted = sorted(cell_results, key=lambda x: abs(x['effect']), reverse=True)

print(f"\nTop 30 cells by |effect|:")
print(f"{'Layer':>5} {'Head':>4} {'q':>5} {'k':>5} {'diff':>10} {'effect':>10} {'metric':>8}")
print("-" * 55)
for r in cell_results_sorted[:30]:
    print(f"  L{r['layer']:2d}  H{r['head']:2d}  {r['q']:>4d}  {r['k']:>4d}"
          f"  {r['diff']:>10.6f}  {r['effect']:>+9.4f}  {r['metric']:>8.4f}")

# Per-head summary: which heads have the most impactful cells?
from collections import defaultdict
head_effects = defaultdict(list)
for r in cell_results:
    head_effects[(r['layer'], r['head'])].append(abs(r['effect']))

print(f"\nPer-head summary (mean |effect| of tested cells):")
print(f"{'Layer':>5} {'Head':>4} {'#cells':>7} {'mean|eff|':>10} {'max|eff|':>10}")
print("-" * 45)
for (l, h), effs in sorted(head_effects.items(), key=lambda x: max(x[1]), reverse=True):
    effs_t = torch.tensor(effs)
    print(f"  L{l:2d}  H{h:2d}  {len(effs):>5d}  {effs_t.mean():>10.4f}  {effs_t.max():>10.4f}")

# %%
# =============================================================================
# CELL-LEVEL SUFFICIENCY TEST
# =============================================================================
# Corrupt ALL attention (every head, every layer, every cell) to corrupt values,
# EXCEPT the top-K cells which stay clean. If the top-K cells are truly the
# circuit, they should recover performance even with everything else corrupted.
#
# At K=0: fully corrupted → corrupt baseline
# At K grows: more cells protected → faithfulness should increase

print(f"\n{'='*60}")
print("CELL-LEVEL SUFFICIENCY TEST")
print(f"{'='*60}")

# Sort by |effect| (causal importance from individual patching)
cell_results_by_effect = sorted(cell_results, key=lambda x: x['effect'], reverse=True)

thresholds = [0, 10, 20, 50, 100, 200, 300, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
thresholds = [t for t in thresholds if t <= len(cell_results_by_effect)]
sufficiency_results = []

for k in thresholds:
    # Top-K cells are "protected" (stay clean); EVERYTHING else gets corrupted
    protected_cells = set()
    for r in cell_results_by_effect[:k]:
        protected_cells.add((r['layer'], r['head'], r['q'], r['k']))

    protected_heads = set((r['layer'], r['head']) for r in cell_results_by_effect[:k]) if k > 0 else set()

    # Forward pass: corrupt ALL heads at ALL layers, but protect specific cells
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            # Cache BEFORE interventions
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
            )

            # Corrupt every layer
            for layer_idx in range(NUM_LAYERS):
                v_raw = model.esm.encoder.layer[layer_idx].attention.self.value.output
                v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                attn_probs = model.esm.encoder.layer[layer_idx].attention.self.output[1]

                # Start from fully corrupt attention for this layer
                patched_attn = corrupt_attn_LBHLL[layer_idx].to(device).clone()

                # Restore protected cells back to clean (from live attention)
                for head, q, kk in [(h, q, kk) for (l, h, q, kk) in protected_cells if l == layer_idx]:
                    patched_attn[:, head, q, kk] = attn_probs[:, head, q, kk]

                new_ctx = torch.matmul(patched_attn, v_heads)
                new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)
                model.esm.encoder.layer[layer_idx].attention.self.output[0][:] = new_ctx

    # Build attention stack for contact head
    attn_list = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()

        # Overwrite with corrupt, then restore protected cells
        corrupt_layer = corrupt_attn_LBHLL[i].clone()
        for head, q, kk in [(h, q, kk) for (l, h, q, kk) in protected_cells if l == i]:
            corrupt_layer[:, head, q, kk] = layer_attn[:, head, q, kk]
        attn_list.append(corrupt_layer)

    contacts = compute_contacts_from_attention(
        attn_list, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()

    metric = patching_metric(contacts, orig_contacts_AA, segment)
    faithfulness = (metric - corrupt_metric) / (clean_metric - corrupt_metric) \
        if abs(clean_metric - corrupt_metric) > 1e-6 else 0.0

    sufficiency_results.append({
        'k': k, 'n_protected': len(protected_cells),
        'n_heads': len(protected_heads),
        'metric': metric, 'faithfulness': faithfulness,
    })
    print(f"  Top {k:4d} protected ({len(protected_cells):,d} cells clean, rest corrupted) → "
          f"metric={metric:.4f}, faithfulness={faithfulness:.2%}")

print(f"\nBaselines:")
print(f"  Clean: {clean_metric:.4f}, Corrupt: {corrupt_metric:.4f}")
print(f"  Head-level IE circuit (45 heads): ~70% faithfulness")

# %%
# =============================================================================
# Save everything
# =============================================================================
torch.save({
    'cell_results': cell_results,
    'sufficiency_results': sufficiency_results,
    'all_cells_sorted': all_cells_sorted,
    'cell_counts': cell_counts,
    'ie_circuit_heads': ie_circuit_heads,
    'clean_metric': clean_metric,
    'corrupt_metric': corrupt_metric,
    'protein': protein,
    'n_cells_run': len(cell_results),
}, f'reports/outputs/{protein}_cell_patching_results.pt')
print(f"Saved to reports/outputs/{protein}_cell_patching_results.pt")
# %%
