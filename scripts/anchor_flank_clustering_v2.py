#!/usr/bin/env python3
"""Anchor flank clustering at scale (v2).

Runs the local-flank masking sweep on 250 proteins (stratified by length from
the behavior audit), discovers each protein's actual minimal radius (R_50 of
projection recovery), extracts the minimal flank subsequence, then clusters
by pairwise sequence identity and ESM2 embedding similarity.

Phase A: Flank sweep — for each protein and each radius in the schedule, mask
         everything outside [anchor-R, anchor+R], run a forward pass, measure
         projection recovery. Determine R_50 per protein.
Phase B: Extract flanks at the discovered R_50.
Phase C: Clustering — pairwise sequence identity (center-aligned on anchor),
         BLOSUM62 scores, ESM2 mean-flank embeddings, anchor-position embeddings.

Usage:
    uv run python scripts/anchor_flank_clustering_v2.py --device cuda [--n-proteins 250]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import random
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy import spatial, cluster, stats as sp_stats

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

TARGET_LAYER = 10
TARGET_HEAD = 9
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
REFERENCE_PROTEIN = "2B61A"
MASK_TOKEN = "<mask>"
RADII_SCHEDULE = [5, 6, 7, 8, 10, 12, 15, 20, 30, 40, 60, 80, 120]
RECOVERY_THRESHOLD = 0.50  # R_50


# ---------------------------------------------------------------------------
# Model
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
    return weights["W_K_hd"].T @ q_mean_norm


# ---------------------------------------------------------------------------
# Protein selection
# ---------------------------------------------------------------------------

def select_proteins(audit_csv: Path, all_seqs: dict, n: int, seed: int = 42) -> list[dict]:
    """Select n proteins stratified by length from the behavior audit.

    Ensures anchor-like proteins are included, and covers the full length range.
    """
    rows = []
    with open(audit_csv) as f:
        reader = csv.DictReader(f)
        for r in reader:
            pid = r["protein"]
            if pid not in all_seqs:
                continue
            top1 = float(r["top1_mass"])
            rho = float(r["rank_corr"])
            if top1 <= 0.15 or rho <= 0.3:
                continue
            rows.append({
                "protein": pid,
                "top3_mass": float(r["top3_mass"]),
                "anchor_pos": int(r["top_key_idx"]),
                "n_res": int(r["n_res"]),
            })

    if len(rows) <= n:
        return rows

    # Stratify by length quartiles
    rows.sort(key=lambda x: x["n_res"])
    rng = random.Random(seed)

    # Split into 4 length bins, sample n//4 from each
    bin_size = len(rows) // 4
    bins = [rows[:bin_size], rows[bin_size:2*bin_size], rows[2*bin_size:3*bin_size], rows[3*bin_size:]]
    per_bin = n // 4
    selected = []
    for b in bins:
        if len(b) <= per_bin:
            selected.extend(b)
        else:
            selected.extend(rng.sample(b, per_bin))

    # If we need more (due to rounding), sample from the remainder
    remaining_ids = set(r["protein"] for r in rows) - set(r["protein"] for r in selected)
    remaining = [r for r in rows if r["protein"] in remaining_ids]
    if len(selected) < n:
        extra = rng.sample(remaining, min(n - len(selected), len(remaining)))
        selected.extend(extra)

    return selected[:n]


# ---------------------------------------------------------------------------
# Flank sweep (Phase A)
# ---------------------------------------------------------------------------

def build_masked_sequence(sequence: str, anchor_pos: int, radius: int) -> str:
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = []
    for i in range(n):
        if lo <= i <= hi:
            chars.append(sequence[i])
        else:
            chars.append(MASK_TOKEN)
    return " ".join(chars)


@torch.no_grad()
def run_single(model, tokenizer, sequence_str: str, device: str):
    inputs = tokenizer(sequence_str, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0, 1:-1]
    return x_ln


def get_projection_at_anchor(x_ln, anchor_pos: int, d_unit: torch.Tensor) -> float:
    proj_scores = (x_ln @ d_unit.cpu()).numpy()
    return float(proj_scores[anchor_pos])


def run_flank_sweep(model, tokenizer, pid: str, seq: str, anchor_pos: int,
                    d_unit: torch.Tensor, device: str) -> dict:
    """Run the full radius sweep for one protein. Returns {radius: alpha_norm} and R_50."""
    n_res = len(seq)
    radii = [r for r in RADII_SCHEDULE if r < n_res // 2]

    # Full sequence baseline
    full_seq_str = " ".join(seq)
    x_ln_full = run_single(model, tokenizer, full_seq_str, device)
    alpha_full = get_projection_at_anchor(x_ln_full, anchor_pos, d_unit)

    if abs(alpha_full) < 1e-8:
        return {"radii": {}, "R_50": None, "alpha_full": alpha_full}

    results = {}
    r50 = None
    for R in radii:
        masked = build_masked_sequence(seq, anchor_pos, R)
        x_ln_R = run_single(model, tokenizer, masked, device)
        alpha_R = get_projection_at_anchor(x_ln_R, anchor_pos, d_unit)
        alpha_norm = alpha_R / alpha_full
        results[R] = alpha_norm
        if r50 is None and alpha_norm >= RECOVERY_THRESHOLD:
            r50 = R

    # Add full
    results[n_res] = 1.0
    if r50 is None:
        r50 = n_res  # needs full sequence

    return {"radii": results, "R_50": r50, "alpha_full": alpha_full}


# ---------------------------------------------------------------------------
# Clustering (Phase C) — reused from v1 script
# ---------------------------------------------------------------------------

def pairwise_sequence_identity(flanks: dict[str, dict]) -> np.ndarray:
    pids = list(flanks.keys())
    n = len(pids)
    matrix = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = flanks[pids[i]], flanks[pids[j]]
            off_a, off_b = a["offset_to_anchor"], b["offset_to_anchor"]
            seq_a, seq_b = a["sequence"], b["sequence"]
            left = max(-off_a, -off_b)
            right = min(len(seq_a) - off_a - 1, len(seq_b) - off_b - 1)
            if left > right:
                continue
            matches = sum(1 for rp in range(left, right + 1) if seq_a[off_a + rp] == seq_b[off_b + rp])
            total = right - left + 1
            ident = matches / max(total, 1)
            matrix[i, j] = ident
            matrix[j, i] = ident
    return matrix


BLOSUM62 = {
    'A': {'A': 4, 'R': -1, 'N': -2, 'D': -2, 'C': 0, 'Q': -1, 'E': -1, 'G': 0, 'H': -2, 'I': -1, 'L': -1, 'K': -1, 'M': -1, 'F': -2, 'P': -1, 'S': 1, 'T': 0, 'W': -3, 'Y': -2, 'V': 0},
    'R': {'A': -1, 'R': 5, 'N': 0, 'D': -2, 'C': -3, 'Q': 1, 'E': 0, 'G': -2, 'H': 0, 'I': -3, 'L': -2, 'K': 2, 'M': -1, 'F': -3, 'P': -2, 'S': -1, 'T': -1, 'W': -3, 'Y': -2, 'V': -3},
    'N': {'A': -2, 'R': 0, 'N': 6, 'D': 1, 'C': -3, 'Q': 0, 'E': 0, 'G': 0, 'H': 1, 'I': -3, 'L': -3, 'K': 0, 'M': -2, 'F': -3, 'P': -2, 'S': 1, 'T': 0, 'W': -4, 'Y': -2, 'V': -3},
    'D': {'A': -2, 'R': -2, 'N': 1, 'D': 6, 'C': -3, 'Q': 0, 'E': 2, 'G': -1, 'H': -1, 'I': -3, 'L': -4, 'K': -1, 'M': -3, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -4, 'Y': -3, 'V': -3},
    'C': {'A': 0, 'R': -3, 'N': -3, 'D': -3, 'C': 9, 'Q': -3, 'E': -4, 'G': -3, 'H': -3, 'I': -1, 'L': -1, 'K': -3, 'M': -1, 'F': -2, 'P': -3, 'S': -1, 'T': -1, 'W': -2, 'Y': -2, 'V': -1},
    'Q': {'A': -1, 'R': 1, 'N': 0, 'D': 0, 'C': -3, 'Q': 5, 'E': 2, 'G': -2, 'H': 0, 'I': -3, 'L': -2, 'K': 1, 'M': 0, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -2, 'Y': -1, 'V': -2},
    'E': {'A': -1, 'R': 0, 'N': 0, 'D': 2, 'C': -4, 'Q': 2, 'E': 5, 'G': -2, 'H': 0, 'I': -3, 'L': -3, 'K': 1, 'M': -2, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -3, 'Y': -2, 'V': -2},
    'G': {'A': 0, 'R': -2, 'N': 0, 'D': -1, 'C': -3, 'Q': -2, 'E': -2, 'G': 6, 'H': -2, 'I': -4, 'L': -4, 'K': -2, 'M': -3, 'F': -3, 'P': -2, 'S': 0, 'T': -2, 'W': -2, 'Y': -3, 'V': -3},
    'H': {'A': -2, 'R': 0, 'N': 1, 'D': -1, 'C': -3, 'Q': 0, 'E': 0, 'G': -2, 'H': 8, 'I': -3, 'L': -3, 'K': -1, 'M': -2, 'F': -1, 'P': -2, 'S': -1, 'T': -2, 'W': -2, 'Y': 2, 'V': -3},
    'I': {'A': -1, 'R': -3, 'N': -3, 'D': -3, 'C': -1, 'Q': -3, 'E': -3, 'G': -4, 'H': -3, 'I': 4, 'L': 2, 'K': -3, 'M': 1, 'F': 0, 'P': -3, 'S': -2, 'T': -1, 'W': -3, 'Y': -1, 'V': 3},
    'L': {'A': -1, 'R': -2, 'N': -3, 'D': -4, 'C': -1, 'Q': -2, 'E': -3, 'G': -4, 'H': -3, 'I': 2, 'L': 4, 'K': -2, 'M': 2, 'F': 0, 'P': -3, 'S': -2, 'T': -1, 'W': -2, 'Y': -1, 'V': 1},
    'K': {'A': -1, 'R': 2, 'N': 0, 'D': -1, 'C': -3, 'Q': 1, 'E': 1, 'G': -2, 'H': -1, 'I': -3, 'L': -2, 'K': 5, 'M': -1, 'F': -3, 'P': -1, 'S': 0, 'T': -1, 'W': -3, 'Y': -2, 'V': -2},
    'M': {'A': -1, 'R': -1, 'N': -2, 'D': -3, 'C': -1, 'Q': 0, 'E': -2, 'G': -3, 'H': -2, 'I': 1, 'L': 2, 'K': -1, 'M': 5, 'F': 0, 'P': -2, 'S': -1, 'T': -1, 'W': -1, 'Y': -1, 'V': 1},
    'F': {'A': -2, 'R': -3, 'N': -3, 'D': -3, 'C': -2, 'Q': -3, 'E': -3, 'G': -3, 'H': -1, 'I': 0, 'L': 0, 'K': -3, 'M': 0, 'F': 6, 'P': -4, 'S': -2, 'T': -2, 'W': 1, 'Y': 3, 'V': -1},
    'P': {'A': -1, 'R': -2, 'N': -2, 'D': -1, 'C': -3, 'Q': -1, 'E': -1, 'G': -2, 'H': -2, 'I': -3, 'L': -3, 'K': -1, 'M': -2, 'F': -4, 'P': 7, 'S': -1, 'T': -1, 'W': -4, 'Y': -3, 'V': -2},
    'S': {'A': 1, 'R': -1, 'N': 1, 'D': 0, 'C': -1, 'Q': 0, 'E': 0, 'G': 0, 'H': -1, 'I': -2, 'L': -2, 'K': 0, 'M': -1, 'F': -2, 'P': -1, 'S': 4, 'T': 1, 'W': -3, 'Y': -2, 'V': -2},
    'T': {'A': 0, 'R': -1, 'N': 0, 'D': -1, 'C': -1, 'Q': -1, 'E': -1, 'G': -2, 'H': -2, 'I': -1, 'L': -1, 'K': -1, 'M': -1, 'F': -2, 'P': -1, 'S': 1, 'T': 5, 'W': -2, 'Y': -2, 'V': 0},
    'W': {'A': -3, 'R': -3, 'N': -4, 'D': -4, 'C': -2, 'Q': -2, 'E': -3, 'G': -2, 'H': -2, 'I': -3, 'L': -2, 'K': -3, 'M': -1, 'F': 1, 'P': -4, 'S': -3, 'T': -2, 'W': 11, 'Y': 2, 'V': -3},
    'Y': {'A': -2, 'R': -2, 'N': -2, 'D': -3, 'C': -2, 'Q': -1, 'E': -2, 'G': -3, 'H': 2, 'I': -1, 'L': -1, 'K': -2, 'M': -1, 'F': 3, 'P': -3, 'S': -2, 'T': -2, 'W': 2, 'Y': 7, 'V': -1},
    'V': {'A': 0, 'R': -3, 'N': -3, 'D': -3, 'C': -1, 'Q': -2, 'E': -2, 'G': -3, 'H': -3, 'I': 3, 'L': 1, 'K': -2, 'M': 1, 'F': -1, 'P': -2, 'S': -2, 'T': 0, 'W': -3, 'Y': -1, 'V': 4},
}


def pairwise_blosum62(flanks: dict[str, dict]) -> np.ndarray:
    pids = list(flanks.keys())
    n = len(pids)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            a, b = flanks[pids[i]], flanks[pids[j]]
            off_a, off_b = a["offset_to_anchor"], b["offset_to_anchor"]
            seq_a, seq_b = a["sequence"], b["sequence"]
            left = max(-off_a, -off_b)
            right = min(len(seq_a) - off_a - 1, len(seq_b) - off_b - 1)
            if left > right:
                continue
            total, count = 0.0, 0
            for rp in range(left, right + 1):
                aa_a, aa_b = seq_a[off_a + rp], seq_b[off_b + rp]
                if aa_a in BLOSUM62 and aa_b in BLOSUM62.get(aa_a, {}):
                    total += BLOSUM62[aa_a][aa_b]
                    count += 1
            score = total / max(count, 1)
            matrix[i, j] = score
            matrix[j, i] = score
    return matrix


@torch.no_grad()
def get_flank_embedding(model, tokenizer, sequence: str, device: str) -> np.ndarray:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0, 1:-1]
    return x_ln.mean(dim=0).numpy()


@torch.no_grad()
def get_anchor_embedding(model, tokenizer, sequence: str, anchor_offset: int, device: str) -> np.ndarray:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    return x_ln[anchor_offset + 1].numpy()


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_sim_matrix(matrix, labels, title, path, cmap="RdYlBu_r", vmin=None, vmax=None):
    n = len(labels)
    fig, ax = plt.subplots(figsize=(max(8, n * 0.06), max(7, n * 0.055)))
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontsize=3, rotation=90)
    ax.set_yticklabels(labels, fontsize=3)
    ax.set_title(title, fontsize=10)
    plt.tight_layout()
    fig.savefig(path, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_dendro(linkage_mat, labels, title, path):
    fig, ax = plt.subplots(figsize=(max(12, len(labels) * 0.08), 4))
    cluster.hierarchy.dendrogram(linkage_mat, labels=labels, ax=ax, leaf_rotation=90, leaf_font_size=3)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Distance")
    plt.tight_layout()
    fig.savefig(path, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_pca(embeddings, labels, color_vals, color_label, title, path):
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    coords = pca.fit_transform(embeddings)
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(coords[:, 0], coords[:, 1], c=color_vals, cmap="viridis", s=15, edgecolors="white", linewidths=0.3)
    plt.colorbar(sc, ax=ax, label=color_label)
    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} var)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} var)")
    ax.set_title(title)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--n-proteins", type=int, default=250)
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("Loading sequences...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    audit_csv = REPORT_DIR / "anchor_behavior_audit.csv"
    print(f"Selecting {args.n_proteins} proteins (stratified by length)...")
    proteins = select_proteins(audit_csv, all_seqs, args.n_proteins)
    print(f"  Selected {len(proteins)} anchor-like proteins")
    lengths = [p["n_res"] for p in proteins]
    print(f"  Length range: {min(lengths)}-{max(lengths)}, mean={np.mean(lengths):.0f}, median={np.median(lengths):.0f}")

    print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    d = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_unit = (d / d.norm().clamp(min=1e-8)).to(args.device)

    # ===================================================================
    # Phase A: Flank sweep
    # ===================================================================
    print(f"\n{'='*60}")
    print(f"Phase A: Flank sweep on {len(proteins)} proteins")
    print(f"{'='*60}")

    sweep_results = {}
    t0 = time.time()
    errors = 0
    for i, p in enumerate(proteins):
        pid = p["protein"]
        seq = all_seqs[pid]
        anchor = p["anchor_pos"]
        try:
            result = run_flank_sweep(model, tokenizer, pid, seq, anchor, d_unit, args.device)
            sweep_results[pid] = result
            sweep_results[pid]["anchor_pos"] = anchor
            sweep_results[pid]["n_res"] = len(seq)
        except Exception as e:
            print(f"  ERROR on {pid}: {e}")
            errors += 1
            continue

        if (i + 1) % 25 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed
            eta = (len(proteins) - i - 1) / rate
            done_r50s = [v["R_50"] for v in sweep_results.values() if v["R_50"] is not None]
            med_r50 = int(np.median(done_r50s)) if done_r50s else "?"
            print(f"  [{i+1}/{len(proteins)}] {rate:.1f} prot/s, ETA {eta:.0f}s | median R_50 so far: {med_r50} | errors: {errors}")

    elapsed = time.time() - t0
    print(f"\nPhase A done: {len(sweep_results)} proteins in {elapsed:.0f}s ({len(sweep_results)/elapsed:.1f} prot/s)")

    # Save sweep results
    sweep_csv = REPORT_DIR / "anchor_flank_clustering_v2_sweep.csv"
    with open(sweep_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["protein", "n_res", "anchor_pos", "R_50", "alpha_full"])
        for pid, res in sweep_results.items():
            writer.writerow([pid, res["n_res"], res["anchor_pos"], res["R_50"], f"{res['alpha_full']:.6f}"])
    print(f"Saved: {sweep_csv}")

    # R_50 distribution
    r50_vals = [v["R_50"] for v in sweep_results.values() if v["R_50"] is not None]
    print(f"\nR_50 distribution (n={len(r50_vals)}):")
    for r in sorted(set(r50_vals)):
        ct = sum(1 for x in r50_vals if x == r)
        if ct >= 3 or r in RADII_SCHEDULE:
            print(f"  R={r}: {ct} proteins")

    # ===================================================================
    # Phase B: Extract flanks
    # ===================================================================
    print(f"\n{'='*60}")
    print(f"Phase B: Extracting minimal flanks at discovered R_50")
    print(f"{'='*60}")

    flanks = {}
    for pid, res in sweep_results.items():
        if res["R_50"] is None:
            continue
        seq = all_seqs[pid]
        anchor = res["anchor_pos"]
        radius = res["R_50"]
        start = max(0, anchor - radius)
        end = min(len(seq), anchor + radius + 1)
        flank_seq = seq[start:end]
        flanks[pid] = {
            "sequence": flank_seq,
            "anchor_pos": anchor,
            "radius": radius,
            "start": start,
            "end": end,
            "offset_to_anchor": anchor - start,
            "n_res_full": len(seq),
            "n_res_flank": len(flank_seq),
            "anchor_aa": seq[anchor],
        }

    pids = sorted(flanks.keys())
    print(f"  {len(pids)} flanks extracted")

    flank_lens = [flanks[p]["n_res_flank"] for p in pids]
    print(f"  Flank length: min={min(flank_lens)}, max={max(flank_lens)}, mean={np.mean(flank_lens):.0f}, median={np.median(flank_lens):.0f}")

    # Anchor AA composition
    anchor_aas = [flanks[p]["anchor_aa"] for p in pids]
    aa_counts = {}
    for aa in anchor_aas:
        aa_counts[aa] = aa_counts.get(aa, 0) + 1
    print("\n  Anchor residue composition:")
    for aa, ct in sorted(aa_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"    {aa}: {ct} ({ct/len(anchor_aas):.0%})")

    # ===================================================================
    # Phase C: Clustering
    # ===================================================================
    print(f"\n{'='*60}")
    print(f"Phase C: Clustering analysis")
    print(f"{'='*60}")

    n = len(pids)

    # C.1: Pairwise sequence identity
    print(f"\nComputing pairwise sequence identity ({n}x{n})...")
    id_matrix = pairwise_sequence_identity(flanks)
    id_upper = id_matrix[np.triu_indices(n, k=1)]
    print(f"  Mean: {id_upper.mean():.3f}, Max: {id_upper.max():.3f}, Min: {id_upper.min():.3f}")

    # C.2: BLOSUM62
    print("Computing pairwise BLOSUM62 scores...")
    blosum_matrix = pairwise_blosum62(flanks)
    blosum_upper = blosum_matrix[np.triu_indices(n, k=1)]
    print(f"  Mean: {blosum_upper.mean():.2f}")

    # C.3: ESM2 embeddings
    print(f"\nComputing ESM2 flank embeddings ({len(pids)} proteins)...")
    mean_embs = []
    anchor_embs = []
    for i, pid in enumerate(pids):
        f = flanks[pid]
        mean_embs.append(get_flank_embedding(model, tokenizer, f["sequence"], args.device))
        anchor_embs.append(get_anchor_embedding(model, tokenizer, f["sequence"], f["offset_to_anchor"], args.device))
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(pids)} done")

    mean_embs = np.array(mean_embs)
    anchor_embs = np.array(anchor_embs)

    mean_cos = 1.0 - spatial.distance.squareform(spatial.distance.pdist(mean_embs, metric="cosine"))
    anchor_cos = 1.0 - spatial.distance.squareform(spatial.distance.pdist(anchor_embs, metric="cosine"))

    mean_cos_upper = mean_cos[np.triu_indices(n, k=1)]
    anchor_cos_upper = anchor_cos[np.triu_indices(n, k=1)]
    print(f"\n  Mean flank embedding cosine sim: {mean_cos_upper.mean():.3f}")
    print(f"  Anchor-position embedding cosine sim: {anchor_cos_upper.mean():.3f}")

    # Hierarchical clustering
    id_dist = spatial.distance.squareform(1.0 - id_matrix)
    id_linkage = cluster.hierarchy.linkage(id_dist, method="average")

    emb_dist = spatial.distance.pdist(mean_embs, metric="cosine")
    emb_linkage = cluster.hierarchy.linkage(emb_dist, method="average")

    anchor_emb_dist = spatial.distance.pdist(anchor_embs, metric="cosine")
    anchor_emb_linkage = cluster.hierarchy.linkage(anchor_emb_dist, method="average")

    # Cross-analysis
    print("\n  Cross-correlations:")
    rho_id_mean, p_id_mean = sp_stats.spearmanr(id_upper, mean_cos_upper)
    rho_id_anch, p_id_anch = sp_stats.spearmanr(id_upper, anchor_cos_upper)
    rho_bl_mean, p_bl_mean = sp_stats.spearmanr(blosum_upper, mean_cos_upper)
    print(f"    Spearman(seq_id, mean_emb_cos): rho={rho_id_mean:.3f}, p={p_id_mean:.2e}")
    print(f"    Spearman(seq_id, anchor_emb_cos): rho={rho_id_anch:.3f}, p={p_id_anch:.2e}")
    print(f"    Spearman(blosum, mean_emb_cos): rho={rho_bl_mean:.3f}, p={p_bl_mean:.2e}")

    radii = [flanks[p]["radius"] for p in pids]
    full_lengths = [flanks[p]["n_res_full"] for p in pids]
    rho_len_rad, p_len_rad = sp_stats.spearmanr(full_lengths, radii)
    print(f"    Spearman(protein_length, R_50): rho={rho_len_rad:.3f}, p={p_len_rad:.2e}")

    # ===================================================================
    # Plots
    # ===================================================================
    print(f"\n{'='*60}")
    print("Generating plots")
    print(f"{'='*60}")

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "figure.dpi": 200})

    short_labels = [f"{p[:4]}R{flanks[p]['radius']}" for p in pids]

    # Order by embedding dendrogram
    emb_order = cluster.hierarchy.leaves_list(emb_linkage)
    ord_labels = [short_labels[i] for i in emb_order]

    # Similarity matrices (ordered by embedding clustering)
    plot_sim_matrix(id_matrix[np.ix_(emb_order, emb_order)], ord_labels,
                    f"Pairwise sequence identity of minimal flanks (n={n})",
                    REPORT_DIR / "anchor_flank_v2_seq_identity.png", cmap="YlOrRd", vmin=0, vmax=0.4)

    plot_sim_matrix(mean_cos[np.ix_(emb_order, emb_order)], ord_labels,
                    f"Mean flank embedding cosine similarity (n={n})",
                    REPORT_DIR / "anchor_flank_v2_emb_cosine.png", cmap="RdYlBu_r", vmin=0.7, vmax=1.0)

    plot_sim_matrix(anchor_cos[np.ix_(emb_order, emb_order)], ord_labels,
                    f"Anchor-position embedding cosine similarity (n={n})",
                    REPORT_DIR / "anchor_flank_v2_anchor_emb_cosine.png", cmap="RdYlBu_r", vmin=None, vmax=1.0)

    # Dendrograms
    plot_dendro(id_linkage, short_labels, f"Clustering by flank sequence identity (n={n})",
                REPORT_DIR / "anchor_flank_v2_seq_dendro.png")
    plot_dendro(emb_linkage, short_labels, f"Clustering by mean flank embedding (n={n})",
                REPORT_DIR / "anchor_flank_v2_emb_dendro.png")
    plot_dendro(anchor_emb_linkage, short_labels, f"Clustering by anchor-position embedding (n={n})",
                REPORT_DIR / "anchor_flank_v2_anchor_dendro.png")

    # PCA
    plot_pca(mean_embs, [p[:5] for p in pids], radii, "R_50",
             f"PCA of mean flank embeddings (n={n}, colored by R_50)",
             REPORT_DIR / "anchor_flank_v2_emb_pca.png")
    plot_pca(anchor_embs, [p[:5] for p in pids], radii, "R_50",
             f"PCA of anchor-position embeddings (n={n}, colored by R_50)",
             REPORT_DIR / "anchor_flank_v2_anchor_pca.png")

    # PCA colored by anchor AA type (hydrophobic vs other)
    hydrophobic = {'V', 'I', 'L', 'F', 'W', 'M', 'A'}
    aa_is_hydrophobic = [1.0 if flanks[p]["anchor_aa"] in hydrophobic else 0.0 for p in pids]
    plot_pca(anchor_embs, [p[:5] for p in pids], aa_is_hydrophobic, "Hydrophobic anchor",
             f"PCA of anchor embeddings (n={n}, colored by hydrophobic anchor)",
             REPORT_DIR / "anchor_flank_v2_anchor_pca_hydro.png")

    # Cross-analysis scatter
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    axes[0].scatter(id_upper, mean_cos_upper, s=1, alpha=0.1, color="#5B7FA3")
    axes[0].set_xlabel("Flank sequence identity")
    axes[0].set_ylabel("Mean embedding cosine sim")
    axes[0].set_title(f"rho={rho_id_mean:.3f}")
    axes[1].scatter(id_upper, anchor_cos_upper, s=1, alpha=0.1, color="#D64550")
    axes[1].set_xlabel("Flank sequence identity")
    axes[1].set_ylabel("Anchor embedding cosine sim")
    axes[1].set_title(f"rho={rho_id_anch:.3f}")
    axes[2].scatter(full_lengths, radii, s=8, alpha=0.4, color="#4DAF4A")
    axes[2].set_xlabel("Protein length")
    axes[2].set_ylabel("R_50")
    axes[2].set_title(f"Length vs R_50 (rho={rho_len_rad:.3f})")
    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_flank_v2_cross_analysis.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {REPORT_DIR / 'anchor_flank_v2_cross_analysis.png'}")

    # R_50 distribution histogram
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(r50_vals, bins=20, color="#5B7FA3", edgecolor="white")
    ax.set_xlabel("R_50 (minimal flank radius for 50% projection recovery)")
    ax.set_ylabel("Count")
    ax.set_title(f"Distribution of minimal flank radii (n={len(r50_vals)})")
    ax.axvline(np.median(r50_vals), color="#D64550", lw=2, ls="--", label=f"Median={int(np.median(r50_vals))}")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_flank_v2_r50_distribution.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {REPORT_DIR / 'anchor_flank_v2_r50_distribution.png'}")

    # ===================================================================
    # Report
    # ===================================================================
    print("\nWriting report...")
    report = []
    report.append("# Anchor Flank Clustering v2 (Scaled Up)\n\n")
    report.append(f"Proteins: {len(pids)} (stratified sample from {len(proteins)} anchor-like proteins in behavior audit).\n")
    report.append(f"Flank sweep: {len(RADII_SCHEDULE)} radii + full, discovering actual R_50 per protein.\n")
    report.append(f"Recovery threshold: {RECOVERY_THRESHOLD:.0%} of full-sequence projection.\n\n")

    report.append("## R_50 distribution\n\n")
    report.append(f"Median R_50: {int(np.median(r50_vals))}.\n")
    report.append(f"Mean: {np.mean(r50_vals):.0f}.\n")
    report.append(f"Range: {min(r50_vals)}-{max(r50_vals)}.\n")
    report.append(f"Correlation with protein length: Spearman rho={rho_len_rad:.3f} (p={p_len_rad:.2e}).\n\n")
    report.append("![R_50 distribution](anchor_flank_v2_r50_distribution.png)\n\n")

    report.append("## Anchor residue composition\n\n")
    for aa, ct in sorted(aa_counts.items(), key=lambda x: -x[1])[:10]:
        report.append(f"- {aa}: {ct} ({ct/len(anchor_aas):.0%})\n")
    hydro_frac = sum(1 for a in anchor_aas if a in hydrophobic) / len(anchor_aas)
    report.append(f"\nHydrophobic anchor residues (V/I/L/F/W/M/A): {hydro_frac:.0%}.\n\n")

    report.append("## Sequence identity of minimal flanks\n\n")
    report.append(f"Mean pairwise identity (center-aligned): {id_upper.mean():.3f}.\n")
    report.append(f"Max: {id_upper.max():.3f}. Min: {id_upper.min():.3f}.\n")
    report.append(f"Mean BLOSUM62 score: {blosum_upper.mean():.2f}.\n\n")
    report.append("![Sequence identity](anchor_flank_v2_seq_identity.png)\n\n")
    report.append("![Sequence dendrogram](anchor_flank_v2_seq_dendro.png)\n\n")

    report.append("## ESM2 embedding similarity\n\n")
    report.append(f"Mean flank embedding cosine sim: {mean_cos_upper.mean():.3f}.\n")
    report.append(f"Anchor-position embedding cosine sim: {anchor_cos_upper.mean():.3f}.\n\n")
    report.append("![Mean embedding cosine](anchor_flank_v2_emb_cosine.png)\n\n")
    report.append("![Anchor embedding cosine](anchor_flank_v2_anchor_emb_cosine.png)\n\n")
    report.append("![Mean embedding dendrogram](anchor_flank_v2_emb_dendro.png)\n\n")
    report.append("![Anchor embedding dendrogram](anchor_flank_v2_anchor_dendro.png)\n\n")
    report.append("![Mean embedding PCA](anchor_flank_v2_emb_pca.png)\n\n")
    report.append("![Anchor embedding PCA](anchor_flank_v2_anchor_pca.png)\n\n")
    report.append("![Anchor PCA hydrophobic](anchor_flank_v2_anchor_pca_hydro.png)\n\n")

    report.append("## Cross-analysis\n\n")
    report.append(f"Spearman(seq_id, mean_emb_cos): rho={rho_id_mean:.3f} (p={p_id_mean:.2e}).\n")
    report.append(f"Spearman(seq_id, anchor_emb_cos): rho={rho_id_anch:.3f} (p={p_id_anch:.2e}).\n")
    report.append(f"Spearman(blosum, mean_emb_cos): rho={rho_bl_mean:.3f} (p={p_bl_mean:.2e}).\n\n")
    report.append("![Cross-analysis](anchor_flank_v2_cross_analysis.png)\n\n")

    report_path = REPORT_DIR / "anchor_flank_clustering_v2.md"
    with open(report_path, "w") as f:
        f.writelines(report)
    print(f"Saved: {report_path}")

    # Save flank CSV
    csv_path = REPORT_DIR / "anchor_flank_clustering_v2_flanks.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["protein", "n_res_full", "anchor_pos", "anchor_aa", "R_50", "flank_start", "flank_end", "flank_len", "flank_sequence"])
        for pid in pids:
            fl = flanks[pid]
            writer.writerow([pid, fl["n_res_full"], fl["anchor_pos"], fl["anchor_aa"],
                             fl["radius"], fl["start"], fl["end"], fl["n_res_flank"], fl["sequence"]])
    print(f"Saved: {csv_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
