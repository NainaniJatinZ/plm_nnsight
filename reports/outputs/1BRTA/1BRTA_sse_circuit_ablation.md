# SSE Circuit Ablation: 1BRTA

Generated: 2026-03-05 04:19:04   Model: facebook/esm2_t33_650M_UR50D

## Hypothesis

INTRA heads gather local SSE information within regions. CROSS heads bridge the two contact sides. Ablating INTRA heads should drop both contact and SSE accuracy. Ablating CROSS heads should drop contact accuracy but preserve SSE accuracy.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1BRTA |
| Contact pair | (119, 221) |
| ss1 | [114, 125) |
| ss2 | [216, 227) |
| Clean flank | 32 |
| Corrupt flank | 31 |
| Top-K cells | 1000 |

## Cell Partition

| Group | Cells | Heads |
|-------|-------|-------|
| INTRA | 121 | 9 |
| CROSS | 178 | 11 |
| ANCHOR | 103 | 8 |
| OTHER | 598 | 62 |
| **Total** | **1000** | **90** |

**INTRA heads**: L6H12, L10H0, L11H14, L13H2, L13H9, L14H14, L17H10, L18H8, L19H0

**CROSS heads**: L7H4, L9H7, L10H9, L12H2, L18H1, L22H14, L26H16, L27H15, L30H1, L32H13, L32H18

**ANCHOR heads**: L5H19, L7H0, L7H16, L12H19, L13H17, L14H0, L14H13, L16H18

**OTHER heads**: L0H7, L0H9, L0H13, L0H19, L1H8, L2H9, L2H16, L4H2, L4H13, L4H16, L5H11, L6H3, L6H15, L7H13, L8H0, L8H10, L8H13, L9H13, L10H12, L10H16, L11H10, L12H6, L12H10, L12H16, L13H1, L13H7, L13H13, L13H14, L13H16, L13H18, L13H19, L14H9, L15H2, L15H7, L15H18, L16H0, L16H12, L16H15, L16H17, L16H19, L17H13, L17H18, L17H19, L18H2, L18H17, L20H0, L20H5, L21H2, L23H6, L24H18, L25H12, L28H18, L29H10, L29H15, L29H18, L30H0, L30H2, L30H4, L30H6, L30H13, L32H11, L32H14

## Results

### Baselines

| | Value |
|---|---|
| Clean metric | 0.7367 |
| Corrupt metric | 0.0152 |
| Gap | 0.7215 |

### Ablation Conditions

| Condition | #cells | contact | faith | ss1 | ss2 | seg_mean | flkL | flkR | flk_mean |
|-----------|--------|---------|-------|-----|-----|----------|------|------|----------|
| none | 0 | 0.0152 | 0.00% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |
| full_circuit | 1000 | 0.3769 | 50.13% | 0.364 | 1.000 | 0.682 | 0.750 | 0.938 | 0.844 |
| –INTRA | 879 | 0.0691 | 7.47% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |
| –CROSS | 822 | 0.0169 | 0.23% | 0.091 | 1.000 | 0.545 | 0.750 | 0.938 | 0.844 |
| –ANCHOR | 897 | 0.1173 | 14.15% | 0.091 | 1.000 | 0.545 | 0.750 | 0.938 | 0.844 |
| –OTHER | 402 | 0.0205 | 0.73% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |
| only_INTRA | 121 | 0.0153 | 0.00% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |
| only_CROSS | 178 | 0.0153 | 0.02% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |
| only_ANCHOR | 103 | 0.0152 | -0.00% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |
| only_OTHER | 598 | 0.0155 | 0.03% | 0.091 | 1.000 | 0.545 | 0.688 | 0.938 | 0.812 |

### SSE Ground Truth

| Segment | SSE |
|---------|-----|
| SS1 [114:125] | `CECEEEEEECE` |
| SS2 [216:227] | `CCCEEEEECCC` |

### Per-Residue SSE Changes

#### –INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 105 | H | H | E |
| flkL | 109 | H | H | C |

#### –CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |
| flkL | 109 | H | H | C |
| flkL | 113 | H | C | H |

#### –ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |

#### –OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |
| flkL | 105 | H | H | E |
| flkL | 109 | H | H | C |

#### only_INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |
| flkL | 105 | H | H | E |
| flkL | 109 | H | H | C |

#### only_CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |
| flkL | 105 | H | H | E |
| flkL | 109 | H | H | C |

#### only_ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |
| flkL | 105 | H | H | E |
| flkL | 109 | H | H | C |

#### only_OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 116 | C | C | H |
| ss1 | 120 | E | E | H |
| ss1 | 121 | E | E | H |
| flkL | 90 | C | C | E |
| flkL | 99 | H | C | H |
| flkL | 105 | H | H | E |
| flkL | 109 | H | H | C |

## Interpretation

### Effect of removing each group (drop from full_circuit)

| Removed | Contact drop | SSE seg drop |
|---------|-------------|-------------|
| INTRA | +0.3078 | +0.136 |
| CROSS | +0.3600 | +0.136 |
| ANCHOR | +0.2596 | +0.136 |
| OTHER | +0.3565 | +0.136 |

### Sufficiency of each group alone (only_X)

| Kept | Contact | Faith | SSE seg |
|------|---------|-------|---------|
| INTRA | 0.0153 | 0.00% | 0.545 |
| CROSS | 0.0153 | 0.02% | 0.545 |
| ANCHOR | 0.0152 | -0.00% | 0.545 |
| OTHER | 0.0155 | 0.03% | 0.545 |

**Inconclusive**: removing INTRA and CROSS cause similar SSE drops (+0.136 vs +0.136).
