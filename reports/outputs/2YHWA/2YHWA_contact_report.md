# Contact Pattern Analysis: 2YHWA

Generated: 2026-03-22 21:31:56   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2YHWA |
| Contact pair | (161, 288) |
| ss1 | [156, 167) |
| ss2 | [283, 294) |
| Clean flank | 62 |
| Corrupt flank | 61 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.8796 |
| Corrupt metric | 0.0104 |
| Gap | 0.8692 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 400 | 76.28% |
| positive IE | 140 | 77.29% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H13 | +0.2509 |
| 2 | L32 | H18 | +0.1981 |
| 3 | L10 | H9 | +0.1952 |
| 4 | L14 | H13 | +0.1854 |
| 5 | L16 | H7 | +0.1370 |
| 6 | L11 | H16 | +0.1351 |
| 7 | L29 | H18 | +0.1269 |
| 8 | L13 | H2 | +0.1033 |
| 9 | L30 | H1 | +0.1025 |
| 10 | L17 | H1 | +0.0997 |
| 11 | L8 | H11 | +0.0995 |
| 12 | L0 | H7 | +0.0926 |
| 13 | L12 | H9 | +0.0837 |
| 14 | L6 | H5 | +0.0726 |
| 15 | L0 | H4 | +0.0699 |
| 16 | L6 | H19 | +0.0639 |
| 17 | L31 | H17 | +0.0638 |
| 18 | L27 | H15 | +0.0614 |
| 19 | L11 | H14 | +0.0539 |
| 20 | L15 | H14 | +0.0532 |
| 21 | L26 | H16 | +0.0473 |
| 22 | L15 | H2 | +0.0469 |
| 23 | L22 | H10 | +0.0460 |
| 24 | L4 | H0 | +0.0450 |
| 25 | L17 | H13 | +0.0449 |
| 26 | L16 | H1 | +0.0433 |
| 27 | L14 | H14 | +0.0431 |
| 28 | L0 | H13 | +0.0425 |
| 29 | L12 | H8 | +0.0416 |
| 30 | L22 | H14 | +0.0416 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | -0.00% |
| 3 | -0.00% |
| 4 | -0.00% |
| 5 | 0.00% |
| 6 | 0.00% |
| 7 | 0.00% |
| 8 | 0.01% |
| 9 | 0.01% |
| 10 | 0.01% |
| 20 | 0.08% |
| 80 | 12.03% |
| 450 | 139.33% |

## Cell Attribution Analysis

Total cells: 15,023,588

- Positive: 7,501,854
- Negative: 7,518,983

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000051 | 1,502,360 |
| 95th | +0.00000175 | 751,181 |
| 99th | +0.00001535 | 150,237 |
| 99.5th | +0.00003325 | 75,119 |
| 99.9th | +0.00017048 | 15,024 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L8 | H11 | 92 | other | 287 | ss2 | +0.233054 | 0.181429 |
| L14 | H13 | 170 | other | 165 | ss1 | +0.226913 | 0.542523 |
| L10 | H9 | 165 | ss1 | 92 | other | +0.153911 | 0.127586 |
| L6 | H19 | 92 | other | 134 | flkL | +0.117421 | 0.052977 |
| L10 | H9 | 165 | ss1 | 287 | ss2 | +0.109402 | 0.082926 |
| L6 | H5 | 287 | ss2 | 330 | flkR | +0.096607 | 0.013233 |
| L14 | H14 | 170 | other | 165 | ss1 | +0.062014 | 0.523882 |
| L11 | H16 | 92 | other | 165 | ss1 | +0.053759 | 0.427575 |
| L8 | H12 | 165 | ss1 | 287 | ss2 | +0.047198 | 0.038999 |
| L8 | H7 | 165 | ss1 | 126 | flkL | +0.046779 | 0.031131 |
| L0 | H7 | 92 | other | 94 | flkL | +0.044428 | 0.018965 |
| L1 | H1 | 92 | other | 94 | flkL | +0.041364 | 0.039052 |
| L2 | H9 | 94 | flkL | 94 | flkL | +0.038973 | 0.243650 |
| L4 | H0 | 92 | other | 94 | flkL | +0.038932 | 0.056621 |
| L11 | H14 | 92 | other | 165 | ss1 | +0.037942 | 0.116329 |
| L12 | H8 | 165 | ss1 | 287 | ss2 | +0.037768 | 0.163500 |
| L8 | H19 | 92 | other | 126 | flkL | +0.036714 | 0.022363 |
| L13 | H13 | 287 | ss2 | 165 | ss1 | +0.035078 | 0.465623 |
| L11 | H14 | 287 | ss2 | 165 | ss1 | +0.033823 | 0.184254 |
| L16 | H9 | 170 | other | 165 | ss1 | +0.033692 | 0.453723 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L13 | H1 | 136 | flkL | 165 | ss1 | -0.013421 | 0.539883 |
| L11 | H18 | 159 | ss1 | 92 | other | -0.013489 | 0.372983 |
| L14 | H13 | 172 | other | 165 | ss1 | -0.014544 | 0.540207 |
| L7 | H7 | 92 | other | 94 | flkL | -0.015075 | 0.019444 |
| L12 | H8 | 343 | flkR | 287 | ss2 | -0.015110 | 0.587287 |
| L16 | H7 | 164 | ss1 | 165 | ss1 | -0.015146 | 0.481059 |
| L2 | H9 | 95 | flkL | 94 | flkL | -0.016411 | 0.223230 |
| L11 | H18 | 165 | ss1 | 111 | flkL | -0.016538 | 0.117934 |
| L15 | H4 | 293 | ss2 | 165 | ss1 | -0.016824 | 0.489828 |
| L14 | H9 | 92 | other | 165 | ss1 | -0.018501 | 0.683275 |
| L14 | H9 | 136 | flkL | 165 | ss1 | -0.019600 | 0.470080 |
| L5 | H7 | 165 | ss1 | 98 | flkL | -0.020023 | 0.013669 |
| L15 | H18 | 165 | ss1 | 136 | flkL | -0.020487 | 0.462761 |
| L14 | H9 | 165 | ss1 | -1 | other | -0.020895 | 0.264173 |
| L14 | H13 | 173 | other | 165 | ss1 | -0.021349 | 0.558959 |
| L2 | H9 | 92 | other | 94 | flkL | -0.024680 | 0.115894 |
| L14 | H13 | 167 | other | 165 | ss1 | -0.027750 | 0.688422 |
| L14 | H13 | 162 | ss1 | 165 | ss1 | -0.033710 | 0.814025 |
| L8 | H12 | 92 | other | 287 | ss2 | -0.037254 | 0.067091 |
| L14 | H13 | 163 | ss1 | 165 | ss1 | -0.071201 | 0.702348 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0104 | 0.00% |
| 10 | 10 | 9 | 0.0104 | 0.00% |
| 20 | 20 | 18 | 0.0104 | 0.00% |
| 50 | 50 | 37 | 0.0104 | 0.00% |
| 100 | 100 | 63 | 0.0105 | 0.01% |
| 200 | 200 | 93 | 0.0108 | 0.05% |
| 500 | 500 | 123 | 0.0153 | 0.56% |
| 1000 | 1,000 | 137 | 0.0212 | 1.25% |
| 2000 | 2,000 | 139 | 0.0377 | 3.14% |
| 5000 | 5,000 | 140 | 0.1133 | 11.84% |
| 10000 | 10,000 | 140 | 0.2186 | 23.95% |
| 20000 | 20,000 | 140 | 0.3149 | 35.03% |
| 50000 | 50,000 | 140 | 0.3961 | 44.37% |

