# Attention Output Tracking

Tracks the layer-10 attention residual contribution vector (`attention.output.dense`) under the canonical direct/top-3 intervention.

Proteins analyzed: 2

## Aggregate metrics

| Alpha | Anchor norm ratio | Non-anchor norm ratio | Anchor cosine | Non-anchor cosine |
|------:|------------------:|----------------------:|--------------:|------------------:|
| 0.0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.5 | 0.8385 | 0.7336 | 0.9564 | 0.9328 |
| 1.0 | 0.7609 | 0.6227 | 0.8416 | 0.7710 |
| 2.0 | 0.7509 | 0.5791 | 0.6278 | 0.6052 |
| 4.0 | 0.8740 | 0.5650 | 0.5033 | 0.5609 |
| 8.0 | 1.5256 | 0.5785 | 0.2774 | 0.5196 |
| 10.0 | 2.5322 | 0.6823 | 0.0349 | 0.4397 |
| 12.0 | 3.9094 | 0.9352 | -0.1268 | 0.3247 |
| 14.0 | 4.9692 | 1.3151 | -0.1746 | 0.2295 |
| 16.0 | 5.7700 | 1.7637 | -0.1727 | 0.1599 |
| 32.0 | 11.9521 | 6.4955 | -0.1296 | -0.0303 |
