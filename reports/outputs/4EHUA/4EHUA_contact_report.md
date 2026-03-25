# Contact Pattern Analysis: 4EHUA

Generated: 2026-03-22 21:59:14   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4EHUA |
| Contact pair | (97, 211) |
| ss1 | [92, 103) |
| ss2 | [206, 217) |
| Clean flank | 34 |
| Corrupt flank | 33 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.6809 |
| Corrupt metric | 0.0645 |
| Gap | 0.6164 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 110 | 70.01% |
| positive IE | 45 | 72.70% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L17 | H1 | +0.2655 |
| 2 | L32 | H13 | +0.2206 |
| 3 | L32 | H18 | +0.2158 |
| 4 | L0 | H19 | +0.1123 |
| 5 | L30 | H1 | +0.1005 |
| 6 | L29 | H18 | +0.1000 |
| 7 | L16 | H9 | +0.0974 |
| 8 | L18 | H5 | +0.0820 |
| 9 | L14 | H15 | +0.0760 |
| 10 | L16 | H7 | +0.0664 |
| 11 | L15 | H3 | +0.0652 |
| 12 | L8 | H0 | +0.0643 |
| 13 | L14 | H14 | +0.0582 |
| 14 | L14 | H13 | +0.0560 |
| 15 | L27 | H15 | +0.0554 |
| 16 | L6 | H11 | +0.0550 |
| 17 | L26 | H16 | +0.0546 |
| 18 | L7 | H4 | +0.0537 |
| 19 | L5 | H18 | +0.0534 |
| 20 | L20 | H0 | +0.0522 |
| 21 | L10 | H0 | +0.0510 |
| 22 | L13 | H19 | +0.0487 |
| 23 | L10 | H19 | +0.0484 |
| 24 | L11 | H16 | +0.0484 |
| 25 | L10 | H9 | +0.0478 |
| 26 | L22 | H14 | +0.0444 |
| 27 | L19 | H15 | +0.0407 |
| 28 | L17 | H16 | +0.0366 |
| 29 | L12 | H3 | +0.0348 |
| 30 | L6 | H17 | +0.0333 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | 1.35% |
| 3 | 2.33% |
| 4 | 2.24% |
| 5 | 2.96% |
| 6 | 4.10% |
| 7 | 4.96% |
| 8 | 5.01% |
| 9 | 6.12% |
| 10 | 6.11% |
| 20 | 15.82% |
| 80 | 122.22% |
| 450 | 159.44% |

## Cell Attribution Analysis

Total cells: 3,379,753

- Positive: 1,738,651
- Negative: 1,638,895

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000059 | 337,976 |
| 95th | +0.00000183 | 168,988 |
| 99th | +0.00001528 | 33,798 |
| 99.5th | +0.00003498 | 16,899 |
| 99.9th | +0.00018702 | 3,380 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L17 | H1 | 97 | ss1 | 106 | other | +0.125711 | 0.756310 |
| L17 | H1 | 93 | ss1 | 106 | other | +0.061868 | 0.623940 |
| L17 | H1 | 96 | ss1 | 106 | other | +0.061634 | 0.615437 |
| L30 | H1 | 209 | ss2 | 95 | ss1 | +0.059468 | 0.489045 |
| L14 | H15 | 97 | ss1 | 100 | ss1 | +0.049703 | 0.456024 |
| L13 | H19 | 100 | ss1 | 209 | ss2 | +0.045530 | 0.097143 |
| L18 | H5 | 100 | ss1 | 106 | other | +0.041461 | 0.704528 |
| L32 | H13 | 206 | ss2 | 95 | ss1 | +0.033125 | 0.212304 |
| L7 | H4 | 100 | ss1 | 210 | ss2 | +0.031397 | 0.052297 |
| L14 | H14 | 106 | other | 100 | ss1 | +0.031237 | 0.291942 |
| L16 | H9 | 97 | ss1 | 100 | ss1 | +0.028587 | 0.188539 |
| L14 | H15 | 96 | ss1 | 100 | ss1 | +0.027516 | 0.277946 |
| L14 | H13 | 97 | ss1 | 100 | ss1 | +0.026881 | 0.072667 |
| L7 | H4 | 100 | ss1 | 209 | ss2 | +0.026324 | 0.042842 |
| L14 | H13 | 106 | other | 100 | ss1 | +0.024199 | 0.384203 |
| L32 | H18 | 95 | ss1 | 209 | ss2 | +0.023333 | 0.092029 |
| L12 | H3 | 75 | flkL | 100 | ss1 | +0.021402 | 0.284673 |
| L32 | H18 | 208 | ss2 | 93 | ss1 | +0.021053 | 0.195225 |
| L16 | H9 | 100 | ss1 | 106 | other | +0.020842 | 0.449405 |
| L32 | H13 | 95 | ss1 | 206 | ss2 | +0.020202 | 0.129480 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L14 | H13 | 102 | ss1 | 100 | ss1 | -0.009308 | 0.415046 |
| L17 | H1 | 106 | other | 106 | other | -0.009450 | 0.139519 |
| L19 | H3 | 103 | other | 106 | other | -0.009472 | 0.735355 |
| L14 | H13 | 89 | flkL | 100 | ss1 | -0.009591 | 0.185499 |
| L14 | H13 | 104 | other | 100 | ss1 | -0.010190 | 0.358178 |
| L14 | H13 | 103 | other | 100 | ss1 | -0.010359 | 0.414335 |
| L14 | H15 | 89 | flkL | 100 | ss1 | -0.010824 | 0.121993 |
| L8 | H0 | 208 | ss2 | 58 | flkL | -0.011411 | 0.330268 |
| L16 | H2 | 97 | ss1 | 100 | ss1 | -0.011443 | 0.320950 |
| L11 | H16 | 75 | flkL | 100 | ss1 | -0.012104 | 0.232263 |
| L6 | H19 | 100 | ss1 | 209 | ss2 | -0.012325 | 0.046890 |
| L10 | H0 | 75 | flkL | 100 | ss1 | -0.012450 | 0.234811 |
| L8 | H0 | 241 | flkR | 57 | other | -0.012608 | 0.445233 |
| L14 | H13 | 105 | other | 100 | ss1 | -0.012921 | 0.282602 |
| L17 | H1 | 92 | ss1 | 106 | other | -0.018274 | 0.665692 |
| L14 | H13 | 107 | other | 100 | ss1 | -0.021612 | 0.437979 |
| L11 | H16 | 276 | other | 100 | ss1 | -0.026261 | 0.190914 |
| L17 | H1 | 95 | ss1 | 106 | other | -0.045677 | 0.701323 |
| L17 | H1 | 94 | ss1 | 106 | other | -0.056229 | 0.735365 |
| L0 | H19 | 250 | flkR | 250 | flkR | -0.074929 | 0.987957 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0645 | 0.00% |
| 10 | 10 | 8 | 0.0671 | 0.43% |
| 20 | 20 | 12 | 0.0715 | 1.14% |
| 50 | 50 | 25 | 0.0806 | 2.62% |
| 100 | 100 | 34 | 0.0996 | 5.70% |
| 200 | 200 | 41 | 0.1282 | 10.34% |
| 500 | 500 | 44 | 0.2036 | 22.56% |
| 1000 | 1,000 | 44 | 0.3474 | 45.90% |
| 2000 | 2,000 | 45 | 0.5585 | 80.14% |
| 5000 | 5,000 | 45 | 0.7256 | 107.25% |
| 10000 | 10,000 | 45 | 0.7900 | 117.71% |
| 20000 | 20,000 | 45 | 0.8270 | 123.70% |
| 50000 | 50,000 | 45 | 0.8571 | 128.58% |

