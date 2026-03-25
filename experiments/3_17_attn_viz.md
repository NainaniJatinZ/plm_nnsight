Read and understand @contact_pattern_v2.py . I want to visualize and understand the attention patterns that are in the circuit for each protein. We have ran this script for a few proteins. Before writing this, we had a attention viz as an html but only for the protein 2B61A and it was super hardcoded and cached and stuff. You can see it in the reports/attention_viz_table.html.

I want a better interface - I want it to be able to switch between proteins, have attention patterns for the heads that are in the circuit, switch between different indices for queries and keys

For regions, we want options of 
- seq_l * seq_l
- flank_left x flank_right 
- flank_right x flank_left 
- flank_left x flank_left
- flank_right x flank_right

for each we want 
- attention on full sequence 
- attention on clean sequence 
- attention on corrupted sequence 
- attention diff between clean and corrupted 

and for that head, 
lets just print the cells 

For this, I am fine with calculating things online and then saving it or do whatever it takes like streamlit or sticking with html. I want to reach this viz and generate hypotheses about these patterns! 