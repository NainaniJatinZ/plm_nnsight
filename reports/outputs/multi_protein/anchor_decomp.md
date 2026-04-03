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
| 2YHWA | 165 | G | 12.324 | 1 | 99.7 | 3.89 | 0.028 | 0.090 | 332 |
| 3CSSA | 158 | V | 11.148 | 6 | 97.8 | 1.75 | 0.000 | 0.098 | 266 |
| 3CSSA | 40 | L | 11.238 | 2 | 99.3 | 1.94 | 0.000 | 0.044 | 267 |
| 3HO7A | 32 | W | 13.923 | 1 | 99.6 | 5.70 | 0.002 | 0.007 | 230 |
| 3LEWA | 353 | A | 14.400 | 1 | 99.8 | 9.46 | 0.012 | 0.125 | 492 |
| 3OKPA | 200 | I | 11.381 | 2 | 99.5 | 2.73 | 0.026 | 0.112 | 383 |
| 3WJPA | 276 | M | 12.258 | 1 | 99.7 | 3.81 | 0.022 | 0.146 | 334 |
| 4EHUA | 100 | G | 12.522 | 1 | 99.6 | 5.64 | 0.024 | 0.077 | 271 |

Mean anchor key norm Z-score: 3.95 (std 2.43)
Mean anchor percentile: 95.8%

### Step 2: Anchor direction correlations

#### AA embedding cosine similarity (top 5, averaged across proteins)

| AA | mean cos | std |
|----|----------|-----|
| T | 0.0542 | 0.0139 |
| E | 0.0202 | 0.0149 |
| A | 0.0185 | 0.0178 |
| Y | 0.0089 | 0.0232 |
| N | 0.0085 | 0.0140 |

#### SSE projection (mean dot product with anchor direction)

| protein | helix | strand | coil |
|---------|-------|--------|------|
| 1PVGA | 0.7644 | 0.8478 | 0.8129 |
| 1YKIA | 1.8401 | 1.7715 | 1.8680 |
| 2B61A | 1.0829 | 1.0595 | 0.9493 |
| 2EK8A | 0.8006 | 0.5750 | 0.6020 |
| 2FBQA | 0.7492 | 0.0000 | 0.7773 |
| 2YHWA | 1.3342 | 1.2205 | 1.2002 |
| 3CSSA | 1.2449 | 1.2792 | 1.2492 |
| 3HO7A | 1.2413 | 0.9482 | 1.0086 |
| 3LEWA | 0.5391 | 0.4099 | 0.4410 |
| 3OKPA | 1.3079 | 1.3643 | 1.2951 |
| 3WJPA | 0.8753 | 0.8559 | 0.7596 |
| 4EHUA | 1.0253 | 0.9390 | 0.9539 |

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
| 2YHWA | 165 | 1 | 343 |
| 3CSSA | 158 | 1 | 267 |
| 3CSSA | 40 | 2 | 267 |
| 3HO7A | 32 | 1 | 232 |
| 3LEWA | 353 | 1 | 495 |
| 3OKPA | 200 | 1 | 394 |
| 3WJPA | 276 | 1 | 338 |
| 4EHUA | 100 | 1 | 276 |

### Step 3: Cross-protein anchor direction comparison

#### Key vectors (raw)

Anchor-anchor pairwise cosine: mean=0.5733, std=0.1306, n=66
Anchor-random control cosine: mean=0.4619, std=0.1768, n=132
Mann-Whitney U (anchor > control): U=6411.0, p=3.237e-08

#### Key vectors (nobias)

Anchor-anchor pairwise cosine: mean=0.5355, std=0.1275, n=66
Anchor-random control cosine: mean=0.4358, std=0.1859, n=132
Mann-Whitney U (anchor > control): U=6318.0, p=1.231e-07

Bias contamination check: raw mean cos - nobias mean cos = 0.0378
Bias contribution is small (delta <= 0.05).

#### Pairwise cosine similarity (nobias)

