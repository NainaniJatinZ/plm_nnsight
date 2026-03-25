# Contact Pattern Analysis: 3HO7A

Generated: 2026-03-22 21:25:08   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3HO7A |
| Contact pair | (76, 189) |
| ss1 | [71, 82) |
| ss2 | [184, 195) |
| Clean flank | 43 |
| Corrupt flank | 42 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.8569 |
| Corrupt metric | 0.3557 |
| Gap | 0.5012 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 110 | 70.52% |
| positive IE | 60 | 76.16% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H18 | +0.3004 |
| 2 | L32 | H13 | +0.1685 |
| 3 | L27 | H15 | +0.0899 |
| 4 | L29 | H18 | +0.0828 |
| 5 | L12 | H2 | +0.0547 |
| 6 | L0 | H19 | +0.0520 |
| 7 | L31 | H17 | +0.0470 |
| 8 | L13 | H10 | +0.0435 |
| 9 | L30 | H19 | +0.0425 |
| 10 | L11 | H16 | +0.0405 |
| 11 | L21 | H2 | +0.0387 |
| 12 | L13 | H18 | +0.0298 |
| 13 | L30 | H12 | +0.0285 |
| 14 | L21 | H4 | +0.0238 |
| 15 | L31 | H10 | +0.0210 |
| 16 | L30 | H4 | +0.0184 |
| 17 | L30 | H0 | +0.0182 |
| 18 | L14 | H16 | +0.0181 |
| 19 | L15 | H6 | +0.0179 |
| 20 | L18 | H4 | +0.0164 |
| 21 | L30 | H13 | +0.0161 |
| 22 | L8 | H7 | +0.0158 |
| 23 | L14 | H17 | +0.0152 |
| 24 | L10 | H9 | +0.0148 |
| 25 | L15 | H12 | +0.0148 |
| 26 | L20 | H8 | +0.0134 |
| 27 | L15 | H19 | +0.0130 |
| 28 | L14 | H9 | +0.0128 |
| 29 | L22 | H16 | +0.0122 |
| 30 | L18 | H14 | +0.0118 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 1.18% |
| 2 | 2.25% |
| 3 | 2.97% |
| 4 | 4.64% |
| 5 | 6.00% |
| 6 | 14.08% |
| 7 | 15.01% |
| 8 | 16.23% |
| 9 | 16.98% |
| 10 | 20.57% |
| 20 | 23.54% |
| 80 | 96.03% |
| 450 | 129.31% |

## Cell Attribution Analysis

Total cells: 3,120,588

- Positive: 1,553,948
- Negative: 1,564,780

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000037 | 312,059 |
| 95th | +0.00000122 | 156,030 |
| 99th | +0.00001029 | 31,206 |
| 99.5th | +0.00002280 | 15,604 |
| 99.9th | +0.00012307 | 3,121 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L21 | H2 | 79 | ss1 | 86 | other | +0.047949 | 0.349086 |
| L11 | H16 | 86 | other | 32 | flkL | +0.032062 | 0.232287 |
| L13 | H10 | 86 | other | 63 | flkL | +0.029942 | 0.192309 |
| L16 | H17 | 86 | other | 61 | flkL | +0.023247 | 0.090227 |
| L32 | H13 | 192 | ss2 | 77 | ss1 | +0.022647 | 0.282321 |
| L9 | H3 | 32 | flkL | 17 | other | +0.021681 | 0.200604 |
| L32 | H13 | 187 | ss2 | 78 | ss1 | +0.021286 | 0.178580 |
| L30 | H19 | 78 | ss1 | 81 | ss1 | +0.021245 | 0.392601 |
| L12 | H2 | -1 | other | 17 | other | +0.020882 | 0.340003 |
| L13 | H18 | -1 | other | 63 | flkL | +0.020780 | 0.230170 |
| L8 | H7 | 63 | flkL | 32 | flkL | +0.017326 | 0.133241 |
| L32 | H18 | 190 | ss2 | 79 | ss1 | +0.017143 | 0.099262 |
| L21 | H4 | 76 | ss1 | 86 | other | +0.017053 | 0.157798 |
| L27 | H15 | 77 | ss1 | 190 | ss2 | +0.016873 | 0.203387 |
| L15 | H15 | -1 | other | 17 | other | +0.015529 | 0.192157 |
| L32 | H18 | 187 | ss2 | 78 | ss1 | +0.014836 | 0.075718 |
| L32 | H13 | 78 | ss1 | 187 | ss2 | +0.013847 | 0.116168 |
| L12 | H2 | 86 | other | 32 | flkL | +0.013042 | 0.097646 |
| L32 | H18 | 79 | ss1 | 190 | ss2 | +0.012283 | 0.071123 |
| L22 | H16 | 79 | ss1 | 76 | ss1 | +0.011953 | 0.211536 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L21 | H2 | 81 | ss1 | 86 | other | -0.004196 | 0.339268 |
| L29 | H18 | 187 | ss2 | 67 | flkL | -0.004322 | 0.046295 |
| L11 | H16 | 84 | other | 32 | flkL | -0.004489 | 0.197941 |
| L13 | H10 | 88 | other | 63 | flkL | -0.004492 | 0.122229 |
| L9 | H3 | 32 | flkL | 21 | other | -0.004515 | 0.060537 |
| L11 | H16 | 88 | other | 32 | flkL | -0.004871 | 0.209532 |
| L11 | H16 | 201 | flkR | 32 | flkL | -0.004912 | 0.131674 |
| L29 | H18 | 79 | ss1 | 202 | flkR | -0.005456 | 0.071226 |
| L31 | H17 | 187 | ss2 | -1 | other | -0.005459 | 0.118799 |
| L14 | H16 | 78 | ss1 | 17 | other | -0.005784 | 0.140097 |
| L10 | H9 | 63 | flkL | 17 | other | -0.006453 | 0.201852 |
| L14 | H16 | 76 | ss1 | 17 | other | -0.007087 | 0.110545 |
| L14 | H16 | 79 | ss1 | 17 | other | -0.007272 | 0.113479 |
| L14 | H16 | 63 | flkL | 17 | other | -0.007290 | 0.231871 |
| L22 | H16 | 76 | ss1 | 86 | other | -0.007708 | 0.210618 |
| L15 | H12 | 86 | other | 86 | other | -0.007860 | 0.042169 |
| L21 | H2 | 80 | ss1 | 86 | other | -0.008738 | 0.331155 |
| L27 | H15 | 77 | ss1 | 192 | ss2 | -0.009265 | 0.105636 |
| L21 | H2 | 78 | ss1 | 86 | other | -0.013338 | 0.330369 |
| L13 | H18 | 86 | other | 63 | flkL | -0.020020 | 0.121732 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.3557 | 0.00% |
| 10 | 10 | 9 | 0.3559 | 0.03% |
| 20 | 20 | 15 | 0.3585 | 0.56% |
| 50 | 50 | 27 | 0.3639 | 1.63% |
| 100 | 100 | 36 | 0.3678 | 2.40% |
| 200 | 200 | 47 | 0.3787 | 4.59% |
| 500 | 500 | 55 | 0.4063 | 10.09% |
| 1000 | 1,000 | 59 | 0.4564 | 20.08% |
| 2000 | 2,000 | 60 | 0.5020 | 29.18% |
| 5000 | 5,000 | 60 | 0.5749 | 43.72% |
| 10000 | 10,000 | 60 | 0.6221 | 53.14% |
| 20000 | 20,000 | 60 | 0.6733 | 63.36% |
| 50000 | 50,000 | 60 | 0.7199 | 72.65% |

