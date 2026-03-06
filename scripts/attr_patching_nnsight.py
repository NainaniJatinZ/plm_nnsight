# %% [markdown]
# # Attribution Patching for ESM2 Contact Prediction (nnsight + hooks)
#
# Node-level: nnsight caches attention weights, offline autograd for gradients.
# Path-level: nnsight for clean pre-W_O captures, PyTorch hooks for corrupt
#   forward+backward (Q/K with retain_grad). Hooks are needed because ESM2
#   applies RoPE after Q/K projections, so autograd must flow through RoPE
#   to give correct Q/K gradients.
#
# Reference: testing/attribution_patching.py (nnsight node-level pattern)
# Reference: testing/attribution_patching_demo.py (TransformerLens path-level)
# Cross-check: attr_patching.py (PyTorch hooks version — same math, different plumbing)

# %%
from __future__ import annotations
import gc
import json
import os
import torch
import matplotlib.pyplot as plt
from dataclasses import dataclass
from transformers import EsmForMaskedLM, EsmTokenizer
from nnsight import NNsight

# =============================================================================
# Configuration
# =============================================================================
DATA_PATH = 'data/full_seq_dict.json'
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
SEGMENT_RADIUS = 5

PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}

PLOT_DIR = "reports/outputs"
os.makedirs(PLOT_DIR, exist_ok=True)

# =============================================================================
# Utilities
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
    for i in range(max(0, segment.ss1_start - flank_size), segment.ss1_start):
        masked_L[i] = seq_S[i]
    for i in range(segment.ss2_end, min(seq_len, segment.ss2_end + flank_size)):
        masked_L[i] = seq_S[i]
    return "".join(masked_L)

def compute_contacts_from_attention(
    attn_list_BHLL, tokens_BL, attention_mask_BL, contact_head, device="cuda",
):
    """Offline contact computation (for baselines, not inside trace)."""
    attn_list_BHLL = [a.to(device) for a in attn_list_BHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_list_BHLL, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)
    return contact_head(tokens_BL, attns_BLHLL)

def patching_metric(pred_contacts_AA, orig_contacts_AA, segment):
    pred_seg = pred_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    orig_seg = orig_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

# =============================================================================
# Contact head ops as standalone functions (for use inside nnsight trace)
# =============================================================================
# We reimplement the contact head logic as pure tensor ops so that nnsight
# proxy operations can build the autograd graph. The learned weights are
# passed as concrete tensors (not proxies).

