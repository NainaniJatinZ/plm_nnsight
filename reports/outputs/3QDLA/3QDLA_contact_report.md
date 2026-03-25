# Contact Pattern Analysis: 3QDLA

Generated: 2026-03-22 21:43:32   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3QDLA |
| Contact pair | (84, 186) |
| ss1 | [79, 90) |
| ss2 | [181, 192) |
| Clean flank | 40 |
| Corrupt flank | 39 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.7185 |
| Corrupt metric | 0.1492 |
| Gap | 0.5693 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 74.60% |
| positive IE | 23 | 74.02% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L0 | H14 | +0.5998 |
| 2 | L11 | H16 | +0.5436 |
| 3 | L32 | H18 | +0.4714 |
| 4 | L5 | H13 | +0.4182 |
| 5 | L11 | H4 | +0.2372 |
| 6 | L29 | H18 | +0.1742 |
| 7 | L32 | H13 | +0.1717 |
| 8 | L27 | H15 | +0.1622 |
| 9 | L10 | H12 | +0.1608 |
| 10 | L13 | H14 | +0.1354 |
| 11 | L13 | H15 | +0.1318 |
| 12 | L16 | H10 | +0.1181 |
| 13 | L11 | H5 | +0.1019 |
| 14 | L23 | H15 | +0.0977 |
| 15 | L17 | H9 | +0.0962 |
| 16 | L10 | H9 | +0.0881 |
| 17 | L23 | H8 | +0.0789 |
| 18 | L13 | H18 | +0.0711 |
| 19 | L27 | H10 | +0.0711 |
| 20 | L16 | H7 | +0.0702 |
| 21 | L10 | H14 | +0.0692 |
| 22 | L17 | H12 | +0.0660 |
| 23 | L11 | H14 | +0.0566 |
| 24 | L14 | H13 | +0.0556 |
| 25 | L23 | H18 | +0.0516 |
| 26 | L10 | H16 | +0.0510 |
| 27 | L12 | H19 | +0.0508 |
| 28 | L11 | H18 | +0.0498 |
| 29 | L25 | H13 | +0.0444 |
| 30 | L17 | H3 | +0.0436 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 3.18% |
| 4 | 3.28% |
| 5 | 4.57% |
| 6 | 8.47% |
| 7 | 12.66% |
| 8 | 18.34% |
| 9 | 26.09% |
| 10 | 27.93% |
| 20 | 61.01% |
| 80 | 142.17% |
| 450 | 168.91% |

## Cell Attribution Analysis

Total cells: 1,010,834

- Positive: 519,576
- Negative: 489,573

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000337 | 101,084 |
| 95th | +0.00000952 | 50,542 |
| 99th | +0.00008058 | 10,109 |
| 99.5th | +0.00018592 | 5,055 |
| 99.9th | +0.00106166 | 1,011 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H13 | 114 | other | 35 | other | +0.810360 | 0.119435 |
| L0 | H14 | 39 | flkL | 39 | flkL | +0.185600 | 0.982710 |
| L5 | H13 | 114 | other | 36 | other | +0.065213 | 0.017231 |
| L16 | H7 | 185 | ss2 | 115 | other | +0.061916 | 0.099885 |
| L5 | H13 | 110 | other | 35 | other | +0.059096 | 0.096826 |
| L32 | H18 | 184 | ss2 | 82 | ss1 | +0.054661 | 0.197545 |
| L32 | H13 | 182 | ss2 | 87 | ss1 | +0.054360 | 0.241465 |
| L5 | H13 | 113 | other | 35 | other | +0.053743 | 0.113744 |
| L13 | H15 | 185 | ss2 | 115 | other | +0.051733 | 0.050840 |
| L16 | H7 | 185 | ss2 | 117 | other | +0.051658 | 0.090180 |
| L13 | H15 | 185 | ss2 | 114 | other | +0.043839 | 0.040306 |
| L13 | H14 | 185 | ss2 | 115 | other | +0.043463 | 0.074008 |
| L17 | H9 | 185 | ss2 | 53 | flkL | +0.042739 | 0.065029 |
| L16 | H7 | 83 | ss1 | 113 | other | +0.041361 | 0.407274 |
| L5 | H13 | 117 | other | 35 | other | +0.040715 | 0.100796 |
| L16 | H7 | 187 | ss2 | 113 | other | +0.039958 | 0.304261 |
| L23 | H15 | 82 | ss1 | 39 | flkL | +0.039700 | 0.364181 |
| L32 | H18 | 186 | ss2 | 82 | ss1 | +0.039636 | 0.221063 |
| L11 | H5 | 114 | other | 113 | other | +0.039032 | 0.126531 |
| L5 | H13 | 114 | other | 34 | other | +0.038493 | 0.014311 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H13 | 118 | other | 35 | other | -0.019653 | 0.099621 |
| L5 | H13 | 121 | other | 35 | other | -0.020238 | 0.123695 |
| L5 | H13 | 114 | other | 188 | ss2 | -0.020398 | 0.007333 |
| L5 | H13 | 106 | other | 35 | other | -0.020500 | 0.086383 |
| L5 | H13 | 107 | other | 35 | other | -0.021110 | 0.092454 |
| L16 | H7 | 204 | flkR | 113 | other | -0.021508 | 0.312970 |
| L5 | H13 | 108 | other | 35 | other | -0.021667 | 0.095334 |
| L16 | H7 | 87 | ss1 | 113 | other | -0.023283 | 0.347556 |
| L5 | H13 | 119 | other | 35 | other | -0.024300 | 0.107021 |
| L5 | H13 | 120 | other | 35 | other | -0.025833 | 0.118242 |
| L11 | H5 | 113 | other | 115 | other | -0.026384 | 0.202736 |
| L23 | H15 | 87 | ss1 | 39 | flkL | -0.029364 | 0.281284 |
| L11 | H5 | 114 | other | 112 | other | -0.029419 | 0.109053 |
| L23 | H15 | 84 | ss1 | 39 | flkL | -0.035746 | 0.405919 |
| L5 | H13 | 115 | other | 35 | other | -0.039118 | 0.117456 |
| L13 | H14 | 185 | ss2 | 113 | other | -0.062895 | 0.121917 |
| L5 | H13 | 116 | other | 35 | other | -0.081309 | 0.106945 |
| L5 | H13 | 111 | other | 35 | other | -0.093532 | 0.099500 |
| L16 | H7 | 185 | ss2 | 113 | other | -0.177872 | 0.289938 |
| L5 | H13 | 112 | other | 35 | other | -0.245938 | 0.106668 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.1492 | 0.00% |
| 10 | 10 | 6 | 0.1489 | -0.06% |
| 20 | 20 | 10 | 0.1530 | 0.67% |
| 50 | 50 | 18 | 0.1576 | 1.46% |
| 100 | 100 | 20 | 0.3090 | 28.06% |
| 200 | 200 | 23 | 0.4020 | 44.40% |
| 500 | 500 | 23 | 0.5285 | 66.62% |
| 1000 | 1,000 | 23 | 0.5871 | 76.91% |
| 2000 | 2,000 | 23 | 0.6397 | 86.15% |
| 5000 | 5,000 | 23 | 0.7365 | 103.16% |
| 10000 | 10,000 | 23 | 0.8004 | 114.39% |
| 20000 | 20,000 | 23 | 0.8316 | 119.85% |
| 50000 | 50,000 | 23 | 0.8842 | 129.10% |

