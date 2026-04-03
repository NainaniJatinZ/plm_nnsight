# Expanded Anchor Feature Regression (v2)

Search direction: L10H9 key-side W_K^T @ q_mean from 2B61A clean masked sequence.
Target: key score = dot(post-LN residual at layer 10, W_K^T @ q_mean_unit), on full unmasked sequence.
Total residues: 5427 across 18 proteins.
Residues with PDB features: 4861 (17 proteins).
Residues with conservation + PDB: 1252.

## New features in v2

- RSA: Relative Solvent Accessibility via ShrakeRupley (normalized by Tien et al. 2013 max ASA).
- self_hydro: Kyte-Doolittle hydrophobicity of the residue.
- local_hydro_w5: Mean KD hydrophobicity in a window of +/-2 residues.
- same_face_hydro: Mean KD hydrophobicity of same-face beta-strand neighbors (positions i-2, i, i+2).
- contacts_8A: Number of CB-CB contacts within 8 A (CA for glycine).
- long_range_contacts: Contacts within 8 A with sequence separation > 12.

## Anchor feature summary

| Protein | Pos | AA | SSE | Proj | RSA | Contacts 8A | LR contacts | Self hydro |
|---------|-----|-----|-----|------|-----|-------------|-------------|------------|
| 1BRTA | 220 | L | E | 0.864 | 0.000 | 16 | 12 | 3.8 |
| 1PVGA | 101 | V | E | 1.190 | 0.000 | 13 | 7 | 4.2 |
| 2B61A | 315 | T | E | 1.059 | 0.000 | 13 | 9 | -0.7 |
| 2DPMA | 39 | F | E | 0.963 | 0.000 | 14 | 10 | 2.8 |
| 2PKEA | 131 | L | E | 0.625 | - | - | - | 3.8 |
| 2QY6A | 64 | A | E | 1.076 | 0.000 | 13 | 9 | 1.8 |
| 2YHWA | 287 | V | E | 1.254 | 0.000 | 16 | 9 | 4.2 |
| 3CSSA | 40 | L | E | 0.784 | 0.012 | 13 | 9 | 3.8 |
| 3HO7A | 63 | A | E | 0.514 | 0.000 | 15 | 7 | 1.8 |
| 3OKPA | 200 | I | E | 0.836 | 0.012 | 17 | 13 | 4.5 |
| 3QDLA | 114 | P | H | -0.547 | - | - | - | -1.6 |
| 3WJPA | 94 | L | E | 1.262 | 0.012 | 16 | 12 | 3.8 |
| 4EHUA | 100 | G | C | 0.834 | 0.000 | 14 | 8 | -0.4 |
| 4EX6A | 124 | M | E | 0.983 | 0.000 | 18 | 13 | 1.9 |
| 4EZIA | 310 | L | E | 0.967 | 0.006 | 15 | 11 | 3.8 |
| 4ME3A | 75 | G | H | 0.300 | 0.000 | 12 | 4 | -0.4 |
| 4N9WA | 194 | V | E | 0.820 | 0.000 | 16 | 12 | 4.2 |
| 4OY3A | 193 | L | E | 0.905 | 0.018 | 16 | 12 | 3.8 |

## OLS Model R2 summary

All models fit on rows with complete PDB features (RSA + contacts).

| Model | Description | N | R2 | adj-R2 |
|-------|-------------|---|-----|--------|
| A | SSE + protein FE | 4861 | 0.1092 | 0.1059 |
| B | A + position + RSA | 4861 | 0.1590 | 0.1552 |
| C | B + hydrophobic context | 4861 | 0.2160 | 0.2119 |
| D | C + 3D contact number | 4861 | 0.2446 | 0.2403 |
| E | D + conservation + AA identity | 1252 | 0.2733 | 0.2530 |

## Model A: SSE + protein FE (baseline)

N=4861, k=19, R2=0.1092, adj-R2=0.1059

