# SAE Frozen-Error IE Ranking and Sufficiency (v1)

Proteins analysed: 50

## Coarse decomposition controls

| Condition | M_score frac (mean +- std) | M_attn frac (mean +- std) |
|---|---|---|
| Full (lat+err) | 1.000 +- 0.000 | 1.000 +- 0.000 |
| Latents only | 0.663 +- 0.237 | 0.679 +- 0.341 |
| Error only | -0.267 +- 0.530 | 0.267 +- 0.414 |

## Sufficiency summary

| k | M_score frac mean | M_score frac median | M_attn frac mean | M_attn frac median |
|---|---|---|---|---|
| 1 | -0.147 | -0.040 | 0.327 | 0.024 |
| 2 | -0.133 | -0.021 | 0.268 | 0.020 |
| 5 | -0.038 | 0.042 | 0.262 | 0.015 |
| 10 | 0.021 | 0.119 | 0.259 | 0.022 |
| 20 | 0.119 | 0.170 | 0.290 | 0.047 |
| 50 | 0.210 | 0.225 | 0.291 | 0.036 |
| 100 | 0.176 | 0.212 | 0.178 | 0.027 |
| 200 | 0.090 | 0.084 | 0.083 | 0.012 |
| 500 | 0.219 | 0.191 | 0.082 | 0.034 |

## Minimal k for recovery thresholds

- 50%: mean=118.0, median=50.0 (32/50 never reached)
- 80%: mean=2.0, median=2.0 (49/50 never reached)
- 90%: mean=10.0, median=10.0 (49/50 never reached)

## IE mass concentration

- Mean |IE| at anchor token: 0.347
- Mean |IE| within +-5 of anchor: 0.389
- Mean |IE| rest of sequence: 0.611

## Top 10 recurring latent indices (in top-20 IE pairs)

| Latent | Count |
|---|---|
| 619 | 63/50 |
| 1815 | 50/50 |
| 1591 | 40/50 |
| 2662 | 39/50 |
| 2894 | 39/50 |
| 431 | 32/50 |
| 3716 | 30/50 |
| 3539 | 30/50 |
| 3139 | 22/50 |
| 2380 | 18/50 |

## Interpretation

Full reconstruction recovers 100.0% of clean M_score (sanity check).
Latents-only recovers 66.3%; error-only recovers -26.7%.
Neither latents-only nor error-only fully explains the metric. The anchor behavior depends on both SAE-captured and SAE-missed components.
Median k_50 = 50, suggesting distributed causal support (Outcome B direction).