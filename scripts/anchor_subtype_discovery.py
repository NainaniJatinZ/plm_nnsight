#!/usr/bin/env python3
"""Anchor subtype discovery: cluster residues orthogonal to the universal direction.

For each high-confidence protein, extracts layer-10 LN activations at the top-3
anchor residues and matched control residues.  Decomposes each x_i into:
    x_i = alpha_i * d + r_i
where d is the universal search direction and r_i is the orthogonal residual.

Two parallel analyses:
  A. Model-space: PCA -> UMAP -> HDBSCAN on r_i
  B. Structure-space: PCA -> UMAP -> HDBSCAN on structural feature vectors
Then compare cluster assignments between the two.

Usage:
    uv run python scripts/anchor_subtype_discovery.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from scipy import stats as sp_stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDB_DIR = DATA_DIR / "pdb"
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

ANCHOR_POSITIONS = {
    "1BRTA": 220, "1PVGA": 101, "2B61A": 315, "2DPMA": 39,
    "2PKEA": 131, "2QY6A": 64, "2YHWA": 287, "3CSSA": 40,
    "3HO7A": 63, "3OKPA": 200, "3QDLA": 114, "3WJPA": 94,
    "4EHUA": 100, "4EX6A": 124, "4EZIA": 310, "4ME3A": 75,
    "4N9WA": 194, "4OY3A": 193,
}

# Structural feature names for structure-space clustering
STRUCT_FEATURES = [
    "rsa", "contacts_8A", "contacts_10A", "long_range_contacts",
    "long_range_fraction", "mean_contact_span", "max_contact_span",
    "n_contact_bins", "contact_bin_entropy", "n_distinct_sse_partners",
    "contacts_outside_own_sse", "fraction_contacts_outside_own_sse",
    "degree", "betweenness", "closeness", "eigenvector",
    "core_number", "clustering_coeff", "bridge_score",
]


# ---------------------------------------------------------------------------
# Model loading (shared with audit script)
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
        "W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(),
        "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone(),
    }


def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Compute d = W_K^T @ q_mean_norm from a full sequence."""
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


# ---------------------------------------------------------------------------
# PDB download + structural feature extraction
# ---------------------------------------------------------------------------

def download_pdb(pdb_id: str) -> Path | None:
    """Download PDB file from RCSB if not already cached in data/pdb/."""
    PDB_DIR.mkdir(parents=True, exist_ok=True)
    pdb_file = PDB_DIR / f"{pdb_id}.pdb"
    if pdb_file.exists():
        return pdb_file
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        urllib.request.urlretrieve(url, pdb_file)
        return pdb_file
    except Exception:
        return None


def _find_pdb(protein: str) -> tuple[Path | None, str]:
    """Find PDB file for a protein key like '2B61A'. Returns (path, chain_id).

    Checks data/pdb/ first (downloaded from RCSB), then falls back to _EV dirs.
    """
    pdb_id = protein[:4].upper()
    chain_id = protein[4] if len(protein) > 4 else "A"

    # Check downloaded PDBs first
    pdb_file = PDB_DIR / f"{pdb_id}.pdb"
    if pdb_file.exists():
        return pdb_file, chain_id

    # Try downloading
    downloaded = download_pdb(pdb_id)
    if downloaded is not None:
        return downloaded, chain_id

    # Fall back to _EV directory
    ev_dir = DATA_DIR / f"{protein}_EV"
    if ev_dir.exists():
        candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
        candidates = [c for c in candidates if "compare" not in str(c) and "aux" not in str(c)]
        if candidates:
            return candidates[0], chain_id

    return None, chain_id


def _parse_pdb_residues(pdb_path: Path, chain_id: str = "A"):
    """Parse PDB residues for a specific chain."""
    from Bio.PDB import PDBParser
    from Bio.Data.IUPACData import protein_letters_3to1

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("prot", str(pdb_path))

    # Find the requested chain
    chain = None
    for c in structure[0]:
        if c.get_id() == chain_id:
            chain = c
            break
    if chain is None:
        # Fall back to first chain
        chains = list(structure[0])
        if not chains:
            return [], structure
        chain = chains[0]

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


MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


