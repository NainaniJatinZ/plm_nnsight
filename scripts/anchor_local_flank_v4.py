#!/usr/bin/env python3
"""Anchor local flank v4: H4+ with cluster-level features.

Extends v3 H4 (per-position structural features) with window-level summary
features that describe the local structural cluster as a whole.

Feature sets:
  H4_base:         244 per-position features (same as v3 H4)
  H4_plus:         244 + 16 cluster + 7 H5 = 267 features
  H4_cluster_only: 16 cluster + 7 H5 = 23 features

Usage:
    PYTHONUNBUFFERED=1 uv run python scripts/anchor_local_flank_v4.py
"""

from __future__ import annotations

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

TOP_N = 500
RADIUS = 30
CONTROLS_PER_ANCHOR = 5
MIN_EDGE_DISTANCE = 30
N_SPLITS = 10
N_PERMUTATIONS = 100

# Max ASA for RSA computation (Tien et al. 2013)
MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}

SSE_ORDER = ["H", "E", "C"]

def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


# ---------------------------------------------------------------------------
# Data loading (copied from v3)
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
            rows.append({"protein": pid, "top3_mass": mass, "anchor_pos": anchor_pos, "n_res": n_res})
    rows.sort(key=lambda x: x["top3_mass"], reverse=True)
    return rows[:n]


# ---------------------------------------------------------------------------
# PDB feature computation (copied from v3)
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

    features["_dists"] = dists
    features["_seq_to_pdb"] = seq_to_pdb

    return features


# ---------------------------------------------------------------------------
# Control matching (structural, copied from v3)
# ---------------------------------------------------------------------------

def match_controls_structural(proteins, seqs, ss_dict, pdb_features_cache):
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

    flush_print(f"  Structural matching: {len(proteins) - dropped} proteins with controls, {dropped} dropped, {len(all_matches)} total pairs")
    return all_matches


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def features_h4_base(center_pos, radius, pdb_feats):
    """Per-position structural features (same as v3 H4). 4 x (2R+1) = 244 features."""
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


def features_cluster(center_pos, radius, pdb_feats, sse_str):
    """16 cluster-level summary features."""
    wlen = 2 * radius + 1
    dists = pdb_feats.get("_dists")
    seq_to_pdb = pdb_feats.get("_seq_to_pdb", {})
    center_pdb_idx = seq_to_pdb.get(center_pos)
    n_res = len(sse_str)

    # Gather per-position info within window
    window_positions = []  # (seq_pos, relative_pos, pdb_idx, rsa, c8a, lrf, contact_with_center)
    for j in range(wlen):
        seq_pos = center_pos - radius + j
        rel_pos = j - radius
        if seq_pos < 0 or seq_pos >= n_res:
            continue
        pdb_idx = seq_to_pdb.get(seq_pos)
        if seq_pos in pdb_feats and isinstance(pdb_feats[seq_pos], dict):
            pf = pdb_feats[seq_pos]
            contact_with_center = False
            if center_pdb_idx is not None and pdb_idx is not None and dists is not None:
                contact_with_center = dists[pdb_idx, center_pdb_idx] < 8.0
            window_positions.append({
                "seq_pos": seq_pos, "rel_pos": rel_pos, "pdb_idx": pdb_idx,
                "rsa": pf["rsa"], "c8a": pf["contacts_8A"], "lrf": pf["long_range_fraction"],
                "contact_center": contact_with_center,
            })

    feats = {}

    # --- Contact cluster summaries (features 1-7) ---
    flank_contacting = [p for p in window_positions if p["rel_pos"] != 0 and p["contact_center"]]
    n_flank = sum(1 for p in window_positions if p["rel_pos"] != 0)

    feats["n_flank_contacting_center"] = len(flank_contacting)
    feats["frac_flank_contacting_center"] = len(flank_contacting) / max(n_flank, 1)
    feats["mean_rsa_contacting"] = np.mean([p["rsa"] for p in flank_contacting]) if flank_contacting else 0.0
    feats["mean_contacts_contacting"] = np.mean([p["c8a"] for p in flank_contacting]) if flank_contacting else 0.0
    feats["mean_lr_frac_contacting"] = np.mean([p["lrf"] for p in flank_contacting]) if flank_contacting else 0.0

    # SSE segments contacting center
    center_sse_seg_id = _get_sse_segment_id(center_pos, sse_str)
    contacting_sse_segments = set()
    n_cross_sse = 0
    for p in flank_contacting:
        seg_id = _get_sse_segment_id(p["seq_pos"], sse_str)
        contacting_sse_segments.add(seg_id)
        if seg_id != center_sse_seg_id:
            n_cross_sse += 1
    feats["n_sse_segments_contacting"] = len(contacting_sse_segments)
    feats["frac_cross_sse_contacts"] = n_cross_sse / max(len(flank_contacting), 1)

    # --- Burial pattern summaries (features 8-11) ---
    left_positions = [p for p in window_positions if p["rel_pos"] < 0]
    right_positions = [p for p in window_positions if p["rel_pos"] > 0]
    all_flank = [p for p in window_positions if p["rel_pos"] != 0]

    frac_buried_all = sum(1 for p in all_flank if p["rsa"] < 0.05) / max(len(all_flank), 1)
    frac_buried_left = sum(1 for p in left_positions if p["rsa"] < 0.05) / max(len(left_positions), 1)
    frac_buried_right = sum(1 for p in right_positions if p["rsa"] < 0.05) / max(len(right_positions), 1)

    feats["frac_buried_flank"] = frac_buried_all
    feats["frac_buried_left"] = frac_buried_left
    feats["frac_buried_right"] = frac_buried_right
    feats["burial_asymmetry"] = abs(frac_buried_left - frac_buried_right)

    # --- Contact density within window (features 12-14) ---
    window_pdb_idxs = [p["pdb_idx"] for p in window_positions if p["pdb_idx"] is not None]
    n_win = len(window_pdb_idxs)
    if n_win >= 2 and dists is not None:
        # Count contact pairs within window
        n_pairs = 0
        degree = np.zeros(n_win)
        for i in range(n_win):
            for j2 in range(i + 1, n_win):
                if dists[window_pdb_idxs[i], window_pdb_idxs[j2]] < 8.0:
                    n_pairs += 1
                    degree[i] += 1
                    degree[j2] += 1
        total_possible = n_win * (n_win - 1) / 2
        feats["contact_density_window"] = n_pairs / total_possible
        feats["mean_degree_window"] = float(np.mean(degree))
        feats["max_degree_window"] = float(np.max(degree))
    else:
        feats["contact_density_window"] = 0.0
        feats["mean_degree_window"] = 0.0
        feats["max_degree_window"] = 0.0

    # --- Spatial distribution of contacts (features 15-16) ---
    contacting_rel_pos = [p["rel_pos"] for p in flank_contacting]
    if len(contacting_rel_pos) >= 2:
        feats["contact_spread"] = float(np.std(contacting_rel_pos))
        feats["contact_span"] = max(contacting_rel_pos) - min(contacting_rel_pos)
    elif len(contacting_rel_pos) == 1:
        feats["contact_spread"] = 0.0
        feats["contact_span"] = 0
    else:
        feats["contact_spread"] = 0.0
        feats["contact_span"] = 0

    return feats


