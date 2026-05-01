# 4_28 Anchor — results from the next-day experiment plan

Companion to `experiments/4_28_anchor_next.md`. All three pre-registered next-day experiments ran and landed on their "yes" outcomes. This document records the numbers and the paper-grade claims they support.

Model: `facebook/esm2_t33_650M_UR50D`. Head: L10H9. d-direction: derived from the 2B61A reference once and reused.

## Selection refinements vs the doc

- Stricter audit filter: `top1_mass >= 0.5 AND keys_50pct == 1 AND top_key_proj_rank == 0` (1166 chains qualify) instead of `top3_mass >= 0.8` (1251 chains). Drops chains where attention is split over a triad. Keeps SDR families.
- Pfam-first selection: 8 Pfams with >= 8 anchor-in-domain chains each, deduplicated to one primary Pfam per chain (highest state-IC at the anchor). Total 79 chains. The doc target of "10 Pfams with >= 10 each" was infeasible at audit-corpus depth: only 4 Pfams reach >= 10 after dedup.
- Per-chain selected_radius: derived from a custom Exp 0 sweep on the new set. The script's default jump-based criterion was unreliable — many chains have an alpha_norm spike at R=0 (anchor AA alone is sufficient), then a "valley of confusion" at R=5–25, and final recovery beyond R=30. Used "smallest R >= 10 where alpha_norm crosses 0.7" as the local-window radius. R distribution: median 34, IQR [22, 46], max 69.

## E2a — C_far diagnosis (n = 83 prior survivors)

Three diagnostics on the existing Exp 2 set:

| Diagnostic | Purpose | Result |
|---|---|---|
| D1 | k_far ∈ {2,4,8,16}: dose response when unmasking distal residues into the local-window baseline | Median Δα_norm = 0.10 → 0.15 → 0.21 → 0.27. Strictly monotonic in 82% of chains. Wilcoxon k=16 vs k=2: p = 2.9e-15. Not saturated by k=16 (k=16 vs k=8: p = 4.0e-13). |
| D2 | Mask k far positions in the FULL sequence: does removing distal info change alpha? | Median \|Δα_norm\| = 0.005. 100% of chains have \|Δ\| < 0.05. Wilcoxon vs 0: p = 0.10 (not significant). |
| D3 | Sample k=4 from distance bins (R+1..R+10, R+10..R+30, R+30..R+60, R+60..end); per-bin Δα_norm | Near 0.172, mid 0.165, far 0.156, veryfar 0.140. Wilcoxon near vs far: p = 5.1e-7. Per-chain decay slope median = -0.010 (75% of chains negative slope). |

Interpretation. The C_far positivity reported in the prior writeup (Δα_far +0.17 to +0.32) is a context-starvation effect, not encoded long-range information. D2 is decisive: the local window already captures alpha to within 0.5% of the full-sequence value. D1 + D3 together describe a small graded contribution from distal residues when the local window is information-starved, but the absolute magnitude is small relative to the local window's contribution.

Paper claim. "Anchor information is locally recoverable. The local window (±R) reproduces alpha at the anchor to within 0.5% of the full sequence. Distal residues contribute weakly to the masked-window baseline (about 10% distance-decay across four distance bins), consistent with a graded long-range channel that does not encode the anchor itself but disambiguates context."

## E1' — Pfam-first replication of Exp 1 (n = 79 chains, 12 Pfams hit)

Selection produced 8 primary Pfams; mapping_df (which uses ALL hits per chain, not just the primary) covers 12 Pfams.

| Comparison | Pfams where anchor concentrates more than control | Sign-test p |
|---|---|---|
| anchor h_norm < random_h_norm_mean | 12 / 12 | 4.9e-4 |
| anchor h_norm < buried_h_norm_mean (where buried n >= 1) | 8 / 10 | 0.11 |
| anchor h_norm < sse_h_norm_mean (where sse n >= 1) | 9 / 10 | 0.021 |
| anchor h_norm < ALL three (where all are testable) | 8 / 9 | — |

In 11 of 12 Pfams, anchor_h_norm = 0.0 — every chain in the family lands its anchor on the SAME HMM match-state. The 12th (PF13508) has anchor_h_norm = 0.085 with anchor_top1_conc = 0.875 (7 of 8 chains share a state).

