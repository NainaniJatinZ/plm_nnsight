# Contact Pattern Analysis: 3LEWA

Generated: 2026-03-26 00:45:37   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3LEWA |
| Contact pair | (225, 352) |
| ss1 | [220, 231) |
| ss2 | [347, 358) |
| Clean flank | 57 |
| Corrupt flank | 56 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.5274 |
| Corrupt metric | 0.0099 |
| Gap | 0.5174 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 400 | 78.77% |
| positive IE | 200 | 71.29% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L11 | H16 | +0.9970 |
| 2 | L9 | H16 | +0.4728 |
| 3 | L27 | H15 | +0.4521 |
| 4 | L32 | H13 | +0.3295 |
| 5 | L32 | H18 | +0.3255 |
| 6 | L29 | H18 | +0.2584 |
| 7 | L31 | H17 | +0.1349 |
| 8 | L26 | H16 | +0.1333 |
| 9 | L6 | H14 | +0.1308 |
| 10 | L24 | H18 | +0.1253 |
| 11 | L23 | H15 | +0.0964 |
| 12 | L5 | H8 | +0.0941 |
| 13 | L28 | H4 | +0.0865 |
| 14 | L19 | H0 | +0.0861 |
| 15 | L22 | H16 | +0.0824 |
| 16 | L21 | H6 | +0.0785 |
| 17 | L21 | H11 | +0.0762 |
| 18 | L13 | H14 | +0.0759 |
| 19 | L17 | H2 | +0.0756 |
| 20 | L10 | H16 | +0.0705 |
| 21 | L23 | H2 | +0.0705 |
| 22 | L22 | H11 | +0.0703 |
| 23 | L30 | H13 | +0.0693 |
| 24 | L24 | H11 | +0.0640 |
| 25 | L30 | H1 | +0.0635 |
| 26 | L26 | H1 | +0.0622 |
| 27 | L28 | H8 | +0.0620 |
| 28 | L4 | H9 | +0.0611 |
| 29 | L18 | H14 | +0.0604 |
| 30 | L22 | H3 | +0.0587 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.01% |
| 4 | 0.02% |
| 5 | 0.02% |
| 6 | 0.03% |
| 7 | 0.03% |
| 8 | 0.03% |
| 9 | 0.03% |
| 10 | 0.03% |
| 20 | 0.04% |
| 80 | 0.12% |
| 450 | 169.72% |

## Cell Attribution Analysis

Total cells: 44,749,032

- Positive: 22,599,655
- Negative: 22,141,918

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L9 | H16 | 353 | ss2 | 209 | flkL | +0.203011 | 0.157281 |
| L6 | H14 | 353 | ss2 | 221 | ss1 | +0.100808 | 0.072516 |
| L5 | H8 | 221 | ss1 | 216 | flkL | +0.083461 | 0.030552 |
| L17 | H13 | 364 | flkR | 353 | ss2 | +0.074865 | 0.328564 |
| L11 | H16 | 225 | ss1 | 353 | ss2 | +0.065034 | 0.634100 |
| L0 | H8 | 206 | flkL | 163 | flkL | +0.063480 | 0.093835 |
| L7 | H13 | 353 | ss2 | 353 | ss2 | +0.051355 | 0.106423 |
| L32 | H13 | 226 | ss1 | 352 | ss2 | +0.046275 | 0.359772 |
| L26 | H16 | 221 | ss1 | 355 | ss2 | +0.038914 | 0.427263 |
| L28 | H4 | 226 | ss1 | 229 | ss1 | +0.037275 | 0.434424 |
| L27 | H15 | 348 | ss2 | 225 | ss1 | +0.036860 | 0.528943 |
| L17 | H10 | 352 | ss2 | 353 | ss2 | +0.034296 | 0.852588 |
| L17 | H10 | 348 | ss2 | 353 | ss2 | +0.032383 | 0.530964 |
| L10 | H9 | 353 | ss2 | -1 | other | +0.032271 | 0.077736 |
| L32 | H18 | 351 | ss2 | 225 | ss1 | +0.031719 | 0.184072 |
| L6 | H6 | 209 | flkL | 221 | ss1 | +0.030881 | 0.051468 |
| L16 | H7 | 364 | flkR | 348 | ss2 | +0.029716 | 0.326761 |
| L19 | H0 | 371 | flkR | 364 | flkR | +0.029516 | 0.734440 |
| L13 | H14 | 225 | ss1 | 209 | flkL | +0.028545 | 0.486499 |
| L14 | H0 | 371 | flkR | 353 | ss2 | +0.027937 | 0.494984 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L14 | H0 | 377 | flkR | 353 | ss2 | -0.015307 | 0.529279 |
| L17 | H19 | 345 | other | 348 | ss2 | -0.015443 | 0.744295 |
| L17 | H13 | 365 | flkR | 353 | ss2 | -0.015830 | 0.283058 |
| L11 | H16 | 216 | flkL | 353 | ss2 | -0.015854 | 0.724233 |
| L11 | H16 | 347 | ss2 | 353 | ss2 | -0.016135 | 0.494951 |
| L0 | H8 | 206 | flkL | 206 | flkL | -0.016456 | 0.024325 |
| L19 | H4 | 352 | ss2 | 349 | ss2 | -0.017207 | 0.590816 |
| L11 | H16 | 209 | flkL | 353 | ss2 | -0.018927 | 0.787664 |
| L11 | H16 | 397 | flkR | 353 | ss2 | -0.019595 | 0.770563 |
| L19 | H0 | 404 | flkR | 397 | flkR | -0.020617 | 0.376084 |
| L17 | H7 | 365 | flkR | 353 | ss2 | -0.020823 | 0.642423 |
| L20 | H16 | 229 | ss1 | 228 | ss1 | -0.021024 | 0.751944 |
| L16 | H7 | 221 | ss1 | 353 | ss2 | -0.021984 | 0.445650 |
| L14 | H9 | 348 | ss2 | 352 | ss2 | -0.027147 | 0.493614 |
| L17 | H13 | 377 | flkR | 353 | ss2 | -0.028988 | 0.358406 |
| L19 | H0 | 355 | ss2 | 348 | ss2 | -0.032273 | 0.633096 |
| L17 | H10 | 355 | ss2 | 353 | ss2 | -0.040312 | 0.869629 |
| L14 | H9 | 209 | flkL | 353 | ss2 | -0.041232 | 0.509066 |
| L17 | H13 | 221 | ss1 | 209 | flkL | -0.043613 | 0.631169 |
| L11 | H1 | 353 | ss2 | 353 | ss2 | -0.062176 | 0.555683 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0099 | -0.00% |
| 10 | 10 | 10 | 0.0100 | 0.00% |
| 20 | 20 | 19 | 0.0100 | 0.00% |
| 50 | 50 | 31 | 0.0100 | 0.00% |
| 100 | 100 | 55 | 0.0100 | 0.00% |
| 200 | 200 | 83 | 0.0099 | 0.00% |
| 500 | 500 | 139 | 0.0100 | 0.01% |
| 1000 | 1,000 | 174 | 0.0100 | 0.01% |
| 2000 | 2,000 | 192 | 0.0101 | 0.02% |
| 5000 | 5,000 | 199 | 0.0106 | 0.12% |
| 10000 | 10,000 | 200 | 0.0114 | 0.28% |
| 20000 | 20,000 | 200 | 0.0144 | 0.85% |
| 50000 | 50,000 | 200 | 0.0272 | 3.34% |

