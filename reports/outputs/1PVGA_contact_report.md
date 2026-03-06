# Contact Pattern Analysis: 1PVGA

Generated: 2026-02-24 23:47:38   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1PVGA |
| Contact pair | (101, 202) |
| ss1 | [96, 107) |
| ss2 | [197, 208) |
| Clean flank | 65 |
| Corrupt flank | 63 |
| Segment radius | 5 |
| Faith target | 70% |
| Model dims | 33L × 20H, head_dim=64 |
| topk_cell | 1000 |
| topk_heads | 30 |

## Baselines

| Metric | Value |
|--------|-------|
| Clean metric | 0.8647 |
| Corrupt metric | 0.0644 |
| Gap | 0.8003 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 242 | 72.27% |
| positive IE | 65 | 71.58% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L10 | H9 | +0.2404 |
| 2 | L9 | H17 | +0.1837 |
| 3 | L32 | H13 | +0.1514 |
| 4 | L32 | H18 | +0.1312 |
| 5 | L27 | H15 | +0.1241 |
| 6 | L29 | H18 | +0.1215 |
| 7 | L17 | H10 | +0.0785 |
| 8 | L11 | H16 | +0.0623 |
| 9 | L7 | H7 | +0.0583 |
| 10 | L5 | H9 | +0.0559 |
| 11 | L12 | H10 | +0.0524 |
| 12 | L7 | H13 | +0.0511 |
| 13 | L26 | H16 | +0.0428 |
| 14 | L11 | H14 | +0.0399 |
| 15 | L6 | H0 | +0.0386 |
| 16 | L16 | H7 | +0.0376 |
| 17 | L0 | H12 | +0.0354 |
| 18 | L13 | H2 | +0.0296 |
| 19 | L17 | H18 | +0.0296 |
| 20 | L14 | H4 | +0.0258 |
| 21 | L7 | H18 | +0.0250 |
| 22 | L3 | H7 | +0.0224 |
| 23 | L14 | H9 | +0.0223 |
| 24 | L16 | H12 | +0.0222 |
| 25 | L19 | H3 | +0.0221 |
| 26 | L8 | H2 | +0.0219 |
| 27 | L4 | H14 | +0.0212 |
| 28 | L11 | H8 | +0.0205 |
| 29 | L15 | H8 | +0.0203 |
| 30 | L17 | H7 | +0.0203 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | 0.00% |
| 3 | 0.50% |
| 4 | 0.67% |
| 5 | 1.60% |
| 6 | 3.20% |
| 7 | 3.35% |
| 8 | 4.30% |
| 9 | 4.44% |
| 10 | 5.95% |
| 20 | 16.54% |
| 80 | 85.01% |
| 177 | 115.87% |
| 277 | 131.07% |
| 460 | 131.25% |

## Cell Attribution Analysis

Total cells: 10,568,237

- Positive: 5,368,467
- Negative: 5,196,423

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000040 | 1,056,825 |
| 95th | +0.00000123 | 528,413 |
| 99th | +0.00000844 | 105,683 |
| 99.5th | +0.00001746 | 52,842 |
| 99.9th | +0.00008559 | 10,569 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L5 | H9 | 101 | ss1 | 97 | ss1 | +0.079421 | 0.063276 |
| L17 | H10 | 203 | ss2 | 201 | ss2 | +0.044690 | 0.609016 |
| L29 | H18 | 202 | ss2 | 100 | ss1 | +0.034263 | 0.455452 |
| L19 | H0 | 203 | ss2 | 201 | ss2 | +0.033384 | 0.169773 |
| L15 | H8 | 203 | ss2 | 101 | ss1 | +0.030909 | 0.312436 |
| L10 | H9 | 201 | ss2 | 101 | ss1 | +0.029846 | 0.205972 |
| L7 | H13 | 217 | flkR | 270 | flkR | +0.029452 | 0.230602 |
| L29 | H18 | 103 | ss1 | 199 | ss2 | +0.028711 | 0.425008 |
| L14 | H4 | 203 | ss2 | 101 | ss1 | +0.027010 | 0.213033 |
| L29 | H18 | 102 | ss1 | 200 | ss2 | +0.023882 | 0.566388 |
| L14 | H4 | 201 | ss2 | 101 | ss1 | +0.022874 | 0.251049 |
| L7 | H13 | 270 | flkR | 217 | flkR | +0.022672 | 0.417911 |
| L4 | H5 | 97 | ss1 | 92 | flkL | +0.020753 | 0.015520 |
| L17 | H10 | 202 | ss2 | 201 | ss2 | +0.020491 | 0.693866 |
| L17 | H18 | 201 | ss2 | 101 | ss1 | +0.018594 | 0.226862 |
| L10 | H9 | 101 | ss1 | 101 | ss1 | +0.017854 | 0.058968 |
| L26 | H16 | 199 | ss2 | 103 | ss1 | +0.017655 | 0.169158 |
| L27 | H15 | 200 | ss2 | 102 | ss1 | +0.017267 | 0.296327 |
| L17 | H1 | 201 | ss2 | 223 | flkR | +0.015529 | 0.130110 |
| L27 | H10 | 205 | ss2 | 203 | ss2 | +0.015187 | 0.321621 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L9 | H17 | 101 | ss1 | 137 | other | -0.006649 | 0.022128 |
| L12 | H10 | 115 | other | 101 | ss1 | -0.006707 | 0.221530 |
| L18 | H5 | 205 | ss2 | 201 | ss2 | -0.006874 | 0.234106 |
| L10 | H9 | 107 | other | 101 | ss1 | -0.006895 | 0.262855 |
| L7 | H13 | 217 | flkR | 253 | flkR | -0.007746 | 0.069634 |
| L31 | H17 | 100 | ss1 | 200 | ss2 | -0.007815 | 0.209782 |
| L14 | H4 | 205 | ss2 | 101 | ss1 | -0.008256 | 0.257905 |
| L29 | H18 | 100 | ss1 | 200 | ss2 | -0.008451 | 0.328672 |
| L4 | H14 | 101 | ss1 | 271 | flkR | -0.008666 | 0.014578 |
| L10 | H9 | 239 | flkR | 101 | ss1 | -0.008814 | 0.229352 |
| L11 | H16 | 201 | ss2 | 101 | ss1 | -0.009489 | 0.076222 |
| L19 | H0 | 201 | ss2 | 199 | ss2 | -0.009615 | 0.391114 |
| L15 | H6 | 101 | ss1 | 92 | flkL | -0.010612 | 0.222829 |
| L11 | H14 | 197 | ss2 | 101 | ss1 | -0.011383 | 0.176847 |
| L7 | H13 | 217 | flkR | 217 | flkR | -0.011815 | 0.113160 |
| L5 | H9 | 101 | ss1 | 95 | flkL | -0.012700 | 0.016153 |
| L7 | H13 | 32 | flkL | 198 | ss2 | -0.014278 | 0.502870 |
| L10 | H9 | 199 | ss2 | 101 | ss1 | -0.016101 | 0.246348 |
| L17 | H10 | 201 | ss2 | 203 | ss2 | -0.016777 | 0.440773 |
| L9 | H17 | 201 | ss2 | 101 | ss1 | -0.020021 | 0.081358 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0644 | 0.00% |
| 10 | 10 | 8 | 0.0658 | 0.18% |
| 20 | 20 | 14 | 0.0681 | 0.45% |
| 50 | 50 | 28 | 0.0749 | 1.30% |
| 100 | 100 | 39 | 0.0850 | 2.57% |
| 200 | 200 | 47 | 0.1073 | 5.35% |
| 500 | 500 | 59 | 0.2183 | 19.22% |
| 1000 | 1,000 | 65 | 0.3500 | 35.68% |
| 2000 | 2,000 | 65 | 0.4666 | 50.26% |
| 5000 | 5,000 | 65 | 0.5792 | 64.32% |
| 10000 | 10,000 | 65 | 0.7023 | 79.70% |
| 20000 | 20,000 | 65 | 0.8190 | 94.29% |
| 50000 | 50,000 | 65 | 0.8831 | 102.30% |

