# Contact Pattern Analysis: 4HZIA

Generated: 2026-03-22 21:45:25   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4HZIA |
| Contact pair | (63, 228) |
| ss1 | [58, 69) |
| ss2 | [223, 234) |
| Clean flank | 33 |
| Corrupt flank | 32 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.8632 |
| Corrupt metric | 0.1481 |
| Gap | 0.7151 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 135 | 72.03% |
| positive IE | 70 | 81.41% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L6 | H13 | +0.4212 |
| 2 | L32 | H13 | +0.2142 |
| 3 | L26 | H16 | +0.2101 |
| 4 | L32 | H18 | +0.1721 |
| 5 | L29 | H18 | +0.1489 |
| 6 | L5 | H9 | +0.1009 |
| 7 | L7 | H0 | +0.0775 |
| 8 | L31 | H17 | +0.0732 |
| 9 | L9 | H17 | +0.0700 |
| 10 | L0 | H19 | +0.0649 |
| 11 | L13 | H18 | +0.0643 |
| 12 | L4 | H17 | +0.0624 |
| 13 | L27 | H15 | +0.0596 |
| 14 | L3 | H19 | +0.0465 |
| 15 | L30 | H13 | +0.0454 |
| 16 | L30 | H0 | +0.0440 |
| 17 | L1 | H8 | +0.0431 |
| 18 | L30 | H1 | +0.0372 |
| 19 | L13 | H3 | +0.0369 |
| 20 | L20 | H15 | +0.0302 |
| 21 | L17 | H16 | +0.0296 |
| 22 | L6 | H19 | +0.0290 |
| 23 | L0 | H13 | +0.0281 |
| 24 | L13 | H7 | +0.0278 |
| 25 | L16 | H0 | +0.0276 |
| 26 | L3 | H14 | +0.0247 |
| 27 | L14 | H14 | +0.0240 |
| 28 | L16 | H11 | +0.0235 |
| 29 | L15 | H8 | +0.0227 |
| 30 | L13 | H19 | +0.0223 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | -0.48% |
| 3 | 0.62% |
| 4 | 2.82% |
| 5 | 3.93% |
| 6 | 4.30% |
| 7 | 4.13% |
| 8 | 4.66% |
| 9 | 4.76% |
| 10 | 5.15% |
| 20 | 7.34% |
| 80 | 94.01% |
| 450 | 142.35% |

## Cell Attribution Analysis

Total cells: 5,788,151

- Positive: 2,926,571
- Negative: 2,859,221

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000049 | 578,816 |
| 95th | +0.00000148 | 289,408 |
| 99th | +0.00001149 | 57,882 |
| 99.5th | +0.00002474 | 28,941 |
| 99.9th | +0.00012883 | 5,789 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H0 | 200 | other | 227 | ss2 | +1.065014 | 0.412589 |
| L6 | H13 | 227 | ss2 | 243 | flkR | +0.244622 | 0.153538 |
| L6 | H13 | 200 | other | 243 | flkR | +0.126300 | 0.075164 |
| L5 | H9 | 243 | flkR | 249 | flkR | +0.118221 | 0.042235 |
| L11 | H14 | 228 | ss2 | 200 | other | +0.061853 | 0.742652 |
| L4 | H17 | 249 | flkR | 266 | flkR | +0.043050 | 0.046254 |
| L0 | H19 | 25 | flkL | 25 | flkL | +0.038059 | 0.986537 |
| L14 | H12 | 219 | other | 227 | ss2 | +0.031167 | 0.667841 |
| L11 | H14 | 226 | ss2 | 200 | other | +0.029800 | 0.685007 |
| L9 | H17 | 200 | other | 69 | other | +0.028211 | 0.085264 |
| L6 | H19 | 227 | ss2 | 243 | flkR | +0.025501 | 0.060855 |
| L14 | H9 | 227 | ss2 | 64 | ss1 | +0.025049 | 0.322258 |
| L32 | H13 | 223 | ss2 | 59 | ss1 | +0.024287 | 0.183780 |
| L5 | H9 | 244 | flkR | 249 | flkR | +0.024209 | 0.063011 |
| L29 | H18 | 223 | ss2 | 59 | ss1 | +0.023639 | 0.143528 |
| L11 | H14 | 224 | ss2 | 200 | other | +0.022519 | 0.765854 |
| L29 | H18 | 58 | ss1 | 225 | ss2 | +0.020412 | 0.366802 |
| L14 | H14 | 227 | ss2 | 227 | ss2 | +0.020018 | 0.361946 |
| L13 | H3 | 223 | ss2 | 227 | ss2 | +0.019973 | 0.748953 |
| L11 | H14 | 223 | ss2 | 200 | other | +0.019574 | 0.677896 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L20 | H15 | 224 | ss2 | 228 | ss2 | -0.008612 | 0.232184 |
| L16 | H18 | 233 | ss2 | 200 | other | -0.009421 | 0.918561 |
| L11 | H14 | 213 | other | 200 | other | -0.010527 | 0.654176 |
| L6 | H13 | 199 | other | 243 | flkR | -0.012584 | 0.064818 |
| L7 | H6 | 200 | other | 266 | flkR | -0.012645 | 0.038180 |
| L7 | H0 | 202 | other | 227 | ss2 | -0.012678 | 0.347464 |
| L7 | H0 | 200 | other | 228 | ss2 | -0.012906 | 0.015264 |
| L11 | H14 | 222 | other | 200 | other | -0.013516 | 0.723603 |
| L10 | H9 | 200 | other | 64 | ss1 | -0.013590 | 0.281656 |
| L13 | H18 | 223 | ss2 | 200 | other | -0.013981 | 0.263751 |
| L11 | H14 | 217 | other | 200 | other | -0.014029 | 0.709861 |
| L13 | H7 | 228 | ss2 | 200 | other | -0.014559 | 0.695400 |
| L17 | H18 | 227 | ss2 | 200 | other | -0.014693 | 0.590370 |
| L13 | H3 | 226 | ss2 | 227 | ss2 | -0.014779 | 0.434900 |
| L11 | H14 | 225 | ss2 | 200 | other | -0.015348 | 0.718292 |
| L7 | H0 | 197 | other | 227 | ss2 | -0.017552 | 0.351220 |
| L7 | H0 | 198 | other | 227 | ss2 | -0.028260 | 0.392848 |
| L6 | H13 | 201 | other | 243 | flkR | -0.032599 | 0.076933 |
| L7 | H0 | 199 | other | 227 | ss2 | -0.108718 | 0.409353 |
| L7 | H0 | 201 | other | 227 | ss2 | -0.232841 | 0.402999 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.1481 | 0.00% |
| 10 | 10 | 8 | 0.1481 | 0.00% |
| 20 | 20 | 14 | 0.1493 | 0.16% |
| 50 | 50 | 30 | 0.1532 | 0.70% |
| 100 | 100 | 45 | 0.1629 | 2.06% |
| 200 | 200 | 57 | 0.1885 | 5.64% |
| 500 | 500 | 68 | 0.4977 | 48.89% |
| 1000 | 1,000 | 70 | 0.6608 | 71.70% |
| 2000 | 2,000 | 70 | 0.8105 | 92.63% |
| 5000 | 5,000 | 70 | 0.9535 | 112.63% |
| 10000 | 10,000 | 70 | 1.0230 | 122.34% |
| 20000 | 20,000 | 70 | 1.1097 | 134.47% |
| 50000 | 50,000 | 70 | 1.1637 | 142.02% |

