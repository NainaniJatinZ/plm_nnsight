# Anchor Information-Hub Experiment v1

## Methodology

This experiment tests whether anchor residues (high L10H9 projection score positions) function as information hubs.

Two tracks: (A) EVcouplings-based coupling feature analysis on 4 proteins with MSA data, and (B) ESM conditional influence test on all 18 proteins.

Matched controls: 5 per anchor, matched on SSE type, RSA, and contacts_8A, with top-10% projection rank excluded.

## Matched control summary

| Protein | Anchor | SSE | N controls | Tolerance tier |
|---------|--------|-----|------------|----------------|
| 1BRTA | 220 | E | 5 | 0 |
| 1PVGA | 101 | E | 5 | 0 |
| 2B61A | 315 | E | 5 | 0 |
| 2DPMA | 39 | E | 5 | 0 |
| 2PKEA | 131 | E | 0 | -1 |
| 2QY6A | 64 | E | 5 | 0 |
| 2YHWA | 287 | E | 5 | 0 |
| 3CSSA | 40 | E | 5 | 0 |
| 3HO7A | 63 | E | 5 | 0 |
| 3OKPA | 200 | E | 5 | 0 |
| 3QDLA | 114 | H | 0 | -1 |
| 3WJPA | 94 | E | 5 | 0 |
| 4EHUA | 100 | C | 5 | 0 |
| 4EX6A | 124 | E | 5 | 2 |
| 4EZIA | 310 | E | 5 | 0 |
| 4ME3A | 75 | H | 5 | 0 |
| 4N9WA | 194 | E | 5 | 0 |
| 4OY3A | 193 | E | 5 | 0 |

## Part A: EVcouplings coupling features

Proteins with coupling data: 1BRTA, 1PVGA, 2B61A, 2DPMA

### Per-protein anchor vs control comparison

| Protein | Feature | Anchor | Control mean | Diff | z-score | Anchor > all? |
|---------|---------|--------|-------------|------|---------|---------------|
| 1BRTA | sum_longrange_score | -182.37 | -215.03 | 32.66 | 0.51 | no |
| 1BRTA | n_longrange_pairs | 207.00 | 213.00 | -6.00 | -0.67 | no |
| 1BRTA | n_coupling_bins | 10.00 | 10.00 | 0.00 | 0.00 | no |
| 1BRTA | coupling_bin_entropy | 3.29 | 3.28 | 0.01 | 0.52 | no |
| 1BRTA | n_distinct_sse_segments | 41.00 | 40.60 | 0.40 | 0.73 | no |
| 1PVGA | sum_longrange_score | -710.61 | -770.24 | 59.63 | 4.69 | yes |
| 1PVGA | n_longrange_pairs | 320.00 | 322.40 | -2.40 | -1.58 | no |
| 1PVGA | n_coupling_bins | 10.00 | 10.00 | 0.00 | 0.00 | no |
| 1PVGA | coupling_bin_entropy | 3.29 | 3.29 | -0.00 | -0.28 | no |
| 1PVGA | n_distinct_sse_segments | 68.00 | 66.80 | 1.20 | 0.92 | no |
| 2B61A | sum_longrange_score | -615.95 | -656.00 | 40.05 | 1.16 | yes |
| 2B61A | n_longrange_pairs | 284.00 | 290.80 | -6.80 | -1.18 | no |
| 2B61A | n_coupling_bins | 10.00 | 10.00 | 0.00 | 0.00 | no |
| 2B61A | coupling_bin_entropy | 3.27 | 3.26 | 0.01 | 0.44 | no |
| 2B61A | n_distinct_sse_segments | 62.00 | 61.40 | 0.60 | 0.67 | no |
| 2DPMA | sum_longrange_score | -345.68 | -328.96 | -16.72 | -0.08 | no |
| 2DPMA | n_longrange_pairs | 203.00 | 168.20 | 34.80 | 0.37 | no |
| 2DPMA | n_coupling_bins | 10.00 | 8.00 | 2.00 | 0.45 | no |
| 2DPMA | coupling_bin_entropy | 3.30 | 2.64 | 0.66 | 0.45 | no |
| 2DPMA | n_distinct_sse_segments | 47.00 | 37.20 | 9.80 | 0.47 | no |

### Cross-protein paired tests (N=4, treat as descriptive)

| Feature | Mean diff | Cohen's d | t-test p | Wilcoxon p |
|---------|-----------|-----------|----------|------------|
| sum_longrange_score | 28.906 | 0.890 | 0.1731 | 0.2500 |
| n_longrange_pairs | 4.900 | 0.245 | 0.6581 | 0.8750 |
| n_coupling_bins | 0.500 | 0.500 | 0.3910 | 1.0000 |
| coupling_bin_entropy | 0.171 | 0.523 | 0.3728 | 0.2500 |
| n_distinct_sse_segments | 3.000 | 0.660 | 0.2786 | 0.1250 |

