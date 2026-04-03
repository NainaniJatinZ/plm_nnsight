#!/usr/bin/env python3
"""Classification framing of the anchor search direction.

The R2=0.24 from regression is misleading because the structural features
gate (threshold) rather than scale linearly with projection score. The right
question is: how well do these features *classify* high-scoring residues?

Analyses:
1. Enrichment: what fraction of top-k scorers pass the tail filter?
2. ROC/PR for "top 10% scorer" classification using structural features
3. Within-tail vs between-tail variance decomposition
4. Conditional distributions: projection score | in-tail vs out-of-tail

Usage:
    uv run python scripts/anchor_classification_analysis.py --device cuda
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

KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
      "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
      "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
      "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}

MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167,
           "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197,
           "L": 201, "K": 236, "M": 224, "F": 240, "P": 159,
           "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


# ---------------------------------------------------------------------------
# Data / PDB loading (same as tail_analysis)
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
    for offset in range(- max(resids), n_seq - min(resids) + 1):
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
        features[seq_pos] = {
            "rsa": rsa,
            "contacts_8A": int(contacts_8A[pdb_idx]),
        }
    return features


def compute_search_dir_and_scores(model, tokenizer, sequence, ref_clean, weights, device):
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    # Search direction from reference
    inputs_ref = tokenizer(ref_clean, return_tensors="pt").to(device)
    with model.trace() as tracer:
        with tracer.invoke(**inputs_ref):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln_ref = cache[key].output.detach().cpu()[0]
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    q_all = x_ln_ref @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    search_dir = W_K.T @ q_mean_norm
    search_dir_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(device)
    return search_dir_unit


def capture_projection_scores(model, tokenizer, sequence, search_dir_unit, device):
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    x_residues = x_ln[1:-1]
    return (x_residues @ search_dir_unit.cpu()).numpy()


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


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading configs and model...")
    protein_configs, seqs, ss_dict = load_configs()
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir_unit = compute_search_dir_and_scores(model, tokenizer, ref_seq, ref_clean, weights, args.device)

    # Collect all residue data across proteins
    print("Processing proteins...")
    all_records = []  # list of dicts per residue
    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        sequence = seqs[protein]
        config = protein_configs[protein]
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")

        pdb_features = load_pdb_features(protein, sequence)
        proj_scores = capture_projection_scores(model, tokenizer, sequence, search_dir_unit, args.device)
        print(f"  {protein}: {len(sequence)} residues, PDB={'yes' if pdb_features else 'no'}")

        for j in range(min(len(sequence), len(proj_scores))):
            pf = pdb_features.get(j, {}) if pdb_features else {}
            rsa = pf.get("rsa", np.nan)
            c8 = pf.get("contacts_8A", np.nan)
            all_records.append({
                "protein": protein,
                "pos": j,
                "aa": sequence[j],
                "sse": sse_str[j],
                "proj": float(proj_scores[j]),
                "rsa": rsa,
                "contacts_8A": c8,
                "self_hydro": KD.get(sequence[j], 0.0),
                "is_anchor": 1 if j == anchor_pos else 0,
            })

    # Only work with residues that have PDB features
    records = [r for r in all_records if not np.isnan(r["rsa"]) and not np.isnan(r["contacts_8A"])]
    N = len(records)
    print(f"\nTotal residues with PDB features: {N}")

    # Define tail membership
    for r in records:
        r["in_tail"] = 1 if (r["sse"] == "E" and r["rsa"] < 0.05 and r["contacts_8A"] >= 10) else 0

    n_tail = sum(r["in_tail"] for r in records)
    print(f"Tail size: {n_tail} ({100*n_tail/N:.1f}%)")

    projs = np.array([r["proj"] for r in records])
    in_tail = np.array([r["in_tail"] for r in records])

    report = []
    report.append("# Classification Framing of the Anchor Search Direction\n\n")
    report.append("The regression R2=0.24 understates the explanatory power of structural features because the relationship is a threshold/gate, not a linear slope.\n")
    report.append("These features define an eligibility set; within that set the contextual computation in layers 7-9 determines the final ranking.\n\n")

    # =========================================================================
    # 1. Enrichment: fraction of top-k in tail
    # =========================================================================
    report.append("## 1. Enrichment analysis\n\n")
    report.append("What fraction of the top-k scoring residues (by projection score) pass the tail filter (RSA < 0.05, contacts >= 10, SSE = E)?\n\n")

    sorted_idx = np.argsort(projs)[::-1]  # descending
    ks = [5, 10, 20, 30, 50, 100, 200, 500]
    report.append("| Top-k | k/N | Tail in top-k | Fraction in tail | Enrichment vs baseline |\n")
    report.append("|-------|-----|---------------|-----------------|------------------------|\n")
    baseline_rate = n_tail / N
    enrichment_data = []
    for k in ks:
        if k > N:
            continue
        top_k_idx = sorted_idx[:k]
        n_tail_in_top_k = sum(in_tail[i] for i in top_k_idx)
        frac = n_tail_in_top_k / k
        enrichment = frac / baseline_rate if baseline_rate > 0 else 0
        enrichment_data.append((k, n_tail_in_top_k, frac, enrichment))
        report.append(f"| {k} | {k/N:.3f} | {n_tail_in_top_k}/{k} | {frac:.3f} | {enrichment:.1f}x |\n")
    report.append(f"\nBaseline tail rate: {n_tail}/{N} = {baseline_rate:.3f}\n\n")

    # Per-protein enrichment at top-10
    report.append("Per-protein: fraction of top-10 scorers that are in tail:\n\n")
    report.append("| Protein | Top-10 in tail | Top-10 fraction |\n")
    report.append("|---------|---------------|------------------|\n")
    proteins = sorted(set(r["protein"] for r in records))
    per_protein_fracs = []
    for p in proteins:
        p_records = [r for r in records if r["protein"] == p]
        p_sorted = sorted(p_records, key=lambda r: r["proj"], reverse=True)
        top10 = p_sorted[:10]
        n_in_tail = sum(r["in_tail"] for r in top10)
        frac = n_in_tail / len(top10)
        per_protein_fracs.append(frac)
        report.append(f"| {p} | {n_in_tail}/10 | {frac:.2f} |\n")
    report.append(f"\nMean per-protein top-10 tail fraction: {np.mean(per_protein_fracs):.3f}\n\n")

    # =========================================================================
    # 2. Variance decomposition: between-group vs within-group
    # =========================================================================
    report.append("## 2. Variance decomposition\n\n")
    report.append("How much of the total variance in projection scores is explained by the binary tail membership alone?\n\n")

    proj_tail = projs[in_tail == 1]
    proj_nontail = projs[in_tail == 0]
    grand_mean = projs.mean()
    ss_total = np.sum((projs - grand_mean) ** 2)
    ss_between = len(proj_tail) * (proj_tail.mean() - grand_mean) ** 2 + len(proj_nontail) * (proj_nontail.mean() - grand_mean) ** 2
    eta_squared = ss_between / ss_total

    report.append(f"Grand mean projection: {grand_mean:.4f}\n")
    report.append(f"Tail mean: {proj_tail.mean():.4f} (N={len(proj_tail)})\n")
    report.append(f"Non-tail mean: {proj_nontail.mean():.4f} (N={len(proj_nontail)})\n")
    report.append(f"Tail std: {proj_tail.std():.4f}\n")
    report.append(f"Non-tail std: {proj_nontail.std():.4f}\n\n")
    report.append(f"SS_between / SS_total (eta-squared): {eta_squared:.4f}\n")
    report.append(f"This single binary feature explains {100*eta_squared:.1f}% of variance.\n\n")

    # Compare: how much does each component contribute?
    report.append("Stepwise eta-squared for individual filter components:\n\n")
    for label, cond_fn in [
        ("SSE = E", lambda r: r["sse"] == "E"),
        ("RSA < 0.05", lambda r: r["rsa"] < 0.05),
        ("contacts_8A >= 10", lambda r: r["contacts_8A"] >= 10),
        ("SSE=E AND RSA<0.05", lambda r: r["sse"] == "E" and r["rsa"] < 0.05),
        ("SSE=E AND contacts>=10", lambda r: r["sse"] == "E" and r["contacts_8A"] >= 10),
        ("Full tail filter", lambda r: r["sse"] == "E" and r["rsa"] < 0.05 and r["contacts_8A"] >= 10),
    ]:
        membership = np.array([1 if cond_fn(r) else 0 for r in records])
        group1 = projs[membership == 1]
        group0 = projs[membership == 0]
        if len(group1) == 0 or len(group0) == 0:
            continue
        ss_b = len(group1) * (group1.mean() - grand_mean) ** 2 + len(group0) * (group0.mean() - grand_mean) ** 2
        eta2 = ss_b / ss_total
        t_stat, p_val = stats.ttest_ind(group1, group0)
        report.append(f"- {label}: eta2={eta2:.4f} ({100*eta2:.1f}%), in-group N={len(group1)}, mean={group1.mean():.4f}, t={t_stat:.1f}, p={p_val:.2e}\n")
    report.append("\n")

    # =========================================================================
    # 3. Rank-based metrics per protein
    # =========================================================================
    report.append("## 3. Rank concentration\n\n")
    report.append("For each protein: what fraction of the top-scoring decile (top 10%) falls in the tail?\n")
    report.append("And conversely: what fraction of the tail falls in the top decile?\n\n")
    report.append("| Protein | N | Tail N | Top-10% in tail (precision) | Tail in top-10% (recall) |\n")
    report.append("|---------|---|--------|----------------------------|-------------------------|\n")
    precisions = []
    recalls = []
    for p in proteins:
        p_recs = [r for r in records if r["protein"] == p]
        p_sorted = sorted(p_recs, key=lambda r: r["proj"], reverse=True)
        n_p = len(p_sorted)
        top_decile_n = max(1, n_p // 10)
        top_decile = p_sorted[:top_decile_n]
        tail_recs = [r for r in p_recs if r["in_tail"]]
        n_tail_p = len(tail_recs)
        n_top_in_tail = sum(r["in_tail"] for r in top_decile)
        precision = n_top_in_tail / top_decile_n if top_decile_n > 0 else 0
        recall = n_top_in_tail / n_tail_p if n_tail_p > 0 else 0
        precisions.append(precision)
        recalls.append(recall)
        report.append(f"| {p} | {n_p} | {n_tail_p} | {n_top_in_tail}/{top_decile_n} = {precision:.2f} | {n_top_in_tail}/{n_tail_p} = {recall:.2f} |\n")
    report.append(f"\nMean precision: {np.mean(precisions):.3f}\n")
    report.append(f"Mean recall: {np.mean(recalls):.3f}\n\n")

    # =========================================================================
    # 4. Effect sizes: Cohen's d for tail vs non-tail
    # =========================================================================
    report.append("## 4. Effect sizes\n\n")
    pooled_std = np.sqrt(((len(proj_tail) - 1) * proj_tail.var() + (len(proj_nontail) - 1) * proj_nontail.var()) / (N - 2))
    cohens_d = (proj_tail.mean() - proj_nontail.mean()) / pooled_std
    report.append(f"Cohen's d (tail vs non-tail): {cohens_d:.3f}\n")
    report.append(f"This is a {'large' if abs(cohens_d) > 0.8 else 'medium' if abs(cohens_d) > 0.5 else 'small'} effect.\n\n")

    # Mann-Whitney U
    u_stat, u_p = stats.mannwhitneyu(proj_tail, proj_nontail, alternative="greater")
    # Common language effect size: P(tail > nontail)
    cles = u_stat / (len(proj_tail) * len(proj_nontail))
    report.append(f"Mann-Whitney U: U={u_stat:.0f}, p={u_p:.2e}\n")
    report.append(f"Common Language Effect Size: P(tail residue scores higher than non-tail residue) = {cles:.3f}\n\n")

    # =========================================================================
    # 5. Logistic regression: P(in tail) from projection score
    # =========================================================================
    report.append("## 5. Reverse test: can projection score predict tail membership?\n\n")
    report.append("If the direction encodes these structural features, then projection score should predict tail membership.\n\n")

    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score, average_precision_score

    X_logit = projs.reshape(-1, 1)
    y_logit = in_tail
    lr = LogisticRegression()
    lr.fit(X_logit, y_logit)
    y_prob = lr.predict_proba(X_logit)[:, 1]
    auroc = roc_auc_score(y_logit, y_prob)
    auprc = average_precision_score(y_logit, y_prob)
    report.append(f"Logistic regression: P(in_tail | proj_score)\n")
    report.append(f"AUROC: {auroc:.4f}\n")
    report.append(f"AUPRC: {auprc:.4f} (baseline = {baseline_rate:.4f})\n")
    report.append(f"Logistic coef: {lr.coef_[0][0]:.4f}, intercept: {lr.intercept_[0]:.4f}\n\n")

    # Multi-feature logistic: P(top 10% | features)
    report.append("Multi-feature logistic: P(top-decile | structural features)\n\n")
    y_top10 = np.zeros(N)
    for p in proteins:
        p_idx = [i for i, r in enumerate(records) if r["protein"] == p]
        p_projs = projs[p_idx]
        threshold = np.percentile(p_projs, 90)
        for i in p_idx:
            if projs[i] >= threshold:
                y_top10[i] = 1

    X_multi = np.column_stack([
        np.array([1.0 if r["sse"] == "E" else 0.0 for r in records]),
        np.array([1.0 if r["sse"] == "H" else 0.0 for r in records]),
        np.array([r["rsa"] for r in records]),
        np.array([float(r["contacts_8A"]) for r in records]),
        np.array([r["self_hydro"] for r in records]),
    ])
    feature_names = ["SSE_E", "SSE_H", "RSA", "contacts_8A", "self_hydro"]
    lr_multi = LogisticRegression(max_iter=1000)
    lr_multi.fit(X_multi, y_top10)
    y_prob_multi = lr_multi.predict_proba(X_multi)[:, 1]
    auroc_multi = roc_auc_score(y_top10, y_prob_multi)
    auprc_multi = average_precision_score(y_top10, y_prob_multi)
    report.append(f"AUROC: {auroc_multi:.4f}\n")
    report.append(f"AUPRC: {auprc_multi:.4f} (baseline = {y_top10.mean():.4f})\n\n")
    report.append("| Feature | Logistic coef |\n")
    report.append("|---------|---------------|\n")
    for name, coef in zip(feature_names, lr_multi.coef_[0]):
        report.append(f"| {name} | {coef:.4f} |\n")
    report.append("\n")

    # =========================================================================
    # 6. Within-tail ranking: what residual signal remains?
    # =========================================================================
    report.append("## 6. Within-tail variance\n\n")
    report.append("After conditioning on tail membership, how much variance remains? This is the part attributable to the contextual layers 7-9 computation.\n\n")
    report.append(f"Total variance in projection scores: {projs.var():.4f}\n")
    report.append(f"Within-tail variance: {proj_tail.var():.4f}\n")
    report.append(f"Within-non-tail variance: {proj_nontail.var():.4f}\n")
    within_var = (len(proj_tail) * proj_tail.var() + len(proj_nontail) * proj_nontail.var()) / N
    report.append(f"Pooled within-group variance: {within_var:.4f}\n")
    report.append(f"Fraction of variance explained by tail membership: {1 - within_var / projs.var():.4f}\n\n")

    # Within tail: what's the range and how does the anchor compare?
    report.append("Within-tail projection score distribution per protein:\n\n")
    report.append("| Protein | Tail N | Tail mean | Tail std | Anchor proj | Anchor z (within tail) |\n")
    report.append("|---------|--------|-----------|----------|-------------|------------------------|\n")
    for p in proteins:
        p_recs = [r for r in records if r["protein"] == p and r["in_tail"]]
        if not p_recs:
            continue
        p_projs = np.array([r["proj"] for r in p_recs])
        anchor_rec = [r for r in p_recs if r["is_anchor"]]
        if anchor_rec:
            anchor_proj = anchor_rec[0]["proj"]
            z_within = (anchor_proj - p_projs.mean()) / p_projs.std() if p_projs.std() > 0 else 0
            report.append(f"| {p} | {len(p_recs)} | {p_projs.mean():.3f} | {p_projs.std():.3f} | {anchor_proj:.3f} | {z_within:.2f} |\n")
        else:
            report.append(f"| {p} | {len(p_recs)} | {p_projs.mean():.3f} | {p_projs.std():.3f} | - | - |\n")
    report.append("\n")

    # =========================================================================
    # Plots
    # =========================================================================
    print("Generating plots...")

    # Plot A: Distribution of projection scores, tail vs non-tail
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    bins = np.linspace(projs.min(), projs.max(), 60)
    ax.hist(proj_nontail, bins=bins, alpha=0.6, color="#888888", label=f"Non-tail (N={len(proj_nontail)})", density=True)
    ax.hist(proj_tail, bins=bins, alpha=0.7, color="#61afef", label=f"Tail (N={len(proj_tail)})", density=True)
    ax.axvline(proj_tail.mean(), color="#61afef", ls="--", lw=1.5)
    ax.axvline(proj_nontail.mean(), color="#888888", ls="--", lw=1.5)
    ax.set_xlabel("Projection score")
    ax.set_ylabel("Density")
    ax.set_title("Projection score distributions")
    ax.legend(fontsize=8)

    # Plot B: Enrichment curve
    ax = axes[1]
    ks_fine = list(range(5, min(500, N), 5))
    fracs_fine = []
    for k in ks_fine:
        top_k_idx = sorted_idx[:k]
        n_in = sum(in_tail[i] for i in top_k_idx)
        fracs_fine.append(n_in / k)
    ax.plot(ks_fine, fracs_fine, color="#61afef", lw=2)
    ax.axhline(baseline_rate, color="#888888", ls="--", lw=1, label=f"Baseline: {baseline_rate:.3f}")
    ax.set_xlabel("Top-k residues (by projection score)")
    ax.set_ylabel("Fraction in tail")
    ax.set_title("Enrichment of tail filter in top scorers")
    ax.legend(fontsize=8)

    plt.tight_layout()
    out = REPORT_DIR / "anchor_regression_v2_classification.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out}")
    report.append(f"## Plots\n\nSee anchor_regression_v2_classification.png\n")

    out_path = REPORT_DIR / "anchor_classification_analysis.md"
    with open(out_path, "w") as f:
        f.writelines(report)
    print(f"Saved: {out_path}")
    print("Done.")


if __name__ == "__main__":
    main()
