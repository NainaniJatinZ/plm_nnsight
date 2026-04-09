# Experiment: Anchor Transfer Across Structural Homologs (Low Sequence Identity)

## The question

If L10H9 anchoring reflects protein structure rather than sequence identity, then proteins with similar 3D folds but dissimilar sequences should exhibit similar anchor positions. Specifically: if we structurally align two proteins with TM-score > 0.6 and sequence identity < 25%, do their anchor positions map to the same columns of the structural alignment?

This is the "remote homolog" test from 4_8.md. It separates three stories:
- If aligned structural sites stay anchor-like at low sequence identity, that is evidence for a structure-linked landmark detector.
- If anchorhood follows family columns only within close homologs, that looks more like family memory or motif lookup.
- If neither transfers well, then the anchor may be a local per-protein integration score, not a fold-stable landmark.

---

## Data

Foldseek results for 1PVGA are already in `data/foldmason/`. The foldmason alignment contains 1pvg + 10 structural hits with TM-score > 0.6 and sequence identity < 25%. The alignment is a multiple structure alignment (foldmason), so all 11 proteins share a common column coordinate system.

Proteins in the alignment (from `foldmason_aa.fa`):

| ID | Notes |
|---|---|
| 1pvg-assembly1cifgz | Reference protein (1PVGA), known anchor at position 101 |
| 1ei1-assembly1cifgz | |
| 1mx0-assembly1cifgz | |
| 7cmp-assembly2cifgz | |
| 3zkb-assembly8cifgz | |
| 3zkd-assembly3cifgz | |
| 3zm7-assembly1cifgz | |
| 3zm7-assembly3cifgz | |
| 3cwv-assembly1cifgz | |
| 3cwv-assembly2cifgz | |
| 1b62-assembly1cifgz | |
| 1nhh-assembly1cifgz | |

Note: 3zkb/3zkd/3zm7 look like near-identical sequences (possibly different assemblies of the same or very close proteins). 3cwv assemblies also look similar to each other. 1b62 and 1nhh look like close homologs. Check actual pairwise sequence identities before interpreting results — the "dissimilar sequence" guarantee is relative to 1pvg, not between all pairs.

---

## Phase 1: Retrieve sequences and verify data

### Step 1.1: Extract ungapped sequences from the foldmason alignment

Parse `data/foldmason/foldmason_aa.fa` to get each protein's ungapped amino acid sequence. The aligned sequences contain `-` gap characters — strip these to get the raw sequence for each protein.

### Step 1.2: Retrieve PDB structures

For each protein in the alignment, download the structure from PDB/RCSB (e.g., 1ei1, 1mx0, 7cmp, etc.). We need these for the structure viewer (Phase 3) and to verify residue numbering.

Store in `data/foldmason/pdbs/`.

### Step 1.3: Build the alignment-to-sequence position mapping

From the gapped alignment, build a mapping for each protein: alignment column index -> ungapped sequence position (or gap). This is the coordinate system for comparing anchor positions across proteins.

Verify: 1pvg's known anchor at sequence position 101 should map to a specific alignment column. Record this column.

---

## Phase 2: Anchor behavior audit on new proteins

Run the same L10H9 anchor behavior metrics from `scripts/anchor_behavior_audit.py` on each new protein. This checks whether L10H9 is "anchor-like" at all on these proteins, before asking whether the anchor positions align.

### Step 2.1: For each protein, compute

Using the full (ungapped) sequence:

1. **Verticality metrics**: top1_mass, top3_mass, eff_keys, mean_max_attn
2. **Anchor concentration**: keys_50pct, max_key_mass, top3_key_mass
3. **Projection-attention agreement**: rank_corr, top3_proj_overlap

Use the same reference search direction d (from 2B61A, as in the audit) to compute projection scores and agreement metrics. This tests universality of the search direction on these new proteins.

