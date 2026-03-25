# Anchor Residue Interpretation: 2FBQA

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 2FBQA |
| Contact pair | (94, 201) |
| ss1 | [89, 100) |
| ss2 | [196, 207) |
| Clean flank | 61 |
| Corrupt flank | 60 |
| Jump residues | [28, 135, 160, 267] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 28 | S | flkL | Q(1) | 1 | 0.495 | C | - |  | YES |
| 32 | I | flkL | K(1) | 1 | 0.677 | H | interior | 8 |  |
| 37 | G | flkL | K(2)+Q(1) | 3 | 0.652 | C | - |  |  |
| 43 | V | flkL | K(3) | 3 | 0.478 | H | interior | 7 |  |
| 47 | F | flkL | K(3) | 3 | 0.806 | C | - |  |  |
| 94 | L | ss1 | Q(1) | 1 | 0.215 | H | interior | 14 |  |
| 99 | M | ss1 | K(1) | 1 | 0.203 | H | interior | 14 |  |
| 111 | I | flkL | K(1) | 1 | 0.093 | H | interior | 13 |  |
| 168 | A | flkR | K(1) | 1 | 0.231 | H | interior | 20 |  |
| 169 | A | flkR | K(1) | 1 | 0.164 | H | interior | 20 |  |
| 173 | M | flkR | K(3)+Q(1) | 4 | 0.193 | H | interior | 20 |  |
| 174 | S | flkR | Q(1) | 1 | 0.166 | H | boundary | 20 |  |
| 185 | T | flkR | K(1) | 1 | 0.533 | H | interior | 12 |  |
| 197 | M | ss2 | K(1)+Q(1) | 2 | 0.238 | H | interior | 17 |  |
| 198 | H | ss2 | Q(2) | 2 | 0.249 | H | interior | 17 |  |
| 201 | V | ss2 | K(1)+Q(1) | 2 | 0.220 | H | interior | 17 |  |
| 204 | F | ss2 | Q(1) | 1 | 0.334 | H | interior | 17 |  |

## Head Assignments per Anchor

### Position 28 (S) — Q(1)

Q anchor for: L0H14(r1,s)

### Position 32 (I) — K(1)

K anchor for: L6H4(r6,s)

### Position 37 (G) — K(2)+Q(1)

K anchor for: L7H10(r2,s), L6H19(r9,s)

Q anchor for: L6H4(r6,s)

### Position 43 (V) — K(3)

K anchor for: L18H16(r11,s), L17H14(r19,s), L19H9(r26,d)

### Position 47 (F) — K(3)

K anchor for: L11H16(r7,s), L10H14(r12,s), L8H13(r29,s)

### Position 94 (L) — Q(1)

Q anchor for: L22H10(r28,s)

### Position 99 (M) — K(1)

K anchor for: L30H13(r23,d)

### Position 111 (I) — K(1)

K anchor for: L22H10(r28,s)

### Position 168 (A) — K(1)

K anchor for: L21H7(r17,d)

### Position 169 (A) — K(1)

K anchor for: L21H7(r17,d)

### Position 173 (M) — K(3)+Q(1)

K anchor for: L19H9(r26,d), L18H7(r27,s), L19H2(r30,s)

Q anchor for: L15H12(r8,d)

### Position 174 (S) — Q(1)

Q anchor for: L15H12(r8,d)

### Position 185 (T) — K(1)

K anchor for: L24H14(r25,s)

### Position 197 (M) — K(1)+Q(1)

K anchor for: L30H13(r23,d)

Q anchor for: L16H10(r15,d)

### Position 198 (H) — Q(2)

Q anchor for: L24H0(r20,s), L28H4(r24,s)

### Position 201 (V) — K(1)+Q(1)

K anchor for: L28H4(r24,s)

Q anchor for: L24H14(r25,s)

### Position 204 (F) — Q(1)

Q anchor for: L16H10(r15,d)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 17 |
| K-only anchors | 8 |
| Q-only anchors | 5 |
| Both K and Q | 4 |
| Jump residues among anchors | 1 |
| SSE breakdown | H=14, E=0, C=3 |
| Region breakdown | flkL=6, flkR=5, ss1=2, ss2=4 |
| SSE position | boundary=1, interior=13 |
| Conservation (mean) | 0.350 |
| Conservation (range) | [0.093, 0.806] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (94, 201) |
| Total flank residues | 185 |
| Flank anchors | 11 |
| Flank non-anchors | 174 |
| Anchor coupling (mean) | -0.57 |
| Non-anchor coupling (mean) | -0.02 |
| Top quartile threshold | 0.55 |
| Anchors in top quartile | 1/10 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.7690 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 174 | S | 1 | 0.68 | YES |
| 32 | I | 1 | -0.25 |  |
| 173 | M | 4 | -0.36 |  |
| 111 | I | 1 | -0.37 |  |
| 168 | A | 1 | -0.52 |  |
| 47 | F | 3 | -0.70 |  |
| 43 | V | 3 | -0.87 |  |
| 169 | A | 1 | -1.06 |  |
| 37 | G | 3 | -1.14 |  |
| 28 | S | 1 | -1.16 |  |