## Motif Analysis

### L0 H12 — Rank #17

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkL  |  cells: 10  |  total attr: +0.0105

**Key mass** (top-1=39%, top-2=77%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 271 | flkR | +0.0041 | 39.2% |
| 32 | flkL | +0.0040 | 38.0% |
| 31 | flkL | +0.0016 | 15.7% |
| 272 | flkR | +0.0007 | 7.1% |

**Query mass** (top-1=18%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 267 | flkR | +0.0018 | 17.6% |
| 52 | flkL | +0.0015 | 14.5% |
| 75 | flkL | +0.0013 | 12.1% |
| 239 | flkR | +0.0012 | 11.4% |
| 73 | flkL | +0.0012 | 11.4% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +20 | 1 | 10.0% |
| +43 | 1 | 10.0% |
| -32 | 1 | 10.0% |
| +41 | 1 | 10.0% |
| -4 | 1 | 10.0% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 50.0% |
| flkR | flkR | 4 | 40.0% |
| flkL | flkR | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 52 | flkL | 32 | flkL | +0.0015 | 0.0098 |
| 75 | flkL | 32 | flkL | +0.0013 | 0.0036 |
| 239 | flkR | 271 | flkR | +0.0012 | 0.0067 |
| 73 | flkL | 32 | flkL | +0.0012 | 0.0038 |
| 267 | flkR | 271 | flkR | +0.0011 | 0.0163 |

### L3 H7 — Rank #22

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | INTRA:flkL  |  cells: 12  |  total attr: +0.0394

**Key mass** (top-1=33%, top-2=55%, top-3=70%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0130 | 32.9% |
| 31 | flkL | +0.0085 | 21.7% |
| 270 | flkR | +0.0060 | 15.2% |
| 33 | flkL | +0.0032 | 8.0% |
| 269 | flkR | +0.0028 | 7.1% |

**Query mass** (top-1=48%, top-2=70%, top-3=79%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 31 | flkL | +0.0188 | 47.7% |
| 269 | flkR | +0.0088 | 22.3% |
| 30 | other | +0.0036 | 9.1% |
| 32 | flkL | +0.0032 | 8.0% |
| 271 | flkR | +0.0012 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 7 | 58.3% |
| +0 | 5 | 41.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 5 | 41.7% |
| flkR | flkR | 3 | 25.0% |
| other | flkL | 1 | 8.3% |
| ss1 | ss1 | 1 | 8.3% |
| other | other | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 31 | flkL | 32 | flkL | +0.0130 | 0.3132 |
| 269 | flkR | 270 | flkR | +0.0060 | 0.1233 |
| 31 | flkL | 31 | flkL | +0.0058 | 0.1221 |
| 32 | flkL | 33 | flkL | +0.0032 | 0.0808 |
| 269 | flkR | 269 | flkR | +0.0028 | 0.0712 |

### L4 H14 — Rank #27

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→flkR  |  cells: 2  |  total attr: +0.0046

**Key mass** (top-1=56%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 270 | flkR | +0.0026 | 56.5% |
| 271 | flkR | +0.0020 | 43.5% |

**Query mass** (top-1=56%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0026 | 56.5% |
| 71 | flkL | +0.0020 | 43.5% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -169 | 1 | 50.0% |
| -200 | 1 | 50.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 1 | 50.0% |
| flkL | flkR | 1 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 270 | flkR | +0.0026 | 0.0034 |
| 71 | flkL | 271 | flkR | +0.0020 | 0.0101 |

### L5 H9 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 8  |  total attr: +0.0910

**Key mass** (top-1=91%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 97 | ss1 | +0.0831 | 91.3% |
| 232 | flkR | +0.0052 | 5.7% |
| 29 | other | +0.0015 | 1.7% |
| 101 | ss1 | +0.0012 | 1.3% |

**Query mass** (top-1=89%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0806 | 88.6% |
| 103 | ss1 | +0.0037 | 4.0% |
| 222 | flkR | +0.0021 | 2.3% |
| 33 | flkL | +0.0015 | 1.7% |
| 241 | flkR | +0.0013 | 1.4% |

**Offset distribution [frequency]** (top-2 coverage: 62%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 3 | 37.5% |
| +0 | 2 | 25.0% |
| +6 | 1 | 12.5% |
| -10 | 1 | 12.5% |
| +9 | 1 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 50.0% |
| ss1 | ss1 | 3 | 37.5% |
| flkL | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 97 | ss1 | +0.0794 | 0.0633 |
| 103 | ss1 | 97 | ss1 | +0.0037 | 0.0474 |
| 222 | flkR | 232 | flkR | +0.0021 | 0.0239 |
| 33 | flkL | 29 | other | +0.0015 | 0.1331 |
| 241 | flkR | 232 | flkR | +0.0013 | 0.0458 |

### L6 H0 — Rank #15

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 12  |  total attr: +0.0217

**Key mass** (top-1=31%, top-2=49%, top-3=60%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0068 | 31.3% |
| 44 | flkL | +0.0038 | 17.7% |
| 43 | flkL | +0.0024 | 11.0% |
| 30 | other | +0.0019 | 8.7% |
| 55 | flkL | +0.0013 | 5.8% |

**Query mass** (top-1=87%, top-2=92%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0189 | 87.4% |
| 92 | flkL | +0.0010 | 4.7% |
| 88 | flkL | +0.0009 | 4.0% |
| 217 | flkR | +0.0008 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +58 | 2 | 16.7% |
| +69 | 1 | 8.3% |
| +57 | 1 | 8.3% |
| +46 | 1 | 8.3% |
| +50 | 1 | 8.3% |

**Region-pair profile** (q→k)  [ss1→flkL]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkL | 9 | 75.0% |
| flkL | other | 2 | 16.7% |
| flkR | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 32 | flkL | +0.0068 | 0.0362 |
| 101 | ss1 | 44 | flkL | +0.0038 | 0.0201 |
| 101 | ss1 | 43 | flkL | +0.0024 | 0.0056 |
| 101 | ss1 | 55 | flkL | +0.0013 | 0.0025 |
| 101 | ss1 | 51 | flkL | +0.0011 | 0.0029 |

### L7 H7 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0804

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0804 | 100.0% |

**Query mass** (top-1=15%, top-2=25%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0117 | 14.5% |
| 137 | other | +0.0085 | 10.6% |
| 138 | other | +0.0074 | 9.2% |
| 136 | other | +0.0058 | 7.2% |
| 139 | other | +0.0051 | 6.4% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 1 | 4.2% |
| +36 | 1 | 4.2% |
| +37 | 1 | 4.2% |
| +35 | 1 | 4.2% |
| +38 | 1 | 4.2% |

**Region-pair profile** (q→k)  (top=83%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 20 | 83.3% |
| flkL | ss1 | 2 | 8.3% |
| ss1 | ss1 | 1 | 4.2% |
| ss2 | ss1 | 1 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 101 | ss1 | 101 | ss1 | +0.0117 | 0.1317 |
| 137 | other | 101 | ss1 | +0.0085 | 0.0796 |
| 138 | other | 101 | ss1 | +0.0074 | 0.0771 |
| 136 | other | 101 | ss1 | +0.0058 | 0.0738 |
| 139 | other | 101 | ss1 | +0.0051 | 0.0696 |

### L7 H13 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:flkR  |  cells: 72  |  total attr: +0.1803

**Key mass** (top-1=19%, top-2=31%, top-3=39%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 270 | flkR | +0.0338 | 18.7% |
| 217 | flkR | +0.0227 | 12.6% |
| 269 | flkR | +0.0141 | 7.8% |
| 272 | flkR | +0.0072 | 4.0% |
| 231 | flkR | +0.0070 | 3.9% |

**Query mass** (top-1=16%, top-2=29%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 217 | flkR | +0.0295 | 16.3% |
| 270 | flkR | +0.0227 | 12.6% |
| 229 | flkR | +0.0135 | 7.5% |
| 216 | flkR | +0.0133 | 7.4% |
| 212 | flkR | +0.0093 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 17 | 23.6% |
| -53 | 4 | 5.6% |
| -40 | 4 | 5.6% |
| -39 | 2 | 2.8% |
| -60 | 2 | 2.8% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 31 | 43.1% |
| flkL | flkL | 20 | 27.8% |
| flkR | flkL | 6 | 8.3% |
| flkR | ss2 | 3 | 4.2% |
| flkL | flkR | 3 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 217 | flkR | 270 | flkR | +0.0295 | 0.2306 |
| 270 | flkR | 217 | flkR | +0.0227 | 0.4179 |
| 216 | flkR | 269 | flkR | +0.0133 | 0.0954 |
| 231 | flkR | 231 | flkR | +0.0070 | 0.0916 |
| 212 | flkR | 212 | flkR | +0.0068 | 0.0662 |

### L7 H18 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | INTRA:flkR  |  cells: 23  |  total attr: +0.0303

**Key mass** (top-1=59%, top-2=86%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 272 | flkR | +0.0178 | 58.8% |
| 269 | flkR | +0.0084 | 27.6% |
| 37 | flkL | +0.0021 | 6.8% |
| 95 | flkL | +0.0013 | 4.4% |
| 266 | flkR | +0.0008 | 2.5% |

**Query mass** (top-1=17%, top-2=31%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 264 | flkR | +0.0051 | 16.8% |
| 101 | ss1 | +0.0041 | 13.7% |
| 188 | other | +0.0023 | 7.7% |
| 247 | flkR | +0.0018 | 5.8% |
| 218 | flkR | +0.0017 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 1 | 4.3% |
| +64 | 1 | 4.3% |
| -25 | 1 | 4.3% |
| -54 | 1 | 4.3% |
| -5 | 1 | 4.3% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 10 | 43.5% |
| other | flkR | 6 | 26.1% |
| ss2 | flkR | 4 | 17.4% |
| ss1 | flkL | 2 | 8.7% |
| ss1 | flkR | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 264 | flkR | 272 | flkR | +0.0035 | 0.1015 |
| 101 | ss1 | 37 | flkL | +0.0021 | 0.0062 |
| 247 | flkR | 272 | flkR | +0.0018 | 0.0962 |
| 218 | flkR | 272 | flkR | +0.0017 | 0.0454 |
| 264 | flkR | 269 | flkR | +0.0016 | 0.0318 |

### L8 H2 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0679

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0679 | 100.0% |

**Query mass** (top-1=17%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 137 | other | +0.0113 | 16.7% |
| 138 | other | +0.0103 | 15.1% |
| 139 | other | +0.0083 | 12.2% |
| 136 | other | +0.0083 | 12.2% |
| 140 | other | +0.0074 | 10.9% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +36 | 1 | 10.0% |
| +37 | 1 | 10.0% |
| +38 | 1 | 10.0% |
| +35 | 1 | 10.0% |
| +39 | 1 | 10.0% |

**Region-pair profile** (q→k)  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 10 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 137 | other | 101 | ss1 | +0.0113 | 0.0454 |
| 138 | other | 101 | ss1 | +0.0103 | 0.0532 |
| 139 | other | 101 | ss1 | +0.0083 | 0.0697 |
| 136 | other | 101 | ss1 | +0.0083 | 0.0502 |
| 140 | other | 101 | ss1 | +0.0074 | 0.0916 |

### L9 H17 — Rank #2

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 44  |  total attr: +0.1388

**Key mass** (top-1=11%, top-2=21%, top-3=29%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 141 | other | +0.0149 | 10.8% |
| 140 | other | +0.0141 | 10.1% |
| 142 | other | +0.0106 | 7.7% |
| 139 | other | +0.0099 | 7.2% |
| 138 | other | +0.0092 | 6.6% |

**Query mass** (top-1=70%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0975 | 70.2% |
| 101 | ss1 | +0.0329 | 23.7% |
| 103 | ss1 | +0.0060 | 4.3% |
| 105 | ss1 | +0.0025 | 1.8% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -33 | 2 | 4.5% |
| -32 | 2 | 4.5% |
| -34 | 2 | 4.5% |
| +60 | 1 | 2.3% |
| +61 | 1 | 2.3% |

**Region-pair profile** (q→k)  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 23 | 52.3% |
| ss1 | other | 21 | 47.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 141 | other | +0.0111 | 0.0277 |
| 201 | ss2 | 140 | other | +0.0105 | 0.0257 |
| 201 | ss2 | 138 | other | +0.0092 | 0.0204 |
| 201 | ss2 | 139 | other | +0.0092 | 0.0213 |
| 201 | ss2 | 142 | other | +0.0086 | 0.0210 |

### L10 H9 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 100  |  total attr: +0.2674

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.2664 | 99.6% |
| 226 | flkR | +0.0010 | 0.4% |

**Query mass** (top-1=11%, top-2=18%, top-3=23%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0298 | 11.2% |
| 101 | ss1 | +0.0179 | 6.7% |
| 202 | ss2 | +0.0136 | 5.1% |
| 100 | ss1 | +0.0102 | 3.8% |
| 212 | flkR | +0.0092 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 2%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 1 | 1.0% |
| +0 | 1 | 1.0% |
| +101 | 1 | 1.0% |
| -1 | 1 | 1.0% |
| +111 | 1 | 1.0% |

**Region-pair profile** (q→k)  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 52 | 52.0% |
| flkR | ss1 | 25 | 25.0% |
| flkL | ss1 | 9 | 9.0% |
| ss1 | ss1 | 7 | 7.0% |
| ss2 | ss1 | 6 | 6.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0298 | 0.2060 |
| 101 | ss1 | 101 | ss1 | +0.0179 | 0.0590 |
| 202 | ss2 | 101 | ss1 | +0.0136 | 0.2546 |
| 100 | ss1 | 101 | ss1 | +0.0102 | 0.2569 |
| 212 | flkR | 101 | ss1 | +0.0092 | 0.2474 |

### L11 H8 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkR→ss1  |  cells: 26  |  total attr: +0.0405

**Key mass** (top-1=93%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0379 | 93.5% |
| 418 | other | +0.0026 | 6.5% |

**Query mass** (top-1=9%, top-2=18%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 239 | flkR | +0.0038 | 9.4% |
| 223 | flkR | +0.0036 | 9.0% |
| 418 | other | +0.0034 | 8.4% |
| 222 | flkR | +0.0028 | 6.9% |
| 232 | flkR | +0.0027 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 8%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +138 | 1 | 3.8% |
| +122 | 1 | 3.8% |
| +317 | 1 | 3.8% |
| +121 | 1 | 3.8% |
| +131 | 1 | 3.8% |

**Region-pair profile** (q→k)  [CROSS:flkR→ss1]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | ss1 | 12 | 46.2% |
| other | ss1 | 7 | 26.9% |
| ss2 | ss1 | 4 | 15.4% |
| ss2 | other | 2 | 7.7% |
| flkL | ss1 | 1 | 3.8% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 239 | flkR | 101 | ss1 | +0.0038 | 0.1277 |
| 223 | flkR | 101 | ss1 | +0.0036 | 0.1630 |
| 418 | other | 101 | ss1 | +0.0034 | 0.0633 |
| 222 | flkR | 101 | ss1 | +0.0028 | 0.2006 |
| 232 | flkR | 101 | ss1 | +0.0027 | 0.3510 |

### L11 H14 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 44  |  total attr: +0.0797

**Key mass** (top-1=92%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0734 | 92.1% |
| 228 | flkR | +0.0031 | 3.9% |
| 418 | other | +0.0022 | 2.8% |
| 71 | flkL | +0.0010 | 1.2% |

**Query mass** (top-1=8%, top-2=13%, top-3=17%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0063 | 7.9% |
| 201 | ss2 | +0.0038 | 4.8% |
| 149 | other | +0.0032 | 4.0% |
| 150 | other | +0.0031 | 3.9% |
| 142 | other | +0.0031 | 3.8% |

**Offset distribution [frequency]** (top-2 coverage: 5%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 1 | 2.3% |
| +48 | 1 | 2.3% |
| +49 | 1 | 2.3% |
| +41 | 1 | 2.3% |
| +100 | 1 | 2.3% |

**Region-pair profile** (q→k)  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 32 | 72.7% |
| ss2 | ss1 | 4 | 9.1% |
| ss2 | flkR | 2 | 4.5% |
| ss1 | ss1 | 2 | 4.5% |
| other | other | 1 | 2.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 101 | ss1 | +0.0041 | 0.0277 |
| 149 | other | 101 | ss1 | +0.0032 | 0.1283 |
| 150 | other | 101 | ss1 | +0.0031 | 0.1225 |
| 142 | other | 101 | ss1 | +0.0031 | 0.1018 |
| 201 | ss2 | 101 | ss1 | +0.0029 | 0.0489 |

### L11 H16 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 33  |  total attr: +0.0491

**Key mass** (top-1=85%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0418 | 85.1% |
| 418 | other | +0.0019 | 3.9% |
| 45 | flkL | +0.0018 | 3.8% |
| 53 | flkL | +0.0018 | 3.7% |
| 239 | flkR | +0.0010 | 2.1% |

**Query mass** (top-1=15%, top-2=23%, top-3=30%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 30 | other | +0.0072 | 14.7% |
| 205 | ss2 | +0.0042 | 8.6% |
| 113 | other | +0.0036 | 7.3% |
| 32 | flkL | +0.0027 | 5.6% |
| 116 | other | +0.0026 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 6.1% |
| -71 | 1 | 3.0% |
| +104 | 1 | 3.0% |
| +12 | 1 | 3.0% |
| -69 | 1 | 3.0% |

**Region-pair profile** (q→k)  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 14 | 42.4% |
| other | flkL | 4 | 12.1% |
| ss2 | ss1 | 3 | 9.1% |
| flkR | ss1 | 3 | 9.1% |
| ss1 | ss1 | 3 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 30 | other | 101 | ss1 | +0.0047 | 0.2293 |
| 205 | ss2 | 101 | ss1 | +0.0042 | 0.1442 |
| 113 | other | 101 | ss1 | +0.0036 | 0.2113 |
| 32 | flkL | 101 | ss1 | +0.0027 | 0.2549 |
| 116 | other | 101 | ss1 | +0.0026 | 0.2226 |

### L12 H10 — Rank #11

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 25  |  total attr: +0.0481

**Key mass** (top-1=35%, top-2=42%, top-3=48%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0169 | 35.0% |
| 71 | flkL | +0.0036 | 7.4% |
| 149 | other | +0.0028 | 5.8% |
| 150 | other | +0.0027 | 5.7% |
| 190 | other | +0.0020 | 4.1% |

**Query mass** (top-1=60%, top-2=84%, top-3=95%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0288 | 59.9% |
| 116 | other | +0.0115 | 23.8% |
| 113 | other | +0.0054 | 11.2% |
| 101 | ss1 | +0.0017 | 3.5% |
| 203 | ss2 | +0.0008 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 16%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +12 | 2 | 8.0% |
| +9 | 2 | 8.0% |
| +15 | 1 | 4.0% |
| +52 | 1 | 4.0% |
| +51 | 1 | 4.0% |

**Region-pair profile** (q→k)  (top=84%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 21 | 84.0% |
| other | ss1 | 2 | 8.0% |
| ss2 | flkL | 1 | 4.0% |
| ss1 | flkL | 1 | 4.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 116 | other | 101 | ss1 | +0.0115 | 0.2085 |
| 113 | other | 101 | ss1 | +0.0054 | 0.2593 |
| 201 | ss2 | 149 | other | +0.0028 | 0.0230 |
| 201 | ss2 | 150 | other | +0.0027 | 0.0245 |
| 201 | ss2 | 190 | other | +0.0020 | 0.0562 |

### L13 H2 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 16  |  total attr: +0.0417

**Key mass** (top-1=66%, top-2=79%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0276 | 66.0% |
| 203 | ss2 | +0.0053 | 12.8% |
| 101 | ss1 | +0.0042 | 10.1% |
| 240 | flkR | +0.0019 | 4.5% |
| 198 | ss2 | +0.0012 | 2.9% |

**Query mass** (top-1=25%, top-2=44%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0102 | 24.5% |
| 201 | ss2 | +0.0082 | 19.7% |
| 200 | ss2 | +0.0054 | 12.9% |
| 198 | ss2 | +0.0051 | 12.1% |
| 197 | ss2 | +0.0038 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 3 | 18.8% |
| -2 | 2 | 12.5% |
| -3 | 2 | 12.5% |
| -4 | 2 | 12.5% |
| +6 | 2 | 12.5% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=69%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 11 | 68.8% |
| ss2 | other | 2 | 12.5% |
| other | ss1 | 1 | 6.2% |
| ss1 | ss1 | 1 | 6.2% |
| flkR | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | ss2 | 201 | ss2 | +0.0090 | 0.3382 |
| 198 | ss2 | 201 | ss2 | +0.0051 | 0.2648 |
| 200 | ss2 | 201 | ss2 | +0.0044 | 0.3212 |
| 201 | ss2 | 201 | ss2 | +0.0035 | 0.1186 |
| 201 | ss2 | 203 | ss2 | +0.0031 | 0.0655 |

### L14 H4 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0750

**Key mass** (top-1=95%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0710 | 94.7% |
| 99 | ss1 | +0.0032 | 4.3% |
| -1 | other | +0.0007 | 1.0% |

**Query mass** (top-1=39%, top-2=71%, top-3=79%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0289 | 38.5% |
| 201 | ss2 | +0.0242 | 32.3% |
| 243 | flkR | +0.0063 | 8.4% |
| 206 | ss2 | +0.0053 | 7.0% |
| 202 | ss2 | +0.0037 | 5.0% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 2 | 18.2% |
| +98 | 2 | 18.2% |
| +100 | 1 | 9.1% |
| +142 | 1 | 9.1% |
| +105 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=64%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 63.6% |
| flkR | ss1 | 3 | 27.3% |
| ss1 | other | 1 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 101 | ss1 | +0.0270 | 0.2130 |
| 201 | ss2 | 101 | ss1 | +0.0229 | 0.2510 |
| 243 | flkR | 101 | ss1 | +0.0063 | 0.2822 |
| 206 | ss2 | 101 | ss1 | +0.0053 | 0.2458 |
| 202 | ss2 | 101 | ss1 | +0.0037 | 0.1911 |

### L14 H9 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.0223

**Key mass** (top-1=33%, top-2=49%, top-3=65%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0074 | 33.3% |
| 198 | ss2 | +0.0036 | 16.0% |
| 233 | flkR | +0.0035 | 15.9% |
| 215 | flkR | +0.0035 | 15.7% |
| -1 | other | +0.0015 | 6.5% |

**Query mass** (top-1=23%, top-2=39%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0051 | 22.8% |
| 223 | flkR | +0.0036 | 16.0% |
| 103 | ss1 | +0.0032 | 14.4% |
| 199 | ss2 | +0.0023 | 10.5% |
| 201 | ss2 | +0.0023 | 10.2% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -10 | 2 | 13.3% |
| +2 | 1 | 6.7% |
| +102 | 1 | 6.7% |
| +8 | 1 | 6.7% |
| +6 | 1 | 6.7% |

**Region-pair profile** (q→k)  (top=27%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 4 | 26.7% |
| ss2 | ss2 | 4 | 26.7% |
| ss2 | flkR | 2 | 13.3% |
| ss1 | ss1 | 1 | 6.7% |
| ss2 | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 103 | ss1 | 101 | ss1 | +0.0032 | 0.0959 |
| 203 | ss2 | 101 | ss1 | +0.0032 | 0.0581 |
| 223 | flkR | 233 | flkR | +0.0020 | 0.0936 |
| 223 | flkR | 215 | flkR | +0.0016 | 0.1121 |
| 239 | flkR | 233 | flkR | +0.0016 | 0.0726 |

### L15 H8 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 5  |  total attr: +0.0365

**Key mass** (top-1=91%, top-2=95%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0332 | 90.8% |
| 103 | ss1 | +0.0014 | 4.0% |
| 71 | flkL | +0.0011 | 3.1% |
| 201 | ss2 | +0.0007 | 2.0% |

**Query mass** (top-1=91%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0331 | 90.7% |
| 201 | ss2 | +0.0034 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 60%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 2 | 40.0% |
| +102 | 1 | 20.0% |
| +130 | 1 | 20.0% |
| +2 | 1 | 20.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=60%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 3 | 60.0% |
| ss2 | flkL | 1 | 20.0% |
| ss2 | ss2 | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 101 | ss1 | +0.0309 | 0.3124 |
| 201 | ss2 | 101 | ss1 | +0.0023 | 0.2464 |
| 203 | ss2 | 103 | ss1 | +0.0014 | 0.0257 |
| 201 | ss2 | 71 | flkL | +0.0011 | 0.0138 |
| 203 | ss2 | 201 | ss2 | +0.0007 | 0.0142 |

### L16 H7 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | INTRA:ss2  |  cells: 22  |  total attr: +0.0343

**Key mass** (top-1=47%, top-2=60%, top-3=70%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0160 | 46.6% |
| 198 | ss2 | +0.0045 | 13.1% |
| 203 | ss2 | +0.0036 | 10.4% |
| 201 | ss2 | +0.0036 | 10.4% |
| 210 | flkR | +0.0020 | 6.0% |

**Query mass** (top-1=26%, top-2=46%, top-3=54%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0088 | 25.5% |
| 116 | other | +0.0071 | 20.6% |
| 199 | ss2 | +0.0027 | 8.0% |
| 203 | ss2 | +0.0026 | 7.5% |
| 117 | other | +0.0025 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 2 | 9.1% |
| +3 | 2 | 9.1% |
| +15 | 1 | 4.5% |
| +100 | 1 | 4.5% |
| +16 | 1 | 4.5% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=41%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 9 | 40.9% |
| other | ss1 | 4 | 18.2% |
| ss2 | other | 3 | 13.6% |
| ss2 | ss1 | 1 | 4.5% |
| ss2 | flkR | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 116 | other | 101 | ss1 | +0.0071 | 0.3745 |
| 201 | ss2 | 101 | ss1 | +0.0028 | 0.0541 |
| 117 | other | 101 | ss1 | +0.0025 | 0.4241 |
| 201 | ss2 | 210 | flkR | +0.0020 | 0.0298 |
| 201 | ss2 | 203 | ss2 | +0.0020 | 0.0631 |

### L16 H12 — Rank #24

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 23  |  total attr: +0.0468

**Key mass** (top-1=25%, top-2=41%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0117 | 25.1% |
| 200 | ss2 | +0.0073 | 15.7% |
| 197 | ss2 | +0.0048 | 10.2% |
| 202 | ss2 | +0.0026 | 5.5% |
| 220 | flkR | +0.0025 | 5.3% |

**Query mass** (top-1=31%, top-2=46%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0145 | 31.0% |
| 201 | ss2 | +0.0072 | 15.3% |
| 199 | ss2 | +0.0048 | 10.2% |
| 202 | ss2 | +0.0038 | 8.1% |
| 223 | flkR | +0.0025 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 74%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 13 | 56.5% |
| +1 | 4 | 17.4% |
| +3 | 3 | 13.0% |
| -5 | 1 | 4.3% |
| +4 | 1 | 4.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=52%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 12 | 52.2% |
| other | other | 5 | 21.7% |
| flkR | flkR | 3 | 13.0% |
| flkL | flkL | 2 | 8.7% |
| ss1 | ss1 | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 201 | ss2 | +0.0117 | 0.2857 |
| 199 | ss2 | 197 | ss2 | +0.0048 | 0.4003 |
| 202 | ss2 | 200 | ss2 | +0.0038 | 0.2705 |
| 223 | flkR | 220 | flkR | +0.0025 | 0.2291 |
| 201 | ss2 | 200 | ss2 | +0.0024 | 0.0715 |

### L17 H7 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 29  |  total attr: +0.0288

**Key mass** (top-1=10%, top-2=18%, top-3=24%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 71 | flkL | +0.0028 | 9.7% |
| 188 | other | +0.0023 | 8.1% |
| 189 | other | +0.0017 | 5.8% |
| 88 | flkL | +0.0016 | 5.6% |
| 191 | other | +0.0014 | 4.9% |

**Query mass** (top-1=50%, top-2=69%, top-3=78%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0145 | 50.3% |
| 203 | ss2 | +0.0053 | 18.4% |
| 103 | ss1 | +0.0026 | 9.0% |
| 239 | flkR | +0.0017 | 6.0% |
| 90 | flkL | +0.0015 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +15 | 2 | 6.9% |
| +12 | 2 | 6.9% |
| +9 | 2 | 6.9% |
| +11 | 2 | 6.9% |
| +38 | 2 | 6.9% |

**Region-pair profile** (q→k)  (top=72%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | other | 21 | 72.4% |
| ss1 | flkL | 3 | 10.3% |
| flkL | flkL | 2 | 6.9% |
| flkR | ss2 | 2 | 6.9% |
| other | other | 1 | 3.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 103 | ss1 | 88 | flkL | +0.0016 | 0.0774 |
| 90 | flkL | 71 | flkL | +0.0015 | 0.1580 |
| 203 | ss2 | 191 | other | +0.0014 | 0.0342 |
| 203 | ss2 | 188 | other | +0.0013 | 0.0229 |
| 92 | flkL | 71 | flkL | +0.0013 | 0.2319 |

### L17 H10 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 19  |  total attr: +0.1211

**Key mass** (top-1=79%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0958 | 79.1% |
| 203 | ss2 | +0.0185 | 15.2% |
| 101 | ss1 | +0.0048 | 4.0% |
| 204 | ss2 | +0.0010 | 0.9% |
| 114 | other | +0.0009 | 0.8% |

**Query mass** (top-1=38%, top-2=58%, top-3=68%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0457 | 37.8% |
| 202 | ss2 | +0.0244 | 20.1% |
| 206 | ss2 | +0.0119 | 9.8% |
| 205 | ss2 | +0.0104 | 8.6% |
| 198 | ss2 | +0.0080 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 15.8% |
| +2 | 2 | 10.5% |
| -1 | 2 | 10.5% |
| +0 | 2 | 10.5% |
| +5 | 1 | 5.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=74%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 14 | 73.7% |
| other | ss1 | 2 | 10.5% |
| ss1 | ss1 | 1 | 5.3% |
| other | ss2 | 1 | 5.3% |
| other | other | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 203 | ss2 | 201 | ss2 | +0.0447 | 0.6090 |
| 202 | ss2 | 201 | ss2 | +0.0205 | 0.6939 |
| 206 | ss2 | 201 | ss2 | +0.0108 | 0.6821 |
| 205 | ss2 | 203 | ss2 | +0.0104 | 0.5168 |
| 198 | ss2 | 201 | ss2 | +0.0080 | 0.7218 |

### L17 H18 — Rank #19

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 14  |  total attr: +0.0443

**Key mass** (top-1=56%, top-2=65%, top-3=71%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0249 | 56.1% |
| 230 | flkR | +0.0041 | 9.2% |
| 239 | flkR | +0.0023 | 5.2% |
| 203 | ss2 | +0.0022 | 5.0% |
| 201 | ss2 | +0.0022 | 4.9% |

**Query mass** (top-1=51%, top-2=78%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0226 | 50.9% |
| 203 | ss2 | +0.0122 | 27.5% |
| 199 | ss2 | +0.0048 | 10.9% |
| 257 | flkR | +0.0023 | 5.2% |
| 101 | ss1 | +0.0014 | 3.2% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +102 | 2 | 14.3% |
| -31 | 2 | 14.3% |
| +100 | 1 | 7.1% |
| +18 | 1 | 7.1% |
| +0 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 28.6% |
| ss2 | flkL | 3 | 21.4% |
| ss2 | flkR | 2 | 14.3% |
| flkR | flkR | 2 | 14.3% |
| ss2 | ss2 | 2 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 201 | ss2 | 101 | ss1 | +0.0186 | 0.2269 |
| 203 | ss2 | 101 | ss1 | +0.0063 | 0.0683 |
| 199 | ss2 | 230 | flkR | +0.0041 | 0.1359 |
| 257 | flkR | 239 | flkR | +0.0023 | 0.1157 |
| 203 | ss2 | 203 | ss2 | +0.0022 | 0.0306 |

### L19 H3 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 13  |  total attr: +0.0471

**Key mass** (top-1=66%, top-2=80%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 201 | ss2 | +0.0310 | 65.8% |
| 243 | flkR | +0.0065 | 13.8% |
| 75 | flkL | +0.0030 | 6.4% |
| 105 | ss1 | +0.0025 | 5.2% |
| 101 | ss1 | +0.0021 | 4.5% |

**Query mass** (top-1=30%, top-2=55%, top-3=68%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0142 | 30.2% |
| 198 | ss2 | +0.0115 | 24.4% |
| 239 | flkR | +0.0065 | 13.8% |
| 197 | ss2 | +0.0029 | 6.1% |
| 103 | ss1 | +0.0025 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 54%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 4 | 30.8% |
| -2 | 3 | 23.1% |
| -3 | 2 | 15.4% |
| -1 | 1 | 7.7% |
| +1 | 1 | 7.7% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=46%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 6 | 46.2% |
| ss1 | ss1 | 2 | 15.4% |
| flkL | flkL | 2 | 15.4% |
| flkR | flkR | 1 | 7.7% |
| other | ss1 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | ss2 | 201 | ss2 | +0.0130 | 0.4247 |
| 198 | ss2 | 201 | ss2 | +0.0115 | 0.4790 |
| 239 | flkR | 243 | flkR | +0.0065 | 0.3204 |
| 197 | ss2 | 201 | ss2 | +0.0029 | 0.3494 |
| 103 | ss1 | 105 | ss1 | +0.0025 | 0.0899 |

### L26 H16 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 15  |  total attr: +0.0457

**Key mass** (top-1=39%, top-2=60%, top-3=68%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | ss1 | +0.0177 | 38.6% |
| 97 | ss1 | +0.0098 | 21.5% |
| 100 | ss1 | +0.0036 | 7.8% |
| 91 | flkL | +0.0033 | 7.3% |
| 240 | flkR | +0.0032 | 7.1% |

**Query mass** (top-1=39%, top-2=52%, top-3=64%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0177 | 38.6% |
| 202 | ss2 | +0.0063 | 13.8% |
| 205 | ss2 | +0.0053 | 11.5% |
| 200 | ss2 | +0.0045 | 9.7% |
| 102 | ss1 | +0.0033 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -38 | 2 | 13.3% |
| +96 | 1 | 6.7% |
| +108 | 1 | 6.7% |
| +102 | 1 | 6.7% |
| +11 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 7 | 46.7% |
| ss2 | flkR | 4 | 26.7% |
| ss1 | flkL | 2 | 13.3% |
| flkL | ss1 | 2 | 13.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 199 | ss2 | 103 | ss1 | +0.0177 | 0.1692 |
| 205 | ss2 | 97 | ss1 | +0.0053 | 0.5849 |
| 202 | ss2 | 100 | ss1 | +0.0036 | 0.0253 |
| 102 | ss1 | 91 | flkL | +0.0033 | 0.3462 |
| 207 | ss2 | 97 | ss1 | +0.0027 | 0.1803 |

### L27 H15 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 19  |  total attr: +0.0909

**Key mass** (top-1=21%, top-2=37%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0188 | 20.7% |
| 99 | ss1 | +0.0144 | 15.9% |
| 98 | ss1 | +0.0121 | 13.3% |
| 97 | ss1 | +0.0109 | 12.0% |
| 100 | ss1 | +0.0080 | 8.8% |

**Query mass** (top-1=23%, top-2=45%, top-3=67%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0208 | 22.8% |
| 200 | ss2 | +0.0201 | 22.2% |
| 202 | ss2 | +0.0200 | 22.0% |
| 100 | ss1 | +0.0070 | 7.7% |
| 103 | ss1 | +0.0068 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +104 | 2 | 10.5% |
| +108 | 2 | 10.5% |
| +98 | 1 | 5.3% |
| -96 | 1 | 5.3% |
| +102 | 1 | 5.3% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 11 | 57.9% |
| ss1 | ss2 | 3 | 15.8% |
| ss2 | flkL | 3 | 15.8% |
| ss1 | flkL | 2 | 10.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | ss2 | 102 | ss1 | +0.0173 | 0.2963 |
| 203 | ss2 | 99 | ss1 | +0.0144 | 0.1743 |
| 202 | ss2 | 98 | ss1 | +0.0121 | 0.2284 |
| 103 | ss1 | 199 | ss2 | +0.0068 | 0.0575 |
| 205 | ss2 | 97 | ss1 | +0.0058 | 0.3145 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 20  |  total attr: +0.1370

**Key mass** (top-1=28%, top-2=49%, top-3=66%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0384 | 28.0% |
| 199 | ss2 | +0.0287 | 21.0% |
| 200 | ss2 | +0.0239 | 17.4% |
| 103 | ss1 | +0.0126 | 9.2% |
| 202 | ss2 | +0.0083 | 6.0% |

**Query mass** (top-1=26%, top-2=47%, top-3=64%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0354 | 25.8% |
| 103 | ss1 | +0.0287 | 21.0% |
| 102 | ss1 | +0.0239 | 17.4% |
| 199 | ss2 | +0.0166 | 12.1% |
| 100 | ss1 | +0.0124 | 9.1% |

**Offset distribution [frequency]** (top-2 coverage: 15%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +96 | 2 | 10.0% |
| +102 | 1 | 5.0% |
| -96 | 1 | 5.0% |
| -98 | 1 | 5.0% |
| -102 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 45.0% |
| ss1 | ss2 | 5 | 25.0% |
| ss2 | flkL | 3 | 15.0% |
| ss1 | ss1 | 1 | 5.0% |
| ss1 | flkL | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 202 | ss2 | 100 | ss1 | +0.0343 | 0.4555 |
| 103 | ss1 | 199 | ss2 | +0.0287 | 0.4250 |
| 102 | ss1 | 200 | ss2 | +0.0239 | 0.5664 |
| 199 | ss2 | 103 | ss1 | +0.0126 | 0.2488 |
| 100 | ss1 | 202 | ss2 | +0.0083 | 0.1756 |

### L32 H13 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 20  |  total attr: +0.0683

**Key mass** (top-1=15%, top-2=30%, top-3=43%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0101 | 14.8% |
| 202 | ss2 | +0.0101 | 14.8% |
| 100 | ss1 | +0.0091 | 13.4% |
| 102 | ss1 | +0.0085 | 12.4% |
| 199 | ss2 | +0.0078 | 11.5% |

**Query mass** (top-1=18%, top-2=34%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0121 | 17.8% |
| 102 | ss1 | +0.0108 | 15.8% |
| 100 | ss1 | +0.0079 | 11.6% |
| 103 | ss1 | +0.0078 | 11.5% |
| 99 | ss1 | +0.0067 | 9.8% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -96 | 2 | 10.0% |
| +96 | 2 | 10.0% |
| -104 | 2 | 10.0% |
| +104 | 2 | 10.0% |
| -98 | 2 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 10 | 50.0% |
| ss2 | ss1 | 10 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 102 | ss1 | 198 | ss2 | +0.0093 | 0.2656 |
| 202 | ss2 | 100 | ss1 | +0.0091 | 0.0553 |
| 103 | ss1 | 199 | ss2 | +0.0078 | 0.0585 |
| 100 | ss1 | 202 | ss2 | +0.0071 | 0.0428 |
| 198 | ss2 | 102 | ss1 | +0.0067 | 0.1901 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 18  |  total attr: +0.0703

**Key mass** (top-1=20%, top-2=39%, top-3=57%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 198 | ss2 | +0.0141 | 20.0% |
| 203 | ss2 | +0.0133 | 19.0% |
| 103 | ss1 | +0.0130 | 18.5% |
| 99 | ss1 | +0.0074 | 10.6% |
| 205 | ss2 | +0.0051 | 7.3% |

**Query mass** (top-1=26%, top-2=41%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 99 | ss1 | +0.0184 | 26.2% |
| 102 | ss1 | +0.0105 | 15.0% |
| 199 | ss2 | +0.0081 | 11.5% |
| 198 | ss2 | +0.0067 | 9.6% |
| 203 | ss2 | +0.0065 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -96 | 2 | 11.1% |
| +96 | 2 | 11.1% |
| +104 | 2 | 11.1% |
| -98 | 2 | 11.1% |
| +106 | 2 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 50.0% |
| ss2 | ss1 | 9 | 50.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 99 | ss1 | 203 | ss2 | +0.0133 | 0.1263 |
| 102 | ss1 | 198 | ss2 | +0.0089 | 0.1553 |
| 199 | ss2 | 103 | ss1 | +0.0081 | 0.0369 |
| 203 | ss2 | 99 | ss1 | +0.0065 | 0.0618 |
| 99 | ss1 | 205 | ss2 | +0.0051 | 0.0968 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #17 | L0 | H12 | 10 | +0.0105 | DUAL-ANCHOR | G271/Y32 | DISTRIBUTED |  |  | INTRA:flkL |
| #22 | L3 | H7 | 12 | +0.0394 | DISTRIBUTED |  | DUAL-ANCHOR | T31/D269 |  | INTRA:flkL |
| #27 | L4 | H14 | 2 | +0.0046 | DUAL-ANCHOR | N270/G271 | DUAL-ANCHOR | V101/I71 |  | CROSS:ss1→flkR |
| #10 | L5 | H9 | 8 | +0.0910 | SINGLE-ANCHOR | H97 | SINGLE-ANCHOR | V101 |  | INTRA:flkR |
| #15 | L6 | H0 | 12 | +0.0217 | DISTRIBUTED |  | SINGLE-ANCHOR | V101 |  | ss1→flkL |
| #9 | L7 | H7 | 24 | +0.0804 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #12 | L7 | H13 | 72 | +0.1803 | DISTRIBUTED |  | DISTRIBUTED |  |  | INTRA:flkR |
| #21 | L7 | H18 | 23 | +0.0303 | DUAL-ANCHOR | E272/D269 | DISTRIBUTED |  |  | INTRA:flkR |
| #26 | L8 | H2 | 10 | +0.0679 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #2 | L9 | H17 | 44 | +0.1388 | DISTRIBUTED |  | SINGLE-ANCHOR | V201 |  |  |
| #1 | L10 | H9 | 100 | +0.2674 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #28 | L11 | H8 | 26 | +0.0405 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  | CROSS:flkR→ss1 |
| #14 | L11 | H14 | 44 | +0.0797 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #8 | L11 | H16 | 33 | +0.0491 | SINGLE-ANCHOR | V101 | DISTRIBUTED |  |  |  |
| #11 | L12 | H10 | 25 | +0.0481 | DISTRIBUTED |  | DUAL-ANCHOR | V201/E116 |  |  |
| #18 | L13 | H2 | 16 | +0.0417 | SINGLE-ANCHOR | V201 | DISTRIBUTED |  |  | INTRA:ss2 |
| #20 | L14 | H4 | 11 | +0.0750 | SINGLE-ANCHOR | V101 | DUAL-ANCHOR | F203/V201 |  | CROSS:ss2→ss1 |
| #23 | L14 | H9 | 15 | +0.0223 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #29 | L15 | H8 | 5 | +0.0365 | SINGLE-ANCHOR | V101 | SINGLE-ANCHOR | F203 | CROSS_SSE | CROSS:ss2→ss1 |
| #16 | L16 | H7 | 22 | +0.0343 | DISTRIBUTED |  | DISTRIBUTED |  |  | INTRA:ss2 |
| #24 | L16 | H12 | 23 | +0.0468 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL | INTRA:ss2 |
| #30 | L17 | H7 | 29 | +0.0288 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #7 | L17 | H10 | 19 | +0.1211 | SINGLE-ANCHOR | V201 | DISTRIBUTED |  |  | INTRA:ss2 |
| #19 | L17 | H18 | 14 | +0.0443 | DISTRIBUTED |  | DUAL-ANCHOR | V201/F203 |  |  |
| #25 | L19 | H3 | 13 | +0.0471 | SINGLE-ANCHOR | V201 | DISTRIBUTED |  | POSITIONAL | INTRA:ss2 |
| #13 | L26 | H16 | 15 | +0.0457 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #5 | L27 | H15 | 19 | +0.0909 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #6 | L29 | H18 | 20 | +0.1370 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #3 | L32 | H13 | 20 | +0.0683 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #4 | L32 | H18 | 18 | +0.0703 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
