

prev experiment @experiments/3_23_anchor_decomp.md
scripts:
- @scripts/anchor_decomp.py - Anchor decomposition via SVD of per-head key projection matrices.
- @scripts/anchor_interp.py - Anchor residue interpretation for contact pattern analysis.


i am interested in these approximate questions / directions:

why do all of the head's queries attend to the single key? / how does the model decide which key to attend to? / what property / information is present?
what information is this head writing to the interaction heads?
what information is the head reading to decide the key to attend to?


**Question 1: Why does the anchor key win the attention competition?**

We've been testing properties of the anchor *residue*. The SVD showed it's not key norm (especially for L10H9 where anchors have below-average norm). But we haven't asked the simpler question: what direction are all the queries looking for, and why does the anchor key match it best?

The experiment: for a vertical-stripe head like L11H16 on a specific protein, compute all query vectors `q_i = W_Q @ x_i` and all key vectors `k_j = W_K @ x_j`. Compute the mean query direction `q_mean = mean(q_i / ||q_i||)`. Then project all key vectors onto this direction: `score_j = k_j · q_mean`. The anchor should have the highest (or near-highest) projection. That tells you that the anchor wins not because of anything special about itself in isolation, but because it aligns best with a direction that the queries universally share.

Then the deeper question becomes: where does that shared query direction come from? Is it present in the residual stream before this layer (meaning it was written by earlier computation), or is it mostly from W_Q itself (meaning it's a fixed property of the head)? You can check this by looking at whether `q_mean` in head space corresponds to a consistent direction in residual stream space across proteins. If `W_Q^T @ q_mean` is similar across proteins, the head has a fixed "search direction" and the anchor just happens to be the best match. If it varies per protein, the query direction is computed from context.

This is different from the SVD experiment you already ran because that decomposed W_K in isolation. This looks at the actual QK interaction on real inputs — what direction the queries are searching in and why the anchor key matches.

**Question 2: What information does the head write?**

Since attention is concentrated on the anchor, the output is approximately `W_O @ W_V @ x_anchor`, written to every query position (weighted by attention). So this head is broadcasting some transformation of the anchor position's residual stream to many positions in the sequence.

The experiment: for each protein, compute `output = W_O @ W_V @ x_anchor_ln` (the actual OV output from reading the anchor). Then ask:

First, *where* is it written? Weight by attention — positions with highest attention get the most output. Are those positions in SS1, SS2, flanks, everywhere?

Second, *what* is written? Take the output vector and probe it. Project it onto the W_K and W_Q input spaces of the interaction heads. If `W_K_interaction @ output` is large, the anchor head is making the destination position a better *key* for interaction heads. If `W_Q_interaction @ output` is large, it's changing what the destination *queries* for in interaction heads. This directly tells you how the information transfer to interaction heads works.

Third, compare the OV output across proteins. Is `W_O @ W_V @ x_anchor` similar across proteins despite the anchor being a completely different residue? If yes, the head extracts the same abstract feature regardless of which residue it reads from. If no, it's passing protein-specific information.

This is purely activation-based, cheap (one forward pass per protein you already have cached), and directly answers "what information goes downstream."
