# %% [markdown]
# shape suffixes 

# Throughout this tutorial, we use **shape suffixes** to make tensor dimensions obvious at a glance:

# | Suffix | Meaning |
# |--------|---------|
# | `B` | Batch size |
# | `L` | Sequence length (including special tokens) |
# | `A` | Amino acid positions (excluding special tokens) |
# | `H` | Attention heads |
# | `D` | Hidden dimension |
# | `V` | Vocabulary size |
# | `F` | SAE feature dimension |
# | `K` | Top-k |
# | `S` | String length |

# For example, `attn_weights_BHLL` is a tensor with shape `(batch, heads, seq_len, seq_len)`.

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
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"  # 650M params, 33 layers
# MODEL_NAME = "facebook/esm2_t6_8M_UR50D"  # 8M params, 6 layers

PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}
SEGMENT_RADIUS = 5  # residues on each side of contact position

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

def get_cache_path(protein: str, clean_flank: int, corrupt_flank: int) -> str:
    """Get path for cached metrics."""
    import os
    cache_dir = "reports/cache"
    os.makedirs(cache_dir, exist_ok=True)
    return f"{cache_dir}/{protein}_c{clean_flank}_x{corrupt_flank}_metrics.pt"

def save_metrics_cache(
    protein: str,
    clean_flank: int,
    corrupt_flank: int,
    metrics: dict[str, torch.Tensor],
) -> None:
    """
    Save all head metrics to cache file.

    Args:
        protein: Protein ID
        clean_flank: Clean flank size
        corrupt_flank: Corrupt flank size
        metrics: Dict of metric_name -> (num_layers, num_heads) tensor
    """
    cache_path = get_cache_path(protein, clean_flank, corrupt_flank)
    cache_data = {
        "protein": protein,
        "clean_flank": clean_flank,
        "corrupt_flank": corrupt_flank,
        "metrics": metrics,
    }
    torch.save(cache_data, cache_path)
    print(f"✓ Saved metrics cache to {cache_path}")
    print(f"  Cached metrics: {', '.join(metrics.keys())}")

def load_metrics_cache(protein: str, clean_flank: int, corrupt_flank: int) -> dict[str, torch.Tensor] | None:
    """
    Load cached metrics if they exist.

    Returns:
        Dict of metric_name -> (num_layers, num_heads) tensor, or None if cache doesn't exist
    """
    import os
    cache_path = get_cache_path(protein, clean_flank, corrupt_flank)

    if not os.path.exists(cache_path):
        return None

    try:
        cache_data = torch.load(cache_path)
        print(f"✓ Loaded metrics cache from {cache_path}")
        print(f"  Cached metrics: {', '.join(cache_data['metrics'].keys())}")
        return cache_data["metrics"]
    except Exception as e:
        print(f"⚠ Failed to load cache: {e}")
        return None

def compute_diff_metrics_torch(clean_attn_LL: torch.Tensor, corrupt_attn_LL: torch.Tensor) -> dict[str, float]:
    """
    Compute multiple metrics quantifying attention pattern differences.

    For attention matrices (probability distributions), L1 norm is most interpretable.

    Args:
        clean_attn_LL: Clean attention matrix (seq_len, seq_len)
        corrupt_attn_LL: Corrupt attention matrix (seq_len, seq_len)

    Returns:
        Dict of metric_name -> value:
        - diff_l1: Sum of absolute differences (total variation distance)
        - diff_max: Maximum absolute difference (worst-case deviation)
        - diff_l2: Frobenius norm (L2) for comparison
    """
    diff = clean_attn_LL - corrupt_attn_LL

    return {
        "diff_l1": torch.sum(torch.abs(diff)).item(),
        "diff_max": torch.max(torch.abs(diff)).item(),
        "diff_l2": torch.sqrt(torch.sum(diff ** 2)).item(),
    }

