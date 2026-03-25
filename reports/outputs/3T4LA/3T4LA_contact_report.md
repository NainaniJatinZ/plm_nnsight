# Contact Pattern Analysis: 3T4LA

Generated: 2026-03-22 21:46:51   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3T4LA |
| Contact pair | (78, 195) |
| ss1 | [73, 84) |
| ss2 | [190, 201) |
| Clean flank | 56 |
| Corrupt flank | 55 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 1.0758 |
| Corrupt metric | 0.4087 |
| Gap | 0.6671 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 130 | 86.51% |
| positive IE | 140 | 71.90% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L8 | H0 | +0.4547 |
| 2 | L9 | H14 | +0.3499 |
| 3 | L32 | H13 | +0.1865 |
| 4 | L32 | H18 | +0.0940 |
| 5 | L22 | H14 | +0.0569 |
| 6 | L13 | H8 | +0.0483 |
| 7 | L29 | H18 | +0.0303 |
| 8 | L6 | H17 | +0.0265 |
| 9 | L13 | H18 | +0.0259 |
| 10 | L17 | H1 | +0.0230 |
| 11 | L12 | H15 | +0.0225 |
| 12 | L3 | H1 | +0.0193 |
| 13 | L30 | H1 | +0.0190 |
| 14 | L30 | H0 | +0.0170 |
| 15 | L15 | H8 | +0.0141 |
| 16 | L11 | H18 | +0.0139 |
| 17 | L10 | H7 | +0.0133 |
| 18 | L21 | H13 | +0.0128 |
| 19 | L12 | H17 | +0.0120 |
| 20 | L6 | H11 | +0.0109 |
| 21 | L1 | H13 | +0.0106 |
| 22 | L9 | H8 | +0.0102 |
| 23 | L15 | H1 | +0.0100 |
| 24 | L14 | H3 | +0.0099 |
| 25 | L26 | H16 | +0.0099 |
| 26 | L16 | H1 | +0.0099 |
| 27 | L31 | H17 | +0.0098 |
| 28 | L12 | H2 | +0.0095 |
| 29 | L10 | H15 | +0.0095 |
| 30 | L30 | H13 | +0.0094 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 1.01% |
| 4 | 1.85% |
| 5 | 2.21% |
| 6 | 2.36% |
| 7 | 2.02% |
| 8 | 1.91% |
| 9 | 2.17% |
| 10 | 2.75% |
| 20 | 5.35% |
| 80 | 31.10% |
| 450 | 102.48% |

## Cell Attribution Analysis

Total cells: 9,462,377

- Positive: 4,796,547
- Negative: 4,659,362

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000036 | 946,239 |
| 95th | +0.00000107 | 473,121 |
| 99th | +0.00000737 | 94,625 |
| 99.5th | +0.00001491 | 47,313 |
| 99.9th | +0.00006777 | 9,463 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L8 | H0 | 18 | flkL | 18 | flkL | +0.039986 | 0.646095 |
| L12 | H2 | -1 | other | 193 | ss2 | +0.034757 | 0.437763 |
| L12 | H17 | 75 | ss1 | 193 | ss2 | +0.030109 | 0.255774 |
| L15 | H8 | 75 | ss1 | 193 | ss2 | +0.027708 | 0.176582 |
| L9 | H14 | 75 | ss1 | 217 | flkR | +0.025882 | 0.205696 |
| L14 | H3 | 75 | ss1 | 27 | flkL | +0.023481 | 0.081834 |
| L13 | H18 | 75 | ss1 | 193 | ss2 | +0.022803 | 0.118428 |
| L21 | H13 | 74 | ss1 | 75 | ss1 | +0.020103 | 0.242167 |
| L14 | H16 | 75 | ss1 | -1 | other | +0.018715 | 0.145255 |
| L9 | H14 | 17 | flkL | 17 | flkL | +0.018019 | 0.471287 |
| L18 | H1 | 75 | ss1 | 193 | ss2 | +0.017806 | 0.195418 |
| L13 | H8 | -1 | other | 193 | ss2 | +0.016609 | 0.109133 |
| L22 | H14 | 74 | ss1 | 194 | ss2 | +0.016521 | 0.138571 |
| L8 | H0 | 38 | flkL | 38 | flkL | +0.016312 | 0.207411 |
| L13 | H16 | 75 | ss1 | 193 | ss2 | +0.016133 | 0.137392 |
| L12 | H15 | 74 | ss1 | 193 | ss2 | +0.015751 | 0.446660 |
| L8 | H0 | 206 | flkR | 18 | flkL | +0.014956 | 0.306576 |
| L13 | H8 | 75 | ss1 | 193 | ss2 | +0.014920 | 0.103122 |
| L12 | H15 | 75 | ss1 | 193 | ss2 | +0.014696 | 0.354495 |
| L9 | H14 | 206 | flkR | 18 | flkL | +0.013681 | 0.475392 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L12 | H15 | 77 | ss1 | 193 | ss2 | -0.005828 | 0.359958 |
| L9 | H14 | 217 | flkR | 31 | flkL | -0.005836 | 0.242440 |
| L8 | H0 | 254 | flkR | 25 | flkL | -0.005846 | 0.163534 |
| L18 | H14 | 74 | ss1 | 270 | other | -0.006086 | 0.209721 |
| L16 | H19 | 91 | other | 193 | ss2 | -0.006295 | 0.131012 |
| L8 | H0 | 18 | flkL | 206 | flkR | -0.006375 | 0.050869 |
| L12 | H17 | 77 | ss1 | 193 | ss2 | -0.006406 | 0.258657 |
| L13 | H12 | 194 | ss2 | 270 | other | -0.006471 | 0.311303 |
| L9 | H14 | 27 | flkL | 256 | flkR | -0.007277 | 0.128576 |
| L8 | H0 | 72 | flkL | 193 | ss2 | -0.008251 | 0.063718 |
| L13 | H12 | 75 | ss1 | 270 | other | -0.008634 | 0.134111 |
| L12 | H2 | 27 | flkL | 193 | ss2 | -0.008706 | 0.103802 |
| L18 | H1 | 37 | flkL | 193 | ss2 | -0.009326 | 0.198388 |
| L11 | H18 | 27 | flkL | 27 | flkL | -0.011172 | 0.187059 |
| L18 | H1 | 77 | ss1 | 193 | ss2 | -0.011282 | 0.191697 |
| L11 | H18 | 70 | flkL | 70 | flkL | -0.012649 | 0.184773 |
| L13 | H8 | 37 | flkL | 193 | ss2 | -0.013935 | 0.102304 |
| L14 | H3 | 75 | ss1 | -1 | other | -0.013975 | 0.090646 |
| L11 | H18 | 193 | ss2 | 18 | flkL | -0.016519 | 0.660697 |
| L12 | H17 | 37 | flkL | 193 | ss2 | -0.018617 | 0.308020 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.4087 | 0.00% |
| 10 | 10 | 9 | 0.4087 | 0.00% |
| 20 | 20 | 14 | 0.4095 | 0.13% |
| 50 | 50 | 28 | 0.4113 | 0.40% |
| 100 | 100 | 56 | 0.4144 | 0.86% |
| 200 | 200 | 81 | 0.4187 | 1.50% |
| 500 | 500 | 118 | 0.4317 | 3.45% |
| 1000 | 1,000 | 132 | 0.4294 | 3.12% |
| 2000 | 2,000 | 137 | 0.4910 | 12.34% |
| 5000 | 5,000 | 139 | 0.5384 | 19.45% |
| 10000 | 10,000 | 140 | 0.5714 | 24.39% |
| 20000 | 20,000 | 140 | 0.6284 | 32.94% |
| 50000 | 50,000 | 140 | 0.6753 | 39.97% |

