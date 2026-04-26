# Downstream Attention Corruption

Measures attention divergence from clean under the canonical direct/top-3 anchor suppression setup.

Proteins analyzed: 2
Alphas: 0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 10.0, 12.0, 14.0, 16.0, 32.0

## Main readout

- Mean downstream-layer JSD (layers 11-32) rises from 0.0000 at alpha=0 to 0.0090 at alpha=4, 0.0149 at alpha=8, 0.0482 at alpha=10, 0.1560 at alpha=12, and 0.2437 at alpha=16.
- Layer-10 JSD rises earlier and more strongly: 0.0124 at alpha=0.5, 0.0412 at alpha=1, 0.0814 at alpha=2.
- Pre-L10 layers remain near-zero as expected: mean JSD across layers 0-9 is 0.0000 at alpha=8 and 0.0000 at alpha=16.

## Contact overlay

- Canonical P@L/5 stays high through alpha=8 (0.889), then drops at alpha=10 (0.824) and alpha=12 (0.664).
- This should be compared against the downstream JSD curve in `downstream_attn_corruption_overlay.png`.

## Files

- `downstream_attn_corruption.csv`: per-protein/layer/head metrics
- `downstream_attn_corruption_summary.json`: aggregate arrays used by plots
- `downstream_attn_corruption_heatmap.png`: layer x alpha mean JSD
- `downstream_attn_corruption_layer_profiles.png`: mean JSD vs layer for each alpha
- `downstream_attn_corruption_overlay.png`: downstream JSD vs contact P@L/5
