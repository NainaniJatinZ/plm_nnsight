#!/usr/bin/env python3
"""Full-sequence co-suppression of all passing anchor-like heads in L11-L15.

For each protein:
  - scan every head in layers 11..15
  - identify anchor-like heads using the smallest anchor set covering 50% key mass
  - ignore heads requiring more than `max_anchors`
  - co-suppress all passing heads together under three intervention modes:
      * k_only: edit only each head's key output
      * v_only: edit only each head's value output
      * ln_all: edit the shared LayerNorm input using summed head-specific directions

Primary readout is the `contact_pattern_v2` full-sequence segment metric.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.anchor_contact_steering import (
    EXPERIMENT_ROOT,
    HEAD_DIM,
    HIDDEN_DIM,
    NUM_HEADS,
    NUM_LAYERS,
    compute_contacts_from_attention,
    load_model,
)
from scripts.contact_pattern_full_vs_flank import (
    ContactSegment,
    compute_contact_map,
    load_protein_cfg,
    patching_metric,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "full_compensation_multimode"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
ALPHAS = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0]
MODES = ["k_only", "v_only", "ln_all"]
LAYER_RANGE = list(range(11, 16))
PRIMARY_HEAD = (10, 9)
HEAD_CANDIDATES = [(layer, head) for layer in LAYER_RANGE for head in range(NUM_HEADS)]


def head_label(layer: int, head: int) -> str:
    return f"L{layer}H{head}"


def extract_multihead_weights(model, candidates: list[tuple[int, int]]) -> dict[tuple[int, int], dict]:
    weights = {}
    for layer, head in candidates:
        attn = model._model.esm.encoder.layer[layer].attention
        w_q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
        b_q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
        w_k = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
        b_k = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
        w_v = attn.self.value.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
        b_v = attn.self.value.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
        weights[(layer, head)] = {
            "W_Q_hd": w_q[head].clone(),
            "b_Q_d": b_q[head].clone(),
            "W_K_hd": w_k[head].clone(),
            "b_K_d": b_k[head].clone(),
            "W_V_hd": w_v[head].clone(),
            "b_V_d": b_v[head].clone(),
        }
    return weights


@torch.no_grad()
def capture_clean_context(model, tokenizer, sequence: str, layers: list[int], device: str):
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[layer].attention.self for layer in layers]
    ln_modules = [model.esm.encoder.layer[layer].attention.LayerNorm for layer in layers]
    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)
            ln_cache = tracer.cache(modules=ln_modules)

    attn_by_layer = {}
    ln_by_layer = {}
    for layer in layers:
        attn_key = f"model.esm.encoder.layer.{layer}.attention.self"
        ln_key = f"model.esm.encoder.layer.{layer}.attention.LayerNorm"
        attn_by_layer[layer] = attn_cache[attn_key].output[1].detach().cpu()[0]
        ln_by_layer[layer] = ln_cache[ln_key].output.detach().cpu()[0]
    return attn_by_layer, ln_by_layer


def compute_head_spec(
    attn_by_layer: dict[int, torch.Tensor],
    ln_by_layer: dict[int, torch.Tensor],
    weights: dict[tuple[int, int], dict],
    layer: int,
    head: int,
    mass_threshold: float,
    max_anchors: int,
) -> dict:
    attn_AA = attn_by_layer[layer][head, 1:-1, 1:-1].numpy()
    key_mass = attn_AA.mean(axis=0)
    ranked = np.argsort(-key_mass)
    cumsum = np.cumsum(key_mass[ranked])
    total = float(key_mass.sum())
    needed = int(np.searchsorted(cumsum, total * mass_threshold) + 1) if total > 0 else len(key_mass)
    anchors = ranked[:needed].tolist()
    passed = needed <= max_anchors

    x_ln = ln_by_layer[layer][1:-1]
    w = weights[(layer, head)]
    q_all = x_ln @ w["W_Q_hd"].T + w["b_Q_d"]
    q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)

    ln_dir = w["W_K_hd"].T @ q_mean_norm
    ln_dir = ln_dir / ln_dir.norm().clamp(min=1e-8)
    k_dir = w["W_K_hd"] @ ln_dir
    k_dir = k_dir / k_dir.norm().clamp(min=1e-8)
    v_dir = w["W_V_hd"] @ ln_dir
    v_dir = v_dir / v_dir.norm().clamp(min=1e-8)

    p = key_mass / max(total, 1e-12)
    p_pos = p[p > 0]
    ent = -float(np.sum(p_pos * np.log2(p_pos))) if len(p_pos) else float("nan")
    max_ent = math.log2(len(key_mass)) if len(key_mass) > 1 else 0.0

    return {
        "layer": layer,
        "head": head,
        "label": head_label(layer, head),
        "passed_vertical": passed,
        "keys50": needed,
        "anchor_positions": anchors,
        "top1_mass": float(key_mass[ranked[0]]) if len(ranked) else float("nan"),
        "top3_mass": float(key_mass[ranked[: min(3, len(ranked))]].sum()),
        "entropy_norm": ent / max_ent if max_ent > 0 and not np.isnan(ent) else float("nan"),
        "ln_dir_hidden": ln_dir.cpu(),
        "k_only_dir_head": k_dir.cpu(),
        "v_only_dir_head": v_dir.cpu(),
    }


@torch.no_grad()
def cache_attention_with_multimode_suppression(
    model,
    tokenizer,
    sequence: str,
    active_specs: list[dict],
    alpha: float,
    device: str,
    mode: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)

            if alpha != 0.0 and active_specs:
                specs_by_layer: dict[int, list[dict]] = defaultdict(list)
                for spec in active_specs:
                    specs_by_layer[spec["layer"]].append(spec)

                for layer in sorted(specs_by_layer):
                    if mode == "ln_all":
                        ln_module = model.esm.encoder.layer[layer].attention.LayerNorm
                        ln_out = ln_module.output
                        dirs_by_token: dict[int, list[torch.Tensor]] = defaultdict(list)
                        for spec in specs_by_layer[layer]:
                            dir_h = spec["ln_dir_hidden"].to(device)
                            for pos in spec["anchor_positions"]:
                                dirs_by_token[pos + 1].append(dir_h)
                        for tok_idx, dirs in dirs_by_token.items():
                            delta = torch.stack(dirs, dim=0).sum(dim=0)
                            ln_out[:, tok_idx, :] = ln_out[:, tok_idx, :] - alpha * delta
                        ln_module.output = ln_out
                    else:
                        if mode == "k_only":
                            target_module = model.esm.encoder.layer[layer].attention.self.key
                            dir_key = "k_only_dir_head"
                        elif mode == "v_only":
                            target_module = model.esm.encoder.layer[layer].attention.self.value
                            dir_key = "v_only_dir_head"
                        else:
                            raise ValueError(f"Unknown mode: {mode}")

                        target_out = target_module.output
                        for spec in specs_by_layer[layer]:
                            head = spec["head"]
                            start = head * HEAD_DIM
                            end = (head + 1) * HEAD_DIM
                            dir_hd = spec[dir_key].to(device)
                            for pos in spec["anchor_positions"]:
                                tok_idx = pos + 1
                                target_out[:, tok_idx, start:end] = (
                                    target_out[:, tok_idx, start:end] - alpha * dir_hd
                                )
                        target_module.output = target_out

    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_LBHLL, inputs_BL


def save_csv(rows: list[dict], path: Path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compute_multihead_verticality(attn_LBHLL: list[torch.Tensor], active_specs: list[dict]) -> tuple[dict, list[dict]]:
    if not active_specs:
        agg = {
            "mean_anchor_mass": float("nan"),
            "mean_top1_mass": float("nan"),
            "mean_top3_mass": float("nan"),
            "mean_entropy_norm": float("nan"),
            "sum_anchor_mass": 0.0,
            "sum_top3_mass": 0.0,
        }
        return agg, []

    per_head = []
    for spec in active_specs:
        attn_AA = attn_LBHLL[spec["layer"]][0, spec["head"], 1:-1, 1:-1].numpy()
        key_mass = attn_AA.mean(axis=0)
        total_mass = float(key_mass.sum())
        ranked = np.argsort(-key_mass)
        anchor_mass = sum(float(key_mass[p]) for p in spec["anchor_positions"])
        top1_mass = float(key_mass[ranked[0]]) if len(ranked) else float("nan")
        top3_mass = float(key_mass[ranked[: min(3, len(ranked))]].sum()) if len(ranked) else float("nan")
        if total_mass > 0:
            p = key_mass / total_mass
            p = p[p > 0]
            ent = float(-np.sum(p * np.log2(p))) if len(p) else float("nan")
            max_ent = math.log2(len(key_mass)) if len(key_mass) > 1 else 0.0
            entropy_norm = ent / max_ent if max_ent > 0 and not np.isnan(ent) else float("nan")
        else:
            entropy_norm = float("nan")
        per_head.append({
            "layer": spec["layer"],
            "head": spec["head"],
            "label": spec["label"],
            "anchor_mass": anchor_mass,
            "top1_mass": top1_mass,
            "top3_mass": top3_mass,
            "entropy_norm": entropy_norm,
        })

    agg = {
        "mean_anchor_mass": float(np.mean([x["anchor_mass"] for x in per_head])),
        "mean_top1_mass": float(np.mean([x["top1_mass"] for x in per_head])),
        "mean_top3_mass": float(np.mean([x["top3_mass"] for x in per_head])),
        "mean_entropy_norm": float(np.mean([x["entropy_norm"] for x in per_head])),
        "sum_anchor_mass": float(np.sum([x["anchor_mass"] for x in per_head])),
        "sum_top3_mass": float(np.sum([x["top3_mass"] for x in per_head])),
    }
    return agg, per_head


def build_outputs(rows: list[dict], per_head_rows: list[dict], head_meta: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    save_csv(rows, output_dir / "full_compensation_multimode.csv")
    save_csv(per_head_rows, output_dir / "full_compensation_multimode_per_head.csv")
    with open(output_dir / "full_compensation_multimode_head_meta.json", "w") as f:
        json.dump(head_meta, f, indent=2)

    summary = {}
    proteins = sorted({r["protein"] for r in rows})
    for protein in proteins:
        summary[protein] = {}
        for mode in MODES:
            sub = [r for r in rows if r["protein"] == protein and r["mode"] == mode]
            summary[protein][mode] = {
                "alphas": ALPHAS,
                "segment_metric": [float(np.mean([r["segment_metric"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "delta_from_baseline": [float(np.mean([r["delta_from_baseline"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "n_active_heads": [int(np.mean([r["n_active_heads"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "mean_anchor_mass": [float(np.mean([r["mean_anchor_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "mean_top1_mass": [float(np.mean([r["mean_top1_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "mean_top3_mass": [float(np.mean([r["mean_top3_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "mean_entropy_norm": [float(np.mean([r["mean_entropy_norm"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "sum_anchor_mass": [float(np.mean([r["sum_anchor_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
            }
        per_head_summary = {}
        prot_head_rows = [r for r in per_head_rows if r["protein"] == protein]
        for head_label_value in sorted({r["head_label"] for r in prot_head_rows}):
            per_head_summary[head_label_value] = {}
            for mode in MODES:
                sub = [r for r in prot_head_rows if r["head_label"] == head_label_value and r["mode"] == mode]
                per_head_summary[head_label_value][mode] = {
                    "alphas": ALPHAS,
                    "anchor_mass": [float(np.mean([r["anchor_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                    "top1_mass": [float(np.mean([r["top1_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                    "top3_mass": [float(np.mean([r["top3_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                    "entropy_norm": [float(np.mean([r["entropy_norm"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                }
        summary[protein]["per_head"] = per_head_summary
    with open(output_dir / "full_compensation_multimode_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plt.rcParams.update({"font.size": 9, "figure.dpi": 200})
    fig, axes = plt.subplots(len(proteins), 1, figsize=(8, 3.6 * len(proteins)))
    if len(proteins) == 1:
        axes = [axes]
    colors = {"k_only": "#1d3557", "v_only": "#e76f51", "ln_all": "#2a9d8f"}
    labels = {"k_only": "K-only", "v_only": "V-only", "ln_all": "LN-all"}
    for ax, protein in zip(axes, proteins):
        for mode in MODES:
            sub = [r for r in rows if r["protein"] == protein and r["mode"] == mode]
            ys = [float(np.mean([r["segment_metric"] for r in sub if r["alpha"] == a])) for a in ALPHAS]
            ax.plot(ALPHAS, ys, "o-", color=colors[mode], label=labels[mode], markersize=4)
        ax.set_title(f"{protein}: full-sequence L11-L15 co-suppression")
        ax.set_xlabel("alpha")
        ax.set_ylabel("segment metric")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    handles, labels_out = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels_out, loc="upper center", ncol=3, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(output_dir / "full_compensation_multimode.png", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(len(proteins), 2, figsize=(10, 3.6 * len(proteins)))
    if len(proteins) == 1:
        axes = np.array([axes])
    for row_axes, protein in zip(axes, proteins):
        ax_mass, ax_ent = row_axes
        for mode in MODES:
            sub = [r for r in rows if r["protein"] == protein and r["mode"] == mode]
            mass_ys = [float(np.mean([r["mean_anchor_mass"] for r in sub if r["alpha"] == a])) for a in ALPHAS]
            ent_ys = [float(np.mean([r["mean_entropy_norm"] for r in sub if r["alpha"] == a])) for a in ALPHAS]
            ax_mass.plot(ALPHAS, mass_ys, "o-", color=colors[mode], label=labels[mode], markersize=4)
            ax_ent.plot(ALPHAS, ent_ys, "o-", color=colors[mode], label=labels[mode], markersize=4)
        ax_mass.set_title(f"{protein}: mean anchor mass")
        ax_mass.set_xlabel("alpha")
        ax_mass.set_ylabel("mean anchor mass")
        ax_ent.set_title(f"{protein}: mean entropy norm")
        ax_ent.set_xlabel("alpha")
        ax_ent.set_ylabel("mean entropy norm")
        for ax in (ax_mass, ax_ent):
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
    handles, labels_out = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels_out, loc="upper center", ncol=3, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(output_dir / "full_compensation_multimode_verticality.png", bbox_inches="tight")
    plt.close(fig)

    by_protein_meta: dict[str, list[dict]] = defaultdict(list)
    for item in head_meta:
        by_protein_meta[item["protein"]].append(item)

    md = [
        "# Full Compensation Multimode",
        "",
        "Co-suppress all passing anchor-like heads in layers 11-15 on full sequence.",
        "Passing rule: smallest anchor set covering 50% key mass, dropped if more than 7 anchors.",
        "Modes: `k_only`, `v_only`, `ln_all`.",
        "",
    ]
    for protein in proteins:
        passed = [x for x in by_protein_meta[protein] if x["passed_vertical"]]
        md.extend([
            f"## {protein}",
            "",
            f"Passing heads: {len(passed)}",
            "",
            "| Head | keys50 | top1_mass | top3_mass | entropy_norm | anchors |",
            "|------|-------:|----------:|----------:|-------------:|---------|",
        ])
        for item in sorted(passed, key=lambda x: (x["layer"], x["head"])):
            md.append(
                f"| {item['label']} | {item['keys50']} | {item['top1_mass']:.4f} | "
                f"{item['top3_mass']:.4f} | {item['entropy_norm']:.4f} | {item['anchor_positions']} |"
            )
        if not passed:
            md.append("| none | - | - | - | - | - |")
        md.extend([
            "",
            "| Mode | Alpha | Segment metric | Delta vs baseline | Mean anchor mass | Mean entropy norm | Active heads | Active head labels |",
            "|------|------:|---------------:|------------------:|-----------------:|------------------:|-------------:|--------------------|",
        ])
        prot_rows = [r for r in rows if r["protein"] == protein]
        order = {mode: i for i, mode in enumerate(MODES)}
        prot_rows.sort(key=lambda r: (order[r["mode"]], r["alpha"]))
        for r in prot_rows:
            md.append(
                f"| {r['mode']} | {r['alpha']:.1f} | {r['segment_metric']:.4f} | "
                f"{r['delta_from_baseline']:.4f} | {r['mean_anchor_mass']:.4f} | {r['mean_entropy_norm']:.4f} | "
                f"{r['n_active_heads']} | {r['active_head_labels']} |"
            )
        md.append("")
        md.extend([
            "| Head | Mode | Alpha | Anchor mass | Top1 mass | Top3 mass | Entropy norm |",
            "|------|------|------:|------------:|----------:|----------:|-------------:|",
        ])
        prot_head_rows = [r for r in per_head_rows if r["protein"] == protein]
        prot_head_rows.sort(key=lambda r: (r["head_label"], order[r["mode"]], r["alpha"]))
        for r in prot_head_rows:
            md.append(
                f"| {r['head_label']} | {r['mode']} | {r['alpha']:.1f} | {r['anchor_mass']:.4f} | "
                f"{r['top1_mass']:.4f} | {r['top3_mass']:.4f} | {r['entropy_norm']:.4f} |"
            )
        md.append("")
    with open(output_dir / "full_compensation_multimode.md", "w") as f:
        f.write("\n".join(md))


def main():
    parser = argparse.ArgumentParser(description="Co-suppress all passing anchor-like heads in L11-L15")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--mass-threshold", type=float, default=0.5)
    parser.add_argument("--max-anchors", type=int, default=7)
    parser.add_argument(
        "--include-primary-l10h9",
        action="store_true",
        help="Also suppress L10H9 together with the passing anchor-like heads in L11-L15.",
    )
    args = parser.parse_args()

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    all_candidates = list(HEAD_CANDIDATES)
    if args.include_primary_l10h9 and PRIMARY_HEAD not in all_candidates:
        all_candidates = [PRIMARY_HEAD] + all_candidates
    weights = extract_multihead_weights(model, all_candidates)

    rows = []
    per_head_rows = []
    head_meta = []
    target_layers = sorted({layer for layer, _ in all_candidates})

    for protein in args.proteins:
        print(f"Processing {protein}...")
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])

        orig_contacts = compute_contact_map(esm_model, tokenizer, sequence, args.device)
        baseline_metric = patching_metric(orig_contacts, orig_contacts, seg)

        attn_by_layer, ln_by_layer = capture_clean_context(model, tokenizer, sequence, target_layers, args.device)
        specs = []
        for layer, head in all_candidates:
            spec = compute_head_spec(
                attn_by_layer=attn_by_layer,
                ln_by_layer=ln_by_layer,
                weights=weights,
                layer=layer,
                head=head,
                mass_threshold=args.mass_threshold,
                max_anchors=args.max_anchors,
            )
            specs.append(spec)
            head_meta.append({
                "protein": protein,
                **{k: v for k, v in spec.items() if k not in {"ln_dir_hidden", "k_only_dir_head", "v_only_dir_head"}},
            })

        active_specs = [
            spec
            for spec in specs
            if spec["passed_vertical"] and (args.include_primary_l10h9 or (spec["layer"], spec["head"]) != PRIMARY_HEAD)
        ]
        active_labels = [spec["label"] for spec in active_specs]

        for mode in MODES:
            for alpha in ALPHAS:
                attn_LBHLL, inputs_BL = cache_attention_with_multimode_suppression(
                    model=model,
                    tokenizer=tokenizer,
                    sequence=sequence,
                    active_specs=active_specs,
                    alpha=alpha,
                    device=args.device,
                    mode=mode,
                )
                pred_contacts = compute_contacts_from_attention(
                    attn_LBHLL,
                    inputs_BL["input_ids"],
                    inputs_BL["attention_mask"],
                    contact_head,
                    args.device,
                )[0].detach().cpu()
                metric = patching_metric(pred_contacts, orig_contacts, seg)
                agg_metrics, per_head_metrics = compute_multihead_verticality(attn_LBHLL, active_specs)
                rows.append({
                    "protein": protein,
                    "mode": mode,
                    "alpha": alpha,
                    "segment_metric": metric,
                    "delta_from_baseline": metric - baseline_metric,
                    "n_active_heads": len(active_specs),
                    "active_head_labels": str(active_labels),
                    **agg_metrics,
                })
                for head_metrics in per_head_metrics:
                    per_head_rows.append({
                        "protein": protein,
                        "mode": mode,
                        "alpha": alpha,
                        "head_label": head_metrics["label"],
                        "layer": head_metrics["layer"],
                        "head": head_metrics["head"],
                        "anchor_mass": head_metrics["anchor_mass"],
                        "top1_mass": head_metrics["top1_mass"],
                        "top3_mass": head_metrics["top3_mass"],
                        "entropy_norm": head_metrics["entropy_norm"],
                    })

    build_outputs(rows, per_head_rows, head_meta, Path(args.output_dir))
    print(f"Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
