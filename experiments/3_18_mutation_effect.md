We have the contact prediction counterfactual setup in @contact_pattern_v2. Basically, full sequence generates the baseline contacts for 2 long range SSEs defined by the mid indices. 

We have the flanking setup, we gradually unmask residues from the SSEs in an outward fashion. At the corrupted flank length, the contact recovery is low. And then increasing it by 1, the clean flank length, the recovery jumps by >0.5. 

We want to understand the probability distribution of the residues in long range contacts over these three sequences - full, clean, corrupted. 

Background: Zhang et al. [1] proposed that protein language models rely mainly on coevolution signals to predict contacts by showing that a categorical jacobian achieves high contact acc and its similarity to MSA based methods. Additionally, this jump is used by them as evidence that the model learns the coupling signals conditioned on a motif / sequence identity. 

Hypothesis: If the coupling signals is locked behind the residues unmasked in the clean input, and according to Hopf et al. [2], mutation effects can be predicted by seq co variation. Then, the masked token probability distribution for the residues in long range contact should shift significantly between the clean and corrupted sequences.  

Steps:
1. setup the initial bits and get the contact pred jump 
2. for the clean sequence, find the residues in long range contact between SS1 and SS2 - there should be around 4 contacts 
3. Flatten the pairs into a list of residues - add I157, G159, G163, and 326 into the mix
4. For each residue, we are going to do the forward pass for the 3 sequences we have - full, clean and corr; but we will mask the residue in question and look at the probability distribution of that token between the three sequences. 
5. Separately, we also want to see the masked token prob distribution for the jump residues (residues unmasked only in clean, F365/I133) under the corrupted sequence and the full sequence (mask the JRs but everything else unmasked)

Gotchas:
1. indices are weird, be careful of the cls token at the start. stay consistent in how you annotate the contact matrices and sequences 


References:
[1] Zhang, Zhidian, et al. "Protein language models learn evolutionary statistics of interacting sequence motifs." _Proceedings of the National Academy of Sciences_ 121.45 (2024): e2406285121.
[2] Hopf, Thomas A., et al. "Mutation effects predicted from sequence co-variation." _Nature biotechnology_ 35.2 (2017): 128-135.  https://www.nature.com/articles/nbt.3769