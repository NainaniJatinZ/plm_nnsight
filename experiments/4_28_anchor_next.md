# 4_28 Anchor — defensible claims and next-day experiment plan

Goal of this doc: lock down what the 4_26 runs actually established, and define a tightly-scoped next-day experiment set that is designed to (a) generalize Exp 1, (b) close the C_far loophole in Exp 2, and (c) discriminate identity-encoding from generic-disruption at conserved positions. The output of these runs is meant to go directly into the paper draft.

Model: facebook/esm2_t33_650M_UR50D throughout. Selection from `anchor_behavior_audit.csv` (top3_mass ≥ 0.8). No 3B sweep dependency.

## What we can already defend (from 4_26 runs)

1. The anchor signal is locally recoverable. Exp 0, n=200, sweep R=0..80 step 1: median selected_radius = 30, IQR [21, 38]. 195/200 reach α_norm ≥ 0.5 by R=80. The information sufficient to reproduce the anchor projection lives within a ±30 (median) residue window.

2. Inside the local window, conserved AA identity is causally necessary. Exp 2, paired masking inside per-protein selected_radius window, n=83 survivors of the baseline guard:
   - C7 (high-IC) vs C4 (buried-low-IC): Wilcoxon p = 1.6e-12, median Δ = −0.30
   - C7 vs C5 (exposed-low-IC):           p = 1.6e-13, median Δ = −0.45
   - C7 vs C8 (RSA-matched random):       p = 5e-4,    median Δ = −0.04
   argmax-preserved: C0 100%, C_far 100%, C_anchor 40%, C4 40%, C5 20%, C8 2%, C7 0%. Burial alone, SSE alone, and RSA-matched random selection do not explain the loss; identity at conserved positions does.

3. AA windows around the anchor do not separate proteins; 3Di windows do. Exp 3, n=200, ±15 windows:
   - AA NMI vs L_Pfam, L_struct, L_col: 0, 0, 0
   - 3Di NMI vs same: 0.33, 0.31, 0.23
   - 3Di LOO k-NN on L_col: 0.83 (recovers the structural-column equivalence claim from the prior 1PVGA / 2B61A homolog work)
   The earlier P50 AA-NMI = 0.31 was a 3B-selection artifact and disappears under audit-ranked P200.

Combined story for the draft: the L10H9 anchor reads a local structural motif from sequence. The motif is structurally-coherent (3Di-clusterable across families) but is enforced by a small subset of conserved AA positions whose identity is causally necessary. AA windows as a whole do not cluster — most positions are free; only the high-IC subset constrains the geometry.

## What we cannot yet claim, and why each next-day experiment exists

| Claim we want | Why current data can't support it | Targeted next-day experiment |
|---|---|---|
| Anchors hit a canonical Pfam HMM coordinate within and across families | Exp 1 had only 1 qualifying Pfam in P200 (sign_test_p=1.0). Audit-ranked selection scatters across folds. | E1' — Pfam-first selection |
| Anchor information is local (not distal) | C_far positivity (+0.17 to +0.32 in Δα_norm on n=5) means distal unmask reproducibly nudges α up. Could be real long-range dependency or window-construction leak. | E2a — C_far diagnosis |
| Conserved AA *identity* matters, not generic disruption | C7 mask removes both identity and presence. Conservative substitution would test identity specifically. | E2b — conservative-substitution variant |

## Pre-registered outcome maps

For each next-day experiment, both outcomes lead to a defensible paper claim. None of them are vague.

### E1' — Pfam-first selection, rerun Exp 1 / Exp 2 / Exp 3

Selection: from `anchor_behavior_audit.csv` filtered top3_mass ≥ 0.8 AND d_argmax == top_key_idx (so anchor identity is unambiguous), pick the 8–10 Pfams with the most members that pass both filters. From each Pfam, sample 12–15 chains. Target N ≈ 100–150, Pfams ≥ 8, n_per_Pfam ≥ 10.

Verification before running: for each chosen Pfam print n_eligible, anchor-in-domain count, RSA/SSE coverage. Cancel and re-pick if any Pfam has < 8 anchor-in-domain after filtering.

Exp 1 readouts unchanged: per-Pfam h_norm for anchor + 3 matched controls (random, RSA-matched ±0.10, SSE-matched). Meta sign-test across Pfams.

Pre-registered outcomes:
- ≥ 6 / 8 Pfams: anchor h_norm < all three control h_norms → defensible claim "anchors land on canonical Pfam coordinates beyond what burial or SSE alone explain", sign_test_p ≤ 0.035 at 6/8.
- Anchor h_norm beats random but only ties burial OR SSE control in most Pfams → defensible claim "anchors prefer burial/SSE-class positions; canonical-coordinate-beyond-burial signal is family-dependent". List the families where it survives vs fails — this is itself paper material.
- Anchor h_norm ≈ random across Pfams → walk back the canonical-coordinate claim entirely; rely on Exp 2 + Exp 3 only. Acceptable, pre-registered negative.

Exp 2 and Exp 3 reruns on the same Pfam-first set are cheap and act as replications of the existing claims with a non-confounded selection. Report Wilcoxon p and 3Di NMI on the new set; these should reproduce within an order of magnitude. If they don't, the prior result was selection-driven and we need to know.

### E2a — C_far positivity diagnosis (no new infra)

