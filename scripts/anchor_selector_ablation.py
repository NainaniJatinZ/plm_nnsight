#!/usr/bin/env python3
"""Selector-direction ablation for anchor residues (experiments/3_29_steering_against.md).

Tests whether removing the d-component from a residue's layer-10 residual:
  1. suppresses its L10H9 anchor score / attention rank (selector validation)
  2. causes broader downstream disruption for anchors than matched controls (distal leverage)

For each of the 18 proteins:
  - identifies top-1 and top-3 anchors by projection score
  - finds matched non-anchor controls (same SSE, RSA, contacts_8A)
  - ablates d-component from LayerNorm output at layer 10
  - measures attention rank change (Analysis 1)
  - measures distal prediction disruption (Analysis 2)

Usage:
    uv run python scripts/anchor_selector_ablation.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F
from scipy import stats
from scipy.spatial.distance import cdist

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
REFERENCE_PROTEIN = "2B61A"
TOP_K_ANCHORS = 3
N_CONTROLS = 5
MIN_SEQ_SEP = 24
N_DISTANT_TARGETS = 16
N_BINS = 8
ABLATION_C = 1.0
POSITIVE_THRESHOLD = 0.01

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

TOLERANCE_TIERS = [
    (0.05, 3), (0.08, 3), (0.08, 5), (0.12, 5), (0.15, 8), (0.20, 10),
]


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


# ---------------------------------------------------------------------------
# Model + weights
# ---------------------------------------------------------------------------

def load_model(device: str):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager").to(device).eval()
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
# PDB features + SSE
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
# Matched controls
# ---------------------------------------------------------------------------

def build_matched_controls(
    protein: str, anchor_pos: int, sequence: str,
    sse_features: list[dict], pdb_features: dict | None,
    proj_scores: np.ndarray, n_controls: int = N_CONTROLS,
) -> list[int]:
    if pdb_features is None:
        return []
    anchor_sse_f = sse_features[anchor_pos]
    if anchor_sse_f is None:
        return []
    anchor_sse = anchor_sse_f["sse"]
    anchor_pdb = pdb_features.get(anchor_pos)
    if anchor_pdb is None:
        return []
    anchor_rsa = anchor_pdb["rsa"]
    anchor_c8 = anchor_pdb["contacts_8A"]
    proj_threshold = np.percentile(proj_scores, 90)
    n = len(sequence)
    rng = np.random.RandomState(abs(hash(f"{protein}_{anchor_pos}")) % (2**31))

    for rsa_tol, c8_tol in TOLERANCE_TIERS:
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
            return rng.choice(candidates, size=n_controls, replace=False).tolist()
    if candidates:
        return candidates[:n_controls]
    return []


# ---------------------------------------------------------------------------
# Anchor identification
# ---------------------------------------------------------------------------

def identify_top_k_anchors(proj_scores: np.ndarray, k: int = TOP_K_ANCHORS) -> list[int]:
    ranked = np.argsort(proj_scores)[::-1]
    return ranked[:k].tolist()


# ---------------------------------------------------------------------------
# Distant target selection
# ---------------------------------------------------------------------------

def build_distant_targets(source_pos: int, seq_len: int, n_targets: int = N_DISTANT_TARGETS) -> list[int]:
    eligible = [j for j in range(seq_len) if abs(j - source_pos) >= MIN_SEQ_SEP]
    if len(eligible) <= n_targets:
        return eligible
    bin_size = len(eligible) / n_targets
    return [eligible[int((i + 0.5) * bin_size)] for i in range(n_targets)]


# ---------------------------------------------------------------------------
# Analysis 1: clean vs ablated attention
# ---------------------------------------------------------------------------

@torch.no_grad()
def get_clean_attention(model, tokenizer, sequence: str, device: str) -> np.ndarray:
    """Return L10H9 attention matrix (n_res, n_res) for clean forward pass."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=[attn_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    attn_all = cache[key].output[1].detach().cpu()[0]  # (H, L, L)
    return attn_all[TARGET_HEAD, 1:-1, 1:-1].numpy()  # (n_res, n_res)


