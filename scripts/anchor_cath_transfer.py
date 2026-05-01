"""CATH-based cross-fold anchor transfer experiment.

Stages (run with --stage <name>):
  download   download PDBs for manifest
  extract    extract per-chain FASTA + single-chain PDB files
  anchors    run ESM L10H9 inference per chain; save anchors + audit metrics
  msa        run foldmason easy-msa per set (A, B, C) and combined (A+B+C)
  concord    map anchors to MSA columns, compute concordance metrics
  all        run all stages in order

Inputs : data/cath/struc_transfer_manifest.csv
Outputs: reports/out2/cath_transfer/
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/work/pi_annagreen_umass_edu/jatin/plm_nnsight")
MANIFEST = ROOT / "data/cath/struc_transfer_manifest.csv"
OUT_DIR = ROOT / "reports/out2/cath_transfer"
PDB_DIR = OUT_DIR / "pdb"
CHAIN_DIR = OUT_DIR / "chain_pdb"
SEQ_FILE = OUT_DIR / "chain_seqs.json"
ANCHOR_FILE = OUT_DIR / "anchors.csv"
MSA_DIR = OUT_DIR / "msa"
FOLDMASON = ROOT / "foldmason/bin/foldmason"

TARGET_LAYER = 10
TARGET_HEAD = 9

REFERENCE_PROTEIN = "2B61A"
REFERENCE_PDB = ROOT / "data/2B61A_EV/structures/2b61.pdb"


# --------------------------------------------------------------------------
# Stage: download PDBs
# --------------------------------------------------------------------------
def stage_download(manifest: pd.DataFrame) -> None:
    import requests
    PDB_DIR.mkdir(parents=True, exist_ok=True)
    for pdb in manifest.pdb.unique():
        out = PDB_DIR / f"{pdb}.pdb"
        if out.exists() and out.stat().st_size > 0:
            continue
        url = f"https://files.rcsb.org/download/{pdb.upper()}.pdb"
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            out.write_bytes(r.content)
        except Exception as e:
            cif = PDB_DIR / f"{pdb}.cif"
            try:
                r = requests.get(f"https://files.rcsb.org/download/{pdb.upper()}.cif", timeout=30)
                r.raise_for_status()
                cif.write_bytes(r.content)
            except Exception as e2:
                print(f"  FAILED {pdb}: pdb={e}; cif={e2}")
    n_pdb = len(list(PDB_DIR.glob("*.pdb"))); n_cif = len(list(PDB_DIR.glob("*.cif")))
    print(f"[download] {n_pdb} pdb / {n_cif} cif files in {PDB_DIR}")


# --------------------------------------------------------------------------
# Stage: extract per-chain FASTA + single-chain PDB files
# --------------------------------------------------------------------------
def _three_to_one() -> dict[str, str]:
    return {
        "ALA":"A","CYS":"C","ASP":"D","GLU":"E","PHE":"F","GLY":"G","HIS":"H",
        "ILE":"I","LYS":"K","LEU":"L","MET":"M","ASN":"N","PRO":"P","GLN":"Q",
        "ARG":"R","SER":"S","THR":"T","VAL":"V","TRP":"W","TYR":"Y",
        "MSE":"M","SEC":"U","PYL":"O",
    }


def stage_extract(manifest: pd.DataFrame) -> None:
    """For each (pdb,chain), write a single-chain PDB (chain.pdb) and per-chain seq."""
    from Bio.PDB import PDBParser, MMCIFParser, PDBIO, Select
    warnings.filterwarnings("ignore")
    CHAIN_DIR.mkdir(parents=True, exist_ok=True)
    aa3 = _three_to_one()

    seqs: dict[str, str] = {}
    fail = []

    class ChainSel(Select):
        def __init__(self, chain_id): self.chain_id = chain_id
        def accept_chain(self, chain): return chain.id == self.chain_id
        def accept_residue(self, res): return res.id[0] == ' '  # std residues only

    for r in manifest.itertuples(index=False):
        chain_key = f"{r.pdb}_{r.chain}"
        out_pdb = CHAIN_DIR / f"{chain_key}.pdb"
        pdb_path = PDB_DIR / f"{r.pdb}.pdb"
        cif_path = PDB_DIR / f"{r.pdb}.cif"

        if pdb_path.exists():
            try:
                parser = PDBParser(QUIET=True)
                struct = parser.get_structure(r.pdb, str(pdb_path))
            except Exception as e:
                fail.append((chain_key, f"pdb-parse:{e}"))
                continue
        elif cif_path.exists():
            try:
                parser = MMCIFParser(QUIET=True)
                struct = parser.get_structure(r.pdb, str(cif_path))
            except Exception as e:
                fail.append((chain_key, f"cif-parse:{e}"))
                continue
        else:
            fail.append((chain_key, "no-file")); continue

        model = next(struct.get_models())
        try:
            chain = model[r.chain]
        except KeyError:
            fail.append((chain_key, f"chain-missing:{r.chain}")); continue

        # extract sequence (only standard residues with CA)
        seq_chars = []
        for res in chain.get_residues():
            if res.id[0] != ' ': continue
            if 'CA' not in res: continue
            three = res.get_resname()
            seq_chars.append(aa3.get(three, 'X'))
        seq = "".join(seq_chars)
        if len(seq) < 30:
            fail.append((chain_key, f"too-short:{len(seq)}")); continue
        seqs[chain_key] = seq

        # write single-chain PDB
        if not out_pdb.exists():
            io = PDBIO(); io.set_structure(struct)
            io.save(str(out_pdb), ChainSel(r.chain))

    SEQ_FILE.write_text(json.dumps(seqs))
    print(f"[extract] {len(seqs)} chains seq+pdb; failures={len(fail)}")
    if fail:
        for k,v in fail[:8]:
            print(f"  fail {k}: {v}")


# --------------------------------------------------------------------------
# Stage: ESM anchor inference
# --------------------------------------------------------------------------
def _load_model(device: str):
    sys.path.insert(0, str(ROOT / "scripts"))
    from anchor_hmm_experiment import load_model, extract_head_weights, compute_search_dir, load_sequences
    from nnsight import NNsight
    raw_model, tok = load_model(device)
    weights = extract_head_weights(raw_model, TARGET_LAYER, TARGET_HEAD)
    seqs = load_sequences()
    # compute d_ref using raw HF model (compute_search_dir uses traditional forward, not nnsight trace)
    d_ref = compute_search_dir(raw_model, tok, " ".join(seqs[REFERENCE_PROTEIN]),
                               weights, device=device)
    model = NNsight(raw_model)
    return model, tok, weights, d_ref


def _compute_anchor(model, tok, weights, d_ref, sequence: str, device: str) -> dict:
    import torch
    from scipy import stats as sp_stats
    attn_mod = model.esm.encoder.layer[TARGET_LAYER].attention.self
    ln_mod = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    inputs = tok(sequence, return_tensors="pt").to(device)
    n = len(sequence)
    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=[attn_mod, ln_mod])
    ak = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    lk = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    A = cache[ak].output[1].detach().cpu()[0, TARGET_HEAD, 1:-1, 1:-1]
    x_ln = cache[lk].output.detach().cpu()[0, 1:-1]
    proj = (x_ln @ d_ref.cpu()).numpy()

    mean_key = A.mean(dim=0).numpy()
    sorted_mk = np.sort(mean_key)[::-1]
    top1_mass = float(sorted_mk[0])
    top3_mass = float(sorted_mk[:3].sum())
    p = mean_key / (mean_key.sum() + 1e-12)
    ent = -float(np.sum(p * np.log(p + 1e-12)))
    eff_keys = float(np.exp(ent))
    # keys_50pct
    cum = 0.0; keys_50 = 0
    for x in sorted_mk:
        cum += x; keys_50 += 1
        if cum >= 0.5: break

    attn_rank = np.argsort(-mean_key)
    attn_argmax = int(attn_rank[0])
    top3_attn = [int(x) for x in attn_rank[:3]]
    proj_argmax = int(np.argmax(proj))
    rho, _ = sp_stats.spearmanr(mean_key, proj)
    return {
        "n_res": n,
        "top1_mass": top1_mass,
        "top3_mass": top3_mass,
        "eff_keys": eff_keys,
        "keys_50pct": int(keys_50),
        "attn_anchor": attn_argmax,
        "top3_attn": ",".join(str(x) for x in top3_attn),
        "proj_anchor": proj_argmax,
        "argmax_agree": int(attn_argmax == proj_argmax),
        "spearman_d_attn": float(rho) if rho is not None else float('nan'),
        "anchor_aa": sequence[attn_argmax],
    }


def stage_anchors(manifest: pd.DataFrame, device: str = "cuda") -> None:
    seqs = json.loads(SEQ_FILE.read_text())
    model, tok, weights, d_ref = _load_model(device)
    rows = []
    for r in manifest.itertuples(index=False):
        key = f"{r.pdb}_{r.chain}"
        if key not in seqs:
            continue
        try:
            res = _compute_anchor(model, tok, weights, d_ref, seqs[key], device)
        except Exception as e:
            print(f"  ERR {key}: {e}"); continue
        res.update({"chain_key": key, "set": r.set, "pfam_id": r.pfam_id,
                    "hsf": r.hsf, "pdb": r.pdb, "chain": r.chain})
        rows.append(res)
        if len(rows) % 10 == 0:
            print(f"  [anchors] {len(rows)}/{len(manifest)}")
    df = pd.DataFrame(rows)
    df.to_csv(ANCHOR_FILE, index=False)
    print(f"[anchors] wrote {len(df)} rows to {ANCHOR_FILE}")
    # summary
    g = df.groupby("set").agg(
        n=("chain_key","count"),
        top1_mass_med=("top1_mass","median"),
        eff_keys_med=("eff_keys","median"),
        keys50_eq1_frac=("keys_50pct", lambda s: (s==1).mean()),
        argmax_agree_frac=("argmax_agree","mean"),
        rho_med=("spearman_d_attn","median"),
        audit_pass=("top1_mass", lambda s: ((s>=0.5) & (df.loc[s.index,"keys_50pct"]==1)).sum()),
    )
    print("\nPer-set summary:")
    print(g.to_string())


# --------------------------------------------------------------------------
# Stage: foldmason MSA per set + combined
# --------------------------------------------------------------------------
def stage_msa(manifest: pd.DataFrame) -> None:
    MSA_DIR.mkdir(parents=True, exist_ok=True)
    sets = list(manifest.set.unique()) + ["ALL"]
    for set_name in sets:
        out_prefix = MSA_DIR / set_name
        out_aa = MSA_DIR / f"{set_name}_aa.fa"
        if out_aa.exists() and out_aa.stat().st_size > 0:
            print(f"[msa] {set_name} already exists, skipping")
            continue
        if set_name == "ALL":
            sub = manifest
        else:
            sub = manifest[manifest.set == set_name]
        files = []
        for r in sub.itertuples(index=False):
            p = CHAIN_DIR / f"{r.pdb}_{r.chain}.pdb"
            if p.exists():
                files.append(str(p))
        if len(files) < 3:
            print(f"[msa] {set_name}: only {len(files)} chains, skipping")
            continue
        tmpd = MSA_DIR / f"_tmp_{set_name}"
        if tmpd.exists():
            shutil.rmtree(tmpd)
        cmd = [str(FOLDMASON), "easy-msa"] + files + [str(out_prefix), str(tmpd)]
        print(f"[msa] {set_name}: foldmason easy-msa on {len(files)} chains...")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  FAILED ({r.returncode}). stderr tail:\n{r.stderr[-500:]}")
            continue
        # cleanup tmp
        if tmpd.exists():
            shutil.rmtree(tmpd, ignore_errors=True)
        if out_aa.exists():
            print(f"  wrote {out_aa.name}")


# --------------------------------------------------------------------------
# Stage: concordance
# --------------------------------------------------------------------------
def _parse_msa(fasta_path: Path) -> dict[str, str]:
    """Parse FASTA MSA. Headers may have suffixes like '_pdb_A'."""
    out = {}
    name, seq = None, []
    with open(fasta_path) as f:
        for line in f:
            line = line.rstrip()
            if line.startswith(">"):
                if name is not None:
                    out[name] = "".join(seq)
                # canonicalize to chain_key style: take first whitespace-separated token,
                # strip trailing '.pdb' etc.
                name = line[1:].split()[0]
                if name.endswith(".pdb"):
                    name = name[:-4]
                seq = []
            else:
                seq.append(line)
    if name is not None:
        out[name] = "".join(seq)
    return out


def _seq_pos_to_msa_col(aligned: str) -> dict[int, int]:
    """Map ungapped seq position (0-based) -> MSA column (0-based)."""
    out = {}
    seq_pos = 0
    for col, ch in enumerate(aligned):
        if ch != "-":
            out[seq_pos] = col
            seq_pos += 1
    return out


def _concord_metrics(cols: list[int], n_msa_cols: int) -> dict:
    """Top-1 conc, ±2-tolerance, normalized entropy."""
    if not cols:
        return {"n":0,"top1_col":-1,"top1_conc":float('nan'),
                "tol2_conc":float('nan'),"entropy_norm":float('nan')}
    n = len(cols)
    cnt = Counter(cols)
    top_col, top_n = cnt.most_common(1)[0]
    top1_conc = top_n / n
    tol2_conc = sum(1 for c in cols if abs(c - top_col) <= 2) / n
    p = np.array(list(cnt.values()), dtype=float) / n
    H = -float(np.sum(p * np.log2(p + 1e-12)))
    H_max = math.log2(n_msa_cols) if n_msa_cols > 1 else 1.0
    return {"n":n,"top1_col":int(top_col),"top1_conc":float(top1_conc),
            "tol2_conc":float(tol2_conc),"entropy_norm":float(H/H_max)}


def _chain_anchor_cols(row, pos_to_col: dict, top_k: int = 1) -> list[int]:
    """Map a chain's top-k attention positions to MSA columns. Skips unmappable positions."""
    key = row.chain_key
    if key not in pos_to_col: return []
    if top_k == 1:
        positions = [int(row.attn_anchor)]
    else:
        positions = [int(x) for x in str(row.top3_attn).split(",")][:top_k]
    return [pos_to_col[key][p] for p in positions if p in pos_to_col[key]]


