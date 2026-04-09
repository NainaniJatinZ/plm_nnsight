#!/usr/bin/env python3
"""Flank scramble experiment: sequence identity vs geometric logic.

For each confident anchor protein, scrambles the ±25 flank amino acids under
six conditions (preserving different levels of structural information) and
measures whether the anchor signal (alpha_norm) survives.

Conditions:
  C0: Baseline (no modification)
  C1: Scramble within SSE segments
  C2: Scramble across entire flank
  C3: Conservative physicochemical substitutions
  C4: Scramble buried positions only (RSA < 0.05)
  C5: Scramble exposed positions only (RSA > 0.25)
  C6: Random sequence (null control)

Primary analysis uses isolated flank (everything outside ±25 masked).
Secondary analysis uses full context.

Usage:
    PYTHONUNBUFFERED=1 uv run python scripts/scramble_experiment.py --device cuda
    PYTHONUNBUFFERED=1 uv run python scripts/scramble_experiment.py --device cuda --n-proteins 50 --n-repeats 5
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

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDB_DIR = DATA_DIR / "pdb"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN = "2B61A"
MASK_TOKEN = "<mask>"
FLANK_RADIUS = 25
MIN_EDGE_DISTANCE = 30
MIN_BASELINE_ALPHA = 0.3  # on full-sequence alpha (not isolated)

AUDIT_CSV = REPORT_DIR / "anchor_behavior_audit.csv"

# Physicochemical classes for C3
PHYSCHEM_CLASSES = {
    "A": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "V": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "I": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "L": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "M": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "F": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "W": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "P": ["A", "V", "I", "L", "M", "F", "W", "P"],
    "S": ["S", "T", "N", "Q", "Y", "C"],
    "T": ["S", "T", "N", "Q", "Y", "C"],
    "N": ["S", "T", "N", "Q", "Y", "C"],
    "Q": ["S", "T", "N", "Q", "Y", "C"],
    "Y": ["S", "T", "N", "Q", "Y", "C"],
    "C": ["S", "T", "N", "Q", "Y", "C"],
    "K": ["K", "R", "H"],
    "R": ["K", "R", "H"],
    "H": ["K", "R", "H"],
    "D": ["D", "E"],
    "E": ["D", "E"],
    "G": ["G"],
}

# Background AA frequencies (approximate UniRef50)
AA_FREQ = {"A": 0.0825, "R": 0.0553, "N": 0.0406, "D": 0.0545, "C": 0.0137, "Q": 0.0393, "E": 0.0675, "G": 0.0707, "H": 0.0227, "I": 0.0596, "L": 0.0966, "K": 0.0584, "M": 0.0242, "F": 0.0386, "P": 0.0470, "S": 0.0656, "T": 0.0534, "W": 0.0108, "Y": 0.0292, "V": 0.0687}
AA_LIST = list(AA_FREQ.keys())
AA_PROBS = np.array([AA_FREQ[aa] for aa in AA_LIST])
AA_PROBS = AA_PROBS / AA_PROBS.sum()

# Max ASA for RSA (Tien et al. 2013)
MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}


def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


# ---------------------------------------------------------------------------
# Data loading
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


def select_proteins(seqs, ss_dict, n):
    """Select top N proteins by top3_mass that have PDB, SSE, and pass quality filters."""
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
            pdb_path = PDB_DIR / f"{pid[:4]}.pdb"
            if not pdb_path.exists():
                continue
            rows.append({"protein": pid, "top3_mass": mass, "anchor_pos": anchor_pos, "n_res": n_res})
    rows.sort(key=lambda x: x["top3_mass"], reverse=True)
    return rows[:n]


# ---------------------------------------------------------------------------
# PDB feature computation (RSA for C4/C5)
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
        if ca is None:
            continue
        results.append({"resid": resid, "aa": aa, "ca": ca})
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


def compute_rsa_map(protein, full_seq):
    """Return {seq_pos: rsa} for positions with PDB coverage, or None on failure."""
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

    rsa_map = {}
    for pdb_idx, seq_pos in mapping.items():
        aa = full_seq[seq_pos]
        max_asa = MAX_ASA.get(aa, 200)
        sasa = sasa_by_resid.get(pdb_residues[pdb_idx]["resid"], 0)
        rsa_map[seq_pos] = min(sasa / max_asa, 1.0) if max_asa > 0 else 0.0
    return rsa_map


# ---------------------------------------------------------------------------
# Model loading and forward pass
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
    return {"W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(), "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone()}


def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Compute d = W_K^T @ q_mean from a reference protein."""
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


