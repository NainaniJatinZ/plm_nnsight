#!/usr/bin/env python3
# %% [markdown]
# # ESM2 3B Flank Sweep
#
# Finds the first flank jump for `facebook/esm2_t36_3B_UR50D` using the same
# masking and contact metric as `contact_pattern_v2.py`.
#
# Default behavior for large runs:
# - scan flanks outward from 0
# - stop once a single-step jump reaches the requested threshold
# - evaluate a small number of extra flanks for sanity
# - save a `jump_details_esm_3b.json` file in `data/` matching the 650M format

# %% ── Imports and cache config ─────────────────────────────────────────────

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch

CACHE_ROOT = Path("/project/pi_annagreen_umass_edu/jatin/plm_circuits/models")
HF_CACHE_DIR = CACHE_ROOT / "huggingface"
HF_HUB_CACHE_DIR = HF_CACHE_DIR / "hub"
TORCH_CACHE_DIR = CACHE_ROOT / "torch"
MPL_CONFIG_DIR = Path("/tmp/matplotlib-plm-nnsight")

for cache_dir in (HF_CACHE_DIR, HF_HUB_CACHE_DIR, TORCH_CACHE_DIR, MPL_CONFIG_DIR):
    cache_dir.mkdir(parents=True, exist_ok=True)

os.environ["HF_HOME"] = str(HF_CACHE_DIR)
os.environ["HF_HUB_CACHE"] = str(HF_HUB_CACHE_DIR)
os.environ["HUGGINGFACE_HUB_CACHE"] = str(HF_HUB_CACHE_DIR)
os.environ["TORCH_HOME"] = str(TORCH_CACHE_DIR)
os.environ["MPLCONFIGDIR"] = str(MPL_CONFIG_DIR)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from transformers import EsmForMaskedLM, EsmTokenizer


# %% ── Paths and constants ─────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
PAIR_JSON = REPO_ROOT / "data" / "reproduce_pair_recovery_100_w_bos_eos.json"
SEQ_JSON = REPO_ROOT / "data" / "full_seq_dict.json"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "reports" / "out2" / "esm2_3b_flank_sweep"
DEFAULT_JUMP_JSON = REPO_ROOT / "data" / "jump_details_esm_3b.json"
MODEL_NAME = "facebook/esm2_t36_3B_UR50D"


# %% ── Helpers copied from contact_pattern_v2.py ───────────────────────────

@dataclass
class ContactSegment:
    ss1_start: int
    ss1_end: int
    ss2_start: int
    ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int) -> "ContactSegment":
        return cls(
            pos1 - radius,
            pos1 + radius + 1,
            pos2 - radius,
            pos2 + radius + 1,
        )


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


def compute_contact_map(
    esm_model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    sequence_S: str,
    device: str,
) -> torch.Tensor:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.inference_mode():
        return esm_model.predict_contacts(
            inputs_BL["input_ids"],
            inputs_BL["attention_mask"],
        )[0].detach().cpu()


def compute_contact_maps_batch(
    esm_model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    sequences: list[str],
    device: str,
) -> torch.Tensor:
    inputs_BL = tokenizer(sequences, return_tensors="pt", padding=True).to(device)
    with torch.inference_mode():
        return esm_model.predict_contacts(
            inputs_BL["input_ids"],
            inputs_BL["attention_mask"],
        ).detach().cpu()


def patching_metric(
    pred_AA: torch.Tensor,
    orig_AA: torch.Tensor,
    seg: ContactSegment,
) -> float:
    pred = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = (orig * orig).sum()
    return ((pred * orig).sum() / denom).item() if denom > 1e-12 else 0.0


