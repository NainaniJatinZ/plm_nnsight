We get causally relevant attention patterns from @contact_pattern_v2.py, and we also know the cells in the attention patterns that are sufficient to hit a faithfulness score. 

I want to look for "interaction heads" - heads whose attention patterns in general or the causally relevant cells line up or coincide with the coupling we have from EVCoupling. 

We can use the 2b61A protein as the testcase. The EVcouplings output for the protein are in data/TARGET_b0.3/couplings/TARGET_b0.3_CouplingScores.csv 

Can you write a script in scripts/ dir that does this analyses and for each of the heads in the circuit shows me if any at all match with the coupling effects?

You can see how we get the cached attn patterns from @attn_viz_app.py, be careful of the indexing because of the CLS token. The coupling has the AAs for the indices for you to cross check the correct indexing for tensors. 