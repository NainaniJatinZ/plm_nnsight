# Experiment: Flank Scramble — Sequence Identity vs Geometric Logic

## The question

Does the model identify anchors by reading specific amino acid identities at specific positions (sequence identity), or by inferring geometric properties from coarser sequence patterns (geometric logic)?

Everything we've done so far is correlational. H4 > H1 in classification, but that could mean structural features are better proxies for the actual sequence pattern the model reads. The QK decomposition shows what the representation looks like but not how it's computed. We need a causal experiment.

## Core design

Take proteins with known anchors. Scramble the amino acid identities in the flank while preserving different levels of structural information. Re-run ESM2. Measure whether the anchor signal ($\alpha_{norm}$) survives.

If the model needs specific AAs at specific positions → $\alpha_{norm}$ drops under scrambling (sequence identity).
If the model infers geometry from coarser patterns → $\alpha_{norm}$ is preserved under structure-preserving scrambles (geometric logic).

---

## Conditions

For each protein, compute $\alpha_{norm}$ at the anchor position under these flank modifications (all applied to the ±25 window around the anchor, anchor position itself is NOT scrambled):

### C0: Baseline (no modification)
The original sequence. This is the reference $\alpha_{norm}$.

### C1: Scramble within SSE segments
Randomly permute amino acid identities WITHIN each contiguous SSE segment (helix, strand, coil) in the ±25 window. This preserves:
- Which amino acids are in helix vs strand vs coil (composition per SSE)
- SSE boundaries and arrangement
- Global amino acid composition of the flank

This destroys:
- Specific AA at specific position
- Local sequence motifs within SSE segments
- Any position-specific identity pattern

**If $\alpha_{norm}$ is preserved:** The model only needs the AA composition per SSE type — not the specific arrangement. This strongly supports geometric logic (SSE + composition is a structural descriptor).

**If $\alpha_{norm}$ drops:** The model needs position-specific AA identities within SSE segments.

### C2: Scramble across entire flank
Randomly permute ALL amino acid identities in the ±25 window (ignoring SSE boundaries). This preserves:
- Global AA composition of the flank
- Nothing about position-specific identity

This destroys:
- Everything except total composition

**If C1 preserves but C2 drops:** The SSE-specific composition matters (which AAs are in helices vs strands).
**If C2 also preserves:** Even composition doesn't matter — something even coarser is enough.

### C3: Conservative substitutions only
Replace each AA in the ±25 flank with a random AA from the same physicochemical class:
- Hydrophobic: A, V, I, L, M, F, W, P
- Polar: S, T, N, Q, Y, C
- Positive: K, R, H
- Negative: D, E
- Special: G (keep as is)

This preserves:
- Physicochemical profile at each position (hydrophobic stays hydrophobic, charged stays charged)
- Position-specific physical properties

This destroys:
- Specific AA identity (L→I, K→R, etc.)

**If $\alpha_{norm}$ is preserved:** The model uses physicochemical properties, not specific identities. This is the hallmark of geometric logic (hydrophobicity pattern → burial pattern → structural context).

**If $\alpha_{norm}$ drops:** The model needs SPECIFIC amino acids, not just their physical class. This would support sequence identity.

### C4: Scramble buried positions only
Scramble (random permutation) only flank positions with RSA < 0.05. Leave exposed positions unchanged.

### C5: Scramble exposed positions only
Scramble only flank positions with RSA > 0.25. Leave buried positions unchanged.

**C4 vs C5 comparison:** If scrambling buried positions kills the signal but scrambling exposed positions doesn't, the model reads the identities of buried residues specifically. If the reverse, it reads exposed residues. If neither kills it, the model uses a property that's invariant to individual AA identity.

### C6: Random sequence (null control)
Replace the entire ±25 flank with random amino acids drawn from the background frequency of the 20 AAs (from UniRef50 or similar). This destroys everything — composition, SSE-appropriate AAs, all patterns.

This should kill $\alpha_{norm}$ completely. If it doesn't, something is wrong.

---

## Implementation

