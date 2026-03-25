# Anchor Residue Interpretation: 2EK8A

## Configuration

| Parameter | Value |
| --- | --- |
| Protein | 2EK8A |
| Contact pair | (59, 203) |
| ss1 | [54, 65) |
| ss2 | [198, 209) |
| Clean flank | 50 |
| Corrupt flank | 49 |
| Jump residues | [4, 114, 148, 258] |

## Anchor Residue Table

Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.
role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.

| pos | AA | region | role | n_heads | conservation | SSE | SSE position | seg_len | jump? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 201 | T | ss2 | Q(1) | 1 | 0.120 | E | interior | 14 |  |
| 202 | S | ss2 | Q(1) | 1 | 0.176 | E | interior | 14 |  |
| 207 | A | ss2 | K(4)+Q(3) | 7 | 0.597 | E | interior | 14 |  |
| 224 | I | flkR | K(6)+Q(3) | 9 | 0.394 | E | interior | 7 |  |
| 227 | H | flkR | K(1) | 1 | 0.904 | E | boundary | 7 |  |
| 231 | V | flkR | K(1) | 1 | 0.253 | C | - |  |  |
| 243 | G | flkR | K(5)+Q(3) | 8 | 0.742 | H | interior | 18 |  |
| 258 | K | flkR | Q(1) | 1 | 0.175 | C | - |  | YES |
| 266 | I | other | K(1) | 1 | 0.344 | E | interior | 7 |  |
| 267 | T | other | K(1) | 1 | 0.268 | E | interior | 7 |  |

## Head Assignments per Anchor

### Position 201 (T) — Q(1)

Q anchor for: L26H11(r10,d)

### Position 202 (S) — Q(1)

Q anchor for: L26H11(r10,d)

### Position 207 (A) — K(4)+Q(3)

K anchor for: L26H11(r10,s), L22H15(r14,s), L21H6(r15,s), L20H5(r27,s)

Q anchor for: L14H12(r13,s), L14H0(r20,s), L13H13(r29,s)

### Position 224 (I) — K(6)+Q(3)

K anchor for: L7H9(r1,s), L14H12(r13,s), L11H14(r16,s), L17H8(r18,s), L13H3(r26,s), L10H12(r28,s)

Q anchor for: L8H12(r11,s), L6H16(r23,s), L5H13(r24,s)

### Position 227 (H) — K(1)

K anchor for: L14H0(r20,s)

### Position 231 (V) — K(1)

K anchor for: L13H13(r29,s)

### Position 243 (G) — K(5)+Q(3)

K anchor for: L22H17(r5,s), L11H16(r7,s), L16H5(r17,s), L21H10(r19,s), L6H16(r23,s)

Q anchor for: L11H14(r16,s), L10H6(r21,s), L10H12(r28,s)

### Position 258 (K) — Q(1)

Q anchor for: L0H1(r25,s)

### Position 266 (I) — K(1)

K anchor for: L10H6(r21,d)

### Position 267 (T) — K(1)

K anchor for: L10H6(r21,d)

## Summary Statistics

| Statistic | Value |
| --- | --- |
| Total anchor residues | 10 |
| K-only anchors | 4 |
| Q-only anchors | 3 |
| Both K and Q | 3 |
| Jump residues among anchors | 1 |
| SSE breakdown | H=1, E=7, C=2 |
| Region breakdown | flkR=5, other=2, ss2=3 |
| SSE position | boundary=1, interior=7 |
| Conservation (mean) | 0.397 |
| Conservation (range) | [0.120, 0.904] |

## Coupling Analysis (flank anchors vs non-anchors)

Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.

| Parameter | Value |
| --- | --- |
| Contact pair (0-indexed) | (59, 203) |
| Total flank residues | 200 |
| Flank anchors | 5 |
| Flank non-anchors | 195 |
| Anchor coupling (mean) | -1.66 |
| Non-anchor coupling (mean) | -0.50 |
| Top quartile threshold | -0.43 |
| Anchors in top quartile | 0/5 |
| Mann-Whitney U p-value (anchor > non-anchor) | 0.9750 |

### Flank Anchor Coupling Details

| pos | AA | n_heads | max_coupling_to_contact | top quartile? |
| --- | --- | --- | --- | --- |
| 258 | K | 1 | -0.85 |  |
| 243 | G | 8 | -1.68 |  |
| 227 | H | 1 | -1.71 |  |
| 231 | V | 1 | -1.76 |  |
| 224 | I | 9 | -2.29 |  |
