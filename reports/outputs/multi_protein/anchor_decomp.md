# Anchor Decomposition via W_K SVD

Heads analyzed: L11H16, L10H9, L14H9

## L11H16

### W_K singular value spectrum

Top-5 singular values: 5.97, 5.68, 5.40, 5.08, 4.89
Fraction of variance in top-1/3/5: 0.052 / 0.142 / 0.215

### Step 1: Key norm analysis

| protein | anchor_pos | aa | k_norm | rank | percentile | zscore | frac_top1 | frac_top3 | proj_top1_rank |
|---------|-----------|----|---------|----|-----------|--------|----------|----------|---------------|
| 1PVGA | 101 | V | 10.680 | 6 | 98.6 | 2.85 | 0.000 | 0.063 | 418 |
| 1YKIA | 129 | K | 10.159 | 38 | 82.5 | 0.73 | 0.372 | 0.516 | 25 |
| 1YKIA | 130 | D | 9.851 | 80 | 63.1 | 0.21 | 0.332 | 0.462 | 54 |
| 2B61A | 157 | I | 11.841 | 4 | 98.9 | 3.96 | 0.058 | 0.118 | 342 |
| 2B61A | 315 | T | 12.330 | 2 | 99.5 | 4.79 | 0.000 | 0.063 | 377 |
| 2EK8A | 243 | G | 12.857 | 3 | 99.3 | 3.93 | 0.062 | 0.079 | 383 |
| 2FBQA | 47 | F | 16.466 | 1 | 99.6 | 7.87 | 0.001 | 0.015 | 235 |

Mean anchor key norm Z-score: 3.48 (std 2.39)
Mean anchor percentile: 91.6%

### Step 2: Anchor direction correlations

#### AA embedding cosine similarity (top 5, averaged across proteins)

| AA | mean cos | std |
|----|----------|-----|
| T | 0.0557 | 0.0137 |
| E | 0.0244 | 0.0197 |
| A | 0.0146 | 0.0205 |
| N | 0.0036 | 0.0150 |
| G | 0.0005 | 0.0117 |

#### SSE projection (mean dot product with anchor direction)

| protein | helix | strand | coil |
|---------|-------|--------|------|
| 1PVGA | 0.7644 | 0.8478 | 0.8129 |
| 1YKIA | 1.8401 | 1.7715 | 1.8680 |
| 2B61A | 1.0829 | 1.0595 | 0.9493 |
| 2EK8A | 0.8006 | 0.5750 | 0.6020 |
| 2FBQA | 0.7492 | 0.0000 | 0.7773 |

#### Position projection profile: anchor rank

For each protein, we compute dot(x_ln_j, d_resid_nobias) for all j and rank the anchor position.

| protein | anchor_pos | projection_rank | n_residues |
|---------|-----------|----------------|-----------|
| 1PVGA | 101 | 1 | 418 |
| 1YKIA | 129 | 13 | 217 |
| 1YKIA | 130 | 59 | 217 |
| 2B61A | 157 | 1 | 377 |
| 2B61A | 315 | 3 | 377 |
| 2EK8A | 243 | 1 | 421 |
| 2FBQA | 47 | 1 | 235 |

### Step 3: Cross-protein anchor direction comparison

#### Key vectors (raw)

Anchor-anchor pairwise cosine: mean=0.5026, std=0.1511, n=10
Anchor-random control cosine: mean=0.4703, std=0.1985, n=20
Mann-Whitney U (anchor > control): U=116.0, p=0.2476

#### Key vectors (nobias)

Anchor-anchor pairwise cosine: mean=0.4733, std=0.1409, n=10
Anchor-random control cosine: mean=0.4487, std=0.2154, n=20
Mann-Whitney U (anchor > control): U=118.0, p=0.2207

Bias contamination check: raw mean cos - nobias mean cos = 0.0292
Bias contribution is small (delta <= 0.05).

#### Pairwise cosine similarity (nobias)

| protein_i | protein_j | cosine |
|-----------|-----------|--------|
| 2B61A | 2EK8A | 0.7152 |
| 1PVGA | 2EK8A | 0.6008 |
| 1PVGA | 2B61A | 0.5767 |
| 1PVGA | 2FBQA | 0.5610 |
| 2B61A | 2FBQA | 0.5078 |
| 2EK8A | 2FBQA | 0.4985 |
| 1YKIA | 2FBQA | 0.3841 |
| 1PVGA | 1YKIA | 0.3218 |
| 1YKIA | 2B61A | 0.3055 |
| 1YKIA | 2EK8A | 0.2621 |

