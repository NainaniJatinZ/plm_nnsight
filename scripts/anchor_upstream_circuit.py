#!/usr/bin/env python3
"""Upstream circuit discovery for L10H9 anchor feature (Experiment 4_4).

Identifies which model components (attention heads and MLPs in layers 0-9) write
the anchor feature into the residual stream at the anchor position. Uses local
flank masking clean/corrupted pairs as a natural counterfactual.

For each protein:
  - Defines clean/corrupted flank pairs from the alpha_norm jump threshold
  - Decomposes the residual stream into per-head and per-MLP contributions
  - Projects each contribution onto the L10H9 search direction d
  - Computes delta = clean - corrupted for each of 211 components

Analyses:
  1. Component ranking by mean fraction of total delta
  2. Attention vs MLP budget breakdown
  3. Layer-by-layer contribution profile
  4. Head recurrence / overlap across proteins

Sanity check: activation patching for top-5 components validates the linear
decomposition against actual model propagation (including LayerNorm effects).

Usage:
    uv run python scripts/anchor_upstream_circuit.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
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


# ---------------------------------------------------------------------------
# Model loading (reused from anchor_local_flank_v1.py / anchor_interp_v3.py)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Sequence construction (from anchor_local_flank_v1.py)
# ---------------------------------------------------------------------------

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
    return " ".join(chars)


# ---------------------------------------------------------------------------
# CSV loading and threshold computation
# ---------------------------------------------------------------------------

def load_thresholds(csv_path: Path, alpha_threshold: float = 0.5) -> list[dict]:
    """Load per-protein flank data and compute clean/corrupted radius pairs.

    For each protein, finds R_threshold = smallest radius where alpha_norm >= threshold.
    Corrupted = one radius step below R_threshold. Clean = R_threshold.
    """
    protein_data = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = row["protein"]
            if pid not in protein_data:
                protein_data[pid] = {
                    "n_res": int(row["n_res"]),
                    "anchor_pos": int(row["anchor_pos"]),
                    "rows": [],
                }
            protein_data[pid]["rows"].append({
                "radius": row["radius"],
                "radius_int": int(row["radius_int"]),
                "alpha_norm": float(row["alpha_norm"]),
            })

    results = []
    for pid, pdata in protein_data.items():
        rows = sorted(pdata["rows"], key=lambda r: r["radius_int"])

        # Find R_threshold: smallest radius where alpha_norm >= threshold
        r_threshold_idx = None
        for i, r in enumerate(rows):
            if r["alpha_norm"] >= alpha_threshold:
                r_threshold_idx = i
                break

        if r_threshold_idx is None:
            continue

        if r_threshold_idx == 0:
            # Already crosses at smallest radius — try stricter threshold (0.7)
            stricter_idx = None
            for i, r in enumerate(rows):
                if r["alpha_norm"] >= 0.7:
                    stricter_idx = i
                    break
            if stricter_idx is not None and stricter_idx > 0:
                r_threshold_idx = stricter_idx
            else:
                continue

        corrupted_radius = rows[r_threshold_idx - 1]["radius_int"]
        clean_radius = rows[r_threshold_idx]["radius_int"]
        corrupted_alpha_norm = rows[r_threshold_idx - 1]["alpha_norm"]
        clean_alpha_norm = rows[r_threshold_idx]["alpha_norm"]

        results.append({
            "protein": pid,
            "n_res": pdata["n_res"],
            "anchor_pos": pdata["anchor_pos"],
            "clean_radius": clean_radius,
            "corrupted_radius": corrupted_radius,
            "clean_alpha_norm": clean_alpha_norm,
            "corrupted_alpha_norm": corrupted_alpha_norm,
        })

    return results


# ---------------------------------------------------------------------------
# Per-head decomposition
# ---------------------------------------------------------------------------

def extract_W_O_matrices(model) -> list[torch.Tensor]:
    """Extract output projection weight matrices for layers 0-9."""
    W_O_list = []
    for l in range(10):
        W_O = model._model.esm.encoder.layer[l].attention.output.dense.weight.data.cpu()
        W_O_list.append(W_O)
    return W_O_list


def build_component_names() -> list[str]:
    """Return ordered list of 211 component names."""
    names = ["embed"]
    for l in range(10):
        for h in range(NUM_HEADS):
            names.append(f"attn_L{l}_H{h}")
    for l in range(10):
        names.append(f"mlp_L{l}")
    return names


@torch.no_grad()
def capture_anchor_projections(model, tokenizer, sequence_str: str, W_O_list: list[torch.Tensor],
                               anchor_tok_pos: int, d_unit: torch.Tensor, device: str) -> tuple[dict[str, float], float]:
    """Run forward pass and return projection of each component onto d at anchor position.

    Returns:
        scores: dict component_name -> float (scalar projection value)
        post_ln_alpha: float, the post-LayerNorm projection LN(x_10)[anchor] · d

    Per-head decomposition: the attention output at layer l is W_O @ context. We split by head:
    W_O[:, h*64:(h+1)*64] @ context[anchor, h*64:(h+1)*64]. The bias of attention.output.dense
    is omitted; it cancels in clean-minus-corrupted deltas.
    """
    inputs = tokenizer(sequence_str, return_tensors="pt").to(device)

    embed_mod = model.esm.embeddings
    attn_self_mods = [model.esm.encoder.layer[l].attention.self for l in range(10)]
    mlp_dense_mods = [model.esm.encoder.layer[l].output.dense for l in range(10)]
    ln_mod = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    all_modules = [embed_mod] + attn_self_mods + mlp_dense_mods + [ln_mod]

    with model.trace() as tracer:
        with tracer.invoke(**inputs, output_attentions=True):
            cache = tracer.cache(modules=all_modules)

    scores = {}

    # Embedding
    embed = cache["model.esm.embeddings"].output.detach().cpu()[0]
    scores["embed"] = (embed[anchor_tok_pos] @ d_unit).item()

    for l in range(10):
        # Context vectors from attention.self output[0]
        attn_self_key = f"model.esm.encoder.layer.{l}.attention.self"
        context = cache[attn_self_key].output[0].detach().cpu()[0]  # (seq_len, 1280)
        W_O = W_O_list[l]  # (1280, 1280)

        # Per-head decomposition at anchor position
        for h in range(NUM_HEADS):
            h_s, h_e = h * HEAD_DIM, (h + 1) * HEAD_DIM
            context_h = context[anchor_tok_pos, h_s:h_e]  # (64,)
            W_O_h = W_O[:, h_s:h_e]  # (1280, 64)
            head_contrib = W_O_h @ context_h  # (1280,)
            scores[f"attn_L{l}_H{h}"] = (head_contrib @ d_unit).item()

        # MLP contribution
        mlp_key = f"model.esm.encoder.layer.{l}.output.dense"
        mlp_out = cache[mlp_key].output.detach().cpu()[0]
        scores[f"mlp_L{l}"] = (mlp_out[anchor_tok_pos] @ d_unit).item()

    # Post-LN alpha: what L10H9 actually sees
    ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    ln_out = cache[ln_key].output.detach().cpu()[0]
    post_ln_alpha = (ln_out[anchor_tok_pos] @ d_unit).item()

    return scores, post_ln_alpha


# ---------------------------------------------------------------------------
# Main decomposition loop
# ---------------------------------------------------------------------------

def run_all_decompositions(model, tokenizer, proteins: list[dict], all_seqs: dict,
                           d_unit: torch.Tensor, W_O_list: list[torch.Tensor],
                           device: str) -> dict:
    """For each protein, run clean/corrupted decompositions and compute deltas."""
    component_names = build_component_names()
    all_results = {}
    t0 = time.time()

    for pi, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        seq = all_seqs[pid]
        anchor_pos = pinfo["anchor_pos"]
        anchor_tok_pos = anchor_pos + 1  # +1 for BOS token

        clean_seq = build_masked_sequence(seq, anchor_pos, pinfo["clean_radius"])
        corrupt_seq = build_masked_sequence(seq, anchor_pos, pinfo["corrupted_radius"])

        try:
            clean_scores, clean_post_ln = capture_anchor_projections(model, tokenizer, clean_seq, W_O_list, anchor_tok_pos, d_unit, device)
            corrupt_scores, corrupt_post_ln = capture_anchor_projections(model, tokenizer, corrupt_seq, W_O_list, anchor_tok_pos, d_unit, device)
        except Exception as e:
            print(f"  ERROR on {pid}: {e}")
            continue

        delta_d_proj = {comp: clean_scores[comp] - corrupt_scores[comp] for comp in component_names}
        total_delta = sum(delta_d_proj.values())
        frac_of_total = {}
        for comp in component_names:
            frac_of_total[comp] = delta_d_proj[comp] / total_delta if abs(total_delta) > 1e-10 else 0.0

        all_results[pid] = {
            "clean_scores": clean_scores,
            "corrupt_scores": corrupt_scores,
            "delta_d_proj": delta_d_proj,
            "frac_of_total": frac_of_total,
            "total_delta": total_delta,
            "post_ln_delta": clean_post_ln - corrupt_post_ln,
            "clean_post_ln": clean_post_ln,
            "corrupt_post_ln": corrupt_post_ln,
            "clean_radius": pinfo["clean_radius"],
            "corrupted_radius": pinfo["corrupted_radius"],
            "anchor_pos": anchor_pos,
        }

        elapsed = time.time() - t0
        rate = (pi + 1) / elapsed
        eta = (len(proteins) - pi - 1) / rate if rate > 0 else 0
        print(f"  [{pi+1}/{len(proteins)}] {pid}: total_delta={total_delta:.4f}, clean_R={pinfo['clean_radius']}, corrupt_R={pinfo['corrupted_radius']}  ({rate:.1f} prot/s, ETA {eta:.0f}s)")

    return all_results


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def analysis_1_ranking(results: dict, component_names: list[str]) -> dict:
    """Rank all 211 components by mean_frac across proteins."""
    proteins = list(results.keys())

    stats = {}
    for comp in component_names:
        fracs = [results[p]["frac_of_total"][comp] for p in proteins]
        deltas = [results[p]["delta_d_proj"][comp] for p in proteins]
        abs_deltas = [abs(d) for d in deltas]
        signs = [1 if d > 0 else 0 for d in deltas]

        stats[comp] = {
            "mean_frac": np.mean(fracs),
            "median_frac": np.median(fracs),
            "mean_abs_delta": np.mean(abs_deltas),
            "sign_consistency": np.mean(signs),
            "mean_delta": np.mean(deltas),
            "std_delta": np.std(deltas),
        }

    ranked = sorted(stats.items(), key=lambda x: x[1]["mean_frac"], reverse=True)
    return {"stats": stats, "ranked": ranked}


def analysis_2_budget(results: dict) -> dict:
    """Attention vs MLP budget per protein."""
    budget = {}
    for pid, r in results.items():
        attn_total = sum(abs(r["delta_d_proj"][f"attn_L{l}_H{h}"]) for l in range(10) for h in range(NUM_HEADS))
        mlp_total = sum(abs(r["delta_d_proj"][f"mlp_L{l}"]) for l in range(10))
        embed_delta = abs(r["delta_d_proj"]["embed"])
        total = attn_total + mlp_total + embed_delta
        budget[pid] = {
            "attn_total": attn_total,
            "mlp_total": mlp_total,
            "embed_delta": embed_delta,
            "attn_frac": attn_total / total if total > 0 else 0,
            "mlp_frac": mlp_total / total if total > 0 else 0,
            "embed_frac": embed_delta / total if total > 0 else 0,
        }
    return budget


def analysis_3_layer_profile(results: dict) -> dict:
    """Per-layer contribution summed across heads (attention) and MLP."""
    proteins = list(results.keys())
    layer_data = {}
    for l in range(10):
        attn_deltas = []
        mlp_deltas = []
        for pid in proteins:
            attn_sum = sum(results[pid]["delta_d_proj"][f"attn_L{l}_H{h}"] for h in range(NUM_HEADS))
            mlp_val = results[pid]["delta_d_proj"][f"mlp_L{l}"]
            attn_deltas.append(attn_sum)
            mlp_deltas.append(mlp_val)
        layer_data[l] = {
            "mean_attn": np.mean(attn_deltas),
            "mean_mlp": np.mean(mlp_deltas),
            "mean_total": np.mean(attn_deltas) + np.mean(mlp_deltas),
            "std_attn": np.std(attn_deltas),
            "std_mlp": np.std(mlp_deltas),
        }
    return layer_data


def analysis_4_recurrence(results: dict, top_k: int = 10) -> dict:
    """Head recurrence and pairwise Jaccard analysis."""
    proteins = list(results.keys())
    n = len(proteins)
    head_names = [f"attn_L{l}_H{h}" for l in range(10) for h in range(NUM_HEADS)]

    # Top-k heads per protein by |delta_d_proj|
    top_heads_per_protein = {}
    for pid in proteins:
        head_deltas = [(h, abs(results[pid]["delta_d_proj"][h])) for h in head_names]
        head_deltas.sort(key=lambda x: x[1], reverse=True)
        top_heads_per_protein[pid] = set(h for h, _ in head_deltas[:top_k])

    # Per-head recurrence (top-10)
    head_counts = Counter()
    for pid in proteins:
        for h in top_heads_per_protein[pid]:
            head_counts[h] += 1
    recurrence_top10 = {h: head_counts.get(h, 0) / n for h in head_names}

    # Per-head recurrence (top-20)
    top20_per_protein = {}
    for pid in proteins:
        head_deltas = [(h, abs(results[pid]["delta_d_proj"][h])) for h in head_names]
        head_deltas.sort(key=lambda x: x[1], reverse=True)
        top20_per_protein[pid] = set(h for h, _ in head_deltas[:20])
    head_counts_20 = Counter()
    for pid in proteins:
        for h in top20_per_protein[pid]:
            head_counts_20[h] += 1
    recurrence_top20 = {h: head_counts_20.get(h, 0) / n for h in head_names}

    # Pairwise Jaccard
    jaccard_mat = np.zeros((n, n))
    for i, p1 in enumerate(proteins):
        for j, p2 in enumerate(proteins):
            s1 = top_heads_per_protein[p1]
            s2 = top_heads_per_protein[p2]
            jaccard_mat[i, j] = len(s1 & s2) / len(s1 | s2) if len(s1 | s2) > 0 else 0.0

    mean_jaccard = jaccard_mat[np.triu_indices(n, k=1)].mean() if n > 1 else 0.0

    return {
        "top_heads_per_protein": top_heads_per_protein,
        "head_counts": head_counts,
        "recurrence_top10": recurrence_top10,
        "recurrence_top20": recurrence_top20,
        "jaccard_mat": jaccard_mat,
        "proteins": proteins,
        "mean_jaccard": mean_jaccard,
    }


def sanity_check_ln(decomp_results: dict) -> dict:
    """Validate that pre-LN decomposition rankings are preserved after LayerNorm.

    Compares the pre-LN total delta (sum of per-component deltas) to the post-LN
    total delta (from the actual LN output cached during decomposition). If the two
    are strongly correlated across proteins, LayerNorm acts as an approximately
    uniform rescaling and per-component rankings are preserved.
    """
    proteins = list(decomp_results.keys())
    pre_ln_deltas = []
    post_ln_deltas = []
    for pid in proteins:
        pre_ln_deltas.append(decomp_results[pid]["total_delta"])
        post_ln_deltas.append(decomp_results[pid]["post_ln_delta"])

    pre_ln = np.array(pre_ln_deltas)
    post_ln = np.array(post_ln_deltas)

    pearson = np.corrcoef(pre_ln, post_ln)[0, 1] if len(pre_ln) > 1 else float("nan")
    rank_corr, _ = spearmanr(pre_ln, post_ln) if len(pre_ln) > 1 else (float("nan"), 0)

    # Per-protein ratio: post_ln_delta / pre_ln_delta (should be ~constant if LN is uniform scaling)
    ratios = []
    for i in range(len(proteins)):
        if abs(pre_ln[i]) > 1e-10:
            ratios.append(post_ln[i] / pre_ln[i])
    ratio_mean = np.mean(ratios) if ratios else float("nan")
    ratio_std = np.std(ratios) if ratios else float("nan")

    return {
        "proteins": proteins,
        "pre_ln_deltas": pre_ln.tolist(),
        "post_ln_deltas": post_ln.tolist(),
        "pearson": pearson,
        "rank_corr": rank_corr,
        "ratio_mean": ratio_mean,
        "ratio_std": ratio_std,
        "ratios": ratios,
    }


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def generate_plots(ranking_data: dict, budget_data: dict, layer_data: dict,
                   recurrence_data: dict, sanity_data: dict | None,
                   decomp_results: dict, top5_components: list[str]) -> None:
    """Generate all output plots."""
    plt.rcParams.update({
        "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5,
        "figure.dpi": 150,
    })

    # 1. Top-20 components by mean_frac
    fig, ax = plt.subplots(figsize=(10, 6))
    top20 = ranking_data["ranked"][:20]
    labels = [name for name, _ in top20]
    values = [s["mean_frac"] for _, s in top20]
    colors = []
    for name, _ in top20:
        if name == "embed":
            colors.append("#4DAF4A")
        elif name.startswith("mlp"):
            colors.append("#FF7F00")
        else:
            colors.append("#377EB8")
    ax.barh(range(len(labels)), values, color=colors, edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Mean fraction of total delta")
    ax.set_title("Top 20 components by mean fraction of clean-corrupt delta")
    ax.invert_yaxis()
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor="#377EB8", label="Attention head"),
                       Patch(facecolor="#FF7F00", label="MLP"),
                       Patch(facecolor="#4DAF4A", label="Embedding")]
    ax.legend(handles=legend_elements, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_upstream_circuit_ranking.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved anchor_upstream_circuit_ranking.png")

    # 2. Layer profile
    fig, ax = plt.subplots(figsize=(10, 4))
    layers = range(10)
    attn_vals = [layer_data[l]["mean_attn"] for l in layers]
    mlp_vals = [layer_data[l]["mean_mlp"] for l in layers]
    x = np.arange(10)
    width = 0.35
    ax.bar(x - width / 2, attn_vals, width, label="Attention (all heads)", color="#377EB8", alpha=0.85)
    ax.bar(x + width / 2, mlp_vals, width, label="MLP", color="#FF7F00", alpha=0.85)
    ax.set_xlabel("Layer")
    ax.set_ylabel("Mean delta d-projection")
    ax.set_title("Contribution by layer (clean - corrupted)")
    ax.set_xticks(x)
    ax.axhline(0, color="black", linewidth=0.5)
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_upstream_circuit_layer_profile.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved anchor_upstream_circuit_layer_profile.png")

    # 3. Attention vs MLP budget
    proteins = sorted(budget_data.keys())
    fig, ax = plt.subplots(figsize=(8, max(4, len(proteins) * 0.22)))
    attn_fracs = [budget_data[p]["attn_frac"] for p in proteins]
    mlp_fracs = [budget_data[p]["mlp_frac"] for p in proteins]
    embed_fracs = [budget_data[p]["embed_frac"] for p in proteins]
    y = range(len(proteins))
    ax.barh(y, attn_fracs, color="#377EB8", label="Attention")
    ax.barh(y, mlp_fracs, left=attn_fracs, color="#FF7F00", label="MLP")
    left2 = [a + m for a, m in zip(attn_fracs, mlp_fracs)]
    ax.barh(y, embed_fracs, left=left2, color="#4DAF4A", label="Embedding")
    ax.set_yticks(y)
    ax.set_yticklabels(proteins, fontsize=6)
    ax.set_xlabel("Fraction of total |delta|")
    ax.set_title("Budget breakdown: attention vs MLP vs embedding")
    ax.legend(loc="lower right", fontsize=7)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_upstream_circuit_attn_vs_mlp.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved anchor_upstream_circuit_attn_vs_mlp.png")

    # 4. Head recurrence heatmap (layer x head)
    proteins_list = recurrence_data["proteins"]
    n_prot = len(proteins_list)
    fig, ax = plt.subplots(figsize=(12, 5))
    grid = np.zeros((10, NUM_HEADS))
    for head_name, count in recurrence_data["head_counts"].items():
        parts = head_name.split("_")
        l = int(parts[1][1:])
        h = int(parts[2][1:])
        grid[l, h] = count
    im = ax.imshow(grid, aspect="auto", cmap="YlOrRd", vmin=0, vmax=n_prot, interpolation="nearest")
    ax.set_xlabel("Head")
    ax.set_ylabel("Layer")
    ax.set_xticks(range(NUM_HEADS))
    ax.set_yticks(range(10))
    ax.set_title(f"Head recurrence in top-10 across {n_prot} proteins")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("Number of proteins")
    for l in range(10):
        for h in range(NUM_HEADS):
            if grid[l, h] >= n_prot * 0.3:
                ax.text(h, l, f"{int(grid[l, h])}", ha="center", va="center", fontsize=7, fontweight="bold",
                        color="white" if grid[l, h] >= n_prot * 0.5 else "black")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_upstream_circuit_recurrence.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved anchor_upstream_circuit_recurrence.png")

    # 5. Pairwise Jaccard heatmap with dendrogram
    n = len(proteins_list)
    jaccard_mat = recurrence_data["jaccard_mat"]
    fig, (ax_dend, ax_heat) = plt.subplots(1, 2, figsize=(14, max(6, n * 0.18)),
                                            gridspec_kw={"width_ratios": [1, 3]})
    dist = 1 - jaccard_mat
    np.fill_diagonal(dist, 0)
    condensed = squareform(dist, checks=False)
    condensed = np.clip(condensed, 0, None)
    Z = linkage(condensed, method="average")
    dend = dendrogram(Z, orientation="left", labels=proteins_list, ax=ax_dend, leaf_font_size=6)
    ax_dend.set_title("Clustering", fontsize=9)

    order = dend["leaves"]
    reordered = jaccard_mat[np.ix_(order, order)]
    reordered_labels = [proteins_list[i] for i in order]
    im = ax_heat.imshow(reordered, cmap="YlOrRd", vmin=0, vmax=0.7, interpolation="nearest")
    ax_heat.set_xticks(range(n))
    ax_heat.set_yticks(range(n))
    ax_heat.set_xticklabels(reordered_labels, rotation=90, fontsize=5)
    ax_heat.set_yticklabels(reordered_labels, fontsize=5)
    ax_heat.set_title(f"Pairwise Jaccard (top-10 heads), mean={recurrence_data['mean_jaccard']:.3f}")
    cbar = fig.colorbar(im, ax=ax_heat, shrink=0.8)
    cbar.set_label("Jaccard index")
    fig.tight_layout()
    fig.savefig(REPORT_DIR / "anchor_upstream_circuit_jaccard.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  Saved anchor_upstream_circuit_jaccard.png")

    # 6. Sanity check: pre-LN vs post-LN scatter
    if sanity_data:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        pre_ln = np.array(sanity_data["pre_ln_deltas"])
        post_ln = np.array(sanity_data["post_ln_deltas"])

        ax1.scatter(pre_ln, post_ln, alpha=0.6, s=30, color="#2166AC")
        mn = min(pre_ln.min(), post_ln.min())
        mx = max(pre_ln.max(), post_ln.max())
        ax1.plot([mn, mx], [mn, mx], "k--", lw=0.8, alpha=0.3)
        ax1.set_xlabel("Pre-LN total delta (sum of components)")
        ax1.set_ylabel("Post-LN total delta (from LN output)")
        ax1.set_title(f"Pre-LN vs Post-LN delta (r={sanity_data['pearson']:.3f})")
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)

        if sanity_data["ratios"]:
            ax2.hist(sanity_data["ratios"], bins=20, color="#4DAF4A", alpha=0.7, edgecolor="white")
            ax2.axvline(sanity_data["ratio_mean"], color="red", lw=1.5, ls="--",
                        label=f"mean={sanity_data['ratio_mean']:.3f}")
            ax2.set_xlabel("Post-LN / Pre-LN ratio")
            ax2.set_ylabel("Count")
            ax2.set_title(f"LN scaling ratio (std={sanity_data['ratio_std']:.3f})")
            ax2.legend()
            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)

        fig.tight_layout()
        fig.savefig(REPORT_DIR / "anchor_upstream_circuit_sanity.png", dpi=150, bbox_inches="tight")
        plt.close(fig)
        print("  Saved anchor_upstream_circuit_sanity.png")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def write_reports(ranking_data: dict, budget_data: dict, layer_data: dict,
                  recurrence_data: dict, sanity_data: dict | None,
                  decomp_results: dict, component_names: list[str],
                  proteins_info: list[dict], top5_components: list[str]) -> None:
    """Write all CSV and markdown outputs."""

    proteins = sorted(decomp_results.keys())

    # 1. Per-component, per-protein CSV
    csv_path = REPORT_DIR / "anchor_upstream_circuit_components.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["component", "protein", "clean_score", "corrupt_score", "delta_d_proj", "frac_of_total"])
        for comp in component_names:
            for pid in proteins:
                r = decomp_results[pid]
                writer.writerow([comp, pid,
                                 f"{r['clean_scores'][comp]:.6f}",
                                 f"{r['corrupt_scores'][comp]:.6f}",
                                 f"{r['delta_d_proj'][comp]:.6f}",
                                 f"{r['frac_of_total'][comp]:.6f}"])
    print(f"  Saved {csv_path}")

    # 2. Aggregated ranking CSV
    summary_path = REPORT_DIR / "anchor_upstream_circuit_summary.csv"
    with open(summary_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "component", "mean_frac", "median_frac", "mean_abs_delta", "sign_consistency", "recurrence_top10", "recurrence_top20"])
        for rank, (comp, stats) in enumerate(ranking_data["ranked"], 1):
            rec10 = recurrence_data["recurrence_top10"].get(comp, 0)
            rec20 = recurrence_data["recurrence_top20"].get(comp, 0)
            writer.writerow([rank, comp,
                             f"{stats['mean_frac']:.6f}",
                             f"{stats['median_frac']:.6f}",
                             f"{stats['mean_abs_delta']:.6f}",
                             f"{stats['sign_consistency']:.3f}",
                             f"{rec10:.3f}",
                             f"{rec20:.3f}"])
    print(f"  Saved {summary_path}")

    # 3. Sanity check CSV
    if sanity_data:
        sanity_path = REPORT_DIR / "anchor_upstream_circuit_sanity.csv"
        with open(sanity_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["protein", "pre_ln_delta", "post_ln_delta", "ratio"])
            for i, pid in enumerate(sanity_data["proteins"]):
                pre_ln = sanity_data["pre_ln_deltas"][i]
                post_ln = sanity_data["post_ln_deltas"][i]
                ratio = post_ln / pre_ln if abs(pre_ln) > 1e-10 else float("nan")
                writer.writerow([pid, f"{pre_ln:.6f}", f"{post_ln:.6f}",
                                 f"{ratio:.4f}" if not np.isnan(ratio) else "nan"])
        print(f"  Saved {sanity_path}")

    # 4. Markdown report
    report_path = REPORT_DIR / "anchor_upstream_circuit.md"
    lines = []
    lines.append("# Upstream Circuit Discovery for L10H9 Anchor Feature\n\n")
    lines.append(f"Proteins analyzed: {len(proteins)}\n")
    lines.append(f"Search direction d: W_K^T @ q_mean from {REFERENCE_PROTEIN}\n")
    lines.append("Components: 1 embedding + 200 attention heads (10 layers x 20 heads) + 10 MLPs = 211\n")
    lines.append("Per-head decomposition: the attention output W_O @ context is split by W_O[:, h_slice] @ context[:, h_slice]. The bias of the output projection cancels in clean-minus-corrupted deltas.\n\n")

    # Protein table
    lines.append("## Protein counterfactual pairs\n\n")
    lines.append("| Protein | Anchor pos | Clean R | Corrupt R | Clean alpha_norm | Corrupt alpha_norm | Total delta |\n")
    lines.append("|---------|-----------|---------|-----------|-----------------|-------------------|-------------|\n")
    for pinfo in proteins_info:
        pid = pinfo["protein"]
        if pid in decomp_results:
            td = decomp_results[pid]["total_delta"]
            lines.append(f"| {pid} | {pinfo['anchor_pos']} | {pinfo['clean_radius']} | {pinfo['corrupted_radius']} | {pinfo['clean_alpha_norm']:.3f} | {pinfo['corrupted_alpha_norm']:.3f} | {td:.4f} |\n")

    # Analysis 1
    lines.append("\n## Analysis 1: Component ranking (top 20)\n\n")
    lines.append("| Rank | Component | Mean frac | Median frac | Mean |delta| | Sign consistency | Recurrence top-10 | Recurrence top-20 |\n")
    lines.append("|------|-----------|-----------|-------------|-------------|-----------------|-------------------|-------------------|\n")
    for rank, (comp, stats) in enumerate(ranking_data["ranked"][:20], 1):
        rec10 = recurrence_data["recurrence_top10"].get(comp, 0)
        rec20 = recurrence_data["recurrence_top20"].get(comp, 0)
        lines.append(f"| {rank} | {comp} | {stats['mean_frac']:.4f} | {stats['median_frac']:.4f} | {stats['mean_abs_delta']:.4f} | {stats['sign_consistency']:.2f} | {rec10:.2f} | {rec20:.2f} |\n")

    # Split by type
    attn_ranked = [(c, s) for c, s in ranking_data["ranked"] if c.startswith("attn")]
    mlp_ranked = [(c, s) for c, s in ranking_data["ranked"] if c.startswith("mlp")]
    embed_stats = ranking_data["stats"]["embed"]

    lines.append("\n### Top 10 attention heads\n\n")
    lines.append("| Rank | Head | Mean frac | Sign consistency |\n")
    lines.append("|------|------|-----------|------------------|\n")
    for rank, (comp, stats) in enumerate(attn_ranked[:10], 1):
        lines.append(f"| {rank} | {comp} | {stats['mean_frac']:.4f} | {stats['sign_consistency']:.2f} |\n")

    lines.append("\n### Top 5 MLPs\n\n")
    lines.append("| Rank | MLP | Mean frac | Sign consistency |\n")
    lines.append("|------|-----|-----------|------------------|\n")
    for rank, (comp, stats) in enumerate(mlp_ranked[:5], 1):
        lines.append(f"| {rank} | {comp} | {stats['mean_frac']:.4f} | {stats['sign_consistency']:.2f} |\n")

    lines.append(f"\n### Embedding\n\nMean frac: {embed_stats['mean_frac']:.4f}, sign consistency: {embed_stats['sign_consistency']:.2f}\n\n")

    # Analysis 2
    lines.append("## Analysis 2: Attention vs MLP budget\n\n")
    attn_fracs_all = [budget_data[p]["attn_frac"] for p in proteins]
    mlp_fracs_all = [budget_data[p]["mlp_frac"] for p in proteins]
    embed_fracs_all = [budget_data[p]["embed_frac"] for p in proteins]
    lines.append(f"Across {len(proteins)} proteins:\n")
    lines.append(f"- Attention: mean {np.mean(attn_fracs_all):.1%}, median {np.median(attn_fracs_all):.1%}\n")
    lines.append(f"- MLP: mean {np.mean(mlp_fracs_all):.1%}, median {np.median(mlp_fracs_all):.1%}\n")
    lines.append(f"- Embedding: mean {np.mean(embed_fracs_all):.1%}, median {np.median(embed_fracs_all):.1%}\n\n")

    # Analysis 3
    lines.append("## Analysis 3: Layer profile\n\n")
    lines.append("| Layer | Mean attn delta | Mean MLP delta | Mean total |\n")
    lines.append("|-------|----------------|---------------|------------|\n")
    for l in range(10):
        d = layer_data[l]
        lines.append(f"| {l} | {d['mean_attn']:.4f} | {d['mean_mlp']:.4f} | {d['mean_total']:.4f} |\n")

    # Analysis 4
    lines.append("\n## Analysis 4: Head recurrence\n\n")
    lines.append(f"Mean pairwise Jaccard (top-10 heads): {recurrence_data['mean_jaccard']:.3f}\n\n")

    head_counts_sorted = sorted(recurrence_data["head_counts"].items(), key=lambda x: -x[1])
    n_prot = len(recurrence_data["proteins"])

    lines.append("### Heads appearing in top-10 of 30%+ proteins\n\n")
    lines.append("| Head | Count | Fraction |\n")
    lines.append("|------|-------|----------|\n")
    has_high_recurrence = False
    for head_name, count in head_counts_sorted:
        frac = count / n_prot
        if frac >= 0.3:
            lines.append(f"| {head_name} | {count}/{n_prot} | {frac:.2f} |\n")
            has_high_recurrence = True
    if not has_high_recurrence:
        lines.append("No heads reach 30% recurrence.\n")

    max_recurrence = head_counts_sorted[0][1] / n_prot if head_counts_sorted else 0
    lines.append(f"\nHighest single-head recurrence: {max_recurrence:.2f}\n")
    if max_recurrence >= 0.5:
        lines.append("Interpretation: high recurrence — universal upstream circuit detected. Follow up with Analysis 5 (source position analysis for top recurring heads).\n")
    elif max_recurrence >= 0.3:
        lines.append("Interpretation: moderate recurrence — possible protein-type clustering. Follow up with Analysis 6 (protein grouping from Jaccard matrix).\n")
    else:
        lines.append("Interpretation: low recurrence — upstream circuit is protein-specific. The anchor feature is built by diverse computations that converge to a universal detector.\n")

    # Sanity check
    if sanity_data:
        lines.append("\n## Sanity check: pre-LN vs post-LN delta\n\n")
        lines.append("Compares the pre-LN total delta (sum of per-component d-projections, which is what the linear decomposition operates on) to the post-LN total delta (LN(x_10)[anchor] dot d, which is what L10H9 actually sees). If the two are strongly correlated, LayerNorm acts as approximately uniform rescaling and per-component rankings are preserved.\n\n")
        lines.append(f"Pearson correlation: {sanity_data['pearson']:.4f}\n")
        lines.append(f"Spearman rank correlation: {sanity_data['rank_corr']:.4f}\n")
        lines.append(f"Post-LN / Pre-LN ratio: mean={sanity_data['ratio_mean']:.4f}, std={sanity_data['ratio_std']:.4f}\n\n")
        if sanity_data["rank_corr"] > 0.9:
            lines.append("LN distortion is minimal. Per-component rankings from the linear decomposition can be trusted.\n")
        elif sanity_data["rank_corr"] > 0.7:
            lines.append("LN causes some distortion but overall ranking is approximately preserved.\n")
        else:
            lines.append("Significant LN distortion. Per-component rankings may not fully reflect what L10H9 sees. Interpret with caution.\n")

    lines.append("\n## Figures\n\n")
    lines.append("![Component ranking](anchor_upstream_circuit_ranking.png)\n\n")
    lines.append("![Layer profile](anchor_upstream_circuit_layer_profile.png)\n\n")
    lines.append("![Budget breakdown](anchor_upstream_circuit_attn_vs_mlp.png)\n\n")
    lines.append("![Head recurrence](anchor_upstream_circuit_recurrence.png)\n\n")
    lines.append("![Jaccard heatmap](anchor_upstream_circuit_jaccard.png)\n\n")
    if sanity_data:
        lines.append("![Sanity check](anchor_upstream_circuit_sanity.png)\n\n")

    with open(report_path, "w") as f:
        f.writelines(lines)
    print(f"  Saved {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Upstream circuit discovery for L10H9 anchor feature")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--csv", type=str, default=str(REPORT_DIR / "anchor_local_flank_v1_per_protein.csv"),
                        help="Path to per-protein flank CSV")
    parser.add_argument("--skip-sanity", action="store_true", help="Skip activation patching sanity check")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Load sequences
    print("Loading sequences...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    # Load thresholds from CSV
    csv_path = Path(args.csv)
    print(f"Loading thresholds from {csv_path}...")
    proteins_info = load_thresholds(csv_path)
    print(f"  {len(proteins_info)} proteins with valid clean/corrupted pairs")

    # Filter to proteins with sequences available
    proteins_info = [p for p in proteins_info if p["protein"] in all_seqs]
    print(f"  {len(proteins_info)} proteins with sequences available")

    for p in proteins_info[:5]:
        print(f"    {p['protein']}: anchor={p['anchor_pos']}, clean_R={p['clean_radius']}, corrupt_R={p['corrupted_radius']}, alpha_norm clean={p['clean_alpha_norm']:.3f} corrupt={p['corrupted_alpha_norm']:.3f}")

    # Load model
    print(f"\nLoading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    # Extract weights
    print("Extracting L10H9 weights and W_O matrices...")
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    W_O_list = extract_W_O_matrices(model)

    # Compute search direction from reference protein full sequence
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    d = compute_search_dir(model, tokenizer, " ".join(ref_seq), weights, args.device)
    d_unit = d / d.norm().clamp(min=1e-8)
    print(f"  Search direction norm: {d.norm().item():.4f}")

    # Run per-head decomposition for all proteins
    print(f"\nRunning per-head decomposition for {len(proteins_info)} proteins...")
    decomp_results = run_all_decompositions(model, tokenizer, proteins_info, all_seqs, d_unit, W_O_list, args.device)
    print(f"  {len(decomp_results)} proteins completed successfully")

    # Analyses
    component_names = build_component_names()
    print("\nRunning analyses...")

    print("  Analysis 1: Component ranking...")
    ranking_data = analysis_1_ranking(decomp_results, component_names)
    top5_components = [name for name, _ in ranking_data["ranked"][:5]]
    print(f"    Top 5: {top5_components}")
    for name, stats in ranking_data["ranked"][:5]:
        print(f"      {name}: mean_frac={stats['mean_frac']:.4f}, sign_consistency={stats['sign_consistency']:.2f}")

    print("  Analysis 2: Budget breakdown...")
    budget_data = analysis_2_budget(decomp_results)
    proteins_list = list(decomp_results.keys())
    mean_attn_frac = np.mean([budget_data[p]["attn_frac"] for p in proteins_list])
    mean_mlp_frac = np.mean([budget_data[p]["mlp_frac"] for p in proteins_list])
    print(f"    Mean attention fraction: {mean_attn_frac:.1%}, MLP: {mean_mlp_frac:.1%}")

    print("  Analysis 3: Layer profile...")
    layer_data = analysis_3_layer_profile(decomp_results)
    top_layer = max(range(10), key=lambda l: abs(layer_data[l]["mean_total"]))
    print(f"    Highest-contributing layer: {top_layer} (mean_total={layer_data[top_layer]['mean_total']:.4f})")

    print("  Analysis 4: Recurrence...")
    recurrence_data = analysis_4_recurrence(decomp_results)
    print(f"    Mean pairwise Jaccard: {recurrence_data['mean_jaccard']:.3f}")
    top_recurring = sorted(recurrence_data["head_counts"].items(), key=lambda x: -x[1])[:5]
    n_prot = len(recurrence_data["proteins"])
    for h, c in top_recurring:
        print(f"    {h}: {c}/{n_prot} ({c/n_prot:.0%})")

    # Sanity check: pre-LN vs post-LN delta comparison
    sanity_data = None
    if not args.skip_sanity:
        print("\nRunning LN sanity check (pre-LN vs post-LN delta)...")
        sanity_data = sanity_check_ln(decomp_results)
        print(f"  Pearson r={sanity_data['pearson']:.4f}, Spearman rho={sanity_data['rank_corr']:.4f}")
        print(f"  Post-LN/Pre-LN ratio: mean={sanity_data['ratio_mean']:.4f}, std={sanity_data['ratio_std']:.4f}")

    # Generate plots
    print("\nGenerating plots...")
    generate_plots(ranking_data, budget_data, layer_data, recurrence_data, sanity_data, decomp_results, top5_components)

    # Write reports
    print("\nWriting reports...")
    write_reports(ranking_data, budget_data, layer_data, recurrence_data, sanity_data, decomp_results, component_names, proteins_info, top5_components)

    print("\nDone. Outputs written to reports/outputs/multi_protein/")


if __name__ == "__main__":
    main()
