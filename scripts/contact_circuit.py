

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

DATA_PATH = 'data/full_seq_dict.json'
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
SEGMENT_RADIUS = 5

PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}

PLOT_DIR = "reports/outputs"
os.makedirs(PLOT_DIR, exist_ok=True)


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

# %% path attribution 

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
top_k_paths = 100
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

for dl in range(NUM_LAYERS):
    max_val = path_total[dl].abs().max().item()
    if max_val > 0.001:
        print(f"  Dst L{dl}: max path attr = {max_val:.6f}")

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

# How much do late-layer attention patterns change?
for l in [22, 26, 27, 30, 32]:
    for h in range(NUM_HEADS):
        diff = (clean_attn_LBHLL[l][0, h] - corrupt_attn_LBHLL[l][0, h]).abs().sum().item()
        node_val = node_attr_LH[l, h].item()
        if abs(node_val) > 0.001:
            print(f"  L{l}H{h}: node_attr={node_val:+.6f}, attn_diff_L1={diff:.4f}")

# %% ==========================================================================
# Token-level Path Attribution for Top Edges
# =============================================================================
# Break down each top path edge's attribution by token position to identify
# which residues drive the information flow. Requires recomputing the
# clean head outputs and corrupt forward/backward since intermediates were freed.

print("\n=== Token-level Path Attribution ===")

K_TOKEN = 10

# Top K edges by |total attribution|
top_edges = []
for idx in path_flat.abs().argsort(descending=True)[:K_TOKEN * 2]:
    idx_val = idx.item()
    dst_lh, src_lh = idx_val // N, idx_val % N
    dl, dh = dst_lh // NUM_HEADS, dst_lh % NUM_HEADS
    sl, sh = src_lh // NUM_HEADS, src_lh % NUM_HEADS
    if sl < dl:
        top_edges.append((dl, dh, sl, sh))
        if len(top_edges) == K_TOKEN:
            break

for i, (dl, dh, sl, sh) in enumerate(top_edges):
    print(f"  {i+1:2d}. L{sl:2d}H{sh:2d} -> L{dl:2d}H{dh:2d}  attr={path_total[dl,dh,sl,sh].item():+.6f}")

# --- Recompute intermediates ---
print("\n  Recomputing clean head outputs + corrupt forward/backward...")

_clean_ho = []
with model.trace() as tracer:
    with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
        for i in range(NUM_LAYERS):
            _clean_ho.append(model.esm.encoder.layer[i].attention.self.output[0].save())

_sv = {}
_hks = []
for l in range(NUM_LAYERS):
    def _qh(mod, inp, out, l=l):
        out.retain_grad(); _sv[f'q_{l}'] = out
    _hks.append(esm_model.esm.encoder.layer[l].attention.self.query.register_forward_hook(_qh))
    def _kh(mod, inp, out, l=l):
        out.retain_grad(); _sv[f'k_{l}'] = out
    _hks.append(esm_model.esm.encoder.layer[l].attention.self.key.register_forward_hook(_kh))
    def _sh(mod, inp, out, l=l):
        ctx, aw = out; ctx.retain_grad(); _sv[f'ctx_{l}'] = ctx; _sv[f'attn_{l}'] = aw
    _hks.append(esm_model.esm.encoder.layer[l].attention.self.register_forward_hook(_sh))
    def _lnh(mod, inp, out, l=l):
        _sv[f'ln_{l}'] = inp[0]
    _hks.append(esm_model.esm.encoder.layer[l].attention.LayerNorm.register_forward_hook(_lnh))

esm_model(**{**corrupt_inputs_BL, "output_attentions": True})
_m = contact_metric_from_attn_proxies(
    [_sv[f'attn_{l}'] for l in range(NUM_LAYERS)],
    corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'],
    EOS_IDX, REGRESSION_WEIGHT, REGRESSION_BIAS, ORIG_SEG, segment,
)
_m.backward()
for h in _hks:
    h.remove()
print(f"  Metric check: {_m.item():.4f}")

# --- Compute per-token attribution for each edge ---
LN_EPS = esm_model.config.layer_norm_eps
token_attrs = {}
_diff_c, _gq_c, _gk_c = {}, {}, {}

