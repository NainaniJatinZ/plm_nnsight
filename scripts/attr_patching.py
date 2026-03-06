# %% [markdown]
# # Attribution Patching for ESM2 Contact Prediction
#
# Implements node-level and path-level attribution patching
# for attention heads in ESM2, using the contact prediction metric.
#
# Transferred from contact_jump.py setup.
# Reference: testing/attribution_patching.py (nnsight node-level)
# Reference: testing/attribution_patching_demo.py (TransformerLens path-level)

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
# Utilities (from contact_jump.py)
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

def patching_metric(pred_contacts_AA: torch.Tensor, orig_contacts_AA: torch.Tensor, segment: ContactSegment) -> float:
    pred_seg = pred_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    orig_seg = orig_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

# =============================================================================
# Model Setup
# =============================================================================
# %%
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
model = NNsight(esm_model)

NUM_LAYERS = esm_model.config.num_hidden_layers  # 33
NUM_HEADS = esm_model.config.num_attention_heads  # 20
HEAD_DIM = esm_model.config.hidden_size // NUM_HEADS  # 64
HIDDEN_DIM = esm_model.config.hidden_size  # 1280

print(f"Loaded {MODEL_NAME}: {NUM_LAYERS} layers, {NUM_HEADS} heads, dim={HIDDEN_DIM}")
log_memory("after model load")

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
print(f"Contact segment: [{segment.ss1_start}:{segment.ss1_end}] x [{segment.ss2_start}:{segment.ss2_end}]")

# %%
# Tokenize
clean_seq_S = mask_with_flanks(sequence_S, segment, config["clean_flank"])
corrupt_seq_S = mask_with_flanks(sequence_S, segment, config["corrupt_flank"])

clean_inputs_BL = tokenizer(clean_seq_S, return_tensors="pt").to(device)
corrupt_inputs_BL = tokenizer(corrupt_seq_S, return_tensors="pt").to(device)

B = 1
L = clean_inputs_BL["input_ids"].shape[1]
print(f"Sequence length (with special tokens): {L}")

# %%
# Full-sequence contacts (ground truth for metric)
inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
with torch.no_grad():
    orig_contacts_AA = esm_model.predict_contacts(
        inputs_BL['input_ids'], inputs_BL['attention_mask']
    )[0].cpu()

# %%
# Cache attention for clean and corrupt (reuse for attribution patching)
def cache_attention(model, inputs_BL: dict, device: str) -> list[torch.Tensor]:
    inputs_with_attn = {**inputs_BL, "output_attentions": True}
    with model.trace() as tracer:
        with tracer.invoke(**inputs_with_attn):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
            )
    attn_list_BHLL = []
    for layer_idx in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{layer_idx}.attention.self"
        attn_list_BHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_list_BHLL

print("Caching attention...")
clean_attn_LBHLL = cache_attention(model, clean_inputs_BL, device)
corrupt_attn_LBHLL = cache_attention(model, corrupt_inputs_BL, device)

# Compute baseline contact maps from cached attention
clean_contacts_AA = compute_contacts_from_attention(
    clean_attn_LBHLL, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
    esm_model.esm.contact_head, device=device,
)[0].detach().cpu()

corrupt_contacts_AA = compute_contacts_from_attention(
    corrupt_attn_LBHLL, corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'],
    esm_model.esm.contact_head, device=device,
)[0].detach().cpu()

clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, segment)
corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment)
metric_gap = clean_metric - corrupt_metric

print(f"Clean metric:   {clean_metric:.4f}")
print(f"Corrupt metric: {corrupt_metric:.4f}")
print(f"Gap:            {metric_gap:.4f}")

# =============================================================================
# Part 1: Test gradient compatibility of contact head metric
# =============================================================================
# Question: Can we backprop through contact_head + our patching metric?
# The contact head does: symmetrize -> APC -> linear projection.
# APC divides by sum, but with real attention (not zeros) this should be fine.
# %%
print("\n=== Testing gradient compatibility ===")

# Build a differentiable attention stack from cached clean attention
attn_stack = [a.clone().to(device).requires_grad_(True) for a in clean_attn_LBHLL]

