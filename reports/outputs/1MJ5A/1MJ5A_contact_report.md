# Contact Pattern Analysis: 1MJ5A

Generated: 2026-03-03 05:08:56   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1MJ5A |
| Contact pair | (128, 240) |
| ss1 | [123, 134) |
| ss2 | [235, 246) |
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
| Clean metric | 0.8945 |
| Corrupt metric | 0.0078 |
| Gap | 0.8867 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 88.43% |
| positive IE | 200 | 103.87% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L22 | H14 | +0.1180 |
| 2 | L27 | H15 | +0.0812 |
| 3 | L32 | H18 | +0.0574 |
| 4 | L26 | H16 | +0.0574 |
| 5 | L32 | H13 | +0.0488 |
| 6 | L30 | H1 | +0.0388 |
| 7 | L19 | H0 | +0.0327 |
| 8 | L29 | H18 | +0.0240 |
| 9 | L5 | H19 | +0.0227 |
| 10 | L7 | H0 | +0.0157 |
| 11 | L10 | H12 | +0.0150 |
| 12 | L13 | H2 | +0.0147 |
| 13 | L17 | H10 | +0.0137 |
| 14 | L17 | H18 | +0.0109 |
| 15 | L8 | H6 | +0.0104 |
| 16 | L14 | H14 | +0.0102 |
| 17 | L25 | H16 | +0.0082 |
| 18 | L31 | H17 | +0.0081 |
| 19 | L29 | H15 | +0.0078 |
| 20 | L30 | H0 | +0.0073 |
| 21 | L7 | H7 | +0.0066 |
| 22 | L13 | H15 | +0.0064 |
| 23 | L19 | H15 | +0.0063 |
| 24 | L19 | H14 | +0.0059 |
| 25 | L31 | H8 | +0.0057 |
| 26 | L18 | H6 | +0.0056 |
| 27 | L6 | H12 | +0.0051 |
| 28 | L16 | H19 | +0.0051 |
| 29 | L9 | H13 | +0.0047 |
| 30 | L17 | H19 | +0.0047 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.01% |
| 2 | 0.01% |
| 3 | 0.02% |
| 4 | 0.02% |
| 5 | 0.02% |
| 6 | 0.02% |
| 7 | 0.02% |
| 8 | 0.03% |
| 9 | 0.04% |
| 10 | 0.05% |
| 20 | 0.12% |
| 80 | 1.22% |
| 450 | 123.97% |

## Cell Attribution Analysis

Total cells: 16,776,997

- Positive: 8,374,289
- Negative: 8,394,277

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000006 | 1,677,701 |
| 95th | +0.00000022 | 838,851 |
| 99th | +0.00000206 | 167,771 |
| 99.5th | +0.00000477 | 83,886 |
| 99.9th | +0.00002704 | 16,778 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L22 | H14 | 241 | ss2 | 131 | ss1 | +0.027515 | 0.816524 |
| L5 | H19 | 127 | ss1 | 105 | flkL | +0.020656 | 0.155175 |
| L26 | H16 | 129 | ss1 | 239 | ss2 | +0.016179 | 0.708578 |
| L32 | H18 | 245 | ss2 | 131 | ss1 | +0.013858 | 0.099674 |
| L10 | H12 | 127 | ss1 | 103 | flkL | +0.012782 | 0.428831 |
| L19 | H14 | 131 | ss1 | 127 | ss1 | +0.012372 | 0.368439 |
| L13 | H2 | 129 | ss1 | 127 | ss1 | +0.011677 | 0.824880 |
| L8 | H6 | 238 | ss2 | 238 | ss2 | +0.011122 | 0.161775 |
| L7 | H0 | 103 | flkL | 127 | ss1 | +0.010970 | 0.431089 |
| L22 | H14 | 242 | ss2 | 131 | ss1 | +0.010864 | 0.882066 |
| L31 | H8 | 131 | ss1 | 127 | ss1 | +0.009379 | 0.649685 |
| L32 | H13 | 245 | ss2 | 131 | ss1 | +0.009301 | 0.110169 |
| L22 | H14 | 235 | ss2 | 124 | ss1 | +0.009244 | 0.223575 |
| L25 | H11 | 129 | ss1 | 132 | ss1 | +0.008672 | 0.454936 |
| L22 | H14 | 239 | ss2 | 129 | ss1 | +0.008242 | 0.565019 |
| L27 | H15 | 235 | ss2 | 127 | ss1 | +0.008204 | 0.653645 |
| L28 | H13 | 245 | ss2 | 131 | ss1 | +0.007918 | 0.675257 |
| L17 | H19 | 131 | ss1 | 127 | ss1 | +0.007484 | 0.840496 |
| L7 | H7 | 238 | ss2 | 238 | ss2 | +0.007368 | 0.255656 |
| L27 | H15 | 237 | ss2 | 129 | ss1 | +0.006533 | 0.517509 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L26 | H16 | 127 | ss1 | 237 | ss2 | -0.002489 | 0.778151 |
| L31 | H17 | 131 | ss1 | 302 | other | -0.002597 | 0.042190 |
| L23 | H3 | 124 | ss1 | 124 | ss1 | -0.002606 | 0.528467 |
| L30 | H13 | 129 | ss1 | 114 | flkL | -0.002616 | 0.596424 |
| L19 | H0 | 130 | ss1 | 123 | ss1 | -0.002634 | 0.640303 |
| L22 | H14 | 131 | ss1 | 106 | flkL | -0.002654 | 0.163304 |
| L17 | H4 | 131 | ss1 | 131 | ss1 | -0.002744 | 0.614229 |
| L23 | H3 | 131 | ss1 | 133 | ss1 | -0.002827 | 0.253029 |
| L30 | H0 | 131 | ss1 | 133 | ss1 | -0.002878 | 0.189273 |
| L27 | H10 | 131 | ss1 | 129 | ss1 | -0.003016 | 0.668591 |
| L24 | H7 | 132 | ss1 | 126 | ss1 | -0.003079 | 0.333430 |
| L12 | H3 | 127 | ss1 | 238 | ss2 | -0.003421 | 0.134876 |
| L8 | H6 | 113 | flkL | 103 | flkL | -0.003435 | 0.675924 |
| L28 | H13 | 131 | ss1 | 106 | flkL | -0.003710 | 0.433578 |
| L8 | H12 | 302 | other | 103 | flkL | -0.003768 | 0.644706 |
| L17 | H18 | 129 | ss1 | 106 | flkL | -0.003994 | 0.598972 |
| L9 | H3 | 103 | flkL | 103 | flkL | -0.004015 | 0.480150 |
| L28 | H13 | 247 | flkR | 131 | ss1 | -0.004049 | 0.755642 |
| L10 | H12 | 130 | ss1 | 103 | flkL | -0.005616 | 0.417461 |
| L31 | H17 | 131 | ss1 | -1 | other | -0.008087 | 0.170176 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0078 | 0.00% |
| 10 | 10 | 9 | 0.0078 | 0.00% |
| 20 | 20 | 16 | 0.0079 | 0.01% |
| 50 | 50 | 40 | 0.0079 | 0.01% |
| 100 | 100 | 62 | 0.0082 | 0.05% |
| 200 | 200 | 104 | 0.0086 | 0.09% |
| 500 | 500 | 163 | 0.0110 | 0.36% |
| 1000 | 1,000 | 185 | 0.0144 | 0.74% |
| 2000 | 2,000 | 197 | 0.0409 | 3.73% |
| 5000 | 5,000 | 200 | 0.0938 | 9.69% |
| 10000 | 10,000 | 200 | 0.3785 | 41.81% |
| 20000 | 20,000 | 200 | 0.6829 | 76.14% |
| 50000 | 50,000 | 200 | 0.8269 | 92.38% |