for dl, dh, sl, sh in top_edges:
    if sl not in _diff_c:
        W_O = esm_model.esm.encoder.layer[sl].attention.output.dense.weight.detach().cpu()
        diff = (_clean_ho[sl].detach().cpu() - _sv[f'ctx_{sl}'].detach().cpu()).reshape(B, L, NUM_HEADS, HEAD_DIM)
        _diff_c[sl] = torch.einsum('blhd, Dhd -> blhD', diff, W_O.reshape(HIDDEN_DIM, NUM_HEADS, HEAD_DIM))

    if dl not in _gq_c:
        W_Q = esm_model.esm.encoder.layer[dl].attention.self.query.weight.detach().cpu()
        W_K = esm_model.esm.encoder.layer[dl].attention.self.key.weight.detach().cpu()
        gq = _sv[f'q_{dl}'].grad.detach().cpu().reshape(B, L, NUM_HEADS, HEAD_DIM)
        gk = _sv[f'k_{dl}'].grad.detach().cpu().reshape(B, L, NUM_HEADS, HEAD_DIM)
        gq_r = torch.einsum('blhd, hdD -> blhD', gq, W_Q.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM))
        gk_r = torch.einsum('blhd, hdD -> blhD', gk, W_K.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM))
        ln_in = _sv[f'ln_{dl}'].detach().cpu()
        ln_w = esm_model.esm.encoder.layer[dl].attention.LayerNorm.weight.detach().cpu()
        ln_s = ln_w / (ln_in.std(dim=-1, keepdim=True) + LN_EPS)
        _gq_c[dl] = gq_r * ln_s.unsqueeze(2)
        _gk_c[dl] = gk_r * ln_s.unsqueeze(2)

    d_src = _diff_c[sl][0, :, sh, :]
    tq = (_gq_c[dl][0, :, dh, :] * d_src).sum(-1)
    tk = (_gk_c[dl][0, :, dh, :] * d_src).sum(-1)
    token_attrs[(dl, dh, sl, sh)] = {'q': tq, 'k': tk, 'total': tq + tk}

    check = (tq + tk).sum().item()
    expected = path_total[dl, dh, sl, sh].item()
    print(f"  L{sl}H{sh}->L{dl}H{dh}: token_sum={check:+.6f} (expected={expected:+.6f})")

del _sv, _clean_ho, _diff_c, _gq_c, _gk_c
clear_memory()

# %% Plot token-level attribution
print("Plotting token-level attribution...")

data_token = torch.stack([token_attrs[e]['total'] for e in top_edges]).numpy()

fig, ax = plt.subplots(figsize=(18, 5))
vmax_tok = max(abs(data_token).max(), 1e-8)
im = ax.imshow(data_token, cmap='RdBu_r', aspect='auto', vmin=-vmax_tok, vmax=vmax_tok,
               interpolation='nearest')

edge_labels = [f"L{sl}H{sh}->L{dl}H{dh}" for dl, dh, sl, sh in top_edges]
ax.set_yticks(range(len(top_edges)))
ax.set_yticklabels(edge_labels, fontsize=8)

# Highlight contact segments (+1 for CLS token)
for xpos, color in [(segment.ss1_start + 1, 'green'), (segment.ss1_end, 'green'),
                     (segment.ss2_start + 1, 'orange'), (segment.ss2_end, 'orange')]:
    ax.axvline(x=xpos - 0.5, color=color, linewidth=1.5, alpha=0.8)

# Mark critical flank residues (differ between clean and corrupt)
clean_flank_start = max(0, segment.ss1_start - config["clean_flank"])
corrupt_flank_start = max(0, segment.ss1_start - config["corrupt_flank"])
clean_flank_end = min(len(sequence_S), segment.ss2_end + config["clean_flank"])
corrupt_flank_end = min(len(sequence_S), segment.ss2_end + config["corrupt_flank"])

if clean_flank_start < corrupt_flank_start:
    ax.axvline(x=clean_flank_start + 1, color='magenta', linestyle='--', linewidth=1.5,
               label=f'Critical residue (pos {clean_flank_start})')
if clean_flank_end > corrupt_flank_end:
    ax.axvline(x=corrupt_flank_end + 1, color='magenta', linestyle='--', linewidth=1.5,
               label=f'Critical residue (pos {corrupt_flank_end})')

ax.set_xlabel("Token position (0=CLS, 1..N=AA, N+1=EOS)")
ax.set_title(f"Token-level Path Attribution: Top {len(top_edges)} Edges\n"
             f"{protein}: flank {config['corrupt_flank']}->{config['clean_flank']}")