def features_bridge(center_pos, radius, pdb_feats):
    """4 bridge-topology features measuring whether center bridges disconnected structural regions."""
    dists = pdb_feats.get("_dists")
    seq_to_pdb = pdb_feats.get("_seq_to_pdb", {})
    center_pdb_idx = seq_to_pdb.get(center_pos)

    feats = {}

    if dists is None or center_pdb_idx is None:
        feats["frac_nonredundant_contacts"] = 0.0
        feats["n_components_without_center"] = 0
        feats["betweenness_in_window"] = 0.0
        feats["bridge_score"] = 0
        return feats

    # Build window contact graph as adjacency list (using pdb_idx as node IDs)
    wlen = 2 * radius + 1
    window_pdb_idxs = set()
    for j in range(wlen):
        seq_pos = center_pos - radius + j
        pdb_idx = seq_to_pdb.get(seq_pos)
        if pdb_idx is not None:
            window_pdb_idxs.add(pdb_idx)

    if len(window_pdb_idxs) < 3:
        feats["frac_nonredundant_contacts"] = 0.0
        feats["n_components_without_center"] = 0
        feats["betweenness_in_window"] = 0.0
        feats["bridge_score"] = 0
        return feats

    window_pdb_list = sorted(window_pdb_idxs)
    node_set = set(window_pdb_list)

    # Build adjacency dict for window subgraph
    adj = {n: set() for n in window_pdb_list}
    for i, ni in enumerate(window_pdb_list):
        for nj in window_pdb_list[i + 1:]:
            if dists[ni, nj] < 8.0:
                adj[ni].add(nj)
                adj[nj].add(ni)

    # Feature 1: frac_nonredundant_contacts
    # For each pair of center's contacts (i, j), check if i-j are in contact.
    # Fraction where they are NOT = bridge score.
    center_neighbors = [n for n in adj.get(center_pdb_idx, set()) if n != center_pdb_idx]
    if len(center_neighbors) >= 2:
        n_contact_pairs = 0
        n_redundant = 0
        for i in range(len(center_neighbors)):
            for j in range(i + 1, len(center_neighbors)):
                n_contact_pairs += 1
                if center_neighbors[j] in adj.get(center_neighbors[i], set()):
                    n_redundant += 1
        feats["frac_nonredundant_contacts"] = 1.0 - (n_redundant / n_contact_pairs)
    elif len(center_neighbors) == 1:
        feats["frac_nonredundant_contacts"] = 1.0
    else:
        feats["frac_nonredundant_contacts"] = 0.0

    # Feature 2 & 4: n_components_without_center and bridge_score
    def count_components(adj_dict, nodes):
        visited = set()
        n_comp = 0
        for start in nodes:
            if start in visited:
                continue
            n_comp += 1
            stack = [start]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                for neighbor in adj_dict.get(node, set()):
                    if neighbor in nodes and neighbor not in visited:
                        stack.append(neighbor)
        return n_comp

    nodes_with_center = set(window_pdb_list)
    nodes_without_center = nodes_with_center - {center_pdb_idx}

    comp_with = count_components(adj, nodes_with_center)
    comp_without = count_components(adj, nodes_without_center) if nodes_without_center else 0

    feats["n_components_without_center"] = comp_without
    feats["bridge_score"] = 1 if comp_without > comp_with else 0

    # Feature 3: betweenness_in_window (approximate via BFS shortest paths)
    # Betweenness centrality = fraction of shortest paths through center
    n_nodes = len(window_pdb_list)
    if n_nodes <= 2:
        feats["betweenness_in_window"] = 0.0
        return feats

    # BFS-based betweenness for the center node only
    betweenness = 0.0
    node_list = list(nodes_with_center)
    for src in node_list:
        if src == center_pdb_idx:
            continue
        # BFS from src
        from collections import deque
        dist_from = {src: 0}
        n_paths = {src: 1}
        predecessors = {src: []}
        queue = deque([src])
        order = []
        while queue:
            v = queue.popleft()
            order.append(v)
            for w in adj.get(v, set()):
                if w not in nodes_with_center:
                    continue
                if w not in dist_from:
                    dist_from[w] = dist_from[v] + 1
                    n_paths[w] = n_paths[v]
                    predecessors[w] = [v]
                    queue.append(w)
                elif dist_from[w] == dist_from[v] + 1:
                    n_paths[w] += n_paths[v]
                    predecessors[w].append(v)
        # Back-propagation of dependencies
        delta = {v: 0.0 for v in order}
        for w in reversed(order):
            for v in predecessors.get(w, []):
                if n_paths[w] > 0:
                    delta[v] += (n_paths[v] / n_paths[w]) * (1 + delta[w])
            if w != src and w == center_pdb_idx:
                betweenness += delta[w]

    # Normalize by number of pairs (excluding center)
    n_other = n_nodes - 1
    if n_other >= 2:
        betweenness /= ((n_other) * (n_other - 1))

    feats["betweenness_in_window"] = betweenness

    return feats


