"""E2a: C_far positivity diagnosis on the existing n=83 Exp 2 survivors.

Pre-registered outcomes (4_28_anchor_next.md):
  D1 monotonic AND D3 distance-decaying -> graded long-range contribution (refinement).
  D2 zero AND D1 flat -> artifact, drop C_far from Exp 2 reporting.
  Mixed -> flag as unresolved.

Diagnostics:
  D1: vary k_far in {2,4,8,16}; reuse the original deterministic far-position selection
      (first k indices with |pos - anchor| > radius). Measure delta_alpha_norm vs C0.
  D2: full-sequence baseline with k far positions MASKED (same indices as D1, k matched
      to the original Exp 2 k). Measures whether removing distal info changes alpha.
  D3: bin-stratified C_far. Sample k_far=4 from distance bins (R+1..R+10, R+10..R+30,
      R+30..R+60, R+60..end). Measure delta_alpha_norm per bin.

Output: reports/out2/anchor_hmm_v2/e2a_cfar_diag/
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path
import numpy as np
import pandas as pd
import torch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from anchor_hmm_experiment import (  # type: ignore
    TARGET_LAYER, TARGET_HEAD, REFERENCE_PROTEIN,
    load_sequences, load_model, extract_head_weights, compute_search_dir,
    project_batch_at_positions, build_local_window_sequence,
)

OUT_DIR = Path("reports/out2/anchor_hmm_v2/e2a_cfar_diag")
SURVIVORS_CSV = Path("reports/out2/anchor_hmm_v2/exp2_survivors.csv")
EXP2_RESULTS_CSV = Path("reports/out2/anchor_hmm/paired_masking/condition_results.csv")

PRE_REG_HEADER = (
    "# E2a C_far diagnosis. Pre-registered outcomes:\n"
    "# - D1 monotonic AND D3 distance-decaying -> graded long-range contribution.\n"
    "# - D2 |delta| ~0 AND D1 flat -> artifact, drop C_far from Exp 2 reporting.\n"
    "# - Mixed -> unresolved; flag in writeup.\n"
)


def _far_positions_first_k(seq_len: int, anchor_pos: int, radius: int, k: int) -> list[int]:
    """Replicate the original C_far selection: first k indices outside the local window."""
    return [i for i in range(seq_len) if abs(i - anchor_pos) > radius][:k]


def _bin_far_positions(seq_len: int, anchor_pos: int, radius: int) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {"near": [], "mid": [], "far": [], "veryfar": []}
    for i in range(seq_len):
        d = abs(i - anchor_pos)
        if d <= radius:
            continue
        if d <= radius + 10:
            out["near"].append(i)
        elif d <= radius + 30:
            out["mid"].append(i)
        elif d <= radius + 60:
            out["far"].append(i)
        else:
            out["veryfar"].append(i)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None, help="Limit chains for smoke test")
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--bin-seed", type=int, default=42)
    ap.add_argument("--bin-k", type=int, default=4, help="k_far per bin in D3")
    ap.add_argument("--d1-ks", nargs="+", type=int, default=[2, 4, 8, 16])
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    survivors = pd.read_csv(SURVIVORS_CSV)
    if args.limit:
        survivors = survivors.head(args.limit)
    print(f"[E2a] survivors: {len(survivors)}")

    # original Exp 2 k_far per protein (for D2 baseline match)
    cr = pd.read_csv(EXP2_RESULTS_CSV)
    orig_k_by_protein = {}
    for proto, grp in cr[cr.condition == "C7"].groupby("protein"):
        orig_k_by_protein[proto] = int(grp.k.iloc[0])

    seqs = load_sequences()
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    d = compute_search_dir(model, tokenizer, " ".join(seqs[REFERENCE_PROTEIN]), weights, device=args.device)
    d_unit = d / d.norm().clamp(min=1e-8)

    rows: list[dict] = []
    rng = np.random.default_rng(args.bin_seed)

    for idx, row in enumerate(survivors.itertuples(index=False), start=1):
        protein = row.protein
        anchor_pos = int(row.anchor_pos)
        radius = int(row.radius)
        if protein not in seqs:
            print(f"[E2a {idx}/{len(survivors)}] {protein}: missing sequence, skip")
            continue
        seq = seqs[protein]
        n = len(seq)
        full_seq = " ".join(seq)

        # alpha_full
        alpha_full = project_batch_at_positions(
            model, tokenizer, [full_seq], [anchor_pos], d_unit,
            device=args.device, batch_size=1,
        )[0][0]
        if abs(alpha_full) < 1e-8:
            print(f"[E2a {idx}/{len(survivors)}] {protein}: alpha_full ~ 0, skip")
            continue

        # C0 baseline (local window only)
        c0_seq = build_local_window_sequence(seq, anchor_pos, radius, set(), set())
        c0_alpha = project_batch_at_positions(
            model, tokenizer, [c0_seq], [anchor_pos], d_unit,
            device=args.device, batch_size=1,
        )[0][0]
        c0_alpha_norm = c0_alpha / alpha_full

        # ------ build batch of all conditions for this protein ------
        condition_seqs: list[str] = []
        condition_meta: list[dict] = []

        # D1: vary k_far
        for k_far in args.d1_ks:
            far = _far_positions_first_k(n, anchor_pos, radius, k_far)
            if len(far) < k_far:
                continue
            seq_str = build_local_window_sequence(
                seq, anchor_pos=anchor_pos, radius=radius,
                unmask_far_positions=set(far), extra_mask_positions=set(),
            )
            mean_dist = float(np.mean([abs(p - anchor_pos) for p in far]))
            condition_seqs.append(seq_str)
            condition_meta.append({
                "diagnostic": "D1", "subcond": f"k_far={k_far}",
                "k_far": k_far, "ref": "C0", "mean_dist": mean_dist,
                "positions": ";".join(map(str, far)),
            })

        # D2: full-sequence with k_far masked (k matched to original Exp 2 k)
        k_orig = orig_k_by_protein.get(protein, 8)
        far_d2 = _far_positions_first_k(n, anchor_pos, radius, k_orig)
        if far_d2:
            chars = [c if i not in set(far_d2) else "<mask>" for i, c in enumerate(seq)]
            seq_str = " ".join(chars)
            mean_dist = float(np.mean([abs(p - anchor_pos) for p in far_d2]))
            condition_seqs.append(seq_str)
            condition_meta.append({
                "diagnostic": "D2", "subcond": f"mask_far_k={k_orig}",
                "k_far": k_orig, "ref": "FULL", "mean_dist": mean_dist,
                "positions": ";".join(map(str, far_d2)),
            })

        # D3: per-bin stratified C_far
        bins = _bin_far_positions(n, anchor_pos, radius)
        for bin_name, pool in bins.items():
            if len(pool) < args.bin_k:
                continue
            sampled = sorted(rng.choice(pool, size=args.bin_k, replace=False).tolist())
            seq_str = build_local_window_sequence(
                seq, anchor_pos=anchor_pos, radius=radius,
                unmask_far_positions=set(sampled), extra_mask_positions=set(),
            )
            mean_dist = float(np.mean([abs(p - anchor_pos) for p in sampled]))
            condition_seqs.append(seq_str)
            condition_meta.append({
                "diagnostic": "D3", "subcond": f"bin={bin_name}",
                "k_far": args.bin_k, "ref": "C0", "mean_dist": mean_dist,
                "positions": ";".join(map(str, sampled)),
            })

        if not condition_seqs:
            continue

        alphas, argmax_pos = project_batch_at_positions(
            model, tokenizer, condition_seqs, [anchor_pos] * len(condition_seqs),
            d_unit, device=args.device, batch_size=args.batch_size,
        )

        for meta, a, ap_ in zip(condition_meta, alphas, argmax_pos):
            a_norm = a / alpha_full
            ref_norm = c0_alpha_norm if meta["ref"] == "C0" else 1.0
            rows.append({
                "protein": protein,
                "anchor_pos": anchor_pos,
                "radius": radius,
                "alpha_full": alpha_full,
                "c0_alpha_norm": c0_alpha_norm,
                "diagnostic": meta["diagnostic"],
                "subcond": meta["subcond"],
                "k_far": meta["k_far"],
                "ref": meta["ref"],
                "ref_alpha_norm": ref_norm,
                "alpha": a,
                "alpha_norm": a_norm,
                "delta_alpha_norm": a_norm - ref_norm,
                "argmax_pos": ap_,
                "argmax_preserved": int(ap_ == anchor_pos),
                "mean_dist_to_anchor": meta["mean_dist"],
                "positions": meta["positions"],
            })
        if idx % 10 == 0 or idx == len(survivors):
            print(f"[E2a {idx}/{len(survivors)}] {protein} done", flush=True)

    df = pd.DataFrame(rows)
    out_csv = args.out / "e2a_results.csv"
    with out_csv.open("w") as f:
        f.write(PRE_REG_HEADER)
        df.to_csv(f, index=False)
    print(f"[E2a] wrote {out_csv} ({len(df)} rows)")

    # quick aggregate
    if len(df):
        agg = (
            df.groupby(["diagnostic", "subcond"])
              .agg(n=("protein", "nunique"),
                   median_delta=("delta_alpha_norm", "median"),
                   mean_delta=("delta_alpha_norm", "mean"),
                   p25=("delta_alpha_norm", lambda s: s.quantile(0.25)),
                   p75=("delta_alpha_norm", lambda s: s.quantile(0.75)),
                   median_dist=("mean_dist_to_anchor", "median"))
              .reset_index()
        )
        agg_csv = args.out / "e2a_summary.csv"
        agg.to_csv(agg_csv, index=False)
        print(f"[E2a] wrote {agg_csv}\n{agg.to_string(index=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
