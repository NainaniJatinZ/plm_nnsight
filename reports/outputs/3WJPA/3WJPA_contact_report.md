# Contact Pattern Analysis: 3WJPA

Generated: 2026-03-22 21:50:47   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3WJPA |
| Contact pair | (167, 277) |
| ss1 | [162, 173) |
| ss2 | [272, 283) |
| Clean flank | 59 |
| Corrupt flank | 58 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 1.1112 |
| Corrupt metric | 0.0364 |
| Gap | 1.0749 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 250 | 77.92% |
| positive IE | 85 | 79.75% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L6 | H19 | +0.3035 |
| 2 | L32 | H18 | +0.2358 |
| 3 | L29 | H18 | +0.1928 |
| 4 | L6 | H13 | +0.1868 |
| 5 | L32 | H13 | +0.1613 |
| 6 | L10 | H9 | +0.1323 |
| 7 | L27 | H15 | +0.0866 |
| 8 | L12 | H19 | +0.0767 |
| 9 | L11 | H16 | +0.0718 |
| 10 | L12 | H10 | +0.0543 |
| 11 | L13 | H14 | +0.0514 |
| 12 | L26 | H16 | +0.0495 |
| 13 | L14 | H9 | +0.0433 |
| 14 | L12 | H16 | +0.0411 |
| 15 | L13 | H18 | +0.0358 |
| 16 | L17 | H10 | +0.0307 |
| 17 | L12 | H8 | +0.0286 |
| 18 | L20 | H13 | +0.0286 |
| 19 | L23 | H0 | +0.0266 |
| 20 | L10 | H6 | +0.0256 |
| 21 | L1 | H0 | +0.0242 |
| 22 | L21 | H13 | +0.0237 |
| 23 | L14 | H7 | +0.0237 |
| 24 | L23 | H15 | +0.0225 |
| 25 | L31 | H17 | +0.0223 |
| 26 | L20 | H5 | +0.0212 |
| 27 | L5 | H2 | +0.0187 |
| 28 | L25 | H10 | +0.0172 |
| 29 | L30 | H0 | +0.0167 |
| 30 | L0 | H8 | +0.0161 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.01% |
| 3 | 0.03% |
| 4 | 0.03% |
| 5 | 0.05% |
| 6 | 0.05% |
| 7 | 0.05% |
| 8 | 0.05% |
| 9 | 0.05% |
| 10 | 0.06% |
| 20 | 0.08% |
| 80 | 67.09% |
| 450 | 121.84% |

## Cell Attribution Analysis

Total cells: 8,953,947

- Positive: 4,451,285
- Negative: 4,499,958

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000017 | 895,396 |
| 95th | +0.00000058 | 447,698 |
| 99th | +0.00000520 | 89,540 |
| 99.5th | +0.00001171 | 44,771 |
| 99.9th | +0.00006900 | 8,955 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H19 | 94 | other | 127 | flkL | +0.178265 | 0.101169 |
| L6 | H13 | 94 | other | 166 | ss1 | +0.115600 | 0.064160 |
| L11 | H16 | 94 | other | 276 | ss2 | +0.071197 | 0.732058 |
| L20 | H13 | 168 | ss1 | 163 | ss1 | +0.040159 | 0.524326 |
| L12 | H10 | 116 | flkL | 94 | other | +0.037189 | 0.926866 |
| L12 | H8 | 166 | ss1 | 94 | other | +0.037006 | 0.779504 |
| L10 | H6 | 116 | flkL | 94 | other | +0.036034 | 0.839720 |
| L23 | H0 | 165 | ss1 | 166 | ss1 | +0.025296 | 0.587377 |
| L17 | H10 | 166 | ss1 | 166 | ss1 | +0.024045 | 0.594211 |
| L22 | H10 | 168 | ss1 | 163 | ss1 | +0.023296 | 0.405293 |
| L12 | H19 | 166 | ss1 | 94 | other | +0.023191 | 0.483740 |
| L19 | H0 | 168 | ss1 | 166 | ss1 | +0.022178 | 0.804433 |
| L27 | H15 | 165 | ss1 | 278 | ss2 | +0.021022 | 0.226977 |
| L32 | H18 | 278 | ss2 | 167 | ss1 | +0.020202 | 0.237089 |
| L4 | H18 | 94 | other | 103 | flkL | +0.019796 | 0.056882 |
| L12 | H16 | 94 | other | 276 | ss2 | +0.019014 | 0.328654 |
| L18 | H8 | 163 | ss1 | 166 | ss1 | +0.018220 | 0.447838 |
| L1 | H6 | 94 | other | 103 | flkL | +0.017826 | 0.041082 |
| L14 | H9 | 166 | ss1 | 94 | other | +0.017696 | 0.209238 |
| L5 | H2 | 94 | other | 102 | other | +0.017488 | 0.025799 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L31 | H17 | 169 | ss1 | 273 | ss2 | -0.006164 | 0.085263 |
| L12 | H8 | 145 | flkL | 94 | other | -0.006184 | 0.681609 |
| L10 | H9 | 168 | ss1 | 276 | ss2 | -0.006220 | 0.541304 |
| L14 | H9 | 164 | ss1 | 276 | ss2 | -0.006269 | 0.270190 |
| L14 | H7 | 278 | ss2 | 94 | other | -0.006656 | 0.315421 |
| L10 | H9 | 167 | ss1 | 276 | ss2 | -0.007106 | 0.449940 |
| L28 | H2 | 169 | ss1 | 171 | ss1 | -0.007798 | 0.523720 |
| L12 | H8 | 170 | ss1 | 94 | other | -0.008236 | 0.776086 |
| L13 | H18 | 168 | ss1 | 276 | ss2 | -0.011203 | 0.178103 |
| L29 | H18 | 165 | ss1 | 304 | flkR | -0.011986 | 0.704458 |
| L11 | H16 | 276 | ss2 | 276 | ss2 | -0.012115 | 0.158638 |
| L12 | H19 | 168 | ss1 | 94 | other | -0.012234 | 0.430178 |
| L29 | H18 | 167 | ss1 | 301 | flkR | -0.013550 | 0.566964 |
| L0 | H8 | 103 | flkL | 103 | flkL | -0.014469 | 0.155768 |
| L22 | H10 | 169 | ss1 | 163 | ss1 | -0.016558 | 0.372386 |
| L17 | H10 | 163 | ss1 | 166 | ss1 | -0.016895 | 0.648111 |
| L29 | H18 | 169 | ss1 | 273 | ss2 | -0.017418 | 0.152512 |
| L12 | H8 | 163 | ss1 | 94 | other | -0.019215 | 0.692484 |
| L25 | H10 | 168 | ss1 | 163 | ss1 | -0.023135 | 0.749513 |
| L23 | H15 | 169 | ss1 | 276 | ss2 | -0.027944 | 0.342963 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0364 | 0.00% |
| 10 | 10 | 10 | 0.0364 | -0.00% |
| 20 | 20 | 20 | 0.0364 | 0.00% |
| 50 | 50 | 32 | 0.0365 | 0.01% |
| 100 | 100 | 41 | 0.0367 | 0.03% |
| 200 | 200 | 63 | 0.0387 | 0.22% |
| 500 | 500 | 80 | 0.0612 | 2.31% |
| 1000 | 1,000 | 84 | 0.1848 | 13.81% |
| 2000 | 2,000 | 85 | 0.4501 | 38.49% |
| 5000 | 5,000 | 85 | 0.7926 | 70.36% |
| 10000 | 10,000 | 85 | 1.0077 | 90.37% |
| 20000 | 20,000 | 85 | 1.1486 | 103.48% |
| 50000 | 50,000 | 85 | 1.2180 | 109.93% |

