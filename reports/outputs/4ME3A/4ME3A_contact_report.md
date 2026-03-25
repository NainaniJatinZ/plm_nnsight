# Contact Pattern Analysis: 4ME3A

Generated: 2026-03-22 21:49:22   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4ME3A |
| Contact pair | (126, 238) |
| ss1 | [121, 132) |
| ss2 | [233, 244) |
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
| Clean metric | 1.0465 |
| Corrupt metric | 0.3700 |
| Gap | 0.6766 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 72.58% |
| positive IE | 75 | 72.32% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L32 | H18 | +0.3397 |
| 2 | L0 | H19 | +0.0918 |
| 3 | L9 | H14 | +0.0729 |
| 4 | L17 | H10 | +0.0607 |
| 5 | L10 | H9 | +0.0486 |
| 6 | L29 | H18 | +0.0424 |
| 7 | L17 | H18 | +0.0384 |
| 8 | L27 | H15 | +0.0376 |
| 9 | L32 | H13 | +0.0375 |
| 10 | L19 | H6 | +0.0303 |
| 11 | L14 | H4 | +0.0289 |
| 12 | L18 | H12 | +0.0289 |
| 13 | L31 | H17 | +0.0266 |
| 14 | L30 | H1 | +0.0261 |
| 15 | L13 | H7 | +0.0253 |
| 16 | L13 | H14 | +0.0234 |
| 17 | L24 | H18 | +0.0212 |
| 18 | L17 | H1 | +0.0204 |
| 19 | L24 | H3 | +0.0202 |
| 20 | L26 | H7 | +0.0200 |
| 21 | L18 | H4 | +0.0194 |
| 22 | L20 | H10 | +0.0190 |
| 23 | L21 | H6 | +0.0190 |
| 24 | L10 | H13 | +0.0190 |
| 25 | L17 | H3 | +0.0190 |
| 26 | L20 | H1 | +0.0187 |
| 27 | L11 | H1 | +0.0185 |
| 28 | L16 | H12 | +0.0175 |
| 29 | L22 | H3 | +0.0172 |
| 30 | L13 | H2 | +0.0169 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.20% |
| 2 | 0.91% |
| 3 | 0.83% |
| 4 | 0.53% |
| 5 | 0.89% |
| 6 | 3.50% |
| 7 | 3.51% |
| 8 | 7.69% |
| 9 | 10.41% |
| 10 | 18.81% |
| 20 | 26.81% |
| 80 | 85.24% |
| 450 | 119.99% |

## Cell Attribution Analysis

Total cells: 5,245,608

- Positive: 2,659,613
- Negative: 2,583,844

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000059 | 524,562 |
| 95th | +0.00000195 | 262,281 |
| 99th | +0.00001608 | 52,457 |
| 99.5th | +0.00003399 | 26,229 |
| 99.9th | +0.00016748 | 5,246 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L13 | H7 | 82 | flkL | 237 | ss2 | +0.064854 | 0.733923 |
| L32 | H18 | 236 | ss2 | 122 | ss1 | +0.057283 | 0.184948 |
| L9 | H14 | 75 | flkL | 230 | other | +0.051312 | 0.228561 |
| L29 | H18 | 236 | ss2 | 124 | ss1 | +0.045687 | 0.654087 |
| L32 | H18 | 122 | ss1 | 236 | ss2 | +0.043687 | 0.141052 |
| L20 | H10 | 122 | ss1 | 127 | ss1 | +0.032772 | 0.214753 |
| L32 | H18 | 238 | ss2 | 122 | ss1 | +0.031294 | 0.136233 |
| L18 | H3 | 110 | flkL | 110 | flkL | +0.030718 | 0.399163 |
| L19 | H6 | 127 | ss1 | 237 | ss2 | +0.030532 | 0.694207 |
| L29 | H18 | 122 | ss1 | 238 | ss2 | +0.027936 | 0.203615 |
| L31 | H17 | 122 | ss1 | 261 | flkR | +0.026701 | 0.284609 |
| L18 | H12 | 122 | ss1 | 127 | ss1 | +0.025868 | 0.210320 |
| L14 | H4 | 239 | ss2 | 127 | ss1 | +0.023472 | 0.188923 |
| L19 | H6 | 230 | other | 127 | ss1 | +0.022762 | 0.864043 |
| L14 | H12 | 117 | flkL | 127 | ss1 | +0.022094 | 0.621718 |
| L21 | H6 | 122 | ss1 | 127 | ss1 | +0.021608 | 0.376112 |
| L14 | H0 | 110 | flkL | 127 | ss1 | +0.021145 | 0.492380 |
| L18 | H4 | 122 | ss1 | 127 | ss1 | +0.020354 | 0.457801 |
| L9 | H14 | 230 | other | 75 | flkL | +0.019632 | 0.209696 |
| L27 | H15 | 125 | ss1 | 235 | ss2 | +0.018648 | 0.608154 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L14 | H12 | 110 | flkL | 127 | ss1 | -0.009046 | 0.557380 |
| L17 | H3 | 122 | ss1 | 237 | ss2 | -0.009118 | 0.085170 |
| L28 | H4 | 122 | ss1 | 124 | ss1 | -0.009294 | 0.076840 |
| L14 | H0 | 111 | flkL | 127 | ss1 | -0.009646 | 0.544501 |
| L15 | H6 | 260 | flkR | 237 | ss2 | -0.010176 | 0.411910 |
| L20 | H5 | 99 | flkL | 110 | flkL | -0.010292 | 0.502953 |
| L27 | H15 | 238 | ss2 | 259 | flkR | -0.011138 | 0.300829 |
| L18 | H4 | 120 | flkL | 127 | ss1 | -0.011746 | 0.618360 |
| L13 | H7 | 237 | ss2 | 127 | ss1 | -0.011872 | 0.395236 |
| L13 | H7 | 82 | flkL | 236 | ss2 | -0.011974 | 0.441850 |
| L17 | H9 | 238 | ss2 | 127 | ss1 | -0.012843 | 0.227301 |
| L13 | H7 | 122 | ss1 | 122 | ss1 | -0.012848 | 0.430663 |
| L13 | H14 | 239 | ss2 | 127 | ss1 | -0.012975 | 0.342764 |
| L10 | H9 | 127 | ss1 | 75 | flkL | -0.014871 | 0.188718 |
| L10 | H13 | 127 | ss1 | 75 | flkL | -0.016766 | 0.159262 |
| L14 | H12 | 114 | flkL | 127 | ss1 | -0.016938 | 0.548304 |
| L29 | H18 | 124 | ss1 | 236 | ss2 | -0.020650 | 0.767333 |
| L14 | H0 | 127 | ss1 | 127 | ss1 | -0.033266 | 0.539538 |
| L14 | H0 | 122 | ss1 | 127 | ss1 | -0.033884 | 0.487718 |
| L0 | H19 | 71 | flkL | 71 | flkL | -0.062193 | 0.985295 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.3700 | 0.00% |
| 10 | 10 | 7 | 0.3702 | 0.03% |
| 20 | 20 | 15 | 0.3714 | 0.21% |
| 50 | 50 | 26 | 0.3748 | 0.71% |
| 100 | 100 | 43 | 0.3823 | 1.83% |
| 200 | 200 | 64 | 0.3847 | 2.17% |
| 500 | 500 | 67 | 0.3882 | 2.70% |
| 1000 | 1,000 | 73 | 0.3911 | 3.13% |
| 2000 | 2,000 | 75 | 0.3950 | 3.71% |
| 5000 | 5,000 | 75 | 0.4070 | 5.47% |
| 10000 | 10,000 | 75 | 0.4161 | 6.82% |
| 20000 | 20,000 | 75 | 0.4301 | 8.88% |
| 50000 | 50,000 | 75 | 0.4556 | 12.66% |

