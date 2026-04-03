# Anchor Feature Regression Analysis (experiments/3_25_anchor_regression.md)

## Context

From previous experiments we know:
- L10H9 has a fixed search direction in residual stream space (cosine 0.93 across
  proteins) that selects the anchor position as rank #1 in every protein tested.
- The anchor feature is built contextually in layers 7–9 (not from embedding/AA identity).
- SAE latent 3539 (layer 8) fires differentially at anchor positions across all 5 proteins
  but has 100% activation frequency — it's a continuous feature, not binary.
- SAE latent 52 fires at 4/5 anchor positions with sparser activation pattern.

**The question:** Can we explain what the search direction detects using known biological
and structural properties? What fraction of the variance in projection scores is
attributable to interpretable features?

## Previous experiments (reference these for code patterns)

- `scripts/anchor_interp_v2.py` — has `capture_post_ln_residuals()` for getting residual
  streams, `load_model()`, `load_configs()`, `extract_head_weights()`, and the search
  direction computation (`q1_mean_query_direction()`).
- `scripts/anchor_interp_v3.py` — has the layer-wise decomposition and SAE alignment.
  Contains the search direction computation and masked sequence construction.
  **Reuse the search direction from this script** (the `search_dir` vector for L10H9,
  computed from 2B61A or averaged across proteins — check what v3 used and be consistent).
- `scripts/anchor_decomp.py` — has model loading and weight extraction patterns.

## Data available

- Sequences: `data/full_seq_dict.json`
- SSE assignments: `data/ss_dict.json` — per-residue SSE labels (H/E/C)
- Protein configs: `configs/proteins.json` — contact pairs, flanks
- Conservation scores: available in the EVcouplings output directories. Check
  `scripts/anchor_interp.py` or the anchor interpretation pipeline for how conservation
  was loaded previously. Each protein should have per-residue conservation scores.
- Relative solvent accessibility (rel_acc): check if available in the anchor
  interpretation CSV files (`reports/outputs/{protein}/{protein}_anchor_interp.csv`).
  These were computed for the anchor residue tables earlier.
- Anchor positions for L10H9 (0-indexed):
  - 1BRTA: 220 (L), contact pair (119, 221)
  - 1PVGA: 101 (V), contact pair (101, 202)
  - 2B61A: 315 (T), contact pair (182, 316)
  - 2DPMA: 39 (F), contact pair (59, 172)
  - 2PKEA: 131 (L), contact pair (16, 131)

## Target

**L10H9** only. Use the same search direction as experiments v2/v3.

## Method

### Step 1: Compute projection scores for all positions

For each of the 5 proteins, run a forward pass on the **full unmasked sequence** (not
masked — we want to characterize the feature across all residues, and the full sequence
is where we have biological annotations for every position).

**Also run on the clean masked sequence** for comparison — the anchor is rank #1 there,
and we want to check if the regression features explain *why*.

For each protein and each residue position j (excluding BOS/EOS):
```python
# x_ln_j: post-LayerNorm residual at layer 10, position j
# search_dir: the L10H9 search direction (1280-dim, unit normalized)
projection_score_j = dot(x_ln_j, search_dir)
```

This gives ~1500 data points across 5 proteins (full sequence) with continuous scores.

### Step 2: Annotate each position with biological features

For each residue position j, collect:

1. **Amino acid identity** — 20-dimensional one-hot (from the sequence)
2. **SSE label** — from `ss_dict.json`. Encode as: H=helix, E=strand, C=coil.
   Use one-hot encoding (3 features, or 2 with coil as reference).
3. **Conservation score** — continuous, from EVcouplings alignment data.
   Load the same way as in the anchor interpretation experiments.
4. **Relative solvent accessibility** — continuous, if available in the data.
   Check `_anchor_interp.csv` files or compute from PDB structures if accessible.
   If not available for all positions, skip this feature and note it.
5. **Position within SSE** — compute for each residue:
   - `seg_len`: length of the SSE segment it belongs to
   - `dist_to_boundary`: distance to nearest SSE boundary (0 = boundary, higher = more
     interior). Compute from the SSE string by finding runs of same label.
   - `is_boundary`: binary, 1 if within 1 residue of an SSE boundary
6. **SSE segment length** — length of the contiguous SSE segment the residue is in
7. **Distance to contact segments** — for each residue, compute:
   - `dist_to_ss1`: absolute sequence distance to nearest residue in SS1
   - `dist_to_ss2`: absolute sequence distance to nearest residue in SS2
   - `in_analysis_window`: binary, 1 if within the unmasked region of the clean sequence
8. **Protein identity** — categorical (5 levels), to capture protein-level effects

### Step 3: Exploratory visualization (do this BEFORE regression)