| protein_i | protein_j | cosine |
|-----------|-----------|--------|
| 2YHWA | 4EHUA | 0.7856 |
| 2FBQA | 3HO7A | 0.7421 |
| 2EK8A | 3HO7A | 0.7329 |
| 2B61A | 2EK8A | 0.7152 |
| 2B61A | 3OKPA | 0.7041 |
| 2B61A | 2YHWA | 0.6985 |
| 2B61A | 3CSSA | 0.6927 |
| 2YHWA | 3CSSA | 0.6868 |
| 2YHWA | 3WJPA | 0.6780 |
| 2B61A | 4EHUA | 0.6778 |
| 2EK8A | 2YHWA | 0.6588 |
| 2B61A | 3HO7A | 0.6295 |
| 3HO7A | 3LEWA | 0.6290 |
| 3CSSA | 4EHUA | 0.6266 |
| 1PVGA | 3HO7A | 0.6207 |
| 2EK8A | 3LEWA | 0.6196 |
| 2B61A | 3LEWA | 0.6178 |
| 2B61A | 3WJPA | 0.6119 |
| 2YHWA | 3OKPA | 0.6072 |
| 3OKPA | 3WJPA | 0.6058 |
| 2EK8A | 3WJPA | 0.6039 |
| 1PVGA | 2EK8A | 0.6008 |
| 3HO7A | 3OKPA | 0.5958 |
| 3WJPA | 4EHUA | 0.5957 |
| 3LEWA | 3WJPA | 0.5847 |
| 3OKPA | 4EHUA | 0.5832 |
| 2YHWA | 3HO7A | 0.5794 |
| 1PVGA | 3OKPA | 0.5781 |
| 1PVGA | 2B61A | 0.5767 |
| 3CSSA | 3OKPA | 0.5748 |
| 1PVGA | 3LEWA | 0.5731 |
| 2EK8A | 4EHUA | 0.5719 |
| 3LEWA | 3OKPA | 0.5683 |
| 2YHWA | 3LEWA | 0.5670 |
| 1PVGA | 2FBQA | 0.5610 |
| 3LEWA | 4EHUA | 0.5504 |
| 1PVGA | 3WJPA | 0.5435 |
| 1PVGA | 2YHWA | 0.5431 |
| 3CSSA | 3HO7A | 0.5266 |
| 2FBQA | 3LEWA | 0.5222 |
| 2EK8A | 3OKPA | 0.5098 |
| 2B61A | 2FBQA | 0.5078 |
| 2EK8A | 2FBQA | 0.4985 |
| 3HO7A | 3WJPA | 0.4973 |
| 1YKIA | 3OKPA | 0.4968 |
| 3CSSA | 3WJPA | 0.4953 |
| 2FBQA | 3OKPA | 0.4843 |
| 3HO7A | 4EHUA | 0.4793 |
| 1PVGA | 3CSSA | 0.4788 |
| 2EK8A | 3CSSA | 0.4733 |
| 1YKIA | 3CSSA | 0.4673 |
| 3CSSA | 3LEWA | 0.4639 |
| 2FBQA | 2YHWA | 0.4229 |
| 1YKIA | 3HO7A | 0.4089 |
| 2FBQA | 3WJPA | 0.4012 |
| 1PVGA | 4EHUA | 0.3960 |
| 2FBQA | 3CSSA | 0.3946 |
| 1YKIA | 2FBQA | 0.3841 |
| 2FBQA | 4EHUA | 0.3808 |
| 1YKIA | 2YHWA | 0.3679 |
| 1PVGA | 1YKIA | 0.3218 |
| 1YKIA | 2B61A | 0.3055 |
| 1YKIA | 4EHUA | 0.2916 |
| 1YKIA | 2EK8A | 0.2621 |
| 1YKIA | 3WJPA | 0.2161 |
| 1YKIA | 3LEWA | 0.1951 |

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
| 2QY6A | 64 | A | 13.205 | 1 | 99.6 | 5.68 | 0.041 | 0.070 | 244 |
| 2YHWA | 92 | V | 14.801 | 2 | 99.4 | 8.07 | 0.079 | 0.081 | 277 |
| 2YHWA | 287 | V | 15.107 | 1 | 99.7 | 8.51 | 0.017 | 0.246 | 335 |
| 3CSSA | 40 | L | 10.437 | 3 | 98.9 | 2.07 | 0.033 | 0.033 | 262 |
| 3HO7A | 63 | A | 9.480 | 50 | 78.4 | 0.71 | 0.027 | 0.054 | 227 |
| 3HO7A | 17 | L | 8.399 | 217 | 6.5 | -1.27 | 0.202 | 0.364 | 208 |
| 3OKPA | 200 | I | 12.870 | 2 | 99.5 | 4.97 | 0.008 | 0.103 | 386 |
| 3QDLA | 114 | P | 8.670 | 121 | 42.4 | -0.26 | 0.356 | 0.504 | 40 |
| 3QDLA | 115 | S | 8.497 | 148 | 29.5 | -0.57 | 0.323 | 0.527 | 71 |
| 3WJPA | 94 | L | 12.852 | 1 | 99.7 | 7.58 | 0.050 | 0.072 | 328 |
| 4EHUA | 100 | G | 12.390 | 2 | 99.3 | 6.59 | 0.007 | 0.055 | 273 |
| 4EX6A | 124 | M | 14.039 | 1 | 99.6 | 6.90 | 0.000 | 0.027 | 236 |
| 4EX6A | 180 | V | 8.499 | 211 | 11.0 | -1.06 | 0.184 | 0.295 | 210 |
| 4EZIA | 310 | L | 12.217 | 2 | 99.5 | 5.51 | 0.066 | 0.181 | 351 |
| 4ME3A | 75 | G | 7.981 | 201 | 25.0 | -0.73 | 0.260 | 0.391 | 116 |
| 4N9WA | 147 | R | 11.342 | 5 | 98.7 | 2.65 | 0.008 | 0.038 | 387 |
| 4N9WA | 194 | V | 12.445 | 2 | 99.5 | 4.22 | 0.008 | 0.068 | 386 |
| 4OY3A | 193 | L | 11.352 | 2 | 99.1 | 4.04 | 0.024 | 0.332 | 229 |

