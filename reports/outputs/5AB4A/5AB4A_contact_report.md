# Contact Pattern Analysis: 5AB4A

Generated: 2026-03-22 22:34:44   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 5AB4A |
| Contact pair | (127, 233) |
| ss1 | [122, 133) |
| ss2 | [228, 239) |
| Clean flank | 66 |
| Corrupt flank | 65 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 1.0716 |
| Corrupt metric | 0.0572 |
| Gap | 1.0144 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 300 | 88.28% |
| positive IE | 85 | 71.57% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L27 | H15 | +0.2816 |
| 2 | L32 | H18 | +0.1937 |
| 3 | L8 | H14 | +0.1557 |
| 4 | L11 | H16 | +0.1480 |
| 5 | L29 | H18 | +0.1343 |
| 6 | L26 | H16 | +0.1334 |
| 7 | L25 | H16 | +0.0941 |
| 8 | L14 | H9 | +0.0916 |
| 9 | L10 | H9 | +0.0841 |
| 10 | L32 | H13 | +0.0816 |
| 11 | L14 | H13 | +0.0778 |
| 12 | L30 | H1 | +0.0757 |
| 13 | L31 | H17 | +0.0613 |
| 14 | L16 | H7 | +0.0598 |
| 15 | L23 | H18 | +0.0468 |
| 16 | L30 | H0 | +0.0376 |
| 17 | L26 | H3 | +0.0360 |
| 18 | L12 | H8 | +0.0340 |
| 19 | L7 | H13 | +0.0335 |
| 20 | L9 | H1 | +0.0305 |
| 21 | L21 | H4 | +0.0302 |
| 22 | L15 | H12 | +0.0290 |
| 23 | L20 | H4 | +0.0284 |
| 24 | L16 | H2 | +0.0279 |
| 25 | L15 | H13 | +0.0262 |
| 26 | L17 | H7 | +0.0256 |
| 27 | L13 | H13 | +0.0255 |
| 28 | L4 | H9 | +0.0255 |
| 29 | L32 | H0 | +0.0250 |
| 30 | L0 | H8 | +0.0244 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.05% |
| 2 | 0.21% |
| 3 | 0.27% |
| 4 | 0.39% |
| 5 | 0.56% |
| 6 | 0.64% |
| 7 | 0.65% |
| 8 | 0.77% |
| 9 | 1.08% |
| 10 | 1.36% |
| 20 | 4.51% |
| 80 | 60.24% |
| 450 | 150.93% |

## Cell Attribution Analysis

Total cells: 14,295,448

- Positive: 7,193,125
- Negative: 7,095,840

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000023 | 1,429,546 |
| 95th | +0.00000080 | 714,774 |
| 99th | +0.00000847 | 142,955 |
| 99.5th | +0.00001995 | 71,478 |
| 99.9th | +0.00011586 | 14,296 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L8 | H14 | 104 | flkL | 124 | ss1 | +0.234334 | 0.101532 |
| L14 | H13 | 119 | flkL | 104 | flkL | +0.064671 | 0.360426 |
| L14 | H13 | 125 | ss1 | 104 | flkL | +0.061267 | 0.466336 |
| L11 | H16 | 232 | ss2 | 104 | flkL | +0.057398 | 0.223598 |
| L29 | H18 | 127 | ss1 | 232 | ss2 | +0.049474 | 0.383723 |
| L14 | H9 | 232 | ss2 | 104 | flkL | +0.049415 | 0.366346 |
| L25 | H16 | 234 | ss2 | 235 | ss2 | +0.044794 | 0.508165 |
| L27 | H15 | 231 | ss2 | 128 | ss1 | +0.042838 | 0.180715 |
| L16 | H7 | 124 | ss1 | 104 | flkL | +0.042439 | 0.805714 |
| L20 | H3 | 228 | ss2 | 234 | ss2 | +0.041007 | 0.376971 |
| L11 | H6 | 63 | flkL | 104 | flkL | +0.040540 | 0.104118 |
| L26 | H16 | 128 | ss1 | 231 | ss2 | +0.040250 | 0.204070 |
| L10 | H9 | 104 | flkL | 104 | flkL | +0.039393 | 0.118395 |
| L20 | H9 | 85 | flkL | 119 | flkL | +0.037959 | 0.337318 |
| L5 | H8 | 124 | ss1 | 119 | flkL | +0.037441 | 0.020776 |
| L19 | H0 | 119 | flkL | 112 | flkL | +0.036960 | 0.521799 |
| L16 | H12 | 237 | ss2 | 233 | ss2 | +0.034331 | 0.363590 |
| L19 | H0 | 127 | ss1 | 124 | ss1 | +0.033731 | 0.191947 |
| L17 | H12 | 124 | ss1 | 104 | flkL | +0.033221 | 0.475191 |
| L30 | H1 | 127 | ss1 | 232 | ss2 | +0.032095 | 0.196446 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L16 | H10 | 231 | ss2 | 126 | ss1 | -0.012516 | 0.193711 |
| L14 | H13 | 130 | ss1 | 104 | flkL | -0.013287 | 0.367126 |
| L16 | H7 | 120 | flkL | 104 | flkL | -0.013325 | 0.768086 |
| L14 | H13 | 233 | ss2 | 104 | flkL | -0.013688 | 0.048700 |
| L9 | H1 | 63 | flkL | 104 | flkL | -0.014300 | 0.131547 |
| L21 | H11 | 85 | flkL | 80 | flkL | -0.014655 | 0.125105 |
| L12 | H19 | 104 | flkL | 104 | flkL | -0.016328 | 0.119182 |
| L19 | H0 | 116 | flkL | 108 | flkL | -0.016837 | 0.320835 |
| L13 | H16 | 304 | flkR | 104 | flkL | -0.017397 | 0.580444 |
| L13 | H16 | 127 | ss1 | 104 | flkL | -0.017549 | 0.208529 |
| L12 | H19 | 233 | ss2 | 104 | flkL | -0.017908 | 0.196090 |
| L15 | H18 | 234 | ss2 | 104 | flkL | -0.018452 | 0.319776 |
| L16 | H7 | 121 | flkL | 104 | flkL | -0.018813 | 0.752072 |
| L17 | H12 | 132 | ss1 | 104 | flkL | -0.019594 | 0.604894 |
| L26 | H3 | 237 | ss2 | 233 | ss2 | -0.019975 | 0.357340 |
| L16 | H7 | 128 | ss1 | 104 | flkL | -0.023649 | 0.678147 |
| L17 | H12 | 231 | ss2 | 104 | flkL | -0.024050 | 0.522862 |
| L18 | H3 | 232 | ss2 | 104 | flkL | -0.026676 | 0.304676 |
| L9 | H1 | 104 | flkL | 104 | flkL | -0.027732 | 0.068194 |
| L17 | H12 | 228 | ss2 | 104 | flkL | -0.038102 | 0.525643 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0572 | 0.00% |
| 10 | 10 | 9 | 0.0579 | 0.07% |
| 20 | 20 | 18 | 0.0583 | 0.12% |
| 50 | 50 | 27 | 0.0597 | 0.25% |
| 100 | 100 | 45 | 0.0613 | 0.41% |
| 200 | 200 | 61 | 0.0677 | 1.04% |
| 500 | 500 | 74 | 0.0822 | 2.47% |
| 1000 | 1,000 | 82 | 0.1042 | 4.63% |
| 2000 | 2,000 | 84 | 0.1374 | 7.91% |
| 5000 | 5,000 | 85 | 0.2226 | 16.31% |
| 10000 | 10,000 | 85 | 0.4001 | 33.81% |
| 20000 | 20,000 | 85 | 0.5845 | 51.99% |
| 50000 | 50,000 | 85 | 0.9218 | 85.23% |

