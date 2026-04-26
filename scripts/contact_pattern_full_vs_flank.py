#!/usr/bin/env python3
"""Compare contact-pattern steering effects in full-sequence vs flank contexts.

For selected proteins, evaluate the exact contact-pattern segment metric under:
  - full clean sequence
  - clean flank masked sequence from contact_pattern_v2

In each context:
  - dynamically identify top-3 anchors in that clean context
  - apply `ln_all`, `k_only`, and `v_only` interventions on the clean input
  - patch in the corrupt-flank L10H9 attention pattern as a reference perturbation

This is the direct context-dependence comparison for the same proteins.
"""

from __future__ import annotations

import argparse
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
    TARGET_HEAD,
    TARGET_LAYER,
    compute_contacts_from_attention,
    compute_l10h9_head_metrics,
    compute_l10h9_top3_mass,
    compute_search_dir,
    extract_head_weights,
    identify_anchors,
    load_model,
)
from scripts.jump_to_contact_pattern_bridge import (
    ContactSegment,
    load_protein_cfg,
    mask_with_flanks,
    compute_contact_map,
    patching_metric,
    cache_attention_all_layers,
    patch_corrupt_l10h9_into_clean,
)
from scripts.qkv_decomposition import (
    compute_head_space_dirs,
    extract_value_head_weights,
    cache_attention_with_targeted_intervention,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "contact_pattern_full_vs_flank"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
TARGETS = ["ln_all", "k_only", "v_only"]


def summarize_row(
    protein: str,
    context: str,
    variant: str,
    alpha: float | None,
    metric: float,
    context_baseline: float,
    anchor_positions: list[int],
    attn_LBHLL: list[torch.Tensor],
) -> dict:
    head_metrics = compute_l10h9_head_metrics(attn_LBHLL, anchor_positions)
    return {
        "protein": protein,
        "context": context,
        "variant": variant,
        "alpha": float("nan") if alpha is None else float(alpha),
        "segment_metric": metric,
        "delta_from_context_baseline": metric - context_baseline,
        "anchor_positions": str(anchor_positions),
        "l10h9_top3_mass": compute_l10h9_top3_mass(attn_LBHLL),
        **head_metrics,
    }


def save_outputs(rows: list[dict], protein_meta: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "contact_pattern_full_vs_flank.csv"
    md_path = output_dir / "contact_pattern_full_vs_flank.md"
    meta_path = output_dir / "contact_pattern_full_vs_flank_meta.json"
    summary_path = output_dir / "contact_pattern_full_vs_flank_summary.json"

    fields = list(rows[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with open(meta_path, "w") as f:
        json.dump(protein_meta, f, indent=2)

    summary = {"proteins": [m["protein"] for m in protein_meta], "alphas": ALPHAS}
    for context in ["full", "flank"]:
        for variant in ["corrupt_head_patch_from_flank", *TARGETS]:
            if variant == "corrupt_head_patch_from_flank":
                sub = [r for r in rows if r["context"] == context and r["variant"] == variant]
                if sub:
                    summary[f"{context}_{variant}_segment_metric_mean"] = float(np.mean([r["segment_metric"] for r in sub]))
                    summary[f"{context}_{variant}_anchor_mass_mean"] = float(np.mean([r["l10h9_anchor_mass"] for r in sub]))
                continue
            metrics = []
            anchor_mass = []
            for alpha in ALPHAS:
                sub = [r for r in rows if r["context"] == context and r["variant"] == variant and r["alpha"] == alpha]
                metrics.append(float(np.mean([r["segment_metric"] for r in sub])))
                anchor_mass.append(float(np.mean([r["l10h9_anchor_mass"] for r in sub])))
            summary[f"{context}_{variant}_segment_metric_mean"] = metrics
            summary[f"{context}_{variant}_anchor_mass_mean"] = anchor_mass

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 8,
        "figure.dpi": 200,
    })

    colors = {"ln_all": "#1d3557", "k_only": "#2a9d8f", "v_only": "#e76f51", "corrupt_head_patch_from_flank": "#6a4c93"}
    styles = {"full": "-", "flank": "--"}

    fig, axes = plt.subplots(len(protein_meta), 2, figsize=(12, 4 * len(protein_meta)))
    if len(protein_meta) == 1:
        axes = np.array([axes])
    for row_idx, meta in enumerate(protein_meta):
        protein = meta["protein"]
        prot_rows = [r for r in rows if r["protein"] == protein]
        for col_idx, metric_name in enumerate(["segment_metric", "l10h9_anchor_mass"]):
            ax = axes[row_idx, col_idx]
            for context in ["full", "flank"]:
                base = [r for r in prot_rows if r["context"] == context and r["variant"] == "baseline"][0]
                ax.scatter(
                    [-1.0 if context == "full" else -0.5],
                    [base[metric_name]],
                    color="#2d6a4f" if context == "full" else "#40916c",
                    s=70,
                    label=f"{context} baseline",
                )
                patch_rows = [r for r in prot_rows if r["context"] == context and r["variant"] == "corrupt_head_patch_from_flank"]
                if patch_rows:
                    ax.scatter(
                        [0.0 if context == "full" else 0.3],
                        [patch_rows[0][metric_name]],
                        color=colors["corrupt_head_patch_from_flank"],
                        s=70,
                        label=f"{context} corrupt_head_patch",
                    )
                for variant in TARGETS:
                    curve = sorted([r for r in prot_rows if r["context"] == context and r["variant"] == variant], key=lambda x: x["alpha"])
                    ax.plot(
                        [r["alpha"] for r in curve],
                        [r[metric_name] for r in curve],
                        "o",
                        color=colors[variant],
                        markersize=3,
                    )
                    ax.plot(
                        [r["alpha"] for r in curve],
                        [r[metric_name] for r in curve],
                        styles[context],
                        color=colors[variant],
                        label=f"{context} {variant}",
                    )
            ax.set_title(f"{protein}: {'segment metric' if metric_name == 'segment_metric' else 'anchor mass'}")
            ax.set_xlabel("alpha")
            ax.set_ylabel(metric_name.replace("_", " "))
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
    handles, labels = axes[0, 0].get_legend_handles_labels()
    seen = set()
    dedup_handles = []
    dedup_labels = []
    for h, l in zip(handles, labels):
        if l not in seen:
            seen.add(l)
            dedup_handles.append(h)
            dedup_labels.append(l)
    fig.legend(dedup_handles, dedup_labels, loc="upper center", ncol=4, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(output_dir / "contact_pattern_full_vs_flank.png", bbox_inches="tight")
    plt.close(fig)

    md_lines = [
        "# Contact Pattern Full vs Flank",
        "",
        "Compares the same segment-level contact-pattern metric in `full` and `flank` contexts.",
        "The corrupt reference patch always comes from the corrupt flank sequence.",
        "",
        "## Protein Setup",
        "",
        "| Protein | Contact pair | Clean flank | Corrupt flank | Full anchors | Flank anchors | Corrupt flank anchors |",
        "|---------|--------------|-------------|---------------|--------------|---------------|-----------------------|",
    ]
    for meta in protein_meta:
        md_lines.append(
            f"| {meta['protein']} | {tuple(meta['contact_pair'])} | {meta['clean_flank']} | {meta['corrupt_flank']} | "
            f"{meta['full_anchor_positions']} | {meta['flank_anchor_positions']} | {meta['corrupt_flank_anchor_positions']} |"
        )

    for meta in protein_meta:
        protein = meta["protein"]
        md_lines.extend([
            "",
            f"## {protein}",
            "",
            "| Context | Variant | Alpha | Segment metric | Delta vs context baseline | Anchor mass | Top-1 mass | Entropy norm | Top-3 mass |",
            "|---------|---------|------:|---------------:|--------------------------:|------------:|-----------:|-------------:|-----------:|",
        ])
        prot_rows = [r for r in rows if r["protein"] == protein]
        order = {"baseline": 0, "corrupt_head_patch_from_flank": 1, "ln_all": 2, "k_only": 3, "v_only": 4}
        prot_rows.sort(key=lambda r: (r["context"], order[r["variant"]], -1 if np.isnan(r["alpha"]) else r["alpha"]))
        for r in prot_rows:
            alpha_str = "—" if np.isnan(r["alpha"]) else f"{r['alpha']:.1f}"
            md_lines.append(
                f"| {r['context']} | {r['variant']} | {alpha_str} | {r['segment_metric']:.4f} | "
                f"{r['delta_from_context_baseline']:.4f} | {r['l10h9_anchor_mass']:.4f} | "
                f"{r['l10h9_top1_mass']:.4f} | {r['l10h9_entropy_norm']:.4f} | {r['l10h9_top3_mass']:.4f} |"
            )

    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))


def main():
    parser = argparse.ArgumentParser(description="Compare contact-pattern steering in full vs flank contexts")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    qk_weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    v_weights = extract_value_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    print("Computing search direction from 2B61A...")
    search_dir = compute_search_dir(model, tokenizer, seq_dict["2B61A"], qk_weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)
    head_dirs = compute_head_space_dirs(qk_weights, v_weights, d_unit, args.device)

    rows = []
    protein_meta = []

    for protein in args.proteins:
        print(f"Processing {protein}...")
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])
        full_seq = sequence
        flank_seq = mask_with_flanks(sequence, seg, cfg["clean_flank"])
        corrupt_flank_seq = mask_with_flanks(sequence, seg, cfg["corrupt_flank"])

        orig_contacts = compute_contact_map(esm_model, tokenizer, full_seq, args.device)
        full_contacts = compute_contact_map(esm_model, tokenizer, full_seq, args.device)
        flank_contacts = compute_contact_map(esm_model, tokenizer, flank_seq, args.device)
        corrupt_contacts = compute_contact_map(esm_model, tokenizer, corrupt_flank_seq, args.device)

        full_metric = patching_metric(full_contacts, orig_contacts, seg)
        flank_metric = patching_metric(flank_contacts, orig_contacts, seg)
        corrupt_metric = patching_metric(corrupt_contacts, orig_contacts, seg)

        corrupt_attn, _ = cache_attention_all_layers(model, tokenizer, corrupt_flank_seq, args.device)
        corrupt_l10h9_attn = corrupt_attn[TARGET_LAYER][:, TARGET_HEAD, :, :]
        corrupt_flank_anchor_positions = identify_anchors(model, tokenizer, corrupt_flank_seq, args.device, top_k=3)

        full_anchor_positions = identify_anchors(model, tokenizer, full_seq, args.device, top_k=3)
        flank_anchor_positions = identify_anchors(model, tokenizer, flank_seq, args.device, top_k=3)
        protein_meta.append({
            "protein": protein,
            "contact_pair": cfg["contact_pair"],
            "clean_flank": cfg["clean_flank"],
            "corrupt_flank": cfg["corrupt_flank"],
            "full_anchor_positions": full_anchor_positions,
            "flank_anchor_positions": flank_anchor_positions,
            "corrupt_flank_anchor_positions": corrupt_flank_anchor_positions,
            "full_metric": full_metric,
            "flank_metric": flank_metric,
            "corrupt_flank_metric": corrupt_metric,
        })

        for context, clean_sequence, context_baseline, context_anchors in [
            ("full", full_seq, full_metric, full_anchor_positions),
            ("flank", flank_seq, flank_metric, flank_anchor_positions),
        ]:
            clean_attn, _ = cache_attention_all_layers(model, tokenizer, clean_sequence, args.device)
            rows.append(summarize_row(
                protein=protein,
                context=context,
                variant="baseline",
                alpha=None,
                metric=context_baseline,
                context_baseline=context_baseline,
                anchor_positions=context_anchors,
                attn_LBHLL=clean_attn,
            ))

            patched_attn, patched_inputs = patch_corrupt_l10h9_into_clean(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                corrupt_l10h9_attn_BLL=corrupt_l10h9_attn,
                device=args.device,
            )
            patched_contacts = compute_contacts_from_attention(
                patched_attn,
                patched_inputs["input_ids"],
                patched_inputs["attention_mask"],
                contact_head,
                args.device,
            )[0].detach().cpu()
            patched_metric = patching_metric(patched_contacts, orig_contacts, seg)
            rows.append(summarize_row(
                protein=protein,
                context=context,
                variant="corrupt_head_patch_from_flank",
                alpha=None,
                metric=patched_metric,
                context_baseline=context_baseline,
                anchor_positions=context_anchors,
                attn_LBHLL=patched_attn,
            ))

            for target in TARGETS:
                for alpha in ALPHAS:
                    attn_LBHLL, inputs_BL, _ = cache_attention_with_targeted_intervention(
                        model=model,
                        tokenizer=tokenizer,
                        sequence=clean_sequence,
                        anchor_positions=context_anchors,
                        d_unit=d_unit,
                        alpha=alpha,
                        device=args.device,
                        target=target,
                        head_dirs=head_dirs,
                    )
                    contacts = compute_contacts_from_attention(
                        attn_LBHLL,
                        inputs_BL["input_ids"],
                        inputs_BL["attention_mask"],
                        contact_head,
                        args.device,
                    )[0].detach().cpu()
                    metric = patching_metric(contacts, orig_contacts, seg)
                    rows.append(summarize_row(
                        protein=protein,
                        context=context,
                        variant=target,
                        alpha=alpha,
                        metric=metric,
                        context_baseline=context_baseline,
                        anchor_positions=context_anchors,
                        attn_LBHLL=attn_LBHLL,
                    ))

    save_outputs(rows, protein_meta, Path(args.output_dir))
    print(f"Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