## Motif Analysis

### L0 H8 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 4  |  total attr: +0.0062

**Key mass** (top-1=88%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | flkL | +0.0054 | 87.9% |
| 170 | ss1 | +0.0007 | 12.1% |

**Query mass** (top-1=55%, top-2=74%, top-3=88%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 142 | flkL | +0.0034 | 54.8% |
| 165 | ss1 | +0.0012 | 18.9% |
| 90 | other | +0.0009 | 14.1% |
| 170 | ss1 | +0.0007 | 12.1% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +39 | 1 | 25.0% |
| +62 | 1 | 25.0% |
| -13 | 1 | 25.0% |
| +0 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 1 | 25.0% |
| ss1 | flkL | 1 | 25.0% |
| other | flkL | 1 | 25.0% |
| ss1 | ss1 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 142 | flkL | 103 | flkL | +0.0034 | 0.0473 |
| 165 | ss1 | 103 | flkL | +0.0012 | 0.0025 |
| 90 | other | 103 | flkL | +0.0009 | 0.0031 |
| 170 | ss1 | 170 | ss1 | +0.0007 | 0.0060 |

### L1 H0 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 6  |  total attr: +0.0391

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | flkL | +0.0391 | 100.0% |

**Query mass** (top-1=35%, top-2=58%, top-3=78%)  [DISTR(S97/M98/A95)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | other | +0.0136 | 34.8% |
| 98 | other | +0.0091 | 23.2% |
| 95 | other | +0.0079 | 20.3% |
| 96 | other | +0.0041 | 10.6% |
| 99 | other | +0.0031 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 1 | 16.7% |
| -5 | 1 | 16.7% |
| -8 | 1 | 16.7% |
| -7 | 1 | 16.7% |
| -4 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 6 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | other | 103 | flkL | +0.0136 | 0.0416 |
| 98 | other | 103 | flkL | +0.0091 | 0.0559 |
| 95 | other | 103 | flkL | +0.0079 | 0.0211 |
| 96 | other | 103 | flkL | +0.0041 | 0.0293 |
| 99 | other | 103 | flkL | +0.0031 | 0.0586 |

### L5 H2 — Rank #27

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +0.0400

**Key mass** (top-1=44%, top-2=61%, top-3=77%)  [DISTR(E102/D105/G101)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | other | +0.0175 | 43.8% |
| 105 | flkL | +0.0070 | 17.5% |
| 101 | other | +0.0063 | 15.9% |
| 99 | other | +0.0046 | 11.4% |
| 100 | other | +0.0035 | 8.7% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0400 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 1 | 16.7% |
| -11 | 1 | 16.7% |
| -7 | 1 | 16.7% |
| -5 | 1 | 16.7% |
| -6 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 5 | 83.3% |
| other | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | other | 102 | other | +0.0175 | 0.0258 |
| 94 | other | 105 | flkL | +0.0070 | 0.0526 |
| 94 | other | 101 | other | +0.0063 | 0.0158 |
| 94 | other | 99 | other | +0.0046 | 0.0065 |
| 94 | other | 100 | other | +0.0035 | 0.0084 |

### L6 H13 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 7  |  total attr: +0.1257

**Key mass** (top-1=92%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.1156 | 92.0% |
| 104 | flkL | +0.0043 | 3.4% |
| 103 | flkL | +0.0016 | 1.3% |
| 168 | ss1 | +0.0012 | 1.0% |
| 142 | flkL | +0.0012 | 0.9% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.1257 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -72 | 1 | 14.3% |
| -10 | 1 | 14.3% |
| -9 | 1 | 14.3% |
| -74 | 1 | 14.3% |
| -48 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 71.4% |
| other | ss1 | 2 | 28.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | other | 166 | ss1 | +0.1156 | 0.0642 |
| 94 | other | 104 | flkL | +0.0043 | 0.0049 |
| 94 | other | 103 | flkL | +0.0016 | 0.0022 |
| 94 | other | 168 | ss1 | +0.0012 | 0.0012 |
| 94 | other | 142 | flkL | +0.0012 | 0.0038 |

### L6 H19 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 2  |  total attr: +0.1789

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | flkL | +0.1783 | 99.6% |
| 313 | flkR | +0.0007 | 0.4% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.1789 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -33 | 1 | 50.0% |
| -219 | 1 | 50.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 1 | 50.0% |
| other | flkR | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | other | 127 | flkL | +0.1783 | 0.1012 |
| 94 | other | 313 | flkR | +0.0007 | 0.0016 |

### L10 H6 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0421

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0414 | 98.3% |
| 122 | flkL | +0.0007 | 1.7% |

**Query mass** (top-1=86%, top-2=93%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 116 | flkL | +0.0360 | 85.5% |
| 120 | flkL | +0.0031 | 7.4% |
| 119 | flkL | +0.0023 | 5.4% |
| 94 | other | +0.0007 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +22 | 1 | 25.0% |
| +26 | 1 | 25.0% |
| +25 | 1 | 25.0% |
| -28 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 3 | 75.0% |
| other | flkL | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 116 | flkL | 94 | other | +0.0360 | 0.8397 |
| 120 | flkL | 94 | other | +0.0031 | 0.3752 |
| 119 | flkL | 94 | other | +0.0023 | 0.3517 |
| 94 | other | 122 | flkL | +0.0007 | 0.0325 |

### L10 H9 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 45  |  total attr: +0.1102

**Key mass** (top-1=66%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0731 | 66.3% |
| 276 | ss2 | +0.0371 | 33.7% |

**Query mass** (top-1=12%, top-2=23%, top-3=30%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0132 | 12.0% |
| 166 | ss1 | +0.0124 | 11.2% |
| 167 | ss1 | +0.0080 | 7.3% |
| 169 | ss1 | +0.0069 | 6.2% |
| 171 | ss1 | +0.0062 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 4%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -182 | 1 | 2.2% |
| +72 | 1 | 2.2% |
| +73 | 1 | 2.2% |
| +75 | 1 | 2.2% |
| +77 | 1 | 2.2% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 9 | 20.0% |
| ss1 | other | 8 | 17.8% |
| other | other | 8 | 17.8% |
| flkL | other | 7 | 15.6% |
| ss2 | ss2 | 4 | 8.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | other | 276 | ss2 | +0.0132 | 0.4261 |
| 166 | ss1 | 94 | other | +0.0124 | 0.5514 |
| 167 | ss1 | 94 | other | +0.0080 | 0.6045 |
| 169 | ss1 | 94 | other | +0.0069 | 0.5545 |
| 171 | ss1 | 94 | other | +0.0062 | 0.5986 |

### L11 H16 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 8  |  total attr: +0.0823

**Key mass** (top-1=91%, top-2=96%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0749 | 91.0% |
| 116 | flkL | +0.0044 | 5.3% |
| 94 | other | +0.0030 | 3.6% |

**Query mass** (top-1=87%, top-2=93%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0712 | 86.5% |
| 276 | ss2 | +0.0052 | 6.3% |
| 166 | ss1 | +0.0023 | 2.8% |
| 169 | ss1 | +0.0015 | 1.8% |
| 93 | other | +0.0013 | 1.5% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -182 | 1 | 12.5% |
| +160 | 1 | 12.5% |
| -110 | 1 | 12.5% |
| +75 | 1 | 12.5% |
| -183 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 3 | 37.5% |
| ss1 | other | 2 | 25.0% |
| ss2 | flkL | 1 | 12.5% |
| ss1 | ss2 | 1 | 12.5% |
| ss2 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | other | 276 | ss2 | +0.0712 | 0.7321 |
| 276 | ss2 | 116 | flkL | +0.0044 | 0.0799 |
| 166 | ss1 | 276 | ss2 | +0.0016 | 0.0851 |
| 169 | ss1 | 94 | other | +0.0015 | 0.0535 |
| 93 | other | 276 | ss2 | +0.0013 | 0.5111 |

### L12 H8 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.1030

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.1020 | 99.1% |
| 276 | ss2 | +0.0010 | 0.9% |

**Query mass** (top-1=36%, top-2=48%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0370 | 35.9% |
| 169 | ss1 | +0.0128 | 12.4% |
| 172 | ss1 | +0.0089 | 8.6% |
| 127 | flkL | +0.0071 | 6.9% |
| 161 | flkL | +0.0056 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +72 | 1 | 4.8% |
| +75 | 1 | 4.8% |
| +78 | 1 | 4.8% |
| +33 | 1 | 4.8% |
| +67 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 9 | 42.9% |
| ss1 | other | 5 | 23.8% |
| other | other | 3 | 14.3% |
| ss2 | other | 3 | 14.3% |
| ss1 | ss2 | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 166 | ss1 | 94 | other | +0.0370 | 0.7795 |
| 169 | ss1 | 94 | other | +0.0128 | 0.7236 |
| 172 | ss1 | 94 | other | +0.0089 | 0.7648 |
| 127 | flkL | 94 | other | +0.0071 | 0.5910 |
| 161 | flkL | 94 | other | +0.0056 | 0.6497 |

### L12 H10 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 10  |  total attr: +0.0551

**Key mass** (top-1=92%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0505 | 91.6% |
| 276 | ss2 | +0.0018 | 3.3% |
| -1 | other | +0.0013 | 2.3% |
| 82 | other | +0.0008 | 1.4% |
| 83 | other | +0.0008 | 1.4% |

**Query mass** (top-1=67%, top-2=80%, top-3=85%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 116 | flkL | +0.0372 | 67.5% |
| 120 | flkL | +0.0068 | 12.4% |
| 112 | flkL | +0.0030 | 5.4% |
| 94 | other | +0.0028 | 5.1% |
| 253 | other | +0.0018 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +22 | 1 | 10.0% |
| +26 | 1 | 10.0% |
| +18 | 1 | 10.0% |
| -23 | 1 | 10.0% |
| +19 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 6 | 60.0% |
| other | other | 3 | 30.0% |
| other | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 116 | flkL | 94 | other | +0.0372 | 0.9269 |
| 120 | flkL | 94 | other | +0.0068 | 0.4659 |
| 112 | flkL | 94 | other | +0.0030 | 0.8746 |
| 253 | other | 276 | ss2 | +0.0018 | 0.0589 |
| 113 | flkL | 94 | other | +0.0013 | 0.8267 |

### L12 H16 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 7  |  total attr: +0.0248

**Key mass** (top-1=87%, top-2=93%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0216 | 86.9% |
| -1 | other | +0.0016 | 6.4% |
| 94 | other | +0.0009 | 3.7% |
| 338 | flkR | +0.0007 | 3.0% |

**Query mass** (top-1=79%, top-2=86%, top-3=90%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0197 | 79.5% |
| 276 | ss2 | +0.0016 | 6.4% |
| 127 | flkL | +0.0010 | 3.9% |
| 273 | ss2 | +0.0009 | 3.7% |
| 97 | other | +0.0009 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -182 | 1 | 14.3% |
| +277 | 1 | 14.3% |
| -149 | 1 | 14.3% |
| +179 | 1 | 14.3% |
| -179 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 2 | 28.6% |
| ss2 | other | 2 | 28.6% |
| flkL | ss2 | 2 | 28.6% |
| other | flkR | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | other | 276 | ss2 | +0.0190 | 0.3287 |
| 276 | ss2 | -1 | other | +0.0016 | 0.0469 |
| 127 | flkL | 276 | ss2 | +0.0010 | 0.1562 |
| 273 | ss2 | 94 | other | +0.0009 | 0.0248 |
| 97 | other | 276 | ss2 | +0.0009 | 0.5221 |

### L12 H19 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.1235

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.1228 | 99.4% |
| -1 | other | +0.0007 | 0.6% |

**Query mass** (top-1=19%, top-2=31%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0232 | 18.8% |
| 276 | ss2 | +0.0156 | 12.6% |
| 127 | flkL | +0.0141 | 11.5% |
| 165 | ss1 | +0.0082 | 6.7% |
| 169 | ss1 | +0.0081 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +72 | 1 | 4.3% |
| +182 | 1 | 4.3% |
| +33 | 1 | 4.3% |
| +71 | 1 | 4.3% |
| +75 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=70%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 16 | 69.6% |
| ss1 | other | 4 | 17.4% |
| other | other | 2 | 8.7% |
| ss2 | other | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 166 | ss1 | 94 | other | +0.0232 | 0.4837 |
| 276 | ss2 | 94 | other | +0.0156 | 0.5667 |
| 127 | flkL | 94 | other | +0.0141 | 0.8097 |
| 165 | ss1 | 94 | other | +0.0082 | 0.4327 |
| 169 | ss1 | 94 | other | +0.0081 | 0.3742 |

### L13 H14 — Rank #11

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0501

**Key mass** (top-1=48%, top-2=72%, top-3=84%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 116 | flkL | +0.0242 | 48.2% |
| 94 | other | +0.0121 | 24.1% |
| -1 | other | +0.0060 | 11.9% |
| 253 | other | +0.0028 | 5.6% |
| 142 | flkL | +0.0016 | 3.1% |

**Query mass** (top-1=12%, top-2=23%, top-3=32%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | flkL | +0.0061 | 12.1% |
| 94 | other | +0.0053 | 10.5% |
| 147 | flkL | +0.0045 | 8.9% |
| 143 | flkL | +0.0043 | 8.5% |
| 145 | flkL | +0.0037 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +28 | 3 | 14.3% |
| +33 | 2 | 9.5% |
| +31 | 2 | 9.5% |
| +30 | 2 | 9.5% |
| +32 | 2 | 9.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 8 | 38.1% |
| flkL | other | 5 | 23.8% |
| ss1 | flkL | 5 | 23.8% |
| other | other | 2 | 9.5% |
| ss2 | other | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | flkL | 94 | other | +0.0061 | 0.8596 |
| 94 | other | -1 | other | +0.0053 | 0.8467 |
| 147 | flkL | 116 | flkL | +0.0045 | 0.3448 |
| 143 | flkL | 116 | flkL | +0.0043 | 0.4515 |
| 145 | flkL | 116 | flkL | +0.0037 | 0.3661 |

### L13 H18 — Rank #15

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 41  |  total attr: +0.0900

**Key mass** (top-1=51%, top-2=94%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0458 | 50.9% |
| 94 | other | +0.0391 | 43.5% |
| 87 | other | +0.0008 | 0.9% |
| 88 | other | +0.0008 | 0.9% |
| 86 | other | +0.0007 | 0.8% |

**Query mass** (top-1=18%, top-2=28%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0163 | 18.1% |
| 165 | ss1 | +0.0086 | 9.5% |
| 127 | flkL | +0.0060 | 6.6% |
| 162 | ss1 | +0.0055 | 6.1% |
| 94 | other | +0.0050 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +72 | 1 | 2.4% |
| -111 | 1 | 2.4% |
| -149 | 1 | 2.4% |
| -110 | 1 | 2.4% |
| +75 | 1 | 2.4% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 12 | 29.3% |
| ss1 | other | 8 | 19.5% |
| other | other | 8 | 19.5% |
| ss1 | ss2 | 5 | 12.2% |
| flkL | other | 5 | 12.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 166 | ss1 | 94 | other | +0.0113 | 0.2905 |
| 165 | ss1 | 276 | ss2 | +0.0086 | 0.2664 |
| 127 | flkL | 276 | ss2 | +0.0060 | 0.3812 |
| 166 | ss1 | 276 | ss2 | +0.0051 | 0.2641 |
| 169 | ss1 | 94 | other | +0.0046 | 0.1608 |

### L14 H7 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0804

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0795 | 98.9% |
| 276 | ss2 | +0.0009 | 1.1% |

**Query mass** (top-1=20%, top-2=36%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | ss1 | +0.0158 | 19.7% |
| 276 | ss2 | +0.0130 | 16.2% |
| 164 | ss1 | +0.0073 | 9.1% |
| 275 | ss2 | +0.0071 | 8.8% |
| 274 | ss2 | +0.0070 | 8.8% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +75 | 1 | 5.0% |
| +182 | 1 | 5.0% |
| +70 | 1 | 5.0% |
| +181 | 1 | 5.0% |
| +180 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 30.0% |
| flkR | other | 5 | 25.0% |
| ss2 | other | 4 | 20.0% |
| other | other | 3 | 15.0% |
| ss2 | ss2 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | ss1 | 94 | other | +0.0158 | 0.4291 |
| 276 | ss2 | 94 | other | +0.0121 | 0.5759 |
| 164 | ss1 | 94 | other | +0.0073 | 0.3950 |
| 275 | ss2 | 94 | other | +0.0071 | 0.3098 |
| 274 | ss2 | 94 | other | +0.0070 | 0.2559 |

### L14 H9 — Rank #13

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0893

**Key mass** (top-1=51%, top-2=99%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | other | +0.0452 | 50.7% |
| 276 | ss2 | +0.0430 | 48.2% |
| -1 | other | +0.0010 | 1.1% |

**Query mass** (top-1=37%, top-2=48%, top-3=57%)  [DISTR(V166/G163/V168/D164/A165)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0331 | 37.1% |
| 163 | ss1 | +0.0098 | 11.0% |
| 168 | ss1 | +0.0083 | 9.3% |
| 164 | ss1 | +0.0075 | 8.3% |
| 165 | ss1 | +0.0049 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +72 | 1 | 4.2% |
| -110 | 1 | 4.2% |
| -108 | 1 | 4.2% |
| +70 | 1 | 4.2% |
| +69 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 9 | 37.5% |
| ss1 | other | 7 | 29.2% |
| ss1 | ss2 | 3 | 12.5% |
| other | other | 2 | 8.3% |
| ss2 | ss2 | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 166 | ss1 | 94 | other | +0.0177 | 0.2092 |
| 166 | ss1 | 276 | ss2 | +0.0154 | 0.2378 |
| 168 | ss1 | 276 | ss2 | +0.0083 | 0.1766 |
| 164 | ss1 | 94 | other | +0.0075 | 0.1576 |
| 163 | ss1 | 94 | other | +0.0059 | 0.2068 |

### L17 H10 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0662

**Key mass** (top-1=94%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0620 | 93.8% |
| 94 | other | +0.0034 | 5.2% |
| 142 | flkL | +0.0007 | 1.1% |

**Query mass** (top-1=36%, top-2=59%, top-3=79%)  [DISTR(V166/A165/G170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0240 | 36.3% |
| 165 | ss1 | +0.0148 | 22.4% |
| 170 | ss1 | +0.0135 | 20.5% |
| 167 | ss1 | +0.0045 | 6.9% |
| 94 | other | +0.0024 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 18.2% |
| -1 | 1 | 9.1% |
| +4 | 1 | 9.1% |
| +1 | 1 | 9.1% |
| +9 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 4 | 36.4% |
| other | ss1 | 3 | 27.3% |
| other | other | 1 | 9.1% |
| flkL | ss1 | 1 | 9.1% |
| flkL | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 166 | ss1 | 166 | ss1 | +0.0240 | 0.5942 |
| 165 | ss1 | 166 | ss1 | +0.0148 | 0.7754 |
| 170 | ss1 | 166 | ss1 | +0.0135 | 0.7627 |
| 167 | ss1 | 166 | ss1 | +0.0045 | 0.7137 |
| 94 | other | 94 | other | +0.0024 | 0.6728 |

### L20 H5 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 11  |  total attr: +0.0468

**Key mass** (top-1=89%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0418 | 89.2% |
| 168 | ss1 | +0.0036 | 7.8% |
| 163 | ss1 | +0.0008 | 1.6% |
| 179 | other | +0.0006 | 1.4% |

**Query mass** (top-1=32%, top-2=54%, top-3=72%)  [DISTR(A165/D164/K161)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0148 | 31.5% |
| 164 | ss1 | +0.0104 | 22.3% |
| 161 | flkL | +0.0084 | 18.0% |
| 163 | ss1 | +0.0054 | 11.4% |
| 160 | flkL | +0.0026 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 2 | 18.2% |
| -3 | 2 | 18.2% |
| -7 | 2 | 18.2% |
| -2 | 1 | 9.1% |
| -5 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 54.5% |
| flkL | ss1 | 4 | 36.4% |
| ss1 | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 166 | ss1 | +0.0121 | 0.2708 |
| 164 | ss1 | 166 | ss1 | +0.0104 | 0.4453 |
| 161 | flkL | 166 | ss1 | +0.0084 | 0.5716 |
| 163 | ss1 | 166 | ss1 | +0.0054 | 0.3173 |
| 165 | ss1 | 168 | ss1 | +0.0027 | 0.1178 |

### L20 H13 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 10  |  total attr: +0.0662

**Key mass** (top-1=83%, top-2=91%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | ss1 | +0.0549 | 82.8% |
| 161 | flkL | +0.0056 | 8.4% |
| 162 | ss1 | +0.0027 | 4.1% |
| 160 | flkL | +0.0009 | 1.4% |
| 270 | other | +0.0008 | 1.2% |

**Query mass** (top-1=61%, top-2=84%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 168 | ss1 | +0.0402 | 60.6% |
| 165 | ss1 | +0.0156 | 23.5% |
| 166 | ss1 | +0.0074 | 11.2% |
| 164 | ss1 | +0.0009 | 1.4% |
| 273 | ss2 | +0.0008 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 70%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 4 | 40.0% |
| +3 | 3 | 30.0% |
| +5 | 1 | 10.0% |
| +2 | 1 | 10.0% |
| +17 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 60.0% |
| ss1 | flkL | 3 | 30.0% |
| ss2 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 168 | ss1 | 163 | ss1 | +0.0402 | 0.5243 |
| 165 | ss1 | 163 | ss1 | +0.0086 | 0.3007 |
| 166 | ss1 | 163 | ss1 | +0.0061 | 0.5969 |
| 165 | ss1 | 161 | flkL | +0.0056 | 0.3110 |
| 165 | ss1 | 162 | ss1 | +0.0014 | 0.1168 |

### L21 H13 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:ss1  |  cells: 7  |  total attr: +0.0451

**Key mass** (top-1=68%, top-2=86%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0306 | 67.8% |
| 168 | ss1 | +0.0080 | 17.8% |
| 165 | ss1 | +0.0039 | 8.5% |
| 164 | ss1 | +0.0019 | 4.2% |
| 163 | ss1 | +0.0008 | 1.7% |

**Query mass** (top-1=42%, top-2=79%, top-3=97%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0191 | 42.3% |
| 167 | ss1 | +0.0165 | 36.6% |
| 169 | ss1 | +0.0080 | 17.8% |
| 166 | ss1 | +0.0008 | 1.7% |
| 164 | ss1 | +0.0007 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 71%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 42.9% |
| -1 | 2 | 28.6% |
| +0 | 1 | 14.3% |
| +3 | 1 | 14.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 167 | ss1 | 166 | ss1 | +0.0165 | 0.5226 |
| 165 | ss1 | 166 | ss1 | +0.0141 | 0.5299 |
| 169 | ss1 | 168 | ss1 | +0.0080 | 0.3445 |
| 165 | ss1 | 165 | ss1 | +0.0031 | 0.3453 |
| 165 | ss1 | 164 | ss1 | +0.0019 | 0.0799 |

### L23 H0 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | POSITIONAL | INTRA:ss1  |  cells: 14  |  total attr: +0.0669

**Key mass** (top-1=81%, top-2=85%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | ss1 | +0.0544 | 81.3% |
| 168 | ss1 | +0.0028 | 4.2% |
| 171 | ss1 | +0.0023 | 3.5% |
| 164 | ss1 | +0.0018 | 2.6% |
| 159 | flkL | +0.0017 | 2.6% |

**Query mass** (top-1=39%, top-2=65%, top-3=84%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0261 | 39.1% |
| 163 | ss1 | +0.0174 | 26.1% |
| 164 | ss1 | +0.0125 | 18.6% |
| 167 | ss1 | +0.0036 | 5.3% |
| 169 | ss1 | +0.0022 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 5 | 35.7% |
| -2 | 3 | 21.4% |
| +5 | 2 | 14.3% |
| +6 | 2 | 14.3% |
| -3 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 71.4% |
| ss1 | flkL | 3 | 21.4% |
| ss2 | ss2 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 166 | ss1 | +0.0253 | 0.5874 |
| 163 | ss1 | 166 | ss1 | +0.0157 | 0.6797 |
| 164 | ss1 | 166 | ss1 | +0.0116 | 0.5359 |
| 167 | ss1 | 168 | ss1 | +0.0028 | 0.1860 |
| 166 | ss1 | 166 | ss1 | +0.0018 | 0.1097 |

### L23 H15 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 10  |  total attr: +0.0410

**Key mass** (top-1=80%, top-2=93%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0329 | 80.3% |
| 274 | ss2 | +0.0054 | 13.2% |
| 124 | flkL | +0.0011 | 2.6% |
| 277 | ss2 | +0.0008 | 2.0% |
| 94 | other | +0.0008 | 2.0% |

**Query mass** (top-1=46%, top-2=71%, top-3=91%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 168 | ss1 | +0.0187 | 45.7% |
| 165 | ss1 | +0.0105 | 25.7% |
| 167 | ss1 | +0.0081 | 19.7% |
| 166 | ss1 | +0.0026 | 6.3% |
| 274 | ss2 | +0.0011 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -109 | 2 | 20.0% |
| -108 | 1 | 10.0% |
| -111 | 1 | 10.0% |
| -106 | 1 | 10.0% |
| -110 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 80.0% |
| ss2 | flkL | 1 | 10.0% |
| ss1 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 168 | ss1 | 276 | ss2 | +0.0139 | 0.2384 |
| 165 | ss1 | 276 | ss2 | +0.0090 | 0.1850 |
| 167 | ss1 | 276 | ss2 | +0.0074 | 0.6540 |
| 168 | ss1 | 274 | ss2 | +0.0040 | 0.0717 |
| 166 | ss1 | 276 | ss2 | +0.0026 | 0.1125 |

### L25 H10 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 14  |  total attr: +0.0630

**Key mass** (top-1=91%, top-2=96%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | ss1 | +0.0571 | 90.6% |
| 166 | ss1 | +0.0034 | 5.4% |
| 159 | flkL | +0.0009 | 1.4% |
| 153 | flkL | +0.0008 | 1.3% |
| 162 | ss1 | +0.0008 | 1.3% |

**Query mass** (top-1=25%, top-2=45%, top-3=58%)  [DISTR(G173/S169/D174/I172/T171)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | other | +0.0158 | 25.1% |
| 169 | ss1 | +0.0124 | 19.6% |
| 174 | other | +0.0082 | 13.0% |
| 172 | ss1 | +0.0072 | 11.3% |
| 171 | ss1 | +0.0065 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 3 | 21.4% |
| +7 | 3 | 21.4% |
| +6 | 2 | 14.3% |
| +10 | 1 | 7.1% |
| +11 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 42.9% |
| other | ss1 | 5 | 35.7% |
| ss1 | flkL | 1 | 7.1% |
| flkL | flkL | 1 | 7.1% |
| flkL | ss1 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | other | 163 | ss1 | +0.0132 | 0.7951 |
| 169 | ss1 | 163 | ss1 | +0.0124 | 0.8038 |
| 174 | other | 163 | ss1 | +0.0074 | 0.8305 |
| 172 | ss1 | 163 | ss1 | +0.0072 | 0.6606 |
| 171 | ss1 | 163 | ss1 | +0.0065 | 0.7534 |

### L26 H16 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0429

**Key mass** (top-1=21%, top-2=41%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 273 | ss2 | +0.0089 | 20.7% |
| 165 | ss1 | +0.0088 | 20.4% |
| 164 | ss1 | +0.0044 | 10.2% |
| 299 | flkR | +0.0041 | 9.6% |
| 169 | ss1 | +0.0022 | 5.0% |

**Query mass** (top-1=32%, top-2=52%, top-3=64%)  [DISTR(V278/S169/V166/R280)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 278 | ss2 | +0.0136 | 31.7% |
| 169 | ss1 | +0.0086 | 20.0% |
| 166 | ss1 | +0.0052 | 12.0% |
| 280 | ss2 | +0.0028 | 6.4% |
| 167 | ss1 | +0.0025 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -133 | 2 | 8.3% |
| +118 | 2 | 8.3% |
| -103 | 2 | 8.3% |
| +113 | 1 | 4.2% |
| -104 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 9 | 37.5% |
| ss2 | ss1 | 7 | 29.2% |
| ss1 | ss2 | 6 | 25.0% |
| ss2 | flkL | 1 | 4.2% |
| other | flkL | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 278 | ss2 | 165 | ss1 | +0.0088 | 0.1276 |
| 169 | ss1 | 273 | ss2 | +0.0078 | 0.0769 |
| 166 | ss1 | 299 | flkR | +0.0033 | 0.1362 |
| 278 | ss2 | 164 | ss1 | +0.0030 | 0.0947 |
| 273 | ss2 | 169 | ss1 | +0.0022 | 0.0305 |

### L27 H15 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 27  |  total attr: +0.0926

**Key mass** (top-1=28%, top-2=41%, top-3=54%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 278 | ss2 | +0.0263 | 28.4% |
| 165 | ss1 | +0.0118 | 12.7% |
| 274 | ss2 | +0.0117 | 12.6% |
| 164 | ss1 | +0.0080 | 8.6% |
| 168 | ss1 | +0.0059 | 6.3% |

**Query mass** (top-1=27%, top-2=42%, top-3=57%)  [DISTR(A165/V168/V278/D164/K273)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0251 | 27.1% |
| 168 | ss1 | +0.0141 | 15.2% |
| 278 | ss2 | +0.0132 | 14.2% |
| 164 | ss1 | +0.0066 | 7.1% |
| 273 | ss2 | +0.0062 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 2 | 7.4% |
| +113 | 2 | 7.4% |
| +111 | 2 | 7.4% |
| +114 | 2 | 7.4% |
| -106 | 1 | 3.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=59%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 16 | 59.3% |
| ss1 | ss2 | 10 | 37.0% |
| ss2 | flkL | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 278 | ss2 | +0.0210 | 0.2270 |
| 168 | ss1 | 274 | ss2 | +0.0117 | 0.1550 |
| 278 | ss2 | 165 | ss1 | +0.0101 | 0.1913 |
| 164 | ss1 | 278 | ss2 | +0.0043 | 0.0915 |
| 165 | ss1 | 277 | ss2 | +0.0041 | 0.1235 |

### L29 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 46  |  total attr: +0.1186

**Key mass** (top-1=15%, top-2=29%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 273 | ss2 | +0.0179 | 15.1% |
| 165 | ss1 | +0.0170 | 14.3% |
| 280 | ss2 | +0.0127 | 10.8% |
| 169 | ss1 | +0.0087 | 7.4% |
| 166 | ss1 | +0.0086 | 7.2% |

**Query mass** (top-1=16%, top-2=28%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 273 | ss2 | +0.0184 | 15.5% |
| 164 | ss1 | +0.0142 | 12.0% |
| 280 | ss2 | +0.0123 | 10.4% |
| 162 | ss1 | +0.0119 | 10.0% |
| 170 | ss1 | +0.0099 | 8.3% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +111 | 2 | 4.3% |
| -115 | 2 | 4.3% |
| -107 | 2 | 4.3% |
| -116 | 2 | 4.3% |
| +106 | 2 | 4.3% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 14 | 30.4% |
| ss1 | flkR | 10 | 21.7% |
| ss2 | ss1 | 9 | 19.6% |
| flkR | ss1 | 3 | 6.5% |
| flkL | ss2 | 3 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 280 | ss2 | 165 | ss1 | +0.0116 | 0.4408 |
| 170 | ss1 | 273 | ss2 | +0.0099 | 0.2747 |
| 273 | ss2 | 169 | ss1 | +0.0087 | 0.1974 |
| 277 | ss2 | 166 | ss1 | +0.0086 | 0.4958 |
| 164 | ss1 | 279 | ss2 | +0.0078 | 0.1981 |

### L30 H0 — Rank #29

**Tags:** k:DUAL-ANCHOR / q:MULTI-ANCHOR | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.0232

**Key mass** (top-1=50%, top-2=79%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 278 | ss2 | +0.0115 | 49.6% |
| 280 | ss2 | +0.0068 | 29.3% |
| 168 | ss1 | +0.0015 | 6.3% |
| 167 | ss1 | +0.0011 | 4.7% |
| 276 | ss2 | +0.0009 | 3.8% |

**Query mass** (top-1=36%, top-2=68%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 167 | ss1 | +0.0084 | 36.4% |
| 165 | ss1 | +0.0074 | 32.1% |
| 278 | ss2 | +0.0028 | 12.3% |
| 273 | ss2 | +0.0021 | 9.2% |
| 162 | ss1 | +0.0015 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 2 | 18.2% |
| -111 | 1 | 9.1% |
| -115 | 1 | 9.1% |
| -118 | 1 | 9.1% |
| +105 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 45.5% |
| ss2 | ss1 | 3 | 27.3% |
| ss2 | ss2 | 2 | 18.2% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 167 | ss1 | 278 | ss2 | +0.0076 | 0.2729 |
| 165 | ss1 | 280 | ss2 | +0.0045 | 0.4272 |
| 165 | ss1 | 278 | ss2 | +0.0030 | 0.1045 |
| 162 | ss1 | 280 | ss2 | +0.0015 | 0.1677 |
| 273 | ss2 | 168 | ss1 | +0.0015 | 0.1308 |

### L31 H17 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 38  |  total attr: +0.0491

**Key mass** (top-1=31%, top-2=44%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0153 | 31.1% |
| 338 | flkR | +0.0063 | 12.9% |
| 282 | ss2 | +0.0034 | 7.0% |
| 271 | other | +0.0031 | 6.3% |
| 270 | other | +0.0031 | 6.3% |

**Query mass** (top-1=28%, top-2=37%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 167 | ss1 | +0.0138 | 28.2% |
| 290 | flkR | +0.0045 | 9.2% |
| 169 | ss1 | +0.0042 | 8.6% |
| 168 | ss1 | +0.0040 | 8.2% |
| 283 | flkR | +0.0039 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +119 | 2 | 5.3% |
| -104 | 1 | 2.6% |
| +170 | 1 | 2.6% |
| -118 | 1 | 2.6% |
| +168 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=21%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 8 | 21.1% |
| ss1 | ss2 | 7 | 18.4% |
| flkR | other | 5 | 13.2% |
| flkR | ss1 | 4 | 10.5% |
| ss1 | flkR | 3 | 7.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 167 | ss1 | 271 | other | +0.0031 | 0.0626 |
| 169 | ss1 | -1 | other | +0.0030 | 0.0970 |
| 164 | ss1 | 282 | ss2 | +0.0024 | 0.1752 |
| 167 | ss1 | -1 | other | +0.0023 | 0.0799 |
| 167 | ss1 | 270 | other | +0.0023 | 0.0825 |

### L32 H13 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 24  |  total attr: +0.0741

**Key mass** (top-1=19%, top-2=34%, top-3=42%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | ss1 | +0.0142 | 19.2% |
| 280 | ss2 | +0.0109 | 14.7% |
| 278 | ss2 | +0.0062 | 8.3% |
| 277 | ss2 | +0.0058 | 7.8% |
| 165 | ss1 | +0.0056 | 7.5% |

**Query mass** (top-1=22%, top-2=34%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 273 | ss2 | +0.0166 | 22.3% |
| 280 | ss2 | +0.0090 | 12.2% |
| 163 | ss1 | +0.0071 | 9.6% |
| 164 | ss1 | +0.0061 | 8.2% |
| 278 | ss2 | +0.0059 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +115 | 2 | 8.3% |
| +111 | 2 | 8.3% |
| -111 | 2 | 8.3% |
| -105 | 2 | 8.3% |
| -115 | 2 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 15 | 62.5% |
| ss2 | ss1 | 9 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 273 | ss2 | 169 | ss1 | +0.0133 | 0.0875 |
| 163 | ss1 | 280 | ss2 | +0.0071 | 0.1117 |
| 279 | ss2 | 164 | ss1 | +0.0052 | 0.2065 |
| 278 | ss2 | 167 | ss1 | +0.0051 | 0.0981 |
| 280 | ss2 | 165 | ss1 | +0.0047 | 0.4029 |

### L32 H18 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 34  |  total attr: +0.1509

**Key mass** (top-1=25%, top-2=42%, top-3=53%)  [DISTR(L167/V278/R280/V168/K273)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 167 | ss1 | +0.0380 | 25.2% |
| 278 | ss2 | +0.0248 | 16.5% |
| 280 | ss2 | +0.0174 | 11.5% |
| 168 | ss1 | +0.0138 | 9.1% |
| 273 | ss2 | +0.0136 | 9.0% |

**Query mass** (top-1=16%, top-2=31%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 278 | ss2 | +0.0246 | 16.3% |
| 273 | ss2 | +0.0226 | 15.0% |
| 167 | ss1 | +0.0167 | 11.0% |
| 275 | ss2 | +0.0145 | 9.6% |
| 163 | ss1 | +0.0142 | 9.4% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +111 | 2 | 5.9% |
| -111 | 2 | 5.9% |
| +105 | 2 | 5.9% |
| -113 | 2 | 5.9% |
| -105 | 2 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 18 | 52.9% |
| ss1 | ss2 | 16 | 47.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 278 | ss2 | 167 | ss1 | +0.0202 | 0.2371 |
| 167 | ss1 | 278 | ss2 | +0.0167 | 0.1956 |
| 163 | ss1 | 280 | ss2 | +0.0142 | 0.1363 |
| 275 | ss2 | 167 | ss1 | +0.0137 | 0.2498 |
| 273 | ss2 | 169 | ss1 | +0.0108 | 0.0434 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #30 | L0 | H8 | 4 | +0.0062 | SINGLE-ANCHOR | G103 | DUAL-ANCHOR | F142/A165 |  |  |
| #21 | L1 | H0 | 6 | +0.0391 | SINGLE-ANCHOR | G103 | DISTRIBUTED | S97/M98/A95 |  |  |
| #27 | L5 | H2 | 6 | +0.0400 | DISTRIBUTED | E102/D105/G101 | SINGLE-ANCHOR | L94 |  |  |
| #4 | L6 | H13 | 7 | +0.1257 | SINGLE-ANCHOR | V166 | SINGLE-ANCHOR | L94 |  |  |
| #1 | L6 | H19 | 2 | +0.1789 | SINGLE-ANCHOR | I127 | SINGLE-ANCHOR | L94 |  |  |
| #20 | L10 | H6 | 4 | +0.0421 | SINGLE-ANCHOR | L94 | SINGLE-ANCHOR | M116 |  |  |
| #6 | L10 | H9 | 45 | +0.1102 | SINGLE-ANCHOR | L94 | DISTRIBUTED |  |  |  |
| #9 | L11 | H16 | 8 | +0.0823 | SINGLE-ANCHOR | M276 | SINGLE-ANCHOR | L94 |  |  |
| #17 | L12 | H8 | 21 | +0.1030 | SINGLE-ANCHOR | L94 | DISTRIBUTED |  |  |  |
| #10 | L12 | H10 | 10 | +0.0551 | SINGLE-ANCHOR | L94 | SINGLE-ANCHOR | M116 |  |  |
| #14 | L12 | H16 | 7 | +0.0248 | SINGLE-ANCHOR | M276 | SINGLE-ANCHOR | L94 |  |  |
| #8 | L12 | H19 | 23 | +0.1235 | SINGLE-ANCHOR | L94 | DISTRIBUTED |  |  |  |
| #11 | L13 | H14 | 21 | +0.0501 | DUAL-ANCHOR | M116/L94 | DISTRIBUTED |  |  |  |
| #15 | L13 | H18 | 41 | +0.0900 | DUAL-ANCHOR | M276/L94 | DISTRIBUTED |  |  |  |
| #23 | L14 | H7 | 20 | +0.0804 | SINGLE-ANCHOR | L94 | DISTRIBUTED |  |  |  |
| #13 | L14 | H9 | 24 | +0.0893 | DUAL-ANCHOR | L94/M276 | DISTRIBUTED | V166/G163/V168/D164/A165 |  |  |
| #16 | L17 | H10 | 11 | +0.0662 | SINGLE-ANCHOR | V166 | DISTRIBUTED | V166/A165/G170 |  |  |
| #26 | L20 | H5 | 11 | +0.0468 | SINGLE-ANCHOR | V166 | DISTRIBUTED | A165/D164/K161 |  | INTRA:ss1 |
| #18 | L20 | H13 | 10 | +0.0662 | SINGLE-ANCHOR | G163 | SINGLE-ANCHOR | V168 |  | INTRA:ss1 |
| #22 | L21 | H13 | 7 | +0.0451 | SINGLE-ANCHOR | V166 | DUAL-ANCHOR | A165/L167 |  | INTRA:ss1 |
| #19 | L23 | H0 | 14 | +0.0669 | SINGLE-ANCHOR | V166 | MULTI-ANCHOR |  | POSITIONAL | INTRA:ss1 |
| #24 | L23 | H15 | 10 | +0.0410 | SINGLE-ANCHOR | M276 | DUAL-ANCHOR | V168/A165 |  | CROSS:ss1→ss2 |
| #28 | L25 | H10 | 14 | +0.0630 | SINGLE-ANCHOR | G163 | DISTRIBUTED | G173/S169/D174/I172/T171 |  | INTRA:ss1 |
| #12 | L26 | H16 | 24 | +0.0429 | DISTRIBUTED |  | DISTRIBUTED | V278/S169/V166/R280 |  |  |
| #7 | L27 | H15 | 27 | +0.0926 | DISTRIBUTED |  | DISTRIBUTED | A165/V168/V278/D164/K273 |  | CROSS:ss2→ss1 |
| #3 | L29 | H18 | 46 | +0.1186 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #29 | L30 | H0 | 11 | +0.0232 | DUAL-ANCHOR | V278/R280 | MULTI-ANCHOR |  |  | CROSS:ss1→ss2 |
| #25 | L31 | H17 | 38 | +0.0491 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #5 | L32 | H13 | 24 | +0.0741 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #2 | L32 | H18 | 34 | +0.1509 | DISTRIBUTED | L167/V278/R280/V168/K273 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
