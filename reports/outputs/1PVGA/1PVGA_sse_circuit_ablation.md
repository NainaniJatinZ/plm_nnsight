# SSE Circuit Ablation: 1PVGA

Generated: 2026-03-05 04:23:22   Model: facebook/esm2_t33_650M_UR50D

## Hypothesis

INTRA heads gather local SSE information within regions. CROSS heads bridge the two contact sides. Ablating INTRA heads should drop both contact and SSE accuracy. Ablating CROSS heads should drop contact accuracy but preserve SSE accuracy.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1PVGA |
| Contact pair | (101, 202) |
| ss1 | [96, 107) |
| ss2 | [197, 208) |
| Clean flank | 64 |
| Corrupt flank | 63 |
| Top-K cells | 1000 |

## Cell Partition

| Group | Cells | Heads |
|-------|-------|-------|
| INTRA | 103 | 4 |
| CROSS | 98 | 7 |
| ANCHOR | 424 | 16 |
| OTHER | 375 | 18 |
| **Total** | **1000** | **45** |

**INTRA heads**: L0H9, L0H12, L13H2, L17H10

**CROSS heads**: L14H4, L15H8, L26H16, L27H15, L29H18, L32H13, L32H18

**ANCHOR heads**: L4H5, L4H14, L5H9, L6H0, L7H7, L8H2, L9H15, L9H17, L10H9, L11H14, L11H16, L12H10, L12H15, L13H18, L14H9, L17H18

**OTHER heads**: L0H7, L1H1, L2H17, L2H18, L6H17, L6H19, L7H13, L7H14, L7H18, L12H8, L13H17, L14H0, L14H3, L16H7, L16H14, L20H3, L21H13, L24H18

## Results

### Baselines

| | Value |
|---|---|
| Clean metric | 0.5921 |
| Corrupt metric | 0.0644 |
| Gap | 0.5277 |

### Ablation Conditions

| Condition | #cells | contact | faith | ss1 | ss2 | seg_mean | flkL | flkR | flk_mean |
|-----------|--------|---------|-------|-----|-----|----------|------|------|----------|
| none | 0 | 0.0644 | 0.00% | 0.909 | 0.909 | 0.909 | 0.750 | 0.703 | 0.727 |
| full_circuit | 1000 | 0.4454 | 72.20% | 0.909 | 0.909 | 0.909 | 0.797 | 0.719 | 0.758 |
| –INTRA | 897 | 0.2846 | 41.72% | 0.909 | 0.818 | 0.864 | 0.797 | 0.719 | 0.758 |
| –CROSS | 902 | 0.0669 | 0.47% | 0.909 | 0.909 | 0.909 | 0.797 | 0.719 | 0.758 |
| –ANCHOR | 576 | 0.0989 | 6.53% | 0.909 | 0.909 | 0.909 | 0.781 | 0.703 | 0.742 |
| –OTHER | 625 | 0.2994 | 44.52% | 0.909 | 0.909 | 0.909 | 0.797 | 0.703 | 0.750 |
| only_INTRA | 103 | 0.0644 | 0.00% | 0.909 | 0.909 | 0.909 | 0.766 | 0.703 | 0.734 |
| only_CROSS | 98 | 0.0755 | 2.10% | 0.909 | 0.909 | 0.909 | 0.750 | 0.703 | 0.727 |
| only_ANCHOR | 424 | 0.0647 | 0.05% | 0.909 | 0.909 | 0.909 | 0.797 | 0.703 | 0.750 |
| only_OTHER | 375 | 0.0646 | 0.03% | 0.909 | 0.909 | 0.909 | 0.781 | 0.703 | 0.742 |

### SSE Ground Truth

| Segment | SSE |
|---------|-----|
| SS1 [96:107] | `CCEEEEECCCC` |
| SS2 [197:208] | `CEEEEEEECCC` |

### Per-Residue SSE Changes

#### –INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss2 | 205 | C | C | E |

#### –CROSS

_(no SSE prediction changes)_

#### –ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkL | 79 | H | H | C |
| flkR | 210 | C | C | H |
| flkR | 248 | C | H | C |
| flkR | 249 | C | C | H |

#### –OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkR | 249 | C | C | H |

#### only_INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkL | 79 | H | H | C |
| flkL | 94 | C | C | E |
| flkR | 210 | C | C | H |
| flkR | 248 | C | H | C |
| flkR | 249 | C | C | H |

#### only_CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkL | 79 | H | H | C |
| flkL | 86 | C | C | E |
| flkL | 94 | C | C | E |
| flkR | 210 | C | C | H |
| flkR | 248 | C | H | C |
| flkR | 249 | C | C | H |

#### only_ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkR | 210 | C | C | H |
| flkR | 248 | C | H | C |
| flkR | 249 | C | C | H |

#### only_OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkL | 79 | H | H | C |
| flkR | 210 | C | C | H |
| flkR | 248 | C | H | C |
| flkR | 249 | C | C | H |

## Interpretation

### Effect of removing each group (drop from full_circuit)

| Removed | Contact drop | SSE seg drop |
|---------|-------------|-------------|
| INTRA | +0.1608 | +0.045 |
| CROSS | +0.3785 | +0.000 |
| ANCHOR | +0.3465 | +0.000 |
| OTHER | +0.1460 | +0.000 |

### Sufficiency of each group alone (only_X)

| Kept | Contact | Faith | SSE seg |
|------|---------|-------|---------|
| INTRA | 0.0644 | 0.00% | 0.909 |
| CROSS | 0.0755 | 2.10% | 0.909 |
| ANCHOR | 0.0647 | 0.05% | 0.909 |
| OTHER | 0.0646 | 0.03% | 0.909 |

**Inconclusive**: removing INTRA and CROSS cause similar SSE drops (+0.045 vs +0.000).