## Motif Analysis

### L0 H19 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.0041

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 28 | flkL | +0.0041 | 100.0% |

**Query mass** (top-1=66%, top-2=84%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 43 | flkL | +0.0027 | 65.7% |
| -1 | other | +0.0008 | 18.2% |
| 192 | ss2 | +0.0007 | 16.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +15 | 1 | 33.3% |
| -29 | 1 | 33.3% |
| +164 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 1 | 33.3% |
| other | flkL | 1 | 33.3% |
| ss2 | flkL | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 43 | flkL | 28 | flkL | +0.0027 | 0.0610 |
| -1 | other | 28 | flkL | +0.0008 | 0.0050 |
| 192 | ss2 | 28 | flkL | +0.0007 | 0.0227 |

### L8 H7 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0194

**Key mass** (top-1=89%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0173 | 89.4% |
| 28 | flkL | +0.0021 | 10.6% |

**Query mass** (top-1=89%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0173 | 89.4% |
| 86 | other | +0.0013 | 6.8% |
| 85 | other | +0.0004 | 1.9% |
| 190 | ss2 | +0.0004 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +31 | 1 | 25.0% |
| +58 | 1 | 25.0% |
| +57 | 1 | 25.0% |
| +162 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 2 | 50.0% |
| flkL | flkL | 1 | 25.0% |
| ss2 | flkL | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | flkL | 32 | flkL | +0.0173 | 0.1332 |
| 86 | other | 28 | flkL | +0.0013 | 0.0338 |
| 85 | other | 28 | flkL | +0.0004 | 0.0500 |
| 190 | ss2 | 28 | flkL | +0.0004 | 0.0124 |

### L10 H9 — Rank #24

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0290

**Key mass** (top-1=51%, top-2=88%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0149 | 51.3% |
| 17 | other | +0.0106 | 36.7% |
| 18 | other | +0.0023 | 8.1% |
| 20 | other | +0.0007 | 2.5% |
| 64 | flkL | +0.0004 | 1.4% |

**Query mass** (top-1=26%, top-2=45%, top-3=62%)  [DISTR(G86/W32/A63/L190)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0074 | 25.6% |
| 32 | flkL | +0.0056 | 19.4% |
| 63 | flkL | +0.0050 | 17.2% |
| 190 | ss2 | +0.0023 | 8.0% |
| 187 | ss2 | +0.0016 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +69 | 1 | 4.2% |
| +0 | 1 | 4.2% |
| -31 | 1 | 4.2% |
| +23 | 1 | 4.2% |
| +127 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 29.2% |
| flkL | other | 4 | 16.7% |
| other | other | 3 | 12.5% |
| ss2 | other | 3 | 12.5% |
| ss2 | flkL | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 86 | other | 17 | other | +0.0039 | 0.0402 |
| 63 | flkL | 63 | flkL | +0.0038 | 0.0621 |
| 32 | flkL | 63 | flkL | +0.0035 | 0.0753 |
| 86 | other | 63 | flkL | +0.0020 | 0.0268 |
| 190 | ss2 | 63 | flkL | +0.0016 | 0.0163 |

### L11 H16 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 46  |  total attr: +0.0911

**Key mass** (top-1=78%, top-2=87%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0709 | 77.8% |
| -1 | other | +0.0085 | 9.3% |
| 36 | flkL | +0.0039 | 4.3% |
| 31 | flkL | +0.0034 | 3.8% |
| 63 | flkL | +0.0033 | 3.6% |

**Query mass** (top-1=41%, top-2=53%, top-3=59%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0374 | 41.1% |
| 190 | ss2 | +0.0112 | 12.3% |
| 192 | ss2 | +0.0054 | 6.0% |
| 232 | flkR | +0.0039 | 4.3% |
| -1 | other | +0.0031 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +154 | 2 | 4.3% |
| +164 | 2 | 4.3% |
| +155 | 2 | 4.3% |
| +156 | 2 | 4.3% |
| +54 | 1 | 2.2% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 9 | 19.6% |
| ss2 | flkL | 9 | 19.6% |
| flkR | flkL | 8 | 17.4% |
| flkR | other | 5 | 10.9% |
| flkL | flkL | 4 | 8.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 86 | other | 32 | flkL | +0.0321 | 0.2323 |
| 190 | ss2 | 32 | flkL | +0.0099 | 0.1484 |
| 192 | ss2 | 32 | flkL | +0.0047 | 0.0996 |
| 232 | flkR | 32 | flkL | +0.0039 | 0.1706 |
| -1 | other | 63 | flkL | +0.0025 | 0.0626 |

### L12 H2 — Rank #5

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 30  |  total attr: +0.0695

**Key mass** (top-1=51%, top-2=91%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | other | +0.0358 | 51.4% |
| 32 | flkL | +0.0273 | 39.3% |
| 63 | flkL | +0.0032 | 4.7% |
| 18 | other | +0.0010 | 1.4% |
| 28 | flkL | +0.0008 | 1.1% |

**Query mass** (top-1=30%, top-2=52%, top-3=64%)  [DISTR(?-1/G86/L205/A63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0209 | 30.0% |
| 86 | other | +0.0153 | 22.0% |
| 205 | flkR | +0.0083 | 11.9% |
| 63 | flkL | +0.0058 | 8.4% |
| 201 | flkR | +0.0028 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +180 | 2 | 6.7% |
| -18 | 1 | 3.3% |
| +54 | 1 | 3.3% |
| +188 | 1 | 3.3% |
| +31 | 1 | 3.3% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 7 | 23.3% |
| flkL | flkL | 5 | 16.7% |
| other | flkL | 4 | 13.3% |
| ss1 | flkL | 4 | 13.3% |
| flkR | flkL | 3 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 17 | other | +0.0209 | 0.3400 |
| 86 | other | 32 | flkL | +0.0130 | 0.0976 |
| 205 | flkR | 17 | other | +0.0063 | 0.1018 |
| 63 | flkL | 32 | flkL | +0.0058 | 0.2338 |
| 201 | flkR | 17 | other | +0.0028 | 0.0606 |

### L13 H10 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0561

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0543 | 96.8% |
| 18 | other | +0.0013 | 2.3% |
| 17 | other | +0.0005 | 0.9% |

**Query mass** (top-1=53%, top-2=61%, top-3=67%)  [DISTR(G86/L78/L209/A63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0299 | 53.3% |
| 78 | ss1 | +0.0043 | 7.7% |
| 209 | flkR | +0.0033 | 5.9% |
| 63 | flkL | +0.0029 | 5.1% |
| 81 | ss1 | +0.0021 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 9.5% |
| +23 | 1 | 4.8% |
| +15 | 1 | 4.8% |
| +146 | 1 | 4.8% |
| +18 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 28.6% |
| flkR | flkL | 4 | 19.0% |
| flkL | flkL | 4 | 19.0% |
| other | flkL | 3 | 14.3% |
| other | other | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 86 | other | 63 | flkL | +0.0299 | 0.1923 |
| 78 | ss1 | 63 | flkL | +0.0043 | 0.1538 |
| 209 | flkR | 63 | flkL | +0.0033 | 0.0477 |
| 63 | flkL | 63 | flkL | +0.0029 | 0.1150 |
| 81 | ss1 | 63 | flkL | +0.0021 | 0.2405 |

### L13 H18 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 37  |  total attr: +0.0797

**Key mass** (top-1=89%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0708 | 88.8% |
| 17 | other | +0.0086 | 10.8% |
| 16 | other | +0.0004 | 0.5% |

**Query mass** (top-1=26%, top-2=36%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0208 | 26.1% |
| 86 | other | +0.0079 | 9.9% |
| 232 | flkR | +0.0049 | 6.2% |
| 78 | ss1 | +0.0043 | 5.4% |
| 205 | flkR | +0.0031 | 3.9% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -64 | 1 | 2.7% |
| +69 | 1 | 2.7% |
| +169 | 1 | 2.7% |
| +15 | 1 | 2.7% |
| +142 | 1 | 2.7% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 11 | 29.7% |
| other | flkL | 9 | 24.3% |
| ss1 | flkL | 7 | 18.9% |
| flkR | flkL | 5 | 13.5% |
| other | other | 2 | 5.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 63 | flkL | +0.0208 | 0.2302 |
| 86 | other | 17 | other | +0.0075 | 0.0532 |
| 232 | flkR | 63 | flkL | +0.0049 | 0.0979 |
| 78 | ss1 | 63 | flkL | +0.0043 | 0.1501 |
| 205 | flkR | 63 | flkL | +0.0031 | 0.0334 |

### L14 H9 — Rank #28

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0291

**Key mass** (top-1=57%, top-2=69%, top-3=79%)  [DISTR(A63/?-1/W32)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0165 | 56.9% |
| -1 | other | +0.0035 | 12.1% |
| 32 | flkL | +0.0029 | 9.8% |
| 0 | other | +0.0019 | 6.7% |
| 190 | ss2 | +0.0018 | 6.4% |

**Query mass** (top-1=54%, top-2=64%, top-3=70%)  [DISTR(?-1/W32/L190/P93)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0158 | 54.5% |
| 32 | flkL | +0.0027 | 9.4% |
| 190 | ss2 | +0.0017 | 5.8% |
| 93 | other | +0.0013 | 4.5% |
| 209 | flkR | +0.0013 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 10.0% |
| +31 | 2 | 10.0% |
| -64 | 1 | 5.0% |
| -31 | 1 | 5.0% |
| -1 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 7 | 35.0% |
| other | other | 2 | 10.0% |
| flkL | flkL | 2 | 10.0% |
| ss1 | flkL | 2 | 10.0% |
| ss2 | flkL | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 63 | flkL | +0.0099 | 0.2788 |
| -1 | other | -1 | other | +0.0035 | 0.1006 |
| 32 | flkL | 63 | flkL | +0.0021 | 0.0551 |
| -1 | other | 0 | other | +0.0019 | 0.1241 |
| 93 | other | 63 | flkL | +0.0013 | 0.1271 |

### L14 H16 — Rank #18

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 72  |  total attr: +0.0960

**Key mass** (top-1=46%, top-2=76%, top-3=83%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | other | +0.0439 | 45.8% |
| 18 | other | +0.0290 | 30.2% |
| 63 | flkL | +0.0069 | 7.2% |
| -1 | other | +0.0019 | 2.0% |
| 32 | flkL | +0.0018 | 1.8% |

**Query mass** (top-1=19%, top-2=25%, top-3=30%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0186 | 19.3% |
| 79 | ss1 | +0.0051 | 5.3% |
| 190 | ss2 | +0.0050 | 5.2% |
| 76 | ss1 | +0.0047 | 4.9% |
| 78 | ss1 | +0.0045 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +68 | 2 | 2.8% |
| +60 | 2 | 2.8% |
| +58 | 2 | 2.8% |
| +45 | 2 | 2.8% |
| +71 | 2 | 2.8% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 22 | 30.6% |
| other | other | 15 | 20.8% |
| ss1 | other | 9 | 12.5% |
| other | flkL | 7 | 9.7% |
| ss2 | flkL | 5 | 6.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 86 | other | 18 | other | +0.0085 | 0.0305 |
| 79 | ss1 | 18 | other | +0.0051 | 0.0942 |
| 78 | ss1 | 18 | other | +0.0045 | 0.0962 |
| 76 | ss1 | 18 | other | +0.0043 | 0.0946 |
| 63 | flkL | 18 | other | +0.0040 | 0.1559 |

### L14 H17 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS:flkR→flkL  |  cells: 4  |  total attr: +0.0019

**Key mass** (top-1=57%, top-2=80%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0011 | 56.9% |
| 232 | flkR | +0.0005 | 23.5% |
| 43 | flkL | +0.0004 | 19.6% |

**Query mass** (top-1=42%, top-2=77%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | flkR | +0.0008 | 41.9% |
| 89 | other | +0.0007 | 34.6% |
| 205 | flkR | +0.0005 | 23.5% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 1 | 25.0% |
| -27 | 1 | 25.0% |
| +200 | 1 | 25.0% |
| +189 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:flkR→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 2 | 50.0% |
| other | flkL | 1 | 25.0% |
| flkR | flkR | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 89 | other | 32 | flkL | +0.0007 | 0.0190 |
| 205 | flkR | 232 | flkR | +0.0005 | 0.0392 |
| 232 | flkR | 32 | flkL | +0.0004 | 0.0289 |
| 232 | flkR | 43 | flkL | +0.0004 | 0.0178 |

### L15 H6 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 30  |  total attr: +0.0360

**Key mass** (top-1=72%, top-2=82%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0261 | 72.4% |
| 17 | other | +0.0035 | 9.7% |
| 191 | ss2 | +0.0020 | 5.7% |
| 43 | flkL | +0.0014 | 3.9% |
| 28 | flkL | +0.0008 | 2.1% |

**Query mass** (top-1=15%, top-2=29%, top-3=35%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | ss1 | +0.0053 | 14.8% |
| 86 | other | +0.0049 | 13.7% |
| 89 | other | +0.0024 | 6.7% |
| 191 | ss2 | +0.0023 | 6.3% |
| 68 | flkL | +0.0021 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +13 | 2 | 6.7% |
| +15 | 2 | 6.7% |
| +7 | 2 | 6.7% |
| +23 | 1 | 3.3% |
| +26 | 1 | 3.3% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 26.7% |
| ss1 | flkL | 5 | 16.7% |
| flkL | flkL | 5 | 16.7% |
| ss2 | flkL | 3 | 10.0% |
| flkL | other | 3 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 76 | ss1 | 63 | flkL | +0.0053 | 0.1458 |
| 86 | other | 63 | flkL | +0.0049 | 0.1190 |
| 89 | other | 63 | flkL | +0.0024 | 0.1026 |
| 191 | ss2 | 63 | flkL | +0.0023 | 0.0665 |
| 87 | other | 63 | flkL | +0.0018 | 0.1246 |

### L15 H12 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 34  |  total attr: +0.0435

**Key mass** (top-1=55%, top-2=64%, top-3=70%)  [DISTR(A63/G86/R90/W32)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0239 | 54.9% |
| 86 | other | +0.0038 | 8.8% |
| 90 | other | +0.0027 | 6.1% |
| 32 | flkL | +0.0022 | 5.0% |
| 190 | ss2 | +0.0021 | 4.7% |

**Query mass** (top-1=24%, top-2=45%, top-3=55%)  [DISTR(G86/A63/Y87/S89/V88)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0106 | 24.4% |
| 63 | flkL | +0.0092 | 21.1% |
| 87 | other | +0.0041 | 9.4% |
| 89 | other | +0.0037 | 8.6% |
| 88 | other | +0.0033 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 14.7% |
| -1 | 5 | 14.7% |
| -3 | 3 | 8.8% |
| -2 | 3 | 8.8% |
| +15 | 3 | 8.8% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 19 | 55.9% |
| flkL | flkL | 4 | 11.8% |
| other | flkL | 3 | 8.8% |
| ss1 | flkL | 3 | 8.8% |
| ss2 | ss2 | 2 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 86 | other | 63 | flkL | +0.0093 | 0.0957 |
| 63 | flkL | 63 | flkL | +0.0085 | 0.1616 |
| 79 | ss1 | 63 | flkL | +0.0028 | 0.0766 |
| 32 | flkL | 32 | flkL | +0.0022 | 0.0586 |
| 190 | ss2 | 190 | ss2 | +0.0016 | 0.0154 |

### L15 H19 — Rank #27

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0091

**Key mass** (top-1=44%, top-2=70%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | other | +0.0040 | 43.8% |
| 0 | other | +0.0024 | 26.6% |
| 232 | flkR | +0.0015 | 16.3% |
| 41 | flkL | +0.0006 | 6.8% |
| 18 | other | +0.0006 | 6.5% |

**Query mass** (top-1=34%, top-2=56%, top-3=69%)  [DISTR(?-1/L209/A63/G86)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0031 | 34.0% |
| 209 | flkR | +0.0020 | 21.7% |
| 63 | flkL | +0.0013 | 13.7% |
| 86 | other | +0.0009 | 10.0% |
| 190 | ss2 | +0.0007 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -18 | 1 | 10.0% |
| +209 | 1 | 10.0% |
| -146 | 1 | 10.0% |
| +46 | 1 | 10.0% |
| +190 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 2 | 20.0% |
| flkR | other | 2 | 20.0% |
| flkL | other | 2 | 20.0% |
| other | flkR | 1 | 10.0% |
| ss2 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 17 | other | +0.0025 | 0.0524 |
| 209 | flkR | 0 | other | +0.0014 | 0.0345 |
| 86 | other | 232 | flkR | +0.0009 | 0.0609 |
| 63 | flkL | 17 | other | +0.0009 | 0.0288 |
| 190 | ss2 | 0 | other | +0.0007 | 0.0209 |

### L18 H4 — Rank #20

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.0138

**Key mass** (top-1=18%, top-2=34%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 43 | flkL | +0.0024 | 17.5% |
| 86 | other | +0.0023 | 16.8% |
| 190 | ss2 | +0.0017 | 12.6% |
| 87 | other | +0.0011 | 8.1% |
| 63 | flkL | +0.0011 | 8.0% |

**Query mass** (top-1=73%, top-2=88%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0100 | 72.5% |
| 190 | ss2 | +0.0021 | 15.6% |
| 205 | flkR | +0.0005 | 3.3% |
| 77 | ss1 | +0.0004 | 3.1% |
| 37 | flkL | +0.0004 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 12.5% |
| +43 | 1 | 6.2% |
| -1 | 1 | 6.2% |
| -2 | 1 | 6.2% |
| -42 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 6 | 37.5% |
| other | flkL | 4 | 25.0% |
| flkR | ss2 | 2 | 12.5% |
| ss2 | ss2 | 1 | 6.2% |
| ss2 | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 86 | other | 43 | flkL | +0.0024 | 0.0163 |
| 86 | other | 86 | other | +0.0023 | 0.0253 |
| 190 | ss2 | 190 | ss2 | +0.0014 | 0.0252 |
| 86 | other | 87 | other | +0.0011 | 0.0091 |
| 86 | other | 88 | other | +0.0009 | 0.0070 |

### L18 H14 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 34  |  total attr: +0.0317

**Key mass** (top-1=38%, top-2=68%, top-3=77%)  [DISTR(L17/?232/E59)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | other | +0.0119 | 37.7% |
| 232 | flkR | +0.0097 | 30.7% |
| 59 | flkL | +0.0028 | 8.8% |
| -1 | other | +0.0019 | 6.1% |
| 57 | flkL | +0.0014 | 4.5% |

**Query mass** (top-1=19%, top-2=37%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | ss2 | +0.0061 | 19.3% |
| 76 | ss1 | +0.0056 | 17.6% |
| 86 | other | +0.0027 | 8.6% |
| 78 | ss1 | +0.0025 | 7.9% |
| 209 | flkR | +0.0024 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +173 | 1 | 2.9% |
| +69 | 1 | 2.9% |
| -156 | 1 | 2.9% |
| +63 | 1 | 2.9% |
| +158 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=15%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 5 | 14.7% |
| ss2 | flkR | 5 | 14.7% |
| ss1 | flkL | 5 | 14.7% |
| ss1 | other | 4 | 11.8% |
| ss2 | other | 3 | 8.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 190 | ss2 | 17 | other | +0.0056 | 0.1275 |
| 86 | other | 17 | other | +0.0027 | 0.0975 |
| 76 | ss1 | 232 | flkR | +0.0024 | 0.1345 |
| 80 | ss1 | 17 | other | +0.0019 | 0.0891 |
| 209 | flkR | 51 | flkL | +0.0014 | 0.0362 |

### L20 H8 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.0271

**Key mass** (top-1=83%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0224 | 82.7% |
| 32 | flkL | +0.0038 | 14.1% |
| 232 | flkR | +0.0009 | 3.2% |

**Query mass** (top-1=15%, top-2=30%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0040 | 14.8% |
| 77 | ss1 | +0.0040 | 14.8% |
| 186 | ss2 | +0.0038 | 14.0% |
| 86 | other | +0.0022 | 8.0% |
| 198 | flkR | +0.0017 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +78 | 1 | 4.5% |
| +187 | 1 | 4.5% |
| +194 | 1 | 4.5% |
| +54 | 1 | 4.5% |
| +79 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 6 | 27.3% |
| ss2 | other | 4 | 18.2% |
| ss1 | other | 3 | 13.6% |
| other | other | 2 | 9.1% |
| ss2 | flkL | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 77 | ss1 | -1 | other | +0.0040 | 0.2159 |
| 186 | ss2 | -1 | other | +0.0038 | 0.2668 |
| 193 | ss2 | -1 | other | +0.0035 | 0.2383 |
| 86 | other | 32 | flkL | +0.0022 | 0.1630 |
| 78 | ss1 | -1 | other | +0.0015 | 0.2080 |

### L21 H2 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 18  |  total attr: +0.0674

**Key mass** (top-1=87%, top-2=94%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0585 | 86.8% |
| 205 | flkR | +0.0049 | 7.2% |
| 70 | flkL | +0.0014 | 2.0% |
| 47 | flkL | +0.0012 | 1.8% |
| 190 | ss2 | +0.0010 | 1.4% |

**Query mass** (top-1=73%, top-2=83%, top-3=87%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 79 | ss1 | +0.0491 | 72.8% |
| 76 | ss1 | +0.0070 | 10.4% |
| 75 | ss1 | +0.0024 | 3.5% |
| 212 | flkR | +0.0023 | 3.4% |
| 217 | flkR | +0.0014 | 2.1% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 3 | 16.7% |
| -7 | 2 | 11.1% |
| -10 | 1 | 5.6% |
| -11 | 1 | 5.6% |
| +12 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 5 | 27.8% |
| ss1 | other | 4 | 22.2% |
| ss1 | flkL | 4 | 22.2% |
| other | other | 3 | 16.7% |
| flkR | ss2 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 79 | ss1 | 86 | other | +0.0479 | 0.3491 |
| 76 | ss1 | 86 | other | +0.0055 | 0.3108 |
| 75 | ss1 | 86 | other | +0.0024 | 0.1742 |
| 212 | flkR | 205 | flkR | +0.0023 | 0.1490 |
| 217 | flkR | 205 | flkR | +0.0014 | 0.0823 |

### L21 H4 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0365

**Key mass** (top-1=72%, top-2=87%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 86 | other | +0.0263 | 72.2% |
| 205 | flkR | +0.0056 | 15.2% |
| 87 | other | +0.0014 | 3.8% |
| 209 | flkR | +0.0012 | 3.4% |
| 88 | other | +0.0011 | 3.0% |

**Query mass** (top-1=54%, top-2=68%, top-3=75%)  [DISTR(D76/L190/L78)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | ss1 | +0.0195 | 53.5% |
| 190 | ss2 | +0.0053 | 14.5% |
| 78 | ss1 | +0.0025 | 6.9% |
| 79 | ss1 | +0.0016 | 4.3% |
| 86 | other | +0.0013 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -12 | 3 | 18.8% |
| -11 | 2 | 12.5% |
| +0 | 2 | 12.5% |
| -10 | 1 | 6.2% |
| -15 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 8 | 50.0% |
| other | other | 3 | 18.8% |
| ss2 | flkR | 2 | 12.5% |
| flkR | flkR | 2 | 12.5% |
| ss2 | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 76 | ss1 | 86 | other | +0.0171 | 0.1578 |
| 190 | ss2 | 205 | flkR | +0.0044 | 0.0646 |
| 78 | ss1 | 86 | other | +0.0025 | 0.1058 |
| 79 | ss1 | 86 | other | +0.0016 | 0.0373 |
| 76 | ss1 | 87 | other | +0.0014 | 0.0500 |

### L22 H16 — Rank #29

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0287

**Key mass** (top-1=42%, top-2=60%, top-3=68%)  [DISTR(D76/G86/L74/L190)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | ss1 | +0.0120 | 41.7% |
| 86 | other | +0.0052 | 18.1% |
| 74 | ss1 | +0.0024 | 8.3% |
| 190 | ss2 | +0.0018 | 6.1% |
| 205 | flkR | +0.0016 | 5.4% |

**Query mass** (top-1=46%, top-2=59%, top-3=72%)  [DISTR(L79/E82/D76)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 79 | ss1 | +0.0132 | 46.1% |
| 82 | other | +0.0037 | 12.8% |
| 76 | ss1 | +0.0036 | 12.6% |
| 77 | ss1 | +0.0020 | 6.9% |
| 186 | ss2 | +0.0018 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 3 | 18.8% |
| -4 | 3 | 18.8% |
| +2 | 3 | 18.8% |
| -9 | 3 | 18.8% |
| +4 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 31.2% |
| ss1 | other | 5 | 31.2% |
| ss2 | ss2 | 2 | 12.5% |
| other | other | 1 | 6.2% |
| flkR | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 79 | ss1 | 76 | ss1 | +0.0120 | 0.2115 |
| 82 | other | 86 | other | +0.0026 | 0.3312 |
| 76 | ss1 | 74 | ss1 | +0.0024 | 0.0916 |
| 77 | ss1 | 86 | other | +0.0020 | 0.1156 |
| 186 | ss2 | 190 | ss2 | +0.0018 | 0.0663 |

### L27 H15 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 34  |  total attr: +0.0684

**Key mass** (top-1=26%, top-2=46%, top-3=55%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | ss2 | +0.0181 | 26.5% |
| 80 | ss1 | +0.0135 | 19.8% |
| 81 | ss1 | +0.0062 | 9.1% |
| 188 | ss2 | +0.0047 | 6.8% |
| 191 | ss2 | +0.0036 | 5.3% |

**Query mass** (top-1=26%, top-2=44%, top-3=57%)  [DISTR(D77/V188/R186/L78/Y80)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | ss1 | +0.0177 | 25.8% |
| 188 | ss2 | +0.0122 | 17.9% |
| 186 | ss2 | +0.0094 | 13.8% |
| 78 | ss1 | +0.0077 | 11.3% |
| 80 | ss1 | +0.0041 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 3 | 8.8% |
| +104 | 3 | 8.8% |
| -105 | 3 | 8.8% |
| -109 | 2 | 5.9% |
| +128 | 2 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 15 | 44.1% |
| ss2 | ss1 | 11 | 32.4% |
| ss2 | other | 2 | 5.9% |
| ss2 | flkL | 2 | 5.9% |
| ss1 | flkL | 1 | 2.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 77 | ss1 | 190 | ss2 | +0.0169 | 0.2034 |
| 188 | ss2 | 80 | ss1 | +0.0116 | 0.2430 |
| 186 | ss2 | 81 | ss1 | +0.0050 | 0.1062 |
| 78 | ss1 | 191 | ss2 | +0.0028 | 0.0479 |
| 80 | ss1 | 188 | ss2 | +0.0027 | 0.1219 |

### L29 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 45  |  total attr: +0.0738

**Key mass** (top-1=17%, top-2=27%, top-3=36%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 81 | ss1 | +0.0123 | 16.6% |
| 78 | ss1 | +0.0076 | 10.3% |
| 232 | flkR | +0.0064 | 8.7% |
| 187 | ss2 | +0.0063 | 8.5% |
| 74 | ss1 | +0.0054 | 7.3% |

**Query mass** (top-1=16%, top-2=30%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 189 | ss2 | +0.0117 | 15.8% |
| 187 | ss2 | +0.0107 | 14.5% |
| 78 | ss1 | +0.0094 | 12.7% |
| 81 | ss1 | +0.0071 | 9.7% |
| 77 | ss1 | +0.0060 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +111 | 2 | 4.4% |
| -115 | 2 | 4.4% |
| +106 | 1 | 2.2% |
| -106 | 1 | 2.2% |
| +119 | 1 | 2.2% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 9 | 20.0% |
| ss2 | ss1 | 8 | 17.8% |
| ss1 | ss2 | 6 | 13.3% |
| flkR | ss1 | 5 | 11.1% |
| ss1 | flkL | 5 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 187 | ss2 | 81 | ss1 | +0.0094 | 0.4643 |
| 189 | ss2 | 78 | ss1 | +0.0072 | 0.0827 |
| 81 | ss1 | 187 | ss2 | +0.0063 | 0.3908 |
| 193 | ss2 | 74 | ss1 | +0.0054 | 0.2222 |
| 189 | ss2 | 76 | ss1 | +0.0045 | 0.1221 |

### L30 H0 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 14  |  total attr: +0.0124

**Key mass** (top-1=18%, top-2=33%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0022 | 18.0% |
| 79 | ss1 | +0.0018 | 14.8% |
| 55 | flkL | +0.0017 | 13.7% |
| 77 | ss1 | +0.0016 | 12.7% |
| 52 | flkL | +0.0011 | 8.7% |

**Query mass** (top-1=26%, top-2=49%, top-3=61%)  [DISTR(L190/Y81/V192/L79)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | ss2 | +0.0032 | 25.8% |
| 81 | ss1 | +0.0028 | 22.8% |
| 192 | ss2 | +0.0016 | 12.7% |
| 79 | ss1 | +0.0012 | 9.6% |
| 187 | ss2 | +0.0010 | 8.2% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -104 | 1 | 7.1% |
| +111 | 1 | 7.1% |
| +115 | 1 | 7.1% |
| +24 | 1 | 7.1% |
| +110 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 5 | 35.7% |
| ss2 | ss1 | 4 | 28.6% |
| ss1 | ss2 | 2 | 14.3% |
| ss2 | flkL | 1 | 7.1% |
| ss1 | other | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 81 | ss1 | 185 | ss2 | +0.0022 | 0.2111 |
| 190 | ss2 | 79 | ss1 | +0.0018 | 0.0322 |
| 192 | ss2 | 77 | ss1 | +0.0016 | 0.1838 |
| 79 | ss1 | 55 | flkL | +0.0012 | 0.0703 |
| 190 | ss2 | 80 | ss1 | +0.0010 | 0.0349 |

### L30 H4 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 8  |  total attr: +0.0044

**Key mass** (top-1=36%, top-2=56%, top-3=70%)  [DISTR(D61/R193/P182/Y87)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | flkL | +0.0016 | 35.6% |
| 193 | ss2 | +0.0009 | 19.9% |
| 182 | other | +0.0006 | 14.1% |
| 87 | other | +0.0005 | 10.9% |
| 224 | flkR | +0.0004 | 9.9% |

**Query mass** (top-1=24%, top-2=46%, top-3=60%)  [DISTR(L190/L78/L79/G86)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | ss2 | +0.0011 | 24.4% |
| 78 | ss1 | +0.0009 | 21.3% |
| 79 | ss1 | +0.0006 | 14.2% |
| 86 | other | +0.0005 | 10.9% |
| 187 | ss2 | +0.0004 | 9.9% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 2 | 25.0% |
| +17 | 1 | 12.5% |
| +18 | 1 | 12.5% |
| +8 | 1 | 12.5% |
| -3 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 25.0% |
| ss2 | ss2 | 2 | 25.0% |
| ss2 | other | 1 | 12.5% |
| other | other | 1 | 12.5% |
| ss2 | flkR | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 78 | ss1 | 61 | flkL | +0.0009 | 0.0194 |
| 79 | ss1 | 61 | flkL | +0.0006 | 0.0160 |
| 190 | ss2 | 182 | other | +0.0006 | 0.0084 |
| 86 | other | 87 | other | +0.0005 | 0.0747 |
| 190 | ss2 | 193 | ss2 | +0.0005 | 0.0097 |

### L30 H12 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss1  |  cells: 27  |  total attr: +0.0277

**Key mass** (top-1=26%, top-2=38%, top-3=49%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0073 | 26.4% |
| 76 | ss1 | +0.0032 | 11.6% |
| 187 | ss2 | +0.0032 | 11.4% |
| 83 | other | +0.0025 | 9.0% |
| 78 | ss1 | +0.0019 | 6.7% |

**Query mass** (top-1=39%, top-2=51%, top-3=61%)  [DISTR(L78/D77/Y80/E187/L190)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | ss1 | +0.0108 | 39.0% |
| 77 | ss1 | +0.0033 | 12.0% |
| 80 | ss1 | +0.0028 | 9.9% |
| 187 | ss2 | +0.0023 | 8.3% |
| 190 | ss2 | +0.0021 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 7 | 25.9% |
| +4 | 5 | 18.5% |
| -3 | 3 | 11.1% |
| +2 | 2 | 7.4% |
| -5 | 2 | 7.4% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 12 | 44.4% |
| ss2 | ss2 | 7 | 25.9% |
| ss1 | other | 5 | 18.5% |
| ss1 | flkL | 2 | 7.4% |
| ss2 | other | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 78 | ss1 | 75 | ss1 | +0.0040 | 0.3343 |
| 77 | ss1 | 75 | ss1 | +0.0029 | 0.0829 |
| 78 | ss1 | 83 | other | +0.0025 | 0.0873 |
| 190 | ss2 | 187 | ss2 | +0.0017 | 0.0768 |
| 79 | ss1 | 76 | ss1 | +0.0017 | 0.1180 |

### L30 H13 — Rank #21

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | ss1→flkL  |  cells: 17  |  total attr: +0.0156

**Key mass** (top-1=23%, top-2=35%, top-3=46%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 52 | flkL | +0.0035 | 22.5% |
| 65 | flkL | +0.0019 | 12.3% |
| 62 | flkL | +0.0018 | 11.6% |
| 56 | flkL | +0.0016 | 10.4% |
| 80 | ss1 | +0.0015 | 9.3% |

**Query mass** (top-1=20%, top-2=37%, top-3=52%)  [DISTR(D77/L79/D76/L78/V188)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | ss1 | +0.0031 | 19.7% |
| 79 | ss1 | +0.0026 | 16.9% |
| 76 | ss1 | +0.0024 | 15.3% |
| 78 | ss1 | +0.0022 | 14.3% |
| 188 | ss2 | +0.0015 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +17 | 2 | 11.8% |
| +24 | 2 | 11.8% |
| +111 | 2 | 11.8% |
| +25 | 1 | 5.9% |
| +13 | 1 | 5.9% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=65%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 11 | 64.7% |
| ss2 | ss1 | 3 | 17.6% |
| ss1 | flkR | 1 | 5.9% |
| ss2 | other | 1 | 5.9% |
| flkR | flkL | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 77 | ss1 | 52 | flkL | +0.0023 | 0.1244 |
| 78 | ss1 | 65 | flkL | +0.0015 | 0.0446 |
| 188 | ss2 | 80 | ss1 | +0.0015 | 0.2377 |
| 79 | ss1 | 62 | flkL | +0.0014 | 0.0875 |
| 76 | ss1 | 52 | flkL | +0.0012 | 0.1351 |

### L30 H19 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | INTRA:ss1  |  cells: 10  |  total attr: +0.0428

**Key mass** (top-1=50%, top-2=75%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 81 | ss1 | +0.0212 | 49.7% |
| 79 | ss1 | +0.0110 | 25.7% |
| 80 | ss1 | +0.0062 | 14.5% |
| 76 | ss1 | +0.0015 | 3.5% |
| 78 | ss1 | +0.0012 | 2.7% |

**Query mass** (top-1=55%, top-2=78%, top-3=90%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | ss1 | +0.0236 | 55.2% |
| 77 | ss1 | +0.0096 | 22.5% |
| 79 | ss1 | +0.0052 | 12.1% |
| 76 | ss1 | +0.0017 | 3.9% |
| 75 | ss1 | +0.0015 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 90%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 5 | 50.0% |
| -2 | 4 | 40.0% |
| -3 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=90%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 90.0% |
| ss1 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 78 | ss1 | 81 | ss1 | +0.0212 | 0.3926 |
| 77 | ss1 | 79 | ss1 | +0.0096 | 0.3126 |
| 79 | ss1 | 80 | ss1 | +0.0052 | 0.2991 |
| 75 | ss1 | 76 | ss1 | +0.0015 | 0.1594 |
| 78 | ss1 | 79 | ss1 | +0.0013 | 0.0881 |

### L31 H10 — Rank #15

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | INTRA:ss1  |  cells: 22  |  total attr: +0.0153

**Key mass** (top-1=26%, top-2=41%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 79 | ss1 | +0.0040 | 25.9% |
| 77 | ss1 | +0.0023 | 15.0% |
| 75 | ss1 | +0.0015 | 9.7% |
| 82 | other | +0.0012 | 7.8% |
| 86 | other | +0.0012 | 7.7% |

**Query mass** (top-1=59%, top-2=83%, top-3=97%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | ss1 | +0.0091 | 59.3% |
| 79 | ss1 | +0.0036 | 23.5% |
| 77 | ss1 | +0.0021 | 13.8% |
| 190 | ss2 | +0.0005 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 4 | 18.2% |
| +1 | 2 | 9.1% |
| -8 | 2 | 9.1% |
| -7 | 2 | 9.1% |
| +0 | 2 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 50.0% |
| ss1 | other | 8 | 36.4% |
| ss1 | flkL | 2 | 9.1% |
| ss2 | ss2 | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 78 | ss1 | 79 | ss1 | +0.0028 | 0.1203 |
| 78 | ss1 | 77 | ss1 | +0.0011 | 0.0220 |
| 78 | ss1 | 75 | ss1 | +0.0011 | 0.0167 |
| 78 | ss1 | 82 | other | +0.0008 | 0.0158 |
| 77 | ss1 | 79 | ss1 | +0.0008 | 0.0602 |

### L31 H17 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 39  |  total attr: +0.0494

**Key mass** (top-1=25%, top-2=46%, top-3=57%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0122 | 24.8% |
| 232 | flkR | +0.0102 | 20.7% |
| 189 | ss2 | +0.0055 | 11.1% |
| 187 | ss2 | +0.0038 | 7.7% |
| 202 | flkR | +0.0022 | 4.5% |

**Query mass** (top-1=44%, top-2=58%, top-3=72%)  [DISTR(L78/K68/D77)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | ss1 | +0.0217 | 44.0% |
| 68 | flkL | +0.0071 | 14.3% |
| 77 | ss1 | +0.0070 | 14.1% |
| 202 | flkR | +0.0025 | 5.1% |
| 206 | flkR | +0.0020 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -154 | 1 | 2.6% |
| +79 | 1 | 2.6% |
| -111 | 1 | 2.6% |
| -109 | 1 | 2.6% |
| +78 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=21%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 20.5% |
| ss1 | flkR | 7 | 17.9% |
| ss1 | other | 3 | 7.7% |
| flkR | other | 3 | 7.7% |
| flkL | ss1 | 3 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 78 | ss1 | 232 | flkR | +0.0068 | 0.0778 |
| 78 | ss1 | -1 | other | +0.0046 | 0.0598 |
| 78 | ss1 | 189 | ss2 | +0.0033 | 0.0326 |
| 78 | ss1 | 187 | ss2 | +0.0024 | 0.0315 |
| 77 | ss1 | -1 | other | +0.0022 | 0.0904 |

### L32 H13 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 19  |  total attr: +0.0812

**Key mass** (top-1=30%, top-2=58%, top-3=75%)  [DISTR(D77/L78/E187)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | ss1 | +0.0245 | 30.2% |
| 78 | ss1 | +0.0222 | 27.4% |
| 187 | ss2 | +0.0138 | 17.0% |
| 192 | ss2 | +0.0052 | 6.4% |
| 190 | ss2 | +0.0033 | 4.0% |

**Query mass** (top-1=28%, top-2=54%, top-3=72%)  [DISTR(V192/E187/L78)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 192 | ss2 | +0.0226 | 27.9% |
| 187 | ss2 | +0.0213 | 26.2% |
| 78 | ss1 | +0.0147 | 18.1% |
| 77 | ss1 | +0.0052 | 6.4% |
| 190 | ss2 | +0.0046 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +115 | 2 | 10.5% |
| -115 | 2 | 10.5% |
| -111 | 2 | 10.5% |
| +111 | 2 | 10.5% |
| +113 | 2 | 10.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 57.9% |
| ss1 | ss2 | 8 | 42.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 192 | ss2 | 77 | ss1 | +0.0226 | 0.2823 |
| 187 | ss2 | 78 | ss1 | +0.0213 | 0.1786 |
| 78 | ss1 | 187 | ss2 | +0.0138 | 0.1162 |
| 77 | ss1 | 192 | ss2 | +0.0052 | 0.0645 |
| 79 | ss1 | 190 | ss2 | +0.0033 | 0.0310 |

### L32 H18 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 22  |  total attr: +0.0880

**Key mass** (top-1=21%, top-2=41%, top-3=59%)  [DISTR(L78/L79/L190/D77)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | ss1 | +0.0186 | 21.1% |
| 79 | ss1 | +0.0171 | 19.5% |
| 190 | ss2 | +0.0164 | 18.7% |
| 77 | ss1 | +0.0117 | 13.3% |
| 192 | ss2 | +0.0062 | 7.0% |

**Query mass** (top-1=29%, top-2=48%, top-3=62%)  [DISTR(L190/E187/L79/D77)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | ss2 | +0.0255 | 29.0% |
| 187 | ss2 | +0.0171 | 19.4% |
| 79 | ss1 | +0.0123 | 14.0% |
| 77 | ss1 | +0.0103 | 11.7% |
| 189 | ss2 | +0.0044 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +111 | 2 | 9.1% |
| -111 | 2 | 9.1% |
| +113 | 2 | 9.1% |
| +115 | 2 | 9.1% |
| +109 | 1 | 4.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 12 | 54.5% |
| ss1 | ss2 | 10 | 45.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 190 | ss2 | 79 | ss1 | +0.0171 | 0.0993 |
| 187 | ss2 | 78 | ss1 | +0.0148 | 0.0757 |
| 79 | ss1 | 190 | ss2 | +0.0123 | 0.0711 |
| 190 | ss2 | 77 | ss1 | +0.0084 | 0.1225 |
| 77 | ss1 | 192 | ss2 | +0.0062 | 0.0469 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #6 | L0 | H19 | 3 | +0.0041 | SINGLE-ANCHOR | V28 | SINGLE-ANCHOR | V43 |  |  |
| #22 | L8 | H7 | 4 | +0.0194 | SINGLE-ANCHOR | W32 | SINGLE-ANCHOR | A63 |  |  |
| #24 | L10 | H9 | 24 | +0.0290 | DUAL-ANCHOR | A63/L17 | DISTRIBUTED | G86/W32/A63/L190 |  |  |
| #10 | L11 | H16 | 46 | +0.0911 | SINGLE-ANCHOR | W32 | DISTRIBUTED |  |  |  |
| #5 | L12 | H2 | 30 | +0.0695 | DUAL-ANCHOR | L17/W32 | DISTRIBUTED | ?-1/G86/L205/A63 |  |  |
| #8 | L13 | H10 | 21 | +0.0561 | SINGLE-ANCHOR | A63 | DISTRIBUTED | G86/L78/L209/A63 |  |  |
| #12 | L13 | H18 | 37 | +0.0797 | SINGLE-ANCHOR | A63 | DISTRIBUTED |  |  |  |
| #28 | L14 | H9 | 20 | +0.0291 | DISTRIBUTED | A63/?-1/W32 | DISTRIBUTED | ?-1/W32/L190/P93 |  |  |
| #18 | L14 | H16 | 72 | +0.0960 | DUAL-ANCHOR | L17/P18 | DISTRIBUTED |  |  |  |
| #23 | L14 | H17 | 4 | +0.0019 | DUAL-ANCHOR | W32/?232 | DUAL-ANCHOR | ?232/S89 |  | CROSS:flkR→flkL |
| #19 | L15 | H6 | 30 | +0.0360 | SINGLE-ANCHOR | A63 | DISTRIBUTED |  |  |  |
| #25 | L15 | H12 | 34 | +0.0435 | DISTRIBUTED | A63/G86/R90/W32 | DISTRIBUTED | G86/A63/Y87/S89/V88 |  |  |
| #27 | L15 | H19 | 10 | +0.0091 | DUAL-ANCHOR | L17/I0 | DISTRIBUTED | ?-1/L209/A63/G86 |  |  |
| #20 | L18 | H4 | 16 | +0.0138 | DISTRIBUTED |  | SINGLE-ANCHOR | G86 |  |  |
| #30 | L18 | H14 | 34 | +0.0317 | DISTRIBUTED | L17/?232/E59 | DISTRIBUTED |  |  |  |
| #26 | L20 | H8 | 22 | +0.0271 | SINGLE-ANCHOR | ?-1 | DISTRIBUTED |  |  |  |
| #11 | L21 | H2 | 18 | +0.0674 | SINGLE-ANCHOR | G86 | SINGLE-ANCHOR | L79 |  |  |
| #14 | L21 | H4 | 16 | +0.0365 | SINGLE-ANCHOR | G86 | DISTRIBUTED | D76/L190/L78 |  |  |
| #29 | L22 | H16 | 16 | +0.0287 | DISTRIBUTED | D76/G86/L74/L190 | DISTRIBUTED | L79/E82/D76 |  |  |
| #3 | L27 | H15 | 34 | +0.0684 | DISTRIBUTED |  | DISTRIBUTED | D77/V188/R186/L78/Y80 |  | CROSS:ss1→ss2 |
| #4 | L29 | H18 | 45 | +0.0738 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #17 | L30 | H0 | 14 | +0.0124 | DISTRIBUTED |  | DISTRIBUTED | L190/Y81/V192/L79 |  |  |
| #16 | L30 | H4 | 8 | +0.0044 | DISTRIBUTED | D61/R193/P182/Y87 | DISTRIBUTED | L190/L78/L79/G86 |  |  |
| #13 | L30 | H12 | 27 | +0.0277 | DISTRIBUTED |  | DISTRIBUTED | L78/D77/Y80/E187/L190 |  | INTRA:ss1 |
| #21 | L30 | H13 | 17 | +0.0156 | DISTRIBUTED |  | DISTRIBUTED | D77/L79/D76/L78/V188 |  | ss1→flkL |
| #9 | L30 | H19 | 10 | +0.0428 | DUAL-ANCHOR | Y81/L79 | DUAL-ANCHOR | L78/D77 |  | INTRA:ss1 |
| #15 | L31 | H10 | 22 | +0.0153 | DISTRIBUTED |  | DUAL-ANCHOR | L78/L79 |  | INTRA:ss1 |
| #7 | L31 | H17 | 39 | +0.0494 | DISTRIBUTED |  | DISTRIBUTED | L78/K68/D77 |  |  |
| #2 | L32 | H13 | 19 | +0.0812 | DISTRIBUTED | D77/L78/E187 | DISTRIBUTED | V192/E187/L78 |  | CROSS:ss2→ss1 |
| #1 | L32 | H18 | 22 | +0.0880 | DISTRIBUTED | L78/L79/L190/D77 | DISTRIBUTED | L190/E187/L79/D77 |  | CROSS:ss2→ss1 |
