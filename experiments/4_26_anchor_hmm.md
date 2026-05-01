# 4_26 Anchor HMM / Locality vs Domain-Coordinate

Central question: is ESM2 L10H9 anchoring better explained by (a) a Pfam/HMM domain coordinate, (b) a local structural feature inferable from the anchor window (3Di-like), or (c) neither — a more abstract learned landmark.

This spec replaces the previous draft. It reuses existing infrastructure rather than reinventing it, fixes vague controls, and pre-registers outcome interpretations so each experiment forces a discriminating result.

## Background already established (do not redo)

- L10H9 has vertical attention concentrated on 1–3 anchor residues. `top1_mass` median ≈ high, `top3_mass` median 0.878 across 1982 proteins (`reports/outputs/multi_protein/anchor_behavior_audit.csv`).
- Anchor identity = argmax of d-projection on L10 LayerNorm output, where d = W_K^T @ q_mean. Spearman vs true L10H9 attention ≈ 0.96. Function: `get_projection_at_anchor` and `compute_search_dir` in `scripts/anchor_flank_clustering_v2.py`.
- Recovery curves (α_norm vs flank R) and R_50 already defined in `anchor_flank_clustering_v2.py`. R_50 = smallest R where α_norm ≥ 0.5.
- Structural transfer: at the structurally aligned anchor column, 3Di IC ≈ 4.32 bits (saturated) while AA IC ≈ 3 bits, mean flank seq identity 0.064 yet ESM flank embedding cosine 0.90. Outputs in `reports/out2/structure_anchor_transfer_v2/` (1PVGA, 2B61A homolog groups).
- Embedding-based clustering of anchor flanks (mean L10 LN, anchor-only L10 LN) was tried and failed: cosine 0.9+ across all proteins, no structure vs sequence id, BLOSUM62, RSA, contacts, SSE. PCA on K_anchor and OV outputs also failed (|rho|<0.2 vs scalar structural features). Scripts: `scripts/anchor_flank_clustering.py`, `scripts/anchor_flank_clustering_v2.py`, `scripts/qk_anchor_pca.py`, `scripts/ov_output_pca.py`. Do not repeat with the same representations.

## Shared protein set

P50 = top 50 chains from `reports/out2/esm2_3b_flank_sweep/esm2_3b_flank_sweep_summary.csv` filtered by `jump_found = True` and `top3_mass ≥ 0.8` (cross-joined with `reports/outputs/multi_protein/anchor_behavior_audit.csv`), ranked by `max_jump_delta` descending.

All three experiments use P50. Where homolog groups are needed (Experiment 3) extend with the existing 1PVGA and 2B61A structural-homolog sets.

PDB structures: `data/pdb/`. 3Di tokens: `data/foldseek/all_3di.fa` for the full set, `data/foldseek/v2/v2_3di.fa` for transfer set. Per-residue features (RSA, SSE) computed from the PDB on the fly; reuse the loaders already present in `scripts/scramble_experiment.py` and `anchor_flank_clustering_v2.py`.

## Experiment 0 — Granular flank sweep (prerequisite)

The current sweep ran at step=4 (`--batch-size 4` in `scripts/esm2_3b_flank_sweep.py`). For per-protein local windows we need step=1, since the jump can be a 1-residue effect.

- Set: P50.
- Sweep R = 0..40, step 1. Drop max-flank from 60 to 40 — the existing CSV shows almost all jumps below R=35, so 40 is safe.
- For each protein record: α_norm(R) curve, R_50, jump location R* (max single-step Δα_norm), jump magnitude.
- Output: `reports/out2/anchor_flank_sweep_step1/per_protein.csv`, plus α_norm-vs-R plots.

Reuse `scripts/esm2_3b_flank_sweep.py` with `--batch-size 1 --max-flank 40`.

R_50 from this sweep is the local window for Experiment 2 and the centering radius for Experiment 3. Without this, "local window" is hand-waved.

## Experiment 1 — Within-family Pfam-coordinate concentration

Reframed. The original "do anchors land on canonical Pfam columns" is near-tautological because Pfam IC peaks are correlated with burial and SSE. The discriminating question is within-family:

> Within proteins sharing a Pfam, do anchors map to the same HMM match-state, more concentrated than residues matched on burial/SSE drawn from the same proteins?

This separates a domain-coordinate hypothesis from a "buried/secondary-structure detector" hypothesis.

