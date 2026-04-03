# Classification Framing of the Anchor Search Direction

The regression R2=0.24 understates the explanatory power of structural features because the relationship is a threshold/gate, not a linear slope.
These features define an eligibility set; within that set the contextual computation in layers 7-9 determines the final ranking.

## 1. Enrichment analysis

What fraction of the top-k scoring residues (by projection score) pass the tail filter (RSA < 0.05, contacts >= 10, SSE = E)?

| Top-k | k/N | Tail in top-k | Fraction in tail | Enrichment vs baseline |
|-------|-----|---------------|-----------------|------------------------|
| 5 | 0.001 | 5/5 | 1.000 | 7.2x |
| 10 | 0.002 | 9/10 | 0.900 | 6.5x |
| 20 | 0.004 | 17/20 | 0.850 | 6.1x |
| 30 | 0.006 | 25/30 | 0.833 | 6.0x |
| 50 | 0.010 | 40/50 | 0.800 | 5.8x |
| 100 | 0.021 | 73/100 | 0.730 | 5.2x |
| 200 | 0.041 | 121/200 | 0.605 | 4.4x |
| 500 | 0.103 | 206/500 | 0.412 | 3.0x |

Baseline tail rate: 676/4861 = 0.139

Per-protein: fraction of top-10 scorers that are in tail:

| Protein | Top-10 in tail | Top-10 fraction |
|---------|---------------|------------------|
| 1BRTA | 7/10 | 0.70 |
| 1PVGA | 5/10 | 0.50 |
| 2B61A | 7/10 | 0.70 |
| 2DPMA | 7/10 | 0.70 |
| 2QY6A | 4/10 | 0.40 |
| 2YHWA | 6/10 | 0.60 |
| 3CSSA | 7/10 | 0.70 |
| 3HO7A | 6/10 | 0.60 |
| 3OKPA | 9/10 | 0.90 |
| 3QDLA | 4/10 | 0.40 |
| 3WJPA | 7/10 | 0.70 |
| 4EHUA | 7/10 | 0.70 |
| 4EX6A | 6/10 | 0.60 |
| 4EZIA | 7/10 | 0.70 |
| 4ME3A | 4/10 | 0.40 |
| 4N9WA | 7/10 | 0.70 |
| 4OY3A | 8/10 | 0.80 |

Mean per-protein top-10 tail fraction: 0.635

## 2. Variance decomposition

How much of the total variance in projection scores is explained by the binary tail membership alone?

Grand mean projection: -0.5093
Tail mean: -0.3242 (N=676)
Non-tail mean: -0.5392 (N=4185)
Tail std: 0.3804
Non-tail std: 0.1641

SS_between / SS_total (eta-squared): 0.1134
This single binary feature explains 11.3% of variance.

Stepwise eta-squared for individual filter components:

- SSE = E: eta2=0.0774 (7.7%), in-group N=1053, mean=-0.3924, t=20.2, p=4.60e-87
- RSA < 0.05: eta2=0.0807 (8.1%), in-group N=2505, mean=-0.4484, t=20.7, p=6.78e-91
- contacts_8A >= 10: eta2=0.0830 (8.3%), in-group N=2813, mean=-0.4550, t=21.0, p=1.36e-93
- SSE=E AND RSA<0.05: eta2=0.1090 (10.9%), in-group N=713, mean=-0.3333, t=24.4, p=5.18e-124
- SSE=E AND contacts>=10: eta2=0.1020 (10.2%), in-group N=822, mean=-0.3529, t=23.5, p=1.19e-115
- Full tail filter: eta2=0.1134 (11.3%), in-group N=676, mean=-0.3242, t=24.9, p=3.85e-129

## 3. Rank concentration

For each protein: what fraction of the top-scoring decile (top 10%) falls in the tail?
And conversely: what fraction of the tail falls in the top decile?