def compute_struct_features_for_positions(protein: str, full_seq: str, positions: list[int]) -> dict[int, dict] | None:
    """Compute structural features for specific sequence positions.

    Returns dict: seq_position -> feature dict, or None if PDB not available.
    """
    from scipy.spatial.distance import cdist
    import networkx as nx

    pdb_path, chain_id = _find_pdb(protein)
    if pdb_path is None:
        return None

    pdb_residues_raw, structure = _parse_pdb_residues(pdb_path, chain_id)
    if not pdb_residues_raw:
        return None

    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues_raw]
    mapping = _align_pdb_to_seq(pdb_tuples, full_seq)
    n_mapped = len(mapping)
    n_total = len(pdb_residues_raw)
    if n_mapped < n_total * 0.5:
        return None

    # Build reverse mapping: seq_pos -> pdb_idx
    seq_to_pdb = {v: k for k, v in mapping.items()}

    # Check which requested positions have PDB data
    valid_positions = [p for p in positions if p in seq_to_pdb]
    if not valid_positions:
        return None

    # RSA
    from Bio.PDB import ShrakeRupley
    sr = ShrakeRupley()
    sr.compute(structure[0], level="R")
    # Find the chain we used for parsing
    target_chain = None
    for c in structure[0]:
        if c.get_id() == chain_id:
            target_chain = c
            break
    if target_chain is None:
        target_chain = list(structure[0])[0]
    sasa_by_resid = {}
    for residue in target_chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa

    # Distance matrix
    cb_coords = np.array([r["cb"] for r in pdb_residues_raw])
    n_pdb = len(pdb_residues_raw)
    dists = cdist(cb_coords, cb_coords)

    # Contact adjacency
    contacts_8A_arr = (dists < 8.0).sum(axis=1) - 1
    contacts_10A_arr = (dists < 10.0).sum(axis=1) - 1
    contact_mask_8A = (dists < 8.0)
    np.fill_diagonal(contact_mask_8A, False)

    long_range_arr = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) > 12 and dists[i, j] < 8.0:
                long_range_arr[i] += 1

    long_range_fraction = long_range_arr / np.maximum(contacts_8A_arr, 1).astype(float)

    mean_contact_span = np.zeros(n_pdb)
    max_contact_span = np.zeros(n_pdb)
    for i in range(n_pdb):
        partners = np.where(contact_mask_8A[i])[0]
        if len(partners) > 0:
            spans = np.abs(partners - i)
            mean_contact_span[i] = spans.mean()
            max_contact_span[i] = spans.max()

    # Contact spread
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
        n_contact_bins_arr[i] = len(set(bin_assignments))
        counts = np.bincount(bin_assignments, minlength=n_bins).astype(float)
        counts = counts[counts > 0]
        probs = counts / counts.sum()
        contact_bin_entropy_arr[i] = float(-np.sum(probs * np.log2(probs)))

    # SSE partners (need ss_dict)
    ss_path = DATA_DIR / "ss_dict.json"
    sse_str = None
    if ss_path.exists():
        with open(ss_path) as f:
            ss_raw = json.load(f)
        for k, v in ss_raw.items():
            prot_key = k.replace(".pdb", "")
            if prot_key == protein:
                sse_str = v.replace("-", "C")
                break

    # SSE segment IDs
    seg_ids = np.full(len(full_seq), -1, dtype=int)
    if sse_str is not None and len(sse_str) == len(full_seq):
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

    pdb_seg_ids = np.full(n_pdb, -1, dtype=int)
    for pdb_idx, seq_pos in mapping.items():
        if seq_pos < len(seg_ids):
            pdb_seg_ids[pdb_idx] = seg_ids[seq_pos]

    n_distinct_sse_partners = np.zeros(n_pdb, dtype=int)
    contacts_outside_own_sse = np.zeros(n_pdb, dtype=int)
    for i in range(n_pdb):
        own_seg = pdb_seg_ids[i]
        partners = np.where(contact_mask_8A[i])[0]
        partner_seg_ids = set()
        for p in partners:
            if pdb_seg_ids[p] != own_seg:
                contacts_outside_own_sse[i] += 1
            if pdb_seg_ids[p] >= 0:
                partner_seg_ids.add(pdb_seg_ids[p])
        partner_seg_ids.discard(own_seg)
        n_distinct_sse_partners[i] = len(partner_seg_ids)
    fraction_contacts_outside_own_sse = contacts_outside_own_sse / np.maximum(contacts_8A_arr, 1).astype(float)

    # Graph centrality
    G = nx.Graph()
    for i in range(n_pdb):
        G.add_node(i)
    for i in range(n_pdb):
        for j in range(i + 1, n_pdb):
            if contact_mask_8A[i, j]:
                G.add_edge(i, j)

    degree_arr = np.array([G.degree(i) for i in range(n_pdb)], dtype=float)
    betweenness_dict = nx.betweenness_centrality(G)
    betweenness_arr = np.array([betweenness_dict[i] for i in range(n_pdb)])
    closeness_dict = nx.closeness_centrality(G)
    closeness_arr = np.array([closeness_dict[i] for i in range(n_pdb)])
    try:
        eigenvector_dict = nx.eigenvector_centrality(G, max_iter=1000)
        eigenvector_arr = np.array([eigenvector_dict[i] for i in range(n_pdb)])
    except Exception:
        eigenvector_arr = np.zeros(n_pdb)
    core_number_dict = nx.core_number(G)
    core_number_arr = np.array([core_number_dict[i] for i in range(n_pdb)], dtype=float)
    clustering_dict = nx.clustering(G)
    clustering_arr = np.array([clustering_dict[i] for i in range(n_pdb)])
    bridge_score_arr = betweenness_arr / np.maximum(degree_arr, 1.0)

    # Assemble features for requested positions
    features = {}
    for seq_pos in valid_positions:
        pdb_idx = seq_to_pdb[seq_pos]
        r = pdb_residues_raw[pdb_idx]
        aa = r["aa"]
        max_asa = MAX_ASA.get(aa, 200)
        raw_sasa = sasa_by_resid.get(r["resid"], 0.0)
        rsa = min(raw_sasa / max_asa, 1.0) if max_asa > 0 else 0.0

        features[seq_pos] = {
            "rsa": rsa,
            "contacts_8A": int(contacts_8A_arr[pdb_idx]),
            "contacts_10A": int(contacts_10A_arr[pdb_idx]),
            "long_range_contacts": int(long_range_arr[pdb_idx]),
            "long_range_fraction": float(long_range_fraction[pdb_idx]),
            "mean_contact_span": float(mean_contact_span[pdb_idx]),
            "max_contact_span": float(max_contact_span[pdb_idx]),
            "n_contact_bins": int(n_contact_bins_arr[pdb_idx]),
            "contact_bin_entropy": float(contact_bin_entropy_arr[pdb_idx]),
            "n_distinct_sse_partners": int(n_distinct_sse_partners[pdb_idx]),
            "contacts_outside_own_sse": int(contacts_outside_own_sse[pdb_idx]),
            "fraction_contacts_outside_own_sse": float(fraction_contacts_outside_own_sse[pdb_idx]),
            "degree": float(degree_arr[pdb_idx]),
            "betweenness": float(betweenness_arr[pdb_idx]),
            "closeness": float(closeness_arr[pdb_idx]),
            "eigenvector": float(eigenvector_arr[pdb_idx]),
            "core_number": float(core_number_arr[pdb_idx]),
            "clustering_coeff": float(clustering_arr[pdb_idx]),
            "bridge_score": float(bridge_score_arr[pdb_idx]),
        }

    return features


# ---------------------------------------------------------------------------
# Extract layer-10 activations for a protein
# ---------------------------------------------------------------------------

@torch.no_grad()
def extract_activations(model, tokenizer, sequence: str, positions: list[int], device: str) -> torch.Tensor | None:
    """Get L10 LN activations at specific sequence positions. Returns (n_pos, 1280)."""
    if len(sequence) < 10:
        return None
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0, 1:-1]  # (n_res, 1280)
    n_res = x_ln.shape[0]
    valid = [p for p in positions if 0 <= p < n_res]
    if not valid:
        return None
    return x_ln[valid]  # (n_valid, 1280)


# ---------------------------------------------------------------------------
# Select high-confidence anchor proteins + their anchor/control residues
# ---------------------------------------------------------------------------

def select_proteins_and_residues(audit_csv: Path, min_rho: float = 0.95, min_top3_mass: float = 0.7, top_k: int = 3):
    """Select high-confidence proteins and identify anchor + control positions.

    For each protein:
      - Anchors: top-k positions by attention (from the audit CSV)
      - Controls: positions ranked 10th-12th by attention (far from anchor, still have structural data)
    """
    df = pd.read_csv(audit_csv)
    # Filter to high-confidence
    mask = (df["rank_corr"] >= min_rho) & (df["top3_key_mass"] >= min_top3_mass)
    hc = df[mask].copy()
    print(f"High-confidence proteins: {len(hc)} / {len(df)} (rho >= {min_rho}, top3_mass >= {min_top3_mass})")

    records = []
    for _, row in hc.iterrows():
        protein = row["protein"]
        positions_str = str(row["top5_positions"])
        positions = [int(x) for x in positions_str.split(";")]
        anchor_positions = positions[:top_k]
        # Controls: positions ranked around 10-12 by attention (middle of distribution)
        # We'll compute these from the full ranking during activation extraction
        records.append({
            "protein": protein,
            "n_res": int(row["n_res"]),
            "anchor_positions": anchor_positions,
            "top3_mass": float(row["top3_key_mass"]),
            "rho": float(row["rank_corr"]),
            "is_known": protein in ANCHOR_POSITIONS,
        })

    return records


# ---------------------------------------------------------------------------
# Projection-mode analysis: what does alpha_i tell us?
# ---------------------------------------------------------------------------