plt.colorbar(im, ax=ax, label="Attribution", shrink=0.8)
ax.legend(loc='upper right', fontsize=8)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_token_path_attr_top{K_TOKEN}.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_token_path_attr_top{K_TOKEN}.png")
plt.close()

# Focused view around segments
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

margin = 15
# Around segment 1 + flank
s1_lo = max(0, clean_flank_start + 1 - margin)
s1_hi = min(L, segment.ss1_end + margin + 1)
data_s1 = data_token[:, s1_lo:s1_hi]
im1 = ax1.imshow(data_s1, cmap='RdBu_r', aspect='auto', vmin=-vmax_tok, vmax=vmax_tok,
                 extent=[s1_lo, s1_hi, len(top_edges) - 0.5, -0.5], interpolation='nearest')
ax1.set_yticks(range(len(top_edges)))
ax1.set_yticklabels(edge_labels, fontsize=7)
ax1.set_xlabel("Token position")
ax1.set_title(f"Around Segment 1 (AA {segment.ss1_start}-{segment.ss1_end - 1})")
ax1.axvline(x=segment.ss1_start + 1, color='green', linewidth=1.5)
ax1.axvline(x=segment.ss1_end, color='green', linewidth=1.5)
if clean_flank_start < corrupt_flank_start:
    ax1.axvline(x=clean_flank_start + 1, color='magenta', linestyle='--', linewidth=1.5)
plt.colorbar(im1, ax=ax1)

# Around segment 2 + flank
s2_lo = max(0, segment.ss2_start + 1 - margin)
s2_hi = min(L, corrupt_flank_end + margin + 1)
data_s2 = data_token[:, s2_lo:s2_hi]
im2 = ax2.imshow(data_s2, cmap='RdBu_r', aspect='auto', vmin=-vmax_tok, vmax=vmax_tok,
                 extent=[s2_lo, s2_hi, len(top_edges) - 0.5, -0.5], interpolation='nearest')
ax2.set_yticks(range(len(top_edges)))
ax2.set_yticklabels(edge_labels, fontsize=7)
ax2.set_xlabel("Token position")
ax2.set_title(f"Around Segment 2 (AA {segment.ss2_start}-{segment.ss2_end - 1})")
ax2.axvline(x=segment.ss2_start + 1, color='orange', linewidth=1.5)
ax2.axvline(x=segment.ss2_end, color='orange', linewidth=1.5)
if clean_flank_end > corrupt_flank_end:
    ax2.axvline(x=corrupt_flank_end + 1, color='magenta', linestyle='--', linewidth=1.5)
plt.colorbar(im2, ax=ax2)

plt.suptitle(f"Token-level Path Attribution (zoomed): {protein}", fontsize=13)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_token_path_attr_zoom.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_token_path_attr_zoom.png")
plt.close()

# %% ==========================================================================
# Sufficiency Test: Circuit from Path Edges
# =============================================================================
# For increasing K, take the top-K path edges, find the union of all heads
# (src and dst) in those edges. On clean input, corrupt all heads NOT in this
# union. If the path-edge circuit is sufficient, keeping only these heads
# should recover most of the clean metric.
#
# Three sorting criteria (matching contact_jump.py):
#   - |path attr|: largest absolute attribution first
#   - positive:    most positive attribution first
#   - negative:    most negative attribution first

print("\n=== Sufficiency Test: Path Edge Circuit ===")

def get_sorted_valid_edges(path_total_tensor, criterion):
    """Return sorted list of valid (dl, dh, sl, sh) edges."""
    flat = path_total_tensor.reshape(-1)
    if criterion == "abs":
        order = flat.abs().argsort(descending=True)
    elif criterion == "pos":
        order = flat.argsort(descending=True)
    else:
        order = flat.argsort(descending=False)
    edges = []
    for idx in order:
        idx_val = idx.item()
        dst_lh, src_lh = idx_val // N, idx_val % N
        dl, dh = dst_lh // NUM_HEADS, dst_lh % NUM_HEADS
        sl, sh = src_lh // NUM_HEADS, src_lh % NUM_HEADS
        if sl < dl:
            edges.append((dl, dh, sl, sh))
    return edges

