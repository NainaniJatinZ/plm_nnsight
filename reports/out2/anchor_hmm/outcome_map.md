# Outcome Map

## Experiment 1

- `H_anchor < H_random_in_domain` and below both matched controls in most Pfams:
  genuine domain-coordinate signal beyond burial/SSE.
- `H_anchor < H_random_in_domain` but approximately equals buried/SSE-matched:
  structural-feature / burial-class explanation.
- `H_anchor ≈ H_random_in_domain`:
  no strong Pfam-coordinate alignment.

## Experiment 2

- `|Δα_norm(C7)|` exceeds `C4/C5/C8`:
  high-IC amino-acid identities inside the local window matter.
- `C7 ≈ C4` or `C7 ≈ C5`:
  class-level structural feature explanation.
- `C7 ≈ C8`:
  no privileged role for high-IC residues.
- `C_anchor` should collapse the anchor signal; `C_far` should leave it close to baseline.

## Experiment 3

- `R_3Di` tracks structural labels and outperforms `R_AA`:
  structural-window signature supports the structural-feature story.
- both fail:
  window token information is insufficient.
- `R_AA` tracks Pfam strongly:
  amino-acid motif story resurfaces.
- `L_col` recovery in the 1PVGA / 2B61A homolog sets:
  consistency check with the prior structure-transfer result.
