# Contact Pattern Analysis: 3CSSA

Generated: 2026-03-22 21:46:17   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 3CSSA |
| Contact pair | (41, 159) |
| ss1 | [36, 47) |
| ss2 | [154, 165) |
| Clean flank | 35 |
| Corrupt flank | 34 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.9002 |
| Corrupt metric | 0.0082 |
| Gap | 0.8920 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 400 | 80.45% |
| positive IE | 110 | 70.64% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L8 | H12 | +0.9993 |
| 2 | L7 | H9 | +0.9985 |
| 3 | L10 | H9 | +0.9974 |
| 4 | L5 | H12 | +0.8778 |
| 5 | L11 | H14 | +0.4862 |
| 6 | L32 | H18 | +0.3437 |
| 7 | L11 | H16 | +0.3209 |
| 8 | L29 | H18 | +0.1667 |
| 9 | L32 | H13 | +0.1649 |
| 10 | L0 | H11 | +0.1556 |
| 11 | L27 | H15 | +0.1390 |
| 12 | L13 | H2 | +0.1223 |
| 13 | L11 | H9 | +0.1171 |
| 14 | L0 | H3 | +0.1149 |
| 15 | L13 | H8 | +0.1099 |
| 16 | L5 | H7 | +0.1082 |
| 17 | L6 | H7 | +0.1062 |
| 18 | L16 | H7 | +0.1022 |
| 19 | L26 | H16 | +0.0980 |
| 20 | L9 | H8 | +0.0946 |
| 21 | L22 | H14 | +0.0914 |
| 22 | L14 | H9 | +0.0913 |
| 23 | L15 | H1 | +0.0884 |
| 24 | L9 | H13 | +0.0862 |
| 25 | L3 | H4 | +0.0855 |
| 26 | L30 | H1 | +0.0828 |
| 27 | L11 | H18 | +0.0799 |
| 28 | L0 | H9 | +0.0794 |
| 29 | L16 | H19 | +0.0775 |
| 30 | L21 | H4 | +0.0772 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.01% |
| 2 | 0.02% |
| 3 | 0.02% |
| 4 | 0.03% |
| 5 | 0.03% |
| 6 | 0.04% |
| 7 | 0.04% |
| 8 | 0.04% |
| 9 | 0.04% |
| 10 | 0.05% |
| 20 | 0.07% |
| 80 | 18.22% |
| 450 | 129.79% |

## Cell Attribution Analysis

Total cells: 7,582,221

- Positive: 3,917,837
- Negative: 3,662,242

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000122 | 758,223 |
| 95th | +0.00000390 | 379,112 |
| 99th | +0.00003248 | 75,823 |
| 99.5th | +0.00007136 | 37,912 |
| 99.9th | +0.00040013 | 7,583 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H9 | 158 | ss2 | 40 | ss1 | +0.622866 | 0.299176 |
| L5 | H12 | 158 | ss2 | 165 | flkR | +0.426284 | 0.045313 |
| L8 | H12 | 40 | ss1 | 158 | ss2 | +0.333725 | 0.578577 |
| L10 | H9 | 158 | ss2 | 40 | ss1 | +0.321660 | 0.721204 |
| L11 | H14 | 199 | flkR | 158 | ss2 | +0.216599 | 0.575906 |
| L11 | H14 | 198 | flkR | 158 | ss2 | +0.186691 | 0.681082 |
| L11 | H14 | 41 | ss1 | 158 | ss2 | +0.136602 | 0.736619 |
| L6 | H7 | 40 | ss1 | 158 | ss2 | +0.134803 | 0.062936 |
| L11 | H16 | 158 | ss2 | 40 | ss1 | +0.107236 | 0.415604 |
| L15 | H1 | 158 | ss2 | 44 | ss1 | +0.102901 | 0.841752 |
| L15 | H4 | 158 | ss2 | 44 | ss1 | +0.091462 | 0.917724 |
| L9 | H4 | 158 | ss2 | 158 | ss2 | +0.090197 | 0.269430 |
| L8 | H12 | 199 | flkR | 158 | ss2 | +0.089291 | 0.287198 |
| L0 | H9 | 167 | flkR | 199 | flkR | +0.086632 | 0.007572 |
| L14 | H13 | 42 | ss1 | 44 | ss1 | +0.084484 | 0.725753 |
| L21 | H13 | 157 | ss2 | 158 | ss2 | +0.077076 | 0.670851 |
| L11 | H9 | 158 | ss2 | 158 | ss2 | +0.074943 | 0.445581 |
| L11 | H13 | 161 | ss2 | 158 | ss2 | +0.072606 | 0.793115 |
| L8 | H12 | 198 | flkR | 158 | ss2 | +0.069473 | 0.330916 |
| L21 | H13 | 41 | ss1 | 40 | ss1 | +0.069078 | 0.675243 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L16 | H6 | 39 | ss1 | 158 | ss2 | -0.030425 | 0.873171 |
| L1 | H1 | 158 | ss2 | 161 | ss2 | -0.030538 | 0.010517 |
| L14 | H13 | 44 | ss1 | 45 | ss1 | -0.030594 | 0.127486 |
| L13 | H2 | 157 | ss2 | 158 | ss2 | -0.030793 | 0.719483 |
| L13 | H8 | 43 | ss1 | 158 | ss2 | -0.038840 | 0.544676 |
| L16 | H7 | 44 | ss1 | 44 | ss1 | -0.041860 | 0.794057 |
| L14 | H13 | 43 | ss1 | 44 | ss1 | -0.043283 | 0.608798 |
| L19 | H3 | 41 | ss1 | 44 | ss1 | -0.043297 | 0.718565 |
| L14 | H13 | 39 | ss1 | 44 | ss1 | -0.043464 | 0.535601 |
| L29 | H18 | 155 | ss2 | 39 | ss1 | -0.044459 | 0.469757 |
| L15 | H1 | 267 | other | 44 | ss1 | -0.045526 | 0.819404 |
| L14 | H9 | 44 | ss1 | 158 | ss2 | -0.045726 | 0.807862 |
| L16 | H7 | 157 | ss2 | 44 | ss1 | -0.045949 | 0.603249 |
| L16 | H7 | 38 | ss1 | 44 | ss1 | -0.046330 | 0.940700 |
| L16 | H7 | 39 | ss1 | 44 | ss1 | -0.047404 | 0.971364 |
| L15 | H4 | 161 | ss2 | 44 | ss1 | -0.048620 | 0.852757 |
| L17 | H8 | 41 | ss1 | 44 | ss1 | -0.062459 | 0.766554 |
| L14 | H13 | 40 | ss1 | 44 | ss1 | -0.064271 | 0.767597 |
| L1 | H8 | 158 | ss2 | 162 | ss2 | -0.080331 | 0.027703 |
| L14 | H13 | 44 | ss1 | 44 | ss1 | -0.190973 | 0.637648 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0082 | 0.00% |
| 10 | 10 | 8 | 0.0082 | 0.00% |
| 20 | 20 | 15 | 0.0082 | 0.00% |
| 50 | 50 | 37 | 0.0087 | 0.06% |
| 100 | 100 | 59 | 0.0088 | 0.06% |
| 200 | 200 | 82 | 0.0090 | 0.08% |
| 500 | 500 | 100 | 0.0093 | 0.12% |
| 1000 | 1,000 | 108 | 0.0096 | 0.15% |
| 2000 | 2,000 | 109 | 0.0160 | 0.87% |
| 5000 | 5,000 | 110 | 0.0226 | 1.61% |
| 10000 | 10,000 | 110 | 0.0317 | 2.63% |
| 20000 | 20,000 | 110 | 0.0520 | 4.91% |
| 50000 | 50,000 | 110 | 0.1889 | 20.26% |