Run on the existing n=83 Exp 2 survivors. Goal: decide if the +0.17 to +0.32 distal nudge is real or a build_local_window_sequence artifact.

Three diagnostics, each cheap:
1. Vary k_far ∈ {2, 4, 8, 16}. If Δα_far scales monotonically with k_far, the effect is dose-dependent → real distal contribution. If saturates or is flat, likely an artifact of unmasking *anything* far.
2. Replace C_far residues with `<mask>` instead of unmasking (so the manipulation is "remove distal info" instead of "add distal info"). Should give Δα ≈ 0 if the local window is sufficient. Non-zero → genuine distal signal.
3. Plot Δα_far vs selected_radius and vs distance-to-anchor of the unmasked residues. If Δα_far decays with distance, there's a graded long-range channel; if it's flat, it's likely a window-construction edge effect (e.g., BOS/EOS proximity, k-mer spillover from positional encoding).

Pre-registered outcomes:
- Diagnostic 1 monotonic AND diagnostic 3 distance-decaying → claim "anchor is locally dominated but receives a graded long-range contribution"; quantify it and add to the local-sufficiency paragraph as a caveat. This is a refinement, not a retraction.
- Diagnostic 2 zero AND diagnostic 1 flat → artifact; document the cause and remove C_far from Exp 2 reporting.
- Mixed → flag as unresolved in the writeup; do not claim local sufficiency without qualification.

### E2b — Conservative substitution variant of Exp 2

For each protein in the Pfam-first set, run two new conditions inside the per-protein local window:
- C7_sub: substitute the same k high-IC residues with a conservative AA from the same physicochemical class (use the C3 substitution table from `experiments/4_6_scramble_experiment.md`).
- C8_sub: substitute the same k RSA-matched random residues with conservative AAs.

Same readouts as Exp 2: Δα_norm and argmax-preserved. Paired within protein.

Pre-registered outcomes:
- |Δα_norm(C7_sub)| ≈ |Δα_norm(C7_mask)| (within 25%) → identity-of-class is not what matters; specific residue identity is necessary. Strong claim for the paper.
- |Δα_norm(C7_sub)| substantially less than |Δα_norm(C7_mask)| but still > |Δα_norm(C8_sub)| → conservative substitution preserves part of the signal because physicochemical class is partly what the head reads; the residue-specific identity adds on top. Reasonable claim.
- |Δα_norm(C7_sub)| ≈ |Δα_norm(C8_sub)| ≈ 0 → high-IC residues are tolerant of conservative replacement; the original C7 mask was destroying signal by removing presence, not identity. This walks back the "identity is necessary" claim to "presence at conserved positions is necessary"; still a real result but framed differently.

This is the experiment most likely to sharpen the paper claim. Pre-commit to which outcome lands in the abstract before opening the CSV.

## Execution checklist for tomorrow

1. Run `select_p50` variant in Pfam-first mode → save the chosen chain list and Pfam table to `reports/out2/anchor_hmm_v2/selection.csv`. Sanity-check counts before any inference.
2. Rerun Exp 0 step=1 sweep on the new set (max_flank=80). Save selected_radius per chain.
3. Run E1' with the new set. This is the headline question.
4. Run E2b (conservative substitution) on the same set, reusing the per-protein local windows from step 2. Cheap if the existing Exp 2 pipeline takes a substitution table as a parameter.
5. Run E2a diagnostics on the existing n=83 set in parallel (independent compute).
6. Rerun Exp 3 clustering on the new set as a replication of NMI 3Di > AA. Should be cheap.

Outputs land under `reports/out2/anchor_hmm_v2/`. Pre-register the outcome maps above into a header in each results CSV before opening it.

## What goes into the paper if these run cleanly

Best case (all pre-registered "strong" outcomes hit):
- Anchor is locally recoverable (median R≈30 over n≈150).
- Within-Pfam canonical coordinate signal: ≥ 6/8 Pfams beat all three matched controls.
- Conserved-AA identity (not just presence) is causally necessary: C7_sub ≈ C7_mask, both ≫ matched controls.
- AA windows uninformative across families; 3Di windows recover Pfam, structural cluster, and homolog column equivalence (k-NN ≈ 0.83 reproduced).
- C_far either dose-dependent and distance-decaying (graded long-range contribution, quantified) or shown artifactual.

Worst plausible case (mixed outcomes):
- Local recoverability stands.
- Within-Pfam claim drops to "family-dependent canonical coordinate, beats random in all qualifying Pfams but ties burial control in some". List which.
- Identity claim drops to "presence at conserved positions necessary; partial conservative-substitution recovery suggests physicochemical-class encoding".
- 3Di clustering claim stands.

Both cases give us multiple defensible sentences for the draft. The key design choice is that *every* pre-registered outcome leads to a writeable claim, not to "result was unclear."

## House cleaning to do alongside

- Drop r50_first_crossing from outputs (R=0 artifact).
- Drop `derive_selected_radius_for_condition` in Exp 2 (~3x unused cost).
- Cache DSSP RSA across Exp 1 invocations.
- For the SSE-matched control: when the in-window same-SSE pool is degenerate (PF01613 case), report n_candidates per protein and either widen to "same SSE class within ±k of anchor" or skip that control for that protein with a documented flag — do not silently collapse to a single deterministic state.
- In Exp 3 labels.csv, wire in the 1PVGA / 2B61A homolog augmentation — the L_col k-NN result currently rides on those groups even though they're not flagged in source.
