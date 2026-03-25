# Contact Pattern Analysis: 4TL6A

Generated: 2026-03-22 22:23:06   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4TL6A |
| Contact pair | (43, 179) |
| ss1 | [38, 49) |
| ss2 | [174, 185) |
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
| Clean metric | 0.8672 |
| Corrupt metric | 0.0069 |
| Gap | 0.8604 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 400 | 82.92% |
| positive IE | 200 | 78.53% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L9 | H10 | +1.0003 |
| 2 | L10 | H9 | +0.5493 |
| 3 | L32 | H13 | +0.3156 |
| 4 | L27 | H15 | +0.3110 |
| 5 | L0 | H19 | +0.2488 |
| 6 | L26 | H16 | +0.2406 |
| 7 | L12 | H8 | +0.1853 |
| 8 | L32 | H18 | +0.1686 |
| 9 | L7 | H0 | +0.1631 |
| 10 | L29 | H18 | +0.1617 |
| 11 | L6 | H13 | +0.1587 |
| 12 | L19 | H0 | +0.1477 |
| 13 | L11 | H14 | +0.1476 |
| 14 | L13 | H12 | +0.1193 |
| 15 | L31 | H17 | +0.1112 |
| 16 | L13 | H7 | +0.0997 |
| 17 | L13 | H14 | +0.0822 |
| 18 | L11 | H16 | +0.0800 |
| 19 | L10 | H12 | +0.0748 |
| 20 | L15 | H6 | +0.0724 |
| 21 | L5 | H19 | +0.0656 |
| 22 | L6 | H19 | +0.0656 |
| 23 | L16 | H19 | +0.0651 |
| 24 | L26 | H3 | +0.0615 |
| 25 | L4 | H10 | +0.0596 |
| 26 | L11 | H8 | +0.0579 |
| 27 | L12 | H9 | +0.0573 |
| 28 | L10 | H0 | +0.0569 |
| 29 | L30 | H1 | +0.0568 |
| 30 | L16 | H3 | +0.0530 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.00% |
| 4 | 0.00% |
| 5 | 0.00% |
| 6 | 0.00% |
| 7 | 0.00% |
| 8 | 0.00% |
| 9 | 0.00% |
| 10 | 0.00% |
| 20 | -0.00% |
| 80 | 0.57% |
| 450 | 132.95% |

## Cell Attribution Analysis

Total cells: 12,355,474

- Positive: 6,230,995
- Negative: 6,122,449

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000179 | 1,235,549 |
| 95th | +0.00000559 | 617,775 |
| 99th | +0.00004063 | 123,556 |
| 99.5th | +0.00008404 | 61,778 |
| 99.9th | +0.00040242 | 12,356 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L9 | H10 | 149 | other | 50 | other | +0.365804 | 0.712248 |
| L7 | H0 | 149 | other | 178 | ss2 | +0.239667 | 0.168346 |
| L6 | H13 | 149 | other | 203 | flkR | +0.201992 | 0.102778 |
| L0 | H19 | 234 | flkR | 234 | flkR | +0.189403 | 0.987454 |
| L7 | H0 | 150 | other | 178 | ss2 | +0.113381 | 0.135247 |
| L6 | H13 | 150 | other | 203 | flkR | +0.092789 | 0.096447 |
| L32 | H13 | 183 | ss2 | 44 | ss1 | +0.091027 | 0.306760 |
| L21 | H13 | 178 | ss2 | 177 | ss2 | +0.085435 | 0.633050 |
| L12 | H11 | 41 | ss1 | 50 | other | +0.082646 | 0.732770 |
| L9 | H10 | 150 | other | 50 | other | +0.080719 | 0.661729 |
| L32 | H13 | 44 | ss1 | 183 | ss2 | +0.069510 | 0.234246 |
| L5 | H19 | 149 | other | 50 | other | +0.058105 | 0.025766 |
| L15 | H6 | 183 | ss2 | 150 | other | +0.052308 | 0.385191 |
| L26 | H16 | 176 | ss2 | 38 | ss1 | +0.050395 | 0.537801 |
| L15 | H6 | 183 | ss2 | 149 | other | +0.049490 | 0.362593 |
| L10 | H12 | 177 | ss2 | 149 | other | +0.049013 | 0.433722 |
| L13 | H2 | 183 | ss2 | 178 | ss2 | +0.047167 | 0.653767 |
| L17 | H7 | 179 | ss2 | 170 | other | +0.045874 | 0.614627 |
| L27 | H15 | 41 | ss1 | 178 | ss2 | +0.043755 | 0.364750 |
| L12 | H8 | 183 | ss2 | 149 | other | +0.042673 | 0.408434 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L15 | H13 | 184 | ss2 | 178 | ss2 | -0.022468 | 0.796769 |
| L10 | H9 | -1 | other | 149 | other | -0.022525 | 0.360044 |
| L17 | H13 | 178 | ss2 | 150 | other | -0.023727 | 0.374892 |
| L11 | H3 | 43 | ss1 | 50 | other | -0.024495 | 0.415176 |
| L15 | H13 | 203 | flkR | 204 | flkR | -0.025525 | 0.571374 |
| L13 | H15 | 38 | ss1 | 50 | other | -0.026589 | 0.607895 |
| L31 | H17 | 183 | ss2 | 253 | other | -0.026692 | 0.139796 |
| L6 | H13 | 151 | other | 203 | flkR | -0.032508 | 0.077919 |
| L13 | H2 | 177 | ss2 | 178 | ss2 | -0.035763 | 0.867438 |
| L12 | H11 | 42 | ss1 | 50 | other | -0.036109 | 0.617280 |
| L11 | H8 | 43 | ss1 | 150 | other | -0.037550 | 0.401539 |
| L11 | H8 | 43 | ss1 | 149 | other | -0.037898 | 0.411257 |
| L11 | H14 | 179 | ss2 | 149 | other | -0.038006 | 0.361067 |
| L12 | H11 | 40 | ss1 | 50 | other | -0.038015 | 0.640252 |
| L17 | H7 | 178 | ss2 | 170 | other | -0.041492 | 0.508424 |
| L11 | H14 | 179 | ss2 | 150 | other | -0.043720 | 0.416239 |
| L21 | H13 | 176 | ss2 | 177 | ss2 | -0.052394 | 0.820690 |
| L7 | H0 | 151 | other | 178 | ss2 | -0.068400 | 0.129228 |
| L1 | H14 | 50 | other | 234 | flkR | -0.156921 | 0.012662 |
| L9 | H10 | 151 | other | 50 | other | -0.159574 | 0.582829 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0069 | 0.00% |
| 10 | 10 | 7 | 0.0069 | -0.00% |
| 20 | 20 | 15 | 0.0069 | 0.00% |
| 50 | 50 | 29 | 0.0069 | 0.00% |
| 100 | 100 | 56 | 0.0069 | -0.00% |
| 200 | 200 | 97 | 0.0069 | -0.00% |
| 500 | 500 | 147 | 0.0069 | -0.00% |
| 1000 | 1,000 | 180 | 0.0070 | 0.01% |
| 2000 | 2,000 | 195 | 0.0071 | 0.02% |
| 5000 | 5,000 | 199 | 0.0071 | 0.03% |
| 10000 | 10,000 | 200 | 0.0072 | 0.03% |
| 20000 | 20,000 | 200 | 0.0079 | 0.12% |
| 50000 | 50,000 | 200 | 0.0081 | 0.14% |

