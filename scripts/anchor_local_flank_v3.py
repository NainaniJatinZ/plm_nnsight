#!/usr/bin/env python3
"""Anchor local flank v3: hypothesis-driven flank classification at scale.

Tests whether anchorhood can be predicted from a local sequence/SSE/structural
window around the residue, using one model per hypothesis family:

  H1: AA identity (position-specific one-hot)
  H2: SSE arrangement (position-specific one-hot + transitions)
  H3: Physicochemical profile (hydrophobicity, charge, volume, flexibility)
  H4: Local 3D structural context (per-position RSA, contacts, center contact)
  H5: Positional context (where the anchor sits in the protein)
  FULL: All combined
  GBT: Gradient boosted trees on FULL features

Usage:
    uv run python scripts/anchor_local_flank_v3.py --phase 1        # H1-H5 individual
    uv run python scripts/anchor_local_flank_v3.py --phase 2        # FULL + GBT
    uv run python scripts/anchor_local_flank_v3.py --phase all      # everything
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDB_DIR = DATA_DIR / "pdb"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
sys.path.insert(0, str(ROOT))

AUDIT_CSV = REPORT_DIR / "anchor_behavior_audit.csv"
V3_FEATURES_CSV = REPORT_DIR / "anchor_regression_v3_features.csv"

TOP_N = 500
RADIUS_PRIMARY = 30
RADIUS_SECONDARY = 15
CONTROLS_PER_ANCHOR = 5
MIN_EDGE_DISTANCE = 30  # anchor must be >= 30 residues from edges (so R=30 window fits)
N_PERMUTATIONS = 100
N_SPLITS = 10

AA_ORDER = list("ACDEFGHIKLMNPQRSTVWY")
SSE_ORDER = ["H", "E", "C"]

# Kyte-Doolittle hydrophobicity
KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}

# Charge at pH 7
CHARGE = {aa: 0 for aa in AA_ORDER}
for aa in "RKH":
    CHARGE[aa] = 1
for aa in "DE":
    CHARGE[aa] = -1

# Side-chain volume (Zamyatnin, in A^3)
VOLUME = {"A": 88.6, "R": 173.4, "N": 114.1, "D": 111.1, "C": 108.5, "Q": 143.8, "E": 138.4, "G": 60.1, "H": 153.2, "I": 166.7, "L": 166.7, "K": 168.6, "M": 162.9, "F": 189.9, "P": 112.7, "S": 89.0, "T": 116.1, "W": 227.8, "Y": 193.6, "V": 140.0}

# Backbone flexibility (normalized B-factor proxy, Smith et al. scale)
FLEXIBILITY = {"A": 0.36, "R": 0.53, "N": 0.46, "D": 0.51, "C": 0.35, "Q": 0.49, "E": 0.50, "G": 0.54, "H": 0.32, "I": 0.46, "L": 0.40, "K": 0.47, "M": 0.30, "F": 0.31, "P": 0.51, "S": 0.51, "T": 0.44, "W": 0.17, "Y": 0.42, "V": 0.39}

# Max ASA for RSA computation (Tien et al. 2013)
MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data():
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")
    return seqs, ss_dict


def select_proteins(seqs, ss_dict, n=TOP_N, require_pdb=False):
    """Select top N proteins by top3_mass from the audit."""
    rows = []
    with open(AUDIT_CSV) as f:
        for r in csv.DictReader(f):
            pid = r["protein"]
            if pid not in seqs or pid not in ss_dict:
                continue
            if len(seqs[pid]) != len(ss_dict[pid]):
                continue
            rho = float(r["rank_corr"])
            mass = float(r["top3_mass"])
            if rho < 0.95 or mass < 0.70:
                continue
            anchor_pos = int(r["top_key_idx"])
            n_res = len(seqs[pid])
            if anchor_pos < MIN_EDGE_DISTANCE or anchor_pos >= n_res - MIN_EDGE_DISTANCE:
                continue
            if require_pdb:
                pdb_path = PDB_DIR / f"{pid[:4]}.pdb"
                if not pdb_path.exists():
                    continue
            rows.append({"protein": pid, "top3_mass": mass, "anchor_pos": anchor_pos, "n_res": n_res, "proj_score": float(r.get("mean_max_attn", 0))})
    rows.sort(key=lambda x: x["top3_mass"], reverse=True)
    return rows[:n]


# ---------------------------------------------------------------------------
# PDB feature computation
# ---------------------------------------------------------------------------

def _parse_pdb_residues(pdb_path):
    from Bio.PDB import PDBParser
    from Bio.Data.IUPACData import protein_letters_3to1

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("prot", str(pdb_path))
    chain = list(structure[0])[0]

    results = []
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        resid = residue.get_id()[1]
        aa = three_to_one(residue.get_resname())
        if aa == "X":
            continue
        ca = residue["CA"].get_vector().get_array() if "CA" in residue else None
        cb = residue["CB"].get_vector().get_array() if "CB" in residue else ca
        if ca is None:
            continue
        results.append({"resid": resid, "aa": aa, "ca": ca, "cb": cb})
    return results, structure


def _align_pdb_to_seq(pdb_residues, full_seq):
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues]
    resids = [t[0] for t in pdb_tuples]
    n_seq = len(full_seq)
    min_resid, max_resid = min(resids), max(resids)

    best_offset, best_matches = 0, 0
    for offset in range(-max_resid, n_seq - min_resid + 1):
        matches = sum(1 for resid, aa in pdb_tuples if 0 <= resid + offset < n_seq and full_seq[resid + offset] == aa)
        if matches > best_matches:
            best_offset, best_matches = offset, matches

    mapping = {}
    for i, (resid, aa) in enumerate(pdb_tuples):
        seq_pos = resid + best_offset
        if 0 <= seq_pos < n_seq and full_seq[seq_pos] == aa:
            mapping[i] = seq_pos
    return mapping


def compute_pdb_features(protein, full_seq):
    """Compute per-residue PDB features: RSA, contacts_8A, long_range_fraction.

    Returns dict: seq_pos -> {rsa, contacts_8A, long_range_fraction, cb_coord} or None.
    """
    pdb_path = PDB_DIR / f"{protein[:4]}.pdb"
    if not pdb_path.exists():
        return None

    try:
        pdb_residues, structure = _parse_pdb_residues(pdb_path)
    except Exception:
        return None
    if not pdb_residues:
        return None

    mapping = _align_pdb_to_seq(pdb_residues, full_seq)
    if len(mapping) < len(pdb_residues) * 0.5:
        return None

    # RSA via ShrakeRupley
    from Bio.PDB import ShrakeRupley
    sr = ShrakeRupley()
    try:
        sr.compute(structure[0], level="R")
    except Exception:
        return None
    chain = list(structure[0])[0]
    sasa_by_resid = {}
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa

    # Distance matrix from CB coords
    from scipy.spatial.distance import cdist
    cb_coords = np.array([r["cb"] for r in pdb_residues])
    dists = cdist(cb_coords, cb_coords)
    n_pdb = len(pdb_residues)

    contacts_8A_arr = (dists < 8.0).sum(axis=1) - 1
    long_range_arr = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) > 12 and dists[i, j] < 8.0:
                long_range_arr[i] += 1
    long_range_frac = long_range_arr / np.maximum(contacts_8A_arr, 1).astype(float)

    # Build per-seq-position feature dict
    # Also store the pdb_idx -> seq_pos reverse mapping and cb_coords for contact queries
    seq_to_pdb = {v: k for k, v in mapping.items()}
    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_residues[pdb_idx]
        aa = full_seq[seq_pos]
        max_asa = MAX_ASA.get(aa, 200)
        sasa = sasa_by_resid.get(r["resid"], 0)
        rsa = min(sasa / max_asa, 1.0) if max_asa > 0 else 0.0

        features[seq_pos] = {
            "rsa": rsa,
            "contacts_8A": int(contacts_8A_arr[pdb_idx]),
            "long_range_fraction": float(long_range_frac[pdb_idx]),
            "pdb_idx": pdb_idx,
        }

    # Store distance matrix and mapping for contact-with-center queries
    features["_dists"] = dists
    features["_seq_to_pdb"] = seq_to_pdb

    return features


# ---------------------------------------------------------------------------
# Control matching
# ---------------------------------------------------------------------------

def load_projection_scores():
    """Load per-residue projection scores from v3 features CSV if available."""
    scores = {}
    if not V3_FEATURES_CSV.exists():
        return scores
    with open(V3_FEATURES_CSV) as f:
        for r in csv.DictReader(f):
            pid = r["protein"]
            pos = int(r["pos"])
            scores.setdefault(pid, {})[pos] = float(r["proj_full"])
    return scores


def match_controls_structural(proteins, seqs, ss_dict, pdb_features_cache):
    """Structurally matched controls: same SSE + RSA within 0.02/0.05 + contacts_8A within 2/4."""
    all_matches = []
    rng = np.random.RandomState(42)
    dropped = 0

    for pinfo in proteins:
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        sse = ss_dict[pid]
        n = len(seq)

        pdb_feats = pdb_features_cache.get(pid)
        if pdb_feats is None or anchor not in pdb_feats:
            dropped += 1
            continue

        anchor_sse = sse[anchor]
        anchor_rsa = pdb_feats[anchor]["rsa"]
        anchor_c8a = pdb_feats[anchor]["contacts_8A"]

        # Two-pass: strict then relaxed
        for rsa_tol, c8a_tol in [(0.02, 2), (0.05, 4)]:
            candidates = []
            for j in range(MIN_EDGE_DISTANCE, n - MIN_EDGE_DISTANCE):
                if abs(j - anchor) < 10:
                    continue
                if sse[j] != anchor_sse:
                    continue
                if j not in pdb_feats:
                    continue
                if abs(pdb_feats[j]["rsa"] - anchor_rsa) > rsa_tol:
                    continue
                if abs(pdb_feats[j]["contacts_8A"] - anchor_c8a) > c8a_tol:
                    continue
                candidates.append(j)
            if len(candidates) >= 3:
                break

        if len(candidates) < 3:
            dropped += 1
            continue

        if len(candidates) > CONTROLS_PER_ANCHOR:
            idx = rng.choice(len(candidates), CONTROLS_PER_ANCHOR, replace=False)
            candidates = [candidates[i] for i in idx]

        for cp in candidates:
            all_matches.append({"protein": pid, "anchor_pos": anchor, "control_pos": cp})

    print(f"  Structural matching: {len(proteins) - dropped} proteins with controls, {dropped} dropped, {len(all_matches)} total pairs")
    return all_matches


def match_controls_sse_only(proteins, seqs, ss_dict):
    """SSE-only matched controls for broad coverage."""
    all_matches = []
    rng = np.random.RandomState(42)

    for pinfo in proteins:
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        sse = ss_dict[pid]
        n = len(seq)
        anchor_sse = sse[anchor]

        candidates = []
        for j in range(MIN_EDGE_DISTANCE, n - MIN_EDGE_DISTANCE):
            if abs(j - anchor) < 10:
                continue
            if sse[j] != anchor_sse:
                continue
            candidates.append(j)

        if len(candidates) == 0:
            continue
        if len(candidates) > CONTROLS_PER_ANCHOR:
            idx = rng.choice(len(candidates), CONTROLS_PER_ANCHOR, replace=False)
            candidates = [candidates[i] for i in idx]

        for cp in candidates:
            all_matches.append({"protein": pid, "anchor_pos": anchor, "control_pos": cp})

    return all_matches


# ---------------------------------------------------------------------------
# Feature extraction per hypothesis
# ---------------------------------------------------------------------------

def extract_window(seq, center, radius):
    n = len(seq)
    lo, hi = center - radius, center + radius
    if lo < 0 or hi >= n:
        return None
    return seq[lo:hi + 1]


def features_h1(seq_window):
    """H1: per-position AA one-hot. 20 AAs x (2R+1) positions."""
    wlen = len(seq_window)
    center = wlen // 2
    feats = {}
    aa_set = set(AA_ORDER)
    for j in range(wlen):
        pos = j - center
        aa = seq_window[j]
        for a in AA_ORDER:
            feats[f"aa_{pos}_{a}"] = 1.0 if (aa == a and aa in aa_set) else 0.0
    return feats


def features_h2(sse_window):
    """H2: per-position SSE one-hot + transition indicators."""
    wlen = len(sse_window)
    center = wlen // 2
    feats = {}
    for j in range(wlen):
        pos = j - center
        s = sse_window[j]
        for ss in SSE_ORDER:
            feats[f"sse_{pos}_{ss}"] = 1.0 if s == ss else 0.0
    # Transition indicators
    for j in range(1, wlen):
        pos = j - center
        feats[f"sse_trans_{pos}"] = 1.0 if sse_window[j] != sse_window[j - 1] else 0.0
    return feats


def features_h3(seq_window):
    """H3: per-position physicochemical properties (hydrophobicity, charge, volume, flexibility)."""
    wlen = len(seq_window)
    center = wlen // 2
    feats = {}
    for j in range(wlen):
        pos = j - center
        aa = seq_window[j]
        feats[f"hydro_{pos}"] = KD.get(aa, 0.0)
        feats[f"charge_{pos}"] = CHARGE.get(aa, 0)
        feats[f"volume_{pos}"] = VOLUME.get(aa, 120.0)
        feats[f"flex_{pos}"] = FLEXIBILITY.get(aa, 0.4)
    return feats


def features_h4(center_pos, radius, pdb_feats):
    """H4: per-position structural features from PDB (RSA, contacts_8A, contact-with-center, long-range fraction)."""
    wlen = 2 * radius + 1
    center_idx = radius
    feats = {}
    dists = pdb_feats.get("_dists")
    seq_to_pdb = pdb_feats.get("_seq_to_pdb", {})
    center_pdb_idx = seq_to_pdb.get(center_pos)

    for j in range(wlen):
        seq_pos = center_pos - radius + j
        pos = j - center_idx
        if seq_pos in pdb_feats and isinstance(pdb_feats[seq_pos], dict):
            pf = pdb_feats[seq_pos]
            feats[f"rsa_{pos}"] = pf["rsa"]
            feats[f"c8a_{pos}"] = pf["contacts_8A"]
            feats[f"lrf_{pos}"] = pf["long_range_fraction"]
            # Contact with center?
            j_pdb_idx = seq_to_pdb.get(seq_pos)
            if center_pdb_idx is not None and j_pdb_idx is not None and dists is not None:
                feats[f"cnt_center_{pos}"] = 1.0 if dists[j_pdb_idx, center_pdb_idx] < 8.0 else 0.0
            else:
                feats[f"cnt_center_{pos}"] = 0.0
        else:
            feats[f"rsa_{pos}"] = 0.0
            feats[f"c8a_{pos}"] = 0.0
            feats[f"lrf_{pos}"] = 0.0
            feats[f"cnt_center_{pos}"] = 0.0
    return feats


def features_h5(anchor_pos, n_res, sse_str, radius):
    """H5: positional context features."""
    feats = {}
    feats["frac_pos"] = anchor_pos / n_res
    feats["dist_nterm"] = anchor_pos
    feats["dist_cterm"] = n_res - 1 - anchor_pos

    # SSE segment info within the window
    lo = max(0, anchor_pos - radius)
    hi = min(n_res, anchor_pos + radius + 1)
    window_sse = sse_str[lo:hi]
    n_transitions = sum(1 for i in range(1, len(window_sse)) if window_sse[i] != window_sse[i - 1])
    n_segments = n_transitions + 1
    feats["n_sse_segments"] = n_segments
    feats["n_sse_transitions"] = n_transitions

    # Length of SSE the anchor sits in
    anchor_sse = sse_str[anchor_pos]
    seg_len = 1
    for i in range(anchor_pos - 1, -1, -1):
        if sse_str[i] == anchor_sse:
            seg_len += 1
        else:
            break
    seg_start = anchor_pos - (seg_len - 1)
    for i in range(anchor_pos + 1, n_res):
        if sse_str[i] == anchor_sse:
            seg_len += 1
        else:
            break
    feats["sse_seg_len"] = seg_len
    feats["pos_in_sse"] = (anchor_pos - seg_start) / max(seg_len - 1, 1)

    return feats


# ---------------------------------------------------------------------------
# Dataset building
# ---------------------------------------------------------------------------

def build_dataset(proteins, matches, seqs, ss_dict, radius, hypothesis, pdb_features_cache=None):
    """Build X, y, protein_ids for a given hypothesis and radius."""
    matches_by_protein = defaultdict(list)
    for m in matches:
        matches_by_protein[m["protein"]].append(m)

    feature_dicts = []
    labels = []
    pids = []
    protein_set = set(p["protein"] for p in proteins)
    protein_nres = {p["protein"]: p["n_res"] for p in proteins}

    for pid in sorted(protein_set):
        if pid not in matches_by_protein:
            continue
        seq = seqs[pid]
        sse = ss_dict[pid]
        n_res = len(seq)
        pdb_feats = pdb_features_cache.get(pid) if pdb_features_cache else None

        protein_matches = matches_by_protein[pid]
        anchor_pos = protein_matches[0]["anchor_pos"]

        # All positions to featurize: anchor + controls
        positions = [(anchor_pos, 1)]
        for m in protein_matches:
            positions.append((m["control_pos"], 0))

        for pos, label in positions:
            seq_win = extract_window(seq, pos, radius)
            sse_win = extract_window(sse, pos, radius)
            if seq_win is None or sse_win is None:
                continue

            if hypothesis == "H1":
                feats = features_h1(seq_win)
            elif hypothesis == "H2":
                feats = features_h2(sse_win)
            elif hypothesis == "H3":
                feats = features_h3(seq_win)
            elif hypothesis == "H4":
                if pdb_feats is None:
                    continue
                feats = features_h4(pos, radius, pdb_feats)
            elif hypothesis == "H5":
                feats = features_h5(pos, n_res, sse, radius)
            elif hypothesis == "FULL":
                f1 = features_h1(seq_win)
                f2 = features_h2(sse_win)
                f3 = features_h3(seq_win)
                f5 = features_h5(pos, n_res, sse, radius)
                feats = {**f1, **f2, **f3, **f5}
                if pdb_feats is not None:
                    f4 = features_h4(pos, radius, pdb_feats)
                    feats.update(f4)
            else:
                raise ValueError(f"Unknown hypothesis: {hypothesis}")

            feature_dicts.append(feats)
            labels.append(label)
            pids.append(pid)

    if not feature_dicts:
        return None, None, None, None

    all_keys = sorted(feature_dicts[0].keys())
    X = np.array([[fd.get(k, 0.0) for k in all_keys] for fd in feature_dicts])
    y = np.array(labels)
    return X, y, pids, all_keys


# ---------------------------------------------------------------------------
# LOPO evaluation
# ---------------------------------------------------------------------------

def run_lopo_l1(X, y, protein_ids, feature_names, n_splits=N_SPLITS):
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score
    from sklearn.model_selection import GroupKFold

    proteins = sorted(set(protein_ids))
    if len(proteins) < 3:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "n_folds": 0, "coefs": None, "feature_names": feature_names, "n_pos": 0, "n_neg": 0, "base_rate": np.nan}

    le = LabelEncoder()
    groups = le.fit_transform(protein_ids)
    actual_splits = min(n_splits, len(proteins))
    gkf = GroupKFold(n_splits=actual_splits)

    all_probs = np.full(len(y), np.nan)
    coef_accum = []

    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]
        if y_test.sum() == 0 or y_test.sum() == len(y_test):
            continue
        if y_train.sum() == 0 or (y_train == 0).sum() == 0:
            continue

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        clf = LogisticRegression(penalty="l1", solver="liblinear", max_iter=2000, class_weight="balanced", random_state=42, C=1.0)
        clf.fit(X_train_s, y_train)
        probs = clf.predict_proba(X_test_s)[:, 1]
        all_probs[test_idx] = probs
        coef_accum.append(clf.coef_[0] / scaler.scale_)

    valid = ~np.isnan(all_probs)
    if valid.sum() == 0 or y[valid].sum() == 0:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "n_folds": 0, "coefs": None, "feature_names": feature_names, "n_pos": 0, "n_neg": 0, "base_rate": np.nan}

    probs_valid, labels_valid = all_probs[valid], y[valid]
    n_pos, n_neg = int(labels_valid.sum()), int((1 - labels_valid).sum())

    try:
        auroc = roc_auc_score(labels_valid, probs_valid)
    except ValueError:
        auroc = np.nan
    try:
        auprc = average_precision_score(labels_valid, probs_valid)
    except ValueError:
        auprc = np.nan
    bal_acc = balanced_accuracy_score(labels_valid, (probs_valid >= 0.5).astype(int))
    mean_coefs = np.mean(coef_accum, axis=0) if coef_accum else None

    return {"auroc": float(auroc), "auprc": float(auprc), "bal_acc": float(bal_acc), "n_folds": len(coef_accum), "coefs": mean_coefs, "feature_names": feature_names, "n_pos": n_pos, "n_neg": n_neg, "base_rate": n_pos / (n_pos + n_neg) if (n_pos + n_neg) > 0 else np.nan}


def run_lopo_gbt(X, y, protein_ids, n_splits=N_SPLITS):
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score
    from sklearn.model_selection import GroupKFold

    proteins = sorted(set(protein_ids))
    if len(proteins) < 3:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan}

    le = LabelEncoder()
    groups = le.fit_transform(protein_ids)
    actual_splits = min(n_splits, len(proteins))
    gkf = GroupKFold(n_splits=actual_splits)

    all_probs = np.full(len(y), np.nan)

    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]
        if y_test.sum() == 0 or y_test.sum() == len(y_test):
            continue
        if y_train.sum() == 0 or (y_train == 0).sum() == 0:
            continue

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        n_pos = y_train.sum()
        n_neg = len(y_train) - n_pos
        w_pos = len(y_train) / (2 * n_pos) if n_pos > 0 else 1.0
        w_neg = len(y_train) / (2 * n_neg) if n_neg > 0 else 1.0
        sample_weights = np.where(y_train == 1, w_pos, w_neg)

        clf = GradientBoostingClassifier(n_estimators=200, max_depth=3, learning_rate=0.1, random_state=42)
        clf.fit(X_train_s, y_train, sample_weight=sample_weights)
        probs = clf.predict_proba(X_test_s)[:, 1]
        all_probs[test_idx] = probs

    valid = ~np.isnan(all_probs)
    if valid.sum() == 0 or y[valid].sum() == 0:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan}

    probs_valid, labels_valid = all_probs[valid], y[valid]
    try:
        auroc = roc_auc_score(labels_valid, probs_valid)
    except ValueError:
        auroc = np.nan
    try:
        auprc = average_precision_score(labels_valid, probs_valid)
    except ValueError:
        auprc = np.nan
    bal_acc = balanced_accuracy_score(labels_valid, (probs_valid >= 0.5).astype(int))
    return {"auroc": float(auroc), "auprc": float(auprc), "bal_acc": float(bal_acc)}


def run_permutation_test(X, y, protein_ids, feature_names, n_perms=N_PERMUTATIONS, n_splits=N_SPLITS):
    """Shuffle labels, re-run LOPO, return null AUPRC distribution."""
    rng = np.random.RandomState(42)
    null_auprcs = []
    for i in range(n_perms):
        y_perm = rng.permutation(y)
        result = run_lopo_l1(X, y_perm, protein_ids, feature_names, n_splits=n_splits)
        null_auprcs.append(result["auprc"] if not np.isnan(result["auprc"]) else 0.0)
        if (i + 1) % 25 == 0:
            print(f"    Permutation {i+1}/{n_perms}")
    return null_auprcs


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_hypothesis_comparison(results, output_path):
    """Bar chart: AUPRC per model."""
    hypotheses = [k for k in results if k not in ("GBT_FULL",)]
    auprcs = [results[h]["auprc"] for h in hypotheses]
    base_rates = [results[h].get("base_rate", np.nan) for h in hypotheses]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(hypotheses))
    colors = ["#4575b4", "#91bfdb", "#fee090", "#fc8d59", "#d73027", "#542788"]
    bars = ax.bar(x, auprcs, color=colors[:len(hypotheses)], alpha=0.85, edgecolor="black", linewidth=0.5)

    # Base rate line
    br = np.nanmean([b for b in base_rates if not np.isnan(b)])
    if not np.isnan(br):
        ax.axhline(y=br, color="gray", linestyle="--", alpha=0.7, label=f"Base rate ({br:.3f})")

    for i, (h, v) in enumerate(zip(hypotheses, auprcs)):
        if not np.isnan(v):
            ax.text(i, v + 0.005, f"{v:.3f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(hypotheses, fontsize=9)
    ax.set_ylabel("AUPRC")
    ax.set_title("Hypothesis Comparison: AUPRC by Model (R=30, LOPO)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_top_features(coefs, feature_names, title, output_path, top_n=20):
    if coefs is None:
        return
    abs_coefs = np.abs(coefs)
    top_idx = np.argsort(abs_coefs)[-top_n:][::-1]
    fig, ax = plt.subplots(figsize=(8, max(5, top_n * 0.25)))
    y_pos = np.arange(len(top_idx))
    colors = ["#d73027" if coefs[i] > 0 else "#4575b4" for i in top_idx]
    ax.barh(y_pos, coefs[top_idx], color=colors, alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([feature_names[i] for i in top_idx], fontsize=7)
    ax.set_xlabel("L1 coefficient (scaled)")
    ax.set_title(title)
    ax.invert_yaxis()
    ax.axvline(x=0, color="black", linewidth=0.5)
    ax.grid(True, alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


def plot_null_distribution(observed_auprc, null_auprcs, title, output_path):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(null_auprcs, bins=30, color="#91bfdb", edgecolor="black", linewidth=0.5, alpha=0.8, label="Null (permuted)")
    ax.axvline(x=observed_auprc, color="#d73027", linewidth=2, label=f"Observed ({observed_auprc:.3f})")
    p95 = np.percentile(null_auprcs, 95)
    ax.axvline(x=p95, color="orange", linewidth=1, linestyle="--", label=f"95th pctl ({p95:.3f})")
    p_val = np.mean([n >= observed_auprc for n in null_auprcs])
    ax.set_title(f"{title} (p={p_val:.3f})")
    ax.set_xlabel("AUPRC")
    ax.set_ylabel("Count")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="all", choices=["1", "2", "all"], help="Phase 1: H1-H5 individual. Phase 2: FULL + GBT. all: everything.")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    os.makedirs(REPORT_DIR, exist_ok=True)
    t0 = time.time()

    print("Loading data...")
    seqs, ss_dict = load_data()

    # Select proteins: all 500 for non-PDB hypotheses
    proteins_all = select_proteins(seqs, ss_dict, n=TOP_N, require_pdb=False)
    proteins_pdb = select_proteins(seqs, ss_dict, n=TOP_N, require_pdb=True)
    print(f"Selected {len(proteins_all)} proteins (all), {len(proteins_pdb)} proteins (with PDB)")

    # Compute PDB features for proteins that have PDB files
    print("Computing PDB features...")
    pdb_features_cache = {}
    pdb_computed = 0
    for pinfo in proteins_pdb:
        pid = pinfo["protein"]
        if pid in pdb_features_cache:
            continue
        feats = compute_pdb_features(pid, seqs[pid])
        if feats is not None:
            pdb_features_cache[pid] = feats
            pdb_computed += 1
            if pdb_computed % 20 == 0:
                print(f"  Computed PDB features for {pdb_computed} proteins...")
    print(f"  PDB features computed for {pdb_computed} proteins")

    # Build controls
    print("Building matched controls...")
    matches_sse = match_controls_sse_only(proteins_all, seqs, ss_dict)
    print(f"  SSE-only: {len(matches_sse)} control pairs from {len(set(m['protein'] for m in matches_sse))} proteins")

    # For structural matching, use only proteins with PDB features
    proteins_with_pdb = [p for p in proteins_pdb if p["protein"] in pdb_features_cache]
    matches_structural = match_controls_structural(proteins_with_pdb, seqs, ss_dict, pdb_features_cache)

    all_results = {}
    all_datasets = {}

    # ------------------------------------------------------------------
    # Phase 1: individual hypothesis models
    # ------------------------------------------------------------------
    if args.phase in ("1", "all"):
        print("\n" + "=" * 60)
        print("PHASE 1: Individual hypothesis models (R=30)")
        print("=" * 60)

        for hyp in ["H1", "H2", "H3", "H4", "H5"]:
            print(f"\n--- Model {hyp} ---")
            t1 = time.time()

            if hyp == "H4":
                proteins_use = proteins_with_pdb
                matches_use = matches_structural
                pdb_cache = pdb_features_cache
            else:
                proteins_use = proteins_all
                matches_use = matches_sse
                pdb_cache = None

            X, y, pids, feat_names = build_dataset(proteins_use, matches_use, seqs, ss_dict, RADIUS_PRIMARY, hyp, pdb_cache)
            if X is None:
                print(f"  No data for {hyp}, skipping")
                all_results[hyp] = {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "base_rate": np.nan, "n_proteins": 0, "n_features": 0}
                continue

            n_proteins = len(set(pids))
            print(f"  Dataset: {X.shape[0]} samples, {X.shape[1]} features, {n_proteins} proteins, {int(y.sum())} anchors, {int((1-y).sum())} controls")

            result = run_lopo_l1(X, y, pids, feat_names)
            result["n_proteins"] = n_proteins
            result["n_features"] = X.shape[1]
            all_results[hyp] = result
            all_datasets[hyp] = (X, y, pids, feat_names)

            print(f"  AUPRC={result['auprc']:.4f}  AUROC={result['auroc']:.4f}  BalAcc={result['bal_acc']:.4f}  BaseRate={result['base_rate']:.4f}  ({time.time()-t1:.1f}s)")

            # Save coefficients
            if result["coefs"] is not None:
                coef_path = REPORT_DIR / f"anchor_local_flank_v3_coefficients_{hyp}.csv"
                with open(coef_path, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["feature", "coefficient", "abs_coefficient"])
                    for fname, coef in sorted(zip(feat_names, result["coefs"]), key=lambda x: -abs(x[1])):
                        w.writerow([fname, f"{coef:.6f}", f"{abs(coef):.6f}"])
                print(f"  Saved coefficients: {coef_path}")

        # R=15 check for models that showed signal at R=30
        print("\n--- R=15 comparison ---")
        for hyp in ["H1", "H2", "H3", "H5"]:
            if hyp not in all_results or np.isnan(all_results[hyp].get("auprc", np.nan)):
                continue
            base = all_results[hyp].get("base_rate", 0)
            if all_results[hyp]["auprc"] <= base * 1.1:
                continue

            X15, y15, pids15, fn15 = build_dataset(proteins_all, matches_sse, seqs, ss_dict, RADIUS_SECONDARY, hyp, None)
            if X15 is None:
                continue
            r15 = run_lopo_l1(X15, y15, pids15, fn15)
            key = f"{hyp}_R15"
            all_results[key] = r15
            print(f"  {hyp} R=15: AUPRC={r15['auprc']:.4f}  AUROC={r15['auroc']:.4f}")

        # Permutation test for the best-performing model
        best_hyp = None
        best_auprc = 0
        for h in ["H1", "H2", "H3", "H4", "H5"]:
            if h in all_results and not np.isnan(all_results[h].get("auprc", np.nan)):
                if all_results[h]["auprc"] > best_auprc:
                    best_auprc = all_results[h]["auprc"]
                    best_hyp = h

        if best_hyp and best_hyp in all_datasets:
            print(f"\n--- Permutation test for {best_hyp} (AUPRC={best_auprc:.4f}) ---")
            X_b, y_b, pids_b, fn_b = all_datasets[best_hyp]
            null_auprcs = run_permutation_test(X_b, y_b, pids_b, fn_b)
            p_val = np.mean([n >= best_auprc for n in null_auprcs])
            print(f"  p-value: {p_val:.4f} (95th pctl of null: {np.percentile(null_auprcs, 95):.4f})")
            all_results[f"{best_hyp}_perm"] = {"null_auprcs": null_auprcs, "p_value": p_val}

            plot_null_distribution(best_auprc, null_auprcs, f"Permutation Test: {best_hyp}", REPORT_DIR / "anchor_local_flank_v3_null_distribution.png")

        # Phase 1 plots
        phase1_results = {h: all_results[h] for h in ["H1", "H2", "H3", "H4", "H5"] if h in all_results}
        plot_hypothesis_comparison(phase1_results, REPORT_DIR / "anchor_local_flank_v3_hypothesis_comparison.png")

        # Top features for each model that has coefficients
        for hyp in ["H1", "H2", "H3", "H4", "H5"]:
            if hyp in all_results and all_results[hyp].get("coefs") is not None:
                plot_top_features(all_results[hyp]["coefs"], all_results[hyp]["feature_names"], f"Top Features: {hyp} (R=30)", REPORT_DIR / f"anchor_local_flank_v3_top_features_{hyp}.png")

        # Save Phase 1 metrics
        metrics_path = REPORT_DIR / "anchor_local_flank_v3_metrics.csv"
        with open(metrics_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["model", "radius", "matching", "n_proteins", "n_features", "n_pos", "n_neg", "base_rate", "auprc", "auroc", "bal_acc"])
            for hyp in ["H1", "H2", "H3", "H4", "H5"]:
                if hyp in all_results:
                    r = all_results[hyp]
                    matching = "structural" if hyp == "H4" else "sse_only"
                    w.writerow([hyp, RADIUS_PRIMARY, matching, r.get("n_proteins", ""), r.get("n_features", ""), r.get("n_pos", ""), r.get("n_neg", ""), f"{r.get('base_rate', np.nan):.4f}", f"{r.get('auprc', np.nan):.4f}", f"{r.get('auroc', np.nan):.4f}", f"{r.get('bal_acc', np.nan):.4f}"])
            for hyp in ["H1", "H2", "H3", "H5"]:
                key = f"{hyp}_R15"
                if key in all_results:
                    r = all_results[key]
                    w.writerow([hyp, RADIUS_SECONDARY, "sse_only", "", "", r.get("n_pos", ""), r.get("n_neg", ""), f"{r.get('base_rate', np.nan):.4f}", f"{r.get('auprc', np.nan):.4f}", f"{r.get('auroc', np.nan):.4f}", f"{r.get('bal_acc', np.nan):.4f}"])
        print(f"\nPhase 1 metrics saved: {metrics_path}")
        print(f"Phase 1 complete ({time.time()-t0:.1f}s)")

    # ------------------------------------------------------------------
    # Phase 2: FULL model + GBT
    # ------------------------------------------------------------------
    if args.phase in ("2", "all"):
        print("\n" + "=" * 60)
        print("PHASE 2: FULL model + GBT (R=30)")
        print("=" * 60)

        # FULL with SSE-only matching (no H4 features for non-PDB proteins)
        print("\n--- Model FULL (SSE-only matching) ---")
        t2 = time.time()
        X_full, y_full, pids_full, fn_full = build_dataset(proteins_all, matches_sse, seqs, ss_dict, RADIUS_PRIMARY, "FULL", pdb_features_cache)
        if X_full is not None:
            n_prot = len(set(pids_full))
            print(f"  Dataset: {X_full.shape[0]} samples, {X_full.shape[1]} features, {n_prot} proteins")
            result_full = run_lopo_l1(X_full, y_full, pids_full, fn_full)
            result_full["n_proteins"] = n_prot
            result_full["n_features"] = X_full.shape[1]
            all_results["FULL"] = result_full
            print(f"  L1: AUPRC={result_full['auprc']:.4f}  AUROC={result_full['auroc']:.4f}  BalAcc={result_full['bal_acc']:.4f}  ({time.time()-t2:.1f}s)")

            if result_full["coefs"] is not None:
                coef_path = REPORT_DIR / "anchor_local_flank_v3_coefficients_FULL.csv"
                with open(coef_path, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["feature", "coefficient", "abs_coefficient"])
                    for fname, coef in sorted(zip(fn_full, result_full["coefs"]), key=lambda x: -abs(x[1])):
                        w.writerow([fname, f"{coef:.6f}", f"{abs(coef):.6f}"])

                plot_top_features(result_full["coefs"], fn_full, "Top Features: FULL (R=30)", REPORT_DIR / "anchor_local_flank_v3_top_features_FULL.png")

            # GBT on FULL
            print("\n--- GBT on FULL features ---")
            t3 = time.time()
            result_gbt = run_lopo_gbt(X_full, y_full, pids_full)
            all_results["GBT_FULL"] = result_gbt
            print(f"  GBT: AUPRC={result_gbt['auprc']:.4f}  AUROC={result_gbt['auroc']:.4f}  BalAcc={result_gbt['bal_acc']:.4f}  ({time.time()-t3:.1f}s)")
        else:
            print("  No data for FULL model")

        # Analysis 4: SSE-only vs structural controls comparison
        # Re-run H1 with structural matching for artifact check
        if matches_structural:
            print("\n--- Analysis 4: SSE-only vs structural control comparison ---")
            X_h1_str, y_h1_str, pids_h1_str, fn_h1_str = build_dataset(proteins_with_pdb, matches_structural, seqs, ss_dict, RADIUS_PRIMARY, "H1", None)
            if X_h1_str is not None:
                r_h1_str = run_lopo_l1(X_h1_str, y_h1_str, pids_h1_str, fn_h1_str)
                all_results["H1_structural"] = r_h1_str
                print(f"  H1 (structural matching): AUPRC={r_h1_str['auprc']:.4f}  AUROC={r_h1_str['auroc']:.4f}")

                # Also H1 with SSE-only on same protein subset for fair comparison
                matches_sse_subset = [m for m in matches_sse if m["protein"] in set(p["protein"] for p in proteins_with_pdb)]
                X_h1_sse_sub, y_h1_sse_sub, pids_h1_sse_sub, fn_h1_sse_sub = build_dataset(proteins_with_pdb, matches_sse_subset, seqs, ss_dict, RADIUS_PRIMARY, "H1", None)
                if X_h1_sse_sub is not None:
                    r_h1_sse_sub = run_lopo_l1(X_h1_sse_sub, y_h1_sse_sub, pids_h1_sse_sub, fn_h1_sse_sub)
                    all_results["H1_sse_subset"] = r_h1_sse_sub
                    print(f"  H1 (SSE-only, same proteins): AUPRC={r_h1_sse_sub['auprc']:.4f}  AUROC={r_h1_sse_sub['auroc']:.4f}")

                    # Plot comparison
                    fig, ax = plt.subplots(figsize=(6, 4))
                    labels_bar = ["SSE-only\n(same proteins)", "Structural\nmatching"]
                    vals = [r_h1_sse_sub["auprc"], r_h1_str["auprc"]]
                    ax.bar(labels_bar, vals, color=["#4575b4", "#d73027"], alpha=0.85, edgecolor="black", linewidth=0.5)
                    for i, v in enumerate(vals):
                        if not np.isnan(v):
                            ax.text(i, v + 0.005, f"{v:.3f}", ha="center", fontsize=9)
                    ax.set_ylabel("AUPRC")
                    ax.set_title("H1 Model: SSE-only vs Structural Controls (artifact check)")
                    ax.grid(True, alpha=0.3, axis="y")
                    fig.tight_layout()
                    fig.savefig(REPORT_DIR / "anchor_local_flank_v3_sse_vs_structural_controls.png", dpi=150, bbox_inches="tight")
                    plt.close(fig)
                    print(f"  Saved: anchor_local_flank_v3_sse_vs_structural_controls.png")

        # Update metrics CSV with Phase 2 results
        metrics_path = REPORT_DIR / "anchor_local_flank_v3_metrics.csv"
        # Append if Phase 1 already wrote, else create
        mode = "a" if args.phase == "2" else "a" if os.path.exists(metrics_path) else "w"
        with open(metrics_path, mode, newline="") as f:
            w = csv.writer(f)
            if mode == "w":
                w.writerow(["model", "radius", "matching", "n_proteins", "n_features", "n_pos", "n_neg", "base_rate", "auprc", "auroc", "bal_acc"])
            for key in ["FULL", "GBT_FULL", "H1_structural", "H1_sse_subset"]:
                if key in all_results:
                    r = all_results[key]
                    w.writerow([key, RADIUS_PRIMARY, "sse_only" if "sse" in key.lower() or key in ("FULL", "GBT_FULL") else "structural", r.get("n_proteins", ""), r.get("n_features", ""), r.get("n_pos", ""), r.get("n_neg", ""), f"{r.get('base_rate', np.nan):.4f}", f"{r.get('auprc', np.nan):.4f}", f"{r.get('auroc', np.nan):.4f}", f"{r.get('bal_acc', np.nan):.4f}"])

        # Final combined hypothesis comparison plot (if we have phase 1 results too)
        all_hyps = {h: all_results[h] for h in ["H1", "H2", "H3", "H4", "H5", "FULL"] if h in all_results}
        if len(all_hyps) > 1:
            plot_hypothesis_comparison(all_hyps, REPORT_DIR / "anchor_local_flank_v3_hypothesis_comparison.png")

        print(f"\nPhase 2 complete ({time.time()-t0:.1f}s)")

    # ------------------------------------------------------------------
    # Summary report
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    report_lines = []
    report_lines.append("# Anchor Local Flank Classification v3\n")
    report_lines.append(f"Run date: {time.strftime('%Y-%m-%d %H:%M')}\n")
    report_lines.append(f"Proteins (all): {len(proteins_all)}, Proteins (with PDB): {len(proteins_pdb)}, PDB features computed: {pdb_computed}\n")
    report_lines.append(f"Primary radius: {RADIUS_PRIMARY}, Secondary radius: {RADIUS_SECONDARY}\n")
    report_lines.append(f"Controls per anchor: {CONTROLS_PER_ANCHOR}\n")
    report_lines.append(f"SSE-only control pairs: {len(matches_sse)}, Structural control pairs: {len(matches_structural)}\n")

    report_lines.append("\n## Results\n")
    report_lines.append(f"{'Model':<20} {'Matching':<15} {'N_prot':<8} {'N_feat':<8} {'Base':<8} {'AUPRC':<8} {'AUROC':<8} {'BalAcc':<8}")
    report_lines.append("-" * 93)

    for key in ["H1", "H2", "H3", "H4", "H5", "FULL", "GBT_FULL", "H1_R15", "H2_R15", "H3_R15", "H5_R15", "H1_structural", "H1_sse_subset"]:
        if key not in all_results:
            continue
        r = all_results[key]
        matching = "structural" if "structural" in key or key == "H4" else "sse_only"
        n_prot = r.get("n_proteins", "")
        n_feat = r.get("n_features", "")
        br = r.get("base_rate", np.nan)
        report_lines.append(f"{key:<20} {matching:<15} {str(n_prot):<8} {str(n_feat):<8} {br:<8.4f} {r.get('auprc', np.nan):<8.4f} {r.get('auroc', np.nan):<8.4f} {r.get('bal_acc', np.nan):<8.4f}")

    if f"{best_hyp}_perm" in all_results if 'best_hyp' in dir() else False:
        perm = all_results[f"{best_hyp}_perm"]
        report_lines.append(f"\nPermutation test ({best_hyp}): p={perm['p_value']:.4f}, null 95th pctl={np.percentile(perm['null_auprcs'], 95):.4f}")

    report_lines.append("\n## Interpretation\n")

    # Auto-interpret results
    for hyp in ["H1", "H2", "H3", "H4", "H5"]:
        if hyp not in all_results:
            continue
        r = all_results[hyp]
        br = r.get("base_rate", 0)
        auprc = r.get("auprc", 0)
        if np.isnan(auprc) or np.isnan(br):
            report_lines.append(f"{hyp}: insufficient data")
        elif auprc > br * 1.5:
            report_lines.append(f"{hyp}: SIGNAL DETECTED (AUPRC {auprc:.4f} > 1.5x base rate {br:.4f})")
        elif auprc > br * 1.2:
            report_lines.append(f"{hyp}: weak signal (AUPRC {auprc:.4f} ~ 1.2x base rate {br:.4f})")
        else:
            report_lines.append(f"{hyp}: no signal (AUPRC {auprc:.4f} ~ base rate {br:.4f})")

    report_text = "\n".join(report_lines)
    print(report_text)

    report_path = REPORT_DIR / "anchor_local_flank_v3.md"
    with open(report_path, "w") as f:
        f.write(report_text + "\n")
    print(f"\nReport saved: {report_path}")
    print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
