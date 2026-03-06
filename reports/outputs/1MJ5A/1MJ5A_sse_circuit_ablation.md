# SSE Circuit Ablation: 1MJ5A

Generated: 2026-03-05 04:22:04   Model: facebook/esm2_t33_650M_UR50D

## Hypothesis

INTRA heads gather local SSE information within regions. CROSS heads bridge the two contact sides. Ablating INTRA heads should drop both contact and SSE accuracy. Ablating CROSS heads should drop contact accuracy but preserve SSE accuracy.

## Configuration

| Parameter | Value |
|-----------|-------|
| Protein | 1MJ5A |
| Contact pair | (128, 240) |
| ss1 | [123, 134) |
| ss2 | [235, 246) |
| Clean flank | 35 |
| Corrupt flank | 34 |
| Top-K cells | 1000 |

## Cell Partition

| Group | Cells | Heads |
|-------|-------|-------|
| INTRA | 89 | 11 |
| CROSS | 152 | 11 |
| ANCHOR | 33 | 5 |
| OTHER | 726 | 158 |
| **Total** | **1000** | **185** |

**INTRA heads**: L6H12, L7H7, L8H6, L9H13, L14H14, L17H10, L17H19, L18H6, L19H0, L19H14, L25H16

**CROSS heads**: L13H15, L16H19, L17H18, L19H15, L22H14, L26H16, L27H15, L29H15, L30H1, L32H13, L32H18

**ANCHOR heads**: L5H19, L7H0, L10H12, L13H2, L31H8

**OTHER heads**: L0H9, L0H11, L0H19, L1H7, L1H16, L1H17, L2H4, L2H9, L3H19, L4H18, L5H13, L6H3, L6H8, L6H11, L6H19, L7H4, L7H12, L8H9, L8H12, L8H14, L9H3, L9H5, L9H7, L9H12, L9H18, L10H0, L10H3, L10H7, L10H9, L10H10, L10H14, L11H0, L11H9, L11H13, L11H14, L11H16, L11H17, L11H19, L12H0, L12H2, L12H3, L12H9, L12H10, L12H16, L13H1, L13H4, L13H5, L13H6, L13H8, L13H9, L13H10, L13H12, L13H18, L14H8, L14H9, L14H13, L15H1, L15H6, L15H12, L15H16, L15H18, L16H7, L16H12, L16H14, L16H16, L17H4, L17H5, L17H6, L17H7, L17H8, L17H9, L17H12, L17H15, L18H1, L18H3, L18H14, L18H16, L19H3, L19H6, L19H17, L20H0, L20H2, L20H3, L20H4, L20H5, L20H10, L20H18, L21H2, L21H5, L21H11, L21H15, L21H18, L22H0, L22H3, L22H4, L22H6, L22H7, L22H9, L22H10, L23H2, L23H3, L23H6, L23H8, L23H13, L24H0, L24H5, L24H6, L24H7, L24H12, L24H14, L24H15, L24H18, L25H0, L25H6, L25H11, L25H13, L25H18, L25H19, L26H3, L26H8, L26H13, L26H19, L27H1, L27H4, L27H5, L27H9, L27H10, L27H12, L27H14, L27H17, L28H1, L28H2, L28H9, L28H10, L28H12, L28H13, L28H16, L28H18, L28H19, L29H0, L29H4, L29H16, L29H17, L29H18, L30H0, L30H2, L30H13, L30H18, L31H1, L31H10, L31H14, L31H15, L31H17, L31H18, L32H0, L32H3, L32H4, L32H14

## Results

### Baselines

| | Value |
|---|---|
| Clean metric | 0.8945 |
| Corrupt metric | 0.0078 |
| Gap | 0.8867 |

### Ablation Conditions

| Condition | #cells | contact | faith | ss1 | ss2 | seg_mean | flkL | flkR | flk_mean |
|-----------|--------|---------|-------|-----|-----|----------|------|------|----------|
| none | 0 | 0.0078 | 0.00% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |
| full_circuit | 1000 | 0.0144 | 0.74% | 0.455 | 0.818 | 0.636 | 0.800 | 0.914 | 0.857 |
| –INTRA | 911 | 0.0103 | 0.28% | 0.273 | 0.818 | 0.545 | 0.800 | 0.914 | 0.857 |
| –CROSS | 848 | 0.0080 | 0.02% | 0.273 | 0.818 | 0.545 | 0.800 | 0.886 | 0.843 |
| –ANCHOR | 967 | 0.0085 | 0.08% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |
| –OTHER | 274 | 0.0083 | 0.06% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |
| only_INTRA | 89 | 0.0078 | 0.00% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |
| only_CROSS | 152 | 0.0079 | 0.01% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |
| only_ANCHOR | 33 | 0.0078 | -0.00% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |
| only_OTHER | 726 | 0.0078 | 0.00% | 0.091 | 0.818 | 0.455 | 0.829 | 0.886 | 0.857 |

### SSE Ground Truth

| Segment | SSE |
|---------|-----|
| SS1 [123:134] | `CEEEEEEECCC` |
| SS2 [235:246] | `CCEEEEECCCC` |

### Per-Residue SSE Changes

#### –INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |

#### –CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| flkR | 257 | H | H | C |

#### –ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| ss1 | 132 | C | C | H |
| ss1 | 133 | C | C | H |
| flkL | 121 | H | C | H |
| flkR | 257 | H | H | C |

#### –OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| ss1 | 132 | C | C | H |
| ss1 | 133 | C | C | H |
| flkL | 121 | H | C | H |
| flkR | 257 | H | H | C |

#### only_INTRA

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| ss1 | 132 | C | C | H |
| ss1 | 133 | C | C | H |
| flkL | 121 | H | C | H |
| flkR | 257 | H | H | C |

#### only_CROSS

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| ss1 | 132 | C | C | H |
| ss1 | 133 | C | C | H |
| flkL | 121 | H | C | H |
| flkR | 257 | H | H | C |

#### only_ANCHOR

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| ss1 | 132 | C | C | H |
| ss1 | 133 | C | C | H |
| flkL | 121 | H | C | H |
| flkR | 257 | H | H | C |

#### only_OTHER

| Seg | Pos | gt | full | abl |
|-----|-----|----|------|-----|
| ss1 | 127 | E | E | H |
| ss1 | 131 | C | C | H |
| ss1 | 132 | C | C | H |
| ss1 | 133 | C | C | H |
| flkL | 121 | H | C | H |
| flkR | 257 | H | H | C |

## Interpretation

### Effect of removing each group (drop from full_circuit)

| Removed | Contact drop | SSE seg drop |
|---------|-------------|-------------|
| INTRA | +0.0041 | +0.091 |
| CROSS | +0.0064 | +0.091 |
| ANCHOR | +0.0059 | +0.182 |
| OTHER | +0.0061 | +0.182 |

### Sufficiency of each group alone (only_X)

| Kept | Contact | Faith | SSE seg |
|------|---------|-------|---------|
| INTRA | 0.0078 | 0.00% | 0.455 |
| CROSS | 0.0079 | 0.01% | 0.455 |
| ANCHOR | 0.0078 | -0.00% | 0.455 |
| OTHER | 0.0078 | 0.00% | 0.455 |

**Inconclusive**: removing INTRA and CROSS cause similar SSE drops (+0.091 vs +0.091).