| Feature | Coef | SE | t | p |
|---------|------|-----|---|---|
| intercept | -0.5422 | 0.0132 | -41.12 | 0.0000** |
| SSE_E | 0.1507 | 0.0081 | 18.50 | 0.0000** |
| SSE_H | -0.0089 | 0.0068 | -1.30 | 0.1926 |
| protein_1PVGA | 0.0034 | 0.0166 | 0.20 | 0.8383 |
| protein_2B61A | 0.0271 | 0.0168 | 1.61 | 0.1073 |
| protein_2DPMA | -0.0154 | 0.0181 | -0.85 | 0.3957 |
| protein_2QY6A | -0.0069 | 0.0184 | -0.38 | 0.7053 |
| protein_2YHWA | -0.0001 | 0.0173 | -0.00 | 0.9971 |
| protein_3CSSA | -0.0442 | 0.0180 | -2.46 | 0.0140* |
| protein_3HO7A | -0.0827 | 0.0189 | -4.38 | 0.0000** |
| protein_3OKPA | 0.0306 | 0.0165 | 1.85 | 0.0646 |
| protein_3QDLA | 0.0306 | 0.0201 | 1.52 | 0.1280 |
| protein_3WJPA | 0.0197 | 0.0170 | 1.16 | 0.2471 |
| protein_4EHUA | 0.0605 | 0.0179 | 3.38 | 0.0007** |
| protein_4EX6A | 0.0457 | 0.0189 | 2.42 | 0.0158* |
| protein_4EZIA | -0.0399 | 0.0167 | -2.39 | 0.0170* |
| protein_4ME3A | -0.0526 | 0.0184 | -2.87 | 0.0041** |
| protein_4N9WA | 0.0716 | 0.0167 | 4.29 | 0.0000** |
| protein_4OY3A | -0.0194 | 0.0187 | -1.04 | 0.2988 |

## Model B: + position + RSA

N=4861, k=23, R2=0.1590, adj-R2=0.1552

| Feature | Coef | SE | t | p |
|---------|------|-----|---|---|
| intercept | -0.4720 | 0.0161 | -29.25 | 0.0000** |
| SSE_E | 0.1192 | 0.0082 | 14.61 | 0.0000** |
| SSE_H | -0.0146 | 0.0077 | -1.88 | 0.0597 |
| dist_to_boundary | 0.0037 | 0.0024 | 1.51 | 0.1317 |
| seg_len | -0.0028 | 0.0008 | -3.65 | 0.0003** |
| is_boundary | -0.0167 | 0.0091 | -1.82 | 0.0681 |
| RSA | -0.2806 | 0.0174 | -16.14 | 0.0000** |
| protein_1PVGA | 0.0014 | 0.0162 | 0.09 | 0.9300 |
| protein_2B61A | 0.0236 | 0.0164 | 1.44 | 0.1497 |
| protein_2DPMA | -0.0016 | 0.0176 | -0.09 | 0.9289 |
| protein_2QY6A | 0.0043 | 0.0179 | 0.24 | 0.8109 |
| protein_2YHWA | 0.0065 | 0.0168 | 0.39 | 0.6986 |
| protein_3CSSA | -0.0360 | 0.0175 | -2.06 | 0.0398* |
| protein_3HO7A | -0.0821 | 0.0184 | -4.46 | 0.0000** |
| protein_3OKPA | 0.0404 | 0.0161 | 2.50 | 0.0125* |
| protein_3QDLA | 0.0481 | 0.0196 | 2.46 | 0.0140* |
| protein_3WJPA | 0.0206 | 0.0165 | 1.24 | 0.2132 |
| protein_4EHUA | 0.0631 | 0.0174 | 3.62 | 0.0003** |
| protein_4EX6A | 0.0324 | 0.0184 | 1.76 | 0.0789 |
| protein_4EZIA | -0.0520 | 0.0163 | -3.20 | 0.0014** |
| protein_4ME3A | -0.0279 | 0.0179 | -1.56 | 0.1200 |
| protein_4N9WA | 0.0944 | 0.0163 | 5.79 | 0.0000** |
| protein_4OY3A | -0.0258 | 0.0181 | -1.42 | 0.1558 |

