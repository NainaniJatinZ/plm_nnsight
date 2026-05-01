"""E1': rerun Exp 1 on the Pfam-first selection (4_28_anchor_next.md).

Wrapper that constructs a list[P50Row] from pfam_first_selection.csv and calls
anchor_hmm_experiment.run_experiment_1 directly.

Outputs:
  reports/out2/anchor_hmm_v2/exp1/
    anchor_hmm_mapping.tsv
    per_pfam_entropy.csv
    pfam_first_summary.md
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anchor_hmm_experiment import (  # type: ignore
    P50Row, load_sequences, load_ss_dict, run_experiment_1,
)

DEFAULT_SELECTION = Path("reports/out2/anchor_hmm_v2/pfam_first_selection.csv")
DEFAULT_OUT = Path("reports/out2/anchor_hmm_v2/exp1")
DEFAULT_ANNOTATION = Path("reports/out2/interpro_hmm")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--annotation-root", type=Path, default=DEFAULT_ANNOTATION)
    ap.add_argument("--n-control-resamples", type=int, default=200)
    args = ap.parse_args()

    sel = pd.read_csv(args.selection)
    print(f"[E1'] selection: {len(sel)} chains across {sel.pfam_acc.nunique()} Pfams")

    seqs = load_sequences()
    ss_dict = load_ss_dict()

    # Build P50Row list. top3_mass is what we have; max_jump_delta=0 / jump_found=False
    # are placeholders since Exp 1 doesn't use them after selection.
    rows: list[P50Row] = []
    for r in sel.itertuples(index=False):
        if r.protein not in seqs:
            continue
        rows.append(P50Row(
            protein=r.protein,
            anchor_pos=int(r.anchor_pos),
            top3_mass=float(r.top3_mass),
            max_jump_delta=0.0,
            jump_found=False,
            n_res=int(r.n_res),
        ))
    print(f"[E1'] P50Row built for {len(rows)}/{len(sel)}")
    args.out.mkdir(parents=True, exist_ok=True)

    mapping_df, per_pfam_df = run_experiment_1(
        rows, seqs, ss_dict, args.out,
        annotation_root=args.annotation_root,
        n_control_resamples=args.n_control_resamples,
    )
    print(f"[E1'] mapping rows: {len(mapping_df)}; per-Pfam rows: {len(per_pfam_df)}")

    if len(per_pfam_df):
        h = per_pfam_df["anchor_h_norm"]
        beats_random = (h < per_pfam_df["random_h_norm_mean"]).sum()
        beats_buried = ((per_pfam_df["buried_n_mean"] > 0) & (h < per_pfam_df["buried_h_norm_mean"])).sum()
        n_buried_test = (per_pfam_df["buried_n_mean"] > 0).sum()
        beats_sse = ((per_pfam_df["sse_n_mean"] > 0) & (h < per_pfam_df["sse_h_norm_mean"])).sum()
        n_sse_test = (per_pfam_df["sse_n_mean"] > 0).sum()
        print("\n=== E1' summary ===")
        print(f"  anchor h_norm < random:  {beats_random}/{len(per_pfam_df)}")
        print(f"  anchor h_norm < buried:  {beats_buried}/{n_buried_test}  (degenerate skipped)")
        print(f"  anchor h_norm < sse:     {beats_sse}/{n_sse_test}        (degenerate skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