# Forward through contact head
contacts_AA = compute_contacts_from_attention(
    attn_stack,
    clean_inputs_BL['input_ids'],
    clean_inputs_BL['attention_mask'],
    esm_model.esm.contact_head,
    device=device,
)[0]  # (A, A)

# Compute our metric (differentiable version)
pred_seg = contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
orig_seg = orig_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end].to(device)
metric_val = torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)

# Backward
metric_val.backward()

# Check gradients
has_grads = sum(1 for a in attn_stack if a.grad is not None)
grad_norms = [a.grad.norm().item() for a in attn_stack if a.grad is not None]
print(f"  Layers with gradients: {has_grads}/{NUM_LAYERS}")
print(f"  Grad norm range: [{min(grad_norms):.6f}, {max(grad_norms):.6f}]")
print(f"  Metric value: {metric_val.item():.4f} (should match clean_metric={clean_metric:.4f})")
print("  --> Gradients flow through contact head + metric!")

# Clean up
del attn_stack, contacts_AA, pred_seg, metric_val
clear_memory()

# =============================================================================
# Part 2: Node-level Attribution Patching (on attention weights)
# =============================================================================
# attr[l,h] = sum(grad_corrupt_attn[l,h] * (clean_attn[l,h] - corrupt_attn[l,h]))
#
# This is the standard formula: gradient at the corrupt activation times the
# clean-corrupt difference. Approximates what would happen if we patched each
# head's attention from corrupt → clean.
# %%
print("\n=== Part 2: Node-level attribution patching ===")

# Helper: differentiable metric from attention tensors
def differentiable_metric(attn_tensors, tokens_BL, mask_BL, contact_head, segment, orig_contacts_AA, device):
    """Compute patching metric differentiably from attention tensors."""
    contacts = compute_contacts_from_attention(
        attn_tensors, tokens_BL, mask_BL, contact_head, device=device,
    )[0]  # (A, A)
    pred_seg = contacts[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    orig_seg = orig_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end].to(device)
    return torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)

# Step 1: Get gradient of metric w.r.t. corrupt attention weights
corrupt_attn_grad = []
corrupt_attn_requires_grad = [a.clone().to(device).requires_grad_(True) for a in corrupt_attn_LBHLL]

metric_at_corrupt = differentiable_metric(
    corrupt_attn_requires_grad,
    corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'],
    esm_model.esm.contact_head, segment, orig_contacts_AA, device,
)
metric_at_corrupt.backward()

for l in range(NUM_LAYERS):
    corrupt_attn_grad.append(corrupt_attn_requires_grad[l].grad.detach().cpu())

print(f"  Metric at corrupt: {metric_at_corrupt.item():.4f}")

# Step 2: Attribution per head
# attr = grad * (clean - corrupt), summed over batch, dest_pos, src_pos
node_attr_LH = torch.zeros(NUM_LAYERS, NUM_HEADS)
for l in range(NUM_LAYERS):
    grad = corrupt_attn_grad[l]  # (B, H, L, L)
    diff = clean_attn_LBHLL[l] - corrupt_attn_LBHLL[l]  # (B, H, L, L)
    # Sum over batch (dim 0), dest (dim 2), src (dim 3) — keep heads (dim 1)
    node_attr_LH[l] = (grad * diff).sum(dim=(0, 2, 3))

print(f"  Node attribution shape: {node_attr_LH.shape}")

# Clean up
del corrupt_attn_requires_grad, corrupt_attn_grad
clear_memory()

# %%
# Plot node-level attribution heatmap
fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(node_attr_LH.numpy(), cmap='RdBu_r', aspect='auto',
               vmin=-node_attr_LH.abs().max().item(), vmax=node_attr_LH.abs().max().item())
ax.set_xlabel("Head")
ax.set_ylabel("Layer")
ax.set_title(f"Node-level Attribution Patching (attention weights)\n{protein}: flank {config['corrupt_flank']}→{config['clean_flank']}")
plt.colorbar(im, ax=ax, label="Attribution")
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_node_attr_attn.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_node_attr_attn.png")
plt.close()

# %%
# Top heads by node attribution
top_k = 10
flat = node_attr_LH.flatten()
top_idx = flat.abs().argsort(descending=True)[:top_k]

