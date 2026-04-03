#!/usr/bin/env python3
"""Anchor feature regression with matched controls (Experiment 3_27_anchor_regression_v3.md).

Extends v2 with:
  - Graph / long-range / spread structural features
  - Matched-control analysis (anchor vs RSA/contact-matched non-anchors)
  - Leave-one-protein-out classification

Usage:
    uv run python scripts/anchor_regression_v3.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy import stats
from scipy.spatial.distance import cdist
import networkx as nx

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
TOP_K_ANCHORS = 3  # default number of anchor residues per protein

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

KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
      "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
      "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
      "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


# ---------------------------------------------------------------------------
# Data loading (from v2)
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
# PDB parsing and alignment (from v2)
# ---------------------------------------------------------------------------

def _find_pdb(protein: str) -> Path | None:
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
    candidates = [c for c in candidates if "compare" not in str(c) and "aux" not in str(c)]
    return candidates[0] if candidates else None


def _parse_pdb_residues(pdb_path: Path):
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


def _align_pdb_to_seq(pdb_residues: list[tuple[int, str]], full_seq: str) -> dict[int, int]:
    resids = [r[0] for r in pdb_residues]
    n_seq = len(full_seq)
    min_resid = min(resids)
    max_resid = max(resids)

    best_offset, best_matches = 0, 0
    for offset in range(-max_resid, n_seq - min_resid + 1):
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


# ---------------------------------------------------------------------------
# Extended PDB feature extraction (v3: adds graph, spread, SSE-partner features)
# ---------------------------------------------------------------------------

def compute_pdb_features_v3(protein: str, full_seq: str, sse_str: str) -> dict | None:
    """Compute all PDB-derived features including v2 features + v3 graph/spread features.

    Returns dict: 0-indexed seq position -> feature dict, or None if PDB not available.
    """
    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return None

    pdb_residues_raw, structure = _parse_pdb_residues(pdb_path)
    if not pdb_residues_raw:
        return None

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

    # --- Distance matrix from CB coords ---
    cb_coords = np.array([r["cb"] for r in pdb_residues_raw])
    n_pdb = len(pdb_residues_raw)
    dists = cdist(cb_coords, cb_coords)

    # --- v2 contact counts ---
    contacts_8A_arr = (dists < 8.0).sum(axis=1) - 1
    contacts_10A_arr = (dists < 10.0).sum(axis=1) - 1

    long_range_arr = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) > 12 and dists[i, j] < 8.0:
                long_range_arr[i] += 1

    # --- Build contact adjacency (8A) for graph and new features ---
    contact_mask_8A = (dists < 8.0)
    np.fill_diagonal(contact_mask_8A, False)

    # --- SSE segment assignment ---
    # Map each PDB residue to its SSE segment ID (contiguous runs of same SSE type)
    # First, assign segment IDs to full sequence positions
    seg_ids = np.full(len(full_seq), -1, dtype=int)
    seg_id = 0
    i = 0
    while i < len(sse_str):
        label = sse_str[i]
        j = i
        while j < len(sse_str) and sse_str[j] == label:
            j += 1
        for pos in range(i, j):
            seg_ids[pos] = seg_id
        seg_id += 1
        i = j

    # Map PDB index -> SSE segment ID via the alignment mapping
    pdb_seg_ids = np.full(n_pdb, -1, dtype=int)
    for pdb_idx, seq_pos in mapping.items():
        if seq_pos < len(seg_ids):
            pdb_seg_ids[pdb_idx] = seg_ids[seq_pos]

    # --- v3 Feature 1: long-range contact fraction ---
    long_range_fraction = long_range_arr / np.maximum(contacts_8A_arr, 1).astype(float)

    # --- v3 Feature 2: mean and max contact span ---
    mean_contact_span = np.zeros(n_pdb)
    max_contact_span = np.zeros(n_pdb)
    for i in range(n_pdb):
        partners = np.where(contact_mask_8A[i])[0]
        if len(partners) > 0:
            spans = np.abs(partners - i)
            mean_contact_span[i] = spans.mean()
            max_contact_span[i] = spans.max()

    # --- v3 Feature 3: contact spread across sequence bins ---
    n_bins = 8
    bin_edges = np.linspace(0, n_pdb, n_bins + 1)
    n_contact_bins_arr = np.zeros(n_pdb, dtype=int)
    contact_bin_entropy_arr = np.zeros(n_pdb)
    for i in range(n_pdb):
        partners = np.where(contact_mask_8A[i])[0]
        if len(partners) == 0:
            continue
        bin_assignments = np.digitize(partners, bin_edges[1:])
        bin_assignments = np.clip(bin_assignments, 0, n_bins - 1)
        unique_bins = len(set(bin_assignments))
        n_contact_bins_arr[i] = unique_bins
        # Entropy over bin counts
        counts = np.bincount(bin_assignments, minlength=n_bins).astype(float)
        counts = counts[counts > 0]
        probs = counts / counts.sum()
        contact_bin_entropy_arr[i] = float(-np.sum(probs * np.log2(probs)))

    # --- v3 Feature 4: distinct SSE partners ---
    n_distinct_sse_partners = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        partners = np.where(contact_mask_8A[i])[0]
        if len(partners) == 0:
            continue
        partner_seg_ids = set(pdb_seg_ids[p] for p in partners if pdb_seg_ids[p] >= 0)
        # Exclude own segment
        own_seg = pdb_seg_ids[i]
        partner_seg_ids.discard(own_seg)
        n_distinct_sse_partners[i] = len(partner_seg_ids)

    # --- v3 Feature 5: out-of-segment contact count ---
    contacts_outside_own_sse = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        own_seg = pdb_seg_ids[i]
        partners = np.where(contact_mask_8A[i])[0]
        for p in partners:
            if pdb_seg_ids[p] != own_seg:
                contacts_outside_own_sse[i] += 1
    fraction_contacts_outside_own_sse = contacts_outside_own_sse / np.maximum(contacts_8A_arr, 1).astype(float)

    # --- v3 Feature 6: graph centrality ---
    G = nx.Graph()
    for i in range(n_pdb):
        G.add_node(i)
    for i in range(n_pdb):
        for j in range(i + 1, n_pdb):
            if contact_mask_8A[i, j]:
                G.add_edge(i, j)

    degree_arr = np.array([G.degree(i) for i in range(n_pdb)], dtype=float)

    # Betweenness (can be slow for large proteins, but fine for typical sizes <500)
    betweenness_dict = nx.betweenness_centrality(G)
    betweenness_arr = np.array([betweenness_dict[i] for i in range(n_pdb)])

    closeness_dict = nx.closeness_centrality(G)
    closeness_arr = np.array([closeness_dict[i] for i in range(n_pdb)])

    try:
        eigenvector_dict = nx.eigenvector_centrality(G, max_iter=1000)
        eigenvector_arr = np.array([eigenvector_dict[i] for i in range(n_pdb)])
    except nx.PowerIterationFailedConvergence:
        eigenvector_arr = np.zeros(n_pdb)

    core_number_dict = nx.core_number(G)
    core_number_arr = np.array([core_number_dict[i] for i in range(n_pdb)], dtype=float)

    # --- v3 Feature 7: clustering coefficient ---
    clustering_dict = nx.clustering(G)
    clustering_arr = np.array([clustering_dict[i] for i in range(n_pdb)])

    # --- v3 Feature 8: bridge score ---
    bridge_score_arr = betweenness_arr / np.maximum(degree_arr, 1.0)

    # --- Build output keyed by 0-indexed seq position ---
    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_residues_raw[pdb_idx]
        resid = r["resid"]
        aa = r["aa"]
        max_asa = MAX_ASA.get(aa, 200)
        raw_sasa = sasa_by_resid.get(resid, 0.0)
        rsa = min(raw_sasa / max_asa, 1.0) if max_asa > 0 else 0.0

        features[seq_pos] = {
            # v2 features
            "rsa": round(rsa, 4),
            "contacts_8A": int(contacts_8A_arr[pdb_idx]),
            "contacts_10A": int(contacts_10A_arr[pdb_idx]),
            "long_range_contacts": int(long_range_arr[pdb_idx]),
            # v3 features
            "long_range_fraction": round(float(long_range_fraction[pdb_idx]), 4),
            "mean_contact_span": round(float(mean_contact_span[pdb_idx]), 2),
            "max_contact_span": round(float(max_contact_span[pdb_idx]), 2),
            "n_contact_bins": int(n_contact_bins_arr[pdb_idx]),
            "contact_bin_entropy": round(float(contact_bin_entropy_arr[pdb_idx]), 4),
            "n_distinct_sse_partners": int(n_distinct_sse_partners[pdb_idx]),
            "contacts_outside_own_sse": int(contacts_outside_own_sse[pdb_idx]),
            "fraction_contacts_outside_own_sse": round(float(fraction_contacts_outside_own_sse[pdb_idx]), 4),
            "degree": float(degree_arr[pdb_idx]),
            "betweenness": round(float(betweenness_arr[pdb_idx]), 6),
            "closeness": round(float(closeness_arr[pdb_idx]), 4),
            "eigenvector": round(float(eigenvector_arr[pdb_idx]), 6),
            "core_number": float(core_number_arr[pdb_idx]),
            "clustering_coeff": round(float(clustering_arr[pdb_idx]), 4),
            "bridge_score": round(float(bridge_score_arr[pdb_idx]), 6),
        }

    return features


# ---------------------------------------------------------------------------
# Hydrophobic and SSE features (from v2)
# ---------------------------------------------------------------------------

def compute_hydrophobic_features(sequence: str) -> list[dict]:
    n = len(sequence)
    results = []
    for i in range(n):
        aa = sequence[i]
        self_hydro = KD.get(aa, 0.0)

        def window_mean(radius):
            vals = []
            for d in range(-radius, radius + 1):
                j = i + d
                if 0 <= j < n:
                    vals.append(KD.get(sequence[j], 0.0))
            return sum(vals) / len(vals) if vals else 0.0

        local_hydro_w5 = window_mean(2)

        same_face_vals = [KD.get(sequence[i], 0.0)]
        if i - 2 >= 0:
            same_face_vals.append(KD.get(sequence[i - 2], 0.0))
        if i + 2 < n:
            same_face_vals.append(KD.get(sequence[i + 2], 0.0))
        same_face_hydro = sum(same_face_vals) / len(same_face_vals)

        results.append({
            "self_hydro": round(self_hydro, 3),
            "local_hydro_w5": round(local_hydro_w5, 3),
            "same_face_hydro": round(same_face_hydro, 3),
        })
    return results


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
# Model loading, search direction, projection scores (from v2)
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
# OLS (from v2)
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
    adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - k) if n > k else 0.0
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
# Assemble per-protein data (v3: includes all new features)
# ---------------------------------------------------------------------------

V3_PDB_FEATURES = [
    "rsa", "contacts_8A", "contacts_10A", "long_range_contacts",
    "long_range_fraction", "mean_contact_span", "max_contact_span",
    "n_contact_bins", "contact_bin_entropy",
    "n_distinct_sse_partners", "contacts_outside_own_sse", "fraction_contacts_outside_own_sse",
    "degree", "betweenness", "closeness", "eigenvector", "core_number",
    "clustering_coeff", "bridge_score",
]


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

    rows = []
    for j in range(n):
        if j >= len(proj_scores_full):
            break
        aa = sequence[j]
        sse_f = sse_features[j] if j < len(sse_features) else {"sse": "C", "seg_len": 1, "dist_to_boundary": 0, "is_boundary": 1}
        cons_val = conservation.get(j, np.nan) if conservation else np.nan

        pdb_f = pdb_features.get(j, {}) if pdb_features else {}
        hf = hydro_features[j]

        row = {
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
            "self_hydro": hf["self_hydro"],
            "local_hydro_w5": hf["local_hydro_w5"],
            "same_face_hydro": hf["same_face_hydro"],
        }
        for feat in V3_PDB_FEATURES:
            row[feat] = pdb_f.get(feat, np.nan)
        rows.append(row)
    return rows


def add_within_protein_ranks(all_rows: list[dict]) -> None:
    """Add within-protein percentile ranks for key features (Feature 9)."""
    rank_features = ["rsa", "contacts_8A", "long_range_contacts", "betweenness", "n_distinct_sse_partners"]
    proteins = sorted(set(r["protein"] for r in all_rows))
    for protein in proteins:
        prows = [r for r in all_rows if r["protein"] == protein]
        for feat in rank_features:
            vals = np.array([r[feat] for r in prows])
            valid = ~np.isnan(vals)
            ranks = np.full(len(vals), np.nan)
            if valid.sum() > 0:
                from scipy.stats import rankdata
                ranks[valid] = rankdata(vals[valid]) / valid.sum()
            for i, r in enumerate(prows):
                r[f"rank_{feat}"] = float(ranks[i])


# ---------------------------------------------------------------------------
# Anchor labeling (Target A, B, C)
# ---------------------------------------------------------------------------

def add_anchor_labels(all_rows: list[dict], k: int = TOP_K_ANCHORS) -> None:
    """Add top-k anchor and top-1 main-anchor labels per protein."""
    proteins = sorted(set(r["protein"] for r in all_rows))
    for protein in proteins:
        prows = [r for r in all_rows if r["protein"] == protein]
        scores = [(r["proj_full"], r["pos"], r) for r in prows]
        scores.sort(key=lambda x: x[0], reverse=True)
        for rank_idx, (score, pos, r) in enumerate(scores):
            r["is_top_k_anchor"] = 1 if rank_idx < k else 0
            r["is_main_anchor"] = 1 if rank_idx == 0 else 0


# ---------------------------------------------------------------------------
# Matched-control design
# ---------------------------------------------------------------------------

def build_matched_controls(all_rows: list[dict], m: int = 10) -> list[dict]:
    """For each anchor residue, find m matched non-anchor controls from same protein.

    Matching criteria: same SSE coarse type, |delta RSA| <= tolerance, |delta contacts_8A| <= tolerance.
    Returns list of dicts with anchor info and matched control rows.
    """
    matches = []
    proteins = sorted(set(r["protein"] for r in all_rows))

    for protein in proteins:
        prows = [r for r in all_rows if r["protein"] == protein]
        anchors = [r for r in prows if r["is_top_k_anchor"] == 1 and not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]
        non_anchors = [r for r in prows if r["is_top_k_anchor"] == 0 and not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]

        for anchor in anchors:
            a_sse = anchor["sse"]
            a_rsa = anchor["rsa"]
            a_c8 = anchor["contacts_8A"]

            # Try progressively relaxed tolerances
            for rsa_tol, c8_tol in [(0.05, 3), (0.08, 3), (0.08, 5), (0.12, 5), (0.15, 8)]:
                candidates = [r for r in non_anchors
                              if r["sse"] == a_sse
                              and abs(r["rsa"] - a_rsa) <= rsa_tol
                              and abs(r["contacts_8A"] - a_c8) <= c8_tol]
                if len(candidates) >= m:
                    break

            if len(candidates) == 0:
                continue

            # Sample m controls (or take all if fewer)
            rng = np.random.RandomState(hash(f"{protein}_{anchor['pos']}") % (2**31))
            if len(candidates) >= m:
                selected = [candidates[i] for i in rng.choice(len(candidates), m, replace=False)]
            else:
                selected = candidates

            matches.append({
                "protein": protein,
                "anchor_pos": anchor["pos"],
                "anchor_row": anchor,
                "controls": selected,
                "n_controls": len(selected),
            })

    return matches


# ---------------------------------------------------------------------------
# Feature matrix builders for v3 OLS models
# ---------------------------------------------------------------------------

def _base_cols(rows):
    cols, names = [], []
    cols.append(np.array([1.0 if r["sse"] == "E" else 0.0 for r in rows])); names.append("SSE_E")
    cols.append(np.array([1.0 if r["sse"] == "H" else 0.0 for r in rows])); names.append("SSE_H")
    cols.append(np.array([float(r["dist_to_boundary"]) for r in rows])); names.append("dist_to_boundary")
    cols.append(np.array([float(r["seg_len"]) for r in rows])); names.append("seg_len")
    return cols, names


def _protein_dummies(rows):
    proteins = sorted(set(r["protein"] for r in rows))
    cols, names = [], []
    for p in proteins[1:]:
        cols.append(np.array([1.0 if r["protein"] == p else 0.0 for r in rows])); names.append(f"protein_{p}")
    return cols, names


def build_model_A(rows):
    """Model A: v2-style structural baseline."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float)); names.append("contacts_8A")
    cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float)); names.append("long_range_contacts")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_B(rows):
    """Model B: A + integrative connectivity."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float)); names.append("contacts_8A")
    cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float)); names.append("long_range_contacts")
    # Integrative connectivity
    cols.append(np.array([r["long_range_fraction"] for r in rows], dtype=float)); names.append("long_range_fraction")
    cols.append(np.array([r["mean_contact_span"] for r in rows], dtype=float)); names.append("mean_contact_span")
    cols.append(np.array([r["max_contact_span"] for r in rows], dtype=float)); names.append("max_contact_span")
    cols.append(np.array([r["n_contact_bins"] for r in rows], dtype=float)); names.append("n_contact_bins")
    cols.append(np.array([r["contact_bin_entropy"] for r in rows], dtype=float)); names.append("contact_bin_entropy")
    cols.append(np.array([r["n_distinct_sse_partners"] for r in rows], dtype=float)); names.append("n_distinct_sse_partners")
    cols.append(np.array([r["contacts_outside_own_sse"] for r in rows], dtype=float)); names.append("contacts_outside_own_sse")
    cols.append(np.array([r["fraction_contacts_outside_own_sse"] for r in rows], dtype=float)); names.append("fraction_contacts_outside_own_sse")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_C(rows):
    """Model C: B + graph features."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float)); names.append("contacts_8A")
    cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float)); names.append("long_range_contacts")
    # Integrative
    cols.append(np.array([r["long_range_fraction"] for r in rows], dtype=float)); names.append("long_range_fraction")
    cols.append(np.array([r["mean_contact_span"] for r in rows], dtype=float)); names.append("mean_contact_span")
    cols.append(np.array([r["max_contact_span"] for r in rows], dtype=float)); names.append("max_contact_span")
    cols.append(np.array([r["n_contact_bins"] for r in rows], dtype=float)); names.append("n_contact_bins")
    cols.append(np.array([r["contact_bin_entropy"] for r in rows], dtype=float)); names.append("contact_bin_entropy")
    cols.append(np.array([r["n_distinct_sse_partners"] for r in rows], dtype=float)); names.append("n_distinct_sse_partners")
    cols.append(np.array([r["contacts_outside_own_sse"] for r in rows], dtype=float)); names.append("contacts_outside_own_sse")
    cols.append(np.array([r["fraction_contacts_outside_own_sse"] for r in rows], dtype=float)); names.append("fraction_contacts_outside_own_sse")
    # Graph
    cols.append(np.array([r["degree"] for r in rows], dtype=float)); names.append("degree")
    cols.append(np.array([r["betweenness"] for r in rows], dtype=float)); names.append("betweenness")
    cols.append(np.array([r["closeness"] for r in rows], dtype=float)); names.append("closeness")
    cols.append(np.array([r["eigenvector"] for r in rows], dtype=float)); names.append("eigenvector")
    cols.append(np.array([r["core_number"] for r in rows], dtype=float)); names.append("core_number")
    cols.append(np.array([r["clustering_coeff"] for r in rows], dtype=float)); names.append("clustering_coeff")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


