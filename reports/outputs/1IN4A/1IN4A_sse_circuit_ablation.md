# SSE Circuit Ablation: 1IN4A

Generated: 2026-03-05 04:20:34   Model: facebook/esm2_t33_650M_UR50D

## Hypothesis

INTRA heads gather local SSE information within regions. CROSS heads bridge the two contact sides. Ablating INTRA heads should drop both contact and SSE accuracy. Ablating CROSS heads should drop contact accuracy but preserve SSE accuracy.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1IN4A |
| Contact pair | (55, 174) |
| ss1 | [50, 61) |
| ss2 | [169, 180) |
| Clean flank | 40 |
| Corrupt flank | 39 |
| Top-K cells | 1000 |

## Cell Partition

| Group | Cells | Heads |
|-------|-------|-------|
| INTRA | 17 | 1 |
| CROSS | 143 | 8 |
| ANCHOR | 369 | 16 |
| OTHER | 471 | 22 |
| **Total** | **1000** | **47** |

**INTRA heads**: L20H1

**CROSS heads**: L15H4, L17H3, L19H9, L27H15, L30H1, L30H13, L32H13, L32H18

**ANCHOR heads**: L4H8, L5H19, L7H6, L11H16, L13H8, L13H12, L13H19, L14H9, L15H2, L15H6, L16H7, L16H18, L17H19, L19H1, L20H5, L21H17

**OTHER heads**: L0H7, L5H4, L6H17, L7H4, L7H9, L7H13, L10H12, L11H18, L12H0, L12H2, L13H7, L13H16, L13H18, L15H10, L17H10, L18H1, L20H3, L20H19, L22H14, L26H16, L29H18, L31H17

## Results

### Baselines

| | Value |
|---|---|
| Clean metric | 0.9656 |
| Corrupt metric | 0.3736 |
| Gap | 0.5921 |

### Ablation Conditions

| Condition | #cells | contact | faith | ss1 | ss2 | seg_mean | flkL | flkR | flk_mean |
|-----------|--------|---------|-------|-----|-----|----------|------|------|----------|
| none | 0 | 0.3736 | 0.00% | 0.909 | 0.818 | 0.864 | 0.775 | 0.875 | 0.825 |
| full_circuit | 1000 | 0.5582 | 31.19% | 0.909 | 0.727 | 0.818 | 0.800 | 0.875 | 0.838 |
| –INTRA | 983 | 0.5582 | 31.19% | 0.909 | 0.727 | 0.818 | 0.800 | 0.875 | 0.838 |
| –CROSS | 857 | 0.4036 | 5.08% | 0.909 | 0.727 | 0.818 | 0.800 | 0.875 | 0.838 |
| –ANCHOR | 631 | 0.4238 | 8.48% | 0.909 | 0.727 | 0.818 | 0.775 | 0.875 | 0.825 |
| –OTHER | 529 | 0.4210 | 8.01% | 0.909 | 0.727 | 0.818 | 0.800 | 0.875 | 0.838 |
| only_INTRA | 17 | 0.3736 | 0.00% | 0.909 | 0.818 | 0.864 | 0.775 | 0.875 | 0.825 |
| only_CROSS | 143 | 0.3854 | 2.01% | 0.909 | 0.818 | 0.864 | 0.775 | 0.875 | 0.825 |
| only_ANCHOR | 369 | 0.3723 | -0.21% | 0.909 | 0.727 | 0.818 | 0.800 | 0.875 | 0.838 |
| only_OTHER | 471 | 0.3805 | 1.18% | 0.909 | 0.727 | 0.818 | 0.775 | 0.875 | 0.825 |

### SSE Ground Truth

| Segment | SSE |
|---------|-----|
| SS1 [50:61] | `CCEEEEEECCC` |
| SS2 [169:180] | `HCCCEEECCCC` |

### Per-Residue SSE Changes

#### –INTRA

_(no SSE prediction changes)_

#### –CROSS

_(no SSE prediction changes)_

#### –ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkL | 11 | C | C | H |

#### –OTHER

_(no SSE prediction changes)_

#### only_INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss2 | 176 | C | E | C |
| flkL | 11 | C | C | H |

#### only_CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss2 | 176 | C | E | C |
| flkL | 11 | C | C | H |

#### only_ANCHOR

_(no SSE prediction changes)_

#### only_OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| flkL | 11 | C | C | H |

## Interpretation

### Effect of removing each group (drop from full_circuit)

| Removed | Contact drop | SSE seg drop |
|---------|-------------|-------------|
| INTRA | +0.0000 | +0.000 |
| CROSS | +0.1546 | +0.000 |
| ANCHOR | +0.1345 | +0.000 |
| OTHER | +0.1373 | +0.000 |

### Sufficiency of each group alone (only_X)

| Kept | Contact | Faith | SSE seg |
|------|---------|-------|---------|
| INTRA | 0.3736 | 0.00% | 0.864 |
| CROSS | 0.3854 | 2.01% | 0.864 |
| ANCHOR | 0.3723 | -0.21% | 0.818 |
| OTHER | 0.3805 | 1.18% | 0.818 |

**Inconclusive**: removing INTRA and CROSS cause similar SSE drops (+0.000 vs +0.000).
