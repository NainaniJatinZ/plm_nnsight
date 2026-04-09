#!/usr/bin/env python3
"""Anchor-only PCA and partial correlation analysis for QK decomposition.

Supplements the main qk_space_decomposition.py with:
1. PCA on anchor keys only (774 vectors in R^64) to find anchor subclusters
2. Partial correlations: regress out confounds to see which structural property
   independently explains variation along d

Usage:
    PYTHONUNBUFFERED=1 uv run python scripts/qk_anchor_pca.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy import stats as sp_stats
from sklearn.decomposition import PCA

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDB_DIR = DATA_DIR / "pdb"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

AUDIT_CSV = REPORT_DIR / "anchor_behavior_audit.csv"

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN = "2B61A"

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


# --- Reuse functions from qk_space_decomposition.py ---
from scripts.qk_space_decomposition import (
    load_model, extract_head_weights, compute_search_dir,
    extract_qk_vectors, compute_pdb_features, select_confident_proteins,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-proteins", type=int, default=0)
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    flush_print("Loading data...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")

    seqs = {k: v for k, v in all_seqs.items() if 100 <= len(v) <= 500}
    proteins = select_confident_proteins(seqs, ss_dict, min_top1_mass=0.5)
    if args.max_proteins > 0:
        proteins = proteins[:args.max_proteins]
    flush_print(f"  {len(proteins)} confident proteins")

    flush_print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    ref_seq = all_seqs[REFERENCE_PROTEIN]
    q_mean_norm = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_key = q_mean_norm.numpy()
    d_key_unit = d_key / (np.linalg.norm(d_key) + 1e-8)

    # -----------------------------------------------------------------------
    # Collect anchor key vectors + structural labels
    # -----------------------------------------------------------------------
    flush_print(f"\nExtracting anchor key vectors...")
    anchor_keys = []      # (n_proteins, 64)
    anchor_rsa = []
    anchor_contacts = []
    anchor_lrf = []
    anchor_sse = []
    anchor_proj = []
    anchor_pids = []
    anchor_positions = []

    t0 = time.time()
    for i, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]

        try:
            k_Ld, _ = extract_qk_vectors(model, tokenizer, seq, weights, args.device)
        except Exception as e:
            flush_print(f"  ERROR on {pid}: {e}")
            continue

        anchor_k = k_Ld[anchor]  # (64,)
        anchor_keys.append(anchor_k)
        anchor_proj.append(float(anchor_k @ d_key_unit))
        anchor_pids.append(pid)
        anchor_positions.append(anchor)

        # SSE
        if pid in ss_dict and anchor < len(ss_dict[pid]):
            anchor_sse.append(ss_dict[pid][anchor])
        else:
            anchor_sse.append("C")

        # PDB features
        pdb_feats = compute_pdb_features(pid, seq)
        if pdb_feats is not None and anchor in pdb_feats:
            anchor_rsa.append(pdb_feats[anchor]["rsa"])
            anchor_contacts.append(pdb_feats[anchor]["contacts_8A"])
            anchor_lrf.append(pdb_feats[anchor]["long_range_fraction"])
        else:
            anchor_rsa.append(np.nan)
            anchor_contacts.append(np.nan)
            anchor_lrf.append(np.nan)

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            flush_print(f"  {i+1}/{len(proteins)} ({rate:.1f}/s, ETA {(len(proteins)-i-1)/rate:.0f}s)")

    K_anchor = np.array(anchor_keys)   # (n, 64)
    rsa_arr = np.array(anchor_rsa)
    contacts_arr = np.array(anchor_contacts)
    lrf_arr = np.array(anchor_lrf)
    sse_arr = np.array(anchor_sse)
    proj_arr = np.array(anchor_proj)
    n = len(K_anchor)
    flush_print(f"  {n} anchor keys collected in {time.time()-t0:.0f}s")

    has_pdb = ~np.isnan(rsa_arr)
    n_pdb = has_pdb.sum()
    flush_print(f"  {n_pdb} with PDB features")

    # ===================================================================
    # 1. Anchor-only PCA
    # ===================================================================
    flush_print("\n=== Anchor-only PCA ===")
    pca = PCA(n_components=min(20, n))
    K_pca = pca.fit_transform(K_anchor)
    flush_print(f"  Variance explained (top 10): {pca.explained_variance_ratio_[:10].round(4)}")
    flush_print(f"  Cumulative: {np.cumsum(pca.explained_variance_ratio_[:10]).round(4)}")

    # Alignment of d with anchor PCA components
    d_in_pca = pca.transform(d_key_unit.reshape(1, -1))[0]
    d_pca_loadings = d_in_pca / (np.linalg.norm(d_in_pca) + 1e-8)
    flush_print(f"  d loadings on anchor PCs (squared): {(d_pca_loadings[:10]**2).round(4)}")
    flush_print(f"  d is {(d_pca_loadings[:10]**2).sum()*100:.1f}% within top-10 anchor PCs")

    # Correlation of anchor PCs with structural properties
    flush_print("\n  Anchor PC correlations with structural properties:")
    for pc_i in range(min(5, K_pca.shape[1])):
        for prop_name, prop_vals in [("RSA", rsa_arr), ("contacts", contacts_arr), ("LRF", lrf_arr)]:
            valid = has_pdb
            if valid.sum() < 20:
                continue
            rho, p = sp_stats.spearmanr(K_pca[valid, pc_i], prop_vals[valid])
            if abs(rho) > 0.1:
                flush_print(f"    PC{pc_i+1} vs {prop_name}: rho={rho:.4f}, p={p:.2e}")
        for sse_label in ["H", "E"]:
            rho, p = sp_stats.spearmanr(K_pca[:, pc_i], (sse_arr == sse_label).astype(float))
            if abs(rho) > 0.1:
                flush_print(f"    PC{pc_i+1} vs is_{sse_label}: rho={rho:.4f}, p={p:.2e}")

    # --- Anchor PCA figure ---
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    # Panel A: PC1 vs PC2, colored by SSE
    ax = axes[0, 0]
    sse_colors = {"H": "#E07B54", "E": "#5B8FA8", "C": "#AAAAAA"}
    for s, color in sse_colors.items():
        mask = sse_arr == s
        ax.scatter(K_pca[mask, 0], K_pca[mask, 1], s=20, alpha=0.6, c=color, label=f"SSE={s}", edgecolors="white", linewidths=0.3)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_title("A. Anchor keys PC1 vs PC2 (SSE)")
    ax.legend(fontsize=8)

    # Panel B: PC1 vs PC2, colored by RSA
    ax = axes[0, 1]
    valid_rsa = has_pdb
    sc = ax.scatter(K_pca[valid_rsa, 0], K_pca[valid_rsa, 1], s=20, alpha=0.6, c=rsa_arr[valid_rsa], cmap="coolwarm_r", vmin=0, vmax=0.5, edgecolors="white", linewidths=0.3)
    plt.colorbar(sc, ax=ax, label="RSA")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_title("B. Anchor keys PC1 vs PC2 (RSA)")

    # Panel C: PC1 vs PC2, colored by contacts
    ax = axes[0, 2]
    sc = ax.scatter(K_pca[valid_rsa, 0], K_pca[valid_rsa, 1], s=20, alpha=0.6, c=contacts_arr[valid_rsa], cmap="YlOrRd", edgecolors="white", linewidths=0.3)
    plt.colorbar(sc, ax=ax, label="contacts_8A")
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_title("C. Anchor keys PC1 vs PC2 (contacts)")

    # Panel D: PC1 vs PC3
    ax = axes[1, 0]
    for s, color in sse_colors.items():
        mask = sse_arr == s
        ax.scatter(K_pca[mask, 0], K_pca[mask, 2], s=20, alpha=0.6, c=color, label=f"SSE={s}", edgecolors="white", linewidths=0.3)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC3 ({pca.explained_variance_ratio_[2]:.1%})")
    ax.set_title("D. Anchor keys PC1 vs PC3 (SSE)")
    ax.legend(fontsize=8)

    # Panel E: PC2 vs PC3
    ax = axes[1, 1]
    sc = ax.scatter(K_pca[valid_rsa, 1], K_pca[valid_rsa, 2], s=20, alpha=0.6, c=lrf_arr[valid_rsa], cmap="viridis", edgecolors="white", linewidths=0.3)
    plt.colorbar(sc, ax=ax, label="long-range fraction")
    ax.set_xlabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%})")
    ax.set_ylabel(f"PC3 ({pca.explained_variance_ratio_[2]:.1%})")
    ax.set_title("E. Anchor keys PC2 vs PC3 (LRF)")

    # Panel F: projection onto d vs PC1 (is d just PC1?)
    ax = axes[1, 2]
    ax.scatter(proj_arr, K_pca[:, 0], s=15, alpha=0.5, c="#5B7FA3", edgecolors="white", linewidths=0.3)
    rho_d_pc1, _ = sp_stats.spearmanr(proj_arr, K_pca[:, 0])
    ax.set_xlabel("k . d (projection onto search direction)")
    ax.set_ylabel(f"PC1 of anchor keys")
    ax.set_title(f"F. d-projection vs anchor PC1 (rho={rho_d_pc1:.3f})")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out_path = REPORT_DIR / "qk_anchor_only_pca.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_path}")

    # ===================================================================
    # 2. Partial correlation analysis
    # ===================================================================
    flush_print("\n=== Partial correlation analysis ===")
    flush_print("  Goal: which structural property independently predicts k.d among anchors?\n")

    # Work with anchors that have all PDB features
    valid = has_pdb & ~np.isnan(lrf_arr)
    n_valid = valid.sum()
    flush_print(f"  {n_valid} anchors with complete PDB features")

    y = proj_arr[valid]  # k . d
    X_rsa = rsa_arr[valid]
    X_contacts = contacts_arr[valid]
    X_lrf = lrf_arr[valid]
    X_helix = (sse_arr[valid] == "H").astype(float)
    X_strand = (sse_arr[valid] == "E").astype(float)

    # Pairwise correlations among predictors
    flush_print("  Pairwise Spearman correlations among structural features:")
    features = {"RSA": X_rsa, "contacts": X_contacts, "LRF": X_lrf, "helix": X_helix, "strand": X_strand}
    feat_names = list(features.keys())
    for i in range(len(feat_names)):
        for j in range(i+1, len(feat_names)):
            rho, p = sp_stats.spearmanr(features[feat_names[i]], features[feat_names[j]])
            flush_print(f"    {feat_names[i]} vs {feat_names[j]}: rho={rho:.4f}")

    # Zero-order correlations with k.d
    flush_print("\n  Zero-order Spearman correlations with k.d:")
    for name, vals in features.items():
        rho, p = sp_stats.spearmanr(vals, y)
        flush_print(f"    {name}: rho={rho:.4f}, p={p:.2e}")

    # Partial correlations using OLS residuals
    # For each property X_i, compute corr(residual(y ~ others), residual(X_i ~ others))
    flush_print("\n  Partial correlations (controlling for all other features):")
    from numpy.linalg import lstsq

    all_X = np.column_stack([X_rsa, X_contacts, X_lrf, X_helix, X_strand])
    partial_results = {}

    for idx, name in enumerate(feat_names):
        # Confounders = all features except this one
        confound_idx = [j for j in range(len(feat_names)) if j != idx]
        C = np.column_stack([all_X[:, j] for j in confound_idx])
        C_with_intercept = np.column_stack([np.ones(n_valid), C])

        # Residualize y on confounders
        beta_y, _, _, _ = lstsq(C_with_intercept, y, rcond=None)
        y_resid = y - C_with_intercept @ beta_y

        # Residualize X_i on confounders
        xi = all_X[:, idx]
        beta_x, _, _, _ = lstsq(C_with_intercept, xi, rcond=None)
        x_resid = xi - C_with_intercept @ beta_x

        rho, p = sp_stats.spearmanr(y_resid, x_resid)
        partial_results[name] = {"partial_rho": float(rho), "p": float(p)}
        flush_print(f"    {name}: partial rho={rho:.4f}, p={p:.2e}")

    # Multiple regression: all features jointly predicting k.d
    flush_print("\n  Multiple regression (all features -> k.d):")
    X_full = np.column_stack([np.ones(n_valid), all_X])
    beta, residuals, rank, sv = lstsq(X_full, y, rcond=None)
    y_pred = X_full @ beta
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r_squared = 1 - ss_res / ss_tot
    flush_print(f"    R^2 = {r_squared:.4f}")
    flush_print(f"    Coefficients: intercept={beta[0]:.4f}, RSA={beta[1]:.4f}, contacts={beta[2]:.4f}, LRF={beta[3]:.4f}, helix={beta[4]:.4f}, strand={beta[5]:.4f}")

    # Standardized coefficients (for comparable effect sizes)
    X_std = (all_X - all_X.mean(axis=0)) / (all_X.std(axis=0) + 1e-8)
    y_std = (y - y.mean()) / (y.std() + 1e-8)
    X_std_full = np.column_stack([np.ones(n_valid), X_std])
    beta_std, _, _, _ = lstsq(X_std_full, y_std, rcond=None)
    flush_print(f"    Standardized betas: RSA={beta_std[1]:.4f}, contacts={beta_std[2]:.4f}, LRF={beta_std[3]:.4f}, helix={beta_std[4]:.4f}, strand={beta_std[5]:.4f}")

    # Incremental R^2: drop one feature at a time
    flush_print("\n  Incremental R^2 (drop-one):")
    for idx, name in enumerate(feat_names):
        keep_idx = [j for j in range(len(feat_names)) if j != idx]
        X_reduced = np.column_stack([np.ones(n_valid)] + [all_X[:, j] for j in keep_idx])
        beta_red, _, _, _ = lstsq(X_reduced, y, rcond=None)
        y_pred_red = X_reduced @ beta_red
        ss_res_red = np.sum((y - y_pred_red)**2)
        r2_red = 1 - ss_res_red / ss_tot
        delta_r2 = r_squared - r2_red
        flush_print(f"    Drop {name}: R^2 goes from {r_squared:.4f} to {r2_red:.4f} (delta = {delta_r2:.4f})")

    # --- Summary figure ---
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    # Panel A: zero-order vs partial correlations
    ax = axes[0]
    zero_rhos = []
    partial_rhos = []
    for name in feat_names:
        rho_z, _ = sp_stats.spearmanr(features[name], y)
        zero_rhos.append(rho_z)
        partial_rhos.append(partial_results[name]["partial_rho"])
    x_pos = np.arange(len(feat_names))
    w = 0.35
    ax.barh(x_pos - w/2, zero_rhos, height=w, color="#5B7FA3", label="zero-order")
    ax.barh(x_pos + w/2, partial_rhos, height=w, color="#D64550", label="partial")
    ax.set_yticks(x_pos)
    ax.set_yticklabels(feat_names)
    ax.set_xlabel("Spearman rho with k.d")
    ax.set_title("Zero-order vs partial correlations with k.d")
    ax.legend(fontsize=8)
    ax.axvline(0, color="gray", lw=0.5)

    # Panel B: standardized regression coefficients
    ax = axes[1]
    colors = ["#D64550" if b < 0 else "#5B7FA3" for b in beta_std[1:]]
    ax.barh(x_pos, beta_std[1:], color=colors)
    ax.set_yticks(x_pos)
    ax.set_yticklabels(feat_names)
    ax.set_xlabel("Standardized beta")
    ax.set_title(f"Multiple regression (R^2 = {r_squared:.4f})")
    ax.axvline(0, color="gray", lw=0.5)

    # Panel C: incremental R^2
    ax = axes[2]
    delta_r2s = []
    for idx, name in enumerate(feat_names):
        keep_idx = [j for j in range(len(feat_names)) if j != idx]
        X_reduced = np.column_stack([np.ones(n_valid)] + [all_X[:, j] for j in keep_idx])
        beta_red, _, _, _ = lstsq(X_reduced, y, rcond=None)
        y_pred_red = X_reduced @ beta_red
        ss_res_red = np.sum((y - y_pred_red)**2)
        r2_red = 1 - ss_res_red / ss_tot
        delta_r2s.append(r_squared - r2_red)
    ax.barh(x_pos, delta_r2s, color="#6BBF8A")
    ax.set_yticks(x_pos)
    ax.set_yticklabels(feat_names)
    ax.set_xlabel("Delta R^2 (unique contribution)")
    ax.set_title("Incremental R^2 (drop-one)")

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out_path = REPORT_DIR / "qk_anchor_partial_corr.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_path}")

    flush_print("\nDone.")


if __name__ == "__main__":
    main()
