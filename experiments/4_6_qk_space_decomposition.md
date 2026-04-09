# QK Space Decomposition for L10H9

## Motivation

We've been classifying anchors using handcrafted structural features projected from PDB data. The best linear model (H4) reaches AUPRC 0.49; GBT reaches 0.73 with nonlinear interactions we can't interpret. Instead of engineering more features, look at what L10H9's QK circuit itself encodes — in its own representation space.

Inspired by Lee et al. 2026 ("Decomposing Query-Key Feature Interactions Using Contrastive Covariances"). We adapt their key-space visualization and contrastive covariance approach to a protein transformer attention head.

---

## Protein set

Use the ~2000 proteins from the behavior audit (`reports/anchor_behavior_audit.md`). Filter to "confident" proteins: those where the top-1 residue gets >50% of L10H9 attention mass (~62% of proteins, so ~1200+). This ensures the anchor is clearly defined.

---

## Analysis 1: Key-space visualization

### What
For each confident protein, extract L10H9's key vectors for ALL residues (not just the anchor). The key vector for position $j$ is:

```
k_j = W_K @ x_j   # x_j is the residual stream entering layer 10 at position j
```

This is the FULL key vector in head space ($\mathbb{R}^{d_{head}}$), NOT the scalar projection $d^\top x_j$ we've been using. The scalar projection collapses all key-space structure to 1D. The full key vector preserves it.

### Procedure
1. Run ESM2 on each protein, extract residual stream at layer 10 input for all positions
2. Compute $k_j = W_K @ x_j$ for all positions $j$ (dimension: $d_{head} = 64$ for ESM2-650M)
3. Collect key vectors across all proteins. Label each with:
   - is_anchor (binary: top-1 attention position for that protein)
   - SSE type (H/E/C)
   - RSA bin (buried <0.05, intermediate 0.05-0.25, exposed >0.25)
   - contacts_8A bin (low/med/high terciles)
   - protein ID
4. PCA on the full key-vector collection. Plot PC1 vs PC2, PC1 vs PC3
5. Color by: (a) anchor vs non-anchor, (b) SSE type, (c) RSA bin, (d) contacts bin

### Key questions
- Do anchor keys form a single tight cluster, or multiple subclusters?
- If subclusters exist, do they align with SSE type? burial? contact topology?
- How much of the key-space variance does the anchor/non-anchor distinction explain?
- Is the anchor cluster elongated (suggesting a continuum) or round (suggesting a discrete type)?

### Important: also project queries
Compute $q_j = W_Q @ x_j$ for all positions. Project onto the same PCA axes (or do separate PCA). This shows:
- How aligned are queries across positions (confirming rank-1 query)?
- Do queries from different proteins overlap?
- Is there meaningful query variation that correlates with anything?

---

## Analysis 2: Contrastive covariance with structural features as $z_1$

### What
For a chosen binary structural feature $z_1$ (e.g., buried vs exposed), construct:
- $k^+$: key vectors where $z_1 = 1$
- $k^-$: key vectors where $z_1 = 0$

Compute:
```
ΔC(z₁) = E[q k^T | z₁ match] - E[q k^T | z₁ mismatch]
```

Since queries are ~constant, simplify: just look at the key-side structure:
```
Δk(z₁) = E[k | z₁=1] - E[k | z₁=0]
```

And compute the full covariance matrices:
```
Σ_k(z₁=1) = Cov[k | z₁=1]
Σ_k(z₁=0) = Cov[k | z₁=0]
```

The difference in covariance structure tells you how the key-space geometry changes with $z_1$.

### Candidate $z_1$ features (all binary)
1. **anchor vs non-anchor** (the obvious one)
2. **buried vs exposed** (RSA < 0.05 vs > 0.25)
3. **high contacts vs low contacts** (top vs bottom tercile of contacts_8A)
4. **helix vs strand** (SSE type)
5. **high long-range fraction vs low** (top vs bottom tercile)
6. **high $\alpha_{norm}$ vs low** ($d$-projection > 0.5 vs < 0)

For each $z_1$:
- Compute $\Delta k(z_1)$ — the mean key difference
- Compute cosine similarity between $\Delta k(z_1)$ and $d$ (the known search direction in key space). If $\Delta k \parallel d$, then $z_1$ is what $d$ detects.
- Compute explained variance: what fraction of the anchor-vs-non-anchor key variance does $z_1$ explain?

