#!/usr/bin/env python3
"""Anchor head QK and OV analysis (Experiment 3_24).

Question 1: Why does the anchor key win the attention competition?
  - Compute mean query direction across all positions for a target head.
  - Project all key vectors onto this direction; check if anchor ranks highest.
  - Compute W_Q^T @ q_mean (search direction in residual stream space) and compare
    across proteins to determine whether the head has a fixed search direction.

Question 2: What information does the head write?
  - Compute OV output = W_O_h @ W_V_h @ x_anchor_ln for the anchor position.
  - Report where it is written (attention-weighted region distribution).
  - Project OV output onto W_K and W_Q of an interaction head (L32H13).
  - Compare OV outputs across proteins via cosine similarity.

Usage:
    uv run python scripts/anchor_interp_v2.py --device cuda
    uv run python scripts/anchor_interp_v2.py --heads 11,16 10,9 --interaction-heads 32,13 --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs"
CACHE_DIR = ROOT / "reports" / "cache"

NUM_LAYERS = 33
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280

SEGMENT_RADIUS = 5

DEFAULT_ANCHOR_HEADS = [(11, 16), (10, 9), (14, 9)]
DEFAULT_INTERACTION_HEADS = [(32, 13)]

# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_dict = json.load(f)
    return protein_configs, seqs, ss_dict


def build_clean_sequence(sequence: str, config: dict) -> tuple[str, list[bool]]:
    """Build the clean masked sequence used in the contact jump experiment.

    Returns:
        masked_seq: string with '<mask>' at masked positions
        is_unmasked: list[bool] of length len(sequence), True = real residue visible
    """
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_start, ss1_end = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_start, ss2_end = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1

    masked: list[str] = ["<mask>"] * n
    # ss1 and ss2 cores
    for i in range(ss1_start, ss1_end):
        masked[i] = sequence[i]
    for i in range(ss2_start, ss2_end):
        masked[i] = sequence[i]
    # left flank of ss1
    for i in range(max(0, ss1_start - flank), ss1_start):
        masked[i] = sequence[i]
    # right flank of ss2
    for i in range(ss2_end, min(n, ss2_end + flank)):
        masked[i] = sequence[i]

    is_unmasked = [c != "<mask>" for c in masked]
    return "".join(masked), is_unmasked


def load_summary_csv(protein: str) -> list[dict]:
    csv_path = REPORT_DIR / protein / f"{protein}_summary.csv"
    if not csv_path.exists():
        return []
    with open(csv_path) as f:
        return list(csv.DictReader(f))


def parse_anchor_label(label: str) -> list[tuple[str, int]]:
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
    """Return dict: (layer, head) -> list of (seq_pos_0idx, aa)."""
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


def discover_proteins(anchor_heads: list[tuple[int, int]]) -> list[str]:
    """Find proteins that have full_seq_attn_cache.pt and a summary CSV."""
    result = []
    for d in sorted(CACHE_DIR.iterdir()):
        if not d.is_dir():
            continue
        has_attn = (d / "full_seq_attn_cache.pt").exists()
        has_summary = (REPORT_DIR / d.name / f"{d.name}_summary.csv").exists()
        if has_attn and has_summary:
            anchors = discover_anchor_positions(d.name, anchor_heads)
            if anchors:
                result.append(d.name)
    return result


# ---------------------------------------------------------------------------
# Model loading and weight extraction
# ---------------------------------------------------------------------------

def load_model(device: str):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device).eval()
    model = NNsight(esm_model)
    return model, tokenizer


def extract_head_weights(model, layer: int, head: int) -> dict:
    """Extract W_Q, W_K, W_V, W_O for a specific head.

    Returns dict with keys:
        W_Q_hd: (64, 1280)
        b_Q_d:  (64,)
        W_K_hd: (64, 1280)
        b_K_d:  (64,)
        W_V_hd: (64, 1280)
        b_V_d:  (64,)
        W_O_Dh: (1280, 64)  — per-head output projection
    """
    attn = model._model.esm.encoder.layer[layer].attention

    W_Q = attn.self.query.weight.data.cpu()  # (1280, 1280)
    b_Q = attn.self.query.bias.data.cpu()  # (1280,)
    W_K = attn.self.key.weight.data.cpu()
    b_K = attn.self.key.bias.data.cpu()
    W_V = attn.self.value.weight.data.cpu()
    b_V = attn.self.value.bias.data.cpu()
    W_O = attn.output.dense.weight.data.cpu()  # (1280, 1280)

    # Reshape into per-head matrices
    # query/key/value weight stored as (out_features, in_features) = (H*d, D)
    W_Q_heads = W_Q.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)  # (H, d, D)
    b_Q_heads = b_Q.reshape(NUM_HEADS, HEAD_DIM)
    W_K_heads = W_K.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_K_heads = b_K.reshape(NUM_HEADS, HEAD_DIM)
    W_V_heads = W_V.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_V_heads = b_V.reshape(NUM_HEADS, HEAD_DIM)

    # W_O is (D, H*d); per-head slice is columns [h*d:(h+1)*d]
    W_O_per_head = W_O[:, head * HEAD_DIM:(head + 1) * HEAD_DIM]  # (D, d) = (1280, 64)

    return {
        "W_Q_hd": W_Q_heads[head].clone(),  # (64, 1280)
        "b_Q_d": b_Q_heads[head].clone(),
        "W_K_hd": W_K_heads[head].clone(),
        "b_K_d": b_K_heads[head].clone(),
        "W_V_hd": W_V_heads[head].clone(),
        "b_V_d": b_V_heads[head].clone(),
        "W_O_Dh": W_O_per_head.clone(),   # (1280, 64)
    }


# ---------------------------------------------------------------------------
# Residual stream capture
# ---------------------------------------------------------------------------

def capture_post_ln_residuals(model, tokenizer, sequence: str, target_layers: list[int], device: str) -> dict:
    """Run forward pass and capture post-LayerNorm residuals at target layers.

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
# Region classification
# ---------------------------------------------------------------------------

