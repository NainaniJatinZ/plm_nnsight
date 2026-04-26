#!/usr/bin/env python3
"""Bridge contact-pattern patching and anchor steering in the local masked setup.

For selected proteins, recreate the exact clean/corrupt masked setup from
`contact_pattern_v2.py`, then compare on the same segment-level metric:

1. Clean and corrupt masked baselines.
2. Clean pass with the corrupt L10H9 attention pattern patched in.
3. Clean pass with anchor-direction steering on dynamically identified top-3 anchors
   in the clean masked setup.

The goal is to directly compare "this head has a causal effect when we swap in
the corrupt pattern" against "destroying the anchor pattern by steering" on the
same proteins and the same contact-pattern metric.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
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
from scripts.qkv_decomposition import (
    compute_head_space_dirs,
    extract_value_head_weights,
    cache_attention_with_targeted_intervention,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
PROTEINS_CFG = ROOT / "configs" / "proteins.json"
COMMON_CFG = ROOT / "configs" / "common.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "jump_to_contact_pattern_bridge"
REFERENCE_PROTEIN = "2B61A"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
TARGETS = ["ln_all", "k_only", "v_only"]


@dataclass
class ContactSegment:
    ss1_start: int
    ss1_end: int
    ss2_start: int
    ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int):
        return cls(pos1 - radius, pos1 + radius + 1, pos2 - radius, pos2 + radius + 1)


def load_protein_cfg(protein: str) -> dict:
    with open(COMMON_CFG) as f:
        cfg = json.load(f)
    with open(PROTEINS_CFG) as f:
        proteins_cfg = json.load(f)
    cfg.update(proteins_cfg[protein])
    return cfg


def mask_with_flanks(seq_S: str, seg: ContactSegment, flank: int) -> str:
    n = len(seq_S)
    masked: list[str] = ["<mask>"] * n
    masked[seg.ss1_start:seg.ss1_end] = list(seq_S[seg.ss1_start:seg.ss1_end])
    masked[seg.ss2_start:seg.ss2_end] = list(seq_S[seg.ss2_start:seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
        masked[i] = seq_S[i]
    return "".join(masked)


@torch.no_grad()
def compute_contact_map(esm_model, tokenizer, sequence_S: str, device: str) -> torch.Tensor:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    return esm_model.predict_contacts(inputs_BL["input_ids"], inputs_BL["attention_mask"])[0].detach().cpu()


def patching_metric(pred_AA: torch.Tensor | np.ndarray, orig_AA: torch.Tensor | np.ndarray, seg: ContactSegment) -> float:
    if isinstance(pred_AA, torch.Tensor):
        pred_AA = pred_AA.detach().cpu().numpy()
    if isinstance(orig_AA, torch.Tensor):
        orig_AA = orig_AA.detach().cpu().numpy()
    pred = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = float((orig * orig).sum())
    if denom <= 1e-12:
        return 0.0
    return float((pred * orig).sum() / denom)


def faithfulness(metric: float, clean_m: float, corrupt_m: float) -> float:
    gap = clean_m - corrupt_m
    return (metric - corrupt_m) / gap if abs(gap) > 1e-6 else 0.0


@torch.no_grad()
def cache_attention_all_layers(model, tokenizer, sequence: str, device: str) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)
    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_LBHLL, inputs_BL


@torch.no_grad()
def patch_corrupt_l10h9_into_clean(
    model,
    tokenizer,
    clean_sequence: str,
    corrupt_l10h9_attn_BLL: torch.Tensor,
    device: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    self_attn = model.esm.encoder.layer[TARGET_LAYER].attention.self

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)

            batch_size, seq_len = inputs_BL["input_ids"].shape
            v_raw = self_attn.value.output
            v_heads = v_raw.reshape(batch_size, seq_len, NUM_HEADS, -1).transpose(1, 2)

            clean_attn = self_attn.output[1]
            patched_attn = clean_attn.clone()
            patched_attn[:, TARGET_HEAD, :, :] = corrupt_l10h9_attn_BLL.to(device)

            new_ctx = torch.matmul(patched_attn, v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
            self_attn.output[0][:] = new_ctx

    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        if i == TARGET_LAYER:
            layer_attn[:, TARGET_HEAD, :, :] = corrupt_l10h9_attn_BLL.detach().cpu()
        attn_LBHLL.append(layer_attn)
    return attn_LBHLL, inputs_BL


def summarize_variant(
    protein: str,
    variant: str,
    base_setup: str,
    alpha: float | None,
    anchor_positions: list[int],
    metric: float,
    clean_metric: float,
    corrupt_metric: float,
    attn_LBHLL: list[torch.Tensor],
) -> dict:
    head_metrics = compute_l10h9_head_metrics(attn_LBHLL, anchor_positions)
    return {
        "protein": protein,
        "base_setup": base_setup,
        "variant": variant,
        "alpha": float("nan") if alpha is None else float(alpha),
        "anchor_positions": str(anchor_positions),
        "segment_metric": metric,
        "faithfulness": faithfulness(metric, clean_metric, corrupt_metric),
        "l10h9_top3_mass": compute_l10h9_top3_mass(attn_LBHLL),
        **head_metrics,
    }


def aggregate_rows(rows: list[dict]) -> dict:
    proteins = sorted({r["protein"] for r in rows})
    variants = []
    seen = set()
    for row in rows:
        alpha_key = None if np.isnan(row["alpha"]) else float(row["alpha"])
        key = (row["variant"], alpha_key)
        if key not in seen:
            seen.add(key)
            variants.append(key)

    summary = {
        "proteins": proteins,
        "n_proteins": len(proteins),
        "variants": [
            {"variant": variant, "alpha": alpha}
            for variant, alpha in variants
        ],
    }

    metrics = [
        "segment_metric",
        "faithfulness",
        "l10h9_anchor_mass",
        "l10h9_top1_mass",
        "l10h9_entropy_norm",
        "l10h9_top3_mass",
    ]
    for variant, alpha in variants:
        sub = [
            r for r in rows
            if r["variant"] == variant and (
                (np.isnan(r["alpha"]) and alpha is None) or r["alpha"] == alpha
            )
        ]
        key_prefix = variant if alpha is None else f"{variant}_alpha_{alpha:g}"
        for metric in metrics:
            vals = [r[metric] for r in sub if not np.isnan(r[metric])]
            summary[f"{key_prefix}_{metric}_mean"] = float(np.mean(vals)) if vals else float("nan")
            summary[f"{key_prefix}_{metric}_se"] = float(np.std(vals) / np.sqrt(len(vals))) if len(vals) > 1 else 0.0
    return summary


def save_outputs(rows: list[dict], protein_meta: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "jump_to_contact_pattern_bridge.csv"
    meta_path = output_dir / "jump_to_contact_pattern_bridge_protein_meta.json"
    summary_path = output_dir / "jump_to_contact_pattern_bridge_summary.json"
    md_path = output_dir / "jump_to_contact_pattern_bridge.md"

    fields = list(rows[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    with open(meta_path, "w") as f:
        json.dump(protein_meta, f, indent=2)

    summary = aggregate_rows(rows)
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 9,
        "figure.dpi": 200,
    })

    proteins = [m["protein"] for m in protein_meta]

    colors = {
        "clean_baseline": "#2d6a4f",
        "corrupt_baseline": "#c1121f",
        "corrupt_head_patch": "#6a4c93",
        "ln_all": "#1d3557",
        "k_only": "#2a9d8f",
        "v_only": "#e76f51",
    }

    if len(proteins) <= 6:
        fig, axes = plt.subplots(len(proteins), 2, figsize=(12, 4 * len(proteins)))
        if len(proteins) == 1:
            axes = np.array([axes])

        for row_idx, protein in enumerate(proteins):
            prot_rows = [r for r in rows if r["protein"] == protein]
            ax = axes[row_idx, 0]
            base_rows = [r for r in prot_rows if r["variant"] in {"clean_baseline", "corrupt_baseline", "corrupt_head_patch"}]
            for r in base_rows:
                x = -1 if r["variant"] == "clean_baseline" else (-0.5 if r["variant"] == "corrupt_baseline" else 0.0)
                ax.scatter([x], [r["segment_metric"]], s=70, color=colors[r["variant"]], label=r["variant"])
            for variant in ["ln_all", "k_only", "v_only"]:
                curve = sorted([r for r in prot_rows if r["variant"] == variant], key=lambda x: x["alpha"])
                ax.plot(
                    [r["alpha"] for r in curve],
                    [r["segment_metric"] for r in curve],
                    "o-",
                    color=colors[variant],
                    label=variant,
                    markersize=4,
                )
            ax.set_title(f"{protein}: segment metric")
            ax.set_xlabel("alpha")
            ax.set_ylabel("metric vs full-seq orig")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            ax = axes[row_idx, 1]
            for r in base_rows:
                x = -1 if r["variant"] == "clean_baseline" else (-0.5 if r["variant"] == "corrupt_baseline" else 0.0)
                ax.scatter([x], [r["l10h9_anchor_mass"]], s=70, color=colors[r["variant"]], label=r["variant"])
            for variant in ["ln_all", "k_only", "v_only"]:
                curve = sorted([r for r in prot_rows if r["variant"] == variant], key=lambda x: x["alpha"])
                ax.plot(
                    [r["alpha"] for r in curve],
                    [r["l10h9_anchor_mass"] for r in curve],
                    "o-",
                    color=colors[variant],
                    label=variant,
                    markersize=4,
                )
            ax.set_title(f"{protein}: L10H9 anchor mass")
            ax.set_xlabel("alpha")
            ax.set_ylabel("anchor mass")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

        handles, labels = axes[0, 0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=6, frameon=False)
        fig.tight_layout(rect=[0, 0, 1, 0.96])
        fig.savefig(output_dir / "jump_to_contact_pattern_bridge.png", bbox_inches="tight")
        plt.close(fig)
    else:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
        baseline_variants = ["clean_baseline", "corrupt_baseline", "corrupt_head_patch"]
        baseline_x = {"clean_baseline": -1.0, "corrupt_baseline": -0.5, "corrupt_head_patch": 0.0}

        ax = axes[0]
        for variant in baseline_variants:
            vals = [r["segment_metric"] for r in rows if r["variant"] == variant]
            if vals:
                ax.scatter(
                    [baseline_x[variant]],
                    [float(np.mean(vals))],
                    s=80,
                    color=colors[variant],
                    label=variant,
                )
        for variant in ["ln_all", "k_only", "v_only"]:
            means = []
            for alpha in ALPHAS:
                vals = [r["segment_metric"] for r in rows if r["variant"] == variant and r["alpha"] == alpha]
                means.append(float(np.mean(vals)))
            ax.plot(ALPHAS, means, "o-", color=colors[variant], label=variant, markersize=4)
        ax.set_title("Aggregate segment metric")
        ax.set_xlabel("alpha")
        ax.set_ylabel("metric vs full-seq orig")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax = axes[1]
        for variant in baseline_variants:
            vals = [r["l10h9_anchor_mass"] for r in rows if r["variant"] == variant]
            if vals:
                ax.scatter(
                    [baseline_x[variant]],
                    [float(np.mean(vals))],
                    s=80,
                    color=colors[variant],
                    label=variant,
                )
        for variant in ["ln_all", "k_only", "v_only"]:
            means = []
            for alpha in ALPHAS:
                vals = [r["l10h9_anchor_mass"] for r in rows if r["variant"] == variant and r["alpha"] == alpha]
                means.append(float(np.mean(vals)))
            ax.plot(ALPHAS, means, "o-", color=colors[variant], label=variant, markersize=4)
        ax.set_title("Aggregate L10H9 anchor mass")
        ax.set_xlabel("alpha")
        ax.set_ylabel("anchor mass")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc="upper center", ncol=6, frameon=False)
        fig.tight_layout(rect=[0, 0, 1, 0.92])
        fig.savefig(output_dir / "jump_to_contact_pattern_bridge.png", bbox_inches="tight")
        plt.close(fig)

    md_lines = [
        "# jump_to Contact-Pattern Bridge",
        "",
        "Recreates the `contact_pattern_v2` clean/corrupt masked setup for `2B61A` and `1PVGA`,",
        "then compares corrupt-head patching against masked-setup top-3 anchor suppression.",
        "",
        "## Protein Setup",
        "",
        "| Protein | Contact pair | Clean flank | Corrupt flank | Clean anchors | Corrupt anchors |",
        "|---------|--------------|-------------|---------------|---------------|-----------------|",
    ]
    for meta in protein_meta:
        md_lines.append(
            f"| {meta['protein']} | {tuple(meta['contact_pair'])} | {meta['clean_flank']} | {meta['corrupt_flank']} "
            f"| {meta['clean_anchor_positions']} | {meta['corrupt_anchor_positions']} |"
        )

    if len(proteins) <= 6:
        for protein in proteins:
            md_lines.extend([
                "",
                f"## {protein}",
                "",
                "| Variant | Alpha | Segment metric | Faithfulness | Anchor mass | Top-1 mass | Entropy norm | Top-3 mass |",
                "|---------|------:|---------------:|-------------:|------------:|-----------:|-------------:|-----------:|",
            ])
            prot_rows = [r for r in rows if r["protein"] == protein]
            order = {"clean_baseline": 0, "corrupt_baseline": 1, "corrupt_head_patch": 2, "ln_all": 3, "k_only": 4, "v_only": 5}
            prot_rows.sort(key=lambda r: (order[r["variant"]], -1 if np.isnan(r["alpha"]) else r["alpha"]))
            for r in prot_rows:
                alpha_str = "—" if np.isnan(r["alpha"]) else f"{r['alpha']:.1f}"
                md_lines.append(
                    f"| {r['variant']} | {alpha_str} | {r['segment_metric']:.4f} | {r['faithfulness']:.4f} | "
                    f"{r['l10h9_anchor_mass']:.4f} | {r['l10h9_top1_mass']:.4f} | "
                    f"{r['l10h9_entropy_norm']:.4f} | {r['l10h9_top3_mass']:.4f} |"
                )
    else:
        md_lines.extend([
            "",
            "## Aggregate Summary",
            "",
            "| Variant | Alpha | Mean metric | Mean faithfulness | Mean anchor mass | Mean top-1 mass | Mean entropy norm | Mean top-3 mass |",
            "|---------|------:|------------:|------------------:|-----------------:|----------------:|------------------:|----------------:|",
        ])
        order = {"clean_baseline": 0, "corrupt_baseline": 1, "corrupt_head_patch": 2, "ln_all": 3, "k_only": 4, "v_only": 5}
        keys = []
        seen = set()
        for r in rows:
            alpha_key = None if np.isnan(r["alpha"]) else float(r["alpha"])
            key = (r["variant"], alpha_key)
            if key not in seen:
                seen.add(key)
                keys.append(key)
        keys.sort(key=lambda x: (order[x[0]], -1 if x[1] is None else x[1]))
        for variant, alpha in keys:
            sub = [
                r for r in rows
                if r["variant"] == variant and ((alpha is None and np.isnan(r["alpha"])) or r["alpha"] == alpha)
            ]
            alpha_str = "—" if alpha is None else f"{alpha:.1f}"
            md_lines.append(
                f"| {variant} | {alpha_str} | "
                f"{np.mean([r['segment_metric'] for r in sub]):.4f} | "
                f"{np.mean([r['faithfulness'] for r in sub]):.4f} | "
                f"{np.mean([r['l10h9_anchor_mass'] for r in sub]):.4f} | "
                f"{np.mean([r['l10h9_top1_mass'] for r in sub]):.4f} | "
                f"{np.mean([r['l10h9_entropy_norm'] for r in sub]):.4f} | "
                f"{np.mean([r['l10h9_top3_mass'] for r in sub]):.4f} |"
            )

    with open(md_path, "w") as f:
        f.write("\n".join(md_lines))


def main():
    parser = argparse.ArgumentParser(description="Compare contact-pattern corrupt patching and anchor steering in the masked jump_to setup")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--all-config-proteins", action="store_true")
    parser.add_argument("--exclude-proteins", nargs="*", default=[])
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)
    with open(PROTEINS_CFG) as f:
        all_cfg_proteins = list(json.load(f).keys())

    if args.all_config_proteins:
        proteins = [p for p in all_cfg_proteins if p not in set(args.exclude_proteins)]
    else:
        proteins = args.proteins

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)

    qk_weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    v_weights = extract_value_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    ref_seq = seq_dict[REFERENCE_PROTEIN]
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    search_dir = compute_search_dir(model, tokenizer, ref_seq, qk_weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)
    head_dirs = compute_head_space_dirs(qk_weights, v_weights, d_unit, args.device)

    all_rows = []
    protein_meta = []

    for protein in proteins:
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])
        clean_seq = mask_with_flanks(sequence, seg, cfg["clean_flank"])
        corrupt_seq = mask_with_flanks(sequence, seg, cfg["corrupt_flank"])

        print(f"Processing {protein}...")
        orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence, args.device)
        clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_seq, args.device)
        corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq, args.device)
        clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, seg)
        corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)

        clean_attn, clean_inputs = cache_attention_all_layers(model, tokenizer, clean_seq, args.device)
        corrupt_attn, _ = cache_attention_all_layers(model, tokenizer, corrupt_seq, args.device)
        clean_anchor_positions = identify_anchors(model, tokenizer, clean_seq, args.device, top_k=3)
        corrupt_anchor_positions = identify_anchors(model, tokenizer, corrupt_seq, args.device, top_k=3)

        protein_meta.append({
            "protein": protein,
            "contact_pair": cfg["contact_pair"],
            "segment_radius": cfg["segment_radius"],
            "clean_flank": cfg["clean_flank"],
            "corrupt_flank": cfg["corrupt_flank"],
            "clean_anchor_positions": clean_anchor_positions,
            "corrupt_anchor_positions": corrupt_anchor_positions,
            "clean_metric": clean_metric,
            "corrupt_metric": corrupt_metric,
        })

        all_rows.append(summarize_variant(
            protein=protein,
            variant="clean_baseline",
            base_setup="clean",
            alpha=None,
            anchor_positions=clean_anchor_positions,
            metric=clean_metric,
            clean_metric=clean_metric,
            corrupt_metric=corrupt_metric,
            attn_LBHLL=clean_attn,
        ))
        all_rows.append(summarize_variant(
            protein=protein,
            variant="corrupt_baseline",
            base_setup="corrupt",
            alpha=None,
            anchor_positions=corrupt_anchor_positions,
            metric=corrupt_metric,
            clean_metric=clean_metric,
            corrupt_metric=corrupt_metric,
            attn_LBHLL=corrupt_attn,
        ))

        corrupt_l10h9_attn = corrupt_attn[TARGET_LAYER][:, TARGET_HEAD, :, :]
        patched_attn, patched_inputs = patch_corrupt_l10h9_into_clean(
            model=model,
            tokenizer=tokenizer,
            clean_sequence=clean_seq,
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
        patched_metric = patching_metric(patched_contacts, orig_contacts_AA, seg)
        all_rows.append(summarize_variant(
            protein=protein,
            variant="corrupt_head_patch",
            base_setup="clean",
            alpha=None,
            anchor_positions=clean_anchor_positions,
            metric=patched_metric,
            clean_metric=clean_metric,
            corrupt_metric=corrupt_metric,
            attn_LBHLL=patched_attn,
        ))

        for target in TARGETS:
            for alpha in ALPHAS:
                attn_LBHLL, inputs_BL, _ = cache_attention_with_targeted_intervention(
                    model=model,
                    tokenizer=tokenizer,
                    sequence=clean_seq,
                    anchor_positions=clean_anchor_positions,
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
                metric = patching_metric(contacts, orig_contacts_AA, seg)
                all_rows.append(summarize_variant(
                    protein=protein,
                    variant=target,
                    base_setup="clean",
                    alpha=alpha,
                    anchor_positions=clean_anchor_positions,
                    metric=metric,
                    clean_metric=clean_metric,
                    corrupt_metric=corrupt_metric,
                    attn_LBHLL=attn_LBHLL,
                ))

    save_outputs(all_rows, protein_meta, Path(args.output_dir))
    print(f"Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
