# Flank Classification v4: H4+ with Cluster-Level Features

## Goal

Extend the H4 structural feature set with features that describe the **local structural cluster as a whole**, not just individual flank positions. Test whether "center of a dense buried structural cluster" is the right description of what d detects.

The v3 H4 used per-position features only (RSA, contacts_8A, contact-with-center, long-range fraction at each of 61 positions). These describe each position independently. But the GBT's large advantage over L1 (0.727 vs 0.488) suggests interactions between positions matter — e.g., "multiple flank positions are BOTH buried AND in 3D contact with center." Cluster-level features give L1 a chance to capture this without relying on nonlinear interactions.

---

## Protein set

Same 483 proteins with valid PDB features from v3. Use the same structural matching and same controls. This ensures direct comparison.

---

## Feature sets

### H4_base (baseline — same as v3 H4)
Per-position features for positions in [-30, +30]:
- RSA of position j
- contacts_8A count of position j
- binary: is position j in 3D contact (< 8A CB-CB) with center?
- long-range contact fraction of position j

4 features × 61 positions = **244 features**

This is the baseline to beat (AUPRC 0.488).

### H4+ (H4_base + cluster-level features)

All of H4_base, plus the following window-level summary features:

**Contact cluster summaries:**
1. `n_flank_contacting_center`: count of flank positions (j != center) in 3D contact with center. Directly measures "how many neighbors does the center have within ±30?"
2. `frac_flank_contacting_center`: same as above / total flank positions. Normalized version.
3. `mean_rsa_contacting`: mean RSA of flank positions that contact center. Tests: are the contacting neighbors also buried?
4. `mean_contacts_contacting`: mean contacts_8A of flank positions that contact center. Are the contacting neighbors themselves hubs?
5. `mean_lr_frac_contacting`: mean long-range fraction of flank positions that contact center.
6. `n_sse_segments_contacting`: number of distinct SSE segments (contiguous H/E/C stretches) that have at least one position in 3D contact with center. Measures structural diversity of the contact neighborhood.
7. `frac_cross_sse_contacts`: fraction of center's 3D contacts within the window that are in a DIFFERENT SSE segment than the center. Tests cross-SSE integration.

**Burial pattern summaries:**
8. `frac_buried_flank`: fraction of flank positions with RSA < 0.05. How buried is the neighborhood overall?
9. `frac_buried_left`: same for left half of flank (positions -30 to -1).
10. `frac_buried_right`: same for right half (+1 to +30).
11. `burial_asymmetry`: |frac_buried_left - frac_buried_right|. Is the buried neighborhood symmetric?

**Contact density within window:**
12. `contact_density_window`: number of 3D contact pairs (i,j) where both i and j are within the ±30 window, divided by total possible pairs. How dense is the structural neighborhood?
13. `mean_degree_window`: mean number of 3D contacts each window position has with OTHER window positions. Same idea, position-level.
14. `max_degree_window`: max of above. Is there a secondary hub within the flank?

**Spatial distribution of contacts:**
15. `contact_spread`: std of sequence positions (relative to center) of flank residues in 3D contact with center. Low = contacts are clustered nearby in sequence. High = contacts are scattered across the window.
16. `contact_span`: max minus min sequence position (relative to center) of flank residues in 3D contact with center.

**H5 helper features (positional context):**
17. `frac_pos`: anchor position / protein length
18. `dist_nterm`: distance to N-terminus (residues)
19. `dist_cterm`: distance to C-terminus
20. `pos_in_sse`: position within own SSE segment (0 = start, 1 = end)
21. `sse_seg_len`: length of the SSE the center sits in
22. `n_sse_transitions_window`: number of SSE transitions in the ±30 window
23. `n_sse_segments_window`: number of distinct SSE segments in the window

Total H4+: 244 (per-position) + 16 (cluster) + 7 (H5) = **267 features**

### H4_cluster_only (cluster + H5 features without per-position)
Just the 16 cluster features + 7 H5 features = **23 features**.

This tests whether the cluster description alone (without per-position detail) carries signal. If this performs well, the story is very clean: "anchors = centers of dense buried structural clusters."

---

## Models

### L1 logistic regression (primary)
Same settings as v3: `penalty="l1"`, `C=1.0`, `class_weight="balanced"`, LOPO.

### Gradient boosted trees (secondary, on H4+ and H4_cluster_only)
Same settings as v3: `n_estimators=200`, `max_depth=3`.

