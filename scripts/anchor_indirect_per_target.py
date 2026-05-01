#!/usr/bin/env python3
"""Per-target indirect path patching from middle heads into late heads.

Question:
- Keep the same upstream intervention: suppress L10H9 with alpha*
- Fix a single late target head r at a time
- For each intermediate source head s, isolate L10H9 -> s -> r
- Replay only the target-head attention change from that isolated path

This removes:
- joint receiver patching
- blocking-style tests
"""

from __future__ import annotations

import argparse
import gc
import json
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
    TARGET_HEAD,
    TARGET_LAYER,
    compute_search_dir,
    extract_head_weights,
    identify_anchors,
    load_model,
)
from scripts.anchor_fixed_receivers import select_fixed_sets
from scripts.anchor_path_patching import (
    DEFAULT_ALPHAS,
    apply_ln_all_source_suppression,
    cache_clean_state,
    compute_attn_diff_metrics,
    compute_metric_from_attention_stack,
    load_receiver_manifest,
    replay_receiver_attention,
    save_csv,
    summarize_alpha_sweep,
)
from scripts.jump_to_contact_pattern_bridge import (
    ContactSegment,
    compute_contact_map,
    load_protein_cfg,
    mask_with_flanks,
    patching_metric,
)

DATA_PATH = ROOT / "data" / "full_seq_dict.json"
DEFAULT_INPUT_MANIFEST = EXPERIMENT_ROOT / "inputs" / "anchor_path_patching_receiver_manifest.json"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "anchor_indirect_per_target"
DEFAULT_PROTEINS = ["2B61A", "1PVGA"]
REFERENCE_PROTEIN = "2B61A"


def clear_runtime_memory() -> None:
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def write_manifest(
    base_manifest: dict[str, dict],
    proteins: list[str],
    receiver_min_layer: int,
    output_path: Path,
) -> dict[str, dict]:
    derived = {
        "manifest_name": "anchor_indirect_per_target",
        "source_of_heads": str(DEFAULT_INPUT_MANIFEST.relative_to(ROOT)),
        "receiver_min_layer": receiver_min_layer,
        "proteins": {},
    }
    for protein in proteins:
        late_targets, source_candidates = select_fixed_sets(base_manifest, protein, receiver_min_layer)
        derived["proteins"][protein] = {
            "late_targets": late_targets,
            "source_candidates": source_candidates,
            "receiver_source": base_manifest[protein]["receiver_source"],
        }
    with open(output_path, "w") as f:
        json.dump(derived, f, indent=2)
    return derived["proteins"]


def run_source_to_target_pass_c(
    model,
    tokenizer,
    clean_sequence: str,
    clean_state: dict,
    source_layer: int,
    source_head: int,
    target_layer: int,
    target_head: int,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
    upstream_mode: str,
) -> dict:
    inputs_BL = tokenizer(clean_sequence, return_tensors="pt").to(device)
    batch_size, seq_len = inputs_BL["input_ids"].shape
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            apply_ln_all_source_suppression(ln_module, anchor_positions, d_unit, alpha)

            if upstream_mode == "isolated":
                for layer in range(TARGET_LAYER + 1, source_layer):
                    model.esm.encoder.layer[layer].attention.self.output[0][:] = clean_state["full_ctx_LBLD"][layer].to(device)
            elif upstream_mode != "free":
                raise ValueError(f"Unknown upstream_mode: {upstream_mode}")

            source_self = model.esm.encoder.layer[source_layer].attention.self
            source_v_raw = source_self.value.output
            source_attn = source_self.output[1]
            source_v_heads = source_v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
            source_head_ctx = clean_state["head_ctx_LBHLd"][source_layer].to(device).clone()
            source_ctx = torch.matmul(source_attn[:, source_head, :, :], source_v_heads[:, source_head, :, :])
            source_head_ctx[:, source_head, :, :] = source_ctx
            source_self.output[0][:] = source_head_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)

            for layer in range(source_layer + 1, target_layer):
                model.esm.encoder.layer[layer].attention.self.output[0][:] = clean_state["full_ctx_LBLD"][layer].to(device)

            target_self = model.esm.encoder.layer[target_layer].attention.self
            target_q = target_self.query.output
            target_k = target_self.key.output
            target_v_raw = target_self.value.output
            target_attn = target_self.output[1]
            target_v_heads = target_v_raw.reshape(batch_size, seq_len, NUM_HEADS, HEAD_DIM).transpose(1, 2)
            target_head_ctx = clean_state["head_ctx_LBHLd"][target_layer].to(device).clone()
            target_ctx = torch.matmul(target_attn[:, target_head, :, :], target_v_heads[:, target_head, :, :])
            target_head_ctx[:, target_head, :, :] = target_ctx
            target_self.output[0][:] = target_head_ctx.transpose(1, 2).contiguous().reshape(batch_size, seq_len, -1)

            start = target_head * HEAD_DIM
            end = (target_head + 1) * HEAD_DIM
            target_attn_save = target_attn[:, target_head, :, :].save()
            target_q_save = target_q[:, :, start:end].save()
            target_k_save = target_k[:, :, start:end].save()
            target_ctx_save = target_ctx.save()

    return {
        "target_attn_BLL": target_attn_save.detach().cpu(),
        "target_q_BLD": target_q_save.detach().cpu(),
        "target_k_BLD": target_k_save.detach().cpu(),
        "target_ctx_BLD": target_ctx_save.detach().cpu(),
    }