## Motif Analysis

### L5 H19 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 2  |  total attr: +0.0239

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 105 | flkL | +0.0239 | 100.0% |

**Query mass** (top-1=87%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0207 | 86.5% |
| 103 | flkL | +0.0032 | 13.5% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +22 | 1 | 50.0% |
| -2 | 1 | 50.0% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 1 | 50.0% |
| flkL | flkL | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 105 | flkL | +0.0207 | 0.1552 |
| 103 | flkL | 105 | flkL | +0.0032 | 0.1166 |

### L6 H12 — Rank #27

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 4  |  total attr: +0.0078

**Key mass** (top-1=53%, top-2=73%, top-3=88%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 92 | flkL | +0.0041 | 53.2% |
| 91 | flkL | +0.0016 | 20.2% |
| 94 | flkL | +0.0011 | 14.3% |
| 117 | flkL | +0.0010 | 12.3% |

**Query mass** (top-1=88%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | flkL | +0.0068 | 87.7% |
| 127 | ss1 | +0.0010 | 12.3% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +11 | 1 | 25.0% |
| +12 | 1 | 25.0% |
| +9 | 1 | 25.0% |
| +10 | 1 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 3 | 75.0% |
| ss1 | flkL | 1 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 103 | flkL | 92 | flkL | +0.0041 | 0.0897 |
| 103 | flkL | 91 | flkL | +0.0016 | 0.0605 |
| 103 | flkL | 94 | flkL | +0.0011 | 0.0848 |
| 127 | ss1 | 117 | flkL | +0.0010 | 0.0386 |

### L7 H0 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | flkL→ss1  |  cells: 1  |  total attr: +0.0110

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0110 | 100.0% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | flkL | +0.0110 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -24 | 1 | 100.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 1 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 103 | flkL | 127 | ss1 | +0.0110 | 0.4311 |

### L7 H7 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 7  |  total attr: +0.0117

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0117 | 100.0% |

**Query mass** (top-1=63%, top-2=72%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0074 | 62.8% |
| 237 | ss2 | +0.0011 | 9.0% |
| 236 | ss2 | +0.0009 | 8.1% |
| 271 | flkR | +0.0008 | 6.5% |
| 235 | ss2 | +0.0007 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 14.3% |
| -1 | 1 | 14.3% |
| -2 | 1 | 14.3% |
| +33 | 1 | 14.3% |
| -3 | 1 | 14.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=86%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 85.7% |
| flkR | ss2 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 238 | ss2 | 238 | ss2 | +0.0074 | 0.2557 |
| 237 | ss2 | 238 | ss2 | +0.0011 | 0.2183 |
| 236 | ss2 | 238 | ss2 | +0.0009 | 0.2365 |
| 271 | flkR | 238 | ss2 | +0.0008 | 0.1986 |
| 235 | ss2 | 238 | ss2 | +0.0007 | 0.2301 |

### L8 H6 — Rank #15

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 12  |  total attr: +0.0197

**Key mass** (top-1=56%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0111 | 56.4% |
| 103 | flkL | +0.0086 | 43.6% |

**Query mass** (top-1=56%, top-2=65%, top-3=71%)  [DISTR(L238/L112/W116)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0111 | 56.4% |
| 112 | flkL | +0.0017 | 8.4% |
| 116 | flkL | +0.0013 | 6.6% |
| 107 | flkL | +0.0009 | 4.7% |
| 122 | flkL | +0.0009 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 8.3% |
| +9 | 1 | 8.3% |
| +13 | 1 | 8.3% |
| +4 | 1 | 8.3% |
| +19 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 9 | 75.0% |
| ss1 | flkL | 2 | 16.7% |
| ss2 | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 238 | ss2 | 238 | ss2 | +0.0111 | 0.1618 |
| 112 | flkL | 103 | flkL | +0.0017 | 0.4833 |
| 116 | flkL | 103 | flkL | +0.0013 | 0.3418 |
| 107 | flkL | 103 | flkL | +0.0009 | 0.5847 |
| 122 | flkL | 103 | flkL | +0.0009 | 0.3472 |

### L9 H13 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss2  |  cells: 2  |  total attr: +0.0054

**Key mass** (top-1=92%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0050 | 92.5% |
| 274 | flkR | +0.0004 | 7.5% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0054 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 50.0% |
| -36 | 1 | 50.0% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 1 | 50.0% |
| ss2 | flkR | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 238 | ss2 | 238 | ss2 | +0.0050 | 0.2711 |
| 238 | ss2 | 274 | flkR | +0.0004 | 0.0185 |

### L10 H12 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 11  |  total attr: +0.0213

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | flkL | +0.0213 | 100.0% |

**Query mass** (top-1=60%, top-2=72%, top-3=80%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0128 | 60.0% |
| 129 | ss1 | +0.0025 | 11.7% |
| 131 | ss1 | +0.0018 | 8.4% |
| 125 | ss1 | +0.0014 | 6.4% |
| 135 | other | +0.0005 | 2.4% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +24 | 1 | 9.1% |
| +26 | 1 | 9.1% |
| +28 | 1 | 9.1% |
| +22 | 1 | 9.1% |
| +32 | 1 | 9.1% |

**Region-pair profile** (q→k)  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkL | 6 | 54.5% |
| ss1 | flkL | 4 | 36.4% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 103 | flkL | +0.0128 | 0.4288 |
| 129 | ss1 | 103 | flkL | +0.0025 | 0.3259 |
| 131 | ss1 | 103 | flkL | +0.0018 | 0.3542 |
| 125 | ss1 | 103 | flkL | +0.0014 | 0.3742 |
| 135 | other | 103 | flkL | +0.0005 | 0.3014 |

### L13 H2 — Rank #12

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0254

**Key mass** (top-1=86%, top-2=94%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0219 | 86.1% |
| 113 | flkL | +0.0019 | 7.5% |
| 103 | flkL | +0.0016 | 6.4% |

**Query mass** (top-1=46%, top-2=58%, top-3=68%)  [DISTR(Y129/A128/G126/Q125)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss1 | +0.0117 | 45.9% |
| 128 | ss1 | +0.0031 | 12.4% |
| 126 | ss1 | +0.0025 | 9.7% |
| 125 | ss1 | +0.0019 | 7.4% |
| 121 | flkL | +0.0015 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 1 | 7.7% |
| +1 | 1 | 7.7% |
| -1 | 1 | 7.7% |
| -2 | 1 | 7.7% |
| -6 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 38.5% |
| ss1 | ss1 | 4 | 30.8% |
| flkL | ss1 | 2 | 15.4% |
| other | ss1 | 2 | 15.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | ss1 | 127 | ss1 | +0.0117 | 0.8249 |
| 128 | ss1 | 127 | ss1 | +0.0031 | 0.7275 |
| 126 | ss1 | 127 | ss1 | +0.0025 | 0.6088 |
| 125 | ss1 | 127 | ss1 | +0.0019 | 0.5558 |
| 121 | flkL | 127 | ss1 | +0.0015 | 0.3326 |

### L13 H15 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 9  |  total attr: +0.0145

**Key mass** (top-1=79%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0114 | 78.8% |
| 113 | flkL | +0.0031 | 21.2% |

**Query mass** (top-1=27%, top-2=52%, top-3=75%)  [DISTR(I127/Y129/E131)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0039 | 26.7% |
| 129 | ss1 | +0.0037 | 25.4% |
| 131 | ss1 | +0.0033 | 22.7% |
| 124 | ss1 | +0.0010 | 6.7% |
| 126 | ss1 | +0.0008 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -111 | 1 | 11.1% |
| -107 | 1 | 11.1% |
| -109 | 1 | 11.1% |
| +16 | 1 | 11.1% |
| -114 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 55.6% |
| ss1 | flkL | 4 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 238 | ss2 | +0.0039 | 0.4169 |
| 131 | ss1 | 238 | ss2 | +0.0033 | 0.2167 |
| 129 | ss1 | 238 | ss2 | +0.0027 | 0.2866 |
| 129 | ss1 | 113 | flkL | +0.0010 | 0.1898 |
| 124 | ss1 | 238 | ss2 | +0.0010 | 0.2619 |

### L14 H14 — Rank #16

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 10  |  total attr: +0.0147

**Key mass** (top-1=83%, top-2=90%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0122 | 83.4% |
| 103 | flkL | +0.0010 | 6.9% |
| 238 | ss2 | +0.0007 | 5.1% |
| 126 | ss1 | +0.0007 | 4.6% |

**Query mass** (top-1=37%, top-2=53%, top-3=63%)  [DISTR(E131/I133/V124/A134)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0054 | 37.0% |
| 133 | ss1 | +0.0023 | 15.8% |
| 124 | ss1 | +0.0015 | 10.3% |
| 134 | other | +0.0011 | 7.8% |
| 125 | ss1 | +0.0011 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 20.0% |
| +5 | 2 | 20.0% |
| +4 | 1 | 10.0% |
| +6 | 1 | 10.0% |
| -3 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 60.0% |
| other | ss1 | 2 | 20.0% |
| flkL | flkL | 1 | 10.0% |
| ss2 | ss2 | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 131 | ss1 | 127 | ss1 | +0.0047 | 0.6462 |
| 133 | ss1 | 127 | ss1 | +0.0023 | 0.4617 |
| 124 | ss1 | 127 | ss1 | +0.0015 | 0.2008 |
| 134 | other | 127 | ss1 | +0.0011 | 0.5617 |
| 125 | ss1 | 127 | ss1 | +0.0011 | 0.1652 |

### L16 H19 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 9  |  total attr: +0.0086

**Key mass** (top-1=71%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0061 | 71.2% |
| 271 | flkR | +0.0025 | 28.8% |

**Query mass** (top-1=23%, top-2=44%, top-3=64%)  [DISTR(E131/I127/A132/Y129)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0020 | 23.0% |
| 127 | ss1 | +0.0018 | 20.8% |
| 132 | ss1 | +0.0017 | 20.2% |
| 129 | ss1 | +0.0011 | 13.0% |
| 236 | ss2 | +0.0007 | 7.9% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -140 | 1 | 11.1% |
| -111 | 1 | 11.1% |
| -106 | 1 | 11.1% |
| -2 | 1 | 11.1% |
| -109 | 1 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 4 | 44.4% |
| ss1 | flkR | 2 | 22.2% |
| flkL | ss2 | 2 | 22.2% |
| ss2 | ss2 | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 131 | ss1 | 271 | flkR | +0.0020 | 0.1837 |
| 127 | ss1 | 238 | ss2 | +0.0018 | 0.2012 |
| 132 | ss1 | 238 | ss2 | +0.0017 | 0.3452 |
| 236 | ss2 | 238 | ss2 | +0.0007 | 0.1030 |
| 129 | ss1 | 238 | ss2 | +0.0006 | 0.0949 |

### L17 H10 — Rank #13

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 12  |  total attr: +0.0170

**Key mass** (top-1=84%, top-2=95%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0142 | 83.5% |
| 103 | flkL | +0.0020 | 11.6% |
| 129 | ss1 | +0.0004 | 2.6% |
| 108 | flkL | +0.0004 | 2.2% |

**Query mass** (top-1=26%, top-2=43%, top-3=59%)  [DISTR(G126/Y129/Q125/M130)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 126 | ss1 | +0.0044 | 26.0% |
| 129 | ss1 | +0.0029 | 17.3% |
| 125 | ss1 | +0.0027 | 15.9% |
| 130 | ss1 | +0.0020 | 11.8% |
| 131 | ss1 | +0.0014 | 8.5% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 2 | 16.7% |
| +5 | 2 | 16.7% |
| -1 | 1 | 8.3% |
| -2 | 1 | 8.3% |
| +3 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 66.7% |
| ss1 | flkL | 3 | 25.0% |
| flkL | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 126 | ss1 | 127 | ss1 | +0.0040 | 0.9191 |
| 129 | ss1 | 127 | ss1 | +0.0029 | 0.8658 |
| 125 | ss1 | 127 | ss1 | +0.0027 | 0.8211 |
| 130 | ss1 | 127 | ss1 | +0.0020 | 0.8221 |
| 128 | ss1 | 127 | ss1 | +0.0011 | 0.9448 |

### L17 H18 — Rank #14

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0139

**Key mass** (top-1=30%, top-2=59%, top-3=68%)  [DISTR(L103/E131/H106/Y129)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | flkL | +0.0042 | 29.8% |
| 131 | ss1 | +0.0041 | 29.5% |
| 106 | flkL | +0.0012 | 8.7% |
| 129 | ss1 | +0.0011 | 8.0% |
| 102 | flkL | +0.0011 | 7.6% |

**Query mass** (top-1=30%, top-2=55%, top-3=64%)  [DISTR(I127/N241/E131/F239)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0042 | 29.8% |
| 241 | ss2 | +0.0035 | 25.1% |
| 131 | ss1 | +0.0012 | 8.7% |
| 239 | ss2 | +0.0011 | 8.0% |
| 126 | ss1 | +0.0011 | 7.6% |

**Offset distribution [frequency]** (top-2 coverage: 55%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +24 | 3 | 27.3% |
| +110 | 3 | 27.3% |
| +111 | 3 | 27.3% |
| +25 | 1 | 9.1% |
| +27 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=55%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 54.5% |
| ss1 | flkL | 5 | 45.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 103 | flkL | +0.0042 | 0.6051 |
| 241 | ss2 | 131 | ss1 | +0.0035 | 0.1432 |
| 239 | ss2 | 129 | ss1 | +0.0011 | 0.1357 |
| 126 | ss1 | 102 | flkL | +0.0011 | 0.6376 |
| 236 | ss2 | 125 | ss1 | +0.0009 | 0.0364 |

### L17 H19 — Rank #30

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 12  |  total attr: +0.0163

**Key mass** (top-1=50%, top-2=62%, top-3=69%)  [DISTR(I127/A134/Q125/M135)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0082 | 50.2% |
| 134 | other | +0.0020 | 12.1% |
| 125 | ss1 | +0.0011 | 6.8% |
| 135 | other | +0.0011 | 6.6% |
| 133 | ss1 | +0.0010 | 6.3% |

**Query mass** (top-1=73%, top-2=81%, top-3=88%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0120 | 73.5% |
| 124 | ss1 | +0.0013 | 7.7% |
| 129 | ss1 | +0.0011 | 6.8% |
| 133 | ss1 | +0.0006 | 3.9% |
| 130 | ss1 | +0.0005 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 6 | 50.0% |
| -3 | 2 | 16.7% |
| -4 | 1 | 8.3% |
| -2 | 1 | 8.3% |
| +3 | 1 | 8.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 50.0% |
| ss1 | other | 3 | 25.0% |
| other | ss1 | 2 | 16.7% |
| ss1 | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 131 | ss1 | 127 | ss1 | +0.0075 | 0.8405 |
| 131 | ss1 | 134 | other | +0.0020 | 0.1732 |
| 129 | ss1 | 125 | ss1 | +0.0011 | 0.4373 |
| 131 | ss1 | 135 | other | +0.0011 | 0.0902 |
| 131 | ss1 | 133 | ss1 | +0.0010 | 0.0957 |

### L18 H6 — Rank #26

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 8  |  total attr: +0.0075

**Key mass** (top-1=40%, top-2=60%, top-3=73%)  [DISTR(I127/A132/M130)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0030 | 39.6% |
| 132 | ss1 | +0.0015 | 20.2% |
| 130 | ss1 | +0.0010 | 13.7% |
| 128 | ss1 | +0.0010 | 13.6% |
| 113 | flkL | +0.0005 | 6.8% |

**Query mass** (top-1=30%, top-2=53%, top-3=68%)  [DISTR(Q125/I127/E131/Y129)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 125 | ss1 | +0.0023 | 30.5% |
| 127 | ss1 | +0.0017 | 22.7% |
| 131 | ss1 | +0.0011 | 14.6% |
| 129 | ss1 | +0.0010 | 13.7% |
| 112 | flkL | +0.0005 | 6.8% |

**Offset distribution [frequency]** (top-2 coverage: 75%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 4 | 50.0% |
| -2 | 2 | 25.0% |
| +0 | 2 | 25.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 6 | 75.0% |
| flkL | flkL | 2 | 25.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 125 | ss1 | 127 | ss1 | +0.0023 | 0.1934 |
| 131 | ss1 | 132 | ss1 | +0.0011 | 0.0962 |
| 129 | ss1 | 130 | ss1 | +0.0010 | 0.2855 |
| 127 | ss1 | 128 | ss1 | +0.0010 | 0.2737 |
| 127 | ss1 | 127 | ss1 | +0.0007 | 0.0890 |

### L19 H0 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 5  |  total attr: +0.0057

**Key mass** (top-1=61%, top-2=77%, top-3=85%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0035 | 61.0% |
| 113 | flkL | +0.0009 | 16.5% |
| 120 | flkL | +0.0004 | 7.8% |
| 116 | flkL | +0.0004 | 7.8% |
| 130 | ss1 | +0.0004 | 7.0% |

**Query mass** (top-1=61%, top-2=77%, top-3=85%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss1 | +0.0035 | 61.0% |
| 121 | flkL | +0.0009 | 16.5% |
| 127 | ss1 | +0.0004 | 7.8% |
| 124 | ss1 | +0.0004 | 7.8% |
| 132 | ss1 | +0.0004 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 80%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 2 | 40.0% |
| +8 | 2 | 40.0% |
| +7 | 1 | 20.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 2 | 40.0% |
| ss1 | flkL | 2 | 40.0% |
| flkL | flkL | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | ss1 | 127 | ss1 | +0.0035 | 0.8744 |
| 121 | flkL | 113 | flkL | +0.0009 | 0.2787 |
| 127 | ss1 | 120 | flkL | +0.0004 | 0.2740 |
| 124 | ss1 | 116 | flkL | +0.0004 | 0.0786 |
| 132 | ss1 | 130 | ss1 | +0.0004 | 0.7974 |

### L19 H14 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 6  |  total attr: +0.0170

**Key mass** (top-1=73%, top-2=87%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0124 | 72.6% |
| 126 | ss1 | +0.0025 | 14.4% |
| 120 | flkL | +0.0010 | 6.0% |
| 114 | flkL | +0.0008 | 4.6% |
| 102 | flkL | +0.0004 | 2.4% |

**Query mass** (top-1=88%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0150 | 88.2% |
| 130 | ss1 | +0.0012 | 7.1% |
| 125 | ss1 | +0.0008 | 4.6% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 33.3% |
| +11 | 2 | 33.3% |
| +5 | 1 | 16.7% |
| +29 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 50.0% |
| ss1 | flkL | 3 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 131 | ss1 | 127 | ss1 | +0.0124 | 0.3684 |
| 131 | ss1 | 126 | ss1 | +0.0012 | 0.0570 |
| 130 | ss1 | 126 | ss1 | +0.0012 | 0.1760 |
| 131 | ss1 | 120 | flkL | +0.0010 | 0.2489 |
| 125 | ss1 | 114 | flkL | +0.0008 | 0.1665 |

### L19 H15 — Rank #23

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 10  |  total attr: +0.0092

**Key mass** (top-1=62%, top-2=77%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 238 | ss2 | +0.0057 | 61.8% |
| 127 | ss1 | +0.0014 | 15.1% |
| 271 | flkR | +0.0008 | 9.0% |
| 129 | ss1 | +0.0007 | 8.0% |
| 240 | ss2 | +0.0006 | 6.0% |

**Query mass** (top-1=33%, top-2=51%, top-3=65%)  [DISTR(Y129/D107/E131/C256)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss1 | +0.0030 | 32.7% |
| 107 | flkL | +0.0017 | 18.3% |
| 131 | ss1 | +0.0013 | 14.2% |
| 256 | flkR | +0.0008 | 9.0% |
| 124 | ss1 | +0.0008 | 8.8% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -111 | 2 | 20.0% |
| -109 | 1 | 10.0% |
| -107 | 1 | 10.0% |
| -20 | 1 | 10.0% |
| -15 | 1 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 6 | 60.0% |
| flkL | ss1 | 3 | 30.0% |
| flkR | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | ss1 | 238 | ss2 | +0.0025 | 0.1429 |
| 131 | ss1 | 238 | ss2 | +0.0013 | 0.1580 |
| 107 | flkL | 127 | ss1 | +0.0009 | 0.2263 |
| 256 | flkR | 271 | flkR | +0.0008 | 0.1372 |
| 124 | ss1 | 238 | ss2 | +0.0008 | 0.1312 |

### L22 H14 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 25  |  total attr: +0.0865

**Key mass** (top-1=46%, top-2=58%, top-3=69%)  [DISTR(E131/Y129/V124/Q125)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0397 | 45.9% |
| 129 | ss1 | +0.0104 | 12.0% |
| 124 | ss1 | +0.0092 | 10.7% |
| 125 | ss1 | +0.0059 | 6.8% |
| 101 | flkL | +0.0048 | 5.5% |

**Query mass** (top-1=32%, top-2=45%, top-3=58%)  [DISTR(N241/I235/A242/F239/P236)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 241 | ss2 | +0.0275 | 31.8% |
| 235 | ss2 | +0.0115 | 13.3% |
| 242 | ss2 | +0.0109 | 12.6% |
| 239 | ss2 | +0.0087 | 10.0% |
| 236 | ss2 | +0.0055 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 32%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 4 | 16.0% |
| +24 | 4 | 16.0% |
| +111 | 3 | 12.0% |
| +23 | 2 | 8.0% |
| +108 | 2 | 8.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 15 | 60.0% |
| ss1 | flkL | 10 | 40.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 241 | ss2 | 131 | ss1 | +0.0275 | 0.8165 |
| 242 | ss2 | 131 | ss1 | +0.0109 | 0.8821 |
| 235 | ss2 | 124 | ss1 | +0.0092 | 0.2236 |
| 239 | ss2 | 129 | ss1 | +0.0082 | 0.5650 |
| 236 | ss2 | 125 | ss1 | +0.0055 | 0.1522 |

### L25 H16 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss1  |  cells: 11  |  total attr: +0.0177

**Key mass** (top-1=24%, top-2=46%, top-3=67%)  [DISTR(M130/G126/A132/I127)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 130 | ss1 | +0.0042 | 23.8% |
| 126 | ss1 | +0.0039 | 22.1% |
| 132 | ss1 | +0.0038 | 21.6% |
| 127 | ss1 | +0.0033 | 18.8% |
| 128 | ss1 | +0.0006 | 3.5% |

**Query mass** (top-1=24%, top-2=48%, top-3=72%)  [DISTR(E131/Q125/Y129)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0043 | 24.5% |
| 125 | ss1 | +0.0043 | 23.9% |
| 129 | ss1 | +0.0042 | 23.8% |
| 126 | ss1 | +0.0024 | 13.7% |
| 124 | ss1 | +0.0011 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 82%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 7 | 63.6% |
| -2 | 2 | 18.2% |
| +11 | 2 | 18.2% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 72.7% |
| ss1 | flkL | 2 | 18.2% |
| flkL | flkL | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | ss1 | 130 | ss1 | +0.0042 | 0.4598 |
| 131 | ss1 | 132 | ss1 | +0.0038 | 0.2731 |
| 125 | ss1 | 126 | ss1 | +0.0029 | 0.6716 |
| 126 | ss1 | 127 | ss1 | +0.0019 | 0.5089 |
| 125 | ss1 | 127 | ss1 | +0.0014 | 0.2159 |

### L26 H16 — Rank #4

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR | CROSS:ss1→ss2  |  cells: 13  |  total attr: +0.0362

**Key mass** (top-1=45%, top-2=62%, top-3=70%)  [DISTR(F239/I235/P236/N241)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | ss2 | +0.0162 | 44.8% |
| 235 | ss2 | +0.0061 | 16.9% |
| 236 | ss2 | +0.0029 | 8.2% |
| 241 | ss2 | +0.0021 | 5.9% |
| 237 | ss2 | +0.0020 | 5.6% |

**Query mass** (top-1=50%, top-2=69%, top-3=81%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss1 | +0.0182 | 50.4% |
| 124 | ss1 | +0.0066 | 18.2% |
| 125 | ss1 | +0.0044 | 12.1% |
| 131 | ss1 | +0.0042 | 11.7% |
| 235 | ss2 | +0.0015 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -111 | 3 | 23.1% |
| -110 | 2 | 15.4% |
| -24 | 2 | 15.4% |
| -108 | 1 | 7.7% |
| +25 | 1 | 7.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 61.5% |
| ss1 | flkL | 2 | 15.4% |
| ss2 | flkR | 2 | 15.4% |
| flkL | flkL | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 129 | ss1 | 239 | ss2 | +0.0162 | 0.7086 |
| 124 | ss1 | 235 | ss2 | +0.0061 | 0.2209 |
| 125 | ss1 | 236 | ss2 | +0.0029 | 0.0973 |
| 131 | ss1 | 241 | ss2 | +0.0021 | 0.0486 |
| 129 | ss1 | 237 | ss2 | +0.0020 | 0.0971 |

### L27 H15 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 16  |  total attr: +0.0259

**Key mass** (top-1=32%, top-2=59%, top-3=65%)  [DISTR(I127/Y129/E131/Q125)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0082 | 31.7% |
| 129 | ss1 | +0.0070 | 27.1% |
| 131 | ss1 | +0.0017 | 6.6% |
| 125 | ss1 | +0.0013 | 5.1% |
| 102 | flkL | +0.0013 | 5.0% |

**Query mass** (top-1=38%, top-2=63%, top-3=75%)  [DISTR(I235/K237/E131)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 235 | ss2 | +0.0098 | 38.0% |
| 237 | ss2 | +0.0065 | 25.3% |
| 131 | ss1 | +0.0031 | 12.1% |
| 236 | ss2 | +0.0017 | 6.5% |
| 125 | ss1 | +0.0013 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +108 | 2 | 12.5% |
| +111 | 2 | 12.5% |
| +24 | 2 | 12.5% |
| +0 | 2 | 12.5% |
| +110 | 2 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 50.0% |
| ss1 | flkL | 4 | 25.0% |
| ss2 | flkL | 1 | 6.2% |
| ss1 | ss1 | 1 | 6.2% |
| flkL | flkL | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 235 | ss2 | 127 | ss1 | +0.0082 | 0.6536 |
| 237 | ss2 | 129 | ss1 | +0.0065 | 0.5175 |
| 236 | ss2 | 125 | ss1 | +0.0013 | 0.0286 |
| 125 | ss1 | 102 | flkL | +0.0013 | 0.6588 |
| 128 | ss1 | 104 | flkL | +0.0013 | 0.9022 |

### L29 H15 — Rank #19

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0103

**Key mass** (top-1=50%, top-2=82%, top-3=90%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0052 | 50.3% |
| 107 | flkL | +0.0033 | 31.8% |
| 129 | ss1 | +0.0009 | 8.4% |
| 241 | ss2 | +0.0006 | 5.5% |
| 275 | flkR | +0.0004 | 4.0% |

**Query mass** (top-1=70%, top-2=78%, top-3=84%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 245 | ss2 | +0.0072 | 69.6% |
| 271 | flkR | +0.0009 | 8.7% |
| 131 | ss1 | +0.0006 | 5.5% |
| 239 | ss2 | +0.0005 | 4.5% |
| 124 | ss1 | +0.0004 | 4.0% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 2 | 25.0% |
| +114 | 1 | 12.5% |
| +138 | 1 | 12.5% |
| +164 | 1 | 12.5% |
| -110 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 50.0% |
| ss2 | flkL | 1 | 12.5% |
| flkR | flkL | 1 | 12.5% |
| ss1 | ss2 | 1 | 12.5% |
| ss1 | flkR | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 245 | ss2 | 131 | ss1 | +0.0048 | 0.1163 |
| 245 | ss2 | 107 | flkL | +0.0024 | 0.1283 |
| 271 | flkR | 107 | flkL | +0.0009 | 0.2368 |
| 131 | ss1 | 241 | ss2 | +0.0006 | 0.0199 |
| 239 | ss2 | 129 | ss1 | +0.0005 | 0.0481 |

### L29 H18 — Rank #8

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 35  |  total attr: +0.0311

**Key mass** (top-1=15%, top-2=25%, top-3=33%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0048 | 15.4% |
| 245 | ss2 | +0.0029 | 9.2% |
| 121 | flkL | +0.0026 | 8.4% |
| 272 | flkR | +0.0018 | 6.0% |
| 302 | other | +0.0018 | 5.7% |

**Query mass** (top-1=36%, top-2=53%, top-3=64%)  [DISTR(E131/G245/I235/I127)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0111 | 35.8% |
| 245 | ss2 | +0.0053 | 17.1% |
| 235 | ss2 | +0.0036 | 11.5% |
| 127 | ss1 | +0.0024 | 7.9% |
| 129 | ss1 | +0.0020 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 5.7% |
| +111 | 2 | 5.7% |
| +10 | 2 | 5.7% |
| +112 | 2 | 5.7% |
| -111 | 2 | 5.7% |

**Region-pair profile** (q→k)  (top=23%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 8 | 22.9% |
| ss2 | ss1 | 5 | 14.3% |
| ss1 | ss2 | 5 | 14.3% |
| ss1 | flkR | 5 | 14.3% |
| ss1 | other | 4 | 11.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 245 | ss2 | 131 | ss1 | +0.0048 | 0.0917 |
| 131 | ss1 | 245 | ss2 | +0.0024 | 0.0660 |
| 131 | ss1 | 272 | flkR | +0.0018 | 0.0478 |
| 131 | ss1 | 246 | flkR | +0.0017 | 0.0997 |
| 235 | ss2 | 121 | flkL | +0.0016 | 0.1774 |

### L30 H0 — Rank #20

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 8  |  total attr: +0.0082

**Key mass** (top-1=35%, top-2=56%, top-3=74%)  [DISTR(S110/I127/E131)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 110 | flkL | +0.0029 | 35.0% |
| 127 | ss1 | +0.0017 | 21.4% |
| 131 | ss1 | +0.0015 | 17.9% |
| 238 | ss2 | +0.0009 | 11.3% |
| 240 | ss2 | +0.0007 | 8.3% |

**Query mass** (top-1=30%, top-2=52%, top-3=69%)  [DISTR(E131/I235/Y129/G126)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0025 | 30.4% |
| 235 | ss2 | +0.0017 | 21.4% |
| 129 | ss1 | +0.0014 | 17.0% |
| 126 | ss1 | +0.0009 | 11.3% |
| 128 | ss1 | +0.0007 | 8.3% |

**Offset distribution [frequency]** (top-2 coverage: 38%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 2 | 25.0% |
| +108 | 1 | 12.5% |
| +21 | 1 | 12.5% |
| +19 | 1 | 12.5% |
| +0 | 1 | 12.5% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 25.0% |
| ss1 | flkL | 2 | 25.0% |
| ss1 | ss2 | 2 | 25.0% |
| ss1 | ss1 | 1 | 12.5% |
| ss2 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 235 | ss2 | 127 | ss1 | +0.0017 | 0.5615 |
| 131 | ss1 | 110 | flkL | +0.0015 | 0.0986 |
| 129 | ss1 | 110 | flkL | +0.0014 | 0.3082 |
| 131 | ss1 | 131 | ss1 | +0.0010 | 0.0678 |
| 126 | ss1 | 238 | ss2 | +0.0009 | 0.2098 |

### L30 H1 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 15  |  total attr: +0.0237

**Key mass** (top-1=25%, top-2=47%, top-3=61%)  [DISTR(P236/Y129/I127/I235)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 236 | ss2 | +0.0058 | 24.6% |
| 129 | ss1 | +0.0053 | 22.6% |
| 127 | ss1 | +0.0032 | 13.7% |
| 235 | ss2 | +0.0027 | 11.5% |
| 238 | ss2 | +0.0015 | 6.5% |

**Query mass** (top-1=25%, top-2=40%, top-3=54%)  [DISTR(Q125/I235/F239/E131/K237)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 125 | ss1 | +0.0058 | 24.6% |
| 235 | ss2 | +0.0037 | 15.8% |
| 239 | ss2 | +0.0032 | 13.4% |
| 131 | ss1 | +0.0029 | 12.1% |
| 237 | ss2 | +0.0022 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -111 | 3 | 20.0% |
| +108 | 2 | 13.3% |
| +111 | 2 | 13.3% |
| +110 | 1 | 6.7% |
| -112 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 53.3% |
| ss2 | ss1 | 6 | 40.0% |
| ss1 | flkR | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 125 | ss1 | 236 | ss2 | +0.0058 | 0.1634 |
| 235 | ss2 | 127 | ss1 | +0.0032 | 0.1983 |
| 239 | ss2 | 129 | ss1 | +0.0032 | 0.3551 |
| 237 | ss2 | 129 | ss1 | +0.0022 | 0.2110 |
| 124 | ss1 | 235 | ss2 | +0.0017 | 0.0418 |

### L31 H8 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 6  |  total attr: +0.0145

**Key mass** (top-1=65%, top-2=78%, top-3=85%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0094 | 64.8% |
| 120 | flkL | +0.0019 | 13.0% |
| 131 | ss1 | +0.0010 | 6.7% |
| 107 | flkL | +0.0009 | 6.1% |
| 122 | flkL | +0.0008 | 5.2% |

**Query mass** (top-1=82%, top-2=95%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0118 | 81.7% |
| 124 | ss1 | +0.0019 | 13.0% |
| 126 | ss1 | +0.0008 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 67%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 3 | 50.0% |
| +0 | 1 | 16.7% |
| +24 | 1 | 16.7% |
| +23 | 1 | 16.7% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 4 | 66.7% |
| ss1 | ss1 | 2 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 131 | ss1 | 127 | ss1 | +0.0094 | 0.6497 |
| 124 | ss1 | 120 | flkL | +0.0019 | 0.6657 |
| 131 | ss1 | 131 | ss1 | +0.0010 | 0.0995 |
| 131 | ss1 | 107 | flkL | +0.0009 | 0.0723 |
| 126 | ss1 | 122 | flkL | +0.0008 | 0.6748 |

### L31 H17 — Rank #18

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 9  |  total attr: +0.0086

**Key mass** (top-1=20%, top-2=36%, top-3=51%)  [DISTR(E131/F114/?-1/R121/F272)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0018 | 20.5% |
| 114 | flkL | +0.0013 | 15.3% |
| -1 | other | +0.0013 | 15.2% |
| 121 | flkL | +0.0013 | 15.2% |
| 272 | flkR | +0.0012 | 14.0% |

**Query mass** (top-1=24%, top-2=45%, top-3=60%)  [DISTR(E131/G245/Q125/Y129)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0021 | 24.3% |
| 245 | ss2 | +0.0018 | 20.5% |
| 125 | ss1 | +0.0014 | 15.7% |
| 129 | ss1 | +0.0013 | 15.3% |
| 235 | ss2 | +0.0013 | 15.2% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +114 | 2 | 22.2% |
| +15 | 1 | 11.1% |
| -141 | 1 | 11.1% |
| +126 | 1 | 11.1% |
| -127 | 1 | 11.1% |

**Region-pair profile** (q→k)  (top=22%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 2 | 22.2% |
| ss1 | flkR | 2 | 22.2% |
| ss1 | other | 2 | 22.2% |
| ss1 | flkL | 1 | 11.1% |
| ss2 | flkL | 1 | 11.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 245 | ss2 | 131 | ss1 | +0.0018 | 0.0542 |
| 129 | ss1 | 114 | flkL | +0.0013 | 0.1944 |
| 235 | ss2 | 121 | flkL | +0.0013 | 0.1692 |
| 131 | ss1 | 272 | flkR | +0.0012 | 0.0892 |
| 125 | ss1 | -1 | other | +0.0009 | 0.1803 |

### L32 H13 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 18  |  total attr: +0.0336

**Key mass** (top-1=36%, top-2=47%, top-3=57%)  [DISTR(E131/G245/I127/Y129/K237)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0121 | 36.0% |
| 245 | ss2 | +0.0036 | 10.9% |
| 127 | ss1 | +0.0034 | 10.0% |
| 129 | ss1 | +0.0033 | 9.7% |
| 237 | ss2 | +0.0020 | 5.9% |

**Query mass** (top-1=28%, top-2=43%, top-3=56%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 245 | ss2 | +0.0093 | 27.7% |
| 131 | ss1 | +0.0051 | 15.1% |
| 235 | ss2 | +0.0043 | 12.9% |
| 237 | ss2 | +0.0028 | 8.3% |
| 129 | ss1 | +0.0020 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +111 | 3 | 16.7% |
| -111 | 3 | 16.7% |
| +108 | 2 | 11.1% |
| -108 | 2 | 11.1% |
| +110 | 2 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 50.0% |
| ss1 | ss2 | 9 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 245 | ss2 | 131 | ss1 | +0.0093 | 0.1102 |
| 131 | ss1 | 245 | ss2 | +0.0036 | 0.0432 |
| 235 | ss2 | 127 | ss1 | +0.0034 | 0.1385 |
| 237 | ss2 | 129 | ss1 | +0.0028 | 0.1497 |
| 129 | ss1 | 237 | ss2 | +0.0020 | 0.1067 |

### L32 H18 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 18  |  total attr: +0.0394

**Key mass** (top-1=44%, top-2=56%, top-3=63%)  [DISTR(E131/Y129/Q125/F239/K237)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss1 | +0.0173 | 43.8% |
| 129 | ss1 | +0.0047 | 11.9% |
| 125 | ss1 | +0.0030 | 7.7% |
| 239 | ss2 | +0.0024 | 6.0% |
| 237 | ss2 | +0.0021 | 5.4% |

**Query mass** (top-1=35%, top-2=47%, top-3=57%)  [DISTR(G245/Y129/K237/E131/P236)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 245 | ss2 | +0.0139 | 35.2% |
| 129 | ss1 | +0.0045 | 11.4% |
| 237 | ss2 | +0.0040 | 10.1% |
| 131 | ss1 | +0.0028 | 7.0% |
| 236 | ss2 | +0.0025 | 6.3% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +110 | 4 | 22.2% |
| +108 | 2 | 11.1% |
| +111 | 2 | 11.1% |
| -110 | 2 | 11.1% |
| -108 | 2 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 10 | 55.6% |
| ss1 | ss2 | 8 | 44.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 245 | ss2 | 131 | ss1 | +0.0139 | 0.0997 |
| 237 | ss2 | 129 | ss1 | +0.0035 | 0.1156 |
| 236 | ss2 | 125 | ss1 | +0.0025 | 0.0302 |
| 129 | ss1 | 239 | ss2 | +0.0024 | 0.0981 |
| 129 | ss1 | 237 | ss2 | +0.0021 | 0.0700 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #9 | L5 | H19 | 2 | +0.0239 | SINGLE-ANCHOR | V105 | SINGLE-ANCHOR | I127 |  | ss1→flkL |
| #27 | L6 | H12 | 4 | +0.0078 | DUAL-ANCHOR | W92/L91 | SINGLE-ANCHOR | L103 |  | INTRA:flkL |
| #10 | L7 | H0 | 1 | +0.0110 | SINGLE-ANCHOR | I127 | SINGLE-ANCHOR | L103 |  | flkL→ss1 |
| #21 | L7 | H7 | 7 | +0.0117 | SINGLE-ANCHOR | L238 | SINGLE-ANCHOR | L238 |  | INTRA:ss2 |
| #15 | L8 | H6 | 12 | +0.0197 | DUAL-ANCHOR | L238/L103 | DISTRIBUTED | L238/L112/W116 |  | INTRA:flkL |
| #29 | L9 | H13 | 2 | +0.0054 | SINGLE-ANCHOR | L238 | SINGLE-ANCHOR | L238 |  | INTRA:ss2 |
| #11 | L10 | H12 | 11 | +0.0213 | SINGLE-ANCHOR | L103 | SINGLE-ANCHOR | I127 |  |  |
| #12 | L13 | H2 | 13 | +0.0254 | SINGLE-ANCHOR | I127 | DISTRIBUTED | Y129/A128/G126/Q125 |  |  |
| #22 | L13 | H15 | 9 | +0.0145 | SINGLE-ANCHOR | L238 | DISTRIBUTED | I127/Y129/E131 |  | CROSS:ss1→ss2 |
| #16 | L14 | H14 | 10 | +0.0147 | SINGLE-ANCHOR | I127 | DISTRIBUTED | E131/I133/V124/A134 |  | INTRA:ss1 |
| #28 | L16 | H19 | 9 | +0.0086 | SINGLE-ANCHOR | L238 | DISTRIBUTED | E131/I127/A132/Y129 |  | CROSS:ss1→ss2 |
| #13 | L17 | H10 | 12 | +0.0170 | SINGLE-ANCHOR | I127 | DISTRIBUTED | G126/Y129/Q125/M130 |  | INTRA:ss1 |
| #14 | L17 | H18 | 11 | +0.0139 | DISTRIBUTED | L103/E131/H106/Y129 | DISTRIBUTED | I127/N241/E131/F239 |  | CROSS:ss2→ss1 |
| #30 | L17 | H19 | 12 | +0.0163 | DISTRIBUTED | I127/A134/Q125/M135 | SINGLE-ANCHOR | E131 |  | INTRA:ss1 |
| #26 | L18 | H6 | 8 | +0.0075 | DISTRIBUTED | I127/A132/M130 | DISTRIBUTED | Q125/I127/E131/Y129 | POSITIONAL | INTRA:ss1 |
| #7 | L19 | H0 | 5 | +0.0057 | SINGLE-ANCHOR | I127 | SINGLE-ANCHOR | Y129 |  | INTRA:ss1 |
| #24 | L19 | H14 | 6 | +0.0170 | SINGLE-ANCHOR | I127 | SINGLE-ANCHOR | E131 |  | INTRA:ss1 |
| #23 | L19 | H15 | 10 | +0.0092 | SINGLE-ANCHOR | L238 | DISTRIBUTED | Y129/D107/E131/C256 |  | CROSS:ss1→ss2 |
| #1 | L22 | H14 | 25 | +0.0865 | DISTRIBUTED | E131/Y129/V124/Q125 | DISTRIBUTED | N241/I235/A242/F239/P236 |  | CROSS:ss2→ss1 |
| #17 | L25 | H16 | 11 | +0.0177 | DISTRIBUTED | M130/G126/A132/I127 | DISTRIBUTED | E131/Q125/Y129 | POSITIONAL | INTRA:ss1 |
| #4 | L26 | H16 | 13 | +0.0362 | DISTRIBUTED | F239/I235/P236/N241 | MULTI-ANCHOR |  |  | CROSS:ss1→ss2 |
| #2 | L27 | H15 | 16 | +0.0259 | DISTRIBUTED | I127/Y129/E131/Q125 | DISTRIBUTED | I235/K237/E131 |  | CROSS:ss2→ss1 |
| #19 | L29 | H15 | 8 | +0.0103 | DUAL-ANCHOR | E131/D107 | SINGLE-ANCHOR | G245 |  | CROSS:ss2→ss1 |
| #8 | L29 | H18 | 35 | +0.0311 | DISTRIBUTED |  | DISTRIBUTED | E131/G245/I235/I127 |  |  |
| #20 | L30 | H0 | 8 | +0.0082 | DISTRIBUTED | S110/I127/E131 | DISTRIBUTED | E131/I235/Y129/G126 |  |  |
| #6 | L30 | H1 | 15 | +0.0237 | DISTRIBUTED | P236/Y129/I127/I235 | DISTRIBUTED | Q125/I235/F239/E131/K237 |  | CROSS:ss1→ss2 |
| #25 | L31 | H8 | 6 | +0.0145 | SINGLE-ANCHOR | I127 | SINGLE-ANCHOR | E131 |  | ss1→flkL |
| #18 | L31 | H17 | 9 | +0.0086 | DISTRIBUTED | E131/F114/?-1/R121/F272 | DISTRIBUTED | E131/G245/Q125/Y129 |  |  |
| #5 | L32 | H13 | 18 | +0.0336 | DISTRIBUTED | E131/G245/I127/Y129/K237 | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #3 | L32 | H18 | 18 | +0.0394 | DISTRIBUTED | E131/Y129/Q125/F239/K237 | DISTRIBUTED | G245/Y129/K237/E131/P236 |  | CROSS:ss2→ss1 |