## Motif Analysis

### L0 H13 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | INTRA:flkR  |  cells: 4  |  total attr: +0.0044

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 266 | flkR | +0.0044 | 100.0% |

**Query mass** (top-1=32%, top-2=59%, top-3=80%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0014 | 32.0% |
| 245 | flkR | +0.0012 | 27.4% |
| 243 | flkR | +0.0009 | 20.8% |
| 236 | flkR | +0.0009 | 19.8% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -39 | 1 | 25.0% |
| -21 | 1 | 25.0% |
| -23 | 1 | 25.0% |
| -30 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 3 | 75.0% |
| ss2 | flkR | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | ss2 | 266 | flkR | +0.0014 | 0.0017 |
| 245 | flkR | 266 | flkR | +0.0012 | 0.0020 |
| 243 | flkR | 266 | flkR | +0.0009 | 0.0010 |
| 236 | flkR | 266 | flkR | +0.0009 | 0.0021 |

### L0 H19 — Rank #10

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 39  |  total attr: +0.1216

**Key mass** (top-1=34%, top-2=51%, top-3=55%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | flkL | +0.0415 | 34.2% |
| 266 | flkR | +0.0206 | 16.9% |
| 256 | flkR | +0.0046 | 3.8% |
| 264 | flkR | +0.0044 | 3.6% |
| 265 | flkR | +0.0032 | 2.6% |

**Query mass** (top-1=53%, top-2=84%, top-3=90%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 266 | flkR | +0.0640 | 52.7% |
| 25 | flkL | +0.0381 | 31.3% |
| 246 | flkR | +0.0074 | 6.1% |
| 245 | flkR | +0.0045 | 3.7% |
| 224 | ss2 | +0.0026 | 2.1% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 5.1% |
| +224 | 2 | 5.1% |
| -20 | 1 | 2.6% |
| +10 | 1 | 2.6% |
| -21 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 14 | 35.9% |
| flkR | flkL | 14 | 35.9% |
| flkR | ss1 | 4 | 10.3% |
| flkR | ss2 | 3 | 7.7% |
| ss2 | flkR | 2 | 5.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 25 | flkL | 25 | flkL | +0.0381 | 0.9865 |
| 246 | flkR | 266 | flkR | +0.0074 | 0.0122 |
| 266 | flkR | 256 | flkR | +0.0046 | 0.0242 |
| 266 | flkR | 266 | flkR | +0.0045 | 0.0225 |
| 245 | flkR | 266 | flkR | +0.0045 | 0.0114 |

### L1 H8 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:flkR  |  cells: 22  |  total attr: +0.0583

**Key mass** (top-1=18%, top-2=30%, top-3=41%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 255 | flkR | +0.0106 | 18.2% |
| 25 | flkL | +0.0068 | 11.7% |
| 231 | ss2 | +0.0062 | 10.6% |
| 265 | flkR | +0.0060 | 10.3% |
| 266 | flkR | +0.0053 | 9.2% |

**Query mass** (top-1=21%, top-2=39%, top-3=52%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | flkR | +0.0124 | 21.3% |
| 250 | flkR | +0.0106 | 18.1% |
| 227 | ss2 | +0.0074 | 12.8% |
| 256 | flkR | +0.0041 | 7.0% |
| 22 | other | +0.0037 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 73%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 10 | 45.5% |
| -5 | 6 | 27.3% |
| -3 | 6 | 27.3% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=59%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 13 | 59.1% |
| ss2 | ss2 | 3 | 13.6% |
| other | flkL | 3 | 13.6% |
| ss2 | flkR | 1 | 4.5% |
| flkR | other | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 250 | flkR | 255 | flkR | +0.0080 | 0.0155 |
| 227 | ss2 | 231 | ss2 | +0.0062 | 0.0050 |
| 262 | flkR | 265 | flkR | +0.0060 | 0.0375 |
| 262 | flkR | 266 | flkR | +0.0053 | 0.0967 |
| 22 | other | 25 | flkL | +0.0037 | 0.2691 |

### L3 H14 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 9  |  total attr: +0.0224

**Key mass** (top-1=96%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | flkR | +0.0216 | 96.3% |
| 241 | flkR | +0.0008 | 3.7% |

**Query mass** (top-1=41%, top-2=55%, top-3=67%)  [DISTR(L266/L269/Y270/F261)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 266 | flkR | +0.0093 | 41.5% |
| 269 | other | +0.0029 | 13.1% |
| 270 | other | +0.0028 | 12.6% |
| 261 | flkR | +0.0016 | 7.2% |
| 265 | flkR | +0.0015 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 2 | 22.2% |
| +4 | 1 | 11.1% |
| +7 | 1 | 11.1% |
| -1 | 1 | 11.1% |
| +3 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 5 | 55.6% |
| flkR | flkR | 4 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 266 | flkR | 262 | flkR | +0.0093 | 0.1575 |
| 269 | other | 262 | flkR | +0.0029 | 0.1090 |
| 270 | other | 262 | flkR | +0.0028 | 0.1056 |
| 261 | flkR | 262 | flkR | +0.0016 | 0.0422 |
| 265 | flkR | 262 | flkR | +0.0015 | 0.1124 |

### L3 H19 — Rank #14

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR  |  cells: 8  |  total attr: +0.0533

**Key mass** (top-1=37%, top-2=62%, top-3=80%)  [DISTR(T262/Y240/P256)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | flkR | +0.0195 | 36.7% |
| 240 | flkR | +0.0136 | 25.5% |
| 256 | flkR | +0.0094 | 17.7% |
| 247 | flkR | +0.0037 | 7.0% |
| 241 | flkR | +0.0022 | 4.1% |

**Query mass** (top-1=37%, top-2=69%, top-3=86%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 249 | flkR | +0.0195 | 36.7% |
| 227 | ss2 | +0.0171 | 32.1% |
| 243 | flkR | +0.0094 | 17.7% |
| 234 | flkR | +0.0037 | 7.0% |
| 294 | other | +0.0021 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -13 | 5 | 62.5% |
| -14 | 1 | 12.5% |
| +0 | 1 | 12.5% |
| -12 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 3 | 37.5% |
| ss2 | flkR | 3 | 37.5% |
| other | other | 1 | 12.5% |
| flkR | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 249 | flkR | 262 | flkR | +0.0195 | 0.0309 |
| 227 | ss2 | 240 | flkR | +0.0136 | 0.0122 |
| 243 | flkR | 256 | flkR | +0.0094 | 0.0218 |
| 234 | flkR | 247 | flkR | +0.0037 | 0.0176 |
| 227 | ss2 | 241 | flkR | +0.0022 | 0.0024 |

### L4 H17 — Rank #12

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | ss2→flkR  |  cells: 12  |  total attr: +0.0926

**Key mass** (top-1=46%, top-2=68%, top-3=76%)  [DISTR(L266/I252/F261)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 266 | flkR | +0.0431 | 46.5% |
| 252 | flkR | +0.0196 | 21.1% |
| 261 | flkR | +0.0075 | 8.1% |
| 243 | flkR | +0.0066 | 7.2% |
| 244 | flkR | +0.0039 | 4.2% |

**Query mass** (top-1=52%, top-2=90%, top-3=96%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 249 | flkR | +0.0486 | 52.5% |
| 227 | ss2 | +0.0343 | 37.0% |
| 243 | flkR | +0.0061 | 6.5% |
| 200 | other | +0.0022 | 2.4% |
| 244 | flkR | +0.0014 | 1.5% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -17 | 3 | 25.0% |
| -25 | 1 | 8.3% |
| -16 | 1 | 8.3% |
| -18 | 1 | 8.3% |
| -20 | 1 | 8.3% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 5 | 41.7% |
| flkR | flkR | 3 | 25.0% |
| flkR | other | 3 | 25.0% |
| other | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 249 | flkR | 266 | flkR | +0.0431 | 0.0463 |
| 227 | ss2 | 252 | flkR | +0.0196 | 0.0168 |
| 227 | ss2 | 243 | flkR | +0.0066 | 0.0027 |
| 243 | flkR | 261 | flkR | +0.0061 | 0.0208 |
| 227 | ss2 | 244 | flkR | +0.0039 | 0.0025 |

### L5 H9 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 8  |  total attr: +0.1597

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 249 | flkR | +0.1597 | 100.0% |

**Query mass** (top-1=74%, top-2=89%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.1182 | 74.0% |
| 244 | flkR | +0.0242 | 15.2% |
| 227 | ss2 | +0.0099 | 6.2% |
| 242 | flkR | +0.0021 | 1.3% |
| 241 | flkR | +0.0021 | 1.3% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 1 | 12.5% |
| -5 | 1 | 12.5% |
| -22 | 1 | 12.5% |
| -7 | 1 | 12.5% |
| -8 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 6 | 75.0% |
| ss2 | flkR | 1 | 12.5% |
| other | flkR | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 243 | flkR | 249 | flkR | +0.1182 | 0.0422 |
| 244 | flkR | 249 | flkR | +0.0242 | 0.0630 |
| 227 | ss2 | 249 | flkR | +0.0099 | 0.0137 |
| 242 | flkR | 249 | flkR | +0.0021 | 0.0443 |
| 241 | flkR | 249 | flkR | +0.0021 | 0.0539 |

### L6 H13 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 10  |  total attr: +0.4022

**Key mass** (top-1=92%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.3720 | 92.5% |
| 244 | flkR | +0.0237 | 5.9% |
| 257 | flkR | +0.0025 | 0.6% |
| 245 | flkR | +0.0018 | 0.4% |
| 64 | ss1 | +0.0013 | 0.3% |

**Query mass** (top-1=63%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.2542 | 63.2% |
| 200 | other | +0.1459 | 36.3% |
| 64 | ss1 | +0.0020 | 0.5% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -16 | 1 | 10.0% |
| -43 | 1 | 10.0% |
| -44 | 1 | 10.0% |
| -17 | 1 | 10.0% |
| -57 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 5 | 50.0% |
| ss2 | flkR | 2 | 20.0% |
| ss1 | flkR | 2 | 20.0% |
| ss2 | ss1 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | ss2 | 243 | flkR | +0.2446 | 0.1535 |
| 200 | other | 243 | flkR | +0.1263 | 0.0752 |
| 200 | other | 244 | flkR | +0.0153 | 0.0126 |
| 227 | ss2 | 244 | flkR | +0.0083 | 0.0058 |
| 200 | other | 257 | flkR | +0.0025 | 0.0038 |

### L6 H19 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.0495

**Key mass** (top-1=75%, top-2=84%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 243 | flkR | +0.0369 | 74.7% |
| 244 | flkR | +0.0045 | 9.1% |
| 294 | other | +0.0039 | 7.9% |
| 251 | flkR | +0.0011 | 2.3% |
| 227 | ss2 | +0.0011 | 2.2% |

**Query mass** (top-1=65%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0321 | 64.8% |
| 200 | other | +0.0161 | 32.4% |
| 64 | ss1 | +0.0014 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -16 | 1 | 9.1% |
| -43 | 1 | 9.1% |
| -17 | 1 | 9.1% |
| -44 | 1 | 9.1% |
| -230 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 36.4% |
| other | flkR | 2 | 18.2% |
| ss1 | other | 1 | 9.1% |
| ss2 | other | 1 | 9.1% |
| other | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | ss2 | 243 | flkR | +0.0255 | 0.0609 |
| 200 | other | 243 | flkR | +0.0114 | 0.0280 |
| 227 | ss2 | 244 | flkR | +0.0031 | 0.0100 |
| 200 | other | 244 | flkR | +0.0014 | 0.0053 |
| 64 | ss1 | 294 | other | +0.0014 | 0.0187 |

### L7 H0 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 47  |  total attr: +1.1638

**Key mass** (top-1=92%, top-2=92%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +1.0666 | 91.7% |
| 243 | flkR | +0.0066 | 0.6% |
| 59 | ss1 | +0.0050 | 0.4% |
| 241 | flkR | +0.0048 | 0.4% |
| 248 | flkR | +0.0044 | 0.4% |

**Query mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | other | +1.1575 | 99.5% |
| 201 | other | +0.0022 | 0.2% |
| 64 | ss1 | +0.0016 | 0.1% |
| 227 | ss2 | +0.0014 | 0.1% |
| 199 | other | +0.0011 | 0.1% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -27 | 2 | 4.3% |
| -43 | 1 | 2.1% |
| +141 | 1 | 2.1% |
| -41 | 1 | 2.1% |
| -48 | 1 | 2.1% |

**Region-pair profile** (q→k)  (top=49%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 23 | 48.9% |
| other | flkL | 9 | 19.1% |
| other | ss2 | 7 | 14.9% |
| other | ss1 | 4 | 8.5% |
| other | other | 2 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | other | 227 | ss2 | +1.0650 | 0.4126 |
| 200 | other | 243 | flkR | +0.0066 | 0.0154 |
| 200 | other | 59 | ss1 | +0.0050 | 0.0029 |
| 200 | other | 241 | flkR | +0.0048 | 0.0106 |
| 200 | other | 248 | flkR | +0.0044 | 0.0059 |

### L9 H17 — Rank #9

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 18  |  total attr: +0.1142

**Key mass** (top-1=26%, top-2=42%, top-3=58%)  [DISTR(G69/G71/K72/N68)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 69 | other | +0.0297 | 26.0% |
| 71 | other | +0.0188 | 16.5% |
| 72 | other | +0.0179 | 15.6% |
| 68 | ss1 | +0.0172 | 15.1% |
| 73 | other | +0.0131 | 11.5% |

**Query mass** (top-1=92%, top-2=95%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | other | +0.1050 | 92.0% |
| 64 | ss1 | +0.0032 | 2.8% |
| 69 | other | +0.0018 | 1.6% |
| 68 | ss1 | +0.0014 | 1.2% |
| 60 | ss1 | +0.0010 | 0.9% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +131 | 1 | 5.6% |
| +128 | 1 | 5.6% |
| +132 | 1 | 5.6% |
| +129 | 1 | 5.6% |
| +127 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 11 | 61.1% |
| other | ss1 | 3 | 16.7% |
| ss1 | other | 3 | 16.7% |
| ss1 | ss1 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | other | 69 | other | +0.0282 | 0.0853 |
| 200 | other | 72 | other | +0.0179 | 0.0552 |
| 200 | other | 68 | ss1 | +0.0155 | 0.0457 |
| 200 | other | 71 | other | +0.0138 | 0.0432 |
| 200 | other | 73 | other | +0.0121 | 0.0376 |

### L13 H3 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.0966

**Key mass** (top-1=80%, top-2=87%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0775 | 80.3% |
| 200 | other | +0.0070 | 7.2% |
| 243 | flkR | +0.0037 | 3.8% |
| 64 | ss1 | +0.0033 | 3.4% |
| 249 | flkR | +0.0017 | 1.7% |

**Query mass** (top-1=21%, top-2=35%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 223 | ss2 | +0.0200 | 20.7% |
| 225 | ss2 | +0.0139 | 14.4% |
| 231 | ss2 | +0.0119 | 12.3% |
| 230 | ss2 | +0.0097 | 10.0% |
| 201 | other | +0.0070 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 13.6% |
| +0 | 3 | 13.6% |
| -4 | 2 | 9.1% |
| +4 | 2 | 9.1% |
| +6 | 2 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 8 | 36.4% |
| flkR | flkR | 4 | 18.2% |
| other | other | 3 | 13.6% |
| flkR | ss2 | 2 | 9.1% |
| other | ss2 | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 227 | ss2 | +0.0200 | 0.7490 |
| 225 | ss2 | 227 | ss2 | +0.0139 | 0.7218 |
| 231 | ss2 | 227 | ss2 | +0.0119 | 0.9575 |
| 230 | ss2 | 227 | ss2 | +0.0097 | 0.9010 |
| 228 | ss2 | 227 | ss2 | +0.0063 | 0.1737 |

### L13 H7 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0470

**Key mass** (top-1=85%, top-2=90%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | other | +0.0398 | 84.5% |
| 264 | flkR | +0.0026 | 5.6% |
| 250 | flkR | +0.0024 | 5.1% |
| 262 | flkR | +0.0014 | 2.9% |
| 252 | flkR | +0.0009 | 1.8% |

**Query mass** (top-1=34%, top-2=54%, top-3=68%)  [DISTR(L227/S226/T225/I229)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0162 | 34.4% |
| 226 | ss2 | +0.0092 | 19.5% |
| 225 | ss2 | +0.0065 | 13.7% |
| 229 | ss2 | +0.0052 | 11.0% |
| 223 | ss2 | +0.0047 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +27 | 1 | 10.0% |
| +26 | 1 | 10.0% |
| +29 | 1 | 10.0% |
| +25 | 1 | 10.0% |
| -29 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 6 | 60.0% |
| ss2 | flkR | 3 | 30.0% |
| flkR | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | ss2 | 200 | other | +0.0162 | 0.9189 |
| 226 | ss2 | 200 | other | +0.0092 | 0.4863 |
| 229 | ss2 | 200 | other | +0.0052 | 0.6741 |
| 225 | ss2 | 200 | other | +0.0051 | 0.2530 |
| 235 | flkR | 264 | flkR | +0.0026 | 0.6370 |

### L13 H18 — Rank #11

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 40  |  total attr: +0.1073

**Key mass** (top-1=60%, top-2=96%, top-3=99%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0639 | 59.6% |
| 200 | other | +0.0391 | 36.4% |
| 227 | ss2 | +0.0033 | 3.1% |
| 249 | flkR | +0.0011 | 1.0% |

**Query mass** (top-1=14%, top-2=24%, top-3=32%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 223 | ss2 | +0.0153 | 14.3% |
| 228 | ss2 | +0.0103 | 9.6% |
| 225 | ss2 | +0.0088 | 8.2% |
| 229 | ss2 | +0.0071 | 6.6% |
| 219 | other | +0.0069 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +67 | 2 | 5.0% |
| +66 | 2 | 5.0% |
| +159 | 1 | 2.5% |
| +164 | 1 | 2.5% |
| +161 | 1 | 2.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 15 | 37.5% |
| other | other | 9 | 22.5% |
| ss2 | ss1 | 7 | 17.5% |
| other | ss1 | 3 | 7.5% |
| other | ss2 | 2 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 64 | ss1 | +0.0153 | 0.4483 |
| 228 | ss2 | 64 | ss1 | +0.0092 | 0.3726 |
| 225 | ss2 | 64 | ss1 | +0.0088 | 0.3878 |
| 219 | other | 64 | ss1 | +0.0069 | 0.4564 |
| 227 | ss2 | 64 | ss1 | +0.0063 | 0.4741 |

### L13 H19 — Rank #30

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 7  |  total attr: +0.0104

**Key mass** (top-1=45%, top-2=82%, top-3=91%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0047 | 45.0% |
| 200 | other | +0.0039 | 37.4% |
| 64 | ss1 | +0.0009 | 9.1% |
| -1 | other | +0.0009 | 8.6% |

**Query mass** (top-1=48%, top-2=72%, top-3=82%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 294 | other | +0.0050 | 48.1% |
| 293 | other | +0.0025 | 24.2% |
| 266 | flkR | +0.0010 | 10.1% |
| 227 | ss2 | +0.0009 | 9.1% |
| -1 | other | +0.0009 | 8.6% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +66 | 2 | 28.6% |
| +67 | 1 | 14.3% |
| +94 | 1 | 14.3% |
| +163 | 1 | 14.3% |
| +93 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 3 | 42.9% |
| other | ss2 | 2 | 28.6% |
| flkR | other | 1 | 14.3% |
| ss2 | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 294 | other | 227 | ss2 | +0.0031 | 0.5149 |
| 294 | other | 200 | other | +0.0019 | 0.0829 |
| 293 | other | 227 | ss2 | +0.0016 | 0.3030 |
| 266 | flkR | 200 | other | +0.0010 | 0.3204 |
| 227 | ss2 | 64 | ss1 | +0.0009 | 0.0417 |

### L14 H14 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:ss2  |  cells: 12  |  total attr: +0.0407

**Key mass** (top-1=73%, top-2=79%, top-3=83%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0297 | 72.9% |
| 228 | ss2 | +0.0024 | 6.0% |
| 225 | ss2 | +0.0017 | 4.1% |
| 226 | ss2 | +0.0016 | 4.0% |
| 233 | ss2 | +0.0015 | 3.6% |

**Query mass** (top-1=57%, top-2=74%, top-3=83%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0233 | 57.2% |
| 232 | ss2 | +0.0070 | 17.2% |
| 231 | ss2 | +0.0033 | 8.1% |
| 229 | ss2 | +0.0028 | 6.9% |
| 240 | flkR | +0.0026 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 3 | 25.0% |
| +5 | 2 | 16.7% |
| +7 | 2 | 16.7% |
| +0 | 1 | 8.3% |
| -1 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 8 | 66.7% |
| flkR | ss2 | 2 | 16.7% |
| ss2 | other | 1 | 8.3% |
| flkR | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | ss2 | 227 | ss2 | +0.0200 | 0.3619 |
| 232 | ss2 | 227 | ss2 | +0.0070 | 0.6711 |
| 227 | ss2 | 228 | ss2 | +0.0024 | 0.0725 |
| 229 | ss2 | 227 | ss2 | +0.0018 | 0.1487 |
| 231 | ss2 | 225 | ss2 | +0.0017 | 0.2174 |

### L15 H8 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0266

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0266 | 100.0% |

**Query mass** (top-1=25%, top-2=48%, top-3=62%)  [DISTR(C200/L227/L64/H231)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | other | +0.0066 | 24.7% |
| 227 | ss2 | +0.0062 | 23.4% |
| 64 | ss1 | +0.0037 | 13.7% |
| 231 | ss2 | +0.0029 | 11.0% |
| 224 | ss2 | +0.0022 | 8.4% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +136 | 1 | 12.5% |
| +163 | 1 | 12.5% |
| +0 | 1 | 12.5% |
| +167 | 1 | 12.5% |
| +160 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 50.0% |
| other | ss1 | 3 | 37.5% |
| ss1 | ss1 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | other | 64 | ss1 | +0.0066 | 0.4296 |
| 227 | ss2 | 64 | ss1 | +0.0062 | 0.1637 |
| 64 | ss1 | 64 | ss1 | +0.0037 | 0.1606 |
| 231 | ss2 | 64 | ss1 | +0.0029 | 0.3048 |
| 224 | ss2 | 64 | ss1 | +0.0022 | 0.1682 |

### L16 H0 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 12  |  total attr: +0.0339

**Key mass** (top-1=66%, top-2=78%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0223 | 65.8% |
| 219 | other | +0.0042 | 12.4% |
| 224 | ss2 | +0.0026 | 7.6% |
| 59 | ss1 | +0.0012 | 3.4% |
| 218 | other | +0.0010 | 3.0% |

**Query mass** (top-1=43%, top-2=60%, top-3=76%)  [DISTR(S226/L227/Y228)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 226 | ss2 | +0.0146 | 43.0% |
| 227 | ss2 | +0.0056 | 16.5% |
| 228 | ss2 | +0.0056 | 16.4% |
| 219 | other | +0.0044 | 13.0% |
| 223 | ss2 | +0.0017 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 4 | 33.3% |
| +1 | 2 | 16.7% |
| +4 | 2 | 16.7% |
| +2 | 2 | 16.7% |
| -1 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 50.0% |
| other | other | 2 | 16.7% |
| ss2 | other | 2 | 16.7% |
| ss1 | ss1 | 1 | 8.3% |
| flkL | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 226 | ss2 | 227 | ss2 | +0.0133 | 0.3076 |
| 227 | ss2 | 227 | ss2 | +0.0056 | 0.1522 |
| 219 | other | 219 | other | +0.0034 | 0.2809 |
| 228 | ss2 | 227 | ss2 | +0.0034 | 0.1117 |
| 228 | ss2 | 224 | ss2 | +0.0013 | 0.0838 |

### L16 H11 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0322

**Key mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | other | +0.0314 | 97.3% |
| 201 | other | +0.0009 | 2.7% |

**Query mass** (top-1=35%, top-2=51%, top-3=62%)  [DISTR(K223/L227/T225/I229/P237)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 223 | ss2 | +0.0112 | 34.6% |
| 227 | ss2 | +0.0052 | 16.2% |
| 225 | ss2 | +0.0036 | 11.3% |
| 229 | ss2 | +0.0023 | 7.0% |
| 237 | flkR | +0.0018 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +23 | 1 | 7.7% |
| +27 | 1 | 7.7% |
| +25 | 1 | 7.7% |
| +29 | 1 | 7.7% |
| +37 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 7 | 53.8% |
| ss2 | other | 5 | 38.5% |
| other | other | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 200 | other | +0.0103 | 0.4665 |
| 227 | ss2 | 200 | other | +0.0052 | 0.8364 |
| 225 | ss2 | 200 | other | +0.0036 | 0.3823 |
| 229 | ss2 | 200 | other | +0.0023 | 0.7274 |
| 237 | flkR | 200 | other | +0.0018 | 0.1830 |

### L17 H16 — Rank #21

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | INTRA:ss2  |  cells: 25  |  total attr: +0.0680

**Key mass** (top-1=25%, top-2=39%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0173 | 25.4% |
| 200 | other | +0.0091 | 13.3% |
| 231 | ss2 | +0.0086 | 12.7% |
| 233 | ss2 | +0.0073 | 10.8% |
| 228 | ss2 | +0.0037 | 5.5% |

**Query mass** (top-1=54%, top-2=71%, top-3=79%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 228 | ss2 | +0.0370 | 54.4% |
| 226 | ss2 | +0.0111 | 16.3% |
| 232 | ss2 | +0.0058 | 8.5% |
| 217 | other | +0.0028 | 4.1% |
| 223 | ss2 | +0.0025 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 12.0% |
| +2 | 3 | 12.0% |
| -3 | 2 | 8.0% |
| -6 | 2 | 8.0% |
| -7 | 2 | 8.0% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 11 | 44.0% |
| ss2 | other | 6 | 24.0% |
| ss2 | flkR | 3 | 12.0% |
| other | other | 3 | 12.0% |
| ss1 | ss1 | 1 | 4.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 228 | ss2 | 232 | ss2 | +0.0093 | 0.2248 |
| 228 | ss2 | 231 | ss2 | +0.0086 | 0.1368 |
| 226 | ss2 | 232 | ss2 | +0.0069 | 0.1812 |
| 232 | ss2 | 200 | other | +0.0046 | 0.6811 |
| 228 | ss2 | 233 | ss2 | +0.0041 | 0.0693 |

### L20 H15 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:MULTI-ANCHOR | POSITIONAL | INTRA:ss2  |  cells: 12  |  total attr: +0.0582

**Key mass** (top-1=45%, top-2=73%, top-3=83%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss2 | +0.0264 | 45.4% |
| 228 | ss2 | +0.0160 | 27.5% |
| 230 | ss2 | +0.0058 | 10.0% |
| 231 | ss2 | +0.0021 | 3.5% |
| 241 | flkR | +0.0020 | 3.4% |

**Query mass** (top-1=37%, top-2=63%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss2 | +0.0218 | 37.4% |
| 223 | ss2 | +0.0151 | 25.9% |
| 224 | ss2 | +0.0105 | 18.0% |
| 229 | ss2 | +0.0023 | 4.0% |
| 227 | ss2 | +0.0021 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 83%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 7 | 58.3% |
| -4 | 3 | 25.0% |
| -11 | 1 | 8.3% |
| +2 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 50.0% |
| flkR | flkR | 2 | 16.7% |
| other | ss2 | 2 | 16.7% |
| ss2 | flkR | 2 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | ss2 | 229 | ss2 | +0.0160 | 0.3689 |
| 223 | ss2 | 228 | ss2 | +0.0151 | 0.4077 |
| 224 | ss2 | 229 | ss2 | +0.0105 | 0.2951 |
| 225 | ss2 | 230 | ss2 | +0.0058 | 0.5830 |
| 227 | ss2 | 231 | ss2 | +0.0021 | 0.2502 |

### L26 H16 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 30  |  total attr: +0.1020

**Key mass** (top-1=19%, top-2=33%, top-3=42%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0194 | 19.0% |
| 60 | ss1 | +0.0140 | 13.7% |
| 61 | ss1 | +0.0097 | 9.5% |
| 226 | ss2 | +0.0093 | 9.1% |
| 62 | ss1 | +0.0091 | 8.9% |

**Query mass** (top-1=17%, top-2=33%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss2 | +0.0177 | 17.4% |
| 64 | ss1 | +0.0161 | 15.8% |
| 228 | ss2 | +0.0152 | 14.9% |
| 61 | ss1 | +0.0093 | 9.1% |
| 223 | ss2 | +0.0093 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -165 | 5 | 16.7% |
| +165 | 4 | 13.3% |
| +0 | 3 | 10.0% |
| -163 | 2 | 6.7% |
| -24 | 2 | 6.7% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 30.0% |
| ss2 | flkR | 8 | 26.7% |
| ss2 | ss1 | 7 | 23.3% |
| ss1 | ss1 | 2 | 6.7% |
| flkL | ss2 | 2 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | ss2 | 60 | ss1 | +0.0131 | 0.2514 |
| 64 | ss1 | 227 | ss2 | +0.0113 | 0.1562 |
| 227 | ss2 | 62 | ss1 | +0.0091 | 0.4208 |
| 61 | ss1 | 226 | ss2 | +0.0084 | 0.4053 |
| 60 | ss1 | 225 | ss2 | +0.0059 | 0.0622 |

### L27 H15 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.0473

**Key mass** (top-1=30%, top-2=53%, top-3=70%)  [DISTR(L64/T225/L227/Y228)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0142 | 29.9% |
| 225 | ss2 | +0.0111 | 23.5% |
| 227 | ss2 | +0.0077 | 16.2% |
| 228 | ss2 | +0.0054 | 11.5% |
| 244 | flkR | +0.0031 | 6.5% |

**Query mass** (top-1=35%, top-2=53%, top-3=63%)  [DISTR(L227/E60/L64/T225)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 227 | ss2 | +0.0164 | 34.7% |
| 60 | ss1 | +0.0088 | 18.6% |
| 64 | ss1 | +0.0044 | 9.3% |
| 225 | ss2 | +0.0039 | 8.3% |
| 62 | ss1 | +0.0031 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +163 | 2 | 13.3% |
| -165 | 2 | 13.3% |
| -163 | 2 | 13.3% |
| -167 | 2 | 13.3% |
| -182 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 40.0% |
| ss2 | ss1 | 3 | 20.0% |
| ss2 | ss2 | 2 | 13.3% |
| ss1 | flkR | 1 | 6.7% |
| flkL | ss2 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 227 | ss2 | 64 | ss1 | +0.0142 | 0.1074 |
| 60 | ss1 | 225 | ss2 | +0.0088 | 0.0627 |
| 64 | ss1 | 227 | ss2 | +0.0044 | 0.0282 |
| 62 | ss1 | 244 | flkR | +0.0031 | 0.4754 |
| 61 | ss1 | 228 | ss2 | +0.0029 | 0.0286 |

### L29 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 53  |  total attr: +0.1907

**Key mass** (top-1=17%, top-2=30%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss2 | +0.0326 | 17.1% |
| 59 | ss1 | +0.0252 | 13.2% |
| 58 | ss1 | +0.0180 | 9.4% |
| 61 | ss1 | +0.0120 | 6.3% |
| 64 | ss1 | +0.0119 | 6.2% |

**Query mass** (top-1=26%, top-2=38%, top-3=49%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 223 | ss2 | +0.0505 | 26.5% |
| 58 | ss1 | +0.0220 | 11.6% |
| 228 | ss2 | +0.0212 | 11.1% |
| 64 | ss1 | +0.0177 | 9.3% |
| 227 | ss2 | +0.0166 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +164 | 3 | 5.7% |
| -165 | 3 | 5.7% |
| -180 | 3 | 5.7% |
| +165 | 2 | 3.8% |
| -163 | 2 | 3.8% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 12 | 22.6% |
| ss1 | ss2 | 8 | 15.1% |
| ss1 | flkR | 8 | 15.1% |
| ss2 | other | 8 | 15.1% |
| ss2 | flkL | 5 | 9.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 59 | ss1 | +0.0236 | 0.1435 |
| 58 | ss1 | 225 | ss2 | +0.0204 | 0.3668 |
| 223 | ss2 | 58 | ss1 | +0.0155 | 0.1271 |
| 64 | ss1 | 227 | ss2 | +0.0115 | 0.1401 |
| 59 | ss1 | 225 | ss2 | +0.0089 | 0.3848 |

### L30 H0 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0367

**Key mass** (top-1=63%, top-2=72%, top-3=79%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss2 | +0.0231 | 62.8% |
| 229 | ss2 | +0.0033 | 9.0% |
| 227 | ss2 | +0.0028 | 7.6% |
| 243 | flkR | +0.0022 | 6.0% |
| 228 | ss2 | +0.0021 | 5.7% |

**Query mass** (top-1=30%, top-2=53%, top-3=72%)  [DISTR(T58/E60/L227)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 58 | ss1 | +0.0109 | 29.6% |
| 60 | ss1 | +0.0087 | 23.6% |
| 227 | ss2 | +0.0071 | 19.3% |
| 59 | ss1 | +0.0036 | 9.7% |
| 61 | ss1 | +0.0035 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 2 | 18.2% |
| -165 | 1 | 9.1% |
| -166 | 1 | 9.1% |
| -2 | 1 | 9.1% |
| -16 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 36.4% |
| ss2 | ss2 | 3 | 27.3% |
| ss2 | flkR | 1 | 9.1% |
| ss1 | flkR | 1 | 9.1% |
| ss1 | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 58 | ss1 | 225 | ss2 | +0.0109 | 0.3815 |
| 60 | ss1 | 225 | ss2 | +0.0087 | 0.2520 |
| 59 | ss1 | 225 | ss2 | +0.0036 | 0.2693 |
| 227 | ss2 | 229 | ss2 | +0.0033 | 0.1438 |
| 227 | ss2 | 243 | flkR | +0.0022 | 0.0679 |

### L30 H1 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 10  |  total attr: +0.0276

**Key mass** (top-1=34%, top-2=67%, top-3=75%)  [DISTR(L64/K223/H61)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0094 | 33.9% |
| 223 | ss2 | +0.0090 | 32.7% |
| 61 | ss1 | +0.0024 | 8.8% |
| 62 | ss1 | +0.0018 | 6.6% |
| 228 | ss2 | +0.0011 | 4.2% |

**Query mass** (top-1=34%, top-2=61%, top-3=73%)  [DISTR(I229/N59/Y228)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss2 | +0.0094 | 33.9% |
| 59 | ss1 | +0.0076 | 27.5% |
| 228 | ss2 | +0.0033 | 12.1% |
| 227 | ss2 | +0.0018 | 6.6% |
| 58 | ss1 | +0.0014 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +165 | 3 | 30.0% |
| -164 | 1 | 10.0% |
| +167 | 1 | 10.0% |
| -165 | 1 | 10.0% |
| -167 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 50.0% |
| ss1 | ss2 | 3 | 30.0% |
| ss2 | ss2 | 1 | 10.0% |
| ss2 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 229 | ss2 | 64 | ss1 | +0.0094 | 0.2561 |
| 59 | ss1 | 223 | ss2 | +0.0076 | 0.1103 |
| 228 | ss2 | 61 | ss1 | +0.0024 | 0.0239 |
| 227 | ss2 | 62 | ss1 | +0.0018 | 0.3881 |
| 58 | ss1 | 223 | ss2 | +0.0014 | 0.0588 |

### L30 H13 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0403

**Key mass** (top-1=31%, top-2=50%, top-3=57%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0123 | 30.6% |
| 228 | ss2 | +0.0078 | 19.4% |
| 229 | ss2 | +0.0028 | 7.0% |
| 68 | ss1 | +0.0027 | 6.7% |
| 231 | ss2 | +0.0022 | 5.4% |

**Query mass** (top-1=31%, top-2=58%, top-3=74%)  [DISTR(Y228/H61/L227)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 228 | ss2 | +0.0123 | 30.6% |
| 61 | ss1 | +0.0110 | 27.4% |
| 227 | ss2 | +0.0066 | 16.3% |
| 231 | ss2 | +0.0027 | 6.7% |
| 225 | ss2 | +0.0027 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +167 | 2 | 12.5% |
| +162 | 2 | 12.5% |
| -167 | 1 | 6.2% |
| +163 | 1 | 6.2% |
| -163 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 37.5% |
| ss1 | ss2 | 3 | 18.8% |
| ss1 | flkR | 3 | 18.8% |
| ss2 | ss2 | 3 | 18.8% |
| ss2 | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 228 | ss2 | 61 | ss1 | +0.0123 | 0.2241 |
| 61 | ss1 | 228 | ss2 | +0.0070 | 0.1470 |
| 231 | ss2 | 68 | ss1 | +0.0027 | 0.1364 |
| 68 | ss1 | 231 | ss2 | +0.0022 | 0.1743 |
| 61 | ss1 | 261 | flkR | +0.0020 | 0.0755 |

### L31 H17 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0673

**Key mass** (top-1=18%, top-2=33%, top-3=48%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0124 | 18.4% |
| 59 | ss1 | +0.0101 | 15.0% |
| 228 | ss2 | +0.0099 | 14.6% |
| 223 | ss2 | +0.0073 | 10.9% |
| 68 | ss1 | +0.0051 | 7.6% |

**Query mass** (top-1=15%, top-2=28%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 223 | ss2 | +0.0101 | 15.0% |
| 61 | ss1 | +0.0086 | 12.8% |
| 33 | flkL | +0.0058 | 8.6% |
| 240 | flkR | +0.0055 | 8.2% |
| 231 | ss2 | +0.0051 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -164 | 2 | 7.7% |
| -163 | 2 | 7.7% |
| +164 | 1 | 3.8% |
| -167 | 1 | 3.8% |
| +163 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 30.8% |
| ss2 | ss1 | 5 | 19.2% |
| ss2 | other | 3 | 11.5% |
| ss1 | flkR | 2 | 7.7% |
| flkL | other | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 59 | ss1 | +0.0101 | 0.1625 |
| 61 | ss1 | 228 | ss2 | +0.0063 | 0.2226 |
| 231 | ss2 | 68 | ss1 | +0.0051 | 0.2148 |
| 229 | ss2 | -1 | other | +0.0038 | 0.2297 |
| 58 | ss1 | 223 | ss2 | +0.0037 | 0.1190 |

### L32 H13 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 18  |  total attr: +0.1285

**Key mass** (top-1=19%, top-2=34%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0243 | 18.9% |
| 223 | ss2 | +0.0197 | 15.4% |
| 64 | ss1 | +0.0162 | 12.6% |
| 61 | ss1 | +0.0162 | 12.6% |
| 227 | ss2 | +0.0120 | 9.3% |

**Query mass** (top-1=21%, top-2=38%, top-3=52%)  [DISTR(K223/L64/N59/Y228/L227)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 223 | ss2 | +0.0273 | 21.3% |
| 64 | ss1 | +0.0213 | 16.5% |
| 59 | ss1 | +0.0176 | 13.7% |
| 228 | ss2 | +0.0150 | 11.7% |
| 227 | ss2 | +0.0112 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -165 | 3 | 16.7% |
| +165 | 3 | 16.7% |
| +167 | 2 | 11.1% |
| -163 | 2 | 11.1% |
| +163 | 2 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 50.0% |
| ss1 | ss2 | 9 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 223 | ss2 | 59 | ss1 | +0.0243 | 0.1838 |
| 59 | ss1 | 223 | ss2 | +0.0176 | 0.1334 |
| 228 | ss2 | 61 | ss1 | +0.0150 | 0.1012 |
| 64 | ss1 | 227 | ss2 | +0.0120 | 0.0681 |
| 227 | ss2 | 64 | ss1 | +0.0112 | 0.0635 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.1015

**Key mass** (top-1=26%, top-2=39%, top-3=53%)  [DISTR(T225/L64/T58/N68/N59)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss2 | +0.0264 | 26.0% |
| 64 | ss1 | +0.0137 | 13.5% |
| 58 | ss1 | +0.0135 | 13.3% |
| 68 | ss1 | +0.0134 | 13.2% |
| 59 | ss1 | +0.0077 | 7.6% |

**Query mass** (top-1=19%, top-2=37%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss2 | +0.0196 | 19.3% |
| 60 | ss1 | +0.0183 | 18.0% |
| 231 | ss2 | +0.0134 | 13.2% |
| 64 | ss1 | +0.0096 | 9.5% |
| 58 | ss1 | +0.0081 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -165 | 2 | 13.3% |
| +163 | 2 | 13.3% |
| -167 | 2 | 13.3% |
| +165 | 2 | 13.3% |
| -163 | 2 | 13.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 53.3% |
| ss2 | ss1 | 7 | 46.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 225 | ss2 | +0.0183 | 0.0726 |
| 225 | ss2 | 58 | ss1 | +0.0135 | 0.0844 |
| 231 | ss2 | 68 | ss1 | +0.0134 | 0.0960 |
| 58 | ss1 | 225 | ss2 | +0.0081 | 0.0505 |
| 229 | ss2 | 64 | ss1 | +0.0078 | 0.0797 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #23 | L0 | H13 | 4 | +0.0044 | SINGLE-ANCHOR | L266 | MULTI-ANCHOR |  |  | INTRA:flkR |
| #10 | L0 | H19 | 39 | +0.1216 | DISTRIBUTED |  | DUAL-ANCHOR | L266/Y25 |  |  |
| #17 | L1 | H8 | 22 | +0.0583 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL | INTRA:flkR |
| #26 | L3 | H14 | 9 | +0.0224 | SINGLE-ANCHOR | T262 | DISTRIBUTED | L266/L269/Y270/F261 |  |  |
| #14 | L3 | H19 | 8 | +0.0533 | DISTRIBUTED | T262/Y240/P256 | MULTI-ANCHOR |  |  |  |
| #12 | L4 | H17 | 12 | +0.0926 | DISTRIBUTED | L266/I252/F261 | DUAL-ANCHOR | G249/L227 |  | ss2→flkR |
| #6 | L5 | H9 | 8 | +0.1597 | SINGLE-ANCHOR | G249 | SINGLE-ANCHOR | A243 |  | INTRA:flkR |
| #1 | L6 | H13 | 10 | +0.4022 | SINGLE-ANCHOR | A243 | SINGLE-ANCHOR | L227 |  |  |
| #22 | L6 | H19 | 11 | +0.0495 | SINGLE-ANCHOR | A243 | SINGLE-ANCHOR | L227 |  |  |
| #7 | L7 | H0 | 47 | +1.1638 | SINGLE-ANCHOR | L227 | SINGLE-ANCHOR | C200 |  |  |
| #9 | L9 | H17 | 18 | +0.1142 | DISTRIBUTED | G69/G71/K72/N68 | SINGLE-ANCHOR | C200 |  |  |
| #19 | L13 | H3 | 22 | +0.0966 | SINGLE-ANCHOR | L227 | DISTRIBUTED |  |  |  |
| #24 | L13 | H7 | 10 | +0.0470 | SINGLE-ANCHOR | C200 | DISTRIBUTED | L227/S226/T225/I229 |  |  |
| #11 | L13 | H18 | 40 | +0.1073 | DUAL-ANCHOR | L64/C200 | DISTRIBUTED |  |  |  |
| #30 | L13 | H19 | 7 | +0.0104 | DUAL-ANCHOR | L227/C200 | DUAL-ANCHOR | ?294/Y293 |  |  |
| #27 | L14 | H14 | 12 | +0.0407 | SINGLE-ANCHOR | L227 | DUAL-ANCHOR | L227/R232 |  | INTRA:ss2 |
| #29 | L15 | H8 | 8 | +0.0266 | SINGLE-ANCHOR | L64 | DISTRIBUTED | C200/L227/L64/H231 |  | CROSS:ss2→ss1 |
| #25 | L16 | H0 | 12 | +0.0339 | SINGLE-ANCHOR | L227 | DISTRIBUTED | S226/L227/Y228 | POSITIONAL | INTRA:ss2 |
| #28 | L16 | H11 | 13 | +0.0322 | SINGLE-ANCHOR | C200 | DISTRIBUTED | K223/L227/T225/I229/P237 |  |  |
| #21 | L17 | H16 | 25 | +0.0680 | DISTRIBUTED |  | DUAL-ANCHOR | Y228/S226 |  | INTRA:ss2 |
| #20 | L20 | H15 | 12 | +0.0582 | DUAL-ANCHOR | I229/Y228 | MULTI-ANCHOR |  | POSITIONAL | INTRA:ss2 |
| #3 | L26 | H16 | 30 | +0.1020 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #13 | L27 | H15 | 15 | +0.0473 | DISTRIBUTED | L64/T225/L227/Y228 | DISTRIBUTED | L227/E60/L64/T225 |  | CROSS:ss1→ss2 |
| #5 | L29 | H18 | 53 | +0.1907 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #16 | L30 | H0 | 11 | +0.0367 | SINGLE-ANCHOR | T225 | DISTRIBUTED | T58/E60/L227 |  |  |
| #18 | L30 | H1 | 10 | +0.0276 | DISTRIBUTED | L64/K223/H61 | DISTRIBUTED | I229/N59/Y228 |  | CROSS:ss2→ss1 |
| #15 | L30 | H13 | 16 | +0.0403 | DISTRIBUTED |  | DISTRIBUTED | Y228/H61/L227 |  |  |
| #8 | L31 | H17 | 26 | +0.0673 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #2 | L32 | H13 | 18 | +0.1285 | DISTRIBUTED |  | DISTRIBUTED | K223/L64/N59/Y228/L227 |  | CROSS:ss2→ss1 |
| #4 | L32 | H18 | 15 | +0.1015 | DISTRIBUTED | T225/L64/T58/N68/N59 | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