## Motif Analysis

### L0 H14 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 5  |  total attr: +0.1912

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.1912 | 100.0% |

**Query mass** (top-1=97%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.1856 | 97.1% |
| 115 | other | +0.0021 | 1.1% |
| 191 | ss2 | +0.0013 | 0.7% |
| 114 | other | +0.0011 | 0.6% |
| 53 | flkL | +0.0011 | 0.6% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 20.0% |
| +76 | 1 | 20.0% |
| +152 | 1 | 20.0% |
| +75 | 1 | 20.0% |
| +14 | 1 | 20.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 2 | 40.0% |
| other | flkL | 2 | 40.0% |
| ss2 | flkL | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 39 | flkL | 39 | flkL | +0.1856 | 0.9827 |
| 115 | other | 39 | flkL | +0.0021 | 0.0023 |
| 191 | ss2 | 39 | flkL | +0.0013 | 0.0049 |
| 114 | other | 39 | flkL | +0.0011 | 0.0022 |
| 53 | flkL | 39 | flkL | +0.0011 | 0.0046 |

### L5 H13 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 49  |  total attr: +1.2068

**Key mass** (top-1=80%, top-2=86%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 35 | other | +0.9675 | 80.2% |
| 36 | other | +0.0759 | 6.3% |
| 34 | other | +0.0470 | 3.9% |
| 32 | other | +0.0207 | 1.7% |
| 65 | flkL | +0.0116 | 1.0% |

**Query mass** (top-1=82%, top-2=88%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.9931 | 82.3% |
| 110 | other | +0.0687 | 5.7% |
| 113 | other | +0.0628 | 5.2% |
| 117 | other | +0.0462 | 3.8% |
| 112 | other | +0.0204 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +78 | 3 | 6.1% |
| +81 | 3 | 6.1% |
| +47 | 3 | 6.1% |
| +79 | 2 | 4.1% |
| +75 | 2 | 4.1% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 20 | 40.8% |
| other | flkL | 12 | 24.5% |
| other | ss2 | 8 | 16.3% |
| other | ss1 | 7 | 14.3% |
| ss2 | other | 1 | 2.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 114 | other | 35 | other | +0.8104 | 0.1194 |
| 114 | other | 36 | other | +0.0652 | 0.0172 |
| 110 | other | 35 | other | +0.0591 | 0.0968 |
| 113 | other | 35 | other | +0.0537 | 0.1137 |
| 117 | other | 35 | other | +0.0407 | 0.1008 |

### L10 H9 — Rank #16

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 54  |  total attr: +0.1396

**Key mass** (top-1=53%, top-2=75%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.0736 | 52.8% |
| 115 | other | +0.0316 | 22.6% |
| 113 | other | +0.0304 | 21.8% |
| 45 | flkL | +0.0027 | 1.9% |
| 116 | other | +0.0013 | 0.9% |

**Query mass** (top-1=19%, top-2=29%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 184 | ss2 | +0.0270 | 19.3% |
| 84 | ss1 | +0.0137 | 9.8% |
| 182 | ss2 | +0.0114 | 8.2% |
| 181 | ss2 | +0.0091 | 6.5% |
| 204 | flkR | +0.0091 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +68 | 4 | 7.4% |
| +69 | 3 | 5.6% |
| +70 | 2 | 3.7% |
| -30 | 2 | 3.7% |
| +67 | 2 | 3.7% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 17 | 31.5% |
| flkR | other | 12 | 22.2% |
| flkL | other | 11 | 20.4% |
| ss1 | other | 6 | 11.1% |
| other | other | 6 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 184 | ss2 | 114 | other | +0.0127 | 0.0893 |
| 184 | ss2 | 115 | other | +0.0071 | 0.0546 |
| 84 | ss1 | 114 | other | +0.0061 | 0.1491 |
| 184 | ss2 | 113 | other | +0.0059 | 0.0458 |
| 182 | ss2 | 114 | other | +0.0056 | 0.0954 |

### L10 H12 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0501

**Key mass** (top-1=52%, top-2=73%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.0263 | 52.5% |
| 115 | other | +0.0105 | 20.9% |
| 113 | other | +0.0084 | 16.8% |
| 87 | ss1 | +0.0035 | 7.0% |
| 90 | other | +0.0014 | 2.9% |

**Query mass** (top-1=21%, top-2=36%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss2 | +0.0106 | 21.2% |
| 187 | ss2 | +0.0072 | 14.3% |
| 182 | ss2 | +0.0060 | 12.0% |
| 204 | flkR | +0.0051 | 10.2% |
| 114 | other | +0.0036 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +67 | 2 | 7.7% |
| +73 | 2 | 7.7% |
| +68 | 2 | 7.7% |
| +74 | 2 | 7.7% |
| +66 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 13 | 50.0% |
| other | other | 8 | 30.8% |
| flkR | other | 3 | 11.5% |
| other | ss1 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss2 | 114 | other | +0.0053 | 0.1051 |
| 187 | ss2 | 114 | other | +0.0033 | 0.0623 |
| 181 | ss2 | 115 | other | +0.0028 | 0.0692 |
| 182 | ss2 | 114 | other | +0.0028 | 0.0727 |
| 181 | ss2 | 113 | other | +0.0025 | 0.0550 |

### L10 H14 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.0640

**Key mass** (top-1=46%, top-2=75%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.0297 | 46.4% |
| 115 | other | +0.0183 | 28.6% |
| 113 | other | +0.0138 | 21.5% |
| 112 | other | +0.0012 | 1.8% |
| 116 | other | +0.0011 | 1.7% |

**Query mass** (top-1=24%, top-2=44%, top-3=63%)  [DISTR(L184/I206/I185/G188)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 184 | ss2 | +0.0154 | 24.1% |
| 206 | flkR | +0.0129 | 20.1% |
| 185 | ss2 | +0.0118 | 18.4% |
| 188 | ss2 | +0.0096 | 15.1% |
| 207 | flkR | +0.0061 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +92 | 2 | 8.7% |
| +70 | 2 | 8.7% |
| +71 | 2 | 8.7% |
| +72 | 2 | 8.7% |
| +69 | 2 | 8.7% |

**Region-pair profile** (q→k)  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 14 | 60.9% |
| flkR | other | 8 | 34.8% |
| other | other | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 206 | flkR | 114 | other | +0.0060 | 0.0855 |
| 184 | ss2 | 114 | other | +0.0055 | 0.0482 |
| 185 | ss2 | 114 | other | +0.0052 | 0.0537 |
| 188 | ss2 | 114 | other | +0.0042 | 0.0669 |
| 184 | ss2 | 113 | other | +0.0041 | 0.0382 |

### L11 H4 — Rank #5

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 48  |  total attr: +0.2207

**Key mass** (top-1=34%, top-2=68%, top-3=81%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 115 | other | +0.0755 | 34.2% |
| 114 | other | +0.0744 | 33.7% |
| 113 | other | +0.0297 | 13.5% |
| 116 | other | +0.0208 | 9.4% |
| 112 | other | +0.0102 | 4.6% |

**Query mass** (top-1=41%, top-2=64%, top-3=71%)  [DISTR(I185/L184/C183)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0906 | 41.0% |
| 184 | ss2 | +0.0513 | 23.2% |
| 183 | ss2 | +0.0158 | 7.2% |
| 191 | ss2 | +0.0123 | 5.6% |
| 204 | flkR | +0.0095 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +67 | 6 | 12.5% |
| +68 | 4 | 8.3% |
| +70 | 3 | 6.2% |
| +71 | 3 | 6.2% |
| +69 | 3 | 6.2% |

**Region-pair profile** (q→k)  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 28 | 58.3% |
| flkR | other | 14 | 29.2% |
| other | other | 6 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 115 | other | +0.0278 | 0.0907 |
| 185 | ss2 | 114 | other | +0.0260 | 0.0834 |
| 184 | ss2 | 114 | other | +0.0190 | 0.1020 |
| 184 | ss2 | 115 | other | +0.0183 | 0.1021 |
| 185 | ss2 | 113 | other | +0.0119 | 0.0389 |

### L11 H5 — Rank #13

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.1207

**Key mass** (top-1=56%, top-2=82%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 113 | other | +0.0682 | 56.5% |
| 114 | other | +0.0313 | 25.9% |
| 115 | other | +0.0161 | 13.3% |
| 112 | other | +0.0027 | 2.2% |
| 116 | other | +0.0025 | 2.0% |

**Query mass** (top-1=42%, top-2=64%, top-3=74%)  [DISTR(P114/I113/V112)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.0512 | 42.4% |
| 113 | other | +0.0259 | 21.4% |
| 112 | other | +0.0121 | 10.0% |
| 187 | ss2 | +0.0076 | 6.3% |
| 182 | ss2 | +0.0061 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 7.4% |
| +0 | 2 | 7.4% |
| -3 | 2 | 7.4% |
| -2 | 2 | 7.4% |
| +67 | 2 | 7.4% |

**Region-pair profile** (q→k)  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 12 | 44.4% |
| ss2 | other | 12 | 44.4% |
| ss1 | other | 2 | 7.4% |
| flkL | other | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 114 | other | 113 | other | +0.0390 | 0.1265 |
| 113 | other | 113 | other | +0.0197 | 0.1407 |
| 114 | other | 114 | other | +0.0121 | 0.0409 |
| 112 | other | 115 | other | +0.0090 | 0.1917 |
| 113 | other | 114 | other | +0.0061 | 0.0446 |

### L11 H14 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 47  |  total attr: +0.1107

**Key mass** (top-1=31%, top-2=56%, top-3=80%)  [DISTR(P114/S115/I113)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.0348 | 31.5% |
| 115 | other | +0.0275 | 24.8% |
| 113 | other | +0.0259 | 23.5% |
| 65 | flkL | +0.0072 | 6.5% |
| 116 | other | +0.0044 | 3.9% |

**Query mass** (top-1=17%, top-2=30%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0187 | 16.9% |
| 180 | other | +0.0150 | 13.6% |
| 181 | ss2 | +0.0142 | 12.8% |
| 182 | ss2 | +0.0119 | 10.7% |
| 186 | ss2 | +0.0099 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +68 | 4 | 8.5% |
| +66 | 3 | 6.4% |
| +67 | 3 | 6.4% |
| +72 | 3 | 6.4% |
| +74 | 3 | 6.4% |

**Region-pair profile** (q→k)  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 25 | 53.2% |
| ss1 | other | 6 | 12.8% |
| other | other | 5 | 10.6% |
| ss2 | flkR | 3 | 6.4% |
| flkR | other | 3 | 6.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 180 | other | 114 | other | +0.0047 | 0.1395 |
| 185 | ss2 | 65 | flkL | +0.0045 | 0.0536 |
| 181 | ss2 | 115 | other | +0.0043 | 0.0899 |
| 181 | ss2 | 114 | other | +0.0043 | 0.0983 |
| 180 | other | 115 | other | +0.0041 | 0.1118 |

### L11 H16 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 153  |  total attr: +0.4054

**Key mass** (top-1=32%, top-2=54%, top-3=73%)  [DISTR(I113/V112/S115)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 113 | other | +0.1301 | 32.1% |
| 112 | other | +0.0869 | 21.4% |
| 115 | other | +0.0798 | 19.7% |
| 114 | other | +0.0769 | 19.0% |
| 116 | other | +0.0179 | 4.4% |

**Query mass** (top-1=11%, top-2=21%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 117 | other | +0.0433 | 10.7% |
| 203 | flkR | +0.0432 | 10.6% |
| 186 | ss2 | +0.0224 | 5.5% |
| 116 | other | +0.0182 | 4.5% |
| 166 | other | +0.0172 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +51 | 5 | 3.3% |
| +57 | 5 | 3.3% |
| +53 | 4 | 2.6% |
| +52 | 4 | 2.6% |
| +54 | 4 | 2.6% |

**Region-pair profile** (q→k)  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 87 | 56.9% |
| flkR | other | 23 | 15.0% |
| ss1 | other | 15 | 9.8% |
| ss2 | other | 10 | 6.5% |
| flkL | other | 10 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 117 | other | 113 | other | +0.0197 | 0.2422 |
| 203 | flkR | 113 | other | +0.0117 | 0.1524 |
| 117 | other | 114 | other | +0.0100 | 0.1221 |
| 117 | other | 112 | other | +0.0098 | 0.1494 |
| 203 | flkR | 114 | other | +0.0093 | 0.1254 |

### L13 H14 — Rank #10

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 59  |  total attr: +0.2483

**Key mass** (top-1=34%, top-2=52%, top-3=65%)  [DISTR(S115/P114/F116/I113)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 115 | other | +0.0854 | 34.4% |
| 114 | other | +0.0428 | 17.2% |
| 116 | other | +0.0337 | 13.6% |
| 113 | other | +0.0319 | 12.8% |
| 112 | other | +0.0197 | 7.9% |

**Query mass** (top-1=35%, top-2=53%, top-3=59%)  [DISTR(I185/A186/?210/L184/I181)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0873 | 35.2% |
| 186 | ss2 | +0.0442 | 17.8% |
| 210 | flkR | +0.0156 | 6.3% |
| 184 | ss2 | +0.0141 | 5.7% |
| 181 | ss2 | +0.0131 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +69 | 6 | 10.2% |
| +67 | 5 | 8.5% |
| +70 | 3 | 5.1% |
| +68 | 3 | 5.1% |
| +75 | 3 | 5.1% |

**Region-pair profile** (q→k)  (top=49%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 29 | 49.2% |
| other | other | 12 | 20.3% |
| flkR | other | 11 | 18.6% |
| flkR | ss1 | 3 | 5.1% |
| flkR | flkL | 2 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 115 | other | +0.0435 | 0.0740 |
| 185 | ss2 | 116 | other | +0.0215 | 0.0458 |
| 186 | ss2 | 115 | other | +0.0168 | 0.0986 |
| 186 | ss2 | 114 | other | +0.0138 | 0.0741 |
| 185 | ss2 | 117 | other | +0.0108 | 0.0255 |

### L13 H15 — Rank #11

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 45  |  total attr: +0.2811

**Key mass** (top-1=39%, top-2=70%, top-3=78%)  [DISTR(P114/S115/F116)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.1090 | 38.8% |
| 115 | other | +0.0871 | 31.0% |
| 116 | other | +0.0232 | 8.2% |
| 112 | other | +0.0190 | 6.7% |
| 117 | other | +0.0119 | 4.2% |

**Query mass** (top-1=58%, top-2=71%, top-3=76%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.1639 | 58.3% |
| 83 | ss1 | +0.0349 | 12.4% |
| 204 | flkR | +0.0159 | 5.7% |
| 84 | ss1 | +0.0135 | 4.8% |
| 184 | ss2 | +0.0123 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +70 | 3 | 6.7% |
| +73 | 3 | 6.7% |
| +68 | 3 | 6.7% |
| +72 | 3 | 6.7% |
| -31 | 2 | 4.4% |

**Region-pair profile** (q→k)  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 19 | 42.2% |
| ss1 | other | 7 | 15.6% |
| flkR | other | 6 | 13.3% |
| other | other | 6 | 13.3% |
| flkL | other | 3 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 115 | other | +0.0517 | 0.0508 |
| 185 | ss2 | 114 | other | +0.0438 | 0.0403 |
| 83 | ss1 | 114 | other | +0.0237 | 0.2036 |
| 185 | ss2 | 116 | other | +0.0205 | 0.0250 |
| 185 | ss2 | 112 | other | +0.0149 | 0.0199 |

### L13 H18 — Rank #18

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 80  |  total attr: +0.2400

**Key mass** (top-1=48%, top-2=68%, top-3=83%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 113 | other | +0.1142 | 47.6% |
| 114 | other | +0.0485 | 20.2% |
| 115 | other | +0.0355 | 14.8% |
| 112 | other | +0.0121 | 5.0% |
| 116 | other | +0.0052 | 2.2% |

**Query mass** (top-1=15%, top-2=24%, top-3=32%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0350 | 14.6% |
| 183 | ss2 | +0.0223 | 9.3% |
| 82 | ss1 | +0.0184 | 7.7% |
| 84 | ss1 | +0.0161 | 6.7% |
| -1 | other | +0.0126 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -30 | 4 | 5.0% |
| +69 | 3 | 3.8% |
| +71 | 3 | 3.8% |
| +68 | 3 | 3.8% |
| -32 | 2 | 2.5% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 28 | 35.0% |
| ss2 | other | 22 | 27.5% |
| ss1 | other | 16 | 20.0% |
| flkR | flkR | 4 | 5.0% |
| flkR | other | 4 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 113 | other | +0.0126 | 0.2422 |
| 84 | ss1 | 114 | other | +0.0083 | 0.1202 |
| 82 | ss1 | 114 | other | +0.0081 | 0.1041 |
| 183 | ss2 | 114 | other | +0.0079 | 0.0779 |
| 185 | ss2 | 114 | other | +0.0076 | 0.0440 |

### L16 H7 — Rank #20

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 120  |  total attr: +0.6086

**Key mass** (top-1=43%, top-2=62%, top-3=75%)  [DISTR(I113/S115/A117)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 113 | other | +0.2623 | 43.1% |
| 115 | other | +0.1151 | 18.9% |
| 117 | other | +0.0765 | 12.6% |
| 116 | other | +0.0538 | 8.8% |
| 114 | other | +0.0531 | 8.7% |

**Query mass** (top-1=32%, top-2=39%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.1932 | 31.7% |
| 83 | ss1 | +0.0414 | 6.8% |
| 187 | ss2 | +0.0400 | 6.6% |
| 82 | ss1 | +0.0233 | 3.8% |
| 186 | ss2 | +0.0216 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +89 | 4 | 3.3% |
| +68 | 3 | 2.5% |
| +74 | 3 | 2.5% |
| +73 | 3 | 2.5% |
| +67 | 3 | 2.5% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 28 | 23.3% |
| flkL | other | 27 | 22.5% |
| other | other | 23 | 19.2% |
| ss2 | other | 22 | 18.3% |
| ss1 | other | 12 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 115 | other | +0.0619 | 0.0999 |
| 185 | ss2 | 117 | other | +0.0517 | 0.0902 |
| 83 | ss1 | 113 | other | +0.0414 | 0.4073 |
| 187 | ss2 | 113 | other | +0.0400 | 0.3043 |
| 185 | ss2 | 116 | other | +0.0377 | 0.0679 |

### L16 H10 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 58  |  total attr: +0.2027

**Key mass** (top-1=24%, top-2=46%, top-3=55%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | other | +0.0492 | 24.3% |
| 113 | other | +0.0443 | 21.8% |
| 183 | ss2 | +0.0178 | 8.8% |
| 180 | other | +0.0161 | 7.9% |
| 181 | ss2 | +0.0116 | 5.7% |

**Query mass** (top-1=27%, top-2=50%, top-3=63%)  [DISTR(S201/I185/I206/L187)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | flkR | +0.0538 | 26.6% |
| 185 | ss2 | +0.0480 | 23.7% |
| 206 | flkR | +0.0264 | 13.0% |
| 187 | ss2 | +0.0144 | 7.1% |
| 202 | flkR | +0.0131 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +71 | 3 | 5.2% |
| +21 | 3 | 5.2% |
| +22 | 3 | 5.2% |
| +90 | 3 | 5.2% |
| +91 | 3 | 5.2% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 26 | 44.8% |
| flkR | ss2 | 13 | 22.4% |
| ss2 | other | 12 | 20.7% |
| ss2 | ss1 | 5 | 8.6% |
| other | flkL | 2 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 114 | other | +0.0181 | 0.1179 |
| 185 | ss2 | 113 | other | +0.0144 | 0.1094 |
| 201 | flkR | 183 | ss2 | +0.0102 | 0.0760 |
| 187 | ss2 | 113 | other | +0.0075 | 0.0804 |
| 187 | ss2 | 114 | other | +0.0069 | 0.0788 |

### L17 H9 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 39  |  total attr: +0.2003

**Key mass** (top-1=26%, top-2=46%, top-3=57%)  [DISTR(F53/I113/S115/A117/P114)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.0518 | 25.9% |
| 113 | other | +0.0402 | 20.1% |
| 115 | other | +0.0222 | 11.1% |
| 117 | other | +0.0194 | 9.7% |
| 114 | other | +0.0181 | 9.0% |

**Query mass** (top-1=43%, top-2=60%, top-3=74%)  [DISTR(I185/S201/D204)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0852 | 42.6% |
| 201 | flkR | +0.0340 | 17.0% |
| 204 | flkR | +0.0286 | 14.3% |
| 188 | ss2 | +0.0235 | 11.7% |
| 210 | flkR | +0.0062 | 3.1% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +70 | 3 | 7.7% |
| +85 | 3 | 7.7% |
| +76 | 3 | 7.7% |
| +86 | 2 | 5.1% |
| +87 | 2 | 5.1% |

**Region-pair profile** (q→k)  (top=49%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 19 | 48.7% |
| flkR | other | 14 | 35.9% |
| ss2 | flkL | 2 | 5.1% |
| flkR | flkL | 2 | 5.1% |
| ss1 | flkL | 1 | 2.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 53 | flkL | +0.0427 | 0.0650 |
| 204 | flkR | 113 | other | +0.0248 | 0.1956 |
| 201 | flkR | 115 | other | +0.0096 | 0.0846 |
| 201 | flkR | 114 | other | +0.0086 | 0.0782 |
| 185 | ss2 | 115 | other | +0.0080 | 0.0232 |

### L17 H12 — Rank #22

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 30  |  total attr: +0.1237

**Key mass** (top-1=26%, top-2=50%, top-3=64%)  [DISTR(Q118/A117/I113/R111)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 118 | other | +0.0326 | 26.3% |
| 117 | other | +0.0288 | 23.3% |
| 113 | other | +0.0180 | 14.6% |
| 111 | other | +0.0163 | 13.2% |
| 116 | other | +0.0116 | 9.4% |

**Query mass** (top-1=57%, top-2=68%, top-3=75%)  [DISTR(I185/D204/G188)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | ss2 | +0.0702 | 56.8% |
| 204 | flkR | +0.0137 | 11.1% |
| 188 | ss2 | +0.0090 | 7.2% |
| 183 | ss2 | +0.0065 | 5.3% |
| 201 | flkR | +0.0051 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +69 | 4 | 13.3% |
| +70 | 3 | 10.0% |
| +75 | 2 | 6.7% |
| +74 | 2 | 6.7% |
| +88 | 2 | 6.7% |

**Region-pair profile** (q→k)  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 17 | 56.7% |
| flkR | other | 8 | 26.7% |
| other | other | 5 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 185 | ss2 | 117 | other | +0.0238 | 0.0828 |
| 185 | ss2 | 118 | other | +0.0217 | 0.0667 |
| 185 | ss2 | 116 | other | +0.0116 | 0.0513 |
| 188 | ss2 | 113 | other | +0.0067 | 0.0782 |
| 185 | ss2 | 111 | other | +0.0062 | 0.0575 |

### L23 H8 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | INTRA:flkR  |  cells: 10  |  total attr: +0.1006

**Key mass** (top-1=55%, top-2=85%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | flkR | +0.0548 | 54.5% |
| 202 | flkR | +0.0305 | 30.3% |
| 204 | flkR | +0.0079 | 7.9% |
| 185 | ss2 | +0.0043 | 4.3% |
| 39 | flkL | +0.0018 | 1.8% |

**Query mass** (top-1=56%, top-2=85%, top-3=92%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | flkR | +0.0560 | 55.7% |
| 205 | flkR | +0.0293 | 29.1% |
| 208 | flkR | +0.0068 | 6.8% |
| 43 | flkL | +0.0018 | 1.8% |
| 187 | ss2 | +0.0017 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 5 | 50.0% |
| +5 | 1 | 10.0% |
| +2 | 1 | 10.0% |
| +10 | 1 | 10.0% |
| +3 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 40.0% |
| flkL | flkL | 2 | 20.0% |
| ss2 | ss2 | 2 | 20.0% |
| flkR | ss2 | 1 | 10.0% |
| ss2 | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 206 | flkR | 202 | flkR | +0.0305 | 0.3769 |
| 205 | flkR | 201 | flkR | +0.0293 | 0.6924 |
| 206 | flkR | 201 | flkR | +0.0256 | 0.2771 |
| 208 | flkR | 204 | flkR | +0.0068 | 0.1156 |
| 43 | flkL | 39 | flkL | +0.0018 | 0.2966 |

### L23 H15 — Rank #14

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 25  |  total attr: +0.1352

**Key mass** (top-1=53%, top-2=78%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.0714 | 52.8% |
| 35 | other | +0.0336 | 24.8% |
| 113 | other | +0.0098 | 7.2% |
| 36 | other | +0.0045 | 3.3% |
| 114 | other | +0.0042 | 3.1% |

**Query mass** (top-1=29%, top-2=45%, top-3=58%)  [DISTR(L82/I185/V85/L187/A186)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | ss1 | +0.0397 | 29.4% |
| 185 | ss2 | +0.0214 | 15.9% |
| 85 | ss1 | +0.0166 | 12.3% |
| 187 | ss2 | +0.0145 | 10.7% |
| 186 | ss2 | +0.0125 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +150 | 2 | 8.0% |
| +151 | 2 | 8.0% |
| +148 | 2 | 8.0% |
| +144 | 2 | 8.0% |
| +43 | 1 | 4.0% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 7 | 28.0% |
| ss2 | flkL | 6 | 24.0% |
| ss1 | flkL | 5 | 20.0% |
| ss1 | other | 4 | 16.0% |
| ss2 | flkR | 2 | 8.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 82 | ss1 | 39 | flkL | +0.0397 | 0.3642 |
| 85 | ss1 | 39 | flkL | +0.0166 | 0.2357 |
| 185 | ss2 | 35 | other | +0.0164 | 0.1400 |
| 186 | ss2 | 35 | other | +0.0082 | 0.1641 |
| 87 | ss1 | 113 | other | +0.0069 | 0.1100 |

### L27 H10 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 15  |  total attr: +0.0886

**Key mass** (top-1=23%, top-2=42%, top-3=59%)  [DISTR(I206/I185/I181/A79)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 206 | flkR | +0.0205 | 23.2% |
| 185 | ss2 | +0.0168 | 19.0% |
| 181 | ss2 | +0.0149 | 16.8% |
| 79 | ss1 | +0.0117 | 13.1% |
| 204 | flkR | +0.0063 | 7.1% |

**Query mass** (top-1=19%, top-2=36%, top-3=49%)  [DISTR(L187/L184/L82/W208/L209)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 187 | ss2 | +0.0168 | 19.0% |
| 184 | ss2 | +0.0148 | 16.6% |
| 82 | ss1 | +0.0117 | 13.1% |
| 208 | flkR | +0.0114 | 12.9% |
| 209 | flkR | +0.0091 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 93%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 8 | 53.3% |
| +3 | 6 | 40.0% |
| -4 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 8 | 53.3% |
| flkR | flkR | 5 | 33.3% |
| ss1 | ss1 | 1 | 6.7% |
| other | other | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 187 | ss2 | 185 | ss2 | +0.0168 | 0.1658 |
| 82 | ss1 | 79 | ss1 | +0.0117 | 0.3188 |
| 208 | flkR | 206 | flkR | +0.0114 | 0.3697 |
| 184 | ss2 | 181 | ss2 | +0.0102 | 0.1504 |
| 209 | flkR | 206 | flkR | +0.0091 | 0.3052 |

### L27 H15 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.0960

**Key mass** (top-1=20%, top-2=37%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.0194 | 20.2% |
| 85 | ss1 | +0.0159 | 16.6% |
| 84 | ss1 | +0.0094 | 9.8% |
| 184 | ss2 | +0.0078 | 8.1% |
| 81 | ss1 | +0.0078 | 8.1% |

**Query mass** (top-1=20%, top-2=37%, top-3=51%)  [DISTR(C183/V85/V84/S87/L184)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss2 | +0.0193 | 20.2% |
| 85 | ss1 | +0.0159 | 16.5% |
| 84 | ss1 | +0.0140 | 14.6% |
| 87 | ss1 | +0.0133 | 13.9% |
| 184 | ss2 | +0.0096 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 2 | 9.1% |
| +127 | 2 | 9.1% |
| +98 | 1 | 4.5% |
| -98 | 1 | 4.5% |
| -100 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 31.8% |
| ss1 | ss2 | 5 | 22.7% |
| ss1 | flkL | 4 | 18.2% |
| ss2 | flkL | 3 | 13.6% |
| ss1 | other | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss2 | 85 | ss1 | +0.0159 | 0.2217 |
| 85 | ss1 | 183 | ss2 | +0.0159 | 0.3318 |
| 84 | ss1 | 184 | ss2 | +0.0078 | 0.0472 |
| 187 | ss2 | 81 | ss1 | +0.0078 | 0.1279 |
| 184 | ss2 | 84 | ss1 | +0.0073 | 0.1059 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 39  |  total attr: +0.1848

**Key mass** (top-1=18%, top-2=31%, top-3=42%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | ss1 | +0.0339 | 18.3% |
| 184 | ss2 | +0.0241 | 13.1% |
| 86 | ss1 | +0.0204 | 11.0% |
| 62 | flkL | +0.0133 | 7.2% |
| 84 | ss1 | +0.0128 | 6.9% |

**Query mass** (top-1=16%, top-2=30%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 186 | ss2 | +0.0293 | 15.9% |
| 187 | ss2 | +0.0261 | 14.1% |
| 84 | ss1 | +0.0228 | 12.3% |
| 181 | ss2 | +0.0189 | 10.2% |
| 182 | ss2 | +0.0136 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +95 | 2 | 5.1% |
| +123 | 2 | 5.1% |
| -91 | 2 | 5.1% |
| +150 | 2 | 5.1% |
| +104 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 28.2% |
| ss2 | flkL | 9 | 23.1% |
| ss1 | other | 5 | 12.8% |
| ss1 | ss2 | 3 | 7.7% |
| ss2 | other | 2 | 5.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 186 | ss2 | 82 | ss1 | +0.0280 | 0.2611 |
| 84 | ss1 | 184 | ss2 | +0.0228 | 0.2367 |
| 181 | ss2 | 86 | ss1 | +0.0170 | 0.3985 |
| 86 | ss1 | 181 | ss2 | +0.0098 | 0.1917 |
| 184 | ss2 | 84 | ss1 | +0.0092 | 0.0772 |

### L32 H13 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 14  |  total attr: +0.1300

**Key mass** (top-1=42%, top-2=70%, top-3=77%)  [DISTR(S87/A182/L184)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 87 | ss1 | +0.0544 | 41.8% |
| 182 | ss2 | +0.0364 | 28.0% |
| 184 | ss2 | +0.0092 | 7.1% |
| 82 | ss1 | +0.0076 | 5.8% |
| 86 | ss1 | +0.0061 | 4.7% |

**Query mass** (top-1=42%, top-2=70%, top-3=75%)  [DISTR(A182/S87/V84)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 182 | ss2 | +0.0544 | 41.8% |
| 87 | ss1 | +0.0364 | 28.0% |
| 84 | ss1 | +0.0065 | 5.0% |
| 187 | ss2 | +0.0063 | 4.8% |
| 181 | ss2 | +0.0061 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +95 | 2 | 14.3% |
| -95 | 2 | 14.3% |
| +104 | 2 | 14.3% |
| -104 | 2 | 14.3% |
| -100 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 57.1% |
| ss2 | ss1 | 6 | 42.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 182 | ss2 | 87 | ss1 | +0.0544 | 0.2415 |
| 87 | ss1 | 182 | ss2 | +0.0364 | 0.1619 |
| 84 | ss1 | 184 | ss2 | +0.0065 | 0.0316 |
| 181 | ss2 | 86 | ss1 | +0.0061 | 0.0891 |
| 186 | ss2 | 82 | ss1 | +0.0050 | 0.0454 |

### L32 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.1893

**Key mass** (top-1=50%, top-2=68%, top-3=75%)  [DISTR(L82/L184/L187)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | ss1 | +0.0943 | 49.8% |
| 184 | ss2 | +0.0337 | 17.8% |
| 187 | ss2 | +0.0144 | 7.6% |
| 182 | ss2 | +0.0134 | 7.1% |
| 186 | ss2 | +0.0112 | 5.9% |

**Query mass** (top-1=29%, top-2=50%, top-3=63%)  [DISTR(L184/A186/V84/L82)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 184 | ss2 | +0.0547 | 28.9% |
| 186 | ss2 | +0.0396 | 20.9% |
| 84 | ss1 | +0.0242 | 12.8% |
| 82 | ss1 | +0.0207 | 11.0% |
| 81 | ss1 | +0.0144 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 2 | 16.7% |
| +95 | 2 | 16.7% |
| +104 | 1 | 8.3% |
| -100 | 1 | 8.3% |
| -106 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 58.3% |
| ss1 | ss2 | 5 | 41.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 184 | ss2 | 82 | ss1 | +0.0547 | 0.1975 |
| 186 | ss2 | 82 | ss1 | +0.0396 | 0.2211 |
| 84 | ss1 | 184 | ss2 | +0.0242 | 0.0716 |
| 81 | ss1 | 187 | ss2 | +0.0144 | 0.1899 |
| 87 | ss1 | 182 | ss2 | +0.0134 | 0.0361 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #1 | L0 | H14 | 5 | +0.1912 | SINGLE-ANCHOR | A39 | SINGLE-ANCHOR | A39 |  | INTRA:flkL |
| #4 | L5 | H13 | 49 | +1.2068 | SINGLE-ANCHOR | I35 | SINGLE-ANCHOR | P114 |  |  |
| #16 | L10 | H9 | 54 | +0.1396 | DUAL-ANCHOR | P114/S115 | DISTRIBUTED |  |  |  |
| #9 | L10 | H12 | 26 | +0.0501 | DUAL-ANCHOR | P114/S115 | DISTRIBUTED |  |  |  |
| #21 | L10 | H14 | 23 | +0.0640 | DUAL-ANCHOR | P114/S115 | DISTRIBUTED | L184/I206/I185/G188 |  |  |
| #5 | L11 | H4 | 48 | +0.2207 | MULTI-ANCHOR |  | DISTRIBUTED | I185/L184/C183 |  |  |
| #13 | L11 | H5 | 27 | +0.1207 | DUAL-ANCHOR | I113/P114 | DISTRIBUTED | P114/I113/V112 |  |  |
| #23 | L11 | H14 | 47 | +0.1107 | DISTRIBUTED | P114/S115/I113 | DISTRIBUTED |  |  |  |
| #2 | L11 | H16 | 153 | +0.4054 | DISTRIBUTED | I113/V112/S115 | DISTRIBUTED |  |  |  |
| #10 | L13 | H14 | 59 | +0.2483 | DISTRIBUTED | S115/P114/F116/I113 | DISTRIBUTED | I185/A186/?210/L184/I181 |  |  |
| #11 | L13 | H15 | 45 | +0.2811 | DISTRIBUTED | P114/S115/F116 | DUAL-ANCHOR | I185/M83 |  |  |
| #18 | L13 | H18 | 80 | +0.2400 | MULTI-ANCHOR |  | DISTRIBUTED |  |  |  |
| #20 | L16 | H7 | 120 | +0.6086 | DISTRIBUTED | I113/S115/A117 | DISTRIBUTED |  |  |  |
| #12 | L16 | H10 | 58 | +0.2027 | DISTRIBUTED |  | DISTRIBUTED | S201/I185/I206/L187 |  |  |
| #15 | L17 | H9 | 39 | +0.2003 | DISTRIBUTED | F53/I113/S115/A117/P114 | DISTRIBUTED | I185/S201/D204 |  |  |
| #22 | L17 | H12 | 30 | +0.1237 | DISTRIBUTED | Q118/A117/I113/R111 | DISTRIBUTED | I185/D204/G188 |  |  |
| #17 | L23 | H8 | 10 | +0.1006 | DUAL-ANCHOR | S201/K202 | DUAL-ANCHOR | I206/A205 |  | INTRA:flkR |
| #14 | L23 | H15 | 25 | +0.1352 | DUAL-ANCHOR | A39/I35 | DISTRIBUTED | L82/I185/V85/L187/A186 |  |  |
| #19 | L27 | H10 | 15 | +0.0886 | DISTRIBUTED | I206/I185/I181/A79 | DISTRIBUTED | L187/L184/L82/W208/L209 | POSITIONAL | INTRA:ss2 |
| #8 | L27 | H15 | 22 | +0.0960 | DISTRIBUTED |  | DISTRIBUTED | C183/V85/V84/S87/L184 |  |  |
| #6 | L29 | H18 | 39 | +0.1848 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #7 | L32 | H13 | 14 | +0.1300 | DISTRIBUTED | S87/A182/L184 | DISTRIBUTED | A182/S87/V84 |  | CROSS:ss1→ss2 |
| #3 | L32 | H18 | 12 | +0.1893 | DISTRIBUTED | L82/L184/L187 | DISTRIBUTED | L184/A186/V84/L82 |  | CROSS:ss2→ss1 |