## Motif Analysis

### L4 H9 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 2  |  total attr: +0.0212

**Key mass** (top-1=80%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 414 | flkR | +0.0169 | 80.0% |
| -1 | other | +0.0042 | 20.0% |

**Query mass** (top-1=80%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.0169 | 80.0% |
| -1 | other | +0.0042 | 20.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -61 | 1 | 50.0% |
| +0 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 1 | 50.0% |
| other | other | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 353 | ss2 | 414 | flkR | +0.0169 | 0.0095 |
| -1 | other | -1 | other | +0.0042 | 0.0953 |

### L5 H8 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 2  |  total attr: +0.0877

**Key mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 216 | flkL | +0.0835 | 95.1% |
| 360 | flkR | +0.0043 | 4.9% |

**Query mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.0835 | 95.1% |
| 364 | flkR | +0.0043 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 1 | 50.0% |
| +4 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 1 | 50.0% |
| flkR | flkR | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 221 | ss1 | 216 | flkL | +0.0835 | 0.0306 |
| 364 | flkR | 360 | flkR | +0.0043 | 0.0147 |

### L6 H14 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→ss1  |  cells: 4  |  total attr: +0.1131

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.1131 | 100.0% |

**Query mass** (top-1=89%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.1008 | 89.1% |
| 209 | flkL | +0.0062 | 5.5% |
| 352 | ss2 | +0.0032 | 2.8% |
| 351 | ss2 | +0.0029 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +132 | 1 | 25.0% |
| -12 | 1 | 25.0% |
| +131 | 1 | 25.0% |
| +130 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 75.0% |
| flkL | ss1 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 353 | ss2 | 221 | ss1 | +0.1008 | 0.0725 |
| 209 | flkL | 221 | ss1 | +0.0062 | 0.0099 |
| 352 | ss2 | 221 | ss1 | +0.0032 | 0.0789 |
| 351 | ss2 | 221 | ss1 | +0.0029 | 0.0502 |

### L9 H16 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→flkL  |  cells: 2  |  total attr: +0.2168

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | flkL | +0.2168 | 100.0% |

**Query mass** (top-1=94%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.2030 | 93.6% |
| 209 | flkL | +0.0138 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +144 | 1 | 50.0% |
| +0 | 1 | 50.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 1 | 50.0% |
| flkL | flkL | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 353 | ss2 | 209 | flkL | +0.2030 | 0.1573 |
| 209 | flkL | 209 | flkL | +0.0138 | 0.0400 |

### L10 H16 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 4  |  total attr: +0.0296

**Key mass** (top-1=57%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | flkL | +0.0170 | 57.4% |
| 353 | ss2 | +0.0126 | 42.6% |

**Query mass** (top-1=49%, top-2=78%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.0144 | 48.5% |
| 209 | flkL | +0.0086 | 29.0% |
| 225 | ss1 | +0.0066 | 22.4% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +144 | 1 | 25.0% |
| -128 | 1 | 25.0% |
| -144 | 1 | 25.0% |
| +0 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 1 | 25.0% |
| ss1 | ss2 | 1 | 25.0% |
| flkL | ss2 | 1 | 25.0% |
| flkL | flkL | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 353 | ss2 | 209 | flkL | +0.0144 | 0.0295 |
| 225 | ss1 | 353 | ss2 | +0.0066 | 0.0581 |
| 209 | flkL | 353 | ss2 | +0.0060 | 0.0578 |
| 209 | flkL | 209 | flkL | +0.0026 | 0.0314 |

### L11 H16 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 54  |  total attr: +0.5050

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.5016 | 99.3% |
| 209 | flkL | +0.0034 | 0.7% |

**Query mass** (top-1=13%, top-2=18%, top-3=22%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss1 | +0.0650 | 12.9% |
| 356 | ss2 | +0.0244 | 4.8% |
| 352 | ss2 | +0.0232 | 4.6% |
| 360 | flkR | +0.0225 | 4.5% |
| 380 | flkR | +0.0223 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 4%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -128 | 1 | 1.9% |
| +3 | 1 | 1.9% |
| -1 | 1 | 1.9% |
| +7 | 1 | 1.9% |
| +27 | 1 | 1.9% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 21 | 38.9% |
| flkL | ss2 | 18 | 33.3% |
| ss2 | ss2 | 7 | 13.0% |
| ss1 | ss2 | 5 | 9.3% |
| other | ss2 | 2 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | ss1 | 353 | ss2 | +0.0650 | 0.6341 |
| 356 | ss2 | 353 | ss2 | +0.0244 | 0.7116 |
| 352 | ss2 | 353 | ss2 | +0.0232 | 0.7139 |
| 360 | flkR | 353 | ss2 | +0.0225 | 0.7036 |
| 380 | flkR | 353 | ss2 | +0.0223 | 0.7799 |

### L13 H14 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.1036

**Key mass** (top-1=68%, top-2=88%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | flkL | +0.0703 | 67.9% |
| 353 | ss2 | +0.0207 | 20.0% |
| 225 | ss1 | +0.0064 | 6.2% |
| 183 | flkL | +0.0035 | 3.4% |
| 352 | ss2 | +0.0025 | 2.5% |

**Query mass** (top-1=30%, top-2=58%, top-3=74%)  [DISTR(A353/S225/L368)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.0311 | 30.0% |
| 225 | ss1 | +0.0285 | 27.6% |
| 368 | flkR | +0.0174 | 16.8% |
| 228 | ss1 | +0.0088 | 8.5% |
| 371 | flkR | +0.0059 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +16 | 2 | 20.0% |
| +144 | 1 | 10.0% |
| +15 | 1 | 10.0% |
| +19 | 1 | 10.0% |
| +128 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 3 | 30.0% |
| flkR | ss2 | 3 | 30.0% |
| ss2 | flkL | 2 | 20.0% |
| ss2 | ss1 | 1 | 10.0% |
| flkL | flkL | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | ss1 | 209 | flkL | +0.0285 | 0.4865 |
| 353 | ss2 | 209 | flkL | +0.0247 | 0.3201 |
| 368 | flkR | 353 | ss2 | +0.0148 | 0.3409 |
| 228 | ss1 | 209 | flkL | +0.0088 | 0.3250 |
| 353 | ss2 | 225 | ss1 | +0.0064 | 0.0930 |

### L17 H2 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.0895

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.0895 | 100.0% |

**Query mass** (top-1=16%, top-2=27%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 226 | ss1 | +0.0141 | 15.8% |
| 228 | ss1 | +0.0097 | 10.8% |
| 216 | flkL | +0.0084 | 9.3% |
| 221 | ss1 | +0.0075 | 8.4% |
| 222 | ss1 | +0.0058 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -127 | 1 | 5.6% |
| -125 | 1 | 5.6% |
| -137 | 1 | 5.6% |
| -132 | 1 | 5.6% |
| -131 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 7 | 38.9% |
| ss1 | ss2 | 6 | 33.3% |
| ss2 | ss2 | 2 | 11.1% |
| flkR | ss2 | 2 | 11.1% |
| other | ss2 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 226 | ss1 | 353 | ss2 | +0.0141 | 0.5382 |
| 228 | ss1 | 353 | ss2 | +0.0097 | 0.4236 |
| 216 | flkL | 353 | ss2 | +0.0084 | 0.8805 |
| 221 | ss1 | 353 | ss2 | +0.0075 | 0.4871 |
| 222 | ss1 | 353 | ss2 | +0.0058 | 0.6551 |

### L18 H14 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 9  |  total attr: +0.0371

**Key mass** (top-1=64%, top-2=79%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.0239 | 64.4% |
| -1 | other | +0.0054 | 14.5% |
| 360 | flkR | +0.0054 | 14.4% |
| 209 | flkL | +0.0024 | 6.6% |

**Query mass** (top-1=56%, top-2=69%, top-3=79%)  [DISTR(L371/R216/N352)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 371 | flkR | +0.0207 | 55.8% |
| 216 | flkL | +0.0050 | 13.6% |
| 352 | ss2 | +0.0036 | 9.7% |
| 348 | ss2 | +0.0028 | 7.6% |
| 397 | flkR | +0.0025 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 11.1% |
| -1 | 1 | 11.1% |
| -12 | 1 | 11.1% |
| +372 | 1 | 11.1% |
| +217 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 3 | 33.3% |
| ss2 | ss2 | 1 | 11.1% |
| ss2 | flkR | 1 | 11.1% |
| flkR | other | 1 | 11.1% |
| flkL | other | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 371 | flkR | 353 | ss2 | +0.0154 | 0.2675 |
| 352 | ss2 | 353 | ss2 | +0.0036 | 0.3234 |
| 348 | ss2 | 360 | flkR | +0.0028 | 0.0921 |
| 371 | flkR | -1 | other | +0.0028 | 0.1287 |
| 216 | flkL | -1 | other | +0.0026 | 0.3402 |

### L19 H0 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 15  |  total attr: +0.1075

**Key mass** (top-1=27%, top-2=52%, top-3=60%)  [DISTR(A364/A353/D363/A221/N352)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 364 | flkR | +0.0295 | 27.5% |
| 353 | ss2 | +0.0259 | 24.1% |
| 363 | flkR | +0.0090 | 8.4% |
| 221 | ss1 | +0.0083 | 7.7% |
| 352 | ss2 | +0.0078 | 7.3% |

**Query mass** (top-1=39%, top-2=60%, top-3=67%)  [DISTR(L371/N360/I351/K356)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 371 | flkR | +0.0414 | 38.5% |
| 360 | flkR | +0.0229 | 21.3% |
| 351 | ss2 | +0.0078 | 7.2% |
| 356 | ss2 | +0.0071 | 6.6% |
| 225 | ss1 | +0.0062 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 80%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 8 | 53.3% |
| +8 | 4 | 26.7% |
| +2 | 1 | 6.7% |
| +13 | 1 | 6.7% |
| +1 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 3 | 20.0% |
| flkR | ss2 | 3 | 20.0% |
| ss2 | ss2 | 3 | 20.0% |
| ss1 | ss1 | 2 | 13.3% |
| ss1 | flkL | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 371 | flkR | 364 | flkR | +0.0295 | 0.7344 |
| 360 | flkR | 353 | ss2 | +0.0205 | 0.5338 |
| 371 | flkR | 363 | flkR | +0.0090 | 0.1164 |
| 351 | ss2 | 344 | other | +0.0078 | 0.4540 |
| 356 | ss2 | 349 | ss2 | +0.0071 | 0.5660 |

### L21 H6 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 8  |  total attr: +0.0394

**Key mass** (top-1=27%, top-2=51%, top-3=73%)  [DISTR(A353/R216/L228)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 353 | ss2 | +0.0106 | 26.8% |
| 216 | flkL | +0.0096 | 24.2% |
| 228 | ss1 | +0.0085 | 21.5% |
| 209 | flkL | +0.0057 | 14.5% |
| 360 | flkR | +0.0051 | 12.9% |

**Query mass** (top-1=22%, top-2=36%, top-3=50%)  [DISTR(D232/L213/R216/A353/H358)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | other | +0.0085 | 21.5% |
| 213 | flkL | +0.0057 | 14.5% |
| 216 | flkL | +0.0055 | 13.9% |
| 353 | ss2 | +0.0051 | 12.9% |
| 358 | flkR | +0.0044 | 11.1% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 25.0% |
| -7 | 2 | 25.0% |
| +0 | 1 | 12.5% |
| +5 | 1 | 12.5% |
| +6 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 3 | 37.5% |
| flkR | ss2 | 2 | 25.0% |
| other | ss1 | 1 | 12.5% |
| ss2 | flkR | 1 | 12.5% |
| ss2 | ss2 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 232 | other | 228 | ss1 | +0.0085 | 0.4207 |
| 213 | flkL | 209 | flkL | +0.0057 | 0.4871 |
| 216 | flkL | 216 | flkL | +0.0055 | 0.5549 |
| 353 | ss2 | 360 | flkR | +0.0051 | 0.4510 |
| 358 | flkR | 353 | ss2 | +0.0044 | 0.6640 |

### L21 H11 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | POSITIONAL  |  cells: 11  |  total attr: +0.0572

**Key mass** (top-1=46%, top-2=85%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 216 | flkL | +0.0262 | 45.9% |
| 360 | flkR | +0.0226 | 39.5% |
| 355 | ss2 | +0.0043 | 7.4% |
| 371 | flkR | +0.0041 | 7.2% |

**Query mass** (top-1=18%, top-2=30%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 213 | flkL | +0.0102 | 17.7% |
| 359 | flkR | +0.0071 | 12.5% |
| 364 | flkR | +0.0069 | 12.1% |
| 357 | ss2 | +0.0056 | 9.7% |
| 221 | ss1 | +0.0046 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 55%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 4 | 36.4% |
| -3 | 2 | 18.2% |
| -1 | 1 | 9.1% |
| +4 | 1 | 9.1% |
| -2 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 36.4% |
| flkL | flkL | 3 | 27.3% |
| ss1 | flkL | 2 | 18.2% |
| ss2 | flkR | 1 | 9.1% |
| flkR | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 213 | flkL | 216 | flkL | +0.0102 | 0.9124 |
| 359 | flkR | 360 | flkR | +0.0071 | 0.8487 |
| 364 | flkR | 360 | flkR | +0.0069 | 0.7883 |
| 357 | ss2 | 360 | flkR | +0.0056 | 0.8810 |
| 221 | ss1 | 216 | flkL | +0.0046 | 0.8001 |

### L22 H3 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 9  |  total attr: +0.0631

**Key mass** (top-1=31%, top-2=49%, top-3=66%)  [DISTR(L228/L371/L229/A353)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 228 | ss1 | +0.0193 | 30.6% |
| 371 | flkR | +0.0116 | 18.4% |
| 229 | ss1 | +0.0104 | 16.5% |
| 353 | ss2 | +0.0089 | 14.2% |
| 358 | flkR | +0.0050 | 7.9% |

**Query mass** (top-1=25%, top-2=42%, top-3=56%)  [DISTR(S209/K222/A364/A346)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | flkL | +0.0160 | 25.4% |
| 222 | ss1 | +0.0104 | 16.5% |
| 364 | flkR | +0.0091 | 14.4% |
| 346 | other | +0.0089 | 14.2% |
| 351 | ss2 | +0.0050 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 78%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 6 | 66.7% |
| -19 | 1 | 11.1% |
| -8 | 1 | 11.1% |
| -18 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 2 | 22.2% |
| flkR | flkR | 2 | 22.2% |
| ss2 | flkR | 2 | 22.2% |
| flkL | ss1 | 1 | 11.1% |
| other | ss2 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 209 | flkL | 228 | ss1 | +0.0160 | 0.6712 |
| 222 | ss1 | 229 | ss1 | +0.0104 | 0.3578 |
| 364 | flkR | 371 | flkR | +0.0091 | 0.6475 |
| 346 | other | 353 | ss2 | +0.0089 | 0.7605 |
| 351 | ss2 | 358 | flkR | +0.0050 | 0.3687 |

### L22 H11 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 6  |  total attr: +0.0383

**Key mass** (top-1=90%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 360 | flkR | +0.0346 | 90.3% |
| 200 | flkL | +0.0037 | 9.7% |

**Query mass** (top-1=26%, top-2=51%, top-3=67%)  [DISTR(N352/I351/A355/I348)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 352 | ss2 | +0.0100 | 26.2% |
| 351 | ss2 | +0.0095 | 24.9% |
| 355 | ss2 | +0.0063 | 16.4% |
| 348 | ss2 | +0.0060 | 15.6% |
| 225 | ss1 | +0.0037 | 9.7% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 1 | 16.7% |
| -9 | 1 | 16.7% |
| -5 | 1 | 16.7% |
| -12 | 1 | 16.7% |
| +25 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 5 | 83.3% |
| ss1 | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 352 | ss2 | 360 | flkR | +0.0100 | 0.1130 |
| 351 | ss2 | 360 | flkR | +0.0095 | 0.1796 |
| 355 | ss2 | 360 | flkR | +0.0063 | 0.1017 |
| 348 | ss2 | 360 | flkR | +0.0060 | 0.1252 |
| 225 | ss1 | 200 | flkL | +0.0037 | 0.1284 |

### L22 H16 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 10  |  total attr: +0.0719

**Key mass** (top-1=30%, top-2=43%, top-3=56%)  [DISTR(S225/K222/A221/V345/I393)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss1 | +0.0213 | 29.6% |
| 222 | ss1 | +0.0098 | 13.7% |
| 221 | ss1 | +0.0089 | 12.4% |
| 345 | other | +0.0085 | 11.8% |
| 393 | flkR | +0.0083 | 11.5% |

**Query mass** (top-1=30%, top-2=44%, top-3=56%)  [DISTR(L229/D226/S225/I348/I351)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss1 | +0.0218 | 30.3% |
| 226 | ss1 | +0.0098 | 13.7% |
| 225 | ss1 | +0.0089 | 12.4% |
| 348 | ss2 | +0.0085 | 11.8% |
| 351 | ss2 | +0.0053 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 6 | 60.0% |
| +4 | 4 | 40.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 50.0% |
| ss2 | ss2 | 2 | 20.0% |
| flkR | flkR | 2 | 20.0% |
| ss2 | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 229 | ss1 | 225 | ss1 | +0.0173 | 0.5826 |
| 226 | ss1 | 222 | ss1 | +0.0098 | 0.3890 |
| 225 | ss1 | 221 | ss1 | +0.0089 | 0.1568 |
| 348 | ss2 | 345 | other | +0.0085 | 0.3855 |
| 351 | ss2 | 348 | ss2 | +0.0053 | 0.6190 |

### L23 H2 — Rank #21

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | ss1→flkL  |  cells: 11  |  total attr: +0.0544

**Key mass** (top-1=26%, top-2=39%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | flkL | +0.0142 | 26.1% |
| 197 | flkL | +0.0069 | 12.6% |
| 347 | ss2 | +0.0062 | 11.4% |
| 371 | flkR | +0.0059 | 10.9% |
| 364 | flkR | +0.0046 | 8.4% |

**Query mass** (top-1=18%, top-2=35%, top-3=49%)  [DISTR(I348/A221/S225/I351/A346)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 348 | ss2 | +0.0098 | 18.0% |
| 221 | ss1 | +0.0090 | 16.6% |
| 225 | ss1 | +0.0078 | 14.4% |
| 351 | ss2 | +0.0062 | 11.4% |
| 346 | other | +0.0059 | 10.9% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +12 | 1 | 9.1% |
| +151 | 1 | 9.1% |
| +4 | 1 | 9.1% |
| -25 | 1 | 9.1% |
| +16 | 1 | 9.1% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 5 | 45.5% |
| ss2 | flkR | 2 | 18.2% |
| ss2 | flkL | 1 | 9.1% |
| ss2 | ss2 | 1 | 9.1% |
| other | flkR | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 221 | ss1 | 209 | flkL | +0.0090 | 0.5737 |
| 348 | ss2 | 197 | flkL | +0.0069 | 0.1462 |
| 351 | ss2 | 347 | ss2 | +0.0062 | 0.1654 |
| 346 | other | 371 | flkR | +0.0059 | 0.8309 |
| 225 | ss1 | 209 | flkL | +0.0051 | 0.2372 |

### L23 H15 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | CROSS:ss1→ss2  |  cells: 5  |  total attr: +0.0487

**Key mass** (top-1=91%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 348 | ss2 | +0.0442 | 90.8% |
| 352 | ss2 | +0.0045 | 9.2% |

**Query mass** (top-1=36%, top-2=65%, top-3=87%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss1 | +0.0175 | 35.9% |
| 225 | ss1 | +0.0144 | 29.5% |
| 222 | ss1 | +0.0105 | 21.6% |
| 226 | ss1 | +0.0063 | 13.0% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -123 | 2 | 40.0% |
| -119 | 1 | 20.0% |
| -126 | 1 | 20.0% |
| -122 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | ss1 | 348 | ss2 | +0.0144 | 0.2705 |
| 229 | ss1 | 348 | ss2 | +0.0130 | 0.3068 |
| 222 | ss1 | 348 | ss2 | +0.0105 | 0.1145 |
| 226 | ss1 | 348 | ss2 | +0.0063 | 0.1982 |
| 229 | ss1 | 352 | ss2 | +0.0045 | 0.1812 |

### L24 H11 — Rank #24

**Tags:** k:MULTI-ANCHOR / q:DUAL-ANCHOR | INTRA:ss2  |  cells: 4  |  total attr: +0.0142

**Key mass** (top-1=38%, top-2=66%, top-3=83%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 355 | ss2 | +0.0053 | 37.6% |
| 346 | other | +0.0040 | 28.1% |
| 353 | ss2 | +0.0025 | 17.3% |
| 345 | other | +0.0024 | 16.9% |

**Query mass** (top-1=55%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 352 | ss2 | +0.0078 | 54.9% |
| 348 | ss2 | +0.0064 | 45.1% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 1 | 25.0% |
| +2 | 1 | 25.0% |
| -1 | 1 | 25.0% |
| +3 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 2 | 50.0% |
| ss2 | other | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 352 | ss2 | 355 | ss2 | +0.0053 | 0.1002 |
| 348 | ss2 | 346 | other | +0.0040 | 0.1563 |
| 352 | ss2 | 353 | ss2 | +0.0025 | 0.0476 |
| 348 | ss2 | 345 | other | +0.0024 | 0.1681 |

### L24 H18 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 3  |  total attr: +0.0202

**Key mass** (top-1=85%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 355 | ss2 | +0.0171 | 84.8% |
| 348 | ss2 | +0.0031 | 15.2% |

**Query mass** (top-1=46%, top-2=85%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.0094 | 46.4% |
| 225 | ss1 | +0.0077 | 38.3% |
| 229 | ss1 | +0.0031 | 15.2% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -134 | 1 | 33.3% |
| -130 | 1 | 33.3% |
| -119 | 1 | 33.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 221 | ss1 | 355 | ss2 | +0.0094 | 0.1112 |
| 225 | ss1 | 355 | ss2 | +0.0077 | 0.1803 |
| 229 | ss1 | 348 | ss2 | +0.0031 | 0.0717 |

### L26 H1 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 5  |  total attr: +0.0207

**Key mass** (top-1=72%, top-2=87%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 397 | flkR | +0.0149 | 71.9% |
| 367 | flkR | +0.0031 | 14.8% |
| 220 | ss1 | +0.0027 | 13.2% |

**Query mass** (top-1=46%, top-2=61%, top-3=75%)  [DISTR(I351/I348/S225)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 351 | ss2 | +0.0096 | 46.5% |
| 348 | ss2 | +0.0031 | 14.8% |
| 225 | ss1 | +0.0027 | 13.2% |
| 355 | ss2 | +0.0027 | 13.2% |
| 352 | ss2 | +0.0025 | 12.3% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -46 | 1 | 20.0% |
| -19 | 1 | 20.0% |
| +5 | 1 | 20.0% |
| -42 | 1 | 20.0% |
| -45 | 1 | 20.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 80.0% |
| ss1 | ss1 | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 351 | ss2 | 397 | flkR | +0.0096 | 0.3770 |
| 348 | ss2 | 367 | flkR | +0.0031 | 0.2103 |
| 225 | ss1 | 220 | ss1 | +0.0027 | 0.1906 |
| 355 | ss2 | 397 | flkR | +0.0027 | 0.1340 |
| 352 | ss2 | 397 | flkR | +0.0025 | 0.0758 |

### L26 H16 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.1104

**Key mass** (top-1=35%, top-2=54%, top-3=71%)  [DISTR(A355/K356/S225)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 355 | ss2 | +0.0389 | 35.3% |
| 356 | ss2 | +0.0202 | 18.3% |
| 225 | ss1 | +0.0193 | 17.5% |
| 352 | ss2 | +0.0127 | 11.5% |
| 348 | ss2 | +0.0115 | 10.4% |

**Query mass** (top-1=37%, top-2=52%, top-3=62%)  [DISTR(A221/K222/L228/D226)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 221 | ss1 | +0.0413 | 37.5% |
| 222 | ss1 | +0.0158 | 14.3% |
| 228 | ss1 | +0.0115 | 10.4% |
| 226 | ss1 | +0.0092 | 8.3% |
| 209 | flkL | +0.0085 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -134 | 2 | 18.2% |
| -120 | 1 | 9.1% |
| -16 | 1 | 9.1% |
| +0 | 1 | 9.1% |
| -123 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 54.5% |
| ss1 | ss1 | 2 | 18.2% |
| flkL | ss1 | 1 | 9.1% |
| ss2 | flkR | 1 | 9.1% |
| ss2 | ss1 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 221 | ss1 | 355 | ss2 | +0.0389 | 0.4273 |
| 222 | ss1 | 356 | ss2 | +0.0158 | 0.1866 |
| 228 | ss1 | 348 | ss2 | +0.0115 | 0.1758 |
| 209 | flkL | 225 | ss1 | +0.0085 | 0.8490 |
| 225 | ss1 | 225 | ss1 | +0.0084 | 0.1886 |

### L27 H15 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.1924

**Key mass** (top-1=35%, top-2=49%, top-3=61%)  [DISTR(S225/K222/I348/L205)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss1 | +0.0675 | 35.1% |
| 222 | ss1 | +0.0274 | 14.3% |
| 348 | ss2 | +0.0215 | 11.2% |
| 205 | flkL | +0.0214 | 11.1% |
| 209 | flkL | +0.0211 | 10.9% |

**Query mass** (top-1=19%, top-2=33%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 348 | ss2 | +0.0369 | 19.2% |
| 352 | ss2 | +0.0262 | 13.6% |
| 356 | ss2 | +0.0220 | 11.4% |
| 229 | ss1 | +0.0215 | 11.2% |
| 225 | ss1 | +0.0211 | 10.9% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +123 | 1 | 6.7% |
| +127 | 1 | 6.7% |
| +134 | 1 | 6.7% |
| -119 | 1 | 6.7% |
| +16 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 33.3% |
| ss1 | ss2 | 4 | 26.7% |
| ss1 | flkL | 4 | 26.7% |
| ss2 | flkR | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 348 | ss2 | 225 | ss1 | +0.0369 | 0.5289 |
| 352 | ss2 | 225 | ss1 | +0.0262 | 0.9248 |
| 356 | ss2 | 222 | ss1 | +0.0220 | 0.2085 |
| 229 | ss1 | 348 | ss2 | +0.0215 | 0.3271 |
| 225 | ss1 | 209 | flkL | +0.0211 | 0.9278 |

### L28 H4 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss1  |  cells: 15  |  total attr: +0.1234

**Key mass** (top-1=37%, top-2=49%, top-3=61%)  [DISTR(L229/Y224/S225/N352/K222)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss1 | +0.0459 | 37.2% |
| 224 | ss1 | +0.0152 | 12.3% |
| 225 | ss1 | +0.0138 | 11.2% |
| 352 | ss2 | +0.0104 | 8.4% |
| 222 | ss1 | +0.0096 | 7.8% |

**Query mass** (top-1=30%, top-2=44%, top-3=56%)  [DISTR(D226/L228/L229/A221/S225)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 226 | ss1 | +0.0373 | 30.2% |
| 228 | ss1 | +0.0169 | 13.7% |
| 229 | ss1 | +0.0155 | 12.6% |
| 221 | ss1 | +0.0149 | 12.1% |
| 225 | ss1 | +0.0132 | 10.7% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 3 | 20.0% |
| -4 | 3 | 20.0% |
| +4 | 2 | 13.3% |
| +3 | 2 | 13.3% |
| +22 | 1 | 6.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 53.3% |
| ss1 | flkL | 4 | 26.7% |
| ss2 | ss2 | 1 | 6.7% |
| flkL | ss1 | 1 | 6.7% |
| ss2 | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 226 | ss1 | 229 | ss1 | +0.0373 | 0.4344 |
| 229 | ss1 | 225 | ss1 | +0.0108 | 0.3577 |
| 348 | ss2 | 352 | ss2 | +0.0104 | 0.1198 |
| 219 | flkL | 222 | ss1 | +0.0096 | 0.6274 |
| 221 | ss1 | 218 | flkL | +0.0093 | 0.1714 |

### L28 H8 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 11  |  total attr: +0.0616

**Key mass** (top-1=48%, top-2=67%, top-3=76%)  [DISTR(L229/L213/S209)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss1 | +0.0297 | 48.2% |
| 213 | flkL | +0.0117 | 18.9% |
| 209 | flkL | +0.0057 | 9.3% |
| 218 | flkL | +0.0035 | 5.7% |
| 361 | flkR | +0.0030 | 4.9% |

**Query mass** (top-1=27%, top-2=47%, top-3=64%)  [DISTR(D226/K222/L229/S225)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 226 | ss1 | +0.0163 | 26.5% |
| 222 | ss1 | +0.0125 | 20.2% |
| 229 | ss1 | +0.0106 | 17.2% |
| 225 | ss1 | +0.0085 | 13.8% |
| 352 | ss2 | +0.0030 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 18.2% |
| -3 | 1 | 9.1% |
| +9 | 1 | 9.1% |
| +16 | 1 | 9.1% |
| +4 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 36.4% |
| ss1 | ss1 | 3 | 27.3% |
| ss2 | flkR | 3 | 27.3% |
| ss2 | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 226 | ss1 | 229 | ss1 | +0.0163 | 0.2228 |
| 229 | ss1 | 229 | ss1 | +0.0106 | 0.2089 |
| 222 | ss1 | 213 | flkL | +0.0089 | 0.2377 |
| 225 | ss1 | 209 | flkL | +0.0057 | 0.3090 |
| 222 | ss1 | 218 | flkL | +0.0035 | 0.1391 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.1809

**Key mass** (top-1=14%, top-2=28%, top-3=35%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 209 | flkL | +0.0262 | 14.5% |
| 352 | ss2 | +0.0243 | 13.4% |
| 225 | ss1 | +0.0119 | 6.6% |
| 218 | flkL | +0.0113 | 6.3% |
| 363 | flkR | +0.0112 | 6.2% |

**Query mass** (top-1=18%, top-2=32%, top-3=46%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 352 | ss2 | +0.0323 | 17.9% |
| 225 | ss1 | +0.0263 | 14.5% |
| 226 | ss1 | +0.0240 | 13.3% |
| 355 | ss2 | +0.0209 | 11.6% |
| 348 | ss2 | +0.0208 | 11.5% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -140 | 2 | 8.3% |
| +16 | 1 | 4.2% |
| -126 | 1 | 4.2% |
| +127 | 1 | 4.2% |
| -7 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 25.0% |
| ss1 | ss2 | 5 | 20.8% |
| ss2 | flkR | 3 | 12.5% |
| ss1 | flkL | 2 | 8.3% |
| flkL | flkR | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 225 | ss1 | 209 | flkL | +0.0218 | 0.2607 |
| 226 | ss1 | 352 | ss2 | +0.0210 | 0.1409 |
| 352 | ss2 | 225 | ss1 | +0.0119 | 0.1310 |
| 356 | ss2 | 363 | flkR | +0.0112 | 0.4735 |
| 355 | ss2 | 221 | ss1 | +0.0108 | 0.1481 |

### L30 H1 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 2  |  total attr: +0.0080

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 348 | ss2 | +0.0080 | 100.0% |

**Query mass** (top-1=61%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 228 | ss1 | +0.0049 | 60.9% |
| 229 | ss1 | +0.0031 | 39.1% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -120 | 1 | 50.0% |
| -119 | 1 | 50.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 228 | ss1 | 348 | ss2 | +0.0049 | 0.0738 |
| 229 | ss1 | 348 | ss2 | +0.0031 | 0.0890 |

### L30 H13 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 3  |  total attr: +0.0142

**Key mass** (top-1=39%, top-2=78%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss1 | +0.0056 | 39.3% |
| 213 | flkL | +0.0054 | 38.3% |
| 352 | ss2 | +0.0032 | 22.5% |

**Query mass** (top-1=39%, top-2=78%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 352 | ss2 | +0.0056 | 39.3% |
| 351 | ss2 | +0.0054 | 38.3% |
| 367 | flkR | +0.0032 | 22.5% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +123 | 1 | 33.3% |
| +138 | 1 | 33.3% |
| +15 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 1 | 33.3% |
| ss2 | flkL | 1 | 33.3% |
| flkR | ss2 | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 352 | ss2 | 229 | ss1 | +0.0056 | 0.1190 |
| 351 | ss2 | 213 | flkL | +0.0054 | 0.1422 |
| 367 | flkR | 352 | ss2 | +0.0032 | 0.5627 |

### L31 H17 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 12  |  total attr: +0.0791

**Key mass** (top-1=72%, top-2=89%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0571 | 72.2% |
| 352 | ss2 | +0.0131 | 16.5% |
| 356 | ss2 | +0.0059 | 7.5% |
| 495 | other | +0.0030 | 3.8% |

**Query mass** (top-1=25%, top-2=42%, top-3=55%)  [DISTR(A355/N352/K367/D226/S225)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 355 | ss2 | +0.0197 | 24.9% |
| 352 | ss2 | +0.0133 | 16.8% |
| 367 | flkR | +0.0109 | 13.7% |
| 226 | ss1 | +0.0106 | 13.4% |
| 225 | ss1 | +0.0059 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +356 | 1 | 8.3% |
| +353 | 1 | 8.3% |
| +227 | 1 | 8.3% |
| +15 | 1 | 8.3% |
| +226 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 4 | 33.3% |
| ss1 | other | 3 | 25.0% |
| flkR | ss2 | 2 | 16.7% |
| ss1 | ss2 | 2 | 16.7% |
| other | other | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 355 | ss2 | -1 | other | +0.0167 | 0.2532 |
| 352 | ss2 | -1 | other | +0.0133 | 0.1087 |
| 226 | ss1 | -1 | other | +0.0106 | 0.2550 |
| 367 | flkR | 352 | ss2 | +0.0081 | 0.3027 |
| 225 | ss1 | -1 | other | +0.0059 | 0.0834 |

### L32 H13 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 18  |  total attr: +0.1823

**Key mass** (top-1=30%, top-2=40%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 352 | ss2 | +0.0542 | 29.7% |
| 225 | ss1 | +0.0190 | 10.4% |
| 355 | ss2 | +0.0179 | 9.8% |
| 356 | ss2 | +0.0167 | 9.2% |
| 226 | ss1 | +0.0161 | 8.8% |

**Query mass** (top-1=29%, top-2=41%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 226 | ss1 | +0.0525 | 28.8% |
| 352 | ss2 | +0.0221 | 12.1% |
| 348 | ss2 | +0.0183 | 10.1% |
| 355 | ss2 | +0.0158 | 8.7% |
| 221 | ss1 | +0.0153 | 8.4% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -126 | 2 | 11.1% |
| +126 | 2 | 11.1% |
| +134 | 2 | 11.1% |
| -134 | 2 | 11.1% |
| +123 | 2 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 10 | 55.6% |
| ss2 | ss1 | 8 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 226 | ss1 | 352 | ss2 | +0.0463 | 0.3598 |
| 352 | ss2 | 226 | ss1 | +0.0161 | 0.1249 |
| 355 | ss2 | 221 | ss1 | +0.0158 | 0.1212 |
| 221 | ss1 | 355 | ss2 | +0.0153 | 0.1172 |
| 222 | ss1 | 356 | ss2 | +0.0104 | 0.0898 |

### L32 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 13  |  total attr: +0.1212

**Key mass** (top-1=39%, top-2=61%, top-3=72%)  [DISTR(S225/A355/N352)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 225 | ss1 | +0.0478 | 39.4% |
| 355 | ss2 | +0.0260 | 21.4% |
| 352 | ss2 | +0.0132 | 10.9% |
| 351 | ss2 | +0.0128 | 10.5% |
| 229 | ss1 | +0.0100 | 8.2% |

**Query mass** (top-1=26%, top-2=41%, top-3=55%)  [DISTR(I351/K222/I348/S225/A355)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 351 | ss2 | +0.0317 | 26.2% |
| 222 | ss1 | +0.0175 | 14.4% |
| 348 | ss2 | +0.0173 | 14.3% |
| 225 | ss1 | +0.0128 | 10.5% |
| 355 | ss2 | +0.0125 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -126 | 2 | 15.4% |
| +123 | 2 | 15.4% |
| +126 | 1 | 7.7% |
| -133 | 1 | 7.7% |
| -134 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 53.8% |
| ss1 | ss2 | 6 | 46.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 351 | ss2 | 225 | ss1 | +0.0317 | 0.1841 |
| 222 | ss1 | 355 | ss2 | +0.0175 | 0.2266 |
| 225 | ss1 | 351 | ss2 | +0.0128 | 0.0741 |
| 348 | ss2 | 225 | ss1 | +0.0118 | 0.0715 |
| 221 | ss1 | 355 | ss2 | +0.0085 | 0.0398 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #28 | L4 | H9 | 2 | +0.0212 | SINGLE-ANCHOR | N414 | SINGLE-ANCHOR | A353 |  | ss2→flkR |
| #12 | L5 | H8 | 2 | +0.0877 | SINGLE-ANCHOR | R216 | SINGLE-ANCHOR | A221 |  | ss1→flkL |
| #9 | L6 | H14 | 4 | +0.1131 | SINGLE-ANCHOR | A221 | SINGLE-ANCHOR | A353 |  | CROSS:ss2→ss1 |
| #2 | L9 | H16 | 2 | +0.2168 | SINGLE-ANCHOR | S209 | SINGLE-ANCHOR | A353 |  | CROSS:ss2→flkL |
| #20 | L10 | H16 | 4 | +0.0296 | DUAL-ANCHOR | S209/A353 | DUAL-ANCHOR | A353/S209 |  |  |
| #1 | L11 | H16 | 54 | +0.5050 | SINGLE-ANCHOR | A353 | DISTRIBUTED |  |  |  |
| #18 | L13 | H14 | 10 | +0.1036 | SINGLE-ANCHOR | S209 | DISTRIBUTED | A353/S225/L368 |  |  |
| #19 | L17 | H2 | 18 | +0.0895 | SINGLE-ANCHOR | A353 | DISTRIBUTED |  |  |  |
| #29 | L18 | H14 | 9 | +0.0371 | SINGLE-ANCHOR | A353 | DISTRIBUTED | L371/R216/N352 |  |  |
| #14 | L19 | H0 | 15 | +0.1075 | DISTRIBUTED | A364/A353/D363/A221/N352 | DISTRIBUTED | L371/N360/I351/K356 | POSITIONAL |  |
| #16 | L21 | H6 | 8 | +0.0394 | DISTRIBUTED | A353/R216/L228 | DISTRIBUTED | D232/L213/R216/A353/H358 | POSITIONAL |  |
| #17 | L21 | H11 | 11 | +0.0572 | DUAL-ANCHOR | R216/N360 | DISTRIBUTED |  | POSITIONAL |  |
| #30 | L22 | H3 | 9 | +0.0631 | DISTRIBUTED | L228/L371/L229/A353 | DISTRIBUTED | S209/K222/A364/A346 | POSITIONAL |  |
| #22 | L22 | H11 | 6 | +0.0383 | SINGLE-ANCHOR | N360 | DISTRIBUTED | N352/I351/A355/I348 |  | ss2→flkR |
| #15 | L22 | H16 | 10 | +0.0719 | DISTRIBUTED | S225/K222/A221/V345/I393 | DISTRIBUTED | L229/D226/S225/I348/I351 | POSITIONAL | INTRA:ss1 |
| #21 | L23 | H2 | 11 | +0.0544 | DISTRIBUTED |  | DISTRIBUTED | I348/A221/S225/I351/A346 |  | ss1→flkL |
| #11 | L23 | H15 | 5 | +0.0487 | SINGLE-ANCHOR | I348 | MULTI-ANCHOR |  |  | CROSS:ss1→ss2 |
| #24 | L24 | H11 | 4 | +0.0142 | MULTI-ANCHOR |  | DUAL-ANCHOR | N352/I348 |  | INTRA:ss2 |
| #10 | L24 | H18 | 3 | +0.0202 | SINGLE-ANCHOR | A355 | DUAL-ANCHOR | A221/S225 |  | CROSS:ss1→ss2 |
| #26 | L26 | H1 | 5 | +0.0207 | SINGLE-ANCHOR | R397 | DISTRIBUTED | I351/I348/S225 |  | ss2→flkR |
| #8 | L26 | H16 | 11 | +0.1104 | DISTRIBUTED | A355/K356/S225 | DISTRIBUTED | A221/K222/L228/D226 |  | CROSS:ss1→ss2 |
| #3 | L27 | H15 | 15 | +0.1924 | DISTRIBUTED | S225/K222/I348/L205 | DISTRIBUTED |  |  |  |
| #13 | L28 | H4 | 15 | +0.1234 | DISTRIBUTED | L229/Y224/S225/N352/K222 | DISTRIBUTED | D226/L228/L229/A221/S225 |  | INTRA:ss1 |
| #27 | L28 | H8 | 11 | +0.0616 | DISTRIBUTED | L229/L213/S209 | DISTRIBUTED | D226/K222/L229/S225 |  |  |
| #6 | L29 | H18 | 24 | +0.1809 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #25 | L30 | H1 | 2 | +0.0080 | SINGLE-ANCHOR | I348 | SINGLE-ANCHOR | L228 |  | CROSS:ss1→ss2 |
| #23 | L30 | H13 | 3 | +0.0142 | DUAL-ANCHOR | L229/L213 | DUAL-ANCHOR | N352/I351 |  |  |
| #7 | L31 | H17 | 12 | +0.0791 | SINGLE-ANCHOR | ?-1 | DISTRIBUTED | A355/N352/K367/D226/S225 |  |  |
| #4 | L32 | H13 | 18 | +0.1823 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #5 | L32 | H18 | 13 | +0.1212 | DISTRIBUTED | S225/A355/N352 | DISTRIBUTED | I351/K222/I348/S225/A355 |  | CROSS:ss2→ss1 |