def contact_metric_from_attn_proxies(
    attn_proxies,
    tokens_BL,
    attention_mask_BL,
    eos_idx,
    regression_weight,
    regression_bias,
    orig_seg,
    segment,
):
    """
    Compute the contact patching metric from attention weight proxies.
    All tensor ops are proxy-safe (torch.stack, indexing, matmul, etc).

    Args:
        attn_proxies: list of (B, H, L, L) attention weight proxies, one per layer
        tokens_BL: (B, L) concrete token ids
        attention_mask_BL: (B, L) concrete attention mask
        eos_idx: int, EOS token id
        regression_weight: (1, num_layers*num_heads) concrete weight from contact head
        regression_bias: (1,) concrete bias
        orig_seg: (seg1, seg2) concrete original contact segment
        segment: ContactSegment
    """
    # Stack: (B, num_layers, H, L, L)
    attns = torch.stack(attn_proxies, dim=1)

    # Apply attention mask
    attns = attns * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns = attns * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)

    # EOS mask
    eos_mask = tokens_BL.ne(eos_idx).float()
    eos_mask_2d = eos_mask.unsqueeze(1) * eos_mask.unsqueeze(2)  # (B, L, L)
    attns = attns * eos_mask_2d[:, None, None, :, :]

    # Remove CLS (first) and EOS (last) tokens
    attns = attns[..., :-1, :-1]
    attns = attns[..., 1:, 1:]

    batch_size, layers, heads, seqlen, _ = attns.shape
    attns = attns.reshape(batch_size, layers * heads, seqlen, seqlen)

    # Symmetrize
    attns = attns + attns.transpose(-1, -2)

    # Average Product Correction (APC)
    a1 = attns.sum(-1, keepdim=True)
    a2 = attns.sum(-2, keepdim=True)
    a12 = attns.sum(dim=(-1, -2), keepdim=True)
    avg = a1 * a2 / a12
    attns = attns - avg

    # Linear regression: (B, seqlen, seqlen, channels) @ (channels, 1) + bias → sigmoid
    attns = attns.permute(0, 2, 3, 1)  # (B, seqlen, seqlen, channels)
    contacts = torch.sigmoid(torch.nn.functional.linear(attns, regression_weight, regression_bias))
    contacts = contacts.squeeze(3)  # (B, seqlen, seqlen)

    # Metric on segment
    pred_seg = contacts[0, segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    metric = (pred_seg * orig_seg).sum() / (orig_seg * orig_seg).sum()
    return metric

# =============================================================================
# Model Setup
# =============================================================================
# %%
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
model = NNsight(esm_model)
print(model)
NUM_LAYERS = esm_model.config.num_hidden_layers  # 33
NUM_HEADS = esm_model.config.num_attention_heads  # 20
HEAD_DIM = esm_model.config.hidden_size // NUM_HEADS  # 64
HIDDEN_DIM = esm_model.config.hidden_size  # 1280

print(f"Loaded {MODEL_NAME}: {NUM_LAYERS} layers, {NUM_HEADS} heads, dim={HIDDEN_DIM}")
log_memory("after model load")

# Extract contact head parameters (concrete, for use inside traces)
contact_head = esm_model.esm.contact_head
EOS_IDX = contact_head.eos_idx
REGRESSION_WEIGHT = contact_head.regression.weight.detach()  # (1, 660)
REGRESSION_BIAS = contact_head.regression.bias.detach()      # (1,)

# =============================================================================
# Load Data & Compute Baselines
# =============================================================================
# %%
with open(DATA_PATH, "r") as f:
    seq_dict = json.load(f)

protein = "2B61A"
config = PROTEINS[protein]
sequence_S = seq_dict[protein]
segment = ContactSegment.from_contact_pair(*config["contact_pair"])

print(f"Protein: {protein}, Length: {len(sequence_S)}")
print(f"Contact: [{segment.ss1_start}:{segment.ss1_end}] x [{segment.ss2_start}:{segment.ss2_end}]")

# %%
clean_seq_S = mask_with_flanks(sequence_S, segment, config["clean_flank"])
corrupt_seq_S = mask_with_flanks(sequence_S, segment, config["corrupt_flank"])

clean_inputs_BL = tokenizer(clean_seq_S, return_tensors="pt").to(device)
corrupt_inputs_BL = tokenizer(corrupt_seq_S, return_tensors="pt").to(device)

B = 1
L = clean_inputs_BL["input_ids"].shape[1]
print(f"Sequence length (with special tokens): {L}")

# %%
# Full-sequence contacts (ground truth)
inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
with torch.no_grad():
    orig_contacts_AA = esm_model.predict_contacts(
        inputs_BL['input_ids'], inputs_BL['attention_mask']
    )[0].cpu()

# Precompute the orig segment tensor (concrete, reused in traces)
ORIG_SEG = orig_contacts_AA[
    segment.ss1_start:segment.ss1_end,
    segment.ss2_start:segment.ss2_end,
].to(device)

# %%
# Baseline metrics
def cache_attention_nnsight(model, inputs_BL, num_layers):
    with model.trace() as tracer:
        with tracer.invoke(**{**inputs_BL, "output_attentions": True}):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )
    attn_list = []
    for i in range(num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_list.append(attn_cache[key].output[1].detach().cpu())
    return attn_list

print("Caching attention...")
clean_attn_LBHLL = cache_attention_nnsight(model, clean_inputs_BL, NUM_LAYERS)
corrupt_attn_LBHLL = cache_attention_nnsight(model, corrupt_inputs_BL, NUM_LAYERS)

clean_contacts_AA = compute_contacts_from_attention(
    clean_attn_LBHLL, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
    contact_head, device=device,
)[0].detach().cpu()
corrupt_contacts_AA = compute_contacts_from_attention(
    corrupt_attn_LBHLL, corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'],
    contact_head, device=device,
)[0].detach().cpu()

clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, segment)
corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment)
print(f"Clean metric:   {clean_metric:.4f}")
print(f"Corrupt metric: {corrupt_metric:.4f}")
print(f"Gap:            {clean_metric - corrupt_metric:.4f}")

