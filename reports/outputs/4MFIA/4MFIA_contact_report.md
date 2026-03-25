# Contact Pattern Analysis: 4MFIA

Generated: 2026-03-22 21:56:03   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4MFIA |
| Contact pair | (157, 288) |
| ss1 | [152, 163) |
| ss2 | [283, 294) |
| Clean flank | 69 |
| Corrupt flank | 68 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.6302 |
| Corrupt metric | 0.0796 |
| Gap | 0.5506 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 90 | 70.98% |
| positive IE | 55 | 70.56% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H18 | +0.2606 |
| 2 | L32 | H13 | +0.2377 |
| 3 | L26 | H16 | +0.1407 |
| 4 | L11 | H16 | +0.1034 |
| 5 | L12 | H19 | +0.0866 |
| 6 | L29 | H18 | +0.0850 |
| 7 | L27 | H15 | +0.0840 |
| 8 | L30 | H1 | +0.0478 |
| 9 | L13 | H7 | +0.0435 |
| 10 | L21 | H13 | +0.0387 |
| 11 | L16 | H17 | +0.0384 |
| 12 | L21 | H2 | +0.0375 |
| 13 | L31 | H17 | +0.0373 |
| 14 | L16 | H2 | +0.0357 |
| 15 | L23 | H18 | +0.0324 |
| 16 | L15 | H3 | +0.0320 |
| 17 | L21 | H4 | +0.0280 |
| 18 | L7 | H13 | +0.0274 |
| 19 | L14 | H9 | +0.0271 |
| 20 | L26 | H11 | +0.0268 |
| 21 | L10 | H19 | +0.0267 |
| 22 | L16 | H1 | +0.0266 |
| 23 | L17 | H7 | +0.0251 |
| 24 | L14 | H17 | +0.0247 |
| 25 | L17 | H1 | +0.0246 |
| 26 | L27 | H9 | +0.0246 |
| 27 | L19 | H9 | +0.0244 |
| 28 | L17 | H8 | +0.0239 |
| 29 | L20 | H18 | +0.0235 |
| 30 | L15 | H1 | +0.0234 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 1.17% |
| 2 | 2.00% |
| 3 | 2.53% |
| 4 | 3.26% |
| 5 | 4.37% |
| 6 | 5.71% |
| 7 | 7.13% |
| 8 | 7.67% |
| 9 | 8.65% |
| 10 | 8.34% |
| 20 | 24.46% |
| 80 | 97.90% |
| 450 | 147.46% |

## Cell Attribution Analysis

Total cells: 9,686,336

- Positive: 4,894,068
- Negative: 4,787,314

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000016 | 968,635 |
| 95th | +0.00000056 | 484,318 |
| 99th | +0.00000524 | 96,864 |
| 99.5th | +0.00001194 | 48,433 |
| 99.9th | +0.00006558 | 9,687 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L11 | H16 | 97 | flkL | 326 | flkR | +0.043151 | 0.212535 |
| L29 | H18 | 285 | ss2 | 161 | ss1 | +0.033497 | 0.263488 |
| L16 | H2 | 156 | ss1 | 97 | flkL | +0.030735 | 0.432143 |
| L29 | H18 | 287 | ss2 | 160 | ss1 | +0.028962 | 0.240999 |
| L12 | H13 | 97 | flkL | 97 | flkL | +0.027978 | 0.284455 |
| L32 | H18 | 288 | ss2 | 157 | ss1 | +0.027618 | 0.145106 |
| L32 | H18 | 288 | ss2 | 155 | ss1 | +0.026613 | 0.162931 |
| L21 | H4 | 157 | ss1 | 156 | ss1 | +0.024897 | 0.457022 |
| L12 | H1 | 326 | flkR | 97 | flkL | +0.024769 | 0.594750 |
| L13 | H16 | 156 | ss1 | 97 | flkL | +0.024043 | 0.120684 |
| L10 | H19 | 97 | flkL | 95 | flkL | +0.023447 | 0.128159 |
| L13 | H7 | 155 | ss1 | 97 | flkL | +0.022571 | 0.362974 |
| L26 | H16 | 160 | ss1 | 285 | ss2 | +0.019023 | 0.204664 |
| L14 | H1 | 288 | ss2 | 326 | flkR | +0.018755 | 0.086174 |
| L26 | H16 | 159 | ss1 | 285 | ss2 | +0.018719 | 0.280811 |
| L21 | H13 | 285 | ss2 | 286 | ss2 | +0.017414 | 0.242671 |
| L17 | H8 | 163 | other | 156 | ss1 | +0.017041 | 0.357382 |
| L32 | H13 | 288 | ss2 | 155 | ss1 | +0.016405 | 0.164643 |
| L12 | H19 | 160 | ss1 | 97 | flkL | +0.015858 | 0.291479 |
| L21 | H2 | 163 | other | 156 | ss1 | +0.014800 | 0.285775 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L13 | H7 | 288 | ss2 | 297 | flkR | -0.005301 | 0.148777 |
| L13 | H14 | 147 | flkL | 97 | flkL | -0.005347 | 0.117972 |
| L14 | H10 | 160 | ss1 | 326 | flkR | -0.005410 | 0.068481 |
| L13 | H16 | 288 | ss2 | 326 | flkR | -0.005496 | 0.023258 |
| L8 | H0 | 160 | ss1 | 361 | flkR | -0.005637 | 0.174049 |
| L16 | H2 | 159 | ss1 | 97 | flkL | -0.005854 | 0.233728 |
| L16 | H2 | 160 | ss1 | 156 | ss1 | -0.006093 | 0.142337 |
| L14 | H9 | 159 | ss1 | 326 | flkR | -0.006184 | 0.122682 |
| L8 | H0 | 163 | other | 363 | other | -0.006263 | 0.451642 |
| L14 | H9 | 298 | flkR | 97 | flkL | -0.006658 | 0.101107 |
| L7 | H13 | 287 | ss2 | 85 | flkL | -0.006687 | 0.216568 |
| L31 | H17 | 285 | ss2 | 162 | ss1 | -0.006784 | 0.088468 |
| L21 | H4 | 163 | other | 156 | ss1 | -0.007424 | 0.281733 |
| L13 | H7 | 151 | flkL | 97 | flkL | -0.008294 | 0.376897 |
| L14 | H0 | 154 | ss1 | 326 | flkR | -0.008575 | 0.154610 |
| L27 | H15 | 287 | ss2 | 156 | ss1 | -0.009874 | 0.265830 |
| L16 | H2 | -1 | other | 97 | flkL | -0.010796 | 0.394514 |
| L7 | H13 | 84 | flkL | 84 | flkL | -0.011971 | 0.476079 |
| L17 | H8 | 156 | ss1 | 156 | ss1 | -0.012484 | 0.172319 |
| L13 | H16 | -1 | other | 97 | flkL | -0.019654 | 0.361849 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0796 | 0.00% |
| 10 | 10 | 8 | 0.0815 | 0.35% |
| 20 | 20 | 17 | 0.0840 | 0.80% |
| 50 | 50 | 27 | 0.1004 | 3.79% |
| 100 | 100 | 40 | 0.1193 | 7.22% |
| 200 | 200 | 47 | 0.1642 | 15.37% |
| 500 | 500 | 53 | 0.2602 | 32.80% |
| 1000 | 1,000 | 55 | 0.3538 | 49.80% |
| 2000 | 2,000 | 55 | 0.4695 | 70.81% |
| 5000 | 5,000 | 55 | 0.5908 | 92.83% |
| 10000 | 10,000 | 55 | 0.6454 | 102.76% |
| 20000 | 20,000 | 55 | 0.6869 | 110.30% |
| 50000 | 50,000 | 55 | 0.7296 | 118.05% |

