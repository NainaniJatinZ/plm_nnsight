
# Anchor Local Flank Reconstruction Analysis
**File:** `experiments/3_31_anchor_local_flank_v1.md`

## Goal

Test whether the universal anchor signal for L10H9 can be reconstructed from **local sequence context around the anchor**, by masking everything except an anchor-centered local window and then gradually expanding that visible flank.

This is the anchor analogue of a jump-style context sweep.

---

## Main question

If we keep only the anchor-centered local window visible and mask the rest of the sequence:

1. Does the anchor’s projection onto the original universal search direction `d` collapse?
2. Does L10H9 stop ranking the original anchor as a special key?
3. As the visible flank grows outward, do these metrics rise gradually or show a sudden jump?

---

## Protein set

Use the same **top 50 most confident anchor proteins** as in the SAE experiment.

For each protein:
- use the canonical top anchor position `a`
- use the same universal search direction `d` from the reference setup already used in previous analyses

---

## Sequence construction

Start from the full native sequence.

For each protein and each flank radius `R`, create a masked sequence where:
- residues in `[a-R, a+R]` are left visible
- all other residues are replaced with `<mask>`

### Important
Track the **original anchor position `a`** across all masked variants.

We are not asking “what becomes top-ranked under masking?”  
We are asking whether the original anchor signal reappears as context is restored.

---

## Flank schedule

Use base visible radius 5, then expand outward.

Recommended schedule:
```python
R ∈ {5, 6, 7, 8, 10, 12, 15, 20, 30, 40, 60, 80, 120, full}
````

Cap by protein length.

This gives:

* fine resolution near the expected transition
* broader coverage at large radii

Optional denser schedule for short proteins:

```python
R ∈ {5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, full}
```

---

## Metrics

For each radius `R`, compute the following at the **original anchor position `a`**.

## Metric 1: anchor projection to the universal direction

At the relevant layer-10 LN residual vector:

```python
alpha_R = x_a^(R) · d
```

Also record:

* anchor rank by projection
* normalized `alpha_R / alpha_full`

## Metric 2: incoming pre-softmax anchor score

Primary head metric:

```python
score_R = mean_q [ (q_q · k_a) / sqrt(d_head) ]
```

Also record:

* rank of anchor key by incoming pre-softmax score
* normalized `score_R / score_full`

## Metric 3: incoming attention mass

```python
attn_R = mean_q A[q, a]
```

Also record:

* anchor key rank by incoming attention mass
* normalized `attn_R / attn_full`

## Metric 4: top-k overlap sanity

Compare the original full-sequence top keys to the top keys under radius `R`:

* top-1 overlap
* top-3 overlap

This checks when the original anchor configuration reappears.

---

## Main analyses

## Analysis 1: per-protein recovery curves

For each protein, plot metric vs radius:

* `alpha_R`
* `score_R`
* `attn_R`

Normalize by full-sequence values to compare across proteins.

## Analysis 2: threshold radii

For each metric and protein, record the smallest radius where:

* metric reaches 25% of full
* metric reaches 50% of full
* metric reaches 80% of full
* metric reaches 90% of full

This gives a compact summary of context requirements.

## Analysis 3: jump detection

We want to test whether recovery is:

* smooth
* or jump-like

For each protein and metric:

1. compute discrete increments:

```python
delta_R = metric(R_next) - metric(R)
```

2. record the largest jump and its radius
3. compare the largest jump to the median increment

Also fit:

* a simple linear recovery model
* a two-segment piecewise linear model with one changepoint

Record whether the piecewise model substantially improves fit.

We do **not** need elaborate statistics here. This is mainly descriptive:

* where does recovery happen?
* is there often a sharp transition?

## Analysis 4: aggregate recovery

Across proteins, plot:

* median normalized recovery curve
* interquartile range
  for `alpha_R`, `score_R`, and `attn_R`

This gives the “typical” anchor flank dependence.

---

## Optional sanity control

For each protein, choose one matched non-anchor control position `c` and run the same sweep.

Then compare:

* recovery of the true anchor position
  vs
* recovery of the matched control

This tests whether the effect is anchor-specific rather than a generic consequence of local unmasking.

This is optional. Run it only if compute stays reasonable.

---

## Key interpretations

### Outcome A: sharp recovery / jump

If `alpha_R`, `score_R`, and `attn_R` remain near zero for small flanks and then jump sharply:

* anchor selection depends on a finite local context threshold
* this would be directly analogous to the jump-style story, but centered on the anchor itself

### Outcome B: smooth recovery

If metrics increase steadily with radius:

* anchorhood is built cumulatively from local context
* less evidence for a sharp anchor-context threshold

### Outcome C: projection recovers before attention

If `alpha_R` rises before `score_R` / `attn_R`:

* the local representation at the anchor is being built first
* L10H9 only later acts on it once enough sequence context is restored

### Outcome D: attention recovers before projection

This would be surprising and should trigger manual inspection

---

## Output files

* `reports/outputs/multi_protein/anchor_local_flank_v1.md`
* `reports/outputs/multi_protein/anchor_local_flank_v1_per_protein.csv`
* `reports/outputs/multi_protein/anchor_local_flank_v1_thresholds.csv`

Plots:

1. per-protein recovery curves for a subset of representative proteins
2. aggregate median recovery curves with IQR
3. histogram of threshold radii
4. histogram of detected jump radii
5. optional anchor-vs-control recovery comparison

---

## Guardrails

* Always track the **original anchor position**, not whichever position becomes top-ranked after masking.
* Use the same canonical universal direction `d` as previous experiments.
* Keep BOS/EOS handling consistent with earlier scripts.
* Normalize recovery metrics by the full-sequence value from the same protein.
* Report proteins where the anchor signal never meaningfully recovers before full context.

---

## Script name

Create:

* `scripts/anchor_local_flank_v1.py`

---

## Execution

```bash
uv run python scripts/anchor_local_flank_v1.py --device cuda
```
\