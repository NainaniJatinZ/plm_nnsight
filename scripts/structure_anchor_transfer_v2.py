#!/usr/bin/env python3
"""Structure anchor transfer v2: expanded dataset with deduplication, top-3 concordance, and motif analysis.

Repeats the v1 structure anchor transfer experiment on a larger dataset (98 entries,
66 unique PDB IDs) from Foldseek top-2 hits for 1PVGA (TM > 0.6, seq id < 0.20),
with proper deduplication at 90% global identity.

Phases:
  0. Data preparation: parse alignment, collapse assemblies, deduplicate, download PDBs, generate 3Di.
  1. Anchor behavior audit: reference direction from 1PVGA, forward pass, gating.
  2. Top-1 anchor column concordance + random control + projection transfer.
  3. Top-3 anchor column concordance: consensus columns, set overlap.
  4. Local sequence conservation around anchor columns.
  5. AA flank motif analysis (PWM, IC, sequence logo).
  6. 3Di flank motif analysis (PWM, IC, sequence logo).

Usage:
    uv run python scripts/structure_anchor_transfer_v2.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy import stats as sp_stats
from scipy.cluster.hierarchy import linkage, fcluster

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
FOLDMASON_DIR = DATA_DIR / "foldmason_top2_tm_gt_06_seq_lt_02"
PDB_DIR = DATA_DIR / "pdb"
FOLDSEEK_BIN = ROOT / "foldseek" / "bin" / "foldseek"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN_1PVG = "1PVGA"
REFERENCE_PROTEIN_2B61 = "2B61A"
REFERENCE_ANCHOR_POS = 101  # 1PVGA known anchor (0-indexed in ungapped sequence)

ANCHOR_TOP1_THRESH = 0.15
ANCHOR_RANKCORR_THRESH = 0.3

DEDUP_IDENTITY_THRESHOLD = 0.90

STANDARD_AA = "ACDEFGHIKLMNPQRSTVWY"
AA_TO_IDX = {aa: i for i, aa in enumerate(STANDARD_AA)}
HYDROPHOBIC = set("VILFMAW")

AA_COLORS = {
    'A': '#0000CC', 'V': '#0000CC', 'I': '#0000CC', 'L': '#0000CC', 'M': '#0000CC',
    'F': '#0000CC', 'W': '#0000CC',
    'D': '#CC0000', 'E': '#CC0000',
    'K': '#CC0000', 'R': '#CC0000', 'H': '#CC0000',
    'S': '#00CC00', 'T': '#00CC00', 'N': '#00CC00', 'Q': '#00CC00',
    'G': '#CC8800', 'P': '#CC8800', 'C': '#CC8800', 'Y': '#00CC00',
}

DI_ALPHABET = "ACDEFGHIKLMNPQRSTVWY"
DI_TO_IDX = {c: i for i, c in enumerate(DI_ALPHABET)}
_CORE_3DI = set("AEGHIKMTVY")
DI_COLORS = {c: ("#1f77b4" if c in _CORE_3DI else "#d62728") for c in DI_ALPHABET}


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
    return {
        "W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(),
        "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone(),
    }


def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Compute d = W_K^T @ q_mean from a full (unmasked) sequence."""
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
# Phase 0: Data preparation
# ---------------------------------------------------------------------------

def parse_fasta_alignment(fasta_path: Path) -> dict[str, str]:
    records = {}
    current_header = None
    current_seq = []
    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if current_header is not None:
                    records[current_header] = "".join(current_seq)
                current_header = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
    if current_header is not None:
        records[current_header] = "".join(current_seq)
    return records


def build_alignment_mappings(aligned_seqs: dict[str, str]):
    ungapped_seqs = {}
    col_to_pos = {}
    pos_to_col = {}
    for name, aligned in aligned_seqs.items():
        ungapped = aligned.replace("-", "")
        ungapped_seqs[name] = ungapped
        c2p = []
        p2c = []
        pos = 0
        for col_idx, char in enumerate(aligned):
            if char == "-":
                c2p.append(-1)
            else:
                c2p.append(pos)
                p2c.append(col_idx)
                pos += 1
        col_to_pos[name] = c2p
        pos_to_col[name] = p2c
    return ungapped_seqs, col_to_pos, pos_to_col


def extract_pdb_id(name: str) -> str:
    """Extract PDB ID from foldmason header like '1ei1-assembly1cifgz'."""
    return name.split("-")[0]


def collapse_assemblies(aligned_seqs: dict[str, str]) -> dict[str, str]:
    """Keep one representative per PDB ID (longest ungapped sequence)."""
    pdb_groups: dict[str, list[tuple[str, str]]] = {}
    for name, aligned in aligned_seqs.items():
        pdb_id = extract_pdb_id(name)
        pdb_groups.setdefault(pdb_id, []).append((name, aligned))

    kept = {}
    collapsed_log = []
    for pdb_id, entries in pdb_groups.items():
        best_name, best_aligned = max(entries, key=lambda x: len(x[1].replace("-", "")))
        kept[best_name] = best_aligned
        if len(entries) > 1:
            dropped = [n for n, _ in entries if n != best_name]
            collapsed_log.append((pdb_id, best_name, dropped))
    return kept, collapsed_log


def compute_pairwise_identity(aligned_seqs: dict[str, str]) -> dict[tuple[str, str], float]:
    names = list(aligned_seqs.keys())
    identities = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = aligned_seqs[names[i]]
            b = aligned_seqs[names[j]]
            aligned_count = 0
            match_count = 0
            for ca, cb in zip(a, b):
                if ca != "-" and cb != "-":
                    aligned_count += 1
                    if ca == cb:
                        match_count += 1
            identity = match_count / max(aligned_count, 1)
            identities[(names[i], names[j])] = identity
            identities[(names[j], names[i])] = identity
    return identities


def deduplicate_by_identity(aligned_seqs: dict[str, str], threshold: float = 0.90):
    """Cluster proteins by single-linkage at given identity threshold. Keep longest per cluster."""
    names = list(aligned_seqs.keys())
    n = len(names)
    if n <= 1:
        return aligned_seqs, [], {}

    identities = compute_pairwise_identity(aligned_seqs)

    # Build condensed distance matrix (1 - identity)
    from scipy.spatial.distance import squareform
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist_matrix[i, j] = 1.0 - identities[(names[i], names[j])]
            dist_matrix[j, i] = dist_matrix[i, j]
    condensed = squareform(dist_matrix)

    Z = linkage(condensed, method="single")
    clusters = fcluster(Z, t=1.0 - threshold, criterion="distance")

    # Keep longest per cluster
    cluster_groups: dict[int, list[str]] = {}
    for name, cl in zip(names, clusters):
        cluster_groups.setdefault(cl, []).append(name)

    kept = {}
    dedup_log = []
    for cl, members in cluster_groups.items():
        best = max(members, key=lambda n: len(aligned_seqs[n].replace("-", "")))
        kept[best] = aligned_seqs[best]
        if len(members) > 1:
            dropped = [m for m in members if m != best]
            dedup_log.append((best, dropped))

    return kept, dedup_log, identities


def download_pdbs(pdb_ids: list[str], out_dir: Path):
    """Download PDB files from RCSB for each PDB ID."""
    import requests
    out_dir.mkdir(parents=True, exist_ok=True)
    for pdb_id in pdb_ids:
        upper = pdb_id.upper()
        out_path = out_dir / f"{upper}.pdb"
        if out_path.exists():
            continue
        url = f"https://files.rcsb.org/download/{upper}.pdb"
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            with open(out_path, "wb") as f:
                f.write(resp.content)
            print(f"  Downloaded {upper}.pdb")
        except Exception as e:
            # Try CIF format as fallback
            url_cif = f"https://files.rcsb.org/download/{pdb_id.lower()}.cif"
            try:
                resp = requests.get(url_cif, timeout=30)
                resp.raise_for_status()
                cif_path = out_dir / f"{upper}.cif"
                with open(cif_path, "wb") as f:
                    f.write(resp.content)
                print(f"  Downloaded {upper}.cif (PDB format not available)")
            except Exception as e2:
                print(f"  WARNING: failed to download {upper}: PDB={e}, CIF={e2}")


