# Selector-Direction Ablation for Anchor Residues

## Context

For L10H9, we have a global selector direction

[
d = W_K^\top \tilde q
]

and the projection score (x_j \cdot d) ranks anchor residues highly.

The open question is:

> Among buried / high-contact residues, are anchors the ones whose (d)-aligned residual component gives unusually broad distal predictive leverage?

## Goal

Test whether removing the (d)-component from a residue's layer-10 residual:

1. suppresses its L10H9 anchor score / attention rank
2. causes broader downstream disruption for anchors than for matched controls

## Hypothesis

Anchors are not just buried hubs.

They are residues whose layer-10 residual contains a strong selector-aligned component that supports broad distal prediction across multiple sequence regions.

So removing that component should hurt anchors more than matched controls, especially on sparse / diversity-aware summaries.

## Inputs

* protein sequences
* ESM2 model access
* global L10H9 selector direction (d)
* per-protein top-1 and top-3 anchor residues by projection score
* matched non-anchor controls from the same protein, matched on:

  * SSE coarse type
  * RSA
  * contacts_8A

## Intervention

For source residue (j) with layer-10 input residual (x_j), compute

[
\operatorname{proj}_d(x_j) = \frac{x_j^\top d}{|d|_2^2} d
]

and edit

[
x_j' = x_j - c , \operatorname{proj}_d(x_j)
]

Use:

* `c = 1.0` by default
* optional `c = 0.5` as a softer ablation

Then rerun from layer 10 onward.

Run this for:

* top-1 anchor
* top-3 anchors
* matched controls

## Analysis 1: selector validation

Check whether removing the (d)-component actually suppresses anchorhood.

For each edited source residue, measure before vs after:

* L10H9 attention mass into that residue
* rank percentile of that residue among key targets
* whether the top-1 / top-3 anchor identity changes

This is the sanity check.

## Analysis 2: distal leverage

For each source residue (j), evaluate distant target positions (t) with

[
|j - t| \ge 24
]

Define target effect as

[
\Delta(j \to t) =
\log P(\text{true}_t \mid t\ \text{masked},\ \text{clean})
----------------------------------------------------------

\log P(\text{true}_t \mid t\ \text{masked},\ d\text{-ablated at } j)
]

Interpretation:

* positive (\Delta) means the (d)-aligned component at source (j) helps predict target (t)

Sample up to 16 distant targets per source, stratified across sequence bins if possible.

Per source residue, report:

* `mean_delta`
* `top25_mean_delta`
* `max_delta`
* `fraction_positive`
* `n_bins_affected` = number of sequence bins with at least one target above threshold
* `affected_bin_entropy`

## Main comparisons

### A. Top-1 anchor vs matched controls

Per protein, compare top-1 anchor summaries against the mean of matched controls.

### B. Top-3 anchor pooled analysis

Per protein, average summaries over the top-3 anchors and compare against pooled matched controls.

This matters because many proteins appear to have more than one anchor-like residue.

## Success criteria

### Strong success

* removing (d) sharply lowers L10H9 attention rank at anchor residues
* anchors show larger distal disruption than matched controls
* the clearest effects are in:

  * `top25_mean_delta`
  * `n_bins_affected`
  * `affected_bin_entropy`
    rather than only plain mean

Interpretation:

> L10H9 is selecting residues whose selector-aligned state gives unusually broad distal predictive leverage, not just generic buried hubs.

### Weak / negative result

* selector ablation lowers attention rank
* but anchors do not beat matched controls on distal disruption

Interpretation:

> (d) captures the selector mechanics, but not the property that makes anchors special.

## Outputs

* `reports/outputs/multi_protein/anchor_selector_ablation.md`
* `reports/outputs/multi_protein/anchor_selector_ablation_source_level.csv`
* `reports/outputs/multi_protein/anchor_selector_ablation_target_level.csv`

Suggested plots:

* anchor rank drop before vs after ablation
* anchor vs control differences for `top25_mean_delta`
* anchor vs control differences for `n_bins_affected`
* top-1 vs top-3 comparison

## Fast path

If time is tight, run only:

1. top-1 and top-3 anchors
2. matched controls
3. `c = 1.0`
4. 16 distant targets per source
5. metrics:

   * attention rank drop
   * `top25_mean_delta`
   * `n_bins_affected`
   * `fraction_positive`

## Script plan

Create:

* `scripts/anchor_selector_ablation.py`

Reuse existing utilities for:

* model loading
* layer-10 residual capture
* anchor positions
* matched controls
* report writing

