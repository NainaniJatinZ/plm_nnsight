# Contact Pattern Analysis: 3OKPA

Generated: 2026-03-22 21:41:44   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3OKPA |
| Contact pair | (219, 336) |
| ss1 | [214, 225) |
| ss2 | [331, 342) |
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
| Clean metric | 0.8964 |
| Corrupt metric | 0.1103 |
| Gap | 0.7861 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 80.24% |
| positive IE | 115 | 73.02% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L6 | H0 | +0.5582 |
| 2 | L8 | H12 | +0.3822 |
| 3 | L32 | H13 | +0.1996 |
| 4 | L32 | H18 | +0.1318 |
| 5 | L10 | H6 | +0.1304 |
| 6 | L29 | H18 | +0.1260 |
| 7 | L10 | H9 | +0.1040 |
| 8 | L0 | H9 | +0.0819 |
| 9 | L13 | H7 | +0.0764 |
| 10 | L11 | H11 | +0.0612 |
| 11 | L31 | H17 | +0.0527 |
| 12 | L13 | H18 | +0.0404 |
| 13 | L16 | H14 | +0.0396 |
| 14 | L11 | H6 | +0.0387 |
| 15 | L28 | H4 | +0.0386 |
| 16 | L6 | H19 | +0.0367 |
| 17 | L12 | H16 | +0.0363 |
| 18 | L12 | H4 | +0.0357 |
| 19 | L30 | H13 | +0.0354 |
| 20 | L9 | H3 | +0.0345 |
| 21 | L27 | H15 | +0.0332 |
| 22 | L16 | H4 | +0.0322 |
| 23 | L13 | H2 | +0.0308 |
| 24 | L26 | H16 | +0.0306 |
| 25 | L0 | H19 | +0.0296 |
| 26 | L14 | H12 | +0.0287 |
| 27 | L14 | H1 | +0.0277 |
| 28 | L5 | H13 | +0.0276 |
| 29 | L9 | H13 | +0.0259 |
| 30 | L11 | H16 | +0.0257 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | -0.00% |
| 3 | 0.83% |
| 4 | 3.40% |
| 5 | 3.57% |
| 6 | 5.06% |
| 7 | 6.58% |
| 8 | 7.62% |
| 9 | 7.69% |
| 10 | 7.70% |
| 20 | 13.41% |
| 80 | 44.90% |
| 450 | 112.94% |

## Cell Attribution Analysis

Total cells: 15,965,282

- Positive: 8,017,743
- Negative: 7,944,393

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000020 | 1,596,529 |
| 95th | +0.00000064 | 798,265 |
| 99th | +0.00000574 | 159,654 |
| 99.5th | +0.00001276 | 79,827 |
| 99.9th | +0.00007091 | 15,966 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H0 | 200 | flkL | 143 | other | +0.165916 | 0.346391 |
| L10 | H6 | 219 | ss1 | 200 | flkL | +0.096589 | 0.352474 |
| L12 | H16 | 143 | other | 200 | flkL | +0.058424 | 0.565531 |
| L32 | H13 | 331 | ss2 | 221 | ss1 | +0.046503 | 0.322498 |
| L12 | H4 | 143 | other | 200 | flkL | +0.045509 | 0.594699 |
| L1 | H1 | 143 | other | 146 | flkL | +0.044537 | 0.096905 |
| L28 | H4 | 221 | ss1 | 218 | ss1 | +0.037015 | 0.598380 |
| L4 | H19 | 143 | other | 141 | other | +0.031741 | 0.130293 |
| L9 | H3 | 219 | ss1 | 200 | flkL | +0.030402 | 0.255017 |
| L32 | H18 | 333 | ss2 | 214 | ss1 | +0.027812 | 0.138003 |
| L13 | H18 | 327 | other | 200 | flkL | +0.025829 | 0.555306 |
| L30 | H12 | 221 | ss1 | 218 | ss1 | +0.025041 | 0.540980 |
| L12 | H16 | 293 | other | 200 | flkL | +0.024408 | 0.689272 |
| L12 | H16 | 292 | other | 200 | flkL | +0.024097 | 0.713868 |
| L10 | H14 | 337 | ss2 | 200 | flkL | +0.024070 | 0.316406 |
| L13 | H7 | 225 | other | 202 | flkL | +0.024011 | 0.433119 |
| L14 | H1 | 327 | other | 200 | flkL | +0.023398 | 0.193339 |
| L1 | H8 | 141 | other | 145 | flkL | +0.023133 | 0.247199 |
| L10 | H9 | 200 | flkL | 200 | flkL | +0.022669 | 0.098125 |
| L32 | H13 | 331 | ss2 | 218 | ss1 | +0.022413 | 0.334797 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L4 | H19 | 143 | other | 142 | other | -0.010522 | 0.081813 |
| L21 | H11 | 211 | flkL | 219 | ss1 | -0.010736 | 0.504207 |
| L1 | H1 | 142 | other | 145 | flkL | -0.010785 | 0.103500 |
| L13 | H18 | 328 | other | 200 | flkL | -0.011476 | 0.546024 |
| L13 | H7 | 225 | other | 200 | flkL | -0.013101 | 0.296526 |
| L25 | H8 | 214 | ss1 | 211 | flkL | -0.013304 | 0.494574 |
| L29 | H18 | 221 | ss1 | 338 | ss2 | -0.014565 | 0.381125 |
| L14 | H10 | 327 | other | 371 | flkR | -0.017682 | 0.165670 |
| L12 | H10 | 327 | other | 219 | ss1 | -0.018621 | 0.124426 |
| L14 | H9 | 228 | other | 200 | flkL | -0.019160 | 0.342823 |
| L10 | H14 | 371 | flkR | 200 | flkL | -0.020667 | 0.378428 |
| L12 | H16 | 157 | flkL | 200 | flkL | -0.021469 | 0.475671 |
| L13 | H14 | 228 | other | 200 | flkL | -0.022097 | 0.630482 |
| L13 | H14 | 225 | other | 200 | flkL | -0.023474 | 0.562741 |
| L30 | H12 | 331 | ss2 | 334 | ss2 | -0.023722 | 0.224278 |
| L6 | H17 | 144 | other | 144 | other | -0.031535 | 0.347546 |
| L14 | H9 | 327 | other | 200 | flkL | -0.034503 | 0.165047 |
| L14 | H9 | 225 | other | 200 | flkL | -0.044108 | 0.347346 |
| L1 | H1 | 143 | other | 145 | flkL | -0.084673 | 0.168296 |
| L0 | H19 | 145 | flkL | 145 | flkL | -0.301326 | 0.984049 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.1103 | 0.00% |
| 10 | 10 | 10 | 0.1105 | 0.02% |
| 20 | 20 | 17 | 0.1107 | 0.04% |
| 50 | 50 | 33 | 0.1110 | 0.09% |
| 100 | 100 | 53 | 0.1113 | 0.13% |
| 200 | 200 | 74 | 0.1149 | 0.58% |
| 500 | 500 | 104 | 0.1510 | 5.17% |
| 1000 | 1,000 | 111 | 0.2024 | 11.71% |
| 2000 | 2,000 | 113 | 0.2111 | 12.82% |
| 5000 | 5,000 | 115 | 0.2980 | 23.87% |
| 10000 | 10,000 | 115 | 0.3898 | 35.55% |
| 20000 | 20,000 | 115 | 0.4548 | 43.82% |
| 50000 | 50,000 | 115 | 0.5090 | 50.72% |

