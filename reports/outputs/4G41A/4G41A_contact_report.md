# Contact Pattern Analysis: 4G41A

Generated: 2026-03-22 21:41:20   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4G41A |
| Contact pair | (62, 184) |
| ss1 | [57, 68) |
| ss2 | [179, 190) |
| Clean flank | 50 |
| Corrupt flank | 49 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.9031 |
| Corrupt metric | 0.2966 |
| Gap | 0.6066 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 250 | 91.44% |
| positive IE | 200 | 78.18% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H13 | +0.4753 |
| 2 | L5 | H7 | +0.2715 |
| 3 | L32 | H18 | +0.2085 |
| 4 | L12 | H15 | +0.1664 |
| 5 | L29 | H18 | +0.1052 |
| 6 | L0 | H0 | +0.1002 |
| 7 | L12 | H3 | +0.0735 |
| 8 | L16 | H13 | +0.0679 |
| 9 | L30 | H1 | +0.0670 |
| 10 | L13 | H18 | +0.0554 |
| 11 | L14 | H12 | +0.0530 |
| 12 | L15 | H4 | +0.0467 |
| 13 | L31 | H2 | +0.0435 |
| 14 | L21 | H13 | +0.0424 |
| 15 | L22 | H8 | +0.0416 |
| 16 | L24 | H8 | +0.0411 |
| 17 | L7 | H13 | +0.0378 |
| 18 | L14 | H8 | +0.0369 |
| 19 | L26 | H2 | +0.0342 |
| 20 | L28 | H5 | +0.0338 |
| 21 | L23 | H5 | +0.0290 |
| 22 | L5 | H10 | +0.0289 |
| 23 | L27 | H15 | +0.0259 |
| 24 | L17 | H1 | +0.0252 |
| 25 | L19 | H18 | +0.0252 |
| 26 | L18 | H17 | +0.0238 |
| 27 | L23 | H8 | +0.0236 |
| 28 | L12 | H8 | +0.0226 |
| 29 | L10 | H11 | +0.0223 |
| 30 | L31 | H7 | +0.0217 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.66% |
| 2 | 0.85% |
| 3 | 0.97% |
| 4 | 0.28% |
| 5 | 0.24% |
| 6 | -1.49% |
| 7 | -3.39% |
| 8 | -2.96% |
| 9 | -3.16% |
| 10 | -2.85% |
| 20 | -3.38% |
| 80 | 14.06% |
| 450 | 136.22% |

## Cell Attribution Analysis

Total cells: 10,666,026

- Positive: 5,342,130
- Negative: 5,319,167

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000104 | 1,066,604 |
| 95th | +0.00000304 | 533,302 |
| 99th | +0.00002145 | 106,661 |
| 99.5th | +0.00004422 | 53,331 |
| 99.9th | +0.00020676 | 10,667 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H7 | 77 | other | 7 | flkL | +0.218134 | 0.074604 |
| L32 | H13 | 59 | ss1 | 182 | ss2 | +0.063511 | 0.246258 |
| L32 | H13 | 186 | ss2 | 63 | ss1 | +0.061922 | 0.273638 |
| L17 | H12 | 178 | other | 80 | other | +0.048970 | 0.319996 |
| L23 | H8 | 60 | ss1 | 55 | flkL | +0.048414 | 0.325590 |
| L17 | H12 | 185 | ss2 | 196 | flkR | +0.045199 | 0.406538 |
| L17 | H12 | 186 | ss2 | 80 | other | +0.041081 | 0.360030 |
| L6 | H0 | 77 | other | 7 | flkL | +0.036991 | 0.032111 |
| L32 | H13 | 182 | ss2 | 59 | ss1 | +0.036578 | 0.141829 |
| L12 | H15 | 61 | ss1 | 76 | other | +0.036530 | 0.425699 |
| L15 | H4 | 182 | ss2 | 80 | other | +0.035381 | 0.308806 |
| L32 | H13 | 63 | ss1 | 186 | ss2 | +0.032107 | 0.141884 |
| L20 | H1 | 61 | ss1 | 66 | ss1 | +0.031774 | 0.418694 |
| L24 | H8 | 60 | ss1 | 53 | flkL | +0.031252 | 0.303932 |
| L26 | H2 | 60 | ss1 | 80 | other | +0.030027 | 0.133375 |
| L5 | H7 | 79 | other | 7 | flkL | +0.029979 | 0.060951 |
| L17 | H12 | 61 | ss1 | 196 | flkR | +0.029112 | 0.440822 |
| L12 | H15 | 60 | ss1 | 76 | other | +0.029009 | 0.396908 |
| L22 | H8 | 63 | ss1 | 67 | ss1 | +0.028636 | 0.647927 |
| L12 | H15 | 59 | ss1 | 76 | other | +0.028415 | 0.438052 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L17 | H12 | 60 | ss1 | 80 | other | -0.019127 | 0.524503 |
| L12 | H15 | 66 | ss1 | 76 | other | -0.019136 | 0.387661 |
| L18 | H2 | 55 | flkL | 196 | flkR | -0.019381 | 0.159954 |
| L13 | H3 | 80 | other | 76 | other | -0.021557 | 0.168926 |
| L15 | H4 | 178 | other | 80 | other | -0.022100 | 0.384306 |
| L8 | H6 | 77 | other | 75 | other | -0.024483 | 0.053372 |
| L17 | H12 | 64 | ss1 | 80 | other | -0.024696 | 0.520862 |
| L31 | H17 | 185 | ss2 | 61 | ss1 | -0.028648 | 0.130716 |
| L17 | H12 | 59 | ss1 | 196 | flkR | -0.030700 | 0.357247 |
| L12 | H15 | 63 | ss1 | 76 | other | -0.031448 | 0.419827 |
| L17 | H12 | 185 | ss2 | 80 | other | -0.031991 | 0.370059 |
| L7 | H9 | 76 | other | 9 | flkL | -0.033069 | 0.070931 |
| L6 | H0 | 76 | other | 7 | flkL | -0.033786 | 0.040301 |
| L5 | H13 | 77 | other | 13 | flkL | -0.034882 | 0.033224 |
| L31 | H17 | 189 | ss2 | -1 | other | -0.035586 | 0.155630 |
| L29 | H18 | 63 | ss1 | 185 | ss2 | -0.038616 | 0.303480 |
| L29 | H18 | 67 | ss1 | 8 | flkL | -0.040322 | 0.383919 |
| L29 | H18 | 63 | ss1 | 8 | flkL | -0.050178 | 0.185313 |
| L17 | H12 | 61 | ss1 | 80 | other | -0.067626 | 0.525686 |
| L5 | H7 | 76 | other | 7 | flkL | -0.216041 | 0.096395 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.2966 | 0.00% |
| 10 | 10 | 6 | 0.2966 | 0.00% |
| 20 | 20 | 11 | 0.2966 | 0.00% |
| 50 | 50 | 27 | 0.2968 | 0.04% |
| 100 | 100 | 51 | 0.3004 | 0.63% |
| 200 | 200 | 77 | 0.2999 | 0.54% |
| 500 | 500 | 131 | 0.3028 | 1.03% |
| 1000 | 1,000 | 163 | 0.3098 | 2.18% |
| 2000 | 2,000 | 190 | 0.3120 | 2.55% |
| 5000 | 5,000 | 198 | 0.2687 | -4.59% |
| 10000 | 10,000 | 200 | 0.3006 | 0.66% |
| 20000 | 20,000 | 200 | 0.3380 | 6.83% |
| 50000 | 50,000 | 200 | 0.4770 | 29.74% |

