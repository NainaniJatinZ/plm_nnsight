#!/usr/bin/env python3
"""Universality audit for L10H9 anchor search direction.

Two sharp checks:
  1. Cross-protein cosine similarity of q_mean, W_Q^T @ q_mean, and W_K^T @ q_mean
     in both masked-task and full-sequence contexts.
  2. Cross-protein generalization: use protein A's search direction to rank residues
     in protein B. Measure anchor rank and top-k hit rate across all pairs.

Usage:
    uv run python scripts/anchor_universality_audit.py --device cuda
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
TOP_K = 3

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


def get_layer_ln_activations(model, tokenizer, sequence: str, device: str) -> torch.Tensor:
    """Get LayerNorm activations at L10 for all residue positions. Returns (n_residues, hidden_dim) on CPU."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    return x_ln[1:-1]  # strip BOS/EOS


def compute_directions(x_ln: torch.Tensor, weights: dict) -> dict:
    """From LayerNorm activations, compute q_mean (unit), W_Q^T @ q_mean, and W_K^T @ q_mean.

    Returns dict with 1D torch tensors.
    """
    W_Q = weights["W_Q_hd"]
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]

    q_all = x_ln @ W_Q.T + b_Q  # (n_res, head_dim)
    q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)

    # W_Q^T @ q_mean: the query-side direction projected back into hidden space
    wq_q_mean = W_Q.T @ q_mean_norm  # (hidden_dim,)
    wq_q_mean_norm = wq_q_mean / wq_q_mean.norm().clamp(min=1e-8)

    # W_K^T @ q_mean: the key-side search direction (what v3 uses)
    wk_q_mean = W_K.T @ q_mean_norm  # (hidden_dim,)
    wk_q_mean_norm = wk_q_mean / wk_q_mean.norm().clamp(min=1e-8)

    return {
        "q_mean": q_mean_norm,           # (head_dim,) — the mean query direction
        "wq_q_mean": wq_q_mean_norm,     # (hidden_dim,) — query-side in residual stream
        "wk_q_mean": wk_q_mean_norm,     # (hidden_dim,) — key-side search direction
    }


def cosine_sim(a: torch.Tensor, b: torch.Tensor) -> float:
    return float(torch.dot(a, b) / (a.norm() * b.norm()).clamp(min=1e-8))


