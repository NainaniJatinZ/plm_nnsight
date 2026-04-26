# Structure Anchor Transfer v2: Cross-Family Summary

## Setup

We tested whether ESM2's L10H9 attention head places its anchor (the dominant key position by attention mass) at structurally equivalent positions across sequence-diverse structural homologs.
Two protein families were tested independently, each assembled from Foldseek hits with TM > 0.6 and pairwise sequence identity < 20% to the reference protein.
After assembly collapse and single-linkage deduplication at 90% identity:

| Family | Reference | Fold | n (after dedup) | Alignment length | Functional groups |
|--------|-----------|------|-----------------|-----------------|-------------------|
| 1PVGA | DNA gyrase B | GHKL ATPase / Bergerat fold | 20 | 999 columns | DNA gyrases, topoisomerases, HSP90, MutL, histidine kinases |
| 2B61A | Homoserine transacetylase | Alpha/beta hydrolase | 101 | 431 columns | Epoxide hydrolases, esterases, dehalogenases, lactonases, haloperoxidases, strigolactone receptors, NDRG proteins, C-C bond hydrolases, iminopeptidases |

## Finding 1: Anchor positions converge on structurally equivalent sites

In both families, the top-1 anchor positions cluster at a single alignment column far more tightly than expected by chance.

| Metric | 1PVGA | 2B61A |
|--------|-------|-------|
| Dominant anchor column | 122 | 64 |
| Proteins at dominant column | 20/20 (100%) | 95/101 (94%) |
| Top-1 exact pairwise match | 190/190 (100%) | 4472/5050 (88.5%) |
| Top-1 within 5 columns | 190/190 (100%) | 4662/5050 (92.3%) |
| Anchor mean pairwise distance | 0.0 | 22.2 |
| Random mean pairwise distance (200 trials) | 216.3 +/- 27.6 | 133.1 +/- 6.2 |
| Anchor tighter than X% of random | 100% | 100% |

The 6 outliers in the 2B61A set (anchoring at columns 352 or 66 instead of 64) include 3 NDRG proteins (which have the alpha/beta hydrolase fold but have lost catalytic activity) and 3 esterases from the Abhydrolase_6 sub-family.

## Finding 2: Secondary anchor sites are shared across proteins

Top-3 anchor analysis reveals additional consensus columns that are shared across proteins.
In both families, the "outlier" anchor positions are not noise — they correspond to secondary anchor sites present in the top-3 for most or all proteins.

| Family | Consensus columns (top-3, >25% of proteins) |
|--------|----------------------------------------------|
| 1PVGA | 123 (100%), 179 (95%), 536 (40%) |
| 2B61A | 64 (100%), 352 (100%), 171 (46%), 196 (27%) |

In 2B61A, columns 64 and 352 both appear in the top-3 anchors of all 101 proteins.
The 4 proteins whose top-1 anchor is at column 352 simply have their ranking of these two sites swapped.

Top-3 pairwise min set distance is 0.0 for both families (190/190 and 5047/5050 exact matches respectively).

## Finding 3: Structural conservation at the anchor exceeds sequence conservation

The 3Di structural alphabet encodes local backbone geometry.
At the anchor position, 3Di information content is maximal (4.322 bits = perfect conservation of a single 3Di letter) in both families, while amino acid IC is lower.

| Metric | 1PVGA | 2B61A |
|--------|-------|-------|
| AA IC at anchor | 3.065 bits | 2.709 bits |
| 3Di IC at anchor | 4.322 bits (max) | 4.322 bits (max) |
| AA mean IC (+-25 window) | 2.212 bits | 1.097 bits |
| 3Di mean IC (+-25 window) | 2.790 bits | 2.144 bits |

The anchor residue is hydrophobic in 95% (1PVGA) and 99% (2B61A) of proteins, but the specific amino acid varies (V, I, L, C, M, F, A).
The 3Di letter is perfectly conserved.
This means: the local backbone geometry at the anchor is identical across all proteins in each family, even when the amino acid identity is not.

## Finding 4: Local sequence identity is elevated around the anchor

In both families, pairwise sequence identity in the +-25 residue window around the anchor is significantly higher than the global pairwise identity.

| Metric | 1PVGA | 2B61A |
|--------|-------|-------|
| Global mean pairwise seq identity | 0.298 | 0.182 |
| Local (+-25) mean pairwise seq identity | 0.327 | 0.242 |
| t-test | t=4.76, p=3.83e-06 | t=54.12, p~0 |

This means we cannot fully rule out that local sequence features contribute to anchor placement.
The anchor region is more sequence-conserved than average, which is expected for a structurally important region, but it prevents us from cleanly attributing anchor placement to structure alone.

## What these results support

1. L10H9's anchor placement is non-random with respect to 3D structure. Across two unrelated folds and 121 proteins with <20% sequence identity, the anchor lands at structurally equivalent alignment positions. This is tighter than 100% of random position controls in both families.

2. The anchor position marks a site of high structural conservation. 3Di IC is maximal at the anchor in both families, meaning the local backbone geometry is identical across all tested homologs. The amino acid at that position is strongly biased toward hydrophobic residues but is not a single conserved amino acid.

3. Multiple structurally conserved anchor sites exist per fold. Both families show 2-3 consensus columns in the top-3 analysis. This is consistent with the fold having multiple structural landmarks that L10H9 can lock onto.

## What these results do not establish

1. We do not establish that ESM2 uses structural information per se. ESM2 is a sequence-only model. The elevated local sequence conservation around the anchor (Finding 4) means that sequence features correlated with structure could be sufficient. The model may be detecting a local sequence pattern that happens to be structurally conserved, rather than inferring structure.

2. We do not establish what the anchor position represents biologically. The anchor could correspond to a catalytic site, a hydrophobic core residue, a folding nucleus, or some other structural feature. We have not mapped the anchor to any specific functional or structural annotation.

3. We do not establish generality beyond these two folds. GHKL ATPases and alpha/beta hydrolases are both well-represented in training data. The result may not hold for rarer folds or for proteins with less training data coverage.

4. The 1PVGA result (20 proteins, 100% exact match) is suspiciously clean. With only 20 proteins after 90% identity deduplication, and the fact that many of these are DNA gyrases with potentially correlated sequence features, the effective independence of samples may be lower than 20. The 2B61A result (101 proteins, 94% at dominant column) is more convincing as an independent test.

## Interpretation (per experiment design matrix)

| Concordance | Local seq conservation | 3Di > AA IC | Observed | Interpretation |
|---|---|---|---|---|
| Strong | High | Yes | Both families | Anchor is at a structurally conserved site, but local sequence conservation prevents clean separation of structural vs sequence signal |

Both families fall in the same cell of the interpretation matrix.
The structural signal (3Di) is stronger than the sequence signal (AA) at the anchor, but the sequence signal is not absent.