print(f"\nTop {top_k} heads by |node attribution|:")
for idx in top_idx:
    l = idx // NUM_HEADS
    h = idx % NUM_HEADS
    val = node_attr_LH[l, h].item()
    print(f"  L{l:2d} H{h:2d}: {val:+.6f}")

# =============================================================================
# Part 3: Path-level Attribution Patching (head output → head Q/K input)
# =============================================================================
# Two-phase approach:
# Approach: standard PyTorch forward hooks to capture activations and gradients.
# We run the model forward, capture attention weights from self-attention hooks,
# compute the contact metric, and backward. This gives us gradients at Q, K
# through the full autograd graph (softmax, QK^T, etc).
#
# Formula:
#   path_attr[src_layer, src_head, dst_layer, dst_head, q_or_k] =
#       sum_pos_d(grad_residual_through_QK[dst] * diff_head_result[src])
#
#   where grad_residual_through_Q_h = grad_Q_h @ W_Q_h * ln_scale
#   and diff_head_result = clean_output @ W_O_h^T - corrupt_output @ W_O_h^T
# %%
print("\n=== Part 3: Path-level attribution patching ===")

# Helper: register forward hooks to capture activations
def register_capture_hooks(esm_model, save_dict, num_layers, retain_grads=False):
    """Register hooks on Q, K, self-attention, and LayerNorm modules."""
    hooks = []
    for l in range(num_layers):
        # Q projection output
        def q_hook(module, input, output, l=l):
            if retain_grads:
                output.retain_grad()
            save_dict[f'q_{l}'] = output
        hooks.append(esm_model.esm.encoder.layer[l].attention.self.query.register_forward_hook(q_hook))

        # K projection output
        def k_hook(module, input, output, l=l):
            if retain_grads:
                output.retain_grad()
            save_dict[f'k_{l}'] = output
        hooks.append(esm_model.esm.encoder.layer[l].attention.self.key.register_forward_hook(k_hook))

        # Self-attention output: (context_BLD, attn_weights_BHLL)
        def self_hook(module, input, output, l=l):
            context, attn_weights = output
            if retain_grads:
                context.retain_grad()
                attn_weights.retain_grad()
            save_dict[f'context_{l}'] = context
            save_dict[f'attn_{l}'] = attn_weights
        hooks.append(esm_model.esm.encoder.layer[l].attention.self.register_forward_hook(self_hook))

        # LayerNorm input (residual stream before this layer's attention)
        def ln_hook(module, input, output, l=l):
            save_dict[f'ln_input_{l}'] = input[0]
        hooks.append(esm_model.esm.encoder.layer[l].attention.LayerNorm.register_forward_hook(ln_hook))

    return hooks

# Phase 1: Clean forward — capture head outputs (no grads needed)
print("Phase 1: Clean forward pass...")
saved_clean = {}
hooks = register_capture_hooks(esm_model, saved_clean, NUM_LAYERS, retain_grads=False)
with torch.no_grad():
    esm_model(**{**clean_inputs_BL, "output_attentions": True})
for h in hooks:
    h.remove()
print(f"  Captured {len(saved_clean)} activations")

# Phase 2: Corrupt forward + backward — capture activations and gradients
print("Phase 2: Corrupt forward + metric backward...")
saved_corrupt = {}
hooks = register_capture_hooks(esm_model, saved_corrupt, NUM_LAYERS, retain_grads=True)

# Forward pass (with gradients enabled)
esm_model(**{**corrupt_inputs_BL, "output_attentions": True})

# Compute contact metric from captured attention weights (autograd-connected)
attn_from_hooks = [saved_corrupt[f'attn_{l}'] for l in range(NUM_LAYERS)]
metric_path = differentiable_metric(
    attn_from_hooks,
    corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'],
    esm_model.esm.contact_head, segment, orig_contacts_AA, device,
)
metric_path.backward()

for h in hooks:
    h.remove()

# Verify gradients exist
has_q_grad = sum(1 for l in range(NUM_LAYERS) if saved_corrupt[f'q_{l}'].grad is not None)
has_k_grad = sum(1 for l in range(NUM_LAYERS) if saved_corrupt[f'k_{l}'].grad is not None)
print(f"  Metric: {metric_path.item():.4f}")
print(f"  Q grads: {has_q_grad}/{NUM_LAYERS}, K grads: {has_k_grad}/{NUM_LAYERS}")

