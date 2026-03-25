we discovered attention circuits from contact_pattern_v2.py

we then did head level overlap in scripts/circuit_head_overlap.py

from there we found that L10H9 and L11H16 are recurring in around 22+ / 31 of the proteins and have vertical ish attention patterns.

we did the anchor experiment before scripts/anchor_decomp.py to check for some svd stuff that wasnt successful. 

We now want to use the SAEs we get from interprot, use this script as example to test it @scripts/interprot_sae_viz.py

For a protein like 2B61A and a head like 10H9, find the latents in layer 8 and layer 12. We should get the causal cells in the head - ithink the circuit size was like 2k cells. 

For layer 8, we want to find the latent-token pairs that influence the contact prediction through the head 

for layer 12, we want to find the latent-token pairs that get influenced by the change in causal cells of the head to influence the contact prediction. 


here is some pseudo code for this :
Yes. For your goal, strip it down.
We care about **the head as a mechanism**, not the final contact readout. So the two things to do are:

## 1. Upstream edge attribution

**Layer-8 SAE latents → target head Q/K**

Use EAP-style edge attribution from each layer-8 latent-position pair into the **Q and K inputs** of your target head. This is the right upstream object because attention cells are determined primarily by Q and K. Attribution patching is exactly a first-order edge approximation using clean-minus-corrupted activation change times gradient.

Use this target scalar:

[
y_{\text{head}} = \sum_{q,k} w_{qk}, A_H[q,k]
]

where (A_H) is the target head’s attention pattern and (w_{qk}) is:

* 1 on the cells you care about, 0 elsewhere, or
* a soft weighting if you want.

Then score edges:

[
\text{AttrUpQ}(p,f,q)
=====================

\Delta e^{Q}*{(p,f)\to q}
\cdot
\frac{\partial y*{\text{head}}}{\partial e^{Q}_{(p,f)\to q}}
]

[
\text{AttrUpK}(p,f,k)
=====================

\Delta e^{K}*{(p,f)\to k}
\cdot
\frac{\partial y*{\text{head}}}{\partial e^{K}_{(p,f)\to k}}
]

where ((p,f)) is a layer-8 latent at position (p), latent (f).

This gives you:

* which layer-8 latents matter
* at which token positions
* through Q or through K
* for your head

That is the first thing.

---

## 2. Downstream edge attribution

**Target head output → layer-12 SAE latents**

Do **not** patch cells one by one. You are right, that is not the right first move here.

Instead, treat the **entire target head output at all positions** as the source, and do edge attribution from that head’s output into layer-12 SAE latents.

So now the source is:

* target head (H) output at position (t)

and the target is:

* layer-12 latent ((p,f))

Use the corrupted run as base, clean run as source, and score:

[
\text{AttrDown}(t \to p,f)
==========================

\Delta e_{H_t \to z_{12}[p,f]}
\cdot
\frac{\partial y_{\text{down}}}{\partial e_{H_t \to z_{12}[p,f]}}
]

But here, to keep it simple, set the downstream scalar to just the latent activation itself:

[
y_{\text{down}} = z_{12}[p,f]
]

Then the gradient term becomes just sensitivity of that latent to the head-output edge.

In practice, you do this in matrix form for **all** layer-12 latents at once.

So yes, your instinct is right:

* you do **not** need to restrict to the 20 cells downstream
* you can use the **whole head output**
* and get token-level downstream information into SAE latents

That is much easier.

---

# The two things you should do

## A. Upstream

**Layer-8 SAE latents → target head Q/K**

This tells you what creates the head’s behavior.

## B. Downstream

**Target head output → layer-12 SAE latents**

This tells you what the head writes into later computation.

That is the clean end-to-end story for understanding the head.

---

# Why this is better

Because it matches the actual causal roles:

* **upstream of attention pattern**: Q/K matter most
* **downstream of the head**: the head affects later computation through its **output vector writes**, not through its own attention pattern