@torch.no_grad()
def run_forward(model, tokenizer, sequence_str: str, device: str):
    """Run forward pass, return L10 LN activations (n_res, 1280)."""
    inputs = tokenizer(sequence_str, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0, 1:-1]  # (n_res, 1280)
    return x_ln


def compute_alpha(x_ln, anchor_pos: int, d_unit: torch.Tensor) -> float:
    """Compute projection of anchor position onto search direction d."""
    proj_scores = (x_ln @ d_unit.cpu()).numpy()
    return float(proj_scores[anchor_pos])


# ---------------------------------------------------------------------------
# Sequence building helpers
# ---------------------------------------------------------------------------

def build_isolated_flank(sequence: str, anchor_pos: int, radius: int) -> str:
    """Mask everything outside [anchor-R, anchor+R]."""
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = []
    for i in range(n):
        if lo <= i <= hi:
            chars.append(sequence[i])
        else:
            chars.append(MASK_TOKEN)
    return " ".join(chars)


def build_full_context(sequence: str) -> str:
    """Space-separated full sequence for ESM tokenizer."""
    return " ".join(sequence)


# ---------------------------------------------------------------------------
# Scramble conditions
# ---------------------------------------------------------------------------

def get_flank_positions(anchor_pos: int, n_res: int, radius: int = FLANK_RADIUS):
    """Return sorted list of flank positions (excludes anchor itself)."""
    lo = max(0, anchor_pos - radius)
    hi = min(n_res - 1, anchor_pos + radius)
    return [i for i in range(lo, hi + 1) if i != anchor_pos]


def apply_c1_within_sse(sequence: str, anchor_pos: int, sse: str, rng: np.random.RandomState) -> str:
    """Scramble within each contiguous SSE segment in the flank."""
    chars = list(sequence)
    flank = get_flank_positions(anchor_pos, len(sequence))
    flank_set = set(flank)

    # Find contiguous SSE segments within the flank
    segments = []
    current_segment = []
    for pos in sorted(flank):
        if current_segment and (pos != current_segment[-1] + 1 or sse[pos] != sse[current_segment[-1]]):
            if len(current_segment) > 1:
                segments.append(current_segment[:])
            current_segment = [pos]
        else:
            current_segment.append(pos)
    if len(current_segment) > 1:
        segments.append(current_segment)

    for seg in segments:
        seg_chars = [chars[p] for p in seg]
        rng.shuffle(seg_chars)
        for p, c in zip(seg, seg_chars):
            chars[p] = c
    return "".join(chars)


def apply_c2_scramble_all(sequence: str, anchor_pos: int, rng: np.random.RandomState) -> str:
    """Scramble all flank positions (ignoring SSE)."""
    chars = list(sequence)
    flank = get_flank_positions(anchor_pos, len(sequence))
    flank_chars = [chars[p] for p in flank]
    rng.shuffle(flank_chars)
    for p, c in zip(flank, flank_chars):
        chars[p] = c
    return "".join(chars)


def apply_c3_conservative(sequence: str, anchor_pos: int, rng: np.random.RandomState) -> str:
    """Replace each flank AA with a random AA from same physicochemical class."""
    chars = list(sequence)
    flank = get_flank_positions(anchor_pos, len(sequence))
    for p in flank:
        aa = chars[p]
        group = PHYSCHEM_CLASSES.get(aa, [aa])
        # Pick a different AA from same class if possible
        candidates = [a for a in group if a != aa]
        if candidates:
            chars[p] = rng.choice(candidates)
        # else keep as is (e.g., G)
    return "".join(chars)


def apply_c4_scramble_buried(sequence: str, anchor_pos: int, rsa_map: dict, rng: np.random.RandomState) -> str:
    """Scramble only buried positions (RSA < 0.05) in the flank."""
    chars = list(sequence)
    flank = get_flank_positions(anchor_pos, len(sequence))
    buried = [p for p in flank if p in rsa_map and rsa_map[p] < 0.05]
    if len(buried) < 2:
        return "".join(chars)
    buried_chars = [chars[p] for p in buried]
    rng.shuffle(buried_chars)
    for p, c in zip(buried, buried_chars):
        chars[p] = c
    return "".join(chars)


