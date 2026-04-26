#!/usr/bin/env python3
"""Track downstream attention corruption under anchor suppression.

Experiment 1 from experiments/downstream_attn_corruption_spec.md.

For the canonical 20-protein direct/top-3 steering setup, measure how attention
patterns in every layer/head diverge from clean as steering alpha increases.

Outputs:
  - per-protein/layer/head CSV
  - summary JSON
  - JSD heatmap
  - layer-profile plot
  - downstream-vs-contact overlay plot
  - short markdown report
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.anchor_contact_steering import (
    ALPHAS,
    EXPERIMENT_ROOT,
    NUM_HEADS,
    NUM_LAYERS,
    cache_attention_with_steering,
    compute_search_dir,
    extract_head_weights,
    identify_anchors,
    load_model,
)

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "downstream_corruption"
DEFAULT_CANONICAL_RESULTS = (
    EXPERIMENT_ROOT / "contact_steering" / "direct_top3" / "anchor_contact_steering_results.csv"
)
DEFAULT_CANONICAL_SUMMARY = (
    EXPERIMENT_ROOT / "contact_steering" / "direct_top3" / "anchor_contact_steering_summary.json"
)
REFERENCE_PROTEIN = "2B61A"
CHECKPOINT_EVERY = 5


def load_canonical_setup(results_csv: Path) -> tuple[list[str], dict[str, list[int]]]:
    proteins = []
    anchors_by_protein = {}
    seen = set()
    with open(results_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if float(row["alpha"]) != 0.0:
                continue
            protein = row["protein"]
            if protein in seen:
                continue
            seen.add(protein)
            proteins.append(protein)
            anchors_by_protein[protein] = list(ast.literal_eval(row["anchor_positions"]))
    return proteins, anchors_by_protein


def mean_query_jsd(clean_HLL: np.ndarray, steered_HLL: np.ndarray) -> float:
    """Mean JSD across residue queries, using full key distributions."""
    p = clean_HLL[1:-1].astype(np.float64)
    q = steered_HLL[1:-1].astype(np.float64)
    p = p / np.clip(p.sum(axis=-1, keepdims=True), 1e-12, None)
    q = q / np.clip(q.sum(axis=-1, keepdims=True), 1e-12, None)
    m = 0.5 * (p + q)

    log_p = np.log2(np.clip(p, 1e-12, None))
    log_q = np.log2(np.clip(q, 1e-12, None))
    log_m = np.log2(np.clip(m, 1e-12, None))

    kl_pm = np.sum(np.where(p > 0, p * (log_p - log_m), 0.0), axis=-1)
    kl_qm = np.sum(np.where(q > 0, q * (log_q - log_m), 0.0), axis=-1)
    jsd = 0.5 * (kl_pm + kl_qm)
    return float(jsd.mean())


def attention_cosine(clean_HLL: np.ndarray, steered_HLL: np.ndarray) -> float:
    """Cosine similarity over residue-only attention matrices."""
    a = clean_HLL[1:-1, 1:-1].astype(np.float64).reshape(-1)
    b = steered_HLL[1:-1, 1:-1].astype(np.float64).reshape(-1)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom <= 1e-12:
        return float("nan")
    return float(np.dot(a, b) / denom)


def compute_divergence_rows(
    protein: str,
    alpha: float,
    clean_attn_LBHLL: list[torch.Tensor],
    steered_attn_LBHLL: list[torch.Tensor],
) -> list[dict]:
    rows = []
    for layer in range(NUM_LAYERS):
        clean_HHLL = clean_attn_LBHLL[layer][0].numpy()
        steered_HHLL = steered_attn_LBHLL[layer][0].numpy()
        for head in range(NUM_HEADS):
            clean_HLL = clean_HHLL[head]
            steered_HLL = steered_HHLL[head]
            if alpha == 0.0:
                mean_jsd = 0.0
                cosine_sim = 1.0
            else:
                mean_jsd = mean_query_jsd(clean_HLL, steered_HLL)
                cosine_sim = attention_cosine(clean_HLL, steered_HLL)
            rows.append({
                "protein": protein,
                "alpha": alpha,
                "layer": layer,
                "head": head,
                "mean_jsd": mean_jsd,
                "cosine_sim": cosine_sim,
            })
    return rows


def aggregate_summary(all_rows: list[dict], contact_summary: dict) -> dict:
    alphas_sorted = sorted({r["alpha"] for r in all_rows})
    layers_sorted = list(range(NUM_LAYERS))
    jsd_alpha_layer = []
    cosine_alpha_layer = []

    for alpha in alphas_sorted:
        jsd_by_layer = []
        cosine_by_layer = []
        for layer in layers_sorted:
            rows = [r for r in all_rows if r["alpha"] == alpha and r["layer"] == layer]
            jsd_vals = [r["mean_jsd"] for r in rows if not np.isnan(r["mean_jsd"])]
            cos_vals = [r["cosine_sim"] for r in rows if not np.isnan(r["cosine_sim"])]
            jsd_by_layer.append(float(np.mean(jsd_vals)) if jsd_vals else float("nan"))
            cosine_by_layer.append(float(np.mean(cos_vals)) if cos_vals else float("nan"))
        jsd_alpha_layer.append(jsd_by_layer)
        cosine_alpha_layer.append(cosine_by_layer)

    downstream_mean_jsd = [float(np.mean(row[11:])) for row in jsd_alpha_layer]
    pre_l10_mean_jsd = [float(np.mean(row[:10])) for row in jsd_alpha_layer]
    l10_mean_jsd = [float(row[10]) for row in jsd_alpha_layer]
    downstream_mean_cosine = [float(np.mean(row[11:])) for row in cosine_alpha_layer]

    summary = {
        "n_proteins": len({r["protein"] for r in all_rows}),
        "alphas": alphas_sorted,
        "layers": layers_sorted,
        "mean_jsd_by_alpha_layer": jsd_alpha_layer,
        "mean_cosine_by_alpha_layer": cosine_alpha_layer,
        "pre_l10_mean_jsd": pre_l10_mean_jsd,
        "l10_mean_jsd": l10_mean_jsd,
        "downstream_mean_jsd": downstream_mean_jsd,
        "downstream_mean_cosine": downstream_mean_cosine,
        "contact_P_L5_mean": contact_summary["P_L5_mean"],
        "contact_P_L5_se": contact_summary["P_L5_se"],
    }
    return summary


def write_report(output_dir: Path, summary: dict):
    alphas = summary["alphas"]
    down_jsd = summary["downstream_mean_jsd"]
    l10_jsd = summary["l10_mean_jsd"]
    pre_jsd = summary["pre_l10_mean_jsd"]
    p_l5 = summary["contact_P_L5_mean"]

    def idx(alpha_val: float) -> int:
        return alphas.index(alpha_val)

    report = []
    report.append("# Downstream Attention Corruption\n\n")
    report.append("Measures attention divergence from clean under the canonical direct/top-3 anchor suppression setup.\n\n")
    report.append(f"Proteins analyzed: {summary['n_proteins']}\n")
    report.append(f"Alphas: {', '.join(str(a) for a in alphas)}\n\n")
    report.append("## Main readout\n\n")
    report.append(
        f"- Mean downstream-layer JSD (layers 11-32) rises from {down_jsd[idx(0.0)]:.4f} at alpha=0 to "
        f"{down_jsd[idx(4.0)]:.4f} at alpha=4, {down_jsd[idx(8.0)]:.4f} at alpha=8, "
        f"{down_jsd[idx(10.0)]:.4f} at alpha=10, {down_jsd[idx(12.0)]:.4f} at alpha=12, "
        f"and {down_jsd[idx(16.0)]:.4f} at alpha=16.\n"
    )
    report.append(
        f"- Layer-10 JSD rises earlier and more strongly: {l10_jsd[idx(0.5)]:.4f} at alpha=0.5, "
        f"{l10_jsd[idx(1.0)]:.4f} at alpha=1, {l10_jsd[idx(2.0)]:.4f} at alpha=2.\n"
    )
    report.append(
        f"- Pre-L10 layers remain near-zero as expected: mean JSD across layers 0-9 is "
        f"{pre_jsd[idx(8.0)]:.4f} at alpha=8 and {pre_jsd[idx(16.0)]:.4f} at alpha=16.\n\n"
    )
    report.append("## Contact overlay\n\n")
    report.append(
        f"- Canonical P@L/5 stays high through alpha=8 ({p_l5[idx(8.0)]:.3f}), then drops at "
        f"alpha=10 ({p_l5[idx(10.0)]:.3f}) and alpha=12 ({p_l5[idx(12.0)]:.3f}).\n"
    )
    report.append(
        "- This should be compared against the downstream JSD curve in `downstream_attn_corruption_overlay.png`.\n\n"
    )
    report.append("## Files\n\n")
    report.append("- `downstream_attn_corruption.csv`: per-protein/layer/head metrics\n")
    report.append("- `downstream_attn_corruption_summary.json`: aggregate arrays used by plots\n")
    report.append("- `downstream_attn_corruption_heatmap.png`: layer x alpha mean JSD\n")
    report.append("- `downstream_attn_corruption_layer_profiles.png`: mean JSD vs layer for each alpha\n")
    report.append("- `downstream_attn_corruption_overlay.png`: downstream JSD vs contact P@L/5\n")

    with open(output_dir / "downstream_attn_corruption.md", "w") as f:
        f.writelines(report)


def plot_outputs(output_dir: Path, summary: dict):
    alphas = summary["alphas"]
    layers = summary["layers"]
    jsd = np.array(summary["mean_jsd_by_alpha_layer"], dtype=float)
    p_l5 = np.array(summary["contact_P_L5_mean"], dtype=float)
    down_jsd = np.array(summary["downstream_mean_jsd"], dtype=float)
    l10_jsd = np.array(summary["l10_mean_jsd"], dtype=float)
    pre_jsd = np.array(summary["pre_l10_mean_jsd"], dtype=float)

    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8,
        "figure.dpi": 200,
    })

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(jsd.T, aspect="auto", origin="lower", cmap="viridis")
    ax.set_xticks(range(len(alphas)))
    ax.set_xticklabels([str(a) for a in alphas], rotation=45, ha="right")
    ax.set_yticks(range(len(layers)))
    ax.set_yticklabels([str(l) for l in layers])
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Layer")
    ax.set_title("Mean attention JSD by layer and alpha")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Mean JSD")
    fig.tight_layout()
    fig.savefig(output_dir / "downstream_attn_corruption_heatmap.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = plt.cm.plasma(np.linspace(0.0, 1.0, len(alphas)))
    for color, alpha, row in zip(colors, alphas, jsd):
        ax.plot(layers, row, color=color, lw=1.6, label=f"alpha={alpha}")
    ax.set_xlabel("Layer")
    ax.set_ylabel("Mean JSD")
    ax.set_title("Attention divergence vs layer")
    ax.legend(ncol=2)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "downstream_attn_corruption_layer_profiles.png", bbox_inches="tight")
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(alphas, pre_jsd, "o-", color="#4c566a", label="layers 0-9")
    ax1.plot(alphas, l10_jsd, "o-", color="#c678dd", label="layer 10")
    ax1.plot(alphas, down_jsd, "o-", color="#e06c75", label="layers 11-32")
    ax1.set_xlabel("Alpha")
    ax1.set_ylabel("Mean JSD")
    ax1.set_title("Downstream attention corruption vs contact quality")
    ax1.spines["top"].set_visible(False)

    ax2 = ax1.twinx()
    ax2.plot(alphas, p_l5, "s--", color="#61afef", label="P@L/5")
    ax2.set_ylabel("Contact P@L/5")
    ax2.spines["top"].set_visible(False)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")
    fig.tight_layout()
    fig.savefig(output_dir / "downstream_attn_corruption_overlay.png", bbox_inches="tight")
    plt.close(fig)


def save_checkpoint(rows: list[dict], checkpoint_path: Path):
    if not rows:
        return
    fields = ["protein", "alpha", "layer", "head", "mean_jsd", "cosine_sim"]
    with open(checkpoint_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Track downstream attention corruption under anchor suppression")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--canonical-results", type=str, default=str(DEFAULT_CANONICAL_RESULTS))
    parser.add_argument("--canonical-summary", type=str, default=str(DEFAULT_CANONICAL_SUMMARY))
    parser.add_argument("--max-proteins", type=int, default=None)
    parser.add_argument("--steering-mode", choices=["direct", "projection"], default="direct")
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "downstream_attn_corruption.csv"

    canonical_results = Path(args.canonical_results)
    proteins, anchors_by_protein = load_canonical_setup(canonical_results)
    if args.max_proteins is not None:
        proteins = proteins[:args.max_proteins]
    expected_rows_per_protein = len(ALPHAS) * NUM_LAYERS * NUM_HEADS

    existing_rows = []
    completed = set()
    if checkpoint_path.exists():
        with open(checkpoint_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["alpha"] = float(row["alpha"])
                row["layer"] = int(row["layer"])
                row["head"] = int(row["head"])
                row["mean_jsd"] = float(row["mean_jsd"])
                row["cosine_sim"] = float(row["cosine_sim"])
                existing_rows.append(row)
        counts = {}
        for row in existing_rows:
            counts[row["protein"]] = counts.get(row["protein"], 0) + 1
        completed = {protein for protein, count in counts.items() if count == expected_rows_per_protein}
        print(f"Resuming with {len(completed)} proteins already complete")

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    with open(args.canonical_summary) as f:
        contact_summary = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, _, _ = load_model(args.device)
    weights = extract_head_weights(model, 10, 9)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    all_rows = list(existing_rows)
    remaining = [protein for protein in proteins if protein not in completed]
    print(f"Processing {len(remaining)} proteins ({len(completed)} already done)")

    for idx, protein in enumerate(remaining, start=1):
        sequence = all_seqs[protein]
        anchor_positions = anchors_by_protein.get(protein)
        if anchor_positions is None:
            anchor_positions = identify_anchors(model, tokenizer, sequence, args.device, top_k=args.top_k)

        clean_attn_LBHLL, _, _ = cache_attention_with_steering(
            model, tokenizer, sequence, anchor_positions, d_unit, 0.0, args.device, steering_mode=args.steering_mode
        )
        protein_rows = compute_divergence_rows(protein, 0.0, clean_attn_LBHLL, clean_attn_LBHLL)

        for alpha in ALPHAS[1:]:
            steered_attn_LBHLL, _, _ = cache_attention_with_steering(
                model, tokenizer, sequence, anchor_positions, d_unit, alpha, args.device, steering_mode=args.steering_mode
            )
            protein_rows.extend(compute_divergence_rows(protein, alpha, clean_attn_LBHLL, steered_attn_LBHLL))

        all_rows.extend(protein_rows)
        print(f"  [{idx}/{len(remaining)}] {protein} complete")

        if idx % CHECKPOINT_EVERY == 0:
            save_checkpoint(all_rows, checkpoint_path)
            print(f"  Checkpoint saved: {checkpoint_path}")

    if not all_rows:
        print("No results.")
        return

    save_checkpoint(all_rows, checkpoint_path)
    summary = aggregate_summary(all_rows, contact_summary)
    with open(output_dir / "downstream_attn_corruption_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plot_outputs(output_dir, summary)
    write_report(output_dir, summary)
    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
