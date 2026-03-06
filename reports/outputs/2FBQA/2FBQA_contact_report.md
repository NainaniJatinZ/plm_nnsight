# Contact Pattern Analysis: 2FBQA

Generated: 2026-03-03 05:30:21   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2FBQA |
| Contact pair | (94, 201) |
| ss1 | [89, 100) |
| ss2 | [196, 207) |
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
| Clean metric | 0.8185 |
| Corrupt metric | 0.0130 |
| Gap | 0.8056 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 81.57% |
| positive IE | 140 | 74.20% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L0 | H14 | +0.9999 |
| 2 | L7 | H10 | +0.9996 |
| 3 | L29 | H18 | +0.3586 |
| 4 | L32 | H18 | +0.3219 |
| 5 | L32 | H13 | +0.2762 |
| 6 | L6 | H4 | +0.1740 |
| 7 | L11 | H16 | +0.1662 |
| 8 | L15 | H12 | +0.1424 |
| 9 | L6 | H19 | +0.1421 |
| 10 | L9 | H13 | +0.1254 |
| 11 | L18 | H16 | +0.1236 |
| 12 | L10 | H14 | +0.1099 |
| 13 | L13 | H13 | +0.0895 |
| 14 | L17 | H1 | +0.0841 |
| 15 | L16 | H10 | +0.0837 |
| 16 | L9 | H8 | +0.0811 |
| 17 | L21 | H7 | +0.0811 |
| 18 | L30 | H0 | +0.0559 |
| 19 | L17 | H14 | +0.0542 |
| 20 | L24 | H0 | +0.0515 |
| 21 | L27 | H15 | +0.0513 |
| 22 | L24 | H1 | +0.0489 |
| 23 | L30 | H13 | +0.0487 |
| 24 | L28 | H4 | +0.0471 |
| 25 | L24 | H14 | +0.0469 |
| 26 | L19 | H9 | +0.0459 |
| 27 | L18 | H7 | +0.0419 |
| 28 | L22 | H10 | +0.0409 |
| 29 | L8 | H13 | +0.0393 |
| 30 | L19 | H2 | +0.0391 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | -0.00% |
| 3 | 0.00% |
| 4 | -0.00% |
| 5 | 0.00% |
| 6 | 0.00% |
| 7 | -0.00% |
| 8 | -0.00% |
| 9 | -0.00% |
| 10 | -0.01% |
| 20 | -0.01% |
| 80 | 4.13% |
| 450 | 134.71% |

## Cell Attribution Analysis

Total cells: 7,622,569

- Positive: 3,831,310
- Negative: 3,789,372

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000251 | 762,258 |
| 95th | +0.00000721 | 381,129 |
| 99th | +0.00004868 | 76,226 |
| 99.5th | +0.00009872 | 38,114 |
| 99.9th | +0.00044292 | 7,623 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H4 | 37 | flkL | 32 | flkL | +0.164708 | 0.229405 |
| L7 | H10 | 169 | other | 37 | flkL | +0.131051 | 0.307798 |
| L28 | H4 | 198 | ss2 | 201 | ss2 | +0.104915 | 0.730179 |
| L11 | H16 | 169 | other | 47 | flkL | +0.077893 | 0.309505 |
| L18 | H16 | 198 | ss2 | 43 | flkL | +0.075703 | 0.554330 |
| L6 | H4 | 37 | flkL | 39 | flkL | +0.073480 | 0.068506 |
| L7 | H10 | 170 | other | 37 | flkL | +0.069896 | 0.310071 |
| L17 | H4 | 200 | ss2 | 43 | flkL | +0.068180 | 0.608038 |
| L10 | H14 | 169 | other | 47 | flkL | +0.068142 | 0.179210 |
| L18 | H16 | 201 | ss2 | 43 | flkL | +0.064475 | 0.568762 |
| L29 | H18 | 198 | ss2 | 92 | ss1 | +0.064092 | 0.318691 |
| L18 | H16 | 197 | ss2 | 43 | flkL | +0.058098 | 0.529457 |
| L11 | H16 | 168 | other | 47 | flkL | +0.057408 | 0.392419 |
| L22 | H8 | 201 | ss2 | 204 | ss2 | +0.055378 | 0.479176 |
| L7 | H10 | 172 | other | 37 | flkL | +0.053689 | 0.303813 |
| L11 | H16 | 165 | other | 47 | flkL | +0.053514 | 0.510217 |
| L18 | H16 | 173 | other | 43 | flkL | +0.053350 | 0.998329 |
| L18 | H16 | 169 | other | 43 | flkL | +0.051166 | 0.977305 |
| L17 | H5 | 204 | ss2 | 43 | flkL | +0.050346 | 0.140688 |
| L7 | H10 | 168 | other | 37 | flkL | +0.050324 | 0.320917 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L23 | H18 | 197 | ss2 | 200 | ss2 | -0.018728 | 0.173712 |
| L29 | H18 | 197 | ss2 | 96 | ss1 | -0.019445 | 0.213555 |
| L16 | H7 | 198 | ss2 | 43 | flkL | -0.020150 | 0.294323 |
| L28 | H4 | 92 | ss1 | 95 | ss1 | -0.020347 | 0.174342 |
| L19 | H13 | 208 | flkR | 173 | other | -0.020814 | 0.232818 |
| L14 | H10 | 204 | ss2 | 235 | flkR | -0.020902 | 0.159266 |
| L16 | H7 | 197 | ss2 | 43 | flkL | -0.021020 | 0.223596 |
| L13 | H13 | 169 | other | 39 | flkL | -0.023227 | 0.087388 |
| L21 | H6 | 204 | ss2 | 204 | ss2 | -0.023616 | 0.196749 |
| L22 | H8 | 200 | ss2 | 204 | ss2 | -0.024206 | 0.614276 |
| L7 | H10 | 47 | flkL | 37 | flkL | -0.026536 | 0.170456 |
| L21 | H8 | 204 | ss2 | 173 | other | -0.027556 | 0.422215 |
| L0 | H14 | 49 | flkL | 28 | flkL | -0.028301 | 0.091328 |
| L31 | H17 | 92 | ss1 | 235 | flkR | -0.028650 | 0.408437 |
| L16 | H11 | 169 | other | 43 | flkL | -0.031118 | 0.719580 |
| L23 | H3 | 197 | ss2 | 200 | ss2 | -0.033296 | 0.669800 |
| L29 | H18 | 197 | ss2 | 92 | ss1 | -0.053313 | 0.358996 |
| L16 | H7 | 200 | ss2 | 43 | flkL | -0.064192 | 0.551783 |
| L17 | H4 | 204 | ss2 | 43 | flkL | -0.090505 | 0.474773 |
| L18 | H16 | 204 | ss2 | 43 | flkL | -0.238264 | 0.497718 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0130 | 0.00% |
| 10 | 10 | 7 | 0.0130 | 0.00% |
| 20 | 20 | 10 | 0.0130 | 0.00% |
| 50 | 50 | 24 | 0.0130 | 0.00% |
| 100 | 100 | 39 | 0.0130 | -0.00% |
| 200 | 200 | 63 | 0.0130 | -0.00% |
| 500 | 500 | 98 | 0.0130 | 0.00% |
| 1000 | 1,000 | 113 | 0.0135 | 0.06% |
| 2000 | 2,000 | 133 | 0.0166 | 0.45% |
| 5000 | 5,000 | 139 | 0.0445 | 3.91% |
| 10000 | 10,000 | 140 | 0.3248 | 38.70% |
| 20000 | 20,000 | 140 | 0.5920 | 71.88% |
| 50000 | 50,000 | 140 | 0.6516 | 79.28% |

