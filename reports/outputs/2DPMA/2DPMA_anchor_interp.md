# Anchor Residue Interpretation: 2DPMA

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 2DPMA |
| Contact pair | (59, 172) |
| ss1 | [54, 65) |
| ss2 | [167, 178) |
| Clean flank | 30 |
| Corrupt flank | 29 |
| Jump residues | [24, 94, 137, 207] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 39 | F | flkL | K(4)+Q(1) | 5 | 0.362 | E | interior | 3 |  |
| 42 | F | flkL | K(3) | 3 | 0.809 | C | - |  |  |
| 57 | A | ss1 | K(2)+Q(5) | 7 | 0.290 | E | interior | 6 |  |
| 59 | I | ss1 | K(1)+Q(1) | 2 | 0.462 | E | interior | 6 |  |
| 61 | D | ss1 | K(1) | 1 | 0.914 | E | boundary | 6 |  |
| 170 | L | ss2 | Q(1) | 1 | 0.412 | E | interior | 6 |  |
| 172 | I | ss2 | Q(3) | 3 | 0.543 | E | interior | 6 |  |
| 176 | D | ss2 | Q(1) | 1 | 0.581 | C | - |  |  |
| 190 | V | flkR | K(7)+Q(1) | 8 | 0.427 | E | interior | 4 |  |

## Head Assignments per Anchor

### Position 39 (F) — K(4)+Q(1)

K anchor for: L10H9(r2,s), L10H12(r4,s), L11H14(r18,s), L10H7(r21,s)

Q anchor for: L7H0(r12,s)

### Position 42 (F) — K(3)

K anchor for: L12H17(r6,s), L9H10(r11,s), L5H19(r28,s)

### Position 57 (A) — K(2)+Q(5)

K anchor for: L22H14(r8,d), L7H0(r12,s)

Q anchor for: L6H7(r1,s), L9H10(r11,s), L10H7(r21,s), L17H1(r22,d), L12H16(r26,s)

### Position 59 (I) — K(1)+Q(1)

K anchor for: L22H14(r8,d)

Q anchor for: L17H1(r22,d)

### Position 61 (D) — K(1)

K anchor for: L21H6(r27,s)

### Position 170 (L) — Q(1)

Q anchor for: L22H14(r8,d)

### Position 172 (I) — Q(3)

Q anchor for: L22H14(r8,d), L13H1(r16,d), L12H15(r25,s)

### Position 176 (D) — Q(1)

Q anchor for: L13H1(r16,d)

### Position 190 (V) — K(7)+Q(1)

K anchor for: L6H7(r1,s), L16H7(r14,s), L13H1(r16,s), L15H6(r17,s), L13H8(r20,s), L12H15(r25,s), L12H16(r26,s)

Q anchor for: L5H19(r28,s)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 9 |
| K-only anchors | 2 |
| Q-only anchors | 3 |
| Both K and Q | 4 |
| Jump residues among anchors | 0 |
| SSE breakdown | H=0, E=7, C=2 |
| Region breakdown | flkL=2, flkR=1, ss1=3, ss2=3 |
| SSE position | boundary=1, interior=6 |
| Conservation (mean) | 0.533 |
| Conservation (range) | [0.290, 0.914] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (59, 172) |
| Total flank residues | 120 |
| Flank anchors | 3 |
| Flank non-anchors | 117 |
| Anchor coupling (mean) | -1.07 |
| Non-anchor coupling (mean) | -0.73 |
| Top quartile threshold | -0.89 |
| Anchors in top quartile | 1/3 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.1780 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 190 | V | 8 | -0.64 | YES |
| 42 | F | 3 | -1.19 |  |
| 39 | F | 5 | -1.38 |  |