def get_region(pos: int, config: dict) -> str:
    """Classify a sequence position (0-indexed) as ss1, ss2, flkL, flkR, or other."""
    pos1, pos2 = config["contact_pair"]
    radius = 5
    clean_f = config.get("clean_flank", 44)

    ss1_start, ss1_end = pos1 - radius, pos1 + radius + 1
    ss2_start, ss2_end = pos2 - radius, pos2 + radius + 1
    left_start = ss1_start - clean_f
    left_end = ss1_end + clean_f
    right_start = ss2_start - clean_f
    right_end = ss2_end + clean_f

    if ss1_start <= pos < ss1_end:
        return "ss1"
    if ss2_start <= pos < ss2_end:
        return "ss2"
    if left_start <= pos < ss1_start or ss1_end <= pos < left_end:
        return "flkL"
    if right_start <= pos < ss2_start or ss2_end <= pos < right_end:
        return "flkR"
    return "other"


# ---------------------------------------------------------------------------
# Question 1: Mean query direction analysis
# ---------------------------------------------------------------------------

def q1_mean_query_direction(
    x_ln_LD: torch.Tensor,
    weights: dict,
    anchor_token_positions: list[int],
    config: dict,
    unmasked_flags: list[bool] | None = None,
) -> dict:
    """Analyze why anchor key wins against the mean query direction.

    x_ln_LD: (seq_len, 1280) post-LN residuals (token space, includes BOS/EOS)
    weights: from extract_head_weights
    anchor_token_positions: token-space positions (seq_pos + 1 for BOS offset)
    config: protein config (for region labels)
    unmasked_flags: if provided (len = seq_len - 2, one per residue), True = real residue.
        Used to report anchor rank within unmasked positions only (separate from rank
        among all positions including mask tokens).

    Returns:
        q_mean_d: (64,) mean unit query direction in head space
        anchor_scores: {tok_pos: score}
        anchor_ranks_all: {tok_pos: rank among ALL residue positions}
        anchor_ranks_unmasked: {tok_pos: rank among unmasked positions only} (empty if no flags)
        score_all_L: (seq_len,) key-onto-q_mean scores for all positions
        q_search_D: (1280,) search direction in residual stream space
        n_residues: total number of residue positions
        n_unmasked: number of unmasked residue positions
    """
    W_Q = weights["W_Q_hd"]  # (64, 1280)
    b_Q = weights["b_Q_d"]  # (64,)
    W_K = weights["W_K_hd"]  # (64, 1280)
    b_K = weights["b_K_d"]

    seq_len = x_ln_LD.shape[0]

    # Compute all query vectors: (seq_len, 64)
    q_all_Ld = x_ln_LD @ W_Q.T + b_Q.unsqueeze(0)

    # Compute all key vectors: (seq_len, 64)
    k_all_Ld = x_ln_LD @ W_K.T + b_K.unsqueeze(0)

    # Mean unit query direction (exclude BOS and EOS)
    q_residues = q_all_Ld[1:-1]  # (n_residues, 64)
    q_norms = q_residues.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_unit = q_residues / q_norms  # (n_residues, 64)
    q_mean_d = q_unit.mean(dim=0)  # (64,)

    # Score = k_j · q_mean for each position
    score_all_L = k_all_Ld @ q_mean_d  # (seq_len,)
    score_residues = score_all_L[1:-1]  # (n_residues,), excludes BOS/EOS
    n_residues = score_residues.shape[0]

    # Unmasked-only scores
    unmasked_tok_positions: set[int] = set()
    n_unmasked = 0
    if unmasked_flags is not None:
        for i, flag in enumerate(unmasked_flags):
            if flag:
                unmasked_tok_positions.add(i + 1)  # +1 for BOS
        n_unmasked = len(unmasked_tok_positions)
        score_unmasked = score_all_L[torch.tensor(sorted(unmasked_tok_positions))]
    else:
        score_unmasked = None

    # Anchor scores and ranks
    anchor_scores = {}
    anchor_ranks_all = {}
    anchor_ranks_unmasked = {}
    for tok_pos in anchor_token_positions:
        if 1 <= tok_pos <= seq_len - 2:
            s = score_all_L[tok_pos].item()
            anchor_scores[tok_pos] = s
            anchor_ranks_all[tok_pos] = (score_residues > s).sum().item() + 1
            if score_unmasked is not None:
                anchor_ranks_unmasked[tok_pos] = (score_unmasked > s).sum().item() + 1

    # Search direction in residual stream: W_Q^T @ q_mean
    q_mean_normalized = q_mean_d / q_mean_d.norm().clamp(min=1e-8)
    q_search_D = W_Q.T @ q_mean_normalized  # (1280,)

    return {
        "q_mean_d": q_mean_d,
        "q_search_D": q_search_D,
        "anchor_scores": anchor_scores,
        "anchor_ranks_all": anchor_ranks_all,
        "anchor_ranks_unmasked": anchor_ranks_unmasked,
        "score_all_L": score_all_L,
        "n_residues": n_residues,
        "n_unmasked": n_unmasked,
        "q_mean_norm": q_mean_d.norm().item(),
    }


# ---------------------------------------------------------------------------
# Question 2: OV output analysis
# ---------------------------------------------------------------------------