def plot_outputs(rows: list[dict], output_dir: Path) -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "figure.dpi": 200,
        }
    )
    proteins = sorted({row["protein"] for row in rows})
    for protein in proteins:
        prot_rows = [row for row in rows if row["protein"] == protein]
        targets = sorted({(int(r["target_layer"]), int(r["target_head"])) for r in prot_rows})
        sources = sorted({(int(r["source_layer"]), int(r["source_head"])) for r in prot_rows})
        source_index = {src: idx for idx, src in enumerate(sources)}
        target_index = {tgt: idx for idx, tgt in enumerate(targets)}

        heat = torch.full((len(targets), len(sources)), float("nan"))
        for row in prot_rows:
            tgt = (int(row["target_layer"]), int(row["target_head"]))
            src = (int(row["source_layer"]), int(row["source_head"]))
            heat[target_index[tgt], source_index[src]] = float(row["indirect_fraction_of_total_drop"])

        fig, ax = plt.subplots(figsize=(max(8, 0.5 * len(sources)), max(4, 0.6 * len(targets))))
        im = ax.imshow(heat.numpy(), aspect="auto", cmap="viridis")
        ax.set_title(f"{protein}: indirect effect into late targets")
        ax.set_xlabel("middle source head")
        ax.set_ylabel("late target head")
        ax.set_xticks(range(len(sources)))
        ax.set_xticklabels([f"L{s[0]}H{s[1]}" for s in sources], rotation=90)
        ax.set_yticks(range(len(targets)))
        ax.set_yticklabels([f"L{t[0]}H{t[1]}" for t in targets])
        fig.colorbar(im, ax=ax, label="indirect fraction of total drop")
        fig.tight_layout()
        fig.savefig(output_dir / f"{protein}_anchor_indirect_per_target_heatmap.png", bbox_inches="tight")
        plt.close(fig)


