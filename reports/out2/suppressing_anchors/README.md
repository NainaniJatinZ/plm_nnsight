# Suppressing Anchors

This folder is the canonical home for the anchor-suppression experiments from this conversation.
Old outputs under `reports/outputs/...` were left untouched.

## What Was Repointed

These scripts now default to writing under `reports/out2/suppressing_anchors`:

- `scripts/anchor_contact_steering.py`
  - default output: `contact_steering/{steering_mode}_top{top_k}`
- `scripts/anchor_local_flank_v1.py`
  - default output: `local_flank_v1`
- `scripts/anchor_local_flank_contact_jump_v1.py`
  - default output: `local_flank_contact_jump_v1`
- `scripts/anchor_local_flank_jump_to_steering.py`
  - default output: `local_flank_jump_to_steering/{steering_mode}`

I also copied the upstream audit CSV used by the local-flank sweep into:

- `inputs/anchor_behavior_audit.csv`

## Canonical Reruns In This Folder

These are the reruns that matter enough to keep:

1. `local_flank_v1/`
   - local reconstruction of the anchor signal as flank radius expands
2. `local_flank_contact_jump_v1/`
   - visible-subset contact precision at the projection jump pair
3. `local_flank_jump_to_steering/direct/`
   - direct suppression inside the `jump_to` window
4. `contact_steering/direct_top3/`
   - 20-protein full-sequence sweep, direct suppression, top-3 anchors
5. `contact_steering/projection_top3/`
   - 20-protein full-sequence sweep, projection suppression, top-3 anchors
6. `downstream_corruption/`
   - layer-by-layer downstream attention divergence under canonical direct/top-3 suppression
7. `qkv_decomposition/`
   - separates `ln_all`, `k_only`, `q_only`, and `v_only` interventions at layer 10
8. `attn_output_tracking/`
   - tracks the layer-10 attention residual contribution vector at anchor vs non-anchor positions
9. `jump_to_contact_pattern_bridge/`
   - for `2B61A` and `1PVGA`, compares `contact_pattern_v2`-style corrupt-head patching against masked-setup top-3 steering
10. `contact_pattern_full_vs_flank/`
   - compares the same segment-level metric in `full` and `flank` contexts for `2B61A` and `1PVGA`
11. `contact_pattern_flank_batch/`
   - runs the masked contact-pattern bridge over the remaining `contact_pattern_v2` proteins
12. `full_compensation_heads/`
   - audits which downstream heads reorganize toward the clean `L10H9` anchor pattern in `full` but not `flank`
13. `full_compensation_coablation/`
   - co-suppresses the most anchor-like compensation candidates with head-specific `k_only` interventions
14. `full_compensation_multimode/`
   - scans all anchor-like heads in layers 11-15 and co-suppresses the passing set under `k_only`, `v_only`, and `ln_all`
15. `full_compensation_multimode_with_l10h9/`
   - same multimode scan, but with `L10H9` included in the active suppression set to test the compensation story directly

I did not rerun the older top-1 branches or dated one-off folders here.

## Summary

This section is the short, corrected summary to cite in the next experiment round.
It intentionally keeps only the stable conclusions and the outputs/scripts that support them.

### 1. The core script bugs were fixed, but the scientific effect remained

- The original `OutOfOrderError` and plotting bug in `scripts/anchor_contact_steering.py` were real implementation bugs and were fixed there.
- After those fixes, the main scientific pattern still remained in the reruns under `contact_steering/`.

Cite:
- code: `scripts/anchor_contact_steering.py`
- results: `contact_steering/direct_top3/anchor_contact_steering_summary.json`

### 2. Full-sequence top-3 suppression clearly changes L10H9, but contacts are robust until larger alpha

- The canonical 20-protein direct top-3 run strongly suppresses anchor usage and raises entropy.
- Contact precision stays high at small-to-moderate alpha and only breaks later.

This is the main “pattern removal is real, but performance is initially robust” result.

Cite:
- code: `scripts/anchor_contact_steering.py`
- results: `contact_steering/direct_top3/anchor_contact_steering_summary.json`
- comparison: `contact_steering/projection_top3/anchor_contact_steering_summary.json`

### 3. In the local masked `jump_to` setup, anchor suppression does hurt contact prediction

- `local_flank_v1/` and `local_flank_contact_jump_v1/` identify a sharp local-context jump where the visible contact metric becomes good.
- In that `jump_to` setting, direct suppression strongly reduces anchor mass and also reduces local contact quality.

This is still the cleanest causal evidence for the local circuit story.

Cite:
- code: `scripts/anchor_local_flank_v1.py`, `scripts/anchor_local_flank_contact_jump_v1.py`, `scripts/anchor_local_flank_jump_to_steering.py`
- results: `local_flank_v1/anchor_local_flank_v1.md`
- results: `local_flank_contact_jump_v1/anchor_local_flank_contact_jump_v1.md`
- results: `local_flank_jump_to_steering/direct/anchor_local_flank_jump_to_steering.md`

### 4. The same head looks much more causal in flank than in full sequence

- In `contact_pattern_full_vs_flank/`, `k_only` and `ln_all` hurt the segment metric in `flank`.
- On the same proteins and metric in `full`, the same interventions are much weaker.
- The corrupt-head patch from the flank setup also hurts in `flank` but is largely neutral in `full`.

