# Contact Pattern Analysis: 4WY2A

Generated: 2026-03-22 22:27:12   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4WY2A |
| Contact pair | (159, 271) |
| ss1 | [154, 165) |
| ss2 | [266, 277) |
| Clean flank | 45 |
| Corrupt flank | 44 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.6507 |
| Corrupt metric | 0.0718 |
| Gap | 0.5789 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 73.61% |
| positive IE | 50 | 82.36% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L7 | H0 | +0.2186 |
| 2 | L32 | H18 | +0.1472 |
| 3 | L6 | H19 | +0.1386 |
| 4 | L12 | H8 | +0.1383 |
| 5 | L8 | H12 | +0.1366 |
| 6 | L22 | H14 | +0.1237 |
| 7 | L30 | H1 | +0.1009 |
| 8 | L26 | H16 | +0.0920 |
| 9 | L12 | H2 | +0.0855 |
| 10 | L32 | H13 | +0.0846 |
| 11 | L11 | H16 | +0.0692 |
| 12 | L11 | H11 | +0.0688 |
| 13 | L10 | H9 | +0.0647 |
| 14 | L27 | H15 | +0.0645 |
| 15 | L11 | H10 | +0.0635 |
| 16 | L0 | H13 | +0.0613 |
| 17 | L17 | H1 | +0.0558 |
| 18 | L13 | H13 | +0.0553 |
| 19 | L21 | H4 | +0.0454 |
| 20 | L10 | H12 | +0.0443 |
| 21 | L9 | H12 | +0.0416 |
| 22 | L8 | H0 | +0.0411 |
| 23 | L29 | H18 | +0.0397 |
| 24 | L15 | H7 | +0.0372 |
| 25 | L11 | H14 | +0.0366 |
| 26 | L14 | H9 | +0.0340 |
| 27 | L5 | H13 | +0.0338 |
| 28 | L23 | H18 | +0.0302 |
| 29 | L9 | H14 | +0.0292 |
| 30 | L12 | H3 | +0.0288 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | 0.13% |
| 3 | 0.18% |
| 4 | 0.23% |
| 5 | 0.28% |
| 6 | 0.84% |
| 7 | 1.16% |
| 8 | 1.79% |
| 9 | 1.88% |
| 10 | 2.29% |
| 20 | 11.54% |
| 80 | 118.13% |
| 450 | 173.89% |

## Cell Attribution Analysis

Total cells: 4,665,876

- Positive: 2,378,363
- Negative: 2,284,962

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000049 | 466,588 |
| 95th | +0.00000139 | 233,295 |
| 99th | +0.00001026 | 46,659 |
| 99.5th | +0.00002189 | 23,330 |
| 99.9th | +0.00011765 | 4,667 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L8 | H12 | 159 | ss1 | 269 | ss2 | +0.090158 | 0.057844 |
| L8 | H12 | 158 | ss1 | 269 | ss2 | +0.085972 | 0.047954 |
| L6 | H19 | 269 | ss2 | 299 | flkR | +0.070851 | 0.028773 |
| L6 | H19 | 115 | flkL | 144 | flkL | +0.070226 | 0.027815 |
| L7 | H0 | 115 | flkL | 144 | flkL | +0.066510 | 0.039716 |
| L7 | H0 | 114 | flkL | 144 | flkL | +0.053023 | 0.029999 |
| L13 | H13 | 158 | ss1 | 269 | ss2 | +0.043534 | 0.075186 |
| L7 | H0 | 269 | ss2 | 299 | flkR | +0.042252 | 0.061694 |
| L30 | H1 | 269 | ss2 | 159 | ss1 | +0.042172 | 0.427651 |
| L10 | H12 | 144 | flkL | 115 | flkL | +0.038656 | 0.054265 |
| L7 | H3 | 114 | flkL | 109 | flkL | +0.035787 | 0.066457 |
| L12 | H8 | 158 | ss1 | 114 | flkL | +0.034842 | 0.169291 |
| L21 | H4 | 158 | ss1 | 160 | ss1 | +0.033643 | 0.480975 |
| L12 | H2 | 158 | ss1 | 269 | ss2 | +0.033066 | 0.128132 |
| L12 | H2 | 159 | ss1 | 269 | ss2 | +0.028068 | 0.092980 |
| L9 | H14 | 269 | ss2 | 115 | flkL | +0.026164 | 0.053533 |
| L11 | H14 | 158 | ss1 | 269 | ss2 | +0.022581 | 0.034452 |
| L8 | H12 | 158 | ss1 | 115 | flkL | +0.022178 | 0.010872 |
| L6 | H19 | 114 | flkL | 144 | flkL | +0.021430 | 0.007573 |
| L8 | H12 | 159 | ss1 | 115 | flkL | +0.020333 | 0.010877 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L11 | H18 | 309 | flkR | 112 | flkL | -0.005794 | 0.313347 |
| L11 | H14 | 144 | flkL | 115 | flkL | -0.006178 | 0.037405 |
| L14 | H9 | 144 | flkL | 115 | flkL | -0.007309 | 0.042297 |
| L9 | H14 | 159 | ss1 | 269 | ss2 | -0.007493 | 0.020588 |
| L10 | H9 | 114 | flkL | 114 | flkL | -0.008845 | 0.057788 |
| L10 | H9 | 159 | ss1 | 269 | ss2 | -0.008983 | 0.093847 |
| L11 | H18 | 158 | ss1 | 269 | ss2 | -0.009001 | 0.064119 |
| L11 | H14 | 158 | ss1 | 114 | flkL | -0.009366 | 0.015474 |
| L12 | H8 | -1 | other | 115 | flkL | -0.010028 | 0.076516 |
| L7 | H3 | 114 | flkL | 112 | flkL | -0.011049 | 0.022942 |
| L15 | H7 | 159 | ss1 | 269 | ss2 | -0.011477 | 0.092528 |
| L10 | H11 | 144 | flkL | 115 | flkL | -0.011542 | 0.041438 |
| L10 | H18 | 144 | flkL | 114 | flkL | -0.013986 | 0.053069 |
| L10 | H18 | 159 | ss1 | 269 | ss2 | -0.015058 | 0.074809 |
| L11 | H18 | 299 | flkR | 144 | flkL | -0.015679 | 0.300875 |
| L10 | H9 | 269 | ss2 | 114 | flkL | -0.017196 | 0.071970 |
| L12 | H2 | 163 | ss1 | 269 | ss2 | -0.017626 | 0.104433 |
| L9 | H14 | 269 | ss2 | 114 | flkL | -0.017916 | 0.053498 |
| L8 | H12 | 159 | ss1 | 114 | flkL | -0.039805 | 0.014943 |
| L10 | H12 | 144 | flkL | 114 | flkL | -0.039862 | 0.051403 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0718 | 0.00% |
| 10 | 10 | 6 | 0.0720 | 0.03% |
| 20 | 20 | 12 | 0.0720 | 0.04% |
| 50 | 50 | 28 | 0.0729 | 0.20% |
| 100 | 100 | 41 | 0.0799 | 1.40% |
| 200 | 200 | 47 | 0.1049 | 5.72% |
| 500 | 500 | 48 | 0.2222 | 25.98% |
| 1000 | 1,000 | 49 | 0.3625 | 50.21% |
| 2000 | 2,000 | 50 | 0.4968 | 73.42% |
| 5000 | 5,000 | 50 | 0.6080 | 92.62% |
| 10000 | 10,000 | 50 | 0.7336 | 114.31% |
| 20000 | 20,000 | 50 | 0.7800 | 122.32% |
| 50000 | 50,000 | 50 | 0.8165 | 128.63% |

