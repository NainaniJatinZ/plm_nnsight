# Anchor Local Flank Classification v4: H4+ with Cluster Features

Run date: 2026-04-05 17:19

Proteins with PDB: 488, PDB features computed: 488

Radius: 30, Controls per anchor: 5

Structural control pairs: 2386


## Results

Model                     N_prot   N_feat   Base     AUPRC    AUROC    BalAcc  
---------------------------------------------------------------------------------
H4_base_L1                483      244      0.1684   0.4878   0.8211   0.7490  
H4_plus_L1                483      271      0.1684   0.5020   0.8306   0.7673  
H4_cluster_only_L1        483      23       0.1684   0.3690   0.7557   0.6934  
H4_bridge_L1              483      255      0.1684   0.4942   0.8230   0.7575  
H4_bridge_only_L1         483      11       0.1684   0.2009   0.5822   0.5525  
H4_plus_GBT                                 nan      0.6512   0.8792   0.7796  
H4_cluster_only_GBT                         nan      0.5372   0.8287   0.7441  
H4_bridge_GBT                               nan      0.6585   0.8813   0.7829  
H4_bridge_only_GBT                          nan      0.4232   0.7722   0.7017  

Permutation test (H4+): p=0.0000, null 95th pctl=0.1830

## Feature Family Ablation (H4+)

Family                         AUPRC    Drop      
------------------------------------------------
contact_cluster (1-7)          0.4922   +0.0098
burial_pattern (8-11)          0.5056   -0.0036
contact_density (12-14)        0.4997   +0.0023
spatial_dist (15-16)           0.5051   -0.0031
H5_helper (17-23)              0.4950   +0.0070
bridge_topology                0.5035   -0.0015

## Interpretation

MODERATE SUCCESS: H4+ L1 in 0.50-0.55 range, cluster features modestly improve over H4_base.
H4_cluster_only AUPRC=0.369 > 0.30: cluster description alone carries signal.

H4_bridge L1 AUPRC=0.494 (base + bridge + H5).
Bridge features do not improve over cluster features when added to per-position base.
H4_bridge_only L1 AUPRC=0.201 (bridge + H5 only, 11 features).