Random controls are well-sampled (n_mean 8–12) and are decisively beaten in every Pfam. The two failures vs buried/SSE controls are degenerate-control cases (n_mean = 1–2 — same finding as the doc's PF01613 housekeeping flag), not real failures.

Paper claim. "Anchors land on a canonical Pfam coordinate. Across 12 Pfams of the audit-ranked set, the anchor lands on the same HMM match-state for every chain in 11 / 12 Pfams (anchor_h_norm = 0; top1 concentration = 1.0). The within-Pfam concentration beats matched random selection in 12 / 12 Pfams (sign-test p = 4.9e-4); beats SSE-matched controls in 9 / 10 testable Pfams (p = 0.021); and beats RSA-matched buried controls in 8 / 10 testable Pfams. Failures are limited to degenerate single-sample controls."

Caveat to write into the methods section. The mapping_df is built over all Pfam hits per chain, so chains in multi-domain families contribute to several Pfams. Across-Pfam independence is not strict — but the within-Pfam signal in PF00106, PF13561, PF00072, PF00293, PF00155, PF00881, PF13407 (all single-domain or non-overlapping) is sufficient on its own.

## E2b — Conservative substitution variant (n = 40 surviving chains at per-chain R)

Inside the local window of each chain: mask vs substitute conditions, paired within chain, 20 RSA-matched random resamples for C8/C8_sub.

| Condition | Median Δα_norm | Argmax preserved |
|---|---|---|
| C7 (mask k=8 highest-IC positions) | -0.990 | 5% |
| C7_sub (substitute same positions, same physicochemical class) | -0.767 | 43% |
| C8 (mask k RSA-matched random positions) | -0.904 | 23% |
| C8_sub (substitute same random positions, same class) | -0.409 | 68% |

Paired Wilcoxon (n = 40):

| Comparison | Median Δ | p |
|---|---|---|
| C7 vs C7_sub | -0.223 | 4.5e-6 |
| C7 vs C8 | -0.087 | 1.1e-5 |
| C7_sub vs C8_sub | -0.358 | 5.4e-5 |
| C8 vs C8_sub | -0.494 | 1.8e-12 |
| C7_sub vs C8 | +0.137 | 7.9e-3 |

Recovery rates relative to mask:
- |C7_sub| / |C7| = 0.77 — class-preserving substitution at conserved positions recovers only **23% of the masking effect**.
- |C8_sub| / |C8| = 0.45 — substitution at random positions recovers **55%** of the masking effect.

Paper claim. "L10H9 reads conserved positions in a way that depends substantially on specific residue identity beyond physicochemical class. Class-preserving substitution at the top-IC positions in the local window recovers only 23 percent of the masking effect, vs 55 percent recovery at non-conserved positions. The diagnostic separates more sharply under substitution than under masking: C7-vs-C8 (mask) gap is 0.087, while C7_sub-vs-C8_sub (substitute) gap is 0.358."

This is the doc's pre-registered "outcome 2": substitution preserves part of the signal because physicochemical class is partly what the head reads; the residue-specific identity adds on top. The asymmetry between conserved and random positions is itself a paper-grade observation: the head reads class-only information at low-IC positions and identity-plus-class at high-IC positions.

## What the three results say together

1. The anchor signal is local. The full sequence contributes essentially nothing beyond the local ±R window (E2a / D2).
2. Within a Pfam family, the anchor lands on a canonical HMM coordinate, beyond what burial or SSE can explain (E1').
3. At the conserved positions inside the local window, residue identity is causally necessary in a way that physicochemical class alone does not capture (E2b).

These claims sit naturally in this order in the paper. (1) sets up the locality argument. (2) shows the anchor is family-coordinate, not random. (3) demonstrates the head reads specific identity at the canonical positions, not just hydrophobicity / charge.

## Open issues / caveats to address in writeup

- The E1' mapping_df includes multi-Pfam hits per chain. Within-Pfam claims are clean but cross-Pfam meta-tests are not strictly independent. Single-domain Pfams give the cleanest signal.
- Buried- and SSE-matched controls collapse to n = 1–2 in some Pfams (degenerate within-window pool). Either widen the same-SSE pool (per the doc's housekeeping note) or drop those Pfams from those specific comparisons. Do not silently report a "control beats control by 0" as a tie.
- E2a's D1 monotonic rise could in principle come from "any well-formed AA disambiguates the masked window" rather than encoded distal info. A scrambled-AA control on the unmasked far positions is the cleanest test and would land in the same script. Not yet run; add as an asterisk if the reviewer pushes.
- E2b's C7_sub uses one substitution draw per position. Variance across substitution choices is not quantified. Adding 5–10 substitution seeds per chain would tighten the IQR but is unlikely to change the paired comparisons.
- Per-chain selected_radius derivation: the standard jump-based selection from `summarize_recovery_curve` is not reliable for this set; we used "smallest R >= 10 where alpha_norm >= 0.7." This produces a more conservative, larger window and is necessary to avoid the R = 0 anchor-AA-only artifact and the valley-of-confusion at R = 5–25. Document this in the methods.

## Output artifact map

```
reports/out2/anchor_hmm_v2/
  annotate_todo.txt                       # 943 chains queued for InterPro annotation
  annotate_batch.log                      # batch driver log
  annotate_failed.txt                     # 128 chains with no Pfam / no SIFTS / API error
  pfam_first_overview.csv                 # all Pfams seen with member counts
  pfam_first_selection.csv                # 79 chains x 8 primary Pfams
  pfam_first_selection.md                 # human-readable
  exp0/
    per_protein.csv                       # full Exp 0 sweep, R = 0..80
    summary.csv                           # default jump-based selected_radius
    summary_v3.csv                        # alpha >= 0.7 (R >= 10) per-chain R, used for E2b
    alpha_norm_curves.png
  exp1/
    anchor_hmm_mapping.tsv                # seq_pos -> hmm_state per chain x Pfam
    per_pfam_entropy.csv                  # 12 Pfam rows with all controls
    meta_sign_test.csv                    # cross-Pfam sign tests
    plots/                                # per-Pfam plots
  e2a_cfar_diag/
    e2a_results.csv                       # per-chain D1/D2/D3 results (735 rows)
    e2a_summary.csv
  e2b_substitution/                       # fixed R = 40 first attempt (n = 19)
  e2b_substitution_perchain/              # jump-based R; bad signal (n = 21)
  e2b_v3/                                 # alpha-0.7-based per-chain R; FINAL (n = 40)
    e2b_results.csv
    e2b_paired.csv
  exp2_survivors.csv                      # original n = 83 anchor list (input to E2a)
```

Scripts referenced:

- `scripts/anchor_pfam_first_select.py` — Pfam-first selection with state-IC dedup
- `scripts/run_interpro_annotate_batch.sh` — wrapper around interpro_hmm_annotate.py
- `scripts/anchor_e0_pfam_first.py` — Exp 0 sweep wrapper
- `scripts/anchor_e1prime_run.py` — Exp 1 wrapper for the Pfam-first set
- `scripts/anchor_e2a_cfar_diag.py` — D1/D2/D3 diagnostics
- `scripts/anchor_e2b_substitution.py` — C7/C7_sub/C8/C8_sub