So your graph is:

[
\text{layer-8 SAE latents}
\to
Q/K \text{ of target head}
\to
\text{target head behavior}
\to
\text{target head output}
\to
\text{layer-12 SAE latents}
]

That is much cleaner than trying to force cells into both halves.
---

# The simplest pseudocode sketch

## 1. Upstream: layer-8 latents to head Q/K

```python
# clean and corrupted runs
z8_clean = sae8.encode(resid_layer8(clean))      # [seq, F8]
z8_corr  = sae8.encode(resid_layer8(corr))       # [seq, F8]

# target head quantities on corrupted run
Q_corr, K_corr, A_corr = get_head_qka(corr, target_head)
retain_grad(Q_corr)
retain_grad(K_corr)

# scalar describing the head cells you care about
y_head = weighted_sum(A_corr, cell_weights)      # can be sparse over known cells
y_head.backward()

# latent decoder writes
# decoder8[f] is [d_model]
# latent write from (p,f) is z8[p,f] * decoder8[f]

for p in positions:
    for f in latents8:
        u_clean = z8_clean[p,f] * decoder8[f]
        u_corr  = z8_corr[p,f]  * decoder8[f]

        delta_q = (u_clean - u_corr) @ W_Q[target_head]   # [d_head]
        delta_k = (u_clean - u_corr) @ W_K[target_head]   # [d_head]

        # aggregate over query/key positions
        score_q[p,f] = sum_q( delta_q · grad_Q[q] )
        score_k[p,f] = sum_k( delta_k · grad_K[k] )
```

This gives you top layer-8 latent-position pairs for Q-side and K-side influence.

---

## 2. Downstream: head output to layer-12 latents

```python
# clean and corrupted head outputs
hout_clean = get_head_output(clean, target_head)   # [seq, d_model]
hout_corr  = get_head_output(corr, target_head)    # [seq, d_model]
delta_hout = hout_clean - hout_corr                # [seq, d_model]

# corrupted run to layer 12 SAE
z12_corr = sae12.encode(resid_layer12(corr))       # [seq, F12]

# we want influence on all downstream latents
# do this one latent at a time conceptually, batched in practice
for p in positions12:
    for f in latents12:
        zero_grads()
        y_down = z12_corr[p,f]
        y_down.backward(retain_graph=True)

        # grad wrt target head output at all source positions
        grad_hout = grad_of_head_output(target_head)   # [seq, d_model]

        for t in source_positions:
            score_down[t,p,f] = delta_hout[t] · grad_hout[t]
```

This gives you:

* which token positions of the head output matter
* which layer-12 latents they affect

In practice you would batch over many ((p,f)), but this is the conceptual pseudocode.

---

# My recommendation

Do exactly these two analyses:

### Upstream

**latent → Q/K**
with target scalar = weighted attention mass on the head cells you care about

### Downstream

**head output → layer-12 latents**
with target scalar = downstream latent activation

That is the cleanest possible head-centric decomposition.

If you want, I can turn this into cleaner research-note pseudocode with exact tensor shapes and aggregation choices.

---- 

# Plan feedback

The overall structure is good, but there are a couple of places where the math and the engineering target are drifting apart. The biggest issues are the LayerNorm handling, the positional indexing for upstream Q/K attribution, and the downstream “analytical EAP” being too coarse if your goal is truly head-specific. 

The main thing I would keep is the split:

* upstream: layer-8 SAE latents → target head Q/K
* downstream: target head output → layer-12 SAE latents

That is the right decomposition for understanding the head. 

What I would change:

First, for the upstream metric choice, doing both is good, but I would make **contact** the default ranking and **head-local** the diagnostic ranking. That part of the plan is fine. Where I’d be careful is the construction of `cell_weights` as `|clean - corrupt|` restricted to the contact segment. That is okay for a diagnostic mask, but it should not quietly define “causal cells.” It defines “cells that changed,” which is not the same thing. If you already have a known list of causally relevant cells from prior patching, the script should accept those explicitly and only fall back to the diff-based weights when none are provided. We get the cells from the contact_pattern_v2 script right? 

