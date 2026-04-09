#!/usr/bin/env python3
"""QK space decomposition for L10H9.

Three analyses:
  1. Key-space PCA visualization (anchor vs non-anchor, colored by structural features)
  2. Contrastive covariance: which structural binary feature produces Delta_k most aligned with d?
  3. Eigenspectrum of anchor key covariance + subspace correlation with structural properties

Usage:
    PYTHONUNBUFFERED=1 uv run python scripts/qk_space_decomposition.py --device cuda
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

# Max ASA for RSA (Tien et al. 2013)
MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


# ---------------------------------------------------------------------------
# Model + weights (reused from anchor_behavior_audit.py)
# ---------------------------------------------------------------------------

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


def extract_head_weights(model, layer: int, head: int) -> dict:
    attn = model._model.esm.encoder.layer[layer].attention
    W_Q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_Q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    W_K = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_K = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    return {
        "W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(),
        "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone(),
    }


def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Compute d = W_K^T @ q_mean_norm from reference protein."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    q_all = x_ln @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    return q_mean_norm  # Return the normalized mean query direction (in head space)


# ---------------------------------------------------------------------------
# PDB features (minimal, reused from v4)
# ---------------------------------------------------------------------------

def _parse_pdb_residues(pdb_path):
    from Bio.PDB import PDBParser
    from Bio.Data.IUPACData import protein_letters_3to1

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("prot", str(pdb_path))
    chain = list(structure[0])[0]

    results = []
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        resid = residue.get_id()[1]
        aa = three_to_one(residue.get_resname())
        if aa == "X":
            continue
        ca = residue["CA"].get_vector().get_array() if "CA" in residue else None
        cb = residue["CB"].get_vector().get_array() if "CB" in residue else ca
        if ca is None:
            continue
        results.append({"resid": resid, "aa": aa, "ca": ca, "cb": cb})
    return results, structure


def _align_pdb_to_seq(pdb_residues, full_seq):
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues]
    resids = [t[0] for t in pdb_tuples]
    n_seq = len(full_seq)
    min_resid, max_resid = min(resids), max(resids)

    best_offset, best_matches = 0, 0
    for offset in range(-max_resid, n_seq - min_resid + 1):
        matches = sum(1 for resid, aa in pdb_tuples if 0 <= resid + offset < n_seq and full_seq[resid + offset] == aa)
        if matches > best_matches:
            best_offset, best_matches = offset, matches

    mapping = {}
    for i, (resid, aa) in enumerate(pdb_tuples):
        seq_pos = resid + best_offset
        if 0 <= seq_pos < n_seq and full_seq[seq_pos] == aa:
            mapping[i] = seq_pos
    return mapping


def compute_pdb_features(protein, full_seq):
    """Returns dict: seq_pos -> {rsa, contacts_8A, long_range_fraction} or None."""
    pdb_path = PDB_DIR / f"{protein[:4]}.pdb"
    if not pdb_path.exists():
        return None

    try:
        pdb_residues, structure = _parse_pdb_residues(pdb_path)
    except Exception:
        return None
    if not pdb_residues:
        return None

    mapping = _align_pdb_to_seq(pdb_residues, full_seq)
    if len(mapping) < len(pdb_residues) * 0.5:
        return None

    from Bio.PDB import ShrakeRupley
    sr = ShrakeRupley()
    try:
        sr.compute(structure[0], level="R")
    except Exception:
        return None
    chain = list(structure[0])[0]
    sasa_by_resid = {}
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa

    from scipy.spatial.distance import cdist
    cb_coords = np.array([r["cb"] for r in pdb_residues])
    dists = cdist(cb_coords, cb_coords)
    n_pdb = len(pdb_residues)

    contacts_8A_arr = (dists < 8.0).sum(axis=1) - 1
    long_range_arr = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) > 12 and dists[i, j] < 8.0:
                long_range_arr[i] += 1
    long_range_frac = long_range_arr / np.maximum(contacts_8A_arr, 1).astype(float)

    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_residues[pdb_idx]
        aa = full_seq[seq_pos]
        max_asa = MAX_ASA.get(aa, 200)
        sasa = sasa_by_resid.get(r["resid"], 0)
        rsa = min(sasa / max_asa, 1.0) if max_asa > 0 else 0.0

        features[seq_pos] = {
            "rsa": rsa,
            "contacts_8A": int(contacts_8A_arr[pdb_idx]),
            "long_range_fraction": float(long_range_frac[pdb_idx]),
        }

    return features


# ---------------------------------------------------------------------------
# Data selection
# ---------------------------------------------------------------------------

def select_confident_proteins(seqs, ss_dict, min_top1_mass=0.5):
    """Select proteins where top-1 residue gets >50% of L10H9 attention mass."""
    rows = []
    with open(AUDIT_CSV) as f:
        for r in csv.DictReader(f):
            pid = r["protein"]
            if pid not in seqs or pid not in ss_dict:
                continue
            if len(seqs[pid]) != len(ss_dict[pid]):
                continue
            mass = float(r["top1_mass"])
            if mass < min_top1_mass:
                continue
            anchor_pos = int(r["top_key_idx"])
            rows.append({"protein": pid, "anchor_pos": anchor_pos, "top1_mass": mass, "n_res": len(seqs[pid])})
    rows.sort(key=lambda x: x["top1_mass"], reverse=True)
    return rows


# ---------------------------------------------------------------------------
# Extract key and query vectors for one protein
# ---------------------------------------------------------------------------

@torch.no_grad()
def extract_qk_vectors(model, tokenizer, sequence: str, weights: dict, device: str):
    """Extract full key and query vectors (R^64) for all residues of one protein.

    Returns:
        k_Ld: (n_res, 64) key vectors
        q_Ld: (n_res, 64) query vectors
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0, 1:-1]  # (n_res, 1280)

    W_Q = weights["W_Q_hd"]  # (64, 1280)
    b_Q = weights["b_Q_d"]   # (64,)
    W_K = weights["W_K_hd"]  # (64, 1280)
    b_K = weights["b_K_d"]   # (64,)

    q_Ld = x_ln @ W_Q.T + b_Q  # (n_res, 64)
    k_Ld = x_ln @ W_K.T + b_K  # (n_res, 64)

    return k_Ld.float().numpy(), q_Ld.float().numpy()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-proteins", type=int, default=0, help="0 = all confident proteins")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    flush_print("Loading sequences and secondary structure...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")

    seqs = {k: v for k, v in all_seqs.items() if 100 <= len(v) <= 500}
    flush_print(f"  {len(seqs)} proteins in 100-500 residue range")

    proteins = select_confident_proteins(seqs, ss_dict, min_top1_mass=0.5)
    if args.max_proteins > 0:
        proteins = proteins[:args.max_proteins]
    flush_print(f"  {len(proteins)} confident proteins selected (top1_mass > 0.5)")

    flush_print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    # Compute search direction d (normalized mean query in head space)
    flush_print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    q_mean_norm = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    # d in residual-stream space = W_K^T @ q_mean_norm, but for key-space analysis
    # we want d in key space = q_mean_norm itself (since k^T q = (W_K x)^T q_mean_norm)
    d_key = q_mean_norm.numpy()  # (64,) direction in key space
    d_key_unit = d_key / (np.linalg.norm(d_key) + 1e-8)

    # -----------------------------------------------------------------------
    # Collect key/query vectors and labels for all proteins
    # -----------------------------------------------------------------------
    flush_print(f"\nExtracting Q/K vectors for {len(proteins)} proteins...")
    all_keys = []       # list of (n_res, 64) arrays
    all_queries = []    # list of (n_res, 64) arrays
    all_is_anchor = []  # list of (n_res,) bool arrays
    all_sse = []        # list of (n_res,) char arrays
    all_rsa = []        # list of (n_res,) float arrays (NaN if no PDB)
    all_contacts = []   # list of (n_res,) float arrays (NaN if no PDB)
    all_lrf = []        # list of (n_res,) float arrays (NaN if no PDB)
    all_proj = []       # list of (n_res,) float arrays (k . d)
    all_protein_ids = []

    n_with_pdb = 0
    t0 = time.time()

    for i, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        n_res = len(seq)

        try:
            k_Ld, q_Ld = extract_qk_vectors(model, tokenizer, seq, weights, args.device)
        except Exception as e:
            flush_print(f"  ERROR on {pid}: {e}")
            continue

        # Labels
        is_anchor = np.zeros(n_res, dtype=bool)
        is_anchor[anchor] = True

        sse_arr = np.array(list(ss_dict[pid][:n_res])) if pid in ss_dict and len(ss_dict[pid]) >= n_res else np.full(n_res, "C")

        rsa_arr = np.full(n_res, np.nan)
        contacts_arr = np.full(n_res, np.nan)
        lrf_arr = np.full(n_res, np.nan)

        pdb_feats = compute_pdb_features(pid, seq)
        if pdb_feats is not None:
            n_with_pdb += 1
            for pos, feats in pdb_feats.items():
                if isinstance(pos, int) and 0 <= pos < n_res:
                    rsa_arr[pos] = feats["rsa"]
                    contacts_arr[pos] = feats["contacts_8A"]
                    lrf_arr[pos] = feats["long_range_fraction"]

        proj_arr = k_Ld @ d_key_unit  # (n_res,) projection of each key onto d

        all_keys.append(k_Ld)
        all_queries.append(q_Ld)
        all_is_anchor.append(is_anchor)
        all_sse.append(sse_arr)
        all_rsa.append(rsa_arr)
        all_contacts.append(contacts_arr)
        all_lrf.append(lrf_arr)
        all_proj.append(proj_arr)
        all_protein_ids.append(np.full(n_res, pid))

        if (i + 1) % 100 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (len(proteins) - i - 1) / rate
            flush_print(f"  {i+1}/{len(proteins)} done ({rate:.1f} prot/s, ETA {eta:.0f}s)")

    elapsed = time.time() - t0
    flush_print(f"  Collected from {len(all_keys)} proteins in {elapsed:.0f}s ({n_with_pdb} with PDB features)")

    # Concatenate
    K = np.concatenate(all_keys, axis=0)        # (N, 64)
    Q = np.concatenate(all_queries, axis=0)      # (N, 64)
    is_anchor = np.concatenate(all_is_anchor)    # (N,)
    sse = np.concatenate(all_sse)                # (N,)
    rsa = np.concatenate(all_rsa)                # (N,)
    contacts = np.concatenate(all_contacts)      # (N,)
    lrf = np.concatenate(all_lrf)                # (N,)
    proj = np.concatenate(all_proj)              # (N,)
    protein_ids = np.concatenate(all_protein_ids) # (N,)

    N = K.shape[0]
    n_anchors = is_anchor.sum()
    flush_print(f"\nTotal vectors: {N} ({n_anchors} anchor, {N - n_anchors} non-anchor)")

    # ===================================================================
    # Analysis 1: Key-space PCA visualization
    # ===================================================================
    flush_print("\n=== Analysis 1: Key-space PCA ===")

    pca_k = PCA(n_components=10)
    K_pca = pca_k.fit_transform(K)  # (N, 10)
    flush_print(f"  Key PCA explained variance (top 10): {pca_k.explained_variance_ratio_[:10].round(4)}")
    flush_print(f"  Cumulative: {np.cumsum(pca_k.explained_variance_ratio_[:10]).round(4)}")

    # Check alignment of d with PCA components
    d_in_pca = pca_k.transform(d_key_unit.reshape(1, -1))[0]
    d_pca_norm = d_in_pca / (np.linalg.norm(d_in_pca) + 1e-8)
    flush_print(f"  Search direction d projected onto top-10 PCs: {d_in_pca[:5].round(4)}")
    flush_print(f"  d weight in PC1-3: {np.abs(d_pca_norm[:3]).round(4)}")

    # How much key-space variance does anchor/non-anchor explain?
    anchor_mean = K[is_anchor].mean(axis=0)
    non_anchor_mean = K[~is_anchor].mean(axis=0)
    grand_mean = K.mean(axis=0)
    between_var = n_anchors * np.sum((anchor_mean - grand_mean)**2) + (N - n_anchors) * np.sum((non_anchor_mean - grand_mean)**2)
    total_var = np.sum((K - grand_mean)**2)
    anchor_var_explained = between_var / total_var
    flush_print(f"  Anchor/non-anchor between-group variance ratio: {anchor_var_explained:.6f}")

    # Subsample for plotting (too many points otherwise)
    rng = np.random.RandomState(42)
    max_plot = 50000
    if N > max_plot:
        non_anchor_idx = np.where(~is_anchor)[0]
        sample_idx = rng.choice(non_anchor_idx, min(max_plot, len(non_anchor_idx)), replace=False)
        plot_idx = np.concatenate([np.where(is_anchor)[0], sample_idx])
    else:
        plot_idx = np.arange(N)

    # --- Key PCA figure: 4 panels ---
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Panel A: anchor vs non-anchor (PC1 vs PC2)
    ax = axes[0, 0]
    mask_na = ~is_anchor[plot_idx]
    mask_a = is_anchor[plot_idx]
    ax.scatter(K_pca[plot_idx[mask_na], 0], K_pca[plot_idx[mask_na], 1], s=1, alpha=0.05, c="#8899AA", rasterized=True, label="non-anchor")
    ax.scatter(K_pca[plot_idx[mask_a], 0], K_pca[plot_idx[mask_a], 1], s=15, alpha=0.7, c="#D64550", zorder=5, label="anchor")
    ax.set_xlabel(f"PC1 ({pca_k.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_k.explained_variance_ratio_[1]:.1%})")
    ax.set_title("A. Key vectors: anchor vs non-anchor")
    ax.legend(markerscale=3, loc="upper right")

    # Panel B: SSE type
    ax = axes[0, 1]
    sse_colors = {"H": "#E07B54", "E": "#5B8FA8", "C": "#AAAAAA"}
    for s, color in sse_colors.items():
        mask_s = sse[plot_idx] == s
        ax.scatter(K_pca[plot_idx[mask_s], 0], K_pca[plot_idx[mask_s], 1], s=1, alpha=0.05, c=color, rasterized=True, label=f"SSE={s}")
    # Overlay anchors colored by SSE
    for s, color in sse_colors.items():
        mask_sa = is_anchor[plot_idx] & (sse[plot_idx] == s)
        if mask_sa.any():
            ax.scatter(K_pca[plot_idx[mask_sa], 0], K_pca[plot_idx[mask_sa], 1], s=30, alpha=0.8, c=color, edgecolors="black", linewidths=0.5, zorder=5)
    ax.set_xlabel(f"PC1 ({pca_k.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_k.explained_variance_ratio_[1]:.1%})")
    ax.set_title("B. Key vectors colored by SSE type")
    ax.legend(markerscale=3, loc="upper right")

    # Panel C: RSA bin
    ax = axes[1, 0]
    has_rsa = ~np.isnan(rsa[plot_idx])
    rsa_plot = rsa[plot_idx]
    rsa_colors = np.full(len(plot_idx), "#CCCCCC", dtype=object)
    rsa_colors[has_rsa & (rsa_plot < 0.05)] = "#2C5F8A"    # buried
    rsa_colors[has_rsa & (rsa_plot >= 0.05) & (rsa_plot < 0.25)] = "#7BA7C9"  # intermediate
    rsa_colors[has_rsa & (rsa_plot >= 0.25)] = "#E8A838"    # exposed
    for label, color, mask_fn in [
        ("buried (RSA<0.05)", "#2C5F8A", lambda r, h: h & (r < 0.05)),
        ("intermediate", "#7BA7C9", lambda r, h: h & (r >= 0.05) & (r < 0.25)),
        ("exposed (RSA>0.25)", "#E8A838", lambda r, h: h & (r >= 0.25)),
    ]:
        mask_r = mask_fn(rsa_plot, has_rsa)
        ax.scatter(K_pca[plot_idx[mask_r], 0], K_pca[plot_idx[mask_r], 1], s=1, alpha=0.05, c=color, rasterized=True, label=label)
    # Overlay anchors
    anchor_plot_mask = is_anchor[plot_idx] & has_rsa
    if anchor_plot_mask.any():
        a_rsa = rsa_plot[anchor_plot_mask]
        a_colors = np.where(a_rsa < 0.05, "#2C5F8A", np.where(a_rsa < 0.25, "#7BA7C9", "#E8A838"))
        ax.scatter(K_pca[plot_idx[anchor_plot_mask], 0], K_pca[plot_idx[anchor_plot_mask], 1], s=30, alpha=0.8, c=a_colors, edgecolors="black", linewidths=0.5, zorder=5)
    ax.set_xlabel(f"PC1 ({pca_k.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_k.explained_variance_ratio_[1]:.1%})")
    ax.set_title("C. Key vectors colored by RSA bin")
    ax.legend(markerscale=3, loc="upper right")

    # Panel D: contacts_8A tercile
    ax = axes[1, 1]
    has_c = ~np.isnan(contacts[plot_idx])
    c_plot = contacts[plot_idx]
    c_valid = contacts[~np.isnan(contacts)]
    c_t1 = np.percentile(c_valid, 33.3) if len(c_valid) > 0 else 10
    c_t2 = np.percentile(c_valid, 66.7) if len(c_valid) > 0 else 20
    for label, color, mask_fn in [
        (f"low contacts (<{c_t1:.0f})", "#6BBF8A", lambda c, h: h & (c < c_t1)),
        (f"med contacts", "#C9A85B", lambda c, h: h & (c >= c_t1) & (c < c_t2)),
        (f"high contacts (>{c_t2:.0f})", "#B85450", lambda c, h: h & (c >= c_t2)),
    ]:
        mask_c = mask_fn(c_plot, has_c)
        ax.scatter(K_pca[plot_idx[mask_c], 0], K_pca[plot_idx[mask_c], 1], s=1, alpha=0.05, c=color, rasterized=True, label=label)
    # Overlay anchors
    anchor_c_mask = is_anchor[plot_idx] & has_c
    if anchor_c_mask.any():
        a_c = c_plot[anchor_c_mask]
        a_colors = np.where(a_c < c_t1, "#6BBF8A", np.where(a_c < c_t2, "#C9A85B", "#B85450"))
        ax.scatter(K_pca[plot_idx[anchor_c_mask], 0], K_pca[plot_idx[anchor_c_mask], 1], s=30, alpha=0.8, c=a_colors, edgecolors="black", linewidths=0.5, zorder=5)
    ax.set_xlabel(f"PC1 ({pca_k.explained_variance_ratio_[0]:.1%})")
    ax.set_ylabel(f"PC2 ({pca_k.explained_variance_ratio_[1]:.1%})")
    ax.set_title("D. Key vectors colored by contact count")
    ax.legend(markerscale=3, loc="upper right")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out_key_pca = REPORT_DIR / "qk_key_pca.png"
    fig.savefig(out_key_pca, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_key_pca}")

    # --- Query PCA figure ---
    flush_print("\n  Query PCA...")
    pca_q = PCA(n_components=5)
    Q_pca = pca_q.fit_transform(Q)
    flush_print(f"  Query PCA explained variance (top 5): {pca_q.explained_variance_ratio_[:5].round(4)}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    # Queries colored by protein
    unique_pids = np.unique(protein_ids)
    pid_colors = plt.cm.tab20(np.linspace(0, 1, min(20, len(unique_pids))))
    ax1.scatter(Q_pca[plot_idx, 0], Q_pca[plot_idx, 1], s=1, alpha=0.05, c="#8899AA", rasterized=True)
    ax1.set_xlabel(f"PC1 ({pca_q.explained_variance_ratio_[0]:.1%})")
    ax1.set_ylabel(f"PC2 ({pca_q.explained_variance_ratio_[1]:.1%})")
    ax1.set_title("Query vectors (all proteins)")

    # Query norms histogram
    q_norms = np.linalg.norm(Q, axis=1)
    ax2.hist(q_norms, bins=100, color="#5B7FA3", edgecolor="white", linewidth=0.3)
    ax2.set_xlabel("Query vector norm")
    ax2.set_ylabel("Count")
    ax2.set_title("Query vector norm distribution")
    # Check query alignment: mean pairwise cosine similarity of per-protein mean queries
    per_protein_q_mean = []
    for q_arr in all_queries:
        qm = q_arr.mean(axis=0)
        qm = qm / (np.linalg.norm(qm) + 1e-8)
        per_protein_q_mean.append(qm)
    per_protein_q_mean = np.array(per_protein_q_mean)
    cos_sim_matrix = per_protein_q_mean @ per_protein_q_mean.T
    upper_tri = cos_sim_matrix[np.triu_indices_from(cos_sim_matrix, k=1)]
    ax2.text(0.05, 0.95, f"Cross-protein mean query\ncosine similarity: {upper_tri.mean():.4f} +/- {upper_tri.std():.4f}", transform=ax2.transAxes, va="top", fontsize=8)

    for ax in (ax1, ax2):
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    plt.tight_layout()
    out_query_pca = REPORT_DIR / "qk_query_pca.png"
    fig.savefig(out_query_pca, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_query_pca}")

    # ===================================================================
    # Analysis 2: Contrastive covariance
    # ===================================================================
    flush_print("\n=== Analysis 2: Contrastive covariance ===")

    has_pdb = ~np.isnan(rsa)
    c_valid_all = contacts[has_pdb]
    c_t1_all = np.percentile(c_valid_all, 33.3)
    c_t2_all = np.percentile(c_valid_all, 66.7)
    lrf_valid = lrf[has_pdb & ~np.isnan(lrf)]
    lrf_t1 = np.percentile(lrf_valid, 33.3) if len(lrf_valid) > 0 else 0.3
    lrf_t2 = np.percentile(lrf_valid, 66.7) if len(lrf_valid) > 0 else 0.6

    # Define binary features z1
    contrasts = {}
    # 1. anchor vs non-anchor
    contrasts["anchor vs non-anchor"] = (is_anchor, ~is_anchor, np.ones(N, dtype=bool))
    # 2. buried vs exposed (among positions with PDB data)
    mask_buried = has_pdb & (rsa < 0.05)
    mask_exposed = has_pdb & (rsa > 0.25)
    contrasts["buried vs exposed"] = (mask_buried, mask_exposed, mask_buried | mask_exposed)
    # 3. high contacts vs low contacts
    mask_high_c = has_pdb & (contacts >= c_t2_all)
    mask_low_c = has_pdb & (contacts < c_t1_all)
    contrasts["high vs low contacts"] = (mask_high_c, mask_low_c, mask_high_c | mask_low_c)
    # 4. helix vs strand
    mask_H = sse == "H"
    mask_E = sse == "E"
    contrasts["helix vs strand"] = (mask_H, mask_E, mask_H | mask_E)
    # 5. high long-range fraction vs low
    mask_high_lrf = has_pdb & ~np.isnan(lrf) & (lrf >= lrf_t2)
    mask_low_lrf = has_pdb & ~np.isnan(lrf) & (lrf < lrf_t1)
    contrasts["high vs low long-range frac"] = (mask_high_lrf, mask_low_lrf, mask_high_lrf | mask_low_lrf)
    # 6. high d-projection vs low
    proj_t1 = np.percentile(proj, 33.3)
    proj_t2 = np.percentile(proj, 66.7)
    mask_high_proj = proj >= proj_t2
    mask_low_proj = proj < proj_t1
    contrasts["high vs low d-projection"] = (mask_high_proj, mask_low_proj, mask_high_proj | mask_low_proj)

    results_contrast = {}
    for name, (mask_pos, mask_neg, mask_valid) in contrasts.items():
        n_pos = mask_pos.sum()
        n_neg = mask_neg.sum()
        if n_pos < 10 or n_neg < 10:
            flush_print(f"  {name}: skipped (n_pos={n_pos}, n_neg={n_neg})")
            continue

        k_pos_mean = K[mask_pos].mean(axis=0)
        k_neg_mean = K[mask_neg].mean(axis=0)
        delta_k = k_pos_mean - k_neg_mean
        delta_k_norm = np.linalg.norm(delta_k)
        delta_k_unit = delta_k / (delta_k_norm + 1e-8)

        # Cosine similarity between delta_k and d
        cos_with_d = float(np.dot(delta_k_unit, d_key_unit))

        # How much of the anchor-vs-nonanchor mean difference does this z1 explain?
        anchor_delta = K[is_anchor].mean(axis=0) - K[~is_anchor].mean(axis=0)
        anchor_delta_norm = np.linalg.norm(anchor_delta)
        cos_with_anchor_delta = float(np.dot(delta_k_unit, anchor_delta / (anchor_delta_norm + 1e-8)))

        # Explained variance: project all keys onto delta_k, compute between-group variance ratio
        proj_on_delta = K @ delta_k_unit
        between_v = n_pos * (proj_on_delta[mask_pos].mean() - proj_on_delta[mask_valid].mean())**2 + n_neg * (proj_on_delta[mask_neg].mean() - proj_on_delta[mask_valid].mean())**2
        total_v = np.sum((proj_on_delta[mask_valid] - proj_on_delta[mask_valid].mean())**2)
        var_ratio = between_v / (total_v + 1e-8)

        results_contrast[name] = {
            "n_pos": int(n_pos), "n_neg": int(n_neg),
            "delta_k_norm": float(delta_k_norm),
            "cos_with_d": cos_with_d,
            "cos_with_anchor_delta": cos_with_anchor_delta,
            "explained_var_ratio": float(var_ratio),
        }
        flush_print(f"  {name}: cos(delta_k, d)={cos_with_d:.4f}, cos(delta_k, anchor_delta)={cos_with_anchor_delta:.4f}, delta_k_norm={delta_k_norm:.4f}, var_ratio={var_ratio:.4f}")

    # --- Contrastive alignment bar chart ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    names = list(results_contrast.keys())
    cos_d_vals = [results_contrast[n]["cos_with_d"] for n in names]
    cos_anchor_vals = [results_contrast[n]["cos_with_anchor_delta"] for n in names]

    x = np.arange(len(names))
    w = 0.35
    ax1.barh(x - w/2, cos_d_vals, height=w, color="#5B7FA3", label="cos(delta_k, d)")
    ax1.barh(x + w/2, cos_anchor_vals, height=w, color="#D64550", label="cos(delta_k, anchor_delta)")
    ax1.set_yticks(x)
    ax1.set_yticklabels(names, fontsize=8)
    ax1.set_xlabel("Cosine similarity")
    ax1.set_title("Alignment of contrast directions with d and anchor direction")
    ax1.legend(fontsize=8)
    ax1.axvline(0, color="gray", lw=0.5)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    var_ratios = [results_contrast[n]["explained_var_ratio"] for n in names]
    ax2.barh(x, var_ratios, color="#6BBF8A")
    ax2.set_yticks(x)
    ax2.set_yticklabels(names, fontsize=8)
    ax2.set_xlabel("Between-group variance ratio along delta_k")
    ax2.set_title("Separability of each binary contrast in key space")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    plt.tight_layout()
    out_contrast = REPORT_DIR / "qk_contrastive_alignment.png"
    fig.savefig(out_contrast, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_contrast}")

    # ===================================================================
    # Analysis 3: Eigenspectrum and subspace structure
    # ===================================================================
    flush_print("\n=== Analysis 3: Eigenspectrum ===")

    K_anchor = K[is_anchor]
    K_non_anchor = K[~is_anchor]
    flush_print(f"  Anchor keys: {K_anchor.shape[0]}, Non-anchor keys: {K_non_anchor.shape[0]}")

    # Center and compute covariance
    K_anchor_centered = K_anchor - K_anchor.mean(axis=0)
    K_non_centered = K_non_anchor - K_non_anchor.mean(axis=0)

    cov_anchor = np.cov(K_anchor_centered.T)   # (64, 64)
    cov_non = np.cov(K_non_centered.T)         # (64, 64)

    eig_anchor, evec_anchor = np.linalg.eigh(cov_anchor)
    eig_non, evec_non = np.linalg.eigh(cov_non)
    # Sort descending
    eig_anchor = eig_anchor[::-1]
    evec_anchor = evec_anchor[:, ::-1]
    eig_non = eig_non[::-1]
    evec_non = evec_non[:, ::-1]

    eig_anchor_frac = eig_anchor / eig_anchor.sum()
    eig_non_frac = eig_non / eig_non.sum()

    flush_print(f"  Anchor eigenspectrum (top 10 fraction): {eig_anchor_frac[:10].round(4)}")
    flush_print(f"  Non-anchor eigenspectrum (top 10 fraction): {eig_non_frac[:10].round(4)}")

    # Effective rank (exponential of entropy)
    def effective_rank(eig_frac):
        p = eig_frac[eig_frac > 1e-10]
        p = p / p.sum()
        return float(np.exp(-np.sum(p * np.log(p))))

    eff_rank_anchor = effective_rank(eig_anchor_frac)
    eff_rank_non = effective_rank(eig_non_frac)
    flush_print(f"  Effective rank: anchor={eff_rank_anchor:.2f}, non-anchor={eff_rank_non:.2f}")

    # Cumulative explained variance: how many components for 90%?
    cum_anchor = np.cumsum(eig_anchor_frac)
    cum_non = np.cumsum(eig_non_frac)
    n90_anchor = int(np.searchsorted(cum_anchor, 0.9) + 1)
    n90_non = int(np.searchsorted(cum_non, 0.9) + 1)
    flush_print(f"  Components for 90% variance: anchor={n90_anchor}, non-anchor={n90_non}")

    # Alignment of top eigenvectors with d
    flush_print("\n  Alignment of anchor eigenvectors with d:")
    d_alignment = []
    for i in range(min(10, 64)):
        cos = float(np.abs(np.dot(evec_anchor[:, i], d_key_unit)))
        d_alignment.append(cos)
        flush_print(f"    EV{i+1}: |cos(ev, d)| = {cos:.4f}")

    # Correlation of top eigenvectors with structural properties (among anchors with PDB)
    flush_print("\n  Correlation of anchor eigenvectors with structural properties:")
    anchor_idx = np.where(is_anchor)[0]
    anchor_has_pdb = has_pdb[anchor_idx]
    anchor_rsa = rsa[anchor_idx]
    anchor_contacts = contacts[anchor_idx]
    anchor_lrf = lrf[anchor_idx]
    anchor_sse = sse[anchor_idx]

    # Project anchor keys onto top eigenvectors
    anchor_proj_evs = K_anchor_centered @ evec_anchor[:, :10]  # (n_anchors, 10)

    subspace_corr_rows = []
    properties = {
        "RSA": anchor_rsa,
        "contacts_8A": anchor_contacts,
        "long_range_frac": anchor_lrf,
        "is_helix": (anchor_sse == "H").astype(float),
        "is_strand": (anchor_sse == "E").astype(float),
    }

    for prop_name, prop_vals in properties.items():
        valid = ~np.isnan(prop_vals) if np.issubdtype(prop_vals.dtype, np.floating) else np.ones(len(prop_vals), dtype=bool)
        if valid.sum() < 20:
            continue
        for ev_i in range(min(10, 64)):
            rho, pval = sp_stats.spearmanr(anchor_proj_evs[valid, ev_i], prop_vals[valid])
            subspace_corr_rows.append({"property": prop_name, "eigenvector": ev_i + 1, "spearman_rho": float(rho), "p_value": float(pval)})
            if abs(rho) > 0.15:
                flush_print(f"    EV{ev_i+1} vs {prop_name}: rho={rho:.4f}, p={pval:.4e}")

    # Save subspace correlations CSV
    csv_path = REPORT_DIR / "qk_subspace_correlations.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["property", "eigenvector", "spearman_rho", "p_value"])
        writer.writeheader()
        writer.writerows(subspace_corr_rows)
    flush_print(f"  Saved: {csv_path}")

    # Grassmann distance between anchor and non-anchor subspaces (top-k)
    flush_print("\n  Grassmann distance between anchor and non-anchor subspaces:")
    for k in [1, 3, 5, 10]:
        U_a = evec_anchor[:, :k]
        U_n = evec_non[:, :k]
        svals = np.linalg.svd(U_a.T @ U_n, compute_uv=False)
        svals = np.clip(svals, 0, 1)
        theta = np.arccos(svals)
        grassmann = float(np.linalg.norm(theta))
        flush_print(f"    top-{k}: Grassmann distance = {grassmann:.4f}")

    # --- Eigenspectrum figure ---
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))

    ax = axes[0]
    ax.semilogy(np.arange(1, 65), eig_anchor_frac, "o-", ms=3, color="#D64550", label=f"anchor (eff rank={eff_rank_anchor:.1f})")
    ax.semilogy(np.arange(1, 65), eig_non_frac, "o-", ms=3, color="#5B7FA3", label=f"non-anchor (eff rank={eff_rank_non:.1f})")
    ax.set_xlabel("Eigenvalue index")
    ax.set_ylabel("Fraction of variance")
    ax.set_title("Eigenspectra of key covariance")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.plot(np.arange(1, 65), cum_anchor, "-", color="#D64550", label="anchor")
    ax.plot(np.arange(1, 65), cum_non, "-", color="#5B7FA3", label="non-anchor")
    ax.axhline(0.9, color="gray", ls=":", lw=0.7)
    ax.text(n90_anchor + 1, 0.88, f"anchor: {n90_anchor}", fontsize=7, color="#D64550")
    ax.text(n90_non + 1, 0.85, f"non-anchor: {n90_non}", fontsize=7, color="#5B7FA3")
    ax.set_xlabel("Number of components")
    ax.set_ylabel("Cumulative variance fraction")
    ax.set_title("Cumulative explained variance")
    ax.legend(fontsize=8)

    ax = axes[2]
    ax.bar(np.arange(1, 11), d_alignment, color="#6BBF8A")
    ax.set_xlabel("Eigenvector index")
    ax.set_ylabel("|cos(eigenvector, d)|")
    ax.set_title("Alignment of anchor eigenvectors with d")
    ax.set_xticks(np.arange(1, 11))

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out_eigen = REPORT_DIR / "qk_eigenspectrum.png"
    fig.savefig(out_eigen, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_eigen}")

    # ===================================================================
    # Write report
    # ===================================================================
    flush_print("\n=== Writing report ===")
    report = []
    report.append("# QK Space Decomposition for L10H9\n\n")
    report.append(f"Proteins: {len(all_keys)} confident (top1_mass > 0.5) from {len(proteins)} candidates.\n")
    report.append(f"Total key/query vectors: {N} ({n_anchors} anchor, {N - n_anchors} non-anchor).\n")
    report.append(f"Proteins with PDB features: {n_with_pdb}.\n\n")

    report.append("## Analysis 1: Key-space PCA\n\n")
    report.append(f"PCA on {N} key vectors in R^64.\n\n")
    report.append("| PC | Variance explained | Cumulative |\n|---|---|---|\n")
    for i in range(10):
        report.append(f"| PC{i+1} | {pca_k.explained_variance_ratio_[i]:.4f} | {np.cumsum(pca_k.explained_variance_ratio_)[i]:.4f} |\n")
    report.append("\n")
    report.append(f"Anchor/non-anchor between-group variance ratio (full 64D): {anchor_var_explained:.6f}.\n")
    report.append(f"This is extremely small, meaning anchors and non-anchors are not separated by a large distance in key space relative to overall key-space spread.\n\n")

    report.append("Cross-protein mean query cosine similarity: {:.4f} +/- {:.4f}. ".format(upper_tri.mean(), upper_tri.std()))
    if upper_tri.mean() > 0.95:
        report.append("Queries are near-identical across proteins, confirming the rank-1 query structure.\n\n")
    elif upper_tri.mean() > 0.8:
        report.append("Queries are highly similar across proteins, largely consistent with rank-1 structure.\n\n")
    else:
        report.append("Queries show meaningful variation across proteins.\n\n")

    report.append("![Key PCA](qk_key_pca.png)\n\n")
    report.append("![Query PCA](qk_query_pca.png)\n\n")

    report.append("## Analysis 2: Contrastive covariance\n\n")
    report.append("For each binary structural feature z1, compute delta_k = E[k|z1=1] - E[k|z1=0] and measure its alignment with the search direction d and the anchor mean direction.\n\n")
    report.append("| Contrast | n_pos | n_neg | ||delta_k|| | cos(delta_k, d) | cos(delta_k, anchor_delta) | var ratio |\n")
    report.append("|---|---|---|---|---|---|---|\n")
    for name in results_contrast:
        r = results_contrast[name]
        report.append(f"| {name} | {r['n_pos']} | {r['n_neg']} | {r['delta_k_norm']:.4f} | {r['cos_with_d']:.4f} | {r['cos_with_anchor_delta']:.4f} | {r['explained_var_ratio']:.4f} |\n")
    report.append("\n")

    # Identify the best-aligned structural feature (excluding anchor itself and d-projection)
    structural_contrasts = {n: r for n, r in results_contrast.items() if n not in ("anchor vs non-anchor", "high vs low d-projection")}
    if structural_contrasts:
        best_name = max(structural_contrasts, key=lambda n: abs(structural_contrasts[n]["cos_with_d"]))
        best_cos = structural_contrasts[best_name]["cos_with_d"]
        report.append(f"Best structural alignment with d: {best_name} (cos = {best_cos:.4f}).\n\n")

    report.append("![Contrastive alignment](qk_contrastive_alignment.png)\n\n")

    report.append("## Analysis 3: Eigenspectrum and subspace structure\n\n")
    report.append(f"Effective rank of anchor key covariance: {eff_rank_anchor:.2f}.\n")
    report.append(f"Effective rank of non-anchor key covariance: {eff_rank_non:.2f}.\n")
    report.append(f"Components for 90% variance: anchor = {n90_anchor}, non-anchor = {n90_non}.\n\n")

    report.append("Alignment of anchor eigenvectors with d:\n\n")
    report.append("| EV | Var fraction | |cos(ev, d)| |\n|---|---|---|\n")
    for i in range(10):
        report.append(f"| EV{i+1} | {eig_anchor_frac[i]:.4f} | {d_alignment[i]:.4f} |\n")
    report.append("\n")

    # Noteworthy structural correlations
    sig_corrs = [r for r in subspace_corr_rows if abs(r["spearman_rho"]) > 0.15 and r["p_value"] < 0.01]
    if sig_corrs:
        report.append("Notable correlations between anchor eigenvector projections and structural properties (|rho| > 0.15, p < 0.01):\n\n")
        report.append("| Eigenvector | Property | Spearman rho | p-value |\n|---|---|---|---|\n")
        for r in sorted(sig_corrs, key=lambda x: abs(x["spearman_rho"]), reverse=True):
            report.append(f"| EV{r['eigenvector']} | {r['property']} | {r['spearman_rho']:.4f} | {r['p_value']:.2e} |\n")
        report.append("\n")
    else:
        report.append("No eigenvector-structural property correlations exceeded |rho| > 0.15 with p < 0.01.\n\n")

    report.append("![Eigenspectrum](qk_eigenspectrum.png)\n\n")

    out_report = REPORT_DIR / "qk_decomposition.md"
    with open(out_report, "w") as f:
        f.writelines(report)
    flush_print(f"  Saved: {out_report}")

    flush_print("\nDone.")


if __name__ == "__main__":
    main()
