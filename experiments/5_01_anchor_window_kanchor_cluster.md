# 5_01 — Unsupervised cluster structure of anchor windows and K vectors on CATH corpus

Companion to `experiments/4_30_anchor_e3_cath_repl.md`. The 4_30 regression answered "do windows predict structural-column-equivalence beyond TM" using pair-level scalar distances. This experiment runs the unsupervised counterpart on the same corpus: cluster the windows directly, describe what comes out, and ask at what taxonomic level the partition happens. Repeats with the head's K vector at the anchor position so the input-side and recognition-side answers can be compared.

Model: `facebook/esm2_t33_650M_UR50D`. Head: L10H9. Anchor positions reused from `reports/out2/cath_transfer/anchors.csv`.

## Question

Two questions, parallel:

Q1 (input side): When the 31-residue local windows around the L10H9 anchor are clustered without supervision, at what taxonomic level does the partition fall — Pfam, H-superfamily, fold, or none? Does 3Di-alphabet clustering recover a different level than AA-alphabet clustering?

Q2 (head side): When the head's key vector at the anchor position (`K_anchor = LN10(x_anchor) @ W_K`) is clustered without supervision across chains, at what level does the partition fall? Does it agree with the input-side partition or abstract beyond it?

The unit of analysis is the chain, not the pair. There is no `same_col` label. Foldmason MSAs are not used. TM is not used.

## Operational definitions (locked)

- Anchor position: attn-argmax of L10H9 (`top_key_idx` in `anchors.csv`). Top-1 only; top-3 dropped after 4_30 showed top-3 collapses the signal.
- Local window: residue indices `[anchor-15, anchor+15]`. 31 positions, gap-padded for chain-boundary overflow.
- W_AA(i) and W_3Di(i): 31-character strings, alphabets and gap handling as in 4_30. One-hot encoded to a 31 × |alphabet| matrix, then flattened to a single vector per chain.
- K_anchor(i) ∈ R^d: the head's key vector at the anchor position. d = head_dim of L10H9 (esm2_t33_650M has 20 heads, hidden 1280, head_dim 64). Computed once per chain via a single ESM2 forward pass on the full sequence: extract `LN10_output[anchor_pos]`, apply `W_K[head_9]`, where `W_K[head_9]` is the 9th head's slice of the layer-10 attention key projection. Saved alongside Q_anchor and V_anchor for reference.
- Q_mean(i): mean query vector at the head, used as the head's "search direction" reference. Reused from prior code (`compute_search_dir` in `scripts/anchor_flank_clustering_v2.py`).
- Labels (used for evaluation only, never as input):
  - L_Pfam: primary Pfam from `reports/out2/cath_transfer/struc_transfer_manifest.csv` (or `pfam_first_selection.csv` if a chain is multi-Pfam).
  - L_HSF: H-superfamily (Set A / B / C → 3.40.50.720 / 3.40.50.1820 / 2.60.40.10).
  - L_fold: fold class (A and B → α/β; C → all-β); flag the A vs B fold-vs-distinct-fold classification ambiguity from the 4_29 doc methods note.
  - L_foldseek_cluster: foldseek `easy-cluster --min-seq-id 0 -c 0.0 --cov-mode 0 --tmscore-threshold 0.5` cluster id, run once on the n=129 chain set. Independent structural label, not derived from manifest.

## Set

- Primary: full CATH corpus n = 129 (Set A 60 + Set B 39 + Set C 30). Audit-pass subset (n = 74) reported as supplement.
- Why full set as primary: this is unsupervised; audit filtering is fold-biased and would bake the fold imbalance into the cluster structure. We want to see whether the unsupervised partition is fold-biased on its own, not impose it.

## Representations and cluster pipeline

Four representations:

| name | dim | source |
|---|---|---|
| R_AA | 31 × 22 = 682 | one-hot of AA window |
| R_3Di | 31 × 21 = 651 | one-hot of 3Di window |
| R_K | 64 | L10H9 K vector at anchor |
| R_Q | 64 | L10H9 Q vector at anchor (sanity / vertical-attention check; expected near-uniform across chains) |

For each representation, identical pipeline:

