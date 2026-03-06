# Contact Pattern Analysis: 1IN4A

Generated: 2026-03-03 05:04:35   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1IN4A |
| Contact pair | (55, 174) |
| ss1 | [50, 61) |
| ss2 | [169, 180) |
| Clean flank | 40 |
| Corrupt flank | 39 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.9656 |
| Corrupt metric | 0.3736 |
| Gap | 0.5921 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 75 | 70.91% |
| positive IE | 50 | 91.45% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H18 | +0.1307 |
| 2 | L26 | H16 | +0.1051 |
| 3 | L13 | H8 | +0.0676 |
| 4 | L13 | H12 | +0.0617 |
| 5 | L32 | H13 | +0.0474 |
| 6 | L29 | H18 | +0.0461 |
| 7 | L4 | H8 | +0.0456 |
| 8 | L14 | H9 | +0.0381 |
| 9 | L17 | H19 | +0.0361 |
| 10 | L13 | H19 | +0.0300 |
| 11 | L27 | H15 | +0.0275 |
| 12 | L16 | H18 | +0.0274 |
| 13 | L16 | H7 | +0.0265 |
| 14 | L18 | H1 | +0.0264 |
| 15 | L30 | H13 | +0.0229 |
| 16 | L11 | H16 | +0.0224 |
| 17 | L30 | H1 | +0.0204 |
| 18 | L20 | H5 | +0.0199 |
| 19 | L5 | H19 | +0.0189 |
| 20 | L13 | H7 | +0.0189 |
| 21 | L20 | H1 | +0.0184 |
| 22 | L7 | H4 | +0.0182 |
| 23 | L17 | H3 | +0.0177 |
| 24 | L15 | H4 | +0.0176 |
| 25 | L15 | H6 | +0.0145 |
| 26 | L19 | H1 | +0.0141 |
| 27 | L7 | H6 | +0.0140 |
| 28 | L19 | H9 | +0.0128 |
| 29 | L15 | H2 | +0.0127 |
| 30 | L21 | H17 | +0.0125 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 1.03% |
| 2 | 1.38% |
| 3 | 1.51% |
| 4 | 1.70% |
| 5 | 2.53% |
| 6 | 3.31% |
| 7 | 4.25% |
| 8 | 4.95% |
| 9 | 4.97% |
| 10 | 4.63% |
| 20 | 16.10% |
| 80 | 101.55% |
| 450 | 133.17% |

## Cell Attribution Analysis

Total cells: 5,338,334

- Positive: 2,653,424
- Negative: 2,682,232

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000019 | 533,834 |
| 95th | +0.00000064 | 266,917 |
| 99th | +0.00000524 | 53,384 |
| 99.5th | +0.00001168 | 26,692 |
| 99.9th | +0.00006429 | 5,339 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L17 | H19 | 214 | flkR | 218 | flkR | +0.042245 | 0.931092 |
| L13 | H8 | 150 | other | 218 | flkR | +0.028932 | 0.821681 |
| L16 | H18 | 218 | flkR | 174 | ss2 | +0.022164 | 0.576716 |
| L5 | H19 | 106 | other | 62 | other | +0.021133 | 0.047987 |
| L13 | H8 | 173 | ss2 | 218 | flkR | +0.020097 | 0.429348 |
| L5 | H19 | 107 | other | 62 | other | +0.018311 | 0.046498 |
| L4 | H8 | 62 | other | 29 | flkL | +0.017915 | 0.063323 |
| L13 | H19 | 150 | other | 218 | flkR | +0.015871 | 0.821778 |
| L11 | H18 | 187 | flkR | 187 | flkR | +0.015433 | 0.602961 |
| L13 | H8 | 151 | other | 218 | flkR | +0.014390 | 0.840584 |
| L15 | H2 | 174 | ss2 | 218 | flkR | +0.011533 | 0.560140 |
| L13 | H12 | 174 | ss2 | 218 | flkR | +0.011418 | 0.621879 |
| L26 | H16 | 54 | ss1 | 173 | ss2 | +0.010970 | 0.286864 |
| L13 | H12 | 173 | ss2 | 218 | flkR | +0.010015 | 0.519917 |
| L7 | H9 | 218 | flkR | 55 | ss1 | +0.009877 | 0.135730 |
| L7 | H9 | 106 | other | 55 | ss1 | +0.009694 | 0.076155 |
| L13 | H8 | 170 | ss2 | 218 | flkR | +0.009587 | 0.429830 |
| L16 | H7 | 218 | flkR | 218 | flkR | +0.009285 | 0.489014 |
| L12 | H0 | 218 | flkR | 217 | flkR | +0.009128 | 0.225013 |
| L29 | H18 | 58 | ss1 | 178 | ss2 | +0.008913 | 0.101106 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L16 | H7 | 52 | ss1 | 218 | flkR | -0.004716 | 0.462616 |
| L13 | H8 | 28 | flkL | 218 | flkR | -0.004758 | 0.536511 |
| L7 | H4 | 106 | other | 153 | other | -0.005126 | 0.050622 |
| L11 | H16 | 218 | flkR | 28 | flkL | -0.005150 | 0.129682 |
| L13 | H8 | 52 | ss1 | 218 | flkR | -0.005151 | 0.145000 |
| L7 | H4 | 107 | other | 152 | other | -0.005196 | 0.055506 |
| L7 | H4 | 107 | other | 153 | other | -0.005321 | 0.057318 |
| L14 | H9 | 173 | ss2 | 55 | ss1 | -0.005445 | 0.164330 |
| L16 | H7 | 180 | flkR | 218 | flkR | -0.005497 | 0.813808 |
| L7 | H4 | 106 | other | 152 | other | -0.005673 | 0.055688 |
| L13 | H18 | 184 | flkR | 218 | flkR | -0.005793 | 0.643283 |
| L7 | H4 | 106 | other | 151 | other | -0.006321 | 0.060074 |
| L13 | H18 | 151 | other | 218 | flkR | -0.006449 | 0.468416 |
| L13 | H18 | 150 | other | 218 | flkR | -0.007169 | 0.340540 |
| L13 | H18 | 180 | flkR | 218 | flkR | -0.007428 | 0.651725 |
| L14 | H9 | 214 | flkR | 218 | flkR | -0.007973 | 0.824239 |
| L13 | H7 | 218 | flkR | 208 | flkR | -0.008043 | 0.796178 |
| L16 | H7 | 171 | ss2 | 218 | flkR | -0.008713 | 0.708888 |
| L13 | H19 | 152 | other | 218 | flkR | -0.009370 | 0.876021 |
| L13 | H18 | 218 | flkR | 218 | flkR | -0.016934 | 0.532992 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.3736 | 0.00% |
| 10 | 10 | 7 | 0.3736 | 0.00% |
| 20 | 20 | 14 | 0.3749 | 0.22% |
| 50 | 50 | 26 | 0.3784 | 0.82% |
| 100 | 100 | 35 | 0.3821 | 1.44% |
| 200 | 200 | 45 | 0.4079 | 5.80% |
| 500 | 500 | 46 | 0.4540 | 13.58% |
| 1000 | 1,000 | 47 | 0.5582 | 31.19% |
| 2000 | 2,000 | 50 | 0.6483 | 46.40% |
| 5000 | 5,000 | 50 | 0.8025 | 72.44% |
| 10000 | 10,000 | 50 | 0.9319 | 94.30% |
| 20000 | 20,000 | 50 | 1.0208 | 109.31% |
| 50000 | 50,000 | 50 | 1.0686 | 117.39% |