def q2_ov_output(
    x_ln_LD: torch.Tensor,
    attn_weights_LL: torch.Tensor,
    weights: dict,
    anchor_tok_pos: int,
    config: dict,
    seq_len_residues: int,
    interaction_weights: dict,
) -> dict:
    """Analyze what the anchor head writes.

    attn_weights_LL: (seq_len, seq_len) attention probs for this head
    anchor_tok_pos: token-space position of anchor residue
    interaction_weights: dict of (layer, head) -> weights dict from extract_head_weights

    Returns:
        ov_output_D: (1280,) OV output vector from reading the anchor
        region_attn: dict of region -> total attention weight received
        proj_K_interaction: dict of (layer, head) -> projection onto W_K
        proj_Q_interaction: dict of (layer, head) -> projection onto W_Q
    """
    W_V = weights["W_V_hd"]  # (64, 1280)
    b_V = weights["b_V_d"]   # (64,)
    W_O = weights["W_O_Dh"]  # (1280, 64)

    # Value at anchor position
    x_anchor = x_ln_LD[anchor_tok_pos]  # (1280,)
    v_anchor = W_V @ x_anchor + b_V  # (64,)

    # OV output = W_O @ v_anchor
    ov_output_D = W_O @ v_anchor  # (1280,)

    # Attention distribution: attn_weights_LL[q, anchor_tok_pos] = weight that position q
    # puts on the anchor key. This is where the OV output goes.
    # For each query position q, it receives ov_output * attn[q, anchor].
    attn_to_anchor = attn_weights_LL[:, anchor_tok_pos]  # (seq_len,) attention from each q to anchor

    # Region breakdown of where the OV output is sent (weighted by attention)
    region_attn = defaultdict(float)
    for tok_pos in range(1, seq_len_residues + 1):
        seq_pos = tok_pos - 1
        region = get_region(seq_pos, config)
        region_attn[region] += attn_to_anchor[tok_pos].item()

    # Projection onto interaction head W_K and W_Q
    ov_unit = ov_output_D / ov_output_D.norm().clamp(min=1e-8)
    proj_K_interaction = {}
    proj_Q_interaction = {}
    for (ilayer, ihead), iweights in interaction_weights.items():
        W_K_i = iweights["W_K_hd"]  # (64, 1280)
        W_Q_i = iweights["W_Q_hd"]  # (64, 1280)

        # How much does ov_output change the key representation at the interaction head?
        # key_delta = W_K_i @ ov_output_D; measure its norm relative to typical key norms
        k_delta = W_K_i @ ov_output_D  # (64,)
        q_delta = W_Q_i @ ov_output_D  # (64,)

        proj_K_interaction[(ilayer, ihead)] = {
            "k_delta_norm": k_delta.norm().item(),
            "q_delta_norm": q_delta.norm().item(),
            "k_delta": k_delta,
            "q_delta": q_delta,
        }
        proj_Q_interaction[(ilayer, ihead)] = proj_K_interaction[(ilayer, ihead)]

    return {
        "ov_output_D": ov_output_D,
        "v_anchor": v_anchor,
        "region_attn": dict(region_attn),
        "interaction_probes": proj_K_interaction,
    }


# ---------------------------------------------------------------------------
# Main analysis loop
# ---------------------------------------------------------------------------

