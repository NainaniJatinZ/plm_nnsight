#!/usr/bin/env python3
"""Contact prediction at local-flank projection jump radii.

Uses the existing local-flank sweep from anchor_local_flank_v1 to find, for each
protein, the largest jump in projection recovery (alpha_norm). Then evaluates
contact prediction on the two flank windows around that jump:
  - jump_from: the radius before the jump
  - jump_to: the radius after the jump

Contact precision is evaluated only on residue pairs where both residues are
visible (unmasked) in the flank window.

Outputs:
  - per-protein CSV with masked-window and full-baseline visible-subset metrics
  - summary JSON
  - short markdown report

Usage:
    uv run python scripts/anchor_local_flank_contact_jump_v1.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
EXPERIMENT_ROOT = ROOT / "reports" / "out2" / "suppressing_anchors"
DEFAULT_LOCAL_FLANK_DIR = EXPERIMENT_ROOT / "local_flank_v1"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "local_flank_contact_jump_v1"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"

sys.path.insert(0, str(ROOT))

LONG_RANGE_SEP = 24


def load_contact_model(device: str):
    from transformers import EsmForMaskedLM, EsmTokenizer

    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(
        model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager"
    ).to(device).eval()
    return tokenizer, esm_model


def build_masked_sequence(sequence: str, anchor_pos: int, radius: int) -> str:
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = []
    for i in range(n):
        if lo <= i <= hi:
            chars.append(sequence[i])
        else:
            chars.append("<mask>")
    return " ".join(chars)


def visible_mask(n_res: int, anchor_pos: int, radius: int) -> np.ndarray:
    lo = max(0, anchor_pos - radius)
    hi = min(n_res - 1, anchor_pos + radius)
    mask = np.zeros(n_res, dtype=bool)
    mask[lo : hi + 1] = True
    return mask


@torch.no_grad()
def predict_contacts(esm_model, tokenizer, sequence_str: str, device: str) -> np.ndarray:
    inputs = tokenizer(sequence_str, return_tensors="pt").to(device)
    pred = esm_model.predict_contacts(inputs["input_ids"], inputs["attention_mask"])[0]
    return pred.detach().cpu().numpy()


def precision_at_k_visible(
    pred_probs_AA: np.ndarray,
    gt_contacts_AA: np.ndarray,
    visible_A: np.ndarray,
    k: int,
    min_sep: int = LONG_RANGE_SEP,
) -> float:
    n = pred_probs_AA.shape[0]
    rows, cols = np.triu_indices(n, k=min_sep)
    keep = visible_A[rows] & visible_A[cols]
    rows = rows[keep]
    cols = cols[keep]
    if len(rows) == 0 or k == 0:
        return float("nan")
    pred_vals = pred_probs_AA[rows, cols]
    gt_vals = gt_contacts_AA[rows, cols]
    top_k = min(k, len(pred_vals))
    top_idx = np.argsort(-pred_vals)[:top_k]
    return float(gt_vals[top_idx].sum()) / top_k


def evaluate_visible_contacts(pred_probs_AA: np.ndarray, gt_contacts_AA: np.ndarray, visible_A: np.ndarray) -> dict:
    n_visible = int(visible_A.sum())
    return {
        "n_visible": n_visible,
        "P_L5_visible": precision_at_k_visible(pred_probs_AA, gt_contacts_AA, visible_A, max(1, n_visible // 5)),
        "P_L2_visible": precision_at_k_visible(pred_probs_AA, gt_contacts_AA, visible_A, max(1, n_visible // 2)),
        "P_L_visible": precision_at_k_visible(pred_probs_AA, gt_contacts_AA, visible_A, n_visible),
    }


def load_flank_rows(csv_path: Path) -> list[dict]:
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["n_res"] = int(row["n_res"])
            row["anchor_pos"] = int(row["anchor_pos"])
            row["radius_int"] = int(row["radius_int"])
            row["alpha_norm"] = float(row["alpha_norm"])
            rows.append(row)
    return rows


def detect_projection_jump(protein_rows: list[dict]) -> dict | None:
    prows = sorted(protein_rows, key=lambda x: x["radius_int"])
    vals = [r["alpha_norm"] for r in prows]
    if len(vals) < 2:
        return None
    deltas = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    max_idx = int(np.argmax(deltas))
    return {
        "jump_from_radius": int(prows[max_idx]["radius_int"]),
        "jump_to_radius": int(prows[max_idx + 1]["radius_int"]),
        "jump_from_alpha_norm": float(prows[max_idx]["alpha_norm"]),
        "jump_to_alpha_norm": float(prows[max_idx + 1]["alpha_norm"]),
        "max_jump_alpha_norm": float(deltas[max_idx]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument(
        "--flank-csv",
        type=str,
        default=str(DEFAULT_LOCAL_FLANK_DIR / "anchor_local_flank_v1_per_protein.csv"),
        help="Per-protein output CSV from anchor_local_flank_v1.py",
    )
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    from scripts.anchor_contact_steering import parse_pdb_contacts

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    flank_rows = load_flank_rows(Path(args.flank_csv))
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    proteins = sorted(set(r["protein"] for r in flank_rows))

    print(f"Loading contact model on {args.device}...")
    tokenizer, esm_model = load_contact_model(args.device)

    results = []
    n_skipped_no_pdb = 0
    n_skipped_no_jump = 0

    for idx, protein in enumerate(proteins, start=1):
        seq = all_seqs.get(protein)
        if seq is None:
            continue
        gt_contacts_AA = parse_pdb_contacts(protein, seq)
        if gt_contacts_AA is None:
            n_skipped_no_pdb += 1
            continue

        prows = [r for r in flank_rows if r["protein"] == protein]
        jump = detect_projection_jump(prows)
        if jump is None:
            n_skipped_no_jump += 1
            continue

        anchor_pos = prows[0]["anchor_pos"]
        n_res = len(seq)
        full_seq_str = " ".join(seq)
        full_pred_AA = predict_contacts(esm_model, tokenizer, full_seq_str, args.device)

        for jump_kind, radius in [("jump_from", jump["jump_from_radius"]), ("jump_to", jump["jump_to_radius"])]:
            masked_seq = build_masked_sequence(seq, anchor_pos, radius)
            masked_pred_AA = predict_contacts(esm_model, tokenizer, masked_seq, args.device)
            vis_A = visible_mask(n_res, anchor_pos, radius)

            masked_metrics = evaluate_visible_contacts(masked_pred_AA, gt_contacts_AA, vis_A)
            full_metrics = evaluate_visible_contacts(full_pred_AA, gt_contacts_AA, vis_A)

            results.append({
                "protein": protein,
                "n_res": n_res,
                "anchor_pos": anchor_pos,
                "jump_kind": jump_kind,
                "radius_int": radius,
                "jump_from_radius": jump["jump_from_radius"],
                "jump_to_radius": jump["jump_to_radius"],
                "jump_from_alpha_norm": jump["jump_from_alpha_norm"],
                "jump_to_alpha_norm": jump["jump_to_alpha_norm"],
                "max_jump_alpha_norm": jump["max_jump_alpha_norm"],
                **masked_metrics,
                "full_P_L5_visible": full_metrics["P_L5_visible"],
                "full_P_L2_visible": full_metrics["P_L2_visible"],
                "full_P_L_visible": full_metrics["P_L_visible"],
                "delta_P_L5_visible": masked_metrics["P_L5_visible"] - full_metrics["P_L5_visible"],
                "delta_P_L2_visible": masked_metrics["P_L2_visible"] - full_metrics["P_L2_visible"],
                "delta_P_L_visible": masked_metrics["P_L_visible"] - full_metrics["P_L_visible"],
            })

        print(
            f"  [{idx}/{len(proteins)}] {protein}: jump {jump['jump_from_radius']} -> {jump['jump_to_radius']} "
            f"(max delta {jump['max_jump_alpha_norm']:.3f})"
        )

    csv_path = output_dir / "anchor_local_flank_contact_jump_v1.csv"
    fields = list(results[0].keys()) if results else []
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved: {csv_path}")

    summary = {
        "n_rows": len(results),
        "n_proteins": len(set(r["protein"] for r in results)),
        "n_skipped_no_pdb": n_skipped_no_pdb,
        "n_skipped_no_jump": n_skipped_no_jump,
    }

    for jump_kind in ["jump_from", "jump_to"]:
        rows = [r for r in results if r["jump_kind"] == jump_kind]
        if not rows:
            continue
        for key in [
            "radius_int",
            "P_L5_visible", "P_L2_visible", "P_L_visible",
            "full_P_L5_visible", "full_P_L2_visible", "full_P_L_visible",
            "delta_P_L5_visible", "delta_P_L2_visible", "delta_P_L_visible",
        ]:
            vals = [r[key] for r in rows if not np.isnan(r[key])]
            summary[f"{jump_kind}_{key}_median"] = float(np.median(vals)) if vals else float("nan")
            summary[f"{jump_kind}_{key}_mean"] = float(np.mean(vals)) if vals else float("nan")

    by_protein = {}
    for r in results:
        by_protein.setdefault(r["protein"], {})[r["jump_kind"]] = r

    jump_deltas = {"P_L5_visible": [], "P_L2_visible": [], "P_L_visible": []}
    for protein, entries in by_protein.items():
        if "jump_from" in entries and "jump_to" in entries:
            for key in jump_deltas:
                v_from = entries["jump_from"][key]
                v_to = entries["jump_to"][key]
                if not np.isnan(v_from) and not np.isnan(v_to):
                    jump_deltas[key].append(v_to - v_from)

    for key, vals in jump_deltas.items():
        summary[f"jump_to_minus_from_{key}_median"] = float(np.median(vals)) if vals else float("nan")
        summary[f"jump_to_minus_from_{key}_mean"] = float(np.mean(vals)) if vals else float("nan")

    summary_path = output_dir / "anchor_local_flank_contact_jump_v1_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {summary_path}")

    md_path = output_dir / "anchor_local_flank_contact_jump_v1.md"
    with open(md_path, "w") as f:
        f.write("# Anchor Local Flank Jump Contact Analysis\n\n")
        f.write("Uses the projection jump pair from `anchor_local_flank_v1_per_protein.csv`.\n")
        f.write("For each protein, evaluates contact precision only on residue pairs where both residues are visible in the flank window.\n\n")
        f.write(f"Proteins scored: {summary['n_proteins']}\n")
        f.write(f"Skipped (no PDB contacts): {summary['n_skipped_no_pdb']}\n")
        f.write(f"Skipped (no jump pair): {summary['n_skipped_no_jump']}\n\n")
        f.write("## Median visible-subset precision\n\n")
        f.write("| Window | Radius | P@L/5 | P@L/2 | P@L |\n")
        f.write("|--------|--------|-------|--------|-----|\n")
        for jump_kind in ["jump_from", "jump_to"]:
            f.write(
                f"| {jump_kind} | {summary.get(f'{jump_kind}_radius_int_median', float('nan')):.1f} "
                f"| {summary.get(f'{jump_kind}_P_L5_visible_median', float('nan')):.4f} "
                f"| {summary.get(f'{jump_kind}_P_L2_visible_median', float('nan')):.4f} "
                f"| {summary.get(f'{jump_kind}_P_L_visible_median', float('nan')):.4f} |\n"
            )
        f.write("\n## Median change from jump_from to jump_to\n\n")
        f.write(
            f"- Delta P@L/5: {summary.get('jump_to_minus_from_P_L5_visible_median', float('nan')):.4f}\n"
        )
        f.write(
            f"- Delta P@L/2: {summary.get('jump_to_minus_from_P_L2_visible_median', float('nan')):.4f}\n"
        )
        f.write(
            f"- Delta P@L: {summary.get('jump_to_minus_from_P_L_visible_median', float('nan')):.4f}\n"
        )
        f.write("\n## Median masked-vs-full gap on the same visible subset\n\n")
        for jump_kind in ["jump_from", "jump_to"]:
            f.write(
                f"- {jump_kind} delta P@L/5: {summary.get(f'{jump_kind}_delta_P_L5_visible_median', float('nan')):.4f}\n"
            )
            f.write(
                f"- {jump_kind} delta P@L/2: {summary.get(f'{jump_kind}_delta_P_L2_visible_median', float('nan')):.4f}\n"
            )
            f.write(
                f"- {jump_kind} delta P@L: {summary.get(f'{jump_kind}_delta_P_L_visible_median', float('nan')):.4f}\n"
            )
    print(f"Saved: {md_path}")


if __name__ == "__main__":
    main()
