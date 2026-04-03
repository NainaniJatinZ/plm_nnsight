#!/usr/bin/env python3
"""Anchor feature regression analysis (Experiment 3_25_anchor_regression.md).

For each of the 5 proteins, computes L10H9 projection scores for every residue
in the full unmasked sequence, then regresses those scores against biological
and structural annotations: SSE type, position within SSE, conservation,
relative solvent accessibility, distance to contact segments, and protein identity.

Also cross-references SAE latents 3539 and 52 from the differential activation
analysis.

Usage:
    uv run python scripts/anchor_regression.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

from helpers.utils import load_sae_prot

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
SEGMENT_RADIUS = 5
REFERENCE_PROTEIN = "2B61A"

ANCHOR_POSITIONS = {
    "1BRTA": 220,
    "1PVGA": 101,
    "2B61A": 315,
    "2DPMA": 39,
    "2PKEA": 131,
    # new proteins added after expanding full_seq_attn_cache coverage
    "2QY6A": 64,
    "2YHWA": 287,   # dual-anchor V92/V287; V287 ranks #1 (z=8.51)
    "3CSSA": 40,
    "3HO7A": 63,    # dual-anchor A63/L17; A63 ranks #50 (L17 ranks #217)
    "3OKPA": 200,
    "3QDLA": 114,   # dual-anchor P114/S115; both weak (ranks 121/148)
    "3WJPA": 94,
    "4EHUA": 100,
    "4EX6A": 124,   # dual-anchor M124/V180; M124 ranks #1 (z=6.90)
    "4EZIA": 310,
    "4ME3A": 75,    # weak anchor (rank 201, z=-0.73)
    "4N9WA": 194,   # dual-anchor R147/V194; V194 ranks #2 (z=4.22)
    "4OY3A": 193,
}

AA_ORDER = list("ACDEFGHIKLMNPQRSTVWY")
SSE_COLORS = {"H": "#e06c75", "E": "#61afef", "C": "#98c379"}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    # Normalize ss_dict keys: strip .pdb suffix, remap '-' -> 'C'
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")
    return protein_configs, seqs, ss_dict


def load_conservation(protein: str) -> dict | None:
    """Returns dict: 0-indexed position -> conservation score, or None."""
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/align/TARGET_b*_frequencies.csv"))
    if not candidates:
        return None
    cons = {}
    with open(candidates[0]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cons[int(row["i"]) - 1] = float(row["conservation"])
    return cons


def compute_rsa(protein: str, seq_len: int) -> dict | None:
    """Contact-number proxy for RSA from PDB. Returns dict: 0-idx pos -> float, or None."""
    try:
        from Bio.PDB import PDBParser
        from scipy.spatial.distance import cdist
    except ImportError:
        return None
    ev_dir = DATA_DIR / f"{protein}_EV"
    pdb_candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
    if not pdb_candidates:
        return None
    pdb_path = pdb_candidates[0]
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(protein, str(pdb_path))
    ca_coords = {}
    for chain in structure[0]:
        for residue in chain:
            if "CA" in residue:
                resid = residue.get_id()[1]
                ca_coords[resid] = residue["CA"].get_vector().get_array()
    if not ca_coords:
        return None
    pdb_residues = sorted(ca_coords.keys())
    coords = np.array([ca_coords[r] for r in pdb_residues])
    dists = cdist(coords, coords)
    neighbor_counts = (dists < 11.0).sum(axis=1) - 1
    max_neighbors = max(neighbor_counts.max(), 1)
    offset = pdb_residues[0] - 1
    accessibility = {}
    for i, resid in enumerate(pdb_residues):
        seq_pos = resid - offset - 1
        if 0 <= seq_pos < seq_len:
            accessibility[seq_pos] = round(1.0 - neighbor_counts[i] / max_neighbors, 3)
    return accessibility


# ---------------------------------------------------------------------------
# SSE feature computation
# ---------------------------------------------------------------------------

def compute_sse_features(sse_str: str) -> list[dict]:
    """Compute per-residue SSE features from a SSE string.

    Returns list of dicts (one per position) with:
        sse, seg_len, dist_to_boundary, is_boundary
    """
    n = len(sse_str)
    features = [None] * n

    # Find contiguous segments
    i = 0
    while i < n:
        label = sse_str[i]
        j = i
        while j < n and sse_str[j] == label:
            j += 1
        seg_len = j - i
        for pos in range(i, j):
            dist_left = pos - i
            dist_right = j - 1 - pos
            dist_to_boundary = min(dist_left, dist_right)
            features[pos] = {
                "sse": label,
                "seg_len": seg_len,
                "dist_to_boundary": dist_to_boundary,
                "is_boundary": 1 if dist_to_boundary <= 1 else 0,
            }
        i = j
    return features


# ---------------------------------------------------------------------------
# Model loading
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
        "W_Q_hd": W_Q[head].clone(),
        "b_Q_d": b_Q[head].clone(),
        "W_K_hd": W_K[head].clone(),
        "b_K_d": b_K[head].clone(),
    }


# ---------------------------------------------------------------------------
# Search direction (same as anchor_interp_v3.py)
# ---------------------------------------------------------------------------

def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Returns key-side search direction (1280,) on CPU.

    Computes mean unit-query direction q_mean_norm from W_Q, then maps it to
    residual-stream space via W_K: search_dir = W_K^T @ q_mean_norm.

    This gives the direction x such that k_j · q_mean = x_j · search_dir is
    maximized, i.e. the direction that makes a position's key vector score
    highly against the average query — which is what ranked the anchor #1 in v2.
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]  # (seq_len, 1280)
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q  # (seq_len, 64)
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    return W_K.T @ q_mean_norm  # (1280,)


def build_clean_sequence(sequence: str, config: dict) -> str:
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_start, ss1_end = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_start, ss2_end = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
    masked = ["<mask>"] * n
    for i in range(ss1_start, ss1_end):
        masked[i] = sequence[i]
    for i in range(ss2_start, ss2_end):
        masked[i] = sequence[i]
    for i in range(max(0, ss1_start - flank), ss1_start):
        masked[i] = sequence[i]
    for i in range(ss2_end, min(n, ss2_end + flank)):
        masked[i] = sequence[i]
    return "".join(masked)


# ---------------------------------------------------------------------------
# Projection score computation
# ---------------------------------------------------------------------------

def capture_projection_scores(model, tokenizer, sequence: str, search_dir_unit: torch.Tensor, device: str) -> np.ndarray:
    """Forward pass on sequence; return projection scores for each residue (excluding BOS/EOS).

    Returns array of shape (n_residues,) = (len(sequence),).
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]  # (seq_len, 1280)
    # Residues only (exclude BOS at 0, EOS at -1)
    x_residues = x_ln[1:-1]  # (n_residues, 1280) on CPU
    scores = (x_residues @ search_dir_unit.cpu()).numpy()  # (n_residues,)
    return scores


