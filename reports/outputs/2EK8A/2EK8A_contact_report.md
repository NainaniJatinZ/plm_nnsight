# Contact Pattern Analysis: 2EK8A

Generated: 2026-03-03 05:27:43   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2EK8A |
| Contact pair | (59, 203) |
| ss1 | [54, 65) |
| ss2 | [198, 209) |
| Clean flank | 50 |
| Corrupt flank | 49 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.6519 |
| Corrupt metric | 0.0235 |
| Gap | 0.6284 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 71.23% |
| positive IE | 60 | 70.37% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L7 | H9 | +0.6210 |
| 2 | L32 | H13 | +0.5346 |
| 3 | L29 | H18 | +0.3419 |
| 4 | L32 | H18 | +0.3007 |
| 5 | L22 | H17 | +0.2319 |
| 6 | L27 | H15 | +0.2097 |
| 7 | L11 | H16 | +0.1888 |
| 8 | L10 | H9 | +0.1826 |
| 9 | L12 | H15 | +0.1793 |
| 10 | L26 | H11 | +0.1262 |
| 11 | L8 | H12 | +0.1108 |
| 12 | L8 | H15 | +0.0944 |
| 13 | L14 | H12 | +0.0888 |
| 14 | L22 | H15 | +0.0839 |
| 15 | L21 | H6 | +0.0823 |
| 16 | L11 | H14 | +0.0817 |
| 17 | L16 | H5 | +0.0808 |
| 18 | L17 | H8 | +0.0800 |
| 19 | L21 | H10 | +0.0788 |
| 20 | L14 | H0 | +0.0718 |
| 21 | L10 | H6 | +0.0717 |
| 22 | L31 | H17 | +0.0699 |
| 23 | L6 | H16 | +0.0694 |
| 24 | L5 | H13 | +0.0681 |
| 25 | L0 | H1 | +0.0672 |
| 26 | L13 | H3 | +0.0670 |
| 27 | L20 | H5 | +0.0638 |
| 28 | L10 | H12 | +0.0588 |
| 29 | L13 | H13 | +0.0540 |
| 30 | L16 | H13 | +0.0532 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | 0.08% |
| 3 | 0.10% |
| 4 | 0.11% |
| 5 | 0.11% |
| 6 | 0.09% |
| 7 | 0.05% |
| 8 | 0.13% |
| 9 | 0.59% |
| 10 | 0.59% |
| 20 | 5.32% |
| 80 | 105.57% |
| 450 | 161.11% |

## Cell Attribution Analysis

Total cells: 9,967,361

- Positive: 5,202,152
- Negative: 4,761,835

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000037 | 996,737 |
| 95th | +0.00000120 | 498,369 |
| 99th | +0.00001096 | 99,675 |
| 99.5th | +0.00002473 | 49,838 |
| 99.9th | +0.00012898 | 9,968 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H9 | 267 | other | 224 | flkR | +0.281797 | 0.141153 |
| L7 | H9 | 265 | other | 224 | flkR | +0.148257 | 0.179403 |
| L14 | H12 | 207 | ss2 | 224 | flkR | +0.132527 | 0.511699 |
| L7 | H9 | 266 | other | 224 | flkR | +0.107113 | 0.160059 |
| L21 | H10 | 243 | flkR | 243 | flkR | +0.087281 | 0.794412 |
| L12 | H15 | 243 | flkR | 267 | other | +0.084726 | 0.328729 |
| L10 | H12 | 243 | flkR | 224 | flkR | +0.081987 | 0.250806 |
| L7 | H9 | 269 | other | 224 | flkR | +0.073674 | 0.200176 |
| L11 | H14 | 243 | flkR | 224 | flkR | +0.069909 | 0.220156 |
| L26 | H11 | 202 | ss2 | 207 | ss2 | +0.069093 | 0.690441 |
| L14 | H0 | 207 | ss2 | 227 | flkR | +0.066125 | 0.324656 |
| L29 | H18 | 203 | ss2 | 58 | ss1 | +0.064947 | 0.636206 |
| L21 | H6 | 199 | ss2 | 207 | ss2 | +0.061011 | 0.655187 |
| L22 | H17 | 200 | ss2 | 243 | flkR | +0.059566 | 0.771944 |
| L6 | H3 | 224 | flkR | 227 | flkR | +0.058730 | 0.046992 |
| L8 | H12 | 224 | flkR | 267 | other | +0.052407 | 0.134556 |
| L10 | H8 | 243 | flkR | 224 | flkR | +0.047546 | 0.209664 |
| L12 | H15 | 207 | ss2 | 224 | flkR | +0.047371 | 0.462219 |
| L17 | H8 | 200 | ss2 | 224 | flkR | +0.047362 | 0.522378 |
| L16 | H2 | 205 | ss2 | 227 | flkR | +0.045670 | 0.909268 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L11 | H16 | 200 | ss2 | 243 | flkR | -0.019632 | 0.367856 |
| L16 | H13 | 63 | ss1 | 243 | flkR | -0.019717 | 0.340837 |
| L16 | H2 | 243 | flkR | 227 | flkR | -0.020400 | 0.818220 |
| L16 | H2 | 59 | ss1 | 227 | flkR | -0.020980 | 0.854945 |
| L16 | H2 | 58 | ss1 | 227 | flkR | -0.021100 | 0.904466 |
| L12 | H15 | 200 | ss2 | 224 | flkR | -0.021279 | 0.455058 |
| L10 | H12 | 43 | flkL | 43 | flkL | -0.021725 | 0.091318 |
| L14 | H12 | 200 | ss2 | 224 | flkR | -0.022279 | 0.402566 |
| L16 | H2 | 201 | ss2 | 227 | flkR | -0.024609 | 0.815230 |
| L27 | H15 | 55 | ss1 | 206 | ss2 | -0.025246 | 0.670934 |
| L21 | H6 | 203 | ss2 | 207 | ss2 | -0.025812 | 0.653423 |
| L16 | H2 | 204 | ss2 | 227 | flkR | -0.026426 | 0.883700 |
| L10 | H9 | 224 | flkR | 224 | flkR | -0.030496 | 0.184176 |
| L21 | H6 | 204 | ss2 | 207 | ss2 | -0.035205 | 0.614953 |
| L14 | H0 | 243 | flkR | 224 | flkR | -0.036998 | 0.307817 |
| L16 | H2 | 202 | ss2 | 227 | flkR | -0.037237 | 0.877297 |
| L16 | H2 | 205 | ss2 | 224 | flkR | -0.039996 | 0.724227 |
| L16 | H2 | 61 | ss1 | 227 | flkR | -0.041350 | 0.858404 |
| L17 | H8 | 207 | ss2 | 224 | flkR | -0.044733 | 0.433285 |
| L16 | H2 | 57 | ss1 | 227 | flkR | -0.050355 | 0.883925 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0235 | 0.00% |
| 10 | 10 | 7 | 0.0235 | 0.00% |
| 20 | 20 | 16 | 0.0235 | 0.00% |
| 50 | 50 | 27 | 0.0237 | 0.04% |
| 100 | 100 | 37 | 0.0249 | 0.23% |
| 200 | 200 | 42 | 0.0424 | 3.01% |
| 500 | 500 | 53 | 0.0710 | 7.57% |
| 1000 | 1,000 | 56 | 0.1487 | 19.92% |
| 2000 | 2,000 | 60 | 0.2263 | 32.28% |
| 5000 | 5,000 | 60 | 0.2976 | 43.62% |
| 10000 | 10,000 | 60 | 0.3684 | 54.88% |
| 20000 | 20,000 | 60 | 0.4626 | 69.87% |
| 50000 | 50,000 | 60 | 0.5867 | 89.62% |

