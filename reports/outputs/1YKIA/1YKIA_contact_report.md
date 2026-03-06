# Contact Pattern Analysis: 1YKIA

Generated: 2026-03-03 05:19:37   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1YKIA |
| Contact pair | (83, 189) |
| ss1 | [78, 89) |
| ss2 | [184, 195) |
| Clean flank | 51 |
| Corrupt flank | 50 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.7543 |
| Corrupt metric | 0.1791 |
| Gap | 0.5751 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 400 | 98.16% |
| positive IE | 250 | 84.21% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L13 | H14 | +1.2240 |
| 2 | L0 | H11 | +1.2213 |
| 3 | L5 | H13 | +1.1920 |
| 4 | L6 | H0 | +1.1815 |
| 5 | L11 | H9 | +1.1761 |
| 6 | L11 | H17 | +1.1543 |
| 7 | L16 | H7 | +1.1282 |
| 8 | L14 | H1 | +1.1240 |
| 9 | L13 | H15 | +1.0919 |
| 10 | L12 | H16 | +1.0748 |
| 11 | L11 | H16 | +1.0080 |
| 12 | L11 | H11 | +0.9443 |
| 13 | L4 | H3 | +0.9324 |
| 14 | L9 | H4 | +0.8944 |
| 15 | L11 | H4 | +0.8876 |
| 16 | L3 | H14 | +0.8639 |
| 17 | L17 | H6 | +0.8244 |
| 18 | L12 | H9 | +0.8138 |
| 19 | L2 | H11 | +0.7465 |
| 20 | L0 | H1 | +0.7281 |
| 21 | L12 | H17 | +0.6618 |
| 22 | L9 | H14 | +0.5904 |
| 23 | L12 | H8 | +0.5854 |
| 24 | L32 | H18 | +0.5639 |
| 25 | L18 | H3 | +0.5602 |
| 26 | L13 | H18 | +0.5369 |
| 27 | L11 | H12 | +0.5330 |
| 28 | L2 | H9 | +0.5049 |
| 29 | L7 | H15 | +0.5032 |
| 30 | L13 | H9 | +0.4938 |

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
| 20 | 0.00% |
| 80 | 0.06% |
| 450 | 190.13% |

## Cell Attribution Analysis

Total cells: 11,339,840

- Positive: 5,709,749
- Negative: 5,628,348

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00001193 | 1,133,985 |
| 95th | +0.00003514 | 566,993 |
| 99th | +0.00026423 | 113,399 |
| 99.5th | +0.00056072 | 56,700 |
| 99.9th | +0.00280576 | 11,341 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H13 | 129 | other | 29 | flkL | +16.927946 | 0.099101 |
| L6 | H0 | 129 | other | 47 | flkL | +7.155049 | 0.041260 |
| L5 | H13 | 130 | other | 29 | flkL | +4.238221 | 0.095440 |
| L6 | H0 | 130 | other | 47 | flkL | +1.844948 | 0.043712 |
| L16 | H7 | 188 | ss2 | 129 | other | +1.610043 | 0.832947 |
| L14 | H1 | 188 | ss2 | 129 | other | +1.465410 | 0.306911 |
| L13 | H14 | 188 | ss2 | 129 | other | +1.446647 | 0.411793 |
| L17 | H6 | 188 | ss2 | 129 | other | +1.020823 | 0.698716 |
| L11 | H9 | 129 | other | 129 | other | +0.948736 | 0.329634 |
| L13 | H15 | 188 | ss2 | 129 | other | +0.946158 | 0.352544 |
| L5 | H13 | 129 | other | 32 | flkL | +0.939255 | 0.023789 |
| L16 | H4 | 188 | ss2 | 129 | other | +0.883495 | 0.237693 |
| L1 | H11 | 29 | flkL | 27 | flkL | +0.838854 | 0.121225 |
| L19 | H19 | 188 | ss2 | 129 | other | +0.718069 | 0.583238 |
| L4 | H3 | 129 | other | 31 | flkL | +0.688495 | 0.019000 |
| L4 | H3 | 129 | other | 28 | flkL | +0.682817 | 0.011449 |
| L18 | H3 | 188 | ss2 | 129 | other | +0.607568 | 0.527487 |
| L5 | H13 | 126 | other | 29 | flkL | +0.603317 | 0.103255 |
| L13 | H9 | 188 | ss2 | 191 | ss2 | +0.590563 | 0.308020 |
| L11 | H4 | 188 | ss2 | 129 | other | +0.573081 | 0.189500 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H0 | 138 | other | 47 | flkL | -0.413966 | 0.061576 |
| L3 | H1 | 25 | other | 27 | flkL | -0.439577 | 0.228556 |
| L5 | H13 | 122 | other | 29 | flkL | -0.440395 | 0.075854 |
| L5 | H13 | 129 | other | 55 | flkL | -0.460379 | 0.007426 |
| L11 | H9 | 128 | other | 128 | other | -0.467594 | 0.452319 |
| L6 | H0 | 132 | other | 47 | flkL | -0.480855 | 0.066528 |
| L16 | H4 | 188 | ss2 | 47 | flkL | -0.516068 | 0.143808 |
| L5 | H13 | 137 | other | 29 | flkL | -0.523890 | 0.101579 |
| L5 | H13 | 139 | other | 29 | flkL | -0.551479 | 0.102908 |
| L5 | H13 | 123 | other | 29 | flkL | -0.555516 | 0.079897 |
| L5 | H13 | 124 | other | 29 | flkL | -0.564420 | 0.086932 |
| L6 | H0 | 131 | other | 47 | flkL | -0.626662 | 0.054384 |
| L5 | H13 | 138 | other | 29 | flkL | -0.640573 | 0.103068 |
| L5 | H13 | 129 | other | 27 | flkL | -0.647169 | 0.009713 |
| L6 | H0 | 127 | other | 47 | flkL | -0.793405 | 0.045055 |
| L6 | H0 | 128 | other | 47 | flkL | -1.142721 | 0.042891 |
| L5 | H13 | 132 | other | 29 | flkL | -1.165026 | 0.096703 |
| L5 | H13 | 131 | other | 29 | flkL | -1.230560 | 0.094808 |
| L5 | H13 | 127 | other | 29 | flkL | -1.788857 | 0.106527 |
| L5 | H13 | 128 | other | 29 | flkL | -2.492525 | 0.104312 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.1791 | 0.00% |
| 10 | 10 | 8 | 0.1791 | 0.00% |
| 20 | 20 | 15 | 0.1791 | 0.00% |
| 50 | 50 | 31 | 0.1791 | 0.00% |
| 100 | 100 | 50 | 0.1791 | 0.00% |
| 200 | 200 | 90 | 0.1818 | 0.45% |
| 500 | 500 | 149 | 0.1761 | -0.52% |
| 1000 | 1,000 | 193 | 0.1952 | 2.80% |
| 2000 | 2,000 | 221 | 0.2368 | 10.02% |
| 5000 | 5,000 | 246 | 0.3042 | 21.74% |
| 10000 | 10,000 | 250 | 0.2702 | 15.83% |
| 20000 | 20,000 | 250 | 0.2838 | 18.20% |
| 50000 | 50,000 | 250 | 0.3763 | 34.28% |