## Motif Analysis

### L0 H0 — Rank #6

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L5 H7 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.3469

**Key mass** (top-1=78%, top-2=84%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 7 | flkL | +0.2705 | 78.0% |
| 8 | flkL | +0.0222 | 6.4% |
| 173 | other | +0.0162 | 4.7% |
| 174 | other | +0.0116 | 3.3% |
| 5 | other | +0.0056 | 1.6% |

**Query mass** (top-1=83%, top-2=92%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | other | +0.2877 | 82.9% |
| 79 | other | +0.0323 | 9.3% |
| 75 | other | +0.0221 | 6.4% |
| 74 | other | +0.0026 | 0.7% |
| 76 | other | +0.0022 | 0.6% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +72 | 2 | 12.5% |
| +68 | 2 | 12.5% |
| +67 | 2 | 12.5% |
| +70 | 1 | 6.2% |
| +69 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 9 | 56.2% |
| other | other | 7 | 43.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 77 | other | 7 | flkL | +0.2181 | 0.0746 |
| 79 | other | 7 | flkL | +0.0300 | 0.0610 |
| 75 | other | 7 | flkL | +0.0198 | 0.0867 |
| 77 | other | 8 | flkL | +0.0175 | 0.0090 |
| 77 | other | 173 | other | +0.0162 | 0.0067 |

### L5 H10 — Rank #22

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 5  |  total attr: +0.0192

**Key mass** (top-1=49%, top-2=83%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 9 | flkL | +0.0095 | 49.2% |
| 7 | flkL | +0.0064 | 33.4% |
| 10 | flkL | +0.0033 | 17.4% |

**Query mass** (top-1=82%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | other | +0.0158 | 82.0% |
| 79 | other | +0.0035 | 18.0% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +70 | 2 | 40.0% |
| +68 | 1 | 20.0% |
| +67 | 1 | 20.0% |
| +72 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 77 | other | 9 | flkL | +0.0077 | 0.0143 |
| 77 | other | 7 | flkL | +0.0047 | 0.0133 |
| 77 | other | 10 | flkL | +0.0033 | 0.0044 |
| 79 | other | 9 | flkL | +0.0017 | 0.0173 |
| 79 | other | 7 | flkL | +0.0017 | 0.0134 |

### L7 H13 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 2  |  total attr: +0.0075

**Key mass** (top-1=66%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 8 | flkL | +0.0050 | 66.3% |
| 49 | flkL | +0.0025 | 33.7% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 66 | ss1 | +0.0075 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +58 | 1 | 50.0% |
| +17 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 66 | ss1 | 8 | flkL | +0.0050 | 0.0899 |
| 66 | ss1 | 49 | flkL | +0.0025 | 0.0210 |

### L10 H11 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0154

**Key mass** (top-1=74%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | other | +0.0114 | 73.8% |
| 76 | other | +0.0040 | 26.2% |

**Query mass** (top-1=62%, top-2=88%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | other | +0.0095 | 61.8% |
| 80 | other | +0.0041 | 26.5% |
| 66 | ss1 | +0.0018 | 11.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 25.0% |
| +4 | 1 | 25.0% |
| +3 | 1 | 25.0% |
| -10 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 3 | 75.0% |
| ss1 | other | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 77 | other | 77 | other | +0.0095 | 0.0815 |
| 80 | other | 76 | other | +0.0022 | 0.0507 |
| 80 | other | 77 | other | +0.0018 | 0.0425 |
| 66 | ss1 | 76 | other | +0.0018 | 0.0803 |

### L12 H3 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 14  |  total attr: +0.0681

**Key mass** (top-1=88%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | other | +0.0600 | 88.0% |
| 77 | other | +0.0063 | 9.3% |
| 79 | other | +0.0018 | 2.7% |

**Query mass** (top-1=20%, top-2=39%, top-3=54%)  [DISTR(G53/K56/L49/S59/Q51)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.0139 | 20.4% |
| 56 | flkL | +0.0128 | 18.7% |
| 49 | flkL | +0.0103 | 15.1% |
| 59 | ss1 | +0.0078 | 11.5% |
| 51 | flkL | +0.0054 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 2 | 14.3% |
| -23 | 1 | 7.1% |
| -27 | 1 | 7.1% |
| -25 | 1 | 7.1% |
| -29 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 10 | 71.4% |
| ss1 | other | 4 | 28.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 53 | flkL | 76 | other | +0.0117 | 0.3014 |
| 56 | flkL | 76 | other | +0.0104 | 0.2184 |
| 49 | flkL | 76 | other | +0.0103 | 0.3363 |
| 51 | flkL | 76 | other | +0.0054 | 0.3363 |
| 47 | flkL | 76 | other | +0.0053 | 0.2613 |

### L12 H8 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 3  |  total attr: +0.0097

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | other | +0.0097 | 100.0% |

**Query mass** (top-1=48%, top-2=79%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | other | +0.0047 | 47.9% |
| 186 | ss2 | +0.0030 | 31.1% |
| 177 | other | +0.0020 | 21.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 1 | 33.3% |
| +110 | 1 | 33.3% |
| +101 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 2 | 66.7% |
| ss2 | other | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | other | 76 | other | +0.0047 | 0.0614 |
| 186 | ss2 | 76 | other | +0.0030 | 0.0324 |
| 177 | other | 76 | other | +0.0020 | 0.0496 |

### L12 H15 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.2273

**Key mass** (top-1=92%, top-2=96%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | other | +0.2099 | 92.3% |
| 77 | other | +0.0094 | 4.1% |
| 196 | flkR | +0.0080 | 3.5% |

**Query mass** (top-1=17%, top-2=31%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0384 | 16.9% |
| 59 | ss1 | +0.0313 | 13.8% |
| 60 | ss1 | +0.0312 | 13.7% |
| 64 | ss1 | +0.0224 | 9.9% |
| 53 | flkL | +0.0218 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -18 | 3 | 13.0% |
| -16 | 2 | 8.7% |
| -17 | 2 | 8.7% |
| -24 | 2 | 8.7% |
| -15 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 12 | 52.2% |
| flkL | other | 7 | 30.4% |
| other | flkR | 2 | 8.7% |
| other | other | 1 | 4.3% |
| ss2 | flkR | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 61 | ss1 | 76 | other | +0.0365 | 0.4257 |
| 60 | ss1 | 76 | other | +0.0290 | 0.3969 |
| 59 | ss1 | 76 | other | +0.0284 | 0.4381 |
| 64 | ss1 | 76 | other | +0.0224 | 0.3827 |
| 53 | flkL | 76 | other | +0.0194 | 0.2542 |

### L13 H18 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0938

**Key mass** (top-1=79%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | other | +0.0738 | 78.7% |
| 196 | flkR | +0.0179 | 19.1% |
| 77 | other | +0.0021 | 2.2% |

**Query mass** (top-1=21%, top-2=40%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 196 | flkR | +0.0193 | 20.6% |
| 186 | ss2 | +0.0186 | 19.8% |
| 185 | ss2 | +0.0061 | 6.5% |
| 183 | ss2 | +0.0058 | 6.2% |
| 182 | ss2 | +0.0056 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 1 | 5.6% |
| +110 | 1 | 5.6% |
| +109 | 1 | 5.6% |
| +107 | 1 | 5.6% |
| -14 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 8 | 44.4% |
| flkR | other | 3 | 16.7% |
| other | flkR | 2 | 11.1% |
| ss2 | flkR | 1 | 5.6% |
| flkL | flkR | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 196 | flkR | 76 | other | +0.0193 | 0.1408 |
| 186 | ss2 | 76 | other | +0.0186 | 0.1450 |
| 185 | ss2 | 76 | other | +0.0061 | 0.1344 |
| 183 | ss2 | 76 | other | +0.0058 | 0.1169 |
| 182 | ss2 | 196 | flkR | +0.0056 | 0.0953 |

### L14 H8 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 9  |  total attr: +0.0235

**Key mass** (top-1=24%, top-2=41%, top-3=51%)  [DISTR(A64/F70/V63/M58/L66)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0056 | 24.0% |
| 70 | other | +0.0040 | 17.0% |
| 63 | ss1 | +0.0024 | 10.4% |
| 58 | ss1 | +0.0023 | 9.7% |
| 66 | ss1 | +0.0022 | 9.4% |

**Query mass** (top-1=31%, top-2=55%, top-3=72%)  [DISTR(M61/V67/V63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0073 | 31.0% |
| 67 | ss1 | +0.0057 | 24.3% |
| 63 | ss1 | +0.0039 | 16.8% |
| 59 | ss1 | +0.0024 | 10.4% |
| 62 | ss1 | +0.0022 | 9.4% |

**Offset distribution [frequency]** (top-2 coverage: 78%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 4 | 44.4% |
| -3 | 3 | 33.3% |
| +5 | 1 | 11.1% |
| +4 | 1 | 11.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 66.7% |
| ss1 | other | 2 | 22.2% |
| other | other | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 61 | ss1 | 64 | ss1 | +0.0056 | 0.4103 |
| 67 | ss1 | 70 | other | +0.0040 | 0.1868 |
| 59 | ss1 | 63 | ss1 | +0.0024 | 0.0642 |
| 63 | ss1 | 58 | ss1 | +0.0023 | 0.0885 |
| 62 | ss1 | 66 | ss1 | +0.0022 | 0.2490 |

### L14 H12 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 11  |  total attr: +0.0427

**Key mass** (top-1=60%, top-2=81%, top-3=87%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | other | +0.0257 | 60.2% |
| 63 | ss1 | +0.0090 | 21.0% |
| 62 | ss1 | +0.0025 | 5.8% |
| 60 | ss1 | +0.0022 | 5.1% |
| 59 | ss1 | +0.0017 | 3.9% |

**Query mass** (top-1=24%, top-2=45%, top-3=59%)  [DISTR(L49/V63/M61/A64)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 49 | flkL | +0.0101 | 23.7% |
| 63 | ss1 | +0.0091 | 21.2% |
| 61 | ss1 | +0.0059 | 13.9% |
| 64 | ss1 | +0.0059 | 13.7% |
| 53 | flkL | +0.0052 | 12.2% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -13 | 2 | 18.2% |
| -10 | 2 | 18.2% |
| -15 | 1 | 9.1% |
| -12 | 1 | 9.1% |
| -14 | 1 | 9.1% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 5 | 45.5% |
| ss1 | other | 4 | 36.4% |
| other | other | 2 | 18.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 76 | other | +0.0091 | 0.1640 |
| 61 | ss1 | 76 | other | +0.0059 | 0.1095 |
| 64 | ss1 | 76 | other | +0.0059 | 0.3130 |
| 53 | flkL | 63 | ss1 | +0.0052 | 0.0776 |
| 49 | flkL | 63 | ss1 | +0.0038 | 0.0586 |

### L15 H4 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.1276

**Key mass** (top-1=90%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 80 | other | +0.1152 | 90.3% |
| -1 | other | +0.0107 | 8.4% |
| 222 | flkR | +0.0017 | 1.4% |

**Query mass** (top-1=28%, top-2=40%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 182 | ss2 | +0.0354 | 27.7% |
| 190 | flkR | +0.0155 | 12.1% |
| 185 | ss2 | +0.0072 | 5.6% |
| 181 | ss2 | +0.0070 | 5.5% |
| 193 | flkR | +0.0068 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 1 | 4.5% |
| +110 | 1 | 4.5% |
| +105 | 1 | 4.5% |
| +101 | 1 | 4.5% |
| +113 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 10 | 45.5% |
| ss2 | other | 4 | 18.2% |
| ss1 | other | 3 | 13.6% |
| other | other | 3 | 13.6% |
| flkL | other | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 182 | ss2 | 80 | other | +0.0354 | 0.3088 |
| 190 | flkR | 80 | other | +0.0155 | 0.4367 |
| 185 | ss2 | 80 | other | +0.0072 | 0.2307 |
| 181 | ss2 | 80 | other | +0.0070 | 0.3285 |
| 193 | flkR | 80 | other | +0.0068 | 0.3470 |

### L16 H13 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0752

**Key mass** (top-1=82%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 80 | other | +0.0613 | 81.5% |
| 196 | flkR | +0.0095 | 12.7% |
| -1 | other | +0.0027 | 3.5% |
| 9 | flkL | +0.0017 | 2.2% |

**Query mass** (top-1=18%, top-2=33%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 186 | ss2 | +0.0132 | 17.6% |
| 226 | flkR | +0.0116 | 15.4% |
| 196 | flkR | +0.0113 | 15.1% |
| 219 | flkR | +0.0046 | 6.1% |
| 215 | flkR | +0.0042 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +106 | 1 | 5.6% |
| +116 | 1 | 5.6% |
| +146 | 1 | 5.6% |
| +139 | 1 | 5.6% |
| +135 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 8 | 44.4% |
| ss2 | other | 5 | 27.8% |
| other | flkR | 1 | 5.6% |
| flkL | flkR | 1 | 5.6% |
| other | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 186 | ss2 | 80 | other | +0.0132 | 0.1693 |
| 196 | flkR | 80 | other | +0.0113 | 0.4152 |
| 226 | flkR | 80 | other | +0.0099 | 0.4295 |
| 219 | flkR | 80 | other | +0.0046 | 0.4185 |
| 215 | flkR | 80 | other | +0.0042 | 0.4317 |

### L17 H1 — Rank #24

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0438

**Key mass** (top-1=45%, top-2=84%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 196 | flkR | +0.0195 | 44.5% |
| 76 | other | +0.0171 | 39.1% |
| 77 | other | +0.0072 | 16.4% |

**Query mass** (top-1=29%, top-2=55%, top-3=66%)  [DISTR(V63/S80/V67/I76)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0126 | 28.7% |
| 80 | other | +0.0114 | 26.1% |
| 67 | ss1 | +0.0049 | 11.2% |
| 76 | other | +0.0047 | 10.7% |
| 79 | other | +0.0034 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -116 | 1 | 10.0% |
| -13 | 1 | 10.0% |
| -14 | 1 | 10.0% |
| -120 | 1 | 10.0% |
| -117 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 60.0% |
| other | flkR | 3 | 30.0% |
| flkL | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 80 | other | 196 | flkR | +0.0114 | 0.1753 |
| 63 | ss1 | 76 | other | +0.0075 | 0.1226 |
| 63 | ss1 | 77 | other | +0.0051 | 0.0958 |
| 76 | other | 196 | flkR | +0.0047 | 0.1871 |
| 79 | other | 196 | flkR | +0.0034 | 0.1297 |

### L18 H17 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0474

**Key mass** (top-1=53%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | other | +0.0253 | 53.3% |
| 77 | other | +0.0221 | 46.7% |

**Query mass** (top-1=37%, top-2=58%, top-3=75%)  [DISTR(E178/A186/A181)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | other | +0.0173 | 36.6% |
| 186 | ss2 | +0.0101 | 21.2% |
| 181 | ss2 | +0.0080 | 16.8% |
| 60 | ss1 | +0.0060 | 12.7% |
| 188 | ss2 | +0.0036 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 1 | 9.1% |
| +102 | 1 | 9.1% |
| +110 | 1 | 9.1% |
| +109 | 1 | 9.1% |
| +104 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 6 | 54.5% |
| ss1 | other | 3 | 27.3% |
| other | other | 2 | 18.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | other | 77 | other | +0.0092 | 0.1041 |
| 178 | other | 76 | other | +0.0082 | 0.0772 |
| 186 | ss2 | 76 | other | +0.0055 | 0.0870 |
| 186 | ss2 | 77 | other | +0.0046 | 0.0864 |
| 181 | ss2 | 77 | other | +0.0042 | 0.0892 |

### L19 H18 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR  |  cells: 4  |  total attr: +0.0092

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 80 | other | +0.0092 | 100.0% |

**Query mass** (top-1=30%, top-2=56%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0027 | 29.6% |
| 59 | ss1 | +0.0024 | 26.5% |
| 64 | ss1 | +0.0023 | 24.9% |
| 61 | ss1 | +0.0018 | 19.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 1 | 25.0% |
| -21 | 1 | 25.0% |
| -16 | 1 | 25.0% |
| -19 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 80 | other | +0.0027 | 0.0982 |
| 59 | ss1 | 80 | other | +0.0024 | 0.1179 |
| 64 | ss1 | 80 | other | +0.0023 | 0.1134 |
| 61 | ss1 | 80 | other | +0.0018 | 0.0499 |

### L21 H13 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 11  |  total attr: +0.0693

**Key mass** (top-1=37%, top-2=58%, top-3=75%)  [DISTR(V63/S59/T62)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0256 | 36.9% |
| 59 | ss1 | +0.0147 | 21.2% |
| 62 | ss1 | +0.0114 | 16.5% |
| 66 | ss1 | +0.0089 | 12.9% |
| 58 | ss1 | +0.0030 | 4.3% |

**Query mass** (top-1=22%, top-2=40%, top-3=58%)  [DISTR(A64/A60/L66/M61)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0151 | 21.8% |
| 60 | ss1 | +0.0129 | 18.7% |
| 66 | ss1 | +0.0124 | 17.9% |
| 61 | ss1 | +0.0097 | 14.0% |
| 67 | ss1 | +0.0089 | 12.9% |

**Offset distribution [frequency]** (top-2 coverage: 64%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 4 | 36.4% |
| -1 | 3 | 27.3% |
| +0 | 3 | 27.3% |
| +3 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=91%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 90.9% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 63 | ss1 | +0.0151 | 0.2826 |
| 60 | ss1 | 59 | ss1 | +0.0110 | 0.3228 |
| 66 | ss1 | 63 | ss1 | +0.0104 | 0.3626 |
| 61 | ss1 | 62 | ss1 | +0.0097 | 0.3219 |
| 67 | ss1 | 66 | ss1 | +0.0089 | 0.6853 |

### L22 H8 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 12  |  total attr: +0.0610

**Key mass** (top-1=54%, top-2=63%, top-3=70%)  [DISTR(V67/A72/K71)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 67 | ss1 | +0.0327 | 53.6% |
| 72 | other | +0.0059 | 9.7% |
| 71 | other | +0.0044 | 7.1% |
| 63 | ss1 | +0.0043 | 7.1% |
| 62 | ss1 | +0.0032 | 5.2% |

**Query mass** (top-1=47%, top-2=61%, top-3=68%)  [DISTR(V63/T62/A64/I65)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0286 | 46.9% |
| 62 | ss1 | +0.0087 | 14.3% |
| 64 | ss1 | +0.0041 | 6.7% |
| 65 | ss1 | +0.0032 | 5.2% |
| 52 | flkL | +0.0030 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 4 | 33.3% |
| -10 | 2 | 16.7% |
| -3 | 2 | 16.7% |
| +3 | 2 | 16.7% |
| +4 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 58.3% |
| ss1 | other | 2 | 16.7% |
| flkL | flkL | 1 | 8.3% |
| flkL | other | 1 | 8.3% |
| other | other | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 67 | ss1 | +0.0286 | 0.6479 |
| 62 | ss1 | 72 | other | +0.0059 | 0.2850 |
| 64 | ss1 | 67 | ss1 | +0.0041 | 0.1910 |
| 65 | ss1 | 62 | ss1 | +0.0032 | 0.3952 |
| 52 | flkL | 55 | flkL | +0.0030 | 0.3011 |

### L23 H5 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 6  |  total attr: +0.0418

**Key mass** (top-1=88%, top-2=94%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | flkL | +0.0369 | 88.2% |
| 47 | flkL | +0.0025 | 6.0% |
| 49 | flkL | +0.0024 | 5.8% |

**Query mass** (top-1=60%, top-2=78%, top-3=90%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0251 | 60.1% |
| 64 | ss1 | +0.0076 | 18.2% |
| 57 | ss1 | +0.0048 | 11.5% |
| 63 | ss1 | +0.0043 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +13 | 2 | 33.3% |
| +16 | 1 | 16.7% |
| +20 | 1 | 16.7% |
| +19 | 1 | 16.7% |
| +15 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 44 | flkL | +0.0226 | 0.1997 |
| 64 | ss1 | 44 | flkL | +0.0052 | 0.0930 |
| 57 | ss1 | 44 | flkL | +0.0048 | 0.1774 |
| 63 | ss1 | 44 | flkL | +0.0043 | 0.1206 |
| 60 | ss1 | 47 | flkL | +0.0025 | 0.0677 |

### L23 H8 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 4  |  total attr: +0.0598

**Key mass** (top-1=84%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 55 | flkL | +0.0501 | 83.7% |
| 178 | other | +0.0065 | 10.9% |
| 60 | ss1 | +0.0032 | 5.4% |

**Query mass** (top-1=81%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0484 | 80.9% |
| 181 | ss2 | +0.0065 | 10.9% |
| 64 | ss1 | +0.0032 | 5.4% |
| 59 | ss1 | +0.0017 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 50.0% |
| +5 | 1 | 25.0% |
| +3 | 1 | 25.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 50.0% |
| ss2 | other | 1 | 25.0% |
| ss1 | ss1 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 55 | flkL | +0.0484 | 0.3256 |
| 181 | ss2 | 178 | other | +0.0065 | 0.0486 |
| 64 | ss1 | 60 | ss1 | +0.0032 | 0.1394 |
| 59 | ss1 | 55 | flkL | +0.0017 | 0.1276 |

### L24 H8 — Rank #16

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | POSITIONAL | ss1→flkL  |  cells: 7  |  total attr: +0.0685

**Key mass** (top-1=56%, top-2=85%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.0384 | 56.0% |
| 178 | other | +0.0197 | 28.8% |
| 55 | flkL | +0.0086 | 12.5% |
| 59 | ss1 | +0.0019 | 2.7% |

**Query mass** (top-1=46%, top-2=67%, top-3=77%)  [DISTR(A60/A185/M61)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0313 | 45.6% |
| 185 | ss2 | +0.0145 | 21.2% |
| 61 | ss1 | +0.0071 | 10.4% |
| 64 | ss1 | +0.0064 | 9.3% |
| 181 | ss2 | +0.0052 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 71%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 3 | 42.9% |
| +8 | 2 | 28.6% |
| +9 | 1 | 14.3% |
| +3 | 1 | 14.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 57.1% |
| ss2 | other | 2 | 28.6% |
| ss1 | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 53 | flkL | +0.0313 | 0.3039 |
| 185 | ss2 | 178 | other | +0.0145 | 0.0739 |
| 61 | ss1 | 53 | flkL | +0.0071 | 0.1011 |
| 64 | ss1 | 55 | flkL | +0.0064 | 0.1702 |
| 181 | ss2 | 178 | other | +0.0052 | 0.0827 |

### L26 H2 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 8  |  total attr: +0.0720

**Key mass** (top-1=75%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 80 | other | +0.0540 | 75.0% |
| 53 | flkL | +0.0102 | 14.2% |
| 73 | other | +0.0029 | 4.0% |
| 91 | other | +0.0028 | 3.9% |
| 77 | other | +0.0021 | 2.9% |

**Query mass** (top-1=59%, top-2=90%, top-3=96%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0425 | 59.1% |
| 57 | ss1 | +0.0223 | 31.0% |
| 61 | ss1 | +0.0043 | 6.0% |
| 66 | ss1 | +0.0029 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 1 | 12.5% |
| -23 | 1 | 12.5% |
| +7 | 1 | 12.5% |
| -7 | 1 | 12.5% |
| -31 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 75.0% |
| ss1 | flkL | 2 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 80 | other | +0.0300 | 0.1334 |
| 57 | ss1 | 80 | other | +0.0223 | 0.2860 |
| 60 | ss1 | 53 | flkL | +0.0076 | 0.0569 |
| 66 | ss1 | 73 | other | +0.0029 | 0.2278 |
| 60 | ss1 | 91 | other | +0.0028 | 0.0135 |

### L27 H15 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 6  |  total attr: +0.0168

**Key mass** (top-1=30%, top-2=48%, top-3=67%)  [DISTR(A181/A60/A64/S59)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss2 | +0.0051 | 30.2% |
| 60 | ss1 | +0.0031 | 18.3% |
| 64 | ss1 | +0.0030 | 18.1% |
| 59 | ss1 | +0.0020 | 11.7% |
| 178 | other | +0.0019 | 11.0% |

**Query mass** (top-1=30%, top-2=60%, top-3=78%)  [DISTR(A60/A181/A189)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0051 | 30.2% |
| 181 | ss2 | +0.0050 | 30.0% |
| 189 | ss2 | +0.0030 | 18.1% |
| 56 | flkL | +0.0019 | 11.0% |
| 61 | ss1 | +0.0018 | 10.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -121 | 1 | 16.7% |
| +121 | 1 | 16.7% |
| +125 | 1 | 16.7% |
| +122 | 1 | 16.7% |
| -122 | 1 | 16.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 50.0% |
| ss1 | ss2 | 1 | 16.7% |
| flkL | other | 1 | 16.7% |
| ss1 | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 181 | ss2 | +0.0051 | 0.0730 |
| 181 | ss2 | 60 | ss1 | +0.0031 | 0.0335 |
| 189 | ss2 | 64 | ss1 | +0.0030 | 0.0328 |
| 181 | ss2 | 59 | ss1 | +0.0020 | 0.0250 |
| 56 | flkL | 178 | other | +0.0019 | 0.0591 |

### L28 H5 — Rank #20

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | ss1→flkL  |  cells: 15  |  total attr: +0.0548

**Key mass** (top-1=34%, top-2=50%, top-3=58%)  [DISTR(L49/I48/G53/V54/F70)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 49 | flkL | +0.0189 | 34.5% |
| 48 | flkL | +0.0086 | 15.6% |
| 53 | flkL | +0.0044 | 8.1% |
| 54 | flkL | +0.0040 | 7.2% |
| 70 | other | +0.0038 | 6.9% |

**Query mass** (top-1=53%, top-2=74%, top-3=87%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0290 | 52.9% |
| 63 | ss1 | +0.0113 | 20.6% |
| 59 | ss1 | +0.0075 | 13.7% |
| 64 | ss1 | +0.0029 | 5.2% |
| 57 | ss1 | +0.0022 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 2 | 13.3% |
| -10 | 2 | 13.3% |
| -14 | 2 | 13.3% |
| +12 | 1 | 6.7% |
| +13 | 1 | 6.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 10 | 66.7% |
| ss1 | other | 4 | 26.7% |
| ss2 | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 61 | ss1 | 49 | flkL | +0.0150 | 0.1342 |
| 61 | ss1 | 48 | flkL | +0.0061 | 0.0455 |
| 61 | ss1 | 53 | flkL | +0.0044 | 0.0640 |
| 59 | ss1 | 70 | other | +0.0038 | 0.0827 |
| 61 | ss1 | 50 | flkL | +0.0035 | 0.0359 |

### L29 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 38  |  total attr: +0.2256

**Key mass** (top-1=11%, top-2=20%, top-3=29%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss2 | +0.0250 | 11.1% |
| 59 | ss1 | +0.0209 | 9.3% |
| 186 | ss2 | +0.0195 | 8.6% |
| 61 | ss1 | +0.0188 | 8.3% |
| 185 | ss2 | +0.0182 | 8.1% |

**Query mass** (top-1=12%, top-2=24%, top-3=35%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0272 | 12.1% |
| 185 | ss2 | +0.0260 | 11.5% |
| 182 | ss2 | +0.0259 | 11.5% |
| 59 | ss1 | +0.0250 | 11.1% |
| 63 | ss1 | +0.0237 | 10.5% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +123 | 3 | 7.9% |
| -123 | 3 | 7.9% |
| +124 | 3 | 7.9% |
| -124 | 3 | 7.9% |
| +126 | 3 | 7.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 28.9% |
| ss1 | ss2 | 10 | 26.3% |
| ss1 | flkR | 5 | 13.2% |
| ss1 | flkL | 5 | 13.2% |
| ss2 | other | 3 | 7.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 182 | ss2 | 59 | ss1 | +0.0209 | 0.2312 |
| 63 | ss1 | 186 | ss2 | +0.0195 | 0.1373 |
| 185 | ss2 | 61 | ss1 | +0.0188 | 0.1164 |
| 60 | ss1 | 181 | ss2 | +0.0175 | 0.2622 |
| 59 | ss1 | 182 | ss2 | +0.0164 | 0.2051 |

### L30 H1 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 7  |  total attr: +0.0319

**Key mass** (top-1=35%, top-2=57%, top-3=74%)  [DISTR(M61/A64/A186)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0113 | 35.5% |
| 64 | ss1 | +0.0069 | 21.6% |
| 186 | ss2 | +0.0053 | 16.6% |
| 60 | ss1 | +0.0037 | 11.8% |
| 48 | flkL | +0.0025 | 7.7% |

**Query mass** (top-1=46%, top-2=63%, top-3=75%)  [DISTR(A185/V63/A181)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0147 | 46.2% |
| 63 | ss1 | +0.0053 | 16.6% |
| 181 | ss2 | +0.0037 | 11.8% |
| 189 | ss2 | +0.0035 | 10.8% |
| 10 | flkL | +0.0025 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +121 | 2 | 28.6% |
| +124 | 1 | 14.3% |
| -123 | 1 | 14.3% |
| +125 | 1 | 14.3% |
| -38 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 57.1% |
| ss1 | ss2 | 2 | 28.6% |
| flkL | flkL | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 61 | ss1 | +0.0113 | 0.0618 |
| 63 | ss1 | 186 | ss2 | +0.0053 | 0.0381 |
| 181 | ss2 | 60 | ss1 | +0.0037 | 0.0824 |
| 189 | ss2 | 64 | ss1 | +0.0035 | 0.0356 |
| 185 | ss2 | 64 | ss1 | +0.0034 | 0.0611 |

### L31 H2 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss1  |  cells: 13  |  total attr: +0.0624

**Key mass** (top-1=53%, top-2=66%, top-3=74%)  [DISTR(L66/M61/T188)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 66 | ss1 | +0.0333 | 53.4% |
| 61 | ss1 | +0.0079 | 12.7% |
| 188 | ss2 | +0.0048 | 7.7% |
| 189 | ss2 | +0.0047 | 7.5% |
| 185 | ss2 | +0.0028 | 4.4% |

**Query mass** (top-1=37%, top-2=61%, top-3=72%)  [DISTR(V63/S59/M61)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0229 | 36.7% |
| 59 | ss1 | +0.0150 | 24.0% |
| 61 | ss1 | +0.0070 | 11.3% |
| 185 | ss2 | +0.0051 | 8.2% |
| 64 | ss1 | +0.0033 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 46%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 4 | 30.8% |
| -7 | 2 | 15.4% |
| +0 | 2 | 15.4% |
| +3 | 1 | 7.7% |
| -4 | 1 | 7.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 61.5% |
| ss2 | ss2 | 5 | 38.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 66 | ss1 | +0.0184 | 0.2893 |
| 59 | ss1 | 66 | ss1 | +0.0150 | 0.2443 |
| 61 | ss1 | 61 | ss1 | +0.0046 | 0.1040 |
| 64 | ss1 | 61 | ss1 | +0.0033 | 0.1543 |
| 185 | ss2 | 185 | ss2 | +0.0028 | 0.0228 |

### L31 H7 — Rank #30

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L32 H13 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 20  |  total attr: +0.3183

**Key mass** (top-1=21%, top-2=43%, top-3=56%)  [DISTR(V63/I182/S59/A186/A64)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0681 | 21.4% |
| 182 | ss2 | +0.0679 | 21.3% |
| 59 | ss1 | +0.0436 | 13.7% |
| 186 | ss2 | +0.0321 | 10.1% |
| 64 | ss1 | +0.0245 | 7.7% |

**Query mass** (top-1=21%, top-2=40%, top-3=54%)  [DISTR(S59/A186/I182/A185/V63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0667 | 20.9% |
| 186 | ss2 | +0.0619 | 19.5% |
| 182 | ss2 | +0.0427 | 13.4% |
| 185 | ss2 | +0.0395 | 12.4% |
| 63 | ss1 | +0.0365 | 11.5% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -123 | 2 | 10.0% |
| +123 | 2 | 10.0% |
| +125 | 2 | 10.0% |
| -125 | 2 | 10.0% |
| +121 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 55.0% |
| ss1 | ss2 | 9 | 45.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 59 | ss1 | 182 | ss2 | +0.0635 | 0.2463 |
| 186 | ss2 | 63 | ss1 | +0.0619 | 0.2736 |
| 182 | ss2 | 59 | ss1 | +0.0366 | 0.1418 |
| 63 | ss1 | 186 | ss2 | +0.0321 | 0.1419 |
| 185 | ss2 | 60 | ss1 | +0.0174 | 0.1574 |

### L32 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 15  |  total attr: +0.1092

**Key mass** (top-1=29%, top-2=53%, top-3=65%)  [DISTR(V63/I182/M61/A181)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0316 | 28.9% |
| 182 | ss2 | +0.0263 | 24.1% |
| 61 | ss1 | +0.0135 | 12.4% |
| 181 | ss2 | +0.0093 | 8.5% |
| 185 | ss2 | +0.0073 | 6.7% |

**Query mass** (top-1=21%, top-2=36%, top-3=50%)  [DISTR(I182/V63/S59/A185/A186)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 182 | ss2 | +0.0228 | 20.8% |
| 63 | ss1 | +0.0168 | 15.4% |
| 59 | ss1 | +0.0156 | 14.3% |
| 185 | ss2 | +0.0128 | 11.7% |
| 186 | ss2 | +0.0104 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -123 | 2 | 13.3% |
| +123 | 2 | 13.3% |
| -124 | 2 | 13.3% |
| +125 | 2 | 13.3% |
| +119 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 60.0% |
| ss1 | ss2 | 6 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 182 | ss2 | 63 | ss1 | +0.0174 | 0.1139 |
| 59 | ss1 | 182 | ss2 | +0.0156 | 0.0368 |
| 63 | ss1 | 182 | ss2 | +0.0107 | 0.0700 |
| 186 | ss2 | 63 | ss1 | +0.0104 | 0.0281 |
| 185 | ss2 | 61 | ss1 | +0.0088 | 0.0232 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #6 | L0 | H0 | 0 | +0.0000 | — |  | — |  |  |  |
| #2 | L5 | H7 | 16 | +0.3469 | SINGLE-ANCHOR | I7 | SINGLE-ANCHOR | N77 |  |  |
| #22 | L5 | H10 | 5 | +0.0192 | DUAL-ANCHOR | I9/I7 | SINGLE-ANCHOR | N77 |  |  |
| #17 | L7 | H13 | 2 | +0.0075 | SINGLE-ANCHOR | G8 | SINGLE-ANCHOR | L66 |  | ss1→flkL |
| #29 | L10 | H11 | 4 | +0.0154 | SINGLE-ANCHOR | N77 | SINGLE-ANCHOR | N77 |  |  |
| #7 | L12 | H3 | 14 | +0.0681 | SINGLE-ANCHOR | I76 | DISTRIBUTED | G53/K56/L49/S59/Q51 |  |  |
| #28 | L12 | H8 | 3 | +0.0097 | SINGLE-ANCHOR | I76 | DUAL-ANCHOR | E178/A186 |  |  |
| #4 | L12 | H15 | 23 | +0.2273 | SINGLE-ANCHOR | I76 | DISTRIBUTED |  |  |  |
| #10 | L13 | H18 | 18 | +0.0938 | SINGLE-ANCHOR | I76 | DISTRIBUTED |  |  |  |
| #18 | L14 | H8 | 9 | +0.0235 | DISTRIBUTED | A64/F70/V63/M58/L66 | DISTRIBUTED | M61/V67/V63 | POSITIONAL | INTRA:ss1 |
| #11 | L14 | H12 | 11 | +0.0427 | SINGLE-ANCHOR | I76 | DISTRIBUTED | L49/V63/M61/A64 |  | flkL→ss1 |
| #12 | L15 | H4 | 22 | +0.1276 | SINGLE-ANCHOR | S80 | DISTRIBUTED |  |  |  |
| #8 | L16 | H13 | 18 | +0.0752 | SINGLE-ANCHOR | S80 | DISTRIBUTED |  |  |  |
| #24 | L17 | H1 | 10 | +0.0438 | DUAL-ANCHOR | V196/I76 | DISTRIBUTED | V63/S80/V67/I76 |  |  |
| #26 | L18 | H17 | 11 | +0.0474 | DUAL-ANCHOR | I76/N77 | DISTRIBUTED | E178/A186/A181 |  |  |
| #25 | L19 | H18 | 4 | +0.0092 | SINGLE-ANCHOR | S80 | MULTI-ANCHOR |  |  |  |
| #14 | L21 | H13 | 11 | +0.0693 | DISTRIBUTED | V63/S59/T62 | DISTRIBUTED | A64/A60/L66/M61 | POSITIONAL | INTRA:ss1 |
| #15 | L22 | H8 | 12 | +0.0610 | DISTRIBUTED | V67/A72/K71 | DISTRIBUTED | V63/T62/A64/I65 | POSITIONAL | INTRA:ss1 |
| #21 | L23 | H5 | 6 | +0.0418 | SINGLE-ANCHOR | K44 | SINGLE-ANCHOR | A60 |  | ss1→flkL |
| #27 | L23 | H8 | 4 | +0.0598 | SINGLE-ANCHOR | G55 | SINGLE-ANCHOR | A60 |  | ss1→flkL |
| #16 | L24 | H8 | 7 | +0.0685 | DUAL-ANCHOR | G53/E178 | DISTRIBUTED | A60/A185/M61 | POSITIONAL | ss1→flkL |
| #19 | L26 | H2 | 8 | +0.0720 | SINGLE-ANCHOR | S80 | DUAL-ANCHOR | A60/V57 |  |  |
| #23 | L27 | H15 | 6 | +0.0168 | DISTRIBUTED | A181/A60/A64/S59 | DISTRIBUTED | A60/A181/A189 |  | CROSS:ss2→ss1 |
| #20 | L28 | H5 | 15 | +0.0548 | DISTRIBUTED | L49/I48/G53/V54/F70 | DUAL-ANCHOR | M61/V63 |  | ss1→flkL |
| #5 | L29 | H18 | 38 | +0.2256 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #9 | L30 | H1 | 7 | +0.0319 | DISTRIBUTED | M61/A64/A186 | DISTRIBUTED | A185/V63/A181 |  | CROSS:ss2→ss1 |
| #13 | L31 | H2 | 13 | +0.0624 | DISTRIBUTED | L66/M61/T188 | DISTRIBUTED | V63/S59/M61 |  | INTRA:ss1 |
| #30 | L31 | H7 | 0 | +0.0000 | — |  | — |  |  |  |
| #1 | L32 | H13 | 20 | +0.3183 | DISTRIBUTED | V63/I182/S59/A186/A64 | DISTRIBUTED | S59/A186/I182/A185/V63 |  | CROSS:ss2→ss1 |
| #3 | L32 | H18 | 15 | +0.1092 | DISTRIBUTED | V63/I182/M61/A181 | DISTRIBUTED | I182/V63/S59/A185/A186 |  | CROSS:ss2→ss1 |
