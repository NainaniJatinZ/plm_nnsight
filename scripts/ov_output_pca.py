#!/usr/bin/env python3
"""PCA on per-protein effective OV output of L10H9.

For each protein, L10H9's output is approximately v_anchor @ W_O (since attention
is near-rank-1 onto the anchor). We extract this vector and do PCA across proteins
to see what the head writes into the residual stream.

Usage:
    PYTHONUNBUFFERED=1 uv run python scripts/ov_output_pca.py --device cuda
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


def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def load_model(device: str):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(
        model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager"
    ).to(device).eval()
    model = NNsight(esm_model)
    return model, tokenizer


def extract_ov_weights(model):
    """Extract W_V and W_O for L10H9."""
    attn = model._model.esm.encoder.layer[TARGET_LAYER].attention
    W_V_all = attn.self.value.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_V_all = attn.self.value.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    W_O_all = attn.output.dense.weight.data.cpu()  # (1280, 1280)
    # W_O is shared across heads but operates on concatenated head outputs
    # For head h, the relevant slice is W_O[:, h*HEAD_DIM:(h+1)*HEAD_DIM]
    W_O_h = W_O_all[:, TARGET_HEAD * HEAD_DIM:(TARGET_HEAD + 1) * HEAD_DIM]  # (1280, 64)
    return {
        "W_V_hd": W_V_all[TARGET_HEAD].clone(),  # (64, 1280)
        "b_V_d": b_V_all[TARGET_HEAD].clone(),    # (64,)
        "W_O_dh": W_O_h.clone(),                  # (1280, 64)
    }


def select_proteins(seqs, ss_dict, n):
    rows = []
    with open(AUDIT_CSV) as f:
        for r in csv.DictReader(f):
            pid = r["protein"]
            if pid not in seqs or pid not in ss_dict:
                continue
            if len(seqs[pid]) != len(ss_dict[pid]):
                continue
            mass = float(r["top1_mass"])
            if mass < 0.5:
                continue
            anchor_pos = int(r["top_key_idx"])
            rows.append({"protein": pid, "anchor_pos": anchor_pos, "top1_mass": mass})
    rows.sort(key=lambda x: x["top1_mass"], reverse=True)
    return rows[:n]


@torch.no_grad()
def extract_ov_output(model, tokenizer, sequence: str, anchor_pos: int, ov_weights: dict, device: str):
    """Extract L10H9's effective output vector: v_anchor @ W_O.

    Also extracts the actual head output (attention-weighted) for comparison.

    Returns:
        ov_anchor_D: (1280,) the OV output using only the anchor's value vector
        ov_actual_D: (1280,) the actual mean head output across query positions
        v_anchor_d: (64,) the anchor's value vector (before W_O)
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self

    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=[ln_module, attn_module])

    ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    attn_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"

    x_ln = cache[ln_key].output.detach().cpu()[0]  # (L, 1280) with BOS/EOS
    attn_all = cache[attn_key].output[1].detach().cpu()[0]  # (H, L, L)

    W_V = ov_weights["W_V_hd"]   # (64, 1280)
    b_V = ov_weights["b_V_d"]    # (64,)
    W_O = ov_weights["W_O_dh"]   # (1280, 64)

    # Value vectors for all positions (including BOS/EOS)
    V_Ld = x_ln @ W_V.T + b_V  # (L, 64)

    # Anchor value vector (anchor_pos in residue space = anchor_pos+1 in token space)
    v_anchor_d = V_Ld[anchor_pos + 1]  # (64,)

    # OV output from anchor only: v_anchor @ W_O^T
    # W_O is (1280, 64), so output = W_O @ v_anchor
    ov_anchor_D = W_O @ v_anchor_d  # (1280,)

    # Actual head output: for each query q, output_q = sum_k A[q,k] * V[k] @ W_O
    # Since A is near-rank-1, this should be close to ov_anchor_D for all queries
    A_h = attn_all[TARGET_HEAD]  # (L, L)
    # Attention-weighted value for all queries
    AV = A_h @ V_Ld  # (L, 64) -- attention-weighted value per query
    # Mean across residue queries (exclude BOS/EOS)
    av_mean_d = AV[1:-1].mean(dim=0)  # (64,)
    ov_actual_D = W_O @ av_mean_d  # (1280,)

    return ov_anchor_D.numpy(), ov_actual_D.numpy(), v_anchor_d.numpy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--n-proteins", type=int, default=0, help="0 = all confident proteins")
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
    n_select = args.n_proteins if args.n_proteins > 0 else 9999
    proteins = select_proteins(seqs, ss_dict, n_select)
    flush_print(f"  {len(proteins)} proteins selected")

    flush_print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    ov_weights = extract_ov_weights(model)

    # Also get key weights for d computation
    from scripts.qk_space_decomposition import extract_head_weights, compute_search_dir
    kq_weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    q_mean_norm = compute_search_dir(model, tokenizer, all_seqs[REFERENCE_PROTEIN], kq_weights, args.device)
    d_key = q_mean_norm.numpy()
    d_key_unit = d_key / (np.linalg.norm(d_key) + 1e-8)

    # PDB features
    from scripts.qk_space_decomposition import compute_pdb_features

    flush_print(f"\nExtracting OV outputs for {len(proteins)} proteins...")
    ov_anchors = []     # (n, 1280) -- v_anchor @ W_O per protein
    ov_actuals = []     # (n, 1280) -- actual attention-weighted output
    v_anchors = []      # (n, 64) -- anchor value vectors (pre-W_O)
    anchor_sse_list = []
    anchor_rsa_list = []
    anchor_contacts_list = []
    anchor_aa_list = []
    pids = []

    t0 = time.time()
    for i, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]

        try:
            ov_a, ov_act, v_a = extract_ov_output(model, tokenizer, seq, anchor, ov_weights, args.device)
        except Exception as e:
            flush_print(f"  ERROR on {pid}: {e}")
            continue

        ov_anchors.append(ov_a)
        ov_actuals.append(ov_act)
        v_anchors.append(v_a)
        pids.append(pid)
        anchor_aa_list.append(seq[anchor])

        sse = ss_dict.get(pid, "C" * len(seq))
        anchor_sse_list.append(sse[anchor] if anchor < len(sse) else "C")

        pdb_feats = compute_pdb_features(pid, seq)
        if pdb_feats is not None and anchor in pdb_feats:
            anchor_rsa_list.append(pdb_feats[anchor]["rsa"])
            anchor_contacts_list.append(pdb_feats[anchor]["contacts_8A"])
        else:
            anchor_rsa_list.append(np.nan)
            anchor_contacts_list.append(np.nan)

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            flush_print(f"  {i+1}/{len(proteins)} ({rate:.1f}/s, ETA {(len(proteins)-i-1)/rate:.0f}s)")

    OV_anchor = np.array(ov_anchors)   # (n, 1280)
    OV_actual = np.array(ov_actuals)   # (n, 1280)
    V_anchor = np.array(v_anchors)     # (n, 64)
    sse_arr = np.array(anchor_sse_list)
    rsa_arr = np.array(anchor_rsa_list)
    contacts_arr = np.array(anchor_contacts_list)
    aa_arr = np.array(anchor_aa_list)
    n = len(OV_anchor)
    flush_print(f"  {n} proteins collected in {time.time()-t0:.0f}s")

    # ===================================================================
    # Sanity check: how close is ov_anchor to ov_actual?
    # ===================================================================
    flush_print("\n=== Sanity: anchor-only vs actual output ===")
    cos_sims = []
    for i in range(n):
        cos = np.dot(OV_anchor[i], OV_actual[i]) / (np.linalg.norm(OV_anchor[i]) * np.linalg.norm(OV_actual[i]) + 1e-8)
        cos_sims.append(cos)
    cos_sims = np.array(cos_sims)
    flush_print(f"  Cosine(ov_anchor, ov_actual): mean={cos_sims.mean():.4f}, min={cos_sims.min():.4f}, max={cos_sims.max():.4f}")
    flush_print(f"  (1.0 = rank-1 approximation is perfect)")

    # ===================================================================
    # PCA on OV output (1280-dim)
    # ===================================================================
    flush_print("\n=== PCA on OV output (1280-dim, one vector per protein) ===")
    pca_ov = PCA(n_components=min(20, n))
    OV_pca = pca_ov.fit_transform(OV_anchor)
    flush_print(f"  Variance explained (top 10): {pca_ov.explained_variance_ratio_[:10].round(4)}")
    flush_print(f"  Cumulative: {np.cumsum(pca_ov.explained_variance_ratio_[:10]).round(4)}")

    # Effective rank
    eig_frac = pca_ov.explained_variance_ratio_
    p = eig_frac[eig_frac > 1e-10]
    p = p / p.sum()
    eff_rank = float(np.exp(-np.sum(p * np.log(p))))
    flush_print(f"  Effective rank: {eff_rank:.2f}")

    # ===================================================================
    # PCA on value vectors (64-dim)
    # ===================================================================
    flush_print("\n=== PCA on anchor value vectors (64-dim) ===")
    pca_v = PCA(n_components=min(20, n))
    V_pca = pca_v.fit_transform(V_anchor)
    flush_print(f"  Variance explained (top 10): {pca_v.explained_variance_ratio_[:10].round(4)}")
    flush_print(f"  Cumulative: {np.cumsum(pca_v.explained_variance_ratio_[:10]).round(4)}")

    # ===================================================================
    # What correlates with OV PCs?
    # ===================================================================
    flush_print("\n=== OV PC correlations ===")
    has_pdb = ~np.isnan(rsa_arr)

    for pc_i in range(min(5, OV_pca.shape[1])):
        for prop_name, prop_vals, mask in [
            ("RSA", rsa_arr, has_pdb),
            ("contacts", contacts_arr, has_pdb),
        ]:
            if mask.sum() < 20:
                continue
            rho, p = sp_stats.spearmanr(OV_pca[mask, pc_i], prop_vals[mask])
            if abs(rho) > 0.1:
                flush_print(f"  OV-PC{pc_i+1} vs {prop_name}: rho={rho:.4f}, p={p:.2e}")
        for sse_label in ["H", "E"]:
            rho, p = sp_stats.spearmanr(OV_pca[:, pc_i], (sse_arr == sse_label).astype(float))
            if abs(rho) > 0.1:
                flush_print(f"  OV-PC{pc_i+1} vs is_{sse_label}: rho={rho:.4f}, p={p:.2e}")

    # Amino acid identity -- does the OV output encode which AA the anchor is?
    flush_print("\n=== Amino acid identity in OV space ===")
    unique_aa, aa_counts = np.unique(aa_arr, return_counts=True)
    flush_print(f"  Anchor AA distribution: {dict(zip(unique_aa[np.argsort(-aa_counts)][:10], aa_counts[np.argsort(-aa_counts)][:10]))}")

    # For each common AA, compute mean OV vector and check separation
    common_aas = unique_aa[aa_counts >= 10]
    if len(common_aas) >= 2:
        aa_means = {}
        for aa in common_aas:
            mask_aa = aa_arr == aa
            aa_means[aa] = OV_anchor[mask_aa].mean(axis=0)

        # Between-AA variance / total variance
        grand_mean = OV_anchor.mean(axis=0)
        between_var = sum(((aa_arr == aa).sum() * np.sum((aa_means[aa] - grand_mean)**2)) for aa in common_aas)
        total_var = np.sum((OV_anchor - grand_mean)**2)
        aa_var_ratio = between_var / total_var
        flush_print(f"  AA between-group variance ratio: {aa_var_ratio:.4f}")

        # Same for SSE
        sse_means = {}
        for s in ["H", "E", "C"]:
            mask_s = sse_arr == s
            if mask_s.sum() >= 5:
                sse_means[s] = OV_anchor[mask_s].mean(axis=0)
        between_var_sse = sum(((sse_arr == s).sum() * np.sum((sse_means[s] - grand_mean)**2)) for s in sse_means)
        sse_var_ratio = between_var_sse / total_var
        flush_print(f"  SSE between-group variance ratio: {sse_var_ratio:.4f}")

    # ===================================================================
    # Figures
    # ===================================================================
    flush_print("\nGenerating figures...")
    sse_colors_map = {"H": "#E07B54", "E": "#5B8FA8", "C": "#AAAAAA"}

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    # Panel A: OV PC1 vs PC2, colored by SSE
    ax = axes[0, 0]
    for s, color in sse_colors_map.items():
        mask = sse_arr == s
        ax.scatter(OV_pca[mask, 0], OV_pca[mask, 1], s=25, alpha=0.6, c=color, label=f"SSE={s}", edgecolors="white", linewidths=0.3)
    ax.set_xlabel(f"PC1 ({pca_ov.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_ov.explained_variance_ratio_[1]:.1%})")
    ax.set_title("A. OV output PC1 vs PC2 (SSE)")
    ax.legend(fontsize=8)

    # Panel B: OV PC1 vs PC2, colored by amino acid
    ax = axes[0, 1]
    top_aas = unique_aa[np.argsort(-aa_counts)][:8]
    aa_cmap = plt.cm.tab10(np.linspace(0, 1, len(top_aas)))
    for j, aa in enumerate(top_aas):
        mask = aa_arr == aa
        ax.scatter(OV_pca[mask, 0], OV_pca[mask, 1], s=25, alpha=0.6, c=[aa_cmap[j]], label=f"{aa} (n={mask.sum()})", edgecolors="white", linewidths=0.3)
    other_mask = ~np.isin(aa_arr, top_aas)
    if other_mask.any():
        ax.scatter(OV_pca[other_mask, 0], OV_pca[other_mask, 1], s=15, alpha=0.3, c="#CCCCCC", edgecolors="white", linewidths=0.3, label="other")
    ax.set_xlabel(f"PC1 ({pca_ov.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_ov.explained_variance_ratio_[1]:.1%})")
    ax.set_title("B. OV output PC1 vs PC2 (amino acid)")
    ax.legend(fontsize=7, ncol=2, loc="upper right")

    # Panel C: OV PC1 vs PC2, colored by RSA
    ax = axes[0, 2]
    valid_rsa = has_pdb
    if valid_rsa.any():
        sc = ax.scatter(OV_pca[valid_rsa, 0], OV_pca[valid_rsa, 1], s=25, alpha=0.6, c=rsa_arr[valid_rsa], cmap="coolwarm_r", vmin=0, vmax=0.5, edgecolors="white", linewidths=0.3)
        plt.colorbar(sc, ax=ax, label="RSA")
    ax.set_xlabel(f"PC1 ({pca_ov.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_ov.explained_variance_ratio_[1]:.1%})")
    ax.set_title("C. OV output PC1 vs PC2 (RSA)")

    # Panel D: Value vector PCA (64-dim), colored by SSE
    ax = axes[1, 0]
    for s, color in sse_colors_map.items():
        mask = sse_arr == s
        ax.scatter(V_pca[mask, 0], V_pca[mask, 1], s=25, alpha=0.6, c=color, label=f"SSE={s}", edgecolors="white", linewidths=0.3)
    ax.set_xlabel(f"PC1 ({pca_v.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_v.explained_variance_ratio_[1]:.1%})")
    ax.set_title("D. Value vectors PC1 vs PC2 (SSE)")
    ax.legend(fontsize=8)

    # Panel E: Value vector PCA, colored by AA
    ax = axes[1, 1]
    for j, aa in enumerate(top_aas):
        mask = aa_arr == aa
        ax.scatter(V_pca[mask, 0], V_pca[mask, 1], s=25, alpha=0.6, c=[aa_cmap[j]], label=f"{aa} (n={mask.sum()})", edgecolors="white", linewidths=0.3)
    if other_mask.any():
        ax.scatter(V_pca[other_mask, 0], V_pca[other_mask, 1], s=15, alpha=0.3, c="#CCCCCC", edgecolors="white", linewidths=0.3, label="other")
    ax.set_xlabel(f"PC1 ({pca_v.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_v.explained_variance_ratio_[1]:.1%})")
    ax.set_title("E. Value vectors PC1 vs PC2 (amino acid)")
    ax.legend(fontsize=7, ncol=2, loc="upper right")

    # Panel F: Eigenspectrum comparison
    ax = axes[1, 2]
    n_show = min(20, len(pca_ov.explained_variance_ratio_))
    ax.semilogy(np.arange(1, n_show + 1), pca_ov.explained_variance_ratio_[:n_show], "o-", ms=4, color="#5B7FA3", label="OV output (1280-dim)")
    n_show_v = min(20, len(pca_v.explained_variance_ratio_))
    ax.semilogy(np.arange(1, n_show_v + 1), pca_v.explained_variance_ratio_[:n_show_v], "o-", ms=4, color="#D64550", label="Value vectors (64-dim)")
    ax.set_xlabel("PC index")
    ax.set_ylabel("Fraction of variance")
    ax.set_title(f"F. Eigenspectra (OV eff-rank={eff_rank:.1f})")
    ax.legend(fontsize=8)

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out_path = REPORT_DIR / "ov_output_pca.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_path}")

    flush_print("\nDone.")


if __name__ == "__main__":
    main()
