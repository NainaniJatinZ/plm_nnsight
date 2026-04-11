# Experiment: Structure Anchor Transfer v2 (Expanded Dataset)

## Motivation

The v1 experiment (4_9) showed that L10H9 anchor positions cluster tightly at alignment column 98 across 12 structural homologs of 1PVGA (TM > 0.6, seq id < 25%). However, the effective sample size was ~7 due to near-duplicate sequences (3zkb/3zkd/3zm7 at 99%+ identity, 1b62/1nhh at 99.7%, 3cwv assemblies at 100%).

We now have a larger dataset: 98 entries (66 unique PDB IDs) from Foldseek top-2 hits for 1PVGA, filtered by TM > 0.6 and seq id < 0.20. This experiment repeats the structure anchor transfer analysis with proper deduplication, adds top-3 anchor concordance (motivated by the 3cwv outlier, whose anchor at column 493 turned out to be a secondary anchor for other proteins), and runs AA + 3Di flank motif analysis on the structurally aligned set.

The broader goal: determine whether L10H9's anchor selection reflects structural properties. ESM2 is a sequence-only model, so if it reliably places anchors at structurally equivalent positions across sequence-diverse proteins, that is non-trivial evidence that the model has learned to detect structural landmarks from sequence alone.

## Prior results informing this design

1. v1 anchor concordance: 11/12 proteins anchor at column 98, one outlier at column 493. Projection score transfer top-1 hit rate: 83.3%.
2. Flank motif analysis (n=250, diverse proteins): IC at anchor = 0.874 bits (max 4.32). No dominant AA motif. 3Di max freq = 0.35. Interpreted as evidence against motif detection.
3. Flank clustering (n=250): mean pairwise flank seq identity = 0.064, yet mean ESM2 flank embedding cosine = 0.903. No correlation between seq identity and embedding similarity.
4. 3cwv outlier: its top-1 anchor (column 493) was the top-2/3 anchor for other proteins, and its top-2/3 anchor was at column 98. This motivates the top-3 analysis.

---

## Data

Source: `data/foldmason_top2_tm_gt_06_seq_lt_02/foldmason_aa.fa`
- 98 alignment entries from 66 unique PDB IDs
- Multiple assemblies for many PDBs (3zkb: 7, 4uro: 4, 3zkd: 4, etc.)
- Reference protein: 1pvg-assembly1cifgz (1PVGA)
- 63/66 PDBs need downloading from RCSB (existing PDBs in `data/pdb/`)

---

## Phase 0: Data Preparation

### 0.1 Parse alignment and extract ungapped sequences

Parse `foldmason_aa.fa`. For each entry, strip gaps to get the raw sequence. Build bidirectional mappings: alignment column <-> ungapped position.

### 0.2 Collapse same-PDB assemblies

Multiple assemblies of the same PDB (e.g., 3zkb-assembly1, 3zkb-assembly4, 3zkb-assembly5, 3zkb-assembly7) are near-identical sequences. Keep one representative per PDB ID (the longest ungapped sequence). This reduces 98 entries to 66.

### 0.3 Deduplicate by 90% global sequence identity

Compute all-vs-all pairwise global sequence identity among the 66 representatives. Cluster with single-linkage at 90% identity threshold. Keep one representative per cluster (longest sequence). Report how many clusters remain (expected: ~50-60 after removing known near-duplicates like 3zkb/3zkd/3zm7).

Output: a clean protein list with effective n, plus the pairwise identity matrix for transparency.

### 0.4 Download missing PDB structures

For each representative protein, check if `data/pdb/{PDBID}.pdb` exists. Download missing ones from RCSB (`https://files.rcsb.org/download/{PDBID}.pdb`). Store in `data/pdb/`.

### 0.5 Generate 3Di sequences

Foldseek is available at `foldseek/bin/foldseek`. Run `foldseek structurealphabet` (or `foldseek createdb` + `convert2fasta` as done previously for `data/foldseek/all_3di.fa`) on each PDB to get 3Di sequences. Store in a new file alongside the existing 3Di data.