# %%
# Phase 3: Compute path attributions offline
print("Phase 3: Computing path attributions...")

# 3a: Compute per-head output differences in d_model space (post-W_O)
# head_result[l, h] = pre_wo_h @ W_O_h^T, shape (B, L, D)
# diff_head_result = clean - corrupt

diff_head_results = []  # list of (B, L, H, D) tensors per layer
for l in range(NUM_LAYERS):
    W_O = esm_model.esm.encoder.layer[l].attention.output.dense.weight  # (D, D)
    clean_pre_wo = saved_clean[f'context_{l}'].detach().cpu()  # (B, L, D)
    corrupt_pre_wo = saved_corrupt[f'context_{l}'].detach().cpu()  # (B, L, D)
    diff_pre_wo = clean_pre_wo - corrupt_pre_wo  # (B, L, D)

    # Reshape to per-head: (B, L, H, D_head)
    diff_per_head = diff_pre_wo.reshape(B, L, NUM_HEADS, HEAD_DIM)

    # Apply W_O per head to get result in d_model space
    # W_O[:, h*D_head:(h+1)*D_head] has shape (D, D_head)
    # result_h = diff_h @ W_O_h^T = (B, L, D_head) @ (D_head, D) → (B, L, D)
    W_O_per_head = W_O.detach().cpu().reshape(HIDDEN_DIM, NUM_HEADS, HEAD_DIM)  # (D, H, D_head)
    diff_in_dmodel = torch.einsum('blhd, Dhd -> blhD', diff_per_head, W_O_per_head)
    # shape: (B, L, H, D)
    diff_head_results.append(diff_in_dmodel)

# Stack: (NUM_LAYERS, B, L, H, D)
diff_head_result_stack = torch.stack(diff_head_results, dim=0)
print(f"  diff_head_result_stack shape: {diff_head_result_stack.shape}")

# 3b: Compute grad w.r.t. residual stream through Q and K
# grad_resid_through_Q_h = grad_Q_h @ W_Q_h * ln_scale
# grad_resid_through_K_h = grad_K_h @ W_K_h * ln_scale
# where ln_scale = LN.weight / (std(x) + eps)

LN_EPS = esm_model.config.layer_norm_eps

grad_resid_Q = []  # list of (B, L, H, D) per layer
grad_resid_K = []

for l in range(NUM_LAYERS):
    # Q gradient and weight
    gq = saved_corrupt[f'q_{l}'].grad.detach().cpu()  # (B, L, D)
    gq_per_head = gq.reshape(B, L, NUM_HEADS, HEAD_DIM)  # (B, L, H, D_head)
    W_Q = esm_model.esm.encoder.layer[l].attention.self.query.weight.detach().cpu()  # (D, D)
    W_Q_per_head = W_Q.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)  # (H, D_head, D)
    # grad_Q_h @ W_Q_h = (B, L, D_head) @ (D_head, D) for each head
    gq_resid = torch.einsum('blhd, hdD -> blhD', gq_per_head, W_Q_per_head)  # (B, L, H, D)

    # K gradient and weight
    gk = saved_corrupt[f'k_{l}'].grad.detach().cpu()  # (B, L, D)
    gk_per_head = gk.reshape(B, L, NUM_HEADS, HEAD_DIM)
    W_K = esm_model.esm.encoder.layer[l].attention.self.key.weight.detach().cpu()  # (D, D)
    W_K_per_head = W_K.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    gk_resid = torch.einsum('blhd, hdD -> blhD', gk_per_head, W_K_per_head)  # (B, L, H, D)

    # LayerNorm scale correction
    ln_input = saved_corrupt[f'ln_input_{l}'].detach().cpu()  # (B, L, D)
    ln_weight = esm_model.esm.encoder.layer[l].attention.LayerNorm.weight.detach().cpu()  # (D,)
    # std along last dim
    ln_std = ln_input.std(dim=-1, keepdim=True)  # (B, L, 1)
    ln_scale = ln_weight / (ln_std + LN_EPS)  # (B, L, D) broadcast

    # Apply LN scale
    gq_resid = gq_resid * ln_scale.unsqueeze(2)  # (B, L, 1, D) * (B, L, H, D)
    gk_resid = gk_resid * ln_scale.unsqueeze(2)

    grad_resid_Q.append(gq_resid)
    grad_resid_K.append(gk_resid)