## Motif Analysis

### L0 H8 — Rank #30

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 8  |  total attr: +0.0238

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 304 | flkR | +0.0238 | 100.0% |

**Query mass** (top-1=20%, top-2=35%, top-3=49%)  [DISTR(F296/G101/F93/F245/G276)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 296 | flkR | +0.0048 | 20.2% |
| 101 | flkL | +0.0036 | 15.3% |
| 93 | flkL | +0.0032 | 13.5% |
| 245 | flkR | +0.0030 | 12.6% |
| 276 | flkR | +0.0027 | 11.2% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 1 | 12.5% |
| -203 | 1 | 12.5% |
| -211 | 1 | 12.5% |
| -59 | 1 | 12.5% |
| -28 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 50.0% |
| flkL | flkR | 4 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 296 | flkR | 304 | flkR | +0.0048 | 0.1189 |
| 101 | flkL | 304 | flkR | +0.0036 | 0.0174 |
| 93 | flkL | 304 | flkR | +0.0032 | 0.0217 |
| 245 | flkR | 304 | flkR | +0.0030 | 0.0469 |
| 276 | flkR | 304 | flkR | +0.0027 | 0.0449 |

### L4 H9 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | INTRA:flkL  |  cells: 6  |  total attr: +0.0189

**Key mass** (top-1=63%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 56 | flkL | +0.0119 | 63.1% |
| 59 | flkL | +0.0070 | 36.9% |

**Query mass** (top-1=42%, top-2=81%, top-3=91%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0080 | 42.3% |
| 124 | ss1 | +0.0073 | 38.6% |
| 119 | flkL | +0.0019 | 9.9% |
| 64 | flkL | +0.0017 | 9.2% |

**Offset distribution [frequency]** (top-2 coverage: 33%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +7 | 1 | 16.7% |
| +65 | 1 | 16.7% |
| +68 | 1 | 16.7% |
| +4 | 1 | 16.7% |
| +63 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=67%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 4 | 66.7% |
| ss1 | flkL | 2 | 33.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 63 | flkL | 56 | flkL | +0.0047 | 0.0114 |
| 124 | ss1 | 59 | flkL | +0.0037 | 0.0055 |
| 124 | ss1 | 56 | flkL | +0.0036 | 0.0036 |
| 63 | flkL | 59 | flkL | +0.0033 | 0.0106 |
| 119 | flkL | 56 | flkL | +0.0019 | 0.0062 |

### L7 H13 — Rank #19

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 20  |  total attr: +0.0702

**Key mass** (top-1=29%, top-2=43%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 301 | flkR | +0.0204 | 29.0% |
| 302 | flkR | +0.0100 | 14.2% |
| 300 | flkR | +0.0057 | 8.1% |
| 264 | flkR | +0.0052 | 7.4% |
| 97 | flkL | +0.0048 | 6.9% |

**Query mass** (top-1=14%, top-2=26%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 234 | ss2 | +0.0100 | 14.2% |
| 229 | ss2 | +0.0085 | 12.1% |
| 301 | flkR | +0.0054 | 7.7% |
| 104 | flkL | +0.0040 | 5.7% |
| 278 | flkR | +0.0038 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 3 | 15.0% |
| -21 | 2 | 10.0% |
| -68 | 1 | 5.0% |
| -72 | 1 | 5.0% |
| -18 | 1 | 5.0% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 6 | 30.0% |
| flkL | flkR | 3 | 15.0% |
| ss2 | flkR | 2 | 10.0% |
| flkL | ss1 | 2 | 10.0% |
| ss1 | flkL | 2 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 234 | ss2 | 302 | flkR | +0.0100 | 0.1355 |
| 229 | ss2 | 301 | flkR | +0.0085 | 0.1266 |
| 301 | flkR | 301 | flkR | +0.0054 | 0.3902 |
| 104 | flkL | 122 | ss1 | +0.0040 | 0.0057 |
| 278 | flkR | 301 | flkR | +0.0038 | 0.0641 |

### L8 H14 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | flkL→ss1  |  cells: 2  |  total attr: +0.2363

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss1 | +0.2343 | 99.2% |
| 115 | flkL | +0.0020 | 0.8% |

**Query mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.2363 | 100.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 1 | 50.0% |
| -11 | 1 | 50.0% |

**Region-pair profile** (q→k)  [flkL→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 1 | 50.0% |
| flkL | flkL | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 104 | flkL | 124 | ss1 | +0.2343 | 0.1015 |
| 104 | flkL | 115 | flkL | +0.0020 | 0.0022 |

### L9 H1 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 16  |  total attr: +0.0566

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.0566 | 100.0% |

**Query mass** (top-1=12%, top-2=24%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0069 | 12.3% |
| 125 | ss1 | +0.0069 | 12.2% |
| 123 | ss1 | +0.0065 | 11.4% |
| 119 | flkL | +0.0054 | 9.6% |
| 232 | ss2 | +0.0049 | 8.6% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +23 | 1 | 6.2% |
| +21 | 1 | 6.2% |
| +19 | 1 | 6.2% |
| +15 | 1 | 6.2% |
| +128 | 1 | 6.2% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 43.8% |
| ss1 | flkL | 6 | 37.5% |
| ss2 | flkL | 3 | 18.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 104 | flkL | +0.0069 | 0.1617 |
| 125 | ss1 | 104 | flkL | +0.0069 | 0.1579 |
| 123 | ss1 | 104 | flkL | +0.0065 | 0.1429 |
| 119 | flkL | 104 | flkL | +0.0054 | 0.1260 |
| 232 | ss2 | 104 | flkL | +0.0049 | 0.0685 |

### L10 H9 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss2→flkL  |  cells: 15  |  total attr: +0.1201

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.1201 | 100.0% |

**Query mass** (top-1=33%, top-2=49%, top-3=64%)  [DISTR(G104/A232/L63/V126)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.0394 | 32.8% |
| 232 | ss2 | +0.0190 | 15.8% |
| 63 | flkL | +0.0179 | 14.9% |
| 126 | ss1 | +0.0092 | 7.6% |
| 234 | ss2 | +0.0064 | 5.4% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 6.7% |
| +128 | 1 | 6.7% |
| -41 | 1 | 6.7% |
| +22 | 1 | 6.7% |
| +130 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 6 | 40.0% |
| flkL | flkL | 4 | 26.7% |
| ss1 | flkL | 4 | 26.7% |
| flkR | flkL | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 104 | flkL | 104 | flkL | +0.0394 | 0.1184 |
| 232 | ss2 | 104 | flkL | +0.0190 | 0.0885 |
| 63 | flkL | 104 | flkL | +0.0179 | 0.1993 |
| 126 | ss1 | 104 | flkL | +0.0092 | 0.1248 |
| 234 | ss2 | 104 | flkL | +0.0064 | 0.0500 |

### L11 H16 — Rank #4

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 35  |  total attr: +0.2771

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.2771 | 100.0% |

**Query mass** (top-1=21%, top-2=28%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0574 | 20.7% |
| 234 | ss2 | +0.0192 | 6.9% |
| 63 | flkL | +0.0188 | 6.8% |
| 128 | ss1 | +0.0164 | 5.9% |
| 126 | ss1 | +0.0147 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +128 | 1 | 2.9% |
| +130 | 1 | 2.9% |
| -41 | 1 | 2.9% |
| +24 | 1 | 2.9% |
| +22 | 1 | 2.9% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=54%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 19 | 54.3% |
| ss2 | flkL | 7 | 20.0% |
| ss1 | flkL | 6 | 17.1% |
| flkR | flkL | 2 | 5.7% |
| other | flkL | 1 | 2.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 232 | ss2 | 104 | flkL | +0.0574 | 0.2236 |
| 234 | ss2 | 104 | flkL | +0.0192 | 0.2387 |
| 63 | flkL | 104 | flkL | +0.0188 | 0.3217 |
| 128 | ss1 | 104 | flkL | +0.0164 | 0.2431 |
| 126 | ss1 | 104 | flkL | +0.0147 | 0.3174 |

### L12 H8 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkL  |  cells: 9  |  total attr: +0.0597

**Key mass** (top-1=90%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 63 | flkL | +0.0536 | 89.9% |
| 64 | flkL | +0.0060 | 10.1% |

**Query mass** (top-1=61%, top-2=71%, top-3=78%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.0366 | 61.3% |
| 128 | ss1 | +0.0061 | 10.1% |
| 126 | ss1 | +0.0040 | 6.7% |
| 233 | ss2 | +0.0033 | 5.5% |
| 119 | flkL | +0.0032 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +41 | 1 | 11.1% |
| +65 | 1 | 11.1% |
| +40 | 1 | 11.1% |
| +63 | 1 | 11.1% |
| +170 | 1 | 11.1% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 55.6% |
| ss1 | flkL | 2 | 22.2% |
| ss2 | flkL | 2 | 22.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 104 | flkL | 63 | flkL | +0.0305 | 0.2631 |
| 128 | ss1 | 63 | flkL | +0.0061 | 0.1681 |
| 104 | flkL | 64 | flkL | +0.0060 | 0.0672 |
| 126 | ss1 | 63 | flkL | +0.0040 | 0.1517 |
| 233 | ss2 | 63 | flkL | +0.0033 | 0.1268 |

### L13 H13 — Rank #27

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss2→flkL  |  cells: 15  |  total attr: +0.0716

**Key mass** (top-1=97%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.0698 | 97.4% |
| 123 | ss1 | +0.0019 | 2.6% |

**Query mass** (top-1=17%, top-2=30%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 68 | flkL | +0.0121 | 16.9% |
| 232 | ss2 | +0.0094 | 13.2% |
| 237 | ss2 | +0.0083 | 11.7% |
| 108 | flkL | +0.0062 | 8.7% |
| 236 | ss2 | +0.0060 | 8.4% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -36 | 1 | 6.7% |
| +128 | 1 | 6.7% |
| +133 | 1 | 6.7% |
| +4 | 1 | 6.7% |
| +132 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→flkL]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 6 | 40.0% |
| flkL | flkL | 5 | 33.3% |
| flkR | flkL | 3 | 20.0% |
| ss1 | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 68 | flkL | 104 | flkL | +0.0121 | 0.3549 |
| 232 | ss2 | 104 | flkL | +0.0094 | 0.2501 |
| 237 | ss2 | 104 | flkL | +0.0083 | 0.1546 |
| 108 | flkL | 104 | flkL | +0.0062 | 0.3221 |
| 236 | ss2 | 104 | flkL | +0.0060 | 0.1701 |

### L14 H9 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 40  |  total attr: +0.2783

**Key mass** (top-1=68%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.1885 | 67.8% |
| 63 | flkL | +0.0578 | 20.8% |
| 234 | ss2 | +0.0138 | 5.0% |
| 106 | flkL | +0.0091 | 3.3% |
| 261 | flkR | +0.0030 | 1.1% |

**Query mass** (top-1=26%, top-2=34%, top-3=42%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0727 | 26.1% |
| 233 | ss2 | +0.0229 | 8.2% |
| 237 | ss2 | +0.0226 | 8.1% |
| 238 | ss2 | +0.0220 | 7.9% |
| 236 | ss2 | +0.0171 | 6.2% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +169 | 2 | 5.0% |
| +128 | 1 | 2.5% |
| +133 | 1 | 2.5% |
| +134 | 1 | 2.5% |
| +129 | 1 | 2.5% |

**Region-pair profile** (q→k)  (top=28%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 11 | 27.5% |
| flkR | flkL | 9 | 22.5% |
| ss1 | flkL | 9 | 22.5% |
| flkL | flkL | 6 | 15.0% |
| ss2 | ss2 | 2 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 232 | ss2 | 104 | flkL | +0.0494 | 0.3663 |
| 232 | ss2 | 63 | flkL | +0.0233 | 0.1081 |
| 237 | ss2 | 104 | flkL | +0.0226 | 0.4195 |
| 238 | ss2 | 104 | flkL | +0.0220 | 0.4894 |
| 233 | ss2 | 104 | flkL | +0.0210 | 0.2574 |

### L14 H13 — Rank #11

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | ss1→flkL  |  cells: 18  |  total attr: +0.2489

**Key mass** (top-1=95%, top-2=97%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.2366 | 95.0% |
| 234 | ss2 | +0.0041 | 1.6% |
| 108 | flkL | +0.0033 | 1.3% |
| 117 | flkL | +0.0027 | 1.1% |
| 101 | flkL | +0.0022 | 0.9% |

**Query mass** (top-1=28%, top-2=53%, top-3=63%)  [DISTR(R119/A125/A128/E122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 119 | flkL | +0.0696 | 27.9% |
| 125 | ss1 | +0.0613 | 24.6% |
| 128 | ss1 | +0.0262 | 10.5% |
| 122 | ss1 | +0.0230 | 9.2% |
| 124 | ss1 | +0.0180 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +18 | 2 | 11.1% |
| +20 | 2 | 11.1% |
| +15 | 1 | 5.6% |
| +21 | 1 | 5.6% |
| +24 | 1 | 5.6% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 8 | 44.4% |
| flkL | flkL | 7 | 38.9% |
| ss2 | flkL | 2 | 11.1% |
| ss2 | ss2 | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 119 | flkL | 104 | flkL | +0.0647 | 0.3604 |
| 125 | ss1 | 104 | flkL | +0.0613 | 0.4663 |
| 122 | ss1 | 104 | flkL | +0.0230 | 0.4060 |
| 128 | ss1 | 104 | flkL | +0.0229 | 0.2941 |
| 124 | ss1 | 104 | flkL | +0.0180 | 0.3565 |

### L15 H12 — Rank #22

**Tags:** k:DISTRIBUTED / q:MULTI-ANCHOR  |  cells: 13  |  total attr: +0.0502

**Key mass** (top-1=37%, top-2=50%, top-3=61%)  [DISTR(A232/V124/L233/V126)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0186 | 37.1% |
| 124 | ss1 | +0.0063 | 12.6% |
| 233 | ss2 | +0.0058 | 11.5% |
| 126 | ss1 | +0.0051 | 10.1% |
| 125 | ss1 | +0.0048 | 9.5% |

**Query mass** (top-1=45%, top-2=64%, top-3=82%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 233 | ss2 | +0.0227 | 45.2% |
| 127 | ss1 | +0.0096 | 19.2% |
| 126 | ss1 | +0.0086 | 17.2% |
| 234 | ss2 | +0.0051 | 10.1% |
| 104 | flkL | +0.0025 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 46%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 23.1% |
| +2 | 3 | 23.1% |
| +0 | 2 | 15.4% |
| +3 | 1 | 7.7% |
| +22 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 38.5% |
| ss2 | ss2 | 3 | 23.1% |
| flkL | flkL | 2 | 15.4% |
| ss2 | flkR | 2 | 15.4% |
| ss1 | flkL | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 233 | ss2 | 232 | ss2 | +0.0136 | 0.1132 |
| 233 | ss2 | 233 | ss2 | +0.0058 | 0.0378 |
| 127 | ss1 | 126 | ss1 | +0.0051 | 0.0438 |
| 234 | ss2 | 232 | ss2 | +0.0051 | 0.0902 |
| 126 | ss1 | 124 | ss1 | +0.0035 | 0.0291 |

### L15 H13 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss2  |  cells: 17  |  total attr: +0.0479

**Key mass** (top-1=24%, top-2=46%, top-3=63%)  [DISTR(L233/A232/I234/R119)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 233 | ss2 | +0.0115 | 24.1% |
| 232 | ss2 | +0.0104 | 21.8% |
| 234 | ss2 | +0.0081 | 16.9% |
| 119 | flkL | +0.0058 | 12.0% |
| 262 | flkR | +0.0040 | 8.2% |

**Query mass** (top-1=46%, top-2=60%, top-3=72%)  [DISTR(L233/I234/D228)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 233 | ss2 | +0.0221 | 46.1% |
| 234 | ss2 | +0.0067 | 14.0% |
| 228 | ss2 | +0.0058 | 12.1% |
| 128 | ss1 | +0.0051 | 10.7% |
| 127 | ss1 | +0.0024 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 2 | 11.8% |
| -28 | 2 | 11.8% |
| +0 | 1 | 5.9% |
| +4 | 1 | 5.9% |
| -6 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 9 | 52.9% |
| ss2 | flkR | 4 | 23.5% |
| ss1 | flkL | 3 | 17.6% |
| ss1 | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 233 | ss2 | 233 | ss2 | +0.0069 | 0.0437 |
| 233 | ss2 | 232 | ss2 | +0.0058 | 0.0423 |
| 128 | ss1 | 124 | ss1 | +0.0035 | 0.0907 |
| 228 | ss2 | 234 | ss2 | +0.0033 | 0.0887 |
| 233 | ss2 | 234 | ss2 | +0.0028 | 0.0203 |

### L16 H2 — Rank #24

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | CROSS:ss2→flkL  |  cells: 12  |  total attr: +0.0391

**Key mass** (top-1=39%, top-2=70%, top-3=82%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 257 | flkR | +0.0151 | 38.5% |
| 104 | flkL | +0.0122 | 31.1% |
| 68 | flkL | +0.0050 | 12.8% |
| 67 | flkL | +0.0026 | 6.6% |
| 105 | flkL | +0.0023 | 5.8% |

**Query mass** (top-1=46%, top-2=65%, top-3=79%)  [DISTR(G237/A232/E122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0179 | 45.7% |
| 232 | ss2 | +0.0074 | 19.0% |
| 122 | ss1 | +0.0057 | 14.7% |
| 234 | ss2 | +0.0023 | 5.9% |
| 235 | ss2 | +0.0020 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 17%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -20 | 1 | 8.3% |
| +133 | 1 | 8.3% |
| -25 | 1 | 8.3% |
| +54 | 1 | 8.3% |
| +128 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→flkL]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 5 | 41.7% |
| ss2 | flkR | 4 | 33.3% |
| ss1 | flkL | 2 | 16.7% |
| flkL | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 237 | ss2 | 257 | flkR | +0.0086 | 0.1394 |
| 237 | ss2 | 104 | flkL | +0.0049 | 0.1863 |
| 232 | ss2 | 257 | flkR | +0.0044 | 0.1733 |
| 122 | ss1 | 68 | flkL | +0.0032 | 0.0906 |
| 232 | ss2 | 104 | flkL | +0.0030 | 0.1267 |

### L16 H7 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 27  |  total attr: +0.2902

**Key mass** (top-1=93%, top-2=96%, top-3=97%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.2686 | 92.6% |
| 127 | ss1 | +0.0092 | 3.2% |
| 105 | flkL | +0.0046 | 1.6% |
| 108 | flkL | +0.0032 | 1.1% |
| 257 | flkR | +0.0029 | 1.0% |

**Query mass** (top-1=15%, top-2=26%, top-3=37%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss1 | +0.0424 | 14.6% |
| 232 | ss2 | +0.0335 | 11.5% |
| 130 | ss1 | +0.0305 | 10.5% |
| 127 | ss1 | +0.0302 | 10.4% |
| 129 | ss1 | +0.0274 | 9.4% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 7.4% |
| +20 | 1 | 3.7% |
| +26 | 1 | 3.7% |
| +23 | 1 | 3.7% |
| +25 | 1 | 3.7% |

**Region-pair profile** (q→k)  (top=30%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 8 | 29.6% |
| ss1 | flkL | 7 | 25.9% |
| ss2 | flkL | 4 | 14.8% |
| ss2 | ss1 | 2 | 7.4% |
| other | flkL | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 124 | ss1 | 104 | flkL | +0.0424 | 0.8057 |
| 130 | ss1 | 104 | flkL | +0.0305 | 0.7622 |
| 127 | ss1 | 104 | flkL | +0.0281 | 0.6754 |
| 129 | ss1 | 104 | flkL | +0.0274 | 0.7509 |
| 232 | ss2 | 104 | flkL | +0.0257 | 0.2009 |

### L17 H7 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 21  |  total attr: +0.0952

**Key mass** (top-1=61%, top-2=91%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.0583 | 61.3% |
| 232 | ss2 | +0.0281 | 29.5% |
| 127 | ss1 | +0.0037 | 3.8% |
| 233 | ss2 | +0.0017 | 1.8% |
| 105 | flkL | +0.0017 | 1.8% |

**Query mass** (top-1=16%, top-2=29%, top-3=39%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0157 | 16.5% |
| 119 | flkL | +0.0120 | 12.6% |
| 242 | flkR | +0.0095 | 10.0% |
| 128 | ss1 | +0.0089 | 9.4% |
| 125 | ss1 | +0.0063 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +13 | 3 | 14.3% |
| +22 | 2 | 9.5% |
| +19 | 2 | 9.5% |
| +20 | 2 | 9.5% |
| +23 | 1 | 4.8% |

**Region-pair profile** (q→k)  (top=33%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 7 | 33.3% |
| flkR | ss2 | 7 | 33.3% |
| flkL | flkL | 4 | 19.0% |
| ss2 | ss1 | 1 | 4.8% |
| ss2 | flkL | 1 | 4.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 104 | flkL | +0.0123 | 0.2403 |
| 119 | flkL | 104 | flkL | +0.0120 | 0.4252 |
| 242 | flkR | 232 | ss2 | +0.0095 | 0.2870 |
| 128 | ss1 | 104 | flkL | +0.0089 | 0.1171 |
| 125 | ss1 | 104 | flkL | +0.0063 | 0.1712 |

### L20 H4 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:flkL  |  cells: 8  |  total attr: +0.0357

**Key mass** (top-1=26%, top-2=51%, top-3=63%)  [DISTR(G104/A112/L233/A232)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | flkL | +0.0092 | 25.8% |
| 112 | flkL | +0.0091 | 25.5% |
| 233 | ss2 | +0.0042 | 11.8% |
| 232 | ss2 | +0.0038 | 10.7% |
| 238 | ss2 | +0.0037 | 10.5% |

**Query mass** (top-1=28%, top-2=54%, top-3=71%)  [DISTR(G237/A121/R119)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0100 | 28.2% |
| 121 | flkL | +0.0092 | 25.8% |
| 119 | flkL | +0.0061 | 17.2% |
| 236 | ss2 | +0.0037 | 10.5% |
| 88 | flkL | +0.0036 | 10.1% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 25.0% |
| +5 | 2 | 25.0% |
| +17 | 1 | 12.5% |
| +7 | 1 | 12.5% |
| -2 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 4 | 50.0% |
| ss2 | ss2 | 4 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 121 | flkL | 104 | flkL | +0.0092 | 0.4593 |
| 119 | flkL | 112 | flkL | +0.0061 | 0.2143 |
| 237 | ss2 | 233 | ss2 | +0.0042 | 0.0966 |
| 237 | ss2 | 232 | ss2 | +0.0038 | 0.0868 |
| 236 | ss2 | 238 | ss2 | +0.0037 | 0.1547 |

### L21 H4 — Rank #21

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss2  |  cells: 17  |  total attr: +0.0790

**Key mass** (top-1=23%, top-2=46%, top-3=68%)  [DISTR(I234/V124/A232/I127)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 234 | ss2 | +0.0182 | 23.0% |
| 124 | ss1 | +0.0179 | 22.6% |
| 232 | ss2 | +0.0173 | 22.0% |
| 127 | ss1 | +0.0107 | 13.5% |
| 233 | ss2 | +0.0057 | 7.3% |

**Query mass** (top-1=23%, top-2=42%, top-3=55%)  [DISTR(E122/G237/A232/I234/A125)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0179 | 22.6% |
| 237 | ss2 | +0.0154 | 19.5% |
| 232 | ss2 | +0.0105 | 13.2% |
| 234 | ss2 | +0.0080 | 10.1% |
| 125 | ss1 | +0.0065 | 8.2% |

**Offset distribution [frequency]** (top-2 coverage: 41%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 4 | 23.5% |
| -1 | 3 | 17.6% |
| -3 | 2 | 11.8% |
| +0 | 2 | 11.8% |
| +1 | 2 | 11.8% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=53%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 9 | 52.9% |
| ss1 | ss1 | 7 | 41.2% |
| flkL | flkL | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 124 | ss1 | +0.0179 | 0.5720 |
| 237 | ss2 | 234 | ss2 | +0.0100 | 0.1683 |
| 232 | ss2 | 234 | ss2 | +0.0082 | 0.2089 |
| 234 | ss2 | 232 | ss2 | +0.0058 | 0.3180 |
| 231 | ss2 | 232 | ss2 | +0.0058 | 0.1370 |

### L23 H18 — Rank #15

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss2  |  cells: 23  |  total attr: +0.1156

**Key mass** (top-1=42%, top-2=67%, top-3=75%)  [DISTR(D228/V124/G229)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 228 | ss2 | +0.0486 | 42.0% |
| 124 | ss1 | +0.0292 | 25.3% |
| 229 | ss2 | +0.0092 | 7.9% |
| 231 | ss2 | +0.0088 | 7.6% |
| 230 | ss2 | +0.0071 | 6.2% |

**Query mass** (top-1=28%, top-2=44%, top-3=59%)  [DISTR(G229/A128/V231/G237/A129)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 229 | ss2 | +0.0320 | 27.7% |
| 128 | ss1 | +0.0187 | 16.2% |
| 231 | ss2 | +0.0177 | 15.3% |
| 237 | ss2 | +0.0079 | 6.8% |
| 129 | ss1 | +0.0066 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 30%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +6 | 4 | 17.4% |
| +5 | 3 | 13.0% |
| +1 | 2 | 8.7% |
| +3 | 2 | 8.7% |
| -4 | 2 | 8.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=70%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 16 | 69.6% |
| ss1 | ss1 | 3 | 13.0% |
| ss1 | flkL | 2 | 8.7% |
| other | ss2 | 1 | 4.3% |
| flkL | flkL | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 229 | ss2 | 228 | ss2 | +0.0246 | 0.5614 |
| 128 | ss1 | 124 | ss1 | +0.0187 | 0.5347 |
| 231 | ss2 | 228 | ss2 | +0.0127 | 0.5236 |
| 129 | ss1 | 124 | ss1 | +0.0066 | 0.7081 |
| 231 | ss2 | 230 | ss2 | +0.0051 | 0.2142 |

### L25 H16 — Rank #7

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 17  |  total attr: +0.1635

**Key mass** (top-1=27%, top-2=49%, top-3=65%)  [DISTR(V235/D228/V124/E122)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 235 | ss2 | +0.0448 | 27.4% |
| 228 | ss2 | +0.0354 | 21.7% |
| 124 | ss1 | +0.0254 | 15.5% |
| 122 | ss1 | +0.0133 | 8.1% |
| 234 | ss2 | +0.0103 | 6.3% |

**Query mass** (top-1=30%, top-2=54%, top-3=71%)  [DISTR(I234/L233/E122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 234 | ss2 | +0.0490 | 30.0% |
| 233 | ss2 | +0.0385 | 23.5% |
| 122 | ss1 | +0.0289 | 17.6% |
| 121 | flkL | +0.0133 | 8.1% |
| 226 | other | +0.0093 | 5.7% |

**Offset distribution [frequency]** (top-2 coverage: 82%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 10 | 58.8% |
| -2 | 4 | 23.5% |
| +5 | 1 | 5.9% |
| -14 | 1 | 5.9% |
| +0 | 1 | 5.9% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 7 | 41.2% |
| ss1 | ss1 | 3 | 17.6% |
| flkL | flkL | 2 | 11.8% |
| ss2 | flkR | 2 | 11.8% |
| flkL | ss1 | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 234 | ss2 | 235 | ss2 | +0.0448 | 0.5082 |
| 233 | ss2 | 228 | ss2 | +0.0282 | 0.5957 |
| 122 | ss1 | 124 | ss1 | +0.0237 | 0.2015 |
| 121 | flkL | 122 | ss1 | +0.0133 | 0.4498 |
| 233 | ss2 | 234 | ss2 | +0.0103 | 0.2490 |

### L26 H3 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 17  |  total attr: +0.1211

**Key mass** (top-1=31%, top-2=52%, top-3=65%)  [DISTR(V124/D228/I234/A246)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 124 | ss1 | +0.0372 | 30.7% |
| 228 | ss2 | +0.0255 | 21.0% |
| 234 | ss2 | +0.0162 | 13.4% |
| 246 | flkR | +0.0098 | 8.1% |
| 235 | ss2 | +0.0075 | 6.2% |

**Query mass** (top-1=24%, top-2=42%, top-3=55%)  [DISTR(V231/A128/G237/I127/A242)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 231 | ss2 | +0.0289 | 23.8% |
| 128 | ss1 | +0.0221 | 18.3% |
| 237 | ss2 | +0.0162 | 13.4% |
| 127 | ss1 | +0.0151 | 12.5% |
| 242 | flkR | +0.0097 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 65%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 6 | 35.3% |
| -3 | 5 | 29.4% |
| +4 | 4 | 23.5% |
| -4 | 2 | 11.8% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 7 | 41.2% |
| ss1 | ss1 | 3 | 17.6% |
| flkR | flkR | 3 | 17.6% |
| flkL | flkL | 3 | 17.6% |
| ss1 | flkL | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 128 | ss1 | 124 | ss1 | +0.0221 | 0.4149 |
| 231 | ss2 | 228 | ss2 | +0.0214 | 0.2671 |
| 237 | ss2 | 234 | ss2 | +0.0162 | 0.3462 |
| 127 | ss1 | 124 | ss1 | +0.0151 | 0.5353 |
| 242 | flkR | 246 | flkR | +0.0076 | 0.4637 |

### L26 H16 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | ss1→flkL  |  cells: 26  |  total attr: +0.1598

**Key mass** (top-1=30%, top-2=45%, top-3=54%)  [DISTR(V231/I64/Q61/L63/A121)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 231 | ss2 | +0.0473 | 29.6% |
| 64 | flkL | +0.0241 | 15.1% |
| 61 | flkL | +0.0156 | 9.8% |
| 63 | flkL | +0.0135 | 8.5% |
| 121 | flkL | +0.0133 | 8.3% |

**Query mass** (top-1=38%, top-2=61%, top-3=77%)  [DISTR(A128/I127/G237)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 128 | ss1 | +0.0602 | 37.7% |
| 127 | ss1 | +0.0379 | 23.7% |
| 237 | ss2 | +0.0248 | 15.5% |
| 122 | ss1 | +0.0156 | 9.8% |
| 61 | flkL | +0.0047 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 23%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +61 | 4 | 15.4% |
| +63 | 2 | 7.7% |
| +64 | 2 | 7.7% |
| +62 | 2 | 7.7% |
| -103 | 1 | 3.8% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 11 | 42.3% |
| ss2 | flkL | 5 | 19.2% |
| ss1 | ss2 | 4 | 15.4% |
| ss2 | ss1 | 3 | 11.5% |
| flkL | ss1 | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 128 | ss1 | 231 | ss2 | +0.0402 | 0.2041 |
| 122 | ss1 | 61 | flkL | +0.0156 | 0.4725 |
| 127 | ss1 | 64 | flkL | +0.0151 | 0.1423 |
| 237 | ss2 | 121 | flkL | +0.0133 | 0.1394 |
| 127 | ss1 | 63 | flkL | +0.0081 | 0.0824 |

### L27 H15 — Rank #1

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 27  |  total attr: +0.2237

**Key mass** (top-1=23%, top-2=34%, top-3=43%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 128 | ss1 | +0.0510 | 22.8% |
| 122 | ss1 | +0.0258 | 11.5% |
| 125 | ss1 | +0.0186 | 8.3% |
| 127 | ss1 | +0.0186 | 8.3% |
| 123 | ss1 | +0.0181 | 8.1% |

**Query mass** (top-1=22%, top-2=39%, top-3=49%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 231 | ss2 | +0.0502 | 22.5% |
| 237 | ss2 | +0.0373 | 16.7% |
| 232 | ss2 | +0.0223 | 10.0% |
| 234 | ss2 | +0.0212 | 9.5% |
| 122 | ss1 | +0.0203 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +107 | 2 | 7.4% |
| +111 | 2 | 7.4% |
| +106 | 2 | 7.4% |
| -111 | 2 | 7.4% |
| +103 | 1 | 3.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=56%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 15 | 55.6% |
| ss1 | ss2 | 7 | 25.9% |
| ss1 | flkL | 3 | 11.1% |
| ss2 | ss2 | 1 | 3.7% |
| ss2 | flkL | 1 | 3.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 231 | ss2 | 128 | ss1 | +0.0428 | 0.1807 |
| 237 | ss2 | 122 | ss1 | +0.0258 | 0.1245 |
| 126 | ss1 | 233 | ss2 | +0.0137 | 0.3625 |
| 234 | ss2 | 125 | ss1 | +0.0130 | 0.1914 |
| 232 | ss2 | 127 | ss1 | +0.0122 | 0.0580 |

### L29 H18 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.2112

**Key mass** (top-1=23%, top-2=39%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0495 | 23.4% |
| 234 | ss2 | +0.0324 | 15.3% |
| 237 | ss2 | +0.0262 | 12.4% |
| 236 | ss2 | +0.0110 | 5.2% |
| 116 | flkL | +0.0089 | 4.2% |

**Query mass** (top-1=28%, top-2=42%, top-3=54%)  [DISTR(I127/E122/A128/A125/A232)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0587 | 27.8% |
| 122 | ss1 | +0.0298 | 14.1% |
| 128 | ss1 | +0.0250 | 11.8% |
| 125 | ss1 | +0.0245 | 11.6% |
| 232 | ss2 | +0.0163 | 7.7% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +121 | 2 | 6.5% |
| +126 | 2 | 6.5% |
| -105 | 1 | 3.2% |
| -115 | 1 | 3.2% |
| -109 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | flkL | 8 | 25.8% |
| ss1 | ss2 | 7 | 22.6% |
| ss1 | flkL | 7 | 22.6% |
| ss2 | ss1 | 4 | 12.9% |
| flkL | flkL | 2 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 232 | ss2 | +0.0495 | 0.3837 |
| 122 | ss1 | 237 | ss2 | +0.0262 | 0.2431 |
| 125 | ss1 | 234 | ss2 | +0.0226 | 0.5801 |
| 123 | ss1 | 236 | ss2 | +0.0110 | 0.2840 |
| 128 | ss1 | 128 | ss1 | +0.0077 | 0.0864 |

### L30 H0 — Rank #16

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 7  |  total attr: +0.0352

**Key mass** (top-1=35%, top-2=65%, top-3=84%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0124 | 35.1% |
| 128 | ss1 | +0.0104 | 29.5% |
| 237 | ss2 | +0.0066 | 18.9% |
| 232 | ss2 | +0.0038 | 10.7% |
| 129 | ss1 | +0.0020 | 5.8% |

**Query mass** (top-1=30%, top-2=58%, top-3=77%)  [DISTR(A232/V231/E122)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0105 | 29.9% |
| 231 | ss2 | +0.0101 | 28.6% |
| 122 | ss1 | +0.0066 | 18.9% |
| 127 | ss1 | +0.0038 | 10.7% |
| 128 | ss1 | +0.0024 | 6.7% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +105 | 1 | 14.3% |
| +103 | 1 | 14.3% |
| -115 | 1 | 14.3% |
| -105 | 1 | 14.3% |
| +0 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 57.1% |
| ss1 | ss2 | 2 | 28.6% |
| ss1 | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 232 | ss2 | 127 | ss1 | +0.0105 | 0.2670 |
| 231 | ss2 | 128 | ss1 | +0.0080 | 0.1167 |
| 122 | ss1 | 237 | ss2 | +0.0066 | 0.1255 |
| 127 | ss1 | 232 | ss2 | +0.0038 | 0.0545 |
| 128 | ss1 | 128 | ss1 | +0.0024 | 0.1520 |

### L30 H1 — Rank #12

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | CROSS:ss2→ss1  |  cells: 8  |  total attr: +0.0668

**Key mass** (top-1=48%, top-2=64%, top-3=77%)  [DISTR(A232/I127/A128)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 232 | ss2 | +0.0321 | 48.1% |
| 127 | ss1 | +0.0109 | 16.4% |
| 128 | ss1 | +0.0080 | 12.1% |
| 122 | ss1 | +0.0072 | 10.7% |
| 231 | ss2 | +0.0067 | 10.0% |

**Query mass** (top-1=58%, top-2=72%, top-3=84%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0388 | 58.1% |
| 231 | ss2 | +0.0095 | 14.3% |
| 232 | ss2 | +0.0076 | 11.4% |
| 237 | ss2 | +0.0072 | 10.7% |
| 123 | ss1 | +0.0018 | 2.7% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -105 | 1 | 12.5% |
| +105 | 1 | 12.5% |
| +115 | 1 | 12.5% |
| -104 | 1 | 12.5% |
| +103 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 5 | 62.5% |
| ss1 | ss2 | 3 | 37.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 127 | ss1 | 232 | ss2 | +0.0321 | 0.1964 |
| 232 | ss2 | 127 | ss1 | +0.0076 | 0.0492 |
| 237 | ss2 | 122 | ss1 | +0.0072 | 0.0439 |
| 127 | ss1 | 231 | ss2 | +0.0067 | 0.1639 |
| 231 | ss2 | 128 | ss1 | +0.0063 | 0.0403 |

### L31 H17 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 16  |  total attr: +0.0823

**Key mass** (top-1=60%, top-2=69%, top-3=77%)  [DISTR(?-1/?425/Q61)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.0492 | 59.8% |
| 425 | other | +0.0073 | 8.9% |
| 61 | flkL | +0.0071 | 8.7% |
| 128 | ss1 | +0.0052 | 6.3% |
| 239 | flkR | +0.0044 | 5.3% |

**Query mass** (top-1=40%, top-2=56%, top-3=70%)  [DISTR(E122/G237/Q61/V231)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0329 | 40.0% |
| 237 | ss2 | +0.0130 | 15.8% |
| 61 | flkL | +0.0116 | 14.1% |
| 231 | ss2 | +0.0108 | 13.1% |
| 127 | ss1 | +0.0084 | 10.2% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +123 | 1 | 6.2% |
| +128 | 1 | 6.2% |
| +176 | 1 | 6.2% |
| +62 | 1 | 6.2% |
| +103 | 1 | 6.2% |

**Region-pair profile** (q→k)  (top=25%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | other | 4 | 25.0% |
| flkL | other | 3 | 18.8% |
| ss2 | other | 3 | 18.8% |
| ss2 | flkL | 2 | 12.5% |
| ss2 | ss1 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | -1 | other | +0.0256 | 0.2094 |
| 127 | ss1 | -1 | other | +0.0084 | 0.1215 |
| 237 | ss2 | 61 | flkL | +0.0071 | 0.0305 |
| 61 | flkL | -1 | other | +0.0059 | 0.1284 |
| 231 | ss2 | 128 | ss1 | +0.0052 | 0.0531 |

### L32 H0 — Rank #29

**Tags:** k:MULTI-ANCHOR / q:MULTI-ANCHOR | CROSS:ss2→ss1  |  cells: 5  |  total attr: +0.0184

**Key mass** (top-1=35%, top-2=62%, top-3=84%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 127 | ss1 | +0.0063 | 34.5% |
| 237 | ss2 | +0.0050 | 27.4% |
| 128 | ss1 | +0.0041 | 22.5% |
| 122 | ss1 | +0.0029 | 15.5% |

**Query mass** (top-1=34%, top-2=61%, top-3=84%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 231 | ss2 | +0.0062 | 33.7% |
| 122 | ss1 | +0.0050 | 27.4% |
| 232 | ss2 | +0.0043 | 23.4% |
| 237 | ss2 | +0.0029 | 15.5% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 1 | 20.0% |
| +105 | 1 | 20.0% |
| +103 | 1 | 20.0% |
| +115 | 1 | 20.0% |
| +104 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=80%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 80.0% |
| ss1 | ss2 | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 122 | ss1 | 237 | ss2 | +0.0050 | 0.0286 |
| 232 | ss2 | 127 | ss1 | +0.0043 | 0.0242 |
| 231 | ss2 | 128 | ss1 | +0.0041 | 0.0225 |
| 237 | ss2 | 122 | ss1 | +0.0029 | 0.0162 |
| 231 | ss2 | 127 | ss1 | +0.0021 | 0.0236 |

### L32 H13 — Rank #10

**Tags:** k:MULTI-ANCHOR / q:DUAL-ANCHOR | CROSS:ss2→ss1  |  cells: 7  |  total attr: +0.0585

**Key mass** (top-1=53%, top-2=69%, top-3=81%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 122 | ss1 | +0.0309 | 52.8% |
| 237 | ss2 | +0.0093 | 15.8% |
| 231 | ss2 | +0.0070 | 11.9% |
| 123 | ss1 | +0.0043 | 7.4% |
| 128 | ss1 | +0.0041 | 7.0% |

**Query mass** (top-1=57%, top-2=73%, top-3=85%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0336 | 57.4% |
| 122 | ss1 | +0.0093 | 15.8% |
| 128 | ss1 | +0.0070 | 11.9% |
| 231 | ss2 | +0.0041 | 7.0% |
| 127 | ss1 | +0.0029 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +115 | 1 | 14.3% |
| -115 | 1 | 14.3% |
| -103 | 1 | 14.3% |
| +103 | 1 | 14.3% |
| -105 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 57.1% |
| ss1 | ss2 | 3 | 42.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 237 | ss2 | 122 | ss1 | +0.0309 | 0.1288 |
| 122 | ss1 | 237 | ss2 | +0.0093 | 0.0387 |
| 128 | ss1 | 231 | ss2 | +0.0070 | 0.0282 |
| 231 | ss2 | 128 | ss1 | +0.0041 | 0.0166 |
| 127 | ss1 | 232 | ss2 | +0.0029 | 0.0124 |

### L32 H18 — Rank #2

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 14  |  total attr: +0.1496

**Key mass** (top-1=21%, top-2=42%, top-3=61%)  [DISTR(V231/A128/E122/I127/G237)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 231 | ss2 | +0.0318 | 21.3% |
| 128 | ss1 | +0.0310 | 20.7% |
| 122 | ss1 | +0.0289 | 19.3% |
| 127 | ss1 | +0.0130 | 8.7% |
| 237 | ss2 | +0.0129 | 8.6% |

**Query mass** (top-1=22%, top-2=42%, top-3=60%)  [DISTR(G237/V231/A128/E122/I234)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 237 | ss2 | +0.0327 | 21.9% |
| 231 | ss2 | +0.0294 | 19.6% |
| 128 | ss1 | +0.0281 | 18.7% |
| 122 | ss1 | +0.0129 | 8.6% |
| 234 | ss2 | +0.0117 | 7.8% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +115 | 1 | 7.1% |
| -103 | 1 | 7.1% |
| +103 | 1 | 7.1% |
| -115 | 1 | 7.1% |
| +105 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 8 | 57.1% |
| ss1 | ss2 | 6 | 42.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 237 | ss2 | 122 | ss1 | +0.0289 | 0.0734 |
| 128 | ss1 | 231 | ss2 | +0.0281 | 0.0693 |
| 231 | ss2 | 128 | ss1 | +0.0270 | 0.0668 |
| 122 | ss1 | 237 | ss2 | +0.0129 | 0.0327 |
| 232 | ss2 | 127 | ss1 | +0.0106 | 0.0272 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #30 | L0 | H8 | 8 | +0.0238 | SINGLE-ANCHOR | G304 | DISTRIBUTED | F296/G101/F93/F245/G276 |  | INTRA:flkR |
| #28 | L4 | H9 | 6 | +0.0189 | SINGLE-ANCHOR | K56 | DUAL-ANCHOR | L63/V124 |  | INTRA:flkL |
| #19 | L7 | H13 | 20 | +0.0702 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #3 | L8 | H14 | 2 | +0.2363 | SINGLE-ANCHOR | V124 | SINGLE-ANCHOR | G104 |  | flkL→ss1 |
| #20 | L9 | H1 | 16 | +0.0566 | SINGLE-ANCHOR | G104 | DISTRIBUTED |  |  | INTRA:flkL |
| #9 | L10 | H9 | 15 | +0.1201 | SINGLE-ANCHOR | G104 | DISTRIBUTED | G104/A232/L63/V126 |  | CROSS:ss2→flkL |
| #4 | L11 | H16 | 35 | +0.2771 | SINGLE-ANCHOR | G104 | DISTRIBUTED |  |  | INTRA:flkL |
| #18 | L12 | H8 | 9 | +0.0597 | SINGLE-ANCHOR | L63 | SINGLE-ANCHOR | G104 |  | INTRA:flkL |
| #27 | L13 | H13 | 15 | +0.0716 | SINGLE-ANCHOR | G104 | DISTRIBUTED |  |  | CROSS:ss2→flkL |
| #8 | L14 | H9 | 40 | +0.2783 | SINGLE-ANCHOR | G104 | DISTRIBUTED |  |  |  |
| #11 | L14 | H13 | 18 | +0.2489 | SINGLE-ANCHOR | G104 | DISTRIBUTED | R119/A125/A128/E122 |  | ss1→flkL |
| #22 | L15 | H12 | 13 | +0.0502 | DISTRIBUTED | A232/V124/L233/V126 | MULTI-ANCHOR |  |  |  |
| #25 | L15 | H13 | 17 | +0.0479 | DISTRIBUTED | L233/A232/I234/R119 | DISTRIBUTED | L233/I234/D228 |  | INTRA:ss2 |
| #24 | L16 | H2 | 12 | +0.0391 | MULTI-ANCHOR |  | DISTRIBUTED | G237/A232/E122 |  | CROSS:ss2→flkL |
| #14 | L16 | H7 | 27 | +0.2902 | SINGLE-ANCHOR | G104 | DISTRIBUTED |  |  |  |
| #26 | L17 | H7 | 21 | +0.0952 | SINGLE-ANCHOR | G104 | DISTRIBUTED |  |  |  |
| #23 | L20 | H4 | 8 | +0.0357 | DISTRIBUTED | G104/A112/L233/A232 | DISTRIBUTED | G237/A121/R119 | POSITIONAL | INTRA:flkL |
| #21 | L21 | H4 | 17 | +0.0790 | DISTRIBUTED | I234/V124/A232/I127 | DISTRIBUTED | E122/G237/A232/I234/A125 |  | INTRA:ss2 |
| #15 | L23 | H18 | 23 | +0.1156 | DISTRIBUTED | D228/V124/G229 | DISTRIBUTED | G229/A128/V231/G237/A129 |  | INTRA:ss2 |
| #7 | L25 | H16 | 17 | +0.1635 | DISTRIBUTED | V235/D228/V124/E122 | DISTRIBUTED | I234/L233/E122 | POSITIONAL | INTRA:ss2 |
| #17 | L26 | H3 | 17 | +0.1211 | DISTRIBUTED | V124/D228/I234/A246 | DISTRIBUTED | V231/A128/G237/I127/A242 | POSITIONAL | INTRA:ss2 |
| #6 | L26 | H16 | 26 | +0.1598 | DISTRIBUTED | V231/I64/Q61/L63/A121 | DISTRIBUTED | A128/I127/G237 |  | ss1→flkL |
| #1 | L27 | H15 | 27 | +0.2237 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #5 | L29 | H18 | 31 | +0.2112 | DISTRIBUTED |  | DISTRIBUTED | I127/E122/A128/A125/A232 |  |  |
| #16 | L30 | H0 | 7 | +0.0352 | MULTI-ANCHOR |  | DISTRIBUTED | A232/V231/E122 |  | CROSS:ss2→ss1 |
| #12 | L30 | H1 | 8 | +0.0668 | DISTRIBUTED | A232/I127/A128 | DUAL-ANCHOR | I127/V231 |  | CROSS:ss2→ss1 |
| #13 | L31 | H17 | 16 | +0.0823 | DISTRIBUTED | ?-1/?425/Q61 | DISTRIBUTED | E122/G237/Q61/V231 |  |  |
| #29 | L32 | H0 | 5 | +0.0184 | MULTI-ANCHOR |  | MULTI-ANCHOR |  |  | CROSS:ss2→ss1 |
| #10 | L32 | H13 | 7 | +0.0585 | MULTI-ANCHOR |  | DUAL-ANCHOR | G237/E122 |  | CROSS:ss2→ss1 |
| #2 | L32 | H18 | 14 | +0.1496 | DISTRIBUTED | V231/A128/E122/I127/G237 | DISTRIBUTED | G237/V231/A128/E122/I234 |  | CROSS:ss2→ss1 |