## Motif Analysis

### L0 H3 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss2→flkR  |  cells: 15  |  total attr: +0.1271

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | flkR | +0.1271 | 100.0% |

**Query mass** (top-1=17%, top-2=32%, top-3=41%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 167 | flkR | +0.0211 | 16.6% |
| 158 | ss2 | +0.0191 | 15.0% |
| 161 | ss2 | +0.0115 | 9.0% |
| 155 | ss2 | +0.0102 | 8.0% |
| 156 | ss2 | +0.0094 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -32 | 1 | 6.7% |
| -41 | 1 | 6.7% |
| -38 | 1 | 6.7% |
| -44 | 1 | 6.7% |
| -43 | 1 | 6.7% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 8 | 53.3% |
| flkR | flkR | 4 | 26.7% |
| ss1 | flkR | 2 | 13.3% |
| other | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 167 | flkR | 199 | flkR | +0.0211 | 0.0038 |
| 158 | ss2 | 199 | flkR | +0.0191 | 0.0063 |
| 161 | ss2 | 199 | flkR | +0.0115 | 0.0050 |
| 155 | ss2 | 199 | flkR | +0.0102 | 0.0063 |
| 156 | ss2 | 199 | flkR | +0.0094 | 0.0055 |

### L0 H9 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 22  |  total attr: +0.2351

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | flkR | +0.2321 | 98.7% |
| 1 | flkL | +0.0030 | 1.3% |

**Query mass** (top-1=37%, top-2=46%, top-3=54%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 167 | flkR | +0.0866 | 36.8% |
| 171 | flkR | +0.0209 | 8.9% |
| 172 | flkR | +0.0193 | 8.2% |
| 168 | flkR | +0.0111 | 4.7% |
| 159 | ss2 | +0.0094 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -32 | 1 | 4.5% |
| -28 | 1 | 4.5% |
| -27 | 1 | 4.5% |
| -31 | 1 | 4.5% |
| -40 | 1 | 4.5% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=68%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 15 | 68.2% |
| ss2 | flkR | 3 | 13.6% |
| other | flkR | 2 | 9.1% |
| ss1 | flkR | 1 | 4.5% |
| ss1 | flkL | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 167 | flkR | 199 | flkR | +0.0866 | 0.0076 |
| 171 | flkR | 199 | flkR | +0.0209 | 0.0074 |
| 172 | flkR | 199 | flkR | +0.0193 | 0.0070 |
| 168 | flkR | 199 | flkR | +0.0111 | 0.0063 |
| 159 | ss2 | 199 | flkR | +0.0094 | 0.0061 |

### L0 H11 — Rank #10

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1494

**Key mass** (top-1=39%, top-2=70%, top-3=84%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 1 | flkL | +0.0584 | 39.1% |
| 199 | flkR | +0.0459 | 30.8% |
| 6 | flkL | +0.0216 | 14.5% |
| 45 | ss1 | +0.0056 | 3.7% |
| 44 | ss1 | +0.0051 | 3.4% |

**Query mass** (top-1=52%, top-2=63%, top-3=71%)  [DISTR(T1/H167/T168)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 1 | flkL | +0.0772 | 51.6% |
| 167 | flkR | +0.0171 | 11.5% |
| 168 | flkR | +0.0116 | 7.7% |
| 172 | flkR | +0.0084 | 5.6% |
| 157 | ss2 | +0.0079 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 11.1% |
| -32 | 1 | 5.6% |
| -5 | 1 | 5.6% |
| +167 | 1 | 5.6% |
| -27 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=17%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 3 | 16.7% |
| flkR | flkR | 3 | 16.7% |
| ss2 | flkR | 3 | 16.7% |
| flkR | flkL | 2 | 11.1% |
| flkL | ss1 | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 1 | flkL | 1 | flkL | +0.0399 | 0.3684 |
| 167 | flkR | 199 | flkR | +0.0171 | 0.0054 |
| 1 | flkL | 6 | flkL | +0.0139 | 0.1283 |
| 168 | flkR | 1 | flkL | +0.0116 | 0.0150 |
| 172 | flkR | 199 | flkR | +0.0084 | 0.0063 |

### L3 H4 — Rank #25

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.0148

**Key mass** (top-1=29%, top-2=56%, top-3=78%)  [DISTR(K34/I157/W199)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 34 | flkL | +0.0043 | 29.2% |
| 157 | ss2 | +0.0039 | 26.3% |
| 199 | flkR | +0.0034 | 22.9% |
| 168 | flkR | +0.0032 | 21.5% |

**Query mass** (top-1=77%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | flkR | +0.0114 | 77.1% |
| 158 | ss2 | +0.0034 | 22.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +165 | 1 | 25.0% |
| +42 | 1 | 25.0% |
| -41 | 1 | 25.0% |
| +31 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 1 | 25.0% |
| flkR | ss2 | 1 | 25.0% |
| ss2 | flkR | 1 | 25.0% |
| flkR | flkR | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | flkR | 34 | flkL | +0.0043 | 0.0211 |
| 199 | flkR | 157 | ss2 | +0.0039 | 0.0056 |
| 158 | ss2 | 199 | flkR | +0.0034 | 0.0009 |
| 199 | flkR | 168 | flkR | +0.0032 | 0.0066 |

### L5 H7 — Rank #16

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | CROSS:ss2→ss1  |  cells: 9  |  total attr: +0.0544

**Key mass** (top-1=17%, top-2=31%, top-3=44%)  [DISTR(L40/L42/?-1/V187/A41)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.0091 | 16.7% |
| 42 | ss1 | +0.0078 | 14.4% |
| -1 | other | +0.0073 | 13.4% |
| 187 | flkR | +0.0071 | 13.1% |
| 41 | ss1 | +0.0070 | 12.8% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0544 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +118 | 1 | 11.1% |
| +116 | 1 | 11.1% |
| +159 | 1 | 11.1% |
| -29 | 1 | 11.1% |
| +117 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 55.6% |
| ss2 | flkR | 2 | 22.2% |
| ss2 | other | 1 | 11.1% |
| ss2 | ss2 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 40 | ss1 | +0.0091 | 0.0060 |
| 158 | ss2 | 42 | ss1 | +0.0078 | 0.0024 |
| 158 | ss2 | -1 | other | +0.0073 | 0.0020 |
| 158 | ss2 | 187 | flkR | +0.0071 | 0.0029 |
| 158 | ss2 | 41 | ss1 | +0.0070 | 0.0033 |

### L5 H12 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 4  |  total attr: +0.4386

**Key mass** (top-1=97%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | flkR | +0.4263 | 97.2% |
| 158 | ss2 | +0.0052 | 1.2% |
| 47 | other | +0.0038 | 0.9% |
| 0 | other | +0.0032 | 0.7% |

**Query mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.4315 | 98.4% |
| 40 | ss1 | +0.0070 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -7 | 2 | 50.0% |
| +0 | 1 | 25.0% |
| +40 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 2 | 50.0% |
| ss2 | flkR | 1 | 25.0% |
| ss2 | ss2 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 165 | flkR | +0.4263 | 0.0453 |
| 158 | ss2 | 158 | ss2 | +0.0052 | 0.0019 |
| 40 | ss1 | 47 | other | +0.0038 | 0.0069 |
| 40 | ss1 | 0 | other | +0.0032 | 0.0019 |

### L6 H7 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS_SSE | CROSS:ss1→ss2  |  cells: 3  |  total attr: +0.1494

**Key mass** (top-1=90%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.1348 | 90.2% |
| 159 | ss2 | +0.0098 | 6.6% |
| 8 | flkL | +0.0048 | 3.2% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.1494 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 33.3% |
| -119 | 1 | 33.3% |
| +32 | 1 | 33.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 2 | 66.7% |
| ss1 | flkL | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 40 | ss1 | 158 | ss2 | +0.1348 | 0.0629 |
| 40 | ss1 | 159 | ss2 | +0.0098 | 0.0056 |
| 40 | ss1 | 8 | flkL | +0.0048 | 0.0046 |

### L7 H9 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 8  |  total attr: +0.6527

**Key mass** (top-1=95%, top-2=97%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.6229 | 95.4% |
| 174 | flkR | +0.0070 | 1.1% |
| 8 | flkL | +0.0050 | 0.8% |
| 181 | flkR | +0.0045 | 0.7% |
| 156 | ss2 | +0.0037 | 0.6% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.6527 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +118 | 1 | 12.5% |
| -16 | 1 | 12.5% |
| +150 | 1 | 12.5% |
| -23 | 1 | 12.5% |
| +2 | 1 | 12.5% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 50.0% |
| ss2 | flkL | 2 | 25.0% |
| ss2 | ss1 | 1 | 12.5% |
| ss2 | ss2 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 40 | ss1 | +0.6229 | 0.2992 |
| 158 | ss2 | 174 | flkR | +0.0070 | 0.0094 |
| 158 | ss2 | 8 | flkL | +0.0050 | 0.0056 |
| 158 | ss2 | 181 | flkR | +0.0045 | 0.0036 |
| 158 | ss2 | 156 | ss2 | +0.0037 | 0.0065 |

### L8 H12 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.6457

**Key mass** (top-1=88%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.5705 | 88.4% |
| 40 | ss1 | +0.0649 | 10.1% |
| 38 | ss1 | +0.0103 | 1.6% |

**Query mass** (top-1=52%, top-2=66%, top-3=77%)  [DISTR(L40/W199/V158)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.3337 | 51.7% |
| 199 | flkR | +0.0893 | 13.8% |
| 158 | ss2 | +0.0752 | 11.6% |
| 198 | flkR | +0.0695 | 10.8% |
| 41 | ss1 | +0.0535 | 8.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 10.0% |
| +41 | 1 | 10.0% |
| +40 | 1 | 10.0% |
| +118 | 1 | 10.0% |
| -117 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 4 | 40.0% |
| ss1 | ss2 | 2 | 20.0% |
| flkR | ss2 | 2 | 20.0% |
| ss2 | ss1 | 2 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 40 | ss1 | 158 | ss2 | +0.3337 | 0.5786 |
| 199 | flkR | 158 | ss2 | +0.0893 | 0.2872 |
| 198 | flkR | 158 | ss2 | +0.0695 | 0.3309 |
| 158 | ss2 | 40 | ss1 | +0.0649 | 0.0468 |
| 41 | ss1 | 158 | ss2 | +0.0535 | 0.3974 |

### L9 H8 — Rank #20

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 6  |  total attr: +0.0409

**Key mass** (top-1=23%, top-2=44%, top-3=64%)  [DISTR(D156/D29/V155/V154)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss2 | +0.0095 | 23.2% |
| 29 | flkL | +0.0084 | 20.5% |
| 155 | ss2 | +0.0082 | 20.0% |
| 154 | ss2 | +0.0069 | 16.8% |
| 167 | flkR | +0.0046 | 11.3% |

**Query mass** (top-1=80%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0325 | 79.5% |
| 40 | ss1 | +0.0084 | 20.5% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 1 | 16.7% |
| +11 | 1 | 16.7% |
| +3 | 1 | 16.7% |
| +4 | 1 | 16.7% |
| -9 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 3 | 50.0% |
| ss1 | flkL | 1 | 16.7% |
| ss2 | flkR | 1 | 16.7% |
| ss2 | other | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 156 | ss2 | +0.0095 | 0.0212 |
| 40 | ss1 | 29 | flkL | +0.0084 | 0.0637 |
| 158 | ss2 | 155 | ss2 | +0.0082 | 0.0199 |
| 158 | ss2 | 154 | ss2 | +0.0069 | 0.0207 |
| 158 | ss2 | 167 | flkR | +0.0046 | 0.0140 |

### L9 H13 — Rank #24

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 3  |  total attr: +0.0127

**Key mass** (top-1=42%, top-2=72%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 29 | flkL | +0.0053 | 42.0% |
| 42 | ss1 | +0.0039 | 30.5% |
| 167 | flkR | +0.0035 | 27.5% |

**Query mass** (top-1=72%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.0092 | 72.5% |
| 199 | flkR | +0.0035 | 27.5% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +11 | 1 | 33.3% |
| -2 | 1 | 33.3% |
| +32 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 1 | 33.3% |
| ss1 | ss1 | 1 | 33.3% |
| flkR | flkR | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 40 | ss1 | 29 | flkL | +0.0053 | 0.0273 |
| 40 | ss1 | 42 | ss1 | +0.0039 | 0.0221 |
| 199 | flkR | 167 | flkR | +0.0035 | 0.0467 |

### L10 H9 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 28  |  total attr: +0.4834

**Key mass** (top-1=84%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.4051 | 83.8% |
| 158 | ss2 | +0.0783 | 16.2% |

**Query mass** (top-1=68%, top-2=73%, top-3=77%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.3274 | 67.7% |
| 38 | ss1 | +0.0242 | 5.0% |
| 159 | ss2 | +0.0192 | 4.0% |
| 176 | flkR | +0.0180 | 3.7% |
| 157 | ss2 | +0.0173 | 3.6% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 2 | 7.1% |
| +118 | 1 | 3.6% |
| -2 | 1 | 3.6% |
| +1 | 1 | 3.6% |
| -120 | 1 | 3.6% |

**Region-pair profile** (q→k)  (top=21%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 6 | 21.4% |
| ss2 | ss1 | 5 | 17.9% |
| ss2 | ss2 | 4 | 14.3% |
| flkR | ss2 | 4 | 14.3% |
| ss1 | ss1 | 3 | 10.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 40 | ss1 | +0.3217 | 0.7212 |
| 157 | ss2 | 158 | ss2 | +0.0144 | 0.1360 |
| 38 | ss1 | 40 | ss1 | +0.0126 | 0.2896 |
| 159 | ss2 | 158 | ss2 | +0.0120 | 0.2519 |
| 38 | ss1 | 158 | ss2 | +0.0116 | 0.2065 |

### L11 H9 — Rank #13

**Tags:** k:DUAL-ANCHOR / q:MULTI-ANCHOR | POSITIONAL  |  cells: 8  |  total attr: +0.1296

**Key mass** (top-1=58%, top-2=73%, top-3=87%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0749 | 57.8% |
| 40 | ss1 | +0.0203 | 15.6% |
| 47 | other | +0.0179 | 13.8% |
| 44 | ss1 | +0.0132 | 10.2% |
| 50 | other | +0.0033 | 2.6% |

**Query mass** (top-1=58%, top-2=69%, top-3=80%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0749 | 57.8% |
| 40 | ss1 | +0.0149 | 11.5% |
| 41 | ss1 | +0.0143 | 11.1% |
| 38 | ss1 | +0.0067 | 5.2% |
| 44 | ss1 | +0.0065 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 62.5% |
| -6 | 3 | 37.5% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 37.5% |
| other | other | 2 | 25.0% |
| ss2 | ss2 | 1 | 12.5% |
| ss1 | other | 1 | 12.5% |
| flkL | ss1 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 158 | ss2 | +0.0749 | 0.4456 |
| 40 | ss1 | 40 | ss1 | +0.0149 | 0.3722 |
| 41 | ss1 | 47 | other | +0.0143 | 0.3653 |
| 38 | ss1 | 44 | ss1 | +0.0067 | 0.2833 |
| 44 | ss1 | 44 | ss1 | +0.0065 | 0.1592 |

### L11 H14 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkR→ss2  |  cells: 33  |  total attr: +0.8002

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.7871 | 98.4% |
| 40 | ss1 | +0.0130 | 1.6% |

**Query mass** (top-1=27%, top-2=50%, top-3=67%)  [DISTR(W199/V198/A41/S191)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | flkR | +0.2166 | 27.1% |
| 198 | flkR | +0.1867 | 23.3% |
| 41 | ss1 | +0.1366 | 17.1% |
| 191 | flkR | +0.0423 | 5.3% |
| 170 | flkR | +0.0240 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +41 | 1 | 3.0% |
| +40 | 1 | 3.0% |
| -117 | 1 | 3.0% |
| +33 | 1 | 3.0% |
| +12 | 1 | 3.0% |

**Region-pair profile** (q→k)  [flkR→ss2]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 18 | 54.5% |
| other | ss2 | 6 | 18.2% |
| ss2 | ss2 | 4 | 12.1% |
| ss1 | ss2 | 2 | 6.1% |
| flkL | ss2 | 1 | 3.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | flkR | 158 | ss2 | +0.2166 | 0.5759 |
| 198 | flkR | 158 | ss2 | +0.1867 | 0.6811 |
| 41 | ss1 | 158 | ss2 | +0.1366 | 0.7366 |
| 191 | flkR | 158 | ss2 | +0.0423 | 0.7811 |
| 170 | flkR | 158 | ss2 | +0.0240 | 0.5331 |

### L11 H16 — Rank #7

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.2841

**Key mass** (top-1=51%, top-2=96%, top-3=98%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.1450 | 51.0% |
| 40 | ss1 | +0.1272 | 44.8% |
| 167 | flkR | +0.0057 | 2.0% |
| 41 | ss1 | +0.0031 | 1.1% |
| 17 | flkL | +0.0030 | 1.0% |

**Query mass** (top-1=43%, top-2=53%, top-3=61%)  [DISTR(V158/V198/W199/A41/G44)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.1214 | 42.7% |
| 198 | flkR | +0.0280 | 9.9% |
| 199 | flkR | +0.0244 | 8.6% |
| 41 | ss1 | +0.0186 | 6.5% |
| 44 | ss1 | +0.0142 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +118 | 1 | 3.8% |
| +41 | 1 | 3.8% |
| +40 | 1 | 3.8% |
| -114 | 1 | 3.8% |
| -117 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 7 | 26.9% |
| ss1 | ss2 | 4 | 15.4% |
| ss2 | ss2 | 4 | 15.4% |
| flkL | ss2 | 3 | 11.5% |
| ss2 | ss1 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 40 | ss1 | +0.1072 | 0.4156 |
| 199 | flkR | 158 | ss2 | +0.0206 | 0.3576 |
| 198 | flkR | 158 | ss2 | +0.0205 | 0.2897 |
| 44 | ss1 | 158 | ss2 | +0.0142 | 0.5423 |
| 41 | ss1 | 158 | ss2 | +0.0141 | 0.4763 |

### L11 H18 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 18  |  total attr: +0.1889

**Key mass** (top-1=24%, top-2=37%, top-3=49%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 161 | ss2 | +0.0446 | 23.6% |
| 164 | ss2 | +0.0248 | 13.1% |
| 176 | flkR | +0.0229 | 12.1% |
| 159 | ss2 | +0.0218 | 11.6% |
| -1 | other | +0.0119 | 6.3% |

**Query mass** (top-1=24%, top-2=35%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.0446 | 23.6% |
| 159 | ss2 | +0.0218 | 11.6% |
| 176 | flkR | +0.0195 | 10.3% |
| 158 | ss2 | +0.0174 | 9.2% |
| 46 | ss1 | +0.0127 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 7 | 38.9% |
| -118 | 2 | 11.1% |
| -117 | 1 | 5.6% |
| +159 | 1 | 5.6% |
| +173 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=17%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 3 | 16.7% |
| ss2 | ss2 | 2 | 11.1% |
| flkR | flkR | 2 | 11.1% |
| flkR | ss1 | 2 | 11.1% |
| ss1 | ss1 | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 44 | ss1 | 161 | ss2 | +0.0446 | 0.3592 |
| 159 | ss2 | 159 | ss2 | +0.0218 | 0.3479 |
| 176 | flkR | 176 | flkR | +0.0195 | 0.2652 |
| 46 | ss1 | 164 | ss2 | +0.0127 | 0.2431 |
| 164 | ss2 | 164 | ss2 | +0.0120 | 0.2613 |

### L13 H2 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 15  |  total attr: +0.2082

**Key mass** (top-1=71%, top-2=91%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.1470 | 70.6% |
| 40 | ss1 | +0.0423 | 20.3% |
| 198 | flkR | +0.0103 | 5.0% |
| 41 | ss1 | +0.0054 | 2.6% |
| 151 | other | +0.0032 | 1.5% |

**Query mass** (top-1=25%, top-2=40%, top-3=53%)  [DISTR(L159/V155/V38/G161/L160)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | ss2 | +0.0512 | 24.6% |
| 155 | ss2 | +0.0318 | 15.2% |
| 38 | ss1 | +0.0283 | 13.6% |
| 161 | ss2 | +0.0272 | 13.1% |
| 160 | ss2 | +0.0210 | 10.1% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 3 | 20.0% |
| +1 | 2 | 13.3% |
| -2 | 2 | 13.3% |
| +3 | 2 | 13.3% |
| -4 | 2 | 13.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 7 | 46.7% |
| ss1 | ss1 | 4 | 26.7% |
| flkR | flkR | 2 | 13.3% |
| other | ss1 | 1 | 6.7% |
| ss2 | other | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | ss2 | 158 | ss2 | +0.0512 | 0.7953 |
| 155 | ss2 | 158 | ss2 | +0.0286 | 0.1156 |
| 38 | ss1 | 40 | ss1 | +0.0283 | 0.6389 |
| 161 | ss2 | 158 | ss2 | +0.0272 | 0.9431 |
| 160 | ss2 | 158 | ss2 | +0.0210 | 0.8576 |

### L13 H8 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→ss2  |  cells: 3  |  total attr: +0.0390

**Key mass** (top-1=92%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0361 | 92.5% |
| 267 | other | +0.0029 | 7.5% |

**Query mass** (top-1=55%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 45 | ss1 | +0.0216 | 55.3% |
| 38 | ss1 | +0.0174 | 44.7% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -113 | 1 | 33.3% |
| -120 | 1 | 33.3% |
| -229 | 1 | 33.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 2 | 66.7% |
| ss1 | other | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 45 | ss1 | 158 | ss2 | +0.0216 | 0.2727 |
| 38 | ss1 | 158 | ss2 | +0.0145 | 0.1352 |
| 38 | ss1 | 267 | other | +0.0029 | 0.1416 |

### L14 H9 — Rank #22

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 13  |  total attr: +0.0971

**Key mass** (top-1=57%, top-2=71%, top-3=80%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.0550 | 56.6% |
| 158 | ss2 | +0.0144 | 14.8% |
| 175 | flkR | +0.0084 | 8.7% |
| 176 | flkR | +0.0047 | 4.9% |
| 25 | flkL | +0.0040 | 4.1% |

**Query mass** (top-1=32%, top-2=57%, top-3=68%)  [DISTR(V155/D156/L40/G161)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 155 | ss2 | +0.0309 | 31.8% |
| 156 | ss2 | +0.0244 | 25.1% |
| 40 | ss1 | +0.0107 | 11.1% |
| 161 | ss2 | +0.0098 | 10.1% |
| 42 | ss1 | +0.0084 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +112 | 1 | 7.7% |
| +111 | 1 | 7.7% |
| +117 | 1 | 7.7% |
| -116 | 1 | 7.7% |
| -20 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 46.2% |
| ss1 | ss2 | 2 | 15.4% |
| ss2 | flkR | 2 | 15.4% |
| ss1 | ss1 | 1 | 7.7% |
| ss1 | flkL | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss2 | 44 | ss1 | +0.0207 | 0.3442 |
| 155 | ss2 | 44 | ss1 | +0.0148 | 0.0987 |
| 161 | ss2 | 44 | ss1 | +0.0098 | 0.4564 |
| 42 | ss1 | 158 | ss2 | +0.0084 | 0.2170 |
| 155 | ss2 | 175 | flkR | +0.0084 | 0.0601 |

### L15 H1 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 20  |  total attr: +0.3450

**Key mass** (top-1=95%, top-2=96%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.3280 | 95.1% |
| 45 | ss1 | +0.0042 | 1.2% |
| 165 | flkR | +0.0035 | 1.0% |
| 40 | ss1 | +0.0032 | 0.9% |
| 41 | ss1 | +0.0031 | 0.9% |

**Query mass** (top-1=31%, top-2=47%, top-3=60%)  [DISTR(V158/V155/L159/L42/D156)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.1059 | 30.7% |
| 155 | ss2 | +0.0577 | 16.7% |
| 159 | ss2 | +0.0445 | 12.9% |
| 42 | ss1 | +0.0253 | 7.3% |
| 156 | ss2 | +0.0171 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +115 | 3 | 15.0% |
| +116 | 2 | 10.0% |
| +114 | 1 | 5.0% |
| +111 | 1 | 5.0% |
| -2 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 10 | 50.0% |
| ss1 | ss1 | 4 | 20.0% |
| flkL | ss1 | 3 | 15.0% |
| flkR | ss1 | 2 | 10.0% |
| ss2 | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 44 | ss1 | +0.1029 | 0.8418 |
| 155 | ss2 | 44 | ss1 | +0.0503 | 0.5830 |
| 159 | ss2 | 44 | ss1 | +0.0445 | 0.8030 |
| 42 | ss1 | 44 | ss1 | +0.0253 | 0.7209 |
| 156 | ss2 | 44 | ss1 | +0.0171 | 0.5141 |

### L16 H7 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 32  |  total attr: +0.4268

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 44 | ss1 | +0.4222 | 98.9% |
| 158 | ss2 | +0.0046 | 1.1% |

**Query mass** (top-1=12%, top-2=20%, top-3=29%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 40 | ss1 | +0.0507 | 11.9% |
| 158 | ss2 | +0.0363 | 8.5% |
| 156 | ss2 | +0.0363 | 8.5% |
| 42 | ss1 | +0.0317 | 7.4% |
| 43 | ss1 | +0.0299 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 2 | 6.2% |
| -4 | 1 | 3.1% |
| +114 | 1 | 3.1% |
| +112 | 1 | 3.1% |
| -1 | 1 | 3.1% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 17 | 53.1% |
| ss1 | ss1 | 6 | 18.8% |
| ss2 | ss1 | 5 | 15.6% |
| flkR | ss1 | 2 | 6.2% |
| other | ss1 | 1 | 3.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 40 | ss1 | 44 | ss1 | +0.0507 | 0.9725 |
| 158 | ss2 | 44 | ss1 | +0.0363 | 0.9332 |
| 156 | ss2 | 44 | ss1 | +0.0317 | 0.3455 |
| 42 | ss1 | 44 | ss1 | +0.0317 | 0.9661 |
| 43 | ss1 | 44 | ss1 | +0.0299 | 0.9354 |

### L16 H19 — Rank #29

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.1276

**Key mass** (top-1=51%, top-2=76%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0648 | 50.8% |
| 44 | ss1 | +0.0316 | 24.8% |
| 199 | flkR | +0.0184 | 14.4% |
| 45 | ss1 | +0.0065 | 5.1% |
| -1 | other | +0.0063 | 4.9% |

**Query mass** (top-1=30%, top-2=39%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0381 | 29.9% |
| 161 | ss2 | +0.0117 | 9.2% |
| 42 | ss1 | +0.0108 | 8.5% |
| 40 | ss1 | +0.0084 | 6.6% |
| 28 | flkL | +0.0078 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 1 | 5.0% |
| -116 | 1 | 5.0% |
| -118 | 1 | 5.0% |
| -130 | 1 | 5.0% |
| +113 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 25.0% |
| flkL | ss2 | 3 | 15.0% |
| flkR | flkR | 3 | 15.0% |
| flkR | ss2 | 3 | 15.0% |
| ss2 | ss1 | 2 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 158 | ss2 | 44 | ss1 | +0.0316 | 0.2332 |
| 42 | ss1 | 158 | ss2 | +0.0108 | 0.5008 |
| 40 | ss1 | 158 | ss2 | +0.0084 | 0.4320 |
| 28 | flkL | 158 | ss2 | +0.0078 | 0.3332 |
| 158 | ss2 | 45 | ss1 | +0.0065 | 0.0591 |

### L21 H4 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 10  |  total attr: +0.1435

**Key mass** (top-1=69%, top-2=82%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 158 | ss2 | +0.0991 | 69.1% |
| 42 | ss1 | +0.0182 | 12.7% |
| 44 | ss1 | +0.0156 | 10.8% |
| 38 | ss1 | +0.0061 | 4.2% |
| 43 | ss1 | +0.0046 | 3.2% |

**Query mass** (top-1=31%, top-2=51%, top-3=68%)  [DISTR(D156/V155/A41/L40)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss2 | +0.0446 | 31.1% |
| 155 | ss2 | +0.0282 | 19.7% |
| 41 | ss1 | +0.0247 | 17.2% |
| 40 | ss1 | +0.0136 | 9.5% |
| 159 | ss2 | +0.0131 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 4 | 40.0% |
| -3 | 2 | 20.0% |
| -1 | 2 | 20.0% |
| +1 | 1 | 10.0% |
| +0 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 5 | 50.0% |
| ss1 | ss1 | 5 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss2 | 158 | ss2 | +0.0446 | 0.5400 |
| 155 | ss2 | 158 | ss2 | +0.0282 | 0.5857 |
| 41 | ss1 | 44 | ss1 | +0.0156 | 0.3250 |
| 40 | ss1 | 42 | ss1 | +0.0136 | 0.3384 |
| 159 | ss2 | 158 | ss2 | +0.0131 | 0.5145 |

### L22 H14 — Rank #21

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0684

**Key mass** (top-1=40%, top-2=59%, top-3=75%)  [DISTR(D156/I157/V38)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss2 | +0.0274 | 40.1% |
| 157 | ss2 | +0.0129 | 18.9% |
| 38 | ss1 | +0.0109 | 15.9% |
| 158 | ss2 | +0.0106 | 15.5% |
| 40 | ss1 | +0.0036 | 5.3% |

**Query mass** (top-1=38%, top-2=54%, top-3=69%)  [DISTR(V38/D156/A41/V39)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0258 | 37.7% |
| 156 | ss2 | +0.0109 | 15.9% |
| 41 | ss1 | +0.0106 | 15.5% |
| 39 | ss1 | +0.0088 | 12.9% |
| 40 | ss1 | +0.0087 | 12.8% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 3 | 37.5% |
| -118 | 1 | 12.5% |
| +118 | 1 | 12.5% |
| -119 | 1 | 12.5% |
| +117 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 62.5% |
| ss2 | ss1 | 2 | 25.0% |
| ss1 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 38 | ss1 | 156 | ss2 | +0.0186 | 0.1856 |
| 156 | ss2 | 38 | ss1 | +0.0109 | 0.0853 |
| 41 | ss1 | 158 | ss2 | +0.0106 | 0.1685 |
| 39 | ss1 | 156 | ss2 | +0.0088 | 0.1027 |
| 40 | ss1 | 157 | ss2 | +0.0087 | 0.0833 |

### L26 H16 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 10  |  total attr: +0.0701

**Key mass** (top-1=26%, top-2=51%, top-3=74%)  [DISTR(D156/I157/V38)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss2 | +0.0184 | 26.2% |
| 157 | ss2 | +0.0173 | 24.7% |
| 38 | ss1 | +0.0159 | 22.6% |
| 197 | flkR | +0.0108 | 15.4% |
| 36 | ss1 | +0.0048 | 6.9% |

**Query mass** (top-1=35%, top-2=67%, top-3=77%)  [DISTR(V38/D156/L40)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0249 | 35.5% |
| 156 | ss2 | +0.0220 | 31.3% |
| 40 | ss1 | +0.0070 | 10.0% |
| 157 | ss2 | +0.0063 | 9.0% |
| 155 | ss2 | +0.0062 | 8.8% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -118 | 1 | 10.0% |
| +118 | 1 | 10.0% |
| -119 | 1 | 10.0% |
| -117 | 1 | 10.0% |
| -42 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 40.0% |
| ss2 | ss1 | 3 | 30.0% |
| ss2 | flkR | 2 | 20.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 38 | ss1 | 156 | ss2 | +0.0146 | 0.0945 |
| 156 | ss2 | 38 | ss1 | +0.0125 | 0.0827 |
| 38 | ss1 | 157 | ss2 | +0.0103 | 0.1209 |
| 40 | ss1 | 157 | ss2 | +0.0070 | 0.0849 |
| 155 | ss2 | 197 | flkR | +0.0062 | 0.0957 |

### L27 H15 — Rank #11

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 10  |  total attr: +0.0844

**Key mass** (top-1=27%, top-2=53%, top-3=76%)  [DISTR(A41/I157/D156)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 41 | ss1 | +0.0230 | 27.2% |
| 157 | ss2 | +0.0216 | 25.6% |
| 156 | ss2 | +0.0198 | 23.4% |
| 38 | ss1 | +0.0121 | 14.3% |
| 39 | ss1 | +0.0045 | 5.3% |

**Query mass** (top-1=36%, top-2=54%, top-3=64%)  [DISTR(V38/V155/D156/V158)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0303 | 35.9% |
| 155 | ss2 | +0.0150 | 17.8% |
| 156 | ss2 | +0.0091 | 10.7% |
| 158 | ss2 | +0.0080 | 9.5% |
| 157 | ss2 | +0.0075 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +117 | 2 | 20.0% |
| -117 | 2 | 20.0% |
| -119 | 1 | 10.0% |
| +114 | 1 | 10.0% |
| -118 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 50.0% |
| ss2 | ss1 | 5 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 38 | ss1 | 157 | ss2 | +0.0172 | 0.1865 |
| 155 | ss2 | 41 | ss1 | +0.0150 | 0.0610 |
| 38 | ss1 | 156 | ss2 | +0.0131 | 0.0641 |
| 158 | ss2 | 41 | ss1 | +0.0080 | 0.2291 |
| 157 | ss2 | 38 | ss1 | +0.0075 | 0.0855 |

### L29 H18 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1921

**Key mass** (top-1=27%, top-2=45%, top-3=58%)  [DISTR(R31/I28/A41/V155)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 31 | flkL | +0.0527 | 27.4% |
| 28 | flkL | +0.0335 | 17.5% |
| 41 | ss1 | +0.0260 | 13.6% |
| 155 | ss2 | +0.0235 | 12.2% |
| 27 | flkL | +0.0130 | 6.8% |

**Query mass** (top-1=26%, top-2=44%, top-3=59%)  [DISTR(V38/I157/D156/A41)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0491 | 25.6% |
| 157 | ss2 | +0.0362 | 18.9% |
| 156 | ss2 | +0.0289 | 15.0% |
| 41 | ss1 | +0.0277 | 14.4% |
| 155 | ss2 | +0.0260 | 13.6% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 2 | 11.1% |
| +125 | 1 | 5.6% |
| +114 | 1 | 5.6% |
| -114 | 1 | 5.6% |
| +10 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 5 | 27.8% |
| ss1 | ss2 | 5 | 27.8% |
| ss1 | flkL | 5 | 27.8% |
| ss2 | ss1 | 2 | 11.1% |
| ss1 | ss1 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 156 | ss2 | 31 | flkL | +0.0289 | 0.5461 |
| 155 | ss2 | 41 | ss1 | +0.0260 | 0.2710 |
| 41 | ss1 | 155 | ss2 | +0.0235 | 0.1505 |
| 38 | ss1 | 28 | flkL | +0.0184 | 0.1697 |
| 38 | ss1 | 31 | flkL | +0.0181 | 0.1841 |

### L30 H1 — Rank #26

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 7  |  total attr: +0.0486

**Key mass** (top-1=26%, top-2=48%, top-3=65%)  [DISTR(I157/D156/V39/A41)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | ss2 | +0.0125 | 25.8% |
| 156 | ss2 | +0.0110 | 22.6% |
| 39 | ss1 | +0.0080 | 16.5% |
| 41 | ss1 | +0.0065 | 13.3% |
| 37 | ss1 | +0.0064 | 13.3% |

**Query mass** (top-1=31%, top-2=60%, top-3=78%)  [DISTR(V38/D156/L40)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0149 | 30.6% |
| 156 | ss2 | +0.0145 | 29.8% |
| 40 | ss1 | +0.0086 | 17.8% |
| 158 | ss2 | +0.0065 | 13.3% |
| 157 | ss2 | +0.0042 | 8.6% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +117 | 3 | 42.9% |
| -118 | 1 | 14.3% |
| -117 | 1 | 14.3% |
| +119 | 1 | 14.3% |
| -119 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 57.1% |
| ss1 | ss2 | 3 | 42.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 38 | ss1 | 156 | ss2 | +0.0110 | 0.0802 |
| 40 | ss1 | 157 | ss2 | +0.0086 | 0.1135 |
| 156 | ss2 | 39 | ss1 | +0.0080 | 0.1576 |
| 158 | ss2 | 41 | ss1 | +0.0065 | 0.2507 |
| 156 | ss2 | 37 | ss1 | +0.0064 | 0.4288 |

### L32 H13 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.1265

**Key mass** (top-1=42%, top-2=62%, top-3=70%)  [DISTR(D156/I157/A41)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss2 | +0.0526 | 41.6% |
| 157 | ss2 | +0.0256 | 20.2% |
| 41 | ss1 | +0.0110 | 8.7% |
| 36 | ss1 | +0.0107 | 8.4% |
| 40 | ss1 | +0.0084 | 6.6% |

**Query mass** (top-1=33%, top-2=52%, top-3=65%)  [DISTR(V36/V38/D156/L40)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 36 | ss1 | +0.0423 | 33.5% |
| 38 | ss1 | +0.0239 | 18.9% |
| 156 | ss2 | +0.0154 | 12.2% |
| 40 | ss1 | +0.0148 | 11.7% |
| 157 | ss2 | +0.0117 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -119 | 2 | 18.2% |
| -120 | 1 | 9.1% |
| -117 | 1 | 9.1% |
| +114 | 1 | 9.1% |
| +120 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 54.5% |
| ss2 | ss1 | 5 | 45.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 36 | ss1 | 156 | ss2 | +0.0423 | 0.3180 |
| 38 | ss1 | 157 | ss2 | +0.0137 | 0.1553 |
| 40 | ss1 | 157 | ss2 | +0.0119 | 0.0982 |
| 155 | ss2 | 41 | ss1 | +0.0110 | 0.0538 |
| 156 | ss2 | 36 | ss1 | +0.0107 | 0.0801 |

### L32 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 15  |  total attr: +0.2404

**Key mass** (top-1=22%, top-2=44%, top-3=58%)  [DISTR(V38/V155/L40/D156)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 38 | ss1 | +0.0530 | 22.0% |
| 155 | ss2 | +0.0524 | 21.8% |
| 40 | ss1 | +0.0351 | 14.6% |
| 156 | ss2 | +0.0341 | 14.2% |
| 41 | ss1 | +0.0178 | 7.4% |

**Query mass** (top-1=25%, top-2=50%, top-3=68%)  [DISTR(D156/A41/I157/V38)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 156 | ss2 | +0.0611 | 25.4% |
| 41 | ss1 | +0.0597 | 24.8% |
| 157 | ss2 | +0.0425 | 17.7% |
| 38 | ss1 | +0.0319 | 13.3% |
| 155 | ss2 | +0.0178 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +117 | 3 | 20.0% |
| -117 | 3 | 20.0% |
| +119 | 2 | 13.3% |
| -114 | 1 | 6.7% |
| +118 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 53.3% |
| ss1 | ss2 | 7 | 46.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 41 | ss1 | 155 | ss2 | +0.0524 | 0.1560 |
| 156 | ss2 | 38 | ss1 | +0.0402 | 0.1110 |
| 157 | ss2 | 40 | ss1 | +0.0297 | 0.1484 |
| 38 | ss1 | 156 | ss2 | +0.0257 | 0.0710 |
| 155 | ss2 | 41 | ss1 | +0.0178 | 0.0528 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #14 | L0 | H3 | 15 | +0.1271 | SINGLE-ANCHOR | W199 | DISTRIBUTED |  |  | ss2→flkR |
| #28 | L0 | H9 | 22 | +0.2351 | SINGLE-ANCHOR | W199 | DISTRIBUTED |  |  | INTRA:flkR |
| #10 | L0 | H11 | 18 | +0.1494 | MULTI-ANCHOR |  | DISTRIBUTED | T1/H167/T168 |  |  |
| #25 | L3 | H4 | 4 | +0.0148 | DISTRIBUTED | K34/I157/W199 | SINGLE-ANCHOR | W199 |  |  |
| #16 | L5 | H7 | 9 | +0.0544 | DISTRIBUTED | L40/L42/?-1/V187/A41 | SINGLE-ANCHOR | V158 |  | CROSS:ss2→ss1 |
| #4 | L5 | H12 | 4 | +0.4386 | SINGLE-ANCHOR | D165 | SINGLE-ANCHOR | V158 |  |  |
| #17 | L6 | H7 | 3 | +0.1494 | SINGLE-ANCHOR | V158 | SINGLE-ANCHOR | L40 | CROSS_SSE | CROSS:ss1→ss2 |
| #2 | L7 | H9 | 8 | +0.6527 | SINGLE-ANCHOR | L40 | SINGLE-ANCHOR | V158 |  | ss2→flkR |
| #1 | L8 | H12 | 10 | +0.6457 | SINGLE-ANCHOR | V158 | DISTRIBUTED | L40/W199/V158 |  |  |
| #20 | L9 | H8 | 6 | +0.0409 | DISTRIBUTED | D156/D29/V155/V154 | SINGLE-ANCHOR | V158 |  | INTRA:ss2 |
| #24 | L9 | H13 | 3 | +0.0127 | DUAL-ANCHOR | D29/L42 | SINGLE-ANCHOR | L40 |  |  |
| #3 | L10 | H9 | 28 | +0.4834 | SINGLE-ANCHOR | L40 | SINGLE-ANCHOR | V158 |  |  |
| #13 | L11 | H9 | 8 | +0.1296 | DUAL-ANCHOR | V158/L40 | MULTI-ANCHOR |  | POSITIONAL |  |
| #5 | L11 | H14 | 33 | +0.8002 | SINGLE-ANCHOR | V158 | DISTRIBUTED | W199/V198/A41/S191 |  | flkR→ss2 |
| #7 | L11 | H16 | 26 | +0.2841 | DUAL-ANCHOR | V158/L40 | DISTRIBUTED | V158/V198/W199/A41/G44 |  |  |
| #27 | L11 | H18 | 18 | +0.1889 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL |  |
| #12 | L13 | H2 | 15 | +0.2082 | SINGLE-ANCHOR | V158 | DISTRIBUTED | L159/V155/V38/G161/L160 |  | INTRA:ss2 |
| #15 | L13 | H8 | 3 | +0.0390 | SINGLE-ANCHOR | V158 | DUAL-ANCHOR | G45/V38 |  | CROSS:ss1→ss2 |
| #22 | L14 | H9 | 13 | +0.0971 | DUAL-ANCHOR | G44/V158 | DISTRIBUTED | V155/D156/L40/G161 |  | CROSS:ss2→ss1 |
| #23 | L15 | H1 | 20 | +0.3450 | SINGLE-ANCHOR | G44 | DISTRIBUTED | V158/V155/L159/L42/D156 |  | CROSS:ss2→ss1 |
| #18 | L16 | H7 | 32 | +0.4268 | SINGLE-ANCHOR | G44 | DISTRIBUTED |  |  | flkL→ss1 |
| #29 | L16 | H19 | 20 | +0.1276 | DUAL-ANCHOR | V158/G44 | DISTRIBUTED |  |  |  |
| #30 | L21 | H4 | 10 | +0.1435 | SINGLE-ANCHOR | V158 | DISTRIBUTED | D156/V155/A41/L40 | POSITIONAL | INTRA:ss2 |
| #21 | L22 | H14 | 8 | +0.0684 | DISTRIBUTED | D156/I157/V38 | DISTRIBUTED | V38/D156/A41/V39 | CROSS_SSE | CROSS:ss1→ss2 |
| #19 | L26 | H16 | 10 | +0.0701 | DISTRIBUTED | D156/I157/V38 | DISTRIBUTED | V38/D156/L40 |  | CROSS:ss1→ss2 |
| #11 | L27 | H15 | 10 | +0.0844 | DISTRIBUTED | A41/I157/D156 | DISTRIBUTED | V38/V155/D156/V158 |  | CROSS:ss1→ss2 |
| #8 | L29 | H18 | 18 | +0.1921 | DISTRIBUTED | R31/I28/A41/V155 | DISTRIBUTED | V38/I157/D156/A41 |  |  |
| #26 | L30 | H1 | 7 | +0.0486 | DISTRIBUTED | I157/D156/V39/A41 | DISTRIBUTED | V38/D156/L40 | CROSS_SSE | CROSS:ss2→ss1 |
| #9 | L32 | H13 | 11 | +0.1265 | DISTRIBUTED | D156/I157/A41 | DISTRIBUTED | V36/V38/D156/L40 |  | CROSS:ss1→ss2 |
| #6 | L32 | H18 | 15 | +0.2404 | DISTRIBUTED | V38/V155/L40/D156 | DISTRIBUTED | D156/A41/I157/V38 |  | CROSS:ss2→ss1 |
