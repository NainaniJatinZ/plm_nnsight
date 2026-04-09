#!/usr/bin/env python3
"""Anchor flank motif analysis.

Center-aligns all 250 minimal flanks on the anchor position and asks:
are there conserved amino acids at fixed offsets from the anchor?

1. Position-weight matrix (PWM) and sequence logo centered on anchor (pos 0).
2. Per-position amino acid frequency and conservation score (information content).
3. Stratified logos: hydrophobic anchors (V/I/L/F/M/A/W) vs polar/other anchors.
4. Per-position enrichment of amino acid properties (hydrophobic, charged, small, etc.).

No multiple sequence alignment — the anchor position IS the alignment anchor.

Usage:
    uv run python scripts/anchor_flank_motif.py
"""

from __future__ import annotations

import csv
import math
import sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"

STANDARD_AA = "ACDEFGHIKLMNPQRSTVWY"
AA_TO_IDX = {aa: i for i, aa in enumerate(STANDARD_AA)}

HYDROPHOBIC = set("VILFMAW")
CHARGED = set("DEKRH")
SMALL = set("AGSTC")
AROMATIC = set("FYW")
POLAR_UNCHARGED = set("STNQ")

AA_COLORS = {
    'A': '#0000CC', 'V': '#0000CC', 'I': '#0000CC', 'L': '#0000CC', 'M': '#0000CC',
    'F': '#0000CC', 'W': '#0000CC',  # hydrophobic: blue
    'D': '#CC0000', 'E': '#CC0000',  # acidic: red
    'K': '#CC0000', 'R': '#CC0000', 'H': '#CC0000',  # basic: red
    'S': '#00CC00', 'T': '#00CC00', 'N': '#00CC00', 'Q': '#00CC00',  # polar: green
    'G': '#CC8800', 'P': '#CC8800', 'C': '#CC8800', 'Y': '#00CC00',  # special: orange
}


def load_flanks(csv_path: Path) -> list[dict]:
    flanks = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            flanks.append({
                "protein": row["protein"],
                "anchor_pos": int(row["anchor_pos"]),
                "anchor_aa": row["anchor_aa"],
                "radius": int(row["R_50"]),
                "flank_start": int(row["flank_start"]),
                "flank_len": int(row["flank_len"]),
                "sequence": row["flank_sequence"],
                "offset_to_anchor": int(row["anchor_pos"]) - int(row["flank_start"]),
            })
    return flanks


def build_centered_matrix(flanks: list[dict], window: int) -> tuple[np.ndarray, list[int]]:
    """Build a count matrix: positions [-window, +window] x 20 amino acids.

    Returns (count_matrix, n_seqs_per_position).
    """
    n_pos = 2 * window + 1
    counts = np.zeros((n_pos, 20), dtype=float)
    n_seqs = np.zeros(n_pos, dtype=int)

    for f in flanks:
        seq = f["sequence"]
        off = f["offset_to_anchor"]
        for rel_pos in range(-window, window + 1):
            seq_idx = off + rel_pos
            if 0 <= seq_idx < len(seq):
                aa = seq[seq_idx]
                if aa in AA_TO_IDX:
                    pos_idx = rel_pos + window
                    counts[pos_idx, AA_TO_IDX[aa]] += 1
                    n_seqs[pos_idx] += 1

    return counts, n_seqs


def compute_information_content(counts: np.ndarray, n_seqs: np.ndarray) -> np.ndarray:
    """Compute per-position information content (bits) using Shannon entropy.

    IC = log2(20) - H(position)  where H = -sum(p * log2(p))
    Max IC = log2(20) ~ 4.32 bits (perfectly conserved)
    """
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


def compute_property_fractions(counts: np.ndarray, n_seqs: np.ndarray) -> dict[str, np.ndarray]:
    """Compute per-position fraction of residues with each property."""
    n_pos = counts.shape[0]
    props = {
        "hydrophobic": np.zeros(n_pos),
        "charged": np.zeros(n_pos),
        "small": np.zeros(n_pos),
        "aromatic": np.zeros(n_pos),
        "polar_uncharged": np.zeros(n_pos),
        "glycine": np.zeros(n_pos),
        "proline": np.zeros(n_pos),
    }
    for i in range(n_pos):
        if n_seqs[i] == 0:
            continue
        freq = counts[i] / n_seqs[i]
        for j, aa in enumerate(STANDARD_AA):
            if aa in HYDROPHOBIC:
                props["hydrophobic"][i] += freq[j]
            if aa in CHARGED:
                props["charged"][i] += freq[j]
            if aa in SMALL:
                props["small"][i] += freq[j]
            if aa in AROMATIC:
                props["aromatic"][i] += freq[j]
            if aa in POLAR_UNCHARGED:
                props["polar_uncharged"][i] += freq[j]
            if aa == 'G':
                props["glycine"][i] += freq[j]
            if aa == 'P':
                props["proline"][i] += freq[j]
    return props