def _concord_metrics_topk(rows: list, pos_to_col: dict, n_msa_cols: int, top_k: int) -> dict:
    """Concordance using each chain's top-k attention positions.
    Modal column is computed from chains' top-1 anchor (always); we then ask:
    fraction of chains whose top-k contains a column within ±2 of mode.
    Also: fraction of chains whose top-k EXACTLY contains the mode."""
    top1_cols = []
    topk_cols_per_chain = []
    for r in rows:
        c1 = _chain_anchor_cols(r, pos_to_col, top_k=1)
        ck = _chain_anchor_cols(r, pos_to_col, top_k=top_k)
        if not c1 or not ck: continue
        top1_cols.append(c1[0])
        topk_cols_per_chain.append(ck)
    if not top1_cols:
        return {"n":0,"top1_col":-1,"top1_conc":float('nan'),"tol2_conc":float('nan'),
                "topk_exact_conc":float('nan'),"topk_tol2_conc":float('nan'),
                "entropy_norm":float('nan')}
    n = len(top1_cols)
    cnt = Counter(top1_cols)
    top_col, top_n = cnt.most_common(1)[0]
    top1_conc = top_n / n
    tol2_conc = sum(1 for c in top1_cols if abs(c - top_col) <= 2) / n
    # top-k metrics (any top-k pos near mode)
    topk_exact = sum(1 for cks in topk_cols_per_chain if top_col in cks) / n
    topk_tol2 = sum(1 for cks in topk_cols_per_chain
                    if any(abs(c - top_col) <= 2 for c in cks)) / n
    p = np.array(list(cnt.values()), dtype=float) / n
    H = -float(np.sum(p * np.log2(p + 1e-12)))
    H_max = math.log2(n_msa_cols) if n_msa_cols > 1 else 1.0
    return {"n":n,"top1_col":int(top_col),"top1_conc":float(top1_conc),
            "tol2_conc":float(tol2_conc),"topk_exact_conc":float(topk_exact),
            "topk_tol2_conc":float(topk_tol2),"entropy_norm":float(H/H_max)}