## Motif Analysis

### L0 H19 — Rank #4

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L5 H18 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 9  |  total attr: +0.0111

**Key mass** (top-1=80%, top-2=94%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 250 | flkR | +0.0089 | 79.6% |
| 239 | flkR | +0.0016 | 13.9% |
| 227 | flkR | +0.0007 | 6.4% |

**Query mass** (top-1=23%, top-2=39%, top-3=53%)  [DISTR(V59/V209/G100/M211/V215)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | flkL | +0.0026 | 23.3% |
| 209 | ss2 | +0.0017 | 15.7% |
| 100 | ss1 | +0.0016 | 13.9% |
| 211 | ss2 | +0.0014 | 12.8% |
| 215 | ss2 | +0.0011 | 10.2% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -191 | 1 | 11.1% |
| -139 | 1 | 11.1% |
| -39 | 1 | 11.1% |
| -35 | 1 | 11.1% |
| -40 | 1 | 11.1% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 6 | 66.7% |
| flkL | flkR | 2 | 22.2% |
| ss1 | flkR | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 59 | flkL | 250 | flkR | +0.0026 | 0.0358 |
| 100 | ss1 | 239 | flkR | +0.0016 | 0.0016 |
| 211 | ss2 | 250 | flkR | +0.0014 | 0.0358 |
| 215 | ss2 | 250 | flkR | +0.0011 | 0.0349 |
| 210 | ss2 | 250 | flkR | +0.0011 | 0.0409 |

### L6 H11 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 7  |  total attr: +0.0167

**Key mass** (top-1=67%, top-2=79%, top-3=87%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | flkL | +0.0112 | 66.8% |
| 65 | flkL | +0.0021 | 12.6% |
| 61 | flkL | +0.0013 | 7.5% |
| 58 | flkL | +0.0011 | 6.5% |
| 234 | flkR | +0.0011 | 6.5% |

**Query mass** (top-1=73%, top-2=86%, top-3=94%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0123 | 73.5% |
| 89 | flkL | +0.0021 | 12.7% |
| 209 | ss2 | +0.0013 | 7.5% |
| 73 | flkL | +0.0010 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +41 | 1 | 14.3% |
| +30 | 1 | 14.3% |
| +35 | 1 | 14.3% |
| +148 | 1 | 14.3% |
| +42 | 1 | 14.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 3 | 42.9% |
| flkL | flkL | 2 | 28.6% |
| ss2 | flkL | 1 | 14.3% |
| ss1 | flkR | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 100 | ss1 | 59 | flkL | +0.0080 | 0.0337 |
| 89 | flkL | 59 | flkL | +0.0021 | 0.0531 |
| 100 | ss1 | 65 | flkL | +0.0021 | 0.0104 |
| 209 | ss2 | 61 | flkL | +0.0013 | 0.0091 |
| 100 | ss1 | 58 | flkL | +0.0011 | 0.0069 |

### L6 H17 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 30  |  total attr: +0.0571

**Key mass** (top-1=16%, top-2=27%, top-3=34%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 249 | flkR | +0.0093 | 16.3% |
| 58 | flkL | +0.0062 | 10.8% |
| 252 | other | +0.0042 | 7.4% |
| 248 | flkR | +0.0038 | 6.7% |
| 60 | flkL | +0.0037 | 6.4% |

**Query mass** (top-1=13%, top-2=24%, top-3=31%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | flkR | +0.0074 | 12.9% |
| 209 | ss2 | +0.0061 | 10.6% |
| 60 | flkL | +0.0044 | 7.7% |
| 221 | flkR | +0.0043 | 7.6% |
| 100 | ss1 | +0.0042 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 15 | 50.0% |
| +10 | 2 | 6.7% |
| -152 | 1 | 3.3% |
| -28 | 1 | 3.3% |
| -23 | 1 | 3.3% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 7 | 23.3% |
| flkL | flkL | 6 | 20.0% |
| ss2 | ss2 | 4 | 13.3% |
| ss2 | flkR | 3 | 10.0% |
| ss1 | ss1 | 2 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 100 | ss1 | 252 | other | +0.0042 | 0.0119 |
| 60 | flkL | 60 | flkL | +0.0037 | 0.0499 |
| 221 | flkR | 249 | flkR | +0.0035 | 0.0510 |
| 58 | flkL | 58 | flkL | +0.0035 | 0.0655 |
| 249 | flkR | 249 | flkR | +0.0034 | 0.3101 |

### L7 H4 — Rank #18

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 25  |  total attr: +0.0850

**Key mass** (top-1=47%, top-2=89%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 210 | ss2 | +0.0398 | 46.8% |
| 209 | ss2 | +0.0362 | 42.6% |
| 211 | ss2 | +0.0030 | 3.6% |
| 212 | ss2 | +0.0025 | 3.0% |
| 207 | ss2 | +0.0011 | 1.3% |

**Query mass** (top-1=77%, top-2=82%, top-3=85%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0659 | 77.5% |
| 90 | flkL | +0.0038 | 4.5% |
| 92 | ss1 | +0.0024 | 2.8% |
| 87 | flkL | +0.0019 | 2.2% |
| 104 | other | +0.0018 | 2.1% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -110 | 2 | 8.0% |
| -111 | 2 | 8.0% |
| -112 | 2 | 8.0% |
| -109 | 1 | 4.0% |
| -119 | 1 | 4.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=48%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 12 | 48.0% |
| flkL | ss2 | 8 | 32.0% |
| other | ss2 | 3 | 12.0% |
| other | other | 1 | 4.0% |
| ss1 | flkL | 1 | 4.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 100 | ss1 | 210 | ss2 | +0.0314 | 0.0523 |
| 100 | ss1 | 209 | ss2 | +0.0263 | 0.0428 |
| 100 | ss1 | 211 | ss2 | +0.0030 | 0.0097 |
| 100 | ss1 | 212 | ss2 | +0.0025 | 0.0067 |
| 90 | flkL | 209 | ss2 | +0.0025 | 0.0468 |

### L8 H0 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 68  |  total attr: +0.1478

**Key mass** (top-1=16%, top-2=26%, top-3=33%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0235 | 15.9% |
| 89 | flkL | +0.0146 | 9.9% |
| 276 | other | +0.0103 | 7.0% |
| 241 | flkR | +0.0090 | 6.1% |
| 249 | flkR | +0.0068 | 4.6% |

**Query mass** (top-1=19%, top-2=29%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0276 | 18.7% |
| 89 | flkL | +0.0150 | 10.2% |
| 56 | other | +0.0144 | 9.7% |
| 207 | ss2 | +0.0102 | 6.9% |
| 59 | flkL | +0.0092 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 16 | 23.5% |
| -145 | 3 | 4.4% |
| -176 | 2 | 2.9% |
| -109 | 2 | 2.9% |
| -149 | 2 | 2.9% |

**Region-pair profile** (q→k)  (top=24%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 16 | 23.5% |
| ss1 | flkR | 10 | 14.7% |
| flkL | flkL | 7 | 10.3% |
| flkR | flkL | 6 | 8.8% |
| flkL | ss2 | 5 | 7.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 89 | flkL | 89 | flkL | +0.0138 | 0.1536 |
| 100 | ss1 | 276 | other | +0.0103 | 0.0744 |
| 56 | other | 207 | ss2 | +0.0103 | 0.2160 |
| 207 | ss2 | 207 | ss2 | +0.0102 | 0.2524 |
| 56 | other | 241 | flkR | +0.0041 | 0.2090 |

### L10 H0 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0900

**Key mass** (top-1=87%, top-2=92%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0786 | 87.3% |
| 96 | ss1 | +0.0045 | 5.0% |
| 209 | ss2 | +0.0024 | 2.7% |
| 71 | flkL | +0.0014 | 1.5% |
| 69 | flkL | +0.0009 | 1.0% |

**Query mass** (top-1=21%, top-2=38%, top-3=49%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0187 | 20.7% |
| 88 | flkL | +0.0159 | 17.6% |
| 101 | ss1 | +0.0100 | 11.1% |
| 106 | other | +0.0079 | 8.8% |
| 105 | other | +0.0060 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 7.7% |
| +2 | 2 | 7.7% |
| +4 | 2 | 7.7% |
| -12 | 1 | 3.8% |
| +0 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 8 | 30.8% |
| ss1 | ss1 | 7 | 26.9% |
| ss1 | flkL | 5 | 19.2% |
| other | ss1 | 3 | 11.5% |
| ss2 | ss2 | 3 | 11.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 88 | flkL | 100 | ss1 | +0.0159 | 0.1475 |
| 101 | ss1 | 100 | ss1 | +0.0100 | 0.3135 |
| 100 | ss1 | 100 | ss1 | +0.0096 | 0.0399 |
| 106 | other | 100 | ss1 | +0.0079 | 0.2729 |
| 105 | other | 100 | ss1 | +0.0060 | 0.3348 |

### L10 H9 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 54  |  total attr: +0.1350

**Key mass** (top-1=71%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0959 | 71.0% |
| 209 | ss2 | +0.0362 | 26.8% |
| 276 | other | +0.0029 | 2.2% |

**Query mass** (top-1=13%, top-2=21%, top-3=29%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | other | +0.0177 | 13.1% |
| 209 | ss2 | +0.0112 | 8.3% |
| 106 | other | +0.0104 | 7.7% |
| 88 | flkL | +0.0085 | 6.3% |
| 275 | other | +0.0078 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 2 | 3.7% |
| +0 | 2 | 3.7% |
| +3 | 2 | 3.7% |
| +2 | 2 | 3.7% |
| +176 | 1 | 1.9% |

**Region-pair profile** (q→k)  (top=17%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 9 | 16.7% |
| ss1 | ss1 | 8 | 14.8% |
| other | ss1 | 7 | 13.0% |
| flkL | ss2 | 7 | 13.0% |
| flkR | ss2 | 6 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 276 | other | 100 | ss1 | +0.0155 | 0.1853 |
| 209 | ss2 | 100 | ss1 | +0.0112 | 0.4632 |
| 106 | other | 100 | ss1 | +0.0097 | 0.0740 |
| 88 | flkL | 100 | ss1 | +0.0085 | 0.0784 |
| 275 | other | 100 | ss1 | +0.0072 | 0.2609 |

### L10 H19 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 14  |  total attr: +0.0430

**Key mass** (top-1=73%, top-2=82%, top-3=87%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0314 | 73.0% |
| 101 | ss1 | +0.0037 | 8.6% |
| 209 | ss2 | +0.0023 | 5.4% |
| 106 | other | +0.0017 | 4.0% |
| 107 | other | +0.0014 | 3.2% |

**Query mass** (top-1=24%, top-2=43%, top-3=62%)  [DISTR(D98/G101/V106/I97)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 98 | ss1 | +0.0102 | 23.7% |
| 101 | ss1 | +0.0084 | 19.6% |
| 106 | other | +0.0082 | 19.1% |
| 97 | ss1 | +0.0064 | 15.0% |
| 100 | ss1 | +0.0034 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 21.4% |
| +6 | 2 | 14.3% |
| -2 | 1 | 7.1% |
| +1 | 1 | 7.1% |
| -3 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 57.1% |
| other | ss1 | 3 | 21.4% |
| other | other | 2 | 14.3% |
| ss2 | ss2 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 98 | ss1 | 100 | ss1 | +0.0102 | 0.2071 |
| 101 | ss1 | 100 | ss1 | +0.0064 | 0.3539 |
| 97 | ss1 | 100 | ss1 | +0.0064 | 0.1068 |
| 106 | other | 100 | ss1 | +0.0034 | 0.1991 |
| 103 | other | 100 | ss1 | +0.0027 | 0.1452 |

### L11 H16 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 46  |  total attr: +0.1550

**Key mass** (top-1=92%, top-2=94%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.1426 | 92.0% |
| 276 | other | +0.0024 | 1.6% |
| 213 | ss2 | +0.0022 | 1.4% |
| 214 | ss2 | +0.0020 | 1.3% |
| -1 | other | +0.0018 | 1.2% |

**Query mass** (top-1=11%, top-2=19%, top-3=26%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 88 | flkL | +0.0174 | 11.2% |
| 106 | other | +0.0121 | 7.8% |
| 85 | flkL | +0.0103 | 6.6% |
| 89 | flkL | +0.0089 | 5.7% |
| 276 | other | +0.0083 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 2 | 4.3% |
| -12 | 1 | 2.2% |
| +6 | 1 | 2.2% |
| -15 | 1 | 2.2% |
| -11 | 1 | 2.2% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 13 | 28.3% |
| other | ss1 | 13 | 28.3% |
| ss1 | ss1 | 9 | 19.6% |
| ss2 | ss1 | 4 | 8.7% |
| other | other | 3 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 88 | flkL | 100 | ss1 | +0.0174 | 0.2867 |
| 106 | other | 100 | ss1 | +0.0114 | 0.1042 |
| 85 | flkL | 100 | ss1 | +0.0103 | 0.3004 |
| 89 | flkL | 100 | ss1 | +0.0089 | 0.2679 |
| 98 | ss1 | 100 | ss1 | +0.0070 | 0.1777 |

### L12 H3 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 20  |  total attr: +0.0766

**Key mass** (top-1=73%, top-2=90%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0556 | 72.7% |
| 209 | ss2 | +0.0132 | 17.3% |
| 213 | ss2 | +0.0037 | 4.8% |
| 212 | ss2 | +0.0012 | 1.5% |
| 215 | ss2 | +0.0010 | 1.3% |

**Query mass** (top-1=28%, top-2=38%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | flkL | +0.0214 | 28.0% |
| 88 | flkL | +0.0075 | 9.8% |
| 100 | ss1 | +0.0075 | 9.8% |
| 81 | flkL | +0.0065 | 8.5% |
| 79 | flkL | +0.0056 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 2 | 10.0% |
| -25 | 1 | 5.0% |
| -121 | 1 | 5.0% |
| -19 | 1 | 5.0% |
| -21 | 1 | 5.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 10 | 50.0% |
| ss1 | ss2 | 6 | 30.0% |
| flkL | ss2 | 2 | 10.0% |
| other | flkL | 1 | 5.0% |
| other | ss2 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | flkL | 100 | ss1 | +0.0214 | 0.2847 |
| 88 | flkL | 209 | ss2 | +0.0067 | 0.0597 |
| 81 | flkL | 100 | ss1 | +0.0065 | 0.3441 |
| 79 | flkL | 100 | ss1 | +0.0056 | 0.3166 |
| 83 | flkL | 100 | ss1 | +0.0055 | 0.3163 |

### L13 H19 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 12  |  total attr: +0.0720

**Key mass** (top-1=84%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | ss2 | +0.0602 | 83.7% |
| 275 | other | +0.0089 | 12.3% |
| 276 | other | +0.0022 | 3.1% |
| 59 | flkL | +0.0007 | 0.9% |

**Query mass** (top-1=77%, top-2=83%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0551 | 76.5% |
| 75 | flkL | +0.0044 | 6.1% |
| 97 | ss1 | +0.0042 | 5.9% |
| 95 | ss1 | +0.0034 | 4.7% |
| 96 | ss1 | +0.0027 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -109 | 1 | 8.3% |
| -175 | 1 | 8.3% |
| -134 | 1 | 8.3% |
| -112 | 1 | 8.3% |
| -114 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 41.7% |
| ss1 | other | 4 | 33.3% |
| flkL | ss2 | 1 | 8.3% |
| other | ss2 | 1 | 8.3% |
| other | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 100 | ss1 | 209 | ss2 | +0.0455 | 0.0971 |
| 100 | ss1 | 275 | other | +0.0074 | 0.0409 |
| 75 | flkL | 209 | ss2 | +0.0044 | 0.1137 |
| 97 | ss1 | 209 | ss2 | +0.0035 | 0.0234 |
| 95 | ss1 | 209 | ss2 | +0.0034 | 0.0493 |

### L14 H13 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.1097

**Key mass** (top-1=94%, top-2=96%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.1035 | 94.3% |
| 106 | other | +0.0015 | 1.4% |
| 209 | ss2 | +0.0012 | 1.1% |
| 105 | other | +0.0010 | 0.9% |
| 59 | flkL | +0.0010 | 0.9% |

**Query mass** (top-1=25%, top-2=50%, top-3=67%)  [DISTR(V106/I97/I96/T95)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0276 | 25.2% |
| 97 | ss1 | +0.0269 | 24.5% |
| 96 | ss1 | +0.0185 | 16.9% |
| 95 | ss1 | +0.0135 | 12.3% |
| 75 | flkL | +0.0100 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 13.3% |
| -5 | 2 | 13.3% |
| +6 | 1 | 6.7% |
| -4 | 1 | 6.7% |
| -25 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 33.3% |
| flkL | ss1 | 3 | 20.0% |
| other | other | 3 | 20.0% |
| flkL | flkL | 2 | 13.3% |
| other | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 100 | ss1 | +0.0269 | 0.0727 |
| 106 | other | 100 | ss1 | +0.0242 | 0.3842 |
| 96 | ss1 | 100 | ss1 | +0.0185 | 0.1244 |
| 95 | ss1 | 100 | ss1 | +0.0135 | 0.0741 |
| 75 | flkL | 100 | ss1 | +0.0100 | 0.1468 |

### L14 H14 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:ss1  |  cells: 14  |  total attr: +0.0574

**Key mass** (top-1=81%, top-2=85%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0467 | 81.3% |
| 92 | ss1 | +0.0019 | 3.3% |
| 90 | flkL | +0.0018 | 3.1% |
| 209 | ss2 | +0.0018 | 3.1% |
| 59 | flkL | +0.0014 | 2.5% |

**Query mass** (top-1=54%, top-2=82%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0312 | 54.4% |
| 97 | ss1 | +0.0161 | 28.0% |
| 100 | ss1 | +0.0039 | 6.7% |
| 213 | ss2 | +0.0018 | 3.1% |
| 96 | ss1 | +0.0016 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 3 | 21.4% |
| +6 | 2 | 14.3% |
| +5 | 2 | 14.3% |
| -3 | 1 | 7.1% |
| +4 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 64.3% |
| other | ss1 | 1 | 7.1% |
| ss1 | flkL | 1 | 7.1% |
| ss2 | ss2 | 1 | 7.1% |
| flkL | flkL | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 106 | other | 100 | ss1 | +0.0312 | 0.2919 |
| 97 | ss1 | 100 | ss1 | +0.0131 | 0.0601 |
| 97 | ss1 | 90 | flkL | +0.0018 | 0.0473 |
| 213 | ss2 | 209 | ss2 | +0.0018 | 0.1138 |
| 96 | ss1 | 100 | ss1 | +0.0016 | 0.0346 |

### L14 H15 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:ss1  |  cells: 3  |  total attr: +0.0882

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0882 | 100.0% |

**Query mass** (top-1=56%, top-2=88%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0497 | 56.3% |
| 96 | ss1 | +0.0275 | 31.2% |
| 95 | ss1 | +0.0110 | 12.5% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 1 | 33.3% |
| -4 | 1 | 33.3% |
| -5 | 1 | 33.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 100 | ss1 | +0.0497 | 0.4560 |
| 96 | ss1 | 100 | ss1 | +0.0275 | 0.2779 |
| 95 | ss1 | 100 | ss1 | +0.0110 | 0.1389 |

### L15 H3 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 10  |  total attr: +0.0509

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0491 | 96.6% |
| 60 | flkL | +0.0010 | 1.9% |
| 107 | other | +0.0007 | 1.4% |

**Query mass** (top-1=29%, top-2=50%, top-3=67%)  [DISTR(V106/I96/I97/G100)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0147 | 29.0% |
| 96 | ss1 | +0.0106 | 20.8% |
| 97 | ss1 | +0.0085 | 16.8% |
| 100 | ss1 | +0.0078 | 15.4% |
| 93 | ss1 | +0.0027 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 2 | 20.0% |
| +6 | 1 | 10.0% |
| -4 | 1 | 10.0% |
| -3 | 1 | 10.0% |
| +0 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 50.0% |
| flkL | ss1 | 2 | 20.0% |
| other | ss1 | 1 | 10.0% |
| flkL | flkL | 1 | 10.0% |
| other | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 106 | other | 100 | ss1 | +0.0140 | 0.6195 |
| 96 | ss1 | 100 | ss1 | +0.0106 | 0.1682 |
| 97 | ss1 | 100 | ss1 | +0.0085 | 0.0770 |
| 100 | ss1 | 100 | ss1 | +0.0078 | 0.1753 |
| 93 | ss1 | 100 | ss1 | +0.0027 | 0.1264 |

### L16 H7 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 34  |  total attr: +0.0829

**Key mass** (top-1=68%, top-2=87%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0561 | 67.6% |
| 209 | ss2 | +0.0161 | 19.4% |
| 106 | other | +0.0107 | 12.9% |

**Query mass** (top-1=18%, top-2=34%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0147 | 17.8% |
| 106 | other | +0.0131 | 15.8% |
| 86 | flkL | +0.0080 | 9.6% |
| 96 | ss1 | +0.0073 | 8.8% |
| 98 | ss1 | +0.0060 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 5.9% |
| +0 | 2 | 5.9% |
| -9 | 2 | 5.9% |
| +6 | 1 | 2.9% |
| -14 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=18%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 17.6% |
| other | ss1 | 5 | 14.7% |
| flkR | ss2 | 5 | 14.7% |
| ss1 | ss2 | 4 | 11.8% |
| ss1 | other | 4 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 106 | other | 100 | ss1 | +0.0109 | 0.3863 |
| 97 | ss1 | 100 | ss1 | +0.0086 | 0.2342 |
| 86 | flkL | 100 | ss1 | +0.0080 | 0.1251 |
| 96 | ss1 | 100 | ss1 | +0.0047 | 0.1969 |
| 98 | ss1 | 100 | ss1 | +0.0047 | 0.2273 |

### L16 H9 — Rank #7

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0939

**Key mass** (top-1=56%, top-2=85%, top-3=89%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0529 | 56.3% |
| 106 | other | +0.0270 | 28.8% |
| 99 | ss1 | +0.0034 | 3.6% |
| 96 | ss1 | +0.0027 | 2.9% |
| 105 | other | +0.0023 | 2.5% |

**Query mass** (top-1=32%, top-2=61%, top-3=75%)  [DISTR(I97/G100/V106)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0303 | 32.3% |
| 100 | ss1 | +0.0270 | 28.8% |
| 106 | other | +0.0134 | 14.3% |
| 95 | ss1 | +0.0086 | 9.2% |
| 96 | ss1 | +0.0049 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 4 | 19.0% |
| -4 | 4 | 19.0% |
| +9 | 2 | 9.5% |
| -3 | 1 | 4.8% |
| -6 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 33.3% |
| ss1 | other | 6 | 28.6% |
| other | ss1 | 3 | 14.3% |
| flkL | ss1 | 2 | 9.5% |
| ss1 | flkL | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 100 | ss1 | +0.0286 | 0.1885 |
| 100 | ss1 | 106 | other | +0.0208 | 0.4494 |
| 106 | other | 100 | ss1 | +0.0096 | 0.7522 |
| 95 | ss1 | 100 | ss1 | +0.0072 | 0.0766 |
| 96 | ss1 | 100 | ss1 | +0.0049 | 0.0689 |

### L17 H1 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 49  |  total attr: +0.3501

**Key mass** (top-1=81%, top-2=87%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.2833 | 80.9% |
| 105 | other | +0.0218 | 6.2% |
| 97 | ss1 | +0.0168 | 4.8% |
| 100 | ss1 | +0.0062 | 1.8% |
| 209 | ss2 | +0.0057 | 1.6% |

**Query mass** (top-1=38%, top-2=58%, top-3=77%)  [DISTR(I97/T93/I96)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.1333 | 38.1% |
| 93 | ss1 | +0.0701 | 20.0% |
| 96 | ss1 | +0.0672 | 19.2% |
| 95 | ss1 | +0.0164 | 4.7% |
| 98 | ss1 | +0.0136 | 3.9% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 3 | 6.1% |
| -6 | 3 | 6.1% |
| -115 | 3 | 6.1% |
| -4 | 3 | 6.1% |
| -9 | 2 | 4.1% |

**Region-pair profile** (q→k)  (top=24%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 12 | 24.5% |
| ss1 | other | 11 | 22.4% |
| ss1 | ss1 | 11 | 22.4% |
| flkL | other | 7 | 14.3% |
| flkL | ss1 | 7 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 106 | other | +0.1257 | 0.7563 |
| 93 | ss1 | 106 | other | +0.0619 | 0.6239 |
| 96 | ss1 | 106 | other | +0.0616 | 0.6154 |
| 98 | ss1 | 106 | other | +0.0113 | 0.4922 |
| 99 | ss1 | 106 | other | +0.0080 | 0.4107 |

### L17 H16 — Rank #28

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 19  |  total attr: +0.0478

**Key mass** (top-1=23%, top-2=38%, top-3=51%)  [DISTR(V106/I97/G100/K105/L107)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0110 | 23.0% |
| 97 | ss1 | +0.0069 | 14.5% |
| 100 | ss1 | +0.0066 | 13.8% |
| 105 | other | +0.0058 | 12.1% |
| 107 | other | +0.0046 | 9.7% |

**Query mass** (top-1=43%, top-2=63%, top-3=75%)  [DISTR(V106/I97/I96)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0205 | 42.9% |
| 97 | ss1 | +0.0098 | 20.4% |
| 96 | ss1 | +0.0057 | 11.9% |
| 209 | ss2 | +0.0042 | 8.9% |
| 86 | flkL | +0.0013 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 58%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 6 | 31.6% |
| +0 | 5 | 26.3% |
| +1 | 3 | 15.8% |
| -3 | 1 | 5.3% |
| -4 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 36.8% |
| other | other | 6 | 31.6% |
| ss2 | ss2 | 3 | 15.8% |
| flkL | flkL | 2 | 10.5% |
| flkL | other | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 106 | other | 106 | other | +0.0101 | 0.1973 |
| 97 | ss1 | 97 | ss1 | +0.0055 | 0.0917 |
| 106 | other | 105 | other | +0.0047 | 0.1090 |
| 106 | other | 107 | other | +0.0046 | 0.1356 |
| 97 | ss1 | 100 | ss1 | +0.0043 | 0.0660 |

### L18 H5 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 21  |  total attr: +0.0847

**Key mass** (top-1=63%, top-2=71%, top-3=78%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 106 | other | +0.0534 | 63.1% |
| 95 | ss1 | +0.0068 | 8.1% |
| 100 | ss1 | +0.0059 | 7.0% |
| 97 | ss1 | +0.0051 | 6.1% |
| 96 | ss1 | +0.0023 | 2.7% |

**Query mass** (top-1=54%, top-2=69%, top-3=76%)  [DISTR(G100/I97/T93)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0459 | 54.2% |
| 97 | ss1 | +0.0123 | 14.6% |
| 93 | ss1 | +0.0060 | 7.1% |
| 95 | ss1 | +0.0049 | 5.8% |
| 96 | ss1 | +0.0044 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 52%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 8 | 38.1% |
| -1 | 3 | 14.3% |
| -3 | 3 | 14.3% |
| -6 | 2 | 9.5% |
| -9 | 1 | 4.8% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=48%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 47.6% |
| ss1 | other | 3 | 14.3% |
| flkL | flkL | 3 | 14.3% |
| flkL | ss1 | 3 | 14.3% |
| ss2 | ss2 | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 100 | ss1 | 106 | other | +0.0415 | 0.7045 |
| 97 | ss1 | 106 | other | +0.0094 | 0.3634 |
| 93 | ss1 | 95 | ss1 | +0.0060 | 0.1495 |
| 100 | ss1 | 100 | ss1 | +0.0044 | 0.2416 |
| 95 | ss1 | 97 | ss1 | +0.0042 | 0.2628 |

### L19 H15 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 43  |  total attr: +0.0858

**Key mass** (top-1=45%, top-2=63%, top-3=78%)  [DISTR(G100/V106/G213)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0388 | 45.2% |
| 106 | other | +0.0152 | 17.7% |
| 213 | ss2 | +0.0129 | 15.0% |
| 211 | ss2 | +0.0124 | 14.4% |
| 212 | ss2 | +0.0028 | 3.3% |

**Query mass** (top-1=12%, top-2=23%, top-3=33%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0101 | 11.7% |
| 95 | ss1 | +0.0095 | 11.0% |
| 91 | flkL | +0.0085 | 9.9% |
| 94 | ss1 | +0.0085 | 9.9% |
| 93 | ss1 | +0.0075 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 3 | 7.0% |
| -120 | 3 | 7.0% |
| -115 | 3 | 7.0% |
| -9 | 2 | 4.7% |
| -118 | 2 | 4.7% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 16 | 37.2% |
| flkL | ss1 | 15 | 34.9% |
| ss1 | other | 5 | 11.6% |
| other | ss1 | 2 | 4.7% |
| ss1 | ss1 | 2 | 4.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 106 | other | +0.0067 | 0.2554 |
| 91 | flkL | 100 | ss1 | +0.0062 | 0.1819 |
| 81 | flkL | 100 | ss1 | +0.0052 | 0.4207 |
| 56 | other | 100 | ss1 | +0.0041 | 0.7735 |
| 94 | ss1 | 213 | ss2 | +0.0039 | 0.0562 |

### L20 H0 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 29  |  total attr: +0.0795

**Key mass** (top-1=49%, top-2=75%, top-3=81%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0387 | 48.6% |
| 106 | other | +0.0213 | 26.8% |
| 103 | other | +0.0047 | 5.9% |
| 213 | ss2 | +0.0040 | 5.0% |
| 104 | other | +0.0039 | 4.9% |

**Query mass** (top-1=21%, top-2=39%, top-3=53%)  [DISTR(T95/I97/T93/R94/I96)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0168 | 21.2% |
| 97 | ss1 | +0.0143 | 18.0% |
| 93 | ss1 | +0.0113 | 14.2% |
| 94 | ss1 | +0.0109 | 13.7% |
| 96 | ss1 | +0.0050 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 4 | 13.8% |
| -11 | 4 | 13.8% |
| -8 | 4 | 13.8% |
| -9 | 3 | 10.3% |
| -4 | 3 | 10.3% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 12 | 41.4% |
| ss1 | ss1 | 7 | 24.1% |
| flkL | ss1 | 3 | 10.3% |
| ss2 | ss2 | 2 | 6.9% |
| other | ss2 | 1 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 93 | ss1 | 100 | ss1 | +0.0113 | 0.3104 |
| 95 | ss1 | 100 | ss1 | +0.0076 | 0.2883 |
| 97 | ss1 | 106 | other | +0.0075 | 0.2185 |
| 94 | ss1 | 100 | ss1 | +0.0073 | 0.2863 |
| 95 | ss1 | 106 | other | +0.0068 | 0.1338 |

### L22 H14 — Rank #26

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 21  |  total attr: +0.0330

**Key mass** (top-1=26%, top-2=48%, top-3=60%)  [DISTR(R207/R94/H82/V209)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 207 | ss2 | +0.0085 | 25.7% |
| 94 | ss1 | +0.0073 | 22.2% |
| 82 | flkL | +0.0039 | 11.8% |
| 209 | ss2 | +0.0035 | 10.5% |
| 208 | ss2 | +0.0025 | 7.5% |

**Query mass** (top-1=18%, top-2=36%, top-3=52%)  [DISTR(T95/T93/R94/I97/N208)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0060 | 18.2% |
| 93 | ss1 | +0.0058 | 17.6% |
| 94 | ss1 | +0.0052 | 15.7% |
| 97 | ss1 | +0.0041 | 12.4% |
| 208 | ss2 | +0.0040 | 12.1% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -114 | 4 | 19.0% |
| -113 | 2 | 9.5% |
| +114 | 2 | 9.5% |
| -112 | 2 | 9.5% |
| +113 | 1 | 4.8% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 42.9% |
| ss2 | ss1 | 5 | 23.8% |
| ss1 | flkL | 3 | 14.3% |
| ss1 | other | 3 | 14.3% |
| other | ss1 | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 94 | ss1 | 207 | ss2 | +0.0040 | 0.0453 |
| 207 | ss2 | 94 | ss1 | +0.0036 | 0.0507 |
| 93 | ss1 | 207 | ss2 | +0.0032 | 0.0701 |
| 208 | ss2 | 94 | ss1 | +0.0029 | 0.1294 |
| 95 | ss1 | 209 | ss2 | +0.0019 | 0.0191 |

### L26 H16 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 21  |  total attr: +0.0432

**Key mass** (top-1=17%, top-2=34%, top-3=49%)  [DISTR(V205/N208/R207/Q206/G204)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 205 | other | +0.0075 | 17.3% |
| 208 | ss2 | +0.0072 | 16.6% |
| 207 | ss2 | +0.0066 | 15.4% |
| 206 | ss2 | +0.0061 | 14.1% |
| 204 | other | +0.0052 | 12.0% |

**Query mass** (top-1=36%, top-2=68%, top-3=79%)  [DISTR(T95/T93/Q206)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0157 | 36.3% |
| 93 | ss1 | +0.0135 | 31.3% |
| 206 | ss2 | +0.0050 | 11.5% |
| 94 | ss1 | +0.0034 | 7.8% |
| 97 | ss1 | +0.0024 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 3 | 14.3% |
| -112 | 3 | 14.3% |
| -114 | 3 | 14.3% |
| +0 | 3 | 14.3% |
| +1 | 2 | 9.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 42.9% |
| ss1 | other | 4 | 19.0% |
| ss2 | other | 2 | 9.5% |
| ss2 | ss2 | 2 | 9.5% |
| ss1 | flkR | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 95 | ss1 | 208 | ss2 | +0.0059 | 0.0352 |
| 93 | ss1 | 205 | other | +0.0040 | 0.0824 |
| 93 | ss1 | 206 | ss2 | +0.0037 | 0.0651 |
| 94 | ss1 | 207 | ss2 | +0.0034 | 0.0583 |
| 93 | ss1 | 207 | ss2 | +0.0033 | 0.0532 |

### L27 H15 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 17  |  total attr: +0.0339

**Key mass** (top-1=27%, top-2=47%, top-3=66%)  [DISTR(T95/V209/R94/I96)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0092 | 27.0% |
| 209 | ss2 | +0.0069 | 20.4% |
| 94 | ss1 | +0.0063 | 18.5% |
| 96 | ss1 | +0.0029 | 8.5% |
| 234 | flkR | +0.0020 | 5.8% |

**Query mass** (top-1=26%, top-2=50%, top-3=73%)  [DISTR(T95/N208/Q206)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0089 | 26.2% |
| 208 | ss2 | +0.0080 | 23.5% |
| 206 | ss2 | +0.0077 | 22.8% |
| 209 | ss2 | +0.0019 | 5.6% |
| 207 | ss2 | +0.0017 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 11.8% |
| -112 | 2 | 11.8% |
| +113 | 2 | 11.8% |
| +112 | 2 | 11.8% |
| +111 | 1 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 41.2% |
| ss1 | ss2 | 4 | 23.5% |
| ss1 | other | 2 | 11.8% |
| ss2 | ss2 | 2 | 11.8% |
| ss2 | flkR | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 206 | ss2 | 95 | ss1 | +0.0077 | 0.0714 |
| 208 | ss2 | 94 | ss1 | +0.0053 | 0.2768 |
| 95 | ss1 | 209 | ss2 | +0.0045 | 0.0255 |
| 208 | ss2 | 234 | flkR | +0.0020 | 0.0847 |
| 95 | ss1 | 96 | ss1 | +0.0019 | 0.0264 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.0812

**Key mass** (top-1=47%, top-2=55%, top-3=62%)  [DISTR(T93/N208/R94/V209/T95)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | ss1 | +0.0379 | 46.7% |
| 208 | ss2 | +0.0067 | 8.2% |
| 94 | ss1 | +0.0061 | 7.5% |
| 209 | ss2 | +0.0046 | 5.7% |
| 95 | ss1 | +0.0046 | 5.7% |

**Query mass** (top-1=20%, top-2=40%, top-3=52%)  [DISTR(V210/N208/T93/Q206/T95)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 210 | ss2 | +0.0166 | 20.5% |
| 208 | ss2 | +0.0159 | 19.6% |
| 93 | ss1 | +0.0098 | 12.1% |
| 206 | ss2 | +0.0093 | 11.5% |
| 95 | ss1 | +0.0092 | 11.4% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +115 | 3 | 10.7% |
| +117 | 2 | 7.1% |
| +112 | 2 | 7.1% |
| +113 | 2 | 7.1% |
| -115 | 1 | 3.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 39.3% |
| ss1 | ss2 | 5 | 17.9% |
| ss1 | other | 5 | 17.9% |
| ss2 | flkL | 2 | 7.1% |
| flkL | flkR | 2 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 210 | ss2 | 93 | ss1 | +0.0157 | 0.3251 |
| 208 | ss2 | 93 | ss1 | +0.0132 | 0.3323 |
| 93 | ss1 | 208 | ss2 | +0.0067 | 0.0777 |
| 206 | ss2 | 95 | ss1 | +0.0046 | 0.0383 |
| 209 | ss2 | 97 | ss1 | +0.0036 | 0.0564 |

### L30 H1 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 4  |  total attr: +0.0647

**Key mass** (top-1=92%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0595 | 91.9% |
| 93 | ss1 | +0.0046 | 7.1% |
| -1 | other | +0.0007 | 1.0% |

**Query mass** (top-1=92%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | ss2 | +0.0595 | 91.9% |
| 210 | ss2 | +0.0039 | 6.0% |
| 208 | ss2 | +0.0007 | 1.1% |
| 95 | ss1 | +0.0007 | 1.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 1 | 25.0% |
| +117 | 1 | 25.0% |
| +115 | 1 | 25.0% |
| +96 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 75.0% |
| ss1 | other | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 209 | ss2 | 95 | ss1 | +0.0595 | 0.4890 |
| 210 | ss2 | 93 | ss1 | +0.0039 | 0.0551 |
| 208 | ss2 | 93 | ss1 | +0.0007 | 0.0150 |
| 95 | ss1 | -1 | other | +0.0007 | 0.0513 |

### L32 H13 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 21  |  total attr: +0.1282

**Key mass** (top-1=28%, top-2=45%, top-3=60%)  [DISTR(T95/Q206/R94/T93)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0364 | 28.4% |
| 206 | ss2 | +0.0209 | 16.3% |
| 94 | ss1 | +0.0190 | 14.8% |
| 93 | ss1 | +0.0156 | 12.2% |
| 210 | ss2 | +0.0092 | 7.2% |

**Query mass** (top-1=26%, top-2=43%, top-3=57%)  [DISTR(Q206/T95/R207/T93/N208)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | ss2 | +0.0331 | 25.8% |
| 95 | ss1 | +0.0221 | 17.3% |
| 207 | ss2 | +0.0180 | 14.1% |
| 93 | ss1 | +0.0129 | 10.0% |
| 208 | ss2 | +0.0112 | 8.8% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 3 | 14.3% |
| +114 | 2 | 9.5% |
| -114 | 2 | 9.5% |
| -116 | 2 | 9.5% |
| +112 | 2 | 9.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 11 | 52.4% |
| ss2 | ss1 | 10 | 47.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 206 | ss2 | 95 | ss1 | +0.0331 | 0.2123 |
| 95 | ss1 | 206 | ss2 | +0.0202 | 0.1295 |
| 207 | ss2 | 94 | ss1 | +0.0180 | 0.1588 |
| 208 | ss2 | 93 | ss1 | +0.0093 | 0.1422 |
| 93 | ss1 | 210 | ss2 | +0.0092 | 0.1056 |

### L32 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 16  |  total attr: +0.0883

**Key mass** (top-1=39%, top-2=68%, top-3=76%)  [DISTR(T93/V209/R207)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 93 | ss1 | +0.0346 | 39.1% |
| 209 | ss2 | +0.0255 | 28.9% |
| 207 | ss2 | +0.0071 | 8.0% |
| 210 | ss2 | +0.0042 | 4.7% |
| 206 | ss2 | +0.0033 | 3.8% |

**Query mass** (top-1=30%, top-2=54%, top-3=69%)  [DISTR(T95/N208/V210/R94)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 95 | ss1 | +0.0267 | 30.2% |
| 208 | ss2 | +0.0211 | 23.8% |
| 210 | ss2 | +0.0135 | 15.3% |
| 94 | ss1 | +0.0078 | 8.9% |
| 93 | ss1 | +0.0051 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -114 | 2 | 12.5% |
| -112 | 2 | 12.5% |
| +112 | 2 | 12.5% |
| +115 | 1 | 6.2% |
| +117 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 56.2% |
| ss2 | ss1 | 7 | 43.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 95 | ss1 | 209 | ss2 | +0.0233 | 0.0920 |
| 208 | ss2 | 93 | ss1 | +0.0211 | 0.1952 |
| 210 | ss2 | 93 | ss1 | +0.0135 | 0.0939 |
| 94 | ss1 | 207 | ss2 | +0.0071 | 0.0378 |
| 93 | ss1 | 210 | ss2 | +0.0042 | 0.0289 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #4 | L0 | H19 | 0 | +0.0000 | — |  | — |  |  |  |
| #19 | L5 | H18 | 9 | +0.0111 | SINGLE-ANCHOR | Y250 | DISTRIBUTED | V59/V209/G100/M211/V215 |  | ss2→flkR |
| #16 | L6 | H11 | 7 | +0.0167 | SINGLE-ANCHOR | V59 | SINGLE-ANCHOR | G100 |  | ss1→flkL |
| #30 | L6 | H17 | 30 | +0.0571 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL |  |
| #18 | L7 | H4 | 25 | +0.0850 | DUAL-ANCHOR | V210/V209 | SINGLE-ANCHOR | G100 |  | CROSS:ss1→ss2 |
| #12 | L8 | H0 | 68 | +0.1478 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #21 | L10 | H0 | 26 | +0.0900 | SINGLE-ANCHOR | G100 | DISTRIBUTED |  |  |  |
| #25 | L10 | H9 | 54 | +0.1350 | SINGLE-ANCHOR | G100 | DISTRIBUTED |  |  |  |
| #23 | L10 | H19 | 14 | +0.0430 | SINGLE-ANCHOR | G100 | DISTRIBUTED | D98/G101/V106/I97 |  | INTRA:ss1 |
| #24 | L11 | H16 | 46 | +0.1550 | SINGLE-ANCHOR | G100 | DISTRIBUTED |  |  |  |
| #29 | L12 | H3 | 20 | +0.0766 | SINGLE-ANCHOR | G100 | DISTRIBUTED |  |  | flkL→ss1 |
| #22 | L13 | H19 | 12 | +0.0720 | SINGLE-ANCHOR | V209 | SINGLE-ANCHOR | G100 |  | CROSS:ss1→ss2 |
| #14 | L14 | H13 | 15 | +0.1097 | SINGLE-ANCHOR | G100 | DISTRIBUTED | V106/I97/I96/T95 |  |  |
| #13 | L14 | H14 | 14 | +0.0574 | SINGLE-ANCHOR | G100 | DUAL-ANCHOR | V106/I97 |  | INTRA:ss1 |
| #9 | L14 | H15 | 3 | +0.0882 | SINGLE-ANCHOR | G100 | DUAL-ANCHOR | I97/I96 |  | INTRA:ss1 |
| #11 | L15 | H3 | 10 | +0.0509 | SINGLE-ANCHOR | G100 | DISTRIBUTED | V106/I96/I97/G100 |  | INTRA:ss1 |
| #10 | L16 | H7 | 34 | +0.0829 | SINGLE-ANCHOR | G100 | DISTRIBUTED |  |  |  |
| #7 | L16 | H9 | 21 | +0.0939 | DUAL-ANCHOR | G100/V106 | DISTRIBUTED | I97/G100/V106 |  |  |
| #1 | L17 | H1 | 49 | +0.3501 | SINGLE-ANCHOR | V106 | DISTRIBUTED | I97/T93/I96 |  |  |
| #28 | L17 | H16 | 19 | +0.0478 | DISTRIBUTED | V106/I97/G100/K105/L107 | DISTRIBUTED | V106/I97/I96 | POSITIONAL |  |
| #8 | L18 | H5 | 21 | +0.0847 | SINGLE-ANCHOR | V106 | DISTRIBUTED | G100/I97/T93 | POSITIONAL | INTRA:ss1 |
| #27 | L19 | H15 | 43 | +0.0858 | DISTRIBUTED | G100/V106/G213 | DISTRIBUTED |  |  |  |
| #20 | L20 | H0 | 29 | +0.0795 | DUAL-ANCHOR | G100/V106 | DISTRIBUTED | T95/I97/T93/R94/I96 |  |  |
| #26 | L22 | H14 | 21 | +0.0330 | DISTRIBUTED | R207/R94/H82/V209 | DISTRIBUTED | T95/T93/R94/I97/N208 |  | CROSS:ss1→ss2 |
| #17 | L26 | H16 | 21 | +0.0432 | DISTRIBUTED | V205/N208/R207/Q206/G204 | DISTRIBUTED | T95/T93/Q206 |  | CROSS:ss1→ss2 |
| #15 | L27 | H15 | 17 | +0.0339 | DISTRIBUTED | T95/V209/R94/I96 | DISTRIBUTED | T95/N208/Q206 |  | CROSS:ss2→ss1 |
| #6 | L29 | H18 | 28 | +0.0812 | DISTRIBUTED | T93/N208/R94/V209/T95 | DISTRIBUTED | V210/N208/T93/Q206/T95 |  |  |
| #5 | L30 | H1 | 4 | +0.0647 | SINGLE-ANCHOR | T95 | SINGLE-ANCHOR | V209 | CROSS_SSE | CROSS:ss2→ss1 |
| #2 | L32 | H13 | 21 | +0.1282 | DISTRIBUTED | T95/Q206/R94/T93 | DISTRIBUTED | Q206/T95/R207/T93/N208 |  | CROSS:ss1→ss2 |
| #3 | L32 | H18 | 16 | +0.0883 | DISTRIBUTED | T93/V209/R207 | DISTRIBUTED | T95/N208/V210/R94 |  | CROSS:ss1→ss2 |
