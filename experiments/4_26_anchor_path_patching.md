# Experiment: Path Patching From L10H9 Into the Flank Contact Circuit

## Goal

Measure which downstream circuit heads mediate the contact-prediction drop caused by suppressing the anchor head `L10H9` in the masked flank setting.

This is a **proper causal path-patching** experiment:

- not token-level patching
- not attribution patching
- not full-sequence contact evaluation

The base setting is the **contact-pattern clean/corrupt masked-flank setup** where anchor suppression is already known to matter.

## Why This Setting

Use the masked flank setup, not full sequence.

More precisely:

- this is the same clean/corrupt counterfactual setup used in `contact_pattern.py`
- each protein has a fixed `clean_flank` and fixed `corrupt_flank`
- everything is masked except the two contact segments and the outward flanks

So for this spec, "`jump_to` setting" means:

- the masked contact-pattern setup at the chosen clean flank for that protein
- with the corresponding corrupt flank retained as the counterfactual baseline

It does **not** mean the anchor-centered local-flank reconstruction setup from `anchor_local_flank_v1.py`.

Reason:

- In `flank`, suppressing `L10H9` clearly hurts the segment metric.
- In `full`, strong de-anchoring can leave the segment metric nearly unchanged.

For the exact two proteins of interest, current results already show this split:

- `2B61A`: [reports/out2/suppressing_anchors/jump_to_contact_pattern_bridge/jump_to_contact_pattern_bridge.md](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/reports/out2/suppressing_anchors/jump_to_contact_pattern_bridge/jump_to_contact_pattern_bridge.md)
- `1PVGA`: [reports/out2/suppressing_anchors/contact_pattern_full_vs_flank/contact_pattern_full_vs_flank.md](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/reports/out2/suppressing_anchors/contact_pattern_full_vs_flank/contact_pattern_full_vs_flank.md)

## Proteins And Receiver Sets

Start with:

- `2B61A`
- `1PVGA`

Source head:

- `L10H9`

Receiver heads:

- use the previously discovered downstream head-level circuit for each protein
- restrict to heads with `layer > 10`
- exclude `L10H9` itself

Existing circuit references:

- `2B61A`: [reports/outputs/2B61A/2B61A_single_contact_circuits.txt](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/reports/outputs/2B61A/2B61A_single_contact_circuits.txt)
- `1PVGA`: [reports/outputs/1PVGA/1PVGA_sse_circuit_ablation.md](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/reports/outputs/1PVGA/1PVGA_sse_circuit_ablation.md)

Before running the experiment, write an explicit per-protein receiver manifest to disk. The experiment should consume that manifest, not re-discover the circuit on the fly.

Masked-setup references:

- [scripts/contact_pattern.py](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/scripts/contact_pattern.py)
- [scripts/jump_to_contact_pattern_bridge.py](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/scripts/jump_to_contact_pattern_bridge.py)

## Step 1: Calibrate The Counterfactual Alpha

We need one source intervention strength `alpha*` for each protein, using the **clean masked flank sequence**.

Intervention for calibration:

- `ln_all` suppression of `L10H9` at the clean anchor positions

Sweep:

- `alpha in [0.0, 0.25, 0.5, 0.75, 1.0, 2.0, 4.0, 6.0, 8.0]`

For each alpha, record:

- segment metric
- faithfulness relative to clean/corrupt masked baselines
- `L10H9` anchor mass
- `L10H9` top-1 mass
- `L10H9` entropy norm

Definition of `alpha*`:

- choose the **smallest** alpha where both:
- anchor mass is materially below clean
- segment metric is materially below clean

Operationally, use:

- anchor mass drop `>= 25%` relative to clean
- segment-faithfulness drop `>= 10%` of the clean-corrupt gap

Also report the raw sweep table, because the threshold itself matters.

Current repo evidence suggests the answer is already near `alpha = 0.5` for both proteins in the flank setting, so do not assume `alpha ≈ 5`.

## Step 2: Baseline Effects

Using `alpha*`, compute three baseline quantities on the clean masked flank input.

### 2.1 Total Effect

Suppress `L10H9` and let everything downstream run normally.

Measure:

- segment metric drop
- receiver-head attention changes

### 2.2 Direct Effect