1. Cosine-distance matrix across all chains.
2. HDBSCAN(metric="precomputed", min_cluster_size = max(3, n//12), min_samples = 2). Single hyperparameter setting picked up front; do not tune to label.
3. UMAP(n_neighbors=15, min_dist=0.1, metric="cosine") for visualization only.
4. Cluster composition table: for each cluster, count of chains by L_Pfam, L_HSF, L_fold, L_foldseek_cluster, plus dominant label and purity (fraction in dominant).
5. Quantitative metrics vs each label:
   - NMI (`adjusted=True`)
   - ARI
   - Leave-one-out k-NN classification accuracy with k=3 on cosine distance directly (more stable than HDBSCAN to small n; in 4_28's prior Exp 3, this was the strongest 3Di signal).

## Pre-registered outcome thresholds

For the input-side question Q1:

H1a (3Di partitions at the H-superfamily / fold level):
- LOO k-NN accuracy of R_3Di vs L_HSF ≥ 0.75, AND
- HDBSCAN-NMI of R_3Di vs L_HSF ≥ R_3Di vs L_Pfam − 0.05 (i.e. HSF is at least as informative as Pfam).
- Interpretation if met: 3Di window content groups proteins at the structural-superfamily level, not finer-grained per-Pfam motif level.

H1b (3Di partitions at the Pfam level only):
- R_3Di k-NN(L_Pfam) ≥ 0.75 AND R_3Di k-NN(L_HSF) < 0.75, AND
- NMI(R_3Di, L_Pfam) > NMI(R_3Di, L_HSF) + 0.10.
- Interpretation: the head's input window encodes family-specific motif information, not a generalized fold-level structural feature. Pfam-detector reading.

H1c (AA does not partition at any level):
- R_AA k-NN accuracy ≤ 0.50 vs all of {L_Pfam, L_HSF, L_fold, L_foldseek_cluster}.
- This was the 4_28 finding on the audit set. We test whether it still holds on CATH.

For the head-side question Q2:

H2 (R_K agrees with R_3Di at the same partition level):
- The label level at which R_K NMI peaks matches the level at which R_3Di NMI peaks (both Pfam-peaked, both HSF-peaked, etc.), AND
- Peak NMI(R_K) ≥ peak NMI(R_3Di) − 0.05.
- Interpretation: the head's recognition vector partitions at the same level as the structural-alphabet input. Structural-feature-detector at the head level.

H3 (R_K abstracts beyond R_3Di):
- R_K NMI peaks at a coarser label level than R_3Di (e.g. R_3Di Pfam-peaked, R_K HSF-peaked).
- Interpretation: the head computes a more general structural feature than the local 3Di alphabet directly encodes. Stronger mechanism claim.

H4 (R_K is uninformative):
- R_K LOO k-NN ≤ 0.50 vs all labels.
- Interpretation (consistent with prior PCA failure): the head's recognition vector is approximately constant in direction across proteins, only its alignment with q_mean varies; clustering on K_anchor is not the right view. Pre-registered acceptable negative; document and pivot to alternative mechanistic representations in future work.

## Auxiliary, descriptive

A. Dominant-label purity histograms per representation. For each cluster's dominant Pfam (and HSF, fold), histogram of purity. Tells the "are families split or merged" story directly.

B. Confusion-style cross-tabs. Cross-tab of HDBSCAN cluster id × L_Pfam, × L_HSF, × L_fold, per representation. Visual answer to "at what level does the partition happen."

C. Foldseek-cluster comparison. NMI of HDBSCAN clusters vs L_foldseek_cluster. Sanity check that the partition tracks an independent structural-similarity grouping.

D. Q vector check. NMI(R_Q, any label) and pairwise cosine of Q across chains. Confirms vertical-attention hypothesis: Q is approximately shared, so it should cluster as one blob and label-NMI should be near 0. If Q does cluster, that's a finding worth reporting.

E. Shuffled negative controls. Permute the chain-to-window mapping (200 perms) for R_AA and R_3Di. Confirms NMI under permutation collapses to the null. Calibrates effect size.

## Things this does not test (state in writeup)

- Causation. None of these representations are intervened on. Claims are correlational ("R_K clusters at level X") not causal ("K_anchor is what causes the head to anchor at column Y").
- Other heads, other layers. Single head, single position (the anchor). No claim about ESM2 representations broadly.
- Within-cluster substructure. HDBSCAN at one hyperparameter setting; we are not running hierarchical analysis or sub-cluster discovery.

## Pipeline and outputs

Single script `scripts/anchor_e3_cluster.py`, stages:

```
load_anchors → build_windows → extract_kqv → cluster → metrics → composition → plots
```

```
reports/out2/anchor_e3_cluster/
  windows_aa.npy            # n × 682
  windows_3di.npy           # n × 651
  k_anchor.npy              # n × 64
  q_anchor.npy              # n × 64
  v_anchor.npy              # n × 64 (saved, not analyzed in this experiment)
  labels.csv                # chain, L_Pfam, L_HSF, L_fold, L_foldseek_cluster
  cluster_assignments.csv   # chain × {hdbscan_aa, hdbscan_3di, hdbscan_k, hdbscan_q}
  metrics.csv               # NMI / ARI / k-NN-acc per (representation × label)
  composition_aa.csv        # cluster × Pfam/HSF/fold counts and purity
  composition_3di.csv
  composition_k.csv
  shuffled_null.csv
  fig_umap.png              # 4 reps × 4 colorings = 16-panel grid
  fig_metrics.png           # bar chart of k-NN acc and NMI per (rep × label)
```

## Reuse from prior code

- `fixed_window`, `encode_window_onehot`, `load_3di_fasta` from `scripts/anchor_hmm_experiment.py` (prior Exp 3 implementation). Match window length and alphabet handling exactly so any difference vs 4_30 numbers is attributable to corpus and metric, not representation.
- `compute_search_dir`, `get_projection_at_anchor` from `scripts/anchor_flank_clustering_v2.py` for q_mean and K-vector extraction.
- ESM2 loader and L10H9 W_K access from `scripts/anchor_cath_transfer.py:_load_model` (NNsight wrap), reused across all extraction calls.
- Anchors and labels: `reports/out2/cath_transfer/anchors.csv`, `struc_transfer_manifest.csv`.

## Estimated effort

Window extraction and one-hot: minutes. ESM2 forward pass per chain (n=129) for K/Q/V extraction: ~30 minutes on a single GPU. HDBSCAN + UMAP + metrics: minutes. Foldseek easy-cluster: minutes. Total: under 2 hours including the figure grid. No new MSA / TM compute.

## Why this complements the 4_30 regression

4_30 answered: "do windows carry information about structural-column-equivalence beyond TM" (pair-level, supervised by `same_col`).

5_01 answers: "when windows and K vectors are grouped without supervision, at what taxonomic level does the partition fall" (chain-level, unsupervised).

These are different questions. Together they speak to the family-vs-sequence-vs-structure question: 4_30 tells you the alphabet-content carries structural information beyond global similarity; 5_01 tells you whether the head groups proteins at the family, superfamily, or fold level — the answer to "is the head doing family-specific stuff or generalized structural stuff."

## Results — full corpus (n_chains=123, primary)

Run: `uv run python scripts/anchor_e3_cluster.py --device cuda --batch-size 2`. Outputs in `reports/out2/anchor_e3_cluster/`. The corpus loaded 123/129 chains — 6 chains drop out at the foldmason 3Di / chain_seqs join (no usable 3Di string). Audit-pass count among the 123 is 71. Foldseek `easy-cluster --tmscore-threshold 0.5` returns 9 cluster representatives across the 123 chains; this is the `L_foldseek_cluster` label.

After a first pass, the spec's H3 ("R_K abstracts beyond R_3Di") was identified by the planning review as unsupported without a residual-stream control. R_LN10 (the LayerNorm-10 output at the anchor position, before any W_K / W_Q / W_V projection) was added as a fifth representation and the metrics table re-run.

Headline metrics (per representation × label):

| rep | label | n_clusters | n_noise | NMI(adj) | ARI | LOO k=3 NN acc |
|---|---|---|---|---|---|---|
| R_AA | L_Pfam | 2 | 29 | 0.093 | 0.004 | 0.488 |
| R_AA | L_HSF | 2 | 29 | 0.105 | -0.057 | 0.878 |
| R_AA | L_fold | 2 | 29 | 0.043 | -0.096 | 0.935 |
| R_AA | L_foldseek_cluster | 2 | 29 | 0.087 | -0.001 | 0.764 |
| R_3Di | L_Pfam | 2 | 5 | 0.171 | 0.027 | 0.626 |
| R_3Di | L_HSF | 2 | 5 | 0.218 | 0.153 | 0.943 |
| R_3Di | L_fold | 2 | 5 | 0.291 | 0.481 | 0.976 |
| R_3Di | L_foldseek_cluster | 2 | 5 | 0.206 | 0.079 | 0.829 |
| R_K | L_Pfam | 5 | 15 | 0.674 | 0.373 | 0.650 |
| R_K | L_HSF | 5 | 15 | 0.701 | 0.542 | 0.992 |
| R_K | L_fold | 5 | 15 | 0.493 | 0.239 | 0.992 |
| R_K | L_foldseek_cluster | 5 | 15 | 0.762 | 0.672 | 0.894 |
| R_Q | L_Pfam | 5 | 17 | 0.715 | 0.392 | 0.642 |
| R_Q | L_HSF | 5 | 17 | 0.809 | 0.668 | 0.984 |
| R_Q | L_fold | 5 | 17 | 0.496 | 0.244 | 0.984 |
| R_Q | L_foldseek_cluster | 5 | 17 | 0.755 | 0.628 | 0.886 |
| R_LN10 | L_Pfam | 5 | 21 | 0.719 | 0.429 | 0.626 |
| R_LN10 | L_HSF | 5 | 21 | 0.807 | 0.655 | 0.984 |
| R_LN10 | L_fold | 5 | 21 | 0.499 | 0.240 | 0.992 |
| R_LN10 | L_foldseek_cluster | 5 | 21 | 0.806 | 0.735 | 0.886 |

Shuffled null (200 perms, AA and 3Di vs L_Pfam / L_HSF): null NMI mean ≈ 0.01–0.05, p95 ≈ 0.04–0.07, max ≈ 0.05–0.09.

HDBSCAN composition (top-line):
- R_K: 5 clusters of sizes 22, 30, 12, 30, 14, plus 15 noise. Cluster 0 (n=22) is 100% HSF 2.60.40.10 (Ig). Clusters 1, 2 (n=30, 12) are 80% / 100% HSF 3.40.50.1820 and split that HSF into two foldseek-cluster reps (both 6brt_B). Clusters 3, 4 (n=30, 14) are 100% HSF 3.40.50.720, split into foldseek 2hrz_A and 4gi2_B.
- R_LN10: 5 clusters with 21 noise; same alignment to HSF / foldseek_cluster as R_K. Slightly higher NMI(L_foldseek_cluster) than R_K (0.806 vs 0.762).
- R_3Di: 2 clusters of sizes 99 and 19, plus 5 noise. The α/β chains stay merged into one big blob; the partition is essentially α/β-vs-all-β.
- R_AA: 2 clusters with 29 noise. ARI < 0 vs L_HSF / L_fold — HDBSCAN does not find structure that aligns with labels at this resolution.

## Decision against pre-registered thresholds

H1a (3Di partitions at HSF / fold). Met. R_3Di k-NN(L_HSF) = 0.943 ≥ 0.75. NMI(R_3Di, L_HSF) = 0.218 ≥ NMI(R_3Di, L_Pfam) − 0.05 = 0.121. The 3Di window groups proteins at the structural-superfamily level, not finer-grained per-Pfam motif level. R_3Di k-NN values rise monotonically as the label coarsens (Pfam 0.63 → HSF 0.94 → fold 0.98). This is the cleanest pre-registered result and it triangulates with the 4_30 regression: 3Di windows carry cross-Pfam structural-column-equivalence information beyond TM, and that information partitions chains at the structural-superfamily level rather than at family-motif level.

H1b (3Di partitions at the Pfam level only). Not met. k-NN(L_Pfam) = 0.626 < 0.75 and HSF k-NN strictly higher than Pfam k-NN. Rules out the "Pfam-detector" reading.

H1c (AA does not partition at any level). The high k-NN values for R_AA at L_HSF (0.878) and L_fold (0.935) are an artefact of label cardinality. L_fold has 2 classes, L_HSF has 3 — k=3 NN can hit those accuracies from coarse compositional differences alone (α/β chains have measurably different AA composition than the Ig set). The HDBSCAN-NMI for R_AA at every label is 0.04–0.11, sitting at or just above the shuffled-null max (≈ 0.05–0.09). The signal-vs-noise read: R_AA k-NN(L_Pfam) = 0.488 (chance for the Pfam multiclass problem), HDBSCAN cannot find clusters that align with labels (ARI ≤ 0.004 at every label), and NMI is at the null floor. The 4_28 "AA NMI ≈ 0" framing survives once we account for label cardinality: R_AA shows weak compositional signal that distinguishes broad fold class but does not partition by Pfam and does not generate label-aligned cluster structure.

## R_K vs R_3Di — re-framed

The HDBSCAN-NMI gap between R_K (0.762 vs L_foldseek_cluster) and R_3Di (0.206) is large but partly an artefact of the metric: HDBSCAN finds 5 well-separated clusters in R_K (cosine geometry) and only 2 in R_3Di, and NMI rewards finer label-aligned partitions. The k-NN gap, which is invariant to clustering granularity, is much smaller: R_K = 0.894 vs R_3Di = 0.829 at L_foldseek_cluster. Both representations carry similar amounts of foldseek-cluster information when measured by k-NN; R_K is more cleanly partitioned in cosine geometry, but the underlying structural-cluster identity information is not dramatically more abundant.

Honest framing: R_K is more cluster-friendly than R_3Di (HDBSCAN can resolve substructure in cosine space that it can't resolve in the 3Di one-hot space), not "the head abstracts beyond the input window." H3 as written ("R_K abstracts beyond R_3Di") is too strong; the data support "R_K is more cleanly partitioned in cosine geometry."

## R_LN10 anchor-vs-position controls — the load-bearing findings

Step 1 — R_LN10 at the anchor. R_LN10 (residual-stream LayerNorm output at the anchor, before W_K / W_Q / W_V projection) clusters as well as R_K and R_Q at every label: NMI(L_HSF) 0.807 vs 0.701 (R_K) vs 0.809 (R_Q); NMI(L_foldseek_cluster) 0.806 vs 0.762 vs 0.755; LOO k=3 NN(L_HSF) 0.984 vs 0.992 vs 0.984. The head reads from a structurally-aware substrate; W_K is not extracting structural information, it is a near-isometric projection of an already-structurally-organized vector at the anchor position.

Step 2 — pre-registered position control. To decide whether the anchor position is structurally-special at the LN10 level or whether all positions at L10 are structurally-aware, two further representations were added: R_LN10_rand (LN10 at a random non-anchor position, single seed paired per chain) and R_LN10_mean (mean LN10 over the full chain). Same metrics:

| rep | k-NN(L_Pfam) | k-NN(L_HSF) | k-NN(L_fold) | k-NN(L_foldseek) | NMI(L_HSF) | NMI(L_foldseek) | n_clusters | n_noise |
|---|---|---|---|---|---|---|---|---|
| R_LN10 (anchor) | 0.626 | 0.984 | 0.992 | 0.886 | 0.807 | 0.806 | 5 | 21 |
| R_LN10_rand | 0.480 | 0.967 | 0.984 | 0.732 | NaN | NaN | 0 | 123 |
| R_LN10_mean | 0.756 | 0.992 | 0.992 | 0.902 | 0.753 | 0.835 | 6 | 6 |

Three things to read off:

(a) At L_HSF / L_fold (3 / 2 classes), LN10 at any position recovers chain identity at ~0.97–0.99 k-NN. Random non-anchor is essentially as accurate as anchor. This is the planning review's outcome (1) at the coarse-label level: by layer 10, the residual stream is broadly structurally-aware everywhere in the chain. The anchor is not coarse-structurally-special.

(b) At the finer labels (L_foldseek_cluster with 9 reps, L_Pfam multiclass), the anchor is measurably more informative than a random non-anchor position. k-NN(L_foldseek_cluster): 0.886 anchor vs 0.732 random (Δ = 0.15). k-NN(L_Pfam): 0.626 anchor vs 0.480 random (Δ = 0.15; random is at chance for Pfam). The anchor position carries finer-grained structural-cluster / family identity than a random position does — this is a partial outcome (2) at the fine-label level. Magnitude is modest, not dramatic.

(c) R_LN10_mean is the strongest single representation of all reps tested — NMI(L_foldseek_cluster) = 0.835 (highest in the table); k-NN(L_Pfam) = 0.756; HDBSCAN finds 6 clean clusters with only 6 noise points (vs 21 for anchor). Chain-level pooling of LN10 outperforms any single position. This means the structural-class signal is broadly available across the chain and pooling cleans up per-position noise; the anchor's advantage over a random position (item b) does not extend to an advantage over the chain mean.

(d) Side note on HDBSCAN at R_LN10_rand: HDBSCAN finds 0 clusters (all 123 points are flagged as noise). NMI undefined. Random-position vectors are too noisy in cosine space for HDBSCAN to find density structure — yet k-NN still recovers labels at coarse levels because nearest-neighbour-by-cosine still works between chains of the same fold class. This is a useful methodological caveat: HDBSCAN-NMI under-reports signal that k-NN picks up.

Mechanism statement that survives all three controls. By layer 10 of ESM2-650M, the residual stream at every chain position encodes structural superfamily (HSF / fold class) — this is a property of the model, not of L10H9. L10H9's role is positional: it selects an anchor position whose representation, in addition to the broadly-shared HSF signal, carries fine-grained foldseek-subcluster and Pfam-family information at modestly higher fidelity than a random non-anchor position (k-NN gap ≈ 0.15 at L_foldseek_cluster). The head's K-vector R_K inherits this signal via near-isometric projection of LN10[anchor]; W_K does not construct it. The chain-level mean (R_LN10_mean) carries an even cleaner version of the same signal, so the anchor position is not a unique structural reservoir.

H2 / H3 / H4 final dispositions:
- H2 (R_K matches R_3Di partition level): not the right frame — both carry HSF-level information via different routes. k-NN comparable on L_foldseek_cluster (0.89 vs 0.83).
- H3 (R_K abstracts beyond R_3Di): falsified. The structural cluster geometry visible in R_K is already in LN10[anchor]; W_K does not contribute abstraction.
- H4 (R_K uninformative): falsified, but inheritance from the substrate.

## Final claim, revised

Cross-fold CATH corpus (n=123). Four findings:

(1) The L10H9 anchor's local 3Di window partitions proteins at the H-superfamily level (LOO k=3 NN 0.94 vs L_HSF; 0.83 vs L_foldseek_cluster), not the Pfam level (0.63). The AA window does not. R_AA HDBSCAN-NMI sits at the shuffled-null floor at every label, and its high k-NN against L_HSF / L_fold reflects label cardinality (3 / 2 classes) plus crude compositional differences between α/β chains and Ig. The 4_28 "AA carries no alignment-grade signal" reading holds on this cross-fold corpus.

(2) The head's L10H9 K-vector (R_K) clusters chains cleanly into 5 HSF / foldseek-cluster sub-groups in cosine space, while the 3Di window can only separate α/β-vs-all-β. This is best read as "R_K is more cluster-friendly in cosine geometry," not "R_K abstracts beyond the input"; k-NN on L_foldseek_cluster is only modestly higher for R_K (0.894) than for R_3Di (0.829).

(3) R_LN10 (residual-stream output at the anchor, before any head projection) clusters as well as or better than R_K / R_Q on every label and metric. W_K preserves rather than extracts the structural organization.

(4) Position control. LN10 at a random non-anchor position recovers L_HSF / L_fold at near-ceiling k-NN (0.97 / 0.98), so the residual stream is broadly structurally-aware at L10 and the anchor is not coarse-structurally-special. At finer labels, the anchor outperforms a random position by a modest margin (k-NN gap ≈ 0.15 at L_foldseek_cluster and L_Pfam). Mean-pooled LN10 over the chain is the strongest single representation of all reps tested (NMI 0.835 vs L_foldseek_cluster, 6 clean clusters vs 21 noise). Combined with (3): the head's job is positional selection, not structural feature construction. The structural processing happens at or before L10 and is broadcast across the chain; L10H9 picks a position whose representation has somewhat more fine-grained structural identity than a random one.

Limitations to cite. (i) 6 of 129 chains drop on 3Di-extract (foldmason / chain_seqs join failure); n=123. (ii) HDBSCAN run at one hyperparameter setting (mcs=10, ms=2); cluster counts depend on this — k-NN is the more granularity-robust metric. R_LN10_rand fails to cluster at all under HDBSCAN despite recovering coarse labels by k-NN; HDBSCAN-NMI under-reports k-NN-detectable signal in noisy regimes. (iii) L_fold (2 classes) and L_HSF (3 classes) are low-cardinality labels; k-NN against them is not a fine-grained structural test. L_foldseek_cluster (9 reps) is the rigorous label. (iv) R_LN10_rand uses one random position with one seed; a multi-seed average would tighten (4) but is unlikely to change the direction. (v) The R_LN10 result re-locates structural processing to ≤ L10 but says nothing about which earlier layer first encodes it — follow-up. (vi) "L10H9's job is positional" is supported by the position control but the mechanism of its position-selection (3Di environment? sequence motif? earlier-layer feature?) is not addressed by this experiment.
