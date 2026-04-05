# Flank Classification at Scale (v3)

## Goal

Determine whether anchorhood can be predicted from a local sequence/SSE/structural window around the residue, using structurally matched controls at scale. Hypothesis-driven feature design, one feature family per hypothesis.

---

## Hypotheses

**H1 (AA pattern):** There is a specific amino acid arrangement at particular relative positions in the flank that distinguishes anchors. E.g., "leucine at -5, proline at +7."

**H2 (SSE arrangement):** The secondary structure layout around the anchor (transitions, segment types) predicts anchorhood. E.g., "strand-loop-strand" junctions.

**H3 (physicochemical profile):** A gradient or pattern in physical properties (hydrophobicity, charge, volume) across the flank distinguishes anchors. Could include amphipathic periodicity at helix/strand frequencies.

**H4 (local 3D structural context):** The structural properties of the FLANK positions (not just the center) predict anchorhood. E.g., the flank has an unusual spatial arrangement — multiple positions in 3D contact with the center, or a contact density peak.

**H5 (positional context):** Where the anchor sits in the protein matters — relative position, distance to termini, proximity to SSE boundaries, position within its own SSE segment.

**H0 (no simple pattern):** None of the above feature families predict anchorhood once burial and packing are controlled for. The model computes a nonlinear function of the flank.

---

## Design principle

Run one model per hypothesis. This lets us identify WHICH feature family carries signal (if any), rather than mixing everything and hoping L1 sorts it out. Then run one combined model to test conjunctions.

---

## Protein set

Top 500 high-confidence anchor proteins from `anchor_behavior_audit.csv`:
- rho >= 0.95, top3_mass >= 0.70
- Anchor at least 30 residues from sequence edges

Compute PDB-derived features (RSA, contacts_8A, SSE) for all proteins. Use existing infrastructure — generate for any protein that doesn't have them.

**Minimum viable:** >= 200 proteins with full PDB features.

---

## Anchor definition

**Top-1 anchor per protein** by projection score. Cleanest, avoids multi-anchor ambiguity.

---

## Control matching

For each anchor, find 5 matched controls from the SAME protein:
1. Same SSE coarse type (H/E/C)
2. RSA within 0.02 (relax to 0.05 if needed)
3. contacts_8A within 2 (relax to 4 if needed)
4. At least 10 residues away from anchor
5. Not in the top 10% of projection score for that protein
6. At least 30 residues from sequence edges (so R=30 window fits)

If < 3 controls after relaxation, drop the protein.

---

## Radius

**Primary: R = 30.** One radius. We know the anchor signal requires ±20-30 residues (flank masking v1). Testing smaller radii where the signal doesn't exist yet is uninformative.

**Secondary: R = 15.** One check at half-radius. If signal exists here, the discriminating pattern is local to the immediate neighborhood. If not, the full ±30 context is needed.

No center censoring. Controls are matched on center properties.

---

## Feature sets (one per hypothesis)

### Model H1: AA identity (tests specific amino acid patterns)
- Per-position amino acid one-hot: 20 AAs x 61 positions = **1220 features**
- This is the maximal representation for detecting any position-specific AA pattern
- Do NOT reduce to AA classes — that loses information (leucine vs isoleucine might matter)

### Model H2: SSE arrangement (tests secondary structure layout)
- Per-position SSE one-hot: 3 (H/E/C) x 61 positions = **183 features**
- SSE transition indicator at each position (1 if SSE changes from previous position): 60 features
- Total: **243 features**

### Model H3: Physicochemical profile (tests property gradients)
- Per-position continuous features:
  - Kyte-Doolittle hydrophobicity
  - Charge at pH 7 (+1 for R/K/H, -1 for D/E, 0 otherwise)
  - Side-chain volume (Zamyatnin scale or similar)
  - Backbone flexibility (B-factor proxy from AA identity, e.g., Smith et al. scale)
- 4 properties x 61 positions = **244 features**

### Model H4: Local 3D structural context (tests spatial arrangement of the flank)
- Per-position PDB features:
  - RSA of position j
  - contacts_8A count of position j
  - Binary: is position j in 3D contact (< 8A) with the center residue?
  - Long-range contact fraction of position j
- 4 features x 61 positions = **244 features**
- This has NEVER been tested before. The v2 experiment only used center-residue structural features for matching.

### Model H5: Positional context (tests where the anchor sits)
- Anchor position / protein length (fractional position)
- Distance to N-terminus (residues)
- Distance to C-terminus (residues)
- Number of SSE segments in the ±30 window
- Length of the SSE the anchor sits in
- Position within own SSE (fraction: 0 = start, 1 = end)
- Number of SSE transitions in the ±30 window
- Total: **~7 features**

