# Anchor Feature Identification (experiments/3_24_anchor_interp_v3.md)

## Context

We have identified universal anchor heads in ESM2 (L10H9, L11H16, L14H9) that appear
across 31 protein circuits for contact prediction. These heads have a **fixed search
direction** in W_Q that is consistent across proteins (cosine 0.93 for L10H9 in residual
stream space). In the correct circuit context (clean masked sequence), the anchor residue
ranks #1 among all positions on the pre-rotary content-based key score for L10H9 across
all 5 tested proteins.

**The question:** What feature in the residual stream does this search direction detect?
What makes the anchor position special?

## Previous experiments (read these for data loading patterns and variable names)

- `scripts/anchor_interp_v2.py` — Computed the search direction and anchor rankings.
  Key function: `q1_mean_query_direction()` computes `q_mean_d` (mean unit query in head
  space) and `q_search_D` = `W_Q.T @ q_mean_normalized` (search direction in residual
  stream space, shape 1280).
  Key function: `capture_post_ln_residuals()` captures post-LayerNorm residuals via
  nnsight tracing.
  Key function: `extract_head_weights()` extracts per-head W_Q, W_K, W_V, W_O.
  Key function: `load_model()` loads model via NNsight wrapping EsmForMaskedLM.
  Output: `reports/outputs/multi_protein/anchor_interp_v2.md`

- `scripts/anchor_decomp.py` — SVD analysis of W_K. Uses same model loading and
  residual stream capture patterns.
  Output: `reports/outputs/multi_protein/anchor_decomp.md`

- `scripts/interprot_sae_viz.py` — SAE loading and visualization. Contains patterns
  for loading SAE weights and computing activations. Reference this for SAE decoder
  weight loading.

## Data available

- Proteins with full circuit data: 1BRTA, 1IN4A, 1PVGA, 1YKIA, 2B61A, 2DPMA, 2EK8A,
  2FBQA, 2PKEA
- Sequences: `data/full_seq_dict.json`
- SSE assignments: `data/ss_dict.json`
- Protein configs (contact pairs, flanks): `configs/proteins.json`
- SAE weights: check `scripts/interprot_sae_viz.py` for the loading pattern and paths.
  SAEs are available for residual stream at layers 4, 8, 12, 16, 20, 24, 32.
  Each SAE has decoder directions (the dictionary vectors). The decoder weight matrix
  maps from latent space to residual stream space — each row (or column, check the code)
  is a dictionary direction `f_i` in R^1280.
- Anchor positions per protein for L10H9 (0-indexed, from corrected analysis):
  - 1BRTA: pos 220 (L)
  - 1PVGA: pos 101 (V)
  - 2B61A: pos 315 (T)
  - 2DPMA: pos 39 (F)
  - 2PKEA: pos 131 (L)

## Primary target head

**L10H9** — this head has the cleanest results:
- Anchor is rank 1 in all proteins (masked and full-seq)
- Search direction cosine across proteins: 0.93
- Key norm Z-score: 5.50 (anchors are extreme outliers)
- Cross-protein anchor key similarity: p = 6e-6

Also run for L11H16 and L14H9 if time permits, but L10H9 is the priority.

## Part A: Layer-wise decomposition of anchor projection score

### Goal

Determine which model components (embedding, attention heads, MLPs at each layer)
contribute to the anchor position's high projection onto the search direction. This tells
us *where* the feature is computed.

### Method

