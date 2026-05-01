"""E2b: conservative-substitution variant of Exp 2 (4_28_anchor_next.md).

For each chain in the Pfam-first selection, run inside the local window:
  C0      baseline (window only, everything outside window masked)
  C7      mask top-k highest-IC positions
  C7_sub  conservatively substitute same positions (same physicochemical class)
  C8      mask k RSA-matched random positions (with resamples)
  C8_sub  conservatively substitute same positions (with resamples)

Pre-registered outcome map (4_28_anchor_next.md):
  |C7_sub| ~ |C7|     -> identity-of-class is not what matters; specific identity necessary.
  |C7_sub| < |C7| > |C8_sub|  -> physicochemical class encodes part of the signal.
  |C7_sub| ~ |C8_sub| ~ 0     -> presence at conserved positions is the necessary feature.

Output: reports/out2/anchor_hmm_v2/e2b_substitution/
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from anchor_hmm_experiment import (  # type: ignore
    TARGET_LAYER, TARGET_HEAD, REFERENCE_PROTEIN, MASK_TOKEN,
    load_sequences, load_model, extract_head_weights, compute_search_dir,
    project_batch_at_positions, build_local_window_sequence,
    compute_rsa_map, read_hmm_state_ic, parse_stockholm_mapping,
)

INTERPRO_ROOT = Path("reports/out2/interpro_hmm")
DEFAULT_SELECTION = Path("reports/out2/anchor_hmm_v2/pfam_first_selection.csv")
OUT_DIR = Path("reports/out2/anchor_hmm_v2/e2b_substitution")

# Conservative substitution classes (C3 from experiments/4_6_scramble_experiment.md)
SUB_CLASSES: dict[str, list[str]] = {
    "hydrophobic": list("AVILMFWP"),
    "polar":       list("STNQYC"),
    "positive":    list("KRH"),
    "negative":    list("DE"),
    "special":     list("G"),
}
AA_TO_CLASS: dict[str, str] = {aa: cls for cls, members in SUB_CLASSES.items() for aa in members}


def pick_substitute(aa: str, rng: np.random.Generator) -> str:
    cls = AA_TO_CLASS.get(aa)
    if cls is None:
        return aa
    pool = [a for a in SUB_CLASSES[cls] if a != aa]
    if not pool:
        return aa  # G has no peers
    return str(rng.choice(pool))


def build_window_with_subs(
    seq: str, anchor_pos: int, radius: int,
    extra_mask_positions: set[int], substitute_positions: dict[int, str],
) -> str:
    """Like build_local_window_sequence, but allows substitutions at given positions.

    Substitutions take precedence over masking. Positions outside the local window
    are masked unconditionally.
    """
    n = len(seq)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars: list[str] = []
    for i in range(n):
        if i in substitute_positions and lo <= i <= hi:
            chars.append(substitute_positions[i])
        elif i in extra_mask_positions and lo <= i <= hi:
            chars.append(MASK_TOKEN)
        elif lo <= i <= hi:
            chars.append(seq[i])
        else:
            chars.append(MASK_TOKEN)
    return " ".join(chars)


def get_state_ic_map(protein: str, pfam_acc: str) -> dict[int, float] | None:
    """Build seq_pos -> state_ic dict for given protein/Pfam from cached annotations."""
    base = INTERPRO_ROOT / protein
    hmm = base / "hmms" / f"{pfam_acc}.hmm"
    sto = base / "alignments" / f"{pfam_acc}.sto"
    if not (hmm.exists() and sto.exists()):
        return None
    state_ic = read_hmm_state_ic(hmm)
    state_map, _ = parse_stockholm_mapping(sto)
    return {pos: state_ic.get(state, np.nan) for pos, state in state_map.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    ap.add_argument("--radius", type=int, default=40, help="fixed local-window radius (used if --exp0-summary not given)")
    ap.add_argument("--exp0-summary", type=Path, default=None,
                    help="Exp 0 summary.csv with per-chain selected_radius column; overrides --radius per chain")
    ap.add_argument("--radius-floor", type=int, default=15, help="minimum radius even if Exp 0 reports lower")
    ap.add_argument("--n-random-resamples", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    sel = pd.read_csv(args.selection)
    if args.limit:
        sel = sel.head(args.limit)
    print(f"[E2b] selection chains: {len(sel)} across {sel.pfam_acc.nunique()} Pfams")

    radius_by_protein: dict[str, int] = {}
    if args.exp0_summary and args.exp0_summary.exists():
        e0 = pd.read_csv(args.exp0_summary)
        for r in e0.itertuples(index=False):
            sr = getattr(r, "selected_radius", None)
            if sr is None or pd.isna(sr):
                continue
            radius_by_protein[r.protein] = max(args.radius_floor, int(sr))
        print(f"[E2b] per-chain radii loaded for {len(radius_by_protein)} chains from {args.exp0_summary}")

    seqs = load_sequences()
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    d = compute_search_dir(model, tokenizer, " ".join(seqs[REFERENCE_PROTEIN]), weights, device=args.device)
    d_unit = d / d.norm().clamp(min=1e-8)

    rows: list[dict] = []
    rng_global = np.random.default_rng(args.seed)

    for idx, r in enumerate(sel.itertuples(index=False), start=1):
        protein = r.protein
        anchor_pos = int(r.anchor_pos)
        pfam_acc = r.pfam_acc
        seq = seqs.get(protein)
        if not seq:
            print(f"[E2b {idx}/{len(sel)}] {protein}: missing sequence")
            continue
        radius = radius_by_protein.get(protein, args.radius)
        n = len(seq)
        full_seq = " ".join(seq)

        alpha_full = project_batch_at_positions(
            model, tokenizer, [full_seq], [anchor_pos], d_unit,
            device=args.device, batch_size=1,
        )[0][0]
        if abs(alpha_full) < 1e-8:
            continue

        # Baseline guard: C0 alpha_norm >= 0.5 AND argmax == anchor_pos
        c0_seq = build_local_window_sequence(seq, anchor_pos, radius, set(), set())
        c0_alphas, c0_argmax = project_batch_at_positions(
            model, tokenizer, [c0_seq], [anchor_pos], d_unit,
            device=args.device, batch_size=1,
        )
        c0_alpha = c0_alphas[0]
        c0_an = c0_alpha / alpha_full
        if not (c0_an >= 0.5 and c0_argmax[0] == anchor_pos):
            print(f"[E2b {idx}/{len(sel)}] {protein} SKIP guard: c0_an={c0_an:.3f}, argmax={c0_argmax[0]}")
            continue

        state_ic = get_state_ic_map(protein, pfam_acc)
        if state_ic is None:
            print(f"[E2b {idx}/{len(sel)}] {protein}: no HMM/alignment cache for {pfam_acc}")
            continue

        window = list(range(max(0, anchor_pos - radius), min(n, anchor_pos + radius + 1)))
        mapped_window = [p for p in window if p in state_ic and not np.isnan(state_ic[p]) and p != anchor_pos]
        if len(mapped_window) < 4:
            continue
        ic_vals = [state_ic[p] for p in mapped_window]
        median_ic = float(np.median(ic_vals))
        k = min(8, max(1, int(0.25 * len(window))))

        # Top-k high-IC = C7 positions
        c7 = [p for p, _ in sorted(((p, state_ic[p]) for p in mapped_window),
                                    key=lambda x: x[1], reverse=True)[:k]]
        if len(c7) < k:
            continue

        # RSA map for C8 sampling
        rsa_map = compute_rsa_map(protein, seq) or {}
        if not rsa_map:
            print(f"[E2b {idx}/{len(sel)}] {protein}: no RSA, skip")
            continue

        # bin C7 by RSA for matched random sampling
        bin_edges = [0.0, 0.05, 0.25, 10.0]
        c7_bins = Counter(np.digitize([rsa_map.get(p, 0.0) for p in c7], bin_edges, right=False))
        random_pool = [p for p in window if p != anchor_pos and p in rsa_map]

        # Build all conditions in one batch per chain (replicates included)
        conditions: list[dict] = []
        # Per-chain RNG for substitutions, deterministic across re-runs
        rng = np.random.default_rng(args.seed + idx)

        # C0
        conditions.append({"cond": "C0", "rep": 0, "mask": set(), "subs": {}, "positions": []})

        # C7 (mask)
        conditions.append({"cond": "C7", "rep": 0, "mask": set(c7), "subs": {}, "positions": c7})

        # C7_sub (substitute same positions)
        c7_subs = {p: pick_substitute(seq[p], rng) for p in c7}
        conditions.append({"cond": "C7_sub", "rep": 0, "mask": set(), "subs": c7_subs, "positions": c7})

        # C8 (mask, with resamples) and C8_sub (substitute, with resamples).
        # Use the same sampled positions for C8 and C8_sub at each rep so they pair.
        for rep in range(args.n_random_resamples):
            sampled: list[int] = []
            pool_by_bin: dict[int, list[int]] = defaultdict(list)
            for p in random_pool:
                pool_by_bin[int(np.digitize([rsa_map[p]], bin_edges, right=False)[0])].append(p)
            for bin_id, count in c7_bins.items():
                pool = pool_by_bin.get(bin_id, [])
                if not pool:
                    continue
                idxs = rng.choice(pool, size=min(count, len(pool)), replace=len(pool) < count).tolist()
                sampled.extend(idxs)
            sampled = sampled[:k]
            if len(sampled) < k:
                continue
            conditions.append({"cond": "C8", "rep": rep, "mask": set(sampled), "subs": {}, "positions": sampled})
            sub_map = {p: pick_substitute(seq[p], rng) for p in sampled}
            conditions.append({"cond": "C8_sub", "rep": rep, "mask": set(), "subs": sub_map, "positions": sampled})

        # Build sequences
        batch_seqs = []
        for c in conditions:
            batch_seqs.append(build_window_with_subs(
                seq, anchor_pos, radius,
                extra_mask_positions=c["mask"], substitute_positions=c["subs"],
            ))
        batch_pos = [anchor_pos] * len(batch_seqs)

        alphas, argmax_pos = project_batch_at_positions(
            model, tokenizer, batch_seqs, batch_pos, d_unit,
            device=args.device, batch_size=args.batch_size,
        )

        for c, a, ap_ in zip(conditions, alphas, argmax_pos):
            an = a / alpha_full
            rows.append({
                "protein": protein,
                "pfam_acc": pfam_acc,
                "anchor_pos": anchor_pos,
                "radius": radius,
                "k": k,
                "condition": c["cond"],
                "repeat": c["rep"],
                "alpha": a,
                "alpha_full": alpha_full,
                "alpha_norm": an,
                "delta_alpha_norm": an - c0_an,
                "c0_alpha_norm": c0_an,
                "argmax_pos": ap_,
                "anchor_argmax_preserved": int(ap_ == anchor_pos),
                "perturbed_positions": ";".join(map(str, c["positions"])),
                "substitutions": ";".join(f"{p}:{aa}" for p, aa in c["subs"].items()),
            })

        if idx % 10 == 0 or idx == len(sel):
            print(f"[E2b {idx}/{len(sel)}] {protein} (Pfam={pfam_acc})", flush=True)

    df = pd.DataFrame(rows)
    out_csv = args.out / "e2b_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"[E2b] wrote {out_csv} ({len(df)} rows)")

    # quick aggregate: per-condition median |delta_alpha_norm|, paired
    if len(df):
        # collapse C8/C8_sub across replicates by mean within protein
        agg = (
            df.groupby(["protein", "condition"], as_index=False)["delta_alpha_norm"].mean()
        )
        wide = agg.pivot(index="protein", columns="condition", values="delta_alpha_norm")
        keep = [c for c in ["C7", "C7_sub", "C8", "C8_sub"] if c in wide.columns]
        print("\n=== E2b summary (median delta_alpha_norm, paired) ===")
        print(wide[keep].median().round(3).to_string())
        print(f"\nN paired: {len(wide.dropna(subset=keep))}")
        wide.to_csv(args.out / "e2b_paired.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
