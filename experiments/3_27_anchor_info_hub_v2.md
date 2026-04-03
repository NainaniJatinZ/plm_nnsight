
# Targeted Anchor Information-Hub Test (experiments/3_27_anchor_information_hub_v2.md)

## Context

v1 of the information-hub experiment gave partial support for the family C hypothesis:

- EVcouplings signals were weakly suggestive but underpowered.
- The ESM conditional-influence test showed a medium effect in the right direction, but only 10/16 proteins had anchor > matched controls.
- The current belief is that anchor information-hub behavior is likely **heterogeneous** and may be concentrated on the **right target residues**, rather than appearing uniformly on random distant targets.

Separately, the v3 structural regression experiment showed that anchors are strongly enriched for:
- distributed contact structure
- contact-bin entropy
- closeness / betweenness
- long-range contact fraction

So the open question is now:

> Are anchors informative in a broad, generic way, or specifically for the residues that matter for structure / task performance?

This experiment is designed to answer that more sharply.

---

## Goal

Refine the information-hub test by asking:

1. **Where** does the anchor help prediction?
2. Does the effect become stronger when we use:
   - multiple anchor-like source residues per protein
   - structurally or task-relevant target sets
   - better summaries than plain mean over random distant targets?

---

## Main hypothesis

Anchors are not uniformly more informative for all distant residues.

Instead, compared with matched controls, anchors should show stronger conditional influence on:

- **task-relevant target residues**
- **distant 3D-contact residues**
- possibly a small subset of especially affected targets

The old v1 signal was likely diluted by averaging over too many random distant targets and by using only a single top-1 anchor residue.

---

## Key changes from v1

### Change 1: Use an anchor set, not just top-1
Per protein, define:
- `anchor_top1`: highest L10H9 projection residue
- `anchor_top3`: top 3 projection residues by score

Run both:
- top-1 anchor analysis
- top-3 anchor-set pooled analysis

This directly addresses the fact that many proteins have 2 to 4 anchor-like residues.

### Change 2: Split targets into biologically / mechanistically meaningful groups
Instead of using only random distant targets, evaluate several target sets separately.

### Change 3: Use sparse-target summaries
In addition to mean influence, compute:
- top quartile mean
- max influence
- fraction positive

This captures the possibility that anchors strongly help a subset of targets rather than weakly helping everything.

---

## Inputs

Reuse from previous experiments:
- sequences
- anchor projection scores
- matched controls from `anchor_regression_v3`
- PDB-derived residue contact maps
- task SSE / flank metadata if available from protein configs
- ESM2 model access

Do **not** include the EVcouplings part in v2. Keep this experiment focused and fast.

---

## Source residues

For each protein:

### Anchor sources
- `A1`: top-1 projection residue
- `A3`: top-3 projection residues

### Control sources
For each anchor residue, use matched controls from v1 / v3:
- same SSE coarse type
- matched on RSA
- matched on contacts_8A
- exclude top-10% projection rank residues

Use:
- 5 matched controls per anchor if available
- if fewer, use all available and record count

### Optional hard negatives
For each protein, optionally include:
- 1 high-contact, low-projection residue
- 1 random non-anchor residue

Only as sanity checks, not main comparisons.

---

## Target sets

Evaluate influence separately on the following target groups.

### G1: random distant targets
Purpose: baseline / negative-control-like target set.

For source residue `i`, sample:
- up to 16 targets `j`
- such that `|i - j| >= 24`
- stratified across sequence bins if possible

This reproduces the v1 setup in a cleaner way.

### G2: task-relevant targets
Purpose: test whether anchors preferentially help the contact-prediction task.

If protein config provides target SSEs / flanks, define:
- all residues in SS1
- all residues in SS2
- optional flank windows around those SSEs

Exclude `j = i`.

If no task metadata exists for a protein, skip G2 for that protein and record it explicitly.

### G3: distant structural-contact targets
Purpose: test whether anchors preferentially help structurally linked residues.

For source residue `i`, define targets `j` such that:
- `j` is in 3D contact with `i` in the PDB
- `|i - j| >= 24`

If there are more than 16 such targets:
- keep all, or cap at 16 with deterministic selection

If there are fewer than 4:
- still use them, but mark the set as low-count

### Optional G4: high-uncertainty targets
Optional, only if easy.

For each protein, estimate masked-token entropy per position under ESM.
Then for source residue `i`, use:
- top 16 high-entropy positions with `|i-j| >= 24`

This asks whether anchors matter most where the model is uncertain.

Do **not** block the experiment on G4. It is optional.

---

## Influence definition

Use the same metric as v1:

```python
influence(i -> j) = logP(true_j | seq with j masked)
                  - logP(true_j | seq with i and j masked)
````

Interpretation:

* positive influence means residue `i` helps predict target `j`
* larger positive values mean stronger conditional dependence

---

## Per-source summaries

For each source residue `i` and target set `G`, compute:

* `mean_influence`
* `median_influence`
* `max_influence`
* `top25_mean_influence`
* `fraction_positive`
* `n_targets`
* `n_targets_above_0.01` or another fixed threshold

These summaries matter because anchor effects may be sparse rather than diffuse.

---

## Main comparisons

## Analysis 1: top-1 anchor vs matched controls

For each protein and each target set G1/G2/G3:

Compare:

* top-1 anchor summary metrics
  vs
* mean matched-control summary metrics

Primary readouts:

* `mean_influence`
* `top25_mean_influence`
* `fraction_positive`

This is the direct replacement for v1.

## Analysis 2: top-3 anchor-set pooled analysis

For each protein:

Compute the mean of the top-3 anchor source summaries.
Compare against:

* pooled mean of matched control summaries

This addresses the multi-anchor issue.

## Analysis 3: target-set specificity

For anchors and controls, compare performance across target groups:

* G2 vs G1
* G3 vs G1

Main question:

> Does anchor advantage get stronger on task-relevant or structural-contact targets than on random distant targets?

This is the highest-value analysis.

## Analysis 4: sparse-target advantage

Test whether anchors differ more strongly from controls on:

* `top25_mean_influence`
* `max_influence`
  than on plain mean

If yes, that supports the idea that anchors help a subset of key targets strongly.

## Analysis 5: bridge to structural features

Using outputs from `anchor_regression_v3`, correlate source-level influence summaries with:

* contact_bin_entropy
* n_contact_bins
* long_range_fraction
* closeness
* betweenness

Do this across:

* anchors
* matched controls
* optional hard negatives

This is a bridge analysis:

> Do the same structural-integration features that predict anchorhood also predict conditional influence?

This is secondary but high value.

---

## Statistical reporting

For each analysis, report:

* per-protein differences
* cross-protein paired mean difference
* Cohen’s d
* paired t-test p
* Wilcoxon signed-rank p

Treat cross-protein tests as descriptive unless the effect is strong and consistent.

The main emphasis should be:

* direction consistency
* effect sizes
* target-set specificity

not only p-values.

---

## Success criteria

### Strong success

Anchors beat matched controls clearly on G2 and/or G3, especially in:

* top-3 anchor-set analysis
* top25_mean_influence
* fraction_positive

This would mean the information-hub effect is real but target-specific.

### Moderate success

Anchors weakly beat controls on G1 and more clearly on G2/G3 in a subset of proteins.

This would still be a useful result and likely the expected outcome.

### Weak result

Anchors do not reliably beat controls on any target set.

Then the information-hub story is likely secondary to structural integration.

---

## Interpretation guide

### Outcome A

Anchors win strongly on G2 and G3, but not G1.
Interpretation:

* anchors are not generic global predictors
* they are targeted structural / task-relevant information hubs

### Outcome B

Anchors win on all target sets.
Interpretation:

* anchors are broad global information hubs

### Outcome C

Anchors only win in top25 / max metrics, not mean.
Interpretation:

* anchors help a sparse set of critical targets strongly

### Outcome D

Anchors do not win beyond matched controls.
Interpretation:

* family C is weaker than family A and probably not the main explanation

---

## Outputs

* `reports/outputs/multi_protein/anchor_information_hub_v2.md`
* `reports/outputs/multi_protein/anchor_information_hub_v2_*.png`
* `reports/outputs/multi_protein/anchor_information_hub_v2_source_level.csv`
* `reports/outputs/multi_protein/anchor_information_hub_v2_target_level.csv`

---

## Suggested plots

### Plot A: anchor-control difference by target set

For each metric:

* G1, G2, G3 on x-axis
* anchor minus control difference on y-axis

Use:

* mean influence
* top25 mean
* fraction positive

### Plot B: per-protein connected-line plots

For a few representative proteins:

* anchor summary
* control mean summary
  for each target set

### Plot C: top-1 vs top-3 comparison

Does using top-3 anchors strengthen the effect?

### Plot D: influence heatmaps

For a few proteins, show:

* source on x-axis
* target position on y-axis
* influence value as heatmap

Include:

* top anchor
* one matched control

### Plot E: structure-feature bridge

Scatter plots:

* influence summary vs contact_bin_entropy
* influence summary vs closeness
* influence summary vs long_range_fraction

---

## Implementation notes

* Reuse matched controls from previous experiments whenever possible.
* Do not expand to all residues.
* Do not rerun EVcouplings here.
* Keep compute manageable:

  * anchor sources only
  * matched controls only
  * up to 16 targets per group
* Batch masked inputs wherever possible.

### Practical defaults

* `top_k_anchors = 3`
* `n_random_targets = 16`
* `long_range_sep = 24`
* `positive_threshold = 0.01`

---

## Fast path / minimal version

If time is tight, run only:

1. top-1 and top-3 anchors
2. matched controls
3. G1 random distant targets
4. G2 task-relevant targets
5. metrics:

   * mean influence
   * top25 mean
   * fraction positive

Then add G3 as a second pass.

---

## Script plan

Create:

* `scripts/anchor_information_hub_v2.py`

It should:

1. load source residues
2. load matched controls
3. construct target sets G1/G2/G3
4. compute influence metrics
5. summarize per source and per protein
6. write markdown report + plots + CSVs

---

## Execution

```bash
uv run python scripts/anchor_information_hub_v2.py --device cuda
```

Dependencies:

```bash
pip install biopython pandas numpy scipy matplotlib
```

---

## Decision after running

If G2/G3 sharpen the signal:

* family C is alive and target-specific
* next step should be mechanistic analysis of anchor-to-target pathways

If not:

* focus on family A structural integration story
* path patching should probably target how anchor heads identify structurally integrative residues rather than how they transmit sequence information

```


Two very small practical notes for the agent, which I’d include outside the spec if needed:

- **Do not overbuild G4.** Skip it unless it is genuinely easy.
- **Top-3 anchor-set analysis is important.** I would not drop that part.