def apply_c5_scramble_exposed(sequence: str, anchor_pos: int, rsa_map: dict, rng: np.random.RandomState) -> str:
    """Scramble only exposed positions (RSA > 0.25) in the flank."""
    chars = list(sequence)
    flank = get_flank_positions(anchor_pos, len(sequence))
    exposed = [p for p in flank if p in rsa_map and rsa_map[p] > 0.25]
    if len(exposed) < 2:
        return "".join(chars)
    exposed_chars = [chars[p] for p in exposed]
    rng.shuffle(exposed_chars)
    for p, c in zip(exposed, exposed_chars):
        chars[p] = c
    return "".join(chars)


def apply_c6_random(sequence: str, anchor_pos: int, rng: np.random.RandomState) -> str:
    """Replace all flank positions with random AAs from background frequency."""
    chars = list(sequence)
    flank = get_flank_positions(anchor_pos, len(sequence))
    for p in flank:
        chars[p] = rng.choice(AA_LIST, p=AA_PROBS)
    return "".join(chars)


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--n-proteins", type=int, default=200)
    parser.add_argument("--n-repeats", type=int, default=10)
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    device = args.device
    n_repeats = args.n_repeats

    flush_print(f"Device: {device}, n_proteins: {args.n_proteins}, n_repeats: {n_repeats}")

    # Load data
    flush_print("Loading data...")
    seqs, ss_dict = load_data()

    # Load model
    flush_print("Loading model...")
    model, tokenizer = load_model(device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    # Compute search direction d
    flush_print("Computing search direction d from reference protein...")
    ref_seq = " ".join(seqs[REFERENCE_PROTEIN])
    d_vec = compute_search_dir(model, tokenizer, ref_seq, weights, device)
    d_unit = d_vec / d_vec.norm().clamp(min=1e-8)

    # Select proteins
    flush_print("Selecting proteins...")
    proteins = select_proteins(seqs, ss_dict, n=args.n_proteins)
    flush_print(f"  Selected {len(proteins)} candidates (before baseline filter)")

    # Pre-compute RSA maps for all proteins
    flush_print("Computing RSA maps...")
    rsa_cache = {}
    for pinfo in proteins:
        pid = pinfo["protein"]
        rsa_cache[pid] = compute_rsa_map(pid, seqs[pid])

    # Phase 1: compute full-sequence baseline alpha for all proteins and filter
    flush_print("Computing full-sequence baselines (C0)...")
    full_alphas = {}
    for i, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        full_seq_str = build_full_context(seq)
        x_ln = run_forward(model, tokenizer, full_seq_str, device)
        alpha = compute_alpha(x_ln, anchor, d_unit)
        full_alphas[pid] = alpha
        if (i + 1) % 50 == 0:
            flush_print(f"  Baseline: {i + 1}/{len(proteins)}")

    # Filter to proteins with baseline alpha > MIN_BASELINE_ALPHA
    proteins = [p for p in proteins if full_alphas[p["protein"]] > MIN_BASELINE_ALPHA]
    flush_print(f"  After baseline filter (alpha > {MIN_BASELINE_ALPHA}): {len(proteins)} proteins")

    if len(proteins) == 0:
        flush_print("ERROR: No proteins pass baseline filter. Exiting.")
        return

    # Phase 2: run all conditions (full context: scramble flank, rest unchanged)
    CONDITIONS = ["C0", "C1", "C2", "C3", "C4", "C5", "C6"]
    STOCHASTIC = {"C1", "C2", "C3", "C4", "C5", "C6"}

    results = []  # list of dicts
    t0 = time.time()
    n_total = len(proteins)

    for pi, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        sse = ss_dict[pid]
        rsa_map = rsa_cache.get(pid)

        # C0: baseline (full sequence, already computed)
        alpha_full = full_alphas[pid]
        alpha_norm_c0 = 1.0  # by definition

        results.append({"protein": pid, "anchor_pos": anchor, "condition": "C0", "repeat": 0, "alpha": alpha_full, "alpha_full": alpha_full, "alpha_norm": alpha_norm_c0})

        # C1-C6
        for cond in ["C1", "C2", "C3", "C4", "C5", "C6"]:
            repeats = n_repeats if cond in STOCHASTIC else 1
            for rep in range(repeats):
                rng = np.random.RandomState(42 + rep * 1000 + pi)

                if cond == "C1":
                    mod_seq = apply_c1_within_sse(seq, anchor, sse, rng)
                elif cond == "C2":
                    mod_seq = apply_c2_scramble_all(seq, anchor, rng)
                elif cond == "C3":
                    mod_seq = apply_c3_conservative(seq, anchor, rng)
                elif cond == "C4":
                    if rsa_map is None:
                        continue
                    mod_seq = apply_c4_scramble_buried(seq, anchor, rsa_map, rng)
                elif cond == "C5":
                    if rsa_map is None:
                        continue
                    mod_seq = apply_c5_scramble_exposed(seq, anchor, rsa_map, rng)
                elif cond == "C6":
                    mod_seq = apply_c6_random(seq, anchor, rng)

                # Run full context (scrambled flank + rest of protein unchanged)
                full_mod_str = build_full_context(mod_seq)
                x_ln = run_forward(model, tokenizer, full_mod_str, device)
                alpha = compute_alpha(x_ln, anchor, d_unit)
                alpha_norm = alpha / alpha_full if abs(alpha_full) > 1e-8 else 0.0

                results.append({"protein": pid, "anchor_pos": anchor, "condition": cond, "repeat": rep, "alpha": alpha, "alpha_full": alpha_full, "alpha_norm": alpha_norm})

        elapsed = time.time() - t0
        rate = (pi + 1) / elapsed
        eta = (n_total - pi - 1) / rate if rate > 0 else 0
        if (pi + 1) % 10 == 0 or pi == 0:
            flush_print(f"  Protein {pi + 1}/{n_total} ({pid}): C0 alpha_norm={alpha_norm_c0:.3f} | elapsed={elapsed:.0f}s, ETA={eta:.0f}s")

    flush_print(f"\nDone. {len(results)} rows collected in {time.time() - t0:.0f}s")

    # Save raw results
    csv_path = REPORT_DIR / "scramble_results.csv"
    fieldnames = ["protein", "anchor_pos", "condition", "repeat", "alpha", "alpha_full", "alpha_norm"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    flush_print(f"Saved: {csv_path}")

    # ---------------------------------------------------------------------------
    # Analysis
    # ---------------------------------------------------------------------------
    analyze_results(results)


def analyze_results(results):
    """Analyze and plot scramble experiment results."""
    import pandas as pd

    df = pd.DataFrame(results)
    conditions = ["C0", "C1", "C2", "C3", "C4", "C5", "C6"]
    cond_labels = {"C0": "Baseline", "C1": "Within-SSE\nscramble", "C2": "Full flank\nscramble", "C3": "Conservative\nsubstitution", "C4": "Scramble\nburied", "C5": "Scramble\nexposed", "C6": "Random\n(null)"}

    # Compute per-protein mean across repeats
    summary = df.groupby(["protein", "condition"])["alpha_norm"].agg(["mean", "std"]).reset_index()
    summary.columns = ["protein", "condition", "alpha_norm_mean", "alpha_norm_std"]

    # Print summary table
    flush_print("\n" + "=" * 70)
    flush_print("SCRAMBLE EXPERIMENT RESULTS")
    flush_print("=" * 70)
    flush_print(f"\n{'Condition':<25} {'Mean alpha_norm':>15} {'Std':>10} {'Survival (>0.5)':>18} {'N':>5}")
    flush_print("-" * 75)

    summary_stats = {}
    for cond in conditions:
        sub = summary[summary["condition"] == cond]
        if len(sub) == 0:
            continue
        mean_val = sub["alpha_norm_mean"].mean()
        std_val = sub["alpha_norm_mean"].std()
        survival = (sub["alpha_norm_mean"] > 0.5).mean()
        n = len(sub)
        summary_stats[cond] = {"mean": mean_val, "std": std_val, "survival": survival, "n": n}
        flush_print(f"{cond} ({cond_labels[cond].replace(chr(10), ' ')}){'':<3} {mean_val:>15.4f} {std_val:>10.4f} {survival:>17.1%} {n:>5}")

    # Decision table interpretation
    flush_print("\n" + "=" * 70)
    flush_print("INTERPRETATION")
    flush_print("=" * 70)

    c1_preserved = summary_stats.get("C1", {}).get("survival", 0) > 0.5
    c3_preserved = summary_stats.get("C3", {}).get("survival", 0) > 0.5
    c2_preserved = summary_stats.get("C2", {}).get("survival", 0) > 0.5
    c6_dead = summary_stats.get("C6", {}).get("survival", 0) < 0.3

    if c1_preserved and c3_preserved:
        flush_print("\nC1 preserved + C3 preserved => GEOMETRIC LOGIC: coarse physical properties + SSE layout is sufficient.")
    elif c1_preserved and not c3_preserved:
        flush_print("\nC1 preserved + C3 drops => SSE-specific composition matters but not physical class (unusual).")
    elif not c1_preserved and c3_preserved:
        flush_print("\nC1 drops + C3 preserved => FINE-GRAINED GEOMETRIC: position-specific physicochemical profile matters.")
    else:
        flush_print("\nC1 drops + C3 drops => SEQUENCE IDENTITY: specific amino acid identities at specific positions are required.")

    if c1_preserved and not c2_preserved:
        flush_print("C1 preserved but C2 drops => SSE-specific composition matters (which AAs are in helices vs strands).")
    elif c1_preserved and c2_preserved:
        flush_print("Both C1 and C2 preserved => even SSE-specific composition is not needed; something coarser is enough.")

    c4_surv = summary_stats.get("C4", {}).get("survival", 0)
    c5_surv = summary_stats.get("C5", {}).get("survival", 0)
    if c4_surv < 0.5 and c5_surv > 0.5:
        flush_print("C4 kills signal, C5 preserves => model reads buried residue identities specifically.")
    elif c4_surv > 0.5 and c5_surv < 0.5:
        flush_print("C4 preserves, C5 kills signal => model reads exposed residue identities specifically.")
    elif c4_surv > 0.5 and c5_surv > 0.5:
        flush_print("Both C4 and C5 preserve signal => model uses a property invariant to individual AA identity.")
    else:
        flush_print("Both C4 and C5 kill signal => both buried and exposed identities matter.")

    if not c6_dead:
        flush_print("WARNING: C6 (random null) did NOT kill the signal. Something may be wrong with the experimental setup.")

    # Compute paired deltas
    flush_print("\nPaired delta (C0 - Ci) per condition:")
    c0_by_protein = summary[summary["condition"] == "C0"].set_index("protein")["alpha_norm_mean"]
    for cond in ["C1", "C2", "C3", "C4", "C5", "C6"]:
        sub = summary[summary["condition"] == cond].set_index("protein")["alpha_norm_mean"]
        common = c0_by_protein.index.intersection(sub.index)
        if len(common) == 0:
            continue
        deltas = c0_by_protein.loc[common] - sub.loc[common]
        flush_print(f"  {cond}: mean delta = {deltas.mean():.4f} (std={deltas.std():.4f}, median={deltas.median():.4f})")

    # ---------------------------------------------------------------------------
    # Plots
    # ---------------------------------------------------------------------------

    # Plot 1: Box plot of alpha_norm by condition
    fig, ax = plt.subplots(figsize=(10, 6))
    box_data = []
    box_labels = []
    for cond in conditions:
        sub = summary[summary["condition"] == cond]["alpha_norm_mean"]
        if len(sub) > 0:
            box_data.append(sub.values)
            box_labels.append(cond_labels[cond])
    bp = ax.boxplot(box_data, tick_labels=box_labels, patch_artist=True, showfliers=True, flierprops=dict(markersize=3, alpha=0.3))
    colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336", "#00BCD4", "#795548"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.axhline(y=0.5, color="gray", linestyle="--", alpha=0.5, label="survival threshold")
    ax.axhline(y=1.0, color="gray", linestyle=":", alpha=0.3)
    ax.set_ylabel("alpha_norm (mean across repeats)")
    ax.set_title("Anchor signal preservation under flank scrambling")
    ax.legend()
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "scramble_alpha_by_condition.png", dpi=150)
    plt.close(fig)
    flush_print(f"Saved: {REPORT_DIR / 'scramble_alpha_by_condition.png'}")

    # Plot 2: Survival rate bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    survivals = []
    labels = []
    for cond in conditions:
        sub = summary[summary["condition"] == cond]
        if len(sub) > 0:
            survivals.append((sub["alpha_norm_mean"] > 0.5).mean())
            labels.append(cond_labels[cond])
    bars = ax.bar(range(len(survivals)), survivals, color=colors[:len(survivals)], alpha=0.7)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_ylabel("Fraction of proteins with alpha_norm > 0.5")
    ax.set_title("Anchor signal survival rate by condition")
    ax.set_ylim(0, 1.1)
    for bar, val in zip(bars, survivals):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02, f"{val:.0%}", ha="center", va="bottom", fontsize=9)
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "scramble_survival_rate.png", dpi=150)
    plt.close(fig)
    flush_print(f"Saved: {REPORT_DIR / 'scramble_survival_rate.png'}")

    # Plot 3: Paired delta distributions
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for idx, cond in enumerate(["C1", "C2", "C3", "C4", "C5", "C6"]):
        ax = axes[idx]
        sub = summary[summary["condition"] == cond].set_index("protein")["alpha_norm_mean"]
        common = c0_by_protein.index.intersection(sub.index)
        if len(common) == 0:
            ax.set_title(f"{cond}: no data")
            continue
        deltas = c0_by_protein.loc[common] - sub.loc[common]
        ax.hist(deltas.values, bins=30, alpha=0.7, color=colors[idx + 1], edgecolor="black", linewidth=0.5)
        ax.axvline(x=0, color="black", linestyle="-", alpha=0.3)
        ax.axvline(x=deltas.mean(), color="red", linestyle="--", alpha=0.7, label=f"mean={deltas.mean():.3f}")
        ax.set_title(f"{cond}: {cond_labels[cond].replace(chr(10), ' ')}")
        ax.set_xlabel("delta alpha_norm (C0 - Ci)")
        ax.legend(fontsize=8)
    plt.suptitle("Paired alpha_norm change per condition", fontsize=13)
    plt.tight_layout()
    fig.savefig(REPORT_DIR / "scramble_paired_delta.png", dpi=150)
    plt.close(fig)
    flush_print(f"Saved: {REPORT_DIR / 'scramble_paired_delta.png'}")

    # Write markdown report
    write_report(summary_stats, summary, c0_by_protein, c1_preserved, c3_preserved, c2_preserved, c6_dead)