---

## L10H9

### W_K singular value spectrum

Top-5 singular values: 6.95, 6.18, 5.84, 5.57, 5.01
Fraction of variance in top-1/3/5: 0.064 / 0.159 / 0.233

### Step 1: Key norm analysis

| protein | anchor_pos | aa | k_norm | rank | percentile | zscore | frac_top1 | frac_top3 | proj_top1_rank |
|---------|-----------|----|---------|----|-----------|--------|----------|----------|---------------|
| 1BRTA | 220 | L | 13.588 | 2 | 99.3 | 6.13 | 0.008 | 0.169 | 273 |
| 1PVGA | 101 | V | 12.905 | 1 | 99.8 | 4.54 | 0.163 | 0.183 | 62 |
| 2B61A | 315 | T | 13.458 | 1 | 99.7 | 7.45 | 0.027 | 0.164 | 365 |
| 2DPMA | 39 | F | 12.202 | 2 | 99.3 | 5.09 | 0.021 | 0.025 | 279 |
| 2PKEA | 131 | L | 12.212 | 2 | 99.2 | 4.28 | 0.000 | 0.003 | 250 |

Mean anchor key norm Z-score: 5.50 (std 1.17)
Mean anchor percentile: 99.5%

### Step 2: Anchor direction correlations

#### AA embedding cosine similarity (top 5, averaged across proteins)

| AA | mean cos | std |
|----|----------|-----|
| L | 0.0425 | 0.0189 |
| T | 0.0381 | 0.0112 |
| K | 0.0315 | 0.0140 |
| D | 0.0187 | 0.0146 |
| R | 0.0160 | 0.0071 |

#### SSE projection (mean dot product with anchor direction)

| protein | helix | strand | coil |
|---------|-------|--------|------|
| 1BRTA | 0.7165 | 0.8668 | 0.7102 |
| 1PVGA | 0.3580 | 0.5297 | 0.4496 |
| 2B61A | 0.3982 | 0.4969 | 0.3765 |
| 2DPMA | 0.3279 | 0.4715 | 0.3197 |
| 2PKEA | 0.8104 | 0.9855 | 0.7884 |

#### Position projection profile: anchor rank

For each protein, we compute dot(x_ln_j, d_resid_nobias) for all j and rank the anchor position.

| protein | anchor_pos | projection_rank | n_residues |
|---------|-----------|----------------|-----------|
| 1BRTA | 220 | 1 | 277 |
| 1PVGA | 101 | 1 | 418 |
| 2B61A | 315 | 1 | 377 |
| 2DPMA | 39 | 1 | 284 |
| 2PKEA | 131 | 1 | 251 |

### Step 3: Cross-protein anchor direction comparison

#### Key vectors (raw)

Anchor-anchor pairwise cosine: mean=0.6264, std=0.1085, n=10
Anchor-random control cosine: mean=0.2219, std=0.1083, n=20
Mann-Whitney U (anchor > control): U=200.0, p=6.005e-06

#### Key vectors (nobias)

Anchor-anchor pairwise cosine: mean=0.6053, std=0.1150, n=10
Anchor-random control cosine: mean=0.2255, std=0.1107, n=20
Mann-Whitney U (anchor > control): U=200.0, p=6.005e-06

Bias contamination check: raw mean cos - nobias mean cos = 0.0211
Bias contribution is small (delta <= 0.05).

#### Pairwise cosine similarity (nobias)

| protein_i | protein_j | cosine |
|-----------|-----------|--------|
| 1BRTA | 2B61A | 0.8307 |
| 1BRTA | 2PKEA | 0.7710 |
| 2B61A | 2PKEA | 0.6403 |
| 2B61A | 2DPMA | 0.6373 |
| 1PVGA | 2DPMA | 0.6134 |
| 1PVGA | 2B61A | 0.5564 |
| 2DPMA | 2PKEA | 0.5414 |
| 1BRTA | 2DPMA | 0.5269 |
| 1PVGA | 2PKEA | 0.4928 |
| 1BRTA | 1PVGA | 0.4427 |

