
# SAE Frozen-Error Zero-Ablation IE Ranking and Sufficiency
**File:** `experiments/3_31_anchor_sae_frozen_error_ie_v1.md`

## Goal

Test whether the public **layer-8 SAE** provides a causally useful basis for the **L10H9 anchor mechanism**, using:

1. **IE ranking** over latent-token pairs with **0 as the counterfactual**
2. **Sufficiency tests** that keep only the top-k latent-token pairs and zero-ablate everything else
3. A **frozen error node** so the SAE decomposition remains anchored to the clean forward pass

This is explicitly a **causal** test, not a geometric projection test.

---

## Main question

For proteins where L10H9 strongly behaves as an anchor head, can a small set of **layer-8 SAE latent-token pairs** preserve the downstream anchor behavior of L10H9?

If yes:
- the public layer-8 SAE gives a useful causal basis for the anchor mechanism

If no:
- the relevant information is likely distributed, lives largely outside this SAE vocabulary, or only becomes clean later than layer 8

---

## Protein set

Use the **top 50 most confident anchor proteins** from the large anchor-behavior audit.

### Confidence definition
Pick proteins with strongest evidence that L10H9 is behaving canonically:
- high projection-attention agreement
- high top-3 key mass
- positive top anchor projection

Use a simple score like:
```python
confidence = z(spearman_rho) + z(top3_key_mass) + z(top1_anchor_alpha)
````

Take the top 50 proteins after filtering for:

* `spearman_rho >= 0.95`
* `top3_key_mass >= 0.70`
* top anchor `alpha >= 0.25`

Use the same canonical top anchor definition as the recent large-scale anchor runs.

---

## Layer and decomposition

### Intervention layer

* **Layer 8 residual stream**, using the public InterProt SAE already used before

### Clean decomposition

For each token position `t` in the clean forward pass, decompose:

```python
x_t = x_latents_t + x_biasmean_t + x_error_t
```

Where:

* `x_latents_t` = decoded SAE latents at token `t`
* `x_biasmean_t` = the fixed SAE bias/mean contribution
* `x_error_t = x_t - x_hat_t`

### Critical rule

**Freeze `x_error_t` from the clean pass once per protein.**
Do not recompute error after interventions.

All interventions must use:

```python
x'_t = decode(modified_latents_t) + x_biasmean_t + x_error_t_clean
```

This keeps the error node interpretable as “the part of the original representation missed by the SAE.”

---

## Primary downstream metric

Do **not** use only projection to `d` as the main metric.

Use a downstream **L10H9 anchor-head metric**.

### Primary metric: incoming pre-softmax anchor score

For the known anchor key position `a`, define:

```python
M_score = mean_q [ (q_q · k_a) / sqrt(d_head) ]
```

Where:

* `q_q` = L10H9 query vector at query position `q`
* `k_a` = L10H9 key vector at the anchor key position `a`

Average over all residue queries.

This is the cleanest “how attractive is the anchor key to the head?” metric.

### Secondary metrics

Also record:

1. **Incoming attention mass**

```python
M_attn = mean_q A[q, a]
```

2. **Anchor key rank by incoming attention mass**

3. **Anchor key rank by incoming pre-softmax score**

4. Optional sanity metric:

   * layer-10 anchor projection `alpha_anchor = x_anchor · d`

The main conclusions should use `M_score` first, not the projection proxy.

---

## Attribution ranking

## Intervention variable

Use **post-topk SAE latent activations** as the intervention variable.

For each token `t` and latent `l`, let:

```python
a_clean[t, l]
```

be the clean post-topk activation.

### Counterfactual

The counterfactual is:

```python
a_cf[t, l] = 0
```

### IE / attribution score

Rank latent-token pairs by:

```python
IE[t, l] = a_clean[t, l] * (∂M_score / ∂a[t, l])_clean
```

This is “clean activation times gradient wrt the anchor metric,” with zero as the counterfactual.

Notes:

* Only active latent-token pairs need to be ranked, since inactive pairs have zero clean activation
* Gradients are wrt the **post-topk** activation tensor, not pre-topk logits

---

## Analyses

## Analysis 1: IE ranking summaries

For each protein:

* rank all active latent-token pairs by `IE[t, l]`
* report the top 20

Aggregate across proteins:

* which latents recur most often in top 20
* which token positions recur most often
* how much of top IE mass is concentrated at:

  * the anchor token
  * nearby tokens
  * the rest of the sequence

This tells us whether the causal support is local or distributed.

## Analysis 2: leave-one-out zero ablation

For each protein, zero-ablate one active latent-token pair at a time:

```python
a'[t, l] = 0
```

while leaving all others unchanged.

Measure drop in:

* `M_score`
* `M_attn`
* anchor rank

This validates whether the IE ranking tracks actual causal effect.

## Analysis 3: sufficiency test with top-k kept pairs

For each protein:

* keep only the top-k IE-ranked latent-token pairs
* set all other latent activations to zero
* keep `x_biasmean` and frozen `x_error_clean` unchanged

Sweep:

```python
k ∈ {1, 2, 5, 10, 20, 50, 100, 200, 500}
```

Measure:

* retained fraction of clean `M_score`
* retained fraction of clean `M_attn`
* whether anchor remains top-1 / top-3

### Suggested sufficiency thresholds

For each protein, record minimal `k` needed to achieve:

* `M_score >= 0.50 * clean`
* `M_score >= 0.80 * clean`
* `M_score >= 0.90 * clean`

Also record the same thresholds for `M_attn`.

## Analysis 4: coarse decomposition controls

Run three coarse conditions:

### A. Full clean decomposition

* original latents
* original bias/mean
* frozen clean error

### B. Latents-only

* original latents
* original bias/mean
* **error = 0**

### C. Error-only

* **all latents = 0**
* original bias/mean
* frozen clean error

This is the highest-value sanity check.

Interpretation:

* if error-only preserves most of the anchor metric, this SAE vocabulary is not causally sufficient
* if latents-only preserves little, again the SAE vocabulary is weak
* if top-k latents plus frozen error recover most of the clean metric, then the SAE latents contribute but only in the presence of frozen error

## Optional Analysis 5: anchor-token-only sufficiency

As a secondary comparison, repeat sufficiency using only active latents at the **anchor token position**.

This tests whether most causal support comes from:

* the anchor token itself
* or distributed latent-token pairs elsewhere in the sequence

This is optional but useful.

---

## Output files

* `reports/outputs/multi_protein/anchor_sae_frozen_error_ie_v1.md`
* `reports/outputs/multi_protein/anchor_sae_frozen_error_ie_v1_per_protein.csv`
* `reports/outputs/multi_protein/anchor_sae_frozen_error_ie_v1_top_pairs.csv`
* `reports/outputs/multi_protein/anchor_sae_frozen_error_ie_v1_sufficiency.csv`

Plots:

1. top-k sufficiency curves across proteins
2. histogram of minimal `k` for 50%, 80%, 90% recovery
3. coarse control bar chart: full vs latents-only vs error-only
4. heatmap of top recurring latent indices across proteins
5. token-position concentration of top IE pairs

---

## Guardrails

* Freeze the clean error node once. Never recompute it under interventions.
* Use the downstream L10H9 metric as primary, not only anchor projection.
* Rank latent-token pairs by gradient wrt **post-topk** latent activations.
* Report both mean and median across proteins, since tails may be large.
* Save enough intermediate outputs that we can inspect a few proteins manually.

---

## Expected interpretations

### Outcome A

Small `k` preserves most anchor behavior.

* public layer-8 SAE provides a compact causal basis

### Outcome B

Large `k` is needed, but top pairs help.

* layer-8 SAE has weak/distributed causal support

### Outcome C

Error-only preserves most anchor behavior, latents-only fails.

* public layer-8 SAE is the wrong explanatory basis

### Outcome D

Neither error-only nor small/large-k latent subsets preserve behavior.

* layer-8 decomposition itself is not close enough to the relevant computation

---

## Script name

Create:

* `scripts/anchor_sae_frozen_error_ie_v1.py`

---

## Execution

```bash
uv run python scripts/anchor_sae_frozen_error_ie_v1.py --device cuda
```

A small recommendation: for experiment 1, treat **incoming pre-softmax anchor score** as the primary metric and **incoming attention mass** as the secondary metric. That will make the sufficiency curves much easier to interpret.
```