## Motif Analysis

### L1 H13 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 10  |  total attr: +0.0116

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 256 | flkR | +0.0116 | 100.0% |

**Query mass** (top-1=23%, top-2=41%, top-3=58%)  [DISTR(D251/G253/L193/K249/S243)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 251 | flkR | +0.0027 | 23.2% |
| 253 | flkR | +0.0021 | 17.6% |
| 193 | ss2 | +0.0020 | 16.8% |
| 249 | flkR | +0.0011 | 9.8% |
| 243 | flkR | +0.0009 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 1 | 10.0% |
| -3 | 1 | 10.0% |
| -63 | 1 | 10.0% |
| -7 | 1 | 10.0% |
| -13 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=90%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 9 | 90.0% |
| ss2 | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 251 | flkR | 256 | flkR | +0.0027 | 0.1560 |
| 253 | flkR | 256 | flkR | +0.0021 | 0.1670 |
| 193 | ss2 | 256 | flkR | +0.0020 | 0.0080 |
| 249 | flkR | 256 | flkR | +0.0011 | 0.1250 |
| 243 | flkR | 256 | flkR | +0.0009 | 0.0898 |

### L3 H1 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 10  |  total attr: +0.0075

**Key mass** (top-1=73%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | flkL | +0.0055 | 73.5% |
| 256 | flkR | +0.0015 | 19.6% |
| 254 | flkR | +0.0005 | 6.9% |

**Query mass** (top-1=16%, top-2=28%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.0012 | 15.8% |
| 16 | other | +0.0009 | 11.9% |
| 253 | flkR | +0.0008 | 10.5% |
| 41 | flkL | +0.0008 | 10.4% |
| 37 | flkL | +0.0008 | 10.1% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +22 | 1 | 10.0% |
| -1 | 1 | 10.0% |
| -3 | 1 | 10.0% |
| +24 | 1 | 10.0% |
| +20 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 50.0% |
| other | flkL | 2 | 20.0% |
| flkR | flkR | 2 | 20.0% |
| ss2 | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 39 | flkL | 17 | flkL | +0.0012 | 0.0175 |
| 16 | other | 17 | flkL | +0.0009 | 0.0372 |
| 253 | flkR | 256 | flkR | +0.0008 | 0.0500 |
| 41 | flkL | 17 | flkL | +0.0008 | 0.0228 |
| 37 | flkL | 17 | flkL | +0.0008 | 0.0161 |

### L6 H11 — Rank #20

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L6 H17 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0289

**Key mass** (top-1=31%, top-2=49%, top-3=60%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 254 | flkR | +0.0090 | 31.3% |
| 255 | flkR | +0.0051 | 17.7% |
| 37 | flkL | +0.0033 | 11.3% |
| 26 | flkL | +0.0013 | 4.4% |
| 256 | flkR | +0.0010 | 3.5% |

**Query mass** (top-1=31%, top-2=49%, top-3=60%)  [DISTR(Y192/Q236/L37/Q18/L23)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 192 | ss2 | +0.0090 | 31.3% |
| 236 | flkR | +0.0051 | 17.7% |
| 37 | flkL | +0.0031 | 10.6% |
| 18 | flkL | +0.0026 | 9.0% |
| 23 | flkL | +0.0011 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 14.3% |
| +12 | 2 | 9.5% |
| -21 | 2 | 9.5% |
| +8 | 2 | 9.5% |
| -62 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 6 | 28.6% |
| flkR | flkR | 5 | 23.8% |
| flkL | other | 4 | 19.0% |
| ss2 | flkR | 2 | 9.5% |
| ss1 | flkL | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 192 | ss2 | 254 | flkR | +0.0090 | 0.0718 |
| 236 | flkR | 255 | flkR | +0.0051 | 0.1057 |
| 37 | flkL | 37 | flkL | +0.0022 | 0.0255 |
| 18 | flkL | 26 | flkL | +0.0013 | 0.0226 |
| 75 | ss1 | 37 | flkL | +0.0011 | 0.0129 |

### L8 H0 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 38  |  total attr: +0.1234

**Key mass** (top-1=47%, top-2=61%, top-3=72%)  [DISTR(Q18/A38/V75)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 18 | flkL | +0.0585 | 47.4% |
| 38 | flkL | +0.0173 | 14.0% |
| 75 | ss1 | +0.0136 | 11.0% |
| 17 | flkL | +0.0081 | 6.6% |
| 37 | flkL | +0.0033 | 2.7% |

**Query mass** (top-1=32%, top-2=46%, top-3=58%)  [DISTR(Q18/A38/V217/L206)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 18 | flkL | +0.0400 | 32.4% |
| 38 | flkL | +0.0163 | 13.2% |
| 217 | flkR | +0.0153 | 12.4% |
| 206 | flkR | +0.0150 | 12.1% |
| 17 | flkL | +0.0080 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 34%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 11 | 28.9% |
| +188 | 2 | 5.3% |
| -142 | 2 | 5.3% |
| +142 | 1 | 2.6% |
| +163 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 10 | 26.3% |
| flkL | flkL | 8 | 21.1% |
| ss2 | flkL | 6 | 15.8% |
| flkR | ss1 | 2 | 5.3% |
| flkR | flkR | 2 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 18 | flkL | 18 | flkL | +0.0400 | 0.6461 |
| 38 | flkL | 38 | flkL | +0.0163 | 0.2074 |
| 206 | flkR | 18 | flkL | +0.0150 | 0.3066 |
| 217 | flkR | 75 | ss1 | +0.0125 | 0.1180 |
| 17 | flkL | 17 | flkL | +0.0075 | 0.3888 |

### L9 H8 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | ss2→flkR  |  cells: 8  |  total attr: +0.0095

**Key mass** (top-1=62%, top-2=77%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | flkL | +0.0059 | 62.5% |
| 254 | flkR | +0.0013 | 14.2% |
| 247 | flkR | +0.0009 | 9.8% |
| 241 | flkR | +0.0007 | 7.4% |
| 225 | flkR | +0.0006 | 6.2% |

**Query mass** (top-1=38%, top-2=65%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0036 | 37.5% |
| 75 | ss1 | +0.0026 | 27.8% |
| -1 | other | +0.0016 | 16.4% |
| 34 | flkL | +0.0013 | 13.2% |
| 205 | flkR | +0.0005 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +58 | 1 | 12.5% |
| -18 | 1 | 12.5% |
| -61 | 1 | 12.5% |
| +17 | 1 | 12.5% |
| -54 | 1 | 12.5% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 50.0% |
| ss1 | flkL | 1 | 12.5% |
| other | flkL | 1 | 12.5% |
| flkL | flkL | 1 | 12.5% |
| flkR | flkL | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 17 | flkL | +0.0026 | 0.0265 |
| -1 | other | 17 | flkL | +0.0016 | 0.0445 |
| 193 | ss2 | 254 | flkR | +0.0013 | 0.0114 |
| 34 | flkL | 17 | flkL | +0.0013 | 0.0508 |
| 193 | ss2 | 247 | flkR | +0.0009 | 0.0049 |

### L9 H14 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 42  |  total attr: +0.1273

**Key mass** (top-1=21%, top-2=39%, top-3=53%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | flkR | +0.0268 | 21.1% |
| 17 | flkL | +0.0232 | 18.2% |
| 18 | flkL | +0.0175 | 13.8% |
| 38 | flkL | +0.0091 | 7.1% |
| 72 | flkL | +0.0076 | 6.0% |

**Query mass** (top-1=20%, top-2=38%, top-3=52%)  [DISTR(V75/L193/D17/L206/A38)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0259 | 20.3% |
| 193 | ss2 | +0.0221 | 17.3% |
| 17 | flkL | +0.0180 | 14.2% |
| 206 | flkR | +0.0149 | 11.7% |
| 38 | flkL | +0.0091 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 7 | 16.7% |
| +171 | 2 | 4.8% |
| +196 | 2 | 4.8% |
| +170 | 2 | 4.8% |
| +179 | 2 | 4.8% |

**Region-pair profile** (q→k)  (top=14%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 6 | 14.3% |
| ss2 | flkL | 6 | 14.3% |
| ss2 | other | 5 | 11.9% |
| flkL | flkL | 4 | 9.5% |
| flkL | flkR | 4 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 217 | flkR | +0.0259 | 0.2057 |
| 17 | flkL | 17 | flkL | +0.0180 | 0.4713 |
| 206 | flkR | 18 | flkL | +0.0137 | 0.4754 |
| 38 | flkL | 38 | flkL | +0.0091 | 0.2446 |
| 193 | ss2 | 72 | flkL | +0.0076 | 0.0431 |

### L10 H7 — Rank #17

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 6  |  total attr: +0.0068

**Key mass** (top-1=49%, top-2=63%, top-3=74%)  [DISTR(V199/Q236/D237)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0034 | 49.4% |
| 236 | flkR | +0.0009 | 13.3% |
| 237 | flkR | +0.0008 | 11.1% |
| 78 | ss1 | +0.0007 | 10.0% |
| 247 | flkR | +0.0006 | 8.3% |

**Query mass** (top-1=90%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0061 | 90.0% |
| 27 | flkL | +0.0007 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 1 | 16.7% |
| -43 | 1 | 16.7% |
| -44 | 1 | 16.7% |
| -51 | 1 | 16.7% |
| -54 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 66.7% |
| ss2 | ss2 | 1 | 16.7% |
| flkL | ss1 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss2 | 199 | ss2 | +0.0034 | 0.0225 |
| 193 | ss2 | 236 | flkR | +0.0009 | 0.0075 |
| 193 | ss2 | 237 | flkR | +0.0008 | 0.0038 |
| 27 | flkL | 78 | ss1 | +0.0007 | 0.0111 |
| 193 | ss2 | 247 | flkR | +0.0006 | 0.0038 |

### L10 H15 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 2  |  total attr: +0.0070

**Key mass** (top-1=71%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 205 | flkR | +0.0050 | 71.4% |
| 206 | flkR | +0.0020 | 28.6% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0070 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -12 | 1 | 50.0% |
| -13 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss2 | 205 | flkR | +0.0050 | 0.0542 |
| 193 | ss2 | 206 | flkR | +0.0020 | 0.0213 |

### L11 H18 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.0238

**Key mass** (top-1=13%, top-2=24%, top-3=33%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | flkR | +0.0031 | 13.0% |
| 191 | ss2 | +0.0027 | 11.3% |
| 0 | other | +0.0022 | 9.1% |
| 270 | other | +0.0017 | 7.3% |
| 247 | flkR | +0.0015 | 6.4% |

**Query mass** (top-1=16%, top-2=28%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0039 | 16.4% |
| 70 | flkL | +0.0027 | 11.3% |
| 40 | flkL | +0.0023 | 9.5% |
| 74 | ss1 | +0.0020 | 8.6% |
| 75 | ss1 | +0.0015 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -139 | 2 | 8.7% |
| +0 | 2 | 8.7% |
| -121 | 1 | 4.3% |
| +193 | 1 | 4.3% |
| -166 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 6 | 26.1% |
| flkL | ss2 | 4 | 17.4% |
| ss1 | flkR | 4 | 17.4% |
| ss2 | other | 3 | 13.0% |
| flkR | flkL | 2 | 8.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 70 | flkL | 191 | ss2 | +0.0027 | 0.2032 |
| 193 | ss2 | 0 | other | +0.0022 | 0.1129 |
| 40 | flkL | 206 | flkR | +0.0018 | 0.1209 |
| 193 | ss2 | 270 | other | +0.0017 | 0.1610 |
| 75 | ss1 | 247 | flkR | +0.0015 | 0.1115 |

### L12 H2 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 26  |  total attr: +0.0619

**Key mass** (top-1=95%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0590 | 95.3% |
| 216 | flkR | +0.0020 | 3.2% |
| 218 | flkR | +0.0009 | 1.4% |

**Query mass** (top-1=56%, top-2=69%, top-3=73%)  [DISTR(?-1/L37/F27)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0348 | 56.2% |
| 37 | flkL | +0.0079 | 12.8% |
| 27 | flkL | +0.0024 | 3.8% |
| 29 | flkL | +0.0021 | 3.4% |
| 19 | flkL | +0.0012 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -189 | 2 | 7.7% |
| -191 | 2 | 7.7% |
| -175 | 2 | 7.7% |
| -194 | 1 | 3.8% |
| -156 | 1 | 3.8% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 11 | 42.3% |
| other | ss2 | 9 | 34.6% |
| flkL | flkR | 3 | 11.5% |
| ss1 | ss2 | 3 | 11.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 193 | ss2 | +0.0348 | 0.4378 |
| 37 | flkL | 193 | ss2 | +0.0079 | 0.0954 |
| 29 | flkL | 193 | ss2 | +0.0021 | 0.1330 |
| 27 | flkL | 216 | flkR | +0.0015 | 0.0371 |
| 19 | flkL | 193 | ss2 | +0.0012 | 0.1787 |

### L12 H15 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 23  |  total attr: +0.0607

**Key mass** (top-1=98%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0595 | 98.1% |
| 53 | flkL | +0.0006 | 1.0% |
| 216 | flkR | +0.0006 | 1.0% |

**Query mass** (top-1=27%, top-2=51%, top-3=59%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | ss1 | +0.0163 | 26.9% |
| 75 | ss1 | +0.0147 | 24.2% |
| 66 | flkL | +0.0047 | 7.8% |
| 65 | flkL | +0.0034 | 5.6% |
| 85 | other | +0.0031 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 1 | 4.3% |
| -118 | 1 | 4.3% |
| -127 | 1 | 4.3% |
| -128 | 1 | 4.3% |
| -108 | 1 | 4.3% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=48%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 11 | 47.8% |
| ss1 | ss2 | 6 | 26.1% |
| other | ss2 | 4 | 17.4% |
| flkL | flkL | 1 | 4.3% |
| ss1 | flkR | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | ss1 | 193 | ss2 | +0.0158 | 0.4467 |
| 75 | ss1 | 193 | ss2 | +0.0147 | 0.3545 |
| 66 | flkL | 193 | ss2 | +0.0047 | 0.3074 |
| 65 | flkL | 193 | ss2 | +0.0034 | 0.2924 |
| 85 | other | 193 | ss2 | +0.0031 | 0.2616 |

### L12 H17 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 26  |  total attr: +0.0668

**Key mass** (top-1=89%, top-2=94%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0596 | 89.2% |
| 216 | flkR | +0.0029 | 4.4% |
| 37 | flkL | +0.0010 | 1.5% |
| 78 | ss1 | +0.0008 | 1.2% |
| 218 | flkR | +0.0008 | 1.1% |

**Query mass** (top-1=54%, top-2=68%, top-3=73%)  [DISTR(V75/F27/L193)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0360 | 54.0% |
| 27 | flkL | +0.0096 | 14.4% |
| 193 | ss2 | +0.0029 | 4.4% |
| 76 | ss1 | +0.0026 | 3.9% |
| 44 | flkL | +0.0020 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 3.8% |
| -166 | 1 | 3.8% |
| +0 | 1 | 3.8% |
| -117 | 1 | 3.8% |
| -141 | 1 | 3.8% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 11 | 42.3% |
| ss1 | flkR | 3 | 11.5% |
| other | ss2 | 3 | 11.5% |
| ss1 | ss2 | 2 | 7.7% |
| ss2 | ss2 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 193 | ss2 | +0.0301 | 0.2558 |
| 27 | flkL | 193 | ss2 | +0.0090 | 0.3014 |
| 193 | ss2 | 193 | ss2 | +0.0029 | 0.0477 |
| 76 | ss1 | 193 | ss2 | +0.0026 | 0.2908 |
| 75 | ss1 | 216 | flkR | +0.0022 | 0.0192 |

### L13 H8 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR  |  cells: 16  |  total attr: +0.0487

**Key mass** (top-1=93%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0455 | 93.4% |
| 270 | other | +0.0032 | 6.6% |

**Query mass** (top-1=35%, top-2=69%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0170 | 34.9% |
| -1 | other | +0.0166 | 34.1% |
| 27 | flkL | +0.0061 | 12.5% |
| 74 | ss1 | +0.0019 | 4.0% |
| 16 | other | +0.0012 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -194 | 1 | 6.2% |
| -118 | 1 | 6.2% |
| -166 | 1 | 6.2% |
| -195 | 1 | 6.2% |
| -119 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 31.2% |
| other | ss2 | 4 | 25.0% |
| flkL | ss2 | 4 | 25.0% |
| ss1 | other | 2 | 12.5% |
| flkL | other | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 193 | ss2 | +0.0166 | 0.1091 |
| 75 | ss1 | 193 | ss2 | +0.0149 | 0.1031 |
| 27 | flkL | 193 | ss2 | +0.0056 | 0.0251 |
| 75 | ss1 | 270 | other | +0.0021 | 0.0376 |
| 74 | ss1 | 193 | ss2 | +0.0013 | 0.0415 |

### L13 H18 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0293

**Key mass** (top-1=96%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0280 | 95.8% |
| -1 | other | +0.0006 | 2.2% |
| 218 | flkR | +0.0006 | 2.0% |

**Query mass** (top-1=80%, top-2=89%, top-3=92%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0234 | 79.9% |
| 74 | ss1 | +0.0026 | 8.8% |
| 195 | ss2 | +0.0008 | 2.8% |
| 37 | flkL | +0.0006 | 2.2% |
| 78 | ss1 | +0.0006 | 2.1% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 12.5% |
| -119 | 1 | 12.5% |
| +2 | 1 | 12.5% |
| +38 | 1 | 12.5% |
| -115 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 50.0% |
| ss2 | ss2 | 1 | 12.5% |
| flkL | other | 1 | 12.5% |
| flkL | ss2 | 1 | 12.5% |
| ss1 | flkR | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 193 | ss2 | +0.0228 | 0.1184 |
| 74 | ss1 | 193 | ss2 | +0.0026 | 0.1365 |
| 195 | ss2 | 193 | ss2 | +0.0008 | 0.0514 |
| 37 | flkL | -1 | other | +0.0006 | 0.0266 |
| 78 | ss1 | 193 | ss2 | +0.0006 | 0.0915 |

### L14 H3 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 14  |  total attr: +0.0413

**Key mass** (top-1=60%, top-2=84%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 27 | flkL | +0.0249 | 60.3% |
| -1 | other | +0.0100 | 24.2% |
| 193 | ss2 | +0.0033 | 7.9% |
| 23 | flkL | +0.0024 | 5.9% |
| 30 | flkL | +0.0007 | 1.7% |

**Query mass** (top-1=64%, top-2=73%, top-3=82%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0266 | 64.5% |
| 193 | ss2 | +0.0036 | 8.8% |
| 37 | flkL | +0.0036 | 8.8% |
| 92 | other | +0.0025 | 6.1% |
| 91 | other | +0.0009 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +48 | 1 | 7.1% |
| +38 | 1 | 7.1% |
| +0 | 1 | 7.1% |
| +93 | 1 | 7.1% |
| +52 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 5 | 35.7% |
| ss1 | flkL | 3 | 21.4% |
| flkL | other | 1 | 7.1% |
| ss2 | ss2 | 1 | 7.1% |
| ss2 | other | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 27 | flkL | +0.0235 | 0.0818 |
| 37 | flkL | -1 | other | +0.0036 | 0.0625 |
| 193 | ss2 | 193 | ss2 | +0.0026 | 0.0536 |
| 92 | other | -1 | other | +0.0025 | 0.1030 |
| 75 | ss1 | 23 | flkL | +0.0024 | 0.0098 |

### L15 H1 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 7  |  total attr: +0.0098

**Key mass** (top-1=82%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0080 | 82.3% |
| -1 | other | +0.0010 | 10.2% |
| 269 | other | +0.0007 | 7.5% |

**Query mass** (top-1=56%, top-2=66%, top-3=75%)  [DISTR(L193/?-1/G194)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0054 | 55.6% |
| -1 | other | +0.0010 | 10.2% |
| 194 | ss2 | +0.0009 | 8.8% |
| 75 | ss1 | +0.0007 | 7.5% |
| 269 | other | +0.0007 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +118 | 1 | 14.3% |
| +0 | 1 | 14.3% |
| +119 | 1 | 14.3% |
| -194 | 1 | 14.3% |
| +194 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 57.1% |
| other | other | 1 | 14.3% |
| ss1 | other | 1 | 14.3% |
| other | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss2 | 75 | ss1 | +0.0054 | 0.1743 |
| -1 | other | -1 | other | +0.0010 | 0.1736 |
| 194 | ss2 | 75 | ss1 | +0.0009 | 0.1115 |
| 75 | ss1 | 269 | other | +0.0007 | 0.0195 |
| 269 | other | 75 | ss1 | +0.0007 | 0.0869 |

### L15 H8 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS_SSE | CROSS:ss1→ss2  |  cells: 3  |  total attr: +0.0292

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0292 | 100.0% |

**Query mass** (top-1=95%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0277 | 95.0% |
| 27 | flkL | +0.0008 | 2.6% |
| 79 | ss1 | +0.0007 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 33.3% |
| -166 | 1 | 33.3% |
| -114 | 1 | 33.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 2 | 66.7% |
| flkL | ss2 | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 193 | ss2 | +0.0277 | 0.1766 |
| 27 | flkL | 193 | ss2 | +0.0008 | 0.0624 |
| 79 | ss1 | 193 | ss2 | +0.0007 | 0.0430 |

### L16 H1 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 11  |  total attr: +0.0176

**Key mass** (top-1=82%, top-2=87%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0145 | 82.5% |
| 63 | flkL | +0.0009 | 4.9% |
| 96 | other | +0.0008 | 4.6% |
| 27 | flkL | +0.0008 | 4.6% |
| 90 | other | +0.0006 | 3.4% |

**Query mass** (top-1=44%, top-2=59%, top-3=72%)  [DISTR(L37/T62/V75)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 37 | flkL | +0.0078 | 44.4% |
| 62 | flkL | +0.0025 | 14.3% |
| 75 | ss1 | +0.0023 | 13.0% |
| 65 | flkL | +0.0022 | 12.4% |
| 63 | flkL | +0.0009 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -15 | 2 | 18.2% |
| -38 | 1 | 9.1% |
| -13 | 1 | 9.1% |
| -10 | 1 | 9.1% |
| -12 | 1 | 9.1% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 7 | 63.6% |
| ss1 | other | 2 | 18.2% |
| ss1 | flkL | 1 | 9.1% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 37 | flkL | 75 | ss1 | +0.0070 | 0.0662 |
| 62 | flkL | 75 | ss1 | +0.0025 | 0.2519 |
| 65 | flkL | 75 | ss1 | +0.0022 | 0.1788 |
| 63 | flkL | 75 | ss1 | +0.0009 | 0.2394 |
| 75 | ss1 | 63 | flkL | +0.0009 | 0.0470 |

### L17 H1 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0315

**Key mass** (top-1=86%, top-2=91%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss2 | +0.0271 | 85.8% |
| 96 | other | +0.0017 | 5.3% |
| 75 | ss1 | +0.0015 | 4.8% |
| 87 | other | +0.0007 | 2.1% |
| 88 | other | +0.0006 | 2.0% |

**Query mass** (top-1=16%, top-2=31%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | other | +0.0052 | 16.5% |
| 91 | other | +0.0047 | 14.8% |
| 92 | other | +0.0038 | 11.9% |
| 77 | ss1 | +0.0032 | 10.1% |
| 90 | other | +0.0023 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -13 | 2 | 11.1% |
| -102 | 1 | 5.6% |
| -108 | 1 | 5.6% |
| -101 | 1 | 5.6% |
| -116 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 10 | 55.6% |
| ss1 | other | 3 | 16.7% |
| ss1 | ss2 | 2 | 11.1% |
| flkL | ss2 | 1 | 5.6% |
| flkL | ss1 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 91 | other | 193 | ss2 | +0.0047 | 0.2067 |
| 85 | other | 193 | ss2 | +0.0043 | 0.1316 |
| 92 | other | 193 | ss2 | +0.0038 | 0.2721 |
| 77 | ss1 | 193 | ss2 | +0.0024 | 0.0861 |
| 90 | other | 193 | ss2 | +0.0023 | 0.2183 |

### L21 H13 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 4  |  total attr: +0.0224

**Key mass** (top-1=90%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | ss1 | +0.0201 | 89.7% |
| 77 | ss1 | +0.0010 | 4.3% |
| 79 | ss1 | +0.0008 | 3.8% |
| 23 | flkL | +0.0005 | 2.2% |

**Query mass** (top-1=90%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | ss1 | +0.0201 | 89.7% |
| 78 | ss1 | +0.0010 | 4.3% |
| 80 | ss1 | +0.0008 | 3.8% |
| 23 | flkL | +0.0005 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 50.0% |
| -1 | 1 | 25.0% |
| +0 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 75.0% |
| flkL | flkL | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | ss1 | 75 | ss1 | +0.0201 | 0.2422 |
| 78 | ss1 | 77 | ss1 | +0.0010 | 0.2605 |
| 80 | ss1 | 79 | ss1 | +0.0008 | 0.2423 |
| 23 | flkL | 23 | flkL | +0.0005 | 0.0632 |

### L22 H14 — Rank #5

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.0382

**Key mass** (top-1=45%, top-2=76%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0172 | 45.2% |
| 195 | ss2 | +0.0118 | 30.9% |
| 75 | ss1 | +0.0040 | 10.6% |
| 76 | ss1 | +0.0020 | 5.1% |
| 191 | ss2 | +0.0014 | 3.5% |

**Query mass** (top-1=45%, top-2=76%, top-3=87%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | ss1 | +0.0172 | 45.1% |
| 75 | ss1 | +0.0120 | 31.4% |
| 195 | ss2 | +0.0040 | 10.6% |
| 194 | ss2 | +0.0016 | 4.1% |
| 196 | ss2 | +0.0014 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 45%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 27.3% |
| -120 | 2 | 18.2% |
| -125 | 1 | 9.1% |
| -119 | 1 | 9.1% |
| -117 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 45.5% |
| ss2 | ss1 | 4 | 36.4% |
| flkL | ss2 | 2 | 18.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | ss1 | 194 | ss2 | +0.0165 | 0.1386 |
| 75 | ss1 | 195 | ss2 | +0.0113 | 0.1970 |
| 195 | ss2 | 75 | ss1 | +0.0040 | 0.0895 |
| 196 | ss2 | 76 | ss1 | +0.0014 | 0.0580 |
| 194 | ss2 | 74 | ss1 | +0.0010 | 0.0084 |

### L26 H16 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0171

**Key mass** (top-1=42%, top-2=56%, top-3=67%)  [DISTR(A76/G74/K80/Y221)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | ss1 | +0.0072 | 42.0% |
| 74 | ss1 | +0.0023 | 13.7% |
| 80 | ss1 | +0.0020 | 11.6% |
| 221 | flkR | +0.0015 | 8.8% |
| 196 | ss2 | +0.0012 | 7.3% |

**Query mass** (top-1=37%, top-2=62%, top-3=71%)  [DISTR(G194/A196/G74)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0063 | 36.6% |
| 196 | ss2 | +0.0044 | 25.7% |
| 74 | ss1 | +0.0015 | 8.8% |
| 76 | ss1 | +0.0012 | 7.3% |
| 195 | ss2 | +0.0012 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 27.3% |
| +118 | 1 | 9.1% |
| -147 | 1 | 9.1% |
| -120 | 1 | 9.1% |
| +197 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 72.7% |
| ss1 | flkR | 1 | 9.1% |
| ss1 | ss2 | 1 | 9.1% |
| ss2 | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 194 | ss2 | 76 | ss1 | +0.0039 | 0.3300 |
| 196 | ss2 | 76 | ss1 | +0.0033 | 0.1328 |
| 194 | ss2 | 74 | ss1 | +0.0023 | 0.0201 |
| 74 | ss1 | 221 | flkR | +0.0015 | 0.0790 |
| 76 | ss1 | 196 | ss2 | +0.0012 | 0.0338 |

### L29 H18 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0259

**Key mass** (top-1=13%, top-2=24%, top-3=33%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 77 | ss1 | +0.0034 | 13.1% |
| 78 | ss1 | +0.0027 | 10.5% |
| 75 | ss1 | +0.0025 | 9.5% |
| 197 | ss2 | +0.0022 | 8.3% |
| 79 | ss1 | +0.0021 | 7.9% |

**Query mass** (top-1=15%, top-2=29%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0040 | 15.4% |
| 193 | ss2 | +0.0034 | 13.1% |
| 78 | ss1 | +0.0028 | 10.9% |
| 76 | ss1 | +0.0025 | 9.6% |
| 195 | ss2 | +0.0025 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 9.5% |
| +120 | 2 | 9.5% |
| -116 | 2 | 9.5% |
| -125 | 1 | 4.8% |
| +118 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 33.3% |
| ss1 | ss2 | 7 | 33.3% |
| flkL | flkL | 2 | 9.5% |
| ss1 | flkL | 2 | 9.5% |
| ss1 | other | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss2 | 77 | ss1 | +0.0034 | 0.4275 |
| 194 | ss2 | 78 | ss1 | +0.0027 | 0.0624 |
| 195 | ss2 | 75 | ss1 | +0.0025 | 0.0881 |
| 72 | flkL | 197 | ss2 | +0.0022 | 0.3678 |
| 77 | ss1 | 193 | ss2 | +0.0020 | 0.1185 |

### L30 H0 — Rank #14

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0086

**Key mass** (top-1=46%, top-2=61%, top-3=74%)  [DISTR(G194/G74/L37)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0040 | 45.9% |
| 74 | ss1 | +0.0013 | 14.9% |
| 37 | flkL | +0.0011 | 12.8% |
| 75 | ss1 | +0.0010 | 11.9% |
| 76 | ss1 | +0.0007 | 7.8% |

**Query mass** (top-1=40%, top-2=62%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | ss1 | +0.0035 | 40.3% |
| 194 | ss2 | +0.0019 | 21.6% |
| 195 | ss2 | +0.0016 | 18.9% |
| 196 | ss2 | +0.0007 | 7.8% |
| 193 | ss2 | +0.0005 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 37.5% |
| -120 | 1 | 12.5% |
| +158 | 1 | 12.5% |
| +114 | 1 | 12.5% |
| +156 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 50.0% |
| ss1 | ss2 | 2 | 25.0% |
| ss2 | flkL | 2 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | ss1 | 194 | ss2 | +0.0035 | 0.1116 |
| 194 | ss2 | 74 | ss1 | +0.0013 | 0.0421 |
| 195 | ss2 | 75 | ss1 | +0.0010 | 0.0579 |
| 196 | ss2 | 76 | ss1 | +0.0007 | 0.0534 |
| 195 | ss2 | 37 | flkL | +0.0006 | 0.0517 |

### L30 H1 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0109

**Key mass** (top-1=22%, top-2=41%, top-3=59%)  [DISTR(G194/G195/V75/A76)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0024 | 21.9% |
| 195 | ss2 | +0.0021 | 19.2% |
| 75 | ss1 | +0.0019 | 17.7% |
| 76 | ss1 | +0.0017 | 15.4% |
| 74 | ss1 | +0.0014 | 12.7% |

**Query mass** (top-1=21%, top-2=41%, top-3=58%)  [DISTR(G194/V75/G195/A196)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0023 | 21.4% |
| 75 | ss1 | +0.0021 | 19.2% |
| 195 | ss2 | +0.0019 | 17.7% |
| 196 | ss2 | +0.0017 | 15.4% |
| 74 | ss1 | +0.0017 | 15.2% |

**Offset distribution [frequency]** (top-2 coverage: 62%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 37.5% |
| -120 | 2 | 25.0% |
| +116 | 1 | 12.5% |
| -116 | 1 | 12.5% |
| +113 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 62.5% |
| ss1 | ss2 | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | ss1 | 195 | ss2 | +0.0021 | 0.0405 |
| 195 | ss2 | 75 | ss1 | +0.0019 | 0.0407 |
| 196 | ss2 | 76 | ss1 | +0.0017 | 0.0481 |
| 74 | ss1 | 194 | ss2 | +0.0017 | 0.0142 |
| 194 | ss2 | 74 | ss1 | +0.0014 | 0.0133 |

### L30 H13 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 7  |  total attr: +0.0054

**Key mass** (top-1=23%, top-2=43%, top-3=60%)  [DISTR(G194/A196/A76/L193)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0012 | 22.7% |
| 196 | ss2 | +0.0011 | 20.1% |
| 76 | ss1 | +0.0010 | 17.6% |
| 193 | ss2 | +0.0006 | 10.5% |
| -1 | other | +0.0005 | 9.8% |

**Query mass** (top-1=27%, top-2=50%, top-3=70%)  [DISTR(A196/G74/G195)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 196 | ss2 | +0.0015 | 27.1% |
| 74 | ss1 | +0.0012 | 22.7% |
| 195 | ss2 | +0.0011 | 20.3% |
| 76 | ss1 | +0.0011 | 20.1% |
| 190 | ss2 | +0.0005 | 9.8% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -120 | 2 | 28.6% |
| +120 | 1 | 14.3% |
| +2 | 1 | 14.3% |
| +196 | 1 | 14.3% |
| +113 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 2 | 28.6% |
| ss2 | ss1 | 2 | 28.6% |
| ss2 | ss2 | 2 | 28.6% |
| ss2 | other | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | ss1 | 194 | ss2 | +0.0012 | 0.0195 |
| 76 | ss1 | 196 | ss2 | +0.0011 | 0.0900 |
| 196 | ss2 | 76 | ss1 | +0.0010 | 0.0472 |
| 195 | ss2 | 193 | ss2 | +0.0006 | 0.0510 |
| 195 | ss2 | -1 | other | +0.0005 | 0.0992 |

### L31 H17 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0101

**Key mass** (top-1=23%, top-2=44%, top-3=54%)  [DISTR(A196/G194/L193/H33/V75)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 196 | ss2 | +0.0023 | 22.5% |
| 194 | ss2 | +0.0022 | 21.3% |
| 193 | ss2 | +0.0010 | 10.4% |
| 33 | flkL | +0.0009 | 9.2% |
| 75 | ss1 | +0.0009 | 8.9% |

**Query mass** (top-1=33%, top-2=50%, top-3=61%)  [DISTR(G194/A76/V75/L72/G195)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0033 | 33.1% |
| 76 | ss1 | +0.0017 | 17.1% |
| 75 | ss1 | +0.0010 | 10.4% |
| 72 | flkL | +0.0009 | 9.2% |
| 195 | ss2 | +0.0009 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -120 | 2 | 18.2% |
| +120 | 2 | 18.2% |
| +0 | 1 | 9.1% |
| -118 | 1 | 9.1% |
| +39 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 3 | 27.3% |
| ss2 | ss2 | 2 | 18.2% |
| ss2 | ss1 | 2 | 18.2% |
| ss2 | flkL | 2 | 18.2% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 76 | ss1 | 196 | ss2 | +0.0017 | 0.1425 |
| 194 | ss2 | 194 | ss2 | +0.0013 | 0.0692 |
| 75 | ss1 | 193 | ss2 | +0.0010 | 0.0438 |
| 72 | flkL | 33 | flkL | +0.0009 | 0.1380 |
| 195 | ss2 | 75 | ss1 | +0.0009 | 0.0413 |

### L32 H13 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 15  |  total attr: +0.0413

**Key mass** (top-1=18%, top-2=36%, top-3=48%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | ss1 | +0.0074 | 17.9% |
| 75 | ss1 | +0.0074 | 17.9% |
| 196 | ss2 | +0.0049 | 11.8% |
| 77 | ss1 | +0.0040 | 9.8% |
| 194 | ss2 | +0.0035 | 8.5% |

**Query mass** (top-1=18%, top-2=36%, top-3=49%)  [DISTR(A196/G195/A190/G194/A76)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 196 | ss2 | +0.0074 | 17.9% |
| 195 | ss2 | +0.0074 | 17.9% |
| 190 | ss2 | +0.0054 | 13.0% |
| 194 | ss2 | +0.0049 | 11.9% |
| 76 | ss1 | +0.0049 | 11.8% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 20.0% |
| -120 | 3 | 20.0% |
| +113 | 1 | 6.7% |
| +116 | 1 | 6.7% |
| -116 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 53.3% |
| ss1 | ss2 | 7 | 46.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 196 | ss2 | 76 | ss1 | +0.0074 | 0.1440 |
| 195 | ss2 | 75 | ss1 | +0.0074 | 0.0996 |
| 76 | ss1 | 196 | ss2 | +0.0049 | 0.0943 |
| 190 | ss2 | 77 | ss1 | +0.0040 | 0.1535 |
| 194 | ss2 | 74 | ss1 | +0.0025 | 0.0159 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.0325

**Key mass** (top-1=27%, top-2=53%, top-3=73%)  [DISTR(G194/Y77/A78)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0086 | 26.5% |
| 77 | ss1 | +0.0085 | 26.3% |
| 78 | ss1 | +0.0065 | 19.9% |
| 74 | ss1 | +0.0024 | 7.5% |
| 75 | ss1 | +0.0015 | 4.5% |

**Query mass** (top-1=27%, top-2=47%, top-3=64%)  [DISTR(G194/A190/G74/A78)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 194 | ss2 | +0.0089 | 27.5% |
| 190 | ss2 | +0.0063 | 19.5% |
| 74 | ss1 | +0.0055 | 17.1% |
| 78 | ss1 | +0.0031 | 9.5% |
| 193 | ss2 | +0.0022 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 25.0% |
| +116 | 2 | 16.7% |
| -116 | 2 | 16.7% |
| +113 | 1 | 8.3% |
| -120 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 58.3% |
| ss1 | ss2 | 5 | 41.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 194 | ss2 | 78 | ss1 | +0.0065 | 0.1383 |
| 190 | ss2 | 77 | ss1 | +0.0063 | 0.1471 |
| 74 | ss1 | 194 | ss2 | +0.0055 | 0.0212 |
| 78 | ss1 | 194 | ss2 | +0.0031 | 0.0658 |
| 194 | ss2 | 74 | ss1 | +0.0024 | 0.0093 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #21 | L1 | H13 | 10 | +0.0116 | SINGLE-ANCHOR | F256 | DISTRIBUTED | D251/G253/L193/K249/S243 |  | INTRA:flkR |
| #12 | L3 | H1 | 10 | +0.0075 | SINGLE-ANCHOR | D17 | DISTRIBUTED |  |  | INTRA:flkL |
| #20 | L6 | H11 | 0 | +0.0000 | — |  | — |  |  |  |
| #8 | L6 | H17 | 21 | +0.0289 | DISTRIBUTED |  | DISTRIBUTED | Y192/Q236/L37/Q18/L23 |  |  |
| #1 | L8 | H0 | 38 | +0.1234 | DISTRIBUTED | Q18/A38/V75 | DISTRIBUTED | Q18/A38/V217/L206 |  |  |
| #22 | L9 | H8 | 8 | +0.0095 | SINGLE-ANCHOR | D17 | MULTI-ANCHOR |  |  | ss2→flkR |
| #2 | L9 | H14 | 42 | +0.1273 | DISTRIBUTED |  | DISTRIBUTED | V75/L193/D17/L206/A38 |  |  |
| #17 | L10 | H7 | 6 | +0.0068 | DISTRIBUTED | V199/Q236/D237 | SINGLE-ANCHOR | L193 |  | ss2→flkR |
| #29 | L10 | H15 | 2 | +0.0070 | SINGLE-ANCHOR | N205 | SINGLE-ANCHOR | L193 |  | ss2→flkR |
| #16 | L11 | H18 | 23 | +0.0238 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #28 | L12 | H2 | 26 | +0.0619 | SINGLE-ANCHOR | L193 | DISTRIBUTED | ?-1/L37/F27 |  | CROSS:flkL→ss2 |
| #11 | L12 | H15 | 23 | +0.0607 | SINGLE-ANCHOR | L193 | DISTRIBUTED |  |  | CROSS:flkL→ss2 |
| #19 | L12 | H17 | 26 | +0.0668 | SINGLE-ANCHOR | L193 | DISTRIBUTED | V75/F27/L193 |  | CROSS:flkL→ss2 |
| #6 | L13 | H8 | 16 | +0.0487 | SINGLE-ANCHOR | L193 | MULTI-ANCHOR |  |  |  |
| #9 | L13 | H18 | 8 | +0.0293 | SINGLE-ANCHOR | L193 | SINGLE-ANCHOR | V75 |  | CROSS:ss1→ss2 |
| #24 | L14 | H3 | 14 | +0.0413 | SINGLE-ANCHOR | F27 | SINGLE-ANCHOR | V75 |  |  |
| #23 | L15 | H1 | 7 | +0.0098 | SINGLE-ANCHOR | V75 | DISTRIBUTED | L193/?-1/G194 |  | CROSS:ss2→ss1 |
| #15 | L15 | H8 | 3 | +0.0292 | SINGLE-ANCHOR | L193 | SINGLE-ANCHOR | V75 | CROSS_SSE | CROSS:ss1→ss2 |
| #26 | L16 | H1 | 11 | +0.0176 | SINGLE-ANCHOR | V75 | DISTRIBUTED | L37/T62/V75 |  | flkL→ss1 |
| #10 | L17 | H1 | 18 | +0.0315 | SINGLE-ANCHOR | L193 | DISTRIBUTED |  |  |  |
| #18 | L21 | H13 | 4 | +0.0224 | SINGLE-ANCHOR | V75 | SINGLE-ANCHOR | G74 |  | INTRA:ss1 |
| #5 | L22 | H14 | 11 | +0.0382 | DUAL-ANCHOR | G194/G195 | DUAL-ANCHOR | G74/V75 |  | CROSS:ss1→ss2 |
| #25 | L26 | H16 | 11 | +0.0171 | DISTRIBUTED | A76/G74/K80/Y221 | DISTRIBUTED | G194/A196/G74 |  | CROSS:ss2→ss1 |
| #7 | L29 | H18 | 21 | +0.0259 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #14 | L30 | H0 | 8 | +0.0086 | DISTRIBUTED | G194/G74/L37 | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss2→ss1 |
| #13 | L30 | H1 | 8 | +0.0109 | DISTRIBUTED | G194/G195/V75/A76 | DISTRIBUTED | G194/V75/G195/A196 | CROSS_SSE | CROSS:ss2→ss1 |
| #30 | L30 | H13 | 7 | +0.0054 | DISTRIBUTED | G194/A196/A76/L193 | DISTRIBUTED | A196/G74/G195 |  |  |
| #27 | L31 | H17 | 11 | +0.0101 | DISTRIBUTED | A196/G194/L193/H33/V75 | DISTRIBUTED | G194/A76/V75/L72/G195 |  |  |
| #3 | L32 | H13 | 15 | +0.0413 | DISTRIBUTED |  | DISTRIBUTED | A196/G195/A190/G194/A76 |  | CROSS:ss2→ss1 |
| #4 | L32 | H18 | 12 | +0.0325 | DISTRIBUTED | G194/Y77/A78 | DISTRIBUTED | G194/A190/G74/A78 |  | CROSS:ss2→ss1 |
