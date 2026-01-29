# Contact Jump Analysis

## Overview

This project investigates how ESM2's attention patterns contribute to contact prediction, specifically the "contact jump" phenomenon where a single residue change in flanking regions causes a dramatic shift in contact prediction accuracy.

## Key Learnings

### 1. Manual Contact Prediction Pipeline

ESM's `predict_contacts()` does its own forward pass internally, so interventions during nnsight tracing don't affect it. We must:

1. **Cache attention weights** from all 33 layers during a traced forward pass
2. **Stack and process** the attention manually
3. **Call `contact_head` directly** with our (possibly modified) attention

```python
# Cache attention from all layers
with model.trace() as tracer:
    with tracer.invoke(**inputs_with_attn_BL):
        attn_cache = tracer.cache(
            modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
        )

# Extract attention weights
attn_list_BHLL = []
for layer_idx in range(NUM_LAYERS):
    key = f"model.esm.encoder.layer.{layer_idx}.attention.self"
    attn_list_BHLL.append(attn_cache[key].output[1].detach())

# Compute contacts manually
contacts = compute_contacts_from_attention(attn_list_BHLL, tokens, mask, contact_head)
```

### 2. APC Constraint on Interventions

ESM's contact head uses **Average Product Correction (APC)**:
```python
apc = a.sum(dim=-2) * a.sum(dim=-1) / a.sum(dim=(-2, -1))  # Division here!
```

**Cannot use zeros** for ablation - causes division by zero → NaN.

**Solutions:**
- Use **uniform attention** (`1/seq_len`) to ablate a layer/head
- Use **attention from another sequence** (patching)
- Scale attention by small factor (e.g., `* 0.001`) rather than zeroing

### 3. Shape Suffixes Convention

| Suffix | Meaning |
|--------|---------|
| `B` | Batch size |
| `L` | Sequence length (including special tokens) |
| `A` | Amino acid positions (excluding special tokens) |
| `H` | Attention heads |
| `_S` | String |

Example: `attn_weights_BHLL` is shape `(batch, heads, seq_len, seq_len)`

### 4. Patching Metric

Measures how well predicted contacts match original contacts in the target segment:
```python
metric = (pred * orig).sum() / (orig * orig).sum()
```
- `1.0` = perfect match to original
- `0.0` = no overlap with original contacts

### 5. Contact Segment Definition

For a contact pair at positions (pos1, pos2), we define segments with a radius (default 5):
```python
ss1_start, ss1_end = pos1 - 5, pos1 + 6  # 11 residues around pos1
ss2_start, ss2_end = pos2 - 5, pos2 + 6  # 11 residues around pos2
```

## File Structure

- `contact_jump.py` - Main analysis notebook (# %% cell format)
- `data/full_seq_dict.json` - Protein sequences by PDB ID
- `helpers/` - Utility functions from plm_nnsight tutorial

## Protein Configurations

```python
PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}
```

The "jump" occurs when flank size changes by just 1 residue (e.g., 43→44 for 2B61A).

## Attention Patching Experiment

To identify which attention heads contribute to the contact jump:

1. **Cache attention** for clean (high metric) and corrupt (low metric) sequences
2. **For each head**: Replace clean attention with corrupt attention at that head
3. **Compute normalized effect**: `(patched_metric - clean_metric) / (corrupt_metric - clean_metric)`
   - Effect ≈ 0: Head doesn't matter
   - Effect ≈ 1: Head fully explains the gap
   - Effect < 0: Head has opposite effect

```python
# Patch one head
patched = clean_attn_LBHLL[layer].clone()
patched[:, head, :, :] = corrupt_attn_LBHLL[layer][:, head, :, :]
```

This reveals which layer/head combinations are responsible for the contact prediction change.
