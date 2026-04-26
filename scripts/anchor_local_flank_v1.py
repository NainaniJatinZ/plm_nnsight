#!/usr/bin/env python3
"""Anchor local flank reconstruction analysis.

Tests whether the anchor signal at L10H9 can be reconstructed from local
sequence context around the anchor, by masking everything except an
anchor-centered window and gradually expanding the visible flank.

Selects the top 50 most confident anchor proteins from the behavior audit
(by top3_mass), then for each protein and each flank radius R:
  - replaces residues outside [anchor-R, anchor+R] with <mask>
  - runs a traced forward pass caching L10 LayerNorm activations and L10H9 attention
  - computes: projection onto d, pre-softmax key scores, attention mass, top-k overlap

Usage:
    uv run python scripts/anchor_local_flank_v1.py --device cuda
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
from scipy import optimize as sp_opt

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LEGACY_REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
EXPERIMENT_ROOT = ROOT / "reports" / "out2" / "suppressing_anchors"
DEFAULT_OUTPUT_DIR = EXPERIMENT_ROOT / "local_flank_v1"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
REFERENCE_PROTEIN = "2B61A"
TOP_N = 50
MASK_TOKEN = "<mask>"

RADII_SCHEDULE = [5, 6, 7, 8, 10, 12, 15, 20, 30, 40, 60, 80, 120]
# "full" is handled separately


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
    q_all = x_ln @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    return weights["W_K_hd"].T @ q_mean_norm


def select_top_proteins(audit_csv: Path, all_seqs: dict, n: int) -> list[dict]:
    """Select top N proteins by top3_mass from the behavior audit CSV."""
    rows = []
    with open(audit_csv) as f:
        reader = csv.DictReader(f)
        for r in reader:
            pid = r["protein"]
            if pid not in all_seqs:
                continue
            rows.append({
                "protein": pid,
                "top3_mass": float(r["top3_mass"]),
                "anchor_pos": int(r["top_key_idx"]),
                "n_res": int(r["n_res"]),
            })
    rows.sort(key=lambda x: x["top3_mass"], reverse=True)
    return rows[:n]


def build_masked_sequence(sequence: str, anchor_pos: int, radius: int) -> str:
    """Replace residues outside [anchor-R, anchor+R] with <mask> tokens."""
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = []
    for i in range(n):
        if lo <= i <= hi:
            chars.append(sequence[i])
        else:
            chars.append(MASK_TOKEN)
    # Join with spaces so tokenizer treats each as a separate token
    # ESM tokenizer expects space-separated single characters or <mask>
    return " ".join(chars)


@torch.no_grad()
def run_single(model, tokenizer, sequence_str: str, device: str):
    """Run a single forward pass, return L10 LN activations and L10H9 attention."""
    inputs = tokenizer(sequence_str, return_tensors="pt").to(device)
    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=[attn_module, ln_module])
    attn_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    attn_all = cache[attn_key].output[1].detach().cpu()[0]  # (H, L, L)
    A = attn_all[TARGET_HEAD, 1:-1, 1:-1]  # (n_res, n_res) query x key
    x_ln = cache[ln_key].output.detach().cpu()[0, 1:-1]  # (n_res, 1280)
    return x_ln, A


@torch.no_grad()
def compute_metrics(x_ln, A, anchor_pos: int, d_unit: torch.Tensor, weights: dict):
    """Compute all four metric families at the original anchor position."""
    n_res = x_ln.shape[0]

    # Metric 1: projection onto universal direction
    proj_scores = (x_ln @ d_unit.cpu()).numpy()
    alpha = float(proj_scores[anchor_pos])
    proj_rank = int((proj_scores > proj_scores[anchor_pos]).sum())  # 0 = top

    # Metric 2: pre-softmax key score at anchor
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]
    b_K = weights["b_K_d"]
    q_all = x_ln @ W_Q.T + b_Q  # (n_res, d_head)
    k_all = x_ln @ W_K.T + b_K  # (n_res, d_head)
    k_anchor = k_all[anchor_pos]  # (d_head,)
    # mean over queries of (q_q . k_anchor) / sqrt(d_head)
    scores_at_anchor = (q_all @ k_anchor) / (HEAD_DIM ** 0.5)  # (n_res,)
    score = float(scores_at_anchor.mean())
    # rank: how many keys have higher mean incoming score than anchor?
    mean_key_scores = torch.zeros(n_res)
    for ki in range(n_res):
        mean_key_scores[ki] = (q_all @ k_all[ki]).mean() / (HEAD_DIM ** 0.5)
    score_rank = int((mean_key_scores > mean_key_scores[anchor_pos]).sum())

    # Metric 3: attention mass at anchor key
    mean_key_attn = A.mean(dim=0).numpy()  # (n_res,)
    attn_mass = float(mean_key_attn[anchor_pos])
    attn_rank = int((mean_key_attn > mean_key_attn[anchor_pos]).sum())

    # Metric 4: top-k overlap with full
    top_keys = np.argsort(-mean_key_attn)
    return {
        "alpha": alpha,
        "proj_rank": proj_rank,
        "score": score,
        "score_rank": score_rank,
        "attn_mass": attn_mass,
        "attn_rank": attn_rank,
        "top1_key": int(top_keys[0]),
        "top3_keys": top_keys[:3].tolist(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--top-n", type=int, default=TOP_N)
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument(
        "--audit-csv",
        type=str,
        default=str(LEGACY_REPORT_DIR / "anchor_behavior_audit.csv"),
        help="Input audit CSV used to select the anchor proteins.",
    )
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Loading sequences...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    audit_csv = Path(args.audit_csv)
    print(f"Selecting top {args.top_n} proteins from {audit_csv}...")
    proteins = select_top_proteins(audit_csv, all_seqs, args.top_n)
    print(f"  Selected {len(proteins)} proteins")
    for p in proteins[:5]:
        print(f"    {p['protein']}: anchor={p['anchor_pos']}, n_res={p['n_res']}, top3_mass={p['top3_mass']:.4f}")

    print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    d = compute_search_dir(model, tokenizer, ref_seq, weights, args.device)
    d_unit = (d / d.norm().clamp(min=1e-8)).to(args.device)

    # Process each protein
    all_rows = []
    t0 = time.time()

    for pi, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = all_seqs[pid]
        n_res = len(seq)

        # Determine radii schedule for this protein (cap by length, add "full")
        radii = [r for r in RADII_SCHEDULE if r < n_res // 2] + [n_res]  # last entry = full

        # First run the full sequence to get baseline values
        full_seq_str = " ".join(seq)
        try:
            x_ln_full, A_full = run_single(model, tokenizer, full_seq_str, args.device)
        except Exception as e:
            print(f"  ERROR on {pid} (full): {e}")
            continue
        full_metrics = compute_metrics(x_ln_full, A_full, anchor, d_unit, weights)
        full_top3 = set(full_metrics["top3_keys"])

        for ri, R in enumerate(radii):
            is_full = (R == n_res)
            label = "full" if is_full else str(R)

            if is_full:
                metrics = full_metrics
            else:
                masked_seq = build_masked_sequence(seq, anchor, R)
                try:
                    x_ln_R, A_R = run_single(model, tokenizer, masked_seq, args.device)
                except Exception as e:
                    print(f"  ERROR on {pid} R={R}: {e}")
                    continue
                metrics = compute_metrics(x_ln_R, A_R, anchor, d_unit, weights)

            # Normalize by full
            alpha_norm = metrics["alpha"] / full_metrics["alpha"] if abs(full_metrics["alpha"]) > 1e-8 else 0.0
            score_norm = metrics["score"] / full_metrics["score"] if abs(full_metrics["score"]) > 1e-8 else 0.0
            attn_norm = metrics["attn_mass"] / full_metrics["attn_mass"] if abs(full_metrics["attn_mass"]) > 1e-8 else 0.0

            # Top-k overlap with full
            R_top3 = set(metrics["top3_keys"])
            top1_overlap = 1.0 if metrics["top1_key"] == full_metrics["top1_key"] else 0.0
            top3_overlap = len(R_top3 & full_top3) / 3.0

            row = {
                "protein": pid,
                "n_res": n_res,
                "anchor_pos": anchor,
                "radius": label,
                "radius_int": R,
                "alpha": metrics["alpha"],
                "alpha_norm": alpha_norm,
                "proj_rank": metrics["proj_rank"],
                "score": metrics["score"],
                "score_norm": score_norm,
                "score_rank": metrics["score_rank"],
                "attn_mass": metrics["attn_mass"],
                "attn_norm": attn_norm,
                "attn_rank": metrics["attn_rank"],
                "top1_overlap": top1_overlap,
                "top3_overlap": top3_overlap,
            }
            all_rows.append(row)

        elapsed = time.time() - t0
        rate = (pi + 1) / elapsed
        eta = (len(proteins) - pi - 1) / rate
        print(f"  [{pi+1}/{len(proteins)}] {pid} ({n_res} res, anchor={anchor}): {len(radii)} radii done  ({rate:.2f} prot/s, ETA {eta:.0f}s)")

    elapsed = time.time() - t0
    print(f"\nProcessed {len(proteins)} proteins, {len(all_rows)} rows in {elapsed:.0f}s")

    # Save per-protein CSV
    csv_path = output_dir / "anchor_local_flank_v1_per_protein.csv"
    fields = ["protein", "n_res", "anchor_pos", "radius", "radius_int", "alpha", "alpha_norm", "proj_rank", "score", "score_norm", "score_rank", "attn_mass", "attn_norm", "attn_rank", "top1_overlap", "top3_overlap"]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"Saved: {csv_path}")

    # -----------------------------------------------------------------------
    # Analysis 2: threshold radii
    # -----------------------------------------------------------------------
    print("\nComputing threshold radii...")
    thresholds = [0.25, 0.50, 0.80, 0.90]
    threshold_rows = []
    unique_proteins = sorted(set(r["protein"] for r in all_rows))

    for pid in unique_proteins:
        prows = [r for r in all_rows if r["protein"] == pid]
        prows.sort(key=lambda x: x["radius_int"])
        n_res = prows[0]["n_res"]

        for metric_key, metric_norm_key in [("alpha", "alpha_norm"), ("score", "score_norm"), ("attn_mass", "attn_norm")]:
            trow = {"protein": pid, "n_res": n_res, "metric": metric_key}
            for thr in thresholds:
                found = None
                for r in prows:
                    if r[metric_norm_key] >= thr:
                        found = r["radius"]
                        break
                trow[f"R_{int(thr*100)}"] = found if found is not None else "never"
            threshold_rows.append(trow)

    thr_csv = output_dir / "anchor_local_flank_v1_thresholds.csv"
    thr_fields = ["protein", "n_res", "metric", "R_25", "R_50", "R_80", "R_90"]
    with open(thr_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=thr_fields)
        writer.writeheader()
        writer.writerows(threshold_rows)
    print(f"Saved: {thr_csv}")

    # -----------------------------------------------------------------------
    # Analysis 3: jump detection
    # -----------------------------------------------------------------------
    print("Detecting jumps...")
    jump_results = []
    for pid in unique_proteins:
        prows = sorted([r for r in all_rows if r["protein"] == pid], key=lambda x: x["radius_int"])
        for metric_norm_key in ["alpha_norm", "score_norm", "attn_norm"]:
            vals = [r[metric_norm_key] for r in prows]
            radii_vals = [r["radius_int"] for r in prows]
            deltas = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
            if len(deltas) == 0:
                continue
            max_jump_idx = int(np.argmax(deltas))
            max_jump = deltas[max_jump_idx]
            median_delta = float(np.median(deltas))
            jump_ratio = max_jump / median_delta if abs(median_delta) > 1e-8 else float("inf")
            jump_results.append({
                "protein": pid,
                "metric": metric_norm_key,
                "jump_radius": radii_vals[max_jump_idx],
                "jump_to_radius": radii_vals[max_jump_idx + 1],
                "max_jump": max_jump,
                "median_delta": median_delta,
                "jump_ratio": jump_ratio,
            })

    # -----------------------------------------------------------------------
    # Plots
    # -----------------------------------------------------------------------
    print("\nGenerating plots...")

    C_PROJ = "#2166AC"
    C_SCORE = "#B2182B"
    C_ATTN = "#4DAF4A"
    C_FILL = "#DDDDDD"

    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
        "figure.dpi": 200,
    })

    # Build aggregate curves
    # Group by radius, compute median/IQR for each normalized metric
    all_radii_set = sorted(set(r["radius_int"] for r in all_rows))

    agg = {R: {"alpha_norm": [], "score_norm": [], "attn_norm": [], "top1_overlap": [], "top3_overlap": []} for R in all_radii_set}
    for r in all_rows:
        R = r["radius_int"]
        for k in agg[R]:
            agg[R][k].append(r[k])

    # Only keep radii present in at least half the proteins
    min_count = len(unique_proteins) // 2
    plot_radii = [R for R in all_radii_set if len(agg[R]["alpha_norm"]) >= min_count]

    def get_stats(metric_key):
        medians, q25, q75 = [], [], []
        for R in plot_radii:
            vals = np.array(agg[R][metric_key])
            medians.append(np.median(vals))
            q25.append(np.percentile(vals, 25))
            q75.append(np.percentile(vals, 75))
        return np.array(medians), np.array(q25), np.array(q75)

    # Plot 1: Aggregate recovery curves
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))

    for ax, metric_key, color, title in [
        (axes[0], "alpha_norm", C_PROJ, "Projection onto d"),
        (axes[1], "score_norm", C_SCORE, "Pre-softmax key score"),
        (axes[2], "attn_norm", C_ATTN, "Attention mass"),
    ]:
        med, q25, q75 = get_stats(metric_key)
        ax.plot(plot_radii, med, color=color, lw=2, label="Median")
        ax.fill_between(plot_radii, q25, q75, color=color, alpha=0.15, label="IQR")
        ax.axhline(1.0, color="gray", ls=":", lw=0.7, alpha=0.5)
        ax.set_xlabel("Visible flank radius R")
        ax.set_ylabel("Normalized metric (fraction of full)")
        ax.set_title(title)
        ax.legend(loc="lower right")
        ax.set_ylim(-0.1, 1.3)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out1 = output_dir / "anchor_local_flank_v1_recovery.png"
    fig.savefig(out1, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out1}")

    # Plot 2: Per-protein recovery for subset of 8 representative proteins
    n_show = min(8, len(unique_proteins))
    show_prots = unique_proteins[:n_show]
    fig, axes = plt.subplots(2, 4, figsize=(14, 6))
    axes = axes.flatten()

    for idx, pid in enumerate(show_prots):
        ax = axes[idx]
        prows = sorted([r for r in all_rows if r["protein"] == pid], key=lambda x: x["radius_int"])
        rads = [r["radius_int"] for r in prows]
        ax.plot(rads, [r["alpha_norm"] for r in prows], color=C_PROJ, lw=1.5, label="proj")
        ax.plot(rads, [r["score_norm"] for r in prows], color=C_SCORE, lw=1.5, label="score")
        ax.plot(rads, [r["attn_norm"] for r in prows], color=C_ATTN, lw=1.5, label="attn")
        ax.axhline(1.0, color="gray", ls=":", lw=0.5)
        ax.set_title(f"{pid} (a={prows[0]['anchor_pos']})", fontsize=8)
        ax.set_ylim(-0.1, 1.3)
        if idx >= 4:
            ax.set_xlabel("Radius R")
        if idx % 4 == 0:
            ax.set_ylabel("Norm. metric")
        if idx == 0:
            ax.legend(fontsize=6)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out2 = output_dir / "anchor_local_flank_v1_per_protein.png"
    fig.savefig(out2, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out2}")

    # Plot 3: Threshold radii histograms
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, metric_key, title in [
        (axes[0], "alpha", "Projection"),
        (axes[1], "score", "Pre-softmax score"),
        (axes[2], "attn_mass", "Attention mass"),
    ]:
        trows = [t for t in threshold_rows if t["metric"] == metric_key]
        for thr_key, color, label in [("R_50", "#1b7837", "50%"), ("R_80", "#d73027", "80%")]:
            vals = [int(t[thr_key]) for t in trows if t[thr_key] not in ("never", "full")]
            if vals:
                ax.hist(vals, bins=15, alpha=0.5, color=color, label=f"{label} threshold", edgecolor="white")
        ax.set_xlabel("Threshold radius R")
        ax.set_ylabel("Count")
        ax.set_title(title)
        ax.legend(fontsize=7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out3 = output_dir / "anchor_local_flank_v1_thresholds.png"
    fig.savefig(out3, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out3}")

    # Plot 4: Jump radii histograms
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
    for ax, metric_key, title in [
        (axes[0], "alpha_norm", "Projection"),
        (axes[1], "score_norm", "Pre-softmax score"),
        (axes[2], "attn_norm", "Attention mass"),
    ]:
        jrows = [j for j in jump_results if j["metric"] == metric_key]
        jump_rads = [j["jump_radius"] for j in jrows]
        jump_ratios = [j["jump_ratio"] for j in jrows]
        if jump_rads:
            ax.hist(jump_rads, bins=15, color="#636363", alpha=0.7, edgecolor="white")
        median_ratio = float(np.median(jump_ratios)) if jump_ratios else 0
        ax.set_xlabel("Radius of largest jump")
        ax.set_ylabel("Count")
        ax.set_title(f"{title}\nmedian jump/med_delta = {median_ratio:.1f}x")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out4 = output_dir / "anchor_local_flank_v1_jumps.png"
    fig.savefig(out4, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out4}")

    # Plot 5: Top-k overlap recovery
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    med1, q25_1, q75_1 = get_stats("top1_overlap")
    med3, q25_3, q75_3 = get_stats("top3_overlap")
    ax1.plot(plot_radii, med1, color="#7570B3", lw=2, label="Median")
    ax1.fill_between(plot_radii, q25_1, q75_1, color="#7570B3", alpha=0.15)
    ax1.set_title("Top-1 overlap with full")
    ax1.set_xlabel("Radius R")
    ax1.set_ylabel("Overlap fraction")
    ax1.set_ylim(-0.05, 1.1)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ax2.plot(plot_radii, med3, color="#E7298A", lw=2, label="Median")
    ax2.fill_between(plot_radii, q25_3, q75_3, color="#E7298A", alpha=0.15)
    ax2.set_title("Top-3 overlap with full")
    ax2.set_xlabel("Radius R")
    ax2.set_ylabel("Overlap fraction")
    ax2.set_ylim(-0.05, 1.1)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    plt.tight_layout()
    out5 = output_dir / "anchor_local_flank_v1_topk.png"
    fig.savefig(out5, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out5}")

    # -----------------------------------------------------------------------
    # Write markdown report
    # -----------------------------------------------------------------------
    print("\nWriting report...")

    # Compute summary stats for report
    alpha_thrs = [t for t in threshold_rows if t["metric"] == "alpha"]
    score_thrs = [t for t in threshold_rows if t["metric"] == "score"]
    attn_thrs = [t for t in threshold_rows if t["metric"] == "attn_mass"]

    def median_threshold(trows, thr_key):
        vals = [int(t[thr_key]) for t in trows if t[thr_key] not in ("never", "full")]
        if not vals:
            return "N/A"
        return str(int(np.median(vals)))

    # Jump summary
    alpha_jumps = [j for j in jump_results if j["metric"] == "alpha_norm"]
    score_jumps = [j for j in jump_results if j["metric"] == "score_norm"]
    attn_jumps = [j for j in jump_results if j["metric"] == "attn_norm"]

    def jump_summary(jrows):
        if not jrows:
            return "N/A", "N/A"
        ratios = [j["jump_ratio"] for j in jrows]
        rads = [j["jump_radius"] for j in jrows]
        return f"{np.median(rads):.0f}", f"{np.median(ratios):.1f}"

    # Check recovery ordering: does projection recover before attention?
    # For each protein, compare R_50 for alpha vs attn_mass
    proj_before_attn = 0
    attn_before_proj = 0
    for pid in unique_proteins:
        at = [t for t in alpha_thrs if t["protein"] == pid]
        att = [t for t in attn_thrs if t["protein"] == pid]
        if at and att:
            a_r50 = at[0]["R_50"]
            att_r50 = att[0]["R_50"]
            if a_r50 not in ("never", "full") and att_r50 not in ("never", "full"):
                if int(a_r50) < int(att_r50):
                    proj_before_attn += 1
                elif int(att_r50) < int(a_r50):
                    attn_before_proj += 1

    report = []
    report.append("# Anchor Local Flank Reconstruction Analysis\n\n")
    report.append(f"Proteins analyzed: {len(unique_proteins)} (top {args.top_n} by top3_mass from behavior audit).\n")
    report.append(f"Search direction d: W_K^T @ q_mean from {REFERENCE_PROTEIN}.\n")
    report.append(f"Radii schedule: {', '.join(str(r) for r in RADII_SCHEDULE)}, full.\n\n")

    report.append("## Key findings\n\n")

    # Determine which outcome
    alpha_jump_med_rad, alpha_jump_ratio = jump_summary(alpha_jumps)
    score_jump_med_rad, score_jump_ratio = jump_summary(score_jumps)
    attn_jump_med_rad, attn_jump_ratio = jump_summary(attn_jumps)

    report.append(f"### Recovery shape\n\n")
    report.append(f"Median 50% recovery radius: projection R={median_threshold(alpha_thrs, 'R_50')}, pre-softmax score R={median_threshold(score_thrs, 'R_50')}, attention mass R={median_threshold(attn_thrs, 'R_50')}.\n\n")
    report.append(f"Median 80% recovery radius: projection R={median_threshold(alpha_thrs, 'R_80')}, pre-softmax score R={median_threshold(score_thrs, 'R_80')}, attention mass R={median_threshold(attn_thrs, 'R_80')}.\n\n")
    report.append(f"### Jump detection\n\n")
    report.append(f"Median largest-jump radius: projection R={alpha_jump_med_rad}, score R={score_jump_med_rad}, attention R={attn_jump_med_rad}.\n\n")
    report.append(f"Median jump/median-delta ratio: projection {alpha_jump_ratio}x, score {score_jump_ratio}x, attention {attn_jump_ratio}x.\n\n")

    report.append(f"### Metric ordering\n\n")
    report.append(f"Projection recovers before attention in {proj_before_attn}/{len(unique_proteins)} proteins; attention recovers before projection in {attn_before_proj}/{len(unique_proteins)}.\n\n")

    report.append("## Threshold radii summary (median across proteins)\n\n")
    report.append("| Metric | R_25 | R_50 | R_80 | R_90 |\n")
    report.append("|--------|------|------|------|------|\n")
    for metric_key, label in [("alpha", "Projection"), ("score", "Score"), ("attn_mass", "Attention")]:
        trows = [t for t in threshold_rows if t["metric"] == metric_key]
        report.append(f"| {label} | {median_threshold(trows, 'R_25')} | {median_threshold(trows, 'R_50')} | {median_threshold(trows, 'R_80')} | {median_threshold(trows, 'R_90')} |\n")
    report.append("\n")

    report.append("## Figures\n\n")
    report.append("![Aggregate recovery](anchor_local_flank_v1_recovery.png)\n\n")
    report.append("![Per-protein recovery](anchor_local_flank_v1_per_protein.png)\n\n")
    report.append("![Threshold radii](anchor_local_flank_v1_thresholds.png)\n\n")
    report.append("![Jump radii](anchor_local_flank_v1_jumps.png)\n\n")
    report.append("![Top-k overlap](anchor_local_flank_v1_topk.png)\n\n")

    out_report = output_dir / "anchor_local_flank_v1.md"
    with open(out_report, "w") as f:
        f.writelines(report)
    print(f"Saved: {out_report}")

    print("\nDone.")


if __name__ == "__main__":
    main()
