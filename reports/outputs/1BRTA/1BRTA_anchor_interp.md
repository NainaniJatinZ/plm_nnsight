# Anchor Residue Interpretation: 1BRTA

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 1BRTA |
| Contact pair | (119, 221) |
| ss1 | [114, 125) |
| ss2 | [216, 227) |
| Clean flank | 32 |
| Corrupt flank | 31 |
| Jump residues | [82, 156, 184, 258] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 82 | V | flkL | K(1) | 1 | 0.486 | H | interior | 14 | YES |
| 93 | L | flkL | K(6)+Q(3) | 9 | 0.507 | E | interior | 6 |  |
| 95 | G | flkL | K(2) | 2 | 0.810 | E | interior | 6 |  |
| 99 | G | flkL | K(2)+Q(1) | 3 | 0.925 | H | interior | 13 |  |
| 118 | V | ss1 | K(4)+Q(5) | 9 | 0.570 | E | interior | 5 |  |
| 120 | F | ss1 | Q(3) | 3 | 0.426 | E | interior | 5 |  |
| 220 | L | ss2 | K(5)+Q(1) | 6 | 0.601 | E | interior | 7 |  |
| 248 | Y | flkR | K(1) | 1 | 0.275 | E | interior | 5 |  |

## Head Assignments per Anchor

### Position 82 (V) — K(1)

K anchor for: L6H12(r11,s)

### Position 93 (L) — K(6)+Q(3)

K anchor for: L11H14(r3,s), L12H19(r10,s), L14H0(r17,d), L13H17(r19,d), L10H0(r20,s), L13H9(r25,s)

Q anchor for: L9H7(r6,s), L6H12(r11,s), L7H0(r18,s)

### Position 95 (G) — K(2)

K anchor for: L5H19(r4,s), L13H17(r19,d)

### Position 99 (G) — K(2)+Q(1)

K anchor for: L14H0(r17,d), L14H13(r27,s)

Q anchor for: L13H9(r25,s)

### Position 118 (V) — K(4)+Q(5)

K anchor for: L17H10(r9,s), L7H0(r18,s), L19H0(r24,s), L13H2(r26,s)

Q anchor for: L5H19(r4,s), L13H17(r19,s), L18H1(r21,d), L18H8(r28,s), L16H18(r29,d)

### Position 120 (F) — Q(3)

Q anchor for: L18H1(r21,d), L19H0(r24,s), L16H18(r29,d)

### Position 220 (L) — K(5)+Q(1)

K anchor for: L9H7(r6,s), L7H4(r14,s), L10H9(r15,s), L12H2(r16,s), L18H1(r21,s)

Q anchor for: L7H16(r23,s)

### Position 248 (Y) — K(1)

K anchor for: L7H16(r23,s)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 8 |
| K-only anchors | 3 |
| Q-only anchors | 1 |
| Both K and Q | 4 |
| Jump residues among anchors | 1 |
| SSE breakdown | H=2, E=6, C=0 |
| Region breakdown | flkL=4, flkR=1, ss1=2, ss2=1 |
| SSE position | interior=8 |
| Conservation (mean) | 0.575 |
| Conservation (range) | [0.275, 0.925] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (119, 221) |
| Total flank residues | 128 |
| Flank anchors | 5 |
| Flank non-anchors | 123 |
| Anchor coupling (mean) | 1.74 |
| Non-anchor coupling (mean) | -0.33 |
| Top quartile threshold | -0.22 |
| Anchors in top quartile | 4/5 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.0043 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 248 | Y | 1 | 8.61 | YES |
| 95 | G | 2 | 0.75 | YES |
| 93 | L | 9 | 0.09 | YES |
| 99 | G | 3 | -0.14 | YES |
| 82 | V | 1 | -0.59 |  |