# =============================================================================
# Node-level Attribution Patching
# =============================================================================
# Our contact metric depends on attention weights (output[1]), NOT the context
# vector (output[0]). The metric doesn't flow through the residual stream.
#
# Attention weights were already cached via nnsight (tracer.cache) in the
# baseline section. We compute the metric offline with requires_grad on the
# corrupt attention weights, then backward to get per-head attribution.
#
# Attribution: grad_attn * (clean_attn - corrupt_attn), summed per head.
# This measures each head's direct contribution to the contact metric.
# %%
print("\n=== Node-level Attribution Patching ===")

# Make corrupt attention weights differentiable (from nnsight-cached values)
corrupt_attn_grad = [
    a.clone().detach().to(device).requires_grad_(True) for a in corrupt_attn_LBHLL
]

# Compute metric offline using the same function
node_metric = contact_metric_from_attn_proxies(
    corrupt_attn_grad,
    corrupt_inputs_BL['input_ids'],
    corrupt_inputs_BL['attention_mask'],
    EOS_IDX,
    REGRESSION_WEIGHT,
    REGRESSION_BIAS,
    ORIG_SEG,
    segment,
)
print(f"  Corrupt metric (from offline recompute): {node_metric.item():.4f}")
node_metric.backward()

# Compute node attribution: grad * (clean - corrupt), summed per head
# attention weights shape: (B, H, L, L)
node_attr_LH = torch.zeros(NUM_LAYERS, NUM_HEADS)

for l in range(NUM_LAYERS):
    grad_BHLL = corrupt_attn_grad[l].grad  # (B, H, L, L)
    clean_BHLL = clean_attn_LBHLL[l].to(device)
    corrupt_BHLL = corrupt_attn_LBHLL[l].to(device)

    attr = (grad_BHLL * (clean_BHLL - corrupt_BHLL)).sum(dim=(0, 2, 3))  # (H,)
    node_attr_LH[l] = attr.detach().cpu()

del corrupt_attn_grad
clear_memory()
print(f"  Node attribution shape: {node_attr_LH.shape}")

# %%
# Plot
fig, ax = plt.subplots(figsize=(12, 8))
vmax = node_attr_LH.abs().max().item()
im = ax.imshow(node_attr_LH.numpy(), cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax)
ax.set_xlabel("Head")
ax.set_ylabel("Layer")
ax.set_title(f"Node Attribution (attention weights)\n{protein}: flank {config['corrupt_flank']}→{config['clean_flank']}")
plt.colorbar(im, ax=ax, label="Attribution")
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_node_attr_nnsight.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_node_attr_nnsight.png")
plt.close()

# %%
top_k = 10
flat = node_attr_LH.flatten()
top_idx = flat.abs().argsort(descending=True)[:top_k]

print(f"\nTop {top_k} heads by |node attribution| (attention weights):")
for idx in top_idx:
    l = idx // NUM_HEADS
    h = idx % NUM_HEADS
    val = node_attr_LH[l, h].item()
    print(f"  L{l:2d} H{h:2d}: {val:+.6f}")

# Free node-level intermediates
clear_memory()

# =============================================================================
# Path-level Attribution Patching
# =============================================================================
# Following testing/attribution_patching_demo.py "Head Path Attribution Patching":
#   path_attr[src, dst, qk] = grad_residual_input_to_dst_QK · diff_head_result_src
#
# Strategy:
#   1. nnsight trace: capture clean pre-W_O (context vectors)
#   2. PyTorch hooks for corrupt forward+backward: capture Q, K (with
#      retain_grad), attention weights, pre-W_O, and LN inputs. Compute
#      metric from hook-captured attention weights, then backward() gives
#      correct Q/K grads through the FULL autograd graph (softmax → RoPE →
#      Q/K projections). This is necessary because ESM2 applies RoPE after
#      the Q/K linear projections, so analytical softmax Jacobian on pre-RoPE
#      Q/K values gives wrong gradients.
#   3. Back-project Q/K grads through W_Q/W_K + LN scale → path attribution
# %%
print("\n=== Path-level Attribution Patching ===")