def _draw_letter(ax, letter: str, x: float, y: float, width: float, height: float, color: str):
    """Draw a single letter stretched to fill (x, y, width, height) using matplotlib transforms."""
    from matplotlib.transforms import Affine2D
    from matplotlib.textpath import TextPath
    from matplotlib.patches import PathPatch

    # Create text path for the letter
    tp = TextPath((0, 0), letter, size=1, prop={"weight": "bold", "family": "monospace"})
    # Get bounding box of the raw glyph
    bbox = tp.get_extents()
    if bbox.width == 0 or bbox.height == 0:
        return

    # Build transform: translate to origin, scale to fill target box, translate to position
    transform = Affine2D()
    transform.translate(-bbox.x0, -bbox.y0)
    transform.scale(width / bbox.width, height / bbox.height)
    transform.translate(x - width / 2, y)

    # Combine with the axes data transform
    tp_transformed = tp.transformed(transform)
    patch = PathPatch(tp_transformed, facecolor=color, edgecolor="none", lw=0)
    ax.add_patch(patch)


def plot_sequence_logo(counts: np.ndarray, n_seqs: np.ndarray, ic: np.ndarray,
                       window: int, title: str, out_path: Path, n_total: int):
    """Plot a sequence logo: stacked letters with heights proportional to IC * frequency."""
    n_pos = 2 * window + 1
    positions = list(range(-window, window + 1))

    fig, (ax_logo, ax_ic) = plt.subplots(2, 1, figsize=(max(14, window * 0.5), 5.5),
                                          gridspec_kw={"height_ratios": [3, 1]}, sharex=True)

    letter_width = 0.8
    for i in range(n_pos):
        if n_seqs[i] == 0:
            continue
        freq = counts[i] / n_seqs[i]
        # Heights = IC * freq for each AA
        heights = ic[i] * freq
        # Sort by height (smallest at bottom, largest on top)
        order = np.argsort(heights)
        y_offset = 0.0
        for j in order:
            h = heights[j]
            if h < 0.003:
                continue
            aa = STANDARD_AA[j]
            color = AA_COLORS.get(aa, "#888888")
            _draw_letter(ax_logo, aa, positions[i], y_offset, letter_width, h, color)
            y_offset += h

    y_max = min(4.5, ic.max() * 1.3) if ic.max() > 0 else 1.0
    ax_logo.set_xlim(-window - 0.5, window + 0.5)
    ax_logo.set_ylim(0, y_max)
    ax_logo.set_ylabel("Information\ncontent (bits)")
    ax_logo.axvline(0, color="#D64550", ls="--", lw=1, alpha=0.7)
    ax_logo.set_title(f"{title} (n={n_total})")
    ax_logo.spines["top"].set_visible(False)
    ax_logo.spines["right"].set_visible(False)

    # IC bar plot below
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


