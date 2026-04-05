# Anchor Flank Position Importance Maps

## Goal

For each anchor, determine which positions in the local ±30 flank are most important for constructing the anchor signal. Produce per-protein importance curves that can be compared and clustered across proteins.

This directly asks: "what is the model reading from the flank to decide anchorhood?"

---

## Motivation

We know:
- The anchor feature requires ±20-30 residues of local context (flank masking v1)
- There is no simple static motif once burial is controlled (flank classification v2)
- The search direction d is universal — the QUESTION is the same across proteins

If the question is the same, but the answer (which residues are selected) varies, then what drives the selection must live in how d interacts with each protein's local context. The importance map captures this: which positions in the flank contribute to the anchor's d-projection?

We tried clustering on r_i (orthogonal to d) in the subtype discovery experiment — that found noise (PCA at 28.8%, one mega-cluster of 986/1050). That was the wrong object. Importance maps are the right object because they capture the d-RELEVANT information from the flank, not the protein-specific residual.

---

## Method

### Approach A: Leave-one-out masking (primary)

For each anchor with its full flank (R=30):

1. Compute baseline: alpha_full = x_anchor . d with full flank visible
2. For each position j in [anchor-30, anchor+30], j != anchor:
   - Mask position j (replace with `<mask>` token)
   - Forward pass
   - Compute alpha_j = x_anchor . d
   - Importance: I(j) = alpha_full - alpha_j

This gives an importance curve I(j) of length 60 (or 61 including anchor) for each protein.

**Cost:** 60 forward passes per protein. For 100 proteins = 6000 forward passes. For 500 proteins = 30,000. Start with 100, extend if patterns emerge.

**Normalization:** Normalize each curve by alpha_full so that I_norm(j) = I(j) / alpha_full. This makes curves comparable across proteins with different anchor strengths.

### Approach B: Gradient-based importance (faster alternative)

Instead of leave-one-out, compute:

```
I_grad(j) = (d x_anchor / d input_embedding_j) . d
```

This is the gradient of the anchor's d-projection with respect to each input position's embedding. Can be computed in a single backward pass per protein.

**Advantages:** 1 forward + 1 backward per protein instead of 60 forward passes.
**Disadvantages:** gradient-based attribution can be noisy and may not match the actual leave-one-out effect (nonlinearities in attention).

**Recommendation:** Run Approach A as primary. Use Approach B as a fast sanity check on 500 proteins. If they correlate well, use B for the large-scale analysis.

---

## Protein set

**Primary:** top 100 high-confidence proteins (same as upstream circuit experiment).
**Extended (with Approach B):** top 500.

---

## Analyses

### Analysis 1: Average importance profile

Align all importance curves by the anchor position (j=0) and compute:
- Mean importance at each relative position
- Median importance
- Std / IQR

Key question: is there a universal spatial pattern? E.g., do nearby positions matter more? Is there a characteristic decay length?

### Analysis 2: Importance vs structural properties

For each (protein, flank position j), annotate:
- Sequence separation from anchor
- Same SSE as anchor? (yes/no)
- SSE type of position j
- RSA of position j
- In 3D contact with anchor? (yes/no)
- AA class of position j

Then test:
- Are positions in 3D contact with the anchor more important?
- Are positions in the same SSE more/less important?
- Are buried positions in the flank more important?
- Do specific AA classes at specific relative positions have high importance?

This is the most informative analysis for understanding what the flank provides.

### Analysis 3: Importance curve clustering

Cluster the 100 normalized importance curves.

Methods:
- Hierarchical clustering on L2 distance between curves
- PCA on the 100 x 60 importance matrix, then UMAP + HDBSCAN

Check whether clusters correlate with:
- Anchor SSE type (strand vs helix vs coil)
- Protein fold / domain family (SCOP/CATH if available)
- Number of SSE transitions in the flank
- Anchor burial level

