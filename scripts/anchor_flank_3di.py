#!/usr/bin/env python3
"""Anchor flank analysis using 3Di structural alphabet.

Reuses anchor positions and R_50 radii from anchor_flank_clustering_v2_flanks.csv.
Extracts the same flank window from each protein's 3Di sequence (produced by
foldseek createdb on data/pdb/) and runs:

  1. Pairwise 3Di identity clustering + dendrogram
  2. Sequence logo centered on anchor position (3Di alphabet)
  3. Per-position 3Di letter frequency and information content

3Di sequences are produced by running:
    foldseek/bin/foldseek createdb data/pdb/ data/foldseek/alldb
    foldseek/bin/foldseek lndb data/foldseek/alldb_h data/foldseek/alldb_ss_h
    foldseek/bin/foldseek convert2fasta data/foldseek/alldb_ss data/foldseek/all_3di.fa

Position mapping: for each protein, the PDB structure sequence is aligned to the full
sequence (from full_seq_dict.json) using global pairwise alignment. This maps the
anchor position from full-sequence coordinates to structure (and thus 3Di) coordinates.
Proteins where the alignment fails or the anchor lands in a gap are excluded.

Usage:
    uv run python scripts/anchor_flank_3di.py [--plots-only]

Flags:
    --plots-only   Skip position mapping, load data/foldseek/anchor_3di_flanks.csv
                   and regenerate plots only. Useful for re-running plots without
                   re-parsing PDBs.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import cluster, spatial

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
FOLDSEEK_FA = DATA_DIR / "foldseek" / "all_3di.fa"
AA_FLANKS_CSV = REPORT_DIR / "anchor_flank_clustering_v2_flanks.csv"
OUT_CSV = DATA_DIR / "foldseek" / "anchor_3di_flanks.csv"

# 3Di uses the same 20 single-letter codes as amino acids, but they represent
# structural states (local geometry), not amino acid identity.
# We use neutral colors grouped by the foldseek documentation clustering:
# states {C, D, F, L, N, P, Q, R, S, W} are "surface" states (lighter),
# {A, E, G, H, I, K, M, T, V, Y} are "core" states (darker).
# For the logo we use a simple two-color scheme: core vs surface.
DI_ALPHABET = "ACDEFGHIKLMNPQRSTVWY"  # same letters, structural meaning
DI_TO_IDX = {c: i for i, c in enumerate(DI_ALPHABET)}

# Color scheme: structural states loosely grouped by foldseek's published
# characterization of the 3Di states. Using two hues for readability.
_CORE = set("AEGHIKMTVY")
_SURFACE = set("CDFLN PQRSW")
DI_COLORS = {c: ("#1f77b4" if c in _CORE else "#d62728") for c in DI_ALPHABET}


# ---------------------------------------------------------------------------
# 3Di FASTA loader
# ---------------------------------------------------------------------------

def load_3di_fasta(path: Path) -> dict[str, str]:
    sequences = {}
    with open(path) as f:
        name, seq = None, []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    sequences[name] = "".join(seq)
                name = line[1:].split()[0]
                seq = []
            else:
                seq.append(line)
        if name:
            sequences[name] = "".join(seq)
    return sequences


# ---------------------------------------------------------------------------
# Position mapping via PDB structure
# ---------------------------------------------------------------------------

def get_struct_seq(pdb4: str, chain_id: str, pdb_dir: Path) -> str:
    """Extract amino acid sequence of a PDB chain (residues with complete backbone only)."""
    from Bio import PDB
    pdb_path = pdb_dir / f"{pdb4}.pdb"
    if not pdb_path.exists():
        return ""
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure(pdb4, str(pdb_path))
    for model in structure:
        for ch in model:
            if ch.id == chain_id:
                seq_pdb = ""
                for res in ch:
                    if PDB.is_aa(res, standard=True):
                        try:
                            from Bio.PDB.Polypeptide import index_to_one, three_to_index
                            seq_pdb += index_to_one(three_to_index(res.get_resname()))
                        except Exception:
                            seq_pdb += "X"
                return seq_pdb
    return ""


def build_full_to_struct_map(full_seq: str, struct_seq: str) -> dict[int, int]:
    """Global alignment of full_seq vs struct_seq, returns mapping full_pos -> struct_pos."""
    from Bio.Align import PairwiseAligner
    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.open_gap_score = -5.0
    aligner.extend_gap_score = -0.5
    aln = aligner.align(full_seq, struct_seq)[0]
    coords = aln.coordinates  # shape (2, n_cols)
    mapping = {}
    for k in range(coords.shape[1] - 1):
        f0, f1 = int(coords[0, k]), int(coords[0, k + 1])
        s0, s1 = int(coords[1, k]), int(coords[1, k + 1])
        if f1 - f0 == s1 - s0 > 0:  # aligned block (no gap)
            for df, ds in zip(range(f0, f1), range(s0, s1)):
                mapping[df] = ds
    return mapping


# ---------------------------------------------------------------------------
# Build 3Di flanks
# ---------------------------------------------------------------------------

def build_3di_flanks(aa_flanks_csv: Path, threed: dict[str, str],
                     all_seqs: dict[str, str], pdb_dir: Path) -> list[dict]:
    """For each protein in the AA flanks CSV, extract the corresponding 3Di flank.

    Returns a list of dicts with keys:
        protein, anchor_pos_full, struct_anchor_pos, R_50, flank_start_3di,
        flank_end_3di, offset_to_anchor, di_sequence
    """
    from Bio import PDB
    rows = []
    with open(aa_flanks_csv) as f:
        reader = csv.DictReader(f)
        aa_rows = list(reader)

    pdb_parser_cache = {}  # avoid re-parsing same PDB

    skipped = {"no_pdb": 0, "no_3di": 0, "len_mismatch": 0, "anchor_in_gap": 0}
    for row in aa_rows:
        p = row["protein"]
        pdb4 = p[:4].upper()
        chain_id = p[4].upper()
        anchor_pos = int(row["anchor_pos"])
        R_50 = int(row["R_50"])

        # Find 3Di key
        di_key = None
        for k in [f"{pdb4}_{chain_id}", pdb4]:
            if k in threed:
                di_key = k
                break
        if di_key is None:
            skipped["no_3di"] += 1
            continue

        full_seq = all_seqs.get(p, "")
        di_seq = threed[di_key]

        # Get struct seq for position mapping
        struct_seq = get_struct_seq(pdb4, chain_id, pdb_dir)
        if not struct_seq:
            skipped["no_pdb"] += 1
            continue
        if len(struct_seq) != len(di_seq):
            skipped["len_mismatch"] += 1
            continue

        # Map anchor position
        try:
            mapping = build_full_to_struct_map(full_seq, struct_seq)
        except Exception:
            skipped["anchor_in_gap"] += 1
            continue
        if anchor_pos not in mapping:
            skipped["anchor_in_gap"] += 1
            continue
        struct_anchor = mapping[anchor_pos]

        # Extract 3Di flank
        flank_start = max(0, struct_anchor - R_50)
        flank_end = min(len(di_seq) - 1, struct_anchor + R_50)
        di_flank = di_seq[flank_start: flank_end + 1]
        offset = struct_anchor - flank_start

        rows.append({
            "protein": p,
            "anchor_pos_full": anchor_pos,
            "struct_anchor_pos": struct_anchor,
            "R_50": R_50,
            "flank_start_3di": flank_start,
            "flank_end_3di": flank_end,
            "flank_len": len(di_flank),
            "offset_to_anchor": offset,
            "di_sequence": di_flank,
            "anchor_di_letter": di_seq[struct_anchor],
        })

    print(f"  Built 3Di flanks: {len(rows)} proteins")
    print(f"  Skipped: {skipped}")
    return rows


def save_3di_flanks(flanks: list[dict], out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["protein", "anchor_pos_full", "struct_anchor_pos", "R_50",
              "flank_start_3di", "flank_end_3di", "flank_len",
              "offset_to_anchor", "anchor_di_letter", "di_sequence"]
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(flanks)
    print(f"  Saved: {out_path}")


def load_3di_flanks(csv_path: Path) -> list[dict]:
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "protein": row["protein"],
                "anchor_pos_full": int(row["anchor_pos_full"]),
                "struct_anchor_pos": int(row["struct_anchor_pos"]),
                "R_50": int(row["R_50"]),
                "flank_start_3di": int(row["flank_start_3di"]),
                "flank_end_3di": int(row["flank_end_3di"]),
                "flank_len": int(row["flank_len"]),
                "offset_to_anchor": int(row["offset_to_anchor"]),
                "anchor_di_letter": row["anchor_di_letter"],
                "di_sequence": row["di_sequence"],
            })
    return rows


# ---------------------------------------------------------------------------
# Clustering
# ---------------------------------------------------------------------------

def pairwise_3di_identity(flanks: list[dict]) -> np.ndarray:
    """Pairwise 3Di identity, center-aligned on anchor position."""
    n = len(flanks)
    matrix = np.eye(n)
    for i in range(n):
        for j in range(i + 1, n):
            a, b = flanks[i], flanks[j]
            off_a, off_b = a["offset_to_anchor"], b["offset_to_anchor"]
            seq_a, seq_b = a["di_sequence"], b["di_sequence"]
            left = max(-off_a, -off_b)
            right = min(len(seq_a) - off_a - 1, len(seq_b) - off_b - 1)
            if left > right:
                continue
            matches = sum(1 for rp in range(left, right + 1)
                          if seq_a[off_a + rp] == seq_b[off_b + rp])
            total = right - left + 1
            ident = matches / max(total, 1)
            matrix[i, j] = ident
            matrix[j, i] = ident
    return matrix


# ---------------------------------------------------------------------------
# Motif analysis
# ---------------------------------------------------------------------------

def build_centered_matrix(flanks: list[dict], window: int) -> tuple[np.ndarray, np.ndarray]:
    """Count matrix: positions [-window, +window] x 20 3Di letters."""
    n_pos = 2 * window + 1
    counts = np.zeros((n_pos, 20), dtype=float)
    n_seqs = np.zeros(n_pos, dtype=int)
    for f in flanks:
        seq = f["di_sequence"]
        off = f["offset_to_anchor"]
        for rel_pos in range(-window, window + 1):
            seq_idx = off + rel_pos
            if 0 <= seq_idx < len(seq):
                c = seq[seq_idx]
                if c in DI_TO_IDX:
                    counts[rel_pos + window, DI_TO_IDX[c]] += 1
                    n_seqs[rel_pos + window] += 1
    return counts, n_seqs


def compute_information_content(counts: np.ndarray, n_seqs: np.ndarray) -> np.ndarray:
    n_pos = counts.shape[0]
    ic = np.zeros(n_pos)
    max_entropy = math.log2(20)
    for i in range(n_pos):
        if n_seqs[i] == 0:
            continue
        freq = counts[i] / n_seqs[i]
        freq = freq[freq > 0]
        entropy = -np.sum(freq * np.log2(freq))
        ic[i] = max_entropy - entropy
    return ic


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def _draw_letter(ax, letter: str, x: float, y: float, width: float, height: float, color: str):
    from matplotlib.transforms import Affine2D
    from matplotlib.textpath import TextPath
    from matplotlib.patches import PathPatch
    tp = TextPath((0, 0), letter, size=1, prop={"weight": "bold", "family": "monospace"})
    bbox = tp.get_extents()
    if bbox.width == 0 or bbox.height == 0:
        return
    transform = Affine2D()
    transform.translate(-bbox.x0, -bbox.y0)
    transform.scale(width / bbox.width, height / bbox.height)
    transform.translate(x - width / 2, y)
    tp_transformed = tp.transformed(transform)
    patch = PathPatch(tp_transformed, facecolor=color, edgecolor="none", lw=0)
    ax.add_patch(patch)


def plot_sequence_logo(counts: np.ndarray, n_seqs: np.ndarray, ic: np.ndarray,
                       window: int, title: str, out_path: Path, n_total: int):
    n_pos = 2 * window + 1
    positions = list(range(-window, window + 1))
    fig, (ax_logo, ax_ic) = plt.subplots(2, 1, figsize=(max(14, window * 0.5), 5.5),
                                          gridspec_kw={"height_ratios": [3, 1]}, sharex=True)
    letter_width = 0.8
    for i in range(n_pos):
        if n_seqs[i] == 0:
            continue
        freq = counts[i] / n_seqs[i]
        heights = ic[i] * freq
        order = np.argsort(heights)
        y_offset = 0.0
        for j in order:
            h = heights[j]
            if h < 0.003:
                continue
            c = DI_ALPHABET[j]
            color = DI_COLORS.get(c, "#888888")
            _draw_letter(ax_logo, c, positions[i], y_offset, letter_width, h, color)
            y_offset += h

    y_max = min(4.5, ic.max() * 1.3) if ic.max() > 0 else 1.0
    ax_logo.set_xlim(-window - 0.5, window + 0.5)
    ax_logo.set_ylim(0, y_max)
    ax_logo.set_ylabel("Information\ncontent (bits)")
    ax_logo.axvline(0, color="#D64550", ls="--", lw=1, alpha=0.7)
    ax_logo.set_title(f"{title} (n={n_total})\nBlue=core 3Di states, Red=surface 3Di states")
    ax_logo.spines["top"].set_visible(False)
    ax_logo.spines["right"].set_visible(False)

    colors = ["#D64550" if p == 0 else "#5B7FA3" for p in positions]
    ax_ic.bar(positions, ic, color=colors, width=0.8, edgecolor="none")
    ax_ic.set_xlabel("Position relative to anchor")
    ax_ic.set_ylabel("IC (bits)")
    ax_ic.axhline(0, color="gray", lw=0.5)
    ax_ic.spines["top"].set_visible(False)
    ax_ic.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_sim_matrix(matrix: np.ndarray, labels: list[str], title: str, path: Path,
                    cmap: str = "RdYlBu_r", vmin: float = 0.0, vmax: float = 1.0):
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
    cluster.hierarchy.dendrogram(linkage_mat, labels=labels, ax=ax,
                                 leaf_rotation=90, leaf_font_size=3)
    ax.set_title(title, fontsize=10)
    ax.set_ylabel("Distance")
    plt.tight_layout()
    fig.savefig(path, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path}")


def plot_top_letter_per_position(counts: np.ndarray, n_seqs: np.ndarray,
                                  window: int, title: str, out_path: Path):
    positions = list(range(-window, window + 1))
    n_pos = 2 * window + 1
    top_letter, top_freq = [], []
    for i in range(n_pos):
        if n_seqs[i] == 0:
            top_letter.append("-")
            top_freq.append(0.0)
            continue
        freq = counts[i] / n_seqs[i]
        idx = int(np.argmax(freq))
        top_letter.append(DI_ALPHABET[idx])
        top_freq.append(float(freq[idx]))

    fig, ax = plt.subplots(figsize=(max(12, window * 0.4), 4))
    ax.axhline(0.05, color="gray", ls=":", lw=0.7, alpha=0.5, label="Random (5%)")
    colors = [DI_COLORS.get(c, "#888888") for c in top_letter]
    ax.bar(positions, top_freq, color=colors, width=0.8, edgecolor="none", alpha=0.8)
    for pos, letter, freq in zip(positions, top_letter, top_freq):
        if freq > 0.1:
            ax.text(pos, freq + 0.01, letter, ha="center", va="bottom",
                    fontsize=6, fontweight="bold", color=DI_COLORS.get(letter, "#888888"))
    ax.axvline(0, color="#D64550", ls="--", lw=1.5, alpha=0.7)
    ax.set_xlabel("Position relative to anchor")
    ax.set_ylabel("Frequency of most common 3Di letter")
    ax.set_title(title)
    ax.set_xlim(-window - 0.5, window + 0.5)
    ax.legend(fontsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_plots(flanks: list[dict]):
    window = 25
    labels = [f["protein"] for f in flanks]
    n = len(flanks)

    print(f"\n{'='*60}")
    print("Pairwise 3Di identity clustering")
    print(f"{'='*60}")
    print(f"  Computing {n}x{n} identity matrix...")
    id_matrix = pairwise_3di_identity(flanks)
    print(f"  Mean off-diagonal identity: {id_matrix[np.triu_indices(n, k=1)].mean():.3f}")
    print(f"  Max off-diagonal identity: {id_matrix[np.triu_indices(n, k=1)].max():.3f}")

    dist_matrix = 1.0 - id_matrix
    condensed = spatial.distance.squareform(dist_matrix)
    linkage_mat = cluster.hierarchy.linkage(condensed, method="average")

    plot_sim_matrix(id_matrix, labels, f"3Di identity (n={n}, center-aligned on anchor)",
                    REPORT_DIR / "anchor_3di_cluster_identity.png", vmin=0.0, vmax=1.0)
    plot_dendro(linkage_mat, labels, f"3Di identity dendrogram (n={n})",
                REPORT_DIR / "anchor_3di_cluster_dendro.png")

    print(f"\n{'='*60}")
    print("Sequence logo (3Di alphabet)")
    print(f"{'='*60}")
    counts, n_seqs = build_centered_matrix(flanks, window)
    ic = compute_information_content(counts, n_seqs)

    print(f"  n_seqs at anchor (pos 0): {n_seqs[window]}")
    print(f"  IC at anchor: {ic[window]:.3f} bits")
    print(f"  Max IC: {ic.max():.3f} bits at offset {np.argmax(ic) - window}")
    print(f"  Mean IC: {ic.mean():.3f} bits")
    print(f"  Positions with IC > 0.15 bits:")
    for i in range(len(ic)):
        if ic[i] > 0.15:
            pos = i - window
            freq = counts[i] / max(n_seqs[i], 1)
            top_idx = int(np.argmax(freq))
            print(f"    Offset {pos:+3d}: IC={ic[i]:.3f}, top letter={DI_ALPHABET[top_idx]} ({freq[top_idx]:.1%}), n={n_seqs[i]}")

    # Distribution of anchor 3Di letters
    anchor_letters = Counter(f["anchor_di_letter"] for f in flanks)
    print(f"\n  3Di letter at anchor position (top 5):")
    for letter, cnt in anchor_letters.most_common(5):
        print(f"    {letter}: {cnt} ({cnt/n:.1%})")

    plot_sequence_logo(counts, n_seqs, ic, window,
                       "Anchor flank 3Di logo (all proteins)",
                       REPORT_DIR / "anchor_3di_logo_all.png", n)
    plot_top_letter_per_position(counts, n_seqs, window,
                                  "Most common 3Di letter at each position",
                                  REPORT_DIR / "anchor_3di_top_letter.png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--plots-only", action="store_true",
                        help="Skip PDB parsing, load from anchor_3di_flanks.csv and regenerate plots")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if args.plots_only:
        print(f"Loading 3Di flanks from {OUT_CSV}...")
        flanks = load_3di_flanks(OUT_CSV)
        print(f"  {len(flanks)} flanks loaded")
        run_plots(flanks)
        return

    print("Loading 3Di sequences from foldseek FASTA...")
    threed = load_3di_fasta(FOLDSEEK_FA)
    print(f"  {len(threed)} 3Di sequences loaded")

    print("Loading full amino acid sequences...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    print("Building 3Di flanks (parsing PDB structures for position mapping)...")
    flanks = build_3di_flanks(AA_FLANKS_CSV, threed, all_seqs, DATA_DIR / "pdb")

    print(f"\nSaving 3Di flanks to {OUT_CSV}...")
    save_3di_flanks(flanks, OUT_CSV)

    run_plots(flanks)


if __name__ == "__main__":
    main()