# =============================================================================
# Core Functions
# =============================================================================
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
    """Mask sequence except for contact segments and flanking regions."""
    seq_len = len(seq_S)
    masked_L: list[str] = ["<mask>"] * seq_len

    # Unmask contact segments
    masked_L[segment.ss1_start:segment.ss1_end] = list(seq_S[segment.ss1_start:segment.ss1_end])
    masked_L[segment.ss2_start:segment.ss2_end] = list(seq_S[segment.ss2_start:segment.ss2_end])

    # Unmask flanks
    left_flank_idxs = range(max(0, segment.ss1_start - flank_size), segment.ss1_start)
    right_flank_idxs = range(segment.ss2_end, min(seq_len, segment.ss2_end + flank_size))
    for i in left_flank_idxs:
        masked_L[i] = seq_S[i]
    for i in right_flank_idxs:
        masked_L[i] = seq_S[i]

    return "".join(masked_L)

def compute_contact_map(model, tokenizer, sequence_S: str, device: str) -> torch.Tensor:
    """Compute contact predictions for a sequence."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        contacts_AA = model.predict_contacts(inputs_BL['input_ids'], inputs_BL['attention_mask'])[0].cpu()
    return contacts_AA

def patching_metric(pred_contacts_AA: torch.Tensor, orig_contacts_AA: torch.Tensor, segment: ContactSegment) -> float:
    """Compute overlap metric between predicted and original contacts in segment."""
    pred_seg = pred_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    orig_seg = orig_contacts_AA[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

PLOT_DIR = "reports/outputs"
os.makedirs(PLOT_DIR, exist_ok=True)

def plot_contact_map(contacts_AA: torch.Tensor, title: str, filename: str | None = None):
    plt.figure(figsize=(6, 6))
    plt.imshow(contacts_AA, cmap='viridis', aspect='equal')
    plt.colorbar(label="Contact Probability")
    plt.title(title)
    plt.xlabel("Residue Index")
    plt.ylabel("Residue Index")
    plt.tight_layout()
    if filename:
        plt.savefig(f"{PLOT_DIR}/{filename}", dpi=150, bbox_inches='tight')
        print(f"  Saved plot to {PLOT_DIR}/{filename}")
    plt.close()

# =============================================================================
# Model Setup
# =============================================================================
# %%
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
model = NNsight(esm_model)

print(f"Loaded {MODEL_NAME}: {esm_model.config.num_hidden_layers} layers, {esm_model.config.hidden_size} hidden")
log_memory("after model load")

# =============================================================================
# Load Data
# =============================================================================
# %%
with open(DATA_PATH, "r") as f:
    seq_dict = json.load(f)

protein = "2B61A"
config = PROTEINS[protein]
sequence_S = seq_dict[protein]
segment = ContactSegment.from_contact_pair(*config["contact_pair"])
inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)

print(f"Protein: {protein}, Length: {len(sequence_S)}")
print(f"Contact segment: [{segment.ss1_start}:{segment.ss1_end}] x [{segment.ss2_start}:{segment.ss2_end}]")

# =============================================================================
# Compute Contact Maps
# =============================================================================
# %%
# Original (full sequence)
orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)
# plot_contact_map(orig_contacts_AA, f"{protein} - Full Sequence")

# %%
# Clean (larger flank - higher metric)
clean_seq_S = mask_with_flanks(sequence_S, segment, config["clean_flank"])
clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_seq_S, device)

# Corrupt (smaller flank - lower metric)
corrupt_seq_S = mask_with_flanks(sequence_S, segment, config["corrupt_flank"])
corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, device)

# =============================================================================
# Results
# =============================================================================
# %%
print(f"\nPatching Metrics (flank size -> metric):")
print(f"  Original (full):     1.000")
print(f"  Clean (flank={config['clean_flank']}):   {patching_metric(clean_contacts_AA, orig_contacts_AA, segment):.4f}")
print(f"  Corrupt (flank={config['corrupt_flank']}): {patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment):.4f}")

# %%
# Sweep flank sizes to find the jump
print("\nFlank sweep:")
for flank in range(config["corrupt_flank"] - 2, config["clean_flank"] + 3):
    masked_seq_S = mask_with_flanks(sequence_S, segment, flank)
    contacts_AA = compute_contact_map(esm_model, tokenizer, masked_seq_S, device)
    metric = patching_metric(contacts_AA, orig_contacts_AA, segment)
    print(f"  flank={flank:3d}: {metric:.4f}")


# %%
NUM_LAYERS = esm_model.config.num_hidden_layers  # 33
NUM_HEADS = esm_model.config.num_attention_heads  # 20

def compute_contacts_from_attention(
    attn_list_BHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor,
    attention_mask_BL: torch.Tensor,
    contact_head,
    device: str = "cuda",
) -> torch.Tensor:
    """
    Replicates predict_contacts logic:
    1. Stack attentions from all layers
    2. Apply attention mask
    3. Call contact_head

    Note: Cannot use zeros for ablation - contact_head uses APC which divides by sum.
    """
    attn_list_BHLL = [a.to(device) for a in attn_list_BHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)

    attns_BLHLL = torch.stack(attn_list_BHLL, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)

    return contact_head(tokens_BL, attns_BLHLL)


def cache_attention(model, tokenizer, sequence_S: str, device: str) -> list[torch.Tensor]:
    """Cache attention weights from all layers for a sequence."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
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

    return attn_list_BHLL, inputs_BL