Procedure:
1. Run `scripts/interpro_hmm_annotate.py` on each P50 chain. Output: per-chain Pfam hits and `pyhmmer.hmmalign` mapping seq-pos → HMM match-state.
2. Keep Pfams F with ≥ 5 P50 proteins where the anchor falls inside the Pfam span. If fewer than 3 such Pfams exist, report n and stop — the experiment is underpowered and should not be over-interpreted.
3. For each F:
   - Anchor distribution: list of HMM match-states across the proteins in F.
   - Three matched-control distributions, one residue per protein, drawn from the same proteins:
     - random in-domain residue
     - residue with RSA within ±0.05 of anchor RSA (buried-matched)
     - residue with same SSE (H/E/L) as anchor (SSE-matched)
   - Sample each control 200×; report mean entropy and 95% CI.
4. Compute normalized entropy H_norm = H / log(M) where M = number of HMM match-states in F. Also compute top-1 and top-3 state concentration.

Pre-registered outcomes:
- H_anchor < H_random_in_domain AND H_anchor < H_buried_matched AND H_anchor < H_SSE_matched, in a majority of qualifying Pfams → genuine domain-coordinate signal beyond burial/SSE.
- H_anchor < H_random_in_domain but H_anchor ≈ H_buried_matched (or H_SSE_matched) → the head is detecting a burial/SSE-class feature, not a domain coordinate. Burial-matched control is the discriminator.
- H_anchor ≈ H_random_in_domain → no Pfam-coordinate alignment; anchoring is sub-domain (e.g., a fold landmark not captured by Pfam IC).

Outputs:
- `reports/out2/anchor_hmm/anchor_hmm_mapping.tsv`
- `reports/out2/anchor_hmm/per_pfam_entropy.csv` with anchor + 3 control entropies and CIs.
- One paired-bar plot per Pfam, anchor vs three controls.

Stat test: per-Pfam permutation test (anchor vs each control) and a meta-test across Pfams (sign test on which control wins).

Caveat to note in the writeup: Pfam HMMs are AA HMMs. The structural-transfer result already shows AA IC at the anchor is moderate (≈3 bits) while 3Di IC is saturated (≈4.32 bits). So the prior expectation is closer to the burial-matched or SSE-matched outcome than to the strong domain-coordinate outcome. A strong-domain-coordinate result would be informative and somewhat surprising.

## Experiment 2 — Paired matched-residue corruption inside the local window

Goal: test whether the AA identity of high-IC Pfam residues inside the recovery-sufficient window is necessary for the anchor. Replaces and supersedes the unrun spec at `experiments/4_6_scramble_experiment.md`. Merge the two specs; do not fork.

Set: P50. Local window per protein is ±R_50 from Experiment 0. If R_50 > 30 fall back to ±30.

Conditions, all paired within protein and matched on residue count k = 8 (or 25% of window length, whichever is smaller). Same perturbation type for all conditions: masking with `<mask>` token. (Substitution variant deferred unless masking results are ambiguous.)

- C0 baseline: no perturbation (anchor centered, window kept, rest of seq masked at ±R_50 boundary as in `scramble_experiment.py`).
- C7 high-IC Pfam: top-k residues in window by HMM match-state IC from Experiment 1.
- C4 buried-low-IC: k residues with RSA < 0.05 and below-median IC, from same window.
- C5 exposed-low-IC: k residues with RSA > 0.25 and below-median IC, from same window.
- C8 random-matched: k residues drawn uniformly from the window, RSA distribution matched to C7 by stratified sampling. 200 resamples.
- C_anchor (positive control): k=1, anchor itself masked. Should kill the signal; included to confirm pipeline.
- C_far (negative control): k residues drawn outside ±R_50 (in the surrounding masked region — re-unmask k positions far from anchor). Should not affect the anchor.

Readouts:
- Δα_norm = α_norm(condition) − α_norm(C0).
- ΔR_50 measured by re-running a small sweep (R = R_50−5 .. R_50+5) under each condition.
- Top-1 anchor identity preserved (binary).
- Optional: contact-segment metric using the existing `patching_metric` from `contact_jump.py` for a downstream sanity check.

Stats: per-protein paired Wilcoxon C7 vs each of {C4, C5, C8}. Across-protein effect size (paired Hodges–Lehmann) and 95% CI.

Pre-registered outcomes:
- |Δα_norm(C7)| > |Δα_norm(C4)|, |Δα_norm(C5)|, |Δα_norm(C8)| with significance → high AA-IC residues in the local window carry necessary identity information beyond burial/SSE/random — local domain-marker hypothesis supported.
- |Δα_norm(C7)| ≈ |Δα_norm(C4)| or ≈ |Δα_norm(C5)| → the head depends on a class-level feature (burial or SSE) not on conserved AA identity. This is consistent with the structural-feature story.
- |Δα_norm(C7)| ≈ |Δα_norm(C8)| → no special role for high-IC residues; the anchor is robust to most local perturbations and depends on something more global.
- C_anchor must zero the signal and C_far must leave it intact; if either fails, abort and debug before interpreting the rest.

