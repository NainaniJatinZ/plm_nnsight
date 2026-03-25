# Contact Pattern Analysis: 4EX6A

Generated: 2026-03-22 22:01:26   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 4EX6A |
| Contact pair | (22, 123) |
| ss1 | [17, 28) |
| ss2 | [118, 129) |
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
| Clean metric | 0.8468 |
| Corrupt metric | 0.0242 |
| Gap | 0.8226 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 80.45% |
| positive IE | 70 | 70.48% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L8 | H12 | +0.2290 |
| 2 | L32 | H18 | +0.1561 |
| 3 | L27 | H15 | +0.1467 |
| 4 | L26 | H16 | +0.1147 |
| 5 | L12 | H16 | +0.1049 |
| 6 | L22 | H14 | +0.0950 |
| 7 | L32 | H13 | +0.0857 |
| 8 | L16 | H9 | +0.0819 |
| 9 | L10 | H9 | +0.0782 |
| 10 | L29 | H18 | +0.0772 |
| 11 | L13 | H2 | +0.0630 |
| 12 | L12 | H2 | +0.0574 |
| 13 | L11 | H17 | +0.0550 |
| 14 | L30 | H1 | +0.0439 |
| 15 | L11 | H18 | +0.0428 |
| 16 | L11 | H14 | +0.0391 |
| 17 | L10 | H16 | +0.0389 |
| 18 | L24 | H18 | +0.0375 |
| 19 | L21 | H2 | +0.0329 |
| 20 | L12 | H14 | +0.0317 |
| 21 | L10 | H6 | +0.0304 |
| 22 | L23 | H16 | +0.0291 |
| 23 | L18 | H8 | +0.0288 |
| 24 | L9 | H16 | +0.0278 |
| 25 | L8 | H0 | +0.0271 |
| 26 | L13 | H1 | +0.0261 |
| 27 | L7 | H13 | +0.0254 |
| 28 | L23 | H15 | +0.0245 |
| 29 | L13 | H8 | +0.0234 |
| 30 | L26 | H6 | +0.0227 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.08% |
| 3 | 0.22% |
| 4 | 0.27% |
| 5 | 0.32% |
| 6 | 0.56% |
| 7 | 0.62% |
| 8 | 0.72% |
| 9 | 0.94% |
| 10 | 0.99% |
| 20 | 4.57% |
| 80 | 89.43% |
| 450 | 133.73% |

## Cell Attribution Analysis

Total cells: 3,898,345

- Positive: 1,982,078
- Negative: 1,914,364

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000072 | 389,835 |
| 95th | +0.00000225 | 194,918 |
| 99th | +0.00001839 | 38,984 |
| 99.5th | +0.00003970 | 19,492 |
| 99.9th | +0.00021884 | 3,899 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L8 | H12 | 124 | ss2 | 180 | other | +0.155010 | 0.228267 |
| L12 | H16 | 22 | ss1 | 180 | other | +0.121879 | 0.372907 |
| L8 | H12 | 124 | ss2 | 181 | other | +0.085366 | 0.134527 |
| L32 | H18 | 124 | ss2 | 25 | ss1 | +0.060230 | 0.286510 |
| L10 | H16 | 22 | ss1 | 124 | ss2 | +0.058251 | 0.212025 |
| L11 | H14 | 180 | other | 124 | ss2 | +0.055397 | 0.764525 |
| L12 | H2 | 22 | ss1 | 124 | ss2 | +0.050109 | 0.705625 |
| L12 | H2 | 124 | ss2 | 180 | other | +0.047359 | 0.600290 |
| L13 | H2 | 25 | ss1 | 22 | ss1 | +0.045159 | 0.339112 |
| L12 | H14 | 124 | ss2 | 180 | other | +0.042002 | 0.465777 |
| L27 | H15 | 122 | ss2 | 23 | ss1 | +0.038861 | 0.465338 |
| L11 | H14 | 181 | other | 124 | ss2 | +0.035748 | 0.660715 |
| L12 | H16 | 22 | ss1 | 181 | other | +0.032557 | 0.108929 |
| L16 | H9 | 20 | ss1 | 24 | ss1 | +0.031538 | 0.553960 |
| L13 | H1 | 22 | ss1 | 124 | ss2 | +0.030943 | 0.393461 |
| L8 | H12 | 180 | other | 124 | ss2 | +0.030635 | 0.365925 |
| L10 | H9 | 181 | other | 124 | ss2 | +0.029234 | 0.416647 |
| L10 | H6 | 136 | flkR | 124 | ss2 | +0.025980 | 0.309207 |
| L32 | H18 | 25 | ss1 | 124 | ss2 | +0.025845 | 0.122941 |
| L22 | H14 | 123 | ss2 | 20 | ss1 | +0.025059 | 0.405950 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L14 | H9 | 24 | ss1 | 22 | ss1 | -0.008842 | 0.317675 |
| L17 | H4 | 26 | ss1 | 26 | ss1 | -0.008844 | 0.502068 |
| L0 | H19 | 155 | flkR | 168 | flkR | -0.009241 | 0.086042 |
| L16 | H9 | 21 | ss1 | 24 | ss1 | -0.010377 | 0.634592 |
| L12 | H16 | 22 | ss1 | 149 | flkR | -0.010397 | 0.102699 |
| L11 | H14 | 115 | other | 180 | other | -0.010765 | 0.111397 |
| L0 | H19 | 148 | flkR | 168 | flkR | -0.010899 | 0.062472 |
| L10 | H6 | 115 | other | 124 | ss2 | -0.011105 | 0.224574 |
| L0 | H19 | 129 | flkR | 168 | flkR | -0.011615 | 0.049891 |
| L8 | H0 | 4 | flkL | 168 | flkR | -0.012410 | 0.406538 |
| L14 | H16 | 115 | other | 22 | ss1 | -0.012831 | 0.502219 |
| L10 | H2 | 181 | other | 180 | other | -0.014328 | 0.291547 |
| L0 | H19 | 21 | ss1 | 168 | flkR | -0.017260 | 0.037328 |
| L14 | H9 | 22 | ss1 | 22 | ss1 | -0.018259 | 0.217737 |
| L12 | H2 | -1 | other | 124 | ss2 | -0.019205 | 0.556269 |
| L13 | H1 | -1 | other | 124 | ss2 | -0.021200 | 0.328286 |
| L10 | H9 | 237 | other | 124 | ss2 | -0.027233 | 0.370165 |
| L13 | H8 | -1 | other | 180 | other | -0.029569 | 0.526558 |
| L13 | H1 | 22 | ss1 | 148 | flkR | -0.030893 | 0.200964 |
| L8 | H12 | 124 | ss2 | 124 | ss2 | -0.051011 | 0.134265 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0242 | 0.00% |
| 10 | 10 | 8 | 0.0242 | 0.00% |
| 20 | 20 | 14 | 0.0242 | 0.01% |
| 50 | 50 | 31 | 0.0243 | 0.02% |
| 100 | 100 | 45 | 0.0255 | 0.16% |
| 200 | 200 | 60 | 0.0279 | 0.45% |
| 500 | 500 | 66 | 0.0609 | 4.47% |
| 1000 | 1,000 | 69 | 0.1309 | 12.97% |
| 2000 | 2,000 | 69 | 0.1671 | 17.37% |
| 5000 | 5,000 | 70 | 0.2985 | 33.35% |
| 10000 | 10,000 | 70 | 0.3611 | 40.97% |
| 20000 | 20,000 | 70 | 0.4372 | 50.21% |
| 50000 | 50,000 | 70 | 0.5217 | 60.48% |