Before fitting any model, generate these plots:

**Plot A: Projection scores by SSE type (box/violin plot)**
- x-axis: SSE label (H, E, C)
- y-axis: projection score
- One panel per protein, plus a combined panel
- The corrected SVD data showed strand > helix > coil for L10H9 — verify this holds
  for full projection scores.

**Plot B: Projection score vs. conservation (scatter)**
- x-axis: conservation score
- y-axis: projection score
- Color by SSE type
- One panel per protein

**Plot C: Projection score vs. position within SSE (scatter)**
- x-axis: distance to nearest SSE boundary
- y-axis: projection score
- Color by SSE type

**Plot D: Projection score along sequence (line plot)**
- x-axis: residue position
- y-axis: projection score
- Color the background by SSE assignment
- Mark the anchor position, SS1, SS2 regions
- One plot per protein — this is the most informative single visualization

### Step 4: Regression analysis

**Model 1: SSE-only model**
```python
# Features: SSE one-hot (E, H — C as reference)
# Target: projection_score
# Include protein fixed effects
model_sse = OLS(projection_score ~ SSE_E + SSE_H + protein_dummies)
```

**Model 2: SSE + position features**
```python
# Add: dist_to_boundary, seg_len, is_boundary
model_pos = OLS(projection_score ~ SSE_E + SSE_H + dist_to_boundary + seg_len
                + is_boundary + protein_dummies)
```

**Model 3: Full biological model**
```python
# Add: conservation, rel_acc (if available), AA identity
model_full = OLS(projection_score ~ SSE_E + SSE_H + dist_to_boundary + seg_len
                 + is_boundary + conservation + AA_dummies + protein_dummies)
```

**Model 4: Distance-to-contact model**
```python
# Add: dist_to_ss1, dist_to_ss2, in_analysis_window
# This tests whether the feature is related to proximity to the contact site
model_dist = OLS(projection_score ~ SSE_E + SSE_H + dist_to_boundary + seg_len
                 + conservation + dist_to_ss1 + dist_to_ss2 + in_analysis_window
                 + protein_dummies)
```

For each model, report:
- R² (adjusted)
- Coefficients with standard errors and p-values for each feature
- Residual analysis: is the anchor position a positive outlier? (residual > 2 std)

**Key interpretive questions:**
- If R² > 0.5: the feature is largely explainable by known biology. Report the top
  features by coefficient magnitude. This is the punchline.
- If R² = 0.2–0.5: partial explanation. Report what's explained and what's not.
- If R² < 0.2: the feature is mostly model-internal. Report this honestly.
- Is the anchor position well-predicted by the model, or is it an outlier even after
  accounting for all features? If outlier: the model has learned something beyond
  standard annotations.

### Step 5: Anchor-specific analysis

After the regression, examine the anchor positions specifically:
- What are the predicted vs. actual projection scores at anchor positions?
- What is the residual at anchor positions? (actual - predicted)
- If the regression explains most of the variance but the anchor has a large positive
  residual, there's an additional anchor-specific signal beyond the features.
- If the regression explains the anchor position well (small residual), then the
  combination of features in the model IS the anchor feature.

### Step 6: Cross-reference with SAE latents 3539 and 52

For each position, also record the activation of SAE latents 3539 and 52 (from the
layer 8 SAE, if you can run the encoder — or from cached activations if available).
- Compute correlation between projection_score and latent_3539_activation
- Compute correlation between projection_score and latent_52_activation
- Add these as features in a final regression model — do they explain variance
  beyond the biological features?

This directly connects the SAE and regression analyses.

## Output

- Plots A–D saved to `reports/outputs/multi_protein/anchor_regression_*.png`
- Regression tables saved to `reports/outputs/multi_protein/anchor_regression.md`
- Summary table of R² across models
- Per-protein anchor residual analysis

## Execution

```bash
uv run python scripts/anchor_regression.py --device cuda
```

Create `scripts/anchor_regression.py`. Reuse model/data loading from
`scripts/anchor_interp_v3.py`. Use statsmodels or sklearn for regression.

Dependencies: `pip install statsmodels` (or use sklearn's LinearRegression).

Estimated runtime: ~10 min (forward passes for 5 proteins, plus regression which is
instant).

## Verification

1. Sanity check: the projection score at the anchor position should be the highest or
   near-highest for each protein (we already know this from Q1 analysis).
2. The SSE coefficient for strand (E) should be positive relative to coil (C), based
   on the SVD analysis showing strand > coil for L10H9.
3. R² should increase monotonically from Model 1 → Model 4 (more features = more
   explained variance, at minimum).
4. If conservation was not significant in the earlier anchor-level analysis, it should
   also have a small coefficient here (consistency check).