# Contact Pattern Analysis: 2XD3A

Generated: 2026-03-22 21:26:11   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2XD3A |
| Contact pair | (145, 280) |
| ss1 | [140, 151) |
| ss2 | [275, 286) |
| Clean flank | 54 |
| Corrupt flank | 53 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.8759 |
| Corrupt metric | 0.0131 |
| Gap | 0.8628 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 250 | 79.38% |
| positive IE | 95 | 78.54% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H13 | +0.2798 |
| 2 | L11 | H16 | +0.2315 |
| 3 | L17 | H10 | +0.2226 |
| 4 | L29 | H18 | +0.2002 |
| 5 | L32 | H18 | +0.1946 |
| 6 | L27 | H15 | +0.1878 |
| 7 | L26 | H16 | +0.1734 |
| 8 | L6 | H17 | +0.1161 |
| 9 | L16 | H9 | +0.0796 |
| 10 | L21 | H4 | +0.0749 |
| 11 | L13 | H18 | +0.0725 |
| 12 | L14 | H9 | +0.0687 |
| 13 | L12 | H16 | +0.0666 |
| 14 | L7 | H13 | +0.0650 |
| 15 | L10 | H2 | +0.0588 |
| 16 | L25 | H8 | +0.0520 |
| 17 | L21 | H6 | +0.0507 |
| 18 | L16 | H12 | +0.0481 |
| 19 | L13 | H19 | +0.0458 |
| 20 | L13 | H12 | +0.0448 |
| 21 | L23 | H18 | +0.0414 |
| 22 | L31 | H17 | +0.0404 |
| 23 | L12 | H2 | +0.0387 |
| 24 | L20 | H12 | +0.0375 |
| 25 | L15 | H4 | +0.0338 |
| 26 | L13 | H3 | +0.0331 |
| 27 | L14 | H18 | +0.0329 |
| 28 | L16 | H2 | +0.0324 |
| 29 | L23 | H8 | +0.0319 |
| 30 | L25 | H14 | +0.0316 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | -0.00% |
| 2 | -0.00% |
| 3 | -0.00% |
| 4 | 0.01% |
| 5 | 0.01% |
| 6 | 0.02% |
| 7 | 0.02% |
| 8 | 0.03% |
| 9 | 0.03% |
| 10 | 0.03% |
| 20 | 1.47% |
| 80 | 61.59% |
| 450 | 125.99% |

## Cell Attribution Analysis

Total cells: 15,589,005

- Positive: 7,817,449
- Negative: 7,766,905

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000027 | 1,558,902 |
| 95th | +0.00000093 | 779,451 |
| 99th | +0.00000852 | 155,891 |
| 99.5th | +0.00001922 | 77,946 |
| 99.9th | +0.00010327 | 15,590 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L17 | H10 | 147 | ss1 | 144 | ss1 | +0.104909 | 0.838120 |
| L13 | H18 | 144 | ss1 | 259 | other | +0.073983 | 0.393414 |
| L11 | H16 | 260 | other | 317 | flkR | +0.073333 | 0.145777 |
| L11 | H16 | 259 | other | 317 | flkR | +0.070657 | 0.182516 |
| L12 | H16 | 259 | other | -1 | other | +0.059464 | 0.341352 |
| L22 | H16 | 147 | ss1 | 144 | ss1 | +0.056269 | 0.525116 |
| L32 | H18 | 145 | ss1 | 278 | ss2 | +0.049909 | 0.277278 |
| L27 | H15 | 281 | ss2 | 144 | ss1 | +0.040904 | 0.280563 |
| L10 | H2 | 260 | other | 317 | flkR | +0.038725 | 0.043327 |
| L16 | H19 | 147 | ss1 | 260 | other | +0.036951 | 0.230558 |
| L10 | H2 | 259 | other | 317 | flkR | +0.036125 | 0.042893 |
| L14 | H9 | 280 | ss2 | 259 | other | +0.036065 | 0.162765 |
| L16 | H19 | 147 | ss1 | 259 | other | +0.035203 | 0.218156 |
| L14 | H18 | 144 | ss1 | 144 | ss1 | +0.033558 | 0.124382 |
| L16 | H12 | 147 | ss1 | 144 | ss1 | +0.031869 | 0.440142 |
| L16 | H9 | 144 | ss1 | 144 | ss1 | +0.031484 | 0.087918 |
| L12 | H2 | 144 | ss1 | 259 | other | +0.031217 | 0.186361 |
| L21 | H4 | 147 | ss1 | 144 | ss1 | +0.031019 | 0.329772 |
| L21 | H6 | 144 | ss1 | 147 | ss1 | +0.030504 | 0.308881 |
| L27 | H15 | 145 | ss1 | 279 | ss2 | +0.028516 | 0.226882 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L17 | H10 | 90 | flkL | 90 | flkL | -0.011007 | 0.552365 |
| L13 | H19 | 280 | ss2 | 259 | other | -0.011026 | 0.072186 |
| L13 | H18 | 146 | ss1 | 259 | other | -0.011112 | 0.391094 |
| L23 | H8 | 151 | other | 147 | ss1 | -0.011531 | 0.606210 |
| L13 | H18 | 279 | ss2 | 259 | other | -0.011729 | 0.336131 |
| L13 | H3 | 278 | ss2 | 260 | other | -0.011977 | 0.182180 |
| L16 | H10 | 147 | ss1 | 124 | flkL | -0.012201 | 0.274601 |
| L13 | H19 | 111 | flkL | 259 | other | -0.012821 | 0.242697 |
| L9 | H14 | 145 | ss1 | 94 | flkL | -0.013261 | 0.174239 |
| L20 | H5 | 130 | flkL | 144 | ss1 | -0.013758 | 0.486590 |
| L13 | H18 | 90 | flkL | 259 | other | -0.014688 | 0.235462 |
| L8 | H0 | 277 | ss2 | 87 | flkL | -0.016637 | 0.445634 |
| L13 | H18 | 145 | ss1 | 260 | other | -0.016652 | 0.186133 |
| L7 | H13 | 90 | flkL | 90 | flkL | -0.017197 | 0.188293 |
| L29 | H18 | 279 | ss2 | 148 | ss1 | -0.017476 | 0.710575 |
| L18 | H8 | 145 | ss1 | 147 | ss1 | -0.018450 | 0.496381 |
| L13 | H18 | 280 | ss2 | 260 | other | -0.021597 | 0.135421 |
| L13 | H18 | 280 | ss2 | 259 | other | -0.033681 | 0.211297 |
| L13 | H18 | 145 | ss1 | 259 | other | -0.037339 | 0.404088 |
| L18 | H13 | 147 | ss1 | 147 | ss1 | -0.136983 | 0.959306 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0131 | 0.00% |
| 10 | 10 | 9 | 0.0131 | 0.01% |
| 20 | 20 | 16 | 0.0132 | 0.02% |
| 50 | 50 | 28 | 0.0137 | 0.08% |
| 100 | 100 | 42 | 0.0148 | 0.21% |
| 200 | 200 | 58 | 0.0186 | 0.64% |
| 500 | 500 | 83 | 0.0492 | 4.20% |
| 1000 | 1,000 | 93 | 0.1230 | 12.75% |
| 2000 | 2,000 | 94 | 0.3399 | 37.88% |
| 5000 | 5,000 | 95 | 0.6489 | 73.69% |
| 10000 | 10,000 | 95 | 0.7827 | 89.21% |
| 20000 | 20,000 | 95 | 0.8988 | 102.66% |
| 50000 | 50,000 | 95 | 0.9574 | 109.45% |