Also compute a per-protein search direction d_self (from each protein's own q_mean) and check cosine similarity with the reference d. High similarity = the head computes the same "question" across these structurally similar proteins.

### Step 2.2: Anchor-like filtering

A protein passes the anchor-like check if:
- top1_mass > 0.15 (the head concentrates attention on a dominant key)
- rank_corr > 0.3 (projection score and attention mass are correlated)

These thresholds are the same as those used in the 2k-protein audit to separate anchor-like from non-anchor-like behavior. Report the fraction of the 10 new proteins that pass.

If most proteins fail: stop here. The head is not anchor-like on these proteins, and the structural transfer question is moot.

### Step 2.3: Identify anchor position in each new protein

For each protein that passes the anchor-like check, identify its anchor position as:
- The position with the highest mean-key attention mass (argmax of mean key distribution)
- Also record the top-3 positions by mean-key mass and by projection score

---

## Phase 3: Structural alignment of anchor positions

This is the core analysis. Do the anchor positions of structurally similar proteins map to the same columns of the structural alignment?

### Step 3.1: Map anchor positions to alignment columns

For each protein, take its anchor position (from Phase 2) and map it to the corresponding alignment column using the mapping from Step 1.3.

### Step 3.2: Primary analysis — anchor column concordance

Compare the alignment columns of anchor positions across proteins:
- Do the top-1 anchor positions map to the same or nearby alignment columns?
- More precisely: for each pair of proteins (A, B), is A's anchor column within k columns of B's anchor column in the alignment? Report for k = 0 (exact match), k = 3, k = 5.

### Step 3.3: Control — random buried positions

For each protein, select 10 random buried positions (RSA < 0.1 if available, or just random non-anchor positions). Map them to alignment columns. Compare the alignment column spread of random positions vs anchor positions. The anchor positions should cluster more tightly in alignment space if they reflect a shared structural feature.

### Step 3.4: Projection score transfer

For each pair of proteins (A, B):
1. Identify A's anchor position.
2. Map it to alignment column c.
3. Find which residue position in B corresponds to column c.
4. Check B's projection score at that position. Is it in the top-k?

Report: when we transfer the anchor position via structural alignment, what fraction of the time does the transferred position land in the target protein's top-1, top-3, top-5, top-10 by projection score?

Compare against transfer via sequence alignment (BLOSUM-based or from Foldseek's sequence-only alignment if available).

---

## Phase 4: Visualization

### Option A: Add to structure viewer

Extend `scripts/anchor_structure_viewer.py` to include the new proteins. For each, color residues by L10H9 projection score and highlight the anchor position. This gives a visual check: do the bright spots (high projection score) occur at structurally equivalent positions?

### Option B: Alignment-annotated projection plot

For each alignment column, plot the mean projection score across all proteins (after mapping each protein's scores to alignment coordinates). Columns where anchor positions cluster should show peaks.

---

## Implementation

### Script: `scripts/structure_anchor_transfer.py`

```bash
uv run python scripts/structure_anchor_transfer.py --device cuda
```

### Inputs
- `data/foldmason/foldmason_aa.fa` — multiple structure alignment (amino acid)
- `data/foldmason/foldmason_ss.fa` — secondary structure alignment
- `data/foldmason/foldmason.nw` — guide tree (not strictly needed but useful)
- PDB files for each protein (downloaded in Step 1.2)
- ESM2-650M model weights (same as other scripts)

### Key functions to reuse
- `load_model()`, `extract_head_weights()`, `compute_search_dir_from_full_seq()` from `scripts/anchor_behavior_audit.py`
- `analyze_protein()` from `scripts/anchor_behavior_audit.py` (for the anchor-like metrics)
- Alignment parsing: write new, but straightforward FASTA parsing with gap tracking

### New code needed
1. Parse foldmason FASTA alignment → ungapped sequences + column-to-position mappings
2. Download PDB files (can use `requests` to fetch from RCSB)
3. Anchor column concordance analysis
4. Projection score transfer analysis
5. Visualization (extend structure viewer or new alignment-projection plot)

---

## Outputs

- `reports/outputs/multi_protein/structure_anchor_transfer.md` — main report
- `reports/outputs/multi_protein/structure_anchor_transfer_audit.csv` — per-protein anchor behavior metrics
- `reports/outputs/multi_protein/structure_anchor_transfer_concordance.csv` — pairwise anchor column distances
- `reports/outputs/multi_protein/structure_anchor_transfer_projection.png` — mean projection score by alignment column
- `reports/outputs/multi_protein/structure_anchor_transfer_heatmap.png` — projection score heatmap (proteins x alignment columns)

---

## Success criteria

### Strong success
- Most (>7/10) new proteins show anchor-like L10H9 behavior (top1_mass > 0.15, rank_corr > 0.3).
- Anchor positions cluster within 3-5 alignment columns across proteins.
- Projection score transfer via structural alignment yields top-5 hit rate > 50%.
- The alignment column with 1PVGA's anchor (position 101) is also high-scoring in the majority of structural homologs.

Interpretation: L10H9 detects a structurally conserved landmark, not a sequence motif. This is direct evidence for "structure-linked anchor."

### Moderate success
- Most proteins are anchor-like, but anchor positions are spread across 2-3 distinct alignment column clusters rather than one.

Interpretation: there may be multiple structurally conserved anchor sites per fold, and L10H9 picks one depending on context. Still structural, but not a single landmark.

### Negative result
- Anchor positions do not cluster in alignment space any more than random buried positions.

Interpretation: anchorhood is not conserved across the fold at the resolution of structural alignment. The anchor may depend on fine sequence details or local packing, not fold-level topology.

---

## Compute estimate

- 11 proteins × 1 forward pass each for the behavior audit: ~2 seconds total
- Per-protein search direction computation: ~2 seconds each
- Pairwise transfer: 11 × 10 = 110 pairs, but we already have projection scores from the audit, so no extra forward passes
- Total: under 1 minute on GPU. The bottleneck is data preparation, not compute.

---

## Caveats and things to verify before interpreting

1. **Assembly duplicates**: 3zkb/3zkd/3zm7 may be the same protein in different crystal forms, and 3cwv has two assemblies. Check pairwise sequence identity within the set. If duplicates exist, treat them as one entry to avoid inflating concordance.
2. **Alignment quality**: foldmason alignment has many gap columns. Verify that the alignment is sensible around 1PVGA position 101 (the known anchor). If that region is poorly aligned, the experiment cannot answer the question.
3. **Sequence length**: some alignment entries look truncated (3zm7-assembly3 starts at column ~14). Verify that the ungapped sequences are long enough for ESM2 to produce meaningful representations.
4. **Search direction**: we use the 2B61A-derived reference direction d. Also compute protein-specific d_self for each new protein and check cosine similarity with the reference. If they diverge, report both sets of anchor positions.

---

## Notes

This experiment is cheap, fast, and directly addresses the central question of the paper: is the anchor a structural feature or a sequence feature? The 4_8.md notes correctly identify this as the highest-value experiment. A clean positive result here would be the strongest piece of evidence in the paper. A clean negative result would also be valuable — it would redirect the story toward sequence-level explanations.

The 10 proteins from foldseek are a pilot. If the result is positive, extend to more folds and more proteins per fold (the 4_8.md notes suggest doing this for each of our 18 known anchor proteins).
