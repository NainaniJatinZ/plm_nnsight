# ESM2 3B Flank Sweep

First-pass 3B flank scan using the masking and contact metric from `contact_pattern_v2.py`.
Jump criterion: first single-step increase with delta >= 0.500.

- Output CSV: `reports/out2/esm2_3b_flank_sweep_smoke/esm2_3b_flank_sweep.csv`
- Summary CSV: `reports/out2/esm2_3b_flank_sweep_smoke/esm2_3b_flank_sweep_summary.csv`
- Plot written: `True`

| Protein | Pair | Jump found | Jump from | Jump to | Jump delta | Max jump delta | Last flank | Metric @ last flank |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1BRTA | (119, 221) | True | 21 | 22 | 0.9178 | 0.9178 | 27 | 0.9014 |
| 1BS0A | (90, 276) | True | 34 | 35 | 0.5006 | 0.5006 | 39 | 0.6824 |
| 1DYPA | (116, 228) | False | 28 | 29 | 0.2993 | 0.2993 | 60 | 0.6412 |
| 1E6UA | (19, 219) | True | 31 | 32 | 0.8088 | 0.8088 | 35 | 0.9993 |
| 1ELUA | (61, 281) | True | 37 | 38 | 0.6497 | 0.6497 | 43 | 0.7289 |
