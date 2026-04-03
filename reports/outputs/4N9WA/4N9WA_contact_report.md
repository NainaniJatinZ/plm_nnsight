# Contact Pattern Analysis: 4N9WA

Generated: 2026-03-26 00:43:56   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4N9WA |
| Contact pair | (214, 325) |
| ss1 | [209, 220) |
| ss2 | [320, 331) |
| Clean flank | 61 |
| Corrupt flank | 60 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.7791 |
| Corrupt metric | 0.0212 |
| Gap | 0.7578 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 76.15% |
| positive IE | 135 | 72.64% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L6 | H19 | +0.4738 |
| 2 | L29 | H18 | +0.2254 |
| 3 | L32 | H18 | +0.1922 |
| 4 | L32 | H13 | +0.1802 |
| 5 | L11 | H18 | +0.1405 |
| 6 | L9 | H14 | +0.1332 |
| 7 | L0 | H0 | +0.1039 |
| 8 | L8 | H14 | +0.0780 |
| 9 | L11 | H12 | +0.0780 |
| 10 | L9 | H18 | +0.0768 |
| 11 | L13 | H18 | +0.0748 |
| 12 | L11 | H4 | +0.0619 |
| 13 | L5 | H7 | +0.0601 |
| 14 | L14 | H9 | +0.0584 |
| 15 | L6 | H7 | +0.0574 |
| 16 | L11 | H10 | +0.0573 |
| 17 | L9 | H17 | +0.0563 |
| 18 | L13 | H2 | +0.0552 |
| 19 | L10 | H9 | +0.0551 |
| 20 | L11 | H15 | +0.0544 |
| 21 | L30 | H13 | +0.0538 |
| 22 | L7 | H7 | +0.0505 |
| 23 | L8 | H18 | +0.0501 |
| 24 | L9 | H8 | +0.0499 |
| 25 | L9 | H7 | +0.0496 |
| 26 | L27 | H15 | +0.0484 |
| 27 | L8 | H5 | +0.0444 |
| 28 | L13 | H7 | +0.0419 |
| 29 | L7 | H13 | +0.0416 |
| 30 | L8 | H11 | +0.0409 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | 0.02% |
| 3 | 0.13% |
| 4 | 0.23% |
| 5 | 0.23% |
| 6 | 0.22% |
| 7 | 0.30% |
| 8 | 0.37% |
| 9 | 0.36% |
| 10 | 0.36% |
| 20 | 1.24% |
| 80 | 31.01% |
| 450 | 113.91% |

## Cell Attribution Analysis

Total cells: 19,013,337

- Positive: 9,559,989
- Negative: 9,450,224

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H14 | 289 | other | 333 | flkR | +0.587844 | 0.291262 |
| L6 | H19 | 289 | other | 147 | other | +0.498898 | 0.693987 |
| L7 | H14 | 288 | other | 333 | flkR | +0.310147 | 0.311479 |
| L6 | H19 | 288 | other | 147 | other | +0.258384 | 0.694580 |
| L7 | H14 | 290 | other | 333 | flkR | +0.250412 | 0.298287 |
| L6 | H19 | 290 | other | 147 | other | +0.195310 | 0.694254 |
| L5 | H7 | 147 | other | 194 | flkL | +0.080607 | 0.068629 |
| L6 | H19 | 326 | ss2 | 147 | other | +0.054192 | 0.690730 |
| L6 | H19 | 217 | ss1 | 147 | other | +0.048293 | 0.607904 |
| L15 | H8 | 289 | other | 194 | flkL | +0.034564 | 0.674493 |
| L6 | H19 | 289 | other | -1 | other | +0.034409 | 0.151562 |
| L4 | H17 | 147 | other | 167 | flkL | +0.033558 | 0.038596 |
| L6 | H7 | 289 | other | 147 | other | +0.033220 | 0.152714 |
| L29 | H18 | 213 | ss1 | 323 | ss2 | +0.033127 | 0.321743 |
| L11 | H10 | 359 | flkR | 359 | flkR | +0.032738 | 0.486957 |
| L7 | H19 | 289 | other | 147 | other | +0.032635 | 0.110040 |
| L29 | H18 | 322 | ss2 | 213 | ss1 | +0.031160 | 0.264774 |
| L2 | H4 | 147 | other | 148 | flkL | +0.028944 | 0.094921 |
| L32 | H18 | 216 | ss1 | 327 | ss2 | +0.028483 | 0.154458 |
| L15 | H0 | 322 | ss2 | 207 | flkL | +0.028250 | 0.873787 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H19 | 325 | ss2 | 147 | other | -0.028930 | 0.646539 |
| L9 | H17 | 289 | other | 194 | flkL | -0.030840 | 0.434673 |
| L7 | H14 | 297 | other | 333 | flkR | -0.033132 | 0.393313 |
| L7 | H14 | 285 | other | 333 | flkR | -0.033915 | 0.340416 |
| L6 | H19 | 296 | other | 147 | other | -0.064824 | 0.676342 |
| L6 | H19 | 293 | other | 147 | other | -0.076204 | 0.685234 |
| L7 | H14 | 296 | other | 333 | flkR | -0.078449 | 0.410968 |
| L6 | H19 | 294 | other | 147 | other | -0.079398 | 0.683614 |
| L6 | H19 | 286 | other | 147 | other | -0.094569 | 0.700654 |
| L6 | H19 | 295 | other | 147 | other | -0.094622 | 0.680142 |
| L7 | H14 | 293 | other | 333 | flkR | -0.103175 | 0.359321 |
| L7 | H14 | 294 | other | 333 | flkR | -0.105037 | 0.389508 |
| L7 | H14 | 295 | other | 333 | flkR | -0.114287 | 0.404907 |
| L7 | H14 | 286 | other | 333 | flkR | -0.117663 | 0.378378 |
| L6 | H19 | 287 | other | 147 | other | -0.117943 | 0.698220 |
| L7 | H14 | 287 | other | 333 | flkR | -0.126355 | 0.368491 |
| L6 | H19 | 292 | other | 147 | other | -0.138447 | 0.690729 |
| L7 | H14 | 292 | other | 333 | flkR | -0.154853 | 0.325845 |
| L7 | H14 | 291 | other | 333 | flkR | -0.160647 | 0.312839 |
| L6 | H19 | 291 | other | 147 | other | -0.165267 | 0.694605 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0212 | 0.00% |
| 10 | 10 | 4 | 0.0212 | 0.00% |
| 20 | 20 | 12 | 0.0213 | 0.01% |
| 50 | 50 | 27 | 0.0213 | 0.01% |
| 100 | 100 | 46 | 0.0214 | 0.02% |
| 200 | 200 | 73 | 0.0214 | 0.03% |
| 500 | 500 | 101 | 0.0224 | 0.15% |
| 1000 | 1,000 | 120 | 0.0241 | 0.38% |
| 2000 | 2,000 | 131 | 0.0303 | 1.19% |
| 5000 | 5,000 | 133 | 0.0500 | 3.80% |
| 10000 | 10,000 | 135 | 0.0993 | 10.31% |
| 20000 | 20,000 | 135 | 0.2224 | 26.54% |
| 50000 | 50,000 | 135 | 0.3016 | 36.99% |