def plot_property_profiles(props: dict[str, np.ndarray], window: int, title: str, out_path: Path, bg_fracs: dict[str, float]):
    """Plot per-position property fractions with background lines."""
    positions = list(range(-window, window + 1))
    prop_colors = {
        "hydrophobic": "#0000CC", "charged": "#CC0000", "small": "#CC8800",
        "aromatic": "#9900CC", "polar_uncharged": "#00CC00",
        "glycine": "#666666", "proline": "#CC6600",
    }

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()

    plot_groups = [
        (["hydrophobic", "charged", "polar_uncharged"], "Major groups"),
        (["small", "aromatic"], "Size/aromatic"),
        (["glycine", "proline"], "Special residues"),
    ]

    for ax_idx, (prop_keys, group_title) in enumerate(plot_groups):
        ax = axes[ax_idx]
        for pk in prop_keys:
            ax.plot(positions, props[pk], color=prop_colors[pk], lw=1.5, label=pk)
            ax.axhline(bg_fracs.get(pk, 0), color=prop_colors[pk], ls=":", lw=0.7, alpha=0.5)
        ax.axvline(0, color="#D64550", ls="--", lw=1, alpha=0.5)
        ax.set_xlabel("Position relative to anchor")
        ax.set_ylabel("Fraction")
        ax.set_title(group_title)
        ax.legend(fontsize=7)
        ax.set_xlim(-window - 0.5, window + 0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    # Fourth panel: IC profile
    axes[3].set_visible(False)

    fig.suptitle(title, fontsize=11)
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_top_aa_per_position(counts: np.ndarray, n_seqs: np.ndarray, window: int, title: str, out_path: Path):
    """At each position, show the top-1 AA and its frequency. Highlights positions where one AA dominates."""
    positions = list(range(-window, window + 1))
    n_pos = 2 * window + 1

    top_aa = []
    top_freq = []
    second_freq = []
    for i in range(n_pos):
        if n_seqs[i] == 0:
            top_aa.append("-")
            top_freq.append(0)
            second_freq.append(0)
            continue
        freq = counts[i] / n_seqs[i]
        sorted_idx = np.argsort(-freq)
        top_aa.append(STANDARD_AA[sorted_idx[0]])
        top_freq.append(freq[sorted_idx[0]])
        second_freq.append(freq[sorted_idx[1]] if len(sorted_idx) > 1 else 0)

    fig, ax = plt.subplots(figsize=(max(12, window * 0.4), 4))

    # Background expectation: 1/20 = 5%
    ax.axhline(0.05, color="gray", ls=":", lw=0.7, alpha=0.5, label="Random (5%)")

    colors = [AA_COLORS.get(aa, "#888888") for aa in top_aa]
    bars = ax.bar(positions, top_freq, color=colors, width=0.8, edgecolor="none", alpha=0.8)

    # Label each bar with the AA
    for pos, aa, freq in zip(positions, top_aa, top_freq):
        if freq > 0.08:
            ax.text(pos, freq + 0.01, aa, ha="center", va="bottom", fontsize=6, fontweight="bold",
                    color=AA_COLORS.get(aa, "#888888"))

    ax.axvline(0, color="#D64550", ls="--", lw=1.5, alpha=0.7)
    ax.set_xlabel("Position relative to anchor")
    ax.set_ylabel("Frequency of most common AA")
    ax.set_title(title)
    ax.set_xlim(-window - 0.5, window + 0.5)
    ax.legend(fontsize=7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def compute_background_fracs(flanks: list[dict]) -> dict[str, float]:
    """Compute background amino acid property fractions from all flank residues."""
    total = Counter()
    for f in flanks:
        for aa in f["sequence"]:
            if aa in AA_TO_IDX:
                total[aa] += 1
    n = sum(total.values())
    bg = {}
    bg["hydrophobic"] = sum(total[aa] for aa in HYDROPHOBIC) / n
    bg["charged"] = sum(total[aa] for aa in CHARGED) / n
    bg["small"] = sum(total[aa] for aa in SMALL) / n
    bg["aromatic"] = sum(total[aa] for aa in AROMATIC) / n
    bg["polar_uncharged"] = sum(total[aa] for aa in POLAR_UNCHARGED) / n
    bg["glycine"] = total.get("G", 0) / n
    bg["proline"] = total.get("P", 0) / n
    return bg


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = REPORT_DIR / "anchor_flank_clustering_v2_flanks.csv"
    print(f"Loading flanks from {csv_path}...")
    flanks = load_flanks(csv_path)
    print(f"  {len(flanks)} flanks loaded")

    # ===================================================================
    # All proteins combined
    # ===================================================================
    window = 30  # show +/- 30 positions around anchor
    print(f"\nBuilding centered matrix (window=+/-{window})...")
    counts, n_seqs = build_centered_matrix(flanks, window)
    ic = compute_information_content(counts, n_seqs)
    props = compute_property_fractions(counts, n_seqs)
    bg_fracs = compute_background_fracs(flanks)

    print(f"  Coverage at anchor (pos 0): {n_seqs[window]}/{len(flanks)} proteins")
    print(f"  Coverage at pos +/-{window}: {n_seqs[0]}, {n_seqs[-1]}")

    print(f"\n  Information content at anchor (pos 0): {ic[window]:.3f} bits")
    print(f"  Max IC in window: {ic.max():.3f} bits at offset {np.argmax(ic) - window}")
    print(f"  Mean IC: {ic.mean():.3f} bits")

    # Top AA at anchor position
    anchor_freq = counts[window] / n_seqs[window]
    top3_idx = np.argsort(-anchor_freq)[:3]
    print(f"\n  Top-3 AAs at anchor position:")
    for idx in top3_idx:
        print(f"    {STANDARD_AA[idx]}: {anchor_freq[idx]:.1%}")

    # Check positions with elevated IC
    print(f"\n  Positions with IC > 0.2 bits (above random baseline ~0.05):")
    for i in range(len(ic)):
        if ic[i] > 0.2:
            pos = i - window
            freq = counts[i] / max(n_seqs[i], 1)
            top_idx = np.argmax(freq)
            print(f"    Offset {pos:+3d}: IC={ic[i]:.3f}, top AA = {STANDARD_AA[top_idx]} ({freq[top_idx]:.1%}), n={n_seqs[i]}")

    # Background fractions
    print(f"\n  Background property fractions (from all flank residues):")
    for k, v in bg_fracs.items():
        print(f"    {k}: {v:.1%}")

    # Property enrichment at anchor
    print(f"\n  Property fractions at anchor position (pos 0) vs background:")
    for k in props:
        at_anchor = props[k][window]
        bg = bg_fracs[k]
        enrichment = at_anchor / bg if bg > 0 else float("inf")
        print(f"    {k}: {at_anchor:.1%} (bg={bg:.1%}, enrichment={enrichment:.2f}x)")

    # ===================================================================
    # Stratified by anchor AA type
    # ===================================================================
    hydro_flanks = [f for f in flanks if f["anchor_aa"] in HYDROPHOBIC]
    other_flanks = [f for f in flanks if f["anchor_aa"] not in HYDROPHOBIC]
    print(f"\n  Hydrophobic anchors: {len(hydro_flanks)}, other: {len(other_flanks)}")

    counts_h, n_seqs_h = build_centered_matrix(hydro_flanks, window)
    ic_h = compute_information_content(counts_h, n_seqs_h)
    props_h = compute_property_fractions(counts_h, n_seqs_h)

    counts_o, n_seqs_o = build_centered_matrix(other_flanks, window)
    ic_o = compute_information_content(counts_o, n_seqs_o)
    props_o = compute_property_fractions(counts_o, n_seqs_o)

    print(f"\n  Hydrophobic anchors: IC at anchor = {ic_h[window]:.3f}")
    print(f"  Other anchors: IC at anchor = {ic_o[window]:.3f}")

    # ===================================================================
    # Plots
    # ===================================================================
    print(f"\n{'='*60}")
    print("Generating plots")
    print(f"{'='*60}")

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "figure.dpi": 200})

    # Sequence logo - all
    plot_sequence_logo(counts, n_seqs, ic, window, "Anchor flank sequence logo (all proteins)",
                       REPORT_DIR / "anchor_flank_motif_logo_all.png", len(flanks))

    # Sequence logo - hydrophobic anchors
    plot_sequence_logo(counts_h, n_seqs_h, ic_h, window, "Anchor flank logo (hydrophobic anchors: V/I/L/F/M/A/W)",
                       REPORT_DIR / "anchor_flank_motif_logo_hydro.png", len(hydro_flanks))

    # Sequence logo - other anchors
    plot_sequence_logo(counts_o, n_seqs_o, ic_o, window, "Anchor flank logo (non-hydrophobic anchors)",
                       REPORT_DIR / "anchor_flank_motif_logo_other.png", len(other_flanks))

    # Top AA per position
    plot_top_aa_per_position(counts, n_seqs, window, "Most common AA at each position (all proteins)",
                             REPORT_DIR / "anchor_flank_motif_top_aa.png")

    # Property profiles - all
    plot_property_profiles(props, window, "AA property profiles around anchor (all proteins, dotted=background)",
                           REPORT_DIR / "anchor_flank_motif_properties_all.png", bg_fracs)

    # Property profiles - hydrophobic vs other
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    positions = list(range(-window, window + 1))

    for ax, p_data, title_part in [
        (axes[0], props_h, f"Hydrophobic anchors (n={len(hydro_flanks)})"),
        (axes[1], props_o, f"Non-hydrophobic anchors (n={len(other_flanks)})"),
    ]:
        ax.plot(positions, p_data["hydrophobic"], color="#0000CC", lw=1.5, label="hydrophobic")
        ax.plot(positions, p_data["charged"], color="#CC0000", lw=1.5, label="charged")
        ax.plot(positions, p_data["glycine"], color="#666666", lw=1.5, label="glycine")
        ax.axhline(bg_fracs["hydrophobic"], color="#0000CC", ls=":", lw=0.5, alpha=0.5)
        ax.axhline(bg_fracs["charged"], color="#CC0000", ls=":", lw=0.5, alpha=0.5)
        ax.axhline(bg_fracs["glycine"], color="#666666", ls=":", lw=0.5, alpha=0.5)
        ax.axvline(0, color="#D64550", ls="--", lw=1, alpha=0.5)
        ax.set_xlabel("Position relative to anchor")
        ax.set_ylabel("Fraction")
        ax.set_title(title_part)
        ax.legend(fontsize=7)
        ax.set_xlim(-window - 0.5, window + 0.5)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_flank_motif_properties_stratified.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {REPORT_DIR / 'anchor_flank_motif_properties_stratified.png'}")

    # IC comparison: hydrophobic vs other
    fig, ax = plt.subplots(figsize=(12, 3.5))
    ax.plot(positions, ic_h, color="#0000CC", lw=1.5, label=f"Hydrophobic anchors (n={len(hydro_flanks)})")
    ax.plot(positions, ic_o, color="#CC0000", lw=1.5, label=f"Other anchors (n={len(other_flanks)})")
    ax.plot(positions, ic, color="#888888", lw=1, ls="--", label=f"All (n={len(flanks)})")
    ax.axvline(0, color="#D64550", ls="--", lw=1, alpha=0.5)
    ax.set_xlabel("Position relative to anchor")
    ax.set_ylabel("Information content (bits)")
    ax.set_title("Positional conservation: hydrophobic vs non-hydrophobic anchors")
    ax.legend(fontsize=7)
    ax.set_xlim(-window - 0.5, window + 0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_flank_motif_ic_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {REPORT_DIR / 'anchor_flank_motif_ic_comparison.png'}")

    # ===================================================================
    # Report
    # ===================================================================
    print("\nWriting report...")
    report = []
    report.append("# Anchor Flank Motif Analysis\n\n")
    report.append(f"Flanks from {len(flanks)} proteins (v2 clustering data), center-aligned on anchor position.\n")
    report.append(f"Window: +/- {window} positions around anchor.\n\n")

    report.append("## Information content\n\n")
    report.append(f"IC at anchor position (pos 0): {ic[window]:.3f} bits.\n")
    report.append(f"Max IC in window: {ic.max():.3f} bits at offset {np.argmax(ic) - window}.\n")
    report.append(f"Mean IC across window: {ic.mean():.3f} bits.\n")
    report.append(f"For reference: max possible IC = {math.log2(20):.2f} bits (perfectly conserved); random ~ 0.05 bits.\n\n")

    report.append("## Anchor position composition\n\n")
    for idx in top3_idx:
        report.append(f"- {STANDARD_AA[idx]}: {anchor_freq[idx]:.1%}\n")
    report.append("\n")

    report.append("## Positions with elevated conservation (IC > 0.2 bits)\n\n")
    report.append("| Offset | IC (bits) | Top AA | Frequency | n seqs |\n")
    report.append("|--------|-----------|--------|-----------|--------|\n")
    for i in range(len(ic)):
        if ic[i] > 0.2:
            pos = i - window
            freq = counts[i] / max(n_seqs[i], 1)
            top_idx = np.argmax(freq)
            report.append(f"| {pos:+3d} | {ic[i]:.3f} | {STANDARD_AA[top_idx]} | {freq[top_idx]:.1%} | {n_seqs[i]} |\n")
    report.append("\n")

    report.append("## Property enrichment at anchor\n\n")
    report.append("| Property | At anchor | Background | Enrichment |\n")
    report.append("|----------|-----------|------------|------------|\n")
    for k in ["hydrophobic", "charged", "small", "aromatic", "glycine"]:
        at_anchor = props[k][window]
        bg = bg_fracs[k]
        enrichment = at_anchor / bg if bg > 0 else float("inf")
        report.append(f"| {k} | {at_anchor:.1%} | {bg:.1%} | {enrichment:.2f}x |\n")
    report.append("\n")

    report.append("## Stratified analysis\n\n")
    report.append(f"Hydrophobic anchors (V/I/L/F/M/A/W): {len(hydro_flanks)} proteins. IC at anchor: {ic_h[window]:.3f}.\n")
    report.append(f"Non-hydrophobic anchors: {len(other_flanks)} proteins. IC at anchor: {ic_o[window]:.3f}.\n\n")

    report.append("## Figures\n\n")
    report.append("![Logo all](anchor_flank_motif_logo_all.png)\n\n")
    report.append("![Logo hydro](anchor_flank_motif_logo_hydro.png)\n\n")
    report.append("![Logo other](anchor_flank_motif_logo_other.png)\n\n")
    report.append("![Top AA](anchor_flank_motif_top_aa.png)\n\n")
    report.append("![Properties all](anchor_flank_motif_properties_all.png)\n\n")
    report.append("![Properties stratified](anchor_flank_motif_properties_stratified.png)\n\n")
    report.append("![IC comparison](anchor_flank_motif_ic_comparison.png)\n\n")

    report_path = REPORT_DIR / "anchor_flank_motif.md"
    with open(report_path, "w") as f:
        f.writelines(report)
    print(f"Saved: {report_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