def run(args):
    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    anchor_heads = args.heads
    interaction_heads_list = args.interaction_heads

    print(f"Anchor heads: {anchor_heads}")
    print(f"Interaction heads: {interaction_heads_list}")

    # Extract weights for all target heads
    print("\nExtracting weights...")
    anchor_weights = {}
    for layer, head in anchor_heads:
        anchor_weights[(layer, head)] = extract_head_weights(model, layer, head)
        print(f"  L{layer}H{head}: extracted")

    interaction_weights = {}
    for layer, head in interaction_heads_list:
        interaction_weights[(layer, head)] = extract_head_weights(model, layer, head)
        print(f"  L{layer}H{head} (interaction): extracted")

    # Discover proteins
    protein_configs, seqs, ss_dict = load_configs()
    proteins = discover_proteins(anchor_heads)
    print(f"\nProteins with anchor data + cache: {proteins}")

    # Per-protein, per-head results
    all_results = {}  # (protein, layer, head) -> result dict
    ov_outputs = {}  # (protein, layer, head) -> (1280,) tensor for cross-protein comparison

    for protein in proteins:
        config = protein_configs.get(protein, {})
        sequence = seqs.get(protein, "")
        if not sequence:
            print(f"  WARNING: no sequence for {protein}, skipping")
            continue

        print(f"\n=== {protein} (len={len(sequence)}) ===")

        # Get anchor positions for all target heads
        anchor_positions = discover_anchor_positions(protein, anchor_heads)
        if not anchor_positions:
            print(f"  No anchor positions found, skipping")
            continue

        # Target layers needed
        target_layers = list(set(l for l, h in anchor_heads) | set(l for l, h in interaction_heads_list))

        # Build the clean masked sequence (the actual circuit context)
        if "contact_pair" in config:
            clean_seq, is_unmasked = build_clean_sequence(sequence, config)
            n_unmasked = sum(is_unmasked)
            print(f"  Clean masked seq: {n_unmasked}/{len(sequence)} positions unmasked")
        else:
            clean_seq = sequence
            is_unmasked = [True] * len(sequence)
            print(f"  WARNING: no contact_pair in config, using full sequence")

        # Capture post-LN residuals on BOTH full sequence and masked sequence
        print(f"  Capturing residuals (full seq) at layers {sorted(target_layers)}...")
        residuals_full = capture_post_ln_residuals(model, tokenizer, sequence, target_layers, args.device)
        print(f"  Capturing residuals (masked seq) at layers {sorted(target_layers)}...")
        residuals_masked = capture_post_ln_residuals(model, tokenizer, clean_seq, target_layers, args.device)

        # Load cached attention (full sequence, used for Q2)
        attn_cache_path = CACHE_DIR / protein / "full_seq_attn_cache.pt"
        attn_cache = torch.load(attn_cache_path, weights_only=False, map_location="cpu")
        attn_LBHLL = attn_cache["attn_LBHLL"]

        for layer, head in anchor_heads:
            if (layer, head) not in anchor_positions:
                continue

            anchors = anchor_positions[(layer, head)]
            if not anchors:
                continue

            x_ln_full = residuals_full[layer]  # (seq_len_tok, 1280)
            x_ln_masked = residuals_masked[layer]  # same shape, different context
            seq_len_tok = x_ln_full.shape[0]
            seq_len_res = seq_len_tok - 2

            weights = anchor_weights[(layer, head)]
            attn_for_head = attn_LBHLL[layer][0, head]  # (seq_len_tok, seq_len_tok)

            # Convert seq_pos (0-indexed) to tok_pos (+1 for BOS)
            anchor_tok_positions = [pos + 1 for pos, aa in anchors]

            # -------- Q1: full sequence (baseline) --------
            q1_full = q1_mean_query_direction(x_ln_full, weights, anchor_tok_positions, config)

            # -------- Q1: masked sequence (circuit context) --------
            q1_masked = q1_mean_query_direction(
                x_ln_masked, weights, anchor_tok_positions, config,
                unmasked_flags=is_unmasked,
            )

            for tok_pos, (seq_pos, aa) in zip(anchor_tok_positions, anchors):
                region = get_region(seq_pos, config)
                # Full sequence ranking
                rank_full = q1_full["anchor_ranks_all"].get(tok_pos)
                score_full = q1_full["anchor_scores"].get(tok_pos, float("nan"))
                pct_full = 100.0 * (1.0 - rank_full / q1_full["n_residues"]) if rank_full else float("nan")
                # Masked sequence rankings
                rank_masked_all = q1_masked["anchor_ranks_all"].get(tok_pos)
                rank_masked_unm = q1_masked["anchor_ranks_unmasked"].get(tok_pos)
                score_masked = q1_masked["anchor_scores"].get(tok_pos, float("nan"))
                pct_masked_all = 100.0 * (1.0 - rank_masked_all / q1_masked["n_residues"]) if rank_masked_all else float("nan")
                pct_masked_unm = 100.0 * (1.0 - rank_masked_unm / q1_masked["n_unmasked"]) if rank_masked_unm and q1_masked["n_unmasked"] else float("nan")
                print(f"  L{layer}H{head}: {aa}{seq_pos+1} ({region})"
                      f" | FULL rank={rank_full}/{q1_full['n_residues']} ({pct_full:.0f}pct) score={score_full:.3f}"
                      f" | MASKED rank={rank_masked_all}/{q1_masked['n_residues']} ({pct_masked_all:.0f}pct)"
                      f" | among-unmasked rank={rank_masked_unm}/{q1_masked['n_unmasked']} ({pct_masked_unm:.0f}pct)")

            # -------- Q2 --------
            # Use first anchor only for OV analysis. Use full-seq residuals since
            # attn_LBHLL is from the full sequence forward pass.
            anchor_seq_pos, anchor_aa = anchors[0]
            anchor_tok_pos = anchor_seq_pos + 1

            q2 = q2_ov_output(
                x_ln_full, attn_for_head, weights,
                anchor_tok_pos, config, seq_len_res, interaction_weights
            )

            # Store results. Use q1_masked as primary Q1 result.
            key = (protein, layer, head)
            all_results[key] = {
                "q1": q1_masked,
                "q1_full": q1_full,
                "q2": q2,
                "anchor_seq_pos": anchor_seq_pos,
                "anchor_aa": anchor_aa,
            }
            ov_outputs[key] = q2["ov_output_D"]

            # Print OV summary
            ratd = q2["region_attn"]
            total = sum(ratd.values())
            print(f"  L{layer}H{head} OV: region attn distribution: "
                  + ", ".join(f"{r}={v/total:.2%}" for r, v in sorted(ratd.items()) if total > 0))

            for (il, ih), probe in q2["interaction_probes"].items():
                print(f"  L{layer}H{head} -> L{il}H{ih}: "
                      f"k_delta_norm={probe['k_delta_norm']:.4f}, "
                      f"q_delta_norm={probe['q_delta_norm']:.4f}")

    # -------------------------------------------------------------------------
    # Q1 Cross-protein: compare search directions
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Q1 CROSS-PROTEIN: Search direction (W_Q^T @ q_mean) alignment")
    print("=" * 60)

    for layer, head in anchor_heads:
        hname = f"L{layer}H{head}"
        search_dirs = {
            protein: all_results[(protein, layer, head)]["q1"]["q_search_D"]
            for protein in proteins
            if (protein, layer, head) in all_results
        }
        if len(search_dirs) < 2:
            continue

        # Pairwise cosine
        names = sorted(search_dirs.keys())
        cos_vals = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                vi = search_dirs[names[i]]
                vj = search_dirs[names[j]]
                cos = F.cosine_similarity(vi.unsqueeze(0), vj.unsqueeze(0)).item()
                cos_vals.append(cos)

        print(f"\n{hname}: mean pairwise cosine = {np.mean(cos_vals):.4f} "
              f"(std={np.std(cos_vals):.4f}, n={len(cos_vals)} pairs)")
        print(f"  Range: [{min(cos_vals):.4f}, {max(cos_vals):.4f}]")

        # Also report mean q_mean_norm (how concentrated queries are)
        norms = [all_results[(p, layer, head)]["q1"]["q_mean_norm"]
                 for p in names if (p, layer, head) in all_results]
        print(f"  Mean q_mean_norm: {np.mean(norms):.4f} (range [{min(norms):.4f}, {max(norms):.4f}])")
        print(f"  Interpretation: q_mean_norm close to 1.0 = queries are highly aligned; "
              f"search dir cosine close to 1.0 = fixed direction across proteins")

    # Also compute q_mean in head space alignment (not projected back to residual stream)
    print("\nQ1 CROSS-PROTEIN: Raw q_mean_d alignment (in head space)")
    for layer, head in anchor_heads:
        hname = f"L{layer}H{head}"
        q_means = {
            protein: all_results[(protein, layer, head)]["q1"]["q_mean_d"]
            for protein in proteins
            if (protein, layer, head) in all_results
        }
        if len(q_means) < 2:
            continue
        names = sorted(q_means.keys())
        cos_vals = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                vi = q_means[names[i]]
                vj = q_means[names[j]]
                cos = F.cosine_similarity(vi.unsqueeze(0), vj.unsqueeze(0)).item()
                cos_vals.append(cos)
        print(f"  {hname}: mean cos={np.mean(cos_vals):.4f} (std={np.std(cos_vals):.4f})")

    # -------------------------------------------------------------------------
    # Q2 Cross-protein: compare OV outputs
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Q2 CROSS-PROTEIN: OV output cosine similarity")
    print("=" * 60)

    for layer, head in anchor_heads:
        hname = f"L{layer}H{head}"
        ov_vecs = {
            protein: ov_outputs[(protein, layer, head)]
            for protein in proteins
            if (protein, layer, head) in ov_outputs
        }
        if len(ov_vecs) < 2:
            continue

        names = sorted(ov_vecs.keys())
        cos_vals = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                vi = ov_vecs[names[i]]
                vj = ov_vecs[names[j]]
                cos = F.cosine_similarity(vi.unsqueeze(0), vj.unsqueeze(0)).item()
                cos_vals.append(cos)

        print(f"\n{hname} OV outputs: mean pairwise cos={np.mean(cos_vals):.4f} "
              f"(std={np.std(cos_vals):.4f}, n={len(cos_vals)} pairs)")
        print(f"  Range: [{min(cos_vals):.4f}, {max(cos_vals):.4f}]")

        # OV norms
        norms = [ov_vecs[p].norm().item() for p in names]
        print(f"  OV output norms: mean={np.mean(norms):.4f}, range=[{min(norms):.4f}, {max(norms):.4f}]")

        # Per-protein anchor info
        print(f"  Anchor residues: "
              + ", ".join(f"{p}:{all_results.get((p, layer, head), {}).get('anchor_aa', '?')}"
                          f"{all_results.get((p, layer, head), {}).get('anchor_seq_pos', -1)+1}"
                          for p in names if (p, layer, head) in all_results))

    # -------------------------------------------------------------------------
    # Q2 interaction head projection summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("Q2: OV -> Interaction head projections (averaged across proteins)")
    print("=" * 60)

    for layer, head in anchor_heads:
        hname = f"L{layer}H{head}"
        print(f"\n{hname}:")
        for il, ih in interaction_heads_list:
            k_norms = []
            q_norms = []
            for protein in proteins:
                key = (protein, layer, head)
                if key not in all_results:
                    continue
                probes = all_results[key]["q2"]["interaction_probes"]
                if (il, ih) in probes:
                    k_norms.append(probes[(il, ih)]["k_delta_norm"])
                    q_norms.append(probes[(il, ih)]["q_delta_norm"])
            if k_norms:
                print(f"  -> L{il}H{ih}: mean k_delta_norm={np.mean(k_norms):.4f}, "
                      f"mean q_delta_norm={np.mean(q_norms):.4f}")
                print(f"     (k: {[f'{x:.3f}' for x in k_norms]}, "
                      f"q: {[f'{x:.3f}' for x in q_norms]})")

    # -------------------------------------------------------------------------
    # Write report and plots
    # -------------------------------------------------------------------------
    write_report(all_results, ov_outputs, proteins, anchor_heads, interaction_heads_list)
    plot_results(all_results, ov_outputs, proteins, anchor_heads, interaction_heads_list)


