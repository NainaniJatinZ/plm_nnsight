# Contact Pattern Analysis: 2YXZA

Generated: 2026-03-22 21:35:32   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2YXZA |
| Contact pair | (154, 262) |
| ss1 | [149, 160) |
| ss2 | [257, 268) |
| Clean flank | 64 |
| Corrupt flank | 63 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.6947 |
| Corrupt metric | 0.0192 |
| Gap | 0.6755 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 89.65% |
| positive IE | 50 | 74.13% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L0 | H8 | +0.5056 |
| 2 | L12 | H19 | +0.3931 |
| 3 | L32 | H18 | +0.3014 |
| 4 | L27 | H15 | +0.2922 |
| 5 | L29 | H18 | +0.2789 |
| 6 | L32 | H13 | +0.2102 |
| 7 | L14 | H9 | +0.2023 |
| 8 | L10 | H2 | +0.1981 |
| 9 | L13 | H18 | +0.1969 |
| 10 | L12 | H8 | +0.1611 |
| 11 | L11 | H8 | +0.1611 |
| 12 | L10 | H4 | +0.1394 |
| 13 | L16 | H15 | +0.1366 |
| 14 | L16 | H18 | +0.1118 |
| 15 | L17 | H10 | +0.1107 |
| 16 | L8 | H6 | +0.1058 |
| 17 | L12 | H2 | +0.1049 |
| 18 | L11 | H15 | +0.0957 |
| 19 | L16 | H19 | +0.0875 |
| 20 | L16 | H7 | +0.0861 |
| 21 | L20 | H13 | +0.0778 |
| 22 | L10 | H16 | +0.0763 |
| 23 | L26 | H16 | +0.0728 |
| 24 | L14 | H7 | +0.0691 |
| 25 | L23 | H15 | +0.0646 |
| 26 | L14 | H3 | +0.0638 |
| 27 | L14 | H10 | +0.0636 |
| 28 | L22 | H14 | +0.0607 |
| 29 | L11 | H14 | +0.0601 |
| 30 | L11 | H9 | +0.0589 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.04% |
| 4 | 0.09% |
| 5 | 0.13% |
| 6 | 0.21% |
| 7 | 0.35% |
| 8 | 0.50% |
| 9 | 0.92% |
| 10 | 1.10% |
| 20 | 2.76% |
| 80 | 113.23% |
| 450 | 153.76% |

## Cell Attribution Analysis

Total cells: 4,771,333

- Positive: 2,405,352
- Negative: 2,363,495

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000061 | 477,134 |
| 95th | +0.00000193 | 238,567 |
| 99th | +0.00001597 | 47,714 |
| 99.5th | +0.00003510 | 23,857 |
| 99.9th | +0.00020971 | 4,772 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L9 | H9 | 262 | ss2 | 85 | flkL | +0.229375 | 0.690912 |
| L12 | H19 | 153 | ss1 | 85 | flkL | +0.162913 | 0.400106 |
| L10 | H2 | 262 | ss2 | 85 | flkL | +0.156647 | 0.300449 |
| L12 | H19 | 262 | ss2 | 85 | flkL | +0.139935 | 0.454806 |
| L14 | H9 | 153 | ss1 | 85 | flkL | +0.135076 | 0.145887 |
| L16 | H15 | 153 | ss1 | 150 | ss1 | +0.134298 | 0.188022 |
| L10 | H4 | 107 | flkL | 85 | flkL | +0.127816 | 0.440756 |
| L14 | H7 | 153 | ss1 | 85 | flkL | +0.112437 | 0.227118 |
| L11 | H16 | 150 | ss1 | 262 | ss2 | +0.108244 | 0.589595 |
| L8 | H6 | 85 | flkL | 85 | flkL | +0.103454 | 0.763288 |
| L13 | H18 | 262 | ss2 | 85 | flkL | +0.094749 | 0.320482 |
| L13 | H18 | 150 | ss1 | 85 | flkL | +0.084791 | 0.476953 |
| L8 | H0 | 85 | flkL | 85 | flkL | +0.081083 | 0.410606 |
| L14 | H9 | 150 | ss1 | 85 | flkL | +0.081039 | 0.220909 |
| L12 | H8 | 150 | ss1 | 85 | flkL | +0.079525 | 0.253757 |
| L16 | H18 | 153 | ss1 | 118 | flkL | +0.070788 | 0.156725 |
| L14 | H7 | 150 | ss1 | 85 | flkL | +0.070640 | 0.211698 |
| L12 | H8 | 153 | ss1 | 85 | flkL | +0.069468 | 0.130404 |
| L13 | H18 | 153 | ss1 | 262 | ss2 | +0.066206 | 0.428120 |
| L11 | H9 | 262 | ss2 | 262 | ss2 | +0.062857 | 0.149888 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L16 | H4 | 153 | ss1 | 85 | flkL | -0.020682 | 0.239743 |
| L14 | H3 | 150 | ss1 | 85 | flkL | -0.020985 | 0.064406 |
| L13 | H18 | 133 | flkL | 85 | flkL | -0.021101 | 0.323025 |
| L10 | H16 | 85 | flkL | 85 | flkL | -0.021111 | 0.060481 |
| L14 | H7 | 163 | other | 85 | flkL | -0.022025 | 0.370943 |
| L11 | H16 | 155 | ss1 | 262 | ss2 | -0.023063 | 0.519428 |
| L12 | H19 | 152 | ss1 | 85 | flkL | -0.023902 | 0.393024 |
| L13 | H18 | 147 | flkL | 85 | flkL | -0.024640 | 0.561994 |
| L12 | H19 | 156 | ss1 | 85 | flkL | -0.024867 | 0.292303 |
| L9 | H9 | 263 | ss2 | 85 | flkL | -0.026748 | 0.650700 |
| L14 | H9 | 133 | flkL | 85 | flkL | -0.028616 | 0.192466 |
| L14 | H9 | 153 | ss1 | 262 | ss2 | -0.030061 | 0.178421 |
| L11 | H16 | 85 | flkL | 262 | ss2 | -0.037041 | 0.189687 |
| L13 | H18 | 150 | ss1 | 262 | ss2 | -0.037487 | 0.411848 |
| L11 | H16 | 262 | ss2 | 262 | ss2 | -0.044259 | 0.389223 |
| L14 | H7 | 133 | flkL | 85 | flkL | -0.045170 | 0.343031 |
| L22 | H10 | 150 | ss1 | 150 | ss1 | -0.046515 | 0.514981 |
| L13 | H18 | 262 | ss2 | 262 | ss2 | -0.061198 | 0.571730 |
| L12 | H19 | 150 | ss1 | 85 | flkL | -0.094492 | 0.374094 |
| L9 | H9 | 85 | flkL | 85 | flkL | -0.234409 | 0.451340 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0192 | 0.00% |
| 10 | 10 | 9 | 0.0192 | 0.00% |
| 20 | 20 | 14 | 0.0192 | -0.00% |
| 50 | 50 | 26 | 0.0191 | -0.00% |
| 100 | 100 | 36 | 0.0192 | -0.00% |
| 200 | 200 | 43 | 0.0687 | 7.33% |
| 500 | 500 | 49 | 0.3756 | 52.77% |
| 1000 | 1,000 | 49 | 0.6289 | 90.26% |
| 2000 | 2,000 | 50 | 0.7646 | 110.36% |
| 5000 | 5,000 | 50 | 0.8482 | 122.74% |
| 10000 | 10,000 | 50 | 0.8855 | 128.25% |
| 20000 | 20,000 | 50 | 0.9182 | 133.09% |
| 50000 | 50,000 | 50 | 0.9483 | 137.54% |

