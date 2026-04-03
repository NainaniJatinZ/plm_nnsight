# Anchor Information-Hub Test (experiments/3_27_anchor_information_hub_v1.md)

## Context

The structural regression experiment asks:
> what geometric or graph property distinguishes anchors?

This experiment asks:
> are anchors unusually informative positions for predicting the rest of the sequence?

This is the family C / information-hub experiment.

We want a residue-level test of whether anchors are:
- unusually strong carriers of coevolutionary signal
- unusually useful for predicting distant residues
- unusually informative compared with matched non-anchor controls

This experiment has two tracks:

1. **MSA / EVcouplings track** for proteins with EVcouplings outputs
2. **Non-MSA ESM conditional-influence track** for all proteins

The point is not to prove full information theory. The point is to get an operational answer to:
> does knowing the anchor help predict many other residues more than knowing a matched non-anchor?

---

## Previous experiments to reference

- `scripts/anchor_regression.py`
- `scripts/anchor_regression_v2.py`
- `scripts/anchor_regression_v3.py` once available

Reuse:
- protein loading
- sequence loading
- anchor positions / projection score logic
- matched control construction from v3 if implemented

---

## Data available

### Available for subset of proteins
For proteins with EVcouplings runs:
- alignment:
  - `data/<PROTEIN>_EV/TARGET_b*/align/TARGET_b*.a2m`
- conservation:
  - `data/<PROTEIN>_EV/TARGET_b*/align/TARGET_b*_frequencies.csv`
- coupling scores:
  - `data/<PROTEIN>_EV/TARGET_b*/couplings/TARGET_b*_CouplingScores.csv`
  - `data/<PROTEIN>_EV/TARGET_b*/couplings/TARGET_b*_CouplingScores_longrange.csv`

### Available for all proteins
- full sequences
- SSE
- anchor positions / projection scores
- ESM2 model access

---

## Core hypothesis

If anchors are information hubs, then compared with matched non-anchor residues they should have one or both of:

### H1: coupling-dispersion enrichment
In proteins with MSAs, anchors participate in stronger and more spatially distributed coupling structure.

### H2: conditional influence enrichment
In ESM, masking the anchor should hurt prediction of many distant target residues more than masking a matched non-anchor.

---

# Part A: MSA / EVcouplings track

## Goal

For proteins with EVcouplings outputs, quantify whether anchors are residues with unusually:
- strong couplings
- many long-range couplings
- couplings spread across many sequence regions
- couplings to many distinct SSEs

This is the cleanest bridge to the coevolution story.

## Input files

For each protein with EVcouplings:
- `TARGET_b*.a2m`
- `TARGET_b*_frequencies.csv`
- `TARGET_b*_CouplingScores.csv`
- `TARGET_b*_CouplingScores_longrange.csv`

Use the long-range coupling file when available.

---

## Per-residue coupling features

From the coupling CSV, aggregate pairwise rows into residue-level features.

For each residue `i`, compute:

### Strength features
- `sum_coupling_score`
- `mean_coupling_score`
- `max_coupling_score`
- `sum_cn`
- `max_cn`
- `sum_probability`
- `n_strong_pairs_above_threshold`

Use thresholds on `score`, `cn`, or `probability`.

### Long-range features
Using long-range file or `|i-j| >= 24`:
- `n_longrange_pairs`
- `sum_longrange_score`
- `mean_longrange_score`
- `max_longrange_score`

### Spread features
Across sequence bins:
- `n_coupling_bins`
- `coupling_bin_entropy`

Across SSE segments:
- `n_distinct_sse_coupling_partners`

### Rank features
Within each protein:
- percentile rank of `sum_longrange_score`
- percentile rank of `n_longrange_pairs`
- percentile rank of `coupling_bin_entropy`

---

## Analysis A1: anchor vs matched controls
Reuse the matched controls from v3 if possible.

For each anchor residue, compare against matched non-anchor residues from the same protein:
- matched on SSE type
- RSA
- contacts_8A
- optionally projection-rank neighborhood excluded

Test whether anchors are enriched in:
- `sum_longrange_score`
- `n_longrange_pairs`
- `n_coupling_bins`
- `coupling_bin_entropy`
- `n_distinct_sse_coupling_partners`

This is the main MSA result.

## Analysis A2: projection score vs coupling features
On proteins with MSA data:
- correlate projection score with per-residue coupling features
- fit a simple regression:
```python
proj ~ coupling_strength + coupling_spread + protein_FE
````

This is secondary to A1.

## Analysis A3: anchor rank in coupling space

For each protein, report where the anchor ranks by:

- long-range coupling strength
    
- coupling spread
    
- distinct SSE coupling partners
    

If anchors are consistently top-ranked or near top-ranked, that is a strong result.

---

# Part B: non-MSA ESM conditional-influence track

## Goal

Measure whether the anchor residue is unusually useful for predicting distant residues under ESM, compared with matched controls.

This is the model-native version of the information-hub test.

## Key idea

For a source residue `i` and target residue `j`, define the influence of `i` on predicting `j` as:

1. mask target residue `j`
    
2. compute log-probability of the true residue at `j`
    
3. also mask source residue `i` in addition to `j`
    
4. recompute log-probability of the true residue at `j`
    
5. define:
    

```python
influence(i -> j) = logP(true_j | seq with j masked)
                  - logP(true_j | seq with i and j masked)