def stage_concord(manifest: pd.DataFrame, audit_only: bool = False) -> None:
    anchors = pd.read_csv(ANCHOR_FILE)
    if audit_only:
        anchors = anchors[(anchors.top1_mass >= 0.5) & (anchors.keys_50pct == 1)]
    sets = ["A_3.40.50.720", "B_3.40.50.1820", "C_2.60.40.10", "ALL"]

    summary_rows = []
    for set_name in sets:
        msa_path = MSA_DIR / f"{set_name}_aa.fa"
        if not msa_path.exists():
            print(f"  no MSA for {set_name}"); continue
        msa = _parse_msa(msa_path)
        # build pos->col map per chain
        pos_to_col = {k: _seq_pos_to_msa_col(v) for k,v in msa.items()}
        n_msa_cols = max(len(v) for v in msa.values())

        if set_name == "ALL":
            sub = anchors  # all chains
        else:
            sub = anchors[anchors.set == set_name]

        def _add(rows_iter, group: str, label: str):
            rows = list(rows_iter)
            m = _concord_metrics_topk(rows, pos_to_col, n_msa_cols, top_k=3)
            m.update({"msa_set": set_name, "group": group, "label": label})
            summary_rows.append(m)

        for pf, g in sub.groupby("pfam_id"):
            _add(g.itertuples(index=False), "pfam", pf)
        for hsf, g in sub.groupby("hsf"):
            _add(g.itertuples(index=False), "hsf", hsf)
        _add(sub.itertuples(index=False), "set", set_name)

        pfams_here = sub.pfam_id.unique()
        for i in range(len(pfams_here)):
            for j in range(i+1, len(pfams_here)):
                pf1, pf2 = pfams_here[i], pfams_here[j]
                gpair = sub[sub.pfam_id.isin([pf1, pf2])]
                _add(gpair.itertuples(index=False), "pfam_pair", f"{pf1}|{pf2}")

    df = pd.DataFrame(summary_rows)
    suffix = "_audit" if audit_only else "_all"
    out_csv = OUT_DIR / f"concordance{suffix}.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n[concord] wrote {out_csv}")
    # Quick text summary: per-set per-group medians
    for grp in ["pfam","hsf","set"]:
        sub = df[df.group == grp]
        if sub.empty: continue
        agg = sub.groupby("msa_set").agg(
            n_groups=("label","count"),
            med_top1=("top1_conc","median"),
            med_tol2=("tol2_conc","median"),
            med_topk_exact=("topk_exact_conc","median"),
            med_topk_tol2=("topk_tol2_conc","median"),
            med_entropy=("entropy_norm","median"),
        )
        print(f"\n{grp.upper()} groups{' (audit-pass only)' if audit_only else ''}:")
        print(agg.to_string())


