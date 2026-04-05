# Upstream Circuit Discovery for L10H9 Anchor Feature

## Goal

Identify which model components (attention heads and MLPs in layers 0-9) write the anchor feature into the residual stream at the anchor position. Use the local flank masking as a natural counterfactual.

---

## Counterfactual design

### Per-protein jump thresholds

Use the existing flank recovery data in `reports/anchor_local_flank_v1_per_protein.csv` (50 proteins, radii from 5 to full).

For each protein, define:
- **R_threshold:** smallest radius where `alpha_norm >= 0.5`
- **Corrupted flank:** one radius step BELOW R_threshold (anchor signal is weak/absent)
- **Clean flank:** R_threshold itself (or one step above if R_threshold is exact boundary)

The radius schedule in the CSV is: 5, 6, 7, 8, 10, 12, 15, 20, 30, 40, 60, 80, 120, full. So "one step below" means the previous entry in this list.

Example: if protein X first crosses alpha_norm >= 0.5 at R=20, then:
- corrupted = R=15 (alpha_norm ≈ 0.1-0.3 typically)
- clean = R=20 (alpha_norm ≈ 0.5-0.7)

This gives us semantically close pairs — only a few flank residues differ. Much cleaner than a fixed R=5 vs R=40.

### Edge cases
- If alpha_norm >= 0.5 already at R=5 (very short proteins or early jumpers): use R=5 as clean, but we have no corrupted below that. Drop this protein OR use a stricter threshold (alpha_norm >= 0.7).
- If alpha_norm never reaches 0.5 even at R=full: drop this protein (anchor behavior is weak).

### Protein set
Start with the 50 proteins from the v1 flank experiment. After filtering edge cases, expect 40-45 usable proteins. This is enough for overlap analysis — the contact circuit experiment used ~30 proteins.

If we want more proteins: extend the flank sweep to additional proteins from the audit (top 100-200 by top3_mass). But this requires running the flank v1 sweep first. Only do this if 50 is underpowered.

---

## Method: Direct residual stream decomposition

The residual stream at the anchor position, before layer 10 LN, is:

```
x_anchor = emb_anchor + sum_{l=0}^{9} (attn_out[l, :, anchor] + mlp_out[l, anchor])
```

where `attn_out[l, :, anchor]` can be split by head:

```
attn_out[l, :, anchor] = sum_{h=0}^{19} attn_out[l, h, anchor]
```

Each component's contribution to the anchor score:

```
contrib[component] = component_output_at_anchor · d
```