## Motif Analysis

### L0 H19 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 2  |  total attr: +0.1944

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 234 | flkR | +0.1944 | 100.0% |

**Query mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 234 | flkR | +0.1894 | 97.4% |
| 51 | other | +0.0050 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 50.0% |
| -183 | 1 | 50.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 1 | 50.0% |
| other | flkR | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 234 | flkR | 234 | flkR | +0.1894 | 0.9875 |
| 51 | other | 234 | flkR | +0.0050 | 0.0024 |

### L4 H10 — Rank #25

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 9  |  total attr: +0.0721

**Key mass** (top-1=38%, top-2=62%, top-3=73%)  [DISTR(Y234/F236/I221)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 234 | flkR | +0.0272 | 37.7% |
| 236 | other | +0.0177 | 24.6% |
| 221 | flkR | +0.0077 | 10.6% |
| 222 | flkR | +0.0076 | 10.6% |
| 219 | flkR | +0.0075 | 10.4% |

**Query mass** (top-1=47%, top-2=83%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0337 | 46.7% |
| 50 | other | +0.0265 | 36.7% |
| 150 | other | +0.0119 | 16.6% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -85 | 1 | 11.1% |
| -87 | 1 | 11.1% |
| -171 | 1 | 11.1% |
| -172 | 1 | 11.1% |
| -84 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 5 | 55.6% |
| other | other | 4 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 149 | other | 234 | flkR | +0.0196 | 0.0193 |
| 149 | other | 236 | other | +0.0097 | 0.0167 |
| 50 | other | 221 | flkR | +0.0077 | 0.0024 |
| 50 | other | 222 | flkR | +0.0076 | 0.0033 |
| 150 | other | 234 | flkR | +0.0076 | 0.0178 |

### L5 H19 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR  |  cells: 5  |  total attr: +0.1490

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 50 | other | +0.1490 | 100.0% |

**Query mass** (top-1=39%, top-2=62%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0581 | 39.0% |
| 178 | ss2 | +0.0337 | 22.6% |
| 150 | other | +0.0287 | 19.2% |
| 203 | flkR | +0.0219 | 14.7% |
| 148 | other | +0.0067 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +99 | 1 | 20.0% |
| +128 | 1 | 20.0% |
| +100 | 1 | 20.0% |
| +153 | 1 | 20.0% |
| +98 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 3 | 60.0% |
| ss2 | other | 1 | 20.0% |
| flkR | other | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 149 | other | 50 | other | +0.0581 | 0.0258 |
| 178 | ss2 | 50 | other | +0.0337 | 0.0301 |
| 150 | other | 50 | other | +0.0287 | 0.0257 |
| 203 | flkR | 50 | other | +0.0219 | 0.0343 |
| 148 | other | 50 | other | +0.0067 | 0.0262 |

### L6 H13 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.3216

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | flkR | +0.3216 | 100.0% |

**Query mass** (top-1=63%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.2020 | 62.8% |
| 150 | other | +0.0928 | 28.9% |
| 148 | other | +0.0184 | 5.7% |
| 152 | other | +0.0084 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -54 | 1 | 25.0% |
| -53 | 1 | 25.0% |
| -55 | 1 | 25.0% |
| -51 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 149 | other | 203 | flkR | +0.2020 | 0.1028 |
| 150 | other | 203 | flkR | +0.0928 | 0.0964 |
| 148 | other | 203 | flkR | +0.0184 | 0.0907 |
| 152 | other | 203 | flkR | +0.0084 | 0.0642 |

### L6 H19 — Rank #22

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 7  |  total attr: +0.1195

**Key mass** (top-1=52%, top-2=87%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0619 | 51.8% |
| 203 | flkR | +0.0418 | 34.9% |
| 177 | ss2 | +0.0159 | 13.3% |

**Query mass** (top-1=39%, top-2=74%, top-3=94%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0471 | 39.4% |
| 178 | ss2 | +0.0418 | 34.9% |
| 150 | other | +0.0230 | 19.3% |
| 148 | other | +0.0043 | 3.6% |
| 152 | other | +0.0034 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -28 | 2 | 28.6% |
| -25 | 1 | 14.3% |
| -29 | 1 | 14.3% |
| -27 | 1 | 14.3% |
| -30 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 6 | 85.7% |
| ss2 | flkR | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | ss2 | 203 | flkR | +0.0418 | 0.0576 |
| 149 | other | 178 | ss2 | +0.0364 | 0.0717 |
| 150 | other | 178 | ss2 | +0.0178 | 0.0732 |
| 149 | other | 177 | ss2 | +0.0106 | 0.0284 |
| 150 | other | 177 | ss2 | +0.0053 | 0.0300 |

### L7 H0 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 5  |  total attr: +0.4333

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.4333 | 100.0% |

**Query mass** (top-1=55%, top-2=81%, top-3=90%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.2397 | 55.3% |
| 150 | other | +0.1134 | 26.2% |
| 148 | other | +0.0351 | 8.1% |
| 152 | other | +0.0298 | 6.9% |
| 153 | other | +0.0154 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -29 | 1 | 20.0% |
| -28 | 1 | 20.0% |
| -30 | 1 | 20.0% |
| -26 | 1 | 20.0% |
| -25 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 149 | other | 178 | ss2 | +0.2397 | 0.1683 |
| 150 | other | 178 | ss2 | +0.1134 | 0.1352 |
| 148 | other | 178 | ss2 | +0.0351 | 0.2117 |
| 152 | other | 178 | ss2 | +0.0298 | 0.1421 |
| 153 | other | 178 | ss2 | +0.0154 | 0.1611 |

### L9 H10 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 9  |  total attr: +0.5378

**Key mass** (top-1=92%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 50 | other | +0.4922 | 91.5% |
| 51 | other | +0.0296 | 5.5% |
| 52 | other | +0.0160 | 3.0% |

**Query mass** (top-1=75%, top-2=91%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.4010 | 74.6% |
| 150 | other | +0.0911 | 16.9% |
| 152 | other | +0.0227 | 4.2% |
| 148 | other | +0.0129 | 2.4% |
| 153 | other | +0.0101 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 56%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +98 | 3 | 33.3% |
| +99 | 2 | 22.2% |
| +100 | 1 | 11.1% |
| +102 | 1 | 11.1% |
| +97 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 9 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 149 | other | 50 | other | +0.3658 | 0.7122 |
| 150 | other | 50 | other | +0.0807 | 0.6617 |
| 152 | other | 50 | other | +0.0227 | 0.4564 |
| 149 | other | 51 | other | +0.0226 | 0.0527 |
| 148 | other | 50 | other | +0.0129 | 0.5380 |

### L10 H0 — Rank #28

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L10 H9 — Rank #2

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.1172

**Key mass** (top-1=53%, top-2=85%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0624 | 53.2% |
| 150 | other | +0.0378 | 32.3% |
| 253 | other | +0.0170 | 14.5% |

**Query mass** (top-1=37%, top-2=50%, top-3=59%)  [DISTR(V178/G45/E186/I184/G188)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0429 | 36.6% |
| 45 | ss1 | +0.0154 | 13.1% |
| 186 | flkR | +0.0108 | 9.2% |
| 184 | ss2 | +0.0107 | 9.2% |
| 188 | flkR | +0.0096 | 8.2% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +29 | 1 | 5.9% |
| +28 | 1 | 5.9% |
| -203 | 1 | 5.9% |
| -104 | 1 | 5.9% |
| -105 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 6 | 35.3% |
| ss1 | other | 4 | 23.5% |
| flkR | other | 4 | 23.5% |
| other | other | 3 | 17.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | ss2 | 149 | other | +0.0228 | 0.4073 |
| 178 | ss2 | 150 | other | +0.0161 | 0.3493 |
| 50 | other | 253 | other | +0.0094 | 0.1635 |
| 45 | ss1 | 149 | other | +0.0082 | 0.3852 |
| 45 | ss1 | 150 | other | +0.0072 | 0.3344 |

### L10 H12 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.2978

**Key mass** (top-1=52%, top-2=89%, top-3=98%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.1552 | 52.1% |
| 150 | other | +0.1108 | 37.2% |
| 151 | other | +0.0247 | 8.3% |
| 148 | other | +0.0070 | 2.4% |

**Query mass** (top-1=31%, top-2=62%, top-3=75%)  [DISTR(T177/R183/E182)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 177 | ss2 | +0.0927 | 31.1% |
| 183 | ss2 | +0.0919 | 30.9% |
| 182 | ss2 | +0.0378 | 12.7% |
| 200 | flkR | +0.0201 | 6.7% |
| 166 | other | +0.0170 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +33 | 2 | 8.7% |
| +32 | 2 | 8.7% |
| +28 | 1 | 4.3% |
| +34 | 1 | 4.3% |
| +27 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 10 | 43.5% |
| other | other | 7 | 30.4% |
| flkR | other | 6 | 26.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 177 | ss2 | 149 | other | +0.0490 | 0.4337 |
| 183 | ss2 | 149 | other | +0.0399 | 0.3587 |
| 183 | ss2 | 150 | other | +0.0398 | 0.3617 |
| 177 | ss2 | 150 | other | +0.0322 | 0.2915 |
| 182 | ss2 | 149 | other | +0.0170 | 0.3875 |

### L11 H8 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 14  |  total attr: +0.1249

**Key mass** (top-1=50%, top-2=97%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0624 | 50.0% |
| 150 | other | +0.0589 | 47.2% |
| 151 | other | +0.0036 | 2.9% |

**Query mass** (top-1=24%, top-2=45%, top-3=62%)  [DISTR(T41/S44/S47/G38)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 41 | ss1 | +0.0298 | 23.8% |
| 44 | ss1 | +0.0264 | 21.2% |
| 47 | ss1 | +0.0213 | 17.1% |
| 38 | ss1 | +0.0203 | 16.3% |
| 45 | ss1 | +0.0118 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -105 | 2 | 14.3% |
| -108 | 1 | 7.1% |
| -106 | 1 | 7.1% |
| -109 | 1 | 7.1% |
| -102 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=79%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 11 | 78.6% |
| other | other | 3 | 21.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 44 | ss1 | 149 | other | +0.0133 | 0.2912 |
| 41 | ss1 | 149 | other | +0.0132 | 0.1767 |
| 44 | ss1 | 150 | other | +0.0132 | 0.3029 |
| 41 | ss1 | 150 | other | +0.0130 | 0.1715 |
| 47 | ss1 | 149 | other | +0.0110 | 0.2781 |

### L11 H14 — Rank #13

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.2542

**Key mass** (top-1=50%, top-2=94%, top-3=98%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | other | +0.1275 | 50.1% |
| 149 | other | +0.1126 | 44.3% |
| 151 | other | +0.0085 | 3.3% |
| 50 | other | +0.0057 | 2.2% |

**Query mass** (top-1=26%, top-2=49%, top-3=64%)  [DISTR(T177/V178/T176/E182)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 177 | ss2 | +0.0653 | 25.7% |
| 178 | ss2 | +0.0590 | 23.2% |
| 176 | ss2 | +0.0389 | 15.3% |
| 182 | ss2 | +0.0371 | 14.6% |
| 183 | ss2 | +0.0196 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +27 | 2 | 11.1% |
| +28 | 2 | 11.1% |
| +26 | 2 | 11.1% |
| +33 | 2 | 11.1% |
| +25 | 2 | 11.1% |

**Region-pair profile** (q→k)  (top=78%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 14 | 77.8% |
| other | other | 2 | 11.1% |
| ss1 | other | 1 | 5.6% |
| flkR | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 177 | ss2 | 150 | other | +0.0305 | 0.3902 |
| 178 | ss2 | 150 | other | +0.0303 | 0.4483 |
| 177 | ss2 | 149 | other | +0.0300 | 0.3864 |
| 178 | ss2 | 149 | other | +0.0286 | 0.4163 |
| 182 | ss2 | 150 | other | +0.0198 | 0.4017 |

### L11 H16 — Rank #18

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0824

**Key mass** (top-1=60%, top-2=87%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 50 | other | +0.0494 | 59.9% |
| 253 | other | +0.0220 | 26.7% |
| 150 | other | +0.0055 | 6.7% |
| 149 | other | +0.0055 | 6.6% |

**Query mass** (top-1=28%, top-2=49%, top-3=63%)  [DISTR(?-1/V43/S44/M0)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0231 | 28.0% |
| 43 | ss1 | +0.0177 | 21.5% |
| 44 | ss1 | +0.0112 | 13.6% |
| 0 | flkL | +0.0086 | 10.4% |
| 149 | other | +0.0065 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -51 | 1 | 10.0% |
| -6 | 1 | 10.0% |
| -50 | 1 | 10.0% |
| -210 | 1 | 10.0% |
| +99 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 4 | 40.0% |
| other | other | 2 | 20.0% |
| ss2 | other | 2 | 20.0% |
| flkL | other | 1 | 10.0% |
| flkR | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 50 | other | +0.0231 | 0.3981 |
| 44 | ss1 | 50 | other | +0.0112 | 0.1847 |
| 0 | flkL | 50 | other | +0.0086 | 0.3247 |
| 43 | ss1 | 253 | other | +0.0067 | 0.1222 |
| 149 | other | 50 | other | +0.0065 | 0.0645 |

### L12 H8 — Rank #7

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 25  |  total attr: +0.2525

**Key mass** (top-1=53%, top-2=92%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.1339 | 53.0% |
| 150 | other | +0.0988 | 39.1% |
| 50 | other | +0.0119 | 4.7% |
| 179 | ss2 | +0.0079 | 3.1% |

**Query mass** (top-1=30%, top-2=40%, top-3=49%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.0764 | 30.3% |
| 201 | flkR | +0.0245 | 9.7% |
| 184 | ss2 | +0.0225 | 8.9% |
| 179 | ss2 | +0.0204 | 8.1% |
| 253 | other | +0.0202 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +34 | 2 | 8.0% |
| +52 | 2 | 8.0% |
| +35 | 2 | 8.0% |
| +30 | 2 | 8.0% |
| +53 | 2 | 8.0% |

**Region-pair profile** (q→k)  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 10 | 40.0% |
| ss2 | other | 8 | 32.0% |
| other | other | 5 | 20.0% |
| ss2 | ss2 | 2 | 8.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss2 | 149 | other | +0.0427 | 0.4084 |
| 183 | ss2 | 150 | other | +0.0293 | 0.2705 |
| 201 | flkR | 149 | other | +0.0138 | 0.5267 |
| 184 | ss2 | 149 | other | +0.0130 | 0.5239 |
| -1 | other | 50 | other | +0.0119 | 0.4571 |

### L12 H9 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.1593

**Key mass** (top-1=70%, top-2=80%, top-3=85%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.1112 | 69.8% |
| 149 | other | +0.0163 | 10.2% |
| 173 | other | +0.0082 | 5.2% |
| 150 | other | +0.0078 | 4.9% |
| 146 | other | +0.0043 | 2.7% |

**Query mass** (top-1=20%, top-2=36%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.0314 | 19.7% |
| 176 | ss2 | +0.0257 | 16.1% |
| 182 | ss2 | +0.0234 | 14.7% |
| 150 | other | +0.0148 | 9.3% |
| 149 | other | +0.0134 | 8.4% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 3 | 17.6% |
| +5 | 2 | 11.8% |
| +0 | 2 | 11.8% |
| -1 | 2 | 11.8% |
| +3 | 2 | 11.8% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 7 | 41.2% |
| ss2 | ss2 | 6 | 35.3% |
| flkR | ss2 | 1 | 5.9% |
| ss2 | other | 1 | 5.9% |
| other | ss2 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss2 | 178 | ss2 | +0.0314 | 0.8979 |
| 176 | ss2 | 178 | ss2 | +0.0257 | 0.4105 |
| 182 | ss2 | 178 | ss2 | +0.0234 | 0.9180 |
| 189 | flkR | 178 | ss2 | +0.0106 | 0.7449 |
| 178 | ss2 | 173 | other | +0.0082 | 0.1454 |

### L13 H7 — Rank #16

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.1211

**Key mass** (top-1=47%, top-2=72%, top-3=80%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0571 | 47.2% |
| 150 | other | +0.0297 | 24.5% |
| 181 | ss2 | +0.0107 | 8.8% |
| 185 | flkR | +0.0080 | 6.6% |
| 178 | ss2 | +0.0073 | 6.0% |

**Query mass** (top-1=40%, top-2=58%, top-3=72%)  [DISTR(V178/M179/R183)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0481 | 39.7% |
| 179 | ss2 | +0.0219 | 18.0% |
| 183 | ss2 | +0.0168 | 13.9% |
| 177 | ss2 | +0.0143 | 11.8% |
| 181 | ss2 | +0.0116 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +29 | 2 | 15.4% |
| +28 | 2 | 15.4% |
| -4 | 2 | 15.4% |
| +0 | 2 | 15.4% |
| +30 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 8 | 61.5% |
| ss2 | ss2 | 3 | 23.1% |
| ss2 | flkR | 1 | 7.7% |
| ss1 | flkL | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | ss2 | 149 | other | +0.0273 | 0.5161 |
| 178 | ss2 | 150 | other | +0.0135 | 0.2601 |
| 179 | ss2 | 149 | other | +0.0131 | 0.4169 |
| 177 | ss2 | 181 | ss2 | +0.0107 | 0.5895 |
| 183 | ss2 | 149 | other | +0.0094 | 0.1670 |

### L13 H12 — Rank #14

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1478

**Key mass** (top-1=54%, top-2=97%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0794 | 53.7% |
| 150 | other | +0.0641 | 43.4% |
| 43 | ss1 | +0.0043 | 2.9% |

**Query mass** (top-1=22%, top-2=38%, top-3=51%)  [DISTR(V43/?-1/S44/S40/M0)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 43 | ss1 | +0.0326 | 22.1% |
| -1 | other | +0.0238 | 16.1% |
| 44 | ss1 | +0.0192 | 13.0% |
| 40 | ss1 | +0.0157 | 10.6% |
| 0 | flkL | +0.0150 | 10.1% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -106 | 2 | 11.1% |
| -107 | 2 | 11.1% |
| -150 | 2 | 11.1% |
| -151 | 1 | 5.6% |
| -105 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 7 | 38.9% |
| other | other | 6 | 33.3% |
| flkL | other | 4 | 22.2% |
| ss1 | ss1 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 43 | ss1 | 149 | other | +0.0185 | 0.4397 |
| 43 | ss1 | 150 | other | +0.0141 | 0.3491 |
| -1 | other | 149 | other | +0.0131 | 0.3593 |
| -1 | other | 150 | other | +0.0107 | 0.3188 |
| 44 | ss1 | 150 | other | +0.0096 | 0.4027 |

### L13 H14 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 12  |  total attr: +0.1472

**Key mass** (top-1=39%, top-2=74%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 149 | other | +0.0571 | 38.8% |
| 150 | other | +0.0526 | 35.7% |
| -1 | other | +0.0330 | 22.4% |
| 170 | other | +0.0046 | 3.1% |

**Query mass** (top-1=29%, top-2=51%, top-3=69%)  [DISTR(T176/T177/?-1/L170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0424 | 28.8% |
| 177 | ss2 | +0.0330 | 22.4% |
| -1 | other | +0.0266 | 18.0% |
| 170 | other | +0.0208 | 14.1% |
| 183 | ss2 | +0.0099 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +27 | 2 | 16.7% |
| +28 | 2 | 16.7% |
| +0 | 1 | 8.3% |
| +26 | 1 | 8.3% |
| +21 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 6 | 50.0% |
| other | other | 4 | 33.3% |
| flkL | other | 1 | 8.3% |
| flkR | other | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | -1 | other | +0.0266 | 0.6222 |
| 176 | ss2 | 150 | other | +0.0219 | 0.3000 |
| 176 | ss2 | 149 | other | +0.0205 | 0.2770 |
| 177 | ss2 | 150 | other | +0.0178 | 0.3010 |
| 177 | ss2 | 149 | other | +0.0153 | 0.2622 |

### L15 H6 — Rank #20

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.2131

**Key mass** (top-1=28%, top-2=53%, top-3=76%)  [DISTR(L206/F150/V149)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | flkR | +0.0604 | 28.4% |
| 150 | other | +0.0523 | 24.5% |
| 149 | other | +0.0495 | 23.2% |
| 204 | flkR | +0.0256 | 12.0% |
| 178 | ss2 | +0.0146 | 6.8% |

**Query mass** (top-1=48%, top-2=58%, top-3=65%)  [DISTR(R183/L219/T177/V178/V203)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.1018 | 47.8% |
| 219 | flkR | +0.0221 | 10.3% |
| 177 | ss2 | +0.0149 | 7.0% |
| 178 | ss2 | +0.0094 | 4.4% |
| 203 | flkR | +0.0088 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +33 | 1 | 5.9% |
| +34 | 1 | 5.9% |
| +15 | 1 | 5.9% |
| -29 | 1 | 5.9% |
| -28 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 6 | 35.3% |
| ss2 | flkR | 5 | 29.4% |
| ss2 | other | 2 | 11.8% |
| flkR | ss2 | 2 | 11.8% |
| other | ss1 | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss2 | 150 | other | +0.0523 | 0.3852 |
| 183 | ss2 | 149 | other | +0.0495 | 0.3626 |
| 219 | flkR | 204 | flkR | +0.0184 | 0.7586 |
| 177 | ss2 | 206 | flkR | +0.0149 | 0.3944 |
| 178 | ss2 | 206 | flkR | +0.0094 | 0.2675 |

### L16 H3 — Rank #30

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | INTRA:ss2  |  cells: 3  |  total attr: +0.0181

**Key mass** (top-1=44%, top-2=80%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.0080 | 44.0% |
| 178 | ss2 | +0.0066 | 36.5% |
| 182 | ss2 | +0.0035 | 19.5% |

**Query mass** (top-1=44%, top-2=80%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.0080 | 44.0% |
| 178 | ss2 | +0.0066 | 36.5% |
| 183 | ss2 | +0.0035 | 19.5% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 66.7% |
| +1 | 1 | 33.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 2 | 66.7% |
| ss1 | ss1 | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 44 | ss1 | 44 | ss1 | +0.0080 | 0.2204 |
| 178 | ss2 | 178 | ss2 | +0.0066 | 0.2450 |
| 183 | ss2 | 182 | ss2 | +0.0035 | 0.0849 |

### L16 H19 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 3  |  total attr: +0.0205

**Key mass** (top-1=42%, top-2=73%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 253 | other | +0.0086 | 42.1% |
| 50 | other | +0.0065 | 31.4% |
| 48 | ss1 | +0.0054 | 26.5% |

**Query mass** (top-1=58%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.0119 | 57.9% |
| 178 | ss2 | +0.0086 | 42.1% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -75 | 1 | 33.3% |
| +133 | 1 | 33.3% |
| +135 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 2 | 66.7% |
| ss2 | ss1 | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | ss2 | 253 | other | +0.0086 | 0.5506 |
| 183 | ss2 | 50 | other | +0.0065 | 0.1448 |
| 183 | ss2 | 48 | ss1 | +0.0054 | 0.0868 |

### L19 H0 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 10  |  total attr: +0.1552

**Key mass** (top-1=26%, top-2=50%, top-3=71%)  [DISTR(T177/L170/T176)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 177 | ss2 | +0.0399 | 25.7% |
| 170 | other | +0.0374 | 24.1% |
| 176 | ss2 | +0.0337 | 21.7% |
| 179 | ss2 | +0.0154 | 9.9% |
| 41 | ss1 | +0.0095 | 6.1% |

**Query mass** (top-1=26%, top-2=52%, top-3=74%)  [DISTR(T177/M179/V178)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 177 | ss2 | +0.0409 | 26.4% |
| 179 | ss2 | +0.0399 | 25.7% |
| 178 | ss2 | +0.0337 | 21.7% |
| 181 | ss2 | +0.0105 | 6.8% |
| 43 | ss1 | +0.0095 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 5 | 50.0% |
| +7 | 5 | 50.0% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 4 | 40.0% |
| ss2 | other | 2 | 20.0% |
| ss1 | ss1 | 1 | 10.0% |
| other | ss1 | 1 | 10.0% |
| other | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 179 | ss2 | 177 | ss2 | +0.0399 | 0.7989 |
| 177 | ss2 | 170 | other | +0.0374 | 0.7858 |
| 178 | ss2 | 176 | ss2 | +0.0337 | 0.3803 |
| 181 | ss2 | 179 | ss2 | +0.0105 | 0.8043 |
| 43 | ss1 | 41 | ss1 | +0.0095 | 0.5893 |

### L26 H3 — Rank #24

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 7  |  total attr: +0.0436

**Key mass** (top-1=43%, top-2=60%, top-3=74%)  [DISTR(G38/M179/G50)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0186 | 42.6% |
| 179 | ss2 | +0.0074 | 17.0% |
| 50 | other | +0.0063 | 14.5% |
| 28 | flkL | +0.0061 | 14.0% |
| 40 | ss1 | +0.0052 | 11.9% |

**Query mass** (top-1=20%, top-2=37%, top-3=51%)  [DISTR(T41/E182/L42/G38/S44)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 41 | ss1 | +0.0086 | 19.7% |
| 182 | ss2 | +0.0074 | 17.0% |
| 42 | ss1 | +0.0063 | 14.5% |
| 38 | ss1 | +0.0061 | 14.0% |
| 44 | ss1 | +0.0052 | 11.9% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 28.6% |
| -8 | 1 | 14.3% |
| +10 | 1 | 14.3% |
| +4 | 1 | 14.3% |
| -3 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 2 | 28.6% |
| flkL | ss1 | 2 | 28.6% |
| ss2 | ss2 | 1 | 14.3% |
| ss1 | other | 1 | 14.3% |
| ss1 | flkL | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 41 | ss1 | 38 | ss1 | +0.0086 | 0.1614 |
| 182 | ss2 | 179 | ss2 | +0.0074 | 0.3155 |
| 42 | ss1 | 50 | other | +0.0063 | 0.4862 |
| 38 | ss1 | 28 | flkL | +0.0061 | 0.2721 |
| 44 | ss1 | 40 | ss1 | +0.0052 | 0.1305 |

### L26 H16 — Rank #6

**Tags:** k:MULTI-ANCHOR / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 5  |  total attr: +0.1242

**Key mass** (top-1=41%, top-2=64%, top-3=85%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0504 | 40.6% |
| 176 | ss2 | +0.0289 | 23.3% |
| 178 | ss2 | +0.0262 | 21.1% |
| 41 | ss1 | +0.0151 | 12.2% |
| 40 | ss1 | +0.0035 | 2.9% |

**Query mass** (top-1=41%, top-2=64%, top-3=85%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0504 | 40.6% |
| 38 | ss1 | +0.0289 | 23.3% |
| 41 | ss1 | +0.0262 | 21.1% |
| 178 | ss2 | +0.0151 | 12.2% |
| 177 | ss2 | +0.0035 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +137 | 2 | 40.0% |
| +138 | 1 | 20.0% |
| -138 | 1 | 20.0% |
| -137 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 60.0% |
| ss1 | ss2 | 2 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 176 | ss2 | 38 | ss1 | +0.0504 | 0.5378 |
| 38 | ss1 | 176 | ss2 | +0.0289 | 0.1917 |
| 41 | ss1 | 178 | ss2 | +0.0262 | 0.3016 |
| 178 | ss2 | 41 | ss1 | +0.0151 | 0.2002 |
| 177 | ss2 | 40 | ss1 | +0.0035 | 0.5912 |

### L27 H15 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 7  |  total attr: +0.1204

**Key mass** (top-1=60%, top-2=74%, top-3=83%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0726 | 60.3% |
| 176 | ss2 | +0.0166 | 13.8% |
| 220 | flkR | +0.0110 | 9.1% |
| 183 | ss2 | +0.0085 | 7.0% |
| 43 | ss1 | +0.0075 | 6.2% |

**Query mass** (top-1=36%, top-2=60%, top-3=74%)  [DISTR(T41/V43/G38)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 41 | ss1 | +0.0438 | 36.3% |
| 43 | ss1 | +0.0288 | 23.9% |
| 38 | ss1 | +0.0166 | 13.8% |
| 44 | ss1 | +0.0127 | 10.6% |
| 205 | flkR | +0.0110 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -137 | 1 | 14.3% |
| -135 | 1 | 14.3% |
| -138 | 1 | 14.3% |
| -15 | 1 | 14.3% |
| -139 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 57.1% |
| flkR | flkR | 1 | 14.3% |
| ss2 | ss1 | 1 | 14.3% |
| ss1 | flkL | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 41 | ss1 | 178 | ss2 | +0.0438 | 0.3647 |
| 43 | ss1 | 178 | ss2 | +0.0288 | 0.4448 |
| 38 | ss1 | 176 | ss2 | +0.0166 | 0.0959 |
| 205 | flkR | 220 | flkR | +0.0110 | 0.7664 |
| 44 | ss1 | 183 | ss2 | +0.0085 | 0.0310 |

### L29 H18 — Rank #10

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1918

**Key mass** (top-1=20%, top-2=36%, top-3=51%)  [DISTR(T176/I205/S44/L35/G38)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0389 | 20.3% |
| 205 | flkR | +0.0301 | 15.7% |
| 44 | ss1 | +0.0279 | 14.5% |
| 35 | flkL | +0.0238 | 12.4% |
| 38 | ss1 | +0.0216 | 11.2% |

**Query mass** (top-1=24%, top-2=46%, top-3=63%)  [DISTR(G38/R183/S44/T176)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0460 | 24.0% |
| 183 | ss2 | +0.0430 | 22.4% |
| 44 | ss1 | +0.0327 | 17.1% |
| 176 | ss2 | +0.0265 | 13.8% |
| 41 | ss1 | +0.0174 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +139 | 2 | 11.1% |
| -137 | 2 | 11.1% |
| -138 | 1 | 5.6% |
| -161 | 1 | 5.6% |
| +138 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 27.8% |
| ss2 | flkR | 4 | 22.2% |
| ss2 | flkL | 3 | 16.7% |
| ss2 | ss1 | 2 | 11.1% |
| flkR | other | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 38 | ss1 | 176 | ss2 | +0.0389 | 0.2288 |
| 183 | ss2 | 44 | ss1 | +0.0279 | 0.1706 |
| 44 | ss1 | 205 | flkR | +0.0231 | 0.2101 |
| 176 | ss2 | 38 | ss1 | +0.0216 | 0.1993 |
| 41 | ss1 | 35 | flkL | +0.0174 | 0.2526 |

### L30 H1 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 5  |  total attr: +0.0499

**Key mass** (top-1=65%, top-2=80%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 41 | ss1 | +0.0324 | 65.0% |
| 202 | flkR | +0.0076 | 15.1% |
| 183 | ss2 | +0.0052 | 10.4% |
| 43 | ss1 | +0.0047 | 9.4% |

**Query mass** (top-1=48%, top-2=65%, top-3=80%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0237 | 47.6% |
| 176 | ss2 | +0.0087 | 17.4% |
| 41 | ss1 | +0.0076 | 15.1% |
| 44 | ss1 | +0.0052 | 10.4% |
| 180 | ss2 | +0.0047 | 9.4% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +137 | 2 | 40.0% |
| +135 | 1 | 20.0% |
| -161 | 1 | 20.0% |
| -139 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 60.0% |
| ss1 | flkR | 1 | 20.0% |
| ss1 | ss2 | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | ss2 | 41 | ss1 | +0.0237 | 0.2218 |
| 176 | ss2 | 41 | ss1 | +0.0087 | 0.6026 |
| 41 | ss1 | 202 | flkR | +0.0076 | 0.9718 |
| 44 | ss1 | 183 | ss2 | +0.0052 | 0.0309 |
| 180 | ss2 | 43 | ss1 | +0.0047 | 0.1592 |

### L31 H17 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0893

**Key mass** (top-1=89%, top-2=96%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 253 | other | +0.0796 | 89.2% |
| 43 | ss1 | +0.0058 | 6.5% |
| -1 | other | +0.0038 | 4.3% |

**Query mass** (top-1=26%, top-2=41%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 205 | flkR | +0.0232 | 26.0% |
| 203 | flkR | +0.0136 | 15.2% |
| 198 | flkR | +0.0086 | 9.7% |
| 202 | flkR | +0.0077 | 8.6% |
| 178 | ss2 | +0.0058 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -48 | 1 | 7.7% |
| -50 | 1 | 7.7% |
| -55 | 1 | 7.7% |
| -51 | 1 | 7.7% |
| +135 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=85%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 11 | 84.6% |
| ss2 | ss1 | 1 | 7.7% |
| other | other | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 205 | flkR | 253 | other | +0.0194 | 0.4373 |
| 203 | flkR | 253 | other | +0.0136 | 0.3933 |
| 198 | flkR | 253 | other | +0.0086 | 0.4217 |
| 202 | flkR | 253 | other | +0.0077 | 0.4574 |
| 178 | ss2 | 43 | ss1 | +0.0058 | 0.0893 |

### L32 H13 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.2635

**Key mass** (top-1=35%, top-2=61%, top-3=73%)  [DISTR(S44/R183/V43)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.0910 | 34.5% |
| 183 | ss2 | +0.0695 | 26.4% |
| 43 | ss1 | +0.0316 | 12.0% |
| 178 | ss2 | +0.0166 | 6.3% |
| 38 | ss1 | +0.0166 | 6.3% |

**Query mass** (top-1=35%, top-2=61%, top-3=72%)  [DISTR(R183/S44/V178)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.0910 | 34.5% |
| 44 | ss1 | +0.0695 | 26.4% |
| 178 | ss2 | +0.0282 | 10.7% |
| 176 | ss2 | +0.0166 | 6.3% |
| 181 | ss2 | +0.0158 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +139 | 2 | 16.7% |
| -139 | 2 | 16.7% |
| +137 | 2 | 16.7% |
| -137 | 2 | 16.7% |
| +135 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 50.0% |
| ss1 | ss2 | 6 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss2 | 44 | ss1 | +0.0910 | 0.3068 |
| 44 | ss1 | 183 | ss2 | +0.0695 | 0.2342 |
| 178 | ss2 | 43 | ss1 | +0.0238 | 0.2470 |
| 176 | ss2 | 38 | ss1 | +0.0166 | 0.0743 |
| 181 | ss2 | 42 | ss1 | +0.0158 | 0.2302 |

### L32 H18 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 9  |  total attr: +0.1128

**Key mass** (top-1=22%, top-2=44%, top-3=58%)  [DISTR(G38/T176/R183/S44/L42)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0249 | 22.1% |
| 176 | ss2 | +0.0246 | 21.8% |
| 183 | ss2 | +0.0157 | 13.9% |
| 44 | ss1 | +0.0109 | 9.7% |
| 42 | ss1 | +0.0103 | 9.1% |

**Query mass** (top-1=22%, top-2=44%, top-3=58%)  [DISTR(T176/G38/S44/V178)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0249 | 22.1% |
| 38 | ss1 | +0.0246 | 21.8% |
| 44 | ss1 | +0.0157 | 13.9% |
| 178 | ss2 | +0.0138 | 12.2% |
| 183 | ss2 | +0.0109 | 9.7% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -139 | 2 | 22.2% |
| +139 | 2 | 22.2% |
| +138 | 1 | 11.1% |
| -138 | 1 | 11.1% |
| +137 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 55.6% |
| ss1 | ss2 | 4 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 176 | ss2 | 38 | ss1 | +0.0249 | 0.0679 |
| 38 | ss1 | 176 | ss2 | +0.0246 | 0.0671 |
| 44 | ss1 | 183 | ss2 | +0.0157 | 0.0321 |
| 183 | ss2 | 44 | ss1 | +0.0109 | 0.0223 |
| 181 | ss2 | 42 | ss1 | +0.0103 | 0.0914 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #5 | L0 | H19 | 2 | +0.1944 | SINGLE-ANCHOR | Y234 | SINGLE-ANCHOR | Y234 |  | INTRA:flkR |
| #25 | L4 | H10 | 9 | +0.0721 | DISTRIBUTED | Y234/F236/I221 | DUAL-ANCHOR | V149/G50 |  |  |
| #21 | L5 | H19 | 5 | +0.1490 | SINGLE-ANCHOR | G50 | MULTI-ANCHOR |  |  |  |
| #11 | L6 | H13 | 4 | +0.3216 | SINGLE-ANCHOR | V203 | SINGLE-ANCHOR | V149 |  |  |
| #22 | L6 | H19 | 7 | +0.1195 | DUAL-ANCHOR | V178/V203 | DUAL-ANCHOR | V149/V178 |  |  |
| #9 | L7 | H0 | 5 | +0.4333 | SINGLE-ANCHOR | V178 | DUAL-ANCHOR | V149/F150 |  |  |
| #1 | L9 | H10 | 9 | +0.5378 | SINGLE-ANCHOR | G50 | SINGLE-ANCHOR | V149 |  |  |
| #28 | L10 | H0 | 0 | +0.0000 | — |  | — |  |  |  |
| #2 | L10 | H9 | 17 | +0.1172 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED | V178/G45/E186/I184/G188 |  |  |
| #19 | L10 | H12 | 23 | +0.2978 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED | T177/R183/E182 |  |  |
| #26 | L11 | H8 | 14 | +0.1249 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED | T41/S44/S47/G38 |  |  |
| #13 | L11 | H14 | 18 | +0.2542 | DUAL-ANCHOR | F150/V149 | DISTRIBUTED | T177/V178/T176/E182 |  |  |
| #18 | L11 | H16 | 10 | +0.0824 | DUAL-ANCHOR | G50/?253 | DISTRIBUTED | ?-1/V43/S44/M0 |  |  |
| #7 | L12 | H8 | 25 | +0.2525 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED |  |  |  |
| #27 | L12 | H9 | 17 | +0.1593 | SINGLE-ANCHOR | V178 | DISTRIBUTED |  |  |  |
| #16 | L13 | H7 | 13 | +0.1211 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED | V178/M179/R183 |  |  |
| #14 | L13 | H12 | 18 | +0.1478 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED | V43/?-1/S44/S40/M0 |  |  |
| #17 | L13 | H14 | 12 | +0.1472 | DUAL-ANCHOR | V149/F150 | DISTRIBUTED | T176/T177/?-1/L170 |  |  |
| #20 | L15 | H6 | 17 | +0.2131 | DISTRIBUTED | L206/F150/V149 | DISTRIBUTED | R183/L219/T177/V178/V203 |  |  |
| #30 | L16 | H3 | 3 | +0.0181 | DUAL-ANCHOR | S44/V178 | DUAL-ANCHOR | S44/V178 |  | INTRA:ss2 |
| #23 | L16 | H19 | 3 | +0.0205 | DUAL-ANCHOR | ?253/G50 | DUAL-ANCHOR | R183/V178 |  |  |
| #12 | L19 | H0 | 10 | +0.1552 | DISTRIBUTED | T177/L170/T176 | DISTRIBUTED | T177/M179/V178 | POSITIONAL | INTRA:ss2 |
| #24 | L26 | H3 | 7 | +0.0436 | DISTRIBUTED | G38/M179/G50 | DISTRIBUTED | T41/E182/L42/G38/S44 |  |  |
| #6 | L26 | H16 | 5 | +0.1242 | MULTI-ANCHOR |  | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss2→ss1 |
| #4 | L27 | H15 | 7 | +0.1204 | SINGLE-ANCHOR | V178 | DISTRIBUTED | T41/V43/G38 |  | CROSS:ss1→ss2 |
| #10 | L29 | H18 | 18 | +0.1918 | DISTRIBUTED | T176/I205/S44/L35/G38 | DISTRIBUTED | G38/R183/S44/T176 |  |  |
| #29 | L30 | H1 | 5 | +0.0499 | SINGLE-ANCHOR | T41 | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss2→ss1 |
| #15 | L31 | H17 | 13 | +0.0893 | SINGLE-ANCHOR | ?253 | DISTRIBUTED |  |  |  |
| #3 | L32 | H13 | 12 | +0.2635 | DISTRIBUTED | S44/R183/V43 | DISTRIBUTED | R183/S44/V178 |  | CROSS:ss2→ss1 |
| #8 | L32 | H18 | 9 | +0.1128 | DISTRIBUTED | G38/T176/R183/S44/L42 | DISTRIBUTED | T176/G38/S44/V178 |  | CROSS:ss2→ss1 |