def build_model_D(rows):
    """Model D: C + conservation (subset)."""
    y = np.array([r["proj_full"] for r in rows], dtype=float)
    cols, names = _base_cols(rows)
    cols.append(np.array([r["rsa"] for r in rows], dtype=float)); names.append("RSA")
    cols.append(np.array([r["contacts_8A"] for r in rows], dtype=float)); names.append("contacts_8A")
    cols.append(np.array([r["long_range_contacts"] for r in rows], dtype=float)); names.append("long_range_contacts")
    cols.append(np.array([r["long_range_fraction"] for r in rows], dtype=float)); names.append("long_range_fraction")
    cols.append(np.array([r["mean_contact_span"] for r in rows], dtype=float)); names.append("mean_contact_span")
    cols.append(np.array([r["max_contact_span"] for r in rows], dtype=float)); names.append("max_contact_span")
    cols.append(np.array([r["n_contact_bins"] for r in rows], dtype=float)); names.append("n_contact_bins")
    cols.append(np.array([r["contact_bin_entropy"] for r in rows], dtype=float)); names.append("contact_bin_entropy")
    cols.append(np.array([r["n_distinct_sse_partners"] for r in rows], dtype=float)); names.append("n_distinct_sse_partners")
    cols.append(np.array([r["contacts_outside_own_sse"] for r in rows], dtype=float)); names.append("contacts_outside_own_sse")
    cols.append(np.array([r["fraction_contacts_outside_own_sse"] for r in rows], dtype=float)); names.append("fraction_contacts_outside_own_sse")
    cols.append(np.array([r["degree"] for r in rows], dtype=float)); names.append("degree")
    cols.append(np.array([r["betweenness"] for r in rows], dtype=float)); names.append("betweenness")
    cols.append(np.array([r["closeness"] for r in rows], dtype=float)); names.append("closeness")
    cols.append(np.array([r["eigenvector"] for r in rows], dtype=float)); names.append("eigenvector")
    cols.append(np.array([r["core_number"] for r in rows], dtype=float)); names.append("core_number")
    cols.append(np.array([r["clustering_coeff"] for r in rows], dtype=float)); names.append("clustering_coeff")
    cols.append(np.array([r["conservation"] for r in rows], dtype=float)); names.append("conservation")
    pc, pn = _protein_dummies(rows); cols.extend(pc); names.extend(pn)
    return np.column_stack(cols), names, y