def generate_3di_sequences(pdb_ids: list[str], pdb_dir: Path, out_dir: Path) -> dict[str, str]:
    """Generate 3Di sequences using foldseek for each PDB."""
    out_dir.mkdir(parents=True, exist_ok=True)
    three_di_seqs = {}

    # Collect all PDB/CIF files that exist
    pdb_files = []
    for pdb_id in pdb_ids:
        upper = pdb_id.upper()
        pdb_path = pdb_dir / f"{upper}.pdb"
        cif_path = pdb_dir / f"{upper}.cif"
        if pdb_path.exists():
            pdb_files.append((pdb_id, pdb_path))
        elif cif_path.exists():
            pdb_files.append((pdb_id, cif_path))
        else:
            print(f"  WARNING: no structure file for {upper}")

    if not pdb_files:
        return three_di_seqs

    # Create a temporary directory with symlinks for batch processing
    tmp_dir = out_dir / "_tmp_pdb"
    tmp_dir.mkdir(exist_ok=True)
    for pdb_id, pdb_path in pdb_files:
        link = tmp_dir / pdb_path.name
        if not link.exists():
            link.symlink_to(pdb_path)

    db_prefix = out_dir / "v2_db"
    fasta_out = out_dir / "v2_3di.fa"

    # Run foldseek createdb
    print("  Running foldseek createdb...")
    result = subprocess.run(
        [str(FOLDSEEK_BIN), "createdb", str(tmp_dir), str(db_prefix)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  foldseek createdb failed: {result.stderr[:500]}")
        return three_di_seqs

    # Link headers for 3Di extraction
    ss_h = str(db_prefix) + "_ss_h"
    h = str(db_prefix) + "_h"
    if not Path(ss_h).exists():
        subprocess.run([str(FOLDSEEK_BIN), "lndb", h, ss_h], capture_output=True)

    # Convert 3Di to FASTA
    ss_db = str(db_prefix) + "_ss"
    print("  Running foldseek convert2fasta...")
    result = subprocess.run(
        [str(FOLDSEEK_BIN), "convert2fasta", ss_db, str(fasta_out)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  foldseek convert2fasta failed: {result.stderr[:500]}")
        return three_di_seqs

    # Parse the output FASTA
    if fasta_out.exists():
        with open(fasta_out) as f:
            name, seq = None, []
            for line in f:
                line = line.strip()
                if line.startswith(">"):
                    if name is not None:
                        three_di_seqs[name] = "".join(seq)
                    name = line[1:].split()[0]
                    seq = []
                else:
                    seq.append(line)
            if name is not None:
                three_di_seqs[name] = "".join(seq)

    # Clean up temp directory
    for link in tmp_dir.iterdir():
        link.unlink()
    tmp_dir.rmdir()

    print(f"  Generated 3Di sequences for {len(three_di_seqs)} structures")
    return three_di_seqs


# ---------------------------------------------------------------------------
# Phase 1: Anchor behavior analysis
# ---------------------------------------------------------------------------

@torch.no_grad()
def analyze_protein(model, tokenizer, protein_id: str, sequence: str, d_ref: torch.Tensor, weights: dict, device: str) -> dict | None:
    if len(sequence) < 10:
        return None

    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    n_res = len(sequence)

    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=[attn_module, ln_module])

    attn_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"

    attn_all_heads = cache[attn_key].output[1].detach().cpu()[0]
    A = attn_all_heads[TARGET_HEAD, 1:-1, 1:-1].clone()
    x_ln = cache[ln_key].output.detach().cpu()[0, 1:-1]

    proj_scores = (x_ln @ d_ref.cpu()).numpy()

    # Protein-specific search direction
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q
    q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    d_self = W_K.T @ q_mean_norm
    d_self_unit = d_self / d_self.norm().clamp(min=1e-8)
    d_ref_unit = d_ref.cpu() / d_ref.cpu().norm().clamp(min=1e-8)
    cos_sim_d = float(torch.dot(d_self_unit, d_ref_unit))

    # Verticality metrics
    mean_key_dist = A.mean(dim=0).numpy()
    mean_key_dist_sorted = np.sort(mean_key_dist)[::-1]
    top1_mass = float(mean_key_dist_sorted[0])
    top3_mass = float(mean_key_dist_sorted[:min(3, n_res)].sum())
    p = mean_key_dist / (mean_key_dist.sum() + 1e-12)
    entropy = -float(np.sum(p * np.log(p + 1e-12)))
    eff_keys = float(np.exp(entropy))

    # Projection-attention agreement
    attn_rank = np.argsort(-mean_key_dist)
    proj_rank = np.argsort(-proj_scores)
    rho, rho_p = sp_stats.spearmanr(mean_key_dist, proj_scores)
    attn_top3_set = set(attn_rank[:3].tolist())
    proj_top3_set = set(proj_rank[:3].tolist())
    top3_overlap = len(attn_top3_set & proj_top3_set) / 3.0

    anchor_pos = int(attn_rank[0])
    top3_positions = attn_rank[:3].tolist()
    top5_positions = attn_rank[:5].tolist()

    return {
        "protein": protein_id,
        "n_res": n_res,
        "top1_mass": top1_mass,
        "top3_mass": top3_mass,
        "eff_keys": eff_keys,
        "rank_corr": float(rho),
        "rank_corr_p": float(rho_p),
        "top3_overlap": top3_overlap,
        "cos_sim_d": cos_sim_d,
        "anchor_pos": anchor_pos,
        "anchor_aa": sequence[anchor_pos] if anchor_pos < len(sequence) else "?",
        "top3_positions": top3_positions,
        "top5_positions": top5_positions,
        "proj_scores": proj_scores,
        "mean_key_dist": mean_key_dist,
        "is_anchor_like": top1_mass > ANCHOR_TOP1_THRESH and float(rho) > ANCHOR_RANKCORR_THRESH,
    }


# ---------------------------------------------------------------------------
# Phase 2: Top-1 concordance
# ---------------------------------------------------------------------------

def anchor_column_concordance(results: list[dict], pos_to_col: dict, names: list[str]):
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    pairs = []
    anchor_like_names = [n for n in names if n in result_map]
    for i in range(len(anchor_like_names)):
        for j in range(i + 1, len(anchor_like_names)):
            na, nb = anchor_like_names[i], anchor_like_names[j]
            ra, rb = result_map[na], result_map[nb]
            pos_a, pos_b = ra["anchor_pos"], rb["anchor_pos"]
            if pos_a >= len(pos_to_col[na]) or pos_b >= len(pos_to_col[nb]):
                continue
            col_a = pos_to_col[na][pos_a]
            col_b = pos_to_col[nb][pos_b]
            pairs.append({
                "protein_a": na, "protein_b": nb,
                "anchor_pos_a": pos_a, "anchor_pos_b": pos_b,
                "anchor_col_a": col_a, "anchor_col_b": col_b,
                "col_distance": abs(col_a - col_b),
            })
    return pairs


def random_position_control(results: list[dict], pos_to_col: dict, names: list[str], n_trials: int = 200, seed: int = 42):
    rng = np.random.RandomState(seed)
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]
    if len(anchor_like_names) < 2:
        return None, None

    anchor_cols = []
    for n in anchor_like_names:
        pos = result_map[n]["anchor_pos"]
        if pos < len(pos_to_col[n]):
            anchor_cols.append(pos_to_col[n][pos])

    random_mean_dists = []
    for _ in range(n_trials):
        random_cols = []
        for n in anchor_like_names:
            n_res = result_map[n]["n_res"]
            anchor_pos = result_map[n]["anchor_pos"]
            candidates = [p for p in range(n_res) if p != anchor_pos and p < len(pos_to_col[n])]
            if not candidates:
                continue
            rp = rng.choice(candidates)
            random_cols.append(pos_to_col[n][rp])
        if len(random_cols) >= 2:
            dists = [abs(random_cols[a] - random_cols[b]) for a in range(len(random_cols)) for b in range(a + 1, len(random_cols))]
            random_mean_dists.append(np.mean(dists))

    anchor_dists = [abs(anchor_cols[a] - anchor_cols[b]) for a in range(len(anchor_cols)) for b in range(a + 1, len(anchor_cols))]
    anchor_mean_dist = np.mean(anchor_dists) if anchor_dists else float("nan")
    return anchor_mean_dist, np.array(random_mean_dists)


def projection_score_transfer(results: list[dict], pos_to_col: dict, col_to_pos: dict, names: list[str]):
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]
    transfers = []
    for na in anchor_like_names:
        ra = result_map[na]
        pos_a = ra["anchor_pos"]
        if pos_a >= len(pos_to_col[na]):
            continue
        col_a = pos_to_col[na][pos_a]
        for nb in anchor_like_names:
            if na == nb:
                continue
            rb = result_map[nb]
            if col_a >= len(col_to_pos[nb]):
                continue
            pos_b_at_col = col_to_pos[nb][col_a]
            if pos_b_at_col == -1:
                transfers.append({"source": na, "target": nb, "source_anchor_col": col_a, "target_pos": -1, "target_proj_rank": -1, "is_gap": True, "in_top1": False, "in_top3": False, "in_top5": False, "in_top10": False})
                continue
            proj_scores_b = rb["proj_scores"]
            proj_rank_b = np.argsort(np.argsort(-proj_scores_b))
            rank_at_transfer = int(proj_rank_b[pos_b_at_col])
            transfers.append({"source": na, "target": nb, "source_anchor_col": col_a, "target_pos": pos_b_at_col, "target_proj_rank": rank_at_transfer, "is_gap": False, "in_top1": rank_at_transfer == 0, "in_top3": rank_at_transfer < 3, "in_top5": rank_at_transfer < 5, "in_top10": rank_at_transfer < 10})
    return transfers


# ---------------------------------------------------------------------------
# Phase 3: Top-3 concordance
# ---------------------------------------------------------------------------

def top3_concordance(results: list[dict], pos_to_col: dict, names: list[str], col_tolerance: int = 5):
    """Map top-3 anchors to alignment columns, find consensus columns, compute set overlap."""
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]

    # Collect all top-3 anchor columns per protein
    protein_cols = {}
    for n in anchor_like_names:
        r = result_map[n]
        cols = []
        for pos in r["top3_positions"]:
            if pos < len(pos_to_col[n]):
                cols.append(pos_to_col[n][pos])
        protein_cols[n] = cols

    # Pool all top-3 columns and cluster them
    all_cols = []
    for n, cols in protein_cols.items():
        for c in cols:
            all_cols.append((c, n))
    all_cols.sort(key=lambda x: x[0])

    # Greedy clustering: merge columns within tolerance
    consensus_columns = []
    used = set()
    col_values = sorted(set(c for c, _ in all_cols))
    for cv in col_values:
        if cv in used:
            continue
        cluster_members = []
        for c, n in all_cols:
            if abs(c - cv) <= col_tolerance:
                cluster_members.append((c, n))
                used.add(c)
        if cluster_members:
            mean_col = np.mean([c for c, _ in cluster_members])
            proteins_in_cluster = set(n for _, n in cluster_members)
            consensus_columns.append({
                "center_col": int(round(mean_col)),
                "n_proteins": len(proteins_in_cluster),
                "proteins": proteins_in_cluster,
                "frac_proteins": len(proteins_in_cluster) / len(anchor_like_names),
                "member_cols": [c for c, _ in cluster_members],
            })

    # Sort by number of contributing proteins
    consensus_columns.sort(key=lambda x: -x["n_proteins"])

    # Pairwise minimum set distance
    pair_min_dists = []
    for i in range(len(anchor_like_names)):
        for j in range(i + 1, len(anchor_like_names)):
            na, nb = anchor_like_names[i], anchor_like_names[j]
            cols_a, cols_b = protein_cols[na], protein_cols[nb]
            if not cols_a or not cols_b:
                continue
            min_dist = min(abs(ca - cb) for ca in cols_a for cb in cols_b)
            pair_min_dists.append(min_dist)

    # Random control for top-3
    rng = np.random.RandomState(123)
    random_min_dists_trials = []
    for _ in range(200):
        rand_cols = {}
        for n in anchor_like_names:
            n_res = result_map[n]["n_res"]
            candidates = [p for p in range(n_res) if p < len(pos_to_col[n])]
            if len(candidates) >= 3:
                chosen = rng.choice(candidates, size=3, replace=False)
                rand_cols[n] = [pos_to_col[n][p] for p in chosen]
            else:
                rand_cols[n] = []
        trial_dists = []
        for i in range(len(anchor_like_names)):
            for j in range(i + 1, len(anchor_like_names)):
                na, nb = anchor_like_names[i], anchor_like_names[j]
                cols_a, cols_b = rand_cols[na], rand_cols[nb]
                if not cols_a or not cols_b:
                    continue
                trial_dists.append(min(abs(ca - cb) for ca in cols_a for cb in cols_b))
        if trial_dists:
            random_min_dists_trials.append(np.mean(trial_dists))

    return consensus_columns, pair_min_dists, np.array(random_min_dists_trials), protein_cols