Mean anchor key norm Z-score: 3.96 (std 3.09)
Mean anchor percentile: 81.8%

### Step 2: Anchor direction correlations

#### AA embedding cosine similarity (top 5, averaged across proteins)

| AA | mean cos | std |
|----|----------|-----|
| L | 0.0449 | 0.0185 |
| T | 0.0403 | 0.0128 |
| K | 0.0216 | 0.0209 |
| R | 0.0153 | 0.0156 |
| A | 0.0119 | 0.0143 |

#### SSE projection (mean dot product with anchor direction)

| protein | helix | strand | coil |
|---------|-------|--------|------|
| 1BRTA | 0.7165 | 0.8668 | 0.7102 |
| 1PVGA | 0.3580 | 0.5297 | 0.4496 |
| 2B61A | 0.3982 | 0.4969 | 0.3765 |
| 2DPMA | 0.3279 | 0.4715 | 0.3197 |
| 2PKEA | 0.8104 | 0.9855 | 0.7884 |
| 2QY6A | 0.1872 | 0.3095 | 0.2041 |
| 2YHWA | 0.4047 | 0.4971 | 0.4410 |
| 3CSSA | 0.6167 | 0.7233 | 0.6039 |
| 3HO7A | 0.7471 | 0.8460 | 0.7368 |
| 3OKPA | 0.7413 | 0.9369 | 0.7002 |
| 3QDLA | 1.5686 | 1.4640 | 1.5619 |
| 3WJPA | 0.3499 | 0.4662 | 0.3821 |
| 4EHUA | 0.5420 | 0.6313 | 0.5944 |
| 4EX6A | 0.6873 | 0.9863 | 0.6773 |
| 4EZIA | 0.3111 | 0.4173 | 0.2660 |
| 4ME3A | 0.7767 | 0.6973 | 0.6875 |
| 4N9WA | 0.9110 | 1.0934 | 0.8808 |
| 4OY3A | 0.0254 | 0.1399 | 0.0073 |

#### Position projection profile: anchor rank

For each protein, we compute dot(x_ln_j, d_resid_nobias) for all j and rank the anchor position.