# --------------------------------------------------------------------------
# Stage: random-shuffle baseline
# --------------------------------------------------------------------------
def stage_baseline(manifest: pd.DataFrame, audit_only: bool = True,
                    n_trials: int = 200, seed: int = 42) -> None:
    """For each group (Pfam, HSF, set) within each MSA, shuffle each chain's anchor to
    a uniform random position within that chain (mapped to MSA col), recompute
    top-1 + top-3 concordance × n_trials. Empirical p = fraction of trials where
    shuffled top1_conc >= observed."""
    anchors = pd.read_csv(ANCHOR_FILE)
    if audit_only:
        anchors = anchors[(anchors.top1_mass >= 0.5) & (anchors.keys_50pct == 1)]
    rng = np.random.default_rng(seed)

    sets = ["A_3.40.50.720","B_3.40.50.1820","C_2.60.40.10","ALL"]
    rows = []
    for set_name in sets:
        msa_path = MSA_DIR / f"{set_name}_aa.fa"
        if not msa_path.exists(): continue
        msa = _parse_msa(msa_path)
        pos_to_col = {k: _seq_pos_to_msa_col(v) for k,v in msa.items()}
        n_msa_cols = max(len(v) for v in msa.values())

        sub = anchors if set_name == "ALL" else anchors[anchors.set == set_name]

        # observed concordance per group (top-1 only here for null test)
        groups_to_test = []
        for pf, g in sub.groupby("pfam_id"):
            groups_to_test.append(("pfam", pf, list(g.itertuples(index=False))))
        for hsf, g in sub.groupby("hsf"):
            groups_to_test.append(("hsf", hsf, list(g.itertuples(index=False))))
        groups_to_test.append(("set", set_name, list(sub.itertuples(index=False))))

        for grp_kind, label, members in groups_to_test:
            obs_cols = []
            for r in members:
                c = _chain_anchor_cols(r, pos_to_col, top_k=1)
                if c: obs_cols.append(c[0])
            if not obs_cols: continue
            obs = _concord_metrics(obs_cols, n_msa_cols)
            obs_top1 = obs["top1_conc"]; obs_tol2 = obs["tol2_conc"]

            # null: shuffle each chain's anchor to a uniform random position; map to MSA col
            ge_top1 = 0; ge_tol2 = 0
            null_top1 = []
            for _ in range(n_trials):
                cols = []
                for r in members:
                    key = r.chain_key
                    if key not in pos_to_col: continue
                    n_res = int(r.n_res)
                    p = int(rng.integers(0, n_res))
                    if p in pos_to_col[key]:
                        cols.append(pos_to_col[key][p])
                if not cols: continue
                m = _concord_metrics(cols, n_msa_cols)
                null_top1.append(m["top1_conc"])
                if m["top1_conc"] >= obs_top1: ge_top1 += 1
                if m["tol2_conc"] >= obs_tol2: ge_tol2 += 1
            null_arr = np.array(null_top1)
            rows.append({
                "msa_set": set_name, "group": grp_kind, "label": label,
                "n": obs["n"],
                "obs_top1": obs_top1, "null_top1_mean": float(null_arr.mean()) if len(null_arr) else float('nan'),
                "null_top1_p95": float(np.quantile(null_arr, 0.95)) if len(null_arr) else float('nan'),
                "p_top1": (ge_top1 + 1)/(n_trials + 1),
                "obs_tol2": obs_tol2, "p_tol2": (ge_tol2 + 1)/(n_trials + 1),
            })

    df = pd.DataFrame(rows)
    suffix = "_audit" if audit_only else "_all"
    out = OUT_DIR / f"baseline_random{suffix}.csv"
    df.to_csv(out, index=False)
    print(f"[baseline] wrote {out}")
    # quick aggregate: median of obs_top1 vs null_top1_mean per (msa_set, group)
    for grp in ["pfam","hsf","set"]:
        sub = df[df.group == grp]
        if sub.empty: continue
        agg = sub.groupby("msa_set").agg(
            n=("label","count"),
            med_obs=("obs_top1","median"),
            med_null=("null_top1_mean","median"),
            med_null_p95=("null_top1_p95","median"),
            n_signif=("p_top1", lambda s: (s < 0.05).sum()),
        )
        print(f"\n{grp.upper()}{' (audit)' if audit_only else ''}: obs vs random null")
        print(agg.to_string())


