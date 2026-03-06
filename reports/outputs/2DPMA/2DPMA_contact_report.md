# Contact Pattern Analysis: 2DPMA

Generated: 2026-03-03 05:23:17   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2DPMA |
| Contact pair | (59, 172) |
| ss1 | [54, 65) |
| ss2 | [167, 178) |
| Clean flank | 30 |
| Corrupt flank | 29 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.9394 |
| Corrupt metric | 0.0169 |
| Gap | 0.9226 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 71.15% |
| positive IE | 100 | 74.84% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L6 | H7 | +0.2775 |
| 2 | L10 | H9 | +0.2135 |
| 3 | L32 | H13 | +0.1393 |
| 4 | L10 | H12 | +0.1367 |
| 5 | L32 | H18 | +0.1153 |
| 6 | L12 | H17 | +0.1145 |
| 7 | L29 | H18 | +0.1048 |
| 8 | L22 | H14 | +0.1044 |
| 9 | L26 | H16 | +0.1022 |
| 10 | L30 | H1 | +0.0951 |
| 11 | L9 | H10 | +0.0835 |
| 12 | L7 | H0 | +0.0797 |
| 13 | L19 | H0 | +0.0782 |
| 14 | L16 | H7 | +0.0768 |
| 15 | L27 | H15 | +0.0668 |
| 16 | L13 | H1 | +0.0644 |
| 17 | L15 | H6 | +0.0606 |
| 18 | L11 | H14 | +0.0526 |
| 19 | L31 | H17 | +0.0526 |
| 20 | L13 | H8 | +0.0524 |
| 21 | L10 | H7 | +0.0518 |
| 22 | L17 | H1 | +0.0516 |
| 23 | L20 | H5 | +0.0493 |
| 24 | L18 | H8 | +0.0476 |
| 25 | L12 | H15 | +0.0473 |
| 26 | L12 | H16 | +0.0462 |
| 27 | L21 | H6 | +0.0449 |
| 28 | L5 | H19 | +0.0399 |
| 29 | L13 | H3 | +0.0392 |
| 30 | L14 | H14 | +0.0371 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.01% |
| 4 | 0.01% |
| 5 | 0.01% |
| 6 | -0.00% |
| 7 | 0.00% |
| 8 | 0.05% |
| 9 | 0.05% |
| 10 | 0.03% |
| 20 | 0.15% |
| 80 | 37.33% |
| 450 | 123.51% |

## Cell Attribution Analysis

Total cells: 8,005,648

- Positive: 3,993,758
- Negative: 4,009,611

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000078 | 800,566 |
| 95th | +0.00000247 | 400,283 |
| 99th | +0.00001983 | 80,057 |
| 99.5th | +0.00004270 | 40,029 |
| 99.9th | +0.00022730 | 8,006 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L12 | H15 | 172 | ss2 | 190 | flkR | +0.146079 | 0.629072 |
| L9 | H10 | 57 | ss1 | 42 | flkL | +0.138781 | 0.491393 |
| L6 | H7 | 57 | ss1 | 190 | flkR | +0.129432 | 0.116354 |
| L13 | H1 | 172 | ss2 | 190 | flkR | +0.121321 | 0.633528 |
| L12 | H16 | 57 | ss1 | 190 | flkR | +0.112599 | 0.657904 |
| L10 | H7 | 57 | ss1 | 39 | flkL | +0.106989 | 0.485167 |
| L13 | H8 | 57 | ss1 | 190 | flkR | +0.071413 | 0.902466 |
| L7 | H0 | 39 | flkL | 57 | ss1 | +0.069365 | 0.356735 |
| L11 | H14 | 57 | ss1 | 39 | flkL | +0.067562 | 0.263054 |
| L11 | H19 | 57 | ss1 | 42 | flkL | +0.060243 | 0.454416 |
| L10 | H9 | 42 | flkL | 39 | flkL | +0.057122 | 0.662712 |
| L11 | H15 | 59 | ss1 | 42 | flkL | +0.054390 | 0.606537 |
| L14 | H15 | 172 | ss2 | 176 | ss2 | +0.049228 | 0.635050 |
| L19 | H0 | 59 | ss1 | 57 | ss1 | +0.047562 | 0.569549 |
| L16 | H7 | 170 | ss2 | 190 | flkR | +0.046331 | 0.565395 |
| L10 | H9 | 59 | ss1 | 39 | flkL | +0.046216 | 0.528058 |
| L22 | H14 | 172 | ss2 | 59 | ss1 | +0.045170 | 0.329816 |
| L8 | H4 | 190 | flkR | 39 | flkL | +0.043880 | 0.234600 |
| L13 | H1 | 176 | ss2 | 190 | flkR | +0.043409 | 0.809371 |
| L12 | H15 | 170 | ss2 | 190 | flkR | +0.042321 | 0.807271 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L15 | H6 | 53 | flkL | 39 | flkL | -0.022892 | 0.914613 |
| L12 | H15 | 184 | flkR | 190 | flkR | -0.022908 | 0.728071 |
| L12 | H16 | 39 | flkL | 190 | flkR | -0.023299 | 0.828713 |
| L10 | H9 | 57 | ss1 | 190 | flkR | -0.023958 | 0.252298 |
| L12 | H15 | 175 | ss2 | 190 | flkR | -0.024913 | 0.845345 |
| L16 | H7 | 176 | ss2 | 190 | flkR | -0.026067 | 0.577911 |
| L9 | H10 | 59 | ss1 | 42 | flkL | -0.027218 | 0.519981 |
| L19 | H0 | 61 | ss1 | 59 | ss1 | -0.028940 | 0.797136 |
| L13 | H8 | 60 | ss1 | 190 | flkR | -0.028995 | 0.850919 |
| L13 | H12 | 59 | ss1 | 190 | flkR | -0.030870 | 0.558984 |
| L9 | H10 | 62 | ss1 | 42 | flkL | -0.032130 | 0.386155 |
| L12 | H17 | 170 | ss2 | 190 | flkR | -0.032141 | 0.624038 |
| L13 | H1 | 184 | flkR | 190 | flkR | -0.032446 | 0.656726 |
| L12 | H1 | 172 | ss2 | 190 | flkR | -0.032974 | 0.317549 |
| L14 | H14 | 61 | ss1 | 57 | ss1 | -0.034148 | 0.600090 |
| L11 | H10 | 57 | ss1 | 180 | flkR | -0.035720 | 0.502647 |
| L11 | H14 | 59 | ss1 | 39 | flkL | -0.036562 | 0.475657 |
| L13 | H1 | 171 | ss2 | 190 | flkR | -0.039812 | 0.732039 |
| L12 | H15 | 171 | ss2 | 190 | flkR | -0.042918 | 0.867572 |
| L10 | H9 | 57 | ss1 | 39 | flkL | -0.072984 | 0.523735 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0169 | 0.00% |
| 10 | 10 | 10 | 0.0169 | -0.00% |
| 20 | 20 | 17 | 0.0168 | -0.00% |
| 50 | 50 | 38 | 0.0169 | 0.00% |
| 100 | 100 | 57 | 0.0169 | 0.01% |
| 200 | 200 | 77 | 0.0170 | 0.02% |
| 500 | 500 | 95 | 0.0177 | 0.09% |
| 1000 | 1,000 | 99 | 0.0217 | 0.53% |
| 2000 | 2,000 | 100 | 0.0376 | 2.25% |
| 5000 | 5,000 | 100 | 0.0993 | 8.93% |
| 10000 | 10,000 | 100 | 0.1624 | 15.78% |
| 20000 | 20,000 | 100 | 0.2030 | 20.18% |
| 50000 | 50,000 | 100 | 0.2882 | 29.41% |