| protein | anchor_pos | projection_rank | n_residues |
|---------|-----------|----------------|-----------|
| 1BRTA | 220 | 1 | 277 |
| 1PVGA | 101 | 1 | 418 |
| 2B61A | 315 | 1 | 377 |
| 2DPMA | 39 | 1 | 284 |
| 2PKEA | 131 | 1 | 251 |
| 2QY6A | 64 | 1 | 257 |
| 2YHWA | 92 | 1 | 343 |
| 2YHWA | 287 | 3 | 343 |
| 3CSSA | 40 | 1 | 267 |
| 3HO7A | 63 | 1 | 232 |
| 3HO7A | 17 | 8 | 232 |
| 3OKPA | 200 | 1 | 394 |
| 3QDLA | 114 | 57 | 210 |
| 3QDLA | 115 | 108 | 210 |
| 3WJPA | 94 | 1 | 338 |
| 4EHUA | 100 | 1 | 276 |
| 4EX6A | 124 | 1 | 237 |
| 4EX6A | 180 | 22 | 237 |
| 4EZIA | 310 | 1 | 377 |
| 4ME3A | 75 | 1 | 268 |
| 4N9WA | 147 | 1 | 390 |
| 4N9WA | 194 | 2 | 390 |
| 4OY3A | 193 | 1 | 231 |

### Step 3: Cross-protein anchor direction comparison

#### Key vectors (raw)

Anchor-anchor pairwise cosine: mean=0.5588, std=0.1620, n=153
Anchor-random control cosine: mean=0.2875, std=0.1909, n=306
Mann-Whitney U (anchor > control): U=40963.0, p=1.584e-39

#### Key vectors (nobias)

Anchor-anchor pairwise cosine: mean=0.5353, std=0.1653, n=153
Anchor-random control cosine: mean=0.2922, std=0.1935, n=306
Mann-Whitney U (anchor > control): U=40096.0, p=6.505e-36

Bias contamination check: raw mean cos - nobias mean cos = 0.0235
Bias contribution is small (delta <= 0.05).

#### Pairwise cosine similarity (nobias)