# Stack: (NUM_LAYERS, B, L, H, D)
grad_resid_Q_stack = torch.stack(grad_resid_Q, dim=0)
grad_resid_K_stack = torch.stack(grad_resid_K, dim=0)
print(f"  grad_resid_Q shape: {grad_resid_Q_stack.shape}")

# 3c: Path attribution via dot product
# path_attr[dst_layer, dst_head, src_layer, src_head, qk] =
#   sum_over_batch_pos_d(grad_resid_QK[dst_layer, :, :, dst_head, :] *
#                        diff_head_result[src_layer, :, :, src_head, :])
# Only valid for src_layer < dst_layer (causal ordering in residual stream)

print("  Computing path attribution tensor...")
# Einsum: (dst, B, L, Hdst, D) x (src, B, L, Hsrc, D) → (dst, Hdst, src, Hsrc)
# sum over B, L, D
path_attr_Q = torch.einsum(
    'dblhD, sblgD -> dhsg',
    grad_resid_Q_stack, diff_head_result_stack,
)
path_attr_K = torch.einsum(
    'dblhD, sblgD -> dhsg',
    grad_resid_K_stack, diff_head_result_stack,
)
# shapes: (NUM_LAYERS, NUM_HEADS, NUM_LAYERS, NUM_HEADS)

# Zero out invalid paths (src_layer >= dst_layer)
for dst in range(NUM_LAYERS):
    path_attr_Q[dst, :, dst:, :] = 0
    path_attr_K[dst, :, dst:, :] = 0

# Stack Q and K: (2, dst_layers, dst_heads, src_layers, src_heads)
path_attr_QK = torch.stack([path_attr_Q, path_attr_K], dim=0)
print(f"  path_attr shape: {path_attr_QK.shape} (QK, dst_L, dst_H, src_L, src_H)")

# Free big intermediate tensors
del diff_head_results, diff_head_result_stack
del grad_resid_Q, grad_resid_K, grad_resid_Q_stack, grad_resid_K_stack
del saved_clean, saved_corrupt
clear_memory()

# %%
# Aggregate path attributions for visualization

# Sum over Q and K pathways
path_attr_total = path_attr_QK.sum(dim=0)  # (dst_L, dst_H, src_L, src_H)

# Collapse to (src_layer_head, dst_layer_head) matrix
path_matrix = path_attr_total.reshape(
    NUM_LAYERS * NUM_HEADS, NUM_LAYERS * NUM_HEADS
)  # (dst, src)

# Find top paths
path_flat = path_matrix.flatten()
top_k_paths = 20
top_path_idx = path_flat.abs().argsort(descending=True)[:top_k_paths]

print(f"\nTop {top_k_paths} paths by |attribution|:")
print(f"  {'Source':<12} {'Dest':<12} {'Q attr':>10} {'K attr':>10} {'Total':>10}")
print(f"  {'─'*12} {'─'*12} {'─'*10} {'─'*10} {'─'*10}")
for idx in top_path_idx:
    dst_flat = idx // (NUM_LAYERS * NUM_HEADS)
    src_flat = idx % (NUM_LAYERS * NUM_HEADS)
    dst_l, dst_h = dst_flat // NUM_HEADS, dst_flat % NUM_HEADS
    src_l, src_h = src_flat // NUM_HEADS, src_flat % NUM_HEADS
    q_val = path_attr_QK[0, dst_l, dst_h, src_l, src_h].item()
    k_val = path_attr_QK[1, dst_l, dst_h, src_l, src_h].item()
    total = q_val + k_val
    print(f"  L{src_l:2d}H{src_h:2d}  →  L{dst_l:2d}H{dst_h:2d}    {q_val:+.6f}  {k_val:+.6f}  {total:+.6f}")

# %%
# Plot: aggregate by source head (which heads' outputs matter most for downstream Q/K?)
src_importance = path_attr_total.sum(dim=(0, 1))  # sum over all dst → (src_L, src_H)
dst_importance = path_attr_total.sum(dim=(2, 3))  # sum over all src → (dst_L, dst_H)