Second, the upstream score formula currently looks wrong in one important way. The plan says:
`score_q[p,f] = delta_resid[p] @ grad_resid_Q[0, p]`
and similarly for K. 

That only makes sense if the latent at position `p` can only influence the query/key at the **same** position `p`. For Q and K of a later head, that is usually true only if the target layer directly reads from the residual at that same position. So:

* for **Q at query position q**, only the latent at **position q** should contribute directly
* for **K at key position k**, only the latent at **position k** should contribute directly

That means the correct aggregation should be position-aware:

* Q-side attribution should use gradients at query positions
* K-side attribution should use gradients at key positions

So instead of one `score_q[p,f]` from all positions, it should really be something like:

* `score_q[q,f]` for latent at position `q` affecting Q at position `q`
* `score_k[k,f]` for latent at position `k` affecting K at position `k`

Then aggregate over the cell set afterward. The current plan is too collapsed and risks mixing query-side and key-side roles. That is the single biggest change I’d request.

Third, the LayerNorm correction is too hand-wavy right now. The plan says “simplified LN Jacobian” using `1/std`. 
That may be fine as a rough approximation, but if this is going to be a serious analysis, you should either:

* explicitly label it as an approximation and provide a flag to disable it, or
* derive the exact linearized mapping actually used by your SAE normalization convention and the model’s pre-attn LN

I would not present `1/std` as if it were the exact Jacobian. For ranking, it may still work fine, but it is a place where people can poke holes.

Fourth, on the downstream side, I would slightly tighten the interpretation. The plan computes:

* clean/corrupt head context
* projects through `W_O`
* gets `delta_hout`
* then scores downstream SAE latents using encoder directions. 

Conceptually this is good. But two caveats:

1. this is a **direct residual-path approximation**, not the full downstream effect of the head through all later nonlinear computation
2. it is head-output to downstream-SAE attribution, not cell-specific downstream attribution

That is actually okay, and I think it matches your stated goal better than per-cell downstream patching. I would just rename it more explicitly to something like:

* “direct downstream write attribution”
  instead of “analytical EAP” in a broad sense

That will keep expectations clear.

Fifth, I would add one missing validation: for the **top upstream latents**, do a small number of actual patches. Not thousands, just maybe top 10 or 20. Same for downstream top latents. This is important because attribution alone can drift. The plan already has reconstruction and score-mass checks, which are good, but a tiny causal validation set would make the results much more trustworthy. 

Sixth, I would change the “mask to active latents” rule downstream. Right now it says:

* active if `z_down_clean > 0 or z_down_corr > 0` 

That is a decent filter, but I’d prefer:

* keep all scores in the saved tensor
* only filter for reporting
* and maybe report both “all-latent rank” and “active-latent rank”

Otherwise you may accidentally hide useful negative or near-threshold effects.

Seventh, I would add one output that will help you a lot later:

* for upstream, save separate tensors for Q-side and K-side scores before summing
* for downstream, save score by source position as well as aggregated over source positions

The plan mentions reporting Q vs K contribution, which is good. I’d make that mandatory in the saved artifact too. 

So my concise recommended edits are:

1. Accept explicit causal-cell lists, and use diff-based `cell_weights` only as fallback.
2. Fix upstream indexing so Q uses query positions and K uses key positions, instead of one same-position formula for everything.
3. Mark LN correction as approximate, not exact.
4. Rename downstream method to emphasize it is direct-write attribution, not the full downstream effect.
5. Add a tiny actual-patching validation on top-ranked upstream and downstream items.
6. Save unfiltered score tensors, and only filter latents for reporting.
7. Save Q and K score tensors separately.


