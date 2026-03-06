# Contact Pattern Analysis: 2PKEA

Generated: 2026-03-03 04:17:41   Model: facebook/esm2_t33_650M_UR50D

> **Position convention:** all `q`, `k`, and anchor positions are **0-indexed sequence positions**,
> matching `CONTACT_PAIR` and `sequence_S` indexing.  `seq_S[pos]` gives the amino acid directly.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2PKEA |
| Contact pair | (16, 131) |
| ss1 | [11, 22) |
| ss2 | [126, 137) |
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
| Clean metric | 0.6155 |
| Corrupt metric | 0.0182 |
| Gap | 0.5973 |

## Circuit Discovery

### Minimum K to Reach Faithfulness Target (70%)

| Sort order | min_K | faithfulness_at_K |
|------------|-------|-------------------|
| |indirect| | 200 | 85.23% |
| positive IE | 70 | 77.00% |
| negative IE | 660 | 100.00% |

### Top Indirect Effect Heads (by positive IE)

| Rank | Layer | Head | IE score |
|------|-------|------|----------|
| 1 | L0 | H11 | +0.6096 |
| 2 | L8 | H12 | +0.3584 |
| 3 | L13 | H2 | +0.2169 |
| 4 | L27 | H15 | +0.1802 |
| 5 | L10 | H2 | +0.1365 |
| 6 | L14 | H16 | +0.1143 |
| 7 | L32 | H18 | +0.1096 |
| 8 | L10 | H0 | +0.0993 |
| 9 | L12 | H3 | +0.0991 |
| 10 | L5 | H2 | +0.0971 |
| 11 | L9 | H8 | +0.0895 |
| 12 | L22 | H14 | +0.0876 |
| 13 | L14 | H9 | +0.0835 |
| 14 | L12 | H9 | +0.0815 |
| 15 | L10 | H9 | +0.0809 |
| 16 | L30 | H1 | +0.0799 |
| 17 | L29 | H18 | +0.0744 |
| 18 | L18 | H8 | +0.0740 |
| 19 | L18 | H16 | +0.0734 |
| 20 | L17 | H4 | +0.0707 |
| 21 | L6 | H8 | +0.0670 |
| 22 | L17 | H18 | +0.0638 |
| 23 | L12 | H15 | +0.0607 |
| 24 | L11 | H9 | +0.0597 |
| 25 | L6 | H17 | +0.0585 |
| 26 | L12 | H16 | +0.0560 |
| 27 | L32 | H13 | +0.0529 |
| 28 | L26 | H16 | +0.0512 |
| 29 | L18 | H12 | +0.0511 |
| 30 | L26 | H6 | +0.0497 |

### Faithfulness Sweep (Positive IE)

| k | faithfulness |
|---|--------------|
| 0 | 0.00% |
| 1 | 0.00% |
| 2 | -0.00% |
| 3 | -0.00% |
| 4 | 0.02% |
| 5 | 0.08% |
| 6 | 0.10% |
| 7 | 0.15% |
| 8 | 0.16% |
| 9 | 0.17% |
| 10 | 0.22% |
| 20 | 1.87% |
| 80 | 89.16% |
| 450 | 171.19% |

## Cell Attribution Analysis

Total cells: 4,170,406

- Positive: 2,110,288
- Negative: 2,058,108

**Percentile table:**

| Percentile | Value | Cells above |
|------------|-------|-------------|
| 90th | +0.00000067 | 417,041 |
| 95th | +0.00000219 | 208,521 |
| 99th | +0.00001682 | 41,705 |
| 99.5th | +0.00003672 | 20,853 |
| 99.9th | +0.00021483 | 4,171 |

**Top 20 positive cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L8 | H12 | 16 | ss1 | 183 | flkR | +0.280199 | 0.038755 |
| L10 | H2 | 16 | ss1 | 183 | flkR | +0.270131 | 0.089742 |
| L5 | H2 | 183 | flkR | 190 | flkR | +0.121429 | 0.098013 |
| L10 | H9 | 16 | ss1 | 131 | ss2 | +0.111096 | 0.117951 |
| L12 | H3 | 16 | ss1 | 131 | ss2 | +0.094236 | 0.116060 |
| L13 | H2 | 16 | ss1 | 16 | ss1 | +0.087051 | 0.133507 |
| L6 | H8 | 183 | flkR | 192 | flkR | +0.074593 | 0.081002 |
| L14 | H16 | 12 | ss1 | -1 | other | +0.057391 | 0.374915 |
| L8 | H12 | 131 | ss2 | 183 | flkR | +0.056768 | 0.022580 |
| L11 | H9 | 16 | ss1 | 16 | ss1 | +0.055314 | 0.099736 |
| L14 | H9 | 16 | ss1 | 183 | flkR | +0.050636 | 0.086435 |
| L12 | H17 | 16 | ss1 | 131 | ss2 | +0.048976 | 0.068770 |
| L18 | H16 | 15 | ss1 | 183 | flkR | +0.043594 | 0.596857 |
| L13 | H2 | 12 | ss1 | 16 | ss1 | +0.042182 | 0.087304 |
| L17 | H4 | 16 | ss1 | 18 | ss1 | +0.038789 | 0.529079 |
| L12 | H16 | 16 | ss1 | 183 | flkR | +0.038785 | 0.025820 |
| L18 | H8 | 12 | ss1 | 16 | ss1 | +0.038303 | 0.316010 |
| L14 | H16 | 16 | ss1 | -1 | other | +0.038028 | 0.327105 |
| L18 | H12 | 15 | ss1 | 21 | ss1 | +0.037631 | 0.294709 |
| L17 | H4 | 17 | ss1 | 18 | ss1 | +0.035722 | 0.602796 |

**Top 20 negative cells:**

| Layer | Head | q | q-region | k | k-region | attr | \|diff\| |
|-------|------|---|----------|---|----------|------|--------|
| L16 | H15 | 18 | ss1 | 18 | ss1 | -0.011716 | 0.261602 |
| L9 | H9 | 16 | ss1 | 114 | other | -0.012211 | 0.008032 |
| L13 | H2 | 18 | ss1 | 16 | ss1 | -0.012247 | 0.209318 |
| L9 | H12 | 131 | ss2 | 131 | ss2 | -0.012411 | 0.026060 |
| L17 | H10 | 15 | ss1 | 14 | ss1 | -0.012485 | 0.358031 |
| L10 | H9 | 131 | ss2 | 16 | ss1 | -0.014422 | 0.119236 |
| L12 | H15 | 0 | flkL | 131 | ss2 | -0.015216 | 0.082103 |
| L17 | H4 | 18 | ss1 | 18 | ss1 | -0.015525 | 0.362095 |
| L16 | H9 | 12 | ss1 | 14 | ss1 | -0.015684 | 0.106965 |
| L10 | H2 | 16 | ss1 | 195 | other | -0.016018 | 0.014050 |
| L17 | H10 | 17 | ss1 | 16 | ss1 | -0.017720 | 0.637528 |
| L26 | H16 | 13 | ss1 | 127 | ss2 | -0.020914 | 0.550682 |
| L10 | H2 | 16 | ss1 | 131 | ss2 | -0.021461 | 0.009151 |
| L9 | H6 | 183 | flkR | 196 | other | -0.022927 | 0.040391 |
| L16 | H15 | 12 | ss1 | 21 | ss1 | -0.024532 | 0.083685 |
| L16 | H9 | 12 | ss1 | 5 | flkL | -0.028694 | 0.142865 |
| L5 | H2 | 183 | flkR | 189 | flkR | -0.031530 | 0.037281 |
| L14 | H16 | 12 | ss1 | 16 | ss1 | -0.037670 | 0.130253 |
| L8 | H12 | 16 | ss1 | 131 | ss2 | -0.037901 | 0.013286 |
| L10 | H2 | 16 | ss1 | 16 | ss1 | -0.069917 | 0.085088 |

