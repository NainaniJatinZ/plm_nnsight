#!/usr/bin/env python3
"""Anchor information-hub experiment v2 (experiments/3_27_anchor_info_hub_v2.md).

Refines v1 by using:
  - top-3 anchors (not just top-1)
  - three target sets: G1 (random distant), G2 (task-relevant), G3 (distant structural contacts)
  - sparse-target summaries (top25 mean, max, fraction positive)

No EVcouplings track. Focus on whether anchor advantage is target-specific.

Usage:
    uv run python scripts/anchor_information_hub_v2.py --device cuda
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
    "1BRTA": 220, "1PVGA": 101, "2B61A": 315, "2DPMA": 39,
    "2PKEA": 131, "2QY6A": 64, "2YHWA": 287, "3CSSA": 40,
    "3HO7A": 63, "3OKPA": 200, "3QDLA": 114, "3WJPA": 94,
    "4EHUA": 100, "4EX6A": 124, "4EZIA": 310, "4ME3A": 75,
    "4N9WA": 194, "4OY3A": 193,
}

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}

TOP_K_ANCHORS = 3
N_CONTROLS = 5
N_RANDOM_TARGETS = 16
MIN_SEQ_SEP = 24
BATCH_SIZE = 16
POSITIVE_THRESHOLD = 0.01

TARGET_SETS = ["G1", "G2", "G3"]
SUMMARY_METRICS = ["mean_influence", "top25_mean", "max_influence", "fraction_positive"]


# ---------------------------------------------------------------------------
# Data loading (from v1)
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
# PDB features and contact map (from v1 + extended for G3)
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
        print(f"    WARNING: poor PDB alignment for {protein}")
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

    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_residues_raw[pdb_idx]
        max_asa = MAX_ASA.get(r["aa"], 200)
        raw_sasa = sasa_by_resid.get(r["resid"], 0.0)
        rsa = min(raw_sasa / max_asa, 1.0) if max_asa > 0 else 0.0
        features[seq_pos] = {
            "rsa": round(rsa, 4),
            "contacts_8A": int(contacts_8A[pdb_idx]),
        }
    return features


def compute_pdb_contact_map(protein: str, full_seq: str) -> tuple[dict[int, list[int]], bool]:
    """Compute per-residue 3D contact neighbors (CB < 8A, |i-j| >= MIN_SEQ_SEP).

    Returns (contact_map: {seq_pos -> [seq_pos neighbors]}, success: bool).
    """
    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return {}, False
    pdb_residues_raw, _ = _parse_pdb_residues(pdb_path)
    if not pdb_residues_raw:
        return {}, False
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues_raw]
    mapping = _align_pdb_to_seq(pdb_tuples, full_seq)
    if len(mapping) < len(pdb_residues_raw) * 0.5:
        return {}, False

    # Build reverse mapping: seq_pos -> pdb_idx
    rev_mapping = {seq_pos: pdb_idx for pdb_idx, seq_pos in mapping.items()}

    cb_coords = np.array([r["cb"] for r in pdb_residues_raw])
    from scipy.spatial.distance import cdist
    dists = cdist(cb_coords, cb_coords)

    contact_map = {}
    for seq_pos_i, pdb_idx_i in rev_mapping.items():
        neighbors = []
        for seq_pos_j, pdb_idx_j in rev_mapping.items():
            if seq_pos_i == seq_pos_j:
                continue
            if abs(seq_pos_i - seq_pos_j) < MIN_SEQ_SEP:
                continue
            if dists[pdb_idx_i, pdb_idx_j] < 8.0:
                neighbors.append(seq_pos_j)
        contact_map[seq_pos_i] = neighbors
    return contact_map, True


# ---------------------------------------------------------------------------
# SSE features (from v1)
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
            features[pos] = {
                "sse": label,
                "seg_len": seg_len,
                "dist_to_boundary": min(dist_left, dist_right),
            }
        i = j
    return features


# ---------------------------------------------------------------------------
# Model loading and projection scores (from v1)
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
    return {"W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(),
            "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone()}


def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    q_all = x_ln @ weights["W_Q_hd"].T + weights["b_Q_d"]
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    return weights["W_K_hd"].T @ q_mean_norm


def capture_projection_scores(model, tokenizer, sequence: str, search_dir_unit: torch.Tensor, device: str) -> np.ndarray:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    return (x_ln[1:-1] @ search_dir_unit.cpu()).numpy()


# ---------------------------------------------------------------------------
# Top-k anchor identification (new)
# ---------------------------------------------------------------------------

def identify_top_k_anchors(proj_scores: np.ndarray, k: int = TOP_K_ANCHORS) -> list[int]:
    """Return top-k positions by projection score (descending)."""
    ranked = np.argsort(proj_scores)[::-1]
    return ranked[:k].tolist()


# ---------------------------------------------------------------------------
# Matched controls (from v1)
# ---------------------------------------------------------------------------

TOLERANCE_TIERS = [
    (0.05, 3), (0.08, 3), (0.08, 5), (0.12, 5), (0.15, 8), (0.20, 10),
]


def build_matched_controls(
    protein: str, anchor_pos: int, sequence: str,
    sse_features: list[dict], pdb_features: dict | None,
    proj_scores: np.ndarray, n_controls: int = N_CONTROLS,
) -> tuple[list[int], int]:
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
            return rng.choice(candidates, size=n_controls, replace=False).tolist(), tier_idx
    if candidates:
        return candidates[:n_controls], len(TOLERANCE_TIERS) - 1
    return [], -1


# ---------------------------------------------------------------------------
# Target set construction (new)
# ---------------------------------------------------------------------------

def build_g1_targets(source_pos: int, seq_len: int, n_targets: int = N_RANDOM_TARGETS) -> list[int]:
    """G1: random distant targets, stratified across sequence."""
    eligible = [j for j in range(seq_len) if abs(j - source_pos) >= MIN_SEQ_SEP]
    if len(eligible) <= n_targets:
        return eligible
    bin_size = len(eligible) / n_targets
    return [eligible[int((i + 0.5) * bin_size)] for i in range(n_targets)]


def build_g2_targets(config: dict, source_pos: int, seq_len: int) -> list[int]:
    """G2: task-relevant targets (SS1 and SS2 segments +/- SEGMENT_RADIUS)."""
    pos1, pos2 = config["contact_pair"]
    targets = set()
    for center in [pos1, pos2]:
        for offset in range(-SEGMENT_RADIUS, SEGMENT_RADIUS + 1):
            p = center + offset
            if 0 <= p < seq_len and p != source_pos:
                targets.add(p)
    return sorted(targets)


def build_g3_targets(contact_map: dict, source_pos: int, max_targets: int = 16) -> list[int]:
    """G3: distant structural contacts of source (CB < 8A, |i-j| >= 24)."""
    neighbors = contact_map.get(source_pos, [])
    if len(neighbors) <= max_targets:
        return sorted(neighbors)
    # deterministic subsample: evenly spaced
    neighbors = sorted(neighbors)
    step = len(neighbors) / max_targets
    return [neighbors[int(i * step)] for i in range(max_targets)]


# ---------------------------------------------------------------------------
# ESM conditional influence (from v1)
# ---------------------------------------------------------------------------

def compute_conditional_influence(
    esm_model, tokenizer, sequence: str,
    source_positions: list[int], target_positions: list[int],
    device: str, batch_size: int = BATCH_SIZE,
) -> dict[int, dict[int, float]]:
    """influence(i->j) = logP(true_j | mask_j) - logP(true_j | mask_i, mask_j)."""
    if not target_positions:
        return {i: {} for i in source_positions}

    mask_id = tokenizer.mask_token_id
    base_tokens = tokenizer(sequence, return_tensors="pt")["input_ids"][0]

    # Single-mask logprobs (shared across sources)
    single_mask_logp = {}
    single_batch_ids = []
    for j in target_positions:
        ids = base_tokens.clone()
        ids[j + 1] = mask_id
        single_batch_ids.append(ids)

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

    # Double-mask logprobs
    influence = {i: {} for i in source_positions}
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
            influence[i][j] = single_mask_logp[j] - log_probs[idx, j + 1, true_tok].item()

    return influence


# ---------------------------------------------------------------------------
# Influence summaries (extended from v1)
# ---------------------------------------------------------------------------

def summarize_influence_v2(influence_per_source: dict[int, float]) -> dict:
    vals = list(influence_per_source.values())
    if not vals:
        return {"mean_influence": 0.0, "median_influence": 0.0, "max_influence": 0.0,
                "top25_mean": 0.0, "fraction_positive": 0.0, "n_targets": 0,
                "n_above_threshold": 0}
    arr = np.array(vals)
    n = len(arr)
    sorted_vals = np.sort(arr)[::-1]
    top25_k = max(1, n // 4)
    return {
        "mean_influence": float(arr.mean()),
        "median_influence": float(np.median(arr)),
        "max_influence": float(arr.max()),
        "top25_mean": float(sorted_vals[:top25_k].mean()),
        "fraction_positive": float((arr > 0).sum() / n),
        "n_targets": n,
        "n_above_threshold": int((arr > POSITIVE_THRESHOLD).sum()),
    }


# ---------------------------------------------------------------------------
# Statistical helpers
# ---------------------------------------------------------------------------

def paired_test(diffs: list[float], label: str) -> dict:
    n = len(diffs)
    if n < 3:
        return {"label": label, "n": n, "mean_diff": np.mean(diffs) if diffs else 0.0, "cohens_d": np.nan, "t_p": np.nan, "wilcoxon_p": np.nan}
    arr = np.array(diffs)
    mean_d = float(arr.mean())
    std_d = float(arr.std(ddof=1))
    d = mean_d / std_d if std_d > 1e-8 else 0.0
    _, t_p = stats.ttest_1samp(arr, 0.0)
    try:
        _, w_p = stats.wilcoxon(arr)
    except ValueError:
        w_p = np.nan
    return {"label": label, "n": n, "mean_diff": mean_d, "cohens_d": d, "t_p": float(t_p), "wilcoxon_p": float(w_p)}


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_a_target_set_effects(analysis1: dict, analysis2: dict, output_dir: Path) -> None:
    """Plot A: anchor-control difference by target set and metric."""
    fig, axes = plt.subplots(1, len(SUMMARY_METRICS), figsize=(4 * len(SUMMARY_METRICS), 4.5))

    for ax, metric in zip(axes, SUMMARY_METRICS):
        # Top-1
        top1_diffs = {g: analysis1[g].get("mean_diff", 0.0) for g in TARGET_SETS if g in analysis1}
        # Top-3
        top3_diffs = {g: analysis2[g].get("mean_diff", 0.0) for g in TARGET_SETS if g in analysis2}

        x = np.arange(len(TARGET_SETS))
        w = 0.35
        t1_vals = [top1_diffs.get(g, 0.0) for g in TARGET_SETS]
        t3_vals = [top3_diffs.get(g, 0.0) for g in TARGET_SETS]

        ax.bar(x - w / 2, t1_vals, w, label="top-1", color="#e06c75", alpha=0.8)
        ax.bar(x + w / 2, t3_vals, w, label="top-3", color="#61afef", alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(TARGET_SETS)
        ax.set_title(metric.replace("_", " "), fontsize=10)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.legend(fontsize=7)

    fig.suptitle("Anchor - control difference by target set", fontsize=11)
    plt.tight_layout()
    out = output_dir / "anchor_infohub_v2_A_target_set_effects.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_b_per_protein(protein_results: list[dict], output_dir: Path) -> None:
    """Plot B: per-protein connected-line plots for mean_influence on G1/G2/G3."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    for ax, g in zip(axes, TARGET_SETS):
        proteins_with_data = [r for r in protein_results if g in r["top1_summaries"]]
        if not proteins_with_data:
            ax.set_title(f"{g}: no data")
            continue
        proteins = [r["protein"] for r in proteins_with_data]
        anchor_vals = [r["top1_summaries"][g]["mean_influence"] for r in proteins_with_data]
        ctrl_vals = [np.mean([s["mean_influence"] for s in r["control_summaries_by_set"].get(g, [])]) if r["control_summaries_by_set"].get(g) else 0.0 for r in proteins_with_data]

        x = np.arange(len(proteins))
        for i in range(len(proteins)):
            ax.plot([x[i], x[i]], [ctrl_vals[i], anchor_vals[i]], color="#888888", linewidth=1, zorder=1)
        ax.scatter(x, anchor_vals, color="#e06c75", s=60, zorder=2, marker="*", label="anchor")
        ax.scatter(x, ctrl_vals, color="#61afef", s=40, zorder=2, label="control mean")
        ax.set_xticks(x)
        ax.set_xticklabels(proteins, rotation=45, ha="right", fontsize=7)
        ax.set_title(f"{g}: mean influence")
        ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
        ax.legend(fontsize=7)

    plt.tight_layout()
    out = output_dir / "anchor_infohub_v2_B_per_protein.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_c_top1_vs_top3(analysis1: dict, analysis2: dict, output_dir: Path) -> None:
    """Plot C: does top-3 pooling strengthen the effect?"""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    metrics_to_plot = ["mean_influence", "top25_mean", "fraction_positive"]
    x = np.arange(len(TARGET_SETS))
    w = 0.12
    colors_top1 = ["#e06c75", "#c0392b", "#922b21"]
    colors_top3 = ["#61afef", "#2980b9", "#1f618d"]

    for mi, metric in enumerate(metrics_to_plot):
        t1_ds = [analysis1[g].get("cohens_d", 0.0) if g in analysis1 else 0.0 for g in TARGET_SETS]
        t3_ds = [analysis2[g].get("cohens_d", 0.0) if g in analysis2 else 0.0 for g in TARGET_SETS]
        offset = (mi - 1) * w * 2.5
        ax.bar(x + offset - w / 2, t1_ds, w, color=colors_top1[mi], alpha=0.8, label=f"top1 {metric}" if mi == 0 else "")
        ax.bar(x + offset + w / 2, t3_ds, w, color=colors_top3[mi], alpha=0.8, label=f"top3 {metric}" if mi == 0 else "")

    ax.set_xticks(x)
    ax.set_xticklabels(TARGET_SETS)
    ax.set_ylabel("Cohen's d")
    ax.set_title("Top-1 vs top-3 anchor effect sizes")
    ax.axhline(0, color="black", linewidth=0.5)
    # Custom legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor="#e06c75", label="top-1"), Patch(facecolor="#61afef", label="top-3")]
    for mi, metric in enumerate(metrics_to_plot):
        legend_elements.append(Patch(facecolor="white", edgecolor="black", label=metric.replace("_", " ")))
    ax.legend(handles=legend_elements[:2], fontsize=8)
    plt.tight_layout()
    out = output_dir / "anchor_infohub_v2_C_top1_vs_top3.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