```

If this value is positive, residue `i` helps predict `j`.

This is simple, interpretable, and compatible with ESM MLM training.

---

## Candidate source residues

Do **not** run this for every residue at first.

For each protein, evaluate:

- top 1 to 3 anchor residues
    
- matched controls from v3
    
- optionally 2 high-contact but non-anchor residues
    
- optionally 2 low-contact random residues for sanity
    

This keeps compute manageable.

---

## Target sets

For each source residue `i`, evaluate influence on several target sets.

### Target set T1: distant random targets

Sample `n = 32` target positions `j` such that:

- `|i - j| >= 24`
    
- not equal to `i`
    

Stratify across sequence bins.

### Target set T2: task-relevant targets

Use residues inside:

- SS1
    
- SS2
    
- flanking windows used in the contact task
    

This tests whether anchors specifically matter for the contact setup.

### Target set T3: structurally contacting targets

If PDB available, use residues that are in 3D contact with `i` but distant in sequence.

This helps distinguish direct contact influence from global influence.

---

## Per-source summary metrics

For each source residue `i`, summarize influence over each target set:

- `mean_influence`
    
- `median_influence`
    
- `max_influence`
    
- `fraction_positive_influence`
    
- `n_targets_above_threshold`
    
- `influence_bin_entropy` over sequence bins of target positions helped
    

Interpretation:

- anchors should help many distant targets, not just one local neighborhood
    

---

## Main comparisons

### Analysis B1: anchor vs matched controls

For each protein, compare anchor source residues vs matched control residues on:

- mean influence on T1
    
- mean influence on T2
    
- mean influence on T3
    
- fraction positive influence
    
- influence spread across bins
    

This is the main non-MSA result.

### Analysis B2: source rank

Within each protein, rank candidate source residues by influence score.  
Does the anchor rank near the top?

### Analysis B3: anchor specificity

Compare anchor influence to:

- high-contact non-anchor controls
    
- random controls
    

This tells us whether the anchor is more than a generic buried hub.

---

## Optional faster approximation

If double-masking every `(i, j)` is too slow, use a reduced version:

- only evaluate anchor + matched controls
    
- only use 16 targets per target set
    
- batch target masks where possible
    

Do **not** expand to all residues until the anchor-vs-control signal is established.

---

## Combined interpretation

### Strong family C support

Anchors beat matched controls on:

- coupling spread / long-range coupling metrics  
    and
    
- ESM conditional influence on distant targets
    

### Partial support

Only one track is positive.

Interpretation:

- MSA-positive, ESM-negative: anchor tracks evolutionary coupling but not strong sequence-prediction influence
    
- ESM-positive, MSA-negative: anchor is a model-native information hub not well captured by EVcouplings
    

### Weak support

Neither track shows consistent enrichment over matched controls.

Then family C is probably not the main explanation.

---

## Outputs

- `reports/outputs/multi_protein/anchor_information_hub_v1.md`
    
- `reports/outputs/multi_protein/anchor_information_hub_v1_*.png`
    
- optional:
    
    - `anchor_information_hub_v1_msa_features.csv`
        
    - `anchor_information_hub_v1_influence_scores.csv`
        

---

## Suggested plots

### Plot A: anchor vs matched controls on MSA coupling features

Effect sizes for:

- `sum_longrange_score`
    
- `n_longrange_pairs`
    
- `n_coupling_bins`
    
- `coupling_bin_entropy`
    
- `n_distinct_sse_coupling_partners`
    

### Plot B: anchor vs matched controls on ESM influence

Per-protein connected-line plots for:

- mean influence on T1
    
- mean influence on T2
    
- mean influence on T3
    

### Plot C: rank of anchor among source residues

Bar or table:

- coupling rank
    
- influence rank
    

### Plot D: per-protein influence maps

Heatmaps of `influence(i -> j)` for anchors and controls on a few proteins.

---

## Script plan

### Script 1

`scripts/anchor_information_hub_v1.py`

Contains:

- EVcouplings residue-level aggregation
    
- ESM conditional influence computation
    
- comparison against matched controls
    
- report + plots
    

### Optional split

If cleaner:

- `scripts/anchor_coupling_features.py`
    
- `scripts/anchor_conditional_influence.py`
    

But one script is fine for v1.

---

## Execution

```bash
uv run python scripts/anchor_information_hub_v1.py --device cuda
```

Dependencies:

```bash
pip install biopython pandas numpy scipy scikit-learn matplotlib
```

---

## Guardrails

- EVcouplings positions are 1-indexed; convert to 0-indexed.
    
- Be careful about which `TARGET_b*` directory is chosen if multiple exist. Pick the same one consistently per protein.
    
- For the influence test, never compare residues at tiny sequence separation only. The whole point is distant / distributed influence.
    
- Reuse matched controls from v3 whenever possible so the two experiments line up.
    

---

## Minimal version if time is tight

If you want the fastest first pass:

1. run the MSA residue-level coupling aggregation on the 5 proteins
    
2. run the ESM influence test only for:
    
    - anchors
        
    - 5 matched controls per anchor
        
    - 16 distant targets per source
        

That is enough to see whether the family C direction is alive.

## Decision after running

If anchors clearly beat matched controls on the influence test:

- family C is real enough to pursue mechanistically
    

If anchors only win on structural-integration features from v3:

- probably pivot next to structural / upstream path patching
    

If anchors win on both:

- that is the strongest story