---

## L14H9

### W_K singular value spectrum

Top-5 singular values: 5.87, 5.82, 5.61, 4.93, 4.80
Fraction of variance in top-1/3/5: 0.045 / 0.129 / 0.190

### Step 1: Key norm analysis

| protein | anchor_pos | aa | k_norm | rank | percentile | zscore | frac_top1 | frac_top3 | proj_top1_rank |
|---------|-----------|----|---------|----|-----------|--------|----------|----------|---------------|
| 1IN4A | 218 | A | 12.729 | 2 | 99.4 | 3.93 | 0.509 | 0.550 | 1 |
| 1IN4A | 55 | L | 11.214 | 9 | 97.3 | 2.83 | 0.389 | 0.480 | 6 |
| 1PVGA | 101 | V | 12.322 | 3 | 99.3 | 4.52 | 0.255 | 0.471 | 5 |
| 1PVGA | 198 | Y | 8.340 | 43 | 89.7 | 0.96 | 0.146 | 0.481 | 132 |
| 2B61A | 315 | T | 14.137 | 1 | 99.7 | 4.91 | 0.076 | 0.257 | 60 |
| 2PKEA | 183 | M | 14.133 | 1 | 99.6 | 5.55 | 0.017 | 0.184 | 163 |
| 2PKEA | 131 | L | 12.741 | 2 | 99.2 | 4.42 | 0.197 | 0.325 | 3 |

Mean anchor key norm Z-score: 3.87 (std 1.42)
Mean anchor percentile: 97.7%

### Step 2: Anchor direction correlations

#### AA embedding cosine similarity (top 5, averaged across proteins)

| AA | mean cos | std |
|----|----------|-----|
| Y | 0.0437 | 0.0157 |
| R | 0.0349 | 0.0096 |
| G | 0.0271 | 0.0078 |
| N | 0.0258 | 0.0130 |
| F | 0.0212 | 0.0077 |

#### SSE projection (mean dot product with anchor direction)

| protein | helix | strand | coil |
|---------|-------|--------|------|
| 1IN4A | 0.6922 | 0.6848 | 0.5583 |
| 1PVGA | 0.6079 | 0.7914 | 0.5988 |
| 2B61A | 0.3809 | 0.6360 | 0.3571 |
| 2PKEA | 0.2196 | 0.7944 | 0.3405 |

#### Position projection profile: anchor rank

For each protein, we compute dot(x_ln_j, d_resid_nobias) for all j and rank the anchor position.

| protein | anchor_pos | projection_rank | n_residues |
|---------|-----------|----------------|-----------|
| 1IN4A | 218 | 1 | 334 |
| 1IN4A | 55 | 7 | 334 |
| 1PVGA | 101 | 1 | 418 |
| 1PVGA | 198 | 21 | 418 |
| 2B61A | 315 | 1 | 377 |
| 2PKEA | 183 | 1 | 251 |
| 2PKEA | 131 | 3 | 251 |

### Step 3: Cross-protein anchor direction comparison

#### Key vectors (raw)

Anchor-anchor pairwise cosine: mean=0.5072, std=0.0799, n=6
Anchor-random control cosine: mean=0.3483, std=0.0708, n=12
Mann-Whitney U (anchor > control): U=66.0, p=0.001616

#### Key vectors (nobias)

Anchor-anchor pairwise cosine: mean=0.4391, std=0.0856, n=6
Anchor-random control cosine: mean=0.2008, std=0.0711, n=12
Mann-Whitney U (anchor > control): U=71.0, p=0.0001077

Bias contamination check: raw mean cos - nobias mean cos = 0.0681
Note: bias contributes meaningfully to cross-protein similarity (delta > 0.05).

#### Pairwise cosine similarity (nobias)

| protein_i | protein_j | cosine |
|-----------|-----------|--------|
| 1IN4A | 1PVGA | 0.5831 |
| 2B61A | 2PKEA | 0.4745 |
| 1PVGA | 2B61A | 0.4609 |
| 1PVGA | 2PKEA | 0.4451 |
| 1IN4A | 2B61A | 0.3387 |
| 1IN4A | 2PKEA | 0.3325 |

---
