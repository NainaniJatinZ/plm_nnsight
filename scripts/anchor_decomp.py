#!/usr/bin/env python3
"""Anchor decomposition via SVD of per-head key projection matrices.

For anchor heads (heads that produce vertical-stripe attention patterns), this script
asks: what feature in the residual stream causes certain positions to become anchors?

Step 1: Compute k_j = W_K @ LN(x_j) + b_K for every position j. Check whether anchor
        positions have outsized key norms or project strongly onto top SVD components.
Step 2: Project anchor keys back to residual stream space to find the "anchor direction".
        Correlate with AA embeddings, SSE, and position projection profiles.
Step 3: Compare anchor directions across proteins. If anchor keys from different proteins
        align in key space, the model has learned a universal "relay position" feature.

Usage:
    uv run python scripts/anchor_decomp.py --device cuda
    uv run python scripts/anchor_decomp.py --heads 11,16 10,9 --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs"
CACHE_DIR = ROOT / "reports" / "cache"

NUM_LAYERS = 33
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280

DEFAULT_HEADS = [(11, 16), (10, 9), (14, 9)]


# ---------------------------------------------------------------------------
# Data loaders (adapted from anchor_interp.py)
# ---------------------------------------------------------------------------

def load_all_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(CONFIG_DIR / "common.json") as f:
        common_cfg = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_dict = json.load(f)
    return protein_configs, common_cfg, seqs, ss_dict


def load_summary_csv(protein: str) -> list[dict]:
    csv_path = REPORT_DIR / protein / f"{protein}_summary.csv"
    if not csv_path.exists():
        return []
    with open(csv_path) as f:
        return list(csv.DictReader(f))


def parse_anchor_label(label: str) -> list[tuple[str, int]]:
    """Parse anchor label like 'F365/I133' into [(F, 365), (I, 133)].
    Positions are 1-indexed as stored in the CSV."""
    if not label or not label.strip():
        return []
    result = []
    for p in label.split("/"):
        p = p.strip()
        m = re.match(r"([A-Z])(\d+)", p)
        if m:
            result.append((m.group(1), int(m.group(2))))
    return result


def discover_anchor_positions(protein: str, target_heads: list[tuple[int, int]]) -> dict:
    """For each target head, find its K-anchor positions from the summary CSV.

    Returns dict: (layer, head) -> list of (pos_0idx, aa) tuples.
    Positions are converted to 0-indexed sequence space."""
    rows = load_summary_csv(protein)
    if not rows:
        return {}
    target_set = set(target_heads)
    result = defaultdict(list)
    for row in rows:
        layer = int(row["layer"])
        head = int(row["head"])
        if (layer, head) not in target_set:
            continue
        k_type = row["k_anchor"].strip()
        if k_type in ("SINGLE-ANCHOR", "DUAL-ANCHOR", "MULTI-ANCHOR"):
            for aa, pos_0idx in parse_anchor_label(row["k_label"]):
                result[(layer, head)].append((pos_0idx, aa))  # CSV positions are 0-indexed
    return dict(result)


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model(device: str):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer

    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device).eval()
    model = NNsight(esm_model)
    return model, tokenizer


# ---------------------------------------------------------------------------
# Weight extraction and SVD
# ---------------------------------------------------------------------------

def extract_head_wk_svd(model, layer: int, head: int) -> dict:
    """Extract per-head W_K and compute its SVD.

    Returns dict with keys:
        W_K_hd: (64, 1280) — per-head key weight
        b_K_d: (64,) — per-head key bias
        U_dd: (64, 64) — left singular vectors (key space)
        S_d: (64,) — singular values
        Vh_dD: (64, 1280) — right singular vectors (residual stream space)
    """
    W_K_full = model._model.esm.encoder.layer[layer].attention.self.key.weight.data  # (1280, 1280)
    b_K_full = model._model.esm.encoder.layer[layer].attention.self.key.bias.data  # (1280,)

    W_K_per_head = W_K_full.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)  # (20, 64, 1280)
    b_K_per_head = b_K_full.reshape(NUM_HEADS, HEAD_DIM)  # (20, 64)

    W_K_hd = W_K_per_head[head].clone().cpu()  # (64, 1280)
    b_K_d = b_K_per_head[head].clone().cpu()  # (64,)

    U_dd, S_d, Vh_dD = torch.linalg.svd(W_K_hd, full_matrices=False)
    # U_dd: (64, 64), S_d: (64,), Vh_dD: (64, 1280)

    return {
        "W_K_hd": W_K_hd,
        "b_K_d": b_K_d,
        "U_dd": U_dd,
        "S_d": S_d,
        "Vh_dD": Vh_dD,
    }


# ---------------------------------------------------------------------------
# Residual stream capture
# ---------------------------------------------------------------------------

def capture_post_ln_residual(model, tokenizer, sequence: str, target_layers: list[int], device: str) -> dict:
    """Run forward pass and capture post-LayerNorm residual stream at target layers.

    Returns dict: layer -> Tensor(seq_len_with_tokens, 1280) on CPU."""
    inputs = tokenizer(sequence, return_tensors="pt").to(device)

    ln_modules = [model.esm.encoder.layer[L].attention.LayerNorm for L in target_layers]

    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            ln_cache = tracer.cache(modules=ln_modules)

    result = {}
    for L in target_layers:
        key = f"model.esm.encoder.layer.{L}.attention.LayerNorm"
        x_ln = ln_cache[key].output.detach().cpu()  # (1, seq_len, 1280)
        result[L] = x_ln[0]  # (seq_len, 1280)

    return result


# ---------------------------------------------------------------------------
# Step 1: Key norm and SVD projection analysis
# ---------------------------------------------------------------------------

def compute_key_vectors(x_ln_LD: torch.Tensor, svd_dict: dict) -> tuple[torch.Tensor, torch.Tensor]:
    """Compute per-position key vectors (with and without bias).

    Returns:
        k_raw_Ld: (seq_len, 64) — with bias
        k_nobias_Ld: (seq_len, 64) — without bias
    """
    W_K_hd = svd_dict["W_K_hd"]  # (64, 1280)
    b_K_d = svd_dict["b_K_d"]  # (64,)

    k_nobias_Ld = x_ln_LD @ W_K_hd.T  # (seq_len, 64)
    k_raw_Ld = k_nobias_Ld + b_K_d.unsqueeze(0)  # (seq_len, 64)

    return k_raw_Ld, k_nobias_Ld


def analyze_key_norms(k_raw_Ld: torch.Tensor, k_nobias_Ld: torch.Tensor, anchor_token_positions: list[int], svd_dict: dict) -> list[dict]:
    """Step 1 analysis for one protein/head combination.

    anchor_token_positions: list of positions in TOKEN space (0-indexed, with BOS offset).

    Returns list of result dicts, one per anchor position."""
    norms_raw_L = k_raw_Ld.norm(dim=-1)  # (seq_len,)
    norms_nobias_L = k_nobias_Ld.norm(dim=-1)  # (seq_len,)

    U_dd = svd_dict["U_dd"]  # (64, 64)
    S_d = svd_dict["S_d"]  # (64,)

    # Exclude BOS (0) and EOS (last) for statistics
    seq_len = k_raw_Ld.shape[0]
    residue_mask = torch.zeros(seq_len, dtype=torch.bool)
    residue_mask[1:-1] = True
    residue_norms = norms_raw_L[residue_mask]

    mean_norm = residue_norms.mean().item()
    std_norm = residue_norms.std().item()

    results = []
    for tok_pos in anchor_token_positions:
        if tok_pos < 0 or tok_pos >= seq_len:
            continue

        k_anchor = k_raw_Ld[tok_pos]  # (64,)
        k_anchor_nobias = k_nobias_Ld[tok_pos]  # (64,)
        anchor_norm = norms_raw_L[tok_pos].item()
        anchor_norm_nobias = norms_nobias_L[tok_pos].item()

        # Rank among residue positions (1 = largest)
        rank = (residue_norms > anchor_norm).sum().item() + 1
        n_residues = residue_mask.sum().item()
        percentile = 100.0 * (1.0 - rank / n_residues)
        zscore = (anchor_norm - mean_norm) / std_norm if std_norm > 0 else 0.0

        # SVD projections: project k_anchor onto left-singular vectors (key space directions)
        projections = k_anchor @ U_dd  # (64,) — projection onto each left-SV
        proj_sq = projections ** 2
        total_sq_norm = (k_anchor ** 2).sum().item()

        # Fraction explained by top-k SVD components
        frac_top1 = proj_sq[0].item() / total_sq_norm if total_sq_norm > 0 else 0.0
        frac_top3 = proj_sq[:3].sum().item() / total_sq_norm if total_sq_norm > 0 else 0.0
        frac_top5 = proj_sq[:5].sum().item() / total_sq_norm if total_sq_norm > 0 else 0.0

        # Rank of anchor's top-1 projection among all residue positions
        all_proj_top1 = (k_raw_Ld @ U_dd[:, 0]).abs()  # (seq_len,)
        anchor_proj_top1 = all_proj_top1[tok_pos].item()
        proj_top1_rank = (all_proj_top1[residue_mask] > anchor_proj_top1).sum().item() + 1

        results.append({
            "tok_pos": tok_pos,
            "k_norm_raw": anchor_norm,
            "k_norm_nobias": anchor_norm_nobias,
            "k_norm_rank": rank,
            "k_norm_percentile": percentile,
            "k_norm_zscore": zscore,
            "mean_k_norm": mean_norm,
            "max_k_norm": residue_norms.max().item(),
            "n_residues": n_residues,
            "svd_proj_top1": projections[0].item(),
            "svd_proj_top1_rank": proj_top1_rank,
            "frac_top1": frac_top1,
            "frac_top3": frac_top3,
            "frac_top5": frac_top5,
        })

    return results


# ---------------------------------------------------------------------------
# Step 2: Anchor direction in residual stream space
# ---------------------------------------------------------------------------

def compute_anchor_directions(k_raw_d: torch.Tensor, k_nobias_d: torch.Tensor, svd_dict: dict) -> tuple[torch.Tensor, torch.Tensor]:
    """Project anchor key back to residual stream space.

    Returns:
        d_resid_raw_D: (1280,) — from raw key (includes bias)
        d_resid_nobias_D: (1280,) — from bias-subtracted key (content only)
    """
    W_K_hd = svd_dict["W_K_hd"]  # (64, 1280)

    k_hat_raw = k_raw_d / k_raw_d.norm()
    k_hat_nobias = k_nobias_d / k_nobias_d.norm()

    d_resid_raw_D = W_K_hd.T @ k_hat_raw  # (1280,)
    d_resid_nobias_D = W_K_hd.T @ k_hat_nobias  # (1280,)

    return d_resid_raw_D, d_resid_nobias_D


def correlate_with_aa_embeddings(d_resid_D: torch.Tensor, model) -> list[tuple[str, float]]:
    """Cosine similarity between anchor direction and each amino acid embedding.

    Returns sorted list of (aa_token, cosine_sim) from highest to lowest."""
    emb_weight = model._model.esm.embeddings.word_embeddings.weight.data.cpu()  # (vocab_size, 1280)
    from transformers import EsmTokenizer
    tokenizer = EsmTokenizer.from_pretrained("facebook/esm2_t33_650M_UR50D")

    d_norm = d_resid_D / d_resid_D.norm()
    emb_norms = emb_weight / emb_weight.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    cos_sims = emb_norms @ d_norm  # (vocab_size,)

    # Standard amino acids
    standard_aas = "ACDEFGHIKLMNPQRSTVWY"
    results = []
    for aa in standard_aas:
        tok_id = tokenizer.convert_tokens_to_ids(aa)
        if tok_id is not None:
            results.append((aa, cos_sims[tok_id].item()))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def correlate_with_sse(d_resid_D: torch.Tensor, x_ln_LD: torch.Tensor, sse_str: str) -> dict:
    """Group residue positions by SSE type and compare mean projection onto anchor direction.

    x_ln_LD is in token space (includes BOS/EOS). sse_str is in sequence space.
    Returns dict: sse_type -> (mean_projection, n_positions)."""
    d_norm = d_resid_D / d_resid_D.norm()
    projections = x_ln_LD @ d_norm  # (seq_len_tokens,)

    sse_groups = defaultdict(list)
    for i, ss_char in enumerate(sse_str):
        tok_pos = i + 1  # BOS offset
        if tok_pos < projections.shape[0] - 1:  # exclude EOS
            label = {"H": "helix", "E": "strand", "-": "coil"}.get(ss_char, "other")
            sse_groups[label].append(projections[tok_pos].item())

    result = {}
    for label, vals in sse_groups.items():
        result[label] = (np.mean(vals), len(vals))
    return result


def compute_position_projection_profile(d_resid_D: torch.Tensor, x_ln_LD: torch.Tensor) -> torch.Tensor:
    """Compute dot(x_ln_j, d_resid) for every position. Returns (seq_len_tokens,)."""
    d_norm = d_resid_D / d_resid_D.norm()
    return (x_ln_LD @ d_norm)  # (seq_len_tokens,)


# ---------------------------------------------------------------------------
# Step 3: Cross-protein comparison
# ---------------------------------------------------------------------------

def compute_pairwise_cosine(vectors: dict) -> dict:
    """Compute pairwise cosine similarity between named vectors.

    vectors: name -> Tensor(d,)
    Returns dict of (name_i, name_j) -> cosine_sim for all unique pairs."""
    names = sorted(vectors.keys())
    result = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            vi = vectors[names[i]]
            vj = vectors[names[j]]
            cos = F.cosine_similarity(vi.unsqueeze(0), vj.unsqueeze(0)).item()
            result[(names[i], names[j])] = cos
    return result


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def write_report(out_path: Path, head_results: dict, svd_dicts: dict, target_heads: list[tuple[int, int]]):
    """Generate markdown report."""
    lines = []
    lines.append("# Anchor Decomposition via W_K SVD")
    lines.append("")
    lines.append(f"Heads analyzed: {', '.join(f'L{l}H{h}' for l, h in target_heads)}")
    lines.append("")

    for layer, head in target_heads:
        hname = f"L{layer}H{head}"
        hdata = head_results.get((layer, head), {})
        svd = svd_dicts.get((layer, head), {})

        lines.append(f"## {hname}")
        lines.append("")

        # SVD spectrum
        if "S_d" in svd:
            S = svd["S_d"]
            total_var = (S ** 2).sum().item()
            lines.append("### W_K singular value spectrum")
            lines.append("")
            lines.append(f"Top-5 singular values: {', '.join(f'{s:.2f}' for s in S[:5].tolist())}")
            lines.append(f"Fraction of variance in top-1/3/5: {(S[0]**2/total_var).item():.3f} / {(S[:3]**2).sum().item()/total_var:.3f} / {(S[:5]**2).sum().item()/total_var:.3f}")
            lines.append("")

        # Step 1 table
        step1_rows = hdata.get("step1_rows", [])
        if step1_rows:
            lines.append("### Step 1: Key norm analysis")
            lines.append("")
            lines.append("| protein | anchor_pos | aa | k_norm | rank | percentile | zscore | frac_top1 | frac_top3 | proj_top1_rank |")
            lines.append("|---------|-----------|----|---------|----|-----------|--------|----------|----------|---------------|")
            for r in step1_rows:
                lines.append(f"| {r['protein']} | {r['seq_pos']} | {r['aa']} | {r['k_norm_raw']:.3f} | {r['k_norm_rank']} | {r['k_norm_percentile']:.1f} | {r['k_norm_zscore']:.2f} | {r['frac_top1']:.3f} | {r['frac_top3']:.3f} | {r['svd_proj_top1_rank']} |")
            lines.append("")

            # Summary stats
            norms_z = [r["k_norm_zscore"] for r in step1_rows]
            percentiles = [r["k_norm_percentile"] for r in step1_rows]
            lines.append(f"Mean anchor key norm Z-score: {np.mean(norms_z):.2f} (std {np.std(norms_z):.2f})")
            lines.append(f"Mean anchor percentile: {np.mean(percentiles):.1f}%")
            lines.append("")

        # Step 2: AA embedding correlation
        aa_corr_all = hdata.get("aa_embedding_corr", {})
        if aa_corr_all:
            lines.append("### Step 2: Anchor direction correlations")
            lines.append("")

            lines.append("#### AA embedding cosine similarity (top 5, averaged across proteins)")
            lines.append("")
            # Average across proteins
            aa_avg = defaultdict(list)
            for protein, aa_list in aa_corr_all.items():
                for aa, cos in aa_list:
                    aa_avg[aa].append(cos)
            aa_sorted = sorted(aa_avg.items(), key=lambda x: np.mean(x[1]), reverse=True)
            lines.append("| AA | mean cos | std |")
            lines.append("|----|----------|-----|")
            for aa, vals in aa_sorted[:5]:
                lines.append(f"| {aa} | {np.mean(vals):.4f} | {np.std(vals):.4f} |")
            lines.append("")

        # Step 2: SSE correlation
        sse_corr_all = hdata.get("sse_corr", {})
        if sse_corr_all:
            lines.append("#### SSE projection (mean dot product with anchor direction)")
            lines.append("")
            lines.append("| protein | helix | strand | coil |")
            lines.append("|---------|-------|--------|------|")
            for protein, sse_data in sorted(sse_corr_all.items()):
                h_val = sse_data.get("helix", (0.0, 0))[0]
                e_val = sse_data.get("strand", (0.0, 0))[0]
                c_val = sse_data.get("coil", (0.0, 0))[0]
                lines.append(f"| {protein} | {h_val:.4f} | {e_val:.4f} | {c_val:.4f} |")
            lines.append("")

        # Step 2: Position projection profile — anchor rank
        proj_ranks = hdata.get("projection_profile_ranks", {})
        if proj_ranks:
            lines.append("#### Position projection profile: anchor rank")
            lines.append("")
            lines.append("For each protein, we compute dot(x_ln_j, d_resid_nobias) for all j and rank the anchor position.")
            lines.append("")
            lines.append("| protein | anchor_pos | projection_rank | n_residues |")
            lines.append("|---------|-----------|----------------|-----------|")
            for protein, rank_list in sorted(proj_ranks.items()):
                for rd in rank_list:
                    lines.append(f"| {protein} | {rd['seq_pos']} | {rd['rank']} | {rd['n_residues']} |")
            lines.append("")

        # Step 3: Cross-protein similarity
        cos_data = hdata.get("cross_protein_cosine", {})
        if cos_data:
            lines.append("### Step 3: Cross-protein anchor direction comparison")
            lines.append("")

            for version in ("raw", "nobias"):
                anchor_cos = cos_data.get(f"anchor_{version}", {})
                control_cos = cos_data.get(f"control_{version}", [])
                if not anchor_cos:
                    continue

                anchor_vals = list(anchor_cos.values())
                lines.append(f"#### Key vectors ({version})")
                lines.append("")

                if anchor_vals:
                    lines.append(f"Anchor-anchor pairwise cosine: mean={np.mean(anchor_vals):.4f}, std={np.std(anchor_vals):.4f}, n={len(anchor_vals)}")
                if control_cos:
                    lines.append(f"Anchor-random control cosine: mean={np.mean(control_cos):.4f}, std={np.std(control_cos):.4f}, n={len(control_cos)}")

                if anchor_vals and control_cos and len(anchor_vals) >= 2 and len(control_cos) >= 2:
                    U_stat, p_val = stats.mannwhitneyu(anchor_vals, control_cos, alternative="greater")
                    lines.append(f"Mann-Whitney U (anchor > control): U={U_stat:.1f}, p={p_val:.4g}")
                lines.append("")

            # Bias contamination check
            raw_cos = cos_data.get("anchor_raw", {})
            nobias_cos = cos_data.get("anchor_nobias", {})
            if raw_cos and nobias_cos:
                raw_mean = np.mean(list(raw_cos.values()))
                nobias_mean = np.mean(list(nobias_cos.values()))
                diff = raw_mean - nobias_mean
                lines.append(f"Bias contamination check: raw mean cos - nobias mean cos = {diff:.4f}")
                if abs(diff) > 0.05:
                    lines.append(f"Note: bias contributes meaningfully to cross-protein similarity (delta > 0.05).")
                else:
                    lines.append(f"Bias contribution is small (delta <= 0.05).")
                lines.append("")

            # Pairwise detail table
            nobias_cos_pairs = cos_data.get("anchor_nobias", {})
            if nobias_cos_pairs:
                lines.append("#### Pairwise cosine similarity (nobias)")
                lines.append("")
                lines.append("| protein_i | protein_j | cosine |")
                lines.append("|-----------|-----------|--------|")
                for (pi, pj), cos in sorted(nobias_cos_pairs.items(), key=lambda x: x[1], reverse=True):
                    lines.append(f"| {pi} | {pj} | {cos:.4f} |")
                lines.append("")

        lines.append("---")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    print(f"Report written to {out_path}")


def write_step1_csv(out_path: Path, all_step1_rows: list[dict]):
    """Write Step 1 data as CSV."""
    if not all_step1_rows:
        return
    fieldnames = ["head", "protein", "seq_pos", "aa", "k_norm_raw", "k_norm_nobias", "k_norm_rank", "k_norm_percentile", "k_norm_zscore", "mean_k_norm", "max_k_norm", "n_residues", "svd_proj_top1", "svd_proj_top1_rank", "frac_top1", "frac_top3", "frac_top5"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in all_step1_rows:
            writer.writerow({k: row[k] for k in fieldnames})
    print(f"Step 1 CSV written to {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Anchor decomposition via W_K SVD")
    parser.add_argument("--heads", nargs="+", default=None, help="Heads to analyze as layer,head pairs (e.g. 11,16 10,9)")
    parser.add_argument("--device", default=None)
    parser.add_argument("--proteins", nargs="+", default=None, help="Specific proteins to analyze")
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Parse target heads
    if args.heads:
        target_heads = []
        for h in args.heads:
            parts = h.split(",")
            target_heads.append((int(parts[0]), int(parts[1])))
    else:
        target_heads = DEFAULT_HEADS

    print(f"Target heads: {', '.join(f'L{l}H{h}' for l, h in target_heads)}")

    # Load configs and data
    protein_configs, common_cfg, seqs, ss_dict = load_all_configs()

    # Discover proteins with both summary CSV and full_seq_attn_cache
    if args.proteins:
        proteins = args.proteins
    else:
        proteins = []
        for p in sorted(protein_configs.keys()):
            summary_path = REPORT_DIR / p / f"{p}_summary.csv"
            cache_path = CACHE_DIR / p / "full_seq_attn_cache.pt"
            if summary_path.exists() and cache_path.exists():
                proteins.append(p)
    print(f"Proteins to analyze ({len(proteins)}): {', '.join(proteins)}")

    # Load model
    print("Loading model...")
    model, tokenizer = load_model(device)

    # Extract W_K and SVD for each target head
    print("Computing W_K SVD for target heads...")
    svd_dicts = {}
    for layer, head in target_heads:
        svd_dicts[(layer, head)] = extract_head_wk_svd(model, layer, head)
        S = svd_dicts[(layer, head)]["S_d"]
        print(f"  L{layer}H{head}: top-3 singular values = {S[0]:.2f}, {S[1]:.2f}, {S[2]:.2f}")

    # Unique layers needed for residual stream capture
    unique_layers = sorted(set(l for l, h in target_heads))

    # Per-head result accumulators
    head_results = {(l, h): {
        "step1_rows": [],
        "aa_embedding_corr": {},
        "sse_corr": {},
        "projection_profile_ranks": {},
        "cross_protein_cosine": {
            "anchor_raw_keys": {},
            "anchor_nobias_keys": {},
            "anchor_raw_dresid": {},
            "anchor_nobias_dresid": {},
        },
    } for l, h in target_heads}

    all_step1_rows = []

    # Process each protein
    for protein in proteins:
        print(f"\n{'='*60}")
        print(f"Processing {protein}...")

        seq = seqs.get(protein)
        if not seq:
            print(f"  Skipping: no sequence found")
            continue

        sse_key = f"{protein}.pdb"
        sse_str = ss_dict.get(sse_key, "")

        # Discover anchor positions for target heads
        anchors = discover_anchor_positions(protein, target_heads)
        if not anchors:
            print(f"  Skipping: no anchor positions found for target heads")
            continue

        found_heads = [f"L{l}H{h}" for (l, h) in anchors]
        print(f"  Anchors found for: {', '.join(found_heads)}")

        # Capture post-LN residual streams
        needed_layers = sorted(set(l for l, h in anchors))
        print(f"  Capturing residual streams at layers: {needed_layers}")
        residual_streams = capture_post_ln_residual(model, tokenizer, seq, needed_layers, device)

        for (layer, head), anchor_list in anchors.items():
            hname = f"L{layer}H{head}"
            svd = svd_dicts[(layer, head)]
            x_ln_LD = residual_streams[layer]  # (seq_len_tokens, 1280)

            # Compute key vectors
            k_raw_Ld, k_nobias_Ld = compute_key_vectors(x_ln_LD, svd)

            # Convert anchor positions from 0-indexed sequence space to token space (BOS offset)
            anchor_token_positions = [pos + 1 for pos, aa in anchor_list]
            anchor_aas = {pos + 1: aa for pos, aa in anchor_list}

            # Step 1: Key norm analysis
            step1 = analyze_key_norms(k_raw_Ld, k_nobias_Ld, anchor_token_positions, svd)
            for r in step1:
                seq_pos = r["tok_pos"] - 1  # back to 0-indexed sequence
                aa = anchor_aas.get(r["tok_pos"], "?")
                row = {
                    "head": hname,
                    "protein": protein,
                    "seq_pos": seq_pos,
                    "aa": aa,
                    **r,
                }
                head_results[(layer, head)]["step1_rows"].append(row)
                all_step1_rows.append(row)

            print(f"  {hname}: {len(step1)} anchor(s) analyzed")
            for r in step1:
                print(f"    pos {r['tok_pos']-1}: norm={r['k_norm_raw']:.3f}, rank={r['k_norm_rank']}/{r['n_residues']}, percentile={r['k_norm_percentile']:.1f}%, z={r['k_norm_zscore']:.2f}")

            # Step 2: Anchor direction analysis (use first anchor for this head/protein)
            tok_pos = anchor_token_positions[0]
            k_raw_anchor = k_raw_Ld[tok_pos]
            k_nobias_anchor = k_nobias_Ld[tok_pos]

            d_resid_raw, d_resid_nobias = compute_anchor_directions(k_raw_anchor, k_nobias_anchor, svd)

            # AA embedding correlation (nobias version)
            aa_corr = correlate_with_aa_embeddings(d_resid_nobias, model)
            head_results[(layer, head)]["aa_embedding_corr"][protein] = aa_corr
            top3_aa = aa_corr[:3]
            print(f"    Top AA correlations: {', '.join(f'{aa}={c:.3f}' for aa, c in top3_aa)}")

            # SSE correlation (nobias version)
            if sse_str:
                sse_corr = correlate_with_sse(d_resid_nobias, x_ln_LD, sse_str)
                head_results[(layer, head)]["sse_corr"][protein] = sse_corr

            # Position projection profile rank
            proj_profile = compute_position_projection_profile(d_resid_nobias, x_ln_LD)
            residue_projs = proj_profile[1:-1]  # exclude BOS/EOS
            rank_list = []
            for tp in anchor_token_positions:
                anchor_proj_val = proj_profile[tp].item()
                rank = (residue_projs > anchor_proj_val).sum().item() + 1
                rank_list.append({
                    "seq_pos": tp - 1,
                    "rank": rank,
                    "n_residues": residue_projs.shape[0],
                })
            head_results[(layer, head)]["projection_profile_ranks"][protein] = rank_list

            # Store keys for Step 3 cross-protein comparison
            cross = head_results[(layer, head)]["cross_protein_cosine"]
            cross["anchor_raw_keys"][protein] = k_raw_anchor.cpu()
            cross["anchor_nobias_keys"][protein] = k_nobias_anchor.cpu()
            cross["anchor_raw_dresid"][protein] = d_resid_raw.cpu()
            cross["anchor_nobias_dresid"][protein] = d_resid_nobias.cpu()

            # Also store a random non-anchor key for control
            seq_len_tokens = k_raw_Ld.shape[0]
            anchor_set = set(anchor_token_positions)
            residue_positions = [i for i in range(1, seq_len_tokens - 1) if i not in anchor_set]
            if residue_positions:
                rng = np.random.RandomState(hash(protein) % (2**31))
                random_pos = rng.choice(residue_positions)
                cross.setdefault("control_raw_keys", {})[protein] = k_raw_Ld[random_pos].cpu()
                cross.setdefault("control_nobias_keys", {})[protein] = k_nobias_Ld[random_pos].cpu()

    # Step 3: Cross-protein comparisons
    print(f"\n{'='*60}")
    print("Step 3: Cross-protein anchor direction comparison")

    for layer, head in target_heads:
        hname = f"L{layer}H{head}"
        cross = head_results[(layer, head)]["cross_protein_cosine"]

        for version in ("raw", "nobias"):
            anchor_keys = cross.get(f"anchor_{version}_keys", {})
            if len(anchor_keys) < 2:
                continue

            # Pairwise anchor-anchor cosine
            pairwise = compute_pairwise_cosine(anchor_keys)
            cross[f"anchor_{version}"] = pairwise

            anchor_vals = list(pairwise.values())
            print(f"  {hname} ({version}): {len(anchor_keys)} proteins, {len(pairwise)} pairs")
            print(f"    Anchor-anchor cos: mean={np.mean(anchor_vals):.4f}, std={np.std(anchor_vals):.4f}")

            # Control: anchor-random cosine
            control_keys = cross.get(f"control_{version}_keys", {})
            control_cos_vals = []
            anchor_names = sorted(anchor_keys.keys())
            control_names = sorted(control_keys.keys())
            for an in anchor_names:
                for cn in control_names:
                    if an != cn:
                        cos = F.cosine_similarity(anchor_keys[an].unsqueeze(0), control_keys[cn].unsqueeze(0)).item()
                        control_cos_vals.append(cos)
            cross[f"control_{version}"] = control_cos_vals
            if control_cos_vals:
                print(f"    Anchor-random cos: mean={np.mean(control_cos_vals):.4f}, std={np.std(control_cos_vals):.4f}")

    # Write outputs
    print(f"\n{'='*60}")
    print("Writing outputs...")

    report_path = REPORT_DIR / "multi_protein" / "anchor_decomp.md"
    write_report(report_path, head_results, svd_dicts, target_heads)

    csv_path = REPORT_DIR / "multi_protein" / "anchor_decomp_step1.csv"
    write_step1_csv(csv_path, all_step1_rows)

    print("\nDone.")


if __name__ == "__main__":
    main()
