# Anchor Head QK and OV Analysis

Anchor heads: L11H16, L10H9, L14H9
Interaction heads: L32H13
Proteins: 1BRTA, 1IN4A, 1PVGA, 1YKIA, 2B61A, 2DPMA, 2EK8A, 2FBQA, 2PKEA

## Question 1: Why does the anchor key win?

### Per-protein anchor key rankings

#### L11H16

Masked context = residuals from clean masked sequence (circuit context). Rank-among-unmasked = anchor rank relative to other real residues only.

| protein | anchor | region | masked rank/total | rank/unmasked | full-seq rank | q_mean_norm |
|---------|--------|--------|-------------------|---------------|---------------|-------------|
| 1PVGA | V102 | ss1 | 1/418 (100%) | 1/150 (99%) | 3/418 (99%) | 0.892 |
| 1YKIA | K130 | flkL | 1/217 (100%) | 1/95 (99%) | 171/217 (21%) | 0.794 |
| 2B61A | I158 | flkL | 1/377 (100%) | 1/110 (99%) | 3/377 (99%) | 0.911 |
| 2EK8A | G244 | flkR | 1/421 (100%) | 1/122 (99%) | 1/421 (100%) | 0.914 |
| 2FBQA | F48 | flkL | 1/235 (100%) | 1/111 (99%) | 1/235 (100%) | 0.881 |

#### L10H9

Masked context = residuals from clean masked sequence (circuit context). Rank-among-unmasked = anchor rank relative to other real residues only.

| protein | anchor | region | masked rank/total | rank/unmasked | full-seq rank | q_mean_norm |
|---------|--------|--------|-------------------|---------------|---------------|-------------|
| 1BRTA | L221 | ss2 | 1/277 (100%) | 1/86 (99%) | 1/277 (100%) | 0.920 |
| 1PVGA | V102 | ss1 | 1/418 (100%) | 1/150 (99%) | 1/418 (100%) | 0.933 |
| 2B61A | T316 | ss2 | 1/377 (100%) | 1/110 (99%) | 1/377 (100%) | 0.954 |
| 2DPMA | F40 | flkL | 1/284 (100%) | 1/82 (99%) | 2/284 (99%) | 0.928 |
| 2PKEA | L132 | ss2 | 1/251 (100%) | 1/90 (99%) | 3/251 (99%) | 0.898 |

#### L14H9

Masked context = residuals from clean masked sequence (circuit context). Rank-among-unmasked = anchor rank relative to other real residues only.

| protein | anchor | region | masked rank/total | rank/unmasked | full-seq rank | q_mean_norm |
|---------|--------|--------|-------------------|---------------|---------------|-------------|
| 1IN4A | A219 | flkR | 1/334 (100%) | 1/102 (99%) | 2/334 (99%) | 0.830 |
| 1PVGA | V102 | ss1 | 9/418 (98%) | 7/150 (95%) | 3/418 (99%) | 0.880 |
| 2B61A | T316 | ss2 | 31/377 (92%) | 14/110 (87%) | 55/377 (85%) | 0.897 |
| 2PKEA | M184 | flkR | 9/251 (96%) | 3/90 (97%) | 5/251 (98%) | 0.774 |

### Cross-protein search direction alignment

q_mean is the average unit query direction. W_Q^T @ q_mean is the corresponding direction in residual stream space.
High cosine similarity across proteins = fixed search direction (property of W_Q); low = context-dependent.

| head | q_mean cosine (head space) | search dir cosine (resid space) | mean q_mean_norm |
|------|---------------------------|--------------------------------|------------------|
| L11H16 | 0.8439 | 0.7922 | 0.8785 |
| L10H9 | 0.9391 | 0.9269 | 0.9266 |
| L14H9 | 0.9288 | 0.9265 | 0.8455 |

## Question 2: What does the anchor head write?

### Attention distribution to anchor (where OV output goes)

Values are fraction of total attention in the column pointing to the anchor.