def capture_sae_activations(model, tokenizer, sequence: str, sae, device: str, latent_indices: list[int]) -> np.ndarray:
    """Return SAE activations for requested latent indices at every residue position.

    Returns array of shape (n_residues, len(latent_indices)).
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model._model.esm(**inputs, output_hidden_states=True)
    hidden = out.hidden_states[8]  # (1, seq_len, 1280) — layer 8 SAE convention
    acts_all = sae.get_acts(hidden)[0].cpu()  # (seq_len, 4096)
    acts_residues = acts_all[1:-1]  # (n_residues, 4096)
    return acts_residues[:, latent_indices].numpy()  # (n_residues, len(latent_indices))


# ---------------------------------------------------------------------------
# OLS with p-values (numpy + scipy)
# ---------------------------------------------------------------------------

def run_ols(X: np.ndarray, y: np.ndarray, feature_names: list[str]) -> dict:
    """OLS regression: y ~ 1 + X. Returns coefficients, SEs, p-values, R², residuals."""
    n = len(y)
    Xb = np.hstack([np.ones((n, 1)), X])  # add intercept column
    k = Xb.shape[1]
    beta, _, _, _ = np.linalg.lstsq(Xb, y, rcond=None)
    y_hat = Xb @ beta
    residuals = y - y_hat
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - k)
    sigma2 = ss_res / (n - k)
    try:
        XtX_inv = np.linalg.pinv(Xb.T @ Xb)
        se = np.sqrt(sigma2 * np.diag(XtX_inv))
    except Exception:
        se = np.full(k, np.nan)
    t_stats = beta / np.where(se > 0, se, np.nan)
    p_values = 2 * stats.t.sf(np.abs(t_stats), df=n - k)
    return {
        "feature_names": ["intercept"] + list(feature_names),
        "beta": beta,
        "se": se,
        "t_stats": t_stats,
        "p_values": p_values,
        "r2": r2,
        "adj_r2": adj_r2,
        "residuals": residuals,
        "y_hat": y_hat,
        "n": n,
        "k": k,
    }


# ---------------------------------------------------------------------------
# Assemble per-protein data
# ---------------------------------------------------------------------------

def build_protein_data(
    protein: str,
    sequence: str,
    config: dict,
    sse_str: str,
    conservation: dict | None,
    rsa: dict | None,
    proj_scores_full: np.ndarray,
    proj_scores_masked: np.ndarray,
    sae_acts: np.ndarray,  # (n_residues, 2) — latents 3539 and 52
    anchor_pos: int,
    protein_idx: int,
) -> list[dict]:
    """Build one row per residue with all features and the projection score."""
    n = len(sequence)
    sse_features = compute_sse_features(sse_str)
    pos1, pos2 = config["contact_pair"]
    ss1_start, ss1_end = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_start, ss2_end = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
    clean_seq = build_clean_sequence(sequence, config)
    is_unmasked = [c != "<mask>" for c in clean_seq.split() if False] + [True]  # recompute
    # Recompute is_unmasked from the masked sequence character by character
    is_unmasked = []
    i = 0
    s = clean_seq
    pos_in_seq = 0
    while pos_in_seq < n:
        if s[i:i+6] == "<mask>":
            is_unmasked.append(False)
            i += 6
            pos_in_seq += 1
        else:
            is_unmasked.append(True)
            i += 1
            pos_in_seq += 1

    rows = []
    for j in range(n):
        if j >= len(proj_scores_full):
            break
        aa = sequence[j]
        sse_f = sse_features[j] if j < len(sse_features) else {"sse": "C", "seg_len": 1, "dist_to_boundary": 0, "is_boundary": 1}
        cons_val = conservation.get(j, np.nan) if conservation else np.nan
        rsa_val = rsa.get(j, np.nan) if rsa else np.nan
        dist_to_ss1 = max(0, ss1_start - j) if j < ss1_start else (max(0, j - (ss1_end - 1)) if j >= ss1_end else 0)
        dist_to_ss2 = max(0, ss2_start - j) if j < ss2_start else (max(0, j - (ss2_end - 1)) if j >= ss2_end else 0)
        rows.append({
            "protein": protein,
            "protein_idx": protein_idx,
            "pos": j,
            "aa": aa,
            "is_anchor": 1 if j == anchor_pos else 0,
            "proj_full": float(proj_scores_full[j]),
            "proj_masked": float(proj_scores_masked[j]) if j < len(proj_scores_masked) else np.nan,
            "sse": sse_f["sse"],
            "seg_len": sse_f["seg_len"],
            "dist_to_boundary": sse_f["dist_to_boundary"],
            "is_boundary": sse_f["is_boundary"],
            "conservation": cons_val,
            "rel_acc": rsa_val,
            "dist_to_ss1": dist_to_ss1,
            "dist_to_ss2": dist_to_ss2,
            "in_analysis_window": 1 if is_unmasked[j] else 0,
            "latent_3539": float(sae_acts[j, 0]),
            "latent_52": float(sae_acts[j, 1]),
        })
    return rows


def parse_masked_positions(clean_seq: str, n: int) -> list[bool]:
    """Parse clean_seq string (with '<mask>' tokens) into a bool list of length n."""
    result = []
    i = 0
    while i < len(clean_seq) and len(result) < n:
        if clean_seq[i:i+6] == "<mask>":
            result.append(False)
            i += 6
        else:
            result.append(True)
            i += 1
    return result


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_a_sse_boxplot(all_rows: list[dict], output_dir: Path) -> None:
    proteins = sorted(set(r["protein"] for r in all_rows))
    fig, axes = plt.subplots(1, len(proteins) + 1, figsize=(4 * (len(proteins) + 1), 4), sharey=False)
    sse_labels = ["H", "E", "C"]

    def draw_panel(ax, rows, title):
        groups = {s: [r["proj_full"] for r in rows if r["sse"] == s] for s in sse_labels}
        data = [groups[s] for s in sse_labels]
        bp = ax.boxplot(data, labels=sse_labels, patch_artist=True, widths=0.5)
        for patch, s in zip(bp["boxes"], sse_labels):
            patch.set_facecolor(SSE_COLORS[s])
            patch.set_alpha(0.7)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("SSE type")
        ax.set_ylabel("Projection score" if ax == axes[0] else "")
        medians = {s: float(np.median(groups[s])) if groups[s] else 0.0 for s in sse_labels}
        for i, s in enumerate(sse_labels):
            ax.text(i + 1, ax.get_ylim()[1] * 0.95 if ax.get_ylim()[1] != 0 else 1, f"n={len(groups[s])}", ha="center", fontsize=7)

    for ax, protein in zip(axes[:-1], proteins):
        draw_panel(ax, [r for r in all_rows if r["protein"] == protein], protein)
    draw_panel(axes[-1], all_rows, "Combined")
    plt.tight_layout()
    out = output_dir / "anchor_regression_A_sse_boxplot.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_b_conservation_scatter(all_rows: list[dict], output_dir: Path) -> None:
    proteins = sorted(set(r["protein"] for r in all_rows))
    rows_with_cons = [r for r in all_rows if not np.isnan(r["conservation"])]
    if not rows_with_cons:
        print("  Plot B skipped: no conservation data")
        return
    proteins_with_cons = sorted(set(r["protein"] for r in rows_with_cons))
    fig, axes = plt.subplots(1, len(proteins_with_cons), figsize=(4 * len(proteins_with_cons), 4), sharey=False)
    if len(proteins_with_cons) == 1:
        axes = [axes]
    for ax, protein in zip(axes, proteins_with_cons):
        prows = [r for r in rows_with_cons if r["protein"] == protein]
        for s in ["H", "E", "C"]:
            sr = [r for r in prows if r["sse"] == s]
            if sr:
                ax.scatter([r["conservation"] for r in sr], [r["proj_full"] for r in sr],
                           color=SSE_COLORS[s], alpha=0.4, s=12, label=s)
        anchors = [r for r in prows if r["is_anchor"]]
        if anchors:
            ax.scatter([r["conservation"] for r in anchors], [r["proj_full"] for r in anchors],
                       color="black", marker="*", s=120, zorder=5, label="anchor")
        ax.set_title(protein, fontsize=9)
        ax.set_xlabel("Conservation")
        ax.set_ylabel("Projection score" if ax == axes[0] else "")
        ax.legend(fontsize=7, markerscale=0.8)
    plt.tight_layout()
    out = output_dir / "anchor_regression_B_conservation.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_c_boundary_scatter(all_rows: list[dict], output_dir: Path) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, s in zip(axes, ["H", "E", "C"]):
        sr = [r for r in all_rows if r["sse"] == s]
        if sr:
            ax.scatter([r["dist_to_boundary"] for r in sr], [r["proj_full"] for r in sr],
                       color=SSE_COLORS[s], alpha=0.3, s=10)
        anchors = [r for r in sr if r["is_anchor"]]
        if anchors:
            ax.scatter([r["dist_to_boundary"] for r in anchors], [r["proj_full"] for r in anchors],
                       color="black", marker="*", s=120, zorder=5)
        ax.set_title(f"SSE={s}", fontsize=9)
        ax.set_xlabel("Dist to SSE boundary")
        ax.set_ylabel("Projection score" if ax == axes[0] else "")
    plt.tight_layout()
    out = output_dir / "anchor_regression_C_boundary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_d_sequence_profile(all_rows: list[dict], protein_configs: dict, output_dir: Path) -> None:
    proteins = sorted(set(r["protein"] for r in all_rows))
    fig, axes = plt.subplots(len(proteins), 1, figsize=(16, 3.5 * len(proteins)), squeeze=False)
    for i, protein in enumerate(proteins):
        ax = axes[i, 0]
        prows = sorted([r for r in all_rows if r["protein"] == protein], key=lambda r: r["pos"])
        positions = [r["pos"] for r in prows]
        scores = [r["proj_full"] for r in prows]
        sse_labels = [r["sse"] for r in prows]

        # Color background by SSE
        prev_pos, prev_sse = positions[0], sse_labels[0]
        for k in range(1, len(positions) + 1):
            if k == len(positions) or sse_labels[k] != prev_sse:
                ax.axvspan(prev_pos - 0.5, positions[k - 1] + 0.5, alpha=0.15,
                           color=SSE_COLORS.get(prev_sse, "#aaaaaa"), lw=0)
                if k < len(positions):
                    prev_pos, prev_sse = positions[k], sse_labels[k]

        ax.plot(positions, scores, color="#444444", lw=0.8, alpha=0.9)

        # Mark SS1, SS2, anchor
        config = protein_configs[protein]
        pos1, pos2 = config["contact_pair"]
        ss1_s, ss1_e = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
        ss2_s, ss2_e = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
        ax.axvspan(ss1_s, ss1_e, alpha=0.3, color="orange", label="SS1", lw=0)
        ax.axvspan(ss2_s, ss2_e, alpha=0.3, color="purple", label="SS2", lw=0)
        anchor_pos = ANCHOR_POSITIONS[protein]
        anchor_score = next((r["proj_full"] for r in prows if r["pos"] == anchor_pos), None)
        if anchor_score is not None:
            ax.scatter([anchor_pos], [anchor_score], color="red", s=60, zorder=6, label="anchor")

        ax.set_title(protein, fontsize=9)
        ax.set_xlabel("Residue position")
        ax.set_ylabel("Projection score")
        ax.legend(fontsize=7, loc="upper right")
        patches = [mpatches.Patch(color=SSE_COLORS[s], alpha=0.5, label=s) for s in ["H", "E", "C"]]
        ax.legend(handles=patches + [mpatches.Patch(color="orange", alpha=0.5, label="SS1"),
                                      mpatches.Patch(color="purple", alpha=0.5, label="SS2"),
                                      plt.Line2D([0], [0], marker="o", color="red", lw=0, markersize=6, label="anchor")],
                  fontsize=7, loc="upper right", ncol=2)
    plt.tight_layout()
    out = output_dir / "anchor_regression_D_sequence_profile.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Regression
# ---------------------------------------------------------------------------

def build_matrix(rows: list[dict], include_conservation: bool = True, include_rsa: bool = False,
                 include_dist: bool = False, include_aa: bool = False,
                 include_sae: bool = False) -> tuple[np.ndarray, list[str], np.ndarray]:
    """Assemble feature matrix X and target y from rows.

    Returns (X, feature_names, y).
    """
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    proteins = sorted(set(r["protein"] for r in rows))
    ref_protein = proteins[0]

    cols = []
    names = []

    # SSE one-hot (C is reference)
    cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows]))
    names.append("SSE_E")
    cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows]))
    names.append("SSE_H")

    # Position features
    cols.append(np.array([float(r["dist_to_boundary"]) for r in rows]))
    names.append("dist_to_boundary")
    cols.append(np.array([float(r["seg_len"]) for r in rows]))
    names.append("seg_len")
    cols.append(np.array([float(r["is_boundary"]) for r in rows]))
    names.append("is_boundary")

    # Conservation
    if include_conservation:
        cols.append(np.array([r["conservation"] for r in rows], dtype=float))
        names.append("conservation")

    # RSA
    if include_rsa:
        cols.append(np.array([r["rel_acc"] for r in rows], dtype=float))
        names.append("rel_acc")

    # AA one-hot (drop 'A' as reference)
    if include_aa:
        for aa in AA_ORDER[1:]:  # skip 'A'
            cols.append(np.array([1.0 if r["aa"] == aa else 0.0 for r in rows]))
            names.append(f"AA_{aa}")

    # Distance-to-contact features
    if include_dist:
        cols.append(np.array([float(r["dist_to_ss1"]) for r in rows]))
        names.append("dist_to_ss1")
        cols.append(np.array([float(r["dist_to_ss2"]) for r in rows]))
        names.append("dist_to_ss2")
        cols.append(np.array([float(r["in_analysis_window"]) for r in rows]))
        names.append("in_analysis_window")

    # SAE latents
    if include_sae:
        cols.append(np.array([r["latent_3539"] for r in rows], dtype=float))
        names.append("latent_3539")
        cols.append(np.array([r["latent_52"] for r in rows], dtype=float))
        names.append("latent_52")

    # Protein dummies (ref_protein is reference)
    for p in proteins[1:]:
        cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows]))
        names.append(f"protein_{p}")

    X = np.column_stack(cols)
    return X, names, y


def format_ols_table(result: dict) -> list[str]:
    lines = []
    lines.append(f"N={result['n']}, k={result['k']}, R²={result['r2']:.4f}, adj-R²={result['adj_r2']:.4f}\n\n")
    lines.append("| Feature | Coef | SE | t | p |\n")
    lines.append("|---------|------|-----|---|---|\n")
    for fname, b, s, t, p in zip(result["feature_names"], result["beta"], result["se"], result["t_stats"], result["p_values"]):
        star = "**" if p < 0.01 else ("*" if p < 0.05 else "")
        lines.append(f"| {fname} | {b:.4f} | {s:.4f} | {t:.2f} | {p:.4f}{star} |\n")
    return lines


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading configs...")
    protein_configs, seqs, ss_dict = load_configs()

    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    print("Extracting L10H9 weights and computing search direction from 2B61A...")
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir = compute_search_dir(model, tokenizer, ref_clean, weights, args.device)
    search_dir_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)
    print(f"  Search direction norm: {search_dir.norm().item():.4f}")

    print("Loading layer-8 SAE (for latents 3539 and 52)...")
    sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=8, device=args.device)
    sae.eval()
    LATENT_INDICES = [3539, 52]

    print("\nProcessing proteins...")
    all_rows = []
    for p_idx, (protein, anchor_pos) in enumerate(ANCHOR_POSITIONS.items()):
        print(f"  {protein}...")
        sequence = seqs[protein]
        config = protein_configs[protein]
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            print(f"    WARNING: SSE length mismatch ({len(sse_str)} vs {len(sequence)}), padding with C")
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")

        conservation = load_conservation(protein)
        if conservation is None:
            print(f"    No conservation data for {protein}")
        rsa = compute_rsa(protein, len(sequence))
        if rsa is None:
            print(f"    No RSA data for {protein}")

        # Forward pass on full sequence
        proj_full = capture_projection_scores(model, tokenizer, sequence, search_dir_unit, args.device)

        # Forward pass on clean masked sequence (for anchor rank check)
        clean_seq = build_clean_sequence(sequence, config)
        proj_masked = capture_projection_scores(model, tokenizer, clean_seq, search_dir_unit, args.device)

        # SAE activations on full sequence
        sae_acts = capture_sae_activations(model, tokenizer, sequence, sae, args.device, LATENT_INDICES)

        # Anchor rank check on masked sequence
        anchor_score_masked = proj_masked[anchor_pos]
        anchor_rank = int((proj_masked > anchor_score_masked).sum()) + 1
        anchor_score_full = proj_full[anchor_pos]
        anchor_rank_full = int((proj_full > anchor_score_full).sum()) + 1
        print(f"    Anchor rank: {anchor_rank}/{len(proj_masked)} (masked), {anchor_rank_full}/{len(proj_full)} (full)")
        print(f"    Proj scores: anchor_full={anchor_score_full:.3f}, anchor_masked={anchor_score_masked:.3f}")

        rows = build_protein_data(protein, sequence, config, sse_str, conservation, rsa,
                                  proj_full, proj_masked, sae_acts, anchor_pos, p_idx)
        all_rows.extend(rows)
        print(f"    {len(rows)} residues added")

    print(f"\nTotal rows: {len(all_rows)}")

    # Sanity checks
    anchor_rows = [r for r in all_rows if r["is_anchor"]]
    print("\nSanity checks:")
    for r in anchor_rows:
        cons_str = f"{r['conservation']:.3f}" if not np.isnan(r["conservation"]) else "NaN"
        print(f"  {r['protein']}: anchor pos={r['pos']} ({r['aa']}), proj_full={r['proj_full']:.3f}, "
              f"proj_masked={r['proj_masked']:.3f}, sse={r['sse']}, cons={cons_str}")

    # ---------------------------------------------------------------------------
    # Exploratory plots (before regression)
    # ---------------------------------------------------------------------------
    print("\nGenerating plots...")
    plot_a_sse_boxplot(all_rows, REPORT_DIR)
    plot_b_conservation_scatter(all_rows, REPORT_DIR)
    plot_c_boundary_scatter(all_rows, REPORT_DIR)
    plot_d_sequence_profile(all_rows, protein_configs, REPORT_DIR)

    # ---------------------------------------------------------------------------
    # Regression analysis
    # ---------------------------------------------------------------------------
    print("\nRunning regressions...")

    # Rows with conservation (excludes 2PKEA)
    rows_with_cons = [r for r in all_rows if not np.isnan(r["conservation"])]
    rows_with_rsa = [r for r in all_rows if not np.isnan(r["rel_acc"])]

    # Model 1: SSE-only + protein dummies (all proteins, no conservation)
    X1, names1, y1 = build_matrix(all_rows, include_conservation=False, include_rsa=False,
                                   include_dist=False, include_aa=False, include_sae=False)
    res1 = run_ols(X1, y1, names1)
    print(f"  Model 1 (SSE-only):        R²={res1['r2']:.4f}, adj-R²={res1['adj_r2']:.4f}")

    # Model 2: SSE + position features (all proteins)
    X2, names2, y2 = build_matrix(all_rows, include_conservation=False, include_rsa=False,
                                   include_dist=False, include_aa=False, include_sae=False)
    # Model 2 already includes position features (dist_to_boundary, seg_len, is_boundary) via build_matrix
    res2 = run_ols(X2, y2, names2)  # same as model 1 since build_matrix always includes position features

    # Rebuild with explicit controls to match the experiment spec
    # Model 1: only SSE + protein
    def build_minimal(rows, include_conservation=False, include_aa=False, include_dist=False, include_sae=False):
        y = np.array([r["proj_full"] for r in rows], dtype=float)
        proteins = sorted(set(r["protein"] for r in rows))
        cols, names = [], []
        cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
        cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
        if include_aa or True:  # always include position features from Model 2 onward... skip for M1
            pass
        for p in proteins[1:]:
            cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
        return np.column_stack(cols), names, y

    X1b, n1b, y1b = build_minimal(all_rows)
    res1 = run_ols(X1b, y1b, n1b)
    print(f"  Model 1 (SSE + protein FE): R²={res1['r2']:.4f}, adj-R²={res1['adj_r2']:.4f}")

    # Model 2: SSE + position + protein
    def build_m2(rows):
        y = np.array([r["proj_full"] for r in rows], dtype=float)
        proteins = sorted(set(r["protein"] for r in rows))
        cols, names = [], []
        cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
        cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
        cols.append(np.array([float(r["dist_to_boundary"]) for r in rows])); names.append("dist_to_boundary")
        cols.append(np.array([float(r["seg_len"]) for r in rows])); names.append("seg_len")
        cols.append(np.array([float(r["is_boundary"]) for r in rows])); names.append("is_boundary")
        for p in proteins[1:]:
            cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
        return np.column_stack(cols), names, y

    X2b, n2b, y2b = build_m2(all_rows)
    res2 = run_ols(X2b, y2b, n2b)
    print(f"  Model 2 (+ position):       R²={res2['r2']:.4f}, adj-R²={res2['adj_r2']:.4f}")

    # Model 3: full biological (conservation-available proteins only)
    def build_m3(rows):
        y = np.array([r["proj_full"] for r in rows], dtype=float)
        proteins = sorted(set(r["protein"] for r in rows))
        cols, names = [], []
        cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
        cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
        cols.append(np.array([float(r["dist_to_boundary"]) for r in rows])); names.append("dist_to_boundary")
        cols.append(np.array([float(r["seg_len"]) for r in rows])); names.append("seg_len")
        cols.append(np.array([float(r["is_boundary"]) for r in rows])); names.append("is_boundary")
        cols.append(np.array([r["conservation"] for r in rows], dtype=float)); names.append("conservation")
        for aa in AA_ORDER[1:]:
            cols.append(np.array([1.0 if r["aa"] == aa else 0.0 for r in rows])); names.append(f"AA_{aa}")
        for p in proteins[1:]:
            cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
        return np.column_stack(cols), names, y

    X3b, n3b, y3b = build_m3(rows_with_cons)
    res3 = run_ols(X3b, y3b, n3b)
    print(f"  Model 3 (+ cons + AA, {len(rows_with_cons)} rows): R²={res3['r2']:.4f}, adj-R²={res3['adj_r2']:.4f}")

    # Model 4: + distance-to-contact
    def build_m4(rows):
        y = np.array([r["proj_full"] for r in rows], dtype=float)
        proteins = sorted(set(r["protein"] for r in rows))
        cols, names = [], []
        cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
        cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
        cols.append(np.array([float(r["dist_to_boundary"]) for r in rows])); names.append("dist_to_boundary")
        cols.append(np.array([float(r["seg_len"]) for r in rows])); names.append("seg_len")
        cols.append(np.array([r["conservation"] for r in rows], dtype=float)); names.append("conservation")
        cols.append(np.array([float(r["dist_to_ss1"]) for r in rows])); names.append("dist_to_ss1")
        cols.append(np.array([float(r["dist_to_ss2"]) for r in rows])); names.append("dist_to_ss2")
        cols.append(np.array([float(r["in_analysis_window"]) for r in rows])); names.append("in_analysis_window")
        for p in proteins[1:]:
            cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
        return np.column_stack(cols), names, y

    X4b, n4b, y4b = build_m4(rows_with_cons)
    res4 = run_ols(X4b, y4b, n4b)
    print(f"  Model 4 (+ distance):       R²={res4['r2']:.4f}, adj-R²={res4['adj_r2']:.4f}")

    # Model 5: + SAE latents 3539 and 52 (all proteins)
    def build_m5(rows):
        y = np.array([r["proj_full"] for r in rows], dtype=float)
        proteins = sorted(set(r["protein"] for r in rows))
        cols, names = [], []
        cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
        cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
        cols.append(np.array([float(r["dist_to_boundary"]) for r in rows])); names.append("dist_to_boundary")
        cols.append(np.array([float(r["seg_len"]) for r in rows])); names.append("seg_len")
        cols.append(np.array([float(r["is_boundary"]) for r in rows])); names.append("is_boundary")
        cols.append(np.array([r["latent_3539"] for r in rows], dtype=float)); names.append("latent_3539")
        cols.append(np.array([r["latent_52"] for r in rows], dtype=float)); names.append("latent_52")
        for p in proteins[1:]:
            cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
        return np.column_stack(cols), names, y

    X5b, n5b, y5b = build_m5(all_rows)
    res5 = run_ols(X5b, y5b, n5b)
    print(f"  Model 5 (+ SAE latents):    R²={res5['r2']:.4f}, adj-R²={res5['adj_r2']:.4f}")

    # SAE correlations
    proj_all = np.array([r["proj_full"] for r in all_rows])
    lat3539 = np.array([r["latent_3539"] for r in all_rows])
    lat52 = np.array([r["latent_52"] for r in all_rows])
    corr_3539 = float(np.corrcoef(proj_all, lat3539)[0, 1])
    corr_52 = float(np.corrcoef(proj_all, lat52)[0, 1])
    print(f"\n  Pearson corr(proj, latent_3539): {corr_3539:.4f}")
    print(f"  Pearson corr(proj, latent_52):   {corr_52:.4f}")

    # ---------------------------------------------------------------------------
    # Anchor residual analysis
    # ---------------------------------------------------------------------------
    print("\nAnchor residual analysis (Model 2, all proteins):")
    residual_std = float(np.std(res2["residuals"]))
    anchor_residuals = {}
    for r in anchor_rows:
        protein = r["protein"]
        pos = r["pos"]
        # Find row index in all_rows
        idx = next(i for i, row in enumerate(all_rows) if row["protein"] == protein and row["pos"] == pos)
        resid = res2["residuals"][idx]
        yhat = res2["y_hat"][idx]
        z = resid / residual_std
        anchor_residuals[protein] = {"actual": r["proj_full"], "predicted": float(yhat), "residual": float(resid), "z_score": float(z)}
        print(f"  {protein}: actual={r['proj_full']:.3f}, predicted={yhat:.3f}, residual={resid:.3f}, z={z:.2f}")

    # Model 3 anchor residuals (cons proteins only)
    print("\nAnchor residual analysis (Model 3, conservation proteins):")
    residual_std3 = float(np.std(res3["residuals"]))
    for r in anchor_rows:
        protein = r["protein"]
        if not any(row["protein"] == protein for row in rows_with_cons):
            print(f"  {protein}: excluded (no conservation data)")
            continue
        idx = next(i for i, row in enumerate(rows_with_cons) if row["protein"] == protein and row["pos"] == r["pos"])
        resid = res3["residuals"][idx]
        yhat = res3["y_hat"][idx]
        z = resid / residual_std3
        print(f"  {protein}: actual={r['proj_full']:.3f}, predicted={yhat:.3f}, residual={resid:.3f}, z={z:.2f}")

    # ---------------------------------------------------------------------------
    # Write report
    # ---------------------------------------------------------------------------
    print("\nWriting report...")
    report_lines = []
    report_lines.append("# Anchor Feature Regression Analysis\n\n")
    report_lines.append(f"Search direction: L10H9 key-side direction W_K^T @ q_mean from {REFERENCE_PROTEIN} clean masked sequence.\n")
    report_lines.append("Target: key score = dot(post-LN residual at layer 10, W_K^T @ q_mean_unit), computed on full unmasked sequence.\n")
    report_lines.append(f"Total residues: {len(all_rows)} across {len(ANCHOR_POSITIONS)} proteins.\n")
    report_lines.append(f"Proteins without conservation data (excluded from Models 3–4): 2PKEA.\n\n")

    report_lines.append("## Sanity checks\n\n")
    report_lines.append("| Protein | Anchor pos | AA | SSE | Proj (full) | Proj (masked) | Rank (full) | Rank (masked) |\n")
    report_lines.append("|---------|-----------|-----|-----|-------------|---------------|-------------|---------------|\n")
    for r in anchor_rows:
        p = r["protein"]
        proj_full_all = np.array([row["proj_full"] for row in all_rows if row["protein"] == p])
        proj_masked_this = r["proj_masked"]
        rank_full = int((proj_full_all > r["proj_full"]).sum()) + 1
        report_lines.append(f"| {p} | {r['pos']} | {r['aa']} | {r['sse']} | {r['proj_full']:.3f} | {proj_masked_this:.3f} | {rank_full}/{len(proj_full_all)} | — |\n")
    report_lines.append("\n")

    report_lines.append("## Model R² summary\n\n")
    report_lines.append("| Model | Description | N | R² | adj-R² |\n")
    report_lines.append("|-------|-------------|---|-----|--------|\n")
    report_lines.append(f"| M1 | SSE + protein FE | {res1['n']} | {res1['r2']:.4f} | {res1['adj_r2']:.4f} |\n")
    report_lines.append(f"| M2 | M1 + position (dist_to_boundary, seg_len, is_boundary) | {res2['n']} | {res2['r2']:.4f} | {res2['adj_r2']:.4f} |\n")
    report_lines.append(f"| M3 | M2 + conservation + AA identity (4 proteins) | {res3['n']} | {res3['r2']:.4f} | {res3['adj_r2']:.4f} |\n")
    report_lines.append(f"| M4 | M3 + dist_to_ss1/ss2 + in_analysis_window | {res4['n']} | {res4['r2']:.4f} | {res4['adj_r2']:.4f} |\n")
    report_lines.append(f"| M5 | M2 + SAE latents 3539 and 52 (all 5 proteins) | {res5['n']} | {res5['r2']:.4f} | {res5['adj_r2']:.4f} |\n")
    report_lines.append("\n")

    for label, res, note in [
        ("Model 1: SSE + protein FE", res1, "all proteins"),
        ("Model 2: + position features", res2, "all proteins"),
        ("Model 3: + conservation + AA", res3, "4 proteins with conservation"),
        ("Model 4: + distance to contact", res4, "4 proteins with conservation"),
        ("Model 5: + SAE latents 3539 and 52", res5, "all proteins"),
    ]:
        report_lines.append(f"## {label} ({note})\n\n")
        report_lines.extend(format_ols_table(res))
        report_lines.append("\n")

    report_lines.append("## Anchor residual analysis (Model 2)\n\n")
    report_lines.append(f"Residual std (all positions): {residual_std:.4f}\n\n")
    report_lines.append("| Protein | Actual | Predicted | Residual | Z-score |\n")
    report_lines.append("|---------|--------|-----------|----------|---------|\n")
    for protein, d in anchor_residuals.items():
        report_lines.append(f"| {protein} | {d['actual']:.3f} | {d['predicted']:.3f} | {d['residual']:.3f} | {d['z_score']:.2f} |\n")
    report_lines.append("\n")

    report_lines.append("## SAE latent correlations with projection score\n\n")
    report_lines.append(f"Pearson corr(proj_full, latent_3539): {corr_3539:.4f}\n\n")
    report_lines.append(f"Pearson corr(proj_full, latent_52): {corr_52:.4f}\n\n")

    out_path = REPORT_DIR / "anchor_regression.md"
    with open(out_path, "w") as f:
        f.writelines(report_lines)
    print(f"  Saved: {out_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