def run_projection_analysis(
    anchor_vecs, control_vecs, anchor_meta, control_meta,
    anchor_struct, control_struct, alpha_anchor, alpha_ctrl,
    d_np, args,
):
    """Analyze the universal projection alpha_i = x_i . d.

    Since alpha is scalar, we can't cluster it. Instead we ask:
    1. What predicts alpha? (AA identity, structural features)
    2. Full x_i UMAP colored by alpha — how does d-variation relate to global structure?
    3. Alpha stratification — do high/low alpha anchors differ structurally?
    """
    import umap
    from scipy.stats import spearmanr, kruskal

    n_anchor = len(anchor_vecs)
    n_ctrl = len(control_vecs)

    print(f"\n{'=' * 70}")
    print(f"Projection-mode analysis: what determines alpha_i = x_i . d?")
    print(f"{'=' * 70}")

    # -----------------------------------------------------------------------
    # 1. Per-AA alpha distributions
    # -----------------------------------------------------------------------
    print("\nStep P1: Per-amino-acid alpha distributions")
    aa_alphas = {}
    for i, meta in enumerate(anchor_meta):
        aa = meta["aa"]
        aa_alphas.setdefault(aa, []).append(alpha_anchor[i])

    aa_summary = []
    for aa in sorted(aa_alphas.keys()):
        vals = np.array(aa_alphas[aa])
        aa_summary.append({
            "aa": aa, "n": len(vals), "mean": vals.mean(), "median": np.median(vals), "std": vals.std(),
        })
    aa_summary.sort(key=lambda x: -x["mean"])
    print("  Top-5 AAs by mean alpha:")
    for s in aa_summary[:5]:
        print(f"    {s['aa']}: mean={s['mean']:.3f}, median={s['median']:.3f}, n={s['n']}")
    print("  Bottom-5 AAs by mean alpha:")
    for s in aa_summary[-5:]:
        print(f"    {s['aa']}: mean={s['mean']:.3f}, median={s['median']:.3f}, n={s['n']}")

    # Kruskal-Wallis test: does AA identity predict alpha?
    aa_groups = [np.array(aa_alphas[aa]) for aa in aa_alphas if len(aa_alphas[aa]) >= 5]
    if len(aa_groups) >= 2:
        kw_stat, kw_p = kruskal(*aa_groups)
        print(f"  Kruskal-Wallis (AA -> alpha): H={kw_stat:.1f}, p={kw_p:.2e}")

    # -----------------------------------------------------------------------
    # 2. Structural feature correlations with alpha
    # -----------------------------------------------------------------------
    print("\nStep P2: Structural feature correlations with alpha")
    valid_struct_idx = [i for i, s in enumerate(anchor_struct) if s is not None]
    struct_corrs = []
    if len(valid_struct_idx) > 50:
        alpha_valid = alpha_anchor[valid_struct_idx]
        for feat in STRUCT_FEATURES:
            feat_vals = np.array([anchor_struct[i][feat] for i in valid_struct_idx])
            if feat_vals.std() < 1e-10:
                continue
            rho, p = spearmanr(alpha_valid, feat_vals)
            struct_corrs.append({"feature": feat, "rho": rho, "p": p, "n": len(valid_struct_idx)})
        struct_corrs.sort(key=lambda x: -abs(x["rho"]))
        print(f"  Top correlations (n={len(valid_struct_idx)} anchors with struct data):")
        for sc in struct_corrs[:10]:
            sig = "***" if sc["p"] < 0.001 else "**" if sc["p"] < 0.01 else "*" if sc["p"] < 0.05 else ""
            print(f"    {sc['feature']:35s}  rho={sc['rho']:+.3f}  p={sc['p']:.2e} {sig}")

    # -----------------------------------------------------------------------
    # 3. Alpha stratification: high/medium/low terciles
    # -----------------------------------------------------------------------
    print("\nStep P3: Alpha stratification (terciles)")
    tercile_edges = np.percentile(alpha_anchor, [33.3, 66.7])
    tercile_labels = np.digitize(alpha_anchor, tercile_edges)  # 0=low, 1=mid, 2=high
    tercile_names = ["low", "mid", "high"]

    tercile_struct_means = {}
    for t in range(3):
        t_idx = np.where(tercile_labels == t)[0]
        t_struct_idx = [i for i in t_idx if i < len(anchor_struct) and anchor_struct[i] is not None]
        if len(t_struct_idx) < 10:
            continue
        means = {}
        for feat in STRUCT_FEATURES:
            vals = [anchor_struct[i][feat] for i in t_struct_idx]
            means[feat] = np.mean(vals)
        tercile_struct_means[tercile_names[t]] = means
        print(f"  {tercile_names[t]} tercile: n={len(t_idx)}, n_struct={len(t_struct_idx)}, alpha range=[{alpha_anchor[t_idx].min():.3f}, {alpha_anchor[t_idx].max():.3f}]")

    # -----------------------------------------------------------------------
    # 4. Anchor-only PCA + UMAP on full x_i
    # -----------------------------------------------------------------------
    print("\nStep P4: Anchor-only PCA + UMAP on full x_i")

    # PCA on anchors only
    n_pca = min(args.n_pca, anchor_vecs.shape[0] - 1, anchor_vecs.shape[1])
    pca_full = PCA(n_components=n_pca, random_state=42)
    anchor_pca = pca_full.fit_transform(anchor_vecs)
    var_full = pca_full.explained_variance_ratio_.cumsum()
    print(f"  PCA on anchor x_i: {n_pca} components, cumulative variance: {var_full[-1]:.3f}")

    # How does d decompose in anchor PCA space?
    d_cos_all = np.array([float(np.dot(pca_full.components_[i], d_np)) for i in range(n_pca)])
    d_cos_abs = np.abs(d_cos_all)
    best_pc = int(np.argmax(d_cos_abs))
    print(f"  |cos(PC1, d)| = {d_cos_abs[0]:.4f}")
    print(f"  Most d-aligned PC: PC{best_pc+1} with |cos| = {d_cos_abs[best_pc]:.4f}")
    # How much of d is captured by the top PCs?
    d_in_pca = np.sum(d_cos_all**2)
    print(f"  Fraction of d in PCA span: {d_in_pca:.4f}")

    # Correlate each PC with alpha
    pc_alpha_corrs = []
    for i in range(min(10, n_pca)):
        rho_val, _ = spearmanr(anchor_pca[:, i], alpha_anchor)
        pc_alpha_corrs.append((i + 1, rho_val))
    print(f"  PC-alpha correlations (top 10):")
    for pc_idx, rho_val in sorted(pc_alpha_corrs, key=lambda x: -abs(x[1])):
        print(f"    PC{pc_idx}: rho={rho_val:+.3f}")

    # UMAP on anchors only
    reducer = umap.UMAP(n_components=2, n_neighbors=min(30, n_anchor - 1), min_dist=0.1, random_state=42)
    anchor_umap = reducer.fit_transform(anchor_pca)
    print(f"  Anchor-only UMAP computed")

    # -----------------------------------------------------------------------
    # 5. Plots
    # -----------------------------------------------------------------------
    print("\nStep P5: Generating plots")
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))

    # Panel A: Per-AA alpha boxplot
    ax = axes[0, 0]
    aa_order = [s["aa"] for s in aa_summary if s["n"] >= 3]
    aa_data = [np.array(aa_alphas[aa]) for aa in aa_order]
    bp = ax.boxplot(aa_data, labels=aa_order, patch_artist=True, showfliers=False, medianprops=dict(color="black"))
    # Color by hydrophobicity
    KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}
    import matplotlib.cm as cm
    kd_vals = [KD.get(aa, 0) for aa in aa_order]
    kd_norm = [(v - min(kd_vals)) / (max(kd_vals) - min(kd_vals) + 1e-8) for v in kd_vals]
    cmap = cm.RdYlBu_r
    for patch, kd in zip(bp["boxes"], kd_norm):
        patch.set_facecolor(cmap(kd))
        patch.set_alpha(0.7)
    ax.set_xlabel("amino acid (sorted by mean alpha)")
    ax.set_ylabel("projection score alpha")
    ax.set_title("A. Alpha by amino acid\n(color = hydrophobicity: red=hydrophobic)")
    ax.axhline(np.median(alpha_anchor), color="gray", linestyle="--", linewidth=0.8)

    # Panel B: Anchor-only UMAP colored by alpha
    ax = axes[0, 1]
    vmin, vmax = np.percentile(alpha_anchor, [2, 98])
    sc = ax.scatter(anchor_umap[:, 0], anchor_umap[:, 1], c=alpha_anchor, s=10, alpha=0.6, cmap="RdBu_r", vmin=vmin, vmax=vmax, rasterized=True)
    plt.colorbar(sc, ax=ax, label="alpha (projection onto d)")
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")
    ax.set_title("B. Anchor-only UMAP, colored by alpha")

    # Panel C: Anchor-only UMAP colored by AA identity
    ax = axes[0, 2]
    aa_class = {"A": "hydrophobic", "V": "hydrophobic", "I": "hydrophobic", "L": "hydrophobic", "M": "hydrophobic", "F": "hydrophobic", "W": "hydrophobic", "P": "hydrophobic", "G": "special", "C": "special", "S": "polar", "T": "polar", "Y": "polar", "N": "polar", "Q": "polar", "D": "charged", "E": "charged", "K": "charged", "R": "charged", "H": "charged"}
    class_colors = {"hydrophobic": "#e06c75", "polar": "#61afef", "charged": "#98c379", "special": "#d19a66"}
    for cls, color in class_colors.items():
        mask = np.array([aa_class.get(anchor_meta[i]["aa"], "special") == cls for i in range(n_anchor)])
        if mask.sum() > 0:
            ax.scatter(anchor_umap[mask, 0], anchor_umap[mask, 1], c=color, s=10, alpha=0.6, label=f"{cls} ({mask.sum()})", rasterized=True)
    ax.legend(fontsize=7, markerscale=2)
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")
    ax.set_title("C. Anchor-only UMAP, colored by AA class")

    # Panel D: Structural correlations with alpha (top features)
    ax = axes[1, 0]
    if struct_corrs:
        top_n = min(12, len(struct_corrs))
        feats = [sc["feature"] for sc in struct_corrs[:top_n]][::-1]
        rhos = [sc["rho"] for sc in struct_corrs[:top_n]][::-1]
        pvals = [sc["p"] for sc in struct_corrs[:top_n]][::-1]
        colors = ["#e06c75" if r > 0 else "#61afef" for r in rhos]
        bars = ax.barh(range(top_n), rhos, color=colors, alpha=0.7)
        ax.set_yticks(range(top_n))
        ax.set_yticklabels(feats, fontsize=7)
        ax.set_xlabel("Spearman rho with alpha")
        ax.axvline(0, color="black", linewidth=0.5)
        # Mark significance
        for i, (r, p) in enumerate(zip(rhos, pvals)):
            sig = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else ""
            ax.text(r + 0.01 * np.sign(r), i, sig, ha="left" if r > 0 else "right", va="center", fontsize=8)
        ax.set_title("D. What structural features predict alpha?")
    else:
        ax.text(0.5, 0.5, "No structural data", ha="center", va="center", transform=ax.transAxes)

    # Panel E: Alpha vs top structural feature (scatter)
    ax = axes[1, 1]
    if struct_corrs and len(valid_struct_idx) > 50:
        best_feat = struct_corrs[0]["feature"]
        feat_vals = np.array([anchor_struct[i][best_feat] for i in valid_struct_idx])
        alpha_valid = alpha_anchor[valid_struct_idx]
        ax.scatter(feat_vals, alpha_valid, s=8, alpha=0.4, rasterized=True)
        # Add trend line
        z = np.polyfit(feat_vals, alpha_valid, 1)
        x_line = np.linspace(feat_vals.min(), feat_vals.max(), 100)
        ax.plot(x_line, np.polyval(z, x_line), "r-", linewidth=1.5)
        ax.set_xlabel(best_feat)
        ax.set_ylabel("alpha")
        ax.set_title(f"E. Alpha vs {best_feat}\n(rho={struct_corrs[0]['rho']:.3f})")
    else:
        ax.text(0.5, 0.5, "No structural data", ha="center", va="center", transform=ax.transAxes)

    # Panel F: Tercile comparison — structural profile
    ax = axes[1, 2]
    if len(tercile_struct_means) >= 2:
        compare_feats = ["rsa", "contacts_8A", "long_range_fraction", "betweenness", "degree", "n_distinct_sse_partners"]
        available_cf = [f for f in compare_feats if f in next(iter(tercile_struct_means.values()))]
        x_pos = np.arange(len(available_cf))
        bar_w = 0.25
        for t_idx, tname in enumerate(["low", "mid", "high"]):
            if tname not in tercile_struct_means:
                continue
            means = tercile_struct_means[tname]
            # Normalize by mid-tercile mean for comparability
            mid_means = tercile_struct_means.get("mid", means)
            ratios = [means[f] / max(abs(mid_means[f]), 1e-8) for f in available_cf]
            ax.bar(x_pos + t_idx * bar_w, ratios, bar_w, label=f"{tname} alpha", alpha=0.8)
        ax.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
        ax.set_xticks(x_pos + bar_w)
        ax.set_xticklabels(available_cf, rotation=45, ha="right", fontsize=7)
        ax.set_ylabel("ratio to mid-tercile")
        ax.legend(fontsize=7)
        ax.set_title("F. Low / mid / high alpha: structural profiles")
    else:
        ax.text(0.5, 0.5, "Insufficient data for terciles", ha="center", va="center", transform=ax.transAxes)

    plt.tight_layout()
    fig_path = REPORT_DIR / "anchor_projection_analysis.png"
    plt.savefig(fig_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {fig_path}")

    # -----------------------------------------------------------------------
    # 6. Write report
    # -----------------------------------------------------------------------
    print("\nStep P6: Writing report")
    report_path = REPORT_DIR / "anchor_projection_analysis.md"
    with open(report_path, "w") as f:
        f.write("# Anchor Projection Analysis: What Determines alpha_i = x_i . d?\n\n")
        f.write(f"High-confidence subset: {len(set(m['protein'] for m in anchor_meta))} proteins.\n")
        f.write(f"Anchor residues: {n_anchor} (top-{args.top_k} per protein, proj >= {args.min_proj}).\n")
        f.write(f"Control residues: {n_ctrl} (median-ranked by projection).\n\n")

        f.write("## Decomposition summary\n\n")
        f.write(f"| Metric | Anchors | Controls |\n")
        f.write(f"|--------|---------|----------|\n")
        f.write(f"| Mean alpha | {alpha_anchor.mean():.3f} | {alpha_ctrl.mean():.3f} |\n")
        f.write(f"| Std alpha | {alpha_anchor.std():.3f} | {alpha_ctrl.std():.3f} |\n")
        f.write(f"| Mean ||x|| | {np.linalg.norm(anchor_vecs, axis=1).mean():.3f} | {np.linalg.norm(control_vecs, axis=1).mean():.3f} |\n\n")

        f.write("## Per-amino-acid alpha\n\n")
        f.write("| AA | N | Mean alpha | Median alpha | Std |\n")
        f.write("|----|----|------------|-------------|-----|\n")
        for s in aa_summary:
            f.write(f"| {s['aa']} | {s['n']} | {s['mean']:.3f} | {s['median']:.3f} | {s['std']:.3f} |\n")
        if len(aa_groups) >= 2:
            f.write(f"\nKruskal-Wallis test (AA -> alpha): H={kw_stat:.1f}, p={kw_p:.2e}.\n")
        f.write("\n")

        f.write("## Structural feature correlations with alpha\n\n")
        if struct_corrs:
            f.write(f"N = {struct_corrs[0]['n']} anchors with structural data.\n\n")
            f.write("| Feature | Spearman rho | p-value |\n")
            f.write("|---------|-------------|----------|\n")
            for sc in struct_corrs:
                f.write(f"| {sc['feature']} | {sc['rho']:+.3f} | {sc['p']:.2e} |\n")
        else:
            f.write("Insufficient structural data.\n")
        f.write("\n")

        f.write("## Alpha tercile structural profiles\n\n")
        if len(tercile_struct_means) >= 2:
            compare_feats = ["rsa", "contacts_8A", "long_range_fraction", "betweenness", "degree", "n_distinct_sse_partners"]
            available_cf = [cf for cf in compare_feats if cf in next(iter(tercile_struct_means.values()))]
            header = "| Tercile | alpha range | " + " | ".join(available_cf) + " |\n"
            sep = "|---------|-------------|" + "|".join(["--------"] * len(available_cf)) + "|\n"
            f.write(header)
            f.write(sep)
            for t in range(3):
                tname = tercile_names[t]
                if tname not in tercile_struct_means:
                    continue
                t_idx = np.where(tercile_labels == t)[0]
                a_min, a_max = alpha_anchor[t_idx].min(), alpha_anchor[t_idx].max()
                vals = " | ".join(f"{tercile_struct_means[tname][cf]:.3f}" for cf in available_cf)
                f.write(f"| {tname} | [{a_min:.2f}, {a_max:.2f}] | {vals} |\n")
        f.write("\n")

        f.write("## How d decomposes in anchor PCA space\n\n")
        f.write(f"|cos(PC1, d)| = {d_cos_abs[0]:.4f}.\n")
        f.write(f"Most d-aligned PC: PC{best_pc+1} with |cos| = {d_cos_abs[best_pc]:.4f}.\n")
        f.write(f"Fraction of d captured by {n_pca} PCs: {d_in_pca:.4f}.\n\n")
        f.write("### PC-alpha correlations\n\n")
        f.write("| PC | rho(PC, alpha) | |cos(PC, d)| |\n")
        f.write("|----|---------------|----------------|\n")
        for pc_idx, rho_val in sorted(pc_alpha_corrs, key=lambda x: -abs(x[1])):
            f.write(f"| PC{pc_idx} | {rho_val:+.3f} | {d_cos_abs[pc_idx-1]:.4f} |\n")
        f.write("\n")

        f.write("![Projection analysis](anchor_projection_analysis.png)\n")

    print(f"  Saved: {report_path}")
    print("\nDone (projection mode).")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--min-rho", type=float, default=0.95)
    parser.add_argument("--min-top3-mass", type=float, default=0.70)
    parser.add_argument("--n-pca", type=int, default=30, help="PCA dimensions before UMAP")
    parser.add_argument("--top-k", type=int, default=3, help="Top-k anchors per protein")
    parser.add_argument("--n-controls", type=int, default=3, help="Controls per protein (median-ranked)")
    parser.add_argument("--max-proteins", type=int, default=500, help="Max proteins to use (0 = all, sorted by confidence)")
    parser.add_argument("--min-proj", type=float, default=0.25, help="Min projection score to count as anchor")
    parser.add_argument("--mode", choices=["residual", "projection"], default="residual", help="residual: cluster r_i (orthogonal). projection: analyze alpha_i (universal direction)")
    parser.add_argument("--from-cache", action="store_true", help="Load cached vectors from .npz instead of re-running forward passes")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    audit_csv = REPORT_DIR / "anchor_behavior_audit.csv"
    cache_path = REPORT_DIR / "anchor_subtype_cache.npz"

    if not audit_csv.exists():
        print(f"ERROR: audit CSV not found at {audit_csv}. Run anchor_behavior_audit.py first.")
        sys.exit(1)

    if args.from_cache and cache_path.exists():
        print("Loading from cache...")
        cache_data = np.load(cache_path, allow_pickle=True)
        anchor_vecs = cache_data["anchor_vecs"]
        control_vecs = cache_data["control_vecs"]
        anchor_meta = cache_data["anchor_meta"].tolist()
        control_meta = cache_data["control_meta"].tolist()
        anchor_struct = cache_data["anchor_struct"].tolist()
        control_struct = cache_data["control_struct"].tolist()
        d_np = cache_data["d_unit"]
        d_unit_t = torch.from_numpy(d_np)
        alpha_anchor = anchor_vecs @ d_np
        alpha_ctrl = control_vecs @ d_np
        r_anchor = anchor_vecs - np.outer(alpha_anchor, d_np)
        r_ctrl = control_vecs - np.outer(alpha_ctrl, d_np)
        print(f"  {len(anchor_vecs)} anchors, {len(control_vecs)} controls loaded")
        print(f"  Anchor alpha: mean={alpha_anchor.mean():.3f}, std={alpha_anchor.std():.3f}")
        print(f"  Control alpha: mean={alpha_ctrl.mean():.3f}, std={alpha_ctrl.std():.3f}")
    else:
        # --- Step 1: Select high-confidence proteins ---
        print("=" * 70)
        print("Step 1: Selecting high-confidence proteins")
        print("=" * 70)
        records = select_proteins_and_residues(audit_csv, args.min_rho, args.min_top3_mass, args.top_k)
        if len(records) < 50:
            print(f"WARNING: only {len(records)} proteins pass filters. Relaxing to rho >= 0.90, mass >= 0.50.")
            records = select_proteins_and_residues(audit_csv, 0.90, 0.50, args.top_k)

        # Sort by confidence (top3_mass * rho) and take top N
        records.sort(key=lambda r: r["top3_mass"] * r["rho"], reverse=True)
        if args.max_proteins > 0 and len(records) > args.max_proteins:
            records = records[:args.max_proteins]
            print(f"  Trimmed to top {args.max_proteins} by confidence (top3_mass * rho)")

        # Pre-download PDB files
        print(f"\nStep 1b: Downloading PDB files for {len(records)} proteins...")
        PDB_DIR.mkdir(parents=True, exist_ok=True)
        n_downloaded = 0
        n_cached = 0
        n_failed = 0
        for rec in records:
            pdb_id = rec["protein"][:4].upper()
            pdb_file = PDB_DIR / f"{pdb_id}.pdb"
            if pdb_file.exists():
                n_cached += 1
                continue
            result = download_pdb(pdb_id)
            if result is not None:
                n_downloaded += 1
            else:
                n_failed += 1
        print(f"  {n_cached} cached, {n_downloaded} downloaded, {n_failed} failed")

        # --- Step 2: Load model, compute search direction ---
        print(f"\nStep 2: Loading model on {args.device}")
        with open(DATA_DIR / "full_seq_dict.json") as f:
            all_seqs = json.load(f)

        model, tokenizer = load_model(args.device)
        weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

        print(f"Computing search direction from {REFERENCE_PROTEIN}...")
        d = compute_search_dir(model, tokenizer, all_seqs[REFERENCE_PROTEIN], weights, args.device)
        d_unit_t = (d / d.norm()).cpu()
        d_np = d_unit_t.numpy()

        # --- Step 3: Extract activations for anchor + control residues ---
        print(f"\nStep 3: Extracting layer-10 activations")
        anchor_vecs = []
        control_vecs = []
        anchor_meta = []
        control_meta = []
        anchor_struct = []
        control_struct = []

        t0 = time.time()
        n_ok = 0
        n_struct_ok = 0

        for idx, rec in enumerate(records):
            protein = rec["protein"]
            if protein not in all_seqs:
                continue
            seq = all_seqs[protein]
            n_res = len(seq)

            anchor_pos = rec["anchor_positions"]

            inputs = tokenizer(seq, return_tensors="pt").to(args.device)
            ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
            with model.trace() as tracer:
                with tracer.invoke(**inputs):
                    cache = tracer.cache(modules=[ln_module])
            ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
            x_ln_full = cache[ln_key].output.detach().cpu()[0, 1:-1]

            proj_all = (x_ln_full @ d_unit_t).numpy()
            proj_rank = np.argsort(-proj_all)
            median_start = n_res // 2 - args.n_controls // 2
            median_end = median_start + args.n_controls
            median_start = max(0, min(median_start, n_res - args.n_controls))
            median_end = min(n_res, median_start + args.n_controls)
            control_pos = proj_rank[median_start:median_end].tolist()

            valid_anchor_pos = []
            for pos in anchor_pos:
                if pos >= n_res:
                    continue
                if float(proj_all[pos]) < args.min_proj:
                    continue
                valid_anchor_pos.append(pos)
                anchor_vecs.append(x_ln_full[pos].numpy())
                anchor_meta.append({
                    "protein": protein, "position": pos, "aa": seq[pos],
                    "proj_score": float(proj_all[pos]),
                    "is_known": rec["is_known"],
                })

            for pos in control_pos:
                if pos >= n_res:
                    continue
                control_vecs.append(x_ln_full[pos].numpy())
                control_meta.append({
                    "protein": protein, "position": pos, "aa": seq[pos],
                    "proj_score": float(proj_all[pos]),
                })

            struct_feats = compute_struct_features_for_positions(protein, seq, valid_anchor_pos + control_pos)
            if struct_feats is not None:
                for pos in valid_anchor_pos:
                    if pos in struct_feats:
                        anchor_struct.append(struct_feats[pos])
                        n_struct_ok += 1
                    else:
                        anchor_struct.append(None)
                for pos in control_pos:
                    if pos in struct_feats:
                        control_struct.append(struct_feats[pos])
                    else:
                        control_struct.append(None)
            else:
                anchor_struct.extend([None] * len(valid_anchor_pos))
                control_struct.extend([None] * len(control_pos))

            n_ok += 1
            if (idx + 1) % 100 == 0:
                elapsed = time.time() - t0
                print(f"  {idx + 1}/{len(records)} proteins processed ({elapsed:.1f}s)")

        elapsed = time.time() - t0
        print(f"  Done: {n_ok} proteins, {len(anchor_vecs)} anchors, {len(control_vecs)} controls ({elapsed:.1f}s)")
        print(f"  Structural features available for {sum(1 for s in anchor_struct if s is not None)} anchors")

        anchor_vecs = np.array(anchor_vecs)
        control_vecs = np.array(control_vecs)

        # Cache to disk
        print(f"\n  Saving cache to {cache_path}...")
        np.savez(cache_path,
                 anchor_vecs=anchor_vecs, control_vecs=control_vecs,
                 anchor_meta=np.array(anchor_meta, dtype=object),
                 control_meta=np.array(control_meta, dtype=object),
                 anchor_struct=np.array(anchor_struct, dtype=object),
                 control_struct=np.array(control_struct, dtype=object),
                 d_unit=d_np)
        print(f"  Cache saved ({cache_path.stat().st_size / 1e6:.1f} MB)")

        # --- Step 4: Decompose into projection + orthogonal residual ---
        print(f"\nStep 4: Decomposing into alpha*d + r_i")

        def decompose(X):
            alpha = X @ d_np
            projection = np.outer(alpha, d_np)
            residual = X - projection
            return alpha, residual

        alpha_anchor, r_anchor = decompose(anchor_vecs)
        alpha_ctrl, r_ctrl = decompose(control_vecs)

        print(f"  Anchor alpha: mean={alpha_anchor.mean():.3f}, std={alpha_anchor.std():.3f}")
        print(f"  Control alpha: mean={alpha_ctrl.mean():.3f}, std={alpha_ctrl.std():.3f}")
        print(f"  Anchor ||r||: mean={np.linalg.norm(r_anchor, axis=1).mean():.3f}")
        print(f"  Control ||r||: mean={np.linalg.norm(r_ctrl, axis=1).mean():.3f}")

    if args.mode == "projection":
        run_projection_analysis(
            anchor_vecs, control_vecs, anchor_meta, control_meta,
            anchor_struct, control_struct, alpha_anchor, alpha_ctrl,
            d_np, args,
        )
        return

    # --- Step 5A: Model-space clustering (on r_i) ---
    print(f"\nStep 5A: Model-space subtype discovery (PCA -> UMAP -> HDBSCAN)")
    import umap
    import hdbscan

    # Combine anchor and control residuals for joint embedding
    all_r = np.vstack([r_anchor, r_ctrl])
    labels = np.array(["anchor"] * len(r_anchor) + ["control"] * len(r_ctrl))
    n_anchor = len(r_anchor)

    # PCA
    n_pca = min(args.n_pca, all_r.shape[0] - 1, all_r.shape[1])
    pca_model = PCA(n_components=n_pca, random_state=42)
    all_pca = pca_model.fit_transform(all_r)
    var_explained = pca_model.explained_variance_ratio_.cumsum()
    print(f"  PCA: {n_pca} components, cumulative variance: {var_explained[-1]:.3f}")
    print(f"  Top-5 PC variance ratios: {pca_model.explained_variance_ratio_[:5].round(4).tolist()}")

    # UMAP
    reducer = umap.UMAP(n_components=2, n_neighbors=30, min_dist=0.1, random_state=42, metric="euclidean")
    all_umap = reducer.fit_transform(all_pca)
    print(f"  UMAP 2D embedding computed")

    # HDBSCAN on PCA space (not UMAP, since UMAP distorts distances)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=max(15, n_anchor // 50), min_samples=5, cluster_selection_method="eom")
    cluster_labels = clusterer.fit_predict(all_pca)
    n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
    n_noise = (cluster_labels == -1).sum()
    print(f"  HDBSCAN: {n_clusters} clusters, {n_noise} noise points ({n_noise / len(cluster_labels) * 100:.1f}%)")

    # Anchor-only cluster stats
    anchor_clusters = cluster_labels[:n_anchor]
    ctrl_clusters = cluster_labels[n_anchor:]
    print(f"  Anchor cluster distribution: {dict(zip(*np.unique(anchor_clusters, return_counts=True)))}")

    # --- Step 5B: Structure-space clustering ---
    print(f"\nStep 5B: Structure-space subtype discovery")

    # Build structure feature matrix for anchors with valid features
    anchor_struct_valid_idx = [i for i, s in enumerate(anchor_struct) if s is not None]
    ctrl_struct_valid_idx = [i for i, s in enumerate(control_struct) if s is not None]

    if len(anchor_struct_valid_idx) < 50:
        print(f"  WARNING: only {len(anchor_struct_valid_idx)} anchors have structural features. Skipping structure-space clustering.")
        struct_clusters = None
        struct_umap = None
    else:
        anchor_struct_mat = np.array([[anchor_struct[i][f] for f in STRUCT_FEATURES] for i in anchor_struct_valid_idx])
        ctrl_struct_mat = np.array([[control_struct[i][f] for f in STRUCT_FEATURES] for i in ctrl_struct_valid_idx])
        all_struct_mat = np.vstack([anchor_struct_mat, ctrl_struct_mat])
        struct_labels_type = np.array(["anchor"] * len(anchor_struct_valid_idx) + ["control"] * len(ctrl_struct_valid_idx))

        # Standardize
        scaler = StandardScaler()
        all_struct_scaled = scaler.fit_transform(all_struct_mat)

        # PCA on struct features
        n_struct_pca = min(15, all_struct_scaled.shape[1], all_struct_scaled.shape[0] - 1)
        struct_pca_model = PCA(n_components=n_struct_pca, random_state=42)
        all_struct_pca = struct_pca_model.fit_transform(all_struct_scaled)
        struct_var = struct_pca_model.explained_variance_ratio_.cumsum()
        print(f"  Struct PCA: {n_struct_pca} components, cumulative variance: {struct_var[-1]:.3f}")

        # UMAP
        struct_reducer = umap.UMAP(n_components=2, n_neighbors=30, min_dist=0.1, random_state=42)
        struct_umap = struct_reducer.fit_transform(all_struct_pca)

        # HDBSCAN
        struct_clusterer = hdbscan.HDBSCAN(min_cluster_size=max(15, len(anchor_struct_valid_idx) // 50), min_samples=5, cluster_selection_method="eom")
        struct_clusters = struct_clusterer.fit_predict(all_struct_pca)
        n_struct_clusters = len(set(struct_clusters)) - (1 if -1 in struct_clusters else 0)
        n_struct_noise = (struct_clusters == -1).sum()
        print(f"  HDBSCAN: {n_struct_clusters} clusters, {n_struct_noise} noise ({n_struct_noise / len(struct_clusters) * 100:.1f}%)")

    # --- Step 6: Cluster enrichment analysis ---
    print(f"\nStep 6: Cluster enrichment analysis (model-space)")

    # For each model-space cluster, compute mean structural features of anchors in that cluster
    enrichment_rows = []
    for cl in sorted(set(anchor_clusters)):
        if cl == -1:
            continue
        member_idx = np.where(anchor_clusters == cl)[0]
        n_members = len(member_idx)
        # Mean projection score
        mean_alpha = float(alpha_anchor[member_idx].mean())
        # Amino acid composition
        aa_counts = {}
        for i in member_idx:
            aa = anchor_meta[i]["aa"]
            aa_counts[aa] = aa_counts.get(aa, 0) + 1
        top_aa = sorted(aa_counts.items(), key=lambda x: -x[1])[:5]
        top_aa_str = ", ".join(f"{aa}({c})" for aa, c in top_aa)

        # Structural feature means (for members with struct data)
        struct_means = {}
        struct_member_count = 0
        for i in member_idx:
            if i < len(anchor_struct) and anchor_struct[i] is not None:
                struct_member_count += 1
                for f in STRUCT_FEATURES:
                    struct_means[f] = struct_means.get(f, 0.0) + anchor_struct[i][f]
        if struct_member_count > 0:
            for f in STRUCT_FEATURES:
                struct_means[f] /= struct_member_count

        enrichment_rows.append({
            "cluster": cl,
            "n_members": n_members,
            "mean_alpha": mean_alpha,
            "top_aa": top_aa_str,
            "n_struct": struct_member_count,
            **{f"mean_{f}": struct_means.get(f, float("nan")) for f in STRUCT_FEATURES},
        })

    enrichment_df = pd.DataFrame(enrichment_rows)

    # --- Step 7: Compare model-space vs structure-space clusters ---
    print(f"\nStep 7: Model-space vs structure-space comparison")
    if struct_clusters is not None:
        # Only compare anchors that have both model-space and structure-space labels
        model_labels_for_struct = anchor_clusters[anchor_struct_valid_idx]
        struct_labels_anchors = struct_clusters[:len(anchor_struct_valid_idx)]
        # Filter out noise from both
        both_valid = (model_labels_for_struct != -1) & (struct_labels_anchors != -1)
        if both_valid.sum() > 20:
            ari = adjusted_rand_score(model_labels_for_struct[both_valid], struct_labels_anchors[both_valid])
            nmi = normalized_mutual_info_score(model_labels_for_struct[both_valid], struct_labels_anchors[both_valid])
            print(f"  ARI (model vs struct clusters): {ari:.4f}")
            print(f"  NMI (model vs struct clusters): {nmi:.4f}")
        else:
            ari, nmi = float("nan"), float("nan")
            print(f"  Too few non-noise points ({both_valid.sum()}) for cross-comparison")
    else:
        ari, nmi = float("nan"), float("nan")

    # --- Step 8: Plots ---
    print(f"\nStep 8: Generating plots")
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel A: Model-space UMAP colored by cluster
    ax = axes[0, 0]
    scatter = ax.scatter(all_umap[n_anchor:, 0], all_umap[n_anchor:, 1], c="lightgray", s=8, alpha=0.3, label="control", rasterized=True)
    for cl in sorted(set(anchor_clusters)):
        mask = anchor_clusters == cl
        label = f"cluster {cl}" if cl >= 0 else "noise"
        ax.scatter(all_umap[:n_anchor][mask, 0], all_umap[:n_anchor][mask, 1], s=15, alpha=0.7, label=label, rasterized=True)
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")
    ax.set_title(f"A. Model-space (orthogonal residual r_i)\n{n_clusters} clusters, {n_noise} noise")
    ax.legend(fontsize=7, loc="best", markerscale=1.5)

    # Panel B: Model-space UMAP colored by projection score alpha
    ax = axes[0, 1]
    all_alpha = np.concatenate([alpha_anchor, alpha_ctrl])
    vmin, vmax = np.percentile(all_alpha, [5, 95])
    sc = ax.scatter(all_umap[:, 0], all_umap[:, 1], c=all_alpha, s=8, alpha=0.5, cmap="RdBu_r", vmin=vmin, vmax=vmax, rasterized=True)
    plt.colorbar(sc, ax=ax, label="projection score alpha")
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")
    ax.set_title("B. Colored by universal projection alpha")

    # Panel C: Structure-space UMAP (if available)
    ax = axes[1, 0]
    if struct_umap is not None and struct_clusters is not None:
        n_struct_anchor = len(anchor_struct_valid_idx)
        ax.scatter(struct_umap[n_struct_anchor:, 0], struct_umap[n_struct_anchor:, 1], c="lightgray", s=8, alpha=0.3, label="control", rasterized=True)
        struct_anchor_clusters = struct_clusters[:n_struct_anchor]
        for cl in sorted(set(struct_anchor_clusters)):
            mask = struct_anchor_clusters == cl
            label = f"cluster {cl}" if cl >= 0 else "noise"
            ax.scatter(struct_umap[:n_struct_anchor][mask, 0], struct_umap[:n_struct_anchor][mask, 1], s=15, alpha=0.7, label=label, rasterized=True)
        n_sc = len(set(struct_clusters)) - (1 if -1 in struct_clusters else 0)
        ax.set_title(f"C. Structure-space\n{n_sc} clusters")
        ax.legend(fontsize=7, loc="best", markerscale=1.5)
    else:
        ax.text(0.5, 0.5, "Insufficient structural data", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("C. Structure-space (N/A)")
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")

    # Panel D: Cluster enrichment — bar chart comparing cluster means to population mean
    ax = axes[1, 1]
    display_features = ["mean_rsa", "mean_contacts_8A", "mean_long_range_fraction", "mean_betweenness", "mean_degree", "mean_n_distinct_sse_partners"]
    available = [f for f in display_features if f in enrichment_df.columns]
    # Compute population means from all anchors with struct data
    pop_means = {}
    pop_count = 0
    for s in anchor_struct:
        if s is not None:
            pop_count += 1
            for feat in STRUCT_FEATURES:
                pop_means[feat] = pop_means.get(feat, 0.0) + s[feat]
    if pop_count > 0:
        for feat in STRUCT_FEATURES:
            pop_means[feat] /= pop_count

    valid_enrichment = enrichment_df[enrichment_df["n_struct"] > 0]
    if len(valid_enrichment) >= 1 and pop_count > 0:
        short_names = [f.replace("mean_", "") for f in available]
        x_pos = np.arange(len(available))
        bar_width = 0.8 / (len(valid_enrichment) + 1)
        # Plot population mean as reference
        pop_vals = [pop_means.get(f.replace("mean_", ""), 0) for f in available]
        # Normalize each feature by pop mean for comparability
        for i, (_, row) in enumerate(valid_enrichment.iterrows()):
            cl_vals = []
            for f in available:
                feat_name = f.replace("mean_", "")
                pop_v = pop_means.get(feat_name, 1e-8)
                cl_v = row[f] if not pd.isna(row[f]) else 0
                cl_vals.append(cl_v / max(abs(pop_v), 1e-8))
            ax.bar(x_pos + i * bar_width, cl_vals, bar_width, label=f"cl {int(row['cluster'])} (n={int(row['n_members'])})", alpha=0.8)
        # Reference line at 1.0 (population mean)
        ax.axhline(1.0, color="black", linestyle="--", linewidth=0.8, alpha=0.5, label="all anchors")
        ax.set_xticks(x_pos + bar_width * len(valid_enrichment) / 2)
        ax.set_xticklabels(short_names, rotation=45, ha="right", fontsize=7)
        ax.set_ylabel("ratio to population mean")
        ax.legend(fontsize=7, loc="best")
        ax.set_title("D. Structural enrichment per cluster")
    else:
        ax.text(0.5, 0.5, f"Insufficient structural data\n({pop_count} anchors with struct)", ha="center", va="center", transform=ax.transAxes)
        ax.set_title("D. Cluster enrichment (N/A)")

    plt.tight_layout()
    fig_path = REPORT_DIR / "anchor_subtype_discovery.png"
    plt.savefig(fig_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {fig_path}")

    # --- Step 9: Write report ---
    print(f"\nStep 9: Writing report")
    report_path = REPORT_DIR / "anchor_subtype_discovery.md"
    with open(report_path, "w") as f:
        f.write("# Anchor Subtype Discovery\n\n")
        f.write(f"High-confidence subset: {n_ok} proteins (rho >= {args.min_rho}, top-3 mass >= {args.min_top3_mass}).\n")
        f.write(f"Anchor residues: {len(anchor_vecs)} (top-{args.top_k} per protein, proj >= {args.min_proj}).\n")
        f.write(f"Control residues: {len(control_vecs)} (median-ranked by projection).\n")
        f.write(f"Search direction d from {REFERENCE_PROTEIN}.\n\n")

        f.write("## Decomposition: x_i = alpha_i * d + r_i\n\n")
        f.write(f"| Metric | Anchors | Controls |\n")
        f.write(f"|--------|---------|----------|\n")
        f.write(f"| Mean alpha | {alpha_anchor.mean():.3f} | {alpha_ctrl.mean():.3f} |\n")
        f.write(f"| Std alpha | {alpha_anchor.std():.3f} | {alpha_ctrl.std():.3f} |\n")
        f.write(f"| Mean ||r|| | {np.linalg.norm(r_anchor, axis=1).mean():.3f} | {np.linalg.norm(r_ctrl, axis=1).mean():.3f} |\n\n")

        f.write("## A. Model-space clustering (PCA -> UMAP -> HDBSCAN on r_i)\n\n")
        f.write(f"PCA: {n_pca} components, cumulative variance explained: {var_explained[-1]:.3f}.\n")
        f.write(f"Top-5 PC variance ratios: {pca_model.explained_variance_ratio_[:5].round(4).tolist()}.\n\n")
        f.write(f"HDBSCAN found {n_clusters} clusters with {n_noise} noise points ({n_noise / len(cluster_labels) * 100:.1f}%).\n\n")

        f.write("### Cluster summary\n\n")
        f.write("| Cluster | N anchors | Mean alpha | Top AAs |\n")
        f.write("|---------|-----------|------------|---------|\n")
        for _, row in enrichment_df.iterrows():
            f.write(f"| {int(row['cluster'])} | {int(row['n_members'])} | {row['mean_alpha']:.3f} | {row['top_aa']} |\n")
        f.write("\n")

        if len(enrichment_df) > 1:
            f.write("### Structural enrichment per cluster\n\n")
            key_feats = ["mean_rsa", "mean_contacts_8A", "mean_long_range_fraction", "mean_betweenness", "mean_degree", "mean_n_distinct_sse_partners"]
            available_key = [feat for feat in key_feats if feat in enrichment_df.columns]
            header = "| Cluster | " + " | ".join(f.replace("mean_", "") for f in available_key) + " |\n"
            sep = "|---------|" + "|".join(["--------"] * len(available_key)) + "|\n"
            f.write(header)
            f.write(sep)
            for _, row in enrichment_df.iterrows():
                vals = " | ".join(f"{row[feat]:.3f}" if not pd.isna(row[feat]) else "N/A" for feat in available_key)
                f.write(f"| {int(row['cluster'])} | {vals} |\n")
            f.write("\n")

        f.write("## B. Structure-space clustering\n\n")
        if struct_clusters is not None:
            n_sc = len(set(struct_clusters)) - (1 if -1 in struct_clusters else 0)
            n_sn = (struct_clusters == -1).sum()
            f.write(f"Features: {len(STRUCT_FEATURES)} structural descriptors.\n")
            f.write(f"HDBSCAN found {n_sc} clusters with {n_sn} noise points.\n\n")
        else:
            f.write("Insufficient structural data for structure-space clustering.\n\n")

        f.write("## Model vs structure comparison\n\n")
        if not np.isnan(ari):
            f.write(f"Adjusted Rand Index: {ari:.4f}.\n")
            f.write(f"Normalized Mutual Information: {nmi:.4f}.\n\n")
            if ari < 0.1:
                f.write("Model-space and structure-space clusters show low agreement, suggesting the orthogonal variation captured by the model is not simply recapitulating structural similarity.\n\n")
            elif ari > 0.3:
                f.write("Moderate-to-strong agreement between model-space and structure-space clusters, suggesting the model's orthogonal representation partially reflects structural context.\n\n")
        else:
            f.write("Comparison not possible (insufficient overlapping non-noise points).\n\n")

        f.write("![Subtype discovery](anchor_subtype_discovery.png)\n")

    print(f"  Saved: {report_path}")

    # Save per-residue data
    csv_path = REPORT_DIR / "anchor_subtype_discovery.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["protein", "position", "aa", "type", "proj_score", "model_cluster", "alpha", "residual_norm"])
        for i, meta in enumerate(anchor_meta):
            writer.writerow([
                meta["protein"], meta["position"], meta["aa"], "anchor",
                f"{meta['proj_score']:.4f}", int(anchor_clusters[i]),
                f"{alpha_anchor[i]:.4f}", f"{np.linalg.norm(r_anchor[i]):.4f}",
            ])
        for i, meta in enumerate(control_meta):
            writer.writerow([
                meta["protein"], meta["position"], meta["aa"], "control",
                f"{meta['proj_score']:.4f}", int(ctrl_clusters[i]),
                f"{alpha_ctrl[i]:.4f}", f"{np.linalg.norm(r_ctrl[i]):.4f}",
            ])
    print(f"  Saved: {csv_path}")

    print(f"\nDone.")


if __name__ == "__main__":
    main()