## Motif Analysis

### L0 H9 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 39  |  total attr: +0.0986

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 145 | flkL | +0.0986 | 100.0% |

**Query mass** (top-1=9%, top-2=15%, top-3=20%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0084 | 8.5% |
| 150 | flkL | +0.0059 | 6.0% |
| 143 | other | +0.0049 | 5.0% |
| 164 | flkL | +0.0047 | 4.8% |
| 202 | flkL | +0.0046 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +55 | 1 | 2.6% |
| +5 | 1 | 2.6% |
| -2 | 1 | 2.6% |
| +19 | 1 | 2.6% |
| +57 | 1 | 2.6% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=90%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 35 | 89.7% |
| other | flkL | 2 | 5.1% |
| ss1 | flkL | 2 | 5.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 145 | flkL | +0.0084 | 0.0033 |
| 150 | flkL | 145 | flkL | +0.0059 | 0.0078 |
| 143 | other | 145 | flkL | +0.0049 | 0.0077 |
| 164 | flkL | 145 | flkL | +0.0047 | 0.0057 |
| 202 | flkL | 145 | flkL | +0.0046 | 0.0032 |

### L0 H19 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | ss1→flkL  |  cells: 2  |  total attr: +0.0023

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 145 | flkL | +0.0023 | 100.0% |

**Query mass** (top-1=51%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 220 | ss1 | +0.0012 | 50.6% |
| 204 | flkL | +0.0012 | 49.4% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +75 | 1 | 50.0% |
| +59 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 1 | 50.0% |
| flkL | flkL | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 220 | ss1 | 145 | flkL | +0.0012 | 0.0032 |
| 204 | flkL | 145 | flkL | +0.0012 | 0.0025 |

### L5 H13 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 4  |  total attr: +0.0330

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 337 | ss2 | +0.0330 | 100.0% |

**Query mass** (top-1=42%, top-2=80%, top-3=95%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 293 | other | +0.0138 | 42.0% |
| 292 | other | +0.0124 | 37.6% |
| 294 | other | +0.0052 | 15.7% |
| 299 | other | +0.0016 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -44 | 1 | 25.0% |
| -45 | 1 | 25.0% |
| -43 | 1 | 25.0% |
| -38 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 293 | other | 337 | ss2 | +0.0138 | 0.0128 |
| 292 | other | 337 | ss2 | +0.0124 | 0.0129 |
| 294 | other | 337 | ss2 | +0.0052 | 0.0121 |
| 299 | other | 337 | ss2 | +0.0016 | 0.0145 |

### L6 H0 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 4  |  total attr: +0.1724

**Key mass** (top-1=96%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 143 | other | +0.1659 | 96.2% |
| 152 | flkL | +0.0027 | 1.6% |
| 153 | flkL | +0.0019 | 1.1% |
| 155 | flkL | +0.0019 | 1.1% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.1724 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 1 | 25.0% |
| +48 | 1 | 25.0% |
| +47 | 1 | 25.0% |
| +45 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 3 | 75.0% |
| flkL | other | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 143 | other | +0.1659 | 0.3464 |
| 200 | flkL | 152 | flkL | +0.0027 | 0.0135 |
| 200 | flkL | 153 | flkL | +0.0019 | 0.0071 |
| 200 | flkL | 155 | flkL | +0.0019 | 0.0090 |

### L6 H19 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.0078

**Key mass** (top-1=68%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 143 | other | +0.0053 | 67.9% |
| -1 | other | +0.0025 | 32.1% |

**Query mass** (top-1=84%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0066 | 84.0% |
| 292 | other | +0.0012 | 16.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 1 | 33.3% |
| +201 | 1 | 33.3% |
| +293 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 2 | 66.7% |
| other | other | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 143 | other | +0.0053 | 0.0282 |
| 200 | flkL | -1 | other | +0.0013 | 0.0296 |
| 292 | other | -1 | other | +0.0012 | 0.0219 |

### L8 H12 — Rank #2

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 29  |  total attr: +0.1377

**Key mass** (top-1=14%, top-2=28%, top-3=39%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 293 | other | +0.0197 | 14.3% |
| 292 | other | +0.0183 | 13.3% |
| 200 | flkL | +0.0163 | 11.8% |
| 294 | other | +0.0109 | 7.9% |
| 276 | other | +0.0066 | 4.8% |

**Query mass** (top-1=88%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.1214 | 88.2% |
| 143 | other | +0.0163 | 11.8% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -93 | 1 | 3.4% |
| -92 | 1 | 3.4% |
| -57 | 1 | 3.4% |
| -94 | 1 | 3.4% |
| -76 | 1 | 3.4% |

**Region-pair profile** (q→k)  (top=79%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 23 | 79.3% |
| flkL | flkR | 3 | 10.3% |
| other | flkL | 1 | 3.4% |
| flkL | ss2 | 1 | 3.4% |
| flkL | flkL | 1 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 293 | other | +0.0197 | 0.0425 |
| 200 | flkL | 292 | other | +0.0183 | 0.0418 |
| 143 | other | 200 | flkL | +0.0163 | 0.1363 |
| 200 | flkL | 294 | other | +0.0109 | 0.0246 |
| 200 | flkL | 276 | other | +0.0066 | 0.0274 |

### L9 H3 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 7  |  total attr: +0.0441

**Key mass** (top-1=96%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0421 | 95.6% |
| 223 | ss1 | +0.0019 | 4.4% |

**Query mass** (top-1=69%, top-2=77%, top-3=83%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss1 | +0.0304 | 69.0% |
| 225 | other | +0.0033 | 7.6% |
| 214 | ss1 | +0.0027 | 6.2% |
| 215 | ss1 | +0.0025 | 5.6% |
| 200 | flkL | +0.0019 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +19 | 1 | 14.3% |
| +25 | 1 | 14.3% |
| +14 | 1 | 14.3% |
| +15 | 1 | 14.3% |
| -23 | 1 | 14.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 3 | 42.9% |
| flkL | flkL | 2 | 28.6% |
| other | flkL | 1 | 14.3% |
| flkL | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 219 | ss1 | 200 | flkL | +0.0304 | 0.2550 |
| 225 | other | 200 | flkL | +0.0033 | 0.0926 |
| 214 | ss1 | 200 | flkL | +0.0027 | 0.2329 |
| 215 | ss1 | 200 | flkL | +0.0025 | 0.2152 |
| 200 | flkL | 223 | ss1 | +0.0019 | 0.0179 |

### L9 H13 — Rank #29

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 6  |  total attr: +0.0241

**Key mass** (top-1=31%, top-2=60%, top-3=78%)  [DISTR(R153/Q148/R188)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | flkL | +0.0076 | 31.3% |
| 148 | flkL | +0.0070 | 28.9% |
| 188 | flkL | +0.0042 | 17.5% |
| 155 | flkL | +0.0021 | 8.7% |
| 184 | flkL | +0.0018 | 7.5% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0241 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +47 | 1 | 16.7% |
| +52 | 1 | 16.7% |
| +12 | 1 | 16.7% |
| +45 | 1 | 16.7% |
| +16 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 6 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 153 | flkL | +0.0076 | 0.0155 |
| 200 | flkL | 148 | flkL | +0.0070 | 0.0439 |
| 200 | flkL | 188 | flkL | +0.0042 | 0.0140 |
| 200 | flkL | 155 | flkL | +0.0021 | 0.0095 |
| 200 | flkL | 184 | flkL | +0.0018 | 0.0065 |

### L10 H6 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 4  |  total attr: +0.1021

**Key mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0991 | 97.1% |
| 143 | other | +0.0029 | 2.9% |

**Query mass** (top-1=95%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss1 | +0.0966 | 94.6% |
| 221 | ss1 | +0.0026 | 2.5% |
| 154 | flkL | +0.0015 | 1.5% |
| 157 | flkL | +0.0014 | 1.3% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +19 | 1 | 25.0% |
| +21 | 1 | 25.0% |
| +11 | 1 | 25.0% |
| +14 | 1 | 25.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 50.0% |
| flkL | other | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 219 | ss1 | 200 | flkL | +0.0966 | 0.3525 |
| 221 | ss1 | 200 | flkL | +0.0026 | 0.1308 |
| 154 | flkL | 143 | other | +0.0015 | 0.1077 |
| 157 | flkL | 143 | other | +0.0014 | 0.0769 |

### L10 H9 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.1257

**Key mass** (top-1=95%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.1199 | 95.4% |
| 293 | other | +0.0035 | 2.8% |
| 143 | other | +0.0023 | 1.9% |

**Query mass** (top-1=22%, top-2=35%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0273 | 21.7% |
| 337 | ss2 | +0.0162 | 12.9% |
| 143 | other | +0.0102 | 8.1% |
| 219 | ss1 | +0.0084 | 6.7% |
| 293 | other | +0.0073 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 3.7% |
| +137 | 1 | 3.7% |
| -57 | 1 | 3.7% |
| +19 | 1 | 3.7% |
| +93 | 1 | 3.7% |

**Region-pair profile** (q→k)  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 14 | 51.9% |
| ss1 | flkL | 5 | 18.5% |
| ss2 | flkL | 3 | 11.1% |
| flkL | other | 2 | 7.4% |
| flkL | flkL | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 200 | flkL | +0.0227 | 0.0981 |
| 337 | ss2 | 200 | flkL | +0.0162 | 0.2626 |
| 143 | other | 200 | flkL | +0.0090 | 0.1300 |
| 219 | ss1 | 200 | flkL | +0.0084 | 0.1915 |
| 293 | other | 200 | flkL | +0.0073 | 0.1655 |

### L11 H6 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | flkL→ss1  |  cells: 2  |  total attr: +0.0219

**Key mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | ss1 | +0.0208 | 94.8% |
| 284 | other | +0.0011 | 5.2% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0219 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -19 | 1 | 50.0% |
| -84 | 1 | 50.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 1 | 50.0% |
| flkL | other | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 219 | ss1 | +0.0208 | 0.4371 |
| 200 | flkL | 284 | other | +0.0011 | 0.0076 |

### L11 H11 — Rank #10

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.0264

**Key mass** (top-1=12%, top-2=21%, top-3=29%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 311 | other | +0.0031 | 11.6% |
| 205 | flkL | +0.0024 | 9.2% |
| 307 | other | +0.0023 | 8.6% |
| 306 | other | +0.0021 | 7.8% |
| 156 | flkL | +0.0020 | 7.6% |

**Query mass** (top-1=79%, top-2=88%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 327 | other | +0.0208 | 78.7% |
| 219 | ss1 | +0.0024 | 9.2% |
| 200 | flkL | +0.0020 | 7.6% |
| 337 | ss2 | +0.0012 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +44 | 2 | 12.5% |
| +14 | 1 | 6.2% |
| +20 | 1 | 6.2% |
| +21 | 1 | 6.2% |
| +19 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=81%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 13 | 81.2% |
| ss1 | flkL | 1 | 6.2% |
| flkL | flkL | 1 | 6.2% |
| ss2 | other | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 219 | ss1 | 205 | flkL | +0.0024 | 0.0275 |
| 327 | other | 307 | other | +0.0023 | 0.0068 |
| 327 | other | 306 | other | +0.0021 | 0.0060 |
| 200 | flkL | 156 | flkL | +0.0020 | 0.0341 |
| 327 | other | 308 | other | +0.0020 | 0.0060 |

### L11 H16 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 9  |  total attr: +0.0288

**Key mass** (top-1=77%, top-2=87%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0223 | 77.4% |
| 156 | flkL | +0.0028 | 9.9% |
| 219 | ss1 | +0.0022 | 7.6% |
| 201 | flkL | +0.0015 | 5.1% |

**Query mass** (top-1=47%, top-2=63%, top-3=74%)  [DISTR(L143/?-1/V222)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 143 | other | +0.0136 | 47.4% |
| -1 | other | +0.0045 | 15.7% |
| 222 | ss1 | +0.0031 | 10.7% |
| 200 | flkL | +0.0022 | 7.6% |
| 327 | other | +0.0015 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -57 | 1 | 11.1% |
| -201 | 1 | 11.1% |
| +22 | 1 | 11.1% |
| -19 | 1 | 11.1% |
| -13 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 55.6% |
| flkL | flkL | 2 | 22.2% |
| ss1 | flkL | 1 | 11.1% |
| flkL | ss1 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 143 | other | 200 | flkL | +0.0121 | 0.2682 |
| -1 | other | 200 | flkL | +0.0045 | 0.1308 |
| 222 | ss1 | 200 | flkL | +0.0031 | 0.1288 |
| 200 | flkL | 219 | ss1 | +0.0022 | 0.0785 |
| 143 | other | 156 | flkL | +0.0015 | 0.0591 |

### L12 H4 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 17  |  total attr: +0.1134

**Key mass** (top-1=94%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.1063 | 93.7% |
| 293 | other | +0.0033 | 2.9% |
| 294 | other | +0.0022 | 1.9% |
| 292 | other | +0.0016 | 1.4% |

**Query mass** (top-1=46%, top-2=63%, top-3=76%)  [DISTR(L143/K155/?-1)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 143 | other | +0.0526 | 46.4% |
| 155 | flkL | +0.0185 | 16.3% |
| -1 | other | +0.0147 | 13.0% |
| 170 | flkL | +0.0054 | 4.8% |
| 166 | flkL | +0.0049 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -57 | 1 | 5.9% |
| -45 | 1 | 5.9% |
| -201 | 1 | 5.9% |
| -30 | 1 | 5.9% |
| -34 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 12 | 70.6% |
| other | other | 3 | 17.6% |
| other | flkL | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 143 | other | 200 | flkL | +0.0455 | 0.5947 |
| 155 | flkL | 200 | flkL | +0.0185 | 0.4973 |
| -1 | other | 200 | flkL | +0.0147 | 0.2391 |
| 170 | flkL | 200 | flkL | +0.0054 | 0.3463 |
| 166 | flkL | 200 | flkL | +0.0049 | 0.5044 |

### L12 H16 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.1434

**Key mass** (top-1=95%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.1359 | 94.7% |
| 371 | flkR | +0.0058 | 4.0% |
| 337 | ss2 | +0.0018 | 1.2% |

**Query mass** (top-1=41%, top-2=58%, top-3=75%)  [DISTR(L143/I293/G292)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 143 | other | +0.0584 | 40.7% |
| 293 | other | +0.0244 | 17.0% |
| 292 | other | +0.0241 | 16.8% |
| 294 | other | +0.0096 | 6.7% |
| -1 | other | +0.0041 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -57 | 1 | 6.2% |
| +93 | 1 | 6.2% |
| +92 | 1 | 6.2% |
| +94 | 1 | 6.2% |
| -372 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 50.0% |
| ss1 | flkL | 3 | 18.8% |
| flkL | flkL | 2 | 12.5% |
| other | flkR | 1 | 6.2% |
| flkL | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 143 | other | 200 | flkL | +0.0584 | 0.5655 |
| 293 | other | 200 | flkL | +0.0244 | 0.6893 |
| 292 | other | 200 | flkL | +0.0241 | 0.7139 |
| 294 | other | 200 | flkL | +0.0096 | 0.6511 |
| -1 | other | 371 | flkR | +0.0041 | 0.1101 |

### L13 H2 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0364

**Key mass** (top-1=36%, top-2=58%, top-3=73%)  [DISTR(I200/M219/L337)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0130 | 35.8% |
| 219 | ss1 | +0.0081 | 22.3% |
| 337 | ss2 | +0.0055 | 15.1% |
| 197 | flkL | +0.0027 | 7.5% |
| 215 | ss1 | +0.0026 | 7.1% |

**Query mass** (top-1=47%, top-2=59%, top-3=67%)  [DISTR(I200/V222/A225/M219)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0171 | 47.1% |
| 222 | ss1 | +0.0042 | 11.5% |
| 225 | other | +0.0030 | 8.4% |
| 219 | ss1 | +0.0026 | 7.1% |
| 215 | ss1 | +0.0022 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 3 | 23.1% |
| +2 | 2 | 15.4% |
| +0 | 1 | 7.7% |
| +4 | 1 | 7.7% |
| -4 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 4 | 30.8% |
| flkL | flkL | 3 | 23.1% |
| other | ss2 | 3 | 23.1% |
| other | ss1 | 2 | 15.4% |
| ss2 | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | flkL | 200 | flkL | +0.0130 | 0.1976 |
| 222 | ss1 | 219 | ss1 | +0.0042 | 0.3227 |
| 200 | flkL | 197 | flkL | +0.0027 | 0.0789 |
| 219 | ss1 | 215 | ss1 | +0.0026 | 0.1434 |
| 215 | ss1 | 219 | ss1 | +0.0022 | 0.4164 |

### L13 H7 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.0855

**Key mass** (top-1=52%, top-2=81%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0442 | 51.7% |
| 202 | flkL | +0.0253 | 29.6% |
| 143 | other | +0.0035 | 4.1% |
| 148 | flkL | +0.0021 | 2.5% |
| 223 | ss1 | +0.0019 | 2.2% |

**Query mass** (top-1=28%, top-2=46%, top-3=61%)  [DISTR(A225/Q230/L231/I200/D331)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | other | +0.0240 | 28.1% |
| 230 | other | +0.0155 | 18.1% |
| 231 | other | +0.0124 | 14.4% |
| 200 | flkL | +0.0058 | 6.8% |
| 331 | ss2 | +0.0041 | 4.8% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 13.0% |
| +23 | 2 | 8.7% |
| +30 | 1 | 4.3% |
| +31 | 1 | 4.3% |
| +32 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 34.8% |
| ss1 | flkL | 5 | 21.7% |
| ss2 | other | 3 | 13.0% |
| flkL | flkL | 2 | 8.7% |
| flkL | other | 2 | 8.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | other | 202 | flkL | +0.0240 | 0.4331 |
| 230 | other | 200 | flkL | +0.0155 | 0.7014 |
| 231 | other | 200 | flkL | +0.0124 | 0.5049 |
| 232 | other | 200 | flkL | +0.0036 | 0.7497 |
| 215 | ss1 | 200 | flkL | +0.0021 | 0.2067 |

### L13 H18 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 25  |  total attr: +0.1372

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.1332 | 97.1% |
| 337 | ss2 | +0.0023 | 1.6% |
| -1 | other | +0.0017 | 1.3% |

**Query mass** (top-1=19%, top-2=32%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 327 | other | +0.0258 | 18.8% |
| 337 | ss2 | +0.0186 | 13.6% |
| 219 | ss1 | +0.0129 | 9.4% |
| 333 | ss2 | +0.0120 | 8.8% |
| 326 | other | +0.0075 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 2 | 8.0% |
| +127 | 1 | 4.0% |
| +137 | 1 | 4.0% |
| +19 | 1 | 4.0% |
| +133 | 1 | 4.0% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 32.0% |
| ss2 | flkL | 6 | 24.0% |
| ss1 | flkL | 4 | 16.0% |
| flkR | flkL | 4 | 16.0% |
| other | ss2 | 1 | 4.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 327 | other | 200 | flkL | +0.0258 | 0.5553 |
| 337 | ss2 | 200 | flkL | +0.0186 | 0.4953 |
| 219 | ss1 | 200 | flkL | +0.0129 | 0.3082 |
| 333 | ss2 | 200 | flkL | +0.0120 | 0.5450 |
| 326 | other | 200 | flkL | +0.0075 | 0.5171 |

### L14 H1 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 25  |  total attr: +0.1025

**Key mass** (top-1=77%, top-2=86%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0787 | 76.8% |
| 143 | other | +0.0097 | 9.5% |
| 293 | other | +0.0049 | 4.8% |
| 157 | flkL | +0.0044 | 4.3% |
| 294 | other | +0.0037 | 3.6% |

**Query mass** (top-1=30%, top-2=46%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 327 | other | +0.0310 | 30.2% |
| 331 | ss2 | +0.0164 | 16.0% |
| 225 | other | +0.0109 | 10.7% |
| 326 | other | +0.0060 | 5.9% |
| 325 | other | +0.0055 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +127 | 1 | 4.0% |
| +131 | 1 | 4.0% |
| +126 | 1 | 4.0% |
| +125 | 1 | 4.0% |
| +25 | 1 | 4.0% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 9 | 36.0% |
| ss2 | flkL | 5 | 20.0% |
| flkR | other | 4 | 16.0% |
| other | other | 3 | 12.0% |
| ss1 | flkL | 3 | 12.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 327 | other | 200 | flkL | +0.0234 | 0.1933 |
| 331 | ss2 | 200 | flkL | +0.0164 | 0.2548 |
| 326 | other | 200 | flkL | +0.0060 | 0.2043 |
| 325 | other | 200 | flkL | +0.0055 | 0.1333 |
| 225 | other | 200 | flkL | +0.0049 | 0.0823 |

### L14 H12 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 12  |  total attr: +0.0400

**Key mass** (top-1=92%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0368 | 92.0% |
| 337 | ss2 | +0.0020 | 5.0% |
| 333 | ss2 | +0.0012 | 3.1% |

**Query mass** (top-1=34%, top-2=49%, top-3=62%)  [DISTR(A225/R226/M219/A218)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | other | +0.0135 | 33.8% |
| 226 | other | +0.0059 | 14.8% |
| 219 | ss1 | +0.0053 | 13.3% |
| 218 | ss1 | +0.0034 | 8.5% |
| 223 | ss1 | +0.0026 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +25 | 1 | 8.3% |
| +26 | 1 | 8.3% |
| +19 | 1 | 8.3% |
| +23 | 1 | 8.3% |
| +18 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 33.3% |
| other | flkL | 3 | 25.0% |
| flkL | flkL | 3 | 25.0% |
| other | ss2 | 1 | 8.3% |
| ss1 | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | other | 200 | flkL | +0.0135 | 0.1838 |
| 226 | other | 200 | flkL | +0.0059 | 0.2163 |
| 219 | ss1 | 200 | flkL | +0.0053 | 0.4363 |
| 223 | ss1 | 200 | flkL | +0.0026 | 0.4716 |
| 218 | ss1 | 200 | flkL | +0.0022 | 0.4791 |

### L16 H4 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.0435

**Key mass** (top-1=79%, top-2=85%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | flkL | +0.0342 | 78.5% |
| 293 | other | +0.0030 | 6.9% |
| 201 | flkL | +0.0015 | 3.5% |
| 389 | flkR | +0.0014 | 3.2% |
| 202 | flkL | +0.0012 | 2.7% |

**Query mass** (top-1=39%, top-2=56%, top-3=63%)  [DISTR(S334/V325/D331/S363/L337)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 334 | ss2 | +0.0168 | 38.5% |
| 325 | other | +0.0074 | 17.0% |
| 331 | ss2 | +0.0031 | 7.2% |
| 363 | flkR | +0.0029 | 6.6% |
| 337 | ss2 | +0.0025 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +134 | 1 | 5.9% |
| +131 | 1 | 5.9% |
| +137 | 1 | 5.9% |
| +130 | 1 | 5.9% |
| +125 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 5 | 29.4% |
| other | flkL | 5 | 29.4% |
| flkR | other | 3 | 17.6% |
| flkR | flkL | 2 | 11.8% |
| other | flkR | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 334 | ss2 | 200 | flkL | +0.0168 | 0.3374 |
| 331 | ss2 | 200 | flkL | +0.0031 | 0.1413 |
| 337 | ss2 | 200 | flkL | +0.0025 | 0.1580 |
| 330 | other | 200 | flkL | +0.0024 | 0.2428 |
| 325 | other | 200 | flkL | +0.0022 | 0.0546 |

### L16 H14 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0316

**Key mass** (top-1=31%, top-2=60%, top-3=75%)  [DISTR(A218/S334/L337)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | ss1 | +0.0097 | 30.6% |
| 334 | ss2 | +0.0093 | 29.3% |
| 337 | ss2 | +0.0049 | 15.6% |
| 222 | ss1 | +0.0033 | 10.4% |
| 338 | ss2 | +0.0032 | 10.0% |

**Query mass** (top-1=39%, top-2=62%, top-3=78%)  [DISTR(V222/S334/M219)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 222 | ss1 | +0.0124 | 39.3% |
| 334 | ss2 | +0.0072 | 22.9% |
| 219 | ss1 | +0.0049 | 15.6% |
| 331 | ss2 | +0.0031 | 9.8% |
| 338 | ss2 | +0.0026 | 8.3% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 1 | 12.5% |
| -118 | 1 | 12.5% |
| +116 | 1 | 12.5% |
| +112 | 1 | 12.5% |
| -116 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 62.5% |
| ss1 | ss2 | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 222 | ss1 | 334 | ss2 | +0.0093 | 0.2509 |
| 219 | ss1 | 337 | ss2 | +0.0049 | 0.1487 |
| 334 | ss2 | 218 | ss1 | +0.0040 | 0.1816 |
| 334 | ss2 | 222 | ss1 | +0.0033 | 0.1112 |
| 222 | ss1 | 338 | ss2 | +0.0032 | 0.2083 |

### L26 H16 — Rank #24

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→ss1  |  cells: 4  |  total attr: +0.0163

**Key mass** (top-1=52%, top-2=76%, top-3=91%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 222 | ss1 | +0.0084 | 51.6% |
| 221 | ss1 | +0.0039 | 24.0% |
| 334 | ss2 | +0.0025 | 15.2% |
| 225 | other | +0.0015 | 9.1% |

**Query mass** (top-1=61%, top-2=85%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 334 | ss2 | +0.0099 | 60.7% |
| 331 | ss2 | +0.0039 | 24.0% |
| 222 | ss1 | +0.0025 | 15.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +112 | 1 | 25.0% |
| +110 | 1 | 25.0% |
| -112 | 1 | 25.0% |
| +109 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 50.0% |
| ss1 | ss2 | 1 | 25.0% |
| ss2 | other | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 334 | ss2 | 222 | ss1 | +0.0084 | 0.1135 |
| 331 | ss2 | 221 | ss1 | +0.0039 | 0.0533 |
| 222 | ss1 | 334 | ss2 | +0.0025 | 0.0541 |
| 334 | ss2 | 225 | other | +0.0015 | 0.0508 |

### L27 H15 — Rank #21

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | CROSS:ss1→ss2  |  cells: 7  |  total attr: +0.0217

**Key mass** (top-1=33%, top-2=58%, top-3=76%)  [DISTR(S334/L215/L333)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 334 | ss2 | +0.0072 | 33.0% |
| 215 | ss1 | +0.0054 | 24.7% |
| 333 | ss2 | +0.0039 | 18.0% |
| 199 | flkL | +0.0020 | 9.0% |
| 201 | flkL | +0.0017 | 8.0% |

**Query mass** (top-1=48%, top-2=66%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 222 | ss1 | +0.0105 | 48.3% |
| 215 | ss1 | +0.0039 | 18.0% |
| 337 | ss2 | +0.0032 | 14.8% |
| 333 | ss2 | +0.0021 | 9.9% |
| 221 | ss1 | +0.0020 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 1 | 14.3% |
| -118 | 1 | 14.3% |
| +122 | 1 | 14.3% |
| +118 | 1 | 14.3% |
| +22 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 3 | 42.9% |
| ss2 | ss1 | 2 | 28.6% |
| ss1 | flkL | 2 | 28.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 222 | ss1 | 334 | ss2 | +0.0072 | 0.0916 |
| 215 | ss1 | 333 | ss2 | +0.0039 | 0.1963 |
| 337 | ss2 | 215 | ss1 | +0.0032 | 0.0986 |
| 333 | ss2 | 215 | ss1 | +0.0021 | 0.0882 |
| 221 | ss1 | 199 | flkL | +0.0020 | 0.0723 |

### L28 H4 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 15  |  total attr: +0.0837

**Key mass** (top-1=63%, top-2=70%, top-3=77%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | ss1 | +0.0529 | 63.2% |
| 333 | ss2 | +0.0060 | 7.2% |
| 337 | ss2 | +0.0054 | 6.4% |
| 334 | ss2 | +0.0042 | 5.0% |
| 222 | ss1 | +0.0040 | 4.8% |

**Query mass** (top-1=44%, top-2=60%, top-3=68%)  [DISTR(Q221/V222/S214/I338)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.0370 | 44.2% |
| 222 | ss1 | +0.0128 | 15.3% |
| 214 | ss1 | +0.0072 | 8.7% |
| 338 | ss2 | +0.0061 | 7.3% |
| 331 | ss2 | +0.0060 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 53%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 4 | 26.7% |
| -4 | 4 | 26.7% |
| +3 | 3 | 20.0% |
| +4 | 3 | 20.0% |
| -2 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 40.0% |
| ss1 | ss1 | 5 | 33.3% |
| ss1 | flkL | 2 | 13.3% |
| other | ss1 | 1 | 6.7% |
| other | ss2 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 221 | ss1 | 218 | ss1 | +0.0370 | 0.5984 |
| 222 | ss1 | 218 | ss1 | +0.0128 | 0.3347 |
| 331 | ss2 | 333 | ss2 | +0.0060 | 0.0525 |
| 334 | ss2 | 337 | ss2 | +0.0042 | 0.0553 |
| 338 | ss2 | 341 | ss2 | +0.0032 | 0.2431 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.1440

**Key mass** (top-1=20%, top-2=39%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | ss1 | +0.0283 | 19.7% |
| 221 | ss1 | +0.0274 | 19.0% |
| 329 | other | +0.0125 | 8.7% |
| 338 | ss2 | +0.0111 | 7.7% |
| 347 | flkR | +0.0108 | 7.5% |

**Query mass** (top-1=28%, top-2=43%, top-3=57%)  [DISTR(D331/S214/Q221/V222/L333)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 331 | ss2 | +0.0403 | 28.0% |
| 214 | ss1 | +0.0223 | 15.5% |
| 221 | ss1 | +0.0201 | 14.0% |
| 222 | ss1 | +0.0163 | 11.3% |
| 333 | ss2 | +0.0129 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -116 | 3 | 9.7% |
| +110 | 2 | 6.5% |
| -115 | 2 | 6.5% |
| -113 | 2 | 6.5% |
| +113 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 22.6% |
| ss2 | ss1 | 6 | 19.4% |
| ss2 | flkL | 5 | 16.1% |
| ss1 | other | 3 | 9.7% |
| ss1 | flkR | 3 | 9.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 331 | ss2 | 221 | ss1 | +0.0217 | 0.3484 |
| 331 | ss2 | 218 | ss1 | +0.0168 | 0.2394 |
| 214 | ss1 | 329 | other | +0.0125 | 0.1475 |
| 221 | ss1 | 347 | flkR | +0.0108 | 0.1487 |
| 222 | ss1 | 337 | ss2 | +0.0084 | 0.2323 |

### L30 H13 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0300

**Key mass** (top-1=31%, top-2=58%, top-3=68%)  [DISTR(L333/Q221/D331/M367)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 333 | ss2 | +0.0093 | 31.0% |
| 221 | ss1 | +0.0081 | 27.2% |
| 331 | ss2 | +0.0029 | 9.6% |
| 367 | flkR | +0.0028 | 9.3% |
| 222 | ss1 | +0.0017 | 5.7% |

**Query mass** (top-1=27%, top-2=52%, top-3=65%)  [DISTR(S214/S334/A218/D331)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 214 | ss1 | +0.0080 | 26.5% |
| 334 | ss2 | +0.0075 | 25.0% |
| 218 | ss1 | +0.0041 | 13.8% |
| 331 | ss2 | +0.0032 | 10.6% |
| 221 | ss1 | +0.0029 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 1 | 7.7% |
| +113 | 1 | 7.7% |
| -115 | 1 | 7.7% |
| -110 | 1 | 7.7% |
| +110 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 38.5% |
| ss1 | ss2 | 3 | 23.1% |
| ss1 | flkR | 2 | 15.4% |
| ss1 | ss1 | 2 | 15.4% |
| ss2 | other | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 214 | ss1 | 333 | ss2 | +0.0064 | 0.1289 |
| 334 | ss2 | 221 | ss1 | +0.0042 | 0.1286 |
| 218 | ss1 | 333 | ss2 | +0.0029 | 0.3156 |
| 221 | ss1 | 331 | ss2 | +0.0029 | 0.0530 |
| 331 | ss2 | 221 | ss1 | +0.0020 | 0.0551 |

### L31 H17 — Rank #11

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0529

**Key mass** (top-1=25%, top-2=49%, top-3=62%)  [DISTR(?-1/Q221/D331/L215)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0132 | 25.0% |
| 221 | ss1 | +0.0128 | 24.2% |
| 331 | ss2 | +0.0067 | 12.7% |
| 215 | ss1 | +0.0061 | 11.5% |
| 342 | flkR | +0.0046 | 8.7% |

**Query mass** (top-1=26%, top-2=50%, top-3=66%)  [DISTR(Q221/S334/S214/L333)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.0139 | 26.3% |
| 334 | ss2 | +0.0124 | 23.4% |
| 214 | ss1 | +0.0087 | 16.4% |
| 333 | ss2 | +0.0061 | 11.5% |
| 338 | ss2 | +0.0039 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 2 | 12.5% |
| -110 | 1 | 6.2% |
| +118 | 1 | 6.2% |
| +215 | 1 | 6.2% |
| -180 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 25.0% |
| ss1 | flkR | 4 | 25.0% |
| ss1 | other | 3 | 18.8% |
| ss2 | other | 2 | 12.5% |
| ss1 | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 334 | ss2 | 221 | ss1 | +0.0106 | 0.4105 |
| 221 | ss1 | 331 | ss2 | +0.0067 | 0.1906 |
| 333 | ss2 | 215 | ss1 | +0.0061 | 0.2425 |
| 214 | ss1 | -1 | other | +0.0057 | 0.1958 |
| 214 | ss1 | 394 | flkR | +0.0030 | 0.0703 |

### L32 H13 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 14  |  total attr: +0.1407

**Key mass** (top-1=36%, top-2=56%, top-3=72%)  [DISTR(Q221/D331/A218)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.0510 | 36.2% |
| 331 | ss2 | +0.0274 | 19.5% |
| 218 | ss1 | +0.0236 | 16.8% |
| 222 | ss1 | +0.0139 | 9.9% |
| 334 | ss2 | +0.0120 | 8.5% |

**Query mass** (top-1=49%, top-2=65%, top-3=77%)  [DISTR(D331/Q221/V222)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 331 | ss2 | +0.0689 | 49.0% |
| 221 | ss1 | +0.0231 | 16.4% |
| 222 | ss1 | +0.0170 | 12.1% |
| 334 | ss2 | +0.0081 | 5.7% |
| 338 | ss2 | +0.0070 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 14.3% |
| -116 | 2 | 14.3% |
| +110 | 1 | 7.1% |
| +113 | 1 | 7.1% |
| -110 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 50.0% |
| ss1 | ss2 | 7 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 331 | ss2 | 221 | ss1 | +0.0465 | 0.3225 |
| 331 | ss2 | 218 | ss1 | +0.0224 | 0.3348 |
| 221 | ss1 | 331 | ss2 | +0.0220 | 0.1523 |
| 222 | ss1 | 334 | ss2 | +0.0106 | 0.1033 |
| 338 | ss2 | 222 | ss1 | +0.0070 | 0.2041 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0898

**Key mass** (top-1=31%, top-2=52%, top-3=73%)  [DISTR(S214/L333/S334)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 214 | ss1 | +0.0278 | 31.0% |
| 333 | ss2 | +0.0190 | 21.2% |
| 334 | ss2 | +0.0186 | 20.7% |
| 222 | ss1 | +0.0099 | 11.1% |
| 218 | ss1 | +0.0057 | 6.3% |

**Query mass** (top-1=31%, top-2=54%, top-3=75%)  [DISTR(L333/V222/S214)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 333 | ss2 | +0.0278 | 31.0% |
| 222 | ss1 | +0.0208 | 23.1% |
| 214 | ss1 | +0.0190 | 21.2% |
| 334 | ss2 | +0.0121 | 13.5% |
| 331 | ss2 | +0.0056 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -116 | 2 | 18.2% |
| +116 | 2 | 18.2% |
| +119 | 1 | 9.1% |
| -119 | 1 | 9.1% |
| -112 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 54.5% |
| ss1 | ss2 | 5 | 45.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 333 | ss2 | 214 | ss1 | +0.0278 | 0.1380 |
| 214 | ss1 | 333 | ss2 | +0.0190 | 0.0945 |
| 222 | ss1 | 334 | ss2 | +0.0170 | 0.1006 |
| 334 | ss2 | 222 | ss1 | +0.0084 | 0.0500 |
| 222 | ss1 | 338 | ss2 | +0.0038 | 0.0677 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #8 | L0 | H9 | 39 | +0.0986 | SINGLE-ANCHOR | Y145 | DISTRIBUTED |  |  | INTRA:flkL |
| #25 | L0 | H19 | 2 | +0.0023 | SINGLE-ANCHOR | Y145 | DUAL-ANCHOR | P220/S204 |  | ss1→flkL |
| #28 | L5 | H13 | 4 | +0.0330 | SINGLE-ANCHOR | L337 | DUAL-ANCHOR | I293/G292 |  |  |
| #1 | L6 | H0 | 4 | +0.1724 | SINGLE-ANCHOR | L143 | SINGLE-ANCHOR | I200 |  | INTRA:flkL |
| #16 | L6 | H19 | 3 | +0.0078 | SINGLE-ANCHOR | L143 | SINGLE-ANCHOR | I200 |  |  |
| #2 | L8 | H12 | 29 | +0.1377 | DISTRIBUTED |  | SINGLE-ANCHOR | I200 |  |  |
| #20 | L9 | H3 | 7 | +0.0441 | SINGLE-ANCHOR | I200 | SINGLE-ANCHOR | M219 |  | ss1→flkL |
| #29 | L9 | H13 | 6 | +0.0241 | DISTRIBUTED | R153/Q148/R188 | SINGLE-ANCHOR | I200 |  | INTRA:flkL |
| #5 | L10 | H6 | 4 | +0.1021 | SINGLE-ANCHOR | I200 | SINGLE-ANCHOR | M219 |  | ss1→flkL |
| #7 | L10 | H9 | 27 | +0.1257 | SINGLE-ANCHOR | I200 | DISTRIBUTED |  |  |  |
| #14 | L11 | H6 | 2 | +0.0219 | SINGLE-ANCHOR | M219 | SINGLE-ANCHOR | I200 |  | flkL→ss1 |
| #10 | L11 | H11 | 16 | +0.0264 | DISTRIBUTED |  | SINGLE-ANCHOR | G327 |  |  |
| #30 | L11 | H16 | 9 | +0.0288 | SINGLE-ANCHOR | I200 | DISTRIBUTED | L143/?-1/V222 |  |  |
| #18 | L12 | H4 | 17 | +0.1134 | SINGLE-ANCHOR | I200 | DISTRIBUTED | L143/K155/?-1 |  | INTRA:flkL |
| #17 | L12 | H16 | 16 | +0.1434 | SINGLE-ANCHOR | I200 | DISTRIBUTED | L143/I293/G292 |  |  |
| #23 | L13 | H2 | 13 | +0.0364 | DISTRIBUTED | I200/M219/L337 | DISTRIBUTED | I200/V222/A225/M219 |  |  |
| #9 | L13 | H7 | 23 | +0.0855 | DUAL-ANCHOR | I200/C202 | DISTRIBUTED | A225/Q230/L231/I200/D331 |  |  |
| #12 | L13 | H18 | 25 | +0.1372 | SINGLE-ANCHOR | I200 | DISTRIBUTED |  |  |  |
| #27 | L14 | H1 | 25 | +0.1025 | SINGLE-ANCHOR | I200 | DISTRIBUTED |  |  |  |
| #26 | L14 | H12 | 12 | +0.0400 | SINGLE-ANCHOR | I200 | DISTRIBUTED | A225/R226/M219/A218 |  |  |
| #22 | L16 | H4 | 17 | +0.0435 | SINGLE-ANCHOR | I200 | DISTRIBUTED | S334/V325/D331/S363/L337 |  |  |
| #13 | L16 | H14 | 8 | +0.0316 | DISTRIBUTED | A218/S334/L337 | DISTRIBUTED | V222/S334/M219 |  | CROSS:ss2→ss1 |
| #24 | L26 | H16 | 4 | +0.0163 | DUAL-ANCHOR | V222/Q221 | SINGLE-ANCHOR | S334 |  | CROSS:ss2→ss1 |
| #21 | L27 | H15 | 7 | +0.0217 | DISTRIBUTED | S334/L215/L333 | MULTI-ANCHOR |  |  | CROSS:ss1→ss2 |
| #15 | L28 | H4 | 15 | +0.0837 | SINGLE-ANCHOR | A218 | DISTRIBUTED | Q221/V222/S214/I338 | POSITIONAL | INTRA:ss2 |
| #6 | L29 | H18 | 31 | +0.1440 | DISTRIBUTED |  | DISTRIBUTED | D331/S214/Q221/V222/L333 |  |  |
| #19 | L30 | H13 | 13 | +0.0300 | DISTRIBUTED | L333/Q221/D331/M367 | DISTRIBUTED | S214/S334/A218/D331 |  |  |
| #11 | L31 | H17 | 16 | +0.0529 | DISTRIBUTED | ?-1/Q221/D331/L215 | DISTRIBUTED | Q221/S334/S214/L333 |  |  |
| #3 | L32 | H13 | 14 | +0.1407 | DISTRIBUTED | Q221/D331/A218 | DISTRIBUTED | D331/Q221/V222 |  | CROSS:ss2→ss1 |
| #4 | L32 | H18 | 11 | +0.0898 | DISTRIBUTED | S214/L333/S334 | DISTRIBUTED | L333/V222/S214 |  | CROSS:ss2→ss1 |