## Motif Analysis

### L0 H0 — Rank #7

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 2  |  total attr: +0.0045

**Key mass** (top-1=55%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 148 | flkL | +0.0025 | 55.1% |
| 178 | flkL | +0.0020 | 44.9% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 148 | flkL | +0.0045 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 50.0% |
| -30 | 1 | 50.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 148 | flkL | 148 | flkL | +0.0025 | 0.0175 |
| 148 | flkL | 178 | flkL | +0.0020 | 0.0119 |

### L5 H7 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0966

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | flkL | +0.0966 | 100.0% |

**Query mass** (top-1=83%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +0.0806 | 83.5% |
| 289 | other | +0.0081 | 8.4% |
| 288 | other | +0.0047 | 4.9% |
| 290 | other | +0.0031 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -47 | 1 | 25.0% |
| +95 | 1 | 25.0% |
| +94 | 1 | 25.0% |
| +96 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | other | 194 | flkL | +0.0806 | 0.0686 |
| 289 | other | 194 | flkL | +0.0081 | 0.0124 |
| 288 | other | 194 | flkL | +0.0047 | 0.0130 |
| 290 | other | 194 | flkL | +0.0031 | 0.0114 |

### L6 H7 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 8  |  total attr: +0.0809

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +0.0809 | 100.0% |

**Query mass** (top-1=41%, top-2=63%, top-3=79%)  [DISTR(A289/A288/G290)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0332 | 41.1% |
| 288 | other | +0.0181 | 22.4% |
| 290 | other | +0.0128 | 15.8% |
| 284 | other | +0.0041 | 5.1% |
| 283 | other | +0.0037 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +142 | 1 | 12.5% |
| +141 | 1 | 12.5% |
| +143 | 1 | 12.5% |
| +137 | 1 | 12.5% |
| +136 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 8 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 147 | other | +0.0332 | 0.1527 |
| 288 | other | 147 | other | +0.0181 | 0.1424 |
| 290 | other | 147 | other | +0.0128 | 0.1633 |
| 284 | other | 147 | other | +0.0041 | 0.1796 |
| 283 | other | 147 | other | +0.0037 | 0.1602 |

### L6 H19 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 109  |  total attr: +1.8004

**Key mass** (top-1=96%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +1.7223 | 95.7% |
| -1 | other | +0.0674 | 3.7% |
| 215 | ss1 | +0.0057 | 0.3% |
| 348 | flkR | +0.0027 | 0.2% |
| 196 | flkL | +0.0022 | 0.1% |

**Query mass** (top-1=30%, top-2=45%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.5368 | 29.8% |
| 288 | other | +0.2777 | 15.4% |
| 290 | other | +0.2076 | 11.5% |
| 326 | ss2 | +0.0542 | 3.0% |
| 217 | ss1 | +0.0483 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 4%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +73 | 2 | 1.8% |
| +74 | 2 | 1.8% |
| +95 | 2 | 1.8% |
| +142 | 1 | 0.9% |
| +141 | 1 | 0.9% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 49 | 45.0% |
| flkL | other | 25 | 22.9% |
| flkR | other | 22 | 20.2% |
| ss1 | other | 7 | 6.4% |
| ss2 | other | 2 | 1.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 147 | other | +0.4989 | 0.6940 |
| 288 | other | 147 | other | +0.2584 | 0.6946 |
| 290 | other | 147 | other | +0.1953 | 0.6943 |
| 326 | ss2 | 147 | other | +0.0542 | 0.6907 |
| 217 | ss1 | 147 | other | +0.0483 | 0.6079 |

### L7 H7 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 7  |  total attr: +0.0157

**Key mass** (top-1=72%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +0.0114 | 72.5% |
| 194 | flkL | +0.0043 | 27.5% |

**Query mass** (top-1=26%, top-2=43%, top-3=60%)  [DISTR(L211/A166/I226/L217)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 211 | ss1 | +0.0040 | 25.5% |
| 166 | flkL | +0.0027 | 17.4% |
| 226 | other | +0.0027 | 17.1% |
| 217 | ss1 | +0.0022 | 14.3% |
| 225 | other | +0.0021 | 13.1% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +19 | 1 | 14.3% |
| +79 | 1 | 14.3% |
| +23 | 1 | 14.3% |
| +17 | 1 | 14.3% |
| +78 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 2 | 28.6% |
| other | other | 2 | 28.6% |
| ss1 | flkL | 2 | 28.6% |
| ss1 | other | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 166 | flkL | 147 | other | +0.0027 | 0.4702 |
| 226 | other | 147 | other | +0.0027 | 0.2026 |
| 217 | ss1 | 194 | flkL | +0.0022 | 0.2094 |
| 211 | ss1 | 194 | flkL | +0.0021 | 0.1712 |
| 225 | other | 147 | other | +0.0021 | 0.1903 |

### L7 H13 — Rank #29

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0920

**Key mass** (top-1=19%, top-2=31%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 358 | flkR | +0.0177 | 19.2% |
| 322 | ss2 | +0.0112 | 12.2% |
| 148 | flkL | +0.0081 | 8.8% |
| 323 | ss2 | +0.0079 | 8.6% |
| 329 | ss2 | +0.0071 | 7.7% |

**Query mass** (top-1=14%, top-2=28%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0132 | 14.3% |
| 325 | ss2 | +0.0125 | 13.6% |
| 323 | ss2 | +0.0079 | 8.6% |
| 326 | ss2 | +0.0075 | 8.1% |
| 340 | flkR | +0.0073 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 20.8% |
| -32 | 2 | 8.3% |
| +32 | 2 | 8.3% |
| -33 | 1 | 4.2% |
| +18 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 8 | 33.3% |
| flkR | ss2 | 5 | 20.8% |
| ss2 | flkR | 3 | 12.5% |
| flkL | flkL | 3 | 12.5% |
| ss2 | flkL | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 325 | ss2 | 358 | flkR | +0.0102 | 0.0973 |
| 323 | ss2 | 323 | ss2 | +0.0079 | 0.1102 |
| 326 | ss2 | 358 | flkR | +0.0075 | 0.0508 |
| 340 | flkR | 322 | ss2 | +0.0073 | 0.0753 |
| 359 | flkR | 329 | ss2 | +0.0071 | 0.0782 |

### L8 H5 — Rank #27

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | POSITIONAL  |  cells: 9  |  total attr: +0.0701

**Key mass** (top-1=40%, top-2=59%, top-3=76%)  [DISTR(M287/A288/A286)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | other | +0.0277 | 39.6% |
| 288 | other | +0.0135 | 19.3% |
| 286 | other | +0.0122 | 17.4% |
| 331 | flkR | +0.0040 | 5.7% |
| 330 | ss2 | +0.0030 | 4.2% |

**Query mass** (top-1=48%, top-2=70%, top-3=89%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0338 | 48.3% |
| 288 | other | +0.0151 | 21.6% |
| 290 | other | +0.0135 | 19.3% |
| 286 | other | +0.0026 | 3.7% |
| 194 | flkL | +0.0025 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 4 | 44.4% |
| -42 | 2 | 22.2% |
| +1 | 2 | 22.2% |
| +71 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 5 | 55.6% |
| other | flkR | 1 | 11.1% |
| other | ss2 | 1 | 11.1% |
| flkL | flkL | 1 | 11.1% |
| other | ss1 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 287 | other | +0.0277 | 0.4013 |
| 290 | other | 288 | other | +0.0135 | 0.3908 |
| 288 | other | 286 | other | +0.0122 | 0.3717 |
| 289 | other | 331 | flkR | +0.0040 | 0.0445 |
| 288 | other | 330 | ss2 | +0.0030 | 0.0478 |

### L8 H11 — Rank #30

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 5  |  total attr: +0.0104

**Key mass** (top-1=21%, top-2=42%, top-3=62%)  [DISTR(A292/V293/A289/G290)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 292 | other | +0.0022 | 20.9% |
| 293 | other | +0.0022 | 20.7% |
| 289 | other | +0.0021 | 20.0% |
| 290 | other | +0.0021 | 19.8% |
| 291 | other | +0.0019 | 18.6% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +0.0104 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -145 | 1 | 20.0% |
| -146 | 1 | 20.0% |
| -142 | 1 | 20.0% |
| -143 | 1 | 20.0% |
| -144 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | other | 292 | other | +0.0022 | 0.0413 |
| 147 | other | 293 | other | +0.0022 | 0.0398 |
| 147 | other | 289 | other | +0.0021 | 0.0455 |
| 147 | other | 290 | other | +0.0021 | 0.0420 |
| 147 | other | 291 | other | +0.0019 | 0.0387 |

### L8 H14 — Rank #8

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 31  |  total attr: +0.1410

**Key mass** (top-1=15%, top-2=26%, top-3=37%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0206 | 14.6% |
| 290 | other | +0.0164 | 11.6% |
| 288 | other | +0.0155 | 11.0% |
| 291 | other | +0.0114 | 8.1% |
| 294 | other | +0.0107 | 7.6% |

**Query mass** (top-1=43%, top-2=83%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 326 | ss2 | +0.0612 | 43.4% |
| 359 | flkR | +0.0553 | 39.2% |
| 288 | other | +0.0085 | 6.0% |
| 205 | flkL | +0.0040 | 2.9% |
| 343 | flkR | +0.0027 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 2 | 6.5% |
| +70 | 1 | 3.2% |
| +69 | 1 | 3.2% |
| +37 | 1 | 3.2% |
| +71 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 10 | 32.3% |
| ss2 | other | 10 | 32.3% |
| other | other | 3 | 9.7% |
| flkL | ss1 | 2 | 6.5% |
| flkR | flkR | 2 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 359 | flkR | 289 | other | +0.0119 | 0.0997 |
| 359 | flkR | 290 | other | +0.0098 | 0.0862 |
| 326 | ss2 | 289 | other | +0.0086 | 0.0862 |
| 359 | flkR | 288 | other | +0.0080 | 0.0679 |
| 326 | ss2 | 288 | other | +0.0075 | 0.0747 |

### L8 H18 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 1  |  total attr: +0.0019

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkL | +0.0019 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0019 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 1 | 100.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 183 | flkL | +0.0019 | 0.0326 |

### L9 H7 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 1  |  total attr: +0.0060

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +0.0060 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0060 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +212 | 1 | 100.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 359 | flkR | 147 | other | +0.0060 | 0.1197 |

### L9 H8 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 2  |  total attr: +0.0065

**Key mass** (top-1=68%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 387 | flkR | +0.0044 | 67.6% |
| 383 | flkR | +0.0021 | 32.4% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0065 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -28 | 1 | 50.0% |
| -24 | 1 | 50.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 359 | flkR | 387 | flkR | +0.0044 | 0.0416 |
| 359 | flkR | 383 | flkR | +0.0021 | 0.0205 |

### L9 H14 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.1177

**Key mass** (top-1=17%, top-2=30%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | flkL | +0.0200 | 17.0% |
| 207 | flkL | +0.0159 | 13.5% |
| 191 | flkL | +0.0116 | 9.9% |
| 325 | ss2 | +0.0087 | 7.4% |
| 221 | other | +0.0083 | 7.0% |

**Query mass** (top-1=14%, top-2=27%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | flkL | +0.0162 | 13.7% |
| 322 | ss2 | +0.0159 | 13.5% |
| 325 | ss2 | +0.0147 | 12.5% |
| 326 | ss2 | +0.0142 | 12.1% |
| 321 | ss2 | +0.0129 | 10.9% |

**Offset distribution [frequency]** (top-2 coverage: 45%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 7 | 31.8% |
| +115 | 3 | 13.6% |
| +130 | 1 | 4.5% |
| +105 | 1 | 4.5% |
| +116 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=18%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 4 | 18.2% |
| flkR | flkR | 4 | 18.2% |
| flkL | flkL | 3 | 13.6% |
| flkR | flkL | 3 | 13.6% |
| ss2 | ss2 | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 206 | flkL | 206 | flkL | +0.0162 | 0.5349 |
| 322 | ss2 | 207 | flkL | +0.0159 | 0.4523 |
| 321 | ss2 | 191 | flkL | +0.0091 | 0.1804 |
| 325 | ss2 | 325 | ss2 | +0.0087 | 0.5643 |
| 326 | ss2 | 221 | other | +0.0083 | 0.1582 |

### L9 H17 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0963

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | flkL | +0.0963 | 100.0% |

**Query mass** (top-1=17%, top-2=32%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 291 | other | +0.0161 | 16.7% |
| 292 | other | +0.0150 | 15.5% |
| 293 | other | +0.0144 | 14.9% |
| 294 | other | +0.0120 | 12.5% |
| 295 | other | +0.0087 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +97 | 1 | 7.7% |
| +98 | 1 | 7.7% |
| +99 | 1 | 7.7% |
| +100 | 1 | 7.7% |
| +101 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 13 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 291 | other | 194 | flkL | +0.0161 | 0.4729 |
| 292 | other | 194 | flkL | +0.0150 | 0.4840 |
| 293 | other | 194 | flkL | +0.0144 | 0.4951 |
| 294 | other | 194 | flkL | +0.0120 | 0.4960 |
| 295 | other | 194 | flkL | +0.0087 | 0.4691 |

### L9 H18 — Rank #10

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 58  |  total attr: +0.2354

**Key mass** (top-1=14%, top-2=24%, top-3=35%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 212 | ss1 | +0.0319 | 13.5% |
| 218 | ss1 | +0.0250 | 10.6% |
| 209 | ss1 | +0.0250 | 10.6% |
| 211 | ss1 | +0.0245 | 10.4% |
| 341 | flkR | +0.0179 | 7.6% |

**Query mass** (top-1=51%, top-2=73%, top-3=94%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.1207 | 51.3% |
| 290 | other | +0.0502 | 21.3% |
| 288 | other | +0.0502 | 21.3% |
| 359 | flkR | +0.0040 | 1.7% |
| 208 | flkL | +0.0028 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +77 | 3 | 5.2% |
| +71 | 3 | 5.2% |
| +76 | 3 | 5.2% |
| +78 | 2 | 3.4% |
| +80 | 2 | 3.4% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 24 | 41.4% |
| other | flkR | 18 | 31.0% |
| other | flkL | 8 | 13.8% |
| other | other | 3 | 5.2% |
| ss2 | ss2 | 2 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 212 | ss1 | +0.0139 | 0.0295 |
| 289 | other | 211 | ss1 | +0.0125 | 0.0312 |
| 289 | other | 209 | ss1 | +0.0125 | 0.0364 |
| 289 | other | 218 | ss1 | +0.0118 | 0.0212 |
| 290 | other | 212 | ss1 | +0.0095 | 0.0344 |

### L10 H9 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0935

**Key mass** (top-1=59%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | other | +0.0551 | 59.0% |
| 194 | flkL | +0.0384 | 41.0% |

**Query mass** (top-1=15%, top-2=26%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0143 | 15.3% |
| 289 | other | +0.0105 | 11.2% |
| 290 | other | +0.0089 | 9.5% |
| 288 | other | +0.0083 | 8.9% |
| 210 | ss1 | +0.0074 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +142 | 1 | 5.0% |
| +165 | 1 | 5.0% |
| +141 | 1 | 5.0% |
| -148 | 1 | 5.0% |
| +179 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 4 | 20.0% |
| other | flkL | 4 | 20.0% |
| flkR | flkL | 3 | 15.0% |
| ss1 | flkL | 3 | 15.0% |
| flkL | other | 2 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 147 | other | +0.0105 | 0.0419 |
| 359 | flkR | 194 | flkL | +0.0096 | 0.1148 |
| 288 | other | 147 | other | +0.0083 | 0.0592 |
| -1 | other | 147 | other | +0.0064 | 0.1267 |
| 326 | ss2 | 147 | other | +0.0059 | 0.1244 |

### L11 H4 — Rank #12

**Tags:** k:MULTI-ANCHOR / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +0.0318

**Key mass** (top-1=38%, top-2=65%, top-3=82%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0119 | 37.6% |
| 288 | other | +0.0087 | 27.3% |
| 290 | other | +0.0053 | 16.7% |
| 287 | other | +0.0035 | 11.0% |
| 214 | ss1 | +0.0023 | 7.4% |

**Query mass** (top-1=86%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0272 | 85.7% |
| 322 | ss2 | +0.0023 | 7.4% |
| 355 | flkR | +0.0022 | 6.9% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +70 | 1 | 16.7% |
| +71 | 1 | 16.7% |
| +69 | 1 | 16.7% |
| +72 | 1 | 16.7% |
| +108 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 5 | 83.3% |
| ss2 | ss1 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 359 | flkR | 289 | other | +0.0098 | 0.1170 |
| 359 | flkR | 288 | other | +0.0087 | 0.1075 |
| 359 | flkR | 290 | other | +0.0053 | 0.0661 |
| 359 | flkR | 287 | other | +0.0035 | 0.0502 |
| 322 | ss2 | 214 | ss1 | +0.0023 | 0.1125 |

### L11 H10 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:flkR  |  cells: 10  |  total attr: +0.0624

**Key mass** (top-1=52%, top-2=62%, top-3=71%)  [DISTR(I359/D351/G206)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0327 | 52.5% |
| 351 | flkR | +0.0060 | 9.7% |
| 206 | flkL | +0.0055 | 8.8% |
| 325 | ss2 | +0.0046 | 7.3% |
| 190 | flkL | +0.0036 | 5.7% |

**Query mass** (top-1=58%, top-2=67%, top-3=74%)  [DISTR(I359/G321/A325)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0362 | 58.0% |
| 321 | ss2 | +0.0055 | 8.8% |
| 325 | ss2 | +0.0046 | 7.3% |
| 205 | flkL | +0.0036 | 5.7% |
| 210 | ss1 | +0.0032 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 50.0% |
| +115 | 1 | 10.0% |
| +15 | 1 | 10.0% |
| +8 | 1 | 10.0% |
| +12 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 40.0% |
| flkL | flkL | 2 | 20.0% |
| ss1 | ss1 | 2 | 20.0% |
| ss2 | flkL | 1 | 10.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 359 | flkR | 359 | flkR | +0.0327 | 0.4870 |
| 321 | ss2 | 206 | flkL | +0.0055 | 0.5558 |
| 325 | ss2 | 325 | ss2 | +0.0046 | 0.4162 |
| 205 | flkL | 190 | flkL | +0.0036 | 0.3584 |
| 359 | flkR | 351 | flkR | +0.0034 | 0.0634 |

### L11 H12 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 11  |  total attr: +0.0729

**Key mass** (top-1=35%, top-2=54%, top-3=73%)  [DISTR(L326/I359/V355)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 326 | ss2 | +0.0258 | 35.4% |
| 359 | flkR | +0.0139 | 19.0% |
| 355 | flkR | +0.0134 | 18.4% |
| 210 | ss1 | +0.0101 | 13.9% |
| 214 | ss1 | +0.0071 | 9.8% |

**Query mass** (top-1=30%, top-2=52%, top-3=64%)  [DISTR(M322/I359/V355/V209)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 322 | ss2 | +0.0217 | 29.8% |
| 359 | flkR | +0.0164 | 22.5% |
| 355 | flkR | +0.0082 | 11.2% |
| 209 | ss1 | +0.0077 | 10.6% |
| 213 | ss1 | +0.0054 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 64%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 4 | 36.4% |
| +4 | 3 | 27.3% |
| +3 | 1 | 9.1% |
| -5 | 1 | 9.1% |
| +0 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 36.4% |
| ss1 | ss1 | 3 | 27.3% |
| ss2 | ss2 | 2 | 18.2% |
| flkL | ss1 | 1 | 9.1% |
| other | ss1 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 322 | ss2 | 326 | ss2 | +0.0217 | 0.5179 |
| 359 | flkR | 355 | flkR | +0.0134 | 0.2436 |
| 355 | flkR | 359 | flkR | +0.0082 | 0.4295 |
| 213 | ss1 | 210 | ss1 | +0.0054 | 0.3468 |
| 209 | ss1 | 214 | ss1 | +0.0052 | 0.2341 |

### L11 H15 — Rank #20

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 8  |  total attr: +0.0314

**Key mass** (top-1=28%, top-2=50%, top-3=69%)  [DISTR(A289/G290/A288/T291)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0087 | 27.6% |
| 290 | other | +0.0072 | 22.8% |
| 288 | other | +0.0060 | 19.1% |
| 291 | other | +0.0039 | 12.4% |
| 147 | other | +0.0038 | 12.1% |

**Query mass** (top-1=75%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 359 | flkR | +0.0236 | 75.0% |
| 326 | ss2 | +0.0079 | 25.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +69 | 1 | 12.5% |
| +70 | 1 | 12.5% |
| +68 | 1 | 12.5% |
| +71 | 1 | 12.5% |
| +179 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 5 | 62.5% |
| ss2 | other | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 359 | flkR | 290 | other | +0.0072 | 0.0948 |
| 359 | flkR | 289 | other | +0.0068 | 0.1022 |
| 359 | flkR | 291 | other | +0.0039 | 0.0514 |
| 359 | flkR | 288 | other | +0.0038 | 0.0628 |
| 326 | ss2 | 147 | other | +0.0038 | 0.0385 |

### L11 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 21  |  total attr: +0.1040

**Key mass** (top-1=20%, top-2=36%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0212 | 20.4% |
| 191 | flkL | +0.0160 | 15.4% |
| 326 | ss2 | +0.0142 | 13.7% |
| 206 | flkL | +0.0075 | 7.2% |
| 322 | ss2 | +0.0058 | 5.6% |

**Query mass** (top-1=12%, top-2=23%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 321 | ss2 | +0.0129 | 12.4% |
| 206 | flkL | +0.0114 | 10.9% |
| 211 | ss1 | +0.0107 | 10.2% |
| 289 | other | +0.0104 | 10.0% |
| 333 | flkR | +0.0080 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 9 | 42.9% |
| -115 | 3 | 14.3% |
| +130 | 2 | 9.5% |
| +115 | 2 | 9.5% |
| +290 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=19%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 4 | 19.0% |
| other | other | 3 | 14.3% |
| flkL | ss2 | 3 | 14.3% |
| flkR | flkR | 3 | 14.3% |
| ss2 | flkL | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 321 | ss2 | 191 | flkL | +0.0129 | 0.4761 |
| 211 | ss1 | 326 | ss2 | +0.0107 | 0.3977 |
| 289 | other | -1 | other | +0.0104 | 0.1613 |
| 206 | flkL | 206 | flkL | +0.0075 | 0.2267 |
| 290 | other | -1 | other | +0.0068 | 0.1648 |

### L13 H2 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 11  |  total attr: +0.0553

**Key mass** (top-1=73%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 326 | ss2 | +0.0404 | 73.1% |
| 359 | flkR | +0.0109 | 19.7% |
| 324 | ss2 | +0.0039 | 7.1% |

**Query mass** (top-1=16%, top-2=30%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 322 | ss2 | +0.0087 | 15.8% |
| 330 | ss2 | +0.0081 | 14.6% |
| 327 | ss2 | +0.0065 | 11.8% |
| 319 | other | +0.0061 | 11.0% |
| 351 | flkR | +0.0046 | 8.3% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 3 | 27.3% |
| -4 | 1 | 9.1% |
| +1 | 1 | 9.1% |
| -7 | 1 | 9.1% |
| -8 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 5 | 45.5% |
| flkR | flkR | 3 | 27.3% |
| flkR | ss2 | 2 | 18.2% |
| other | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 322 | ss2 | 326 | ss2 | +0.0087 | 0.3072 |
| 330 | ss2 | 326 | ss2 | +0.0081 | 0.6104 |
| 327 | ss2 | 326 | ss2 | +0.0065 | 0.4414 |
| 319 | other | 326 | ss2 | +0.0061 | 0.2751 |
| 351 | flkR | 359 | flkR | +0.0046 | 0.1875 |

### L13 H7 — Rank #28

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0394

**Key mass** (top-1=34%, top-2=66%, top-3=78%)  [DISTR(V194/L211/M207)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | flkL | +0.0135 | 34.2% |
| 211 | ss1 | +0.0126 | 31.9% |
| 207 | flkL | +0.0046 | 11.7% |
| 214 | ss1 | +0.0037 | 9.5% |
| 199 | flkL | +0.0031 | 7.8% |

**Query mass** (top-1=20%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 211 | ss1 | +0.0081 | 20.5% |
| 322 | ss2 | +0.0046 | 11.7% |
| 326 | ss2 | +0.0045 | 11.5% |
| 213 | ss1 | +0.0043 | 11.0% |
| 214 | ss1 | +0.0037 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 18.2% |
| +115 | 2 | 18.2% |
| +27 | 1 | 9.1% |
| +117 | 1 | 9.1% |
| +95 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 45.5% |
| ss1 | ss1 | 2 | 18.2% |
| ss2 | flkL | 1 | 9.1% |
| ss2 | ss1 | 1 | 9.1% |
| ss1 | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 211 | ss1 | 211 | ss1 | +0.0081 | 0.4595 |
| 322 | ss2 | 207 | flkL | +0.0046 | 0.4319 |
| 326 | ss2 | 211 | ss1 | +0.0045 | 0.5413 |
| 214 | ss1 | 214 | ss1 | +0.0037 | 0.2299 |
| 221 | other | 194 | flkL | +0.0036 | 0.1425 |

### L13 H18 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkR→flkL  |  cells: 15  |  total attr: +0.0685

**Key mass** (top-1=94%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | flkL | +0.0642 | 93.7% |
| 147 | other | +0.0043 | 6.3% |

**Query mass** (top-1=20%, top-2=38%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 332 | flkR | +0.0138 | 20.1% |
| 322 | ss2 | +0.0124 | 18.1% |
| 351 | flkR | +0.0066 | 9.6% |
| 213 | ss1 | +0.0055 | 8.1% |
| 343 | flkR | +0.0050 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +138 | 1 | 6.7% |
| +128 | 1 | 6.7% |
| +157 | 1 | 6.7% |
| +149 | 1 | 6.7% |
| +139 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:flkR→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 6 | 40.0% |
| ss2 | flkL | 3 | 20.0% |
| other | flkL | 2 | 13.3% |
| ss1 | flkL | 2 | 13.3% |
| ss1 | other | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 332 | flkR | 194 | flkL | +0.0138 | 0.6171 |
| 322 | ss2 | 194 | flkL | +0.0124 | 0.6846 |
| 351 | flkR | 194 | flkL | +0.0066 | 0.5874 |
| 343 | flkR | 194 | flkL | +0.0050 | 0.5975 |
| 333 | flkR | 194 | flkL | +0.0041 | 0.6070 |

### L14 H9 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.0941

**Key mass** (top-1=88%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | flkL | +0.0824 | 87.6% |
| 147 | other | +0.0066 | 7.0% |
| 326 | ss2 | +0.0051 | 5.5% |

**Query mass** (top-1=22%, top-2=33%, top-3=41%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 289 | other | +0.0211 | 22.4% |
| 220 | other | +0.0102 | 10.9% |
| 221 | other | +0.0075 | 7.9% |
| 321 | ss2 | +0.0070 | 7.4% |
| 223 | other | +0.0069 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +95 | 1 | 5.9% |
| +26 | 1 | 5.9% |
| +27 | 1 | 5.9% |
| +127 | 1 | 5.9% |
| +29 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 7 | 41.2% |
| ss2 | flkL | 4 | 23.5% |
| other | other | 2 | 11.8% |
| flkL | flkL | 1 | 5.9% |
| ss1 | ss2 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | other | 194 | flkL | +0.0192 | 0.2306 |
| 220 | other | 194 | flkL | +0.0102 | 0.2713 |
| 221 | other | 194 | flkL | +0.0075 | 0.2635 |
| 321 | ss2 | 194 | flkL | +0.0070 | 0.1821 |
| 223 | other | 194 | flkL | +0.0069 | 0.2016 |

### L27 H15 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss2→flkL  |  cells: 4  |  total attr: +0.0194

**Key mass** (top-1=67%, top-2=90%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | flkL | +0.0129 | 66.6% |
| 322 | ss2 | +0.0046 | 23.7% |
| 326 | ss2 | +0.0019 | 9.8% |

**Query mass** (top-1=48%, top-2=72%, top-3=90%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 322 | ss2 | +0.0093 | 48.0% |
| 210 | ss1 | +0.0046 | 23.7% |
| 323 | ss2 | +0.0036 | 18.5% |
| 213 | ss1 | +0.0019 | 9.8% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +128 | 1 | 25.0% |
| -112 | 1 | 25.0% |
| +129 | 1 | 25.0% |
| -113 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 2 | 50.0% |
| ss1 | ss2 | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 322 | ss2 | 194 | flkL | +0.0093 | 0.2186 |
| 210 | ss1 | 322 | ss2 | +0.0046 | 0.1550 |
| 323 | ss2 | 194 | flkL | +0.0036 | 0.1584 |
| 213 | ss1 | 326 | ss2 | +0.0019 | 0.0565 |

### L29 H18 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.1984

**Key mass** (top-1=27%, top-2=43%, top-3=54%)  [DISTR(A323/A213/A319/K216/I327)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 323 | ss2 | +0.0536 | 27.0% |
| 213 | ss1 | +0.0312 | 15.7% |
| 319 | other | +0.0216 | 10.9% |
| 216 | ss1 | +0.0184 | 9.3% |
| 327 | ss2 | +0.0142 | 7.1% |

**Query mass** (top-1=24%, top-2=46%, top-3=64%)  [DISTR(A213/K216/M322/V209)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 213 | ss1 | +0.0467 | 23.5% |
| 216 | ss1 | +0.0452 | 22.8% |
| 322 | ss2 | +0.0356 | 18.0% |
| 209 | ss1 | +0.0231 | 11.6% |
| 324 | ss2 | +0.0157 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -110 | 2 | 8.7% |
| -107 | 2 | 8.7% |
| -111 | 2 | 8.7% |
| +111 | 2 | 8.7% |
| -109 | 2 | 8.7% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 34.8% |
| ss2 | ss1 | 5 | 21.7% |
| ss1 | other | 4 | 17.4% |
| ss1 | flkR | 2 | 8.7% |
| flkR | other | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 213 | ss1 | 323 | ss2 | +0.0331 | 0.3217 |
| 322 | ss2 | 213 | ss1 | +0.0312 | 0.2648 |
| 216 | ss1 | 323 | ss2 | +0.0184 | 0.4672 |
| 216 | ss1 | 327 | ss2 | +0.0142 | 0.1392 |
| 324 | ss2 | 216 | ss1 | +0.0138 | 0.3480 |

### L30 H13 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 6  |  total attr: +0.0227

**Key mass** (top-1=46%, top-2=91%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | ss1 | +0.0104 | 46.0% |
| 322 | ss2 | +0.0102 | 45.1% |
| 216 | ss1 | +0.0020 | 8.9% |

**Query mass** (top-1=37%, top-2=61%, top-3=72%)  [DISTR(M322/A213/V209)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 322 | ss2 | +0.0085 | 37.3% |
| 213 | ss1 | +0.0055 | 24.1% |
| 209 | ss1 | +0.0024 | 10.6% |
| 210 | ss1 | +0.0024 | 10.4% |
| 327 | ss2 | +0.0020 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 1 | 16.7% |
| -109 | 1 | 16.7% |
| -113 | 1 | 16.7% |
| -112 | 1 | 16.7% |
| +111 | 1 | 16.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 3 | 50.0% |
| ss2 | ss1 | 2 | 33.3% |
| other | ss1 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 322 | ss2 | 209 | ss1 | +0.0085 | 0.1490 |
| 213 | ss1 | 322 | ss2 | +0.0055 | 0.1821 |
| 209 | ss1 | 322 | ss2 | +0.0024 | 0.0418 |
| 210 | ss1 | 322 | ss2 | +0.0024 | 0.1702 |
| 327 | ss2 | 216 | ss1 | +0.0020 | 0.0622 |

### L32 H13 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0679

**Key mass** (top-1=49%, top-2=67%, top-3=78%)  [DISTR(K216/M322/A324)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 216 | ss1 | +0.0333 | 49.1% |
| 322 | ss2 | +0.0119 | 17.6% |
| 324 | ss2 | +0.0079 | 11.6% |
| 213 | ss1 | +0.0076 | 11.2% |
| 210 | ss1 | +0.0043 | 6.3% |

**Query mass** (top-1=38%, top-2=52%, top-3=65%)  [DISTR(A324/A213/M322/K216)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 324 | ss2 | +0.0261 | 38.5% |
| 213 | ss1 | +0.0090 | 13.3% |
| 322 | ss2 | +0.0088 | 13.0% |
| 216 | ss1 | +0.0079 | 11.6% |
| 210 | ss1 | +0.0038 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +108 | 1 | 9.1% |
| -108 | 1 | 9.1% |
| -109 | 1 | 9.1% |
| +109 | 1 | 9.1% |
| +112 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 54.5% |
| ss1 | ss2 | 5 | 45.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 324 | ss2 | 216 | ss1 | +0.0261 | 0.3600 |
| 216 | ss1 | 324 | ss2 | +0.0079 | 0.1084 |
| 213 | ss1 | 322 | ss2 | +0.0061 | 0.0818 |
| 322 | ss2 | 213 | ss1 | +0.0046 | 0.0607 |
| 322 | ss2 | 210 | ss1 | +0.0043 | 0.1070 |

### L32 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.1116

**Key mass** (top-1=26%, top-2=50%, top-3=71%)  [DISTR(I327/M322/V209)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 327 | ss2 | +0.0285 | 25.5% |
| 322 | ss2 | +0.0270 | 24.2% |
| 209 | ss1 | +0.0235 | 21.1% |
| 213 | ss1 | +0.0155 | 13.9% |
| 216 | ss1 | +0.0116 | 10.4% |

**Query mass** (top-1=28%, top-2=53%, top-3=67%)  [DISTR(M322/K216/A213/V209)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 322 | ss2 | +0.0310 | 27.8% |
| 216 | ss1 | +0.0285 | 25.5% |
| 213 | ss1 | +0.0157 | 14.1% |
| 209 | ss1 | +0.0146 | 13.1% |
| 327 | ss2 | +0.0072 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +111 | 2 | 18.2% |
| -111 | 1 | 9.1% |
| +113 | 1 | 9.1% |
| -113 | 1 | 9.1% |
| -109 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 63.6% |
| ss1 | ss2 | 4 | 36.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 216 | ss1 | 327 | ss2 | +0.0285 | 0.1545 |
| 322 | ss2 | 209 | ss1 | +0.0200 | 0.1097 |
| 209 | ss1 | 322 | ss2 | +0.0146 | 0.0804 |
| 213 | ss1 | 322 | ss2 | +0.0124 | 0.1004 |
| 322 | ss2 | 213 | ss1 | +0.0110 | 0.0894 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #7 | L0 | H0 | 2 | +0.0045 | DUAL-ANCHOR | I148/F178 | SINGLE-ANCHOR | I148 |  | INTRA:flkL |
| #13 | L5 | H7 | 4 | +0.0966 | SINGLE-ANCHOR | V194 | SINGLE-ANCHOR | R147 |  |  |
| #15 | L6 | H7 | 8 | +0.0809 | SINGLE-ANCHOR | R147 | DISTRIBUTED | A289/A288/G290 |  |  |
| #1 | L6 | H19 | 109 | +1.8004 | SINGLE-ANCHOR | R147 | DISTRIBUTED |  |  |  |
| #22 | L7 | H7 | 7 | +0.0157 | SINGLE-ANCHOR | R147 | DISTRIBUTED | L211/A166/I226/L217 |  |  |
| #29 | L7 | H13 | 24 | +0.0920 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #27 | L8 | H5 | 9 | +0.0701 | DISTRIBUTED | M287/A288/A286 | MULTI-ANCHOR |  | POSITIONAL |  |
| #30 | L8 | H11 | 5 | +0.0104 | DISTRIBUTED | A292/V293/A289/G290 | SINGLE-ANCHOR | R147 |  |  |
| #8 | L8 | H14 | 31 | +0.1410 | DISTRIBUTED |  | DUAL-ANCHOR | L326/I359 |  |  |
| #23 | L8 | H18 | 1 | +0.0019 | SINGLE-ANCHOR | L183 | SINGLE-ANCHOR | A289 |  |  |
| #25 | L9 | H7 | 1 | +0.0060 | SINGLE-ANCHOR | R147 | SINGLE-ANCHOR | I359 |  |  |
| #24 | L9 | H8 | 2 | +0.0065 | SINGLE-ANCHOR | E387 | SINGLE-ANCHOR | I359 |  | INTRA:flkR |
| #6 | L9 | H14 | 22 | +0.1177 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #17 | L9 | H17 | 13 | +0.0963 | SINGLE-ANCHOR | V194 | DISTRIBUTED |  |  |  |
| #10 | L9 | H18 | 58 | +0.2354 | DISTRIBUTED |  | DUAL-ANCHOR | A289/G290 |  |  |
| #19 | L10 | H9 | 20 | +0.0935 | DUAL-ANCHOR | R147/V194 | DISTRIBUTED |  |  |  |
| #12 | L11 | H4 | 6 | +0.0318 | MULTI-ANCHOR |  | SINGLE-ANCHOR | I359 |  |  |
| #16 | L11 | H10 | 10 | +0.0624 | DISTRIBUTED | I359/D351/G206 | DISTRIBUTED | I359/G321/A325 | POSITIONAL | INTRA:flkR |
| #9 | L11 | H12 | 11 | +0.0729 | DISTRIBUTED | L326/I359/V355 | DISTRIBUTED | M322/I359/V355/V209 | POSITIONAL |  |
| #20 | L11 | H15 | 8 | +0.0314 | DISTRIBUTED | A289/G290/A288/T291 | SINGLE-ANCHOR | I359 |  |  |
| #5 | L11 | H18 | 21 | +0.1040 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL |  |
| #18 | L13 | H2 | 11 | +0.0553 | SINGLE-ANCHOR | L326 | DISTRIBUTED |  |  | INTRA:ss2 |
| #28 | L13 | H7 | 11 | +0.0394 | DISTRIBUTED | V194/L211/M207 | DISTRIBUTED |  |  |  |
| #11 | L13 | H18 | 15 | +0.0685 | SINGLE-ANCHOR | V194 | DISTRIBUTED |  |  | CROSS:flkR→flkL |
| #14 | L14 | H9 | 17 | +0.0941 | SINGLE-ANCHOR | V194 | DISTRIBUTED |  |  |  |
| #26 | L27 | H15 | 4 | +0.0194 | SINGLE-ANCHOR | V194 | DUAL-ANCHOR | M322/L210 |  | CROSS:ss2→flkL |
| #2 | L29 | H18 | 23 | +0.1984 | DISTRIBUTED | A323/A213/A319/K216/I327 | DISTRIBUTED | A213/K216/M322/V209 |  |  |
| #21 | L30 | H13 | 6 | +0.0227 | DUAL-ANCHOR | V209/M322 | DISTRIBUTED | M322/A213/V209 |  | CROSS:ss1→ss2 |
| #4 | L32 | H13 | 11 | +0.0679 | DISTRIBUTED | K216/M322/A324 | DISTRIBUTED | A324/A213/M322/K216 |  | CROSS:ss2→ss1 |
| #3 | L32 | H18 | 11 | +0.1116 | DISTRIBUTED | I327/M322/V209 | DISTRIBUTED | M322/K216/A213/V209 |  | CROSS:ss2→ss1 |