# --------------------------------------------------------------------------
# Stage: pairwise TM + seq-id + anchor-col distances; regression
# --------------------------------------------------------------------------
def stage_tm(manifest: pd.DataFrame) -> None:
    """All-vs-all TM-score via foldseek easy-search."""
    out_tsv = OUT_DIR / "pairwise_tm.tsv"
    if out_tsv.exists() and out_tsv.stat().st_size > 0:
        print(f"[tm] {out_tsv} exists; skipping foldseek run")
        return
    tmp = OUT_DIR / "_fs_tmp"
    if tmp.exists(): shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    foldseek = ROOT / "foldseek/bin/foldseek"
    fmt = "query,target,alntmscore,qtmscore,ttmscore,fident,alnlen,qlen,tlen"
    cmd = [str(foldseek), "easy-search", str(CHAIN_DIR), str(CHAIN_DIR),
           str(out_tsv), str(tmp), "--format-output", fmt,
           "--alignment-type","2","--exhaustive-search","1","-e","100","--max-seqs","500"]
    print(f"[tm] foldseek easy-search all-vs-all on {CHAIN_DIR}...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[tm] FAILED: {r.stderr[-800:]}"); return
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"[tm] wrote {out_tsv}")


def _msa_pair_seqid(s1: str, s2: str) -> float:
    n_match = 0; n_aligned = 0
    for a, b in zip(s1, s2):
        if a == "-" or b == "-": continue
        n_aligned += 1
        if a == b: n_match += 1
    return n_match / n_aligned if n_aligned > 0 else float('nan')


