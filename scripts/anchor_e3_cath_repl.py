"""Cross-fold replication of Exp 3 (3Di vs AA windows) on the CATH corpus.

See experiments/4_30_anchor_e3_cath_repl.md for the full spec.

Stages:
    extract_3di    -> verify gap-stripped foldmason 3Di vs foldseek 3Di
    build_windows  -> per-chain AA and 3Di windows around anchor(s)
    pair_features  -> d_AA, d_3Di, same_col_pm2, stratum, tm, seqid per pair
    regression     -> M0/M1_AA/M1_3Di/M2 per stratum and TM range
    cv             -> leave-one-Pfam-out AUC
    aux_clustering -> HDBSCAN NMI/ARI for AA and 3Di windows
    plots          -> 4-panel main figure
    null           -> shuffled chain->window negative controls

Default: --mode top1 --audit-only. Use --mode top3 to add the top-3 supplement,
--all-chains to run on n=129 instead of n=74.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CATH_DIR = ROOT / "reports" / "out2" / "cath_transfer"
OUT_DIR = ROOT / "reports" / "out2" / "anchor_e3_cath_repl"
FOLDSEEK = ROOT / "foldseek" / "bin" / "foldseek"

WINDOW_HALF = 15  # 31 residues total
GAP = "-"
AA_ALPHABET = list("ACDEFGHIKLMNPQRSTVWYX") + [GAP]  # 22
DI_ALPHABET = list("ACDEFGHIKLMNPQRSTVWY") + [GAP]   # 21
SETS = ["A_3.40.50.720", "B_3.40.50.1820", "C_2.60.40.10"]

# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def read_fasta(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    name, buf = None, []
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    out[name] = "".join(buf)
                name = line[1:].split()[0]
                buf = []
            else:
                buf.append(line.strip())
    if name is not None:
        out[name] = "".join(buf)
    return out


def load_anchors() -> pd.DataFrame:
    df = pd.read_csv(CATH_DIR / "anchors.csv")
    df["audit_pass"] = (df["top1_mass"] >= 0.5) & (df["keys_50pct"] == 1)
    df["top3_attn_list"] = df["top3_attn"].apply(
        lambda s: [int(x) for x in str(s).split(",") if x.strip().isdigit()]
    )
    return df


def load_pairs(all_chains: bool = False) -> pd.DataFrame:
    fname = "pairs_all.csv" if all_chains else "pairs.csv"
    df = pd.read_csv(CATH_DIR / fname)
    df["same_col"] = ((df["set_i"] == df["set_j"]) & (df["anchor_col_dist"] == 0)).astype(int)
    df["same_col_pm2"] = (
        (df["set_i"] == df["set_j"]) & (df["anchor_col_dist"] <= 2)
    ).astype(int)
    df["stratum"] = df["category"]
    return df


def load_pairwise_tm() -> pd.DataFrame:
    df = pd.read_csv(CATH_DIR / "pairwise_tm.tsv", sep="\t", header=None)
    df.columns = ["q", "t", "c1", "c2", "tm", "rmsd", "alnlen", "qlen", "tlen"]
    return df


# ---------------------------------------------------------------------------
# Stage: extract_3di
# ---------------------------------------------------------------------------

def stage_extract_3di() -> dict[str, str]:
    """Build per-chain 3Di string from foldmason MSA, verify against foldseek."""
    chain_seqs = json.load(open(CATH_DIR / "chain_seqs.json"))

    threed: dict[str, str] = {}
    for s in SETS:
        msa3di = read_fasta(CATH_DIR / "msa" / f"{s}_3di.fa")
        for ch, aln in msa3di.items():
            if ch in threed:
                continue
            threed[ch] = aln.replace("-", "")

    # Length check on every chain that has a sequence
    bad_len = []
    for ch, aa in chain_seqs.items():
        if ch not in threed:
            continue
        if len(aa) != len(threed[ch]):
            bad_len.append((ch, len(aa), len(threed[ch])))
    if bad_len:
        msg = "3Di length mismatch (foldmason gap-stripped vs chain_seqs):\n"
        msg += "\n".join(f"  {c}: aa={a} 3di={b}" for c, a, b in bad_len[:20])
        raise SystemExit(msg)

    # Foldseek cross-check (token-by-token)
    fs_threed = run_foldseek_3di_extract()
    diffs = []
    for ch, di in threed.items():
        if ch not in fs_threed:
            continue
        if fs_threed[ch] != di:
            # Try matching ignoring case (foldseek emits lowercase for low-confidence)
            if fs_threed[ch].upper() != di.upper():
                diffs.append((ch, len(di), len(fs_threed[ch])))
    if diffs:
        msg = "3Di token mismatch foldmason vs foldseek:\n"
        msg += "\n".join(f"  {c}: foldmason={a} foldseek={b}" for c, a, b in diffs[:20])
        raise SystemExit(msg)
    print(f"[extract_3di] {len(threed)} chains, length check passed, foldseek cross-check on {sum(1 for c in threed if c in fs_threed)} chains passed")
    return threed


def run_foldseek_3di_extract() -> dict[str, str]:
    """Run `foldseek structureto3didescriptor` on chain_pdb/ once and cache."""
    cache = OUT_DIR / "foldseek_3di.fa"
    if cache.exists():
        return read_fasta(cache)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    chain_pdb = CATH_DIR / "chain_pdb"
    pdbs = sorted(chain_pdb.glob("*.pdb"))
    if not pdbs:
        raise SystemExit(f"No PDBs in {chain_pdb}")
    desc_out = OUT_DIR / "foldseek_descriptor.tsv"
    cmd = [str(FOLDSEEK), "structureto3didescriptor"] + [str(p) for p in pdbs] + [str(desc_out)]
    print(f"[extract_3di] running foldseek on {len(pdbs)} PDBs")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # Some foldseek builds want a tmp dir as last arg; try that
        raise SystemExit(f"foldseek failed:\n{res.stderr[-2000:]}")
    out: dict[str, str] = {}
    with open(desc_out) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            name, aa_seq, di_seq = parts[0], parts[1], parts[2]
            # name is e.g. "6won_G.pdb_G" or "6won_G_A"; normalize to chain key
            chain_key = Path(name).stem
            # foldseek emits "<stem>_<chainId>" — strip if it matches
            m = re.match(r"^(.+)_([A-Za-z0-9])$", chain_key)
            if m and m.group(1) in {p.stem for p in (CATH_DIR / "chain_pdb").glob("*.pdb")}:
                chain_key = m.group(1)
            out[chain_key] = di_seq
    with open(cache, "w") as f:
        for k, v in out.items():
            f.write(f">{k}\n{v}\n")
    return out


# ---------------------------------------------------------------------------
# Stage: build_windows
# ---------------------------------------------------------------------------

def slice_window(seq: str, anchor: int, half: int = WINDOW_HALF, gap: str = GAP) -> str:
    """Return the 2*half+1 chars centered on anchor; pad with gap on overflow."""
    L = len(seq)
    out = []
    for k in range(anchor - half, anchor + half + 1):
        if 0 <= k < L:
            out.append(seq[k])
        else:
            out.append(gap)
    return "".join(out)


def stage_build_windows(anchors: pd.DataFrame, threed: dict[str, str], mode: str) -> pd.DataFrame:
    """Build per-chain windows. mode in {top1, top3}.

    Returns dataframe with columns:
        chain_key, set, pfam_id, hsf, audit_pass, anchor_idx (0..k-1),
        anchor_pos, w_aa, w_3di
    """
    chain_seqs = json.load(open(CATH_DIR / "chain_seqs.json"))
    rows = []
    for _, r in anchors.iterrows():
        ch = r["chain_key"]
        if ch not in chain_seqs or ch not in threed:
            continue
        aa_seq = chain_seqs[ch]
        di_seq = threed[ch]
        if mode == "top1":
            anchor_list = [int(r["attn_anchor"])]
        else:
            anchor_list = list(r["top3_attn_list"])[:3]
        for k, pos in enumerate(anchor_list):
            rows.append({
                "chain_key": ch,
                "set": r["set"],
                "pfam_id": r["pfam_id"],
                "hsf": r["hsf"],
                "audit_pass": bool(r["audit_pass"]),
                "anchor_idx": k,
                "anchor_pos": pos,
                "w_aa": slice_window(aa_seq, pos),
                "w_3di": slice_window(di_seq, pos),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Stage: residue -> MSA column maps (top-3 same_col label)
# ---------------------------------------------------------------------------

def build_res_to_col_map() -> dict[str, dict[int, int]]:
    """For each chain in each set's _aa.fa, residue index -> MSA column index.

    Foldmason _aa.fa rows: gap-stripped length should equal chain residue count;
    each non-gap position maps that residue to its MSA column.
    """
    res2col: dict[str, dict[int, int]] = {}
    for s in SETS:
        msa = read_fasta(CATH_DIR / "msa" / f"{s}_aa.fa")
        for ch, aln in msa.items():
            mp = {}
            res_idx = 0
            for col_idx, c in enumerate(aln):
                if c != "-":
                    mp[res_idx] = col_idx
                    res_idx += 1
            res2col[ch] = mp
    return res2col


# ---------------------------------------------------------------------------
# Stage: pair_features
# ---------------------------------------------------------------------------

def hamming_norm(a: str, b: str, gap: str = GAP) -> float | None:
    """Hamming over non-gap-non-gap positions / count of those positions."""
    assert len(a) == len(b)
    n_match = 0
    n_pos = 0
    for x, y in zip(a, b):
        if x == gap or y == gap:
            continue
        n_pos += 1
        if x != y:
            n_match += 1
    if n_pos == 0:
        return None
    return n_match / n_pos


def stage_pair_features(
    pairs: pd.DataFrame,
    windows: pd.DataFrame,
    mode: str,
    audit_only: bool,
    res2col: dict[str, dict[int, int]] | None = None,
    anchors: pd.DataFrame | None = None,
) -> pd.DataFrame:
    win_by_chain: dict[str, list[dict]] = defaultdict(list)
    for _, r in windows.iterrows():
        win_by_chain[r["chain_key"]].append({
            "anchor_pos": int(r["anchor_pos"]),
            "w_aa": r["w_aa"],
            "w_3di": r["w_3di"],
        })

    if audit_only:
        keep = set(windows.loc[windows["audit_pass"], "chain_key"])
        pairs = pairs[pairs["i"].isin(keep) & pairs["j"].isin(keep)].copy()
    else:
        keep = set(windows["chain_key"])
        pairs = pairs[pairs["i"].isin(keep) & pairs["j"].isin(keep)].copy()

    out_rows = []
    for _, r in pairs.iterrows():
        wi = win_by_chain.get(r["i"], [])
        wj = win_by_chain.get(r["j"], [])
        if not wi or not wj:
            continue

        if mode == "top1":
            wi = wi[:1]
            wj = wj[:1]

        d_aa_list = []
        d_di_list = []
        for a in wi:
            for b in wj:
                d_aa = hamming_norm(a["w_aa"], b["w_aa"])
                d_di = hamming_norm(a["w_3di"], b["w_3di"])
                if d_aa is not None and d_di is not None:
                    d_aa_list.append(d_aa)
                    d_di_list.append(d_di)
        if not d_aa_list:
            continue

        d_aa_min = min(d_aa_list)
        d_di_min = min(d_di_list)

        # Same-col label is always derived from primary (top-1) anchor column.
        # Reasoning: under min-over-9 the label inflates dramatically (27% -> 72% in
        # cross_pfam_same_hsf), changing what "same column" means. We keep the label
        # fixed to top-1 and let top-3 windows compete on the SAME prediction target.
        same_col_pm2 = int(r["same_col_pm2"])
        same_col = int(r["same_col"])

        out_rows.append({
            "i": r["i"],
            "j": r["j"],
            "tm": float(r["tm"]),
            "seqid": float(r["seqid"]),
            "d_aa": d_aa_min,
            "d_3di": d_di_min,
            "same_col": same_col,
            "same_col_pm2": same_col_pm2,
            "stratum": r["stratum"],
            "pfam_i": r["pfam_i"],
            "pfam_j": r["pfam_j"],
            "set_i": r["set_i"],
            "set_j": r["set_j"],
        })
    return pd.DataFrame(out_rows)


# ---------------------------------------------------------------------------
# Stage: regression
# ---------------------------------------------------------------------------

def fit_logit(df: pd.DataFrame, formula: str, cluster_col: str | None = None):
    import statsmodels.formula.api as smf
    if df.empty or df["same_col_pm2"].nunique() < 2:
        return None
    try:
        if cluster_col is not None:
            mod = smf.logit(formula, data=df).fit(
                disp=0,
                cov_type="cluster",
                cov_kwds={"groups": df[cluster_col].values},
                method="bfgs",
                maxiter=200,
            )
        else:
            mod = smf.logit(formula, data=df).fit(disp=0, method="bfgs", maxiter=200)
        return mod
    except Exception as e:
        print(f"  fit failed for `{formula}`: {e}")
        return None


def mcfadden_r2(model) -> float | None:
    if model is None:
        return None
    try:
        ll = model.llf
        ll0 = model.llnull
        return 1.0 - ll / ll0
    except Exception:
        return None


def chain_bootstrap_dr2(df: pd.DataFrame, formula_full: str, formula_null: str,
                       n_boot: int = 200, seed: int = 0) -> tuple[float, float]:
    """Resample chains (not pairs); refit and compute ΔR². Return (lo, hi) 95% CI."""
    rng = np.random.default_rng(seed)
    chains = pd.unique(pd.concat([df["i"], df["j"]]))
    drs = []
    for _ in range(n_boot):
        sample = rng.choice(chains, size=len(chains), replace=True)
        sample_set = set(sample)
        # Boot pairs where both endpoints are in the sample (with multiplicity)
        # Use a count-based weight (multinomial) — simpler: filter to pairs in sample
        sub = df[df["i"].isin(sample_set) & df["j"].isin(sample_set)]
        if len(sub) < 30 or sub["same_col_pm2"].nunique() < 2:
            continue
        m_full = fit_logit(sub, formula_full)
        m_null = fit_logit(sub, formula_null)
        r_full = mcfadden_r2(m_full)
        r_null = mcfadden_r2(m_null)
        if r_full is None or r_null is None:
            continue
        drs.append(r_full - r_null)
    if not drs:
        return float("nan"), float("nan")
    return float(np.percentile(drs, 2.5)), float(np.percentile(drs, 97.5))


def stage_regression(pf: pd.DataFrame, mode: str) -> pd.DataFrame:
    rows = []
    strata_with_signal = ["within_pfam", "cross_pfam_same_hsf"]
    formulae = {
        "M0": "same_col_pm2 ~ tm",
        "M1_AA": "same_col_pm2 ~ tm + d_aa",
        "M1_3Di": "same_col_pm2 ~ tm + d_3di",
        "M2": "same_col_pm2 ~ tm + d_aa + d_3di",
    }

    def run_block(sub: pd.DataFrame, stratum: str, tm_range: str):
        # Cluster on chain i (single-side); approximate dyadic clustering
        for name, f in formulae.items():
            mod = fit_logit(sub, f, cluster_col="i")
            r2 = mcfadden_r2(mod)
            if mod is None:
                rows.append({
                    "mode": mode, "stratum": stratum, "tm_range": tm_range,
                    "model": name, "n": len(sub), "r2": None, "params": None, "se": None,
                })
                continue
            params = {p: float(mod.params.get(p, np.nan)) for p in mod.params.index}
            ses = {p: float(mod.bse.get(p, np.nan)) for p in mod.bse.index}
            rows.append({
                "mode": mode, "stratum": stratum, "tm_range": tm_range,
                "model": name, "n": len(sub),
                "r2": r2,
                "params": json.dumps(params),
                "se": json.dumps(ses),
            })

        # ΔR² CIs (chain bootstrap) for M1_AA and M1_3Di vs M0
        for name, f in [("M1_AA", formulae["M1_AA"]), ("M1_3Di", formulae["M1_3Di"])]:
            lo, hi = chain_bootstrap_dr2(sub, f, formulae["M0"])
            rows.append({
                "mode": mode, "stratum": stratum, "tm_range": tm_range,
                "model": f"dR2_{name}_vs_M0_CI", "n": len(sub),
                "r2": None, "params": json.dumps({"lo": lo, "hi": hi}), "se": None,
            })

    for stratum in strata_with_signal:
        sub = pf[pf["stratum"] == stratum].copy()
        run_block(sub, stratum, "all")
        sub_tm = sub[(sub["tm"] >= 0.3) & (sub["tm"] <= 0.8)]
        run_block(sub_tm, stratum, "tm03_08")

    # Combined: within ∪ cross_pfam_same_hsf
    combined = pf[pf["stratum"].isin(strata_with_signal)].copy()
    run_block(combined, "within_or_cross_pfam_same_hsf", "all")
    run_block(combined[(combined["tm"] >= 0.3) & (combined["tm"] <= 0.8)],
              "within_or_cross_pfam_same_hsf", "tm03_08")

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Stage: cv (leave-one-Pfam-out AUC)
# ---------------------------------------------------------------------------

def stage_lopo_cv(pf: pd.DataFrame, mode: str) -> pd.DataFrame:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score

    rows = []
    feature_sets = {
        "M0": ["tm"],
        "M1_AA": ["tm", "d_aa"],
        "M1_3Di": ["tm", "d_3di"],
        "M2": ["tm", "d_aa", "d_3di"],
    }
    strata = ["within_pfam", "cross_pfam_same_hsf", "within_or_cross_pfam_same_hsf"]
    for stratum in strata:
        if stratum == "within_or_cross_pfam_same_hsf":
            sub = pf[pf["stratum"].isin(["within_pfam", "cross_pfam_same_hsf"])].copy()
        else:
            sub = pf[pf["stratum"] == stratum].copy()
        if sub.empty or sub["same_col_pm2"].nunique() < 2:
            continue
        pfams = sorted(set(sub["pfam_i"]) | set(sub["pfam_j"]))
        for tm_range, lo, hi in [("all", -np.inf, np.inf), ("tm03_08", 0.3, 0.8)]:
            df = sub[(sub["tm"] >= lo) & (sub["tm"] <= hi)].copy()
            if df.empty or df["same_col_pm2"].nunique() < 2:
                continue
            for name, feats in feature_sets.items():
                preds, ys = [], []
                for fold in pfams:
                    mask_test = (df["pfam_i"] == fold) | (df["pfam_j"] == fold)
                    train, test = df[~mask_test], df[mask_test]
                    if train.empty or test.empty:
                        continue
                    if train["same_col_pm2"].nunique() < 2:
                        continue
                    if test["same_col_pm2"].nunique() < 2:
                        # still useful to predict; keep
                        pass
                    X_tr = train[feats].values
                    y_tr = train["same_col_pm2"].values
                    X_te = test[feats].values
                    y_te = test["same_col_pm2"].values
                    clf = LogisticRegression(max_iter=500).fit(X_tr, y_tr)
                    p = clf.predict_proba(X_te)[:, 1]
                    preds.extend(p.tolist())
                    ys.extend(y_te.tolist())
                if len(set(ys)) < 2:
                    auc = None
                else:
                    auc = float(roc_auc_score(ys, preds))
                rows.append({
                    "mode": mode, "stratum": stratum, "tm_range": tm_range,
                    "model": name, "n_test_pairs": len(ys),
                    "auc": auc,
                })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Stage: shuffled null
# ---------------------------------------------------------------------------

def stage_shuffled_null(
    pairs: pd.DataFrame, windows: pd.DataFrame, mode: str, audit_only: bool,
    res2col: dict[str, dict[int, int]] | None, n_perm: int = 200, seed: int = 0,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    win_by_chain: dict[str, list[dict]] = defaultdict(list)
    for _, r in windows.iterrows():
        win_by_chain[r["chain_key"]].append({
            "anchor_pos": int(r["anchor_pos"]),
            "w_aa": r["w_aa"],
            "w_3di": r["w_3di"],
        })
    chains = list(win_by_chain.keys())
    rows = []
    base_pf = stage_pair_features(pairs, windows, mode, audit_only, res2col=res2col)
    base_pf = base_pf[base_pf["stratum"].isin(["within_pfam", "cross_pfam_same_hsf"])].copy()
    if base_pf.empty:
        return pd.DataFrame()

    for p in range(n_perm):
        perm = rng.permutation(len(chains))
        mapping = {chains[k]: chains[perm[k]] for k in range(len(chains))}
        # Rebuild win_by_chain shuffled
        sw_rows = windows.copy()
        sw_rows["chain_key_orig"] = sw_rows["chain_key"]
        sw_rows["chain_key"] = sw_rows["chain_key"].map(mapping)
        # but pairs.csv references chain_key_orig; we want to swap windows but keep pair labels
        # → equivalent: replace win_by_chain with shuffled mapping on the fly
        shuffled_win_by_chain = {orig: win_by_chain[mapping[orig]] for orig in chains}

        # Compute features against base pairs using shuffled windows
        sub_rows = []
        pf_pairs = pairs[pairs["i"].isin(set(chains)) & pairs["j"].isin(set(chains))]
        for _, r in pf_pairs.iterrows():
            wi = shuffled_win_by_chain.get(r["i"], [])
            wj = shuffled_win_by_chain.get(r["j"], [])
            if not wi or not wj:
                continue
            if mode == "top1":
                wi = wi[:1]; wj = wj[:1]
            d_aa_list, d_di_list = [], []
            for a in wi:
                for b in wj:
                    da = hamming_norm(a["w_aa"], b["w_aa"])
                    dd = hamming_norm(a["w_3di"], b["w_3di"])
                    if da is not None and dd is not None:
                        d_aa_list.append(da); d_di_list.append(dd)
            if not d_aa_list:
                continue
            sub_rows.append({
                "tm": float(r["tm"]), "d_aa": min(d_aa_list), "d_3di": min(d_di_list),
                "same_col_pm2": int(r["same_col_pm2"]), "stratum": r["stratum"],
                "i": r["i"], "j": r["j"],
            })
        sub = pd.DataFrame(sub_rows)
        sub = sub[sub["stratum"].isin(["within_pfam", "cross_pfam_same_hsf"])]
        if sub.empty or sub["same_col_pm2"].nunique() < 2:
            continue
        m0 = fit_logit(sub, "same_col_pm2 ~ tm")
        m_aa = fit_logit(sub, "same_col_pm2 ~ tm + d_aa")
        m_di = fit_logit(sub, "same_col_pm2 ~ tm + d_3di")
        r0 = mcfadden_r2(m0); ra = mcfadden_r2(m_aa); rd = mcfadden_r2(m_di)
        rows.append({
            "perm": p,
            "dR2_AA": (ra - r0) if (ra is not None and r0 is not None) else None,
            "dR2_3Di": (rd - r0) if (rd is not None and r0 is not None) else None,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Stage: aux clustering (HDBSCAN NMI/ARI)
# ---------------------------------------------------------------------------

def onehot(seqs: list[str], alphabet: list[str]) -> np.ndarray:
    a2i = {c: k for k, c in enumerate(alphabet)}
    L = len(seqs[0])
    n = len(seqs)
    A = len(alphabet)
    out = np.zeros((n, L * A), dtype=np.float64)
    for i, s in enumerate(seqs):
        for j, c in enumerate(s):
            k = a2i.get(c, a2i[GAP])
            out[i, j * A + k] = 1.0
    return out


def stage_aux_clustering(windows: pd.DataFrame, anchors: pd.DataFrame,
                         audit_only: bool, mode: str) -> pd.DataFrame:
    """HDBSCAN on AA and 3Di window encodings, NMI vs labels."""
    import hdbscan
    from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

    if mode == "top1":
        sub = windows[windows["anchor_idx"] == 0].copy()
    else:
        sub = windows.copy()
    if audit_only:
        sub = sub[sub["audit_pass"]].copy()

    rows = []
    chains = sub["chain_key"].tolist()
    pfam_labels = sub["pfam_id"].astype("category").cat.codes.values
    set_labels = sub["set"].astype("category").cat.codes.values

    for label_name, labels in [("pfam", pfam_labels), ("set", set_labels)]:
        if len(set(labels)) < 2:
            continue
        for alpha_name, alphabet, seq_col in [
            ("aa", AA_ALPHABET, "w_aa"),
            ("3di", DI_ALPHABET, "w_3di"),
        ]:
            X = onehot(sub[seq_col].tolist(), alphabet)
            n = X.shape[0]
            mcs = max(3, n // 12)
            try:
                clusterer = hdbscan.HDBSCAN(
                    min_cluster_size=mcs, min_samples=2, metric="cosine",
                    cluster_selection_method="eom", algorithm="generic",
                )
                pred = clusterer.fit_predict(X)
            except Exception as e:
                print(f"  HDBSCAN failed ({alpha_name} vs {label_name}): {e}")
                continue
            mask = pred != -1
            if mask.sum() < 2 or len(set(pred[mask])) < 2:
                nmi = ari = None
            else:
                nmi = float(normalized_mutual_info_score(labels[mask], pred[mask]))
                ari = float(adjusted_rand_score(labels[mask], pred[mask]))
            rows.append({
                "mode": mode, "alphabet": alpha_name, "label": label_name,
                "n": n, "mcs": mcs,
                "n_clusters": int(len(set(pred)) - (1 if -1 in pred else 0)),
                "n_noise": int((pred == -1).sum()),
                "nmi": nmi, "ari": ari,
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Stage: per-set IC at modal anchor column
# ---------------------------------------------------------------------------

def stage_ic_per_set(anchors: pd.DataFrame, audit_only: bool) -> pd.DataFrame:
    """IC_3Di and IC_AA at the modal anchor column per set."""
    rows = []
    for s in SETS:
        sub_chains = anchors[anchors["set"] == s].copy()
        if audit_only:
            sub_chains = sub_chains[sub_chains["audit_pass"]]
        if sub_chains.empty:
            continue
        msa_aa = read_fasta(CATH_DIR / "msa" / f"{s}_aa.fa")
        msa_di = read_fasta(CATH_DIR / "msa" / f"{s}_3di.fa")
        # residue idx -> col idx per chain
        chain_res2col: dict[str, dict[int, int]] = {}
        for ch, aln in msa_aa.items():
            mp = {}
            ridx = 0
            for cidx, c in enumerate(aln):
                if c != "-":
                    mp[ridx] = cidx
                    ridx += 1
            chain_res2col[ch] = mp
        cols = []
        for _, r in sub_chains.iterrows():
            mp = chain_res2col.get(r["chain_key"])
            if mp is None:
                continue
            c = mp.get(int(r["attn_anchor"]))
            if c is not None:
                cols.append(c)
        if not cols:
            continue
        modal_col = max(set(cols), key=cols.count)

        def col_ic(msa: dict[str, str], col: int, alphabet: list[str]) -> float:
            chars = [aln[col] for ch, aln in msa.items()
                     if ch in set(sub_chains["chain_key"]) and col < len(aln) and aln[col] != "-"]
            if not chars:
                return 0.0
            from collections import Counter
            counts = Counter(chars)
            n = sum(counts.values())
            ps = np.array([counts[c] / n for c in alphabet if c != GAP and counts[c] > 0])
            entropy = -np.sum(ps * np.log2(ps + 1e-12))
            max_entropy = np.log2(len([c for c in alphabet if c != GAP]))
            return float(max_entropy - entropy)

        ic_aa = col_ic(msa_aa, modal_col, AA_ALPHABET)
        ic_di = col_ic(msa_di, modal_col, DI_ALPHABET)
        rows.append({
            "set": s, "n_chains": len(sub_chains), "modal_col": modal_col,
            "ic_aa": ic_aa, "ic_3di": ic_di,
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def stage_plots(reg: pd.DataFrame, lopo: pd.DataFrame, ic: pd.DataFrame,
                pf: pd.DataFrame, mode: str, tag: str, out_dir: Path) -> None:
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))

    # Panel 1: ΔR² bars per stratum, M1_AA and M1_3Di vs M0
    ax = axes[0, 0]
    strata = ["within_pfam", "cross_pfam_same_hsf", "within_or_cross_pfam_same_hsf"]
    width = 0.35
    xs = np.arange(len(strata))
    drs_aa = []
    drs_3di = []
    err_aa_lo, err_aa_hi = [], []
    err_3di_lo, err_3di_hi = [], []
    for s in strata:
        r0 = reg[(reg["stratum"] == s) & (reg["model"] == "M0") & (reg["tm_range"] == "all")]["r2"].values
        ra = reg[(reg["stratum"] == s) & (reg["model"] == "M1_AA") & (reg["tm_range"] == "all")]["r2"].values
        rd = reg[(reg["stratum"] == s) & (reg["model"] == "M1_3Di") & (reg["tm_range"] == "all")]["r2"].values
        r0v = float(r0[0]) if len(r0) and r0[0] is not None and not pd.isna(r0[0]) else 0.0
        rav = float(ra[0]) if len(ra) and ra[0] is not None and not pd.isna(ra[0]) else 0.0
        rdv = float(rd[0]) if len(rd) and rd[0] is not None and not pd.isna(rd[0]) else 0.0
        drs_aa.append(rav - r0v)
        drs_3di.append(rdv - r0v)

        ci_aa = reg[(reg["stratum"] == s) & (reg["model"] == "dR2_M1_AA_vs_M0_CI") & (reg["tm_range"] == "all")]
        ci_3d = reg[(reg["stratum"] == s) & (reg["model"] == "dR2_M1_3Di_vs_M0_CI") & (reg["tm_range"] == "all")]
        try:
            ci_aa_d = json.loads(ci_aa["params"].values[0])
            err_aa_lo.append(max(0, (rav - r0v) - ci_aa_d["lo"]))
            err_aa_hi.append(max(0, ci_aa_d["hi"] - (rav - r0v)))
        except Exception:
            err_aa_lo.append(0); err_aa_hi.append(0)
        try:
            ci_3d_d = json.loads(ci_3d["params"].values[0])
            err_3di_lo.append(max(0, (rdv - r0v) - ci_3d_d["lo"]))
            err_3di_hi.append(max(0, ci_3d_d["hi"] - (rdv - r0v)))
        except Exception:
            err_3di_lo.append(0); err_3di_hi.append(0)

    ax.bar(xs - width / 2, drs_aa, width, yerr=[err_aa_lo, err_aa_hi], label="ΔR² M1_AA vs M0", color="#888")
    ax.bar(xs + width / 2, drs_3di, width, yerr=[err_3di_lo, err_3di_hi], label="ΔR² M1_3Di vs M0", color="#1f77b4")
    ax.axhline(0.05, linestyle="--", color="red", linewidth=0.8)
    ax.set_xticks(xs)
    ax.set_xticklabels([s.replace("_", "\n") for s in strata], fontsize=8)
    ax.set_ylabel("ΔR² over M0(tm)")
    ax.set_title(f"ΔR² by stratum [{mode}]")
    ax.legend(fontsize=8)

    # Panel 2: LOPO AUC by model, in cross_pfam_same_hsf stratum
    ax = axes[0, 1]
    for stratum, ls in [("cross_pfam_same_hsf", "-"), ("within_or_cross_pfam_same_hsf", ":")]:
        models = ["M0", "M1_AA", "M1_3Di", "M2"]
        aucs = []
        for m in models:
            row = lopo[(lopo["stratum"] == stratum) & (lopo["tm_range"] == "all") & (lopo["model"] == m)]
            aucs.append(row["auc"].values[0] if len(row) else None)
        aucs_plot = [a if a is not None else 0 for a in aucs]
        ax.plot(models, aucs_plot, marker="o", linestyle=ls, label=stratum)
    ax.axhline(0.75, linestyle="--", color="red", linewidth=0.8)
    ax.set_ylabel("LOPO-CV AUC")
    ax.set_ylim(0.4, 1.0)
    ax.set_title(f"LOPO-CV AUC [{mode}]")
    ax.legend(fontsize=8)

    # Panel 3: per-set IC bars
    ax = axes[1, 0]
    if not ic.empty:
        sets = ic["set"].tolist()
        xs2 = np.arange(len(sets))
        ax.bar(xs2 - 0.2, ic["ic_aa"], 0.4, label="IC AA", color="#888")
        ax.bar(xs2 + 0.2, ic["ic_3di"], 0.4, label="IC 3Di", color="#1f77b4")
        ax.set_xticks(xs2)
        ax.set_xticklabels([s.split("_")[0] for s in sets])
        ax.set_ylabel("IC at modal anchor column (bits)")
        ax.set_title("Per-set IC at modal anchor column")
        ax.legend(fontsize=8)
    else:
        ax.text(0.5, 0.5, "no IC data", ha="center", transform=ax.transAxes)

    # Panel 4: d_aa vs d_3di scatter on cross_pfam_same_hsf, color by same_col_pm2
    ax = axes[1, 1]
    sub = pf[pf["stratum"] == "cross_pfam_same_hsf"]
    if not sub.empty:
        for v, c, lbl in [(0, "#bbb", "diff col"), (1, "#d62728", "same col ±2")]:
            s2 = sub[sub["same_col_pm2"] == v]
            ax.scatter(s2["d_aa"], s2["d_3di"], s=8, alpha=0.4, color=c, label=lbl)
        ax.plot([0, 1], [0, 1], color="k", linewidth=0.5)
        ax.set_xlabel("d_AA (window Hamming)")
        ax.set_ylabel("d_3Di (window Hamming)")
        ax.set_title("AA vs 3Di window distance, cross_pfam_same_hsf")
        ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out_dir / f"fig_main_{tag}.png", dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def write_windows_fasta(windows: pd.DataFrame, out_dir: Path, tag: str) -> None:
    with open(out_dir / f"windows_aa_{tag}.fa", "w") as f:
        for _, r in windows.iterrows():
            f.write(f">{r['chain_key']}|k={r['anchor_idx']}|pos={r['anchor_pos']}\n{r['w_aa']}\n")
    with open(out_dir / f"windows_3di_{tag}.fa", "w") as f:
        for _, r in windows.iterrows():
            f.write(f">{r['chain_key']}|k={r['anchor_idx']}|pos={r['anchor_pos']}\n{r['w_3di']}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["top1", "top3"], default="top1")
    ap.add_argument("--all-chains", action="store_true",
                    help="Run on full corpus (n=129) instead of audit-pass (n=74)")
    ap.add_argument("--skip-foldseek-check", action="store_true",
                    help="Skip foldseek cross-check (length check still runs)")
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--stages", default="all",
                    help="comma-separated subset: extract,windows,pairs,reg,cv,aux,ic,null,plots")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    audit_only = not args.all_chains
    mode = args.mode
    tag = f"{mode}_{'audit' if audit_only else 'all'}"
    print(f"=== anchor_e3_cath_repl tag={tag} ===")

    stages_run = set(args.stages.split(",")) if args.stages != "all" else {
        "extract", "windows", "pairs", "reg", "cv", "aux", "ic", "null", "plots"
    }

    # Stage extract
    if "extract" in stages_run or not (OUT_DIR / "foldseek_3di.fa").exists():
        if args.skip_foldseek_check:
            chain_seqs = json.load(open(CATH_DIR / "chain_seqs.json"))
            threed: dict[str, str] = {}
            for s in SETS:
                msa3di = read_fasta(CATH_DIR / "msa" / f"{s}_3di.fa")
                for ch, aln in msa3di.items():
                    threed.setdefault(ch, aln.replace("-", ""))
            bad = [(c, len(chain_seqs[c]), len(threed[c])) for c in threed
                   if c in chain_seqs and len(chain_seqs[c]) != len(threed[c])]
            if bad:
                raise SystemExit(f"Length mismatch: {bad[:10]}")
            print(f"[extract_3di] {len(threed)} chains, length check passed (foldseek skipped)")
        else:
            threed = stage_extract_3di()
    else:
        threed = read_fasta(OUT_DIR / "foldseek_3di.fa") if (OUT_DIR / "foldseek_3di.fa").exists() else {}

    anchors = load_anchors()
    pairs = load_pairs(all_chains=args.all_chains)

    # Stage windows
    windows = stage_build_windows(anchors, threed, mode=mode)
    write_windows_fasta(windows, OUT_DIR, tag)
    print(f"[windows] {len(windows)} windows ({mode}); audit-pass chains: {windows['audit_pass'].sum()}")

    # res2col map needed for top3 same_col label
    res2col = build_res_to_col_map() if mode == "top3" else None

    # Stage pair_features
    pf = stage_pair_features(pairs, windows, mode=mode, audit_only=audit_only,
                             res2col=res2col, anchors=anchors)
    pf_path = OUT_DIR / f"pair_features_{tag}.csv"
    pf.to_csv(pf_path, index=False)
    print(f"[pair_features] {len(pf)} pairs -> {pf_path}")
    print(pf.groupby("stratum")["same_col_pm2"].agg(["count", "mean"]))

    # Stage regression
    if "reg" in stages_run:
        reg = stage_regression(pf, mode=mode)
        reg.to_csv(OUT_DIR / f"regression_table_{tag}.csv", index=False)
        print(f"[regression] -> regression_table_{tag}.csv")
    else:
        reg = pd.read_csv(OUT_DIR / f"regression_table_{tag}.csv") if (OUT_DIR / f"regression_table_{tag}.csv").exists() else pd.DataFrame()

    # Stage CV
    if "cv" in stages_run:
        lopo = stage_lopo_cv(pf, mode=mode)
        lopo.to_csv(OUT_DIR / f"lopo_auc_{tag}.csv", index=False)
        print(f"[cv] -> lopo_auc_{tag}.csv")
    else:
        lopo = pd.read_csv(OUT_DIR / f"lopo_auc_{tag}.csv") if (OUT_DIR / f"lopo_auc_{tag}.csv").exists() else pd.DataFrame()

    # Stage IC
    if "ic" in stages_run:
        ic = stage_ic_per_set(anchors, audit_only=audit_only)
        ic.to_csv(OUT_DIR / f"ic_per_set_{tag}.csv", index=False)
        print(f"[ic] -> ic_per_set_{tag}.csv")
    else:
        ic = pd.read_csv(OUT_DIR / f"ic_per_set_{tag}.csv") if (OUT_DIR / f"ic_per_set_{tag}.csv").exists() else pd.DataFrame()

    # Stage aux clustering
    if "aux" in stages_run:
        nmi = stage_aux_clustering(windows, anchors, audit_only=audit_only, mode=mode)
        nmi.to_csv(OUT_DIR / f"hdbscan_nmi_{tag}.csv", index=False)
        print(f"[aux] -> hdbscan_nmi_{tag}.csv")

    # Stage shuffled null
    if "null" in stages_run:
        null = stage_shuffled_null(pairs, windows, mode=mode, audit_only=audit_only,
                                   res2col=res2col, n_perm=args.n_perm)
        null.to_csv(OUT_DIR / f"shuffled_null_{tag}.csv", index=False)
        print(f"[null] -> shuffled_null_{tag}.csv  (n_perm={len(null)})")

    # Plots
    if "plots" in stages_run and not reg.empty:
        stage_plots(reg, lopo, ic, pf, mode=mode, tag=tag, out_dir=OUT_DIR)
        print(f"[plots] -> fig_main_{tag}.png")


if __name__ == "__main__":
    main()
