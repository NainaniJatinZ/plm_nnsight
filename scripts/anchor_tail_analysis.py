#!/usr/bin/env python3
"""Tail analysis: among buried, well-packed beta-strand residues, what distinguishes the anchor?

Quick analysis 1: Filter to RSA < 0.05, contacts_8A >= 10, SSE = E.
  - How many per protein? How does anchor rank among those?
  - Print the top ~20 positions per protein with all features.

Quick analysis 2: Beta-sheet H-bonding / strand pairing.
  - For each buried beta-strand residue, count backbone H-bonds to other strands.
  - Does the anchor sit in the most "connected" (interior) strand?

Reads all data from disk — no model forward passes needed.

Usage:
    uv run python scripts/anchor_tail_analysis.py --device cuda
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

KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
      "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
      "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
      "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


# ---------------------------------------------------------------------------
# Data loading (same as v2)
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
# PDB loading (from v2)
# ---------------------------------------------------------------------------

def _find_pdb(protein: str) -> Path | None:
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
    candidates = [c for c in candidates if "compare" not in str(c) and "aux" not in str(c)]
    return candidates[0] if candidates else None


def _align_pdb_to_seq(pdb_residues, full_seq):
    resids = [r[0] for r in pdb_residues]
    n_seq = len(full_seq)
    best_offset, best_matches = 0, 0
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
    return mapping, best_offset


def load_pdb_structure(protein, full_seq):
    """Load PDB, compute RSA, contacts, and return per-seq-pos feature dict + structure for H-bond analysis."""
    from Bio.PDB import PDBParser, ShrakeRupley
    from Bio.Data.IUPACData import protein_letters_3to1
    from scipy.spatial.distance import cdist

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return None, None

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(protein, str(pdb_path))
    chain = list(structure[0])[0]

    pdb_residues_raw = []
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
        pdb_residues_raw.append({"resid": resid, "aa": aa, "ca": ca, "cb": cb, "residue_obj": residue})

    if not pdb_residues_raw:
        return None, None

    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues_raw]
    mapping, offset = _align_pdb_to_seq(pdb_tuples, full_seq)
    if len(mapping) < len(pdb_residues_raw) * 0.5:
        return None, None

    # RSA
    sr = ShrakeRupley()
    sr.compute(structure[0], level="R")
    sasa_by_resid = {}
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa

    # Contacts
    cb_coords = np.array([r["cb"] for r in pdb_residues_raw])
    dists = cdist(cb_coords, cb_coords)
    contacts_8A = (dists < 8.0).sum(axis=1) - 1
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
            "long_range_contacts": int(long_range[pdb_idx]),
            "pdb_idx": pdb_idx,
        }

    return features, (pdb_residues_raw, mapping, offset, chain, structure)


# ---------------------------------------------------------------------------
# H-bond analysis for beta-strand residues
# ---------------------------------------------------------------------------

def compute_strand_hbonds(pdb_residues_raw, mapping, sse_str, full_seq):
    """For each beta-strand residue, count backbone H-bonds to residues in OTHER strands.

    Uses N-O distance < 3.5 A as H-bond criterion (standard backbone H-bond cutoff).
    Identifies strand segments and counts inter-strand H-bonds per residue.
    """
    # Build strand segments from SSE string
    n_seq = len(sse_str)
    strand_id = [-1] * n_seq  # which strand segment each position belongs to
    current_strand = 0
    i = 0
    while i < n_seq:
        if sse_str[i] == "E":
            j = i
            while j < n_seq and sse_str[j] == "E":
                strand_id[j] = current_strand
                j += 1
            current_strand += 1
            i = j
        else:
            i += 1

    # Reverse mapping: seq_pos -> pdb_idx
    seq_to_pdb = {seq_pos: pdb_idx for pdb_idx, seq_pos in mapping.items()}

    # For each PDB residue, get N and O coords
    n_coords = {}  # pdb_idx -> N coord
    o_coords = {}  # pdb_idx -> O coord
    for pdb_idx, r in enumerate(pdb_residues_raw):
        res_obj = r["residue_obj"]
        if "N" in res_obj:
            n_coords[pdb_idx] = res_obj["N"].get_vector().get_array()
        if "O" in res_obj:
            o_coords[pdb_idx] = res_obj["O"].get_vector().get_array()

    # For each beta-strand residue, count H-bonds to OTHER strands
    hbond_counts = {}  # seq_pos -> n_inter_strand_hbonds
    strand_connectivity = {}  # seq_pos -> set of strand_ids this residue H-bonds to

    for seq_pos in range(n_seq):
        if sse_str[seq_pos] != "E":
            continue
        if seq_pos not in seq_to_pdb:
            continue

        pdb_i = seq_to_pdb[seq_pos]
        my_strand = strand_id[seq_pos]
        n_hbonds = 0
        connected_strands = set()

        # Check all other beta-strand residues for backbone H-bonds
        for other_seq_pos in range(n_seq):
            if sse_str[other_seq_pos] != "E":
                continue
            if strand_id[other_seq_pos] == my_strand:
                continue
            if other_seq_pos not in seq_to_pdb:
                continue
            pdb_j = seq_to_pdb[other_seq_pos]

            # Check N_i -- O_j (i donates to j)
            if pdb_i in n_coords and pdb_j in o_coords:
                dist = np.linalg.norm(n_coords[pdb_i] - o_coords[pdb_j])
                if dist < 3.5:
                    n_hbonds += 1
                    connected_strands.add(strand_id[other_seq_pos])

            # Check O_i -- N_j (j donates to i)
            if pdb_i in o_coords and pdb_j in n_coords:
                dist = np.linalg.norm(o_coords[pdb_i] - n_coords[pdb_j])
                if dist < 3.5:
                    n_hbonds += 1
                    connected_strands.add(strand_id[other_seq_pos])

        hbond_counts[seq_pos] = n_hbonds
        strand_connectivity[seq_pos] = connected_strands

    # Compute strand-level statistics
    strand_partner_count = {}  # strand_id -> number of distinct partner strands
    for sid in range(current_strand):
        positions = [p for p in range(n_seq) if strand_id[p] == sid]
        all_partners = set()
        for p in positions:
            if p in strand_connectivity:
                all_partners |= strand_connectivity[p]
        strand_partner_count[sid] = len(all_partners)

    # Map to seq_pos features
    result = {}
    for seq_pos in range(n_seq):
        if sse_str[seq_pos] != "E":
            continue
        sid = strand_id[seq_pos]
        result[seq_pos] = {
            "inter_strand_hbonds": hbond_counts.get(seq_pos, 0),
            "n_partner_strands": len(strand_connectivity.get(seq_pos, set())),
            "strand_id": sid,
            "strand_total_partners": strand_partner_count.get(sid, 0),
            "is_interior_strand": 1 if strand_partner_count.get(sid, 0) >= 2 else 0,
        }

    return result


# ---------------------------------------------------------------------------
# SSE features
# ---------------------------------------------------------------------------

def compute_sse_features(sse_str):
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
            }
        i = j
    return features


# ---------------------------------------------------------------------------
# Hydrophobic features
# ---------------------------------------------------------------------------

def compute_hydrophobic_features(sequence):
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


# ---------------------------------------------------------------------------
# Model loading and projection scores
# ---------------------------------------------------------------------------

def load_model(device):
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


def extract_head_weights(model, layer, head):
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


def compute_search_dir(model, tokenizer, sequence, weights, device):
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


def build_clean_sequence(sequence, config):
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


def capture_projection_scores(model, tokenizer, sequence, search_dir_unit, device):
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

    print("Computing search direction...")
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir = compute_search_dir(model, tokenizer, ref_clean, weights, args.device)
    search_dir_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    report = []
    report.append("# Anchor Tail Analysis\n\n")
    report.append("Question: among buried, well-packed beta-strand residues, what distinguishes the anchor from the runner-up?\n\n")

    # =========================================================================
    # ANALYSIS 1: Filter to buried+packed+strand, examine anchor rank
    # =========================================================================
    report.append("## Analysis 1: Filtered tail examination\n\n")
    report.append("Filter: RSA < 0.05, contacts_8A >= 10, SSE = E\n\n")

    all_tail_stats = []

    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        sequence = seqs[protein]
        config = protein_configs[protein]
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")

        pdb_features, pdb_data = load_pdb_structure(protein, sequence)
        if pdb_features is None:
            report.append(f"### {protein}: skipped (no PDB)\n\n")
            continue

        conservation = load_conservation(protein)
        hydro_features = compute_hydrophobic_features(sequence)
        sse_features = compute_sse_features(sse_str)

        print(f"  {protein}: computing projection scores...")
        proj_scores = capture_projection_scores(model, tokenizer, sequence, search_dir_unit, args.device)

        # H-bond analysis
        pdb_residues_raw, mapping, offset, chain, structure = pdb_data
        hbond_data = compute_strand_hbonds(pdb_residues_raw, mapping, sse_str, sequence)

        # Build per-position records for this protein
        records = []
        for j in range(len(sequence)):
            if j >= len(proj_scores):
                break
            pf = pdb_features.get(j, {})
            rsa = pf.get("rsa", np.nan)
            c8 = pf.get("contacts_8A", np.nan)
            lr = pf.get("long_range_contacts", np.nan)
            sse = sse_str[j] if j < len(sse_str) else "C"
            hf = hydro_features[j]
            sf = sse_features[j]
            cons = conservation.get(j, np.nan) if conservation else np.nan
            hb = hbond_data.get(j, {})

            records.append({
                "pos": j,
                "aa": sequence[j],
                "sse": sse,
                "proj": float(proj_scores[j]),
                "rsa": rsa,
                "contacts_8A": c8,
                "long_range_contacts": lr,
                "self_hydro": hf["self_hydro"],
                "local_hydro_w5": hf["local_hydro_w5"],
                "same_face_hydro": hf["same_face_hydro"],
                "conservation": cons,
                "seg_len": sf["seg_len"],
                "dist_to_boundary": sf["dist_to_boundary"],
                "is_anchor": 1 if j == anchor_pos else 0,
                "inter_strand_hbonds": hb.get("inter_strand_hbonds", np.nan),
                "n_partner_strands": hb.get("n_partner_strands", np.nan),
                "strand_total_partners": hb.get("strand_total_partners", np.nan),
                "is_interior_strand": hb.get("is_interior_strand", np.nan),
                "strand_id": hb.get("strand_id", np.nan),
            })

        # Apply tail filter
        tail = [r for r in records if r["sse"] == "E"
                and not np.isnan(r["rsa"]) and r["rsa"] < 0.05
                and not np.isnan(r["contacts_8A"]) and r["contacts_8A"] >= 10]

        # Sort by projection score descending
        tail.sort(key=lambda r: r["proj"], reverse=True)
        n_tail = len(tail)
        anchor_in_tail = [r for r in tail if r["is_anchor"]]
        anchor_rank_in_tail = next((i + 1 for i, r in enumerate(tail) if r["is_anchor"]), None)

        all_tail_stats.append({
            "protein": protein,
            "n_total": len(records),
            "n_tail": n_tail,
            "anchor_rank_tail": anchor_rank_in_tail,
            "anchor_in_tail": len(anchor_in_tail) > 0,
        })

        report.append(f"### {protein}\n\n")
        report.append(f"Total residues: {len(records)}, tail (buried+packed+strand): {n_tail}\n")
        if anchor_rank_in_tail is not None:
            report.append(f"Anchor rank in tail: {anchor_rank_in_tail}/{n_tail}\n\n")
        else:
            report.append(f"Anchor NOT in tail filter (anchor SSE={sse_str[anchor_pos]}, RSA={pdb_features.get(anchor_pos, {}).get('rsa', 'N/A')}, contacts={pdb_features.get(anchor_pos, {}).get('contacts_8A', 'N/A')})\n\n")

        # Print top positions and anchor
        show_n = min(20, n_tail)
        report.append(f"Top {show_n} positions in tail (+ anchor if not in top {show_n}):\n\n")
        report.append("| Rank | Pos | AA | Proj | RSA | C8A | LR | self_h | w5_h | face_h | cons | seg_len | d_bnd | hb_inter | n_part | str_part | int_str | ANCHOR |\n")
        report.append("|------|-----|-----|------|-----|-----|-----|--------|------|--------|------|---------|-------|----------|--------|----------|---------|--------|\n")

        shown_anchor = False
        for i, r in enumerate(tail[:show_n]):
            is_anch = "*" if r["is_anchor"] else ""
            if r["is_anchor"]:
                shown_anchor = True
            cons_str = f"{r['conservation']:.2f}" if not np.isnan(r["conservation"]) else "-"
            hb_str = f"{r['inter_strand_hbonds']}" if not np.isnan(r["inter_strand_hbonds"]) else "-"
            np_str = f"{r['n_partner_strands']}" if not np.isnan(r["n_partner_strands"]) else "-"
            sp_str = f"{r['strand_total_partners']}" if not np.isnan(r["strand_total_partners"]) else "-"
            is_str = f"{r['is_interior_strand']:.0f}" if not np.isnan(r["is_interior_strand"]) else "-"
            report.append(f"| {i+1} | {r['pos']} | {r['aa']} | {r['proj']:.3f} | {r['rsa']:.3f} | {r['contacts_8A']:.0f} | {r['long_range_contacts']:.0f} | {r['self_hydro']:.1f} | {r['local_hydro_w5']:.1f} | {r['same_face_hydro']:.1f} | {cons_str} | {r['seg_len']} | {r['dist_to_boundary']} | {hb_str} | {np_str} | {sp_str} | {is_str} | {is_anch} |\n")

        # If anchor wasn't in top N, show it separately
        if not shown_anchor and anchor_rank_in_tail is not None:
            r = anchor_in_tail[0]
            cons_str = f"{r['conservation']:.2f}" if not np.isnan(r["conservation"]) else "-"
            hb_str = f"{r['inter_strand_hbonds']}" if not np.isnan(r["inter_strand_hbonds"]) else "-"
            np_str = f"{r['n_partner_strands']}" if not np.isnan(r["n_partner_strands"]) else "-"
            sp_str = f"{r['strand_total_partners']}" if not np.isnan(r["strand_total_partners"]) else "-"
            is_str = f"{r['is_interior_strand']:.0f}" if not np.isnan(r["is_interior_strand"]) else "-"
            report.append(f"| {anchor_rank_in_tail} | {r['pos']} | {r['aa']} | {r['proj']:.3f} | {r['rsa']:.3f} | {r['contacts_8A']:.0f} | {r['long_range_contacts']:.0f} | {r['self_hydro']:.1f} | {r['local_hydro_w5']:.1f} | {r['same_face_hydro']:.1f} | {cons_str} | {r['seg_len']} | {r['dist_to_boundary']} | {hb_str} | {np_str} | {sp_str} | {is_str} | * |\n")

        report.append("\n")

    # Summary table
    report.append("## Analysis 1 summary\n\n")
    report.append("| Protein | Total | Tail | Anchor rank in tail |\n")
    report.append("|---------|-------|------|--------------------|\n")
    for s in all_tail_stats:
        rank_str = f"{s['anchor_rank_tail']}/{s['n_tail']}" if s["anchor_rank_tail"] is not None else "not in tail"
        report.append(f"| {s['protein']} | {s['n_total']} | {s['n_tail']} | {rank_str} |\n")
    report.append("\n")

    # Aggregate: how often is anchor #1 in tail?
    in_tail = [s for s in all_tail_stats if s["anchor_rank_tail"] is not None]
    rank_1 = sum(1 for s in in_tail if s["anchor_rank_tail"] == 1)
    top_3 = sum(1 for s in in_tail if s["anchor_rank_tail"] <= 3)
    report.append(f"Anchors in tail: {len(in_tail)}/{len(all_tail_stats)}\n")
    report.append(f"Anchor is #1 in tail: {rank_1}/{len(in_tail)}\n")
    report.append(f"Anchor in top 3 of tail: {top_3}/{len(in_tail)}\n\n")

    # =========================================================================
    # ANALYSIS 2: H-bond / strand connectivity summary across anchors
    # =========================================================================
    report.append("## Analysis 2: Beta-sheet H-bonding and strand connectivity\n\n")
    report.append("For each anchor, compare its inter-strand H-bond count and strand partner count to other buried beta-strand residues in the same protein.\n\n")
    report.append("| Protein | Anchor hb | Anchor n_part | Anchor str_part | interior? | Tail median hb | Tail median n_part | Tail median str_part | Anchor hb percentile |\n")
    report.append("|---------|-----------|---------------|-----------------|-----------|----------------|--------------------|-----------------------|---------------------|\n")

    # We need to re-examine the tail data per protein — let's recompute from the stored data
    # Re-run with stored data
    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        sequence = seqs[protein]
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")

        pdb_features, pdb_data = load_pdb_structure(protein, sequence)
        if pdb_features is None:
            continue

        pdb_residues_raw, mapping, offset, chain, structure = pdb_data
        hbond_data = compute_strand_hbonds(pdb_residues_raw, mapping, sse_str, sequence)

        # Tail filter
        tail_positions = []
        for j in range(len(sequence)):
            pf = pdb_features.get(j, {})
            rsa = pf.get("rsa", np.nan)
            c8 = pf.get("contacts_8A", np.nan)
            if sse_str[j] == "E" and not np.isnan(rsa) and rsa < 0.05 and not np.isnan(c8) and c8 >= 10:
                hb = hbond_data.get(j, {})
                tail_positions.append({
                    "pos": j,
                    "inter_strand_hbonds": hb.get("inter_strand_hbonds", 0),
                    "n_partner_strands": hb.get("n_partner_strands", 0),
                    "strand_total_partners": hb.get("strand_total_partners", 0),
                    "is_interior_strand": hb.get("is_interior_strand", 0),
                })

        if not tail_positions:
            continue

        anchor_rec = next((t for t in tail_positions if t["pos"] == anchor_pos), None)
        if anchor_rec is None:
            continue

        hb_vals = [t["inter_strand_hbonds"] for t in tail_positions]
        np_vals = [t["n_partner_strands"] for t in tail_positions]
        sp_vals = [t["strand_total_partners"] for t in tail_positions]

        # Percentile of anchor hb among tail
        hb_pctile = sum(1 for v in hb_vals if v <= anchor_rec["inter_strand_hbonds"]) / len(hb_vals) * 100

        report.append(f"| {protein} | {anchor_rec['inter_strand_hbonds']} | {anchor_rec['n_partner_strands']} | {anchor_rec['strand_total_partners']} | {anchor_rec['is_interior_strand']} | {np.median(hb_vals):.0f} | {np.median(np_vals):.0f} | {np.median(sp_vals):.0f} | {hb_pctile:.0f}% |\n")

    report.append("\n")

    out_path = REPORT_DIR / "anchor_tail_analysis.md"
    with open(out_path, "w") as f:
        f.writelines(report)
    print(f"\nSaved: {out_path}")
    print("Done.")


if __name__ == "__main__":
    main()
