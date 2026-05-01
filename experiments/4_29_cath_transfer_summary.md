# 4_29 — Cross-fold anchor transfer (Option B from prior planning)

Goal: replace the within-Pfam HMM-coordinate framing of E1' with a cross-Pfam, cross-HSF, cross-fold structural test of where L10H9 places its anchor. The original three pre-registered hypotheses were per-Pfam family detection, fold-level recognition, and sequence-distant homology.

Headline. The pre-registered taxonomic framing was the wrong axis. Anchor-column concordance is a smooth monotonic function of pairwise TM-score across the entire corpus; Pfam / HSF / fold labels add essentially nothing once TM is controlled for. The defensible claim is: L10H9's anchor reads a structurally-recognizable feature whose cross-protein transferability decays smoothly with structural divergence. This is a stronger, cleaner, and more parsimonious story than any of the three original hypotheses, and it absorbs the within-Pfam result from E1' as a corollary (within-Pfam pairs are simply the high-TM tail of the same curve).

## Design

Three sets sampled from CATH + SIFTS Pfam annotation:

| Set | CATH H-superfamily | Description | Pfams | Chains |
|---|---|---|---|---|
| A | 3.40.50.720 | Rossmann NAD-binding | PF13561, PF00106, PF01370, PF00107, PF08240, PF01408 | 60 |
| B | 3.40.50.1820 | α/β hydrolase | PF00561, PF12697, PF07859, PF00756 | 39 |
| C | 2.60.40.10 | Ig-like β-sandwich | PF00041, PF07686, PF07679 | 30 |

A and B share the same fold (3.40.50, "Rossmann fold" in CATH; some classifications treat α/β-hydrolase as a distinct fold — flag this in methods), different H-superfamilies. C is a different fold class (2.60.40, all-β). Total 129 chains, 13 Pfams, 3 H-superfamilies, 2 folds. S35-deduped to avoid near-identical chains.

Manifest: `data/cath/struc_transfer_manifest.csv`.

## Pipeline

`scripts/anchor_cath_transfer.py`, stages: download → extract → anchors → msa → concord → baseline → tm → pairs → regression.

- PDBs from RCSB (one CIF fallback; all 129 chains extracted).
- ESM2-650M L10H9 anchors per chain via NNsight trace; record top-3 attention positions, top1_mass, keys_50pct, d-vs-attn argmax agreement, Spearman(d-projection, attention).
- Foldmason `easy-msa` for structural MSAs per set + a combined ALL MSA. The ALL MSA across 2 folds is biologically thin (Ig and α/β are not structurally alignable across the full chain); used as supporting context, not primary signal — the TM regression does not depend on it.
- All-vs-all foldseek `easy-search` (`--alignment-type 2 --exhaustive-search 1`) for pairwise TM-scores.
- Random-shuffle baselines (200 trials per group) to test concordance significance.

## Key results