### Anchor rank in coupling space

| Protein | Feature | Anchor rank | Total residues | Percentile |
|---------|---------|-------------|----------------|------------|
| 1BRTA | sum_longrange_score | 51 | 277 | 81.6 |
| 1BRTA | n_longrange_pairs | 122 | 277 | 56.0 |
| 1BRTA | n_coupling_bins | 1 | 277 | 99.6 |
| 1BRTA | coupling_bin_entropy | 92 | 277 | 66.8 |
| 1BRTA | n_distinct_sse_segments | 88 | 277 | 68.2 |
| 1PVGA | sum_longrange_score | 98 | 418 | 76.6 |
| 1PVGA | n_longrange_pairs | 183 | 418 | 56.2 |
| 1PVGA | n_coupling_bins | 1 | 418 | 99.8 |
| 1PVGA | coupling_bin_entropy | 211 | 418 | 49.5 |
| 1PVGA | n_distinct_sse_segments | 115 | 418 | 72.5 |
| 2B61A | sum_longrange_score | 61 | 377 | 83.8 |
| 2B61A | n_longrange_pairs | 246 | 377 | 34.7 |
| 2B61A | n_coupling_bins | 1 | 377 | 99.7 |
| 2B61A | coupling_bin_entropy | 90 | 377 | 76.1 |
| 2B61A | n_distinct_sse_segments | 104 | 377 | 72.4 |
| 2DPMA | sum_longrange_score | 61 | 284 | 78.5 |
| 2DPMA | n_longrange_pairs | 204 | 284 | 28.2 |
| 2DPMA | n_coupling_bins | 1 | 284 | 99.6 |
| 2DPMA | coupling_bin_entropy | 109 | 284 | 61.6 |
| 2DPMA | n_distinct_sse_segments | 64 | 284 | 77.5 |

## Part B: ESM conditional influence

For each protein, masked the anchor and 5 matched controls as source residues, measured influence on 16 distant targets (|i-j| >= 24).

influence(i->j) = logP(true_j | mask_j) - logP(true_j | mask_i, mask_j)

### Per-protein results

| Protein | Anchor mean | Control mean | Diff | Anchor n_pos | Control n_pos | Anchor > ctrl mean? |
|---------|-------------|--------------|------|-------------|---------------|---------------------|
| 1BRTA | -0.0049 | -0.0040 | -0.0010 | 11 | 8.6 | no |
| 1PVGA | -0.0002 | -0.0041 | 0.0039 | 6 | 6.6 | yes |
| 2B61A | 0.0483 | 0.0037 | 0.0445 | 10 | 9.4 | yes |
| 2DPMA | 0.0033 | 0.0032 | 0.0000 | 11 | 9.0 | yes |
| 2QY6A | 0.0052 | -0.0023 | 0.0075 | 10 | 6.4 | yes |
| 2YHWA | -0.0025 | 0.0027 | -0.0052 | 8 | 7.8 | no |
| 3CSSA | 0.0008 | 0.0016 | -0.0008 | 9 | 9.0 | no |
| 3HO7A | 0.0020 | 0.0074 | -0.0054 | 7 | 7.4 | no |
| 3OKPA | 0.0177 | -0.0018 | 0.0195 | 8 | 7.6 | yes |
| 3WJPA | -0.0030 | 0.0018 | -0.0048 | 6 | 9.4 | no |
| 4EHUA | -0.0012 | -0.0023 | 0.0011 | 6 | 8.2 | yes |
| 4EX6A | 0.0002 | 0.0058 | -0.0056 | 8 | 7.6 | no |
| 4EZIA | 0.0116 | -0.0043 | 0.0159 | 10 | 7.2 | yes |
| 4ME3A | 0.0580 | 0.0065 | 0.0516 | 11 | 8.0 | yes |
| 4N9WA | 0.0035 | -0.0023 | 0.0058 | 7 | 6.8 | yes |
| 4OY3A | 0.0076 | -0.0060 | 0.0137 | 8 | 6.6 | yes |

### Cross-protein paired test

N = 16

Mean difference (anchor - control mean): 0.0088

Cohen's d: 0.511

Paired t-test p: 0.0588

Wilcoxon signed-rank p: 0.0934


## Combined interpretation

Part B: anchor beats control mean in 10/16 proteins.

Part A: anchor has higher coupling features in 4 / 8 (protein x feature) comparisons.

