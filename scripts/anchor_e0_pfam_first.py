"""Exp 0 sweep on the Pfam-first selection (4_28_anchor_next.md, step 4 sanity).

Determines per-chain selected_radius for use in E2b (and E1' as a confirmation).
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anchor_hmm_experiment import (  # type: ignore
    P50Row, TARGET_LAYER, TARGET_HEAD, REFERENCE_PROTEIN,
    load_sequences, load_model, extract_head_weights, compute_search_dir,
    run_experiment_0,
)

DEFAULT_SELECTION = Path("reports/out2/anchor_hmm_v2/pfam_first_selection.csv")
DEFAULT_OUT = Path("reports/out2/anchor_hmm_v2/exp0")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--max-flank", type=int, default=80)
    ap.add_argument("--jump-threshold", type=float, default=0.5)
    ap.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    sel = pd.read_csv(args.selection)
    seqs = load_sequences()

    rows: list[P50Row] = []
    for r in sel.itertuples(index=False):
        if r.protein not in seqs:
            continue
        rows.append(P50Row(
            protein=r.protein, anchor_pos=int(r.anchor_pos),
            top3_mass=float(r.top3_mass), max_jump_delta=0.0,
            jump_found=False, n_res=int(r.n_res),
        ))
    print(f"[E0'] running Exp 0 on {len(rows)} chains, max_flank={args.max_flank}")

    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    d = compute_search_dir(model, tokenizer, " ".join(seqs[REFERENCE_PROTEIN]), weights, device=args.device)
    d_unit = d / d.norm().clamp(min=1e-8)

    args.out.mkdir(parents=True, exist_ok=True)
    per_protein_df, summary_df = run_experiment_0(
        rows, seqs, args.out, model, tokenizer, d_unit,
        device=args.device, max_flank=args.max_flank,
        batch_size=args.batch_size, jump_threshold=args.jump_threshold,
    )
    print(f"[E0'] wrote per-protein curves and summary to {args.out}")
    if "selected_radius" in summary_df.columns:
        sr = summary_df["selected_radius"].dropna()
        print(f"[E0'] selected_radius: n={len(sr)}, median={sr.median():.1f}, IQR=[{sr.quantile(.25):.1f}, {sr.quantile(.75):.1f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
