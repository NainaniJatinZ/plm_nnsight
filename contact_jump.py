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

def plot_contact_map(contacts_AA: torch.Tensor, title: str):
    plt.figure(figsize=(6, 6))
    plt.imshow(contacts_AA, cmap='viridis', aspect='equal')
    plt.colorbar(label="Contact Probability")
    plt.title(title)
    plt.xlabel("Residue Index")
    plt.ylabel("Residue Index")
    plt.tight_layout()
    plt.show()

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
plot_contact_map(orig_contacts_AA, f"{protein} - Full Sequence")

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

# =============================================================================
# Manual Contact Prediction (to enable interventions)
# =============================================================================
# predict_contacts does its own forward pass, so interventions don't affect it.
# We manually collect attention from all layers and call contact_head directly.
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
# Attention Patching: Find Important Heads
# =============================================================================
# For each head, replace clean attention with corrupt attention and measure effect
# Normalized effect: (noised_metric - clean_metric) / (corrupt_metric - clean_metric)
# %%
print(f"\nRunning attention patching over {NUM_LAYERS} layers x {NUM_HEADS} heads...")

effects_LH = torch.zeros(NUM_LAYERS, NUM_HEADS)

for layer_idx in range(NUM_LAYERS):
    for head_idx in range(NUM_HEADS):
        # Create patched attention: replace one head with corrupt version
        patched_attn_LBHLL = []
        for l in range(NUM_LAYERS):
            if l == layer_idx:
                # Copy clean attention and replace this head with corrupt
                patched = clean_attn_LBHLL[l].clone()
                patched[:, head_idx, :, :] = corrupt_attn_LBHLL[l][:, head_idx, :, :]
                patched_attn_LBHLL.append(patched)
            else:
                patched_attn_LBHLL.append(clean_attn_LBHLL[l])

        # Compute contacts with patched attention
        patched_contacts_AA = compute_contacts_from_attention(
            patched_attn_LBHLL,
            clean_inputs_BL['input_ids'],
            clean_inputs_BL['attention_mask'],
            esm_model.esm.contact_head,
            device=device,
        )[0].detach().cpu()

        # Compute normalized effect
        patched_metric = patching_metric(patched_contacts_AA, orig_contacts_AA, segment)
        if abs(corrupt_metric - clean_metric) > 1e-6:
            effect = (patched_metric - clean_metric) / (corrupt_metric - clean_metric)
        else:
            effect = 0.0
        effects_LH[layer_idx, head_idx] = effect

    if (layer_idx + 1) % 5 == 0:
        print(f"  Processed layer {layer_idx + 1}/{NUM_LAYERS}")

print("Done!")

# %%
# Plot effect heatmap
plt.figure(figsize=(12, 8))
plt.imshow(effects_LH.numpy(), cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
plt.colorbar(label="Normalized Effect (0=clean, 1=corrupt)")
plt.xlabel("Head")
plt.ylabel("Layer")
plt.title(f"Attention Head Effects on Contact Prediction\n{protein}: flank {config['corrupt_flank']}→{config['clean_flank']}")
plt.tight_layout()
plt.show()

# %%
# Find top heads by absolute effect
effects_flat = effects_LH.flatten()
top_k = 6
top_indices = effects_flat.abs().argsort(descending=True)[:top_k]

print(f"\nTop {top_k} heads by absolute effect:")
top_heads = []
for idx in top_indices:
    layer = idx // NUM_HEADS
    head = idx % NUM_HEADS
    effect = effects_LH[layer, head].item()
    print(f"  Layer {layer:2d}, Head {head:2d}: effect = {effect:+.4f}")
    top_heads.append((layer.item(), head.item(), effect))

# %%
# Plot attention patterns for top heads (clean vs corrupt)
fig, axes = plt.subplots(top_k, 2, figsize=(12, 3 * top_k))

for i, (layer, head, effect) in enumerate(top_heads):
    # Clean attention
    ax_clean = axes[i, 0]
    clean_pattern_LL = clean_attn_LBHLL[layer][0, head].numpy()
    im = ax_clean.imshow(clean_pattern_LL, cmap='viridis', aspect='equal')
    ax_clean.set_title(f"L{layer}H{head} Clean (effect={effect:+.3f})")
    ax_clean.set_xlabel("Key")
    ax_clean.set_ylabel("Query")

    # Corrupt attention
    ax_corrupt = axes[i, 1]
    corrupt_pattern_LL = corrupt_attn_LBHLL[layer][0, head].numpy()
    ax_corrupt.imshow(corrupt_pattern_LL, cmap='viridis', aspect='equal')
    ax_corrupt.set_title(f"L{layer}H{head} Corrupt")
    ax_corrupt.set_xlabel("Key")
    ax_corrupt.set_ylabel("Query")

plt.suptitle(f"Top {top_k} Attention Heads: Clean vs Corrupt", y=1.02)
plt.tight_layout()
plt.show()

# =============================================================================
# Export Visualization Data
# =============================================================================
# %%
from export_viz_data import export_visualization_data

export_visualization_data(
    clean_attn_LBHLL=clean_attn_LBHLL,
    corrupt_attn_LBHLL=corrupt_attn_LBHLL,
    effects_LH=effects_LH,
    clean_contacts_AA=clean_contacts_AA,
    corrupt_contacts_AA=corrupt_contacts_AA,
    orig_contacts_AA=orig_contacts_AA,
    segment=segment,
    sequences={'full': sequence_S, 'clean': clean_seq_S, 'corrupt': corrupt_seq_S},
    protein=protein,
    config=config,
    output_path="reports/viz_data.json.gz"
)
print(f"✓ Exported visualization data to reports/viz_data.json.gz")

# %%