---

## Evaluation

Same as v3: LOPO with GroupKFold, AUPRC (primary), AUROC, balanced accuracy.
Permutation test on H4+ (100 shuffles).

---

## Main analyses

### Analysis 1: Feature set comparison

| Model | Features | Expected comparison |
|---|---|---|
| H4_base | 244 | Baseline: 0.488 AUPRC |
| H4+ | 267 | Does cluster context help L1? |
| H4_cluster_only | 23 | Is the cluster description alone enough? |
| H4+ (GBT) | 267 | How much nonlinear signal remains? |
| H4_cluster_only (GBT) | 23 | Cluster features + nonlinearity |

Key question: does H4+ close the gap between H4_base L1 (0.488) and H4_base GBT (0.727)?

### Analysis 2: Top features from H4+
L1 coefficients for the cluster-level features. Which ones have the largest weights?

Predictions:
- `n_flank_contacting_center` should be positive (more contacts = more likely anchor)
- `mean_rsa_contacting` should be negative (contacting neighbors are buried)
- `contact_density_window` should be positive (dense structural cluster)
- `n_sse_segments_contacting` should be positive (cross-SSE integration)

If these hold, the "local buried structural cluster" hypothesis is directly confirmed.

### Analysis 3: Top features from H4_cluster_only
Same analysis but with only 23 features. Much more interpretable. The ranking directly tells us which cluster properties matter most.

### Analysis 4: Feature ablation within H4+
Run H4+ with each cluster feature REMOVED one at a time. Which ones cause the biggest drop?

This is a leave-one-feature-family-out analysis:
- H4+ without contact-cluster features (1-7)
- H4+ without burial-pattern features (8-11)
- H4+ without contact-density features (12-14)
- H4+ without spatial-distribution features (15-16)
- H4+ without H5 features (17-23)

---

## Success criteria

### Strong success
H4+ L1 AUPRC > 0.55 (closing the gap toward GBT). Cluster features have large, interpretable L1 coefficients. H4_cluster_only alone > 0.30 AUPRC.

Interpretation: "local dense buried structural cluster" is a good description. The per-position features plus cluster summaries capture most of the signal.

### Moderate success
H4+ L1 modestly improves over H4_base (0.50-0.55). Cluster features help but don't close the GBT gap.

Interpretation: cluster description is part of the story but nonlinear feature interactions still matter.

### Weak result
H4+ ≈ H4_base (< 0.50). Cluster features don't add to per-position features.

Interpretation: the interaction signal GBT captures isn't "cluster density" in the way we formulated it. The nonlinearity is something else.

---

## Outputs

- `reports/outputs/multi_protein/anchor_local_flank_v4.md`
- `reports/outputs/multi_protein/anchor_local_flank_v4_metrics.csv`
- `reports/outputs/multi_protein/anchor_local_flank_v4_coefficients.csv`
- `reports/outputs/multi_protein/anchor_local_flank_v4_ablation.csv`

Plots:
1. `anchor_local_flank_v4_comparison.png` — bar chart: H4_base vs H4+ vs H4_cluster_only (L1 and GBT)
2. `anchor_local_flank_v4_cluster_features.png` — L1 coefficients for cluster features
3. `anchor_local_flank_v4_ablation.png` — feature-family ablation

---

## Reuse

- Entire v3 infrastructure: protein selection, control matching, LOPO classification, plotting
- PDB feature computation: extend existing per-residue features to compute pairwise contacts within window
- v3 H4 results as direct baseline

New code:
1. Compute pairwise 3D contacts within each ±30 window (need contact map for window positions)
2. Compute cluster-level summary features from per-position features + pairwise contacts
3. Feature ablation loop

---

## Script

Extend `scripts/anchor_local_flank_v3.py` or create `scripts/anchor_local_flank_v4.py`

```bash
uv run python scripts/anchor_local_flank_v4.py --device cpu
```

---

## Notes

- The 16 cluster features are deliberately designed to be INTERPRETABLE. Each one tests a specific aspect of the "local buried structural cluster" hypothesis.
- H4_cluster_only (23 features) is the key diagnostic model. If it works, we can say "anchorhood ≈ center of a dense buried structural cluster" in plain English. That's the paper's punchline.
- If GBT on H4_cluster_only >> L1 on H4_cluster_only, there are important nonlinear interactions even among the cluster features (e.g., "high contact density AND cross-SSE contacts" matters more than either alone).
