#!/usr/bin/env python3
"""Anchor information-hub experiment (experiments/3_27_anchor_info_hub_v1.md).

Two tracks:
  Part A: EVcouplings -- aggregate pairwise coupling scores into per-residue features,
          compare anchors vs structurally matched controls.
  Part B: ESM conditional influence -- measure how much masking the anchor hurts
          prediction of distant residues, compared with matched controls.

Usage:
    uv run python scripts/anchor_information_hub_v1.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from math import log2
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

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

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}

N_CONTROLS = 5
N_TARGETS = 16
MIN_SEQ_SEP = 24
BATCH_SIZE = 16
N_SEQ_BINS = 10
COUPLING_STRONG_THRESHOLD = 1.0


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


# ---------------------------------------------------------------------------
# PDB features (from v2)
# ---------------------------------------------------------------------------

def _find_pdb(protein: str) -> Path | None:
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
    candidates = [c for c in candidates if "compare" not in str(c) and "aux" not in str(c)]
    return candidates[0] if candidates else None


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


def compute_pdb_features(protein: str, full_seq: str) -> dict | None:
    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return None
    pdb_residues_raw, structure = _parse_pdb_residues(pdb_path)
    if not pdb_residues_raw:
        return None
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues_raw]
    mapping = _align_pdb_to_seq(pdb_tuples, full_seq)
    if len(mapping) < len(pdb_residues_raw) * 0.5:
        print(f"    WARNING: poor PDB alignment for {protein}: {len(mapping)}/{len(pdb_residues_raw)} mapped")
        return None

    from Bio.PDB import ShrakeRupley
    sr = ShrakeRupley()
    sr.compute(structure[0], level="R")
    chain = list(structure[0])[0]
    sasa_by_resid = {}
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa

    cb_coords = np.array([r["cb"] for r in pdb_residues_raw])
    from scipy.spatial.distance import cdist
    dists = cdist(cb_coords, cb_coords)
    contacts_8A = (dists < 8.0).sum(axis=1) - 1
    contacts_10A = (dists < 10.0).sum(axis=1) - 1

    n_pdb = len(pdb_residues_raw)
    long_range = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) > 12 and dists[i, j] < 8.0:
                long_range[i] += 1

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
# SSE features (from v2)
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
        seg_id = i  # use start position as segment ID
        for pos in range(i, j):
            dist_left = pos - i
            dist_right = j - 1 - pos
            dist_to_boundary = min(dist_left, dist_right)
            features[pos] = {
                "sse": label,
                "seg_len": seg_len,
                "seg_id": seg_id,
                "dist_to_boundary": dist_to_boundary,
                "is_boundary": 1 if dist_to_boundary <= 1 else 0,
            }
        i = j
    return features


# ---------------------------------------------------------------------------
# Model loading and projection scores (from v2)
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
# EVcouplings loading (new)
# ---------------------------------------------------------------------------

def find_ev_coupling_csv(protein: str, longrange_only: bool = True) -> Path | None:
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    suffix = "_CouplingScores_longrange.csv" if longrange_only else "_CouplingScores.csv"
    candidates = sorted(ev_dir.glob(f"TARGET_b*/couplings/TARGET_b*{suffix}"))
    return candidates[0] if candidates else None


def load_coupling_scores(csv_path: Path) -> list[dict]:
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "i": int(row["i"]) - 1,  # convert to 0-indexed
                "j": int(row["j"]) - 1,
                "A_i": row["A_i"],
                "A_j": row["A_j"],
                "cn": float(row["cn"]),
                "score": float(row["score"]),
                "probability": float(row["probability"]),
            })
    return rows


# ---------------------------------------------------------------------------
# Coupling feature aggregation (new)
# ---------------------------------------------------------------------------

def aggregate_coupling_features(coupling_rows: list[dict], seq_len: int, sse_features: list[dict]) -> dict[int, dict]:
    partners = defaultdict(list)
    for row in coupling_rows:
        i, j = row["i"], row["j"]
        partners[i].append({"partner": j, "score": row["score"], "cn": row["cn"]})
        partners[j].append({"partner": i, "score": row["score"], "cn": row["cn"]})

    bin_size = max(1, seq_len // N_SEQ_BINS)

    features = {}
    for pos in range(seq_len):
        plist = partners.get(pos, [])
        if not plist:
            features[pos] = {
                "sum_score": 0.0, "mean_score": 0.0, "max_score": 0.0,
                "sum_cn": 0.0, "n_couplings": 0, "n_strong_pairs": 0,
                "n_longrange_pairs": 0, "sum_longrange_score": 0.0, "mean_longrange_score": 0.0,
                "n_coupling_bins": 0, "coupling_bin_entropy": 0.0,
                "n_distinct_sse_segments": 0,
            }
            continue

        scores = [p["score"] for p in plist]
        cns = [p["cn"] for p in plist]
        lr_scores = [p["score"] for p in plist if abs(pos - p["partner"]) >= MIN_SEQ_SEP]

        # Spread: which sequence bins have coupling partners
        bin_counts = defaultdict(int)
        for p in plist:
            b = min(p["partner"] // bin_size, N_SEQ_BINS - 1)
            bin_counts[b] += 1
        n_bins = len(bin_counts)
        total_partners = sum(bin_counts.values())
        entropy = 0.0
        if total_partners > 0 and n_bins > 1:
            for count in bin_counts.values():
                frac = count / total_partners
                if frac > 0:
                    entropy -= frac * log2(frac)

        # SSE segment spread
        sse_segments = set()
        for p in plist:
            partner = p["partner"]
            if 0 <= partner < len(sse_features) and sse_features[partner] is not None:
                sse_segments.add(sse_features[partner]["seg_id"])

        features[pos] = {
            "sum_score": sum(scores),
            "mean_score": sum(scores) / len(scores),
            "max_score": max(scores),
            "sum_cn": sum(cns),
            "n_couplings": len(scores),
            "n_strong_pairs": sum(1 for s in scores if s > COUPLING_STRONG_THRESHOLD),
            "n_longrange_pairs": len(lr_scores),
            "sum_longrange_score": sum(lr_scores),
            "mean_longrange_score": sum(lr_scores) / len(lr_scores) if lr_scores else 0.0,
            "n_coupling_bins": n_bins,
            "coupling_bin_entropy": entropy,
            "n_distinct_sse_segments": len(sse_segments),
        }
    return features


# ---------------------------------------------------------------------------
# Matched controls (new)
# ---------------------------------------------------------------------------

TOLERANCE_TIERS = [
    (0.05, 3),
    (0.08, 3),
    (0.08, 5),
    (0.12, 5),
    (0.15, 8),
    (0.20, 10),
]


def build_matched_controls(
    protein: str,
    anchor_pos: int,
    sequence: str,
    sse_features: list[dict],
    pdb_features: dict | None,
    proj_scores: np.ndarray,
    n_controls: int = N_CONTROLS,
) -> tuple[list[int], int]:
    """Find matched non-anchor control residues. Returns (positions, tier_used)."""
    if pdb_features is None:
        return [], -1

    anchor_sse_f = sse_features[anchor_pos]
    if anchor_sse_f is None:
        return [], -1
    anchor_sse = anchor_sse_f["sse"]
    anchor_pdb = pdb_features.get(anchor_pos)
    if anchor_pdb is None:
        return [], -1
    anchor_rsa = anchor_pdb["rsa"]
    anchor_c8 = anchor_pdb["contacts_8A"]

    proj_threshold = np.percentile(proj_scores, 90)
    n = len(sequence)
    rng = np.random.RandomState(abs(hash(f"{protein}_{anchor_pos}")) % (2**31))

    for tier_idx, (rsa_tol, c8_tol) in enumerate(TOLERANCE_TIERS):
        candidates = []
        for pos in range(n):
            if pos == anchor_pos:
                continue
            if proj_scores[pos] >= proj_threshold:
                continue
            sf = sse_features[pos]
            if sf is None or sf["sse"] != anchor_sse:
                continue
            pf = pdb_features.get(pos)
            if pf is None:
                continue
            if abs(pf["rsa"] - anchor_rsa) > rsa_tol:
                continue
            if abs(pf["contacts_8A"] - anchor_c8) > c8_tol:
                continue
            candidates.append(pos)
        if len(candidates) >= n_controls:
            chosen = rng.choice(candidates, size=n_controls, replace=False).tolist()
            return chosen, tier_idx
    # fallback: return whatever we have
    if candidates:
        return candidates[:n_controls], len(TOLERANCE_TIERS) - 1
    return [], -1


# ---------------------------------------------------------------------------
# Target selection for Part B (new)
# ---------------------------------------------------------------------------

def select_distant_targets(anchor_pos: int, seq_len: int, n_targets: int = N_TARGETS, min_sep: int = MIN_SEQ_SEP) -> list[int]:
    eligible = [j for j in range(seq_len) if abs(j - anchor_pos) >= min_sep]
    if len(eligible) <= n_targets:
        return eligible
    # stratified: divide eligible into n_targets bins, pick midpoint of each
    bin_size = len(eligible) / n_targets
    selected = []
    for i in range(n_targets):
        start = int(i * bin_size)
        end = int((i + 1) * bin_size)
        mid = (start + end) // 2
        selected.append(eligible[mid])
    return selected


# ---------------------------------------------------------------------------
# ESM conditional influence (new -- Part B core)
# ---------------------------------------------------------------------------

def compute_conditional_influence(
    esm_model,
    tokenizer,
    sequence: str,
    source_positions: list[int],
    target_positions: list[int],
    device: str,
    batch_size: int = BATCH_SIZE,
) -> dict[int, dict[int, float]]:
    """Compute influence(source -> target) for all (source, target) pairs.

    influence(i->j) = logP(true_j | mask_j) - logP(true_j | mask_i_and_j)
    Positive = source i helps predict target j.
    """
    mask_id = tokenizer.mask_token_id
    base_tokens = tokenizer(sequence, return_tensors="pt")["input_ids"][0]  # shape [L+2]

    # Step 1: single-mask logprobs (shared across sources)
    single_mask_logp = {}
    single_batch_ids = []
    for j in target_positions:
        ids = base_tokens.clone()
        ids[j + 1] = mask_id  # +1 for CLS
        single_batch_ids.append(ids)

    # Process in batches
    for batch_start in range(0, len(single_batch_ids), batch_size):
        batch_end = min(batch_start + batch_size, len(single_batch_ids))
        batch = torch.stack(single_batch_ids[batch_start:batch_end]).to(device)
        with torch.no_grad():
            logits = esm_model(input_ids=batch).logits
            log_probs = F.log_softmax(logits, dim=-1)
        for idx in range(batch_end - batch_start):
            j = target_positions[batch_start + idx]
            true_tok = base_tokens[j + 1].item()
            single_mask_logp[j] = log_probs[idx, j + 1, true_tok].item()

    # Step 2: double-mask logprobs
    influence = {i: {} for i in source_positions}
    # Build all (source, target) pairs
    pairs = [(i, j) for i in source_positions for j in target_positions]

    double_batch_ids = []
    for i, j in pairs:
        ids = base_tokens.clone()
        ids[i + 1] = mask_id
        ids[j + 1] = mask_id
        double_batch_ids.append(ids)

    for batch_start in range(0, len(double_batch_ids), batch_size):
        batch_end = min(batch_start + batch_size, len(double_batch_ids))
        batch = torch.stack(double_batch_ids[batch_start:batch_end]).to(device)
        with torch.no_grad():
            logits = esm_model(input_ids=batch).logits
            log_probs = F.log_softmax(logits, dim=-1)
        for idx in range(batch_end - batch_start):
            pair_idx = batch_start + idx
            i, j = pairs[pair_idx]
            true_tok = base_tokens[j + 1].item()
            double_logp = log_probs[idx, j + 1, true_tok].item()
            influence[i][j] = single_mask_logp[j] - double_logp

    return influence


def summarize_influence(influence_per_source: dict[int, float]) -> dict:
    vals = list(influence_per_source.values())
    if not vals:
        return {"mean": 0.0, "median": 0.0, "max": 0.0, "n_positive": 0, "sum": 0.0}
    return {
        "mean": float(np.mean(vals)),
        "median": float(np.median(vals)),
        "max": float(np.max(vals)),
        "n_positive": int(sum(1 for v in vals if v > 0)),
        "sum": float(np.sum(vals)),
    }


# ---------------------------------------------------------------------------
# Statistical comparison
# ---------------------------------------------------------------------------

def compare_anchor_vs_controls(anchor_vals: dict, control_vals_list: list[dict], feature_names: list[str]) -> dict:
    result = {}
    for feat in feature_names:
        a_val = anchor_vals[feat]
        c_vals = [cv[feat] for cv in control_vals_list if feat in cv]
        if not c_vals:
            result[feat] = {"anchor": a_val, "control_mean": np.nan, "diff": np.nan, "z": np.nan}
            continue
        c_mean = np.mean(c_vals)
        c_std = np.std(c_vals, ddof=1) if len(c_vals) > 1 else 1e-8
        z = (a_val - c_mean) / max(c_std, 1e-8)
        result[feat] = {
            "anchor": a_val,
            "control_mean": c_mean,
            "control_std": c_std,
            "diff": a_val - c_mean,
            "z": z,
            "anchor_exceeds_all": a_val > max(c_vals) if c_vals else False,
        }
    return result


def paired_test_across_proteins(all_diffs: list[float], label: str) -> dict:
    n = len(all_diffs)
    if n < 3:
        return {"label": label, "n": n, "mean_diff": np.mean(all_diffs) if all_diffs else 0.0, "t_p": np.nan, "wilcoxon_p": np.nan, "cohens_d": np.nan}
    arr = np.array(all_diffs)
    mean_d = float(arr.mean())
    std_d = float(arr.std(ddof=1))
    cohens_d = mean_d / std_d if std_d > 1e-8 else 0.0
    t_stat, t_p = stats.ttest_1samp(arr, 0.0)
    try:
        w_stat, w_p = stats.wilcoxon(arr)
    except ValueError:
        w_p = np.nan
    return {"label": label, "n": n, "mean_diff": mean_d, "cohens_d": cohens_d, "t_p": float(t_p), "wilcoxon_p": float(w_p)}


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

SSE_COLORS = {"H": "#e06c75", "E": "#61afef", "C": "#98c379"}


def plot_coupling_comparison(coupling_results: list[dict], output_dir: Path) -> None:
    features = ["sum_longrange_score", "n_longrange_pairs", "n_coupling_bins", "coupling_bin_entropy", "n_distinct_sse_segments"]
    n_feat = len(features)
    fig, axes = plt.subplots(1, n_feat, figsize=(3.5 * n_feat, 4))
    if n_feat == 1:
        axes = [axes]

    for ax, feat in zip(axes, features):
        proteins = [r["protein"] for r in coupling_results]
        anchor_vals = [r["comparison"][feat]["anchor"] for r in coupling_results]
        control_means = [r["comparison"][feat]["control_mean"] for r in coupling_results]

        x = np.arange(len(proteins))
        w = 0.35
        ax.bar(x - w / 2, anchor_vals, w, label="anchor", color="#e06c75", alpha=0.8)
        ax.bar(x + w / 2, control_means, w, label="control mean", color="#61afef", alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(proteins, rotation=45, ha="right", fontsize=8)
        ax.set_title(feat.replace("_", " "), fontsize=9)
        ax.legend(fontsize=7)

    plt.tight_layout()
    out = output_dir / "anchor_infohub_v1_A_coupling.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_coupling_effect_sizes(paired_results: list[dict], output_dir: Path) -> None:
    labels = [r["label"] for r in paired_results]
    ds = [r["cohens_d"] for r in paired_results]
    ps = [r["t_p"] for r in paired_results]

    fig, ax = plt.subplots(figsize=(6, 4))
    colors = ["#e06c75" if (not np.isnan(p) and p < 0.05) else "#999999" for p in ps]
    y = np.arange(len(labels))
    ax.barh(y, ds, color=colors, alpha=0.8)
    ax.set_yticks(y)
    ax.set_yticklabels([l.replace("_", " ") for l in labels], fontsize=9)
    ax.set_xlabel("Cohen's d (anchor - control)")
    ax.axvline(0, color="black", linewidth=0.5)
    ax.set_title("Part A: coupling feature effect sizes")
    plt.tight_layout()
    out = output_dir / "anchor_infohub_v1_B_coupling_effects.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_influence_comparison(influence_results: list[dict], output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    proteins = [r["protein"] for r in influence_results]
    anchor_means = [r["anchor_summary"]["mean"] for r in influence_results]
    control_means = [np.mean([s["mean"] for s in r["control_summaries"]]) for r in influence_results]

    x = np.arange(len(proteins))
    for i in range(len(proteins)):
        ax.plot([x[i], x[i]], [control_means[i], anchor_means[i]], color="#888888", linewidth=1, zorder=1)
    ax.scatter(x, anchor_means, color="#e06c75", s=60, zorder=2, label="anchor", marker="*")
    ax.scatter(x, control_means, color="#61afef", s=40, zorder=2, label="control mean")

    ax.set_xticks(x)
    ax.set_xticklabels(proteins, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Mean influence on distant targets")
    ax.set_title("Part B: ESM conditional influence (anchor vs controls)")
    ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
    ax.legend(fontsize=8)
    plt.tight_layout()
    out = output_dir / "anchor_infohub_v1_C_influence.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_influence_heatmap(influence_data: dict, protein: str, source_labels: dict, output_dir: Path) -> None:
    sources = sorted(influence_data.keys())
    if not sources:
        return
    targets = sorted(influence_data[sources[0]].keys())
    if not targets:
        return

    matrix = np.array([[influence_data[s].get(t, 0.0) for t in targets] for s in sources])
    fig, ax = plt.subplots(figsize=(max(6, len(targets) * 0.4), max(3, len(sources) * 0.5)))
    vmax = max(abs(matrix.min()), abs(matrix.max()), 0.01)
    im = ax.imshow(matrix, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_yticks(range(len(sources)))
    ax.set_yticklabels([source_labels.get(s, str(s)) for s in sources], fontsize=8)
    ax.set_xlabel("Target position")
    ax.set_title(f"Influence map: {protein}")
    plt.colorbar(im, ax=ax, label="influence")
    plt.tight_layout()
    out = output_dir / "anchor_infohub_v1_D_heatmap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    coupling_results: list[dict],
    coupling_paired: list[dict],
    influence_results: list[dict],
    influence_paired: dict,
    matched_info: dict,
    output_dir: Path,
) -> None:
    lines = []
    lines.append("# Anchor Information-Hub Experiment v1\n\n")
    lines.append("## Methodology\n\n")
    lines.append("This experiment tests whether anchor residues (high L10H9 projection score positions) function as information hubs.\n\n")
    lines.append("Two tracks: (A) EVcouplings-based coupling feature analysis on 4 proteins with MSA data, and (B) ESM conditional influence test on all 18 proteins.\n\n")
    lines.append(f"Matched controls: {N_CONTROLS} per anchor, matched on SSE type, RSA, and contacts_8A, with top-10% projection rank excluded.\n\n")

    # Matched controls summary
    lines.append("## Matched control summary\n\n")
    lines.append("| Protein | Anchor | SSE | N controls | Tolerance tier |\n")
    lines.append("|---------|--------|-----|------------|----------------|\n")
    for protein, info in sorted(matched_info.items()):
        lines.append(f"| {protein} | {info['anchor_pos']} | {info['anchor_sse']} | {info['n_controls']} | {info['tier']} |\n")
    lines.append("\n")

    # Part A
    lines.append("## Part A: EVcouplings coupling features\n\n")
    if not coupling_results:
        lines.append("No proteins with coupling data found.\n\n")
    else:
        lines.append(f"Proteins with coupling data: {', '.join(r['protein'] for r in coupling_results)}\n\n")

        features = ["sum_longrange_score", "n_longrange_pairs", "n_coupling_bins", "coupling_bin_entropy", "n_distinct_sse_segments"]
        lines.append("### Per-protein anchor vs control comparison\n\n")
        lines.append("| Protein | Feature | Anchor | Control mean | Diff | z-score | Anchor > all? |\n")
        lines.append("|---------|---------|--------|-------------|------|---------|---------------|\n")
        for r in coupling_results:
            for feat in features:
                c = r["comparison"][feat]
                exceeds = "yes" if c.get("anchor_exceeds_all", False) else "no"
                lines.append(f"| {r['protein']} | {feat} | {c['anchor']:.2f} | {c['control_mean']:.2f} | {c['diff']:.2f} | {c['z']:.2f} | {exceeds} |\n")
        lines.append("\n")

        lines.append("### Cross-protein paired tests (N=4, treat as descriptive)\n\n")
        lines.append("| Feature | Mean diff | Cohen's d | t-test p | Wilcoxon p |\n")
        lines.append("|---------|-----------|-----------|----------|------------|\n")
        for r in coupling_paired:
            lines.append(f"| {r['label']} | {r['mean_diff']:.3f} | {r['cohens_d']:.3f} | {r['t_p']:.4f} | {r['wilcoxon_p']:.4f} |\n")
        lines.append("\n")

        # Anchor rank in coupling space
        lines.append("### Anchor rank in coupling space\n\n")
        lines.append("| Protein | Feature | Anchor rank | Total residues | Percentile |\n")
        lines.append("|---------|---------|-------------|----------------|------------|\n")
        for r in coupling_results:
            for feat in features:
                rank = r["anchor_ranks"].get(feat, {})
                lines.append(f"| {r['protein']} | {feat} | {rank.get('rank', 'N/A')} | {rank.get('total', 'N/A')} | {rank.get('percentile', 0):.1f} |\n")
        lines.append("\n")

    # Part B
    lines.append("## Part B: ESM conditional influence\n\n")
    lines.append(f"For each protein, masked the anchor and {N_CONTROLS} matched controls as source residues, measured influence on {N_TARGETS} distant targets (|i-j| >= {MIN_SEQ_SEP}).\n\n")
    lines.append("influence(i->j) = logP(true_j | mask_j) - logP(true_j | mask_i, mask_j)\n\n")

    lines.append("### Per-protein results\n\n")
    lines.append("| Protein | Anchor mean | Control mean | Diff | Anchor n_pos | Control n_pos | Anchor > ctrl mean? |\n")
    lines.append("|---------|-------------|--------------|------|-------------|---------------|---------------------|\n")
    for r in influence_results:
        a = r["anchor_summary"]
        c_means = [s["mean"] for s in r["control_summaries"]]
        c_mean = np.mean(c_means) if c_means else 0.0
        c_npos = np.mean([s["n_positive"] for s in r["control_summaries"]]) if r["control_summaries"] else 0.0
        diff = a["mean"] - c_mean
        win = "yes" if a["mean"] > c_mean else "no"
        lines.append(f"| {r['protein']} | {a['mean']:.4f} | {c_mean:.4f} | {diff:.4f} | {a['n_positive']} | {c_npos:.1f} | {win} |\n")
    lines.append("\n")

    lines.append("### Cross-protein paired test\n\n")
    lines.append(f"N = {influence_paired['n']}\n\n")
    lines.append(f"Mean difference (anchor - control mean): {influence_paired['mean_diff']:.4f}\n\n")
    lines.append(f"Cohen's d: {influence_paired['cohens_d']:.3f}\n\n")
    lines.append(f"Paired t-test p: {influence_paired['t_p']:.4f}\n\n")
    if not np.isnan(influence_paired.get("wilcoxon_p", np.nan)):
        lines.append(f"Wilcoxon signed-rank p: {influence_paired['wilcoxon_p']:.4f}\n\n")
    lines.append("\n")

    # Combined interpretation
    lines.append("## Combined interpretation\n\n")
    n_win_b = sum(1 for r in influence_results if r["anchor_summary"]["mean"] > np.mean([s["mean"] for s in r["control_summaries"]]))
    n_total_b = len(influence_results)
    lines.append(f"Part B: anchor beats control mean in {n_win_b}/{n_total_b} proteins.\n\n")
    if coupling_results:
        n_win_a = sum(1 for r in coupling_results
                      for feat in ["sum_longrange_score", "n_coupling_bins"]
                      if r["comparison"][feat]["diff"] > 0)
        lines.append(f"Part A: anchor has higher coupling features in {n_win_a} / {2 * len(coupling_results)} (protein x feature) comparisons.\n\n")

    out = output_dir / "anchor_information_hub_v1.md"
    with open(out, "w") as f:
        f.writelines(lines)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Anchor information-hub experiment v1")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    device = args.device
    print(f"Device: {device}")

    # --- Load data ---
    print("Loading configs...")
    protein_configs, seqs, ss_dict = load_configs()

    print("Loading model...")
    model, tokenizer = load_model(device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    ref_seq = seqs[REFERENCE_PROTEIN]
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights, device)
    search_dir_unit = search_dir / search_dir.norm().clamp(min=1e-8)

    # --- Per-protein: PDB features, SSE, projection, matched controls ---
    print("\nComputing per-protein features...")
    protein_data = {}
    matched_info = {}

    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        seq = seqs.get(protein)
        if seq is None:
            print(f"  {protein}: sequence not found, skipping")
            continue
        sse_str = ss_dict.get(protein)
        if sse_str is None:
            print(f"  {protein}: SSE not found, skipping")
            continue

        # Truncate SSE to sequence length if needed
        if len(sse_str) > len(seq):
            sse_str = sse_str[:len(seq)]
        elif len(sse_str) < len(seq):
            sse_str = sse_str + "C" * (len(seq) - len(sse_str))

        sse_features = compute_sse_features(sse_str)
        pdb_features = compute_pdb_features(protein, seq)
        proj_scores = capture_projection_scores(model, tokenizer, seq, search_dir_unit, device)

        controls, tier = build_matched_controls(protein, anchor_pos, seq, sse_features, pdb_features, proj_scores)

        anchor_sse = sse_features[anchor_pos]["sse"] if anchor_pos < len(sse_features) and sse_features[anchor_pos] else "?"
        matched_info[protein] = {
            "anchor_pos": anchor_pos,
            "anchor_sse": anchor_sse,
            "n_controls": len(controls),
            "tier": tier,
        }

        protein_data[protein] = {
            "seq": seq,
            "sse_features": sse_features,
            "pdb_features": pdb_features,
            "proj_scores": proj_scores,
            "anchor_pos": anchor_pos,
            "controls": controls,
        }

        n_ctrl = len(controls)
        print(f"  {protein}: anchor={anchor_pos} ({anchor_sse}), controls={n_ctrl}, tier={tier}")

    # ======================================================================
    # Part A: EVcouplings coupling features
    # ======================================================================
    print("\n=== Part A: EVcouplings coupling features ===")
    coupling_results = []
    coupling_feature_names = ["sum_longrange_score", "n_longrange_pairs", "n_coupling_bins", "coupling_bin_entropy", "n_distinct_sse_segments"]

    for protein, pdata in protein_data.items():
        csv_path = find_ev_coupling_csv(protein, longrange_only=True)
        if csv_path is None:
            continue
        if not pdata["controls"]:
            print(f"  {protein}: has coupling data but no matched controls, skipping")
            continue

        print(f"  {protein}: loading coupling scores from {csv_path.name}")
        coupling_rows = load_coupling_scores(csv_path)
        print(f"    {len(coupling_rows)} coupling pairs loaded")

        coup_features = aggregate_coupling_features(coupling_rows, len(pdata["seq"]), pdata["sse_features"])

        anchor_pos = pdata["anchor_pos"]
        anchor_feats = coup_features.get(anchor_pos, {})
        control_feats = [coup_features.get(c, {}) for c in pdata["controls"]]

        comparison = compare_anchor_vs_controls(anchor_feats, control_feats, coupling_feature_names)

        # Anchor rank computation
        anchor_ranks = {}
        for feat in coupling_feature_names:
            all_vals = sorted([coup_features[p][feat] for p in coup_features if feat in coup_features[p]], reverse=True)
            a_val = anchor_feats.get(feat, 0.0)
            rank = next((i + 1 for i, v in enumerate(all_vals) if v <= a_val), len(all_vals))
            total = len(all_vals)
            pctile = 100.0 * (1.0 - rank / total) if total > 0 else 0.0
            anchor_ranks[feat] = {"rank": rank, "total": total, "percentile": round(pctile, 1)}

        coupling_results.append({
            "protein": protein,
            "comparison": comparison,
            "anchor_ranks": anchor_ranks,
        })

        # Print summary
        for feat in coupling_feature_names:
            c = comparison[feat]
            print(f"    {feat}: anchor={c['anchor']:.2f}, ctrl_mean={c['control_mean']:.2f}, z={c['z']:.2f}")

    # Cross-protein paired tests for Part A
    coupling_paired = []
    for feat in coupling_feature_names:
        diffs = [r["comparison"][feat]["diff"] for r in coupling_results if not np.isnan(r["comparison"][feat]["diff"])]
        coupling_paired.append(paired_test_across_proteins(diffs, feat))

    if coupling_results:
        plot_coupling_comparison(coupling_results, REPORT_DIR)
        plot_coupling_effect_sizes(coupling_paired, REPORT_DIR)

    # ======================================================================
    # Part B: ESM conditional influence
    # ======================================================================
    print("\n=== Part B: ESM conditional influence ===")
    esm_model = model._model  # unwrap NNsight for direct forward passes
    influence_results = []
    first_protein_influence = None

    for protein, pdata in protein_data.items():
        if not pdata["controls"]:
            print(f"  {protein}: no controls, skipping influence test")
            continue

        anchor_pos = pdata["anchor_pos"]
        controls = pdata["controls"]
        seq = pdata["seq"]

        targets = select_distant_targets(anchor_pos, len(seq))
        source_positions = [anchor_pos] + controls

        print(f"  {protein}: {len(source_positions)} sources x {len(targets)} targets = {len(source_positions) * len(targets)} pairs")

        influence = compute_conditional_influence(esm_model, tokenizer, seq, source_positions, targets, device)

        anchor_summary = summarize_influence(influence[anchor_pos])
        control_summaries = [summarize_influence(influence[c]) for c in controls]

        result = {
            "protein": protein,
            "anchor_pos": anchor_pos,
            "controls": controls,
            "targets": targets,
            "anchor_summary": anchor_summary,
            "control_summaries": control_summaries,
        }
        influence_results.append(result)

        if first_protein_influence is None:
            first_protein_influence = (influence, protein, source_positions, anchor_pos, controls)

        c_mean = np.mean([s["mean"] for s in control_summaries]) if control_summaries else 0.0
        diff = anchor_summary["mean"] - c_mean
        print(f"    anchor mean_influence={anchor_summary['mean']:.4f}, control_mean={c_mean:.4f}, diff={diff:.4f}")

    # Cross-protein paired test for Part B
    influence_diffs = []
    for r in influence_results:
        c_mean = np.mean([s["mean"] for s in r["control_summaries"]]) if r["control_summaries"] else 0.0
        influence_diffs.append(r["anchor_summary"]["mean"] - c_mean)

    influence_paired = paired_test_across_proteins(influence_diffs, "mean_influence")

    if influence_results:
        plot_influence_comparison(influence_results, REPORT_DIR)

    # Heatmap for first protein
    if first_protein_influence is not None:
        inf_data, inf_protein, inf_sources, inf_anchor, inf_controls = first_protein_influence
        labels = {inf_anchor: f"ANCHOR ({inf_anchor})"}
        for c in inf_controls:
            labels[c] = f"ctrl ({c})"
        plot_influence_heatmap(inf_data, inf_protein, labels, REPORT_DIR)

    # ======================================================================
    # Report
    # ======================================================================
    print("\nGenerating report...")
    generate_report(coupling_results, coupling_paired, influence_results, influence_paired, matched_info, REPORT_DIR)

    # Summary
    print("\n=== Summary ===")
    if influence_results:
        n_win = sum(1 for r in influence_results if r["anchor_summary"]["mean"] > np.mean([s["mean"] for s in r["control_summaries"]]))
        print(f"Part B: anchor beats control mean in {n_win}/{len(influence_results)} proteins")
        print(f"  Cohen's d = {influence_paired['cohens_d']:.3f}, p = {influence_paired['t_p']:.4f}")
    if coupling_results:
        print(f"Part A: {len(coupling_results)} proteins with coupling data analyzed")
        for r in coupling_paired:
            print(f"  {r['label']}: d={r['cohens_d']:.3f}, p={r['t_p']:.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
