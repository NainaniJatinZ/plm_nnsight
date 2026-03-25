#!/usr/bin/env python3
"""Cross-protein circuit head overlap analysis.

Discovers all proteins with cached circuit results, extracts the actual
circuit heads (using pos_k = faithfulness-crossing threshold), and reports
which heads recur across proteins.

Usage:
    python scripts/circuit_head_overlap.py
    python scripts/circuit_head_overlap.py --min-recurrence 4
"""

import argparse
import json
import torch
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "reports" / "cache"
REPORT_DIR = ROOT / "reports" / "outputs"
CONFIG_DIR = ROOT / "configs"

NUM_LAYERS = 33
NUM_HEADS = 20


def load_configs():
    with open(CONFIG_DIR / "common.json") as f:
        common = json.load(f)
    with open(CONFIG_DIR / "proteins.json") as f:
        proteins = json.load(f)
    return common, proteins


def discover_proteins():
    """Find all proteins that have both circuit_results.pt and indirect_effects.pt cached."""
    available = []
    for d in sorted(CACHE_DIR.iterdir()):
        if not d.is_dir():
            continue
        if (d / "circuit_results.pt").exists() and (d / "indirect_effects.pt").exists():
            available.append(d.name)
    return available


def load_circuit_heads(protein: str, common_cfg: dict):
    """Load indirect effects and circuit results, return the set of circuit heads and metadata."""
    cr_d = torch.load(CACHE_DIR / protein / "circuit_results.pt", map_location="cpu", weights_only=False)
    ie_d = torch.load(CACHE_DIR / protein / "indirect_effects.pt", map_location="cpu", weights_only=False)

    ie_LH = ie_d["indirect_effects_LH"]
    cr = cr_d["circuit_results"]

    # Recompute crossed_k with current faith_target (cache may be stale)
    faith_target = common_cfg["faith_target"]
    sort_results = {}
    for sort_name in ["pos", "neg", "abs"]:
        entry = cr[sort_name]
        crossed = None
        for k_val, f_val in zip(entry["k"], entry["faith"]):
            if f_val >= faith_target:
                crossed = k_val
                break
        sort_results[sort_name] = crossed

    pos_k = sort_results["pos"]
    if pos_k is None:
        pos_k = common_cfg["topk_heads"]

    # Extract circuit heads using positive IE sort
    flat = ie_LH.flatten()
    sorted_idx = flat.argsort(descending=True)

    circuit_heads = set()
    ie_values = {}
    for i in range(pos_k):
        idx = sorted_idx[i].item()
        layer = idx // NUM_HEADS
        head = idx % NUM_HEADS
        circuit_heads.add((layer, head))
        ie_values[(layer, head)] = ie_LH[layer, head].item()

    return {
        "circuit_heads": circuit_heads,
        "ie_values": ie_values,
        "pos_k": pos_k,
        "abs_k": sort_results["abs"],
        "neg_k": sort_results["neg"],
    }


