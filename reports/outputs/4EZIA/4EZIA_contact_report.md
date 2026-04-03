# Contact Pattern Analysis: 4EZIA

Generated: 2026-03-26 00:44:01   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4EZIA |
| Contact pair | (194, 311) |
| ss1 | [189, 200) |
| ss2 | [306, 317) |
| Clean flank | 38 |
| Corrupt flank | 37 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.7957 |
| Corrupt metric | 0.0133 |
| Gap | 0.7825 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 70.41% |
| positive IE | 150 | 73.96% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L10 | H9 | +0.9518 |
| 2 | L5 | H19 | +0.2462 |
| 3 | L8 | H12 | +0.2355 |
| 4 | L22 | H14 | +0.1735 |
| 5 | L6 | H8 | +0.1586 |
| 6 | L9 | H7 | +0.1284 |
| 7 | L32 | H18 | +0.1102 |
| 8 | L27 | H15 | +0.0952 |
| 9 | L19 | H0 | +0.0769 |
| 10 | L5 | H7 | +0.0742 |
| 11 | L12 | H2 | +0.0684 |
| 12 | L32 | H13 | +0.0677 |
| 13 | L6 | H19 | +0.0645 |
| 14 | L24 | H18 | +0.0606 |
| 15 | L30 | H1 | +0.0585 |
| 16 | L14 | H9 | +0.0512 |
| 17 | L11 | H6 | +0.0473 |
| 18 | L29 | H18 | +0.0467 |
| 19 | L14 | H0 | +0.0461 |
| 20 | L17 | H10 | +0.0458 |
| 21 | L7 | H4 | +0.0426 |
| 22 | L14 | H13 | +0.0405 |
| 23 | L17 | H18 | +0.0349 |
| 24 | L9 | H3 | +0.0315 |
| 25 | L11 | H19 | +0.0308 |
| 26 | L26 | H16 | +0.0292 |
| 27 | L30 | H0 | +0.0283 |
| 28 | L7 | H0 | +0.0280 |
| 29 | L15 | H14 | +0.0267 |
| 30 | L10 | H0 | +0.0258 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | -0.00% |
| 4 | 0.01% |
| 5 | 0.02% |
| 6 | 0.02% |
| 7 | 0.04% |
| 8 | 0.09% |
| 9 | 0.09% |
| 10 | 0.10% |
| 20 | 0.42% |
| 80 | 18.58% |
| 450 | 132.61% |

## Cell Attribution Analysis

Total cells: 20,224,776

- Positive: 10,316,922
- Negative: 9,904,832

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H19 | 193 | ss1 | 166 | flkL | +0.162588 | 0.076376 |
| L8 | H12 | 310 | ss2 | 164 | flkL | +0.151518 | 0.496158 |
| L6 | H8 | 310 | ss2 | 321 | flkR | +0.114511 | 0.101172 |
| L9 | H7 | 193 | ss1 | 310 | ss2 | +0.105931 | 0.312251 |
| L10 | H9 | 193 | ss1 | 310 | ss2 | +0.067978 | 0.367213 |
| L6 | H19 | 310 | ss2 | 193 | ss1 | +0.067347 | 0.116419 |
| L2 | H15 | 166 | flkL | 151 | flkL | +0.059472 | 0.065962 |
| L10 | H9 | 310 | ss2 | 310 | ss2 | +0.049323 | 0.421953 |
| L5 | H7 | 310 | ss2 | 166 | flkL | +0.044916 | 0.093179 |
| L7 | H0 | 164 | flkL | 193 | ss1 | +0.043623 | 0.073529 |
| L27 | H15 | 307 | ss2 | 193 | ss1 | +0.042381 | 0.379723 |
| L22 | H14 | 313 | ss2 | 197 | ss1 | +0.039922 | 0.790126 |
| L7 | H4 | 164 | flkL | 310 | ss2 | +0.039441 | 0.196057 |
| L10 | H6 | 328 | flkR | 310 | ss2 | +0.038865 | 0.459861 |
| L10 | H9 | 164 | flkL | 310 | ss2 | +0.037196 | 0.463711 |
| L8 | H12 | 164 | flkL | 310 | ss2 | +0.035666 | 0.392950 |
| L8 | H12 | 193 | ss1 | 310 | ss2 | +0.030461 | 0.300549 |
| L4 | H18 | 166 | flkL | 170 | flkL | +0.029356 | 0.033199 |
| L11 | H6 | 310 | ss2 | 328 | flkR | +0.029086 | 0.396737 |
| L10 | H9 | 170 | flkL | 310 | ss2 | +0.027353 | 0.518613 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L13 | H18 | 332 | flkR | 170 | flkL | -0.009103 | 0.777586 |
| L16 | H12 | 196 | ss1 | 193 | ss1 | -0.009379 | 0.864521 |
| L10 | H0 | 310 | ss2 | 310 | ss2 | -0.009408 | 0.109279 |
| L7 | H13 | 182 | flkL | 151 | flkL | -0.009485 | 0.112869 |
| L13 | H18 | 304 | other | 170 | flkL | -0.010309 | 0.659840 |
| L17 | H16 | 308 | ss2 | 310 | ss2 | -0.010332 | 0.730897 |
| L12 | H15 | 166 | flkL | 310 | ss2 | -0.010782 | 0.821145 |
| L7 | H13 | 183 | flkL | 152 | flkL | -0.010835 | 0.189210 |
| L13 | H2 | 316 | ss2 | 310 | ss2 | -0.010970 | 0.960795 |
| L10 | H6 | 164 | flkL | 164 | flkL | -0.011002 | 0.168166 |
| L12 | H15 | 169 | flkL | 310 | ss2 | -0.011010 | 0.895666 |
| L11 | H14 | 169 | flkL | 164 | flkL | -0.011069 | 0.608465 |
| L26 | H16 | 193 | ss1 | 309 | ss2 | -0.012111 | 0.540717 |
| L13 | H2 | 317 | flkR | 310 | ss2 | -0.013224 | 0.953495 |
| L20 | H15 | 307 | ss2 | 311 | ss2 | -0.013896 | 0.407078 |
| L8 | H12 | 310 | ss2 | 193 | ss1 | -0.014366 | 0.074364 |
| L12 | H15 | 173 | flkL | 310 | ss2 | -0.015862 | 0.955984 |
| L13 | H18 | 310 | ss2 | 170 | flkL | -0.017007 | 0.796998 |
| L13 | H2 | 310 | ss2 | 310 | ss2 | -0.028169 | 0.926215 |
| L12 | H15 | 193 | ss1 | 310 | ss2 | -0.039283 | 0.751484 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0133 | 0.00% |
| 10 | 10 | 9 | 0.0133 | -0.00% |
| 20 | 20 | 15 | 0.0133 | 0.00% |
| 50 | 50 | 36 | 0.0133 | 0.01% |
| 100 | 100 | 62 | 0.0135 | 0.03% |
| 200 | 200 | 96 | 0.0161 | 0.36% |
| 500 | 500 | 132 | 0.0288 | 1.99% |
| 1000 | 1,000 | 140 | 0.0827 | 8.87% |
| 2000 | 2,000 | 145 | 0.1881 | 22.34% |
| 5000 | 5,000 | 150 | 0.3367 | 41.34% |
| 10000 | 10,000 | 150 | 0.4673 | 58.02% |
| 20000 | 20,000 | 150 | 0.5544 | 69.16% |
| 50000 | 50,000 | 150 | 0.7192 | 90.22% |