| protein_i | protein_j | cosine |
|-----------|-----------|--------|
| 2PKEA | 4EX6A | 0.9399 |
| 2B61A | 4EZIA | 0.8742 |
| 1BRTA | 2B61A | 0.8307 |
| 2DPMA | 2QY6A | 0.8219 |
| 1BRTA | 4EZIA | 0.8013 |
| 1BRTA | 4EX6A | 0.7873 |
| 1BRTA | 2PKEA | 0.7710 |
| 2YHWA | 4EHUA | 0.7707 |
| 1BRTA | 3OKPA | 0.7695 |
| 2YHWA | 3CSSA | 0.7586 |
| 3CSSA | 4EX6A | 0.7586 |
| 2B61A | 3OKPA | 0.7506 |
| 2PKEA | 3CSSA | 0.7490 |
| 3OKPA | 4N9WA | 0.7403 |
| 3CSSA | 4EHUA | 0.7343 |
| 2PKEA | 4N9WA | 0.7340 |
| 1PVGA | 2QY6A | 0.7302 |
| 4EX6A | 4N9WA | 0.7279 |
| 2PKEA | 3OKPA | 0.7268 |
| 3CSSA | 3OKPA | 0.7226 |
| 2YHWA | 3WJPA | 0.7216 |
| 2YHWA | 4EX6A | 0.7160 |
| 3CSSA | 3HO7A | 0.7092 |
| 1PVGA | 3WJPA | 0.6929 |
| 4EHUA | 4EX6A | 0.6921 |
| 3OKPA | 4EX6A | 0.6915 |
| 3OKPA | 4EZIA | 0.6775 |
| 3CSSA | 4N9WA | 0.6740 |
| 3HO7A | 4N9WA | 0.6739 |
| 3HO7A | 3OKPA | 0.6705 |
| 1PVGA | 2YHWA | 0.6694 |
| 1BRTA | 4EHUA | 0.6607 |
| 3HO7A | 4EX6A | 0.6509 |
| 1BRTA | 3CSSA | 0.6453 |
| 2PKEA | 2QY6A | 0.6422 |
| 3HO7A | 4EHUA | 0.6409 |
| 2B61A | 2QY6A | 0.6408 |
| 2B61A | 2PKEA | 0.6403 |
| 2PKEA | 2YHWA | 0.6387 |
| 2B61A | 2DPMA | 0.6373 |
| 1BRTA | 4N9WA | 0.6359 |
| 3WJPA | 4EX6A | 0.6357 |
| 2B61A | 4EX6A | 0.6339 |
| 2B61A | 4N9WA | 0.6336 |
| 2QY6A | 4N9WA | 0.6218 |
| 2QY6A | 3WJPA | 0.6205 |
| 1PVGA | 3CSSA | 0.6189 |
| 2PKEA | 3HO7A | 0.6149 |
| 1PVGA | 2DPMA | 0.6134 |
| 2QY6A | 3OKPA | 0.6076 |
| 2PKEA | 4EHUA | 0.6064 |
| 1BRTA | 4OY3A | 0.6028 |
| 2YHWA | 3HO7A | 0.6028 |
| 2PKEA | 4EZIA | 0.6016 |
| 2QY6A | 3CSSA | 0.6005 |
| 2DPMA | 3CSSA | 0.6001 |
| 3CSSA | 3WJPA | 0.5996 |
| 4EX6A | 4EZIA | 0.5921 |
| 2DPMA | 4N9WA | 0.5916 |
| 3WJPA | 4EHUA | 0.5855 |
| 2QY6A | 4EX6A | 0.5848 |
| 3WJPA | 4EZIA | 0.5821 |
| 2B61A | 3CSSA | 0.5818 |
| 2B61A | 3HO7A | 0.5812 |
| 4EHUA | 4OY3A | 0.5807 |
| 4EZIA | 4N9WA | 0.5792 |
| 2QY6A | 4EZIA | 0.5785 |
| 3OKPA | 4EHUA | 0.5779 |
| 2DPMA | 3OKPA | 0.5751 |
| 4EHUA | 4EZIA | 0.5745 |
| 4EX6A | 4OY3A | 0.5709 |
| 1BRTA | 3HO7A | 0.5678 |
| 3HO7A | 4EZIA | 0.5675 |
| 3CSSA | 4EZIA | 0.5638 |
| 2YHWA | 4EZIA | 0.5619 |
| 2DPMA | 2YHWA | 0.5604 |
| 1PVGA | 2B61A | 0.5564 |
| 2DPMA | 4EZIA | 0.5563 |
| 2QY6A | 2YHWA | 0.5557 |
| 2B61A | 4EHUA | 0.5523 |
| 1BRTA | 2YHWA | 0.5512 |
| 1PVGA | 4EZIA | 0.5466 |
| 2DPMA | 3HO7A | 0.5450 |
| 3HO7A | 3WJPA | 0.5445 |
| 2YHWA | 4N9WA | 0.5417 |
| 2DPMA | 2PKEA | 0.5414 |
| 2B61A | 2YHWA | 0.5395 |
| 2PKEA | 3WJPA | 0.5382 |
| 2DPMA | 3WJPA | 0.5363 |
| 2B61A | 3WJPA | 0.5351 |
| 1BRTA | 2QY6A | 0.5312 |
| 1BRTA | 3WJPA | 0.5308 |
| 4EHUA | 4N9WA | 0.5306 |
| 2B61A | 4OY3A | 0.5282 |
| 3WJPA | 4N9WA | 0.5280 |
| 1BRTA | 2DPMA | 0.5269 |
| 2DPMA | 4EX6A | 0.5135 |
| 4EZIA | 4ME3A | 0.5122 |
| 2PKEA | 4OY3A | 0.5088 |
| 1PVGA | 4N9WA | 0.5029 |
| 1PVGA | 4ME3A | 0.5015 |
| 2QY6A | 3HO7A | 0.5008 |
| 1PVGA | 3OKPA | 0.4997 |
| 1PVGA | 2PKEA | 0.4928 |
| 4EZIA | 4OY3A | 0.4906 |
| 3HO7A | 4ME3A | 0.4862 |
| 3CSSA | 4ME3A | 0.4851 |
| 2DPMA | 4EHUA | 0.4812 |
| 1PVGA | 4EHUA | 0.4786 |
| 3CSSA | 4OY3A | 0.4720 |
| 2YHWA | 3OKPA | 0.4712 |
| 1PVGA | 3HO7A | 0.4621 |
| 1PVGA | 4EX6A | 0.4606 |
| 1BRTA | 1PVGA | 0.4427 |
| 2QY6A | 4EHUA | 0.4418 |
| 2YHWA | 4ME3A | 0.4405 |
| 2PKEA | 3QDLA | 0.4334 |
| 4ME3A | 4N9WA | 0.4319 |
| 3OKPA | 3WJPA | 0.4192 |
| 3OKPA | 4OY3A | 0.4172 |
| 2YHWA | 4OY3A | 0.4169 |
| 1BRTA | 3QDLA | 0.4162 |
| 3QDLA | 4N9WA | 0.4156 |
| 2B61A | 4ME3A | 0.4081 |
| 3OKPA | 4ME3A | 0.3984 |
| 2PKEA | 4ME3A | 0.3788 |
| 3QDLA | 4EX6A | 0.3752 |
| 4N9WA | 4OY3A | 0.3492 |
| 4EX6A | 4ME3A | 0.3445 |
| 3WJPA | 4OY3A | 0.3390 |
| 1BRTA | 4ME3A | 0.3378 |
| 3OKPA | 3QDLA | 0.3314 |
| 3HO7A | 3QDLA | 0.3299 |
| 3WJPA | 4ME3A | 0.3270 |
| 1PVGA | 4OY3A | 0.3244 |
| 3CSSA | 3QDLA | 0.3234 |
| 4EHUA | 4ME3A | 0.3093 |
| 3HO7A | 4OY3A | 0.3075 |
| 2QY6A | 4ME3A | 0.2986 |
| 3QDLA | 4EHUA | 0.2549 |
| 4ME3A | 4OY3A | 0.2399 |
| 2QY6A | 4OY3A | 0.2378 |
| 3QDLA | 4ME3A | 0.2343 |
| 2DPMA | 4ME3A | 0.2337 |
| 2DPMA | 3QDLA | 0.2131 |
| 2B61A | 3QDLA | 0.2120 |
| 3QDLA | 3WJPA | 0.2118 |
| 2YHWA | 3QDLA | 0.2084 |
| 2QY6A | 3QDLA | 0.1803 |
| 3QDLA | 4EZIA | 0.1752 |
| 2DPMA | 4OY3A | 0.1604 |
| 1PVGA | 3QDLA | 0.1312 |
| 3QDLA | 4OY3A | 0.0165 |

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
| 2QY6A | 176 | W | 12.678 | 2 | 99.2 | 3.87 | 0.080 | 0.234 | 39 |
| 3CSSA | 44 | G | 12.142 | 2 | 99.3 | 4.78 | 0.242 | 0.478 | 1 |
| 3CSSA | 158 | V | 15.015 | 1 | 99.6 | 7.34 | 0.020 | 0.242 | 125 |
| 3WJPA | 94 | L | 13.600 | 2 | 99.4 | 6.95 | 0.068 | 0.256 | 72 |
| 3WJPA | 276 | M | 14.420 | 1 | 99.7 | 7.79 | 0.119 | 0.320 | 6 |
| 4EZIA | 310 | L | 12.718 | 1 | 99.7 | 4.56 | 0.130 | 0.362 | 22 |
| 4N9WA | 194 | V | 12.960 | 2 | 99.5 | 4.10 | 0.180 | 0.238 | 8 |
| 4OY3A | 193 | L | 13.699 | 1 | 99.6 | 6.61 | 0.121 | 0.551 | 3 |
| 4OY3A | 74 | L | 8.621 | 11 | 95.2 | 1.96 | 0.110 | 0.199 | 62 |