@torch.no_grad()
def get_ablated_attention(model, tokenizer, sequence: str, source_pos: int,
                          d_unit: torch.Tensor, c: float, device: str) -> np.ndarray:
    """Return L10H9 attention matrix after removing d-component at source_pos."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    seq_len_with_special = inputs["input_ids"].shape[1]
    j_tok = source_pos + 1  # +1 for BOS

    d_device = d_unit.to(device)
    pos_mask = torch.zeros(1, seq_len_with_special, 1, device=device)
    pos_mask[0, j_tok, 0] = c

    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            attn_cache = tracer.cache(modules=[attn_module])
            ln_out = ln_module.output
            proj_coeffs = (ln_out @ d_device).unsqueeze(-1)  # (1, L, 1)
            delta = pos_mask * proj_coeffs * d_device  # (1, L, 1280)
            ln_module.output = ln_out - delta

    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    attn_all = attn_cache[key].output[1].detach().cpu()[0]
    return attn_all[TARGET_HEAD, 1:-1, 1:-1].numpy()


def compute_attention_metrics(clean_attn: np.ndarray, ablated_attn: np.ndarray, source_pos: int) -> dict:
    """Compare attention rank of source_pos before and after ablation."""
    n_res = clean_attn.shape[0]
    clean_key_dist = clean_attn.mean(axis=0)  # mean over queries
    ablated_key_dist = ablated_attn.mean(axis=0)

    clean_rank = int(np.argsort(-clean_key_dist).tolist().index(source_pos)) if source_pos < n_res else n_res
    ablated_rank = int(np.argsort(-ablated_key_dist).tolist().index(source_pos)) if source_pos < n_res else n_res

    clean_mass = float(clean_key_dist[source_pos])
    ablated_mass = float(ablated_key_dist[source_pos])

    clean_top3 = set(np.argsort(-clean_key_dist)[:3].tolist())
    ablated_top3 = set(np.argsort(-ablated_key_dist)[:3].tolist())
    in_clean_top3 = source_pos in clean_top3
    in_ablated_top3 = source_pos in ablated_top3

    return {
        "clean_rank": clean_rank,
        "ablated_rank": ablated_rank,
        "rank_drop": ablated_rank - clean_rank,
        "clean_mass": clean_mass,
        "ablated_mass": ablated_mass,
        "mass_ratio": ablated_mass / clean_mass if clean_mass > 1e-8 else float("nan"),
        "in_clean_top3": in_clean_top3,
        "in_ablated_top3": in_ablated_top3,
        "lost_top3": in_clean_top3 and not in_ablated_top3,
    }


# ---------------------------------------------------------------------------
# Analysis 2: distal leverage
# ---------------------------------------------------------------------------

@torch.no_grad()
def get_baseline_logprobs(model, tokenizer, sequence: str, targets: list[int], device: str) -> dict[int, float]:
    """logP(true_t | mask_t, clean) for each target t."""
    mask_id = tokenizer.mask_token_id
    base_tokens = tokenizer(sequence, return_tensors="pt")["input_ids"][0]
    esm_model = model._model

    result = {}
    batch_ids = []
    for t in targets:
        ids = base_tokens.clone()
        ids[t + 1] = mask_id
        batch_ids.append(ids)

    batch = torch.stack(batch_ids).to(device)
    logits = esm_model(input_ids=batch).logits
    log_probs = F.log_softmax(logits, dim=-1)

    for idx, t in enumerate(targets):
        true_tok = base_tokens[t + 1].item()
        result[t] = log_probs[idx, t + 1, true_tok].item()

    return result


@torch.no_grad()
def get_ablated_logprobs(model, tokenizer, sequence: str, source_pos: int,
                         targets: list[int], d_unit: torch.Tensor, c: float,
                         device: str) -> dict[int, float]:
    """logP(true_t | mask_t, d-ablated at source_pos) for each target t."""
    mask_id = tokenizer.mask_token_id
    base_tokens = tokenizer(sequence, return_tensors="pt")["input_ids"][0]

    batch_ids = []
    for t in targets:
        ids = base_tokens.clone()
        ids[t + 1] = mask_id
        batch_ids.append(ids)

    batch = torch.stack(batch_ids).to(device)
    seq_len_with_special = batch.shape[1]
    j_tok = source_pos + 1
    n_batch = len(targets)

    d_device = d_unit.to(device)
    pos_mask = torch.zeros(n_batch, seq_len_with_special, 1, device=device)
    pos_mask[:, j_tok, 0] = c

    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(input_ids=batch):
            ln_out = ln_module.output
            proj_coeffs = (ln_out @ d_device).unsqueeze(-1)
            delta = pos_mask * proj_coeffs * d_device
            ln_module.output = ln_out - delta
            logits_save = model.output.logits.save()

    log_probs = F.log_softmax(logits_save.detach().cpu(), dim=-1)

    result = {}
    for idx, t in enumerate(targets):
        true_tok = base_tokens[t + 1].item()
        result[t] = log_probs[idx, t + 1, true_tok].item()

    return result


def summarize_distal_effects(baseline_logps: dict, ablated_logps: dict,
                             targets: list[int], seq_len: int) -> dict:
    """Compute distal leverage metrics for one source residue."""
    deltas = []
    target_deltas = {}
    for t in targets:
        if t in baseline_logps and t in ablated_logps:
            d = baseline_logps[t] - ablated_logps[t]
            deltas.append(d)
            target_deltas[t] = d

    if not deltas:
        return {"mean_delta": 0.0, "top25_mean_delta": 0.0, "max_delta": 0.0,
                "fraction_positive": 0.0, "n_bins_affected": 0, "affected_bin_entropy": 0.0,
                "n_targets": 0}

    arr = np.array(deltas)
    sorted_desc = np.sort(arr)[::-1]
    top25_k = max(1, len(arr) // 4)

    # Bin targets across the sequence and count affected bins
    bin_edges = np.linspace(0, seq_len, N_BINS + 1)
    bin_counts = np.zeros(N_BINS)
    for t, d in target_deltas.items():
        if d > POSITIVE_THRESHOLD:
            bin_idx = min(int(np.searchsorted(bin_edges[1:], t)), N_BINS - 1)
            bin_counts[bin_idx] += 1

    n_bins_affected = int((bin_counts > 0).sum())
    # Entropy of affected bin distribution
    if bin_counts.sum() > 0:
        p = bin_counts / bin_counts.sum()
        p = p[p > 0]
        affected_bin_entropy = float(-np.sum(p * np.log(p)))
    else:
        affected_bin_entropy = 0.0

    return {
        "mean_delta": float(arr.mean()),
        "top25_mean_delta": float(sorted_desc[:top25_k].mean()),
        "max_delta": float(arr.max()),
        "fraction_positive": float((arr > 0).sum() / len(arr)),
        "n_bins_affected": n_bins_affected,
        "affected_bin_entropy": affected_bin_entropy,
        "n_targets": len(deltas),
    }


# ---------------------------------------------------------------------------
# Per-protein processing
# ---------------------------------------------------------------------------

def process_protein(
    model, tokenizer, protein: str, sequence: str, config: dict,
    sse_str: str, d_unit: torch.Tensor, weights: dict, device: str,
) -> tuple[list[dict], list[dict]]:
    """Process one protein. Returns (source_rows, target_rows)."""
    n_res = len(sequence)
    print(f"  {protein} ({n_res} res)")

    # Projection scores and anchors
    proj_scores = capture_projection_scores(model, tokenizer, sequence, d_unit, device)
    anchor_positions = identify_top_k_anchors(proj_scores, TOP_K_ANCHORS)
    print(f"    top-3 anchors: {anchor_positions} (proj: {[f'{proj_scores[p]:.3f}' for p in anchor_positions]})")

    # PDB + SSE features for matched controls
    pdb_features = compute_pdb_features(protein, sequence)
    sse_features = compute_sse_features(sse_str)

    # Build matched controls for top-1 anchor
    top1_pos = anchor_positions[0]
    controls = build_matched_controls(protein, top1_pos, sequence, sse_features, pdb_features, proj_scores)
    if not controls:
        print(f"    WARNING: no matched controls found for {protein}, skipping")
        return [], []
    print(f"    matched controls: {controls[:3]}... ({len(controls)} total)")

    # All source positions
    sources = anchor_positions + controls
    source_labels = {}
    for i, pos in enumerate(anchor_positions):
        source_labels[pos] = f"anchor_top{i+1}"
    for pos in controls:
        source_labels[pos] = "control"

    # Analysis 1: clean attention
    clean_attn = get_clean_attention(model, tokenizer, sequence, device)

    source_rows = []
    target_rows = []

    for src_idx, src_pos in enumerate(sources):
        label = source_labels[src_pos]
        is_anchor = label.startswith("anchor")

        # Analysis 1: ablated attention
        ablated_attn = get_ablated_attention(model, tokenizer, sequence, src_pos, d_unit, ABLATION_C, device)
        attn_metrics = compute_attention_metrics(clean_attn, ablated_attn, src_pos)

        # Analysis 2: distant targets specific to this source
        targets = build_distant_targets(src_pos, n_res)
        if not targets:
            print(f"    WARNING: no distant targets for pos {src_pos}, skipping")
            continue

        baseline_logps = get_baseline_logprobs(model, tokenizer, sequence, targets, device)
        ablated_logps = get_ablated_logprobs(model, tokenizer, sequence, src_pos, targets, d_unit, ABLATION_C, device)
        distal_metrics = summarize_distal_effects(baseline_logps, ablated_logps, targets, n_res)

        row = {
            "protein": protein,
            "source_pos": src_pos,
            "source_label": label,
            "is_anchor": int(is_anchor),
            "proj_score": float(proj_scores[src_pos]),
            "aa": sequence[src_pos] if src_pos < n_res else "?",
        }
        row.update({f"attn_{k}": v for k, v in attn_metrics.items()})
        row.update({f"distal_{k}": v for k, v in distal_metrics.items()})
        source_rows.append(row)

        # Target-level rows
        for t in targets:
            if t in baseline_logps and t in ablated_logps:
                target_rows.append({
                    "protein": protein,
                    "source_pos": src_pos,
                    "source_label": label,
                    "is_anchor": int(is_anchor),
                    "target_pos": t,
                    "seq_sep": abs(src_pos - t),
                    "baseline_logp": baseline_logps[t],
                    "ablated_logp": ablated_logps[t],
                    "delta": baseline_logps[t] - ablated_logps[t],
                })

        if (src_idx + 1) % 4 == 0:
            print(f"    processed {src_idx + 1}/{len(sources)} sources")

    return source_rows, target_rows


# ---------------------------------------------------------------------------
# Aggregation and reporting
# ---------------------------------------------------------------------------

def aggregate_results(all_source_rows: list[dict]) -> dict:
    """Aggregate source-level results into protein-level comparisons."""
    proteins = sorted(set(r["protein"] for r in all_source_rows))
    analysis = {"top1_vs_ctrl": [], "top3_vs_ctrl": [], "proteins": {}}

    for protein in proteins:
        prows = [r for r in all_source_rows if r["protein"] == protein]
        anchors = [r for r in prows if r["is_anchor"]]
        controls = [r for r in prows if not r["is_anchor"]]
        if not anchors or not controls:
            continue

        top1 = [r for r in anchors if r["source_label"] == "anchor_top1"]
        ctrl_means = {}
        for metric in ["distal_mean_delta", "distal_top25_mean_delta", "distal_max_delta",
                       "distal_fraction_positive", "distal_n_bins_affected", "distal_affected_bin_entropy",
                       "attn_rank_drop", "attn_mass_ratio"]:
            ctrl_vals = [r[metric] for r in controls if metric in r and not np.isnan(r.get(metric, float("nan")))]
            ctrl_means[metric] = np.mean(ctrl_vals) if ctrl_vals else 0.0

        protein_result = {"protein": protein, "n_anchors": len(anchors), "n_controls": len(controls)}

        # Top-1 vs controls
        if top1:
            t1 = top1[0]
            for metric in ctrl_means:
                t1_val = t1.get(metric, 0.0)
                protein_result[f"top1_{metric}"] = t1_val
                protein_result[f"ctrl_mean_{metric}"] = ctrl_means[metric]
                protein_result[f"top1_minus_ctrl_{metric}"] = t1_val - ctrl_means[metric]

        # Top-3 mean vs controls
        for metric in ctrl_means:
            anch_vals = [r[metric] for r in anchors if metric in r and not np.isnan(r.get(metric, float("nan")))]
            anch_mean = np.mean(anch_vals) if anch_vals else 0.0
            protein_result[f"top3_mean_{metric}"] = anch_mean
            protein_result[f"top3_minus_ctrl_{metric}"] = anch_mean - ctrl_means[metric]

        analysis["proteins"][protein] = protein_result

    return analysis


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

def plot_results(all_source_rows: list[dict], analysis: dict, output_dir: Path):
    C_ANCHOR = "#D64550"
    C_CTRL = "#5B7FA3"

    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
        "figure.dpi": 200,
    })

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Panel A: Attention rank drop (anchor vs control)
    ax = axes[0, 0]
    anchors = [r for r in all_source_rows if r["is_anchor"]]
    controls = [r for r in all_source_rows if not r["is_anchor"]]
    a_drops = [r["attn_rank_drop"] for r in anchors]
    c_drops = [r["attn_rank_drop"] for r in controls]
    bp = ax.boxplot([a_drops, c_drops], labels=["Anchors", "Controls"], patch_artist=True)
    bp["boxes"][0].set_facecolor(C_ANCHOR)
    bp["boxes"][0].set_alpha(0.6)
    bp["boxes"][1].set_facecolor(C_CTRL)
    bp["boxes"][1].set_alpha(0.6)
    ax.set_ylabel("Attention rank drop (higher = more suppression)")
    ax.set_title("A. d-ablation suppresses anchor attention rank")
    ax.axhline(0, color="gray", ls=":", lw=0.7)

    # Panel B: top25_mean_delta (anchor vs control)
    ax = axes[0, 1]
    a_vals = [r["distal_top25_mean_delta"] for r in anchors]
    c_vals = [r["distal_top25_mean_delta"] for r in controls]
    bp = ax.boxplot([a_vals, c_vals], labels=["Anchors", "Controls"], patch_artist=True)
    bp["boxes"][0].set_facecolor(C_ANCHOR)
    bp["boxes"][0].set_alpha(0.6)
    bp["boxes"][1].set_facecolor(C_CTRL)
    bp["boxes"][1].set_alpha(0.6)
    ax.set_ylabel("Top-25% mean delta (nats)")
    ax.set_title("B. Distal leverage: top-25% mean delta")
    ax.axhline(0, color="gray", ls=":", lw=0.7)

    # Panel C: n_bins_affected (anchor vs control)
    ax = axes[1, 0]
    a_bins = [r["distal_n_bins_affected"] for r in anchors]
    c_bins = [r["distal_n_bins_affected"] for r in controls]
    bp = ax.boxplot([a_bins, c_bins], labels=["Anchors", "Controls"], patch_artist=True)
    bp["boxes"][0].set_facecolor(C_ANCHOR)
    bp["boxes"][0].set_alpha(0.6)
    bp["boxes"][1].set_facecolor(C_CTRL)
    bp["boxes"][1].set_alpha(0.6)
    ax.set_ylabel("Number of sequence bins affected")
    ax.set_title("C. Distal leverage: breadth of disruption")

    # Panel D: top-1 vs top-3 comparison per protein
    ax = axes[1, 1]
    proteins_data = analysis.get("proteins", {})
    if proteins_data:
        pnames = sorted(proteins_data.keys())
        top1_vals = [proteins_data[p].get("top1_minus_ctrl_distal_top25_mean_delta", 0) for p in pnames]
        top3_vals = [proteins_data[p].get("top3_minus_ctrl_distal_top25_mean_delta", 0) for p in pnames]
        x = np.arange(len(pnames))
        w = 0.35
        ax.bar(x - w/2, top1_vals, w, label="Top-1", color=C_ANCHOR, alpha=0.7)
        ax.bar(x + w/2, top3_vals, w, label="Top-3 mean", color="#61afef", alpha=0.7)
        ax.set_xticks(x)
        ax.set_xticklabels(pnames, rotation=60, ha="right", fontsize=6)
        ax.axhline(0, color="gray", ls=":", lw=0.7)
        ax.set_ylabel("Anchor - control difference")
        ax.set_title("D. Per-protein anchor advantage (top25 mean delta)")
        ax.legend()

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = output_dir / "anchor_selector_ablation.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_report(all_source_rows: list[dict], analysis: dict, output_dir: Path):
    anchors = [r for r in all_source_rows if r["is_anchor"]]
    controls = [r for r in all_source_rows if not r["is_anchor"]]

    proteins_data = analysis.get("proteins", {})
    n_proteins = len(proteins_data)

    report = []
    report.append("# Selector-Direction Ablation for Anchor Residues\n\n")
    report.append(f"Proteins analyzed: {n_proteins}.\n")
    report.append(f"Ablation strength: c = {ABLATION_C}.\n")
    report.append(f"Anchors: top-{TOP_K_ANCHORS} by projection score. Controls: {N_CONTROLS} matched on SSE/RSA/contacts_8A.\n")
    report.append(f"Distant targets: {N_DISTANT_TARGETS} per source, |i-j| >= {MIN_SEQ_SEP}.\n\n")

    # Analysis 1 summary
    report.append("## Analysis 1: Selector validation\n\n")
    a_drops = [r["attn_rank_drop"] for r in anchors]
    c_drops = [r["attn_rank_drop"] for r in controls]
    a_lost = sum(1 for r in anchors if r.get("attn_lost_top3"))
    a_total = len(anchors)
    report.append(f"Mean rank drop: anchors = {np.mean(a_drops):.1f}, controls = {np.mean(c_drops):.1f}.\n")
    report.append(f"Anchors losing top-3 status: {a_lost}/{a_total} ({100*a_lost/a_total:.0f}%).\n")

    a_mass_ratios = [r["attn_mass_ratio"] for r in anchors if not np.isnan(r.get("attn_mass_ratio", float("nan")))]
    c_mass_ratios = [r["attn_mass_ratio"] for r in controls if not np.isnan(r.get("attn_mass_ratio", float("nan")))]
    if a_mass_ratios:
        report.append(f"Mean mass ratio (ablated/clean): anchors = {np.mean(a_mass_ratios):.3f}, controls = {np.mean(c_mass_ratios):.3f}.\n")
    report.append("\n")

    # Analysis 2 summary
    report.append("## Analysis 2: Distal leverage\n\n")
    metrics_to_report = [
        ("distal_top25_mean_delta", "Top-25% mean delta"),
        ("distal_n_bins_affected", "Bins affected"),
        ("distal_fraction_positive", "Fraction positive"),
        ("distal_affected_bin_entropy", "Affected bin entropy"),
        ("distal_mean_delta", "Mean delta"),
    ]

    report.append("| Metric | Anchors (mean) | Controls (mean) | Diff | t-test p | Wilcoxon p |\n")
    report.append("|--------|---------------|-----------------|------|----------|------------|\n")

    for metric_key, metric_label in metrics_to_report:
        a_vals = [r[metric_key] for r in anchors if metric_key in r]
        c_vals = [r[metric_key] for r in controls if metric_key in r]
        a_mean = np.mean(a_vals) if a_vals else 0.0
        c_mean = np.mean(c_vals) if c_vals else 0.0
        # Per-protein paired differences
        diffs = []
        for p in proteins_data:
            d = proteins_data[p].get(f"top1_minus_ctrl_{metric_key}", None)
            if d is not None:
                diffs.append(d)
        test = paired_test(diffs, metric_label) if diffs else {"t_p": np.nan, "wilcoxon_p": np.nan}
        report.append(f"| {metric_label} | {a_mean:.4f} | {c_mean:.4f} | {a_mean - c_mean:.4f} | {test['t_p']:.4f} | {test['wilcoxon_p']:.4f} |\n")
    report.append("\n")

    # Top-1 vs Top-3
    report.append("## Top-1 vs Top-3 comparison\n\n")
    report.append("| Metric | Top-1 mean diff | Top-3 mean diff |\n")
    report.append("|--------|----------------|----------------|\n")
    for metric_key, metric_label in metrics_to_report:
        top1_diffs = [proteins_data[p].get(f"top1_minus_ctrl_{metric_key}", 0) for p in proteins_data]
        top3_diffs = [proteins_data[p].get(f"top3_minus_ctrl_{metric_key}", 0) for p in proteins_data]
        report.append(f"| {metric_label} | {np.mean(top1_diffs):.4f} | {np.mean(top3_diffs):.4f} |\n")
    report.append("\n")

    # Per-protein table
    report.append("## Per-protein results\n\n")
    report.append("| Protein | Top-1 rank drop | Top-1 top25 delta | Ctrl mean top25 delta | Diff |\n")
    report.append("|---------|----------------|-------------------|----------------------|------|\n")
    for p in sorted(proteins_data):
        pd = proteins_data[p]
        rd = pd.get("top1_distal_top25_mean_delta", 0)
        cd = pd.get("ctrl_mean_distal_top25_mean_delta", 0)
        rdrop = pd.get("top1_attn_rank_drop", 0)
        report.append(f"| {p} | {rdrop:.0f} | {rd:.4f} | {cd:.4f} | {rd - cd:.4f} |\n")
    report.append("\n")

    report.append("![Results](anchor_selector_ablation.png)\n\n")

    out = output_dir / "anchor_selector_ablation.md"
    with open(out, "w") as f:
        f.writelines(report)
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
    protein_configs, all_seqs, ss_dict = load_configs()

    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    # Process each known anchor protein
    proteins_to_run = [p for p in ANCHOR_POSITIONS if p in all_seqs and p in ss_dict]
    print(f"\nProcessing {len(proteins_to_run)} proteins...\n")

    all_source_rows = []
    all_target_rows = []
    t0 = time.time()

    for protein in proteins_to_run:
        sequence = all_seqs[protein]
        config = protein_configs.get(protein, {})
        sse_str = ss_dict.get(protein, "C" * len(sequence))

        try:
            source_rows, target_rows = process_protein(
                model, tokenizer, protein, sequence, config, sse_str,
                d_unit, weights, args.device,
            )
            all_source_rows.extend(source_rows)
            all_target_rows.extend(target_rows)
        except Exception as e:
            print(f"  ERROR on {protein}: {e}")
            import traceback
            traceback.print_exc()
            continue

    elapsed = time.time() - t0
    print(f"\nProcessed {len(proteins_to_run)} proteins in {elapsed:.0f}s")
    print(f"  {len(all_source_rows)} source rows, {len(all_target_rows)} target rows")

    if not all_source_rows:
        print("No results to report.")
        return

    # Save CSVs
    source_csv = REPORT_DIR / "anchor_selector_ablation_source_level.csv"
    if all_source_rows:
        fields = list(all_source_rows[0].keys())
        with open(source_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_source_rows)
        print(f"  Saved: {source_csv}")

    target_csv = REPORT_DIR / "anchor_selector_ablation_target_level.csv"
    if all_target_rows:
        fields = list(all_target_rows[0].keys())
        with open(target_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_target_rows)
        print(f"  Saved: {target_csv}")

    # Aggregate and report
    print("\nAggregating results...")
    analysis = aggregate_results(all_source_rows)

    print("Generating plots...")
    plot_results(all_source_rows, analysis, REPORT_DIR)

    print("Writing report...")
    write_report(all_source_rows, analysis, REPORT_DIR)

    print("\nDone.")


if __name__ == "__main__":
    main()
