
# Anchor Feature Regression with Matched Controls (experiments/3_27_anchor_regression_v3.md)

## Context

From v1 and v2 we know:
- The key-side search direction `W_K^T @ q_mean` for L10H9 ranks the main anchor highly.
- SSE / conservation / hydrophobicity explain part of the variance, but anchors remain strong outliers.
- RSA and contact number are useful, but they do not by themselves explain why only a tiny subset of buried, high-contact residues become anchors.
- The current open question is not just “are anchors buried?” but “what distinguishes anchor residues from other similarly buried / similarly connected residues?”

**Goal:** Test whether anchors are residues with unusually high **structural integration** beyond burial and raw contact density.

This is the sharper version of v2:
- keep the projection score pipeline
- keep PDB-derived residue features
- add **graph / long-range / spread** features
- add **matched-control analysis**
- add **anchor-vs-control classification**, not just full-residue regression

## Previous experiments to reference

- `scripts/anchor_regression.py` — v1 baseline regression and projection score pipeline
- `scripts/anchor_regression_v2.py` — v2 structural feature extraction and reporting
- `scripts/anchor_interp_v2.py` — model loading and residual stream capture

**Extend `scripts/anchor_regression_v2.py` into `scripts/anchor_regression_v3.py`.**

Reuse from v2:
- `load_configs()`
- `load_conservation()`
- `_find_pdb()`
- `_align_pdb_to_seq()`
- `compute_pdb_features()`
- `compute_hydrophobic_features()`
- `extract_head_weights()`
- `compute_search_dir()`
- `capture_projection_scores()`

## Data available

- Sequences: `data/full_seq_dict.json`
- SSE: `data/ss_dict.json`
- EVcouplings conservation where available:
  - `data/<PROTEIN>_EV/TARGET_b*/align/TARGET_b*_frequencies.csv`
- PDBs in each EVcouplings protein directory
- Anchor positions for L10H9 from previous summaries / current dictionary
- ~15 to 18 proteins with PDBs
- Only a subset have conservation, but conservation is not the main point of v3

## Core hypothesis

Anchors are **not** merely buried or highly connected residues.

Instead, they are residues with unusually high **distributed structural integration**, such as:
- many long-range contacts
- contacts spread across multiple sequence regions
- contacts to multiple distinct SSEs
- bridge-like or high-centrality positions in the residue contact graph

## Main change from v2

v2 asked:
> can structural features increase R²?

v3 asks:
> after matching on burial and contact density, what still separates anchors from non-anchors?

That is the key experiment.

---

## Labels

Create three analysis targets:

### Target A: continuous projection score
Same as v2:
```python
proj_score[i] = dot(x_ln_layer10[i], key_search_dir_unit)
```

### Target B: hard anchor label

Per protein, mark the top `k` residues by projection score as anchors.

Use:

- `k = 3` by default
    
- or use the protein-specific known number of anchors if available from prior analyses
    

### Target C: main-anchor label

Per protein, the top-1 projection residue only.

This gives:

- a regression task on all residues
    
- a classification task for anchor detection
    
- a stricter top-1 analysis
    

---

## New structural features to add

Keep v2 features:

- RSA
    
- contacts_8A
    
- contacts_10A
    
- long_range_contacts
    
- self_hydro
    
- local_hydro_w5
    
- same_face_hydro
    
- SSE / segment features
    

Add the following:

### Feature 1: long-range contact fraction

```python
long_range_fraction = long_range_contacts / max(contacts_8A, 1)
```

### Feature 2: mean and max contact span

For residue `i`, let contact partners be residues `j` with 8A contact.  
Compute:

```python
mean_contact_span = mean(abs(i - j))
max_contact_span = max(abs(i - j))
```

### Feature 3: contact spread across sequence bins

Split each sequence into `n_bins = 8` equal bins.  
For residue `i`, count how many bins contain at least one contacting residue:

```python
n_contact_bins
```

Also compute entropy over those bins:

```python
contact_bin_entropy
```

Interpretation:

- high `n_contact_bins` / entropy = contacts distributed across the chain
    
- low values = mostly local packing
    

### Feature 4: distinct SSE partners

Assign each residue to an SSE segment ID, not just H/E/C type.  
For residue `i`, count:

```python
n_distinct_sse_partners
```

This is more important than raw degree.

### Feature 5: out-of-segment contact count

Within the residue’s own SSE segment, local contacts are less interesting.  
Compute:

```python
contacts_outside_own_sse
fraction_contacts_outside_own_sse
```

### Feature 6: graph centrality on residue contact graph

Build an undirected graph:

- node = residue
    
- edge = CB-CB distance < 8A (CA for glycine)
    

Compute:

- degree
    
- betweenness centrality
    
- closeness centrality
    
- eigenvector centrality
    
- core number
    

Use `networkx`.

### Feature 7: local clustering coefficient

If anchors are bridge-like, they may have:

- high degree but
    
- lower clustering than dense local cores
    

Compute:

```python
clustering_coeff
```

### Feature 8: bridge-like score

A simple derived feature:

```python
bridge_score = betweenness_centrality / max(degree, 1)
```

This is optional but useful.

### Feature 9: relative rank within protein

For each residue, compute within-protein percentile ranks for:

- RSA
    
- contacts_8A
    
- long_range_contacts
    
- betweenness
    
- n_distinct_sse_partners
    

This helps normalize across proteins.

---

## Matched-control design

This is the heart of the experiment.

For each anchor residue, sample `m = 10` matched non-anchor controls from the same protein satisfying:

- same SSE coarse type (`H`, `E`, or `C`)
    