def write_report(meta_rows: list[dict], baseline_rows: list[dict], rows: list[dict], output_dir: Path) -> None:
    baseline_by_protein = {row["protein"]: row for row in baseline_rows}
    rows_by_protein_target = defaultdict(list)
    for row in rows:
        rows_by_protein_target[(row["protein"], int(row["target_layer"]), int(row["target_head"]))].append(row)

    lines = [
        "# Anchor Indirect Per Target",
        "",
        "Per-target indirect path patching from middle heads into late target heads.",
        "",
    ]

    for meta in meta_rows:
        protein = meta["protein"]
        base = baseline_by_protein[protein]
        lines.extend(
            [
                f"## {protein}",
                "",
                f"- Contact pair: `{tuple(meta['contact_pair'])}`",
                f"- Clean anchors: `{meta['clean_anchor_positions']}`",
                f"- `alpha*`: `{base['alpha_star']}`",
                f"- Upstream mode: `{meta['upstream_mode']}`",
                f"- Late targets: `{meta['late_targets']}`",
                f"- Middle sources: `{meta['source_count']}`",
                f"- Total metric: `{base['total_metric']:.4f}`",
                "",
            ]
        )
        for target in meta["late_targets"]:
            layer, head = target
            tgt_rows = sorted(
                rows_by_protein_target[(protein, layer, head)],
                key=lambda row: row["indirect_fraction_of_total_drop"],
                reverse=True,
            )[:8]
            lines.extend(
                [
                    f"### Target L{layer}H{head}",
                    "",
                    "| Source | Indirect frac total | Indirect drop | Pass-C attn L1 |",
                    "|--------|--------------------:|--------------:|---------------:|",
                ]
            )
            for row in tgt_rows:
                lines.append(
                    f"| L{int(row['source_layer'])}H{int(row['source_head'])} | {row['indirect_fraction_of_total_drop']:.4f} | "
                    f"{row['indirect_drop']:.4f} | {row['pass_c_attn_diff_l1']:.2f} |"
                )
            lines.append("")

    (output_dir / "anchor_indirect_per_target.md").write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(description="Per-target indirect path patching into late heads")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--proteins", nargs="+", default=DEFAULT_PROTEINS)
    parser.add_argument("--manifest", type=str, default=str(DEFAULT_INPUT_MANIFEST))
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--receiver-min-layer", type=int, default=26)
    parser.add_argument("--max-targets", type=int, default=None)
    parser.add_argument("--max-sources", type=int, default=None)
    parser.add_argument("--upstream-mode", choices=["isolated", "free"], default="isolated")
    parser.add_argument("--skip-plots", action="store_true")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(DATA_PATH) as f:
        seq_dict = json.load(f)
    base_manifest = load_receiver_manifest(Path(args.manifest))
    manifest = write_manifest(
        base_manifest=base_manifest,
        proteins=args.proteins,
        receiver_min_layer=args.receiver_min_layer,
        output_path=output_dir / "anchor_indirect_per_target_manifest.json",
    )

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    qk_weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    search_dir = compute_search_dir(model, tokenizer, seq_dict[REFERENCE_PROTEIN], qk_weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    alpha_rows = []
    baseline_rows = []
    rows = []
    meta_rows = []

    for protein in args.proteins:
        print(f"Processing {protein}...")
        cfg = load_protein_cfg(protein)
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*cfg["contact_pair"], radius=cfg["segment_radius"])
        clean_sequence = mask_with_flanks(sequence, seg, cfg["clean_flank"])
        corrupt_sequence = mask_with_flanks(sequence, seg, cfg["corrupt_flank"])

        late_targets = manifest[protein]["late_targets"]
        source_candidates = manifest[protein]["source_candidates"]
        if args.max_targets is not None:
            late_targets = late_targets[: args.max_targets]
        if args.max_sources is not None:
            source_candidates = source_candidates[: args.max_sources]

        orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence, args.device)
        clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_sequence, args.device)
        corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_sequence, args.device)
        clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, seg)
        corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)
        clean_anchor_positions = identify_anchors(model, tokenizer, clean_sequence, args.device, top_k=3)
        clean_state = cache_clean_state(model, tokenizer, clean_sequence, args.device)
        clean_attn_LBHLL = clean_state["attn_LBHLL"]

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
        total_metric = compute_metric_from_attention_stack(
            total_attn_LBHLL,
            total_source_state["inputs_BL"],
            contact_head,
            orig_contacts_AA,
            seg,
            args.device,
        )
        total_drop = clean_metric - total_metric

        baseline_rows.append(
            {
                "protein": protein,
                "alpha_star": float(alpha_star),
                "clean_metric": float(clean_metric),
                "corrupt_metric": float(corrupt_metric),
                "total_metric": float(total_metric),
                "total_drop": float(total_drop),
                "upstream_mode": args.upstream_mode,
            }
        )
        meta_rows.append(
            {
                "protein": protein,
                "contact_pair": cfg["contact_pair"],
                "clean_anchor_positions": clean_anchor_positions,
                "late_targets": [(int(t["layer"]), int(t["head"])) for t in late_targets],
                "source_count": len(source_candidates),
                "upstream_mode": args.upstream_mode,
            }
        )

        for target_idx, target in enumerate(late_targets, start=1):
            target_layer = int(target["layer"])
            target_head = int(target["head"])
            print(f"  Target {target_idx}/{len(late_targets)}: L{target_layer}H{target_head}")

            for source in source_candidates:
                source_layer = int(source["layer"])
                source_head = int(source["head"])
                source_group = source.get("group", "")

                pass_c = run_source_to_target_pass_c(
                    model=model,
                    tokenizer=tokenizer,
                    clean_sequence=clean_sequence,
                    clean_state=clean_state,
                    source_layer=source_layer,
                    source_head=source_head,
                    target_layer=target_layer,
                    target_head=target_head,
                    anchor_positions=clean_anchor_positions,
                    d_unit=d_unit,
                    alpha=alpha_star,
                    device=args.device,
                    upstream_mode=args.upstream_mode,
                )

                replay_attn_LBHLL, replay_inputs_BL = replay_receiver_attention(
                    model=model,
                    tokenizer=tokenizer,
                    clean_sequence=clean_sequence,
                    receiver_layer=target_layer,
                    receiver_head=target_head,
                    patched_attn_BLL=pass_c["target_attn_BLL"],
                    device=args.device,
                )
                indirect_metric = compute_metric_from_attention_stack(
                    replay_attn_LBHLL,
                    replay_inputs_BL,
                    contact_head,
                    orig_contacts_AA,
                    seg,
                    args.device,
                )
                indirect_drop = clean_metric - indirect_metric

                rows.append(
                    {
                        "protein": protein,
                        "target_layer": target_layer,
                        "target_head": target_head,
                        "source_layer": source_layer,
                        "source_head": source_head,
                        "source_group": source_group,
                        "upstream_mode": args.upstream_mode,
                        "alpha_star": float(alpha_star),
                        "indirect_metric": float(indirect_metric),
                        "indirect_drop": float(indirect_drop),
                        "indirect_fraction_of_total_drop": float(indirect_drop / total_drop) if abs(total_drop) > 1e-12 else float("nan"),
                        "pass_c_attn_diff_l1": float(
                            compute_attn_diff_metrics(
                                clean_attn_LBHLL[target_layer][:, target_head, :, :],
                                pass_c["target_attn_BLL"],
                            )["attn_diff_l1"]
                        ),
                        "pass_c_q_norm": float(pass_c["target_q_BLD"].norm().item()),
                        "pass_c_k_norm": float(pass_c["target_k_BLD"].norm().item()),
                        "pass_c_ctx_norm": float(pass_c["target_ctx_BLD"].norm().item()),
                        "target_total_attn_diff_l1": float(
                            compute_attn_diff_metrics(
                                clean_attn_LBHLL[target_layer][:, target_head, :, :],
                                total_attn_LBHLL[target_layer][:, target_head, :, :],
                            )["attn_diff_l1"]
                        ),
                    }
                )

                del pass_c
                del replay_attn_LBHLL
                del replay_inputs_BL
                clear_runtime_memory()

            clear_runtime_memory()

        clear_runtime_memory()

    save_csv(alpha_rows, output_dir / "anchor_indirect_per_target_alpha_calibration.csv")
    save_csv(baseline_rows, output_dir / "anchor_indirect_per_target_baselines.csv")
    save_csv(rows, output_dir / "anchor_indirect_per_target.csv")
    with open(output_dir / "anchor_indirect_per_target_meta.json", "w") as f:
        json.dump(meta_rows, f, indent=2)
    write_report(meta_rows, baseline_rows, rows, output_dir)
    if not args.skip_plots:
        plot_outputs(rows, output_dir)

    print(f"Saved outputs to {output_dir}")


if __name__ == "__main__":
    main()