## Motif Analysis

### L0 H14 — Rank #1

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 15  |  total attr: +0.1903

**Key mass** (top-1=33%, top-2=51%, top-3=64%)  [DISTR(S28/Y45/S34/S49)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 28 | flkL | +0.0627 | 32.9% |
| 45 | flkL | +0.0345 | 18.1% |
| 34 | flkL | +0.0245 | 12.9% |
| 49 | flkL | +0.0234 | 12.3% |
| 59 | flkL | +0.0198 | 10.4% |

**Query mass** (top-1=79%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 28 | flkL | +0.1512 | 79.5% |
| 49 | flkL | +0.0244 | 12.8% |
| 96 | ss1 | +0.0095 | 5.0% |
| 37 | flkL | +0.0051 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 13.3% |
| -17 | 1 | 6.7% |
| -6 | 1 | 6.7% |
| -31 | 1 | 6.7% |
| -21 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 12 | 80.0% |
| flkL | ss1 | 1 | 6.7% |
| ss1 | flkL | 1 | 6.7% |
| flkL | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 28 | flkL | 28 | flkL | +0.0480 | 0.3081 |
| 28 | flkL | 45 | flkL | +0.0305 | 0.1397 |
| 28 | flkL | 34 | flkL | +0.0210 | 0.1345 |
| 28 | flkL | 59 | flkL | +0.0156 | 0.1001 |
| 28 | flkL | 49 | flkL | +0.0145 | 0.0927 |

### L6 H4 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 5  |  total attr: +0.2483

**Key mass** (top-1=66%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.1647 | 66.3% |
| 39 | flkL | +0.0735 | 29.6% |
| 44 | flkL | +0.0048 | 1.9% |
| 50 | flkL | +0.0028 | 1.1% |
| 46 | flkL | +0.0025 | 1.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 37 | flkL | +0.2483 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 1 | 20.0% |
| -2 | 1 | 20.0% |
| -7 | 1 | 20.0% |
| -13 | 1 | 20.0% |
| -9 | 1 | 20.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 37 | flkL | 32 | flkL | +0.1647 | 0.2294 |
| 37 | flkL | 39 | flkL | +0.0735 | 0.0685 |
| 37 | flkL | 44 | flkL | +0.0048 | 0.0052 |
| 37 | flkL | 50 | flkL | +0.0028 | 0.0040 |
| 37 | flkL | 46 | flkL | +0.0025 | 0.0030 |

### L6 H19 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 45  |  total attr: +0.3217

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 37 | flkL | +0.3217 | 100.0% |

**Query mass** (top-1=14%, top-2=21%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0465 | 14.5% |
| 170 | other | +0.0224 | 7.0% |
| 172 | other | +0.0182 | 5.7% |
| 168 | other | +0.0158 | 4.9% |
| 171 | other | +0.0149 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 4%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +132 | 1 | 2.2% |
| +133 | 1 | 2.2% |
| +135 | 1 | 2.2% |
| +131 | 1 | 2.2% |
| +134 | 1 | 2.2% |

**Region-pair profile** (q→k)  (top=98%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 44 | 97.8% |
| flkL | flkL | 1 | 2.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | other | 37 | flkL | +0.0465 | 0.1538 |
| 170 | other | 37 | flkL | +0.0224 | 0.1558 |
| 172 | other | 37 | flkL | +0.0182 | 0.1596 |
| 168 | other | 37 | flkL | +0.0158 | 0.1520 |
| 171 | other | 37 | flkL | +0.0149 | 0.1573 |

### L7 H10 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 68  |  total attr: +0.9417

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 37 | flkL | +0.9417 | 100.0% |

**Query mass** (top-1=14%, top-2=21%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.1311 | 13.9% |
| 170 | other | +0.0699 | 7.4% |
| 172 | other | +0.0537 | 5.7% |
| 168 | other | +0.0503 | 5.3% |
| 171 | other | +0.0479 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 3%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +132 | 1 | 1.5% |
| +133 | 1 | 1.5% |
| +135 | 1 | 1.5% |
| +131 | 1 | 1.5% |
| +134 | 1 | 1.5% |

**Region-pair profile** (q→k)  (top=91%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 62 | 91.2% |
| ss2 | flkL | 2 | 2.9% |
| flkR | flkL | 2 | 2.9% |
| ss1 | flkL | 2 | 2.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | other | 37 | flkL | +0.1311 | 0.3078 |
| 170 | other | 37 | flkL | +0.0699 | 0.3101 |
| 172 | other | 37 | flkL | +0.0537 | 0.3038 |
| 168 | other | 37 | flkL | +0.0503 | 0.3209 |
| 171 | other | 37 | flkL | +0.0479 | 0.3202 |

### L8 H13 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 6  |  total attr: +0.0502

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +0.0502 | 100.0% |

**Query mass** (top-1=46%, top-2=61%, top-3=75%)  [DISTR(A169/G37/A170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0231 | 46.0% |
| 37 | flkL | +0.0078 | 15.5% |
| 170 | other | +0.0068 | 13.6% |
| 172 | other | +0.0049 | 9.8% |
| 168 | other | +0.0049 | 9.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +122 | 1 | 16.7% |
| -10 | 1 | 16.7% |
| +123 | 1 | 16.7% |
| +125 | 1 | 16.7% |
| +121 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 4 | 66.7% |
| flkL | flkL | 2 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | other | 47 | flkL | +0.0231 | 0.0664 |
| 37 | flkL | 47 | flkL | +0.0078 | 0.1113 |
| 170 | other | 47 | flkL | +0.0068 | 0.0655 |
| 172 | other | 47 | flkL | +0.0049 | 0.0472 |
| 168 | other | 47 | flkL | +0.0049 | 0.0456 |

### L9 H8 — Rank #16

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L9 H13 — Rank #10

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L10 H14 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.1741

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +0.1741 | 100.0% |

**Query mass** (top-1=39%, top-2=60%, top-3=69%)  [DISTR(A169/A168/A170/M165)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0681 | 39.1% |
| 168 | other | +0.0363 | 20.9% |
| 170 | other | +0.0149 | 8.5% |
| 165 | other | +0.0148 | 8.5% |
| 172 | other | +0.0119 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +122 | 1 | 9.1% |
| +121 | 1 | 9.1% |
| +123 | 1 | 9.1% |
| +118 | 1 | 9.1% |
| +125 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 11 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | other | 47 | flkL | +0.0681 | 0.1792 |
| 168 | other | 47 | flkL | +0.0363 | 0.2043 |
| 170 | other | 47 | flkL | +0.0149 | 0.1650 |
| 165 | other | 47 | flkL | +0.0148 | 0.2337 |
| 172 | other | 47 | flkL | +0.0119 | 0.1160 |

### L11 H16 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 30  |  total attr: +0.3464

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +0.3464 | 100.0% |

**Query mass** (top-1=22%, top-2=39%, top-3=55%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0779 | 22.5% |
| 168 | other | +0.0574 | 16.6% |
| 165 | other | +0.0535 | 15.4% |
| 172 | other | +0.0268 | 7.7% |
| 173 | other | +0.0154 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +122 | 1 | 3.3% |
| +121 | 1 | 3.3% |
| +118 | 1 | 3.3% |
| +125 | 1 | 3.3% |
| +126 | 1 | 3.3% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 30 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | other | 47 | flkL | +0.0779 | 0.3095 |
| 168 | other | 47 | flkL | +0.0574 | 0.3924 |
| 165 | other | 47 | flkL | +0.0535 | 0.5102 |
| 172 | other | 47 | flkL | +0.0268 | 0.3587 |
| 173 | other | 47 | flkL | +0.0154 | 0.3335 |

### L13 H13 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.0901

**Key mass** (top-1=35%, top-2=56%, top-3=67%)  [DISTR(V43/N39/L94/G37)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 43 | flkL | +0.0319 | 35.4% |
| 39 | flkL | +0.0183 | 20.4% |
| 94 | ss1 | +0.0103 | 11.4% |
| 37 | flkL | +0.0095 | 10.5% |
| 47 | flkL | +0.0057 | 6.4% |

**Query mass** (top-1=45%, top-2=65%, top-3=78%)  [DISTR(A169/M173/A168)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0406 | 45.1% |
| 173 | other | +0.0179 | 19.9% |
| 168 | other | +0.0118 | 13.1% |
| 174 | other | +0.0099 | 11.0% |
| 170 | other | +0.0041 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +137 | 2 | 13.3% |
| +126 | 1 | 6.7% |
| +134 | 1 | 6.7% |
| +125 | 1 | 6.7% |
| +75 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 53.3% |
| other | ss1 | 3 | 20.0% |
| other | other | 2 | 13.3% |
| flkL | flkL | 1 | 6.7% |
| ss2 | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | other | 43 | flkL | +0.0192 | 0.1182 |
| 173 | other | 39 | flkL | +0.0126 | 0.0877 |
| 168 | other | 43 | flkL | +0.0086 | 0.1360 |
| 169 | other | 94 | ss1 | +0.0071 | 0.0256 |
| 174 | other | 39 | flkL | +0.0058 | 0.0601 |

### L15 H12 — Rank #8

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 19  |  total attr: +0.1090

**Key mass** (top-1=41%, top-2=56%, top-3=71%)  [DISTR(A169/A168/A170)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0444 | 40.7% |
| 168 | other | +0.0167 | 15.4% |
| 170 | other | +0.0162 | 14.8% |
| 173 | other | +0.0155 | 14.2% |
| 172 | other | +0.0105 | 9.6% |

**Query mass** (top-1=51%, top-2=74%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | other | +0.0557 | 51.1% |
| 174 | other | +0.0245 | 22.5% |
| 200 | ss2 | +0.0164 | 15.1% |
| 172 | other | +0.0065 | 6.0% |
| 204 | ss2 | +0.0032 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 32%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 3 | 15.8% |
| +2 | 3 | 15.8% |
| +5 | 2 | 10.5% |
| +3 | 2 | 10.5% |
| +0 | 2 | 10.5% |

**Region-pair profile** (q→k)  (top=74%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 14 | 73.7% |
| ss2 | other | 4 | 21.1% |
| ss2 | ss2 | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | other | 169 | other | +0.0240 | 0.2408 |
| 173 | other | 168 | other | +0.0103 | 0.1261 |
| 174 | other | 169 | other | +0.0094 | 0.1783 |
| 173 | other | 170 | other | +0.0086 | 0.1006 |
| 173 | other | 173 | other | +0.0064 | 0.0567 |

### L16 H10 — Rank #15

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 24  |  total attr: +0.2636

**Key mass** (top-1=28%, top-2=56%, top-3=67%)  [DISTR(A169/M173/A170/S172)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0741 | 28.1% |
| 173 | other | +0.0738 | 28.0% |
| 170 | other | +0.0296 | 11.2% |
| 172 | other | +0.0295 | 11.2% |
| 168 | other | +0.0257 | 9.7% |

**Query mass** (top-1=57%, top-2=85%, top-3=95%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.1500 | 56.9% |
| 197 | ss2 | +0.0751 | 28.5% |
| 203 | ss2 | +0.0253 | 9.6% |
| 201 | ss2 | +0.0070 | 2.7% |
| 193 | other | +0.0032 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +31 | 2 | 8.3% |
| +35 | 2 | 8.3% |
| +28 | 2 | 8.3% |
| +32 | 2 | 8.3% |
| +34 | 2 | 8.3% |

**Region-pair profile** (q→k)  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 20 | 83.3% |
| ss2 | ss1 | 2 | 8.3% |
| other | other | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 204 | ss2 | 173 | other | +0.0456 | 0.2867 |
| 204 | ss2 | 169 | other | +0.0306 | 0.1902 |
| 197 | ss2 | 169 | other | +0.0279 | 0.3264 |
| 204 | ss2 | 172 | other | +0.0183 | 0.1139 |
| 204 | ss2 | 170 | other | +0.0157 | 0.1020 |

### L17 H1 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.1318

**Key mass** (top-1=33%, top-2=50%, top-3=64%)  [DISTR(M173/A169/S172/V43)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | other | +0.0439 | 33.3% |
| 169 | other | +0.0217 | 16.4% |
| 172 | other | +0.0187 | 14.2% |
| 43 | flkL | +0.0112 | 8.5% |
| 170 | other | +0.0104 | 7.9% |

**Query mass** (top-1=34%, top-2=65%, top-3=78%)  [DISTR(A98/K102/V101)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 98 | ss1 | +0.0451 | 34.2% |
| 102 | other | +0.0411 | 31.2% |
| 101 | other | +0.0165 | 12.5% |
| 94 | ss1 | +0.0085 | 6.5% |
| 200 | ss2 | +0.0066 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -71 | 3 | 12.5% |
| -75 | 2 | 8.3% |
| -72 | 2 | 8.3% |
| -68 | 2 | 8.3% |
| -69 | 2 | 8.3% |

**Region-pair profile** (q→k)  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 11 | 45.8% |
| ss1 | other | 7 | 29.2% |
| ss1 | ss2 | 2 | 8.3% |
| flkR | flkL | 2 | 8.3% |
| ss2 | flkR | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 98 | ss1 | 173 | other | +0.0162 | 0.2349 |
| 102 | other | 173 | other | +0.0142 | 0.1491 |
| 102 | other | 172 | other | +0.0084 | 0.0951 |
| 102 | other | 169 | other | +0.0074 | 0.1049 |
| 98 | ss1 | 172 | other | +0.0070 | 0.1150 |

### L17 H14 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0701

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 43 | flkL | +0.0701 | 100.0% |

**Query mass** (top-1=30%, top-2=48%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0208 | 29.7% |
| 95 | ss1 | +0.0131 | 18.7% |
| 102 | other | +0.0058 | 8.3% |
| 120 | other | +0.0045 | 6.4% |
| 98 | ss1 | +0.0045 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +161 | 1 | 9.1% |
| +52 | 1 | 9.1% |
| +59 | 1 | 9.1% |
| +77 | 1 | 9.1% |
| +55 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 45.5% |
| ss1 | flkL | 4 | 36.4% |
| ss2 | flkL | 1 | 9.1% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 204 | ss2 | 43 | flkL | +0.0208 | 0.0996 |
| 95 | ss1 | 43 | flkL | +0.0131 | 0.2034 |
| 102 | other | 43 | flkL | +0.0058 | 0.1425 |
| 120 | other | 43 | flkL | +0.0045 | 0.4955 |
| 98 | ss1 | 43 | flkL | +0.0045 | 0.1561 |

### L18 H7 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0542

**Key mass** (top-1=64%, top-2=79%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | other | +0.0344 | 63.5% |
| 172 | other | +0.0084 | 15.5% |
| 169 | other | +0.0062 | 11.4% |
| 43 | flkL | +0.0052 | 9.6% |

**Query mass** (top-1=35%, top-2=56%, top-3=66%)  [DISTR(V201/S192/F204/M200)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0188 | 34.7% |
| 192 | other | +0.0115 | 21.2% |
| 204 | ss2 | +0.0052 | 9.6% |
| 200 | ss2 | +0.0046 | 8.4% |
| 198 | ss2 | +0.0043 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +20 | 2 | 18.2% |
| +28 | 1 | 9.1% |
| +29 | 1 | 9.1% |
| +19 | 1 | 9.1% |
| +161 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 5 | 45.5% |
| other | other | 4 | 36.4% |
| ss2 | flkL | 1 | 9.1% |
| flkL | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 173 | other | +0.0130 | 0.1185 |
| 201 | ss2 | 172 | other | +0.0058 | 0.0645 |
| 192 | other | 173 | other | +0.0056 | 0.1163 |
| 204 | ss2 | 43 | flkL | +0.0052 | 0.0193 |
| 200 | ss2 | 173 | other | +0.0046 | 0.0849 |

### L18 H16 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.5180

**Key mass** (top-1=92%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 43 | flkL | +0.4771 | 92.1% |
| 173 | other | +0.0285 | 5.5% |
| 172 | other | +0.0062 | 1.2% |
| 169 | other | +0.0034 | 0.6% |
| 174 | other | +0.0028 | 0.5% |

**Query mass** (top-1=15%, top-2=27%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0757 | 14.6% |
| 201 | ss2 | +0.0645 | 12.4% |
| 197 | ss2 | +0.0581 | 11.2% |
| 173 | other | +0.0534 | 10.3% |
| 169 | other | +0.0512 | 9.9% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +155 | 1 | 4.8% |
| +158 | 1 | 4.8% |
| +154 | 1 | 4.8% |
| +130 | 1 | 4.8% |
| +126 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 38.1% |
| ss2 | flkL | 6 | 28.6% |
| ss2 | other | 4 | 19.0% |
| flkR | flkL | 2 | 9.5% |
| flkL | flkL | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 198 | ss2 | 43 | flkL | +0.0757 | 0.5543 |
| 201 | ss2 | 43 | flkL | +0.0645 | 0.5688 |
| 197 | ss2 | 43 | flkL | +0.0581 | 0.5295 |
| 173 | other | 43 | flkL | +0.0534 | 0.9983 |
| 169 | other | 43 | flkL | +0.0512 | 0.9773 |

### L19 H2 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 12  |  total attr: +0.0523

**Key mass** (top-1=63%, top-2=72%, top-3=79%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | other | +0.0331 | 63.2% |
| 172 | other | +0.0044 | 8.4% |
| 169 | other | +0.0041 | 7.9% |
| 43 | flkL | +0.0030 | 5.7% |
| 32 | flkL | +0.0027 | 5.1% |

**Query mass** (top-1=57%, top-2=69%, top-3=75%)  [DISTR(F204/V201/S96)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0300 | 57.3% |
| 201 | ss2 | +0.0060 | 11.6% |
| 96 | ss1 | +0.0030 | 5.7% |
| 199 | ss2 | +0.0028 | 5.4% |
| 95 | ss1 | +0.0027 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +31 | 1 | 8.3% |
| +28 | 1 | 8.3% |
| +32 | 1 | 8.3% |
| +35 | 1 | 8.3% |
| +53 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 7 | 58.3% |
| ss1 | other | 3 | 25.0% |
| ss1 | flkL | 2 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 204 | ss2 | 173 | other | +0.0164 | 0.1329 |
| 201 | ss2 | 173 | other | +0.0060 | 0.1307 |
| 204 | ss2 | 172 | other | +0.0044 | 0.0402 |
| 204 | ss2 | 169 | other | +0.0041 | 0.0416 |
| 96 | ss1 | 43 | flkL | +0.0030 | 0.0490 |

### L19 H9 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.1231

**Key mass** (top-1=48%, top-2=83%, top-3=89%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | other | +0.0592 | 48.1% |
| 43 | flkL | +0.0430 | 34.9% |
| 169 | other | +0.0071 | 5.8% |
| 174 | other | +0.0057 | 4.6% |
| 199 | ss2 | +0.0028 | 2.3% |

**Query mass** (top-1=17%, top-2=30%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0211 | 17.1% |
| 204 | ss2 | +0.0163 | 13.2% |
| 120 | other | +0.0090 | 7.3% |
| 201 | ss2 | +0.0080 | 6.5% |
| 208 | flkR | +0.0076 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +30 | 3 | 11.5% |
| +28 | 2 | 7.7% |
| +35 | 2 | 7.7% |
| +31 | 1 | 3.8% |
| +77 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 12 | 46.2% |
| other | flkL | 6 | 23.1% |
| flkR | flkL | 3 | 11.5% |
| flkR | other | 2 | 7.7% |
| flkL | other | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 204 | ss2 | 173 | other | +0.0108 | 0.3702 |
| 120 | other | 43 | flkL | +0.0090 | 0.6729 |
| 198 | ss2 | 173 | other | +0.0085 | 0.1769 |
| 201 | ss2 | 173 | other | +0.0080 | 0.2485 |
| 208 | flkR | 173 | other | +0.0076 | 0.4108 |

### L21 H7 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:MULTI-ANCHOR  |  cells: 12  |  total attr: +0.0414

**Key mass** (top-1=45%, top-2=71%, top-3=81%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | other | +0.0185 | 44.6% |
| 168 | other | +0.0109 | 26.3% |
| 195 | other | +0.0040 | 9.5% |
| 173 | other | +0.0028 | 6.8% |
| 39 | flkL | +0.0026 | 6.3% |

**Query mass** (top-1=38%, top-2=65%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | flkR | +0.0158 | 38.2% |
| 208 | flkR | +0.0112 | 27.1% |
| 197 | ss2 | +0.0064 | 15.5% |
| 205 | ss2 | +0.0027 | 6.5% |
| 192 | other | +0.0026 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +39 | 2 | 16.7% |
| +38 | 1 | 8.3% |
| +13 | 1 | 8.3% |
| +28 | 1 | 8.3% |
| +40 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 7 | 58.3% |
| ss2 | other | 3 | 25.0% |
| other | other | 1 | 8.3% |
| ss1 | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 207 | flkR | 169 | other | +0.0056 | 0.1589 |
| 207 | flkR | 168 | other | +0.0048 | 0.1513 |
| 208 | flkR | 195 | other | +0.0040 | 0.3562 |
| 208 | flkR | 169 | other | +0.0038 | 0.1579 |
| 197 | ss2 | 169 | other | +0.0037 | 0.1852 |

### L22 H10 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 2  |  total attr: +0.0081

**Key mass** (top-1=63%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 111 | other | +0.0051 | 63.0% |
| 204 | ss2 | +0.0030 | 37.0% |

**Query mass** (top-1=63%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | ss1 | +0.0051 | 63.0% |
| 219 | flkR | +0.0030 | 37.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -17 | 1 | 50.0% |
| +15 | 1 | 50.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 1 | 50.0% |
| flkR | ss2 | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | ss1 | 111 | other | +0.0051 | 0.1278 |
| 219 | flkR | 204 | ss2 | +0.0030 | 0.2303 |

### L24 H0 — Rank #20

**Tags:** k:MULTI-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0136

**Key mass** (top-1=35%, top-2=59%, top-3=82%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | other | +0.0048 | 35.1% |
| 192 | other | +0.0033 | 24.1% |
| 193 | other | +0.0031 | 22.6% |
| 173 | other | +0.0025 | 18.2% |

**Query mass** (top-1=82%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0111 | 81.8% |
| 197 | ss2 | +0.0025 | 18.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 1 | 25.0% |
| +6 | 1 | 25.0% |
| +5 | 1 | 25.0% |
| +24 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 198 | ss2 | 194 | other | +0.0048 | 0.0779 |
| 198 | ss2 | 192 | other | +0.0033 | 0.0600 |
| 198 | ss2 | 193 | other | +0.0031 | 0.0732 |
| 197 | ss2 | 173 | other | +0.0025 | 0.0518 |

### L24 H1 — Rank #22

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 10  |  total attr: +0.0527

**Key mass** (top-1=43%, top-2=60%, top-3=72%)  [DISTR(F204/I111/F112)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0225 | 42.8% |
| 111 | other | +0.0091 | 17.3% |
| 112 | other | +0.0064 | 12.1% |
| 108 | other | +0.0045 | 8.5% |
| 208 | flkR | +0.0039 | 7.5% |

**Query mass** (top-1=26%, top-2=51%, top-3=60%)  [DISTR(M197/S105/H198/A100/P202)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss2 | +0.0136 | 25.9% |
| 105 | other | +0.0130 | 24.8% |
| 198 | ss2 | +0.0052 | 9.8% |
| 100 | other | +0.0045 | 8.5% |
| 202 | ss2 | +0.0039 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 4 | 40.0% |
| -7 | 2 | 20.0% |
| -8 | 2 | 20.0% |
| -5 | 1 | 10.0% |
| -10 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 5 | 50.0% |
| ss2 | ss2 | 3 | 30.0% |
| ss2 | flkR | 1 | 10.0% |
| flkR | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 197 | ss2 | 204 | ss2 | +0.0136 | 0.2940 |
| 105 | other | 111 | other | +0.0091 | 0.2049 |
| 198 | ss2 | 204 | ss2 | +0.0052 | 0.3352 |
| 100 | other | 108 | other | +0.0045 | 0.1796 |
| 105 | other | 112 | other | +0.0040 | 0.1087 |

### L24 H14 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 1  |  total attr: +0.0027

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | other | +0.0027 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0027 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +16 | 1 | 100.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 185 | other | +0.0027 | 0.0859 |

### L27 H15 — Rank #21

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 6  |  total attr: +0.0311

**Key mass** (top-1=31%, top-2=54%, top-3=70%)  [DISTR(V201/F204/A205)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0098 | 31.4% |
| 204 | ss2 | +0.0070 | 22.4% |
| 205 | ss2 | +0.0051 | 16.2% |
| 95 | ss1 | +0.0036 | 11.7% |
| 91 | ss1 | +0.0032 | 10.2% |

**Query mass** (top-1=34%, top-2=66%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0106 | 34.1% |
| 95 | ss1 | +0.0098 | 31.4% |
| 91 | ss1 | +0.0051 | 16.2% |
| 205 | ss2 | +0.0032 | 10.2% |
| 198 | ss2 | +0.0025 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 2 | 33.3% |
| -106 | 1 | 16.7% |
| -3 | 1 | 16.7% |
| -114 | 1 | 16.7% |
| +114 | 1 | 16.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 50.0% |
| ss1 | ss2 | 2 | 33.3% |
| ss2 | ss2 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 95 | ss1 | 201 | ss2 | +0.0098 | 0.0943 |
| 201 | ss2 | 204 | ss2 | +0.0070 | 0.1645 |
| 91 | ss1 | 205 | ss2 | +0.0051 | 0.0896 |
| 201 | ss2 | 95 | ss1 | +0.0036 | 0.0364 |
| 205 | ss2 | 91 | ss1 | +0.0032 | 0.0705 |

### L28 H4 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 15  |  total attr: +0.1746

**Key mass** (top-1=62%, top-2=69%, top-3=74%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.1089 | 62.4% |
| 208 | flkR | +0.0118 | 6.7% |
| 205 | ss2 | +0.0077 | 4.4% |
| 91 | ss1 | +0.0069 | 4.0% |
| 202 | ss2 | +0.0068 | 3.9% |

**Query mass** (top-1=62%, top-2=69%, top-3=75%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.1087 | 62.2% |
| 205 | ss2 | +0.0118 | 6.7% |
| 197 | ss2 | +0.0108 | 6.2% |
| 95 | ss1 | +0.0100 | 5.7% |
| 201 | ss2 | +0.0093 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 6 | 40.0% |
| +3 | 3 | 20.0% |
| +4 | 2 | 13.3% |
| -4 | 2 | 13.3% |
| -5 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 40.0% |
| ss1 | ss1 | 4 | 26.7% |
| flkR | flkR | 2 | 13.3% |
| ss2 | flkR | 1 | 6.7% |
| ss2 | other | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 198 | ss2 | 201 | ss2 | +0.1049 | 0.7302 |
| 205 | ss2 | 208 | flkR | +0.0118 | 0.2870 |
| 95 | ss1 | 91 | ss1 | +0.0069 | 0.1197 |
| 197 | ss2 | 202 | ss2 | +0.0068 | 0.0771 |
| 99 | ss1 | 96 | ss1 | +0.0064 | 0.0582 |

### L29 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 40  |  total attr: +0.4300

**Key mass** (top-1=24%, top-2=42%, top-3=59%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | ss1 | +0.1012 | 23.5% |
| 88 | flkL | +0.0805 | 18.7% |
| 197 | ss2 | +0.0736 | 17.1% |
| 201 | ss2 | +0.0241 | 5.6% |
| 205 | ss2 | +0.0195 | 4.5% |

**Query mass** (top-1=20%, top-2=33%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0843 | 19.6% |
| 96 | ss1 | +0.0570 | 13.2% |
| 201 | ss2 | +0.0486 | 11.3% |
| 205 | ss2 | +0.0439 | 10.2% |
| 197 | ss2 | +0.0383 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 2 | 5.0% |
| -106 | 2 | 5.0% |
| -109 | 2 | 5.0% |
| -8 | 2 | 5.0% |
| -101 | 1 | 2.5% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 22.5% |
| ss2 | ss1 | 4 | 10.0% |
| ss2 | flkL | 4 | 10.0% |
| ss2 | ss2 | 4 | 10.0% |
| ss2 | flkR | 3 | 7.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 198 | ss2 | 92 | ss1 | +0.0641 | 0.3187 |
| 96 | ss1 | 197 | ss2 | +0.0488 | 0.4212 |
| 205 | ss2 | 88 | flkL | +0.0439 | 0.8335 |
| 201 | ss2 | 92 | ss1 | +0.0250 | 0.3405 |
| 201 | ss2 | 88 | flkL | +0.0209 | 0.4868 |

### L30 H0 — Rank #18

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 5  |  total attr: +0.0295

**Key mass** (top-1=29%, top-2=56%, top-3=80%)  [DISTR(H92/V95/V201)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | ss1 | +0.0086 | 28.9% |
| 95 | ss1 | +0.0081 | 27.5% |
| 201 | ss2 | +0.0069 | 23.4% |
| 197 | ss2 | +0.0060 | 20.2% |

**Query mass** (top-1=39%, top-2=66%, top-3=86%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0114 | 38.7% |
| 201 | ss2 | +0.0081 | 27.5% |
| 96 | ss1 | +0.0060 | 20.2% |
| 95 | ss1 | +0.0040 | 13.7% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 2 | 40.0% |
| -101 | 1 | 20.0% |
| -106 | 1 | 20.0% |
| -3 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 40.0% |
| ss1 | ss2 | 2 | 40.0% |
| ss2 | ss2 | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 198 | ss2 | 92 | ss1 | +0.0086 | 0.1739 |
| 201 | ss2 | 95 | ss1 | +0.0081 | 0.3104 |
| 96 | ss1 | 197 | ss2 | +0.0060 | 0.1519 |
| 95 | ss1 | 201 | ss2 | +0.0040 | 0.1344 |
| 198 | ss2 | 201 | ss2 | +0.0029 | 0.0764 |

### L30 H13 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 6  |  total attr: +0.0270

**Key mass** (top-1=48%, top-2=78%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss2 | +0.0129 | 47.7% |
| 99 | ss1 | +0.0083 | 30.7% |
| 201 | ss2 | +0.0032 | 11.7% |
| 95 | ss1 | +0.0027 | 9.8% |

**Query mass** (top-1=31%, top-2=55%, top-3=79%)  [DISTR(M197/V201/M99)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss2 | +0.0083 | 30.7% |
| 201 | ss2 | +0.0067 | 24.7% |
| 99 | ss1 | +0.0063 | 23.4% |
| 95 | ss1 | +0.0032 | 11.7% |
| 198 | ss2 | +0.0026 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +98 | 1 | 16.7% |
| -98 | 1 | 16.7% |
| +4 | 1 | 16.7% |
| -106 | 1 | 16.7% |
| +106 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 33.3% |
| ss1 | ss2 | 2 | 33.3% |
| ss2 | ss2 | 2 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 197 | ss2 | 99 | ss1 | +0.0083 | 0.1352 |
| 99 | ss1 | 197 | ss2 | +0.0063 | 0.1216 |
| 201 | ss2 | 197 | ss2 | +0.0040 | 0.0914 |
| 95 | ss1 | 201 | ss2 | +0.0032 | 0.0646 |
| 201 | ss2 | 95 | ss1 | +0.0027 | 0.0491 |

### L32 H13 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 12  |  total attr: +0.2113

**Key mass** (top-1=32%, top-2=48%, top-3=60%)  [DISTR(M197/S96/H92/M99)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss2 | +0.0685 | 32.4% |
| 96 | ss1 | +0.0323 | 15.3% |
| 92 | ss1 | +0.0262 | 12.4% |
| 99 | ss1 | +0.0215 | 10.2% |
| 198 | ss2 | +0.0211 | 10.0% |

**Query mass** (top-1=25%, top-2=48%, top-3=61%)  [DISTR(M197/S96/H198/H92)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss2 | +0.0539 | 25.5% |
| 96 | ss1 | +0.0482 | 22.8% |
| 198 | ss2 | +0.0262 | 12.4% |
| 92 | ss1 | +0.0211 | 10.0% |
| 99 | ss1 | +0.0203 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 2 | 16.7% |
| -106 | 2 | 16.7% |
| -101 | 1 | 8.3% |
| +101 | 1 | 8.3% |
| +98 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 50.0% |
| ss2 | ss1 | 6 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 96 | ss1 | 197 | ss2 | +0.0482 | 0.2924 |
| 197 | ss2 | 96 | ss1 | +0.0323 | 0.1963 |
| 198 | ss2 | 92 | ss1 | +0.0262 | 0.1471 |
| 197 | ss2 | 99 | ss1 | +0.0215 | 0.1184 |
| 92 | ss1 | 198 | ss2 | +0.0211 | 0.1184 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 12  |  total attr: +0.1661

**Key mass** (top-1=30%, top-2=52%, top-3=65%)  [DISTR(M197/V201/L91/H92)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss2 | +0.0503 | 30.3% |
| 201 | ss2 | +0.0367 | 22.1% |
| 91 | ss1 | +0.0218 | 13.1% |
| 92 | ss1 | +0.0198 | 11.9% |
| 99 | ss1 | +0.0171 | 10.3% |

**Query mass** (top-1=19%, top-2=35%, top-3=47%)  [DISTR(V95/M99/S96/H198/M197)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0317 | 19.1% |
| 99 | ss1 | +0.0263 | 15.8% |
| 96 | ss1 | +0.0202 | 12.2% |
| 198 | ss2 | +0.0198 | 11.9% |
| 197 | ss2 | +0.0197 | 11.9% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 2 | 16.7% |
| -106 | 1 | 8.3% |
| -98 | 1 | 8.3% |
| -101 | 1 | 8.3% |
| +98 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 50.0% |
| ss2 | ss1 | 6 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 95 | ss1 | 201 | ss2 | +0.0280 | 0.1210 |
| 99 | ss1 | 197 | ss2 | +0.0263 | 0.0879 |
| 96 | ss1 | 197 | ss2 | +0.0202 | 0.0745 |
| 198 | ss2 | 92 | ss1 | +0.0198 | 0.0674 |
| 197 | ss2 | 99 | ss1 | +0.0171 | 0.0572 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #1 | L0 | H14 | 15 | +0.1903 | DISTRIBUTED | S28/Y45/S34/S49 | SINGLE-ANCHOR | S28 |  | INTRA:flkL |
| #6 | L6 | H4 | 5 | +0.2483 | SINGLE-ANCHOR | I32 | SINGLE-ANCHOR | G37 |  | INTRA:flkL |
| #9 | L6 | H19 | 45 | +0.3217 | SINGLE-ANCHOR | G37 | DISTRIBUTED |  |  |  |
| #2 | L7 | H10 | 68 | +0.9417 | SINGLE-ANCHOR | G37 | DISTRIBUTED |  |  |  |
| #29 | L8 | H13 | 6 | +0.0502 | SINGLE-ANCHOR | F47 | DISTRIBUTED | A169/G37/A170 |  |  |
| #16 | L9 | H8 | 0 | +0.0000 | — |  | — |  |  |  |
| #10 | L9 | H13 | 0 | +0.0000 | — |  | — |  |  |  |
| #12 | L10 | H14 | 11 | +0.1741 | SINGLE-ANCHOR | F47 | DISTRIBUTED | A169/A168/A170/M165 |  |  |
| #7 | L11 | H16 | 30 | +0.3464 | SINGLE-ANCHOR | F47 | DISTRIBUTED |  |  |  |
| #13 | L13 | H13 | 15 | +0.0901 | DISTRIBUTED | V43/N39/L94/G37 | DISTRIBUTED | A169/M173/A168 |  |  |
| #8 | L15 | H12 | 19 | +0.1090 | DISTRIBUTED | A169/A168/A170 | DUAL-ANCHOR | M173/S174 |  |  |
| #15 | L16 | H10 | 24 | +0.2636 | DISTRIBUTED | A169/M173/A170/S172 | DUAL-ANCHOR | F204/M197 |  |  |
| #14 | L17 | H1 | 24 | +0.1318 | DISTRIBUTED | M173/A169/S172/V43 | DISTRIBUTED | A98/K102/V101 |  |  |
| #19 | L17 | H14 | 11 | +0.0701 | SINGLE-ANCHOR | V43 | DISTRIBUTED |  |  |  |
| #27 | L18 | H7 | 11 | +0.0542 | SINGLE-ANCHOR | M173 | DISTRIBUTED | V201/S192/F204/M200 |  |  |
| #11 | L18 | H16 | 21 | +0.5180 | SINGLE-ANCHOR | V43 | DISTRIBUTED |  |  |  |
| #30 | L19 | H2 | 12 | +0.0523 | SINGLE-ANCHOR | M173 | DISTRIBUTED | F204/V201/S96 |  |  |
| #26 | L19 | H9 | 26 | +0.1231 | DUAL-ANCHOR | M173/V43 | DISTRIBUTED |  |  |  |
| #17 | L21 | H7 | 12 | +0.0414 | DUAL-ANCHOR | A169/A168 | MULTI-ANCHOR |  |  |  |
| #28 | L22 | H10 | 2 | +0.0081 | SINGLE-ANCHOR | I111 | SINGLE-ANCHOR | L94 |  |  |
| #20 | L24 | H0 | 4 | +0.0136 | MULTI-ANCHOR |  | SINGLE-ANCHOR | H198 |  |  |
| #22 | L24 | H1 | 10 | +0.0527 | DISTRIBUTED | F204/I111/F112 | DISTRIBUTED | M197/S105/H198/A100/P202 | POSITIONAL |  |
| #25 | L24 | H14 | 1 | +0.0027 | SINGLE-ANCHOR | T185 | SINGLE-ANCHOR | V201 |  |  |
| #21 | L27 | H15 | 6 | +0.0311 | DISTRIBUTED | V201/F204/A205 | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss2→ss1 |
| #24 | L28 | H4 | 15 | +0.1746 | SINGLE-ANCHOR | V201 | SINGLE-ANCHOR | H198 |  | INTRA:ss2 |
| #3 | L29 | H18 | 40 | +0.4300 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #18 | L30 | H0 | 5 | +0.0295 | DISTRIBUTED | H92/V95/V201 | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss2→ss1 |
| #23 | L30 | H13 | 6 | +0.0270 | DUAL-ANCHOR | M197/M99 | DISTRIBUTED | M197/V201/M99 |  |  |
| #5 | L32 | H13 | 12 | +0.2113 | DISTRIBUTED | M197/S96/H92/M99 | DISTRIBUTED | M197/S96/H198/H92 |  | CROSS:ss1→ss2 |
| #4 | L32 | H18 | 12 | +0.1661 | DISTRIBUTED | M197/V201/L91/H92 | DISTRIBUTED | V95/M99/S96/H198/M197 |  | CROSS:ss1→ss2 |