## Motif Analysis

### L0 H19 — Rank #2

**Tags:** k:— / q:—  |  cells: 0  |  total attr: +0.0000

_No cells in top-1000_

### L9 H14 — Rank #3

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 18  |  total attr: +0.0955

**Key mass** (top-1=54%, top-2=74%, top-3=77%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 230 | other | +0.0513 | 53.7% |
| 75 | flkL | +0.0196 | 20.5% |
| 125 | ss1 | +0.0028 | 2.9% |
| 252 | flkR | +0.0024 | 2.5% |
| 246 | flkR | +0.0024 | 2.5% |

**Query mass** (top-1=54%, top-2=74%, top-3=79%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | flkL | +0.0513 | 53.7% |
| 230 | other | +0.0196 | 20.5% |
| 70 | other | +0.0044 | 4.6% |
| 125 | ss1 | +0.0028 | 2.9% |
| 233 | ss2 | +0.0024 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 4 | 22.2% |
| +155 | 2 | 11.1% |
| -155 | 1 | 5.6% |
| -182 | 1 | 5.6% |
| -184 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 4 | 22.2% |
| flkL | flkR | 3 | 16.7% |
| flkL | flkL | 3 | 16.7% |
| other | flkL | 2 | 11.1% |
| flkR | flkL | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | flkL | 230 | other | +0.0513 | 0.2286 |
| 230 | other | 75 | flkL | +0.0196 | 0.2097 |
| 125 | ss1 | 125 | ss1 | +0.0028 | 0.0473 |
| 70 | other | 252 | flkR | +0.0024 | 0.0778 |
| 233 | ss2 | 78 | flkL | +0.0024 | 0.1848 |

### L10 H9 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 19  |  total attr: +0.0665

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | flkL | +0.0665 | 100.0% |

**Query mass** (top-1=19%, top-2=37%, top-3=54%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0126 | 18.9% |
| 230 | other | +0.0120 | 18.0% |
| 237 | ss2 | +0.0115 | 17.2% |
| 125 | ss1 | +0.0049 | 7.3% |
| 122 | ss1 | +0.0041 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -76 | 1 | 5.3% |
| +155 | 1 | 5.3% |
| +162 | 1 | 5.3% |
| +50 | 1 | 5.3% |
| +47 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 31.6% |
| flkL | flkL | 5 | 26.3% |
| ss2 | flkL | 4 | 21.1% |
| other | flkL | 3 | 15.8% |
| flkR | flkL | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 75 | flkL | +0.0126 | 0.3586 |
| 230 | other | 75 | flkL | +0.0120 | 0.3498 |
| 237 | ss2 | 75 | flkL | +0.0115 | 0.3482 |
| 125 | ss1 | 75 | flkL | +0.0049 | 0.2251 |
| 122 | ss1 | 75 | flkL | +0.0041 | 0.1803 |

### L10 H13 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 11  |  total attr: +0.0500

**Key mass** (top-1=96%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | flkL | +0.0482 | 96.4% |
| 230 | other | +0.0018 | 3.6% |

**Query mass** (top-1=35%, top-2=57%, top-3=73%)  [DISTR(V125/L122/V129)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 125 | ss1 | +0.0173 | 34.5% |
| 122 | ss1 | +0.0111 | 22.2% |
| 129 | ss1 | +0.0082 | 16.3% |
| 126 | ss1 | +0.0028 | 5.6% |
| 133 | other | +0.0023 | 4.5% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +38 | 2 | 18.2% |
| +50 | 1 | 9.1% |
| +47 | 1 | 9.1% |
| +54 | 1 | 9.1% |
| +51 | 1 | 9.1% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 5 | 45.5% |
| flkL | flkL | 4 | 36.4% |
| other | flkL | 1 | 9.1% |
| flkR | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 125 | ss1 | 75 | flkL | +0.0173 | 0.3558 |
| 122 | ss1 | 75 | flkL | +0.0111 | 0.1709 |
| 129 | ss1 | 75 | flkL | +0.0082 | 0.1195 |
| 126 | ss1 | 75 | flkL | +0.0028 | 0.1218 |
| 133 | other | 75 | flkL | +0.0023 | 0.1816 |

### L11 H1 — Rank #27

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | POSITIONAL  |  cells: 8  |  total attr: +0.0182

**Key mass** (top-1=51%, top-2=70%, top-3=80%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0093 | 50.8% |
| 82 | flkL | +0.0034 | 18.9% |
| 120 | flkL | +0.0019 | 10.4% |
| 80 | flkL | +0.0009 | 5.2% |
| 84 | flkL | +0.0009 | 5.1% |

**Query mass** (top-1=46%, top-2=65%, top-3=75%)  [DISTR(G127/G237/G120)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0084 | 46.0% |
| 237 | ss2 | +0.0034 | 18.9% |
| 120 | flkL | +0.0019 | 10.4% |
| 235 | ss2 | +0.0009 | 5.2% |
| 84 | flkL | +0.0009 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 4 | 50.0% |
| +155 | 2 | 25.0% |
| -154 | 1 | 12.5% |
| -1 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 2 | 25.0% |
| ss2 | flkL | 2 | 25.0% |
| flkL | flkL | 2 | 25.0% |
| flkL | ss2 | 1 | 12.5% |
| ss2 | ss2 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 127 | ss1 | +0.0084 | 0.0515 |
| 237 | ss2 | 82 | flkL | +0.0034 | 0.0430 |
| 120 | flkL | 120 | flkL | +0.0019 | 0.0497 |
| 235 | ss2 | 80 | flkL | +0.0009 | 0.0390 |
| 84 | flkL | 84 | flkL | +0.0009 | 0.0380 |

### L13 H2 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 12  |  total attr: +0.0378

**Key mass** (top-1=79%, top-2=93%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0299 | 79.0% |
| 237 | ss2 | +0.0052 | 13.8% |
| 230 | other | +0.0014 | 3.8% |
| 128 | ss1 | +0.0013 | 3.4% |

**Query mass** (top-1=30%, top-2=48%, top-3=59%)  [DISTR(L122/G120/I123/V235/G127)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0115 | 30.4% |
| 120 | flkL | +0.0068 | 18.0% |
| 123 | ss1 | +0.0042 | 11.1% |
| 235 | ss2 | +0.0032 | 8.5% |
| 127 | ss1 | +0.0024 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 16.7% |
| -5 | 1 | 8.3% |
| -7 | 1 | 8.3% |
| -4 | 1 | 8.3% |
| -2 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 50.0% |
| flkL | ss1 | 3 | 25.0% |
| ss2 | ss2 | 2 | 16.7% |
| ss2 | other | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 127 | ss1 | +0.0115 | 0.3796 |
| 120 | flkL | 127 | ss1 | +0.0068 | 0.1906 |
| 123 | ss1 | 127 | ss1 | +0.0042 | 0.4147 |
| 235 | ss2 | 237 | ss2 | +0.0032 | 0.1813 |
| 128 | ss1 | 127 | ss1 | +0.0022 | 0.2474 |

### L13 H7 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.1311

**Key mass** (top-1=56%, top-2=65%, top-3=70%)  [DISTR(G237/G127/I119/G120)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0737 | 56.2% |
| 127 | ss1 | +0.0108 | 8.3% |
| 119 | flkL | +0.0072 | 5.5% |
| 120 | flkL | +0.0048 | 3.6% |
| 235 | ss2 | +0.0041 | 3.1% |

**Query mass** (top-1=49%, top-2=58%, top-3=65%)  [DISTR(D82/I249/?-1/G237)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 82 | flkL | +0.0649 | 49.5% |
| 249 | flkR | +0.0113 | 8.6% |
| -1 | other | +0.0092 | 7.1% |
| 237 | ss2 | +0.0089 | 6.8% |
| 122 | ss1 | +0.0048 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 8 | 30.8% |
| +155 | 3 | 11.5% |
| +130 | 2 | 7.7% |
| +110 | 2 | 7.7% |
| -155 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=15%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 4 | 15.4% |
| ss2 | ss2 | 3 | 11.5% |
| flkL | flkL | 3 | 11.5% |
| ss1 | ss2 | 2 | 7.7% |
| ss1 | other | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 82 | flkL | 237 | ss2 | +0.0649 | 0.7339 |
| -1 | other | 127 | ss1 | +0.0092 | 0.2973 |
| 237 | ss2 | 237 | ss2 | +0.0089 | 0.4014 |
| 249 | flkR | 119 | flkL | +0.0072 | 0.4818 |
| 120 | flkL | 120 | flkL | +0.0048 | 0.2204 |

### L13 H14 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.0450

**Key mass** (top-1=66%, top-2=81%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0299 | 66.5% |
| 75 | flkL | +0.0067 | 14.9% |
| 230 | other | +0.0051 | 11.3% |
| -1 | other | +0.0033 | 7.3% |

**Query mass** (top-1=18%, top-2=36%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 230 | other | +0.0082 | 18.3% |
| 233 | ss2 | +0.0081 | 17.9% |
| 238 | ss2 | +0.0050 | 11.2% |
| 237 | ss2 | +0.0030 | 6.6% |
| 97 | flkL | +0.0029 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +103 | 1 | 5.9% |
| +106 | 1 | 5.9% |
| +111 | 1 | 5.9% |
| +22 | 1 | 5.9% |
| +24 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 29.4% |
| other | ss1 | 3 | 17.6% |
| flkL | flkL | 3 | 17.6% |
| flkR | other | 3 | 17.6% |
| flkL | other | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 230 | other | 127 | ss1 | +0.0082 | 0.5238 |
| 233 | ss2 | 127 | ss1 | +0.0081 | 0.5735 |
| 238 | ss2 | 127 | ss1 | +0.0050 | 0.2967 |
| 97 | flkL | 75 | flkL | +0.0029 | 0.2292 |
| 99 | flkL | 75 | flkL | +0.0026 | 0.2141 |

### L14 H4 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | CROSS:ss2→ss1  |  cells: 14  |  total attr: +0.0510

**Key mass** (top-1=72%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0369 | 72.3% |
| -1 | other | +0.0103 | 20.2% |
| 129 | ss1 | +0.0038 | 7.4% |

**Query mass** (top-1=55%, top-2=70%, top-3=80%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | ss2 | +0.0279 | 54.7% |
| 238 | ss2 | +0.0077 | 15.1% |
| 237 | ss2 | +0.0054 | 10.6% |
| 97 | flkL | +0.0032 | 6.3% |
| 247 | flkR | +0.0017 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 2 | 14.3% |
| +109 | 2 | 14.3% |
| +112 | 1 | 7.1% |
| +111 | 1 | 7.1% |
| +98 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 50.0% |
| flkL | other | 2 | 14.3% |
| ss2 | other | 2 | 14.3% |
| flkR | other | 2 | 14.3% |
| flkR | ss1 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 239 | ss2 | 127 | ss1 | +0.0235 | 0.1889 |
| 237 | ss2 | 127 | ss1 | +0.0054 | 0.1607 |
| 238 | ss2 | 127 | ss1 | +0.0039 | 0.1305 |
| 97 | flkL | -1 | other | +0.0032 | 0.2303 |
| 239 | ss2 | -1 | other | +0.0028 | 0.0325 |

### L16 H12 — Rank #28

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 17  |  total attr: +0.0487

**Key mass** (top-1=40%, top-2=50%, top-3=57%)  [DISTR(G237/G127/N231/T121/D236)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0196 | 40.3% |
| 127 | ss1 | +0.0049 | 10.0% |
| 231 | other | +0.0034 | 7.1% |
| 121 | ss1 | +0.0033 | 6.7% |
| 236 | ss2 | +0.0029 | 5.9% |

**Query mass** (top-1=25%, top-2=48%, top-3=63%)  [DISTR(L239/I238/I123/V233)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | ss2 | +0.0121 | 24.8% |
| 238 | ss2 | +0.0113 | 23.2% |
| 123 | ss1 | +0.0074 | 15.1% |
| 233 | ss2 | +0.0034 | 7.1% |
| 129 | ss1 | +0.0034 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 82%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 11 | 64.7% |
| +1 | 3 | 17.6% |
| +3 | 1 | 5.9% |
| +0 | 1 | 5.9% |
| -1 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 35.3% |
| ss1 | ss1 | 4 | 23.5% |
| ss1 | flkL | 2 | 11.8% |
| flkL | flkL | 2 | 11.8% |
| flkR | flkR | 2 | 11.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 239 | ss2 | 237 | ss2 | +0.0103 | 0.3160 |
| 238 | ss2 | 237 | ss2 | +0.0085 | 0.0977 |
| 233 | ss2 | 231 | other | +0.0034 | 0.5619 |
| 129 | ss1 | 127 | ss1 | +0.0034 | 0.1838 |
| 123 | ss1 | 121 | ss1 | +0.0033 | 0.3166 |

### L17 H1 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 32  |  total attr: +0.0510

**Key mass** (top-1=16%, top-2=30%, top-3=41%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 260 | flkR | +0.0082 | 16.1% |
| 261 | flkR | +0.0073 | 14.3% |
| 123 | ss1 | +0.0057 | 11.1% |
| 263 | flkR | +0.0051 | 10.0% |
| 233 | ss2 | +0.0044 | 8.6% |

**Query mass** (top-1=25%, top-2=40%, top-3=52%)  [DISTR(L122/I238/R110/G230/G127)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0127 | 24.9% |
| 238 | ss2 | +0.0077 | 15.0% |
| 110 | flkL | +0.0063 | 12.4% |
| 230 | other | +0.0057 | 11.1% |
| 127 | ss1 | +0.0041 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 3 | 9.4% |
| -24 | 3 | 9.4% |
| -22 | 2 | 6.2% |
| -25 | 2 | 6.2% |
| -28 | 2 | 6.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 12 | 37.5% |
| ss1 | ss1 | 5 | 15.6% |
| ss1 | ss2 | 4 | 12.5% |
| other | flkR | 3 | 9.4% |
| flkR | flkR | 3 | 9.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 261 | flkR | +0.0041 | 0.2053 |
| 122 | ss1 | 123 | ss1 | +0.0031 | 0.0346 |
| 238 | ss2 | 260 | flkR | +0.0030 | 0.1556 |
| 122 | ss1 | 233 | ss2 | +0.0027 | 0.0317 |
| 110 | flkL | 111 | flkL | +0.0022 | 0.0684 |

### L17 H3 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0268

**Key mass** (top-1=40%, top-2=57%, top-3=74%)  [DISTR(?-1/?268/G127)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0108 | 40.1% |
| 268 | flkR | +0.0047 | 17.3% |
| 127 | ss1 | +0.0045 | 16.7% |
| 237 | ss2 | +0.0027 | 10.1% |
| 260 | flkR | +0.0017 | 6.2% |

**Query mass** (top-1=21%, top-2=38%, top-3=54%)  [DISTR(R110/L239/D236/I238/T256)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 110 | flkL | +0.0056 | 20.7% |
| 239 | ss2 | +0.0047 | 17.3% |
| 236 | ss2 | +0.0044 | 16.2% |
| 238 | ss2 | +0.0034 | 12.7% |
| 256 | flkR | +0.0018 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -29 | 1 | 7.7% |
| -17 | 1 | 7.7% |
| +237 | 1 | 7.7% |
| +239 | 1 | 7.7% |
| +257 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 3 | 23.1% |
| ss2 | other | 2 | 15.4% |
| flkR | other | 2 | 15.4% |
| flkL | ss1 | 1 | 7.7% |
| flkL | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 239 | ss2 | 268 | flkR | +0.0047 | 0.1703 |
| 110 | flkL | 127 | ss1 | +0.0045 | 0.1293 |
| 236 | ss2 | -1 | other | +0.0035 | 0.2154 |
| 238 | ss2 | -1 | other | +0.0034 | 0.1560 |
| 256 | flkR | -1 | other | +0.0018 | 0.1713 |

### L17 H10 — Rank #4

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.1013

**Key mass** (top-1=51%, top-2=75%, top-3=80%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0516 | 51.0% |
| 127 | ss1 | +0.0244 | 24.1% |
| 238 | ss2 | +0.0047 | 4.6% |
| 240 | ss2 | +0.0037 | 3.7% |
| 114 | flkL | +0.0025 | 2.5% |

**Query mass** (top-1=24%, top-2=42%, top-3=58%)  [DISTR(L239/D236/L122/I238)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | ss2 | +0.0246 | 24.3% |
| 236 | ss2 | +0.0180 | 17.8% |
| 122 | ss1 | +0.0158 | 15.6% |
| 238 | ss2 | +0.0146 | 14.5% |
| 125 | ss1 | +0.0064 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 5 | 18.5% |
| -2 | 4 | 14.8% |
| +0 | 4 | 14.8% |
| +2 | 3 | 11.1% |
| +1 | 3 | 11.1% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 10 | 37.0% |
| ss1 | ss1 | 7 | 25.9% |
| flkL | flkL | 5 | 18.5% |
| flkR | flkR | 4 | 14.8% |
| flkL | ss1 | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 236 | ss2 | 237 | ss2 | +0.0180 | 0.4792 |
| 239 | ss2 | 237 | ss2 | +0.0173 | 0.5267 |
| 238 | ss2 | 237 | ss2 | +0.0127 | 0.4747 |
| 122 | ss1 | 127 | ss1 | +0.0114 | 0.2047 |
| 125 | ss1 | 127 | ss1 | +0.0064 | 0.3049 |

### L17 H18 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 35  |  total attr: +0.1063

**Key mass** (top-1=24%, top-2=46%, top-3=60%)  [DISTR(L239/?-1/V78/L84)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | ss2 | +0.0260 | 24.4% |
| -1 | other | +0.0234 | 22.0% |
| 78 | flkL | +0.0148 | 13.9% |
| 84 | flkL | +0.0107 | 10.0% |
| 80 | flkL | +0.0053 | 5.0% |

**Query mass** (top-1=16%, top-2=32%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0173 | 16.3% |
| 239 | ss2 | +0.0163 | 15.4% |
| 123 | ss1 | +0.0158 | 14.9% |
| 129 | ss1 | +0.0109 | 10.2% |
| 125 | ss1 | +0.0053 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -110 | 6 | 17.1% |
| +45 | 3 | 8.6% |
| +155 | 1 | 2.9% |
| +44 | 1 | 2.9% |
| -116 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 22.9% |
| flkL | other | 7 | 20.0% |
| ss1 | flkL | 5 | 14.3% |
| flkR | other | 2 | 5.7% |
| ss2 | other | 2 | 5.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | ss1 | 239 | ss2 | +0.0109 | 0.7216 |
| 239 | ss2 | 84 | flkL | +0.0107 | 0.1998 |
| 122 | ss1 | 78 | flkL | +0.0098 | 0.1904 |
| 123 | ss1 | 239 | ss2 | +0.0093 | 0.1805 |
| 125 | ss1 | 80 | flkL | +0.0053 | 0.4384 |

### L18 H4 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 8  |  total attr: +0.0417

**Key mass** (top-1=57%, top-2=90%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0236 | 56.7% |
| 237 | ss2 | +0.0141 | 33.8% |
| 260 | flkR | +0.0012 | 3.0% |
| 261 | flkR | +0.0009 | 2.2% |
| 259 | flkR | +0.0009 | 2.2% |

**Query mass** (top-1=49%, top-2=83%, top-3=90%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0204 | 48.9% |
| 237 | ss2 | +0.0141 | 33.8% |
| 238 | ss2 | +0.0031 | 7.5% |
| 123 | ss1 | +0.0022 | 5.3% |
| 119 | flkL | +0.0010 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 2 | 25.0% |
| -5 | 1 | 12.5% |
| +0 | 1 | 12.5% |
| -22 | 1 | 12.5% |
| -8 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 3 | 37.5% |
| ss1 | ss1 | 2 | 25.0% |
| ss2 | ss2 | 2 | 25.0% |
| flkL | ss1 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 127 | ss1 | +0.0204 | 0.4578 |
| 237 | ss2 | 237 | ss2 | +0.0141 | 0.6899 |
| 123 | ss1 | 127 | ss1 | +0.0022 | 0.2873 |
| 238 | ss2 | 260 | flkR | +0.0012 | 0.0322 |
| 119 | flkL | 127 | ss1 | +0.0010 | 0.4710 |

### L18 H12 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.0625

**Key mass** (top-1=49%, top-2=68%, top-3=78%)  [DISTR(G127/G230/G120)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0304 | 48.6% |
| 230 | other | +0.0122 | 19.5% |
| 120 | flkL | +0.0064 | 10.2% |
| 267 | flkR | +0.0027 | 4.3% |
| 268 | flkR | +0.0022 | 3.6% |

**Query mass** (top-1=52%, top-2=59%, top-3=63%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0322 | 51.6% |
| 233 | ss2 | +0.0047 | 7.4% |
| 268 | flkR | +0.0022 | 3.6% |
| 237 | ss2 | +0.0021 | 3.4% |
| 234 | ss2 | +0.0021 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 3 | 13.6% |
| +0 | 2 | 9.1% |
| -7 | 2 | 9.1% |
| -4 | 2 | 9.1% |
| +2 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=18%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 4 | 18.2% |
| flkR | flkR | 4 | 18.2% |
| flkL | ss1 | 3 | 13.6% |
| ss1 | ss1 | 2 | 9.1% |
| other | other | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 127 | ss1 | +0.0259 | 0.2103 |
| 122 | ss1 | 120 | flkL | +0.0064 | 0.0529 |
| 233 | ss2 | 230 | other | +0.0047 | 0.5988 |
| 268 | flkR | 268 | flkR | +0.0022 | 0.3313 |
| 234 | ss2 | 230 | other | +0.0021 | 0.4046 |

### L19 H6 — Rank #10

**Tags:** k:DUAL-ANCHOR / q:MULTI-ANCHOR  |  cells: 11  |  total attr: +0.0816

**Key mass** (top-1=49%, top-2=94%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0399 | 48.9% |
| 237 | ss2 | +0.0364 | 44.7% |
| 120 | flkL | +0.0018 | 2.2% |
| 263 | flkR | +0.0014 | 1.7% |
| 112 | flkL | +0.0011 | 1.4% |

**Query mass** (top-1=37%, top-2=65%, top-3=84%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0305 | 37.4% |
| 230 | other | +0.0228 | 27.9% |
| 237 | ss2 | +0.0153 | 18.7% |
| 120 | flkL | +0.0066 | 8.1% |
| 236 | ss2 | +0.0023 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -23 | 2 | 18.2% |
| -110 | 1 | 9.1% |
| +103 | 1 | 9.1% |
| +110 | 1 | 9.1% |
| -117 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=18%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 18.2% |
| ss2 | flkR | 2 | 18.2% |
| ss1 | ss2 | 1 | 9.1% |
| other | ss1 | 1 | 9.1% |
| flkL | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 237 | ss2 | +0.0305 | 0.6942 |
| 230 | other | 127 | ss1 | +0.0228 | 0.8640 |
| 237 | ss2 | 127 | ss1 | +0.0142 | 0.3231 |
| 120 | flkL | 237 | ss2 | +0.0048 | 0.1105 |
| 120 | flkL | 127 | ss1 | +0.0019 | 0.0534 |

### L20 H1 — Rank #26

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 12  |  total attr: +0.0285

**Key mass** (top-1=39%, top-2=57%, top-3=72%)  [DISTR(I114/R110/G127)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | flkL | +0.0112 | 39.3% |
| 110 | flkL | +0.0050 | 17.4% |
| 127 | ss1 | +0.0043 | 15.0% |
| 237 | ss2 | +0.0028 | 9.7% |
| 240 | ss2 | +0.0022 | 7.8% |

**Query mass** (top-1=26%, top-2=48%, top-3=60%)  [DISTR(G127/I114/L239/L122/A260)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0075 | 26.3% |
| 114 | flkL | +0.0061 | 21.2% |
| 239 | ss2 | +0.0037 | 12.8% |
| 122 | ss1 | +0.0025 | 8.9% |
| 260 | flkR | +0.0022 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 25.0% |
| +17 | 1 | 8.3% |
| +2 | 1 | 8.3% |
| +8 | 1 | 8.3% |
| +13 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 4 | 33.3% |
| ss1 | flkL | 3 | 25.0% |
| ss2 | ss2 | 3 | 25.0% |
| ss1 | ss1 | 1 | 8.3% |
| flkR | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 114 | flkL | 114 | flkL | +0.0061 | 0.1586 |
| 127 | ss1 | 127 | ss1 | +0.0043 | 0.2332 |
| 127 | ss1 | 110 | flkL | +0.0032 | 0.1886 |
| 239 | ss2 | 237 | ss2 | +0.0028 | 0.0605 |
| 122 | ss1 | 114 | flkL | +0.0025 | 0.0538 |

### L20 H10 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 6  |  total attr: +0.0420

**Key mass** (top-1=78%, top-2=86%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0328 | 78.0% |
| 121 | ss1 | +0.0033 | 8.0% |
| 238 | ss2 | +0.0026 | 6.3% |
| 114 | flkL | +0.0015 | 3.6% |
| 235 | ss2 | +0.0009 | 2.2% |

**Query mass** (top-1=92%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0385 | 91.5% |
| 238 | ss2 | +0.0026 | 6.3% |
| 236 | ss2 | +0.0009 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 33.3% |
| +0 | 2 | 33.3% |
| -5 | 1 | 16.7% |
| +8 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 50.0% |
| ss2 | ss2 | 2 | 33.3% |
| ss1 | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 127 | ss1 | +0.0328 | 0.2148 |
| 122 | ss1 | 121 | ss1 | +0.0033 | 0.1640 |
| 238 | ss2 | 238 | ss2 | +0.0026 | 0.0869 |
| 122 | ss1 | 114 | flkL | +0.0015 | 0.0136 |
| 236 | ss2 | 235 | ss2 | +0.0009 | 0.0791 |

### L21 H6 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:flkR  |  cells: 15  |  total attr: +0.0503

**Key mass** (top-1=46%, top-2=69%, top-3=79%)  [DISTR(G127/A260/G230)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0232 | 46.1% |
| 260 | flkR | +0.0116 | 23.1% |
| 230 | other | +0.0049 | 9.7% |
| 237 | ss2 | +0.0047 | 9.3% |
| 123 | ss1 | +0.0027 | 5.3% |

**Query mass** (top-1=48%, top-2=58%, top-3=68%)  [DISTR(L122/A260/D236/Y259)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0243 | 48.3% |
| 260 | flkR | +0.0050 | 9.9% |
| 236 | ss2 | +0.0049 | 9.7% |
| 259 | flkR | +0.0024 | 4.8% |
| 255 | flkR | +0.0023 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -5 | 3 | 20.0% |
| +0 | 2 | 13.3% |
| +6 | 2 | 13.3% |
| -1 | 2 | 13.3% |
| +7 | 2 | 13.3% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 6 | 40.0% |
| ss1 | ss1 | 2 | 13.3% |
| other | ss2 | 2 | 13.3% |
| ss2 | ss2 | 2 | 13.3% |
| ss2 | other | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 127 | ss1 | +0.0216 | 0.3761 |
| 260 | flkR | 260 | flkR | +0.0050 | 0.5658 |
| 236 | ss2 | 230 | other | +0.0049 | 0.1838 |
| 122 | ss1 | 123 | ss1 | +0.0027 | 0.0892 |
| 255 | flkR | 260 | flkR | +0.0023 | 0.6249 |

### L22 H3 — Rank #29

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 10  |  total attr: +0.0210

**Key mass** (top-1=28%, top-2=46%, top-3=58%)  [DISTR(S116/I123/R130/R110/R115)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 116 | flkL | +0.0058 | 27.9% |
| 123 | ss1 | +0.0038 | 18.0% |
| 130 | ss1 | +0.0024 | 11.7% |
| 110 | flkL | +0.0023 | 11.2% |
| 115 | flkL | +0.0019 | 9.0% |

**Query mass** (top-1=79%, top-2=88%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0165 | 78.6% |
| 120 | flkL | +0.0019 | 9.0% |
| 127 | ss1 | +0.0017 | 8.0% |
| 237 | ss2 | +0.0009 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 2 | 20.0% |
| +4 | 2 | 20.0% |
| +6 | 1 | 10.0% |
| -8 | 1 | 10.0% |
| +12 | 1 | 10.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 40.0% |
| ss1 | ss1 | 4 | 40.0% |
| flkL | flkL | 1 | 10.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 116 | flkL | +0.0058 | 0.1107 |
| 122 | ss1 | 130 | ss1 | +0.0024 | 0.0724 |
| 122 | ss1 | 110 | flkL | +0.0023 | 0.0305 |
| 122 | ss1 | 123 | ss1 | +0.0021 | 0.0420 |
| 120 | flkL | 115 | flkL | +0.0019 | 0.1352 |

### L24 H3 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 14  |  total attr: +0.0422

**Key mass** (top-1=42%, top-2=77%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 260 | flkR | +0.0179 | 42.3% |
| 237 | ss2 | +0.0148 | 35.0% |
| 127 | ss1 | +0.0031 | 7.3% |
| 268 | flkR | +0.0018 | 4.3% |
| 120 | flkL | +0.0016 | 3.9% |

**Query mass** (top-1=39%, top-2=60%, top-3=68%)  [DISTR(L239/A260/L122/Y257)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | ss2 | +0.0166 | 39.4% |
| 260 | flkR | +0.0085 | 20.2% |
| 122 | ss1 | +0.0037 | 8.7% |
| 257 | flkR | +0.0031 | 7.2% |
| 256 | flkR | +0.0028 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 2 | 14.3% |
| -1 | 2 | 14.3% |
| +0 | 1 | 7.1% |
| -3 | 1 | 7.1% |
| -4 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 6 | 42.9% |
| flkL | ss1 | 3 | 21.4% |
| ss1 | ss1 | 2 | 14.3% |
| ss2 | ss2 | 1 | 7.1% |
| ss2 | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 239 | ss2 | 237 | ss2 | +0.0148 | 0.4661 |
| 260 | flkR | 260 | flkR | +0.0085 | 0.6805 |
| 257 | flkR | 260 | flkR | +0.0031 | 0.6031 |
| 256 | flkR | 260 | flkR | +0.0028 | 0.4619 |
| 258 | flkR | 260 | flkR | +0.0024 | 0.3484 |

### L24 H18 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0199

**Key mass** (top-1=48%, top-2=70%, top-3=79%)  [DISTR(I114/A260/V233)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 114 | flkL | +0.0095 | 47.6% |
| 260 | flkR | +0.0044 | 22.1% |
| 233 | ss2 | +0.0018 | 9.1% |
| 237 | ss2 | +0.0013 | 6.5% |
| 236 | ss2 | +0.0012 | 6.2% |

**Query mass** (top-1=22%, top-2=42%, top-3=59%)  [DISTR(G237/L239/L122/I238)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0043 | 21.8% |
| 239 | ss2 | +0.0041 | 20.6% |
| 122 | ss1 | +0.0032 | 16.2% |
| 238 | ss2 | +0.0031 | 15.8% |
| 236 | ss2 | +0.0022 | 11.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +123 | 1 | 7.7% |
| +125 | 1 | 7.7% |
| -24 | 1 | 7.7% |
| +8 | 1 | 7.7% |
| +1 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 30.8% |
| ss2 | flkL | 2 | 15.4% |
| ss1 | flkL | 2 | 15.4% |
| ss2 | ss2 | 2 | 15.4% |
| ss1 | ss2 | 2 | 15.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 237 | ss2 | 114 | flkL | +0.0043 | 0.2349 |
| 239 | ss2 | 114 | flkL | +0.0023 | 0.0525 |
| 236 | ss2 | 260 | flkR | +0.0022 | 0.0836 |
| 122 | ss1 | 114 | flkL | +0.0020 | 0.0721 |
| 238 | ss2 | 237 | ss2 | +0.0013 | 0.0329 |

### L26 H7 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0282

**Key mass** (top-1=51%, top-2=91%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0145 | 51.5% |
| 237 | ss2 | +0.0111 | 39.6% |
| 260 | flkR | +0.0016 | 5.6% |
| -1 | other | +0.0009 | 3.3% |

**Query mass** (top-1=31%, top-2=49%, top-3=64%)  [DISTR(I238/I111/I114/I128)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0088 | 31.1% |
| 111 | flkL | +0.0049 | 17.4% |
| 114 | flkL | +0.0044 | 15.7% |
| 128 | ss1 | +0.0035 | 12.4% |
| 260 | flkR | +0.0016 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 20.0% |
| -16 | 1 | 10.0% |
| -13 | 1 | 10.0% |
| +0 | 1 | 10.0% |
| -1 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 3 | 30.0% |
| ss2 | ss2 | 2 | 20.0% |
| ss1 | ss1 | 2 | 20.0% |
| flkR | flkR | 1 | 10.0% |
| ss1 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 238 | ss2 | 237 | ss2 | +0.0088 | 0.2919 |
| 111 | flkL | 127 | ss1 | +0.0049 | 0.6270 |
| 114 | flkL | 127 | ss1 | +0.0044 | 0.5718 |
| 128 | ss1 | 127 | ss1 | +0.0027 | 0.2805 |
| 260 | flkR | 260 | flkR | +0.0016 | 0.1945 |

### L27 H15 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0924

**Key mass** (top-1=20%, top-2=36%, top-3=46%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 235 | ss2 | +0.0186 | 20.2% |
| 238 | ss2 | +0.0151 | 16.3% |
| 236 | ss2 | +0.0087 | 9.4% |
| 239 | ss2 | +0.0073 | 7.9% |
| 125 | ss1 | +0.0070 | 7.6% |

**Query mass** (top-1=31%, top-2=51%, top-3=61%)  [DISTR(L122/V125/T121/L239)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0284 | 30.7% |
| 125 | ss1 | +0.0186 | 20.2% |
| 121 | ss1 | +0.0098 | 10.6% |
| 239 | ss2 | +0.0092 | 10.0% |
| 235 | ss2 | +0.0070 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +45 | 2 | 7.7% |
| -110 | 1 | 3.8% |
| -116 | 1 | 3.8% |
| -114 | 1 | 3.8% |
| +110 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 7 | 26.9% |
| ss2 | flkR | 6 | 23.1% |
| ss1 | ss2 | 5 | 19.2% |
| ss2 | ss1 | 3 | 11.5% |
| flkR | ss2 | 3 | 11.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 125 | ss1 | 235 | ss2 | +0.0186 | 0.6082 |
| 122 | ss1 | 238 | ss2 | +0.0151 | 0.1162 |
| 122 | ss1 | 236 | ss2 | +0.0078 | 0.0648 |
| 235 | ss2 | 125 | ss1 | +0.0070 | 0.6715 |
| 239 | ss2 | 258 | flkR | +0.0066 | 0.2187 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 39  |  total attr: +0.1753

**Key mass** (top-1=27%, top-2=43%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss1 | +0.0467 | 26.6% |
| 238 | ss2 | +0.0279 | 15.9% |
| 122 | ss1 | +0.0128 | 7.3% |
| 82 | flkL | +0.0110 | 6.3% |
| 268 | flkR | +0.0109 | 6.2% |

**Query mass** (top-1=34%, top-2=58%, top-3=71%)  [DISTR(D236/L122/I238)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 236 | ss2 | +0.0588 | 33.5% |
| 122 | ss1 | +0.0429 | 24.5% |
| 238 | ss2 | +0.0229 | 13.1% |
| 123 | ss1 | +0.0115 | 6.5% |
| 234 | ss2 | +0.0071 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 5.1% |
| -104 | 2 | 5.1% |
| +128 | 2 | 5.1% |
| +112 | 1 | 2.6% |
| -116 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=15%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 15.4% |
| ss1 | flkR | 6 | 15.4% |
| ss2 | flkL | 6 | 15.4% |
| ss2 | flkR | 5 | 12.8% |
| ss1 | flkL | 3 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 236 | ss2 | 124 | ss1 | +0.0457 | 0.6541 |
| 122 | ss1 | 238 | ss2 | +0.0279 | 0.2036 |
| 238 | ss2 | 122 | ss1 | +0.0128 | 0.0763 |
| 122 | ss1 | 268 | flkR | +0.0085 | 0.1041 |
| 236 | ss2 | 82 | flkL | +0.0079 | 0.0618 |

### L30 H1 — Rank #14

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | CROSS:ss2→ss1  |  cells: 10  |  total attr: +0.0197

**Key mass** (top-1=46%, top-2=60%, top-3=66%)  [DISTR(L122/I123/L258/D236)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0091 | 46.4% |
| 123 | ss1 | +0.0027 | 13.7% |
| 258 | flkR | +0.0011 | 5.5% |
| 236 | ss2 | +0.0011 | 5.4% |
| 124 | ss1 | +0.0011 | 5.4% |

**Query mass** (top-1=46%, top-2=70%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0091 | 46.4% |
| 239 | ss2 | +0.0047 | 23.8% |
| 236 | ss2 | +0.0028 | 14.4% |
| 126 | ss1 | +0.0011 | 5.4% |
| 234 | ss2 | +0.0011 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 20.0% |
| +110 | 2 | 20.0% |
| -19 | 1 | 10.0% |
| -110 | 1 | 10.0% |
| -4 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 40.0% |
| ss2 | flkR | 3 | 30.0% |
| ss1 | ss2 | 2 | 20.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 238 | ss2 | 122 | ss1 | +0.0091 | 0.0798 |
| 239 | ss2 | 123 | ss1 | +0.0027 | 0.0351 |
| 239 | ss2 | 258 | flkR | +0.0011 | 0.0458 |
| 126 | ss1 | 236 | ss2 | +0.0011 | 0.0254 |
| 234 | ss2 | 124 | ss1 | +0.0011 | 0.0470 |

### L31 H17 — Rank #13

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 17  |  total attr: +0.0513

**Key mass** (top-1=52%, top-2=64%, top-3=71%)  [DISTR(I261/?-1/Q81)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 261 | flkR | +0.0267 | 52.0% |
| -1 | other | +0.0062 | 12.0% |
| 81 | flkL | +0.0035 | 6.7% |
| 110 | flkL | +0.0031 | 6.0% |
| 126 | ss1 | +0.0022 | 4.3% |

**Query mass** (top-1=64%, top-2=80%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0327 | 63.7% |
| 236 | ss2 | +0.0086 | 16.7% |
| 123 | ss1 | +0.0054 | 10.6% |
| 239 | ss2 | +0.0016 | 3.1% |
| 266 | flkR | +0.0011 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -139 | 1 | 5.9% |
| +126 | 1 | 5.9% |
| +237 | 1 | 5.9% |
| +41 | 1 | 5.9% |
| +14 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=18%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 3 | 17.6% |
| ss1 | flkL | 3 | 17.6% |
| ss1 | flkR | 2 | 11.8% |
| ss2 | flkR | 2 | 11.8% |
| ss2 | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 261 | flkR | +0.0267 | 0.2846 |
| 236 | ss2 | 110 | flkL | +0.0031 | 0.0442 |
| 236 | ss2 | -1 | other | +0.0026 | 0.0428 |
| 122 | ss1 | 81 | flkL | +0.0024 | 0.0278 |
| 123 | ss1 | 109 | flkL | +0.0021 | 0.0882 |

### L32 H13 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 6  |  total attr: +0.0218

**Key mass** (top-1=45%, top-2=79%, top-3=89%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 236 | ss2 | +0.0099 | 45.2% |
| 122 | ss1 | +0.0073 | 33.4% |
| 238 | ss2 | +0.0022 | 10.1% |
| 239 | ss2 | +0.0013 | 6.1% |
| 234 | ss2 | +0.0011 | 5.2% |

**Query mass** (top-1=55%, top-2=73%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0121 | 55.3% |
| 238 | ss2 | +0.0039 | 18.0% |
| 236 | ss2 | +0.0034 | 15.4% |
| 123 | ss1 | +0.0013 | 6.1% |
| 124 | ss1 | +0.0011 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -116 | 2 | 33.3% |
| -114 | 1 | 16.7% |
| +116 | 1 | 16.7% |
| +114 | 1 | 16.7% |
| -110 | 1 | 16.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 66.7% |
| ss2 | ss1 | 2 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 236 | ss2 | +0.0099 | 0.0524 |
| 238 | ss2 | 122 | ss1 | +0.0039 | 0.0282 |
| 236 | ss2 | 122 | ss1 | +0.0034 | 0.0179 |
| 122 | ss1 | 238 | ss2 | +0.0022 | 0.0158 |
| 123 | ss1 | 239 | ss2 | +0.0013 | 0.0101 |

### L32 H18 — Rank #1

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 13  |  total attr: +0.1900

**Key mass** (top-1=47%, top-2=76%, top-3=84%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0886 | 46.6% |
| 236 | ss2 | +0.0555 | 29.2% |
| 239 | ss2 | +0.0157 | 8.3% |
| 123 | ss1 | +0.0110 | 5.8% |
| 124 | ss1 | +0.0066 | 3.5% |

**Query mass** (top-1=31%, top-2=56%, top-3=72%)  [DISTR(D236/L122/I238)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 236 | ss2 | +0.0595 | 31.3% |
| 122 | ss1 | +0.0467 | 24.6% |
| 238 | ss2 | +0.0313 | 16.5% |
| 239 | ss2 | +0.0135 | 7.1% |
| 126 | ss1 | +0.0118 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 15.4% |
| -110 | 2 | 15.4% |
| -116 | 2 | 15.4% |
| +110 | 2 | 15.4% |
| +114 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 53.8% |
| ss2 | ss1 | 6 | 46.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 236 | ss2 | 122 | ss1 | +0.0573 | 0.1849 |
| 122 | ss1 | 236 | ss2 | +0.0437 | 0.1411 |
| 238 | ss2 | 122 | ss1 | +0.0313 | 0.1362 |
| 126 | ss1 | 236 | ss2 | +0.0118 | 0.1180 |
| 239 | ss2 | 123 | ss1 | +0.0110 | 0.0503 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #2 | L0 | H19 | 0 | +0.0000 | — |  | — |  |  |  |
| #3 | L9 | H14 | 18 | +0.0955 | DUAL-ANCHOR | G230/G75 | DUAL-ANCHOR | G75/G230 |  |  |
| #5 | L10 | H9 | 19 | +0.0665 | SINGLE-ANCHOR | G75 | DISTRIBUTED |  |  |  |
| #24 | L10 | H13 | 11 | +0.0500 | SINGLE-ANCHOR | G75 | DISTRIBUTED | V125/L122/V129 |  | ss1→flkL |
| #27 | L11 | H1 | 8 | +0.0182 | MULTI-ANCHOR |  | DISTRIBUTED | G127/G237/G120 | POSITIONAL |  |
| #30 | L13 | H2 | 12 | +0.0378 | SINGLE-ANCHOR | G127 | DISTRIBUTED | L122/G120/I123/V235/G127 |  | INTRA:ss1 |
| #15 | L13 | H7 | 26 | +0.1311 | DISTRIBUTED | G237/G127/I119/G120 | DISTRIBUTED | D82/I249/?-1/G237 |  |  |
| #16 | L13 | H14 | 17 | +0.0450 | SINGLE-ANCHOR | G127 | DISTRIBUTED |  |  |  |
| #11 | L14 | H4 | 14 | +0.0510 | SINGLE-ANCHOR | G127 | MULTI-ANCHOR |  |  | CROSS:ss2→ss1 |
| #28 | L16 | H12 | 17 | +0.0487 | DISTRIBUTED | G237/G127/N231/T121/D236 | DISTRIBUTED | L239/I238/I123/V233 | POSITIONAL |  |
| #18 | L17 | H1 | 32 | +0.0510 | DISTRIBUTED |  | DISTRIBUTED | L122/I238/R110/G230/G127 |  |  |
| #25 | L17 | H3 | 13 | +0.0268 | DISTRIBUTED | ?-1/?268/G127 | DISTRIBUTED | R110/L239/D236/I238/T256 |  |  |
| #4 | L17 | H10 | 27 | +0.1013 | DUAL-ANCHOR | G237/G127 | DISTRIBUTED | L239/D236/L122/I238 |  |  |
| #7 | L17 | H18 | 35 | +0.1063 | DISTRIBUTED | L239/?-1/V78/L84 | DISTRIBUTED |  |  |  |
| #21 | L18 | H4 | 8 | +0.0417 | DUAL-ANCHOR | G127/G237 | DUAL-ANCHOR | L122/G237 |  |  |
| #12 | L18 | H12 | 22 | +0.0625 | DISTRIBUTED | G127/G230/G120 | DISTRIBUTED |  |  |  |
| #10 | L19 | H6 | 11 | +0.0816 | DUAL-ANCHOR | G127/G237 | MULTI-ANCHOR |  |  |  |
| #26 | L20 | H1 | 12 | +0.0285 | DISTRIBUTED | I114/R110/G127 | DISTRIBUTED | G127/I114/L239/L122/A260 |  |  |
| #22 | L20 | H10 | 6 | +0.0420 | SINGLE-ANCHOR | G127 | SINGLE-ANCHOR | L122 |  | INTRA:ss1 |
| #23 | L21 | H6 | 15 | +0.0503 | DISTRIBUTED | G127/A260/G230 | DISTRIBUTED | L122/A260/D236/Y259 |  | INTRA:flkR |
| #29 | L22 | H3 | 10 | +0.0210 | DISTRIBUTED | S116/I123/R130/R110/R115 | SINGLE-ANCHOR | L122 |  | ss1→flkL |
| #19 | L24 | H3 | 14 | +0.0422 | DUAL-ANCHOR | A260/G237 | DISTRIBUTED | L239/A260/L122/Y257 |  | INTRA:flkR |
| #17 | L24 | H18 | 13 | +0.0199 | DISTRIBUTED | I114/A260/V233 | DISTRIBUTED | G237/L239/L122/I238 |  |  |
| #20 | L26 | H7 | 10 | +0.0282 | DUAL-ANCHOR | G127/G237 | DISTRIBUTED | I238/I111/I114/I128 |  |  |
| #8 | L27 | H15 | 26 | +0.0924 | DISTRIBUTED |  | DISTRIBUTED | L122/V125/T121/L239 |  |  |
| #6 | L29 | H18 | 39 | +0.1753 | DISTRIBUTED |  | DISTRIBUTED | D236/L122/I238 |  |  |
| #14 | L30 | H1 | 10 | +0.0197 | DISTRIBUTED | L122/I123/L258/D236 | DUAL-ANCHOR | I238/L239 |  | CROSS:ss2→ss1 |
| #13 | L31 | H17 | 17 | +0.0513 | DISTRIBUTED | I261/?-1/Q81 | SINGLE-ANCHOR | L122 |  |  |
| #9 | L32 | H13 | 6 | +0.0218 | DUAL-ANCHOR | D236/L122 | DUAL-ANCHOR | L122/I238 |  | CROSS:ss1→ss2 |
| #1 | L32 | H18 | 13 | +0.1900 | DUAL-ANCHOR | L122/D236 | DISTRIBUTED | D236/L122/I238 |  | CROSS:ss1→ss2 |
