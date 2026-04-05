# Anchor Local Flank Classification v3

Run date: 2026-04-05 14:13

Proteins (all): 500, Proteins (with PDB): 500, PDB features computed: 488

Primary radius: 30, Secondary radius: 15

Controls per anchor: 5

SSE-only control pairs: 2500, Structural control pairs: 2386


## Results

Model                Matching        N_prot   N_feat   Base     AUPRC    AUROC    BalAcc  
---------------------------------------------------------------------------------------------
H1                   sse_only        500      1220     0.1667   0.3203   0.6930   0.6168  
H2                   sse_only        500      243      0.1667   0.3936   0.7738   0.7018  
H3                   sse_only        500      244      0.1667   0.3816   0.7314   0.6650  
H4                   structural      483      244      0.1684   0.4878   0.8211   0.7490  
H5                   sse_only        500      7        0.1667   0.1818   0.5498   0.5282  
FULL                 sse_only        500      1958     0.1667   0.5632   0.8355   0.7346  
GBT_FULL             sse_only                          nan      0.7272   0.9147   0.8048  
H1_R15               sse_only                          0.1667   0.3339   0.7045   0.6346  
H2_R15               sse_only                          0.1667   0.3845   0.7849   0.7186  
H3_R15               sse_only                          0.1667   0.4128   0.7415   0.6686  
H1_structural        structural                        0.1684   0.2794   0.6620   0.6035  
H1_sse_subset        sse_only                          0.1667   0.3192   0.6999   0.6131  

Permutation test (H4): p=0.0000, null 95th pctl=0.1813

## Interpretation

H1: SIGNAL DETECTED (AUPRC 0.3203 > 1.5x base rate 0.1667)
H2: SIGNAL DETECTED (AUPRC 0.3936 > 1.5x base rate 0.1667)
H3: SIGNAL DETECTED (AUPRC 0.3816 > 1.5x base rate 0.1667)
H4: SIGNAL DETECTED (AUPRC 0.4878 > 1.5x base rate 0.1684)
H5: no signal (AUPRC 0.1818 ~ base rate 0.1667)