## Motif Analysis

### L0 H4 — Rank #15

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 5  |  total attr: +0.0110

**Key mass** (top-1=21%, top-2=42%, top-3=61%)  [DISTR(P102/P284/P326/P125)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | flkL | +0.0023 | 20.9% |
| 284 | ss2 | +0.0023 | 20.8% |
| 326 | flkR | +0.0021 | 19.6% |
| 125 | flkL | +0.0021 | 19.4% |
| 101 | flkL | +0.0021 | 19.3% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | flkL | +0.0110 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 1 | 20.0% |
| -190 | 1 | 20.0% |
| -232 | 1 | 20.0% |
| -31 | 1 | 20.0% |
| -7 | 1 | 20.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 3 | 60.0% |
| flkL | ss2 | 1 | 20.0% |
| flkL | flkR | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | flkL | 102 | flkL | +0.0023 | 0.0015 |
| 94 | flkL | 284 | ss2 | +0.0023 | 0.0015 |
| 94 | flkL | 326 | flkR | +0.0021 | 0.0014 |
| 94 | flkL | 125 | flkL | +0.0021 | 0.0014 |
| 94 | flkL | 101 | flkL | +0.0021 | 0.0017 |

### L0 H7 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 14  |  total attr: +0.1522

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | flkL | +0.1522 | 100.0% |

**Query mass** (top-1=29%, top-2=51%, top-3=67%)  [DISTR(V92/S95/G93/T96)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.0444 | 29.2% |
| 95 | flkL | +0.0325 | 21.3% |
| 93 | other | +0.0254 | 16.7% |
| 96 | flkL | +0.0122 | 8.0% |
| 105 | flkL | +0.0057 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 1 | 7.1% |
| +1 | 1 | 7.1% |
| -1 | 1 | 7.1% |
| +2 | 1 | 7.1% |
| +11 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 9 | 64.3% |
| other | flkL | 3 | 21.4% |
| flkR | flkL | 1 | 7.1% |
| ss1 | flkL | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 92 | other | 94 | flkL | +0.0444 | 0.0190 |
| 95 | flkL | 94 | flkL | +0.0325 | 0.0348 |
| 93 | other | 94 | flkL | +0.0254 | 0.0200 |
| 96 | flkL | 94 | flkL | +0.0122 | 0.0269 |
| 105 | flkL | 94 | flkL | +0.0057 | 0.0171 |

### L0 H13 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:flkR→flkL  |  cells: 1  |  total attr: +0.0021

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | flkL | +0.0021 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 337 | flkR | +0.0021 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +243 | 1 | 100.0% |

**Region-pair profile** (q→k)  [CROSS:flkR→flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 337 | flkR | 94 | flkL | +0.0021 | 0.0022 |

### L4 H0 — Rank #24

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 9  |  total attr: +0.0959

**Key mass** (top-1=49%, top-2=67%, top-3=80%)  [DISTR(I94/T96/G97)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 94 | flkL | +0.0473 | 49.3% |
| 96 | flkL | +0.0166 | 17.3% |
| 97 | flkL | +0.0125 | 13.1% |
| 95 | flkL | +0.0114 | 11.9% |
| 98 | flkL | +0.0046 | 4.8% |

**Query mass** (top-1=72%, top-2=84%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.0690 | 72.0% |
| 89 | other | +0.0118 | 12.3% |
| 93 | other | +0.0104 | 10.9% |
| 95 | flkL | +0.0046 | 4.8% |

**Offset distribution [frequency]** (top-2 coverage: 56%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 3 | 33.3% |
| -2 | 2 | 22.2% |
| -4 | 2 | 22.2% |
| -5 | 2 | 22.2% |

**Region-pair profile** (q→k)  (top=78%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 7 | 77.8% |
| flkL | flkL | 1 | 11.1% |
| other | other | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 92 | other | 94 | flkL | +0.0389 | 0.0566 |
| 92 | other | 95 | flkL | +0.0114 | 0.0589 |
| 92 | other | 96 | flkL | +0.0095 | 0.0417 |
| 92 | other | 97 | flkL | +0.0091 | 0.0507 |
| 89 | other | 94 | flkL | +0.0084 | 0.0138 |

### L6 H5 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 7  |  total attr: +0.1587

**Key mass** (top-1=61%, top-2=75%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 330 | flkR | +0.0966 | 60.9% |
| 331 | flkR | +0.0230 | 14.5% |
| 133 | flkL | +0.0170 | 10.7% |
| 130 | flkL | +0.0135 | 8.5% |
| 146 | flkL | +0.0035 | 2.2% |

**Query mass** (top-1=75%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | ss2 | +0.1196 | 75.4% |
| 92 | other | +0.0391 | 24.6% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -43 | 1 | 14.3% |
| -44 | 1 | 14.3% |
| -41 | 1 | 14.3% |
| -38 | 1 | 14.3% |
| -54 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 71.4% |
| ss2 | flkR | 2 | 28.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 287 | ss2 | 330 | flkR | +0.0966 | 0.0132 |
| 287 | ss2 | 331 | flkR | +0.0230 | 0.0040 |
| 92 | other | 133 | flkL | +0.0170 | 0.0160 |
| 92 | other | 130 | flkL | +0.0135 | 0.0132 |
| 92 | other | 146 | flkL | +0.0035 | 0.0037 |

### L6 H19 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.1553

**Key mass** (top-1=85%, top-2=92%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 134 | flkL | +0.1315 | 84.7% |
| 93 | other | +0.0108 | 6.9% |
| 318 | flkR | +0.0049 | 3.1% |
| 95 | flkL | +0.0040 | 2.6% |
| 91 | other | +0.0021 | 1.3% |

**Query mass** (top-1=76%, top-2=83%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.1174 | 75.6% |
| 165 | ss1 | +0.0115 | 7.4% |
| 287 | ss2 | +0.0086 | 5.6% |
| 93 | other | +0.0058 | 3.8% |
| 91 | other | +0.0056 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -42 | 1 | 9.1% |
| -41 | 1 | 9.1% |
| -43 | 1 | 9.1% |
| -31 | 1 | 9.1% |
| +70 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 3 | 27.3% |
| ss1 | other | 2 | 18.2% |
| ss2 | flkR | 1 | 9.1% |
| ss1 | flkL | 1 | 9.1% |
| ss2 | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 92 | other | 134 | flkL | +0.1174 | 0.0530 |
| 93 | other | 134 | flkL | +0.0058 | 0.0820 |
| 91 | other | 134 | flkL | +0.0056 | 0.0956 |
| 287 | ss2 | 318 | flkR | +0.0049 | 0.0046 |
| 165 | ss1 | 95 | flkL | +0.0040 | 0.0054 |

### L8 H11 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 2  |  total attr: +0.2427

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | ss2 | +0.2427 | 100.0% |

**Query mass** (top-1=96%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.2331 | 96.0% |
| 165 | ss1 | +0.0096 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -195 | 1 | 50.0% |
| -122 | 1 | 50.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 1 | 50.0% |
| ss1 | ss2 | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 92 | other | 287 | ss2 | +0.2331 | 0.1814 |
| 165 | ss1 | 287 | ss2 | +0.0096 | 0.0172 |

### L10 H9 — Rank #3

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 9  |  total attr: +0.3218

**Key mass** (top-1=51%, top-2=89%, top-3=98%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.1648 | 51.2% |
| 287 | ss2 | +0.1202 | 37.4% |
| 165 | ss1 | +0.0309 | 9.6% |
| 94 | flkL | +0.0058 | 1.8% |

**Query mass** (top-1=89%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.2870 | 89.2% |
| 92 | other | +0.0218 | 6.8% |
| 287 | ss2 | +0.0084 | 2.6% |
| -1 | other | +0.0046 | 1.4% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 22.2% |
| +73 | 1 | 11.1% |
| -122 | 1 | 11.1% |
| -195 | 1 | 11.1% |
| -73 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 2 | 22.2% |
| ss1 | other | 1 | 11.1% |
| ss1 | ss2 | 1 | 11.1% |
| ss1 | ss1 | 1 | 11.1% |
| other | ss2 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 92 | other | +0.1539 | 0.1276 |
| 165 | ss1 | 287 | ss2 | +0.1094 | 0.0829 |
| 165 | ss1 | 165 | ss1 | +0.0179 | 0.0193 |
| 92 | other | 287 | ss2 | +0.0108 | 0.0599 |
| 92 | other | 165 | ss1 | +0.0085 | 0.0651 |

### L11 H14 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.1264

**Key mass** (top-1=88%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.1115 | 88.2% |
| 92 | other | +0.0149 | 11.8% |

**Query mass** (top-1=37%, top-2=63%, top-3=76%)  [DISTR(V92/V287/?343)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.0461 | 36.5% |
| 287 | ss2 | +0.0338 | 26.8% |
| 343 | flkR | +0.0161 | 12.8% |
| 300 | flkR | +0.0068 | 5.4% |
| 165 | ss1 | +0.0063 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 18.2% |
| -73 | 1 | 9.1% |
| +122 | 1 | 9.1% |
| +178 | 1 | 9.1% |
| +135 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss1 | 4 | 36.4% |
| ss2 | ss1 | 2 | 18.2% |
| other | other | 2 | 18.2% |
| other | ss1 | 1 | 9.1% |
| ss1 | ss1 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 92 | other | 165 | ss1 | +0.0379 | 0.1163 |
| 287 | ss2 | 165 | ss1 | +0.0338 | 0.1843 |
| 343 | flkR | 165 | ss1 | +0.0161 | 0.3271 |
| 92 | other | 92 | other | +0.0082 | 0.0584 |
| 300 | flkR | 165 | ss1 | +0.0068 | 0.3029 |

### L11 H16 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.1978

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.1978 | 100.0% |

**Query mass** (top-1=27%, top-2=39%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | other | +0.0538 | 27.2% |
| 287 | ss2 | +0.0229 | 11.6% |
| 134 | flkL | +0.0118 | 5.9% |
| 285 | ss2 | +0.0086 | 4.3% |
| 170 | other | +0.0080 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -73 | 1 | 3.7% |
| +122 | 1 | 3.7% |
| -31 | 1 | 3.7% |
| +120 | 1 | 3.7% |
| +5 | 1 | 3.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 9 | 33.3% |
| ss2 | ss1 | 5 | 18.5% |
| flkR | ss1 | 5 | 18.5% |
| ss1 | ss1 | 5 | 18.5% |
| other | ss1 | 3 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 92 | other | 165 | ss1 | +0.0538 | 0.4276 |
| 287 | ss2 | 165 | ss1 | +0.0229 | 0.5782 |
| 134 | flkL | 165 | ss1 | +0.0118 | 0.3901 |
| 285 | ss2 | 165 | ss1 | +0.0086 | 0.2119 |
| 170 | other | 165 | ss1 | +0.0080 | 0.0268 |

### L12 H8 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | flkR→ss2  |  cells: 7  |  total attr: +0.0636

**Key mass** (top-1=89%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | ss2 | +0.0565 | 88.9% |
| 92 | other | +0.0036 | 5.7% |
| 165 | ss1 | +0.0035 | 5.5% |

**Query mass** (top-1=65%, top-2=80%, top-3=86%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0414 | 65.1% |
| 335 | flkR | +0.0094 | 14.8% |
| 318 | flkR | +0.0036 | 5.7% |
| 287 | ss2 | +0.0035 | 5.5% |
| 332 | flkR | +0.0033 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -122 | 1 | 14.3% |
| +48 | 1 | 14.3% |
| +31 | 1 | 14.3% |
| +73 | 1 | 14.3% |
| +122 | 1 | 14.3% |

**Region-pair profile** (q→k)  [flkR→ss2]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 4 | 57.1% |
| ss1 | ss2 | 1 | 14.3% |
| ss1 | other | 1 | 14.3% |
| ss2 | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 287 | ss2 | +0.0378 | 0.1635 |
| 335 | flkR | 287 | ss2 | +0.0094 | 0.6883 |
| 318 | flkR | 287 | ss2 | +0.0036 | 0.2867 |
| 165 | ss1 | 92 | other | +0.0036 | 0.0756 |
| 287 | ss2 | 165 | ss1 | +0.0035 | 0.0424 |

### L12 H9 — Rank #13

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 18  |  total attr: +0.1099

**Key mass** (top-1=51%, top-2=79%, top-3=83%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | ss2 | +0.0565 | 51.4% |
| 165 | ss1 | +0.0307 | 27.9% |
| 90 | other | +0.0040 | 3.7% |
| 290 | ss2 | +0.0037 | 3.4% |
| 168 | other | +0.0037 | 3.4% |

**Query mass** (top-1=23%, top-2=36%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | other | +0.0252 | 23.0% |
| 293 | ss2 | +0.0147 | 13.4% |
| 92 | other | +0.0095 | 8.7% |
| 291 | ss2 | +0.0093 | 8.5% |
| 289 | ss2 | +0.0086 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 3 | 16.7% |
| +2 | 3 | 16.7% |
| +3 | 3 | 16.7% |
| -3 | 2 | 11.1% |
| +6 | 1 | 5.6% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 8 | 44.4% |
| other | other | 4 | 22.2% |
| ss1 | ss1 | 3 | 16.7% |
| other | ss1 | 1 | 5.6% |
| flkR | ss2 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | other | 165 | ss1 | +0.0215 | 0.1380 |
| 293 | ss2 | 287 | ss2 | +0.0147 | 0.5337 |
| 291 | ss2 | 287 | ss2 | +0.0093 | 0.6064 |
| 289 | ss2 | 287 | ss2 | +0.0086 | 0.3120 |
| 290 | ss2 | 287 | ss2 | +0.0080 | 0.5441 |

### L13 H2 — Rank #8

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 12  |  total attr: +0.1241

**Key mass** (top-1=57%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | ss2 | +0.0711 | 57.3% |
| 165 | ss1 | +0.0529 | 42.7% |

**Query mass** (top-1=20%, top-2=37%, top-3=50%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | other | +0.0248 | 20.0% |
| 289 | ss2 | +0.0212 | 17.1% |
| 164 | ss1 | +0.0157 | 12.7% |
| 290 | ss2 | +0.0139 | 11.2% |
| 161 | ss1 | +0.0096 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 2 | 16.7% |
| -1 | 2 | 16.7% |
| +2 | 1 | 8.3% |
| +3 | 1 | 8.3% |
| -4 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 7 | 58.3% |
| ss1 | ss1 | 3 | 25.0% |
| other | ss1 | 1 | 8.3% |
| flkR | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | other | 165 | ss1 | +0.0248 | 0.6078 |
| 289 | ss2 | 287 | ss2 | +0.0212 | 0.6417 |
| 164 | ss1 | 165 | ss1 | +0.0157 | 0.5568 |
| 290 | ss2 | 287 | ss2 | +0.0139 | 0.6299 |
| 161 | ss1 | 165 | ss1 | +0.0096 | 0.3096 |

### L14 H13 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 14  |  total attr: +0.3393

**Key mass** (top-1=96%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.3260 | 96.1% |
| 159 | ss1 | +0.0056 | 1.7% |
| 162 | ss1 | +0.0053 | 1.6% |
| 161 | ss1 | +0.0024 | 0.7% |

**Query mass** (top-1=71%, top-2=78%, top-3=84%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | other | +0.2402 | 70.8% |
| 161 | ss1 | +0.0247 | 7.3% |
| 160 | ss1 | +0.0202 | 6.0% |
| 168 | other | +0.0197 | 5.8% |
| 159 | ss1 | +0.0092 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 1 | 7.1% |
| -4 | 1 | 7.1% |
| -5 | 1 | 7.1% |
| +3 | 1 | 7.1% |
| -6 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 6 | 42.9% |
| ss1 | ss1 | 6 | 42.9% |
| flkL | ss1 | 2 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | other | 165 | ss1 | +0.2269 | 0.5425 |
| 161 | ss1 | 165 | ss1 | +0.0247 | 0.7125 |
| 160 | ss1 | 165 | ss1 | +0.0202 | 0.6329 |
| 168 | other | 165 | ss1 | +0.0197 | 0.5072 |
| 159 | ss1 | 165 | ss1 | +0.0092 | 0.6686 |

### L14 H14 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +0.0896

**Key mass** (top-1=75%, top-2=88%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0669 | 74.7% |
| 287 | ss2 | +0.0122 | 13.7% |
| 164 | ss1 | +0.0076 | 8.5% |
| 86 | other | +0.0028 | 3.1% |

**Query mass** (top-1=78%, top-2=86%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | other | +0.0696 | 77.7% |
| 293 | ss2 | +0.0072 | 8.1% |
| 291 | ss2 | +0.0050 | 5.6% |
| 156 | ss1 | +0.0049 | 5.5% |
| 92 | other | +0.0028 | 3.1% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 3 | 50.0% |
| +5 | 1 | 16.7% |
| +4 | 1 | 16.7% |
| -9 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 2 | 33.3% |
| ss2 | ss2 | 2 | 33.3% |
| ss1 | ss1 | 1 | 16.7% |
| other | other | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | other | 165 | ss1 | +0.0620 | 0.5239 |
| 170 | other | 164 | ss1 | +0.0076 | 0.3090 |
| 293 | ss2 | 287 | ss2 | +0.0072 | 0.4685 |
| 291 | ss2 | 287 | ss2 | +0.0050 | 0.4766 |
| 156 | ss1 | 165 | ss1 | +0.0049 | 0.1665 |

### L15 H2 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 12  |  total attr: +0.0469

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0469 | 100.0% |

**Query mass** (top-1=15%, top-2=29%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0069 | 14.6% |
| 136 | flkL | +0.0066 | 14.0% |
| 170 | other | +0.0055 | 11.7% |
| 161 | ss1 | +0.0047 | 10.0% |
| 162 | ss1 | +0.0036 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 8.3% |
| -29 | 1 | 8.3% |
| +5 | 1 | 8.3% |
| -4 | 1 | 8.3% |
| -3 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 50.0% |
| flkL | ss1 | 2 | 16.7% |
| flkR | ss1 | 2 | 16.7% |
| other | ss1 | 1 | 8.3% |
| ss2 | ss1 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 165 | ss1 | +0.0069 | 0.1259 |
| 136 | flkL | 165 | ss1 | +0.0066 | 0.2086 |
| 170 | other | 165 | ss1 | +0.0055 | 0.0525 |
| 161 | ss1 | 165 | ss1 | +0.0047 | 0.2043 |
| 162 | ss1 | 165 | ss1 | +0.0036 | 0.2044 |

### L15 H14 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 12  |  total attr: +0.1161

**Key mass** (top-1=60%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0702 | 60.5% |
| 287 | ss2 | +0.0459 | 39.5% |

**Query mass** (top-1=22%, top-2=42%, top-3=56%)  [DISTR(F159/S285/G165/L162/I163)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0256 | 22.1% |
| 285 | ss2 | +0.0227 | 19.5% |
| 165 | ss1 | +0.0171 | 14.7% |
| 162 | ss1 | +0.0104 | 9.0% |
| 163 | ss1 | +0.0092 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 2 | 16.7% |
| -3 | 2 | 16.7% |
| +2 | 2 | 16.7% |
| -6 | 1 | 8.3% |
| +0 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 50.0% |
| ss1 | ss1 | 5 | 41.7% |
| other | ss1 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss1 | 165 | ss1 | +0.0256 | 0.6975 |
| 285 | ss2 | 287 | ss2 | +0.0227 | 0.6101 |
| 165 | ss1 | 165 | ss1 | +0.0171 | 0.2522 |
| 162 | ss1 | 165 | ss1 | +0.0104 | 0.6457 |
| 163 | ss1 | 165 | ss1 | +0.0092 | 0.5337 |

### L16 H1 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 6  |  total attr: +0.0392

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 136 | flkL | +0.0392 | 100.0% |

**Query mass** (top-1=46%, top-2=65%, top-3=77%)  [DISTR(L126/G151/R123)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 126 | flkL | +0.0182 | 46.5% |
| 151 | flkL | +0.0072 | 18.3% |
| 123 | flkL | +0.0046 | 11.8% |
| 153 | flkL | +0.0044 | 11.2% |
| 156 | ss1 | +0.0026 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -10 | 1 | 16.7% |
| +15 | 1 | 16.7% |
| -13 | 1 | 16.7% |
| +17 | 1 | 16.7% |
| +20 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 83.3% |
| ss1 | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 126 | flkL | 136 | flkL | +0.0182 | 0.7584 |
| 151 | flkL | 136 | flkL | +0.0072 | 0.5050 |
| 123 | flkL | 136 | flkL | +0.0046 | 0.6722 |
| 153 | flkL | 136 | flkL | +0.0044 | 0.3932 |
| 156 | ss1 | 136 | flkL | +0.0026 | 0.3561 |

### L16 H7 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 29  |  total attr: +0.1456

**Key mass** (top-1=66%, top-2=85%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0957 | 65.8% |
| 287 | ss2 | +0.0274 | 18.8% |
| 92 | other | +0.0187 | 12.8% |
| 162 | ss1 | +0.0038 | 2.6% |

**Query mass** (top-1=22%, top-2=30%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | other | +0.0319 | 21.9% |
| 165 | ss1 | +0.0118 | 8.1% |
| 139 | flkL | +0.0089 | 6.1% |
| 169 | other | +0.0079 | 5.4% |
| 285 | ss2 | +0.0078 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 2 | 6.9% |
| +5 | 1 | 3.4% |
| +73 | 1 | 3.4% |
| +4 | 1 | 3.4% |
| -12 | 1 | 3.4% |

**Region-pair profile** (q→k)  (top=24%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 7 | 24.1% |
| other | ss1 | 4 | 13.8% |
| ss2 | ss2 | 4 | 13.8% |
| ss2 | ss1 | 4 | 13.8% |
| ss1 | ss1 | 3 | 10.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | other | 165 | ss1 | +0.0217 | 0.3463 |
| 165 | ss1 | 92 | other | +0.0118 | 0.2119 |
| 169 | other | 165 | ss1 | +0.0079 | 0.5501 |
| 285 | ss2 | 287 | ss2 | +0.0078 | 0.3205 |
| 163 | ss1 | 165 | ss1 | +0.0076 | 0.4354 |

### L17 H1 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 19  |  total attr: +0.1457

**Key mass** (top-1=67%, top-2=81%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | other | +0.0974 | 66.8% |
| 165 | ss1 | +0.0204 | 14.0% |
| 171 | other | +0.0120 | 8.2% |
| 305 | flkR | +0.0060 | 4.1% |
| 169 | other | +0.0053 | 3.7% |

**Query mass** (top-1=18%, top-2=34%, top-3=49%)  [DISTR(F159/V160/L156/T161/L162)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0257 | 17.6% |
| 160 | ss1 | +0.0234 | 16.1% |
| 156 | ss1 | +0.0219 | 15.0% |
| 161 | ss1 | +0.0207 | 14.2% |
| 162 | ss1 | +0.0182 | 12.5% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -10 | 3 | 15.8% |
| -11 | 2 | 10.5% |
| -9 | 2 | 10.5% |
| -16 | 2 | 10.5% |
| -8 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=63%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 12 | 63.2% |
| flkL | ss1 | 3 | 15.8% |
| ss2 | flkR | 1 | 5.3% |
| other | other | 1 | 5.3% |
| flkL | other | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss1 | 170 | other | +0.0236 | 0.5105 |
| 160 | ss1 | 170 | other | +0.0207 | 0.5045 |
| 161 | ss1 | 170 | other | +0.0173 | 0.4803 |
| 162 | ss1 | 170 | other | +0.0150 | 0.4089 |
| 156 | ss1 | 170 | other | +0.0138 | 0.2923 |

### L17 H13 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 16  |  total attr: +0.0748

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0748 | 100.0% |

**Query mass** (top-1=23%, top-2=33%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 291 | ss2 | +0.0171 | 22.9% |
| 290 | ss2 | +0.0076 | 10.2% |
| 143 | flkL | +0.0069 | 9.3% |
| 287 | ss2 | +0.0064 | 8.6% |
| 331 | flkR | +0.0038 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +126 | 1 | 6.2% |
| +125 | 1 | 6.2% |
| -22 | 1 | 6.2% |
| +122 | 1 | 6.2% |
| +166 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 43.8% |
| flkL | ss1 | 5 | 31.2% |
| flkR | ss1 | 2 | 12.5% |
| ss1 | ss1 | 2 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 291 | ss2 | 165 | ss1 | +0.0171 | 0.5774 |
| 290 | ss2 | 165 | ss1 | +0.0076 | 0.5059 |
| 143 | flkL | 165 | ss1 | +0.0069 | 0.3163 |
| 287 | ss2 | 165 | ss1 | +0.0064 | 0.2557 |
| 331 | flkR | 165 | ss1 | +0.0038 | 0.4286 |

### L22 H10 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.1169

**Key mass** (top-1=48%, top-2=75%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0564 | 48.3% |
| 291 | ss2 | +0.0308 | 26.3% |
| 169 | other | +0.0147 | 12.6% |
| 167 | other | +0.0128 | 10.9% |
| 331 | flkR | +0.0022 | 1.9% |

**Query mass** (top-1=25%, top-2=46%, top-3=59%)  [DISTR(F159/L289/T164/L162/V160)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0291 | 24.8% |
| 289 | ss2 | +0.0246 | 21.0% |
| 164 | ss1 | +0.0158 | 13.5% |
| 162 | ss1 | +0.0104 | 8.9% |
| 160 | ss1 | +0.0097 | 8.3% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 13.3% |
| -5 | 2 | 13.3% |
| -1 | 2 | 13.3% |
| -2 | 1 | 6.7% |
| -6 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 33.3% |
| ss2 | ss2 | 3 | 20.0% |
| ss1 | other | 3 | 20.0% |
| other | other | 2 | 13.3% |
| other | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 289 | ss2 | 291 | ss2 | +0.0246 | 0.7676 |
| 159 | ss1 | 165 | ss1 | +0.0244 | 0.3858 |
| 164 | ss1 | 167 | other | +0.0128 | 0.6177 |
| 162 | ss1 | 165 | ss1 | +0.0104 | 0.6421 |
| 160 | ss1 | 165 | ss1 | +0.0097 | 0.6520 |

### L22 H14 — Rank #30

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 6  |  total attr: +0.0343

**Key mass** (top-1=48%, top-2=65%, top-3=81%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | ss1 | +0.0164 | 47.9% |
| 159 | ss1 | +0.0057 | 16.6% |
| 161 | ss1 | +0.0056 | 16.2% |
| 285 | ss2 | +0.0042 | 12.2% |
| 162 | ss1 | +0.0024 | 7.1% |

**Query mass** (top-1=34%, top-2=51%, top-3=67%)  [DISTR(V292/S285/S290/G291)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 292 | ss2 | +0.0118 | 34.4% |
| 285 | ss2 | +0.0057 | 16.6% |
| 290 | ss2 | +0.0056 | 16.2% |
| 291 | ss2 | +0.0046 | 13.6% |
| 159 | ss1 | +0.0042 | 12.2% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +127 | 2 | 33.3% |
| +126 | 2 | 33.3% |
| +129 | 1 | 16.7% |
| -126 | 1 | 16.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 83.3% |
| ss1 | ss2 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 292 | ss2 | 165 | ss1 | +0.0118 | 0.1395 |
| 285 | ss2 | 159 | ss1 | +0.0057 | 0.1489 |
| 290 | ss2 | 161 | ss1 | +0.0056 | 0.1653 |
| 291 | ss2 | 165 | ss1 | +0.0046 | 0.1553 |
| 159 | ss1 | 285 | ss2 | +0.0042 | 0.0939 |

### L26 H16 — Rank #21

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | CROSS_SSE | CROSS:ss1→ss2  |  cells: 12  |  total attr: +0.0492

**Key mass** (top-1=25%, top-2=48%, top-3=69%)  [DISTR(I288/L289/V287/S285)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 288 | ss2 | +0.0123 | 25.0% |
| 289 | ss2 | +0.0114 | 23.3% |
| 287 | ss2 | +0.0101 | 20.5% |
| 285 | ss2 | +0.0073 | 14.9% |
| 286 | ss2 | +0.0050 | 10.2% |

**Query mass** (top-1=37%, top-2=70%, top-3=82%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 162 | ss1 | +0.0182 | 37.0% |
| 159 | ss1 | +0.0163 | 33.2% |
| 156 | ss1 | +0.0058 | 11.7% |
| 164 | ss1 | +0.0038 | 7.7% |
| 160 | ss1 | +0.0028 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 58%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -127 | 5 | 41.7% |
| -126 | 2 | 16.7% |
| -125 | 2 | 16.7% |
| -129 | 2 | 16.7% |
| -128 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 12 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 162 | ss1 | 289 | ss2 | +0.0077 | 0.1333 |
| 162 | ss1 | 288 | ss2 | +0.0056 | 0.1673 |
| 159 | ss1 | 286 | ss2 | +0.0050 | 0.0912 |
| 162 | ss1 | 287 | ss2 | +0.0049 | 0.2088 |
| 159 | ss1 | 285 | ss2 | +0.0046 | 0.0766 |

### L27 H15 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 10  |  total attr: +0.0399

**Key mass** (top-1=26%, top-2=47%, top-3=63%)  [DISTR(S285/V160/L162/F159)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0103 | 25.8% |
| 160 | ss1 | +0.0083 | 20.8% |
| 162 | ss1 | +0.0066 | 16.7% |
| 159 | ss1 | +0.0063 | 15.9% |
| 288 | ss2 | +0.0031 | 7.8% |

**Query mass** (top-1=37%, top-2=55%, top-3=68%)  [DISTR(S285/F159/L156/L162)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0146 | 36.6% |
| 159 | ss1 | +0.0072 | 18.0% |
| 156 | ss1 | +0.0055 | 13.9% |
| 162 | ss1 | +0.0036 | 9.0% |
| 157 | ss1 | +0.0035 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -129 | 3 | 30.0% |
| +125 | 1 | 10.0% |
| +126 | 1 | 10.0% |
| -126 | 1 | 10.0% |
| +0 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 60.0% |
| ss2 | ss1 | 3 | 30.0% |
| ss1 | ss1 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 285 | ss2 | 160 | ss1 | +0.0083 | 0.2836 |
| 285 | ss2 | 159 | ss1 | +0.0063 | 0.0857 |
| 159 | ss1 | 285 | ss2 | +0.0041 | 0.0616 |
| 162 | ss1 | 162 | ss1 | +0.0036 | 0.1648 |
| 157 | ss1 | 285 | ss2 | +0.0035 | 0.1222 |

### L29 H18 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1003

**Key mass** (top-1=20%, top-2=35%, top-3=45%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0204 | 20.4% |
| 156 | ss1 | +0.0143 | 14.3% |
| 164 | ss1 | +0.0108 | 10.8% |
| 286 | ss2 | +0.0101 | 10.1% |
| 153 | flkL | +0.0078 | 7.8% |

**Query mass** (top-1=33%, top-2=48%, top-3=61%)  [DISTR(L156/S285/L293/L286)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0327 | 32.6% |
| 285 | ss2 | +0.0155 | 15.5% |
| 293 | ss2 | +0.0129 | 12.9% |
| 286 | ss2 | +0.0092 | 9.2% |
| 292 | ss2 | +0.0054 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -129 | 2 | 11.1% |
| +129 | 2 | 11.1% |
| -126 | 2 | 11.1% |
| -130 | 1 | 5.6% |
| +127 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 33.3% |
| ss2 | ss1 | 5 | 27.8% |
| ss2 | flkR | 3 | 16.7% |
| ss2 | flkL | 3 | 16.7% |
| ss1 | flkR | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss1 | 285 | ss2 | +0.0204 | 0.1677 |
| 285 | ss2 | 156 | ss1 | +0.0122 | 0.1622 |
| 293 | ss2 | 164 | ss1 | +0.0108 | 0.0690 |
| 156 | ss1 | 286 | ss2 | +0.0101 | 0.2167 |
| 292 | ss2 | 165 | ss1 | +0.0054 | 0.0591 |

### L30 H1 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0502

**Key mass** (top-1=48%, top-2=67%, top-3=79%)  [DISTR(N158/L162/S285)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss1 | +0.0239 | 47.6% |
| 162 | ss1 | +0.0099 | 19.8% |
| 285 | ss2 | +0.0057 | 11.3% |
| 288 | ss2 | +0.0043 | 8.6% |
| 317 | flkR | +0.0032 | 6.4% |

**Query mass** (top-1=33%, top-2=53%, top-3=67%)  [DISTR(P284/L289/S285/T161)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 284 | ss2 | +0.0165 | 32.9% |
| 289 | ss2 | +0.0099 | 19.8% |
| 285 | ss2 | +0.0074 | 14.7% |
| 161 | ss1 | +0.0043 | 8.6% |
| 286 | ss2 | +0.0032 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +127 | 3 | 37.5% |
| +126 | 1 | 12.5% |
| -127 | 1 | 12.5% |
| -31 | 1 | 12.5% |
| -129 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 50.0% |
| ss1 | ss2 | 3 | 37.5% |
| ss2 | flkR | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 284 | ss2 | 158 | ss1 | +0.0165 | 0.4289 |
| 289 | ss2 | 162 | ss1 | +0.0099 | 0.1997 |
| 285 | ss2 | 158 | ss1 | +0.0074 | 0.8733 |
| 161 | ss1 | 288 | ss2 | +0.0043 | 0.4659 |
| 286 | ss2 | 317 | flkR | +0.0032 | 0.8897 |

### L31 H17 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 10  |  total attr: +0.0594

**Key mass** (top-1=42%, top-2=75%, top-3=89%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0251 | 42.2% |
| 292 | ss2 | +0.0195 | 32.8% |
| 343 | flkR | +0.0083 | 14.0% |
| 327 | flkR | +0.0023 | 3.9% |
| 165 | ss1 | +0.0021 | 3.6% |

**Query mass** (top-1=38%, top-2=74%, top-3=84%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 164 | ss1 | +0.0224 | 37.8% |
| 165 | ss1 | +0.0218 | 36.7% |
| -1 | other | +0.0055 | 9.3% |
| 292 | ss2 | +0.0053 | 9.0% |
| 293 | ss2 | +0.0023 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -127 | 1 | 10.0% |
| +165 | 1 | 10.0% |
| -179 | 1 | 10.0% |
| +293 | 1 | 10.0% |
| -344 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 2 | 20.0% |
| ss2 | other | 2 | 20.0% |
| ss2 | ss1 | 2 | 20.0% |
| ss1 | ss2 | 1 | 10.0% |
| ss1 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 165 | ss1 | 292 | ss2 | +0.0195 | 0.1689 |
| 164 | ss1 | -1 | other | +0.0169 | 0.2967 |
| 164 | ss1 | 343 | flkR | +0.0055 | 0.0836 |
| 292 | ss2 | -1 | other | +0.0032 | 0.0981 |
| -1 | other | 343 | flkR | +0.0028 | 0.0877 |

### L32 H13 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 22  |  total attr: +0.1890

**Key mass** (top-1=16%, top-2=28%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 164 | ss1 | +0.0304 | 16.1% |
| 165 | ss1 | +0.0228 | 12.0% |
| 285 | ss2 | +0.0225 | 11.9% |
| 156 | ss1 | +0.0196 | 10.4% |
| 293 | ss2 | +0.0124 | 6.6% |

**Query mass** (top-1=16%, top-2=30%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0297 | 15.7% |
| 293 | ss2 | +0.0279 | 14.7% |
| 165 | ss1 | +0.0176 | 9.3% |
| 292 | ss2 | +0.0154 | 8.2% |
| 164 | ss1 | +0.0124 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +129 | 4 | 18.2% |
| -129 | 4 | 18.2% |
| -127 | 3 | 13.6% |
| +127 | 2 | 9.1% |
| +126 | 2 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 50.0% |
| ss1 | ss2 | 11 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 293 | ss2 | 164 | ss1 | +0.0279 | 0.2112 |
| 156 | ss1 | 285 | ss2 | +0.0186 | 0.1329 |
| 292 | ss2 | 165 | ss1 | +0.0154 | 0.1116 |
| 164 | ss1 | 293 | ss2 | +0.0124 | 0.0939 |
| 156 | ss1 | 286 | ss2 | +0.0112 | 0.1899 |

### L32 H18 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.1339

**Key mass** (top-1=23%, top-2=41%, top-3=57%)  [DISTR(F159/L293/L156/V292)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss1 | +0.0304 | 22.7% |
| 293 | ss2 | +0.0250 | 18.7% |
| 156 | ss1 | +0.0206 | 15.4% |
| 292 | ss2 | +0.0180 | 13.4% |
| 285 | ss2 | +0.0096 | 7.1% |

**Query mass** (top-1=28%, top-2=46%, top-3=63%)  [DISTR(S285/T164/G165/L156)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | ss2 | +0.0372 | 27.8% |
| 164 | ss1 | +0.0250 | 18.7% |
| 165 | ss1 | +0.0224 | 16.7% |
| 156 | ss1 | +0.0096 | 7.1% |
| 288 | ss2 | +0.0086 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +129 | 3 | 20.0% |
| -126 | 3 | 20.0% |
| -129 | 2 | 13.3% |
| +126 | 2 | 13.3% |
| -127 | 2 | 13.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 53.3% |
| ss2 | ss1 | 7 | 46.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 164 | ss1 | 293 | ss2 | +0.0250 | 0.1152 |
| 285 | ss2 | 159 | ss1 | +0.0218 | 0.2030 |
| 165 | ss1 | 292 | ss2 | +0.0180 | 0.0794 |
| 285 | ss2 | 156 | ss1 | +0.0154 | 0.0670 |
| 288 | ss2 | 159 | ss1 | +0.0086 | 0.1297 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #15 | L0 | H4 | 5 | +0.0110 | DISTRIBUTED | P102/P284/P326/P125 | SINGLE-ANCHOR | I94 |  | INTRA:flkL |
| #12 | L0 | H7 | 14 | +0.1522 | SINGLE-ANCHOR | I94 | DISTRIBUTED | V92/S95/G93/T96 |  | INTRA:flkL |
| #28 | L0 | H13 | 1 | +0.0021 | SINGLE-ANCHOR | I94 | SINGLE-ANCHOR | D337 |  | CROSS:flkR→flkL |
| #24 | L4 | H0 | 9 | +0.0959 | DISTRIBUTED | I94/T96/G97 | SINGLE-ANCHOR | V92 |  |  |
| #14 | L6 | H5 | 7 | +0.1587 | SINGLE-ANCHOR | G330 | SINGLE-ANCHOR | V287 |  |  |
| #16 | L6 | H19 | 11 | +0.1553 | SINGLE-ANCHOR | V134 | SINGLE-ANCHOR | V92 |  |  |
| #11 | L8 | H11 | 2 | +0.2427 | SINGLE-ANCHOR | V287 | SINGLE-ANCHOR | V92 |  |  |
| #3 | L10 | H9 | 9 | +0.3218 | DUAL-ANCHOR | V92/V287 | SINGLE-ANCHOR | G165 |  |  |
| #19 | L11 | H14 | 11 | +0.1264 | SINGLE-ANCHOR | G165 | DISTRIBUTED | V92/V287/?343 |  |  |
| #6 | L11 | H16 | 27 | +0.1978 | SINGLE-ANCHOR | G165 | DISTRIBUTED |  |  |  |
| #29 | L12 | H8 | 7 | +0.0636 | SINGLE-ANCHOR | V287 | SINGLE-ANCHOR | G165 |  | flkR→ss2 |
| #13 | L12 | H9 | 18 | +0.1099 | DUAL-ANCHOR | V287/G165 | DISTRIBUTED |  |  | INTRA:ss2 |
| #8 | L13 | H2 | 12 | +0.1241 | DUAL-ANCHOR | V287/G165 | DISTRIBUTED |  |  | INTRA:ss2 |
| #4 | L14 | H13 | 14 | +0.3393 | SINGLE-ANCHOR | G165 | SINGLE-ANCHOR | G170 |  |  |
| #27 | L14 | H14 | 6 | +0.0896 | SINGLE-ANCHOR | G165 | SINGLE-ANCHOR | G170 |  |  |
| #22 | L15 | H2 | 12 | +0.0469 | SINGLE-ANCHOR | G165 | DISTRIBUTED |  |  | INTRA:ss1 |
| #20 | L15 | H14 | 12 | +0.1161 | SINGLE-ANCHOR | G165 | DISTRIBUTED | F159/S285/G165/L162/I163 |  | INTRA:ss2 |
| #26 | L16 | H1 | 6 | +0.0392 | SINGLE-ANCHOR | V136 | DISTRIBUTED | L126/G151/R123 |  | INTRA:flkL |
| #5 | L16 | H7 | 29 | +0.1456 | SINGLE-ANCHOR | G165 | DISTRIBUTED |  |  |  |
| #10 | L17 | H1 | 19 | +0.1457 | SINGLE-ANCHOR | G170 | DISTRIBUTED | F159/V160/L156/T161/L162 |  |  |
| #25 | L17 | H13 | 16 | +0.0748 | SINGLE-ANCHOR | G165 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #23 | L22 | H10 | 15 | +0.1169 | DUAL-ANCHOR | G165/G291 | DISTRIBUTED | F159/L289/T164/L162/V160 |  |  |
| #30 | L22 | H14 | 6 | +0.0343 | MULTI-ANCHOR |  | DISTRIBUTED | V292/S285/S290/G291 | CROSS_SSE | CROSS:ss2→ss1 |
| #21 | L26 | H16 | 12 | +0.0492 | DISTRIBUTED | I288/L289/V287/S285 | DUAL-ANCHOR | L162/F159 | CROSS_SSE | CROSS:ss1→ss2 |
| #18 | L27 | H15 | 10 | +0.0399 | DISTRIBUTED | S285/V160/L162/F159 | DISTRIBUTED | S285/F159/L156/L162 |  | CROSS:ss1→ss2 |
| #7 | L29 | H18 | 18 | +0.1003 | DISTRIBUTED |  | DISTRIBUTED | L156/S285/L293/L286 |  |  |
| #9 | L30 | H1 | 8 | +0.0502 | DISTRIBUTED | N158/L162/S285 | DISTRIBUTED | P284/L289/S285/T161 | CROSS_SSE | CROSS:ss2→ss1 |
| #17 | L31 | H17 | 10 | +0.0594 | DUAL-ANCHOR | ?-1/V292 | DUAL-ANCHOR | T164/G165 |  |  |
| #1 | L32 | H13 | 22 | +0.1890 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #2 | L32 | H18 | 15 | +0.1339 | DISTRIBUTED | F159/L293/L156/V292 | DISTRIBUTED | S285/T164/G165/L156 |  | CROSS:ss1→ss2 |
