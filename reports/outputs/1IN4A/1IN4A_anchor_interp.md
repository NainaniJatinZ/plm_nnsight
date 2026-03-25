# Anchor Residue Interpretation: 1IN4A

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 1IN4A |
| Contact pair | (55, 174) |
| ss1 | [50, 61) |
| ss2 | [169, 180) |
| Clean flank | 40 |
| Corrupt flank | 39 |
| Jump residues | [10, 100, 129, 219] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 29 | Q | flkL | K(1) | 1 | 0.858 | C | - |  |  |
| 55 | L | ss1 | K(1) | 1 | 0.679 | E | interior | 4 |  |
| 62 | G | flkL | K(1)+Q(1) | 2 | 0.986 | C | - |  |  |
| 106 | F | other | K(2)+Q(1) | 3 | 0.585 | E | interior | 5 |  |
| 107 | I | other | K(2) | 2 | 0.654 | E | interior | 5 |  |
| 150 | F | flkR | Q(1) | 1 | 0.440 | C | - |  |  |
| 170 | F | ss2 | Q(1) | 1 | 0.512 | C | - |  |  |
| 173 | I | ss2 | Q(1) | 1 | 0.564 | E | interior | 4 |  |
| 174 | L | ss2 | K(1) | 1 | 0.424 | E | interior | 4 |  |
| 180 | T | flkR | K(1) | 1 | 0.281 | C | - |  |  |
| 184 | L | flkR | K(1) | 1 | 0.528 | H | interior | 14 |  |
| 213 | G | flkR | K(1) | 1 | 0.899 | C | - |  |  |
| 214 | T | flkR | Q(1) | 1 | 0.514 | C | - |  |  |
| 218 | A | flkR | K(11)+Q(1) | 12 | 0.583 | H | interior | 18 |  |

## Head Assignments per Anchor

### Position 29 (Q) — K(1)

K anchor for: L4H8(r7,s)

### Position 55 (L) — K(1)

K anchor for: L14H9(r8,d)

### Position 62 (G) — K(1)+Q(1)

K anchor for: L5H19(r19,s)

Q anchor for: L4H8(r7,s)

### Position 106 (F) — K(2)+Q(1)

K anchor for: L19H1(r26,d), L21H17(r30,d)

Q anchor for: L7H6(r27,d)

### Position 107 (I) — K(2)

K anchor for: L19H1(r26,d), L21H17(r30,d)

### Position 150 (F) — Q(1)

Q anchor for: L13H19(r10,s)

### Position 170 (F) — Q(1)

Q anchor for: L19H1(r26,d)

### Position 173 (I) — Q(1)

Q anchor for: L19H1(r26,d)

### Position 174 (L) — K(1)

K anchor for: L16H18(r12,s)

### Position 180 (T) — K(1)

K anchor for: L20H5(r18,s)

### Position 184 (L) — K(1)

K anchor for: L20H1(r21,d)

### Position 213 (G) — K(1)

K anchor for: L19H9(r28,d)

### Position 214 (T) — Q(1)

Q anchor for: L17H19(r9,s)

### Position 218 (A) — K(11)+Q(1)

K anchor for: L13H8(r3,s), L13H12(r4,s), L14H9(r8,d), L17H19(r9,s), L13H19(r10,s), L16H7(r13,s), L20H1(r21,d), L17H3(r23,s), L15H4(r24,s), L19H9(r28,d), L15H2(r29,s)

Q anchor for: L7H6(r27,d)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 14 |
| K-only anchors | 7 |
| Q-only anchors | 4 |
| Both K and Q | 3 |
| Jump residues among anchors | 0 |
| SSE breakdown | H=2, E=5, C=7 |
| Region breakdown | flkL=2, flkR=6, other=2, ss1=1, ss2=3 |
| SSE position | interior=7 |
| Conservation (mean) | 0.608 |
| Conservation (range) | [0.281, 0.986] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (55, 174) |
| Total flank residues | 160 |
| Flank anchors | 8 |
| Flank non-anchors | 152 |
| Anchor coupling (mean) | -1.16 |
| Non-anchor coupling (mean) | -0.87 |
| Top quartile threshold | -0.61 |
| Anchors in top quartile | 3/8 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.5239 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 29 | Q | 1 | 0.32 | YES |
| 62 | G | 2 | -0.18 | YES |
| 213 | G | 1 | -0.36 | YES |
| 184 | L | 1 | -0.87 |  |
| 214 | T | 1 | -0.92 |  |
| 180 | T | 1 | -2.00 |  |
| 218 | A | 12 | -2.26 |  |
| 150 | F | 1 | -3.03 |  |
