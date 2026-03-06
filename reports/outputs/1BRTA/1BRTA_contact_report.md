# Contact Pattern Analysis: 1BRTA

Generated: 2026-03-03 05:01:14   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1BRTA |
| Contact pair | (119, 221) |
| ss1 | [114, 125) |
| ss2 | [216, 227) |
| Clean flank | 32 |
| Corrupt flank | 31 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.7367 |
| Corrupt metric | 0.0152 |
| Gap | 0.7215 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 75.43% |
| positive IE | 90 | 77.90% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L22 | H14 | +0.3099 |
| 2 | L0 | H19 | +0.2460 |
| 3 | L11 | H14 | +0.2371 |
| 4 | L5 | H19 | +0.2214 |
| 5 | L26 | H16 | +0.2210 |
| 6 | L9 | H7 | +0.2006 |
| 7 | L32 | H18 | +0.1922 |
| 8 | L30 | H1 | +0.0814 |
| 9 | L17 | H10 | +0.0749 |
| 10 | L12 | H19 | +0.0660 |
| 11 | L6 | H12 | +0.0628 |
| 12 | L32 | H13 | +0.0583 |
| 13 | L27 | H15 | +0.0568 |
| 14 | L7 | H4 | +0.0472 |
| 15 | L10 | H9 | +0.0404 |
| 16 | L12 | H2 | +0.0387 |
| 17 | L14 | H0 | +0.0372 |
| 18 | L7 | H0 | +0.0365 |
| 19 | L13 | H17 | +0.0355 |
| 20 | L10 | H0 | +0.0342 |
| 21 | L18 | H1 | +0.0340 |
| 22 | L17 | H18 | +0.0325 |
| 23 | L7 | H16 | +0.0321 |
| 24 | L19 | H0 | +0.0315 |
| 25 | L13 | H9 | +0.0302 |
| 26 | L13 | H2 | +0.0299 |
| 27 | L14 | H13 | +0.0294 |
| 28 | L18 | H8 | +0.0275 |
| 29 | L16 | H18 | +0.0235 |
| 30 | L14 | H14 | +0.0230 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | 0.01% |
| 3 | 0.03% |
| 4 | 0.05% |
| 5 | 0.10% |
| 6 | 0.17% |
| 7 | 0.21% |
| 8 | 0.26% |
| 9 | 0.42% |
| 10 | 0.42% |
| 20 | 1.58% |
| 80 | 61.97% |
| 450 | 132.19% |

## Cell Attribution Analysis

Total cells: 6,498,221

- Positive: 3,274,596
- Negative: 3,219,209

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000029 | 649,824 |
| 95th | +0.00000092 | 324,912 |
| 99th | +0.00000745 | 64,983 |
| 99.5th | +0.00001644 | 32,492 |
| 99.9th | +0.00009390 | 6,499 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H19 | 118 | ss1 | 95 | flkL | +0.121692 | 0.087473 |
| L9 | H7 | 93 | flkL | 220 | ss2 | +0.097052 | 0.139514 |
| L11 | H14 | 118 | ss1 | 93 | flkL | +0.089000 | 0.381058 |
| L5 | H19 | 93 | flkL | 95 | flkL | +0.066994 | 0.111529 |
| L7 | H0 | 93 | flkL | 118 | ss1 | +0.047107 | 0.056542 |
| L26 | H16 | 118 | ss1 | 219 | ss2 | +0.041894 | 0.699235 |
| L7 | H16 | 220 | ss2 | 248 | flkR | +0.038167 | 0.101795 |
| L22 | H14 | 222 | ss2 | 121 | ss1 | +0.035146 | 0.556286 |
| L22 | H14 | 221 | ss2 | 120 | ss1 | +0.034923 | 0.700787 |
| L22 | H14 | 219 | ss2 | 120 | ss1 | +0.034224 | 0.505152 |
| L11 | H14 | 107 | flkL | 93 | flkL | +0.034211 | 0.387708 |
| L12 | H19 | 118 | ss1 | 93 | flkL | +0.031632 | 0.322932 |
| L6 | H12 | 93 | flkL | 82 | flkL | +0.029860 | 0.165051 |
| L26 | H16 | 120 | ss1 | 221 | ss2 | +0.029748 | 0.564175 |
| L7 | H4 | 118 | ss1 | 220 | ss2 | +0.029230 | 0.038248 |
| L16 | H0 | 120 | ss1 | 118 | ss1 | +0.028551 | 0.379670 |
| L6 | H3 | 93 | flkL | 256 | flkR | +0.028044 | 0.061727 |
| L22 | H14 | 223 | ss2 | 122 | ss1 | +0.027596 | 0.538135 |
| L13 | H2 | 120 | ss1 | 118 | ss1 | +0.026646 | 0.478948 |
| L17 | H10 | 122 | ss1 | 118 | ss1 | +0.024646 | 0.647010 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H3 | 93 | flkL | 223 | ss2 | -0.005726 | 0.057689 |
| L11 | H10 | 103 | flkL | 82 | flkL | -0.005851 | 0.168127 |
| L17 | H18 | 120 | ss1 | 93 | flkL | -0.005917 | 0.290311 |
| L13 | H2 | 124 | ss1 | 118 | ss1 | -0.006210 | 0.403315 |
| L11 | H14 | 111 | flkL | 93 | flkL | -0.006279 | 0.302941 |
| L13 | H2 | 125 | other | 118 | ss1 | -0.006406 | 0.211065 |
| L11 | H14 | 124 | ss1 | 93 | flkL | -0.006659 | 0.231242 |
| L4 | H16 | 94 | flkL | 82 | flkL | -0.006912 | 0.170762 |
| L19 | H0 | 121 | ss1 | 119 | ss1 | -0.007411 | 0.474857 |
| L12 | H19 | 93 | flkL | 93 | flkL | -0.008533 | 0.205745 |
| L22 | H14 | 117 | ss1 | 92 | flkL | -0.008761 | 0.694537 |
| L15 | H7 | 118 | ss1 | 248 | flkR | -0.009108 | 0.063984 |
| L7 | H13 | 90 | flkL | 90 | flkL | -0.009677 | 0.061223 |
| L17 | H13 | 120 | ss1 | 99 | flkL | -0.009929 | 0.168981 |
| L0 | H19 | 92 | flkL | 82 | flkL | -0.010625 | 0.054387 |
| L11 | H14 | 118 | ss1 | 92 | flkL | -0.010929 | 0.087540 |
| L7 | H13 | 105 | flkL | 255 | flkR | -0.011264 | 0.111347 |
| L8 | H0 | 84 | flkL | 84 | flkL | -0.011370 | 0.181066 |
| L7 | H13 | 90 | flkL | 115 | ss1 | -0.012834 | 0.063577 |
| L0 | H19 | 118 | ss1 | 82 | flkL | -0.014465 | 0.041537 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0152 | 0.00% |
| 10 | 10 | 7 | 0.0154 | 0.02% |
| 20 | 20 | 14 | 0.0156 | 0.05% |
| 50 | 50 | 29 | 0.0172 | 0.28% |
| 100 | 100 | 49 | 0.0213 | 0.83% |
| 200 | 200 | 69 | 0.0324 | 2.39% |
| 500 | 500 | 85 | 0.1751 | 22.16% |
| 1000 | 1,000 | 90 | 0.3769 | 50.13% |
| 2000 | 2,000 | 90 | 0.5662 | 76.37% |
| 5000 | 5,000 | 90 | 0.7092 | 96.19% |
| 10000 | 10,000 | 90 | 0.7815 | 106.20% |
| 20000 | 20,000 | 90 | 0.8316 | 113.15% |
| 50000 | 50,000 | 90 | 0.9373 | 127.80% |