def _get_sse_segment_id(pos, sse_str):
    """Return a unique segment ID for the SSE segment containing pos."""
    seg_start = pos
    while seg_start > 0 and sse_str[seg_start - 1] == sse_str[pos]:
        seg_start -= 1
    return (seg_start, sse_str[pos])


def features_h5_helper(center_pos, n_res, sse_str, radius):
    """7 H5 positional context features."""
    feats = {}
    feats["frac_pos"] = center_pos / n_res
    feats["dist_nterm"] = center_pos
    feats["dist_cterm"] = n_res - 1 - center_pos

    # SSE segment info within the window
    lo = max(0, center_pos - radius)
    hi = min(n_res, center_pos + radius + 1)
    window_sse = sse_str[lo:hi]
    n_transitions = sum(1 for i in range(1, len(window_sse)) if window_sse[i] != window_sse[i - 1])
    n_segments = n_transitions + 1
    feats["n_sse_segments_window"] = n_segments
    feats["n_sse_transitions_window"] = n_transitions

    # Length of SSE the center sits in
    center_sse = sse_str[center_pos]
    seg_len = 1
    for i in range(center_pos - 1, -1, -1):
        if sse_str[i] == center_sse:
            seg_len += 1
        else:
            break
    seg_start = center_pos - (seg_len - 1)
    for i in range(center_pos + 1, n_res):
        if sse_str[i] == center_sse:
            seg_len += 1
        else:
            break
    feats["sse_seg_len"] = seg_len
    feats["pos_in_sse"] = (center_pos - seg_start) / max(seg_len - 1, 1)

    return feats


# ---------------------------------------------------------------------------
# Dataset building
# ---------------------------------------------------------------------------

def extract_window(seq, center, radius):
    n = len(seq)
    lo, hi = center - radius, center + radius
    if lo < 0 or hi >= n:
        return None
    return seq[lo:hi + 1]


