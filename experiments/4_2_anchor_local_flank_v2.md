# 4_2_local_flank_v2


## Goal

Test whether anchorhood is encoded in a **local window motif** around the residue rather than only in properties of the center residue itself.

This experiment has two parts:

1. **Flank pattern discovery**
   - stack anchor-centered windows across proteins
   - visualize amino-acid and SSE patterns

2. **Flank-window anchor classification**
   - predict whether the middle residue is an anchor or a matched non-anchor control
   - compare performance as flank radius grows
   - compare models **with center residue visible** vs **center residue masked out**

The central question is:

> Does local context around a residue contain enough information to predict anchorhood, and does predictive power rise sharply around the same flank size where the anchor signal recovered in the v1 masking experiment?

---

## Motivation from v1

The previous anchor local flank experiment found:

- anchor projection, pre-softmax score, and attention are near zero at small flanks
- all three recover sharply around roughly `R = 20–30`
- projection recovers slightly before or with attention, never after

This suggests the anchor feature is built from a finite local context window.

The natural next step is to ask:
- what is in that window?
- can the window predict anchorhood?

---

## Protein set

### Primary set for visualization
Use the **top 50 most confident anchor proteins** from the anchor behavior audit / flank v1 run.

### Primary set for classification
Use the **top 500 high-confidence proteins** for which:
- anchor behavior is strong
- PDBs are already downloaded or available
- anchor positions are defined
- matched controls are available

If the structural-window pipeline becomes fragile, fall back to:
- all 500 proteins for sequence/SSE features
- only proteins with valid PDB-derived windows for structural-window features

---

## Labels

### Positive examples
For each protein, use:
- top 1 anchor only for the cleanest first pass
- optional second pass: top 3 anchors with `proj >= 0.25`

Start with **top 1** as the default to avoid ambiguity.

### Negative examples
Use **matched non-anchor controls** from the same protein:
- matched on SSE coarse type
- matched on RSA
- matched on contacts_8A
- low projection score

Use 3 to 5 controls per anchor if available.

This is important because the classifier should not solve the task by trivial burial or contact-count effects.

---

## Window definitions

