# Contact Pattern Analysis: 4OY3A

Generated: 2026-03-22 22:07:04   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4OY3A |
| Contact pair | (61, 181) |
| ss1 | [56, 67) |
| ss2 | [176, 187) |
| Clean flank | 39 |
| Corrupt flank | 38 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.5170 |
| Corrupt metric | 0.0137 |
| Gap | 0.5033 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 350 | 85.62% |
| positive IE | 115 | 71.87% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L5 | H13 | +0.8383 |
| 2 | L7 | H9 | +0.8273 |
| 3 | L0 | H0 | +0.7870 |
| 4 | L14 | H9 | +0.7731 |
| 5 | L12 | H2 | +0.7583 |
| 6 | L4 | H5 | +0.7279 |
| 7 | L32 | H13 | +0.6633 |
| 8 | L29 | H18 | +0.5603 |
| 9 | L16 | H19 | +0.5405 |
| 10 | L0 | H1 | +0.4184 |
| 11 | L11 | H15 | +0.4113 |
| 12 | L16 | H4 | +0.3979 |
| 13 | L3 | H6 | +0.3963 |
| 14 | L32 | H18 | +0.3493 |
| 15 | L15 | H18 | +0.3469 |
| 16 | L12 | H15 | +0.3340 |
| 17 | L5 | H7 | +0.3174 |
| 18 | L12 | H14 | +0.3036 |
| 19 | L16 | H17 | +0.2854 |
| 20 | L19 | H14 | +0.2794 |
| 21 | L12 | H3 | +0.2731 |
| 22 | L1 | H0 | +0.2531 |
| 23 | L10 | H9 | +0.2482 |
| 24 | L13 | H8 | +0.2428 |
| 25 | L5 | H9 | +0.2367 |
| 26 | L0 | H13 | +0.2295 |
| 27 | L13 | H1 | +0.2279 |
| 28 | L5 | H19 | +0.2238 |
| 29 | L4 | H10 | +0.2136 |
| 30 | L6 | H0 | +0.2077 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.00% |
| 4 | 0.00% |
| 5 | -0.00% |
| 6 | -0.00% |
| 7 | 0.07% |
| 8 | 0.11% |
| 9 | 0.10% |
| 10 | 0.11% |
| 20 | 0.31% |
| 80 | 42.68% |
| 450 | 201.61% |

## Cell Attribution Analysis

Total cells: 5,827,670

- Positive: 2,942,733
- Negative: 2,883,081

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000383 | 582,768 |
| 95th | +0.00001126 | 291,384 |
| 99th | +0.00008178 | 58,277 |
| 99.5th | +0.00017325 | 29,139 |
| 99.9th | +0.00089250 | 5,828 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H9 | 74 | other | 47 | flkL | +0.270843 | 0.036197 |
| L3 | H6 | 74 | other | 53 | flkL | +0.214134 | 0.015046 |
| L11 | H15 | 74 | other | 193 | flkR | +0.190800 | 0.291351 |
| L20 | H2 | 61 | ss1 | 47 | flkL | +0.159711 | 0.212913 |
| L15 | H4 | 53 | flkL | -1 | other | +0.144433 | 0.535679 |
| L10 | H9 | 74 | other | 193 | flkR | +0.138686 | 0.071755 |
| L3 | H9 | 74 | other | 47 | flkL | +0.137674 | 0.011889 |
| L2 | H0 | 74 | other | -1 | other | +0.136017 | 0.033191 |
| L16 | H19 | 53 | flkL | 193 | flkR | +0.133592 | 0.520448 |
| L19 | H14 | 57 | ss1 | 53 | flkL | +0.122284 | 0.213360 |
| L12 | H15 | 57 | ss1 | 74 | other | +0.119448 | 0.377248 |
| L10 | H16 | 74 | other | 193 | flkR | +0.118572 | 0.059898 |
| L20 | H13 | 61 | ss1 | 57 | ss1 | +0.116179 | 0.221014 |
| L6 | H0 | 74 | other | 6 | other | +0.111092 | 0.010098 |
| L6 | H19 | 74 | other | 6 | other | +0.109919 | 0.023288 |
| L12 | H14 | -1 | other | 74 | other | +0.103374 | 0.460778 |
| L5 | H7 | 74 | other | 1 | other | +0.102877 | 0.007466 |
| L12 | H15 | 61 | ss1 | 74 | other | +0.100341 | 0.387903 |
| L14 | H9 | 7 | other | 74 | other | +0.099845 | 0.687916 |
| L5 | H7 | 74 | other | 0 | other | +0.094188 | 0.010544 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H0 | 168 | other | 0 | other | -0.037605 | 0.008676 |
| L5 | H13 | 74 | other | 17 | flkL | -0.037890 | 0.016012 |
| L5 | H19 | 74 | other | 9 | other | -0.038129 | 0.015316 |
| L12 | H3 | 50 | flkL | 74 | other | -0.038419 | 0.383578 |
| L19 | H15 | 61 | ss1 | 74 | other | -0.040206 | 0.220301 |
| L21 | H6 | 61 | ss1 | 64 | ss1 | -0.040507 | 0.112910 |
| L7 | H13 | 193 | flkR | 223 | flkR | -0.042186 | 0.118200 |
| L12 | H2 | 0 | other | 74 | other | -0.043686 | 0.344236 |
| L12 | H15 | 66 | ss1 | 74 | other | -0.044592 | 0.343985 |
| L4 | H17 | 1 | other | 18 | flkL | -0.045337 | 0.051126 |
| L7 | H13 | 66 | ss1 | 18 | flkL | -0.050574 | 0.253047 |
| L5 | H13 | 168 | other | 219 | flkR | -0.056276 | 0.022202 |
| L1 | H0 | 219 | flkR | 225 | flkR | -0.056906 | 0.113033 |
| L8 | H13 | 74 | other | 183 | ss2 | -0.063691 | 0.089378 |
| L16 | H19 | 57 | ss1 | 193 | flkR | -0.065072 | 0.457918 |
| L6 | H17 | 66 | ss1 | 18 | flkL | -0.068184 | 0.069381 |
| L4 | H17 | 0 | other | 18 | flkL | -0.069518 | 0.084956 |
| L18 | H2 | 53 | flkL | 193 | flkR | -0.075433 | 0.087630 |
| L20 | H2 | 63 | ss1 | 47 | flkL | -0.103589 | 0.214621 |
| L6 | H19 | 168 | other | 190 | flkR | -0.136053 | 0.015534 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0137 | 0.00% |
| 10 | 10 | 10 | 0.0137 | 0.00% |
| 20 | 20 | 18 | 0.0137 | 0.00% |
| 50 | 50 | 38 | 0.0137 | -0.00% |
| 100 | 100 | 55 | 0.0137 | 0.01% |
| 200 | 200 | 75 | 0.0143 | 0.11% |
| 500 | 500 | 96 | 0.0302 | 3.27% |
| 1000 | 1,000 | 112 | 0.1788 | 32.80% |
| 2000 | 2,000 | 114 | 0.2502 | 46.99% |
| 5000 | 5,000 | 115 | 0.3708 | 70.95% |
| 10000 | 10,000 | 115 | 0.4536 | 87.40% |
| 20000 | 20,000 | 115 | 0.5614 | 108.81% |
| 50000 | 50,000 | 115 | 0.6239 | 121.23% |

