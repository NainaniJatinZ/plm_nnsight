Read and understand @contact_pattern_v2 
Currently we are discovering the circuit for predicting contacts between two segments. As each is around 11 AA long, the patching metric is averaging over 121 cells. 
But in the contact map, only ~4 contacts really are high, and those are the ones that change the most between clean and corrupted. 
So lets create a new script or add a flag to this one that allows circuit discovery (the same head, then cell attr and then motif analysis) but for each contact on its own. 