## Motif Analysis

### L0 H8 — Rank #1

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | CROSS:flkL→flkR  |  cells: 32  |  total attr: +0.1543

**Key mass** (top-1=8%, top-2=16%, top-3=24%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 98 | flkL | +0.0124 | 8.0% |
| 88 | flkL | +0.0121 | 7.9% |
| 106 | flkL | +0.0120 | 7.8% |
| 115 | flkL | +0.0105 | 6.8% |
| 126 | flkL | +0.0100 | 6.5% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.1543 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -13 | 1 | 3.1% |
| -3 | 1 | 3.1% |
| -21 | 1 | 3.1% |
| -30 | 1 | 3.1% |
| -41 | 1 | 3.1% |

**Region-pair profile** (q→k)  [CROSS:flkL→flkR]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 14 | 43.8% |
| flkL | flkL | 12 | 37.5% |
| flkL | ss1 | 3 | 9.4% |
| flkL | ss2 | 3 | 9.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 85 | flkL | 98 | flkL | +0.0124 | 0.0695 |
| 85 | flkL | 88 | flkL | +0.0121 | 0.0682 |
| 85 | flkL | 106 | flkL | +0.0120 | 0.0673 |
| 85 | flkL | 115 | flkL | +0.0105 | 0.0592 |
| 85 | flkL | 126 | flkL | +0.0100 | 0.0562 |

### L8 H6 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 34  |  total attr: +0.2713

**Key mass** (top-1=97%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.2625 | 96.8% |
| 124 | flkL | +0.0040 | 1.5% |
| 87 | flkL | +0.0017 | 0.6% |
| 122 | flkL | +0.0016 | 0.6% |
| 93 | flkL | +0.0015 | 0.5% |

**Query mass** (top-1=41%, top-2=53%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.1105 | 40.7% |
| 153 | ss1 | +0.0326 | 12.0% |
| 262 | ss2 | +0.0116 | 4.3% |
| 160 | other | +0.0114 | 4.2% |
| 163 | other | +0.0112 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 2.9% |
| +68 | 1 | 2.9% |
| +177 | 1 | 2.9% |
| +75 | 1 | 2.9% |
| +78 | 1 | 2.9% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 18 | 52.9% |
| other | flkL | 8 | 23.5% |
| ss1 | flkL | 6 | 17.6% |
| ss2 | flkL | 2 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 85 | flkL | 85 | flkL | +0.1035 | 0.7633 |
| 153 | ss1 | 85 | flkL | +0.0326 | 0.5760 |
| 262 | ss2 | 85 | flkL | +0.0116 | 0.0743 |
| 160 | other | 85 | flkL | +0.0114 | 0.5550 |
| 163 | other | 85 | flkL | +0.0112 | 0.3305 |

### L10 H2 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:flkR→flkL  |  cells: 15  |  total attr: +0.2052

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.2052 | 100.0% |

**Query mass** (top-1=76%, top-2=82%, top-3=85%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.1566 | 76.3% |
| 263 | ss2 | +0.0124 | 6.0% |
| 261 | ss2 | +0.0051 | 2.5% |
| 272 | flkR | +0.0048 | 2.3% |
| 260 | ss2 | +0.0044 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +177 | 1 | 6.7% |
| +178 | 1 | 6.7% |
| +176 | 1 | 6.7% |
| +187 | 1 | 6.7% |
| +175 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:flkR→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 6 | 40.0% |
| ss2 | flkL | 4 | 26.7% |
| other | flkL | 2 | 13.3% |
| flkL | flkL | 2 | 13.3% |
| ss1 | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 262 | ss2 | 85 | flkL | +0.1566 | 0.3004 |
| 263 | ss2 | 85 | flkL | +0.0124 | 0.3367 |
| 261 | ss2 | 85 | flkL | +0.0051 | 0.3166 |
| 272 | flkR | 85 | flkL | +0.0048 | 0.1810 |
| 260 | ss2 | 85 | flkL | +0.0044 | 0.3042 |

### L10 H4 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 6  |  total attr: +0.1469

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.1450 | 98.7% |
| 96 | flkL | +0.0018 | 1.3% |

**Query mass** (top-1=88%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 107 | flkL | +0.1297 | 88.3% |
| 111 | flkL | +0.0090 | 6.1% |
| 108 | flkL | +0.0046 | 3.2% |
| 110 | flkL | +0.0020 | 1.4% |
| 153 | ss1 | +0.0016 | 1.1% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +22 | 1 | 16.7% |
| +26 | 1 | 16.7% |
| +23 | 1 | 16.7% |
| +25 | 1 | 16.7% |
| +11 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 83.3% |
| ss1 | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 107 | flkL | 85 | flkL | +0.1278 | 0.4408 |
| 111 | flkL | 85 | flkL | +0.0090 | 0.0615 |
| 108 | flkL | 85 | flkL | +0.0046 | 0.1734 |
| 110 | flkL | 85 | flkL | +0.0020 | 0.0696 |
| 107 | flkL | 96 | flkL | +0.0018 | 0.0747 |

### L10 H16 — Rank #22

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0849

**Key mass** (top-1=53%, top-2=95%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.0451 | 53.2% |
| 262 | ss2 | +0.0358 | 42.2% |
| 80 | other | +0.0040 | 4.7% |

**Query mass** (top-1=44%, top-2=58%, top-3=66%)  [DISTR(?-1/L153/G150/L118)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0376 | 44.3% |
| 153 | ss1 | +0.0115 | 13.6% |
| 150 | ss1 | +0.0072 | 8.4% |
| 118 | flkL | +0.0042 | 5.0% |
| 262 | ss2 | +0.0040 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -86 | 1 | 5.6% |
| -109 | 1 | 5.6% |
| -112 | 1 | 5.6% |
| -144 | 1 | 5.6% |
| +182 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 7 | 38.9% |
| other | flkL | 5 | 27.8% |
| ss1 | ss2 | 3 | 16.7% |
| ss2 | other | 1 | 5.6% |
| other | ss2 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 85 | flkL | +0.0357 | 0.3842 |
| 153 | ss1 | 262 | ss2 | +0.0115 | 0.1767 |
| 150 | ss1 | 262 | ss2 | +0.0072 | 0.1717 |
| 118 | flkL | 262 | ss2 | +0.0042 | 0.1902 |
| 262 | ss2 | 80 | other | +0.0040 | 0.0188 |

### L11 H8 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 28  |  total attr: +0.1939

**Key mass** (top-1=87%, top-2=96%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.1680 | 86.6% |
| 262 | ss2 | +0.0181 | 9.3% |
| 311 | flkR | +0.0078 | 4.0% |

**Query mass** (top-1=11%, top-2=21%, top-3=31%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | ss1 | +0.0218 | 11.3% |
| 163 | other | +0.0197 | 10.2% |
| 148 | flkL | +0.0185 | 9.5% |
| 85 | flkL | +0.0168 | 8.6% |
| 155 | ss1 | +0.0165 | 8.5% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +65 | 1 | 3.6% |
| +78 | 1 | 3.6% |
| +63 | 1 | 3.6% |
| +70 | 1 | 3.6% |
| +67 | 1 | 3.6% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 12 | 42.9% |
| ss1 | flkL | 9 | 32.1% |
| other | flkL | 3 | 10.7% |
| flkL | ss2 | 1 | 3.6% |
| ss1 | ss2 | 1 | 3.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 150 | ss1 | 85 | flkL | +0.0218 | 0.2458 |
| 163 | other | 85 | flkL | +0.0197 | 0.4283 |
| 148 | flkL | 85 | flkL | +0.0185 | 0.3772 |
| 155 | ss1 | 85 | flkL | +0.0165 | 0.3128 |
| 152 | ss1 | 85 | flkL | +0.0129 | 0.3136 |

### L11 H9 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 21  |  total attr: +0.1265

**Key mass** (top-1=50%, top-2=60%, top-3=67%)  [DISTR(L262/F85/Y154/A156)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0629 | 49.7% |
| 85 | flkL | +0.0125 | 9.9% |
| 154 | ss1 | +0.0089 | 7.0% |
| 156 | ss1 | +0.0056 | 4.4% |
| 263 | ss2 | +0.0052 | 4.1% |

**Query mass** (top-1=55%, top-2=69%, top-3=76%)  [DISTR(L262/F85/L148)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0699 | 55.2% |
| 85 | flkL | +0.0173 | 13.6% |
| 148 | flkL | +0.0089 | 7.0% |
| 150 | ss1 | +0.0071 | 5.6% |
| 146 | flkL | +0.0034 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 52%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 6 | 28.6% |
| +0 | 5 | 23.8% |
| +1 | 2 | 9.5% |
| -7 | 2 | 9.5% |
| -1 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 6 | 28.6% |
| ss2 | ss2 | 4 | 19.0% |
| ss1 | ss1 | 4 | 19.0% |
| flkL | ss1 | 3 | 14.3% |
| ss1 | other | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 262 | ss2 | 262 | ss2 | +0.0629 | 0.1499 |
| 85 | flkL | 85 | flkL | +0.0125 | 0.1279 |
| 148 | flkL | 154 | ss1 | +0.0089 | 0.2587 |
| 150 | ss1 | 156 | ss1 | +0.0056 | 0.1859 |
| 146 | flkL | 152 | ss1 | +0.0034 | 0.2034 |

### L11 H14 — Rank #29

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.1003

**Key mass** (top-1=37%, top-2=73%, top-3=79%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.0376 | 37.5% |
| 262 | ss2 | +0.0353 | 35.2% |
| 107 | flkL | +0.0065 | 6.5% |
| 153 | ss1 | +0.0059 | 5.9% |
| 135 | flkL | +0.0036 | 3.5% |

**Query mass** (top-1=25%, top-2=40%, top-3=50%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0251 | 25.0% |
| 111 | flkL | +0.0145 | 14.5% |
| 85 | flkL | +0.0105 | 10.5% |
| 150 | ss1 | +0.0081 | 8.0% |
| 137 | flkL | +0.0074 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +26 | 1 | 3.8% |
| -177 | 1 | 3.8% |
| +65 | 1 | 3.8% |
| -125 | 1 | 3.8% |
| +22 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 10 | 38.5% |
| ss2 | flkL | 5 | 19.2% |
| flkL | flkL | 3 | 11.5% |
| ss1 | flkL | 3 | 11.5% |
| ss2 | ss1 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 111 | flkL | 85 | flkL | +0.0145 | 0.2640 |
| 85 | flkL | 262 | ss2 | +0.0083 | 0.0933 |
| 150 | ss1 | 85 | flkL | +0.0081 | 0.0474 |
| 137 | flkL | 262 | ss2 | +0.0074 | 0.1905 |
| 107 | flkL | 85 | flkL | +0.0066 | 0.1402 |

### L11 H15 — Rank #18

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0963

**Key mass** (top-1=48%, top-2=68%, top-3=86%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0462 | 48.0% |
| 85 | flkL | +0.0194 | 20.2% |
| 311 | flkR | +0.0168 | 17.4% |
| 245 | other | +0.0019 | 2.0% |
| 107 | flkL | +0.0019 | 1.9% |

**Query mass** (top-1=26%, top-2=40%, top-3=52%)  [DISTR(L262/G150/Y154/L153/A156)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0251 | 26.0% |
| 150 | ss1 | +0.0131 | 13.6% |
| 154 | ss1 | +0.0122 | 12.7% |
| 153 | ss1 | +0.0104 | 10.8% |
| 156 | ss1 | +0.0096 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -108 | 1 | 3.8% |
| -49 | 1 | 3.8% |
| -106 | 1 | 3.8% |
| -107 | 1 | 3.8% |
| +65 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 7 | 26.9% |
| ss1 | flkL | 6 | 23.1% |
| ss1 | ss2 | 5 | 19.2% |
| ss2 | flkR | 2 | 7.7% |
| ss1 | flkR | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 154 | ss1 | 262 | ss2 | +0.0096 | 0.2621 |
| 262 | ss2 | 311 | flkR | +0.0090 | 0.0543 |
| 156 | ss1 | 262 | ss2 | +0.0073 | 0.1210 |
| 155 | ss1 | 262 | ss2 | +0.0072 | 0.2496 |
| 150 | ss1 | 85 | flkL | +0.0070 | 0.0662 |

### L12 H2 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.1571

**Key mass** (top-1=87%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.1361 | 86.6% |
| 85 | flkL | +0.0211 | 13.4% |

**Query mass** (top-1=36%, top-2=52%, top-3=65%)  [DISTR(F85/G150/L153/L262)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.0566 | 36.0% |
| 150 | ss1 | +0.0256 | 16.3% |
| 153 | ss1 | +0.0195 | 12.4% |
| 262 | ss2 | +0.0154 | 9.8% |
| 156 | ss1 | +0.0091 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -177 | 1 | 6.7% |
| -112 | 1 | 6.7% |
| -109 | 1 | 6.7% |
| +177 | 1 | 6.7% |
| -106 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 53.3% |
| flkL | ss2 | 4 | 26.7% |
| ss2 | flkL | 1 | 6.7% |
| flkR | flkL | 1 | 6.7% |
| other | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 85 | flkL | 262 | ss2 | +0.0566 | 0.3408 |
| 150 | ss1 | 262 | ss2 | +0.0256 | 0.0884 |
| 153 | ss1 | 262 | ss2 | +0.0195 | 0.0924 |
| 262 | ss2 | 85 | flkL | +0.0154 | 0.0965 |
| 156 | ss1 | 262 | ss2 | +0.0091 | 0.2188 |

### L12 H8 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.3111

**Key mass** (top-1=93%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.2886 | 92.8% |
| 262 | ss2 | +0.0211 | 6.8% |
| 88 | flkL | +0.0014 | 0.4% |

**Query mass** (top-1=26%, top-2=48%, top-3=62%)  [DISTR(G150/L153/L262/T163)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | ss1 | +0.0795 | 25.6% |
| 153 | ss1 | +0.0695 | 22.3% |
| 262 | ss2 | +0.0441 | 14.2% |
| 163 | other | +0.0435 | 14.0% |
| 118 | flkL | +0.0128 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +65 | 1 | 3.6% |
| +68 | 1 | 3.6% |
| +78 | 1 | 3.6% |
| +177 | 1 | 3.6% |
| +33 | 1 | 3.6% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 8 | 28.6% |
| flkL | flkL | 6 | 21.4% |
| ss2 | flkL | 5 | 17.9% |
| ss1 | flkL | 4 | 14.3% |
| flkL | ss2 | 3 | 10.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 150 | ss1 | 85 | flkL | +0.0795 | 0.2538 |
| 153 | ss1 | 85 | flkL | +0.0695 | 0.1304 |
| 163 | other | 85 | flkL | +0.0435 | 0.4250 |
| 262 | ss2 | 85 | flkL | +0.0427 | 0.1425 |
| 118 | flkL | 85 | flkL | +0.0128 | 0.2396 |

### L12 H19 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 45  |  total attr: +0.5571

**Key mass** (top-1=96%, top-2=98%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.5375 | 96.5% |
| 262 | ss2 | +0.0064 | 1.1% |
| 118 | flkL | +0.0045 | 0.8% |
| 87 | flkL | +0.0015 | 0.3% |
| 130 | flkL | +0.0015 | 0.3% |

**Query mass** (top-1=31%, top-2=56%, top-3=59%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.1710 | 30.7% |
| 262 | ss2 | +0.1399 | 25.1% |
| 158 | ss1 | +0.0172 | 3.1% |
| 141 | flkL | +0.0162 | 2.9% |
| 132 | flkL | +0.0153 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +61 | 2 | 4.4% |
| +48 | 2 | 4.4% |
| +44 | 2 | 4.4% |
| +68 | 1 | 2.2% |
| +177 | 1 | 2.2% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 18 | 40.0% |
| ss1 | flkL | 13 | 28.9% |
| other | flkL | 4 | 8.9% |
| ss2 | flkL | 3 | 6.7% |
| flkR | flkL | 3 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 85 | flkL | +0.1629 | 0.4001 |
| 262 | ss2 | 85 | flkL | +0.1399 | 0.4548 |
| 158 | ss1 | 85 | flkL | +0.0172 | 0.3627 |
| 141 | flkL | 85 | flkL | +0.0162 | 0.3928 |
| 132 | flkL | 85 | flkL | +0.0153 | 0.2450 |

### L13 H18 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 56  |  total attr: +0.5048

**Key mass** (top-1=57%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.2853 | 56.5% |
| 262 | ss2 | +0.2194 | 43.5% |

**Query mass** (top-1=19%, top-2=38%, top-3=55%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.0971 | 19.2% |
| 262 | ss2 | +0.0947 | 18.8% |
| 150 | ss1 | +0.0848 | 16.8% |
| 163 | other | +0.0209 | 4.1% |
| 118 | flkL | +0.0159 | 3.1% |

**Offset distribution [frequency]** (top-2 coverage: 4%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +177 | 1 | 1.8% |
| +65 | 1 | 1.8% |
| -109 | 1 | 1.8% |
| +68 | 1 | 1.8% |
| -144 | 1 | 1.8% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 18 | 32.1% |
| ss2 | ss2 | 7 | 12.5% |
| flkR | ss2 | 7 | 12.5% |
| ss1 | flkL | 6 | 10.7% |
| ss1 | ss2 | 6 | 10.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 262 | ss2 | 85 | flkL | +0.0947 | 0.3205 |
| 150 | ss1 | 85 | flkL | +0.0848 | 0.4770 |
| 153 | ss1 | 262 | ss2 | +0.0662 | 0.4281 |
| 153 | ss1 | 85 | flkL | +0.0309 | 0.5192 |
| 118 | flkL | 262 | ss2 | +0.0159 | 0.3458 |

### L14 H3 — Rank #26

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0728

**Key mass** (top-1=36%, top-2=61%, top-3=84%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0262 | 36.0% |
| 85 | flkL | +0.0184 | 25.3% |
| 118 | flkL | +0.0168 | 23.1% |
| 89 | flkL | +0.0046 | 6.3% |
| 107 | flkL | +0.0024 | 3.2% |

**Query mass** (top-1=37%, top-2=59%, top-3=71%)  [DISTR(L153/L262/F85)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.0268 | 36.8% |
| 262 | ss2 | +0.0165 | 22.6% |
| 85 | flkL | +0.0081 | 11.2% |
| 150 | ss1 | +0.0037 | 5.1% |
| 156 | ss1 | +0.0037 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +36 | 2 | 9.5% |
| +154 | 1 | 4.8% |
| +177 | 1 | 4.8% |
| +86 | 1 | 4.8% |
| +144 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 8 | 38.1% |
| ss1 | other | 4 | 19.0% |
| ss2 | flkL | 3 | 14.3% |
| flkL | other | 2 | 9.5% |
| other | flkL | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | -1 | other | +0.0111 | 0.0465 |
| 262 | ss2 | 85 | flkL | +0.0100 | 0.0799 |
| 85 | flkL | -1 | other | +0.0081 | 0.1315 |
| 262 | ss2 | 118 | flkL | +0.0065 | 0.0705 |
| 153 | ss1 | 118 | flkL | +0.0058 | 0.0143 |

### L14 H7 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.3177

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.3092 | 97.3% |
| 262 | ss2 | +0.0068 | 2.1% |
| -1 | other | +0.0017 | 0.5% |

**Query mass** (top-1=35%, top-2=59%, top-3=68%)  [DISTR(L153/G150/Y154/L155)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.1124 | 35.4% |
| 150 | ss1 | +0.0753 | 23.7% |
| 154 | ss1 | +0.0298 | 9.4% |
| 155 | ss1 | +0.0259 | 8.1% |
| 262 | ss2 | +0.0106 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +68 | 1 | 3.8% |
| +65 | 1 | 3.8% |
| +69 | 1 | 3.8% |
| +70 | 1 | 3.8% |
| +177 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 23.1% |
| ss2 | flkL | 6 | 23.1% |
| other | flkL | 6 | 23.1% |
| flkR | flkL | 4 | 15.4% |
| ss1 | ss2 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 85 | flkL | +0.1124 | 0.2271 |
| 150 | ss1 | 85 | flkL | +0.0706 | 0.2117 |
| 154 | ss1 | 85 | flkL | +0.0298 | 0.2537 |
| 155 | ss1 | 85 | flkL | +0.0237 | 0.2588 |
| 262 | ss2 | 85 | flkL | +0.0106 | 0.4336 |

### L14 H9 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 37  |  total attr: +0.3967

**Key mass** (top-1=65%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 85 | flkL | +0.2564 | 64.6% |
| 262 | ss2 | +0.1256 | 31.7% |
| 118 | flkL | +0.0067 | 1.7% |
| 311 | flkR | +0.0036 | 0.9% |
| -1 | other | +0.0031 | 0.8% |

**Query mass** (top-1=35%, top-2=65%, top-3=69%)  [DISTR(L153/G150/L118/L155)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.1403 | 35.4% |
| 150 | ss1 | +0.1174 | 29.6% |
| 118 | flkL | +0.0179 | 4.5% |
| 155 | ss1 | +0.0140 | 3.5% |
| 154 | ss1 | +0.0135 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +68 | 1 | 2.7% |
| +65 | 1 | 2.7% |
| -112 | 1 | 2.7% |
| -144 | 1 | 2.7% |
| +70 | 1 | 2.7% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 17 | 45.9% |
| ss1 | flkL | 7 | 18.9% |
| ss1 | ss2 | 5 | 13.5% |
| other | flkL | 2 | 5.4% |
| flkR | flkR | 1 | 2.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 85 | flkL | +0.1351 | 0.1459 |
| 150 | ss1 | 85 | flkL | +0.0810 | 0.2209 |
| 150 | ss1 | 262 | ss2 | +0.0363 | 0.3010 |
| 118 | flkL | 262 | ss2 | +0.0179 | 0.4834 |
| 155 | ss1 | 85 | flkL | +0.0140 | 0.1526 |

### L14 H10 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.1295

**Key mass** (top-1=62%, top-2=80%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0809 | 62.4% |
| 310 | flkR | +0.0231 | 17.8% |
| 311 | flkR | +0.0123 | 9.5% |
| 261 | ss2 | +0.0034 | 2.6% |
| 260 | ss2 | +0.0022 | 1.7% |

**Query mass** (top-1=33%, top-2=53%, top-3=69%)  [DISTR(L153/G150/L262/L155)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.0432 | 33.3% |
| 150 | ss1 | +0.0257 | 19.9% |
| 262 | ss2 | +0.0209 | 16.1% |
| 155 | ss1 | +0.0097 | 7.5% |
| 163 | other | +0.0096 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -48 | 2 | 9.5% |
| -107 | 2 | 9.5% |
| -108 | 2 | 9.5% |
| -109 | 1 | 4.8% |
| -112 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 33.3% |
| ss2 | flkR | 7 | 33.3% |
| other | flkR | 5 | 23.8% |
| ss1 | flkR | 1 | 4.8% |
| flkL | ss2 | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 262 | ss2 | +0.0376 | 0.0690 |
| 150 | ss1 | 262 | ss2 | +0.0239 | 0.1361 |
| 262 | ss2 | 310 | flkR | +0.0107 | 0.0838 |
| 262 | ss2 | 311 | flkR | +0.0102 | 0.0996 |
| 155 | ss1 | 262 | ss2 | +0.0097 | 0.0905 |

### L16 H7 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 41  |  total attr: +0.2613

**Key mass** (top-1=69%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.1799 | 68.8% |
| 85 | flkL | +0.0732 | 28.0% |
| -1 | other | +0.0082 | 3.1% |

**Query mass** (top-1=21%, top-2=34%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.0556 | 21.3% |
| 150 | ss1 | +0.0328 | 12.5% |
| 157 | ss1 | +0.0145 | 5.6% |
| 163 | other | +0.0134 | 5.1% |
| 147 | flkL | +0.0118 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 4.9% |
| -109 | 1 | 2.4% |
| +65 | 1 | 2.4% |
| -105 | 1 | 2.4% |
| -99 | 1 | 2.4% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 9 | 22.0% |
| ss1 | ss2 | 7 | 17.1% |
| flkL | flkL | 6 | 14.6% |
| ss1 | flkL | 5 | 12.2% |
| other | ss2 | 3 | 7.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 262 | ss2 | +0.0537 | 0.2218 |
| 150 | ss1 | 85 | flkL | +0.0307 | 0.1452 |
| 157 | ss1 | 262 | ss2 | +0.0145 | 0.2260 |
| 163 | other | 262 | ss2 | +0.0134 | 0.1115 |
| 147 | flkL | 262 | ss2 | +0.0118 | 0.2949 |

### L16 H15 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 6  |  total attr: +0.1758

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | ss1 | +0.1729 | 98.3% |
| 262 | ss2 | +0.0029 | 1.7% |

**Query mass** (top-1=76%, top-2=91%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.1343 | 76.4% |
| 155 | ss1 | +0.0253 | 14.4% |
| 156 | ss1 | +0.0072 | 4.1% |
| 154 | ss1 | +0.0048 | 2.7% |
| 263 | ss2 | +0.0029 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 1 | 16.7% |
| +5 | 1 | 16.7% |
| +6 | 1 | 16.7% |
| +4 | 1 | 16.7% |
| +1 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 4 | 66.7% |
| ss2 | ss2 | 1 | 16.7% |
| flkL | ss1 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 150 | ss1 | +0.1343 | 0.1880 |
| 155 | ss1 | 150 | ss1 | +0.0253 | 0.1469 |
| 156 | ss1 | 150 | ss1 | +0.0072 | 0.0955 |
| 154 | ss1 | 150 | ss1 | +0.0048 | 0.2005 |
| 263 | ss2 | 262 | ss2 | +0.0029 | 0.1416 |

### L16 H18 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 19  |  total attr: +0.1496

**Key mass** (top-1=61%, top-2=75%, top-3=87%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | flkL | +0.0917 | 61.3% |
| 120 | flkL | +0.0208 | 13.9% |
| 262 | ss2 | +0.0176 | 11.8% |
| 121 | flkL | +0.0089 | 6.0% |
| 119 | flkL | +0.0048 | 3.2% |

**Query mass** (top-1=69%, top-2=76%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.1030 | 68.9% |
| 155 | ss1 | +0.0103 | 6.9% |
| 263 | ss2 | +0.0070 | 4.7% |
| 156 | ss1 | +0.0066 | 4.4% |
| 260 | ss2 | +0.0057 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +35 | 2 | 10.5% |
| +33 | 2 | 10.5% |
| +1 | 2 | 10.5% |
| +34 | 2 | 10.5% |
| +36 | 2 | 10.5% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 11 | 57.9% |
| ss2 | ss2 | 4 | 21.1% |
| ss1 | ss1 | 2 | 10.5% |
| other | flkL | 1 | 5.3% |
| flkL | flkL | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 118 | flkL | +0.0708 | 0.1567 |
| 153 | ss1 | 120 | flkL | +0.0169 | 0.0391 |
| 153 | ss1 | 121 | flkL | +0.0073 | 0.0179 |
| 263 | ss2 | 262 | ss2 | +0.0070 | 0.2655 |
| 155 | ss1 | 118 | flkL | +0.0063 | 0.0538 |

### L16 H19 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.1233

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.1233 | 100.0% |

**Query mass** (top-1=38%, top-2=55%, top-3=68%)  [DISTR(L153/G150/L155/G157)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.0471 | 38.2% |
| 150 | ss1 | +0.0210 | 17.0% |
| 155 | ss1 | +0.0151 | 12.3% |
| 157 | ss1 | +0.0089 | 7.2% |
| 154 | ss1 | +0.0084 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -109 | 1 | 9.1% |
| -112 | 1 | 9.1% |
| -107 | 1 | 9.1% |
| -105 | 1 | 9.1% |
| -108 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 72.7% |
| other | ss2 | 2 | 18.2% |
| flkL | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 262 | ss2 | +0.0471 | 0.1686 |
| 150 | ss1 | 262 | ss2 | +0.0210 | 0.1340 |
| 155 | ss1 | 262 | ss2 | +0.0151 | 0.1624 |
| 157 | ss1 | 262 | ss2 | +0.0089 | 0.1594 |
| 154 | ss1 | 262 | ss2 | +0.0084 | 0.1335 |

### L17 H10 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 17  |  total attr: +0.1383

**Key mass** (top-1=87%, top-2=92%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.1206 | 87.1% |
| 133 | flkL | +0.0064 | 4.6% |
| 262 | ss2 | +0.0056 | 4.0% |
| 155 | ss1 | +0.0041 | 3.0% |
| 131 | flkL | +0.0017 | 1.2% |

**Query mass** (top-1=21%, top-2=40%, top-3=58%)  [DISTR(L155/Y154/L153/A156)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 155 | ss1 | +0.0284 | 20.6% |
| 154 | ss1 | +0.0267 | 19.3% |
| 153 | ss1 | +0.0249 | 18.0% |
| 156 | ss1 | +0.0172 | 12.5% |
| 151 | ss1 | +0.0089 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 17.6% |
| +2 | 2 | 11.8% |
| +1 | 2 | 11.8% |
| -2 | 2 | 11.8% |
| +3 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=65%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 64.7% |
| flkL | flkL | 2 | 11.8% |
| ss2 | ss2 | 1 | 5.9% |
| flkL | ss1 | 1 | 5.9% |
| other | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 155 | ss1 | 153 | ss1 | +0.0284 | 0.4261 |
| 154 | ss1 | 153 | ss1 | +0.0267 | 0.4900 |
| 153 | ss1 | 153 | ss1 | +0.0249 | 0.3019 |
| 156 | ss1 | 153 | ss1 | +0.0153 | 0.4841 |
| 151 | ss1 | 153 | ss1 | +0.0089 | 0.4632 |

### L20 H13 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | POSITIONAL | INTRA:ss1  |  cells: 10  |  total attr: +0.0985

**Key mass** (top-1=82%, top-2=88%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 150 | ss1 | +0.0813 | 82.5% |
| 147 | flkL | +0.0055 | 5.6% |
| 149 | ss1 | +0.0032 | 3.2% |
| 160 | other | +0.0030 | 3.0% |
| 153 | ss1 | +0.0027 | 2.8% |

**Query mass** (top-1=42%, top-2=68%, top-3=86%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 153 | ss1 | +0.0410 | 41.6% |
| 155 | ss1 | +0.0265 | 26.9% |
| 154 | ss1 | +0.0170 | 17.2% |
| 150 | ss1 | +0.0030 | 3.0% |
| 163 | other | +0.0030 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 80%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 5 | 50.0% |
| +3 | 3 | 30.0% |
| +5 | 1 | 10.0% |
| +10 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 50.0% |
| ss1 | flkL | 2 | 20.0% |
| flkL | flkL | 2 | 20.0% |
| other | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 153 | ss1 | 150 | ss1 | +0.0378 | 0.3517 |
| 155 | ss1 | 150 | ss1 | +0.0265 | 0.3417 |
| 154 | ss1 | 150 | ss1 | +0.0170 | 0.1418 |
| 153 | ss1 | 149 | ss1 | +0.0032 | 0.2227 |
| 150 | ss1 | 147 | flkL | +0.0030 | 0.1553 |

### L22 H14 — Rank #28

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 14  |  total attr: +0.0488

**Key mass** (top-1=43%, top-2=63%, top-3=81%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0209 | 42.7% |
| 260 | ss2 | +0.0101 | 20.7% |
| 261 | ss2 | +0.0086 | 17.6% |
| 153 | ss1 | +0.0047 | 9.6% |
| 263 | ss2 | +0.0026 | 5.2% |

**Query mass** (top-1=37%, top-2=59%, top-3=76%)  [DISTR(Y154/L153/L155)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 154 | ss1 | +0.0179 | 36.7% |
| 153 | ss1 | +0.0108 | 22.2% |
| 155 | ss1 | +0.0085 | 17.3% |
| 156 | ss1 | +0.0049 | 10.1% |
| 263 | ss2 | +0.0047 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -107 | 3 | 21.4% |
| -106 | 3 | 21.4% |
| -108 | 2 | 14.3% |
| +110 | 1 | 7.1% |
| -109 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 12 | 85.7% |
| ss2 | ss1 | 2 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 154 | ss1 | 262 | ss2 | +0.0117 | 0.1291 |
| 263 | ss2 | 153 | ss1 | +0.0047 | 0.0489 |
| 154 | ss1 | 261 | ss2 | +0.0038 | 0.1817 |
| 153 | ss1 | 262 | ss2 | +0.0038 | 0.0746 |
| 155 | ss1 | 260 | ss2 | +0.0036 | 0.0481 |

### L23 H15 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 7  |  total attr: +0.0979

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0952 | 97.3% |
| 85 | flkL | +0.0014 | 1.4% |
| 260 | ss2 | +0.0013 | 1.3% |

**Query mass** (top-1=59%, top-2=77%, top-3=93%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 154 | ss1 | +0.0576 | 58.8% |
| 155 | ss1 | +0.0176 | 18.0% |
| 156 | ss1 | +0.0158 | 16.1% |
| 153 | ss1 | +0.0038 | 3.9% |
| 152 | ss1 | +0.0017 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -108 | 1 | 14.3% |
| -107 | 1 | 14.3% |
| -106 | 1 | 14.3% |
| -109 | 1 | 14.3% |
| -110 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 85.7% |
| ss2 | flkL | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 154 | ss1 | 262 | ss2 | +0.0576 | 0.5579 |
| 155 | ss1 | 262 | ss2 | +0.0164 | 0.2174 |
| 156 | ss1 | 262 | ss2 | +0.0158 | 0.1980 |
| 153 | ss1 | 262 | ss2 | +0.0038 | 0.3153 |
| 152 | ss1 | 262 | ss2 | +0.0017 | 0.2055 |

### L26 H16 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0398

**Key mass** (top-1=19%, top-2=32%, top-3=46%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 287 | flkR | +0.0074 | 18.6% |
| 284 | flkR | +0.0055 | 13.8% |
| 152 | ss1 | +0.0054 | 13.7% |
| 286 | flkR | +0.0048 | 12.0% |
| 259 | ss2 | +0.0035 | 8.7% |

**Query mass** (top-1=22%, top-2=40%, top-3=50%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 154 | ss1 | +0.0087 | 21.7% |
| 264 | ss2 | +0.0072 | 18.1% |
| 159 | ss1 | +0.0040 | 10.1% |
| 151 | ss1 | +0.0033 | 8.3% |
| 265 | ss2 | +0.0031 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -130 | 2 | 11.1% |
| +112 | 1 | 5.6% |
| +114 | 1 | 5.6% |
| -25 | 1 | 5.6% |
| -98 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 6 | 33.3% |
| ss1 | ss2 | 5 | 27.8% |
| ss2 | ss1 | 4 | 22.2% |
| ss2 | flkR | 3 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 154 | ss1 | 284 | flkR | +0.0055 | 0.1243 |
| 264 | ss2 | 152 | ss1 | +0.0054 | 0.1015 |
| 265 | ss2 | 151 | ss1 | +0.0031 | 0.2358 |
| 262 | ss2 | 287 | flkR | +0.0026 | 0.0972 |
| 159 | ss1 | 257 | ss2 | +0.0020 | 0.0579 |

### L27 H15 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 25  |  total attr: +0.1412

**Key mass** (top-1=22%, top-2=36%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 154 | ss1 | +0.0310 | 22.0% |
| 262 | ss2 | +0.0194 | 13.7% |
| 264 | ss2 | +0.0163 | 11.5% |
| 260 | ss2 | +0.0158 | 11.2% |
| 263 | ss2 | +0.0121 | 8.6% |

**Query mass** (top-1=20%, top-2=34%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 262 | ss2 | +0.0280 | 19.8% |
| 152 | ss1 | +0.0195 | 13.8% |
| 154 | ss1 | +0.0194 | 13.7% |
| 155 | ss1 | +0.0119 | 8.4% |
| 264 | ss2 | +0.0110 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 2 | 8.0% |
| -104 | 2 | 8.0% |
| +110 | 2 | 8.0% |
| +104 | 2 | 8.0% |
| +112 | 2 | 8.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 13 | 52.0% |
| ss1 | ss2 | 9 | 36.0% |
| ss2 | flkL | 1 | 4.0% |
| ss1 | flkR | 1 | 4.0% |
| ss2 | flkR | 1 | 4.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 262 | ss2 | 154 | ss1 | +0.0245 | 0.3643 |
| 154 | ss1 | 262 | ss2 | +0.0194 | 0.2834 |
| 152 | ss1 | 264 | ss2 | +0.0143 | 0.1328 |
| 155 | ss1 | 260 | ss2 | +0.0088 | 0.1943 |
| 156 | ss1 | 260 | ss2 | +0.0070 | 0.0826 |

### L29 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 38  |  total attr: +0.1828

**Key mass** (top-1=13%, top-2=26%, top-3=37%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 285 | flkR | +0.0239 | 13.1% |
| 265 | ss2 | +0.0231 | 12.6% |
| 263 | ss2 | +0.0210 | 11.5% |
| 259 | ss2 | +0.0192 | 10.5% |
| 152 | ss1 | +0.0149 | 8.2% |

**Query mass** (top-1=15%, top-2=28%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 151 | ss1 | +0.0277 | 15.2% |
| 154 | ss1 | +0.0233 | 12.7% |
| 156 | ss1 | +0.0217 | 11.9% |
| 153 | ss1 | +0.0197 | 10.8% |
| 266 | ss2 | +0.0164 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -131 | 2 | 5.3% |
| +114 | 2 | 5.3% |
| -136 | 2 | 5.3% |
| -115 | 2 | 5.3% |
| -105 | 2 | 5.3% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 14 | 36.8% |
| ss1 | flkR | 12 | 31.6% |
| ss2 | ss1 | 5 | 13.2% |
| flkR | ss1 | 3 | 7.9% |
| flkL | ss2 | 2 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 151 | ss1 | 265 | ss2 | +0.0231 | 0.2263 |
| 153 | ss1 | 263 | ss2 | +0.0197 | 0.2506 |
| 154 | ss1 | 285 | flkR | +0.0181 | 0.6835 |
| 156 | ss1 | 259 | ss2 | +0.0151 | 0.3865 |
| 266 | ss2 | 152 | ss1 | +0.0149 | 0.3788 |

### L32 H13 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 24  |  total attr: +0.1021

**Key mass** (top-1=20%, top-2=32%, top-3=42%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 259 | ss2 | +0.0201 | 19.6% |
| 151 | ss1 | +0.0128 | 12.5% |
| 156 | ss1 | +0.0097 | 9.5% |
| 266 | ss2 | +0.0096 | 9.4% |
| 154 | ss1 | +0.0094 | 9.2% |

**Query mass** (top-1=16%, top-2=28%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss1 | +0.0164 | 16.1% |
| 264 | ss2 | +0.0122 | 12.0% |
| 266 | ss2 | +0.0117 | 11.5% |
| 259 | ss2 | +0.0101 | 9.9% |
| 265 | ss2 | +0.0086 | 8.5% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 8.3% |
| -104 | 2 | 8.3% |
| -114 | 2 | 8.3% |
| +104 | 2 | 8.3% |
| +112 | 2 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 13 | 54.2% |
| ss1 | ss2 | 11 | 45.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss1 | 259 | ss2 | +0.0114 | 0.1425 |
| 264 | ss2 | 154 | ss1 | +0.0094 | 0.0935 |
| 265 | ss2 | 151 | ss1 | +0.0086 | 0.1887 |
| 154 | ss1 | 264 | ss2 | +0.0075 | 0.0748 |
| 259 | ss2 | 156 | ss1 | +0.0068 | 0.0850 |

### L32 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 23  |  total attr: +0.1389

**Key mass** (top-1=15%, top-2=26%, top-3=37%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 263 | ss2 | +0.0204 | 14.7% |
| 260 | ss2 | +0.0158 | 11.4% |
| 151 | ss1 | +0.0154 | 11.1% |
| 264 | ss2 | +0.0154 | 11.1% |
| 156 | ss1 | +0.0144 | 10.4% |

**Query mass** (top-1=14%, top-2=26%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 263 | ss2 | +0.0190 | 13.7% |
| 151 | ss1 | +0.0166 | 11.9% |
| 260 | ss2 | +0.0156 | 11.2% |
| 156 | ss1 | +0.0137 | 9.8% |
| 152 | ss1 | +0.0120 | 8.6% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 2 | 8.7% |
| +112 | 2 | 8.7% |
| +104 | 2 | 8.7% |
| +110 | 2 | 8.7% |
| +108 | 2 | 8.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 14 | 60.9% |
| ss1 | ss2 | 9 | 39.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 151 | ss1 | 263 | ss2 | +0.0166 | 0.1945 |
| 152 | ss1 | 264 | ss2 | +0.0120 | 0.0803 |
| 263 | ss2 | 151 | ss1 | +0.0097 | 0.1139 |
| 156 | ss1 | 260 | ss2 | +0.0096 | 0.0515 |
| 260 | ss2 | 156 | ss1 | +0.0094 | 0.0506 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #1 | L0 | H8 | 32 | +0.1543 | DISTRIBUTED |  | SINGLE-ANCHOR | F85 |  | CROSS:flkL→flkR |
| #16 | L8 | H6 | 34 | +0.2713 | SINGLE-ANCHOR | F85 | DISTRIBUTED |  |  | INTRA:flkL |
| #8 | L10 | H2 | 15 | +0.2052 | SINGLE-ANCHOR | F85 | SINGLE-ANCHOR | L262 |  | CROSS:flkR→flkL |
| #12 | L10 | H4 | 6 | +0.1469 | SINGLE-ANCHOR | F85 | SINGLE-ANCHOR | A107 |  | INTRA:flkL |
| #22 | L10 | H16 | 18 | +0.0849 | DUAL-ANCHOR | F85/L262 | DISTRIBUTED | ?-1/L153/G150/L118 |  |  |
| #11 | L11 | H8 | 28 | +0.1939 | SINGLE-ANCHOR | F85 | DISTRIBUTED |  |  | INTRA:flkL |
| #30 | L11 | H9 | 21 | +0.1265 | DISTRIBUTED | L262/F85/Y154/A156 | DISTRIBUTED | L262/F85/L148 | POSITIONAL |  |
| #29 | L11 | H14 | 26 | +0.1003 | DUAL-ANCHOR | F85/L262 | DISTRIBUTED |  |  |  |
| #18 | L11 | H15 | 26 | +0.0963 | MULTI-ANCHOR |  | DISTRIBUTED | L262/G150/Y154/L153/A156 |  |  |
| #17 | L12 | H2 | 15 | +0.1571 | SINGLE-ANCHOR | L262 | DISTRIBUTED | F85/G150/L153/L262 |  | CROSS:ss1→ss2 |
| #10 | L12 | H8 | 28 | +0.3111 | SINGLE-ANCHOR | F85 | DISTRIBUTED | G150/L153/L262/T163 |  |  |
| #2 | L12 | H19 | 45 | +0.5571 | SINGLE-ANCHOR | F85 | DISTRIBUTED |  |  | INTRA:flkL |
| #9 | L13 | H18 | 56 | +0.5048 | DUAL-ANCHOR | F85/L262 | DISTRIBUTED |  |  |  |
| #26 | L14 | H3 | 21 | +0.0728 | MULTI-ANCHOR |  | DISTRIBUTED | L153/L262/F85 |  |  |
| #24 | L14 | H7 | 26 | +0.3177 | SINGLE-ANCHOR | F85 | DISTRIBUTED | L153/G150/Y154/L155 |  |  |
| #7 | L14 | H9 | 37 | +0.3967 | SINGLE-ANCHOR | F85 | DISTRIBUTED | L153/G150/L118/L155 |  | CROSS:flkL→ss2 |
| #27 | L14 | H10 | 21 | +0.1295 | SINGLE-ANCHOR | L262 | DISTRIBUTED | L153/G150/L262/L155 |  |  |
| #20 | L16 | H7 | 41 | +0.2613 | SINGLE-ANCHOR | L262 | DISTRIBUTED |  |  |  |
| #13 | L16 | H15 | 6 | +0.1758 | SINGLE-ANCHOR | G150 | SINGLE-ANCHOR | L153 |  | INTRA:ss1 |
| #14 | L16 | H18 | 19 | +0.1496 | SINGLE-ANCHOR | L118 | SINGLE-ANCHOR | L153 |  | ss1→flkL |
| #19 | L16 | H19 | 11 | +0.1233 | SINGLE-ANCHOR | L262 | DISTRIBUTED | L153/G150/L155/G157 |  | CROSS:ss1→ss2 |
| #15 | L17 | H10 | 17 | +0.1383 | SINGLE-ANCHOR | L153 | DISTRIBUTED | L155/Y154/L153/A156 |  | INTRA:ss1 |
| #21 | L20 | H13 | 10 | +0.0985 | SINGLE-ANCHOR | G150 | MULTI-ANCHOR |  | POSITIONAL | INTRA:ss1 |
| #28 | L22 | H14 | 14 | +0.0488 | MULTI-ANCHOR |  | DISTRIBUTED | Y154/L153/L155 |  | CROSS:ss1→ss2 |
| #25 | L23 | H15 | 7 | +0.0979 | SINGLE-ANCHOR | L262 | DUAL-ANCHOR | Y154/L155 |  | CROSS:ss1→ss2 |
| #23 | L26 | H16 | 18 | +0.0398 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #4 | L27 | H15 | 25 | +0.1412 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #5 | L29 | H18 | 38 | +0.1828 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #6 | L32 | H13 | 24 | +0.1021 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #3 | L32 | H18 | 23 | +0.1389 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