## Motif Analysis

### L0 H19 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 49  |  total attr: +0.0682

**Key mass** (top-1=23%, top-2=34%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | flkL | +0.0157 | 22.9% |
| 258 | flkR | +0.0073 | 10.7% |
| 97 | flkL | +0.0043 | 6.4% |
| 94 | flkL | +0.0042 | 6.2% |
| 92 | flkL | +0.0040 | 5.9% |

**Query mass** (top-1=37%, top-2=54%, top-3=67%)  [DISTR(V82/L258/V118/V92)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | flkL | +0.0254 | 37.3% |
| 258 | flkR | +0.0116 | 17.0% |
| 118 | ss1 | +0.0090 | 13.1% |
| 92 | flkL | +0.0062 | 9.1% |
| 107 | flkL | +0.0058 | 8.5% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 10.2% |
| -36 | 2 | 4.1% |
| -5 | 2 | 4.1% |
| +15 | 2 | 4.1% |
| +25 | 1 | 2.0% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 18 | 36.7% |
| flkR | flkR | 7 | 14.3% |
| ss1 | flkL | 7 | 14.3% |
| flkL | flkR | 4 | 8.2% |
| flkR | ss2 | 3 | 6.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 82 | flkL | 82 | flkL | +0.0065 | 0.2027 |
| 107 | flkL | 82 | flkL | +0.0058 | 0.0441 |
| 118 | ss1 | 118 | ss1 | +0.0027 | 0.0078 |
| 121 | ss1 | 258 | flkR | +0.0026 | 0.0089 |
| 82 | flkL | 97 | flkL | +0.0025 | 0.0758 |

### L5 H19 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 4  |  total attr: +0.1983

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | flkL | +0.1983 | 100.0% |

**Query mass** (top-1=61%, top-2=95%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.1217 | 61.4% |
| 93 | flkL | +0.0670 | 33.8% |
| 99 | flkL | +0.0083 | 4.2% |
| 120 | ss1 | +0.0013 | 0.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +23 | 1 | 25.0% |
| -2 | 1 | 25.0% |
| +4 | 1 | 25.0% |
| +25 | 1 | 25.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 50.0% |
| flkL | flkL | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 95 | flkL | +0.1217 | 0.0875 |
| 93 | flkL | 95 | flkL | +0.0670 | 0.1115 |
| 99 | flkL | 95 | flkL | +0.0083 | 0.0933 |
| 120 | ss1 | 95 | flkL | +0.0013 | 0.0428 |

### L6 H12 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 12  |  total attr: +0.0475

**Key mass** (top-1=68%, top-2=77%, top-3=83%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | flkL | +0.0324 | 68.3% |
| 80 | other | +0.0041 | 8.6% |
| 87 | flkL | +0.0030 | 6.4% |
| 107 | flkL | +0.0021 | 4.4% |
| 84 | flkL | +0.0012 | 2.4% |

**Query mass** (top-1=90%, top-2=96%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0428 | 90.2% |
| 94 | flkL | +0.0026 | 5.4% |
| 118 | ss1 | +0.0021 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +11 | 2 | 16.7% |
| +12 | 2 | 16.7% |
| +13 | 1 | 8.3% |
| +6 | 1 | 8.3% |
| +9 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 6 | 50.0% |
| flkL | other | 5 | 41.7% |
| ss1 | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 93 | flkL | 82 | flkL | +0.0299 | 0.1651 |
| 93 | flkL | 80 | other | +0.0041 | 0.0131 |
| 93 | flkL | 87 | flkL | +0.0030 | 0.0067 |
| 94 | flkL | 82 | flkL | +0.0026 | 0.0831 |
| 118 | ss1 | 107 | flkL | +0.0021 | 0.0184 |

### L7 H0 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.0485

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0471 | 97.1% |
| 225 | ss2 | +0.0008 | 1.6% |
| 93 | flkL | +0.0007 | 1.4% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0485 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -25 | 1 | 33.3% |
| -132 | 1 | 33.3% |
| +0 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 1 | 33.3% |
| flkL | ss2 | 1 | 33.3% |
| flkL | flkL | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 93 | flkL | 118 | ss1 | +0.0471 | 0.0565 |
| 93 | flkL | 225 | ss2 | +0.0008 | 0.0010 |
| 93 | flkL | 93 | flkL | +0.0007 | 0.0023 |

### L7 H4 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 24  |  total attr: +0.0814

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.0814 | 100.0% |

**Query mass** (top-1=36%, top-2=57%, top-3=63%)  [DISTR(V118/L93/D87/L124/L220)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0292 | 35.9% |
| 93 | flkL | +0.0171 | 21.0% |
| 87 | flkL | +0.0050 | 6.2% |
| 124 | ss1 | +0.0031 | 3.8% |
| 220 | ss2 | +0.0030 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -102 | 1 | 4.2% |
| -127 | 1 | 4.2% |
| -133 | 1 | 4.2% |
| -96 | 1 | 4.2% |
| +0 | 1 | 4.2% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 11 | 45.8% |
| other | ss2 | 7 | 29.2% |
| ss1 | ss2 | 4 | 16.7% |
| ss2 | ss2 | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 220 | ss2 | +0.0292 | 0.0382 |
| 93 | flkL | 220 | ss2 | +0.0171 | 0.0273 |
| 87 | flkL | 220 | ss2 | +0.0050 | 0.1426 |
| 124 | ss1 | 220 | ss2 | +0.0031 | 0.0345 |
| 220 | ss2 | 220 | ss2 | +0.0030 | 0.0092 |

### L7 H16 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 3  |  total attr: +0.0428

**Key mass** (top-1=89%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 248 | flkR | +0.0382 | 89.2% |
| 251 | flkR | +0.0038 | 9.0% |
| 246 | flkR | +0.0008 | 1.8% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.0428 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -28 | 1 | 33.3% |
| -31 | 1 | 33.3% |
| -26 | 1 | 33.3% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 220 | ss2 | 248 | flkR | +0.0382 | 0.1018 |
| 220 | ss2 | 251 | flkR | +0.0038 | 0.0595 |
| 220 | ss2 | 246 | flkR | +0.0008 | 0.0127 |

### L9 H7 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:flkL→ss2  |  cells: 16  |  total attr: +0.1388

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.1379 | 99.3% |
| -1 | other | +0.0009 | 0.7% |

**Query mass** (top-1=71%, top-2=83%, top-3=87%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0980 | 70.6% |
| 118 | ss1 | +0.0171 | 12.3% |
| 124 | ss1 | +0.0056 | 4.1% |
| 92 | flkL | +0.0046 | 3.3% |
| 127 | other | +0.0026 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -127 | 1 | 6.2% |
| -102 | 1 | 6.2% |
| -96 | 1 | 6.2% |
| -128 | 1 | 6.2% |
| -93 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 8 | 50.0% |
| other | ss2 | 4 | 25.0% |
| ss1 | ss2 | 3 | 18.8% |
| flkL | other | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 93 | flkL | 220 | ss2 | +0.0971 | 0.1395 |
| 118 | ss1 | 220 | ss2 | +0.0171 | 0.0258 |
| 124 | ss1 | 220 | ss2 | +0.0056 | 0.0716 |
| 92 | flkL | 220 | ss2 | +0.0046 | 0.0861 |
| 127 | other | 220 | ss2 | +0.0026 | 0.0723 |

### L10 H0 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 15  |  total attr: +0.0521

**Key mass** (top-1=91%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0476 | 91.5% |
| 220 | ss2 | +0.0016 | 3.1% |
| 115 | ss1 | +0.0011 | 2.1% |
| 108 | flkL | +0.0009 | 1.7% |
| 118 | ss1 | +0.0009 | 1.7% |

**Query mass** (top-1=39%, top-2=61%, top-3=68%)  [DISTR(G99/G95/F96/S97)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 99 | flkL | +0.0203 | 39.0% |
| 95 | flkL | +0.0116 | 22.4% |
| 96 | flkL | +0.0036 | 6.9% |
| 97 | flkL | +0.0020 | 3.9% |
| 103 | flkL | +0.0020 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 13.3% |
| +10 | 2 | 13.3% |
| +1 | 2 | 13.3% |
| -1 | 2 | 13.3% |
| +6 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 11 | 73.3% |
| ss1 | ss1 | 2 | 13.3% |
| ss2 | ss2 | 1 | 6.7% |
| ss1 | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 99 | flkL | 93 | flkL | +0.0203 | 0.3796 |
| 95 | flkL | 93 | flkL | +0.0116 | 0.3095 |
| 96 | flkL | 93 | flkL | +0.0036 | 0.2747 |
| 97 | flkL | 93 | flkL | +0.0020 | 0.3155 |
| 103 | flkL | 93 | flkL | +0.0020 | 0.1195 |

### L10 H9 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 13  |  total attr: +0.0499

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.0499 | 100.0% |

**Query mass** (top-1=29%, top-2=44%, top-3=57%)  [DISTR(L93/V118/G99/V107/G95)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0146 | 29.3% |
| 118 | ss1 | +0.0075 | 15.0% |
| 99 | flkL | +0.0066 | 13.2% |
| 107 | flkL | +0.0060 | 12.0% |
| 95 | flkL | +0.0044 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -127 | 1 | 7.7% |
| -102 | 1 | 7.7% |
| -121 | 1 | 7.7% |
| -113 | 1 | 7.7% |
| -125 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=77%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 10 | 76.9% |
| ss1 | ss2 | 3 | 23.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 93 | flkL | 220 | ss2 | +0.0146 | 0.0528 |
| 118 | ss1 | 220 | ss2 | +0.0075 | 0.0397 |
| 99 | flkL | 220 | ss2 | +0.0066 | 0.0424 |
| 107 | flkL | 220 | ss2 | +0.0060 | 0.0427 |
| 95 | flkL | 220 | ss2 | +0.0044 | 0.0400 |

### L11 H14 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 20  |  total attr: +0.2172

**Key mass** (top-1=98%, top-2=99%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.2139 | 98.5% |
| -1 | other | +0.0011 | 0.5% |
| 92 | flkL | +0.0008 | 0.4% |
| 96 | flkL | +0.0008 | 0.3% |
| 94 | flkL | +0.0006 | 0.3% |

**Query mass** (top-1=42%, top-2=57%, top-3=67%)  [DISTR(V118/V107/G99/F120)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0904 | 41.6% |
| 107 | flkL | +0.0342 | 15.8% |
| 99 | flkL | +0.0200 | 9.2% |
| 120 | ss1 | +0.0095 | 4.4% |
| 116 | ss1 | +0.0091 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +22 | 2 | 10.0% |
| +25 | 1 | 5.0% |
| +14 | 1 | 5.0% |
| +6 | 1 | 5.0% |
| +27 | 1 | 5.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 11 | 55.0% |
| ss1 | flkL | 8 | 40.0% |
| flkL | other | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 93 | flkL | +0.0890 | 0.3811 |
| 107 | flkL | 93 | flkL | +0.0342 | 0.3877 |
| 99 | flkL | 93 | flkL | +0.0200 | 0.5222 |
| 120 | ss1 | 93 | flkL | +0.0095 | 0.1847 |
| 116 | ss1 | 93 | flkL | +0.0091 | 0.3511 |

### L12 H2 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 13  |  total attr: +0.0422

**Key mass** (top-1=94%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.0398 | 94.4% |
| 93 | flkL | +0.0024 | 5.6% |

**Query mass** (top-1=28%, top-2=46%, top-3=60%)  [DISTR(V118/G99/L93/?-1/F120)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0119 | 28.1% |
| 99 | flkL | +0.0073 | 17.4% |
| 93 | flkL | +0.0059 | 14.0% |
| -1 | other | +0.0031 | 7.4% |
| 120 | ss1 | +0.0030 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -102 | 1 | 7.7% |
| -121 | 1 | 7.7% |
| -127 | 1 | 7.7% |
| -100 | 1 | 7.7% |
| -125 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 6 | 46.2% |
| ss1 | ss2 | 5 | 38.5% |
| other | flkL | 1 | 7.7% |
| other | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 220 | ss2 | +0.0119 | 0.1748 |
| 99 | flkL | 220 | ss2 | +0.0073 | 0.1828 |
| 93 | flkL | 220 | ss2 | +0.0059 | 0.1427 |
| 120 | ss1 | 220 | ss2 | +0.0030 | 0.1509 |
| 95 | flkL | 220 | ss2 | +0.0024 | 0.0968 |

### L12 H19 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0620

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0620 | 100.0% |

**Query mass** (top-1=51%, top-2=62%, top-3=66%)  [DISTR(V118/A119/L124/A122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0316 | 51.0% |
| 119 | ss1 | +0.0068 | 11.0% |
| 124 | ss1 | +0.0027 | 4.4% |
| 122 | ss1 | +0.0026 | 4.2% |
| 115 | ss1 | +0.0022 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +25 | 1 | 5.6% |
| +26 | 1 | 5.6% |
| +31 | 1 | 5.6% |
| +29 | 1 | 5.6% |
| +22 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 10 | 55.6% |
| ss1 | flkL | 8 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 93 | flkL | +0.0316 | 0.3229 |
| 119 | ss1 | 93 | flkL | +0.0068 | 0.2498 |
| 124 | ss1 | 93 | flkL | +0.0027 | 0.1657 |
| 122 | ss1 | 93 | flkL | +0.0026 | 0.1502 |
| 115 | ss1 | 93 | flkL | +0.0022 | 0.0942 |

### L13 H2 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | INTRA:ss1  |  cells: 13  |  total attr: +0.0694

**Key mass** (top-1=81%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0564 | 81.3% |
| 93 | flkL | +0.0098 | 14.1% |
| 115 | ss1 | +0.0009 | 1.3% |
| 117 | ss1 | +0.0008 | 1.2% |
| 220 | ss2 | +0.0008 | 1.2% |

**Query mass** (top-1=41%, top-2=62%, top-3=83%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 120 | ss1 | +0.0284 | 40.9% |
| 122 | ss1 | +0.0149 | 21.5% |
| 121 | ss1 | +0.0140 | 20.2% |
| 100 | flkL | +0.0050 | 7.3% |
| 101 | flkL | +0.0019 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 15.4% |
| +5 | 2 | 15.4% |
| -4 | 2 | 15.4% |
| +2 | 1 | 7.7% |
| +4 | 1 | 7.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 53.8% |
| flkL | flkL | 5 | 38.5% |
| ss2 | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 120 | ss1 | 118 | ss1 | +0.0266 | 0.4789 |
| 122 | ss1 | 118 | ss1 | +0.0149 | 0.4157 |
| 121 | ss1 | 118 | ss1 | +0.0140 | 0.4994 |
| 100 | flkL | 93 | flkL | +0.0050 | 0.4751 |
| 101 | flkL | 93 | flkL | +0.0019 | 0.3931 |

### L13 H9 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 5  |  total attr: +0.0298

**Key mass** (top-1=74%, top-2=90%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0219 | 73.6% |
| 103 | flkL | +0.0048 | 16.0% |
| 92 | flkL | +0.0011 | 3.7% |
| 95 | flkL | +0.0011 | 3.7% |
| 111 | flkL | +0.0009 | 3.0% |

**Query mass** (top-1=93%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 99 | flkL | +0.0278 | 93.3% |
| 95 | flkL | +0.0011 | 3.7% |
| 107 | flkL | +0.0009 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 2 | 40.0% |
| +6 | 1 | 20.0% |
| +3 | 1 | 20.0% |
| +4 | 1 | 20.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 99 | flkL | 93 | flkL | +0.0219 | 0.7164 |
| 99 | flkL | 103 | flkL | +0.0048 | 0.2491 |
| 95 | flkL | 92 | flkL | +0.0011 | 0.0795 |
| 99 | flkL | 95 | flkL | +0.0011 | 0.0222 |
| 107 | flkL | 111 | flkL | +0.0009 | 0.0480 |

### L13 H17 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 19  |  total attr: +0.0422

**Key mass** (top-1=49%, top-2=70%, top-3=86%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | flkL | +0.0205 | 48.6% |
| 93 | flkL | +0.0092 | 21.9% |
| 107 | flkL | +0.0064 | 15.1% |
| 99 | flkL | +0.0061 | 14.4% |

**Query mass** (top-1=62%, top-2=71%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0262 | 62.2% |
| 122 | ss1 | +0.0037 | 8.8% |
| 120 | ss1 | +0.0036 | 8.6% |
| 121 | ss1 | +0.0025 | 5.8% |
| 111 | flkL | +0.0019 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +23 | 2 | 10.5% |
| +25 | 2 | 10.5% |
| +13 | 2 | 10.5% |
| +11 | 1 | 5.3% |
| +19 | 1 | 5.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=63%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 12 | 63.2% |
| flkL | flkL | 7 | 36.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 95 | flkL | +0.0126 | 0.1118 |
| 118 | ss1 | 93 | flkL | +0.0066 | 0.1075 |
| 118 | ss1 | 107 | flkL | +0.0038 | 0.0484 |
| 118 | ss1 | 99 | flkL | +0.0032 | 0.0366 |
| 122 | ss1 | 95 | flkL | +0.0017 | 0.0784 |

### L14 H0 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 19  |  total attr: +0.0459

**Key mass** (top-1=51%, top-2=86%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 99 | flkL | +0.0235 | 51.1% |
| 93 | flkL | +0.0159 | 34.7% |
| 95 | flkL | +0.0048 | 10.4% |
| -1 | other | +0.0010 | 2.2% |
| 220 | ss2 | +0.0008 | 1.7% |

**Query mass** (top-1=36%, top-2=66%, top-3=77%)  [DISTR(V118/F120/I115)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0164 | 35.7% |
| 120 | ss1 | +0.0141 | 30.8% |
| 115 | ss1 | +0.0048 | 10.4% |
| 122 | ss1 | +0.0037 | 8.1% |
| 121 | ss1 | +0.0016 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +25 | 3 | 15.8% |
| +23 | 2 | 10.5% |
| +22 | 2 | 10.5% |
| +21 | 1 | 5.3% |
| +19 | 1 | 5.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=74%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 14 | 73.7% |
| flkL | flkL | 3 | 15.8% |
| ss1 | other | 1 | 5.3% |
| ss1 | ss2 | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 120 | ss1 | 99 | flkL | +0.0074 | 0.1445 |
| 118 | ss1 | 99 | flkL | +0.0065 | 0.1623 |
| 120 | ss1 | 93 | flkL | +0.0060 | 0.1183 |
| 118 | ss1 | 93 | flkL | +0.0057 | 0.1479 |
| 122 | ss1 | 99 | flkL | +0.0037 | 0.1543 |

### L14 H13 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 23  |  total attr: +0.0707

**Key mass** (top-1=62%, top-2=75%, top-3=83%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 99 | flkL | +0.0436 | 61.7% |
| 95 | flkL | +0.0096 | 13.5% |
| 93 | flkL | +0.0058 | 8.2% |
| 111 | flkL | +0.0054 | 7.7% |
| 107 | flkL | +0.0038 | 5.4% |

**Query mass** (top-1=33%, top-2=48%, top-3=60%)  [DISTR(V118/F120/L121/V107)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0233 | 32.9% |
| 120 | ss1 | +0.0109 | 15.4% |
| 121 | ss1 | +0.0085 | 12.1% |
| 107 | flkL | +0.0078 | 11.1% |
| 115 | ss1 | +0.0055 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 13.0% |
| +12 | 2 | 8.7% |
| +11 | 2 | 8.7% |
| +10 | 2 | 8.7% |
| +19 | 1 | 4.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 12 | 52.2% |
| flkL | flkL | 9 | 39.1% |
| ss1 | ss1 | 2 | 8.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 99 | flkL | +0.0133 | 0.3358 |
| 120 | ss1 | 99 | flkL | +0.0109 | 0.2881 |
| 121 | ss1 | 99 | flkL | +0.0061 | 0.3885 |
| 115 | ss1 | 99 | flkL | +0.0055 | 0.4026 |
| 107 | flkL | 95 | flkL | +0.0037 | 0.2851 |

### L14 H14 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:flkL  |  cells: 17  |  total attr: +0.0372

**Key mass** (top-1=26%, top-2=44%, top-3=60%)  [DISTR(V118/T112/L93/G111)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0096 | 25.9% |
| 112 | flkL | +0.0066 | 17.8% |
| 93 | flkL | +0.0060 | 16.1% |
| 111 | flkL | +0.0041 | 11.0% |
| 88 | flkL | +0.0024 | 6.5% |

**Query mass** (top-1=29%, top-2=48%, top-3=62%)  [DISTR(V118/A122/L93/G99)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0107 | 28.7% |
| 122 | ss1 | +0.0073 | 19.5% |
| 93 | flkL | +0.0052 | 13.9% |
| 99 | flkL | +0.0044 | 11.8% |
| 103 | flkL | +0.0018 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 53%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 5 | 29.4% |
| +4 | 4 | 23.5% |
| +5 | 3 | 17.6% |
| +7 | 1 | 5.9% |
| +2 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=59%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 10 | 58.8% |
| ss1 | ss1 | 5 | 29.4% |
| ss1 | flkL | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 118 | ss1 | +0.0073 | 0.3816 |
| 118 | ss1 | 112 | flkL | +0.0066 | 0.1009 |
| 118 | ss1 | 111 | flkL | +0.0041 | 0.1474 |
| 99 | flkL | 93 | flkL | +0.0030 | 0.2037 |
| 93 | flkL | 88 | flkL | +0.0024 | 0.0888 |

### L16 H18 — Rank #29

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | ss1→flkL  |  cells: 14  |  total attr: +0.0258

**Key mass** (top-1=30%, top-2=59%, top-3=75%)  [DISTR(L220/G99/L93)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.0078 | 30.3% |
| 99 | flkL | +0.0075 | 29.1% |
| 93 | flkL | +0.0040 | 15.4% |
| 95 | flkL | +0.0038 | 14.9% |
| -1 | other | +0.0015 | 5.8% |

**Query mass** (top-1=50%, top-2=71%, top-3=80%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0130 | 50.4% |
| 120 | ss1 | +0.0054 | 21.0% |
| 112 | flkL | +0.0022 | 8.7% |
| 113 | flkL | +0.0021 | 8.0% |
| 114 | ss1 | +0.0012 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +25 | 2 | 14.3% |
| -102 | 1 | 7.1% |
| -100 | 1 | 7.1% |
| +23 | 1 | 7.1% |
| +13 | 1 | 7.1% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 42.9% |
| ss1 | ss2 | 3 | 21.4% |
| flkL | flkL | 3 | 21.4% |
| ss1 | other | 1 | 7.1% |
| ss1 | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 220 | ss2 | +0.0042 | 0.0229 |
| 118 | ss1 | 93 | flkL | +0.0027 | 0.0320 |
| 120 | ss1 | 220 | ss2 | +0.0026 | 0.0258 |
| 118 | ss1 | 95 | flkL | +0.0024 | 0.0183 |
| 112 | flkL | 99 | flkL | +0.0022 | 0.2330 |

### L17 H10 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | INTRA:ss1  |  cells: 15  |  total attr: +0.0784

**Key mass** (top-1=89%, top-2=94%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0698 | 89.1% |
| 124 | ss1 | +0.0041 | 5.2% |
| 120 | ss1 | +0.0018 | 2.3% |
| 106 | flkL | +0.0012 | 1.5% |
| 226 | ss2 | +0.0008 | 1.0% |

**Query mass** (top-1=34%, top-2=61%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0270 | 34.5% |
| 121 | ss1 | +0.0212 | 27.0% |
| 120 | ss1 | +0.0162 | 20.6% |
| 118 | ss1 | +0.0030 | 3.9% |
| 117 | ss1 | +0.0027 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 4 | 26.7% |
| -1 | 2 | 13.3% |
| -2 | 2 | 13.3% |
| +4 | 1 | 6.7% |
| +3 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 73.3% |
| ss1 | ss2 | 2 | 13.3% |
| flkL | ss1 | 1 | 6.7% |
| flkL | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 118 | ss1 | +0.0246 | 0.6470 |
| 121 | ss1 | 118 | ss1 | +0.0201 | 0.6447 |
| 120 | ss1 | 118 | ss1 | +0.0147 | 0.5208 |
| 118 | ss1 | 118 | ss1 | +0.0030 | 0.3008 |
| 117 | ss1 | 118 | ss1 | +0.0027 | 0.4711 |

### L17 H18 — Rank #22

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | ss1→flkL  |  cells: 15  |  total attr: +0.0330

**Key mass** (top-1=25%, top-2=41%, top-3=54%)  [DISTR(L93/A122/V118/F96/F120)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | flkL | +0.0081 | 24.6% |
| 122 | ss1 | +0.0054 | 16.3% |
| 118 | ss1 | +0.0043 | 13.0% |
| 96 | flkL | +0.0036 | 10.8% |
| 120 | ss1 | +0.0035 | 10.5% |

**Query mass** (top-1=19%, top-2=34%, top-3=47%)  [DISTR(L121/F120/H223/A219/I221)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 121 | ss1 | +0.0062 | 18.7% |
| 120 | ss1 | +0.0050 | 15.2% |
| 223 | ss2 | +0.0043 | 13.1% |
| 219 | ss2 | +0.0043 | 13.0% |
| 221 | ss2 | +0.0035 | 10.5% |

**Offset distribution [frequency]** (top-2 coverage: 53%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 4 | 26.7% |
| +25 | 4 | 26.7% |
| +28 | 2 | 13.3% |
| +13 | 1 | 6.7% |
| +15 | 1 | 6.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 9 | 60.0% |
| ss2 | ss1 | 5 | 33.3% |
| flkL | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 122 | ss1 | +0.0043 | 0.1200 |
| 219 | ss2 | 118 | ss1 | +0.0043 | 0.1012 |
| 121 | ss1 | 93 | flkL | +0.0038 | 0.2669 |
| 221 | ss2 | 120 | ss1 | +0.0035 | 0.1095 |
| 106 | flkL | 93 | flkL | +0.0033 | 0.2704 |

### L18 H1 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0426

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss2 | +0.0418 | 98.1% |
| 277 | other | +0.0008 | 1.9% |

**Query mass** (top-1=42%, top-2=73%, top-3=83%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 120 | ss1 | +0.0179 | 42.0% |
| 118 | ss1 | +0.0134 | 31.5% |
| 121 | ss1 | +0.0039 | 9.1% |
| 117 | ss1 | +0.0031 | 7.2% |
| 107 | flkL | +0.0018 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -100 | 1 | 12.5% |
| -102 | 1 | 12.5% |
| -99 | 1 | 12.5% |
| -103 | 1 | 12.5% |
| -113 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 75.0% |
| flkL | ss2 | 1 | 12.5% |
| ss1 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 120 | ss1 | 220 | ss2 | +0.0179 | 0.4714 |
| 118 | ss1 | 220 | ss2 | +0.0126 | 0.2417 |
| 121 | ss1 | 220 | ss2 | +0.0039 | 0.4058 |
| 117 | ss1 | 220 | ss2 | +0.0031 | 0.4288 |
| 107 | flkL | 220 | ss2 | +0.0018 | 0.1610 |

### L18 H8 — Rank #28

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 10  |  total attr: +0.0280

**Key mass** (top-1=29%, top-2=54%, top-3=75%)  [DISTR(L121/A122/S123)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 121 | ss1 | +0.0083 | 29.5% |
| 122 | ss1 | +0.0070 | 25.0% |
| 123 | ss1 | +0.0057 | 20.3% |
| 120 | ss1 | +0.0036 | 12.7% |
| 119 | ss1 | +0.0021 | 7.7% |

**Query mass** (top-1=81%, top-2=87%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0226 | 80.9% |
| 120 | ss1 | +0.0018 | 6.6% |
| 121 | ss1 | +0.0015 | 5.3% |
| 117 | ss1 | +0.0013 | 4.7% |
| 222 | ss2 | +0.0007 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 3 | 30.0% |
| -3 | 2 | 20.0% |
| -4 | 2 | 20.0% |
| -1 | 2 | 20.0% |
| -5 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=90%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 90.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 121 | ss1 | +0.0083 | 0.2180 |
| 118 | ss1 | 122 | ss1 | +0.0070 | 0.4078 |
| 118 | ss1 | 120 | ss1 | +0.0036 | 0.1243 |
| 118 | ss1 | 123 | ss1 | +0.0030 | 0.1199 |
| 121 | ss1 | 123 | ss1 | +0.0015 | 0.3159 |

### L19 H0 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 14  |  total attr: +0.0412

**Key mass** (top-1=62%, top-2=71%, top-3=78%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0255 | 61.8% |
| 120 | ss1 | +0.0037 | 9.0% |
| 114 | ss1 | +0.0031 | 7.6% |
| 117 | ss1 | +0.0021 | 5.1% |
| 113 | flkL | +0.0019 | 4.5% |

**Query mass** (top-1=66%, top-2=81%, top-3=92%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 120 | ss1 | +0.0274 | 66.5% |
| 121 | ss1 | +0.0062 | 14.9% |
| 122 | ss1 | +0.0043 | 10.5% |
| 119 | ss1 | +0.0014 | 3.3% |
| 106 | flkL | +0.0012 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 4 | 28.6% |
| +2 | 3 | 21.4% |
| +7 | 3 | 21.4% |
| +3 | 2 | 14.3% |
| +1 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 57.1% |
| ss1 | flkL | 5 | 35.7% |
| flkL | flkL | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 120 | ss1 | 118 | ss1 | +0.0238 | 0.4879 |
| 122 | ss1 | 120 | ss1 | +0.0037 | 0.4657 |
| 121 | ss1 | 114 | ss1 | +0.0025 | 0.2506 |
| 121 | ss1 | 118 | ss1 | +0.0017 | 0.0425 |
| 119 | ss1 | 117 | ss1 | +0.0014 | 0.4384 |

### L22 H14 — Rank #1

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 22  |  total attr: +0.1749

**Key mass** (top-1=40%, top-2=60%, top-3=80%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 120 | ss1 | +0.0701 | 40.1% |
| 122 | ss1 | +0.0351 | 20.1% |
| 121 | ss1 | +0.0351 | 20.1% |
| 118 | ss1 | +0.0099 | 5.6% |
| 93 | flkL | +0.0055 | 3.2% |

**Query mass** (top-1=25%, top-2=46%, top-3=66%)  [DISTR(A219/L222/I221/H223)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss2 | +0.0438 | 25.0% |
| 222 | ss2 | +0.0361 | 20.7% |
| 221 | ss2 | +0.0349 | 20.0% |
| 223 | ss2 | +0.0276 | 15.8% |
| 217 | ss2 | +0.0143 | 8.2% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 5 | 22.7% |
| +102 | 3 | 13.6% |
| +99 | 2 | 9.1% |
| +103 | 2 | 9.1% |
| +24 | 2 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 14 | 63.6% |
| ss1 | flkL | 6 | 27.3% |
| ss2 | flkL | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 222 | ss2 | 121 | ss1 | +0.0351 | 0.5563 |
| 221 | ss2 | 120 | ss1 | +0.0349 | 0.7008 |
| 219 | ss2 | 120 | ss1 | +0.0342 | 0.5052 |
| 223 | ss2 | 122 | ss1 | +0.0276 | 0.5381 |
| 224 | ss2 | 122 | ss1 | +0.0076 | 0.2046 |

### L26 H16 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.1402

**Key mass** (top-1=38%, top-2=59%, top-3=72%)  [DISTR(A219/I221/V217)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss2 | +0.0526 | 37.6% |
| 221 | ss2 | +0.0297 | 21.2% |
| 217 | ss2 | +0.0184 | 13.1% |
| 222 | ss2 | +0.0172 | 12.2% |
| 220 | ss2 | +0.0100 | 7.1% |

**Query mass** (top-1=31%, top-2=62%, top-3=75%)  [DISTR(V118/F120/I115)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0440 | 31.4% |
| 120 | ss1 | +0.0433 | 30.9% |
| 115 | ss1 | +0.0184 | 13.1% |
| 121 | ss1 | +0.0172 | 12.2% |
| 119 | ss1 | +0.0100 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 47%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -101 | 5 | 33.3% |
| -102 | 2 | 13.3% |
| -99 | 1 | 6.7% |
| -119 | 1 | 6.7% |
| -118 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 60.0% |
| ss1 | flkR | 5 | 33.3% |
| flkL | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 118 | ss1 | 219 | ss2 | +0.0419 | 0.6992 |
| 120 | ss1 | 221 | ss2 | +0.0297 | 0.5642 |
| 115 | ss1 | 217 | ss2 | +0.0184 | 0.3553 |
| 121 | ss1 | 222 | ss2 | +0.0172 | 0.3962 |
| 120 | ss1 | 219 | ss2 | +0.0107 | 0.1080 |

### L27 H15 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.0372

**Key mass** (top-1=42%, top-2=64%, top-3=78%)  [DISTR(V118/F120/L121)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0155 | 41.7% |
| 120 | ss1 | +0.0083 | 22.2% |
| 121 | ss1 | +0.0051 | 13.8% |
| 92 | flkL | +0.0028 | 7.5% |
| 117 | ss1 | +0.0022 | 5.9% |

**Query mass** (top-1=37%, top-2=65%, top-3=79%)  [DISTR(A219/V217/L222)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss2 | +0.0137 | 36.9% |
| 217 | ss2 | +0.0104 | 28.0% |
| 222 | ss2 | +0.0051 | 13.8% |
| 117 | ss1 | +0.0028 | 7.5% |
| 221 | ss2 | +0.0019 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 3 | 25.0% |
| +99 | 2 | 16.7% |
| +25 | 2 | 16.7% |
| +100 | 2 | 16.7% |
| +102 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 66.7% |
| ss1 | flkL | 3 | 25.0% |
| ss2 | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 217 | ss2 | 118 | ss1 | +0.0073 | 0.2630 |
| 219 | ss2 | 118 | ss1 | +0.0065 | 0.1190 |
| 219 | ss2 | 120 | ss1 | +0.0064 | 0.0644 |
| 222 | ss2 | 121 | ss1 | +0.0051 | 0.0822 |
| 117 | ss1 | 92 | flkL | +0.0028 | 0.4534 |

### L30 H1 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.0462

**Key mass** (top-1=25%, top-2=42%, top-3=56%)  [DISTR(V118/H223/I221/A219/F120)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0117 | 25.4% |
| 223 | ss2 | +0.0078 | 17.0% |
| 221 | ss2 | +0.0062 | 13.4% |
| 219 | ss2 | +0.0051 | 11.0% |
| 120 | ss1 | +0.0034 | 7.4% |

**Query mass** (top-1=20%, top-2=39%, top-3=54%)  [DISTR(A122/V217/V118/F120/A219)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0090 | 19.5% |
| 217 | ss2 | +0.0089 | 19.3% |
| 118 | ss1 | +0.0068 | 14.6% |
| 120 | ss1 | +0.0062 | 13.4% |
| 219 | ss2 | +0.0047 | 10.2% |

**Offset distribution [frequency]** (top-2 coverage: 47%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -101 | 5 | 33.3% |
| +99 | 2 | 13.3% |
| +101 | 2 | 13.3% |
| -102 | 2 | 13.3% |
| -103 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 60.0% |
| ss2 | ss1 | 5 | 33.3% |
| ss1 | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 223 | ss2 | +0.0078 | 0.1587 |
| 217 | ss2 | 118 | ss1 | +0.0078 | 0.1791 |
| 120 | ss1 | 221 | ss2 | +0.0062 | 0.1021 |
| 118 | ss1 | 219 | ss2 | +0.0051 | 0.0799 |
| 219 | ss2 | 118 | ss1 | +0.0039 | 0.0696 |

### L32 H13 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 17  |  total attr: +0.0375

**Key mass** (top-1=22%, top-2=36%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | ss1 | +0.0084 | 22.3% |
| 120 | ss1 | +0.0051 | 13.5% |
| 115 | ss1 | +0.0041 | 11.0% |
| 219 | ss2 | +0.0039 | 10.3% |
| 121 | ss1 | +0.0032 | 8.7% |

**Query mass** (top-1=31%, top-2=47%, top-3=55%)  [DISTR(V217/A219/F120/L222/A122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | ss2 | +0.0117 | 31.1% |
| 219 | ss2 | +0.0058 | 15.5% |
| 120 | ss1 | +0.0033 | 8.7% |
| 222 | ss2 | +0.0032 | 8.7% |
| 122 | ss1 | +0.0032 | 8.5% |

**Offset distribution [frequency]** (top-2 coverage: 53%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 5 | 29.4% |
| -101 | 4 | 23.5% |
| +99 | 2 | 11.8% |
| +102 | 2 | 11.8% |
| -99 | 2 | 11.8% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 52.9% |
| ss1 | ss2 | 8 | 47.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 217 | ss2 | 118 | ss1 | +0.0065 | 0.1096 |
| 217 | ss2 | 115 | ss1 | +0.0041 | 0.0364 |
| 219 | ss2 | 120 | ss1 | +0.0040 | 0.0302 |
| 222 | ss2 | 121 | ss1 | +0.0032 | 0.0376 |
| 120 | ss1 | 219 | ss2 | +0.0023 | 0.0174 |

### L32 H18 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 23  |  total attr: +0.1032

**Key mass** (top-1=20%, top-2=40%, top-3=55%)  [DISTR(V217/F120/A219/L121/V118)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | ss2 | +0.0212 | 20.5% |
| 120 | ss1 | +0.0196 | 19.0% |
| 219 | ss2 | +0.0155 | 15.0% |
| 121 | ss1 | +0.0102 | 9.8% |
| 118 | ss1 | +0.0096 | 9.3% |

**Query mass** (top-1=18%, top-2=33%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss2 | +0.0188 | 18.2% |
| 120 | ss1 | +0.0154 | 14.9% |
| 217 | ss2 | +0.0109 | 10.5% |
| 118 | ss1 | +0.0104 | 10.1% |
| 222 | ss2 | +0.0102 | 9.8% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 5 | 21.7% |
| -101 | 5 | 21.7% |
| -99 | 2 | 8.7% |
| +99 | 2 | 8.7% |
| -102 | 2 | 8.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 12 | 52.2% |
| ss1 | ss2 | 11 | 47.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 120 | ss1 | 219 | ss2 | +0.0144 | 0.0659 |
| 219 | ss2 | 120 | ss1 | +0.0142 | 0.0649 |
| 222 | ss2 | 121 | ss1 | +0.0102 | 0.0721 |
| 118 | ss1 | 217 | ss2 | +0.0093 | 0.0938 |
| 115 | ss1 | 217 | ss2 | +0.0083 | 0.0446 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #2 | L0 | H19 | 49 | +0.0682 | DISTRIBUTED |  | DISTRIBUTED | V82/L258/V118/V92 |  |  |
| #4 | L5 | H19 | 4 | +0.1983 | SINGLE-ANCHOR | G95 | SINGLE-ANCHOR | V118 |  | ss1→flkL |
| #11 | L6 | H12 | 12 | +0.0475 | SINGLE-ANCHOR | V82 | SINGLE-ANCHOR | L93 |  | INTRA:flkL |
| #18 | L7 | H0 | 3 | +0.0485 | SINGLE-ANCHOR | V118 | SINGLE-ANCHOR | L93 |  |  |
| #14 | L7 | H4 | 24 | +0.0814 | SINGLE-ANCHOR | L220 | DISTRIBUTED | V118/L93/D87/L124/L220 |  | CROSS:flkL→ss2 |
| #23 | L7 | H16 | 3 | +0.0428 | SINGLE-ANCHOR | Y248 | SINGLE-ANCHOR | L220 |  | ss2→flkR |
| #6 | L9 | H7 | 16 | +0.1388 | SINGLE-ANCHOR | L220 | SINGLE-ANCHOR | L93 |  | CROSS:flkL→ss2 |
| #20 | L10 | H0 | 15 | +0.0521 | SINGLE-ANCHOR | L93 | DISTRIBUTED | G99/G95/F96/S97 |  | INTRA:flkL |
| #15 | L10 | H9 | 13 | +0.0499 | SINGLE-ANCHOR | L220 | DISTRIBUTED | L93/V118/G99/V107/G95 |  | CROSS:flkL→ss2 |
| #3 | L11 | H14 | 20 | +0.2172 | SINGLE-ANCHOR | L93 | DISTRIBUTED | V118/V107/G99/F120 |  | INTRA:flkL |
| #16 | L12 | H2 | 13 | +0.0422 | SINGLE-ANCHOR | L220 | DISTRIBUTED | V118/G99/L93/?-1/F120 |  | CROSS:flkL→ss2 |
| #10 | L12 | H19 | 18 | +0.0620 | SINGLE-ANCHOR | L93 | DISTRIBUTED | V118/A119/L124/A122 |  |  |
| #26 | L13 | H2 | 13 | +0.0694 | SINGLE-ANCHOR | V118 | MULTI-ANCHOR |  |  | INTRA:ss1 |
| #25 | L13 | H9 | 5 | +0.0298 | SINGLE-ANCHOR | L93 | SINGLE-ANCHOR | G99 |  | INTRA:flkL |
| #19 | L13 | H17 | 19 | +0.0422 | DUAL-ANCHOR | G95/L93 | SINGLE-ANCHOR | V118 |  | ss1→flkL |
| #17 | L14 | H0 | 19 | +0.0459 | DUAL-ANCHOR | G99/L93 | DISTRIBUTED | V118/F120/I115 |  | ss1→flkL |
| #27 | L14 | H13 | 23 | +0.0707 | SINGLE-ANCHOR | G99 | DISTRIBUTED | V118/F120/L121/V107 |  | ss1→flkL |
| #30 | L14 | H14 | 17 | +0.0372 | DISTRIBUTED | V118/T112/L93/G111 | DISTRIBUTED | V118/A122/L93/G99 | POSITIONAL | INTRA:flkL |
| #29 | L16 | H18 | 14 | +0.0258 | DISTRIBUTED | L220/G99/L93 | DUAL-ANCHOR | V118/F120 |  | ss1→flkL |
| #9 | L17 | H10 | 15 | +0.0784 | SINGLE-ANCHOR | V118 | MULTI-ANCHOR |  |  | INTRA:ss1 |
| #22 | L17 | H18 | 15 | +0.0330 | DISTRIBUTED | L93/A122/V118/F96/F120 | DISTRIBUTED | L121/F120/H223/A219/I221 | CROSS_SSE | ss1→flkL |
| #21 | L18 | H1 | 8 | +0.0426 | SINGLE-ANCHOR | L220 | DUAL-ANCHOR | F120/V118 |  | CROSS:ss1→ss2 |
| #28 | L18 | H8 | 10 | +0.0280 | DISTRIBUTED | L121/A122/S123 | SINGLE-ANCHOR | V118 |  | INTRA:ss1 |
| #24 | L19 | H0 | 14 | +0.0412 | SINGLE-ANCHOR | V118 | SINGLE-ANCHOR | F120 |  | INTRA:ss1 |
| #1 | L22 | H14 | 22 | +0.1749 | MULTI-ANCHOR |  | DISTRIBUTED | A219/L222/I221/H223 |  | CROSS:ss2→ss1 |
| #5 | L26 | H16 | 15 | +0.1402 | DISTRIBUTED | A219/I221/V217 | DISTRIBUTED | V118/F120/I115 |  | CROSS:ss1→ss2 |
| #13 | L27 | H15 | 12 | +0.0372 | DISTRIBUTED | V118/F120/L121 | DISTRIBUTED | A219/V217/L222 |  | CROSS:ss2→ss1 |
| #8 | L30 | H1 | 15 | +0.0462 | DISTRIBUTED | V118/H223/I221/A219/F120 | DISTRIBUTED | A122/V217/V118/F120/A219 |  | CROSS:ss1→ss2 |
| #12 | L32 | H13 | 17 | +0.0375 | DISTRIBUTED |  | DISTRIBUTED | V217/A219/F120/L222/A122 | CROSS_SSE | CROSS:ss2→ss1 |
| #7 | L32 | H18 | 23 | +0.1032 | DISTRIBUTED | V217/F120/A219/L121/V118 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