### Model FULL: All combined
- H1 + H2 + H3 + H4 + H5 = **~1958 features**
- Tests whether conjunctions across families carry signal that individual families miss

---

## Models

### Primary: L1 logistic regression
- `penalty="l1"`, `solver="liblinear"`, `C=1.0`, `max_iter=2000`
- `class_weight="balanced"`
- StandardScaler on train fold
- Coefficients rescaled by 1/scale for interpretability

L1 is the right regularizer here — it's designed for exactly this situation (many features, sparse signal expected). If the signal exists, L1 will find it and zero out irrelevant features.

### Secondary: Gradient boosted trees (on Model FULL only)
- `n_estimators=200`, `max_depth=3`, `learning_rate=0.1`
- Balanced sample weights
- Tests whether there's nonlinear/interaction signal that L1 misses

---

## Evaluation

### Leave-one-protein-out (LOPO)
`GroupKFold` with protein as group. `n_splits = min(10, n_proteins)`.

### Metrics
- **AUPRC** (primary — handles class imbalance correctly)
- AUROC
- Balanced accuracy at 0.5 threshold
- **Base rate** reported explicitly (expected: ~1/6 if 1 anchor per 5 controls)

### Significance
- Permutation test: shuffle labels 100 times, re-run LOPO, get null distribution of AUPRC
- Report whether observed AUPRC exceeds 95th percentile of null

---

## Main analyses

### Analysis 1: Per-hypothesis model comparison
Bar chart: AUPRC for each of {H1, H2, H3, H4, H5, FULL} at R=30.

This is the main result. It directly tells us which hypothesis (if any) has predictive power.

### Analysis 2: R=30 vs R=15 comparison
For the model(s) that show signal at R=30, check R=15.

If signal drops at R=15, the discriminating pattern requires the full ±30 context.
If signal is already present at R=15, the pattern is more local.

### Analysis 3: Top features (if signal exists)
For whichever model works, extract top 20 L1 coefficients.

For H1: which amino acids at which relative positions?
For H2: which SSE types at which positions?
For H4: which structural properties at which positions?

These are direct hypothesis outputs — "the model can predict anchors because of [this specific feature]."

### Analysis 4: SSE-only control comparison (artifact check)
Re-run Model H1 and Model FULL with SSE-only matched controls (no RSA/contact matching).

If AUPRC jumps dramatically, the v2 SSE-only signal was a burial artifact.
If AUPRC stays similar, structural matching wasn't the issue.

---

## Success criteria

### H1-H5 confirmed (strong positive)
One or more individual models have AUPRC > 1.5x base rate, survives permutation test.
Top coefficients are interpretable and biologically coherent.

### FULL works but individuals don't (conjunction)
Signal exists in feature combinations across families but not within any single family.
Harder to interpret but still informative.

### All models fail (H0 confirmed)
AUPRC ≈ base rate for all models at R=30 with 500 proteins and proper matching.
This is a definitive negative: no handcrafted feature of the local window predicts anchorhood.
Publishable as: "the anchor feature is a genuinely learned concept not expressible in standard structural/sequence descriptors."

---

## Outputs

- `reports/outputs/multi_protein/anchor_local_flank_v3.md`
- `reports/outputs/multi_protein/anchor_local_flank_v3_metrics.csv`
- `reports/outputs/multi_protein/anchor_local_flank_v3_coefficients_{H1,H2,H3,H4,H5,FULL}.csv`

Plots:
1. `anchor_local_flank_v3_hypothesis_comparison.png` — AUPRC per model
2. `anchor_local_flank_v3_top_features.png` — top coefficients for best model
3. `anchor_local_flank_v3_null_distribution.png` — permutation test
4. `anchor_local_flank_v3_sse_vs_structural_controls.png` — artifact check

---

## Reuse

- Protein selection: `anchor_behavior_audit.csv`
- PDB feature computation: `anchor_regression_v3.py` (per-residue RSA, contacts, SSE) — extend to all proteins
- Control matching: adapt from `anchor_regression_v3.py`
- Classification infrastructure: adapt from `anchor_local_flank_v2.py`
- Contact map computation: from existing PDB pipeline

---

## Script

Create: `scripts/anchor_local_flank_v3.py`

```bash
uv run python scripts/anchor_local_flank_v3.py --device cpu
```

No GPU needed.

---

## Notes

- The per-position PDB features (H4) are the most novel test here. V2 never checked whether the STRUCTURAL context of the flank (not just the center) distinguishes anchors.
- H1 with full AA one-hot is the most powerful motif detector. If it fails at 500 proteins with L1, there's no simple AA pattern.
- H5 is cheap but connects to the Pfam "last conserved block" observation.
- The permutation test is important — with high-dimensional features and LOPO, we need to know the null distribution to trust any positive result.