sorted_edges_suf = {
    "abs": get_sorted_valid_edges(path_total, "abs"),
    "pos": get_sorted_valid_edges(path_total, "pos"),
    "neg": get_sorted_valid_edges(path_total, "neg"),
}
total_valid_edges = len(sorted_edges_suf["abs"])
total_heads = NUM_LAYERS * NUM_HEADS
print(f"  Total valid edges: {total_valid_edges}")

# K values: fine near start, coarser at tail
k_values_suf = list(range(0, min(31, total_valid_edges)))
k_values_suf += list(range(35, min(101, total_valid_edges), 5))
k_values_suf += list(range(110, min(501, total_valid_edges), 10))
k_values_suf += list(range(550, min(2001, total_valid_edges), 50))
k_values_suf += list(range(2100, 7000, 500))
if total_valid_edges not in k_values_suf:
    k_values_suf.append(total_valid_edges)
k_values_suf = sorted(set(k_values_suf))
print(f"  K values to test: {len(k_values_suf)}")


def get_head_union(edges_list, k):
    """Get union of all (layer, head) pairs appearing as src or dst in top-k edges."""
    heads = set()
    for dl, dh, sl, sh in edges_list[:k]:
        heads.add((sl, sh))
        heads.add((dl, dh))
    return heads


def run_sufficiency(sorted_edges_list, label):
    """Run sufficiency test: keep union-of-heads clean, corrupt the rest."""
    print(f"\n  [{label}] Running {len(k_values_suf)} k-values...")
    scores, head_counts = [], []

    for k_idx, k in enumerate(k_values_suf):
        keep = get_head_union(sorted_edges_list, k)
        head_counts.append(len(keep))

        # Early termination: all heads included
        if len(keep) == total_heads and scores:
            last_score = scores[-1]
            for _ in k_values_suf[k_idx:]:
                scores.append(last_score)
                head_counts.append(total_heads)
            scores = scores[:len(k_values_suf)]
            head_counts = head_counts[:len(k_values_suf)]
            print(f"    All {total_heads} heads covered at k={k}, stopping early")
            break

        with model.trace() as tracer:
            with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
                attn_cache = tracer.cache(
                    modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
                )
                for li in range(NUM_LAYERS):
                    to_corrupt = [h for h in range(NUM_HEADS) if (li, h) not in keep]
                    if not to_corrupt:
                        continue
                    v_raw = model.esm.encoder.layer[li].attention.self.value.output
                    v_h = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)
                    ap = model.esm.encoder.layer[li].attention.self.output[1]
                    pa = ap.clone()
                    for h in to_corrupt:
                        pa[:, h, :, :] = corrupt_attn_LBHLL[li][:, h, :, :].to(device)
                    nc = torch.matmul(pa, v_h).transpose(1, 2).contiguous().reshape(B, L, -1)
                    model.esm.encoder.layer[li].attention.self.output[0][:] = nc

        attn_list = []
        for i in range(NUM_LAYERS):
            key = f"model.esm.encoder.layer.{i}.attention.self"
            la = attn_cache[key].output[1].detach().cpu()
            for h in range(NUM_HEADS):
                if (i, h) not in keep:
                    la[:, h, :, :] = corrupt_attn_LBHLL[i][:, h, :, :]
            attn_list.append(la)

        c_AA = compute_contacts_from_attention(
            attn_list, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
            contact_head, device=device,
        )[0].detach().cpu()

        score = patching_metric(c_AA, orig_contacts_AA, segment)
        scores.append(score)

        if k <= 10 or k_idx % 20 == 0:
            gap = clean_metric - corrupt_metric
            faith = (score - corrupt_metric) / gap if abs(gap) > 1e-6 else 0.0
            print(f"    k={k:4d} edges ({len(keep):3d} heads): faith={faith:.2%}")

    return k_values_suf[:len(scores)], scores, head_counts[:len(scores)]


print(f"Baseline: clean={clean_metric:.4f}, corrupt={corrupt_metric:.4f}, "
      f"gap={clean_metric - corrupt_metric:.4f}")

suf_results = {}
for sn, sl in [("abs", "|path attr|"), ("pos", "positive path"), ("neg", "negative path")]:
    kv, sc, hc = run_sufficiency(sorted_edges_suf[sn], sl)
    gap = clean_metric - corrupt_metric
    faith = [(s - corrupt_metric) / gap if abs(gap) > 1e-6 else 0.0 for s in sc]
    crossed = next((k for k, f in zip(kv, faith) if f >= 0.7), None)
    suf_results[sn] = {"k": kv, "scores": sc, "faith": faith, "head_counts": hc, "crossed_k": crossed}