## Motif Analysis

### L7 H13 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:flkL  |  cells: 38  |  total attr: +0.0699

**Key mass** (top-1=17%, top-2=29%, top-3=39%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.0122 | 17.4% |
| 86 | flkL | +0.0082 | 11.7% |
| 83 | flkL | +0.0068 | 9.8% |
| 158 | ss1 | +0.0054 | 7.7% |
| 361 | flkR | +0.0039 | 5.6% |

**Query mass** (top-1=9%, top-2=17%, top-3=23%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.0062 | 8.8% |
| 84 | flkL | +0.0054 | 7.7% |
| 157 | ss1 | +0.0044 | 6.3% |
| 101 | flkL | +0.0037 | 5.4% |
| 100 | flkL | +0.0037 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 37%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 10 | 26.3% |
| +74 | 4 | 10.5% |
| -74 | 3 | 7.9% |
| +21 | 3 | 7.9% |
| -25 | 2 | 5.3% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 17 | 44.7% |
| ss2 | flkR | 6 | 15.8% |
| ss1 | flkL | 3 | 7.9% |
| flkR | flkR | 3 | 7.9% |
| flkR | ss2 | 2 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 85 | flkL | 85 | flkL | +0.0062 | 0.1099 |
| 84 | flkL | 158 | ss1 | +0.0054 | 0.1955 |
| 157 | ss1 | 83 | flkL | +0.0044 | 0.2170 |
| 101 | flkL | 101 | flkL | +0.0037 | 0.0557 |
| 100 | flkL | 100 | flkL | +0.0037 | 0.0695 |

### L10 H19 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 4  |  total attr: +0.0270

**Key mass** (top-1=87%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | flkL | +0.0234 | 86.8% |
| 100 | flkL | +0.0014 | 5.2% |
| 101 | flkL | +0.0013 | 4.7% |
| 96 | flkL | +0.0009 | 3.3% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0270 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 1 | 25.0% |
| -3 | 1 | 25.0% |
| -4 | 1 | 25.0% |
| +1 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | flkL | 95 | flkL | +0.0234 | 0.1282 |
| 97 | flkL | 100 | flkL | +0.0014 | 0.0114 |
| 97 | flkL | 101 | flkL | +0.0013 | 0.0137 |
| 97 | flkL | 96 | flkL | +0.0009 | 0.0182 |

### L11 H16 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.1008

**Key mass** (top-1=89%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 326 | flkR | +0.0896 | 88.8% |
| -1 | other | +0.0064 | 6.4% |
| 95 | flkL | +0.0048 | 4.8% |

**Query mass** (top-1=43%, top-2=55%, top-3=63%)  [DISTR(V97/D95/A288/N159/L155)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0432 | 42.8% |
| 95 | flkL | +0.0123 | 12.2% |
| 288 | ss2 | +0.0084 | 8.3% |
| 159 | ss1 | +0.0065 | 6.4% |
| 155 | ss1 | +0.0045 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -229 | 1 | 4.8% |
| -231 | 1 | 4.8% |
| -38 | 1 | 4.8% |
| -167 | 1 | 4.8% |
| +157 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 6 | 28.6% |
| flkL | flkR | 4 | 19.0% |
| ss2 | flkR | 4 | 19.0% |
| ss1 | other | 2 | 9.5% |
| ss1 | flkL | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | flkL | 326 | flkR | +0.0432 | 0.2125 |
| 95 | flkL | 326 | flkR | +0.0123 | 0.1536 |
| 288 | ss2 | 326 | flkR | +0.0084 | 0.0317 |
| 159 | ss1 | 326 | flkR | +0.0065 | 0.0554 |
| 156 | ss1 | -1 | other | +0.0041 | 0.0465 |

### L12 H19 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 45  |  total attr: +0.1528

**Key mass** (top-1=63%, top-2=90%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0966 | 63.2% |
| 95 | flkL | +0.0412 | 26.9% |
| -1 | other | +0.0150 | 9.8% |

**Query mass** (top-1=18%, top-2=32%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0273 | 17.9% |
| 147 | flkL | +0.0221 | 14.5% |
| 156 | ss1 | +0.0158 | 10.3% |
| 155 | ss1 | +0.0124 | 8.1% |
| 286 | ss2 | +0.0114 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +50 | 2 | 4.4% |
| +60 | 2 | 4.4% |
| +189 | 2 | 4.4% |
| +59 | 2 | 4.4% |
| +51 | 2 | 4.4% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 13 | 28.9% |
| ss1 | flkL | 12 | 26.7% |
| ss2 | flkL | 11 | 24.4% |
| flkL | other | 4 | 8.9% |
| ss2 | other | 2 | 4.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 97 | flkL | +0.0159 | 0.2915 |
| 147 | flkL | 97 | flkL | +0.0122 | 0.3053 |
| 160 | ss1 | 95 | flkL | +0.0114 | 0.2038 |
| 155 | ss1 | 97 | flkL | +0.0097 | 0.2041 |
| 147 | flkL | 95 | flkL | +0.0086 | 0.2121 |

### L13 H7 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 41  |  total attr: +0.0979

**Key mass** (top-1=75%, top-2=80%, top-3=83%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0738 | 75.5% |
| 126 | flkL | +0.0043 | 4.4% |
| 88 | flkL | +0.0027 | 2.7% |
| -1 | other | +0.0018 | 1.8% |
| 301 | flkR | +0.0017 | 1.7% |

**Query mass** (top-1=23%, top-2=34%, top-3=41%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 155 | ss1 | +0.0226 | 23.1% |
| 159 | ss1 | +0.0106 | 10.9% |
| 156 | ss1 | +0.0073 | 7.5% |
| 291 | ss2 | +0.0064 | 6.6% |
| 289 | ss2 | +0.0057 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +14 | 3 | 7.3% |
| +0 | 3 | 7.3% |
| +19 | 2 | 4.9% |
| +13 | 2 | 4.9% |
| +58 | 1 | 2.4% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 12 | 29.3% |
| ss2 | other | 8 | 19.5% |
| ss1 | flkL | 7 | 17.1% |
| ss2 | flkL | 4 | 9.8% |
| flkR | flkL | 3 | 7.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 155 | ss1 | 97 | flkL | +0.0226 | 0.3630 |
| 159 | ss1 | 97 | flkL | +0.0106 | 0.1711 |
| 289 | ss2 | 97 | flkL | +0.0057 | 0.2804 |
| 156 | ss1 | 97 | flkL | +0.0055 | 0.1459 |
| 287 | ss2 | 97 | flkL | +0.0048 | 0.0486 |

### L14 H9 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 38  |  total attr: +0.0553

**Key mass** (top-1=46%, top-2=74%, top-3=79%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0254 | 45.8% |
| 326 | flkR | +0.0156 | 28.1% |
| 156 | ss1 | +0.0029 | 5.2% |
| 282 | other | +0.0022 | 3.9% |
| -1 | other | +0.0020 | 3.6% |

**Query mass** (top-1=28%, top-2=38%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0156 | 28.1% |
| -1 | other | +0.0053 | 9.5% |
| 287 | ss2 | +0.0042 | 7.6% |
| 285 | ss2 | +0.0031 | 5.7% |
| 147 | flkL | +0.0030 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 5.3% |
| +2 | 2 | 5.3% |
| +191 | 1 | 2.6% |
| -39 | 1 | 2.6% |
| -98 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=18%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 18.4% |
| ss1 | flkR | 6 | 15.8% |
| ss2 | flkL | 5 | 13.2% |
| ss2 | other | 5 | 13.2% |
| ss2 | ss1 | 3 | 7.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 288 | ss2 | 97 | flkL | +0.0086 | 0.0214 |
| 287 | ss2 | 326 | flkR | +0.0035 | 0.0488 |
| -1 | other | 97 | flkL | +0.0034 | 0.3719 |
| 147 | flkL | 97 | flkL | +0.0030 | 0.0579 |
| 288 | ss2 | -1 | other | +0.0020 | 0.0047 |

### L14 H17 — Rank #24

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 26  |  total attr: +0.0494

**Key mass** (top-1=21%, top-2=36%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 283 | ss2 | +0.0105 | 21.2% |
| 285 | ss2 | +0.0074 | 14.9% |
| 288 | ss2 | +0.0069 | 14.1% |
| 296 | flkR | +0.0029 | 5.9% |
| 289 | ss2 | +0.0024 | 4.8% |

**Query mass** (top-1=65%, top-2=76%, top-3=83%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0319 | 64.5% |
| 97 | flkL | +0.0058 | 11.8% |
| 285 | ss2 | +0.0031 | 6.4% |
| 157 | ss1 | +0.0030 | 6.0% |
| 308 | flkR | +0.0012 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 11.5% |
| +2 | 3 | 11.5% |
| +3 | 2 | 7.7% |
| -2 | 2 | 7.7% |
| +6 | 2 | 7.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 11 | 42.3% |
| flkL | flkL | 6 | 23.1% |
| ss1 | ss1 | 3 | 11.5% |
| flkR | flkR | 2 | 7.7% |
| ss2 | flkR | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 288 | ss2 | 283 | ss2 | +0.0088 | 0.0477 |
| 288 | ss2 | 288 | ss2 | +0.0069 | 0.0301 |
| 288 | ss2 | 285 | ss2 | +0.0049 | 0.0277 |
| 288 | ss2 | 296 | flkR | +0.0029 | 0.0270 |
| 288 | ss2 | 289 | ss2 | +0.0024 | 0.0194 |

### L15 H1 — Rank #30

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 20  |  total attr: +0.0284

**Key mass** (top-1=60%, top-2=75%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0170 | 59.7% |
| 98 | flkL | +0.0042 | 14.8% |
| 97 | flkL | +0.0031 | 10.8% |
| 102 | flkL | +0.0015 | 5.4% |
| 99 | flkL | +0.0014 | 4.8% |

**Query mass** (top-1=20%, top-2=34%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0058 | 20.3% |
| 97 | flkL | +0.0040 | 14.0% |
| 155 | ss1 | +0.0037 | 13.0% |
| 160 | ss1 | +0.0030 | 10.6% |
| 147 | flkL | +0.0023 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 2 | 10.0% |
| +98 | 1 | 5.0% |
| +157 | 1 | 5.0% |
| +148 | 1 | 5.0% |
| +62 | 1 | 5.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 8 | 40.0% |
| flkL | other | 5 | 25.0% |
| ss1 | other | 4 | 20.0% |
| flkR | flkL | 1 | 5.0% |
| other | flkL | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | flkL | -1 | other | +0.0040 | 0.2109 |
| 156 | ss1 | -1 | other | +0.0036 | 0.2823 |
| 147 | flkL | -1 | other | +0.0023 | 0.1363 |
| 160 | ss1 | 98 | flkL | +0.0023 | 0.0509 |
| 326 | flkR | 97 | flkL | +0.0018 | 0.0392 |

### L15 H3 — Rank #16

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 14  |  total attr: +0.0360

**Key mass** (top-1=28%, top-2=46%, top-3=61%)  [DISTR(A288/R283/K160/A289)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0100 | 27.7% |
| 283 | ss2 | +0.0066 | 18.2% |
| 160 | ss1 | +0.0053 | 14.9% |
| 289 | ss2 | +0.0038 | 10.5% |
| 287 | ss2 | +0.0037 | 10.3% |

**Query mass** (top-1=73%, top-2=86%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0264 | 73.4% |
| 160 | ss1 | +0.0045 | 12.6% |
| 156 | ss1 | +0.0042 | 11.6% |
| 285 | ss2 | +0.0009 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 21.4% |
| -2 | 2 | 14.3% |
| +5 | 1 | 7.1% |
| -1 | 1 | 7.1% |
| +1 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 5 | 35.7% |
| ss1 | ss1 | 4 | 28.6% |
| ss2 | flkR | 3 | 21.4% |
| ss1 | flkR | 2 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 288 | ss2 | 288 | ss2 | +0.0100 | 0.0331 |
| 288 | ss2 | 283 | ss2 | +0.0066 | 0.0445 |
| 160 | ss1 | 160 | ss1 | +0.0045 | 0.1418 |
| 288 | ss2 | 289 | ss2 | +0.0038 | 0.0227 |
| 288 | ss2 | 287 | ss2 | +0.0028 | 0.0177 |

### L16 H1 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.0281

**Key mass** (top-1=66%, top-2=78%, top-3=84%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 326 | flkR | +0.0186 | 66.0% |
| 288 | ss2 | +0.0034 | 12.0% |
| 156 | ss1 | +0.0018 | 6.3% |
| 338 | flkR | +0.0014 | 5.1% |
| 147 | flkL | +0.0014 | 4.9% |

**Query mass** (top-1=19%, top-2=33%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0054 | 19.3% |
| 159 | ss1 | +0.0039 | 14.0% |
| 160 | ss1 | +0.0038 | 13.5% |
| 331 | flkR | +0.0030 | 10.7% |
| 285 | ss2 | +0.0023 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -166 | 1 | 5.9% |
| +0 | 1 | 5.9% |
| +5 | 1 | 5.9% |
| -41 | 1 | 5.9% |
| -18 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 5 | 29.4% |
| ss1 | flkR | 3 | 17.6% |
| ss2 | flkR | 3 | 17.6% |
| ss2 | ss2 | 2 | 11.8% |
| ss1 | flkL | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 326 | flkR | +0.0038 | 0.0387 |
| 288 | ss2 | 288 | ss2 | +0.0034 | 0.0202 |
| 331 | flkR | 326 | flkR | +0.0030 | 0.1711 |
| 285 | ss2 | 326 | flkR | +0.0023 | 0.0201 |
| 308 | flkR | 326 | flkR | +0.0020 | 0.1657 |

### L16 H2 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 60  |  total attr: +0.1477

**Key mass** (top-1=67%, top-2=84%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0991 | 67.1% |
| 156 | ss1 | +0.0251 | 17.0% |
| 155 | ss1 | +0.0165 | 11.1% |
| -1 | other | +0.0024 | 1.6% |
| 326 | flkR | +0.0017 | 1.1% |

**Query mass** (top-1=21%, top-2=32%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0307 | 20.8% |
| 288 | ss2 | +0.0160 | 10.8% |
| 160 | ss1 | +0.0108 | 7.3% |
| 286 | ss2 | +0.0086 | 5.8% |
| 287 | ss2 | +0.0083 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 3 | 5.0% |
| +0 | 3 | 5.0% |
| +132 | 2 | 3.3% |
| +133 | 2 | 3.3% |
| +130 | 2 | 3.3% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 15 | 25.0% |
| ss2 | ss1 | 9 | 15.0% |
| flkR | flkL | 9 | 15.0% |
| ss2 | flkL | 6 | 10.0% |
| ss1 | ss1 | 6 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss1 | 97 | flkL | +0.0307 | 0.4321 |
| 160 | ss1 | 97 | flkL | +0.0085 | 0.1360 |
| 288 | ss2 | 156 | ss1 | +0.0074 | 0.2257 |
| 111 | flkL | 97 | flkL | +0.0067 | 0.4909 |
| 288 | ss2 | 155 | ss1 | +0.0059 | 0.1371 |

### L16 H17 — Rank #11

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 19  |  total attr: +0.0479

**Key mass** (top-1=35%, top-2=53%, top-3=65%)  [DISTR(D95/V97/A288/V96)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | flkL | +0.0170 | 35.4% |
| 97 | flkL | +0.0085 | 17.7% |
| 288 | ss2 | +0.0056 | 11.7% |
| 96 | flkL | +0.0027 | 5.7% |
| 100 | flkL | +0.0027 | 5.7% |

**Query mass** (top-1=67%, top-2=81%, top-3=88%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0321 | 67.1% |
| 288 | ss2 | +0.0069 | 14.3% |
| 97 | flkL | +0.0029 | 6.1% |
| 157 | ss1 | +0.0017 | 3.6% |
| 159 | ss1 | +0.0015 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +60 | 2 | 10.5% |
| +62 | 2 | 10.5% |
| +61 | 1 | 5.3% |
| +59 | 1 | 5.3% |
| +0 | 1 | 5.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 11 | 57.9% |
| flkL | flkL | 2 | 10.5% |
| other | ss1 | 2 | 10.5% |
| ss2 | ss2 | 1 | 5.3% |
| ss1 | other | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss1 | 95 | flkL | +0.0140 | 0.0540 |
| 156 | ss1 | 97 | flkL | +0.0061 | 0.0685 |
| 288 | ss2 | 288 | ss2 | +0.0056 | 0.0932 |
| 97 | flkL | 95 | flkL | +0.0029 | 0.2069 |
| 156 | ss1 | 96 | flkL | +0.0027 | 0.0254 |

### L17 H1 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 31  |  total attr: +0.0673

**Key mass** (top-1=76%, top-2=82%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0511 | 75.9% |
| 288 | ss2 | +0.0041 | 6.2% |
| 326 | flkR | +0.0041 | 6.1% |
| 307 | flkR | +0.0030 | 4.4% |
| 97 | flkL | +0.0023 | 3.5% |

**Query mass** (top-1=21%, top-2=31%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 142 | flkL | +0.0142 | 21.1% |
| 148 | flkL | +0.0068 | 10.2% |
| 147 | flkL | +0.0059 | 8.7% |
| 146 | flkL | +0.0059 | 8.7% |
| 140 | flkL | +0.0049 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -14 | 2 | 6.5% |
| -19 | 2 | 6.5% |
| -7 | 2 | 6.5% |
| -8 | 1 | 3.2% |
| -9 | 1 | 3.2% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 13 | 41.9% |
| ss1 | flkR | 4 | 12.9% |
| ss2 | flkR | 3 | 9.7% |
| ss1 | ss1 | 3 | 9.7% |
| flkL | flkL | 3 | 9.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 142 | flkL | 156 | ss1 | +0.0142 | 0.6575 |
| 148 | flkL | 156 | ss1 | +0.0068 | 0.5127 |
| 147 | flkL | 156 | ss1 | +0.0059 | 0.5386 |
| 146 | flkL | 156 | ss1 | +0.0059 | 0.5618 |
| 140 | flkL | 156 | ss1 | +0.0049 | 0.6697 |

### L17 H7 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | ss1→flkL  |  cells: 12  |  total attr: +0.0289

**Key mass** (top-1=64%, top-2=77%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | flkL | +0.0186 | 64.4% |
| 149 | flkL | +0.0036 | 12.5% |
| 156 | ss1 | +0.0035 | 12.2% |
| 146 | flkL | +0.0024 | 8.5% |
| 150 | flkL | +0.0007 | 2.5% |

**Query mass** (top-1=32%, top-2=57%, top-3=70%)  [DISTR(K160/N159/Y157/F156)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0094 | 32.4% |
| 159 | ss1 | +0.0071 | 24.6% |
| 157 | ss1 | +0.0036 | 12.6% |
| 156 | ss1 | +0.0033 | 11.4% |
| 165 | other | +0.0020 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +10 | 5 | 41.7% |
| +11 | 3 | 25.0% |
| +9 | 2 | 16.7% |
| +13 | 1 | 8.3% |
| +12 | 1 | 8.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 10 | 83.3% |
| other | ss1 | 2 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 147 | flkL | +0.0061 | 0.1638 |
| 159 | ss1 | 147 | flkL | +0.0060 | 0.1637 |
| 157 | ss1 | 147 | flkL | +0.0028 | 0.1038 |
| 160 | ss1 | 149 | flkL | +0.0025 | 0.0645 |
| 165 | other | 156 | ss1 | +0.0020 | 0.1278 |

### L17 H8 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 14  |  total attr: +0.0542

**Key mass** (top-1=90%, top-2=93%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0485 | 89.5% |
| 147 | flkL | +0.0021 | 3.9% |
| 97 | flkL | +0.0018 | 3.3% |
| 301 | flkR | +0.0010 | 1.9% |
| 155 | ss1 | +0.0007 | 1.3% |

**Query mass** (top-1=31%, top-2=58%, top-3=69%)  [DISTR(W163/K160/L155/N159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | other | +0.0170 | 31.4% |
| 160 | ss1 | +0.0142 | 26.2% |
| 155 | ss1 | +0.0061 | 11.3% |
| 159 | ss1 | +0.0056 | 10.2% |
| 158 | ss1 | +0.0035 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 1 | 7.1% |
| +4 | 1 | 7.1% |
| -1 | 1 | 7.1% |
| +3 | 1 | 7.1% |
| +2 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 50.0% |
| other | ss1 | 3 | 21.4% |
| flkL | flkL | 2 | 14.3% |
| ss1 | flkL | 1 | 7.1% |
| ss2 | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 163 | other | 156 | ss1 | +0.0170 | 0.3574 |
| 160 | ss1 | 156 | ss1 | +0.0114 | 0.2482 |
| 155 | ss1 | 156 | ss1 | +0.0061 | 0.1611 |
| 159 | ss1 | 156 | ss1 | +0.0056 | 0.1979 |
| 158 | ss1 | 156 | ss1 | +0.0035 | 0.1566 |

### L19 H9 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0519

**Key mass** (top-1=69%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | flkL | +0.0359 | 69.1% |
| 156 | ss1 | +0.0121 | 23.4% |
| 326 | flkR | +0.0013 | 2.6% |
| 436 | other | +0.0010 | 1.9% |
| 155 | ss1 | +0.0009 | 1.7% |

**Query mass** (top-1=20%, top-2=38%, top-3=54%)  [DISTR(D285/G287/F156/N159/L155)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0105 | 20.2% |
| 287 | ss2 | +0.0092 | 17.7% |
| 156 | ss1 | +0.0084 | 16.2% |
| 159 | ss1 | +0.0057 | 11.1% |
| 155 | ss1 | +0.0038 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +61 | 2 | 10.0% |
| +59 | 1 | 5.0% |
| +188 | 1 | 5.0% |
| +131 | 1 | 5.0% |
| +62 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 7 | 35.0% |
| ss2 | flkL | 4 | 20.0% |
| ss2 | ss1 | 4 | 20.0% |
| ss2 | other | 1 | 5.0% |
| ss1 | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss1 | 97 | flkL | +0.0077 | 0.2539 |
| 285 | ss2 | 97 | flkL | +0.0066 | 0.1395 |
| 287 | ss2 | 156 | ss1 | +0.0060 | 0.1648 |
| 159 | ss1 | 97 | flkL | +0.0057 | 0.2294 |
| 285 | ss2 | 156 | ss1 | +0.0039 | 0.0662 |

### L20 H18 — Rank #29

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 15  |  total attr: +0.0188

**Key mass** (top-1=48%, top-2=70%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0090 | 47.7% |
| 326 | flkR | +0.0043 | 22.7% |
| 159 | ss1 | +0.0036 | 19.2% |
| 348 | flkR | +0.0010 | 5.3% |
| 160 | ss1 | +0.0009 | 4.9% |

**Query mass** (top-1=17%, top-2=28%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0032 | 16.9% |
| 115 | flkL | +0.0021 | 11.2% |
| 126 | flkL | +0.0021 | 11.0% |
| 131 | flkL | +0.0018 | 9.3% |
| 124 | flkL | +0.0013 | 6.9% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -41 | 2 | 13.3% |
| +0 | 1 | 6.7% |
| -30 | 1 | 6.7% |
| -25 | 1 | 6.7% |
| -32 | 1 | 6.7% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 7 | 46.7% |
| ss1 | ss1 | 3 | 20.0% |
| ss1 | flkR | 2 | 13.3% |
| ss2 | flkR | 2 | 13.3% |
| flkR | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss1 | 159 | ss1 | +0.0023 | 0.0872 |
| 115 | flkL | 156 | ss1 | +0.0021 | 0.4116 |
| 126 | flkL | 156 | ss1 | +0.0021 | 0.2355 |
| 131 | flkL | 156 | ss1 | +0.0018 | 0.1568 |
| 124 | flkL | 156 | ss1 | +0.0013 | 0.3198 |

### L21 H2 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 15  |  total attr: +0.0513

**Key mass** (top-1=80%, top-2=87%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0411 | 80.2% |
| 288 | ss2 | +0.0038 | 7.3% |
| 155 | ss1 | +0.0028 | 5.5% |
| 326 | flkR | +0.0023 | 4.5% |
| 151 | flkL | +0.0007 | 1.4% |

**Query mass** (top-1=30%, top-2=59%, top-3=66%)  [DISTR(K160/W163/A162/N159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0153 | 29.9% |
| 163 | other | +0.0148 | 28.9% |
| 162 | ss1 | +0.0036 | 6.9% |
| 159 | ss1 | +0.0032 | 6.2% |
| 157 | ss1 | +0.0032 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 13.3% |
| +6 | 2 | 13.3% |
| +5 | 2 | 13.3% |
| +7 | 1 | 6.7% |
| +3 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 46.7% |
| ss2 | ss2 | 3 | 20.0% |
| flkR | flkR | 2 | 13.3% |
| other | ss1 | 1 | 6.7% |
| flkR | ss2 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 163 | other | 156 | ss1 | +0.0148 | 0.2858 |
| 160 | ss1 | 156 | ss1 | +0.0125 | 0.2325 |
| 162 | ss1 | 156 | ss1 | +0.0036 | 0.3310 |
| 159 | ss1 | 156 | ss1 | +0.0032 | 0.2349 |
| 157 | ss1 | 156 | ss1 | +0.0032 | 0.1841 |

### L21 H4 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 11  |  total attr: +0.0508

**Key mass** (top-1=91%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0462 | 90.8% |
| 288 | ss2 | +0.0030 | 6.0% |
| 311 | flkR | +0.0009 | 1.7% |
| 159 | ss1 | +0.0007 | 1.5% |

**Query mass** (top-1=49%, top-2=62%, top-3=75%)  [DISTR(Y157/L155/K160)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | ss1 | +0.0249 | 49.0% |
| 155 | ss1 | +0.0066 | 13.0% |
| 160 | ss1 | +0.0065 | 12.7% |
| 159 | ss1 | +0.0036 | 7.0% |
| 286 | ss2 | +0.0030 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 1 | 9.1% |
| -1 | 1 | 9.1% |
| +4 | 1 | 9.1% |
| +3 | 1 | 9.1% |
| -2 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 63.6% |
| flkL | ss1 | 2 | 18.2% |
| ss2 | ss2 | 1 | 9.1% |
| ss2 | flkR | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 157 | ss1 | 156 | ss1 | +0.0249 | 0.4570 |
| 155 | ss1 | 156 | ss1 | +0.0066 | 0.3639 |
| 160 | ss1 | 156 | ss1 | +0.0065 | 0.1516 |
| 159 | ss1 | 156 | ss1 | +0.0036 | 0.1865 |
| 286 | ss2 | 288 | ss2 | +0.0030 | 0.0770 |

### L21 H13 — Rank #10

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 14  |  total attr: +0.0524

**Key mass** (top-1=36%, top-2=66%, top-3=77%)  [DISTR(F286/F156/D285)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 286 | ss2 | +0.0186 | 35.5% |
| 156 | ss1 | +0.0161 | 30.8% |
| 285 | ss2 | +0.0055 | 10.6% |
| 159 | ss1 | +0.0041 | 7.8% |
| 163 | other | +0.0034 | 6.4% |

**Query mass** (top-1=47%, top-2=68%, top-3=77%)  [DISTR(D285/F156/Y157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0244 | 46.6% |
| 156 | ss1 | +0.0113 | 21.5% |
| 157 | ss1 | +0.0048 | 9.2% |
| 155 | ss1 | +0.0034 | 6.5% |
| 163 | other | +0.0034 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 64%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 35.7% |
| -1 | 4 | 28.6% |
| +1 | 3 | 21.4% |
| -3 | 1 | 7.1% |
| -2 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 50.0% |
| ss2 | ss2 | 4 | 28.6% |
| flkL | flkL | 2 | 14.3% |
| other | other | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 285 | ss2 | 286 | ss2 | +0.0174 | 0.2427 |
| 156 | ss1 | 156 | ss1 | +0.0079 | 0.1517 |
| 285 | ss2 | 285 | ss2 | +0.0055 | 0.0714 |
| 157 | ss1 | 156 | ss1 | +0.0048 | 0.1575 |
| 155 | ss1 | 156 | ss1 | +0.0034 | 0.0578 |

### L23 H18 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss1  |  cells: 20  |  total attr: +0.0331

**Key mass** (top-1=55%, top-2=68%, top-3=80%)  [DISTR(F156/N159/Y158)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0182 | 55.2% |
| 159 | ss1 | +0.0042 | 12.8% |
| 158 | ss1 | +0.0039 | 11.8% |
| 288 | ss2 | +0.0026 | 7.8% |
| 157 | ss1 | +0.0011 | 3.3% |

**Query mass** (top-1=34%, top-2=45%, top-3=52%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | other | +0.0112 | 33.9% |
| 161 | ss1 | +0.0035 | 10.6% |
| 155 | ss1 | +0.0026 | 7.8% |
| 154 | ss1 | +0.0025 | 7.5% |
| 159 | ss1 | +0.0022 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 3 | 15.0% |
| +4 | 3 | 15.0% |
| +6 | 3 | 15.0% |
| +3 | 2 | 10.0% |
| +8 | 2 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 40.0% |
| other | ss1 | 5 | 25.0% |
| ss2 | ss2 | 2 | 10.0% |
| flkL | ss1 | 2 | 10.0% |
| flkL | flkL | 2 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 163 | other | 156 | ss1 | +0.0071 | 0.2033 |
| 161 | ss1 | 156 | ss1 | +0.0035 | 0.2926 |
| 154 | ss1 | 159 | ss1 | +0.0025 | 0.2408 |
| 163 | other | 158 | ss1 | +0.0023 | 0.1115 |
| 155 | ss1 | 156 | ss1 | +0.0019 | 0.0737 |

### L26 H11 — Rank #20

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 23  |  total attr: +0.0354

**Key mass** (top-1=22%, top-2=39%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | ss2 | +0.0078 | 22.0% |
| 288 | ss2 | +0.0062 | 17.4% |
| 156 | ss1 | +0.0041 | 11.7% |
| 131 | flkL | +0.0033 | 9.4% |
| 159 | ss1 | +0.0030 | 8.4% |

**Query mass** (top-1=29%, top-2=38%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0102 | 28.8% |
| 152 | ss1 | +0.0033 | 9.3% |
| 157 | ss1 | +0.0030 | 8.5% |
| 283 | ss2 | +0.0026 | 7.4% |
| 286 | ss2 | +0.0022 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 74%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 10 | 43.5% |
| -4 | 7 | 30.4% |
| -3 | 2 | 8.7% |
| +1 | 1 | 4.3% |
| -12 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 39.1% |
| ss2 | ss2 | 8 | 34.8% |
| flkL | flkL | 5 | 21.7% |
| flkR | flkR | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 285 | ss2 | 289 | ss2 | +0.0070 | 0.0621 |
| 152 | ss1 | 156 | ss1 | +0.0033 | 0.2721 |
| 283 | ss2 | 288 | ss2 | +0.0026 | 0.1214 |
| 285 | ss2 | 288 | ss2 | +0.0025 | 0.0264 |
| 286 | ss2 | 291 | ss2 | +0.0022 | 0.0638 |

### L26 H16 — Rank #3

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 21  |  total attr: +0.0810

**Key mass** (top-1=56%, top-2=72%, top-3=78%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0454 | 56.1% |
| 160 | ss1 | +0.0131 | 16.2% |
| 159 | ss1 | +0.0048 | 6.0% |
| 287 | ss2 | +0.0034 | 4.2% |
| 288 | ss2 | +0.0028 | 3.5% |

**Query mass** (top-1=31%, top-2=55%, top-3=78%)  [DISTR(K160/D285/N159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0253 | 31.3% |
| 285 | ss2 | +0.0192 | 23.7% |
| 159 | ss1 | +0.0187 | 23.1% |
| 161 | ss1 | +0.0084 | 10.4% |
| 287 | ss2 | +0.0045 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -125 | 1 | 4.8% |
| -126 | 1 | 4.8% |
| +125 | 1 | 4.8% |
| -124 | 1 | 4.8% |
| +126 | 1 | 4.8% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 42.9% |
| ss2 | ss1 | 6 | 28.6% |
| ss1 | flkL | 4 | 19.0% |
| ss1 | flkR | 1 | 4.8% |
| ss2 | flkR | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 285 | ss2 | +0.0190 | 0.2047 |
| 159 | ss1 | 285 | ss2 | +0.0187 | 0.2808 |
| 285 | ss2 | 160 | ss1 | +0.0116 | 0.0915 |
| 161 | ss1 | 285 | ss2 | +0.0077 | 0.2116 |
| 285 | ss2 | 159 | ss1 | +0.0048 | 0.0349 |

### L27 H9 — Rank #26

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | ss1→flkL  |  cells: 6  |  total attr: +0.0077

**Key mass** (top-1=36%, top-2=60%, top-3=80%)  [DISTR(Y138/P148/G142)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | flkL | +0.0027 | 35.6% |
| 148 | flkL | +0.0019 | 24.0% |
| 142 | flkL | +0.0016 | 20.1% |
| 146 | flkL | +0.0008 | 11.0% |
| 149 | flkL | +0.0007 | 9.2% |

**Query mass** (top-1=44%, top-2=77%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0034 | 43.8% |
| 157 | ss1 | +0.0026 | 33.2% |
| 159 | ss1 | +0.0009 | 12.0% |
| 155 | ss1 | +0.0008 | 11.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +9 | 2 | 33.3% |
| +22 | 1 | 16.7% |
| +18 | 1 | 16.7% |
| +21 | 1 | 16.7% |
| +8 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 157 | ss1 | 148 | flkL | +0.0019 | 0.2001 |
| 160 | ss1 | 138 | flkL | +0.0018 | 0.0637 |
| 160 | ss1 | 142 | flkL | +0.0016 | 0.0573 |
| 159 | ss1 | 138 | flkL | +0.0009 | 0.0417 |
| 155 | ss1 | 146 | flkL | +0.0008 | 0.0909 |

### L27 H15 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0711

**Key mass** (top-1=21%, top-2=41%, top-3=56%)  [DISTR(F156/D285/G287/K160/V97)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0147 | 20.7% |
| 285 | ss2 | +0.0146 | 20.6% |
| 287 | ss2 | +0.0104 | 14.6% |
| 160 | ss1 | +0.0091 | 12.8% |
| 97 | flkL | +0.0057 | 8.0% |

**Query mass** (top-1=21%, top-2=42%, top-3=61%)  [DISTR(K160/A289/D285/Y157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0149 | 20.9% |
| 289 | ss2 | +0.0147 | 20.7% |
| 285 | ss2 | +0.0135 | 19.1% |
| 157 | ss1 | +0.0090 | 12.6% |
| 158 | ss1 | +0.0065 | 9.2% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 1 | 5.0% |
| -125 | 1 | 5.0% |
| +125 | 1 | 5.0% |
| -129 | 1 | 5.0% |
| +60 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 35.0% |
| ss2 | ss1 | 6 | 30.0% |
| ss2 | flkR | 4 | 20.0% |
| ss1 | flkL | 2 | 10.0% |
| ss2 | ss2 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | ss2 | 156 | ss1 | +0.0147 | 0.2287 |
| 160 | ss1 | 285 | ss2 | +0.0126 | 0.0801 |
| 285 | ss2 | 160 | ss1 | +0.0091 | 0.0458 |
| 158 | ss1 | 287 | ss2 | +0.0065 | 0.2704 |
| 157 | ss1 | 97 | flkL | +0.0057 | 0.2916 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 34  |  total attr: +0.1361

**Key mass** (top-1=26%, top-2=49%, top-3=59%)  [DISTR(A161/K160/G287/T114/A288)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 161 | ss1 | +0.0349 | 25.7% |
| 160 | ss1 | +0.0312 | 22.9% |
| 287 | ss2 | +0.0138 | 10.1% |
| 114 | flkL | +0.0104 | 7.6% |
| 288 | ss2 | +0.0097 | 7.1% |

**Query mass** (top-1=26%, top-2=51%, top-3=70%)  [DISTR(D285/G287/K160)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0357 | 26.2% |
| 287 | ss2 | +0.0330 | 24.3% |
| 160 | ss1 | +0.0266 | 19.6% |
| 157 | ss1 | +0.0082 | 6.1% |
| 288 | ss2 | +0.0060 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +127 | 2 | 5.9% |
| -127 | 2 | 5.9% |
| +46 | 2 | 5.9% |
| +124 | 1 | 2.9% |
| -131 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 10 | 29.4% |
| ss2 | ss1 | 9 | 26.5% |
| ss1 | other | 5 | 14.7% |
| ss1 | flkL | 3 | 8.8% |
| ss2 | flkL | 2 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 285 | ss2 | 161 | ss1 | +0.0335 | 0.2635 |
| 287 | ss2 | 160 | ss1 | +0.0290 | 0.2410 |
| 160 | ss1 | 287 | ss2 | +0.0138 | 0.0621 |
| 160 | ss1 | 114 | flkL | +0.0104 | 0.0841 |
| 157 | ss1 | 288 | ss2 | +0.0073 | 0.0859 |

### L30 H1 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 10  |  total attr: +0.0257

**Key mass** (top-1=64%, top-2=79%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0163 | 63.6% |
| 160 | ss1 | +0.0039 | 15.0% |
| 289 | ss2 | +0.0024 | 9.2% |
| 155 | ss1 | +0.0013 | 5.1% |
| 159 | ss1 | +0.0011 | 4.2% |

**Query mass** (top-1=41%, top-2=58%, top-3=72%)  [DISTR(K160/D285/N159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0106 | 41.2% |
| 285 | ss2 | +0.0043 | 16.8% |
| 159 | ss1 | +0.0035 | 13.5% |
| 156 | ss1 | +0.0024 | 9.2% |
| 287 | ss2 | +0.0017 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -125 | 1 | 10.0% |
| -126 | 1 | 10.0% |
| -133 | 1 | 10.0% |
| +125 | 1 | 10.0% |
| +127 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 50.0% |
| ss2 | ss1 | 4 | 40.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 285 | ss2 | +0.0106 | 0.0737 |
| 159 | ss1 | 285 | ss2 | +0.0035 | 0.0436 |
| 156 | ss1 | 289 | ss2 | +0.0024 | 0.0458 |
| 285 | ss2 | 160 | ss1 | +0.0022 | 0.0174 |
| 287 | ss2 | 160 | ss1 | +0.0017 | 0.0166 |

### L31 H17 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 25  |  total attr: +0.0435

**Key mass** (top-1=53%, top-2=61%, top-3=69%)  [DISTR(?-1/L314/?436/A288)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0231 | 53.0% |
| 314 | flkR | +0.0036 | 8.3% |
| 436 | other | +0.0033 | 7.7% |
| 288 | ss2 | +0.0024 | 5.4% |
| 157 | ss1 | +0.0018 | 4.2% |

**Query mass** (top-1=23%, top-2=44%, top-3=57%)  [DISTR(D285/K160/G287/N159/Y157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0102 | 23.5% |
| 160 | ss1 | +0.0088 | 20.2% |
| 287 | ss2 | +0.0056 | 12.9% |
| 159 | ss1 | +0.0051 | 11.8% |
| 157 | ss1 | +0.0039 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +161 | 2 | 8.0% |
| +286 | 1 | 4.0% |
| +288 | 1 | 4.0% |
| -155 | 1 | 4.0% |
| +158 | 1 | 4.0% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 9 | 36.0% |
| ss1 | flkR | 4 | 16.0% |
| ss2 | other | 3 | 12.0% |
| ss1 | ss2 | 3 | 12.0% |
| ss2 | ss1 | 2 | 8.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 285 | ss2 | -1 | other | +0.0053 | 0.0542 |
| 160 | ss1 | -1 | other | +0.0048 | 0.1077 |
| 287 | ss2 | -1 | other | +0.0043 | 0.1052 |
| 159 | ss1 | 314 | flkR | +0.0036 | 0.0602 |
| 157 | ss1 | -1 | other | +0.0026 | 0.1822 |

### L32 H13 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 16  |  total attr: +0.0998

**Key mass** (top-1=18%, top-2=35%, top-3=51%)  [DISTR(D285/L155/A288/G287/A161)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0184 | 18.5% |
| 155 | ss1 | +0.0164 | 16.4% |
| 288 | ss2 | +0.0157 | 15.7% |
| 287 | ss2 | +0.0134 | 13.5% |
| 161 | ss1 | +0.0102 | 10.3% |

**Query mass** (top-1=23%, top-2=38%, top-3=49%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0231 | 23.1% |
| 160 | ss1 | +0.0146 | 14.6% |
| 161 | ss1 | +0.0115 | 11.5% |
| 155 | ss1 | +0.0103 | 10.3% |
| 287 | ss2 | +0.0087 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 2 | 12.5% |
| -133 | 2 | 12.5% |
| -127 | 1 | 6.2% |
| -124 | 1 | 6.2% |
| +127 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 56.2% |
| ss2 | ss1 | 7 | 43.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 288 | ss2 | 155 | ss1 | +0.0164 | 0.1646 |
| 160 | ss1 | 287 | ss2 | +0.0134 | 0.0857 |
| 155 | ss1 | 288 | ss2 | +0.0103 | 0.1035 |
| 161 | ss1 | 285 | ss2 | +0.0100 | 0.1899 |
| 287 | ss2 | 160 | ss1 | +0.0087 | 0.0556 |

### L32 H18 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 18  |  total attr: +0.1232

**Key mass** (top-1=22%, top-2=44%, top-3=60%)  [DISTR(Y157/L155/A288/K160)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | ss1 | +0.0276 | 22.4% |
| 155 | ss1 | +0.0266 | 21.6% |
| 288 | ss2 | +0.0195 | 15.8% |
| 160 | ss1 | +0.0164 | 13.4% |
| 285 | ss2 | +0.0091 | 7.4% |

**Query mass** (top-1=44%, top-2=62%, top-3=72%)  [DISTR(A288/D285/Y157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0542 | 44.0% |
| 285 | ss2 | +0.0227 | 18.4% |
| 157 | ss1 | +0.0124 | 10.0% |
| 155 | ss1 | +0.0082 | 6.6% |
| 156 | ss1 | +0.0070 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 2 | 11.1% |
| -131 | 2 | 11.1% |
| -133 | 2 | 11.1% |
| +131 | 1 | 5.6% |
| +125 | 1 | 5.6% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 11 | 61.1% |
| ss2 | ss1 | 7 | 38.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 288 | ss2 | 157 | ss1 | +0.0276 | 0.1451 |
| 288 | ss2 | 155 | ss1 | +0.0266 | 0.1629 |
| 285 | ss2 | 160 | ss1 | +0.0142 | 0.0448 |
| 157 | ss1 | 288 | ss2 | +0.0113 | 0.0593 |
| 155 | ss1 | 288 | ss2 | +0.0082 | 0.0500 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #18 | L7 | H13 | 38 | +0.0699 | DISTRIBUTED |  | DISTRIBUTED |  |  | INTRA:flkL |
| #21 | L10 | H19 | 4 | +0.0270 | SINGLE-ANCHOR | D95 | SINGLE-ANCHOR | V97 |  | INTRA:flkL |
| #4 | L11 | H16 | 21 | +0.1008 | SINGLE-ANCHOR | I326 | DISTRIBUTED | V97/D95/A288/N159/L155 |  |  |
| #5 | L12 | H19 | 45 | +0.1528 | SINGLE-ANCHOR | V97 | DISTRIBUTED |  |  |  |
| #9 | L13 | H7 | 41 | +0.0979 | SINGLE-ANCHOR | V97 | DISTRIBUTED |  |  |  |
| #19 | L14 | H9 | 38 | +0.0553 | DUAL-ANCHOR | V97/I326 | DISTRIBUTED |  |  |  |
| #24 | L14 | H17 | 26 | +0.0494 | DISTRIBUTED |  | SINGLE-ANCHOR | A288 |  | INTRA:ss2 |
| #30 | L15 | H1 | 20 | +0.0284 | DUAL-ANCHOR | ?-1/L98 | DISTRIBUTED |  |  | ss1→flkL |
| #16 | L15 | H3 | 14 | +0.0360 | DISTRIBUTED | A288/R283/K160/A289 | SINGLE-ANCHOR | A288 |  |  |
| #22 | L16 | H1 | 17 | +0.0281 | SINGLE-ANCHOR | I326 | DISTRIBUTED |  |  |  |
| #14 | L16 | H2 | 60 | +0.1477 | SINGLE-ANCHOR | V97 | DISTRIBUTED |  |  |  |
| #11 | L16 | H17 | 19 | +0.0479 | DISTRIBUTED | D95/V97/A288/V96 | SINGLE-ANCHOR | F156 |  | ss1→flkL |
| #25 | L17 | H1 | 31 | +0.0673 | SINGLE-ANCHOR | F156 | DISTRIBUTED |  |  | flkL→ss1 |
| #23 | L17 | H7 | 12 | +0.0289 | SINGLE-ANCHOR | V147 | DISTRIBUTED | K160/N159/Y157/F156 | POSITIONAL | ss1→flkL |
| #28 | L17 | H8 | 14 | +0.0542 | SINGLE-ANCHOR | F156 | DISTRIBUTED | W163/K160/L155/N159 |  | INTRA:ss1 |
| #27 | L19 | H9 | 20 | +0.0519 | SINGLE-ANCHOR | V97 | DISTRIBUTED | D285/G287/F156/N159/L155 |  |  |
| #29 | L20 | H18 | 15 | +0.0188 | DUAL-ANCHOR | F156/I326 | DISTRIBUTED |  |  | flkL→ss1 |
| #12 | L21 | H2 | 15 | +0.0513 | SINGLE-ANCHOR | F156 | DISTRIBUTED | K160/W163/A162/N159 |  | INTRA:ss1 |
| #17 | L21 | H4 | 11 | +0.0508 | SINGLE-ANCHOR | F156 | DISTRIBUTED | Y157/L155/K160 |  | INTRA:ss1 |
| #10 | L21 | H13 | 14 | +0.0524 | DISTRIBUTED | F286/F156/D285 | DISTRIBUTED | D285/F156/Y157 | POSITIONAL | INTRA:ss1 |
| #15 | L23 | H18 | 20 | +0.0331 | DISTRIBUTED | F156/N159/Y158 | DISTRIBUTED |  |  | INTRA:ss1 |
| #20 | L26 | H11 | 23 | +0.0354 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL |  |
| #3 | L26 | H16 | 21 | +0.0810 | DUAL-ANCHOR | D285/K160 | DISTRIBUTED | K160/D285/N159 |  | CROSS:ss1→ss2 |
| #26 | L27 | H9 | 6 | +0.0077 | DISTRIBUTED | Y138/P148/G142 | DUAL-ANCHOR | K160/Y157 |  | ss1→flkL |
| #7 | L27 | H15 | 20 | +0.0711 | DISTRIBUTED | F156/D285/G287/K160/V97 | DISTRIBUTED | K160/A289/D285/Y157 |  |  |
| #6 | L29 | H18 | 34 | +0.1361 | DISTRIBUTED | A161/K160/G287/T114/A288 | DISTRIBUTED | D285/G287/K160 |  |  |
| #8 | L30 | H1 | 10 | +0.0257 | SINGLE-ANCHOR | D285 | DISTRIBUTED | K160/D285/N159 |  | CROSS:ss1→ss2 |
| #13 | L31 | H17 | 25 | +0.0435 | DISTRIBUTED | ?-1/L314/?436/A288 | DISTRIBUTED | D285/K160/G287/N159/Y157 |  |  |
| #2 | L32 | H13 | 16 | +0.0998 | DISTRIBUTED | D285/L155/A288/G287/A161 | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #1 | L32 | H18 | 18 | +0.1232 | DISTRIBUTED | Y157/L155/A288/K160 | DISTRIBUTED | A288/D285/Y157 |  | CROSS:ss1→ss2 |