def summarize_curve(protein_rows: list[dict], stop_threshold: float) -> dict:
    flanks = np.array([row["flank"] for row in protein_rows], dtype=int)
    metrics = np.array([row["contact_metric"] for row in protein_rows], dtype=float)
    deltas = np.diff(metrics)
    if len(deltas) == 0:
        max_jump_idx = 0
        max_jump = 0.0
    else:
        max_jump_idx = int(np.argmax(deltas))
        max_jump = float(deltas[max_jump_idx])

    first_threshold_idx = next((i for i, d in enumerate(deltas) if d >= stop_threshold), None)
    jump_found = first_threshold_idx is not None
    if jump_found:
        corrupt_idx = first_threshold_idx
        clean_idx = first_threshold_idx + 1
    else:
        corrupt_idx = max_jump_idx
        clean_idx = min(max_jump_idx + 1, len(flanks) - 1)

    return {
        "jump_found": jump_found,
        "jump_from_flank": int(flanks[corrupt_idx]),
        "jump_to_flank": int(flanks[clean_idx]),
        "jump_delta": float(metrics[clean_idx] - metrics[corrupt_idx]) if clean_idx != corrupt_idx else 0.0,
        "max_jump_from_flank": int(flanks[max_jump_idx]),
        "max_jump_to_flank": int(flanks[min(max_jump_idx + 1, len(flanks) - 1)]),
        "max_jump_delta": max_jump,
        "metric_before_jump": float(metrics[corrupt_idx]),
        "metric_after_jump": float(metrics[clean_idx]),
        "metric_at_last_flank": float(metrics[-1]),
        "last_flank_evaluated": int(flanks[-1]),
        "first_flank_ge_0_5": next((int(f) for f, m in zip(flanks, metrics) if m >= 0.5), None),
        "first_flank_ge_0_7": next((int(f) for f, m in zip(flanks, metrics) if m >= 0.7), None),
    }


def build_jump_detail(summary: dict) -> dict:
    return {
        "clean_flank_length": summary["jump_to_flank"],
        "clean_recovery": summary["metric_after_jump"],
        "corrupted_flank_length": summary["jump_from_flank"],
        "corrupted_recovery": summary["metric_before_jump"],
        "jump_delta": summary["jump_delta"],
        "pair_index": summary["pair_index"],
        "contact_pair": summary["contact_pair"],
        "sequence_length": summary["sequence_length"],
        "segment_radius": summary["segment_radius"],
    }


# %% ── Plotting and reports ────────────────────────────────────────────────

