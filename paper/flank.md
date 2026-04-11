#research 
## 1 Jump in Anchoring 
![[branches/plm_attn_jump/reports/anchor_local_flank_v1_per_protein.png]]

![[anchor_local_flank_v1_topk.png]]


## 2 High struc, low seq similarity proteins have similar anchors  

https://search.foldseek.com/result/foldmason/l_Ks2qHFZgvujSaKVmfAd4cUWLi5Rs_KiXUVrA

For 1PVGA, proteins with TM > 0.6 but seq iden < 25%
https://search.foldseek.com/result/_EKBOm5JMKTIBGaLuS43aJtEDSPo82-6wk99hQ/0

![[branches/plm_attn_jump/reports/structure_anchor_transfer_heatmap.png]]
![[branches/plm_attn_jump/reports/structure_anchor_transfer_projection.png]]

## 3 no consistent motif 
Mean pairwise identity (center-aligned): 0.064.
Max: 0.545. Min: 0.000.
Mean BLOSUM62 score: -0.93.
![[branches/plm_attn_jump/reports/anchor_flank_v2_seq_identity.png]]

Anchor residue composition
- I: 48 (19%)
- V: 48 (19%)
- L: 39 (16%)
- G: 24 (10%)
- F: 15 (6%)
- Y: 13 (5%)
- A: 11 (4%)
- S: 9 (4%)
- D: 9 (4%)
- M: 8 (3%)

Hydrophobic anchor residues (V/I/L/F/W/M/A): 69%.


![[branches/plm_attn_jump/reports/anchor_flank_v2_emb_cosine.png]]


![[branches/plm_attn_jump/reports/anchor_flank_motif_top_aa.png]]
![[branches/plm_attn_jump/reports/anchor_flank_motif_logo_all.png]]


## 3DI based flank analysis 

![[anchor_3di_cluster_identity.png]]


![[anchor_3di_top_letter.png]]

![[anchor_3di_logo_all.png]]




![[image.jpg]]


- 