This is the main evidence that the paradox is context dependence, not that the head is irrelevant.

Cite:
- code: `scripts/contact_pattern_full_vs_flank.py`
- results: `contact_pattern_full_vs_flank/contact_pattern_full_vs_flank.md`

### 5. The local masked story generalizes beyond `2B61A` and `1PVGA`

- In `contact_pattern_flank_batch/`, patching or steering L10H9 in the masked local setup hurts the metric on most proteins with the contact jump.

This says the local causal effect is not just a two-protein anecdote.

Cite:
- code: `scripts/jump_to_contact_pattern_bridge.py`
- results: `contact_pattern_flank_batch/jump_to_contact_pattern_bridge.md`

### 6. In full sequence, `k_only` can remove anchoring without hurting the contact metric

- The single-head decomposition in `qkv_decomposition/` remains one of the most important mechanistic results.
- `k_only` removes the L10H9 anchor pattern while the contact metric stays flat.
- `v_only` and especially larger `ln_all`/downstream corruption are more associated with performance loss.

This is the strongest evidence that “destroying the key pattern” is not sufficient to explain full-sequence contact degradation.

Cite:
- code: `scripts/qkv_decomposition.py`, `scripts/downstream_attn_corruption.py`, `scripts/attn_output_tracking.py`
- results: `qkv_decomposition/qkv_decomposition.md`
- results: `downstream_corruption/downstream_attn_corruption.md`
- results: `attn_output_tracking/attn_output_tracking.md`

### 7. Compensation-head audits found plausible backup heads, but simple co-suppression did not explain full-sequence robustness

- `full_compensation_heads/` identified heads like `L11H16` as plausible reorganizing backup candidates.
- `full_compensation_coablation/` still showed that small candidate sets were not enough to break the full-sequence metric.

Cite:
- code: `scripts/full_compensation_heads.py`, `scripts/full_compensation_coablation.py`
- results: `full_compensation_heads/full_compensation_heads.md`
- results: `full_compensation_coablation/full_compensation_coablation.md`

### 8. Important correction: the first multimode compensation runs were contaminated by a bad direction implementation and were rerun

- In the original multimode compensation scripts, the search direction was accidentally changed from the original key-based construction to a query-based one.
- That made the first `full_compensation_multimode*` interpretation invalid.
- The scripts were corrected to use the original key-based direction again and the canonical output folders were overwritten with corrected reruns.

After correction:

- `k_only` in `full_compensation_multimode_with_l10h9/` now really does reduce multi-head anchor mass strongly.
- But even after that correction, the full-sequence metric still does not fall under `k_only`; it stays flat or even rises slightly.

So the corrected conclusion is stronger than before:

- the old multimode contradiction was an implementation mistake
- after fixing it, the deeper full-sequence result still survives
- strong key-side de-anchoring is still not sufficient to hurt the full-sequence metric on these proteins

Cite:
- code: `scripts/full_compensation_multimode.py`
- results: `full_compensation_multimode/full_compensation_multimode.md`
- results: `full_compensation_multimode_with_l10h9/full_compensation_multimode.md`
- results: `full_compensation_multimode_with_l10h9/full_compensation_multimode_summary.json`
- results: `full_compensation_multimode_with_l10h9/full_compensation_multimode_per_head.csv`

### 9. Current best working interpretation

- Local masked contact prediction really is sensitive to this head.
- Full-sequence contact prediction is much more robust.
- That robustness is not currently explained by a simple “backup vertical head” or “key-only substitute head” story.
- The remaining plausible mechanisms are broader hidden-state / value-residual / downstream recomputation effects enabled by full sequence context.

## Important Caveats

- `2B61A` and `1PVGA` are not in the local-flank top-50 audit cohort, so they are not part of the `local_flank_*` aggregate reruns here.
- `top3_mass` saturation does not mean the intervention stopped working. It often means the head rerouted to other preferred keys.
- Very large alpha values mix “targeted suppression” with broader distribution shift, so the cleanest mechanistic region is usually around `alpha = 0.5` to `2`.
- The first multimode compensation interpretation was invalid because the direction implementation drifted; use the corrected `full_compensation_multimode*` outputs, not any earlier verbal summary of them.

## Recommended Reading Order

If you want the shortest path through the folder:

1. `local_flank_v1/anchor_local_flank_v1.md`
2. `local_flank_contact_jump_v1/anchor_local_flank_contact_jump_v1.md`
3. `local_flank_jump_to_steering/direct/anchor_local_flank_jump_to_steering.md`
4. `contact_steering/direct_top3/anchor_contact_steering_summary.json`
5. `qkv_decomposition/qkv_decomposition.md`
6. `contact_pattern_full_vs_flank/contact_pattern_full_vs_flank.md`
7. `contact_pattern_flank_batch/jump_to_contact_pattern_bridge.md`
8. `full_compensation_heads/full_compensation_heads.md`
9. `full_compensation_coablation/full_compensation_coablation.md`
10. `full_compensation_multimode_with_l10h9/full_compensation_multimode.md`

## Next Good Experiments

If we continue from here, the highest-signal next steps are:

- keep future interventions mathematically aligned with the original key-based direction
- focus new compensation experiments on mechanisms beyond simple key-only backup heads
- prefer the local `jump_to` setup when the goal is the cleanest causal test