---

## Phase 1: Anchor Behavior Audit

### 1.1 Compute reference search direction

Compute d_ref from 1PVGA itself (d_ref = W_K^T @ q_mean from 1PVGA's full sequence). This is the primary reference direction. Also compute d_ref_2b61 from 2B61A as a sanity check. Report cosine(d_ref_1pvg, d_ref_2b61) — if high (>0.8, as seen in v1), both are interchangeable.

### 1.2 Per-protein forward pass

For each deduplicated protein, run a forward pass through ESM2-650M. Cache L10 LayerNorm output and L10H9 attention weights.

Compute:
- top1_mass, top3_mass (attention concentration on dominant keys)
- rank_corr (Spearman between projection score and mean key attention mass)
- cos(d_self, d_ref) (cosine between protein's own search direction and reference)
- Top-3 anchor positions (by mean key attention mass)
- Top-3 projection score positions

### 1.3 Anchor-like gating

Gate: top1_mass > 0.15 AND rank_corr > 0.3 (same thresholds as v1 and the 2k-protein audit).

Report: fraction passing, fraction failing, and a table of all proteins with their metrics. If fewer than 50% pass, flag this as a concern and investigate before proceeding.

---

## Phase 2: Top-1 Anchor Column Concordance

### 2.1 Map anchors to alignment columns

For each protein that passes the gate, map its top-1 anchor (argmax attention mass) to the corresponding alignment column.

### 2.2 Pairwise column distances

For each pair of proteins, compute |column_A - column_B|. Report:
- Median pairwise distance
- Fraction of pairs with exact match (distance = 0)
- Fraction within 5 columns
- Mean pairwise distance

### 2.3 Random position control

For each protein, sample a random (non-anchor) position. Map to alignment column. Compute the same pairwise distance statistics. Repeat 200 times to build a null distribution for the mean pairwise distance.

Report: anchor mean distance vs null distribution (percentile rank, z-score).

### 2.4 Projection score transfer (top-1)

For each ordered pair (A -> B):
1. Take A's top-1 anchor column.
2. Find B's residue at that column (skip if gap).
3. Report where that residue ranks in B's projection score distribution.

Aggregate: top-1, top-3, top-5, top-10 hit rates. Mean projection rank.

---

## Phase 3: Top-3 Anchor Column Concordance

This addresses the 3cwv-type scenario where the "outlier" protein's anchor is actually a secondary anchor for other proteins.

### 3.1 Map top-3 anchors to alignment columns

For each protein, map its top-3 anchor positions to alignment columns. This gives each protein a set of up to 3 anchor columns.

### 3.2 Identify consensus anchor columns

Pool all top-3 anchor columns across all proteins. Cluster them (within a tolerance of 5 columns). Identify consensus columns — alignment positions where many proteins have one of their top-3 anchors nearby.

Report: number of consensus columns, how many proteins contribute to each, and the column positions.

### 3.3 Pairwise set overlap

For each pair of proteins, compute the minimum distance between any of A's top-3 anchor columns and any of B's top-3 anchor columns. Report the same statistics as Phase 2.2 (median, exact match fraction, within-5 fraction).

### 3.4 Random control for top-3

Sample 3 random positions per protein, compute the same set-overlap metric. 200 trials for null distribution.

---

## Phase 4: Local Sequence Conservation Around Anchor

### 4.1 Per-column conservation

For each alignment column, compute the fraction of the most common amino acid across all proteins (ignoring gaps). This gives a conservation profile across the full alignment.

### 4.2 Anchor-window vs global conservation

Compare mean per-column conservation in the +/-25 window around the consensus anchor column(s) vs the global mean conservation. If the anchor region is not more conserved than average, the concordance in Phase 2 cannot be explained by local sequence conservation — strengthening the structural interpretation.

### 4.3 Pairwise local sequence identity

For each pair of proteins, compute pairwise sequence identity in the +/-25 window around the consensus anchor column. Compare to their global pairwise identity. Report whether local identity is significantly higher than global.

---

## Phase 5: Flank Motif Analysis (Amino Acid)

### 5.1 Extract flanks

For each protein, extract the +/-25 amino acid window centered on the top-1 anchor position (in ungapped sequence coordinates, not alignment coordinates). This gives the actual local sequence context the model sees.

### 5.2 Position-weight matrix and information content

Build a PWM across all proteins. Compute per-position IC (bits). Compare to the 250-protein motif analysis (where IC at anchor was 0.874 bits).

Key comparison: the 250-protein set was diverse across all folds. This set shares a common fold. If a motif emerges here but not in the general set, it is fold-specific (interesting). If no motif emerges here either, the anchor is not doing motif detection at any level.

### 5.3 Sequence logo

Generate sequence logo colored by amino acid chemical properties.

---

## Phase 6: Flank Motif Analysis (3Di)

### 6.1 Map anchors to 3Di coordinates

Align each protein's full sequence to its PDB structural sequence (to handle any numbering offsets). Map the anchor position to the corresponding 3Di position.

### 6.2 Extract 3Di flanks and build PWM

Same as Phase 5 but using 3Di alphabet (20 letters encoding local backbone geometry).

### 6.3 Information content comparison

This is the sharpest test in the experiment. The proteins share 3D structure but not sequence. If 3Di flanks show higher IC than AA flanks, that is direct evidence that the anchor's local context is structurally conserved even when the sequence is not.

Report: IC at anchor (3Di vs AA), max IC in window (3Di vs AA), number of positions with IC > 0.5 bits.

---

## Success Criteria

### Phase 2 (top-1 concordance)
- Median pairwise anchor-column distance < 10
- Anchor column spread tighter than 95th percentile of null (200 random trials)
- Projection score transfer: top-5 hit rate > 50%

### Phase 3 (top-3 concordance)
- At least 2 consensus anchor columns with >30% of proteins contributing
- Minimum pairwise set distance: median < 5

### Phase 4 (local conservation)
- If local conservation around anchor is NOT significantly higher than global: strengthens structural interpretation (concordance is not driven by local sequence conservation)
- If it IS higher: does not invalidate the result, but means we cannot rule out that the model is using local sequence features

### Phase 5-6 (motif analysis)
- 3Di IC at anchor > AA IC at anchor (structural conservation > sequence conservation)
- If 3Di IC is also low: the anchor is not at a structurally stereotyped local geometry either — it may be a topological landmark (long-range fold feature) rather than a local structural motif

### Interpretation matrix

| Concordance | Local seq conservation | 3Di > AA motif | Interpretation |
|---|---|---|---|
| Strong | Low | Yes | Structure-landmark detector (strongest result) |
| Strong | Low | No | Topological landmark, not local geometry |
| Strong | High | Either | Cannot separate structure from local sequence |
| Weak | Any | Any | Anchor is not fold-conserved; per-protein or sequence-dependent |

---

## Implementation

### Script: `scripts/structure_anchor_transfer_v2.py`

```bash
uv run python scripts/structure_anchor_transfer_v2.py --device cuda
```

### Inputs
- `data/foldmason_top2_tm_gt_06_seq_lt_02/foldmason_aa.fa` — structural alignment
- `data/pdb/` — PDB structures (downloaded in Phase 0)
- `data/full_seq_dict.json` — protein sequences (for proteins already in our database)
- ESM2-650M model weights

### Key functions to reuse from `scripts/structure_anchor_transfer.py`
- `parse_fasta_alignment()`, `build_alignment_mappings()`
- `compute_search_dir_from_full_seq()`
- `analyze_protein()`
- `anchor_column_concordance()`
- `random_position_column_spread()`
- `projection_score_transfer()`

### New code needed
1. Assembly collapsing (keep one per PDB ID)
2. 90% identity clustering (pairwise identity + single-linkage)
3. PDB download from RCSB
4. 3Di sequence generation (foldseek or fallback to foldmason_ss.fa)
5. Top-3 anchor concordance analysis (consensus columns, set overlap)
6. Local conservation analysis (per-column conservation, window comparison)
7. AA and 3Di flank motif analysis (PWM, IC, logos)

### Outputs
- `reports/outputs/multi_protein/structure_anchor_transfer_v2.md` — main report
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_audit.csv` — per-protein metrics
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_concordance.csv` — pairwise distances
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_dedup.csv` — deduplication log
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_conservation.png` — conservation profile
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_top3_consensus.png` — consensus anchor columns
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_aa_logo.png` — AA sequence logo
- `reports/outputs/multi_protein/structure_anchor_transfer_v2_3di_logo.png` — 3Di sequence logo

---

## Compute estimate

- Phase 0: PDB downloads (~1 min), 3Di generation (~2 min), deduplication (~seconds)
- Phase 1: ~60 forward passes x ~0.2s each = ~12 seconds on GPU
- Phases 2-6: pure numpy/scipy, < 1 minute total
- Total: under 5 minutes excluding PDB downloads

---

## Caveats

1. The dataset is filtered by TM > 0.6 and seq id < 0.2 against 1PVGA, but pairwise identity between hits could still be high. The deduplication step (Phase 0.3) addresses this, but the pairwise identity matrix should be inspected.
2. Foldmason alignment quality may vary across proteins. Inspect the alignment around the anchor region for obvious misalignment or excessive gaps.
3. Some alignment entries look truncated (e.g., 4kfg, 5mmn in the FASTA). Proteins with ungapped length < 100 should be flagged and possibly excluded.
4. Foldseek is available locally at `foldseek/bin/foldseek` for 3Di generation.
5. The reference search direction d_ref is computed from 1PVGA. This is appropriate since all proteins are structural homologs of 1PVGA. The 2B61A sanity check (Phase 1.1) verifies that the direction is not protein-specific.

---

## Raw notes (user)

Previous we did experiments/4_9_structure_anchor_transfer.md, and got reports/outputs/multi_protein/structure_anchor_transfer.md
scripts/structure_anchor_transfer_followup.py
scripts/structure_anchor_transfer.py

We also did motif experiments

scripts/anchor_flank_3di.py
scripts/anchor_flank_motif.py

The structure anchor experiment was done on the foldmason data which only had 10 proteins and the proteins where chosen to have high structural (tm > 0.6) but low seq similarity (seq id < 0.25). But the proteins had high seq sim between each other so the effective n was even lower.

We have a new data with around ~90 proteins here on the top2 sequence (id in our protein is 1PVGA), with the filter of tm>0.6 , seq id < 0.2. data/foldmason_top2_tm_gt_06_seq_lt_02/

We want to filter out the seqs that have very high seq sim with other proteins if possible. And then repeat the experiment for the structure anchor and look for anchor position overlap between the aligned columns. We also want good amount of information for each protein on the global seq sim pairwise, seq sim around each of the anchors (top3 should be fine) with a flank of +-25.

And we also want to do the flank motif analysis with AA and 3Di tokens.

The goal of the experiment is to check if the anchor positions decided by L10H9 are looking for structural properites. The reason why I believe this experiment is worth -
the proteins have low seq id to target 1pvg, but high structural sim. So if the anchor positions are at the same aligned columns here, then its likely looking for some structural property.

In our experiments of creating a seq logo from the AA or 3Di flanks, we didnt find a single consistent motif. The high freq was 0.2 for AA and 0.35 for 3Di. To me, this also suggests that the anchor is not doing motif detection and "something to do with structural stuff".

My expectation from this experiment is that we will see overlap happening for anchors in aligned columns. As for the motifs on the flanks of these aligned proteins, we might see a motif if the flank level seq similarity is high. If we see a motif when the flank level seq sim is low that would be surprising.
