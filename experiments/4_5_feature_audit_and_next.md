# Feature Audit, Missing Hypotheses, and the Identity vs Geometry Question

## Part 1: Every feature hypothesis tested, with honest assessment

---

### H1: Amino acid identity pattern
**What we tested:** Full per-position AA one-hot (20 × 61 = 1220 features) at R=30.
**Result:** AUPRC 0.320 (1.9× base rate). Weakest of H1-H4.
**What it means:** There IS some AA pattern, but it's weak. Not a clean motif like "leucine at -5."
**Caveats:** SSE-only matching (not structural). On the same 285 proteins, structurally matched H1 gave 0.279 — slightly lower. Could be that the AA signal is partially a burial proxy (hydrophobic AAs are buried).
**Verdict:** Real but weak. Not the primary feature.

---

### H2: SSE arrangement
**What we tested:** Per-position SSE one-hot (3 × 61) + SSE transition indicators (60) = 243 features.
**Result:** AUPRC 0.394 (2.4× base rate). Second strongest individual.
**Top features:** Coil at center (+), strand at -1 (+), helix at +2 (+). Suggests SSE boundary/junction.
**Caveats:** SSE-only matching. The classifier might pick up on SSE patterns that correlate with burial environments rather than anchor-specific layouts.
**Verdict:** Real signal. SSE layout around the anchor matters. But SSE is a coarse descriptor — 3 labels per position.

---

### H3: Physicochemical profile
**What we tested:** Per-position hydrophobicity, charge, volume, flexibility (4 × 61 = 244 features).
**Result:** AUPRC 0.382 (2.3× base rate). Similar to H2.
**What it means:** There's a physicochemical gradient around anchors. Signal comparable at R=15 and R=30 — the pattern is local.
**Caveats:** SSE-only matching. Hydrophobicity correlates strongly with burial. This might just be a smoother version of "the neighborhood is buried."
**Verdict:** Real but potentially redundant with H4 (burial pattern).

---

### H4_base: Per-position 3D structural context
**What we tested:** Per-position RSA, contacts_8A, contact-with-center, long-range fraction (4 × 61 = 244 features). Structurally matched controls (SSE + RSA + contacts at center).
**Result:** AUPRC 0.488 (2.9× base rate). Strongest individual L1 model.
**Top features:** RSA at nearby positions (-1, +2, +3, +4), contact-with-center at -4, -1, +6, long-range fraction at -3, -15.
**What it means:** The structural properties of the FLANK positions (not center) predict anchorhood. This is the most novel finding.
**Caveats:** Uses PDB features not available to the model. The model computes this from sequence; we're testing whether the property is structural, not whether the model uses these features directly.
**Verdict:** Strong. The flank's structural context is the most informative single feature family.

---

