#!/usr/bin/env python3
"""Q/K/V decomposition of anchor suppression.

Experiment 2 from experiments/downstream_attn_corruption_spec.md.

Compare four intervention targets under the canonical direct/top-3 setup:
  - ln_all: existing LayerNorm-space intervention (control)
  - k_only: modify only L10H9 key output at anchor positions
  - q_only: modify only L10H9 query output at anchor positions
  - v_only: modify only L10H9 value output at anchor positions
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
    HEAD_DIM,
    HIDDEN_DIM,
    NUM_HEADS,
    NUM_LAYERS,
    TARGET_HEAD,
    TARGET_LAYER,
    compute_contacts_from_attention,
    compute_kl_divergence,
    compute_l10h9_head_metrics,
    compute_l10h9_top3_mass,
    compute_search_dir,
    evaluate_contact_prediction,
    extract_head_weights,
    load_model,
    parse_pdb_contacts,
)

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "qkv_decomposition"
DEFAULT_CANONICAL_RESULTS = (
    EXPERIMENT_ROOT / "contact_steering" / "direct_top3" / "anchor_contact_steering_results.csv"
)
REFERENCE_PROTEIN = "2B61A"
TARGETS = ["ln_all", "k_only", "q_only", "v_only"]
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


def extract_value_head_weights(model, layer: int, head: int) -> dict:
    attn = model._model.esm.encoder.layer[layer].attention
    w_v = attn.self.value.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_v = attn.self.value.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    return {"W_V_hd": w_v[head].clone(), "b_V_d": b_v[head].clone()}


def compute_head_space_dirs(weights_qk: dict, weights_v: dict, d_unit: torch.Tensor, device: str) -> dict[str, torch.Tensor]:
    d_device = d_unit.to(device)
    q_dir = weights_qk["W_Q_hd"].to(device) @ d_device
    k_dir = weights_qk["W_K_hd"].to(device) @ d_device
    v_dir = weights_v["W_V_hd"].to(device) @ d_device
    return {
        "q_only": q_dir / q_dir.norm().clamp(min=1e-8),
        "k_only": k_dir / k_dir.norm().clamp(min=1e-8),
        "v_only": v_dir / v_dir.norm().clamp(min=1e-8),
    }


@torch.no_grad()
def cache_attention_with_targeted_intervention(
    model,
    tokenizer,
    sequence: str,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
    target: str,
    head_dirs: dict[str, torch.Tensor],
) -> tuple[list[torch.Tensor], dict, torch.Tensor]:
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    self_attn = model.esm.encoder.layer[TARGET_LAYER].attention.self
    query_module = self_attn.query
    key_module = self_attn.key
    value_module = self_attn.value

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)

            if alpha != 0.0:
                if target == "ln_all":
                    d_device = d_unit.to(device)
                    ln_out = ln_module.output
                    for pos in anchor_positions:
                        tok_idx = pos + 1
                        x_j = ln_out[:, tok_idx, :]
                        ln_out[:, tok_idx, :] = x_j - alpha * d_device
                    ln_module.output = ln_out
                else:
                    head_dir = head_dirs[target]
                    head_start = TARGET_HEAD * HEAD_DIM
                    head_end = (TARGET_HEAD + 1) * HEAD_DIM
                    if target == "q_only":
                        target_out = query_module.output
                    elif target == "k_only":
                        target_out = key_module.output
                    elif target == "v_only":
                        target_out = value_module.output
                    else:
                        raise ValueError(f"Unknown target: {target}")

                    for pos in anchor_positions:
                        tok_idx = pos + 1
                        x_j = target_out[:, tok_idx, head_start:head_end]
                        target_out[:, tok_idx, head_start:head_end] = x_j - alpha * head_dir

                    if target == "q_only":
                        query_module.output = target_out
                    elif target == "k_only":
                        key_module.output = target_out
                    else:
                        value_module.output = target_out

            logits_save = model.output.logits.save()

    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    logits_BLV = logits_save.detach().cpu()
    return attn_LBHLL, inputs_BL, logits_BLV


def process_one_pair(
    model,
    tokenizer,
    contact_head,
    protein: str,
    sequence: str,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    head_dirs: dict[str, torch.Tensor],
    device: str,
    target: str,
) -> list[dict]:
    gt_contacts_AA = parse_pdb_contacts(protein, sequence)
    if gt_contacts_AA is None:
        return []

    seq_len = len(sequence)
    results = []
    logits_clean = None
    for alpha in ALPHAS:
        attn_LBHLL, inputs_BL, logits_BLV = cache_attention_with_targeted_intervention(
            model=model,
            tokenizer=tokenizer,
            sequence=sequence,
            anchor_positions=anchor_positions,
            d_unit=d_unit,
            alpha=alpha,
            device=device,
            target=target,
            head_dirs=head_dirs,
        )
        pred_AA = compute_contacts_from_attention(
            attn_LBHLL,
            inputs_BL["input_ids"],
            inputs_BL["attention_mask"],
            contact_head,
            device,
        )[0].detach().cpu().numpy()
        contact_metrics = evaluate_contact_prediction(pred_AA, gt_contacts_AA, seq_len)
        head_metrics = compute_l10h9_head_metrics(attn_LBHLL, anchor_positions)
        top3_mass = compute_l10h9_top3_mass(attn_LBHLL)

        if alpha == 0.0:
            logits_clean = logits_BLV
            kl_div = 0.0
        else:
            kl_div = compute_kl_divergence(logits_clean, logits_BLV)

        results.append({
            "protein": protein,
            "seq_len": seq_len,
            "anchor_positions": str(anchor_positions),
            "alpha": alpha,
            "intervention_target": target,
            **contact_metrics,
            "kl_div": kl_div,
            "l10h9_top3_mass": top3_mass,
            **head_metrics,
        })
    return results


def save_csv(rows: list[dict], path: Path):
    if not rows:
        return
    fields = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def aggregate_summary(rows: list[dict]) -> dict:
    targets = [t for t in TARGETS if any(r["intervention_target"] == t for r in rows)]
    metrics = [
        "P_L5", "P_L2", "P_L", "kl_div",
        "l10h9_anchor_mass", "l10h9_top3_mass", "l10h9_entropy_norm",
    ]
    summary = {
        "n_proteins": len({r["protein"] for r in rows}),
        "alphas": ALPHAS,
        "targets": targets,
    }

    for target in targets:
        target_rows = [r for r in rows if r["intervention_target"] == target]
        for metric in metrics:
            means = []
            ses = []
            for alpha in ALPHAS:
                vals = [r[metric] for r in target_rows if r["alpha"] == alpha and not np.isnan(r[metric])]
                means.append(float(np.mean(vals)) if vals else float("nan"))
                ses.append(float(np.std(vals) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0)
            summary[f"{target}_{metric}_mean"] = means
            summary[f"{target}_{metric}_se"] = ses
    return summary


def plot_summary(summary: dict, output_dir: Path):
    targets = summary["targets"]
    alphas = summary["alphas"]
    pretty = {
        "ln_all": "LN-all",
        "k_only": "K-only",
        "q_only": "Q-only",
        "v_only": "V-only",
    }
    p_colors = {"P_L5": "#D64550", "anchor": "#c678dd"}

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    axes = axes.flatten()
    for ax, target in zip(axes, targets):
        p_l5 = np.array(summary[f"{target}_P_L5_mean"])
        p_l5_se = np.array(summary[f"{target}_P_L5_se"])
        anchor_mass = np.array(summary[f"{target}_l10h9_anchor_mass_mean"])
        anchor_se = np.array(summary[f"{target}_l10h9_anchor_mass_se"])

        ax.plot(alphas, p_l5, "o-", color=p_colors["P_L5"], label="P@L/5")
        ax.fill_between(alphas, p_l5 - p_l5_se, p_l5 + p_l5_se, color=p_colors["P_L5"], alpha=0.15)
        ax.set_xlabel("Alpha")
        ax.set_ylabel("P@L/5", color=p_colors["P_L5"])
        ax.tick_params(axis="y", labelcolor=p_colors["P_L5"])
        ax.set_title(pretty[target])
        ax.spines["top"].set_visible(False)

        ax2 = ax.twinx()
        ax2.plot(alphas, anchor_mass, "s--", color=p_colors["anchor"], label="Anchor mass")
        ax2.fill_between(alphas, anchor_mass - anchor_se, anchor_mass + anchor_se, color=p_colors["anchor"], alpha=0.12)
        ax2.set_ylabel("Anchor mass", color=p_colors["anchor"])
        ax2.tick_params(axis="y", labelcolor=p_colors["anchor"])
        ax2.spines["top"].set_visible(False)

        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc="upper right")

    fig.suptitle("Q/K/V decomposition of anchor suppression", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "qkv_decomposition.png", bbox_inches="tight")
    plt.close(fig)


def write_report(summary: dict, output_dir: Path):
    alphas = summary["alphas"]
    lines = [
        "# Q/K/V Decomposition\n",
        "\n",
        "Canonical direct/top-3 sweep with four intervention targets: `ln_all`, `k_only`, `q_only`, `v_only`.\n",
        "\n",
        f"Proteins analyzed: {summary['n_proteins']}\n",
        "\n",
    ]
    for target in summary["targets"]:
        lines.append(f"## {target}\n\n")
        lines.append("| Alpha | P@L/5 | Anchor mass | Top-3 mass | Entropy norm | KL |\n")
        lines.append("|------:|------:|------------:|-----------:|-------------:|---:|\n")
        for i, alpha in enumerate(alphas):
            lines.append(
                f"| {alpha:.1f} | {summary[f'{target}_P_L5_mean'][i]:.4f} | "
                f"{summary[f'{target}_l10h9_anchor_mass_mean'][i]:.4f} | "
                f"{summary[f'{target}_l10h9_top3_mass_mean'][i]:.4f} | "
                f"{summary[f'{target}_l10h9_entropy_norm_mean'][i]:.4f} | "
                f"{summary[f'{target}_kl_div_mean'][i]:.4f} |\n"
            )
        lines.append("\n")
    with open(output_dir / "qkv_decomposition.md", "w") as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(description="Q/K/V decomposition of anchor suppression")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--canonical-results", type=str, default=str(DEFAULT_CANONICAL_RESULTS))
    parser.add_argument("--max-proteins", type=int, default=None)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "qkv_decomposition_results.csv"

    proteins, anchors_by_protein = load_canonical_setup(Path(args.canonical_results))
    if args.max_proteins is not None:
        proteins = proteins[:args.max_proteins]
    expected_rows_per_pair = len(ALPHAS)

    existing_rows = []
    completed_pairs = set()
    if checkpoint_path.exists():
        with open(checkpoint_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["seq_len"] = int(row["seq_len"])
                row["alpha"] = float(row["alpha"])
                for key in [
                    "P_L5", "P_L2", "P_L", "kl_div",
                    "l10h9_top3_mass", "l10h9_anchor_mass", "l10h9_top1_mass",
                    "l10h9_entropy", "l10h9_entropy_norm",
                ]:
                    row[key] = float(row[key])
                existing_rows.append(row)
        counts = {}
        for row in existing_rows:
            key = (row["protein"], row["intervention_target"])
            counts[key] = counts.get(key, 0) + 1
        completed_pairs = {key for key, count in counts.items() if count == expected_rows_per_pair}
        print(f"Resuming with {len(completed_pairs)} completed protein/target pairs")

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, _, contact_head = load_model(args.device)
    weights_qk = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    weights_v = extract_value_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights_qk, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)
    head_dirs = compute_head_space_dirs(weights_qk, weights_v, d_unit, args.device)

    all_rows = list(existing_rows)
    processed_pairs = 0
    for protein in proteins:
        sequence = all_seqs[protein]
        anchor_positions = anchors_by_protein[protein]
        for target in TARGETS:
            pair = (protein, target)
            if pair in completed_pairs:
                continue
            rows = process_one_pair(
                model=model,
                tokenizer=tokenizer,
                contact_head=contact_head,
                protein=protein,
                sequence=sequence,
                anchor_positions=anchor_positions,
                d_unit=d_unit,
                head_dirs=head_dirs,
                device=args.device,
                target=target,
            )
            if rows:
                all_rows.extend(rows)
            processed_pairs += 1
            print(f"  {protein} | {target} complete")
            if processed_pairs % CHECKPOINT_EVERY == 0:
                save_csv(all_rows, checkpoint_path)
                print(f"  Checkpoint saved: {checkpoint_path}")

    if not all_rows:
        print("No results.")
        return

    save_csv(all_rows, checkpoint_path)
    summary = aggregate_summary(all_rows)
    with open(output_dir / "qkv_decomposition_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    plot_summary(summary, output_dir)
    write_report(summary, output_dir)
    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
