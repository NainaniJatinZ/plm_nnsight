#!/usr/bin/env python3
"""SAE Frozen-Error Zero-Ablation IE Ranking and Sufficiency.

For the top 50 most confident anchor proteins (from the large anchor-behavior audit),
this script:
1. Decomposes layer-8 residual stream through the InterProt SAE (frozen error node)
2. Ranks latent-token pairs by IE = activation * gradient wrt L10H9 pre-softmax anchor score
3. Tests sufficiency by keeping only top-k IE pairs and zeroing everything else
4. Runs coarse decomposition controls (full vs latents-only vs error-only)

Usage:
    uv run python scripts/anchor_sae_frozen_error_ie_v1.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import gc
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

from helpers.utils import load_sae_prot

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
SAE_LAYER = 8
SAE_DIM = 4096
K_VALUES = [1, 2, 5, 10, 20, 50, 100, 200, 500]
PREFIX = "anchor_sae_frozen_error_ie_v1"


# ---------------------------------------------------------------------------
# Protein selection from audit CSV
# ---------------------------------------------------------------------------

def select_proteins(audit_csv: Path, seqs: dict, n: int = 50) -> list[dict]:
    """Select top-n most confident anchor proteins from the behavior audit."""
    rows = []
    with open(audit_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            protein = row["protein"]
            if protein not in seqs:
                continue
            rank_corr = float(row["rank_corr"])
            top3_key_mass = float(row["top3_key_mass"])
            top1_alpha = float(row["top5_proj"].split(";")[0])
            top_key_idx = int(row["top_key_idx"])
            if rank_corr >= 0.95 and top3_key_mass >= 0.70 and top1_alpha >= 0.25:
                rows.append({
                    "protein": protein,
                    "rank_corr": rank_corr,
                    "top3_key_mass": top3_key_mass,
                    "top1_alpha": top1_alpha,
                    "anchor_idx": top_key_idx,
                })

    if len(rows) < n:
        print(f"  Warning: only {len(rows)} proteins pass filters (requested {n})")

    rc = np.array([r["rank_corr"] for r in rows])
    km = np.array([r["top3_key_mass"] for r in rows])
    al = np.array([r["top1_alpha"] for r in rows])
    def zscore(x):
        return (x - x.mean()) / (x.std() + 1e-8)
    confidence = zscore(rc) + zscore(km) + zscore(al)
    for i, r in enumerate(rows):
        r["confidence"] = float(confidence[i])

    rows.sort(key=lambda r: r["confidence"], reverse=True)
    selected = rows[:n]
    print(f"  {len(rows)} proteins pass filters, selected top {len(selected)} by confidence")
    return selected


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model(device: str):
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager").to(device).eval()
    for p in esm_model.parameters():
        p.requires_grad_(False)
    return esm_model, tokenizer


def extract_head_weights(esm_model, layer: int, head: int, device: str) -> dict:
    attn = esm_model.esm.encoder.layer[layer].attention
    W_Q = attn.self.query.weight.data.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)[head].to(device)
    b_Q = attn.self.query.bias.data.reshape(NUM_HEADS, HEAD_DIM)[head].to(device)
    W_K = attn.self.key.weight.data.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)[head].to(device)
    b_K = attn.self.key.bias.data.reshape(NUM_HEADS, HEAD_DIM)[head].to(device)
    return {"W_Q": W_Q, "b_Q": b_Q, "W_K": W_K, "b_K": b_K}


# ---------------------------------------------------------------------------
# SAE decomposition (vectorised over tokens)
# ---------------------------------------------------------------------------

@torch.no_grad()
def sae_decompose(sae, hidden_states: torch.Tensor):
    """Decompose all tokens through SAE. Returns acts (L,4096), mu (L,1), std (L,1), error (L,1280)."""
    x_3d = hidden_states.unsqueeze(0)  # (1, L, 1280)
    x_normed, mu, std = sae.LN(x_3d)
    x_normed = x_normed.squeeze(0)
    mu = mu.squeeze(0)  # (L, 1)
    std = std.squeeze(0)  # (L, 1)
    x_for_enc = x_normed - sae.b_pre
    pre_acts = x_for_enc @ sae.w_enc + sae.b_enc
    acts = sae.topK_activation(pre_acts.unsqueeze(0), sae.k).squeeze(0)
    recons_normed = acts @ sae.w_dec + sae.b_pre
    x_hat = recons_normed * std + mu
    error = hidden_states - x_hat
    return acts, mu, std, error


def reconstruct_from_acts(acts, sae, mu, std, error):
    """Differentiable reconstruction: (acts @ w_dec + b_pre)*std + mu + error."""
    recons_normed = acts @ sae.w_dec + sae.b_pre
    return recons_normed * std + mu + error


# ---------------------------------------------------------------------------
# Anchor-head metrics from layer-10 LN output
# ---------------------------------------------------------------------------

def compute_metrics(x_ln, weights, anchor_tok):
    """Compute M_score (tensor), M_attn (float), score_rank, attn_rank from L10 LN output (B,L,D)."""
    x = x_ln[0]  # (L, 1280) strip batch
    q = x @ weights["W_Q"].T + weights["b_Q"]
    k = x @ weights["W_K"].T + weights["b_K"]
    k_a = k[anchor_tok]
    presoftmax = (q @ k_a) / (HEAD_DIM ** 0.5)
    M_score = presoftmax[1:-1].mean()
    scores_all = q @ k.T / (HEAD_DIM ** 0.5)
    attn_probs = F.softmax(scores_all, dim=-1)
    M_attn = float(attn_probs[1:-1, anchor_tok].mean().item())
    anchor_res = anchor_tok - 1
    mean_key_attn = attn_probs[1:-1, 1:-1].mean(dim=0)
    attn_rank = int((mean_key_attn > mean_key_attn[anchor_res]).sum().item()) + 1
    mean_key_score = (q[1:-1] @ k[1:-1].T / (HEAD_DIM ** 0.5)).mean(dim=0)
    score_rank = int((mean_key_score > mean_key_score[anchor_res]).sum().item()) + 1
    return M_score, M_attn, score_rank, attn_rank


# ---------------------------------------------------------------------------
# Hook-based forward with layer-8 replacement
# ---------------------------------------------------------------------------

def _replace_output(replacement, out):
    """Replace hidden states in layer output, preserving format (tuple or tensor)."""
    if isinstance(out, tuple):
        return (replacement,) + out[1:]
    return replacement


def forward_with_replacement(esm_model, inputs, replacement, weights, anchor_tok):
    """Forward pass replacing layer-8 output; returns metrics under no_grad."""
    captured = {}
    def l8_hook(mod, inp, out):
        return _replace_output(replacement, out)
    def ln10_hook(mod, inp, out):
        captured["x"] = out
        return out

    h1 = esm_model.esm.encoder.layer[SAE_LAYER].register_forward_hook(l8_hook)
    h2 = esm_model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm.register_forward_hook(ln10_hook)
    with torch.no_grad():
        esm_model(**inputs)
    h1.remove()
    h2.remove()

    M_score_t, M_attn, score_rank, attn_rank = compute_metrics(captured["x"], weights, anchor_tok)
    return float(M_score_t.item()), M_attn, score_rank, attn_rank


# ---------------------------------------------------------------------------
# IE computation (gradient-based)
# ---------------------------------------------------------------------------

def compute_ie(esm_model, inputs, sae, acts_clean, mu, std, error_frozen, weights, anchor_tok):
    """Compute IE[t,l] = a_clean[t,l] * dM_score/da[t,l]. Returns IE tensor and M_score."""
    acts_leaf = acts_clean.clone().detach().requires_grad_(True)
    replacement = reconstruct_from_acts(acts_leaf, sae, mu, std, error_frozen).unsqueeze(0)

    captured = {}
    def l8_hook(mod, inp, out):
        return _replace_output(replacement, out)
    def ln10_hook(mod, inp, out):
        captured["x"] = out
        return out

    h1 = esm_model.esm.encoder.layer[SAE_LAYER].register_forward_hook(l8_hook)
    h2 = esm_model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm.register_forward_hook(ln10_hook)
    esm_model(**inputs)
    h1.remove()
    h2.remove()

    M_score_t, _, _, _ = compute_metrics(captured["x"], weights, anchor_tok)
    M_score_t.backward()

    grad = acts_leaf.grad
    ie = acts_leaf.detach() * grad
    return ie, float(M_score_t.item())


# ---------------------------------------------------------------------------
# Sufficiency sweep
# ---------------------------------------------------------------------------

def run_sufficiency(esm_model, inputs, sae, acts_clean, mu, std, error_frozen,
                    ie, weights, anchor_tok, clean_M_score, clean_M_attn):
    active_mask = acts_clean != 0
    active_ie = ie[active_mask]
    active_pos = active_mask.nonzero()
    sorted_idx = active_ie.abs().argsort(descending=True)
    n_active = len(sorted_idx)

    results = []
    for k in K_VALUES:
        actual_k = min(k, n_active)
        mod_acts = torch.zeros_like(acts_clean)
        top_positions = active_pos[sorted_idx[:actual_k]]
        mod_acts[top_positions[:, 0], top_positions[:, 1]] = acts_clean[top_positions[:, 0], top_positions[:, 1]]

        replacement = reconstruct_from_acts(mod_acts, sae, mu, std, error_frozen).unsqueeze(0)
        ms, ma, sr, ar = forward_with_replacement(esm_model, inputs, replacement, weights, anchor_tok)
        results.append({
            "k": k, "actual_k": actual_k,
            "M_score": ms, "M_score_frac": ms / clean_M_score if abs(clean_M_score) > 1e-8 else 0.0,
            "M_attn": ma, "M_attn_frac": ma / clean_M_attn if abs(clean_M_attn) > 1e-8 else 0.0,
            "score_rank": sr, "attn_rank": ar,
        })
    return results


# ---------------------------------------------------------------------------
# Coarse controls
# ---------------------------------------------------------------------------

def run_coarse(esm_model, inputs, sae, acts_clean, mu, std, error_frozen, weights, anchor_tok):
    conditions = {
        "A_full": (acts_clean, error_frozen),
        "B_latents_only": (acts_clean, torch.zeros_like(error_frozen)),
        "C_error_only": (torch.zeros_like(acts_clean), error_frozen),
    }
    out = {}
    for name, (a, e) in conditions.items():
        replacement = reconstruct_from_acts(a, sae, mu, std, e).unsqueeze(0)
        ms, ma, sr, ar = forward_with_replacement(esm_model, inputs, replacement, weights, anchor_tok)
        out[name] = {"M_score": ms, "M_attn": ma, "score_rank": sr, "attn_rank": ar}
    return out


# ---------------------------------------------------------------------------
# Per-protein analysis
# ---------------------------------------------------------------------------

def analyze_protein(pid, sequence, anchor_idx, esm_model, tokenizer, sae, weights, device):
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    anchor_tok = anchor_idx + 1  # BOS offset

    # --- Clean forward: cache layer-8 hidden and layer-10 LN ---
    captured = {}
    def l8_hook(mod, inp, out):
        captured["l8"] = out[0].detach()
        return out
    def ln10_hook(mod, inp, out):
        captured["ln10"] = out.detach()
        return out

    h1 = esm_model.esm.encoder.layer[SAE_LAYER].register_forward_hook(l8_hook)
    h2 = esm_model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm.register_forward_hook(ln10_hook)
    with torch.no_grad():
        esm_model(**inputs)
    h1.remove()
    h2.remove()

    layer8_hidden = captured["l8"]  # (L, 1280) — batch dim already stripped by out[0] in hook
    clean_M_score_t, clean_M_attn, clean_sr, clean_ar = compute_metrics(captured["ln10"], weights, anchor_tok)
    clean_M_score = float(clean_M_score_t.item())
    del captured

    # --- SAE decomposition ---
    acts_clean, mu, std, error_frozen = sae_decompose(sae, layer8_hidden)
    n_active = int((acts_clean != 0).sum().item())
    del layer8_hidden

    # --- IE ranking ---
    ie, ie_mscore = compute_ie(esm_model, inputs, sae, acts_clean, mu, std, error_frozen, weights, anchor_tok)
    ie_gap = abs(ie_mscore - clean_M_score)

    # Top-20 IE pairs
    active_mask = acts_clean != 0
    active_ie = ie[active_mask]
    active_pos = active_mask.nonzero()
    sorted_idx = active_ie.abs().argsort(descending=True)

    top20 = []
    for i in range(min(20, len(sorted_idx))):
        idx = sorted_idx[i]
        t, l = active_pos[idx]
        top20.append({
            "rank": i + 1,
            "token_pos": int(t.item()) - 1,
            "latent_idx": int(l.item()),
            "ie_value": float(active_ie[idx].item()),
            "activation": float(acts_clean[t, l].item()),
            "is_anchor_token": int(t.item()) == anchor_tok,
        })

    # IE mass concentration
    total_ie = float(active_ie.abs().sum().item())
    if total_ie > 1e-8:
        anch_mask = active_pos[:, 0] == anchor_tok
        ie_mass_anchor = float(active_ie[anch_mask].abs().sum().item()) / total_ie
        near_mask = (active_pos[:, 0] - anchor_tok).abs() <= 5
        ie_mass_near = float(active_ie[near_mask].abs().sum().item()) / total_ie
    else:
        ie_mass_anchor = 0.0
        ie_mass_near = 0.0

    # --- Sufficiency ---
    suff = run_sufficiency(esm_model, inputs, sae, acts_clean, mu, std, error_frozen, ie, weights, anchor_tok, clean_M_score, clean_M_attn)

    # Minimal k for 50/80/90% recovery
    k_thresholds = {}
    for thr_name, thr_val in [("k_50", 0.50), ("k_80", 0.80), ("k_90", 0.90)]:
        k_thresholds[thr_name] = None
        for s in suff:
            if s["M_score_frac"] >= thr_val:
                k_thresholds[thr_name] = s["k"]
                break

    # --- Coarse controls ---
    coarse = run_coarse(esm_model, inputs, sae, acts_clean, mu, std, error_frozen, weights, anchor_tok)

    # Cleanup
    del acts_clean, mu, std, error_frozen, ie, active_ie, active_pos
    gc.collect()
    torch.cuda.empty_cache()

    return {
        "protein": pid, "n_res": len(sequence), "anchor_idx": anchor_idx,
        "n_active": n_active,
        "clean_M_score": clean_M_score, "clean_M_attn": clean_M_attn,
        "clean_score_rank": clean_sr, "clean_attn_rank": clean_ar,
        "ie_gap": ie_gap,
        "ie_mass_anchor": ie_mass_anchor, "ie_mass_near": ie_mass_near,
        "top20": top20,
        "sufficiency": suff, "k_thresholds": k_thresholds,
        "coarse": coarse,
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def make_plots(all_results):
    """Generate the 5 plots specified in the experiment."""
    n = len(all_results)

    # --- Plot 1: Sufficiency curves ---
    fig, ax = plt.subplots(figsize=(8, 5))
    for metric_key, label, ls in [("M_score_frac", "M_score", "-"), ("M_attn_frac", "M_attn", "--")]:
        per_k = {k: [] for k in K_VALUES}
        for r in all_results:
            for s in r["sufficiency"]:
                per_k[s["k"]].append(s[metric_key])
        means = [np.mean(per_k[k]) for k in K_VALUES]
        medians = [np.median(per_k[k]) for k in K_VALUES]
        ax.plot(K_VALUES, means, f"o{ls}", label=f"{label} mean")
        ax.plot(K_VALUES, medians, f"s{ls}", label=f"{label} median", alpha=0.6)
    ax.axhline(1.0, color="gray", ls=":", alpha=0.5)
    ax.axhline(0.5, color="gray", ls=":", alpha=0.3)
    ax.set_xscale("log")
    ax.set_xlabel("Top-k IE pairs kept")
    ax.set_ylabel("Fraction of clean metric retained")
    ax.set_title(f"Sufficiency curves (n={n} proteins)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(REPORT_DIR / f"{PREFIX}_sufficiency.png", dpi=150)
    plt.close(fig)

    # --- Plot 2: Histogram of minimal k ---
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for ax, (thr_name, thr_label) in zip(axes, [("k_50", "50%"), ("k_80", "80%"), ("k_90", "90%")]):
        vals = [r["k_thresholds"][thr_name] for r in all_results if r["k_thresholds"][thr_name] is not None]
        none_count = sum(1 for r in all_results if r["k_thresholds"][thr_name] is None)
        if vals:
            ax.hist(vals, bins=K_VALUES + [1000], edgecolor="black", alpha=0.7)
        ax.set_title(f"Min k for {thr_label} recovery\n({none_count} never reached)")
        ax.set_xlabel("k")
        ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / f"{PREFIX}_min_k_hist.png", dpi=150)
    plt.close(fig)

    # --- Plot 3: Coarse control bar chart ---
    fig, ax = plt.subplots(figsize=(6, 5))
    conds = ["A_full", "B_latents_only", "C_error_only"]
    labels = ["Full (lat+err)", "Latents only", "Error only"]
    score_means = []
    score_stds = []
    for c in conds:
        vals = [r["coarse"][c]["M_score"] / r["clean_M_score"] if abs(r["clean_M_score"]) > 1e-8 else 0 for r in all_results]
        score_means.append(np.mean(vals))
        score_stds.append(np.std(vals))
    x_pos = np.arange(len(conds))
    ax.bar(x_pos, score_means, yerr=score_stds, capsize=5, color=["#4CAF50", "#2196F3", "#FF9800"], edgecolor="black")
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_ylabel("M_score fraction of clean")
    ax.set_title(f"Coarse decomposition controls (n={n})")
    ax.axhline(1.0, color="gray", ls=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(REPORT_DIR / f"{PREFIX}_coarse.png", dpi=150)
    plt.close(fig)

    # --- Plot 4: Top recurring latent indices ---
    latent_counter = Counter()
    for r in all_results:
        for p in r["top20"]:
            latent_counter[p["latent_idx"]] += 1
    top30_latents = latent_counter.most_common(30)
    if top30_latents:
        fig, ax = plt.subplots(figsize=(10, 4))
        lat_ids = [str(x[0]) for x in top30_latents]
        counts = [x[1] for x in top30_latents]
        ax.bar(range(len(counts)), counts, edgecolor="black", alpha=0.7)
        ax.set_xticks(range(len(lat_ids)))
        ax.set_xticklabels(lat_ids, rotation=90, fontsize=7)
        ax.set_xlabel("Latent index")
        ax.set_ylabel(f"Count in top-20 IE pairs (across {n} proteins)")
        ax.set_title("Most recurring SAE latents")
        fig.tight_layout()
        fig.savefig(REPORT_DIR / f"{PREFIX}_recurring_latents.png", dpi=150)
        plt.close(fig)

    # --- Plot 5: Token-position concentration ---
    fig, ax = plt.subplots(figsize=(6, 5))
    anchor_fracs = [r["ie_mass_anchor"] for r in all_results]
    near_fracs = [r["ie_mass_near"] for r in all_results]
    rest_fracs = [1.0 - r["ie_mass_near"] for r in all_results]
    means = [np.mean(anchor_fracs), np.mean(near_fracs) - np.mean(anchor_fracs), np.mean(rest_fracs)]
    labels_pos = ["Anchor token", "Near anchor (+-5)", "Rest of sequence"]
    ax.bar(range(3), means, color=["#E53935", "#FF9800", "#90CAF9"], edgecolor="black")
    ax.set_xticks(range(3))
    ax.set_xticklabels(labels_pos)
    ax.set_ylabel("Fraction of total |IE| mass")
    ax.set_title(f"IE mass concentration (n={n})")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / f"{PREFIX}_ie_concentration.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def write_report(all_results):
    n = len(all_results)
    lines = [f"# SAE Frozen-Error IE Ranking and Sufficiency (v1)\n"]
    lines.append(f"Proteins analysed: {n}\n")

    # Coarse control summary
    lines.append("## Coarse decomposition controls\n")
    lines.append("| Condition | M_score frac (mean +- std) | M_attn frac (mean +- std) |")
    lines.append("|---|---|---|")
    for c, label in [("A_full", "Full (lat+err)"), ("B_latents_only", "Latents only"), ("C_error_only", "Error only")]:
        ms_vals = [r["coarse"][c]["M_score"] / r["clean_M_score"] if abs(r["clean_M_score"]) > 1e-8 else 0 for r in all_results]
        ma_vals = [r["coarse"][c]["M_attn"] / r["clean_M_attn"] if abs(r["clean_M_attn"]) > 1e-8 else 0 for r in all_results]
        lines.append(f"| {label} | {np.mean(ms_vals):.3f} +- {np.std(ms_vals):.3f} | {np.mean(ma_vals):.3f} +- {np.std(ma_vals):.3f} |")
    lines.append("")

    # Sufficiency summary
    lines.append("## Sufficiency summary\n")
    lines.append("| k | M_score frac mean | M_score frac median | M_attn frac mean | M_attn frac median |")
    lines.append("|---|---|---|---|---|")
    for k in K_VALUES:
        ms = [s["M_score_frac"] for r in all_results for s in r["sufficiency"] if s["k"] == k]
        ma = [s["M_attn_frac"] for r in all_results for s in r["sufficiency"] if s["k"] == k]
        lines.append(f"| {k} | {np.mean(ms):.3f} | {np.median(ms):.3f} | {np.mean(ma):.3f} | {np.median(ma):.3f} |")
    lines.append("")

    # Minimal k thresholds
    lines.append("## Minimal k for recovery thresholds\n")
    for thr_name, thr_label in [("k_50", "50%"), ("k_80", "80%"), ("k_90", "90%")]:
        vals = [r["k_thresholds"][thr_name] for r in all_results if r["k_thresholds"][thr_name] is not None]
        n_none = sum(1 for r in all_results if r["k_thresholds"][thr_name] is None)
        if vals:
            lines.append(f"- {thr_label}: mean={np.mean(vals):.1f}, median={np.median(vals):.1f} ({n_none}/{n} never reached)")
        else:
            lines.append(f"- {thr_label}: no proteins reached this threshold")
    lines.append("")

    # IE concentration
    lines.append("## IE mass concentration\n")
    anchor_m = np.mean([r["ie_mass_anchor"] for r in all_results])
    near_m = np.mean([r["ie_mass_near"] for r in all_results])
    lines.append(f"- Mean |IE| at anchor token: {anchor_m:.3f}")
    lines.append(f"- Mean |IE| within +-5 of anchor: {near_m:.3f}")
    lines.append(f"- Mean |IE| rest of sequence: {1 - near_m:.3f}")
    lines.append("")

    # Top recurring latents
    latent_counter = Counter()
    for r in all_results:
        for p in r["top20"]:
            latent_counter[p["latent_idx"]] += 1
    lines.append("## Top 10 recurring latent indices (in top-20 IE pairs)\n")
    lines.append("| Latent | Count |")
    lines.append("|---|---|")
    for lat, cnt in latent_counter.most_common(10):
        lines.append(f"| {lat} | {cnt}/{n} |")
    lines.append("")

    # Interpretation
    lines.append("## Interpretation\n")
    full_ms = np.mean([r["coarse"]["A_full"]["M_score"] / r["clean_M_score"] if abs(r["clean_M_score"]) > 1e-8 else 0 for r in all_results])
    lat_ms = np.mean([r["coarse"]["B_latents_only"]["M_score"] / r["clean_M_score"] if abs(r["clean_M_score"]) > 1e-8 else 0 for r in all_results])
    err_ms = np.mean([r["coarse"]["C_error_only"]["M_score"] / r["clean_M_score"] if abs(r["clean_M_score"]) > 1e-8 else 0 for r in all_results])
    lines.append(f"Full reconstruction recovers {full_ms:.1%} of clean M_score (sanity check).")
    lines.append(f"Latents-only recovers {lat_ms:.1%}; error-only recovers {err_ms:.1%}.")
    if err_ms > 0.8:
        lines.append("Error-only preserves most of the anchor metric. The layer-8 SAE vocabulary is not causally sufficient (Outcome C).")
    elif lat_ms > 0.8:
        lines.append("Latents-only recovers most of the anchor metric. The SAE provides a strong causal basis.")
    else:
        lines.append("Neither latents-only nor error-only fully explains the metric. The anchor behavior depends on both SAE-captured and SAE-missed components.")

    k50_vals = [r["k_thresholds"]["k_50"] for r in all_results if r["k_thresholds"]["k_50"] is not None]
    if k50_vals and np.median(k50_vals) <= 20:
        lines.append(f"A small number of latent-token pairs (median k_50 = {np.median(k50_vals):.0f}) suffices for 50% recovery, suggesting compact causal support (Outcome A direction).")
    elif k50_vals:
        lines.append(f"Median k_50 = {np.median(k50_vals):.0f}, suggesting distributed causal support (Outcome B direction).")

    out_path = REPORT_DIR / f"{PREFIX}.md"
    with open(out_path, "w") as f:
        f.write("\n".join(lines))
    print(f"Report: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--max-proteins", type=int, default=50)
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Load sequences
    print("Loading sequences...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    print(f"  {len(all_seqs)} total proteins")

    # Select proteins
    print("Selecting proteins...")
    audit_csv = REPORT_DIR / "anchor_behavior_audit.csv"
    proteins = select_proteins(audit_csv, all_seqs, n=args.max_proteins)

    # Load model + SAE
    print(f"Loading ESM2 on {args.device}...")
    esm_model, tokenizer = load_model(args.device)
    print("Loading layer-8 SAE...")
    sae = load_sae_prot(LAYER=SAE_LAYER, device=args.device)
    for p in sae.parameters():
        p.requires_grad_(False)

    weights = extract_head_weights(esm_model, TARGET_LAYER, TARGET_HEAD, args.device)

    # Run analysis
    all_results = []
    all_top_pairs = []
    all_sufficiency = []
    t_start = time.time()

    for i, prot in enumerate(proteins):
        pid = prot["protein"]
        seq = all_seqs[pid]
        anchor_idx = prot["anchor_idx"]
        if anchor_idx < 0 or anchor_idx >= len(seq):
            print(f"  [{i+1}] {pid}: anchor_idx={anchor_idx} out of range, skipping")
            continue

        print(f"[{i+1}/{len(proteins)}] {pid} ({len(seq)} res, anchor={anchor_idx})")
        t0 = time.time()

        try:
            result = analyze_protein(pid, seq, anchor_idx, esm_model, tokenizer, sae, weights, args.device)
        except Exception as e:
            print(f"  ERROR: {e}")
            gc.collect()
            torch.cuda.empty_cache()
            continue

        all_results.append(result)
        for p in result["top20"]:
            p["protein"] = pid
            all_top_pairs.append(p)
        for s in result["sufficiency"]:
            s["protein"] = pid
            all_sufficiency.append(s)

        c = result["coarse"]
        dt = time.time() - t0
        print(f"  M={result['clean_M_score']:.3f} gap={result['ie_gap']:.5f} full={c['A_full']['M_score']:.3f} lat={c['B_latents_only']['M_score']:.3f} err={c['C_error_only']['M_score']:.3f} ({dt:.1f}s)")

    total_time = time.time() - t_start
    print(f"\nDone: {len(all_results)} proteins in {total_time:.0f}s")

    if not all_results:
        print("No results to report.")
        return

    # --- Save CSVs ---
    # Per-protein
    csv_path = REPORT_DIR / f"{PREFIX}_per_protein.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protein", "n_res", "anchor_idx", "n_active",
                     "clean_M_score", "clean_M_attn", "clean_score_rank", "clean_attn_rank",
                     "ie_gap", "ie_mass_anchor", "ie_mass_near",
                     "full_M_score_frac", "lat_M_score_frac", "err_M_score_frac",
                     "k_50", "k_80", "k_90"])
        for r in all_results:
            cms = r["clean_M_score"]
            w.writerow([
                r["protein"], r["n_res"], r["anchor_idx"], r["n_active"],
                f"{cms:.6f}", f"{r['clean_M_attn']:.6f}", r["clean_score_rank"], r["clean_attn_rank"],
                f"{r['ie_gap']:.8f}", f"{r['ie_mass_anchor']:.4f}", f"{r['ie_mass_near']:.4f}",
                f"{r['coarse']['A_full']['M_score']/cms:.4f}" if abs(cms) > 1e-8 else "NA",
                f"{r['coarse']['B_latents_only']['M_score']/cms:.4f}" if abs(cms) > 1e-8 else "NA",
                f"{r['coarse']['C_error_only']['M_score']/cms:.4f}" if abs(cms) > 1e-8 else "NA",
                r["k_thresholds"]["k_50"], r["k_thresholds"]["k_80"], r["k_thresholds"]["k_90"],
            ])
    print(f"Per-protein CSV: {csv_path}")

    # Top pairs
    csv_path = REPORT_DIR / f"{PREFIX}_top_pairs.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protein", "rank", "token_pos", "latent_idx", "ie_value", "activation", "is_anchor_token"])
        for p in all_top_pairs:
            w.writerow([p["protein"], p["rank"], p["token_pos"], p["latent_idx"],
                        f"{p['ie_value']:.6f}", f"{p['activation']:.6f}", p["is_anchor_token"]])
    print(f"Top pairs CSV: {csv_path}")

    # Sufficiency
    csv_path = REPORT_DIR / f"{PREFIX}_sufficiency.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["protein", "k", "actual_k", "M_score", "M_score_frac", "M_attn", "M_attn_frac", "score_rank", "attn_rank"])
        for s in all_sufficiency:
            w.writerow([s["protein"], s["k"], s["actual_k"],
                        f"{s['M_score']:.6f}", f"{s['M_score_frac']:.4f}",
                        f"{s['M_attn']:.6f}", f"{s['M_attn_frac']:.4f}",
                        s["score_rank"], s["attn_rank"]])
    print(f"Sufficiency CSV: {csv_path}")

    # Plots and report
    make_plots(all_results)
    write_report(all_results)
    print("All outputs written.")


if __name__ == "__main__":
    main()