fig, axes = plt.subplots(1, 3, figsize=(24, 8))

# Source importance
im0 = axes[0].imshow(src_importance.numpy(), cmap='RdBu_r', aspect='auto',
                      vmin=-src_importance.abs().max().item(), vmax=src_importance.abs().max().item())
axes[0].set_xlabel("Head")
axes[0].set_ylabel("Layer")
axes[0].set_title("Source Head Importance\n(sum of outgoing path attributions)")
plt.colorbar(im0, ax=axes[0])

# Destination importance
im1 = axes[1].imshow(dst_importance.numpy(), cmap='RdBu_r', aspect='auto',
                      vmin=-dst_importance.abs().max().item(), vmax=dst_importance.abs().max().item())
axes[1].set_xlabel("Head")
axes[1].set_ylabel("Layer")
axes[1].set_title("Destination Head Importance\n(sum of incoming path attributions)")
plt.colorbar(im1, ax=axes[1])

# Node-level for comparison
im2 = axes[2].imshow(node_attr_LH.numpy(), cmap='RdBu_r', aspect='auto',
                      vmin=-node_attr_LH.abs().max().item(), vmax=node_attr_LH.abs().max().item())
axes[2].set_xlabel("Head")
axes[2].set_ylabel("Layer")
axes[2].set_title("Node Attribution\n(direct effect on attention weights)")
plt.colorbar(im2, ax=axes[2])

plt.suptitle(f"Attribution Patching: {protein} flank {config['corrupt_flank']}→{config['clean_flank']}", fontsize=14)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_path_attr_summary.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_path_attr_summary.png")
plt.close()

# %%
# Plot path attribution for top node-level heads
# For each important head, show its input and output paths
top_node_heads = flat.abs().argsort(descending=True)[:6]
top_head_indices = [(idx.item() // NUM_HEADS, idx.item() % NUM_HEADS) for idx in top_node_heads]

fig, axes = plt.subplots(len(top_head_indices), 4, figsize=(24, 4 * len(top_head_indices)))

for row, (tl, th) in enumerate(top_head_indices):
    # Incoming Q paths: path_attr_Q[tl, th, :, :] — which src heads feed into this head's Q
    in_Q = path_attr_QK[0, tl, th, :, :].numpy()  # (src_L, src_H)
    in_K = path_attr_QK[1, tl, th, :, :].numpy()

    # Outgoing paths: path_attr_total[:, :, tl, th] — how this head feeds into dst heads
    out_total = path_attr_total[:, :, tl, th].numpy()  # (dst_L, dst_H)

    # Combined incoming
    in_total = (path_attr_QK[0, tl, th, :, :] + path_attr_QK[1, tl, th, :, :]).numpy()

    vmax = max(abs(in_Q).max(), abs(in_K).max(), abs(out_total).max(), abs(in_total).max(), 1e-8)

    for col, (data, title) in enumerate([
        (in_Q, f"L{tl}H{th} ← Q input"),
        (in_K, f"L{tl}H{th} ← K input"),
        (in_total, f"L{tl}H{th} ← Q+K input"),
        (out_total, f"L{tl}H{th} → output"),
    ]):
        ax = axes[row, col] if len(top_head_indices) > 1 else axes[col]
        im = ax.imshow(data, cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax)
        ax.set_xlabel("Head")
        ax.set_ylabel("Layer")
        ax.set_title(title)
        plt.colorbar(im, ax=ax)

plt.suptitle(f"Path Attribution for Top Heads: {protein}", fontsize=14)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_path_attr_top_heads.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_path_attr_top_heads.png")
plt.close()

# %%
# Save results
results = {
    "node_attr_LH": node_attr_LH,
    "path_attr_QK": path_attr_QK,  # (2, dst_L, dst_H, src_L, src_H)
    "protein": protein,
    "clean_metric": clean_metric,
    "corrupt_metric": corrupt_metric,
}
torch.save(results, f"{PLOT_DIR}/{protein}_attr_patching_results.pt")
print(f"  Saved results to {PLOT_DIR}/{protein}_attr_patching_results.pt")

print("\nDone! All three parts complete.")
