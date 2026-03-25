# Anchor Residue Interpretation: 1YKIA

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 1YKIA |
| Contact pair | (83, 189) |
| ss1 | [78, 89) |
| ss2 | [184, 195) |
| Clean flank | 51 |
| Corrupt flank | 50 |
| Jump residues | [27, 133, 139, 245] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 27 | E | flkL | K(1)+Q(1) | 2 | 0.209 | H | interior | 12 | YES |
| 29 | I | flkL | K(2)+Q(3) | 5 | 0.470 | H | interior | 12 |  |
| 30 | K | flkL | K(1) | 1 | 0.466 | H | interior | 12 |  |
| 47 | F | flkL | K(1) | 1 | 0.510 | E | interior | 6 |  |
| 81 | V | ss1 | Q(1) | 1 | 0.196 | E | interior | 8 |  |
| 83 | F | ss1 | K(1) | 1 | 0.136 | E | interior | 8 |  |
| 127 | H | flkL | K(1) | 1 | 0.235 | H | interior | 21 |  |
| 128 | R | flkL | K(1) | 1 | 0.209 | H | interior | 21 |  |
| 129 | K | flkL | K(10)+Q(14) | 24 | 0.111 | H | interior | 21 |  |
| 130 | D | flkL | K(4)+Q(1) | 5 | 0.141 | H | boundary | 21 |  |
| 186 | V | ss2 | Q(1) | 1 | 0.284 | E | boundary | 6 |  |
| 188 | V | ss2 | Q(10) | 10 | 0.451 | E | interior | 6 |  |
| 191 | G | ss2 | K(1) | 1 | 0.938 | E | boundary | 6 |  |

## Head Assignments per Anchor

### Position 27 (E) — K(1)+Q(1)

K anchor for: L0H1(r20,s)

Q anchor for: L0H11(r2,s)

### Position 29 (I) — K(2)+Q(3)

K anchor for: L5H13(r3,s), L2H11(r19,s)

Q anchor for: L3H14(r16,s), L2H11(r19,s), L2H9(r28,s)

### Position 30 (K) — K(1)

K anchor for: L2H9(r28,s)

### Position 47 (F) — K(1)

K anchor for: L6H0(r4,s)

### Position 81 (V) — Q(1)

Q anchor for: L13H18(r26,d)

### Position 83 (F) — K(1)

K anchor for: L32H18(r24,s)

### Position 127 (H) — K(1)

K anchor for: L12H9(r18,d)

### Position 128 (R) — K(1)

K anchor for: L12H9(r18,d)

### Position 129 (K) — K(10)+Q(14)

K anchor for: L13H14(r1,s), L11H9(r5,d), L16H7(r7,s), L14H1(r8,s), L13H15(r9,s), L11H16(r11,d), L11H4(r15,d), L17H6(r17,s), L18H3(r25,d), L13H18(r26,s)

Q anchor for: L5H13(r3,s), L6H0(r4,s), L11H9(r5,s), L11H17(r6,s), L12H16(r10,s), L11H11(r12,s), L4H3(r13,s), L9H4(r14,s), L12H9(r18,s), L0H1(r20,d), L12H17(r21,s), L9H14(r22,s), L12H8(r23,s), L7H15(r29,s)

### Position 130 (D) — K(4)+Q(1)

K anchor for: L11H9(r5,d), L11H16(r11,d), L11H4(r15,d), L18H3(r25,d)

Q anchor for: L0H1(r20,d)

### Position 186 (V) — Q(1)

Q anchor for: L32H18(r24,d)

### Position 188 (V) — Q(10)

Q anchor for: L13H14(r1,s), L16H7(r7,s), L14H1(r8,s), L13H15(r9,s), L11H4(r15,s), L17H6(r17,s), L32H18(r24,d), L18H3(r25,s), L13H18(r26,d), L13H9(r30,s)

### Position 191 (G) — K(1)

K anchor for: L13H9(r30,s)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 13 |
| K-only anchors | 6 |
| Q-only anchors | 3 |
| Both K and Q | 4 |
| Jump residues among anchors | 1 |
| SSE breakdown | H=7, E=6, C=0 |
| Region breakdown | flkL=8, ss1=2, ss2=3 |
| SSE position | boundary=3, interior=10 |
| Conservation (mean) | 0.335 |
| Conservation (range) | [0.111, 0.938] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (83, 189) |
| Total flank residues | 168 |
| Flank anchors | 8 |
| Flank non-anchors | 160 |
| Anchor coupling (mean) | -0.17 |
| Non-anchor coupling (mean) | -0.39 |
| Top quartile threshold | -0.06 |
| Anchors in top quartile | 1/6 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.5723 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 47 | F | 1 | 4.03 | YES |
| 30 | K | 1 | -0.39 |  |
| 129 | K | 24 | -0.59 |  |
| 27 | E | 2 | -1.14 |  |
| 130 | D | 5 | -1.35 |  |
| 29 | I | 5 | -1.57 |  |
