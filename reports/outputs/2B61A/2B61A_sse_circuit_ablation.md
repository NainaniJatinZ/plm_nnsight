# SSE Circuit Ablation: 2B61A

Generated: 2026-03-04 17:12:02   Model: facebook/esm2_t33_650M_UR50D

## Hypothesis

INTRA heads gather local SSE information within regions. CROSS heads bridge the two contact sides. Ablating INTRA heads should drop both contact and SSE accuracy. Ablating CROSS heads should drop contact accuracy but preserve SSE accuracy.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 2B61A |
| Contact pair | (182, 316) |
| ss1 | [177, 188) |
| ss2 | [311, 322) |
| Clean flank | 44 |
| Corrupt flank | 43 |
| Top-K cells | 1000 |

## Cell Partition

| Group | Cells | Heads |
|-------|-------|-------|
| INTRA | 94 | 5 |
| CROSS | 96 | 7 |
| ANCHOR | 356 | 15 |
| OTHER | 454 | 18 |
| **Total** | **1000** | **45** |

**INTRA heads**: L0H6, L1H8, L1H13, L6H8, L9H1

**CROSS heads**: L8H12, L13H8, L22H14, L27H15, L30H1, L32H13, L32H18

**ANCHOR heads**: L0H7, L5H19, L6H3, L6H19, L7H16, L8H19, L10H9, L11H1, L11H16, L14H9, L14H14, L15H2, L16H17, L17H18, L19H0

**OTHER heads**: L0H8, L5H6, L6H17, L7H0, L7H13, L7H15, L9H2, L11H6, L12H3, L13H18, L14H0, L14H13, L14H19, L16H7, L16H15, L17H5, L19H15, L26H16

## Results

### Baselines

| | Value |
|---|---|
| Clean metric | 0.5738 |
| Corrupt metric | 0.0279 |
| Gap | 0.5459 |

### Ablation Conditions

| Condition | #cells | contact | faith | ss1 | ss2 | seg_mean | flkL | flkR | flk_mean |
|-----------|--------|---------|-------|-----|-----|----------|------|------|----------|
| none | 0 | 0.0279 | 0.00% | 0.455 | 0.909 | 0.682 | 0.841 | 0.932 | 0.886 |
| full_circuit | 1000 | 0.3359 | 56.43% | 0.818 | 1.000 | 0.909 | 0.841 | 0.955 | 0.898 |
| –INTRA | 906 | 0.2910 | 48.21% | 0.818 | 1.000 | 0.909 | 0.841 | 0.955 | 0.898 |
| –CROSS | 904 | 0.0490 | 3.87% | 0.818 | 1.000 | 0.909 | 0.841 | 0.955 | 0.898 |
| –ANCHOR | 644 | 0.0365 | 1.59% | 0.727 | 1.000 | 0.864 | 0.841 | 0.932 | 0.886 |
| –OTHER | 546 | 0.1100 | 15.05% | 0.818 | 1.000 | 0.909 | 0.841 | 0.909 | 0.875 |
| only_INTRA | 94 | 0.0279 | 0.00% | 0.545 | 0.909 | 0.727 | 0.841 | 0.932 | 0.886 |
| only_CROSS | 96 | 0.0286 | 0.13% | 0.545 | 0.909 | 0.727 | 0.841 | 0.932 | 0.886 |
| only_ANCHOR | 356 | 0.0281 | 0.04% | 0.818 | 0.909 | 0.864 | 0.841 | 0.909 | 0.875 |
| only_OTHER | 454 | 0.0288 | 0.18% | 0.727 | 0.909 | 0.818 | 0.841 | 0.932 | 0.886 |

### SSE Ground Truth

| Segment | SSE |
|---------|-----|
| SS1 [177:188] | `HHCEEEEECCC` |
| SS2 [311:322] | `CCEEEEEECCC` |

### Per-Residue SSE Changes

#### –INTRA

_(no SSE prediction changes)_

#### –CROSS

_(no SSE prediction changes)_

#### –ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 179 | C | C | H |
| flkR | 343 | C | C | E |

#### –OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkR | 343 | C | C | E |
| flkR | 358 | H | H | C |

#### only_INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 179 | C | C | H |
| ss1 | 182 | E | E | H |
| ss1 | 184 | E | E | C |
| ss2 | 313 | E | E | C |
| flkR | 343 | C | C | E |

#### only_CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 179 | C | C | H |
| ss1 | 182 | E | E | H |
| ss1 | 184 | E | E | C |
| ss2 | 313 | E | E | C |
| flkR | 343 | C | C | E |

#### only_ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss2 | 313 | E | E | C |
| flkR | 343 | C | C | E |
| flkR | 358 | H | H | C |

#### only_OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 179 | C | C | H |
| ss2 | 313 | E | E | C |
| flkR | 343 | C | C | E |

## Interpretation

### Effect of removing each group (drop from full_circuit)

| Removed | Contact drop | SSE seg drop |
|---------|-------------|-------------|
| INTRA | +0.0449 | +0.000 |
| CROSS | +0.2869 | +0.000 |
| ANCHOR | +0.2994 | +0.045 |
| OTHER | +0.2259 | +0.000 |

### Sufficiency of each group alone (only_X)

| Kept | Contact | Faith | SSE seg |
|------|---------|-------|---------|
| INTRA | 0.0279 | 0.00% | 0.727 |
| CROSS | 0.0286 | 0.13% | 0.727 |
| ANCHOR | 0.0281 | 0.04% | 0.864 |
| OTHER | 0.0288 | 0.18% | 0.818 |

**Inconclusive**: removing INTRA and CROSS cause similar SSE drops (+0.000 vs +0.000).