## Motif Analysis

### L5 H7 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +0.0610

**Key mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | flkL | +0.0595 | 97.5% |
| 310 | ss2 | +0.0015 | 2.5% |

**Query mass** (top-1=74%, top-2=85%, top-3=92%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0449 | 73.6% |
| 193 | ss1 | +0.0071 | 11.6% |
| 321 | flkR | +0.0041 | 6.6% |
| 164 | flkL | +0.0032 | 5.2% |
| 330 | flkR | +0.0018 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +144 | 1 | 16.7% |
| +27 | 1 | 16.7% |
| +155 | 1 | 16.7% |
| -2 | 1 | 16.7% |
| +164 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkL | 2 | 33.3% |
| ss2 | flkL | 1 | 16.7% |
| ss1 | flkL | 1 | 16.7% |
| flkL | flkL | 1 | 16.7% |
| ss1 | ss2 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 166 | flkL | +0.0449 | 0.0932 |
| 193 | ss1 | 166 | flkL | +0.0056 | 0.0363 |
| 321 | flkR | 166 | flkL | +0.0041 | 0.0301 |
| 164 | flkL | 166 | flkL | +0.0032 | 0.0256 |
| 330 | flkR | 166 | flkL | +0.0018 | 0.0424 |

### L5 H19 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 2  |  total attr: +0.1666

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 166 | flkL | +0.1666 | 100.0% |

**Query mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.1626 | 97.6% |
| 190 | ss1 | +0.0040 | 2.4% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +27 | 1 | 50.0% |
| +24 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 166 | flkL | +0.1626 | 0.0764 |
| 190 | ss1 | 166 | flkL | +0.0040 | 0.0358 |

### L6 H8 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 1  |  total attr: +0.1145

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 321 | flkR | +0.1145 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.1145 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -11 | 1 | 100.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 321 | flkR | +0.1145 | 0.1012 |

### L6 H19 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 7  |  total attr: +0.0921

**Key mass** (top-1=82%, top-2=90%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0757 | 82.2% |
| 164 | flkL | +0.0070 | 7.6% |
| -1 | other | +0.0053 | 5.7% |
| 190 | ss1 | +0.0027 | 2.9% |
| 170 | flkL | +0.0014 | 1.5% |

**Query mass** (top-1=88%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0811 | 88.0% |
| 164 | flkL | +0.0090 | 9.8% |
| 193 | ss1 | +0.0020 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +117 | 1 | 14.3% |
| +146 | 1 | 14.3% |
| -29 | 1 | 14.3% |
| +311 | 1 | 14.3% |
| -26 | 1 | 14.3% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 2 | 28.6% |
| flkL | ss1 | 2 | 28.6% |
| ss2 | ss1 | 1 | 14.3% |
| ss2 | other | 1 | 14.3% |
| ss1 | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 193 | ss1 | +0.0673 | 0.1164 |
| 310 | ss2 | 164 | flkL | +0.0070 | 0.0150 |
| 164 | flkL | 193 | ss1 | +0.0064 | 0.0474 |
| 310 | ss2 | -1 | other | +0.0053 | 0.0172 |
| 164 | flkL | 190 | ss1 | +0.0027 | 0.0646 |

### L7 H0 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | flkL→ss1  |  cells: 2  |  total attr: +0.0457

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0457 | 100.0% |

**Query mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 164 | flkL | +0.0436 | 95.4% |
| 170 | flkL | +0.0021 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -29 | 1 | 50.0% |
| -23 | 1 | 50.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 2 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 164 | flkL | 193 | ss1 | +0.0436 | 0.0735 |
| 170 | flkL | 193 | ss1 | +0.0021 | 0.0860 |

### L7 H4 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:flkL→ss2  |  cells: 4  |  total attr: +0.0736

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0736 | 100.0% |

**Query mass** (top-1=54%, top-2=91%, top-3=97%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 164 | flkL | +0.0394 | 53.6% |
| 193 | ss1 | +0.0273 | 37.1% |
| 166 | flkL | +0.0049 | 6.6% |
| 194 | ss1 | +0.0020 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -146 | 1 | 25.0% |
| -117 | 1 | 25.0% |
| -144 | 1 | 25.0% |
| -116 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 2 | 50.0% |
| ss1 | ss2 | 2 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 164 | flkL | 310 | ss2 | +0.0394 | 0.1961 |
| 193 | ss1 | 310 | ss2 | +0.0273 | 0.1846 |
| 166 | flkL | 310 | ss2 | +0.0049 | 0.1717 |
| 194 | ss1 | 310 | ss2 | +0.0020 | 0.1210 |

### L8 H12 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:flkL→ss2  |  cells: 4  |  total attr: +0.2241

**Key mass** (top-1=68%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 164 | flkL | +0.1515 | 67.6% |
| 310 | ss2 | +0.0725 | 32.4% |

**Query mass** (top-1=68%, top-2=84%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.1515 | 67.6% |
| 164 | flkL | +0.0357 | 15.9% |
| 193 | ss1 | +0.0305 | 13.6% |
| 170 | flkL | +0.0064 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +146 | 1 | 25.0% |
| -146 | 1 | 25.0% |
| -117 | 1 | 25.0% |
| -140 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 2 | 50.0% |
| ss2 | flkL | 1 | 25.0% |
| ss1 | ss2 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 164 | flkL | +0.1515 | 0.4962 |
| 164 | flkL | 310 | ss2 | +0.0357 | 0.3930 |
| 193 | ss1 | 310 | ss2 | +0.0305 | 0.3005 |
| 170 | flkL | 310 | ss2 | +0.0064 | 0.1962 |

### L9 H3 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0646

**Key mass** (top-1=72%, top-2=90%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0466 | 72.1% |
| 170 | flkL | +0.0113 | 17.5% |
| 320 | flkR | +0.0025 | 3.9% |
| 196 | ss1 | +0.0024 | 3.7% |
| 193 | ss1 | +0.0018 | 2.8% |

**Query mass** (top-1=32%, top-2=50%, top-3=65%)  [DISTR(L310/L164/F332/A328)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0207 | 32.1% |
| 164 | flkL | +0.0113 | 17.5% |
| 332 | flkR | +0.0097 | 15.0% |
| 328 | flkR | +0.0062 | 9.6% |
| 193 | ss1 | +0.0042 | 6.5% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 15.4% |
| -6 | 1 | 7.7% |
| +22 | 1 | 7.7% |
| +18 | 1 | 7.7% |
| +1 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 5 | 38.5% |
| ss2 | ss2 | 3 | 23.1% |
| ss1 | ss1 | 2 | 15.4% |
| flkL | flkL | 1 | 7.7% |
| ss2 | flkR | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 310 | ss2 | +0.0182 | 0.0770 |
| 164 | flkL | 170 | flkL | +0.0113 | 0.1592 |
| 332 | flkR | 310 | ss2 | +0.0097 | 0.3602 |
| 328 | flkR | 310 | ss2 | +0.0062 | 0.3094 |
| 311 | ss2 | 310 | ss2 | +0.0030 | 0.4013 |

### L9 H7 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 6  |  total attr: +0.1470

**Key mass** (top-1=95%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.1402 | 95.3% |
| 166 | flkL | +0.0040 | 2.7% |
| 170 | flkL | +0.0029 | 2.0% |

**Query mass** (top-1=72%, top-2=89%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.1059 | 72.0% |
| 164 | flkL | +0.0245 | 16.7% |
| 310 | ss2 | +0.0146 | 9.9% |
| 170 | flkL | +0.0020 | 1.4% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 1 | 16.7% |
| -146 | 1 | 16.7% |
| +0 | 1 | 16.7% |
| +144 | 1 | 16.7% |
| +140 | 1 | 16.7% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 2 | 33.3% |
| ss2 | flkL | 2 | 33.3% |
| ss1 | ss2 | 1 | 16.7% |
| ss2 | ss2 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 310 | ss2 | +0.1059 | 0.3123 |
| 164 | flkL | 310 | ss2 | +0.0245 | 0.1123 |
| 310 | ss2 | 310 | ss2 | +0.0077 | 0.0484 |
| 310 | ss2 | 166 | flkL | +0.0040 | 0.0328 |
| 310 | ss2 | 170 | flkL | +0.0029 | 0.0250 |

### L10 H0 — Rank #30

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0540

**Key mass** (top-1=47%, top-2=88%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0252 | 46.6% |
| 164 | flkL | +0.0222 | 41.1% |
| 310 | ss2 | +0.0066 | 12.2% |

**Query mass** (top-1=29%, top-2=46%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | flkL | +0.0154 | 28.6% |
| 195 | ss1 | +0.0094 | 17.4% |
| 197 | ss1 | +0.0039 | 7.2% |
| 201 | other | +0.0035 | 6.6% |
| 166 | flkL | +0.0026 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 3 | 18.8% |
| +6 | 2 | 12.5% |
| +2 | 2 | 12.5% |
| +4 | 2 | 12.5% |
| +8 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 37.5% |
| flkL | flkL | 4 | 25.0% |
| ss2 | ss2 | 3 | 18.8% |
| other | ss1 | 2 | 12.5% |
| other | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 170 | flkL | 164 | flkL | +0.0154 | 0.3741 |
| 195 | ss1 | 193 | ss1 | +0.0094 | 0.3822 |
| 197 | ss1 | 193 | ss1 | +0.0039 | 0.4578 |
| 201 | other | 193 | ss1 | +0.0035 | 0.4410 |
| 166 | flkL | 164 | flkL | +0.0026 | 0.4338 |

### L10 H9 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.2628

**Key mass** (top-1=94%, top-2=99%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.2457 | 93.5% |
| -1 | other | +0.0136 | 5.2% |
| 164 | flkL | +0.0018 | 0.7% |
| 170 | flkL | +0.0017 | 0.6% |

**Query mass** (top-1=27%, top-2=49%, top-3=64%)  [DISTR(V193/L310/L164/G170)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0714 | 27.2% |
| 310 | ss2 | +0.0572 | 21.8% |
| 164 | flkL | +0.0399 | 15.2% |
| 170 | flkL | +0.0274 | 10.4% |
| 328 | flkR | +0.0168 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 1 | 3.8% |
| +0 | 1 | 3.8% |
| -146 | 1 | 3.8% |
| -140 | 1 | 3.8% |
| +18 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 7 | 26.9% |
| ss1 | ss2 | 5 | 19.2% |
| ss2 | ss2 | 3 | 11.5% |
| flkR | ss2 | 3 | 11.5% |
| other | ss2 | 3 | 11.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 310 | ss2 | +0.0680 | 0.3672 |
| 310 | ss2 | 310 | ss2 | +0.0493 | 0.4220 |
| 164 | flkL | 310 | ss2 | +0.0372 | 0.4637 |
| 170 | flkL | 310 | ss2 | +0.0274 | 0.5186 |
| 328 | flkR | 310 | ss2 | +0.0138 | 0.3575 |

### L11 H6 — Rank #17

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 10  |  total attr: +0.0514

**Key mass** (top-1=57%, top-2=65%, top-3=71%)  [DISTR(A328/K334/K342)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 328 | flkR | +0.0291 | 56.6% |
| 334 | flkR | +0.0042 | 8.2% |
| 342 | flkR | +0.0033 | 6.4% |
| 329 | flkR | +0.0032 | 6.3% |
| 346 | flkR | +0.0031 | 6.1% |

**Query mass** (top-1=98%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0501 | 97.5% |
| 164 | flkL | +0.0013 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -18 | 1 | 10.0% |
| -24 | 1 | 10.0% |
| -32 | 1 | 10.0% |
| -19 | 1 | 10.0% |
| -36 | 1 | 10.0% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=90%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 9 | 90.0% |
| flkL | flkL | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 328 | flkR | +0.0291 | 0.3967 |
| 310 | ss2 | 334 | flkR | +0.0042 | 0.0210 |
| 310 | ss2 | 342 | flkR | +0.0033 | 0.0298 |
| 310 | ss2 | 329 | flkR | +0.0032 | 0.1634 |
| 310 | ss2 | 346 | flkR | +0.0031 | 0.0186 |

### L11 H19 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | ss1→flkL  |  cells: 6  |  total attr: +0.0373

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | flkL | +0.0373 | 100.0% |

**Query mass** (top-1=40%, top-2=78%, top-3=86%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0148 | 39.5% |
| 195 | ss1 | +0.0143 | 38.4% |
| 169 | flkL | +0.0029 | 7.9% |
| 200 | other | +0.0020 | 5.2% |
| 197 | ss1 | +0.0018 | 4.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +23 | 1 | 16.7% |
| +25 | 1 | 16.7% |
| -1 | 1 | 16.7% |
| +30 | 1 | 16.7% |
| +27 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 3 | 50.0% |
| flkL | flkL | 2 | 33.3% |
| other | flkL | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 170 | flkL | +0.0148 | 0.6976 |
| 195 | ss1 | 170 | flkL | +0.0143 | 0.4699 |
| 169 | flkL | 170 | flkL | +0.0029 | 0.3680 |
| 200 | other | 170 | flkL | +0.0020 | 0.3729 |
| 197 | ss1 | 170 | flkL | +0.0018 | 0.2921 |

### L12 H2 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 20  |  total attr: +0.0806

**Key mass** (top-1=81%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0649 | 80.5% |
| 170 | flkL | +0.0143 | 17.7% |
| -1 | other | +0.0014 | 1.8% |

**Query mass** (top-1=21%, top-2=36%, top-3=50%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0171 | 21.3% |
| 310 | ss2 | +0.0123 | 15.2% |
| 170 | flkL | +0.0112 | 13.9% |
| 201 | other | +0.0040 | 5.0% |
| 197 | ss1 | +0.0038 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 1 | 5.0% |
| -140 | 1 | 5.0% |
| +140 | 1 | 5.0% |
| -109 | 1 | 5.0% |
| -113 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 40.0% |
| flkL | ss2 | 6 | 30.0% |
| ss2 | flkL | 3 | 15.0% |
| other | ss2 | 2 | 10.0% |
| ss2 | other | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 310 | ss2 | +0.0171 | 0.5527 |
| 170 | flkL | 310 | ss2 | +0.0112 | 0.4230 |
| 310 | ss2 | 170 | flkL | +0.0108 | 0.2649 |
| 201 | other | 310 | ss2 | +0.0040 | 0.1989 |
| 197 | ss1 | 310 | ss2 | +0.0038 | 0.2638 |

### L14 H0 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 11  |  total attr: +0.0536

**Key mass** (top-1=70%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | flkL | +0.0375 | 70.1% |
| 310 | ss2 | +0.0160 | 29.9% |

**Query mass** (top-1=24%, top-2=45%, top-3=61%)  [DISTR(L310/S197/V193/P195)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0130 | 24.3% |
| 197 | ss1 | +0.0112 | 20.8% |
| 193 | ss1 | +0.0087 | 16.1% |
| 195 | ss1 | +0.0051 | 9.5% |
| 199 | ss1 | +0.0038 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 9.1% |
| +27 | 1 | 9.1% |
| +23 | 1 | 9.1% |
| +25 | 1 | 9.1% |
| +29 | 1 | 9.1% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 54.5% |
| ss2 | ss2 | 2 | 18.2% |
| flkL | flkL | 2 | 18.2% |
| flkR | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 310 | ss2 | 310 | ss2 | +0.0130 | 0.6668 |
| 197 | ss1 | 170 | flkL | +0.0112 | 0.4081 |
| 193 | ss1 | 170 | flkL | +0.0087 | 0.6809 |
| 195 | ss1 | 170 | flkL | +0.0051 | 0.5534 |
| 199 | ss1 | 170 | flkL | +0.0038 | 0.3047 |

### L14 H9 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0806

**Key mass** (top-1=66%, top-2=79%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0536 | 66.5% |
| 170 | flkL | +0.0097 | 12.1% |
| 193 | ss1 | +0.0088 | 11.0% |
| 323 | flkR | +0.0044 | 5.5% |
| 322 | flkR | +0.0021 | 2.6% |

**Query mass** (top-1=27%, top-2=48%, top-3=64%)  [DISTR(L310/V193/G170/G166)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0217 | 27.0% |
| 193 | ss1 | +0.0170 | 21.1% |
| 170 | flkL | +0.0128 | 15.9% |
| 166 | flkL | +0.0083 | 10.3% |
| 174 | flkL | +0.0035 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -117 | 1 | 4.8% |
| -140 | 1 | 4.8% |
| -144 | 1 | 4.8% |
| +117 | 1 | 4.8% |
| +140 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=24%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 5 | 23.8% |
| ss1 | ss2 | 4 | 19.0% |
| ss2 | flkL | 4 | 19.0% |
| ss2 | flkR | 2 | 9.5% |
| ss2 | ss1 | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 310 | ss2 | +0.0155 | 0.7431 |
| 170 | flkL | 310 | ss2 | +0.0128 | 0.9629 |
| 166 | flkL | 310 | ss2 | +0.0083 | 0.8200 |
| 310 | ss2 | 193 | ss1 | +0.0073 | 0.2868 |
| 310 | ss2 | 170 | flkL | +0.0051 | 0.1258 |

### L14 H13 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0801

**Key mass** (top-1=78%, top-2=86%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 170 | flkL | +0.0623 | 77.8% |
| 193 | ss1 | +0.0063 | 7.9% |
| 310 | ss2 | +0.0037 | 4.6% |
| 314 | ss2 | +0.0037 | 4.6% |
| 195 | ss1 | +0.0022 | 2.7% |

**Query mass** (top-1=33%, top-2=47%, top-3=56%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0263 | 32.8% |
| 195 | ss1 | +0.0110 | 13.8% |
| 197 | ss1 | +0.0079 | 9.8% |
| 192 | ss1 | +0.0046 | 5.7% |
| 186 | flkL | +0.0038 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 2 | 9.5% |
| +2 | 2 | 9.5% |
| +23 | 1 | 4.8% |
| +25 | 1 | 4.8% |
| +0 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 7 | 33.3% |
| flkL | flkL | 6 | 28.6% |
| ss1 | ss1 | 4 | 19.0% |
| flkR | ss2 | 2 | 9.5% |
| ss2 | ss2 | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | ss1 | 170 | flkL | +0.0213 | 0.7402 |
| 195 | ss1 | 170 | flkL | +0.0110 | 0.3844 |
| 193 | ss1 | 193 | ss1 | +0.0049 | 0.1839 |
| 192 | ss1 | 170 | flkL | +0.0046 | 0.7719 |
| 186 | flkL | 170 | flkL | +0.0038 | 0.8479 |

### L15 H14 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:ss1  |  cells: 6  |  total attr: +0.0428

**Key mass** (top-1=78%, top-2=94%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0336 | 78.5% |
| 193 | ss1 | +0.0066 | 15.3% |
| 306 | ss2 | +0.0014 | 3.2% |
| 196 | ss1 | +0.0013 | 3.0% |

**Query mass** (top-1=50%, top-2=78%, top-3=88%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 305 | other | +0.0214 | 49.9% |
| 307 | ss2 | +0.0122 | 28.6% |
| 192 | ss1 | +0.0041 | 9.7% |
| 191 | ss1 | +0.0024 | 5.7% |
| 302 | other | +0.0014 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 2 | 33.3% |
| -5 | 1 | 16.7% |
| -1 | 1 | 16.7% |
| -2 | 1 | 16.7% |
| -4 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 50.0% |
| other | ss2 | 2 | 33.3% |
| ss2 | ss2 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 305 | other | 310 | ss2 | +0.0214 | 0.6935 |
| 307 | ss2 | 310 | ss2 | +0.0122 | 0.3648 |
| 192 | ss1 | 193 | ss1 | +0.0041 | 0.5576 |
| 191 | ss1 | 193 | ss1 | +0.0024 | 0.5329 |
| 302 | other | 306 | ss2 | +0.0014 | 0.3084 |

### L17 H10 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0707

**Key mass** (top-1=55%, top-2=88%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0391 | 55.3% |
| 310 | ss2 | +0.0228 | 32.2% |
| 309 | ss2 | +0.0055 | 7.8% |
| 177 | flkL | +0.0020 | 2.8% |
| 164 | flkL | +0.0013 | 1.9% |

**Query mass** (top-1=31%, top-2=62%, top-3=73%)  [DISTR(S197/A307/A198)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss1 | +0.0219 | 31.1% |
| 307 | ss2 | +0.0219 | 31.0% |
| 198 | ss1 | +0.0074 | 10.4% |
| 192 | ss1 | +0.0055 | 7.7% |
| 199 | ss1 | +0.0023 | 3.3% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 3 | 23.1% |
| +4 | 2 | 15.4% |
| -2 | 2 | 15.4% |
| -4 | 2 | 15.4% |
| -3 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 38.5% |
| ss2 | ss2 | 5 | 38.5% |
| flkL | flkL | 2 | 15.4% |
| other | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 197 | ss1 | 193 | ss1 | +0.0219 | 0.8383 |
| 307 | ss2 | 310 | ss2 | +0.0186 | 0.5492 |
| 198 | ss1 | 193 | ss1 | +0.0074 | 0.8629 |
| 192 | ss1 | 193 | ss1 | +0.0055 | 0.8634 |
| 307 | ss2 | 309 | ss2 | +0.0034 | 0.2228 |

### L17 H18 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 13  |  total attr: +0.0292

**Key mass** (top-1=27%, top-2=44%, top-3=59%)  [DISTR(P195/V193/L164/G324/L310)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 195 | ss1 | +0.0080 | 27.3% |
| 193 | ss1 | +0.0048 | 16.4% |
| 164 | flkL | +0.0044 | 15.1% |
| 324 | flkR | +0.0026 | 8.8% |
| 310 | ss2 | +0.0024 | 8.1% |

**Query mass** (top-1=23%, top-2=36%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0068 | 23.4% |
| 311 | ss2 | +0.0038 | 12.9% |
| 307 | ss2 | +0.0033 | 11.4% |
| 309 | ss2 | +0.0029 | 9.7% |
| 312 | ss2 | +0.0028 | 9.7% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 15.4% |
| +114 | 2 | 15.4% |
| +117 | 2 | 15.4% |
| +29 | 1 | 7.7% |
| -131 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 46.2% |
| ss1 | flkL | 3 | 23.1% |
| ss1 | flkR | 1 | 7.7% |
| flkR | ss2 | 1 | 7.7% |
| ss1 | ss1 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 311 | ss2 | 195 | ss1 | +0.0038 | 0.5049 |
| 307 | ss2 | 193 | ss1 | +0.0033 | 0.0604 |
| 193 | ss1 | 164 | flkL | +0.0030 | 0.5042 |
| 312 | ss2 | 195 | ss1 | +0.0028 | 0.5648 |
| 193 | ss1 | 324 | flkR | +0.0026 | 0.1623 |

### L19 H0 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 20  |  total attr: +0.0749

**Key mass** (top-1=26%, top-2=47%, top-3=56%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 310 | ss2 | +0.0196 | 26.2% |
| 193 | ss1 | +0.0157 | 21.0% |
| 320 | flkR | +0.0066 | 8.8% |
| 170 | flkL | +0.0041 | 5.5% |
| 176 | flkL | +0.0041 | 5.4% |

**Query mass** (top-1=33%, top-2=49%, top-3=60%)  [DISTR(L311/P195/F178/A328/L181)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 311 | ss2 | +0.0244 | 32.6% |
| 195 | ss1 | +0.0121 | 16.2% |
| 178 | flkL | +0.0082 | 11.0% |
| 328 | flkR | +0.0066 | 8.8% |
| 181 | flkL | +0.0038 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 8 | 40.0% |
| +8 | 4 | 20.0% |
| +7 | 4 | 20.0% |
| +1 | 2 | 10.0% |
| +3 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 35.0% |
| ss2 | ss2 | 4 | 20.0% |
| ss1 | ss1 | 3 | 15.0% |
| other | ss1 | 2 | 10.0% |
| flkR | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 311 | ss2 | 310 | ss2 | +0.0171 | 0.9291 |
| 195 | ss1 | 193 | ss1 | +0.0121 | 0.8361 |
| 328 | flkR | 320 | flkR | +0.0066 | 0.6129 |
| 178 | flkL | 170 | flkL | +0.0041 | 0.6957 |
| 178 | flkL | 176 | flkL | +0.0041 | 0.3739 |

### L22 H14 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 13  |  total attr: +0.0862

**Key mass** (top-1=56%, top-2=69%, top-3=79%)  [DISTR(S197/V193/P195)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 197 | ss1 | +0.0487 | 56.5% |
| 193 | ss1 | +0.0112 | 12.9% |
| 195 | ss1 | +0.0080 | 9.3% |
| 165 | flkL | +0.0059 | 6.8% |
| 194 | ss1 | +0.0029 | 3.4% |

**Query mass** (top-1=46%, top-2=58%, top-3=68%)  [DISTR(G313/A307/T314/L309)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 313 | ss2 | +0.0399 | 46.3% |
| 307 | ss2 | +0.0099 | 11.5% |
| 314 | ss2 | +0.0088 | 10.2% |
| 309 | ss2 | +0.0087 | 10.0% |
| 195 | ss1 | +0.0059 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 46%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 3 | 23.1% |
| +117 | 3 | 23.1% |
| +114 | 2 | 15.4% |
| +118 | 2 | 15.4% |
| +30 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=77%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 10 | 76.9% |
| ss1 | flkL | 3 | 23.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 313 | ss2 | 197 | ss1 | +0.0399 | 0.7901 |
| 314 | ss2 | 197 | ss1 | +0.0088 | 0.5818 |
| 307 | ss2 | 193 | ss1 | +0.0081 | 0.0590 |
| 195 | ss1 | 165 | flkL | +0.0059 | 0.5519 |
| 309 | ss2 | 195 | ss1 | +0.0056 | 0.0888 |

### L24 H18 — Rank #14

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS_SSE  |  cells: 3  |  total attr: +0.0089

**Key mass** (top-1=58%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0051 | 57.6% |
| 174 | flkL | +0.0038 | 42.4% |

**Query mass** (top-1=58%, top-2=86%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0051 | 57.6% |
| 195 | ss1 | +0.0025 | 28.2% |
| 320 | flkR | +0.0013 | 14.2% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 1 | 33.3% |
| +21 | 1 | 33.3% |
| +146 | 1 | 33.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 1 | 33.3% |
| ss1 | flkL | 1 | 33.3% |
| flkR | flkL | 1 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 193 | ss1 | +0.0051 | 0.0513 |
| 195 | ss1 | 174 | flkL | +0.0025 | 0.1532 |
| 320 | flkR | 174 | flkL | +0.0013 | 0.2231 |

### L26 H16 — Rank #26

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 9  |  total attr: +0.0246

**Key mass** (top-1=21%, top-2=41%, top-3=60%)  [DISTR(G313/A307/D337/L311)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 313 | ss2 | +0.0052 | 21.3% |
| 307 | ss2 | +0.0049 | 20.0% |
| 337 | flkR | +0.0047 | 19.1% |
| 311 | ss2 | +0.0032 | 13.0% |
| 336 | flkR | +0.0028 | 11.2% |

**Query mass** (top-1=40%, top-2=61%, top-3=72%)  [DISTR(A307/S197/V190)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0098 | 39.9% |
| 197 | ss1 | +0.0052 | 21.3% |
| 190 | ss1 | +0.0026 | 10.4% |
| 174 | flkL | +0.0019 | 7.9% |
| 192 | ss1 | +0.0019 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -116 | 2 | 22.2% |
| -30 | 1 | 11.1% |
| -29 | 1 | 11.1% |
| -117 | 1 | 11.1% |
| +0 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 44.4% |
| ss2 | flkR | 2 | 22.2% |
| ss2 | ss2 | 1 | 11.1% |
| flkL | ss1 | 1 | 11.1% |
| flkR | ss2 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 197 | ss1 | 313 | ss2 | +0.0052 | 0.1356 |
| 307 | ss2 | 337 | flkR | +0.0047 | 0.2038 |
| 307 | ss2 | 336 | flkR | +0.0028 | 0.1638 |
| 190 | ss1 | 307 | ss2 | +0.0026 | 0.1287 |
| 307 | ss2 | 307 | ss2 | +0.0023 | 0.1240 |

### L27 H15 — Rank #8

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→ss1  |  cells: 9  |  total attr: +0.0721

**Key mass** (top-1=59%, top-2=77%, top-3=85%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0424 | 58.8% |
| 195 | ss1 | +0.0131 | 18.1% |
| 174 | flkL | +0.0057 | 7.9% |
| 167 | flkL | +0.0029 | 4.1% |
| 192 | ss1 | +0.0028 | 3.8% |

**Query mass** (top-1=61%, top-2=81%, top-3=89%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0438 | 60.7% |
| 309 | ss2 | +0.0146 | 20.3% |
| 195 | ss1 | +0.0057 | 7.9% |
| 196 | ss1 | +0.0029 | 4.1% |
| 314 | ss2 | +0.0023 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 22.2% |
| +116 | 2 | 22.2% |
| +21 | 1 | 11.1% |
| +29 | 1 | 11.1% |
| -29 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 55.6% |
| ss1 | flkL | 2 | 22.2% |
| ss2 | flkR | 2 | 22.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 193 | ss1 | +0.0424 | 0.3797 |
| 309 | ss2 | 195 | ss1 | +0.0131 | 0.1623 |
| 195 | ss1 | 174 | flkL | +0.0057 | 0.4480 |
| 196 | ss1 | 167 | flkL | +0.0029 | 0.1618 |
| 314 | ss2 | 343 | flkR | +0.0023 | 0.3008 |

### L29 H18 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.0473

**Key mass** (top-1=35%, top-2=46%, top-3=56%)  [DISTR(F178/A328/T174/?377/G171)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 178 | flkL | +0.0163 | 34.6% |
| 328 | flkR | +0.0055 | 11.5% |
| 174 | flkL | +0.0047 | 10.0% |
| 377 | other | +0.0038 | 8.0% |
| 171 | flkL | +0.0031 | 6.6% |

**Query mass** (top-1=24%, top-2=40%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0112 | 23.6% |
| 195 | ss1 | +0.0079 | 16.7% |
| 193 | ss1 | +0.0052 | 10.9% |
| 313 | ss2 | +0.0044 | 9.3% |
| 200 | other | +0.0041 | 8.6% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +129 | 1 | 6.7% |
| +15 | 1 | 6.7% |
| +21 | 1 | 6.7% |
| -128 | 1 | 6.7% |
| +24 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 26.7% |
| ss2 | flkR | 3 | 20.0% |
| ss2 | flkL | 2 | 13.3% |
| ss1 | ss2 | 2 | 13.3% |
| other | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 178 | flkL | +0.0112 | 0.3772 |
| 193 | ss1 | 178 | flkL | +0.0052 | 0.7868 |
| 195 | ss1 | 174 | flkL | +0.0047 | 0.5168 |
| 200 | other | 328 | flkR | +0.0041 | 0.4031 |
| 195 | ss1 | 171 | flkL | +0.0031 | 0.0870 |

### L30 H0 — Rank #27

**Tags:** k:MULTI-ANCHOR / q:MULTI-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 4  |  total attr: +0.0157

**Key mass** (top-1=45%, top-2=68%, top-3=90%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0070 | 44.8% |
| 197 | ss1 | +0.0037 | 23.3% |
| 307 | ss2 | +0.0034 | 21.6% |
| 194 | ss1 | +0.0016 | 10.3% |

**Query mass** (top-1=45%, top-2=68%, top-3=90%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0070 | 44.8% |
| 313 | ss2 | +0.0037 | 23.3% |
| 193 | ss1 | +0.0034 | 21.6% |
| 312 | ss2 | +0.0016 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 1 | 25.0% |
| +116 | 1 | 25.0% |
| -114 | 1 | 25.0% |
| +118 | 1 | 25.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 75.0% |
| ss1 | ss2 | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 193 | ss1 | +0.0070 | 0.3031 |
| 313 | ss2 | 197 | ss1 | +0.0037 | 0.2148 |
| 193 | ss1 | 307 | ss2 | +0.0034 | 0.0781 |
| 312 | ss2 | 194 | ss1 | +0.0016 | 0.2565 |

### L30 H1 — Rank #15

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 7  |  total attr: +0.0219

**Key mass** (top-1=54%, top-2=82%, top-3=94%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0118 | 54.0% |
| 195 | ss1 | +0.0061 | 28.1% |
| 308 | ss2 | +0.0025 | 11.4% |
| 190 | ss1 | +0.0014 | 6.4% |

**Query mass** (top-1=48%, top-2=73%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0104 | 47.7% |
| 309 | ss2 | +0.0056 | 25.6% |
| 192 | ss1 | +0.0025 | 11.4% |
| 311 | ss2 | +0.0019 | 8.9% |
| 195 | ss1 | +0.0014 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 28.6% |
| +116 | 2 | 28.6% |
| -116 | 1 | 14.3% |
| +117 | 1 | 14.3% |
| +0 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 71.4% |
| ss1 | ss2 | 1 | 14.3% |
| ss1 | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 193 | ss1 | +0.0090 | 0.0890 |
| 309 | ss2 | 195 | ss1 | +0.0028 | 0.0425 |
| 309 | ss2 | 193 | ss1 | +0.0028 | 0.4656 |
| 192 | ss1 | 308 | ss2 | +0.0025 | 0.3848 |
| 311 | ss2 | 195 | ss1 | +0.0019 | 0.4350 |

### L32 H13 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 9  |  total attr: +0.0396

**Key mass** (top-1=30%, top-2=47%, top-3=58%)  [DISTR(V193/A307/P195/S197/G313)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | ss1 | +0.0119 | 30.0% |
| 307 | ss2 | +0.0067 | 16.8% |
| 195 | ss1 | +0.0045 | 11.5% |
| 197 | ss1 | +0.0040 | 10.0% |
| 313 | ss2 | +0.0038 | 9.7% |

**Query mass** (top-1=30%, top-2=47%, top-3=60%)  [DISTR(A307/V193/S197/L309)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0119 | 30.0% |
| 193 | ss1 | +0.0067 | 16.8% |
| 197 | ss1 | +0.0053 | 13.3% |
| 309 | ss2 | +0.0045 | 11.5% |
| 313 | ss2 | +0.0040 | 10.0% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 22.2% |
| -114 | 2 | 22.2% |
| +116 | 1 | 11.1% |
| -116 | 1 | 11.1% |
| +118 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 55.6% |
| ss2 | ss1 | 4 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 193 | ss1 | +0.0119 | 0.0732 |
| 193 | ss1 | 307 | ss2 | +0.0067 | 0.0411 |
| 309 | ss2 | 195 | ss1 | +0.0045 | 0.0453 |
| 313 | ss2 | 197 | ss1 | +0.0040 | 0.0542 |
| 197 | ss1 | 313 | ss2 | +0.0038 | 0.0525 |

### L32 H18 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0536

**Key mass** (top-1=31%, top-2=53%, top-3=64%)  [DISTR(A192/V193/A307/L309)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 192 | ss1 | +0.0165 | 30.8% |
| 193 | ss1 | +0.0118 | 22.1% |
| 307 | ss2 | +0.0058 | 10.9% |
| 309 | ss2 | +0.0055 | 10.2% |
| 195 | ss1 | +0.0049 | 9.2% |

**Query mass** (top-1=35%, top-2=47%, top-3=58%)  [DISTR(A307/L309/V193/P195/G313)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 307 | ss2 | +0.0189 | 35.3% |
| 309 | ss2 | +0.0065 | 12.2% |
| 193 | ss1 | +0.0058 | 10.9% |
| 195 | ss1 | +0.0055 | 10.2% |
| 313 | ss2 | +0.0049 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 45%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 3 | 27.3% |
| +114 | 2 | 18.2% |
| -114 | 2 | 18.2% |
| +118 | 2 | 18.2% |
| +115 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 72.7% |
| ss1 | ss2 | 3 | 27.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 307 | ss2 | 193 | ss1 | +0.0102 | 0.0384 |
| 307 | ss2 | 192 | ss1 | +0.0087 | 0.1499 |
| 193 | ss1 | 307 | ss2 | +0.0058 | 0.0219 |
| 195 | ss1 | 309 | ss2 | +0.0055 | 0.0332 |
| 309 | ss2 | 195 | ss1 | +0.0049 | 0.0300 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #10 | L5 | H7 | 6 | +0.0610 | SINGLE-ANCHOR | G166 | SINGLE-ANCHOR | L310 |  |  |
| #2 | L5 | H19 | 2 | +0.1666 | SINGLE-ANCHOR | G166 | SINGLE-ANCHOR | V193 |  | ss1→flkL |
| #5 | L6 | H8 | 1 | +0.1145 | SINGLE-ANCHOR | P321 | SINGLE-ANCHOR | L310 |  | ss2→flkR |
| #13 | L6 | H19 | 7 | +0.0921 | SINGLE-ANCHOR | V193 | SINGLE-ANCHOR | L310 |  |  |
| #28 | L7 | H0 | 2 | +0.0457 | SINGLE-ANCHOR | V193 | SINGLE-ANCHOR | L164 |  | flkL→ss1 |
| #21 | L7 | H4 | 4 | +0.0736 | SINGLE-ANCHOR | L310 | DUAL-ANCHOR | L164/V193 |  | CROSS:flkL→ss2 |
| #3 | L8 | H12 | 4 | +0.2241 | SINGLE-ANCHOR | L164 | SINGLE-ANCHOR | L310 |  | CROSS:flkL→ss2 |
| #24 | L9 | H3 | 13 | +0.0646 | SINGLE-ANCHOR | L310 | DISTRIBUTED | L310/L164/F332/A328 |  |  |
| #6 | L9 | H7 | 6 | +0.1470 | SINGLE-ANCHOR | L310 | SINGLE-ANCHOR | V193 |  |  |
| #30 | L10 | H0 | 16 | +0.0540 | DUAL-ANCHOR | V193/L164 | DISTRIBUTED |  |  |  |
| #1 | L10 | H9 | 26 | +0.2628 | SINGLE-ANCHOR | L310 | DISTRIBUTED | V193/L310/L164/G170 |  |  |
| #17 | L11 | H6 | 10 | +0.0514 | DISTRIBUTED | A328/K334/K342 | SINGLE-ANCHOR | L310 |  | ss2→flkR |
| #25 | L11 | H19 | 6 | +0.0373 | SINGLE-ANCHOR | G170 | DUAL-ANCHOR | V193/P195 |  | ss1→flkL |
| #11 | L12 | H2 | 20 | +0.0806 | SINGLE-ANCHOR | L310 | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #19 | L14 | H0 | 11 | +0.0536 | SINGLE-ANCHOR | G170 | DISTRIBUTED | L310/S197/V193/P195 |  | ss1→flkL |
| #16 | L14 | H9 | 21 | +0.0806 | SINGLE-ANCHOR | L310 | DISTRIBUTED | L310/V193/G170/G166 |  |  |
| #22 | L14 | H13 | 21 | +0.0801 | SINGLE-ANCHOR | G170 | DISTRIBUTED |  |  |  |
| #29 | L15 | H14 | 6 | +0.0428 | SINGLE-ANCHOR | L310 | DUAL-ANCHOR | P305/A307 |  | INTRA:ss1 |
| #20 | L17 | H10 | 13 | +0.0707 | DUAL-ANCHOR | V193/L310 | DISTRIBUTED | S197/A307/A198 |  |  |
| #23 | L17 | H18 | 13 | +0.0292 | DISTRIBUTED | P195/V193/L164/G324/L310 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #9 | L19 | H0 | 20 | +0.0749 | DISTRIBUTED |  | DISTRIBUTED | L311/P195/F178/A328/L181 | POSITIONAL |  |
| #4 | L22 | H14 | 13 | +0.0862 | DISTRIBUTED | S197/V193/P195 | DISTRIBUTED | G313/A307/T314/L309 |  | CROSS:ss2→ss1 |
| #14 | L24 | H18 | 3 | +0.0089 | DUAL-ANCHOR | V193/T174 | DUAL-ANCHOR | A307/P195 | CROSS_SSE |  |
| #26 | L26 | H16 | 9 | +0.0246 | DISTRIBUTED | G313/A307/D337/L311 | DISTRIBUTED | A307/S197/V190 |  | CROSS:ss1→ss2 |
| #8 | L27 | H15 | 9 | +0.0721 | DUAL-ANCHOR | V193/P195 | SINGLE-ANCHOR | A307 |  | CROSS:ss2→ss1 |
| #18 | L29 | H18 | 15 | +0.0473 | DISTRIBUTED | F178/A328/T174/?377/G171 | DISTRIBUTED |  |  |  |
| #27 | L30 | H0 | 4 | +0.0157 | MULTI-ANCHOR |  | MULTI-ANCHOR |  | CROSS_SSE | CROSS:ss2→ss1 |
| #15 | L30 | H1 | 7 | +0.0219 | DUAL-ANCHOR | V193/P195 | DUAL-ANCHOR | A307/L309 | CROSS_SSE | CROSS:ss2→ss1 |
| #12 | L32 | H13 | 9 | +0.0396 | DISTRIBUTED | V193/A307/P195/S197/G313 | DISTRIBUTED | A307/V193/S197/L309 |  | CROSS:ss1→ss2 |
| #7 | L32 | H18 | 11 | +0.0536 | DISTRIBUTED | A192/V193/A307/L309 | DISTRIBUTED | A307/L309/V193/P195/G313 |  | CROSS:ss2→ss1 |