#### L11H16

| protein | anchor | ss1 | ss2 | flkL | flkR | other |
|---------|--------|-----|-----|------|------|-------|
| 1PVGA | V102 | 4.2% | 0.7% | 58.8% | 9.1% | 27.2% |
| 1YKIA | K130 | 3.0% | 4.9% | 36.9% | 32.8% | 22.4% |
| 2B61A | I158 | 2.4% | 2.6% | 23.8% | 24.8% | 46.3% |
| 2EK8A | G244 | 2.1% | 5.0% | 16.7% | 29.9% | 46.3% |
| 2FBQA | F48 | 6.5% | 6.6% | 58.4% | 28.1% | 0.4% |

#### L10H9

| protein | anchor | ss1 | ss2 | flkL | flkR | other |
|---------|--------|-----|-----|------|------|-------|
| 1BRTA | L221 | 6.6% | 3.9% | 24.3% | 17.4% | 47.8% |
| 1PVGA | V102 | 2.7% | 3.2% | 33.7% | 25.0% | 35.4% |
| 2B61A | T316 | 2.9% | 3.1% | 30.0% | 28.5% | 35.4% |
| 2DPMA | F40 | 5.0% | 4.1% | 24.8% | 22.0% | 44.0% |
| 2PKEA | L132 | 3.1% | 2.6% | 23.9% | 42.5% | 28.0% |

#### L14H9

| protein | anchor | ss1 | ss2 | flkL | flkR | other |
|---------|--------|-----|-----|------|------|-------|
| 1IN4A | A219 | 0.2% | 0.8% | 1.6% | 45.0% | 52.5% |
| 1PVGA | V102 | 5.8% | 5.0% | 36.2% | 15.9% | 37.1% |
| 2B61A | T316 | 5.5% | 3.5% | 63.5% | 20.1% | 7.4% |
| 2PKEA | M184 | 23.5% | 26.1% | 15.6% | 9.2% | 25.6% |

### OV output -> interaction head projections

k_delta_norm = ||W_K_interaction @ ov_output|| (anchor head changes destination as a key).
q_delta_norm = ||W_Q_interaction @ ov_output|| (anchor head changes what destination queries for).

#### L11H16

##### L11H16 -> L32H13

| protein | anchor | k_delta_norm | q_delta_norm |
|---------|--------|--------------|---------------|
| 1PVGA | V102 | 15.3913 | 15.7606 |
| 1YKIA | K130 | 8.2461 | 8.3153 |
| 2B61A | I158 | 18.2112 | 16.2058 |
| 2EK8A | G244 | 16.3960 | 16.3019 |
| 2FBQA | F48 | 23.7010 | 22.1077 |

#### L10H9

##### L10H9 -> L32H13

| protein | anchor | k_delta_norm | q_delta_norm |
|---------|--------|--------------|---------------|
| 1BRTA | L221 | 16.6777 | 14.8087 |
| 1PVGA | V102 | 24.5072 | 24.0952 |
| 2B61A | T316 | 21.9632 | 19.4069 |
| 2DPMA | F40 | 21.3673 | 23.1615 |
| 2PKEA | L132 | 13.7477 | 13.8051 |

#### L14H9

##### L14H9 -> L32H13

| protein | anchor | k_delta_norm | q_delta_norm |
|---------|--------|--------------|---------------|
| 1IN4A | A219 | 17.1698 | 16.3403 |
| 1PVGA | V102 | 19.0095 | 18.3119 |
| 2B61A | T316 | 24.8809 | 22.7505 |
| 2PKEA | M184 | 20.1285 | 19.6146 |

### Cross-protein OV output similarity

| head | mean pairwise cos | std | ov_norm mean |
|------|-------------------|-----|-------------|
| L11H16 | -0.0453 | 0.3034 | 22.6821 |
| L10H9 | 0.2315 | 0.1955 | 28.2120 |
| L14H9 | 0.1236 | 0.1888 | 28.9460 |
