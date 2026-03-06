# Contact Pattern Analysis: 1PVGA

Generated: 2026-03-03 05:16:44   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1PVGA |
| Contact pair | (101, 202) |
| ss1 | [96, 107) |
| ss2 | [197, 208) |
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
| Clean metric | 0.5921 |
| Corrupt metric | 0.0644 |
| Gap | 0.5277 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 81.36% |
| positive IE | 45 | 72.85% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L10 | H9 | +0.3197 |
| 2 | L9 | H17 | +0.3126 |
| 3 | L27 | H15 | +0.2173 |
| 4 | L32 | H13 | +0.2038 |
| 5 | L7 | H13 | +0.1766 |
| 6 | L29 | H18 | +0.1581 |
| 7 | L5 | H9 | +0.1439 |
| 8 | L17 | H10 | +0.1326 |
| 9 | L32 | H18 | +0.1291 |
| 10 | L0 | H9 | +0.1244 |
| 11 | L11 | H16 | +0.1219 |
| 12 | L8 | H2 | +0.1167 |
| 13 | L15 | H8 | +0.1133 |
| 14 | L14 | H4 | +0.1042 |
| 15 | L26 | H16 | +0.1026 |
| 16 | L12 | H10 | +0.0955 |
| 17 | L6 | H0 | +0.0862 |
| 18 | L7 | H7 | +0.0824 |
| 19 | L0 | H12 | +0.0692 |
| 20 | L14 | H9 | +0.0691 |
| 21 | L6 | H17 | +0.0639 |
| 22 | L13 | H18 | +0.0585 |
| 23 | L1 | H1 | +0.0571 |
| 24 | L17 | H18 | +0.0510 |
| 25 | L4 | H5 | +0.0474 |
| 26 | L4 | H14 | +0.0468 |
| 27 | L13 | H2 | +0.0465 |
| 28 | L11 | H14 | +0.0450 |
| 29 | L9 | H15 | +0.0423 |
| 30 | L12 | H15 | +0.0416 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.68% |
| 4 | 1.03% |
| 5 | 1.06% |
| 6 | 2.24% |
| 7 | 2.81% |
| 8 | 2.93% |
| 9 | 3.21% |
| 10 | 3.80% |
| 20 | 22.96% |
| 80 | 116.04% |
| 450 | 188.34% |

## Cell Attribution Analysis

Total cells: 7,257,508

- Positive: 3,777,881
- Negative: 3,476,288

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000066 | 725,752 |
| 95th | +0.00000187 | 362,876 |
| 99th | +0.00001250 | 72,576 |
| 99.5th | +0.00002615 | 36,288 |
| 99.9th | +0.00013213 | 7,258 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H9 | 101 | ss1 | 97 | ss1 | +0.169906 | 0.033740 |
| L14 | H4 | 201 | ss2 | 101 | ss1 | +0.115508 | 0.147846 |
| L15 | H8 | 201 | ss2 | 101 | ss1 | +0.087855 | 0.199882 |
| L7 | H13 | 217 | flkR | 270 | flkR | +0.077376 | 0.259494 |
| L7 | H13 | 270 | flkR | 217 | flkR | +0.074264 | 0.384853 |
| L10 | H9 | 201 | ss2 | 101 | ss1 | +0.067942 | 0.124056 |
| L17 | H10 | 203 | ss2 | 201 | ss2 | +0.063839 | 0.447278 |
| L4 | H5 | 97 | ss1 | 92 | flkL | +0.044080 | 0.008301 |
| L7 | H13 | 262 | flkR | 36 | flkL | +0.039415 | 0.514999 |
| L6 | H17 | 101 | ss1 | 90 | flkL | +0.031315 | 0.018693 |
| L14 | H9 | 201 | ss2 | 101 | ss1 | +0.030856 | 0.048672 |
| L29 | H18 | 102 | ss1 | 200 | ss2 | +0.030207 | 0.440083 |
| L10 | H9 | 101 | ss1 | 101 | ss1 | +0.028834 | 0.037178 |
| L27 | H15 | 200 | ss2 | 102 | ss1 | +0.026381 | 0.230922 |
| L6 | H0 | 101 | ss1 | 32 | flkL | +0.026196 | 0.023941 |
| L2 | H18 | 71 | flkL | 70 | flkL | +0.025440 | 0.009518 |
| L7 | H13 | 33 | flkL | 33 | flkL | +0.025324 | 0.518343 |
| L15 | H8 | 203 | ss2 | 101 | ss1 | +0.024998 | 0.133244 |
| L14 | H4 | 203 | ss2 | 101 | ss1 | +0.024102 | 0.109526 |
| L1 | H1 | 30 | other | 32 | flkL | +0.022740 | 0.146341 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H13 | 217 | flkR | 253 | flkR | -0.010442 | 0.047483 |
| L0 | H9 | 97 | ss1 | 32 | flkL | -0.010446 | 0.002601 |
| L6 | H17 | 271 | flkR | 232 | flkR | -0.010650 | 0.087548 |
| L7 | H13 | 32 | flkL | 198 | ss2 | -0.011418 | 0.273755 |
| L6 | H17 | 32 | flkL | 46 | flkL | -0.011447 | 0.216032 |
| L11 | H16 | 201 | ss2 | 101 | ss1 | -0.011580 | 0.030287 |
| L1 | H1 | 270 | flkR | 272 | other | -0.011790 | 0.148494 |
| L9 | H17 | 101 | ss1 | 137 | other | -0.012895 | 0.012472 |
| L7 | H13 | 270 | flkR | 231 | flkR | -0.015258 | 0.123589 |
| L7 | H7 | 32 | flkL | 101 | ss1 | -0.015510 | 0.195875 |
| L10 | H9 | 197 | ss2 | 101 | ss1 | -0.015528 | 0.103193 |
| L7 | H13 | 36 | flkL | 262 | flkR | -0.018070 | 0.531209 |
| L11 | H14 | 197 | ss2 | 101 | ss1 | -0.019734 | 0.096351 |
| L7 | H13 | 215 | flkR | 268 | flkR | -0.022712 | 0.067188 |
| L6 | H17 | 270 | flkR | 217 | flkR | -0.023551 | 0.067452 |
| L7 | H13 | 217 | flkR | 217 | flkR | -0.027279 | 0.182727 |
| L5 | H9 | 101 | ss1 | 95 | flkL | -0.029439 | 0.009209 |
| L7 | H7 | 101 | ss1 | 101 | ss1 | -0.029958 | 0.047568 |
| L6 | H17 | 31 | other | 45 | flkL | -0.030004 | 0.195811 |
| L9 | H17 | 201 | ss2 | 101 | ss1 | -0.048657 | 0.054819 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0644 | 0.00% |
| 10 | 10 | 8 | 0.0644 | 0.00% |
| 20 | 20 | 14 | 0.0664 | 0.38% |
| 50 | 50 | 24 | 0.0729 | 1.60% |
| 100 | 100 | 29 | 0.0931 | 5.44% |
| 200 | 200 | 41 | 0.1566 | 17.46% |
| 500 | 500 | 43 | 0.2908 | 42.89% |
| 1000 | 1,000 | 45 | 0.4454 | 72.20% |
| 2000 | 2,000 | 45 | 0.5164 | 85.65% |
| 5000 | 5,000 | 45 | 0.5980 | 101.10% |
| 10000 | 10,000 | 45 | 0.6490 | 110.78% |
| 20000 | 20,000 | 45 | 0.6573 | 112.35% |
| 50000 | 50,000 | 45 | 0.7091 | 122.16% |