clean_head_out = []

# --- Clean trace via nnsight: save pre-W_O ---
with model.trace() as tracer:
    with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
        for i in range(NUM_LAYERS):
            ho = model.esm.encoder.layer[i].attention.self.output[0]
            clean_head_out.append(ho.save())

print("  Clean trace (nnsight) complete.")

# --- Corrupt forward+backward via PyTorch hooks ---
# Register hooks to capture Q, K (with retain_grad for autograd), attention
# weights, pre-W_O (context), and LayerNorm inputs.
print("  Corrupt forward + backward (PyTorch hooks)...")

saved_corrupt = {}
hooks = []
for l in range(NUM_LAYERS):
    def q_hook(module, input, output, l=l):
        output.retain_grad()
        saved_corrupt[f'q_{l}'] = output
    hooks.append(esm_model.esm.encoder.layer[l].attention.self.query.register_forward_hook(q_hook))

    def k_hook(module, input, output, l=l):
        output.retain_grad()
        saved_corrupt[f'k_{l}'] = output
    hooks.append(esm_model.esm.encoder.layer[l].attention.self.key.register_forward_hook(k_hook))

    def self_hook(module, input, output, l=l):
        context, attn_weights = output
        context.retain_grad()
        attn_weights.retain_grad()
        saved_corrupt[f'context_{l}'] = context
        saved_corrupt[f'attn_{l}'] = attn_weights
    hooks.append(esm_model.esm.encoder.layer[l].attention.self.register_forward_hook(self_hook))

    def ln_hook(module, input, output, l=l):
        saved_corrupt[f'ln_input_{l}'] = input[0]
    hooks.append(esm_model.esm.encoder.layer[l].attention.LayerNorm.register_forward_hook(ln_hook))

# Forward pass (gradients enabled)
esm_model(**{**corrupt_inputs_BL, "output_attentions": True})

# Compute metric from hook-captured attention weights (still in autograd graph)
attn_from_hooks = [saved_corrupt[f'attn_{l}'] for l in range(NUM_LAYERS)]
path_metric = contact_metric_from_attn_proxies(
    attn_from_hooks,
    corrupt_inputs_BL['input_ids'],
    corrupt_inputs_BL['attention_mask'],
    EOS_IDX,
    REGRESSION_WEIGHT,
    REGRESSION_BIAS,
    ORIG_SEG,
    segment,
)
path_metric.backward()

for h in hooks:
    h.remove()

has_q_grad = sum(1 for l in range(NUM_LAYERS) if saved_corrupt[f'q_{l}'].grad is not None)
has_k_grad = sum(1 for l in range(NUM_LAYERS) if saved_corrupt[f'k_{l}'].grad is not None)
print(f"  Metric: {path_metric.item():.4f}")
print(f"  Q grads: {has_q_grad}/{NUM_LAYERS}, K grads: {has_k_grad}/{NUM_LAYERS}")

# %%
# Compute path attributions
print("Computing path attributions...")

LN_EPS = esm_model.config.layer_norm_eps

# 1. Per-head output diff in d_model space (clean - corrupt, through W_O)
diff_head_results = []
for l in range(NUM_LAYERS):
    W_O = esm_model.esm.encoder.layer[l].attention.output.dense.weight.detach().cpu()
    clean_pre_wo = clean_head_out[l].detach().cpu()
    corrupt_pre_wo = saved_corrupt[f'context_{l}'].detach().cpu()
    diff_pre_wo = clean_pre_wo - corrupt_pre_wo
    diff_per_head = diff_pre_wo.reshape(B, L, NUM_HEADS, HEAD_DIM)
    W_O_per_head = W_O.reshape(HIDDEN_DIM, NUM_HEADS, HEAD_DIM)
    diff_dmodel = torch.einsum('blhd, Dhd -> blhD', diff_per_head, W_O_per_head)
    diff_head_results.append(diff_dmodel)

