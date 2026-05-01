# Anchor Contact Steering: Effect on Contact Prediction

## Context

L10H9 concentrates attention on 1-3 anchor residues per protein, selected by a universal search direction d = W_K^T @ q_mean (Spearman rho ~0.96 across 1982 proteins, see anchor_behavior_audit.md). The selector ablation experiment (3_29_steering_against.md, anchor_selector_ablation.py) showed that removing the d-component suppresses anchor attention and disrupts distal predictions for masked residues.

The missing piece: does the anchor mechanism causally contribute to ESM2's contact prediction? Contact prediction uses attention from all 33 layers via the contact head (a learned linear combination of attention maps + APC correction). If anchors matter for contact prediction, suppressing the search direction at the anchor should degrade contact quality.

## Goal

Steer against d at the anchor position with varying strength (alpha) and measure the effect on contact prediction quality using CASP-standard Precision@L/k metrics.

## Inputs

- ~1020 proteins with PDB structures (data/pdb/) and sequences (data/full_seq_dict.json), 100-500 residues
- ESM2-650M model via nnsight
- Universal search direction d from 2B61A

## Intervention

For each protein:
1. Identify top-1 anchor as argmax of d-projection scores on L10 LayerNorm output
2. Subtract alpha * d_unit from LayerNorm output at anchor position
3. Cache attention from all 33 layers (layers 0-9 unaffected, 10-32 changed via residual stream)
4. Compute contact map via contact_head manually

Alpha values: [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]

Control: at alpha=1.0, also intervene at ALL positions (tests specificity of anchor effect).

## Metrics

Ground truth: Cb-Cb distance < 8A from PDB (Ca for Gly), focus on long-range contacts (|i-j| >= 24).

- P@L/5: precision of top L/5 predicted long-range contacts
- P@L/2: precision of top L/2
- P@L: precision of top L

These are the standard CASP contact prediction evaluation metrics.

## Hypotheses

Strong result: anchor-only steering at moderate alpha (1.0-2.0) causes a clear drop in long-range precision, and this drop is larger than the all-position control (meaning the anchor is a leveraged point, not just one of many positions contributing equally).

Weak/null result: precision does not change with alpha, or all-position control shows equal/larger effect (anchor is not special for contacts).

## Outputs

- reports/outputs/multi_protein/anchor_contact_steering_results.csv
- reports/outputs/multi_protein/anchor_contact_steering_summary.json
- reports/outputs/multi_protein/anchor_contact_steering.png
- reports/outputs/multi_protein/anchor_contact_steering_distributions.png

## Script

scripts/anchor_contact_steering.py

Usage:
    uv run python scripts/anchor_contact_steering.py --device cuda
    uv run python scripts/anchor_contact_steering.py --device cuda --max-proteins 5