def save_outputs(
    rows: list[dict],
    summary_rows: list[dict],
    output_dir: Path,
    make_plot: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    repo_root_resolved = REPO_ROOT.resolve()

    def _display_path(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(repo_root_resolved))
        except ValueError:
            return str(path)

    df = pd.DataFrame(rows)
    summary_df = pd.DataFrame(summary_rows)

    csv_path = output_dir / "esm2_3b_flank_sweep.csv"
    summary_csv_path = output_dir / "esm2_3b_flank_sweep_summary.csv"
    summary_json_path = output_dir / "esm2_3b_flank_sweep_summary.json"
    md_path = output_dir / "esm2_3b_flank_sweep.md"

    df.to_csv(csv_path, index=False)
    summary_df.to_csv(summary_csv_path, index=False)
    summary_json_path.write_text(json.dumps(summary_rows, indent=2))

    plot_path = output_dir / "esm2_3b_flank_sweep.png"
    if make_plot and len(summary_rows) > 0:
        plot_rows = [row for row in summary_rows if row["jump_found"]]
        if not plot_rows:
            plot_rows = summary_rows[: min(len(summary_rows), 12)]
        proteins = [row["protein"] for row in plot_rows]
        n = len(proteins)
        fig, axes = plt.subplots(n, 1, figsize=(9, max(3.0 * n, 4.5)), sharex=True)
        if n == 1:
            axes = [axes]

        for ax, protein in zip(axes, proteins):
            sub = df[df["protein"] == protein].sort_values("flank")
            summary = summary_df[summary_df["protein"] == protein].iloc[0]
            ax.plot(sub["flank"], sub["contact_metric"], marker="o", ms=3, lw=1.8, color="#1f77b4")
            if summary["jump_found"]:
                ax.axvline(summary["jump_to_flank"], color="#d62728", ls="--", lw=1.2, alpha=0.8)
            ax.set_ylabel("contact")
            ax.set_title(
                f"{protein}: pair={tuple(summary['contact_pair'])}, "
                f"jump_found={bool(summary['jump_found'])}, "
                f"max d={summary['max_jump_delta']:.3f}"
            )
            ax.grid(alpha=0.25, lw=0.5)
            ax.set_ylim(bottom=min(0.0, float(sub["contact_metric"].min()) - 0.05), top=1.05)

        axes[-1].set_xlabel("flank size")
        fig.suptitle("ESM2 3B flank sweep", y=0.995)
        fig.tight_layout()
        fig.savefig(plot_path, dpi=200, bbox_inches="tight")
        plt.close(fig)

    lines = [
        "# ESM2 3B Flank Sweep",
        "",
        "First-pass 3B flank scan using the masking and contact metric from `contact_pattern_v2.py`.",
        f"Jump criterion: first single-step increase with delta >= {summary_rows[0]['stop_threshold']:.3f}." if summary_rows else "No rows saved.",
        "",
        f"- Output CSV: `{_display_path(csv_path)}`",
        f"- Summary CSV: `{_display_path(summary_csv_path)}`",
        f"- Plot written: `{make_plot}`",
        "",
        "| Protein | Pair | Jump found | Jump from | Jump to | Jump delta | Max jump delta | Last flank | Metric @ last flank |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in summary_rows:
        lines.append(
            f"| {row['protein']} | {tuple(row['contact_pair'])} | {row['jump_found']} | "
            f"{row['jump_from_flank']} | {row['jump_to_flank']} | {row['jump_delta']:.4f} | "
            f"{row['max_jump_delta']:.4f} | {row['last_flank_evaluated']} | {row['metric_at_last_flank']:.4f} |"
        )
    md_path.write_text("\n".join(lines) + "\n")


# %% ── Main ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Run the 3B contact-pattern flank sweep")
    parser.add_argument("--proteins", nargs="*", default=None, help="Explicit proteins to run")
    parser.add_argument("--n-proteins", type=int, default=5, help="If neither --proteins nor --all-proteins is given, use the first N proteins")
    parser.add_argument("--all-proteins", action="store_true", help="Run all proteins from the pair JSON")
    parser.add_argument("--max-flank", type=int, default=60, help="Maximum flank size to scan")
    parser.add_argument("--segment-radius", type=int, default=5, help="Half-width around each contact position")
    parser.add_argument("--stop-threshold", type=float, default=0.5, help="Stop when a single-step jump reaches this delta")
    parser.add_argument("--extra-after-hit", type=int, default=2, help="Number of extra flanks to evaluate after the threshold hit")
    parser.add_argument("--batch-size", type=int, default=4, help="Number of flank contexts to evaluate per forward pass")
    parser.add_argument("--plot-limit", type=int, default=20, help="Only write a combined plot if the number of proteins is at most this value")
    parser.add_argument("--device", type=str, default=("cuda" if torch.cuda.is_available() else "cpu"))
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--jump-json", type=Path, default=DEFAULT_JUMP_JSON)
    args = parser.parse_args()

    pair_dict: dict[str, list[list[int]]] = json.loads(PAIR_JSON.read_text())
    seq_dict: dict[str, str] = json.loads(SEQ_JSON.read_text())

    if args.proteins:
        proteins = args.proteins
    elif args.all_proteins:
        proteins = list(pair_dict.keys())
    else:
        proteins = list(pair_dict.keys())[: args.n_proteins]

    print(f"Loading model: {MODEL_NAME}")
    print(f"Cache root: {CACHE_ROOT}")
    print(f"Device: {args.device}")
    print(f"Proteins to scan: {len(proteins)}")
    tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME, cache_dir=str(HF_CACHE_DIR))
    esm_model = EsmForMaskedLM.from_pretrained(
        MODEL_NAME,
        cache_dir=str(HF_CACHE_DIR),
        attn_implementation="eager",
    ).to(args.device).eval()

    rows: list[dict] = []
    summary_rows: list[dict] = []
    jump_details: dict[str, dict] = {}

    for i, protein in enumerate(proteins, start=1):
        if protein not in pair_dict:
            print(f"[{i}/{len(proteins)}] {protein}: skipped, no pair entry")
            continue
        if protein not in seq_dict:
            print(f"[{i}/{len(proteins)}] {protein}: skipped, no sequence entry")
            continue
        if not pair_dict[protein]:
            print(f"[{i}/{len(proteins)}] {protein}: skipped, empty pair list")
            continue

        contact_pair = tuple(pair_dict[protein][0])
        sequence = seq_dict[protein]
        seg = ContactSegment.from_contact_pair(*contact_pair, radius=args.segment_radius)

        if seg.ss1_start < 0 or seg.ss2_end > len(sequence):
            print(f"[{i}/{len(proteins)}] {protein}: skipped, segment out of bounds for pair {contact_pair}")
            continue

        print(f"[{i}/{len(proteins)}] {protein}: pair={contact_pair}, len={len(sequence)}")
        orig_contacts = compute_contact_map(esm_model, tokenizer, sequence, args.device)

        protein_rows: list[dict] = []
        prev_metric: float | None = None
        stop_after_flank: int | None = None
        last_flank = -1

        for flank_start in range(0, args.max_flank + 1, args.batch_size):
            flank_end = min(flank_start + args.batch_size, args.max_flank + 1)
            flank_chunk = list(range(flank_start, flank_end))
            masked_sequences = [mask_with_flanks(sequence, seg, flank) for flank in flank_chunk]
            contact_maps = compute_contact_maps_batch(esm_model, tokenizer, masked_sequences, args.device)

            for local_idx, flank in enumerate(flank_chunk):
                metric = patching_metric(contact_maps[local_idx], orig_contacts, seg)
                row = {
                    "protein": protein,
                    "pair_index": 0,
                    "contact_pair": list(contact_pair),
                    "sequence_length": len(sequence),
                    "segment_radius": args.segment_radius,
                    "flank": flank,
                    "contact_metric": metric,
                }
                protein_rows.append(row)
                rows.append(row)
                if prev_metric is not None and stop_after_flank is None:
                    delta = metric - prev_metric
                    if delta >= args.stop_threshold:
                        stop_after_flank = min(args.max_flank, flank + args.extra_after_hit)
                        print(
                            f"  threshold hit at {flank - 1}->{flank}: "
                            f"delta={delta:.4f}; continuing to flank {stop_after_flank}"
                        )
                prev_metric = metric
                last_flank = flank

            if last_flank % 10 == 0 or last_flank == args.max_flank:
                print(f"  flank={last_flank:2d} metric={protein_rows[-1]['contact_metric']:.4f}")
            if stop_after_flank is not None and last_flank >= stop_after_flank:
                break

        summary = summarize_curve(protein_rows, stop_threshold=args.stop_threshold)
        summary.update(
            {
                "protein": protein,
                "pair_index": 0,
                "contact_pair": list(contact_pair),
                "sequence_length": len(sequence),
                "segment_radius": args.segment_radius,
                "max_flank": args.max_flank,
                "stop_threshold": args.stop_threshold,
                "extra_after_hit": args.extra_after_hit,
                "batch_size": args.batch_size,
            }
        )
        summary_rows.append(summary)

        if summary["jump_found"]:
            jump_details[protein] = build_jump_detail(summary)
            print(
                f"  stored jump: {summary['jump_from_flank']}→{summary['jump_to_flank']} "
                f"(delta={summary['jump_delta']:.4f})"
            )
        else:
            print(
                f"  no jump >= {args.stop_threshold:.3f}; "
                f"max was {summary['max_jump_from_flank']}→{summary['max_jump_to_flank']} "
                f"(delta={summary['max_jump_delta']:.4f})"
            )

        if args.device.startswith("cuda"):
            torch.cuda.empty_cache()

    args.jump_json.write_text(json.dumps(jump_details, indent=2))
    make_plot = len(summary_rows) <= args.plot_limit
    save_outputs(rows, summary_rows, args.output_dir, make_plot=make_plot)
    print(f"Saved outputs to {args.output_dir}")
    print(f"Saved jump details for {len(jump_details)} proteins to {args.jump_json}")


if __name__ == "__main__":
    main()