## Motif Analysis

### L5 H19 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.0548

**Key mass** (top-1=96%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.0524 | 95.6% |
| 203 | flkR | +0.0024 | 4.4% |

**Query mass** (top-1=74%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.0403 | 73.5% |
| 57 | ss1 | +0.0145 | 26.5% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +148 | 1 | 33.3% |
| +15 | 1 | 33.3% |
| -13 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 1 | 33.3% |
| ss1 | flkL | 1 | 33.3% |
| flkR | flkR | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 190 | flkR | 42 | flkL | +0.0379 | 0.0701 |
| 57 | ss1 | 42 | flkL | +0.0145 | 0.0204 |
| 190 | flkR | 203 | flkR | +0.0024 | 0.0056 |

### L6 H7 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:flkL→flkR  |  cells: 3  |  total attr: +0.1717

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.1717 | 100.0% |

**Query mass** (top-1=75%, top-2=90%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1294 | 75.4% |
| 39 | flkL | +0.0253 | 14.7% |
| 42 | flkL | +0.0170 | 9.9% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -133 | 1 | 33.3% |
| -151 | 1 | 33.3% |
| -148 | 1 | 33.3% |

**Region-pair profile** (q→k)  [CROSS:flkL→flkR]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 2 | 66.7% |
| ss1 | flkR | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 190 | flkR | +0.1294 | 0.1164 |
| 39 | flkL | 190 | flkR | +0.0253 | 0.1642 |
| 42 | flkL | 190 | flkR | +0.0170 | 0.1331 |

### L7 H0 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | flkL→ss1  |  cells: 1  |  total attr: +0.0694

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0694 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.0694 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -18 | 1 | 100.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 39 | flkL | 57 | ss1 | +0.0694 | 0.3567 |

### L9 H10 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 6  |  total attr: +0.1621

**Key mass** (top-1=96%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.1564 | 96.5% |
| 190 | flkR | +0.0030 | 1.8% |
| 44 | flkL | +0.0027 | 1.7% |

**Query mass** (top-1=87%, top-2=92%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1415 | 87.3% |
| 39 | flkL | +0.0082 | 5.0% |
| 56 | ss1 | +0.0047 | 2.9% |
| 63 | ss1 | +0.0047 | 2.9% |
| 176 | ss2 | +0.0030 | 1.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +15 | 1 | 16.7% |
| -3 | 1 | 16.7% |
| +14 | 1 | 16.7% |
| +21 | 1 | 16.7% |
| -14 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 66.7% |
| flkL | flkL | 1 | 16.7% |
| ss2 | flkR | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 42 | flkL | +0.1388 | 0.4914 |
| 39 | flkL | 42 | flkL | +0.0082 | 0.5357 |
| 56 | ss1 | 42 | flkL | +0.0047 | 0.2048 |
| 63 | ss1 | 42 | flkL | +0.0047 | 0.2678 |
| 176 | ss2 | 190 | flkR | +0.0030 | 0.1933 |

### L10 H7 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 1  |  total attr: +0.1070

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.1070 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1070 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 100.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 39 | flkL | +0.1070 | 0.4852 |

### L10 H9 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 35  |  total attr: +0.2381

**Key mass** (top-1=90%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.2140 | 89.9% |
| 190 | flkR | +0.0241 | 10.1% |

**Query mass** (top-1=24%, top-2=47%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.0571 | 24.0% |
| 59 | ss1 | +0.0542 | 22.8% |
| 40 | flkL | +0.0101 | 4.2% |
| 176 | ss2 | +0.0091 | 3.8% |
| 54 | ss1 | +0.0087 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 1 | 2.9% |
| +20 | 1 | 2.9% |
| +1 | 1 | 2.9% |
| +24 | 1 | 2.9% |
| -131 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 9 | 25.7% |
| other | flkL | 9 | 25.7% |
| ss1 | flkL | 6 | 17.1% |
| ss2 | flkL | 3 | 8.6% |
| flkR | flkL | 3 | 8.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 42 | flkL | 39 | flkL | +0.0571 | 0.6627 |
| 59 | ss1 | 39 | flkL | +0.0462 | 0.5281 |
| 40 | flkL | 39 | flkL | +0.0101 | 0.6437 |
| 63 | ss1 | 39 | flkL | +0.0082 | 0.4655 |
| 59 | ss1 | 190 | flkR | +0.0080 | 0.1894 |

### L10 H12 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.1364

**Key mass** (top-1=70%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.0959 | 70.3% |
| 190 | flkR | +0.0404 | 29.7% |

**Query mass** (top-1=24%, top-2=31%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0334 | 24.5% |
| 61 | ss1 | +0.0089 | 6.6% |
| 59 | ss1 | +0.0087 | 6.4% |
| 60 | ss1 | +0.0065 | 4.8% |
| 63 | ss1 | +0.0058 | 4.2% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 3.2% |
| +22 | 1 | 3.2% |
| +20 | 1 | 3.2% |
| +21 | 1 | 3.2% |
| +24 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=48%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 15 | 48.4% |
| ss1 | flkL | 9 | 29.0% |
| other | flkL | 6 | 19.4% |
| flkL | flkL | 1 | 3.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 39 | flkL | +0.0334 | 0.6655 |
| 61 | ss1 | 39 | flkL | +0.0089 | 0.5883 |
| 59 | ss1 | 39 | flkL | +0.0087 | 0.5538 |
| 60 | ss1 | 39 | flkL | +0.0065 | 0.6618 |
| 63 | ss1 | 39 | flkL | +0.0058 | 0.5878 |

### L11 H14 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 20  |  total attr: +0.1414

**Key mass** (top-1=70%, top-2=91%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 39 | flkL | +0.0989 | 70.0% |
| 190 | flkR | +0.0301 | 21.3% |
| 57 | ss1 | +0.0065 | 4.6% |
| 31 | flkL | +0.0032 | 2.2% |
| 42 | flkL | +0.0027 | 1.9% |

**Query mass** (top-1=58%, top-2=64%, top-3=69%)  [DISTR(A57/D61/K55/S229)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0814 | 57.5% |
| 61 | ss1 | +0.0096 | 6.8% |
| 55 | ss1 | +0.0067 | 4.8% |
| 229 | other | +0.0057 | 4.0% |
| 228 | other | +0.0057 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +15 | 2 | 10.0% |
| +18 | 1 | 5.0% |
| +22 | 1 | 5.0% |
| +16 | 1 | 5.0% |
| +39 | 1 | 5.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 8 | 40.0% |
| other | flkR | 6 | 30.0% |
| ss1 | ss1 | 2 | 10.0% |
| flkL | flkL | 1 | 5.0% |
| ss1 | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 39 | flkL | +0.0676 | 0.2631 |
| 61 | ss1 | 39 | flkL | +0.0077 | 0.3106 |
| 55 | ss1 | 39 | flkL | +0.0067 | 0.7399 |
| 229 | other | 190 | flkR | +0.0057 | 0.5482 |
| 228 | other | 190 | flkR | +0.0057 | 0.5472 |

### L12 H15 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 10  |  total attr: +0.2413

**Key mass** (top-1=96%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.2327 | 96.4% |
| 39 | flkL | +0.0064 | 2.7% |
| 180 | flkR | +0.0022 | 0.9% |

**Query mass** (top-1=61%, top-2=79%, top-3=88%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.1483 | 61.5% |
| 170 | ss2 | +0.0423 | 17.5% |
| 176 | ss2 | +0.0209 | 8.7% |
| 169 | ss2 | +0.0108 | 4.5% |
| 173 | ss2 | +0.0068 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -18 | 1 | 10.0% |
| -20 | 1 | 10.0% |
| -14 | 1 | 10.0% |
| -21 | 1 | 10.0% |
| -17 | 1 | 10.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 6 | 60.0% |
| other | flkL | 2 | 20.0% |
| flkR | flkR | 2 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 172 | ss2 | 190 | flkR | +0.1461 | 0.6291 |
| 170 | ss2 | 190 | flkR | +0.0423 | 0.8073 |
| 176 | ss2 | 190 | flkR | +0.0209 | 0.9189 |
| 169 | ss2 | 190 | flkR | +0.0108 | 0.8765 |
| 173 | ss2 | 190 | flkR | +0.0068 | 0.7745 |

### L12 H16 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→flkR  |  cells: 5  |  total attr: +0.1262

**Key mass** (top-1=92%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.1163 | 92.1% |
| -1 | other | +0.0047 | 3.7% |
| 39 | flkL | +0.0031 | 2.4% |
| 61 | ss1 | +0.0022 | 1.7% |

**Query mass** (top-1=91%, top-2=95%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1148 | 90.9% |
| 39 | flkL | +0.0047 | 3.7% |
| 61 | ss1 | +0.0037 | 2.9% |
| 190 | flkR | +0.0031 | 2.4% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -133 | 1 | 20.0% |
| +40 | 1 | 20.0% |
| -129 | 1 | 20.0% |
| +151 | 1 | 20.0% |
| -4 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 2 | 40.0% |
| flkL | other | 1 | 20.0% |
| flkR | flkL | 1 | 20.0% |
| ss1 | ss1 | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 190 | flkR | +0.1126 | 0.6579 |
| 39 | flkL | -1 | other | +0.0047 | 0.3338 |
| 61 | ss1 | 190 | flkR | +0.0037 | 0.1478 |
| 190 | flkR | 39 | flkL | +0.0031 | 0.1799 |
| 57 | ss1 | 61 | ss1 | +0.0022 | 0.0425 |

### L12 H17 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 41  |  total attr: +0.2813

**Key mass** (top-1=62%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.1755 | 62.4% |
| 190 | flkR | +0.1032 | 36.7% |
| 39 | flkL | +0.0026 | 0.9% |

**Query mass** (top-1=14%, top-2=22%, top-3=28%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0395 | 14.0% |
| 61 | ss1 | +0.0213 | 7.6% |
| 60 | ss1 | +0.0170 | 6.1% |
| 56 | ss1 | +0.0152 | 5.4% |
| 176 | ss2 | +0.0141 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 2 | 4.9% |
| +3 | 2 | 4.9% |
| -19 | 2 | 4.9% |
| +15 | 1 | 2.4% |
| +19 | 1 | 2.4% |

**Region-pair profile** (q→k)  (top=24%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 10 | 24.4% |
| flkL | flkL | 8 | 19.5% |
| ss1 | flkL | 7 | 17.1% |
| other | flkR | 6 | 14.6% |
| ss2 | flkR | 5 | 12.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 42 | flkL | +0.0369 | 0.6027 |
| 61 | ss1 | 42 | flkL | +0.0213 | 0.8239 |
| 60 | ss1 | 42 | flkL | +0.0170 | 0.7328 |
| 56 | ss1 | 42 | flkL | +0.0152 | 0.6962 |
| 176 | ss2 | 190 | flkR | +0.0141 | 0.7519 |

### L13 H1 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | ss2→flkR  |  cells: 11  |  total attr: +0.2114

**Key mass** (top-1=95%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.2017 | 95.4% |
| 65 | other | +0.0043 | 2.0% |
| 64 | ss1 | +0.0030 | 1.4% |
| 66 | other | +0.0025 | 1.2% |

**Query mass** (top-1=57%, top-2=78%, top-3=86%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.1213 | 57.4% |
| 176 | ss2 | +0.0434 | 20.5% |
| 170 | ss2 | +0.0162 | 7.6% |
| 57 | ss1 | +0.0131 | 6.2% |
| 174 | ss2 | +0.0059 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -18 | 1 | 9.1% |
| -14 | 1 | 9.1% |
| -20 | 1 | 9.1% |
| -16 | 1 | 9.1% |
| -17 | 1 | 9.1% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 5 | 45.5% |
| ss1 | other | 2 | 18.2% |
| ss1 | flkR | 2 | 18.2% |
| flkR | flkR | 1 | 9.1% |
| ss1 | ss1 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 172 | ss2 | 190 | flkR | +0.1213 | 0.6335 |
| 176 | ss2 | 190 | flkR | +0.0434 | 0.8094 |
| 170 | ss2 | 190 | flkR | +0.0162 | 0.7678 |
| 174 | ss2 | 190 | flkR | +0.0059 | 0.7347 |
| 173 | ss2 | 190 | flkR | +0.0043 | 0.8096 |

### L13 H3 — Rank #29

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.1213

**Key mass** (top-1=25%, top-2=46%, top-3=66%)  [DISTR(F42/A57/V190/F39)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.0299 | 24.6% |
| 57 | ss1 | +0.0255 | 21.0% |
| 190 | flkR | +0.0251 | 20.7% |
| 39 | flkL | +0.0188 | 15.5% |
| 182 | flkR | +0.0045 | 3.7% |

**Query mass** (top-1=16%, top-2=29%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0195 | 16.1% |
| 195 | flkR | +0.0161 | 13.3% |
| 42 | flkL | +0.0102 | 8.4% |
| 39 | flkL | +0.0095 | 7.8% |
| 54 | ss1 | +0.0081 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 6 | 25.0% |
| +3 | 3 | 12.5% |
| -3 | 2 | 8.3% |
| +15 | 2 | 8.3% |
| +8 | 2 | 8.3% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 29.2% |
| ss1 | ss1 | 6 | 25.0% |
| flkR | flkR | 3 | 12.5% |
| ss1 | flkL | 3 | 12.5% |
| ss2 | flkR | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 195 | flkR | 190 | flkR | +0.0161 | 0.9335 |
| 57 | ss1 | 57 | ss1 | +0.0124 | 0.3746 |
| 39 | flkL | 42 | flkL | +0.0095 | 0.8060 |
| 54 | ss1 | 39 | flkL | +0.0081 | 0.4205 |
| 42 | flkL | 39 | flkL | +0.0077 | 0.8492 |

### L13 H8 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.2264

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.2240 | 99.0% |
| 48 | flkL | +0.0024 | 1.0% |

**Query mass** (top-1=32%, top-2=46%, top-3=58%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0714 | 31.5% |
| 59 | ss1 | +0.0323 | 14.3% |
| 62 | ss1 | +0.0276 | 12.2% |
| 58 | ss1 | +0.0144 | 6.4% |
| 61 | ss1 | +0.0120 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -133 | 1 | 4.8% |
| -131 | 1 | 4.8% |
| -128 | 1 | 4.8% |
| -132 | 1 | 4.8% |
| -129 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 8 | 38.1% |
| flkL | flkR | 6 | 28.6% |
| other | flkR | 6 | 28.6% |
| ss2 | flkL | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 190 | flkR | +0.0714 | 0.9025 |
| 59 | ss1 | 190 | flkR | +0.0323 | 0.8775 |
| 62 | ss1 | 190 | flkR | +0.0276 | 0.8626 |
| 58 | ss1 | 190 | flkR | +0.0144 | 0.7992 |
| 61 | ss1 | 190 | flkR | +0.0120 | 0.8437 |

### L14 H14 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.1577

**Key mass** (top-1=26%, top-2=47%, top-3=60%)  [DISTR(A57/A53/D193/D176/P54)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0410 | 26.0% |
| 53 | flkL | +0.0325 | 20.6% |
| 193 | flkR | +0.0205 | 13.0% |
| 176 | ss2 | +0.0137 | 8.7% |
| 54 | ss1 | +0.0107 | 6.8% |

**Query mass** (top-1=36%, top-2=55%, top-3=72%)  [DISTR(I59/F62/V190)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0564 | 35.7% |
| 62 | ss1 | +0.0301 | 19.1% |
| 190 | flkR | +0.0272 | 17.3% |
| 172 | ss2 | +0.0137 | 8.7% |
| 194 | flkR | +0.0093 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 47%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 5 | 29.4% |
| +5 | 3 | 17.6% |
| -4 | 2 | 11.8% |
| -3 | 1 | 5.9% |
| +4 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 29.4% |
| flkR | flkR | 5 | 29.4% |
| ss1 | flkL | 3 | 17.6% |
| ss2 | ss2 | 1 | 5.9% |
| other | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 59 | ss1 | 53 | flkL | +0.0325 | 0.4707 |
| 62 | ss1 | 57 | ss1 | +0.0301 | 0.5068 |
| 190 | flkR | 193 | flkR | +0.0205 | 0.7267 |
| 172 | ss2 | 176 | ss2 | +0.0137 | 0.6865 |
| 59 | ss1 | 54 | ss1 | +0.0107 | 0.1843 |

### L15 H6 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 17  |  total attr: +0.1582

**Key mass** (top-1=65%, top-2=85%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.1027 | 65.0% |
| 39 | flkL | +0.0325 | 20.5% |
| 57 | ss1 | +0.0116 | 7.4% |
| 172 | ss2 | +0.0114 | 7.2% |

**Query mass** (top-1=23%, top-2=33%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | ss2 | +0.0371 | 23.5% |
| 169 | ss2 | +0.0151 | 9.6% |
| 176 | ss2 | +0.0134 | 8.5% |
| 49 | flkL | +0.0130 | 8.2% |
| 190 | flkR | +0.0114 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 2 | 11.8% |
| -20 | 1 | 5.9% |
| -21 | 1 | 5.9% |
| -14 | 1 | 5.9% |
| +10 | 1 | 5.9% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 8 | 47.1% |
| flkL | flkL | 2 | 11.8% |
| ss1 | ss1 | 2 | 11.8% |
| ss1 | flkL | 2 | 11.8% |
| flkR | ss2 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | ss2 | 190 | flkR | +0.0371 | 0.8802 |
| 169 | ss2 | 190 | flkR | +0.0151 | 0.9260 |
| 176 | ss2 | 190 | flkR | +0.0134 | 0.8598 |
| 49 | flkL | 39 | flkL | +0.0130 | 0.7692 |
| 190 | flkR | 172 | ss2 | +0.0114 | 0.5594 |

### L16 H7 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 36  |  total attr: +0.2246

**Key mass** (top-1=62%, top-2=86%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.1381 | 61.5% |
| 39 | flkL | +0.0547 | 24.4% |
| 62 | ss1 | +0.0230 | 10.2% |
| 177 | ss2 | +0.0066 | 3.0% |
| 57 | ss1 | +0.0021 | 0.9% |

**Query mass** (top-1=24%, top-2=32%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | ss2 | +0.0542 | 24.1% |
| 173 | ss2 | +0.0166 | 7.4% |
| 56 | ss1 | +0.0159 | 7.1% |
| 175 | ss2 | +0.0136 | 6.1% |
| 177 | ss2 | +0.0130 | 5.8% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 2 | 5.6% |
| -21 | 2 | 5.6% |
| -6 | 2 | 5.6% |
| +0 | 2 | 5.6% |
| +1 | 2 | 5.6% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 8 | 22.2% |
| flkR | flkR | 6 | 16.7% |
| ss1 | ss1 | 5 | 13.9% |
| ss1 | flkL | 4 | 11.1% |
| ss2 | flkL | 4 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | ss2 | 190 | flkR | +0.0463 | 0.5654 |
| 173 | ss2 | 190 | flkR | +0.0136 | 0.5906 |
| 175 | ss2 | 190 | flkR | +0.0136 | 0.6207 |
| 177 | ss2 | 190 | flkR | +0.0130 | 0.6750 |
| 56 | ss1 | 39 | flkL | +0.0097 | 0.6376 |

### L17 H1 — Rank #22

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 27  |  total attr: +0.0847

**Key mass** (top-1=15%, top-2=27%, top-3=36%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0123 | 14.5% |
| 71 | other | +0.0102 | 12.0% |
| 68 | other | +0.0077 | 9.1% |
| 70 | other | +0.0070 | 8.3% |
| 67 | other | +0.0069 | 8.2% |

**Query mass** (top-1=42%, top-2=71%, top-3=76%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0356 | 42.1% |
| 57 | ss1 | +0.0246 | 29.1% |
| 43 | flkL | +0.0045 | 5.3% |
| 172 | ss2 | +0.0043 | 5.1% |
| 40 | flkL | +0.0041 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -14 | 5 | 18.5% |
| -12 | 3 | 11.1% |
| -15 | 3 | 11.1% |
| -13 | 3 | 11.1% |
| -11 | 2 | 7.4% |

**Region-pair profile** (q→k)  (top=70%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 19 | 70.4% |
| flkL | ss1 | 3 | 11.1% |
| ss2 | flkR | 3 | 11.1% |
| other | ss2 | 1 | 3.7% |
| flkL | flkL | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 59 | ss1 | 71 | other | +0.0060 | 0.1065 |
| 59 | ss1 | 70 | other | +0.0045 | 0.0769 |
| 43 | flkL | 57 | ss1 | +0.0045 | 0.3026 |
| 59 | ss1 | 68 | other | +0.0044 | 0.0648 |
| 172 | ss2 | 184 | flkR | +0.0043 | 0.3147 |

### L18 H8 — Rank #24

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 13  |  total attr: +0.0819

**Key mass** (top-1=42%, top-2=58%, top-3=70%)  [DISTR(D176/D61/N60)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0343 | 41.9% |
| 61 | ss1 | +0.0129 | 15.7% |
| 60 | ss1 | +0.0104 | 12.8% |
| 42 | flkL | +0.0054 | 6.6% |
| 190 | flkR | +0.0044 | 5.4% |

**Query mass** (top-1=31%, top-2=52%, top-3=63%)  [DISTR(I172/A57/K173/Y38)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.0254 | 31.0% |
| 57 | ss1 | +0.0176 | 21.5% |
| 173 | ss2 | +0.0089 | 10.9% |
| 38 | flkL | +0.0083 | 10.1% |
| 59 | ss1 | +0.0058 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 69%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 5 | 38.5% |
| -4 | 4 | 30.8% |
| -3 | 2 | 15.4% |
| -5 | 1 | 7.7% |
| -1 | 1 | 7.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 46.2% |
| flkR | flkR | 3 | 23.1% |
| ss2 | ss2 | 2 | 15.4% |
| flkL | flkL | 2 | 15.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 172 | ss2 | 176 | ss2 | +0.0254 | 0.8381 |
| 57 | ss1 | 61 | ss1 | +0.0092 | 0.6028 |
| 173 | ss2 | 176 | ss2 | +0.0089 | 0.7913 |
| 57 | ss1 | 60 | ss1 | +0.0084 | 0.3931 |
| 38 | flkL | 42 | flkL | +0.0054 | 0.8265 |

### L19 H0 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 18  |  total attr: +0.1820

**Key mass** (top-1=29%, top-2=46%, top-3=62%)  [DISTR(A57/F62/P41/N60)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0527 | 29.0% |
| 62 | ss1 | +0.0304 | 16.7% |
| 41 | flkL | +0.0303 | 16.6% |
| 60 | ss1 | +0.0141 | 7.7% |
| 55 | ss1 | +0.0114 | 6.3% |

**Query mass** (top-1=29%, top-2=45%, top-3=62%)  [DISTR(I59/F62/Y70/F49)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0521 | 28.6% |
| 62 | ss1 | +0.0307 | 16.9% |
| 70 | other | +0.0304 | 16.7% |
| 49 | flkL | +0.0291 | 16.0% |
| 57 | ss1 | +0.0119 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 61%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 7 | 38.9% |
| +8 | 4 | 22.2% |
| +7 | 3 | 16.7% |
| +1 | 2 | 11.1% |
| +3 | 1 | 5.6% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 50.0% |
| flkL | flkL | 3 | 16.7% |
| ss1 | flkL | 3 | 16.7% |
| other | ss1 | 1 | 5.6% |
| flkL | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 59 | ss1 | 57 | ss1 | +0.0476 | 0.5695 |
| 70 | other | 62 | ss1 | +0.0304 | 0.7353 |
| 49 | flkL | 41 | flkL | +0.0268 | 0.8790 |
| 62 | ss1 | 60 | ss1 | +0.0119 | 0.7560 |
| 62 | ss1 | 55 | ss1 | +0.0114 | 0.5473 |

### L20 H5 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 15  |  total attr: +0.0980

**Key mass** (top-1=34%, top-2=56%, top-3=73%)  [DISTR(D61/I172/D176)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0333 | 33.9% |
| 172 | ss2 | +0.0212 | 21.6% |
| 176 | ss2 | +0.0174 | 17.8% |
| 174 | ss2 | +0.0115 | 11.8% |
| 62 | ss1 | +0.0040 | 4.1% |

**Query mass** (top-1=31%, top-2=56%, top-3=72%)  [DISTR(A57/L170/N167)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0305 | 31.1% |
| 170 | ss2 | +0.0248 | 25.4% |
| 167 | ss2 | +0.0148 | 15.1% |
| 172 | ss2 | +0.0072 | 7.4% |
| 56 | ss1 | +0.0068 | 6.9% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 5 | 33.3% |
| -5 | 4 | 26.7% |
| -3 | 2 | 13.3% |
| -2 | 2 | 13.3% |
| -6 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 10 | 66.7% |
| ss1 | ss1 | 4 | 26.7% |
| flkL | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 61 | ss1 | +0.0265 | 0.5210 |
| 167 | ss2 | 172 | ss2 | +0.0148 | 0.5687 |
| 170 | ss2 | 174 | ss2 | +0.0115 | 0.2424 |
| 172 | ss2 | 176 | ss2 | +0.0072 | 0.5436 |
| 56 | ss1 | 61 | ss1 | +0.0068 | 0.3988 |

### L21 H6 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | POSITIONAL | INTRA:ss1  |  cells: 10  |  total attr: +0.0906

**Key mass** (top-1=64%, top-2=81%, top-3=87%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0583 | 64.3% |
| 176 | ss2 | +0.0154 | 17.0% |
| 177 | ss2 | +0.0047 | 5.2% |
| 63 | ss1 | +0.0037 | 4.1% |
| 41 | flkL | +0.0034 | 3.7% |

**Query mass** (top-1=41%, top-2=67%, top-3=84%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0373 | 41.1% |
| 59 | ss1 | +0.0238 | 26.3% |
| 172 | ss2 | +0.0150 | 16.5% |
| 173 | ss2 | +0.0052 | 5.8% |
| 40 | flkL | +0.0034 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 4 | 40.0% |
| -5 | 2 | 20.0% |
| -2 | 1 | 10.0% |
| -3 | 1 | 10.0% |
| -1 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 50.0% |
| ss2 | ss2 | 4 | 40.0% |
| flkL | flkL | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 61 | ss1 | +0.0349 | 0.3809 |
| 59 | ss1 | 61 | ss1 | +0.0201 | 0.3316 |
| 172 | ss2 | 176 | ss2 | +0.0102 | 0.7121 |
| 173 | ss2 | 176 | ss2 | +0.0052 | 0.7365 |
| 172 | ss2 | 177 | ss2 | +0.0047 | 0.1944 |

### L22 H14 — Rank #8

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS:ss2→ss1  |  cells: 13  |  total attr: +0.1221

**Key mass** (top-1=44%, top-2=76%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0542 | 44.4% |
| 57 | ss1 | +0.0383 | 31.4% |
| 58 | ss1 | +0.0113 | 9.2% |
| 40 | flkL | +0.0044 | 3.6% |
| 36 | flkL | +0.0035 | 2.9% |

**Query mass** (top-1=39%, top-2=75%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.0472 | 38.7% |
| 170 | ss2 | +0.0449 | 36.7% |
| 173 | ss2 | +0.0113 | 9.2% |
| 169 | ss2 | +0.0045 | 3.7% |
| 55 | ss1 | +0.0035 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 3 | 23.1% |
| +111 | 2 | 15.4% |
| +115 | 1 | 7.7% |
| +19 | 1 | 7.7% |
| +112 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 53.8% |
| ss1 | flkL | 3 | 23.1% |
| flkL | flkR | 1 | 7.7% |
| flkL | flkL | 1 | 7.7% |
| ss2 | flkL | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 172 | ss2 | 59 | ss1 | +0.0452 | 0.3298 |
| 170 | ss2 | 57 | ss1 | +0.0359 | 0.2315 |
| 173 | ss2 | 58 | ss1 | +0.0113 | 0.5377 |
| 170 | ss2 | 59 | ss1 | +0.0090 | 0.1349 |
| 55 | ss1 | 36 | flkL | +0.0035 | 0.4586 |

### L26 H16 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss1→ss2  |  cells: 9  |  total attr: +0.0802

**Key mass** (top-1=47%, top-2=67%, top-3=76%)  [DISTR(L170/I172/F177)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | ss2 | +0.0377 | 47.1% |
| 172 | ss2 | +0.0164 | 20.4% |
| 177 | ss2 | +0.0070 | 8.8% |
| 169 | ss2 | +0.0070 | 8.7% |
| 56 | ss1 | +0.0045 | 5.6% |

**Query mass** (top-1=39%, top-2=60%, top-3=72%)  [DISTR(A57/I59/F62)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0316 | 39.5% |
| 59 | ss1 | +0.0164 | 20.4% |
| 62 | ss1 | +0.0095 | 11.9% |
| 56 | ss1 | +0.0070 | 8.7% |
| 170 | ss2 | +0.0061 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 56%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 4 | 44.4% |
| -115 | 1 | 11.1% |
| +0 | 1 | 11.1% |
| -19 | 1 | 11.1% |
| -114 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 66.7% |
| flkL | ss1 | 2 | 22.2% |
| ss2 | ss2 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 170 | ss2 | +0.0316 | 0.3934 |
| 59 | ss1 | 172 | ss2 | +0.0164 | 0.2179 |
| 62 | ss1 | 177 | ss2 | +0.0070 | 0.3534 |
| 56 | ss1 | 169 | ss2 | +0.0070 | 0.3363 |
| 170 | ss2 | 170 | ss2 | +0.0061 | 0.1633 |

### L27 H15 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.0586

**Key mass** (top-1=24%, top-2=43%, top-3=58%)  [DISTR(I59/D56/N60/V58)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0140 | 23.9% |
| 56 | ss1 | +0.0114 | 19.5% |
| 60 | ss1 | +0.0086 | 14.6% |
| 58 | ss1 | +0.0082 | 14.0% |
| 37 | flkL | +0.0071 | 12.0% |

**Query mass** (top-1=22%, top-2=41%, top-3=56%)  [DISTR(I172/Q169/K173/L170/D56)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.0129 | 21.9% |
| 169 | ss2 | +0.0114 | 19.5% |
| 173 | ss2 | +0.0086 | 14.8% |
| 170 | ss2 | +0.0071 | 12.2% |
| 56 | ss1 | +0.0071 | 12.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 4 | 33.3% |
| +19 | 2 | 16.7% |
| +115 | 2 | 16.7% |
| +114 | 1 | 8.3% |
| +111 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 75.0% |
| ss1 | flkL | 2 | 16.7% |
| flkL | ss1 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | ss2 | 56 | ss1 | +0.0114 | 0.1978 |
| 172 | ss2 | 59 | ss1 | +0.0110 | 0.0792 |
| 56 | ss1 | 37 | flkL | +0.0071 | 0.6005 |
| 173 | ss2 | 58 | ss1 | +0.0060 | 0.2279 |
| 170 | ss2 | 57 | ss1 | +0.0041 | 0.0297 |

### L29 H18 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.1077

**Key mass** (top-1=31%, top-2=51%, top-3=69%)  [DISTR(D176/V174/F49/A57)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0329 | 30.5% |
| 174 | ss2 | +0.0219 | 20.4% |
| 49 | flkL | +0.0198 | 18.4% |
| 57 | ss1 | +0.0096 | 8.9% |
| 53 | flkL | +0.0038 | 3.5% |

**Query mass** (top-1=44%, top-2=63%, top-3=76%)  [DISTR(F62/I59/L170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0479 | 44.5% |
| 59 | ss1 | +0.0197 | 18.3% |
| 170 | ss2 | +0.0141 | 13.1% |
| 176 | ss2 | +0.0092 | 8.5% |
| 64 | ss1 | +0.0068 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 3 | 20.0% |
| -114 | 1 | 6.7% |
| +10 | 1 | 6.7% |
| -112 | 1 | 6.7% |
| -110 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 26.7% |
| ss1 | ss2 | 3 | 20.0% |
| ss1 | flkL | 3 | 20.0% |
| ss2 | flkL | 2 | 13.3% |
| ss2 | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 62 | ss1 | 176 | ss2 | +0.0303 | 0.2419 |
| 59 | ss1 | 49 | flkL | +0.0175 | 0.7911 |
| 62 | ss1 | 174 | ss2 | +0.0151 | 0.2119 |
| 170 | ss2 | 57 | ss1 | +0.0096 | 0.1214 |
| 64 | ss1 | 174 | ss2 | +0.0068 | 0.8814 |

### L30 H1 — Rank #10

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0730

**Key mass** (top-1=51%, top-2=66%, top-3=76%)  [DISTR(A57/Q169/E171)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.0371 | 50.8% |
| 169 | ss2 | +0.0109 | 14.9% |
| 171 | ss2 | +0.0076 | 10.4% |
| 59 | ss1 | +0.0049 | 6.7% |
| 172 | ss2 | +0.0045 | 6.2% |

**Query mass** (top-1=55%, top-2=70%, top-3=85%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | ss2 | +0.0398 | 54.6% |
| 58 | ss1 | +0.0112 | 15.4% |
| 56 | ss1 | +0.0109 | 14.9% |
| 59 | ss1 | +0.0045 | 6.2% |
| 62 | ss1 | +0.0044 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 62%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 3 | 37.5% |
| +113 | 2 | 25.0% |
| -114 | 1 | 12.5% |
| -115 | 1 | 12.5% |
| +111 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 62.5% |
| ss2 | ss1 | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | ss2 | 57 | ss1 | +0.0371 | 0.3162 |
| 56 | ss1 | 169 | ss2 | +0.0109 | 0.2650 |
| 58 | ss1 | 171 | ss2 | +0.0076 | 0.6972 |
| 59 | ss1 | 172 | ss2 | +0.0045 | 0.0347 |
| 62 | ss1 | 176 | ss2 | +0.0044 | 0.0753 |

### L31 H17 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 8  |  total attr: +0.0275

**Key mass** (top-1=65%, top-2=92%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0178 | 64.9% |
| 59 | ss1 | +0.0074 | 27.0% |
| 62 | ss1 | +0.0022 | 8.1% |

**Query mass** (top-1=27%, top-2=50%, top-3=67%)  [DISTR(I172/L170/?284/I59)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 172 | ss2 | +0.0074 | 26.8% |
| 170 | ss2 | +0.0064 | 23.3% |
| 284 | other | +0.0046 | 16.9% |
| 59 | ss1 | +0.0038 | 13.8% |
| -1 | other | +0.0030 | 11.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 1 | 12.5% |
| +285 | 1 | 12.5% |
| +171 | 1 | 12.5% |
| +60 | 1 | 12.5% |
| +0 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 37.5% |
| other | other | 2 | 25.0% |
| ss2 | other | 2 | 25.0% |
| ss1 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 172 | ss2 | 59 | ss1 | +0.0054 | 0.0984 |
| 284 | other | -1 | other | +0.0046 | 0.2097 |
| 170 | ss2 | -1 | other | +0.0044 | 0.0712 |
| 59 | ss1 | -1 | other | +0.0038 | 0.0554 |
| -1 | other | -1 | other | +0.0030 | 0.1003 |

### L32 H13 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 14  |  total attr: +0.0817

**Key mass** (top-1=19%, top-2=37%, top-3=50%)  [DISTR(D56/L170/I59/D176/F62)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 56 | ss1 | +0.0158 | 19.3% |
| 170 | ss2 | +0.0148 | 18.1% |
| 59 | ss1 | +0.0101 | 12.3% |
| 176 | ss2 | +0.0092 | 11.2% |
| 62 | ss1 | +0.0078 | 9.6% |

**Query mass** (top-1=19%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 169 | ss2 | +0.0158 | 19.3% |
| 57 | ss1 | +0.0102 | 12.5% |
| 59 | ss1 | +0.0098 | 12.0% |
| 62 | ss1 | +0.0092 | 11.2% |
| 176 | ss2 | +0.0078 | 9.6% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 3 | 21.4% |
| +113 | 2 | 14.3% |
| -115 | 2 | 14.3% |
| -114 | 1 | 7.1% |
| +114 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 57.1% |
| ss2 | ss1 | 6 | 42.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 169 | ss2 | 56 | ss1 | +0.0158 | 0.2183 |
| 57 | ss1 | 170 | ss2 | +0.0102 | 0.0561 |
| 62 | ss1 | 176 | ss2 | +0.0092 | 0.1040 |
| 176 | ss2 | 62 | ss1 | +0.0078 | 0.0889 |
| 172 | ss2 | 59 | ss1 | +0.0058 | 0.0312 |

### L32 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.0779

**Key mass** (top-1=30%, top-2=47%, top-3=63%)  [DISTR(F62/I59/I172/D176)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0235 | 30.2% |
| 59 | ss1 | +0.0130 | 16.7% |
| 172 | ss2 | +0.0122 | 15.7% |
| 176 | ss2 | +0.0077 | 9.9% |
| 170 | ss2 | +0.0066 | 8.5% |

**Query mass** (top-1=21%, top-2=38%, top-3=52%)  [DISTR(I59/V174/F62/D176/L170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 59 | ss1 | +0.0164 | 21.0% |
| 174 | ss2 | +0.0131 | 16.7% |
| 62 | ss1 | +0.0113 | 14.5% |
| 176 | ss2 | +0.0105 | 13.5% |
| 170 | ss2 | +0.0101 | 13.0% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +113 | 3 | 25.0% |
| -113 | 2 | 16.7% |
| +112 | 1 | 8.3% |
| +114 | 1 | 8.3% |
| -114 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 58.3% |
| ss1 | ss2 | 5 | 41.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 174 | ss2 | 62 | ss1 | +0.0131 | 0.3384 |
| 59 | ss1 | 172 | ss2 | +0.0122 | 0.0395 |
| 176 | ss2 | 62 | ss1 | +0.0105 | 0.0726 |
| 172 | ss2 | 59 | ss1 | +0.0082 | 0.0265 |
| 62 | ss1 | 176 | ss2 | +0.0077 | 0.0534 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #28 | L5 | H19 | 3 | +0.0548 | SINGLE-ANCHOR | F42 | SINGLE-ANCHOR | V190 |  |  |
| #1 | L6 | H7 | 3 | +0.1717 | SINGLE-ANCHOR | V190 | SINGLE-ANCHOR | A57 |  | CROSS:flkL→flkR |
| #12 | L7 | H0 | 1 | +0.0694 | SINGLE-ANCHOR | A57 | SINGLE-ANCHOR | F39 |  | flkL→ss1 |
| #11 | L9 | H10 | 6 | +0.1621 | SINGLE-ANCHOR | F42 | SINGLE-ANCHOR | A57 |  | ss1→flkL |
| #21 | L10 | H7 | 1 | +0.1070 | SINGLE-ANCHOR | F39 | SINGLE-ANCHOR | A57 |  | ss1→flkL |
| #2 | L10 | H9 | 35 | +0.2381 | SINGLE-ANCHOR | F39 | DISTRIBUTED |  |  |  |
| #4 | L10 | H12 | 31 | +0.1364 | SINGLE-ANCHOR | F39 | DISTRIBUTED |  |  |  |
| #18 | L11 | H14 | 20 | +0.1414 | SINGLE-ANCHOR | F39 | DISTRIBUTED | A57/D61/K55/S229 |  | ss1→flkL |
| #25 | L12 | H15 | 10 | +0.2413 | SINGLE-ANCHOR | V190 | SINGLE-ANCHOR | I172 |  | ss2→flkR |
| #26 | L12 | H16 | 5 | +0.1262 | SINGLE-ANCHOR | V190 | SINGLE-ANCHOR | A57 |  | CROSS:ss1→flkR |
| #6 | L12 | H17 | 41 | +0.2813 | SINGLE-ANCHOR | F42 | DISTRIBUTED |  |  |  |
| #16 | L13 | H1 | 11 | +0.2114 | SINGLE-ANCHOR | V190 | DUAL-ANCHOR | I172/D176 |  | ss2→flkR |
| #29 | L13 | H3 | 24 | +0.1213 | DISTRIBUTED | F42/A57/V190/F39 | DISTRIBUTED |  |  |  |
| #20 | L13 | H8 | 21 | +0.2264 | SINGLE-ANCHOR | V190 | DISTRIBUTED |  |  |  |
| #30 | L14 | H14 | 17 | +0.1577 | DISTRIBUTED | A57/A53/D193/D176/P54 | DISTRIBUTED | I59/F62/V190 |  |  |
| #17 | L15 | H6 | 17 | +0.1582 | SINGLE-ANCHOR | V190 | DISTRIBUTED |  |  | ss2→flkR |
| #14 | L16 | H7 | 36 | +0.2246 | SINGLE-ANCHOR | V190 | DISTRIBUTED |  |  |  |
| #22 | L17 | H1 | 27 | +0.0847 | DISTRIBUTED |  | DUAL-ANCHOR | I59/A57 |  |  |
| #24 | L18 | H8 | 13 | +0.0819 | DISTRIBUTED | D176/D61/N60 | DISTRIBUTED | I172/A57/K173/Y38 | POSITIONAL | INTRA:ss1 |
| #13 | L19 | H0 | 18 | +0.1820 | DISTRIBUTED | A57/F62/P41/N60 | DISTRIBUTED | I59/F62/Y70/F49 | POSITIONAL | INTRA:ss1 |
| #23 | L20 | H5 | 15 | +0.0980 | DISTRIBUTED | D61/I172/D176 | DISTRIBUTED | A57/L170/N167 | POSITIONAL | INTRA:ss2 |
| #27 | L21 | H6 | 10 | +0.0906 | SINGLE-ANCHOR | D61 | MULTI-ANCHOR |  | POSITIONAL | INTRA:ss1 |
| #8 | L22 | H14 | 13 | +0.1221 | DUAL-ANCHOR | I59/A57 | DUAL-ANCHOR | I172/L170 |  | CROSS:ss2→ss1 |
| #9 | L26 | H16 | 9 | +0.0802 | DISTRIBUTED | L170/I172/F177 | DISTRIBUTED | A57/I59/F62 | CROSS_SSE | CROSS:ss1→ss2 |
| #15 | L27 | H15 | 12 | +0.0586 | DISTRIBUTED | I59/D56/N60/V58 | DISTRIBUTED | I172/Q169/K173/L170/D56 | CROSS_SSE | CROSS:ss2→ss1 |
| #7 | L29 | H18 | 15 | +0.1077 | DISTRIBUTED | D176/V174/F49/A57 | DISTRIBUTED | F62/I59/L170 |  |  |
| #10 | L30 | H1 | 8 | +0.0730 | DISTRIBUTED | A57/Q169/E171 | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss1→ss2 |
| #19 | L31 | H17 | 8 | +0.0275 | SINGLE-ANCHOR | ?-1 | DISTRIBUTED | I172/L170/?284/I59 |  |  |
| #3 | L32 | H13 | 14 | +0.0817 | DISTRIBUTED | D56/L170/I59/D176/F62 | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #5 | L32 | H18 | 12 | +0.0779 | DISTRIBUTED | F62/I59/I172/D176 | DISTRIBUTED | I59/V174/F62/D176/L170 |  | CROSS:ss2→ss1 |