This is the experiment most likely to discriminate hypotheses given existing evidence. Pre-commit to outcomes before running.

## Experiment 3 — Anchor-window clustering, structure-aware

Past clustering on L10 LN embeddings (`anchor_flank_clustering.py`, `anchor_flank_clustering_v2.py`) and PCA on K-anchor / OV outputs failed: cosine 0.9 across proteins, |rho|<0.2 vs scalar structural features. Do not repeat those representations against those labels. Two specific gaps remain:

Gap A: 3Di token windows around the anchor were never clustered directly. The structural-transfer result shows 3Di IC saturates at the anchor column for two families; whether this generalizes across many families and whether 3Di windows naturally partition into structural classes is open.

Gap B: prior clustering was evaluated against scalar structural features (RSA, contacts, SSE). It was not evaluated against categorical biological labels (Pfam, fold cluster, anchor-column-equivalence under structure alignment).

Set: P50 ∪ 1PVGA-homologs ∪ 2B61A-homologs (so we have at least two known equivalence groups for ground-truthing).

Representations:
- R_3Di: one-hot encoding of 3Di tokens in window ±15, centered on anchor (`data/foldseek/all_3di.fa`). Untried.
- R_AA: one-hot encoding of AA tokens in ±15. Cheap baseline; not the failed L10 representation.

Drop: AA k-mer TF-IDF, edit distance, Hamming distance, multiple clustering algorithms. Drop L10 LN representations — already shown to be uninformative here.

Method: HDBSCAN on cosine distance. UMAP for visualization only (n_neighbors=15, min_dist=0.1). Single method, single set of hyperparameters chosen up front.

Labels for evaluation:
- L_Pfam: Pfam family from Experiment 1 annotations.
- L_struct: Foldseek structural cluster id (cluster the PDBs of the set with foldseek easy-cluster at TM 0.5; use cluster id as label).
- L_col: binary anchor-column-equivalence label, available for the 1PVGA and 2B61A homolog groups (anchor lands in their dominant alignment column or not).

Metrics: NMI and ARI of HDBSCAN clusters vs each label. Plus a leave-one-out k-NN accuracy on labels using cosine distance directly (more stable than HDBSCAN to small n).

Pre-registered outcomes:
- R_3Di NMI vs L_struct > 0.3 AND R_3Di NMI > R_AA NMI vs same label → the anchor window has structural-alphabet signature; consistent with the structural-feature story.
- R_3Di and R_AA both fail (NMI < 0.1 vs all labels) → window-level token information is not enough; anchor identity depends on longer-range or non-token information. Negative result, report as such; do not search for spurious clusters.
- R_AA tracks L_Pfam strongly → AA-motif story re-enters; this would be surprising given the 0.9 cosine / 0.06 seq id finding and warrants follow-up.
- L_col is recovered for the two known homolog groups → confirms the representation respects the existing structural-transfer claim.

Outputs:
- `reports/out2/anchor_window_cluster/embeddings_3di.npy`, `embeddings_aa.npy`.
- `reports/out2/anchor_window_cluster/labels.csv` (Pfam, struct cluster, col-equiv).
- NMI/ARI table; UMAP plots colored by each label; k-NN accuracy table.

This is exploratory but pre-registered: each outcome ties back to one of the three working hypotheses, and the negative result is acceptable rather than something to chase.

## General constraints (apply to all experiments)

- Same P50 across all experiments. Any deviation is documented.
- Local window for any "around the anchor" reasoning is per-protein R_50 from Experiment 0. No fixed ±25/±30 unless R_50 is missing.
- Perturbations matched by residue count and at least one of {RSA, SSE}. Paired comparisons within protein.
- Reuse: `get_projection_at_anchor`, `compute_search_dir`, recovery curves, `patching_metric`. Do not reimplement.
- Index hygiene: PDB numbering, sequence index, HMM match-state, model token position. Save the seq-pos → HMM-state mapping per chain so it can be inspected. Verify off-by-one between special tokens and sequence index for ESM2 (BOS shift).
- Pre-register the outcome map for each experiment in the results doc before opening the result CSVs.

## Suggested execution order

1. Experiment 0 (cheap; ~hours on the cluster). Produces R_50 per protein.
2. Experiment 1 annotation pass (Pfam mapping, no model inference). Required for Experiments 2 (C7) and 3 (L_Pfam).
3. Experiment 2. The discriminating experiment.
4. Experiment 3 in parallel with Experiment 2 (independent compute).