# ---------------------------------------------------------------------------
# Analysis 2: matched anchor-vs-control comparisons
# ---------------------------------------------------------------------------

def run_matched_comparisons(matched_sets: list[dict]) -> dict:
    """For each feature, compute paired anchor - mean(controls) differences and test significance."""
    test_features = [
        "long_range_fraction", "n_contact_bins", "contact_bin_entropy",
        "n_distinct_sse_partners", "contacts_outside_own_sse",
        "betweenness", "clustering_coeff", "bridge_score",
        "mean_contact_span", "max_contact_span", "degree", "closeness",
    ]

    results = {}
    for feat in test_features:
        diffs = []
        anchor_vals = []
        control_means = []
        for ms in matched_sets:
            a_val = ms["anchor_row"][feat]
            c_vals = [c[feat] for c in ms["controls"] if not np.isnan(c[feat])]
            if np.isnan(a_val) or len(c_vals) == 0:
                continue
            c_mean = np.mean(c_vals)
            diffs.append(a_val - c_mean)
            anchor_vals.append(a_val)
            control_means.append(c_mean)

        if len(diffs) < 3:
            results[feat] = {"n": len(diffs), "note": "too few pairs"}
            continue

        diffs_arr = np.array(diffs)
        mean_diff = float(np.mean(diffs_arr))
        std_diff = float(np.std(diffs_arr, ddof=1))

        # Paired t-test
        t_stat, t_pval = stats.ttest_1samp(diffs_arr, 0)

        # Wilcoxon signed-rank (more robust)
        try:
            w_stat, w_pval = stats.wilcoxon(diffs_arr, alternative="two-sided")
        except ValueError:
            w_stat, w_pval = np.nan, np.nan

        # Effect size: Cohen's d
        cohens_d = mean_diff / std_diff if std_diff > 0 else 0.0

        results[feat] = {
            "n": len(diffs),
            "mean_diff": mean_diff,
            "std_diff": std_diff,
            "cohens_d": cohens_d,
            "t_stat": float(t_stat),
            "t_pval": float(t_pval),
            "w_stat": float(w_stat) if not np.isnan(w_stat) else None,
            "w_pval": float(w_pval) if not np.isnan(w_pval) else None,
            "anchor_vals": anchor_vals,
            "control_means": control_means,
        }

    return results