def write_report(proteins_data: dict, protein_configs: dict, min_recurrence: int, excluded: dict | None = None):
    """Write the overlap analysis report."""
    proteins = sorted(proteins_data.keys())
    n_proteins = len(proteins)

    # Count head recurrence
    head_counts = Counter()
    head_proteins = defaultdict(list)
    for p in proteins:
        for h in proteins_data[p]["circuit_heads"]:
            head_counts[h] += 1
            head_proteins[h].append(p)

    out_dir = REPORT_DIR / "multi_protein"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "circuit_head_overlap.md"

    total_heads = NUM_LAYERS * NUM_HEADS

    with open(report_path, "w") as f:
        f.write("# Circuit Head Overlap Analysis\n\n")
        f.write(f"Proteins analyzed: {n_proteins}\n")
        if excluded:
            max_frac = next(iter(excluded.values()))["max_fraction"]
            f.write(f"Max circuit fraction: {max_frac:.0%} ({int(max_frac * total_heads)}/{total_heads} heads)\n")
            f.write(f"Excluded: {len(excluded)} proteins (circuit too large for sparse analysis)\n\n")
        else:
            f.write("\n")

        # Excluded proteins table
        if excluded:
            f.write("## Excluded Proteins\n\n")
            f.write("These proteins required too many heads to reach faithfulness target, indicating diffuse rather than sparse circuits.\n\n")
            f.write("| Protein | Circuit Size | Fraction | Reason |\n")
            f.write("| --- | --- | --- | --- |\n")
            for p in sorted(excluded.keys()):
                info = excluded[p]
                f.write(f"| {p} | {info['pos_k']} | {info['pos_k']/total_heads:.0%} | >{max_frac:.0%} of heads |\n")
            f.write("\n")

        # Protein summary table
        f.write("## Per-Protein Circuit Summary\n\n")
        f.write("| Protein | Contact Pair | Clean Flank | Corrupt Flank | Circuit Size (pos_k) | abs_k |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for p in proteins:
            pd = proteins_data[p]
            cfg = protein_configs.get(p, {})
            cp = cfg.get("contact_pair", ["?", "?"])
            cf = cfg.get("clean_flank", "?")
            xf = cfg.get("corrupt_flank", "?")
            f.write(f"| {p} | ({cp[0]}, {cp[1]}) | {cf} | {xf} | {pd['pos_k']} | {pd['abs_k']} |\n")

        # Summary stats
        sizes = [proteins_data[p]["pos_k"] for p in proteins]
        f.write(f"\nCircuit size stats: min={min(sizes)}, max={max(sizes)}, median={sorted(sizes)[len(sizes)//2]}, mean={sum(sizes)/len(sizes):.0f}\n")
        f.write(f"Total unique heads across all circuits: {len(head_counts)}\n\n")

        # Distribution of recurrence
        f.write("## Recurrence Distribution\n\n")
        f.write("| Appears in N proteins | Number of heads |\n")
        f.write("| --- | --- |\n")
        for n in range(n_proteins, 0, -1):
            count = sum(1 for h, c in head_counts.items() if c == n)
            if count > 0:
                f.write(f"| {n}/{n_proteins} | {count} |\n")

        # Detailed recurring heads
        f.write(f"\n## Recurring Circuit Heads (in {min_recurrence}+ proteins)\n\n")
        f.write("Heads sorted by recurrence count, then by layer.\n\n")

        recurring = [(h, c) for h, c in head_counts.items() if c >= min_recurrence]
        recurring.sort(key=lambda x: (-x[1], x[0][0], x[0][1]))

        if recurring:
            f.write("| Head | Layer | Recurrence | Proteins | Mean IE (across proteins) |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            for (layer, head), count in recurring:
                present_in = head_proteins[(layer, head)]
                ie_vals = []
                for p in present_in:
                    ie_val = proteins_data[p]["ie_values"].get((layer, head))
                    if ie_val is not None:
                        ie_vals.append(ie_val)
                mean_ie = sum(ie_vals) / len(ie_vals) if ie_vals else 0
                f.write(f"| L{layer}H{head} | {layer} | {count}/{n_proteins} | {', '.join(present_in)} | {mean_ie:.4f} |\n")
        else:
            f.write("No heads found at this recurrence threshold.\n")

        # Layer-level analysis
        f.write("\n## Layer-Level Recurrence\n\n")
        f.write("For each layer, how many of its 20 heads appear in the circuit of N+ proteins.\n\n")

        f.write("| Layer | Heads in 1+ | 2+ | 3+ | 4+ | 5+ | 6+ | 7+ | 8+ |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
        for layer in range(NUM_LAYERS):
            counts_at_thresh = []
            for thresh in [1, 2, 3, 4, 5, 6, 7, 8]:
                n = sum(1 for h in range(NUM_HEADS) if head_counts.get((layer, h), 0) >= thresh)
                counts_at_thresh.append(n)
            # Only print if layer has any heads
            if counts_at_thresh[0] > 0:
                f.write(f"| {layer} | " + " | ".join(str(c) for c in counts_at_thresh) + " |\n")

        # Core circuit: heads in 50%+ of proteins
        half = max(n_proteins // 2, 2)
        core_heads = sorted([(h, c) for h, c in head_counts.items() if c >= half], key=lambda x: (-x[1], x[0]))
        f.write(f"\n## Core Circuit (heads in {half}+ of {n_proteins} proteins)\n\n")
        f.write(f"{len(core_heads)} heads form the core circuit.\n\n")
        if core_heads:
            # Group by layer
            layer_groups = defaultdict(list)
            for (layer, head), count in core_heads:
                layer_groups[layer].append((head, count))
            f.write("| Layer | Heads (recurrence) |\n")
            f.write("| --- | --- |\n")
            for layer in sorted(layer_groups.keys()):
                heads_str = ", ".join(f"H{h} ({c}/{n_proteins})" for h, c in sorted(layer_groups[layer]))
                f.write(f"| {layer} | {heads_str} |\n")

        # Pairwise Jaccard similarity
        f.write("\n## Pairwise Circuit Similarity (Jaccard Index)\n\n")
        f.write("| " + " | ".join([""] + proteins) + " |\n")
        f.write("| " + " | ".join(["---"] * (n_proteins + 1)) + " |\n")
        for p1 in proteins:
            row = [p1]
            for p2 in proteins:
                s1 = proteins_data[p1]["circuit_heads"]
                s2 = proteins_data[p2]["circuit_heads"]
                jaccard = len(s1 & s2) / len(s1 | s2) if len(s1 | s2) > 0 else 0
                row.append(f"{jaccard:.2f}")
            f.write("| " + " | ".join(row) + " |\n")

    print(f"Report written to {report_path}")
    return report_path


def make_plots(proteins_data: dict, head_counts: Counter, out_dir: Path):
    """Generate all summary plots."""
    proteins = sorted(proteins_data.keys())
    n_proteins = len(proteins)

    plt.rcParams.update({"font.size": 10, "font.family": "sans-serif"})

    # ── 1. Layer x Head recurrence heatmap ────────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 10))
    grid = np.zeros((NUM_LAYERS, NUM_HEADS))
    for (layer, head), count in head_counts.items():
        grid[layer, head] = count

    cmap = LinearSegmentedColormap.from_list("recurrence", ["#f7f7f7", "#92c5de", "#2166ac", "#b2182b"], N=256)
    im = ax.imshow(grid, aspect="auto", cmap=cmap, vmin=0, vmax=n_proteins, interpolation="nearest")
    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_xticks(range(NUM_HEADS))
    ax.set_yticks(range(0, NUM_LAYERS, 2))
    ax.set_title(f"Head Recurrence Across {n_proteins} Protein Circuits")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Number of proteins")

    # Annotate cells with high recurrence
    threshold = n_proteins * 0.7
    for layer in range(NUM_LAYERS):
        for head in range(NUM_HEADS):
            val = grid[layer, head]
            if val >= threshold:
                ax.text(head, layer, f"{int(val)}", ha="center", va="center", fontsize=7, fontweight="bold", color="white")

    fig.tight_layout()
    fig.savefig(out_dir / "head_recurrence_heatmap.png", dpi=150)
    plt.close(fig)
    print(f"  Saved head_recurrence_heatmap.png")

    # ── 2. Circuit size distribution ──────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 4))
    sizes = [proteins_data[p]["pos_k"] for p in proteins]
    bars = ax.barh(proteins, sizes, color="#4393c3", edgecolor="white", linewidth=0.5)
    ax.set_xlabel("Circuit Size (number of heads)")
    ax.set_title("Circuit Size per Protein (positive IE, 70% faithfulness)")
    ax.axvline(np.median(sizes), color="#d6604d", linestyle="--", linewidth=1.2, label=f"median = {int(np.median(sizes))}")
    ax.legend(loc="lower right")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out_dir / "circuit_sizes.png", dpi=150)
    plt.close(fig)
    print(f"  Saved circuit_sizes.png")

    # ── 3. Top recurring heads (bar chart) ────────────────────────────────
    top_n = 30
    top_heads = sorted(head_counts.items(), key=lambda x: -x[1])[:top_n]
    labels = [f"L{l}H{h}" for (l, h), _ in top_heads]
    counts = [c for _, c in top_heads]

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#b2182b" if c >= n_proteins * 0.9 else "#d6604d" if c >= n_proteins * 0.7 else "#4393c3" for c in counts]
    ax.barh(range(len(labels)), counts, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Number of proteins")
    ax.set_title(f"Top {top_n} Most Recurring Circuit Heads")
    ax.axvline(n_proteins * 0.5, color="gray", linestyle=":", linewidth=1, alpha=0.5, label="50%")
    ax.legend(fontsize=8)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out_dir / "top_recurring_heads.png", dpi=150)
    plt.close(fig)
    print(f"  Saved top_recurring_heads.png")

    # ── 4. Layer-level summary ────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 4))
    layer_means = []
    layer_maxes = []
    for layer in range(NUM_LAYERS):
        vals = [head_counts.get((layer, h), 0) for h in range(NUM_HEADS)]
        layer_means.append(np.mean(vals))
        layer_maxes.append(max(vals))

    x = np.arange(NUM_LAYERS)
    ax.bar(x, layer_maxes, color="#d6604d", alpha=0.4, label="max head recurrence")
    ax.bar(x, layer_means, color="#2166ac", alpha=0.8, label="mean head recurrence")
    ax.set_xlabel("Layer")
    ax.set_ylabel("Recurrence (proteins)")
    ax.set_title("Per-Layer Head Recurrence Summary")
    ax.set_xticks(range(0, NUM_LAYERS, 2))
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "layer_recurrence.png", dpi=150)
    plt.close(fig)
    print(f"  Saved layer_recurrence.png")

    # ── 5. Pairwise Jaccard heatmap ───────────────────────────────────────
    n = len(proteins)
    jaccard_mat = np.zeros((n, n))
    for i, p1 in enumerate(proteins):
        for j, p2 in enumerate(proteins):
            s1 = proteins_data[p1]["circuit_heads"]
            s2 = proteins_data[p2]["circuit_heads"]
            jaccard_mat[i, j] = len(s1 & s2) / len(s1 | s2) if len(s1 | s2) > 0 else 0

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(jaccard_mat, cmap="YlOrRd", vmin=0, vmax=0.7, interpolation="nearest")
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(proteins, rotation=90, fontsize=7)
    ax.set_yticklabels(proteins, fontsize=7)
    ax.set_title("Pairwise Circuit Similarity (Jaccard Index)")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Jaccard Index")
    fig.tight_layout()
    fig.savefig(out_dir / "jaccard_heatmap.png", dpi=150)
    plt.close(fig)
    print(f"  Saved jaccard_heatmap.png")

    # ── 6. Mean IE heatmap for recurring heads ────────────────────────────
    fig, ax = plt.subplots(figsize=(12, 10))
    ie_grid = np.full((NUM_LAYERS, NUM_HEADS), np.nan)
    for (layer, head), count in head_counts.items():
        if count >= 3:
            ie_vals = []
            for p in proteins:
                ie_val = proteins_data[p]["ie_values"].get((layer, head))
                if ie_val is not None:
                    ie_vals.append(ie_val)
            if ie_vals:
                ie_grid[layer, head] = np.mean(ie_vals)

    masked = np.ma.masked_invalid(ie_grid)
    cmap_ie = plt.cm.RdBu_r.copy()
    cmap_ie.set_bad(color="#f0f0f0")
    vmax = np.nanmax(np.abs(ie_grid[~np.isnan(ie_grid)])) if np.any(~np.isnan(ie_grid)) else 0.1
    im = ax.imshow(masked, aspect="auto", cmap=cmap_ie, vmin=-vmax, vmax=vmax, interpolation="nearest")
    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_xticks(range(NUM_HEADS))
    ax.set_yticks(range(0, NUM_LAYERS, 2))
    ax.set_title("Mean Indirect Effect (heads in 3+ protein circuits)")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Mean IE across proteins")
    fig.tight_layout()
    fig.savefig(out_dir / "mean_ie_heatmap.png", dpi=150)
    plt.close(fig)
    print(f"  Saved mean_ie_heatmap.png")


def main():
    total_heads = NUM_LAYERS * NUM_HEADS

    parser = argparse.ArgumentParser(description="Circuit head overlap analysis")
    parser.add_argument("--min-recurrence", type=int, default=3, help="Minimum recurrence to list in detailed table (default: 3)")
    parser.add_argument("--max-fraction", type=float, default=0.40, help="Exclude proteins whose circuit exceeds this fraction of total heads (default: 0.40)")
    parser.add_argument("--no-plots", action="store_true", help="Skip plot generation")
    args = parser.parse_args()

    max_heads = int(args.max_fraction * total_heads)

    common_cfg, protein_configs = load_configs()

    available = discover_proteins()
    print(f"Found {len(available)} proteins with cached circuit data")
    print(f"Max circuit fraction: {args.max_fraction:.0%} ({max_heads}/{total_heads} heads)\n")

    all_data = {}
    for p in available:
        try:
            data = load_circuit_heads(p, common_cfg)
            all_data[p] = data
            print(f"  {p}: circuit size = {data['pos_k']} heads ({data['pos_k']/total_heads:.0%})")
        except Exception as e:
            print(f"  {p}: SKIPPED ({e})")

    # Split into included and excluded
    proteins_data = {}
    excluded = {}
    for p, data in all_data.items():
        if data["pos_k"] > max_heads:
            excluded[p] = {**data, "max_fraction": args.max_fraction}
        else:
            proteins_data[p] = data

    if excluded:
        print(f"\nExcluded {len(excluded)} proteins with non-sparse circuits (>{args.max_fraction:.0%}):")
        for p in sorted(excluded):
            print(f"  {p}: {excluded[p]['pos_k']} heads ({excluded[p]['pos_k']/total_heads:.0%})")

    print(f"\nAnalyzing {len(proteins_data)} proteins...")
    report_path = write_report(proteins_data, protein_configs, args.min_recurrence, excluded=excluded)

    if not args.no_plots:
        out_dir = REPORT_DIR / "multi_protein"
        head_counts = Counter()
        for p in proteins_data:
            for h in proteins_data[p]["circuit_heads"]:
                head_counts[h] += 1
        print("\nGenerating plots...")
        make_plots(proteins_data, head_counts, out_dir)

    print("Done.")


if __name__ == "__main__":
    main()