## Motif Analysis

### L4 H8 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 2  |  total attr: +0.0183

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +0.0179 | 97.9% |
| 198 | flkR | +0.0004 | 2.1% |

**Query mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | other | +0.0179 | 97.9% |
| 218 | flkR | +0.0004 | 2.1% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +33 | 1 | 50.0% |
| +20 | 1 | 50.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 1 | 50.0% |
| flkR | flkR | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 62 | other | 29 | flkL | +0.0179 | 0.0633 |
| 218 | flkR | 198 | flkR | +0.0004 | 0.0057 |

### L5 H19 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0606

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | other | +0.0599 | 98.8% |
| 57 | ss1 | +0.0007 | 1.2% |

**Query mass** (top-1=35%, top-2=65%, top-3=73%)  [DISTR(F106/I107/A218)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0211 | 34.9% |
| 107 | other | +0.0183 | 30.2% |
| 218 | flkR | +0.0046 | 7.6% |
| 151 | other | +0.0015 | 2.5% |
| 150 | other | +0.0013 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +44 | 1 | 3.8% |
| +45 | 1 | 3.8% |
| +156 | 1 | 3.8% |
| +89 | 1 | 3.8% |
| +88 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 16 | 61.5% |
| other | other | 7 | 26.9% |
| ss2 | other | 1 | 3.8% |
| other | ss1 | 1 | 3.8% |
| ss1 | other | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 106 | other | 62 | other | +0.0211 | 0.0480 |
| 107 | other | 62 | other | +0.0183 | 0.0465 |
| 218 | flkR | 62 | other | +0.0046 | 0.0496 |
| 151 | other | 62 | other | +0.0015 | 0.0135 |
| 150 | other | 62 | other | +0.0013 | 0.0132 |

### L7 H4 — Rank #22

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 63  |  total attr: +0.0410

**Key mass** (top-1=20%, top-2=38%, top-3=53%)  [DISTR(T151/F150/V153/L152/P149)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 151 | other | +0.0081 | 19.7% |
| 150 | other | +0.0075 | 18.3% |
| 153 | other | +0.0062 | 15.3% |
| 152 | other | +0.0055 | 13.5% |
| 149 | other | +0.0039 | 9.5% |

**Query mass** (top-1=39%, top-2=50%, top-3=58%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0161 | 39.4% |
| 149 | other | +0.0043 | 10.6% |
| 215 | flkR | +0.0031 | 7.6% |
| 113 | other | +0.0022 | 5.5% |
| 114 | other | +0.0019 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -38 | 5 | 7.9% |
| -37 | 5 | 7.9% |
| -39 | 4 | 6.3% |
| -36 | 3 | 4.8% |
| +64 | 2 | 3.2% |

**Region-pair profile** (q→k)  (top=70%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 44 | 69.8% |
| flkR | other | 16 | 25.4% |
| ss1 | other | 2 | 3.2% |
| other | ss2 | 1 | 1.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 218 | flkR | 154 | other | +0.0027 | 0.0497 |
| 218 | flkR | 153 | other | +0.0025 | 0.0453 |
| 218 | flkR | 155 | other | +0.0021 | 0.0373 |
| 218 | flkR | 151 | other | +0.0019 | 0.0363 |
| 218 | flkR | 150 | other | +0.0018 | 0.0364 |

### L7 H6 — Rank #27

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 8  |  total attr: +0.0040

**Key mass** (top-1=26%, top-2=47%, top-3=60%)  [DISTR(N279/A280/A39/M45)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 279 | other | +0.0010 | 25.7% |
| 280 | other | +0.0008 | 20.9% |
| 39 | flkL | +0.0006 | 13.7% |
| 45 | flkL | +0.0005 | 13.4% |
| 42 | flkL | +0.0005 | 13.3% |

**Query mass** (top-1=40%, top-2=77%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0016 | 40.4% |
| 106 | other | +0.0015 | 36.4% |
| 107 | other | +0.0009 | 23.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -173 | 2 | 25.0% |
| -172 | 2 | 25.0% |
| +179 | 1 | 12.5% |
| +173 | 1 | 12.5% |
| +176 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 5 | 62.5% |
| flkR | flkL | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 106 | other | 279 | other | +0.0006 | 0.0043 |
| 218 | flkR | 39 | flkL | +0.0006 | 0.0055 |
| 218 | flkR | 45 | flkL | +0.0005 | 0.0063 |
| 218 | flkR | 42 | flkL | +0.0005 | 0.0158 |
| 106 | other | 278 | other | +0.0005 | 0.0039 |

### L11 H16 — Rank #16

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0130

**Key mass** (top-1=54%, top-2=69%, top-3=81%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 28 | flkL | +0.0070 | 54.0% |
| 331 | other | +0.0020 | 15.1% |
| 218 | flkR | +0.0015 | 11.7% |
| 334 | other | +0.0011 | 8.5% |
| 332 | other | +0.0008 | 6.2% |

**Query mass** (top-1=22%, top-2=31%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0029 | 22.4% |
| 168 | other | +0.0011 | 8.7% |
| 28 | flkL | +0.0011 | 8.5% |
| 150 | other | +0.0011 | 8.3% |
| 172 | ss2 | +0.0009 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 1 | 5.6% |
| +140 | 1 | 5.6% |
| -306 | 1 | 5.6% |
| -68 | 1 | 5.6% |
| +144 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 5 | 27.8% |
| flkR | other | 3 | 16.7% |
| other | flkL | 3 | 16.7% |
| ss1 | flkL | 2 | 11.1% |
| flkL | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 218 | flkR | 331 | other | +0.0015 | 0.0408 |
| 168 | other | 28 | flkL | +0.0011 | 0.1590 |
| 28 | flkL | 334 | other | +0.0011 | 0.0402 |
| 150 | other | 218 | flkR | +0.0011 | 0.1415 |
| 172 | ss2 | 28 | flkL | +0.0009 | 0.1018 |

### L13 H7 — Rank #20

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 35  |  total attr: +0.0242

**Key mass** (top-1=16%, top-2=27%, top-3=37%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0038 | 15.8% |
| -1 | other | +0.0028 | 11.4% |
| 107 | other | +0.0024 | 9.8% |
| 171 | ss2 | +0.0019 | 8.0% |
| 150 | other | +0.0010 | 4.0% |

**Query mass** (top-1=23%, top-2=37%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0056 | 23.0% |
| 150 | other | +0.0034 | 13.9% |
| 151 | other | +0.0026 | 10.6% |
| 174 | ss2 | +0.0017 | 6.9% |
| 171 | ss2 | +0.0015 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 34%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 7 | 20.0% |
| +3 | 5 | 14.3% |
| +44 | 2 | 5.7% |
| +65 | 2 | 5.7% |
| +47 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 11 | 31.4% |
| ss2 | other | 5 | 14.3% |
| flkR | other | 5 | 14.3% |
| flkR | flkR | 5 | 14.3% |
| flkL | flkL | 2 | 5.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 218 | flkR | 171 | ss2 | +0.0019 | 0.0919 |
| 150 | other | 106 | other | +0.0018 | 0.0480 |
| 174 | ss2 | -1 | other | +0.0017 | 0.1820 |
| 150 | other | 107 | other | +0.0012 | 0.0335 |
| 151 | other | 106 | other | +0.0011 | 0.0386 |

### L13 H8 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.1015

**Key mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0988 | 97.3% |
| 334 | other | +0.0027 | 2.7% |

**Query mass** (top-1=30%, top-2=50%, top-3=65%)  [DISTR(F150/I173/T151/F170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | other | +0.0301 | 29.7% |
| 173 | ss2 | +0.0207 | 20.4% |
| 151 | other | +0.0153 | 15.1% |
| 170 | ss2 | +0.0096 | 9.4% |
| 62 | other | +0.0057 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -68 | 1 | 4.5% |
| -45 | 1 | 4.5% |
| -67 | 1 | 4.5% |
| -48 | 1 | 4.5% |
| -156 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 11 | 50.0% |
| ss2 | flkR | 6 | 27.3% |
| other | other | 2 | 9.1% |
| ss2 | other | 1 | 4.5% |
| flkL | flkR | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 150 | other | 218 | flkR | +0.0289 | 0.8217 |
| 173 | ss2 | 218 | flkR | +0.0201 | 0.4293 |
| 151 | other | 218 | flkR | +0.0144 | 0.8406 |
| 170 | ss2 | 218 | flkR | +0.0096 | 0.4298 |
| 62 | other | 218 | flkR | +0.0057 | 0.4151 |

### L13 H12 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 36  |  total attr: +0.0788

**Key mass** (top-1=93%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0736 | 93.4% |
| 106 | other | +0.0031 | 4.0% |
| 107 | other | +0.0012 | 1.6% |
| 334 | other | +0.0004 | 0.5% |
| 55 | ss1 | +0.0004 | 0.5% |

**Query mass** (top-1=14%, top-2=28%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 174 | ss2 | +0.0114 | 14.5% |
| 173 | ss2 | +0.0104 | 13.3% |
| 170 | ss2 | +0.0079 | 10.1% |
| 150 | other | +0.0054 | 6.9% |
| 171 | ss2 | +0.0054 | 6.9% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -48 | 2 | 5.6% |
| -55 | 2 | 5.6% |
| -56 | 2 | 5.6% |
| -44 | 1 | 2.8% |
| -45 | 1 | 2.8% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 14 | 38.9% |
| ss2 | flkR | 8 | 22.2% |
| flkR | flkR | 4 | 11.1% |
| ss1 | other | 4 | 11.1% |
| flkL | other | 3 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 174 | ss2 | 218 | flkR | +0.0114 | 0.6219 |
| 173 | ss2 | 218 | flkR | +0.0100 | 0.5199 |
| 170 | ss2 | 218 | flkR | +0.0079 | 0.7256 |
| 150 | other | 218 | flkR | +0.0054 | 0.7181 |
| 171 | ss2 | 218 | flkR | +0.0054 | 0.6450 |

### L13 H19 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 17  |  total attr: +0.0328

**Key mass** (top-1=79%, top-2=85%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0258 | 78.8% |
| 151 | other | +0.0021 | 6.4% |
| 152 | other | +0.0020 | 6.1% |
| 150 | other | +0.0017 | 5.2% |
| 153 | other | +0.0007 | 2.0% |

**Query mass** (top-1=64%, top-2=73%, top-3=82%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | other | +0.0209 | 63.7% |
| 218 | flkR | +0.0030 | 9.3% |
| 151 | other | +0.0029 | 8.9% |
| 106 | other | +0.0015 | 4.6% |
| 171 | ss2 | +0.0013 | 3.9% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 17.6% |
| -1 | 2 | 11.8% |
| -68 | 1 | 5.9% |
| -112 | 1 | 5.9% |
| -67 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 7 | 41.2% |
| other | flkR | 6 | 35.3% |
| flkR | flkR | 1 | 5.9% |
| ss2 | flkR | 1 | 5.9% |
| ss1 | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 150 | other | 218 | flkR | +0.0159 | 0.8218 |
| 218 | flkR | 218 | flkR | +0.0030 | 0.0708 |
| 150 | other | 151 | other | +0.0016 | 0.0613 |
| 106 | other | 218 | flkR | +0.0015 | 0.3886 |
| 151 | other | 218 | flkR | +0.0015 | 0.8989 |

### L14 H9 — Rank #8

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 55  |  total attr: +0.0548

**Key mass** (top-1=52%, top-2=78%, top-3=88%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0284 | 51.8% |
| 55 | ss1 | +0.0142 | 25.9% |
| 150 | other | +0.0057 | 10.4% |
| 151 | other | +0.0030 | 5.4% |
| 184 | flkR | +0.0010 | 1.7% |

**Query mass** (top-1=14%, top-2=22%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0079 | 14.4% |
| 218 | flkR | +0.0040 | 7.2% |
| 169 | ss2 | +0.0030 | 5.4% |
| 150 | other | +0.0025 | 4.6% |
| 170 | ss2 | +0.0024 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 2 | 3.6% |
| -45 | 1 | 1.8% |
| -49 | 1 | 1.8% |
| +95 | 1 | 1.8% |
| +23 | 1 | 1.8% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 19 | 34.5% |
| ss1 | other | 7 | 12.7% |
| ss2 | flkR | 6 | 10.9% |
| ss2 | other | 5 | 9.1% |
| flkR | ss1 | 5 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | ss2 | 218 | flkR | +0.0034 | 0.2851 |
| 169 | ss2 | 218 | flkR | +0.0030 | 0.2984 |
| 150 | other | 55 | ss1 | +0.0025 | 0.1145 |
| 173 | ss2 | 150 | other | +0.0024 | 0.0456 |
| 171 | ss2 | 218 | flkR | +0.0023 | 0.3998 |

### L15 H2 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 12  |  total attr: +0.0243

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0239 | 98.1% |
| 151 | other | +0.0005 | 1.9% |

**Query mass** (top-1=49%, top-2=64%, top-3=79%)  [DISTR(L174/I173/G171)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 174 | ss2 | +0.0120 | 49.2% |
| 173 | ss2 | +0.0037 | 15.1% |
| 171 | ss2 | +0.0034 | 14.2% |
| 169 | ss2 | +0.0011 | 4.7% |
| 172 | ss2 | +0.0011 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -44 | 1 | 8.3% |
| -45 | 1 | 8.3% |
| -47 | 1 | 8.3% |
| -49 | 1 | 8.3% |
| -46 | 1 | 8.3% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 6 | 50.0% |
| flkR | flkR | 3 | 25.0% |
| other | flkR | 2 | 16.7% |
| ss2 | other | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 174 | ss2 | 218 | flkR | +0.0115 | 0.5601 |
| 173 | ss2 | 218 | flkR | +0.0037 | 0.5836 |
| 171 | ss2 | 218 | flkR | +0.0034 | 0.5589 |
| 169 | ss2 | 218 | flkR | +0.0011 | 0.4322 |
| 172 | ss2 | 218 | flkR | +0.0011 | 0.3922 |

### L15 H4 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→flkR  |  cells: 19  |  total attr: +0.0236

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0236 | 100.0% |

**Query mass** (top-1=30%, top-2=41%, top-3=50%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 50 | ss1 | +0.0072 | 30.3% |
| 54 | ss1 | +0.0025 | 10.6% |
| 28 | flkL | +0.0022 | 9.3% |
| 52 | ss1 | +0.0012 | 5.2% |
| 58 | ss1 | +0.0010 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -168 | 1 | 5.3% |
| -164 | 1 | 5.3% |
| -190 | 1 | 5.3% |
| -166 | 1 | 5.3% |
| -160 | 1 | 5.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 10 | 52.6% |
| flkL | flkR | 6 | 31.6% |
| other | flkR | 2 | 10.5% |
| ss2 | flkR | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 50 | ss1 | 218 | flkR | +0.0072 | 0.6833 |
| 54 | ss1 | 218 | flkR | +0.0025 | 0.1865 |
| 28 | flkL | 218 | flkR | +0.0022 | 0.4483 |
| 52 | ss1 | 218 | flkR | +0.0012 | 0.1958 |
| 58 | ss1 | 218 | flkR | +0.0010 | 0.1013 |

### L15 H6 — Rank #25

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.0283

**Key mass** (top-1=52%, top-2=70%, top-3=80%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | other | +0.0148 | 52.5% |
| 151 | other | +0.0049 | 17.5% |
| 55 | ss1 | +0.0029 | 10.3% |
| 152 | other | +0.0028 | 10.0% |
| 57 | ss1 | +0.0008 | 2.9% |

**Query mass** (top-1=41%, top-2=53%, top-3=62%)  [DISTR(I173/L174/F178/A218/L176)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0116 | 41.1% |
| 174 | ss2 | +0.0034 | 11.9% |
| 178 | ss2 | +0.0025 | 8.8% |
| 218 | flkR | +0.0017 | 6.1% |
| 176 | ss2 | +0.0017 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +21 | 2 | 8.7% |
| +67 | 2 | 8.7% |
| +24 | 2 | 8.7% |
| +20 | 2 | 8.7% |
| +26 | 2 | 8.7% |

**Region-pair profile** (q→k)  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 14 | 60.9% |
| other | other | 3 | 13.0% |
| ss2 | ss1 | 2 | 8.7% |
| flkR | other | 2 | 8.7% |
| flkR | ss2 | 2 | 8.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | ss2 | 150 | other | +0.0084 | 0.2178 |
| 174 | ss2 | 55 | ss1 | +0.0029 | 0.1462 |
| 173 | ss2 | 152 | other | +0.0021 | 0.0604 |
| 178 | ss2 | 150 | other | +0.0021 | 0.1524 |
| 176 | ss2 | 151 | other | +0.0017 | 0.2124 |

### L16 H7 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 81  |  total attr: +0.1147

**Key mass** (top-1=74%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0846 | 73.7% |
| 55 | ss1 | +0.0252 | 22.0% |
| 151 | other | +0.0039 | 3.4% |
| 36 | flkL | +0.0010 | 0.9% |

**Query mass** (top-1=8%, top-2=13%, top-3=17%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0093 | 8.1% |
| 173 | ss2 | +0.0052 | 4.5% |
| 174 | ss2 | +0.0051 | 4.5% |
| 151 | other | +0.0040 | 3.5% |
| 172 | ss2 | +0.0036 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 2.5% |
| +116 | 2 | 2.5% |
| -23 | 2 | 2.5% |
| -5 | 2 | 2.5% |
| +0 | 1 | 1.2% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 21 | 25.9% |
| flkL | flkR | 14 | 17.3% |
| other | flkR | 11 | 13.6% |
| flkR | ss1 | 7 | 8.6% |
| ss2 | flkR | 5 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 218 | flkR | 218 | flkR | +0.0093 | 0.4890 |
| 174 | ss2 | 218 | flkR | +0.0051 | 0.9320 |
| 173 | ss2 | 218 | flkR | +0.0041 | 0.8216 |
| 151 | other | 218 | flkR | +0.0040 | 0.3781 |
| 172 | ss2 | 218 | flkR | +0.0036 | 0.8024 |

### L16 H18 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 19  |  total attr: +0.0445

**Key mass** (top-1=81%, top-2=88%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 174 | ss2 | +0.0360 | 80.8% |
| 106 | other | +0.0031 | 6.9% |
| 107 | other | +0.0018 | 4.1% |
| 151 | other | +0.0013 | 3.0% |
| 218 | flkR | +0.0010 | 2.2% |

**Query mass** (top-1=50%, top-2=62%, top-3=74%)  [DISTR(A218/F150/T151)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0222 | 49.8% |
| 150 | other | +0.0056 | 12.5% |
| 151 | other | +0.0053 | 11.9% |
| 170 | ss2 | +0.0037 | 8.2% |
| 152 | other | +0.0015 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -23 | 2 | 10.5% |
| -22 | 2 | 10.5% |
| +64 | 2 | 10.5% |
| +63 | 2 | 10.5% |
| +44 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 9 | 47.4% |
| other | ss2 | 6 | 31.6% |
| flkR | ss2 | 2 | 10.5% |
| ss2 | flkR | 1 | 5.3% |
| flkR | flkR | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 218 | flkR | 174 | ss2 | +0.0222 | 0.5767 |
| 150 | other | 174 | ss2 | +0.0052 | 0.4085 |
| 151 | other | 174 | ss2 | +0.0048 | 0.3979 |
| 152 | other | 174 | ss2 | +0.0015 | 0.5128 |
| 213 | flkR | 174 | ss2 | +0.0014 | 0.3267 |

### L17 H3 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→flkR  |  cells: 36  |  total attr: +0.0392

**Key mass** (top-1=94%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0367 | 93.6% |
| 213 | flkR | +0.0020 | 5.2% |
| 334 | other | +0.0005 | 1.2% |

**Query mass** (top-1=11%, top-2=20%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 36 | flkL | +0.0044 | 11.1% |
| 52 | ss1 | +0.0035 | 9.0% |
| 188 | flkR | +0.0025 | 6.4% |
| 53 | ss1 | +0.0023 | 6.0% |
| 170 | ss2 | +0.0023 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -161 | 2 | 5.6% |
| -182 | 1 | 2.8% |
| -166 | 1 | 2.8% |
| -30 | 1 | 2.8% |
| -165 | 1 | 2.8% |

**Region-pair profile** (q→k)  [CROSS:flkL→flkR]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 16 | 44.4% |
| ss1 | flkR | 8 | 22.2% |
| ss2 | flkR | 5 | 13.9% |
| other | flkR | 5 | 13.9% |
| flkR | flkR | 1 | 2.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 36 | flkL | 218 | flkR | +0.0044 | 0.6870 |
| 52 | ss1 | 218 | flkR | +0.0030 | 0.2360 |
| 188 | flkR | 218 | flkR | +0.0025 | 0.4201 |
| 53 | ss1 | 218 | flkR | +0.0023 | 0.2313 |
| 170 | ss2 | 218 | flkR | +0.0023 | 0.1818 |

### L17 H19 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 9  |  total attr: +0.0538

**Key mass** (top-1=94%, top-2=96%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0507 | 94.3% |
| 170 | ss2 | +0.0009 | 1.6% |
| 53 | ss1 | +0.0007 | 1.3% |
| 334 | other | +0.0005 | 1.0% |
| 173 | ss2 | +0.0005 | 0.9% |

**Query mass** (top-1=79%, top-2=93%, top-3=94%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 214 | flkR | +0.0422 | 78.6% |
| 212 | flkR | +0.0078 | 14.5% |
| 50 | ss1 | +0.0007 | 1.3% |
| 216 | flkR | +0.0007 | 1.2% |
| 334 | other | +0.0005 | 1.0% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 22.2% |
| +3 | 2 | 22.2% |
| -4 | 1 | 11.1% |
| -6 | 1 | 11.1% |
| -2 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 3 | 33.3% |
| ss2 | ss2 | 2 | 22.2% |
| ss1 | ss1 | 1 | 11.1% |
| other | other | 1 | 11.1% |
| ss2 | other | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 214 | flkR | 218 | flkR | +0.0422 | 0.9311 |
| 212 | flkR | 218 | flkR | +0.0078 | 0.8575 |
| 50 | ss1 | 53 | ss1 | +0.0007 | 0.1507 |
| 216 | flkR | 218 | flkR | +0.0007 | 0.4434 |
| 334 | other | 334 | other | +0.0005 | 0.3080 |

### L18 H1 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 36  |  total attr: +0.0353

**Key mass** (top-1=25%, top-2=43%, top-3=58%)  [DISTR(A218/G213/F150/T151)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0087 | 24.6% |
| 213 | flkR | +0.0064 | 18.1% |
| 150 | other | +0.0054 | 15.2% |
| 151 | other | +0.0044 | 12.5% |
| 152 | other | +0.0041 | 11.7% |

**Query mass** (top-1=19%, top-2=38%, top-3=54%)  [DISTR(H52/F170/L54/V53/I173)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 52 | ss1 | +0.0068 | 19.2% |
| 170 | ss2 | +0.0065 | 18.3% |
| 54 | ss1 | +0.0060 | 16.9% |
| 53 | ss1 | +0.0043 | 12.1% |
| 173 | ss2 | +0.0035 | 9.8% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -99 | 4 | 11.1% |
| -98 | 3 | 8.3% |
| -48 | 2 | 5.6% |
| -100 | 2 | 5.6% |
| -96 | 2 | 5.6% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 24 | 66.7% |
| ss2 | flkR | 7 | 19.4% |
| ss1 | flkR | 2 | 5.6% |
| other | flkR | 1 | 2.8% |
| ss2 | other | 1 | 2.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | ss2 | 213 | flkR | +0.0033 | 0.2809 |
| 170 | ss2 | 218 | flkR | +0.0032 | 0.1931 |
| 173 | ss2 | 218 | flkR | +0.0031 | 0.1429 |
| 52 | ss1 | 150 | other | +0.0019 | 0.1426 |
| 52 | ss1 | 152 | other | +0.0015 | 0.0911 |

### L19 H1 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 15  |  total attr: +0.0162

**Key mass** (top-1=51%, top-2=75%, top-3=82%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0083 | 50.8% |
| 107 | other | +0.0039 | 24.3% |
| 150 | other | +0.0012 | 7.4% |
| 62 | other | +0.0012 | 7.3% |
| 152 | other | +0.0009 | 5.8% |

**Query mass** (top-1=60%, top-2=76%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | ss2 | +0.0097 | 59.8% |
| 173 | ss2 | +0.0027 | 16.4% |
| 169 | ss2 | +0.0015 | 9.0% |
| 178 | ss2 | +0.0008 | 5.1% |
| 176 | ss2 | +0.0006 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +63 | 3 | 20.0% |
| +64 | 1 | 6.7% |
| +67 | 1 | 6.7% |
| +116 | 1 | 6.7% |
| +66 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 11 | 73.3% |
| flkR | other | 2 | 13.3% |
| ss2 | ss1 | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | ss2 | 106 | other | +0.0051 | 0.3168 |
| 170 | ss2 | 107 | other | +0.0027 | 0.1731 |
| 173 | ss2 | 106 | other | +0.0016 | 0.3176 |
| 169 | ss2 | 106 | other | +0.0010 | 0.3125 |
| 178 | ss2 | 62 | other | +0.0008 | 0.1045 |

### L19 H9 — Rank #28

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→flkR  |  cells: 17  |  total attr: +0.0148

**Key mass** (top-1=53%, top-2=94%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 213 | flkR | +0.0079 | 53.3% |
| 218 | flkR | +0.0061 | 41.1% |
| 55 | ss1 | +0.0005 | 3.1% |
| 152 | other | +0.0004 | 2.5% |

**Query mass** (top-1=20%, top-2=37%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 54 | ss1 | +0.0029 | 19.9% |
| 58 | ss1 | +0.0026 | 17.4% |
| 12 | flkL | +0.0013 | 9.1% |
| 51 | ss1 | +0.0012 | 8.4% |
| 28 | flkL | +0.0011 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -162 | 2 | 11.8% |
| -155 | 1 | 5.9% |
| -164 | 1 | 5.9% |
| -201 | 1 | 5.9% |
| -165 | 1 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 8 | 47.1% |
| flkL | flkR | 7 | 41.2% |
| ss1 | ss1 | 1 | 5.9% |
| ss2 | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 58 | ss1 | 213 | flkR | +0.0026 | 0.1884 |
| 54 | ss1 | 218 | flkR | +0.0025 | 0.2261 |
| 12 | flkL | 213 | flkR | +0.0013 | 0.2477 |
| 53 | ss1 | 218 | flkR | +0.0010 | 0.2108 |
| 50 | ss1 | 218 | flkR | +0.0010 | 0.3238 |

### L20 H1 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 17  |  total attr: +0.0219

**Key mass** (top-1=44%, top-2=72%, top-3=83%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0097 | 44.3% |
| 184 | flkR | +0.0060 | 27.2% |
| 188 | flkR | +0.0024 | 11.1% |
| 67 | other | +0.0012 | 5.3% |
| 191 | flkR | +0.0010 | 4.8% |

**Query mass** (top-1=34%, top-2=50%, top-3=58%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 213 | flkR | +0.0074 | 33.9% |
| 178 | ss2 | +0.0036 | 16.5% |
| 184 | flkR | +0.0017 | 7.6% |
| 171 | ss2 | +0.0013 | 5.8% |
| 57 | ss1 | +0.0012 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 17.6% |
| +3 | 3 | 17.6% |
| -4 | 2 | 11.8% |
| -5 | 1 | 5.9% |
| -6 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=65%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 11 | 64.7% |
| ss2 | flkR | 2 | 11.8% |
| other | flkR | 2 | 11.8% |
| ss1 | other | 1 | 5.9% |
| ss1 | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 213 | flkR | 218 | flkR | +0.0070 | 0.7859 |
| 178 | ss2 | 184 | flkR | +0.0036 | 0.3505 |
| 184 | flkR | 188 | flkR | +0.0017 | 0.3040 |
| 171 | ss2 | 184 | flkR | +0.0013 | 0.1492 |
| 57 | ss1 | 67 | other | +0.0012 | 0.1698 |

### L20 H5 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 12  |  total attr: +0.0208

**Key mass** (top-1=86%, top-2=94%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | flkR | +0.0179 | 85.7% |
| 176 | ss2 | +0.0018 | 8.4% |
| 191 | flkR | +0.0004 | 2.1% |
| 153 | other | +0.0004 | 2.1% |
| 152 | other | +0.0004 | 1.7% |

**Query mass** (top-1=36%, top-2=57%, top-3=73%)  [DISTR(I173/F170/R167)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0076 | 36.3% |
| 170 | ss2 | +0.0044 | 21.0% |
| 167 | other | +0.0032 | 15.4% |
| 174 | ss2 | +0.0016 | 7.5% |
| 180 | flkR | +0.0013 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 2 | 16.7% |
| -9 | 2 | 16.7% |
| -2 | 2 | 16.7% |
| -10 | 1 | 8.3% |
| -6 | 1 | 8.3% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 6 | 50.0% |
| flkR | flkR | 2 | 16.7% |
| other | other | 2 | 16.7% |
| other | ss2 | 1 | 8.3% |
| other | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | ss2 | 180 | flkR | +0.0076 | 0.3797 |
| 170 | ss2 | 180 | flkR | +0.0044 | 0.2479 |
| 167 | other | 176 | ss2 | +0.0018 | 0.1266 |
| 174 | ss2 | 180 | flkR | +0.0016 | 0.2637 |
| 167 | other | 180 | flkR | +0.0014 | 0.0649 |

### L21 H17 — Rank #30

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 14  |  total attr: +0.0145

**Key mass** (top-1=52%, top-2=93%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0075 | 52.0% |
| 107 | other | +0.0060 | 41.5% |
| 28 | flkL | +0.0009 | 6.6% |

**Query mass** (top-1=31%, top-2=53%, top-3=74%)  [DISTR(A56/H52/G57)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 56 | ss1 | +0.0044 | 30.5% |
| 52 | ss1 | +0.0032 | 22.3% |
| 57 | ss1 | +0.0031 | 21.4% |
| 54 | ss1 | +0.0013 | 8.9% |
| 51 | ss1 | +0.0013 | 8.8% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -50 | 2 | 14.3% |
| -55 | 2 | 14.3% |
| -49 | 2 | 14.3% |
| -51 | 1 | 7.1% |
| -54 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 12 | 85.7% |
| ss1 | flkL | 2 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 56 | ss1 | 106 | other | +0.0025 | 0.2347 |
| 56 | ss1 | 107 | other | +0.0019 | 0.1661 |
| 52 | ss1 | 106 | other | +0.0019 | 0.3003 |
| 52 | ss1 | 107 | other | +0.0014 | 0.2163 |
| 57 | ss1 | 106 | other | +0.0013 | 0.1537 |

### L26 H16 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.0515

**Key mass** (top-1=28%, top-2=44%, top-3=58%)  [DISTR(I173/H52/D51/F170/G213)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0145 | 28.2% |
| 52 | ss1 | +0.0082 | 15.9% |
| 51 | ss1 | +0.0070 | 13.5% |
| 170 | ss2 | +0.0061 | 11.9% |
| 213 | flkR | +0.0045 | 8.7% |

**Query mass** (top-1=22%, top-2=40%, top-3=56%)  [DISTR(L54/F170/H52/G171)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 54 | ss1 | +0.0115 | 22.3% |
| 170 | ss2 | +0.0092 | 17.9% |
| 52 | ss1 | +0.0084 | 16.3% |
| 171 | ss2 | +0.0073 | 14.2% |
| 173 | ss2 | +0.0049 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 2 | 7.1% |
| -118 | 2 | 7.1% |
| -121 | 2 | 7.1% |
| -161 | 2 | 7.1% |
| -120 | 2 | 7.1% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 32.1% |
| ss2 | flkR | 9 | 32.1% |
| ss2 | ss1 | 5 | 17.9% |
| ss1 | flkR | 5 | 17.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 54 | ss1 | 173 | ss2 | +0.0110 | 0.2869 |
| 170 | ss2 | 52 | ss1 | +0.0082 | 0.1517 |
| 171 | ss2 | 51 | ss1 | +0.0063 | 0.1704 |
| 52 | ss1 | 170 | ss2 | +0.0061 | 0.1341 |
| 56 | ss1 | 173 | ss2 | +0.0036 | 0.1334 |

### L27 H15 — Rank #11

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 14  |  total attr: +0.0167

**Key mass** (top-1=30%, top-2=45%, top-3=54%)  [DISTR(A56/I172/L54/F170/V53)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 56 | ss1 | +0.0050 | 30.1% |
| 172 | ss2 | +0.0025 | 15.2% |
| 54 | ss1 | +0.0015 | 9.2% |
| 170 | ss2 | +0.0014 | 8.2% |
| 53 | ss1 | +0.0013 | 7.7% |

**Query mass** (top-1=30%, top-2=48%, top-3=57%)  [DISTR(I173/D51/F170/A56/H52)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0050 | 30.1% |
| 51 | ss1 | +0.0030 | 17.7% |
| 170 | ss2 | +0.0015 | 9.2% |
| 56 | ss1 | +0.0014 | 8.2% |
| 52 | ss1 | +0.0014 | 8.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -121 | 2 | 14.3% |
| +119 | 2 | 14.3% |
| +117 | 1 | 7.1% |
| +116 | 1 | 7.1% |
| -118 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 42.9% |
| ss2 | ss1 | 5 | 35.7% |
| ss2 | flkR | 2 | 14.3% |
| ss1 | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | ss2 | 56 | ss1 | +0.0050 | 0.1337 |
| 51 | ss1 | 172 | ss2 | +0.0025 | 0.0696 |
| 170 | ss2 | 54 | ss1 | +0.0015 | 0.0419 |
| 52 | ss1 | 170 | ss2 | +0.0014 | 0.0193 |
| 172 | ss2 | 53 | ss1 | +0.0013 | 0.2062 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 42  |  total attr: +0.0531

**Key mass** (top-1=17%, top-2=29%, top-3=38%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0089 | 16.8% |
| 52 | ss1 | +0.0066 | 12.4% |
| 171 | ss2 | +0.0045 | 8.5% |
| 170 | ss2 | +0.0038 | 7.1% |
| 32 | flkL | +0.0032 | 6.1% |

**Query mass** (top-1=19%, top-2=33%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 58 | ss1 | +0.0099 | 18.5% |
| 173 | ss2 | +0.0079 | 14.8% |
| 52 | ss1 | +0.0057 | 10.8% |
| 178 | ss2 | +0.0054 | 10.2% |
| 170 | ss2 | +0.0048 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +119 | 2 | 4.8% |
| -119 | 2 | 4.8% |
| -28 | 2 | 4.8% |
| -120 | 1 | 2.4% |
| +118 | 1 | 2.4% |

**Region-pair profile** (q→k)  (top=17%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 16.7% |
| ss2 | flkR | 7 | 16.7% |
| ss2 | other | 7 | 16.7% |
| ss2 | ss1 | 6 | 14.3% |
| ss2 | flkL | 6 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 58 | ss1 | 178 | ss2 | +0.0089 | 0.1011 |
| 170 | ss2 | 52 | ss1 | +0.0038 | 0.1692 |
| 52 | ss1 | 170 | ss2 | +0.0034 | 0.1309 |
| 176 | ss2 | 32 | flkL | +0.0032 | 0.3458 |
| 172 | ss2 | 39 | flkL | +0.0028 | 0.5167 |

### L30 H1 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0092

**Key mass** (top-1=33%, top-2=52%, top-3=69%)  [DISTR(I172/H52/I173/A56)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.0030 | 32.9% |
| 52 | ss1 | +0.0017 | 18.6% |
| 173 | ss2 | +0.0016 | 17.4% |
| 56 | ss1 | +0.0013 | 14.4% |
| 53 | ss1 | +0.0005 | 5.9% |

**Query mass** (top-1=31%, top-2=55%, top-3=74%)  [DISTR(L54/V53/F170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 54 | ss1 | +0.0028 | 31.0% |
| 53 | ss1 | +0.0022 | 24.3% |
| 170 | ss2 | +0.0017 | 18.6% |
| 173 | ss2 | +0.0013 | 14.4% |
| 174 | ss2 | +0.0005 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 2 | 25.0% |
| -118 | 2 | 25.0% |
| +118 | 1 | 12.5% |
| +117 | 1 | 12.5% |
| +121 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 62.5% |
| ss2 | ss1 | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 53 | ss1 | 172 | ss2 | +0.0022 | 0.4412 |
| 170 | ss2 | 52 | ss1 | +0.0017 | 0.0323 |
| 54 | ss1 | 173 | ss2 | +0.0016 | 0.0344 |
| 173 | ss2 | 56 | ss1 | +0.0013 | 0.0730 |
| 54 | ss1 | 172 | ss2 | +0.0008 | 0.0349 |

### L30 H13 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.0118

**Key mass** (top-1=33%, top-2=57%, top-3=69%)  [DISTR(F170/I173/F178/L176)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | ss2 | +0.0039 | 32.7% |
| 173 | ss2 | +0.0029 | 24.2% |
| 178 | ss2 | +0.0015 | 12.5% |
| 176 | ss2 | +0.0010 | 8.2% |
| 58 | ss1 | +0.0010 | 8.2% |

**Query mass** (top-1=34%, top-2=54%, top-3=67%)  [DISTR(L54/H52/F178/P58)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 54 | ss1 | +0.0040 | 33.9% |
| 52 | ss1 | +0.0024 | 20.4% |
| 178 | ss2 | +0.0015 | 12.9% |
| 58 | ss1 | +0.0015 | 12.5% |
| 173 | ss2 | +0.0009 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 9.1% |
| -119 | 1 | 9.1% |
| -120 | 1 | 9.1% |
| -116 | 1 | 9.1% |
| -122 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 63.6% |
| ss2 | ss1 | 2 | 18.2% |
| ss2 | ss2 | 1 | 9.1% |
| ss1 | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 52 | ss1 | 170 | ss2 | +0.0024 | 0.1088 |
| 54 | ss1 | 173 | ss2 | +0.0016 | 0.0618 |
| 58 | ss1 | 178 | ss2 | +0.0015 | 0.0287 |
| 54 | ss1 | 170 | ss2 | +0.0015 | 0.0626 |
| 54 | ss1 | 176 | ss2 | +0.0010 | 0.1156 |

### L32 H13 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 16  |  total attr: +0.0236

**Key mass** (top-1=36%, top-2=48%, top-3=59%)  [DISTR(F178/F170/I173/L176/L55)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0084 | 35.6% |
| 170 | ss2 | +0.0030 | 12.6% |
| 173 | ss2 | +0.0026 | 11.1% |
| 176 | ss2 | +0.0022 | 9.1% |
| 55 | ss1 | +0.0019 | 8.0% |

**Query mass** (top-1=36%, top-2=47%, top-3=55%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 58 | ss1 | +0.0084 | 35.6% |
| 54 | ss1 | +0.0026 | 11.1% |
| 52 | ss1 | +0.0019 | 7.9% |
| 56 | ss1 | +0.0015 | 6.4% |
| 178 | ss2 | +0.0015 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 3 | 18.8% |
| +120 | 2 | 12.5% |
| +121 | 2 | 12.5% |
| +119 | 2 | 12.5% |
| -120 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 50.0% |
| ss2 | ss1 | 8 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 58 | ss1 | 178 | ss2 | +0.0084 | 0.0769 |
| 52 | ss1 | 170 | ss2 | +0.0019 | 0.0237 |
| 54 | ss1 | 173 | ss2 | +0.0015 | 0.0298 |
| 178 | ss2 | 58 | ss1 | +0.0015 | 0.0135 |
| 55 | ss1 | 176 | ss2 | +0.0014 | 0.1209 |

### L32 H18 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 22  |  total attr: +0.0516

**Key mass** (top-1=15%, top-2=29%, top-3=42%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 171 | ss2 | +0.0076 | 14.8% |
| 56 | ss1 | +0.0074 | 14.4% |
| 173 | ss2 | +0.0068 | 13.1% |
| 170 | ss2 | +0.0060 | 11.7% |
| 54 | ss1 | +0.0056 | 10.8% |

**Query mass** (top-1=16%, top-2=32%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 54 | ss1 | +0.0083 | 16.2% |
| 170 | ss2 | +0.0083 | 16.1% |
| 173 | ss2 | +0.0065 | 12.5% |
| 51 | ss1 | +0.0062 | 12.0% |
| 58 | ss1 | +0.0051 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 4 | 18.2% |
| +119 | 4 | 18.2% |
| -120 | 2 | 9.1% |
| +121 | 2 | 9.1% |
| -117 | 2 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 50.0% |
| ss1 | ss2 | 11 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | ss2 | 56 | ss1 | +0.0065 | 0.0930 |
| 51 | ss1 | 171 | ss2 | +0.0062 | 0.0524 |
| 170 | ss2 | 54 | ss1 | +0.0056 | 0.0974 |
| 58 | ss1 | 178 | ss2 | +0.0051 | 0.0286 |
| 54 | ss1 | 173 | ss2 | +0.0041 | 0.0493 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #7 | L4 | H8 | 2 | +0.0183 | SINGLE-ANCHOR | Q29 | SINGLE-ANCHOR | G62 |  |  |
| #19 | L5 | H19 | 26 | +0.0606 | SINGLE-ANCHOR | G62 | DISTRIBUTED | F106/I107/A218 |  |  |
| #22 | L7 | H4 | 63 | +0.0410 | DISTRIBUTED | T151/F150/V153/L152/P149 | DISTRIBUTED |  |  |  |
| #27 | L7 | H6 | 8 | +0.0040 | DISTRIBUTED | N279/A280/A39/M45 | DUAL-ANCHOR | A218/F106 |  |  |
| #16 | L11 | H16 | 18 | +0.0130 | MULTI-ANCHOR |  | DISTRIBUTED |  |  |  |
| #20 | L13 | H7 | 35 | +0.0242 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #3 | L13 | H8 | 22 | +0.1015 | SINGLE-ANCHOR | A218 | DISTRIBUTED | F150/I173/T151/F170 |  |  |
| #4 | L13 | H12 | 36 | +0.0788 | SINGLE-ANCHOR | A218 | DISTRIBUTED |  |  |  |
| #10 | L13 | H19 | 17 | +0.0328 | SINGLE-ANCHOR | A218 | SINGLE-ANCHOR | F150 |  |  |
| #8 | L14 | H9 | 55 | +0.0548 | DUAL-ANCHOR | A218/L55 | DISTRIBUTED |  |  |  |
| #29 | L15 | H2 | 12 | +0.0243 | SINGLE-ANCHOR | A218 | DISTRIBUTED | L174/I173/G171 |  | ss2→flkR |
| #24 | L15 | H4 | 19 | +0.0236 | SINGLE-ANCHOR | A218 | DISTRIBUTED |  |  | CROSS:ss1→flkR |
| #25 | L15 | H6 | 23 | +0.0283 | MULTI-ANCHOR |  | DISTRIBUTED | I173/L174/F178/A218/L176 |  |  |
| #13 | L16 | H7 | 81 | +0.1147 | SINGLE-ANCHOR | A218 | DISTRIBUTED |  |  |  |
| #12 | L16 | H18 | 19 | +0.0445 | SINGLE-ANCHOR | L174 | DISTRIBUTED | A218/F150/T151 |  |  |
| #23 | L17 | H3 | 36 | +0.0392 | SINGLE-ANCHOR | A218 | DISTRIBUTED |  |  | CROSS:flkL→flkR |
| #9 | L17 | H19 | 9 | +0.0538 | SINGLE-ANCHOR | A218 | SINGLE-ANCHOR | T214 |  |  |
| #14 | L18 | H1 | 36 | +0.0353 | DISTRIBUTED | A218/G213/F150/T151 | DISTRIBUTED | H52/F170/L54/V53/I173 |  |  |
| #26 | L19 | H1 | 15 | +0.0162 | DUAL-ANCHOR | F106/I107 | DUAL-ANCHOR | F170/I173 |  |  |
| #28 | L19 | H9 | 17 | +0.0148 | DUAL-ANCHOR | G213/A218 | DISTRIBUTED |  |  | CROSS:ss1→flkR |
| #21 | L20 | H1 | 17 | +0.0219 | DUAL-ANCHOR | A218/L184 | DISTRIBUTED |  |  | INTRA:flkR |
| #18 | L20 | H5 | 12 | +0.0208 | SINGLE-ANCHOR | T180 | DISTRIBUTED | I173/F170/R167 |  | ss2→flkR |
| #30 | L21 | H17 | 14 | +0.0145 | DUAL-ANCHOR | F106/I107 | DISTRIBUTED | A56/H52/G57 |  |  |
| #2 | L26 | H16 | 28 | +0.0515 | DISTRIBUTED | I173/H52/D51/F170/G213 | DISTRIBUTED | L54/F170/H52/G171 |  |  |
| #11 | L27 | H15 | 14 | +0.0167 | DISTRIBUTED | A56/I172/L54/F170/V53 | DISTRIBUTED | I173/D51/F170/A56/H52 |  | CROSS:ss1→ss2 |
| #6 | L29 | H18 | 42 | +0.0531 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #17 | L30 | H1 | 8 | +0.0092 | DISTRIBUTED | I172/H52/I173/A56 | DISTRIBUTED | L54/V53/F170 | CROSS_SSE | CROSS:ss1→ss2 |
| #15 | L30 | H13 | 11 | +0.0118 | DISTRIBUTED | F170/I173/F178/L176 | DISTRIBUTED | L54/H52/F178/P58 |  | CROSS:ss1→ss2 |
| #5 | L32 | H13 | 16 | +0.0236 | DISTRIBUTED | F178/F170/I173/L176/L55 | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #1 | L32 | H18 | 22 | +0.0516 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