# =============================================================================
# Cache Attention for Clean and Corrupt Sequences
# =============================================================================
# %%
print("Caching attention for clean and corrupt sequences...")

clean_attn_LBHLL, clean_inputs_BL = cache_attention(model, tokenizer, clean_seq_S, device)
corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention(model, tokenizer, corrupt_seq_S, device)

print(f"  Clean attention: {len(clean_attn_LBHLL)} layers, shape {clean_attn_LBHLL[0].shape}")
print(f"  Corrupt attention: {len(corrupt_attn_LBHLL)} layers, shape {corrupt_attn_LBHLL[0].shape}")

# Compute baseline metrics
clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, segment)
corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment)
print(f"\nBaseline metrics:")
print(f"  Clean: {clean_metric:.4f}")
print(f"  Corrupt: {corrupt_metric:.4f}")
print(f"  Gap: {clean_metric - corrupt_metric:.4f}")


# =============================================================================
# Indirect Effect Analysis
# =============================================================================
# The direct effect (above) patches attention into the contact head directly.
# The indirect effect measures how changing attention at one layer propagates
# through the model to affect downstream layers' attention AND contact prediction.
#
# Key insight: attention.self.output[1] (attn probs) is a dead-end output.
# Setting it doesn't change model computation. We must intervene on output[0]
# (the context vector = attn_probs @ V), which flows through the residual stream.
#
# Recipe (single trace with tracer.cache):
#   1. Access V from .value.output (child module — hooks before parent)
#   2. Access attention probs from .output[1], patch one head
#   3. Recompute context = patched_attn @ V (proxy math inside trace)
#   4. Set output[0] = new_context (flows through residual stream)
#   5. Capture downstream attention with tracer.cache()
#   6. Build full attention stack for contact prediction
# %%
HEAD_DIM = esm_model.config.hidden_size // NUM_HEADS
B = clean_attn_LBHLL[0].shape[0]  # 1
L = clean_attn_LBHLL[0].shape[-1]  # seq_len with special tokens

# %%
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

# %%

cached_metrics = load_metrics_cache(protein, config["clean_flank"], config["corrupt_flank"])
head_metrics = cached_metrics.copy()
INDIRECT_CACHE_KEY = "indirect_effect"
top_k = 45 

# %%
# Compute indirect effects for all heads
# For each head: patch it, get downstream attention, compute contacts, measure effect
# FORCE_INDIRECT_RECALC = False
# INDIRECT_CACHE_KEY = "indirect_effect"

# if not FORCE_INDIRECT_RECALC and INDIRECT_CACHE_KEY in head_metrics:
#     print(f"\n✓ Using cached indirect effects")
#     indirect_effects_LH = head_metrics[INDIRECT_CACHE_KEY]
# else:
print(f"\nComputing indirect effects for all {NUM_LAYERS * NUM_HEADS} heads...")
print(f"  Each head requires 1 trace (V + intervention + downstream capture)")
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
        indirect_metric = patching_metric(indirect_contacts_AA, orig_contacts_AA, segment)
        if abs(corrupt_metric - clean_metric) > 1e-6:
            effect = (indirect_metric - clean_metric) / (corrupt_metric - clean_metric)
        else:
            effect = 0.0
        indirect_effects_LH[layer_idx, head_idx] = effect

    if (layer_idx + 1) % 5 == 0:
        print(f"    Processed layer {layer_idx + 1}/{NUM_LAYERS}")

