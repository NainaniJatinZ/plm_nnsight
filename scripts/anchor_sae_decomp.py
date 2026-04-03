#!/usr/bin/env python3
"""Decompose the L10H9 anchor projection score through layer-8 SAE latents.

For each anchor position, decomposes x · d into:
  - per-latent contributions: a_i * (w_dec[i] · d_normed) * std
  - bias node:               (b_pre · d_normed) * std
  - mean node:               mu · d
  - error node:              (x - x_hat) · d

Where d is the key-side search direction (W_K^T @ q_mean).

The error node is computed once from the original forward pass and frozen.

v2 fixes:
  - Uses sae.LN() directly instead of manual LN (eliminates any std mismatch)
  - Verifies manual x_hat matches sae.forward_val() numerically
  - Replaces greedy reconstruction with least-squares projection (proper span coverage)
  - Uses matched controls from v3 regression (same SSE, RSA, contacts) instead of median
  - Compares anchor error properties to matched-control error (norm, directionality)

Usage:
    uv run python scripts/anchor_sae_decomp.py --device cuda
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

from helpers.utils import load_sae_prot

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
SEGMENT_RADIUS = 5
REFERENCE_PROTEIN = "2B61A"
SAE_LAYER = 8

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

MATCHES_CSV = REPORT_DIR / "anchor_regression_v3_matches.csv"


# ---------------------------------------------------------------------------
# Reused loading functions
# ---------------------------------------------------------------------------

def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    return protein_configs, seqs


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
        "W_Q_hd": W_Q[head].clone(),
        "b_Q_d": b_Q[head].clone(),
        "W_K_hd": W_K[head].clone(),
        "b_K_d": b_K[head].clone(),
    }


def build_clean_sequence(sequence: str, config: dict) -> str:
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_start, ss1_end = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_start, ss2_end = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
    masked = ["<mask>"] * n
    for i in range(ss1_start, ss1_end):
        if 0 <= i < n:
            masked[i] = sequence[i]
    for i in range(ss2_start, ss2_end):
        if 0 <= i < n:
            masked[i] = sequence[i]
    for i in range(max(0, ss1_start - flank), ss1_start):
        masked[i] = sequence[i]
    for i in range(ss2_end, min(n, ss2_end + flank)):
        masked[i] = sequence[i]
    return "".join(masked)


def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
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
# SAE decomposition of projection score
# ---------------------------------------------------------------------------

@torch.no_grad()
def decompose_through_sae(
    sae,
    x: torch.Tensor,
    d: torch.Tensor,
) -> dict:
    """Decompose x · d through the SAE into per-latent + error contributions.

    Uses sae.LN() directly to ensure exact match with the SAE's own normalization.
    Verifies manual x_hat matches sae.forward_val() numerically.

    Returns dict with per-latent contributions, error, bias, mu nodes, and verification.
    """
    x_3d = x.unsqueeze(0).unsqueeze(0)  # (1, 1, 1280) for SAE API

    # Use SAE's own LN to get exact mu, std
    x_normed_3d, mu_3d, std_3d = sae.LN(x_3d)
    mu = mu_3d.squeeze()  # scalar
    std = std_3d.squeeze()  # scalar
    x_normed = x_normed_3d.squeeze(0).squeeze(0)  # (1280,)

    # SAE encode (in normalized space)
    x_for_enc = x_normed - sae.b_pre
    pre_acts = x_for_enc @ sae.w_enc + sae.b_enc  # (4096,)
    acts = sae.topK_activation(pre_acts.unsqueeze(0), sae.k)[0]  # (4096,)

    # SAE decode (in normalized space)
    recons_normed = acts @ sae.w_dec + sae.b_pre  # (1280,)

    # Denormalize
    x_hat = recons_normed * std + mu

    # Verify against sae.forward_val()
    x_hat_ref = sae.forward_val(x_3d).squeeze(0).squeeze(0)
    ln_gap = float((x_hat - x_hat_ref).abs().max())

    # Error (frozen from original pass)
    error = x - x_hat

    # Projections
    total_proj = float(x @ d)
    recons_proj = float(x_hat @ d)
    error_proj = float(error @ d)

    # Error norms (for distinguishing "globally high error" from "error specifically along d")
    error_norm = float(error.norm())
    error_proj_frac = abs(error_proj) / (error_norm + 1e-8)  # |error · d| / ||error||

    # Per-latent contributions to x · d
    active_mask = acts != 0
    active_indices = torch.where(active_mask)[0]
    active_acts = acts[active_indices]

    w_dec_dot_d = sae.w_dec @ d  # (4096,)
    latent_contribs = active_acts * w_dec_dot_d[active_indices] * std

    # Bias and mu nodes
    bias_contrib = float(sae.b_pre @ d * std)
    mu_contrib = float(mu * d.sum())

    latent_sum = float(latent_contribs.sum())
    parts_sum = latent_sum + bias_contrib + mu_contrib + error_proj

    return {
        "total_proj": total_proj,
        "recons_proj": recons_proj,
        "error_proj": error_proj,
        "mu_contrib": mu_contrib,
        "bias_contrib": bias_contrib,
        "latent_sum": latent_sum,
        "parts_sum": parts_sum,
        "gap": abs(total_proj - parts_sum),
        "ln_gap": ln_gap,
        "error_norm": error_norm,
        "error_proj_frac": error_proj_frac,
        "n_active": int(active_mask.sum()),
        "active_indices": active_indices.cpu().tolist(),
        "active_acts": active_acts.cpu().tolist(),
        "active_contribs": latent_contribs.cpu().tolist(),
        "w_dec_dot_d": w_dec_dot_d.cpu(),
        "frac_explained_by_recons": recons_proj / total_proj if abs(total_proj) > 1e-8 else 0.0,
        "frac_explained_by_error": error_proj / total_proj if abs(total_proj) > 1e-8 else 0.0,
    }


def load_matched_controls() -> dict:
    """Load matched controls from v3 regression output.
    Returns dict: (protein, anchor_pos) -> list of control positions.
    """
    controls = {}
    if not MATCHES_CSV.exists():
        print(f"  WARNING: {MATCHES_CSV} not found, falling back to median controls")
        return controls
    with open(MATCHES_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            protein = row["protein"]
            anchor_pos = int(row["anchor_pos"])
            control_pos = int(row["control_pos"])
            key = (protein, anchor_pos)
            controls.setdefault(key, []).append(control_pos)
    return controls


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading configs...")
    protein_configs, seqs = load_configs()

    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir = compute_search_dir(model, tokenizer, ref_clean, weights, args.device)
    d = (search_dir / search_dir.norm().clamp(min=1e-8)).to(args.device)
    print(f"  Search direction norm: {search_dir.norm().item():.4f}")

    print(f"\nLoading SAE at layer {SAE_LAYER}...")
    sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=SAE_LAYER, device=args.device)
    sae.eval()

    # Load matched controls from v3 regression
    matched_controls = load_matched_controls()
    print(f"  Loaded matched controls for {len(matched_controls)} (protein, anchor) pairs")

    # ---------------------------------------------------------------------------
    # Decompose at anchor + matched-control positions for each protein
    # ---------------------------------------------------------------------------
    print("\nDecomposing projection scores through SAE...\n")

    all_decomps = {}
    latent_contribs_by_idx = {}

    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        if protein not in seqs:
            continue
        seq = seqs[protein]

        # Get layer-8 hidden states from full sequence
        inputs = tokenizer(seq, return_tensors="pt").to(args.device)
        with torch.no_grad():
            out = model._model.esm(**inputs, output_hidden_states=True)
        hidden = out.hidden_states[SAE_LAYER][0]  # (seq_len, 1280)

        anchor_tok = anchor_pos + 1  # +1 for BOS
        x_anchor = hidden[anchor_tok]
        decomp_anchor = decompose_through_sae(sae, x_anchor, d)

        # Get matched controls (from v3 regression) or fall back to median
        ctrl_key = (protein, anchor_pos)
        if ctrl_key in matched_controls:
            ctrl_positions = matched_controls[ctrl_key]
        else:
            all_projs = (hidden[1:-1] @ d).cpu()
            median_idx = int(torch.argsort(all_projs)[len(all_projs) // 2])
            ctrl_positions = [median_idx]

        ctrl_decomps = []
        for ctrl_pos in ctrl_positions:
            ctrl_tok = ctrl_pos + 1
            if ctrl_tok >= hidden.shape[0] - 1:
                continue
            ctrl_decomps.append(decompose_through_sae(sae, hidden[ctrl_tok], d))

        # Average control metrics
        if ctrl_decomps:
            mean_ctrl = {
                "total_proj": np.mean([c["total_proj"] for c in ctrl_decomps]),
                "recons_proj": np.mean([c["recons_proj"] for c in ctrl_decomps]),
                "error_proj": np.mean([c["error_proj"] for c in ctrl_decomps]),
                "error_norm": np.mean([c["error_norm"] for c in ctrl_decomps]),
                "error_proj_frac": np.mean([c["error_proj_frac"] for c in ctrl_decomps]),
            }
        else:
            mean_ctrl = {"total_proj": 0, "recons_proj": 0, "error_proj": 0, "error_norm": 0, "error_proj_frac": 0}

        print(f"  {protein} (ln_gap={decomp_anchor['ln_gap']:.2e}):")
        print(f"    Anchor pos={anchor_pos}: total={decomp_anchor['total_proj']:.3f}, recons={decomp_anchor['recons_proj']:.3f}, error={decomp_anchor['error_proj']:.3f}")
        print(f"      ||error||={decomp_anchor['error_norm']:.3f}, |error.d|/||error||={decomp_anchor['error_proj_frac']:.4f}")
        print(f"    Matched controls (n={len(ctrl_decomps)}): mean_total={mean_ctrl['total_proj']:.3f}, mean_error={mean_ctrl['error_proj']:.3f}")
        print(f"      mean_||error||={mean_ctrl['error_norm']:.3f}, mean_|error.d|/||error||={mean_ctrl['error_proj_frac']:.4f}")

        all_decomps[protein] = {
            "anchor": decomp_anchor,
            "controls": ctrl_decomps,
            "n_controls": len(ctrl_decomps),
            "mean_ctrl": mean_ctrl,
        }

        # Accumulate per-latent contributions
        for idx, contrib in zip(decomp_anchor["active_indices"], decomp_anchor["active_contribs"]):
            latent_contribs_by_idx.setdefault(idx, []).append((protein, contrib, True))
        for cd in ctrl_decomps:
            for idx, contrib in zip(cd["active_indices"], cd["active_contribs"]):
                latent_contribs_by_idx.setdefault(idx, []).append((protein, contrib, False))

    # ---------------------------------------------------------------------------
    # Find latents that consistently contribute positively at anchors
    # ---------------------------------------------------------------------------
    print("\n\nLatent contribution analysis (across all proteins)...\n")

    latent_summary = []
    for idx, entries in latent_contribs_by_idx.items():
        anchor_contribs = [c for _, c, is_a in entries if is_a]
        control_contribs = [c for _, c, is_a in entries if not is_a]
        n_anchor = len(anchor_contribs)
        n_control = len(control_contribs)
        mean_anchor = np.mean(anchor_contribs) if anchor_contribs else 0.0
        mean_control = np.mean(control_contribs) if control_contribs else 0.0
        latent_summary.append({
            "idx": idx,
            "n_anchor_active": n_anchor,
            "n_control_active": n_control,
            "mean_anchor_contrib": mean_anchor,
            "mean_control_contrib": mean_control,
            "diff": mean_anchor - mean_control,
        })

    latent_summary.sort(key=lambda x: x["mean_anchor_contrib"], reverse=True)
    print(f"Top 20 latents by mean anchor contribution to d-projection:\n")
    print(f"{'Latent':>8} {'N_anch':>7} {'N_ctrl':>7} {'Anchor':>10} {'Control':>10} {'Diff':>10}")
    print("-" * 55)
    for entry in latent_summary[:20]:
        print(f"{entry['idx']:>8d} {entry['n_anchor_active']:>7d} {entry['n_control_active']:>7d} {entry['mean_anchor_contrib']:>10.4f} {entry['mean_control_contrib']:>10.4f} {entry['diff']:>10.4f}")

    latent_summary.sort(key=lambda x: x["diff"], reverse=True)
    print(f"\nTop 20 latents by differential contribution (anchor - control):\n")
    print(f"{'Latent':>8} {'N_anch':>7} {'N_ctrl':>7} {'Anchor':>10} {'Control':>10} {'Diff':>10}")
    print("-" * 55)
    for entry in latent_summary[:20]:
        print(f"{entry['idx']:>8d} {entry['n_anchor_active']:>7d} {entry['n_control_active']:>7d} {entry['mean_anchor_contrib']:>10.4f} {entry['mean_control_contrib']:>10.4f} {entry['diff']:>10.4f}")

    # ---------------------------------------------------------------------------
    # Proper span coverage: least-squares projection of d onto W_dec
    # ---------------------------------------------------------------------------
    print("\n\nLeast-squares projection of d onto span(W_dec)...\n")

    w_dec = sae.w_dec.data  # (4096, 1280)
    d_cpu = d.cpu().to(torch.float64)
    W_T = w_dec.cpu().to(torch.float64).T  # (1280, 4096) — columns are decoder directions

    # Solve: min ||W_T @ alpha - d||^2
    result = torch.linalg.lstsq(W_T, d_cpu)
    alpha_hat = result.solution  # (4096,)
    d_hat = (W_T @ alpha_hat).float()
    d_cpu_f = d_cpu.float()
    lstsq_cos = float(torch.cosine_similarity(d_hat.unsqueeze(0), d_cpu_f.unsqueeze(0)))
    lstsq_residual = float((d_cpu_f - d_hat).norm())
    lstsq_alpha_nnz = int((alpha_hat.abs() > 1e-6).sum())
    print(f"  Full W_dec (4096 directions):")
    print(f"    cos(d, d_hat) = {lstsq_cos:.6f}")
    print(f"    ||d - d_hat|| = {lstsq_residual:.6f}")
    print(f"    Non-zero alpha coefficients: {lstsq_alpha_nnz}")

    # Also try with top-k most aligned decoder directions
    w_dec_dot_d = (w_dec @ d).cpu()
    abs_align, sorted_idx = torch.sort(w_dec_dot_d.abs(), descending=True)

    lstsq_curve = []
    for k_sub in [10, 20, 50, 100, 200, 500, 1000, 2000, 4096]:
        if k_sub > len(sorted_idx):
            continue
        sub_idx = sorted_idx[:k_sub]
        W_sub = W_T[:, sub_idx].to(torch.float64)
        result_sub = torch.linalg.lstsq(W_sub, d_cpu)
        alpha_sub = result_sub.solution
        d_hat_sub = (W_sub @ alpha_sub).float()
        cos_sub = float(torch.cosine_similarity(d_hat_sub.unsqueeze(0), d_cpu_f.unsqueeze(0)))
        resid_sub = float((d_cpu_f - d_hat_sub).norm())
        lstsq_curve.append((k_sub, cos_sub, resid_sub))
        print(f"    Top-{k_sub:>4d} directions: cos={cos_sub:.4f}, residual={resid_sub:.4f}")

    # ---------------------------------------------------------------------------
    # Error analysis: anchor vs matched-control error properties
    # ---------------------------------------------------------------------------
    print("\n\nError analysis: anchor vs matched-control...\n")

    proteins = list(all_decomps.keys())

    anchor_error_projs = [all_decomps[p]["anchor"]["error_proj"] for p in proteins]
    ctrl_error_projs = [all_decomps[p]["mean_ctrl"]["error_proj"] for p in proteins]
    anchor_error_norms = [all_decomps[p]["anchor"]["error_norm"] for p in proteins]
    ctrl_error_norms = [all_decomps[p]["mean_ctrl"]["error_norm"] for p in proteins]
    anchor_error_fracs = [all_decomps[p]["anchor"]["error_proj_frac"] for p in proteins]
    ctrl_error_fracs = [all_decomps[p]["mean_ctrl"]["error_proj_frac"] for p in proteins]

    print(f"  {'Metric':<30} {'Anchor mean':>12} {'Ctrl mean':>12} {'Diff':>12}")
    print(f"  {'-'*66}")
    print(f"  {'error . d':<30} {np.mean(anchor_error_projs):>12.3f} {np.mean(ctrl_error_projs):>12.3f} {np.mean(anchor_error_projs) - np.mean(ctrl_error_projs):>12.3f}")
    print(f"  {'||error||':<30} {np.mean(anchor_error_norms):>12.3f} {np.mean(ctrl_error_norms):>12.3f} {np.mean(anchor_error_norms) - np.mean(ctrl_error_norms):>12.3f}")
    print(f"  {'|error.d| / ||error||':<30} {np.mean(anchor_error_fracs):>12.4f} {np.mean(ctrl_error_fracs):>12.4f} {np.mean(anchor_error_fracs) - np.mean(ctrl_error_fracs):>12.4f}")

    from scipy import stats
    diffs_frac = np.array(anchor_error_fracs) - np.array(ctrl_error_fracs)
    if len(diffs_frac) >= 5:
        t_stat, t_p = stats.ttest_1samp(diffs_frac, 0)
        print(f"\n  Paired t-test on |error.d|/||error|| (anchor - ctrl): t={t_stat:.3f}, p={t_p:.4f}")
        print(f"  Mean difference: {diffs_frac.mean():.4f}, direction consistency: {(diffs_frac > 0).sum()}/{len(diffs_frac)}")

    diffs_norm = np.array(anchor_error_norms) - np.array(ctrl_error_norms)
    if len(diffs_norm) >= 5:
        t_stat_n, t_p_n = stats.ttest_1samp(diffs_norm, 0)
        print(f"  Paired t-test on ||error|| (anchor - ctrl): t={t_stat_n:.3f}, p={t_p_n:.4f}")

    # ---------------------------------------------------------------------------
    # Plots
    # ---------------------------------------------------------------------------
    print("\nGenerating plots...")

    # Plot 1: Per-protein decomposition bar chart (anchor vs matched-control mean)
    fig, ax = plt.subplots(figsize=(14, 5))
    x_pos = np.arange(len(proteins))
    width = 0.35
    anchor_recons = [all_decomps[p]["anchor"]["recons_proj"] for p in proteins]
    anchor_error_vals = [all_decomps[p]["anchor"]["error_proj"] for p in proteins]
    ctrl_recons_vals = [all_decomps[p]["mean_ctrl"]["recons_proj"] for p in proteins]
    ctrl_error_vals = [all_decomps[p]["mean_ctrl"]["error_proj"] for p in proteins]

    ax.bar(x_pos - width/2, anchor_recons, width, label="Anchor: SAE recons", color="#61afef", alpha=0.8)
    ax.bar(x_pos - width/2, anchor_error_vals, width, bottom=anchor_recons, label="Anchor: error node", color="#e06c75", alpha=0.8)
    ax.bar(x_pos + width/2, ctrl_recons_vals, width, label="Ctrl: SAE recons", color="#61afef", alpha=0.3)
    ax.bar(x_pos + width/2, ctrl_error_vals, width, bottom=ctrl_recons_vals, label="Ctrl: error node", color="#e06c75", alpha=0.3)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([p[:5] for p in proteins], rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Projection onto search direction d")
    ax.set_title("SAE decomposition: anchor vs matched controls (v3 regression)")
    ax.legend(fontsize=7)
    ax.axhline(0, color="black", lw=0.5)
    plt.tight_layout()
    out1 = REPORT_DIR / "anchor_sae_decomp_recons_vs_error.png"
    fig.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out1}")

    # Plot 2: Least-squares span coverage curve
    fig, ax = plt.subplots(figsize=(8, 5))
    ks_ls = [r[0] for r in lstsq_curve]
    cos_ls = [r[1] for r in lstsq_curve]
    ax.plot(ks_ls, cos_ls, "o-", color="#61afef", lw=1.5)
    ax.set_xlabel("Number of decoder directions (top-k by |alignment|)")
    ax.set_ylabel("cos(d, d_hat) — least-squares projection")
    ax.set_title("Span coverage of search direction d by W_dec subsets")
    ax.axhline(0.9, color="gray", ls="--", lw=0.5, label="cos = 0.9")
    ax.axhline(0.95, color="gray", ls=":", lw=0.5, label="cos = 0.95")
    ax.set_xscale("log")
    ax.legend(fontsize=7)
    plt.tight_layout()
    out2 = REPORT_DIR / "anchor_sae_decomp_lstsq_curve.png"
    fig.savefig(out2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out2}")

    # Plot 3: Top latent contributions at anchor positions (heatmap)
    latent_summary_by_anchor = sorted(latent_summary, key=lambda x: x["mean_anchor_contrib"], reverse=True)
    top_latents = [e["idx"] for e in latent_summary_by_anchor[:20]]
    fig, ax = plt.subplots(figsize=(14, 6))
    mat = np.zeros((len(proteins), len(top_latents)))
    for i, protein in enumerate(proteins):
        decomp = all_decomps[protein]["anchor"]
        contrib_dict = dict(zip(decomp["active_indices"], decomp["active_contribs"]))
        for j, lat_idx in enumerate(top_latents):
            mat[i, j] = contrib_dict.get(lat_idx, 0.0)
    im = ax.imshow(mat, aspect="auto", cmap="RdBu_r", vmin=-np.max(np.abs(mat)), vmax=np.max(np.abs(mat)))
    ax.set_xticks(range(len(top_latents)))
    ax.set_xticklabels([str(l) for l in top_latents], rotation=90, fontsize=7)
    ax.set_yticks(range(len(proteins)))
    ax.set_yticklabels([p[:5] for p in proteins], fontsize=7)
    ax.set_xlabel("SAE latent index")
    ax.set_ylabel("Protein")
    ax.set_title("Per-latent contribution to anchor projection score (top 20 latents)")
    fig.colorbar(im, ax=ax, fraction=0.02, pad=0.04)
    plt.tight_layout()
    out3 = REPORT_DIR / "anchor_sae_decomp_latent_heatmap.png"
    fig.savefig(out3, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out3}")

    # Plot 4: Error analysis — anchor vs matched-control
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    metrics_plot = [
        ([all_decomps[p]["anchor"]["error_proj"] for p in proteins], [all_decomps[p]["mean_ctrl"]["error_proj"] for p in proteins], "error . d"),
        ([all_decomps[p]["anchor"]["error_norm"] for p in proteins], [all_decomps[p]["mean_ctrl"]["error_norm"] for p in proteins], "||error||"),
        ([all_decomps[p]["anchor"]["error_proj_frac"] for p in proteins], [all_decomps[p]["mean_ctrl"]["error_proj_frac"] for p in proteins], "|error.d| / ||error||"),
    ]
    for ax, (anch_vals, ctrl_vals, label) in zip(axes, metrics_plot):
        for i in range(len(proteins)):
            ax.plot([0, 1], [anch_vals[i], ctrl_vals[i]], "o-", color="gray", alpha=0.4, markersize=3)
        ax.plot([0], [np.mean(anch_vals)], "s", color="#e06c75", markersize=8, zorder=5, label="Anchor mean")
        ax.plot([1], [np.mean(ctrl_vals)], "s", color="#61afef", markersize=8, zorder=5, label="Ctrl mean")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(["Anchor", "Matched ctrl"])
        ax.set_ylabel(label)
        ax.legend(fontsize=7)
    axes[0].set_title("Error projection onto d")
    axes[1].set_title("Total error norm")
    axes[2].set_title("Directional specificity of error")
    plt.tight_layout()
    out4 = REPORT_DIR / "anchor_sae_decomp_error_analysis.png"
    fig.savefig(out4, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out4}")

    # ---------------------------------------------------------------------------
    # Write report
    # ---------------------------------------------------------------------------
    print("\nWriting report...")
    report = []
    report.append("# SAE Decomposition of Anchor Projection Score (v2)\n\n")
    report.append(f"Search direction d: L10H9 key-side W_K^T @ q_mean from {REFERENCE_PROTEIN}.\n")
    report.append(f"SAE: InterProt layer {SAE_LAYER}, top-k={sae.k}, 4096 latents.\n\n")
    report.append("For each position, we decompose x . d = (SAE reconstruction) . d + error . d.\n")
    report.append("The SAE reconstruction further decomposes into per-latent contributions + bias + mean.\n")
    report.append("The error node is computed once from the original forward pass and frozen.\n\n")
    report.append("v2 changes: uses sae.LN() directly (verified against sae.forward_val()), matched controls from v3 regression (same SSE, RSA, contacts_8A), least-squares span coverage instead of greedy reconstruction, error directionality analysis.\n\n")

    # LN verification
    max_ln_gap = max(all_decomps[p]["anchor"]["ln_gap"] for p in proteins)
    report.append(f"## LN verification\n\nMax |x_hat_manual - sae.forward_val(x)| across all proteins: {max_ln_gap:.2e}.\n\n")

    report.append("## Per-protein decomposition\n\n")
    report.append("Controls are matched on SSE type, RSA, and contacts_8A from anchor_regression_v3.\n\n")
    report.append("| Protein | Type | N ctrl | Total | Recons | Error | ||error|| | |e.d|/||e|| |\n")
    report.append("|---------|------|--------|-------|--------|-------|----------|------------|\n")
    for protein in proteins:
        info = all_decomps[protein]
        anch = info["anchor"]
        mc = info["mean_ctrl"]
        report.append(f"| {protein} | anchor | - | {anch['total_proj']:.3f} | {anch['recons_proj']:.3f} | {anch['error_proj']:.3f} | {anch['error_norm']:.3f} | {anch['error_proj_frac']:.4f} |\n")
        report.append(f"| {protein} | ctrl_mean | {info['n_controls']} | {mc['total_proj']:.3f} | {mc['recons_proj']:.3f} | {mc['error_proj']:.3f} | {mc['error_norm']:.3f} | {mc['error_proj_frac']:.4f} |\n")
    report.append("\n")

    # Error analysis summary
    report.append("## Error analysis: anchor vs matched controls\n\n")
    report.append("Key question: are anchors specifically hard to reconstruct along d, or are they just globally high-error points?\n\n")
    report.append("|error.d|/||error|| measures what fraction of the total error vector is aligned with the search direction. If anchors have higher values than matched controls, the SAE specifically misses the d component at anchors rather than being generally worse at reconstructing them.\n\n")
    report.append(f"| Metric | Anchor mean | Ctrl mean | Diff |\n")
    report.append(f"|--------|-------------|-----------|------|\n")
    report.append(f"| error . d | {np.mean(anchor_error_projs):.3f} | {np.mean(ctrl_error_projs):.3f} | {np.mean(anchor_error_projs) - np.mean(ctrl_error_projs):.3f} |\n")
    report.append(f"| ||error|| | {np.mean(anchor_error_norms):.3f} | {np.mean(ctrl_error_norms):.3f} | {np.mean(anchor_error_norms) - np.mean(ctrl_error_norms):.3f} |\n")
    report.append(f"| |error.d|/||error|| | {np.mean(anchor_error_fracs):.4f} | {np.mean(ctrl_error_fracs):.4f} | {np.mean(anchor_error_fracs) - np.mean(ctrl_error_fracs):.4f} |\n")
    report.append("\n")
    if len(diffs_frac) >= 5:
        report.append(f"Paired t-test on |error.d|/||error|| (anchor - ctrl): t={t_stat:.3f}, p={t_p:.4f}, direction consistency={int((diffs_frac > 0).sum())}/{len(diffs_frac)}.\n")
        report.append(f"Paired t-test on ||error|| (anchor - ctrl): t={t_stat_n:.3f}, p={t_p_n:.4f}.\n\n")

    report.append("## Top 20 latents by mean anchor contribution\n\n")
    latent_summary.sort(key=lambda x: x["mean_anchor_contrib"], reverse=True)
    report.append("| Latent | N anchor | N control | Mean anchor | Mean control | Diff |\n")
    report.append("|--------|----------|-----------|-------------|--------------|------|\n")
    for entry in latent_summary[:20]:
        report.append(f"| {entry['idx']} | {entry['n_anchor_active']} | {entry['n_control_active']} | {entry['mean_anchor_contrib']:.4f} | {entry['mean_control_contrib']:.4f} | {entry['diff']:.4f} |\n")
    report.append("\n")

    report.append("## Top 20 latents by differential contribution (anchor - control)\n\n")
    latent_summary.sort(key=lambda x: x["diff"], reverse=True)
    report.append("| Latent | N anchor | N control | Mean anchor | Mean control | Diff |\n")
    report.append("|--------|----------|-----------|-------------|--------------|------|\n")
    for entry in latent_summary[:20]:
        report.append(f"| {entry['idx']} | {entry['n_anchor_active']} | {entry['n_control_active']} | {entry['mean_anchor_contrib']:.4f} | {entry['mean_control_contrib']:.4f} | {entry['diff']:.4f} |\n")
    report.append("\n")

    report.append("## Span coverage of d by W_dec (least-squares projection)\n\n")
    report.append("For each subset size k, we solve min ||W_dec_sub^T @ alpha - d||^2 and report cos(d, d_hat).\n")
    report.append("This is the correct test for whether d lies in the span of the decoder directions, unlike greedy reconstruction which is confounded by non-orthogonality of the overcomplete dictionary.\n\n")
    report.append(f"Full W_dec (4096 directions): cos = {lstsq_cos:.6f}, residual = {lstsq_residual:.6f}\n\n")
    report.append("| k (top by |align|) | cos(d, d_hat) | residual |\n")
    report.append("|---------------------|---------------|----------|\n")
    for k_sub, cos_sub, resid_sub in lstsq_curve:
        report.append(f"| {k_sub} | {cos_sub:.4f} | {resid_sub:.4f} |\n")
    report.append("\n")

    report.append("![Recons vs error](anchor_sae_decomp_recons_vs_error.png)\n\n")
    report.append("![Lstsq span coverage](anchor_sae_decomp_lstsq_curve.png)\n\n")
    report.append("![Latent heatmap](anchor_sae_decomp_latent_heatmap.png)\n\n")
    report.append("![Error analysis](anchor_sae_decomp_error_analysis.png)\n\n")

    out_report = REPORT_DIR / "anchor_sae_decomp.md"
    with open(out_report, "w") as f:
        f.writelines(report)
    print(f"  Saved: {out_report}")

    print("\nDone.")


if __name__ == "__main__":
    main()
