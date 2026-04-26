#!/usr/bin/env python3
"""Anchor contact steering: effect of suppressing the search direction on contact prediction.

For each protein with a PDB structure, steers against the L10H9 search direction d
at the anchor position with varying alpha, then evaluates contact prediction quality
using CASP-style Precision@L/k metrics for long-range contacts.

Intervention at the layer-10 attention LayerNorm output, anchor token only.
Two supported steering modes:
    projection: x[anchor] = x[anchor] - alpha * proj_d(x[anchor])
    direct:     x[anchor] = x[anchor] - alpha * d_unit

Usage:
    uv run python scripts/anchor_contact_steering.py --device cuda --sanity-check
    uv run python scripts/anchor_contact_steering.py --device cuda --max-proteins 5
    uv run python scripts/anchor_contact_steering.py --device cuda
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
from scipy.spatial.distance import cdist

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDB_DIR = DATA_DIR / "pdb"
EXPERIMENT_ROOT = ROOT / "reports" / "out2" / "suppressing_anchors"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"

NUM_LAYERS = 33
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN = "2B61A"

ALPHAS = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 10.0, 12.0, 14.0, 16.0, 32.0]
CONTACT_THRESHOLD_A = 8.0
MIN_SEQ_LEN = 100
MAX_SEQ_LEN = 500
MIN_LONG_RANGE_CONTACTS = 10
LONG_RANGE_SEP = 24
CHECKPOINT_EVERY = 50

# Heads to monitor in sanity checks
MONITOR_HEADS = [(10, 9), (32, 13)]


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model(device: str):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager").to(device).eval()
    model = NNsight(esm_model)
    contact_head = esm_model.esm.contact_head
    return model, tokenizer, esm_model, contact_head


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


def capture_projection_scores(model, tokenizer, sequence: str, d_unit: torch.Tensor, device: str) -> np.ndarray:
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    return (x_ln[1:-1] @ d_unit.cpu()).numpy()


def identify_anchors(model, tokenizer, sequence: str, device: str, top_k: int = 3) -> list[int]:
    """Identify anchor positions by actual L10H9 mean key attention mass on full sequence."""
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            cache = tracer.cache(modules=[attn_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    attn_HLL = cache[key].output[1].detach().cpu()[0]  # (H, L, L)
    attn_AA = attn_HLL[TARGET_HEAD, 1:-1, 1:-1].numpy()  # (n_res, n_res)
    key_mass = attn_AA.mean(axis=0)  # mean attention received by each residue
    ranked = np.argsort(-key_mass)
    return ranked[:top_k].tolist()


# ---------------------------------------------------------------------------
# PDB parsing and ground truth contacts
# ---------------------------------------------------------------------------

def _parse_pdb_residues(pdb_path: Path) -> list[dict]:
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
        results.append({"resid": resid, "aa": aa, "cb": cb})
    return results


def _align_pdb_to_seq(pdb_residues: list[dict], full_seq: str) -> dict[int, int]:
    pdb_tuples = [(r["resid"], r["aa"]) for r in pdb_residues]
    resids = [t[0] for t in pdb_tuples]
    n_seq = len(full_seq)
    min_resid = min(resids)
    max_resid = max(resids)
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


def parse_pdb_contacts(protein_key: str, full_seq: str) -> np.ndarray | None:
    pdb_id = protein_key[:4]
    pdb_path = PDB_DIR / f"{pdb_id}.pdb"
    if not pdb_path.exists():
        return None
    pdb_residues = _parse_pdb_residues(pdb_path)
    if not pdb_residues:
        return None
    mapping = _align_pdb_to_seq(pdb_residues, full_seq)
    if len(mapping) < len(pdb_residues) * 0.5:
        return None

    cb_coords = np.array([r["cb"] for r in pdb_residues])
    dists = cdist(cb_coords, cb_coords)
    pdb_contacts = dists < CONTACT_THRESHOLD_A

    seq_len = len(full_seq)
    gt_AA = np.zeros((seq_len, seq_len), dtype=bool)
    pdb_indices = sorted(mapping.keys())
    for i_idx, i_pdb in enumerate(pdb_indices):
        for j_pdb in pdb_indices[i_idx + 1:]:
            if pdb_contacts[i_pdb, j_pdb]:
                si = mapping[i_pdb]
                sj = mapping[j_pdb]
                gt_AA[si, sj] = True
                gt_AA[sj, si] = True
    return gt_AA


# ---------------------------------------------------------------------------
# Steering intervention + attention caching
# ---------------------------------------------------------------------------

@torch.no_grad()
def cache_attention_with_steering(
    model, tokenizer, sequence: str,
    anchor_positions: list[int],
    d_unit: torch.Tensor,
    alpha: float,
    device: str,
    steering_mode: str = "projection",
) -> tuple[list[torch.Tensor], dict, torch.Tensor]:
    """Cache attention from all 33 layers + logits after steering at anchor position(s).

    Steering modes at each anchor:
        projection:
            proj_d(x) = (x . d / ||d||^2) * d   (since d is unit, this is (x . d) * d)
            x' = x - alpha * proj_d(x)

        direct:
            x' = x - alpha * d

    For projection mode, alpha=1 zeroes the d-component exactly and alpha=2 flips it.
    Applied to LayerNorm output at layer 10.
    Returns (attn_LBHLL, inputs_BL, logits_BLV).
    """
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)

            if alpha != 0.0:
                d_device = d_unit.to(device)
                ln_out = ln_module.output
                for pos in anchor_positions:
                    tok_idx = pos + 1  # +1 for BOS
                    x_j = ln_out[:, tok_idx, :]
                    if steering_mode == "projection":
                        proj = (x_j @ d_device).unsqueeze(-1) * d_device  # (x . d) * d
                        ln_out[:, tok_idx, :] = x_j - alpha * proj
                    elif steering_mode == "direct":
                        ln_out[:, tok_idx, :] = x_j - alpha * d_device
                    else:
                        raise ValueError(f"Unknown steering_mode: {steering_mode}")
                ln_module.output = ln_out

            # NNsight envoys must be read in forward order; save final logits only
            # after reading/intervening on the layer-10 LayerNorm output.
            logits_save = model.output.logits.save()

    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    logits_BLV = logits_save.detach().cpu()
    return attn_LBHLL, inputs_BL, logits_BLV


@torch.no_grad()
def cache_attention_with_random_noise(
    model, tokenizer, sequence: str,
    noise_scale: float,
    device: str,
) -> list[torch.Tensor]:
    """Cache attention after adding random noise to ALL positions at L10 LayerNorm.

    Used as a propagation sanity check: does any perturbation at L10 reach downstream heads?
    """
    inputs_BL = tokenizer(sequence, return_tensors="pt").to(device)
    attn_modules = [model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(modules=attn_modules)
            ln_out = ln_module.output
            noise = torch.randn_like(ln_out) * noise_scale
            ln_module.output = ln_out + noise

    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_LBHLL


def compute_contacts_from_attention(attn_LBHLL, tokens_BL, attention_mask_BL, contact_head, device):
    attn_stack = [a.to(device) for a in attn_LBHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_stack, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]
    return contact_head(tokens_BL, attns_BLHLL)


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------

def _attn_summary(attn_LBHLL, layer, head, positions, seq_len):
    """Compute attention summary stats for a head at given positions."""
    attn_AA = attn_LBHLL[layer][0, head, 1:-1, 1:-1].numpy()
    key_mass = attn_AA.mean(axis=0)
    total_mass = sum(float(key_mass[p]) for p in positions)
    top1_pos = int(np.argmax(key_mass))
    p = key_mass / key_mass.sum()
    p = p[p > 0]
    entropy = float(-np.sum(p * np.log2(p)))
    max_entropy = np.log2(seq_len)
    return total_mass, top1_pos, entropy, max_entropy


def sanity_check(model, tokenizer, d_unit, device, all_seqs, steering_mode: str):
    """Verify steering works and downstream heads respond to L10 perturbations."""
    test_proteins = ["2B61A", "1PVGA", "3CSSA"]
    test_proteins = [p for p in test_proteins if p in all_seqs]

    sanity_alphas = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0]

    # ---- Part 1: Anchor identification (attention-based) ----
    print("\n" + "=" * 70)
    print("PART 1: Anchor identification (by L10H9 attention mass)")
    print("=" * 70)

    for protein_key in test_proteins:
        sequence = all_seqs[protein_key]
        anchors = identify_anchors(model, tokenizer, sequence, device, top_k=3)
        proj_scores = capture_projection_scores(model, tokenizer, sequence, d_unit, device)
        print(f"\n  {protein_key} ({len(sequence)} res)")
        for rank, pos in enumerate(anchors):
            print(f"    top-{rank+1}: pos={pos} aa={sequence[pos]} proj_score={proj_scores[pos]:.3f}")

    # ---- Part 2: Steering diffuses L10H9 attention ----
    print("\n" + "=" * 70)
    print("PART 2: Does steering diffuse L10H9 attention at anchor?")
    print("=" * 70)

    for protein_key in test_proteins:
        sequence = all_seqs[protein_key]
        seq_len = len(sequence)
        anchors_top3 = identify_anchors(model, tokenizer, sequence, device, top_k=3)
        anchor_top1 = anchors_top3[:1]
        print(f"\n--- {protein_key} | top-1 anchor: pos={anchor_top1[0]} ({sequence[anchor_top1[0]]}) ---")

        # Test top-1 steering
        print(f"  Steering top-1 only:")
        print(f"  {'alpha':>6}  |  L10H9: anchor_mass  top1_pos  entropy  |  L32H13: top1_pos  entropy")
        for alpha in sanity_alphas:
            attn_LBHLL, _, _ = cache_attention_with_steering(
                model, tokenizer, sequence, anchor_top1, d_unit, alpha, device, steering_mode=steering_mode
            )
            m10, t10, e10, me10 = _attn_summary(attn_LBHLL, 10, 9, anchor_top1, seq_len)
            m32, t32, e32, me32 = _attn_summary(attn_LBHLL, 32, 13, anchor_top1, seq_len)
            print(f"  {alpha:6.1f}  |          {m10:.4f}       {t10:>4d}    {e10:.1f}/{me10:.1f}  |            {t32:>4d}    {e32:.1f}/{me32:.1f}")

        # Test top-3 steering
        print(f"  Steering top-3 ({anchors_top3}):")
        print(f"  {'alpha':>6}  |  L10H9: top3_mass  top1_pos  entropy  |  L32H13: top1_pos  entropy")
        for alpha in sanity_alphas:
            attn_LBHLL, _, _ = cache_attention_with_steering(
                model, tokenizer, sequence, anchors_top3, d_unit, alpha, device, steering_mode=steering_mode
            )
            m10, t10, e10, me10 = _attn_summary(attn_LBHLL, 10, 9, anchors_top3, seq_len)
            m32, t32, e32, me32 = _attn_summary(attn_LBHLL, 32, 13, anchors_top3, seq_len)
            print(f"  {alpha:6.1f}  |          {m10:.4f}       {t10:>4d}    {e10:.1f}/{me10:.1f}  |            {t32:>4d}    {e32:.1f}/{me32:.1f}")

    # ---- Part 3: Downstream propagation check ----
    print("\n" + "=" * 70)
    print("PART 3: Does ANY large perturbation at L10 affect downstream heads?")
    print("Adding random noise (scale=10, 100) to ALL positions at L10 LN")
    print("=" * 70)

    for protein_key in test_proteins:
        sequence = all_seqs[protein_key]
        seq_len = len(sequence)
        print(f"\n  {protein_key} ({seq_len} res)")

        # Clean baseline
        attn_clean, _, _ = cache_attention_with_steering(
            model, tokenizer, sequence, [], d_unit, 0.0, device, steering_mode=steering_mode
        )
        clean_10 = attn_clean[10][0, 9, 1:-1, 1:-1].numpy()
        clean_32 = attn_clean[32][0, 13, 1:-1, 1:-1].numpy()

        for noise_scale in [10.0, 100.0]:
            attn_noisy = cache_attention_with_random_noise(model, tokenizer, sequence, noise_scale, device)
            noisy_10 = attn_noisy[10][0, 9, 1:-1, 1:-1].numpy()
            noisy_32 = attn_noisy[32][0, 13, 1:-1, 1:-1].numpy()
            # Mean absolute difference in attention patterns
            diff_10 = float(np.abs(noisy_10 - clean_10).mean())
            diff_32 = float(np.abs(noisy_32 - clean_32).mean())
            # Correlation of flattened attention matrices
            corr_10 = float(np.corrcoef(clean_10.flatten(), noisy_10.flatten())[0, 1])
            corr_32 = float(np.corrcoef(clean_32.flatten(), noisy_32.flatten())[0, 1])
            print(f"    noise={noise_scale:>5.0f}  |  L10H9 MAD={diff_10:.6f} corr={corr_10:.4f}  |  L32H13 MAD={diff_32:.6f} corr={corr_32:.4f}")

    print("\n" + "=" * 70)
    print("SANITY CHECK COMPLETE")
    print("Part 2: L10H9 anchor_mass should drop with alpha, entropy should rise.")
    print("Part 3: If corr < 1.0 at high noise, downstream heads DO respond to L10.")
    print("        If corr ~ 1.0 even at high noise, something is wrong.")
    print("=" * 70 + "\n")


# ---------------------------------------------------------------------------
# Precision metrics
# ---------------------------------------------------------------------------

def precision_at_k(pred_probs_AA: np.ndarray, gt_contacts_AA: np.ndarray, k: int, min_sep: int = LONG_RANGE_SEP) -> float:
    n = pred_probs_AA.shape[0]
    rows, cols = np.triu_indices(n, k=min_sep)
    pred_vals = pred_probs_AA[rows, cols]
    gt_vals = gt_contacts_AA[rows, cols]
    if len(pred_vals) == 0 or k == 0:
        return float("nan")
    top_k = min(k, len(pred_vals))
    top_indices = np.argsort(-pred_vals)[:top_k]
    return float(gt_vals[top_indices].sum()) / top_k


def evaluate_contact_prediction(pred_probs_AA: np.ndarray, gt_contacts_AA: np.ndarray, seq_len: int) -> dict:
    return {
        "P_L5": precision_at_k(pred_probs_AA, gt_contacts_AA, max(1, seq_len // 5)),
        "P_L2": precision_at_k(pred_probs_AA, gt_contacts_AA, max(1, seq_len // 2)),
        "P_L": precision_at_k(pred_probs_AA, gt_contacts_AA, seq_len),
    }


# ---------------------------------------------------------------------------
# Per-protein processing
# ---------------------------------------------------------------------------

def compute_kl_divergence(logits_clean_BLV: torch.Tensor, logits_steered_BLV: torch.Tensor) -> float:
    """KL(clean || steered) averaged over residue positions (excluding BOS/EOS)."""
    log_p = torch.nn.functional.log_softmax(logits_clean_BLV[0, 1:-1], dim=-1)
    log_q = torch.nn.functional.log_softmax(logits_steered_BLV[0, 1:-1], dim=-1)
    p = log_p.exp()
    kl_per_pos = (p * (log_p - log_q)).sum(dim=-1)  # (n_res,)
    return float(kl_per_pos.mean())


def compute_l10h9_top3_mass(attn_LBHLL: list[torch.Tensor]) -> float:
    """Median across queries of the top-3 key attention mass for L10H9."""
    attn_AA = attn_LBHLL[TARGET_LAYER][0, TARGET_HEAD, 1:-1, 1:-1].numpy()
    top3_per_query = np.sort(attn_AA, axis=1)[:, -3:].sum(axis=1)  # (n_res,)
    return float(np.median(top3_per_query))


def compute_l10h9_head_metrics(attn_LBHLL: list[torch.Tensor], anchor_positions: list[int]) -> dict:
    """Aggregate L10H9 key-distribution diagnostics over the steered anchor set."""
    attn_AA = attn_LBHLL[TARGET_LAYER][0, TARGET_HEAD, 1:-1, 1:-1].numpy()
    key_mass = attn_AA.mean(axis=0)
    total_mass = key_mass.sum()

    if total_mass <= 0:
        entropy = float("nan")
    else:
        p = key_mass / total_mass
        p = p[p > 0]
        entropy = float(-np.sum(p * np.log2(p)))

    seq_len = attn_AA.shape[0]
    max_entropy = np.log2(seq_len) if seq_len > 1 else 0.0
    entropy_norm = entropy / max_entropy if max_entropy > 0 and not np.isnan(entropy) else float("nan")

    return {
        "l10h9_anchor_mass": float(sum(key_mass[p] for p in anchor_positions)),
        "l10h9_top1_mass": float(np.max(key_mass)),
        "l10h9_entropy": entropy,
        "l10h9_entropy_norm": float(entropy_norm),
    }


def process_one_protein(
    model, tokenizer, contact_head,
    protein_key: str, sequence: str,
    d_unit: torch.Tensor, device: str,
    alphas: list[float],
    steering_mode: str,
    top_k: int = 1,
) -> list[dict]:
    seq_len = len(sequence)

    gt_contacts_AA = parse_pdb_contacts(protein_key, sequence)
    if gt_contacts_AA is None:
        return []

    n_lr = np.triu(gt_contacts_AA, k=LONG_RANGE_SEP).sum()
    if n_lr < MIN_LONG_RANGE_CONTACTS:
        return []

    anchors = identify_anchors(model, tokenizer, sequence, device, top_k=top_k)

    results = []
    logits_clean = None
    for alpha in alphas:
        attn_LBHLL, inputs_BL, logits_BLV = cache_attention_with_steering(
            model, tokenizer, sequence, anchors, d_unit, alpha, device, steering_mode=steering_mode
        )

        # Contact prediction metrics
        pred_AA = compute_contacts_from_attention(attn_LBHLL, inputs_BL["input_ids"], inputs_BL["attention_mask"], contact_head, device)
        pred_AA = pred_AA[0].detach().cpu().numpy()
        metrics = evaluate_contact_prediction(pred_AA, gt_contacts_AA, seq_len)

        # L10H9 top-3 attention mass (verticality)
        top3_mass = compute_l10h9_top3_mass(attn_LBHLL)
        head_metrics = compute_l10h9_head_metrics(attn_LBHLL, anchors)

        # KL divergence vs clean
        if alpha == 0.0:
            logits_clean = logits_BLV
            kl_div = 0.0
        else:
            kl_div = compute_kl_divergence(logits_clean, logits_BLV)

        results.append({
            "protein": protein_key,
            "seq_len": seq_len,
            "n_long_range_contacts": int(n_lr),
            "anchor_positions": str(anchors),
            "n_anchors_steered": len(anchors),
            "steering_mode": steering_mode,
            "alpha": alpha,
            **metrics,
            "kl_div": kl_div,
            "l10h9_top3_mass": top3_mass,
            **head_metrics,
        })

    return results


# ---------------------------------------------------------------------------
# Aggregation and plotting
# ---------------------------------------------------------------------------

def aggregate_and_plot(all_results: list[dict], output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "anchor_contact_steering_results.csv"
    fields = list(all_results[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_results)
    print(f"  Saved: {csv_path}")

    alphas_sorted = sorted(set(r["alpha"] for r in all_results))
    metrics = [
        "P_L5", "P_L2", "P_L", "kl_div", "l10h9_top3_mass",
        "l10h9_anchor_mass", "l10h9_top1_mass", "l10h9_entropy", "l10h9_entropy_norm",
    ]
    agg = {m: {"mean": [], "se": []} for m in metrics}

    for alpha in alphas_sorted:
        rows_at_alpha = [r for r in all_results if r["alpha"] == alpha]
        for m in metrics:
            vals = [r[m] for r in rows_at_alpha if not np.isnan(r[m])]
            agg[m]["mean"].append(np.mean(vals) if vals else float("nan"))
            agg[m]["se"].append(np.std(vals) / np.sqrt(len(vals)) if len(vals) > 1 else 0.0)

    summary = {
        "n_proteins": len(set(r["protein"] for r in all_results)),
        "alphas": alphas_sorted,
        "steering_mode": all_results[0].get("steering_mode", "projection"),
        "top_k": int(all_results[0].get("n_anchors_steered", 1)),
    }
    for m in metrics:
        summary[f"{m}_mean"] = agg[m]["mean"]
        summary[f"{m}_se"] = agg[m]["se"]
    with open(output_dir / "anchor_contact_steering_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  Saved: {output_dir / 'anchor_contact_steering_summary.json'}")

    # --- Main figure: 3 panels ---
    plt.rcParams.update({
        "font.size": 10, "axes.titlesize": 12, "axes.labelsize": 11,
        "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
        "figure.dpi": 200,
    })

    prec_colors = {"P_L5": "#D64550", "P_L2": "#5B7FA3", "P_L": "#61afef"}
    prec_labels = {"P_L5": "P@L/5", "P_L2": "P@L/2", "P_L": "P@L"}

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # Panel 1: Precision metrics
    ax = axes[0]
    for m in ["P_L5", "P_L2", "P_L"]:
        means = np.array(agg[m]["mean"])
        ses = np.array(agg[m]["se"])
        ax.plot(alphas_sorted, means, "o-", color=prec_colors[m], label=prec_labels[m], markersize=5)
        ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color=prec_colors[m])
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Long-range contact precision")
    ax.set_title("Contact prediction quality")
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Panel 2: KL divergence
    ax = axes[1]
    means = np.array(agg["kl_div"]["mean"])
    ses = np.array(agg["kl_div"]["se"])
    ax.plot(alphas_sorted, means, "o-", color="#e5c07b", markersize=5)
    ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color="#e5c07b")
    ax.set_xlabel("Alpha")
    ax.set_ylabel("KL divergence (nats)")
    ax.set_title("KL(clean || steered) logits")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Panel 3: L10H9 top-3 attention mass
    ax = axes[2]
    means = np.array(agg["l10h9_top3_mass"]["mean"])
    ses = np.array(agg["l10h9_top3_mass"]["se"])
    ax.plot(alphas_sorted, means, "o-", color="#98c379", markersize=5)
    ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color="#98c379")
    ax.set_xlabel("Alpha")
    ax.set_ylabel("Median top-3 key mass")
    ax.set_title("L10H9 verticality")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.suptitle("Effect of anchor search direction suppression", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_contact_steering.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_dir / 'anchor_contact_steering.png'}")

    # --- Head diagnostics figure ---
    diag_specs = [
        ("l10h9_anchor_mass", "Anchor key mass", "#c678dd"),
        ("l10h9_top1_mass", "Top-1 key mass", "#e06c75"),
        ("l10h9_entropy_norm", "Normalized entropy", "#56b6c2"),
        ("l10h9_top3_mass", "Median top-3 key mass", "#98c379"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for ax, (metric_name, ylabel, color) in zip(axes, diag_specs):
        means = np.array(agg[metric_name]["mean"])
        ses = np.array(agg[metric_name]["se"])
        ax.plot(alphas_sorted, means, "o-", color=color, markersize=5)
        ax.fill_between(alphas_sorted, means - ses, means + ses, alpha=0.15, color=color)
        ax.set_xlabel("Alpha")
        ax.set_ylabel(ylabel)
        ax.set_title(metric_name.replace("l10h9_", "L10H9 ").replace("_", " "))
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("L10H9 head-pattern diagnostics", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_contact_steering_head_diagnostics.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_dir / 'anchor_contact_steering_head_diagnostics.png'}")

    # --- Distribution figure: per-protein deltas at two alpha values ---
    baseline_by_prot = {}
    for r in all_results:
        if r["alpha"] == 0.0:
            baseline_by_prot[r["protein"]] = r

    show_alphas = [a for a in [4.0, 16.0] if a in alphas_sorted]
    if len(show_alphas) < 2:
        show_alphas = [a for a in alphas_sorted if a > 0][-2:] if len([a for a in alphas_sorted if a > 0]) >= 2 else [a for a in alphas_sorted if a > 0]

    fig, axes = plt.subplots(1, len(show_alphas), figsize=(5 * len(show_alphas), 4))
    if len(show_alphas) == 1:
        axes = [axes]
    for ax_idx, show_alpha in enumerate(show_alphas):
        ax = axes[ax_idx]
        deltas = []
        for r in all_results:
            if r["alpha"] == show_alpha and r["protein"] in baseline_by_prot:
                base = baseline_by_prot[r["protein"]]["P_L5"]
                if not np.isnan(base) and not np.isnan(r["P_L5"]):
                    deltas.append(r["P_L5"] - base)
        if deltas:
            ax.hist(deltas, bins=30, color=prec_colors["P_L5"], alpha=0.7, edgecolor="white")
            ax.axvline(0, color="gray", ls=":", lw=0.8)
            mean_d = np.mean(deltas)
            ax.axvline(mean_d, color="black", ls="--", lw=1)
            ax.set_title(f"alpha={show_alpha}  (mean delta={mean_d:.4f})")
        ax.set_xlabel("Delta P@L/5 (steered - clean)")
        ax.set_ylabel("Count")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.suptitle("Per-protein change in long-range P@L/5", fontsize=12)
    fig.tight_layout()
    fig.savefig(output_dir / "anchor_contact_steering_distributions.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_dir / 'anchor_contact_steering_distributions.png'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Anchor contact steering experiment")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-proteins", type=int, default=None)
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--top-k", type=int, default=1, choices=[1, 3], help="Steer top-1 or top-3 anchors")
    parser.add_argument("--steering-mode", type=str, default="projection", choices=["projection", "direct"])
    parser.add_argument("--sanity-check", action="store_true", help="Run sanity checks only, no contact evaluation")
    args = parser.parse_args()

    if args.output_dir is None:
        output_dir = EXPERIMENT_ROOT / "contact_steering" / f"{args.steering_mode}_top{args.top_k}"
    else:
        output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = output_dir / "anchor_contact_steering_results.csv"

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    print(f"Loading model on {args.device}...")
    model, tokenizer, esm_model, contact_head = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    search_dir = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)

    # Sanity check mode
    if args.sanity_check:
        sanity_check(model, tokenizer, d_unit, args.device, all_seqs, args.steering_mode)
        return

    # Build protein list
    pdb_files = {p.stem for p in PDB_DIR.glob("*.pdb")}
    proteins = []
    for key, seq in all_seqs.items():
        pdb_id = key[:4]
        if pdb_id in pdb_files and MIN_SEQ_LEN <= len(seq) <= MAX_SEQ_LEN:
            proteins.append(key)
    proteins.sort()
    print(f"Proteins with PDB and {MIN_SEQ_LEN}-{MAX_SEQ_LEN} residues: {len(proteins)}")

    if args.max_proteins is not None:
        proteins = proteins[:args.max_proteins]
        print(f"  Limited to {len(proteins)} proteins")

    # Resume from checkpoint
    completed = set()
    existing_rows = []
    if checkpoint_path.exists():
        with open(checkpoint_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                for k in ["seq_len", "n_long_range_contacts", "n_anchors_steered"]:
                    row[k] = int(row[k])
                for k in [
                    "alpha", "P_L5", "P_L2", "P_L", "kl_div", "l10h9_top3_mass",
                    "l10h9_anchor_mass", "l10h9_top1_mass", "l10h9_entropy", "l10h9_entropy_norm",
                ]:
                    if k in row:
                        row[k] = float(row[k])
                existing_rows.append(row)
                completed.add(row["protein"])
        print(f"  Resuming: {len(completed)} proteins already completed")

    remaining = [p for p in proteins if p not in completed]

    print(f"\nProcessing {len(remaining)} proteins ({len(completed)} already done)...\n")
    all_results = list(existing_rows)
    n_done = len(completed)
    n_skipped = 0
    t0 = time.time()

    for idx, protein_key in enumerate(remaining):
        sequence = all_seqs[protein_key]
        try:
            rows = process_one_protein(
                model, tokenizer, contact_head, protein_key, sequence,
                d_unit, args.device, ALPHAS, args.steering_mode, top_k=args.top_k,
            )
        except Exception as e:
            print(f"  ERROR on {protein_key}: {e}")
            continue

        if not rows:
            n_skipped += 1
            continue

        all_results.extend(rows)
        n_done += 1

        if (idx + 1) % 10 == 0:
            elapsed = time.time() - t0
            rate = (idx + 1) / elapsed
            remaining_time = (len(remaining) - idx - 1) / rate if rate > 0 else 0
            print(f"  [{idx + 1}/{len(remaining)}] {protein_key} | {n_done} done, {n_skipped} skipped | {elapsed:.0f}s elapsed, ~{remaining_time:.0f}s remaining")

        if (idx + 1) % CHECKPOINT_EVERY == 0:
            fields = list(all_results[0].keys())
            with open(checkpoint_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(all_results)
            print(f"  Checkpoint saved ({n_done} proteins)")

    elapsed = time.time() - t0
    print(f"\nDone: {n_done} proteins processed, {n_skipped} skipped in {elapsed:.0f}s")

    if not all_results:
        print("No results to report.")
        return

    print("\nGenerating plots and summary...")
    aggregate_and_plot(all_results, output_dir)
    print("Done.")


if __name__ == "__main__":
    main()
