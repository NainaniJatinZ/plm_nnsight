#!/usr/bin/env python3
"""Expanded anchor feature regression (Experiment 3_25_anchor_regression_v2.md).

Extends v1 with structural features from PDB coordinates:
  - Relative Solvent Accessibility (RSA) via ShrakeRupley
  - Local hydrophobic context (sequence window features)
  - 3D contact number from CB/CA distances
  - Random forest / gradient boosting for nonlinear interactions

Usage:
    uv run python scripts/anchor_regression_v2.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from statistics import mean

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

from helpers.utils import load_sae_prot

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
SEGMENT_RADIUS = 5
REFERENCE_PROTEIN = "2B61A"

ANCHOR_POSITIONS = {
    "1BRTA": 220,
    "1PVGA": 101,
    "2B61A": 315,
    "2DPMA": 39,
    "2PKEA": 131,
    "2QY6A": 64,
    "2YHWA": 287,
    "3CSSA": 40,
    "3HO7A": 63,
    "3OKPA": 200,
    "3QDLA": 114,
    "3WJPA": 94,
    "4EHUA": 100,
    "4EX6A": 124,
    "4EZIA": 310,
    "4ME3A": 75,
    "4N9WA": 194,
    "4OY3A": 193,
}

AA_ORDER = list("ACDEFGHIKLMNPQRSTVWY")
SSE_COLORS = {"H": "#e06c75", "E": "#61afef", "C": "#98c379"}

# Kyte-Doolittle hydrophobicity scale
KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
      "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
      "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
      "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}

# Max ASA per residue type (Tien et al. 2013, theoretical)
MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")
    return protein_configs, seqs, ss_dict


def load_conservation(protein: str) -> dict | None:
    """Returns dict: 0-indexed position -> conservation score, or None."""
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/align/TARGET_b*_frequencies.csv"))
    if not candidates:
        return None
    cons = {}
    with open(candidates[0]) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cons[int(row["i"]) - 1] = float(row["conservation"])
    return cons


# ---------------------------------------------------------------------------
# PDB feature extraction
# ---------------------------------------------------------------------------

def _find_pdb(protein: str) -> Path | None:
    """Find the primary PDB file for a protein in its EVcouplings directory."""
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
    # Filter out compare/aux remapped files
    candidates = [c for c in candidates if "compare" not in str(c) and "aux" not in str(c)]
    return candidates[0] if candidates else None


def _align_pdb_to_seq(pdb_residues: list[tuple[int, str]], full_seq: str) -> dict[int, int]:
    """Find the resid offset that best aligns PDB 1-letter codes to full_seq.

    Returns dict: PDB list index -> 0-indexed position in full_seq.
    Only includes positions where the AA identity matches.
    """
    resids = [r[0] for r in pdb_residues]
    aas = [r[1] for r in pdb_residues]
    n_pdb = len(pdb_residues)
    n_seq = len(full_seq)

    best_offset, best_matches = 0, 0
    # Try all offsets: seq_pos = resid + offset
    min_resid = min(resids)
    max_resid = max(resids)
    for offset in range(- max_resid, n_seq - min_resid + 1):
        matches = sum(1 for resid, aa in pdb_residues
                      if 0 <= resid + offset < n_seq and full_seq[resid + offset] == aa)
        if matches > best_matches:
            best_offset, best_matches = offset, matches

    mapping = {}
    for i, (resid, aa) in enumerate(pdb_residues):
        seq_pos = resid + best_offset
        if 0 <= seq_pos < n_seq and full_seq[seq_pos] == aa:
            mapping[i] = seq_pos

    return mapping


def _parse_pdb_residues(pdb_path: Path):
    """Parse PDB, return list of (resid, one_letter_code, CA_coord, CB_coord_or_CA)."""
    from Bio.PDB import PDBParser
    from Bio.Data.IUPACData import protein_letters_3to1

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("prot", str(pdb_path))
    chain = list(structure[0])[0]  # first chain

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


def compute_pdb_features(protein: str, full_seq: str) -> dict | None:
    """Compute RSA, contact number, and long-range contacts from PDB.

    Returns dict: 0-indexed seq position -> {rsa, contacts_8A, contacts_10A, long_range_contacts}
    or None if PDB not available.
    """
    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return None

    pdb_residues_raw, structure = _parse_pdb_residues(pdb_path)
    if not pdb_residues_raw:
        return None

    # Align PDB to full sequence
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues_raw]
    mapping = _align_pdb_to_seq(pdb_tuples, full_seq)
    n_mapped = len(mapping)
    n_total = len(pdb_residues_raw)
    if n_mapped < n_total * 0.5:
        print(f"    WARNING: poor PDB alignment for {protein}: {n_mapped}/{n_total} mapped")
        return None

    # --- RSA via ShrakeRupley ---
    from Bio.PDB import ShrakeRupley
    sr = ShrakeRupley()
    sr.compute(structure[0], level="R")
    chain = list(structure[0])[0]
    sasa_by_resid = {}
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa

    # --- Contact numbers from CB distances ---
    cb_coords = np.array([r["cb"] for r in pdb_residues_raw])
    from scipy.spatial.distance import cdist
    dists = cdist(cb_coords, cb_coords)

    contacts_8A = (dists < 8.0).sum(axis=1) - 1
    contacts_10A = (dists < 10.0).sum(axis=1) - 1

    # Long-range contacts: |i-j| > 12 in PDB order (sequence separation)
    n_pdb = len(pdb_residues_raw)
    long_range = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) > 12 and dists[i, j] < 8.0:
                long_range[i] += 1

    # Build output keyed by 0-indexed seq position
    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_residues_raw[pdb_idx]
        resid = r["resid"]
        aa = r["aa"]
        max_asa = MAX_ASA.get(aa, 200)
        raw_sasa = sasa_by_resid.get(resid, 0.0)
        rsa = min(raw_sasa / max_asa, 1.0) if max_asa > 0 else 0.0

        features[seq_pos] = {
            "rsa": round(rsa, 4),
            "contacts_8A": int(contacts_8A[pdb_idx]),
            "contacts_10A": int(contacts_10A[pdb_idx]),
            "long_range_contacts": int(long_range[pdb_idx]),
        }

    return features


# ---------------------------------------------------------------------------
# Local hydrophobic context (sequence-only)
# ---------------------------------------------------------------------------

def compute_hydrophobic_features(sequence: str) -> list[dict]:
    """Compute per-residue hydrophobic context features from sequence alone."""
    n = len(sequence)
    results = []
    for i in range(n):
        aa = sequence[i]
        self_hydro = KD.get(aa, 0.0)

        # Window averages of KD hydrophobicity
        def window_mean(radius):
            vals = []
            for d in range(-radius, radius + 1):
                j = i + d
                if 0 <= j < n:
                    vals.append(KD.get(sequence[j], 0.0))
            return sum(vals) / len(vals) if vals else 0.0

        local_hydro_w3 = window_mean(1)
        local_hydro_w5 = window_mean(2)
        local_hydro_w7 = window_mean(3)

        # Same-face neighbors in beta strand (positions at ±2 point to same face)
        same_face_vals = [KD.get(sequence[i], 0.0)]
        if i - 2 >= 0:
            same_face_vals.append(KD.get(sequence[i - 2], 0.0))
        if i + 2 < n:
            same_face_vals.append(KD.get(sequence[i + 2], 0.0))
        same_face_hydro = sum(same_face_vals) / len(same_face_vals)

        results.append({
            "self_hydro": round(self_hydro, 3),
            "local_hydro_w3": round(local_hydro_w3, 3),
            "local_hydro_w5": round(local_hydro_w5, 3),
            "local_hydro_w7": round(local_hydro_w7, 3),
            "same_face_hydro": round(same_face_hydro, 3),
        })
    return results


# ---------------------------------------------------------------------------
# SSE feature computation (from v1)
# ---------------------------------------------------------------------------

def compute_sse_features(sse_str: str) -> list[dict]:
    n = len(sse_str)
    features = [None] * n
    i = 0
    while i < n:
        label = sse_str[i]
        j = i
        while j < n and sse_str[j] == label:
            j += 1
        seg_len = j - i
        for pos in range(i, j):
            dist_left = pos - i
            dist_right = j - 1 - pos
            dist_to_boundary = min(dist_left, dist_right)
            features[pos] = {
                "sse": label,
                "seg_len": seg_len,
                "dist_to_boundary": dist_to_boundary,
                "is_boundary": 1 if dist_to_boundary <= 1 else 0,
            }
        i = j
    return features


# ---------------------------------------------------------------------------
# Model loading (from v1)
# ---------------------------------------------------------------------------

def load_model(device: str):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(
        model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager"
    ).to(device).eval()
    model = NNsight(esm_model)
    return model, tokenizer


def extract_head_weights(model, layer: int, head: int) -> dict:
    attn = model._model.esm.encoder.layer[layer].attention
    W_Q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_Q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    W_K = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_K = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    return {
        "W_Q_hd": W_Q[head].clone(),
        "b_Q_d": b_Q[head].clone(),
        "W_K_hd": W_K[head].clone(),
        "b_K_d": b_K[head].clone(),
    }


# ---------------------------------------------------------------------------
# Search direction and projection scores (from v1)
# ---------------------------------------------------------------------------

def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    return W_K.T @ q_mean_norm


def build_clean_sequence(sequence: str, config: dict) -> str:
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_start, ss1_end = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_start, ss2_end = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
    masked = ["<mask>"] * n
    for i in range(ss1_start, ss1_end):
        masked[i] = sequence[i]
    for i in range(ss2_start, ss2_end):
        masked[i] = sequence[i]
    for i in range(max(0, ss1_start - flank), ss1_start):
        masked[i] = sequence[i]
    for i in range(ss2_end, min(n, ss2_end + flank)):
        masked[i] = sequence[i]
    return "".join(masked)


def capture_projection_scores(model, tokenizer, sequence: str, search_dir_unit: torch.Tensor, device: str) -> np.ndarray:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    x_residues = x_ln[1:-1]
    scores = (x_residues @ search_dir_unit.cpu()).numpy()
    return scores


# ---------------------------------------------------------------------------
# OLS (from v1)
# ---------------------------------------------------------------------------

def run_ols(X: np.ndarray, y: np.ndarray, feature_names: list[str]) -> dict:
    n = len(y)
    Xb = np.hstack([np.ones((n, 1)), X])
    k = Xb.shape[1]
    beta, _, _, _ = np.linalg.lstsq(Xb, y, rcond=None)
    y_hat = Xb @ beta
    residuals = y - y_hat
    ss_res = float(np.sum(residuals ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - k)
    sigma2 = ss_res / max(n - k, 1)
    try:
        XtX_inv = np.linalg.pinv(Xb.T @ Xb)
        se = np.sqrt(sigma2 * np.diag(XtX_inv))
    except Exception:
        se = np.full(k, np.nan)
    t_stats = beta / np.where(se > 0, se, np.nan)
    p_values = 2 * stats.t.sf(np.abs(t_stats), df=max(n - k, 1))
    return {
        "feature_names": ["intercept"] + list(feature_names),
        "beta": beta,
        "se": se,
        "t_stats": t_stats,
        "p_values": p_values,
        "r2": r2,
        "adj_r2": adj_r2,
        "residuals": residuals,
        "y_hat": y_hat,
        "n": n,
        "k": k,
    }


def format_ols_table(result: dict) -> list[str]:
    lines = []
    lines.append(f"N={result['n']}, k={result['k']}, R2={result['r2']:.4f}, adj-R2={result['adj_r2']:.4f}\n\n")
    lines.append("| Feature | Coef | SE | t | p |\n")
    lines.append("|---------|------|-----|---|---|\n")
    for fname, b, s, t, p in zip(result["feature_names"], result["beta"], result["se"], result["t_stats"], result["p_values"]):
        star = "**" if p < 0.01 else ("*" if p < 0.05 else "")
        lines.append(f"| {fname} | {b:.4f} | {s:.4f} | {t:.2f} | {p:.4f}{star} |\n")
    return lines


# ---------------------------------------------------------------------------
# Assemble per-protein data
# ---------------------------------------------------------------------------

def build_protein_data(
    protein: str,
    sequence: str,
    config: dict,
    sse_str: str,
    conservation: dict | None,
    pdb_features: dict | None,
    hydro_features: list[dict],
    proj_scores_full: np.ndarray,
    anchor_pos: int,
    protein_idx: int,
) -> list[dict]:
    n = len(sequence)
    sse_features = compute_sse_features(sse_str)
    pos1, pos2 = config["contact_pair"]

    rows = []
    for j in range(n):
        if j >= len(proj_scores_full):
            break
        aa = sequence[j]
        sse_f = sse_features[j] if j < len(sse_features) else {"sse": "C", "seg_len": 1, "dist_to_boundary": 0, "is_boundary": 1}
        cons_val = conservation.get(j, np.nan) if conservation else np.nan

        pdb_f = pdb_features.get(j, {}) if pdb_features else {}
        rsa_val = pdb_f.get("rsa", np.nan)
        contacts_8A = pdb_f.get("contacts_8A", np.nan)
        contacts_10A = pdb_f.get("contacts_10A", np.nan)
        long_range = pdb_f.get("long_range_contacts", np.nan)

        hf = hydro_features[j]

        rows.append({
            "protein": protein,
            "protein_idx": protein_idx,
            "pos": j,
            "aa": aa,
            "is_anchor": 1 if j == anchor_pos else 0,
            "proj_full": float(proj_scores_full[j]),
            "sse": sse_f["sse"],
            "seg_len": sse_f["seg_len"],
            "dist_to_boundary": sse_f["dist_to_boundary"],
            "is_boundary": sse_f["is_boundary"],
            "conservation": cons_val,
            "rsa": rsa_val,
            "contacts_8A": contacts_8A,
            "contacts_10A": contacts_10A,
            "long_range_contacts": long_range,
            "self_hydro": hf["self_hydro"],
            "local_hydro_w5": hf["local_hydro_w5"],
            "same_face_hydro": hf["same_face_hydro"],
        })
    return rows


# ---------------------------------------------------------------------------
# Feature matrix builders
# ---------------------------------------------------------------------------

def _base_cols(rows):
    """SSE + position + protein dummies (always included)."""
    cols, names = [], []
    cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
    cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
    cols.append(np.array([float(r["dist_to_boundary"]) for r in rows])); names.append("dist_to_boundary")
    cols.append(np.array([float(r["seg_len"]) for r in rows])); names.append("seg_len")
    cols.append(np.array([float(r["is_boundary"]) for r in rows])); names.append("is_boundary")
    return cols, names


def _protein_dummies(rows):
    proteins = sorted(set(r["protein"] for r in rows))
    cols, names = [], []
    for p in proteins[1:]:
        cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
    return cols, names


def build_model_a(rows):
    """Model A: SSE + protein FE (v1 baseline)."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = [], []
    cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
    cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_b(rows):
    """Model B: + RSA."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_c(rows):
    """Model C: + RSA + local hydrophobic context."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["self_hydro"] for r in rows], dtype=float)); names.append("self_hydro")
    cols.append(np.array([r["local_hydro_w5"] for r in rows], dtype=float)); names.append("local_hydro_w5")
    cols.append(np.array([r["same_face_hydro"] for r in rows], dtype=float)); names.append("same_face_hydro")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_d(rows):
    """Model D: + RSA + local context + 3D contact number."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["self_hydro"] for r in rows], dtype=float)); names.append("self_hydro")
    cols.append(np.array([r["local_hydro_w5"] for r in rows], dtype=float)); names.append("local_hydro_w5")
    cols.append(np.array([r["same_face_hydro"] for r in rows], dtype=float)); names.append("same_face_hydro")
    cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float)); names.append("contacts_8A")
    cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float)); names.append("long_range_contacts")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_e(rows):
    """Model E: + conservation + AA identity (subset with conservation)."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["self_hydro"] for r in rows], dtype=float)); names.append("self_hydro")
    cols.append(np.array([r["local_hydro_w5"] for r in rows], dtype=float)); names.append("local_hydro_w5")
    cols.append(np.array([r["same_face_hydro"] for r in rows], dtype=float)); names.append("same_face_hydro")
    cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float)); names.append("contacts_8A")
    cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float)); names.append("long_range_contacts")
    cols.append(np.array([r["conservation"] for r in rows], dtype=float)); names.append("conservation")
    for aa in AA_ORDER[1:]:
        cols.append(np.array([1.0 if r["aa"] == aa else 0.0 for r in rows])); names.append(f"AA_{aa}")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_e_proj_vs_rsa(all_rows: list[dict], output_dir: Path) -> None:
    """Plot E: Projection score vs RSA, colored by SSE."""
    rows = [r for r in all_rows if not np.isnan(r["rsa"])]
    if not rows:
        print("  Plot E skipped: no RSA data")
        return
    fig, ax = plt.subplots(figsize=(6, 5))
    for s in ["H", "E", "C"]:
        sr = [r for r in rows if r["sse"] == s]
        if sr:
            ax.scatter([r["rsa"] for r in sr], [r["proj_full"] for r in sr],
                       color=SSE_COLORS[s], alpha=0.2, s=8, label=s)
    anchors = [r for r in rows if r["is_anchor"]]
    if anchors:
        ax.scatter([r["rsa"] for r in anchors], [r["proj_full"] for r in anchors],
                   color="black", marker="*", s=120, zorder=5, label="anchor")
    ax.set_xlabel("Relative Solvent Accessibility")
    ax.set_ylabel("Projection score")
    ax.set_title("Projection score vs RSA")
    ax.legend(fontsize=8)
    r_rsa = np.array([r["rsa"] for r in rows])
    r_proj = np.array([r["proj_full"] for r in rows])
    corr = float(np.corrcoef(r_rsa, r_proj)[0, 1])
    ax.text(0.02, 0.98, f"r = {corr:.3f}", transform=ax.transAxes, va="top", fontsize=9)
    plt.tight_layout()
    out = output_dir / "anchor_regression_v2_E_proj_vs_rsa.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_f_proj_vs_contacts(all_rows: list[dict], output_dir: Path) -> None:
    """Plot F: Projection score vs 3D contact number."""
    rows = [r for r in all_rows if not np.isnan(r["contacts_8A"])]
    if not rows:
        print("  Plot F skipped: no contact data")
        return
    fig, ax = plt.subplots(figsize=(6, 5))
    for s in ["H", "E", "C"]:
        sr = [r for r in rows if r["sse"] == s]
        if sr:
            ax.scatter([r["contacts_8A"] for r in sr], [r["proj_full"] for r in sr],
                       color=SSE_COLORS[s], alpha=0.2, s=8, label=s)
    anchors = [r for r in rows if r["is_anchor"]]
    if anchors:
        ax.scatter([r["contacts_8A"] for r in anchors], [r["proj_full"] for r in anchors],
                   color="black", marker="*", s=120, zorder=5, label="anchor")
    ax.set_xlabel("3D contact number (8 A)")
    ax.set_ylabel("Projection score")
    ax.set_title("Projection score vs 3D contact number")
    ax.legend(fontsize=8)
    r_c = np.array([r["contacts_8A"] for r in rows])
    r_proj = np.array([r["proj_full"] for r in rows])
    corr = float(np.corrcoef(r_c, r_proj)[0, 1])
    ax.text(0.02, 0.98, f"r = {corr:.3f}", transform=ax.transAxes, va="top", fontsize=9)
    plt.tight_layout()
    out = output_dir / "anchor_regression_v2_F_proj_vs_contacts.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_g_sequence_profile_with_rsa(all_rows: list[dict], protein_configs: dict, output_dir: Path) -> None:
    """Plot G: Sequence profile with RSA overlay (2-panel per protein, max 5 proteins)."""
    proteins = sorted(set(r["protein"] for r in all_rows))
    proteins_with_rsa = [p for p in proteins if any(not np.isnan(r["rsa"]) for r in all_rows if r["protein"] == p)]
    if not proteins_with_rsa:
        print("  Plot G skipped: no RSA data")
        return
    show = proteins_with_rsa[:5]
    fig, axes = plt.subplots(len(show), 1, figsize=(16, 3.5 * len(show)), squeeze=False)
    for i, protein in enumerate(show):
        ax = axes[i, 0]
        prows = sorted([r for r in all_rows if r["protein"] == protein], key=lambda r: r["pos"])
        positions = [r["pos"] for r in prows]
        scores = [r["proj_full"] for r in prows]
        rsa_vals = [r["rsa"] for r in prows]
        sse_labels = [r["sse"] for r in prows]

        # Background SSE coloring
        prev_pos, prev_sse = positions[0], sse_labels[0]
        for k in range(1, len(positions) + 1):
            if k == len(positions) or sse_labels[k] != prev_sse:
                ax.axvspan(prev_pos - 0.5, positions[k - 1] + 0.5, alpha=0.15,
                           color=SSE_COLORS.get(prev_sse, "#aaaaaa"), lw=0)
                if k < len(positions):
                    prev_pos, prev_sse = positions[k], sse_labels[k]

        ax.plot(positions, scores, color="#444444", lw=0.8, alpha=0.9, label="proj score")

        # RSA on secondary axis
        ax2 = ax.twinx()
        rsa_clean = [(p, v) for p, v in zip(positions, rsa_vals) if not np.isnan(v)]
        if rsa_clean:
            ax2.plot([p for p, v in rsa_clean], [v for p, v in rsa_clean],
                     color="#e67e22", lw=0.6, alpha=0.6, label="RSA")
            ax2.set_ylabel("RSA", color="#e67e22")
            ax2.set_ylim(0, 1.1)

        # Mark anchor
        anchor_pos = ANCHOR_POSITIONS[protein]
        anchor_score = next((r["proj_full"] for r in prows if r["pos"] == anchor_pos), None)
        if anchor_score is not None:
            ax.scatter([anchor_pos], [anchor_score], color="red", s=60, zorder=6, label="anchor")

        ax.set_title(protein, fontsize=9)
        ax.set_xlabel("Residue position")
        ax.set_ylabel("Projection score")

    plt.tight_layout()
    out = output_dir / "anchor_regression_v2_G_profile_rsa.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_h_feature_importance(importances: dict, output_dir: Path) -> None:
    """Plot H: Feature importance bar chart from Random Forest."""
    sorted_feats = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    names = [f for f, _ in sorted_feats[:15]]
    vals = [v for _, v in sorted_feats[:15]]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(range(len(names)), vals, color="#61afef")
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Feature importance")
    ax.set_title("Random Forest feature importances (top 15)")
    plt.tight_layout()
    out = output_dir / "anchor_regression_v2_H_rf_importance.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading configs...")
    protein_configs, seqs, ss_dict = load_configs()

    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    print("Extracting L10H9 weights and computing search direction from 2B61A...")
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir = compute_search_dir(model, tokenizer, ref_clean, weights, args.device)
    search_dir_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)
    print(f"  Search direction norm: {search_dir.norm().item():.4f}")

    print("\nProcessing proteins...")
    all_rows = []
    pdb_coverage = {"with_pdb": 0, "without_pdb": 0}
    for p_idx, (protein, anchor_pos) in enumerate(ANCHOR_POSITIONS.items()):
        print(f"  {protein}...")
        sequence = seqs[protein]
        config = protein_configs[protein]
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            print(f"    WARNING: SSE length mismatch ({len(sse_str)} vs {len(sequence)}), padding with C")
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")

        conservation = load_conservation(protein)
        if conservation is None:
            print(f"    No conservation data")

        pdb_features = compute_pdb_features(protein, sequence)
        if pdb_features is None:
            print(f"    No PDB features")
            pdb_coverage["without_pdb"] += 1
        else:
            n_mapped = len(pdb_features)
            print(f"    PDB features: {n_mapped}/{len(sequence)} positions mapped")
            pdb_coverage["with_pdb"] += 1

        hydro_features = compute_hydrophobic_features(sequence)

        proj_full = capture_projection_scores(model, tokenizer, sequence, search_dir_unit, args.device)

        anchor_score = proj_full[anchor_pos]
        anchor_rank = int((proj_full > anchor_score).sum()) + 1
        print(f"    Anchor rank (full seq): {anchor_rank}/{len(proj_full)}, score={anchor_score:.3f}")

        rows = build_protein_data(protein, sequence, config, sse_str, conservation,
                                  pdb_features, hydro_features, proj_full, anchor_pos, p_idx)
        all_rows.extend(rows)
        print(f"    {len(rows)} residues added")

    n_total = len(all_rows)
    print(f"\nTotal rows: {n_total}")
    print(f"PDB coverage: {pdb_coverage['with_pdb']} proteins with PDB, {pdb_coverage['without_pdb']} without")

    # Filter subsets
    rows_with_rsa = [r for r in all_rows if not np.isnan(r["rsa"])]
    rows_with_pdb = [r for r in all_rows if not np.isnan(r["contacts_8A"])]
    rows_with_cons = [r for r in all_rows if not np.isnan(r["conservation"])]
    rows_with_all = [r for r in all_rows if not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]
    rows_with_cons_and_pdb = [r for r in rows_with_all if not np.isnan(r["conservation"])]
    print(f"Rows with RSA: {len(rows_with_rsa)}")
    print(f"Rows with PDB (contacts): {len(rows_with_pdb)}")
    print(f"Rows with conservation: {len(rows_with_cons)}")
    print(f"Rows with all structural features: {len(rows_with_all)}")
    print(f"Rows with conservation + PDB: {len(rows_with_cons_and_pdb)}")

    # Sanity: check anchor features
    anchor_rows = [r for r in all_rows if r["is_anchor"]]
    print("\nAnchor feature summary:")
    for r in anchor_rows:
        rsa_str = f"{r['rsa']:.3f}" if not np.isnan(r["rsa"]) else "NaN"
        c8_str = f"{r['contacts_8A']:.0f}" if not np.isnan(r["contacts_8A"]) else "NaN"
        lr_str = f"{r['long_range_contacts']:.0f}" if not np.isnan(r["long_range_contacts"]) else "NaN"
        print(f"  {r['protein']}: pos={r['pos']} ({r['aa']}), proj={r['proj_full']:.3f}, sse={r['sse']}, RSA={rsa_str}, contacts_8A={c8_str}, LR_contacts={lr_str}, self_hydro={r['self_hydro']:.1f}")

    # ---------------------------------------------------------------------------
    # Plots
    # ---------------------------------------------------------------------------
    print("\nGenerating plots...")
    plot_e_proj_vs_rsa(all_rows, REPORT_DIR)
    plot_f_proj_vs_contacts(all_rows, REPORT_DIR)
    plot_g_sequence_profile_with_rsa(all_rows, protein_configs, REPORT_DIR)

    # ---------------------------------------------------------------------------
    # OLS Regressions (on rows with all structural features)
    # ---------------------------------------------------------------------------
    print("\nRunning OLS regressions (on rows with complete PDB features)...")
    work_rows = rows_with_all

    # Model A: SSE + protein FE (baseline)
    Xa, na, ya = build_model_a(work_rows)
    res_a = run_ols(Xa, ya, na)
    print(f"  Model A (SSE + protein FE):              R2={res_a['r2']:.4f}, adj-R2={res_a['adj_r2']:.4f}, N={res_a['n']}")

    # Model B: + RSA
    Xb, nb, yb = build_model_b(work_rows)
    res_b = run_ols(Xb, yb, nb)
    print(f"  Model B (+ RSA):                         R2={res_b['r2']:.4f}, adj-R2={res_b['adj_r2']:.4f}")

    # Model C: + RSA + hydrophobic context
    Xc, nc, yc = build_model_c(work_rows)
    res_c = run_ols(Xc, yc, nc)
    print(f"  Model C (+ RSA + hydrophobic context):    R2={res_c['r2']:.4f}, adj-R2={res_c['adj_r2']:.4f}")

    # Model D: + RSA + hydrophobic + contacts
    Xd, nd, yd = build_model_d(work_rows)
    res_d = run_ols(Xd, yd, nd)
    print(f"  Model D (+ RSA + hydro + contacts):       R2={res_d['r2']:.4f}, adj-R2={res_d['adj_r2']:.4f}")

    # Model E: + conservation + AA identity (subset with conservation)
    if rows_with_cons_and_pdb:
        Xe, ne, ye = build_model_e(rows_with_cons_and_pdb)
        res_e = run_ols(Xe, ye, ne)
        print(f"  Model E (+ cons + AA, {len(rows_with_cons_and_pdb)} rows): R2={res_e['r2']:.4f}, adj-R2={res_e['adj_r2']:.4f}")
    else:
        res_e = None
        print("  Model E skipped: no rows with conservation + PDB")

    # Model F: kitchen sink without AA dummies (all proteins with PDB)
    # Same as Model D — already uses all proteins
    # Just rename for clarity
    res_f = res_d  # already on all PDB-available proteins

    # ---------------------------------------------------------------------------
    # Random Forest (Step 4)
    # ---------------------------------------------------------------------------
    print("\nRunning Random Forest / Gradient Boosting...")
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.model_selection import cross_val_score

    rf_feature_names = ["SSE_E", "SSE_H", "RSA", "self_hydro", "local_hydro_w5",
                        "same_face_hydro", "contacts_8A", "long_range_contacts",
                        "dist_to_boundary", "seg_len"]

    def build_rf_matrix(rows):
        X_cols = []
        X_cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows]))
        X_cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows]))
        X_cols.append(np.array([r["rsa"] for r in rows], dtype=float))
        X_cols.append(np.array([r["self_hydro"] for r in rows], dtype=float))
        X_cols.append(np.array([r["local_hydro_w5"] for r in rows], dtype=float))
        X_cols.append(np.array([r["same_face_hydro"] for r in rows], dtype=float))
        X_cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float))
        X_cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float))
        X_cols.append(np.array([float(r["dist_to_boundary"]) for r in rows]))
        X_cols.append(np.array([float(r["seg_len"]) for r in rows]))
        return np.column_stack(X_cols)

    X_rf = build_rf_matrix(work_rows)
    y_rf = np.array([r["proj_full"] for r in work_rows], dtype=float)

    rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    cv_rf = cross_val_score(rf, X_rf, y_rf, cv=5, scoring="r2")
    print(f"  RF 5-fold CV R2: {cv_rf.mean():.4f} +/- {cv_rf.std():.4f}")

    gb = GradientBoostingRegressor(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    cv_gb = cross_val_score(gb, X_rf, y_rf, cv=5, scoring="r2")
    print(f"  GB 5-fold CV R2: {cv_gb.mean():.4f} +/- {cv_gb.std():.4f}")

    # Fit RF on all data for feature importances
    rf.fit(X_rf, y_rf)
    rf_importances = dict(zip(rf_feature_names, rf.feature_importances_))
    rf_r2_train = rf.score(X_rf, y_rf)
    print(f"  RF train R2: {rf_r2_train:.4f}")
    print("  RF feature importances:")
    for feat, imp in sorted(rf_importances.items(), key=lambda x: x[1], reverse=True):
        print(f"    {feat}: {imp:.4f}")

    plot_h_feature_importance(rf_importances, REPORT_DIR)

    # ---------------------------------------------------------------------------
    # Anchor residual analysis (Step 5)
    # ---------------------------------------------------------------------------
    print("\nAnchor residual analysis...")

    # Best OLS model on all proteins: Model D
    residual_std_d = float(np.std(res_d["residuals"]))
    anchor_residuals_d = {}
    for r in anchor_rows:
        protein = r["protein"]
        pos = r["pos"]
        idx = next((i for i, row in enumerate(work_rows) if row["protein"] == protein and row["pos"] == pos), None)
        if idx is None:
            anchor_residuals_d[protein] = {"actual": r["proj_full"], "predicted": np.nan, "residual": np.nan, "z_score": np.nan, "note": "not in PDB"}
            continue
        resid = res_d["residuals"][idx]
        yhat = res_d["y_hat"][idx]
        z = resid / residual_std_d
        anchor_residuals_d[protein] = {"actual": r["proj_full"], "predicted": float(yhat), "residual": float(resid), "z_score": float(z)}
        print(f"  {protein} (OLS-D): actual={r['proj_full']:.3f}, predicted={yhat:.3f}, z={z:.2f}")

    # RF residuals
    rf_pred = rf.predict(X_rf)
    rf_residuals = y_rf - rf_pred
    rf_resid_std = float(np.std(rf_residuals))
    anchor_residuals_rf = {}
    for r in anchor_rows:
        protein = r["protein"]
        pos = r["pos"]
        idx = next((i for i, row in enumerate(work_rows) if row["protein"] == protein and row["pos"] == pos), None)
        if idx is None:
            anchor_residuals_rf[protein] = {"actual": r["proj_full"], "predicted": np.nan, "residual": np.nan, "z_score": np.nan, "note": "not in PDB"}
            continue
        pred = float(rf_pred[idx])
        resid = float(rf_residuals[idx])
        z = resid / rf_resid_std
        anchor_residuals_rf[protein] = {"actual": r["proj_full"], "predicted": pred, "residual": resid, "z_score": z}
        print(f"  {protein} (RF):    actual={r['proj_full']:.3f}, predicted={pred:.3f}, z={z:.2f}")

    # ---------------------------------------------------------------------------
    # Write report
    # ---------------------------------------------------------------------------
    print("\nWriting report...")
    report = []
    report.append("# Expanded Anchor Feature Regression (v2)\n\n")
    report.append(f"Search direction: L10H9 key-side W_K^T @ q_mean from {REFERENCE_PROTEIN} clean masked sequence.\n")
    report.append("Target: key score = dot(post-LN residual at layer 10, W_K^T @ q_mean_unit), on full unmasked sequence.\n")
    report.append(f"Total residues: {n_total} across {len(ANCHOR_POSITIONS)} proteins.\n")
    report.append(f"Residues with PDB features: {len(rows_with_all)} ({pdb_coverage['with_pdb']} proteins).\n")
    report.append(f"Residues with conservation + PDB: {len(rows_with_cons_and_pdb)}.\n\n")

    report.append("## New features in v2\n\n")
    report.append("- RSA: Relative Solvent Accessibility via ShrakeRupley (normalized by Tien et al. 2013 max ASA).\n")
    report.append("- self_hydro: Kyte-Doolittle hydrophobicity of the residue.\n")
    report.append("- local_hydro_w5: Mean KD hydrophobicity in a window of +/-2 residues.\n")
    report.append("- same_face_hydro: Mean KD hydrophobicity of same-face beta-strand neighbors (positions i-2, i, i+2).\n")
    report.append("- contacts_8A: Number of CB-CB contacts within 8 A (CA for glycine).\n")
    report.append("- long_range_contacts: Contacts within 8 A with sequence separation > 12.\n\n")

    report.append("## Anchor feature summary\n\n")
    report.append("| Protein | Pos | AA | SSE | Proj | RSA | Contacts 8A | LR contacts | Self hydro |\n")
    report.append("|---------|-----|-----|-----|------|-----|-------------|-------------|------------|\n")
    for r in anchor_rows:
        rsa_str = f"{r['rsa']:.3f}" if not np.isnan(r["rsa"]) else "-"
        c8_str = f"{r['contacts_8A']:.0f}" if not np.isnan(r["contacts_8A"]) else "-"
        lr_str = f"{r['long_range_contacts']:.0f}" if not np.isnan(r["long_range_contacts"]) else "-"
        report.append(f"| {r['protein']} | {r['pos']} | {r['aa']} | {r['sse']} | {r['proj_full']:.3f} | {rsa_str} | {c8_str} | {lr_str} | {r['self_hydro']:.1f} |\n")
    report.append("\n")

    report.append("## OLS Model R2 summary\n\n")
    report.append("All models fit on rows with complete PDB features (RSA + contacts).\n\n")
    report.append("| Model | Description | N | R2 | adj-R2 |\n")
    report.append("|-------|-------------|---|-----|--------|\n")
    report.append(f"| A | SSE + protein FE | {res_a['n']} | {res_a['r2']:.4f} | {res_a['adj_r2']:.4f} |\n")
    report.append(f"| B | A + position + RSA | {res_b['n']} | {res_b['r2']:.4f} | {res_b['adj_r2']:.4f} |\n")
    report.append(f"| C | B + hydrophobic context | {res_c['n']} | {res_c['r2']:.4f} | {res_c['adj_r2']:.4f} |\n")
    report.append(f"| D | C + 3D contact number | {res_d['n']} | {res_d['r2']:.4f} | {res_d['adj_r2']:.4f} |\n")
    if res_e:
        report.append(f"| E | D + conservation + AA identity | {res_e['n']} | {res_e['r2']:.4f} | {res_e['adj_r2']:.4f} |\n")
    report.append("\n")

    for label, res, note in [
        ("Model A: SSE + protein FE", res_a, "baseline"),
        ("Model B: + position + RSA", res_b, ""),
        ("Model C: + hydrophobic context", res_c, ""),
        ("Model D: + 3D contacts", res_d, "best linear, all proteins"),
    ]:
        report.append(f"## {label}" + (f" ({note})" if note else "") + "\n\n")
        report.extend(format_ols_table(res))
        report.append("\n")
    if res_e:
        report.append("## Model E: + conservation + AA identity (conservation subset)\n\n")
        report.extend(format_ols_table(res_e))
        report.append("\n")

    report.append("## Random Forest / Gradient Boosting\n\n")
    report.append(f"Features: {', '.join(rf_feature_names)}\n\n")
    report.append(f"RF 5-fold CV R2: {cv_rf.mean():.4f} +/- {cv_rf.std():.4f}\n\n")
    report.append(f"GB 5-fold CV R2: {cv_gb.mean():.4f} +/- {cv_gb.std():.4f}\n\n")
    report.append(f"RF train R2: {rf_r2_train:.4f}\n\n")
    report.append("RF feature importances:\n\n")
    report.append("| Feature | Importance |\n")
    report.append("|---------|------------|\n")
    for feat, imp in sorted(rf_importances.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {feat} | {imp:.4f} |\n")
    report.append("\n")

    report.append("## Anchor residual analysis\n\n")
    report.append(f"OLS Model D residual std: {residual_std_d:.4f}\n\n")
    report.append(f"RF residual std: {rf_resid_std:.4f}\n\n")
    report.append("| Protein | Actual | Pred (OLS-D) | Z (OLS-D) | Pred (RF) | Z (RF) |\n")
    report.append("|---------|--------|-------------|-----------|-----------|--------|\n")
    for protein in ANCHOR_POSITIONS:
        d = anchor_residuals_d.get(protein, {})
        rf_d = anchor_residuals_rf.get(protein, {})
        if "note" in d:
            report.append(f"| {protein} | {d.get('actual', 0):.3f} | - | - | - | - | ({d['note']}) |\n")
        else:
            report.append(f"| {protein} | {d['actual']:.3f} | {d['predicted']:.3f} | {d['z_score']:.2f} | {rf_d['predicted']:.3f} | {rf_d['z_score']:.2f} |\n")
    report.append("\n")

    # Summary statistics on anchor z-scores
    ols_zs = [d["z_score"] for d in anchor_residuals_d.values() if not np.isnan(d.get("z_score", np.nan))]
    rf_zs = [d["z_score"] for d in anchor_residuals_rf.values() if not np.isnan(d.get("z_score", np.nan))]
    if ols_zs:
        report.append(f"OLS-D anchor z-scores: mean={np.mean(ols_zs):.2f}, median={np.median(ols_zs):.2f}, range=[{min(ols_zs):.2f}, {max(ols_zs):.2f}]\n\n")
    if rf_zs:
        report.append(f"RF anchor z-scores: mean={np.mean(rf_zs):.2f}, median={np.median(rf_zs):.2f}, range=[{min(rf_zs):.2f}, {max(rf_zs):.2f}]\n\n")

    n_within_2sigma_ols = sum(1 for z in ols_zs if abs(z) <= 2)
    n_above_4sigma_ols = sum(1 for z in ols_zs if abs(z) >= 4)
    n_within_2sigma_rf = sum(1 for z in rf_zs if abs(z) <= 2)
    n_above_4sigma_rf = sum(1 for z in rf_zs if abs(z) >= 4)
    report.append(f"OLS-D: {n_within_2sigma_ols}/{len(ols_zs)} anchors within 2 sigma, {n_above_4sigma_ols}/{len(ols_zs)} above 4 sigma.\n\n")
    report.append(f"RF: {n_within_2sigma_rf}/{len(rf_zs)} anchors within 2 sigma, {n_above_4sigma_rf}/{len(rf_zs)} above 4 sigma.\n\n")

    out_path = REPORT_DIR / "anchor_regression_v2.md"
    with open(out_path, "w") as f:
        f.writelines(report)
    print(f"  Saved: {out_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()