1. **Compute the search direction** for L10H9 using the same method as
   `anchor_interp_v2.py`:
   - Load model, extract W_Q for L10H9 (layer=10, head=9)
   - For each protein, run forward pass on the **clean masked sequence** (use the masking
     logic from the circuit pipeline — mask everything except the unmasked flanked
     segments and jump residues, using clean_flank from protein config)
   - Compute all query vectors, take mean unit query direction `q_mean_d`
   - Compute search direction: `search_dir = W_Q.T @ (q_mean_d / ||q_mean_d||)`,
     shape (1280,)
   - **Use the search_dir from 2B61A as the reference** (or average across proteins since
     they're cosine 0.93 similar — either works, just be consistent and document choice)

2. **Decompose the residual stream at the anchor position** through layers 0–9:
   The residual stream is built up as:
   ```
   x_0 = token_embedding + position_embedding  (ESM2 doesn't use learned pos embed
          but check — it has a learned position embedding up to max_position)
   x_after_L0 = x_0 + attn_out_L0 + mlp_out_L0
   x_after_L1 = x_after_L0 + attn_out_L1 + mlp_out_L1
   ...
   ```

   For each layer L from 0 to 9, capture:
   - The attention output at the anchor position: `attn_out_L[anchor_tok_pos]`
   - The MLP output (FFN) at the anchor position: `mlp_out_L[anchor_tok_pos]`

   **How to capture these with nnsight:**
   ESM2 architecture (per layer):
   ```
   residual -> LayerNorm -> SelfAttention -> + residual -> LayerNorm -> FFN -> + residual
   ```
   This is post-norm / sandwich norm. Check the exact architecture by inspecting:
   `model._model.esm.encoder.layer[0]` to see the module structure.

   The attention output (before adding to residual) should be accessible as:
   `model.esm.encoder.layer[L].attention.output.dense` (the final linear in attn)
   or the full attention block output including the residual connection.

   The FFN output (before adding to residual):
   `model.esm.encoder.layer[L].output.dense` or similar.

   **IMPORTANT:** You need the *additive contribution* of each component to the residual
   stream, not the residual stream after each component. That is:
   - `attn_contribution_L = attention_output_L` (what gets added to the residual)
   - `mlp_contribution_L = ffn_output_L` (what gets added to the residual)

   Use `tracer.cache()` to capture these. Refer to `anchor_decomp.py` and
   `anchor_interp_v2.py` for the nnsight tracing pattern. You may need to inspect the
   model architecture first:
   ```python
   for name, module in model._model.esm.encoder.layer[0].named_modules():
       print(name, type(module))
   ```

3. **Compute per-component projection scores:**
   ```python
   # search_dir: (1280,)
   # anchor_tok_pos: seq_pos + 1 (for BOS offset)

   score_embed = dot(embedding[anchor_tok_pos], search_dir)

   for L in range(10):
       score_attn_L = dot(attn_contribution_L[anchor_tok_pos], search_dir)
       score_mlp_L = dot(mlp_contribution_L[anchor_tok_pos], search_dir)

   # Verify: score_embed + sum(score_attn) + sum(score_mlp) ≈ total projection
   # (may not be exact due to layernorm — document any discrepancy)
   ```

4. **Also compute the same decomposition for a non-anchor position** (e.g., a random
   unmasked residue that ranks low on the search direction) as a control. This shows
   which components are anchor-specific vs. shared.

### Output

- Per-protein bar chart: x-axis = component (embed, attn_L0, mlp_L0, attn_L1, ...),
  y-axis = projection onto search direction. One bar series for anchor, one for control.
- Table: protein × component → projection score
- Summary: which components contribute most to the anchor's high projection?
  Is it consistent across proteins?
- Save to `reports/outputs/multi_protein/anchor_layerwise_decomp.md`

## Part B: SAE latent alignment with search direction

### Goal

Find SAE latents whose decoder directions align with the L10H9 search direction. These
latents represent *interpretable features* that the search direction detects.

### Method

1. **Load the search direction** (same as Part A — the 1280-dim vector `search_dir`).

2. **Load SAE decoder weights** for layers 4 and 8.
   - Check `scripts/interprot_sae_viz.py` for the SAE loading pattern. The SAEs should
     have a decoder weight matrix where each column (or row — verify orientation) is a
     dictionary direction in R^1280.
   - The decoder matrix shape is typically (n_latents, hidden_dim) or
     (hidden_dim, n_latents). Verify by checking the loaded weights.
   - Each decoder direction `f_i` should be unit-normalized (or normalize it).

3. **Compute alignment scores:**
   ```python
   # decoder_dirs: (n_latents, 1280) — each row is a latent direction
   # search_dir: (1280,)
   search_dir_unit = search_dir / search_dir.norm()
   alignment = decoder_dirs @ search_dir_unit  # (n_latents,)
   top_k = alignment.topk(20)  # top 20 most aligned latents
   bottom_k = alignment.topk(20, largest=False)  # most anti-aligned
   ```

4. **For each top-aligned latent, report:**
   - Latent index
   - Cosine similarity with search direction
   - Top activating proteins/positions from existing cached activations
     (if available in the SAE viz pipeline)
   - Any existing labels or annotations for the latent

5. **Compare layer 4 vs layer 8:**
   - Which latents appear in top-20 at both layers? (shared = feature exists early)
   - Which only at layer 8? (computed between layers 4–8)
   - This directly complements the layer-wise decomposition from Part A.

6. **Activation check on anchor positions:**
   For the top-5 aligned latents at layer 8, run the SAE encoder on the residual stream
   at the anchor positions across proteins. Do these latents actually fire on the anchor?
   If a latent aligns with the search direction AND fires strongly on anchor positions,
   that's strong evidence it represents the feature L10H9 selects for.
   ```python
   # For each protein, get residual stream at layer 8 for anchor position
   # Run through SAE encoder
   # Check activation of top-aligned latents
   ```

### Output

- Table: top 20 aligned latents at layer 8, with cosine score and top activating
  positions
- Table: top 20 aligned latents at layer 4, same format
- Comparison of which latents overlap between layers
- For top-5 latents: do they fire on anchor positions? Table of latent × protein →
  activation value at anchor position
- Save to `reports/outputs/multi_protein/anchor_sae_alignment.md`

## Execution

```bash
uv run python scripts/anchor_interp_v3.py --device cuda
```

Create a single script `scripts/anchor_interp_v3.py` that runs both Part A and Part B.
Reuse data loading patterns from `scripts/anchor_interp_v2.py` and SAE loading from
`scripts/interprot_sae_viz.py`.

Estimated runtime: ~30 min (forward passes for residual stream capture across 5 proteins
× 10 layers, plus SAE computations).

## Verification

1. Part A sanity check: sum of all component projections should approximately equal the
   total residual stream projection at the anchor position (pre-LayerNorm of layer 10).
   Document the gap — it may be nonzero due to LayerNorm but should be in the right
   ballpark.
2. Part B sanity check: the top-aligned latent should have cosine > 0.3 with the search
   direction (if all cosines are < 0.1, the feature is not captured by any single SAE
   latent, which is itself informative).
3. Cross-reference: if Part A says "MLP layers 5-8 contribute most" and Part B says
   "layer 8 SAE has aligned latents that layer 4 doesn't," the stories should be
   consistent.