**Key possible outcomes:**
- **(A) Clusters by fold family:** the model uses different flank information for different protein families. The universal question has family-specific answers.
- **(B) Clusters by local structure type:** e.g., "strand-in-sheet" anchors use different flank positions than "helix-in-bundle" anchors. The question adapts to local topology.
- **(C) Universal decay pattern with no clustering:** importance drops off smoothly with distance, same for all proteins. The model uses a generic "nearby context" strategy.
- **(D) Sparse, idiosyncratic patterns that don't cluster:** each protein uses a unique flank subset. Hardest to interpret.

### Analysis 4: Importance at the jump radius

From flank masking v1, each protein has a "jump radius" where the anchor signal recovers sharply. Does the importance map concentrate at or near that radius?

For each protein:
- Sum importance for positions within [jump_radius - 5, jump_radius + 5]
- Compare to importance outside that range
- Is the importance concentrated at the jump boundary?

This tests whether the jump happens because a SPECIFIC position becomes available, or because enough cumulative context is reached.

### Analysis 5: Connection to upstream circuit (if Experiment 2 runs first)

If the upstream circuit experiment finds reused heads, check:
- Do the top upstream heads attend to the same flank positions that have high importance?
- Source position analysis from the circuit experiment and importance maps should converge.

This is a cross-validation between Experiments 2 and 3.

---

## Controls

### Control 1: Non-anchor position importance
For each protein, pick a matched non-anchor control. Run the same leave-one-out sweep centered on the control position. The importance profile should be flatter / less structured.

### Control 2: Random direction importance
Instead of d, use a random unit vector d_rand in residual stream space. Run importance maps. The importance should be much weaker and less structured.

These controls verify that the importance maps reflect anchor-specific computation, not generic positional effects.

---

## Outputs

- `reports/outputs/multi_protein/anchor_position_importance.md`
- `reports/outputs/multi_protein/anchor_position_importance_curves.csv` (per-protein, per-position)
- `reports/outputs/multi_protein/anchor_position_importance_summary.csv`

Plots:
1. `anchor_position_importance_mean_profile.png` — average importance curve with error bands
2. `anchor_position_importance_examples.png` — 6-8 example proteins showing individual curves with SSE annotations
3. `anchor_position_importance_structural.png` — importance vs contact/SSE/burial annotations
4. `anchor_position_importance_clusters.png` — UMAP/dendrogram if clusters found
5. `anchor_position_importance_jump_link.png` — importance concentration vs jump radius

---

## Reuse

- Model loading, search direction: from `anchor_interp_v3.py`
- Flank masking infrastructure: from `anchor_local_flank_v1.py`
- PDB features for position annotation: from `anchor_regression_v3.py`
- Protein selection: from `anchor_behavior_audit.csv`

The main new code is:
1. Leave-one-out loop over flank positions
2. Importance curve analysis and clustering

---

## Script

Create: `scripts/anchor_position_importance.py`

```bash
uv run python scripts/anchor_position_importance.py --device cuda --n-proteins 100
```

Optional: `--approach gradient` for Approach B on 500 proteins.

---

## Relationship to the other two experiments

- **Experiment 1 (flank classification)** asks: can handcrafted features in the flank predict anchorhood? (Static pattern question)
- **Experiment 2 (upstream circuit)** asks: which model COMPONENTS build the anchor feature? (Circuit question)
- **This experiment** asks: which INPUT POSITIONS does the model use? (Input attribution question)

These are complementary:
- If Exp 1 finds a motif → importance maps should show it concentrates at the motif positions
- If Exp 2 finds reused heads → their attention should align with importance maps
- If Exp 1 finds nothing → importance maps might still show structure (the model uses nonlinear features of specific positions that handcrafted features miss)
- Importance maps on their own can reveal clustering by fold/structure even if the flank classifier fails

The importance maps are the most direct way to bridge "the model needs ±25 residues" to "the model uses THESE specific residues for THESE reasons."

---

## Decision after running

- If clean clusters by fold/structure → the paper can say "universal readout, structure-adapted input selection"
- If importance concentrates on 3D contacts in the flank → the model is detecting local structural topology
- If importance concentrates on SSE boundaries → the model reads SSE context
- If importance is diffuse/unclustered → the model uses a distributed, nonlinear encoding of local context (confirms the "novel learned concept" angle, but less mechanistically satisfying)