## Model C: + hydrophobic context

N=4861, k=26, R2=0.2160, adj-R2=0.2119

| Feature | Coef | SE | t | p |
|---------|------|-----|---|---|
| intercept | -0.4824 | 0.0156 | -30.89 | 0.0000** |
| SSE_E | 0.0908 | 0.0083 | 11.00 | 0.0000** |
| SSE_H | -0.0237 | 0.0075 | -3.14 | 0.0017** |
| dist_to_boundary | 0.0043 | 0.0023 | 1.84 | 0.0664 |
| seg_len | -0.0024 | 0.0007 | -3.29 | 0.0010** |
| is_boundary | -0.0046 | 0.0088 | -0.52 | 0.6049 |
| RSA | -0.1826 | 0.0176 | -10.38 | 0.0000** |
| self_hydro | 0.0183 | 0.0011 | 16.38 | 0.0000** |
| local_hydro_w5 | 0.0169 | 0.0035 | 4.88 | 0.0000** |
| same_face_hydro | -0.0106 | 0.0028 | -3.80 | 0.0001** |
| protein_1PVGA | 0.0120 | 0.0157 | 0.77 | 0.4433 |
| protein_2B61A | 0.0281 | 0.0158 | 1.77 | 0.0760 |
| protein_2DPMA | -0.0013 | 0.0170 | -0.08 | 0.9394 |
| protein_2QY6A | 0.0061 | 0.0173 | 0.35 | 0.7245 |
| protein_2YHWA | -0.0046 | 0.0163 | -0.28 | 0.7771 |
| protein_3CSSA | -0.0439 | 0.0169 | -2.59 | 0.0095** |
| protein_3HO7A | -0.0787 | 0.0178 | -4.42 | 0.0000** |
| protein_3OKPA | 0.0361 | 0.0156 | 2.31 | 0.0207* |
| protein_3QDLA | 0.0414 | 0.0189 | 2.19 | 0.0283* |
| protein_3WJPA | 0.0163 | 0.0160 | 1.02 | 0.3077 |
| protein_4EHUA | 0.0605 | 0.0168 | 3.59 | 0.0003** |
| protein_4EX6A | 0.0255 | 0.0178 | 1.43 | 0.1522 |
| protein_4EZIA | -0.0445 | 0.0157 | -2.83 | 0.0046** |
| protein_4ME3A | -0.0249 | 0.0173 | -1.44 | 0.1499 |
| protein_4N9WA | 0.0795 | 0.0158 | 5.03 | 0.0000** |
| protein_4OY3A | -0.0275 | 0.0175 | -1.57 | 0.1167 |

## Model D: + 3D contacts (best linear, all proteins)

N=4861, k=28, R2=0.2446, adj-R2=0.2403