### H4_cluster: Window-level structural summaries
**What we tested:** 16 features describing the structural cluster as a whole (contact density, burial fraction, # contacting positions, cross-SSE contacts, etc.) + 7 H5 features = 23.
**Result:** L1 AUPRC 0.369 (2.2× base rate). GBT 0.537 (3.2× base rate).
**Surprising finding:** contact_density_window is NEGATIVE (-24.3). Anchors have LESS densely connected neighborhoods. mean_rsa_contacting is negative (contacting neighbors are buried). frac_flank_contacting_center is negative (fewer contacts with flank than controls).
**What it means:** Anchors are NOT at dense structural cores. The neighborhood is buried but not tightly interconnected. This contradicts the "dense cluster" hypothesis.
**Caveats:** L1 with 23 features — the negative coefficients might be picking up confounds. The GBT >> L1 gap (0.537 vs 0.369) is large, meaning these features interact nonlinearly.
**Verdict:** The cluster description carries real signal but the story isn't "dense cluster." The relationships are nonlinear and hard to interpret linearly.

---

### H4_bridge: Bridge topology features
**What we tested:** 4 graph-theoretic features (frac_nonredundant_contacts, n_components_without_center, betweenness_in_window, bridge_score) + 7 H5.
**Result:** L1 AUPRC 0.201 (barely above base rate). GBT 0.423 (2.5× base rate).
**Coefficient signs:** bridge_score positive (removing center disconnects graph — good), frac_nonredundant_contacts positive (contacts don't contact each other — good), betweenness NEGATIVE (contradicts naive bridge expectation).
**What it means:** The bridge features are genuinely nonlinear — L1 can't use them at all, but GBT gets 2.5× base rate from 11 features. The bridge description partially works but not in a clean linear way.
**Caveats:** Only 11 features. The negative betweenness is confusing. These features are computed on a small subgraph (±30 residues) which may not capture the relevant topology.
**Verdict:** The bridge concept is partially right (nonredundant contacts, disconnection on removal) but the linear story doesn't hold. Something more complex is going on.

---

### H5: Positional context
**What we tested:** 7 features (fraction position, distance to termini, position in SSE, SSE segment length, transitions in window).
**Result:** AUPRC 0.182 (≈ base rate). NULL.
**But:** pos_in_sse was GBT's #2 feature when combined with other features. It matters in interactions, not alone.
**Verdict:** Dead as standalone. Useful as helper in nonlinear models.

---

### Combined models

| Model | L1 AUPRC | GBT AUPRC |
|---|---|---|
| H4_base | 0.488 | — |
| H4+ (all structural + cluster + bridge + H5) | 0.502 | 0.651 |
| FULL (all H1-H5 combined) | 0.563 | 0.727 |

The FULL GBT at 0.727 is the ceiling we've found. It uses ALL features nonlinearly.

---

## Part 2: What's the honest assessment?

### What we've learned
1. The flank's structural context is the most informative single feature family (H4)
2. Anchors are buried but NOT in dense clusters — they have buried but loosely connected neighborhoods
3. There are genuine nonlinear interactions between features (GBT >> L1 consistently)
4. No single structural description cleanly captures the anchor property

### What feels wrong
The tea-leaves problem is real. We keep adding features and getting modest gains. The GBT nonlinearity means we're always saying "there are interactions we can't name." The per-position H4 features (AUPRC 0.488) are doing most of the linear work, and everything else adds noise or nonlinear signal we can't interpret.

The fundamental issue: **we're trying to describe a learned nonlinear function using handcrafted linear descriptors.** The model computes something from the flank that doesn't decompose into any clean set of structural features we've tried. Each feature captures a piece, but the pieces don't add up to a clean story.

---

## Part 3: What features / hypotheses are we MISSING?

### A. Coevolutionary / conservation features
**What:** Are anchor positions conserved? Are they at positions of high coevolutionary coupling? Do the flank positions that matter have correlated mutations with the center?
**Why missing:** We don't have MSA data computed for all 500 proteins. Conservation scores exist for a subset.
**Why it matters:** Zhang et al.'s whole thesis is that the model learns coevolutionary statistics. If anchors are at positions of high evolutionary coupling with their flanks, that directly supports "the model reads coevolutionary patterns." We have conservation data for some proteins from earlier experiments (anchor_regression_v3 had conservation for ~1252 residues across a subset).
**Prediction:** If conservation/coupling predicts anchorhood, the answer is "sequence identity" (the model recognizes evolutionarily conserved positions). If it doesn't, the answer leans "geometric logic."

### B. Information-theoretic features of the sequence
**What:** Local Shannon entropy of the sequence around the anchor. Mutual information between center AA and flank AAs across the protein dataset. Essentially: how predictable is the anchor's identity from its flank, and vice versa?
**Why missing:** We tested AA identity (H1) but not the STATISTICAL REGULARITY of the AA pattern. H1 asks "is there a specific AA at position +5?" but not "is the center's AA unusually predictable from its flank?"
**Why it matters:** If the model is doing something like "this position's identity is highly constrained by its local context" — that's exactly what masked LM training optimizes for. The anchor might be the position in the flank window with the highest mutual information with its neighbors. This would be a very clean answer: the model selects positions that are maximally informative about their local context.
**How to compute:** For each position, compute the empirical mutual information between that position's AA and its flank AAs across the 500 proteins. Or simpler: use the ESM log-likelihood under masking as a proxy — positions where the model is most confident given the flank.

### C. ESM's own confidence as a feature
**What:** Instead of handcrafted features, use the model's OWN masked prediction confidence at each position as a feature. Mask position j, let ESM predict, measure entropy/confidence. Then: do anchors have different prediction-confidence profiles in their flanks?
**Why missing:** We've been using PDB-derived features. But the model doesn't see PDB data — it sees sequence and computes internal representations. The model's own confidence profile IS the feature it computes.
**Why it matters:** This bypasses the handcrafted feature problem entirely. If anchor flanks have distinctive ESM-confidence profiles, that tells us the model is detecting a pattern in its own prediction landscape, not a pattern in structural descriptors.
**Caveat:** This is circular if we're not careful. The model selects anchors → the anchor's flank must have properties that the model can detect → the model's confidence at flank positions reflects those properties. But it could still be informative about WHAT the pattern is.

### D. Packing geometry (beyond contacts)
**What:** Contact NUMBER is crude. What about the GEOMETRY of packing? Voronoi tessellation, packing density, local void volume, coordination geometry (tetrahedral, octahedral, irregular). Are anchors at positions with specific packing geometries?
**Why missing:** These require more sophisticated structural analysis than simple contact counting.
**Why it matters:** "Buried" and "many contacts" are rough descriptors. Two positions with identical RSA and contact count can have very different packing environments. If anchors favor specific packing geometries, that's a cleaner structural description.

### E. Sequence-structure mismatch features  
**What:** Positions where the sequence seems "wrong" for the structural context — e.g., a polar residue in a position that's structurally buried, or a hydrophobic residue in an exposed position. The MISMATCH between expected and observed properties.
**Why it matters:** These positions might be under strong evolutionary constraint from structure. The model might detect them as "interesting" because they violate sequence-structure correlations.
**How to compute:** Residuals from a simple sequence→structure regression (e.g., hydrophobicity should predict RSA, deviations from this are mismatches).

---

## Part 4: Experiments to differentiate sequence identity vs geometric logic

The classification approach gives us partial answers but can't cleanly separate the two hypotheses. Here are experiments that directly pit them against each other.

### Experiment A: Scramble sequence, preserve structure
**Design:** Take the ±30 flank around the anchor. Create a scrambled version where:
- AA identities are randomly permuted WITHIN each SSE segment (preserving which AAs are in strand/helix/coil but destroying their specific positions)
- SSE assignments are preserved
- Feed the scrambled sequence to ESM and measure anchor projection alpha

**What it tests:** If alpha drops sharply, the model needs the SPECIFIC AA arrangement (sequence identity matters). If alpha is preserved, the model only needs the general AA composition per SSE (geometric logic — the SSE layout is enough).

**Variants:**
- Scramble within SSE segments (preserves composition per SSE)
- Scramble across whole flank (destroys everything except global composition)
- Scramble only buried positions (tests if buried residues need specific identities)
- Scramble only exposed positions

This directly separates "which AAs are where" from "what's the structural layout."

### Experiment B: Homolog replacement
**Design:** For proteins with known homologs (different sequence, same fold):
- Take the anchor from protein A
- Replace protein A's flank with the corresponding region from homolog B (aligned by structure)
- Run ESM, measure alpha

**What it tests:** If alpha is preserved with the homolog's sequence, the model detects a fold-level geometric property (same fold → same anchor). If alpha drops, the model needs the specific sequence (sequence identity).

**Caveat:** Requires structural alignment between homologs. Limited to proteins with good homologs.

### Experiment C: Synthetic structural contexts
**Design:** Take a known anchor and construct synthetic flanks with:
- Same RSA profile but random AA sequence
- Same AA sequence but randomized RSA profile (impossible to construct directly, but could use different proteins with similar sequences but different structures)
- Matched structural features but different fold

**What it tests:** Which aspect of the flank the model is reading — the sequence pattern or the structural pattern (as encoded in sequence).

### Experiment D: Per-position ablation WITH structural annotation
**Design:** This is Experiment 3 (position importance maps) but with structural annotation. For each flank position, compute its importance (leave-one-out masking). Then ask:
- Do important positions tend to be in 3D contact with the center?
- Do they tend to be at SSE boundaries?
- Do they tend to be conserved?
- Do they tend to have specific AA types?

**What it tests:** What the model actually READS from the flank. If important positions are structurally connected to the center, the model is doing geometric logic. If important positions have conserved AAs, the model is reading sequence identity.

**This might be the cleanest experiment.** It directly maps "what the model uses" to structural vs sequence properties. And it doesn't require handcrafted features to predict anything — it observes what the model does.

### Experiment E: Mutate the anchor, measure flank response
**Design:** Mutate the anchor position to different AAs. For each mutation, measure:
- Does the anchor's projection alpha change?
- Which mutations kill the anchor signal?
- Are the mutations that kill the signal the ones that disrupt the structural property (change burial, break contacts) or the ones that change sequence identity (conservative substitutions like L→I shouldn't matter if it's geometric)?

**What it tests:** If conservative substitutions (L→I, V→A, same physical properties) preserve the anchor but non-conservative ones kill it, it's geometric. If SPECIFIC AAs matter regardless of properties, it's sequence identity.

---

## Part 5: Recommended priority

### For the paper (next 3 weeks)
1. **Experiment D (position importance + structural annotation)** — highest signal/effort ratio. Directly answers "what does the model read from the flank" without requiring feature engineering. Cross-validates Exp 1 and Exp 2.
2. **Experiment A (scramble within SSE)** — directly pits sequence identity vs geometric logic. Fast to implement (just shuffle AAs and re-run ESM). Produces a clean binary result.
3. **Start writing** — the outline is ready. The core results (universality, matched controls, flank jump, upstream circuit, H4 classification) are solid regardless of these additional experiments.

### Lower priority
4. Feature B (conservation/coevolution) — informative but requires MSA computation at scale.
5. Feature C (ESM confidence profiles) — interesting but somewhat circular.
6. Experiment E (mutations) — good but slower to implement and analyze.

### Skip
- More handcrafted structural features. We've hit diminishing returns. The GBT ceiling tells us the signal is there but the linear feature approach won't crack it.
- MLP L9 interpretation. Future work.
- Packing geometry analysis. Too specialized for the timeline.