## Attribution Sufficiency Test

| K | cells | heads | metric | faithfulness |
|---|-------|-------|--------|--------------|
| 0 | 0 | 0 | 0.0182 | 0.00% |
| 10 | 10 | 9 | 0.0182 | -0.00% |
| 20 | 20 | 16 | 0.0182 | 0.00% |
| 50 | 50 | 32 | 0.0182 | 0.00% |
| 100 | 100 | 51 | 0.0198 | 0.27% |
| 200 | 200 | 65 | 0.0309 | 2.13% |
| 500 | 500 | 69 | 0.0954 | 12.93% |
| 1000 | 1,000 | 69 | 0.2555 | 39.72% |
| 2000 | 2,000 | 70 | 0.4847 | 78.10% |
| 5000 | 5,000 | 70 | 0.7897 | 129.17% |
| 10000 | 10,000 | 70 | 0.8773 | 143.83% |
| 20000 | 20,000 | 70 | 0.9405 | 154.41% |
| 50000 | 50,000 | 70 | 0.9654 | 158.57% |

## Motif Analysis

### L0 H11 — Rank #1

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 34  |  total attr: +0.3855

**Key mass** (top-1=20%, top-2=27%, top-3=34%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.0775 | 20.1% |
| 177 | flkR | +0.0261 | 6.8% |
| 186 | flkR | +0.0258 | 6.7% |
| 164 | flkR | +0.0235 | 6.1% |
| 179 | flkR | +0.0224 | 5.8% |

**Query mass** (top-1=86%, top-2=89%, top-3=91%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.3324 | 86.2% |
| 157 | flkR | +0.0101 | 2.6% |
| 173 | flkR | +0.0074 | 1.9% |
| 8 | flkL | +0.0061 | 1.6% |
| 163 | flkR | +0.0059 | 1.5% |

**Offset distribution [frequency]** (top-2 coverage: 6%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +16 | 1 | 2.9% |
| +7 | 1 | 2.9% |
| +0 | 1 | 2.9% |
| +29 | 1 | 2.9% |
| +14 | 1 | 2.9% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=62%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 21 | 61.8% |
| ss2 | flkR | 5 | 14.7% |
| flkR | flkL | 2 | 5.9% |
| flkL | flkR | 2 | 5.9% |
| flkR | ss1 | 1 | 2.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 193 | flkR | 177 | flkR | +0.0261 | 0.0355 |
| 193 | flkR | 186 | flkR | +0.0258 | 0.0338 |
| 193 | flkR | 193 | flkR | +0.0244 | 0.0356 |
| 193 | flkR | 164 | flkR | +0.0235 | 0.0320 |
| 193 | flkR | 179 | flkR | +0.0224 | 0.0325 |

### L5 H2 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 13  |  total attr: +0.1639

**Key mass** (top-1=89%, top-2=95%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 190 | flkR | +0.1460 | 89.1% |
| 188 | flkR | +0.0101 | 6.2% |
| 163 | flkR | +0.0019 | 1.2% |
| 18 | ss1 | +0.0018 | 1.1% |
| 175 | flkR | +0.0015 | 0.9% |

**Query mass** (top-1=81%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.1330 | 81.1% |
| 182 | flkR | +0.0133 | 8.1% |
| 181 | flkR | +0.0058 | 3.5% |
| 184 | flkR | +0.0057 | 3.5% |
| 131 | ss2 | +0.0019 | 1.2% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -6 | 2 | 15.4% |
| -4 | 2 | 15.4% |
| -7 | 1 | 7.7% |
| -8 | 1 | 7.7% |
| -5 | 1 | 7.7% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=77%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 10 | 76.9% |
| ss2 | flkR | 2 | 15.4% |
| ss1 | ss1 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | flkR | 190 | flkR | +0.1214 | 0.0980 |
| 182 | flkR | 190 | flkR | +0.0107 | 0.0984 |
| 183 | flkR | 188 | flkR | +0.0075 | 0.0181 |
| 181 | flkR | 190 | flkR | +0.0058 | 0.0593 |
| 184 | flkR | 190 | flkR | +0.0057 | 0.1775 |

### L6 H8 — Rank #21

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 6  |  total attr: +0.0844

**Key mass** (top-1=94%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 192 | flkR | +0.0795 | 94.3% |
| 193 | flkR | +0.0026 | 3.0% |
| 8 | flkL | +0.0012 | 1.4% |
| 16 | ss1 | +0.0011 | 1.3% |

**Query mass** (top-1=90%, top-2=93%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0757 | 89.8% |
| 182 | flkR | +0.0031 | 3.7% |
| 201 | other | +0.0026 | 3.0% |
| 181 | flkR | +0.0018 | 2.1% |
| 16 | ss1 | +0.0012 | 1.4% |

**Offset distribution [frequency]** (top-2 coverage: 50%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +8 | 2 | 33.3% |
| -9 | 1 | 16.7% |
| -10 | 1 | 16.7% |
| -11 | 1 | 16.7% |
| +167 | 1 | 16.7% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 3 | 50.0% |
| other | flkR | 1 | 16.7% |
| ss1 | flkL | 1 | 16.7% |
| flkR | ss1 | 1 | 16.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | flkR | 192 | flkR | +0.0746 | 0.0810 |
| 182 | flkR | 192 | flkR | +0.0031 | 0.1097 |
| 201 | other | 193 | flkR | +0.0026 | 0.0153 |
| 181 | flkR | 192 | flkR | +0.0018 | 0.0763 |
| 16 | ss1 | 8 | flkL | +0.0012 | 0.0014 |

### L6 H17 — Rank #25

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 36  |  total attr: +0.1129

**Key mass** (top-1=9%, top-2=18%, top-3=25%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 192 | flkR | +0.0103 | 9.1% |
| 14 | ss1 | +0.0098 | 8.7% |
| 169 | flkR | +0.0087 | 7.7% |
| 189 | flkR | +0.0086 | 7.6% |
| 185 | flkR | +0.0081 | 7.1% |

**Query mass** (top-1=18%, top-2=30%, top-3=40%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 185 | flkR | +0.0202 | 17.9% |
| 14 | ss1 | +0.0141 | 12.5% |
| 183 | flkR | +0.0111 | 9.8% |
| 129 | ss2 | +0.0087 | 7.7% |
| 189 | flkR | +0.0085 | 7.5% |

**Offset distribution [frequency]** (top-2 coverage: 39%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 12 | 33.3% |
| -40 | 2 | 5.6% |
| +54 | 2 | 5.6% |
| +10 | 2 | 5.6% |
| +16 | 2 | 5.6% |

**Region-pair profile** (q→k)  (top=39%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 14 | 38.9% |
| ss2 | flkR | 3 | 8.3% |
| flkR | ss2 | 3 | 8.3% |
| ss2 | ss2 | 3 | 8.3% |
| flkL | flkL | 3 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 14 | ss1 | 14 | ss1 | +0.0098 | 0.0078 |
| 129 | ss2 | 169 | flkR | +0.0087 | 0.0331 |
| 183 | flkR | 192 | flkR | +0.0074 | 0.0064 |
| 185 | flkR | 185 | flkR | +0.0068 | 0.0280 |
| 189 | flkR | 189 | flkR | +0.0063 | 0.1969 |

### L8 H12 — Rank #2

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 19  |  total attr: +0.3682

**Key mass** (top-1=99%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.3644 | 99.0% |
| 131 | ss2 | +0.0038 | 1.0% |

**Query mass** (top-1=76%, top-2=92%, top-3=93%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.2802 | 76.1% |
| 131 | ss2 | +0.0568 | 15.4% |
| 183 | flkR | +0.0038 | 1.0% |
| 18 | ss1 | +0.0035 | 0.9% |
| 20 | ss1 | +0.0032 | 0.9% |

**Offset distribution [frequency]** (top-2 coverage: 11%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 1 | 5.3% |
| -52 | 1 | 5.3% |
| +52 | 1 | 5.3% |
| -165 | 1 | 5.3% |
| -163 | 1 | 5.3% |

**Region-pair profile** (q→k)  (top=68%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | flkR | 13 | 68.4% |
| ss1 | flkR | 4 | 21.1% |
| ss2 | flkR | 1 | 5.3% |
| flkR | ss2 | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 183 | flkR | +0.2802 | 0.0388 |
| 131 | ss2 | 183 | flkR | +0.0568 | 0.0226 |
| 183 | flkR | 131 | ss2 | +0.0038 | 0.0186 |
| 18 | ss1 | 183 | flkR | +0.0035 | 0.0595 |
| 20 | ss1 | 183 | flkR | +0.0032 | 0.0237 |

### L9 H8 — Rank #11

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | INTRA:flkR  |  cells: 16  |  total attr: +0.0478

**Key mass** (top-1=42%, top-2=53%, top-3=61%)  [DISTR(E193/M183/?-1/V182/D126)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 193 | flkR | +0.0200 | 41.9% |
| 183 | flkR | +0.0053 | 11.1% |
| -1 | other | +0.0037 | 7.7% |
| 182 | flkR | +0.0030 | 6.3% |
| 126 | ss2 | +0.0028 | 5.8% |

**Query mass** (top-1=56%, top-2=78%, top-3=91%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0268 | 56.1% |
| 16 | ss1 | +0.0104 | 21.8% |
| 131 | ss2 | +0.0061 | 12.7% |
| -1 | other | +0.0033 | 6.9% |
| 20 | ss1 | +0.0012 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 12.5% |
| +1 | 2 | 12.5% |
| -10 | 1 | 6.2% |
| -177 | 1 | 6.2% |
| -62 | 1 | 6.2% |

**Region-pair profile** (q→k)  [INTRA:flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 8 | 50.0% |
| ss1 | ss1 | 2 | 12.5% |
| ss1 | flkR | 1 | 6.2% |
| ss2 | flkR | 1 | 6.2% |
| ss1 | other | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 183 | flkR | 193 | flkR | +0.0070 | 0.0199 |
| 183 | flkR | 183 | flkR | +0.0053 | 0.0181 |
| 16 | ss1 | 193 | flkR | +0.0052 | 0.0060 |
| 131 | ss2 | 193 | flkR | +0.0046 | 0.0133 |
| 16 | ss1 | -1 | other | +0.0037 | 0.0036 |

### L10 H0 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 16  |  total attr: +0.1482

**Key mass** (top-1=98%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.1452 | 98.0% |
| 183 | flkR | +0.0018 | 1.2% |
| 131 | ss2 | +0.0011 | 0.8% |

**Query mass** (top-1=23%, top-2=42%, top-3=53%)  [DISTR(D21/D20/T22/G16/L14)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 21 | ss1 | +0.0344 | 23.2% |
| 20 | ss1 | +0.0279 | 18.8% |
| 22 | other | +0.0158 | 10.7% |
| 16 | ss1 | +0.0141 | 9.5% |
| 14 | ss1 | +0.0134 | 9.0% |

**Offset distribution [frequency]** (top-2 coverage: 19%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +12 | 2 | 12.5% |
| +5 | 1 | 6.2% |
| +4 | 1 | 6.2% |
| +6 | 1 | 6.2% |
| +0 | 1 | 6.2% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=44%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 7 | 43.8% |
| other | ss1 | 7 | 43.8% |
| other | flkR | 1 | 6.2% |
| ss2 | ss2 | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 21 | ss1 | 16 | ss1 | +0.0344 | 0.1351 |
| 20 | ss1 | 16 | ss1 | +0.0279 | 0.1338 |
| 22 | other | 16 | ss1 | +0.0158 | 0.1279 |
| 16 | ss1 | 16 | ss1 | +0.0141 | 0.0746 |
| 14 | ss1 | 16 | ss1 | +0.0134 | 0.0854 |

### L10 H2 — Rank #5

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→flkR  |  cells: 8  |  total attr: +0.3111

**Key mass** (top-1=92%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.2848 | 91.5% |
| 16 | ss1 | +0.0242 | 7.8% |
| 195 | other | +0.0022 | 0.7% |

**Query mass** (top-1=87%, top-2=95%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.2701 | 86.8% |
| -1 | other | +0.0242 | 7.8% |
| 14 | ss1 | +0.0050 | 1.6% |
| 12 | ss1 | +0.0050 | 1.6% |
| 21 | ss1 | +0.0042 | 1.4% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 1 | 12.5% |
| -17 | 1 | 12.5% |
| -169 | 1 | 12.5% |
| -162 | 1 | 12.5% |
| -171 | 1 | 12.5% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=75%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 6 | 75.0% |
| other | ss1 | 1 | 12.5% |
| ss1 | other | 1 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 183 | flkR | +0.2701 | 0.0897 |
| -1 | other | 16 | ss1 | +0.0242 | 0.1349 |
| 14 | ss1 | 183 | flkR | +0.0050 | 0.0424 |
| 21 | ss1 | 183 | flkR | +0.0042 | 0.0210 |
| 12 | ss1 | 183 | flkR | +0.0029 | 0.0321 |

### L10 H9 — Rank #15

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 14  |  total attr: +0.1662

**Key mass** (top-1=70%, top-2=94%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss2 | +0.1164 | 70.0% |
| 183 | flkR | +0.0401 | 24.1% |
| 16 | ss1 | +0.0079 | 4.8% |
| 195 | other | +0.0018 | 1.1% |

**Query mass** (top-1=80%, top-2=85%, top-3=88%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.1336 | 80.4% |
| 21 | ss1 | +0.0071 | 4.3% |
| 14 | ss1 | +0.0056 | 3.4% |
| 20 | ss1 | +0.0047 | 2.8% |
| -1 | other | +0.0043 | 2.6% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 1 | 7.1% |
| -167 | 1 | 7.1% |
| -169 | 1 | 7.1% |
| +5 | 1 | 7.1% |
| -184 | 1 | 7.1% |

**Region-pair profile** (q→k)  (top=29%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 4 | 28.6% |
| ss1 | ss2 | 3 | 21.4% |
| ss1 | ss1 | 2 | 14.3% |
| other | flkR | 2 | 14.3% |
| flkL | flkR | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 131 | ss2 | +0.1111 | 0.1180 |
| 16 | ss1 | 183 | flkR | +0.0225 | 0.1219 |
| 14 | ss1 | 183 | flkR | +0.0056 | 0.0534 |
| 21 | ss1 | 16 | ss1 | +0.0048 | 0.0378 |
| -1 | other | 183 | flkR | +0.0043 | 0.0487 |

### L11 H9 — Rank #24

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 7  |  total attr: +0.0662

**Key mass** (top-1=85%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0564 | 85.1% |
| 15 | ss1 | +0.0026 | 3.9% |
| 195 | other | +0.0025 | 3.7% |
| -1 | other | +0.0020 | 3.0% |
| 21 | ss1 | +0.0017 | 2.5% |

**Query mass** (top-1=90%, top-2=94%, top-3=97%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0595 | 89.9% |
| 183 | flkR | +0.0025 | 3.7% |
| -1 | other | +0.0020 | 3.0% |
| 0 | flkL | +0.0012 | 1.8% |
| 9 | flkL | +0.0011 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 43%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 28.6% |
| +1 | 1 | 14.3% |
| -12 | 1 | 14.3% |
| -5 | 1 | 14.3% |
| -6 | 1 | 14.3% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 3 | 42.9% |
| flkR | other | 1 | 14.3% |
| other | other | 1 | 14.3% |
| flkL | flkL | 1 | 14.3% |
| flkL | ss1 | 1 | 14.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 16 | ss1 | +0.0553 | 0.0997 |
| 16 | ss1 | 15 | ss1 | +0.0026 | 0.0081 |
| 183 | flkR | 195 | other | +0.0025 | 0.0386 |
| -1 | other | -1 | other | +0.0020 | 0.0475 |
| 16 | ss1 | 21 | ss1 | +0.0017 | 0.0085 |

### L12 H3 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS:ss1→ss2  |  cells: 12  |  total attr: +0.1263

**Key mass** (top-1=86%, top-2=90%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss2 | +0.1092 | 86.5% |
| 21 | ss1 | +0.0043 | 3.4% |
| 20 | ss1 | +0.0035 | 2.8% |
| 18 | ss1 | +0.0029 | 2.3% |
| 16 | ss1 | +0.0021 | 1.6% |

**Query mass** (top-1=87%, top-2=91%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.1093 | 86.5% |
| 17 | ss1 | +0.0057 | 4.5% |
| 3 | flkL | +0.0048 | 3.8% |
| 19 | ss1 | +0.0030 | 2.4% |
| -1 | other | +0.0021 | 1.6% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -128 | 2 | 16.7% |
| -115 | 1 | 8.3% |
| -114 | 1 | 8.3% |
| -5 | 1 | 8.3% |
| -4 | 1 | 8.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=42%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 5 | 41.7% |
| ss1 | ss1 | 3 | 25.0% |
| flkL | ss2 | 2 | 16.7% |
| other | ss1 | 1 | 8.3% |
| ss1 | flkR | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 131 | ss2 | +0.0942 | 0.1161 |
| 17 | ss1 | 131 | ss2 | +0.0057 | 0.0583 |
| 3 | flkL | 131 | ss2 | +0.0048 | 0.0654 |
| 16 | ss1 | 21 | ss1 | +0.0043 | 0.0135 |
| 16 | ss1 | 20 | ss1 | +0.0035 | 0.0113 |

### L12 H9 — Rank #14

**Tags:** k:MULTI-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 14  |  total attr: +0.1125

**Key mass** (top-1=36%, top-2=64%, top-3=87%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0402 | 35.7% |
| 21 | ss1 | +0.0313 | 27.8% |
| 20 | ss1 | +0.0259 | 23.0% |
| 18 | ss1 | +0.0069 | 6.2% |
| 19 | ss1 | +0.0045 | 4.0% |

**Query mass** (top-1=65%, top-2=76%, top-3=82%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0735 | 65.3% |
| 21 | ss1 | +0.0117 | 10.4% |
| 18 | ss1 | +0.0073 | 6.5% |
| 19 | ss1 | +0.0061 | 5.4% |
| 20 | ss1 | +0.0059 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -4 | 3 | 21.4% |
| +3 | 2 | 14.3% |
| -5 | 1 | 7.1% |
| +5 | 1 | 7.1% |
| +2 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=79%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 78.6% |
| other | ss1 | 1 | 7.1% |
| flkL | flkL | 1 | 7.1% |
| ss1 | other | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 21 | ss1 | +0.0313 | 0.0427 |
| 16 | ss1 | 20 | ss1 | +0.0259 | 0.0293 |
| 21 | ss1 | 16 | ss1 | +0.0117 | 0.0887 |
| 18 | ss1 | 16 | ss1 | +0.0073 | 0.1172 |
| 16 | ss1 | 18 | ss1 | +0.0069 | 0.0073 |

### L12 H15 — Rank #23

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 20  |  total attr: +0.0871

**Key mass** (top-1=58%, top-2=85%, top-3=95%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss2 | +0.0509 | 58.4% |
| 16 | ss1 | +0.0230 | 26.4% |
| 183 | flkR | +0.0091 | 10.5% |
| 130 | ss2 | +0.0015 | 1.8% |
| 128 | ss2 | +0.0013 | 1.5% |

**Query mass** (top-1=22%, top-2=42%, top-3=58%)  [DISTR(G16/G0/I12/?-1/D21)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0195 | 22.3% |
| 0 | flkL | +0.0171 | 19.6% |
| 12 | ss1 | +0.0138 | 15.8% |
| -1 | other | +0.0098 | 11.3% |
| 21 | ss1 | +0.0061 | 7.0% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 2 | 10.0% |
| -118 | 2 | 10.0% |
| -16 | 1 | 5.0% |
| -167 | 1 | 5.0% |
| -119 | 1 | 5.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 45.0% |
| flkL | ss2 | 4 | 20.0% |
| flkL | ss1 | 2 | 10.0% |
| other | ss2 | 2 | 10.0% |
| ss1 | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 0 | flkL | 16 | ss1 | +0.0171 | 0.0664 |
| 16 | ss1 | 131 | ss2 | +0.0103 | 0.0378 |
| 16 | ss1 | 183 | flkR | +0.0091 | 0.0084 |
| 12 | ss1 | 131 | ss2 | +0.0076 | 0.0240 |
| -1 | other | 131 | ss2 | +0.0074 | 0.0479 |

### L12 H16 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR  |  cells: 5  |  total attr: +0.0616

**Key mass** (top-1=91%, top-2=96%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0561 | 91.2% |
| 131 | ss2 | +0.0028 | 4.5% |
| -1 | other | +0.0013 | 2.2% |
| 195 | other | +0.0013 | 2.1% |

**Query mass** (top-1=65%, top-2=98%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0401 | 65.2% |
| -1 | other | +0.0201 | 32.7% |
| 183 | flkR | +0.0013 | 2.2% |

**Offset distribution [frequency]** (top-2 coverage: 40%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 1 | 20.0% |
| -184 | 1 | 20.0% |
| -132 | 1 | 20.0% |
| +184 | 1 | 20.0% |
| -179 | 1 | 20.0% |

**Region-pair profile** (q→k)  (top=20%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 1 | 20.0% |
| other | flkR | 1 | 20.0% |
| other | ss2 | 1 | 20.0% |
| flkR | other | 1 | 20.0% |
| ss1 | other | 1 | 20.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 183 | flkR | +0.0388 | 0.0258 |
| -1 | other | 183 | flkR | +0.0173 | 0.0304 |
| -1 | other | 131 | ss2 | +0.0028 | 0.0169 |
| 183 | flkR | -1 | other | +0.0013 | 0.0105 |
| 16 | ss1 | 195 | other | +0.0013 | 0.0022 |

### L13 H2 — Rank #3

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss1  |  cells: 28  |  total attr: +0.2289

**Key mass** (top-1=86%, top-2=89%, top-3=91%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.1966 | 85.9% |
| 14 | ss1 | +0.0067 | 2.9% |
| 18 | ss1 | +0.0040 | 1.7% |
| 17 | ss1 | +0.0029 | 1.3% |
| 15 | ss1 | +0.0026 | 1.2% |

**Query mass** (top-1=50%, top-2=69%, top-3=77%)  [DISTR(G16/I12/L14)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.1134 | 49.6% |
| 12 | ss1 | +0.0448 | 19.6% |
| 14 | ss1 | +0.0173 | 7.6% |
| 17 | ss1 | +0.0136 | 6.0% |
| 23 | other | +0.0080 | 3.5% |

**Offset distribution [frequency]** (top-2 coverage: 21%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 3 | 10.7% |
| +1 | 3 | 10.7% |
| +2 | 3 | 10.7% |
| -4 | 2 | 7.1% |
| -1 | 2 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=61%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 17 | 60.7% |
| other | ss1 | 5 | 17.9% |
| ss1 | flkL | 3 | 10.7% |
| ss1 | other | 1 | 3.6% |
| other | other | 1 | 3.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 16 | ss1 | +0.0871 | 0.1335 |
| 12 | ss1 | 16 | ss1 | +0.0422 | 0.0873 |
| 14 | ss1 | 16 | ss1 | +0.0173 | 0.1469 |
| 17 | ss1 | 16 | ss1 | +0.0136 | 0.2741 |
| 23 | other | 16 | ss1 | +0.0080 | 0.2236 |

### L14 H9 — Rank #13

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 17  |  total attr: +0.1098

**Key mass** (top-1=50%, top-2=93%, top-3=96%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0554 | 50.5% |
| 131 | ss2 | +0.0472 | 43.0% |
| 144 | flkR | +0.0029 | 2.6% |
| 16 | ss1 | +0.0027 | 2.5% |
| 0 | flkL | +0.0016 | 1.5% |

**Query mass** (top-1=52%, top-2=70%, top-3=79%)  [DISTR(G16/?-1/D21)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0573 | 52.2% |
| -1 | other | +0.0192 | 17.5% |
| 21 | ss1 | +0.0097 | 8.9% |
| 12 | ss1 | +0.0091 | 8.3% |
| 19 | ss1 | +0.0037 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 12%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 1 | 5.9% |
| -132 | 1 | 5.9% |
| -110 | 1 | 5.9% |
| -119 | 1 | 5.9% |
| -112 | 1 | 5.9% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=47%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 47.1% |
| ss1 | flkR | 5 | 29.4% |
| ss1 | ss1 | 2 | 11.8% |
| other | ss2 | 1 | 5.9% |
| ss1 | flkL | 1 | 5.9% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 183 | flkR | +0.0506 | 0.0864 |
| -1 | other | 131 | ss2 | +0.0192 | 0.1016 |
| 21 | ss1 | 131 | ss2 | +0.0080 | 0.0901 |
| 12 | ss1 | 131 | ss2 | +0.0044 | 0.0186 |
| 19 | ss1 | 131 | ss2 | +0.0037 | 0.1205 |

### L14 H16 — Rank #6

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 31  |  total attr: +0.2370

**Key mass** (top-1=67%, top-2=94%, top-3=95%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| -1 | other | +0.1591 | 67.1% |
| 16 | ss1 | +0.0632 | 26.7% |
| 189 | flkR | +0.0029 | 1.2% |
| 19 | ss1 | +0.0025 | 1.0% |
| 18 | ss1 | +0.0022 | 0.9% |

**Query mass** (top-1=24%, top-2=44%, top-3=52%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 12 | ss1 | +0.0574 | 24.2% |
| 16 | ss1 | +0.0461 | 19.4% |
| 18 | ss1 | +0.0208 | 8.8% |
| 15 | ss1 | +0.0196 | 8.3% |
| 5 | flkL | +0.0171 | 7.2% |

**Offset distribution [frequency]** (top-2 coverage: 13%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +4 | 2 | 6.5% |
| -6 | 2 | 6.5% |
| +13 | 1 | 3.2% |
| +17 | 1 | 3.2% |
| +2 | 1 | 3.2% |

**Region-pair profile** (q→k)  (top=26%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | ss1 | 8 | 25.8% |
| ss1 | ss1 | 7 | 22.6% |
| ss1 | other | 6 | 19.4% |
| ss1 | flkR | 4 | 12.9% |
| flkL | other | 2 | 6.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 12 | ss1 | -1 | other | +0.0574 | 0.3749 |
| 16 | ss1 | -1 | other | +0.0380 | 0.3271 |
| 18 | ss1 | 16 | ss1 | +0.0208 | 0.2050 |
| 5 | flkL | -1 | other | +0.0171 | 0.3168 |
| 15 | ss1 | -1 | other | +0.0129 | 0.4273 |

### L17 H4 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:MULTI-ANCHOR | INTRA:ss1  |  cells: 14  |  total attr: +0.1237

**Key mass** (top-1=87%, top-2=93%, top-3=96%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 18 | ss1 | +0.1082 | 87.4% |
| 20 | ss1 | +0.0070 | 5.7% |
| -1 | other | +0.0038 | 3.0% |
| 195 | other | +0.0017 | 1.4% |
| 14 | ss1 | +0.0015 | 1.2% |

**Query mass** (top-1=31%, top-2=60%, top-3=83%)  [MULTI-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0388 | 31.3% |
| 17 | ss1 | +0.0357 | 28.9% |
| 15 | ss1 | +0.0283 | 22.9% |
| 21 | ss1 | +0.0070 | 5.6% |
| 12 | ss1 | +0.0068 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 2 | 14.3% |
| +1 | 2 | 14.3% |
| -1 | 1 | 7.1% |
| -3 | 1 | 7.1% |
| +13 | 1 | 7.1% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=57%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 8 | 57.1% |
| ss1 | other | 2 | 14.3% |
| flkL | ss1 | 2 | 14.3% |
| other | other | 1 | 7.1% |
| other | ss1 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 16 | ss1 | 18 | ss1 | +0.0388 | 0.5291 |
| 17 | ss1 | 18 | ss1 | +0.0357 | 0.6028 |
| 15 | ss1 | 18 | ss1 | +0.0283 | 0.2619 |
| 21 | ss1 | 20 | ss1 | +0.0059 | 0.3305 |
| 12 | ss1 | -1 | other | +0.0020 | 0.1672 |

### L17 H18 — Rank #22

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:ss1→flkR  |  cells: 14  |  total attr: +0.0529

**Key mass** (top-1=60%, top-2=70%, top-3=75%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0318 | 60.2% |
| 15 | ss1 | +0.0051 | 9.6% |
| 0 | flkL | +0.0028 | 5.2% |
| 14 | ss1 | +0.0023 | 4.4% |
| 13 | ss1 | +0.0023 | 4.3% |

**Query mass** (top-1=22%, top-2=39%, top-3=55%)  [DISTR(V15/I12/V129/F17/G16)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 15 | ss1 | +0.0118 | 22.3% |
| 12 | ss1 | +0.0090 | 17.0% |
| 129 | ss2 | +0.0084 | 16.0% |
| 17 | ss1 | +0.0078 | 14.7% |
| 16 | ss1 | +0.0068 | 12.8% |

**Offset distribution [frequency]** (top-2 coverage: 36%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 3 | 21.4% |
| -166 | 2 | 14.3% |
| +115 | 2 | 14.3% |
| -168 | 1 | 7.1% |
| +114 | 1 | 7.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 7 | 50.0% |
| ss2 | ss1 | 4 | 28.6% |
| flkL | flkR | 1 | 7.1% |
| ss1 | flkL | 1 | 7.1% |
| flkR | ss1 | 1 | 7.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 15 | ss1 | 183 | flkR | +0.0118 | 0.2998 |
| 17 | ss1 | 183 | flkR | +0.0078 | 0.3627 |
| 16 | ss1 | 183 | flkR | +0.0068 | 0.2339 |
| 129 | ss2 | 15 | ss1 | +0.0051 | 0.2316 |
| 5 | flkL | 183 | flkR | +0.0036 | 0.0861 |

### L18 H8 — Rank #18

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 18  |  total attr: +0.0922

**Key mass** (top-1=48%, top-2=70%, top-3=78%)  [DISTR(G16/D18/D20)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0443 | 48.0% |
| 18 | ss1 | +0.0203 | 22.0% |
| 20 | ss1 | +0.0075 | 8.2% |
| 17 | ss1 | +0.0068 | 7.4% |
| 14 | ss1 | +0.0038 | 4.1% |

**Query mass** (top-1=63%, top-2=75%, top-3=83%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 12 | ss1 | +0.0585 | 63.4% |
| 15 | ss1 | +0.0107 | 11.6% |
| 13 | ss1 | +0.0077 | 8.4% |
| 18 | ss1 | +0.0075 | 8.2% |
| 14 | ss1 | +0.0034 | 3.7% |

**Offset distribution [frequency]** (top-2 coverage: 44%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -2 | 5 | 27.8% |
| -4 | 3 | 16.7% |
| -3 | 3 | 16.7% |
| -5 | 2 | 11.1% |
| -6 | 1 | 5.6% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=78%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 14 | 77.8% |
| ss1 | flkL | 2 | 11.1% |
| flkL | ss1 | 1 | 5.6% |
| other | other | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 12 | ss1 | 16 | ss1 | +0.0383 | 0.3160 |
| 15 | ss1 | 18 | ss1 | +0.0078 | 0.0988 |
| 12 | ss1 | 18 | ss1 | +0.0078 | 0.0578 |
| 18 | ss1 | 20 | ss1 | +0.0075 | 0.4482 |
| 12 | ss1 | 14 | ss1 | +0.0038 | 0.1478 |

### L18 H12 — Rank #29

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 16  |  total attr: +0.0848

**Key mass** (top-1=51%, top-2=68%, top-3=79%)  [DISTR(D21/I12/L14)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 21 | ss1 | +0.0432 | 50.9% |
| 12 | ss1 | +0.0144 | 17.0% |
| 14 | ss1 | +0.0095 | 11.2% |
| 20 | ss1 | +0.0057 | 6.7% |
| 0 | flkL | +0.0036 | 4.3% |

**Query mass** (top-1=61%, top-2=88%, top-3=94%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 15 | ss1 | +0.0520 | 61.3% |
| 12 | ss1 | +0.0224 | 26.5% |
| 17 | ss1 | +0.0051 | 6.0% |
| 16 | ss1 | +0.0039 | 4.5% |
| 11 | ss1 | +0.0014 | 1.7% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +3 | 3 | 18.8% |
| -5 | 2 | 12.5% |
| -4 | 2 | 12.5% |
| -6 | 1 | 6.2% |
| +0 | 1 | 6.2% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=69%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 11 | 68.8% |
| ss1 | flkL | 3 | 18.8% |
| ss1 | other | 2 | 12.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 15 | ss1 | 21 | ss1 | +0.0376 | 0.2947 |
| 12 | ss1 | 12 | ss1 | +0.0114 | 0.0785 |
| 15 | ss1 | 20 | ss1 | +0.0057 | 0.0384 |
| 15 | ss1 | 14 | ss1 | +0.0046 | 0.0570 |
| 12 | ss1 | 0 | flkL | +0.0036 | 0.0305 |

### L18 H16 — Rank #19

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→flkR  |  cells: 16  |  total attr: +0.0996

**Key mass** (top-1=76%, top-2=80%, top-3=84%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0756 | 75.9% |
| 20 | ss1 | +0.0043 | 4.3% |
| 186 | flkR | +0.0041 | 4.1% |
| 16 | ss1 | +0.0040 | 4.1% |
| -1 | other | +0.0039 | 4.0% |

**Query mass** (top-1=46%, top-2=76%, top-3=87%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 15 | ss1 | +0.0457 | 45.9% |
| 12 | ss1 | +0.0299 | 30.0% |
| 17 | ss1 | +0.0109 | 11.0% |
| 16 | ss1 | +0.0100 | 10.0% |
| -1 | other | +0.0031 | 3.1% |

**Offset distribution [frequency]** (top-2 coverage: 25%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -167 | 2 | 12.5% |
| -166 | 2 | 12.5% |
| -168 | 1 | 6.2% |
| -171 | 1 | 6.2% |
| -4 | 1 | 6.2% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 8 | 50.0% |
| ss1 | ss1 | 4 | 25.0% |
| ss1 | ss2 | 2 | 12.5% |
| ss1 | other | 1 | 6.2% |
| other | flkR | 1 | 6.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 15 | ss1 | 183 | flkR | +0.0436 | 0.5969 |
| 16 | ss1 | 183 | flkR | +0.0100 | 0.3890 |
| 17 | ss1 | 183 | flkR | +0.0096 | 0.6839 |
| 12 | ss1 | 183 | flkR | +0.0093 | 0.0424 |
| 12 | ss1 | 16 | ss1 | +0.0040 | 0.0150 |

### L22 H14 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 13  |  total attr: +0.0672

**Key mass** (top-1=37%, top-2=62%, top-3=75%)  [DISTR(M183/L14/G16)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 183 | flkR | +0.0248 | 37.0% |
| 14 | ss1 | +0.0166 | 24.7% |
| 16 | ss1 | +0.0088 | 13.1% |
| 129 | ss2 | +0.0074 | 11.0% |
| 181 | flkR | +0.0044 | 6.6% |

**Query mass** (top-1=38%, top-2=55%, top-3=68%)  [DISTR(V15/V130/V129/I132)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 15 | ss1 | +0.0255 | 37.9% |
| 130 | ss2 | +0.0114 | 16.9% |
| 129 | ss2 | +0.0089 | 13.2% |
| 132 | ss2 | +0.0088 | 13.1% |
| 127 | ss2 | +0.0040 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 31%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +116 | 2 | 15.4% |
| +115 | 2 | 15.4% |
| -165 | 2 | 15.4% |
| -53 | 2 | 15.4% |
| -168 | 1 | 7.7% |

**Region-pair profile** (q→k)  (top=31%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 4 | 30.8% |
| ss1 | flkR | 3 | 23.1% |
| ss1 | ss2 | 2 | 15.4% |
| ss2 | flkR | 2 | 15.4% |
| ss2 | ss2 | 1 | 7.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 15 | ss1 | 183 | flkR | +0.0220 | 0.3282 |
| 130 | ss2 | 14 | ss1 | +0.0098 | 0.2253 |
| 132 | ss2 | 16 | ss1 | +0.0088 | 0.4357 |
| 129 | ss2 | 14 | ss1 | +0.0068 | 0.3689 |
| 127 | ss2 | 12 | ss1 | +0.0040 | 0.1448 |

### L26 H6 — Rank #30

**Tags:** k:DUAL-ANCHOR / q:SINGLE-ANCHOR | INTRA:ss1  |  cells: 5  |  total attr: +0.0755

**Key mass** (top-1=42%, top-2=82%, top-3=91%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 14 | ss1 | +0.0317 | 42.0% |
| 15 | ss1 | +0.0304 | 40.2% |
| 20 | ss1 | +0.0067 | 8.9% |
| 17 | ss1 | +0.0039 | 5.2% |
| 18 | ss1 | +0.0028 | 3.8% |

**Query mass** (top-1=82%, top-2=91%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 12 | ss1 | +0.0621 | 82.2% |
| 15 | ss1 | +0.0067 | 8.9% |
| 17 | ss1 | +0.0067 | 8.9% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -3 | 3 | 60.0% |
| -2 | 2 | 40.0% |

**Region-pair profile** (q→k)  [INTRA:ss1]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss1 | 5 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 12 | ss1 | 14 | ss1 | +0.0317 | 0.5238 |
| 12 | ss1 | 15 | ss1 | +0.0304 | 0.5253 |
| 17 | ss1 | 20 | ss1 | +0.0067 | 0.2845 |
| 15 | ss1 | 17 | ss1 | +0.0039 | 0.0984 |
| 15 | ss1 | 18 | ss1 | +0.0028 | 0.0690 |

### L26 H16 — Rank #28

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 19  |  total attr: +0.0587

**Key mass** (top-1=34%, top-2=60%, top-3=68%)  [DISTR(V129/Y127/G135/A128)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss2 | +0.0201 | 34.3% |
| 127 | ss2 | +0.0150 | 25.6% |
| 135 | ss2 | +0.0049 | 8.3% |
| 128 | ss2 | +0.0045 | 7.7% |
| 143 | flkR | +0.0036 | 6.1% |

**Query mass** (top-1=38%, top-2=51%, top-3=60%)  [DISTR(V15/L14/I12/F17/G16)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 15 | ss1 | +0.0223 | 38.1% |
| 14 | ss1 | +0.0079 | 13.4% |
| 12 | ss1 | +0.0051 | 8.7% |
| 17 | ss1 | +0.0044 | 7.5% |
| 16 | ss1 | +0.0035 | 5.9% |

**Offset distribution [frequency]** (top-2 coverage: 37%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 4 | 21.1% |
| -114 | 3 | 15.8% |
| -112 | 3 | 15.8% |
| -116 | 2 | 10.5% |
| -120 | 1 | 5.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=68%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 13 | 68.4% |
| ss1 | flkR | 4 | 21.1% |
| flkL | ss2 | 2 | 10.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 15 | ss1 | 129 | ss2 | +0.0139 | 0.3668 |
| 15 | ss1 | 127 | ss2 | +0.0062 | 0.1119 |
| 14 | ss1 | 128 | ss2 | +0.0045 | 0.3141 |
| 14 | ss1 | 129 | ss2 | +0.0034 | 0.0880 |
| 12 | ss1 | 127 | ss2 | +0.0034 | 0.2677 |

### L27 H15 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 21  |  total attr: +0.0737

**Key mass** (top-1=33%, top-2=46%, top-3=58%)  [DISTR(G16/V130/V15/F17/V129)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0244 | 33.1% |
| 130 | ss2 | +0.0097 | 13.2% |
| 15 | ss1 | +0.0084 | 11.5% |
| 17 | ss1 | +0.0059 | 8.1% |
| 129 | ss2 | +0.0040 | 5.5% |

**Query mass** (top-1=21%, top-2=38%, top-3=54%)  [DISTR(V129/I132/L14/F17/Y127)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss2 | +0.0155 | 21.0% |
| 132 | ss2 | +0.0122 | 16.5% |
| 14 | ss1 | +0.0120 | 16.3% |
| 17 | ss1 | +0.0070 | 9.5% |
| 127 | ss2 | +0.0062 | 8.4% |

**Offset distribution [frequency]** (top-2 coverage: 24%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 3 | 14.3% |
| +116 | 2 | 9.5% |
| -116 | 2 | 9.5% |
| +112 | 2 | 9.5% |
| +115 | 2 | 9.5% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=43%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 42.9% |
| ss1 | ss2 | 8 | 38.1% |
| ss1 | flkR | 2 | 9.5% |
| ss1 | ss1 | 2 | 9.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 132 | ss2 | 16 | ss1 | +0.0122 | 0.5290 |
| 129 | ss2 | 16 | ss1 | +0.0083 | 0.3160 |
| 14 | ss1 | 130 | ss2 | +0.0070 | 0.0980 |
| 127 | ss2 | 15 | ss1 | +0.0062 | 0.4303 |
| 129 | ss2 | 17 | ss1 | +0.0049 | 0.0845 |

### L29 H18 — Rank #17

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→flkR  |  cells: 37  |  total attr: +0.1005

**Key mass** (top-1=12%, top-2=23%, top-3=33%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 181 | flkR | +0.0123 | 12.3% |
| 20 | ss1 | +0.0111 | 11.0% |
| 187 | flkR | +0.0101 | 10.1% |
| 128 | ss2 | +0.0078 | 7.7% |
| 135 | ss2 | +0.0071 | 7.0% |

**Query mass** (top-1=16%, top-2=30%, top-3=41%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 16 | ss1 | +0.0161 | 16.1% |
| 135 | ss2 | +0.0141 | 14.0% |
| 21 | ss1 | +0.0114 | 11.4% |
| 20 | ss1 | +0.0108 | 10.7% |
| 15 | ss1 | +0.0106 | 10.6% |

**Offset distribution [frequency]** (top-2 coverage: 14%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -166 | 3 | 8.1% |
| -165 | 2 | 5.4% |
| -112 | 2 | 5.4% |
| +116 | 2 | 5.4% |
| -121 | 2 | 5.4% |

**Region-pair profile** (q→k)  [CROSS:ss1→flkR]  (top=59%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | flkR | 22 | 59.5% |
| ss1 | ss2 | 6 | 16.2% |
| ss2 | ss1 | 4 | 10.8% |
| flkL | ss2 | 2 | 5.4% |
| ss1 | other | 2 | 5.4% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 135 | ss2 | 20 | ss1 | +0.0111 | 0.4540 |
| 16 | ss1 | 181 | flkR | +0.0107 | 0.2219 |
| 20 | ss1 | 135 | ss2 | +0.0071 | 0.2201 |
| 15 | ss1 | 127 | ss2 | +0.0052 | 0.3012 |
| 21 | ss1 | 187 | flkR | +0.0039 | 0.0618 |

### L30 H1 — Rank #16

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED | CROSS_SSE | CROSS:ss1→ss2  |  cells: 7  |  total attr: +0.0416

**Key mass** (top-1=54%, top-2=94%, top-3=97%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 128 | ss2 | +0.0223 | 53.6% |
| 135 | ss2 | +0.0168 | 40.5% |
| 130 | ss2 | +0.0013 | 3.2% |
| 129 | ss2 | +0.0011 | 2.7% |

**Query mass** (top-1=32%, top-2=63%, top-3=78%)  [DISTR(D20/L14/I12)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 20 | ss1 | +0.0135 | 32.5% |
| 14 | ss1 | +0.0127 | 30.5% |
| 12 | ss1 | +0.0061 | 14.6% |
| 13 | ss1 | +0.0036 | 8.6% |
| 19 | ss1 | +0.0033 | 8.0% |

**Offset distribution [frequency]** (top-2 coverage: 57%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 2 | 28.6% |
| -114 | 2 | 28.6% |
| -116 | 2 | 28.6% |
| -112 | 1 | 14.3% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=100%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 7 | 100.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 20 | ss1 | 135 | ss2 | +0.0135 | 0.1514 |
| 14 | ss1 | 128 | ss2 | +0.0127 | 0.7899 |
| 12 | ss1 | 128 | ss2 | +0.0061 | 0.6426 |
| 13 | ss1 | 128 | ss2 | +0.0036 | 0.2834 |
| 19 | ss1 | 135 | ss2 | +0.0033 | 0.0953 |

### L32 H13 — Rank #27

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.0274

**Key mass** (top-1=42%, top-2=59%, top-3=67%)  [DISTR(V129/G135/V130/F17)]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 129 | ss2 | +0.0114 | 41.5% |
| 135 | ss2 | +0.0048 | 17.5% |
| 130 | ss2 | +0.0023 | 8.5% |
| 17 | ss1 | +0.0018 | 6.5% |
| 131 | ss2 | +0.0015 | 5.5% |

**Query mass** (top-1=28%, top-2=42%, top-3=54%)  [DISTR(F17/V15/G19/V129/D20)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 17 | ss1 | +0.0076 | 27.5% |
| 15 | ss1 | +0.0038 | 14.0% |
| 19 | ss1 | +0.0035 | 12.6% |
| 129 | ss2 | +0.0031 | 11.4% |
| 20 | ss1 | +0.0028 | 10.3% |

**Offset distribution [frequency]** (top-2 coverage: 45%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -115 | 3 | 27.3% |
| -112 | 2 | 18.2% |
| -116 | 2 | 18.2% |
| -114 | 1 | 9.1% |
| +112 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 72.7% |
| ss2 | ss1 | 3 | 27.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 17 | ss1 | 129 | ss2 | +0.0076 | 0.0928 |
| 15 | ss1 | 129 | ss2 | +0.0038 | 0.0688 |
| 20 | ss1 | 135 | ss2 | +0.0028 | 0.0235 |
| 14 | ss1 | 130 | ss2 | +0.0023 | 0.0321 |
| 19 | ss1 | 135 | ss2 | +0.0020 | 0.0407 |

### L32 H18 — Rank #7

**Tags:** k:MULTI-ANCHOR / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 11  |  total attr: +0.0542

**Key mass** (top-1=35%, top-2=69%, top-3=83%)  [MULTI-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 131 | ss2 | +0.0190 | 35.1% |
| 129 | ss2 | +0.0185 | 34.0% |
| 127 | ss2 | +0.0074 | 13.6% |
| 132 | ss2 | +0.0041 | 7.6% |
| 14 | ss1 | +0.0026 | 4.7% |

**Query mass** (top-1=35%, top-2=58%, top-3=76%)  [DISTR(G19/V15/G16)]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 19 | ss1 | +0.0190 | 35.1% |
| 15 | ss1 | +0.0125 | 23.1% |
| 16 | ss1 | +0.0095 | 17.5% |
| 17 | ss1 | +0.0029 | 5.3% |
| 127 | ss2 | +0.0027 | 4.9% |

**Offset distribution [frequency]** (top-2 coverage: 45%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -112 | 3 | 27.3% |
| -115 | 2 | 18.2% |
| -114 | 1 | 9.1% |
| -113 | 1 | 9.1% |
| -116 | 1 | 9.1% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=73%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 8 | 72.7% |
| ss2 | ss1 | 3 | 27.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 19 | ss1 | 131 | ss2 | +0.0190 | 0.1934 |
| 15 | ss1 | 129 | ss2 | +0.0077 | 0.0841 |
| 16 | ss1 | 129 | ss2 | +0.0054 | 0.1258 |
| 15 | ss1 | 127 | ss2 | +0.0048 | 0.1150 |
| 16 | ss1 | 132 | ss2 | +0.0041 | 0.0852 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #1 | L0 | H11 | 34 | +0.3855 | DISTRIBUTED |  | SINGLE-ANCHOR | E193 |  | INTRA:flkR |
| #10 | L5 | H2 | 13 | +0.1639 | SINGLE-ANCHOR | S190 | SINGLE-ANCHOR | M183 |  | INTRA:flkR |
| #21 | L6 | H8 | 6 | +0.0844 | SINGLE-ANCHOR | V192 | SINGLE-ANCHOR | M183 |  | INTRA:flkR |
| #25 | L6 | H17 | 36 | +0.1129 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #2 | L8 | H12 | 19 | +0.3682 | SINGLE-ANCHOR | M183 | SINGLE-ANCHOR | G16 |  |  |
| #11 | L9 | H8 | 16 | +0.0478 | DISTRIBUTED | E193/M183/?-1/V182/D126 | DUAL-ANCHOR | M183/G16 |  | INTRA:flkR |
| #8 | L10 | H0 | 16 | +0.1482 | SINGLE-ANCHOR | G16 | DISTRIBUTED | D21/D20/T22/G16/L14 |  | INTRA:ss1 |
| #5 | L10 | H2 | 8 | +0.3111 | SINGLE-ANCHOR | M183 | SINGLE-ANCHOR | G16 |  | CROSS:ss1→flkR |
| #15 | L10 | H9 | 14 | +0.1662 | SINGLE-ANCHOR | L131 | SINGLE-ANCHOR | G16 |  |  |
| #24 | L11 | H9 | 7 | +0.0662 | SINGLE-ANCHOR | G16 | SINGLE-ANCHOR | G16 |  | INTRA:ss1 |
| #9 | L12 | H3 | 12 | +0.1263 | SINGLE-ANCHOR | L131 | SINGLE-ANCHOR | G16 |  | CROSS:ss1→ss2 |
| #14 | L12 | H9 | 14 | +0.1125 | MULTI-ANCHOR |  | SINGLE-ANCHOR | G16 |  | INTRA:ss1 |
| #23 | L12 | H15 | 20 | +0.0871 | DUAL-ANCHOR | L131/G16 | DISTRIBUTED | G16/G0/I12/?-1/D21 |  | CROSS:ss1→ss2 |
| #26 | L12 | H16 | 5 | +0.0616 | SINGLE-ANCHOR | M183 | SINGLE-ANCHOR | G16 |  |  |
| #3 | L13 | H2 | 28 | +0.2289 | SINGLE-ANCHOR | G16 | DISTRIBUTED | G16/I12/L14 |  | INTRA:ss1 |
| #13 | L14 | H9 | 17 | +0.1098 | DUAL-ANCHOR | M183/L131 | DISTRIBUTED | G16/?-1/D21 |  | CROSS:ss1→ss2 |
| #6 | L14 | H16 | 31 | +0.2370 | SINGLE-ANCHOR | ?-1 | DISTRIBUTED |  |  |  |
| #20 | L17 | H4 | 14 | +0.1237 | SINGLE-ANCHOR | D18 | MULTI-ANCHOR |  |  | INTRA:ss1 |
| #22 | L17 | H18 | 14 | +0.0529 | SINGLE-ANCHOR | M183 | DISTRIBUTED | V15/I12/V129/F17/G16 |  | CROSS:ss1→flkR |
| #18 | L18 | H8 | 18 | +0.0922 | DISTRIBUTED | G16/D18/D20 | SINGLE-ANCHOR | I12 |  | INTRA:ss1 |
| #29 | L18 | H12 | 16 | +0.0848 | DISTRIBUTED | D21/I12/L14 | SINGLE-ANCHOR | V15 |  | INTRA:ss1 |
| #19 | L18 | H16 | 16 | +0.0996 | SINGLE-ANCHOR | M183 | DUAL-ANCHOR | V15/I12 |  | CROSS:ss1→flkR |
| #12 | L22 | H14 | 13 | +0.0672 | DISTRIBUTED | M183/L14/G16 | DISTRIBUTED | V15/V130/V129/I132 |  |  |
| #30 | L26 | H6 | 5 | +0.0755 | DUAL-ANCHOR | L14/V15 | SINGLE-ANCHOR | I12 |  | INTRA:ss1 |
| #28 | L26 | H16 | 19 | +0.0587 | DISTRIBUTED | V129/Y127/G135/A128 | DISTRIBUTED | V15/L14/I12/F17/G16 |  | CROSS:ss1→ss2 |
| #4 | L27 | H15 | 21 | +0.0737 | DISTRIBUTED | G16/V130/V15/F17/V129 | DISTRIBUTED | V129/I132/L14/F17/Y127 |  | CROSS:ss2→ss1 |
| #17 | L29 | H18 | 37 | +0.1005 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→flkR |
| #16 | L30 | H1 | 7 | +0.0416 | DUAL-ANCHOR | A128/G135 | DISTRIBUTED | D20/L14/I12 | CROSS_SSE | CROSS:ss1→ss2 |
| #27 | L32 | H13 | 11 | +0.0274 | DISTRIBUTED | V129/G135/V130/F17 | DISTRIBUTED | F17/V15/G19/V129/D20 |  | CROSS:ss1→ss2 |
| #7 | L32 | H18 | 11 | +0.0542 | MULTI-ANCHOR |  | DISTRIBUTED | G19/V15/G16 |  | CROSS:ss1→ss2 |
