#!/usr/bin/env python3
"""Affected-target characterization after selector ablation (experiments/3_30_steering_against_v2.md).

Characterizes which target residues are most disrupted by d-ablation of anchor sites,
and tests whether they are enriched for direct 3D contacts, contact-graph neighbors,
shared contact neighborhoods, and cross-SSE relationships.

Reuses model loading, search direction, ablation logic, and matched controls from
anchor_selector_ablation.py.

Usage:
    uv run python scripts/anchor_target_characterization.py --device cuda
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
CONTACT_CUTOFF = 8.0
TOP_K_AFFECTED = 4

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
# Data loading (from anchor_selector_ablation.py)
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
# Model + weights (from anchor_selector_ablation.py)
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
# PDB features + contact map + graph distance
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


def compute_pdb_features_extended(protein: str, full_seq: str) -> dict | None:
    """Extended PDB features: RSA, contacts, contact map, CB distance matrix, graph distance, contact neighbors."""
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
    contact_matrix = dists < CONTACT_CUTOFF
    np.fill_diagonal(contact_matrix, False)
    contacts_8A = contact_matrix.sum(axis=1)

    # Build seq_pos -> pdb_idx reverse mapping
    seq_to_pdb = {seq_pos: pdb_idx for pdb_idx, seq_pos in mapping.items()}

    # Graph distance via BFS on contact matrix
    n_pdb = len(pdb_residues_raw)
    adjacency = [[] for _ in range(n_pdb)]
    for i in range(n_pdb):
        for j in range(i + 1, n_pdb):
            if contact_matrix[i, j]:
                adjacency[i].append(j)
                adjacency[j].append(i)

    def bfs_distances(start: int) -> dict[int, int]:
        visited = {start: 0}
        queue = [start]
        while queue:
            next_queue = []
            for node in queue:
                for neighbor in adjacency[node]:
                    if neighbor not in visited:
                        visited[neighbor] = visited[node] + 1
                        next_queue.append(neighbor)
            queue = next_queue
        return visited

    # Precompute contact neighbor sets (in seq_pos space)
    contact_neighbors = {}
    for pdb_idx, seq_pos in mapping.items():
        neighbors = set()
        for j in range(n_pdb):
            if contact_matrix[pdb_idx, j] and j in {pi for pi, sp in mapping.items()}:
                j_seq = mapping.get(j)
                if j_seq is not None:
                    neighbors.add(j_seq)
        contact_neighbors[seq_pos] = neighbors

    # Per-residue features
    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_residues_raw[pdb_idx]
        max_asa = MAX_ASA.get(r["aa"], 200)
        raw_sasa = sasa_by_resid.get(r["resid"], 0.0)
        rsa = min(raw_sasa / max_asa, 1.0) if max_asa > 0 else 0.0
        features[seq_pos] = {
            "rsa": round(rsa, 4),
            "contacts_8A": int(contacts_8A[pdb_idx]),
            "pdb_idx": pdb_idx,
        }

    return {
        "per_residue": features,
        "contact_matrix": contact_matrix,
        "mapping": mapping,
        "seq_to_pdb": seq_to_pdb,
        "bfs_distances": bfs_distances,
        "contact_neighbors": contact_neighbors,
        "n_pdb": n_pdb,
    }


def compute_sse_features(sse_str: str) -> list[dict]:
    n = len(sse_str)
    features = [None] * n
    seg_id = 0
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
                "seg_id": seg_id,
                "dist_to_boundary": min(dist_left, dist_right),
            }
        seg_id += 1
        i = j
    return features


# ---------------------------------------------------------------------------
# EVcoupling loading
# ---------------------------------------------------------------------------

def load_evcouplings(protein: str) -> dict[tuple[int, int], float] | None:
    """Load EVcoupling scores for a protein. Returns dict mapping (i, j) 1-indexed pairs to score."""
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    # Find the TARGET_b* subdirectory
    target_dirs = sorted(ev_dir.glob("TARGET_b*"))
    if not target_dirs:
        return None
    target_dir = target_dirs[0]
    coupling_dir = target_dir / "couplings"
    if not coupling_dir.exists():
        return None
    # Find the CouplingScores file
    candidates = sorted(coupling_dir.glob("*CouplingScores_longrange.csv"))
    if not candidates:
        candidates = sorted(coupling_dir.glob("*CouplingScores*.csv"))
    if not candidates:
        return None
    csv_path = candidates[0]
    couplings = {}
    try:
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                i = int(row["i"])
                j = int(row["j"])
                score = float(row["score"])
                couplings[(i, j)] = score
                couplings[(j, i)] = score
    except Exception as e:
        print(f"    WARNING: could not load EVcouplings for {protein}: {e}")
        return None
    print(f"    Loaded {len(couplings)//2} EVcoupling pairs from {csv_path.name}")
    return couplings


def get_ev_score(couplings: dict | None, source_pos: int, target_pos: int, pdb_features: dict) -> float | None:
    """Get EVcoupling score for a source-target pair. Positions are 0-indexed seq positions; EVcouplings are 1-indexed PDB residue IDs."""
    if couplings is None:
        return None
    # Map seq positions to PDB residue IDs (1-indexed)
    seq_to_pdb = pdb_features["seq_to_pdb"]
    mapping = pdb_features["mapping"]
    if source_pos not in seq_to_pdb or target_pos not in seq_to_pdb:
        return None
    # Get the original PDB residue IDs
    from_raw = pdb_features  # we need the raw PDB residue data
    # The mapping is pdb_idx -> seq_pos, and we stored pdb_idx in per_residue features
    src_pdb_idx = seq_to_pdb[source_pos]
    tgt_pdb_idx = seq_to_pdb[target_pos]
    # EVcouplings use 1-indexed positions in the alignment, which typically map to PDB residue numbering
    # The CSV has columns i, j which are 1-indexed positions
    # We'll try both the pdb_idx+1 mapping and direct lookup
    score = couplings.get((src_pdb_idx + 1, tgt_pdb_idx + 1))
    if score is not None:
        return score
    # Also try with the position indices directly (0-indexed + 1)
    score = couplings.get((source_pos + 1, target_pos + 1))
    return score


# ---------------------------------------------------------------------------
# Matched controls (from anchor_selector_ablation.py)
# ---------------------------------------------------------------------------

def build_matched_controls(
    protein: str, anchor_pos: int, sequence: str,
    sse_features: list[dict], pdb_features: dict | None,
    proj_scores: np.ndarray, n_controls: int = N_CONTROLS,
) -> list[int]:
    if pdb_features is None:
        return []
    per_res = pdb_features["per_residue"]
    anchor_sse_f = sse_features[anchor_pos]
    if anchor_sse_f is None:
        return []
    anchor_sse = anchor_sse_f["sse"]
    anchor_pdb = per_res.get(anchor_pos)
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
            pf = per_res.get(pos)
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


def identify_top_k_anchors(proj_scores: np.ndarray, k: int = TOP_K_ANCHORS) -> list[int]:
    ranked = np.argsort(proj_scores)[::-1]
    return ranked[:k].tolist()


def build_distant_targets(source_pos: int, seq_len: int, n_targets: int = N_DISTANT_TARGETS) -> list[int]:
    eligible = [j for j in range(seq_len) if abs(j - source_pos) >= MIN_SEQ_SEP]
    if len(eligible) <= n_targets:
        return eligible
    bin_size = len(eligible) / n_targets
    return [eligible[int((i + 0.5) * bin_size)] for i in range(n_targets)]


# ---------------------------------------------------------------------------
# Ablation and logprob functions (from anchor_selector_ablation.py)
# ---------------------------------------------------------------------------

@torch.no_grad()
def get_baseline_logprobs(model, tokenizer, sequence: str, targets: list[int], device: str) -> dict[int, float]:
    mask_id = tokenizer.mask_token_id
    base_tokens = tokenizer(sequence, return_tensors="pt")["input_ids"][0]
    esm_model = model._model
    batch_ids = []
    for t in targets:
        ids = base_tokens.clone()
        ids[t + 1] = mask_id
        batch_ids.append(ids)
    batch = torch.stack(batch_ids).to(device)
    logits = esm_model(input_ids=batch).logits
    log_probs = F.log_softmax(logits, dim=-1)
    result = {}
    for idx, t in enumerate(targets):
        true_tok = base_tokens[t + 1].item()
        result[t] = log_probs[idx, t + 1, true_tok].item()
    return result


@torch.no_grad()
def get_ablated_logprobs(model, tokenizer, sequence: str, source_pos: int,
                         targets: list[int], d_unit: torch.Tensor, c: float,
                         device: str) -> dict[int, float]:
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


# ---------------------------------------------------------------------------
# Target-level annotation
# ---------------------------------------------------------------------------

def annotate_target(source_pos: int, target_pos: int, sse_features: list[dict],
                    pdb_features: dict | None, evcouplings: dict | None) -> dict:
    """Compute all target-level annotations for a source-target pair."""
    annot = {}

    # 1. Sequence relationship
    seq_sep = abs(source_pos - target_pos)
    annot["seq_sep"] = seq_sep
    src_sse = sse_features[source_pos] if source_pos < len(sse_features) else None
    tgt_sse = sse_features[target_pos] if target_pos < len(sse_features) else None

    # 2. Structural relationship
    if pdb_features is not None:
        seq_to_pdb = pdb_features["seq_to_pdb"]
        src_pdb = seq_to_pdb.get(source_pos)
        tgt_pdb = seq_to_pdb.get(target_pos)
        if src_pdb is not None and tgt_pdb is not None:
            annot["direct_contact_8A"] = int(pdb_features["contact_matrix"][src_pdb, tgt_pdb])
            # Graph distance
            bfs = pdb_features["bfs_distances"](src_pdb)
            graph_dist = bfs.get(tgt_pdb, -1)
            annot["graph_distance"] = graph_dist if graph_dist >= 0 else 999
            annot["same_contact_component"] = int(graph_dist >= 0)
        else:
            annot["direct_contact_8A"] = -1
            annot["graph_distance"] = -1
            annot["same_contact_component"] = -1

        # 4. Contact-neighborhood overlap
        src_neighbors = pdb_features["contact_neighbors"].get(source_pos, set())
        tgt_neighbors = pdb_features["contact_neighbors"].get(target_pos, set())
        if src_neighbors or tgt_neighbors:
            shared = src_neighbors & tgt_neighbors
            union = src_neighbors | tgt_neighbors
            annot["shared_contact_partners"] = len(shared)
            annot["jaccard_overlap"] = len(shared) / len(union) if union else 0.0
        else:
            annot["shared_contact_partners"] = 0
            annot["jaccard_overlap"] = 0.0
    else:
        annot["direct_contact_8A"] = -1
        annot["graph_distance"] = -1
        annot["same_contact_component"] = -1
        annot["shared_contact_partners"] = 0
        annot["jaccard_overlap"] = 0.0

    # 3. SSE relationship
    if src_sse is not None and tgt_sse is not None:
        annot["same_sse_type"] = int(src_sse["sse"] == tgt_sse["sse"])
        annot["same_sse_segment"] = int(src_sse["seg_id"] == tgt_sse["seg_id"])
        annot["different_sse_same_type"] = int(src_sse["sse"] == tgt_sse["sse"] and src_sse["seg_id"] != tgt_sse["seg_id"])
        annot["different_sse_different_type"] = int(src_sse["sse"] != tgt_sse["sse"])
        annot["source_sse"] = src_sse["sse"]
        annot["target_sse"] = tgt_sse["sse"]
        annot["source_seg_id"] = src_sse["seg_id"]
        annot["target_seg_id"] = tgt_sse["seg_id"]
    else:
        annot["same_sse_type"] = -1
        annot["same_sse_segment"] = -1
        annot["different_sse_same_type"] = -1
        annot["different_sse_different_type"] = -1
        annot["source_sse"] = "?"
        annot["target_sse"] = "?"
        annot["source_seg_id"] = -1
        annot["target_seg_id"] = -1

    # 5. EVcoupling score
    if evcouplings is not None and pdb_features is not None:
        ev_score = get_ev_score(evcouplings, source_pos, target_pos, pdb_features)
        annot["ev_score"] = ev_score if ev_score is not None else float("nan")
    else:
        annot["ev_score"] = float("nan")

    return annot


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

    # Extended PDB features (contact map, graph distance, contact neighbors)
    pdb_features = compute_pdb_features_extended(protein, sequence)
    sse_features = compute_sse_features(sse_str)

    # EVcouplings
    evcouplings = load_evcouplings(protein)

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

    source_rows = []
    target_rows = []

    for src_idx, src_pos in enumerate(sources):
        label = source_labels[src_pos]
        is_anchor = label.startswith("anchor")

        # Distant targets for this source
        targets = build_distant_targets(src_pos, n_res)
        if not targets:
            print(f"    WARNING: no distant targets for pos {src_pos}, skipping")
            continue

        baseline_logps = get_baseline_logprobs(model, tokenizer, sequence, targets, device)
        ablated_logps = get_ablated_logprobs(model, tokenizer, sequence, src_pos, targets, d_unit, ABLATION_C, device)

        # Compute deltas and identify affected targets
        target_deltas = {}
        for t in targets:
            if t in baseline_logps and t in ablated_logps:
                target_deltas[t] = baseline_logps[t] - ablated_logps[t]

        if not target_deltas:
            continue

        all_deltas = np.array(list(target_deltas.values()))
        affected_threshold = [t for t, d in target_deltas.items() if d > POSITIVE_THRESHOLD]
        sorted_by_delta = sorted(target_deltas.items(), key=lambda x: -x[1])
        top_k_affected = [t for t, _ in sorted_by_delta[:TOP_K_AFFECTED]]

        # Source-level summary
        n_distinct_sse_segments = len(set(
            sse_features[t]["seg_id"] for t in affected_threshold
            if t < len(sse_features) and sse_features[t] is not None
        ))

        # Structural annotations for affected vs all targets
        affected_annots = []
        all_annots = []
        for t in targets:
            if t not in target_deltas:
                continue
            annot = annotate_target(src_pos, t, sse_features, pdb_features, evcouplings)
            annot_with_delta = {**annot, "delta": target_deltas[t], "affected_threshold": int(t in affected_threshold), "affected_topk": int(t in top_k_affected)}
            all_annots.append(annot_with_delta)
            if t in affected_threshold:
                affected_annots.append(annot_with_delta)

        # Compute source-level enrichment metrics
        def safe_mean(vals, key):
            valid = [v[key] for v in vals if v.get(key, -1) >= 0]
            return np.mean(valid) if valid else float("nan")

        def safe_frac(vals, key, value=1):
            valid = [v[key] for v in vals if v.get(key, -1) >= 0]
            return np.mean([v == value for v in valid]) if valid else float("nan")

        row = {
            "protein": protein,
            "source_pos": src_pos,
            "source_label": label,
            "is_anchor": int(is_anchor),
            "proj_score": float(proj_scores[src_pos]),
            "aa": sequence[src_pos] if src_pos < n_res else "?",
            "n_targets": len(target_deltas),
            "n_affected_threshold": len(affected_threshold),
            "mean_delta": float(all_deltas.mean()),
            "max_delta": float(all_deltas.max()),
            "fraction_positive": float((all_deltas > 0).sum() / len(all_deltas)),
            "n_distinct_sse_segments_affected": n_distinct_sse_segments,
            # Enrichment: all targets
            "all_frac_direct_contact": safe_frac(all_annots, "direct_contact_8A"),
            "all_mean_graph_distance": safe_mean(all_annots, "graph_distance"),
            "all_frac_same_sse_segment": safe_frac(all_annots, "same_sse_segment"),
            "all_frac_different_sse": safe_frac(all_annots, "different_sse_different_type"),
            "all_mean_jaccard_overlap": safe_mean(all_annots, "jaccard_overlap"),
            "all_mean_shared_contacts": safe_mean(all_annots, "shared_contact_partners"),
            # Enrichment: affected targets (threshold)
            "aff_frac_direct_contact": safe_frac(affected_annots, "direct_contact_8A") if affected_annots else float("nan"),
            "aff_mean_graph_distance": safe_mean(affected_annots, "graph_distance") if affected_annots else float("nan"),
            "aff_frac_same_sse_segment": safe_frac(affected_annots, "same_sse_segment") if affected_annots else float("nan"),
            "aff_frac_different_sse": safe_frac(affected_annots, "different_sse_different_type") if affected_annots else float("nan"),
            "aff_mean_jaccard_overlap": safe_mean(affected_annots, "jaccard_overlap") if affected_annots else float("nan"),
            "aff_mean_shared_contacts": safe_mean(affected_annots, "shared_contact_partners") if affected_annots else float("nan"),
        }

        # EVcoupling enrichment if available
        ev_all = [a["ev_score"] for a in all_annots if not np.isnan(a.get("ev_score", float("nan")))]
        ev_aff = [a["ev_score"] for a in affected_annots if not np.isnan(a.get("ev_score", float("nan")))]
        row["ev_mean_all"] = float(np.mean(ev_all)) if ev_all else float("nan")
        row["ev_mean_affected"] = float(np.mean(ev_aff)) if ev_aff else float("nan")

        source_rows.append(row)

        # Target-level rows
        for t in targets:
            if t not in target_deltas:
                continue
            annot = annotate_target(src_pos, t, sse_features, pdb_features, evcouplings)
            target_rows.append({
                "protein": protein,
                "source_pos": src_pos,
                "source_label": label,
                "is_anchor": int(is_anchor),
                "target_pos": t,
                "baseline_logp": baseline_logps[t],
                "ablated_logp": ablated_logps[t],
                "delta": target_deltas[t],
                "affected_threshold": int(target_deltas[t] > POSITIVE_THRESHOLD),
                "affected_topk": int(t in top_k_affected),
                **annot,
            })

        if (src_idx + 1) % 4 == 0:
            print(f"    processed {src_idx + 1}/{len(sources)} sources")

    return source_rows, target_rows


# ---------------------------------------------------------------------------
# Aggregation and analyses
# ---------------------------------------------------------------------------

def run_analyses(all_source_rows: list[dict], all_target_rows: list[dict]) -> dict:
    """Run all analyses from the experiment spec."""
    results = {}

    # Analysis 1: What kinds of targets are affected?
    anchor_rows = [r for r in all_target_rows if r["is_anchor"]]
    control_rows = [r for r in all_target_rows if not r["is_anchor"]]

    def compute_target_profile(rows: list[dict], affected_only: bool = False) -> dict:
        if affected_only:
            rows = [r for r in rows if r.get("affected_threshold")]
        valid_contact = [r for r in rows if r.get("direct_contact_8A", -1) >= 0]
        valid_graph = [r for r in rows if r.get("graph_distance", -1) >= 0 and r["graph_distance"] < 999]
        valid_sse = [r for r in rows if r.get("same_sse_segment", -1) >= 0]
        valid_jaccard = [r for r in rows if r.get("jaccard_overlap", -1) >= 0]
        return {
            "n": len(rows),
            "frac_direct_contact": np.mean([r["direct_contact_8A"] for r in valid_contact]) if valid_contact else float("nan"),
            "frac_graph_dist_2": np.mean([r["graph_distance"] == 2 for r in valid_graph]) if valid_graph else float("nan"),
            "frac_graph_dist_ge3": np.mean([r["graph_distance"] >= 3 for r in valid_graph]) if valid_graph else float("nan"),
            "mean_graph_distance": np.mean([r["graph_distance"] for r in valid_graph]) if valid_graph else float("nan"),
            "frac_same_sse_segment": np.mean([r["same_sse_segment"] for r in valid_sse]) if valid_sse else float("nan"),
            "frac_different_sse": np.mean([r["different_sse_different_type"] for r in valid_sse]) if valid_sse else float("nan"),
            "mean_jaccard_overlap": np.mean([r["jaccard_overlap"] for r in valid_jaccard]) if valid_jaccard else float("nan"),
            "mean_shared_contacts": np.mean([r["shared_contact_partners"] for r in valid_jaccard]) if valid_jaccard else float("nan"),
        }

    results["analysis1"] = {
        "anchor_affected": compute_target_profile(anchor_rows, affected_only=True),
        "anchor_all": compute_target_profile(anchor_rows, affected_only=False),
        "control_affected": compute_target_profile(control_rows, affected_only=True),
        "control_all": compute_target_profile(control_rows, affected_only=False),
    }

    # Analysis 2: Enrichment of affected vs all targets (within-source comparison)
    proteins = sorted(set(r["protein"] for r in all_target_rows))
    enrichment_rows = []
    for protein in proteins:
        for label_prefix in ["anchor", "control"]:
            prows = [r for r in all_target_rows if r["protein"] == protein and r["source_label"].startswith(label_prefix if label_prefix == "control" else "anchor")]
            if not prows:
                continue
            affected = [r for r in prows if r.get("affected_threshold")]
            if not affected:
                continue
            valid_all = [r for r in prows if r.get("direct_contact_8A", -1) >= 0]
            valid_aff = [r for r in affected if r.get("direct_contact_8A", -1) >= 0]
            if not valid_all or not valid_aff:
                continue
            p_contact_all = np.mean([r["direct_contact_8A"] for r in valid_all])
            p_contact_aff = np.mean([r["direct_contact_8A"] for r in valid_aff])
            valid_g_all = [r for r in prows if r.get("graph_distance", -1) >= 0 and r["graph_distance"] < 999]
            valid_g_aff = [r for r in affected if r.get("graph_distance", -1) >= 0 and r["graph_distance"] < 999]
            p_g2_all = np.mean([r["graph_distance"] <= 2 for r in valid_g_all]) if valid_g_all else float("nan")
            p_g2_aff = np.mean([r["graph_distance"] <= 2 for r in valid_g_aff]) if valid_g_aff else float("nan")
            valid_sse_all = [r for r in prows if r.get("same_sse_segment", -1) >= 0]
            valid_sse_aff = [r for r in affected if r.get("same_sse_segment", -1) >= 0]
            p_sse_all = np.mean([r["same_sse_segment"] for r in valid_sse_all]) if valid_sse_all else float("nan")
            p_sse_aff = np.mean([r["same_sse_segment"] for r in valid_sse_aff]) if valid_sse_aff else float("nan")
            jaccard_all = np.mean([r["jaccard_overlap"] for r in valid_all])
            jaccard_aff = np.mean([r["jaccard_overlap"] for r in valid_aff])
            enrichment_rows.append({
                "protein": protein,
                "group": label_prefix,
                "contact_enrichment": p_contact_aff - p_contact_all,
                "graph_dist2_enrichment": p_g2_aff - p_g2_all,
                "same_sse_enrichment": p_sse_aff - p_sse_all,
                "jaccard_enrichment": jaccard_aff - jaccard_all,
                "p_contact_affected": p_contact_aff,
                "p_contact_all": p_contact_all,
            })
    results["analysis2_enrichment"] = enrichment_rows

    # Analysis 3: Anchor vs control per-protein comparison
    per_protein = {}
    for protein in proteins:
        src_rows = [r for r in all_source_rows if r["protein"] == protein]
        anchor_src = [r for r in src_rows if r["is_anchor"] and r["source_label"] == "anchor_top1"]
        control_src = [r for r in src_rows if not r["is_anchor"]]
        if not anchor_src or not control_src:
            continue
        a = anchor_src[0]
        metrics = {}
        for key in ["aff_frac_direct_contact", "aff_mean_graph_distance", "aff_frac_different_sse",
                     "n_distinct_sse_segments_affected", "aff_mean_jaccard_overlap", "aff_mean_shared_contacts",
                     "mean_delta", "max_delta"]:
            a_val = a.get(key, float("nan"))
            c_vals = [r.get(key, float("nan")) for r in control_src]
            c_vals = [v for v in c_vals if not np.isnan(v)]
            c_mean = np.mean(c_vals) if c_vals else float("nan")
            metrics[f"top1_{key}"] = a_val
            metrics[f"ctrl_mean_{key}"] = c_mean
            metrics[f"diff_{key}"] = a_val - c_mean if not np.isnan(a_val) and not np.isnan(c_mean) else float("nan")
        per_protein[protein] = metrics
    results["analysis3_per_protein"] = per_protein

    # Analysis 4: Top-1 vs Top-3
    top1_src = [r for r in all_source_rows if r["source_label"] == "anchor_top1"]
    top3_src = [r for r in all_source_rows if r["is_anchor"]]
    results["analysis4_top1_vs_top3"] = {
        "top1_mean_delta": np.mean([r["mean_delta"] for r in top1_src]) if top1_src else float("nan"),
        "top3_mean_delta": np.mean([r["mean_delta"] for r in top3_src]) if top3_src else float("nan"),
        "top1_mean_aff_contact": np.mean([r["aff_frac_direct_contact"] for r in top1_src if not np.isnan(r.get("aff_frac_direct_contact", float("nan")))]) if top1_src else float("nan"),
        "top3_mean_aff_contact": np.mean([r["aff_frac_direct_contact"] for r in top3_src if not np.isnan(r.get("aff_frac_direct_contact", float("nan")))]) if top3_src else float("nan"),
        "top1_mean_aff_jaccard": np.mean([r["aff_mean_jaccard_overlap"] for r in top1_src if not np.isnan(r.get("aff_mean_jaccard_overlap", float("nan")))]) if top1_src else float("nan"),
        "top3_mean_aff_jaccard": np.mean([r["aff_mean_jaccard_overlap"] for r in top3_src if not np.isnan(r.get("aff_mean_jaccard_overlap", float("nan")))]) if top3_src else float("nan"),
        "top1_mean_n_sse_segs": np.mean([r["n_distinct_sse_segments_affected"] for r in top1_src]) if top1_src else float("nan"),
        "top3_mean_n_sse_segs": np.mean([r["n_distinct_sse_segments_affected"] for r in top3_src]) if top3_src else float("nan"),
    }

    # Analysis 5: EVcoupling enrichment
    ev_rows_all = [r for r in all_target_rows if not np.isnan(r.get("ev_score", float("nan")))]
    if ev_rows_all:
        affected_ev = [r["ev_score"] for r in ev_rows_all if r.get("affected_threshold")]
        not_affected_ev = [r["ev_score"] for r in ev_rows_all if not r.get("affected_threshold")]
        results["analysis5_evcoupling"] = {
            "n_with_ev": len(ev_rows_all),
            "affected_mean_ev": float(np.mean(affected_ev)) if affected_ev else float("nan"),
            "not_affected_mean_ev": float(np.mean(not_affected_ev)) if not_affected_ev else float("nan"),
            "affected_n": len(affected_ev),
            "not_affected_n": len(not_affected_ev),
        }
        if len(affected_ev) >= 3 and len(not_affected_ev) >= 3:
            try:
                stat, p = stats.mannwhitneyu(affected_ev, not_affected_ev, alternative="greater")
                results["analysis5_evcoupling"]["mannwhitney_p"] = float(p)
            except Exception:
                results["analysis5_evcoupling"]["mannwhitney_p"] = float("nan")
    else:
        results["analysis5_evcoupling"] = {"n_with_ev": 0}

    return results


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_results(all_source_rows: list[dict], all_target_rows: list[dict], analyses: dict, output_dir: Path):
    C_ANCHOR = "#D64550"
    C_CTRL = "#5B7FA3"

    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
        "figure.dpi": 200,
    })

    fig, axes_arr = plt.subplots(2, 2, figsize=(12, 9))

    # Plot A: affected-target relationship breakdown (anchor vs control)
    ax = axes_arr[0, 0]
    a1 = analyses["analysis1"]
    categories = ["Direct contact", "Graph dist <= 2", "Same SSE seg", "Different SSE"]
    anchor_vals = [
        a1["anchor_affected"].get("frac_direct_contact", 0),
        (1 - a1["anchor_affected"].get("frac_graph_dist_ge3", 1)) if not np.isnan(a1["anchor_affected"].get("frac_graph_dist_ge3", float("nan"))) else 0,
        a1["anchor_affected"].get("frac_same_sse_segment", 0),
        a1["anchor_affected"].get("frac_different_sse", 0),
    ]
    control_vals = [
        a1["control_affected"].get("frac_direct_contact", 0),
        (1 - a1["control_affected"].get("frac_graph_dist_ge3", 1)) if not np.isnan(a1["control_affected"].get("frac_graph_dist_ge3", float("nan"))) else 0,
        a1["control_affected"].get("frac_same_sse_segment", 0),
        a1["control_affected"].get("frac_different_sse", 0),
    ]
    # Replace NaN with 0 for plotting
    anchor_vals = [0 if np.isnan(v) else v for v in anchor_vals]
    control_vals = [0 if np.isnan(v) else v for v in control_vals]
    x = np.arange(len(categories))
    w = 0.35
    ax.bar(x - w/2, anchor_vals, w, label="Anchors", color=C_ANCHOR, alpha=0.7)
    ax.bar(x + w/2, control_vals, w, label="Controls", color=C_CTRL, alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=25, ha="right")
    ax.set_ylabel("Fraction of affected targets")
    ax.set_title("A. Affected-target relationship breakdown")
    ax.legend()

    # Plot B: per-protein enrichment (anchor - control)
    ax = axes_arr[0, 1]
    per_protein = analyses.get("analysis3_per_protein", {})
    if per_protein:
        pnames = sorted(per_protein.keys())
        contact_diffs = [per_protein[p].get("diff_aff_frac_direct_contact", 0) for p in pnames]
        jaccard_diffs = [per_protein[p].get("diff_aff_mean_jaccard_overlap", 0) for p in pnames]
        sse_diffs = [per_protein[p].get("diff_n_distinct_sse_segments_affected", 0) for p in pnames]
        # Replace NaN
        contact_diffs = [0 if np.isnan(v) else v for v in contact_diffs]
        jaccard_diffs = [0 if np.isnan(v) else v for v in jaccard_diffs]
        sse_diffs = [0 if np.isnan(v) else v for v in sse_diffs]
        x = np.arange(len(pnames))
        w = 0.25
        ax.bar(x - w, contact_diffs, w, label="Contact enrich.", color=C_ANCHOR, alpha=0.7)
        ax.bar(x, jaccard_diffs, w, label="Jaccard enrich.", color="#61afef", alpha=0.7)
        ax.bar(x + w, [d / 5 for d in sse_diffs], w, label="SSE segs (/ 5)", color="#98c379", alpha=0.7)
        ax.set_xticks(x)
        ax.set_xticklabels(pnames, rotation=60, ha="right", fontsize=6)
        ax.axhline(0, color="gray", ls=":", lw=0.7)
        ax.set_ylabel("Anchor - control difference")
        ax.set_title("B. Per-protein enrichment (anchor - control)")
        ax.legend(fontsize=6)

    # Plot C: target distance scatter colored by contact
    ax = axes_arr[1, 0]
    anchor_targets = [r for r in all_target_rows if r["is_anchor"] and r.get("direct_contact_8A", -1) >= 0]
    if anchor_targets:
        seq_seps = [r["seq_sep"] for r in anchor_targets]
        deltas = [r["delta"] for r in anchor_targets]
        contacts = [r["direct_contact_8A"] for r in anchor_targets]
        colors = [C_ANCHOR if c else C_CTRL for c in contacts]
        ax.scatter(seq_seps, deltas, c=colors, alpha=0.5, s=15, edgecolors="none")
        # Legend
        ax.scatter([], [], c=C_ANCHOR, s=20, label="Direct contact")
        ax.scatter([], [], c=C_CTRL, s=20, label="No contact")
        ax.axhline(POSITIVE_THRESHOLD, color="gray", ls="--", lw=0.7, label=f"threshold={POSITIVE_THRESHOLD}")
        ax.set_xlabel("Sequence separation")
        ax.set_ylabel("Delta (nats)")
        ax.set_title("C. Target delta vs sequence separation (anchors)")
        ax.legend(fontsize=7)

    # Plot D: contact-neighborhood overlap (Jaccard)
    ax = axes_arr[1, 1]
    anchor_src = [r for r in all_source_rows if r["is_anchor"]]
    control_src = [r for r in all_source_rows if not r["is_anchor"]]
    a_jaccard = [r["aff_mean_jaccard_overlap"] for r in anchor_src if not np.isnan(r.get("aff_mean_jaccard_overlap", float("nan")))]
    c_jaccard = [r["aff_mean_jaccard_overlap"] for r in control_src if not np.isnan(r.get("aff_mean_jaccard_overlap", float("nan")))]
    a_shared = [r["aff_mean_shared_contacts"] for r in anchor_src if not np.isnan(r.get("aff_mean_shared_contacts", float("nan")))]
    c_shared = [r["aff_mean_shared_contacts"] for r in control_src if not np.isnan(r.get("aff_mean_shared_contacts", float("nan")))]
    if a_jaccard and c_jaccard:
        bp = ax.boxplot([a_jaccard, c_jaccard], labels=["Anchors", "Controls"], positions=[1, 2], patch_artist=True, widths=0.4)
        bp["boxes"][0].set_facecolor(C_ANCHOR)
        bp["boxes"][0].set_alpha(0.6)
        bp["boxes"][1].set_facecolor(C_CTRL)
        bp["boxes"][1].set_alpha(0.6)
        ax.set_ylabel("Mean Jaccard overlap (affected targets)")
        ax.set_title("D. Contact-neighborhood overlap of affected targets")

    for ax in axes_arr.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out = output_dir / "anchor_target_characterization.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")

    # Optional Plot E: EVcoupling enrichment
    ev_data = analyses.get("analysis5_evcoupling", {})
    if ev_data.get("n_with_ev", 0) > 0 and ev_data.get("affected_n", 0) > 0:
        fig_ev, ax_ev = plt.subplots(1, 1, figsize=(5, 4))
        ev_affected = [r["ev_score"] for r in all_target_rows if r.get("affected_threshold") and not np.isnan(r.get("ev_score", float("nan")))]
        ev_not = [r["ev_score"] for r in all_target_rows if not r.get("affected_threshold") and not np.isnan(r.get("ev_score", float("nan")))]
        if ev_affected and ev_not:
            bp = ax_ev.boxplot([ev_affected, ev_not], labels=["Affected", "Not affected"], patch_artist=True, widths=0.4)
            bp["boxes"][0].set_facecolor(C_ANCHOR)
            bp["boxes"][0].set_alpha(0.6)
            bp["boxes"][1].set_facecolor(C_CTRL)
            bp["boxes"][1].set_alpha(0.6)
            p_val = ev_data.get("mannwhitney_p", float("nan"))
            ax_ev.set_title(f"E. EVcoupling scores: affected vs not (p={p_val:.4f})" if not np.isnan(p_val) else "E. EVcoupling scores: affected vs not")
            ax_ev.set_ylabel("EVcoupling score")
            ax_ev.spines["top"].set_visible(False)
            ax_ev.spines["right"].set_visible(False)
            plt.tight_layout()
            out_ev = output_dir / "anchor_target_characterization_ev.png"
            fig_ev.savefig(out_ev, dpi=200, bbox_inches="tight")
            plt.close(fig_ev)
            print(f"  Saved: {out_ev}")


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_report(all_source_rows: list[dict], all_target_rows: list[dict], analyses: dict, output_dir: Path):
    report = []
    report.append("# Affected-Target Characterization after Selector Ablation\n\n")

    n_proteins = len(set(r["protein"] for r in all_source_rows))
    n_sources = len(all_source_rows)
    n_targets = len(all_target_rows)
    report.append(f"Proteins analyzed: {n_proteins}. Source residues: {n_sources}. Target-level observations: {n_targets}.\n")
    report.append(f"Ablation: c = {ABLATION_C}. Min seq sep: {MIN_SEQ_SEP}. Contact cutoff: {CONTACT_CUTOFF} A. Affected threshold: delta > {POSITIVE_THRESHOLD}. Top-k affected: {TOP_K_AFFECTED}.\n\n")

    # Analysis 1
    a1 = analyses["analysis1"]
    report.append("## Analysis 1: What kinds of targets are affected?\n\n")
    report.append("| Metric | Anchor affected | Anchor all | Control affected | Control all |\n")
    report.append("|--------|----------------|-----------|-----------------|------------|\n")
    for key, label in [
        ("frac_direct_contact", "Frac direct contact"),
        ("frac_graph_dist_2", "Frac graph dist = 2"),
        ("frac_graph_dist_ge3", "Frac graph dist >= 3"),
        ("mean_graph_distance", "Mean graph distance"),
        ("frac_same_sse_segment", "Frac same SSE segment"),
        ("frac_different_sse", "Frac different SSE"),
        ("mean_jaccard_overlap", "Mean Jaccard overlap"),
        ("mean_shared_contacts", "Mean shared contacts"),
    ]:
        vals = [a1[g].get(key, float("nan")) for g in ["anchor_affected", "anchor_all", "control_affected", "control_all"]]
        vals_str = [f"{v:.4f}" if not np.isnan(v) else "n/a" for v in vals]
        report.append(f"| {label} | {vals_str[0]} | {vals_str[1]} | {vals_str[2]} | {vals_str[3]} |\n")
    report.append("\n")

    report.append(f"Anchor affected targets: n = {a1['anchor_affected']['n']}. Control affected targets: n = {a1['control_affected']['n']}.\n\n")

    # Analysis 2
    report.append("## Analysis 2: Contact / graph enrichment over random distant targets\n\n")
    enrichment = analyses.get("analysis2_enrichment", [])
    if enrichment:
        anchor_enrich = [r for r in enrichment if r["group"] == "anchor"]
        control_enrich = [r for r in enrichment if r["group"] == "control"]
        report.append("| Metric | Anchor enrichment (mean) | Control enrichment (mean) |\n")
        report.append("|--------|-------------------------|-------------------------|\n")
        for key, label in [
            ("contact_enrichment", "Direct contact"),
            ("graph_dist2_enrichment", "Graph dist <= 2"),
            ("same_sse_enrichment", "Same SSE segment"),
            ("jaccard_enrichment", "Jaccard overlap"),
        ]:
            a_vals = [r[key] for r in anchor_enrich if not np.isnan(r.get(key, float("nan")))]
            c_vals = [r[key] for r in control_enrich if not np.isnan(r.get(key, float("nan")))]
            a_mean = np.mean(a_vals) if a_vals else float("nan")
            c_mean = np.mean(c_vals) if c_vals else float("nan")
            a_str = f"{a_mean:.4f}" if not np.isnan(a_mean) else "n/a"
            c_str = f"{c_mean:.4f}" if not np.isnan(c_mean) else "n/a"
            report.append(f"| {label} | {a_str} | {c_str} |\n")
        report.append("\n")

    # Analysis 3
    report.append("## Analysis 3: Anchor vs control target-profile comparison\n\n")
    per_protein = analyses.get("analysis3_per_protein", {})
    if per_protein:
        report.append("| Protein | Top-1 contact frac | Ctrl contact frac | Diff | Top-1 Jaccard | Ctrl Jaccard | Diff | Top-1 SSE segs | Ctrl SSE segs | Diff |\n")
        report.append("|---------|-------------------|-------------------|------|--------------|-------------|------|---------------|--------------|------|\n")
        for p in sorted(per_protein):
            d = per_protein[p]
            def fmt(v):
                return f"{v:.4f}" if not np.isnan(v) else "n/a"
            report.append(f"| {p} | {fmt(d.get('top1_aff_frac_direct_contact', float('nan')))} | {fmt(d.get('ctrl_mean_aff_frac_direct_contact', float('nan')))} | {fmt(d.get('diff_aff_frac_direct_contact', float('nan')))} | {fmt(d.get('top1_aff_mean_jaccard_overlap', float('nan')))} | {fmt(d.get('ctrl_mean_aff_mean_jaccard_overlap', float('nan')))} | {fmt(d.get('diff_aff_mean_jaccard_overlap', float('nan')))} | {fmt(d.get('top1_n_distinct_sse_segments_affected', float('nan')))} | {fmt(d.get('ctrl_mean_n_distinct_sse_segments_affected', float('nan')))} | {fmt(d.get('diff_n_distinct_sse_segments_affected', float('nan')))} |\n")
        report.append("\n")

    # Analysis 4
    report.append("## Analysis 4: Top-1 vs Top-3 anchors\n\n")
    a4 = analyses.get("analysis4_top1_vs_top3", {})
    report.append("| Metric | Top-1 | Top-3 mean |\n")
    report.append("|--------|-------|------------|\n")
    for key, label in [
        ("mean_delta", "Mean delta"),
        ("mean_aff_contact", "Affected frac contact"),
        ("mean_aff_jaccard", "Affected mean Jaccard"),
        ("mean_n_sse_segs", "Distinct SSE segments affected"),
    ]:
        t1 = a4.get(f"top1_{key}", float("nan"))
        t3 = a4.get(f"top3_{key}", float("nan"))
        t1_str = f"{t1:.4f}" if not np.isnan(t1) else "n/a"
        t3_str = f"{t3:.4f}" if not np.isnan(t3) else "n/a"
        report.append(f"| {label} | {t1_str} | {t3_str} |\n")
    report.append("\n")

    # Analysis 5
    ev = analyses.get("analysis5_evcoupling", {})
    if ev.get("n_with_ev", 0) > 0:
        report.append("## Analysis 5: EVcoupling enrichment\n\n")
        report.append(f"Target pairs with EVcoupling data: {ev['n_with_ev']}.\n")
        report.append(f"Affected targets: n = {ev.get('affected_n', 0)}, mean EV score = {ev.get('affected_mean_ev', float('nan')):.4f}.\n")
        report.append(f"Non-affected targets: n = {ev.get('not_affected_n', 0)}, mean EV score = {ev.get('not_affected_mean_ev', float('nan')):.4f}.\n")
        p = ev.get("mannwhitney_p", float("nan"))
        if not np.isnan(p):
            report.append(f"Mann-Whitney U test (affected > not affected): p = {p:.4f}.\n")
        report.append("\n")

    report.append("![Results](anchor_target_characterization.png)\n\n")

    out = output_dir / "anchor_target_characterization.md"
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
    source_csv = REPORT_DIR / "anchor_target_characterization_source_level.csv"
    if all_source_rows:
        fields = list(all_source_rows[0].keys())
        with open(source_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_source_rows)
        print(f"  Saved: {source_csv}")

    target_csv = REPORT_DIR / "anchor_target_characterization_target_level.csv"
    if all_target_rows:
        fields = list(all_target_rows[0].keys())
        with open(target_csv, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_target_rows)
        print(f"  Saved: {target_csv}")

    # Run analyses
    print("\nRunning analyses...")
    analyses = run_analyses(all_source_rows, all_target_rows)

    # Plots
    print("Generating plots...")
    plot_results(all_source_rows, all_target_rows, analyses, REPORT_DIR)

    # Report
    print("Writing report...")
    write_report(all_source_rows, all_target_rows, analyses, REPORT_DIR)

    print("\nDone.")


if __name__ == "__main__":
    main()