def capture_projection_scores(model, tokenizer, sequence: str, search_dir_unit: torch.Tensor, device: str) -> np.ndarray:
    x_ln = get_layer_ln_activations(model, tokenizer, sequence, device)
    return (x_ln @ search_dir_unit).numpy()


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

    proteins = list(ANCHOR_POSITIONS.keys())

    # =====================================================================
    # CHECK 1: Cross-protein cosine similarity of directions
    # =====================================================================
    print("\n=== CHECK 1: Cross-protein direction similarity ===\n")

    # Compute directions for each protein in both contexts
    directions = {}  # protein -> {"masked": {...}, "full": {...}}
    for protein in proteins:
        seq = seqs[protein]
        config = protein_configs[protein]
        masked_seq = build_clean_sequence(seq, config)

        print(f"  {protein}...")
        x_ln_masked = get_layer_ln_activations(model, tokenizer, masked_seq, args.device)
        x_ln_full = get_layer_ln_activations(model, tokenizer, seq, args.device)

        dirs_masked = compute_directions(x_ln_masked, weights)
        dirs_full = compute_directions(x_ln_full, weights)

        directions[protein] = {"masked": dirs_masked, "full": dirs_full}

    # Compute pairwise cosine similarity matrices for each direction type and context
    n = len(proteins)
    dir_types = ["q_mean", "wq_q_mean", "wk_q_mean"]
    contexts = ["masked", "full"]

    sim_matrices = {}
    for ctx in contexts:
        for dt in dir_types:
            mat = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    mat[i, j] = cosine_sim(directions[proteins[i]][ctx][dt], directions[proteins[j]][ctx][dt])
            sim_matrices[(ctx, dt)] = mat

    # Print summary statistics
    print("\nCross-protein cosine similarity (off-diagonal mean +/- std):\n")
    print(f"{'Context':<10} {'Direction':<15} {'Mean':>8} {'Std':>8} {'Min':>8} {'Max':>8}")
    print("-" * 60)
    summary_rows = []
    for ctx in contexts:
        for dt in dir_types:
            mat = sim_matrices[(ctx, dt)]
            mask = ~np.eye(n, dtype=bool)
            off_diag = mat[mask]
            row = {
                "context": ctx,
                "direction": dt,
                "mean": float(np.mean(off_diag)),
                "std": float(np.std(off_diag)),
                "min": float(np.min(off_diag)),
                "max": float(np.max(off_diag)),
            }
            summary_rows.append(row)
            print(f"{ctx:<10} {dt:<15} {row['mean']:>8.4f} {row['std']:>8.4f} {row['min']:>8.4f} {row['max']:>8.4f}")

    # =====================================================================
    # CHECK 2: Cross-protein generalization of search direction
    # =====================================================================
    print("\n\n=== CHECK 2: Cross-protein search direction generalization ===\n")

    # For each protein, extract its W_K^T @ q_mean direction (both masked and full)
    # Then use that direction to rank residues in every other protein
    # Measure: anchor rank, top-k hit rate

    # Pre-compute projection scores for all proteins under all source directions
    # Key: (source_protein, context, target_protein) -> scores array

    # First get all search directions (W_K^T @ q_mean, not unit-normalized yet — we normalize here)
    search_dirs = {}
    for protein in proteins:
        for ctx in contexts:
            d = directions[protein][ctx]["wk_q_mean"]
            search_dirs[(protein, ctx)] = d

    # Now compute projection scores and anchor ranks
    print("Computing cross-protein projection scores...")
    results = []

    for ctx in contexts:
        print(f"\n  Context: {ctx}")
        for src_protein in proteins:
            src_dir = search_dirs[(src_protein, ctx)]
            for tgt_protein in proteins:
                tgt_seq = seqs[tgt_protein]
                scores = capture_projection_scores(model, tokenizer, tgt_seq, src_dir, args.device)
                anchor_pos = ANCHOR_POSITIONS[tgt_protein]
                n_res = len(scores)

                if anchor_pos >= n_res:
                    continue

                anchor_score = scores[anchor_pos]
                anchor_rank = int((scores > anchor_score).sum()) + 1
                anchor_percentile = 1.0 - anchor_rank / n_res

                # Top-k hit: is the known anchor in the top-k by this direction?
                top_k_idx = np.argsort(scores)[-TOP_K:]
                top_k_hit = 1 if anchor_pos in top_k_idx else 0

                # Top-1 hit
                top_1_hit = 1 if np.argmax(scores) == anchor_pos else 0

                is_self = src_protein == tgt_protein

                results.append({
                    "context": ctx,
                    "source": src_protein,
                    "target": tgt_protein,
                    "is_self": is_self,
                    "anchor_pos": anchor_pos,
                    "anchor_rank": anchor_rank,
                    "anchor_percentile": round(anchor_percentile, 4),
                    "n_residues": n_res,
                    "top_1_hit": top_1_hit,
                    "top_k_hit": top_k_hit,
                })

        # Print summary for this context
        self_results = [r for r in results if r["context"] == ctx and r["is_self"]]
        cross_results = [r for r in results if r["context"] == ctx and not r["is_self"]]

        print(f"\n  Self-protein ({ctx}):")
        print(f"    Mean anchor rank: {np.mean([r['anchor_rank'] for r in self_results]):.1f}")
        print(f"    Mean anchor percentile: {np.mean([r['anchor_percentile'] for r in self_results]):.4f}")
        print(f"    Top-1 hit rate: {np.mean([r['top_1_hit'] for r in self_results]):.3f}")
        print(f"    Top-{TOP_K} hit rate: {np.mean([r['top_k_hit'] for r in self_results]):.3f}")

        print(f"\n  Cross-protein ({ctx}):")
        print(f"    Mean anchor rank: {np.mean([r['anchor_rank'] for r in cross_results]):.1f}")
        print(f"    Mean anchor percentile: {np.mean([r['anchor_percentile'] for r in cross_results]):.4f}")
        print(f"    Top-1 hit rate: {np.mean([r['top_1_hit'] for r in cross_results]):.3f}")
        print(f"    Top-{TOP_K} hit rate: {np.mean([r['top_k_hit'] for r in cross_results]):.3f}")

    # Leave-one-out summary: for each target, average across all non-self source directions
    print("\n\nLeave-one-out per-target summary (masked context):")
    print(f"{'Target':<10} {'Self rank':>10} {'LOO mean rank':>15} {'LOO top-1':>10} {'LOO top-k':>10}")
    print("-" * 60)
    loo_rows = []
    for tgt in proteins:
        self_r = [r for r in results if r["context"] == "masked" and r["target"] == tgt and r["is_self"]]
        cross_r = [r for r in results if r["context"] == "masked" and r["target"] == tgt and not r["is_self"]]
        if not self_r or not cross_r:
            continue
        self_rank = self_r[0]["anchor_rank"]
        loo_mean_rank = np.mean([r["anchor_rank"] for r in cross_r])
        loo_top1 = np.mean([r["top_1_hit"] for r in cross_r])
        loo_topk = np.mean([r["top_k_hit"] for r in cross_r])
        print(f"{tgt:<10} {self_rank:>10d} {loo_mean_rank:>15.1f} {loo_top1:>10.3f} {loo_topk:>10.3f}")
        loo_rows.append({
            "target": tgt,
            "self_rank": self_rank,
            "loo_mean_rank": loo_mean_rank,
            "loo_top1": loo_top1,
            "loo_topk": loo_topk,
        })

    # =====================================================================
    # Plots
    # =====================================================================
    print("\nGenerating plots...")

    # Plot 1: Heatmaps of cosine similarity matrices (6 panels: 2 contexts x 3 directions)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    short_names = [p[:5] for p in proteins]
    for row_idx, ctx in enumerate(contexts):
        for col_idx, dt in enumerate(dir_types):
            ax = axes[row_idx, col_idx]
            mat = sim_matrices[(ctx, dt)]
            im = ax.imshow(mat, vmin=-1, vmax=1, cmap="RdBu_r")
            ax.set_xticks(range(n))
            ax.set_xticklabels(short_names, rotation=90, fontsize=6)
            ax.set_yticks(range(n))
            ax.set_yticklabels(short_names, fontsize=6)
            off_diag = mat[~np.eye(n, dtype=bool)]
            ax.set_title(f"{ctx} / {dt}\nmean={np.mean(off_diag):.3f}", fontsize=9)
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.suptitle("Check 1: Cross-protein cosine similarity of L10H9 directions", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out1 = REPORT_DIR / "anchor_universality_audit_cosine_sim.png"
    fig.savefig(out1, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out1}")

    # Plot 2: Cross-protein generalization heatmap (anchor percentile, source x target, masked context)
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    for ax_idx, ctx in enumerate(contexts):
        ax = axes[ax_idx]
        mat = np.full((n, n), np.nan)
        for r in results:
            if r["context"] != ctx:
                continue
            si = proteins.index(r["source"])
            ti = proteins.index(r["target"])
            mat[si, ti] = r["anchor_percentile"]
        im = ax.imshow(mat, vmin=0, vmax=1, cmap="YlOrRd")
        ax.set_xticks(range(n))
        ax.set_xticklabels(short_names, rotation=90, fontsize=6)
        ax.set_yticks(range(n))
        ax.set_yticklabels(short_names, fontsize=6)
        ax.set_xlabel("Target protein")
        ax.set_ylabel("Source protein (direction donor)")
        off_diag = mat[~np.eye(n, dtype=bool)]
        ax.set_title(f"{ctx}: anchor percentile\nmean={np.nanmean(off_diag):.3f}", fontsize=9)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.suptitle("Check 2: Cross-protein anchor ranking (higher = anchor ranks better)", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out2 = REPORT_DIR / "anchor_universality_audit_generalization.png"
    fig.savefig(out2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out2}")

    # Plot 3: Bar chart comparing self vs cross-protein hit rates
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax_idx, ctx in enumerate(contexts):
        ax = axes[ax_idx]
        self_r = [r for r in results if r["context"] == ctx and r["is_self"]]
        cross_r = [r for r in results if r["context"] == ctx and not r["is_self"]]
        metrics = ["top_1_hit", "top_k_hit"]
        labels = ["Top-1 hit", f"Top-{TOP_K} hit"]
        self_vals = [np.mean([r[m] for r in self_r]) for m in metrics]
        cross_vals = [np.mean([r[m] for r in cross_r]) for m in metrics]
        x = np.arange(len(metrics))
        ax.bar(x - 0.15, self_vals, 0.3, label="Self-protein", color="#61afef")
        ax.bar(x + 0.15, cross_vals, 0.3, label="Cross-protein", color="#e06c75")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.set_ylabel("Hit rate")
        ax.set_title(f"Context: {ctx}")
        ax.legend()
        ax.set_ylim(0, 1.05)
        for i, (sv, cv) in enumerate(zip(self_vals, cross_vals)):
            ax.text(i - 0.15, sv + 0.02, f"{sv:.2f}", ha="center", fontsize=8)
            ax.text(i + 0.15, cv + 0.02, f"{cv:.2f}", ha="center", fontsize=8)
    plt.suptitle("Check 2: Self vs cross-protein anchor retrieval", fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    out3 = REPORT_DIR / "anchor_universality_audit_hit_rates.png"
    fig.savefig(out3, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out3}")

    # =====================================================================
    # Write report
    # =====================================================================
    print("\nWriting report...")
    report = []
    report.append("# L10H9 Universality Audit\n\n")
    report.append("Two checks: (1) are the query-side and key-side directions universal across proteins? (2) does a search direction from one protein generalize to rank anchors in others?\n\n")

    report.append("## Check 1: Cross-protein cosine similarity\n\n")
    report.append("For each protein, we compute the per-protein mean query direction (q_mean), the query-side projection back to residual stream (W_Q^T @ q_mean), and the key-side search direction (W_K^T @ q_mean) under both masked-task and full-sequence contexts.\n\n")
    report.append("| Context | Direction | Mean cos | Std | Min | Max |\n")
    report.append("|---------|-----------|----------|-----|-----|-----|\n")
    for row in summary_rows:
        report.append(f"| {row['context']} | {row['direction']} | {row['mean']:.4f} | {row['std']:.4f} | {row['min']:.4f} | {row['max']:.4f} |\n")
    report.append("\n")
    report.append("![Cosine similarity heatmaps](anchor_universality_audit_cosine_sim.png)\n\n")

    report.append("## Check 2: Cross-protein search direction generalization\n\n")
    report.append("For each (source, target) protein pair, we use the source protein's W_K^T @ q_mean direction to rank residues in the target protein and check whether the known anchor is retrieved.\n\n")

    for ctx in contexts:
        self_r = [r for r in results if r["context"] == ctx and r["is_self"]]
        cross_r = [r for r in results if r["context"] == ctx and not r["is_self"]]
        report.append(f"### Context: {ctx}\n\n")
        report.append(f"Self-protein: mean anchor rank = {np.mean([r['anchor_rank'] for r in self_r]):.1f}, top-1 hit = {np.mean([r['top_1_hit'] for r in self_r]):.3f}, top-{TOP_K} hit = {np.mean([r['top_k_hit'] for r in self_r]):.3f}\n\n")
        report.append(f"Cross-protein: mean anchor rank = {np.mean([r['anchor_rank'] for r in cross_r]):.1f}, top-1 hit = {np.mean([r['top_1_hit'] for r in cross_r]):.3f}, top-{TOP_K} hit = {np.mean([r['top_k_hit'] for r in cross_r]):.3f}\n\n")

    report.append("### Leave-one-out per-target summary (masked context)\n\n")
    report.append("| Target | Self rank | LOO mean rank | LOO top-1 | LOO top-k |\n")
    report.append("|--------|-----------|---------------|-----------|----------|\n")
    for row in loo_rows:
        report.append(f"| {row['target']} | {row['self_rank']} | {row['loo_mean_rank']:.1f} | {row['loo_top1']:.3f} | {row['loo_topk']:.3f} |\n")
    report.append("\n")
    report.append("![Generalization heatmap](anchor_universality_audit_generalization.png)\n\n")
    report.append("![Hit rates](anchor_universality_audit_hit_rates.png)\n\n")

    out_report = REPORT_DIR / "anchor_universality_audit.md"
    with open(out_report, "w") as f:
        f.writelines(report)
    print(f"  Saved: {out_report}")

    # Save CSV
    csv_path = REPORT_DIR / "anchor_universality_audit_results.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["context", "source", "target", "is_self", "anchor_pos", "anchor_rank", "anchor_percentile", "n_residues", "top_1_hit", "top_k_hit"])
        writer.writeheader()
        for r in results:
            writer.writerow(r)
    print(f"  Saved: {csv_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
