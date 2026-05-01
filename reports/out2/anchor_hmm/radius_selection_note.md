# Radius Selection Note

## Why `R=0` can look artificially good

In the fine-grained anchor-projection sweep, we found at least one protein
(`2QM0A`) where the projection curve is non-monotonic:

- `R=0`: anchor-position `alpha_norm` is already moderately high.
- `R=1..33`: the anchor-position projection drops sharply and stays low.
- `R=33->34`: the main recovery jump occurs.
- `R>=35`: the anchor projection recovers toward the full-sequence value.

This means the old `first radius where alpha_norm >= 0.5` summary can report
`R50 = 0` even when the meaningful local-window recovery happens much later.

Working hypothesis:

- with only the anchor residue left unmasked, attention and downstream
  projection can be artificially concentrated onto that lone visible residue;
- this inflates the anchor-position projection without implying that the true
  local context is unnecessary.

Operational change:

- keep `r50_first_crossing` as a diagnostic only;
- use `selected_radius`, defined from the recovery jump instead:
  first `delta alpha_norm >= jump_threshold`, otherwise the `argmax delta`
  fallback.

For `2QM0A`, this changes the interpretation from `R50 = 0` to
`selected_radius = 34`, which matches the visible recovery jump much better.