# ---------------------------------------------------------------------------
# Phase 4: Local conservation
# ---------------------------------------------------------------------------

def local_conservation_analysis(aligned_seqs: dict[str, str], consensus_col: int, window: int = 25):
    """Compute per-column conservation (fraction most common AA) across the alignment.
    Compare the anchor window to global average."""
    names = list(aligned_seqs.keys())
    aln_len = len(next(iter(aligned_seqs.values())))

    # Per-column conservation
    col_conservation = []
    for col in range(aln_len):
        residues = [aligned_seqs[n][col] for n in names if aligned_seqs[n][col] != "-"]
        if not residues:
            col_conservation.append(0.0)
            continue
        counts = Counter(residues)
        col_conservation.append(counts.most_common(1)[0][1] / len(residues))
    col_conservation = np.array(col_conservation)

    # Window around anchor
    win_start = max(0, consensus_col - window)
    win_end = min(aln_len, consensus_col + window + 1)
    window_cons = col_conservation[win_start:win_end]
    # Global mean (only columns with at least 2 non-gap residues)
    col_counts = []
    for col in range(aln_len):
        n_nongap = sum(1 for n in names if aligned_seqs[n][col] != "-")
        col_counts.append(n_nongap)
    col_counts = np.array(col_counts)
    mask = col_counts >= 2
    global_mean_cons = col_conservation[mask].mean() if mask.any() else 0.0
    window_mean_cons = window_cons.mean() if len(window_cons) > 0 else 0.0

    # Pairwise local seq identity around anchor
    pair_local_ids = []
    pair_global_ids = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            # Global
            a, b = aligned_seqs[names[i]], aligned_seqs[names[j]]
            g_aligned = g_match = 0
            for ca, cb in zip(a, b):
                if ca != "-" and cb != "-":
                    g_aligned += 1
                    if ca == cb:
                        g_match += 1
            pair_global_ids.append(g_match / max(g_aligned, 1))

            # Local window
            l_aligned = l_match = 0
            for col in range(win_start, win_end):
                ca, cb = a[col], b[col]
                if ca != "-" and cb != "-":
                    l_aligned += 1
                    if ca == cb:
                        l_match += 1
            pair_local_ids.append(l_match / max(l_aligned, 1))

    return {
        "col_conservation": col_conservation,
        "global_mean_cons": global_mean_cons,
        "window_mean_cons": window_mean_cons,
        "window_start": win_start,
        "window_end": win_end,
        "pair_global_ids": np.array(pair_global_ids),
        "pair_local_ids": np.array(pair_local_ids),
    }


# ---------------------------------------------------------------------------
# Phase 5-6: Motif analysis (shared logic for AA and 3Di)
# ---------------------------------------------------------------------------

def build_centered_pwm(sequences: list[str], anchor_offsets: list[int], alphabet: str, window: int = 25):
    """Build position-weight matrix centered on anchor position.
    Returns (count_matrix, n_seqs_per_position) where positions are [-window, +window]."""
    alpha_size = len(alphabet)
    alpha_to_idx = {c: i for i, c in enumerate(alphabet)}
    n_pos = 2 * window + 1
    counts = np.zeros((n_pos, alpha_size), dtype=float)
    n_seqs = np.zeros(n_pos, dtype=int)

    for seq, anchor_offset in zip(sequences, anchor_offsets):
        for offset in range(-window, window + 1):
            seq_pos = anchor_offset + offset
            if 0 <= seq_pos < len(seq):
                aa = seq[seq_pos]
                idx = alpha_to_idx.get(aa, -1)
                if idx >= 0:
                    pos_idx = offset + window
                    counts[pos_idx, idx] += 1
                    n_seqs[pos_idx] += 1

    return counts, n_seqs


