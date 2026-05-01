---
title: "Experiment Spec: Downstream Attention Corruption + K-Only Intervention"
date: 2026-04-18
status: spec
---

# Experiment: Diagnosing Why Contact Prediction Survives Anchor Suppression

## Background

In `anchor_contact_steering.py`, suppressing the L10H9 anchor direction at the layer-10 LayerNorm output destroys the anchor attention pattern by alpha=2, but contact prediction (P@L/5) is unaffected until alpha=8-10. We need to understand why.

The intervention modifies the LayerNorm output at anchor positions, which feeds Q, K, AND V projections simultaneously. This means at high alpha, the perturbation propagates through the residual stream to all downstream layers (11-32), whose attention also feeds the contact head.

## Experiment 1: Downstream Attention Corruption Tracking

### Goal

Measure how attention patterns in ALL 33 layers change as a function of steering alpha. If the contact degradation at alpha=8+ is driven by downstream corruption (not L10H9 pattern loss), we should see downstream layers' attention start diverging around alpha=8-10.

### Implementation

Base the script on `anchor_contact_steering.py`. Reuse `cache_attention_with_steering`, `compute_search_dir`, `identify_anchors`, `load_model`, and all the PDB/contact utilities from that file (import or copy them).

For each protein and each alpha:
1. Run `cache_attention_with_steering` with alpha=0 (clean) and alpha=alpha (steered). Both return `attn_LBHLL` (list of 33 tensors, each shape `(1, 20, L, L)`).
2. For each layer `l` in 0..32 and each head `h` in 0..19, compute the Jensen-Shannon divergence between clean and steered attention distributions:
   - For each query position `q` (excluding BOS/EOS), compute `JSD(clean_attn[l][0, h, q, :], steered_attn[l][0, h, q, :])`.
   - Average across query positions to get `jsd[l, h]`.
3. Also compute a simpler metric: cosine similarity between the flattened attention matrices `clean_attn[l][0, h, 1:-1, 1:-1]` and `steered_attn[l][0, h, 1:-1, 1:-1]` (flatten to 1D, compute cosine sim).

### Output

A CSV with columns: `protein, alpha, layer, head, mean_jsd, cosine_sim`.

Summary plots:
1. Heatmap: layer (y) x alpha (x), color = mean JSD averaged across heads and proteins. This shows which layers are most affected at each alpha.
2. Line plot: for each alpha, plot mean JSD as a function of layer, averaged across heads and proteins. Expect layers 0-9 to be flat (not affected by downstream intervention), layer 10 to jump, and layers 11+ to show increasing divergence at high alpha.
3. Overlay the contact P@L/5 curve (from existing results) on a twin y-axis to visually check if downstream corruption onset matches contact degradation onset.

### Parameters

- Same 20 proteins as the existing `contact_steering/direct_top3` run.
- Same alphas: `[0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 10.0, 12.0, 14.0, 16.0, 32.0]`.
- Direct steering mode, top-3 anchors (matching the canonical run).
- Use the same search direction from 2B61A.

### Key files to reference

- `scripts/anchor_contact_steering.py` lines 212-267: `cache_attention_with_steering` (reuse directly)
- `scripts/anchor_contact_steering.py` lines 88-101: `compute_search_dir` (reuse directly)
- `scripts/anchor_contact_steering.py` lines 115-127: `identify_anchors` (reuse directly)
- `scripts/anchor_contact_steering.py` lines 50: `ALPHAS` list
- Contact P@L/5 results for overlay: `reports/out2/suppressing_anchors/contact_steering/direct_top3/anchor_contact_steering_results.csv`

### Output location

`reports/out2/suppressing_anchors/downstream_corruption/`

---

## Experiment 2: K-Only vs Q-Only vs V-Only Intervention

### Goal

Disentangle which projection pathway causes the contact degradation. Currently the intervention modifies the LN output feeding all three projections. By intervening on individual projections, we can determine:
- Does suppressing only K (destroying the attention pattern) affect contacts?
- Does suppressing only V (corrupting the value readout) affect contacts?
- Does suppressing only Q (changing what the anchor attends to) affect contacts?

### Implementation

Modify the intervention to target individual projections instead of the shared LN output. The cleanest way is to intervene AFTER the QKV projection, at the head level.

In ESM2, the attention weights for L10H9 are:
- `W_Q`: `model.esm.encoder.layer[10].attention.self.query.weight` (rows `9*64 : 10*64`)
- `W_K`: `model.esm.encoder.layer[10].attention.self.key.weight` (rows `9*64 : 10*64`)
- `W_V`: `model.esm.encoder.layer[10].attention.self.value.weight` (rows `9*64 : 10*64`)

For "K-only" intervention, you need to modify the key vector at the anchor position for head 9 only. The search direction `d` is in the 1280-dim LN output space. Its effect on the key is `W_K_hd @ d` (64-dim). So:

```python
# K-only: modify key projection output at anchor positions
key_module = model.esm.encoder.layer[10].attention.self.key
key_out = key_module.output  # shape (B, L, 1280) = all heads concatenated
# Extract head 9 slice
h_start, h_end = TARGET_HEAD * HEAD_DIM, (TARGET_HEAD + 1) * HEAD_DIM
for pos in anchor_positions:
    tok_idx = pos + 1
    k_j = key_out[:, tok_idx, h_start:h_end]  # (B, 64)
    # Project d into key space
    d_key = (weights["W_K_hd"] @ d_unit)  # (64,)
    d_key_unit = d_key / d_key.norm().clamp(min=1e-8)
    if steering_mode == "projection":
        proj = (k_j @ d_key_unit).unsqueeze(-1) * d_key_unit
        key_out[:, tok_idx, h_start:h_end] = k_j - alpha * proj
    elif steering_mode == "direct":
        key_out[:, tok_idx, h_start:h_end] = k_j - alpha * d_key_unit
key_module.output = key_out
```

Similarly for Q-only (use `d_query = W_Q_hd @ d_unit`) and V-only (use `d_value = W_V_hd @ d_unit`).

IMPORTANT: For the "direct" mode, the alpha scale needs recalibration because the head-space vectors (64-dim) have different norms than the 1280-dim LN-space vector. Use the same unit-normalized projected direction (as shown above with `d_key_unit`) so alpha has comparable meaning.

Also implement an "LN (all three)" condition that reproduces the existing experiment as a control.

### Output

For each condition (K-only, Q-only, V-only, LN-all), compute:
1. L10H9 attention metrics: anchor_mass, top3_mass, entropy_norm (same as existing)
2. Contact prediction: P@L/5, P@L/2, P@L (same as existing)
3. KL divergence on logits (same as existing)

CSV with columns: `protein, alpha, intervention_target, P_L5, P_L2, P_L, kl_div, l10h9_anchor_mass, l10h9_top3_mass, l10h9_entropy_norm`.

Summary plot: 4-panel figure (one per intervention target), each showing P@L/5 and anchor_mass vs alpha. This directly answers whether attention pattern death (via K-only) is sufficient to break contacts, or whether V corruption is the real driver.

### Parameters

- Same 20 proteins, same alphas, direct mode, top-3 anchors.
- Four conditions: `K-only`, `Q-only`, `V-only`, `LN-all` (control).

### Output location

`reports/out2/suppressing_anchors/qkv_decomposition/`

---

## Experiment 3: Attention Output Norm at Anchor Positions

### Goal

Even if L10H9's attention pattern changes, the attention OUTPUT (context vector = attn_probs @ V) at the anchor position flows through the residual stream. Measure how the norm and direction of this output changes with alpha.

### Implementation

For each protein and alpha:
1. During the steered trace, also cache the attention output: `model.esm.encoder.layer[10].attention.self.output[0]` (shape `(B, L, 1280)`, the context vectors before the output projection).

Actually, more precisely: cache the output of the full attention block `model.esm.encoder.layer[10].attention.output` (shape `(B, L, 1280)`, after output projection + dropout). This is what gets added to the residual stream.

2. For each anchor position, compute:
   - `norm_ratio = ||attn_out_steered[anchor]|| / ||attn_out_clean[anchor]||`
   - `cosine_sim = cos(attn_out_steered[anchor], attn_out_clean[anchor])`
3. Also compute these for non-anchor positions (averaged) to see if the perturbation is localized.

### Output

CSV: `protein, alpha, position_type (anchor/non_anchor), norm_ratio_mean, cosine_sim_mean`.

Plot: norm_ratio and cosine_sim vs alpha, with separate lines for anchor and non-anchor positions. If the attention output at anchor positions diverges sharply at alpha=2 while non-anchor positions stay clean until alpha=8, that explains the contact plateau.

### Parameters

Same 20 proteins, same alphas, direct mode, top-3 anchors.

### Output location

`reports/out2/suppressing_anchors/attn_output_tracking/`

---

## Implementation Notes

- All experiments should follow the existing pattern in `anchor_contact_steering.py`: argparse CLI, CSV checkpointing with resume, matplotlib plots saved as PNGs, summary JSON.
- Use `uv run python scripts/<script_name>.py --device cuda` to run.
- The model loading, search direction computation, anchor identification, and contact evaluation functions should be imported or copied from `anchor_contact_steering.py`.
- Run from `/work/pi_annagreen_umass_edu/jatin/plm_nnsight/`.
- Experiments 1 and 3 are lightweight additions to the existing forward pass. Experiment 2 requires a modified intervention but the same evaluation pipeline.
- Each experiment should be a separate script in `scripts/`.

## Priority

1. Experiment 1 (downstream corruption) is the most informative for the least effort. It reuses the existing intervention and just measures more stuff.
2. Experiment 2 (K/Q/V decomposition) is the cleanest mechanistic test. It directly answers whether attention pattern change vs value corruption drives contact loss.
3. Experiment 3 (attention output tracking) is supplementary and can be folded into Experiment 1 if convenient.
