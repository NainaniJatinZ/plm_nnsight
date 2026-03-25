
The fact that L32H13 appears in 31/31 circuits, and there's a clean core of 25 heads shared across diverse proteins — that's not a property of any individual protein's circuit. That's a property of ESM2 itself. You've found that ESM2 has a universal contact prediction module. And your observation that anchor heads (L10H9, L11H16, L14H9) are among the most recurring while diagonal/motif heads are protein-specific is the key structural insight: the model separates general-purpose computation (anchoring, interaction) from protein-specific computation (local motif recognition).
This is directly analogous to the induction head story in language models — universal computational primitives that implement the same algorithm regardless of input content. Anchor heads are ESM2's version of this: a universal "find the relevant position and broadcast information from it" operation.

Now the main question: the same head (say L11H16) anchors on G163 in 2B61A, K129 in 1YKIA, F47 in 2FBQA, A218 in 1IN4A. Why? What is it looking for?. Something in the residual stream at that position, computed by earlier layers, that the head's key matrix picks up on. This is exactly where the SVD analysis matters, and why it's the right next step rather than more biological annotation.

Here's the SVD experiment concretely:
For a vertical-stripe head like L11H16, the attention pattern means:
softmax(Q @ K^T) has one column dominating
→ one key vector k_anchor has much higher dot product with all queries than any other key
→ either k_anchor has large norm, or it aligns with the dominant direction that all queries share
So the experiment is:
Step 1: For L11H16, across several proteins, compute k_j = W_K @ residual_stream[j] for every position j. Confirm that ||k_anchor|| is much larger than other positions, or that k_anchor projects most strongly onto the top right-singular vector of W_K. This tells you what direction in key space the head selects for.
Step 2: Project the anchor position's residual stream back through W_K to find what direction in residual stream space produces the large key. Call this the "anchor direction." Now you have a vector in residual stream space that you can probe: does it correlate with SSE encoding? With outputs of specific earlier heads? With the embedding of specific amino acids?
Step 3: Compare the anchor direction across proteins. If the same direction in key space is activated by G163 in 2B61A and K129 in 1YKIA, then those residues share a representational feature that isn't visible in their biological properties but is visible in the model's internal representation. That's the finding — the model has learned an abstract feature that identifies "useful relay positions" and anchor heads select for it.

the previous experiments related to this are in 
- scripts/anchor_interp.py (looking at all )
- scripts/circuit_head_overlap.py
- scripts/head_deep_dive.py