def build_dataset(proteins, matches, seqs, ss_dict, pdb_features_cache, feature_set="H4_plus"):
    """Build X, y, protein_ids for a given feature set.

    feature_set: "H4_base", "H4_plus", "H4_cluster_only",
                 "H4_bridge", "H4_bridge_only"
    """
    matches_by_protein = defaultdict(list)
    for m in matches:
        matches_by_protein[m["protein"]].append(m)

    feature_dicts = []
    labels = []
    pids = []
    protein_set = set(p["protein"] for p in proteins)

    for pid in sorted(protein_set):
        if pid not in matches_by_protein:
            continue
        seq = seqs[pid]
        sse = ss_dict[pid]
        n_res = len(seq)
        pdb_feats = pdb_features_cache.get(pid)
        if pdb_feats is None:
            continue

        protein_matches = matches_by_protein[pid]
        anchor_pos = protein_matches[0]["anchor_pos"]

        positions = [(anchor_pos, 1)]
        for m in protein_matches:
            positions.append((m["control_pos"], 0))

        for pos, label in positions:
            if extract_window(seq, pos, RADIUS) is None:
                continue

            feats = {}
            if feature_set in ("H4_base", "H4_plus", "H4_bridge"):
                feats.update(features_h4_base(pos, RADIUS, pdb_feats))
            if feature_set in ("H4_plus", "H4_cluster_only"):
                feats.update(features_cluster(pos, RADIUS, pdb_feats, sse))
            if feature_set in ("H4_bridge", "H4_bridge_only", "H4_plus"):
                feats.update(features_bridge(pos, RADIUS, pdb_feats))
            if feature_set in ("H4_plus", "H4_cluster_only", "H4_bridge", "H4_bridge_only"):
                feats.update(features_h5_helper(pos, n_res, sse, RADIUS))

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
# LOPO evaluation (copied from v3)
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
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "importances": None, "feature_names": None}

    le = LabelEncoder()
    groups = le.fit_transform(protein_ids)
    actual_splits = min(n_splits, len(proteins))
    gkf = GroupKFold(n_splits=actual_splits)

    all_probs = np.full(len(y), np.nan)
    importance_accum = []

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

        n_pos_train = y_train.sum()
        n_neg_train = len(y_train) - n_pos_train
        w_pos = len(y_train) / (2 * n_pos_train) if n_pos_train > 0 else 1.0
        w_neg = len(y_train) / (2 * n_neg_train) if n_neg_train > 0 else 1.0
        sample_weights = np.where(y_train == 1, w_pos, w_neg)

        clf = GradientBoostingClassifier(n_estimators=200, max_depth=3, learning_rate=0.1, random_state=42)
        clf.fit(X_train_s, y_train, sample_weight=sample_weights)
        probs = clf.predict_proba(X_test_s)[:, 1]
        all_probs[test_idx] = probs
        importance_accum.append(clf.feature_importances_)

    valid = ~np.isnan(all_probs)
    if valid.sum() == 0 or y[valid].sum() == 0:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "importances": None, "feature_names": None}

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
    mean_importances = np.mean(importance_accum, axis=0) if importance_accum else None

    return {"auroc": float(auroc), "auprc": float(auprc), "bal_acc": float(bal_acc), "importances": mean_importances}