def stage_pairs(manifest: pd.DataFrame, audit_only: bool = True) -> None:
    """Build pairwise table: TM, seq-id, anchor-col-distance, relationship category."""
    anchors = pd.read_csv(ANCHOR_FILE)
    if audit_only:
        anchors = anchors[(anchors.top1_mass >= 0.5) & (anchors.keys_50pct == 1)]
    anchors = anchors.set_index("chain_key")

    msa_path = MSA_DIR / "ALL_aa.fa"
    msa = _parse_msa(msa_path)
    pos_to_col = {k: _seq_pos_to_msa_col(v) for k,v in msa.items()}

    # Load TM
    tm_path = OUT_DIR / "pairwise_tm.tsv"
    cols = "query,target,alntmscore,qtmscore,ttmscore,fident,alnlen,qlen,tlen".split(",")
    tm = pd.read_csv(tm_path, sep="\t", names=cols, header=None)
    # canonicalize chain_key from filename (strip .pdb)
    tm["q"] = tm["query"].str.replace(".pdb","",regex=False)
    tm["t"] = tm["target"].str.replace(".pdb","",regex=False)
    # max(qtm, ttm) is the standard symmetric pairwise TM
    tm["tm"] = tm[["qtmscore","ttmscore"]].max(axis=1)
    tm_pair = {}
    for r in tm.itertuples(index=False):
        a, b = sorted([r.q, r.t])
        if a == b: continue
        if (a,b) not in tm_pair or r.tm > tm_pair[(a,b)]:
            tm_pair[(a,b)] = float(r.tm)

    rows = []
    chain_keys = [k for k in anchors.index if k in pos_to_col]
    for i in range(len(chain_keys)):
        ki = chain_keys[i]; ai = anchors.loc[ki]
        ci = pos_to_col[ki].get(int(ai.attn_anchor))
        if ci is None: continue
        for j in range(i+1, len(chain_keys)):
            kj = chain_keys[j]; aj = anchors.loc[kj]
            cj = pos_to_col[kj].get(int(aj.attn_anchor))
            if cj is None: continue
            a, b = sorted([ki, kj])
            tm_score = tm_pair.get((a,b), float('nan'))
            seqid = _msa_pair_seqid(msa[ki], msa[kj])
            # category
            if ai.pfam_id == aj.pfam_id:
                cat = "within_pfam"
            elif ai.hsf == aj.hsf:
                cat = "cross_pfam_same_hsf"
            elif ai.set == aj.set:
                cat = "cross_hsf_same_set"  # only relevant if a set has multi HSFs (none do here)
            elif ai.set in {"A_3.40.50.720","B_3.40.50.1820"} and aj.set in {"A_3.40.50.720","B_3.40.50.1820"}:
                cat = "cross_hsf_same_fold"  # A and B share fold 3.40.50
            else:
                cat = "cross_fold"
            rows.append({
                "i": ki, "j": kj, "tm": tm_score, "seqid": seqid,
                "anchor_col_dist": abs(ci - cj),
                "category": cat,
                "pfam_i": ai.pfam_id, "pfam_j": aj.pfam_id,
                "hsf_i": ai.hsf, "hsf_j": aj.hsf,
                "set_i": ai.set, "set_j": aj.set,
            })
    df = pd.DataFrame(rows)
    out = OUT_DIR / "pairs.csv"
    df.to_csv(out, index=False)
    print(f"[pairs] wrote {out} with {len(df)} pairs")
    # category summary
    print("\nPer-category summary (audit-pass chains only):")
    print(df.groupby("category").agg(
        n=("anchor_col_dist","count"),
        tm_med=("tm","median"),
        seqid_med=("seqid","median"),
        anchor_dist_med=("anchor_col_dist","median"),
        anchor_within_2=("anchor_col_dist", lambda s: (s<=2).mean()),
    ).to_string())