### Procedure per protein
1. Run ESM2 on full sequence → get baseline $\alpha_{norm}$ (C0)
2. Identify anchor position and the ±25 flank
3. Get SSE assignments and RSA values (from PDB features, already computed)
4. For each condition C1-C6:
   a. Modify the flank amino acids according to the condition
   b. Run ESM2 on the modified sequence
   c. Compute $\alpha_{norm}$ at the anchor position using the same d direction
5. Repeat each stochastic condition (C1, C2, C3, C6) 10 times with different random seeds
6. Report mean and std of $\alpha_{norm}$ across repeats

### Protein set
Use ~200 confident proteins (top1_mass > 0.5) that also have PDB features (need SSE and RSA for C1, C4, C5). Select proteins where baseline $\alpha_{norm}$ > 0.5 to ensure a clear signal to measure degradation of.

### Key implementation detail
The anchor position itself is NEVER scrambled. Only the flank residues are modified. The rest of the protein (outside the ±25 window) is also unchanged. This isolates the flank's contribution.

Also: positions outside the ±25 window should be masked (set to mask token), not kept as original. Otherwise the model could reconstruct the anchor signal from distal context. Actually — we should run two variants:
- **Full context**: rest of protein is unchanged (only flank is scrambled)
- **Isolated flank**: everything outside ±25 is masked

The isolated flank variant is cleaner because it ensures the signal can ONLY come from the ±25 window. The full context variant tests whether the model can compensate using distal sequence.

For the primary analysis, use **isolated flank** (mask everything outside ±25). Report full context as a secondary check.

---

## Analysis

### Primary metric
For each condition, compute:
- Mean $\alpha_{norm}$ across proteins and repeats
- Fraction of proteins where $\alpha_{norm}$ > 0.5 (anchor signal "survives")
- Paired comparison: $\Delta\alpha = \alpha_{norm}^{C0} - \alpha_{norm}^{Ci}$ per protein

### Decision table

| C1 (within-SSE scramble) | C3 (conservative subs) | Interpretation |
|---|---|---|
| Preserved | Preserved | Geometric logic: coarse physical properties + SSE layout is enough |
| Preserved | Drops | SSE-specific composition matters but not physical class (unlikely) |
| Drops | Preserved | Position-specific physicochemical profile matters (geometric, fine-grained) |
| Drops | Drops | Specific AA identities at specific positions required (sequence identity) |

### Secondary analyses
- C4 vs C5: does the signal depend on buried or exposed residue identities?
- C1 vs C2: does SSE-specific composition matter?
- Effect size: how much does each condition reduce $\alpha_{norm}$? Partial preservation (e.g., 0.5 → 0.3) is informative — the model uses identity partially but not entirely.
- Per-protein variation: are some proteins more robust to scrambling than others? Correlate robustness with structural properties.

---

## Compute estimate

- 200 proteins × 7 conditions × 10 repeats (for stochastic ones) = ~10,000 forward passes
- But C0 is 1 pass, C4/C5 are 10 each, so: 200 × (1 + 10 + 10 + 10 + 10 + 10 + 10) = ~12,200 forward passes
- ESM2-650M forward pass on ~200-residue masked sequence: ~0.1s on GPU
- Total: ~20 min on GPU

---

## Outputs

- `reports/outputs/multi_protein/scramble_experiment.md`
- `reports/outputs/multi_protein/scramble_alpha_by_condition.png` — box plot of $\alpha_{norm}$ per condition
- `reports/outputs/multi_protein/scramble_survival_rate.png` — fraction surviving per condition
- `reports/outputs/multi_protein/scramble_paired_delta.png` — paired $\Delta\alpha$ distributions
- `reports/outputs/multi_protein/scramble_results.csv`

---

## Script

```bash
uv run python scripts/scramble_experiment.py --device cuda --n-proteins 200 --n-repeats 10
```

---

## Why this is the right experiment now

1. It's CAUSAL, not correlational. We directly intervene on the sequence and measure the effect.
2. It directly pits the two hypotheses against each other with a clean decision table.
3. It's fast (~20 min compute).
4. The result is interpretable regardless of outcome — both "identity" and "geometry" results are publishable and interesting.
5. It doesn't require more feature engineering.