Mean anchor key norm Z-score: 4.69 (std 1.82)
Mean anchor percentile: 98.5%

### Step 2: Anchor direction correlations

#### AA embedding cosine similarity (top 5, averaged across proteins)

| AA | mean cos | std |
|----|----------|-----|
| Y | 0.0452 | 0.0144 |
| R | 0.0344 | 0.0106 |
| N | 0.0253 | 0.0111 |
| G | 0.0225 | 0.0114 |
| F | 0.0159 | 0.0097 |

#### SSE projection (mean dot product with anchor direction)

| protein | helix | strand | coil |
|---------|-------|--------|------|
| 1IN4A | 0.6922 | 0.6848 | 0.5583 |
| 1PVGA | 0.6079 | 0.7914 | 0.5988 |
| 2B61A | 0.3809 | 0.6360 | 0.3571 |
| 2PKEA | 0.2196 | 0.7944 | 0.3405 |
| 2QY6A | 0.2292 | 0.4863 | 0.2431 |
| 3CSSA | 0.4202 | 0.4495 | 0.3015 |
| 3WJPA | 0.4727 | 0.8194 | 0.5656 |
| 4EZIA | 0.5165 | 0.7435 | 0.5323 |
| 4N9WA | 0.5921 | 1.1006 | 0.5966 |
| 4OY3A | 0.4180 | 0.5761 | 0.3912 |

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
| 2QY6A | 176 | 1 | 257 |
| 3CSSA | 44 | 1 | 267 |
| 3CSSA | 158 | 37 | 267 |
| 3WJPA | 94 | 1 | 338 |
| 3WJPA | 276 | 2 | 338 |
| 4EZIA | 310 | 1 | 377 |
| 4N9WA | 194 | 1 | 390 |
| 4OY3A | 193 | 1 | 231 |
| 4OY3A | 74 | 15 | 231 |

