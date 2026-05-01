#!/usr/bin/env python3
"""Scan intermediate source heads into a fixed late receiver set.

This is a follow-on to `anchor_path_patching.py`.

Setup:
- keep the same masked-flank clean/corrupt baseline
- keep the same upstream intervention: suppress L10H9 with alpha*
- fix a late receiver set (default: circuit heads with layer >= 26)
- scan candidate source heads from the same circuit with 10 < layer < receiver_min_layer

For each source head s:
- Pass C isolates L10H9 -> s -> late receiver set
- Replay patches only the late receiver-set changes induced by s
- Source blocking resets s back to clean inside the full source-suppressed run
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
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.anchor_contact_steering import (
    EXPERIMENT_ROOT,
    HEAD_DIM,
    NUM_HEADS,
    NUM_LAYERS,
    TARGET_HEAD,
    TARGET_LAYER,
    compute_search_dir,
    extract_head_weights,
    identify_anchors,
    load_model,
)
from scripts.anchor_path_patching import (
    DEFAULT_ALPHAS,
    apply_ln_all_source_suppression,
    cache_clean_state,
    compute_attn_diff_metrics,
    compute_metric_from_attention_stack,
    load_receiver_manifest,
    save_csv,
    summarize_alpha_sweep,
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
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "anchor_fixed_receivers"
DEFAULT_INPUT_MANIFEST = EXPERIMENT_ROOT / "inputs" / "anchor_path_patching_receiver_manifest.json"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
REFERENCE_PROTEIN = "2B61A"


def group_heads_by_layer(heads: list[dict]) -> dict[int, list[int]]:
    grouped: dict[int, list[int]] = defaultdict(list)
    for head in heads:
        grouped[int(head["layer"])].append(int(head["head"]))
    for layer in grouped:
        grouped[layer] = sorted(grouped[layer])
    return dict(grouped)


def select_fixed_sets(
    manifest: dict[str, dict],
    protein: str,
    receiver_min_layer: int,
) -> tuple[list[dict], list[dict]]:
    heads = manifest[protein]["receivers"]
    receiver_set = [dict(head) for head in heads if int(head["layer"]) >= receiver_min_layer]
    source_candidates = [dict(head) for head in heads if TARGET_LAYER < int(head["layer"]) < receiver_min_layer]
    return receiver_set, source_candidates


def write_fixed_manifest(
    manifest: dict[str, dict],
    proteins: list[str],
    receiver_min_layer: int,
    output_path: Path,
) -> dict[str, dict]:
    fixed = {
        "manifest_name": "anchor_fixed_receivers_source_scan",
        "source_of_heads": str(DEFAULT_INPUT_MANIFEST.relative_to(ROOT)),
        "receiver_min_layer": receiver_min_layer,
        "proteins": {},
    }
    for protein in proteins:
        receiver_set, source_candidates = select_fixed_sets(manifest, protein, receiver_min_layer)
        fixed["proteins"][protein] = {
            "receiver_source": manifest[protein]["receiver_source"],
            "fixed_receivers": receiver_set,
            "source_candidates": source_candidates,
        }
    with open(output_path, "w") as f:
        json.dump(fixed, f, indent=2)
    return fixed["proteins"]


def patch_receiver_set_on_clean(
    model,
    tokenizer,
    clean_sequence: str,
    receiver_heads_by_layer: dict[int, list[int]],
    patched_receiver_attn: dict[tuple[int, int], torch.Tensor],
    device: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    batch_size, seq_len = inputs_BL["input_ids"].shape

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)

            for layer in sorted(receiver_heads_by_layer):
                heads = receiver_heads_by_layer[layer]
                self_attn = model.esm.encoder.layer[layer].attention.self
                v_raw = self_attn.value.output
                current_attn = self_attn.output[1]
                v_heads = v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                patched_attn = current_attn.clone()
                for head in heads:
                    patched_attn[:, head, :, :] = patched_receiver_attn[(layer, head)].to(device)

                new_ctx = torch.matmul(patched_attn, v_heads)
                new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
                self_attn.output[0][:] = new_ctx

    attn_LBHLL = []
    for layer in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{layer}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        for head in receiver_heads_by_layer.get(layer, []):
            layer_attn[:, head, :, :] = patched_receiver_attn[(layer, head)].detach().cpu()
        attn_LBHLL.append(layer_attn)
    return attn_LBHLL, {k: v.detach().cpu() for k, v in inputs_BL.items()}


def source_suppressed_with_receiver_set_reset(
    model,
    tokenizer,
    clean_sequence: str,
    receiver_heads_by_layer: dict[int, list[int]],
    clean_receiver_attn: dict[tuple[int, int], torch.Tensor],
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    batch_size, seq_len = inputs_BL["input_ids"].shape
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)
            apply_ln_all_source_suppression(ln_module, anchor_positions, d_unit, alpha)

            for layer in sorted(receiver_heads_by_layer):
                heads = receiver_heads_by_layer[layer]
                self_attn = model.esm.encoder.layer[layer].attention.self
                v_raw = self_attn.value.output
                current_attn = self_attn.output[1]
                v_heads = v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                patched_attn = current_attn.clone()
                for head in heads:
                    patched_attn[:, head, :, :] = clean_receiver_attn[(layer, head)].to(device)

                new_ctx = torch.matmul(patched_attn, v_heads)
                new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
                self_attn.output[0][:] = new_ctx

    attn_LBHLL = []
    for layer in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{layer}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        for head in receiver_heads_by_layer.get(layer, []):
            layer_attn[:, head, :, :] = clean_receiver_attn[(layer, head)].detach().cpu()
        attn_LBHLL.append(layer_attn)
    return attn_LBHLL, {k: v.detach().cpu() for k, v in inputs_BL.items()}


def source_suppressed_with_source_reset(
    model,
    tokenizer,
    clean_sequence: str,
    source_layer: int,
    source_head: int,
    clean_source_attn_BLL: torch.Tensor,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
) -> tuple[list[torch.Tensor], dict]:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    batch_size, seq_len = inputs_BL["input_ids"].shape
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    self_attn = model.esm.encoder.layer[source_layer].attention.self

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)
            apply_ln_all_source_suppression(ln_module, anchor_positions, d_unit, alpha)

            v_raw = self_attn.value.output
            current_attn = self_attn.output[1]
            v_heads = v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)

            patched_attn = current_attn.clone()
            patched_attn[:, source_head, :, :] = clean_source_attn_BLL.to(device)
            new_ctx = torch.matmul(patched_attn, v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
            self_attn.output[0][:] = new_ctx

    attn_LBHLL = []
    for layer in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{layer}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        if layer == source_layer:
            layer_attn[:, source_head, :, :] = clean_source_attn_BLL.detach().cpu()
        attn_LBHLL.append(layer_attn)
    return attn_LBHLL, {k: v.detach().cpu() for k, v in inputs_BL.items()}


def run_source_to_fixed_receivers_pass_c(
    model,
    tokenizer,
    clean_sequence: str,
    clean_state: dict,
    source_layer: int,
    source_head: int,
    receiver_heads_by_layer: dict[int, list[int]],
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
) -> dict:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    batch_size, seq_len = inputs_BL["input_ids"].shape
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    max_receiver_layer = max(receiver_heads_by_layer)
    receiver_saves: dict[tuple[int, int], torch.Tensor] = {}

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            apply_ln_all_source_suppression(ln_module, anchor_positions, d_unit, alpha)

            for layer in range(TARGET_LAYER + 1, source_layer):
                model.esm.encoder.layer[layer].attention.self.output[0][:] = clean_state["full_ctx_LBLD"][layer].to(device)

            source_self = model.esm.encoder.layer[source_layer].attention.self
            source_v_raw = source_self.value.output
            source_attn = source_self.output[1]
            source_v_heads = source_v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
            source_head_ctx = clean_state["head_ctx_LBHLd"][source_layer].to(device).clone()
            source_ctx = torch.matmul(source_attn[:, source_head, :, :], source_v_heads[:, source_head, :, :])
            source_head_ctx[:, source_head, :, :] = source_ctx
            source_self.output[0][:] = source_head_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)
            source_attn_save = source_attn[:, source_head, :, :].save()

            for layer in range(source_layer + 1, max_receiver_layer + 1):
                heads = receiver_heads_by_layer.get(layer, [])
                if not heads:
                    model.esm.encoder.layer[layer].attention.self.output[0][:] = clean_state["full_ctx_LBLD"][layer].to(device)
                    continue

                self_attn = model.esm.encoder.layer[layer].attention.self
                v_raw = self_attn.value.output
                attn = self_attn.output[1]
                v_heads = v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
                head_ctx = clean_state["head_ctx_LBHLd"][layer].to(device).clone()

                for head in heads:
                    ctx = torch.matmul(attn[:, head, :, :], v_heads[:, head, :, :])
                    head_ctx[:, head, :, :] = ctx
                    receiver_saves[(layer, head)] = attn[:, head, :, :].save()

                self_attn.output[0][:] = head_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)

    return {
        "source_attn_BLL": source_attn_save.detach().cpu(),
        "receiver_attn": {k: v.detach().cpu() for k, v in receiver_saves.items()},
    }


def plot_outputs(source_rows: list[dict], output_dir: Path) -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.dpi": 200,
        }
    )

    proteins = sorted({row["protein"] for row in source_rows})
    fig, axes = plt.subplots(1, len(proteins), figsize=(6 * len(proteins), 5))
    if len(proteins) == 1:
        axes = [axes]
    for ax, protein in zip(axes, proteins):
        prot_rows = [r for r in source_rows if r["protein"] == protein]
        ax.scatter(
            [r["replay_fraction_of_total_drop"] for r in prot_rows],
            [r["source_blocking_fraction_of_total_drop"] for r in prot_rows],
            s=40,
            color="#1d3557",
        )
        for row in prot_rows:
            ax.text(
                row["replay_fraction_of_total_drop"],
                row["source_blocking_fraction_of_total_drop"],
                f"L{int(row['source_layer'])}H{int(row['source_head'])}",
                fontsize=7,
                alpha=0.8,
            )
        ax.set_title(f"{protein}: source replay vs source blocking")
        ax.set_xlabel("late-set replay fraction of total drop")
        ax.set_ylabel("source-blocking fraction of total drop")
        ax.axhline(0.0, color="#999999", linewidth=0.8)
        ax.axvline(0.0, color="#999999", linewidth=0.8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_fixed_receivers_scatter.png", bbox_inches="tight")
    plt.close(fig)


def write_report(
    protein_meta: list[dict],
    baseline_rows: list[dict],
    source_rows: list[dict],
    output_dir: Path,
) -> None:
    baseline_by_protein = {row["protein"]: row for row in baseline_rows}
    source_by_protein = defaultdict(list)
    for row in source_rows:
        source_by_protein[row["protein"]].append(row)

    lines = [
        "# Anchor Fixed Receivers",
        "",
        "Late receiver set fixed per protein; intermediate circuit heads are scanned as candidate sources.",
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
                f"- Clean anchors: `{meta['clean_anchor_positions']}`",
                f"- `alpha*`: `{base['alpha_star']}`",
                f"- Fixed late receivers: `{meta['fixed_receivers']}`",
                f"- Source candidates: `{meta['source_count']}`",
                f"- Total metric: `{base['total_metric']:.4f}`",
                f"- Late receiver-set replay metric: `{base['late_receiver_set_replay_metric']:.4f}`",
                f"- Late receiver-set blocking metric: `{base['late_receiver_set_blocking_metric']:.4f}`",
                "",
                "| Source | Replay frac total | Replay frac late-set | Source-block frac total | Pass-C late-set attn L1 | Total late-set attn L1 |",
                "|--------|------------------:|---------------------:|------------------------:|------------------------:|-----------------------:|",
            ]
        )
        top_rows = sorted(
            source_by_protein[protein],
            key=lambda row: (row["source_blocking_fraction_of_total_drop"], row["replay_fraction_of_total_drop"]),
            reverse=True,
        )[:12]
        for row in top_rows:
            lines.append(
                f"| L{int(row['source_layer'])}H{int(row['source_head'])} | {row['replay_fraction_of_total_drop']:.4f} | "
                f"{row['replay_fraction_of_late_set_drop']:.4f} | {row['source_blocking_fraction_of_total_drop']:.4f} | "
                f"{row['pass_c_receiver_diff_l1_sum']:.2f} | {row['total_receiver_diff_l1_sum']:.2f} |"
            )
        lines.append("")

    (output_dir / "anchor_fixed_receivers.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fixed late-receiver source scan for anchor path patching")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_INPUT_MANIFEST))
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--receiver-min-layer", type=int, default=26)
    parser.add_argument("--max-sources", type=int, default=None)
    parser.add_argument("--skip-plots", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)
    base_manifest = load_receiver_manifest(Path(args.manifest))
    fixed_manifest = write_fixed_manifest(
        manifest=base_manifest,
        proteins=args.proteins,
        receiver_min_layer=args.receiver_min_layer,
        output_path=output_dir / "anchor_fixed_receivers_manifest.json",
    )

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    qk_weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    search_dir = compute_search_dir(model, tokenizer, seq_dict[REFERENCE_PROTEIN], qk_weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    alpha_rows = []
    baseline_rows = []
    source_rows = []
    protein_meta = []

    for protein in args.proteins:
        print(f"Processing {protein}...")
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])
        clean_sequence = mask_with_flanks(sequence, seg, cfg["clean_flank"])
        corrupt_sequence = mask_with_flanks(sequence, seg, cfg["corrupt_flank"])

        fixed_receivers = fixed_manifest[protein]["fixed_receivers"]
        source_candidates = fixed_manifest[protein]["source_candidates"]
        if args.max_sources is not None:
            source_candidates = source_candidates[: args.max_sources]
        receiver_heads_by_layer = group_heads_by_layer(fixed_receivers)
        receiver_keys = [(int(head["layer"]), int(head["head"])) for head in fixed_receivers]

        if not receiver_keys:
            raise ValueError(f"{protein} has no fixed receivers with layer >= {args.receiver_min_layer}")

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
        total_drop = clean_metric - total_metric

        clean_receiver_attn = {(layer, head): clean_attn_LBHLL[layer][:, head, :, :] for layer, head in receiver_keys}
        total_receiver_attn = {(layer, head): total_attn_LBHLL[layer][:, head, :, :] for layer, head in receiver_keys}

        late_replay_attn, late_replay_inputs = patch_receiver_set_on_clean(
            model=model,
            tokenizer=tokenizer,
            clean_sequence=clean_sequence,
            receiver_heads_by_layer=receiver_heads_by_layer,
            patched_receiver_attn=total_receiver_attn,
            device=args.device,
        )
        late_replay_metric = compute_metric_from_attention_stack(
            late_replay_attn,
            late_replay_inputs,
            contact_head,
            orig_contacts_AA,
            seg,
            args.device,
        )
        late_replay_drop = clean_metric - late_replay_metric

        late_block_attn, late_block_inputs = source_suppressed_with_receiver_set_reset(
            model=model,
            tokenizer=tokenizer,
            clean_sequence=clean_sequence,
            receiver_heads_by_layer=receiver_heads_by_layer,
            clean_receiver_attn=clean_receiver_attn,
            anchor_positions=clean_anchor_positions,
            d_unit=d_unit,
            alpha=alpha_star,
            device=args.device,
        )
        late_block_metric = compute_metric_from_attention_stack(
            late_block_attn,
            late_block_inputs,
            contact_head,
            orig_contacts_AA,
            seg,
            args.device,
        )
        late_block_reduction = late_block_metric - total_metric

        baseline_rows.append(
            {
                "protein": protein,
                "alpha_star": float(alpha_star),
                "clean_metric": float(clean_metric),
                "corrupt_metric": float(corrupt_metric),
                "total_metric": float(total_metric),
                "total_drop": float(total_drop),
                "late_receiver_set_replay_metric": float(late_replay_metric),
                "late_receiver_set_replay_drop": float(late_replay_drop),
                "late_receiver_set_replay_fraction_of_total_drop": float(late_replay_drop / total_drop) if abs(total_drop) > 1e-12 else float("nan"),
                "late_receiver_set_blocking_metric": float(late_block_metric),
                "late_receiver_set_blocking_reduction": float(late_block_reduction),
                "late_receiver_set_blocking_fraction_of_total_drop": float(late_block_reduction / total_drop) if abs(total_drop) > 1e-12 else float("nan"),
            }
        )

        protein_meta.append(
            {
                "protein": protein,
                "contact_pair": cfg["contact_pair"],
                "clean_flank": cfg["clean_flank"],
                "corrupt_flank": cfg["corrupt_flank"],
                "clean_anchor_positions": clean_anchor_positions,
                "receiver_min_layer": args.receiver_min_layer,
                "fixed_receivers": [(int(head["layer"]), int(head["head"])) for head in fixed_receivers],
                "source_count": len(source_candidates),
            }
        )

        for idx, source in enumerate(source_candidates, start=1):
            source_layer = int(source["layer"])
            source_head = int(source["head"])
            source_group = source.get("group", "")
            print(f"  Source {idx}/{len(source_candidates)}: L{source_layer}H{source_head}")

            pass_c = run_source_to_fixed_receivers_pass_c(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                clean_state=clean_state,
                source_layer=source_layer,
                source_head=source_head,
                receiver_heads_by_layer=receiver_heads_by_layer,
                anchor_positions=clean_anchor_positions,
                d_unit=d_unit,
                alpha=alpha_star,
                device=args.device,
            )

            replay_attn_LBHLL, replay_inputs_BL = patch_receiver_set_on_clean(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                receiver_heads_by_layer=receiver_heads_by_layer,
                patched_receiver_attn=pass_c["receiver_attn"],
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
            replay_drop = clean_metric - replay_metric

            source_block_attn, source_block_inputs = source_suppressed_with_source_reset(
                model=model,
                tokenizer=tokenizer,
                clean_sequence=clean_sequence,
                source_layer=source_layer,
                source_head=source_head,
                clean_source_attn_BLL=clean_attn_LBHLL[source_layer][:, source_head, :, :],
                anchor_positions=clean_anchor_positions,
                d_unit=d_unit,
                alpha=alpha_star,
                device=args.device,
            )
            source_block_metric = compute_metric_from_attention_stack(
                source_block_attn,
                source_block_inputs,
                contact_head,
                orig_contacts_AA,
                seg,
                args.device,
            )
            source_block_reduction = source_block_metric - total_metric

            pass_c_receiver_diff_l1_sum = 0.0
            total_receiver_diff_l1_sum = 0.0
            for key in receiver_keys:
                clean_attn = clean_receiver_attn[key]
                pass_c_receiver_diff_l1_sum += compute_attn_diff_metrics(clean_attn, pass_c["receiver_attn"][key])["attn_diff_l1"]
                total_receiver_diff_l1_sum += compute_attn_diff_metrics(clean_attn, total_receiver_attn[key])["attn_diff_l1"]

            source_rows.append(
                {
                    "protein": protein,
                    "source_layer": source_layer,
                    "source_head": source_head,
                    "source_group": source_group,
                    "alpha_star": float(alpha_star),
                    "replay_metric": float(replay_metric),
                    "replay_drop": float(replay_drop),
                    "replay_fraction_of_total_drop": float(replay_drop / total_drop) if abs(total_drop) > 1e-12 else float("nan"),
                    "replay_fraction_of_late_set_drop": float(replay_drop / late_replay_drop) if abs(late_replay_drop) > 1e-12 else float("nan"),
                    "source_blocking_metric": float(source_block_metric),
                    "source_blocking_reduction": float(source_block_reduction),
                    "source_blocking_fraction_of_total_drop": float(source_block_reduction / total_drop) if abs(total_drop) > 1e-12 else float("nan"),
                    "pass_c_receiver_diff_l1_sum": float(pass_c_receiver_diff_l1_sum),
                    "total_receiver_diff_l1_sum": float(total_receiver_diff_l1_sum),
                    "source_total_attn_diff_l1": float(
                        compute_attn_diff_metrics(
                            clean_attn_LBHLL[source_layer][:, source_head, :, :],
                            total_attn_LBHLL[source_layer][:, source_head, :, :],
                        )["attn_diff_l1"]
                    ),
                    "source_pass_c_attn_diff_l1": float(
                        compute_attn_diff_metrics(
                            clean_attn_LBHLL[source_layer][:, source_head, :, :],
                            pass_c["source_attn_BLL"],
                        )["attn_diff_l1"]
                    ),
                }
            )

    save_csv(alpha_rows, output_dir / "anchor_fixed_receivers_alpha_calibration.csv")
    save_csv(baseline_rows, output_dir / "anchor_fixed_receivers_baselines.csv")
    save_csv(source_rows, output_dir / "anchor_fixed_receivers_sources.csv")
    with open(output_dir / "anchor_fixed_receivers_meta.json", "w") as f:
        json.dump(protein_meta, f, indent=2)
    write_report(protein_meta, baseline_rows, source_rows, output_dir)
    if not args.skip_plots:
        plot_outputs(source_rows, output_dir)

    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