diff_stack = torch.stack(diff_head_results, dim=0)  # (layers, B, L, H, D)
print(f"  diff_head_result shape: {diff_stack.shape}")

# 2. Grad w.r.t. residual stream through Q and K
grad_resid_Q_list = []
grad_resid_K_list = []

for l in range(NUM_LAYERS):
    # Q gradient → back-project through W_Q, per head
    gq = saved_corrupt[f'q_{l}'].grad.detach().cpu()  # (B, L, D)
    gq_per_head = gq.reshape(B, L, NUM_HEADS, HEAD_DIM)
    W_Q = esm_model.esm.encoder.layer[l].attention.self.query.weight.detach().cpu()
    W_Q_ph = W_Q.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    gq_resid = torch.einsum('blhd, hdD -> blhD', gq_per_head, W_Q_ph)

    # K gradient → back-project through W_K, per head
    gk = saved_corrupt[f'k_{l}'].grad.detach().cpu()  # (B, L, D)
    gk_per_head = gk.reshape(B, L, NUM_HEADS, HEAD_DIM)
    W_K = esm_model.esm.encoder.layer[l].attention.self.key.weight.detach().cpu()
    W_K_ph = W_K.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    gk_resid = torch.einsum('blhd, hdD -> blhD', gk_per_head, W_K_ph)

    # LayerNorm scale correction
    ln_input = saved_corrupt[f'ln_input_{l}'].detach().cpu()  # (B, L, D)
    ln_weight = esm_model.esm.encoder.layer[l].attention.LayerNorm.weight.detach().cpu()
    ln_scale = ln_weight / (ln_input.std(dim=-1, keepdim=True) + LN_EPS)  # (B, L, D)

    gq_resid = gq_resid * ln_scale.unsqueeze(2)  # (B, L, 1, D) broadcast to (B, L, H, D)
    gk_resid = gk_resid * ln_scale.unsqueeze(2)

    grad_resid_Q_list.append(gq_resid)
    grad_resid_K_list.append(gk_resid)

grad_Q_stack = torch.stack(grad_resid_Q_list, dim=0)  # (layers, B, L, H, D)
grad_K_stack = torch.stack(grad_resid_K_list, dim=0)
print(f"  grad_resid_Q shape: {grad_Q_stack.shape}")

# 3. Path attribution: dot product
path_attr_Q = torch.einsum('dblhD, sblgD -> dhsg', grad_Q_stack, diff_stack)
path_attr_K = torch.einsum('dblhD, sblgD -> dhsg', grad_K_stack, diff_stack)

# Zero invalid paths (src_layer >= dst_layer)
for d in range(NUM_LAYERS):
    path_attr_Q[d, :, d:, :] = 0
    path_attr_K[d, :, d:, :] = 0

path_attr_QK = torch.stack([path_attr_Q, path_attr_K], dim=0)
print(f"  path_attr shape: {path_attr_QK.shape}")

# Free intermediates
del diff_head_results, diff_stack, grad_resid_Q_list, grad_resid_K_list
del grad_Q_stack, grad_K_stack, saved_corrupt, clean_head_out
clear_memory()

# %%
# Results
path_total = path_attr_QK.sum(dim=0)  # (dst_L, dst_H, src_L, src_H)

# Top paths
top_k_paths = 20
path_flat = path_total.reshape(-1)
top_path_idx = path_flat.abs().argsort(descending=True)[:top_k_paths]
N = NUM_LAYERS * NUM_HEADS

print(f"\nTop {top_k_paths} paths by |attribution|:")
print(f"  {'Source':<12} {'Dest':<12} {'Q attr':>10} {'K attr':>10} {'Total':>10}")
print(f"  {'─'*12} {'─'*12} {'─'*10} {'─'*10} {'─'*10}")
for idx in top_path_idx:
    idx = idx.item()
    dst_lh = idx // N
    src_lh = idx % N
    dl, dh = dst_lh // NUM_HEADS, dst_lh % NUM_HEADS
    sl, sh = src_lh // NUM_HEADS, src_lh % NUM_HEADS
    qv = path_attr_QK[0, dl, dh, sl, sh].item()
    kv = path_attr_QK[1, dl, dh, sl, sh].item()
    print(f"  L{sl:2d}H{sh:2d}  →  L{dl:2d}H{dh:2d}    {qv:+.6f}  {kv:+.6f}  {qv+kv:+.6f}")

