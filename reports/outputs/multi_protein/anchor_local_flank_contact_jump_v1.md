# Anchor Local Flank Jump Contact Analysis

Uses the projection jump pair from `anchor_local_flank_v1_per_protein.csv`.
For each protein, evaluates contact precision only on residue pairs where both residues are visible in the flank window.

Proteins scored: 27
Skipped (no PDB contacts): 23
Skipped (no jump pair): 0

## Median visible-subset precision

| Window | Radius | P@L/5 | P@L/2 | P@L |
|--------|--------|-------|--------|-----|
| jump_from | 20.0 | 0.0000 | 0.0250 | 0.0204 |
| jump_to | 30.0 | 0.5000 | 0.2333 | 0.1570 |

## Median change from jump_from to jump_to

- Delta P@L/5: 0.3333
- Delta P@L/2: 0.2000
- Delta P@L: 0.1447

## Median masked-vs-full gap on the same visible subset

- jump_from delta P@L/5: -0.2500
- jump_from delta P@L/2: -0.1000
- jump_from delta P@L: -0.0488
- jump_to delta P@L/5: 0.0000
- jump_to delta P@L/2: -0.0167
- jump_to delta P@L: 0.0000