### Key question
Which structural $z_1$ produces the $\Delta k$ most aligned with $d$? This directly tells us: in the model's own key space, which structural property best explains the direction the head searches along?

---

## Analysis 3: Key-space rank and subspace structure

### What
Go beyond mean differences. Look at the full covariance structure of anchor keys.

### Procedure
1. Collect key vectors for ALL anchor positions across confident proteins (~1200 vectors in $\mathbb{R}^{64}$)
2. Compute covariance matrix $\Sigma_{anchor} \in \mathbb{R}^{64 \times 64}$
3. Eigendecomposition. How many eigenvalues are significant?
   - If rank ~1: anchors vary along a single direction in key space (the feature is 1D)
   - If rank 2-5: there are anchor subtypes encoded in distinct key-space dimensions
   - If rank >>5: the anchor property is diffuse/not cleanly encoded in key space
4. Same for non-anchor keys: $\Sigma_{non-anchor}$
5. Compare eigenspectra. Do anchors have a tighter or more structured covariance?

### Subspace overlap
Compute the principal subspaces of anchor keys (top-k eigenvectors of $\Sigma_{anchor}$) and check:
- Does the top-1 eigenvector align with $d$?
- Do top-2 through top-5 eigenvectors correlate with structural properties (SSE, burial, contacts)?
- Grassmann distance between anchor and non-anchor subspaces

---

## Implementation

### Script: `scripts/qk_space_decomposition.py`

```bash
uv run python scripts/qk_space_decomposition.py --device cuda --n-proteins 1200
```

### Dependencies
- ESM2-650M (already available)
- The behavior audit CSV for protein list + anchor positions
- PDB features (RSA, contacts, SSE) for structural labels — reuse from v3/v4

### Outputs
- `reports/outputs/multi_protein/qk_decomposition.md` — main results
- `reports/outputs/multi_protein/qk_key_pca.png` — Analysis 1 key PCA
- `reports/outputs/multi_protein/qk_query_pca.png` — Analysis 1 query PCA
- `reports/outputs/multi_protein/qk_contrastive_alignment.png` — Analysis 2 bar chart (cosine of each Δk with d)
- `reports/outputs/multi_protein/qk_eigenspectrum.png` — Analysis 3 eigenspectra
- `reports/outputs/multi_protein/qk_subspace_correlations.csv` — eigenvector vs structural property correlations

### Compute estimate
- ~1200 proteins × 1 forward pass each = ~1200 forward passes (ESM2-650M, ~30 min on GPU)
- PCA/covariance on ~200K key vectors in R^64 — trivial
- Total: ~30-40 min

---

## What success looks like

### Best case
Anchor keys form 2-3 visible subclusters in PCA that correspond to structural contexts (e.g., helix-junction anchors vs strand-bridge anchors). The contrastive covariance for one structural property (e.g., contact topology) aligns strongly with $d$ (cosine > 0.8). The eigenspectrum reveals rank 2-3, with eigenvectors mapping to nameable structural features.

→ We can finally say "d detects X" in the model's own language, and the subtypes explain the nonlinearity.

### Good case
Anchor keys form a single cluster but clearly separated from non-anchors. The contrastive $\Delta k$ for burial aligns with $d$ but doesn't fully explain it — a second structural property (e.g., contact diversity) explains the residual. Eigenspectrum is rank 1-2.

→ Confirms monosemanticity, identifies the primary feature as burial-related but with a secondary component.

### Informative negative
Anchor keys are NOT clearly separated from non-anchors in PCA (the separation is only along $d$, which is rank-1). No structural $z_1$ aligns well with $d$.

→ The anchor feature is truly a novel concept not reducible to known structural properties, even in the model's own representation. This is still a publishable finding — it means the model has learned something genuinely new.

---

## Relation to prior work

This is complementary to the flank classification (Exp 1). That asked "can we PREDICT anchors from structural features?" This asks "what does L10H9's QK circuit ENCODE about anchors?" The classification approach works in external feature space; this works in the model's internal representation space. They should converge if the model encodes the same features we're testing.

The key insight from Lee et al.: "It is when features in keys and queries align in these low-rank subspaces that high attention scores are produced." For L10H9, we know the query subspace is rank-1. This experiment characterizes the key subspace.