## Motif Analysis

### L7 H13 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 26  |  total attr: +0.0948

**Key mass** (top-1=34%, top-2=45%, top-3=55%)  [DISTR(M164/M124/L166/I22/D163)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 164 | flkR | +0.0324 | 34.2% |
| 124 | ss2 | +0.0101 | 10.6% |
| 166 | flkR | +0.0093 | 9.8% |
| 22 | ss1 | +0.0089 | 9.4% |
| 163 | flkR | +0.0061 | 6.4% |

**Query mass** (top-1=22%, top-2=38%, top-3=51%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 0 | flkL | +0.0213 | 22.5% |
| 124 | ss2 | +0.0149 | 15.7% |
| 22 | ss1 | +0.0122 | 12.9% |
| 163 | flkR | +0.0070 | 7.4% |
| 167 | flkR | +0.0060 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 8 | 30.8% |
| -164 | 3 | 11.5% |
| -40 | 2 | 7.7% |
| +20 | 1 | 3.8% |
| +23 | 1 | 3.8% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 10 | 38.5% |
| flkL | flkR | 3 | 11.5% |
| ss2 | flkR | 2 | 7.7% |
| flkR | other | 2 | 7.7% |
| flkR | ss2 | 2 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 0 | flkL | 164 | flkR | +0.0213 | 0.2799 |
| 22 | ss1 | 22 | ss1 | +0.0089 | 0.0707 |
| 124 | ss2 | 164 | flkR | +0.0078 | 0.0560 |
| 124 | ss2 | 124 | ss2 | +0.0071 | 0.0284 |
| 163 | flkR | 163 | flkR | +0.0061 | 0.3553 |

### L8 H0 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 25  |  total attr: +0.0660

**Key mass** (top-1=28%, top-2=36%, top-3=44%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 165 | flkR | +0.0188 | 28.4% |
| 163 | flkR | +0.0051 | 7.8% |
| 164 | flkR | +0.0050 | 7.6% |
| 7 | flkL | +0.0048 | 7.3% |
| 1 | flkL | +0.0047 | 7.1% |

**Query mass** (top-1=20%, top-2=31%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 1 | flkL | +0.0132 | 19.9% |
| 124 | ss2 | +0.0073 | 11.1% |
| 165 | flkR | +0.0071 | 10.7% |
| 19 | ss1 | +0.0064 | 9.8% |
| 180 | other | +0.0057 | 8.6% |

**Offset distribution [frequency]** (top-2 coverage: 28%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 5 | 20.0% |
| +164 | 2 | 8.0% |
| -141 | 2 | 8.0% |
| -164 | 1 | 4.0% |
| -145 | 1 | 4.0% |

**Region-pair profile** (q→k)  (top=16%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkR | 4 | 16.0% |
| ss1 | flkR | 4 | 16.0% |
| other | flkL | 3 | 12.0% |
| flkR | flkL | 2 | 8.0% |
| ss2 | flkL | 2 | 8.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 1 | flkL | 165 | flkR | +0.0119 | 0.2129 |
| 19 | ss1 | 164 | flkR | +0.0050 | 0.1285 |
| 165 | flkR | 1 | flkL | +0.0047 | 0.1968 |
| 24 | ss1 | 165 | flkR | +0.0045 | 0.1066 |
| 124 | ss2 | 12 | flkL | +0.0045 | 0.0788 |

### L8 H12 — Rank #1

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR  |  cells: 12  |  total attr: +0.3193

**Key mass** (top-1=52%, top-2=80%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.1650 | 51.7% |
| 181 | other | +0.0898 | 28.1% |
| 124 | ss2 | +0.0506 | 15.9% |
| 179 | other | +0.0071 | 2.2% |
| 182 | other | +0.0043 | 1.3% |

**Query mass** (top-1=80%, top-2=89%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.2543 | 79.6% |
| 180 | other | +0.0306 | 9.6% |
| 181 | other | +0.0174 | 5.5% |
| 22 | ss1 | +0.0144 | 4.5% |
| 182 | other | +0.0014 | 0.4% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -56 | 1 | 8.3% |
| -57 | 1 | 8.3% |
| +56 | 1 | 8.3% |
| +57 | 1 | 8.3% |
| -158 | 1 | 8.3% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 4 | 33.3% |
| other | ss2 | 4 | 33.3% |
| ss1 | other | 2 | 16.7% |
| ss2 | ss2 | 1 | 8.3% |
| ss2 | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 124 | ss2 | 180 | other | +0.1550 | 0.2283 |
| 124 | ss2 | 181 | other | +0.0854 | 0.1345 |
| 180 | other | 124 | ss2 | +0.0306 | 0.3659 |
| 181 | other | 124 | ss2 | +0.0174 | 0.2802 |
| 22 | ss1 | 180 | other | +0.0100 | 0.0227 |

### L9 H16 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 4  |  total attr: +0.0290

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0290 | 100.0% |

**Query mass** (top-1=55%, top-2=92%, top-3=96%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | other | +0.0160 | 55.1% |
| 180 | other | +0.0106 | 36.5% |
| 179 | other | +0.0014 | 4.7% |
| 182 | other | +0.0011 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 1 | 25.0% |
| +56 | 1 | 25.0% |
| +55 | 1 | 25.0% |
| +58 | 1 | 25.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss2 | 4 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | other | 124 | ss2 | +0.0160 | 0.2227 |
| 180 | other | 124 | ss2 | +0.0106 | 0.2615 |
| 179 | other | 124 | ss2 | +0.0014 | 0.1951 |
| 182 | other | 124 | ss2 | +0.0011 | 0.1082 |

### L10 H6 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | flkR→ss2  |  cells: 12  |  total attr: +0.0763

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0763 | 100.0% |

**Query mass** (top-1=34%, top-2=50%, top-3=60%)  [DISTR(I136/A133/A132/A137/A117)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 136 | flkR | +0.0260 | 34.1% |
| 133 | flkR | +0.0120 | 15.7% |
| 132 | flkR | +0.0074 | 9.8% |
| 137 | flkR | +0.0063 | 8.3% |
| 117 | other | +0.0051 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +12 | 1 | 8.3% |
| +9 | 1 | 8.3% |
| +8 | 1 | 8.3% |
| +13 | 1 | 8.3% |
| -7 | 1 | 8.3% |

**Region-pair profile** (q→k)  [flkR→ss2]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss2 | 8 | 66.7% |
| other | ss2 | 3 | 25.0% |
| ss2 | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 136 | flkR | 124 | ss2 | +0.0260 | 0.3092 |
| 133 | flkR | 124 | ss2 | +0.0120 | 0.3321 |
| 132 | flkR | 124 | ss2 | +0.0074 | 0.3226 |
| 137 | flkR | 124 | ss2 | +0.0063 | 0.3080 |
| 117 | other | 124 | ss2 | +0.0051 | 0.2320 |

### L10 H9 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 35  |  total attr: +0.1474

**Key mass** (top-1=50%, top-2=89%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0733 | 49.8% |
| 180 | other | +0.0571 | 38.8% |
| 135 | flkR | +0.0100 | 6.8% |
| 181 | other | +0.0069 | 4.7% |

**Query mass** (top-1=22%, top-2=43%, top-3=57%)  [DISTR(M124/V181/L25/I136/?237)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0320 | 21.7% |
| 181 | other | +0.0318 | 21.6% |
| 25 | ss1 | +0.0200 | 13.6% |
| 136 | flkR | +0.0177 | 12.0% |
| 237 | other | +0.0100 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +57 | 1 | 2.9% |
| -56 | 1 | 2.9% |
| +102 | 1 | 2.9% |
| -155 | 1 | 2.9% |
| +0 | 1 | 2.9% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 9 | 25.7% |
| other | ss2 | 5 | 14.3% |
| ss2 | other | 4 | 11.4% |
| ss1 | other | 4 | 11.4% |
| ss1 | ss2 | 4 | 11.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | other | 124 | ss2 | +0.0292 | 0.4166 |
| 124 | ss2 | 180 | other | +0.0200 | 0.6706 |
| 237 | other | 135 | flkR | +0.0100 | 0.3236 |
| 25 | ss1 | 180 | other | +0.0096 | 0.1531 |
| 124 | ss2 | 124 | ss2 | +0.0091 | 0.1978 |

### L10 H16 — Rank #17

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 8  |  total attr: +0.0815

**Key mass** (top-1=94%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0765 | 93.9% |
| 180 | other | +0.0029 | 3.6% |
| 237 | other | +0.0020 | 2.5% |

**Query mass** (top-1=74%, top-2=88%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 22 | ss1 | +0.0603 | 74.0% |
| 25 | ss1 | +0.0112 | 13.7% |
| 124 | ss2 | +0.0029 | 3.6% |
| 20 | ss1 | +0.0026 | 3.2% |
| 21 | ss1 | +0.0019 | 2.3% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -102 | 1 | 12.5% |
| -99 | 1 | 12.5% |
| -56 | 1 | 12.5% |
| -104 | 1 | 12.5% |
| -215 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 62.5% |
| ss2 | other | 1 | 12.5% |
| ss1 | other | 1 | 12.5% |
| flkL | ss2 | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 22 | ss1 | 124 | ss2 | +0.0583 | 0.2120 |
| 25 | ss1 | 124 | ss2 | +0.0112 | 0.1131 |
| 124 | ss2 | 180 | other | +0.0029 | 0.0574 |
| 20 | ss1 | 124 | ss2 | +0.0026 | 0.1058 |
| 22 | ss1 | 237 | other | +0.0020 | 0.0262 |

### L11 H14 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.1350

**Key mass** (top-1=68%, top-2=80%, top-3=90%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0921 | 68.2% |
| 180 | other | +0.0157 | 11.6% |
| 148 | flkR | +0.0133 | 9.9% |
| 149 | flkR | +0.0071 | 5.3% |
| 181 | other | +0.0058 | 4.3% |

**Query mass** (top-1=41%, top-2=68%, top-3=75%)  [DISTR(V180/V181/I136)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.0554 | 41.0% |
| 181 | other | +0.0357 | 26.5% |
| 136 | flkR | +0.0106 | 7.9% |
| 115 | other | +0.0079 | 5.9% |
| 125 | ss2 | +0.0053 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -26 | 2 | 10.0% |
| -54 | 2 | 10.0% |
| +56 | 1 | 5.0% |
| +57 | 1 | 5.0% |
| -44 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 5 | 25.0% |
| ss2 | flkR | 5 | 25.0% |
| ss2 | other | 3 | 15.0% |
| other | ss2 | 2 | 10.0% |
| other | flkR | 2 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 180 | other | 124 | ss2 | +0.0554 | 0.7645 |
| 181 | other | 124 | ss2 | +0.0357 | 0.6607 |
| 136 | flkR | 180 | other | +0.0070 | 0.3312 |
| 115 | other | 148 | flkR | +0.0048 | 0.0824 |
| 136 | flkR | 181 | other | +0.0037 | 0.1884 |

### L11 H17 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0637

**Key mass** (top-1=26%, top-2=49%, top-3=59%)  [DISTR(A133/I136/A137/A132/M124)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 133 | flkR | +0.0166 | 26.0% |
| 136 | flkR | +0.0146 | 22.9% |
| 137 | flkR | +0.0065 | 10.3% |
| 132 | flkR | +0.0052 | 8.1% |
| 124 | ss2 | +0.0047 | 7.4% |

**Query mass** (top-1=34%, top-2=58%, top-3=79%)  [DISTR(V180/I22/V181)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.0217 | 34.1% |
| 22 | ss1 | +0.0154 | 24.1% |
| 181 | other | +0.0133 | 20.9% |
| 237 | other | +0.0070 | 11.0% |
| 124 | ss2 | +0.0027 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +44 | 2 | 10.0% |
| +48 | 2 | 10.0% |
| +47 | 1 | 5.0% |
| +45 | 1 | 5.0% |
| -93 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 8 | 40.0% |
| ss1 | flkR | 4 | 20.0% |
| ss1 | other | 2 | 10.0% |
| other | other | 2 | 10.0% |
| ss2 | ss2 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 180 | other | 133 | flkR | +0.0100 | 0.2602 |
| 180 | other | 136 | flkR | +0.0082 | 0.1339 |
| 181 | other | 136 | flkR | +0.0053 | 0.1321 |
| 181 | other | 133 | flkR | +0.0048 | 0.1652 |
| 22 | ss1 | 115 | other | +0.0045 | 0.0576 |

### L11 H18 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0757

**Key mass** (top-1=23%, top-2=42%, top-3=56%)  [DISTR(I136/L25/?237/?-1/F120)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 136 | flkR | +0.0177 | 23.3% |
| 25 | ss1 | +0.0145 | 19.1% |
| 237 | other | +0.0105 | 13.9% |
| -1 | other | +0.0102 | 13.5% |
| 120 | ss2 | +0.0032 | 4.3% |

**Query mass** (top-1=44%, top-2=66%, top-3=76%)  [DISTR(I22/L25/V180)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 22 | ss1 | +0.0336 | 44.3% |
| 25 | ss1 | +0.0162 | 21.5% |
| 180 | other | +0.0078 | 10.3% |
| 181 | other | +0.0034 | 4.5% |
| 18 | ss1 | +0.0032 | 4.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -114 | 2 | 10.0% |
| -164 | 2 | 10.0% |
| +0 | 1 | 5.0% |
| +23 | 1 | 5.0% |
| -57 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 6 | 30.0% |
| other | other | 4 | 20.0% |
| ss1 | flkR | 3 | 15.0% |
| flkL | flkR | 3 | 15.0% |
| ss1 | ss1 | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 22 | ss1 | 136 | flkR | +0.0177 | 0.5197 |
| 25 | ss1 | 25 | ss1 | +0.0145 | 0.3301 |
| 22 | ss1 | -1 | other | +0.0077 | 0.1152 |
| 180 | other | 237 | other | +0.0063 | 0.2401 |
| 18 | ss1 | 120 | ss2 | +0.0032 | 0.1869 |

### L12 H2 — Rank #12

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR  |  cells: 19  |  total attr: +0.1329

**Key mass** (top-1=48%, top-2=89%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.0640 | 48.1% |
| 124 | ss2 | +0.0542 | 40.8% |
| 181 | other | +0.0086 | 6.4% |
| 149 | flkR | +0.0031 | 2.3% |
| 148 | flkR | +0.0022 | 1.6% |

**Query mass** (top-1=42%, top-2=79%, top-3=86%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0552 | 41.5% |
| 22 | ss1 | +0.0501 | 37.7% |
| 133 | flkR | +0.0085 | 6.4% |
| 25 | ss1 | +0.0037 | 2.8% |
| -1 | other | +0.0032 | 2.4% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -57 | 2 | 10.5% |
| -48 | 2 | 10.5% |
| -102 | 1 | 5.3% |
| -56 | 1 | 5.3% |
| -47 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 5 | 26.3% |
| flkR | other | 5 | 26.3% |
| ss1 | ss2 | 3 | 15.8% |
| other | flkR | 2 | 10.5% |
| ss2 | flkR | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 22 | ss1 | 124 | ss2 | +0.0501 | 0.7056 |
| 124 | ss2 | 180 | other | +0.0474 | 0.6003 |
| 124 | ss2 | 181 | other | +0.0069 | 0.0894 |
| 133 | flkR | 180 | other | +0.0069 | 0.4609 |
| 25 | ss1 | 124 | ss2 | +0.0027 | 0.1326 |

### L12 H14 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 28  |  total attr: +0.1297

**Key mass** (top-1=68%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.0888 | 68.4% |
| 181 | other | +0.0347 | 26.7% |
| 237 | other | +0.0021 | 1.6% |
| 124 | ss2 | +0.0019 | 1.4% |
| 22 | ss1 | +0.0012 | 1.0% |

**Query mass** (top-1=46%, top-2=58%, top-3=65%)  [DISTR(M124/I22/?237/L122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0603 | 46.5% |
| 22 | ss1 | +0.0155 | 12.0% |
| 237 | other | +0.0080 | 6.1% |
| 122 | ss2 | +0.0073 | 5.6% |
| 180 | other | +0.0066 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -56 | 1 | 3.6% |
| -57 | 1 | 3.6% |
| -158 | 1 | 3.6% |
| -58 | 1 | 3.6% |
| +57 | 1 | 3.6% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 8 | 28.6% |
| ss1 | other | 6 | 21.4% |
| other | other | 5 | 17.9% |
| flkR | other | 5 | 17.9% |
| other | ss2 | 1 | 3.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 124 | ss2 | 180 | other | +0.0420 | 0.4658 |
| 124 | ss2 | 181 | other | +0.0172 | 0.2085 |
| 22 | ss1 | 180 | other | +0.0108 | 0.1583 |
| 122 | ss2 | 180 | other | +0.0051 | 0.3161 |
| 237 | other | 180 | other | +0.0050 | 0.1044 |

### L12 H16 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 10  |  total attr: +0.1831

**Key mass** (top-1=68%, top-2=87%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.1251 | 68.4% |
| 181 | other | +0.0336 | 18.4% |
| 148 | flkR | +0.0112 | 6.1% |
| 149 | flkR | +0.0053 | 2.9% |
| 237 | other | +0.0039 | 2.2% |

**Query mass** (top-1=87%, top-2=95%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 22 | ss1 | +0.1584 | 86.5% |
| -1 | other | +0.0165 | 9.0% |
| 124 | ss2 | +0.0032 | 1.8% |
| 237 | other | +0.0029 | 1.6% |
| 148 | flkR | +0.0021 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -158 | 1 | 10.0% |
| -159 | 1 | 10.0% |
| -149 | 1 | 10.0% |
| -150 | 1 | 10.0% |
| -215 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 3 | 30.0% |
| other | flkR | 2 | 20.0% |
| ss2 | other | 2 | 20.0% |
| other | other | 1 | 10.0% |
| flkR | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 22 | ss1 | 180 | other | +0.1219 | 0.3729 |
| 22 | ss1 | 181 | other | +0.0326 | 0.1089 |
| -1 | other | 148 | flkR | +0.0112 | 0.2563 |
| -1 | other | 149 | flkR | +0.0053 | 0.1438 |
| 22 | ss1 | 237 | other | +0.0039 | 0.0427 |

### L13 H1 — Rank #26

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.1450

**Key mass** (top-1=41%, top-2=65%, top-3=85%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0596 | 41.1% |
| 148 | flkR | +0.0344 | 23.7% |
| 180 | other | +0.0287 | 19.8% |
| 181 | other | +0.0158 | 10.9% |
| 149 | flkR | +0.0030 | 2.1% |

**Query mass** (top-1=41%, top-2=62%, top-3=71%)  [DISTR(I22/?-1/V148)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 22 | ss1 | +0.0599 | 41.3% |
| -1 | other | +0.0296 | 20.4% |
| 148 | flkR | +0.0132 | 9.1% |
| 21 | ss1 | +0.0080 | 5.5% |
| 20 | ss1 | +0.0064 | 4.4% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -159 | 2 | 8.3% |
| -33 | 2 | 8.3% |
| -102 | 1 | 4.2% |
| -149 | 1 | 4.2% |
| -158 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 33.3% |
| ss1 | other | 4 | 16.7% |
| flkL | flkR | 4 | 16.7% |
| other | flkR | 3 | 12.5% |
| flkR | other | 2 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 22 | ss1 | 124 | ss2 | +0.0309 | 0.3935 |
| -1 | other | 148 | flkR | +0.0241 | 0.2100 |
| 22 | ss1 | 180 | other | +0.0174 | 0.1167 |
| 22 | ss1 | 181 | other | +0.0116 | 0.0798 |
| 148 | flkR | 180 | other | +0.0090 | 0.1322 |

### L13 H2 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 16  |  total attr: +0.1246

**Key mass** (top-1=70%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 22 | ss1 | +0.0868 | 69.7% |
| 124 | ss2 | +0.0325 | 26.0% |
| 180 | other | +0.0044 | 3.5% |
| 20 | ss1 | +0.0009 | 0.8% |

**Query mass** (top-1=36%, top-2=54%, top-3=60%)  [DISTR(L25/D26/K128/L23/A123)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0452 | 36.2% |
| 26 | ss1 | +0.0218 | 17.5% |
| 128 | ss2 | +0.0082 | 6.6% |
| 23 | ss1 | +0.0080 | 6.4% |
| 123 | ss2 | +0.0071 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 2 | 12.5% |
| +4 | 2 | 12.5% |
| +1 | 2 | 12.5% |
| -1 | 2 | 12.5% |
| +2 | 2 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 43.8% |
| ss2 | ss2 | 6 | 37.5% |
| other | other | 2 | 12.5% |
| flkR | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 25 | ss1 | 22 | ss1 | +0.0452 | 0.3391 |
| 26 | ss1 | 22 | ss1 | +0.0218 | 0.2651 |
| 128 | ss2 | 124 | ss2 | +0.0082 | 0.5229 |
| 23 | ss1 | 22 | ss1 | +0.0080 | 0.3425 |
| 123 | ss2 | 124 | ss2 | +0.0071 | 0.5115 |

### L13 H8 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.1092

**Key mass** (top-1=66%, top-2=91%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | other | +0.0722 | 66.1% |
| 181 | other | +0.0275 | 25.2% |
| 148 | flkR | +0.0059 | 5.4% |
| 22 | ss1 | +0.0026 | 2.4% |
| 149 | flkR | +0.0010 | 1.0% |

**Query mass** (top-1=29%, top-2=47%, top-3=59%)  [DISTR(L25/V21/G20/I22/L23)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0319 | 29.2% |
| 21 | ss1 | +0.0198 | 18.1% |
| 20 | ss1 | +0.0133 | 12.2% |
| 22 | ss1 | +0.0110 | 10.0% |
| 23 | ss1 | +0.0104 | 9.5% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -155 | 2 | 11.1% |
| -159 | 2 | 11.1% |
| -158 | 2 | 11.1% |
| -160 | 2 | 11.1% |
| -156 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=78%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 14 | 77.8% |
| other | flkR | 2 | 11.1% |
| other | ss1 | 1 | 5.6% |
| ss2 | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 25 | ss1 | 180 | other | +0.0235 | 0.2674 |
| 21 | ss1 | 180 | other | +0.0142 | 0.4563 |
| 22 | ss1 | 180 | other | +0.0090 | 0.5437 |
| 20 | ss1 | 180 | other | +0.0085 | 0.2845 |
| 25 | ss1 | 181 | other | +0.0084 | 0.1162 |

### L16 H9 — Rank #8

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 19  |  total attr: +0.1067

**Key mass** (top-1=41%, top-2=80%, top-3=92%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 24 | ss1 | +0.0434 | 40.6% |
| 22 | ss1 | +0.0424 | 39.8% |
| 124 | ss2 | +0.0126 | 11.8% |
| 115 | other | +0.0032 | 3.0% |
| 23 | ss1 | +0.0014 | 1.4% |

**Query mass** (top-1=33%, top-2=45%, top-3=56%)  [DISTR(G20/I22/D24/D26/D18)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 20 | ss1 | +0.0352 | 32.9% |
| 22 | ss1 | +0.0129 | 12.1% |
| 24 | ss1 | +0.0119 | 11.2% |
| 26 | ss1 | +0.0113 | 10.6% |
| 18 | ss1 | +0.0098 | 9.2% |

**Offset distribution [frequency]** (top-2 coverage: 42%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 4 | 21.1% |
| +0 | 4 | 21.1% |
| -3 | 3 | 15.8% |
| -2 | 2 | 10.5% |
| -5 | 2 | 10.5% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 57.9% |
| ss2 | ss2 | 4 | 21.1% |
| other | other | 1 | 5.3% |
| flkR | ss2 | 1 | 5.3% |
| flkR | flkR | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 20 | ss1 | 24 | ss1 | +0.0315 | 0.5540 |
| 26 | ss1 | 22 | ss1 | +0.0113 | 0.4299 |
| 24 | ss1 | 22 | ss1 | +0.0102 | 0.4968 |
| 22 | ss1 | 24 | ss1 | +0.0101 | 0.4077 |
| 18 | ss1 | 22 | ss1 | +0.0098 | 0.3130 |

### L18 H8 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 15  |  total attr: +0.0478

**Key mass** (top-1=34%, top-2=58%, top-3=73%)  [DISTR(D24/L23/G27)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 24 | ss1 | +0.0161 | 33.7% |
| 23 | ss1 | +0.0117 | 24.6% |
| 27 | ss1 | +0.0069 | 14.3% |
| 22 | ss1 | +0.0043 | 8.9% |
| 125 | ss2 | +0.0026 | 5.4% |

**Query mass** (top-1=53%, top-2=64%, top-3=73%)  [DISTR(G20/L25/I22)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 20 | ss1 | +0.0253 | 52.9% |
| 25 | ss1 | +0.0054 | 11.4% |
| 22 | ss1 | +0.0041 | 8.5% |
| 19 | ss1 | +0.0040 | 8.4% |
| 122 | ss2 | +0.0037 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 5 | 33.3% |
| -3 | 4 | 26.7% |
| -1 | 4 | 26.7% |
| -4 | 2 | 13.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 10 | 66.7% |
| ss2 | ss2 | 3 | 20.0% |
| flkR | flkR | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 20 | ss1 | 24 | ss1 | +0.0136 | 0.5529 |
| 20 | ss1 | 23 | ss1 | +0.0074 | 0.2269 |
| 25 | ss1 | 27 | ss1 | +0.0054 | 0.1396 |
| 20 | ss1 | 22 | ss1 | +0.0030 | 0.1357 |
| 19 | ss1 | 23 | ss1 | +0.0027 | 0.1775 |

### L21 H2 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.0567

**Key mass** (top-1=24%, top-2=47%, top-3=64%)  [DISTR(M124/I22/L115/L23)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0137 | 24.1% |
| 22 | ss1 | +0.0128 | 22.6% |
| 115 | other | +0.0100 | 17.6% |
| 23 | ss1 | +0.0081 | 14.3% |
| 21 | ss1 | +0.0030 | 5.3% |

**Query mass** (top-1=27%, top-2=41%, top-3=53%)  [DISTR(A123/D26/M124/T28/G27)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 123 | ss2 | +0.0155 | 27.4% |
| 26 | ss1 | +0.0080 | 14.0% |
| 124 | ss2 | +0.0066 | 11.6% |
| 28 | other | +0.0056 | 9.9% |
| 27 | ss1 | +0.0045 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 4 | 14.8% |
| +5 | 4 | 14.8% |
| +4 | 3 | 11.1% |
| +2 | 3 | 11.1% |
| +8 | 2 | 7.4% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 33.3% |
| ss2 | ss2 | 7 | 25.9% |
| ss2 | other | 4 | 14.8% |
| other | ss1 | 3 | 11.1% |
| flkR | flkR | 2 | 7.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 123 | ss2 | 115 | other | +0.0073 | 0.3814 |
| 124 | ss2 | 124 | ss2 | +0.0049 | 0.0924 |
| 123 | ss2 | 124 | ss2 | +0.0038 | 0.1341 |
| 26 | ss1 | 23 | ss1 | +0.0037 | 0.1312 |
| 27 | ss1 | 22 | ss1 | +0.0035 | 0.4054 |

### L22 H14 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 23  |  total attr: +0.0709

**Key mass** (top-1=43%, top-2=57%, top-3=69%)  [DISTR(G20/L122/I22/V21)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 20 | ss1 | +0.0304 | 42.8% |
| 122 | ss2 | +0.0099 | 14.0% |
| 22 | ss1 | +0.0083 | 11.7% |
| 21 | ss1 | +0.0062 | 8.8% |
| 23 | ss1 | +0.0035 | 4.9% |

**Query mass** (top-1=35%, top-2=49%, top-3=60%)  [DISTR(A123/L122/V21/F120)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 123 | ss2 | +0.0251 | 35.4% |
| 122 | ss2 | +0.0095 | 13.3% |
| 21 | ss1 | +0.0079 | 11.1% |
| 120 | ss2 | +0.0074 | 10.4% |
| 25 | ss1 | +0.0045 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 3 | 13.0% |
| +102 | 3 | 13.0% |
| +103 | 2 | 8.7% |
| +101 | 2 | 8.7% |
| -99 | 2 | 8.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 13 | 56.5% |
| ss1 | ss2 | 6 | 26.1% |
| ss1 | ss1 | 4 | 17.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 123 | ss2 | 20 | ss1 | +0.0251 | 0.4060 |
| 21 | ss1 | 122 | ss2 | +0.0070 | 0.1602 |
| 122 | ss2 | 21 | ss1 | +0.0053 | 0.1026 |
| 120 | ss2 | 20 | ss1 | +0.0037 | 0.2715 |
| 125 | ss2 | 22 | ss1 | +0.0033 | 0.4860 |

### L23 H15 — Rank #28

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR  |  cells: 14  |  total attr: +0.0258

**Key mass** (top-1=24%, top-2=43%, top-3=58%)  [DISTR(L115/L122/A165/F120)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 115 | other | +0.0061 | 23.7% |
| 122 | ss2 | +0.0051 | 19.6% |
| 165 | flkR | +0.0038 | 14.8% |
| 120 | ss2 | +0.0037 | 14.2% |
| 148 | flkR | +0.0019 | 7.3% |

**Query mass** (top-1=47%, top-2=64%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0121 | 47.0% |
| 124 | ss2 | +0.0045 | 17.5% |
| 21 | ss1 | +0.0044 | 17.2% |
| 23 | ss1 | +0.0023 | 8.8% |
| 19 | ss1 | +0.0013 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -90 | 1 | 7.1% |
| -101 | 1 | 7.1% |
| -95 | 1 | 7.1% |
| -97 | 1 | 7.1% |
| -24 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 35.7% |
| ss2 | flkR | 4 | 28.6% |
| ss1 | flkR | 3 | 21.4% |
| ss1 | other | 2 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 25 | ss1 | 115 | other | +0.0050 | 0.1159 |
| 21 | ss1 | 122 | ss2 | +0.0030 | 0.2160 |
| 25 | ss1 | 120 | ss2 | +0.0022 | 0.0552 |
| 25 | ss1 | 122 | ss2 | +0.0021 | 0.0749 |
| 124 | ss2 | 148 | flkR | +0.0019 | 0.1033 |

### L23 H16 — Rank #22

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | ss1→flkL  |  cells: 9  |  total attr: +0.0151

**Key mass** (top-1=36%, top-2=56%, top-3=72%)  [DISTR(A16/A165/A15)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | flkL | +0.0054 | 36.0% |
| 165 | flkR | +0.0029 | 19.5% |
| 15 | flkL | +0.0024 | 16.1% |
| 13 | flkL | +0.0019 | 12.8% |
| 22 | ss1 | +0.0013 | 8.4% |

**Query mass** (top-1=50%, top-2=70%, top-3=79%)  [DISTR(L25/M124/D26)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0076 | 50.2% |
| 124 | ss2 | +0.0029 | 19.5% |
| 26 | ss1 | +0.0014 | 9.5% |
| 24 | ss1 | +0.0011 | 7.2% |
| 21 | ss1 | +0.0011 | 7.1% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +9 | 2 | 22.2% |
| +10 | 2 | 22.2% |
| -41 | 1 | 11.1% |
| +3 | 1 | 11.1% |
| +8 | 1 | 11.1% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 6 | 66.7% |
| ss1 | ss1 | 2 | 22.2% |
| ss2 | flkR | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 124 | ss2 | 165 | flkR | +0.0029 | 0.2178 |
| 25 | ss1 | 16 | flkL | +0.0029 | 0.1286 |
| 25 | ss1 | 15 | flkL | +0.0024 | 0.0876 |
| 26 | ss1 | 16 | flkL | +0.0014 | 0.0631 |
| 25 | ss1 | 22 | ss1 | +0.0013 | 0.0798 |

### L24 H18 — Rank #18

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 9  |  total attr: +0.0196

**Key mass** (top-1=26%, top-2=50%, top-3=65%)  [DISTR(M124/D26/A165/V168)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0050 | 25.6% |
| 26 | ss1 | +0.0047 | 23.9% |
| 165 | flkR | +0.0031 | 15.6% |
| 168 | flkR | +0.0016 | 8.0% |
| 123 | ss2 | +0.0015 | 7.8% |

**Query mass** (top-1=51%, top-2=75%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0100 | 50.9% |
| 128 | ss2 | +0.0047 | 23.9% |
| 125 | ss2 | +0.0019 | 9.7% |
| 20 | ss1 | +0.0015 | 7.8% |
| 124 | ss2 | +0.0015 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -99 | 1 | 11.1% |
| +102 | 1 | 11.1% |
| -140 | 1 | 11.1% |
| -143 | 1 | 11.1% |
| -103 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 2 | 22.2% |
| ss2 | ss1 | 2 | 22.2% |
| ss1 | flkR | 2 | 22.2% |
| ss2 | other | 1 | 11.1% |
| ss1 | flkL | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 25 | ss1 | 124 | ss2 | +0.0050 | 0.0690 |
| 128 | ss2 | 26 | ss1 | +0.0047 | 0.0626 |
| 25 | ss1 | 165 | flkR | +0.0021 | 0.1282 |
| 25 | ss1 | 168 | flkR | +0.0016 | 0.1333 |
| 20 | ss1 | 123 | ss2 | +0.0015 | 0.0432 |

### L26 H6 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 12  |  total attr: +0.0449

**Key mass** (top-1=23%, top-2=43%, top-3=58%)  [DISTR(L25/L23/D26/D24)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0104 | 23.2% |
| 23 | ss1 | +0.0087 | 19.5% |
| 26 | ss1 | +0.0070 | 15.5% |
| 24 | ss1 | +0.0055 | 12.3% |
| 20 | ss1 | +0.0032 | 7.2% |

**Query mass** (top-1=39%, top-2=64%, top-3=71%)  [DISTR(L23/V21/D18)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 23 | ss1 | +0.0173 | 38.6% |
| 21 | ss1 | +0.0113 | 25.3% |
| 18 | ss1 | +0.0032 | 7.2% |
| 25 | ss1 | +0.0030 | 6.6% |
| 24 | ss1 | +0.0028 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 83%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 6 | 50.0% |
| -2 | 4 | 33.3% |
| -1 | 2 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 9 | 75.0% |
| flkR | flkR | 3 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 23 | ss1 | 25 | ss1 | +0.0104 | 0.4365 |
| 21 | ss1 | 23 | ss1 | +0.0087 | 0.3036 |
| 23 | ss1 | 26 | ss1 | +0.0040 | 0.1453 |
| 18 | ss1 | 20 | ss1 | +0.0032 | 0.2798 |
| 25 | ss1 | 26 | ss1 | +0.0030 | 0.2010 |

### L26 H16 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 38  |  total attr: +0.1054

**Key mass** (top-1=20%, top-2=35%, top-3=48%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 120 | ss2 | +0.0206 | 19.5% |
| 121 | ss2 | +0.0166 | 15.8% |
| 123 | ss2 | +0.0134 | 12.7% |
| 146 | flkR | +0.0108 | 10.2% |
| 122 | ss2 | +0.0075 | 7.1% |

**Query mass** (top-1=17%, top-2=33%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 23 | ss1 | +0.0177 | 16.8% |
| 18 | ss1 | +0.0171 | 16.3% |
| 20 | ss1 | +0.0116 | 11.0% |
| 25 | ss1 | +0.0104 | 9.9% |
| 21 | ss1 | +0.0094 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -102 | 6 | 15.8% |
| -100 | 4 | 10.5% |
| -101 | 4 | 10.5% |
| -103 | 3 | 7.9% |
| -22 | 3 | 7.9% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 20 | 52.6% |
| ss2 | flkR | 8 | 21.1% |
| ss2 | ss1 | 5 | 13.2% |
| ss1 | ss1 | 2 | 5.3% |
| ss1 | other | 1 | 2.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 18 | ss1 | 120 | ss2 | +0.0119 | 0.4177 |
| 23 | ss1 | 123 | ss2 | +0.0102 | 0.2235 |
| 20 | ss1 | 121 | ss2 | +0.0092 | 0.6946 |
| 122 | ss2 | 146 | flkR | +0.0076 | 0.2974 |
| 18 | ss1 | 121 | ss2 | +0.0052 | 0.1030 |

### L27 H15 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.1081

**Key mass** (top-1=36%, top-2=53%, top-3=63%)  [DISTR(L23/R121/A123/V21)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 23 | ss1 | +0.0389 | 35.9% |
| 121 | ss2 | +0.0189 | 17.5% |
| 123 | ss2 | +0.0106 | 9.8% |
| 21 | ss1 | +0.0094 | 8.7% |
| 26 | ss1 | +0.0080 | 7.4% |

**Query mass** (top-1=43%, top-2=60%, top-3=70%)  [DISTR(L122/D18/G20/M124)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss2 | +0.0470 | 43.5% |
| 18 | ss1 | +0.0179 | 16.5% |
| 20 | ss1 | +0.0106 | 9.8% |
| 124 | ss2 | +0.0086 | 8.0% |
| 128 | ss2 | +0.0080 | 7.4% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -103 | 3 | 18.8% |
| +102 | 2 | 12.5% |
| +103 | 2 | 12.5% |
| +99 | 1 | 6.2% |
| +101 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 37.5% |
| ss1 | ss2 | 6 | 37.5% |
| ss2 | flkR | 3 | 18.8% |
| flkR | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss2 | 23 | ss1 | +0.0389 | 0.4653 |
| 18 | ss1 | 121 | ss2 | +0.0179 | 0.3383 |
| 20 | ss1 | 123 | ss2 | +0.0106 | 0.1852 |
| 122 | ss2 | 21 | ss1 | +0.0082 | 0.1082 |
| 128 | ss2 | 26 | ss1 | +0.0080 | 0.1008 |

### L29 H18 — Rank #10

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 38  |  total attr: +0.1075

**Key mass** (top-1=18%, top-2=35%, top-3=46%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 133 | flkR | +0.0189 | 17.6% |
| 137 | flkR | +0.0189 | 17.5% |
| 128 | ss2 | +0.0121 | 11.2% |
| 120 | ss2 | +0.0068 | 6.3% |
| 165 | flkR | +0.0037 | 3.5% |

**Query mass** (top-1=20%, top-2=39%, top-3=56%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0220 | 20.5% |
| 124 | ss2 | +0.0199 | 18.5% |
| 26 | ss1 | +0.0181 | 16.8% |
| 123 | ss2 | +0.0054 | 5.0% |
| 18 | ss1 | +0.0042 | 3.9% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -102 | 2 | 5.3% |
| -103 | 2 | 5.3% |
| -99 | 2 | 5.3% |
| +102 | 2 | 5.3% |
| -108 | 1 | 2.6% |

**Region-pair profile** (q→k)  (top=21%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 8 | 21.1% |
| ss1 | ss2 | 7 | 18.4% |
| flkR | flkR | 7 | 18.4% |
| ss2 | flkR | 5 | 13.2% |
| ss1 | other | 4 | 10.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 25 | ss1 | 133 | flkR | +0.0178 | 0.2256 |
| 124 | ss2 | 137 | flkR | +0.0168 | 0.2533 |
| 26 | ss1 | 128 | ss2 | +0.0121 | 0.1173 |
| 18 | ss1 | 121 | ss2 | +0.0032 | 0.0574 |
| 26 | ss1 | 136 | flkR | +0.0030 | 0.0435 |

### L30 H1 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 9  |  total attr: +0.0261

**Key mass** (top-1=32%, top-2=53%, top-3=63%)  [DISTR(V21/T147/A123/K128)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 21 | ss1 | +0.0084 | 32.0% |
| 147 | flkR | +0.0054 | 20.5% |
| 123 | ss2 | +0.0029 | 10.9% |
| 128 | ss2 | +0.0028 | 10.6% |
| 119 | ss2 | +0.0018 | 6.9% |

**Query mass** (top-1=36%, top-2=57%, top-3=72%)  [DISTR(L122/A123/D26)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss2 | +0.0094 | 36.0% |
| 123 | ss2 | +0.0054 | 20.5% |
| 26 | ss1 | +0.0041 | 15.5% |
| 20 | ss1 | +0.0029 | 10.9% |
| 19 | ss1 | +0.0018 | 6.9% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -103 | 2 | 22.2% |
| +102 | 2 | 22.2% |
| +101 | 1 | 11.1% |
| -24 | 1 | 11.1% |
| -102 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 55.6% |
| ss2 | ss1 | 3 | 33.3% |
| ss2 | flkR | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss2 | 21 | ss1 | +0.0084 | 0.1946 |
| 123 | ss2 | 147 | flkR | +0.0054 | 0.6327 |
| 20 | ss1 | 123 | ss2 | +0.0029 | 0.0450 |
| 26 | ss1 | 128 | ss2 | +0.0028 | 0.0342 |
| 19 | ss1 | 119 | ss2 | +0.0018 | 0.1010 |

### L32 H13 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.0625

**Key mass** (top-1=20%, top-2=34%, top-3=47%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 26 | ss1 | +0.0127 | 20.3% |
| 128 | ss2 | +0.0084 | 13.4% |
| 124 | ss2 | +0.0082 | 13.1% |
| 122 | ss2 | +0.0054 | 8.7% |
| 23 | ss1 | +0.0047 | 7.6% |

**Query mass** (top-1=20%, top-2=34%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 128 | ss2 | +0.0127 | 20.3% |
| 26 | ss1 | +0.0084 | 13.4% |
| 25 | ss1 | +0.0082 | 13.1% |
| 122 | ss2 | +0.0079 | 12.6% |
| 18 | ss1 | +0.0049 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -103 | 3 | 20.0% |
| -102 | 2 | 13.3% |
| -99 | 2 | 13.3% |
| +99 | 2 | 13.3% |
| +103 | 2 | 13.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 53.3% |
| ss2 | ss1 | 7 | 46.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 128 | ss2 | 26 | ss1 | +0.0127 | 0.1110 |
| 26 | ss1 | 128 | ss2 | +0.0084 | 0.0734 |
| 25 | ss1 | 124 | ss2 | +0.0082 | 0.0638 |
| 122 | ss2 | 23 | ss1 | +0.0047 | 0.0717 |
| 20 | ss1 | 123 | ss2 | +0.0047 | 0.0572 |

### L32 H18 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.1453

**Key mass** (top-1=43%, top-2=61%, top-3=76%)  [DISTR(L25/M124/L122)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 25 | ss1 | +0.0629 | 43.3% |
| 124 | ss2 | +0.0258 | 17.8% |
| 122 | ss2 | +0.0213 | 14.6% |
| 120 | ss2 | +0.0077 | 5.3% |
| 26 | ss1 | +0.0072 | 5.0% |

**Query mass** (top-1=41%, top-2=59%, top-3=68%)  [DISTR(M124/L25/V21/G20)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss2 | +0.0602 | 41.4% |
| 25 | ss1 | +0.0258 | 17.8% |
| 21 | ss1 | +0.0128 | 8.8% |
| 20 | ss1 | +0.0100 | 6.9% |
| 128 | ss2 | +0.0099 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +103 | 4 | 26.7% |
| +99 | 2 | 13.3% |
| -99 | 2 | 13.3% |
| -103 | 2 | 13.3% |
| -102 | 2 | 13.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 53.3% |
| ss2 | ss1 | 7 | 46.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 124 | ss2 | 25 | ss1 | +0.0602 | 0.2865 |
| 25 | ss1 | 124 | ss2 | +0.0258 | 0.1229 |
| 21 | ss1 | 122 | ss2 | +0.0128 | 0.1004 |
| 23 | ss1 | 122 | ss2 | +0.0085 | 0.0778 |
| 128 | ss2 | 26 | ss1 | +0.0072 | 0.0385 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #27 | L7 | H13 | 26 | +0.0948 | DISTRIBUTED | M164/M124/L166/I22/D163 | DISTRIBUTED |  |  |  |
| #25 | L8 | H0 | 25 | +0.0660 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #1 | L8 | H12 | 12 | +0.3193 | DUAL-ANCHOR | V180/V181 | SINGLE-ANCHOR | M124 |  |  |
| #24 | L9 | H16 | 4 | +0.0290 | SINGLE-ANCHOR | M124 | DUAL-ANCHOR | V181/V180 |  |  |
| #21 | L10 | H6 | 12 | +0.0763 | SINGLE-ANCHOR | M124 | DISTRIBUTED | I136/A133/A132/A137/A117 |  | flkR→ss2 |
| #9 | L10 | H9 | 35 | +0.1474 | DUAL-ANCHOR | M124/V180 | DISTRIBUTED | M124/V181/L25/I136/?237 |  |  |
| #17 | L10 | H16 | 8 | +0.0815 | SINGLE-ANCHOR | M124 | SINGLE-ANCHOR | I22 |  | CROSS:ss1→ss2 |
| #16 | L11 | H14 | 20 | +0.1350 | SINGLE-ANCHOR | M124 | DISTRIBUTED | V180/V181/I136 |  |  |
| #13 | L11 | H17 | 20 | +0.0637 | DISTRIBUTED | A133/I136/A137/A132/M124 | DISTRIBUTED | V180/I22/V181 |  |  |
| #15 | L11 | H18 | 20 | +0.0757 | DISTRIBUTED | I136/L25/?237/?-1/F120 | DISTRIBUTED | I22/L25/V180 |  |  |
| #12 | L12 | H2 | 19 | +0.1329 | DUAL-ANCHOR | V180/M124 | DUAL-ANCHOR | M124/I22 |  |  |
| #20 | L12 | H14 | 28 | +0.1297 | SINGLE-ANCHOR | V180 | DISTRIBUTED | M124/I22/?237/L122 |  |  |
| #5 | L12 | H16 | 10 | +0.1831 | SINGLE-ANCHOR | V180 | SINGLE-ANCHOR | I22 |  |  |
| #26 | L13 | H1 | 24 | +0.1450 | MULTI-ANCHOR |  | DISTRIBUTED | I22/?-1/V148 |  |  |
| #11 | L13 | H2 | 16 | +0.1246 | SINGLE-ANCHOR | I22 | DISTRIBUTED | L25/D26/K128/L23/A123 |  | INTRA:ss1 |
| #29 | L13 | H8 | 18 | +0.1092 | SINGLE-ANCHOR | V180 | DISTRIBUTED | L25/V21/G20/I22/L23 |  |  |
| #8 | L16 | H9 | 19 | +0.1067 | DUAL-ANCHOR | D24/I22 | DISTRIBUTED | G20/I22/D24/D26/D18 |  | INTRA:ss1 |
| #23 | L18 | H8 | 15 | +0.0478 | DISTRIBUTED | D24/L23/G27 | DISTRIBUTED | G20/L25/I22 | POSITIONAL | INTRA:ss1 |
| #19 | L21 | H2 | 27 | +0.0567 | DISTRIBUTED | M124/I22/L115/L23 | DISTRIBUTED | A123/D26/M124/T28/G27 |  |  |
| #6 | L22 | H14 | 23 | +0.0709 | DISTRIBUTED | G20/L122/I22/V21 | DISTRIBUTED | A123/L122/V21/F120 |  | CROSS:ss2→ss1 |
| #28 | L23 | H15 | 14 | +0.0258 | DISTRIBUTED | L115/L122/A165/F120 | MULTI-ANCHOR |  |  |  |
| #22 | L23 | H16 | 9 | +0.0151 | DISTRIBUTED | A16/A165/A15 | DISTRIBUTED | L25/M124/D26 |  | ss1→flkL |
| #18 | L24 | H18 | 9 | +0.0196 | DISTRIBUTED | M124/D26/A165/V168 | DUAL-ANCHOR | L25/K128 |  |  |
| #30 | L26 | H6 | 12 | +0.0449 | DISTRIBUTED | L25/L23/D26/D24 | DISTRIBUTED | L23/V21/D18 | POSITIONAL | INTRA:ss1 |
| #4 | L26 | H16 | 38 | +0.1054 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #3 | L27 | H15 | 16 | +0.1081 | DISTRIBUTED | L23/R121/A123/V21 | DISTRIBUTED | L122/D18/G20/M124 |  |  |
| #10 | L29 | H18 | 38 | +0.1075 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #14 | L30 | H1 | 9 | +0.0261 | DISTRIBUTED | V21/T147/A123/K128 | DISTRIBUTED | L122/A123/D26 |  | CROSS:ss1→ss2 |
| #7 | L32 | H13 | 15 | +0.0625 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #2 | L32 | H18 | 15 | +0.1453 | DISTRIBUTED | L25/M124/L122 | DISTRIBUTED | M124/L25/V21/G20 |  | CROSS:ss1→ss2 |
