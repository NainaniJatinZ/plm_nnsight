# Contact Pattern Analysis: 2B61A

Generated: 2026-02-24 21:24:34   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2B61A |
| Contact pair | (182, 316) |
| ss1 | [177, 188) |
| ss2 | [311, 322) |
| Clean flank | 44 |
| Corrupt flank | 43 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.5738 |
| Corrupt metric | 0.0279 |
| Gap | 0.5459 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 250 | 81.59% |
| positive IE | 45 | 73.36% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L7 | H13 | +0.5055 |
| 2 | L11 | H1 | +0.4676 |
| 3 | L6 | H3 | +0.4633 |
| 4 | L10 | H9 | +0.3677 |
| 5 | L26 | H16 | +0.3608 |
| 6 | L22 | H14 | +0.2608 |
| 7 | L8 | H19 | +0.2333 |
| 8 | L32 | H13 | +0.2030 |
| 9 | L7 | H16 | +0.1690 |
| 10 | L6 | H19 | +0.1657 |
| 11 | L0 | H7 | +0.1641 |
| 12 | L32 | H18 | +0.1627 |
| 13 | L14 | H9 | +0.1421 |
| 14 | L5 | H19 | +0.1371 |
| 15 | L30 | H1 | +0.1371 |
| 16 | L6 | H17 | +0.1189 |
| 17 | L11 | H16 | +0.1118 |
| 18 | L0 | H6 | +0.1093 |
| 19 | L27 | H15 | +0.0991 |
| 20 | L19 | H0 | +0.0975 |
| 21 | L17 | H18 | +0.0870 |
| 22 | L14 | H14 | +0.0859 |
| 23 | L16 | H17 | +0.0858 |
| 24 | L15 | H2 | +0.0842 |
| 25 | L9 | H1 | +0.0800 |
| 26 | L6 | H8 | +0.0723 |
| 27 | L1 | H8 | +0.0649 |
| 28 | L1 | H13 | +0.0634 |
| 29 | L8 | H12 | +0.0629 |
| 30 | L13 | H8 | +0.0611 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.00% |
| 4 | 0.00% |
| 5 | 1.65% |
| 6 | 2.45% |
| 7 | 2.77% |
| 8 | 4.03% |
| 9 | 4.64% |
| 10 | 5.31% |
| 20 | 33.51% |
| 80 | 132.44% |
| 450 | 184.53% |

## Cell Attribution Analysis

Total cells: 6,028,033

- Positive: 3,039,497
- Negative: 2,985,530

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000063 | 602,804 |
| 95th | +0.00000184 | 301,402 |
| 99th | +0.00001258 | 60,281 |
| 99.5th | +0.00002692 | 30,141 |
| 99.9th | +0.00015030 | 6,029 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L6 | H3 | 315 | ss2 | 355 | flkR | +0.394994 | 0.056146 |
| L11 | H1 | 181 | ss1 | 163 | flkL | +0.327406 | 0.196450 |
| L6 | H19 | 315 | ss2 | 181 | ss1 | +0.231121 | 0.077537 |
| L10 | H9 | 181 | ss1 | 315 | ss2 | +0.199111 | 0.157788 |
| L8 | H19 | 315 | ss2 | 337 | flkR | +0.163015 | 0.143851 |
| L5 | H19 | 181 | ss1 | 159 | flkL | +0.153338 | 0.033627 |
| L7 | H13 | 181 | ss1 | 138 | flkL | +0.132787 | 0.128904 |
| L7 | H13 | 315 | ss2 | 315 | ss2 | +0.127407 | 0.112132 |
| L14 | H9 | 181 | ss1 | 315 | ss2 | +0.104314 | 0.172116 |
| L26 | H16 | 183 | ss1 | 316 | ss2 | +0.085819 | 0.570957 |
| L16 | H17 | 181 | ss1 | 163 | flkL | +0.078576 | 0.120911 |
| L14 | H14 | 181 | ss1 | 175 | flkL | +0.069808 | 0.125945 |
| L7 | H16 | 315 | ss2 | 344 | flkR | +0.066535 | 0.057710 |
| L9 | H1 | 157 | flkL | 163 | flkL | +0.063204 | 0.151168 |
| L15 | H2 | 181 | ss1 | 163 | flkL | +0.059650 | 0.103436 |
| L7 | H13 | 179 | ss1 | 179 | ss1 | +0.059647 | 0.142796 |
| L10 | H9 | 315 | ss2 | 315 | ss2 | +0.056093 | 0.236479 |
| L6 | H8 | 315 | ss2 | 326 | flkR | +0.054409 | 0.027104 |
| L19 | H0 | 183 | ss1 | 181 | ss1 | +0.051835 | 0.321009 |
| L14 | H13 | 181 | ss1 | 163 | flkL | +0.048266 | 0.111471 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L7 | H13 | 178 | ss1 | 130 | other | -0.013977 | 0.147592 |
| L9 | H1 | 180 | ss1 | 163 | flkL | -0.014534 | 0.150554 |
| L11 | H16 | 315 | ss2 | 163 | flkL | -0.015447 | 0.032875 |
| L7 | H13 | 180 | ss1 | 138 | flkL | -0.016429 | 0.186706 |
| L6 | H17 | 366 | other | 359 | flkR | -0.017156 | 0.121684 |
| L7 | H13 | 364 | flkR | 323 | flkR | -0.017605 | 0.155191 |
| L13 | H8 | 181 | ss1 | 315 | ss2 | -0.019712 | 0.175932 |
| L5 | H19 | 157 | flkL | 159 | flkL | -0.020630 | 0.031566 |
| L0 | H8 | 354 | flkR | 365 | flkR | -0.021178 | 0.006851 |
| L14 | H0 | 183 | ss1 | 163 | flkL | -0.021749 | 0.225827 |
| L7 | H13 | 158 | flkL | 158 | flkL | -0.022118 | 0.357405 |
| L6 | H17 | 366 | other | 350 | flkR | -0.022442 | 0.097228 |
| L6 | H17 | 181 | ss1 | 133 | flkL | -0.023076 | 0.021492 |
| L11 | H16 | 181 | ss1 | 163 | flkL | -0.023501 | 0.071389 |
| L5 | H19 | 163 | flkL | 159 | flkL | -0.025337 | 0.029410 |
| L6 | H17 | 132 | other | 180 | ss1 | -0.027340 | 0.150010 |
| L6 | H17 | 133 | flkL | 133 | flkL | -0.029138 | 0.293767 |
| L6 | H17 | 138 | flkL | 133 | flkL | -0.051407 | 0.303360 |
| L6 | H19 | 315 | ss2 | 157 | flkL | -0.074736 | 0.026551 |
| L7 | H13 | 181 | ss1 | 133 | flkL | -0.088765 | 0.100146 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0279 | 0.00% |
| 10 | 10 | 9 | 0.0308 | 0.54% |
| 20 | 20 | 17 | 0.0326 | 0.87% |
| 50 | 50 | 31 | 0.0419 | 2.57% |
| 100 | 100 | 42 | 0.0522 | 4.45% |
| 200 | 200 | 44 | 0.1330 | 19.25% |
| 500 | 500 | 45 | 0.2198 | 35.16% |
| 1000 | 1,000 | 45 | 0.3359 | 56.43% |
| 2000 | 2,000 | 45 | 0.4329 | 74.19% |
| 5000 | 5,000 | 45 | 0.5553 | 96.61% |
| 10000 | 10,000 | 45 | 0.6159 | 107.71% |
| 20000 | 20,000 | 45 | 0.6810 | 119.64% |
| 50000 | 50,000 | 45 | 0.7381 | 130.10% |

## Motif Analysis

### L0 H6 — Rank #18

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 27  |  total attr: +0.0890

