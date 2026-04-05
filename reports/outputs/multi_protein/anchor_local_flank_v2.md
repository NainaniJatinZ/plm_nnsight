# Anchor Local Flank v2: Results

## SSE-only matched (500 proteins)

Proteins: 500, Anchors: 500, Control pairs: 2500

### Radius-Performance Table (L1 Logistic Regression)

| Radius | Full AUROC | Full AUPRC | Censor-ID AUROC | Censor-ID AUPRC | Censor-All AUROC | Censor-All AUPRC |
|--------|-----------|-----------|----------------|----------------|-----------------|----------------|
| 5 | 0.820 | 0.507 | 0.792 | 0.454 | 0.773 | 0.417 |
| 10 | 0.812 | 0.502 | 0.788 | 0.472 | 0.770 | 0.435 |
| 15 | 0.800 | 0.483 | 0.777 | 0.462 | 0.759 | 0.432 |
| 20 | 0.778 | 0.442 | 0.756 | 0.416 | 0.738 | 0.387 |
| 25 | 0.776 | 0.457 | 0.757 | 0.433 | 0.740 | 0.405 |
| 30 | 0.768 | 0.445 | 0.755 | 0.431 | 0.734 | 0.407 |
| 40 | 0.721 | 0.403 | 0.698 | 0.377 | 0.680 | 0.366 |

### Gradient Boosting Comparison (Full Window Only)

| Radius | GB AUROC | GB AUPRC | LR AUROC | LR AUPRC |
|--------|---------|---------|---------|--------|
| 5 | 0.845 | 0.583 | 0.820 | 0.507 |
| 10 | 0.840 | 0.565 | 0.812 | 0.502 |
| 15 | 0.844 | 0.589 | 0.800 | 0.483 |
| 20 | 0.844 | 0.587 | 0.778 | 0.442 |
| 25 | 0.844 | 0.598 | 0.776 | 0.457 |
| 30 | 0.836 | 0.612 | 0.768 | 0.445 |
| 40 | 0.840 | 0.625 | 0.721 | 0.403 |

### Top Features (L1 LR, R=5)

| Rank | Feature | Coefficient |
|------|---------|------------|
| 1 | sse_-1_E | 2.0862 |
| 2 | sse_1_H | 1.9923 |
| 3 | sse_0_E | -1.4777 |
| 4 | aaclass_0_proline | -1.3271 |
| 5 | sse_-3_H | -1.1435 |
| 6 | sse_3_H | -1.1345 |
| 7 | sse_5_H | 1.0975 |
| 8 | aaclass_-1_glycine | -0.9508 |
| 9 | aaclass_0_positive | 0.8804 |
| 10 | sse_2_C | -0.7713 |
| 11 | center_glycine | 0.6833 |
| 12 | aaclass_-3_glycine | -0.6764 |
| 13 | aaclass_1_glycine | -0.6422 |
| 14 | mean_hydro | 0.6041 |
| 15 | sse_1_C | -0.5586 |
| 16 | center_sse_E | -0.4994 |
| 17 | aaclass_-5_aromatic | -0.4797 |
| 18 | aaclass_-2_negative | 0.4668 |
| 19 | sse_0_C | 0.4579 |
| 20 | aaclass_2_positive | -0.4366 |

---

## Structurally matched (SSE+RSA+contacts_8A, v3 subset)

Proteins: 17, Anchors: 51, Control pairs: 253

### Radius-Performance Table (L1 Logistic Regression)

| Radius | Full AUROC | Full AUPRC | Censor-ID AUROC | Censor-ID AUPRC | Censor-All AUROC | Censor-All AUPRC |
|--------|-----------|-----------|----------------|----------------|-----------------|----------------|
| 5 | 0.670 | 0.115 | 0.678 | 0.125 | 0.694 | 0.125 |
| 10 | 0.615 | 0.097 | 0.616 | 0.095 | 0.613 | 0.093 |
| 15 | 0.509 | 0.079 | 0.519 | 0.084 | 0.523 | 0.085 |
| 20 | 0.656 | 0.107 | 0.659 | 0.108 | 0.655 | 0.106 |
| 25 | 0.594 | 0.093 | 0.595 | 0.093 | 0.596 | 0.093 |
| 30 | 0.710 | 0.144 | 0.710 | 0.144 | 0.710 | 0.144 |
| 40 | 0.524 | 0.079 | 0.524 | 0.079 | 0.523 | 0.079 |

### Gradient Boosting Comparison (Full Window Only)

| Radius | GB AUROC | GB AUPRC | LR AUROC | LR AUPRC |
|--------|---------|---------|---------|--------|
| 5 | 0.693 | 0.166 | 0.670 | 0.115 |
| 10 | 0.508 | 0.076 | 0.615 | 0.097 |
| 15 | 0.579 | 0.096 | 0.509 | 0.079 |
| 20 | 0.714 | 0.185 | 0.656 | 0.107 |
| 25 | 0.517 | 0.105 | 0.594 | 0.093 |
| 30 | 0.541 | 0.078 | 0.710 | 0.144 |
| 40 | 0.445 | 0.066 | 0.524 | 0.079 |

### Top Features (L1 LR, R=30)

| Rank | Feature | Coefficient |
|------|---------|------------|
| 1 | aaclass_10_proline | 4.6300 |
| 2 | aaclass_7_glycine | 2.3012 |
| 3 | aaclass_8_proline | 1.9279 |
| 4 | aaclass_-20_positive | 1.6799 |
| 5 | aaclass_-26_negative | 1.2877 |
| 6 | aaclass_5_positive | 1.0546 |
| 7 | aaclass_-3_proline | 1.0387 |
| 8 | aaclass_29_polar | 0.9592 |
| 9 | aaclass_10_aromatic | 0.8888 |
| 10 | aaclass_8_negative | 0.7968 |
| 11 | aaclass_21_aromatic | 0.7631 |
| 12 | aaclass_-17_polar | 0.7313 |
| 13 | aaclass_14_negative | 0.7304 |
| 14 | aaclass_-14_negative | 0.7286 |
| 15 | aaclass_18_negative | 0.6928 |
| 16 | aaclass_3_proline | 0.6927 |
| 17 | sse_25_C | -0.6545 |
| 18 | aaclass_-5_polar | 0.6435 |
| 19 | sse_-7_C | 0.6388 |
| 20 | aaclass_-6_positive | 0.5797 |

---