- RSA within tolerance, e.g. `|ΔRSA| <= 0.05`
    
- contacts_8A within tolerance, e.g. `|Δcontacts_8A| <= 3`
    
- optional: same sequence-position decile
    

If too few controls exist:

- relax in this order:
    
    1. position decile
        
    2. RSA tolerance to 0.08
        
    3. contacts tolerance to 5
        

Store matched sets:

```python
(anchor_residue, [matched_control_1, ..., matched_control_m])
```

### Why this matters

This directly tests:

> among residues that are equally buried and similarly connected, what still predicts anchor status?

---

## Analyses

## Analysis 1: full-residue regression

Same spirit as v2, but with the new features.

### Model A: v2-style structural baseline

```python
proj ~ SSE + dist_to_boundary + seg_len + RSA + contacts_8A + long_range_contacts + protein_FE
```

### Model B: + integrative connectivity

```python
proj ~ ModelA
     + long_range_fraction
     + mean_contact_span
     + max_contact_span
     + n_contact_bins
     + contact_bin_entropy
     + n_distinct_sse_partners
     + contacts_outside_own_sse
     + fraction_contacts_outside_own_sse
```

### Model C: + graph features

```python
proj ~ ModelB
     + degree
     + betweenness
     + closeness
     + eigenvector
     + core_number
     + clustering_coeff
```

### Model D: + conservation subset

Run on proteins with conservation:

```python
proj ~ ModelC + conservation
```

Report:

- R²
    
- adjusted R²
    
- anchor residuals
    
- whether anchors remain >4σ outliers
    

## Analysis 2: matched anchor-vs-control comparisons

For each feature, compare anchor vs matched controls:

- paired difference
    
- paired t-test or Wilcoxon signed-rank
    
- effect size
    
- per-protein scatter / connected lines
    

This is the highest-value result.

Primary features to test:

- long_range_fraction
    
- n_contact_bins
    
- contact_bin_entropy
    
- n_distinct_sse_partners
    
- contacts_outside_own_sse
    
- betweenness
    
- clustering_coeff
    
- bridge_score
    

## Analysis 3: anchor classification

Train simple classifiers on anchor vs non-anchor.

### Setup

Use one row per residue.  
Use:

- top-k anchor label
    
- optionally balanced sampling for non-anchors
    

### Models

- logistic regression
    
- random forest classifier
    

### Evaluation

Use **leave-one-protein-out** cross-validation.

Compare these feature sets:

#### Classifier A

- RSA
    
- contacts_8A
    
- long_range_contacts
    
- SSE type
    

#### Classifier B

- A + integrative connectivity features
    

#### Classifier C

- B + graph features
    

Metrics:

- AUROC
    
- AUPRC
    
- top-k retrieval accuracy within held-out protein
    

This is important because it tests cross-protein generalization of the “universal feature.”

---

## Visualization

### Plot A: anchor vs matched controls, feature effect sizes

Horizontal bar plot of standardized effect sizes for:

- long_range_fraction
    
- n_contact_bins
    
- contact_bin_entropy
    
- n_distinct_sse_partners
    
- betweenness
    
- clustering_coeff
    
- bridge_score
    

### Plot B: projection vs selected new features

Scatter plots:

- proj vs n_distinct_sse_partners
    
- proj vs contact_bin_entropy
    
- proj vs betweenness
    

Anchor points highlighted.

### Plot C: per-protein sequence profile with top integrative features

Like v2 profile plots, but overlay:

- projection score
    
- long_range_fraction or n_distinct_sse_partners
    
- anchor markers
    

### Plot D: anchor vs matched controls connected lines

For a few proteins, show each anchor and its matched controls on:

- betweenness
    
- n_distinct_sse_partners
    
- contact_bin_entropy
    

### Plot E: leave-one-protein-out classifier performance

Bar chart or table:

- structural baseline
    
- - integrative features
        
- - graph features
        

---

## Output

- `reports/outputs/multi_protein/anchor_regression_v3.md`
    
- `reports/outputs/multi_protein/anchor_regression_v3_*.png`
    
- optional: `reports/outputs/multi_protein/anchor_regression_v3_matches.csv`
    
- optional: `reports/outputs/multi_protein/anchor_regression_v3_features.csv`
    

---

## Execution

```bash
uv run python scripts/anchor_regression_v3.py --device cuda
```

Dependencies:

```bash
uv add biopython scikit-learn networkx statsmodels scipy
```

---

## Verification / success criteria

### Strong success

After matching on RSA and contacts_8A, anchors still show consistent enrichment in one or more of:

- `n_distinct_sse_partners`
    
- `contact_bin_entropy`
    
- `long_range_fraction`
    
- `betweenness`
    
- `bridge_score`
    

### Moderate success

These features improve regression and classifier performance, but matched-control differences are weaker.

### Failure

Once matched on burial and raw contact count, anchors no longer differ from controls.

That would mean the anchor is closer to “buried contact hub” than “special integrative residue.”

---

## Notes / implementation guardrails

- Do **not** use PDB residue numbering directly as sequence index.
    
- Reuse the v2 alignment logic and verify mapping quality per protein.
    
- For graph centrality, skip proteins that produce disconnected graphs only if necessary, but degree / core / clustering should always work.
    
- Use the same anchor position source as v2 for consistency.
    
- Keep the report focused on the matched-control results, not just total R².
    

## Decision after running

If matched-control features survive strongly:

- move next to upstream mechanistic analysis / path patching
    

If they do not:

- shift attention toward family C information-hub tests
    
- structural-centrality story is probably too weak on its own
    