## Motif Analysis

### L0 H1 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 4  |  total attr: +0.1858

**Key mass** (top-1=88%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 27 | flkL | +0.1631 | 87.8% |
| 50 | flkL | +0.0227 | 12.2% |

**Query mass** (top-1=43%, top-2=72%, top-3=88%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.0790 | 42.5% |
| 130 | other | +0.0549 | 29.6% |
| 61 | flkL | +0.0291 | 15.7% |
| 27 | flkL | +0.0227 | 12.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 1 | 25.0% |
| +103 | 1 | 25.0% |
| +34 | 1 | 25.0% |
| -23 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 2 | 50.0% |
| flkL | flkL | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 27 | flkL | +0.0790 | 0.0007 |
| 130 | other | 27 | flkL | +0.0549 | 0.0007 |
| 61 | flkL | 27 | flkL | +0.0291 | 0.0129 |
| 27 | flkL | 50 | flkL | +0.0227 | 0.0093 |

### L0 H11 — Rank #2

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 36  |  total attr: +2.2569

**Key mass** (top-1=17%, top-2=22%, top-3=27%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 27 | flkL | +0.3754 | 16.6% |
| 37 | flkL | +0.1283 | 5.7% |
| 44 | flkL | +0.0985 | 4.4% |
| 41 | flkL | +0.0888 | 3.9% |
| 50 | flkL | +0.0850 | 3.8% |

**Query mass** (top-1=88%, top-2=91%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 27 | flkL | +1.9872 | 88.1% |
| 71 | flkL | +0.0672 | 3.0% |
| 76 | flkL | +0.0473 | 2.1% |
| 29 | flkL | +0.0456 | 2.0% |
| 33 | flkL | +0.0288 | 1.3% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -10 | 1 | 2.8% |
| +0 | 1 | 2.8% |
| -17 | 1 | 2.8% |
| -14 | 1 | 2.8% |
| -23 | 1 | 2.8% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 21 | 58.3% |
| flkL | flkR | 7 | 19.4% |
| flkL | ss1 | 3 | 8.3% |
| flkL | ss2 | 3 | 8.3% |
| other | flkL | 2 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 27 | flkL | 37 | flkL | +0.1283 | 0.0410 |
| 27 | flkL | 27 | flkL | +0.1057 | 0.0278 |
| 27 | flkL | 44 | flkL | +0.0985 | 0.0315 |
| 27 | flkL | 41 | flkL | +0.0888 | 0.0235 |
| 27 | flkL | 50 | flkL | +0.0850 | 0.0217 |

### L2 H9 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 4  |  total attr: +0.6450

**Key mass** (top-1=67%, top-2=92%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 30 | flkL | +0.4332 | 67.2% |
| 28 | flkL | +0.1596 | 24.7% |
| 24 | other | +0.0262 | 4.1% |
| 22 | other | +0.0261 | 4.0% |

**Query mass** (top-1=92%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +0.5928 | 91.9% |
| 25 | other | +0.0523 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 50.0% |
| -1 | 1 | 25.0% |
| +3 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 2 | 50.0% |
| other | other | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 29 | flkL | 30 | flkL | +0.4332 | 0.1304 |
| 29 | flkL | 28 | flkL | +0.1596 | 0.0182 |
| 25 | other | 24 | other | +0.0262 | 0.0167 |
| 25 | other | 22 | other | +0.0261 | 0.0146 |

### L2 H11 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 10  |  total attr: +0.8634

**Key mass** (top-1=66%, top-2=90%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +0.5684 | 65.8% |
| 27 | flkL | +0.2075 | 24.0% |
| 23 | other | +0.0577 | 6.7% |
| 25 | other | +0.0297 | 3.4% |

**Query mass** (top-1=62%, top-2=81%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +0.5326 | 61.7% |
| 28 | flkL | +0.1688 | 19.6% |
| 25 | other | +0.1146 | 13.3% |
| 30 | flkL | +0.0473 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 20.0% |
| +1 | 2 | 20.0% |
| +2 | 1 | 10.0% |
| -1 | 1 | 10.0% |
| -2 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 50.0% |
| other | flkL | 2 | 20.0% |
| flkL | other | 2 | 20.0% |
| other | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 29 | flkL | 29 | flkL | +0.3925 | 0.0381 |
| 29 | flkL | 27 | flkL | +0.1062 | 0.0136 |
| 28 | flkL | 29 | flkL | +0.0897 | 0.0413 |
| 28 | flkL | 27 | flkL | +0.0552 | 0.0196 |
| 30 | flkL | 29 | flkL | +0.0473 | 0.0732 |

### L3 H14 — Rank #16

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 8  |  total attr: +1.0704

**Key mass** (top-1=53%, top-2=68%, top-3=78%)  [DISTR(Q25/E24/L21)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | other | +0.5712 | 53.4% |
| 24 | other | +0.1520 | 14.2% |
| 21 | other | +0.1094 | 10.2% |
| 27 | flkL | +0.0993 | 9.3% |
| 28 | flkL | +0.0773 | 7.2% |

**Query mass** (top-1=95%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +1.0142 | 94.7% |
| 31 | flkL | +0.0290 | 2.7% |
| 32 | flkL | +0.0273 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 2 | 25.0% |
| +4 | 1 | 12.5% |
| +5 | 1 | 12.5% |
| +2 | 1 | 12.5% |
| +1 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 6 | 75.0% |
| flkL | flkL | 2 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 29 | flkL | 25 | other | +0.5422 | 0.0426 |
| 29 | flkL | 24 | other | +0.1248 | 0.0443 |
| 29 | flkL | 21 | other | +0.1094 | 0.0176 |
| 29 | flkL | 27 | flkL | +0.0993 | 0.0110 |
| 29 | flkL | 28 | flkL | +0.0773 | 0.0107 |

### L4 H3 — Rank #13

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 38  |  total attr: +3.8070

**Key mass** (top-1=25%, top-2=48%, top-3=56%)  [DISTR(T31/Q28/I29/E24/F47)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 31 | flkL | +0.9441 | 24.8% |
| 28 | flkL | +0.8657 | 22.7% |
| 29 | flkL | +0.3226 | 8.5% |
| 24 | other | +0.3180 | 8.4% |
| 47 | flkL | +0.2276 | 6.0% |

**Query mass** (top-1=80%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +3.0277 | 79.5% |
| 130 | other | +0.5856 | 15.4% |
| 128 | other | +0.0642 | 1.7% |
| 126 | other | +0.0542 | 1.4% |
| 127 | other | +0.0465 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +98 | 3 | 7.9% |
| +101 | 3 | 7.9% |
| +100 | 2 | 5.3% |
| +105 | 1 | 2.6% |
| +99 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 17 | 44.7% |
| other | other | 17 | 44.7% |
| other | ss1 | 3 | 7.9% |
| other | flkR | 1 | 2.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 31 | flkL | +0.6885 | 0.0190 |
| 129 | other | 28 | flkL | +0.6828 | 0.0114 |
| 129 | other | 24 | other | +0.2640 | 0.0060 |
| 129 | other | 29 | flkL | +0.2637 | 0.0069 |
| 130 | other | 31 | flkL | +0.1972 | 0.0219 |

### L5 H13 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 47  |  total attr: +26.4751

**Key mass** (top-1=84%, top-2=88%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +22.1134 | 83.5% |
| 32 | flkL | +1.2422 | 4.7% |
| 59 | flkL | +0.5252 | 2.0% |
| 28 | flkL | +0.4063 | 1.5% |
| 33 | flkL | +0.3441 | 1.3% |

**Query mass** (top-1=76%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +20.1343 | 76.1% |
| 130 | other | +4.8916 | 18.5% |
| 126 | other | +0.6395 | 2.4% |
| 125 | other | +0.3112 | 1.2% |
| 128 | other | +0.1984 | 0.7% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 3 | 6.4% |
| +97 | 3 | 6.4% |
| +104 | 3 | 6.4% |
| +100 | 2 | 4.3% |
| +96 | 2 | 4.3% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 28 | 59.6% |
| other | other | 9 | 19.1% |
| other | flkR | 7 | 14.9% |
| other | ss2 | 2 | 4.3% |
| ss2 | flkL | 1 | 2.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 29 | flkL | +16.9279 | 0.0991 |
| 130 | other | 29 | flkL | +4.2382 | 0.0954 |
| 129 | other | 32 | flkL | +0.9393 | 0.0238 |
| 126 | other | 29 | flkL | +0.6033 | 0.1033 |
| 129 | other | 59 | flkL | +0.4187 | 0.0069 |

### L6 H0 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 22  |  total attr: +10.5196

**Key mass** (top-1=91%, top-2=97%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +9.5827 | 91.1% |
| 48 | flkL | +0.6009 | 5.7% |
| 46 | flkL | +0.0740 | 0.7% |
| 27 | flkL | +0.0578 | 0.5% |
| 197 | flkR | +0.0483 | 0.5% |

**Query mass** (top-1=75%, top-2=94%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +7.9049 | 75.1% |
| 130 | other | +1.9509 | 18.5% |
| 126 | other | +0.2686 | 2.6% |
| 125 | other | +0.0941 | 0.9% |
| 0 | other | +0.0578 | 0.5% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +82 | 2 | 9.1% |
| +83 | 2 | 9.1% |
| +78 | 2 | 9.1% |
| +81 | 1 | 4.5% |
| +79 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=77%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 17 | 77.3% |
| other | flkR | 3 | 13.6% |
| other | ss1 | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 47 | flkL | +7.1550 | 0.0413 |
| 130 | other | 47 | flkL | +1.8449 | 0.0437 |
| 129 | other | 48 | flkL | +0.4717 | 0.0053 |
| 126 | other | 47 | flkL | +0.2454 | 0.0421 |
| 130 | other | 48 | flkL | +0.1059 | 0.0050 |

### L7 H15 — Rank #29

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 9  |  total attr: +0.3663

**Key mass** (top-1=30%, top-2=45%, top-3=57%)  [DISTR(D76/G181/K180/V92/Q43)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 76 | flkL | +0.1096 | 29.9% |
| 181 | other | +0.0550 | 15.0% |
| 180 | other | +0.0427 | 11.7% |
| 92 | other | +0.0364 | 9.9% |
| 43 | flkL | +0.0350 | 9.6% |

**Query mass** (top-1=92%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.3380 | 92.3% |
| 130 | other | +0.0282 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +53 | 1 | 11.1% |
| -52 | 1 | 11.1% |
| -51 | 1 | 11.1% |
| +37 | 1 | 11.1% |
| +86 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 5 | 55.6% |
| other | other | 4 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 76 | flkL | +0.0814 | 0.0026 |
| 129 | other | 181 | other | +0.0550 | 0.0024 |
| 129 | other | 180 | other | +0.0427 | 0.0034 |
| 129 | other | 92 | other | +0.0364 | 0.0018 |
| 129 | other | 43 | flkL | +0.0350 | 0.0012 |

### L9 H4 — Rank #14

**Tags:** k:MULTI-ANCHOR / q:SINGLE-ANCHOR  |  cells: 10  |  total attr: +0.7939

**Key mass** (top-1=38%, top-2=63%, top-3=80%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 128 | other | +0.3056 | 38.5% |
| 127 | other | +0.1942 | 24.5% |
| 129 | other | +0.1384 | 17.4% |
| 125 | other | +0.0440 | 5.5% |
| 124 | other | +0.0329 | 4.1% |

**Query mass** (top-1=75%, top-2=87%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.5938 | 74.8% |
| 130 | other | +0.0957 | 12.1% |
| 126 | other | +0.0769 | 9.7% |
| 133 | other | +0.0275 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 70%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 4 | 40.0% |
| +1 | 3 | 30.0% |
| +0 | 1 | 10.0% |
| +3 | 1 | 10.0% |
| -75 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=90%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 9 | 90.0% |
| other | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 128 | other | +0.2644 | 0.1286 |
| 129 | other | 127 | other | +0.1942 | 0.1065 |
| 129 | other | 129 | other | +0.0839 | 0.0384 |
| 130 | other | 129 | other | +0.0545 | 0.1206 |
| 126 | other | 125 | other | +0.0440 | 0.1043 |

### L9 H14 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.3754

**Key mass** (top-1=92%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | flkR | +0.3450 | 91.9% |
| 82 | ss1 | +0.0304 | 8.1% |

**Query mass** (top-1=61%, top-2=79%, top-3=92%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.2279 | 60.7% |
| 126 | other | +0.0699 | 18.6% |
| 130 | other | +0.0471 | 12.6% |
| 188 | ss2 | +0.0304 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -88 | 1 | 25.0% |
| -91 | 1 | 25.0% |
| -87 | 1 | 25.0% |
| +106 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 3 | 75.0% |
| ss2 | ss1 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 217 | flkR | +0.2279 | 0.2936 |
| 126 | other | 217 | flkR | +0.0699 | 0.3141 |
| 130 | other | 217 | flkR | +0.0471 | 0.2779 |
| 188 | ss2 | 82 | ss1 | +0.0304 | 0.0366 |

### L11 H4 — Rank #15

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 13  |  total attr: +1.8618

**Key mass** (top-1=42%, top-2=71%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.7742 | 41.6% |
| 130 | other | +0.5411 | 29.1% |
| 128 | other | +0.4565 | 24.5% |
| 127 | other | +0.0485 | 2.6% |
| 131 | other | +0.0415 | 2.2% |

**Query mass** (top-1=76%, top-2=88%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +1.4220 | 76.4% |
| 195 | flkR | +0.2096 | 11.3% |
| 186 | ss2 | +0.1599 | 8.6% |
| 193 | ss2 | +0.0704 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +58 | 2 | 15.4% |
| +57 | 2 | 15.4% |
| +59 | 1 | 7.7% |
| +60 | 1 | 7.7% |
| +66 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=77%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 10 | 76.9% |
| flkR | other | 3 | 23.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +0.5731 | 0.1895 |
| 188 | ss2 | 128 | other | +0.3836 | 0.1326 |
| 188 | ss2 | 130 | other | +0.3753 | 0.1270 |
| 195 | flkR | 129 | other | +0.0936 | 0.2820 |
| 186 | ss2 | 129 | other | +0.0706 | 0.2689 |

### L11 H9 — Rank #5

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 13  |  total attr: +1.8330

**Key mass** (top-1=53%, top-2=72%, top-3=81%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.9718 | 53.0% |
| 130 | other | +0.3570 | 19.5% |
| 128 | other | +0.1537 | 8.4% |
| 173 | other | +0.0812 | 4.4% |
| 188 | ss2 | +0.0622 | 3.4% |

**Query mass** (top-1=84%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +1.5486 | 84.5% |
| 130 | other | +0.2223 | 12.1% |
| 188 | ss2 | +0.0622 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 23.1% |
| -1 | 2 | 15.4% |
| +1 | 2 | 15.4% |
| -44 | 1 | 7.7% |
| +31 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=92%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 12 | 92.3% |
| ss2 | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 129 | other | +0.9487 | 0.3296 |
| 129 | other | 130 | other | +0.1925 | 0.0663 |
| 130 | other | 130 | other | +0.1645 | 0.3198 |
| 129 | other | 128 | other | +0.1537 | 0.0549 |
| 129 | other | 173 | other | +0.0812 | 0.0509 |

### L11 H11 — Rank #12

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 5  |  total attr: +0.1405

**Key mass** (top-1=30%, top-2=50%, top-3=67%)  [DISTR(S42/F123/A124/D130)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.0425 | 30.2% |
| 123 | other | +0.0273 | 19.4% |
| 124 | other | +0.0247 | 17.6% |
| 130 | other | +0.0231 | 16.4% |
| 122 | other | +0.0230 | 16.4% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.1405 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +87 | 1 | 20.0% |
| +6 | 1 | 20.0% |
| +5 | 1 | 20.0% |
| -1 | 1 | 20.0% |
| +7 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 4 | 80.0% |
| other | flkL | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 42 | flkL | +0.0425 | 0.0454 |
| 129 | other | 123 | other | +0.0273 | 0.0156 |
| 129 | other | 124 | other | +0.0247 | 0.0138 |
| 129 | other | 130 | other | +0.0231 | 0.0106 |
| 129 | other | 122 | other | +0.0230 | 0.0133 |

### L11 H12 — Rank #27

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L11 H16 — Rank #11

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 25  |  total attr: +1.3694

**Key mass** (top-1=47%, top-2=83%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.6372 | 46.5% |
| 130 | other | +0.4993 | 36.5% |
| 128 | other | +0.2330 | 17.0% |

**Query mass** (top-1=17%, top-2=34%, top-3=51%)  [DISTR(S184/V187/V186/L185/P189)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 184 | ss2 | +0.2361 | 17.2% |
| 187 | ss2 | +0.2355 | 17.2% |
| 186 | ss2 | +0.2313 | 16.9% |
| 185 | ss2 | +0.2180 | 15.9% |
| 189 | ss2 | +0.1414 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 3 | 12.0% |
| +56 | 3 | 12.0% |
| +58 | 2 | 8.0% |
| +55 | 2 | 8.0% |
| +54 | 2 | 8.0% |

**Region-pair profile** (q→k)  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 16 | 64.0% |
| flkR | other | 5 | 20.0% |
| other | other | 4 | 16.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 187 | ss2 | 129 | other | +0.0984 | 0.3186 |
| 184 | ss2 | 129 | other | +0.0978 | 0.3207 |
| 184 | ss2 | 130 | other | +0.0920 | 0.3056 |
| 186 | ss2 | 129 | other | +0.0881 | 0.3211 |
| 186 | ss2 | 130 | other | +0.0871 | 0.2924 |

### L11 H17 — Rank #6

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.8209

**Key mass** (top-1=49%, top-2=67%, top-3=75%)  [DISTR(I29/L32/K129)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +0.4036 | 49.2% |
| 32 | flkL | +0.1460 | 17.8% |
| 129 | other | +0.0695 | 8.5% |
| 28 | flkL | +0.0671 | 8.2% |
| 33 | flkL | +0.0513 | 6.3% |

**Query mass** (top-1=75%, top-2=85%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.6196 | 75.5% |
| 130 | other | +0.0822 | 10.0% |
| 191 | ss2 | +0.0647 | 7.9% |
| 188 | ss2 | +0.0544 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +101 | 2 | 18.2% |
| +100 | 1 | 9.1% |
| +97 | 1 | 9.1% |
| +96 | 1 | 9.1% |
| +62 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 7 | 63.6% |
| ss2 | other | 4 | 36.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 29 | flkL | +0.3447 | 0.0995 |
| 129 | other | 32 | flkL | +0.1227 | 0.0591 |
| 129 | other | 28 | flkL | +0.0671 | 0.0461 |
| 130 | other | 29 | flkL | +0.0588 | 0.0837 |
| 129 | other | 33 | flkL | +0.0513 | 0.0363 |

### L12 H8 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 1  |  total attr: +0.0238

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | flkR | +0.0238 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.0238 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -88 | 1 | 100.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 217 | flkR | +0.0238 | 0.0470 |

### L12 H9 — Rank #18

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.1366

**Key mass** (top-1=45%, top-2=81%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | other | +0.0610 | 44.7% |
| 128 | other | +0.0501 | 36.7% |
| 129 | other | +0.0255 | 18.7% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.1366 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 1 | 33.3% |
| +1 | 1 | 33.3% |
| +0 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 127 | other | +0.0610 | 0.1166 |
| 129 | other | 128 | other | +0.0501 | 0.0779 |
| 129 | other | 129 | other | +0.0255 | 0.0355 |

### L12 H16 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.3271

**Key mass** (top-1=91%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.2964 | 90.6% |
| 29 | flkL | +0.0307 | 9.4% |

**Query mass** (top-1=79%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.2588 | 79.1% |
| 130 | other | +0.0683 | 20.9% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +130 | 1 | 33.3% |
| +131 | 1 | 33.3% |
| +100 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 2 | 66.7% |
| other | flkL | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | -1 | other | +0.2281 | 0.1526 |
| 130 | other | -1 | other | +0.0683 | 0.1397 |
| 129 | other | 29 | flkL | +0.0307 | 0.0165 |

### L12 H17 — Rank #21

**Tags:** k:MULTI-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.0869

**Key mass** (top-1=36%, top-2=68%, top-3=100%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | other | +0.0310 | 35.6% |
| 125 | other | +0.0284 | 32.6% |
| 123 | other | +0.0276 | 31.7% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.0869 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 1 | 33.3% |
| +4 | 1 | 33.3% |
| +6 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | other | 124 | other | +0.0310 | 0.0193 |
| 129 | other | 125 | other | +0.0284 | 0.0187 |
| 129 | other | 123 | other | +0.0276 | 0.0166 |

### L13 H9 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 3  |  total attr: +0.6903

**Key mass** (top-1=86%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 191 | ss2 | +0.5906 | 85.6% |
| 189 | ss2 | +0.0768 | 11.1% |
| 126 | other | +0.0229 | 3.3% |

**Query mass** (top-1=86%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +0.5906 | 85.6% |
| 186 | ss2 | +0.0768 | 11.1% |
| 129 | other | +0.0229 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 66.7% |
| +3 | 1 | 33.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 2 | 66.7% |
| other | other | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 191 | ss2 | +0.5906 | 0.3080 |
| 186 | ss2 | 189 | ss2 | +0.0768 | 0.2478 |
| 129 | other | 126 | other | +0.0229 | 0.1869 |

### L13 H14 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +2.4520

**Key mass** (top-1=64%, top-2=81%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +1.5771 | 64.3% |
| 130 | other | +0.4208 | 17.2% |
| 128 | other | +0.1851 | 7.5% |
| 82 | ss1 | +0.1372 | 5.6% |
| 69 | flkL | +0.0739 | 3.0% |

**Query mass** (top-1=91%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +2.2401 | 91.4% |
| 190 | ss2 | +0.0921 | 3.8% |
| 191 | ss2 | +0.0392 | 1.6% |
| 129 | other | +0.0310 | 1.3% |
| 47 | flkL | +0.0268 | 1.1% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +60 | 2 | 18.2% |
| +48 | 2 | 18.2% |
| +59 | 1 | 9.1% |
| +58 | 1 | 9.1% |
| +106 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 7 | 63.6% |
| ss2 | ss1 | 1 | 9.1% |
| ss2 | flkL | 1 | 9.1% |
| other | ss1 | 1 | 9.1% |
| flkL | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +1.4466 | 0.4118 |
| 188 | ss2 | 130 | other | +0.3972 | 0.1137 |
| 188 | ss2 | 128 | other | +0.1851 | 0.0718 |
| 188 | ss2 | 82 | ss1 | +0.1372 | 0.0877 |
| 188 | ss2 | 69 | flkL | +0.0739 | 0.0817 |

### L13 H15 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 7  |  total attr: +1.6356

**Key mass** (top-1=61%, top-2=84%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +1.0053 | 61.5% |
| 130 | other | +0.3719 | 22.7% |
| 128 | other | +0.1539 | 9.4% |
| 217 | flkR | +0.0632 | 3.9% |
| 213 | flkR | +0.0414 | 2.5% |

**Query mass** (top-1=96%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +1.5765 | 96.4% |
| 183 | other | +0.0323 | 2.0% |
| 193 | ss2 | +0.0269 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +59 | 1 | 14.3% |
| +58 | 1 | 14.3% |
| +60 | 1 | 14.3% |
| -29 | 1 | 14.3% |
| -25 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 4 | 57.1% |
| ss2 | flkR | 2 | 28.6% |
| other | other | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +0.9462 | 0.3525 |
| 188 | ss2 | 130 | other | +0.3719 | 0.1546 |
| 188 | ss2 | 128 | other | +0.1539 | 0.0784 |
| 188 | ss2 | 217 | flkR | +0.0632 | 0.0969 |
| 188 | ss2 | 213 | flkR | +0.0414 | 0.0319 |

### L13 H18 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 6  |  total attr: +0.3130

**Key mass** (top-1=77%, top-2=89%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.2421 | 77.3% |
| 130 | other | +0.0378 | 12.1% |
| 128 | other | +0.0331 | 10.6% |

**Query mass** (top-1=57%, top-2=78%, top-3=91%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +0.1772 | 56.6% |
| 81 | ss1 | +0.0677 | 21.6% |
| 83 | ss1 | +0.0391 | 12.5% |
| 52 | flkL | +0.0291 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +59 | 1 | 16.7% |
| -48 | 1 | 16.7% |
| -46 | 1 | 16.7% |
| +58 | 1 | 16.7% |
| +60 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 3 | 50.0% |
| ss1 | other | 2 | 33.3% |
| flkL | other | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +0.1063 | 0.0896 |
| 81 | ss1 | 129 | other | +0.0677 | 0.4798 |
| 83 | ss1 | 129 | other | +0.0391 | 0.5449 |
| 188 | ss2 | 130 | other | +0.0378 | 0.0370 |
| 188 | ss2 | 128 | other | +0.0331 | 0.0258 |

### L14 H1 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 8  |  total attr: +2.3453

**Key mass** (top-1=70%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +1.6512 | 70.4% |
| 130 | other | +0.5187 | 22.1% |
| 128 | other | +0.1755 | 7.5% |

**Query mass** (top-1=91%, top-2=97%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +2.1355 | 91.1% |
| 211 | flkR | +0.1288 | 5.5% |
| 213 | flkR | +0.0342 | 1.5% |
| 208 | flkR | +0.0242 | 1.0% |
| 210 | flkR | +0.0226 | 1.0% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +81 | 2 | 25.0% |
| +59 | 1 | 12.5% |
| +58 | 1 | 12.5% |
| +60 | 1 | 12.5% |
| +82 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 5 | 62.5% |
| ss2 | other | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +1.4654 | 0.3069 |
| 188 | ss2 | 130 | other | +0.4947 | 0.1189 |
| 188 | ss2 | 128 | other | +0.1755 | 0.0451 |
| 211 | flkR | 129 | other | +0.1047 | 0.6175 |
| 213 | flkR | 129 | other | +0.0342 | 0.5941 |

### L16 H7 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 13  |  total attr: +2.5301

**Key mass** (top-1=77%, top-2=87%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +1.9538 | 77.2% |
| 185 | ss2 | +0.2498 | 9.9% |
| 130 | other | +0.2433 | 9.6% |
| 47 | flkL | +0.0832 | 3.3% |

**Query mass** (top-1=72%, top-2=82%, top-3=90%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +1.8152 | 71.7% |
| 47 | flkL | +0.2698 | 10.7% |
| 185 | ss2 | +0.1984 | 7.8% |
| 189 | ss2 | +0.1084 | 4.3% |
| 194 | ss2 | +0.0648 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +59 | 1 | 7.7% |
| +58 | 1 | 7.7% |
| -82 | 1 | 7.7% |
| +4 | 1 | 7.7% |
| +138 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 4 | 30.8% |
| flkL | other | 3 | 23.1% |
| ss2 | ss2 | 3 | 23.1% |
| ss2 | flkL | 1 | 7.7% |
| flkL | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +1.6100 | 0.8329 |
| 188 | ss2 | 130 | other | +0.2052 | 0.1510 |
| 47 | flkL | 129 | other | +0.1740 | 0.8115 |
| 189 | ss2 | 185 | ss2 | +0.1084 | 0.3784 |
| 185 | ss2 | 47 | flkL | +0.0832 | 0.2963 |

### L17 H6 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +1.5010

**Key mass** (top-1=73%, top-2=91%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +1.0993 | 73.2% |
| 130 | other | +0.2634 | 17.5% |
| 217 | flkR | +0.0850 | 5.7% |
| 128 | other | +0.0534 | 3.6% |

**Query mass** (top-1=95%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +1.4226 | 94.8% |
| 184 | ss2 | +0.0413 | 2.8% |
| 191 | ss2 | +0.0371 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +59 | 1 | 16.7% |
| +58 | 1 | 16.7% |
| -29 | 1 | 16.7% |
| +60 | 1 | 16.7% |
| +55 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 5 | 83.3% |
| ss2 | flkR | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +1.0208 | 0.6987 |
| 188 | ss2 | 130 | other | +0.2634 | 0.1951 |
| 188 | ss2 | 217 | flkR | +0.0850 | 0.5916 |
| 188 | ss2 | 128 | other | +0.0534 | 0.0520 |
| 184 | ss2 | 129 | other | +0.0413 | 0.6891 |

### L18 H3 — Rank #25

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 7  |  total attr: +1.2989

**Key mass** (top-1=58%, top-2=92%, top-3=98%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | other | +0.7590 | 58.4% |
| 130 | other | +0.4367 | 33.6% |
| 194 | ss2 | +0.0738 | 5.7% |
| 128 | other | +0.0294 | 2.3% |

**Query mass** (top-1=81%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +1.0498 | 80.8% |
| 186 | ss2 | +0.2206 | 17.0% |
| 190 | ss2 | +0.0285 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +59 | 1 | 14.3% |
| +58 | 1 | 14.3% |
| +57 | 1 | 14.3% |
| +56 | 1 | 14.3% |
| -6 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 6 | 85.7% |
| ss2 | ss2 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 129 | other | +0.6076 | 0.5275 |
| 188 | ss2 | 130 | other | +0.3391 | 0.3218 |
| 186 | ss2 | 129 | other | +0.1230 | 0.4937 |
| 186 | ss2 | 130 | other | +0.0976 | 0.3886 |
| 188 | ss2 | 194 | ss2 | +0.0738 | 0.1187 |

### L32 H18 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 2  |  total attr: +0.0611

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 83 | ss1 | +0.0611 | 100.0% |

**Query mass** (top-1=58%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 188 | ss2 | +0.0353 | 57.8% |
| 186 | ss2 | +0.0258 | 42.2% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +105 | 1 | 50.0% |
| +103 | 1 | 50.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 188 | ss2 | 83 | ss1 | +0.0353 | 0.0873 |
| 186 | ss2 | 83 | ss1 | +0.0258 | 0.0878 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #20 | L0 | H1 | 4 | +0.1858 | SINGLE-ANCHOR | E27 | DUAL-ANCHOR | K129/D130 |  |  |
| #2 | L0 | H11 | 36 | +2.2569 | DISTRIBUTED |  | SINGLE-ANCHOR | E27 |  | INTRA:flkL |
| #28 | L2 | H9 | 4 | +0.6450 | SINGLE-ANCHOR | K30 | SINGLE-ANCHOR | I29 |  | INTRA:flkL |
| #19 | L2 | H11 | 10 | +0.8634 | SINGLE-ANCHOR | I29 | SINGLE-ANCHOR | I29 |  | INTRA:flkL |
| #16 | L3 | H14 | 8 | +1.0704 | DISTRIBUTED | Q25/E24/L21 | SINGLE-ANCHOR | I29 |  |  |
| #13 | L4 | H3 | 38 | +3.8070 | DISTRIBUTED | T31/Q28/I29/E24/F47 | SINGLE-ANCHOR | K129 |  |  |
| #3 | L5 | H13 | 47 | +26.4751 | SINGLE-ANCHOR | I29 | SINGLE-ANCHOR | K129 |  |  |
| #4 | L6 | H0 | 22 | +10.5196 | SINGLE-ANCHOR | F47 | SINGLE-ANCHOR | K129 |  |  |
| #29 | L7 | H15 | 9 | +0.3663 | DISTRIBUTED | D76/G181/K180/V92/Q43 | SINGLE-ANCHOR | K129 |  |  |
| #14 | L9 | H4 | 10 | +0.7939 | MULTI-ANCHOR |  | SINGLE-ANCHOR | K129 |  |  |
| #22 | L9 | H14 | 4 | +0.3754 | SINGLE-ANCHOR | ?217 | SINGLE-ANCHOR | K129 |  |  |
| #15 | L11 | H4 | 13 | +1.8618 | DUAL-ANCHOR | K129/D130 | SINGLE-ANCHOR | V188 |  |  |
| #5 | L11 | H9 | 13 | +1.8330 | DUAL-ANCHOR | K129/D130 | SINGLE-ANCHOR | K129 |  |  |
| #12 | L11 | H11 | 5 | +0.1405 | DISTRIBUTED | S42/F123/A124/D130 | SINGLE-ANCHOR | K129 |  |  |
| #27 | L11 | H12 | 0 | +0.0000 | — |  | — |  |  |  |
| #11 | L11 | H16 | 25 | +1.3694 | DUAL-ANCHOR | K129/D130 | DISTRIBUTED | S184/V187/V186/L185/P189 |  |  |
| #6 | L11 | H17 | 11 | +0.8209 | DISTRIBUTED | I29/L32/K129 | SINGLE-ANCHOR | K129 |  |  |
| #23 | L12 | H8 | 1 | +0.0238 | SINGLE-ANCHOR | ?217 | SINGLE-ANCHOR | K129 |  |  |
| #18 | L12 | H9 | 3 | +0.1366 | DUAL-ANCHOR | H127/R128 | SINGLE-ANCHOR | K129 |  |  |
| #10 | L12 | H16 | 3 | +0.3271 | SINGLE-ANCHOR | ?-1 | SINGLE-ANCHOR | K129 |  |  |
| #21 | L12 | H17 | 3 | +0.0869 | MULTI-ANCHOR |  | SINGLE-ANCHOR | K129 |  |  |
| #30 | L13 | H9 | 3 | +0.6903 | SINGLE-ANCHOR | G191 | SINGLE-ANCHOR | V188 |  | INTRA:ss2 |
| #1 | L13 | H14 | 11 | +2.4520 | SINGLE-ANCHOR | K129 | SINGLE-ANCHOR | V188 |  |  |
| #9 | L13 | H15 | 7 | +1.6356 | SINGLE-ANCHOR | K129 | SINGLE-ANCHOR | V188 |  |  |
| #26 | L13 | H18 | 6 | +0.3130 | SINGLE-ANCHOR | K129 | DUAL-ANCHOR | V188/V81 |  |  |
| #8 | L14 | H1 | 8 | +2.3453 | SINGLE-ANCHOR | K129 | SINGLE-ANCHOR | V188 |  |  |
| #7 | L16 | H7 | 13 | +2.5301 | SINGLE-ANCHOR | K129 | SINGLE-ANCHOR | V188 |  |  |
| #17 | L17 | H6 | 6 | +1.5010 | SINGLE-ANCHOR | K129 | SINGLE-ANCHOR | V188 |  |  |
| #25 | L18 | H3 | 7 | +1.2989 | DUAL-ANCHOR | K129/D130 | SINGLE-ANCHOR | V188 |  |  |
| #24 | L32 | H18 | 2 | +0.0611 | SINGLE-ANCHOR | F83 | DUAL-ANCHOR | V188/V186 | CROSS_SSE | CROSS:ss2→ss1 |