def compute_information_content(counts: np.ndarray, n_seqs: np.ndarray, alpha_size: int):
    """Compute per-position information content in bits."""
    n_pos = counts.shape[0]
    ic = np.zeros(n_pos)
    for i in range(n_pos):
        if n_seqs[i] == 0:
            continue
        freq = counts[i] / n_seqs[i]
        freq = freq[freq > 0]
        H = -np.sum(freq * np.log2(freq))
        ic[i] = np.log2(alpha_size) - H
    return ic


def plot_sequence_logo(counts: np.ndarray, n_seqs: np.ndarray, ic: np.ndarray, alphabet: str, colors: dict, window: int, title: str, out_path: Path):
    """Plot a sequence logo with letter heights proportional to IC x frequency."""
    n_pos = 2 * window + 1
    positions = list(range(-window, window + 1))

    fig, ax = plt.subplots(figsize=(max(12, n_pos * 0.3), 3))

    for pos_idx in range(n_pos):
        if n_seqs[pos_idx] == 0:
            continue
        freq = counts[pos_idx] / n_seqs[pos_idx]
        ic_val = ic[pos_idx]
        heights = freq * ic_val
        # Sort by height (smallest first, so tallest on top)
        order = np.argsort(heights)
        y_offset = 0
        for aa_idx in order:
            h = heights[aa_idx]
            if h < 0.001:
                continue
            aa = alphabet[aa_idx]
            color = colors.get(aa, "#888888")
            ax.text(pos_idx, y_offset + h / 2, aa, ha="center", va="center",
                    fontsize=max(4, min(10, h * 15)), fontweight="bold", color=color,
                    fontfamily="monospace")
            y_offset += h

    ax.set_xlim(-0.5, n_pos - 0.5)
    ax.set_ylim(0, max(ic) * 1.1 if max(ic) > 0 else 1)
    tick_step = max(1, window // 10)
    tick_positions = list(range(0, n_pos, tick_step))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([str(positions[i]) for i in tick_positions], fontsize=7)
    ax.set_xlabel("Position relative to anchor")
    ax.set_ylabel("Information content (bits)")
    ax.set_title(title)
    ax.axvline(window, color="red", alpha=0.3, linestyle="--", label="Anchor")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

def plot_concordance_control(anchor_mean_dist, random_dists, title: str, out_path: Path):
    if random_dists is None or len(random_dists) == 0:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(random_dists, bins=30, color="#C4D4E4", edgecolor="#5B7FA3", linewidth=0.5, label="Random positions (200 trials)")
    ax.axvline(anchor_mean_dist, color="#D64550", lw=2, label=f"Anchor (mean dist = {anchor_mean_dist:.1f})")
    percentile = np.mean(random_dists >= anchor_mean_dist) * 100
    ax.text(0.95, 0.95, f"Anchor < {percentile:.0f}% of random", fontsize=8, ha="right", va="top", transform=ax.transAxes)
    ax.set_xlabel("Mean pairwise alignment column distance")
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_conservation_profile(col_conservation: np.ndarray, consensus_col: int, window: int, out_path: Path):
    """Plot per-column conservation around the anchor column."""
    aln_len = len(col_conservation)
    win_start = max(0, consensus_col - window * 2)
    win_end = min(aln_len, consensus_col + window * 2 + 1)
    cols = range(win_start, win_end)
    vals = col_conservation[win_start:win_end]

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.bar(range(len(vals)), vals, width=1.0, color="#5B7FA3", edgecolor="none", alpha=0.7)
    anchor_idx = consensus_col - win_start
    ax.axvline(anchor_idx, color="#D64550", lw=2, alpha=0.7, label=f"Anchor col {consensus_col}")
    # Shade +-25 window
    w_start_idx = max(0, anchor_idx - window)
    w_end_idx = min(len(vals), anchor_idx + window + 1)
    ax.axvspan(w_start_idx, w_end_idx, alpha=0.1, color="#D64550")
    ax.set_xlabel("Alignment column")
    ax.set_ylabel("Conservation (frac most common AA)")
    ax.set_title("Per-column conservation around anchor")
    ax.legend(fontsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    xtick_step = max(1, len(vals) // 20)
    ax.set_xticks(range(0, len(vals), xtick_step))
    ax.set_xticklabels([str(win_start + i) for i in range(0, len(vals), xtick_step)], fontsize=6, rotation=45)

    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def plot_projection_heatmap(results: list[dict], col_to_pos: dict, pos_to_col: dict, names: list[str], out_path: Path):
    result_map = {r["protein"]: r for r in results if r["is_anchor_like"]}
    anchor_like_names = [n for n in names if n in result_map]
    if not anchor_like_names:
        return

    aln_len = len(col_to_pos[names[0]])
    occupied_cols = set()
    for n in anchor_like_names:
        for col, pos in enumerate(col_to_pos[n]):
            if pos != -1:
                occupied_cols.add(col)
    occupied_cols = sorted(occupied_cols)

    matrix = np.full((len(anchor_like_names), len(occupied_cols)), np.nan)
    anchor_markers = []
    for row_idx, n in enumerate(anchor_like_names):
        r = result_map[n]
        proj = r["proj_scores"]
        anchor_pos = r["anchor_pos"]
        for col_idx, aln_col in enumerate(occupied_cols):
            if aln_col < len(col_to_pos[n]):
                seq_pos = col_to_pos[n][aln_col]
                if seq_pos != -1 and seq_pos < len(proj):
                    matrix[row_idx, col_idx] = proj[seq_pos]
                    if seq_pos == anchor_pos:
                        anchor_markers.append((col_idx, row_idx))

    fig, ax = plt.subplots(figsize=(16, max(4, 0.3 * len(anchor_like_names) + 1)))
    im = ax.imshow(matrix, aspect="auto", cmap="YlOrRd", interpolation="none")
    plt.colorbar(im, ax=ax, label="Projection score", shrink=0.8)
    for cx, ry in anchor_markers:
        ax.plot(cx, ry, marker="*", color="blue", markersize=6, markeredgecolor="white", markeredgewidth=0.3)

    short_names = [extract_pdb_id(n) for n in anchor_like_names]
    ax.set_yticks(range(len(anchor_like_names)))
    ax.set_yticklabels(short_names, fontsize=5)

    xtick_step = max(1, len(occupied_cols) // 20)
    xtick_positions = list(range(0, len(occupied_cols), xtick_step))
    ax.set_xticks(xtick_positions)
    ax.set_xticklabels([str(occupied_cols[i]) for i in xtick_positions], fontsize=5, rotation=45)

    ax.set_xlabel("Alignment column")
    ax.set_ylabel("Protein")
    ax.set_title("L10H9 projection score across structural alignment (blue stars = top-1 anchors)")
    plt.tight_layout()
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def write_report(report_lines: list[str], path: Path):
    with open(path, "w") as f:
        f.writelines(report_lines)
    print(f"  Saved report: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Structure anchor transfer v2")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--skip-pdb-download", action="store_true")
    parser.add_argument("--skip-3di", action="store_true", help="Skip 3Di generation")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    PDB_DIR.mkdir(parents=True, exist_ok=True)

    report = []

    # ===================================================================
    # Phase 0: Data preparation
    # ===================================================================
    print("=" * 70)
    print("Phase 0: Data preparation")
    print("=" * 70)

    print("\nParsing foldmason alignment...")
    aligned_seqs_raw = parse_fasta_alignment(FOLDMASON_DIR / "foldmason_aa.fa")
    aln_len = len(next(iter(aligned_seqs_raw.values())))
    print(f"  {len(aligned_seqs_raw)} entries, alignment length = {aln_len}")

    # Step 0.2: Collapse assemblies
    print("\nCollapsing same-PDB assemblies...")
    aligned_seqs_collapsed, collapse_log = collapse_assemblies(aligned_seqs_raw)
    print(f"  {len(aligned_seqs_raw)} entries -> {len(aligned_seqs_collapsed)} unique PDB IDs")
    for pdb_id, kept, dropped in collapse_log:
        print(f"  {pdb_id}: kept {extract_pdb_id(kept)}-{kept.split('-')[1][:8]}, dropped {len(dropped)} assemblies")

    # Step 0.3: Deduplicate at 90% identity
    print(f"\nDeduplicating at {DEDUP_IDENTITY_THRESHOLD:.0%} global identity...")
    aligned_seqs_dedup, dedup_log, all_identities = deduplicate_by_identity(aligned_seqs_collapsed, DEDUP_IDENTITY_THRESHOLD)
    print(f"  {len(aligned_seqs_collapsed)} -> {len(aligned_seqs_dedup)} after deduplication")
    for kept, dropped in dedup_log:
        print(f"  Cluster: kept {extract_pdb_id(kept)}, dropped {[extract_pdb_id(d) for d in dropped]}")

    # Build mappings on deduplicated set
    names = list(aligned_seqs_dedup.keys())
    ungapped_seqs, col_to_pos, pos_to_col = build_alignment_mappings(aligned_seqs_dedup)

    print(f"\nFinal protein set: {len(names)} proteins")
    for n in names:
        print(f"  {extract_pdb_id(n)}: {len(ungapped_seqs[n])} residues")

    # Identify 1pvg
    pvg_names = [n for n in names if n.startswith("1pvg")]
    if not pvg_names:
        print("ERROR: 1pvg not found in deduplicated set!")
        return
    pvg_name = pvg_names[0]

    # Verify anchor position
    if REFERENCE_ANCHOR_POS < len(pos_to_col[pvg_name]):
        pvg_anchor_col = pos_to_col[pvg_name][REFERENCE_ANCHOR_POS]
        pvg_anchor_aa = ungapped_seqs[pvg_name][REFERENCE_ANCHOR_POS]
        print(f"\n1PVGA anchor at seq pos {REFERENCE_ANCHOR_POS} (AA: {pvg_anchor_aa}) -> aln col {pvg_anchor_col}")
    else:
        print(f"WARNING: 1PVGA anchor pos {REFERENCE_ANCHOR_POS} out of range")
        pvg_anchor_col = None

    # Pairwise identities (for the final set)
    print("\nPairwise sequence identity to 1PVG:")
    final_identities = compute_pairwise_identity(aligned_seqs_dedup)
    for n in names:
        if n == pvg_name:
            continue
        ident = final_identities.get((pvg_name, n), 0.0)
        print(f"  {extract_pdb_id(n)}: {ident:.1%}")

    # Check for remaining high-identity pairs
    print("\nRemaining pairs with >50% identity (after dedup):")
    high_pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ident = final_identities.get((names[i], names[j]), 0.0)
            if ident > 0.50:
                print(f"  {extract_pdb_id(names[i])} - {extract_pdb_id(names[j])}: {ident:.1%}")
                high_pairs.append((names[i], names[j], ident))

    # Step 0.4: Download PDBs
    pdb_ids = [extract_pdb_id(n) for n in names]
    if not args.skip_pdb_download:
        print("\nDownloading missing PDB structures...")
        download_pdbs(pdb_ids, PDB_DIR)
    else:
        print("\nSkipping PDB download.")

    # Step 0.5: Generate 3Di
    three_di_seqs = {}
    if not args.skip_3di:
        print("\nGenerating 3Di sequences...")
        three_di_out = DATA_DIR / "foldseek" / "v2"
        three_di_seqs = generate_3di_sequences(pdb_ids, PDB_DIR, three_di_out)
    else:
        print("\nSkipping 3Di generation.")
        # Try loading existing 3Di
        existing_3di = DATA_DIR / "foldseek" / "v2" / "v2_3di.fa"
        if existing_3di.exists():
            print("  Loading existing 3Di sequences...")
            with open(existing_3di) as f:
                name, seq = None, []
                for line in f:
                    line = line.strip()
                    if line.startswith(">"):
                        if name is not None:
                            three_di_seqs[name] = "".join(seq)
                        name = line[1:].split()[0]
                        seq = []
                    else:
                        seq.append(line)
                if name is not None:
                    three_di_seqs[name] = "".join(seq)
            print(f"  Loaded {len(three_di_seqs)} 3Di sequences")

    # Save dedup log
    dedup_csv_path = REPORT_DIR / "structure_anchor_transfer_v2_dedup.csv"
    with open(dedup_csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "kept", "dropped", "detail"])
        for pdb_id, kept, dropped in collapse_log:
            writer.writerow(["assembly_collapse", kept, ";".join(dropped), f"pdb={pdb_id}"])
        for kept, dropped in dedup_log:
            writer.writerow(["identity_dedup", kept, ";".join(dropped), f"threshold={DEDUP_IDENTITY_THRESHOLD}"])
    print(f"  Saved: {dedup_csv_path}")

    # ===================================================================
    # Phase 1: Anchor behavior audit
    # ===================================================================
    print("\n" + "=" * 70)
    print("Phase 1: Anchor behavior audit")
    print("=" * 70)

    print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    # Reference directions
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    print("Computing reference search direction from 1PVGA...")
    d_ref_1pvg = compute_search_dir(model, tokenizer, all_seqs[REFERENCE_PROTEIN_1PVG], weights, args.device)
    d_ref_1pvg_unit = (d_ref_1pvg / d_ref_1pvg.norm().clamp(min=1e-8)).to(args.device)

    print("Computing reference search direction from 2B61A (sanity check)...")
    d_ref_2b61 = compute_search_dir(model, tokenizer, all_seqs[REFERENCE_PROTEIN_2B61], weights, args.device)
    d_ref_2b61_unit = (d_ref_2b61 / d_ref_2b61.norm().clamp(min=1e-8)).to(args.device)

    cos_d_refs = float(torch.dot(d_ref_1pvg_unit.cpu(), d_ref_2b61_unit.cpu()))
    print(f"  cos(d_ref_1pvg, d_ref_2b61) = {cos_d_refs:.4f}")

    # Use 1PVGA as primary reference
    d_ref = d_ref_1pvg_unit

    print(f"\nAnalyzing {len(names)} proteins...")
    results = []
    for name in names:
        seq = ungapped_seqs[name]
        print(f"  {extract_pdb_id(name)} ({len(seq)} res)...", end=" ", flush=True)
        t0 = time.time()
        try:
            r = analyze_protein(model, tokenizer, name, seq, d_ref, weights, args.device)
            if r is not None:
                results.append(r)
                status = "ANCHOR-LIKE" if r["is_anchor_like"] else "not anchor-like"
                print(f"{status} (top1={r['top1_mass']:.3f}, rho={r['rank_corr']:.3f}, cos_d={r['cos_sim_d']:.3f}) [{time.time()-t0:.1f}s]")
            else:
                print("SKIPPED (too short)")
        except Exception as e:
            print(f"ERROR: {e}")

    n_anchor_like = sum(1 for r in results if r["is_anchor_like"])
    print(f"\n  {n_anchor_like}/{len(results)} proteins are anchor-like")

    # Save audit CSV
    audit_path = REPORT_DIR / "structure_anchor_transfer_v2_audit.csv"
    fields = ["protein", "pdb_id", "n_res", "top1_mass", "top3_mass", "eff_keys", "rank_corr", "rank_corr_p", "top3_overlap", "cos_sim_d", "anchor_pos", "anchor_aa", "is_anchor_like", "top3_positions"]
    with open(audit_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for r in results:
            row = dict(r)
            row["pdb_id"] = extract_pdb_id(r["protein"])
            row["top3_positions"] = ";".join(str(p) for p in r["top3_positions"])
            writer.writerow(row)
    print(f"  Saved: {audit_path}")

    if n_anchor_like < 2:
        print("\nSTOP: Fewer than 2 anchor-like proteins.")
        return

    # ===================================================================
    # Phase 2: Top-1 anchor column concordance
    # ===================================================================
    print("\n" + "=" * 70)
    print("Phase 2: Top-1 anchor column concordance")
    print("=" * 70)

    print("\nAnchor positions in alignment coordinates:")
    for r in results:
        if not r["is_anchor_like"]:
            continue
        n = r["protein"]
        pos = r["anchor_pos"]
        if pos < len(pos_to_col[n]):
            col = pos_to_col[n][pos]
            print(f"  {extract_pdb_id(n)}: seq pos {pos} (AA: {r['anchor_aa']}) -> aln col {col}")

    pairs = anchor_column_concordance(results, pos_to_col, names)
    if pairs:
        dists = [p["col_distance"] for p in pairs]
        print(f"\n  Mean pairwise column distance: {np.mean(dists):.1f}")
        print(f"  Median: {np.median(dists):.1f}")
        print(f"  Exact match (dist=0): {sum(1 for d in dists if d == 0)}/{len(dists)}")
        print(f"  Within 5: {sum(1 for d in dists if d <= 5)}/{len(dists)}")
        print(f"  Within 10: {sum(1 for d in dists if d <= 10)}/{len(dists)}")

    # Save concordance CSV
    conc_path = REPORT_DIR / "structure_anchor_transfer_v2_concordance.csv"
    if pairs:
        with open(conc_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(pairs[0].keys()))
            writer.writeheader()
            writer.writerows(pairs)
        print(f"  Saved: {conc_path}")

    # Random control
    print("\nRandom position control (top-1):")
    anchor_mean_dist, random_dists = random_position_control(results, pos_to_col, names)
    if anchor_mean_dist is not None and len(random_dists) > 0:
        percentile = np.mean(random_dists >= anchor_mean_dist) * 100
        print(f"  Anchor mean pairwise column distance: {anchor_mean_dist:.1f}")
        print(f"  Random mean (200 trials): {np.mean(random_dists):.1f} +/- {np.std(random_dists):.1f}")
        print(f"  Anchor tighter than {percentile:.0f}% of random trials")

    # Projection transfer
    print("\nProjection score transfer (top-1):")
    transfers = projection_score_transfer(results, pos_to_col, col_to_pos, names)
    non_gap = [t for t in transfers if not t["is_gap"]]
    gap_count = sum(1 for t in transfers if t["is_gap"])
    if non_gap:
        top1_rate = sum(1 for t in non_gap if t["in_top1"]) / len(non_gap)
        top3_rate = sum(1 for t in non_gap if t["in_top3"]) / len(non_gap)
        top5_rate = sum(1 for t in non_gap if t["in_top5"]) / len(non_gap)
        top10_rate = sum(1 for t in non_gap if t["in_top10"]) / len(non_gap)
        mean_rank = np.mean([t["target_proj_rank"] for t in non_gap])
        print(f"  {len(non_gap)} non-gap transfers, {gap_count} gaps")
        print(f"  Top-1: {top1_rate:.1%}, Top-3: {top3_rate:.1%}, Top-5: {top5_rate:.1%}, Top-10: {top10_rate:.1%}")
        print(f"  Mean projection rank: {mean_rank:.1f}")
    else:
        top1_rate = top3_rate = top5_rate = top10_rate = mean_rank = 0.0

    # ===================================================================
    # Phase 3: Top-3 anchor column concordance
    # ===================================================================
    print("\n" + "=" * 70)
    print("Phase 3: Top-3 anchor column concordance")
    print("=" * 70)

    consensus_cols, pair_min_dists, random_min_dists, protein_cols = top3_concordance(results, pos_to_col, names)

    print(f"\nConsensus anchor columns (tolerance=5):")
    for i, cc in enumerate(consensus_cols[:10]):
        print(f"  Column {cc['center_col']}: {cc['n_proteins']} proteins ({cc['frac_proteins']:.0%})")

    if pair_min_dists:
        print(f"\nPairwise min set distance (top-3):")
        print(f"  Mean: {np.mean(pair_min_dists):.1f}")
        print(f"  Median: {np.median(pair_min_dists):.1f}")
        print(f"  Exact match (dist=0): {sum(1 for d in pair_min_dists if d == 0)}/{len(pair_min_dists)}")
        print(f"  Within 5: {sum(1 for d in pair_min_dists if d <= 5)}/{len(pair_min_dists)}")

    if len(random_min_dists) > 0 and pair_min_dists:
        anchor_min_mean = np.mean(pair_min_dists)
        pct = np.mean(random_min_dists >= anchor_min_mean) * 100
        print(f"  Random control: anchor mean = {anchor_min_mean:.1f}, random = {np.mean(random_min_dists):.1f} +/- {np.std(random_min_dists):.1f}")
        print(f"  Anchor tighter than {pct:.0f}% of random")

    # Print top-3 columns per protein
    print("\nTop-3 anchor columns per protein:")
    for r in results:
        if not r["is_anchor_like"]:
            continue
        n = r["protein"]
        if n in protein_cols:
            cols_str = ", ".join(str(c) for c in protein_cols[n])
            print(f"  {extract_pdb_id(n)}: {cols_str}")

    # ===================================================================
    # Phase 4: Local conservation
    # ===================================================================
    print("\n" + "=" * 70)
    print("Phase 4: Local sequence conservation")
    print("=" * 70)

    # Use the top consensus column as the anchor reference
    if consensus_cols:
        primary_anchor_col = consensus_cols[0]["center_col"]
    elif pvg_anchor_col is not None:
        primary_anchor_col = pvg_anchor_col
    else:
        primary_anchor_col = 98  # fallback

    print(f"\nAnalyzing conservation around anchor column {primary_anchor_col} (+-25 window)...")
    cons_result = local_conservation_analysis(aligned_seqs_dedup, primary_anchor_col, window=25)
    print(f"  Global mean conservation: {cons_result['global_mean_cons']:.3f}")
    print(f"  Anchor window (+-25) mean conservation: {cons_result['window_mean_cons']:.3f}")
    print(f"  Global mean pairwise seq identity: {cons_result['pair_global_ids'].mean():.3f}")
    print(f"  Local (+-25) mean pairwise seq identity: {cons_result['pair_local_ids'].mean():.3f}")

    # Statistical test: is local conservation significantly different from global?
    if len(cons_result['pair_local_ids']) > 1:
        t_stat, p_val = sp_stats.ttest_rel(cons_result['pair_local_ids'], cons_result['pair_global_ids'])
        print(f"  Paired t-test (local vs global pairwise identity): t={t_stat:.2f}, p={p_val:.2e}")
        if p_val < 0.05 and cons_result['pair_local_ids'].mean() > cons_result['pair_global_ids'].mean():
            print(f"  -> Local identity SIGNIFICANTLY HIGHER than global (p={p_val:.2e})")
        else:
            print(f"  -> Local identity NOT significantly higher than global")

    # ===================================================================
    # Phase 5: AA flank motif analysis
    # ===================================================================
    print("\n" + "=" * 70)
    print("Phase 5: Amino acid flank motif analysis")
    print("=" * 70)

    anchor_like_results = [r for r in results if r["is_anchor_like"]]
    aa_sequences = [ungapped_seqs[r["protein"]] for r in anchor_like_results]
    aa_anchor_offsets = [r["anchor_pos"] for r in anchor_like_results]

    aa_counts, aa_nseqs = build_centered_pwm(aa_sequences, aa_anchor_offsets, STANDARD_AA, window=25)
    aa_ic = compute_information_content(aa_counts, aa_nseqs, len(STANDARD_AA))

    print(f"\n  n proteins: {len(anchor_like_results)}")
    print(f"  IC at anchor (pos 0): {aa_ic[25]:.3f} bits (max possible: {np.log2(20):.3f})")
    print(f"  Max IC in window: {aa_ic.max():.3f} bits at offset {np.argmax(aa_ic) - 25}")
    print(f"  Positions with IC > 0.5: {np.sum(aa_ic > 0.5)}")

    # Anchor residue composition
    anchor_aas = [r["anchor_aa"] for r in anchor_like_results]
    aa_counts_anchor = Counter(anchor_aas)
    print(f"  Anchor AA composition: {dict(aa_counts_anchor.most_common(5))}")
    hydro_frac = sum(1 for aa in anchor_aas if aa in HYDROPHOBIC) / len(anchor_aas)
    print(f"  Hydrophobic fraction: {hydro_frac:.1%}")

    # ===================================================================
    # Phase 6: 3Di flank motif analysis
    # ===================================================================
    di_ic = None
    if three_di_seqs:
        print("\n" + "=" * 70)
        print("Phase 6: 3Di flank motif analysis")
        print("=" * 70)

        # Map anchor positions to 3Di coordinates
        # The 3Di sequences from foldseek are keyed by PDB filename (e.g., "1PVG")
        # Need to match them to our protein names
        di_sequences = []
        di_anchor_offsets = []
        di_matched_proteins = []

        for r in anchor_like_results:
            pdb_id = extract_pdb_id(r["protein"]).upper()
            # Try to find matching 3Di sequence
            di_seq = None
            for key in three_di_seqs:
                if pdb_id in key.upper():
                    di_seq = three_di_seqs[key]
                    break

            if di_seq is None:
                continue

            # The 3Di sequence should be the same length as the structural sequence.
            # We need to map the anchor position from the full sequence to the 3Di sequence.
            # Simple approach: if lengths match, positions correspond directly.
            # If not, we try global alignment.
            full_seq = ungapped_seqs[r["protein"]]
            anchor_pos = r["anchor_pos"]

            if len(di_seq) == len(full_seq):
                # Direct correspondence
                di_sequences.append(di_seq)
                di_anchor_offsets.append(anchor_pos)
                di_matched_proteins.append(r["protein"])
            elif len(di_seq) < len(full_seq):
                # PDB structure may be shorter. Use simple sliding window to find best alignment.
                # Find the offset where the structure sequence starts in the full sequence.
                # For now, use the anchor position if it's within range.
                if anchor_pos < len(di_seq):
                    di_sequences.append(di_seq)
                    di_anchor_offsets.append(anchor_pos)
                    di_matched_proteins.append(r["protein"])
                else:
                    # Try to estimate offset: the PDB sequence is typically a substring
                    # We'll try BioPython pairwise alignment if available
                    try:
                        from Bio import pairwise2
                        from Bio.Align import PairwiseAligner
                        aligner = PairwiseAligner()
                        aligner.mode = 'global'
                        aligner.open_gap_score = -10
                        aligner.extend_gap_score = -0.5

                        # Get the structural AA sequence from PDB
                        pdb_path = PDB_DIR / f"{pdb_id}.pdb"
                        cif_path = PDB_DIR / f"{pdb_id}.cif"
                        struct_path = pdb_path if pdb_path.exists() else cif_path if cif_path.exists() else None
                        if struct_path:
                            from Bio.PDB import PDBParser, MMCIFParser
                            from Bio.PDB.Polypeptide import three_to_one
                            if struct_path.suffix == ".pdb":
                                parser_pdb = PDBParser(QUIET=True)
                            else:
                                parser_pdb = MMCIFParser(QUIET=True)
                            structure = parser_pdb.get_structure("s", str(struct_path))
                            struct_seq = ""
                            for residue in structure.get_residues():
                                if residue.id[0] == " ":
                                    try:
                                        struct_seq += three_to_one(residue.get_resname())
                                    except KeyError:
                                        struct_seq += "X"

                            # Align full seq to struct seq
                            alignments = aligner.align(full_seq, struct_seq)
                            if alignments:
                                aln = alignments[0]
                                # Find where anchor_pos in full_seq maps to in struct_seq
                                aligned_full, aligned_struct = str(aln).split("\n")[0], str(aln).split("\n")[2]
                                full_idx = struct_idx = 0
                                mapped_pos = -1
                                for af, as_ in zip(aligned_full, aligned_struct):
                                    if af != "-" and as_ != "-":
                                        if full_idx == anchor_pos:
                                            mapped_pos = struct_idx
                                            break
                                        full_idx += 1
                                        struct_idx += 1
                                    elif af != "-":
                                        if full_idx == anchor_pos:
                                            mapped_pos = -1  # gap
                                            break
                                        full_idx += 1
                                    else:
                                        struct_idx += 1

                                if mapped_pos >= 0 and mapped_pos < len(di_seq):
                                    di_sequences.append(di_seq)
                                    di_anchor_offsets.append(mapped_pos)
                                    di_matched_proteins.append(r["protein"])
                    except Exception:
                        pass  # Skip this protein for 3Di analysis

        print(f"\n  Matched {len(di_sequences)}/{len(anchor_like_results)} proteins with 3Di sequences")

        if len(di_sequences) >= 5:
            di_counts, di_nseqs = build_centered_pwm(di_sequences, di_anchor_offsets, DI_ALPHABET, window=25)
            di_ic = compute_information_content(di_counts, di_nseqs, len(DI_ALPHABET))

            print(f"  IC at anchor (pos 0): {di_ic[25]:.3f} bits (max possible: {np.log2(20):.3f})")
            print(f"  Max IC in window: {di_ic.max():.3f} bits at offset {np.argmax(di_ic) - 25}")
            print(f"  Positions with IC > 0.5: {np.sum(di_ic > 0.5)}")

            # Compare AA vs 3Di IC
            print(f"\n  IC comparison (AA vs 3Di):")
            print(f"    At anchor: AA={aa_ic[25]:.3f}, 3Di={di_ic[25]:.3f}")
            print(f"    Max: AA={aa_ic.max():.3f}, 3Di={di_ic.max():.3f}")
            print(f"    Mean: AA={aa_ic.mean():.3f}, 3Di={di_ic.mean():.3f}")
        else:
            print("  Too few 3Di matches for motif analysis.")

    # ===================================================================
    # Plots
    # ===================================================================
    print("\n" + "=" * 70)
    print("Generating plots...")
    print("=" * 70)

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "figure.dpi": 200})

    # Top-1 null distribution
    plot_concordance_control(anchor_mean_dist, random_dists, "Top-1 anchor column clustering vs random", REPORT_DIR / "structure_anchor_transfer_v2_top1_null.png")

    # Top-3 null distribution
    if pair_min_dists and len(random_min_dists) > 0:
        plot_concordance_control(np.mean(pair_min_dists), random_min_dists, "Top-3 anchor set overlap vs random", REPORT_DIR / "structure_anchor_transfer_v2_top3_null.png")

    # Conservation profile
    if cons_result is not None:
        plot_conservation_profile(cons_result["col_conservation"], primary_anchor_col, 25, REPORT_DIR / "structure_anchor_transfer_v2_conservation.png")

    # Projection heatmap
    plot_projection_heatmap(results, col_to_pos, pos_to_col, names, REPORT_DIR / "structure_anchor_transfer_v2_heatmap.png")

    # AA sequence logo
    plot_sequence_logo(aa_counts, aa_nseqs, aa_ic, STANDARD_AA, AA_COLORS, 25, f"AA motif around anchor (n={len(anchor_like_results)})", REPORT_DIR / "structure_anchor_transfer_v2_aa_logo.png")

    # 3Di sequence logo
    if di_ic is not None:
        plot_sequence_logo(di_counts, di_nseqs, di_ic, DI_ALPHABET, DI_COLORS, 25, f"3Di motif around anchor (n={len(di_sequences)})", REPORT_DIR / "structure_anchor_transfer_v2_3di_logo.png")

    # ===================================================================
    # Write report
    # ===================================================================
    print("\n" + "=" * 70)
    print("Writing report...")
    print("=" * 70)

    report = []
    report.append("# Structure Anchor Transfer v2\n\n")

    report.append("## Data\n\n")
    report.append(f"Foldmason structural alignment of {len(aligned_seqs_raw)} entries ({len(aligned_seqs_collapsed)} unique PDB IDs) from Foldseek top-2 hits for 1PVGA (TM > 0.6, seq id < 0.20).\n")
    report.append(f"After assembly collapse ({len(aligned_seqs_raw)} -> {len(aligned_seqs_collapsed)}) and deduplication at {DEDUP_IDENTITY_THRESHOLD:.0%} identity ({len(aligned_seqs_collapsed)} -> {len(aligned_seqs_dedup)}): {len(names)} proteins.\n")
    report.append(f"Alignment length: {aln_len} columns.\n\n")

    if dedup_log:
        report.append("### Deduplication log\n\n")
        for kept, dropped in dedup_log:
            report.append(f"- Kept {extract_pdb_id(kept)}, dropped {[extract_pdb_id(d) for d in dropped]} (>{DEDUP_IDENTITY_THRESHOLD:.0%} identity)\n")
        report.append("\n")

    report.append("## Phase 1: Anchor behavior audit\n\n")
    report.append(f"Reference search direction: d_ref from 1PVGA.\n")
    report.append(f"Sanity check: cos(d_ref_1pvg, d_ref_2b61) = {cos_d_refs:.4f}.\n")
    report.append(f"Anchor-like thresholds: top1_mass > {ANCHOR_TOP1_THRESH}, rank_corr > {ANCHOR_RANKCORR_THRESH}.\n\n")

    report.append("| PDB | N res | top1_mass | rank_corr | cos(d_self, d_ref) | Anchor pos | Anchor AA | Anchor-like |\n")
    report.append("|-----|-------|-----------|-----------|--------------------|-----------:|-----------|:-----------:|\n")
    for r in results:
        pdb = extract_pdb_id(r["protein"])
        al = "YES" if r["is_anchor_like"] else "no"
        report.append(f"| {pdb} | {r['n_res']} | {r['top1_mass']:.3f} | {r['rank_corr']:.3f} | {r['cos_sim_d']:.3f} | {r['anchor_pos']} | {r['anchor_aa']} | {al} |\n")
    report.append(f"\n{n_anchor_like}/{len(results)} proteins pass the anchor-like gate.\n\n")

    report.append("## Phase 2: Top-1 anchor column concordance\n\n")

    report.append("### Anchor positions in alignment coordinates\n\n")
    report.append("| PDB | Anchor seq pos | Anchor aln col |\n")
    report.append("|-----|---------------:|---------------:|\n")
    for r in results:
        if not r["is_anchor_like"]:
            continue
        n = r["protein"]
        pos = r["anchor_pos"]
        col = pos_to_col[n][pos] if pos < len(pos_to_col[n]) else -1
        report.append(f"| {extract_pdb_id(n)} | {pos} | {col} |\n")
    report.append("\n")

    if pairs:
        dists = [p["col_distance"] for p in pairs]
        report.append(f"Mean pairwise distance: {np.mean(dists):.1f} columns.\n")
        report.append(f"Median: {np.median(dists):.1f}.\n")
        report.append(f"Exact match (dist=0): {sum(1 for d in dists if d == 0)}/{len(dists)}.\n")
        report.append(f"Within 5: {sum(1 for d in dists if d <= 5)}/{len(dists)}.\n")
        report.append(f"Within 10: {sum(1 for d in dists if d <= 10)}/{len(dists)}.\n\n")

    if anchor_mean_dist is not None and len(random_dists) > 0:
        percentile = np.mean(random_dists >= anchor_mean_dist) * 100
        report.append("### Random position control\n\n")
        report.append(f"Anchor mean pairwise distance: {anchor_mean_dist:.1f}.\n")
        report.append(f"Random mean (200 trials): {np.mean(random_dists):.1f} +/- {np.std(random_dists):.1f}.\n")
        report.append(f"Anchor tighter than {percentile:.0f}% of random.\n\n")

    if non_gap:
        report.append("### Projection score transfer\n\n")
        report.append(f"{len(non_gap)} non-gap transfers, {gap_count} gaps.\n")
        report.append(f"Top-1: {top1_rate:.1%}, Top-3: {top3_rate:.1%}, Top-5: {top5_rate:.1%}, Top-10: {top10_rate:.1%}.\n")
        report.append(f"Mean projection rank: {mean_rank:.1f}.\n\n")

    report.append("## Phase 3: Top-3 anchor column concordance\n\n")
    if consensus_cols:
        report.append("### Consensus anchor columns (tolerance=5)\n\n")
        report.append("| Column | N proteins | Fraction |\n")
        report.append("|-------:|-----------:|---------:|\n")
        for cc in consensus_cols[:10]:
            report.append(f"| {cc['center_col']} | {cc['n_proteins']} | {cc['frac_proteins']:.0%} |\n")
        report.append("\n")

    if pair_min_dists:
        report.append(f"Pairwise min set distance: mean={np.mean(pair_min_dists):.1f}, median={np.median(pair_min_dists):.1f}.\n")
        report.append(f"Exact match: {sum(1 for d in pair_min_dists if d == 0)}/{len(pair_min_dists)}.\n")
        report.append(f"Within 5: {sum(1 for d in pair_min_dists if d <= 5)}/{len(pair_min_dists)}.\n\n")

    report.append("## Phase 4: Local sequence conservation\n\n")
    report.append(f"Anchor column: {primary_anchor_col}.\n")
    report.append(f"Global mean conservation: {cons_result['global_mean_cons']:.3f}.\n")
    report.append(f"Anchor window (+-25) mean conservation: {cons_result['window_mean_cons']:.3f}.\n")
    report.append(f"Global mean pairwise seq identity: {cons_result['pair_global_ids'].mean():.3f}.\n")
    report.append(f"Local (+-25) mean pairwise seq identity: {cons_result['pair_local_ids'].mean():.3f}.\n")
    if len(cons_result['pair_local_ids']) > 1:
        t_stat, p_val = sp_stats.ttest_rel(cons_result['pair_local_ids'], cons_result['pair_global_ids'])
        report.append(f"Paired t-test (local vs global identity): t={t_stat:.2f}, p={p_val:.2e}.\n")
        if p_val < 0.05 and cons_result['pair_local_ids'].mean() > cons_result['pair_global_ids'].mean():
            report.append("Local identity is significantly higher than global around the anchor.\n\n")
        else:
            report.append("Local identity is NOT significantly higher than global around the anchor.\n\n")

    report.append("## Phase 5: AA flank motif\n\n")
    report.append(f"n proteins: {len(anchor_like_results)}.\n")
    report.append(f"IC at anchor: {aa_ic[25]:.3f} bits (max possible: {np.log2(20):.3f}).\n")
    report.append(f"Max IC: {aa_ic.max():.3f} bits at offset {np.argmax(aa_ic) - 25}.\n")
    report.append(f"Anchor AA: {dict(aa_counts_anchor.most_common(5))}.\n")
    report.append(f"Hydrophobic fraction: {hydro_frac:.1%}.\n\n")

    if di_ic is not None:
        report.append("## Phase 6: 3Di flank motif\n\n")
        report.append(f"n proteins: {len(di_sequences)}.\n")
        report.append(f"IC at anchor: {di_ic[25]:.3f} bits.\n")
        report.append(f"Max IC: {di_ic.max():.3f} bits at offset {np.argmax(di_ic) - 25}.\n\n")
        report.append("### IC comparison (AA vs 3Di)\n\n")
        report.append(f"At anchor: AA={aa_ic[25]:.3f}, 3Di={di_ic[25]:.3f}.\n")
        report.append(f"Max: AA={aa_ic.max():.3f}, 3Di={di_ic.max():.3f}.\n")
        report.append(f"Mean: AA={aa_ic.mean():.3f}, 3Di={di_ic.mean():.3f}.\n\n")

    # Interpretation
    report.append("## Interpretation\n\n")
    if pairs:
        dists = [p["col_distance"] for p in pairs]
        frac_within_5 = sum(1 for d in dists if d <= 5) / len(dists) if dists else 0
        frac_within_10 = sum(1 for d in dists if d <= 10) / len(dists) if dists else 0

        # Use the t-test result rather than an arbitrary margin
        _, p_cons = sp_stats.ttest_rel(cons_result['pair_local_ids'], cons_result['pair_global_ids'])
        local_higher = p_cons < 0.05 and cons_result['pair_local_ids'].mean() > cons_result['pair_global_ids'].mean()

        if frac_within_10 > 0.5 and non_gap and top5_rate > 0.3:
            report.append("Top-1 concordance: POSITIVE. Anchor positions cluster in structural alignment space.\n")
        elif frac_within_10 > 0.3:
            report.append("Top-1 concordance: MODERATE. Some clustering of anchor positions.\n")
        else:
            report.append("Top-1 concordance: WEAK. Anchor positions show limited clustering.\n")

        if local_higher:
            report.append("Local conservation: local sequence identity around anchor IS higher than global. Cannot fully separate structural signal from local sequence signal.\n")
        else:
            report.append("Local conservation: local sequence identity around anchor is NOT higher than global. Concordance is not driven by local sequence conservation.\n")

        if di_ic is not None:
            if di_ic[25] > aa_ic[25]:
                report.append(f"3Di vs AA: 3Di IC at anchor ({di_ic[25]:.3f}) > AA IC ({aa_ic[25]:.3f}). Structural conservation exceeds sequence conservation at the anchor.\n")
            else:
                report.append(f"3Di vs AA: 3Di IC at anchor ({di_ic[25]:.3f}) <= AA IC ({aa_ic[25]:.3f}). No evidence for stronger structural than sequence conservation.\n")

    report.append("\n## Plots\n\n")
    report.append("![Top-1 null](structure_anchor_transfer_v2_top1_null.png)\n")
    report.append("![Top-3 null](structure_anchor_transfer_v2_top3_null.png)\n")
    report.append("![Conservation](structure_anchor_transfer_v2_conservation.png)\n")
    report.append("![Heatmap](structure_anchor_transfer_v2_heatmap.png)\n")
    report.append("![AA logo](structure_anchor_transfer_v2_aa_logo.png)\n")
    if di_ic is not None:
        report.append("![3Di logo](structure_anchor_transfer_v2_3di_logo.png)\n")

    report_path = REPORT_DIR / "structure_anchor_transfer_v2.md"
    write_report(report, report_path)

    print("\nDone.")


if __name__ == "__main__":
    main()
