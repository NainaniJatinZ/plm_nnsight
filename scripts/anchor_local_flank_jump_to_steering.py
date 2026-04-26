#!/usr/bin/env python3
"""Direct steering at the anchor within each protein's jump_to local-flank window.

For each protein from the local-flank sweep with a detectable projection jump and
available PDB contacts:
  - take the jump_to radius from anchor_local_flank_v1_per_protein.csv
  - mask the sequence outside the anchor-centered jump_to window
  - apply steering at the anchor token inside that masked window
  - evaluate contact precision only on residue pairs where both residues are visible
  - log L10H9 head diagnostics to confirm the intervention lands in the flank setup

Usage:
    uv run python scripts/anchor_local_flank_jump_to_steering.py --device cuda
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
import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
EXPERIMENT_ROOT = ROOT / "reports" / "out2" / "suppressing_anchors"
DEFAULT_LOCAL_FLANK_DIR = EXPERIMENT_ROOT / "local_flank_v1"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"

sys.path.insert(0, str(ROOT))

ALPHAS = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 10.0, 12.0, 14.0, 16.0, 32.0]
MASK_TOKEN = "<mask>"
LONG_RANGE_SEP = 24
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN = "2B61A"


def load_flank_rows(csv_path: Path) -> list[dict]:
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["n_res"] = int(row["n_res"])
            row["anchor_pos"] = int(row["anchor_pos"])
            row["radius_int"] = int(row["radius_int"])
            row["alpha_norm"] = float(row["alpha_norm"])
            rows.append(row)
    return rows


def detect_projection_jump(protein_rows: list[dict]) -> dict | None:
    prows = sorted(protein_rows, key=lambda x: x["radius_int"])
    vals = [r["alpha_norm"] for r in prows]
    if len(vals) < 2:
        return None
    deltas = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    max_idx = int(np.argmax(deltas))
    return {
        "jump_from_radius": int(prows[max_idx]["radius_int"]),
        "jump_to_radius": int(prows[max_idx + 1]["radius_int"]),
        "jump_from_alpha_norm": float(prows[max_idx]["alpha_norm"]),
        "jump_to_alpha_norm": float(prows[max_idx + 1]["alpha_norm"]),
        "max_jump_alpha_norm": float(deltas[max_idx]),
    }


def build_masked_sequence(sequence: str, anchor_pos: int, radius: int) -> str:
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = []
    for i in range(n):
        chars.append(sequence[i] if lo <= i <= hi else MASK_TOKEN)
    return " ".join(chars)


def visible_mask(n_res: int, anchor_pos: int, radius: int) -> np.ndarray:
    lo = max(0, anchor_pos - radius)
    hi = min(n_res - 1, anchor_pos + radius)
    mask = np.zeros(n_res, dtype=bool)
    mask[lo : hi + 1] = True
    return mask


def precision_at_k_visible(
    pred_probs_AA: np.ndarray,
    gt_contacts_AA: np.ndarray,
    visible_A: np.ndarray,
    k: int,
    min_sep: int = LONG_RANGE_SEP,
) -> float:
    n = pred_probs_AA.shape[0]
    rows, cols = np.triu_indices(n, k=min_sep)
    keep = visible_A[rows] & visible_A[cols]
    rows = rows[keep]
    cols = cols[keep]
    if len(rows) == 0 or k == 0:
        return float("nan")
    pred_vals = pred_probs_AA[rows, cols]
    gt_vals = gt_contacts_AA[rows, cols]
    top_k = min(k, len(pred_vals))
    top_idx = np.argsort(-pred_vals)[:top_k]
    return float(gt_vals[top_idx].sum()) / top_k


def evaluate_visible_contacts(
    pred_probs_AA: np.ndarray,
    gt_contacts_AA: np.ndarray,
    visible_A: np.ndarray,
) -> dict:
    n_visible = int(visible_A.sum())
    return {
        "n_visible": n_visible,
        "P_L5_visible": precision_at_k_visible(pred_probs_AA, gt_contacts_AA, visible_A, max(1, n_visible // 5)),
        "P_L2_visible": precision_at_k_visible(pred_probs_AA, gt_contacts_AA, visible_A, max(1, n_visible // 2)),
        "P_L_visible": precision_at_k_visible(pred_probs_AA, gt_contacts_AA, visible_A, n_visible),
    }


def aggregate_and_plot(all_results: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "anchor_local_flank_jump_to_steering_results.csv"
    fields = list(all_results[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_results)

    alphas_sorted = sorted(set(r["alpha"] for r in all_results))
    metrics = [
        "P_L5_visible", "P_L2_visible", "P_L_visible",
        "l10h9_anchor_mass", "l10h9_top1_mass", "l10h9_entropy_norm", "l10h9_top3_mass",
        "full_P_L5_visible", "full_P_L2_visible", "full_P_L_visible",
        "delta_vs_full_P_L5_visible", "delta_vs_full_P_L2_visible", "delta_vs_full_P_L_visible",
    ]
    agg = {m: {"mean": [], "se": []} for m in metrics}

    for alpha in alphas_sorted:
        rows_at_alpha = [r for r in all_results if r["alpha"] == alpha]
        for m in metrics:
            vals = [r[m] for r in rows_at_alpha if not np.isnan(r[m])]
            agg[m]["mean"].append(np.mean(vals) if vals else float("nan"))
            agg[m]["se"].append(np.std(vals) / np.sqrt(len(vals)) if len(vals) > 1 else 0.0)

    summary = {
        "n_proteins": len(set(r["protein"] for r in all_results)),
        "alphas": alphas_sorted,
        "steering_mode": all_results[0]["steering_mode"],
    }
    for m in metrics:
        summary[f"{m}_mean"] = agg[m]["mean"]
        summary[f"{m}_se"] = agg[m]["se"]
    with open(output_dir / "anchor_local_flank_jump_to_steering_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plt.rcParams.update({
        "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 11,
        "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
        "figure.dpi": 200,
    })

    prec_colors = {"P_L5_visible": "#D64550", "P_L2_visible": "#5B7FA3", "P_L_visible": "#61afef"}
    prec_labels = {"P_L5_visible": "P@L/5", "P_L2_visible": "P@L/2", "P_L_visible": "P@L"}

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    ax = axes[0]
    for m in ["P_L5_visible", "P_L2_visible", "P_L_visible"]:
        means = np.array(agg[m]["mean"])
        ses = np.array(agg[m]["se"])
        ax.plot(alphas_sorted, means, "o-", color=prec_colors[m], label=prec_labels[m], markersize=5)
        ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color=prec_colors[m])
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Visible-subset contact precision")
    ax.set_title("jump_to masked-window contact quality")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[1]
    for m in ["delta_vs_full_P_L5_visible", "delta_vs_full_P_L2_visible", "delta_vs_full_P_L_visible"]:
        means = np.array(agg[m]["mean"])
        ses = np.array(agg[m]["se"])
        label = m.replace("delta_vs_full_", "").replace("_visible", "")
        ax.plot(alphas_sorted, means, "o-", markersize=5, label=label)
        ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15)
    ax.axhline(0.0, color="gray", ls=":", lw=0.8)
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Masked - full visible-subset precision")
    ax.set_title("Gap to full sequence on same subset")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax = axes[2]
    means = np.array(agg["l10h9_top3_mass"]["mean"])
    ses = np.array(agg["l10h9_top3_mass"]["se"])
    ax.plot(alphas_sorted, means, "o-", color="#98c379", markersize=5)
    ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color="#98c379")
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Median top-3 key mass")
    ax.set_title("L10H9 verticality in jump_to window")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle("Direct anchor suppression in the jump_to flank window", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_local_flank_jump_to_steering.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    diag_specs = [
        ("l10h9_anchor_mass", "Anchor key mass", "#c678dd"),
        ("l10h9_top1_mass", "Top-1 key mass", "#e06c75"),
        ("l10h9_entropy_norm", "Normalized entropy", "#56b6c2"),
        ("l10h9_top3_mass", "Median top-3 key mass", "#98c379"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for ax, (metric_name, ylabel, color) in zip(axes, diag_specs):
        means = np.array(agg[metric_name]["mean"])
        ses = np.array(agg[metric_name]["se"])
        ax.plot(alphas_sorted, means, "o-", color=color, markersize=5)
        ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color=color)
        ax.set_xlabel("Alpha")
        ax.set_ylabel(ylabel)
        ax.set_title(metric_name.replace("l10h9_", "L10H9 ").replace("_", " "))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("L10H9 head diagnostics in the jump_to flank window", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_local_flank_jump_to_steering_head_diagnostics.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    baseline_by_prot = {r["protein"]: r for r in all_results if r["alpha"] == 0.0}
    show_alphas = [a for a in [4.0, 12.0, 16.0] if a in alphas_sorted]
    fig, axes = plt.subplots(1, len(show_alphas), figsize=(5 * len(show_alphas), 4))
    if len(show_alphas) == 1:
        axes = [axes]
    for ax, show_alpha in zip(axes, show_alphas):
        deltas = []
        for r in all_results:
            if r["alpha"] == show_alpha and r["protein"] in baseline_by_prot:
                base = baseline_by_prot[r["protein"]]["P_L5_visible"]
                if not np.isnan(base) and not np.isnan(r["P_L5_visible"]):
                    deltas.append(r["P_L5_visible"] - base)
        ax.hist(deltas, bins=20, color=prec_colors["P_L5_visible"], alpha=0.7, edgecolor="white")
        ax.axvline(0.0, color="gray", ls=":", lw=0.8)
        ax.axvline(np.mean(deltas), color="black", ls="--", lw=1)
        ax.set_title(f"alpha={show_alpha}")
        ax.set_xlabel("Delta visible P@L/5")
        ax.set_ylabel("Count")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.suptitle("Per-protein change in jump_to visible P@L/5", fontsize=12)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_local_flank_jump_to_steering_distributions.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    md_lines = [
        "# Anchor Local Flank jump_to Steering Analysis",
        "",
        "Direct suppression at the anchor token inside each protein's `jump_to` local flank window.",
        "Contact precision is evaluated only on residue pairs where both residues are visible in that window.",
        "",
        f"Proteins scored: {summary['n_proteins']}",
        "",
        "## Mean visible-subset precision",
        "",
        "| Alpha | P@L/5 | P@L/2 | P@L |",
        "|------:|------:|------:|----:|",
    ]
    for i, alpha in enumerate(alphas_sorted):
        md_lines.append(
            f"| {alpha:.1f} | {summary['P_L5_visible_mean'][i]:.4f} | "
            f"{summary['P_L2_visible_mean'][i]:.4f} | {summary['P_L_visible_mean'][i]:.4f} |"
        )
    md_lines.extend([
        "",
        "## Mean head diagnostics",
        "",
        "| Alpha | Anchor mass | Top-1 mass | Entropy norm | Top-3 mass |",
        "|------:|------------:|-----------:|-------------:|-----------:|",
    ])
    for i, alpha in enumerate(alphas_sorted):
        md_lines.append(
            f"| {alpha:.1f} | {summary['l10h9_anchor_mass_mean'][i]:.4f} | "
            f"{summary['l10h9_top1_mass_mean'][i]:.4f} | {summary['l10h9_entropy_norm_mean'][i]:.4f} | "
            f"{summary['l10h9_top3_mass_mean'][i]:.4f} |"
        )
    md_lines.extend([
        "",
        "## Mean masked-vs-full gap on the same visible subset",
        "",
        "| Alpha | delta P@L/5 | delta P@L/2 | delta P@L |",
        "|------:|------------:|------------:|----------:|",
    ])
    for i, alpha in enumerate(alphas_sorted):
        md_lines.append(
            f"| {alpha:.1f} | {summary['delta_vs_full_P_L5_visible_mean'][i]:.4f} | "
            f"{summary['delta_vs_full_P_L2_visible_mean'][i]:.4f} | {summary['delta_vs_full_P_L_visible_mean'][i]:.4f} |"
        )
    md_lines.append("")
    with open(output_dir / "anchor_local_flank_jump_to_steering.md", "w") as f:
        f.write("\n".join(md_lines))


def main():
    parser = argparse.ArgumentParser(description="Steer the anchor direction inside each protein's jump_to flank window")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument(
        "--flank-csv",
        type=str,
        default=str(DEFAULT_LOCAL_FLANK_DIR / "anchor_local_flank_v1_per_protein.csv"),
    )
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--steering-mode", choices=["direct", "projection"], default="direct")
    parser.add_argument("--max-proteins", type=int, default=None)
    args = parser.parse_args()

    from scripts.anchor_contact_steering import (
        compute_contacts_from_attention,
        compute_l10h9_head_metrics,
        compute_l10h9_top3_mass,
        compute_search_dir,
        extract_head_weights,
        load_model,
        parse_pdb_contacts,
        cache_attention_with_steering,
    )

    if args.output_dir is None:
        output_dir = EXPERIMENT_ROOT / "local_flank_jump_to_steering" / args.steering_mode
    else:
        output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    flank_rows = load_flank_rows(Path(args.flank_csv))
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    os.environ["HF_HOME"] = WEIGHTS_DIR

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    proteins = sorted(set(r["protein"] for r in flank_rows))
    if args.max_proteins is not None:
        proteins = proteins[:args.max_proteins]
    results = []
    n_skipped_no_pdb = 0
    n_skipped_no_jump = 0

    for idx, protein in enumerate(proteins, start=1):
        seq = all_seqs.get(protein)
        if seq is None:
            continue
        gt_contacts_AA = parse_pdb_contacts(protein, seq)
        if gt_contacts_AA is None:
            n_skipped_no_pdb += 1
            continue

        prows = [r for r in flank_rows if r["protein"] == protein]
        jump = detect_projection_jump(prows)
        if jump is None:
            n_skipped_no_jump += 1
            continue

        anchor_pos = prows[0]["anchor_pos"]
        radius = jump["jump_to_radius"]
        n_res = len(seq)
        visible_A = visible_mask(n_res, anchor_pos, radius)
        masked_seq = build_masked_sequence(seq, anchor_pos, radius)
        full_seq_str = " ".join(seq)

        full_attn_LBHLL, full_inputs_BL, _ = cache_attention_with_steering(
            model, tokenizer, full_seq_str, [], d_unit, 0.0, args.device, steering_mode=args.steering_mode
        )
        full_pred_AA = compute_contacts_from_attention(
            full_attn_LBHLL, full_inputs_BL["input_ids"], full_inputs_BL["attention_mask"], contact_head, args.device
        )[0].detach().cpu().numpy()
        full_metrics = evaluate_visible_contacts(full_pred_AA, gt_contacts_AA, visible_A)

        for alpha in ALPHAS:
            attn_LBHLL, inputs_BL, _ = cache_attention_with_steering(
                model, tokenizer, masked_seq, [anchor_pos], d_unit, alpha, args.device, steering_mode=args.steering_mode
            )
            pred_AA = compute_contacts_from_attention(
                attn_LBHLL, inputs_BL["input_ids"], inputs_BL["attention_mask"], contact_head, args.device
            )[0].detach().cpu().numpy()
            masked_metrics = evaluate_visible_contacts(pred_AA, gt_contacts_AA, visible_A)
            head_metrics = compute_l10h9_head_metrics(attn_LBHLL, [anchor_pos])
            results.append({
                "protein": protein,
                "n_res": n_res,
                "anchor_pos": anchor_pos,
                "radius_int": radius,
                "jump_from_radius": jump["jump_from_radius"],
                "jump_to_radius": jump["jump_to_radius"],
                "jump_from_alpha_norm": jump["jump_from_alpha_norm"],
                "jump_to_alpha_norm": jump["jump_to_alpha_norm"],
                "max_jump_alpha_norm": jump["max_jump_alpha_norm"],
                "steering_mode": args.steering_mode,
                "alpha": alpha,
                **masked_metrics,
                "full_P_L5_visible": full_metrics["P_L5_visible"],
                "full_P_L2_visible": full_metrics["P_L2_visible"],
                "full_P_L_visible": full_metrics["P_L_visible"],
                "delta_vs_full_P_L5_visible": masked_metrics["P_L5_visible"] - full_metrics["P_L5_visible"],
                "delta_vs_full_P_L2_visible": masked_metrics["P_L2_visible"] - full_metrics["P_L2_visible"],
                "delta_vs_full_P_L_visible": masked_metrics["P_L_visible"] - full_metrics["P_L_visible"],
                "l10h9_top3_mass": compute_l10h9_top3_mass(attn_LBHLL),
                **head_metrics,
            })

        print(
            f"  [{idx}/{len(proteins)}] {protein}: jump_to R={radius} "
            f"(jump {jump['jump_from_radius']} -> {jump['jump_to_radius']})"
        )

    if not results:
        print("No results.")
        return

    aggregate_and_plot(results, output_dir)
    print(f"Saved results for {len(set(r['protein'] for r in results))} proteins to {output_dir}")
    print(f"Skipped no-PDB: {n_skipped_no_pdb}, no-jump: {n_skipped_no_jump}")


if __name__ == "__main__":
    main()
