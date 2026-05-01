#!/usr/bin/env python3
"""Path patching from L10H9 into the masked-flank contact circuit.

Implements experiments/4_26_anchor_path_patching.md using the canonical
masked-flank setup from the contact-pattern scripts.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import warnings
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

warnings.filterwarnings(
    "ignore",
    message=r".*has pre-defined a `output` attribute.*",
    category=UserWarning,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.anchor_contact_steering import (
    EXPERIMENT_ROOT,
    HEAD_DIM,
    NUM_HEADS,
    NUM_LAYERS,
    TARGET_HEAD,
    TARGET_LAYER,
    cache_attention_with_steering,
    compute_contacts_from_attention,
    compute_l10h9_head_metrics,
    compute_search_dir,
    extract_head_weights,
    identify_anchors,
    load_model,
)
from scripts.jump_to_contact_pattern_bridge import (
    ContactSegment,
    compute_contact_map,
    faithfulness,
    load_protein_cfg,
    mask_with_flanks,
    patching_metric,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "anchor_path_patching"
DEFAULT_MANIFEST = EXPERIMENT_ROOT / "inputs" / "anchor_path_patching_receiver_manifest.json"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
REFERENCE_PROTEIN = "2B61A"
DEFAULT_ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0, 2.0, 4.0, 6.0, 8.0]
ANCHOR_DROP_THRESHOLD = 0.25
SEGMENT_DROP_THRESHOLD = 0.10


def save_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    fields = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compute_metric_from_attention_stack(
    attn_LBHLL: list[torch.Tensor],
    inputs_BL: dict,
    contact_head,
    orig_contacts_AA: torch.Tensor,
    seg: ContactSegment,
    device: str,
) -> float:
    contacts_AA = compute_contacts_from_attention(
        attn_LBHLL,
        inputs_BL["input_ids"],
        inputs_BL["attention_mask"],
        contact_head,
        device=device,
    )[0].detach().cpu()
    return patching_metric(contacts_AA, orig_contacts_AA, seg)


def load_receiver_manifest(path: Path) -> dict[str, dict]:
    with open(path) as f:
        manifest = json.load(f)
    return manifest["proteins"]


def cache_clean_state(model, tokenizer, sequence: str, device: str) -> dict:
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    value_modules = [model.esm.encoder.layer[i].attention.self.value for i in range(NUM_LAYERS)]

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            cache = tracer.cache(modules=attn_modules + value_modules)

    attn_LBHLL = []
    value_LBLD = []
    head_ctx_LBHLd = []
    full_ctx_LBLD = []
    for layer in range(NUM_LAYERS):
        attn_key = f"model.esm.encoder.layer.{layer}.attention.self"
        value_key = f"model.esm.encoder.layer.{layer}.attention.self.value"
        attn = cache[attn_key].output[1].detach().cpu()
        value = cache[value_key].output.detach().cpu()
        v_heads = value.reshape(value.shape[0], value.shape[1], NUM_HEADS, HEAD_DIM).transpose(1, 2)
        head_ctx = torch.matmul(attn, v_heads)
        full_ctx = head_ctx.transpose(1, 2).contiguous().reshape(value.shape[0], value.shape[1], -1)

        attn_LBHLL.append(attn)
        value_LBLD.append(value)
        head_ctx_LBHLd.append(head_ctx)
        full_ctx_LBLD.append(full_ctx)

    return {
        "inputs_BL": {k: v.detach().cpu() for k, v in inputs_BL.items()},
        "attn_LBHLL": attn_LBHLL,
        "value_LBLD": value_LBLD,
        "head_ctx_LBHLd": head_ctx_LBHLd,
        "full_ctx_LBLD": full_ctx_LBLD,
    }


def apply_ln_all_source_suppression(ln_module, anchor_positions: list[int], d_unit: torch.Tensor, alpha: float) -> None:
    if alpha == 0.0:
        return
    ln_out = ln_module.output
    for pos in anchor_positions:
        tok_idx = pos + 1
        x_j = ln_out[:, tok_idx, :]
        ln_out[:, tok_idx, :] = x_j - alpha * d_unit
    ln_module.output = ln_out


def compute_attn_diff_metrics(clean_attn_BLL: torch.Tensor, patched_attn_BLL: torch.Tensor) -> dict[str, float]:
    diff = (patched_attn_BLL - clean_attn_BLL).detach().cpu()
    return {
        "attn_diff_l1": float(diff.abs().sum().item()),
        "attn_diff_l2": float(torch.sqrt((diff ** 2).sum()).item()),
        "attn_diff_max": float(diff.abs().max().item()),
    }


def run_pass_c(
    model,
    tokenizer,
    clean_sequence: str,
    clean_state: dict,
    receiver_layer: int,
    receiver_head: int,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
) -> dict:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    receiver_self = model.esm.encoder.layer[receiver_layer].attention.self
    receiver_query = receiver_self.query
    receiver_key = receiver_self.key
    batch_size, seq_len = inputs_BL["input_ids"].shape
    head_start = receiver_head * HEAD_DIM
    head_end = (receiver_head + 1) * HEAD_DIM

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            apply_ln_all_source_suppression(ln_module, anchor_positions, d_unit, alpha)

            for layer in range(TARGET_LAYER + 1, receiver_layer):
                model.esm.encoder.layer[layer].attention.self.output[0][:] = clean_state["full_ctx_LBLD"][layer].to(device)

            receiver_q = receiver_query.output
            receiver_k = receiver_key.output
            receiver_v_raw = receiver_self.value.output
            receiver_attn = receiver_self.output[1]
            receiver_v_heads = receiver_v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)

            clean_head_ctx = clean_state["head_ctx_LBHLd"][receiver_layer].to(device).clone()
            receiver_ctx = torch.matmul(receiver_attn[:, receiver_head, :, :], receiver_v_heads[:, receiver_head, :, :])
            clean_head_ctx[:, receiver_head, :, :] = receiver_ctx
            receiver_self.output[0][:] = clean_head_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)

            receiver_attn_save = receiver_attn[:, receiver_head, :, :].save()
            receiver_q_save = receiver_q[:, :, head_start:head_end].save()
            receiver_k_save = receiver_k[:, :, head_start:head_end].save()
            receiver_ctx_save = receiver_ctx.save()

    return {
        "attn_BLL": receiver_attn_save.detach().cpu(),
        "q_BLD": receiver_q_save.detach().cpu(),
        "k_BLD": receiver_k_save.detach().cpu(),
        "ctx_BLD": receiver_ctx_save.detach().cpu(),
    }


def replay_receiver_attention(
    model,
    tokenizer,
    clean_sequence: str,
    receiver_layer: int,
    receiver_head: int,
    patched_attn_BLL: torch.Tensor,
    device: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    receiver_self = model.esm.encoder.layer[receiver_layer].attention.self
    batch_size, seq_len = inputs_BL["input_ids"].shape

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)

            receiver_v_raw = receiver_self.value.output
            receiver_v_heads = receiver_v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
            current_attn = receiver_self.output[1]
            patched_attn = current_attn.clone()
            patched_attn[:, receiver_head, :, :] = patched_attn_BLL.to(device)
            new_ctx = torch.matmul(patched_attn, receiver_v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
            receiver_self.output[0][:] = new_ctx

    attn_LBHLL = []
    for layer in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{layer}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        if layer == receiver_layer:
            layer_attn[:, receiver_head, :, :] = patched_attn_BLL.detach().cpu()
        attn_LBHLL.append(layer_attn)
    return attn_LBHLL, {k: v.detach().cpu() for k, v in inputs_BL.items()}


def source_suppressed_with_receiver_reset(
    model,
    tokenizer,
    clean_sequence: str,
    receiver_layer: int,
    receiver_head: int,
    clean_receiver_attn_BLL: torch.Tensor,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    receiver_self = model.esm.encoder.layer[receiver_layer].attention.self
    batch_size, seq_len = inputs_BL["input_ids"].shape

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)
            apply_ln_all_source_suppression(ln_module, anchor_positions, d_unit, alpha)

            receiver_v_raw = receiver_self.value.output
            receiver_v_heads = receiver_v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
            current_attn = receiver_self.output[1]
            patched_attn = current_attn.clone()
            patched_attn[:, receiver_head, :, :] = clean_receiver_attn_BLL.to(device)
            new_ctx = torch.matmul(patched_attn, receiver_v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
            receiver_self.output[0][:] = new_ctx

    attn_LBHLL = []
    for layer in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{layer}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        if layer == receiver_layer:
            layer_attn[:, receiver_head, :, :] = clean_receiver_attn_BLL.detach().cpu()
        attn_LBHLL.append(layer_attn)
    return attn_LBHLL, {k: v.detach().cpu() for k, v in inputs_BL.items()}


def choose_alpha_star(rows: list[dict]) -> tuple[float, bool]:
    for row in rows:
        if row["meets_threshold"]:
            return float(row["alpha"]), True
    return float(rows[-1]["alpha"]), False


def summarize_alpha_sweep(
    protein: str,
    clean_sequence: str,
    orig_contacts_AA: torch.Tensor,
    seg: ContactSegment,
    clean_metric: float,
    corrupt_metric: float,
    clean_anchor_positions: list[int],
    d_unit: torch.Tensor,
    model,
    tokenizer,
    contact_head,
    device: str,
    alphas: list[float],
) -> tuple[list[dict], float, dict]:
    rows = []
    attn_by_alpha = {}
    inputs_by_alpha = {}

    for alpha in alphas:
        attn_LBHLL, inputs_BL, _ = cache_attention_with_steering(
            model,
            tokenizer,
            clean_sequence,
            clean_anchor_positions,
            d_unit,
            alpha,
            device,
            steering_mode="direct",
        )
        metric = compute_metric_from_attention_stack(
            attn_LBHLL,
            inputs_BL,
            contact_head,
            orig_contacts_AA,
            seg,
            device,
        )
        head_metrics = compute_l10h9_head_metrics(attn_LBHLL, clean_anchor_positions)
        attn_by_alpha[alpha] = attn_LBHLL
        inputs_by_alpha[alpha] = {k: v.detach().cpu() for k, v in inputs_BL.items()}
        rows.append(
            {
                "protein": protein,
                "alpha": float(alpha),
                "segment_metric": float(metric),
                "faithfulness": float(faithfulness(metric, clean_metric, corrupt_metric)),
                "l10h9_anchor_mass": float(head_metrics["l10h9_anchor_mass"]),
                "l10h9_top1_mass": float(head_metrics["l10h9_top1_mass"]),
                "l10h9_entropy_norm": float(head_metrics["l10h9_entropy_norm"]),
            }
        )

    clean_anchor_mass = rows[0]["l10h9_anchor_mass"]
    gap = clean_metric - corrupt_metric
    for row in rows:
        anchor_drop = 0.0 if clean_anchor_mass <= 1e-12 else (clean_anchor_mass - row["l10h9_anchor_mass"]) / clean_anchor_mass
        segment_drop_frac = 0.0 if abs(gap) <= 1e-12 else (clean_metric - row["segment_metric"]) / gap
        row["anchor_mass_rel_drop"] = float(anchor_drop)
        row["segment_gap_drop_frac"] = float(segment_drop_frac)
        row["meets_threshold"] = bool(anchor_drop >= ANCHOR_DROP_THRESHOLD and segment_drop_frac >= SEGMENT_DROP_THRESHOLD)

    alpha_star, selected_by_threshold = choose_alpha_star(rows)
    for row in rows:
        row["alpha_star"] = float(alpha_star)
        row["selected_alpha_star"] = bool(row["alpha"] == alpha_star)
        row["selected_by_threshold"] = bool(selected_by_threshold)

    return rows, alpha_star, {
        "attn_LBHLL": attn_by_alpha[alpha_star],
        "inputs_BL": inputs_by_alpha[alpha_star],
    }


def plot_outputs(alpha_rows: list[dict], receiver_rows: list[dict], output_dir: Path) -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.dpi": 200,
        }
    )

    proteins = sorted({row["protein"] for row in alpha_rows})
    fig, axes = plt.subplots(len(proteins), 2, figsize=(12, 4 * len(proteins)))
    if len(proteins) == 1:
        axes = np.array([axes])
    for row_idx, protein in enumerate(proteins):
        prot_alpha = [r for r in alpha_rows if r["protein"] == protein]
        ax = axes[row_idx, 0]
        ax.plot([r["alpha"] for r in prot_alpha], [r["segment_metric"] for r in prot_alpha], "o-", color="#1d3557")
        for r in prot_alpha:
            if r["selected_alpha_star"]:
                ax.axvline(r["alpha"], color="#c1121f", linestyle="--", linewidth=1)
        ax.set_title(f"{protein}: alpha calibration")
        ax.set_xlabel("alpha")
        ax.set_ylabel("segment metric")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax = axes[row_idx, 1]
        ax.plot([r["alpha"] for r in prot_alpha], [r["l10h9_anchor_mass"] for r in prot_alpha], "o-", color="#2a9d8f")
        for r in prot_alpha:
            if r["selected_alpha_star"]:
                ax.axvline(r["alpha"], color="#c1121f", linestyle="--", linewidth=1)
        ax.set_title(f"{protein}: L10H9 anchor mass")
        ax.set_xlabel("alpha")
        ax.set_ylabel("anchor mass")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_path_patching_alpha_sweeps.png", bbox_inches="tight")
    plt.close(fig)

    fig, axes = plt.subplots(1, len(proteins), figsize=(6 * len(proteins), 5))
    if len(proteins) == 1:
        axes = [axes]
    for ax, protein in zip(axes, proteins):
        prot_rows = [r for r in receiver_rows if r["protein"] == protein]
        ax.scatter(
            [r["replay_fraction_of_total_drop"] for r in prot_rows],
            [r["blocking_fraction_of_total_drop"] for r in prot_rows],
            s=40,
            color="#6a4c93",
        )
        for r in prot_rows:
            ax.text(
                r["replay_fraction_of_total_drop"],
                r["blocking_fraction_of_total_drop"],
                f"L{int(r['receiver_layer'])}H{int(r['receiver_head'])}",
                fontsize=7,
                alpha=0.8,
            )
        ax.set_title(f"{protein}: replay vs blocking")
        ax.set_xlabel("replay fraction of total drop")
        ax.set_ylabel("blocking fraction of total drop")
        ax.axhline(0.0, color="#999999", linewidth=0.8)
        ax.axvline(0.0, color="#999999", linewidth=0.8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_path_patching_receiver_scatter.png", bbox_inches="tight")
    plt.close(fig)


def write_report(
    protein_meta: list[dict],
    baseline_rows: list[dict],
    receiver_rows: list[dict],
    output_dir: Path,
) -> None:
    baseline_by_protein = {row["protein"]: row for row in baseline_rows}
    receiver_by_protein = defaultdict(list)
    for row in receiver_rows:
        receiver_by_protein[row["protein"]].append(row)

    lines = [
        "# Anchor Path Patching",
        "",
        "Implements `experiments/4_26_anchor_path_patching.md` in the masked-flank contact-pattern setup.",
        "",
    ]

    for meta in protein_meta:
        protein = meta["protein"]
        base = baseline_by_protein[protein]
        lines.extend(
            [
                f"## {protein}",
                "",
                f"- Contact pair: `{tuple(meta['contact_pair'])}`",
                f"- Clean flank: `{meta['clean_flank']}`",
                f"- Corrupt flank: `{meta['corrupt_flank']}`",
                f"- Clean anchors: `{meta['clean_anchor_positions']}`",
                f"- Receiver count: `{meta['receiver_count']}`",
                f"- `alpha*`: `{base['alpha_star']}`",
                f"- Clean / corrupt metric: `{base['clean_metric']:.4f}` / `{base['corrupt_metric']:.4f}`",
                f"- Total metric: `{base['total_metric']:.4f}`",
                f"- Direct metric: `{base['direct_metric']:.4f}`",
                f"- Downstream-only contribution (`direct - total`): `{base['downstream_metric_delta']:.4f}`",
                "",
                "| Receiver | Replay metric | Replay frac of total | Blocked metric | Blocking frac of total | Pass-C attn L1 | Full-source attn L1 |",
                "|----------|--------------:|---------------------:|---------------:|-----------------------:|---------------:|--------------------:|",
            ]
        )
        top_rows = sorted(
            receiver_by_protein[protein],
            key=lambda row: (row["blocking_fraction_of_total_drop"], row["replay_fraction_of_total_drop"]),
            reverse=True,
        )[:10]
        for row in top_rows:
            lines.append(
                f"| L{int(row['receiver_layer'])}H{int(row['receiver_head'])} | {row['replay_metric']:.4f} | "
                f"{row['replay_fraction_of_total_drop']:.4f} | {row['blocking_metric']:.4f} | "
                f"{row['blocking_fraction_of_total_drop']:.4f} | {row['pass_c_attn_diff_l1']:.2f} | "
                f"{row['total_attn_diff_l1']:.2f} |"
            )
        lines.append("")

    (output_dir / "anchor_path_patching.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Path patching from L10H9 into the masked-flank contact circuit")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_MANIFEST))
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--max-receivers", type=int, default=None)
    parser.add_argument("--skip-plots", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)
    receiver_manifest = load_receiver_manifest(Path(args.manifest))

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)

    qk_weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    search_dir = compute_search_dir(model, tokenizer, seq_dict[REFERENCE_PROTEIN], qk_weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    alpha_rows = []
    baseline_rows = []
    receiver_rows = []
    protein_meta = []
    diagnostics = {}

    for protein in args.proteins:
        if protein not in receiver_manifest:
            raise KeyError(f"{protein} missing from receiver manifest {args.manifest}")

        print(f"Processing {protein}...")
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])
        clean_sequence = mask_with_flanks(sequence, seg, cfg["clean_flank"])
        corrupt_sequence = mask_with_flanks(sequence, seg, cfg["corrupt_flank"])

        orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence, args.device)
        clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_sequence, args.device)
        corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_sequence, args.device)

        clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, seg)
        corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)
        clean_anchor_positions = identify_anchors(model, tokenizer, clean_sequence, args.device, top_k=3)
        clean_state = cache_clean_state(model, tokenizer, clean_sequence, args.device)
        clean_attn_LBHLL = clean_state["attn_LBHLL"]
        clean_inputs_BL = clean_state["inputs_BL"]

        protein_alpha_rows, alpha_star, total_source_state = summarize_alpha_sweep(
            protein=protein,
            clean_sequence=clean_sequence,
            orig_contacts_AA=orig_contacts_AA,
            seg=seg,
            clean_metric=clean_metric,
            corrupt_metric=corrupt_metric,
            clean_anchor_positions=clean_anchor_positions,
            d_unit=d_unit,
            model=model,
            tokenizer=tokenizer,
            contact_head=contact_head,
            device=args.device,
            alphas=DEFAULT_ALPHAS,
        )
        alpha_rows.extend(protein_alpha_rows)
        total_attn_LBHLL = total_source_state["attn_LBHLL"]
        total_inputs_BL = total_source_state["inputs_BL"]
        total_metric = compute_metric_from_attention_stack(
            total_attn_LBHLL,
            total_inputs_BL,
            contact_head,
            orig_contacts_AA,
            seg,
            args.device,
        )

        direct_attn_LBHLL = [layer.clone() for layer in clean_attn_LBHLL]
        direct_attn_LBHLL[TARGET_LAYER][:, TARGET_HEAD, :, :] = total_attn_LBHLL[TARGET_LAYER][:, TARGET_HEAD, :, :]
        direct_metric = compute_metric_from_attention_stack(
            direct_attn_LBHLL,
            clean_inputs_BL,
            contact_head,
            orig_contacts_AA,
            seg,
            args.device,
        )

        total_drop = clean_metric - total_metric
        direct_drop = clean_metric - direct_metric
        downstream_metric_delta = direct_metric - total_metric
        baseline_rows.append(
            {
                "protein": protein,
                "clean_metric": float(clean_metric),
                "corrupt_metric": float(corrupt_metric),
                "alpha_star": float(alpha_star),
                "alpha_selected_by_threshold": bool(any(r["meets_threshold"] for r in protein_alpha_rows)),
                "clean_anchor_positions": json.dumps(clean_anchor_positions),
                "total_metric": float(total_metric),
                "total_drop": float(total_drop),
                "total_faithfulness": float(faithfulness(total_metric, clean_metric, corrupt_metric)),
                "direct_metric": float(direct_metric),
                "direct_drop": float(direct_drop),
                "direct_faithfulness": float(faithfulness(direct_metric, clean_metric, corrupt_metric)),
                "downstream_metric_delta": float(downstream_metric_delta),
                "downstream_drop_delta": float(total_drop - direct_drop),
            }
        )

        receivers = receiver_manifest[protein]["receivers"]
        if args.max_receivers is not None:
            receivers = receivers[: args.max_receivers]

        protein_meta.append(
            {
                "protein": protein,
                "contact_pair": cfg["contact_pair"],
                "segment_radius": cfg["segment_radius"],
                "clean_flank": cfg["clean_flank"],
                "corrupt_flank": cfg["corrupt_flank"],
                "clean_anchor_positions": clean_anchor_positions,
                "receiver_source": receiver_manifest[protein]["receiver_source"],
                "receiver_count": len(receivers),
                "alpha_star": float(alpha_star),
            }
        )

        diagnostics[protein] = {
            "alpha_star": float(alpha_star),
            "clean_anchor_positions": clean_anchor_positions,
            "receivers": {},
        }

        for idx, receiver in enumerate(receivers, start=1):
            receiver_layer = int(receiver["layer"])
            receiver_head = int(receiver["head"])
            receiver_group = receiver.get("group", "")
            print(f"  Receiver {idx}/{len(receivers)}: L{receiver_layer}H{receiver_head}")

            pass_c = run_pass_c(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                clean_state=clean_state,
                receiver_layer=receiver_layer,
                receiver_head=receiver_head,
                anchor_positions=clean_anchor_positions,
                d_unit=d_unit,
                alpha=alpha_star,
                device=args.device,
            )

            replay_attn_LBHLL, replay_inputs_BL = replay_receiver_attention(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                receiver_layer=receiver_layer,
                receiver_head=receiver_head,
                patched_attn_BLL=pass_c["attn_BLL"],
                device=args.device,
            )
            replay_metric = compute_metric_from_attention_stack(
                replay_attn_LBHLL,
                replay_inputs_BL,
                contact_head,
                orig_contacts_AA,
                seg,
                args.device,
            )

            blocking_attn_LBHLL, blocking_inputs_BL = source_suppressed_with_receiver_reset(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                receiver_layer=receiver_layer,
                receiver_head=receiver_head,
                clean_receiver_attn_BLL=clean_attn_LBHLL[receiver_layer][:, receiver_head, :, :],
                anchor_positions=clean_anchor_positions,
                d_unit=d_unit,
                alpha=alpha_star,
                device=args.device,
            )
            blocking_metric = compute_metric_from_attention_stack(
                blocking_attn_LBHLL,
                blocking_inputs_BL,
                contact_head,
                orig_contacts_AA,
                seg,
                args.device,
            )

            replay_drop = clean_metric - replay_metric
            blocking_reduction = blocking_metric - total_metric
            total_den = total_drop if abs(total_drop) > 1e-12 else float("nan")
            total_attn_diff = compute_attn_diff_metrics(
                clean_attn_LBHLL[receiver_layer][:, receiver_head, :, :],
                total_attn_LBHLL[receiver_layer][:, receiver_head, :, :],
            )
            pass_c_attn_diff = compute_attn_diff_metrics(
                clean_attn_LBHLL[receiver_layer][:, receiver_head, :, :],
                pass_c["attn_BLL"],
            )

            receiver_rows.append(
                {
                    "protein": protein,
                    "receiver_layer": receiver_layer,
                    "receiver_head": receiver_head,
                    "receiver_group": receiver_group,
                    "alpha_star": float(alpha_star),
                    "total_metric": float(total_metric),
                    "replay_metric": float(replay_metric),
                    "replay_drop": float(replay_drop),
                    "replay_faithfulness": float(faithfulness(replay_metric, clean_metric, corrupt_metric)),
                    "replay_fraction_of_total_drop": float(replay_drop / total_den) if not math.isnan(total_den) else float("nan"),
                    "blocking_metric": float(blocking_metric),
                    "blocking_reduction": float(blocking_reduction),
                    "blocking_faithfulness": float(faithfulness(blocking_metric, clean_metric, corrupt_metric)),
                    "blocking_fraction_of_total_drop": float(blocking_reduction / total_den) if not math.isnan(total_den) else float("nan"),
                    "total_attn_diff_l1": total_attn_diff["attn_diff_l1"],
                    "total_attn_diff_l2": total_attn_diff["attn_diff_l2"],
                    "total_attn_diff_max": total_attn_diff["attn_diff_max"],
                    "pass_c_attn_diff_l1": pass_c_attn_diff["attn_diff_l1"],
                    "pass_c_attn_diff_l2": pass_c_attn_diff["attn_diff_l2"],
                    "pass_c_attn_diff_max": pass_c_attn_diff["attn_diff_max"],
                    "pass_c_q_norm": float(pass_c["q_BLD"].norm().item()),
                    "pass_c_k_norm": float(pass_c["k_BLD"].norm().item()),
                    "pass_c_ctx_norm": float(pass_c["ctx_BLD"].norm().item()),
                }
            )

            diagnostics[protein]["receivers"][f"L{receiver_layer}H{receiver_head}"] = {
                "group": receiver_group,
                "attn_BLL": pass_c["attn_BLL"],
                "q_BLD": pass_c["q_BLD"],
                "k_BLD": pass_c["k_BLD"],
                "ctx_BLD": pass_c["ctx_BLD"],
            }

    save_csv(alpha_rows, output_dir / "anchor_path_patching_alpha_calibration.csv")
    save_csv(baseline_rows, output_dir / "anchor_path_patching_baselines.csv")
    save_csv(receiver_rows, output_dir / "anchor_path_patching_receivers.csv")
    with open(output_dir / "anchor_path_patching_meta.json", "w") as f:
        json.dump(protein_meta, f, indent=2)
    with open(output_dir / "anchor_path_patching_summary.json", "w") as f:
        json.dump(
            {
                "proteins": [meta["protein"] for meta in protein_meta],
                "alpha_values": DEFAULT_ALPHAS,
                "source_head": {"layer": TARGET_LAYER, "head": TARGET_HEAD},
                "output_files": {
                    "alpha_calibration_csv": "anchor_path_patching_alpha_calibration.csv",
                    "baselines_csv": "anchor_path_patching_baselines.csv",
                    "receivers_csv": "anchor_path_patching_receivers.csv",
                    "diagnostics_pt": "anchor_path_patching_diagnostics.pt",
                    "report_md": "anchor_path_patching.md",
                },
            },
            f,
            indent=2,
        )
    torch.save(diagnostics, output_dir / "anchor_path_patching_diagnostics.pt")
    write_report(protein_meta, baseline_rows, receiver_rows, output_dir)
    if not args.skip_plots:
        plot_outputs(alpha_rows, receiver_rows, output_dir)
    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