def plot_d_heatmap(influence_data: dict, protein: str, source_labels: dict, target_set_name: str, output_dir: Path) -> None:
    """Plot D: influence heatmap for a representative protein."""
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
    ax.set_title(f"{protein} ({target_set_name})")
    plt.colorbar(im, ax=ax, label="influence")
    plt.tight_layout()
    out = output_dir / "anchor_infohub_v2_D_heatmap.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(
    protein_results: list[dict],
    analysis1_paired: dict,  # top-1 paired tests by target set by metric
    analysis2_paired: dict,  # top-3 paired tests by target set by metric
    matched_info: dict,
    output_dir: Path,
) -> None:
    lines = []
    lines.append("# Anchor Information-Hub Experiment v2\n\n")
    lines.append("## Methodology\n\n")
    lines.append("Tests whether anchors are information hubs using top-1 and top-3 anchors against structurally matched controls.\n\n")
    lines.append(f"Three target sets: G1 (random distant, n<={N_RANDOM_TARGETS}), G2 (task-relevant SS1/SS2 segments), G3 (distant 3D contacts, CB < 8A, |i-j| >= {MIN_SEQ_SEP}).\n\n")
    lines.append("Summary metrics: mean_influence, top25_mean (top quartile mean), max_influence, fraction_positive.\n\n")

    # Matched controls
    lines.append("## Matched controls\n\n")
    lines.append("| Protein | Top-1 anchor | Top-3 anchors | N controls (per anchor) |\n")
    lines.append("|---------|-------------|---------------|-------------------------|\n")
    for protein, info in sorted(matched_info.items()):
        top3 = ", ".join(str(a) for a in info["top3"])
        n_ctrl = info["n_controls_per_anchor"]
        lines.append(f"| {protein} | {info['top1']} | {top3} | {n_ctrl} |\n")
    lines.append("\n")

    # Analysis 1: top-1 anchor vs controls
    lines.append("## Analysis 1: top-1 anchor vs matched controls\n\n")
    for g in TARGET_SETS:
        lines.append(f"### {g}\n\n")
        lines.append("| Protein | mean_infl | ctrl_mean | diff | top25 | ctrl_top25 | frac_pos | ctrl_frac_pos |\n")
        lines.append("|---------|-----------|-----------|------|-------|------------|----------|---------------|\n")
        for r in protein_results:
            if g not in r["top1_summaries"]:
                continue
            a = r["top1_summaries"][g]
            ctrls = r["control_summaries_by_set"].get(g, [])
            c_mean = np.mean([s["mean_influence"] for s in ctrls]) if ctrls else 0.0
            c_top25 = np.mean([s["top25_mean"] for s in ctrls]) if ctrls else 0.0
            c_frac = np.mean([s["fraction_positive"] for s in ctrls]) if ctrls else 0.0
            diff = a["mean_influence"] - c_mean
            lines.append(f"| {r['protein']} | {a['mean_influence']:.4f} | {c_mean:.4f} | {diff:.4f} | {a['top25_mean']:.4f} | {c_top25:.4f} | {a['fraction_positive']:.2f} | {c_frac:.2f} |\n")
        lines.append("\n")

        # Paired test summary
        lines.append("| Metric | N | Mean diff | Cohen's d | t-test p | Wilcoxon p |\n")
        lines.append("|--------|---|-----------|-----------|----------|------------|\n")
        for metric in SUMMARY_METRICS:
            key = f"{g}_{metric}"
            r = analysis1_paired.get(key)
            if r:
                lines.append(f"| {metric} | {r['n']} | {r['mean_diff']:.4f} | {r['cohens_d']:.3f} | {r['t_p']:.4f} | {r['wilcoxon_p']:.4f} |\n")
        lines.append("\n")

    # Analysis 2: top-3 pooled
    lines.append("## Analysis 2: top-3 anchor-set pooled\n\n")
    for g in TARGET_SETS:
        lines.append(f"### {g}\n\n")
        lines.append("| Metric | N | Mean diff | Cohen's d | t-test p | Wilcoxon p |\n")
        lines.append("|--------|---|-----------|-----------|----------|------------|\n")
        for metric in SUMMARY_METRICS:
            key = f"{g}_{metric}"
            r = analysis2_paired.get(key)
            if r:
                lines.append(f"| {metric} | {r['n']} | {r['mean_diff']:.4f} | {r['cohens_d']:.3f} | {r['t_p']:.4f} | {r['wilcoxon_p']:.4f} |\n")
        lines.append("\n")

    # Analysis 3: target-set specificity
    lines.append("## Analysis 3: target-set specificity\n\n")
    lines.append("Does anchor advantage strengthen on G2/G3 vs G1?\n\n")
    lines.append("| Metric | G1 d | G2 d | G3 d | G2 > G1? | G3 > G1? |\n")
    lines.append("|--------|------|------|------|----------|----------|\n")
    for metric in SUMMARY_METRICS:
        g1_d = analysis1_paired.get(f"G1_{metric}", {}).get("cohens_d", np.nan)
        g2_d = analysis1_paired.get(f"G2_{metric}", {}).get("cohens_d", np.nan)
        g3_d = analysis1_paired.get(f"G3_{metric}", {}).get("cohens_d", np.nan)
        g2_win = "yes" if (not np.isnan(g2_d) and not np.isnan(g1_d) and g2_d > g1_d) else "no"
        g3_win = "yes" if (not np.isnan(g3_d) and not np.isnan(g1_d) and g3_d > g1_d) else "no"
        lines.append(f"| {metric} | {g1_d:.3f} | {g2_d:.3f} | {g3_d:.3f} | {g2_win} | {g3_win} |\n")
    lines.append("\n")

    # Analysis 4: sparse-target advantage
    lines.append("## Analysis 4: sparse-target advantage\n\n")
    lines.append("Is the effect stronger for top25_mean / max than for mean?\n\n")
    lines.append("| Target set | mean d | top25 d | max d | top25 > mean? | max > mean? |\n")
    lines.append("|------------|--------|---------|-------|---------------|-------------|\n")
    for g in TARGET_SETS:
        d_mean = analysis1_paired.get(f"{g}_mean_influence", {}).get("cohens_d", np.nan)
        d_top25 = analysis1_paired.get(f"{g}_top25_mean", {}).get("cohens_d", np.nan)
        d_max = analysis1_paired.get(f"{g}_max_influence", {}).get("cohens_d", np.nan)
        t25_win = "yes" if (not np.isnan(d_top25) and not np.isnan(d_mean) and d_top25 > d_mean) else "no"
        max_win = "yes" if (not np.isnan(d_max) and not np.isnan(d_mean) and d_max > d_mean) else "no"
        lines.append(f"| {g} | {d_mean:.3f} | {d_top25:.3f} | {d_max:.3f} | {t25_win} | {max_win} |\n")
    lines.append("\n")

    # Win counts
    lines.append("## Summary\n\n")
    for g in TARGET_SETS:
        n_win = sum(1 for r in protein_results if g in r["top1_summaries"]
                    and r["control_summaries_by_set"].get(g)
                    and r["top1_summaries"][g]["mean_influence"] > np.mean([s["mean_influence"] for s in r["control_summaries_by_set"][g]]))
        n_total = sum(1 for r in protein_results if g in r["top1_summaries"] and r["control_summaries_by_set"].get(g))
        lines.append(f"Top-1 anchor beats control mean on {g}: {n_win}/{n_total} proteins\n\n")

    out = output_dir / "anchor_information_hub_v2.md"
    with open(out, "w") as f:
        f.writelines(lines)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# CSV export