# %% Plot sufficiency curves
print("Plotting sufficiency results...")

colors_suf = {"abs": "tab:blue", "pos": "tab:green", "neg": "tab:red"}
labels_suf = {"abs": "Sort by |path attr|", "pos": "Sort by positive", "neg": "Sort by negative"}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# Left: faithfulness vs number of edges
for sn in ["abs", "pos", "neg"]:
    r = suf_results[sn]
    ax1.plot(r["k"], r["faith"], '-o', color=colors_suf[sn], markersize=2,
             linewidth=1.5, label=labels_suf[sn])
    crossed = r["crossed_k"]
    if crossed is not None:
        ax1.axvline(x=crossed, color=colors_suf[sn], linestyle=':', linewidth=0.8, alpha=0.5)
        y_off = {"abs": 0.55, "pos": 0.45, "neg": 0.35}[sn]
        ax1.annotate(f"k={crossed}", xy=(crossed, 0.7),
                     xytext=(crossed + max(r["k"]) * 0.03, y_off),
                     arrowprops=dict(arrowstyle='->', color=colors_suf[sn], lw=0.8),
                     fontsize=9, color=colors_suf[sn])

ax1.axhline(y=0.7, color='gray', linestyle='--', linewidth=1, label="70% threshold")
ax1.axhline(y=1.0, color='gray', linestyle=':', linewidth=0.8, alpha=0.4)
ax1.axhline(y=0.0, color='gray', linestyle=':', linewidth=0.8, alpha=0.4)
ax1.set_xlabel("Top-k path edges", fontsize=12)
ax1.set_ylabel("Faithfulness\n(score - corrupt) / (clean - corrupt)", fontsize=12)
ax1.set_title(f"Sufficiency: Path Edge Circuit\n{protein}: flank {config['corrupt_flank']}->{config['clean_flank']}", fontsize=13)
ax1.legend(loc="lower right")
ax1.set_ylim(-0.1, 1.15)
ax1.grid(True, alpha=0.3)

# Right: faithfulness vs unique heads in circuit
for sn in ["abs", "pos", "neg"]:
    r = suf_results[sn]
    ax2.plot(r["head_counts"], r["faith"], '-o', color=colors_suf[sn], markersize=2,
             linewidth=1.5, label=labels_suf[sn])

ax2.axhline(y=0.7, color='gray', linestyle='--', linewidth=1, label="70% threshold")
ax2.axhline(y=1.0, color='gray', linestyle=':', linewidth=0.8, alpha=0.4)
ax2.axhline(y=0.0, color='gray', linestyle=':', linewidth=0.8, alpha=0.4)
ax2.set_xlabel("Unique heads in circuit", fontsize=12)
ax2.set_ylabel("Faithfulness", fontsize=12)
ax2.set_title(f"Sufficiency: Heads in Circuit\n{protein}", fontsize=13)
ax2.legend(loc="lower right")
ax2.set_ylim(-0.1, 1.15)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/{protein}_sufficiency_path_edges.png", dpi=150, bbox_inches='tight')
print(f"  Saved to {PLOT_DIR}/{protein}_sufficiency_path_edges.png")
plt.close()

# Summary
print(f"\n=== Sufficiency Summary ===")
for sn, sl in [("abs", "|path attr|"), ("pos", "positive"), ("neg", "negative")]:
    r = suf_results[sn]
    crossed = r["crossed_k"]
    if crossed is not None:
        idx = r["k"].index(crossed)
        hc = r["head_counts"][idx]
        print(f"  {sl}: 70% at k={crossed} edges ({hc} unique heads, {hc}/{total_heads} = {hc/total_heads:.1%})")
    else:
        print(f"  {sl}: never reached 70%")

# Save results
suf_save = {
    "token_attrs": {k: {qk: v.cpu() for qk, v in d.items()} for k, d in token_attrs.items()},
    "top_edges": top_edges,
    "suf_results": suf_results,
    "sorted_edges_suf": {k: v[:500] for k, v in sorted_edges_suf.items()},
    "protein": protein,
    "clean_metric": clean_metric,
    "corrupt_metric": corrupt_metric,
}
torch.save(suf_save, f"{PLOT_DIR}/{protein}_sufficiency_results.pt")
print(f"  Saved to {PLOT_DIR}/{protein}_sufficiency_results.pt")

# %%
