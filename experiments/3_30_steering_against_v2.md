# Affected-Target Characterization after Selector Ablation

## Context

`anchor_selector_ablation.py` established two things:

1. removing the (d)-component suppresses L10H9 anchor selection
2. the same ablation causes much broader distal disruption for anchors than for matched controls

The open question now is:

> What kind of target residues are being disrupted?

That is the key step toward interpreting what the selector is detecting.

## Goal

Characterize the residues most affected by (d)-ablation of anchor sites, and test whether they are enriched for:

* direct 3D contacts
* contact-graph neighbors / structural sectors
* same or different SSEs
* EVcouplings / Jacobian-style coupling if available
* shared Pfam / HMM landmarks across proteins

## Main hypothesis

The affected targets are not random distant residues.

Compared with matched controls, anchor ablation should preferentially disrupt residues that are:

* far in sequence but structured in relation to the anchor
* enriched for direct or near contact-graph overlap
* spread across multiple SSEs / sequence bins
* possibly enriched for coupling-based relationships when available

## Reuse from previous script

Extend `scripts/anchor_selector_ablation.py` into:

* `scripts/anchor_target_characterization.py`

Reuse directly where possible:

* model loading
* `compute_search_dir()`
* `capture_projection_scores()`
* `compute_pdb_features()`
* `compute_sse_features()`
* `build_matched_controls()`
* `identify_top_k_anchors()`
* `get_baseline_logprobs()`
* `get_ablated_logprobs()`

Also reuse the same:

* top-1 / top-3 anchor definition
* matched controls
* distant target definition
* delta metric

 

## Inputs

* protein sequences
* SSE annotations
* PDB-derived contact maps
* top-1 and top-3 anchor residues
* matched controls
* target-level delta outputs from selector ablation
* optional:

  * EVcouplings scores
  * Pfam / HMM alignment mappings if already available from prior experiments

## Target selection

For each source residue (i):

Use the same distant targets as in the selector-ablation experiment, and compute

[
\Delta(i \to j) =
\log P(\text{true}_j \mid j\ \text{masked},\ \text{clean})
----------------------------------------------------------

\log P(\text{true}_j \mid j\ \text{masked},\ d\text{-ablated at } i)
]

Then define affected targets in two ways:

### A. continuous

Use all targets with their delta values.

### B. thresholded

Mark targets as affected if:

```python
delta > 0.01
```

Also keep a stricter version:

```python
top_k_affected = top 4 targets by delta
```

This avoids the analysis being dominated by weak near-zero effects.

## New target-level annotations

For each source-target pair ((i, j)), add:

### 1. Sequence relationship

* `seq_sep = abs(i - j)`
* `same_seq_bin`
* `source_bin`
* `target_bin`

### 2. Structural relationship

Using the PDB contact graph:

* `direct_contact_8A`
* `graph_distance` between source and target
* `same_contact_component`
* `same_or_adjacent_contact_shell` if easy

Primary bins:

* graph distance = 1
* graph distance = 2
* graph distance >= 3 / unreachable

### 3. SSE relationship

* `same_sse_type`
* `same_sse_segment`
* `different_sse_same_type`
* `different_sse_different_type`

### 4. Contact-neighborhood overlap

For source (i) and target (j), compare their contact neighborhoods:

* Jaccard overlap of contact partners
* number of shared contact partners

This is important because targets may be far from the anchor but still belong to the same structural sector.

### 5. Optional coupling annotations

If available:

* EVcouplings score for ((i, j))
* categorical-Jacobian coupling score for ((i, j))

Do not block the experiment on this. Add only if already easy.

### 6. Optional family / HMM annotation

If HMM column mappings already exist:

* source HMM column
* target HMM column
* whether affected targets cluster in similar HMM regions across proteins

This is secondary.

## Main analyses

## Analysis 1: what kinds of targets are affected?

Compare anchors vs matched controls on the affected-target set.

Primary summaries:

* fraction of affected targets in direct 3D contact
* fraction with graph distance 2
* mean graph distance
* fraction in same SSE segment
* fraction in different SSEs
* mean contact-neighborhood overlap
* number of distinct SSE segments touched by affected targets

This directly tests whether the disrupted targets are:

* local neighbors
* structural-sector neighbors
* broad cross-SSE targets

## Analysis 2: contact / graph enrichment over random distant targets

For each source residue, compare the affected targets against all sampled distant targets from that same source.

Example:

```python
P(direct_contact | affected) vs P(direct_contact | all_targets)
```

and similarly for:

* graph distance 2
* same SSE
* shared contact-neighborhood overlap

This matters more than raw fractions because different proteins have different base rates.

## Analysis 3: anchor vs control target-profile comparison

For each protein, compare top-1 anchor against mean matched controls on:

* direct-contact enrichment
* graph-distance-2 enrichment
* cross-SSE fraction
* distinct SSE segments touched
* contact-neighborhood overlap

Main question:

> Do anchors disrupt a more structured and more distributed target set than matched controls?

## Analysis 4: top-1 vs top-3 anchors

As before, compare:

* top-1 anchor
* top-3 anchor mean

This matters because many proteins appear to have multiple anchor-like residues with weaker but similar target profiles.

## Analysis 5: optional coupling test

If coupling data is available, test whether affected targets are enriched for high coupling to the source residue.

Main discriminator:

* contact enrichment only
* coupling enrichment only
* both
* neither

This is the strongest geometry-vs-stored-statistics test, but optional.

## Success criteria

### Outcome A: direct-contact / neighborhood overlap enrichment

Affected targets are enriched for:

* direct 3D contacts
* graph distance 1 to 2
* shared contact neighborhoods

Interpretation:
The selector is finding residues that summarize a structural neighborhood or sector.

### Outcome B: broad cross-SSE enrichment

Affected targets are often:

* far in sequence
* across multiple SSEs
* not limited to direct contacts

Interpretation:
The selector is finding residues with broader fold-level leverage.

### Outcome C: coupling enrichment

Affected targets are enriched for coupling signals beyond plain contact.

Interpretation:
The selector may be indexing stored evolutionary dependencies, not just geometry.

### Outcome D: no clear structure

Affected targets do not show clear enrichment relative to baseline distant targets.

Interpretation:
The distal-leverage result is real, but target identity is harder to interpret.

## Suggested plots

### Plot A: affected-target relationship breakdown

For anchors vs controls:

* direct contact
* graph distance 2
* graph distance >= 3
* same SSE
* different SSE

### Plot B: per-protein enrichment

Per-protein anchor minus control difference for:

* direct-contact enrichment
* neighborhood-overlap enrichment
* distinct SSE segments touched

### Plot C: target distance scatter

For target-level rows:

* x = sequence separation
* y = delta
* color by direct contact or graph distance

### Plot D: contact-neighborhood overlap

Anchor vs control comparison on:

* shared contact partners
* Jaccard overlap

### Optional Plot E: coupling enrichment

If available:

* affected vs non-affected target pairs by coupling score

## Outputs

* `reports/outputs/multi_protein/anchor_target_characterization.md`
* `reports/outputs/multi_protein/anchor_target_characterization_source_level.csv`
* `reports/outputs/multi_protein/anchor_target_characterization_target_level.csv`

## Fast path

If time is tight, run only:

1. top-1 and top-3 anchors
2. matched controls
3. target-level annotations for:

   * direct contact
   * graph distance
   * same/different SSE
   * shared contact partners
4. analyses:

   * affected vs all-target enrichment
   * anchor vs control comparison

Skip coupling and HMM alignment for the first pass.

## Decision after running

If affected targets are enriched for direct contact / shared neighborhoods:

* push the story toward structural-sector summary points

If they are enriched across multiple nonlocal SSEs:

* push the story toward fold-level leverage

If coupling enrichment is strongest:

* push the story toward stored evolutionary dependency structure

