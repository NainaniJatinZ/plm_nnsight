#!/usr/bin/env python3
"""Track layer-10 attention output drift under anchor suppression.

Experiment 3 from experiments/downstream_attn_corruption_spec.md.

Uses the canonical direct/top-3 LN intervention and measures how the
layer-10 attention residual contribution vector changes at anchor vs
non-anchor positions.
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
    TARGET_LAYER,
    compute_search_dir,
    extract_head_weights,
    load_model,
)

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "attn_output_tracking"
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


@torch.no_grad()
def capture_attn_output_dense_with_steering(
    model,
    tokenizer,
    sequence: str,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
) -> torch.Tensor:
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    dense_module = model.esm.encoder.layer[TARGET_LAYER].attention.output.dense

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            if alpha != 0.0:
                d_device = d_unit.to(device)
                ln_out = ln_module.output
                for pos in anchor_positions:
                    tok_idx = pos + 1
                    x_j = ln_out[:, tok_idx, :]
                    ln_out[:, tok_idx, :] = x_j - alpha * d_device
                ln_module.output = ln_out
            dense_save = dense_module.output.save()
    return dense_save.detach().cpu()


def mean_norm_ratio_and_cosine(clean_XD: np.ndarray, steered_XD: np.ndarray) -> tuple[float, float]:
    clean_norms = np.linalg.norm(clean_XD, axis=-1)
    steered_norms = np.linalg.norm(steered_XD, axis=-1)
    norm_ratio = steered_norms / np.clip(clean_norms, 1e-12, None)

    denom = clean_norms * steered_norms
    cosine = np.sum(clean_XD * steered_XD, axis=-1) / np.clip(denom, 1e-12, None)
    return float(np.mean(norm_ratio)), float(np.mean(cosine))


def process_one_protein(
    model,
    tokenizer,
    protein: str,
    sequence: str,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    device: str,
) -> list[dict]:
    clean_out_BLD = capture_attn_output_dense_with_steering(
        model=model,
        tokenizer=tokenizer,
        sequence=sequence,
        anchor_positions=anchor_positions,
        d_unit=d_unit,
        alpha=0.0,
        device=device,
    )
    clean_res_D = clean_out_BLD[0, 1:-1].numpy()
    anchor_idx = np.array(anchor_positions, dtype=int)
    non_anchor_idx = np.array([i for i in range(len(sequence)) if i not in set(anchor_positions)], dtype=int)

    rows = []
    for alpha in ALPHAS:
        steered_out_BLD = capture_attn_output_dense_with_steering(
            model=model,
            tokenizer=tokenizer,
            sequence=sequence,
            anchor_positions=anchor_positions,
            d_unit=d_unit,
            alpha=alpha,
            device=device,
        )
        steered_res_D = steered_out_BLD[0, 1:-1].numpy()

        for position_type, idx in [("anchor", anchor_idx), ("non_anchor", non_anchor_idx)]:
            clean_XD = clean_res_D[idx]
            steered_XD = steered_res_D[idx]
            norm_ratio_mean, cosine_sim_mean = mean_norm_ratio_and_cosine(clean_XD, steered_XD)
            rows.append({
                "protein": protein,
                "alpha": alpha,
                "position_type": position_type,
                "n_positions": int(len(idx)),
                "norm_ratio_mean": norm_ratio_mean,
                "cosine_sim_mean": cosine_sim_mean,
            })
    return rows


def save_csv(rows: list[dict], path: Path):
    if not rows:
        return
    fields = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def aggregate_summary(rows: list[dict], canonical_summary: dict) -> dict:
    summary = {
        "n_proteins": len({r["protein"] for r in rows}),
        "alphas": ALPHAS,
        "position_types": ["anchor", "non_anchor"],
        "contact_P_L5_mean": canonical_summary["P_L5_mean"],
        "contact_P_L5_se": canonical_summary["P_L5_se"],
    }
    for position_type in ["anchor", "non_anchor"]:
        for metric in ["norm_ratio_mean", "cosine_sim_mean"]:
            means = []
            ses = []
            for alpha in ALPHAS:
                vals = [r[metric] for r in rows if r["position_type"] == position_type and r["alpha"] == alpha]
                means.append(float(np.mean(vals)) if vals else float("nan"))
                ses.append(float(np.std(vals) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0)
            summary[f"{position_type}_{metric}_mean"] = means
            summary[f"{position_type}_{metric}_se"] = ses
    return summary


def plot_summary(summary: dict, output_dir: Path):
    alphas = summary["alphas"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    colors = {"anchor": "#c678dd", "non_anchor": "#5B7FA3"}

    for ax, metric, ylabel, title in [
        (axes[0], "norm_ratio_mean", "Norm ratio", "Attention output norm drift"),
        (axes[1], "cosine_sim_mean", "Cosine similarity", "Attention output direction drift"),
    ]:
        for position_type in ["anchor", "non_anchor"]:
            means = np.array(summary[f"{position_type}_{metric}_mean"])
            ses = np.array(summary[f"{position_type}_{metric}_se"])
            ax.plot(alphas, means, "o-", color=colors[position_type], label=position_type)
            ax.fill_between(alphas, means - ses, means + ses, color=colors[position_type], alpha=0.15)
        ax.set_xlabel("Alpha")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("Layer-10 attention output tracking", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "attn_output_tracking.png", bbox_inches="tight")
    plt.close(fig)


def write_report(summary: dict, output_dir: Path):
    lines = [
        "# Attention Output Tracking\n\n",
        "Tracks the layer-10 attention residual contribution vector (`attention.output.dense`) under the canonical direct/top-3 intervention.\n\n",
        f"Proteins analyzed: {summary['n_proteins']}\n\n",
        "## Aggregate metrics\n\n",
        "| Alpha | Anchor norm ratio | Non-anchor norm ratio | Anchor cosine | Non-anchor cosine |\n",
        "|------:|------------------:|----------------------:|--------------:|------------------:|\n",
    ]
    for i, alpha in enumerate(summary["alphas"]):
        lines.append(
            f"| {alpha:.1f} | {summary['anchor_norm_ratio_mean_mean'][i]:.4f} | "
            f"{summary['non_anchor_norm_ratio_mean_mean'][i]:.4f} | "
            f"{summary['anchor_cosine_sim_mean_mean'][i]:.4f} | "
            f"{summary['non_anchor_cosine_sim_mean_mean'][i]:.4f} |\n"
        )
    with open(output_dir / "attn_output_tracking.md", "w") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(description="Track L10 attention output drift under anchor suppression")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--canonical-results", type=str, default=str(DEFAULT_CANONICAL_RESULTS))
    parser.add_argument("--canonical-summary", type=str, default=str(DEFAULT_CANONICAL_SUMMARY))
    parser.add_argument("--max-proteins", type=int, default=None)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "attn_output_tracking.csv"

    proteins, anchors_by_protein = load_canonical_setup(Path(args.canonical_results))
    if args.max_proteins is not None:
        proteins = proteins[:args.max_proteins]
    expected_rows_per_protein = len(ALPHAS) * 2

    existing_rows = []
    completed = set()
    if checkpoint_path.exists():
        with open(checkpoint_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["alpha"] = float(row["alpha"])
                row["n_positions"] = int(row["n_positions"])
                row["norm_ratio_mean"] = float(row["norm_ratio_mean"])
                row["cosine_sim_mean"] = float(row["cosine_sim_mean"])
                existing_rows.append(row)
        counts = {}
        for row in existing_rows:
            counts[row["protein"]] = counts.get(row["protein"], 0) + 1
        completed = {protein for protein, count in counts.items() if count == expected_rows_per_protein}
        print(f"Resuming with {len(completed)} proteins already complete")

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    with open(args.canonical_summary) as f:
        canonical_summary = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, _, _ = load_model(args.device)
    weights_qk = extract_head_weights(model, TARGET_LAYER, 9)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights_qk, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    all_rows = list(existing_rows)
    processed = 0
    for protein in proteins:
        if protein in completed:
            continue
        rows = process_one_protein(
            model=model,
            tokenizer=tokenizer,
            protein=protein,
            sequence=all_seqs[protein],
            anchor_positions=anchors_by_protein[protein],
            d_unit=d_unit,
            device=args.device,
        )
        all_rows.extend(rows)
        processed += 1
        print(f"  {protein} complete")
        if processed % CHECKPOINT_EVERY == 0:
            save_csv(all_rows, checkpoint_path)
            print(f"  Checkpoint saved: {checkpoint_path}")

    if not all_rows:
        print("No results.")
        return

    save_csv(all_rows, checkpoint_path)
    summary = aggregate_summary(all_rows, canonical_summary)
    with open(output_dir / "attn_output_tracking_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    plot_summary(summary, output_dir)
    write_report(summary, output_dir)
    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