# ---------------------------------------------------------------------------
# Analysis 3: leave-one-protein-out classification
# ---------------------------------------------------------------------------

def run_lopo_classification(all_rows: list[dict]) -> dict:
    """Leave-one-protein-out cross-validation for anchor classification."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import roc_auc_score, average_precision_score
    from sklearn.preprocessing import StandardScaler

    work_rows = [r for r in all_rows if not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]
    proteins = sorted(set(r["protein"] for r in work_rows))
    if len(proteins) < 3:
        return {"note": "too few proteins for LOPO"}

    # Feature sets
    feat_sets = {
        "A_baseline": ["rsa", "contacts_8A", "long_range_contacts", "SSE_E", "SSE_H"],
        "B_integrative": ["rsa", "contacts_8A", "long_range_contacts", "SSE_E", "SSE_H",
                          "long_range_fraction", "mean_contact_span", "max_contact_span",
                          "n_contact_bins", "contact_bin_entropy",
                          "n_distinct_sse_partners", "contacts_outside_own_sse"],
        "C_graph": ["rsa", "contacts_8A", "long_range_contacts", "SSE_E", "SSE_H",
                     "long_range_fraction", "mean_contact_span", "max_contact_span",
                     "n_contact_bins", "contact_bin_entropy",
                     "n_distinct_sse_partners", "contacts_outside_own_sse",
                     "degree", "betweenness", "closeness", "eigenvector",
                     "core_number", "clustering_coeff"],
    }

    def extract_features(rows, feat_names):
        X = []
        for r in rows:
            feats = []
            for f in feat_names:
                if f == "SSE_E":
                    feats.append(1.0 if r["sse"] == "E" else 0.0)
                elif f == "SSE_H":
                    feats.append(1.0 if r["sse"] == "H" else 0.0)
                else:
                    feats.append(float(r[f]))
            X.append(feats)
        return np.array(X)

    results = {}
    for fs_name, feat_names in feat_sets.items():
        aurocs_lr = []
        auprcs_lr = []
        aurocs_rf = []
        auprcs_rf = []
        top_k_hits_lr = []
        top_k_hits_rf = []

        for held_out in proteins:
            train_rows = [r for r in work_rows if r["protein"] != held_out]
            test_rows = [r for r in work_rows if r["protein"] == held_out]
            if len(test_rows) == 0:
                continue

            X_train = extract_features(train_rows, feat_names)
            y_train = np.array([r["is_top_k_anchor"] for r in train_rows])
            X_test = extract_features(test_rows, feat_names)
            y_test = np.array([r["is_top_k_anchor"] for r in test_rows])

            if y_test.sum() == 0 or y_test.sum() == len(y_test):
                continue
            if y_train.sum() == 0:
                continue

            scaler = StandardScaler()
            X_train_s = scaler.fit_transform(X_train)
            X_test_s = scaler.transform(X_test)

            # Logistic regression
            lr = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
            lr.fit(X_train_s, y_train)
            lr_probs = lr.predict_proba(X_test_s)[:, 1]
            aurocs_lr.append(roc_auc_score(y_test, lr_probs))
            auprcs_lr.append(average_precision_score(y_test, lr_probs))
            # Top-k retrieval: do top-k predicted residues contain any actual anchor?
            top_k_idx = np.argsort(lr_probs)[-TOP_K_ANCHORS:]
            top_k_hits_lr.append(int(y_test[top_k_idx].sum() > 0))

            # Random forest
            rf = RandomForestClassifier(n_estimators=100, max_depth=8, class_weight="balanced", random_state=42)
            rf.fit(X_train_s, y_train)
            rf_probs = rf.predict_proba(X_test_s)[:, 1]
            aurocs_rf.append(roc_auc_score(y_test, rf_probs))
            auprcs_rf.append(average_precision_score(y_test, rf_probs))
            top_k_idx = np.argsort(rf_probs)[-TOP_K_ANCHORS:]
            top_k_hits_rf.append(int(y_test[top_k_idx].sum() > 0))

        results[fs_name] = {
            "lr_auroc": float(np.mean(aurocs_lr)) if aurocs_lr else np.nan,
            "lr_auprc": float(np.mean(auprcs_lr)) if auprcs_lr else np.nan,
            "lr_top_k_acc": float(np.mean(top_k_hits_lr)) if top_k_hits_lr else np.nan,
            "rf_auroc": float(np.mean(aurocs_rf)) if aurocs_rf else np.nan,
            "rf_auprc": float(np.mean(auprcs_rf)) if auprcs_rf else np.nan,
            "rf_top_k_acc": float(np.mean(top_k_hits_rf)) if top_k_hits_rf else np.nan,
            "n_folds": len(aurocs_lr),
        }

    return results


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_A_effect_sizes(matched_results: dict, output_dir: Path) -> None:
    """Plot A: horizontal bar chart of anchor vs matched-control effect sizes."""
    feats = []
    effects = []
    pvals = []
    for feat, res in sorted(matched_results.items(), key=lambda x: abs(x[1].get("cohens_d", 0)), reverse=True):
        if "cohens_d" not in res:
            continue
        feats.append(feat)
        effects.append(res["cohens_d"])
        pvals.append(res.get("t_pval", 1.0))

    if not feats:
        print("  Plot A skipped: no matched comparison results")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ["#e06c75" if p < 0.05 else "#98c379" if p < 0.10 else "#abb2bf" for p in pvals]
    y_pos = range(len(feats))
    ax.barh(y_pos, effects, color=colors)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(feats, fontsize=8)
    ax.invert_yaxis()
    ax.axvline(0, color="black", lw=0.5)
    ax.set_xlabel("Cohen's d (anchor - matched controls)")
    ax.set_title("Anchor vs matched-control effect sizes")

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor="#e06c75", label="p < 0.05"),
                       Patch(facecolor="#98c379", label="p < 0.10"),
                       Patch(facecolor="#abb2bf", label="p >= 0.10")]
    ax.legend(handles=legend_elements, fontsize=7, loc="lower right")

    plt.tight_layout()
    out = output_dir / "anchor_regression_v3_A_effect_sizes.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_B_proj_vs_features(all_rows: list[dict], output_dir: Path) -> None:
    """Plot B: scatter of projection vs n_distinct_sse_partners, contact_bin_entropy, betweenness."""
    rows = [r for r in all_rows if not np.isnan(r["betweenness"])]
    if not rows:
        print("  Plot B skipped: no graph data")
        return

    feat_pairs = [
        ("n_distinct_sse_partners", "Distinct SSE partners"),
        ("contact_bin_entropy", "Contact bin entropy"),
        ("betweenness", "Betweenness centrality"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, (feat, label) in zip(axes, feat_pairs):
        xs = [r[feat] for r in rows]
        ys = [r["proj_full"] for r in rows]
        sse_labels = [r["sse"] for r in rows]

        for s in ["H", "E", "C"]:
            idx = [i for i, sl in enumerate(sse_labels) if sl == s]
            if idx:
                ax.scatter([xs[i] for i in idx], [ys[i] for i in idx],
                           color=SSE_COLORS[s], alpha=0.15, s=6, label=s)

        anchors = [(r[feat], r["proj_full"]) for r in rows if r["is_top_k_anchor"] == 1]
        if anchors:
            ax.scatter([a[0] for a in anchors], [a[1] for a in anchors],
                       color="black", marker="*", s=100, zorder=5, label="anchor (top-k)")

        corr = float(np.corrcoef([r[feat] for r in rows], [r["proj_full"] for r in rows])[0, 1])
        ax.text(0.02, 0.98, f"r = {corr:.3f}", transform=ax.transAxes, va="top", fontsize=9)
        ax.set_xlabel(label)
        ax.set_ylabel("Projection score")
        ax.legend(fontsize=6, markerscale=0.7)

    plt.tight_layout()
    out = output_dir / "anchor_regression_v3_B_proj_vs_features.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_C_sequence_profiles(all_rows: list[dict], output_dir: Path) -> None:
    """Plot C: per-protein sequence profile with projection and long_range_fraction or n_distinct_sse_partners."""
    proteins = sorted(set(r["protein"] for r in all_rows))
    proteins_with_data = [p for p in proteins if any(not np.isnan(r["betweenness"]) for r in all_rows if r["protein"] == p)]
    if not proteins_with_data:
        print("  Plot C skipped: no data")
        return
    show = proteins_with_data[:5]
    fig, axes = plt.subplots(len(show), 1, figsize=(16, 3.5 * len(show)), squeeze=False)
    for i, protein in enumerate(show):
        ax = axes[i, 0]
        prows = sorted([r for r in all_rows if r["protein"] == protein], key=lambda r: r["pos"])
        positions = [r["pos"] for r in prows]
        scores = [r["proj_full"] for r in prows]
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

        # Overlay: n_distinct_sse_partners
        ax2 = ax.twinx()
        sse_partner_vals = [(r["pos"], r["n_distinct_sse_partners"]) for r in prows if not np.isnan(r.get("n_distinct_sse_partners", np.nan))]
        if sse_partner_vals:
            ax2.plot([p for p, v in sse_partner_vals], [v for p, v in sse_partner_vals],
                     color="#9b59b6", lw=0.6, alpha=0.6, label="SSE partners")
            ax2.set_ylabel("SSE partners", color="#9b59b6")

        # Mark anchors
        for r in prows:
            if r["is_top_k_anchor"] == 1:
                ax.scatter([r["pos"]], [r["proj_full"]], color="red", s=60, zorder=6)
            if r["is_main_anchor"] == 1:
                ax.scatter([r["pos"]], [r["proj_full"]], color="red", s=120, zorder=7, marker="*")

        ax.set_title(protein, fontsize=9)
        ax.set_xlabel("Residue position")
        ax.set_ylabel("Projection score")

    plt.tight_layout()
    out = output_dir / "anchor_regression_v3_C_sequence_profiles.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_D_matched_lines(matched_sets: list[dict], output_dir: Path) -> None:
    """Plot D: connected lines showing anchor vs matched controls for key features."""
    if not matched_sets:
        print("  Plot D skipped: no matched sets")
        return

    feats = ["betweenness", "n_distinct_sse_partners", "contact_bin_entropy"]
    feat_labels = ["Betweenness", "SSE partners", "Contact entropy"]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, feat, label in zip(axes, feats, feat_labels):
        for ms in matched_sets:
            a_val = ms["anchor_row"][feat]
            if np.isnan(a_val):
                continue
            c_vals = [c[feat] for c in ms["controls"] if not np.isnan(c[feat])]
            if not c_vals:
                continue
            c_mean = np.mean(c_vals)
            ax.plot([0, 1], [c_mean, a_val], color="#61afef", alpha=0.4, lw=1)
            ax.scatter([0], [c_mean], color="#61afef", s=30, zorder=3)
            ax.scatter([1], [a_val], color="#e06c75", s=30, zorder=3)

        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Matched\ncontrols", "Anchor"])
        ax.set_ylabel(label)
        ax.set_title(f"{label}: anchor vs controls")

    plt.tight_layout()
    out = output_dir / "anchor_regression_v3_D_matched_lines.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_E_classifier_performance(clf_results: dict, output_dir: Path) -> None:
    """Plot E: LOPO classifier performance bar chart."""
    if "note" in clf_results:
        print(f"  Plot E skipped: {clf_results['note']}")
        return

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    feat_set_names = list(clf_results.keys())
    feat_set_labels = ["A: Baseline", "B: +Integrative", "C: +Graph"]

    # AUROC
    ax = axes[0]
    lr_vals = [clf_results[fs]["lr_auroc"] for fs in feat_set_names]
    rf_vals = [clf_results[fs]["rf_auroc"] for fs in feat_set_names]
    x = np.arange(len(feat_set_names))
    ax.bar(x - 0.15, lr_vals, 0.3, label="LogReg", color="#61afef")
    ax.bar(x + 0.15, rf_vals, 0.3, label="RF", color="#e06c75")
    ax.set_xticks(x)
    ax.set_xticklabels(feat_set_labels, fontsize=8)
    ax.set_ylabel("AUROC")
    ax.set_title("AUROC (LOPO CV)")
    ax.legend(fontsize=7)
    ax.set_ylim(0.4, 1.0)
    ax.axhline(0.5, color="gray", ls="--", lw=0.5)

    # AUPRC
    ax = axes[1]
    lr_vals = [clf_results[fs]["lr_auprc"] for fs in feat_set_names]
    rf_vals = [clf_results[fs]["rf_auprc"] for fs in feat_set_names]
    ax.bar(x - 0.15, lr_vals, 0.3, label="LogReg", color="#61afef")
    ax.bar(x + 0.15, rf_vals, 0.3, label="RF", color="#e06c75")
    ax.set_xticks(x)
    ax.set_xticklabels(feat_set_labels, fontsize=8)
    ax.set_ylabel("AUPRC")
    ax.set_title("AUPRC (LOPO CV)")
    ax.legend(fontsize=7)

    # Top-k retrieval
    ax = axes[2]
    lr_vals = [clf_results[fs]["lr_top_k_acc"] for fs in feat_set_names]
    rf_vals = [clf_results[fs]["rf_top_k_acc"] for fs in feat_set_names]
    ax.bar(x - 0.15, lr_vals, 0.3, label="LogReg", color="#61afef")
    ax.bar(x + 0.15, rf_vals, 0.3, label="RF", color="#e06c75")
    ax.set_xticks(x)
    ax.set_xticklabels(feat_set_labels, fontsize=8)
    ax.set_ylabel("Top-k retrieval accuracy")
    ax.set_title(f"Top-{TOP_K_ANCHORS} retrieval (LOPO CV)")
    ax.legend(fontsize=7)
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    out = output_dir / "anchor_regression_v3_E_classifier_performance.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def write_report(
    all_rows, anchor_rows, pdb_coverage,
    res_A, res_B, res_C, res_D,
    matched_sets, matched_results,
    clf_results,
    output_dir: Path,
):
    report = []
    n_total = len(all_rows)
    rows_with_all = [r for r in all_rows if not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]

    report.append("# Anchor Feature Regression with Matched Controls (v3)\n\n")
    report.append(f"Search direction: L10H9 key-side W_K^T @ q_mean from {REFERENCE_PROTEIN} clean masked sequence.\n")
    report.append(f"Total residues: {n_total} across {len(ANCHOR_POSITIONS)} proteins.\n")
    report.append(f"Residues with PDB features: {len(rows_with_all)} ({pdb_coverage['with_pdb']} proteins).\n")
    report.append(f"Anchor label: top-{TOP_K_ANCHORS} residues per protein by projection score.\n\n")

    # Anchor summary
    report.append("## Anchor feature summary (top-1 per protein)\n\n")
    report.append("| Protein | Pos | AA | SSE | Proj | RSA | C8A | LR | SSE-part | Between | Clust |\n")
    report.append("|---------|-----|-----|-----|------|-----|-----|-----|----------|---------|-------|\n")
    for r in anchor_rows:
        def fmt(val, dp=3):
            return f"{val:.{dp}f}" if not np.isnan(val) else "-"
        report.append(f"| {r['protein']} | {r['pos']} | {r['aa']} | {r['sse']} | {fmt(r['proj_full'])} | {fmt(r['rsa'])} | {fmt(r['contacts_8A'], 0)} | {fmt(r['long_range_contacts'], 0)} | {fmt(r['n_distinct_sse_partners'], 0)} | {fmt(r['betweenness'], 4)} | {fmt(r['clustering_coeff'])} |\n")
    report.append("\n")

    # Analysis 1: OLS
    report.append("## Analysis 1: full-residue regression\n\n")
    report.append("| Model | Description | N | R2 | adj-R2 |\n")
    report.append("|-------|-------------|---|-----|--------|\n")
    report.append(f"| A | SSE + RSA + contacts + protein FE | {res_A['n']} | {res_A['r2']:.4f} | {res_A['adj_r2']:.4f} |\n")
    report.append(f"| B | A + integrative connectivity | {res_B['n']} | {res_B['r2']:.4f} | {res_B['adj_r2']:.4f} |\n")
    report.append(f"| C | B + graph features | {res_C['n']} | {res_C['r2']:.4f} | {res_C['adj_r2']:.4f} |\n")
    if res_D is not None:
        report.append(f"| D | C + conservation | {res_D['n']} | {res_D['r2']:.4f} | {res_D['adj_r2']:.4f} |\n")
    report.append("\n")

    # Anchor residuals under Model C
    report.append("### Anchor residuals under Model C\n\n")
    residual_std = float(np.std(res_C["residuals"]))
    report.append(f"Model C residual std: {residual_std:.4f}\n\n")
    report.append("| Protein | Pos | Actual | Predicted | Residual | Z |\n")
    report.append("|---------|-----|--------|-----------|----------|---|\n")
    for r in anchor_rows:
        idx = next((i for i, row in enumerate(rows_with_all) if row["protein"] == r["protein"] and row["pos"] == r["pos"]), None)
        if idx is None:
            report.append(f"| {r['protein']} | {r['pos']} | {r['proj_full']:.3f} | - | - | - |\n")
            continue
        resid = res_C["residuals"][idx]
        yhat = res_C["y_hat"][idx]
        z = resid / residual_std
        report.append(f"| {r['protein']} | {r['pos']} | {r['proj_full']:.3f} | {yhat:.3f} | {resid:.3f} | {z:.2f} |\n")
    report.append("\n")

    # Model C coefficients
    report.append("### Model C (full) OLS coefficients\n\n")
    report.extend(format_ols_table(res_C))
    report.append("\n")

    # Analysis 2: matched comparisons
    report.append("## Analysis 2: matched anchor-vs-control comparisons\n\n")
    report.append(f"Total matched sets: {len(matched_sets)}\n\n")
    if matched_sets:
        mean_controls = np.mean([ms["n_controls"] for ms in matched_sets])
        report.append(f"Mean controls per anchor: {mean_controls:.1f}\n\n")
    report.append("| Feature | N pairs | Mean diff | Cohen's d | t-test p | Wilcoxon p |\n")
    report.append("|---------|---------|-----------|-----------|----------|------------|\n")
    for feat in sorted(matched_results.keys(), key=lambda f: abs(matched_results[f].get("cohens_d", 0)), reverse=True):
        res = matched_results[feat]
        if "cohens_d" not in res:
            report.append(f"| {feat} | {res['n']} | - | - | - | - |\n")
            continue
        star = "**" if res["t_pval"] < 0.01 else ("*" if res["t_pval"] < 0.05 else "")
        w_str = f"{res['w_pval']:.4f}" if res["w_pval"] is not None else "-"
        report.append(f"| {feat} | {res['n']} | {res['mean_diff']:.4f} | {res['cohens_d']:.3f} | {res['t_pval']:.4f}{star} | {w_str} |\n")
    report.append("\n")

    # Analysis 3: classification
    report.append("## Analysis 3: leave-one-protein-out classification\n\n")
    if "note" in clf_results:
        report.append(f"{clf_results['note']}\n\n")
    else:
        report.append("| Feature set | LR AUROC | LR AUPRC | LR top-k | RF AUROC | RF AUPRC | RF top-k | N folds |\n")
        report.append("|-------------|----------|----------|----------|----------|----------|----------|---------|\n")
        labels = {"A_baseline": "A: baseline", "B_integrative": "B: +integrative", "C_graph": "C: +graph"}
        for fs_name, res in clf_results.items():
            label = labels.get(fs_name, fs_name)
            report.append(f"| {label} | {res['lr_auroc']:.3f} | {res['lr_auprc']:.3f} | {res['lr_top_k_acc']:.3f} | {res['rf_auroc']:.3f} | {res['rf_auprc']:.3f} | {res['rf_top_k_acc']:.3f} | {res['n_folds']} |\n")
    report.append("\n")

    out_path = output_dir / "anchor_regression_v3.md"
    with open(out_path, "w") as f:
        f.writelines(report)
    print(f"  Saved: {out_path}")


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

        pdb_features = compute_pdb_features_v3(protein, sequence, sse_str)
        if pdb_features is None:
            print(f"    No PDB features")
            pdb_coverage["without_pdb"] += 1
        else:
            n_mapped = len(pdb_features)
            print(f"    PDB features (v3): {n_mapped}/{len(sequence)} positions mapped")
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

    # Add within-protein ranks and anchor labels
    print("\nAdding within-protein ranks and anchor labels...")
    add_within_protein_ranks(all_rows)
    add_anchor_labels(all_rows, k=TOP_K_ANCHORS)

    # Filter subsets
    rows_with_all = [r for r in all_rows if not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]
    rows_with_cons_and_pdb = [r for r in rows_with_all if not np.isnan(r["conservation"])]
    print(f"Rows with all structural features: {len(rows_with_all)}")
    print(f"Rows with conservation + PDB: {len(rows_with_cons_and_pdb)}")

    # Anchor summary
    anchor_rows = [r for r in all_rows if r["is_anchor"]]
    print(f"\nAnchor residues (original top-1): {len(anchor_rows)}")
    top_k_anchors = [r for r in all_rows if r["is_top_k_anchor"] == 1]
    print(f"Top-{TOP_K_ANCHORS} anchors: {len(top_k_anchors)}")

    # ---------------------------------------------------------------------------
    # Analysis 1: OLS regressions
    # ---------------------------------------------------------------------------
    print("\nAnalysis 1: OLS regressions...")
    work_rows = rows_with_all

    XA, nA, yA = build_model_A(work_rows)
    res_A = run_ols(XA, yA, nA)
    print(f"  Model A (structural baseline):     R2={res_A['r2']:.4f}, adj-R2={res_A['adj_r2']:.4f}, N={res_A['n']}")

    XB, nB, yB = build_model_B(work_rows)
    res_B = run_ols(XB, yB, nB)
    print(f"  Model B (+ integrative):           R2={res_B['r2']:.4f}, adj-R2={res_B['adj_r2']:.4f}")

    XC, nC, yC = build_model_C(work_rows)
    res_C = run_ols(XC, yC, nC)
    print(f"  Model C (+ graph):                 R2={res_C['r2']:.4f}, adj-R2={res_C['adj_r2']:.4f}")

    res_D = None
    if rows_with_cons_and_pdb:
        XD, nD, yD = build_model_D(rows_with_cons_and_pdb)
        res_D = run_ols(XD, yD, nD)
        print(f"  Model D (+ conservation, {len(rows_with_cons_and_pdb)} rows): R2={res_D['r2']:.4f}, adj-R2={res_D['adj_r2']:.4f}")
    else:
        print("  Model D skipped: no rows with conservation + PDB")

    # ---------------------------------------------------------------------------
    # Analysis 2: matched controls
    # ---------------------------------------------------------------------------
    print("\nAnalysis 2: building matched controls...")
    matched_sets = build_matched_controls(all_rows, m=10)
    print(f"  Total matched sets: {len(matched_sets)}")
    if matched_sets:
        n_controls_list = [ms["n_controls"] for ms in matched_sets]
        print(f"  Controls per anchor: mean={np.mean(n_controls_list):.1f}, min={min(n_controls_list)}, max={max(n_controls_list)}")

    print("  Running paired comparisons...")
    matched_results = run_matched_comparisons(matched_sets)
    for feat in sorted(matched_results.keys(), key=lambda f: abs(matched_results[f].get("cohens_d", 0)), reverse=True):
        res = matched_results[feat]
        if "cohens_d" in res:
            star = "**" if res["t_pval"] < 0.01 else ("*" if res["t_pval"] < 0.05 else "")
            print(f"    {feat}: d={res['cohens_d']:.3f}, p={res['t_pval']:.4f}{star} (n={res['n']})")

    # ---------------------------------------------------------------------------
    # Analysis 3: classification
    # ---------------------------------------------------------------------------
    print("\nAnalysis 3: LOPO classification...")
    clf_results = run_lopo_classification(all_rows)
    if "note" not in clf_results:
        for fs_name, res in clf_results.items():
            print(f"  {fs_name}: LR AUROC={res['lr_auroc']:.3f}, RF AUROC={res['rf_auroc']:.3f}, RF top-k={res['rf_top_k_acc']:.3f}")

    # ---------------------------------------------------------------------------
    # Plots
    # ---------------------------------------------------------------------------
    print("\nGenerating plots...")
    plot_A_effect_sizes(matched_results, REPORT_DIR)
    plot_B_proj_vs_features(all_rows, REPORT_DIR)
    plot_C_sequence_profiles(all_rows, REPORT_DIR)
    plot_D_matched_lines(matched_sets, REPORT_DIR)
    plot_E_classifier_performance(clf_results, REPORT_DIR)

    # ---------------------------------------------------------------------------
    # Write report
    # ---------------------------------------------------------------------------
    print("\nWriting report...")
    write_report(
        all_rows, anchor_rows, pdb_coverage,
        res_A, res_B, res_C, res_D,
        matched_sets, matched_results,
        clf_results,
        REPORT_DIR,
    )

    # ---------------------------------------------------------------------------
    # Save features CSV
    # ---------------------------------------------------------------------------
    csv_path = REPORT_DIR / "anchor_regression_v3_features.csv"
    csv_cols = ["protein", "pos", "aa", "sse", "proj_full", "is_anchor", "is_top_k_anchor", "is_main_anchor",
                "rsa", "contacts_8A", "long_range_contacts",
                "long_range_fraction", "mean_contact_span", "max_contact_span",
                "n_contact_bins", "contact_bin_entropy",
                "n_distinct_sse_partners", "contacts_outside_own_sse", "fraction_contacts_outside_own_sse",
                "degree", "betweenness", "closeness", "eigenvector", "core_number",
                "clustering_coeff", "bridge_score", "conservation"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_cols, extrasaction="ignore")
        writer.writeheader()
        for r in all_rows:
            writer.writerow(r)
    print(f"  Saved: {csv_path}")

    # Save matched sets CSV
    match_csv_path = REPORT_DIR / "anchor_regression_v3_matches.csv"
    with open(match_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["protein", "anchor_pos", "control_pos", "anchor_rsa", "control_rsa", "anchor_c8a", "control_c8a"])
        for ms in matched_sets:
            for ctrl in ms["controls"]:
                writer.writerow([ms["protein"], ms["anchor_pos"], ctrl["pos"],
                                 ms["anchor_row"]["rsa"], ctrl["rsa"],
                                 ms["anchor_row"]["contacts_8A"], ctrl["contacts_8A"]])
    print(f"  Saved: {match_csv_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
