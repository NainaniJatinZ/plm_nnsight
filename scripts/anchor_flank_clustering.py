#!/usr/bin/env python3
"""Cluster minimal anchor flanks across proteins.

For each of the 50 proteins from the local-flank-v1 experiment, extracts the
minimal flank subsequence that triggers anchor projection recovery. Then:

1. Pairwise sequence identity of minimal flanks (Blosum62-scored local alignment
   and simple percent identity after center-aligning on the anchor).
2. ESM2 embedding similarity: run each flank through ESM2, extract layer-10
   LayerNorm activations, take the mean embedding, compute pairwise cosine sim.
   Cluster with hierarchical clustering + PCA.

Usage:
    uv run python scripts/anchor_flank_clustering.py --device cuda
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
from scipy import spatial, cluster, stats as sp_stats

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

TARGET_LAYER = 10
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280


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


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_thresholds() -> dict:
    """Load per-protein threshold radii from flank v1 experiment. Returns {protein: {metric: {R_25, R_50, R_80, R_90}}}."""
    path = REPORT_DIR / "anchor_local_flank_v1_thresholds.csv"
    thresholds = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["protein"]
            metric = row["metric"]
            if pid not in thresholds:
                thresholds[pid] = {"n_res": int(row["n_res"])}
            thresholds[pid][metric] = {
                "R_25": row["R_25"], "R_50": row["R_50"],
                "R_80": row["R_80"], "R_90": row["R_90"],
            }
    return thresholds


def load_per_protein_data() -> dict:
    """Load per-protein per-radius data from flank v1. Returns {protein: {anchor_pos, n_res, radii: [{radius, alpha_norm, ...}]}}."""
    path = REPORT_DIR / "anchor_local_flank_v1_per_protein.csv"
    data = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["protein"]
            if pid not in data:
                data[pid] = {
                    "anchor_pos": int(row["anchor_pos"]),
                    "n_res": int(row["n_res"]),
                    "radii": [],
                }
            data[pid]["radii"].append({
                "radius": row["radius"],
                "radius_int": int(row["radius_int"]) if row["radius_int"] != "full" else 9999,
                "alpha_norm": float(row["alpha_norm"]),
                "score_norm": float(row["score_norm"]),
                "attn_norm": float(row["attn_norm"]),
            })
    return data


def get_minimal_radius(thresholds: dict, pid: str, threshold_level: str = "R_50") -> int:
    """Get the minimal flank radius for a protein using the alpha (projection) metric at the given threshold level.

    Returns the radius as an integer. 'full' is converted to the protein's n_res.
    """
    t = thresholds[pid]
    r_str = t["alpha"][threshold_level]
    if r_str == "full":
        return t["n_res"]
    return int(r_str)


# ---------------------------------------------------------------------------
# Analysis 1: Sequence identity of minimal flanks
# ---------------------------------------------------------------------------

def extract_flank_sequence(sequence: str, anchor_pos: int, radius: int) -> str:
    """Extract the subsequence [anchor - radius, anchor + radius] (clamped to bounds)."""
    start = max(0, anchor_pos - radius)
    end = min(len(sequence), anchor_pos + radius + 1)
    return sequence[start:end]


def pairwise_sequence_identity_center_aligned(flanks: dict[str, dict]) -> dict:
    """Compute pairwise sequence identity of flanks, center-aligned on the anchor position.

    For each pair, aligns the anchor residues and counts matches in the overlapping region.
    Returns {(pid_a, pid_b): identity}.
    """
    pids = list(flanks.keys())
    identities = {}
    for i in range(len(pids)):
        for j in range(i + 1, len(pids)):
            a = flanks[pids[i]]
            b = flanks[pids[j]]
            # Center-align on anchor: the anchor is at position radius (or clamped)
            # a["offset_to_anchor"] = anchor_pos - start
            off_a = a["offset_to_anchor"]
            off_b = b["offset_to_anchor"]
            seq_a = a["sequence"]
            seq_b = b["sequence"]

            # Align: find the overlapping region when anchor positions are aligned
            # Position in a relative to anchor: pos - off_a
            # Position in b relative to anchor: pos - off_b
            # Overlap in anchor-relative coords: max of left extents, min of right extents
            left_a = -off_a  # leftmost position in a (relative to anchor)
            right_a = len(seq_a) - off_a - 1
            left_b = -off_b
            right_b = len(seq_b) - off_b - 1

            overlap_left = max(left_a, left_b)
            overlap_right = min(right_a, right_b)

            if overlap_left > overlap_right:
                identities[(pids[i], pids[j])] = 0.0
                continue

            matches = 0
            total = 0
            for rel_pos in range(overlap_left, overlap_right + 1):
                aa_a = seq_a[off_a + rel_pos]
                aa_b = seq_b[off_b + rel_pos]
                total += 1
                if aa_a == aa_b:
                    matches += 1

            identities[(pids[i], pids[j])] = matches / max(total, 1)
    return identities


def blosum62_score_pair(seq_a: str, seq_b: str, off_a: int, off_b: int) -> float:
    """Compute mean BLOSUM62 score per aligned position, center-aligned on anchor."""
    # Minimal BLOSUM62 matrix for the 20 standard amino acids
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

    left_a = -off_a
    right_a = len(seq_a) - off_a - 1
    left_b = -off_b
    right_b = len(seq_b) - off_b - 1
    overlap_left = max(left_a, left_b)
    overlap_right = min(right_a, right_b)

    if overlap_left > overlap_right:
        return 0.0

    total_score = 0.0
    count = 0
    for rel_pos in range(overlap_left, overlap_right + 1):
        aa_a = seq_a[off_a + rel_pos]
        aa_b = seq_b[off_b + rel_pos]
        if aa_a in BLOSUM62 and aa_b in BLOSUM62.get(aa_a, {}):
            total_score += BLOSUM62[aa_a][aa_b]
            count += 1

    return total_score / max(count, 1)


# ---------------------------------------------------------------------------
# Analysis 2: ESM2 embedding similarity of flanks
# ---------------------------------------------------------------------------

@torch.no_grad()
def get_flank_embedding(model, tokenizer, sequence: str, device: str) -> np.ndarray:
    """Run a sequence through ESM2 and return the mean layer-10 LayerNorm activation (1280-dim)."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0, 1:-1]  # strip BOS/EOS
    return x_ln.mean(dim=0).numpy()