### 1. d-projection vs L10H9 attention transfers across folds at the rank level
- Spearman(d, attn) high across all sets: A 0.96, B 0.95, C 0.95 — d's ranking of positions transfers across folds.
- Argmax-agreement varies: A 0.97, B 0.74, C 0.70 — the very top position can flip when 2–3 candidates are near-tied.
- Implications: switched anchor call to attn-argmax (the audit's `top_key_idx`), and added a top-3 metric to absorb the tie-flip. The QK information itself is fold-general at the rank level; only the argmax is fold-dependent.

### 2. Audit-pass rate is fold-biased toward the reference protein's class

| Set | n | top1_mass median | keys_50pct=1 frac | audit-pass |
|---|---|---|---|---|
| A | 60 | 0.50 | 0.45 | 27 (45%) |
| B | 39 | 0.61 | 0.82 | 32 (82%) |
| C | 30 | 0.50 | 0.50 | 15 (50%) |

The α/β hydrolase chains anchor most confidently. The reference protein 2B61A is α/β hydrolase, so this is partly home-court advantage; it also means the head's anchor confidence is fold-class-dependent. Methods text needs this caveat: "audit-passing chain" is itself a fold-correlated filter and we report results both with and without it where it changes anything.

### 3. Concordance significantly above random null in every group
200-trial shuffle baselines (`baseline_random_audit.csv`):

- Within-Pfam (audit-pass): observed top-1 conc median 0.76–0.88, null median 0.13–0.25. All 13 Pfams individually significant.
- Per-HSF in own MSA: obs 0.33–0.80, null 0.05–0.12. All 3 HSFs significant.
- Per-set in ALL MSA: obs 0.16, null 0.03 (p<0.05).

### 4. Within-Pfam structural-MSA concordance holds in all three folds
Top-1 median ≥ 0.76; top-3 (any in mode ±2) median ≥ 0.83 in every fold. The L10H9 anchor lands at a Pfam-canonical structural column in Rossmann, α/β-hydrolase, and Ig β-sandwich.

This subsumes E1's within-Pfam-HMM-column result and replaces it with a structural-MSA version that does not depend on the AA HMM. Caveat for Set C: the 3 Ig Pfams (Fibronectin III, Ig V-set, Ig I-set) are siblings within the Ig superfamily, so Set C's within-Pfam concordance is *also* sampling high-TM pairs by construction. The headline within-Pfam result holds, but the Set C numbers shouldn't be over-read as independent fold-level evidence.

### 5. Taxonomic categories collapse under TM-control
Pairwise TM and pairwise anchor-MSA-column distance (n=2346 audit-pass pairs, `pairs.csv`):

| Category | n | TM med | seq-id med | anchor-dist med | within ±2 |
|---|---|---|---|---|---|
| within_pfam | 195 | 0.70 | 0.16 | 0 | 66% |
| cross_pfam_same_hsf | 697 | 0.44 | 0.10 | 94 | 27% |
| cross_hsf_same_fold | 864 | 0.17 | 0.08 | 303 | 0% |
| cross_fold | 590 | 0.08 | 0.06 | 537 | 0% |

In any TM bin where multiple categories coexist, within_pfam and cross_pfam_same_hsf give essentially identical rates (TM 0.7–0.8: 0.68 vs 0.73; TM 0.8–0.9: 0.92 vs 0.94). The category dummies do not separate the curves.

Logistic regression `same_col ~ tm + category`:
- All pairs: TM-only McFadden R² = 0.484; full R² = 0.517 (Δ = 0.033). LR test significant (p ≈ 3e-13) but coefficients are quasi-separated — within-Pfam pairs have no overlap below TM 0.3, cross-fold pairs have none above TM 0.3 — so the all-pairs regression confounds category with TM range.
- Overlap range TM ∈ [0.3, 0.8] (n=673): TM-only R² = 0.131; full R² = 0.138 (Δ = 0.007). LR p = 0.042. Would not survive multiple-comparison correction.

The honest reading: in the TM range where multiple taxonomic categories coexist, category labels add 0.7 percentage points of R². The "fold-level vs Pfam-level" framing was a discretization of TM-similarity; once TM is on the axis, the discretization adds essentially nothing.

Plot: `reports/out2/cath_transfer/anchor_concord_vs_tm.png`.

### 6. TM-score predicts anchor transfer better than sequence identity
Across n=1825 pairs:
- TM only McFadden R² = 0.435
- seq-id only McFadden R² = 0.289
- TM + seq-id McFadden R² = 0.442 (seq-id adds ≈ 0.007 over TM)

TM and seq-id are correlated (Spearman ρ = 0.57). Caveat: seq-id range in this corpus is squashed to 0.04–0.40 because we sampled cross-Pfam-low-identity pairs by construction; seq-id's ceiling is artificially low here. Honest framing: in this low-seq-id regime, TM is the better predictor and seq-id adds little; we cannot claim TM beats seq-id at higher seq-id from this data alone.

## What this means

Defensible claims for the draft:

1. The L10H9 anchor lands on a structural column whose cross-protein conservation is captured by pairwise TM-score. A single TM-driven curve fits the relationship across all taxonomic levels we tested.
2. Within a Pfam, the anchor lands on the same structural column at top-3 ≥ 0.83 in every fold class tested (Rossmann, α/β-hydrolase, Ig). This is the structural-MSA replication of E1'.
3. There is no detectable taxonomic threshold (Pfam, HSF, fold) for anchor transfer once TM-score is partialed out. Within the TM range our corpus samples (0.05–0.97), the curve is monotonic and smooth.
4. The Set A vs Set B asymmetry observed earlier ("hydrolase shows fold-level transfer, Rossmann shows Pfam-level") is a TM-asymmetry between the sets, not a head-mechanism asymmetry. The 4 hydrolase Pfams have uniformly high pairwise TM (~0.7+); the 6 Rossmann Pfams have a wider TM spread.
5. TM ≈ 0.6 is the empirical crossover in this corpus where same-column rate exceeds 50%. Treat this number as corpus-specific (depends on how the structural MSA is built and the chains sampled), not as a universal threshold.

What we are *not* claiming:

- We are not claiming the head detects "fold." That framing was the discretization; the underlying variable is structural similarity.
- We are not claiming the structural feature is "buried hydrophobic core packing." Prior agent work showed the anchor is universally buried and hydrophobic-dominant in this set (and never on charged catalytic residues), but that finding is over-determined as an explanation, and the TM-driven transfer here is consistent with several mechanisms (see open issues).
- We are not claiming the head is robust outside α/β folds. Audit-pass rate drops sharply outside the α/β-hydrolase reference class; the within-Ig results hold for the audit-passing subset only.

## Caveats

- NNsight wrapping: `anchor_hmm_experiment.load_model` returns a raw HF model; needs `NNsight(raw_model)` wrap before `model.trace()`. Bug burned one ESM run; fix is in `scripts/anchor_cath_transfer.py:_load_model`.
- Tri-set (ALL) MSA across A∪B∪C is biologically thin because Ig and α/β-hydrolase don't structurally align across the full chain; foldmason produces a forced alignment. The per-HSF and per-set numbers from the ALL MSA are reported as supporting context only — the discriminating analysis is the pairwise TM regression, which doesn't depend on the joint MSA quality.
- Set C is 3 Ig-superfamily siblings (Fibronectin III, Ig V-set, Ig I-set). Within-HSF concordance there (0.80) is partly an artifact of high pairwise TM among siblings. Confirmed by the regression.
- Audit filter is fold-biased (B 82% vs A 45% vs C 50%). Methods needs to flag this; report key numbers both with and without the filter.
- Reference d-direction comes from 2B61A (α/β hydrolase). Spearman is fine across folds but the d-argmax flips outside α/β-hydrolase; using attn-argmax avoids this.
- PF00756 capped at 9 of 10 chains due to S35-pool exhaustion. Not a problem.
- TM regression has quasi-separation in the full range (within-Pfam pairs have no TM<0.3 overlap, cross-fold pairs have no TM>0.3 overlap). Use the overlap-range subset for the cleaner test.
- 52% of variance in same-column rate is unexplained by TM. We have not yet checked whether this residual is structured (anchor-confidence, multi-anchor chains, Pfam-after-TM-control) or noise.
- "No taxonomic threshold" is "no threshold within the TM range our corpus samples." Strictly, the claim is corpus-bounded.

## How this reshapes the paper

The original three-experiment plan (E1' within-Pfam HMM coordinate, E2 conserved-residue corruption, E3 3Di vs AA clustering) anticipated a "the head is a structural-feature detector" claim built up from three angles. The TM-vs-concordance result lets us replace the level-of-recognition framing entirely:

- E1' becomes "within-Pfam transfer is the high-TM tail of a single curve." Don't write it up as a separate result.
- The current experiment becomes the headline locality-and-transfer result.
- E2 (locality + identity-vs-class at conserved positions) and E3 (3Di > AA NMI) become the *mechanistic* support: the anchor is local, it depends on conserved-residue identity beyond physicochemical class, and the structural alphabet is more predictive than the AA alphabet for cross-protein clustering. These compose into "the local feature the head reads is structurally-recognizable, identity-specific at conserved positions."
- The combined story is then: anchor transfers smoothly with TM (this experiment), the relevant information lives in a local window (E2a), conserved AA identity at high-IC positions is causally necessary (E2b), and 3Di clusters where AA does not (E3). One coherent picture, no level-of-recognition commitment.

## Open questions (priority order)

1. What does the residual variance look like? 52% of variance in same-column rate is unexplained by TM. Quick analysis: regress same_col ~ TM + (top1_mass_either_chain, multi-anchor indicator, mean_RSA_at_anchor, Pfam-after-TM-partial). 30 minutes of work; tells us whether residual is structured. If anchor-confidence is the main residual driver, we report that as a known limitation. If Pfam-after-TM is non-trivial, the "category labels are redundant" claim weakens.
2. Predictability null. The agent's earlier flag still stands: the head might pick whichever conserved positions are most predictable from local context. Compute per-position pseudo-perplexity from ESM and test whether the anchor sits at the predictability max or merely at a high-but-not-max value. This is the most pointed reviewer-pushback against any "the head reads structure" claim and is not addressed by the TM curve. Before draft.
3. Biological characterization of the modal anchor column (option c, refocused). With the TM framing in place, the question shifts from "what is the head doing in each HSF" to "what kind of structural feature does the head read across folds." For each chain, label anchor by structural role (DSSP SSE, position-along-element, distance from domain center, contact-density rank, RSA, distance to active-site if known), then compare role distributions across A, B, C. Two outcomes:
   - Same role across folds (e.g., always central buried residue of central β-strand) → the head reads a generic structural-feature class that maps to TM-equivalent positions.
   - Different roles across folds (Rossmann's NAD-binding crossover vs hydrolase's nucleophile-elbow-adjacent strand vs Ig's strand C-C' kink) → the head reads fold-specific structurally-defining features.
4. Tighten the curve. Logistic fit with 95% CI bands on the TM-vs-same-col plot for the paper figure. Report the TM at which same-col probability crosses 50% and 80%, with CIs.
5. Optional: cross-fold sample expansion (TIM-barrel 3.20.20, helix-bundle 1.10.x) to confirm the TM curve is universal. Probably not needed for first draft; this can be a "we replicated on additional folds" supplement.

## Key numbers

- Within-Pfam top-1 column concordance (audit-pass median): 0.76–0.88 (vs null ≈ 0.20). Top-3 (any in ±2): ≥ 0.83 in every fold.
- TM-only McFadden R² for predicting same-column: **0.484** (all pairs); **0.131** (overlap TM 0.3–0.8).
- Adding Pfam/HSF/fold dummies: +0.033 R² (all pairs, confounded by quasi-separation); +0.007 R² (overlap range, p = 0.04, would not survive correction).
- TM ≈ 0.6: corpus-specific crossover where same-column rate exceeds 50%.
- Audit-pass rate: A 45% / B 82% / C 50%. Fold-class-correlated.

## File map

```
data/cath/
  cath_parsed.parquet                         # CATH domain list (601k entries)
  struc_transfer_manifest.csv                 # 129 chains × 13 Pfams × 3 sets
data/sifts/
  pdb_chain_pfam.tsv.gz                       # SIFTS Pfam mapping
  pdb_chain_cath_uniprot.tsv.gz               # SIFTS CATH mapping

scripts/
  anchor_cath_transfer.py                     # all stages

reports/out2/cath_transfer/
  pdb/                                        # downloaded full PDBs
  chain_pdb/                                  # per-chain PDB extracts
  chain_seqs.json
  anchors.csv                                 # n=129, audit metrics + top-3 attn positions
  anchors.log
  msa/{A_3.40.50.720,B_3.40.50.1820,C_2.60.40.10,ALL}_aa.fa
  msa/{...}_3di.fa
  msa/{...}.nw
  pairwise_tm.tsv                             # foldseek easy-search all-vs-all
  pairs.csv                                   # 2346 audit-pass pairs (TM, seqid, anchor-dist, category)
  baseline_random_audit.csv                   # null-shuffle p-values per group
  concordance_{all,audit}.csv                 # top-1 + top-3 + ±2-tol concordance per group
  anchor_concord_vs_tm.png                    # the key figure
```