The decomposition is exact for the residual stream (it's a sum). We then compare clean vs corrupted:

```
delta_contrib[component] = contrib_clean[component] - contrib_corrupted[component]
```

### Components
- Embedding: 1
- Attention heads: 20 heads × 10 layers = 200
- MLPs: 10 layers × 1 = 10
- **Total: 211 components**

### LayerNorm caveat
L10H9 sees x_anchor after LayerNorm, which is nonlinear. The decomposition into components is exact for the pre-LN residual stream, but the d-projection operates on the post-LN stream. In practice, LayerNorm is approximately a rescaling (divides by norm of the full vector), so the ranking of components is usually preserved. We validate this with a sanity check (see below).

### Existing infrastructure
`anchor_interp_v3.py` (Part A) already implements layerwise decomposition of anchor projection onto d. It captures per-layer attention and MLP outputs and projects onto d. Reuse this directly — the main new work is running it under two conditions (clean vs corrupted flank) and computing deltas.

---

## Metrics per component

For each component C and protein p:

1. `delta_d_proj[C, p]`: change in d-projection at anchor (clean - corrupted)
2. `frac_of_total[C, p]`: delta_d_proj / sum(all delta_d_proj). Fraction of total signal change.
3. `sign[C, p]`: positive means component helps build anchor feature in clean condition

Across proteins:
4. `mean_frac[C]`: mean fraction across proteins
5. `median_frac[C]`: median (more robust to outliers)
6. `recurrence_top10[C]`: fraction of proteins where C is in top-10 by |delta_d_proj|
7. `recurrence_top20[C]`: same for top-20
8. `sign_consistency[C]`: fraction of proteins where delta_d_proj > 0

---

## Sanity check: validate decomposition against patching

After the decomposition run, take the **top-5 components by mean_frac** and validate with activation patching:

For each top-5 component C and each protein:
1. Run clean forward pass (large flank), cache all intermediate activations
2. Run a patched forward pass: everything is clean EXCEPT component C's output is swapped to its corrupted-flank value
3. Measure: `alpha_patched = x_anchor_patched · d` (after the patching propagates through remaining layers)
4. Direct effect of C: `DE[C] = alpha_clean - alpha_patched`

Compare the ranking of top-5 by decomposition vs by patching:
- If top-5 by decomposition ≈ top-5 by patching: LN approximation is fine, trust decomposition
- If they diverge: flag the LN issue in the report, use patching ranking for those components

**Cost:** 5 patched forward passes per protein × 50 proteins = 250 forward passes. Negligible.

---

## Main analyses

### Analysis 1: Component ranking

Rank all 211 components by `mean_frac` across proteins. Report top-20.

Split into:
- Top attention heads (by mean_frac)
- Top MLPs (by mean_frac)
- Embedding contribution

Key question: is the anchor feature built primarily by attention heads or MLPs?

### Analysis 2: Attention vs MLP budget

For each protein, compute:
- Total attention contribution: sum of |delta_d_proj| over all heads
- Total MLP contribution: sum of |delta_d_proj| over all MLPs
- Embedding contribution

Report distribution across proteins.

### Analysis 3: Layer profile

For each layer (0-9), compute:
- Sum of all head contributions at that layer
- MLP contribution at that layer

Plot: stacked bar or line showing contribution by layer.

Key question: which layers matter most? Is it concentrated near layer 9, or distributed?

### Analysis 4: Recurrence / overlap analysis

For attention heads specifically:

For each protein, take the top-10 heads by |delta_d_proj|.

Compute:
- **Per-head recurrence:** fraction of proteins where each head appears in top-10
- **Pairwise protein Jaccard:** for each pair of proteins, Jaccard similarity of their top-10 head sets
- **Mean pairwise Jaccard:** overall measure of circuit consistency

Use the same approach as `circuit_head_overlap.py`.

**Outcome interpretation:**
- **(A) High recurrence** (multiple heads appear in >50% of proteins): universal upstream circuit. Report which heads and their layer/position.
- **(B) Moderate recurrence with clustering**: compute pairwise Jaccard matrix, cluster proteins (hierarchical clustering on 1 - Jaccard distance). Check if clusters correlate with protein properties (fold, length, anchor SSE type). This tests the "family-specific upstream circuit" hypothesis.
- **(C) Low recurrence** (<20% for all heads): upstream circuit is protein-specific. The anchor feature is built by diverse computations that converge to a universal detector. Report this as a finding.

### Analysis 5: Source position analysis (conditional on Analysis 4)

**Only run if reused heads are found (outcome A or B).**

For the top-3 most recurrent heads, examine which flank positions they attend to at the anchor position:

For each reused head at layer l, head h:
- Extract attention weights A_clean[l, h, anchor, :] — which source positions does this head attend to when writing to the anchor?
- Compare to A_corrupted[l, h, anchor, :] — how does attention change?
- Identify: which source positions gain the most attention in the clean vs corrupted condition?

Aggregate across proteins:
- Do reused heads consistently attend to specific RELATIVE positions in the flank?
- Or to positions with specific properties (same SSE, high contact count)?

This connects to Experiment 3 (position importance maps) as a cross-check.

### Analysis 6: Protein grouping (conditional on outcome B)

**Only run if moderate recurrence with apparent grouping.**

From the pairwise Jaccard matrix in Analysis 4:
- Hierarchical clustering
- Check if clusters correlate with:
  - Anchor SSE type (mostly strand, but some helix/coil)
  - Protein length
  - Number of SSE segments
  - SCOP/CATH fold (if available from PDB headers)

---

## Sufficiency test (optional, run if top components are clean)

If Analysis 1 identifies a compact set of top components:

Take top-k components (k = 5, 10, 20). Run a forward pass where ONLY these components use their clean-flank values, everything else uses corrupted-flank values.

Measure: what fraction of alpha_clean is recovered?

```
sufficiency[k] = alpha_top_k_clean_rest_corrupted / alpha_clean
```

This is the complement of the patching: "is this set of components ENOUGH to build the anchor feature?"

If top-10 recovers >80%: the upstream circuit is compact.
If top-20 barely recovers 50%: the computation is distributed.

---

## Outputs

- `reports/outputs/multi_protein/anchor_upstream_circuit.md`
- `reports/outputs/multi_protein/anchor_upstream_circuit_components.csv` — per-component, per-protein delta_d_proj and frac_of_total
- `reports/outputs/multi_protein/anchor_upstream_circuit_summary.csv` — aggregated ranking
- `reports/outputs/multi_protein/anchor_upstream_circuit_sanity.csv` — decomposition vs patching comparison for top-5

Plots:
1. `anchor_upstream_circuit_ranking.png` — top-20 components by mean_frac (bar chart, colored by type: attn head vs MLP)
2. `anchor_upstream_circuit_layer_profile.png` — contribution by layer (stacked: attention + MLP)
3. `anchor_upstream_circuit_attn_vs_mlp.png` — budget breakdown per protein
4. `anchor_upstream_circuit_recurrence.png` — head recurrence heatmap (layer × head, colored by recurrence fraction)
5. `anchor_upstream_circuit_jaccard.png` — pairwise protein Jaccard matrix with dendrogram
6. `anchor_upstream_circuit_sanity.png` — decomposition rank vs patching rank scatter
7. Optional: `anchor_upstream_circuit_source_positions.png` — attention heatmaps for reused heads

---

## Reuse

- Model loading: `anchor_interp_v3.py` or `anchor_behavior_audit.py`
- Search direction computation: `anchor_interp_v3.py` (`compute_search_dir`)
- Layerwise decomposition: `anchor_interp_v3.py` (Part A — already captures per-layer attn and MLP outputs projected onto d)
- Flank masking: `anchor_local_flank_v1.py` (sequence construction with masked flanks)
- Overlap analysis: `circuit_head_overlap.py`
- Per-protein threshold data: `reports/anchor_local_flank_v1_per_protein.csv`

New code needed:
1. Load per-protein thresholds from CSV, compute clean/corrupted radius pairs
2. Run decomposition under both conditions
3. Compute deltas and rankings
4. Activation patching for top-5 validation
5. Overlap analysis (reuse existing code)

---

## Script

Create: `scripts/anchor_upstream_circuit.py`

```bash
uv run python scripts/anchor_upstream_circuit.py --device cuda
```

---

## Compute estimate

- 50 proteins × 2 forward passes (clean + corrupted) = 100 forward passes for decomposition
- 50 proteins × 5 patched forward passes = 250 for sanity check
- Total: ~350 forward passes. Very fast.

Optional sufficiency test: 50 × 3 (k=5,10,20) = 150 more.

---

## Decision after running

- **Reused heads found →** examine their attention patterns (Analysis 5). What flank positions do they read? This directly feeds into Experiment 3 (position importance).
- **MLPs dominate →** the anchor feature is "retrieved" from MLP memory, not computed by attention. Could pivot to neuron-level analysis, but that's a larger effort. Report as finding.
- **Family-specific circuits →** report protein grouping. Check if it aligns with known structural classification. This is itself a contribution: "universal readout, diverse upstream computation."
- **No clean pattern →** distributed computation. The anchor feature is built incrementally by many components. Less mechanistically satisfying but honest.