def stage_regression(manifest: pd.DataFrame) -> None:
    """Test whether category labels predict anchor concordance after partialing TM-score."""
    pairs_path = OUT_DIR / "pairs.csv"
    df = pd.read_csv(pairs_path)
    df = df.dropna(subset=["tm","anchor_col_dist"])
    # Binarize: same column (±2) vs different
    df["same_col"] = (df["anchor_col_dist"] <= 2).astype(int)

    # Bin TM and ask: within each TM bin, does category still differ?
    df["tm_bin"] = pd.cut(df["tm"], bins=[0,0.3,0.5,0.6,0.7,0.8,0.9,1.0], include_lowest=True)
    print("Same-column (±2) rate by TM bin × category:")
    tab = df.groupby(["tm_bin","category"], observed=True).agg(
        n=("same_col","count"),
        same_col_rate=("same_col","mean"),
    ).unstack("category")
    print(tab.to_string())

    # logistic regression: same_col ~ tm + category dummies; report category coefficients
    try:
        import statsmodels.api as sm
        cat_dummies = pd.get_dummies(df["category"], drop_first=True).astype(float)
        X = pd.concat([pd.Series(1.0, index=df.index, name="const"),
                       df["tm"].astype(float).rename("tm"),
                       cat_dummies], axis=1)
        y = df["same_col"].astype(float)
        # full model
        full = sm.Logit(y, X).fit(disp=0, method="newton", maxiter=200)
        # nested model (tm only)
        Xt = X[["const","tm"]]
        nested = sm.Logit(y, Xt).fit(disp=0, method="newton", maxiter=200)
        lr = 2*(full.llf - nested.llf)
        from scipy.stats import chi2
        df_diff = X.shape[1] - Xt.shape[1]
        p_lr = 1 - chi2.cdf(lr, df_diff)
        print(f"\nLikelihood-ratio test (category | tm): LR = {lr:.2f}, df = {df_diff}, p = {p_lr:.3g}")
        print("\nFull model coefficients (logit):")
        print(full.summary().tables[1])
        print(f"\nTM-only McFadden R²: {1 - nested.llf/sm.Logit(y, X[['const']]).fit(disp=0,maxiter=200).llf:.3f}")
        print(f"Full McFadden R²: {1 - full.llf/sm.Logit(y, X[['const']]).fit(disp=0,maxiter=200).llf:.3f}")
    except Exception as e:
        print(f"[regression] statsmodels unavailable or failed: {e}")


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=["download","extract","anchors","msa","concord","baseline",
                             "tm","pairs","regression","all"])
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--audit-only", action="store_true",
                    help="for concord: restrict to chains passing top1>=0.5 & keys_50pct==1")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = pd.read_csv(MANIFEST)
    print(f"manifest: {len(manifest)} chains, {manifest.set.nunique()} sets, "
          f"{manifest.pfam_id.nunique()} Pfams")

    stages = ["download","extract","anchors","msa","concord"] if args.stage == "all" else [args.stage]
    for s in stages:
        print(f"\n=== STAGE: {s} ===")
        if s == "download": stage_download(manifest)
        elif s == "extract": stage_extract(manifest)
        elif s == "anchors": stage_anchors(manifest, device=args.device)
        elif s == "msa": stage_msa(manifest)
        elif s == "concord":
            stage_concord(manifest, audit_only=False)
            stage_concord(manifest, audit_only=True)
        elif s == "baseline":
            stage_baseline(manifest, audit_only=True)
        elif s == "tm": stage_tm(manifest)
        elif s == "pairs": stage_pairs(manifest, audit_only=True)
        elif s == "regression": stage_regression(manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