@torch.no_grad()
def get_anchor_position_embedding(model, tokenizer, sequence: str, anchor_offset: int, device: str) -> np.ndarray:
    """Run a sequence through ESM2 and return the layer-10 LN activation at the anchor position (1280-dim)."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    # anchor_offset is relative to the flank start; +1 for BOS token
    return x_ln[anchor_offset + 1].numpy()


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_similarity_matrix(matrix, labels, title, out_path, cmap="RdYlBu_r", vmin=None, vmax=None):
    """Plot a labeled similarity matrix as a heatmap."""
    n = len(labels)
    fig, ax = plt.subplots(figsize=(max(8, n * 0.22), max(7, n * 0.2)))
    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax, shrink=0.8)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontsize=5, rotation=90)
    ax.set_yticklabels(labels, fontsize=5)
    ax.set_title(title)
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_dendrogram_with_annotations(linkage_matrix, labels, annotations, title, out_path):
    """Plot a dendrogram with colored leaf labels."""
    fig, ax = plt.subplots(figsize=(max(10, len(labels) * 0.25), 5))
    dendro = cluster.hierarchy.dendrogram(
        linkage_matrix, labels=labels, ax=ax, leaf_rotation=90, leaf_font_size=6,
    )
    ax.set_title(title)
    ax.set_ylabel("Distance")
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_pca_embeddings(embeddings, labels, radii, title, out_path):
    """PCA of embeddings, scatter colored by minimal radius."""
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    coords = pca.fit_transform(embeddings)

    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(coords[:, 0], coords[:, 1], c=radii, cmap="viridis", s=40, edgecolors="white", linewidths=0.5)
    plt.colorbar(sc, ax=ax, label="Minimal flank radius (R_50)")

    for i, label in enumerate(labels):
        ax.annotate(label, (coords[i, 0], coords[i, 1]), fontsize=5, alpha=0.7,
                    xytext=(3, 3), textcoords="offset points")

    ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)")
    ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)")
    ax.set_title(title)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--threshold", default="R_50", choices=["R_25", "R_50", "R_80", "R_90"],
                        help="Which recovery threshold to use for defining the minimal flank")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Load data
    print("Loading flank v1 data...")
    thresholds = load_thresholds()
    per_protein = load_per_protein_data()

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    # Get the 50 proteins from the flank experiment
    proteins = sorted(per_protein.keys())
    print(f"  {len(proteins)} proteins from flank v1 experiment")

    # Extract minimal flanks
    print(f"\nExtracting minimal flanks (threshold: {args.threshold} of projection recovery)...")
    flanks = {}
    for pid in proteins:
        if pid not in all_seqs:
            print(f"  WARNING: {pid} not in full_seq_dict.json, skipping")
            continue
        seq = all_seqs[pid]
        anchor_pos = per_protein[pid]["anchor_pos"]
        radius = get_minimal_radius(thresholds, pid, args.threshold)

        start = max(0, anchor_pos - radius)
        end = min(len(seq), anchor_pos + radius + 1)
        flank_seq = seq[start:end]
        offset_to_anchor = anchor_pos - start

        flanks[pid] = {
            "sequence": flank_seq,
            "full_sequence": seq,
            "anchor_pos": anchor_pos,
            "radius": radius,
            "start": start,
            "end": end,
            "offset_to_anchor": offset_to_anchor,
            "n_res_full": len(seq),
            "n_res_flank": len(flank_seq),
            "anchor_aa": seq[anchor_pos],
        }

    pids = sorted(flanks.keys())
    print(f"  Extracted flanks for {len(pids)} proteins")
    print(f"\n  Radius distribution:")
    radii = [flanks[p]["radius"] for p in pids]
    for r in sorted(set(radii)):
        count = sum(1 for x in radii if x == r)
        print(f"    R={r}: {count} proteins")

    print(f"\n  Flank length distribution:")
    flank_lens = [flanks[p]["n_res_flank"] for p in pids]
    print(f"    Min: {min(flank_lens)}, Max: {max(flank_lens)}, Mean: {np.mean(flank_lens):.0f}, Median: {np.median(flank_lens):.0f}")

    # Print flank sequences centered on anchor
    print(f"\n  Flank sequences (anchor residue marked with []):")
    for pid in pids:
        f = flanks[pid]
        off = f["offset_to_anchor"]
        seq = f["sequence"]
        # Show 10 residues on each side of anchor, or the full flank if shorter
        display_left = max(0, off - 10)
        display_right = min(len(seq), off + 11)
        left_part = seq[display_left:off]
        anchor_part = seq[off]
        right_part = seq[off+1:display_right]
        dots_l = "..." if display_left > 0 else "   "
        dots_r = "..." if display_right < len(seq) else ""
        print(f"    {pid:<8} R={f['radius']:>3} len={f['n_res_flank']:>3}  {dots_l}{left_part}[{anchor_part}]{right_part}{dots_r}")

    # ===================================================================
    # Analysis 1: Pairwise sequence identity of flanks
    # ===================================================================
    print("\n" + "=" * 60)
    print("Analysis 1: Pairwise sequence identity of minimal flanks")
    print("=" * 60)

    print("\nComputing pairwise identity (center-aligned on anchor)...")
    identities = pairwise_sequence_identity_center_aligned(flanks)

    # Build identity matrix
    n = len(pids)
    id_matrix = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            ident = identities.get((pids[i], pids[j]), 0.0)
            id_matrix[i, j] = ident
            id_matrix[j, i] = ident

    print(f"\n  Mean pairwise identity: {id_matrix[np.triu_indices(n, k=1)].mean():.3f}")
    print(f"  Max: {id_matrix[np.triu_indices(n, k=1)].max():.3f}")
    print(f"  Min: {id_matrix[np.triu_indices(n, k=1)].min():.3f}")

    # Compute BLOSUM62 scores
    print("\nComputing pairwise BLOSUM62 scores (center-aligned on anchor)...")
    blosum_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                # Self-score
                f = flanks[pids[i]]
                blosum_matrix[i, j] = blosum62_score_pair(
                    f["sequence"], f["sequence"], f["offset_to_anchor"], f["offset_to_anchor"])
            elif i < j:
                fi, fj = flanks[pids[i]], flanks[pids[j]]
                score = blosum62_score_pair(
                    fi["sequence"], fj["sequence"], fi["offset_to_anchor"], fj["offset_to_anchor"])
                blosum_matrix[i, j] = score
                blosum_matrix[j, i] = score

    print(f"  Mean pairwise BLOSUM62 score: {blosum_matrix[np.triu_indices(n, k=1)].mean():.2f}")

    # Hierarchical clustering on (1 - identity) distance
    id_dist = 1.0 - id_matrix[np.triu_indices(n, k=1)]
    id_linkage = cluster.hierarchy.linkage(id_dist, method="average")

    # ===================================================================
    # Analysis 2: ESM2 embedding similarity
    # ===================================================================
    print("\n" + "=" * 60)
    print("Analysis 2: ESM2 embedding similarity of minimal flanks")
    print("=" * 60)

    print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    # Get mean flank embeddings and anchor-position embeddings
    print(f"\nComputing embeddings for {len(pids)} flanks...")
    mean_embeddings = []
    anchor_embeddings = []
    for i, pid in enumerate(pids):
        f = flanks[pid]
        emb_mean = get_flank_embedding(model, tokenizer, f["sequence"], args.device)
        emb_anchor = get_anchor_position_embedding(model, tokenizer, f["sequence"], f["offset_to_anchor"], args.device)
        mean_embeddings.append(emb_mean)
        anchor_embeddings.append(emb_anchor)
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{len(pids)} done")

    mean_embeddings = np.array(mean_embeddings)  # (n, 1280)
    anchor_embeddings = np.array(anchor_embeddings)  # (n, 1280)

    # Pairwise cosine similarity
    mean_cos_sim = 1.0 - spatial.distance.squareform(
        spatial.distance.pdist(mean_embeddings, metric="cosine"))
    anchor_cos_sim = 1.0 - spatial.distance.squareform(
        spatial.distance.pdist(anchor_embeddings, metric="cosine"))

    print(f"\n  Mean embedding cosine similarity (off-diagonal): {mean_cos_sim[np.triu_indices(n, k=1)].mean():.3f}")
    print(f"  Anchor-position embedding cosine similarity (off-diagonal): {anchor_cos_sim[np.triu_indices(n, k=1)].mean():.3f}")

    # Hierarchical clustering on cosine distance of mean embeddings
    emb_dist = spatial.distance.pdist(mean_embeddings, metric="cosine")
    emb_linkage = cluster.hierarchy.linkage(emb_dist, method="average")

    anchor_emb_dist = spatial.distance.pdist(anchor_embeddings, metric="cosine")
    anchor_emb_linkage = cluster.hierarchy.linkage(anchor_emb_dist, method="average")

    # ===================================================================
    # Cross-analysis: do sequence-similar flanks also have similar embeddings?
    # ===================================================================
    print("\n" + "=" * 60)
    print("Cross-analysis: sequence identity vs embedding similarity")
    print("=" * 60)

    id_flat = id_matrix[np.triu_indices(n, k=1)]
    mean_cos_flat = mean_cos_sim[np.triu_indices(n, k=1)]
    anchor_cos_flat = anchor_cos_sim[np.triu_indices(n, k=1)]
    blosum_flat = blosum_matrix[np.triu_indices(n, k=1)]

    rho_id_mean, p_id_mean = sp_stats.spearmanr(id_flat, mean_cos_flat)
    rho_id_anchor, p_id_anchor = sp_stats.spearmanr(id_flat, anchor_cos_flat)
    rho_blosum_mean, p_blosum_mean = sp_stats.spearmanr(blosum_flat, mean_cos_flat)

    print(f"  Spearman(seq identity, mean embedding cosine): rho={rho_id_mean:.3f}, p={p_id_mean:.2e}")
    print(f"  Spearman(seq identity, anchor embedding cosine): rho={rho_id_anchor:.3f}, p={p_id_anchor:.2e}")
    print(f"  Spearman(BLOSUM62, mean embedding cosine): rho={rho_blosum_mean:.3f}, p={p_blosum_mean:.2e}")

    # Does flank radius correlate with protein length?
    lengths = [flanks[p]["n_res_full"] for p in pids]
    rho_len_rad, p_len_rad = sp_stats.spearmanr(lengths, radii)
    print(f"\n  Spearman(protein length, minimal radius): rho={rho_len_rad:.3f}, p={p_len_rad:.2e}")

    # ===================================================================
    # Amino acid composition at anchor position
    # ===================================================================
    print("\n" + "=" * 60)
    print("Anchor residue composition")
    print("=" * 60)
    anchor_aas = [flanks[p]["anchor_aa"] for p in pids]
    aa_counts = {}
    for aa in anchor_aas:
        aa_counts[aa] = aa_counts.get(aa, 0) + 1
    for aa, count in sorted(aa_counts.items(), key=lambda x: -x[1]):
        print(f"  {aa}: {count} ({count/len(anchor_aas):.0%})")

    # ===================================================================
    # Plots
    # ===================================================================
    print("\n" + "=" * 60)
    print("Generating plots")
    print("=" * 60)

    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "figure.dpi": 200,
    })

    short_labels = [f"{p[:5]} R={flanks[p]['radius']}" for p in pids]

    # Reorder all matrices by embedding dendrogram for visual consistency
    emb_order = cluster.hierarchy.leaves_list(emb_linkage)
    ordered_labels = [short_labels[i] for i in emb_order]
    ordered_pids = [pids[i] for i in emb_order]

    # Sequence identity matrix (ordered by embedding clustering)
    id_reordered = id_matrix[np.ix_(emb_order, emb_order)]
    plot_similarity_matrix(id_reordered, ordered_labels,
                           "Pairwise sequence identity of minimal anchor flanks (center-aligned)",
                           REPORT_DIR / "anchor_flank_cluster_seq_identity.png",
                           cmap="YlOrRd", vmin=0, vmax=0.5)

    # BLOSUM62 matrix (ordered by embedding clustering)
    blosum_reordered = blosum_matrix[np.ix_(emb_order, emb_order)]
    plot_similarity_matrix(blosum_reordered, ordered_labels,
                           "Pairwise BLOSUM62 score of minimal anchor flanks",
                           REPORT_DIR / "anchor_flank_cluster_blosum62.png",
                           cmap="RdYlBu_r")

    # Embedding cosine similarity matrix
    mean_cos_reordered = mean_cos_sim[np.ix_(emb_order, emb_order)]
    plot_similarity_matrix(mean_cos_reordered, ordered_labels,
                           "Mean flank embedding cosine similarity (L10 LayerNorm)",
                           REPORT_DIR / "anchor_flank_cluster_emb_cosine.png",
                           cmap="RdYlBu_r", vmin=0.7, vmax=1.0)

    # Anchor-position embedding cosine similarity
    anchor_cos_reordered = anchor_cos_sim[np.ix_(emb_order, emb_order)]
    plot_similarity_matrix(anchor_cos_reordered, ordered_labels,
                           "Anchor-position embedding cosine similarity",
                           REPORT_DIR / "anchor_flank_cluster_anchor_emb_cosine.png",
                           cmap="RdYlBu_r", vmin=0.7, vmax=1.0)

    # Dendrograms
    plot_dendrogram_with_annotations(id_linkage, short_labels, radii,
                                     "Hierarchical clustering by flank sequence identity",
                                     REPORT_DIR / "anchor_flank_cluster_seq_dendro.png")

    plot_dendrogram_with_annotations(emb_linkage, short_labels, radii,
                                     "Hierarchical clustering by mean flank embedding (cosine)",
                                     REPORT_DIR / "anchor_flank_cluster_emb_dendro.png")

    plot_dendrogram_with_annotations(anchor_emb_linkage, short_labels, radii,
                                     "Hierarchical clustering by anchor-position embedding (cosine)",
                                     REPORT_DIR / "anchor_flank_cluster_anchor_emb_dendro.png")

    # PCA of mean embeddings
    plot_pca_embeddings(mean_embeddings, [p[:5] for p in pids], radii,
                        "PCA of mean flank embeddings (colored by minimal radius)",
                        REPORT_DIR / "anchor_flank_cluster_emb_pca.png")

    # PCA of anchor embeddings
    plot_pca_embeddings(anchor_embeddings, [p[:5] for p in pids], radii,
                        "PCA of anchor-position embeddings (colored by minimal radius)",
                        REPORT_DIR / "anchor_flank_cluster_anchor_emb_pca.png")

    # Cross-analysis scatter: sequence identity vs embedding similarity
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

    ax1.scatter(id_flat, mean_cos_flat, s=3, alpha=0.3, color="#5B7FA3")
    ax1.set_xlabel("Flank sequence identity")
    ax1.set_ylabel("Mean embedding cosine similarity")
    ax1.set_title(f"Seq identity vs embedding sim\n(Spearman rho={rho_id_mean:.3f})")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ax2.scatter(id_flat, anchor_cos_flat, s=3, alpha=0.3, color="#D64550")
    ax2.set_xlabel("Flank sequence identity")
    ax2.set_ylabel("Anchor-position embedding cosine sim")
    ax2.set_title(f"Seq identity vs anchor embedding sim\n(Spearman rho={rho_id_anchor:.3f})")
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_flank_cluster_cross_analysis.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {REPORT_DIR / 'anchor_flank_cluster_cross_analysis.png'}")

    # ===================================================================
    # Save report
    # ===================================================================
    print("\nWriting report...")
    report = []
    report.append("# Anchor Flank Clustering Analysis\n\n")
    report.append(f"Proteins: {len(pids)} (from local-flank-v1 experiment, top 50 by anchor confidence).\n")
    report.append(f"Minimal flank definition: {args.threshold} recovery threshold on projection (alpha) metric.\n\n")

    report.append("## Minimal flank radius distribution\n\n")
    for r in sorted(set(radii)):
        count = sum(1 for x in radii if x == r)
        report.append(f"- R={r}: {count} proteins\n")
    report.append(f"\nFlank length: min={min(flank_lens)}, max={max(flank_lens)}, mean={np.mean(flank_lens):.0f}, median={np.median(flank_lens):.0f}.\n")
    report.append(f"Correlation between protein length and minimal radius: Spearman rho={rho_len_rad:.3f} (p={p_len_rad:.2e}).\n\n")

    report.append("## Anchor residue composition\n\n")
    for aa, count in sorted(aa_counts.items(), key=lambda x: -x[1]):
        report.append(f"- {aa}: {count} ({count/len(anchor_aas):.0%})\n")
    report.append("\n")

    report.append("## Analysis 1: Pairwise sequence identity of minimal flanks\n\n")
    report.append(f"Center-aligned on anchor position, counting matches in overlapping region.\n")
    report.append(f"Mean pairwise identity: {id_matrix[np.triu_indices(n, k=1)].mean():.3f}.\n")
    report.append(f"Max: {id_matrix[np.triu_indices(n, k=1)].max():.3f}.\n")
    report.append(f"Min: {id_matrix[np.triu_indices(n, k=1)].min():.3f}.\n\n")
    report.append(f"Mean pairwise BLOSUM62 score: {blosum_matrix[np.triu_indices(n, k=1)].mean():.2f}.\n\n")

    report.append("![Sequence identity matrix](anchor_flank_cluster_seq_identity.png)\n\n")
    report.append("![BLOSUM62 matrix](anchor_flank_cluster_blosum62.png)\n\n")
    report.append("![Sequence identity dendrogram](anchor_flank_cluster_seq_dendro.png)\n\n")

    report.append("## Analysis 2: ESM2 embedding similarity\n\n")
    report.append(f"Layer-10 LayerNorm activations from ESM2-650M.\n")
    report.append(f"Two embedding types: mean over all flank positions, and anchor position only.\n\n")
    report.append(f"Mean flank embedding cosine similarity (off-diagonal): {mean_cos_sim[np.triu_indices(n, k=1)].mean():.3f}.\n")
    report.append(f"Anchor-position embedding cosine similarity (off-diagonal): {anchor_cos_sim[np.triu_indices(n, k=1)].mean():.3f}.\n\n")

    report.append("![Mean embedding cosine similarity](anchor_flank_cluster_emb_cosine.png)\n\n")
    report.append("![Anchor embedding cosine similarity](anchor_flank_cluster_anchor_emb_cosine.png)\n\n")
    report.append("![Mean embedding dendrogram](anchor_flank_cluster_emb_dendro.png)\n\n")
    report.append("![Anchor embedding dendrogram](anchor_flank_cluster_anchor_emb_dendro.png)\n\n")
    report.append("![Mean embedding PCA](anchor_flank_cluster_emb_pca.png)\n\n")
    report.append("![Anchor embedding PCA](anchor_flank_cluster_anchor_emb_pca.png)\n\n")

    report.append("## Cross-analysis\n\n")
    report.append(f"Spearman(seq identity, mean embedding cosine): rho={rho_id_mean:.3f} (p={p_id_mean:.2e}).\n")
    report.append(f"Spearman(seq identity, anchor embedding cosine): rho={rho_id_anchor:.3f} (p={p_id_anchor:.2e}).\n")
    report.append(f"Spearman(BLOSUM62, mean embedding cosine): rho={rho_blosum_mean:.3f} (p={p_blosum_mean:.2e}).\n\n")

    report.append("![Cross-analysis](anchor_flank_cluster_cross_analysis.png)\n\n")

    report_path = REPORT_DIR / "anchor_flank_clustering.md"
    with open(report_path, "w") as f:
        f.writelines(report)
    print(f"  Saved: {report_path}")

    # Save CSV of flank data
    csv_path = REPORT_DIR / "anchor_flank_clustering_flanks.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["protein", "n_res_full", "anchor_pos", "anchor_aa", "radius", "flank_start", "flank_end", "flank_len", "flank_sequence"])
        for pid in pids:
            fl = flanks[pid]
            writer.writerow([pid, fl["n_res_full"], fl["anchor_pos"], fl["anchor_aa"],
                             fl["radius"], fl["start"], fl["end"], fl["n_res_flank"], fl["sequence"]])
    print(f"  Saved: {csv_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
