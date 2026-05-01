# Anchor Path Patching

Implements `experiments/4_26_anchor_path_patching.md` in the masked-flank contact-pattern setup.

## 2B61A

- Contact pair: `(182, 316)`
- Clean flank: `44`
- Corrupt flank: `43`
- Clean anchors: `[315, 163, 181]`
- Receiver count: `1`
- `alpha*`: `0.25`
- Clean / corrupt metric: `0.5738` / `0.0279`
- Total metric: `0.3315`
- Direct metric: `0.5738`
- Downstream-only contribution (`direct - total`): `0.2423`

| Receiver | Replay metric | Replay frac of total | Blocked metric | Blocking frac of total | Pass-C attn L1 | Full-source attn L1 |
|----------|--------------:|---------------------:|---------------:|-----------------------:|---------------:|--------------------:|
| L11H1 | 0.5197 | 0.2231 | 0.3671 | 0.1471 | 23.77 | 23.77 |
