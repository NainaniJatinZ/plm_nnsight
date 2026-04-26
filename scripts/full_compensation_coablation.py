#!/usr/bin/env python3
"""Full-sequence multi-head co-suppression for the compensation hypothesis.

Candidate backup heads are suppressed with head-specific K-only interventions:
  - per head, choose the smallest anchor set covering 50% mean-key mass
  - ignore heads needing more than `max_anchors`
  - suppress each head at its own anchors along its own mean query direction

Primary readout is the `contact_pattern_v2` segment-level metric on full sequence.
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
    load_protein_cfg,
    compute_contact_map,
    patching_metric,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "full_compensation_coablation"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
ALPHAS = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0]
HEAD_CANDIDATES = [(10, 9), (11, 16), (11, 14), (14, 9)]
HEAD_LABELS = {h: f"L{h[0]}H{h[1]}" for h in HEAD_CANDIDATES}
COMBOS = [
    ("L10H9", [(10, 9)]),
    ("L11H16", [(11, 16)]),
    ("L11H14", [(11, 14)]),
    ("L14H9", [(14, 9)]),
    ("L10H9+L11H16", [(10, 9), (11, 16)]),
    ("L10H9+L11H16+L11H14", [(10, 9), (11, 16), (11, 14)]),
    ("L10H9+L11H16+L11H14+L14H9", [(10, 9), (11, 16), (11, 14), (14, 9)]),
]


def extract_multihead_q_weights(model, candidates: list[tuple[int, int]]) -> dict[tuple[int, int], dict]:
    weights = {}
    for layer, head in candidates:
        attn = model._model.esm.encoder.layer[layer].attention
        w_q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
        b_q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
        w_k = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
        b_k = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
        weights[(layer, head)] = {
            "W_Q_hd": w_q[head].clone(),
            "b_Q_d": b_q[head].clone(),
            "W_K_hd": w_k[head].clone(),
            "b_K_d": b_k[head].clone(),
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
    return inputs_BL, attn_by_layer, ln_by_layer


def compute_head_spec(
    attn_by_layer: dict[int, torch.Tensor],
    ln_by_layer: dict[int, torch.Tensor],
    q_weights: dict[tuple[int, int], dict],
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
    w = q_weights[(layer, head)]
    q_all = x_ln @ w["W_Q_hd"].T + w["b_Q_d"]
    q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    d_hidden = w["W_K_hd"].T @ q_mean_norm
    d_hidden = d_hidden / d_hidden.norm().clamp(min=1e-8)
    k_dir = w["W_K_hd"] @ d_hidden
    k_dir = k_dir / k_dir.norm().clamp(min=1e-8)

    p = key_mass / max(total, 1e-12)
    p_pos = p[p > 0]
    ent = -float(np.sum(p_pos * np.log2(p_pos))) if len(p_pos) else float("nan")
    max_ent = math.log2(len(key_mass)) if len(key_mass) > 1 else 0.0

    return {
        "layer": layer,
        "head": head,
        "label": HEAD_LABELS[(layer, head)],
        "passed_vertical": passed,
        "keys50": needed,
        "anchor_positions": anchors,
        "top1_mass": float(key_mass[ranked[0]]) if len(ranked) else float("nan"),
        "top3_mass": float(key_mass[ranked[: min(3, len(ranked))]].sum()),
        "entropy_norm": ent / max_ent if max_ent > 0 and not np.isnan(ent) else float("nan"),
        "key_dir_head": k_dir.cpu(),
    }


@torch.no_grad()
def cache_attention_with_multihead_k_suppression(
    model,
    tokenizer,
    sequence: str,
    active_specs: list[dict],
    alpha: float,
    device: str,
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
                    key_module = model.esm.encoder.layer[layer].attention.self.key
                    key_out = key_module.output
                    for spec in specs_by_layer[layer]:
                        head = spec["head"]
                        start = head * HEAD_DIM
                        end = (head + 1) * HEAD_DIM
                        dir_hd = spec["key_dir_head"].to(device)
                        for pos in spec["anchor_positions"]:
                            tok_idx = pos + 1
                            key_out[:, tok_idx, start:end] = key_out[:, tok_idx, start:end] - alpha * dir_hd
                    key_module.output = key_out

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


def build_outputs(rows: list[dict], head_meta: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    save_csv(rows, output_dir / "full_compensation_coablation.csv")
    with open(output_dir / "full_compensation_coablation_head_meta.json", "w") as f:
        json.dump(head_meta, f, indent=2)

    summary = {}
    for protein in sorted({r["protein"] for r in rows}):
        summary[protein] = {}
        for combo_name, _ in COMBOS:
            sub = [r for r in rows if r["protein"] == protein and r["combo"] == combo_name]
            summary[protein][combo_name] = {
                "alphas": ALPHAS,
                "segment_metric_mean": [float(np.mean([r["segment_metric"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "delta_from_baseline_mean": [float(np.mean([r["delta_from_baseline"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
                "n_active_heads": [int(np.mean([r["n_active_heads"] for r in sub if r["alpha"] == a])) for a in ALPHAS],
            }
    with open(output_dir / "full_compensation_coablation_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plt.rcParams.update({"font.size": 9, "figure.dpi": 200})
    proteins = sorted({r["protein"] for r in rows})
    fig, axes = plt.subplots(len(proteins), 1, figsize=(8, 3.6 * len(proteins)))
    if len(proteins) == 1:
        axes = [axes]
    colors = ["#1d3557", "#457b9d", "#2a9d8f", "#8d99ae", "#e9c46a", "#f4a261", "#e76f51"]
    for ax, protein in zip(axes, proteins):
        for color, (combo_name, _) in zip(colors, COMBOS):
            sub = [r for r in rows if r["protein"] == protein and r["combo"] == combo_name]
            xs = ALPHAS
            ys = [float(np.mean([r["segment_metric"] for r in sub if r["alpha"] == a])) for a in xs]
            ax.plot(xs, ys, "o-", color=color, label=combo_name, markersize=4)
        ax.set_title(f"{protein}: full-sequence contact-pattern metric")
        ax.set_xlabel("alpha")
        ax.set_ylabel("segment metric")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(output_dir / "full_compensation_coablation.png", bbox_inches="tight")
    plt.close(fig)

    md = [
        "# Full Compensation Coablation",
        "",
        "Full-sequence co-suppression of candidate compensation heads using head-specific K-only interventions.",
        f"Anchor rule: smallest set covering 50% mass, ignored if more than 7 anchors.",
        "",
    ]
    by_protein_meta: dict[str, list[dict]] = defaultdict(list)
    for item in head_meta:
        by_protein_meta[item["protein"]].append(item)
    for protein in proteins:
        md.extend([
            f"## {protein}",
            "",
            "| Head | Passed | keys50 | top1_mass | top3_mass | entropy_norm | anchors |",
            "|------|--------|-------:|----------:|----------:|-------------:|---------|",
        ])
        for item in sorted(by_protein_meta[protein], key=lambda x: (x["layer"], x["head"])):
            md.append(
                f"| {item['label']} | {'yes' if item['passed_vertical'] else 'no'} | {item['keys50']} | "
                f"{item['top1_mass']:.4f} | {item['top3_mass']:.4f} | {item['entropy_norm']:.4f} | {item['anchor_positions']} |"
            )
        md.append("")
        md.extend([
            "| Combo | Alpha | Segment metric | Delta vs baseline | Active heads | Active head labels |",
            "|-------|------:|---------------:|------------------:|-------------:|--------------------|",
        ])
        prot_rows = [r for r in rows if r["protein"] == protein]
        order = {name: i for i, (name, _) in enumerate(COMBOS)}
        prot_rows.sort(key=lambda r: (order[r["combo"]], r["alpha"]))
        for r in prot_rows:
            md.append(
                f"| {r['combo']} | {r['alpha']:.1f} | {r['segment_metric']:.4f} | {r['delta_from_baseline']:.4f} | "
                f"{r['n_active_heads']} | {r['active_head_labels']} |"
            )
        md.append("")
    with open(output_dir / "full_compensation_coablation.md", "w") as f:
        f.write("\n".join(md))


def main():
    parser = argparse.ArgumentParser(description="Co-suppress candidate compensation heads in full sequence")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--mass-threshold", type=float, default=0.5)
    parser.add_argument("--max-anchors", type=int, default=7)
    args = parser.parse_args()

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    q_weights = extract_multihead_q_weights(model, HEAD_CANDIDATES)

    rows = []
    head_meta = []

    for protein in args.proteins:
        print(f"Processing {protein}...")
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])

        orig_contacts = compute_contact_map(esm_model, tokenizer, sequence, args.device)
        baseline_metric = patching_metric(orig_contacts, orig_contacts, seg)

        target_layers = sorted({layer for layer, _ in HEAD_CANDIDATES})
        _, attn_by_layer, ln_by_layer = capture_clean_context(model, tokenizer, sequence, target_layers, args.device)

        specs_by_head = {}
        for layer, head in HEAD_CANDIDATES:
            spec = compute_head_spec(
                attn_by_layer=attn_by_layer,
                ln_by_layer=ln_by_layer,
                q_weights=q_weights,
                layer=layer,
                head=head,
                mass_threshold=args.mass_threshold,
                max_anchors=args.max_anchors,
            )
            specs_by_head[(layer, head)] = spec
            head_meta.append({
                "protein": protein,
                **{k: v for k, v in spec.items() if k != "key_dir_head"},
            })

        for combo_name, combo_heads in COMBOS:
            active_specs = [specs_by_head[h] for h in combo_heads if specs_by_head[h]["passed_vertical"]]
            active_labels = [spec["label"] for spec in active_specs]
            for alpha in ALPHAS:
                attn_LBHLL, inputs_BL = cache_attention_with_multihead_k_suppression(
                    model=model,
                    tokenizer=tokenizer,
                    sequence=sequence,
                    active_specs=active_specs,
                    alpha=alpha,
                    device=args.device,
                )
                pred_contacts = compute_contacts_from_attention(
                    attn_LBHLL,
                    inputs_BL["input_ids"],
                    inputs_BL["attention_mask"],
                    contact_head,
                    args.device,
                )[0].detach().cpu()
                metric = patching_metric(pred_contacts, orig_contacts, seg)
                rows.append({
                    "protein": protein,
                    "combo": combo_name,
                    "alpha": alpha,
                    "segment_metric": metric,
                    "delta_from_baseline": metric - baseline_metric,
                    "n_active_heads": len(active_specs),
                    "active_head_labels": str(active_labels),
                })

    build_outputs(rows, head_meta, Path(args.output_dir))
    print(f"Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