| Feature | Coef | SE | t | p |
|---------|------|-----|---|---|
| intercept | -0.6523 | 0.0223 | -29.22 | 0.0000** |
| SSE_E | 0.0580 | 0.0085 | 6.84 | 0.0000** |
| SSE_H | -0.0263 | 0.0080 | -3.28 | 0.0011** |
| dist_to_boundary | 0.0038 | 0.0023 | 1.65 | 0.0994 |
| seg_len | -0.0026 | 0.0007 | -3.57 | 0.0004** |
| is_boundary | -0.0012 | 0.0088 | -0.14 | 0.8900 |
| RSA | 0.0193 | 0.0234 | 0.83 | 0.4093 |
| self_hydro | 0.0160 | 0.0011 | 14.40 | 0.0000** |
| local_hydro_w5 | 0.0143 | 0.0034 | 4.17 | 0.0000** |
| same_face_hydro | -0.0101 | 0.0027 | -3.70 | 0.0002** |
| contacts_8A | 0.0120 | 0.0018 | 6.62 | 0.0000** |
| long_range_contacts | 0.0062 | 0.0017 | 3.69 | 0.0002** |
| protein_1PVGA | 0.0323 | 0.0155 | 2.09 | 0.0366* |
| protein_2B61A | 0.0364 | 0.0155 | 2.34 | 0.0192* |
| protein_2DPMA | 0.0089 | 0.0167 | 0.53 | 0.5948 |
| protein_2QY6A | 0.0089 | 0.0170 | 0.52 | 0.6010 |
| protein_2YHWA | -0.0124 | 0.0160 | -0.78 | 0.4376 |
| protein_3CSSA | -0.0439 | 0.0166 | -2.64 | 0.0082** |
| protein_3HO7A | -0.0645 | 0.0175 | -3.68 | 0.0002** |
| protein_3OKPA | 0.0250 | 0.0153 | 1.63 | 0.1029 |
| protein_3QDLA | 0.0522 | 0.0186 | 2.81 | 0.0049** |
| protein_3WJPA | 0.0103 | 0.0157 | 0.66 | 0.5113 |
| protein_4EHUA | 0.0589 | 0.0165 | 3.56 | 0.0004** |
| protein_4EX6A | 0.0359 | 0.0175 | 2.05 | 0.0404* |
| protein_4EZIA | -0.0344 | 0.0155 | -2.22 | 0.0263* |
| protein_4ME3A | -0.0189 | 0.0170 | -1.11 | 0.2657 |
| protein_4N9WA | 0.0673 | 0.0155 | 4.33 | 0.0000** |
| protein_4OY3A | -0.0230 | 0.0172 | -1.34 | 0.1814 |

## Model E: + conservation + AA identity (conservation subset)

N=1252, k=35, R2=0.2733, adj-R2=0.2530

| Feature | Coef | SE | t | p |
|---------|------|-----|---|---|
| intercept | -0.7110 | 0.0424 | -16.76 | 0.0000** |
| SSE_E | 0.0772 | 0.0165 | 4.67 | 0.0000** |
| SSE_H | -0.0142 | 0.0155 | -0.92 | 0.3601 |
| dist_to_boundary | 0.0026 | 0.0044 | 0.58 | 0.5616 |
| seg_len | -0.0021 | 0.0013 | -1.60 | 0.1091 |
| is_boundary | -0.0106 | 0.0173 | -0.62 | 0.5386 |
| RSA | 0.1024 | 0.0487 | 2.10 | 0.0356* |
| self_hydro | 0.0052 | 0.0042 | 1.24 | 0.2147 |
| local_hydro_w5 | 0.0031 | 0.0067 | 0.46 | 0.6424 |
| same_face_hydro | -0.0112 | 0.0052 | -2.13 | 0.0332* |
| contacts_8A | 0.0080 | 0.0037 | 2.15 | 0.0318* |
| long_range_contacts | 0.0128 | 0.0034 | 3.74 | 0.0002** |
| conservation | 0.1109 | 0.0278 | 3.99 | 0.0001** |
| AA_C | 0.0538 | 0.0683 | 0.79 | 0.4308 |
| AA_D | 0.0098 | 0.0202 | 0.49 | 0.6274 |
| AA_E | -0.0628 | 0.0220 | -2.86 | 0.0043** |
| AA_F | 0.0800 | 0.0335 | 2.39 | 0.0170* |
| AA_G | 0.0649 | 0.0251 | 2.59 | 0.0098** |
| AA_H | 0.0697 | 0.0367 | 1.90 | 0.0576 |
| AA_I | 0.0672 | 0.0371 | 1.81 | 0.0704 |
| AA_K | -0.0584 | 0.0221 | -2.65 | 0.0082** |
| AA_L | 0.0841 | 0.0337 | 2.50 | 0.0126* |
| AA_M | 0.1014 | 0.0984 | 1.03 | 0.3029 |
| AA_N | 0.0088 | 0.0216 | 0.41 | 0.6852 |
| AA_P | 0.0096 | 0.0286 | 0.33 | 0.7379 |
| AA_Q | -0.0994 | 0.0261 | -3.81 | 0.0001** |
| AA_R | -0.0221 | 0.0243 | -0.91 | 0.3632 |
| AA_S | -0.0235 | 0.0250 | -0.94 | 0.3466 |
| AA_T | -0.0081 | 0.0255 | -0.32 | 0.7511 |
| AA_V | 0.0993 | 0.0368 | 2.70 | 0.0071** |
| AA_W | 0.0823 | 0.0553 | 1.49 | 0.1371 |
| AA_Y | -0.0001 | 0.0252 | -0.00 | 0.9984 |
| protein_1PVGA | 0.0122 | 0.0171 | 0.71 | 0.4784 |
| protein_2B61A | 0.0240 | 0.0159 | 1.51 | 0.1320 |
| protein_2DPMA | 0.0002 | 0.0172 | 0.01 | 0.9888 |