## Motif Analysis

### L0 H9 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 45  |  total attr: +0.2003

**Key mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.1948 | 97.3% |
| 271 | flkR | +0.0055 | 2.7% |

**Query mass** (top-1=9%, top-2=16%, top-3=23%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 90 | flkL | +0.0180 | 9.0% |
| 101 | ss1 | +0.0147 | 7.4% |
| 88 | flkL | +0.0133 | 6.6% |
| 68 | flkL | +0.0129 | 6.5% |
| 99 | ss1 | +0.0119 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 4.4% |
| +58 | 1 | 2.2% |
| +69 | 1 | 2.2% |
| +56 | 1 | 2.2% |
| +36 | 1 | 2.2% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 28 | 62.2% |
| ss1 | flkL | 8 | 17.8% |
| flkR | flkR | 5 | 11.1% |
| other | flkL | 4 | 8.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 90 | flkL | 32 | flkL | +0.0180 | 0.0032 |
| 101 | ss1 | 32 | flkL | +0.0147 | 0.0026 |
| 88 | flkL | 32 | flkL | +0.0133 | 0.0034 |
| 68 | flkL | 32 | flkL | +0.0129 | 0.0047 |
| 99 | ss1 | 32 | flkL | +0.0119 | 0.0027 |

### L0 H12 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 32  |  total attr: +0.0634

**Key mass** (top-1=55%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0351 | 55.4% |
| 271 | flkR | +0.0283 | 44.6% |

**Query mass** (top-1=8%, top-2=16%, top-3=22%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | flkL | +0.0052 | 8.1% |
| 52 | flkL | +0.0048 | 7.5% |
| 73 | flkL | +0.0042 | 6.7% |
| 267 | flkR | +0.0038 | 5.9% |
| 72 | flkL | +0.0036 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +43 | 1 | 3.1% |
| +20 | 1 | 3.1% |
| +41 | 1 | 3.1% |
| -4 | 1 | 3.1% |
| -199 | 1 | 3.1% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 14 | 43.8% |
| flkR | flkR | 8 | 25.0% |
| ss2 | flkR | 4 | 12.5% |
| flkL | flkR | 3 | 9.4% |
| ss1 | flkL | 2 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | flkL | 32 | flkL | +0.0052 | 0.0036 |
| 52 | flkL | 32 | flkL | +0.0048 | 0.0098 |
| 73 | flkL | 32 | flkL | +0.0042 | 0.0038 |
| 267 | flkR | 271 | flkR | +0.0038 | 0.0163 |
| 72 | flkL | 271 | flkR | +0.0036 | 0.0018 |

### L1 H1 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL  |  cells: 28  |  total attr: +0.0976

**Key mass** (top-1=23%, top-2=47%, top-3=52%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 271 | flkR | +0.0229 | 23.4% |
| 32 | flkL | +0.0227 | 23.3% |
| 74 | flkL | +0.0056 | 5.7% |
| 100 | ss1 | +0.0055 | 5.6% |
| 92 | flkL | +0.0048 | 4.9% |

**Query mass** (top-1=26%, top-2=40%, top-3=48%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 30 | other | +0.0257 | 26.4% |
| 270 | flkR | +0.0133 | 13.7% |
| 269 | flkR | +0.0081 | 8.3% |
| 90 | flkL | +0.0078 | 8.0% |
| 201 | ss2 | +0.0078 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 79%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 14 | 50.0% |
| -3 | 8 | 28.6% |
| -1 | 6 | 21.4% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 10 | 35.7% |
| flkR | flkR | 5 | 17.9% |
| other | flkL | 3 | 10.7% |
| ss1 | ss1 | 3 | 10.7% |
| ss2 | ss2 | 3 | 10.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 30 | other | 32 | flkL | +0.0227 | 0.1463 |
| 270 | flkR | 271 | flkR | +0.0133 | 0.1818 |
| 72 | flkL | 74 | flkL | +0.0056 | 0.0020 |
| 269 | flkR | 271 | flkR | +0.0056 | 0.1413 |
| 97 | ss1 | 100 | ss1 | +0.0055 | 0.0017 |

### L4 H5 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 9  |  total attr: +0.0627

**Key mass** (top-1=70%, top-2=86%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | flkL | +0.0441 | 70.3% |
| 90 | flkL | +0.0101 | 16.1% |
| 95 | flkL | +0.0020 | 3.2% |
| 271 | flkR | +0.0013 | 2.1% |
| 268 | flkR | +0.0012 | 1.9% |

**Query mass** (top-1=94%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0591 | 94.3% |
| 239 | flkR | +0.0013 | 2.1% |
| 72 | flkL | +0.0012 | 1.9% |
| 101 | ss1 | +0.0010 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +5 | 1 | 11.1% |
| +7 | 1 | 11.1% |
| +2 | 1 | 11.1% |
| -32 | 1 | 11.1% |
| -196 | 1 | 11.1% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 66.7% |
| flkR | flkR | 1 | 11.1% |
| flkL | flkR | 1 | 11.1% |
| ss1 | ss1 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 92 | flkL | +0.0441 | 0.0083 |
| 97 | ss1 | 90 | flkL | +0.0101 | 0.0035 |
| 97 | ss1 | 95 | flkL | +0.0020 | 0.0004 |
| 239 | flkR | 271 | flkR | +0.0013 | 0.0149 |
| 72 | flkL | 268 | flkR | +0.0012 | 0.0010 |

### L4 H14 — Rank #26

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.0242

**Key mass** (top-1=56%, top-2=69%, top-3=75%)  [DISTR(N270/K264/G271)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 270 | flkR | +0.0136 | 56.2% |
| 264 | flkR | +0.0030 | 12.6% |
| 271 | flkR | +0.0015 | 6.4% |
| 268 | flkR | +0.0014 | 5.9% |
| 58 | flkL | +0.0013 | 5.2% |

**Query mass** (top-1=63%, top-2=74%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0152 | 62.8% |
| 71 | flkL | +0.0028 | 11.6% |
| 199 | ss2 | +0.0014 | 5.9% |
| 32 | flkL | +0.0014 | 5.6% |
| 51 | flkL | +0.0012 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -69 | 2 | 18.2% |
| -169 | 1 | 9.1% |
| -163 | 1 | 9.1% |
| -200 | 1 | 9.1% |
| -232 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 3 | 27.3% |
| flkL | flkR | 3 | 27.3% |
| ss2 | flkR | 2 | 18.2% |
| flkL | flkL | 1 | 9.1% |
| flkR | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 270 | flkR | +0.0114 | 0.0031 |
| 101 | ss1 | 264 | flkR | +0.0017 | 0.0009 |
| 71 | flkL | 271 | flkR | +0.0015 | 0.0027 |
| 199 | ss2 | 268 | flkR | +0.0014 | 0.0155 |
| 32 | flkL | 264 | flkR | +0.0014 | 0.0061 |

### L5 H9 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 13  |  total attr: +0.1915

**Key mass** (top-1=90%, top-2=92%, top-3=94%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.1728 | 90.3% |
| 243 | flkR | +0.0037 | 1.9% |
| 101 | ss1 | +0.0028 | 1.4% |
| 51 | flkL | +0.0027 | 1.4% |
| 197 | ss2 | +0.0017 | 0.9% |

**Query mass** (top-1=91%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.1749 | 91.3% |
| 237 | flkR | +0.0037 | 1.9% |
| 103 | ss1 | +0.0029 | 1.5% |
| 201 | ss2 | +0.0017 | 0.9% |
| 248 | flkR | +0.0016 | 0.8% |

**Offset distribution [frequency]** (top-2 coverage: 46%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 4 | 30.8% |
| +6 | 2 | 15.4% |
| +11 | 2 | 15.4% |
| -6 | 1 | 7.7% |
| +0 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 23.1% |
| flkR | flkR | 3 | 23.1% |
| flkL | other | 2 | 15.4% |
| flkL | flkL | 2 | 15.4% |
| ss1 | flkL | 2 | 15.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 97 | ss1 | +0.1699 | 0.0337 |
| 237 | flkR | 243 | flkR | +0.0037 | 0.0204 |
| 103 | ss1 | 97 | ss1 | +0.0029 | 0.0253 |
| 101 | ss1 | 101 | ss1 | +0.0028 | 0.0008 |
| 201 | ss2 | 197 | ss2 | +0.0017 | 0.0052 |

### L6 H0 — Rank #17

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 17  |  total attr: +0.0585

**Key mass** (top-1=45%, top-2=56%, top-3=63%)  [DISTR(Y32/W44/L42/D30/E55)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0262 | 44.8% |
| 44 | flkL | +0.0066 | 11.2% |
| 42 | flkL | +0.0038 | 6.5% |
| 30 | other | +0.0023 | 3.9% |
| 55 | flkL | +0.0021 | 3.7% |

**Query mass** (top-1=96%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0561 | 96.1% |
| 90 | flkL | +0.0012 | 2.0% |
| 88 | flkL | +0.0011 | 2.0% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +58 | 2 | 11.8% |
| +69 | 1 | 5.9% |
| +57 | 1 | 5.9% |
| +59 | 1 | 5.9% |
| +46 | 1 | 5.9% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=82%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 14 | 82.4% |
| flkL | other | 2 | 11.8% |
| ss1 | flkR | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 32 | flkL | +0.0262 | 0.0239 |
| 101 | ss1 | 44 | flkL | +0.0066 | 0.0156 |
| 101 | ss1 | 42 | flkL | +0.0038 | 0.0061 |
| 101 | ss1 | 55 | flkL | +0.0021 | 0.0013 |
| 101 | ss1 | 48 | flkL | +0.0021 | 0.0017 |

### L6 H17 — Rank #21

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 82  |  total attr: +0.2880

**Key mass** (top-1=11%, top-2=20%, top-3=25%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 90 | flkL | +0.0313 | 10.9% |
| 45 | flkL | +0.0259 | 9.0% |
| 80 | flkL | +0.0142 | 4.9% |
| 266 | flkR | +0.0141 | 4.9% |
| 35 | flkL | +0.0129 | 4.5% |

**Query mass** (top-1=22%, top-2=34%, top-3=41%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0633 | 22.0% |
| 45 | flkL | +0.0344 | 12.0% |
| 31 | other | +0.0215 | 7.5% |
| 35 | flkL | +0.0162 | 5.6% |
| 47 | flkL | +0.0152 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 34%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 23 | 28.0% |
| -12 | 5 | 6.1% |
| +21 | 3 | 3.7% |
| -22 | 3 | 3.7% |
| -11 | 3 | 3.7% |

**Region-pair profile** (q→k)  (top=34%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 28 | 34.1% |
| flkR | flkR | 20 | 24.4% |
| other | flkL | 8 | 9.8% |
| ss1 | flkL | 7 | 8.5% |
| ss1 | ss1 | 4 | 4.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 90 | flkL | +0.0313 | 0.0187 |
| 45 | flkL | 45 | flkL | +0.0182 | 0.0959 |
| 101 | ss1 | 80 | flkL | +0.0142 | 0.0085 |
| 266 | flkR | 266 | flkR | +0.0132 | 0.0673 |
| 35 | flkL | 35 | flkL | +0.0129 | 0.0982 |

### L7 H7 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.1041

**Key mass** (top-1=96%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0996 | 95.7% |
| 239 | flkR | +0.0035 | 3.4% |
| 32 | flkL | +0.0010 | 1.0% |

**Query mass** (top-1=11%, top-2=20%, top-3=28%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 137 | other | +0.0116 | 11.2% |
| 138 | other | +0.0092 | 8.8% |
| 136 | other | +0.0088 | 8.4% |
| 133 | other | +0.0059 | 5.7% |
| 131 | other | +0.0058 | 5.6% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +32 | 2 | 7.1% |
| +33 | 2 | 7.1% |
| +36 | 1 | 3.6% |
| +37 | 1 | 3.6% |
| +35 | 1 | 3.6% |

**Region-pair profile** (q→k)  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 20 | 71.4% |
| flkL | ss1 | 2 | 7.1% |
| ss1 | ss1 | 2 | 7.1% |
| ss2 | ss1 | 1 | 3.6% |
| flkR | flkR | 1 | 3.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 137 | other | 101 | ss1 | +0.0116 | 0.0323 |
| 138 | other | 101 | ss1 | +0.0092 | 0.0289 |
| 136 | other | 101 | ss1 | +0.0088 | 0.0315 |
| 133 | other | 101 | ss1 | +0.0059 | 0.0250 |
| 131 | other | 101 | ss1 | +0.0058 | 0.0289 |

### L7 H13 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 96  |  total attr: +0.5070

**Key mass** (top-1=16%, top-2=31%, top-3=40%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 270 | flkR | +0.0828 | 16.3% |
| 217 | flkR | +0.0743 | 14.6% |
| 33 | flkL | +0.0466 | 9.2% |
| 36 | flkL | +0.0436 | 8.6% |
| 269 | flkR | +0.0168 | 3.3% |

**Query mass** (top-1=15%, top-2=30%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | flkR | +0.0774 | 15.3% |
| 270 | flkR | +0.0743 | 14.6% |
| 262 | flkR | +0.0478 | 9.4% |
| 33 | flkL | +0.0449 | 8.9% |
| 69 | flkL | +0.0194 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 17 | 17.7% |
| -53 | 5 | 5.2% |
| -40 | 3 | 3.1% |
| -56 | 3 | 3.1% |
| +226 | 2 | 2.1% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 37 | 38.5% |
| flkR | flkR | 20 | 20.8% |
| flkR | flkL | 10 | 10.4% |
| flkL | flkR | 5 | 5.2% |
| ss1 | flkL | 4 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 217 | flkR | 270 | flkR | +0.0774 | 0.2595 |
| 270 | flkR | 217 | flkR | +0.0743 | 0.3849 |
| 262 | flkR | 36 | flkL | +0.0394 | 0.5150 |
| 33 | flkL | 33 | flkL | +0.0253 | 0.5183 |
| 33 | flkL | 74 | flkL | +0.0143 | 0.2244 |

### L8 H2 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.1448

**Key mass** (top-1=97%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.1399 | 96.6% |
| 218 | flkR | +0.0023 | 1.6% |
| 269 | flkR | +0.0013 | 0.9% |
| 271 | flkR | +0.0013 | 0.9% |

**Query mass** (top-1=12%, top-2=24%, top-3=35%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | other | +0.0176 | 12.1% |
| 137 | other | +0.0175 | 12.1% |
| 139 | other | +0.0149 | 10.3% |
| 136 | other | +0.0133 | 9.2% |
| 140 | other | +0.0107 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 9.1% |
| +37 | 1 | 4.5% |
| +36 | 1 | 4.5% |
| +38 | 1 | 4.5% |
| +35 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 19 | 86.4% |
| flkR | flkR | 3 | 13.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 138 | other | 101 | ss1 | +0.0176 | 0.0283 |
| 137 | other | 101 | ss1 | +0.0175 | 0.0235 |
| 139 | other | 101 | ss1 | +0.0149 | 0.0387 |
| 136 | other | 101 | ss1 | +0.0133 | 0.0257 |
| 140 | other | 101 | ss1 | +0.0107 | 0.0507 |

### L9 H15 — Rank #29

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 20  |  total attr: +0.0495

**Key mass** (top-1=11%, top-2=20%, top-3=29%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 133 | other | +0.0053 | 10.6% |
| 132 | other | +0.0048 | 9.7% |
| 131 | other | +0.0042 | 8.4% |
| 134 | other | +0.0034 | 6.9% |
| 138 | other | +0.0031 | 6.4% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0495 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -32 | 1 | 5.0% |
| -31 | 1 | 5.0% |
| -30 | 1 | 5.0% |
| -33 | 1 | 5.0% |
| -37 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=95%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 19 | 95.0% |
| ss1 | ss1 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 133 | other | +0.0053 | 0.0066 |
| 101 | ss1 | 132 | other | +0.0048 | 0.0063 |
| 101 | ss1 | 131 | other | +0.0042 | 0.0058 |
| 101 | ss1 | 134 | other | +0.0034 | 0.0046 |
| 101 | ss1 | 138 | other | +0.0031 | 0.0045 |

### L9 H17 — Rank #2

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 33  |  total attr: +0.2860

**Key mass** (top-1=7%, top-2=14%, top-3=21%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | other | +0.0209 | 7.3% |
| 137 | other | +0.0204 | 7.1% |
| 140 | other | +0.0191 | 6.7% |
| 135 | other | +0.0190 | 6.6% |
| 139 | other | +0.0186 | 6.5% |

**Query mass** (top-1=76%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.2160 | 75.5% |
| 101 | ss1 | +0.0700 | 24.5% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +63 | 1 | 3.0% |
| +64 | 1 | 3.0% |
| +62 | 1 | 3.0% |
| +61 | 1 | 3.0% |
| +65 | 1 | 3.0% |

**Region-pair profile** (q→k)  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 22 | 66.7% |
| ss1 | other | 11 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 138 | other | +0.0209 | 0.0129 |
| 201 | ss2 | 137 | other | +0.0204 | 0.0122 |
| 201 | ss2 | 139 | other | +0.0186 | 0.0122 |
| 201 | ss2 | 140 | other | +0.0165 | 0.0117 |
| 201 | ss2 | 136 | other | +0.0160 | 0.0095 |

### L10 H9 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 103  |  total attr: +0.3459

**Key mass** (top-1=98%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.3388 | 98.0% |
| 226 | flkR | +0.0046 | 1.3% |
| 32 | flkL | +0.0014 | 0.4% |
| 239 | flkR | +0.0011 | 0.3% |

**Query mass** (top-1=20%, top-2=29%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0679 | 19.6% |
| 101 | ss1 | +0.0313 | 9.0% |
| 203 | ss2 | +0.0167 | 4.8% |
| 71 | flkL | +0.0101 | 2.9% |
| 198 | ss2 | +0.0098 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 2%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 1 | 1.0% |
| +0 | 1 | 1.0% |
| +102 | 1 | 1.0% |
| -30 | 1 | 1.0% |
| +97 | 1 | 1.0% |

**Region-pair profile** (q→k)  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 42 | 40.8% |
| flkR | ss1 | 30 | 29.1% |
| flkL | ss1 | 14 | 13.6% |
| ss2 | ss1 | 7 | 6.8% |
| ss1 | ss1 | 5 | 4.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0679 | 0.1241 |
| 101 | ss1 | 101 | ss1 | +0.0288 | 0.0372 |
| 203 | ss2 | 101 | ss1 | +0.0154 | 0.1334 |
| 71 | flkL | 101 | ss1 | +0.0101 | 0.0983 |
| 198 | ss2 | 101 | ss1 | +0.0078 | 0.1051 |

### L11 H14 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 34  |  total attr: +0.1173

**Key mass** (top-1=91%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.1071 | 91.3% |
| 228 | flkR | +0.0042 | 3.6% |
| 71 | flkL | +0.0025 | 2.2% |
| 255 | flkR | +0.0023 | 1.9% |
| 248 | flkR | +0.0012 | 1.0% |

**Query mass** (top-1=23%, top-2=31%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0265 | 22.6% |
| 203 | ss2 | +0.0093 | 7.9% |
| 198 | ss2 | +0.0075 | 6.4% |
| 149 | other | +0.0053 | 4.5% |
| 148 | other | +0.0051 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 1 | 2.9% |
| +97 | 1 | 2.9% |
| +102 | 1 | 2.9% |
| +48 | 1 | 2.9% |
| +47 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=59%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 20 | 58.8% |
| ss2 | ss1 | 5 | 14.7% |
| ss2 | flkR | 4 | 11.8% |
| ss1 | ss1 | 2 | 5.9% |
| flkR | ss1 | 1 | 2.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0214 | 0.0440 |
| 198 | ss2 | 101 | ss1 | +0.0075 | 0.0735 |
| 203 | ss2 | 101 | ss1 | +0.0067 | 0.0211 |
| 149 | other | 101 | ss1 | +0.0053 | 0.1037 |
| 148 | other | 101 | ss1 | +0.0051 | 0.1018 |

### L11 H16 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.0423

**Key mass** (top-1=77%, top-2=83%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0326 | 77.1% |
| 32 | flkL | +0.0024 | 5.7% |
| 418 | other | +0.0023 | 5.4% |
| 36 | flkL | +0.0014 | 3.4% |
| 417 | other | +0.0014 | 3.3% |

**Query mass** (top-1=16%, top-2=28%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0066 | 15.7% |
| 203 | ss2 | +0.0051 | 12.0% |
| 205 | ss2 | +0.0028 | 6.7% |
| 201 | ss2 | +0.0028 | 6.7% |
| 228 | flkR | +0.0025 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 1 | 3.7% |
| +104 | 1 | 3.7% |
| +127 | 1 | 3.7% |
| +69 | 1 | 3.7% |
| +0 | 1 | 3.7% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 10 | 37.0% |
| flkR | ss1 | 4 | 14.8% |
| flkL | ss1 | 3 | 11.1% |
| ss2 | ss1 | 2 | 7.4% |
| ss1 | flkL | 2 | 7.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 101 | ss1 | +0.0038 | 0.0316 |
| 205 | ss2 | 101 | ss1 | +0.0028 | 0.0825 |
| 228 | flkR | 101 | ss1 | +0.0025 | 0.0551 |
| 101 | ss1 | 32 | flkL | +0.0024 | 0.0154 |
| 101 | ss1 | 101 | ss1 | +0.0021 | 0.0047 |

### L12 H10 — Rank #16

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 42  |  total attr: +0.0921

**Key mass** (top-1=10%, top-2=17%, top-3=22%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 189 | other | +0.0096 | 10.4% |
| 190 | other | +0.0059 | 6.4% |
| 149 | other | +0.0048 | 5.2% |
| 150 | other | +0.0047 | 5.1% |
| 192 | other | +0.0044 | 4.8% |

**Query mass** (top-1=96%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0886 | 96.2% |
| 199 | ss2 | +0.0014 | 1.5% |
| 203 | ss2 | +0.0011 | 1.2% |
| 116 | other | +0.0010 | 1.0% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +11 | 2 | 4.8% |
| +10 | 2 | 4.8% |
| +15 | 2 | 4.8% |
| +12 | 1 | 2.4% |
| +52 | 1 | 2.4% |

**Region-pair profile** (q→k)  (top=95%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 40 | 95.2% |
| ss2 | flkL | 1 | 2.4% |
| other | ss1 | 1 | 2.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 189 | other | +0.0082 | 0.0702 |
| 201 | ss2 | 190 | other | +0.0059 | 0.0350 |
| 201 | ss2 | 149 | other | +0.0048 | 0.0097 |
| 201 | ss2 | 150 | other | +0.0047 | 0.0099 |
| 201 | ss2 | 151 | other | +0.0036 | 0.0076 |

### L12 H15 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkL→ss1  |  cells: 20  |  total attr: +0.0363

**Key mass** (top-1=86%, top-2=92%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0311 | 85.6% |
| 213 | flkR | +0.0022 | 6.1% |
| 217 | flkR | +0.0019 | 5.2% |
| 216 | flkR | +0.0011 | 3.1% |

**Query mass** (top-1=20%, top-2=31%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 75 | flkL | +0.0072 | 19.8% |
| 201 | ss2 | +0.0042 | 11.6% |
| 49 | flkL | +0.0038 | 10.5% |
| -1 | other | +0.0021 | 5.8% |
| 30 | other | +0.0021 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -12 | 2 | 10.0% |
| -26 | 1 | 5.0% |
| -52 | 1 | 5.0% |
| -102 | 1 | 5.0% |
| -71 | 1 | 5.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=65%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 13 | 65.0% |
| ss2 | flkR | 4 | 20.0% |
| other | ss1 | 2 | 10.0% |
| ss1 | ss1 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 75 | flkL | 101 | ss1 | +0.0072 | 0.1415 |
| 49 | flkL | 101 | ss1 | +0.0038 | 0.1303 |
| -1 | other | 101 | ss1 | +0.0021 | 0.0381 |
| 30 | other | 101 | ss1 | +0.0021 | 0.2497 |
| 37 | flkL | 101 | ss1 | +0.0020 | 0.1429 |

### L13 H2 — Rank #27

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 8  |  total attr: +0.0231

**Key mass** (top-1=49%, top-2=81%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0113 | 49.0% |
| 201 | ss2 | +0.0074 | 32.1% |
| 205 | ss2 | +0.0020 | 8.5% |
| 195 | other | +0.0015 | 6.3% |
| 106 | ss1 | +0.0009 | 4.0% |

**Query mass** (top-1=76%, top-2=85%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0176 | 76.4% |
| 199 | ss2 | +0.0020 | 8.7% |
| 198 | ss2 | +0.0014 | 6.2% |
| 197 | ss2 | +0.0011 | 4.7% |
| 101 | ss1 | +0.0009 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 2 | 25.0% |
| -4 | 2 | 25.0% |
| +0 | 1 | 12.5% |
| +6 | 1 | 12.5% |
| -3 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 75.0% |
| ss2 | other | 1 | 12.5% |
| ss1 | ss1 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 203 | ss2 | +0.0113 | 0.0369 |
| 201 | ss2 | 201 | ss2 | +0.0029 | 0.0372 |
| 199 | ss2 | 201 | ss2 | +0.0020 | 0.0779 |
| 201 | ss2 | 205 | ss2 | +0.0020 | 0.0115 |
| 201 | ss2 | 195 | other | +0.0015 | 0.0095 |

### L13 H18 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 19  |  total attr: +0.0798

**Key mass** (top-1=82%, top-2=94%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0650 | 81.5% |
| 71 | flkL | +0.0102 | 12.8% |
| 216 | flkR | +0.0024 | 3.0% |
| 198 | ss2 | +0.0011 | 1.4% |
| 207 | ss2 | +0.0010 | 1.3% |

**Query mass** (top-1=31%, top-2=42%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0249 | 31.3% |
| 101 | ss1 | +0.0089 | 11.2% |
| 203 | ss2 | +0.0086 | 10.8% |
| 200 | ss2 | +0.0068 | 8.6% |
| 204 | ss2 | +0.0054 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 1 | 5.3% |
| +30 | 1 | 5.3% |
| +102 | 1 | 5.3% |
| +99 | 1 | 5.3% |
| +103 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 36.8% |
| other | ss1 | 3 | 15.8% |
| ss1 | ss1 | 2 | 10.5% |
| ss2 | ss2 | 2 | 10.5% |
| ss1 | flkL | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0212 | 0.1989 |
| 101 | ss1 | 71 | flkL | +0.0089 | 0.1053 |
| 203 | ss2 | 101 | ss1 | +0.0086 | 0.1922 |
| 200 | ss2 | 101 | ss1 | +0.0068 | 0.1566 |
| 204 | ss2 | 101 | ss1 | +0.0054 | 0.1476 |

### L14 H4 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→flkL  |  cells: 11  |  total attr: +0.1554

**Key mass** (top-1=94%, top-2=96%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.1467 | 94.4% |
| 71 | flkL | +0.0023 | 1.5% |
| 99 | ss1 | +0.0020 | 1.3% |
| 69 | flkL | +0.0013 | 0.8% |
| 77 | flkL | +0.0011 | 0.7% |

**Query mass** (top-1=80%, top-2=95%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.1242 | 79.9% |
| 203 | ss2 | +0.0241 | 15.5% |
| 206 | ss2 | +0.0033 | 2.1% |
| 248 | flkR | +0.0019 | 1.2% |
| 254 | flkR | +0.0019 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 2 | 18.2% |
| +100 | 1 | 9.1% |
| +105 | 1 | 9.1% |
| +130 | 1 | 9.1% |
| +147 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→flkL]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 5 | 45.5% |
| ss2 | ss1 | 4 | 36.4% |
| flkR | ss1 | 2 | 18.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.1155 | 0.1478 |
| 203 | ss2 | 101 | ss1 | +0.0241 | 0.1095 |
| 206 | ss2 | 101 | ss1 | +0.0033 | 0.1027 |
| 201 | ss2 | 71 | flkL | +0.0023 | 0.0066 |
| 201 | ss2 | 99 | ss1 | +0.0020 | 0.0081 |

### L14 H9 — Rank #20

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.0661

**Key mass** (top-1=59%, top-2=71%, top-3=82%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0390 | 59.1% |
| 198 | ss2 | +0.0078 | 11.8% |
| 71 | flkL | +0.0073 | 11.1% |
| 90 | flkL | +0.0028 | 4.3% |
| 237 | flkR | +0.0024 | 3.6% |

**Query mass** (top-1=70%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0465 | 70.4% |
| 203 | ss2 | +0.0126 | 19.0% |
| 198 | ss2 | +0.0022 | 3.3% |
| 71 | flkL | +0.0018 | 2.8% |
| 200 | ss2 | +0.0011 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 12.5% |
| +100 | 1 | 6.2% |
| +102 | 1 | 6.2% |
| +130 | 1 | 6.2% |
| +5 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 4 | 25.0% |
| ss2 | flkR | 4 | 25.0% |
| ss2 | flkL | 3 | 18.8% |
| ss2 | ss1 | 2 | 12.5% |
| flkL | ss1 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0309 | 0.0487 |
| 203 | ss2 | 101 | ss1 | +0.0054 | 0.0247 |
| 201 | ss2 | 71 | flkL | +0.0048 | 0.0178 |
| 203 | ss2 | 198 | ss2 | +0.0046 | 0.0508 |
| 201 | ss2 | 90 | flkL | +0.0028 | 0.0054 |

### L15 H8 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 3  |  total attr: +0.1144

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.1129 | 98.7% |
| 103 | ss1 | +0.0015 | 1.3% |

**Query mass** (top-1=77%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0879 | 76.8% |
| 203 | ss2 | +0.0265 | 23.2% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 2 | 66.7% |
| +102 | 1 | 33.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0879 | 0.1999 |
| 203 | ss2 | 101 | ss1 | +0.0250 | 0.1332 |
| 203 | ss2 | 103 | ss1 | +0.0015 | 0.0150 |

### L17 H10 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 18  |  total attr: +0.1502

**Key mass** (top-1=93%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.1393 | 92.8% |
| 203 | ss2 | +0.0049 | 3.2% |
| 101 | ss1 | +0.0040 | 2.7% |
| 204 | ss2 | +0.0010 | 0.6% |
| 92 | flkL | +0.0010 | 0.6% |

**Query mass** (top-1=43%, top-2=54%, top-3=64%)  [DISTR(F203/K200/T202/P205)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0648 | 43.2% |
| 200 | ss2 | +0.0160 | 10.7% |
| 202 | ss2 | +0.0159 | 10.6% |
| 205 | ss2 | +0.0128 | 8.5% |
| 199 | ss2 | +0.0120 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 3 | 16.7% |
| +2 | 2 | 11.1% |
| +1 | 2 | 11.1% |
| -2 | 2 | 11.1% |
| +0 | 2 | 11.1% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=72%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 13 | 72.2% |
| ss1 | ss1 | 2 | 11.1% |
| other | ss1 | 1 | 5.6% |
| flkR | ss2 | 1 | 5.6% |
| flkL | flkL | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 201 | ss2 | +0.0638 | 0.4473 |
| 200 | ss2 | 201 | ss2 | +0.0160 | 0.4830 |
| 202 | ss2 | 201 | ss2 | +0.0138 | 0.4418 |
| 199 | ss2 | 201 | ss2 | +0.0120 | 0.3884 |
| 205 | ss2 | 201 | ss2 | +0.0111 | 0.4064 |

### L17 H18 — Rank #24

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 10  |  total attr: +0.0451

**Key mass** (top-1=47%, top-2=69%, top-3=75%)  [DISTR(V101/F203/I230)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0211 | 46.9% |
| 203 | ss2 | +0.0099 | 22.0% |
| 230 | flkR | +0.0029 | 6.3% |
| 92 | flkL | +0.0025 | 5.5% |
| 90 | flkL | +0.0022 | 4.9% |

**Query mass** (top-1=54%, top-2=91%, top-3=97%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0246 | 54.4% |
| 203 | ss2 | +0.0164 | 36.4% |
| 199 | ss2 | +0.0029 | 6.3% |
| 200 | ss2 | +0.0012 | 2.8% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -31 | 3 | 30.0% |
| +102 | 2 | 20.0% |
| +100 | 1 | 10.0% |
| +0 | 1 | 10.0% |
| +109 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 30.0% |
| ss2 | flkR | 3 | 30.0% |
| ss2 | ss2 | 2 | 20.0% |
| ss2 | flkL | 2 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0187 | 0.1745 |
| 203 | ss2 | 203 | ss2 | +0.0099 | 0.0492 |
| 199 | ss2 | 230 | flkR | +0.0029 | 0.0978 |
| 201 | ss2 | 92 | flkL | +0.0025 | 0.0223 |
| 203 | ss2 | 101 | ss1 | +0.0024 | 0.0230 |

### L26 H16 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 13  |  total attr: +0.0396

**Key mass** (top-1=30%, top-2=59%, top-3=68%)  [DISTR(H97/P205/N91/T98)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0119 | 30.0% |
| 205 | ss2 | +0.0113 | 28.5% |
| 91 | flkL | +0.0039 | 9.8% |
| 98 | ss1 | +0.0025 | 6.2% |
| 103 | ss1 | +0.0022 | 5.6% |

**Query mass** (top-1=29%, top-2=52%, top-3=62%)  [DISTR(H97/P205/K102/T202)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0113 | 28.5% |
| 205 | ss2 | +0.0092 | 23.2% |
| 102 | ss1 | +0.0039 | 9.8% |
| 202 | ss2 | +0.0035 | 8.9% |
| 206 | ss2 | +0.0027 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +104 | 2 | 15.4% |
| -108 | 1 | 7.7% |
| +108 | 1 | 7.7% |
| +11 | 1 | 7.7% |
| +109 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=69%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 69.2% |
| ss1 | ss2 | 2 | 15.4% |
| ss1 | flkL | 1 | 7.7% |
| ss2 | flkR | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 97 | ss1 | 205 | ss2 | +0.0113 | 0.4351 |
| 205 | ss2 | 97 | ss1 | +0.0092 | 0.3503 |
| 102 | ss1 | 91 | flkL | +0.0039 | 0.1848 |
| 206 | ss2 | 97 | ss1 | +0.0027 | 0.1092 |
| 199 | ss2 | 103 | ss1 | +0.0022 | 0.0383 |

### L27 H15 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 18  |  total attr: +0.1023

**Key mass** (top-1=29%, top-2=50%, top-3=70%)  [DISTR(K102/H97/I99/T98)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0294 | 28.7% |
| 97 | ss1 | +0.0215 | 21.0% |
| 99 | ss1 | +0.0205 | 20.1% |
| 98 | ss1 | +0.0072 | 7.1% |
| 203 | ss2 | +0.0058 | 5.7% |

**Query mass** (top-1=32%, top-2=61%, top-3=71%)  [DISTR(F203/K200/P205)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0331 | 32.4% |
| 200 | ss2 | +0.0288 | 28.2% |
| 205 | ss2 | +0.0111 | 10.8% |
| 99 | ss1 | +0.0091 | 8.9% |
| 202 | ss2 | +0.0083 | 8.1% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +104 | 2 | 11.1% |
| +106 | 2 | 11.1% |
| -104 | 2 | 11.1% |
| +98 | 1 | 5.6% |
| +108 | 1 | 5.6% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 10 | 55.6% |
| ss1 | ss2 | 4 | 22.2% |
| ss1 | flkL | 2 | 11.1% |
| ss2 | flkL | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | ss2 | 102 | ss1 | +0.0264 | 0.2309 |
| 203 | ss2 | 99 | ss1 | +0.0205 | 0.1307 |
| 203 | ss2 | 97 | ss1 | +0.0114 | 0.2368 |
| 205 | ss2 | 97 | ss1 | +0.0101 | 0.2159 |
| 99 | ss1 | 203 | ss2 | +0.0058 | 0.0413 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 26  |  total attr: +0.0943

**Key mass** (top-1=33%, top-2=49%, top-3=62%)  [DISTR(K200/E100/T98/K102)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0312 | 33.0% |
| 100 | ss1 | +0.0148 | 15.7% |
| 98 | ss1 | +0.0126 | 13.4% |
| 102 | ss1 | +0.0100 | 10.6% |
| 89 | flkL | +0.0045 | 4.8% |

**Query mass** (top-1=33%, top-2=50%, top-3=61%)  [DISTR(K102/T202/K200/K204/F203)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0311 | 33.0% |
| 202 | ss2 | +0.0165 | 17.5% |
| 200 | ss2 | +0.0097 | 10.3% |
| 204 | ss2 | +0.0082 | 8.7% |
| 203 | ss2 | +0.0065 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 2 | 7.7% |
| +104 | 2 | 7.7% |
| +105 | 2 | 7.7% |
| -98 | 1 | 3.8% |
| +102 | 1 | 3.8% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 42.3% |
| ss1 | ss2 | 7 | 26.9% |
| ss2 | flkL | 3 | 11.5% |
| ss2 | other | 2 | 7.7% |
| ss1 | ss1 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 102 | ss1 | 200 | ss2 | +0.0302 | 0.4401 |
| 202 | ss2 | 100 | ss1 | +0.0089 | 0.1695 |
| 204 | ss2 | 98 | ss1 | +0.0082 | 0.2993 |
| 200 | ss2 | 100 | ss1 | +0.0049 | 0.2062 |
| 200 | ss2 | 102 | ss1 | +0.0048 | 0.1369 |

### L32 H13 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 16  |  total attr: +0.0739

**Key mass** (top-1=24%, top-2=40%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 98 | ss1 | +0.0174 | 23.5% |
| 102 | ss1 | +0.0118 | 16.0% |
| 100 | ss1 | +0.0080 | 10.8% |
| 203 | ss2 | +0.0064 | 8.6% |
| 202 | ss2 | +0.0062 | 8.4% |

**Query mass** (top-1=20%, top-2=31%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0149 | 20.1% |
| 200 | ss2 | +0.0082 | 11.1% |
| 198 | ss2 | +0.0082 | 11.1% |
| 102 | ss1 | +0.0073 | 9.9% |
| 98 | ss1 | +0.0064 | 8.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +104 | 2 | 12.5% |
| -104 | 2 | 12.5% |
| +96 | 1 | 6.2% |
| +106 | 1 | 6.2% |
| -96 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 50.0% |
| ss1 | ss2 | 8 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 202 | ss2 | 98 | ss1 | +0.0115 | 0.1368 |
| 198 | ss2 | 102 | ss1 | +0.0082 | 0.1028 |
| 99 | ss1 | 203 | ss2 | +0.0064 | 0.0401 |
| 204 | ss2 | 98 | ss1 | +0.0059 | 0.1956 |
| 203 | ss2 | 99 | ss1 | +0.0057 | 0.0357 |

### L32 H18 — Rank #9

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0557

**Key mass** (top-1=34%, top-2=59%, top-3=76%)  [DISTR(F203/I99/T98)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0189 | 33.9% |
| 99 | ss1 | +0.0141 | 25.3% |
| 98 | ss1 | +0.0092 | 16.5% |
| 102 | ss1 | +0.0042 | 7.6% |
| 205 | ss2 | +0.0032 | 5.7% |

**Query mass** (top-1=34%, top-2=59%, top-3=75%)  [DISTR(I99/F203/T202)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 99 | ss1 | +0.0189 | 33.9% |
| 203 | ss2 | +0.0141 | 25.3% |
| 202 | ss2 | +0.0090 | 16.2% |
| 200 | ss2 | +0.0038 | 6.8% |
| 97 | ss1 | +0.0032 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +104 | 2 | 18.2% |
| -104 | 1 | 9.1% |
| -108 | 1 | 9.1% |
| +98 | 1 | 9.1% |
| -96 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 63.6% |
| ss1 | ss2 | 4 | 36.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 99 | ss1 | 203 | ss2 | +0.0189 | 0.0727 |
| 203 | ss2 | 99 | ss1 | +0.0141 | 0.0543 |
| 202 | ss2 | 98 | ss1 | +0.0071 | 0.0517 |
| 97 | ss1 | 205 | ss2 | +0.0032 | 0.0279 |
| 200 | ss2 | 102 | ss1 | +0.0027 | 0.0111 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #10 | L0 | H9 | 45 | +0.2003 | SINGLE-ANCHOR | Y32 | DISTRIBUTED |  |  | INTRA:flkL |
| #19 | L0 | H12 | 32 | +0.0634 | DUAL-ANCHOR | Y32/G271 | DISTRIBUTED |  |  | INTRA:flkL |
| #23 | L1 | H1 | 28 | +0.0976 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL |  |
| #25 | L4 | H5 | 9 | +0.0627 | SINGLE-ANCHOR | I92 | SINGLE-ANCHOR | H97 |  | ss1→flkL |
| #26 | L4 | H14 | 11 | +0.0242 | DISTRIBUTED | N270/K264/G271 | SINGLE-ANCHOR | V101 |  |  |
| #7 | L5 | H9 | 13 | +0.1915 | SINGLE-ANCHOR | H97 | SINGLE-ANCHOR | V101 |  |  |
| #17 | L6 | H0 | 17 | +0.0585 | DISTRIBUTED | Y32/W44/L42/D30/E55 | SINGLE-ANCHOR | V101 |  | ss1→flkL |
| #21 | L6 | H17 | 82 | +0.2880 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #18 | L7 | H7 | 28 | +0.1041 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #5 | L7 | H13 | 96 | +0.5070 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #12 | L8 | H2 | 22 | +0.1448 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #29 | L9 | H15 | 20 | +0.0495 | DISTRIBUTED |  | SINGLE-ANCHOR | V101 |  |  |
| #2 | L9 | H17 | 33 | +0.2860 | DISTRIBUTED |  | SINGLE-ANCHOR | V201 |  |  |
| #1 | L10 | H9 | 103 | +0.3459 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #28 | L11 | H14 | 34 | +0.1173 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #11 | L11 | H16 | 27 | +0.0423 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #16 | L12 | H10 | 42 | +0.0921 | DISTRIBUTED |  | SINGLE-ANCHOR | V201 |  |  |
| #30 | L12 | H15 | 20 | +0.0363 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  | flkL→ss1 |
| #27 | L13 | H2 | 8 | +0.0231 | DUAL-ANCHOR | F203/V201 | SINGLE-ANCHOR | V201 |  | INTRA:ss2 |
| #22 | L13 | H18 | 19 | +0.0798 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #14 | L14 | H4 | 11 | +0.1554 | SINGLE-ANCHOR | V101 | SINGLE-ANCHOR | V201 |  | CROSS:ss2→flkL |
| #20 | L14 | H9 | 16 | +0.0661 | DUAL-ANCHOR | V101/Y198 | SINGLE-ANCHOR | V201 |  |  |
| #13 | L15 | H8 | 3 | +0.1144 | SINGLE-ANCHOR | V101 | SINGLE-ANCHOR | V201 | CROSS_SSE | CROSS:ss2→ss1 |
| #8 | L17 | H10 | 18 | +0.1502 | SINGLE-ANCHOR | V201 | DISTRIBUTED | F203/K200/T202/P205 |  | INTRA:ss2 |
| #24 | L17 | H18 | 10 | +0.0451 | DISTRIBUTED | V101/F203/I230 | DUAL-ANCHOR | V201/F203 |  |  |
| #15 | L26 | H16 | 13 | +0.0396 | DISTRIBUTED | H97/P205/N91/T98 | DISTRIBUTED | H97/P205/K102/T202 |  | CROSS:ss2→ss1 |
| #3 | L27 | H15 | 18 | +0.1023 | DISTRIBUTED | K102/H97/I99/T98 | DISTRIBUTED | F203/K200/P205 |  | CROSS:ss2→ss1 |
| #6 | L29 | H18 | 26 | +0.0943 | DISTRIBUTED | K200/E100/T98/K102 | DISTRIBUTED | K102/T202/K200/K204/F203 |  | CROSS:ss2→ss1 |
| #4 | L32 | H13 | 16 | +0.0739 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #9 | L32 | H18 | 11 | +0.0557 | DISTRIBUTED | F203/I99/T98 | DISTRIBUTED | I99/F203/T202 |  | CROSS:ss2→ss1 |
