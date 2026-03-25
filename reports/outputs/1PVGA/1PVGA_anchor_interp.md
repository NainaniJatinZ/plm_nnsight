# Anchor Residue Interpretation: 1PVGA

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 1PVGA |
| Contact pair | (101, 202) |
| ss1 | [96, 107) |
| ss2 | [197, 208) |
| Clean flank | 64 |
| Corrupt flank | 63 |
| Jump residues | [32, 133, 170, 271] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 32 | Y | flkL | K(2) | 2 | 0.872 | H | interior | 4 | YES |
| 92 | I | flkL | K(1) | 1 | 0.588 | E | interior | 7 |  |
| 97 | H | ss1 | K(1)+Q(1) | 2 | 0.474 | C | - |  |  |
| 101 | V | ss1 | K(10)+Q(4) | 14 | 0.775 | E | interior | 6 |  |
| 198 | Y | ss2 | K(1) | 1 | 0.780 | E | boundary | 8 |  |
| 201 | V | ss2 | K(2)+Q(7) | 9 | 0.651 | E | interior | 8 |  |
| 203 | F | ss2 | K(1)+Q(1) | 2 | 0.849 | E | interior | 8 |  |
| 271 | G | flkR | K(1) | 1 | 0.217 | C | - |  | YES |

## Head Assignments per Anchor

### Position 32 (Y) — K(2)

K anchor for: L0H9(r10,s), L0H12(r19,d)

### Position 92 (I) — K(1)

K anchor for: L4H5(r25,s)

### Position 97 (H) — K(1)+Q(1)

K anchor for: L5H9(r7,s)

Q anchor for: L4H5(r25,s)

### Position 101 (V) — K(10)+Q(4)

K anchor for: L10H9(r1,s), L11H16(r11,s), L8H2(r12,s), L15H8(r13,s), L14H4(r14,s), L7H7(r18,s), L14H9(r20,d), L13H18(r22,s), L11H14(r28,s), L12H15(r30,s)

Q anchor for: L5H9(r7,s), L6H0(r17,s), L4H14(r26,s), L9H15(r29,s)

### Position 198 (Y) — K(1)

K anchor for: L14H9(r20,d)

### Position 201 (V) — K(2)+Q(7)

K anchor for: L17H10(r8,s), L13H2(r27,d)

Q anchor for: L9H17(r2,s), L15H8(r13,s), L14H4(r14,s), L12H10(r16,s), L14H9(r20,s), L17H18(r24,d), L13H2(r27,s)

### Position 203 (F) — K(1)+Q(1)

K anchor for: L13H2(r27,d)

Q anchor for: L17H18(r24,d)

### Position 271 (G) — K(1)

K anchor for: L0H12(r19,d)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 8 |
| K-only anchors | 4 |
| Q-only anchors | 0 |
| Both K and Q | 4 |
| Jump residues among anchors | 2 |
| SSE breakdown | H=1, E=5, C=2 |
| Region breakdown | flkL=2, flkR=1, ss1=2, ss2=3 |
| SSE position | boundary=1, interior=5 |
| Conservation (mean) | 0.651 |
| Conservation (range) | [0.217, 0.872] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (101, 202) |
| Total flank residues | 218 |
| Flank anchors | 3 |
| Flank non-anchors | 215 |
| Anchor coupling (mean) | -2.10 |
| Non-anchor coupling (mean) | -1.44 |
| Top quartile threshold | -1.33 |
| Anchors in top quartile | 0/3 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.8027 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 92 | I | 1 | -2.06 |  |
| 32 | Y | 2 | -2.11 |  |
| 271 | G | 1 | -2.14 |  |