## Motif Analysis

### L0 H1 — Rank #25

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 19  |  total attr: +0.0431

**Key mass** (top-1=24%, top-2=33%, top-3=42%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 4 | flkL | +0.0104 | 24.3% |
| 228 | flkR | +0.0038 | 8.9% |
| 227 | flkR | +0.0038 | 8.8% |
| 203 | ss2 | +0.0029 | 6.8% |
| 245 | flkR | +0.0025 | 5.7% |

**Query mass** (top-1=76%, top-2=84%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 258 | flkR | +0.0326 | 75.7% |
| 48 | flkL | +0.0037 | 8.7% |
| 38 | flkL | +0.0019 | 4.3% |
| 51 | flkL | +0.0018 | 4.1% |
| 256 | flkR | +0.0017 | 3.9% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +252 | 2 | 10.5% |
| +30 | 1 | 5.3% |
| +31 | 1 | 5.3% |
| +44 | 1 | 5.3% |
| +55 | 1 | 5.3% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 10 | 52.6% |
| flkR | flkL | 4 | 21.1% |
| flkL | flkL | 3 | 15.8% |
| flkR | ss2 | 2 | 10.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 258 | flkR | 228 | flkR | +0.0038 | 0.0136 |
| 258 | flkR | 227 | flkR | +0.0038 | 0.0133 |
| 48 | flkL | 4 | flkL | +0.0037 | 0.0108 |
| 258 | flkR | 203 | ss2 | +0.0029 | 0.0103 |
| 258 | flkR | 245 | flkR | +0.0025 | 0.0110 |

### L5 H13 — Rank #24

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.0405

**Key mass** (top-1=29%, top-2=46%, top-3=56%)  [DISTR(K258/I43/M254/S255/F47)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 258 | flkR | +0.0118 | 29.0% |
| 43 | flkL | +0.0068 | 16.8% |
| 254 | flkR | +0.0043 | 10.7% |
| 255 | flkR | +0.0040 | 10.0% |
| 47 | flkL | +0.0040 | 9.8% |

**Query mass** (top-1=84%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.0340 | 83.8% |
| 267 | other | +0.0044 | 11.0% |
| 227 | flkR | +0.0021 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -31 | 2 | 18.2% |
| -34 | 1 | 9.1% |
| +181 | 1 | 9.1% |
| -30 | 1 | 9.1% |
| +177 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 36.4% |
| flkR | other | 3 | 27.3% |
| flkR | flkL | 2 | 18.2% |
| other | flkR | 1 | 9.1% |
| other | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 224 | flkR | 258 | flkR | +0.0096 | 0.0039 |
| 224 | flkR | 43 | flkL | +0.0046 | 0.0014 |
| 224 | flkR | 254 | flkR | +0.0043 | 0.0021 |
| 224 | flkR | 255 | flkR | +0.0040 | 0.0024 |
| 224 | flkR | 47 | flkL | +0.0040 | 0.0017 |

### L6 H16 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 7  |  total attr: +0.0582

**Key mass** (top-1=77%, top-2=84%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0446 | 76.6% |
| 242 | flkR | +0.0041 | 7.0% |
| 251 | flkR | +0.0023 | 4.0% |
| 4 | flkL | +0.0021 | 3.6% |
| 211 | flkR | +0.0019 | 3.3% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.0582 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -19 | 1 | 14.3% |
| -18 | 1 | 14.3% |
| -27 | 1 | 14.3% |
| +220 | 1 | 14.3% |
| +13 | 1 | 14.3% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 57.1% |
| flkR | other | 2 | 28.6% |
| flkR | flkL | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 224 | flkR | 243 | flkR | +0.0446 | 0.0378 |
| 224 | flkR | 242 | flkR | +0.0041 | 0.0039 |
| 224 | flkR | 251 | flkR | +0.0023 | 0.0023 |
| 224 | flkR | 4 | flkL | +0.0021 | 0.0019 |
| 224 | flkR | 211 | flkR | +0.0019 | 0.0026 |

### L7 H9 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR  |  cells: 7  |  total attr: +0.6545

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.6525 | 99.7% |
| 240 | flkR | +0.0021 | 0.3% |

**Query mass** (top-1=43%, top-2=66%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 267 | other | +0.2839 | 43.4% |
| 265 | other | +0.1483 | 22.7% |
| 266 | other | +0.1071 | 16.4% |
| 269 | other | +0.0737 | 11.3% |
| 268 | other | +0.0396 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +43 | 1 | 14.3% |
| +41 | 1 | 14.3% |
| +42 | 1 | 14.3% |
| +45 | 1 | 14.3% |
| +44 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 7 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 267 | other | 224 | flkR | +0.2818 | 0.1412 |
| 265 | other | 224 | flkR | +0.1483 | 0.1794 |
| 266 | other | 224 | flkR | +0.1071 | 0.1601 |
| 269 | other | 224 | flkR | +0.0737 | 0.2002 |
| 268 | other | 224 | flkR | +0.0396 | 0.1490 |

### L8 H12 — Rank #11

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +0.1729

**Key mass** (top-1=30%, top-2=55%, top-3=74%)  [DISTR(T267/F265/G269)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 267 | other | +0.0524 | 30.3% |
| 265 | other | +0.0434 | 25.1% |
| 269 | other | +0.0323 | 18.7% |
| 266 | other | +0.0265 | 15.3% |
| 268 | other | +0.0129 | 7.5% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.1729 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -43 | 1 | 16.7% |
| -41 | 1 | 16.7% |
| -45 | 1 | 16.7% |
| -42 | 1 | 16.7% |
| -44 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 6 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 224 | flkR | 267 | other | +0.0524 | 0.1346 |
| 224 | flkR | 265 | other | +0.0434 | 0.1126 |
| 224 | flkR | 269 | other | +0.0323 | 0.0929 |
| 224 | flkR | 266 | other | +0.0265 | 0.0788 |
| 224 | flkR | 268 | other | +0.0129 | 0.0435 |

### L8 H15 — Rank #12

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L10 H6 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 18  |  total attr: +0.1234

**Key mass** (top-1=53%, top-2=73%, top-3=86%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 267 | other | +0.0654 | 53.0% |
| 266 | other | +0.0251 | 20.4% |
| 265 | other | +0.0158 | 12.8% |
| 269 | other | +0.0121 | 9.8% |
| 268 | other | +0.0028 | 2.3% |

**Query mass** (top-1=66%, top-2=78%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0811 | 65.7% |
| 247 | flkR | +0.0146 | 11.9% |
| 250 | flkR | +0.0140 | 11.3% |
| 246 | flkR | +0.0112 | 9.1% |
| 244 | flkR | +0.0025 | 2.0% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -23 | 3 | 16.7% |
| -22 | 2 | 11.1% |
| -20 | 2 | 11.1% |
| -21 | 2 | 11.1% |
| -19 | 2 | 11.1% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 18 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 267 | other | +0.0415 | 0.1122 |
| 243 | flkR | 266 | other | +0.0179 | 0.0588 |
| 243 | flkR | 265 | other | +0.0122 | 0.0408 |
| 247 | flkR | 267 | other | +0.0079 | 0.2138 |
| 246 | flkR | 267 | other | +0.0068 | 0.1650 |

### L10 H9 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 33  |  total attr: +0.1301

**Key mass** (top-1=36%, top-2=59%, top-3=72%)  [DISTR(T267/F265/I43)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 267 | other | +0.0473 | 36.3% |
| 265 | other | +0.0298 | 22.9% |
| 43 | flkL | +0.0165 | 12.7% |
| 266 | other | +0.0146 | 11.2% |
| 224 | flkR | +0.0139 | 10.7% |

**Query mass** (top-1=34%, top-2=63%, top-3=72%)  [DISTR(G243/I224/T247)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0440 | 33.8% |
| 224 | flkR | +0.0381 | 29.3% |
| 247 | flkR | +0.0115 | 8.9% |
| 250 | flkR | +0.0101 | 7.8% |
| 207 | ss2 | +0.0065 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -19 | 3 | 9.1% |
| -23 | 2 | 6.1% |
| -17 | 2 | 6.1% |
| -60 | 2 | 6.1% |
| -25 | 2 | 6.1% |

**Region-pair profile** (q→k)  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 20 | 60.6% |
| flkR | flkL | 4 | 12.1% |
| ss2 | other | 4 | 12.1% |
| flkR | flkR | 3 | 9.1% |
| other | flkL | 1 | 3.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 224 | flkR | 267 | other | +0.0188 | 0.2656 |
| 243 | flkR | 267 | other | +0.0118 | 0.0288 |
| 224 | flkR | 265 | other | +0.0104 | 0.2122 |
| 243 | flkR | 224 | flkR | +0.0084 | 0.0235 |
| 243 | flkR | 43 | flkL | +0.0075 | 0.0989 |

### L10 H12 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 8  |  total attr: +0.1065

**Key mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.1017 | 95.5% |
| 43 | flkL | +0.0048 | 4.5% |

**Query mass** (top-1=77%, top-2=85%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0820 | 77.0% |
| 250 | flkR | +0.0088 | 8.3% |
| 247 | flkR | +0.0037 | 3.4% |
| 68 | other | +0.0031 | 2.9% |
| 239 | flkR | +0.0029 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +19 | 1 | 12.5% |
| +26 | 1 | 12.5% |
| +23 | 1 | 12.5% |
| +25 | 1 | 12.5% |
| +15 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 6 | 75.0% |
| other | flkL | 1 | 12.5% |
| flkL | flkL | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 224 | flkR | +0.0820 | 0.2508 |
| 250 | flkR | 224 | flkR | +0.0088 | 0.3034 |
| 247 | flkR | 224 | flkR | +0.0037 | 0.2314 |
| 68 | other | 43 | flkL | +0.0031 | 0.1234 |
| 239 | flkR | 224 | flkR | +0.0029 | 0.2287 |

### L11 H14 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 11  |  total attr: +0.1147

**Key mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.1093 | 95.3% |
| 43 | flkL | +0.0054 | 4.7% |

**Query mass** (top-1=61%, top-2=77%, top-3=83%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0699 | 60.9% |
| 250 | flkR | +0.0183 | 16.0% |
| 247 | flkR | +0.0065 | 5.7% |
| 248 | flkR | +0.0035 | 3.1% |
| 254 | flkR | +0.0033 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +24 | 2 | 18.2% |
| +29 | 2 | 18.2% |
| +19 | 1 | 9.1% |
| +26 | 1 | 9.1% |
| +23 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 8 | 72.7% |
| other | flkL | 3 | 27.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 224 | flkR | +0.0699 | 0.2202 |
| 250 | flkR | 224 | flkR | +0.0183 | 0.3578 |
| 247 | flkR | 224 | flkR | +0.0065 | 0.2791 |
| 248 | flkR | 224 | flkR | +0.0035 | 0.3652 |
| 254 | flkR | 224 | flkR | +0.0033 | 0.1895 |

### L11 H16 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 39  |  total attr: +0.1529

**Key mass** (top-1=78%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.1191 | 77.9% |
| 43 | flkL | +0.0291 | 19.0% |
| 242 | flkR | +0.0032 | 2.1% |
| 230 | flkR | +0.0015 | 1.0% |

**Query mass** (top-1=20%, top-2=29%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0307 | 20.0% |
| 243 | flkR | +0.0142 | 9.3% |
| 202 | ss2 | +0.0096 | 6.3% |
| 209 | flkR | +0.0074 | 4.8% |
| -1 | other | +0.0064 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -36 | 1 | 2.6% |
| +200 | 1 | 2.6% |
| -34 | 1 | 2.6% |
| -41 | 1 | 2.6% |
| -244 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 14 | 35.9% |
| ss2 | flkR | 7 | 17.9% |
| ss1 | flkR | 6 | 15.4% |
| other | flkR | 5 | 12.8% |
| flkR | flkL | 3 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 207 | ss2 | 243 | flkR | +0.0307 | 0.4872 |
| 243 | flkR | 43 | flkL | +0.0142 | 0.2130 |
| 209 | flkR | 243 | flkR | +0.0074 | 0.4410 |
| 202 | ss2 | 243 | flkR | +0.0066 | 0.5241 |
| -1 | other | 243 | flkR | +0.0064 | 0.4488 |

### L12 H15 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.3408

**Key mass** (top-1=36%, top-2=65%, top-3=80%)  [DISTR(I224/T267/I266)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.1240 | 36.4% |
| 267 | other | +0.0989 | 29.0% |
| 266 | other | +0.0487 | 14.3% |
| 265 | other | +0.0460 | 13.5% |
| 269 | other | +0.0165 | 4.8% |

**Query mass** (top-1=55%, top-2=69%, top-3=77%)  [DISTR(G243/A207/S202)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.1883 | 55.3% |
| 207 | ss2 | +0.0474 | 13.9% |
| 202 | ss2 | +0.0272 | 8.0% |
| 197 | other | +0.0158 | 4.6% |
| 201 | ss2 | +0.0142 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -23 | 3 | 12.5% |
| -17 | 2 | 8.3% |
| -22 | 2 | 8.3% |
| -15 | 2 | 8.3% |
| -20 | 2 | 8.3% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 16 | 66.7% |
| ss2 | flkR | 4 | 16.7% |
| other | flkR | 2 | 8.3% |
| flkR | flkR | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 267 | other | +0.0847 | 0.3287 |
| 207 | ss2 | 224 | flkR | +0.0474 | 0.4622 |
| 243 | flkR | 266 | other | +0.0415 | 0.2091 |
| 243 | flkR | 265 | other | +0.0379 | 0.1836 |
| 202 | ss2 | 224 | flkR | +0.0272 | 0.5668 |

### L13 H3 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 18  |  total attr: +0.0735

**Key mass** (top-1=69%, top-2=78%, top-3=84%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.0505 | 68.7% |
| 227 | flkR | +0.0072 | 9.8% |
| 204 | ss2 | +0.0040 | 5.5% |
| 229 | flkR | +0.0019 | 2.6% |
| 243 | flkR | +0.0018 | 2.5% |

**Query mass** (top-1=21%, top-2=36%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | flkR | +0.0155 | 21.1% |
| 243 | flkR | +0.0112 | 15.2% |
| 224 | flkR | +0.0072 | 9.8% |
| 228 | flkR | +0.0065 | 8.8% |
| 229 | flkR | +0.0062 | 8.5% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 4 | 22.2% |
| +7 | 2 | 11.1% |
| +9 | 2 | 11.1% |
| +3 | 1 | 5.6% |
| +19 | 1 | 5.6% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=72%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 13 | 72.2% |
| other | flkL | 2 | 11.1% |
| ss1 | ss1 | 2 | 11.1% |
| ss2 | ss2 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | flkR | 224 | flkR | +0.0155 | 0.2591 |
| 243 | flkR | 224 | flkR | +0.0094 | 0.3360 |
| 224 | flkR | 227 | flkR | +0.0072 | 0.2224 |
| 228 | flkR | 224 | flkR | +0.0065 | 0.5050 |
| 225 | flkR | 224 | flkR | +0.0051 | 0.3444 |

### L13 H13 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 2  |  total attr: +0.0052

**Key mass** (top-1=74%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 231 | flkR | +0.0039 | 74.1% |
| 80 | other | +0.0014 | 25.9% |

**Query mass** (top-1=74%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0039 | 74.1% |
| 68 | other | +0.0014 | 25.9% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -24 | 1 | 50.0% |
| -12 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 1 | 50.0% |
| other | other | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 207 | ss2 | 231 | flkR | +0.0039 | 0.0544 |
| 68 | other | 80 | other | +0.0014 | 0.0156 |

### L14 H0 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 21  |  total attr: +0.1693

**Key mass** (top-1=61%, top-2=79%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | flkR | +0.1035 | 61.1% |
| 224 | flkR | +0.0297 | 17.5% |
| 228 | flkR | +0.0167 | 9.8% |
| 229 | flkR | +0.0137 | 8.1% |
| 226 | flkR | +0.0039 | 2.3% |

**Query mass** (top-1=63%, top-2=74%, top-3=83%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.1075 | 63.5% |
| 205 | ss2 | +0.0186 | 11.0% |
| 206 | ss2 | +0.0149 | 8.8% |
| 202 | ss2 | +0.0099 | 5.9% |
| 203 | ss2 | +0.0071 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -22 | 4 | 19.0% |
| -21 | 2 | 9.5% |
| -19 | 2 | 9.5% |
| -25 | 2 | 9.5% |
| -24 | 2 | 9.5% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 18 | 85.7% |
| flkR | flkR | 2 | 9.5% |
| ss1 | flkR | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 207 | ss2 | 227 | flkR | +0.0661 | 0.3247 |
| 207 | ss2 | 224 | flkR | +0.0173 | 0.0968 |
| 205 | ss2 | 227 | flkR | +0.0147 | 0.3604 |
| 207 | ss2 | 228 | flkR | +0.0104 | 0.0748 |
| 206 | ss2 | 227 | flkR | +0.0103 | 0.2565 |

### L14 H12 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 15  |  total attr: +0.2008

**Key mass** (top-1=88%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.1767 | 88.0% |
| 243 | flkR | +0.0159 | 7.9% |
| 227 | flkR | +0.0067 | 3.3% |
| 247 | flkR | +0.0016 | 0.8% |

**Query mass** (top-1=68%, top-2=77%, top-3=82%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.1371 | 68.2% |
| 227 | flkR | +0.0169 | 8.4% |
| 204 | ss2 | +0.0098 | 4.9% |
| 205 | ss2 | +0.0097 | 4.8% |
| 203 | ss2 | +0.0085 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 3 | 20.0% |
| -14 | 2 | 13.3% |
| -17 | 1 | 6.7% |
| -16 | 1 | 6.7% |
| -19 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 10 | 66.7% |
| ss2 | flkR | 5 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 207 | ss2 | 224 | flkR | +0.1325 | 0.5117 |
| 227 | flkR | 243 | flkR | +0.0132 | 0.1204 |
| 204 | ss2 | 224 | flkR | +0.0098 | 0.4398 |
| 205 | ss2 | 224 | flkR | +0.0097 | 0.5253 |
| 203 | ss2 | 224 | flkR | +0.0085 | 0.3816 |

### L16 H5 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 8  |  total attr: +0.0673

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0673 | 100.0% |

**Query mass** (top-1=33%, top-2=58%, top-3=69%)  [DISTR(G243/V246/T247/I224)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0223 | 33.1% |
| 246 | flkR | +0.0168 | 24.9% |
| 247 | flkR | +0.0077 | 11.4% |
| 224 | flkR | +0.0064 | 9.5% |
| 244 | flkR | +0.0047 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 12.5% |
| +3 | 1 | 12.5% |
| +4 | 1 | 12.5% |
| -19 | 1 | 12.5% |
| +1 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 8 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 243 | flkR | +0.0223 | 0.6916 |
| 246 | flkR | 243 | flkR | +0.0168 | 0.5967 |
| 247 | flkR | 243 | flkR | +0.0077 | 0.3158 |
| 224 | flkR | 243 | flkR | +0.0064 | 0.0914 |
| 244 | flkR | 243 | flkR | +0.0047 | 0.1781 |

### L16 H13 — Rank #30

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 57  |  total attr: +0.2434

**Key mass** (top-1=54%, top-2=69%, top-3=80%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.1306 | 53.7% |
| 247 | flkR | +0.0368 | 15.1% |
| 421 | other | +0.0275 | 11.3% |
| 246 | flkR | +0.0272 | 11.2% |
| 245 | flkR | +0.0096 | 4.0% |

**Query mass** (top-1=16%, top-2=29%, top-3=41%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 54 | ss1 | +0.0382 | 15.7% |
| 56 | ss1 | +0.0320 | 13.1% |
| 47 | flkL | +0.0296 | 12.2% |
| 58 | ss1 | +0.0236 | 9.7% |
| 57 | ss1 | +0.0232 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -189 | 4 | 7.0% |
| -191 | 3 | 5.3% |
| -188 | 3 | 5.3% |
| -187 | 2 | 3.5% |
| -196 | 2 | 3.5% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 21 | 36.8% |
| flkL | flkR | 15 | 26.3% |
| ss2 | flkR | 9 | 15.8% |
| ss1 | other | 4 | 7.0% |
| ss2 | other | 3 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 54 | ss1 | 243 | flkR | +0.0215 | 0.3477 |
| 56 | ss1 | 243 | flkR | +0.0213 | 0.3813 |
| 47 | flkL | 243 | flkR | +0.0186 | 0.3686 |
| 57 | ss1 | 243 | flkR | +0.0132 | 0.3073 |
| 58 | ss1 | 243 | flkR | +0.0115 | 0.2718 |

### L17 H8 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 24  |  total attr: +0.1606

**Key mass** (top-1=71%, top-2=94%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 224 | flkR | +0.1145 | 71.3% |
| 227 | flkR | +0.0359 | 22.4% |
| 229 | flkR | +0.0053 | 3.3% |
| 54 | ss1 | +0.0021 | 1.3% |
| 243 | flkR | +0.0014 | 0.9% |

**Query mass** (top-1=31%, top-2=46%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0506 | 31.5% |
| 203 | ss2 | +0.0234 | 14.6% |
| 207 | ss2 | +0.0169 | 10.5% |
| 202 | ss2 | +0.0101 | 6.3% |
| 243 | flkR | +0.0087 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -21 | 2 | 8.3% |
| -20 | 2 | 8.3% |
| +19 | 2 | 8.3% |
| -22 | 2 | 8.3% |
| -26 | 2 | 8.3% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 15 | 62.5% |
| flkR | flkR | 7 | 29.2% |
| other | flkR | 1 | 4.2% |
| other | ss1 | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | ss2 | 224 | flkR | +0.0474 | 0.5224 |
| 203 | ss2 | 224 | flkR | +0.0234 | 0.4822 |
| 207 | ss2 | 227 | flkR | +0.0155 | 0.3164 |
| 243 | flkR | 224 | flkR | +0.0087 | 0.3733 |
| 202 | ss2 | 224 | flkR | +0.0079 | 0.4356 |

### L20 H5 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0608

**Key mass** (top-1=65%, top-2=79%, top-3=85%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0393 | 64.6% |
| 209 | flkR | +0.0088 | 14.6% |
| 66 | other | +0.0037 | 6.0% |
| 217 | flkR | +0.0027 | 4.4% |
| 224 | flkR | +0.0024 | 4.0% |

**Query mass** (top-1=28%, top-2=50%, top-3=69%)  [DISTR(L200/T199/S202/N204)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0172 | 28.3% |
| 199 | ss2 | +0.0134 | 22.1% |
| 202 | ss2 | +0.0111 | 18.2% |
| 204 | ss2 | +0.0029 | 4.7% |
| 207 | ss2 | +0.0027 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 3 | 18.8% |
| -8 | 3 | 18.8% |
| -10 | 3 | 18.8% |
| -5 | 2 | 12.5% |
| -9 | 2 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 37.5% |
| ss2 | flkR | 5 | 31.2% |
| flkR | flkR | 2 | 12.5% |
| ss1 | other | 2 | 12.5% |
| other | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | ss2 | 207 | ss2 | +0.0145 | 0.3052 |
| 199 | ss2 | 207 | ss2 | +0.0119 | 0.3865 |
| 202 | ss2 | 207 | ss2 | +0.0048 | 0.1520 |
| 202 | ss2 | 209 | flkR | +0.0046 | 0.1027 |
| 204 | ss2 | 207 | ss2 | +0.0029 | 0.0678 |

### L21 H6 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 27  |  total attr: +0.1871

**Key mass** (top-1=83%, top-2=88%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.1551 | 82.9% |
| 54 | ss1 | +0.0097 | 5.2% |
| 43 | flkL | +0.0095 | 5.1% |
| 205 | ss2 | +0.0052 | 2.8% |
| 227 | flkR | +0.0029 | 1.5% |

**Query mass** (top-1=34%, top-2=58%, top-3=67%)  [DISTR(T199/L200/S202/T201)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0645 | 34.5% |
| 200 | ss2 | +0.0439 | 23.5% |
| 202 | ss2 | +0.0166 | 8.9% |
| 201 | ss2 | +0.0118 | 6.3% |
| 197 | other | +0.0051 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 2 | 7.4% |
| +13 | 2 | 7.4% |
| -1 | 2 | 7.4% |
| -9 | 2 | 7.4% |
| +0 | 2 | 7.4% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 11 | 40.7% |
| other | ss2 | 4 | 14.8% |
| other | ss1 | 3 | 11.1% |
| flkL | flkL | 3 | 11.1% |
| ss1 | flkL | 2 | 7.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | ss2 | 207 | ss2 | +0.0610 | 0.6552 |
| 200 | ss2 | 207 | ss2 | +0.0439 | 0.7054 |
| 202 | ss2 | 207 | ss2 | +0.0153 | 0.7171 |
| 201 | ss2 | 207 | ss2 | +0.0118 | 0.7523 |
| 197 | other | 207 | ss2 | +0.0051 | 0.1905 |

### L21 H10 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 17  |  total attr: +0.1914

**Key mass** (top-1=96%, top-2=97%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.1828 | 95.5% |
| 245 | flkR | +0.0027 | 1.4% |
| 247 | flkR | +0.0026 | 1.4% |
| 222 | flkR | +0.0016 | 0.8% |
| 224 | flkR | +0.0016 | 0.8% |

**Query mass** (top-1=47%, top-2=63%, top-3=71%)  [DISTR(G243/A207/G225)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0905 | 47.3% |
| 207 | ss2 | +0.0295 | 15.4% |
| 225 | flkR | +0.0155 | 8.1% |
| 205 | ss2 | +0.0120 | 6.3% |
| 224 | flkR | +0.0089 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 5.9% |
| -36 | 1 | 5.9% |
| -18 | 1 | 5.9% |
| -19 | 1 | 5.9% |
| -1 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=76%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 13 | 76.5% |
| ss2 | flkR | 4 | 23.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 243 | flkR | +0.0873 | 0.7944 |
| 207 | ss2 | 243 | flkR | +0.0295 | 0.4600 |
| 225 | flkR | 243 | flkR | +0.0155 | 0.6914 |
| 224 | flkR | 243 | flkR | +0.0089 | 0.5018 |
| 242 | flkR | 243 | flkR | +0.0076 | 0.7076 |

### L22 H15 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 9  |  total attr: +0.0944

**Key mass** (top-1=94%, top-2=97%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0885 | 93.7% |
| 218 | flkR | +0.0029 | 3.1% |
| 66 | other | +0.0015 | 1.6% |
| 67 | other | +0.0014 | 1.5% |

**Query mass** (top-1=43%, top-2=65%, top-3=79%)  [DISTR(K198/T199/L200)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0403 | 42.6% |
| 199 | ss2 | +0.0210 | 22.3% |
| 200 | ss2 | +0.0135 | 14.3% |
| 197 | other | +0.0087 | 9.2% |
| 196 | other | +0.0035 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -10 | 2 | 22.2% |
| -11 | 2 | 22.2% |
| -9 | 1 | 11.1% |
| -8 | 1 | 11.1% |
| -7 | 1 | 11.1% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 4 | 44.4% |
| other | ss2 | 2 | 22.2% |
| ss1 | other | 2 | 22.2% |
| ss2 | flkR | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 198 | ss2 | 207 | ss2 | +0.0403 | 0.7045 |
| 199 | ss2 | 207 | ss2 | +0.0210 | 0.6535 |
| 200 | ss2 | 207 | ss2 | +0.0135 | 0.3423 |
| 197 | other | 207 | ss2 | +0.0087 | 0.7858 |
| 196 | other | 207 | ss2 | +0.0035 | 0.6423 |

### L22 H17 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 68  |  total attr: +0.5104

**Key mass** (top-1=91%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.4642 | 91.0% |
| 47 | flkL | +0.0320 | 6.3% |
| 224 | flkR | +0.0103 | 2.0% |
| 205 | ss2 | +0.0023 | 0.4% |
| 207 | ss2 | +0.0016 | 0.3% |

**Query mass** (top-1=12%, top-2=19%, top-3=26%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0596 | 11.7% |
| 58 | ss1 | +0.0398 | 7.8% |
| 201 | ss2 | +0.0339 | 6.6% |
| 197 | other | +0.0295 | 5.8% |
| 56 | ss1 | +0.0231 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -11 | 2 | 2.9% |
| -3 | 2 | 2.9% |
| -17 | 2 | 2.9% |
| -43 | 1 | 1.5% |
| -185 | 1 | 1.5% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 15 | 22.1% |
| flkR | flkR | 15 | 22.1% |
| ss2 | flkR | 12 | 17.6% |
| ss1 | flkR | 10 | 14.7% |
| flkL | flkL | 7 | 10.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | ss2 | 243 | flkR | +0.0596 | 0.7719 |
| 58 | ss1 | 243 | flkR | +0.0398 | 0.5368 |
| 201 | ss2 | 243 | flkR | +0.0339 | 0.8581 |
| 197 | other | 243 | flkR | +0.0295 | 0.8468 |
| 56 | ss1 | 243 | flkR | +0.0231 | 0.5508 |

### L26 H11 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:ss2  |  cells: 14  |  total attr: +0.1280

**Key mass** (top-1=74%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0948 | 74.1% |
| 204 | ss2 | +0.0187 | 14.6% |
| 211 | flkR | +0.0051 | 4.0% |
| 205 | ss2 | +0.0026 | 2.0% |
| 65 | other | +0.0021 | 1.6% |

**Query mass** (top-1=55%, top-2=74%, top-3=83%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0706 | 55.1% |
| 201 | ss2 | +0.0240 | 18.7% |
| 200 | ss2 | +0.0123 | 9.6% |
| 199 | ss2 | +0.0056 | 4.4% |
| 198 | ss2 | +0.0052 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 5 | 35.7% |
| -4 | 3 | 21.4% |
| -6 | 2 | 14.3% |
| -11 | 1 | 7.1% |
| +1 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 7 | 50.0% |
| ss2 | flkR | 4 | 28.6% |
| ss1 | other | 1 | 7.1% |
| flkR | flkR | 1 | 7.1% |
| ss1 | ss1 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 202 | ss2 | 207 | ss2 | +0.0691 | 0.6904 |
| 201 | ss2 | 207 | ss2 | +0.0240 | 0.5391 |
| 200 | ss2 | 204 | ss2 | +0.0079 | 0.2663 |
| 199 | ss2 | 204 | ss2 | +0.0056 | 0.6507 |
| 198 | ss2 | 204 | ss2 | +0.0052 | 0.5170 |

### L27 H15 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 28  |  total attr: +0.1565

**Key mass** (top-1=33%, top-2=53%, top-3=61%)  [DISTR(L200/T201/H203/E55/A207)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0520 | 33.2% |
| 201 | ss2 | +0.0315 | 20.1% |
| 203 | ss2 | +0.0120 | 7.7% |
| 55 | ss1 | +0.0118 | 7.5% |
| 207 | ss2 | +0.0102 | 6.5% |

**Query mass** (top-1=36%, top-2=52%, top-3=60%)  [DISTR(F61/P58/F59/V54/Q57)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0561 | 35.9% |
| 58 | ss1 | +0.0255 | 16.3% |
| 59 | ss1 | +0.0125 | 8.0% |
| 54 | ss1 | +0.0106 | 6.8% |
| 57 | ss1 | +0.0105 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -141 | 3 | 10.7% |
| -143 | 2 | 7.1% |
| -147 | 2 | 7.1% |
| -43 | 2 | 7.1% |
| -139 | 1 | 3.6% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 15 | 53.6% |
| ss2 | ss1 | 5 | 17.9% |
| ss1 | ss1 | 3 | 10.7% |
| ss2 | flkR | 2 | 7.1% |
| ss2 | ss2 | 2 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 61 | ss1 | 200 | ss2 | +0.0445 | 0.2539 |
| 58 | ss1 | 201 | ss2 | +0.0175 | 0.1751 |
| 54 | ss1 | 207 | ss2 | +0.0086 | 0.1039 |
| 61 | ss1 | 201 | ss2 | +0.0084 | 0.1803 |
| 58 | ss1 | 203 | ss2 | +0.0080 | 0.1109 |

### L29 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 45  |  total attr: +0.2921

**Key mass** (top-1=23%, top-2=35%, top-3=46%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 58 | ss1 | +0.0673 | 23.1% |
| 203 | ss2 | +0.0341 | 11.7% |
| 199 | ss2 | +0.0338 | 11.6% |
| 201 | ss2 | +0.0303 | 10.4% |
| 62 | ss1 | +0.0160 | 5.5% |

**Query mass** (top-1=25%, top-2=42%, top-3=54%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0735 | 25.2% |
| 62 | ss1 | +0.0496 | 17.0% |
| 58 | ss1 | +0.0336 | 11.5% |
| 199 | ss2 | +0.0183 | 6.3% |
| 200 | ss2 | +0.0137 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -139 | 3 | 6.7% |
| -145 | 2 | 4.4% |
| -137 | 2 | 4.4% |
| +137 | 2 | 4.4% |
| +147 | 2 | 4.4% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 15 | 33.3% |
| ss2 | ss1 | 11 | 24.4% |
| ss2 | flkL | 6 | 13.3% |
| flkR | flkL | 4 | 8.9% |
| flkL | flkR | 2 | 4.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 58 | ss1 | +0.0649 | 0.6362 |
| 58 | ss1 | 203 | ss2 | +0.0313 | 0.7943 |
| 62 | ss1 | 199 | ss2 | +0.0275 | 0.3077 |
| 62 | ss1 | 201 | ss2 | +0.0221 | 0.3443 |
| 199 | ss2 | 62 | ss1 | +0.0145 | 0.5190 |

### L31 H17 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.1016

**Key mass** (top-1=85%, top-2=90%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0868 | 85.5% |
| 228 | flkR | +0.0041 | 4.0% |
| 203 | ss2 | +0.0036 | 3.5% |
| 59 | ss1 | +0.0026 | 2.6% |
| 54 | ss1 | +0.0016 | 1.5% |

**Query mass** (top-1=18%, top-2=36%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0187 | 18.4% |
| 200 | ss2 | +0.0173 | 17.1% |
| 36 | flkL | +0.0095 | 9.4% |
| 37 | flkL | +0.0070 | 6.9% |
| 40 | flkL | +0.0069 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +200 | 1 | 4.3% |
| +201 | 1 | 4.3% |
| +209 | 1 | 4.3% |
| +205 | 1 | 4.3% |
| +202 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 8 | 34.8% |
| ss2 | other | 7 | 30.4% |
| flkL | ss2 | 3 | 13.0% |
| ss2 | ss1 | 2 | 8.7% |
| ss1 | other | 2 | 8.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | ss2 | -1 | other | +0.0187 | 0.1238 |
| 200 | ss2 | -1 | other | +0.0173 | 0.2041 |
| 208 | ss2 | -1 | other | +0.0065 | 0.1293 |
| 204 | ss2 | -1 | other | +0.0062 | 0.1782 |
| 201 | ss2 | -1 | other | +0.0058 | 0.1363 |

### L32 H13 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 26  |  total attr: +0.3179

**Key mass** (top-1=14%, top-2=24%, top-3=32%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0430 | 13.5% |
| 203 | ss2 | +0.0325 | 10.2% |
| 201 | ss2 | +0.0272 | 8.6% |
| 58 | ss1 | +0.0244 | 7.7% |
| 60 | ss1 | +0.0203 | 6.4% |

**Query mass** (top-1=11%, top-2=22%, top-3=31%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 58 | ss1 | +0.0352 | 11.1% |
| 199 | ss2 | +0.0339 | 10.7% |
| 200 | ss2 | +0.0304 | 9.5% |
| 60 | ss1 | +0.0281 | 8.9% |
| 201 | ss2 | +0.0256 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -139 | 2 | 7.7% |
| -143 | 2 | 7.7% |
| -147 | 2 | 7.7% |
| +143 | 2 | 7.7% |
| +139 | 2 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 13 | 50.0% |
| ss2 | ss1 | 13 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 199 | ss2 | +0.0253 | 0.4015 |
| 58 | ss1 | 201 | ss2 | +0.0244 | 0.2134 |
| 56 | ss1 | 203 | ss2 | +0.0217 | 0.1905 |
| 201 | ss2 | 58 | ss1 | +0.0213 | 0.1864 |
| 200 | ss2 | 61 | ss1 | +0.0195 | 0.1709 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 26  |  total attr: +0.1948

**Key mass** (top-1=15%, top-2=26%, top-3=36%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 56 | ss1 | +0.0295 | 15.1% |
| 59 | ss1 | +0.0206 | 10.6% |
| 54 | ss1 | +0.0196 | 10.0% |
| 202 | ss2 | +0.0166 | 8.5% |
| 61 | ss1 | +0.0165 | 8.5% |

**Query mass** (top-1=17%, top-2=33%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0341 | 17.5% |
| 200 | ss2 | +0.0299 | 15.4% |
| 202 | ss2 | +0.0206 | 10.6% |
| 59 | ss1 | +0.0166 | 8.5% |
| 57 | ss1 | +0.0157 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +147 | 2 | 7.7% |
| +143 | 2 | 7.7% |
| -143 | 2 | 7.7% |
| +139 | 2 | 7.7% |
| +153 | 2 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 14 | 53.8% |
| ss1 | ss2 | 12 | 46.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 56 | ss1 | +0.0295 | 0.1569 |
| 202 | ss2 | 59 | ss1 | +0.0206 | 0.1119 |
| 59 | ss1 | 202 | ss2 | +0.0166 | 0.0906 |
| 200 | ss2 | 61 | ss1 | +0.0165 | 0.0880 |
| 207 | ss2 | 54 | ss1 | +0.0118 | 0.0714 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #25 | L0 | H1 | 19 | +0.0431 | DISTRIBUTED |  | SINGLE-ANCHOR | K258 |  | INTRA:flkR |
| #24 | L5 | H13 | 11 | +0.0405 | DISTRIBUTED | K258/I43/M254/S255/F47 | SINGLE-ANCHOR | I224 |  |  |
| #23 | L6 | H16 | 7 | +0.0582 | SINGLE-ANCHOR | G243 | SINGLE-ANCHOR | I224 |  | INTRA:flkR |
| #1 | L7 | H9 | 7 | +0.6545 | SINGLE-ANCHOR | I224 | MULTI-ANCHOR |  |  |  |
| #11 | L8 | H12 | 6 | +0.1729 | DISTRIBUTED | T267/F265/G269 | SINGLE-ANCHOR | I224 |  |  |
| #12 | L8 | H15 | 0 | +0.0000 | — |  | — |  |  |  |
| #21 | L10 | H6 | 18 | +0.1234 | DUAL-ANCHOR | T267/I266 | SINGLE-ANCHOR | G243 |  |  |
| #8 | L10 | H9 | 33 | +0.1301 | DISTRIBUTED | T267/F265/I43 | DISTRIBUTED | G243/I224/T247 |  |  |
| #28 | L10 | H12 | 8 | +0.1065 | SINGLE-ANCHOR | I224 | SINGLE-ANCHOR | G243 |  | INTRA:flkR |
| #16 | L11 | H14 | 11 | +0.1147 | SINGLE-ANCHOR | I224 | SINGLE-ANCHOR | G243 |  | INTRA:flkR |
| #7 | L11 | H16 | 39 | +0.1529 | SINGLE-ANCHOR | G243 | DISTRIBUTED |  |  |  |
| #9 | L12 | H15 | 24 | +0.3408 | DISTRIBUTED | I224/T267/I266 | DISTRIBUTED | G243/A207/S202 |  |  |
| #26 | L13 | H3 | 18 | +0.0735 | SINGLE-ANCHOR | I224 | DISTRIBUTED |  |  | INTRA:flkR |
| #29 | L13 | H13 | 2 | +0.0052 | SINGLE-ANCHOR | V231 | SINGLE-ANCHOR | A207 |  | ss2→flkR |
| #20 | L14 | H0 | 21 | +0.1693 | SINGLE-ANCHOR | H227 | SINGLE-ANCHOR | A207 |  | ss2→flkR |
| #13 | L14 | H12 | 15 | +0.2008 | SINGLE-ANCHOR | I224 | SINGLE-ANCHOR | A207 |  | INTRA:flkR |
| #17 | L16 | H5 | 8 | +0.0673 | SINGLE-ANCHOR | G243 | DISTRIBUTED | G243/V246/T247/I224 |  | INTRA:flkR |
| #30 | L16 | H13 | 57 | +0.2434 | MULTI-ANCHOR |  | DISTRIBUTED |  |  |  |
| #18 | L17 | H8 | 24 | +0.1606 | SINGLE-ANCHOR | I224 | DISTRIBUTED |  |  | ss2→flkR |
| #27 | L20 | H5 | 16 | +0.0608 | SINGLE-ANCHOR | A207 | DISTRIBUTED | L200/T199/S202/N204 |  |  |
| #15 | L21 | H6 | 27 | +0.1871 | SINGLE-ANCHOR | A207 | DISTRIBUTED | T199/L200/S202/T201 |  | INTRA:ss2 |
| #19 | L21 | H10 | 17 | +0.1914 | SINGLE-ANCHOR | G243 | DISTRIBUTED | G243/A207/G225 |  | INTRA:flkR |
| #14 | L22 | H15 | 9 | +0.0944 | SINGLE-ANCHOR | A207 | DISTRIBUTED | K198/T199/L200 |  | INTRA:ss2 |
| #5 | L22 | H17 | 68 | +0.5104 | SINGLE-ANCHOR | G243 | DISTRIBUTED |  |  |  |
| #10 | L26 | H11 | 14 | +0.1280 | SINGLE-ANCHOR | A207 | DUAL-ANCHOR | S202/T201 |  | INTRA:ss2 |
| #6 | L27 | H15 | 28 | +0.1565 | DISTRIBUTED | L200/T201/H203/E55/A207 | DISTRIBUTED | F61/P58/F59/V54/Q57 |  | CROSS:ss1→ss2 |
| #3 | L29 | H18 | 45 | +0.2921 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #22 | L31 | H17 | 23 | +0.1016 | SINGLE-ANCHOR | ?-1 | DISTRIBUTED |  |  |  |
| #2 | L32 | H13 | 26 | +0.3179 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #4 | L32 | H18 | 26 | +0.1948 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