For a center residue `c`, extract symmetric windows:
```python
[c-R, ..., c, ..., c+R]
````

Test multiple radii:

```python
R ∈ {5, 10, 15, 20, 25, 30, 40}
```

### Why multiple radii

This lets us test whether classification performance also shows a transition near the same `R ≈ 20–30` found in the masking-based flank experiment.

---

## Part A: Flank pattern discovery

## A1. Sequence logos and class logos

For anchor windows in the top 50 proteins, aligned so the anchor is at position 0:

Create the following per-position visualizations:

1. **Raw amino-acid frequency logo**
2. **Amino-acid class logo**

   * hydrophobic
   * polar
   * positive
   * negative
   * glycine
   * proline
   * aromatic
3. **SSE logo**

   * H / E / C at each position

Do the same for matched controls.

Then plot:

* anchor logo
* control logo
* anchor-minus-control enrichment heatmap

### Important note

Because raw AA logos may wash out across diverse proteins, the AA-class and SSE versions are likely more informative than the raw AA logo.

## A2. Radius-conditioned logos

Make logos at:

* `R = 10`
* `R = 20`
* `R = 30`

This checks whether the visually informative pattern really emerges in the same range where the v1 anchor signal recovered.

## A3. Adaptive-threshold subset (optional)

Using the v1 threshold radii, define for each protein:

* `R50_alpha`: smallest radius with `alpha_R >= 0.5 * alpha_full`
* `R80_alpha`: smallest radius with `alpha_R >= 0.8 * alpha_full`

Optional descriptive analysis:

* compare windows from proteins with smaller vs larger threshold radii
* ask whether different motif types need different context lengths

This is optional and should not block the main experiment.

---

## Part B: Flank-window anchor classification

## Core idea

Treat each center residue plus its window as one example.

Predict:

```python
y = 1 if center residue is an anchor
y = 0 if center residue is a matched control
```

This is a **window-level** classifier, not a residue-only classifier.

---

## Feature sets

Build several nested feature sets.

## B1. Sequence-only local features

For each window:

* one-hot AA at each relative position
* AA-class at each relative position
* counts of each AA and AA class in the window
* local hydrophobicity profile
* same-face hydrophobicity proxies for ±2 positions
* counts of glycines / prolines / aromatics
* central residue identity and class

## B2. SSE local features

For each window:

* SSE label at each position
* counts of H / E / C in the window
* number of SSE transitions
* length of contiguous center SSE segment within the window
* whether flanks remain in same SSE type or transition out quickly

## B3. Structural-window summary features

For proteins with PDB data, compute per-position or summarized features over the window:

* RSA profile
* contacts_8A profile
* long-range contact count profile
* long-range contact fraction profile
* contact-bin entropy profile
* contacts outside own SSE profile
* distinct SSE partners profile
* betweenness / closeness / degree profile

Also include summary aggregates:

* mean / max / min within window
* center-minus-flank contrasts
* left-right asymmetry
* number of flank positions above thresholds

## B4. Censored-center variants

This is crucial.

For each radius and feature set, run three variants:

### Variant 1: full window

Center residue visible.

### Variant 2: center-censored identity

Remove only the center AA identity/class features.

### Variant 3: center-censored fully

Remove all center-position features:

* AA
* class
* SSE
* structural features at the center

This is the cleanest test of whether the **flank itself** predicts anchorhood.

---

## Models

Use interpretable models first.

### Model family A: elastic-net logistic regression

This should be the main model.

Why:

* interpretable coefficients
* works with sparse one-hot window features
* can reveal position-specific patterns

### Model family B: shallow tree / gradient boosting

Use only as a secondary comparison to detect nonlinear conjunctions.

Do not let the report hinge on a black-box model.

### Optional model family C: 1D CNN

Only if the simple models fail badly and time permits.
This is optional and should not be part of the first pass.

---

## Evaluation

### Primary split

Use **leave-one-protein-out** evaluation.

This is essential.
Do not use random residue splits because residues from the same protein are too correlated.

### Secondary split

If enough data exists, also try:

* leave-one-fold / family-out if a family label is available
* otherwise skip

### Metrics

Report:

* AUROC
* AUPRC
* balanced accuracy
* accuracy at fixed threshold
* calibration plot if easy

The most important metric is:

* how performance changes with radius
* and how much it drops when the center is censored

---

## Main analyses

## Analysis 1: Radius-performance curve

For each model and feature set, plot performance vs flank radius:

```python
R = 5, 10, 15, 20, 25, 30, 40
```

Question:

* does predictive power jump around the same range as the v1 flank recovery?

This is the most important analysis.

## Analysis 2: Center-censor ablation

Compare:

* full window
* center-censored identity
* fully center-censored

Question:

* how much of anchor predictability is in the flank itself?

Interpretation:

* if performance stays high after center censoring, motif context is real
* if performance collapses, the signal is mostly center-local

## Analysis 3: Feature-family ablation

Compare performance using:

* sequence-only
* sequence + SSE
* sequence + SSE + structural-window features

Question:

* which type of local information matters most?

## Analysis 4: Coefficient / rule extraction

From the elastic-net model, extract:

* top positive position-specific features
* top negative features

Examples:

* enriched strand at specific offsets
* hydrophobic residues at certain relative positions
* local transition patterns

This is the main “hypothesis discovery” output.

## Analysis 5: Anchor-threshold linkage

Relate classifier performance at each radius to the v1 recovery thresholds.

For example:

* does classification AUPRC rise sharply near the same `R` where projection recovered?
* proteins with smaller `R50_alpha` thresholds, do they have more stereotyped local windows?

This is optional but high value.

---

## Visual outputs

Create:

1. **Anchor vs control AA-class logo**
2. **Anchor vs control SSE logo**
3. **Radius vs classifier performance**
4. **Center-censor ablation bar chart**
5. **Top logistic features plot**
6. Optional:

   * separate logo panels for high-alpha vs low-alpha anchors
   * separate logos for top-confidence anchors only

---

## Outputs

* `reports/outputs/multi_protein/anchor_local_flank_v2.md`
* `reports/outputs/multi_protein/anchor_local_flank_v2_windows.csv`
* `reports/outputs/multi_protein/anchor_local_flank_v2_metrics.csv`
* `reports/outputs/multi_protein/anchor_local_flank_v2_coefficients.csv`

Plots:

* `anchor_local_flank_v2_logos.png`
* `anchor_local_flank_v2_radius_curve.png`
* `anchor_local_flank_v2_center_ablation.png`
* `anchor_local_flank_v2_top_features.png`

---

## Guardrails

* Use matched controls from the same protein.
* Keep anchor definition strict:

  * top anchor, or top-3 with `proj >= 0.25`
* Start with top-1 anchors for the cleanest first pass.
* Leave-one-protein-out is required.
* Do not overfit with very flexible models first.
* Make the center-censored analysis mandatory.
* Radius sweep is mandatory.

---

## Success criteria

### Strong success

Classification performance rises sharply near `R = 20–30` and remains substantially above chance even when the center is censored.

Interpretation:

* anchorhood is genuinely encoded in a local flank motif

### Moderate success

Performance improves with radius, but center-censoring causes a large drop.

Interpretation:

* local context matters, but center residue features carry much of the signal

### Weak result

Even large windows do not predict anchorhood much above chance under protein-held-out evaluation.

Interpretation:

* either the motif is more complex than these features capture, or the flank-jump signal is not easily expressible in local handcrafted descriptors

---

## Script plan

Create:

* `scripts/anchor_local_flank_v2.py`

Sub-functions:

* load anchor and matched-control windows
* generate AA / class / SSE logos
* build window features for each radius
* run LOPO classifiers
* run center-censor ablations
* output coefficients and plots

---

## Execution

```bash
uv run python scripts/anchor_local_flank_v2.py --device cuda
```


