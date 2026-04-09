# Scramble Experiment Results

N proteins = 200, repeats per stochastic condition = see CSV

## Summary statistics

| Condition | Description | Mean alpha_norm | Std | Survival rate |
|---|---|---|---|---|
| C0 | Baseline (isolated flank) | 1.0000 | 0.0000 | 100.0% |
| C1 | Within-SSE scramble | 0.6108 | 0.2556 | 71.5% |
| C2 | Full flank scramble | 0.0252 | 0.2837 | 4.0% |
| C3 | Conservative substitution | 0.6341 | 0.3184 | 78.5% |
| C4 | Scramble buried only | 0.5519 | 0.3420 | 61.5% |
| C5 | Scramble exposed only | 0.9908 | 0.0194 | 100.0% |
| C6 | Random (null control) | 0.0141 | 0.2893 | 6.0% |

## Interpretation

C1 and C3 both preserved the anchor signal. The model identifies anchors using coarse physical properties and SSE layout, consistent with geometric logic rather than sequence identity reading.
