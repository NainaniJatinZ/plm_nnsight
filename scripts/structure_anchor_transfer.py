#!/usr/bin/env python3
"""Anchor transfer across structural homologs (low sequence identity).

Tests whether L10H9 anchor positions map to structurally equivalent sites
across proteins with similar 3D folds but dissimilar sequences, using a
foldmason multiple structure alignment of 1PVGA and 10 remote homologs
(TM-score > 0.6, sequence identity < 25% relative to 1PVGA).

Phases:
  1. Parse foldmason alignment, build column-to-position mappings, verify data.
  2. Run L10H9 anchor behavior audit on each protein (go/no-go gate).
  3. Map anchor positions to alignment columns, test concordance and projection transfer.
  4. Visualize: alignment-column projection heatmap, concordance summary, report.

Usage:
    uv run python scripts/structure_anchor_transfer.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
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

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
FOLDMASON_DIR = DATA_DIR / "foldmason"
PDB_DIR = FOLDMASON_DIR / "pdbs"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN = "2B61A"
REFERENCE_ANCHOR_POS = 101  # 1PVGA known anchor (0-indexed in ungapped sequence)

# Anchor-like thresholds (same as 2k-protein audit)
ANCHOR_TOP1_THRESH = 0.15
ANCHOR_RANKCORR_THRESH = 0.3


# ---------------------------------------------------------------------------
# Model + weights (copied from anchor_behavior_audit.py)
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


def compute_search_dir_from_full_seq(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Compute d = W_K^T @ q_mean from a full (unmasked) sequence."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    return W_K.T @ q_mean_norm


# ---------------------------------------------------------------------------
# Phase 1: Parse alignment and build mappings
# ---------------------------------------------------------------------------

def parse_fasta_alignment(fasta_path: Path) -> dict[str, str]:
    """Parse a FASTA alignment file. Returns {header: aligned_sequence}."""
    records = {}
    current_header = None
    current_seq = []
    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_header is not None:
                    records[current_header] = "".join(current_seq)
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
    if current_header is not None:
        records[current_header] = "".join(current_seq)
    return records


def build_alignment_mappings(aligned_seqs: dict[str, str]):
    """Build column-to-position and position-to-column mappings for each protein.

    Returns:
        ungapped_seqs: {name: ungapped_sequence}
        col_to_pos: {name: list where col_to_pos[name][col] = ungapped position or -1 if gap}
        pos_to_col: {name: list where pos_to_col[name][pos] = alignment column}
    """
    ungapped_seqs = {}
    col_to_pos = {}
    pos_to_col = {}

    for name, aligned in aligned_seqs.items():
        ungapped = aligned.replace("-", "")
        ungapped_seqs[name] = ungapped

        c2p = []
        p2c = []
        pos = 0
        for col_idx, char in enumerate(aligned):
            if char == "-":
                c2p.append(-1)
            else:
                c2p.append(pos)
                p2c.append(col_idx)
                pos += 1
        col_to_pos[name] = c2p
        pos_to_col[name] = p2c

    return ungapped_seqs, col_to_pos, pos_to_col


def compute_pairwise_identity(ungapped_seqs: dict[str, str], aligned_seqs: dict[str, str]) -> dict[tuple[str, str], float]:
    """Compute pairwise sequence identity from the alignment (fraction of aligned columns with identical residues)."""
    names = list(aligned_seqs.keys())
    identities = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = aligned_seqs[names[i]]
            b = aligned_seqs[names[j]]
            aligned_count = 0
            match_count = 0
            for ca, cb in zip(a, b):
                if ca != "-" and cb != "-":
                    aligned_count += 1
                    if ca == cb:
                        match_count += 1
            identity = match_count / max(aligned_count, 1)
            identities[(names[i], names[j])] = identity
            identities[(names[j], names[i])] = identity
    return identities


def extract_pdb_id(name: str) -> str:
    """Extract 4-letter PDB ID from foldmason header like '1ei1-assembly1cifgz'."""
    return name[:4]


def download_pdbs(names: list[str], out_dir: Path):
    """Download PDB files from RCSB for each unique PDB ID."""
    import requests
    out_dir.mkdir(parents=True, exist_ok=True)
    seen = set()
    for name in names:
        pdb_id = extract_pdb_id(name)
        if pdb_id in seen:
            continue
        seen.add(pdb_id)
        out_path = out_dir / f"{pdb_id}.cif"
        if out_path.exists():
            print(f"  {pdb_id}: already downloaded")
            continue
        url = f"https://files.rcsb.org/download/{pdb_id}.cif"
        print(f"  {pdb_id}: downloading from RCSB...")
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            print(f"  WARNING: failed to download {pdb_id}: {e}")


# ---------------------------------------------------------------------------
# Phase 2: Anchor behavior analysis (adapted from anchor_behavior_audit.py)
# ---------------------------------------------------------------------------

@torch.no_grad()
def analyze_protein(
    model, tokenizer, protein_id: str, sequence: str,
    d_ref: torch.Tensor, weights: dict, device: str,
) -> dict | None:
    """Run one protein through ESM2, cache L10H9 attention + L10 LN, compute all metrics.

    Also computes a protein-specific search direction d_self and its cosine similarity to d_ref.
    """
    if len(sequence) < 10:
        return None

    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    n_res = len(sequence)

    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=[attn_module, ln_module])

    attn_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"

    attn_all_heads = cache[attn_key].output[1].detach().cpu()[0]
    A = attn_all_heads[TARGET_HEAD, 1:-1, 1:-1].clone()

    x_ln = cache[ln_key].output.detach().cpu()[0, 1:-1]

    # Projection scores using reference direction
    proj_scores = (x_ln @ d_ref.cpu()).numpy()

    # Protein-specific search direction
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q
    q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    d_self = W_K.T @ q_mean_norm
    d_self_unit = d_self / d_self.norm().clamp(min=1e-8)
    d_ref_unit = d_ref.cpu() / d_ref.cpu().norm().clamp(min=1e-8)
    cos_sim_d = float(torch.dot(d_self_unit, d_ref_unit))

    # Projection scores using self direction
    proj_scores_self = (x_ln @ d_self_unit).numpy()

    # 1. Verticality metrics
    max_per_query = A.max(dim=1).values.numpy()
    mean_max_attn = float(max_per_query.mean())

    mean_key_dist = A.mean(dim=0).numpy()
    mean_key_dist_sorted = np.sort(mean_key_dist)[::-1]

    top1_mass = float(mean_key_dist_sorted[0])
    top3_mass = float(mean_key_dist_sorted[:min(3, n_res)].sum())

    p = mean_key_dist / (mean_key_dist.sum() + 1e-12)
    entropy = -float(np.sum(p * np.log(p + 1e-12)))
    eff_keys = float(np.exp(entropy))

    # 2. Anchor concentration
    cumsum = np.cumsum(mean_key_dist_sorted)
    total_mass = cumsum[-1]
    keys_50pct = int(np.searchsorted(cumsum, total_mass * 0.5) + 1)
    max_key_mass = float(mean_key_dist_sorted[0])
    top3_key_mass = float(mean_key_dist_sorted[:min(3, n_res)].sum())

    # 3. Projection-attention agreement
    attn_rank = np.argsort(-mean_key_dist)
    proj_rank = np.argsort(-proj_scores)

    rho, rho_p = sp_stats.spearmanr(mean_key_dist, proj_scores)

    attn_top3_set = set(attn_rank[:3].tolist())
    proj_top3_set = set(proj_rank[:3].tolist())
    top3_overlap = len(attn_top3_set & proj_top3_set) / 3.0

    # Anchor position = argmax of mean key distribution
    anchor_pos = int(attn_rank[0])
    top3_positions = attn_rank[:3].tolist()
    top5_positions = attn_rank[:5].tolist()

    # Top-3 by projection score
    proj_top3_positions = proj_rank[:3].tolist()

    return {
        "protein": protein_id,
        "n_res": n_res,
        "mean_max_attn": mean_max_attn,
        "top1_mass": top1_mass,
        "top3_mass": top3_mass,
        "eff_keys": eff_keys,
        "keys_50pct": keys_50pct,
        "max_key_mass": max_key_mass,
        "top3_key_mass": top3_key_mass,
        "rank_corr": float(rho),
        "rank_corr_p": float(rho_p),
        "top3_overlap": top3_overlap,
        "cos_sim_d": cos_sim_d,
        "anchor_pos": anchor_pos,
        "anchor_aa": sequence[anchor_pos] if anchor_pos < len(sequence) else "?",
        "top3_positions": top3_positions,
        "top5_positions": top5_positions,
        "proj_top3_positions": proj_top3_positions,
        "proj_scores": proj_scores,
        "proj_scores_self": proj_scores_self,
        "mean_key_dist": mean_key_dist,
        "is_anchor_like": top1_mass > ANCHOR_TOP1_THRESH and float(rho) > ANCHOR_RANKCORR_THRESH,
    }


# ---------------------------------------------------------------------------
# Phase 3: Concordance and transfer analysis
# ---------------------------------------------------------------------------

def anchor_column_concordance(results: list[dict], pos_to_col: dict[str, list], names: list[str]):
    """For each pair of anchor-like proteins, compute the alignment column distance between their anchor positions.

    Returns list of dicts with pairwise info.
    """
    # Map protein_id -> result
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    pairs = []

    anchor_like_names = [n for n in names if n in result_map]
    for i in range(len(anchor_like_names)):
        for j in range(i + 1, len(anchor_like_names)):
            na, nb = anchor_like_names[i], anchor_like_names[j]
            ra, rb = result_map[na], result_map[nb]

            pos_a = ra["anchor_pos"]
            pos_b = rb["anchor_pos"]

            # Map to alignment columns
            if pos_a >= len(pos_to_col[na]) or pos_b >= len(pos_to_col[nb]):
                continue
            col_a = pos_to_col[na][pos_a]
            col_b = pos_to_col[nb][pos_b]

            pairs.append({
                "protein_a": na,
                "protein_b": nb,
                "anchor_pos_a": pos_a,
                "anchor_pos_b": pos_b,
                "anchor_col_a": col_a,
                "anchor_col_b": col_b,
                "col_distance": abs(col_a - col_b),
            })
    return pairs


def random_position_column_spread(results: list[dict], pos_to_col: dict[str, list], names: list[str], n_random: int = 10, seed: int = 42):
    """For each anchor-like protein, pick n_random random non-anchor positions and compute their alignment column spread (mean pairwise distance) as a control.

    Returns the mean pairwise column distance for random positions and for anchor positions.
    """
    rng = np.random.RandomState(seed)
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]

    if len(anchor_like_names) < 2:
        return None, None

    # Anchor columns
    anchor_cols = []
    for n in anchor_like_names:
        pos = result_map[n]["anchor_pos"]
        if pos < len(pos_to_col[n]):
            anchor_cols.append(pos_to_col[n][pos])

    # Random control: for each protein, pick n_random positions, map to columns
    n_trials = 200
    random_mean_dists = []
    for _ in range(n_trials):
        random_cols = []
        for n in anchor_like_names:
            n_res = result_map[n]["n_res"]
            anchor_pos = result_map[n]["anchor_pos"]
            candidates = [p for p in range(n_res) if p != anchor_pos and p < len(pos_to_col[n])]
            if not candidates:
                continue
            rp = rng.choice(candidates)
            random_cols.append(pos_to_col[n][rp])
        if len(random_cols) >= 2:
            dists = [abs(random_cols[a] - random_cols[b]) for a in range(len(random_cols)) for b in range(a + 1, len(random_cols))]
            random_mean_dists.append(np.mean(dists))

    anchor_dists = [abs(anchor_cols[a] - anchor_cols[b]) for a in range(len(anchor_cols)) for b in range(a + 1, len(anchor_cols))]
    anchor_mean_dist = np.mean(anchor_dists) if anchor_dists else float("nan")
    random_mean_dist_distribution = np.array(random_mean_dists) if random_mean_dists else np.array([])

    return anchor_mean_dist, random_mean_dist_distribution


def projection_score_transfer(results: list[dict], pos_to_col: dict[str, list], col_to_pos: dict[str, list], names: list[str]):
    """For each pair (A, B) of anchor-like proteins: take A's anchor column, find B's residue at that column, check B's projection rank at that residue.

    Returns list of dicts with transfer results.
    """
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]
    transfers = []

    for na in anchor_like_names:
        ra = result_map[na]
        pos_a = ra["anchor_pos"]
        if pos_a >= len(pos_to_col[na]):
            continue
        col_a = pos_to_col[na][pos_a]

        for nb in anchor_like_names:
            if na == nb:
                continue
            rb = result_map[nb]

            # Find B's position at A's anchor column
            if col_a >= len(col_to_pos[nb]):
                continue
            pos_b_at_col = col_to_pos[nb][col_a]
            if pos_b_at_col == -1:
                # Gap in B at this column
                transfers.append({
                    "source": na, "target": nb,
                    "source_anchor_pos": pos_a, "source_anchor_col": col_a,
                    "target_pos": -1, "target_proj_rank": -1,
                    "is_gap": True,
                    "in_top1": False, "in_top3": False, "in_top5": False, "in_top10": False,
                })
                continue

            # Check B's projection rank at the transferred position
            proj_scores_b = rb["proj_scores"]
            proj_rank_b = np.argsort(np.argsort(-proj_scores_b))
            rank_at_transfer = int(proj_rank_b[pos_b_at_col])

            n_res_b = rb["n_res"]
            transfers.append({
                "source": na, "target": nb,
                "source_anchor_pos": pos_a, "source_anchor_col": col_a,
                "target_pos": pos_b_at_col, "target_proj_rank": rank_at_transfer,
                "is_gap": False,
                "in_top1": rank_at_transfer == 0,
                "in_top3": rank_at_transfer < 3,
                "in_top5": rank_at_transfer < 5,
                "in_top10": rank_at_transfer < 10,
            })

    return transfers


# ---------------------------------------------------------------------------
# Phase 4: Visualization and report
# ---------------------------------------------------------------------------

def plot_projection_heatmap(results: list[dict], col_to_pos: dict[str, list], pos_to_col: dict[str, list], names: list[str], out_path: Path):
    """Heatmap: proteins (rows) x alignment columns (cols), colored by projection score. Anchor positions marked."""
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]
    if not anchor_like_names:
        print("  No anchor-like proteins to plot.")
        return

    # Determine alignment length
    aln_len = len(col_to_pos[names[0]])

    # Find columns where at least one anchor-like protein has a residue
    occupied_cols = set()
    for n in anchor_like_names:
        for col, pos in enumerate(col_to_pos[n]):
            if pos != -1:
                occupied_cols.add(col)
    occupied_cols = sorted(occupied_cols)

    # Build matrix: rows = proteins, cols = occupied alignment columns
    matrix = np.full((len(anchor_like_names), len(occupied_cols)), np.nan)
    anchor_markers = []

    for row_idx, n in enumerate(anchor_like_names):
        r = result_map[n]
        proj = r["proj_scores"]
        anchor_pos = r["anchor_pos"]
        for col_idx, aln_col in enumerate(occupied_cols):
            if aln_col < len(col_to_pos[n]):
                seq_pos = col_to_pos[n][aln_col]
                if seq_pos != -1 and seq_pos < len(proj):
                    matrix[row_idx, col_idx] = proj[seq_pos]
                    if seq_pos == anchor_pos:
                        anchor_markers.append((col_idx, row_idx))

    fig, ax = plt.subplots(figsize=(14, max(3, 0.5 * len(anchor_like_names) + 1)))
    im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", interpolation="none")
    plt.colorbar(im, ax=ax, label="Projection score (x_i . d)", shrink=0.8)

    # Mark anchor positions
    for cx, ry in anchor_markers:
        ax.plot(cx, ry, marker="*", color="blue", markersize=8, markeredgecolor="white", markeredgewidth=0.5)

    # Label rows
    short_names = [extract_pdb_id(n) + " " + n.split("-")[1][:5] for n in anchor_like_names]
    ax.set_yticks(range(len(anchor_like_names)))
    ax.set_yticklabels(short_names, fontsize=7)

    # X-axis: show every 20th column
    xtick_step = max(1, len(occupied_cols) // 20)
    xtick_positions = list(range(0, len(occupied_cols), xtick_step))
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels([str(occupied_cols[i]) for i in xtick_positions], fontsize=6, rotation=45)

    ax.set_xlabel("Alignment column")
    ax.set_ylabel("Protein")
    ax.set_title("L10H9 projection score across structural alignment (blue stars = anchor positions)")

    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_mean_projection_by_column(results: list[dict], col_to_pos: dict[str, list], pos_to_col: dict[str, list], names: list[str], out_path: Path):
    """Bar plot: mean projection score across anchor-like proteins at each alignment column. Highlight anchor columns."""
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]
    if not anchor_like_names:
        return

    aln_len = len(col_to_pos[names[0]])

    # For each column, collect projection scores across proteins
    col_scores = [[] for _ in range(aln_len)]
    anchor_cols = set()
    for n in anchor_like_names:
        r = result_map[n]
        proj = r["proj_scores"]
        anchor_pos = r["anchor_pos"]
        if anchor_pos < len(pos_to_col[n]):
            anchor_cols.add(pos_to_col[n][anchor_pos])
        for col in range(aln_len):
            if col < len(col_to_pos[n]):
                seq_pos = col_to_pos[n][col]
                if seq_pos != -1 and seq_pos < len(proj):
                    col_scores[col].append(proj[seq_pos])

    # Compute mean and count for each column
    mean_scores = []
    counts = []
    for col in range(aln_len):
        if col_scores[col]:
            mean_scores.append(np.mean(col_scores[col]))
            counts.append(len(col_scores[col]))
        else:
            mean_scores.append(0.0)
            counts.append(0)
    mean_scores = np.array(mean_scores)
    counts = np.array(counts)

    # Only plot columns with at least 2 proteins
    mask = counts >= 2
    cols_to_plot = np.where(mask)[0]
    if len(cols_to_plot) == 0:
        return

    fig, ax = plt.subplots(figsize=(14, 4))
    colors = ["#D64550" if c in anchor_cols else "#5B7FA3" for c in cols_to_plot]
    ax.bar(range(len(cols_to_plot)), mean_scores[cols_to_plot], color=colors, width=1.0, edgecolor="none")

    # Mark anchor columns
    for idx, c in enumerate(cols_to_plot):
        if c in anchor_cols:
            ax.annotate("", xy=(idx, mean_scores[c]), xytext=(idx, mean_scores[c] + 0.3),
                        arrowprops=dict(arrowstyle="->", color="#D64550", lw=1.5))

    xtick_step = max(1, len(cols_to_plot) // 20)
    ax.set_xticks(range(0, len(cols_to_plot), xtick_step))
    ax.set_xticklabels([str(cols_to_plot[i]) for i in range(0, len(cols_to_plot), xtick_step)], fontsize=6, rotation=45)

    ax.set_xlabel("Alignment column")
    ax.set_ylabel("Mean projection score (across proteins)")
    ax.set_title("Mean L10H9 projection score by alignment column (red = anchor columns)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_concordance_control(anchor_mean_dist, random_dist_distribution, out_path: Path):
    """Histogram of random pairwise column distances vs anchor pairwise column distance."""
    if random_dist_distribution is None or len(random_dist_distribution) == 0:
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(random_dist_distribution, bins=30, color="#C4D4E4", edgecolor="#5B7FA3", linewidth=0.5, label="Random positions (200 trials)")
    ax.axvline(anchor_mean_dist, color="#D64550", lw=2, label=f"Anchor positions (mean dist = {anchor_mean_dist:.1f})")

    percentile = np.mean(random_dist_distribution >= anchor_mean_dist) * 100
    ax.text(0.95, 0.95, f"Anchor < {percentile:.0f}% of random", fontsize=8, ha="right", va="top", transform=ax.transAxes)

    ax.set_xlabel("Mean pairwise alignment column distance")
    ax.set_ylabel("Count (random trials)")
    ax.set_title("Anchor column clustering vs random control")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Anchor transfer across structural homologs")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--skip-pdb-download", action="store_true", help="Skip PDB download step")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    PDB_DIR.mkdir(parents=True, exist_ok=True)

    # ===================================================================
    # Phase 1: Parse alignment and build mappings
    # ===================================================================
    print("=" * 60)
    print("Phase 1: Data preparation")
    print("=" * 60)

    print("\nParsing foldmason alignment...")
    aligned_seqs = parse_fasta_alignment(FOLDMASON_DIR / "foldmason_aa.fa")
    names = list(aligned_seqs.keys())
    aln_len = len(next(iter(aligned_seqs.values())))
    print(f"  {len(names)} proteins, alignment length = {aln_len} columns")

    # Verify all sequences have the same alignment length
    for n, s in aligned_seqs.items():
        assert len(s) == aln_len, f"{n} has length {len(s)}, expected {aln_len}"

    ungapped_seqs, col_to_pos, pos_to_col = build_alignment_mappings(aligned_seqs)

    print("\nUngapped sequence lengths:")
    for n in names:
        print(f"  {n}: {len(ungapped_seqs[n])} residues")

    # Identify 1pvg
    pvg_name = [n for n in names if n.startswith("1pvg")][0]
    print(f"\nReference protein: {pvg_name}")

    # Verify 1PVGA anchor at position 101 maps to a sensible column
    if REFERENCE_ANCHOR_POS < len(pos_to_col[pvg_name]):
        pvg_anchor_col = pos_to_col[pvg_name][REFERENCE_ANCHOR_POS]
        pvg_anchor_aa = ungapped_seqs[pvg_name][REFERENCE_ANCHOR_POS]
        print(f"  1PVGA anchor at seq pos {REFERENCE_ANCHOR_POS} (AA: {pvg_anchor_aa}) -> alignment column {pvg_anchor_col}")
    else:
        print(f"  WARNING: 1PVGA anchor pos {REFERENCE_ANCHOR_POS} out of range (seq len {len(ungapped_seqs[pvg_name])})")
        pvg_anchor_col = None

    # Pairwise sequence identity
    print("\nPairwise sequence identity (from alignment):")
    identities = compute_pairwise_identity(ungapped_seqs, aligned_seqs)
    # Print identity matrix header
    short = {n: extract_pdb_id(n) for n in names}
    # Flag near-duplicates
    duplicates = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ident = identities[(names[i], names[j])]
            if ident > 0.90:
                duplicates.append((names[i], names[j], ident))
                print(f"  NEAR-DUPLICATE: {short[names[i]]} - {short[names[j]]}: {ident:.1%}")

    # Print identities relative to 1pvg
    print(f"\n  Identity to {pvg_name}:")
    for n in names:
        if n == pvg_name:
            continue
        ident = identities.get((pvg_name, n), 0.0)
        print(f"    {short[n]}: {ident:.1%}")

    # Download PDBs
    if not args.skip_pdb_download:
        print("\nDownloading PDB files...")
        download_pdbs(names, PDB_DIR)
    else:
        print("\nSkipping PDB download.")

    # ===================================================================
    # Phase 2: Anchor behavior audit
    # ===================================================================
    print("\n" + "=" * 60)
    print("Phase 2: Anchor behavior audit on structural homologs")
    print("=" * 60)

    print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    # Load reference sequence for 2B61A search direction
    import json
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    print(f"Computing reference search direction from {REFERENCE_PROTEIN}...")
    d_ref = compute_search_dir_from_full_seq(model, tokenizer, ref_seq, weights, args.device)
    d_ref_unit = (d_ref / d_ref.norm().clamp(min=1e-8)).to(args.device)

    print(f"\nAnalyzing {len(names)} proteins...")
    results = []
    for name in names:
        seq = ungapped_seqs[name]
        print(f"  {name} ({len(seq)} res)...", end=" ", flush=True)
        t0 = time.time()
        try:
            r = analyze_protein(model, tokenizer, name, seq, d_ref_unit, weights, args.device)
            if r is not None:
                results.append(r)
                status = "ANCHOR-LIKE" if r["is_anchor_like"] else "not anchor-like"
                print(f"{status} (top1={r['top1_mass']:.3f}, rho={r['rank_corr']:.3f}, cos_d={r['cos_sim_d']:.3f}) [{time.time()-t0:.1f}s]")
            else:
                print("SKIPPED (too short)")
        except Exception as e:
            print(f"ERROR: {e}")

    n_anchor_like = sum(1 for r in results if r["is_anchor_like"])
    n_non_pvg = sum(1 for r in results if r["is_anchor_like"] and r["protein"] != pvg_name)
    print(f"\n  {n_anchor_like}/{len(results)} proteins are anchor-like (threshold: top1_mass > {ANCHOR_TOP1_THRESH}, rank_corr > {ANCHOR_RANKCORR_THRESH})")
    print(f"  {n_non_pvg} of those are non-reference proteins")

    if n_anchor_like < 2:
        print("\n  STOP: Fewer than 2 anchor-like proteins. Transfer question is moot.")
        # Still save what we have
        save_audit_csv(results, REPORT_DIR / "structure_anchor_transfer_audit.csv")
        return

    # Save audit CSV
    save_audit_csv(results, REPORT_DIR / "structure_anchor_transfer_audit.csv")

    # ===================================================================
    # Phase 3: Core analysis
    # ===================================================================
    print("\n" + "=" * 60)
    print("Phase 3: Anchor column concordance and projection transfer")
    print("=" * 60)

    # 3.1: Map anchor positions to alignment columns
    print("\nAnchor positions and alignment columns:")
    for r in results:
        if not r["is_anchor_like"]:
            continue
        n = r["protein"]
        pos = r["anchor_pos"]
        if pos < len(pos_to_col[n]):
            col = pos_to_col[n][pos]
            print(f"  {extract_pdb_id(n)}: seq pos {pos} (AA: {r['anchor_aa']}) -> aln col {col}")
        else:
            print(f"  {extract_pdb_id(n)}: seq pos {pos} OUT OF RANGE")

    # 3.2: Pairwise anchor column concordance
    print("\nPairwise anchor column distances:")
    pairs = anchor_column_concordance(results, pos_to_col, names)
    for p in pairs:
        print(f"  {extract_pdb_id(p['protein_a'])} vs {extract_pdb_id(p['protein_b'])}: col {p['anchor_col_a']} vs {p['anchor_col_b']} (dist = {p['col_distance']})")

    if pairs:
        dists = [p["col_distance"] for p in pairs]
        print(f"\n  Mean pairwise column distance: {np.mean(dists):.1f}")
        print(f"  Median: {np.median(dists):.1f}")
        print(f"  Exact match (dist=0): {sum(1 for d in dists if d == 0)}/{len(dists)}")
        print(f"  Within 3 columns: {sum(1 for d in dists if d <= 3)}/{len(dists)}")
        print(f"  Within 5 columns: {sum(1 for d in dists if d <= 5)}/{len(dists)}")

    # Save concordance CSV
    conc_path = REPORT_DIR / "structure_anchor_transfer_concordance.csv"
    if pairs:
        with open(conc_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(pairs[0].keys()))
            writer.writeheader()
            writer.writerows(pairs)
        print(f"\n  Saved: {conc_path}")

    # 3.3: Random control
    print("\nRandom position control:")
    anchor_mean_dist, random_dist_distribution = random_position_column_spread(results, pos_to_col, names)
    if anchor_mean_dist is not None and len(random_dist_distribution) > 0:
        percentile = np.mean(random_dist_distribution >= anchor_mean_dist) * 100
        print(f"  Anchor mean pairwise column distance: {anchor_mean_dist:.1f}")
        print(f"  Random mean (across 200 trials): {np.mean(random_dist_distribution):.1f} +/- {np.std(random_dist_distribution):.1f}")
        print(f"  Anchor is tighter than {percentile:.0f}% of random trials")

    # 3.4: Projection score transfer
    print("\nProjection score transfer:")
    transfers = projection_score_transfer(results, pos_to_col, col_to_pos, names)
    non_gap = [t for t in transfers if not t["is_gap"]]
    gap_count = sum(1 for t in transfers if t["is_gap"])

    if non_gap:
        top1_rate = sum(1 for t in non_gap if t["in_top1"]) / len(non_gap)
        top3_rate = sum(1 for t in non_gap if t["in_top3"]) / len(non_gap)
        top5_rate = sum(1 for t in non_gap if t["in_top5"]) / len(non_gap)
        top10_rate = sum(1 for t in non_gap if t["in_top10"]) / len(non_gap)
        print(f"  {len(non_gap)} non-gap transfers, {gap_count} gap transfers")
        print(f"  Transfer -> top-1:  {top1_rate:.1%}")
        print(f"  Transfer -> top-3:  {top3_rate:.1%}")
        print(f"  Transfer -> top-5:  {top5_rate:.1%}")
        print(f"  Transfer -> top-10: {top10_rate:.1%}")
        mean_rank = np.mean([t["target_proj_rank"] for t in non_gap])
        print(f"  Mean projection rank at transferred position: {mean_rank:.1f}")
    else:
        print("  No non-gap transfers available.")
        top1_rate = top3_rate = top5_rate = top10_rate = 0.0

    # ===================================================================
    # Phase 4: Visualization and report
    # ===================================================================
    print("\n" + "=" * 60)
    print("Phase 4: Visualization and report")
    print("=" * 60)

    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "figure.dpi": 200,
    })

    print("\nGenerating projection heatmap...")
    plot_projection_heatmap(results, col_to_pos, pos_to_col, names,
                            REPORT_DIR / "structure_anchor_transfer_heatmap.png")

    print("Generating mean projection by column plot...")
    plot_mean_projection_by_column(results, col_to_pos, pos_to_col, names,
                                   REPORT_DIR / "structure_anchor_transfer_projection.png")

    print("Generating concordance control plot...")
    plot_concordance_control(anchor_mean_dist, random_dist_distribution,
                             REPORT_DIR / "structure_anchor_transfer_null_distribution.png")

    # ===================================================================
    # Write report
    # ===================================================================
    print("\nWriting report...")
    report = []
    report.append("# Anchor Transfer Across Structural Homologs\n\n")

    report.append("## Data\n\n")
    report.append(f"Foldmason multiple structure alignment of {len(names)} proteins (1PVGA + {len(names)-1} structural hits with TM-score > 0.6, sequence identity < 25% vs 1PVGA).\n")
    report.append(f"Alignment length: {aln_len} columns.\n\n")

    report.append("### Ungapped sequence lengths\n\n")
    report.append("| Protein | PDB | Ungapped length | Identity to 1PVG |\n")
    report.append("|---------|-----|-----------------|------------------|\n")
    for n in names:
        pdb = extract_pdb_id(n)
        ident = identities.get((pvg_name, n), 1.0) if n != pvg_name else 1.0
        report.append(f"| {n} | {pdb} | {len(ungapped_seqs[n])} | {ident:.1%} |\n")
    report.append("\n")

    if duplicates:
        report.append("### Near-duplicate pairs (>90% identity)\n\n")
        for na, nb, ident in duplicates:
            report.append(f"- {extract_pdb_id(na)} / {extract_pdb_id(nb)}: {ident:.1%}\n")
        report.append("\nThese pairs should be treated as single entries when interpreting concordance to avoid inflating agreement.\n\n")

    if pvg_anchor_col is not None:
        report.append(f"### 1PVGA anchor verification\n\n")
        report.append(f"1PVGA anchor at sequence position {REFERENCE_ANCHOR_POS} (AA: {pvg_anchor_aa}) maps to alignment column {pvg_anchor_col}.\n\n")

    report.append("## Phase 2: Anchor behavior audit\n\n")
    report.append(f"Reference search direction d from {REFERENCE_PROTEIN} (full sequence).\n")
    report.append(f"Anchor-like thresholds: top1_mass > {ANCHOR_TOP1_THRESH}, rank_corr > {ANCHOR_RANKCORR_THRESH}.\n\n")

    report.append("| Protein | PDB | N res | top1_mass | rank_corr | cos(d_self, d_ref) | Anchor pos | Anchor AA | Anchor-like? |\n")
    report.append("|---------|-----|-------|-----------|-----------|--------------------|-----------:|-----------|:------------:|\n")
    for r in results:
        pdb = extract_pdb_id(r["protein"])
        al = "YES" if r["is_anchor_like"] else "no"
        report.append(f"| {r['protein']} | {pdb} | {r['n_res']} | {r['top1_mass']:.3f} | {r['rank_corr']:.3f} | {r['cos_sim_d']:.3f} | {r['anchor_pos']} | {r['anchor_aa']} | {al} |\n")
    report.append(f"\n{n_anchor_like}/{len(results)} proteins pass the anchor-like gate.\n\n")

    report.append("## Phase 3: Anchor column concordance\n\n")

    report.append("### Anchor positions in alignment coordinates\n\n")
    report.append("| Protein | PDB | Anchor seq pos | Anchor aln col |\n")
    report.append("|---------|-----|---------------:|---------------:|\n")
    for r in results:
        if not r["is_anchor_like"]:
            continue
        n = r["protein"]
        pos = r["anchor_pos"]
        col = pos_to_col[n][pos] if pos < len(pos_to_col[n]) else -1
        report.append(f"| {n} | {extract_pdb_id(n)} | {pos} | {col} |\n")
    report.append("\n")

    if pairs:
        report.append("### Pairwise anchor column distances\n\n")
        dists = [p["col_distance"] for p in pairs]
        report.append(f"Mean pairwise distance: {np.mean(dists):.1f} columns.\n")
        report.append(f"Median: {np.median(dists):.1f}.\n")
        report.append(f"Exact match (dist=0): {sum(1 for d in dists if d == 0)}/{len(dists)}.\n")
        report.append(f"Within 3 columns: {sum(1 for d in dists if d <= 3)}/{len(dists)}.\n")
        report.append(f"Within 5 columns: {sum(1 for d in dists if d <= 5)}/{len(dists)}.\n\n")

    if anchor_mean_dist is not None and len(random_dist_distribution) > 0:
        report.append("### Random position control\n\n")
        percentile = np.mean(random_dist_distribution >= anchor_mean_dist) * 100
        report.append(f"Anchor mean pairwise column distance: {anchor_mean_dist:.1f}.\n")
        report.append(f"Random mean (200 trials): {np.mean(random_dist_distribution):.1f} +/- {np.std(random_dist_distribution):.1f}.\n")
        report.append(f"Anchor is tighter than {percentile:.0f}% of random trials.\n\n")
        report.append("![Null distribution](structure_anchor_transfer_null_distribution.png)\n\n")

    if non_gap:
        report.append("### Projection score transfer\n\n")
        report.append(f"{len(non_gap)} non-gap directed transfers (source anchor column -> target protein's residue at that column).\n")
        report.append(f"{gap_count} transfers hit a gap in the target.\n\n")
        report.append("| Transfer metric | Rate |\n")
        report.append("|-----------------|------|\n")
        report.append(f"| Lands in top-1 | {top1_rate:.1%} |\n")
        report.append(f"| Lands in top-3 | {top3_rate:.1%} |\n")
        report.append(f"| Lands in top-5 | {top5_rate:.1%} |\n")
        report.append(f"| Lands in top-10 | {top10_rate:.1%} |\n")
        report.append(f"| Mean projection rank | {np.mean([t['target_proj_rank'] for t in non_gap]):.1f} |\n")
        report.append("\n")

    report.append("## Visualizations\n\n")
    report.append("![Projection heatmap](structure_anchor_transfer_heatmap.png)\n\n")
    report.append("![Mean projection by column](structure_anchor_transfer_projection.png)\n\n")

    # Interpretation
    report.append("## Interpretation\n\n")
    if pairs:
        dists = [p["col_distance"] for p in pairs]
        frac_within_5 = sum(1 for d in dists if d <= 5) / len(dists) if dists else 0
        if frac_within_5 > 0.7 and non_gap and top5_rate > 0.5:
            report.append("Result: STRONG POSITIVE. Anchor positions cluster tightly in structural alignment space, and projection score transfer via structure yields high hit rates. This is evidence that L10H9 detects a structurally conserved landmark.\n\n")
        elif frac_within_5 > 0.3 or (non_gap and top5_rate > 0.3):
            report.append("Result: MODERATE. Some clustering of anchor positions in alignment space, but not as tight as the strong-success criterion. There may be multiple structurally conserved anchor sites per fold.\n\n")
        else:
            report.append("Result: NEGATIVE. Anchor positions do not cluster in alignment space more than random. Anchorhood may depend on fine sequence details rather than fold-level topology.\n\n")

    report_path = REPORT_DIR / "structure_anchor_transfer.md"
    with open(report_path, "w") as f:
        f.writelines(report)
    print(f"  Saved: {report_path}")

    print("\nDone.")


def save_audit_csv(results: list[dict], path: Path):
    """Save per-protein audit results to CSV."""
    fields = [
        "protein", "n_res", "top1_mass", "top3_mass", "eff_keys",
        "keys_50pct", "max_key_mass", "rank_corr", "rank_corr_p",
        "top3_overlap", "cos_sim_d", "anchor_pos", "anchor_aa",
        "is_anchor_like",
    ]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print(f"  Saved: {path}")


if __name__ == "__main__":
    main()