## Motif Analysis

### L0 H13 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:flkL  |  cells: 43  |  total attr: +0.0473

**Key mass** (top-1=52%, top-2=55%, top-3=57%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 109 | flkL | +0.0244 | 51.6% |
| 122 | flkL | +0.0015 | 3.2% |
| 112 | flkL | +0.0012 | 2.6% |
| 133 | flkL | +0.0012 | 2.5% |
| 149 | flkL | +0.0012 | 2.5% |

**Query mass** (top-1=50%, top-2=59%, top-3=63%)  [DISTR(D109/V144/Q120/I268/W145)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 109 | flkL | +0.0238 | 50.5% |
| 144 | flkL | +0.0042 | 8.9% |
| 120 | flkL | +0.0019 | 4.1% |
| 268 | ss2 | +0.0019 | 4.0% |
| 145 | flkL | +0.0019 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +35 | 1 | 2.3% |
| +11 | 1 | 2.3% |
| +159 | 1 | 2.3% |
| +36 | 1 | 2.3% |
| +191 | 1 | 2.3% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 24 | 55.8% |
| flkL | flkR | 9 | 20.9% |
| flkR | flkL | 7 | 16.3% |
| ss2 | flkL | 2 | 4.7% |
| flkL | ss1 | 1 | 2.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | flkL | 109 | flkL | +0.0042 | 0.0013 |
| 120 | flkL | 109 | flkL | +0.0019 | 0.0079 |
| 268 | ss2 | 109 | flkL | +0.0019 | 0.0017 |
| 145 | flkL | 109 | flkL | +0.0019 | 0.0015 |
| 300 | flkR | 109 | flkL | +0.0018 | 0.0015 |

### L5 H13 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0351

**Key mass** (top-1=34%, top-2=54%, top-3=72%)  [DISTR(L113/A118/D109)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 113 | flkL | +0.0118 | 33.7% |
| 118 | flkL | +0.0073 | 20.8% |
| 109 | flkL | +0.0061 | 17.2% |
| 105 | other | +0.0046 | 13.0% |
| 114 | flkL | +0.0018 | 5.0% |

**Query mass** (top-1=48%, top-2=63%, top-3=77%)  [DISTR(V144/V269/L299)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | flkL | +0.0169 | 48.2% |
| 269 | ss2 | +0.0051 | 14.5% |
| 299 | flkR | +0.0050 | 14.2% |
| 158 | ss1 | +0.0032 | 9.2% |
| 159 | ss1 | +0.0021 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +42 | 2 | 10.0% |
| +31 | 1 | 5.0% |
| +40 | 1 | 5.0% |
| +35 | 1 | 5.0% |
| +26 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 35.0% |
| ss1 | flkL | 3 | 15.0% |
| flkL | other | 3 | 15.0% |
| ss2 | flkL | 3 | 15.0% |
| flkR | flkL | 2 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | flkL | 113 | flkL | +0.0049 | 0.0045 |
| 158 | ss1 | 118 | flkL | +0.0032 | 0.0050 |
| 144 | flkL | 109 | flkL | +0.0030 | 0.0020 |
| 144 | flkL | 118 | flkL | +0.0026 | 0.0026 |
| 144 | flkL | 105 | other | +0.0024 | 0.0015 |

### L6 H19 — Rank #3

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 8  |  total attr: +0.1747

**Key mass** (top-1=58%, top-2=99%, top-3=99%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | flkL | +0.1006 | 57.6% |
| 299 | flkR | +0.0715 | 40.9% |
| 268 | ss2 | +0.0014 | 0.8% |
| 319 | flkR | +0.0011 | 0.6% |

**Query mass** (top-1=41%, top-2=81%, top-3=93%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0709 | 40.6% |
| 115 | flkL | +0.0702 | 40.2% |
| 114 | flkL | +0.0214 | 12.3% |
| 158 | ss1 | +0.0061 | 3.5% |
| 144 | flkL | +0.0054 | 3.1% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -30 | 2 | 25.0% |
| -29 | 2 | 25.0% |
| +0 | 1 | 12.5% |
| +14 | 1 | 12.5% |
| -110 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 3 | 37.5% |
| ss2 | flkR | 2 | 25.0% |
| ss1 | flkL | 1 | 12.5% |
| ss1 | ss2 | 1 | 12.5% |
| ss1 | flkR | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 269 | ss2 | 299 | flkR | +0.0709 | 0.0288 |
| 115 | flkL | 144 | flkL | +0.0702 | 0.0278 |
| 114 | flkL | 144 | flkL | +0.0214 | 0.0076 |
| 144 | flkL | 144 | flkL | +0.0054 | 0.0069 |
| 158 | ss1 | 144 | flkL | +0.0036 | 0.0060 |

### L7 H0 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:flkL  |  cells: 8  |  total attr: +0.1667

**Key mass** (top-1=72%, top-2=97%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | flkL | +0.1195 | 71.7% |
| 299 | flkR | +0.0423 | 25.3% |
| 110 | flkL | +0.0016 | 1.0% |
| 141 | flkL | +0.0011 | 0.6% |
| 275 | ss2 | +0.0009 | 0.6% |

**Query mass** (top-1=41%, top-2=73%, top-3=99%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 115 | flkL | +0.0676 | 40.5% |
| 114 | flkL | +0.0537 | 32.2% |
| 269 | ss2 | +0.0438 | 26.3% |
| 158 | ss1 | +0.0016 | 1.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -30 | 2 | 25.0% |
| -26 | 2 | 25.0% |
| -29 | 1 | 12.5% |
| +48 | 1 | 12.5% |
| -6 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 4 | 50.0% |
| ss2 | ss2 | 2 | 25.0% |
| ss2 | flkR | 1 | 12.5% |
| ss1 | flkL | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 115 | flkL | 144 | flkL | +0.0665 | 0.0397 |
| 114 | flkL | 144 | flkL | +0.0530 | 0.0300 |
| 269 | ss2 | 299 | flkR | +0.0423 | 0.0617 |
| 158 | ss1 | 110 | flkL | +0.0016 | 0.0013 |
| 115 | flkL | 141 | flkL | +0.0011 | 0.0022 |

### L8 H0 — Rank #22

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 30  |  total attr: +0.0983

**Key mass** (top-1=19%, top-2=33%, top-3=46%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 112 | flkL | +0.0188 | 19.1% |
| 110 | flkL | +0.0141 | 14.3% |
| 115 | flkL | +0.0124 | 12.6% |
| 269 | ss2 | +0.0088 | 8.9% |
| 296 | flkR | +0.0075 | 7.6% |

**Query mass** (top-1=21%, top-2=36%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0208 | 21.1% |
| 298 | flkR | +0.0148 | 15.1% |
| 296 | flkR | +0.0141 | 14.3% |
| 114 | flkL | +0.0082 | 8.3% |
| 115 | flkL | +0.0077 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 9 | 30.0% |
| +186 | 3 | 10.0% |
| -186 | 2 | 6.7% |
| -171 | 2 | 6.7% |
| -110 | 2 | 6.7% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 6 | 20.0% |
| ss2 | flkL | 5 | 16.7% |
| flkL | flkR | 5 | 16.7% |
| flkL | ss2 | 4 | 13.3% |
| flkR | flkL | 3 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 298 | flkR | 112 | flkL | +0.0148 | 0.1978 |
| 296 | flkR | 110 | flkL | +0.0141 | 0.4067 |
| 269 | ss2 | 115 | flkL | +0.0124 | 0.0248 |
| 110 | flkL | 296 | flkR | +0.0075 | 0.2779 |
| 269 | ss2 | 114 | flkL | +0.0065 | 0.0325 |

### L8 H12 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | ss1→flkL  |  cells: 8  |  total attr: +0.2238

**Key mass** (top-1=79%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.1761 | 78.7% |
| 115 | flkL | +0.0425 | 19.0% |
| 126 | flkL | +0.0029 | 1.3% |
| 144 | flkL | +0.0015 | 0.7% |
| 110 | flkL | +0.0008 | 0.4% |

**Query mass** (top-1=50%, top-2=99%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.1129 | 50.4% |
| 158 | ss1 | +0.1095 | 48.9% |
| 269 | ss2 | +0.0015 | 0.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -110 | 1 | 12.5% |
| -111 | 1 | 12.5% |
| +43 | 1 | 12.5% |
| +44 | 1 | 12.5% |
| +33 | 1 | 12.5% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 5 | 62.5% |
| ss1 | ss2 | 2 | 25.0% |
| ss2 | flkL | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss1 | 269 | ss2 | +0.0902 | 0.0578 |
| 158 | ss1 | 269 | ss2 | +0.0860 | 0.0480 |
| 158 | ss1 | 115 | flkL | +0.0222 | 0.0109 |
| 159 | ss1 | 115 | flkL | +0.0203 | 0.0109 |
| 159 | ss1 | 126 | flkL | +0.0016 | 0.0013 |

### L9 H12 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 6  |  total attr: +0.0137

**Key mass** (top-1=69%, top-2=88%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | flkL | +0.0094 | 68.7% |
| 269 | ss2 | +0.0027 | 19.5% |
| 126 | flkL | +0.0009 | 6.4% |
| 111 | flkL | +0.0007 | 5.4% |

**Query mass** (top-1=36%, top-2=55%, top-3=74%)  [DISTR(I158/I115/V159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0049 | 35.7% |
| 115 | flkL | +0.0027 | 19.5% |
| 159 | ss1 | +0.0025 | 18.6% |
| 160 | ss1 | +0.0020 | 14.4% |
| 269 | ss2 | +0.0016 | 11.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +44 | 1 | 16.7% |
| -154 | 1 | 16.7% |
| +45 | 1 | 16.7% |
| +46 | 1 | 16.7% |
| +143 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 3 | 50.0% |
| ss2 | flkL | 2 | 33.3% |
| flkL | ss2 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 114 | flkL | +0.0049 | 0.0222 |
| 115 | flkL | 269 | ss2 | +0.0027 | 0.0177 |
| 159 | ss1 | 114 | flkL | +0.0025 | 0.0205 |
| 160 | ss1 | 114 | flkL | +0.0020 | 0.0148 |
| 269 | ss2 | 126 | flkL | +0.0009 | 0.0063 |

### L9 H14 — Rank #29

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.0930

**Key mass** (top-1=31%, top-2=45%, top-3=56%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 115 | flkL | +0.0287 | 30.9% |
| 298 | flkR | +0.0127 | 13.7% |
| 113 | flkL | +0.0105 | 11.3% |
| 124 | flkL | +0.0051 | 5.5% |
| 269 | ss2 | +0.0042 | 4.5% |

**Query mass** (top-1=28%, top-2=42%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0262 | 28.1% |
| 112 | flkL | +0.0127 | 13.7% |
| 299 | flkR | +0.0088 | 9.5% |
| 124 | flkL | +0.0051 | 5.5% |
| 144 | flkL | +0.0050 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 16.1% |
| -110 | 3 | 9.7% |
| -186 | 2 | 6.5% |
| +186 | 2 | 6.5% |
| +155 | 2 | 6.5% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 7 | 22.6% |
| flkL | flkR | 5 | 16.1% |
| flkL | flkL | 4 | 12.9% |
| ss1 | ss2 | 3 | 9.7% |
| flkL | ss2 | 3 | 9.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 269 | ss2 | 115 | flkL | +0.0262 | 0.0535 |
| 112 | flkL | 298 | flkR | +0.0127 | 0.5512 |
| 299 | flkR | 113 | flkL | +0.0069 | 0.0955 |
| 124 | flkL | 124 | flkL | +0.0051 | 0.0791 |
| 296 | flkR | 110 | flkL | +0.0039 | 0.1025 |

### L10 H9 — Rank #13

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 32  |  total attr: +0.0851

**Key mass** (top-1=44%, top-2=69%, top-3=91%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0372 | 43.7% |
| 115 | flkL | +0.0215 | 25.3% |
| 158 | ss1 | +0.0191 | 22.5% |
| 159 | ss1 | +0.0047 | 5.5% |
| 114 | flkL | +0.0026 | 3.0% |

**Query mass** (top-1=30%, top-2=56%, top-3=69%)  [DISTR(I158/V269/L114/A161)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0259 | 30.5% |
| 269 | ss2 | +0.0216 | 25.3% |
| 114 | flkL | +0.0111 | 13.1% |
| 161 | ss1 | +0.0073 | 8.6% |
| 115 | flkL | +0.0037 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 9.4% |
| +47 | 2 | 6.2% |
| -111 | 1 | 3.1% |
| +111 | 1 | 3.1% |
| +43 | 1 | 3.1% |

**Region-pair profile** (q→k)  (top=19%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 18.8% |
| ss1 | flkL | 4 | 12.5% |
| ss2 | flkL | 3 | 9.4% |
| flkL | flkL | 3 | 9.4% |
| flkL | ss2 | 3 | 9.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 269 | ss2 | +0.0194 | 0.0880 |
| 269 | ss2 | 158 | ss1 | +0.0123 | 0.0543 |
| 158 | ss1 | 115 | flkL | +0.0049 | 0.0225 |
| 269 | ss2 | 115 | flkL | +0.0045 | 0.0412 |
| 114 | flkL | 115 | flkL | +0.0043 | 0.0393 |

### L10 H12 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 45  |  total attr: +0.1070

**Key mass** (top-1=67%, top-2=79%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 115 | flkL | +0.0714 | 66.8% |
| 269 | ss2 | +0.0135 | 12.7% |
| 158 | ss1 | +0.0127 | 11.9% |
| 114 | flkL | +0.0072 | 6.7% |
| 159 | ss1 | +0.0008 | 0.8% |

**Query mass** (top-1=36%, top-2=42%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | flkL | +0.0387 | 36.1% |
| 156 | ss1 | +0.0065 | 6.1% |
| 160 | ss1 | +0.0046 | 4.3% |
| 155 | ss1 | +0.0045 | 4.2% |
| 302 | flkR | +0.0030 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +13 | 3 | 6.7% |
| +29 | 2 | 4.4% |
| +45 | 2 | 4.4% |
| +33 | 2 | 4.4% |
| +38 | 2 | 4.4% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 14 | 31.1% |
| ss1 | flkL | 11 | 24.4% |
| flkR | ss2 | 10 | 22.2% |
| other | ss1 | 6 | 13.3% |
| ss1 | ss1 | 2 | 4.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | flkL | 115 | flkL | +0.0387 | 0.0543 |
| 156 | ss1 | 115 | flkL | +0.0052 | 0.0365 |
| 155 | ss1 | 115 | flkL | +0.0045 | 0.0414 |
| 160 | ss1 | 115 | flkL | +0.0036 | 0.0292 |
| 302 | flkR | 269 | ss2 | +0.0030 | 0.1797 |

### L11 H10 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 49  |  total attr: +0.1043

**Key mass** (top-1=10%, top-2=18%, top-3=25%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0103 | 9.9% |
| 112 | flkL | +0.0083 | 8.0% |
| 109 | flkL | +0.0080 | 7.6% |
| 173 | other | +0.0066 | 6.4% |
| 171 | other | +0.0066 | 6.3% |

**Query mass** (top-1=40%, top-2=60%, top-3=72%)  [DISTR(I158/V159/V160)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0417 | 40.0% |
| 159 | ss1 | +0.0213 | 20.4% |
| 160 | ss1 | +0.0126 | 12.0% |
| 155 | ss1 | +0.0080 | 7.7% |
| 165 | other | +0.0053 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 4 | 8.2% |
| +44 | 4 | 8.2% |
| -15 | 2 | 4.1% |
| +45 | 2 | 4.1% |
| -16 | 2 | 4.1% |

**Region-pair profile** (q→k)  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 23 | 46.9% |
| ss1 | flkL | 14 | 28.6% |
| ss1 | ss1 | 3 | 6.1% |
| other | flkL | 3 | 6.1% |
| ss1 | flkR | 2 | 4.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 160 | ss1 | +0.0103 | 0.0962 |
| 158 | ss1 | 171 | other | +0.0066 | 0.0171 |
| 158 | ss1 | 173 | other | +0.0055 | 0.0149 |
| 157 | ss1 | 112 | flkL | +0.0048 | 0.0612 |
| 158 | ss1 | 174 | other | +0.0040 | 0.0120 |

### L11 H11 — Rank #12

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 60  |  total attr: +0.1016

**Key mass** (top-1=6%, top-2=10%, top-3=13%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | other | +0.0062 | 6.1% |
| 218 | other | +0.0039 | 3.8% |
| 219 | other | +0.0036 | 3.5% |
| 217 | other | +0.0034 | 3.4% |
| 272 | ss2 | +0.0032 | 3.1% |

**Query mass** (top-1=92%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0936 | 92.1% |
| 158 | ss1 | +0.0060 | 5.9% |
| 159 | ss1 | +0.0014 | 1.3% |
| 161 | ss1 | +0.0007 | 0.6% |

**Offset distribution [frequency]** (top-2 coverage: 3%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 1 | 1.7% |
| +51 | 1 | 1.7% |
| +50 | 1 | 1.7% |
| +52 | 1 | 1.7% |
| -3 | 1 | 1.7% |

**Region-pair profile** (q→k)  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 48 | 80.0% |
| ss2 | ss1 | 4 | 6.7% |
| ss1 | other | 3 | 5.0% |
| ss2 | ss2 | 3 | 5.0% |
| ss1 | flkL | 1 | 1.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 165 | other | +0.0042 | 0.0087 |
| 269 | ss2 | 218 | other | +0.0039 | 0.0025 |
| 269 | ss2 | 219 | other | +0.0036 | 0.0023 |
| 269 | ss2 | 217 | other | +0.0034 | 0.0021 |
| 269 | ss2 | 272 | ss2 | +0.0032 | 0.0027 |

### L11 H14 — Rank #25

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 17  |  total attr: +0.0791

**Key mass** (top-1=59%, top-2=79%, top-3=91%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0464 | 58.7% |
| 115 | flkL | +0.0162 | 20.5% |
| 114 | flkL | +0.0095 | 12.1% |
| 158 | ss1 | +0.0055 | 7.0% |
| 144 | flkL | +0.0014 | 1.8% |

**Query mass** (top-1=41%, top-2=74%, top-3=83%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0321 | 40.6% |
| 159 | ss1 | +0.0266 | 33.6% |
| 144 | flkL | +0.0067 | 8.4% |
| 160 | ss1 | +0.0045 | 5.7% |
| 156 | ss1 | +0.0023 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +43 | 2 | 11.8% |
| +30 | 2 | 11.8% |
| -111 | 1 | 5.9% |
| -110 | 1 | 5.9% |
| +44 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 35.3% |
| ss1 | ss2 | 4 | 23.5% |
| flkL | flkL | 2 | 11.8% |
| ss1 | ss1 | 2 | 11.8% |
| ss2 | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 269 | ss2 | +0.0226 | 0.0345 |
| 159 | ss1 | 269 | ss2 | +0.0182 | 0.0362 |
| 158 | ss1 | 115 | flkL | +0.0085 | 0.0152 |
| 144 | flkL | 114 | flkL | +0.0067 | 0.0273 |
| 159 | ss1 | 115 | flkL | +0.0062 | 0.0144 |

### L11 H16 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.0242

**Key mass** (top-1=68%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0165 | 68.2% |
| 115 | flkL | +0.0058 | 24.1% |
| -1 | other | +0.0012 | 4.8% |
| 281 | flkR | +0.0007 | 3.0% |

**Query mass** (top-1=29%, top-2=50%, top-3=63%)  [DISTR(I158/V159/V160/V269)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0071 | 29.2% |
| 159 | ss1 | +0.0051 | 21.0% |
| 160 | ss1 | +0.0031 | 12.9% |
| 269 | ss2 | +0.0031 | 12.7% |
| -1 | other | +0.0021 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -111 | 1 | 6.7% |
| -110 | 1 | 6.7% |
| -109 | 1 | 6.7% |
| +154 | 1 | 6.7% |
| -106 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 33.3% |
| ss1 | flkL | 3 | 20.0% |
| other | ss2 | 2 | 13.3% |
| ss2 | flkL | 1 | 6.7% |
| ss1 | other | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 269 | ss2 | +0.0044 | 0.0190 |
| 159 | ss1 | 269 | ss2 | +0.0038 | 0.0250 |
| 160 | ss1 | 269 | ss2 | +0.0023 | 0.0196 |
| 269 | ss2 | 115 | flkL | +0.0023 | 0.0170 |
| 163 | ss1 | 269 | ss2 | +0.0019 | 0.0365 |

### L12 H2 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.1087

**Key mass** (top-1=87%, top-2=93%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0951 | 87.5% |
| 144 | flkL | +0.0063 | 5.8% |
| 115 | flkL | +0.0045 | 4.1% |
| 299 | flkR | +0.0028 | 2.6% |

**Query mass** (top-1=31%, top-2=58%, top-3=71%)  [DISTR(I158/V159/V160)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0338 | 31.1% |
| 159 | ss1 | +0.0289 | 26.6% |
| 160 | ss1 | +0.0142 | 13.1% |
| 167 | other | +0.0061 | 5.6% |
| -1 | other | +0.0045 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -111 | 1 | 3.8% |
| -110 | 1 | 3.8% |
| -109 | 1 | 3.8% |
| -102 | 1 | 3.8% |
| -116 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 8 | 30.8% |
| ss1 | flkL | 5 | 19.2% |
| ss1 | ss2 | 4 | 15.4% |
| ss2 | ss2 | 3 | 11.5% |
| flkL | ss2 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 269 | ss2 | +0.0331 | 0.1281 |
| 159 | ss1 | 269 | ss2 | +0.0281 | 0.0930 |
| 160 | ss1 | 269 | ss2 | +0.0128 | 0.1293 |
| 167 | other | 269 | ss2 | +0.0061 | 0.1699 |
| -1 | other | 115 | flkL | +0.0045 | 0.1169 |

### L12 H3 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→flkR  |  cells: 9  |  total attr: +0.0277

**Key mass** (top-1=63%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 299 | flkR | +0.0173 | 62.5% |
| 269 | ss2 | +0.0104 | 37.5% |

**Query mass** (top-1=41%, top-2=75%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0113 | 40.7% |
| 269 | ss2 | +0.0094 | 33.9% |
| 160 | ss1 | +0.0029 | 10.5% |
| 163 | ss1 | +0.0016 | 5.8% |
| 285 | flkR | +0.0011 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -30 | 1 | 11.1% |
| -111 | 1 | 11.1% |
| -141 | 1 | 11.1% |
| -109 | 1 | 11.1% |
| -136 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 4 | 44.4% |
| ss1 | ss2 | 3 | 33.3% |
| ss2 | flkR | 1 | 11.1% |
| flkR | flkR | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 269 | ss2 | 299 | flkR | +0.0094 | 0.0934 |
| 158 | ss1 | 269 | ss2 | +0.0079 | 0.0149 |
| 158 | ss1 | 299 | flkR | +0.0034 | 0.0112 |
| 160 | ss1 | 269 | ss2 | +0.0017 | 0.0075 |
| 163 | ss1 | 299 | flkR | +0.0016 | 0.0052 |

### L12 H8 — Rank #4

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 32  |  total attr: +0.1350

**Key mass** (top-1=50%, top-2=72%, top-3=94%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | flkL | +0.0677 | 50.2% |
| 269 | ss2 | +0.0295 | 21.9% |
| 115 | flkL | +0.0290 | 21.5% |
| 158 | ss1 | +0.0038 | 2.8% |
| 160 | ss1 | +0.0028 | 2.0% |

**Query mass** (top-1=47%, top-2=74%, top-3=83%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0638 | 47.3% |
| 159 | ss1 | +0.0366 | 27.1% |
| 161 | ss1 | +0.0122 | 9.1% |
| 160 | ss1 | +0.0055 | 4.1% |
| -1 | other | +0.0044 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +44 | 2 | 6.2% |
| +43 | 2 | 6.2% |
| +45 | 2 | 6.2% |
| +0 | 2 | 6.2% |
| +46 | 2 | 6.2% |

**Region-pair profile** (q→k)  (top=34%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 11 | 34.4% |
| ss1 | ss1 | 6 | 18.8% |
| ss1 | ss2 | 5 | 15.6% |
| flkL | flkL | 5 | 15.6% |
| other | flkL | 2 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 114 | flkL | +0.0348 | 0.1693 |
| 158 | ss1 | 115 | flkL | +0.0161 | 0.0567 |
| 159 | ss1 | 269 | ss2 | +0.0142 | 0.0420 |
| 159 | ss1 | 114 | flkL | +0.0136 | 0.0464 |
| 161 | ss1 | 114 | flkL | +0.0080 | 0.0708 |

### L13 H13 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 7  |  total attr: +0.0606

**Key mass** (top-1=94%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0568 | 93.8% |
| 114 | flkL | +0.0029 | 4.8% |
| 113 | flkL | +0.0009 | 1.5% |

**Query mass** (top-1=77%, top-2=89%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0466 | 77.0% |
| 159 | ss1 | +0.0072 | 11.8% |
| 160 | ss1 | +0.0041 | 6.8% |
| 161 | ss1 | +0.0027 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +45 | 2 | 28.6% |
| -111 | 1 | 14.3% |
| -110 | 1 | 14.3% |
| -109 | 1 | 14.3% |
| -108 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 57.1% |
| ss1 | flkL | 3 | 42.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 269 | ss2 | +0.0435 | 0.0752 |
| 159 | ss1 | 269 | ss2 | +0.0065 | 0.0201 |
| 160 | ss1 | 269 | ss2 | +0.0041 | 0.0136 |
| 161 | ss1 | 269 | ss2 | +0.0027 | 0.0145 |
| 158 | ss1 | 114 | flkL | +0.0022 | 0.0041 |

### L14 H9 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 34  |  total attr: +0.0620

**Key mass** (top-1=48%, top-2=89%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | flkL | +0.0299 | 48.2% |
| 269 | ss2 | +0.0250 | 40.3% |
| 159 | ss1 | +0.0037 | 6.0% |
| 115 | flkL | +0.0028 | 4.5% |
| 144 | flkL | +0.0006 | 1.0% |

**Query mass** (top-1=19%, top-2=30%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | flkL | +0.0118 | 19.1% |
| 258 | other | +0.0066 | 10.6% |
| 257 | other | +0.0050 | 8.0% |
| 269 | ss2 | +0.0049 | 7.9% |
| 167 | other | +0.0038 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +30 | 1 | 2.9% |
| -11 | 1 | 2.9% |
| -12 | 1 | 2.9% |
| -102 | 1 | 2.9% |
| +110 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 12 | 35.3% |
| flkL | flkL | 9 | 26.5% |
| ss1 | flkL | 5 | 14.7% |
| ss2 | flkL | 3 | 8.8% |
| other | flkL | 2 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | flkL | 114 | flkL | +0.0118 | 0.0542 |
| 258 | other | 269 | ss2 | +0.0055 | 0.2083 |
| 257 | other | 269 | ss2 | +0.0041 | 0.2050 |
| 167 | other | 269 | ss2 | +0.0038 | 0.1871 |
| 269 | ss2 | 159 | ss1 | +0.0030 | 0.0937 |

### L15 H7 — Rank #24

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 14  |  total attr: +0.0749

**Key mass** (top-1=27%, top-2=50%, top-3=70%)  [DISTR(V160/V159/I158/A161)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0204 | 27.3% |
| 159 | ss1 | +0.0173 | 23.1% |
| 158 | ss1 | +0.0147 | 19.6% |
| 161 | ss1 | +0.0104 | 13.9% |
| 299 | flkR | +0.0076 | 10.2% |

**Query mass** (top-1=36%, top-2=59%, top-3=75%)  [DISTR(V160/I158/V159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0268 | 35.8% |
| 158 | ss1 | +0.0171 | 22.8% |
| 159 | ss1 | +0.0120 | 16.0% |
| 161 | ss1 | +0.0093 | 12.5% |
| 269 | ss2 | +0.0052 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 6 | 42.9% |
| +1 | 2 | 14.3% |
| -1 | 2 | 14.3% |
| -155 | 2 | 14.3% |
| -30 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 64.3% |
| ss2 | flkR | 1 | 7.1% |
| ss1 | flkR | 1 | 7.1% |
| other | other | 1 | 7.1% |
| flkL | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 160 | ss1 | +0.0188 | 0.1668 |
| 158 | ss1 | 158 | ss1 | +0.0147 | 0.1106 |
| 159 | ss1 | 159 | ss1 | +0.0114 | 0.1335 |
| 161 | ss1 | 161 | ss1 | +0.0084 | 0.1544 |
| 160 | ss1 | 159 | ss1 | +0.0060 | 0.0376 |

### L17 H1 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 19  |  total attr: +0.0707

**Key mass** (top-1=78%, top-2=87%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0555 | 78.5% |
| 167 | other | +0.0058 | 8.3% |
| 165 | other | +0.0015 | 2.1% |
| 257 | other | +0.0015 | 2.1% |
| 166 | other | +0.0015 | 2.1% |

**Query mass** (top-1=34%, top-2=57%, top-3=71%)  [DISTR(V160/N163/V159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0242 | 34.3% |
| 163 | ss1 | +0.0159 | 22.5% |
| 159 | ss1 | +0.0101 | 14.3% |
| 158 | ss1 | +0.0058 | 8.2% |
| 157 | ss1 | +0.0053 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -109 | 1 | 5.3% |
| -106 | 1 | 5.3% |
| -110 | 1 | 5.3% |
| -112 | 1 | 5.3% |
| -113 | 1 | 5.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 42.1% |
| ss1 | other | 8 | 42.1% |
| ss2 | flkR | 2 | 10.5% |
| ss1 | flkR | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 269 | ss2 | +0.0155 | 0.1805 |
| 163 | ss1 | 269 | ss2 | +0.0138 | 0.0786 |
| 159 | ss1 | 269 | ss2 | +0.0101 | 0.1195 |
| 157 | ss1 | 269 | ss2 | +0.0053 | 0.0759 |
| 156 | ss1 | 269 | ss2 | +0.0048 | 0.1160 |

### L21 H4 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 10  |  total attr: +0.0619

**Key mass** (top-1=82%, top-2=89%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0507 | 81.9% |
| 158 | ss1 | +0.0045 | 7.3% |
| 161 | ss1 | +0.0028 | 4.5% |
| 162 | ss1 | +0.0023 | 3.7% |
| 163 | ss1 | +0.0016 | 2.5% |

**Query mass** (top-1=61%, top-2=78%, top-3=94%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0375 | 60.7% |
| 159 | ss1 | +0.0106 | 17.2% |
| 157 | ss1 | +0.0099 | 16.0% |
| 156 | ss1 | +0.0026 | 4.2% |
| 161 | ss1 | +0.0012 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 3 | 30.0% |
| -1 | 2 | 20.0% |
| -4 | 2 | 20.0% |
| -3 | 1 | 10.0% |
| -5 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss1 | 160 | ss1 | +0.0336 | 0.4810 |
| 157 | ss1 | 160 | ss1 | +0.0080 | 0.2853 |
| 159 | ss1 | 160 | ss1 | +0.0078 | 0.1852 |
| 159 | ss1 | 161 | ss1 | +0.0028 | 0.1061 |
| 158 | ss1 | 162 | ss1 | +0.0023 | 0.1430 |

### L22 H14 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 28  |  total attr: +0.0738

**Key mass** (top-1=30%, top-2=47%, top-3=64%)  [DISTR(V269/I158/G267/A161)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0223 | 30.2% |
| 158 | ss1 | +0.0127 | 17.2% |
| 267 | ss2 | +0.0123 | 16.7% |
| 161 | ss1 | +0.0107 | 14.5% |
| 156 | ss1 | +0.0033 | 4.4% |

**Query mass** (top-1=20%, top-2=35%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0147 | 20.0% |
| 270 | ss2 | +0.0107 | 14.5% |
| 158 | ss1 | +0.0089 | 12.1% |
| 267 | ss2 | +0.0065 | 8.9% |
| 157 | ss1 | +0.0056 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 39%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 6 | 21.4% |
| -110 | 5 | 17.9% |
| +109 | 2 | 7.1% |
| -111 | 2 | 7.1% |
| -109 | 2 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 13 | 46.4% |
| ss1 | ss2 | 11 | 39.3% |
| ss1 | flkL | 2 | 7.1% |
| ss2 | ss2 | 1 | 3.6% |
| ss2 | flkR | 1 | 3.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss1 | 269 | ss2 | +0.0140 | 0.1104 |
| 270 | ss2 | 158 | ss1 | +0.0066 | 0.3011 |
| 157 | ss1 | 267 | ss2 | +0.0056 | 0.2239 |
| 271 | ss2 | 161 | ss1 | +0.0053 | 0.1031 |
| 267 | ss2 | 158 | ss1 | +0.0045 | 0.1162 |

### L23 H18 — Rank #28

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | ss1→flkL  |  cells: 8  |  total attr: +0.0373

**Key mass** (top-1=44%, top-2=86%, top-3=98%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | ss1 | +0.0164 | 44.0% |
| 147 | flkL | +0.0158 | 42.4% |
| 144 | flkL | +0.0044 | 11.8% |
| 158 | ss1 | +0.0007 | 1.8% |

**Query mass** (top-1=48%, top-2=81%, top-3=90%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 160 | ss1 | +0.0179 | 47.9% |
| 158 | ss1 | +0.0124 | 33.3% |
| 161 | ss1 | +0.0033 | 8.9% |
| 159 | ss1 | +0.0031 | 8.2% |
| 163 | ss1 | +0.0007 | 1.8% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 1 | 12.5% |
| +11 | 1 | 12.5% |
| -2 | 1 | 12.5% |
| +12 | 1 | 12.5% |
| +13 | 1 | 12.5% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 5 | 62.5% |
| ss1 | ss1 | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 160 | ss1 | 163 | ss1 | +0.0131 | 0.6630 |
| 158 | ss1 | 147 | flkL | +0.0098 | 0.1799 |
| 161 | ss1 | 163 | ss1 | +0.0033 | 0.7386 |
| 159 | ss1 | 147 | flkL | +0.0031 | 0.2580 |
| 160 | ss1 | 147 | flkL | +0.0030 | 0.2110 |

### L26 H16 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 18  |  total attr: +0.0529

**Key mass** (top-1=19%, top-2=33%, top-3=45%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 271 | ss2 | +0.0102 | 19.2% |
| 270 | ss2 | +0.0071 | 13.5% |
| 269 | ss2 | +0.0067 | 12.6% |
| 156 | ss1 | +0.0062 | 11.6% |
| 272 | ss2 | +0.0050 | 9.5% |

**Query mass** (top-1=29%, top-2=46%, top-3=64%)  [DISTR(A161/V159/V160/T157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 161 | ss1 | +0.0152 | 28.7% |
| 159 | ss1 | +0.0094 | 17.7% |
| 160 | ss1 | +0.0091 | 17.3% |
| 157 | ss1 | +0.0070 | 13.1% |
| 267 | ss2 | +0.0053 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -110 | 4 | 22.2% |
| +111 | 2 | 11.1% |
| -111 | 2 | 11.1% |
| +110 | 1 | 5.6% |
| +15 | 1 | 5.6% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 44.4% |
| ss2 | ss1 | 3 | 16.7% |
| ss1 | flkL | 2 | 11.1% |
| ss1 | other | 2 | 11.1% |
| ss1 | flkR | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 161 | ss1 | 271 | ss2 | +0.0102 | 0.1861 |
| 160 | ss1 | 270 | ss2 | +0.0071 | 0.1024 |
| 159 | ss1 | 269 | ss2 | +0.0067 | 0.0819 |
| 267 | ss2 | 156 | ss1 | +0.0053 | 0.5567 |
| 161 | ss1 | 272 | ss2 | +0.0050 | 0.1425 |

### L27 H15 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0379

**Key mass** (top-1=25%, top-2=48%, top-3=65%)  [DISTR(V159/V160/I158/V270)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0094 | 24.9% |
| 160 | ss1 | +0.0090 | 23.6% |
| 158 | ss1 | +0.0061 | 16.0% |
| 270 | ss2 | +0.0035 | 9.1% |
| 300 | flkR | +0.0030 | 7.8% |

**Query mass** (top-1=24%, top-2=46%, top-3=61%)  [DISTR(V270/G267/V269/T157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 270 | ss2 | +0.0090 | 23.6% |
| 267 | ss2 | +0.0086 | 22.8% |
| 269 | ss2 | +0.0056 | 14.8% |
| 157 | ss1 | +0.0039 | 10.2% |
| 158 | ss1 | +0.0018 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 3 | 18.8% |
| -112 | 2 | 12.5% |
| +14 | 2 | 12.5% |
| +109 | 1 | 6.2% |
| -143 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 37.5% |
| ss1 | ss2 | 4 | 25.0% |
| ss1 | flkR | 2 | 12.5% |
| ss1 | flkL | 2 | 12.5% |
| other | ss1 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 270 | ss2 | 160 | ss1 | +0.0090 | 0.1269 |
| 267 | ss2 | 158 | ss1 | +0.0061 | 0.1816 |
| 269 | ss2 | 159 | ss1 | +0.0056 | 0.0468 |
| 157 | ss1 | 300 | flkR | +0.0030 | 0.0916 |
| 267 | ss2 | 159 | ss1 | +0.0026 | 0.2722 |

### L29 H18 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 19  |  total attr: +0.0334

**Key mass** (top-1=28%, top-2=55%, top-3=62%)  [DISTR(A266/I257/N265/?-1/Y155)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 266 | ss2 | +0.0094 | 28.0% |
| 257 | other | +0.0089 | 26.8% |
| 265 | other | +0.0023 | 6.8% |
| -1 | other | +0.0020 | 5.9% |
| 155 | ss1 | +0.0018 | 5.4% |

**Query mass** (top-1=26%, top-2=51%, top-3=67%)  [DISTR(A161/V159/T157/G267)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 161 | ss1 | +0.0086 | 25.9% |
| 159 | ss1 | +0.0083 | 24.8% |
| 157 | ss1 | +0.0054 | 16.1% |
| 267 | ss2 | +0.0034 | 10.3% |
| 164 | ss1 | +0.0015 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -109 | 2 | 10.5% |
| -137 | 2 | 10.5% |
| -107 | 1 | 5.3% |
| -96 | 1 | 5.3% |
| -108 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 31.6% |
| ss1 | ss2 | 5 | 26.3% |
| ss2 | ss1 | 3 | 15.8% |
| ss1 | flkR | 3 | 15.8% |
| ss1 | ss1 | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss1 | 266 | ss2 | +0.0076 | 0.2718 |
| 161 | ss1 | 257 | other | +0.0066 | 0.3472 |
| 157 | ss1 | 265 | other | +0.0023 | 0.0383 |
| 267 | ss2 | 155 | ss1 | +0.0018 | 0.0414 |
| 157 | ss1 | 266 | ss2 | +0.0018 | 0.1501 |

### L30 H1 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.0640

**Key mass** (top-1=67%, top-2=80%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0428 | 66.8% |
| 270 | ss2 | +0.0083 | 13.0% |
| 157 | ss1 | +0.0061 | 9.5% |
| 298 | flkR | +0.0020 | 3.1% |
| 158 | ss1 | +0.0015 | 2.4% |

**Query mass** (top-1=66%, top-2=79%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 269 | ss2 | +0.0422 | 65.9% |
| 160 | ss1 | +0.0083 | 13.0% |
| 267 | ss2 | +0.0080 | 12.4% |
| 266 | ss2 | +0.0022 | 3.5% |
| 157 | ss1 | +0.0017 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 2 | 16.7% |
| -110 | 2 | 16.7% |
| +109 | 2 | 16.7% |
| -31 | 1 | 8.3% |
| -109 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 50.0% |
| ss1 | ss2 | 4 | 33.3% |
| ss2 | flkR | 1 | 8.3% |
| ss1 | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 269 | ss2 | 159 | ss1 | +0.0422 | 0.4277 |
| 160 | ss1 | 270 | ss2 | +0.0083 | 0.1269 |
| 267 | ss2 | 157 | ss1 | +0.0039 | 0.1525 |
| 266 | ss2 | 157 | ss1 | +0.0022 | 0.0616 |
| 267 | ss2 | 158 | ss1 | +0.0015 | 0.0456 |

### L32 H13 — Rank #10

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 17  |  total attr: +0.0341

**Key mass** (top-1=19%, top-2=39%, top-3=51%)  [DISTR(T157/A266/V269/G272/G267)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | ss1 | +0.0066 | 19.5% |
| 266 | ss2 | +0.0066 | 19.2% |
| 269 | ss2 | +0.0041 | 12.1% |
| 272 | ss2 | +0.0040 | 11.8% |
| 267 | ss2 | +0.0036 | 10.5% |

**Query mass** (top-1=23%, top-2=38%, top-3=52%)  [DISTR(T157/A266/G267/V159/N163)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | ss1 | +0.0080 | 23.3% |
| 266 | ss2 | +0.0051 | 15.1% |
| 267 | ss2 | +0.0048 | 14.0% |
| 159 | ss1 | +0.0030 | 8.9% |
| 163 | ss1 | +0.0030 | 8.8% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -109 | 3 | 17.6% |
| +109 | 3 | 17.6% |
| -110 | 3 | 17.6% |
| +110 | 2 | 11.8% |
| +111 | 2 | 11.8% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 52.9% |
| ss2 | ss1 | 8 | 47.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 157 | ss1 | 266 | ss2 | +0.0066 | 0.1280 |
| 266 | ss2 | 157 | ss1 | +0.0051 | 0.1004 |
| 159 | ss1 | 269 | ss2 | +0.0030 | 0.0206 |
| 163 | ss1 | 272 | ss2 | +0.0030 | 0.0669 |
| 267 | ss2 | 158 | ss1 | +0.0020 | 0.0387 |

### L32 H18 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 20  |  total attr: +0.0603

**Key mass** (top-1=13%, top-2=26%, top-3=39%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 161 | ss1 | +0.0080 | 13.2% |
| 157 | ss1 | +0.0078 | 12.9% |
| 267 | ss2 | +0.0077 | 12.8% |
| 266 | ss2 | +0.0070 | 11.7% |
| 272 | ss2 | +0.0067 | 11.1% |

**Query mass** (top-1=23%, top-2=41%, top-3=55%)  [DISTR(G267/T157/A161/G272/V159)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 267 | ss2 | +0.0141 | 23.3% |
| 157 | ss1 | +0.0107 | 17.8% |
| 161 | ss1 | +0.0086 | 14.2% |
| 272 | ss2 | +0.0070 | 11.6% |
| 159 | ss1 | +0.0063 | 10.4% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 4 | 20.0% |
| -109 | 3 | 15.0% |
| -110 | 3 | 15.0% |
| +109 | 3 | 15.0% |
| +111 | 2 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 12 | 60.0% |
| ss1 | ss2 | 8 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 157 | ss1 | 266 | ss2 | +0.0070 | 0.0835 |
| 267 | ss2 | 157 | ss1 | +0.0066 | 0.1075 |
| 159 | ss1 | 269 | ss2 | +0.0063 | 0.0259 |
| 272 | ss2 | 161 | ss1 | +0.0057 | 0.0414 |
| 161 | ss1 | 272 | ss2 | +0.0052 | 0.0380 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #16 | L0 | H13 | 43 | +0.0473 | DISTRIBUTED |  | DISTRIBUTED | D109/V144/Q120/I268/W145 |  | INTRA:flkL |
| #27 | L5 | H13 | 20 | +0.0351 | DISTRIBUTED | L113/A118/D109 | DISTRIBUTED | V144/V269/L299 |  |  |
| #3 | L6 | H19 | 8 | +0.1747 | DUAL-ANCHOR | V144/L299 | DUAL-ANCHOR | V269/I115 |  |  |
| #1 | L7 | H0 | 8 | +0.1667 | SINGLE-ANCHOR | V144 | DUAL-ANCHOR | I115/L114 |  | INTRA:flkL |
| #22 | L8 | H0 | 30 | +0.0983 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #5 | L8 | H12 | 8 | +0.2238 | SINGLE-ANCHOR | V269 | DUAL-ANCHOR | V159/I158 |  | ss1→flkL |
| #21 | L9 | H12 | 6 | +0.0137 | SINGLE-ANCHOR | L114 | DISTRIBUTED | I158/I115/V159 |  | ss1→flkL |
| #29 | L9 | H14 | 31 | +0.0930 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #13 | L10 | H9 | 32 | +0.0851 | MULTI-ANCHOR |  | DISTRIBUTED | I158/V269/L114/A161 |  |  |
| #20 | L10 | H12 | 45 | +0.1070 | SINGLE-ANCHOR | I115 | DISTRIBUTED |  |  |  |
| #15 | L11 | H10 | 49 | +0.1043 | DISTRIBUTED |  | DISTRIBUTED | I158/V159/V160 |  |  |
| #12 | L11 | H11 | 60 | +0.1016 | DISTRIBUTED |  | SINGLE-ANCHOR | V269 |  |  |
| #25 | L11 | H14 | 17 | +0.0791 | DUAL-ANCHOR | V269/I115 | DUAL-ANCHOR | I158/V159 |  |  |
| #11 | L11 | H16 | 15 | +0.0242 | SINGLE-ANCHOR | V269 | DISTRIBUTED | I158/V159/V160/V269 |  |  |
| #9 | L12 | H2 | 26 | +0.1087 | SINGLE-ANCHOR | V269 | DISTRIBUTED | I158/V159/V160 |  |  |
| #30 | L12 | H3 | 9 | +0.0277 | SINGLE-ANCHOR | L299 | DUAL-ANCHOR | I158/V269 |  | CROSS:ss1→flkR |
| #4 | L12 | H8 | 32 | +0.1350 | DUAL-ANCHOR | L114/V269 | DUAL-ANCHOR | I158/V159 |  |  |
| #18 | L13 | H13 | 7 | +0.0606 | SINGLE-ANCHOR | V269 | SINGLE-ANCHOR | I158 |  | CROSS:ss1→ss2 |
| #26 | L14 | H9 | 34 | +0.0620 | DUAL-ANCHOR | L114/V269 | DISTRIBUTED |  |  |  |
| #24 | L15 | H7 | 14 | +0.0749 | DISTRIBUTED | V160/V159/I158/A161 | DISTRIBUTED | V160/I158/V159 | POSITIONAL | INTRA:ss1 |
| #17 | L17 | H1 | 19 | +0.0707 | SINGLE-ANCHOR | V269 | DISTRIBUTED | V160/N163/V159 |  | CROSS:ss1→ss2 |
| #19 | L21 | H4 | 10 | +0.0619 | SINGLE-ANCHOR | V160 | SINGLE-ANCHOR | I158 |  | INTRA:ss1 |
| #6 | L22 | H14 | 28 | +0.0738 | DISTRIBUTED | V269/I158/G267/A161 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #28 | L23 | H18 | 8 | +0.0373 | DUAL-ANCHOR | N163/V147 | DUAL-ANCHOR | V160/I158 |  | ss1→flkL |
| #8 | L26 | H16 | 18 | +0.0529 | DISTRIBUTED |  | DISTRIBUTED | A161/V159/V160/T157 |  | CROSS:ss1→ss2 |
| #14 | L27 | H15 | 16 | +0.0379 | DISTRIBUTED | V159/V160/I158/V270 | DISTRIBUTED | V270/G267/V269/T157 |  |  |
| #23 | L29 | H18 | 19 | +0.0334 | DISTRIBUTED | A266/I257/N265/?-1/Y155 | DISTRIBUTED | A161/V159/T157/G267 |  |  |
| #7 | L30 | H1 | 12 | +0.0640 | SINGLE-ANCHOR | V159 | SINGLE-ANCHOR | V269 |  | CROSS:ss2→ss1 |
| #10 | L32 | H13 | 17 | +0.0341 | DISTRIBUTED | T157/A266/V269/G272/G267 | DISTRIBUTED | T157/A266/G267/V159/N163 |  | CROSS:ss1→ss2 |
| #2 | L32 | H18 | 20 | +0.0603 | DISTRIBUTED |  | DISTRIBUTED | G267/T157/A161/G272/V159 |  | CROSS:ss2→ss1 |
