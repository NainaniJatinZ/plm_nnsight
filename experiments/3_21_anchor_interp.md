read and understand @contact_pattern_v2.py

For the test protein of 2B61A, we get an output report like this @reports/outputs/2B61A/2B61A_contact_report.md 

You can see some anchors here. we want to understand if there are any patterns which residues are selected as anchors. 

We have conservation scores from @data/2B61A_EV/TARGET_b0.3/align/TARGET_b0.3_frequencies.csv

we can also get SSE annotation from either the pdb file @data/2B61A_EV/TARGET_b0.3/2b61.pdb or this file: @data/ss_dict.json by indexing as "2B61A.pdb" 

Basically for each residue that acts as an anchor, we want to know which heads it acting that for, whether its k or q for each, that residues conservation score, SSE assignment (H/E/C), position within the SSE (boundary vs interior), whether it's a jump residue, and maybe solvent accessibility from the crystal structure.

The tensors will have a CLS token, where as most strings and will be 0 indexed so be careful. 

Set up the experiment such that it can be easily done over other proteins if needed. 

You can make as many test scripts as you want in testing/ dir and the final script to be inside scripts/ dir. 


----

update: coupling logic

The current tables mix two very different things: residues that are hubs because they're at the contact computation site (I181/T315 in 2B61A, V101/V201 in 1PVGA) and residues that are hubs because they're relay stations in the flanking region (G163 in 2B61A, K129 in 1YKIA, A218 in 1IN4A). These are doing different jobs. The contact-site hubs are expected and uninteresting — of course the model concentrates computation at the positions it's predicting contacts for. The flank hubs are the ones that could tell us something.

I think the first thing to do is split the analysis: separate anchors into "contact-site" (within or immediately adjacent to SS1/SS2) and "flank" (outside both segments). Then only analyze the flank anchors for the coupling hypothesis.

The pairwise coupling scores are what you want, not the enrichment. The hypothesis is specific: flank anchor residues have higher coupling scores with the contact pair residues than non-anchor flank residues do. So for each protein, you'd take every residue in the flanking region, look up its coupling score with the contact pair positions (e.g., for 2B61A, coupling of residue X with positions 182 and 316), then compare anchor vs. non-anchor distributions.

use the files like @data/2B61A_EV/TARGET_b0.3/couplings/TARGET_b0.3_CouplingScores.csv 


The minimal experiment I'd propose:
For each of the proteins:

Take all flank residues (everything in the unmasked region but outside SS1/SS2)
For each, compute max coupling score to any contact pair residue (using the pairwise score or fn column from your coupling CSV)
Label each as anchor (appears in the anchor table) or non-anchor
Compare the two distributions — even just a rank-sum test or a simple scatter of coupling score vs. n_heads

If flank anchors consistently sit in the top quartile of coupling-to-contact scores, that's a finding. If it's mixed, coupling isn't the story.