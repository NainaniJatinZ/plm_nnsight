# Anchor Residue Interpretation: 2B61A

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 2B61A |
| Contact pair | (182, 316) |
| ss1 | [177, 188) |
| ss2 | [311, 322) |
| Clean flank | 44 |
| Corrupt flank | 43 |
| Jump residues | [133, 231, 267, 365] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 133 | I | flkL | K(2) | 2 | 0.404 | C | - |  | YES |
| 157 | I | flkL | K(2)+Q(1) | 3 | 0.565 | E | interior | 5 |  |
| 159 | G | flkL | K(1) | 1 | 0.985 | E | interior | 5 |  |
| 163 | G | flkL | K(4) | 4 | 0.978 | H | interior | 12 |  |
| 180 | N | ss1 | K(1) | 1 | 0.285 | E | boundary | 5 |  |
| 181 | I | ss1 | K(3)+Q(9) | 12 | 0.391 | E | interior | 5 |  |
| 183 | N | ss1 | K(1)+Q(2) | 3 | 0.392 | E | interior | 5 |  |
| 315 | T | ss2 | K(5)+Q(6) | 11 | 0.460 | E | interior | 7 |  |
| 316 | L | ss2 | Q(1) | 1 | 0.471 | E | interior | 7 |  |
| 326 | K | flkR | K(1) | 1 | 0.495 | C | - |  |  |
| 337 | L | flkR | K(1) | 1 | 0.503 | H | interior | 13 |  |
| 344 | L | flkR | K(1) | 1 | 0.367 | E | boundary | 6 |  |
| 355 | H | flkR | K(1) | 1 | 0.958 | H | interior | 7 |  |
| 365 | F | flkR | K(3) | 3 | 0.303 | H | interior | 13 | YES |

## Head Assignments per Anchor

### Position 133 (I) — K(2)

K anchor for: L0H7(r11,d), L0H6(r18,d)

### Position 157 (I) — K(2)+Q(1)

K anchor for: L11H16(r17,d), L17H18(r21,d)

Q anchor for: L8H12(r29,d)

### Position 159 (G) — K(1)

K anchor for: L5H19(r14,s)

### Position 163 (G) — K(4)

K anchor for: L11H1(r2,s), L16H17(r23,s), L15H2(r24,s), L9H1(r25,s)

### Position 180 (N) — K(1)

K anchor for: L32H18(r12,d)

### Position 181 (I) — K(3)+Q(9)

K anchor for: L7H16(r9,d), L6H19(r10,s), L32H18(r12,d)

Q anchor for: L11H1(r2,s), L10H9(r4,d), L14H9(r13,s), L5H19(r14,s), L17H18(r21,d), L14H14(r22,s), L16H17(r23,s), L15H2(r24,d), L8H12(r29,d)

### Position 183 (N) — K(1)+Q(2)

K anchor for: L17H18(r21,d)

Q anchor for: L19H0(r20,s), L15H2(r24,d)

### Position 315 (T) — K(5)+Q(6)

K anchor for: L10H9(r4,s), L14H9(r13,s), L11H16(r17,d), L8H12(r29,s), L13H8(r30,s)

Q anchor for: L6H3(r3,s), L10H9(r4,d), L8H19(r7,s), L7H16(r9,s), L6H19(r10,s), L6H8(r26,s)

### Position 316 (L) — Q(1)

Q anchor for: L17H18(r21,d)

### Position 326 (K) — K(1)

K anchor for: L6H8(r26,s)

### Position 337 (L) — K(1)

K anchor for: L8H19(r7,s)

### Position 344 (L) — K(1)

K anchor for: L7H16(r9,d)

### Position 355 (H) — K(1)

K anchor for: L6H3(r3,s)

### Position 365 (F) — K(3)

K anchor for: L0H7(r11,d), L0H6(r18,d), L1H13(r28,s)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 14 |
| K-only anchors | 9 |
| Q-only anchors | 1 |
| Both K and Q | 4 |
| Jump residues among anchors | 2 |
| SSE breakdown | H=4, E=8, C=2 |
| Region breakdown | flkL=4, flkR=5, ss1=3, ss2=2 |
| SSE position | boundary=2, interior=10 |
| Conservation (mean) | 0.540 |
| Conservation (range) | [0.285, 0.985] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (182, 316) |
| Total flank residues | 176 |
| Flank anchors | 9 |
| Flank non-anchors | 167 |
| Anchor coupling (mean) | -0.25 |
| Non-anchor coupling (mean) | -1.54 |
| Top quartile threshold | -1.42 |
| Anchors in top quartile | 4/9 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.1077 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 337 | L | 1 | 6.03 | YES |
| 344 | L | 1 | 3.44 | YES |
| 326 | K | 1 | -0.11 | YES |
| 133 | I | 2 | -1.42 | YES |
| 365 | F | 3 | -1.85 |  |
| 157 | I | 3 | -1.89 |  |
| 355 | H | 1 | -2.02 |  |
| 159 | G | 1 | -2.06 |  |
| 163 | G | 4 | -2.34 |  |