# ---------------------------------------------------------------------------

def export_source_level_csv(protein_results: list[dict], output_dir: Path) -> None:
    rows = []
    for pr in protein_results:
        protein = pr["protein"]
        for g in TARGET_SETS:
            # Top-1 anchor
            if g in pr["top1_summaries"]:
                s = pr["top1_summaries"][g]
                rows.append({"protein": protein, "source_type": "anchor_top1", "source_pos": pr["top1"],
                             "target_set": g, **s})
            # Top-3 anchors
            for rank, apos in enumerate(pr["top3"]):
                key = f"{g}_{apos}"
                if key in pr.get("all_anchor_summaries", {}):
                    s = pr["all_anchor_summaries"][key]
                    rows.append({"protein": protein, "source_type": f"anchor_top{rank+1}", "source_pos": apos,
                                 "target_set": g, **s})
            # Controls
            for ci, ctrl_pos in enumerate(pr["control_positions"]):
                ckey = f"{g}_{ctrl_pos}"
                if ckey in pr.get("all_control_summaries", {}):
                    s = pr["all_control_summaries"][ckey]
                    rows.append({"protein": protein, "source_type": f"control_{ci}", "source_pos": ctrl_pos,
                                 "target_set": g, **s})

    if not rows:
        return
    fieldnames = list(rows[0].keys())
    out = output_dir / "anchor_information_hub_v2_source_level.csv"
    with open(out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Anchor information-hub experiment v2")
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

    esm_model = model._model  # unwrap for forward passes

    # --- Per-protein setup ---
    print("\nPer-protein setup...")
    protein_data = {}
    matched_info = {}

    for protein in ANCHOR_POSITIONS:
        seq = seqs.get(protein)
        if seq is None:
            print(f"  {protein}: no sequence, skipping")
            continue
        sse_str = ss_dict.get(protein)
        if sse_str is None:
            print(f"  {protein}: no SSE, skipping")
            continue
        if len(sse_str) > len(seq):
            sse_str = sse_str[:len(seq)]
        elif len(sse_str) < len(seq):
            sse_str = sse_str + "C" * (len(seq) - len(sse_str))

        sse_features = compute_sse_features(sse_str)
        pdb_features = compute_pdb_features(protein, seq)
        proj_scores = capture_projection_scores(model, tokenizer, seq, search_dir_unit, device)

        # Top-k anchors
        top_k = identify_top_k_anchors(proj_scores, TOP_K_ANCHORS)
        top1 = top_k[0]

        # Matched controls for each anchor
        all_controls = []
        controls_per_anchor = {}
        for apos in top_k:
            ctrls, tier = build_matched_controls(protein, apos, seq, sse_features, pdb_features, proj_scores)
            controls_per_anchor[apos] = ctrls
            all_controls.extend(ctrls)
        # Deduplicate controls
        unique_controls = sorted(set(all_controls))

        # Contact map for G3
        contact_map, has_contacts = compute_pdb_contact_map(protein, seq)

        config = protein_configs.get(protein, {})

        n_ctrl_str = "/".join(str(len(controls_per_anchor[a])) for a in top_k)
        matched_info[protein] = {
            "top1": top1,
            "top3": top_k,
            "n_controls_per_anchor": n_ctrl_str,
        }

        protein_data[protein] = {
            "seq": seq, "sse_features": sse_features, "pdb_features": pdb_features,
            "proj_scores": proj_scores, "top_k": top_k, "top1": top1,
            "controls_per_anchor": controls_per_anchor, "unique_controls": unique_controls,
            "contact_map": contact_map, "has_contacts": has_contacts, "config": config,
        }

        print(f"  {protein}: top3={top_k}, controls={n_ctrl_str}, G3={'yes' if has_contacts else 'no'}")

    # --- Run influence tests ---
    print("\n=== Running influence tests ===")
    protein_results = []
    first_heatmap_data = None

    for protein, pd in protein_data.items():
        seq = pd["seq"]
        top1 = pd["top1"]
        top_k = pd["top_k"]
        config = pd["config"]
        contact_map = pd["contact_map"]

        # Collect all source positions
        all_sources = list(set(top_k + pd["unique_controls"]))

        # Build target sets for each source
        # G1 and G2 are source-dependent (G1 via separation, G2 excludes source)
        # G3 is source-dependent (different 3D contacts per source)

        # For efficiency, compute influence for all (source, target) pairs per target set
        # But targets differ per source in G1 and G3. For G2, targets are mostly the same.

        # Strategy: for each target set, build union of all targets across sources,
        # run one big influence call, then slice per source.

        result = {
            "protein": protein, "top1": top1, "top3": top_k,
            "control_positions": pd["unique_controls"],
            "top1_summaries": {},
            "top3_pooled_summaries": {},
            "control_summaries_by_set": {},
            "all_anchor_summaries": {},
            "all_control_summaries": {},
        }

        for g in TARGET_SETS:
            # Build per-source target lists
            source_targets = {}
            for src in all_sources:
                if g == "G1":
                    targets = build_g1_targets(src, len(seq))
                elif g == "G2":
                    if not config:
                        continue
                    targets = build_g2_targets(config, src, len(seq))
                elif g == "G3":
                    if not pd["has_contacts"]:
                        continue
                    targets = build_g3_targets(contact_map, src)
                    if len(targets) < 2:
                        continue
                else:
                    continue
                source_targets[src] = targets

            if not source_targets:
                continue

            # Union of all targets
            all_targets = sorted(set(t for tlist in source_targets.values() for t in tlist))
            # Sources that have targets
            active_sources = sorted(source_targets.keys())

            if not all_targets or not active_sources:
                continue

            n_pairs = len(active_sources) * len(all_targets)
            print(f"  {protein} {g}: {len(active_sources)} sources x {len(all_targets)} union targets ({n_pairs} pairs)")

            influence = compute_conditional_influence(esm_model, tokenizer, seq, active_sources, all_targets, device)

            # Slice per source to their specific targets
            for src in active_sources:
                src_targets = source_targets[src]
                src_influence = {t: influence[src][t] for t in src_targets if t in influence[src]}
                summary = summarize_influence_v2(src_influence)

                # Store
                store_key = f"{g}_{src}"
                if src in top_k:
                    result["all_anchor_summaries"][store_key] = summary
                if src in pd["unique_controls"]:
                    result["all_control_summaries"][store_key] = summary

            # Top-1 summary
            if top1 in source_targets:
                top1_inf = {t: influence[top1][t] for t in source_targets[top1] if t in influence[top1]}
                result["top1_summaries"][g] = summarize_influence_v2(top1_inf)

            # Top-3 pooled summary (mean of individual anchor summaries)
            anchor_summaries_g = []
            for apos in top_k:
                if apos in source_targets:
                    a_inf = {t: influence[apos][t] for t in source_targets[apos] if t in influence[apos]}
                    anchor_summaries_g.append(summarize_influence_v2(a_inf))
            if anchor_summaries_g:
                pooled = {}
                for metric in ["mean_influence", "top25_mean", "max_influence", "fraction_positive"]:
                    pooled[metric] = float(np.mean([s[metric] for s in anchor_summaries_g]))
                pooled["n_targets"] = sum(s["n_targets"] for s in anchor_summaries_g)
                pooled["median_influence"] = float(np.mean([s["median_influence"] for s in anchor_summaries_g]))
                pooled["n_above_threshold"] = sum(s["n_above_threshold"] for s in anchor_summaries_g)
                result["top3_pooled_summaries"][g] = pooled

            # Control summaries for this target set
            ctrl_summaries = []
            for cpos in pd["unique_controls"]:
                if cpos in source_targets:
                    c_inf = {t: influence[cpos][t] for t in source_targets[cpos] if t in influence[cpos]}
                    ctrl_summaries.append(summarize_influence_v2(c_inf))
            result["control_summaries_by_set"][g] = ctrl_summaries

            # Save heatmap data for first protein's G2
            if first_heatmap_data is None and g == "G2" and top1 in source_targets:
                hm_sources = [top1]
                if pd["unique_controls"]:
                    hm_sources.append(pd["unique_controls"][0])
                hm_data = {s: {t: influence[s].get(t, 0.0) for t in source_targets.get(s, all_targets)} for s in hm_sources if s in influence}
                hm_labels = {top1: f"ANCHOR ({top1})"}
                if pd["unique_controls"]:
                    hm_labels[pd["unique_controls"][0]] = f"ctrl ({pd['unique_controls'][0]})"
                first_heatmap_data = (hm_data, protein, hm_labels)

        protein_results.append(result)

    # --- Analyses ---
    print("\n=== Analyses ===")

    # Analysis 1: top-1 paired tests
    analysis1_paired = {}
    for g in TARGET_SETS:
        for metric in SUMMARY_METRICS:
            diffs = []
            for r in protein_results:
                if g not in r["top1_summaries"]:
                    continue
                ctrls = r["control_summaries_by_set"].get(g, [])
                if not ctrls:
                    continue
                a_val = r["top1_summaries"][g][metric]
                c_mean = np.mean([s[metric] for s in ctrls])
                diffs.append(a_val - c_mean)
            key = f"{g}_{metric}"
            analysis1_paired[key] = paired_test(diffs, key)
            pt = analysis1_paired[key]
            print(f"  A1 {key}: n={pt['n']}, d={pt['cohens_d']:.3f}, p={pt['t_p']:.4f}")

    # Analysis 2: top-3 pooled paired tests
    analysis2_paired = {}
    for g in TARGET_SETS:
        for metric in SUMMARY_METRICS:
            diffs = []
            for r in protein_results:
                if g not in r["top3_pooled_summaries"]:
                    continue
                ctrls = r["control_summaries_by_set"].get(g, [])
                if not ctrls:
                    continue
                a_val = r["top3_pooled_summaries"][g][metric]
                c_mean = np.mean([s[metric] for s in ctrls])
                diffs.append(a_val - c_mean)
            key = f"{g}_{metric}"
            analysis2_paired[key] = paired_test(diffs, key)
            pt = analysis2_paired[key]
            print(f"  A2 {key}: n={pt['n']}, d={pt['cohens_d']:.3f}, p={pt['t_p']:.4f}")

    # --- Plots ---
    print("\nGenerating plots...")
    plot_a_target_set_effects(analysis1_paired, analysis2_paired, REPORT_DIR)
    plot_b_per_protein(protein_results, REPORT_DIR)
    plot_c_top1_vs_top3(analysis1_paired, analysis2_paired, REPORT_DIR)
    if first_heatmap_data:
        hm_data, hm_protein, hm_labels = first_heatmap_data
        plot_d_heatmap(hm_data, hm_protein, hm_labels, "G2", REPORT_DIR)

    # --- Report ---
    print("\nGenerating report...")
    generate_report(protein_results, analysis1_paired, analysis2_paired, matched_info, REPORT_DIR)

    # --- CSV ---
    export_source_level_csv(protein_results, REPORT_DIR)

    # --- Summary ---
    print("\n=== Summary ===")
    for g in TARGET_SETS:
        key_mean = f"{g}_mean_influence"
        r1 = analysis1_paired.get(key_mean, {})
        r2 = analysis2_paired.get(key_mean, {})
        print(f"  {g} top-1: d={r1.get('cohens_d', np.nan):.3f}, p={r1.get('t_p', np.nan):.4f}")
        print(f"  {g} top-3: d={r2.get('cohens_d', np.nan):.3f}, p={r2.get('t_p', np.nan):.4f}")

    print("\nDone.")


if __name__ == "__main__":
    main()
