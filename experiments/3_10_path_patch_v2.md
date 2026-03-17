# goal: fix previously implemented attention path patching

previously we had implemented path attribution patching between attention output as src and attention input (query / key) as dst. That attempt is present here: scripts/attr_patching.py (look for section "Part 3: Path-level Attribution Patching (head output → head Q/K input)")

This attempt wasn't successful, by that I mean the sufficiency test wasn't good. It was taking too many heads to recover performance, worse than the number of heads we get when doing head level act patch. 


Actual path patching, that seemed to be working, is present here: scripts/path_patching.py

Cell level attribution patching that is also working: contact_pattern_v2.py 

the contact_pattern_v2.py is the main script right now. Here's overview of the file: 
contact_pattern_v2.py desc
Indirect effects: 660-trace patching to rank heads
Circuit discovery: greedy unpatching sweep
Gradient attribution: one forward+backward to score every cell
Sufficiency: protect top-K cells, corrupt rest
Motif extraction for the identified circuit heads - finds anchors in key / query or both, finds positional or intra region heads or cross region heads (regions include left flank, sse1, sse2, right flank)
Markdown report
contact_pattern_v2.py outputs
Ran over the first 10 proteins 
A significant portion of the circuit has anchors on the keys or queries across proteins. Some anchors gather information on motifs (tokens close to each other) while others the tokens to the anchor are spread across the sequence.  

One thing we remembered during cell level attribution is that we have to get both attribution for indirect cells and direct cells. My primary hypothesis is that the same issue exists in the path attr stuff? We also need to compare the way we do attr calc between cell level and the path. 

For the test case, the outputs for the protein 2B61A for contact_pattern_v2 script is a good benchmark. We can compare the sufficiency / faithfulness scores we get from the path attr to the number of heads we get from head level patching and the cell level attr to hit 70% of the metric. 