# Attention Output Tracking

Tracks the layer-10 attention residual contribution vector (`attention.output.dense`) under the canonical direct/top-3 intervention.

Proteins analyzed: 20

## Aggregate metrics

| Alpha | Anchor norm ratio | Non-anchor norm ratio | Anchor cosine | Non-anchor cosine |
|------:|------------------:|----------------------:|--------------:|------------------:|
| 0.0 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| 0.5 | 0.8574 | 0.7678 | 0.9588 | 0.9353 |
| 1.0 | 0.7644 | 0.6351 | 0.8331 | 0.7019 |
| 2.0 | 0.7144 | 0.5981 | 0.5142 | 0.3380 |
| 4.0 | 0.7534 | 0.5918 | 0.3371 | 0.2034 |
| 8.0 | 1.5055 | 0.6317 | 0.1292 | 0.1529 |
| 10.0 | 2.5320 | 0.7771 | -0.0226 | 0.0962 |
| 12.0 | 3.5467 | 1.0604 | -0.0917 | 0.0379 |
| 14.0 | 4.4122 | 1.4355 | -0.1121 | -0.0047 |
| 16.0 | 5.2100 | 1.8659 | -0.1109 | -0.0321 |
| 32.0 | 11.8807 | 6.6847 | -0.1174 | -0.0670 |