## Random Forest / Gradient Boosting

Features: SSE_E, SSE_H, RSA, self_hydro, local_hydro_w5, same_face_hydro, contacts_8A, long_range_contacts, dist_to_boundary, seg_len

RF 5-fold CV R2: 0.2433 +/- 0.0222

GB 5-fold CV R2: 0.1981 +/- 0.0305

RF train R2: 0.6826

RF feature importances:

| Feature | Importance |
|---------|------------|
| contacts_8A | 0.2281 |
| local_hydro_w5 | 0.1661 |
| same_face_hydro | 0.1440 |
| self_hydro | 0.1419 |
| seg_len | 0.0820 |
| long_range_contacts | 0.0587 |
| RSA | 0.0587 |
| dist_to_boundary | 0.0541 |
| SSE_E | 0.0479 |
| SSE_H | 0.0186 |

## Anchor residual analysis

OLS Model D residual std: 0.1921

RF residual std: 0.1245

| Protein | Actual | Pred (OLS-D) | Z (OLS-D) | Pred (RF) | Z (RF) |
|---------|--------|-------------|-----------|-----------|--------|
| 1BRTA | 0.864 | -0.262 | 5.86 | 0.194 | 5.38 |
| 1PVGA | 1.190 | -0.327 | 7.90 | 0.319 | 7.00 |
| 2B61A | 1.059 | -0.360 | 7.39 | 0.205 | 6.86 |
| 2DPMA | 0.963 | -0.327 | 6.72 | 0.434 | 4.25 |
| 2PKEA | 0.625 | - | - | - | - | (not in PDB) |
| 2QY6A | 1.076 | -0.358 | 7.46 | 0.027 | 8.42 |
| 2YHWA | 1.254 | -0.282 | 7.99 | 0.422 | 6.68 |
| 3CSSA | 0.784 | -0.362 | 5.96 | 0.525 | 2.08 |
| 3HO7A | 0.514 | -0.397 | 4.74 | 0.007 | 4.07 |
| 3OKPA | 0.836 | -0.208 | 5.44 | 0.385 | 3.62 |
| 3QDLA | -0.547 | - | - | - | - | (not in PDB) |
| 3WJPA | 1.262 | -0.269 | 7.97 | 0.540 | 5.80 |
| 4EHUA | 0.834 | -0.378 | 6.31 | 0.288 | 4.38 |
| 4EX6A | 0.983 | -0.234 | 6.33 | 0.315 | 5.36 |
| 4EZIA | 0.967 | -0.309 | 6.64 | 0.207 | 6.10 |
| 4ME3A | 0.300 | -0.548 | 4.41 | 0.038 | 2.10 |
| 4N9WA | 0.820 | -0.196 | 5.29 | 0.161 | 5.29 |
| 4OY3A | 0.905 | -0.302 | 6.28 | 0.394 | 4.11 |

OLS-D anchor z-scores: mean=6.42, median=6.32, range=[4.41, 7.99]

RF anchor z-scores: mean=5.09, median=5.33, range=[2.08, 8.42]

OLS-D: 0/16 anchors within 2 sigma, 16/16 above 4 sigma.

RF: 0/16 anchors within 2 sigma, 13/16 above 4 sigma.