def run_permutation_test(X, y, protein_ids, feature_names, n_perms=N_PERMUTATIONS, n_splits=N_SPLITS):
    rng = np.random.RandomState(42)
    null_auprcs = []
    for i in range(n_perms):
        y_perm = rng.permutation(y)
        result = run_lopo_l1(X, y_perm, protein_ids, feature_names, n_splits=n_splits)
        null_auprcs.append(result["auprc"])
        if (i + 1) % 25 == 0:
            flush_print(f"    Permutation {i + 1}/{n_perms}")
    return null_auprcs


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_comparison(results, output_path):
    """Bar chart: AUPRC per model (L1 and GBT side by side)."""
    models = list(results.keys())
    auprcs = [results[m]["auprc"] for m in models]
    base_rates = [results[m].get("base_rate", np.nan) for m in models]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(models))
    colors = ["#4575b4", "#91bfdb", "#fee090", "#fc8d59", "#d73027", "#542788"]
    bars = ax.bar(x, auprcs, color=[colors[i % len(colors)] for i in range(len(models))], alpha=0.85, edgecolor="black", linewidth=0.5)

    br = np.nanmean([b for b in base_rates if not np.isnan(b)])
    if not np.isnan(br):
        ax.axhline(y=br, color="gray", linestyle="--", alpha=0.7, label=f"Base rate ({br:.3f})")

    for i, (m, v) in enumerate(zip(models, auprcs)):
        if not np.isnan(v):
            ax.text(i, v + 0.005, f"{v:.3f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=9, rotation=15)
    ax.set_ylabel("AUPRC")
    ax.set_title("H4 Feature Set Comparison: AUPRC (R=30, LOPO)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {output_path}")


def plot_cluster_features(coefs, feature_names, title, output_path):
    """Bar chart of cluster-level feature coefficients."""
    # Filter to cluster + H5 features only (not per-position)
    per_pos_prefixes = ("rsa_", "c8a_", "lrf_", "cnt_center_")
    cluster_idx = [i for i, fn in enumerate(feature_names) if not any(fn.startswith(p) for p in per_pos_prefixes)]

    if not cluster_idx:
        return

    fig, ax = plt.subplots(figsize=(8, max(4, len(cluster_idx) * 0.3)))
    y_pos = np.arange(len(cluster_idx))
    vals = [coefs[i] for i in cluster_idx]
    names = [feature_names[i] for i in cluster_idx]
    colors = ["#d73027" if v > 0 else "#4575b4" for v in vals]
    ax.barh(y_pos, vals, color=colors, alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=7)
    ax.set_xlabel("L1 coefficient (scaled)")
    ax.set_title(title)
    ax.invert_yaxis()
    ax.axvline(x=0, color="black", linewidth=0.5)
    ax.grid(True, alpha=0.3, axis="x")
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {output_path}")


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
    flush_print(f"  Saved: {output_path}")


def plot_ablation(ablation_results, baseline_auprc, output_path):
    """Bar chart of AUPRC drop from removing each feature family."""
    families = list(ablation_results.keys())
    drops = [baseline_auprc - ablation_results[f]["auprc"] for f in families]

    fig, ax = plt.subplots(figsize=(8, max(4, len(families) * 0.4)))
    y_pos = np.arange(len(families))
    colors = ["#d73027" if d > 0 else "#4575b4" for d in drops]
    ax.barh(y_pos, drops, color=colors, alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(families, fontsize=8)
    ax.set_xlabel(f"AUPRC drop from H4+ baseline ({baseline_auprc:.3f})")
    ax.set_title("Feature Family Ablation (leave-one-family-out)")
    ax.invert_yaxis()
    ax.axvline(x=0, color="black", linewidth=0.5)
    ax.grid(True, alpha=0.3, axis="x")
    for i, d in enumerate(drops):
        ax.text(d + 0.002 if d >= 0 else d - 0.002, i, f"{d:+.3f}", va="center", ha="left" if d >= 0 else "right", fontsize=7)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {output_path}")


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
    flush_print(f"  Saved: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(REPORT_DIR, exist_ok=True)
    t0 = time.time()

    flush_print("Loading data...")
    seqs, ss_dict = load_data()

    proteins_pdb = select_proteins(seqs, ss_dict, n=TOP_N, require_pdb=True)
    flush_print(f"Selected {len(proteins_pdb)} proteins with PDB")

    # Compute PDB features
    flush_print("Computing PDB features...")
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
            if pdb_computed % 50 == 0:
                flush_print(f"  {pdb_computed} proteins...")
    flush_print(f"  PDB features computed for {pdb_computed} proteins")

    # Structural matching
    flush_print("Building structurally matched controls...")
    proteins_with_pdb = [p for p in proteins_pdb if p["protein"] in pdb_features_cache]
    matches = match_controls_structural(proteins_with_pdb, seqs, ss_dict, pdb_features_cache)

    all_results = {}

    # ====================================================================
    # Analysis 1: Feature set comparison
    # ====================================================================
    flush_print("\n" + "=" * 60)
    flush_print("ANALYSIS 1: Feature set comparison")
    flush_print("=" * 60)

    for fset in ["H4_base", "H4_plus", "H4_cluster_only", "H4_bridge", "H4_bridge_only"]:
        flush_print(f"\n--- {fset} (L1) ---")
        t1 = time.time()
        X, y, pids, feat_names = build_dataset(proteins_with_pdb, matches, seqs, ss_dict, pdb_features_cache, feature_set=fset)
        if X is None:
            flush_print(f"  No data, skipping")
            continue
        n_prot = len(set(pids))
        flush_print(f"  Dataset: {X.shape[0]} samples, {X.shape[1]} features, {n_prot} proteins, {int(y.sum())} anchors, {int((1-y).sum())} controls")

        result = run_lopo_l1(X, y, pids, feat_names)
        result["n_proteins"] = n_prot
        result["n_features"] = X.shape[1]
        all_results[f"{fset}_L1"] = result
        flush_print(f"  AUPRC={result['auprc']:.4f}  AUROC={result['auroc']:.4f}  BalAcc={result['bal_acc']:.4f}  ({time.time()-t1:.1f}s)")

        # Save coefficients
        if result["coefs"] is not None:
            coef_path = REPORT_DIR / f"anchor_local_flank_v4_coefficients_{fset}.csv"
            with open(coef_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["feature", "coefficient", "abs_coefficient"])
                for fname, coef in sorted(zip(feat_names, result["coefs"]), key=lambda x: -abs(x[1])):
                    w.writerow([fname, f"{coef:.6f}", f"{abs(coef):.6f}"])
            flush_print(f"  Saved coefficients: {coef_path.name}")

    # GBT on H4_plus, H4_cluster_only, H4_bridge, H4_bridge_only
    for fset in ["H4_plus", "H4_cluster_only", "H4_bridge", "H4_bridge_only"]:
        flush_print(f"\n--- {fset} (GBT) ---")
        t1 = time.time()
        X, y, pids, feat_names = build_dataset(proteins_with_pdb, matches, seqs, ss_dict, pdb_features_cache, feature_set=fset)
        if X is None:
            flush_print(f"  No data, skipping")
            continue
        result_gbt = run_lopo_gbt(X, y, pids)
        result_gbt["feature_names"] = feat_names
        all_results[f"{fset}_GBT"] = result_gbt
        flush_print(f"  AUPRC={result_gbt['auprc']:.4f}  AUROC={result_gbt['auroc']:.4f}  BalAcc={result_gbt['bal_acc']:.4f}  ({time.time()-t1:.1f}s)")

    # Comparison plot
    plot_order = ["H4_base_L1", "H4_plus_L1", "H4_cluster_only_L1", "H4_bridge_L1", "H4_bridge_only_L1", "H4_plus_GBT", "H4_cluster_only_GBT", "H4_bridge_GBT", "H4_bridge_only_GBT"]
    plot_results = {k: all_results[k] for k in plot_order if k in all_results}
    if plot_results:
        plot_comparison(plot_results, REPORT_DIR / "anchor_local_flank_v4_comparison.png")

    # ====================================================================
    # Analysis 2 & 3: Top features
    # ====================================================================
    flush_print("\n" + "=" * 60)
    flush_print("ANALYSIS 2 & 3: Top features")
    flush_print("=" * 60)

    if "H4_plus_L1" in all_results and all_results["H4_plus_L1"]["coefs"] is not None:
        r = all_results["H4_plus_L1"]
        plot_cluster_features(r["coefs"], r["feature_names"], "H4+ Cluster Feature Coefficients (L1)", REPORT_DIR / "anchor_local_flank_v4_cluster_features.png")
        plot_top_features(r["coefs"], r["feature_names"], "H4+ Top 20 Features (L1)", REPORT_DIR / "anchor_local_flank_v4_top_features_H4plus.png")

    if "H4_cluster_only_L1" in all_results and all_results["H4_cluster_only_L1"]["coefs"] is not None:
        r = all_results["H4_cluster_only_L1"]
        plot_top_features(r["coefs"], r["feature_names"], "H4_cluster_only Top Features (L1)", REPORT_DIR / "anchor_local_flank_v4_top_features_cluster_only.png")

    if "H4_bridge_only_L1" in all_results and all_results["H4_bridge_only_L1"]["coefs"] is not None:
        r = all_results["H4_bridge_only_L1"]
        plot_top_features(r["coefs"], r["feature_names"], "H4_bridge_only Top Features (L1)", REPORT_DIR / "anchor_local_flank_v4_top_features_bridge_only.png")

    if "H4_bridge_L1" in all_results and all_results["H4_bridge_L1"]["coefs"] is not None:
        r = all_results["H4_bridge_L1"]
        plot_top_features(r["coefs"], r["feature_names"], "H4_bridge Top 20 Features (L1)", REPORT_DIR / "anchor_local_flank_v4_top_features_H4bridge.png")

    # ====================================================================
    # Analysis 4: Feature ablation within H4+
    # ====================================================================
    flush_print("\n" + "=" * 60)
    flush_print("ANALYSIS 4: Feature family ablation within H4+")
    flush_print("=" * 60)

    X_plus, y_plus, pids_plus, fn_plus = build_dataset(proteins_with_pdb, matches, seqs, ss_dict, pdb_features_cache, feature_set="H4_plus")
    if X_plus is not None:
        baseline_auprc = all_results.get("H4_plus_L1", {}).get("auprc", np.nan)

        # Define feature families to ablate
        families = {
            "contact_cluster (1-7)": ["n_flank_contacting_center", "frac_flank_contacting_center", "mean_rsa_contacting", "mean_contacts_contacting", "mean_lr_frac_contacting", "n_sse_segments_contacting", "frac_cross_sse_contacts"],
            "burial_pattern (8-11)": ["frac_buried_flank", "frac_buried_left", "frac_buried_right", "burial_asymmetry"],
            "contact_density (12-14)": ["contact_density_window", "mean_degree_window", "max_degree_window"],
            "spatial_dist (15-16)": ["contact_spread", "contact_span"],
            "H5_helper (17-23)": ["frac_pos", "dist_nterm", "dist_cterm", "n_sse_segments_window", "n_sse_transitions_window", "sse_seg_len", "pos_in_sse"],
            "bridge_topology": ["frac_nonredundant_contacts", "n_components_without_center", "betweenness_in_window", "bridge_score"],
        }

        ablation_results = {}
        for family_name, family_features in families.items():
            t1 = time.time()
            # Find column indices to KEEP (everything except this family)
            drop_idx = [i for i, fn in enumerate(fn_plus) if fn in family_features]
            keep_idx = [i for i in range(X_plus.shape[1]) if i not in drop_idx]
            if len(keep_idx) == X_plus.shape[1]:
                flush_print(f"  {family_name}: no features found to ablate, skipping")
                continue
            X_ablated = X_plus[:, keep_idx]
            fn_ablated = [fn_plus[i] for i in keep_idx]
            result = run_lopo_l1(X_ablated, y_plus, pids_plus, fn_ablated)
            ablation_results[family_name] = result
            drop = baseline_auprc - result["auprc"]
            flush_print(f"  {family_name}: AUPRC={result['auprc']:.4f} (drop={drop:+.4f}) [{len(drop_idx)} features removed] ({time.time()-t1:.1f}s)")

        if ablation_results and not np.isnan(baseline_auprc):
            plot_ablation(ablation_results, baseline_auprc, REPORT_DIR / "anchor_local_flank_v4_ablation.png")

        # Save ablation CSV
        abl_path = REPORT_DIR / "anchor_local_flank_v4_ablation.csv"
        with open(abl_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["family", "n_removed", "auprc", "auprc_drop", "auroc", "bal_acc"])
            for family_name in families:
                if family_name in ablation_results:
                    r = ablation_results[family_name]
                    drop_idx = [i for i, fn in enumerate(fn_plus) if fn in families[family_name]]
                    w.writerow([family_name, len(drop_idx), f"{r['auprc']:.4f}", f"{baseline_auprc - r['auprc']:+.4f}", f"{r['auroc']:.4f}", f"{r['bal_acc']:.4f}"])
        flush_print(f"  Saved: {abl_path.name}")

    # ====================================================================
    # Permutation test on H4+
    # ====================================================================
    flush_print("\n" + "=" * 60)
    flush_print("PERMUTATION TEST on H4+")
    flush_print("=" * 60)

    if X_plus is not None and "H4_plus_L1" in all_results:
        observed = all_results["H4_plus_L1"]["auprc"]
        flush_print(f"  Running 100 permutations (observed AUPRC={observed:.4f})...")
        null_auprcs = run_permutation_test(X_plus, y_plus, pids_plus, fn_plus)
        p_val = np.mean([n >= observed for n in null_auprcs])
        flush_print(f"  p-value: {p_val:.4f} (95th pctl of null: {np.percentile(null_auprcs, 95):.4f})")
        plot_null_distribution(observed, null_auprcs, "Permutation Test: H4+", REPORT_DIR / "anchor_local_flank_v4_null_distribution.png")

    # ====================================================================
    # Save metrics CSV
    # ====================================================================
    metrics_path = REPORT_DIR / "anchor_local_flank_v4_metrics.csv"
    with open(metrics_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "n_proteins", "n_features", "base_rate", "auprc", "auroc", "bal_acc"])
        for key in ["H4_base_L1", "H4_plus_L1", "H4_cluster_only_L1", "H4_bridge_L1", "H4_bridge_only_L1", "H4_plus_GBT", "H4_cluster_only_GBT", "H4_bridge_GBT", "H4_bridge_only_GBT"]:
            if key in all_results:
                r = all_results[key]
                w.writerow([key, r.get("n_proteins", ""), r.get("n_features", ""), f"{r.get('base_rate', np.nan):.4f}", f"{r.get('auprc', np.nan):.4f}", f"{r.get('auroc', np.nan):.4f}", f"{r.get('bal_acc', np.nan):.4f}"])
    flush_print(f"\nMetrics saved: {metrics_path}")

    # ====================================================================
    # Summary report
    # ====================================================================
    flush_print("\n" + "=" * 60)
    flush_print("SUMMARY")
    flush_print("=" * 60)

    report_lines = []
    report_lines.append("# Anchor Local Flank Classification v4: H4+ with Cluster Features\n")
    report_lines.append(f"Run date: {time.strftime('%Y-%m-%d %H:%M')}\n")
    report_lines.append(f"Proteins with PDB: {len(proteins_with_pdb)}, PDB features computed: {pdb_computed}\n")
    report_lines.append(f"Radius: {RADIUS}, Controls per anchor: {CONTROLS_PER_ANCHOR}\n")
    report_lines.append(f"Structural control pairs: {len(matches)}\n")

    report_lines.append("\n## Results\n")
    report_lines.append(f"{'Model':<25} {'N_prot':<8} {'N_feat':<8} {'Base':<8} {'AUPRC':<8} {'AUROC':<8} {'BalAcc':<8}")
    report_lines.append("-" * 81)

    for key in ["H4_base_L1", "H4_plus_L1", "H4_cluster_only_L1", "H4_bridge_L1", "H4_bridge_only_L1", "H4_plus_GBT", "H4_cluster_only_GBT", "H4_bridge_GBT", "H4_bridge_only_GBT"]:
        if key in all_results:
            r = all_results[key]
            n_prot = r.get("n_proteins", "")
            n_feat = r.get("n_features", "")
            br = r.get("base_rate", np.nan)
            report_lines.append(f"{key:<25} {str(n_prot):<8} {str(n_feat):<8} {br:<8.4f} {r['auprc']:<8.4f} {r['auroc']:<8.4f} {r['bal_acc']:<8.4f}")

    if X_plus is not None and "H4_plus_L1" in all_results:
        report_lines.append(f"\nPermutation test (H4+): p={p_val:.4f}, null 95th pctl={np.percentile(null_auprcs, 95):.4f}")

    report_lines.append("\n## Feature Family Ablation (H4+)\n")
    report_lines.append(f"{'Family':<30} {'AUPRC':<8} {'Drop':<10}")
    report_lines.append("-" * 48)
    if 'ablation_results' in dir():
        for family_name in families:
            if family_name in ablation_results:
                r = ablation_results[family_name]
                drop = baseline_auprc - r["auprc"]
                report_lines.append(f"{family_name:<30} {r['auprc']:<8.4f} {drop:+.4f}")

    report_lines.append("\n## Interpretation\n")
    h4_base = all_results.get("H4_base_L1", {}).get("auprc", np.nan)
    h4_plus = all_results.get("H4_plus_L1", {}).get("auprc", np.nan)
    h4_cluster = all_results.get("H4_cluster_only_L1", {}).get("auprc", np.nan)
    base_rate = all_results.get("H4_base_L1", {}).get("base_rate", 0.167)

    if not np.isnan(h4_plus):
        if h4_plus > 0.55:
            report_lines.append("STRONG SUCCESS: H4+ L1 > 0.55, cluster features substantially help L1 close the GBT gap.")
        elif h4_plus > 0.50:
            report_lines.append("MODERATE SUCCESS: H4+ L1 in 0.50-0.55 range, cluster features modestly improve over H4_base.")
        else:
            report_lines.append("WEAK RESULT: H4+ ≈ H4_base, cluster features don't add much to per-position features.")

    if not np.isnan(h4_cluster):
        if h4_cluster > 0.30:
            report_lines.append(f"H4_cluster_only AUPRC={h4_cluster:.3f} > 0.30: cluster description alone carries signal.")
        else:
            report_lines.append(f"H4_cluster_only AUPRC={h4_cluster:.3f}: cluster description alone is weak.")

    h4_bridge = all_results.get("H4_bridge_L1", {}).get("auprc", np.nan)
    h4_bridge_only = all_results.get("H4_bridge_only_L1", {}).get("auprc", np.nan)
    if not np.isnan(h4_bridge):
        report_lines.append(f"\nH4_bridge L1 AUPRC={h4_bridge:.3f} (base + bridge + H5).")
        if h4_bridge > h4_plus:
            report_lines.append("Bridge features improve over cluster features when added to per-position base.")
        else:
            report_lines.append("Bridge features do not improve over cluster features when added to per-position base.")
    if not np.isnan(h4_bridge_only):
        report_lines.append(f"H4_bridge_only L1 AUPRC={h4_bridge_only:.3f} (bridge + H5 only, {all_results.get('H4_bridge_only_L1', {}).get('n_features', '?')} features).")
        if h4_bridge_only > h4_cluster:
            report_lines.append("Bridge topology alone outperforms cluster summaries — 'structural bridge' is a better description than 'dense cluster'.")

    report_path = REPORT_DIR / "anchor_local_flank_v4.md"
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines) + "\n")

    for line in report_lines:
        flush_print(line)

    flush_print(f"\nReport saved: {report_path}")
    flush_print(f"Total time: {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