### Step 3: Cross-protein anchor direction comparison

#### Key vectors (raw)

Anchor-anchor pairwise cosine: mean=0.5462, std=0.1327, n=45
Anchor-random control cosine: mean=0.4053, std=0.1194, n=90
Mann-Whitney U (anchor > control): U=3196.0, p=2.335e-08

#### Key vectors (nobias)

Anchor-anchor pairwise cosine: mean=0.4819, std=0.1482, n=45
Anchor-random control cosine: mean=0.2717, std=0.1370, n=90
Mann-Whitney U (anchor > control): U=3442.0, p=1.9e-11

Bias contamination check: raw mean cos - nobias mean cos = 0.0643
Note: bias contributes meaningfully to cross-protein similarity (delta > 0.05).

#### Pairwise cosine similarity (nobias)

| protein_i | protein_j | cosine |
|-----------|-----------|--------|
| 2B61A | 4EZIA | 0.9180 |
| 2QY6A | 4EZIA | 0.6728 |
| 4EZIA | 4OY3A | 0.6546 |
| 4EZIA | 4N9WA | 0.6452 |
| 1IN4A | 4N9WA | 0.6213 |
| 3WJPA | 4OY3A | 0.6184 |
| 1PVGA | 4OY3A | 0.6150 |
| 2B61A | 2QY6A | 0.6130 |
| 3WJPA | 4EZIA | 0.6013 |
| 2B61A | 4N9WA | 0.5984 |
| 3WJPA | 4N9WA | 0.5966 |
| 1PVGA | 3WJPA | 0.5906 |
| 1IN4A | 1PVGA | 0.5831 |
| 2B61A | 4OY3A | 0.5797 |
| 1PVGA | 4EZIA | 0.5611 |
| 2QY6A | 4OY3A | 0.5520 |
| 1PVGA | 4N9WA | 0.5445 |
| 2QY6A | 3WJPA | 0.5415 |
| 2PKEA | 4N9WA | 0.5394 |
| 2B61A | 3WJPA | 0.5286 |
| 1IN4A | 3CSSA | 0.5203 |
| 2PKEA | 4OY3A | 0.4913 |
| 2PKEA | 4EZIA | 0.4893 |
| 1PVGA | 2QY6A | 0.4882 |
| 2B61A | 2PKEA | 0.4745 |
| 2PKEA | 3WJPA | 0.4707 |
| 1PVGA | 2B61A | 0.4609 |
| 1PVGA | 2PKEA | 0.4451 |
| 1IN4A | 4EZIA | 0.4411 |
| 3CSSA | 4N9WA | 0.4380 |
| 1IN4A | 3WJPA | 0.4203 |
| 1PVGA | 3CSSA | 0.4100 |
| 1IN4A | 4OY3A | 0.4080 |
| 2QY6A | 4N9WA | 0.4000 |
| 2PKEA | 3CSSA | 0.3861 |
| 2PKEA | 2QY6A | 0.3799 |
| 1IN4A | 2QY6A | 0.3529 |
| 4N9WA | 4OY3A | 0.3423 |
| 1IN4A | 2B61A | 0.3387 |
| 1IN4A | 2PKEA | 0.3325 |
| 3CSSA | 3WJPA | 0.3196 |
| 2B61A | 3CSSA | 0.2073 |
| 3CSSA | 4EZIA | 0.2058 |
| 3CSSA | 4OY3A | 0.1737 |
| 2QY6A | 3CSSA | 0.1129 |

---