print("Done!")
head_metrics[INDIRECT_CACHE_KEY] = indirect_effects_LH
save_metrics_cache(protein, config["clean_flank"], config["corrupt_flank"], head_metrics)

# %%
# Compare direct vs indirect effects
print(f"\nTop {top_k} heads by absolute indirect effect:")
indirect_flat = indirect_effects_LH.flatten()
indirect_top_indices = indirect_flat.argsort(descending=True)[:top_k]
layer_head_indices = [(idx // NUM_HEADS, idx % NUM_HEADS) for idx in indirect_top_indices]
for layer, head in layer_head_indices:
    ind_eff = indirect_effects_LH[layer, head].item()
    print(f"  Layer {layer:2d}, Head {head:2d}: indirect = {ind_eff:+.4f}")
ie_circuit_heads = layer_head_indices 

# %%

# Clean Q/K baseline (one forward pass)
with model.trace() as tracer:
    with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
        qk_cache = tracer.cache(
            modules=[model.esm.encoder.layer[i].attention.self.query for i in range(NUM_LAYERS)]
                  + [model.esm.encoder.layer[i].attention.self.key for i in range(NUM_LAYERS)]
        )

clean_qk = {}
for i in range(NUM_LAYERS):
    clean_qk[f'q_{i}'] = qk_cache[f"model.esm.encoder.layer.{i}.attention.self.query"].output.detach().cpu()
    clean_qk[f'k_{i}'] = qk_cache[f"model.esm.encoder.layer.{i}.attention.self.key"].output.detach().cpu()
# %%

# =============================================================================
# FULL PATH PATCHING: Corrected Pass C + Pass D (Metric-Level Validation)
# =============================================================================

# Step 0: Cache clean context vectors for proper freezing
# (context = attn_probs @ V, before W_O projection)
print("Caching clean context vectors for freezing...")
clean_ctx_LBLD = []
with model.trace() as tracer:
    with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
        ctx_cache = tracer.cache(
            modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
        )
for i in range(NUM_LAYERS):
    key = f"model.esm.encoder.layer.{i}.attention.self"
    clean_ctx_LBLD.append(ctx_cache[key].output[0].detach().cpu())
print(f"  Cached {len(clean_ctx_LBLD)} context vectors, shape {clean_ctx_LBLD[0].shape}")


# Step 1: Corrected Pass C
# - Source head: corrupt attention @ clean V (residual stream is clean at source layer)
# - All other heads: frozen to clean context (NOT recomputed with current V)
# - MLPs: recompute freely (they CAN relay the source head's signal)
# Result: downstream Q/K changes reflect ONLY direct path through residual stream + MLPs

def path_patching_pass_c_v2(
    model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL,
    clean_ctx_LBLD, source_layer, source_head, device,
):
    """
    Corrected IOI-style Pass C.
    
    Key difference from v1: non-source layers freeze the FULL context vector
    to clean values, not just attention patterns. This prevents V-mediated
    relay of the source head's signal through other attention heads.
    """
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            # Cache Q/K BEFORE interventions (nnsight hook ordering)
            cache_modules = []
            for i in range(source_layer + 1, NUM_LAYERS):
                cache_modules.append(model.esm.encoder.layer[i].attention.self.query)
                cache_modules.append(model.esm.encoder.layer[i].attention.self.key)
            downstream_cache = tracer.cache(modules=cache_modules)

            # Freeze/patch every layer
            for l in range(NUM_LAYERS):
                if l == source_layer:
                    # Source layer: corrupt attention for source head, clean for rest
                    # V is from clean residual stream (nothing upstream has changed)
                    v_raw = model.esm.encoder.layer[l].attention.self.value.output
                    v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                    frozen_attn = clean_attn_LBHLL[l].to(device).clone()
                    frozen_attn[:, source_head] = corrupt_attn_LBHLL[l][:, source_head].to(device)

                    new_ctx = torch.matmul(frozen_attn, v_heads)
                    new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)
                    model.esm.encoder.layer[l].attention.self.output[0][:] = new_ctx
                else:
                    # CORRECTED: freeze FULL context to clean value
                    # (v1 froze attention patterns but recomputed V — that leaks signal)
                    model.esm.encoder.layer[l].attention.self.output[0][:] = clean_ctx_LBLD[l].to(device)

    results = {}
    for i in range(source_layer + 1, NUM_LAYERS):
        q_key = f"model.esm.encoder.layer.{i}.attention.self.query"
        k_key = f"model.esm.encoder.layer.{i}.attention.self.key"
        results[f'q_{i}'] = downstream_cache[q_key].output.detach().cpu()
        results[f'k_{i}'] = downstream_cache[k_key].output.detach().cpu()

    return results


# Step 2: Run corrected Pass C for all source heads, collect edge magnitudes
print(f"\nRunning corrected Pass C for {len(ie_circuit_heads)} source heads...")

pass_c_results = {}  # (sl, sh) -> {q_{dl}: tensor, k_{dl}: tensor}
edge_magnitudes = [] # [(sl, sh, dl, dh, channel, magnitude, pass_c_qk), ...]

for src_idx, (sl, sh) in enumerate(ie_circuit_heads):
    results = path_patching_pass_c_v2(
        model, clean_inputs_BL, clean_attn_LBHLL, corrupt_attn_LBHLL,
        clean_ctx_LBLD, sl, sh, device
    )
    pass_c_results[(sl, sh)] = results

    for dl, dh in ie_circuit_heads:
        if dl <= sl:
            continue

        # Q change
        patched_q = results[f'q_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
        clean_q = clean_qk[f'q_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
        q_diff_norm = (patched_q - clean_q).squeeze(0).norm(dim=-1).sum().item()

        # K change
        patched_k = results[f'k_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
        clean_k = clean_qk[f'k_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
        k_diff_norm = (patched_k - clean_k).squeeze(0).norm(dim=-1).sum().item()

        if q_diff_norm > 0.5:
            edge_magnitudes.append((sl, sh, dl, dh, 'q', q_diff_norm, results[f'q_{dl}']))
        if k_diff_norm > 0.5:
            edge_magnitudes.append((sl, sh, dl, dh, 'k', k_diff_norm, results[f'k_{dl}']))

    if (src_idx + 1) % 10 == 0:
        print(f"  Processed {src_idx + 1}/{len(ie_circuit_heads)} source heads")

# Sort by magnitude and take top N for Pass D
edge_magnitudes.sort(key=lambda x: x[5], reverse=True)
TOP_N = 100  # adjust based on patience — each needs 1 forward pass
edges_for_pass_d = edge_magnitudes[:TOP_N]

print(f"\nPass C found {len(edge_magnitudes)} edges above threshold")
print(f"Running Pass D on top {TOP_N} edges...")


# Step 3: Pass D — patch only receiver head's Q or K, measure metric
def path_patching_pass_d(
    model, clean_inputs_BL,
    patched_qk_BLD,       # full Q or K tensor from Pass C (B, L, hidden_dim)
    dest_layer, dest_head,
    channel,               # 'q' or 'k'
    orig_contacts_AA, segment,
    clean_metric, corrupt_metric,
    device,
):
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            # CACHE FIRST — before any interventions
            attn_cache_d = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
            )

            # THEN intervene
            if channel == 'q':
                module = model.esm.encoder.layer[dest_layer].attention.self.query
            else:
                module = model.esm.encoder.layer[dest_layer].attention.self.key

            current = module.output
            patched = current.clone()
            start = dest_head * HEAD_DIM
            end = (dest_head + 1) * HEAD_DIM
            patched[:, :, start:end] = patched_qk_BLD[:, :, start:end].to(device)
            module.output = patched

    attn_list = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_list.append(attn_cache_d[key].output[1].detach().cpu())

    contacts = compute_contacts_from_attention(
        attn_list, clean_inputs_BL['input_ids'],
        clean_inputs_BL['attention_mask'],
        esm_model.esm.contact_head, device
    )[0].detach().cpu()

    metric = patching_metric(contacts, orig_contacts_AA, segment)

    if abs(clean_metric - corrupt_metric) > 1e-6:
        effect = (clean_metric - metric) / (clean_metric - corrupt_metric)
    else:
        effect = 0.0

    return metric, effect


# Step 4: Run Pass D for top edges
pass_d_results = []

for i, (sl, sh, dl, dh, channel, magnitude, pass_c_qk) in enumerate(edges_for_pass_d):
    metric, effect = path_patching_pass_d(
        model, clean_inputs_BL,
        pass_c_qk, dl, dh, channel,
        orig_contacts_AA, segment,
        clean_metric, corrupt_metric,
        device,
    )
    pass_d_results.append({
        'source': (sl, sh),
        'dest': (dl, dh),
        'channel': channel,
        'pass_c_magnitude': magnitude,
        'pass_d_metric': metric,
        'pass_d_effect': effect,
    })

    if (i + 1) % 20 == 0:
        print(f"  Pass D: {i + 1}/{len(edges_for_pass_d)}")

print("Done!")


# Step 5: Report results
print(f"\n{'='*80}")
print(f"PATH PATCHING RESULTS: Pass C magnitude vs Pass D causal effect")
print(f"{'='*80}")

# Sort by |Pass D effect|
pass_d_results.sort(key=lambda x: abs(x['pass_d_effect']), reverse=True)

print(f"\nTop 30 edges by |Pass D effect| (causal metric change):")
print(f"{'Source':>10} → {'Dest':>10} {'Ch':>3}  {'PassC mag':>10} {'PassD effect':>12} {'Metric':>8}")
print("-" * 70)
for r in pass_d_results[:30]:
    sl, sh = r['source']
    dl, dh = r['dest']
    print(f"L{sl:2d}H{sh:2d} → L{dl:2d}H{dh:2d}  {r['channel']:>3}"
          f"  {r['pass_c_magnitude']:>10.2f} {r['pass_d_effect']:>12.4f} {r['pass_d_metric']:>8.4f}")

# Correlation between Pass C magnitude and Pass D effect
magnitudes = torch.tensor([r['pass_c_magnitude'] for r in pass_d_results])
effects = torch.tensor([abs(r['pass_d_effect']) for r in pass_d_results])
correlation = torch.corrcoef(torch.stack([magnitudes, effects]))[0, 1].item()
print(f"\nCorrelation (Pass C magnitude vs |Pass D effect|): {correlation:.4f}")
print(f"  If high (>0.5): Pass C magnitudes are meaningful, not just scale artifacts")
print(f"  If low (<0.3): Pass C magnitudes are unreliable, Pass D is essential")

# Which source heads have the most causal edges?
from collections import Counter
source_counts = Counter()
for r in pass_d_results:
    if abs(r['pass_d_effect']) > 0.01:  # threshold for "meaningful" edge
        source_counts[r['source']] += 1

print(f"\nSource heads with most causally significant edges (|effect| > 0.01):")
for (sl, sh), count in source_counts.most_common(10):
    print(f"  L{sl:2d}H{sh:2d}: {count} significant edges")

# Save results
torch.save({
    'pass_d_results': pass_d_results,
    'edge_magnitudes': [(sl, sh, dl, dh, ch, mag) for sl, sh, dl, dh, ch, mag, _ in edge_magnitudes],
    'clean_metric': clean_metric,
    'corrupt_metric': corrupt_metric,
}, f'reports/outputs/{protein}_path_patching_full.pt')
print(f"\nSaved to reports/outputs/{protein}_path_patching_full.pt")
# %%

# =============================================================================
# Run Pass D on ALL edges with checkpointing
# =============================================================================
import time

TOP_N = len(edge_magnitudes)  # ALL of them
edges_for_pass_d = edge_magnitudes[:TOP_N]
print(f"Running Pass D on ALL {TOP_N} edges...")

pass_d_results = []
start_time = time.time()

for i, (sl, sh, dl, dh, channel, magnitude, pass_c_qk) in enumerate(edges_for_pass_d):
    metric, effect = path_patching_pass_d(
        model, clean_inputs_BL,
        pass_c_qk, dl, dh, channel,
        orig_contacts_AA, segment,
        clean_metric, corrupt_metric,
        device,
    )
    pass_d_results.append({
        'source': (sl, sh),
        'dest': (dl, dh),
        'channel': channel,
        'pass_c_magnitude': magnitude,
        'pass_d_metric': metric,
        'pass_d_effect': effect,
    })

    if (i + 1) % 50 == 0:
        elapsed = time.time() - start_time
        rate = (i + 1) / elapsed
        remaining = (TOP_N - i - 1) / rate
        print(f"  {i+1}/{TOP_N} | {elapsed:.0f}s elapsed | ~{remaining:.0f}s remaining")

    # Checkpoint every 500
    if (i + 1) % 500 == 0:
        torch.save({
            'pass_d_results': pass_d_results,
            'clean_metric': clean_metric,
            'corrupt_metric': corrupt_metric,
            'n_completed': i + 1,
            'n_total': TOP_N,
        }, f'reports/outputs/{protein}_path_patching_checkpoint.pt')
        print(f"    Checkpoint saved ({i+1} edges)")

elapsed = time.time() - start_time
print(f"\nDone! {TOP_N} edges in {elapsed:.0f}s ({elapsed/TOP_N:.2f}s/edge)")

# Final save
torch.save({
    'pass_d_results': pass_d_results,
    'edge_magnitudes': [(sl, sh, dl, dh, ch, mag) for sl, sh, dl, dh, ch, mag, _ in edge_magnitudes],
    'clean_metric': clean_metric,
    'corrupt_metric': corrupt_metric,
}, f'reports/outputs/{protein}_path_patching_full.pt')
print(f"Saved to reports/outputs/{protein}_path_patching_full.pt")

# =============================================================================
# Quick summary
# =============================================================================
pass_d_results.sort(key=lambda x: abs(x['pass_d_effect']), reverse=True)

print(f"\nTop 30 edges by |Pass D effect|:")
print(f"{'Source':>10} → {'Dest':>10} {'Ch':>3}  {'PassC mag':>10} {'PassD effect':>12}")
print("-" * 60)
for r in pass_d_results[:30]:
    sl, sh = r['source']
    dl, dh = r['dest']
    print(f"L{sl:2d}H{sh:2d} → L{dl:2d}H{dh:2d}  {r['channel']:>3}"
          f"  {r['pass_c_magnitude']:>10.2f} {r['pass_d_effect']:>12.4f}")

magnitudes = torch.tensor([r['pass_c_magnitude'] for r in pass_d_results])
effects = torch.tensor([abs(r['pass_d_effect']) for r in pass_d_results])
correlation = torch.corrcoef(torch.stack([magnitudes, effects]))[0, 1].item()
print(f"\nCorrelation (Pass C mag vs |Pass D effect|): {correlation:.4f}")

# %%

# =============================================================================
# SUFFICIENCY TEST: Using proper nnsight forward pass (from working IE code)
# =============================================================================
print(f"\n{'='*60}")
print("SUFFICIENCY TEST")
print(f"{'='*60}")

sorted_results = sorted(pass_d_results, key=lambda x: abs(x['pass_d_effect']), reverse=True)

thresholds = [10, 20, 30, 50, 75, 100, 150, 200, 300, 500, len(sorted_results)]
sufficiency_results = []

for k in thresholds:
    top_edges = sorted_results[:k]
    
    # Collect unique heads (both source and dest)
    circuit_heads = set()
    for r in top_edges:
        sl, sh = r['source']
        dl, dh = r['dest']
        circuit_heads.add((int(sl), int(sh)))
        circuit_heads.add((int(dl), int(dh)))
    
    # Proper forward pass: keep circuit heads clean, patch rest to corrupt
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
            )

            for layer_idx in range(NUM_LAYERS):
                heads_to_patch = [h for h in range(NUM_HEADS) if (layer_idx, h) not in circuit_heads]
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
        # for h in range(NUM_HEADS):
        #     if (i, h) not in circuit_heads:
        #         layer_attn[:, h] = corrupt_attn_LBHLL[i][:, h]
        heads_patched = [h for h in range(NUM_HEADS) if (i, h) not in circuit_heads]
        for h in heads_patched:
            layer_attn[:, h, :, :] = corrupt_attn_LBHLL[i][:, h, :, :]
        attn_list.append(layer_attn)

    contacts = compute_contacts_from_attention(
        attn_list, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()

    metric = patching_metric(contacts, orig_contacts_AA, segment)
    faithfulness = (metric - corrupt_metric) / (clean_metric - corrupt_metric) if abs(clean_metric - corrupt_metric) > 1e-6 else 0.0

    sufficiency_results.append({
        'k': k, 'n_heads': len(circuit_heads),
        'metric': metric, 'faithfulness': faithfulness,
    })
    print(f"  Top {k:4d} edges → {len(circuit_heads):3d} heads → "
          f"metric={metric:.4f}, faithfulness={faithfulness:.2%}")

print(f"\nBaselines:")
print(f"  Clean: {clean_metric:.4f}, Corrupt: {corrupt_metric:.4f}")
print(f"  IE circuit (45 heads): 70% faithfulness")

print(f"\nPath patching circuit:")
for r in sufficiency_results:
    if r['faithfulness'] >= 0.70:
        print(f"  → 70% faithfulness at top {r['k']} edges = {r['n_heads']} heads")
        break

# Save everything
torch.save({
    'pass_d_results': pass_d_results,
    'sufficiency_results': sufficiency_results,
    'edge_magnitudes': [(sl, sh, dl, dh, ch, mag) for sl, sh, dl, dh, ch, mag, _ in edge_magnitudes],
    'clean_metric': clean_metric,
    'corrupt_metric': corrupt_metric,
    'ie_circuit_heads': ie_circuit_heads,
}, f'reports/outputs/{protein}_path_patching_full.pt')
print(f"\nAll results saved to reports/outputs/{protein}_path_patching_full.pt")
# %%
# Debug: check what's in circuit_heads at k=1898
top_edges = sorted_results[:1898]
circuit_heads = set()
for r in top_edges:
    circuit_heads.add(r['source'])
    circuit_heads.add(r['dest'])

print(f"Number of circuit heads: {len(circuit_heads)}")
print(f"First 5: {list(circuit_heads)[:5]}")
print(f"Types: source={type(list(circuit_heads)[0][0])}, {type(list(circuit_heads)[0][1])}")

# Check: does (10, 9) match what's in the set?
test_head = list(circuit_heads)[0]
sl, sh = test_head
print(f"\nTest head: {test_head}")
print(f"(int(sl), int(sh)) in circuit_heads: {(int(sl), int(sh)) in circuit_heads}")
print(f"(sl, sh) in circuit_heads: {(sl, sh) in circuit_heads}")

# Sanity: does the OLD code still work?
print(f"\nSanity check with old ie_circuit_heads:")
print(f"ie_circuit_heads[:3] = {ie_circuit_heads[:3]}")
print(f"Types: {type(ie_circuit_heads[0][0])}")
# %%
# For each validated edge from Pass D, extract position-level signal
# No forward passes — just index into saved Pass C results

significant_edges = [r for r in pass_d_results if abs(r['pass_d_effect']) > 0.005]
print(f"Extracting token-level info for {len(significant_edges)} significant edges")

token_level_edges = []
for r in significant_edges:
    sl, sh = int(r['source'][0]), int(r['source'][1])
    dl, dh = int(r['dest'][0]), int(r['dest'][1])
    ch = r['channel']
    
    # Rebuild with int keys
    pass_c_int = {(int(k[0]), int(k[1])): v for k, v in pass_c_results.items()}

    # Then use:
    pc = pass_c_int[(sl, sh)]
    
    if ch == 'q':
        patched = pc[f'q_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
        clean = clean_qk[f'q_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
    else:
        patched = pc[f'k_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
        clean = clean_qk[f'k_{dl}'].reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, dh]
    
    diff_by_pos = (patched - clean).squeeze(0).norm(dim=-1)  # (L,)
    
    token_level_edges.append({
        'source': (sl, sh),
        'dest': (dl, dh),
        'channel': ch,
        'pass_d_effect': r['pass_d_effect'],
        'pos_signal': diff_by_pos,  # (L,) — THE figure data
    })

# Save before GPU dies
torch.save(token_level_edges, f'reports/outputs/{protein}_token_level_edges.pt')
# %%

token_level_edges[0]['pos_signal'].argmax().item()

# %%

torch.save({
    'token_level_edges': token_level_edges,
    'pass_d_results': pass_d_results,
    'sufficiency_results': sufficiency_results,
    'pass_c_results': {(int(k[0]), int(k[1])): v for k, v in pass_c_results.items()},
    'clean_qk': clean_qk,
    'clean_metric': clean_metric,
    'corrupt_metric': corrupt_metric,
    'ie_circuit_heads': [(int(l), int(h)) for l, h in ie_circuit_heads],
}, f'reports/outputs/{protein}_path_patching_complete.pt')
print("Saved!")
# %%
