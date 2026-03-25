# Contact Pattern Analysis: 2QY6A

Generated: 2026-03-22 21:19:41   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2QY6A |
| Contact pair | (63, 177) |
| ss1 | [58, 69) |
| ss2 | [172, 183) |
| Clean flank | 32 |
| Corrupt flank | 31 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.5565 |
| Corrupt metric | 0.0317 |
| Gap | 0.5248 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 250 | 105.16% |
| positive IE | 40 | 79.86% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L10 | H9 | +0.8597 |
| 2 | L10 | H19 | +0.4968 |
| 3 | L10 | H0 | +0.4457 |
| 4 | L6 | H7 | +0.3996 |
| 5 | L22 | H14 | +0.3221 |
| 6 | L11 | H0 | +0.3077 |
| 7 | L27 | H15 | +0.2364 |
| 8 | L13 | H1 | +0.1818 |
| 9 | L14 | H9 | +0.1553 |
| 10 | L13 | H3 | +0.1443 |
| 11 | L12 | H1 | +0.1438 |
| 12 | L13 | H2 | +0.1438 |
| 13 | L17 | H18 | +0.1405 |
| 14 | L4 | H9 | +0.1303 |
| 15 | L29 | H18 | +0.1234 |
| 16 | L11 | H8 | +0.1230 |
| 17 | L26 | H16 | +0.1133 |
| 18 | L17 | H10 | +0.1033 |
| 19 | L12 | H9 | +0.0970 |
| 20 | L7 | H13 | +0.0959 |
| 21 | L1 | H8 | +0.0925 |
| 22 | L28 | H13 | +0.0776 |
| 23 | L11 | H9 | +0.0769 |
| 24 | L18 | H16 | +0.0752 |
| 25 | L14 | H19 | +0.0725 |
| 26 | L12 | H3 | +0.0707 |
| 27 | L0 | H11 | +0.0678 |
| 28 | L9 | H8 | +0.0601 |
| 29 | L12 | H16 | +0.0591 |
| 30 | L16 | H6 | +0.0590 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.00% |
| 4 | 0.00% |
| 5 | 0.15% |
| 6 | 0.16% |
| 7 | 0.74% |
| 8 | 0.82% |
| 9 | 1.10% |
| 10 | 1.35% |
| 20 | 15.55% |
| 80 | 139.58% |
| 450 | 207.44% |

## Cell Attribution Analysis

Total cells: 2,521,822

- Positive: 1,254,169
- Negative: 1,266,623

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000105 | 252,183 |
| 95th | +0.00000344 | 126,092 |
| 99th | +0.00002839 | 25,219 |
| 99.5th | +0.00006204 | 12,610 |
| 99.9th | +0.00036142 | 2,522 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L10 | H19 | 67 | ss1 | 64 | ss1 | +0.204135 | 0.239443 |
| L10 | H9 | 64 | ss1 | 64 | ss1 | +0.174898 | 0.324975 |
| L6 | H7 | 64 | ss1 | 176 | ss2 | +0.166610 | 0.038027 |
| L10 | H9 | 67 | ss1 | 64 | ss1 | +0.150295 | 0.489325 |
| L11 | H0 | 63 | ss1 | 67 | ss1 | +0.128613 | 0.381801 |
| L10 | H0 | 67 | ss1 | 64 | ss1 | +0.127801 | 0.321239 |
| L10 | H9 | 61 | ss1 | 64 | ss1 | +0.099026 | 0.545982 |
| L12 | H1 | 64 | ss1 | 176 | ss2 | +0.085571 | 0.356133 |
| L13 | H3 | 63 | ss1 | 67 | ss1 | +0.072410 | 0.331533 |
| L10 | H9 | 66 | ss1 | 64 | ss1 | +0.069057 | 0.422213 |
| L10 | H9 | -1 | other | 64 | ss1 | +0.068569 | 0.383308 |
| L10 | H9 | 63 | ss1 | 64 | ss1 | +0.059602 | 0.633129 |
| L10 | H19 | 63 | ss1 | 64 | ss1 | +0.051994 | 0.249653 |
| L10 | H9 | 62 | ss1 | 64 | ss1 | +0.051687 | 0.581333 |
| L10 | H0 | 63 | ss1 | 64 | ss1 | +0.050870 | 0.459478 |
| L10 | H5 | 67 | ss1 | 64 | ss1 | +0.050267 | 0.042836 |
| L10 | H0 | 66 | ss1 | 64 | ss1 | +0.049850 | 0.317092 |
| L18 | H16 | 63 | ss1 | 208 | flkR | +0.049311 | 0.694991 |
| L10 | H0 | 69 | other | 64 | ss1 | +0.046449 | 0.434668 |
| L11 | H8 | 61 | ss1 | 176 | ss2 | +0.044320 | 0.363562 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H13 | 33 | flkL | 33 | flkL | -0.018465 | 0.157499 |
| L11 | H8 | 62 | ss1 | 176 | ss2 | -0.018467 | 0.352272 |
| L13 | H3 | 173 | ss2 | 176 | ss2 | -0.018586 | 0.280036 |
| L6 | H7 | 60 | ss1 | 176 | ss2 | -0.018834 | 0.040550 |
| L12 | H3 | 60 | ss1 | 176 | ss2 | -0.019420 | 0.395073 |
| L10 | H9 | 42 | flkL | 64 | ss1 | -0.020041 | 0.566710 |
| L13 | H2 | 64 | ss1 | 64 | ss1 | -0.020327 | 0.175632 |
| L11 | H8 | 63 | ss1 | 176 | ss2 | -0.020473 | 0.520082 |
| L7 | H13 | 27 | flkL | 27 | flkL | -0.020990 | 0.130681 |
| L10 | H9 | 61 | ss1 | 176 | ss2 | -0.021737 | 0.138447 |
| L10 | H0 | 176 | ss2 | 176 | ss2 | -0.021778 | 0.076131 |
| L13 | H3 | 67 | ss1 | 67 | ss1 | -0.021837 | 0.193462 |
| L12 | H16 | 64 | ss1 | 257 | other | -0.022017 | 0.170654 |
| L12 | H3 | 66 | ss1 | 179 | ss2 | -0.022594 | 0.149542 |
| L11 | H0 | 73 | other | 67 | ss1 | -0.024127 | 0.478602 |
| L17 | H10 | 65 | ss1 | 61 | ss1 | -0.024476 | 0.671043 |
| L7 | H13 | 32 | flkL | 32 | flkL | -0.042404 | 0.189184 |
| L10 | H0 | 65 | ss1 | 64 | ss1 | -0.044313 | 0.429683 |
| L11 | H8 | 68 | ss1 | 176 | ss2 | -0.044760 | 0.579285 |
| L10 | H9 | 64 | ss1 | 176 | ss2 | -0.088628 | 0.292085 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0317 | 0.00% |
| 10 | 10 | 7 | 0.0318 | 0.02% |
| 20 | 20 | 10 | 0.0318 | 0.02% |
| 50 | 50 | 24 | 0.0346 | 0.55% |
| 100 | 100 | 33 | 0.0867 | 10.48% |
| 200 | 200 | 37 | 0.1531 | 23.14% |
| 500 | 500 | 40 | 0.3202 | 54.97% |
| 1000 | 1,000 | 40 | 0.4427 | 78.32% |
| 2000 | 2,000 | 40 | 0.5071 | 90.59% |
| 5000 | 5,000 | 40 | 0.6015 | 108.58% |
| 10000 | 10,000 | 40 | 0.6345 | 114.85% |
| 20000 | 20,000 | 40 | 0.6664 | 120.93% |
| 50000 | 50,000 | 40 | 0.6941 | 126.22% |