# %%
# Plots
src_importance = path_total.sum(dim=(0, 1))
dst_importance = path_total.sum(dim=(2, 3))

fig, axes = plt.subplots(1, 3, figsize=(24, 8))

for ax, data, title in zip(axes, [src_importance, dst_importance, node_attr_LH], [
    "Source Head Importance\n(outgoing paths)",
    "Destination Head Importance\n(incoming paths)",
    "Node Attribution\n(direct, attn weights)",
]):
    vmax = max(data.abs().max().item(), 1e-8)
    im = ax.imshow(data.numpy(), cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax)
    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_title(title)
    plt.colorbar(im, ax=ax)

plt.suptitle(f"Attribution Patching (nnsight): {protein} flank {config['corrupt_flank']}→{config['clean_flank']}", fontsize=14)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_attr_nnsight_summary.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_attr_nnsight_summary.png")
plt.close()

# %%
# Per-head path plots for top node-level heads
top_node_heads = flat.abs().argsort(descending=True)[:6]
top_head_indices = [(idx.item() // NUM_HEADS, idx.item() % NUM_HEADS) for idx in top_node_heads]

fig, axes = plt.subplots(len(top_head_indices), 4, figsize=(24, 4 * len(top_head_indices)))

for row, (tl, th) in enumerate(top_head_indices):
    in_Q = path_attr_QK[0, tl, th, :, :].numpy()
    in_K = path_attr_QK[1, tl, th, :, :].numpy()
    in_total = (path_attr_QK[0, tl, th] + path_attr_QK[1, tl, th]).numpy()
    out_total = path_total[:, :, tl, th].numpy()
    vmax = max(abs(in_Q).max(), abs(in_K).max(), abs(out_total).max(), abs(in_total).max(), 1e-8)

    for col, (data, title) in enumerate([
        (in_Q, f"L{tl}H{th} ← Q"), (in_K, f"L{tl}H{th} ← K"),
        (in_total, f"L{tl}H{th} ← Q+K"), (out_total, f"L{tl}H{th} →"),
    ]):
        ax = axes[row, col] if len(top_head_indices) > 1 else axes[col]
        im = ax.imshow(data, cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax)
        ax.set_xlabel("Head"); ax.set_ylabel("Layer"); ax.set_title(title)
        plt.colorbar(im, ax=ax)

plt.suptitle(f"Path Attribution for Top Heads (nnsight): {protein}", fontsize=14)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_path_attr_nnsight_top.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_path_attr_nnsight_top.png")
plt.close()

# %%
# Save results
results = {
    "node_attr_LH": node_attr_LH,
    "path_attr_QK": path_attr_QK,
    "protein": protein,
    "clean_metric": clean_metric,
    "corrupt_metric": corrupt_metric,
}
torch.save(results, f"{PLOT_DIR}/{protein}_attr_nnsight_results.pt")
print(f"  Saved to {PLOT_DIR}/{protein}_attr_nnsight_results.pt")

# %%
# Cross-check against PyTorch hooks version
torch_results_path = f"{PLOT_DIR}/{protein}_attr_patching_results.pt"
if os.path.exists(torch_results_path):
    torch_results = torch.load(torch_results_path, weights_only=False)
    torch_path = torch_results["path_attr_QK"]
    nnsight_path = path_attr_QK

    # Correlation between the two
    t_flat = torch_path.flatten()
    n_flat = nnsight_path.flatten()
    corr = torch.corrcoef(torch.stack([t_flat, n_flat]))[0, 1].item()
    max_diff = (t_flat - n_flat).abs().max().item()

    print(f"\n=== Cross-check vs PyTorch hooks version ===")
    print(f"  Path attr correlation: {corr:.6f}")
    print(f"  Max absolute diff:     {max_diff:.6f}")
    print(f"  (1.0 = perfect match)")
else:
    print(f"\n  No PyTorch hooks results to cross-check (run attr_patching.py first)")

print("\nDone!")
