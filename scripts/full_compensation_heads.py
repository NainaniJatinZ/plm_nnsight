#!/usr/bin/env python3
"""Audit compensation heads under full-sequence K-only L10H9 ablation.

For selected proteins, compare clean vs K-only ablated attention in `full` and
`flank` contexts. The main question is which heads move toward the original
clean L10H9 anchor pattern in `full` but not in `flank`, i.e. candidate
compensation heads.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
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
    EXPERIMENT_ROOT,
    NUM_HEADS,
    NUM_LAYERS,
    TARGET_HEAD,
    TARGET_LAYER,
    compute_contacts_from_attention,
    compute_search_dir,
    extract_head_weights,
    identify_anchors,
    load_model,
)
from scripts.contact_pattern_full_vs_flank import (
    ContactSegment,
    load_protein_cfg,
    mask_with_flanks,
    compute_contact_map,
    patching_metric,
)
from scripts.qkv_decomposition import (
    compute_head_space_dirs,
    extract_value_head_weights,
    cache_attention_with_targeted_intervention,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "full_compensation_heads"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
ALPHAS_TO_CHECK = [2.0, 4.0]
KNOWN_ANCHOR_HEADS = {(10, 9), (11, 16), (14, 9)}


def mean_key_distribution(attn_LBHLL: list[torch.Tensor], layer: int, head: int) -> np.ndarray:
    attn_AA = attn_LBHLL[layer][0, head, 1:-1, 1:-1].numpy()
    return attn_AA.mean(axis=0)


def top3_mass_from_keydist(keydist: np.ndarray) -> float:
    return float(np.sort(keydist)[::-1][: min(3, len(keydist))].sum())


def entropy_norm_from_keydist(keydist: np.ndarray) -> float:
    total = float(keydist.sum())
    if total <= 0:
        return float("nan")
    p = keydist / total
    p = p[p > 0]
    ent = -float(np.sum(p * np.log2(p)))
    max_ent = math.log2(len(keydist)) if len(keydist) > 1 else 0.0
    return ent / max_ent if max_ent > 0 else float("nan")


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na <= 1e-12 or nb <= 1e-12:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


def jsd(p: np.ndarray, q: np.ndarray) -> float:
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    p = p / max(float(p.sum()), 1e-12)
    q = q / max(float(q.sum()), 1e-12)
    m = 0.5 * (p + q)
    def kl(a, b):
        mask = a > 0
        return float(np.sum(a[mask] * (np.log(a[mask] + 1e-12) - np.log(b[mask] + 1e-12))))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def save_csv(rows: list[dict], path: Path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_report(rows: list[dict], protein_meta: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)
    save_csv(rows, output_dir / "full_compensation_heads.csv")
    with open(output_dir / "full_compensation_heads_meta.json", "w") as f:
        json.dump(protein_meta, f, indent=2)

    summary = {}
    for meta in protein_meta:
        protein = meta["protein"]
        summary[protein] = {}
        for alpha in ALPHAS_TO_CHECK:
            sub = [r for r in rows if r["protein"] == protein and r["alpha"] == alpha]
            full_sub = [r for r in sub if r["context"] == "full" and (r["layer"], r["head"]) != (TARGET_LAYER, TARGET_HEAD)]
            flank_sub = { (r["layer"], r["head"]): r for r in sub if r["context"] == "flank" and (r["layer"], r["head"]) != (TARGET_LAYER, TARGET_HEAD) }

            by_gap_anchor = sorted(
                full_sub,
                key=lambda r: r["delta_anchor_mass_to_clean_l10h9_top3"] - flank_sub[(r["layer"], r["head"])]["delta_anchor_mass_to_clean_l10h9_top3"],
                reverse=True,
            )
            by_gap_cos = sorted(
                full_sub,
                key=lambda r: r["delta_cos_to_clean_l10h9"] - flank_sub[(r["layer"], r["head"])]["delta_cos_to_clean_l10h9"],
                reverse=True,
            )
            summary[protein][f"alpha_{alpha:g}"] = {
                "top_full_minus_flank_anchor_gain": [
                    {
                        "head": f"L{r['layer']}H{r['head']}",
                        "full_anchor_gain": r["delta_anchor_mass_to_clean_l10h9_top3"],
                        "flank_anchor_gain": flank_sub[(r["layer"], r["head"])]["delta_anchor_mass_to_clean_l10h9_top3"],
                        "full_cos_gain": r["delta_cos_to_clean_l10h9"],
                        "flank_cos_gain": flank_sub[(r["layer"], r["head"])]["delta_cos_to_clean_l10h9"],
                        "clean_top3_mass_full": r["clean_top3_mass"],
                        "is_known_anchor_head": r["is_known_anchor_head"],
                    }
                    for r in by_gap_anchor[:10]
                ],
                "top_full_minus_flank_cos_gain": [
                    {
                        "head": f"L{r['layer']}H{r['head']}",
                        "full_anchor_gain": r["delta_anchor_mass_to_clean_l10h9_top3"],
                        "flank_anchor_gain": flank_sub[(r["layer"], r["head"])]["delta_anchor_mass_to_clean_l10h9_top3"],
                        "full_cos_gain": r["delta_cos_to_clean_l10h9"],
                        "flank_cos_gain": flank_sub[(r["layer"], r["head"])]["delta_cos_to_clean_l10h9"],
                        "clean_top3_mass_full": r["clean_top3_mass"],
                        "is_known_anchor_head": r["is_known_anchor_head"],
                    }
                    for r in by_gap_cos[:10]
                ],
            }

    with open(output_dir / "full_compensation_heads_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plt.rcParams.update({"font.size": 9, "figure.dpi": 200})
    fig, axes = plt.subplots(len(protein_meta), len(ALPHAS_TO_CHECK), figsize=(5.5 * len(ALPHAS_TO_CHECK), 3.8 * len(protein_meta)))
    if len(protein_meta) == 1:
        axes = np.array([axes])
    if len(ALPHAS_TO_CHECK) == 1:
        axes = axes[:, None]

    for i, meta in enumerate(protein_meta):
        protein = meta["protein"]
        for j, alpha in enumerate(ALPHAS_TO_CHECK):
            ax = axes[i, j]
            sub = [r for r in rows if r["protein"] == protein and r["alpha"] == alpha and r["context"] == "full" and (r["layer"], r["head"]) != (TARGET_LAYER, TARGET_HEAD)]
            flank_sub = { (r["layer"], r["head"]): r for r in rows if r["protein"] == protein and r["alpha"] == alpha and r["context"] == "flank" and (r["layer"], r["head"]) != (TARGET_LAYER, TARGET_HEAD) }
            scored = []
            for r in sub:
                key = (r["layer"], r["head"])
                gap = r["delta_anchor_mass_to_clean_l10h9_top3"] - flank_sub[key]["delta_anchor_mass_to_clean_l10h9_top3"]
                scored.append((f"L{r['layer']}H{r['head']}", gap, r["is_known_anchor_head"]))
            scored.sort(key=lambda x: x[1], reverse=True)
            top = scored[:8]
            labels = [x[0] for x in top]
            vals = [x[1] for x in top]
            colors = ["#c1121f" if x[2] else "#1d3557" for x in top]
            ax.bar(range(len(top)), vals, color=colors)
            ax.set_xticks(range(len(top)))
            ax.set_xticklabels(labels, rotation=45, ha="right")
            ax.set_ylabel("full - flank anchor gain")
            ax.set_title(f"{protein}, alpha={alpha:g}")
            ax.axhline(0.0, color="gray", lw=0.8, ls=":")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "full_compensation_heads.png", bbox_inches="tight")
    plt.close(fig)

    md = [
        "# Full Compensation Heads",
        "",
        "Under full-sequence `K-only` L10H9 ablation, which other heads move toward the original clean L10H9 anchor pattern,",
        "and do they do so more in `full` than in `flank`?",
        "",
        "Known prior anchor-head shortlist: `L10H9`, `L11H16`, `L14H9`.",
        "",
    ]
    for meta in protein_meta:
        protein = meta["protein"]
        md.extend([
            f"## {protein}",
            "",
            f"- Full clean anchors: {meta['full_anchor_positions']}",
            f"- Flank clean anchors: {meta['flank_anchor_positions']}",
            f"- Full baseline metric: {meta['full_metric']:.4f}",
            f"- Flank baseline metric: {meta['flank_metric']:.4f}",
            "",
        ])
        for alpha in ALPHAS_TO_CHECK:
            key = f"alpha_{alpha:g}"
            md.extend([
                f"### alpha={alpha:g}",
                "",
                "| Rank | Head | full d(anchor) | flank d(anchor) | full d(cos) | flank d(cos) | clean top3 full | prior anchor head |",
                "|-----:|------|---------------:|----------------:|------------:|-------------:|----------------:|------------------:|",
            ])
            for rank, item in enumerate(summary[protein][key]["top_full_minus_flank_anchor_gain"], start=1):
                md.append(
                    f"| {rank} | {item['head']} | {item['full_anchor_gain']:.4f} | {item['flank_anchor_gain']:.4f} | "
                    f"{item['full_cos_gain']:.4f} | {item['flank_cos_gain']:.4f} | {item['clean_top3_mass_full']:.4f} | "
                    f"{'yes' if item['is_known_anchor_head'] else 'no'} |"
                )
            md.append("")
    with open(output_dir / "full_compensation_heads.md", "w") as f:
        f.write("\n".join(md))


def main():
    parser = argparse.ArgumentParser(description="Find compensation heads under full-sequence K-only L10H9 ablation")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
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

        orig_contacts = compute_contact_map(esm_model, tokenizer, full_seq, args.device)

        contexts = []
        for context_name, seq in [("full", full_seq), ("flank", flank_seq)]:
            clean_attn, clean_inputs, _ = cache_attention_with_targeted_intervention(
                model=model,
                tokenizer=tokenizer,
                sequence=seq,
                anchor_positions=[],
                d_unit=d_unit,
                alpha=0.0,
                device=args.device,
                target="k_only",
                head_dirs=head_dirs,
            )
            anchors = identify_anchors(model, tokenizer, seq, args.device, top_k=3)
            baseline_contacts = compute_contacts_from_attention(
                clean_attn,
                clean_inputs["input_ids"],
                clean_inputs["attention_mask"],
                contact_head,
                args.device,
            )[0].detach().cpu()
            baseline_metric = patching_metric(baseline_contacts, orig_contacts, seg)
            contexts.append((context_name, seq, anchors, clean_attn, baseline_metric))

        protein_meta.append({
            "protein": protein,
            "full_anchor_positions": contexts[0][2],
            "flank_anchor_positions": contexts[1][2],
            "full_metric": contexts[0][4],
            "flank_metric": contexts[1][4],
        })

        full_l10h9_clean = mean_key_distribution(contexts[0][3], TARGET_LAYER, TARGET_HEAD)
        full_l10h9_clean_top3 = np.argsort(-full_l10h9_clean)[:3].tolist()

        for alpha in ALPHAS_TO_CHECK:
            for context_name, seq, anchors, clean_attn, baseline_metric in contexts:
                ablated_attn, inputs_BL, _ = cache_attention_with_targeted_intervention(
                    model=model,
                    tokenizer=tokenizer,
                    sequence=seq,
                    anchor_positions=anchors,
                    d_unit=d_unit,
                    alpha=alpha,
                    device=args.device,
                    target="k_only",
                    head_dirs=head_dirs,
                )
                contacts = compute_contacts_from_attention(
                    ablated_attn,
                    inputs_BL["input_ids"],
                    inputs_BL["attention_mask"],
                    contact_head,
                    args.device,
                )[0].detach().cpu()
                metric = patching_metric(contacts, orig_contacts, seg)

                for layer in range(NUM_LAYERS):
                    for head in range(NUM_HEADS):
                        clean_keydist = mean_key_distribution(clean_attn, layer, head)
                        ablated_keydist = mean_key_distribution(ablated_attn, layer, head)
                        row = {
                            "protein": protein,
                            "context": context_name,
                            "alpha": alpha,
                            "layer": layer,
                            "head": head,
                            "label": f"L{layer}H{head}",
                            "context_metric": metric,
                            "delta_metric_from_context_baseline": metric - baseline_metric,
                            "clean_top3_mass": top3_mass_from_keydist(clean_keydist),
                            "ablated_top3_mass": top3_mass_from_keydist(ablated_keydist),
                            "delta_top3_mass": top3_mass_from_keydist(ablated_keydist) - top3_mass_from_keydist(clean_keydist),
                            "clean_entropy_norm": entropy_norm_from_keydist(clean_keydist),
                            "ablated_entropy_norm": entropy_norm_from_keydist(ablated_keydist),
                            "clean_cos_to_clean_l10h9": cosine(clean_keydist, full_l10h9_clean),
                            "ablated_cos_to_clean_l10h9": cosine(ablated_keydist, full_l10h9_clean),
                            "delta_cos_to_clean_l10h9": cosine(ablated_keydist, full_l10h9_clean) - cosine(clean_keydist, full_l10h9_clean),
                            "clean_anchor_mass_to_clean_l10h9_top3": float(clean_keydist[full_l10h9_clean_top3].sum()),
                            "ablated_anchor_mass_to_clean_l10h9_top3": float(ablated_keydist[full_l10h9_clean_top3].sum()),
                            "delta_anchor_mass_to_clean_l10h9_top3": float(ablated_keydist[full_l10h9_clean_top3].sum() - clean_keydist[full_l10h9_clean_top3].sum()),
                            "keydist_jsd": jsd(clean_keydist, ablated_keydist),
                            "is_known_anchor_head": (layer, head) in KNOWN_ANCHOR_HEADS,
                        }
                        rows.append(row)

    build_report(rows, protein_meta, Path(args.output_dir))
    print(f"Saved outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