Direct effect must be defined at the level of the **attention patterns seen by the contact head**, not attention outputs.

So construct a direct-effect attention stack:

- start from the clean attention stack
- replace only `L10H9` with its source-suppressed attention pattern
- keep every other head's attention pattern clean

Then evaluate the segment metric from that modified attention stack.

This is the right direct-effect object because the ESM contact head consumes the attention patterns from all heads directly.

Measure:

- segment metric drop

Expectation:

- probably near zero

### 2.3 Total Minus Direct

This is the aggregate downstream attention-mediated effect.

## Step 3: Single-Receiver Path Patching

For each receiver head `r = (layer_r, head_r)`, run a two-pass experiment.

### Pass C: Isolate `L10H9 -> r`

Run on the **clean masked flank** input.

Apply:

- suppress source `L10H9` with `alpha*`
- keep MLPs free
- freeze all attention heads in layers `11 .. layer_r - 1` to their clean attention-block context outputs
- in `layer_r`, freeze all heads except `head_r` to their clean attention-block context outputs
- let `head_r` recompute normally

Cache from this pass:

- receiver attention pattern `A_r^src`
- receiver Q and K tensors as diagnostics
- receiver context vector

Important:

- in Pass C, freeze the clean **attention-block context output**, not the attention input residual stream
- freeze **full clean context output**, not just clean attention probabilities
- otherwise clean attention + changed V leaks extra paths

Why this is okay:

- Pass C is **not** the final metric intervention
- Pass C is only a tool to isolate how the source changes the receiver attention pattern
- for that internal isolation step, freezing attention outputs is appropriate

### Pass D: Replay Only The Receiver Change

Run a new forward pass on the same clean masked flank input.

Apply:

- patch only receiver head `r` with `A_r^src`
- recompute its context with the clean V from that pass, exactly like the existing head-attention patching code
- let all later layers run freely

Primary causal readout:

- segment metric drop from this receiver replay

Interpretation:

- this is the causal effect of the isolated `L10H9 -> r` path, measured at the end metric
- later heads are allowed to change here, so this is a mediated downstream effect from the receiver onward

## Step 4: Receiver-Blocking Cross-Check

Also run the complementary test for each receiver.

Run the source-suppressed pass again, but patch receiver `r` back to its clean attention pattern.

Measure:

- how much of the total source effect disappears when `r` is blocked

This gives two numbers per receiver:

- `replay_effect(r)`: clean + isolated receiver change
- `blocking_reduction(r)`: source-suppressed run with receiver reset to clean

Good receivers should score on both.

## Primary Outputs

Per protein:

- alpha calibration table
- clean / corrupt / total / direct metrics
- per-receiver table with:
- receiver head
- clean metric
- total-effect metric
- pass-C attention delta magnitude
- replay effect
- blocking reduction
- fraction of total effect explained

Plots:

- bar chart of receiver replay effects
- bar chart of receiver blocking reductions
- optional scatter: pass-C attention delta vs replay effect

## Implementation Notes

Use these as the base, in this order:

- [scripts/jump_to_contact_pattern_bridge.py](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/scripts/jump_to_contact_pattern_bridge.py)
- [scripts/path_patching.py](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/scripts/path_patching.py)
- [scripts/contact_pattern_full_vs_flank.py](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/scripts/contact_pattern_full_vs_flank.py)

Do **not** base this on:

- [scripts/attr_patching.py](/work/pi_annagreen_umass_edu/jatin/plm_nnsight/scripts/attr_patching.py)

Reason:

- that file is attribution patching
- this experiment needs causal sender-to-receiver path patching

Receiver object choice:

- primary object to patch is the **receiver head attention pattern**
- Q/K deltas are diagnostics only

This matches the current project’s head-level circuit framing and the user requirement to “replace the target with the previous experiment’s attention.”

Important distinction:

- for **metric-level direct effect**, clamp or splice **attention patterns**
- for **source-to-receiver isolation** in Pass C, freeze **attention context outputs**

Those are different interventions serving different purposes.

## Success Condition

The experiment is successful if it produces a ranked list of downstream heads showing:

- which heads actually mediate the `L10H9` suppression effect in flank
- how much of the total contact drop is direct vs downstream-mediated
- whether the causal mass is concentrated in a few receivers or spread across many