**Key mass** (top-1=55%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 365 | flkR | +0.0490 | 55.0% |
| 133 | flkL | +0.0400 | 45.0% |

**Query mass** (top-1=14%, top-2=28%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | flkL | +0.0124 | 14.0% |
| 355 | flkR | +0.0123 | 13.8% |
| 354 | flkR | +0.0086 | 9.7% |
| 377 | other | +0.0071 | 8.0% |
| 341 | flkR | +0.0051 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +26 | 1 | 3.7% |
| -10 | 1 | 3.7% |
| -11 | 1 | 3.7% |
| +12 | 1 | 3.7% |
| -24 | 1 | 3.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 11 | 40.7% |
| flkR | flkR | 9 | 33.3% |
| other | flkR | 3 | 11.1% |
| ss2 | flkL | 1 | 3.7% |
| ss1 | flkL | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | flkL | 133 | flkL | +0.0124 | 0.0048 |
| 355 | flkR | 365 | flkR | +0.0123 | 0.0044 |
| 354 | flkR | 365 | flkR | +0.0086 | 0.0054 |
| 377 | other | 365 | flkR | +0.0071 | 0.0056 |
| 341 | flkR | 365 | flkR | +0.0051 | 0.0040 |

**Path patching connections:**

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | +0.0061 |
| L1H8 | #27 | k | +0.0036 |
| L5H19 | #14 | k | +0.0030 |
| L7H13 | #1 | k | +0.0024 |

### L0 H7 — Rank #11

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 56  |  total attr: +0.2028

**Key mass** (top-1=52%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 365 | flkR | +0.1064 | 52.5% |
| 133 | flkL | +0.0964 | 47.5% |

**Query mass** (top-1=12%, top-2=22%, top-3=29%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | flkL | +0.0235 | 11.6% |
| 377 | other | +0.0205 | 10.1% |
| 163 | flkL | +0.0147 | 7.2% |
| 357 | flkR | +0.0127 | 6.2% |
| 157 | flkL | +0.0103 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 7%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +12 | 2 | 3.6% |
| +11 | 2 | 3.6% |
| -2 | 2 | 3.6% |
| +26 | 1 | 1.8% |
| -8 | 1 | 1.8% |

**Region-pair profile** (q→k)  (top=32%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 18 | 32.1% |
| flkR | flkR | 12 | 21.4% |
| flkL | flkR | 11 | 19.6% |
| other | flkR | 5 | 8.9% |
| ss1 | flkR | 4 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 159 | flkL | 133 | flkL | +0.0214 | 0.0079 |
| 377 | other | 365 | flkR | +0.0186 | 0.0123 |
| 357 | flkR | 365 | flkR | +0.0127 | 0.0186 |
| 163 | flkL | 133 | flkL | +0.0113 | 0.0063 |
| 157 | flkL | 133 | flkL | +0.0074 | 0.0075 |

**Path patching connections:**

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | -0.0091 |
| L5H19 | #14 | k | +0.0088 |
| L1H8 | #27 | k | +0.0056 |
| L6H17 | #16 | q | -0.0034 |
| L1H8 | #27 | q | +0.0027 |

### L1 H8 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:flkR  |  cells: 29  |  total attr: +0.1072

**Key mass** (top-1=22%, top-2=35%, top-3=45%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 365 | flkR | +0.0239 | 22.3% |
| 364 | flkR | +0.0141 | 13.2% |
| 359 | flkR | +0.0099 | 9.2% |
| 179 | ss1 | +0.0088 | 8.2% |
| 133 | flkL | +0.0080 | 7.5% |

**Query mass** (top-1=22%, top-2=36%, top-3=47%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 361 | flkR | +0.0237 | 22.1% |
| 355 | flkR | +0.0145 | 13.5% |
| 362 | flkR | +0.0120 | 11.2% |
| 174 | flkL | +0.0088 | 8.2% |
| 326 | flkR | +0.0082 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 86%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 16 | 55.2% |
| -5 | 9 | 31.0% |
| -3 | 4 | 13.8% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 16 | 55.2% |
| flkL | flkL | 7 | 24.1% |
| other | flkL | 2 | 6.9% |
| flkL | ss1 | 1 | 3.4% |
| ss2 | ss2 | 1 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 361 | flkR | 364 | flkR | +0.0129 | 0.0618 |
| 362 | flkR | 365 | flkR | +0.0120 | 0.0412 |
| 361 | flkR | 365 | flkR | +0.0108 | 0.1696 |
| 355 | flkR | 359 | flkR | +0.0099 | 0.0137 |
| 174 | flkL | 179 | ss1 | +0.0088 | 0.0084 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L0H8 | #– | k | -0.0266 |
| L0H7 | #11 | k | +0.0056 |
| L0H6 | #18 | k | +0.0036 |
| L0H7 | #11 | q | +0.0027 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | +0.0091 |
| L7H13 | #1 | k | +0.0052 |
| L6H3 | #3 | q | -0.0027 |

### L1 H13 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 23  |  total attr: +0.1613

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 365 | flkR | +0.1563 | 96.9% |
| 377 | other | +0.0038 | 2.4% |
| 325 | flkR | +0.0012 | 0.7% |

**Query mass** (top-1=16%, top-2=31%, top-3=43%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 358 | flkR | +0.0253 | 15.7% |
| 315 | ss2 | +0.0240 | 14.9% |
| 355 | flkR | +0.0203 | 12.6% |
| 361 | flkR | +0.0176 | 10.9% |
| 359 | flkR | +0.0144 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -10 | 2 | 8.7% |
| -17 | 2 | 8.7% |
| -7 | 1 | 4.3% |
| -50 | 1 | 4.3% |
| -4 | 1 | 4.3% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=70%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 16 | 69.6% |
| ss2 | flkR | 4 | 17.4% |
| flkR | other | 1 | 4.3% |
| flkL | flkR | 1 | 4.3% |
| ss1 | flkR | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 358 | flkR | 365 | flkR | +0.0253 | 0.0854 |
| 315 | ss2 | 365 | flkR | +0.0229 | 0.0124 |
| 355 | flkR | 365 | flkR | +0.0203 | 0.0264 |
| 361 | flkR | 365 | flkR | +0.0176 | 0.0701 |
| 359 | flkR | 365 | flkR | +0.0144 | 0.0967 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L0H8 | #– | k | +0.0337 |
| L0H7 | #11 | k | +0.0023 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | +0.0139 |
| L6H3 | #3 | q | +0.0040 |
| L10H9 | #4 | k | -0.0040 |
| L6H8 | #26 | q | +0.0025 |
| L7H13 | #1 | q | +0.0022 |

### L5 H19 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.1825

**Key mass** (top-1=88%, top-2=92%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 159 | flkL | +0.1600 | 87.6% |
| 377 | other | +0.0079 | 4.3% |
| 368 | other | +0.0047 | 2.6% |
| 376 | other | +0.0044 | 2.4% |
| 347 | flkR | +0.0028 | 1.5% |

**Query mass** (top-1=84%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.1533 | 84.0% |
| 355 | flkR | +0.0168 | 9.2% |
| 315 | ss2 | +0.0041 | 2.3% |
| 158 | flkL | +0.0040 | 2.2% |
| 362 | flkR | +0.0016 | 0.9% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -15 | 2 | 18.2% |
| +22 | 1 | 9.1% |
| -22 | 1 | 9.1% |
| -13 | 1 | 9.1% |
| -21 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 5 | 45.5% |
| flkL | flkL | 3 | 27.3% |
| ss2 | flkR | 2 | 18.2% |
| ss1 | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 159 | flkL | +0.1533 | 0.0336 |
| 355 | flkR | 377 | other | +0.0063 | 0.0042 |
| 355 | flkR | 368 | other | +0.0047 | 0.0028 |
| 355 | flkR | 376 | other | +0.0044 | 0.0026 |
| 158 | flkL | 159 | flkL | +0.0040 | 0.0432 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L0H7 | #11 | k | +0.0088 |
| L0H8 | #– | k | +0.0055 |
| L0H6 | #18 | k | +0.0030 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L6H19 | #10 | k | +0.0516 |
| L7H13 | #1 | q | +0.0303 |
| L11H1 | #2 | q | +0.0239 |
| L7H0 | #– | k | +0.0232 |
| L8H12 | #29 | q | +0.0098 |

### L6 H3 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 22  |  total attr: +0.4475

**Key mass** (top-1=91%, top-2=92%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 355 | flkR | +0.4060 | 90.7% |
| 322 | flkR | +0.0049 | 1.1% |
| 365 | flkR | +0.0044 | 1.0% |
| 326 | flkR | +0.0040 | 0.9% |
| 133 | flkL | +0.0040 | 0.9% |

**Query mass** (top-1=96%, top-2=99%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.4286 | 95.8% |
| 157 | flkL | +0.0148 | 3.3% |
| 134 | flkL | +0.0016 | 0.4% |
| 344 | flkR | +0.0014 | 0.3% |
| 133 | flkL | +0.0012 | 0.3% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -19 | 2 | 9.1% |
| -40 | 1 | 4.5% |
| -198 | 1 | 4.5% |
| -7 | 1 | 4.5% |
| -11 | 1 | 4.5% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 9 | 40.9% |
| ss2 | flkL | 4 | 18.2% |
| flkL | flkL | 3 | 13.6% |
| flkL | flkR | 2 | 9.1% |
| ss2 | ss2 | 2 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 315 | ss2 | 355 | flkR | +0.3950 | 0.0561 |
| 157 | flkL | 355 | flkR | +0.0110 | 0.0108 |
| 315 | ss2 | 322 | flkR | +0.0049 | 0.0022 |
| 315 | ss2 | 326 | flkR | +0.0040 | 0.0020 |
| 315 | ss2 | 155 | flkL | +0.0028 | 0.0012 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L5H6 | #– | k | +0.0269 |
| L1H13 | #28 | k | +0.0139 |
| L1H8 | #27 | k | +0.0091 |
| L0H7 | #11 | k | -0.0091 |
| L0H6 | #18 | k | +0.0061 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.5687 |
| L8H12 | #29 | k | +0.0539 |
| L7H16 | #9 | q | +0.0390 |
| L8H19 | #7 | q | +0.0371 |
| L14H9 | #13 | k | +0.0289 |

### L6 H8 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 4  |  total attr: +0.0639

**Key mass** (top-1=85%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 326 | flkR | +0.0544 | 85.1% |
| 355 | flkR | +0.0082 | 12.8% |
| 353 | flkR | +0.0013 | 2.1% |

**Query mass** (top-1=85%, top-2=93%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.0544 | 85.1% |
| 344 | flkR | +0.0051 | 7.9% |
| 346 | flkR | +0.0045 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -11 | 2 | 50.0% |
| -9 | 2 | 50.0% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 3 | 75.0% |
| ss2 | flkR | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 315 | ss2 | 326 | flkR | +0.0544 | 0.0271 |
| 346 | flkR | 355 | flkR | +0.0045 | 0.0451 |
| 344 | flkR | 355 | flkR | +0.0037 | 0.0556 |
| 344 | flkR | 353 | flkR | +0.0013 | 0.0050 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L1H13 | #28 | q | +0.0025 |
| L5H6 | #– | k | +0.0021 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.0733 |
| L8H12 | #29 | k | +0.0085 |
| L8H19 | #7 | q | +0.0062 |
| L7H16 | #9 | k | +0.0060 |
| L14H9 | #13 | k | +0.0033 |

### L6 H17 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 96  |  total attr: +0.3645

**Key mass** (top-1=12%, top-2=21%, top-3=29%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | flkL | +0.0441 | 12.1% |
| 143 | flkL | +0.0321 | 8.8% |
| 361 | flkR | +0.0294 | 8.1% |
| 181 | ss1 | +0.0205 | 5.6% |
| 357 | flkR | +0.0135 | 3.7% |

**Query mass** (top-1=15%, top-2=24%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | flkL | +0.0544 | 14.9% |
| 181 | ss1 | +0.0349 | 9.6% |
| 361 | flkR | +0.0331 | 9.1% |
| 155 | flkL | +0.0226 | 6.2% |
| 157 | flkL | +0.0150 | 4.1% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 19 | 19.8% |
| -15 | 6 | 6.2% |
| +12 | 5 | 5.2% |
| +9 | 4 | 4.2% |
| +15 | 4 | 4.2% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 37 | 38.5% |
| flkL | flkL | 29 | 30.2% |
| flkL | other | 7 | 7.3% |
| ss1 | flkL | 5 | 5.2% |
| ss2 | ss2 | 4 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 138 | flkL | 138 | flkL | +0.0349 | 0.1932 |
| 361 | flkR | 361 | flkR | +0.0195 | 0.0640 |
| 155 | flkL | 143 | flkL | +0.0191 | 0.0462 |
| 181 | ss1 | 181 | ss1 | +0.0183 | 0.0323 |
| 133 | flkL | 149 | flkL | +0.0115 | 0.0550 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L0H8 | #– | k | -0.0086 |
| L5H19 | #14 | q | +0.0067 |
| L5H19 | #14 | k | +0.0058 |
| L0H7 | #11 | q | -0.0034 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L7H13 | #1 | k | +0.0532 |
| L7H13 | #1 | q | +0.0225 |
| L10H9 | #4 | k | -0.0040 |
| L11H1 | #2 | q | +0.0037 |
| L8H19 | #7 | q | +0.0031 |

### L6 H19 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 52  |  total attr: +0.3671

**Key mass** (top-1=97%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.3570 | 97.3% |
| 157 | flkL | +0.0073 | 2.0% |
| 163 | flkL | +0.0016 | 0.4% |
| 377 | other | +0.0012 | 0.3% |

**Query mass** (top-1=63%, top-2=65%, top-3=67%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.2311 | 63.0% |
| 179 | ss1 | +0.0075 | 2.1% |
| 310 | other | +0.0074 | 2.0% |
| 333 | flkR | +0.0067 | 1.8% |
| 362 | flkR | +0.0061 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -24 | 2 | 3.8% |
| +180 | 2 | 3.8% |
| +134 | 1 | 1.9% |
| -2 | 1 | 1.9% |
| +129 | 1 | 1.9% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss1 | 17 | 32.7% |
| flkL | ss1 | 14 | 26.9% |
| other | ss1 | 7 | 13.5% |
| ss1 | ss1 | 5 | 9.6% |
| ss2 | ss1 | 3 | 5.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 315 | ss2 | 181 | ss1 | +0.2311 | 0.0775 |
| 179 | ss1 | 181 | ss1 | +0.0075 | 0.0714 |
| 310 | other | 181 | ss1 | +0.0074 | 0.1080 |
| 333 | flkR | 181 | ss1 | +0.0067 | 0.0909 |
| 362 | flkR | 181 | ss1 | +0.0061 | 0.1625 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L5H19 | #14 | k | +0.0516 |
| L5H19 | #14 | q | +0.0040 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.0924 |
| L7H13 | #1 | k | +0.0436 |
| L7H13 | #1 | q | +0.0135 |
| L11H16 | #17 | k | -0.0131 |
| L7H16 | #9 | q | +0.0092 |

### L7 H13 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 81  |  total attr: +0.6897

**Key mass** (top-1=20%, top-2=38%, top-3=53%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | flkL | +0.1379 | 20.0% |
| 315 | ss2 | +0.1274 | 18.5% |
| 133 | flkL | +0.0988 | 14.3% |
| 179 | ss1 | +0.0596 | 8.6% |
| 180 | ss1 | +0.0264 | 3.8% |

**Query mass** (top-1=23%, top-2=43%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.1581 | 22.9% |
| 315 | ss2 | +0.1353 | 19.6% |
| 179 | ss1 | +0.0718 | 10.4% |
| 157 | flkL | +0.0667 | 9.7% |
| 180 | ss1 | +0.0331 | 4.8% |

**Offset distribution [frequency]** (top-2 coverage: 35%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 24 | 29.6% |
| +32 | 4 | 4.9% |
| +48 | 3 | 3.7% |
| +43 | 2 | 2.5% |
| +24 | 2 | 2.5% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 16 | 19.8% |
| flkR | flkR | 15 | 18.5% |
| ss1 | flkL | 9 | 11.1% |
| flkL | ss1 | 8 | 9.9% |
| flkR | ss2 | 7 | 8.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 138 | flkL | +0.1328 | 0.1289 |
| 315 | ss2 | 315 | ss2 | +0.1274 | 0.1121 |
| 179 | ss1 | 179 | ss1 | +0.0596 | 0.1428 |
| 157 | flkL | 133 | flkL | +0.0313 | 0.4917 |
| 158 | flkL | 133 | flkL | +0.0312 | 0.4567 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L6H17 | #16 | k | +0.0532 |
| L6H19 | #10 | k | +0.0436 |
| L5H19 | #14 | q | +0.0303 |
| L6H17 | #16 | q | +0.0225 |
| L6H19 | #10 | q | +0.0135 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.0925 |
| L8H19 | #7 | q | +0.0404 |
| L11H1 | #2 | q | +0.0393 |
| L9H2 | #– | q | +0.0225 |
| L11H16 | #17 | k | +0.0174 |

### L7 H16 — Rank #9

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 9  |  total attr: +0.1578

**Key mass** (top-1=42%, top-2=70%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 344 | flkR | +0.0665 | 42.2% |
| 181 | ss1 | +0.0446 | 28.3% |
| 346 | flkR | +0.0360 | 22.8% |
| 315 | ss2 | +0.0032 | 2.0% |
| 317 | ss2 | +0.0023 | 1.5% |

**Query mass** (top-1=72%, top-2=97%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.1131 | 71.7% |
| 157 | flkL | +0.0400 | 25.3% |
| 159 | flkL | +0.0046 | 2.9% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -29 | 1 | 11.1% |
| -24 | 1 | 11.1% |
| -31 | 1 | 11.1% |
| -22 | 1 | 11.1% |
| +0 | 1 | 11.1% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 4 | 44.4% |
| ss2 | ss2 | 3 | 33.3% |
| flkL | ss1 | 2 | 22.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 315 | ss2 | 344 | flkR | +0.0665 | 0.0577 |
| 157 | flkL | 181 | ss1 | +0.0400 | 0.0859 |
| 315 | ss2 | 346 | flkR | +0.0360 | 0.0402 |
| 159 | flkL | 181 | ss1 | +0.0046 | 0.1137 |
| 315 | ss2 | 315 | ss2 | +0.0032 | 0.0021 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | q | +0.0390 |
| L6H19 | #10 | q | +0.0092 |
| L6H19 | #10 | k | +0.0081 |
| L6H8 | #26 | k | +0.0060 |
| L5H19 | #14 | k | +0.0040 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.1208 |
| L8H19 | #7 | q | +0.0190 |
| L9H2 | #– | q | +0.0084 |
| L8H12 | #29 | k | +0.0077 |
| L14H9 | #13 | k | +0.0060 |

### L8 H12 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:flkL→ss2  |  cells: 9  |  total attr: +0.0631

**Key mass** (top-1=79%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.0496 | 78.7% |
| 157 | flkL | +0.0107 | 16.9% |
| -1 | other | +0.0016 | 2.6% |
| 316 | ss2 | +0.0011 | 1.8% |

**Query mass** (top-1=52%, top-2=84%, top-3=91%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | flkL | +0.0330 | 52.3% |
| 181 | ss1 | +0.0200 | 31.7% |
| 159 | flkL | +0.0045 | 7.1% |
| 315 | ss2 | +0.0026 | 4.1% |
| 160 | flkL | +0.0017 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +158 | 2 | 22.2% |
| -158 | 1 | 11.1% |
| -134 | 1 | 11.1% |
| +24 | 1 | 11.1% |
| -156 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 4 | 44.4% |
| ss1 | flkL | 2 | 22.2% |
| ss1 | ss2 | 1 | 11.1% |
| ss2 | flkL | 1 | 11.1% |
| flkL | other | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 157 | flkL | 315 | ss2 | +0.0303 | 0.0751 |
| 181 | ss1 | 315 | ss2 | +0.0132 | 0.0533 |
| 181 | ss1 | 157 | flkL | +0.0067 | 0.0338 |
| 159 | flkL | 315 | ss2 | +0.0045 | 0.0507 |
| 315 | ss2 | 157 | flkL | +0.0026 | 0.0019 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | +0.0539 |
| L5H19 | #14 | q | +0.0098 |
| L7H13 | #1 | q | -0.0093 |
| L6H8 | #26 | k | +0.0085 |
| L7H16 | #9 | k | +0.0077 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | q | +0.0090 |
| L11H1 | #2 | q | +0.0065 |
| L14H14 | #22 | q | +0.0051 |
| L9H1 | #25 | q | +0.0037 |
| L11H1 | #2 | k | -0.0035 |

### L8 H19 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss2→flkR  |  cells: 15  |  total attr: +0.1962

**Key mass** (top-1=83%, top-2=86%, top-3=88%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 337 | flkR | +0.1630 | 83.1% |
| 365 | flkR | +0.0049 | 2.5% |
| 312 | ss2 | +0.0044 | 2.2% |
| 314 | ss2 | +0.0036 | 1.9% |
| 341 | flkR | +0.0030 | 1.5% |

**Query mass** (top-1=95%, top-2=99%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.1873 | 95.5% |
| 332 | flkR | +0.0060 | 3.0% |
| 157 | flkL | +0.0018 | 0.9% |
| 335 | flkR | +0.0011 | 0.6% |

**Offset distribution [frequency]** (top-2 coverage: 27%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -33 | 2 | 13.3% |
| -30 | 2 | 13.3% |
| -22 | 1 | 6.7% |
| +3 | 1 | 6.7% |
| +1 | 1 | 6.7% |

**Region-pair profile** (q→k)  [ss2→flkR]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkR | 8 | 53.3% |
| ss2 | ss2 | 3 | 20.0% |
| flkR | flkR | 3 | 20.0% |
| flkL | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 315 | ss2 | 337 | flkR | +0.1630 | 0.1439 |
| 315 | ss2 | 312 | ss2 | +0.0044 | 0.0066 |
| 332 | flkR | 365 | flkR | +0.0038 | 0.0557 |
| 315 | ss2 | 314 | ss2 | +0.0036 | 0.0033 |
| 315 | ss2 | 341 | flkR | +0.0030 | 0.0047 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L7H13 | #1 | q | +0.0404 |
| L6H3 | #3 | q | +0.0371 |
| L7H16 | #9 | q | +0.0190 |
| L6H8 | #26 | q | +0.0062 |
| L6H19 | #10 | q | +0.0050 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.0987 |
| L9H2 | #– | q | +0.0080 |
| L14H9 | #13 | k | +0.0040 |
| L11H6 | #– | q | -0.0040 |
| L9H2 | #– | k | -0.0039 |

### L9 H1 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | INTRA:flkL  |  cells: 11  |  total attr: +0.1756

**Key mass** (top-1=84%, top-2=90%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | flkL | +0.1474 | 84.0% |
| 159 | flkL | +0.0112 | 6.4% |
| 164 | flkL | +0.0101 | 5.7% |
| 160 | flkL | +0.0058 | 3.3% |
| 315 | ss2 | +0.0011 | 0.7% |

**Query mass** (top-1=36%, top-2=68%, top-3=84%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | flkL | +0.0632 | 36.0% |
| 315 | ss2 | +0.0570 | 32.5% |
| 163 | flkL | +0.0273 | 15.5% |
| 181 | ss1 | +0.0132 | 7.5% |
| 159 | flkL | +0.0107 | 6.1% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 1 | 9.1% |
| +152 | 1 | 9.1% |
| +0 | 1 | 9.1% |
| +18 | 1 | 9.1% |
| -4 | 1 | 9.1% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 45.5% |
| ss2 | flkL | 4 | 36.4% |
| ss1 | flkL | 1 | 9.1% |
| ss1 | ss2 | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 157 | flkL | 163 | flkL | +0.0632 | 0.1512 |
| 315 | ss2 | 163 | flkL | +0.0311 | 0.0175 |
| 163 | flkL | 163 | flkL | +0.0262 | 0.0805 |
| 181 | ss1 | 163 | flkL | +0.0132 | 0.0960 |
| 159 | flkL | 163 | flkL | +0.0107 | 0.1534 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | q | +0.0159 |
| L6H19 | #10 | q | +0.0055 |
| L5H19 | #14 | k | +0.0041 |
| L7H16 | #9 | q | +0.0038 |
| L8H12 | #29 | q | +0.0037 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.0157 |
| L11H1 | #2 | k | +0.0115 |
| L11H16 | #17 | k | +0.0092 |
| L10H9 | #4 | q | -0.0066 |
| L11H1 | #2 | q | +0.0039 |

### L10 H9 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 21  |  total attr: +0.3603

**Key mass** (top-1=95%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.3422 | 95.0% |
| -1 | other | +0.0181 | 5.0% |

**Query mass** (top-1=56%, top-2=75%, top-3=81%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.2011 | 55.8% |
| 315 | ss2 | +0.0674 | 18.7% |
| 157 | flkL | +0.0241 | 6.7% |
| 159 | flkL | +0.0156 | 4.3% |
| 163 | flkL | +0.0091 | 2.5% |

**Offset distribution [frequency]** (top-2 coverage: 10%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -134 | 1 | 4.8% |
| +0 | 1 | 4.8% |
| -158 | 1 | 4.8% |
| -156 | 1 | 4.8% |
| +316 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 7 | 33.3% |
| ss1 | ss2 | 4 | 19.0% |
| ss2 | ss2 | 3 | 14.3% |
| other | ss2 | 2 | 9.5% |
| ss2 | other | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 315 | ss2 | +0.1991 | 0.1578 |
| 315 | ss2 | 315 | ss2 | +0.0561 | 0.2365 |
| 157 | flkL | 315 | ss2 | +0.0241 | 0.1132 |
| 159 | flkL | 315 | ss2 | +0.0156 | 0.1151 |
| 315 | ss2 | -1 | other | +0.0113 | 0.0808 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | +0.5687 |
| L7H16 | #9 | k | +0.1208 |
| L8H19 | #7 | k | +0.0987 |
| L7H13 | #1 | k | +0.0925 |
| L6H19 | #10 | k | +0.0924 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L11H1 | #2 | q | +0.0831 |
| L11H1 | #2 | k | +0.0363 |
| L11H16 | #17 | k | -0.0194 |
| L14H9 | #13 | k | +0.0125 |
| L12H3 | #– | k | +0.0115 |

### L11 H1 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 17  |  total attr: +0.3915

**Key mass** (top-1=86%, top-2=91%, top-3=92%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | flkL | +0.3376 | 86.2% |
| 159 | flkL | +0.0172 | 4.4% |
| 164 | flkL | +0.0069 | 1.8% |
| 145 | flkL | +0.0055 | 1.4% |
| 138 | flkL | +0.0043 | 1.1% |

**Query mass** (top-1=96%, top-2=99%, top-3=99%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.3773 | 96.4% |
| 167 | flkL | +0.0090 | 2.3% |
| 170 | flkL | +0.0018 | 0.5% |
| 177 | ss1 | +0.0012 | 0.3% |
| 315 | ss2 | +0.0012 | 0.3% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 5.9% |
| +22 | 1 | 5.9% |
| +4 | 1 | 5.9% |
| +17 | 1 | 5.9% |
| +36 | 1 | 5.9% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 12 | 70.6% |
| flkL | flkL | 2 | 11.8% |
| ss1 | ss1 | 1 | 5.9% |
| ss2 | flkL | 1 | 5.9% |
| ss2 | flkR | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 163 | flkL | +0.3274 | 0.1964 |
| 181 | ss1 | 159 | flkL | +0.0172 | 0.0187 |
| 167 | flkL | 163 | flkL | +0.0090 | 0.2423 |
| 181 | ss1 | 164 | flkL | +0.0069 | 0.0134 |
| 181 | ss1 | 145 | flkL | +0.0055 | 0.0149 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | q | +0.0831 |
| L7H13 | #1 | q | +0.0393 |
| L10H9 | #4 | k | +0.0363 |
| L5H19 | #14 | q | +0.0239 |
| L9H1 | #25 | k | +0.0115 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L15H2 | #24 | q | +0.0372 |
| L14H9 | #13 | q | +0.0264 |
| L19H0 | #20 | k | +0.0137 |
| L16H15 | #– | q | +0.0115 |
| L17H18 | #21 | q | +0.0113 |

### L11 H16 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 36  |  total attr: +0.1317

**Key mass** (top-1=54%, top-2=78%, top-3=92%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | flkL | +0.0713 | 54.2% |
| 315 | ss2 | +0.0310 | 23.5% |
| 159 | flkL | +0.0182 | 13.8% |
| 339 | flkR | +0.0066 | 5.0% |
| 181 | ss1 | +0.0034 | 2.6% |

**Query mass** (top-1=33%, top-2=40%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.0436 | 33.1% |
| 310 | other | +0.0095 | 7.2% |
| 186 | ss1 | +0.0065 | 5.0% |
| 167 | flkL | +0.0065 | 5.0% |
| 170 | flkL | +0.0062 | 4.7% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 5.6% |
| -6 | 2 | 5.6% |
| +156 | 1 | 2.8% |
| +29 | 1 | 2.8% |
| +13 | 1 | 2.8% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 11 | 30.6% |
| ss1 | flkL | 6 | 16.7% |
| ss2 | flkL | 4 | 11.1% |
| flkL | flkL | 4 | 11.1% |
| flkL | ss2 | 3 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 315 | ss2 | 315 | ss2 | +0.0189 | 0.1149 |
| 315 | ss2 | 159 | flkL | +0.0182 | 0.0315 |
| 186 | ss1 | 157 | flkL | +0.0065 | 0.1444 |
| 170 | flkL | 157 | flkL | +0.0062 | 0.1279 |
| 312 | ss2 | 157 | flkL | +0.0060 | 0.1489 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | -0.0194 |
| L7H13 | #1 | k | +0.0174 |
| L6H3 | #3 | q | +0.0168 |
| L6H19 | #10 | k | -0.0131 |
| L9H1 | #25 | k | +0.0092 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L12H3 | #– | q | +0.0085 |
| L14H13 | #– | k | +0.0053 |
| L15H2 | #24 | q | -0.0045 |
| L14H14 | #22 | q | -0.0044 |
| L15H2 | #24 | k | -0.0040 |

### L13 H8 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkL→ss2  |  cells: 18  |  total attr: +0.0843

**Key mass** (top-1=91%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.0769 | 91.2% |
| 377 | other | +0.0057 | 6.8% |
| 376 | other | +0.0017 | 2.0% |

**Query mass** (top-1=43%, top-2=52%, top-3=61%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | flkL | +0.0365 | 43.3% |
| 178 | ss1 | +0.0077 | 9.1% |
| 181 | ss1 | +0.0074 | 8.8% |
| 180 | ss1 | +0.0044 | 5.3% |
| 157 | flkL | +0.0043 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -152 | 1 | 5.6% |
| -137 | 1 | 5.6% |
| -196 | 1 | 5.6% |
| -135 | 1 | 5.6% |
| -158 | 1 | 5.6% |

**Region-pair profile** (q→k)  [CROSS:flkL→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss2 | 8 | 44.4% |
| ss1 | ss2 | 5 | 27.8% |
| other | ss2 | 3 | 16.7% |
| ss1 | other | 2 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 163 | flkL | 315 | ss2 | +0.0365 | 0.1975 |
| 178 | ss1 | 315 | ss2 | +0.0077 | 0.0944 |
| 181 | ss1 | 377 | other | +0.0057 | 0.0321 |
| 180 | ss1 | 315 | ss2 | +0.0044 | 0.1409 |
| 157 | flkL | 315 | ss2 | +0.0043 | 0.1915 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L10H9 | #4 | k | +0.0075 |
| L6H3 | #3 | k | +0.0057 |
| L11H6 | #– | k | +0.0042 |
| L7H16 | #9 | k | +0.0036 |
| L8H19 | #7 | k | +0.0029 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L15H2 | #24 | k | +0.0106 |
| L14H9 | #13 | q | -0.0054 |
| L16H7 | #– | k | +0.0052 |
| L22H14 | #6 | k | -0.0045 |
| L15H2 | #24 | q | +0.0042 |

### L14 H9 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 32  |  total attr: +0.2168

**Key mass** (top-1=69%, top-2=80%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.1499 | 69.2% |
| 157 | flkL | +0.0236 | 10.9% |
| 163 | flkL | +0.0193 | 8.9% |
| 159 | flkL | +0.0100 | 4.6% |
| 181 | ss1 | +0.0097 | 4.5% |

**Query mass** (top-1=63%, top-2=70%, top-3=76%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.1367 | 63.0% |
| 315 | ss2 | +0.0146 | 6.8% |
| 183 | ss1 | +0.0143 | 6.6% |
| 313 | ss2 | +0.0128 | 5.9% |
| 180 | ss1 | +0.0058 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +24 | 2 | 6.2% |
| +0 | 2 | 6.2% |
| +2 | 2 | 6.2% |
| -134 | 1 | 3.1% |
| -2 | 1 | 3.1% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 9 | 28.1% |
| ss2 | ss2 | 6 | 18.8% |
| ss2 | flkL | 4 | 12.5% |
| ss1 | ss2 | 3 | 9.4% |
| flkL | ss2 | 3 | 9.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 315 | ss2 | +0.1043 | 0.1721 |
| 181 | ss1 | 157 | flkL | +0.0169 | 0.0152 |
| 313 | ss2 | 315 | ss2 | +0.0096 | 0.2365 |
| 181 | ss1 | 163 | flkL | +0.0080 | 0.0106 |
| 166 | flkL | 315 | ss2 | +0.0055 | 0.2899 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L6H3 | #3 | k | +0.0289 |
| L11H1 | #2 | q | +0.0264 |
| L10H9 | #4 | k | +0.0125 |
| L7H16 | #9 | k | +0.0060 |
| L13H8 | #30 | q | -0.0054 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L15H2 | #24 | k | +0.0133 |
| L32H18 | #12 | k | +0.0132 |
| L17H18 | #21 | q | +0.0112 |
| L26H16 | #5 | q | +0.0067 |
| L16H15 | #– | q | +0.0052 |

### L14 H14 — Rank #22

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 18  |  total attr: +0.1255

**Key mass** (top-1=60%, top-2=68%, top-3=76%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 175 | flkL | +0.0749 | 59.7% |
| 157 | flkL | +0.0101 | 8.0% |
| 159 | flkL | +0.0100 | 8.0% |
| 181 | ss1 | +0.0093 | 7.4% |
| 183 | ss1 | +0.0058 | 4.7% |

**Query mass** (top-1=60%, top-2=76%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.0757 | 60.3% |
| 163 | flkL | +0.0198 | 15.8% |
| 183 | ss1 | +0.0051 | 4.1% |
| 186 | ss1 | +0.0044 | 3.5% |
| 187 | ss1 | +0.0034 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 5 | 27.8% |
| +5 | 4 | 22.2% |
| +7 | 2 | 11.1% |
| +4 | 1 | 5.6% |
| -2 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 27.8% |
| ss1 | flkL | 4 | 22.2% |
| ss1 | ss1 | 3 | 16.7% |
| flkR | ss2 | 1 | 5.6% |
| ss2 | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 175 | flkL | +0.0698 | 0.1259 |
| 163 | flkL | 159 | flkL | +0.0100 | 0.0644 |
| 163 | flkL | 157 | flkL | +0.0083 | 0.0981 |
| 181 | ss1 | 183 | ss1 | +0.0058 | 0.0695 |
| 183 | ss1 | 175 | flkL | +0.0051 | 0.0343 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L11H1 | #2 | k | -0.0105 |
| L8H12 | #29 | q | +0.0051 |
| L13H18 | #– | k | -0.0050 |
| L11H16 | #17 | q | -0.0044 |
| L11H1 | #2 | q | -0.0041 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L15H2 | #24 | q | +0.0072 |
| L16H15 | #– | q | +0.0040 |
| L17H18 | #21 | q | +0.0031 |
| L19H0 | #20 | k | +0.0027 |
| L16H17 | #23 | q | -0.0021 |

### L15 H2 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR  |  cells: 19  |  total attr: +0.1140

**Key mass** (top-1=93%, top-2=98%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | flkL | +0.1061 | 93.1% |
| 159 | flkL | +0.0057 | 5.0% |
| 172 | flkL | +0.0011 | 0.9% |
| 315 | ss2 | +0.0011 | 0.9% |

**Query mass** (top-1=56%, top-2=71%, top-3=77%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.0640 | 56.2% |
| 183 | ss1 | +0.0171 | 15.0% |
| 182 | ss1 | +0.0064 | 5.6% |
| 314 | ss2 | +0.0052 | 4.6% |
| 151 | flkL | +0.0043 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 5.3% |
| +20 | 1 | 5.3% |
| +19 | 1 | 5.3% |
| +151 | 1 | 5.3% |
| -12 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=37%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 7 | 36.8% |
| other | flkL | 6 | 31.6% |
| flkL | flkL | 3 | 15.8% |
| ss2 | flkL | 1 | 5.3% |
| flkR | flkL | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 163 | flkL | +0.0596 | 0.1034 |
| 183 | ss1 | 163 | flkL | +0.0146 | 0.0922 |
| 182 | ss1 | 163 | flkL | +0.0064 | 0.2015 |
| 314 | ss2 | 163 | flkL | +0.0052 | 0.1724 |
| 151 | flkL | 163 | flkL | +0.0043 | 0.2073 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L11H1 | #2 | q | +0.0372 |
| L14H9 | #13 | k | +0.0133 |
| L14H13 | #– | q | +0.0131 |
| L10H9 | #4 | q | +0.0106 |
| L13H8 | #30 | k | +0.0106 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L16H17 | #23 | k | +0.0063 |
| L16H7 | #– | k | +0.0043 |
| L17H18 | #21 | k | +0.0041 |
| L19H0 | #20 | k | +0.0033 |
| L26H16 | #5 | q | +0.0031 |

### L16 H17 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 16  |  total attr: +0.1156

**Key mass** (top-1=77%, top-2=81%, top-3=85%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 163 | flkL | +0.0887 | 76.8% |
| 322 | flkR | +0.0047 | 4.1% |
| 318 | ss2 | +0.0044 | 3.8% |
| 320 | ss2 | +0.0037 | 3.2% |
| 170 | flkL | +0.0034 | 2.9% |

**Query mass** (top-1=88%, top-2=94%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.1021 | 88.3% |
| 185 | ss1 | +0.0063 | 5.4% |
| 184 | ss1 | +0.0021 | 1.8% |
| 163 | flkL | +0.0020 | 1.7% |
| 159 | flkL | +0.0018 | 1.5% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 1 | 6.2% |
| +22 | 1 | 6.2% |
| -141 | 1 | 6.2% |
| -137 | 1 | 6.2% |
| -139 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 25.0% |
| ss1 | flkL | 3 | 18.8% |
| flkL | flkL | 3 | 18.8% |
| ss1 | other | 3 | 18.8% |
| ss1 | flkR | 2 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 163 | flkL | +0.0786 | 0.1209 |
| 185 | ss1 | 163 | flkL | +0.0063 | 0.0520 |
| 181 | ss1 | 322 | flkR | +0.0047 | 0.0079 |
| 181 | ss1 | 318 | ss2 | +0.0044 | 0.0111 |
| 181 | ss1 | 320 | ss2 | +0.0037 | 0.0118 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L11H1 | #2 | q | -0.0065 |
| L15H2 | #24 | k | +0.0063 |
| L10H9 | #4 | k | -0.0035 |
| L14H9 | #13 | k | -0.0033 |
| L14H9 | #13 | q | -0.0027 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L19H15 | #– | k | -0.0047 |
| L17H18 | #21 | k | -0.0044 |
| L19H0 | #20 | k | +0.0041 |
| L32H13 | #8 | k | -0.0026 |
| L22H14 | #6 | k | +0.0022 |

### L17 H18 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | ss1→flkL  |  cells: 15  |  total attr: +0.0585

**Key mass** (top-1=49%, top-2=71%, top-3=81%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 157 | flkL | +0.0286 | 48.9% |
| 183 | ss1 | +0.0131 | 22.4% |
| 163 | flkL | +0.0054 | 9.3% |
| 181 | ss1 | +0.0031 | 5.3% |
| 155 | flkL | +0.0019 | 3.2% |

**Query mass** (top-1=51%, top-2=70%, top-3=76%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.0296 | 50.6% |
| 316 | ss2 | +0.0116 | 19.8% |
| 183 | ss1 | +0.0036 | 6.1% |
| 317 | ss2 | +0.0033 | 5.7% |
| 185 | ss1 | +0.0032 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 4 | 26.7% |
| +24 | 2 | 13.3% |
| +134 | 2 | 13.3% |
| +26 | 1 | 6.7% |
| +28 | 1 | 6.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 9 | 60.0% |
| ss2 | ss1 | 6 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 181 | ss1 | 157 | flkL | +0.0264 | 0.2406 |
| 316 | ss2 | 183 | ss1 | +0.0116 | 0.0855 |
| 183 | ss1 | 157 | flkL | +0.0022 | 0.0690 |
| 179 | ss1 | 155 | flkL | +0.0019 | 0.1664 |
| 181 | ss1 | 153 | flkL | +0.0019 | 0.0368 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L11H1 | #2 | q | +0.0113 |
| L14H9 | #13 | q | +0.0112 |
| L16H17 | #23 | k | -0.0044 |
| L15H2 | #24 | k | +0.0041 |
| L13H8 | #30 | k | -0.0034 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L19H0 | #20 | k | +0.0044 |
| L26H16 | #5 | q | +0.0033 |
| L22H14 | #6 | q | +0.0028 |
| L32H13 | #8 | q | -0.0021 |

### L19 H0 — Rank #20

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 17  |  total attr: +0.1015

**Key mass** (top-1=51%, top-2=59%, top-3=66%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.0518 | 51.1% |
| 315 | ss2 | +0.0078 | 7.7% |
| 175 | flkL | +0.0072 | 7.1% |
| 176 | flkL | +0.0053 | 5.2% |
| 170 | flkL | +0.0046 | 4.6% |

**Query mass** (top-1=63%, top-2=75%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss1 | +0.0644 | 63.4% |
| 316 | ss2 | +0.0118 | 11.7% |
| 178 | ss1 | +0.0046 | 4.6% |
| 185 | ss1 | +0.0044 | 4.3% |
| 182 | ss1 | +0.0037 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 65%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 6 | 35.3% |
| +7 | 5 | 29.4% |
| +8 | 4 | 23.5% |
| +1 | 1 | 5.9% |
| +20 | 1 | 5.9% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 29.4% |
| ss1 | flkL | 4 | 23.5% |
| ss2 | ss2 | 3 | 17.6% |
| flkL | flkL | 2 | 11.8% |
| ss2 | other | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss1 | 181 | ss1 | +0.0518 | 0.3210 |
| 316 | ss2 | 315 | ss2 | +0.0078 | 0.2211 |
| 183 | ss1 | 175 | flkL | +0.0072 | 0.1277 |
| 183 | ss1 | 176 | flkL | +0.0053 | 0.1099 |
| 178 | ss1 | 170 | flkL | +0.0046 | 0.0619 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L11H1 | #2 | k | +0.0137 |
| L16H15 | #– | k | +0.0055 |
| L14H13 | #– | k | +0.0050 |
| L17H18 | #21 | k | +0.0044 |
| L16H17 | #23 | k | +0.0041 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L22H14 | #6 | k | +0.0132 |
| L26H16 | #5 | q | +0.0088 |
| L22H14 | #6 | q | +0.0065 |
| L30H1 | #15 | k | -0.0054 |
| L27H15 | #19 | q | -0.0051 |

### L22 H14 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 17  |  total attr: +0.1569

**Key mass** (top-1=28%, top-2=49%, top-3=62%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss1 | +0.0444 | 28.3% |
| 184 | ss1 | +0.0326 | 20.8% |
| 181 | ss1 | +0.0209 | 13.3% |
| 185 | ss1 | +0.0175 | 11.2% |
| 180 | ss1 | +0.0124 | 7.9% |

**Query mass** (top-1=27%, top-2=51%, top-3=65%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 316 | ss2 | +0.0425 | 27.1% |
| 317 | ss2 | +0.0370 | 23.6% |
| 314 | ss2 | +0.0229 | 14.6% |
| 313 | ss2 | +0.0165 | 10.5% |
| 180 | ss1 | +0.0145 | 9.2% |

**Offset distribution [frequency]** (top-2 coverage: 47%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 5 | 29.4% |
| +135 | 3 | 17.6% |
| +134 | 2 | 11.8% |
| +131 | 2 | 11.8% |
| +26 | 2 | 11.8% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=71%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 12 | 70.6% |
| ss1 | flkL | 4 | 23.5% |
| flkL | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 316 | ss2 | 183 | ss1 | +0.0425 | 0.2350 |
| 317 | ss2 | 184 | ss1 | +0.0311 | 0.2561 |
| 314 | ss2 | 181 | ss1 | +0.0196 | 0.3643 |
| 319 | ss2 | 185 | ss1 | +0.0129 | 0.2825 |
| 180 | ss1 | 156 | flkL | +0.0122 | 0.3572 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L19H0 | #20 | k | +0.0132 |
| L11H1 | #2 | k | +0.0113 |
| L14H13 | #– | k | +0.0065 |
| L19H0 | #20 | q | +0.0065 |
| L13H8 | #30 | k | -0.0045 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L26H16 | #5 | k | +0.0051 |
| L32H18 | #12 | k | +0.0050 |
| L32H18 | #12 | q | +0.0046 |
| L32H13 | #8 | k | +0.0039 |
| L27H15 | #19 | q | +0.0039 |

### L26 H16 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 18  |  total attr: +0.2315

**Key mass** (top-1=37%, top-2=56%, top-3=68%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 316 | ss2 | +0.0858 | 37.1% |
| 314 | ss2 | +0.0442 | 19.1% |
| 313 | ss2 | +0.0278 | 12.0% |
| 317 | ss2 | +0.0269 | 11.6% |
| 344 | flkR | +0.0187 | 8.1% |

**Query mass** (top-1=37%, top-2=55%, top-3=68%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | ss1 | +0.0858 | 37.1% |
| 181 | ss1 | +0.0413 | 17.8% |
| 180 | ss1 | +0.0303 | 13.1% |
| 184 | ss1 | +0.0269 | 11.6% |
| 314 | ss2 | +0.0262 | 11.3% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -133 | 4 | 22.2% |
| -30 | 4 | 22.2% |
| -32 | 2 | 11.1% |
| -24 | 1 | 5.6% |
| +0 | 1 | 5.6% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 33.3% |
| ss2 | flkR | 6 | 33.3% |
| flkL | ss1 | 2 | 11.1% |
| ss2 | ss2 | 1 | 5.6% |
| other | flkR | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | ss1 | 316 | ss2 | +0.0858 | 0.5710 |
| 181 | ss1 | 314 | ss2 | +0.0413 | 0.4882 |
| 180 | ss1 | 313 | ss2 | +0.0278 | 0.1981 |
| 184 | ss1 | 317 | ss2 | +0.0269 | 0.2707 |
| 314 | ss2 | 344 | flkR | +0.0187 | 0.4420 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L16H7 | #– | k | -0.0115 |
| L19H0 | #20 | q | +0.0088 |
| L11H1 | #2 | q | +0.0078 |
| L14H9 | #13 | q | +0.0067 |
| L14H0 | #– | q | -0.0067 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L32H13 | #8 | q | +0.0078 |
| L32H18 | #12 | k | +0.0075 |
| L30H1 | #15 | k | +0.0053 |
| L32H13 | #8 | k | +0.0028 |
| L30H1 | #15 | q | +0.0022 |

### L27 H15 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 15  |  total attr: +0.0744

**Key mass** (top-1=25%, top-2=44%, top-3=64%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | ss1 | +0.0183 | 24.6% |
| 333 | flkR | +0.0148 | 19.9% |
| 156 | flkL | +0.0143 | 19.2% |
| 183 | ss1 | +0.0080 | 10.8% |
| 181 | ss1 | +0.0061 | 8.2% |

**Query mass** (top-1=27%, top-2=49%, top-3=64%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 314 | ss2 | +0.0201 | 27.1% |
| 313 | ss2 | +0.0164 | 22.0% |
| 180 | ss1 | +0.0113 | 15.2% |
| 316 | ss2 | +0.0081 | 10.9% |
| 317 | ss2 | +0.0049 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 4 | 26.7% |
| +24 | 2 | 13.3% |
| +131 | 2 | 13.3% |
| -19 | 1 | 6.7% |
| -33 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 46.7% |
| ss2 | flkR | 3 | 20.0% |
| ss1 | flkL | 3 | 20.0% |
| flkR | ss2 | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 313 | ss2 | 180 | ss1 | +0.0164 | 0.1117 |
| 314 | ss2 | 333 | flkR | +0.0125 | 0.2367 |
| 180 | ss1 | 156 | flkL | +0.0113 | 0.3088 |
| 316 | ss2 | 183 | ss1 | +0.0059 | 0.0337 |
| 317 | ss2 | 184 | ss1 | +0.0049 | 0.0356 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L19H0 | #20 | q | -0.0051 |
| L6H3 | #3 | k | -0.0043 |
| L22H14 | #6 | q | +0.0039 |
| L14H0 | #– | k | -0.0034 |
| L19H0 | #20 | k | +0.0032 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L32H13 | #8 | q | +0.0091 |
| L32H18 | #12 | k | +0.0046 |
| L30H1 | #15 | k | -0.0046 |
| L32H13 | #8 | k | +0.0042 |
| L32H18 | #12 | q | +0.0038 |

### L30 H1 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS_SSE | CROSS:ss1→ss2  |  cells: 12  |  total attr: +0.0659

**Key mass** (top-1=31%, top-2=58%, top-3=74%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 315 | ss2 | +0.0203 | 30.8% |
| 313 | ss2 | +0.0180 | 27.2% |
| 181 | ss1 | +0.0107 | 16.2% |
| 183 | ss1 | +0.0063 | 9.5% |
| 317 | ss2 | +0.0037 | 5.7% |

**Query mass** (top-1=38%, top-2=57%, top-3=71%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | ss1 | +0.0253 | 38.4% |
| 314 | ss2 | +0.0125 | 18.9% |
| 182 | ss1 | +0.0088 | 13.4% |
| 316 | ss2 | +0.0063 | 9.5% |
| 312 | ss2 | +0.0042 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -133 | 4 | 33.3% |
| +133 | 2 | 16.7% |
| -1 | 2 | 16.7% |
| -135 | 1 | 8.3% |
| -30 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 41.7% |
| ss2 | ss1 | 3 | 25.0% |
| ss2 | ss2 | 3 | 25.0% |
| ss2 | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 180 | ss1 | 313 | ss2 | +0.0149 | 0.0861 |
| 180 | ss1 | 315 | ss2 | +0.0104 | 0.1935 |
| 314 | ss2 | 181 | ss1 | +0.0095 | 0.0894 |
| 182 | ss1 | 315 | ss2 | +0.0088 | 0.7301 |
| 316 | ss2 | 183 | ss1 | +0.0063 | 0.0382 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L19H0 | #20 | k | -0.0054 |
| L26H16 | #5 | k | +0.0053 |
| L27H15 | #19 | k | -0.0046 |
| L11H1 | #2 | k | +0.0037 |
| L10H9 | #4 | k | +0.0032 |

Sends to:

| dst | rank | channel | effect |
|-----|------|---------|--------|
| L32H13 | #8 | q | +0.0026 |
| L32H13 | #8 | k | +0.0022 |

### L32 H13 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 13  |  total attr: +0.1089

**Key mass** (top-1=24%, top-2=42%, top-3=58%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.0259 | 23.7% |
| 180 | ss1 | +0.0201 | 18.5% |
| 314 | ss2 | +0.0176 | 16.2% |
| 183 | ss1 | +0.0120 | 11.1% |
| 313 | ss2 | +0.0114 | 10.5% |

**Query mass** (top-1=20%, top-2=37%, top-3=55%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | ss1 | +0.0214 | 19.6% |
| 180 | ss1 | +0.0193 | 17.7% |
| 313 | ss2 | +0.0189 | 17.4% |
| 312 | ss2 | +0.0170 | 15.6% |
| 316 | ss2 | +0.0120 | 11.1% |

**Offset distribution [frequency]** (top-2 coverage: 46%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 3 | 23.1% |
| -133 | 3 | 23.1% |
| -135 | 2 | 15.4% |
| -131 | 2 | 15.4% |
| +135 | 2 | 15.4% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 53.8% |
| ss2 | ss1 | 6 | 46.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 313 | ss2 | 180 | ss1 | +0.0189 | 0.0821 |
| 312 | ss2 | 181 | ss1 | +0.0170 | 0.1564 |
| 181 | ss1 | 314 | ss2 | +0.0163 | 0.1102 |
| 316 | ss2 | 183 | ss1 | +0.0120 | 0.0515 |
| 180 | ss1 | 313 | ss2 | +0.0114 | 0.0495 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L27H15 | #19 | q | +0.0091 |
| L26H16 | #5 | q | +0.0078 |
| L27H15 | #19 | k | +0.0042 |
| L11H1 | #2 | q | +0.0041 |
| L22H14 | #6 | k | +0.0039 |

### L32 H18 — Rank #12

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS_SSE | CROSS:ss2→ss1  |  cells: 12  |  total attr: +0.0804

**Key mass** (top-1=57%, top-2=82%, top-3=88%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 180 | ss1 | +0.0461 | 57.4% |
| 181 | ss1 | +0.0201 | 25.0% |
| 314 | ss2 | +0.0045 | 5.6% |
| 316 | ss2 | +0.0022 | 2.7% |
| 183 | ss1 | +0.0019 | 2.4% |

**Query mass** (top-1=54%, top-2=70%, top-3=79%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 313 | ss2 | +0.0438 | 54.4% |
| 314 | ss2 | +0.0125 | 15.5% |
| 312 | ss2 | +0.0076 | 9.5% |
| 181 | ss1 | +0.0047 | 5.9% |
| 180 | ss1 | +0.0032 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +133 | 3 | 25.0% |
| -133 | 3 | 25.0% |
| +135 | 2 | 16.7% |
| +131 | 1 | 8.3% |
| -135 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 50.0% |
| ss1 | ss2 | 6 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 313 | ss2 | 180 | ss1 | +0.0438 | 0.1157 |
| 314 | ss2 | 181 | ss1 | +0.0125 | 0.0514 |
| 312 | ss2 | 181 | ss1 | +0.0076 | 0.0427 |
| 181 | ss1 | 314 | ss2 | +0.0034 | 0.0140 |
| 315 | ss2 | 180 | ss1 | +0.0024 | 0.0247 |

**Path patching connections:**

Receives from:

| src | rank | channel | effect |
|-----|------|---------|--------|
| L14H9 | #13 | k | +0.0132 |
| L26H16 | #5 | k | +0.0075 |
| L14H13 | #– | k | +0.0051 |
| L22H14 | #6 | k | +0.0050 |
| L27H15 | #19 | k | +0.0046 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #18 | L0 | H6 | 27 | +0.0890 | DUAL-ANCHOR | F365/I133 | DISTRIBUTED |  |  | INTRA:flkL |
| #11 | L0 | H7 | 56 | +0.2028 | DUAL-ANCHOR | F365/I133 | DISTRIBUTED |  |  |  |
| #27 | L1 | H8 | 29 | +0.1072 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL | INTRA:flkR |
| #28 | L1 | H13 | 23 | +0.1613 | SINGLE-ANCHOR | F365 | DISTRIBUTED |  |  | INTRA:flkR |
| #14 | L5 | H19 | 11 | +0.1825 | SINGLE-ANCHOR | G159 | SINGLE-ANCHOR | I181 |  |  |
| #3 | L6 | H3 | 22 | +0.4475 | SINGLE-ANCHOR | H355 | SINGLE-ANCHOR | T315 |  | ss2→flkR |
| #26 | L6 | H8 | 4 | +0.0639 | SINGLE-ANCHOR | K326 | SINGLE-ANCHOR | T315 |  | INTRA:flkR |
| #16 | L6 | H17 | 96 | +0.3645 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #10 | L6 | H19 | 52 | +0.3671 | SINGLE-ANCHOR | I181 | SINGLE-ANCHOR | T315 |  |  |
| #1 | L7 | H13 | 81 | +0.6897 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #9 | L7 | H16 | 9 | +0.1578 | DUAL-ANCHOR | L344/I181 | SINGLE-ANCHOR | T315 |  | ss2→flkR |
| #29 | L8 | H12 | 9 | +0.0631 | SINGLE-ANCHOR | T315 | DUAL-ANCHOR | I157/I181 |  | CROSS:flkL→ss2 |
| #7 | L8 | H19 | 15 | +0.1962 | SINGLE-ANCHOR | L337 | SINGLE-ANCHOR | T315 |  | ss2→flkR |
| #25 | L9 | H1 | 11 | +0.1756 | SINGLE-ANCHOR | G163 | MULTI-ANCHOR |  |  | INTRA:flkL |
| #4 | L10 | H9 | 21 | +0.3603 | SINGLE-ANCHOR | T315 | DUAL-ANCHOR | I181/T315 |  |  |
| #2 | L11 | H1 | 17 | +0.3915 | SINGLE-ANCHOR | G163 | SINGLE-ANCHOR | I181 |  | ss1→flkL |
| #17 | L11 | H16 | 36 | +0.1317 | DUAL-ANCHOR | I157/T315 | DISTRIBUTED |  |  |  |
| #30 | L13 | H8 | 18 | +0.0843 | SINGLE-ANCHOR | T315 | DISTRIBUTED |  |  | CROSS:flkL→ss2 |
| #13 | L14 | H9 | 32 | +0.2168 | SINGLE-ANCHOR | T315 | SINGLE-ANCHOR | I181 |  |  |
| #22 | L14 | H14 | 18 | +0.1255 | DISTRIBUTED |  | SINGLE-ANCHOR | I181 |  |  |
| #24 | L15 | H2 | 19 | +0.1140 | SINGLE-ANCHOR | G163 | DUAL-ANCHOR | I181/N183 |  |  |
| #23 | L16 | H17 | 16 | +0.1156 | SINGLE-ANCHOR | G163 | SINGLE-ANCHOR | I181 |  |  |
| #21 | L17 | H18 | 15 | +0.0585 | DUAL-ANCHOR | I157/N183 | DUAL-ANCHOR | I181/L316 |  | ss1→flkL |
| #20 | L19 | H0 | 17 | +0.1015 | DISTRIBUTED |  | SINGLE-ANCHOR | N183 |  |  |
| #6 | L22 | H14 | 17 | +0.1569 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #5 | L26 | H16 | 18 | +0.2315 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #19 | L27 | H15 | 15 | +0.0744 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #15 | L30 | H1 | 12 | +0.0659 | DISTRIBUTED |  | DISTRIBUTED |  | CROSS_SSE | CROSS:ss1→ss2 |
| #8 | L32 | H13 | 13 | +0.1089 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #12 | L32 | H18 | 12 | +0.0804 | DUAL-ANCHOR | N180/I181 | DISTRIBUTED |  | CROSS_SSE | CROSS:ss2→ss1 |