## Motif Analysis

### L6 H17 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 32  |  total attr: +0.1333

**Key mass** (top-1=17%, top-2=29%, top-3=39%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 90 | flkL | +0.0220 | 16.5% |
| 135 | flkL | +0.0164 | 12.3% |
| 338 | flkR | +0.0135 | 10.1% |
| 294 | flkR | +0.0081 | 6.1% |
| 280 | ss2 | +0.0080 | 6.0% |

**Query mass** (top-1=17%, top-2=32%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 90 | flkL | +0.0220 | 16.5% |
| 281 | ss2 | +0.0204 | 15.3% |
| 135 | flkL | +0.0132 | 9.9% |
| 285 | ss2 | +0.0081 | 6.1% |
| 294 | flkR | +0.0078 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 34%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 9 | 28.1% |
| +20 | 2 | 6.2% |
| -3 | 2 | 6.2% |
| -53 | 1 | 3.1% |
| -41 | 1 | 3.1% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 21.9% |
| flkR | flkR | 7 | 21.9% |
| ss2 | flkR | 6 | 18.8% |
| ss2 | ss2 | 5 | 15.6% |
| ss2 | flkL | 2 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 90 | flkL | 90 | flkL | +0.0220 | 0.0925 |
| 135 | flkL | 135 | flkL | +0.0132 | 0.0510 |
| 285 | ss2 | 338 | flkR | +0.0081 | 0.0184 |
| 294 | flkR | 294 | flkR | +0.0055 | 0.0080 |
| 108 | flkL | 88 | flkL | +0.0050 | 0.1005 |

### L7 H13 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.0943

**Key mass** (top-1=13%, top-2=23%, top-3=31%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 335 | flkR | +0.0127 | 13.4% |
| 336 | flkR | +0.0088 | 9.3% |
| 135 | flkL | +0.0076 | 8.0% |
| 321 | flkR | +0.0070 | 7.5% |
| 323 | flkR | +0.0070 | 7.5% |

**Query mass** (top-1=22%, top-2=32%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 281 | ss2 | +0.0204 | 21.6% |
| 135 | flkL | +0.0098 | 10.4% |
| 282 | ss2 | +0.0076 | 8.1% |
| 89 | flkL | +0.0070 | 7.5% |
| 90 | flkL | +0.0064 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 16.1% |
| -41 | 3 | 9.7% |
| +35 | 2 | 6.5% |
| -246 | 1 | 3.2% |
| -53 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 10 | 32.3% |
| flkL | flkL | 8 | 25.8% |
| flkR | flkR | 4 | 12.9% |
| flkL | flkR | 2 | 6.5% |
| flkR | ss2 | 2 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 135 | flkL | 135 | flkL | +0.0076 | 0.0824 |
| 89 | flkL | 335 | flkR | +0.0070 | 0.0844 |
| 281 | ss2 | 322 | flkR | +0.0068 | 0.0050 |
| 280 | ss2 | 321 | flkR | +0.0050 | 0.0620 |
| 283 | ss2 | 336 | flkR | +0.0049 | 0.0931 |

### L10 H2 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 3  |  total attr: +0.0794

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 317 | flkR | +0.0794 | 100.0% |

**Query mass** (top-1=49%, top-2=94%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 260 | other | +0.0387 | 48.8% |
| 259 | other | +0.0361 | 45.5% |
| 258 | other | +0.0045 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -57 | 1 | 33.3% |
| -58 | 1 | 33.3% |
| -59 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 260 | other | 317 | flkR | +0.0387 | 0.0433 |
| 259 | other | 317 | flkR | +0.0361 | 0.0429 |
| 258 | other | 317 | flkR | +0.0045 | 0.0371 |

### L11 H16 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→flkR  |  cells: 20  |  total attr: +0.2130

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 317 | flkR | +0.2130 | 100.0% |

**Query mass** (top-1=34%, top-2=68%, top-3=76%)  [DISTR(A260/A259/M144)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 260 | other | +0.0733 | 34.4% |
| 259 | other | +0.0707 | 33.2% |
| 144 | ss1 | +0.0179 | 8.4% |
| 135 | flkL | +0.0081 | 3.8% |
| 151 | other | +0.0052 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -57 | 1 | 5.0% |
| -58 | 1 | 5.0% |
| -173 | 1 | 5.0% |
| -182 | 1 | 5.0% |
| -166 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:flkL→flkR]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 9 | 45.0% |
| ss1 | flkR | 4 | 20.0% |
| ss2 | flkR | 4 | 20.0% |
| other | flkR | 3 | 15.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 260 | other | 317 | flkR | +0.0733 | 0.1458 |
| 259 | other | 317 | flkR | +0.0707 | 0.1825 |
| 144 | ss1 | 317 | flkR | +0.0179 | 0.0832 |
| 135 | flkL | 317 | flkR | +0.0081 | 0.1468 |
| 151 | other | 317 | flkR | +0.0052 | 0.1600 |

### L12 H2 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.0754

**Key mass** (top-1=55%, top-2=73%, top-3=89%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0414 | 54.9% |
| 260 | other | +0.0137 | 18.2% |
| 415 | other | +0.0122 | 16.2% |
| 258 | other | +0.0046 | 6.1% |
| 261 | other | +0.0018 | 2.3% |

**Query mass** (top-1=67%, top-2=78%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0506 | 67.1% |
| 147 | ss1 | +0.0082 | 10.8% |
| 259 | other | +0.0081 | 10.7% |
| 260 | other | +0.0042 | 5.5% |
| 142 | ss1 | +0.0027 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 2 | 18.2% |
| -113 | 2 | 18.2% |
| -115 | 1 | 9.1% |
| -116 | 1 | 9.1% |
| -156 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=82%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 9 | 81.8% |
| other | other | 2 | 18.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | ss1 | 259 | other | +0.0312 | 0.1864 |
| 144 | ss1 | 260 | other | +0.0114 | 0.0779 |
| 259 | other | 415 | other | +0.0081 | 0.0498 |
| 147 | ss1 | 259 | other | +0.0058 | 0.1138 |
| 144 | ss1 | 258 | other | +0.0046 | 0.0354 |

### L12 H16 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0947

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0947 | 100.0% |

**Query mass** (top-1=63%, top-2=93%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0595 | 62.8% |
| 260 | other | +0.0283 | 29.8% |
| 276 | ss2 | +0.0050 | 5.2% |
| 279 | ss2 | +0.0020 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +260 | 1 | 25.0% |
| +261 | 1 | 25.0% |
| +277 | 1 | 25.0% |
| +280 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 2 | 50.0% |
| ss2 | other | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 259 | other | -1 | other | +0.0595 | 0.3414 |
| 260 | other | -1 | other | +0.0283 | 0.2858 |
| 276 | ss2 | -1 | other | +0.0050 | 0.0721 |
| 279 | ss2 | -1 | other | +0.0020 | 0.0932 |

### L13 H3 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 14  |  total attr: +0.0736

**Key mass** (top-1=47%, top-2=71%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 260 | other | +0.0344 | 46.8% |
| 259 | other | +0.0181 | 24.6% |
| 261 | other | +0.0118 | 16.1% |
| 258 | other | +0.0069 | 9.4% |
| 257 | other | +0.0023 | 3.2% |

**Query mass** (top-1=51%, top-2=83%, top-3=95%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0375 | 51.0% |
| 281 | ss2 | +0.0233 | 31.7% |
| 280 | ss2 | +0.0089 | 12.1% |
| 274 | other | +0.0020 | 2.7% |
| 282 | ss2 | +0.0019 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +21 | 2 | 14.3% |
| +22 | 2 | 14.3% |
| +20 | 2 | 14.3% |
| +19 | 2 | 14.3% |
| +16 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=93%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 13 | 92.9% |
| other | other | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 276 | ss2 | 260 | other | +0.0157 | 0.1109 |
| 281 | ss2 | 260 | other | +0.0101 | 0.1038 |
| 276 | ss2 | 259 | other | +0.0092 | 0.0690 |
| 281 | ss2 | 259 | other | +0.0069 | 0.0663 |
| 276 | ss2 | 261 | other | +0.0057 | 0.0433 |

### L13 H12 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0720

**Key mass** (top-1=58%, top-2=88%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0419 | 58.2% |
| 260 | other | +0.0213 | 29.6% |
| 317 | flkR | +0.0088 | 12.2% |

**Query mass** (top-1=24%, top-2=44%, top-3=58%)  [DISTR(M144/?-1/?416/K148)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0172 | 23.8% |
| -1 | other | +0.0146 | 20.3% |
| 416 | other | +0.0098 | 13.6% |
| 148 | ss1 | +0.0092 | 12.8% |
| 147 | ss1 | +0.0058 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 2 | 11.1% |
| -111 | 2 | 11.1% |
| -116 | 2 | 11.1% |
| -112 | 2 | 11.1% |
| +156 | 2 | 11.1% |

**Region-pair profile** (q→k)  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 11 | 61.1% |
| other | other | 5 | 27.8% |
| ss1 | flkR | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 259 | other | +0.0096 | 0.1701 |
| 144 | ss1 | 317 | flkR | +0.0068 | 0.0825 |
| 416 | other | 259 | other | +0.0067 | 0.1059 |
| 144 | ss1 | 259 | other | +0.0066 | 0.0311 |
| 148 | ss1 | 259 | other | +0.0055 | 0.0654 |

### L13 H18 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 65  |  total attr: +0.3487

**Key mass** (top-1=64%, top-2=91%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.2232 | 64.0% |
| 260 | other | +0.0950 | 27.2% |
| 317 | flkR | +0.0142 | 4.1% |
| 274 | other | +0.0075 | 2.2% |
| 258 | other | +0.0048 | 1.4% |

**Query mass** (top-1=32%, top-2=38%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.1112 | 31.9% |
| 281 | ss2 | +0.0215 | 6.2% |
| 276 | ss2 | +0.0198 | 5.7% |
| 148 | ss1 | +0.0176 | 5.0% |
| 88 | flkL | +0.0162 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 2 | 3.1% |
| -125 | 2 | 3.1% |
| +16 | 2 | 3.1% |
| -126 | 2 | 3.1% |
| +27 | 2 | 3.1% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 15 | 23.1% |
| flkR | other | 15 | 23.1% |
| other | other | 13 | 20.0% |
| ss1 | other | 10 | 15.4% |
| ss2 | other | 7 | 10.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | ss1 | 259 | other | +0.0740 | 0.3934 |
| 144 | ss1 | 260 | other | +0.0285 | 0.1599 |
| 276 | ss2 | 259 | other | +0.0139 | 0.2066 |
| 281 | ss2 | 259 | other | +0.0127 | 0.2757 |
| 148 | ss1 | 259 | other | +0.0109 | 0.1941 |

### L13 H19 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.1672

**Key mass** (top-1=56%, top-2=93%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0931 | 55.7% |
| 260 | other | +0.0619 | 37.0% |
| 415 | other | +0.0039 | 2.3% |
| 258 | other | +0.0037 | 2.2% |
| 261 | other | +0.0029 | 1.7% |

**Query mass** (top-1=32%, top-2=45%, top-3=55%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0530 | 31.7% |
| 147 | ss1 | +0.0216 | 12.9% |
| 145 | ss1 | +0.0179 | 10.7% |
| 148 | ss1 | +0.0145 | 8.7% |
| 88 | flkL | +0.0095 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 2 | 7.4% |
| -116 | 2 | 7.4% |
| -112 | 2 | 7.4% |
| -114 | 2 | 7.4% |
| -119 | 2 | 7.4% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 18 | 66.7% |
| flkL | other | 4 | 14.8% |
| other | other | 2 | 7.4% |
| ss2 | other | 2 | 7.4% |
| flkR | other | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | ss1 | 259 | other | +0.0282 | 0.2418 |
| 144 | ss1 | 260 | other | +0.0182 | 0.1641 |
| 147 | ss1 | 259 | other | +0.0113 | 0.2307 |
| 145 | ss1 | 259 | other | +0.0108 | 0.2120 |
| 147 | ss1 | 260 | other | +0.0103 | 0.2055 |

### L14 H9 — Rank #12

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.1105

**Key mass** (top-1=50%, top-2=73%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0548 | 49.6% |
| 260 | other | +0.0254 | 23.0% |
| 415 | other | +0.0191 | 17.3% |
| 280 | ss2 | +0.0069 | 6.3% |
| 258 | other | +0.0026 | 2.4% |

**Query mass** (top-1=56%, top-2=68%, top-3=77%)  [DISTR(V280/M144/Y145)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 280 | ss2 | +0.0617 | 55.9% |
| 144 | ss1 | +0.0138 | 12.5% |
| 145 | ss1 | +0.0093 | 8.4% |
| 147 | ss1 | +0.0077 | 6.9% |
| 111 | flkL | +0.0055 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -136 | 2 | 9.1% |
| -115 | 2 | 9.1% |
| +22 | 2 | 9.1% |
| +21 | 1 | 4.5% |
| +20 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 8 | 36.4% |
| ss2 | other | 6 | 27.3% |
| flkL | other | 4 | 18.2% |
| ss1 | ss2 | 1 | 4.5% |
| ss2 | ss2 | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 280 | ss2 | 259 | other | +0.0361 | 0.1628 |
| 280 | ss2 | 260 | other | +0.0180 | 0.0860 |
| 144 | ss1 | 415 | other | +0.0058 | 0.0576 |
| 147 | ss1 | 259 | other | +0.0053 | 0.0648 |
| 145 | ss1 | 259 | other | +0.0043 | 0.0659 |

### L14 H18 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 3  |  total attr: +0.0402

**Key mass** (top-1=84%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0336 | 83.6% |
| 132 | flkL | +0.0038 | 9.6% |
| 93 | flkL | +0.0028 | 6.9% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0402 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 33.3% |
| +12 | 1 | 33.3% |
| +51 | 1 | 33.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 66.7% |
| ss1 | ss1 | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | ss1 | 144 | ss1 | +0.0336 | 0.1244 |
| 144 | ss1 | 132 | flkL | +0.0038 | 0.0155 |
| 144 | ss1 | 93 | flkL | +0.0028 | 0.0117 |

### L15 H4 — Rank #25

**Tags:** k:MULTI-ANCHOR / q:MULTI-ANCHOR | CROSS:ss1→flkR  |  cells: 5  |  total attr: +0.0125

**Key mass** (top-1=54%, top-2=70%, top-3=86%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 317 | flkR | +0.0067 | 53.7% |
| 416 | other | +0.0020 | 16.2% |
| 259 | other | +0.0020 | 16.0% |
| 260 | other | +0.0018 | 14.2% |

**Query mass** (top-1=30%, top-2=60%, top-3=84%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0038 | 30.2% |
| 145 | ss1 | +0.0037 | 29.7% |
| 144 | ss1 | +0.0030 | 24.0% |
| 136 | flkL | +0.0020 | 16.2% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -172 | 1 | 20.0% |
| -173 | 1 | 20.0% |
| -280 | 1 | 20.0% |
| -260 | 1 | 20.0% |
| -261 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 2 | 40.0% |
| other | other | 2 | 40.0% |
| flkL | other | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 145 | ss1 | 317 | flkR | +0.0037 | 0.0338 |
| 144 | ss1 | 317 | flkR | +0.0030 | 0.0386 |
| 136 | flkL | 416 | other | +0.0020 | 0.1751 |
| -1 | other | 259 | other | +0.0020 | 0.0658 |
| -1 | other | 260 | other | +0.0018 | 0.0563 |

### L16 H2 — Rank #28

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.1079

**Key mass** (top-1=39%, top-2=76%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0423 | 39.2% |
| 260 | other | +0.0395 | 36.6% |
| 281 | ss2 | +0.0118 | 10.9% |
| 144 | ss1 | +0.0055 | 5.1% |
| 133 | flkL | +0.0020 | 1.9% |

**Query mass** (top-1=21%, top-2=38%, top-3=54%)  [DISTR(Y145/N147/V276/M144/V280)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 145 | ss1 | +0.0232 | 21.5% |
| 147 | ss1 | +0.0184 | 17.0% |
| 276 | ss2 | +0.0173 | 16.0% |
| 144 | ss1 | +0.0148 | 13.7% |
| 280 | ss2 | +0.0073 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 2 | 6.5% |
| +17 | 2 | 6.5% |
| +0 | 2 | 6.5% |
| -113 | 1 | 3.2% |
| -114 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 9 | 29.0% |
| ss1 | other | 8 | 25.8% |
| ss2 | ss2 | 3 | 9.7% |
| ss1 | ss1 | 3 | 9.7% |
| flkR | other | 3 | 9.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | ss1 | 260 | other | +0.0098 | 0.1718 |
| 145 | ss1 | 260 | other | +0.0097 | 0.1339 |
| 276 | ss2 | 259 | other | +0.0094 | 0.1795 |
| 145 | ss1 | 259 | other | +0.0086 | 0.1085 |
| 147 | ss1 | 259 | other | +0.0085 | 0.1442 |

### L16 H9 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.1578

**Key mass** (top-1=40%, top-2=79%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0633 | 40.1% |
| 280 | ss2 | +0.0607 | 38.5% |
| 135 | flkL | +0.0184 | 11.6% |
| 133 | flkL | +0.0060 | 3.8% |
| 301 | flkR | +0.0038 | 2.4% |

**Query mass** (top-1=35%, top-2=52%, top-3=58%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0559 | 35.4% |
| 276 | ss2 | +0.0259 | 16.4% |
| 278 | ss2 | +0.0097 | 6.1% |
| 140 | ss1 | +0.0075 | 4.8% |
| 281 | ss2 | +0.0070 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 3 | 13.6% |
| +0 | 2 | 9.1% |
| -2 | 2 | 9.1% |
| -5 | 2 | 9.1% |
| +3 | 2 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 8 | 36.4% |
| ss1 | ss1 | 4 | 18.2% |
| flkL | ss1 | 4 | 18.2% |
| ss1 | flkL | 2 | 9.1% |
| other | ss2 | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | ss1 | 144 | ss1 | +0.0315 | 0.0879 |
| 276 | ss2 | 280 | ss2 | +0.0259 | 0.3898 |
| 144 | ss1 | 135 | flkL | +0.0184 | 0.1385 |
| 278 | ss2 | 280 | ss2 | +0.0097 | 0.3709 |
| 140 | ss1 | 144 | ss1 | +0.0075 | 0.7595 |

### L16 H12 — Rank #18

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 15  |  total attr: +0.1007

**Key mass** (top-1=58%, top-2=77%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0584 | 58.0% |
| 280 | ss2 | +0.0194 | 19.2% |
| 147 | ss1 | +0.0100 | 9.9% |
| 145 | ss1 | +0.0044 | 4.4% |
| 146 | ss1 | +0.0037 | 3.7% |

**Query mass** (top-1=43%, top-2=57%, top-3=70%)  [DISTR(N147/Y145/A281/D149)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0429 | 42.7% |
| 145 | ss1 | +0.0142 | 14.2% |
| 281 | ss2 | +0.0129 | 12.8% |
| 149 | ss1 | +0.0101 | 10.0% |
| 148 | ss1 | +0.0091 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 53%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 4 | 26.7% |
| +2 | 4 | 26.7% |
| +3 | 3 | 20.0% |
| +4 | 1 | 6.7% |
| +5 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 66.7% |
| ss2 | ss2 | 4 | 26.7% |
| other | other | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | ss1 | 144 | ss1 | +0.0319 | 0.4401 |
| 145 | ss1 | 144 | ss1 | +0.0142 | 0.1892 |
| 281 | ss2 | 280 | ss2 | +0.0129 | 0.2824 |
| 148 | ss1 | 144 | ss1 | +0.0072 | 0.3369 |
| 149 | ss1 | 144 | ss1 | +0.0051 | 0.2106 |

### L17 H10 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.3024

**Key mass** (top-1=84%, top-2=92%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.2551 | 84.4% |
| 280 | ss2 | +0.0224 | 7.4% |
| 90 | flkL | +0.0194 | 6.4% |
| 89 | flkL | +0.0034 | 1.1% |
| 146 | ss1 | +0.0022 | 0.7% |

**Query mass** (top-1=35%, top-2=44%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.1071 | 35.4% |
| 148 | ss1 | +0.0257 | 8.5% |
| 145 | ss1 | +0.0228 | 7.6% |
| 144 | ss1 | +0.0173 | 5.7% |
| 138 | flkL | +0.0128 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 4 | 14.3% |
| -2 | 3 | 10.7% |
| -1 | 3 | 10.7% |
| -3 | 3 | 10.7% |
| +3 | 2 | 7.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 35.7% |
| flkL | ss1 | 8 | 28.6% |
| flkL | flkL | 6 | 21.4% |
| ss2 | ss2 | 4 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | ss1 | 144 | ss1 | +0.1049 | 0.8381 |
| 148 | ss1 | 144 | ss1 | +0.0257 | 0.8258 |
| 145 | ss1 | 144 | ss1 | +0.0228 | 0.6381 |
| 144 | ss1 | 144 | ss1 | +0.0173 | 0.7255 |
| 138 | flkL | 144 | ss1 | +0.0128 | 0.7841 |

### L20 H12 — Rank #24

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.0383

**Key mass** (top-1=43%, top-2=66%, top-3=79%)  [DISTR(A260/M90/A259)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 260 | other | +0.0164 | 42.8% |
| 90 | flkL | +0.0088 | 22.9% |
| 259 | other | +0.0051 | 13.4% |
| 124 | flkL | +0.0023 | 6.0% |
| 89 | flkL | +0.0022 | 5.7% |

**Query mass** (top-1=18%, top-2=34%, top-3=49%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0068 | 17.7% |
| 145 | ss1 | +0.0062 | 16.3% |
| 281 | ss2 | +0.0059 | 15.4% |
| 282 | ss2 | +0.0046 | 11.9% |
| 108 | flkL | +0.0028 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 41%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 4 | 23.5% |
| +21 | 3 | 17.6% |
| +22 | 2 | 11.8% |
| +16 | 1 | 5.9% |
| +56 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 9 | 52.9% |
| flkL | flkL | 4 | 23.5% |
| ss1 | flkL | 3 | 17.6% |
| other | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 281 | ss2 | 260 | other | +0.0040 | 0.3163 |
| 276 | ss2 | 260 | other | +0.0034 | 0.1467 |
| 282 | ss2 | 260 | other | +0.0029 | 0.3340 |
| 108 | flkL | 90 | flkL | +0.0028 | 0.6516 |
| 145 | ss1 | 124 | flkL | +0.0023 | 0.1611 |

### L21 H4 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 14  |  total attr: +0.1069

**Key mass** (top-1=91%, top-2=94%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0970 | 90.7% |
| 145 | ss1 | +0.0038 | 3.5% |
| 280 | ss2 | +0.0027 | 2.5% |
| 90 | flkL | +0.0020 | 1.8% |
| 89 | flkL | +0.0016 | 1.5% |

**Query mass** (top-1=33%, top-2=54%, top-3=63%)  [DISTR(N147/M144/Y145/I139)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0348 | 32.5% |
| 144 | ss1 | +0.0226 | 21.1% |
| 145 | ss1 | +0.0104 | 9.7% |
| 139 | flkL | +0.0085 | 8.0% |
| 143 | ss1 | +0.0069 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 3 | 21.4% |
| +1 | 2 | 14.3% |
| +3 | 1 | 7.1% |
| +0 | 1 | 7.1% |
| -5 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 42.9% |
| flkL | ss1 | 4 | 28.6% |
| flkL | flkL | 2 | 14.3% |
| other | ss1 | 1 | 7.1% |
| ss2 | ss2 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | ss1 | 144 | ss1 | +0.0310 | 0.3298 |
| 144 | ss1 | 144 | ss1 | +0.0226 | 0.3507 |
| 145 | ss1 | 144 | ss1 | +0.0104 | 0.6814 |
| 139 | flkL | 144 | ss1 | +0.0085 | 0.5348 |
| 143 | ss1 | 144 | ss1 | +0.0069 | 0.6497 |

### L21 H6 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 17  |  total attr: +0.0866

**Key mass** (top-1=56%, top-2=76%, top-3=88%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0484 | 55.9% |
| 144 | ss1 | +0.0177 | 20.4% |
| 142 | ss1 | +0.0100 | 11.6% |
| 280 | ss2 | +0.0088 | 10.2% |
| 149 | ss1 | +0.0017 | 2.0% |

**Query mass** (top-1=35%, top-2=51%, top-3=60%)  [DISTR(M144/N147/Y146/A281/E140)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0305 | 35.2% |
| 147 | ss1 | +0.0140 | 16.2% |
| 146 | ss1 | +0.0072 | 8.3% |
| 281 | ss2 | +0.0053 | 6.2% |
| 140 | ss1 | +0.0052 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 11.8% |
| +5 | 2 | 11.8% |
| -1 | 2 | 11.8% |
| +0 | 2 | 11.8% |
| -4 | 2 | 11.8% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=65%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 64.7% |
| ss2 | ss2 | 2 | 11.8% |
| flkL | ss1 | 2 | 11.8% |
| other | ss1 | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 144 | ss1 | 147 | ss1 | +0.0305 | 0.3089 |
| 147 | ss1 | 142 | ss1 | +0.0080 | 0.3792 |
| 146 | ss1 | 147 | ss1 | +0.0072 | 0.5654 |
| 147 | ss1 | 147 | ss1 | +0.0061 | 0.1945 |
| 281 | ss2 | 280 | ss2 | +0.0053 | 0.2797 |

### L23 H8 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 12  |  total attr: +0.0567

**Key mass** (top-1=78%, top-2=86%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0443 | 78.2% |
| 263 | other | +0.0046 | 8.1% |
| 135 | flkL | +0.0031 | 5.5% |
| 145 | ss1 | +0.0030 | 5.3% |
| 133 | flkL | +0.0017 | 2.9% |

**Query mass** (top-1=20%, top-2=39%, top-3=57%)  [DISTR(D149/Y145/K148/N147)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | ss1 | +0.0113 | 20.0% |
| 145 | ss1 | +0.0108 | 19.0% |
| 148 | ss1 | +0.0104 | 18.3% |
| 147 | ss1 | +0.0082 | 14.5% |
| 267 | other | +0.0046 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 3 | 25.0% |
| +1 | 1 | 8.3% |
| +5 | 1 | 8.3% |
| +3 | 1 | 8.3% |
| -4 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 58.3% |
| ss1 | flkL | 3 | 25.0% |
| other | other | 1 | 8.3% |
| flkL | ss1 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 148 | ss1 | 144 | ss1 | +0.0104 | 0.4265 |
| 145 | ss1 | 144 | ss1 | +0.0092 | 0.2068 |
| 149 | ss1 | 144 | ss1 | +0.0084 | 0.3231 |
| 147 | ss1 | 144 | ss1 | +0.0067 | 0.6037 |
| 267 | other | 263 | other | +0.0046 | 0.5633 |

### L23 H18 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 11  |  total attr: +0.0527

**Key mass** (top-1=79%, top-2=90%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0416 | 79.0% |
| 140 | ss1 | +0.0058 | 11.0% |
| 147 | ss1 | +0.0033 | 6.2% |
| 141 | ss1 | +0.0020 | 3.8% |

**Query mass** (top-1=24%, top-2=41%, top-3=56%)  [DISTR(N147/K148/D149/V151/A154)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0127 | 24.1% |
| 148 | ss1 | +0.0090 | 17.2% |
| 149 | ss1 | +0.0078 | 14.8% |
| 151 | other | +0.0067 | 12.8% |
| 154 | other | +0.0053 | 10.1% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 2 | 18.2% |
| +4 | 1 | 9.1% |
| +5 | 1 | 9.1% |
| +10 | 1 | 9.1% |
| +3 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 54.5% |
| other | ss1 | 5 | 45.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 148 | ss1 | 144 | ss1 | +0.0090 | 0.4115 |
| 149 | ss1 | 144 | ss1 | +0.0078 | 0.4021 |
| 151 | other | 144 | ss1 | +0.0067 | 0.3245 |
| 147 | ss1 | 140 | ss1 | +0.0058 | 0.1223 |
| 154 | other | 144 | ss1 | +0.0053 | 0.4960 |

### L25 H8 — Rank #16

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | POSITIONAL | INTRA:ss1  |  cells: 15  |  total attr: +0.0785

**Key mass** (top-1=47%, top-2=65%, top-3=76%)  [DISTR(M144/V143/N147)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0366 | 46.6% |
| 143 | ss1 | +0.0142 | 18.0% |
| 147 | ss1 | +0.0088 | 11.2% |
| 140 | ss1 | +0.0045 | 5.7% |
| 145 | ss1 | +0.0035 | 4.4% |

**Query mass** (top-1=33%, top-2=66%, top-3=85%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | ss1 | +0.0260 | 33.1% |
| 148 | ss1 | +0.0258 | 32.8% |
| 147 | ss1 | +0.0151 | 19.3% |
| 276 | ss2 | +0.0030 | 3.8% |
| 144 | ss1 | +0.0023 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 53%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 4 | 26.7% |
| +3 | 4 | 26.7% |
| +5 | 3 | 20.0% |
| +1 | 1 | 6.7% |
| +2 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 73.3% |
| ss2 | ss2 | 2 | 13.3% |
| ss2 | other | 1 | 6.7% |
| ss1 | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 149 | ss1 | 144 | ss1 | +0.0186 | 0.3139 |
| 148 | ss1 | 144 | ss1 | +0.0135 | 0.1606 |
| 147 | ss1 | 143 | ss1 | +0.0085 | 0.2270 |
| 148 | ss1 | 143 | ss1 | +0.0056 | 0.1621 |
| 148 | ss1 | 147 | ss1 | +0.0049 | 0.0736 |

### L25 H14 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0342

**Key mass** (top-1=45%, top-2=63%, top-3=78%)  [DISTR(A259/A260/M144)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | other | +0.0155 | 45.3% |
| 260 | other | +0.0062 | 18.2% |
| 144 | ss1 | +0.0051 | 15.0% |
| 258 | other | +0.0040 | 11.7% |
| 281 | ss2 | +0.0034 | 9.8% |

**Query mass** (top-1=33%, top-2=64%, top-3=74%)  [DISTR(N277/Y278/V276)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 277 | ss2 | +0.0111 | 32.5% |
| 278 | ss2 | +0.0107 | 31.3% |
| 276 | ss2 | +0.0034 | 9.8% |
| 135 | flkL | +0.0028 | 8.3% |
| 137 | flkL | +0.0023 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +19 | 2 | 18.2% |
| +18 | 2 | 18.2% |
| +20 | 2 | 18.2% |
| -5 | 1 | 9.1% |
| +17 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 8 | 72.7% |
| flkL | ss1 | 2 | 18.2% |
| ss2 | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 278 | ss2 | 259 | other | +0.0060 | 0.3200 |
| 277 | ss2 | 259 | other | +0.0056 | 0.3186 |
| 276 | ss2 | 281 | ss2 | +0.0034 | 0.0977 |
| 278 | ss2 | 260 | other | +0.0032 | 0.2000 |
| 277 | ss2 | 260 | other | +0.0030 | 0.1575 |

### L26 H16 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 19  |  total attr: +0.1069

**Key mass** (top-1=26%, top-2=52%, top-3=62%)  [DISTR(N147/N277/A281/K148)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0278 | 26.0% |
| 277 | ss2 | +0.0273 | 25.5% |
| 281 | ss2 | +0.0108 | 10.1% |
| 148 | ss1 | +0.0092 | 8.6% |
| 149 | ss1 | +0.0068 | 6.4% |

**Query mass** (top-1=31%, top-2=46%, top-3=59%)  [DISTR(V276/K148/Y145/N277/M144)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0336 | 31.5% |
| 148 | ss1 | +0.0159 | 14.9% |
| 145 | ss1 | +0.0131 | 12.2% |
| 277 | ss2 | +0.0120 | 11.2% |
| 144 | ss1 | +0.0102 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +129 | 2 | 10.5% |
| -129 | 2 | 10.5% |
| +128 | 2 | 10.5% |
| -128 | 1 | 5.3% |
| -137 | 1 | 5.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 10 | 52.6% |
| ss2 | ss1 | 8 | 42.1% |
| ss2 | flkR | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 276 | ss2 | 147 | ss1 | +0.0255 | 0.1461 |
| 148 | ss1 | 277 | ss2 | +0.0159 | 0.2786 |
| 149 | ss1 | 277 | ss2 | +0.0098 | 0.2380 |
| 144 | ss1 | 281 | ss2 | +0.0083 | 0.0561 |
| 147 | ss1 | 276 | ss2 | +0.0062 | 0.0579 |

### L27 H15 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 16  |  total attr: +0.1427

**Key mass** (top-1=30%, top-2=58%, top-3=77%)  [DISTR(M144/G279/N277)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 144 | ss1 | +0.0424 | 29.7% |
| 279 | ss2 | +0.0399 | 28.0% |
| 277 | ss2 | +0.0276 | 19.3% |
| 148 | ss1 | +0.0063 | 4.4% |
| 147 | ss1 | +0.0062 | 4.3% |

**Query mass** (top-1=29%, top-2=51%, top-3=64%)  [DISTR(A281/Y145/K148/Y146)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 281 | ss2 | +0.0409 | 28.7% |
| 145 | ss1 | +0.0322 | 22.6% |
| 148 | ss1 | +0.0186 | 13.1% |
| 146 | ss1 | +0.0114 | 8.0% |
| 277 | ss2 | +0.0100 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +129 | 2 | 12.5% |
| +133 | 2 | 12.5% |
| +137 | 1 | 6.2% |
| -134 | 1 | 6.2% |
| -129 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 50.0% |
| ss1 | ss2 | 7 | 43.8% |
| ss1 | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 281 | ss2 | 144 | ss1 | +0.0409 | 0.2806 |
| 145 | ss1 | 279 | ss2 | +0.0285 | 0.2269 |
| 148 | ss1 | 277 | ss2 | +0.0186 | 0.2542 |
| 146 | ss1 | 279 | ss2 | +0.0114 | 0.8353 |
| 277 | ss2 | 148 | ss1 | +0.0063 | 0.0985 |

### L29 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 18  |  total attr: +0.1407

**Key mass** (top-1=22%, top-2=39%, top-3=55%)  [DISTR(D149/N147/V276/N277/Y278)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | ss1 | +0.0314 | 22.3% |
| 147 | ss1 | +0.0239 | 17.0% |
| 276 | ss2 | +0.0221 | 15.7% |
| 277 | ss2 | +0.0122 | 8.7% |
| 278 | ss2 | +0.0101 | 7.2% |

**Query mass** (top-1=31%, top-2=52%, top-3=68%)  [DISTR(V276/N147/N277/Y145)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0432 | 30.7% |
| 147 | ss1 | +0.0305 | 21.6% |
| 277 | ss2 | +0.0214 | 15.2% |
| 145 | ss1 | +0.0180 | 12.8% |
| 149 | ss1 | +0.0140 | 9.9% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -131 | 2 | 11.1% |
| -135 | 2 | 11.1% |
| +129 | 1 | 5.6% |
| +128 | 1 | 5.6% |
| -129 | 1 | 5.6% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 44.4% |
| ss2 | ss1 | 5 | 27.8% |
| ss1 | flkR | 3 | 16.7% |
| ss1 | other | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 276 | ss2 | 147 | ss1 | +0.0239 | 0.1199 |
| 277 | ss2 | 149 | ss1 | +0.0214 | 0.2415 |
| 147 | ss1 | 276 | ss2 | +0.0203 | 0.2205 |
| 149 | ss1 | 277 | ss2 | +0.0122 | 0.2375 |
| 147 | ss1 | 278 | ss2 | +0.0101 | 0.1708 |

### L31 H17 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 8  |  total attr: +0.0479

**Key mass** (top-1=70%, top-2=84%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0335 | 70.1% |
| 276 | ss2 | +0.0065 | 13.6% |
| 147 | ss1 | +0.0061 | 12.7% |
| 416 | other | +0.0017 | 3.7% |

**Query mass** (top-1=55%, top-2=68%, top-3=79%)  [DISTR(N147/V276/Y145)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0265 | 55.3% |
| 276 | ss2 | +0.0061 | 12.7% |
| 145 | ss1 | +0.0051 | 10.7% |
| 149 | ss1 | +0.0037 | 7.7% |
| 144 | ss1 | +0.0036 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +148 | 1 | 12.5% |
| -129 | 1 | 12.5% |
| +129 | 1 | 12.5% |
| +146 | 1 | 12.5% |
| +150 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 75.0% |
| ss1 | ss2 | 1 | 12.5% |
| ss2 | ss1 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 147 | ss1 | -1 | other | +0.0182 | 0.2727 |
| 147 | ss1 | 276 | ss2 | +0.0065 | 0.0606 |
| 276 | ss2 | 147 | ss1 | +0.0061 | 0.0853 |
| 145 | ss1 | -1 | other | +0.0051 | 0.2094 |
| 149 | ss1 | -1 | other | +0.0037 | 0.2434 |

### L32 H13 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 16  |  total attr: +0.1440

**Key mass** (top-1=21%, top-2=38%, top-3=53%)  [DISTR(N147/N277/V276/M144/D149)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 147 | ss1 | +0.0296 | 20.6% |
| 277 | ss2 | +0.0248 | 17.2% |
| 276 | ss2 | +0.0217 | 15.1% |
| 144 | ss1 | +0.0164 | 11.4% |
| 149 | ss1 | +0.0155 | 10.8% |

**Query mass** (top-1=19%, top-2=37%, top-3=53%)  [DISTR(V276/N147/N277/A281/D149)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 276 | ss2 | +0.0275 | 19.1% |
| 147 | ss1 | +0.0252 | 17.5% |
| 277 | ss2 | +0.0233 | 16.1% |
| 281 | ss2 | +0.0201 | 14.0% |
| 149 | ss1 | +0.0140 | 9.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +129 | 2 | 12.5% |
| -129 | 2 | 12.5% |
| +135 | 2 | 12.5% |
| +137 | 1 | 6.2% |
| +128 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 56.2% |
| ss1 | ss2 | 7 | 43.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 276 | ss2 | 147 | ss1 | +0.0275 | 0.1326 |
| 147 | ss1 | 276 | ss2 | +0.0217 | 0.1047 |
| 281 | ss2 | 144 | ss1 | +0.0164 | 0.0827 |
| 277 | ss2 | 149 | ss1 | +0.0155 | 0.2722 |
| 149 | ss1 | 277 | ss2 | +0.0140 | 0.2457 |

### L32 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 17  |  total attr: +0.1843

**Key mass** (top-1=27%, top-2=49%, top-3=60%)  [DISTR(Y278/Y145/M144/V276/A281)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 278 | ss2 | +0.0499 | 27.1% |
| 145 | ss1 | +0.0400 | 21.7% |
| 144 | ss1 | +0.0206 | 11.2% |
| 276 | ss2 | +0.0176 | 9.6% |
| 281 | ss2 | +0.0152 | 8.3% |

**Query mass** (top-1=33%, top-2=48%, top-3=60%)  [DISTR(Y145/G279/A281/N147)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 145 | ss1 | +0.0617 | 33.5% |
| 279 | ss2 | +0.0259 | 14.0% |
| 281 | ss2 | +0.0228 | 12.4% |
| 147 | ss1 | +0.0192 | 10.4% |
| 144 | ss1 | +0.0136 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -129 | 2 | 11.8% |
| +129 | 2 | 11.8% |
| +135 | 2 | 11.8% |
| -135 | 2 | 11.8% |
| -133 | 1 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 52.9% |
| ss2 | ss1 | 8 | 47.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 145 | ss1 | 278 | ss2 | +0.0499 | 0.2773 |
| 279 | ss2 | 145 | ss1 | +0.0259 | 0.1176 |
| 281 | ss2 | 144 | ss1 | +0.0206 | 0.0633 |
| 147 | ss1 | 276 | ss2 | +0.0176 | 0.0519 |
| 144 | ss1 | 281 | ss2 | +0.0136 | 0.0418 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #8 | L6 | H17 | 32 | +0.1333 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #14 | L7 | H13 | 31 | +0.0943 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #15 | L10 | H2 | 3 | +0.0794 | SINGLE-ANCHOR | V317 | DUAL-ANCHOR | A260/A259 |  |  |
| #2 | L11 | H16 | 20 | +0.2130 | SINGLE-ANCHOR | V317 | DISTRIBUTED | A260/A259/M144 |  | CROSS:flkL→flkR |
| #23 | L12 | H2 | 11 | +0.0754 | DUAL-ANCHOR | A259/A260 | SINGLE-ANCHOR | M144 |  |  |
| #13 | L12 | H16 | 4 | +0.0947 | SINGLE-ANCHOR | ?-1 | SINGLE-ANCHOR | A259 |  |  |
| #26 | L13 | H3 | 14 | +0.0736 | DUAL-ANCHOR | A260/A259 | DUAL-ANCHOR | V276/A281 |  |  |
| #20 | L13 | H12 | 18 | +0.0720 | DUAL-ANCHOR | A259/A260 | DISTRIBUTED | M144/?-1/?416/K148 |  |  |
| #11 | L13 | H18 | 65 | +0.3487 | SINGLE-ANCHOR | A259 | DISTRIBUTED |  |  |  |
| #19 | L13 | H19 | 27 | +0.1672 | DUAL-ANCHOR | A259/A260 | DISTRIBUTED |  |  |  |
| #12 | L14 | H9 | 22 | +0.1105 | DUAL-ANCHOR | A259/A260 | DISTRIBUTED | V280/M144/Y145 |  |  |
| #27 | L14 | H18 | 3 | +0.0402 | SINGLE-ANCHOR | M144 | SINGLE-ANCHOR | M144 |  | ss1→flkL |
| #25 | L15 | H4 | 5 | +0.0125 | MULTI-ANCHOR |  | MULTI-ANCHOR |  |  | CROSS:ss1→flkR |
| #28 | L16 | H2 | 31 | +0.1079 | DUAL-ANCHOR | A259/A260 | DISTRIBUTED | Y145/N147/V276/M144/V280 |  |  |
| #9 | L16 | H9 | 22 | +0.1578 | DUAL-ANCHOR | M144/V280 | DISTRIBUTED |  |  |  |
| #18 | L16 | H12 | 15 | +0.1007 | DUAL-ANCHOR | M144/V280 | DISTRIBUTED | N147/Y145/A281/D149 | POSITIONAL | INTRA:ss1 |
| #3 | L17 | H10 | 28 | +0.3024 | SINGLE-ANCHOR | M144 | DISTRIBUTED |  |  |  |
| #24 | L20 | H12 | 17 | +0.0383 | DISTRIBUTED | A260/M90/A259 | DISTRIBUTED |  |  |  |
| #10 | L21 | H4 | 14 | +0.1069 | SINGLE-ANCHOR | M144 | DISTRIBUTED | N147/M144/Y145/I139 |  | INTRA:ss1 |
| #17 | L21 | H6 | 17 | +0.0866 | DUAL-ANCHOR | N147/M144 | DISTRIBUTED | M144/N147/Y146/A281/E140 |  | INTRA:ss1 |
| #29 | L23 | H8 | 12 | +0.0567 | SINGLE-ANCHOR | M144 | DISTRIBUTED | D149/Y145/K148/N147 |  | INTRA:ss1 |
| #21 | L23 | H18 | 11 | +0.0527 | SINGLE-ANCHOR | M144 | DISTRIBUTED | N147/K148/D149/V151/A154 |  | INTRA:ss1 |
| #16 | L25 | H8 | 15 | +0.0785 | DISTRIBUTED | M144/V143/N147 | MULTI-ANCHOR |  | POSITIONAL | INTRA:ss1 |
| #30 | L25 | H14 | 11 | +0.0342 | DISTRIBUTED | A259/A260/M144 | DISTRIBUTED | N277/Y278/V276 |  |  |
| #7 | L26 | H16 | 19 | +0.1069 | DISTRIBUTED | N147/N277/A281/K148 | DISTRIBUTED | V276/K148/Y145/N277/M144 |  | CROSS:ss1→ss2 |
| #6 | L27 | H15 | 16 | +0.1427 | DISTRIBUTED | M144/G279/N277 | DISTRIBUTED | A281/Y145/K148/Y146 |  | CROSS:ss2→ss1 |
| #4 | L29 | H18 | 18 | +0.1407 | DISTRIBUTED | D149/N147/V276/N277/Y278 | DISTRIBUTED | V276/N147/N277/Y145 |  | CROSS:ss1→ss2 |
| #22 | L31 | H17 | 8 | +0.0479 | SINGLE-ANCHOR | ?-1 | DISTRIBUTED | N147/V276/Y145 |  |  |
| #1 | L32 | H13 | 16 | +0.1440 | DISTRIBUTED | N147/N277/V276/M144/D149 | DISTRIBUTED | V276/N147/N277/A281/D149 |  | CROSS:ss2→ss1 |
| #5 | L32 | H18 | 17 | +0.1843 | DISTRIBUTED | Y278/Y145/M144/V276/A281 | DISTRIBUTED | Y145/G279/A281/N147 |  | CROSS:ss1→ss2 |