## Motif Analysis

### L0 H0 — Rank #3

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 26  |  total attr: +0.1998

**Key mass** (top-1=11%, top-2=17%, top-3=21%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | flkL | +0.0214 | 10.7% |
| 48 | flkL | +0.0117 | 5.9% |
| 19 | flkL | +0.0093 | 4.6% |
| 28 | flkL | +0.0091 | 4.6% |
| 200 | flkR | +0.0091 | 4.5% |

**Query mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | flkL | +0.1938 | 97.0% |
| 196 | flkR | +0.0060 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 3.8% |
| -31 | 1 | 3.8% |
| -2 | 1 | 3.8% |
| -11 | 1 | 3.8% |
| -183 | 1 | 3.8% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 14 | 53.8% |
| flkL | flkR | 8 | 30.8% |
| flkL | ss2 | 2 | 7.7% |
| flkL | ss1 | 1 | 3.8% |
| flkR | flkL | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 17 | flkL | 17 | flkL | +0.0154 | 0.0261 |
| 17 | flkL | 48 | flkL | +0.0117 | 0.0133 |
| 17 | flkL | 19 | flkL | +0.0093 | 0.0183 |
| 17 | flkL | 28 | flkL | +0.0091 | 0.0155 |
| 17 | flkL | 200 | flkR | +0.0091 | 0.0103 |

### L0 H1 — Rank #10

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 13  |  total attr: +0.0657

**Key mass** (top-1=8%, top-2=16%, top-3=24%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 23 | flkL | +0.0054 | 8.2% |
| 34 | flkL | +0.0053 | 8.1% |
| 55 | flkL | +0.0052 | 8.0% |
| 48 | flkL | +0.0052 | 7.9% |
| 180 | ss2 | +0.0051 | 7.8% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | flkL | +0.0657 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 1 | 7.7% |
| -17 | 1 | 7.7% |
| -38 | 1 | 7.7% |
| -31 | 1 | 7.7% |
| -163 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 38.5% |
| flkL | flkR | 5 | 38.5% |
| flkL | ss2 | 3 | 23.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 17 | flkL | 23 | flkL | +0.0054 | 0.0022 |
| 17 | flkL | 34 | flkL | +0.0053 | 0.0022 |
| 17 | flkL | 55 | flkL | +0.0052 | 0.0022 |
| 17 | flkL | 48 | flkL | +0.0052 | 0.0021 |
| 17 | flkL | 180 | ss2 | +0.0051 | 0.0021 |

### L0 H13 — Rank #26

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 6  |  total attr: +0.0304

**Key mass** (top-1=50%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | flkR | +0.0152 | 50.1% |
| 17 | flkL | +0.0152 | 49.9% |

**Query mass** (top-1=35%, top-2=52%, top-3=68%)  [DISTR(F35/V47/L59/N42)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 35 | flkL | +0.0106 | 34.9% |
| 47 | flkL | +0.0052 | 17.0% |
| 59 | ss1 | +0.0050 | 16.5% |
| 42 | flkL | +0.0048 | 15.8% |
| 16 | other | +0.0048 | 15.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 16.7% |
| -178 | 1 | 16.7% |
| -190 | 1 | 16.7% |
| -166 | 1 | 16.7% |
| +25 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 2 | 33.3% |
| flkL | flkR | 2 | 33.3% |
| ss1 | flkR | 1 | 16.7% |
| other | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 35 | flkL | 17 | flkL | +0.0056 | 0.0025 |
| 47 | flkL | 225 | flkR | +0.0052 | 0.0016 |
| 35 | flkL | 225 | flkR | +0.0050 | 0.0024 |
| 59 | ss1 | 225 | flkR | +0.0050 | 0.0022 |
| 42 | flkL | 17 | flkL | +0.0048 | 0.0014 |

### L1 H0 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 18  |  total attr: +0.2400

**Key mass** (top-1=88%, top-2=93%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | flkR | +0.2122 | 88.4% |
| 191 | flkR | +0.0109 | 4.6% |
| 190 | flkR | +0.0097 | 4.1% |
| 17 | flkL | +0.0071 | 2.9% |

**Query mass** (top-1=18%, top-2=30%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 215 | flkR | +0.0420 | 17.5% |
| 216 | flkR | +0.0303 | 12.6% |
| 183 | ss2 | +0.0207 | 8.6% |
| 193 | flkR | +0.0182 | 7.6% |
| 190 | flkR | +0.0174 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 11.1% |
| -10 | 1 | 5.6% |
| -9 | 1 | 5.6% |
| -32 | 1 | 5.6% |
| -35 | 1 | 5.6% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=78%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 14 | 77.8% |
| ss2 | flkR | 3 | 16.7% |
| other | flkL | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 215 | flkR | 225 | flkR | +0.0420 | 0.0638 |
| 216 | flkR | 225 | flkR | +0.0303 | 0.0728 |
| 193 | flkR | 225 | flkR | +0.0182 | 0.0129 |
| 190 | flkR | 225 | flkR | +0.0174 | 0.0161 |
| 203 | flkR | 225 | flkR | +0.0123 | 0.0298 |

### L3 H6 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 12  |  total attr: +0.2917

**Key mass** (top-1=78%, top-2=94%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.2281 | 78.2% |
| 17 | flkL | +0.0454 | 15.6% |
| 20 | flkL | +0.0079 | 2.7% |
| 46 | flkL | +0.0055 | 1.9% |
| 61 | ss1 | +0.0047 | 1.6% |

**Query mass** (top-1=73%, top-2=80%, top-3=85%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.2141 | 73.4% |
| 42 | flkL | +0.0190 | 6.5% |
| 73 | other | +0.0140 | 4.8% |
| 43 | flkL | +0.0065 | 2.2% |
| 44 | flkL | +0.0064 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +20 | 3 | 25.0% |
| +22 | 2 | 16.7% |
| +21 | 1 | 8.3% |
| +25 | 1 | 8.3% |
| +26 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 8 | 66.7% |
| other | flkL | 2 | 16.7% |
| ss1 | flkL | 1 | 8.3% |
| other | ss1 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 53 | flkL | +0.2141 | 0.0150 |
| 73 | other | 53 | flkL | +0.0140 | 0.0222 |
| 42 | flkL | 17 | flkL | +0.0110 | 0.0170 |
| 42 | flkL | 20 | flkL | +0.0079 | 0.0072 |
| 43 | flkL | 17 | flkL | +0.0065 | 0.0198 |

### L4 H5 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.4061

**Key mass** (top-1=65%, top-2=73%, top-3=78%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 22 | flkL | +0.2649 | 65.2% |
| 39 | flkL | +0.0300 | 7.4% |
| -1 | other | +0.0230 | 5.7% |
| 187 | flkR | +0.0146 | 3.6% |
| 38 | flkL | +0.0129 | 3.2% |

**Query mass** (top-1=17%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 0 | other | +0.0699 | 17.2% |
| 1 | other | +0.0618 | 15.2% |
| 42 | flkL | +0.0479 | 11.8% |
| 6 | other | +0.0343 | 8.4% |
| 7 | other | +0.0263 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 4 | 15.4% |
| +3 | 3 | 11.5% |
| -17 | 2 | 7.7% |
| +6 | 2 | 7.7% |
| +5 | 2 | 7.7% |

**Region-pair profile** (q→k)  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 11 | 42.3% |
| flkL | flkL | 7 | 26.9% |
| other | other | 3 | 11.5% |
| flkL | other | 3 | 11.5% |
| flkR | flkR | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 0 | other | 22 | flkL | +0.0568 | 0.1162 |
| 1 | other | 22 | flkL | +0.0516 | 0.1265 |
| 6 | other | 22 | flkL | +0.0343 | 0.0992 |
| 42 | flkL | 39 | flkL | +0.0300 | 0.0100 |
| 7 | other | 22 | flkL | +0.0263 | 0.0805 |

### L4 H10 — Rank #29

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 12  |  total attr: +0.2001

**Key mass** (top-1=45%, top-2=61%, top-3=70%)  [DISTR(S219/C183/F222/F208)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 219 | flkR | +0.0893 | 44.6% |
| 183 | ss2 | +0.0319 | 15.9% |
| 222 | flkR | +0.0185 | 9.3% |
| 208 | flkR | +0.0165 | 8.2% |
| 17 | flkL | +0.0136 | 6.8% |

**Query mass** (top-1=72%, top-2=82%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.1448 | 72.3% |
| -1 | other | +0.0194 | 9.7% |
| 168 | other | +0.0176 | 8.8% |
| 172 | other | +0.0063 | 3.2% |
| 192 | flkR | +0.0060 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -145 | 1 | 8.3% |
| -109 | 1 | 8.3% |
| -134 | 1 | 8.3% |
| -18 | 1 | 8.3% |
| -137 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 7 | 58.3% |
| other | flkL | 2 | 16.7% |
| flkR | other | 2 | 16.7% |
| other | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 219 | flkR | +0.0730 | 0.0145 |
| 74 | other | 183 | ss2 | +0.0319 | 0.0071 |
| 74 | other | 208 | flkR | +0.0165 | 0.0013 |
| -1 | other | 17 | flkL | +0.0136 | 0.0128 |
| 74 | other | 211 | flkR | +0.0124 | 0.0019 |

### L5 H7 — Rank #17

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.5561

**Key mass** (top-1=19%, top-2=36%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 1 | other | +0.1076 | 19.4% |
| 0 | other | +0.0942 | 16.9% |
| 38 | flkL | +0.0597 | 10.7% |
| 5 | other | +0.0504 | 9.1% |
| 2 | other | +0.0457 | 8.2% |

**Query mass** (top-1=98%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.5435 | 97.7% |
| 13 | other | +0.0079 | 1.4% |
| 73 | other | +0.0047 | 0.9% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +72 | 2 | 12.5% |
| +73 | 1 | 6.2% |
| +74 | 1 | 6.2% |
| +36 | 1 | 6.2% |
| +69 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 10 | 62.5% |
| other | flkL | 5 | 31.2% |
| other | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 1 | other | +0.1029 | 0.0075 |
| 74 | other | 0 | other | +0.0942 | 0.0105 |
| 74 | other | 38 | flkL | +0.0597 | 0.0092 |
| 74 | other | 5 | other | +0.0504 | 0.0049 |
| 74 | other | 2 | other | +0.0457 | 0.0036 |

### L5 H9 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:flkL  |  cells: 5  |  total attr: +0.1930

**Key mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 42 | flkL | +0.1868 | 96.8% |
| 53 | flkL | +0.0062 | 3.2% |

**Query mass** (top-1=44%, top-2=83%, top-3=96%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +0.0841 | 43.6% |
| 48 | flkL | +0.0754 | 39.1% |
| 46 | flkL | +0.0255 | 13.2% |
| 45 | flkL | +0.0080 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 1 | 20.0% |
| +6 | 1 | 20.0% |
| +4 | 1 | 20.0% |
| +3 | 1 | 20.0% |
| -6 | 1 | 20.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 47 | flkL | 42 | flkL | +0.0780 | 0.0369 |
| 48 | flkL | 42 | flkL | +0.0754 | 0.0487 |
| 46 | flkL | 42 | flkL | +0.0255 | 0.0506 |
| 45 | flkL | 42 | flkL | +0.0080 | 0.0418 |
| 47 | flkL | 53 | flkL | +0.0062 | 0.0040 |

### L5 H13 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 37  |  total attr: +0.5331

**Key mass** (top-1=22%, top-2=38%, top-3=53%)  [DISTR(L18/S219/I14/T15/K43)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 18 | flkL | +0.1157 | 21.7% |
| 219 | flkR | +0.0852 | 16.0% |
| 14 | other | +0.0833 | 15.6% |
| 15 | other | +0.0767 | 14.4% |
| 43 | flkL | +0.0670 | 12.6% |

**Query mass** (top-1=55%, top-2=61%, top-3=68%)  [DISTR(L74/V172/V78/V47)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.2912 | 54.6% |
| 172 | other | +0.0361 | 6.8% |
| 78 | other | +0.0352 | 6.6% |
| 47 | flkL | +0.0186 | 3.5% |
| 193 | flkR | +0.0183 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +59 | 2 | 5.4% |
| +60 | 2 | 5.4% |
| -47 | 2 | 5.4% |
| +62 | 2 | 5.4% |
| +30 | 2 | 5.4% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 12 | 32.4% |
| other | other | 7 | 18.9% |
| other | flkR | 7 | 18.9% |
| flkR | flkR | 4 | 10.8% |
| flkR | flkL | 3 | 8.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 15 | other | +0.0767 | 0.0085 |
| 74 | other | 18 | flkL | +0.0689 | 0.0090 |
| 74 | other | 43 | flkL | +0.0591 | 0.0037 |
| 74 | other | 14 | other | +0.0440 | 0.0145 |
| 172 | other | 219 | flkR | +0.0262 | 0.0297 |

### L5 H19 — Rank #28

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 14  |  total attr: +0.1113

**Key mass** (top-1=40%, top-2=70%, top-3=80%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 9 | other | +0.0448 | 40.3% |
| 229 | other | +0.0330 | 29.7% |
| 228 | other | +0.0115 | 10.3% |
| 17 | flkL | +0.0109 | 9.8% |
| 231 | other | +0.0062 | 5.5% |

**Query mass** (top-1=24%, top-2=44%, top-3=59%)  [DISTR(C190/V192/L74/L193)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.0265 | 23.8% |
| 192 | flkR | +0.0230 | 20.6% |
| 74 | other | +0.0158 | 14.2% |
| 193 | flkR | +0.0149 | 13.4% |
| 76 | other | +0.0086 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -38 | 2 | 14.3% |
| -39 | 1 | 7.1% |
| -37 | 1 | 7.1% |
| +57 | 1 | 7.1% |
| +184 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 7 | 50.0% |
| other | other | 4 | 28.6% |
| other | flkL | 2 | 14.3% |
| flkL | other | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 190 | flkR | 229 | other | +0.0203 | 0.0176 |
| 192 | flkR | 229 | other | +0.0128 | 0.0174 |
| 74 | other | 17 | flkL | +0.0109 | 0.0057 |
| 193 | flkR | 9 | other | +0.0087 | 0.0085 |
| 76 | other | 9 | other | +0.0086 | 0.0232 |

### L6 H0 — Rank #30

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 24  |  total attr: +0.6384

**Key mass** (top-1=19%, top-2=34%, top-3=47%)  [DISTR(I6/M0/L7/G1/K3)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 6 | other | +0.1243 | 19.5% |
| 0 | other | +0.0918 | 14.4% |
| 7 | other | +0.0865 | 13.5% |
| 1 | other | +0.0745 | 11.7% |
| 3 | other | +0.0700 | 11.0% |

**Query mass** (top-1=86%, top-2=93%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.5486 | 85.9% |
| 47 | flkL | +0.0480 | 7.5% |
| 168 | other | +0.0263 | 4.1% |
| 48 | flkL | +0.0100 | 1.6% |
| 51 | flkL | +0.0055 | 0.9% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +45 | 2 | 8.3% |
| +68 | 1 | 4.2% |
| +67 | 1 | 4.2% |
| +74 | 1 | 4.2% |
| +73 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 9 | 37.5% |
| other | flkL | 7 | 29.2% |
| flkL | other | 6 | 25.0% |
| other | ss1 | 1 | 4.2% |
| flkL | flkL | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 6 | other | +0.1111 | 0.0101 |
| 74 | other | 7 | other | +0.0865 | 0.0086 |
| 74 | other | 0 | other | +0.0698 | 0.0104 |
| 74 | other | 1 | other | +0.0663 | 0.0061 |
| 74 | other | 3 | other | +0.0554 | 0.0059 |

### L7 H9 — Rank #2

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 26  |  total attr: +0.7801

**Key mass** (top-1=36%, top-2=47%, top-3=56%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +0.2791 | 35.8% |
| 48 | flkL | +0.0910 | 11.7% |
| 0 | other | +0.0673 | 8.6% |
| 3 | other | +0.0434 | 5.6% |
| 27 | flkL | +0.0331 | 4.2% |

**Query mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.7668 | 98.3% |
| 73 | other | +0.0133 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +26 | 2 | 7.7% |
| +27 | 1 | 3.8% |
| +74 | 1 | 3.8% |
| +71 | 1 | 3.8% |
| +47 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 15 | 57.7% |
| other | other | 6 | 23.1% |
| other | flkR | 3 | 11.5% |
| other | ss1 | 1 | 3.8% |
| other | ss2 | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 47 | flkL | +0.2708 | 0.0362 |
| 74 | other | 48 | flkL | +0.0860 | 0.0198 |
| 74 | other | 0 | other | +0.0673 | 0.0160 |
| 74 | other | 3 | other | +0.0434 | 0.0087 |
| 74 | other | 27 | flkL | +0.0331 | 0.0069 |

### L10 H9 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 6  |  total attr: +0.2391

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.2391 | 100.0% |

**Query mass** (top-1=58%, top-2=69%, top-3=80%)  [DISTR(L74/G77/S76)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.1387 | 58.0% |
| 77 | other | +0.0269 | 11.3% |
| 76 | other | +0.0256 | 10.7% |
| 78 | other | +0.0242 | 10.1% |
| 73 | other | +0.0160 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 1 | 16.7% |
| -116 | 1 | 16.7% |
| -117 | 1 | 16.7% |
| -115 | 1 | 16.7% |
| -120 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 6 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 193 | flkR | +0.1387 | 0.0718 |
| 77 | other | 193 | flkR | +0.0269 | 0.1114 |
| 76 | other | 193 | flkR | +0.0256 | 0.0940 |
| 78 | other | 193 | flkR | +0.0242 | 0.0622 |
| 73 | other | 193 | flkR | +0.0160 | 0.0923 |

### L11 H15 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 5  |  total attr: +0.2338

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.2338 | 100.0% |

**Query mass** (top-1=82%, top-2=87%, top-3=92%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.1908 | 81.6% |
| 76 | other | +0.0128 | 5.5% |
| 77 | other | +0.0126 | 5.4% |
| 73 | other | +0.0095 | 4.1% |
| 78 | other | +0.0081 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 1 | 20.0% |
| -117 | 1 | 20.0% |
| -116 | 1 | 20.0% |
| -120 | 1 | 20.0% |
| -115 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 74 | other | 193 | flkR | +0.1908 | 0.2914 |
| 76 | other | 193 | flkR | +0.0128 | 0.1446 |
| 77 | other | 193 | flkR | +0.0126 | 0.1561 |
| 73 | other | 193 | flkR | +0.0095 | 0.1453 |
| 78 | other | 193 | flkR | +0.0081 | 0.1546 |

### L12 H2 — Rank #5

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.4281

**Key mass** (top-1=54%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.2294 | 53.6% |
| 74 | other | +0.1987 | 46.4% |

**Query mass** (top-1=30%, top-2=48%, top-3=63%)  [DISTR(L7/I6/G53/G5)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 7 | other | +0.1272 | 29.7% |
| 6 | other | +0.0774 | 18.1% |
| 53 | flkL | +0.0662 | 15.5% |
| 5 | other | +0.0579 | 13.5% |
| 4 | other | +0.0350 | 8.2% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -67 | 1 | 5.6% |
| -140 | 1 | 5.6% |
| -186 | 1 | 5.6% |
| -68 | 1 | 5.6% |
| -187 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 7 | 38.9% |
| other | other | 5 | 27.8% |
| flkL | other | 3 | 16.7% |
| flkL | flkR | 2 | 11.1% |
| ss1 | flkR | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 7 | other | 74 | other | +0.0711 | 0.4504 |
| 53 | flkL | 193 | flkR | +0.0576 | 0.1543 |
| 7 | other | 193 | flkR | +0.0560 | 0.3174 |
| 6 | other | 74 | other | +0.0454 | 0.4969 |
| 6 | other | 193 | flkR | +0.0320 | 0.3614 |

### L12 H3 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.2635

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.2635 | 100.0% |

**Query mass** (top-1=24%, top-2=42%, top-3=60%)  [DISTR(V47/T60/G53/T58)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 47 | flkL | +0.0634 | 24.0% |
| 60 | ss1 | +0.0486 | 18.5% |
| 53 | flkL | +0.0460 | 17.5% |
| 58 | ss1 | +0.0302 | 11.4% |
| 52 | flkL | +0.0186 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -27 | 1 | 10.0% |
| -14 | 1 | 10.0% |
| -21 | 1 | 10.0% |
| -16 | 1 | 10.0% |
| -22 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 6 | 60.0% |
| ss1 | other | 4 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 47 | flkL | 74 | other | +0.0634 | 0.3420 |
| 60 | ss1 | 74 | other | +0.0486 | 0.1909 |
| 53 | flkL | 74 | other | +0.0460 | 0.4067 |
| 58 | ss1 | 74 | other | +0.0302 | 0.1761 |
| 52 | flkL | 74 | other | +0.0186 | 0.3630 |

### L12 H14 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.2741

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.2741 | 100.0% |

**Query mass** (top-1=38%, top-2=58%, top-3=68%)  [DISTR(?-1/L7/I6/G5)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.1034 | 37.7% |
| 7 | other | +0.0557 | 20.3% |
| 6 | other | +0.0275 | 10.0% |
| 5 | other | +0.0188 | 6.9% |
| 4 | other | +0.0176 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -75 | 1 | 10.0% |
| -67 | 1 | 10.0% |
| -68 | 1 | 10.0% |
| -69 | 1 | 10.0% |
| -70 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 8 | 80.0% |
| flkL | other | 2 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| -1 | other | 74 | other | +0.1034 | 0.4608 |
| 7 | other | 74 | other | +0.0557 | 0.4805 |
| 6 | other | 74 | other | +0.0275 | 0.5124 |
| 5 | other | 74 | other | +0.0188 | 0.5414 |
| 4 | other | 74 | other | +0.0176 | 0.5440 |

### L12 H15 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.3902

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.3821 | 97.9% |
| 73 | other | +0.0080 | 2.1% |

**Query mass** (top-1=33%, top-2=58%, top-3=73%)  [DISTR(S57/T61/M64)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1275 | 32.7% |
| 61 | ss1 | +0.1003 | 25.7% |
| 64 | ss1 | +0.0562 | 14.4% |
| 60 | ss1 | +0.0467 | 12.0% |
| 51 | flkL | +0.0186 | 4.8% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -16 | 2 | 18.2% |
| -17 | 1 | 9.1% |
| -13 | 1 | 9.1% |
| -10 | 1 | 9.1% |
| -14 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 54.5% |
| flkL | other | 3 | 27.3% |
| other | other | 2 | 18.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 74 | other | +0.1194 | 0.3772 |
| 61 | ss1 | 74 | other | +0.1003 | 0.3879 |
| 64 | ss1 | 74 | other | +0.0562 | 0.3477 |
| 60 | ss1 | 74 | other | +0.0467 | 0.4626 |
| 51 | flkL | 74 | other | +0.0186 | 0.2312 |

### L13 H1 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.2005

**Key mass** (top-1=78%, top-2=87%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 74 | other | +0.1555 | 77.6% |
| 193 | flkR | +0.0199 | 9.9% |
| 78 | other | +0.0119 | 5.9% |
| 73 | other | +0.0066 | 3.3% |
| 77 | other | +0.0065 | 3.3% |

**Query mass** (top-1=29%, top-2=45%, top-3=56%)  [DISTR(L7/V47/I6/T58/I52)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 7 | other | +0.0574 | 28.6% |
| 47 | flkL | +0.0336 | 16.8% |
| 6 | other | +0.0219 | 10.9% |
| 58 | ss1 | +0.0167 | 8.3% |
| 52 | flkL | +0.0159 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -70 | 2 | 12.5% |
| -67 | 1 | 6.2% |
| -27 | 1 | 6.2% |
| -68 | 1 | 6.2% |
| -16 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | other | 8 | 50.0% |
| flkL | other | 4 | 25.0% |
| ss1 | other | 2 | 12.5% |
| other | flkR | 1 | 6.2% |
| ss1 | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 7 | other | 74 | other | +0.0371 | 0.1696 |
| 47 | flkL | 74 | other | +0.0336 | 0.3743 |
| 6 | other | 74 | other | +0.0171 | 0.1364 |
| 58 | ss1 | 74 | other | +0.0167 | 0.1064 |
| 52 | flkL | 74 | other | +0.0159 | 0.2352 |

### L13 H8 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 5  |  total attr: +0.1819

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.1819 | 100.0% |

**Query mass** (top-1=41%, top-2=59%, top-3=76%)  [DISTR(V78/G77/S76)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | other | +0.0749 | 41.2% |
| 77 | other | +0.0328 | 18.0% |
| 76 | other | +0.0300 | 16.5% |
| -1 | other | +0.0284 | 15.6% |
| 80 | other | +0.0159 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 1 | 20.0% |
| -116 | 1 | 20.0% |
| -117 | 1 | 20.0% |
| -194 | 1 | 20.0% |
| -113 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 78 | other | 193 | flkR | +0.0749 | 0.1948 |
| 77 | other | 193 | flkR | +0.0328 | 0.2795 |
| 76 | other | 193 | flkR | +0.0300 | 0.2262 |
| -1 | other | 193 | flkR | +0.0284 | 0.0878 |
| 80 | other | 193 | flkR | +0.0159 | 0.2354 |

### L14 H9 — Rank #4

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 17  |  total attr: +0.4321

**Key mass** (top-1=54%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.2355 | 54.5% |
| 74 | other | +0.1966 | 45.5% |

**Query mass** (top-1=31%, top-2=46%, top-3=59%)  [DISTR(L7/G53/I6/?-1)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 7 | other | +0.1355 | 31.4% |
| 53 | flkL | +0.0612 | 14.2% |
| 6 | other | +0.0561 | 13.0% |
| -1 | other | +0.0532 | 12.3% |
| 0 | other | +0.0322 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -67 | 1 | 5.9% |
| -140 | 1 | 5.9% |
| -194 | 1 | 5.9% |
| -68 | 1 | 5.9% |
| -186 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 8 | 47.1% |
| other | other | 6 | 35.3% |
| flkL | flkR | 3 | 17.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 7 | other | 74 | other | +0.0998 | 0.6879 |
| 53 | flkL | 193 | flkR | +0.0612 | 0.1240 |
| -1 | other | 193 | flkR | +0.0532 | 0.2849 |
| 6 | other | 74 | other | +0.0461 | 0.6623 |
| 7 | other | 193 | flkR | +0.0357 | 0.6185 |

### L15 H18 — Rank #15

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.2932

**Key mass** (top-1=23%, top-2=42%, top-3=58%)  [DISTR(V78/I88/G77/S76)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 78 | other | +0.0689 | 23.5% |
| 88 | other | +0.0535 | 18.3% |
| 77 | other | +0.0477 | 16.3% |
| 76 | other | +0.0452 | 15.4% |
| 80 | other | +0.0247 | 8.4% |

**Query mass** (top-1=78%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.2293 | 78.2% |
| 57 | ss1 | +0.0581 | 19.8% |
| 47 | flkL | +0.0058 | 2.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -23 | 2 | 12.5% |
| -27 | 2 | 12.5% |
| -21 | 2 | 12.5% |
| -25 | 1 | 6.2% |
| -35 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 10 | 62.5% |
| ss1 | other | 6 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 53 | flkL | 78 | other | +0.0529 | 0.0995 |
| 53 | flkL | 88 | other | +0.0454 | 0.0901 |
| 53 | flkL | 77 | other | +0.0359 | 0.0649 |
| 53 | flkL | 76 | other | +0.0356 | 0.0685 |
| 53 | flkL | 89 | other | +0.0171 | 0.0388 |

### L16 H4 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.2567

**Key mass** (top-1=71%, top-2=91%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 7 | other | +0.1818 | 70.8% |
| 6 | other | +0.0509 | 19.8% |
| 5 | other | +0.0096 | 3.7% |
| 193 | flkR | +0.0094 | 3.7% |
| 4 | other | +0.0050 | 2.0% |

**Query mass** (top-1=39%, top-2=58%, top-3=74%)  [DISTR(S57/Y49/T61)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1004 | 39.1% |
| 49 | flkL | +0.0487 | 19.0% |
| 61 | ss1 | +0.0413 | 16.1% |
| 64 | ss1 | +0.0246 | 9.6% |
| 59 | ss1 | +0.0096 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +43 | 2 | 12.5% |
| +52 | 2 | 12.5% |
| +50 | 1 | 6.2% |
| +42 | 1 | 6.2% |
| +54 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 9 | 56.2% |
| flkL | other | 5 | 31.2% |
| flkL | flkR | 1 | 6.2% |
| other | other | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 7 | other | +0.0640 | 0.3694 |
| 49 | flkL | 7 | other | +0.0371 | 0.3115 |
| 61 | ss1 | 7 | other | +0.0319 | 0.2984 |
| 57 | ss1 | 6 | other | +0.0218 | 0.1626 |
| 64 | ss1 | 7 | other | +0.0165 | 0.2580 |

### L16 H17 — Rank #19

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 20  |  total attr: +0.2540

**Key mass** (top-1=35%, top-2=52%, top-3=67%)  [DISTR(I88/V78/G80/N89)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 88 | other | +0.0900 | 35.4% |
| 78 | other | +0.0410 | 16.2% |
| 80 | other | +0.0400 | 15.7% |
| 89 | other | +0.0259 | 10.2% |
| 87 | other | +0.0213 | 8.4% |

**Query mass** (top-1=59%, top-2=85%, top-3=93%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.1497 | 59.0% |
| 57 | ss1 | +0.0671 | 26.4% |
| 47 | flkL | +0.0200 | 7.9% |
| 50 | flkL | +0.0063 | 2.5% |
| 64 | ss1 | +0.0057 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -24 | 3 | 15.0% |
| -31 | 2 | 10.0% |
| -27 | 2 | 10.0% |
| -23 | 2 | 10.0% |
| -35 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | other | 12 | 60.0% |
| ss1 | other | 8 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 53 | flkL | 88 | other | +0.0464 | 0.1123 |
| 57 | ss1 | 88 | other | +0.0275 | 0.1624 |
| 53 | flkL | 78 | other | +0.0244 | 0.0839 |
| 53 | flkL | 80 | other | +0.0215 | 0.0774 |
| 53 | flkL | 89 | other | +0.0203 | 0.0569 |

### L16 H19 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.4131

**Key mass** (top-1=78%, top-2=88%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.3240 | 78.4% |
| 88 | other | +0.0381 | 9.2% |
| 74 | other | +0.0313 | 7.6% |
| 87 | other | +0.0072 | 1.7% |
| 89 | other | +0.0062 | 1.5% |

**Query mass** (top-1=49%, top-2=57%, top-3=64%)  [DISTR(G53/S63/H56/I65)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.2035 | 49.3% |
| 63 | ss1 | +0.0336 | 8.1% |
| 56 | ss1 | +0.0292 | 7.1% |
| 65 | ss1 | +0.0238 | 5.8% |
| 60 | ss1 | +0.0218 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -140 | 1 | 4.8% |
| -130 | 1 | 4.8% |
| -137 | 1 | 4.8% |
| -35 | 1 | 4.8% |
| -21 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 6 | 28.6% |
| flkL | other | 6 | 28.6% |
| flkL | flkR | 5 | 23.8% |
| other | flkR | 2 | 9.5% |
| ss1 | other | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 53 | flkL | 193 | flkR | +0.1336 | 0.5204 |
| 63 | ss1 | 193 | flkR | +0.0336 | 0.3520 |
| 56 | ss1 | 193 | flkR | +0.0292 | 0.4731 |
| 53 | flkL | 88 | other | +0.0255 | 0.0797 |
| 53 | flkL | 74 | other | +0.0248 | 0.0930 |

### L19 H14 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 3  |  total attr: +0.1702

**Key mass** (top-1=92%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 53 | flkL | +0.1572 | 92.3% |
| 60 | ss1 | +0.0131 | 7.7% |

**Query mass** (top-1=72%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 57 | ss1 | +0.1223 | 71.8% |
| 64 | ss1 | +0.0479 | 28.2% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 66.7% |
| +11 | 1 | 33.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 66.7% |
| ss1 | ss1 | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 57 | ss1 | 53 | flkL | +0.1223 | 0.2134 |
| 64 | ss1 | 53 | flkL | +0.0349 | 0.1610 |
| 64 | ss1 | 60 | ss1 | +0.0131 | 0.2027 |

### L29 H18 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 20  |  total attr: +0.3340

**Key mass** (top-1=46%, top-2=61%, top-3=74%)  [DISTR(F186/V182/K185)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 186 | ss2 | +0.1542 | 46.2% |
| 182 | ss2 | +0.0489 | 14.6% |
| 185 | ss2 | +0.0438 | 13.1% |
| 178 | ss2 | +0.0231 | 6.9% |
| 58 | ss1 | +0.0200 | 6.0% |

**Query mass** (top-1=24%, top-2=42%, top-3=52%)  [DISTR(T62/T58/L66/S178/S63)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0812 | 24.3% |
| 58 | ss1 | +0.0593 | 17.8% |
| 66 | ss1 | +0.0318 | 9.5% |
| 178 | ss2 | +0.0316 | 9.5% |
| 63 | ss1 | +0.0312 | 9.4% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -123 | 4 | 20.0% |
| -124 | 3 | 15.0% |
| -120 | 3 | 15.0% |
| +124 | 2 | 10.0% |
| +120 | 2 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=65%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 13 | 65.0% |
| ss2 | ss1 | 3 | 15.0% |
| ss2 | flkL | 1 | 5.0% |
| flkL | ss2 | 1 | 5.0% |
| flkL | flkL | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 62 | ss1 | 186 | ss2 | +0.0584 | 0.5360 |
| 66 | ss1 | 186 | ss2 | +0.0318 | 0.2583 |
| 63 | ss1 | 186 | ss2 | +0.0312 | 0.3973 |
| 58 | ss1 | 182 | ss2 | +0.0292 | 0.3342 |
| 65 | ss1 | 186 | ss2 | +0.0257 | 0.5417 |

### L32 H13 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 22  |  total attr: +0.2800

**Key mass** (top-1=24%, top-2=45%, top-3=55%)  [DISTR(F186/T58/V182/S178/T62)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 186 | ss2 | +0.0665 | 23.8% |
| 58 | ss1 | +0.0602 | 21.5% |
| 182 | ss2 | +0.0259 | 9.3% |
| 178 | ss2 | +0.0230 | 8.2% |
| 62 | ss1 | +0.0220 | 7.9% |

**Query mass** (top-1=14%, top-2=28%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | ss2 | +0.0406 | 14.5% |
| 186 | ss2 | +0.0389 | 13.9% |
| 62 | ss1 | +0.0327 | 11.7% |
| 58 | ss1 | +0.0322 | 11.5% |
| 182 | ss2 | +0.0320 | 11.4% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 13.6% |
| -120 | 3 | 13.6% |
| +124 | 2 | 9.1% |
| -124 | 2 | 9.1% |
| +122 | 1 | 4.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 50.0% |
| ss1 | ss2 | 11 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 178 | ss2 | 58 | ss1 | +0.0406 | 0.2138 |
| 58 | ss1 | 178 | ss2 | +0.0230 | 0.1210 |
| 182 | ss2 | 58 | ss1 | +0.0196 | 0.3623 |
| 66 | ss1 | 186 | ss2 | +0.0193 | 0.1640 |
| 62 | ss1 | 182 | ss2 | +0.0166 | 0.1382 |

### L32 H18 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 10  |  total attr: +0.1120

**Key mass** (top-1=27%, top-2=48%, top-3=67%)  [DISTR(T62/V182/S178/T58)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 62 | ss1 | +0.0307 | 27.4% |
| 182 | ss2 | +0.0231 | 20.6% |
| 178 | ss2 | +0.0214 | 19.1% |
| 58 | ss1 | +0.0127 | 11.3% |
| 65 | ss1 | +0.0065 | 5.8% |

**Query mass** (top-1=26%, top-2=50%, top-3=70%)  [DISTR(T58/F186/V182)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 58 | ss1 | +0.0293 | 26.1% |
| 186 | ss2 | +0.0266 | 23.8% |
| 182 | ss2 | +0.0225 | 20.1% |
| 62 | ss1 | +0.0152 | 13.6% |
| 178 | ss2 | +0.0127 | 11.3% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +120 | 3 | 30.0% |
| -120 | 2 | 20.0% |
| +124 | 1 | 10.0% |
| -124 | 1 | 10.0% |
| +121 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=70%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 70.0% |
| ss1 | ss2 | 3 | 30.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 182 | ss2 | 62 | ss1 | +0.0225 | 0.1136 |
| 58 | ss1 | 178 | ss2 | +0.0214 | 0.0687 |
| 62 | ss1 | 182 | ss2 | +0.0152 | 0.0769 |
| 178 | ss2 | 58 | ss1 | +0.0127 | 0.0407 |
| 186 | ss2 | 62 | ss1 | +0.0082 | 0.0965 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #3 | L0 | H0 | 26 | +0.1998 | DISTRIBUTED |  | SINGLE-ANCHOR | I17 |  | INTRA:flkL |
| #10 | L0 | H1 | 13 | +0.0657 | DISTRIBUTED |  | SINGLE-ANCHOR | I17 |  |  |
| #26 | L0 | H13 | 6 | +0.0304 | DUAL-ANCHOR | S225/I17 | DISTRIBUTED | F35/V47/L59/N42 |  |  |
| #22 | L1 | H0 | 18 | +0.2400 | SINGLE-ANCHOR | S225 | DISTRIBUTED |  |  | INTRA:flkR |
| #13 | L3 | H6 | 12 | +0.2917 | SINGLE-ANCHOR | G53 | SINGLE-ANCHOR | L74 |  | INTRA:flkL |
| #6 | L4 | H5 | 26 | +0.4061 | SINGLE-ANCHOR | G22 | DISTRIBUTED |  |  |  |
| #29 | L4 | H10 | 12 | +0.2001 | DISTRIBUTED | S219/C183/F222/F208 | SINGLE-ANCHOR | L74 |  |  |
| #17 | L5 | H7 | 16 | +0.5561 | DISTRIBUTED |  | SINGLE-ANCHOR | L74 |  |  |
| #25 | L5 | H9 | 5 | +0.1930 | SINGLE-ANCHOR | N42 | DUAL-ANCHOR | V47/A48 |  | INTRA:flkL |
| #1 | L5 | H13 | 37 | +0.5331 | DISTRIBUTED | L18/S219/I14/T15/K43 | DISTRIBUTED | L74/V172/V78/V47 |  |  |
| #28 | L5 | H19 | 14 | +0.1113 | MULTI-ANCHOR |  | DISTRIBUTED | C190/V192/L74/L193 |  |  |
| #30 | L6 | H0 | 24 | +0.6384 | DISTRIBUTED | I6/M0/L7/G1/K3 | SINGLE-ANCHOR | L74 |  |  |
| #2 | L7 | H9 | 26 | +0.7801 | DISTRIBUTED |  | SINGLE-ANCHOR | L74 |  |  |
| #23 | L10 | H9 | 6 | +0.2391 | SINGLE-ANCHOR | L193 | DISTRIBUTED | L74/G77/S76 |  |  |
| #11 | L11 | H15 | 5 | +0.2338 | SINGLE-ANCHOR | L193 | SINGLE-ANCHOR | L74 |  |  |
| #5 | L12 | H2 | 18 | +0.4281 | DUAL-ANCHOR | L193/L74 | DISTRIBUTED | L7/I6/G53/G5 |  |  |
| #21 | L12 | H3 | 10 | +0.2635 | SINGLE-ANCHOR | L74 | DISTRIBUTED | V47/T60/G53/T58 |  |  |
| #18 | L12 | H14 | 10 | +0.2741 | SINGLE-ANCHOR | L74 | DISTRIBUTED | ?-1/L7/I6/G5 |  |  |
| #16 | L12 | H15 | 11 | +0.3902 | SINGLE-ANCHOR | L74 | DISTRIBUTED | S57/T61/M64 |  |  |
| #27 | L13 | H1 | 16 | +0.2005 | SINGLE-ANCHOR | L74 | DISTRIBUTED | L7/V47/I6/T58/I52 |  |  |
| #24 | L13 | H8 | 5 | +0.1819 | SINGLE-ANCHOR | L193 | DISTRIBUTED | V78/G77/S76 |  |  |
| #4 | L14 | H9 | 17 | +0.4321 | DUAL-ANCHOR | L193/L74 | DISTRIBUTED | L7/G53/I6/?-1 |  |  |
| #15 | L15 | H18 | 16 | +0.2932 | DISTRIBUTED | V78/I88/G77/S76 | SINGLE-ANCHOR | G53 |  |  |
| #12 | L16 | H4 | 16 | +0.2567 | SINGLE-ANCHOR | L7 | DISTRIBUTED | S57/Y49/T61 |  |  |
| #19 | L16 | H17 | 20 | +0.2540 | DISTRIBUTED | I88/V78/G80/N89 | DUAL-ANCHOR | G53/S57 |  |  |
| #9 | L16 | H19 | 21 | +0.4131 | SINGLE-ANCHOR | L193 | DISTRIBUTED | G53/S63/H56/I65 |  |  |
| #20 | L19 | H14 | 3 | +0.1702 | SINGLE-ANCHOR | G53 | SINGLE-ANCHOR | S57 |  | ss1→flkL |
| #8 | L29 | H18 | 20 | +0.3340 | DISTRIBUTED | F186/V182/K185 | DISTRIBUTED | T62/T58/L66/S178/S63 |  | CROSS:ss1→ss2 |
| #7 | L32 | H13 | 22 | +0.2800 | DISTRIBUTED | F186/T58/V182/S178/T62 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #14 | L32 | H18 | 10 | +0.1120 | DISTRIBUTED | T62/V182/S178/T58 | DISTRIBUTED | T58/F186/V182 | CROSS_SSE | CROSS:ss2→ss1 |
