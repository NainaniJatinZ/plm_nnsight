#!/usr/bin/env python3
"""Interactive 3D scatter: Projection score vs RSA vs Contact number.

Generates an HTML file with a plotly 3D scatter plot.
Points colored by SSE type, anchors marked distinctly.

Usage:
    uv run python scripts/anchor_3d_plot.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

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
    "1BRTA": 220, "1PVGA": 101, "2B61A": 315, "2DPMA": 39, "2PKEA": 131,
    "2QY6A": 64, "2YHWA": 287, "3CSSA": 40, "3HO7A": 63, "3OKPA": 200,
    "3QDLA": 114, "3WJPA": 94, "4EHUA": 100, "4EX6A": 124, "4EZIA": 310,
    "4ME3A": 75, "4N9WA": 194, "4OY3A": 193,
}

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        ss_dict[k.replace(".pdb", "")] = v.replace("-", "C")
    return protein_configs, seqs, ss_dict


def _find_pdb(protein):
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
    for offset in range(-max(resids), n_seq - min(resids) + 1):
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


def load_pdb_features(protein, full_seq):
    from Bio.PDB import PDBParser, ShrakeRupley
    from Bio.Data.IUPACData import protein_letters_3to1
    from scipy.spatial.distance import cdist

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return None
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(protein, str(pdb_path))
    chain = list(structure[0])[0]
    pdb_res = []
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
        pdb_res.append({"resid": resid, "aa": aa, "cb": cb})
    if not pdb_res:
        return None
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_res]
    mapping = _align_pdb_to_seq(pdb_tuples, full_seq)
    if len(mapping) < len(pdb_res) * 0.5:
        return None
    sr = ShrakeRupley()
    sr.compute(structure[0], level="R")
    sasa_by_resid = {}
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        sasa_by_resid[residue.get_id()[1]] = residue.sasa
    cb_coords = np.array([r["cb"] for r in pdb_res])
    dists = cdist(cb_coords, cb_coords)
    contacts_8A = (dists < 8.0).sum(axis=1) - 1
    features = {}
    for pdb_idx, seq_pos in mapping.items():
        r = pdb_res[pdb_idx]
        max_asa = MAX_ASA.get(r["aa"], 200)
        raw_sasa = sasa_by_resid.get(r["resid"], 0.0)
        rsa = min(raw_sasa / max_asa, 1.0) if max_asa > 0 else 0.0
        features[seq_pos] = {"rsa": rsa, "contacts_8A": int(contacts_8A[pdb_idx])}
    return features


def load_model(device):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(
        model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager"
    ).to(device).eval()
    return NNsight(esm_model), tokenizer


def extract_head_weights(model, layer, head):
    attn = model._model.esm.encoder.layer[layer].attention
    W_Q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_Q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    W_K = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_K = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    return {"W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(),
            "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone()}


def compute_search_dir(model, tokenizer, ref_clean, weights, device):
    inputs = tokenizer(ref_clean, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    W_Q, b_Q, W_K = weights["W_Q_hd"], weights["b_Q_d"], weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    search_dir = W_K.T @ q_mean_norm
    return (search_dir / search_dir.norm().clamp(min=1e-8)).to(device)


def capture_projection_scores(model, tokenizer, sequence, search_dir_unit, device):
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    return (x_ln[1:-1] @ search_dir_unit.cpu()).numpy()


def build_clean_sequence(sequence, config):
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_s, ss1_e = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_s, ss2_e = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
    masked = ["<mask>"] * n
    for i in range(ss1_s, ss1_e):
        masked[i] = sequence[i]
    for i in range(ss2_s, ss2_e):
        masked[i] = sequence[i]
    for i in range(max(0, ss1_s - flank), ss1_s):
        masked[i] = sequence[i]
    for i in range(ss2_e, min(n, ss2_e + flank)):
        masked[i] = sequence[i]
    return "".join(masked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading...")
    protein_configs, seqs, ss_dict = load_configs()
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir_unit = compute_search_dir(model, tokenizer, ref_clean, weights, args.device)

    print("Processing proteins...")
    records = []
    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        sequence = seqs[protein]
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")
        pdb_features = load_pdb_features(protein, sequence)
        if pdb_features is None:
            continue
        proj_scores = capture_projection_scores(model, tokenizer, sequence, search_dir_unit, args.device)
        print(f"  {protein}")
        for j in range(min(len(sequence), len(proj_scores))):
            pf = pdb_features.get(j, {})
            rsa = pf.get("rsa", np.nan)
            c8 = pf.get("contacts_8A", np.nan)
            if np.isnan(rsa) or np.isnan(c8):
                continue
            records.append({
                "protein": protein,
                "pos": j,
                "aa": sequence[j],
                "sse": sse_str[j],
                "proj": float(proj_scores[j]),
                "rsa": rsa,
                "contacts_8A": int(c8),
                "is_anchor": j == anchor_pos,
            })

    print(f"Total points: {len(records)}")

    # Build plotly figure
    import plotly.graph_objects as go

    sse_colors = {"H": "#e06c75", "E": "#61afef", "C": "#98c379"}
    sse_names = {"H": "Helix", "E": "Strand", "C": "Coil"}

    fig = go.Figure()

    # Add traces per SSE type (non-anchor)
    for sse_type in ["C", "H", "E"]:
        pts = [r for r in records if r["sse"] == sse_type and not r["is_anchor"]]
        if not pts:
            continue
        fig.add_trace(go.Scatter3d(
            x=[r["rsa"] for r in pts],
            y=[r["contacts_8A"] for r in pts],
            z=[r["proj"] for r in pts],
            mode="markers",
            marker=dict(size=2, color=sse_colors[sse_type], opacity=0.3),
            name=sse_names[sse_type],
            text=[f"{r['protein']} {r['aa']}{r['pos']}" for r in pts],
            hovertemplate="<b>%{text}</b><br>RSA: %{x:.3f}<br>Contacts: %{y}<br>Proj: %{z:.3f}<extra></extra>",
        ))

    # Add anchors as large distinct markers
    anchors = [r for r in records if r["is_anchor"]]
    fig.add_trace(go.Scatter3d(
        x=[r["rsa"] for r in anchors],
        y=[r["contacts_8A"] for r in anchors],
        z=[r["proj"] for r in anchors],
        mode="markers",
        marker=dict(size=8, color="red", symbol="diamond", line=dict(width=1, color="black")),
        name="Anchor",
        text=[f"ANCHOR {r['protein']} {r['aa']}{r['pos']}" for r in anchors],
        hovertemplate="<b>%{text}</b><br>RSA: %{x:.3f}<br>Contacts: %{y}<br>Proj: %{z:.3f}<extra></extra>",
    ))

    fig.update_layout(
        title="L10H9 Projection Score vs RSA vs 3D Contact Number",
        scene=dict(
            xaxis_title="RSA (0=buried, 1=exposed)",
            yaxis_title="Contacts (8 A)",
            zaxis_title="Projection score",
            xaxis=dict(range=[0, 1]),
        ),
        width=1000,
        height=800,
        legend=dict(itemsizing="constant"),
    )

    out_path = REPORT_DIR / "anchor_3d_proj_rsa_contacts.html"
    fig.write_html(str(out_path), include_plotlyjs=True)
    print(f"Saved: {out_path}")
    print("Done.")


if __name__ == "__main__":
    main()