def write_report(all_results, ov_outputs, proteins, anchor_heads, interaction_heads_list):
    out_dir = REPORT_DIR / "multi_protein"
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / "anchor_interp_v2.md"

    with open(report_path, "w") as f:
        f.write("# Anchor Head QK and OV Analysis\n\n")
        f.write(f"Anchor heads: {', '.join(f'L{l}H{h}' for l, h in anchor_heads)}\n")
        f.write(f"Interaction heads: {', '.join(f'L{l}H{h}' for l, h in interaction_heads_list)}\n")
        f.write(f"Proteins: {', '.join(proteins)}\n\n")

        # ---- Q1 ----
        f.write("## Question 1: Why does the anchor key win?\n\n")
        f.write("### Per-protein anchor key rankings\n\n")

        for layer, head in anchor_heads:
            hname = f"L{layer}H{head}"
            f.write(f"#### {hname}\n\n")
            f.write("Masked context = residuals from clean masked sequence (circuit context). "
                    "Rank-among-unmasked = anchor rank relative to other real residues only.\n\n")
            f.write("| protein | anchor | region | masked rank/total | rank/unmasked | full-seq rank | q_mean_norm |\n")
            f.write("|---------|--------|--------|-------------------|---------------|---------------|-------------|\n")
            for protein in proteins:
                key = (protein, layer, head)
                if key not in all_results:
                    continue
                r = all_results[key]
                seq_pos = r["anchor_seq_pos"]
                aa = r["anchor_aa"]
                tok_pos = seq_pos + 1
                q1 = r["q1"]  # primary = masked context
                q1_full = r.get("q1_full", q1)
                rank_masked = q1["anchor_ranks_all"].get(tok_pos, "?")
                rank_unm = q1["anchor_ranks_unmasked"].get(tok_pos, "?")
                rank_full = q1_full["anchor_ranks_all"].get(tok_pos, "?")
                score_masked = q1["anchor_scores"].get(tok_pos, float("nan"))
                n_all = q1["n_residues"]
                n_unm = q1["n_unmasked"]
                n_full = q1_full["n_residues"]
                pct_masked = 100.0 * (1.0 - rank_masked / n_all) if isinstance(rank_masked, int) else float("nan")
                pct_unm = 100.0 * (1.0 - rank_unm / n_unm) if isinstance(rank_unm, int) and n_unm else float("nan")
                pct_full = 100.0 * (1.0 - rank_full / n_full) if isinstance(rank_full, int) else float("nan")
                config_p = {}
                try:
                    with open(Path(__file__).resolve().parent.parent / "configs" / "proteins.json") as cf:
                        config_p = json.load(cf).get(protein, {})
                except Exception:
                    pass
                region = get_region(seq_pos, config_p)
                f.write(f"| {protein} | {aa}{seq_pos+1} | {region}"
                        f" | {rank_masked}/{n_all} ({pct_masked:.0f}%)"
                        f" | {rank_unm}/{n_unm} ({pct_unm:.0f}%)"
                        f" | {rank_full}/{n_full} ({pct_full:.0f}%)"
                        f" | {q1['q_mean_norm']:.3f} |\n")
            f.write("\n")

        f.write("### Cross-protein search direction alignment\n\n")
        f.write("q_mean is the average unit query direction. W_Q^T @ q_mean is the corresponding direction in residual stream space.\n")
        f.write("High cosine similarity across proteins = fixed search direction (property of W_Q); low = context-dependent.\n\n")

        f.write("| head | q_mean cosine (head space) | search dir cosine (resid space) | mean q_mean_norm |\n")
        f.write("|------|---------------------------|--------------------------------|------------------|\n")
        for layer, head in anchor_heads:
            hname = f"L{layer}H{head}"
            q_means = {p: all_results[(p, layer, head)]["q1"]["q_mean_d"]
                       for p in proteins if (p, layer, head) in all_results}
            search_dirs = {p: all_results[(p, layer, head)]["q1"]["q_search_D"]
                           for p in proteins if (p, layer, head) in all_results}
            norms = [all_results[(p, layer, head)]["q1"]["q_mean_norm"]
                     for p in proteins if (p, layer, head) in all_results]

            names = sorted(q_means.keys())

            def mean_cos(vecs):
                vals = []
                ns = sorted(vecs.keys())
                for i in range(len(ns)):
                    for j in range(i + 1, len(ns)):
                        vals.append(F.cosine_similarity(
                            vecs[ns[i]].unsqueeze(0), vecs[ns[j]].unsqueeze(0)).item())
                return np.mean(vals) if vals else float("nan")

            qm_cos = mean_cos(q_means)
            sd_cos = mean_cos(search_dirs)
            nm = np.mean(norms) if norms else float("nan")
            f.write(f"| {hname} | {qm_cos:.4f} | {sd_cos:.4f} | {nm:.4f} |\n")
        f.write("\n")

        # ---- Q2 ----
        f.write("## Question 2: What does the anchor head write?\n\n")
        f.write("### Attention distribution to anchor (where OV output goes)\n\n")
        f.write("Values are fraction of total attention in the column pointing to the anchor.\n\n")

        for layer, head in anchor_heads:
            hname = f"L{layer}H{head}"
            f.write(f"#### {hname}\n\n")
            f.write("| protein | anchor | ss1 | ss2 | flkL | flkR | other |\n")
            f.write("|---------|--------|-----|-----|------|------|-------|\n")
            for protein in proteins:
                key = (protein, layer, head)
                if key not in all_results:
                    continue
                r = all_results[key]
                ratd = r["q2"]["region_attn"]
                total = sum(ratd.values())
                if total == 0:
                    continue
                aa = r["anchor_aa"]
                sp = r["anchor_seq_pos"]
                def pct(reg): return f"{ratd.get(reg, 0) / total:.1%}"
                f.write(f"| {protein} | {aa}{sp+1} | {pct('ss1')} | {pct('ss2')} | {pct('flkL')} | {pct('flkR')} | {pct('other')} |\n")
            f.write("\n")

        f.write("### OV output -> interaction head projections\n\n")
        f.write("k_delta_norm = ||W_K_interaction @ ov_output|| (anchor head changes destination as a key).\n")
        f.write("q_delta_norm = ||W_Q_interaction @ ov_output|| (anchor head changes what destination queries for).\n\n")

        for layer, head in anchor_heads:
            hname = f"L{layer}H{head}"
            f.write(f"#### {hname}\n\n")
            for il, ih in interaction_heads_list:
                iname = f"L{il}H{ih}"
                f.write(f"##### {hname} -> {iname}\n\n")
                f.write("| protein | anchor | k_delta_norm | q_delta_norm |\n")
                f.write("|---------|--------|--------------|---------------|\n")
                for protein in proteins:
                    key = (protein, layer, head)
                    if key not in all_results:
                        continue
                    r = all_results[key]
                    probes = r["q2"]["interaction_probes"]
                    if (il, ih) not in probes:
                        continue
                    p = probes[(il, ih)]
                    aa = r["anchor_aa"]
                    sp = r["anchor_seq_pos"]
                    f.write(f"| {protein} | {aa}{sp+1} | {p['k_delta_norm']:.4f} | {p['q_delta_norm']:.4f} |\n")
                f.write("\n")

        f.write("### Cross-protein OV output similarity\n\n")
        f.write("| head | mean pairwise cos | std | ov_norm mean |\n")
        f.write("|------|-------------------|-----|-------------|\n")
        for layer, head in anchor_heads:
            hname = f"L{layer}H{head}"
            vecs = {p: ov_outputs[(p, layer, head)]
                    for p in proteins if (p, layer, head) in ov_outputs}
            names = sorted(vecs.keys())
            cos_vals = []
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    cos_vals.append(F.cosine_similarity(
                        vecs[names[i]].unsqueeze(0), vecs[names[j]].unsqueeze(0)).item())
            norms = [vecs[p].norm().item() for p in names]
            mc = np.mean(cos_vals) if cos_vals else float("nan")
            sc = np.std(cos_vals) if cos_vals else float("nan")
            mn = np.mean(norms) if norms else float("nan")
            f.write(f"| {hname} | {mc:.4f} | {sc:.4f} | {mn:.4f} |\n")

    print(f"\nReport written to {report_path}")


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def plot_results(all_results, ov_outputs, proteins, anchor_heads, interaction_heads_list):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    out_dir = REPORT_DIR / "multi_protein"
    out_dir.mkdir(parents=True, exist_ok=True)

    COLORS = {"masked": "#2166ac", "full": "#d1d1d1", "unmasked": "#92c5de"}
    REGION_COLORS = {"ss1": "#d73027", "ss2": "#f46d43", "flkL": "#4393c3",
                     "flkR": "#74add1", "other": "#bababa"}

    # ── Figure 1: Q1 ranking percentiles (masked vs full-seq) ─────────────────
    # One subplot per anchor head. Bars = proteins, showing masked and full-seq
    # rank percentile (100% = rank 1 = best).

    n_heads = len(anchor_heads)
    fig1, axes1 = plt.subplots(1, n_heads, figsize=(5 * n_heads, 4.5), sharey=True)
    if n_heads == 1:
        axes1 = [axes1]

    for ax, (layer, head) in zip(axes1, anchor_heads):
        hname = f"L{layer}H{head}"
        rows = [(p, all_results[(p, layer, head)]) for p in proteins if (p, layer, head) in all_results]
        if not rows:
            ax.set_visible(False)
            continue

        pnames = [p for p, _ in rows]
        q1_m = [r["q1"] for _, r in rows]
        q1_f = [r["q1_full"] for _, r in rows]

        # Use first anchor per protein for ranking
        def get_pct(q1_dict, which):
            r = q1_dict
            if not r["anchor_ranks_all"]:
                return float("nan")
            tok_pos = list(r["anchor_ranks_all"].keys())[0]
            rank = r[which].get(tok_pos, None)
            n = r["n_residues"] if which == "anchor_ranks_all" else r["n_unmasked"]
            if rank is None or not n:
                return float("nan")
            return 100.0 * (1.0 - rank / n)

        pct_masked = [100.0 * (1.0 - list(q["anchor_ranks_all"].values())[0] / q["n_residues"])
                      if q["anchor_ranks_all"] else float("nan") for q in q1_m]
        pct_full   = [100.0 * (1.0 - list(q["anchor_ranks_all"].values())[0] / q["n_residues"])
                      if q["anchor_ranks_all"] else float("nan") for q in q1_f]

        x = np.arange(len(pnames))
        w = 0.38
        ax.bar(x - w/2, pct_masked, w, color=COLORS["masked"], label="masked ctx", zorder=3)
        ax.bar(x + w/2, pct_full,   w, color=COLORS["full"],   label="full seq",  zorder=3, edgecolor="#888", linewidth=0.6)

        ax.axhline(95, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(pnames, rotation=40, ha="right", fontsize=8)
        ax.set_ylim(0, 105)
        ax.set_ylabel("rank percentile (higher = anchor wins)")
        ax.set_title(f"{hname}\nanchor key rank percentile", fontsize=9)
        ax.set_xlabel("protein")
        ax.grid(axis="y", alpha=0.3, zorder=0)
        if ax is axes1[0]:
            ax.legend(fontsize=8)

    fig1.suptitle("Q1: Anchor key ranks among all positions via pre-RoPE q\u00b7k score\n"
                  "(masked ctx = circuit context; dashed line = 95th pct)", fontsize=10)
    fig1.tight_layout()
    p1 = out_dir / "anchor_interp_v2_q1_rankings.png"
    fig1.savefig(p1, dpi=150, bbox_inches="tight")
    plt.close(fig1)
    print(f"Saved {p1}")

    # ── Figure 2: Cross-protein search direction consistency ──────────────────
    # Left: mean pairwise cosine per head (masked context q_mean)
    # Right: q_mean_norm per head (how aligned are all queries)

    fig2, (ax2a, ax2b) = plt.subplots(1, 2, figsize=(9, 4))

    hnames = [f"L{l}H{h}" for l, h in anchor_heads]

    mean_cos_vals = []
    std_cos_vals = []
    mean_norm_vals = []
    for layer, head in anchor_heads:
        q_means = {p: all_results[(p, layer, head)]["q1"]["q_mean_d"]
                   for p in proteins if (p, layer, head) in all_results}
        names = sorted(q_means.keys())
        cos_list = []
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                cos_list.append(F.cosine_similarity(
                    q_means[names[i]].unsqueeze(0), q_means[names[j]].unsqueeze(0)).item())
        mean_cos_vals.append(np.mean(cos_list) if cos_list else float("nan"))
        std_cos_vals.append(np.std(cos_list) if cos_list else 0.0)

        norms = [all_results[(p, layer, head)]["q1"]["q_mean_norm"]
                 for p in proteins if (p, layer, head) in all_results]
        mean_norm_vals.append(np.mean(norms) if norms else float("nan"))

    x = np.arange(len(hnames))
    bars = ax2a.bar(x, mean_cos_vals, color=["#4393c3", "#2166ac", "#92c5de"][:len(hnames)],
                    yerr=std_cos_vals, capsize=4, zorder=3)
    ax2a.set_xticks(x)
    ax2a.set_xticklabels(hnames)
    ax2a.set_ylim(0, 1.05)
    ax2a.axhline(0.9, color="black", linestyle="--", linewidth=0.8, alpha=0.5, label="0.9 threshold")
    ax2a.set_ylabel("mean pairwise cosine similarity")
    ax2a.set_title("Search direction consistency across proteins\n"
                   "(high = head looks for same thing in every protein)", fontsize=9)
    ax2a.legend(fontsize=8)
    ax2a.grid(axis="y", alpha=0.3, zorder=0)
    for bar, val in zip(bars, mean_cos_vals):
        ax2a.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                  f"{val:.3f}", ha="center", va="bottom", fontsize=8)

    bars2 = ax2b.bar(x, mean_norm_vals, color=["#4393c3", "#2166ac", "#92c5de"][:len(hnames)], zorder=3)
    ax2b.set_xticks(x)
    ax2b.set_xticklabels(hnames)
    ax2b.set_ylim(0, 1.05)
    ax2b.axhline(1.0, color="gray", linestyle=":", linewidth=0.8, alpha=0.5, label="max (all queries aligned)")
    ax2b.set_ylabel("q_mean_norm (mean of unit queries)")
    ax2b.set_title("Query alignment within each protein\n"
                   "(close to 1.0 = all query vectors point the same direction)", fontsize=9)
    ax2b.legend(fontsize=8)
    ax2b.grid(axis="y", alpha=0.3, zorder=0)
    for bar, val in zip(bars2, mean_norm_vals):
        ax2b.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                  f"{val:.3f}", ha="center", va="bottom", fontsize=8)

    fig2.suptitle("Q1: These heads look for the same feature in every protein\n"
                  "(cross-protein q_mean cosine and within-protein query alignment)", fontsize=10)
    fig2.tight_layout()
    p2 = out_dir / "anchor_interp_v2_q1_consistency.png"
    fig2.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    print(f"Saved {p2}")

    # ── Figure 3: Q2 OV region distribution (stacked bars) ───────────────────
    # One subplot per anchor head. Each row = a protein.

    fig3, axes3 = plt.subplots(1, n_heads, figsize=(5 * n_heads, 5), sharey=False)
    if n_heads == 1:
        axes3 = [axes3]

    regions_ordered = ["ss1", "ss2", "flkL", "flkR", "other"]

    for ax, (layer, head) in zip(axes3, anchor_heads):
        hname = f"L{layer}H{head}"
        rows = [(p, all_results[(p, layer, head)]["q2"]["region_attn"])
                for p in proteins if (p, layer, head) in all_results]
        if not rows:
            ax.set_visible(False)
            continue

        pnames = [p for p, _ in rows]
        fracs = []
        for _, ratd in rows:
            total = sum(ratd.values())
            fracs.append({r: ratd.get(r, 0) / total if total else 0 for r in regions_ordered})

        y = np.arange(len(pnames))
        lefts = np.zeros(len(pnames))
        for reg in regions_ordered:
            vals = [f[reg] for f in fracs]
            ax.barh(y, vals, left=lefts, color=REGION_COLORS[reg], label=reg, height=0.6)
            lefts += np.array(vals)

        ax.set_yticks(y)
        ax.set_yticklabels(pnames, fontsize=8)
        ax.set_xlim(0, 1)
        ax.set_xlabel("fraction of total attention to anchor key")
        ax.set_title(f"{hname}\nwhere OV output is broadcast", fontsize=9)
        ax.grid(axis="x", alpha=0.3)
        if ax is axes3[0]:
            ax.legend(loc="lower right", fontsize=7, title="region")

    fig3.suptitle("Q2: Where does the anchor head write its OV output?\n"
                  "(attention column for anchor key — receivers of the OV message)", fontsize=10)
    fig3.tight_layout()
    p3 = out_dir / "anchor_interp_v2_q2_ov_regions.png"
    fig3.savefig(p3, dpi=150, bbox_inches="tight")
    plt.close(fig3)
    print(f"Saved {p3}")

    # ── Figure 4: Q2 OV cross-protein cosine heatmaps ────────────────────────
    # One heatmap per head.

    fig4, axes4 = plt.subplots(1, n_heads, figsize=(4.5 * n_heads, 4))
    if n_heads == 1:
        axes4 = [axes4]

    for ax, (layer, head) in zip(axes4, anchor_heads):
        hname = f"L{layer}H{head}"
        vecs = {p: ov_outputs[(p, layer, head)] for p in proteins if (p, layer, head) in ov_outputs}
        names = sorted(vecs.keys())
        n = len(names)
        if n < 2:
            ax.set_visible(False)
            continue

        mat = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                mat[i, j] = F.cosine_similarity(
                    vecs[names[i]].unsqueeze(0), vecs[names[j]].unsqueeze(0)).item()

        im = ax.imshow(mat, vmin=-0.6, vmax=1.0, cmap="RdBu_r", aspect="auto")
        ax.set_xticks(range(n))
        ax.set_yticks(range(n))
        ax.set_xticklabels(names, rotation=45, ha="right", fontsize=7)
        ax.set_yticklabels(names, fontsize=7)
        for i in range(n):
            for j in range(n):
                ax.text(j, i, f"{mat[i,j]:.2f}", ha="center", va="center", fontsize=6,
                        color="white" if abs(mat[i, j]) > 0.5 else "black")
        fig4.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        mean_off = np.mean([mat[i, j] for i in range(n) for j in range(i+1, n)])
        ax.set_title(f"{hname}  (mean off-diag cos = {mean_off:.2f})\n", fontsize=9)

    fig4.suptitle("Q2: OV outputs are protein-specific, not a universal feature\n"
                  "(pairwise cosine of anchor OV output vectors across proteins)", fontsize=10)
    fig4.tight_layout()
    p4 = out_dir / "anchor_interp_v2_q2_ov_similarity.png"
    fig4.savefig(p4, dpi=150, bbox_inches="tight")
    plt.close(fig4)
    print(f"Saved {p4}")

    # ── Figure 5: OV -> L32H13 projection norms ──────────────────────────────
    # Grouped bars per protein: k_delta_norm and q_delta_norm for each anchor head.
    # Only for the first interaction head.

    if not interaction_heads_list:
        return
    il, ih = interaction_heads_list[0]
    iname = f"L{il}H{ih}"

    fig5, axes5 = plt.subplots(1, n_heads, figsize=(5 * n_heads, 4.5), sharey=True)
    if n_heads == 1:
        axes5 = [axes5]

    for ax, (layer, head) in zip(axes5, anchor_heads):
        hname = f"L{layer}H{head}"
        rows = [(p, all_results[(p, layer, head)]) for p in proteins if (p, layer, head) in all_results]
        if not rows:
            ax.set_visible(False)
            continue

        pnames = [p for p, _ in rows]
        k_norms, q_norms = [], []
        for _, r in rows:
            probes = r["q2"]["interaction_probes"]
            if (il, ih) in probes:
                k_norms.append(probes[(il, ih)]["k_delta_norm"])
                q_norms.append(probes[(il, ih)]["q_delta_norm"])
            else:
                k_norms.append(0.0)
                q_norms.append(0.0)

        x = np.arange(len(pnames))
        w = 0.38
        ax.bar(x - w/2, k_norms, w, color="#d73027", label="k_delta_norm", zorder=3)
        ax.bar(x + w/2, q_norms, w, color="#4393c3", label="q_delta_norm", zorder=3)
        ax.set_xticks(x)
        ax.set_xticklabels(pnames, rotation=40, ha="right", fontsize=8)
        ax.set_ylabel(f"||W_{'{K/Q}'}  @ ov_output|| ({iname})")
        ax.set_title(f"{hname} \u2192 {iname}\nOV output projection", fontsize=9)
        ax.grid(axis="y", alpha=0.3, zorder=0)
        if ax is axes5[0]:
            ax.legend(fontsize=8)

    fig5.suptitle(f"Q2: Anchor OV output substantially enters {iname} key/query space\n"
                  "(how much the OV vector shifts keys and queries at the interaction head)", fontsize=10)
    fig5.tight_layout()
    p5 = out_dir / "anchor_interp_v2_q2_projection.png"
    fig5.savefig(p5, dpi=150, bbox_inches="tight")
    plt.close(fig5)
    print(f"Saved {p5}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def parse_head_list(s: str) -> tuple[int, int]:
    parts = s.split(",")
    return (int(parts[0]), int(parts[1]))


def main():
    parser = argparse.ArgumentParser(description="Anchor QK and OV analysis")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument(
        "--heads", nargs="+", type=parse_head_list, default=DEFAULT_ANCHOR_HEADS,
        metavar="L,H",
        help="Anchor heads to analyze, e.g. --heads 11,16 10,9",
    )
    parser.add_argument(
        "--interaction-heads", nargs="+", type=parse_head_list, default=DEFAULT_INTERACTION_HEADS,
        metavar="L,H",
        help="Interaction heads for OV projection, e.g. --interaction-heads 32,13",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
