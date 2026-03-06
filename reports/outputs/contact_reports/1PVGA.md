# Contact Pattern Analysis: 1PVGA

Generated: 2026-02-24 18:47:49   Model: facebook/esm2_t33_650M_UR50D

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
| 272 | flkR | +0.0041 | 39.2% |
| 33 | flkL | +0.0040 | 38.0% |
| 32 | flkL | +0.0016 | 15.7% |
| 273 | other | +0.0007 | 7.1% |

**Query mass** (top-1=18%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 268 | flkR | +0.0018 | 17.6% |
| 53 | flkL | +0.0015 | 14.5% |
| 76 | flkL | +0.0013 | 12.1% |
| 240 | flkR | +0.0012 | 11.4% |
| 74 | flkL | +0.0012 | 11.4% |

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
| flkR | flkR | 3 | 30.0% |
| flkL | flkR | 1 | 10.0% |
| flkR | other | 1 | 10.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 53 | flkL | 33 | flkL | +0.0015 | 0.0098 |
| 76 | flkL | 33 | flkL | +0.0013 | 0.0036 |
| 240 | flkR | 272 | flkR | +0.0012 | 0.0067 |
| 74 | flkL | 33 | flkL | +0.0012 | 0.0038 |
| 268 | flkR | 272 | flkR | +0.0011 | 0.0163 |

### L3 H7 — Rank #22

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR | INTRA:flkL  |  cells: 12  |  total attr: +0.0394

**Key mass** (top-1=33%, top-2=55%, top-3=70%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 33 | flkL | +0.0130 | 32.9% |
| 32 | flkL | +0.0085 | 21.7% |
| 271 | flkR | +0.0060 | 15.2% |
| 34 | flkL | +0.0032 | 8.0% |
| 270 | flkR | +0.0028 | 7.1% |

**Query mass** (top-1=48%, top-2=70%, top-3=79%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 32 | flkL | +0.0188 | 47.7% |
| 270 | flkR | +0.0088 | 22.3% |
| 31 | flkL | +0.0036 | 9.1% |
| 33 | flkL | +0.0032 | 8.0% |
| 272 | flkR | +0.0012 | 3.0% |

**Offset distribution [frequency]** (top-2 coverage: 100%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -1 | 7 | 58.3% |
| +0 | 5 | 41.7% |

**Region-pair profile** (q→k)  [INTRA:flkL]  (top=58%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkL | flkL | 7 | 58.3% |
| flkR | flkR | 2 | 16.7% |
| flkR | other | 1 | 8.3% |
| ss1 | ss1 | 1 | 8.3% |
| ss2 | ss2 | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 32 | flkL | 33 | flkL | +0.0130 | 0.3132 |
| 270 | flkR | 271 | flkR | +0.0060 | 0.1233 |
| 32 | flkL | 32 | flkL | +0.0058 | 0.1221 |
| 33 | flkL | 34 | flkL | +0.0032 | 0.0808 |
| 270 | flkR | 270 | flkR | +0.0028 | 0.0712 |

### L4 H14 — Rank #27

**Tags:** k:DUAL-ANCHOR / q:DUAL-ANCHOR | CROSS:ss1→flkR  |  cells: 2  |  total attr: +0.0046

**Key mass** (top-1=56%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 271 | flkR | +0.0026 | 56.5% |
| 272 | flkR | +0.0020 | 43.5% |

**Query mass** (top-1=56%, top-2=100%, top-3=100%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0026 | 56.5% |
| 72 | flkL | +0.0020 | 43.5% |

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
| 102 | ss1 | 271 | flkR | +0.0026 | 0.0034 |
| 72 | flkL | 272 | flkR | +0.0020 | 0.0101 |

### L5 H9 — Rank #10

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | INTRA:flkR  |  cells: 8  |  total attr: +0.0910

**Key mass** (top-1=91%, top-2=97%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 98 | ss1 | +0.0831 | 91.3% |
| 233 | flkR | +0.0052 | 5.7% |
| 30 | other | +0.0015 | 1.7% |
| 102 | ss1 | +0.0012 | 1.3% |

**Query mass** (top-1=89%, top-2=93%, top-3=95%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0806 | 88.6% |
| 104 | ss1 | +0.0037 | 4.0% |
| 223 | flkR | +0.0021 | 2.3% |
| 34 | flkL | +0.0015 | 1.7% |
| 242 | flkR | +0.0013 | 1.4% |

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
| 102 | ss1 | 98 | ss1 | +0.0794 | 0.0633 |
| 104 | ss1 | 98 | ss1 | +0.0037 | 0.0474 |
| 223 | flkR | 233 | flkR | +0.0021 | 0.0239 |
| 34 | flkL | 30 | other | +0.0015 | 0.1331 |
| 242 | flkR | 233 | flkR | +0.0013 | 0.0458 |

### L6 H0 — Rank #15

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR | ss1→flkL  |  cells: 12  |  total attr: +0.0217

**Key mass** (top-1=31%, top-2=49%, top-3=60%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 33 | flkL | +0.0068 | 31.3% |
| 45 | flkL | +0.0038 | 17.7% |
| 44 | flkL | +0.0024 | 11.0% |
| 31 | flkL | +0.0019 | 8.7% |
| 56 | flkL | +0.0013 | 5.8% |

**Query mass** (top-1=87%, top-2=92%, top-3=96%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0189 | 87.4% |
| 93 | flkL | +0.0010 | 4.7% |
| 89 | flkL | +0.0009 | 4.0% |
| 218 | flkR | +0.0008 | 3.8% |

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
| flkL | flkL | 2 | 16.7% |
| flkR | flkL | 1 | 8.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 102 | ss1 | 33 | flkL | +0.0068 | 0.0362 |
| 102 | ss1 | 45 | flkL | +0.0038 | 0.0201 |
| 102 | ss1 | 44 | flkL | +0.0024 | 0.0056 |
| 102 | ss1 | 56 | flkL | +0.0013 | 0.0025 |
| 102 | ss1 | 52 | flkL | +0.0011 | 0.0029 |

### L7 H7 — Rank #9

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 24  |  total attr: +0.0804

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0804 | 100.0% |

**Query mass** (top-1=15%, top-2=25%, top-3=34%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0117 | 14.5% |
| 138 | other | +0.0085 | 10.6% |
| 139 | other | +0.0074 | 9.2% |
| 137 | other | +0.0058 | 7.2% |
| 140 | other | +0.0051 | 6.4% |

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
| 102 | ss1 | 102 | ss1 | +0.0117 | 0.1317 |
| 138 | other | 102 | ss1 | +0.0085 | 0.0796 |
| 139 | other | 102 | ss1 | +0.0074 | 0.0771 |
| 137 | other | 102 | ss1 | +0.0058 | 0.0738 |
| 140 | other | 102 | ss1 | +0.0051 | 0.0696 |

### L7 H13 — Rank #12

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 72  |  total attr: +0.1803

**Key mass** (top-1=19%, top-2=31%, top-3=39%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 271 | flkR | +0.0338 | 18.7% |
| 218 | flkR | +0.0227 | 12.6% |
| 270 | flkR | +0.0141 | 7.8% |
| 273 | other | +0.0072 | 4.0% |
| 232 | flkR | +0.0070 | 3.9% |

**Query mass** (top-1=16%, top-2=29%, top-3=36%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 218 | flkR | +0.0295 | 16.3% |
| 271 | flkR | +0.0227 | 12.6% |
| 230 | flkR | +0.0135 | 7.5% |
| 217 | flkR | +0.0133 | 7.4% |
| 213 | flkR | +0.0093 | 5.1% |

**Offset distribution [frequency]** (top-2 coverage: 29%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 17 | 23.6% |
| -53 | 4 | 5.6% |
| -40 | 4 | 5.6% |
| -39 | 2 | 2.8% |
| -60 | 2 | 2.8% |

**Region-pair profile** (q→k)  (top=38%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | flkR | 27 | 37.5% |
| flkL | flkL | 20 | 27.8% |
| flkR | flkL | 6 | 8.3% |
| flkR | other | 4 | 5.6% |
| ss1 | flkL | 3 | 4.2% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 218 | flkR | 271 | flkR | +0.0295 | 0.2306 |
| 271 | flkR | 218 | flkR | +0.0227 | 0.4179 |
| 217 | flkR | 270 | flkR | +0.0133 | 0.0954 |
| 232 | flkR | 232 | flkR | +0.0070 | 0.0916 |
| 213 | flkR | 213 | flkR | +0.0068 | 0.0662 |

### L7 H18 — Rank #21

**Tags:** k:DUAL-ANCHOR / q:DISTRIBUTED  |  cells: 23  |  total attr: +0.0303

**Key mass** (top-1=59%, top-2=86%, top-3=93%)  [DUAL-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 273 | other | +0.0178 | 58.8% |
| 270 | flkR | +0.0084 | 27.6% |
| 38 | flkL | +0.0021 | 6.8% |
| 96 | ss1 | +0.0013 | 4.4% |
| 267 | flkR | +0.0008 | 2.5% |

**Query mass** (top-1=17%, top-2=31%, top-3=38%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 265 | flkR | +0.0051 | 16.8% |
| 102 | ss1 | +0.0041 | 13.7% |
| 189 | other | +0.0023 | 7.7% |
| 248 | flkR | +0.0018 | 5.8% |
| 219 | flkR | +0.0017 | 5.5% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -8 | 1 | 4.3% |
| +64 | 1 | 4.3% |
| -25 | 1 | 4.3% |
| -54 | 1 | 4.3% |
| -5 | 1 | 4.3% |

**Region-pair profile** (q→k)  (top=35%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| flkR | other | 8 | 34.8% |
| other | flkR | 5 | 21.7% |
| ss2 | other | 4 | 17.4% |
| flkR | flkR | 2 | 8.7% |
| ss1 | flkL | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 265 | flkR | 273 | other | +0.0035 | 0.1015 |
| 102 | ss1 | 38 | flkL | +0.0021 | 0.0062 |
| 248 | flkR | 273 | other | +0.0018 | 0.0962 |
| 219 | flkR | 273 | other | +0.0017 | 0.0454 |
| 265 | flkR | 270 | flkR | +0.0016 | 0.0318 |

### L8 H2 — Rank #26

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 10  |  total attr: +0.0679

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0679 | 100.0% |

**Query mass** (top-1=17%, top-2=32%, top-3=44%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 138 | other | +0.0113 | 16.7% |
| 139 | other | +0.0103 | 15.1% |
| 140 | other | +0.0083 | 12.2% |
| 137 | other | +0.0083 | 12.2% |
| 141 | other | +0.0074 | 10.9% |

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
| 138 | other | 102 | ss1 | +0.0113 | 0.0454 |
| 139 | other | 102 | ss1 | +0.0103 | 0.0532 |
| 140 | other | 102 | ss1 | +0.0083 | 0.0697 |
| 137 | other | 102 | ss1 | +0.0083 | 0.0502 |
| 141 | other | 102 | ss1 | +0.0074 | 0.0916 |

### L9 H17 — Rank #2

**Tags:** k:DISTRIBUTED / q:SINGLE-ANCHOR  |  cells: 44  |  total attr: +0.1388

**Key mass** (top-1=11%, top-2=21%, top-3=29%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 142 | other | +0.0149 | 10.8% |
| 141 | other | +0.0141 | 10.1% |
| 143 | other | +0.0106 | 7.7% |
| 140 | other | +0.0099 | 7.2% |
| 139 | other | +0.0092 | 6.6% |

**Query mass** (top-1=70%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0975 | 70.2% |
| 102 | ss1 | +0.0329 | 23.7% |
| 104 | ss1 | +0.0060 | 4.3% |
| 106 | ss1 | +0.0025 | 1.8% |

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
| 202 | ss2 | 142 | other | +0.0111 | 0.0277 |
| 202 | ss2 | 141 | other | +0.0105 | 0.0257 |
| 202 | ss2 | 139 | other | +0.0092 | 0.0204 |
| 202 | ss2 | 140 | other | +0.0092 | 0.0213 |
| 202 | ss2 | 143 | other | +0.0086 | 0.0210 |

### L10 H9 — Rank #1

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 100  |  total attr: +0.2674

**Key mass** (top-1=100%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.2664 | 99.6% |
| 227 | flkR | +0.0010 | 0.4% |

**Query mass** (top-1=11%, top-2=18%, top-3=23%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0298 | 11.2% |
| 102 | ss1 | +0.0179 | 6.7% |
| 203 | ss2 | +0.0136 | 5.1% |
| 101 | ss1 | +0.0102 | 3.8% |
| 213 | flkR | +0.0092 | 3.4% |

**Offset distribution [frequency]** (top-2 coverage: 2%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +100 | 1 | 1.0% |
| +0 | 1 | 1.0% |
| +101 | 1 | 1.0% |
| -1 | 1 | 1.0% |
| +111 | 1 | 1.0% |

**Region-pair profile** (q→k)  (top=51%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 51 | 51.0% |
| flkR | ss1 | 25 | 25.0% |
| flkL | ss1 | 9 | 9.0% |
| ss2 | ss1 | 7 | 7.0% |
| ss1 | ss1 | 7 | 7.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 202 | ss2 | 102 | ss1 | +0.0298 | 0.2060 |
| 102 | ss1 | 102 | ss1 | +0.0179 | 0.0590 |
| 203 | ss2 | 102 | ss1 | +0.0136 | 0.2546 |
| 101 | ss1 | 102 | ss1 | +0.0102 | 0.2569 |
| 213 | flkR | 102 | ss1 | +0.0092 | 0.2474 |

### L11 H8 — Rank #28

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | CROSS:flkR→ss1  |  cells: 26  |  total attr: +0.0405

**Key mass** (top-1=93%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0379 | 93.5% |
| 419 | other | +0.0026 | 6.5% |

**Query mass** (top-1=9%, top-2=18%, top-3=27%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 240 | flkR | +0.0038 | 9.4% |
| 224 | flkR | +0.0036 | 9.0% |
| 419 | other | +0.0034 | 8.4% |
| 223 | flkR | +0.0028 | 6.9% |
| 233 | flkR | +0.0027 | 6.6% |

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
| 240 | flkR | 102 | ss1 | +0.0038 | 0.1277 |
| 224 | flkR | 102 | ss1 | +0.0036 | 0.1630 |
| 419 | other | 102 | ss1 | +0.0034 | 0.0633 |
| 223 | flkR | 102 | ss1 | +0.0028 | 0.2006 |
| 233 | flkR | 102 | ss1 | +0.0027 | 0.3510 |

### L11 H14 — Rank #14

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 44  |  total attr: +0.0797

**Key mass** (top-1=92%, top-2=96%, top-3=99%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0734 | 92.1% |
| 229 | flkR | +0.0031 | 3.9% |
| 419 | other | +0.0022 | 2.8% |
| 72 | flkL | +0.0010 | 1.2% |

**Query mass** (top-1=8%, top-2=13%, top-3=17%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0063 | 7.9% |
| 202 | ss2 | +0.0038 | 4.8% |
| 150 | other | +0.0032 | 4.0% |
| 151 | other | +0.0031 | 3.9% |
| 143 | other | +0.0031 | 3.8% |

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
| 204 | ss2 | 102 | ss1 | +0.0041 | 0.0277 |
| 150 | other | 102 | ss1 | +0.0032 | 0.1283 |
| 151 | other | 102 | ss1 | +0.0031 | 0.1225 |
| 143 | other | 102 | ss1 | +0.0031 | 0.1018 |
| 202 | ss2 | 102 | ss1 | +0.0029 | 0.0489 |

### L11 H16 — Rank #8

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED  |  cells: 33  |  total attr: +0.0491

**Key mass** (top-1=85%, top-2=89%, top-3=93%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0418 | 85.1% |
| 419 | other | +0.0019 | 3.9% |
| 46 | flkL | +0.0018 | 3.8% |
| 54 | flkL | +0.0018 | 3.7% |
| 240 | flkR | +0.0010 | 2.1% |

**Query mass** (top-1=15%, top-2=23%, top-3=30%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 31 | flkL | +0.0072 | 14.7% |
| 206 | ss2 | +0.0042 | 8.6% |
| 114 | other | +0.0036 | 7.3% |
| 33 | flkL | +0.0027 | 5.6% |
| 117 | other | +0.0026 | 5.2% |

**Offset distribution [frequency]** (top-2 coverage: 9%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +0 | 2 | 6.1% |
| -71 | 1 | 3.0% |
| +104 | 1 | 3.0% |
| +12 | 1 | 3.0% |
| -69 | 1 | 3.0% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| other | ss1 | 12 | 36.4% |
| ss2 | ss1 | 4 | 12.1% |
| flkL | ss1 | 3 | 9.1% |
| flkR | ss1 | 3 | 9.1% |
| ss1 | ss1 | 3 | 9.1% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 31 | flkL | 102 | ss1 | +0.0047 | 0.2293 |
| 206 | ss2 | 102 | ss1 | +0.0042 | 0.1442 |
| 114 | other | 102 | ss1 | +0.0036 | 0.2113 |
| 33 | flkL | 102 | ss1 | +0.0027 | 0.2549 |
| 117 | other | 102 | ss1 | +0.0026 | 0.2226 |

### L12 H10 — Rank #11

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 25  |  total attr: +0.0481

**Key mass** (top-1=35%, top-2=42%, top-3=48%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0169 | 35.0% |
| 72 | flkL | +0.0036 | 7.4% |
| 150 | other | +0.0028 | 5.8% |
| 151 | other | +0.0027 | 5.7% |
| 191 | other | +0.0020 | 4.1% |

**Query mass** (top-1=60%, top-2=84%, top-3=95%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0288 | 59.9% |
| 117 | other | +0.0115 | 23.8% |
| 114 | other | +0.0054 | 11.2% |
| 102 | ss1 | +0.0017 | 3.5% |
| 204 | ss2 | +0.0008 | 1.6% |

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
| 117 | other | 102 | ss1 | +0.0115 | 0.2085 |
| 114 | other | 102 | ss1 | +0.0054 | 0.2593 |
| 202 | ss2 | 150 | other | +0.0028 | 0.0230 |
| 202 | ss2 | 151 | other | +0.0027 | 0.0245 |
| 202 | ss2 | 191 | other | +0.0020 | 0.0562 |

### L13 H2 — Rank #18

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 16  |  total attr: +0.0417

**Key mass** (top-1=66%, top-2=79%, top-3=89%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0276 | 66.0% |
| 204 | ss2 | +0.0053 | 12.8% |
| 102 | ss1 | +0.0042 | 10.1% |
| 241 | flkR | +0.0019 | 4.5% |
| 199 | ss2 | +0.0012 | 2.9% |

**Query mass** (top-1=25%, top-2=44%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0102 | 24.5% |
| 202 | ss2 | +0.0082 | 19.7% |
| 201 | ss2 | +0.0054 | 12.9% |
| 199 | ss2 | +0.0051 | 12.1% |
| 198 | ss2 | +0.0038 | 9.1% |

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
| 200 | ss2 | 202 | ss2 | +0.0090 | 0.3382 |
| 199 | ss2 | 202 | ss2 | +0.0051 | 0.2648 |
| 201 | ss2 | 202 | ss2 | +0.0044 | 0.3212 |
| 202 | ss2 | 202 | ss2 | +0.0035 | 0.1186 |
| 202 | ss2 | 204 | ss2 | +0.0031 | 0.0655 |

### L14 H4 — Rank #20

**Tags:** k:SINGLE-ANCHOR / q:DUAL-ANCHOR | CROSS:ss2→ss1  |  cells: 11  |  total attr: +0.0750

**Key mass** (top-1=95%, top-2=99%, top-3=100%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0710 | 94.7% |
| 100 | ss1 | +0.0032 | 4.3% |
| 0 | other | +0.0007 | 1.0% |

**Query mass** (top-1=39%, top-2=71%, top-3=79%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0289 | 38.5% |
| 202 | ss2 | +0.0242 | 32.3% |
| 244 | flkR | +0.0063 | 8.4% |
| 207 | ss2 | +0.0053 | 7.0% |
| 203 | ss2 | +0.0037 | 5.0% |

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
| 204 | ss2 | 102 | ss1 | +0.0270 | 0.2130 |
| 202 | ss2 | 102 | ss1 | +0.0229 | 0.2510 |
| 244 | flkR | 102 | ss1 | +0.0063 | 0.2822 |
| 207 | ss2 | 102 | ss1 | +0.0053 | 0.2458 |
| 203 | ss2 | 102 | ss1 | +0.0037 | 0.1911 |

### L14 H9 — Rank #23

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 15  |  total attr: +0.0223

**Key mass** (top-1=33%, top-2=49%, top-3=65%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0074 | 33.3% |
| 199 | ss2 | +0.0036 | 16.0% |
| 234 | flkR | +0.0035 | 15.9% |
| 216 | flkR | +0.0035 | 15.7% |
| 0 | other | +0.0015 | 6.5% |

**Query mass** (top-1=23%, top-2=39%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0051 | 22.8% |
| 224 | flkR | +0.0036 | 16.0% |
| 104 | ss1 | +0.0032 | 14.4% |
| 200 | ss2 | +0.0023 | 10.5% |
| 202 | ss2 | +0.0023 | 10.2% |

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
| 104 | ss1 | 102 | ss1 | +0.0032 | 0.0959 |
| 204 | ss2 | 102 | ss1 | +0.0032 | 0.0581 |
| 224 | flkR | 234 | flkR | +0.0020 | 0.0936 |
| 224 | flkR | 216 | flkR | +0.0016 | 0.1121 |
| 240 | flkR | 234 | flkR | +0.0016 | 0.0726 |

### L15 H8 — Rank #29

**Tags:** k:SINGLE-ANCHOR / q:SINGLE-ANCHOR | CROSS_SSE | CROSS:ss2→ss1  |  cells: 5  |  total attr: +0.0365

**Key mass** (top-1=91%, top-2=95%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0332 | 90.8% |
| 104 | ss1 | +0.0014 | 4.0% |
| 72 | flkL | +0.0011 | 3.1% |
| 202 | ss2 | +0.0007 | 2.0% |

**Query mass** (top-1=91%, top-2=100%, top-3=100%)  [SINGLE-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0331 | 90.7% |
| 202 | ss2 | +0.0034 | 9.3% |

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
| 204 | ss2 | 102 | ss1 | +0.0309 | 0.3124 |
| 202 | ss2 | 102 | ss1 | +0.0023 | 0.2464 |
| 204 | ss2 | 104 | ss1 | +0.0014 | 0.0257 |
| 202 | ss2 | 72 | flkL | +0.0011 | 0.0138 |
| 204 | ss2 | 202 | ss2 | +0.0007 | 0.0142 |

### L16 H7 — Rank #16

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 22  |  total attr: +0.0343

**Key mass** (top-1=47%, top-2=60%, top-3=70%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0160 | 46.6% |
| 199 | ss2 | +0.0045 | 13.1% |
| 204 | ss2 | +0.0036 | 10.4% |
| 202 | ss2 | +0.0036 | 10.4% |
| 211 | flkR | +0.0020 | 6.0% |

**Query mass** (top-1=26%, top-2=46%, top-3=54%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0088 | 25.5% |
| 117 | other | +0.0071 | 20.6% |
| 200 | ss2 | +0.0027 | 8.0% |
| 204 | ss2 | +0.0026 | 7.5% |
| 118 | other | +0.0025 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 18%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 2 | 9.1% |
| +3 | 2 | 9.1% |
| +15 | 1 | 4.5% |
| +100 | 1 | 4.5% |
| +16 | 1 | 4.5% |

**Region-pair profile** (q→k)  (top=36%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 8 | 36.4% |
| other | ss1 | 4 | 18.2% |
| ss2 | other | 3 | 13.6% |
| flkR | ss2 | 2 | 9.1% |
| ss2 | ss1 | 1 | 4.5% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 117 | other | 102 | ss1 | +0.0071 | 0.3745 |
| 202 | ss2 | 102 | ss1 | +0.0028 | 0.0541 |
| 118 | other | 102 | ss1 | +0.0025 | 0.4241 |
| 202 | ss2 | 211 | flkR | +0.0020 | 0.0298 |
| 202 | ss2 | 204 | ss2 | +0.0020 | 0.0631 |

### L16 H12 — Rank #24

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 23  |  total attr: +0.0468

**Key mass** (top-1=25%, top-2=41%, top-3=51%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0117 | 25.1% |
| 201 | ss2 | +0.0073 | 15.7% |
| 198 | ss2 | +0.0048 | 10.2% |
| 203 | ss2 | +0.0026 | 5.5% |
| 221 | flkR | +0.0025 | 5.3% |

**Query mass** (top-1=31%, top-2=46%, top-3=57%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0145 | 31.0% |
| 202 | ss2 | +0.0072 | 15.3% |
| 200 | ss2 | +0.0048 | 10.2% |
| 203 | ss2 | +0.0038 | 8.1% |
| 224 | flkR | +0.0025 | 5.3% |

**Offset distribution [frequency]** (top-2 coverage: 74%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +2 | 13 | 56.5% |
| +1 | 4 | 17.4% |
| +3 | 3 | 13.0% |
| -5 | 1 | 4.3% |
| +4 | 1 | 4.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=48%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 11 | 47.8% |
| other | other | 5 | 21.7% |
| flkR | flkR | 3 | 13.0% |
| flkL | flkL | 2 | 8.7% |
| ss1 | ss1 | 1 | 4.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 204 | ss2 | 202 | ss2 | +0.0117 | 0.2857 |
| 200 | ss2 | 198 | ss2 | +0.0048 | 0.4003 |
| 203 | ss2 | 201 | ss2 | +0.0038 | 0.2705 |
| 224 | flkR | 221 | flkR | +0.0025 | 0.2291 |
| 202 | ss2 | 201 | ss2 | +0.0024 | 0.0715 |

### L17 H7 — Rank #30

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED  |  cells: 29  |  total attr: +0.0288

**Key mass** (top-1=10%, top-2=18%, top-3=24%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 72 | flkL | +0.0028 | 9.7% |
| 189 | other | +0.0023 | 8.1% |
| 190 | other | +0.0017 | 5.8% |
| 89 | flkL | +0.0016 | 5.6% |
| 192 | other | +0.0014 | 4.9% |

**Query mass** (top-1=50%, top-2=69%, top-3=78%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0145 | 50.3% |
| 204 | ss2 | +0.0053 | 18.4% |
| 104 | ss1 | +0.0026 | 9.0% |
| 240 | flkR | +0.0017 | 6.0% |
| 91 | flkL | +0.0015 | 5.2% |

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
| 104 | ss1 | 89 | flkL | +0.0016 | 0.0774 |
| 91 | flkL | 72 | flkL | +0.0015 | 0.1580 |
| 204 | ss2 | 192 | other | +0.0014 | 0.0342 |
| 204 | ss2 | 189 | other | +0.0013 | 0.0229 |
| 93 | flkL | 72 | flkL | +0.0013 | 0.2319 |

### L17 H10 — Rank #7

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | INTRA:ss2  |  cells: 19  |  total attr: +0.1211

**Key mass** (top-1=79%, top-2=94%, top-3=98%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0958 | 79.1% |
| 204 | ss2 | +0.0185 | 15.2% |
| 102 | ss1 | +0.0048 | 4.0% |
| 205 | ss2 | +0.0010 | 0.9% |
| 115 | other | +0.0009 | 0.8% |

**Query mass** (top-1=38%, top-2=58%, top-3=68%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0457 | 37.8% |
| 203 | ss2 | +0.0244 | 20.1% |
| 207 | ss2 | +0.0119 | 9.8% |
| 206 | ss2 | +0.0104 | 8.6% |
| 199 | ss2 | +0.0080 | 6.6% |

**Offset distribution [frequency]** (top-2 coverage: 26%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| +1 | 3 | 15.8% |
| +2 | 2 | 10.5% |
| -1 | 2 | 10.5% |
| +0 | 2 | 10.5% |
| +5 | 1 | 5.3% |

**Region-pair profile** (q→k)  [INTRA:ss2]  (top=68%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss2 | 13 | 68.4% |
| flkR | ss2 | 2 | 10.5% |
| other | ss1 | 2 | 10.5% |
| ss1 | ss1 | 1 | 5.3% |
| other | other | 1 | 5.3% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 204 | ss2 | 202 | ss2 | +0.0447 | 0.6090 |
| 203 | ss2 | 202 | ss2 | +0.0205 | 0.6939 |
| 207 | ss2 | 202 | ss2 | +0.0108 | 0.6821 |
| 206 | ss2 | 204 | ss2 | +0.0104 | 0.5168 |
| 199 | ss2 | 202 | ss2 | +0.0080 | 0.7218 |

### L17 H18 — Rank #19

**Tags:** k:DISTRIBUTED / q:DUAL-ANCHOR  |  cells: 14  |  total attr: +0.0443

**Key mass** (top-1=56%, top-2=65%, top-3=71%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 102 | ss1 | +0.0249 | 56.1% |
| 231 | flkR | +0.0041 | 9.2% |
| 240 | flkR | +0.0023 | 5.2% |
| 204 | ss2 | +0.0022 | 5.0% |
| 202 | ss2 | +0.0022 | 4.9% |

**Query mass** (top-1=51%, top-2=78%, top-3=89%)  [DUAL-ANCHOR]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0226 | 50.9% |
| 204 | ss2 | +0.0122 | 27.5% |
| 200 | ss2 | +0.0048 | 10.9% |
| 258 | flkR | +0.0023 | 5.2% |
| 102 | ss1 | +0.0014 | 3.2% |

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
| 202 | ss2 | 102 | ss1 | +0.0186 | 0.2269 |
| 204 | ss2 | 102 | ss1 | +0.0063 | 0.0683 |
| 200 | ss2 | 231 | flkR | +0.0041 | 0.1359 |
| 258 | flkR | 240 | flkR | +0.0023 | 0.1157 |
| 204 | ss2 | 204 | ss2 | +0.0022 | 0.0306 |

### L19 H3 — Rank #25

**Tags:** k:SINGLE-ANCHOR / q:DISTRIBUTED | POSITIONAL | INTRA:ss2  |  cells: 13  |  total attr: +0.0471

**Key mass** (top-1=66%, top-2=80%, top-3=86%)  [SINGLE-ANCHOR]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 202 | ss2 | +0.0310 | 65.8% |
| 244 | flkR | +0.0065 | 13.8% |
| 76 | flkL | +0.0030 | 6.4% |
| 106 | ss1 | +0.0025 | 5.2% |
| 102 | ss1 | +0.0021 | 4.5% |

**Query mass** (top-1=30%, top-2=55%, top-3=68%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0142 | 30.2% |
| 199 | ss2 | +0.0115 | 24.4% |
| 240 | flkR | +0.0065 | 13.8% |
| 198 | ss2 | +0.0029 | 6.1% |
| 104 | ss1 | +0.0025 | 5.2% |

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
| 200 | ss2 | 202 | ss2 | +0.0130 | 0.4247 |
| 199 | ss2 | 202 | ss2 | +0.0115 | 0.4790 |
| 240 | flkR | 244 | flkR | +0.0065 | 0.3204 |
| 198 | ss2 | 202 | ss2 | +0.0029 | 0.3494 |
| 104 | ss1 | 106 | ss1 | +0.0025 | 0.0899 |

### L26 H16 — Rank #13

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 15  |  total attr: +0.0457

**Key mass** (top-1=39%, top-2=60%, top-3=68%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 104 | ss1 | +0.0177 | 38.6% |
| 98 | ss1 | +0.0098 | 21.5% |
| 101 | ss1 | +0.0036 | 7.8% |
| 92 | flkL | +0.0033 | 7.3% |
| 241 | flkR | +0.0032 | 7.1% |

**Query mass** (top-1=39%, top-2=52%, top-3=64%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 200 | ss2 | +0.0177 | 38.6% |
| 203 | ss2 | +0.0063 | 13.8% |
| 206 | ss2 | +0.0053 | 11.5% |
| 201 | ss2 | +0.0045 | 9.7% |
| 103 | ss1 | +0.0033 | 7.3% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -38 | 2 | 13.3% |
| +96 | 1 | 6.7% |
| +108 | 1 | 6.7% |
| +102 | 1 | 6.7% |
| +11 | 1 | 6.7% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=40%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 6 | 40.0% |
| ss2 | flkR | 4 | 26.7% |
| ss1 | flkL | 2 | 13.3% |
| flkL | ss1 | 2 | 13.3% |
| flkR | ss1 | 1 | 6.7% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 200 | ss2 | 104 | ss1 | +0.0177 | 0.1692 |
| 206 | ss2 | 98 | ss1 | +0.0053 | 0.5849 |
| 203 | ss2 | 101 | ss1 | +0.0036 | 0.0253 |
| 103 | ss1 | 92 | flkL | +0.0033 | 0.3462 |
| 208 | flkR | 98 | ss1 | +0.0027 | 0.1803 |

### L27 H15 — Rank #5

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 19  |  total attr: +0.0909

**Key mass** (top-1=21%, top-2=37%, top-3=50%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 103 | ss1 | +0.0188 | 20.7% |
| 100 | ss1 | +0.0144 | 15.9% |
| 99 | ss1 | +0.0121 | 13.3% |
| 98 | ss1 | +0.0109 | 12.0% |
| 101 | ss1 | +0.0080 | 8.8% |

**Query mass** (top-1=23%, top-2=45%, top-3=67%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 204 | ss2 | +0.0208 | 22.8% |
| 201 | ss2 | +0.0201 | 22.2% |
| 203 | ss2 | +0.0200 | 22.0% |
| 101 | ss1 | +0.0070 | 7.7% |
| 104 | ss1 | +0.0068 | 7.5% |

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
| 201 | ss2 | 103 | ss1 | +0.0173 | 0.2963 |
| 204 | ss2 | 100 | ss1 | +0.0144 | 0.1743 |
| 203 | ss2 | 99 | ss1 | +0.0121 | 0.2284 |
| 104 | ss1 | 200 | ss2 | +0.0068 | 0.0575 |
| 206 | ss2 | 98 | ss1 | +0.0058 | 0.3145 |

### L29 H18 — Rank #6

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 20  |  total attr: +0.1370

**Key mass** (top-1=28%, top-2=49%, top-3=66%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 101 | ss1 | +0.0384 | 28.0% |
| 200 | ss2 | +0.0287 | 21.0% |
| 201 | ss2 | +0.0239 | 17.4% |
| 104 | ss1 | +0.0126 | 9.2% |
| 203 | ss2 | +0.0083 | 6.0% |

**Query mass** (top-1=26%, top-2=47%, top-3=64%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0354 | 25.8% |
| 104 | ss1 | +0.0287 | 21.0% |
| 103 | ss1 | +0.0239 | 17.4% |
| 200 | ss2 | +0.0166 | 12.1% |
| 101 | ss1 | +0.0124 | 9.1% |

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
| 203 | ss2 | 101 | ss1 | +0.0343 | 0.4555 |
| 104 | ss1 | 200 | ss2 | +0.0287 | 0.4250 |
| 103 | ss1 | 201 | ss2 | +0.0239 | 0.5664 |
| 200 | ss2 | 104 | ss1 | +0.0126 | 0.2488 |
| 101 | ss1 | 203 | ss2 | +0.0083 | 0.1756 |

### L32 H13 — Rank #3

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss1→ss2  |  cells: 20  |  total attr: +0.0683

**Key mass** (top-1=15%, top-2=30%, top-3=43%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0101 | 14.8% |
| 203 | ss2 | +0.0101 | 14.8% |
| 101 | ss1 | +0.0091 | 13.4% |
| 103 | ss1 | +0.0085 | 12.4% |
| 200 | ss2 | +0.0078 | 11.5% |

**Query mass** (top-1=18%, top-2=34%, top-3=45%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 203 | ss2 | +0.0121 | 17.8% |
| 103 | ss1 | +0.0108 | 15.8% |
| 101 | ss1 | +0.0079 | 11.6% |
| 104 | ss1 | +0.0078 | 11.5% |
| 100 | ss1 | +0.0067 | 9.8% |

**Offset distribution [frequency]** (top-2 coverage: 20%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -96 | 2 | 10.0% |
| +96 | 2 | 10.0% |
| -104 | 2 | 10.0% |
| +104 | 2 | 10.0% |
| -98 | 2 | 10.0% |

**Region-pair profile** (q→k)  [CROSS:ss1→ss2]  (top=45%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss1 | ss2 | 9 | 45.0% |
| ss2 | ss1 | 9 | 45.0% |
| flkR | ss1 | 1 | 5.0% |
| ss1 | flkR | 1 | 5.0% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 103 | ss1 | 199 | ss2 | +0.0093 | 0.2656 |
| 203 | ss2 | 101 | ss1 | +0.0091 | 0.0553 |
| 104 | ss1 | 200 | ss2 | +0.0078 | 0.0585 |
| 101 | ss1 | 203 | ss2 | +0.0071 | 0.0428 |
| 199 | ss2 | 103 | ss1 | +0.0067 | 0.1901 |

### L32 H18 — Rank #4

**Tags:** k:DISTRIBUTED / q:DISTRIBUTED | CROSS:ss2→ss1  |  cells: 18  |  total attr: +0.0703

**Key mass** (top-1=20%, top-2=39%, top-3=57%)  [DISTRIBUTED]:

| k pos | region | attr | fraction |
|-------|--------|------|----------|
| 199 | ss2 | +0.0141 | 20.0% |
| 204 | ss2 | +0.0133 | 19.0% |
| 104 | ss1 | +0.0130 | 18.5% |
| 100 | ss1 | +0.0074 | 10.6% |
| 206 | ss2 | +0.0051 | 7.3% |

**Query mass** (top-1=26%, top-2=41%, top-3=53%)  [DISTRIBUTED]:

| q pos | region | attr | fraction |
|-------|--------|------|----------|
| 100 | ss1 | +0.0184 | 26.2% |
| 103 | ss1 | +0.0105 | 15.0% |
| 200 | ss2 | +0.0081 | 11.5% |
| 199 | ss2 | +0.0067 | 9.6% |
| 204 | ss2 | +0.0065 | 9.3% |

**Offset distribution [frequency]** (top-2 coverage: 22%):

| offset (q−k) | count | fraction |
|--------------|-------|----------|
| -96 | 2 | 11.1% |
| +96 | 2 | 11.1% |
| +104 | 2 | 11.1% |
| -98 | 2 | 11.1% |
| +106 | 2 | 11.1% |

**Region-pair profile** (q→k)  [CROSS:ss2→ss1]  (top=50%):

| q region | k region | count | fraction |
|----------|----------|-------|----------|
| ss2 | ss1 | 9 | 50.0% |
| ss1 | ss2 | 8 | 44.4% |
| ss1 | flkR | 1 | 5.6% |

**Top 5 cells:**

| q | q-region | k | k-region | attr | \|diff\| |
|---|----------|---|----------|------|--------|
| 100 | ss1 | 204 | ss2 | +0.0133 | 0.1263 |
| 103 | ss1 | 199 | ss2 | +0.0089 | 0.1553 |
| 200 | ss2 | 104 | ss1 | +0.0081 | 0.0369 |
| 204 | ss2 | 100 | ss1 | +0.0065 | 0.0618 |
| 100 | ss1 | 206 | ss2 | +0.0051 | 0.0968 |

## Summary Table

| rank | L | H | cells | total_attr | k_anchor | k_label | q_anchor | q_label | pos_type | region |
|------|---|---|-------|------------|----------|---------|----------|---------|----------|--------|
| #17 | L0 | H12 | 10 | +0.0105 | DUAL-ANCHOR | G272/Y33 | DISTRIBUTED |  |  | INTRA:flkL |
| #22 | L3 | H7 | 12 | +0.0394 | DISTRIBUTED |  | DUAL-ANCHOR | T32/D270 |  | INTRA:flkL |
| #27 | L4 | H14 | 2 | +0.0046 | DUAL-ANCHOR | N271/G272 | DUAL-ANCHOR | V102/I72 |  | CROSS:ss1→flkR |
| #10 | L5 | H9 | 8 | +0.0910 | SINGLE-ANCHOR | H98 | SINGLE-ANCHOR | V102 |  | INTRA:flkR |
| #15 | L6 | H0 | 12 | +0.0217 | DISTRIBUTED |  | SINGLE-ANCHOR | V102 |  | ss1→flkL |
| #9 | L7 | H7 | 24 | +0.0804 | SINGLE-ANCHOR | V102 | DISTRIBUTED |  |  |  |
| #12 | L7 | H13 | 72 | +0.1803 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #21 | L7 | H18 | 23 | +0.0303 | DUAL-ANCHOR | E273/D270 | DISTRIBUTED |  |  |  |
| #26 | L8 | H2 | 10 | +0.0679 | SINGLE-ANCHOR | V102 | DISTRIBUTED |  |  |  |
| #2 | L9 | H17 | 44 | +0.1388 | DISTRIBUTED |  | SINGLE-ANCHOR | V202 |  |  |
| #1 | L10 | H9 | 100 | +0.2674 | SINGLE-ANCHOR | V102 | DISTRIBUTED |  |  |  |
| #28 | L11 | H8 | 26 | +0.0405 | SINGLE-ANCHOR | V102 | DISTRIBUTED |  |  | CROSS:flkR→ss1 |
| #14 | L11 | H14 | 44 | +0.0797 | SINGLE-ANCHOR | V102 | DISTRIBUTED |  |  |  |
| #8 | L11 | H16 | 33 | +0.0491 | SINGLE-ANCHOR | V102 | DISTRIBUTED |  |  |  |
| #11 | L12 | H10 | 25 | +0.0481 | DISTRIBUTED |  | DUAL-ANCHOR | V202/E117 |  |  |
| #18 | L13 | H2 | 16 | +0.0417 | SINGLE-ANCHOR | V202 | DISTRIBUTED |  |  | INTRA:ss2 |
| #20 | L14 | H4 | 11 | +0.0750 | SINGLE-ANCHOR | V102 | DUAL-ANCHOR | F204/V202 |  | CROSS:ss2→ss1 |
| #23 | L14 | H9 | 15 | +0.0223 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #29 | L15 | H8 | 5 | +0.0365 | SINGLE-ANCHOR | V102 | SINGLE-ANCHOR | F204 | CROSS_SSE | CROSS:ss2→ss1 |
| #16 | L16 | H7 | 22 | +0.0343 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #24 | L16 | H12 | 23 | +0.0468 | DISTRIBUTED |  | DISTRIBUTED |  | POSITIONAL | INTRA:ss2 |
| #30 | L17 | H7 | 29 | +0.0288 | DISTRIBUTED |  | DISTRIBUTED |  |  |  |
| #7 | L17 | H10 | 19 | +0.1211 | SINGLE-ANCHOR | V202 | DISTRIBUTED |  |  | INTRA:ss2 |
| #19 | L17 | H18 | 14 | +0.0443 | DISTRIBUTED |  | DUAL-ANCHOR | V202/F204 |  |  |
| #25 | L19 | H3 | 13 | +0.0471 | SINGLE-ANCHOR | V202 | DISTRIBUTED |  | POSITIONAL | INTRA:ss2 |
| #13 | L26 | H16 | 15 | +0.0457 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #5 | L27 | H15 | 19 | +0.0909 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #6 | L29 | H18 | 20 | +0.1370 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |
| #3 | L32 | H13 | 20 | +0.0683 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss1→ss2 |
| #4 | L32 | H18 | 18 | +0.0703 | DISTRIBUTED |  | DISTRIBUTED |  |  | CROSS:ss2→ss1 |