| Protein | N | Tail N | Top-10% in tail (precision) | Tail in top-10% (recall) |
|---------|---|--------|----------------------------|-------------------------|
| 1BRTA | 277 | 35 | 10/27 = 0.37 | 10/35 = 0.29 |
| 1PVGA | 368 | 58 | 11/36 = 0.31 | 11/58 = 0.19 |
| 2B61A | 349 | 43 | 12/34 = 0.35 | 12/43 = 0.28 |
| 2DPMA | 258 | 23 | 11/25 = 0.44 | 11/23 = 0.48 |
| 2QY6A | 244 | 33 | 5/24 = 0.21 | 5/33 = 0.15 |
| 2YHWA | 308 | 48 | 8/30 = 0.27 | 8/48 = 0.17 |
| 3CSSA | 264 | 44 | 10/26 = 0.38 | 10/44 = 0.23 |
| 3HO7A | 220 | 39 | 9/22 = 0.41 | 9/39 = 0.23 |
| 3OKPA | 378 | 46 | 18/37 = 0.49 | 18/46 = 0.39 |
| 3QDLA | 178 | 22 | 7/17 = 0.41 | 7/22 = 0.32 |
| 3WJPA | 335 | 39 | 15/33 = 0.45 | 15/39 = 0.38 |
| 4EHUA | 268 | 38 | 11/26 = 0.42 | 11/38 = 0.29 |
| 4EX6A | 219 | 23 | 9/21 = 0.43 | 9/23 = 0.39 |
| 4EZIA | 359 | 50 | 11/35 = 0.31 | 11/50 = 0.22 |
| 4ME3A | 246 | 41 | 13/24 = 0.54 | 13/41 = 0.32 |
| 4N9WA | 360 | 43 | 19/36 = 0.53 | 19/43 = 0.44 |
| 4OY3A | 230 | 51 | 14/23 = 0.61 | 14/51 = 0.27 |

Mean precision: 0.408
Mean recall: 0.296

## 4. Effect sizes

Cohen's d (tail vs non-tail): 1.034
This is a large effect.

Mann-Whitney U: U=2047058, p=3.42e-78
Common Language Effect Size: P(tail residue scores higher than non-tail residue) = 0.724

## 5. Reverse test: can projection score predict tail membership?

If the direction encodes these structural features, then projection score should predict tail membership.

Logistic regression: P(in_tail | proj_score)
AUROC: 0.7236
AUPRC: 0.3681 (baseline = 0.1391)
Logistic coef: 3.5123, intercept: -0.1753

Multi-feature logistic: P(top-decile | structural features)

AUROC: 0.7942
AUPRC: 0.3211 (baseline = 0.1008)

| Feature | Logistic coef |
|---------|---------------|
| SSE_E | 0.7269 |
| SSE_H | 0.0197 |
| RSA | -0.5608 |
| contacts_8A | 0.2028 |
| self_hydro | 0.1780 |

## 6. Within-tail variance

After conditioning on tail membership, how much variance remains? This is the part attributable to the contextual layers 7-9 computation.

Total variance in projection scores: 0.0488
Within-tail variance: 0.1447
Within-non-tail variance: 0.0269
Pooled within-group variance: 0.0433
Fraction of variance explained by tail membership: 0.1134

Within-tail projection score distribution per protein:

| Protein | Tail N | Tail mean | Tail std | Anchor proj | Anchor z (within tail) |
|---------|--------|-----------|----------|-------------|------------------------|
| 1BRTA | 35 | -0.293 | 0.387 | 0.864 | 2.99 |
| 1PVGA | 58 | -0.331 | 0.316 | 1.190 | 4.82 |
| 2B61A | 43 | -0.311 | 0.366 | 1.059 | 3.75 |
| 2DPMA | 23 | -0.219 | 0.488 | 0.963 | 2.42 |
| 2QY6A | 33 | -0.363 | 0.403 | 1.076 | 3.57 |
| 2YHWA | 48 | -0.375 | 0.398 | 1.254 | 4.09 |
| 3CSSA | 44 | -0.418 | 0.345 | 0.784 | 3.48 |
| 3HO7A | 39 | -0.425 | 0.433 | 0.514 | 2.17 |
| 3OKPA | 46 | -0.184 | 0.433 | 0.836 | 2.35 |
| 3QDLA | 22 | -0.398 | 0.087 | - | - |
| 3WJPA | 39 | -0.316 | 0.349 | 1.262 | 4.52 |
| 4EHUA | 38 | -0.308 | 0.317 | - | - |
| 4EX6A | 23 | -0.172 | 0.432 | 0.983 | 2.67 |
| 4EZIA | 50 | -0.396 | 0.360 | 0.967 | 3.78 |
| 4ME3A | 41 | -0.358 | 0.316 | - | - |
| 4N9WA | 43 | -0.166 | 0.430 | 0.820 | 2.29 |
| 4OY3A | 51 | -0.384 | 0.329 | 0.905 | 3.92 |

## Plots

See anchor_regression_v2_classification.png
