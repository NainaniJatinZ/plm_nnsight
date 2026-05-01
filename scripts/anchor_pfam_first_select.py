"""Pfam-first selection for E1' / E2 / E2b reruns (4_28_anchor_next.md).

Reads anchor_behavior_audit.csv, applies the stricter selection filter
(top1_mass>=0.5 & keys_50pct==1 & top_key_proj_rank==0), cross-references
with cached InterPro Pfam annotations, and groups by Pfam accession.

Outputs:
  reports/out2/anchor_hmm_v2/pfam_first_overview.csv      (per-Pfam sizes)
  reports/out2/anchor_hmm_v2/pfam_first_selection.csv     (chosen chains)
  reports/out2/anchor_hmm_v2/pfam_first_selection.md      (human-readable)

Selection rule:
  - Pfam must have >= --min-per-pfam anchor-in-domain qualifying chains.
  - Pick top --n-pfams Pfams by anchor-in-domain count.
  - From each, sample --per-pfam chains (anchor-in-domain only).
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

import math
import numpy as np
import pandas as pd

AUDIT = Path("reports/outputs/multi_protein/anchor_behavior_audit.csv")
INTERPRO_ROOT = Path("reports/out2/interpro_hmm")
OUT_DIR = Path("reports/out2/anchor_hmm_v2")


def _state_ic_at_anchor(protein: str, pfam_acc: str, anchor: int) -> float:
    """Return state IC of the HMM column the anchor maps to. NaN if unmapped."""
    try:
        from pyhmmer.plan7 import HMMFile
    except Exception:
        return float("nan")
    base = INTERPRO_ROOT / protein
    hmm_path = base / "hmms" / f"{pfam_acc}.hmm"
    sto_path = base / "alignments" / f"{pfam_acc}.sto"
    if not (hmm_path.exists() and sto_path.exists()):
        return float("nan")
    try:
        with HMMFile(hmm_path) as hf:
            hmm = hf.read()
    except Exception:
        return float("nan")
    me = hmm.match_emissions
    log20 = math.log2(20.0)
    state_ic: dict[int, float] = {}
    for st in range(1, int(hmm.M) + 1):
        probs = np.array(list(me[st]), dtype=float)
        probs = probs[probs > 0]
        ent = float(-(probs * np.log2(probs)).sum())
        state_ic[st] = log20 - ent
    # parse stockholm -> seq_pos -> hmm_state
    lines = sto_path.read_text().splitlines()
    seq_chars: list[str] = []
    rf_chars: list[str] = []
    for line in lines:
        if not line or line.startswith("# STOCKHOLM") or line == "//":
            continue
        if line.startswith("#=GC RF"):
            rf_chars.append(line.split(None, 2)[-1].strip())
        elif line.startswith("#"):
            continue
        else:
            toks = line.split()
            if len(toks) >= 2:
                seq_chars.append(toks[1].strip())
    aligned = "".join(seq_chars)
    rf = "".join(rf_chars)
    seq_pos = 0
    hmm_state = 0
    for ch, rfc in zip(aligned, rf):
        is_match = rfc != "."
        if is_match:
            hmm_state += 1
        if ch != "-":
            if seq_pos == anchor and is_match:
                return float(state_ic.get(hmm_state, float("nan")))
            seq_pos += 1
    return float("nan")


def parse_locs(s: str) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for tok in str(s).split(";"):
        m = re.match(r"\s*(\d+)\s*-\s*(\d+)", tok)
        if m:
            out.append((int(m.group(1)), int(m.group(2))))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top1-mass", type=float, default=0.5)
    ap.add_argument("--keys-50pct", type=int, default=1)
    ap.add_argument("--rank0-only", action="store_true", default=True)
    ap.add_argument("--min-per-pfam", type=int, default=10,
                    help="minimum anchor-in-domain qualifying chains required per Pfam")
    ap.add_argument("--n-pfams", type=int, default=10,
                    help="target number of Pfams")
    ap.add_argument("--per-pfam", type=int, default=14,
                    help="chains to sample per Pfam (clamped to availability)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--allow-relax", action="store_true",
                    help="if not enough Pfams meet --min-per-pfam, relax to fewer chains/Pfam.")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(AUDIT)
    mask = (
        (df.top1_mass >= args.top1_mass)
        & (df.keys_50pct == args.keys_50pct)
        & (df.top_key_proj_rank == 0)
    )
    qual = df[mask].copy()
    print(f"[select] qualifying chains (audit filter): {len(qual)}")

    cached = set(os.listdir(INTERPRO_ROOT)) if INTERPRO_ROOT.exists() else set()
    qual_cached = qual[qual.protein.isin(cached)]
    print(f"[select] cached annotations available: {len(qual_cached)} of {len(qual)}")

    rows: list[dict] = []
    for r in qual_cached.itertuples(index=False):
        sf = INTERPRO_ROOT / r.protein / "pfam_summary.tsv"
        if not sf.exists():
            continue
        try:
            t = pd.read_csv(sf, sep="\t")
        except Exception:
            continue
        anc = int(r.top_key_idx)
        for rr in t.itertuples(index=False):
            locs = parse_locs(getattr(rr, "locations", ""))
            if not locs:
                continue
            in_dom = any(s <= anc + 1 <= e for s, e in locs) or any(s <= anc <= e for s, e in locs)
            if not in_dom:
                continue
            rows.append({
                "protein": r.protein,
                "pfam_acc": rr.accession,
                "pfam_name": rr.name,
                "anchor_pos": anc,
                "top1_mass": r.top1_mass,
                "top3_mass": r.top3_mass,
                "n_res": r.n_res,
                "locations": ";".join(f"{s}-{e}" for s, e in locs),
            })
    ph = pd.DataFrame(rows)
    if ph.empty:
        print("[select] no anchor-in-domain hits; nothing to pick.")
        return 1

    # Dedupe: each chain assigned to ONE primary Pfam (highest state-IC at the anchor;
    # tie-broken by smallest start position then alphabetical Pfam id).
    print("[select] computing state-IC at anchor for chain x Pfam pairs...")
    ph["anchor_state_ic"] = ph.apply(
        lambda r: _state_ic_at_anchor(r.protein, r.pfam_acc, int(r.anchor_pos)), axis=1
    )
    ph["_loc_start"] = ph.locations.str.split(";").str[0].str.split("-").str[0].astype(float)
    ph_sorted = ph.sort_values(
        by=["protein", "anchor_state_ic", "_loc_start", "pfam_acc"],
        ascending=[True, False, True, True],
    )
    ph_dedup = ph_sorted.drop_duplicates("protein", keep="first").drop(columns=["_loc_start"])
    print(f"[select] dedup: {len(ph)} chain-Pfam rows -> {len(ph_dedup)} chains (one primary Pfam each)")
    ph = ph_dedup

    overview = (
        ph.groupby(["pfam_acc", "pfam_name"]).protein.nunique()
          .reset_index(name="n_anchor_in_dom")
          .sort_values("n_anchor_in_dom", ascending=False)
          .reset_index(drop=True)
    )
    overview.to_csv(OUT_DIR / "pfam_first_overview.csv", index=False)
    print(f"[select] Pfams seen: {len(overview)}")
    print(overview.head(20).to_string(index=False))

    eligible = overview[overview.n_anchor_in_dom >= args.min_per_pfam]
    print(f"\n[select] Pfams with >= {args.min_per_pfam} anchor-in-dom chains: {len(eligible)}")
    if len(eligible) < args.n_pfams:
        msg = f"only {len(eligible)} Pfams meet >= {args.min_per_pfam}; target was {args.n_pfams}."
        if not args.allow_relax:
            print(f"[select] {msg}\n  Re-run with --allow-relax or wait for more annotation.")
            return 2
        print(f"[select] {msg} relaxing.")
    chosen = eligible.head(args.n_pfams) if len(eligible) >= args.n_pfams else overview.head(args.n_pfams)

    rng = np.random.default_rng(args.seed)
    out_rows: list[dict] = []
    for _, prow in chosen.iterrows():
        pf = prow["pfam_acc"]
        members = ph[ph.pfam_acc == pf].sort_values("top1_mass", ascending=False)
        n_take = min(args.per_pfam, len(members))
        # take top-N by top1_mass for stability rather than random sample
        picked = members.head(n_take)
        for _, mrow in picked.iterrows():
            out_rows.append({
                "pfam_acc": pf,
                "pfam_name": prow["pfam_name"],
                "n_pfam_total": prow["n_anchor_in_dom"],
                **{k: mrow[k] for k in ["protein", "anchor_pos", "top1_mass", "top3_mass", "n_res", "locations"]},
            })
    sel = pd.DataFrame(out_rows)
    sel_csv = OUT_DIR / "pfam_first_selection.csv"
    sel.to_csv(sel_csv, index=False)

    md = ["# Pfam-first selection (E1' / E2 / E2b base set)\n"]
    md.append(f"- Audit filter: top1_mass >= {args.top1_mass} AND keys_50pct == {args.keys_50pct} AND top_key_proj_rank == 0\n")
    md.append(f"- Total qualifying: {len(qual)}; cached: {len(qual_cached)} (annotation in progress: {len(cached)} cached overall)\n")
    md.append(f"- Pfams chosen: {len(chosen)}; chains chosen: {len(sel)}\n\n")
    md.append("## Per-Pfam summary\n")
    summary_tbl = sel.groupby(["pfam_acc", "pfam_name"]).protein.nunique().reset_index(name="n_chosen")
    md.append(summary_tbl.to_csv(index=False, sep="|"))
    md.append("\n")
    (OUT_DIR / "pfam_first_selection.md").write_text("\n".join(md))
    print(f"[select] wrote {sel_csv} ({len(sel)} chains across {sel.pfam_acc.nunique()} Pfams)")
    print(sel.groupby('pfam_acc').protein.nunique().to_string())
    return 0


if __name__ == "__main__":
    sys.exit(main())