def write_report(summary_stats, summary, c0_by_protein, c1_preserved, c3_preserved, c2_preserved, c6_dead):
    """Write a markdown report summarizing the experiment results."""
    lines = []
    lines.append("# Scramble Experiment Results\n")
    lines.append(f"N proteins = {summary_stats.get('C0', {}).get('n', 0)}, repeats per stochastic condition = see CSV\n")

    lines.append("## Summary statistics\n")
    lines.append("| Condition | Description | Mean alpha_norm | Std | Survival rate |")
    lines.append("|---|---|---|---|---|")
    desc_map = {"C0": "Baseline (full context)", "C1": "Within-SSE scramble", "C2": "Full flank scramble", "C3": "Conservative substitution", "C4": "Scramble buried only", "C5": "Scramble exposed only", "C6": "Random (null control)"}
    for cond in ["C0", "C1", "C2", "C3", "C4", "C5", "C6"]:
        s = summary_stats.get(cond)
        if s is None:
            continue
        lines.append(f"| {cond} | {desc_map[cond]} | {s['mean']:.4f} | {s['std']:.4f} | {s['survival']:.1%} |")

    lines.append("\n## Interpretation\n")
    if c1_preserved and c3_preserved:
        lines.append("C1 and C3 both preserved the anchor signal. The model identifies anchors using coarse physical properties and SSE layout, consistent with geometric logic rather than sequence identity reading.")
    elif c1_preserved and not c3_preserved:
        lines.append("C1 preserved but C3 dropped. SSE-specific amino acid composition matters, but not physicochemical class. This is an unusual pattern.")
    elif not c1_preserved and c3_preserved:
        lines.append("C1 dropped but C3 preserved. The model uses position-specific physicochemical profiles (fine-grained geometric logic). It does not need specific AA identities but does need the right physical properties at each position.")
    else:
        lines.append("Both C1 and C3 dropped the anchor signal. The model requires specific amino acid identities at specific positions (sequence identity hypothesis).")

    if not c6_dead:
        lines.append("\nWARNING: The null control (C6) did not fully destroy the signal, which raises concerns about the experimental setup.")

    lines.append("")
    report_path = REPORT_DIR / "scramble_experiment.md"
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    flush_print(f"Saved: {report_path}")


if __name__ == "__main__":
    main()