## Motif Analysis

### L0 H11 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0256

**Key mass** (top-1=84%, top-2=90%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 214 | flkR | +0.0215 | 84.0% |
| 56 | flkL | +0.0015 | 5.9% |
| 58 | ss1 | +0.0014 | 5.5% |
| 26 | flkL | +0.0012 | 4.7% |

**Query mass** (top-1=27%, top-2=48%, top-3=60%)  [DISTR(D179/E65/D26/A64/A202)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 179 | ss2 | +0.0069 | 27.1% |
| 65 | ss1 | +0.0054 | 21.0% |
| 26 | flkL | +0.0029 | 11.4% |
| 64 | ss1 | +0.0021 | 8.2% |
| 202 | flkR | +0.0018 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -35 | 1 | 9.1% |
| -149 | 1 | 9.1% |
| -150 | 1 | 9.1% |
| -12 | 1 | 9.1% |
| -151 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 4 | 36.4% |
| ss2 | flkR | 3 | 27.3% |
| flkR | flkR | 1 | 9.1% |
| flkL | flkL | 1 | 9.1% |
| flkL | ss1 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 179 | ss2 | 214 | flkR | +0.0069 | 0.0207 |
| 65 | ss1 | 214 | flkR | +0.0054 | 0.0119 |
| 64 | ss1 | 214 | flkR | +0.0021 | 0.0018 |
| 202 | flkR | 214 | flkR | +0.0018 | 0.0022 |
| 63 | ss1 | 214 | flkR | +0.0016 | 0.0018 |

### L1 H8 — Rank #21

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:flkR  |  cells: 17  |  total attr: +0.0888

**Key mass** (top-1=30%, top-2=54%, top-3=71%)  [DISTR(F181/A214/F68)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss2 | +0.0265 | 29.9% |
| 214 | flkR | +0.0212 | 23.9% |
| 68 | ss1 | +0.0153 | 17.3% |
| 67 | ss1 | +0.0069 | 7.7% |
| 26 | flkL | +0.0048 | 5.4% |

**Query mass** (top-1=30%, top-2=55%, top-3=73%)  [DISTR(F177/A64/T210)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 177 | ss2 | +0.0265 | 29.9% |
| 64 | ss1 | +0.0222 | 25.0% |
| 210 | flkR | +0.0157 | 17.7% |
| 21 | other | +0.0048 | 5.4% |
| -1 | other | +0.0036 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 76%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 9 | 52.9% |
| -5 | 4 | 23.5% |
| -3 | 3 | 17.6% |
| -215 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 7 | 41.2% |
| ss2 | ss2 | 3 | 17.6% |
| ss1 | ss1 | 2 | 11.8% |
| flkL | flkL | 2 | 11.8% |
| other | flkL | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 177 | ss2 | 181 | ss2 | +0.0265 | 0.0138 |
| 210 | flkR | 214 | flkR | +0.0157 | 0.4086 |
| 64 | ss1 | 68 | ss1 | +0.0153 | 0.0165 |
| 64 | ss1 | 67 | ss1 | +0.0069 | 0.0158 |
| 21 | other | 26 | flkL | +0.0048 | 0.0862 |

### L4 H9 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 30  |  total attr: +0.0478

**Key mass** (top-1=65%, top-2=78%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 26 | flkL | +0.0309 | 64.6% |
| 214 | flkR | +0.0063 | 13.1% |
| 27 | flkL | +0.0053 | 11.2% |
| 47 | flkL | +0.0016 | 3.3% |
| 50 | flkL | +0.0013 | 2.8% |

**Query mass** (top-1=12%, top-2=21%, top-3=28%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0057 | 11.9% |
| 64 | ss1 | +0.0041 | 8.7% |
| 63 | ss1 | +0.0034 | 7.1% |
| 28 | flkL | +0.0030 | 6.3% |
| 61 | ss1 | +0.0029 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +14 | 2 | 6.7% |
| +19 | 2 | 6.7% |
| +17 | 2 | 6.7% |
| +1 | 2 | 6.7% |
| -38 | 1 | 3.3% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 15 | 50.0% |
| ss1 | flkL | 7 | 23.3% |
| other | flkL | 3 | 10.0% |
| ss2 | flkL | 2 | 6.7% |
| ss2 | flkR | 1 | 3.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 176 | ss2 | 214 | flkR | +0.0045 | 0.0041 |
| 63 | ss1 | 26 | flkL | +0.0034 | 0.0293 |
| 61 | ss1 | 26 | flkL | +0.0029 | 0.0284 |
| 62 | ss1 | 26 | flkL | +0.0023 | 0.0318 |
| 28 | flkL | 26 | flkL | +0.0019 | 0.0323 |

### L6 H7 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 14  |  total attr: +0.1893

**Key mass** (top-1=98%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.1861 | 98.3% |
| 26 | flkL | +0.0021 | 1.1% |
| 205 | flkR | +0.0012 | 0.6% |

**Query mass** (top-1=90%, top-2=92%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.1698 | 89.7% |
| 63 | ss1 | +0.0047 | 2.5% |
| 84 | other | +0.0019 | 1.0% |
| 75 | other | +0.0019 | 1.0% |
| 99 | other | +0.0018 | 0.9% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 1 | 7.1% |
| -113 | 1 | 7.1% |
| +38 | 1 | 7.1% |
| -92 | 1 | 7.1% |
| -101 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 9 | 64.3% |
| ss1 | ss2 | 2 | 14.3% |
| ss1 | flkL | 1 | 7.1% |
| flkL | ss2 | 1 | 7.1% |
| ss1 | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 176 | ss2 | +0.1666 | 0.0380 |
| 63 | ss1 | 176 | ss2 | +0.0047 | 0.0290 |
| 64 | ss1 | 26 | flkL | +0.0021 | 0.0035 |
| 84 | other | 176 | ss2 | +0.0019 | 0.0308 |
| 75 | other | 176 | ss2 | +0.0019 | 0.0332 |

### L7 H13 — Rank #20

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 70  |  total attr: +0.3134

**Key mass** (top-1=10%, top-2=20%, top-3=28%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0316 | 10.1% |
| 26 | flkL | +0.0302 | 9.6% |
| 212 | flkR | +0.0275 | 8.8% |
| 210 | flkR | +0.0259 | 8.3% |
| 181 | ss2 | +0.0175 | 5.6% |

**Query mass** (top-1=20%, top-2=29%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0634 | 20.2% |
| 61 | ss1 | +0.0264 | 8.4% |
| 62 | ss1 | +0.0242 | 7.7% |
| 39 | flkL | +0.0214 | 6.8% |
| 26 | flkL | +0.0196 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 14 | 20.0% |
| +35 | 3 | 4.3% |
| -151 | 2 | 2.9% |
| -150 | 2 | 2.9% |
| -147 | 2 | 2.9% |

**Region-pair profile** (q→k)  (top=14%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 10 | 14.3% |
| flkL | flkR | 10 | 14.3% |
| ss1 | flkR | 8 | 11.4% |
| ss1 | flkL | 6 | 8.6% |
| ss1 | ss1 | 5 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 63 | ss1 | +0.0282 | 0.0830 |
| 26 | flkL | 26 | flkL | +0.0196 | 0.3061 |
| 39 | flkL | 39 | flkL | +0.0162 | 0.0498 |
| 61 | ss1 | 212 | flkR | +0.0151 | 0.0529 |
| 63 | ss1 | 198 | flkR | +0.0147 | 0.0692 |

### L9 H8 — Rank #28

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | ss1→flkL  |  cells: 17  |  total attr: +0.0393

**Key mass** (top-1=38%, top-2=49%, top-3=58%)  [DISTR(D27/E65/D179/D26/E50)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 27 | flkL | +0.0150 | 38.2% |
| 65 | ss1 | +0.0041 | 10.5% |
| 179 | ss2 | +0.0037 | 9.4% |
| 26 | flkL | +0.0034 | 8.6% |
| 50 | flkL | +0.0029 | 7.3% |

**Query mass** (top-1=41%, top-2=64%, top-3=73%)  [DISTR(A64/G67/N32)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0162 | 41.1% |
| 67 | ss1 | +0.0091 | 23.1% |
| 32 | flkL | +0.0034 | 8.6% |
| 63 | ss1 | +0.0033 | 8.5% |
| 60 | ss1 | +0.0020 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +33 | 2 | 11.8% |
| +37 | 1 | 5.9% |
| -112 | 1 | 5.9% |
| +6 | 1 | 5.9% |
| +36 | 1 | 5.9% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 9 | 52.9% |
| ss1 | ss2 | 2 | 11.8% |
| flkL | flkL | 1 | 5.9% |
| ss1 | flkR | 1 | 5.9% |
| ss2 | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 27 | flkL | +0.0063 | 0.0197 |
| 67 | ss1 | 179 | ss2 | +0.0037 | 0.0142 |
| 32 | flkL | 26 | flkL | +0.0034 | 0.0981 |
| 63 | ss1 | 27 | flkL | +0.0033 | 0.0397 |
| 67 | ss1 | 27 | flkL | +0.0033 | 0.0097 |

### L10 H0 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 41  |  total attr: +0.4357

**Key mass** (top-1=83%, top-2=90%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.3614 | 82.9% |
| 26 | flkL | +0.0327 | 7.5% |
| 176 | ss2 | +0.0310 | 7.1% |
| 56 | flkL | +0.0045 | 1.0% |
| 185 | flkR | +0.0017 | 0.4% |

**Query mass** (top-1=30%, top-2=42%, top-3=53%)  [DISTR(G67/V63/S66/G69/F61)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 67 | ss1 | +0.1312 | 30.1% |
| 63 | ss1 | +0.0509 | 11.7% |
| 66 | ss1 | +0.0498 | 11.4% |
| 69 | other | +0.0464 | 10.7% |
| 61 | ss1 | +0.0394 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 3 | 7.3% |
| -3 | 3 | 7.3% |
| +5 | 2 | 4.9% |
| +6 | 2 | 4.9% |
| +10 | 2 | 4.9% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 11 | 26.8% |
| ss1 | ss1 | 7 | 17.1% |
| other | ss1 | 4 | 9.8% |
| ss2 | ss2 | 4 | 9.8% |
| flkR | ss2 | 4 | 9.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 67 | ss1 | 64 | ss1 | +0.1278 | 0.3212 |
| 63 | ss1 | 64 | ss1 | +0.0509 | 0.4595 |
| 66 | ss1 | 64 | ss1 | +0.0498 | 0.3171 |
| 69 | other | 64 | ss1 | +0.0464 | 0.4347 |
| 61 | ss1 | 64 | ss1 | +0.0381 | 0.2283 |

### L10 H9 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 72  |  total attr: +1.0980

**Key mass** (top-1=97%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +1.0653 | 97.0% |
| 176 | ss2 | +0.0153 | 1.4% |
| 208 | flkR | +0.0104 | 1.0% |
| 56 | flkL | +0.0070 | 0.6% |

**Query mass** (top-1=16%, top-2=30%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.1749 | 15.9% |
| 67 | ss1 | +0.1531 | 13.9% |
| 61 | ss1 | +0.1005 | 9.2% |
| 66 | ss1 | +0.0705 | 6.4% |
| -1 | other | +0.0686 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 2.8% |
| +7 | 2 | 2.8% |
| +5 | 2 | 2.8% |
| -32 | 2 | 2.8% |
| +10 | 2 | 2.8% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 20 | 27.8% |
| flkR | ss1 | 16 | 22.2% |
| flkL | ss1 | 10 | 13.9% |
| ss1 | ss1 | 9 | 12.5% |
| ss2 | ss1 | 8 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 64 | ss1 | +0.1749 | 0.3250 |
| 67 | ss1 | 64 | ss1 | +0.1503 | 0.4893 |
| 61 | ss1 | 64 | ss1 | +0.0990 | 0.5460 |
| 66 | ss1 | 64 | ss1 | +0.0691 | 0.4222 |
| -1 | other | 64 | ss1 | +0.0686 | 0.3833 |

### L10 H19 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 26  |  total attr: +0.3763

**Key mass** (top-1=88%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.3308 | 87.9% |
| 67 | ss1 | +0.0186 | 4.9% |
| 66 | ss1 | +0.0080 | 2.1% |
| 65 | ss1 | +0.0067 | 1.8% |
| 176 | ss2 | +0.0026 | 0.7% |

**Query mass** (top-1=60%, top-2=76%, top-3=83%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 67 | ss1 | +0.2267 | 60.2% |
| 63 | ss1 | +0.0594 | 15.8% |
| 66 | ss1 | +0.0280 | 7.4% |
| 68 | ss1 | +0.0189 | 5.0% |
| 65 | ss1 | +0.0150 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 7 | 26.9% |
| -1 | 3 | 11.5% |
| +2 | 3 | 11.5% |
| +0 | 3 | 11.5% |
| -3 | 3 | 11.5% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=69%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 18 | 69.2% |
| ss2 | ss2 | 5 | 19.2% |
| other | ss1 | 2 | 7.7% |
| other | other | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 67 | ss1 | 64 | ss1 | +0.2041 | 0.2394 |
| 63 | ss1 | 64 | ss1 | +0.0520 | 0.2497 |
| 66 | ss1 | 64 | ss1 | +0.0269 | 0.2854 |
| 68 | ss1 | 64 | ss1 | +0.0189 | 0.2721 |
| 65 | ss1 | 64 | ss1 | +0.0150 | 0.2072 |

### L11 H0 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 27  |  total attr: +0.3567

**Key mass** (top-1=72%, top-2=84%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 67 | ss1 | +0.2578 | 72.3% |
| 64 | ss1 | +0.0432 | 12.1% |
| 65 | ss1 | +0.0248 | 7.0% |
| 66 | ss1 | +0.0086 | 2.4% |
| 63 | ss1 | +0.0059 | 1.7% |

**Query mass** (top-1=42%, top-2=63%, top-3=74%)  [DISTR(V63/A64/E65)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.1482 | 41.5% |
| 64 | ss1 | +0.0752 | 21.1% |
| 65 | ss1 | +0.0393 | 11.0% |
| 74 | other | +0.0390 | 10.9% |
| 66 | ss1 | +0.0278 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 4 | 14.8% |
| -1 | 4 | 14.8% |
| +0 | 3 | 11.1% |
| -4 | 2 | 7.4% |
| +7 | 2 | 7.4% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=59%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 16 | 59.3% |
| other | ss1 | 4 | 14.8% |
| ss1 | flkL | 3 | 11.1% |
| ss1 | other | 2 | 7.4% |
| flkR | ss2 | 2 | 7.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 67 | ss1 | +0.1286 | 0.3818 |
| 65 | ss1 | 67 | ss1 | +0.0393 | 0.4495 |
| 74 | other | 67 | ss1 | +0.0390 | 0.2997 |
| 64 | ss1 | 64 | ss1 | +0.0344 | 0.1193 |
| 66 | ss1 | 67 | ss1 | +0.0278 | 0.3452 |

### L11 H8 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.1699

**Key mass** (top-1=82%, top-2=93%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.1390 | 81.8% |
| -1 | other | +0.0193 | 11.4% |
| 67 | ss1 | +0.0105 | 6.2% |
| 64 | ss1 | +0.0011 | 0.7% |

**Query mass** (top-1=26%, top-2=43%, top-3=60%)  [DISTR(F61/G67/S66/L60)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0443 | 26.1% |
| 67 | ss1 | +0.0294 | 17.3% |
| 66 | ss1 | +0.0280 | 16.5% |
| 60 | ss1 | +0.0177 | 10.4% |
| 63 | ss1 | +0.0126 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 1 | 4.8% |
| -109 | 1 | 4.8% |
| -110 | 1 | 4.8% |
| -116 | 1 | 4.8% |
| +64 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 28.6% |
| ss1 | other | 4 | 19.0% |
| flkL | ss2 | 4 | 19.0% |
| other | ss1 | 2 | 9.5% |
| other | ss2 | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 61 | ss1 | 176 | ss2 | +0.0443 | 0.3636 |
| 67 | ss1 | 176 | ss2 | +0.0294 | 0.2324 |
| 66 | ss1 | 176 | ss2 | +0.0280 | 0.4593 |
| 60 | ss1 | 176 | ss2 | +0.0177 | 0.2166 |
| 63 | ss1 | -1 | other | +0.0126 | 0.1328 |

### L11 H9 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 35  |  total attr: +0.1244

**Key mass** (top-1=25%, top-2=44%, top-3=55%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0306 | 24.6% |
| 67 | ss1 | +0.0244 | 19.6% |
| 63 | ss1 | +0.0134 | 10.7% |
| 69 | other | +0.0080 | 6.4% |
| 176 | ss2 | +0.0071 | 5.7% |

**Query mass** (top-1=20%, top-2=34%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0243 | 19.5% |
| 63 | ss1 | +0.0186 | 14.9% |
| 64 | ss1 | +0.0149 | 12.0% |
| 58 | ss1 | +0.0097 | 7.8% |
| 67 | ss1 | +0.0096 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 11 | 31.4% |
| +0 | 10 | 28.6% |
| -5 | 4 | 11.4% |
| +1 | 2 | 5.7% |
| -9 | 2 | 5.7% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 13 | 37.1% |
| ss1 | other | 5 | 14.3% |
| other | other | 4 | 11.4% |
| flkL | flkL | 4 | 11.4% |
| flkL | ss1 | 3 | 8.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 62 | ss1 | 67 | ss1 | +0.0167 | 0.2097 |
| 63 | ss1 | 63 | ss1 | +0.0134 | 0.1879 |
| 58 | ss1 | 64 | ss1 | +0.0097 | 0.4038 |
| 64 | ss1 | 64 | ss1 | +0.0094 | 0.0706 |
| 71 | other | 71 | other | +0.0046 | 0.2107 |

### L12 H1 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1731

**Key mass** (top-1=90%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.1560 | 90.1% |
| 64 | ss1 | +0.0050 | 2.9% |
| 194 | flkR | +0.0034 | 2.0% |
| 73 | other | +0.0030 | 1.7% |
| 257 | other | +0.0029 | 1.7% |

**Query mass** (top-1=51%, top-2=65%, top-3=75%)  [DISTR(A64/G67/V63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0882 | 51.0% |
| 67 | ss1 | +0.0245 | 14.1% |
| 63 | ss1 | +0.0169 | 9.8% |
| 66 | ss1 | +0.0108 | 6.2% |
| 62 | ss1 | +0.0104 | 6.0% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 1 | 5.6% |
| -109 | 1 | 5.6% |
| -113 | 1 | 5.6% |
| -110 | 1 | 5.6% |
| -114 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 38.9% |
| ss1 | other | 4 | 22.2% |
| other | ss1 | 1 | 5.6% |
| other | ss2 | 1 | 5.6% |
| ss1 | ss1 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 176 | ss2 | +0.0856 | 0.3561 |
| 67 | ss1 | 176 | ss2 | +0.0245 | 0.3092 |
| 63 | ss1 | 176 | ss2 | +0.0169 | 0.0787 |
| 66 | ss1 | 176 | ss2 | +0.0108 | 0.1636 |
| 62 | ss1 | 176 | ss2 | +0.0088 | 0.0972 |

### L12 H3 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 30  |  total attr: +0.1689

**Key mass** (top-1=69%, top-2=78%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.1166 | 69.0% |
| 198 | flkR | +0.0153 | 9.1% |
| 67 | ss1 | +0.0126 | 7.5% |
| 179 | ss2 | +0.0121 | 7.1% |
| 63 | ss1 | +0.0040 | 2.4% |

**Query mass** (top-1=24%, top-2=44%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0408 | 24.1% |
| 66 | ss1 | +0.0333 | 19.7% |
| 62 | ss1 | +0.0155 | 9.2% |
| 67 | ss1 | +0.0135 | 8.0% |
| 65 | ss1 | +0.0106 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 3 | 10.0% |
| -24 | 3 | 10.0% |
| -6 | 2 | 6.7% |
| -118 | 2 | 6.7% |
| -110 | 1 | 3.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 12 | 40.0% |
| flkL | ss1 | 5 | 16.7% |
| ss1 | ss1 | 5 | 16.7% |
| ss2 | flkR | 3 | 10.0% |
| other | ss2 | 2 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 66 | ss1 | 176 | ss2 | +0.0333 | 0.3217 |
| 63 | ss1 | 176 | ss2 | +0.0302 | 0.2007 |
| 62 | ss1 | 176 | ss2 | +0.0155 | 0.4451 |
| 67 | ss1 | 176 | ss2 | +0.0135 | 0.3614 |
| 65 | ss1 | 176 | ss2 | +0.0106 | 0.3279 |

### L12 H9 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss1  |  cells: 40  |  total attr: +0.1725

**Key mass** (top-1=40%, top-2=55%, top-3=63%)  [DISTR(A64/G67/V62/F68/L60)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0693 | 40.2% |
| 67 | ss1 | +0.0248 | 14.4% |
| 62 | ss1 | +0.0152 | 8.8% |
| 68 | ss1 | +0.0087 | 5.0% |
| 60 | ss1 | +0.0074 | 4.3% |

**Query mass** (top-1=22%, top-2=36%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 67 | ss1 | +0.0382 | 22.1% |
| 66 | ss1 | +0.0240 | 13.9% |
| 61 | ss1 | +0.0201 | 11.7% |
| 176 | ss2 | +0.0181 | 10.5% |
| 64 | ss1 | +0.0122 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 6 | 15.0% |
| -1 | 5 | 12.5% |
| +4 | 4 | 10.0% |
| -4 | 4 | 10.0% |
| +3 | 3 | 7.5% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 18 | 45.0% |
| ss2 | ss2 | 6 | 15.0% |
| ss2 | flkR | 4 | 10.0% |
| other | ss1 | 3 | 7.5% |
| flkL | flkL | 3 | 7.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 67 | ss1 | 64 | ss1 | +0.0361 | 0.1583 |
| 66 | ss1 | 67 | ss1 | +0.0156 | 0.1201 |
| 64 | ss1 | 64 | ss1 | +0.0109 | 0.0698 |
| 68 | ss1 | 64 | ss1 | +0.0082 | 0.1877 |
| 65 | ss1 | 67 | ss1 | +0.0081 | 0.1371 |

### L12 H16 — Rank #29

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0849

**Key mass** (top-1=33%, top-2=53%, top-3=66%)  [DISTR(?257/W176/?-1/A64)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 257 | other | +0.0278 | 32.8% |
| 176 | ss2 | +0.0175 | 20.6% |
| -1 | other | +0.0105 | 12.4% |
| 64 | ss1 | +0.0076 | 9.0% |
| 256 | other | +0.0056 | 6.5% |

**Query mass** (top-1=28%, top-2=48%, top-3=63%)  [DISTR(W176/V63/A64/?-1)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0239 | 28.1% |
| 63 | ss1 | +0.0166 | 19.5% |
| 64 | ss1 | +0.0132 | 15.5% |
| -1 | other | +0.0099 | 11.7% |
| 66 | ss1 | +0.0064 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 12.5% |
| -81 | 1 | 4.2% |
| -177 | 1 | 4.2% |
| -194 | 1 | 4.2% |
| -192 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 7 | 29.2% |
| ss2 | other | 3 | 12.5% |
| ss1 | ss1 | 3 | 12.5% |
| ss2 | flkR | 3 | 12.5% |
| ss1 | ss2 | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 176 | ss2 | 257 | other | +0.0114 | 0.1137 |
| -1 | other | 176 | ss2 | +0.0089 | 0.0919 |
| 64 | ss1 | 64 | ss1 | +0.0076 | 0.0831 |
| 63 | ss1 | 257 | other | +0.0054 | 0.0840 |
| 65 | ss1 | 257 | other | +0.0049 | 0.1464 |

### L13 H1 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.1398

**Key mass** (top-1=79%, top-2=89%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.1099 | 78.6% |
| 63 | ss1 | +0.0152 | 10.9% |
| -1 | other | +0.0077 | 5.5% |
| 61 | ss1 | +0.0028 | 2.0% |
| 208 | flkR | +0.0018 | 1.3% |

**Query mass** (top-1=27%, top-2=41%, top-3=52%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 60 | ss1 | +0.0379 | 27.1% |
| 66 | ss1 | +0.0201 | 14.4% |
| 65 | ss1 | +0.0143 | 10.2% |
| -1 | other | +0.0132 | 9.5% |
| 162 | other | +0.0088 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 7.1% |
| -116 | 1 | 3.6% |
| -110 | 1 | 3.6% |
| -111 | 1 | 3.6% |
| -14 | 1 | 3.6% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 8 | 28.6% |
| ss1 | ss2 | 5 | 17.9% |
| ss1 | ss1 | 5 | 17.9% |
| flkL | ss2 | 4 | 14.3% |
| other | ss1 | 3 | 10.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 60 | ss1 | 176 | ss2 | +0.0379 | 0.2496 |
| 66 | ss1 | 176 | ss2 | +0.0201 | 0.1178 |
| 65 | ss1 | 176 | ss2 | +0.0117 | 0.2149 |
| 162 | other | 176 | ss2 | +0.0088 | 0.2943 |
| -1 | other | -1 | other | +0.0077 | 0.2205 |

### L13 H2 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss1  |  cells: 33  |  total attr: +0.1441

**Key mass** (top-1=43%, top-2=64%, top-3=76%)  [DISTR(A64/V63/L60)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0614 | 42.6% |
| 63 | ss1 | +0.0315 | 21.9% |
| 60 | ss1 | +0.0159 | 11.1% |
| -1 | other | +0.0079 | 5.5% |
| 69 | other | +0.0071 | 4.9% |

**Query mass** (top-1=37%, top-2=52%, top-3=61%)  [DISTR(S66/?-1/V63/F61)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 66 | ss1 | +0.0533 | 37.0% |
| -1 | other | +0.0221 | 15.3% |
| 63 | ss1 | +0.0131 | 9.1% |
| 61 | ss1 | +0.0126 | 8.8% |
| 65 | ss1 | +0.0099 | 6.9% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 5 | 15.2% |
| +0 | 3 | 9.1% |
| -3 | 3 | 9.1% |
| +2 | 2 | 6.1% |
| -1 | 2 | 6.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 14 | 42.4% |
| other | other | 8 | 24.2% |
| ss1 | other | 4 | 12.1% |
| flkL | ss1 | 4 | 12.1% |
| other | ss1 | 3 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 66 | ss1 | 64 | ss1 | +0.0378 | 0.2887 |
| -1 | other | -1 | other | +0.0079 | 0.2496 |
| 65 | ss1 | 63 | ss1 | +0.0077 | 0.1979 |
| 63 | ss1 | 64 | ss1 | +0.0075 | 0.1069 |
| 61 | ss1 | 60 | ss1 | +0.0068 | 0.3025 |

### L13 H3 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 44  |  total attr: +0.2319

**Key mass** (top-1=61%, top-2=69%, top-3=76%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 67 | ss1 | +0.1417 | 61.1% |
| 60 | ss1 | +0.0185 | 8.0% |
| 63 | ss1 | +0.0171 | 7.4% |
| 64 | ss1 | +0.0106 | 4.6% |
| 176 | ss2 | +0.0102 | 4.4% |

**Query mass** (top-1=36%, top-2=51%, top-3=64%)  [DISTR(V63/E65/A64/S66)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0827 | 35.7% |
| 65 | ss1 | +0.0350 | 15.1% |
| 64 | ss1 | +0.0298 | 12.9% |
| 66 | ss1 | +0.0275 | 11.9% |
| 61 | ss1 | +0.0124 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 5 | 11.4% |
| -3 | 4 | 9.1% |
| +3 | 4 | 9.1% |
| +5 | 4 | 9.1% |
| -1 | 3 | 6.8% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 23 | 52.3% |
| ss1 | flkL | 8 | 18.2% |
| ss2 | ss2 | 5 | 11.4% |
| other | ss1 | 4 | 9.1% |
| flkL | flkL | 2 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 67 | ss1 | +0.0724 | 0.3315 |
| 65 | ss1 | 67 | ss1 | +0.0254 | 0.7899 |
| 64 | ss1 | 67 | ss1 | +0.0236 | 0.4206 |
| 66 | ss1 | 67 | ss1 | +0.0203 | 0.5359 |
| 67 | ss1 | 64 | ss1 | +0.0082 | 0.1410 |

### L14 H9 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 16  |  total attr: +0.1616

**Key mass** (top-1=97%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.1563 | 96.8% |
| 179 | ss2 | +0.0018 | 1.1% |
| -1 | other | +0.0014 | 0.9% |
| 60 | ss1 | +0.0011 | 0.7% |
| 208 | flkR | +0.0010 | 0.6% |

**Query mass** (top-1=29%, top-2=46%, top-3=59%)  [DISTR(?-1/F61/S66/A64/V63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0461 | 28.6% |
| 61 | ss1 | +0.0277 | 17.2% |
| 66 | ss1 | +0.0218 | 13.5% |
| 64 | ss1 | +0.0128 | 7.9% |
| 63 | ss1 | +0.0119 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -177 | 1 | 6.2% |
| -115 | 1 | 6.2% |
| -110 | 1 | 6.2% |
| -112 | 1 | 6.2% |
| -113 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 50.0% |
| other | ss2 | 5 | 31.2% |
| other | other | 1 | 6.2% |
| ss1 | ss1 | 1 | 6.2% |
| ss2 | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 176 | ss2 | +0.0430 | 0.1420 |
| 61 | ss1 | 176 | ss2 | +0.0267 | 0.2248 |
| 66 | ss1 | 176 | ss2 | +0.0218 | 0.2130 |
| 64 | ss1 | 176 | ss2 | +0.0128 | 0.1388 |
| 63 | ss1 | 176 | ss2 | +0.0119 | 0.0495 |

### L14 H19 — Rank #25

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | INTRA:ss1  |  cells: 24  |  total attr: +0.1907

**Key mass** (top-1=34%, top-2=59%, top-3=73%)  [DISTR(S66/G67/G69)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 66 | ss1 | +0.0651 | 34.1% |
| 67 | ss1 | +0.0476 | 25.0% |
| 69 | other | +0.0270 | 14.2% |
| 65 | ss1 | +0.0151 | 7.9% |
| 68 | ss1 | +0.0129 | 6.8% |

**Query mass** (top-1=32%, top-2=59%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 61 | ss1 | +0.0616 | 32.3% |
| 64 | ss1 | +0.0517 | 27.1% |
| 63 | ss1 | +0.0427 | 22.4% |
| 60 | ss1 | +0.0159 | 8.3% |
| 62 | ss1 | +0.0095 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 3 | 12.5% |
| -3 | 2 | 8.3% |
| -2 | 2 | 8.3% |
| -6 | 2 | 8.3% |
| -8 | 2 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 14 | 58.3% |
| ss1 | other | 9 | 37.5% |
| other | other | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 66 | ss1 | +0.0327 | 0.2735 |
| 64 | ss1 | 66 | ss1 | +0.0288 | 0.2195 |
| 61 | ss1 | 67 | ss1 | +0.0267 | 0.0920 |
| 61 | ss1 | 69 | other | +0.0191 | 0.0903 |
| 64 | ss1 | 67 | ss1 | +0.0105 | 0.0588 |

### L16 H6 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0782

**Key mass** (top-1=75%, top-2=89%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 176 | ss2 | +0.0586 | 74.8% |
| 177 | ss2 | +0.0107 | 13.7% |
| 178 | ss2 | +0.0075 | 9.5% |
| 255 | other | +0.0015 | 1.9% |

**Query mass** (top-1=44%, top-2=69%, top-3=94%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0342 | 43.7% |
| 63 | ss1 | +0.0201 | 25.7% |
| 65 | ss1 | +0.0192 | 24.6% |
| 211 | flkR | +0.0021 | 2.7% |
| 173 | ss2 | +0.0015 | 1.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 2 | 25.0% |
| -113 | 2 | 25.0% |
| +35 | 1 | 12.5% |
| -82 | 1 | 12.5% |
| -108 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 75.0% |
| flkR | ss2 | 1 | 12.5% |
| ss2 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 176 | ss2 | +0.0342 | 0.3392 |
| 63 | ss1 | 176 | ss2 | +0.0201 | 0.2039 |
| 65 | ss1 | 177 | ss2 | +0.0107 | 0.2142 |
| 65 | ss1 | 178 | ss2 | +0.0075 | 0.1441 |
| 211 | flkR | 176 | ss2 | +0.0021 | 0.3427 |

### L17 H10 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 17  |  total attr: +0.1220

**Key mass** (top-1=69%, top-2=90%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 64 | ss1 | +0.0845 | 69.3% |
| 61 | ss1 | +0.0256 | 21.0% |
| 41 | flkL | +0.0049 | 4.0% |
| 62 | ss1 | +0.0039 | 3.2% |
| 60 | ss1 | +0.0019 | 1.5% |

**Query mass** (top-1=22%, top-2=42%, top-3=59%)  [DISTR(S66/E65/V62/A64)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 66 | ss1 | +0.0267 | 21.9% |
| 65 | ss1 | +0.0246 | 20.2% |
| 62 | ss1 | +0.0202 | 16.6% |
| 64 | ss1 | +0.0188 | 15.4% |
| 63 | ss1 | +0.0185 | 15.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 17.6% |
| -1 | 2 | 11.8% |
| +2 | 2 | 11.8% |
| -3 | 2 | 11.8% |
| +4 | 2 | 11.8% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=76%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 13 | 76.5% |
| flkL | flkL | 3 | 17.6% |
| other | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 65 | ss1 | 64 | ss1 | +0.0246 | 0.6181 |
| 62 | ss1 | 64 | ss1 | +0.0192 | 0.2901 |
| 63 | ss1 | 64 | ss1 | +0.0185 | 0.3586 |
| 66 | ss1 | 64 | ss1 | +0.0143 | 0.5499 |
| 64 | ss1 | 61 | ss1 | +0.0138 | 0.5050 |

### L17 H18 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 17  |  total attr: +0.0752

**Key mass** (top-1=32%, top-2=51%, top-3=60%)  [DISTR(E65/A64/F61/Y29/Y41)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 65 | ss1 | +0.0239 | 31.8% |
| 64 | ss1 | +0.0145 | 19.3% |
| 61 | ss1 | +0.0068 | 9.0% |
| 29 | flkL | +0.0053 | 7.0% |
| 41 | flkL | +0.0037 | 5.0% |

**Query mass** (top-1=32%, top-2=51%, top-3=64%)  [DISTR(F177/W176/F43/V62)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 177 | ss2 | +0.0240 | 32.0% |
| 176 | ss2 | +0.0145 | 19.3% |
| 43 | flkL | +0.0096 | 12.8% |
| 62 | ss1 | +0.0056 | 7.5% |
| 61 | ss1 | +0.0048 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +112 | 3 | 17.6% |
| +19 | 3 | 17.6% |
| +14 | 1 | 5.9% |
| -18 | 1 | 5.9% |
| -113 | 1 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 41.2% |
| ss1 | flkL | 5 | 29.4% |
| ss1 | ss2 | 2 | 11.8% |
| flkL | flkL | 1 | 5.9% |
| flkL | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 177 | ss2 | 65 | ss1 | +0.0227 | 0.6309 |
| 176 | ss2 | 64 | ss1 | +0.0145 | 0.5165 |
| 43 | flkL | 29 | flkL | +0.0053 | 0.1403 |
| 43 | flkL | 61 | ss1 | +0.0043 | 0.1007 |
| 61 | ss1 | 174 | ss2 | +0.0034 | 0.0524 |

### L18 H16 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 11  |  total attr: +0.0936

**Key mass** (top-1=89%, top-2=94%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 208 | flkR | +0.0833 | 89.0% |
| 179 | ss2 | +0.0051 | 5.4% |
| 181 | ss2 | +0.0038 | 4.1% |
| 180 | ss2 | +0.0014 | 1.5% |

**Query mass** (top-1=57%, top-2=81%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0533 | 56.9% |
| 64 | ss1 | +0.0227 | 24.3% |
| 65 | ss1 | +0.0040 | 4.3% |
| 66 | ss1 | +0.0040 | 4.2% |
| -1 | other | +0.0039 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -116 | 2 | 18.2% |
| -145 | 1 | 9.1% |
| -144 | 1 | 9.1% |
| -142 | 1 | 9.1% |
| -209 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 4 | 36.4% |
| ss1 | ss2 | 3 | 27.3% |
| ss2 | ss2 | 2 | 18.2% |
| other | flkR | 1 | 9.1% |
| flkL | flkR | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 208 | flkR | +0.0493 | 0.6950 |
| 64 | ss1 | 208 | flkR | +0.0227 | 0.4460 |
| 63 | ss1 | 179 | ss2 | +0.0040 | 0.0519 |
| 66 | ss1 | 208 | flkR | +0.0040 | 0.2818 |
| -1 | other | 208 | flkR | +0.0039 | 0.0942 |

### L22 H14 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 26  |  total attr: +0.1681

**Key mass** (top-1=34%, top-2=59%, top-3=66%)  [DISTR(A175/F177/V63/S66)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 175 | ss2 | +0.0577 | 34.3% |
| 177 | ss2 | +0.0408 | 24.3% |
| 63 | ss1 | +0.0123 | 7.3% |
| 66 | ss1 | +0.0101 | 6.0% |
| 178 | ss2 | +0.0088 | 5.2% |

**Query mass** (top-1=22%, top-2=44%, top-3=57%)  [DISTR(E65/V63/V62/F61/A175)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 65 | ss1 | +0.0373 | 22.2% |
| 63 | ss1 | +0.0372 | 22.1% |
| 62 | ss1 | +0.0205 | 12.2% |
| 61 | ss1 | +0.0180 | 10.7% |
| 175 | ss2 | +0.0121 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 6 | 23.1% |
| +112 | 3 | 11.5% |
| -113 | 2 | 7.7% |
| +114 | 2 | 7.7% |
| -114 | 1 | 3.8% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 12 | 46.2% |
| ss2 | ss1 | 6 | 23.1% |
| ss1 | flkL | 3 | 11.5% |
| ss1 | ss1 | 2 | 7.7% |
| ss1 | flkR | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 65 | ss1 | 177 | ss2 | +0.0373 | 0.3778 |
| 63 | ss1 | 175 | ss2 | +0.0372 | 0.4841 |
| 61 | ss1 | 175 | ss2 | +0.0126 | 0.1035 |
| 178 | ss2 | 66 | ss1 | +0.0101 | 0.2331 |
| 175 | ss2 | 63 | ss1 | +0.0101 | 0.2206 |

### L26 H16 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 16  |  total attr: +0.0746

**Key mass** (top-1=41%, top-2=62%, top-3=72%)  [DISTR(A175/F61/W176)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 175 | ss2 | +0.0302 | 40.5% |
| 61 | ss1 | +0.0159 | 21.3% |
| 176 | ss2 | +0.0079 | 10.6% |
| 177 | ss2 | +0.0078 | 10.4% |
| 65 | ss1 | +0.0034 | 4.5% |

**Query mass** (top-1=24%, top-2=42%, top-3=60%)  [DISTR(V63/V62/D174/A64)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | ss1 | +0.0181 | 24.3% |
| 62 | ss1 | +0.0135 | 18.1% |
| 174 | ss2 | +0.0130 | 17.4% |
| 64 | ss1 | +0.0125 | 16.7% |
| 61 | ss1 | +0.0036 | 4.8% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 4 | 25.0% |
| -113 | 2 | 12.5% |
| +114 | 2 | 12.5% |
| +113 | 1 | 6.2% |
| +112 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 43.8% |
| ss2 | ss1 | 4 | 25.0% |
| ss1 | ss1 | 2 | 12.5% |
| ss1 | flkR | 1 | 6.2% |
| flkL | ss1 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | ss1 | 175 | ss2 | +0.0167 | 0.2314 |
| 62 | ss1 | 175 | ss2 | +0.0135 | 0.1808 |
| 174 | ss2 | 61 | ss1 | +0.0110 | 0.2063 |
| 64 | ss1 | 176 | ss2 | +0.0079 | 0.1729 |
| 64 | ss1 | 177 | ss2 | +0.0045 | 0.0939 |

### L27 H15 — Rank #7

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 17  |  total attr: +0.1190

**Key mass** (top-1=41%, top-2=71%, top-3=78%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 175 | ss2 | +0.0493 | 41.4% |
| 64 | ss1 | +0.0351 | 29.5% |
| 63 | ss1 | +0.0089 | 7.5% |
| 40 | flkL | +0.0068 | 5.7% |
| 174 | ss2 | +0.0050 | 4.2% |

**Query mass** (top-1=26%, top-2=51%, top-3=63%)  [DISTR(V173/F61/V62/V63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0308 | 25.9% |
| 61 | ss1 | +0.0293 | 24.6% |
| 62 | ss1 | +0.0145 | 12.2% |
| 63 | ss1 | +0.0126 | 10.6% |
| 175 | ss2 | +0.0073 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 3 | 17.6% |
| +112 | 3 | 17.6% |
| -114 | 2 | 11.8% |
| -112 | 2 | 11.8% |
| +109 | 1 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 47.1% |
| ss2 | ss1 | 5 | 29.4% |
| ss1 | ss1 | 2 | 11.8% |
| ss1 | flkL | 1 | 5.9% |
| ss1 | flkR | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 173 | ss2 | 64 | ss1 | +0.0308 | 0.4403 |
| 61 | ss1 | 175 | ss2 | +0.0243 | 0.2675 |
| 63 | ss1 | 175 | ss2 | +0.0126 | 0.1661 |
| 62 | ss1 | 175 | ss2 | +0.0124 | 0.2271 |
| 175 | ss2 | 63 | ss1 | +0.0073 | 0.1200 |

### L28 H13 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 13  |  total attr: +0.0609

**Key mass** (top-1=65%, top-2=72%, top-3=79%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0394 | 64.7% |
| 61 | ss1 | +0.0047 | 7.7% |
| 65 | ss1 | +0.0038 | 6.2% |
| 175 | ss2 | +0.0030 | 4.9% |
| 180 | ss2 | +0.0028 | 4.5% |

**Query mass** (top-1=65%, top-2=77%, top-3=85%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0394 | 64.7% |
| 64 | ss1 | +0.0072 | 11.9% |
| 65 | ss1 | +0.0054 | 8.8% |
| 174 | ss2 | +0.0036 | 6.0% |
| 63 | ss1 | +0.0020 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 3 | 23.1% |
| -114 | 2 | 15.4% |
| -111 | 1 | 7.7% |
| +113 | 1 | 7.7% |
| +0 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 61.5% |
| ss1 | ss1 | 3 | 23.1% |
| ss2 | ss1 | 2 | 15.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 62 | ss1 | 173 | ss2 | +0.0394 | 0.5437 |
| 174 | ss2 | 61 | ss1 | +0.0036 | 0.1975 |
| 64 | ss1 | 176 | ss2 | +0.0026 | 0.1258 |
| 65 | ss1 | 65 | ss1 | +0.0021 | 0.0525 |
| 63 | ss1 | 175 | ss2 | +0.0020 | 0.0686 |

### L29 H18 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 20  |  total attr: +0.1009

**Key mass** (top-1=48%, top-2=56%, top-3=64%)  [DISTR(V173/A64/Q171/W176)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 173 | ss2 | +0.0483 | 47.9% |
| 64 | ss1 | +0.0085 | 8.4% |
| 171 | other | +0.0079 | 7.8% |
| 176 | ss2 | +0.0071 | 7.0% |
| 175 | ss2 | +0.0058 | 5.7% |

**Query mass** (top-1=30%, top-2=55%, top-3=67%)  [DISTR(V62/A64/V173/V63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0307 | 30.4% |
| 64 | ss1 | +0.0253 | 25.0% |
| 173 | ss2 | +0.0121 | 12.0% |
| 63 | ss1 | +0.0113 | 11.2% |
| 61 | ss1 | +0.0095 | 9.4% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -110 | 4 | 20.0% |
| -112 | 3 | 15.0% |
| -109 | 2 | 10.0% |
| -111 | 1 | 5.0% |
| +109 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 10 | 50.0% |
| ss1 | flkR | 4 | 20.0% |
| ss2 | ss1 | 2 | 10.0% |
| ss1 | other | 2 | 10.0% |
| flkL | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 64 | ss1 | 173 | ss2 | +0.0226 | 0.3138 |
| 62 | ss1 | 173 | ss2 | +0.0222 | 0.1733 |
| 173 | ss2 | 64 | ss1 | +0.0085 | 0.2199 |
| 62 | ss1 | 171 | other | +0.0056 | 0.0960 |
| 66 | ss1 | 178 | ss2 | +0.0046 | 0.1158 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #27 | L0 | H11 | 11 | +0.0256 | SINGLE-ANCHOR | A214 | DISTRIBUTED | D179/E65/D26/A64/A202 |  |  |
| #21 | L1 | H8 | 17 | +0.0888 | DISTRIBUTED | F181/A214/F68 | DISTRIBUTED | F177/A64/T210 | POSITIONAL | INTRA:flkR |
| #14 | L4 | H9 | 30 | +0.0478 | SINGLE-ANCHOR | D26 | DISTRIBUTED |  |  | INTRA:flkL |
| #4 | L6 | H7 | 14 | +0.1893 | SINGLE-ANCHOR | W176 | SINGLE-ANCHOR | A64 |  |  |
| #20 | L7 | H13 | 70 | +0.3134 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #28 | L9 | H8 | 17 | +0.0393 | DISTRIBUTED | D27/E65/D179/D26/E50 | DISTRIBUTED | A64/G67/N32 |  | ss1→flkL |
| #3 | L10 | H0 | 41 | +0.4357 | SINGLE-ANCHOR | A64 | DISTRIBUTED | G67/V63/S66/G69/F61 |  |  |
| #1 | L10 | H9 | 72 | +1.0980 | SINGLE-ANCHOR | A64 | DISTRIBUTED |  |  |  |
| #2 | L10 | H19 | 26 | +0.3763 | SINGLE-ANCHOR | A64 | SINGLE-ANCHOR | G67 |  | INTRA:ss1 |
| #6 | L11 | H0 | 27 | +0.3567 | SINGLE-ANCHOR | G67 | DISTRIBUTED | V63/A64/E65 |  | INTRA:ss1 |
| #16 | L11 | H8 | 21 | +0.1699 | SINGLE-ANCHOR | W176 | DISTRIBUTED | F61/G67/S66/L60 |  |  |
| #23 | L11 | H9 | 35 | +0.1244 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL |  |
| #11 | L12 | H1 | 18 | +0.1731 | SINGLE-ANCHOR | W176 | DISTRIBUTED | A64/G67/V63 |  |  |
| #26 | L12 | H3 | 30 | +0.1689 | SINGLE-ANCHOR | W176 | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #19 | L12 | H9 | 40 | +0.1725 | DISTRIBUTED | A64/G67/V62/F68/L60 | DISTRIBUTED |  |  | INTRA:ss1 |
| #29 | L12 | H16 | 24 | +0.0849 | DISTRIBUTED | ?257/W176/?-1/A64 | DISTRIBUTED | W176/V63/A64/?-1 |  |  |
| #8 | L13 | H1 | 28 | +0.1398 | SINGLE-ANCHOR | W176 | DISTRIBUTED |  |  |  |
| #12 | L13 | H2 | 33 | +0.1441 | DISTRIBUTED | A64/V63/L60 | DISTRIBUTED | S66/?-1/V63/F61 |  | INTRA:ss1 |
| #10 | L13 | H3 | 44 | +0.2319 | SINGLE-ANCHOR | G67 | DISTRIBUTED | V63/E65/A64/S66 |  | INTRA:ss1 |
| #9 | L14 | H9 | 16 | +0.1616 | SINGLE-ANCHOR | W176 | DISTRIBUTED | ?-1/F61/S66/A64/V63 |  | CROSS:ss1→ss2 |
| #25 | L14 | H19 | 24 | +0.1907 | DISTRIBUTED | S66/G67/G69 | MULTI-ANCHOR |  |  | INTRA:ss1 |
| #30 | L16 | H6 | 8 | +0.0782 | SINGLE-ANCHOR | W176 | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss1→ss2 |
| #18 | L17 | H10 | 17 | +0.1220 | SINGLE-ANCHOR | A64 | DISTRIBUTED | S66/E65/V62/A64 |  | INTRA:ss1 |
| #13 | L17 | H18 | 17 | +0.0752 | DISTRIBUTED | E65/A64/F61/Y29/Y41 | DISTRIBUTED | F177/W176/F43/V62 |  | CROSS:ss2→ss1 |
| #24 | L18 | H16 | 11 | +0.0936 | SINGLE-ANCHOR | L208 | DUAL-ANCHOR | V63/A64 |  |  |
| #5 | L22 | H14 | 26 | +0.1681 | DISTRIBUTED | A175/F177/V63/S66 | DISTRIBUTED | E65/V63/V62/F61/A175 |  | CROSS:ss1→ss2 |
| #17 | L26 | H16 | 16 | +0.0746 | DISTRIBUTED | A175/F61/W176 | DISTRIBUTED | V63/V62/D174/A64 |  | CROSS:ss1→ss2 |
| #7 | L27 | H15 | 17 | +0.1190 | DUAL-ANCHOR | A175/A64 | DISTRIBUTED | V173/F61/V62/V63 |  | CROSS:ss1→ss2 |
| #22 | L28 | H13 | 13 | +0.0609 | SINGLE-ANCHOR | V173 | SINGLE-ANCHOR | V62 |  | CROSS:ss1→ss2 |
| #15 | L29 | H18 | 20 | +0.1009 | DISTRIBUTED | V173/A64/Q171/W176 | DISTRIBUTED | V62/A64/V173/V63 |  | CROSS:ss1→ss2 |
