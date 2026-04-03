#!/usr/bin/env python3
"""Anchor feature identification (Experiment 3_24_anchor_interp_v3).

Part A: Layer-wise decomposition of anchor projection score onto the L10H9 search
direction. Captures the additive contribution of each model component (embedding,
per-layer attention outputs, per-layer MLP outputs, layers 0-9) and projects each
onto the search direction. Residual stream decomposition is exact (linear).

Part B: SAE latent alignment with the search direction. Finds InterProt SAE latents
(at layers 4 and 8) whose decoder directions are most cosine-aligned with the search
direction. Checks whether top-aligned latents actually activate on anchor positions.

Usage:
    uv run python scripts/anchor_interp_v3.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
sys.path.insert(0, str(ROOT))

from helpers.utils import load_sae_prot

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
SEGMENT_RADIUS = 5
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"

# Hardcoded anchor positions (0-indexed) from experiment 3_24 results
ANCHOR_POSITIONS = {
    "1BRTA": 220,  # L
    "1PVGA": 101,  # V
    "2B61A": 315,  # T
    "2DPMA": 39,   # F
    "2PKEA": 131,  # L
}
REFERENCE_PROTEIN = "2B61A"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    return protein_configs, seqs


def build_clean_sequence(sequence: str, config: dict) -> tuple[str, list[bool]]:
    """Build the clean masked sequence for the contact jump experiment."""
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_start, ss1_end = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_start, ss2_end = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1

    masked: list[str] = ["<mask>"] * n
    for i in range(ss1_start, ss1_end):
        masked[i] = sequence[i]
    for i in range(ss2_start, ss2_end):
        masked[i] = sequence[i]
    for i in range(max(0, ss1_start - flank), ss1_start):
        masked[i] = sequence[i]
    for i in range(ss2_end, min(n, ss2_end + flank)):
        masked[i] = sequence[i]

    is_unmasked = [c != "<mask>" for c in masked]
    return "".join(masked), is_unmasked


# ---------------------------------------------------------------------------
# Model loading and weight extraction
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
    """Extract W_Q and W_K for a specific layer and head."""
    attn = model._model.esm.encoder.layer[layer].attention
    W_Q = attn.self.query.weight.data.cpu()  # (1280, 1280)
    b_Q = attn.self.query.bias.data.cpu()
    W_K = attn.self.key.weight.data.cpu()  # (1280, 1280)
    b_K = attn.self.key.bias.data.cpu()
    W_Q_heads = W_Q.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_Q_heads = b_Q.reshape(NUM_HEADS, HEAD_DIM)
    W_K_heads = W_K.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_K_heads = b_K.reshape(NUM_HEADS, HEAD_DIM)
    return {
        "W_Q_hd": W_Q_heads[head].clone(),  # (64, 1280)
        "b_Q_d": b_Q_heads[head].clone(),
        "W_K_hd": W_K_heads[head].clone(),  # (64, 1280)
        "b_K_d": b_K_heads[head].clone(),
    }


# ---------------------------------------------------------------------------
# Search direction computation
# ---------------------------------------------------------------------------

def compute_search_dir(model, tokenizer, sequence: str, weights: dict, device: str) -> torch.Tensor:
    """Compute the L10H9 search direction in residual stream space.

    Uses the mean unit query direction across all positions in the clean masked sequence,
    then maps to key-side residual stream space via W_K^T. This is the direction that
    identifies which residues the head attends to (key selection), not what the head asks (query).

    Returns search_dir: (1280,) on CPU.
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm

    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])

    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln_LD = cache[key].output.detach().cpu()[0]  # (seq_len, 1280)

    W_Q = weights["W_Q_hd"]  # (64, 1280)
    b_Q = weights["b_Q_d"]
    W_K = weights["W_K_hd"]  # (64, 1280)

    q_all_Ld = x_ln_LD @ W_Q.T + b_Q.unsqueeze(0)  # (seq_len, 64)
    q_residues = q_all_Ld[1:-1]  # exclude BOS and EOS
    q_norms = q_residues.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_unit = q_residues / q_norms  # (n_residues, 64)
    q_mean_d = q_unit.mean(dim=0)  # (64,)

    q_mean_normalized = q_mean_d / q_mean_d.norm().clamp(min=1e-8)
    search_dir = W_K.T @ q_mean_normalized  # (1280,)
    return search_dir


# ---------------------------------------------------------------------------
# Part A: Layer-wise decomposition
# ---------------------------------------------------------------------------

def capture_component_contributions(model, tokenizer, sequence: str, device: str) -> dict:
    """Run forward pass and capture additive contributions of each model component.

    Returns dict with:
        "embed":     (seq_len, 1280) — initial embedding (token + position, after LN)
        "attn_L{l}": (seq_len, 1280) — additive attention contribution at layer l
        "mlp_L{l}":  (seq_len, 1280) — additive MLP contribution at layer l
    All tensors are on CPU.

    Architecture note:
        ESM2 uses pre-norm (sandwich-norm):
            x_l+1 = x_l + attn_dense(LN(x_l)) + mlp_dense(LN2(x_l + attn_dense(LN(x_l))))
        The additive attention contribution is captured at:
            model.esm.encoder.layer[l].attention.output.dense
        which is the final linear projection inside EsmSelfOutput (before dropout + residual add).
        The additive MLP contribution is captured at:
            model.esm.encoder.layer[l].output.dense
        which is the final linear projection inside EsmOutput (before dropout + residual add).
        In eval mode, dropout = 0, so the dense output equals the additive contribution exactly.
    """
    inputs = tokenizer(sequence, return_tensors="pt").to(device)

    embed_mod = model.esm.embeddings
    attn_dense_mods = [model.esm.encoder.layer[l].attention.output.dense for l in range(10)]
    mlp_dense_mods = [model.esm.encoder.layer[l].output.dense for l in range(10)]

    all_modules = [embed_mod] + attn_dense_mods + mlp_dense_mods

    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=all_modules)

    result = {}
    result["embed"] = cache["model.esm.embeddings"].output.detach().cpu()[0]  # (seq_len, 1280)
    for l in range(10):
        attn_key = f"model.esm.encoder.layer.{l}.attention.output.dense"
        mlp_key = f"model.esm.encoder.layer.{l}.output.dense"
        result[f"attn_L{l}"] = cache[attn_key].output.detach().cpu()[0]
        result[f"mlp_L{l}"] = cache[mlp_key].output.detach().cpu()[0]
    return result


def part_a_decomposition(model, tokenizer, protein_configs, seqs, weights, search_dir, device):
    """Run Part A for all proteins and return per-protein decomposition results."""
    print("\n=== Part A: Layer-wise decomposition ===")
    search_dir_unit = search_dir / search_dir.norm().clamp(min=1e-8)

    components = ["embed"] + [f"attn_L{l}" for l in range(10)] + [f"mlp_L{l}" for l in range(10)]

    all_results = {}
    for protein, anchor_pos_0idx in ANCHOR_POSITIONS.items():
        if protein not in protein_configs or protein not in seqs:
            print(f"  Skipping {protein}: missing config or sequence")
            continue
        config = protein_configs[protein]
        sequence = seqs[protein]
        clean_seq, is_unmasked = build_clean_sequence(sequence, config)
        anchor_tok_pos = anchor_pos_0idx + 1  # +1 for BOS

        print(f"  {protein}: anchor seq_pos={anchor_pos_0idx} ({sequence[anchor_pos_0idx]}), tok_pos={anchor_tok_pos}")

        contribs = capture_component_contributions(model, tokenizer, clean_seq, device)

        # Projection of each component's contribution at anchor position
        anchor_scores = {}
        for comp in components:
            v = contribs[comp][anchor_tok_pos]
            anchor_scores[comp] = (v @ search_dir_unit).item()

        # Verify linearity: sum of components = total residual stream projection
        x_10_anchor = sum(contribs[comp][anchor_tok_pos] for comp in components)
        sum_score = sum(anchor_scores.values())
        direct_score = (x_10_anchor @ search_dir_unit).item()
        print(f"    Linearity check — sum of parts: {sum_score:.4f}, direct x_10 dot search_dir: {direct_score:.4f}, gap: {abs(sum_score - direct_score):.2e}")

        # Pick control: unmasked position with the lowest projection score
        # Compute total residual (sum of all components) projection for each unmasked position
        unmasked_tok_positions = [i + 1 for i, flag in enumerate(is_unmasked) if flag and (i + 1) != anchor_tok_pos]
        if unmasked_tok_positions:
            pos_scores = []
            for tp in unmasked_tok_positions:
                x_tp = sum(contribs[comp][tp] for comp in components)
                pos_scores.append((tp, (x_tp @ search_dir_unit).item()))
            pos_scores.sort(key=lambda t: t[1])  # ascending: lowest projection first
            control_tok_pos = pos_scores[0][0]
        else:
            # fallback: use a position near ss2
            pos1, pos2 = config["contact_pair"]
            control_tok_pos = min(pos2 + 3, len(sequence) - 2) + 1

        control_pos_0idx = control_tok_pos - 1

        control_scores = {}
        for comp in components:
            v = contribs[comp][control_tok_pos]
            control_scores[comp] = (v @ search_dir_unit).item()

        print(f"    Control: seq_pos={control_pos_0idx} ({sequence[control_pos_0idx]}), total proj={sum(control_scores.values()):.4f}")

        all_results[protein] = {
            "anchor_scores": anchor_scores,
            "control_scores": control_scores,
            "anchor_pos": anchor_pos_0idx,
            "anchor_aa": sequence[anchor_pos_0idx],
            "control_pos": control_pos_0idx,
            "control_aa": sequence[control_pos_0idx],
            "anchor_total": sum_score,
            "control_total": sum(control_scores.values()),
        }

    return all_results, components


def plot_part_a(results: dict, components: list, output_dir: Path) -> None:
    proteins = list(results.keys())
    n_proteins = len(proteins)
    n_comp = len(components)
    x = np.arange(n_comp)
    width = 0.35

    fig, axes = plt.subplots(n_proteins, 1, figsize=(max(16, n_comp * 0.55), 3.5 * n_proteins), squeeze=False)
    for i, protein in enumerate(proteins):
        ax = axes[i, 0]
        r = results[protein]
        anchor_vals = [r["anchor_scores"][c] for c in components]
        control_vals = [r["control_scores"][c] for c in components]

        ax.bar(x - width / 2, anchor_vals, width, label=f"anchor {r['anchor_aa']}{r['anchor_pos']}", color="steelblue", alpha=0.85)
        ax.bar(x + width / 2, control_vals, width, label=f"control {r['control_aa']}{r['control_pos']}", color="coral", alpha=0.85)
        ax.axhline(0, color="black", linewidth=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(components, rotation=45, ha="right", fontsize=7)
        ax.set_title(f"{protein}: component projections onto L10H9 search direction")
        ax.set_ylabel("Projection score")
        ax.legend(fontsize=8)

    plt.tight_layout()
    out_path = output_dir / "anchor_layerwise_decomp.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {out_path}")


def write_part_a_report(results: dict, components: list, output_dir: Path) -> None:
    proteins = list(results.keys())
    lines = []
    lines.append("# Anchor Layer-wise Decomposition (Part A)\n\n")
    lines.append(f"Reference protein for search direction: {REFERENCE_PROTEIN}\n")
    lines.append("Search direction: L10H9 mean query direction mapped to residual stream space via W_Q^T.\n")
    lines.append("Each value is the dot product of that component's additive contribution to the residual stream with the unit search direction.\n")
    lines.append("The sum across all components equals the total residual stream projection exactly (linear decomposition).\n\n")

    # Wide table: one row per protein/position combo
    header_cols = ["Protein", "Position"] + components + ["Sum"]
    lines.append("| " + " | ".join(header_cols) + " |\n")
    lines.append("|" + "---|" * len(header_cols) + "\n")

    for protein in proteins:
        r = results[protein]
        anchor_vals = [f"{r['anchor_scores'][c]:.3f}" for c in components]
        anchor_sum = f"{r['anchor_total']:.3f}"
        lines.append(f"| {protein} | anchor {r['anchor_aa']}{r['anchor_pos']} | " + " | ".join(anchor_vals) + f" | {anchor_sum} |\n")
        control_vals = [f"{r['control_scores'][c]:.3f}" for c in components]
        control_sum = f"{r['control_total']:.3f}"
        lines.append(f"| {protein} | control {r['control_aa']}{r['control_pos']} | " + " | ".join(control_vals) + f" | {control_sum} |\n")

    lines.append("\n## Average projection per component (anchor vs control, across proteins)\n\n")
    avg_anchor = {c: np.mean([results[p]["anchor_scores"][c] for p in proteins]) for c in components}
    avg_control = {c: np.mean([results[p]["control_scores"][c] for p in proteins]) for c in components}

    sorted_by_diff = sorted(components, key=lambda c: avg_anchor[c] - avg_control[c], reverse=True)
    lines.append("| Component | Avg anchor | Avg control | Anchor - control |\n")
    lines.append("|-----------|-----------|-------------|------------------|\n")
    for c in sorted_by_diff:
        diff = avg_anchor[c] - avg_control[c]
        lines.append(f"| {c} | {avg_anchor[c]:.3f} | {avg_control[c]:.3f} | {diff:+.3f} |\n")

    out_path = output_dir / "anchor_layerwise_decomp.md"
    with open(out_path, "w") as f:
        f.writelines(lines)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Part B: SAE alignment
# ---------------------------------------------------------------------------

def part_b_sae_alignment(model, tokenizer, protein_configs, seqs, search_dir, device):
    """Run Part B: SAE decoder alignment with search direction and anchor activation check."""
    print("\n=== Part B: SAE latent alignment ===")
    search_dir_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).to(device)

    sae_results = {}
    for sae_layer in [4, 8]:
        print(f"  Loading SAE at layer {sae_layer}...")
        sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=sae_layer, device=device)
        sae.eval()

        # w_dec shape: (4096, 1280) — each ROW is a decoder direction in R^1280
        w_dec = sae.w_dec.data  # (4096, 1280)
        row_norms = w_dec.norm(dim=1, keepdim=True).clamp(min=1e-8)
        w_dec_unit = w_dec / row_norms  # (4096, 1280) row-normalized

        alignment = (w_dec_unit @ search_dir_unit).cpu()  # (4096,)

        top20_vals, top20_idx = alignment.topk(20)
        bot20_vals, bot20_idx = alignment.topk(20, largest=False)

        sae_results[sae_layer] = {
            "sae": sae,
            "alignment": alignment,
            "top20_idx": top20_idx.tolist(),
            "top20_vals": top20_vals.tolist(),
            "bot20_idx": bot20_idx.tolist(),
            "bot20_vals": bot20_vals.tolist(),
        }
        print(f"    Top cosine: {top20_vals[0].item():.4f} (latent {top20_idx[0].item()})")
        print(f"    Min cosine: {bot20_vals[0].item():.4f} (latent {bot20_idx[0].item()})")

    # Activation check: top-5 layer-8 latents at anchor positions across proteins
    top5_idx_l8 = sae_results[8]["top20_idx"][:5]
    sae_l8 = sae_results[8]["sae"]
    print(f"  Checking layer-8 top-5 latents {top5_idx_l8} at anchor positions...")

    anchor_acts = {}
    for protein, anchor_pos_0idx in ANCHOR_POSITIONS.items():
        if protein not in protein_configs or protein not in seqs:
            continue
        config = protein_configs[protein]
        sequence = seqs[protein]
        clean_seq, _ = build_clean_sequence(sequence, config)
        anchor_tok_pos = anchor_pos_0idx + 1

        inputs = tokenizer(clean_seq, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model._model.esm(**inputs, output_hidden_states=True)
        # hidden_states[sae_layer] matches the convention in interprot_sae_viz.py
        hidden_at_layer = out.hidden_states[sae_layer]  # (1, seq_len, 1280)
        x_anchor = hidden_at_layer[:, anchor_tok_pos:anchor_tok_pos + 1, :]  # (1, 1, 1280)
        acts = sae_l8.get_acts(x_anchor)  # (1, 1, 4096)
        acts_flat = acts[0, 0].cpu()  # (4096,)

        anchor_acts[protein] = {idx: acts_flat[idx].item() for idx in top5_idx_l8}
        act_strs = ", ".join(f"L{idx}={anchor_acts[protein][idx]:.3f}" for idx in top5_idx_l8)
        print(f"    {protein}: {act_strs}")

    sae_results["anchor_acts_top5_l8"] = anchor_acts
    sae_results["top5_idx_l8"] = top5_idx_l8
    return sae_results


def write_part_b_report(sae_results: dict, output_dir: Path) -> None:
    lines = []
    lines.append("# Anchor SAE Alignment (Part B)\n\n")
    lines.append("Cosine similarity between each SAE decoder direction (row of w_dec, row-normalized) and the L10H9 search direction.\n")
    lines.append(f"Search direction from {REFERENCE_PROTEIN} clean masked sequence.\n\n")

    for sae_layer in [8, 4]:
        r = sae_results[sae_layer]
        lines.append(f"## Layer {sae_layer} SAE — top 20 most aligned latents\n\n")
        lines.append("| Rank | Latent | Cosine |\n")
        lines.append("|------|--------|--------|\n")
        for rank, (idx, val) in enumerate(zip(r["top20_idx"], r["top20_vals"]), 1):
            lines.append(f"| {rank} | {idx} | {val:.4f} |\n")
        lines.append("\n")

        lines.append(f"## Layer {sae_layer} SAE — top 20 most anti-aligned latents\n\n")
        lines.append("| Rank | Latent | Cosine |\n")
        lines.append("|------|--------|--------|\n")
        for rank, (idx, val) in enumerate(zip(r["bot20_idx"], r["bot20_vals"]), 1):
            lines.append(f"| {rank} | {idx} | {val:.4f} |\n")
        lines.append("\n")

    top20_l4 = set(sae_results[4]["top20_idx"])
    top20_l8 = set(sae_results[8]["top20_idx"])
    overlap = sorted(top20_l4 & top20_l8)
    only_l4 = sorted(top20_l4 - top20_l8)
    only_l8 = sorted(top20_l8 - top20_l4)

    lines.append("## Overlap between layer 4 and layer 8 top-20\n\n")
    lines.append(f"In top-20 at both layers: {overlap if overlap else 'none'}\n\n")
    lines.append(f"Only in layer 4 top-20: {only_l4}\n\n")
    lines.append(f"Only in layer 8 top-20: {only_l8}\n\n")

    top5_idx = sae_results["top5_idx_l8"]
    anchor_acts = sae_results["anchor_acts_top5_l8"]
    lines.append("## Layer-8 top-5 latent activations at anchor positions\n\n")
    top5_cosines = {idx: sae_results[8]["top20_vals"][i] for i, idx in enumerate(top5_idx)}
    lines.append("Cosines: " + ", ".join(f"L{idx}={top5_cosines[idx]:.4f}" for idx in top5_idx) + "\n\n")
    lines.append("| Protein | " + " | ".join(f"Latent {idx}" for idx in top5_idx) + " |\n")
    lines.append("|---------|" + "---------|" * len(top5_idx) + "\n")
    for protein, acts in anchor_acts.items():
        vals = [f"{acts[idx]:.4f}" for idx in top5_idx]
        lines.append(f"| {protein} | " + " | ".join(vals) + " |\n")

    out_path = output_dir / "anchor_sae_alignment.md"
    with open(out_path, "w") as f:
        f.writelines(lines)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Part B (continued): Differential activation analysis
# ---------------------------------------------------------------------------

def part_b_differential_activation(model, tokenizer, protein_configs, seqs, device, sae_layer: int = 8, top_k: int = 20):
    """Find SAE latents with highest differential activation at anchor vs non-anchor positions.

    For each latent: compute mean activation at anchor positions (across proteins) minus
    mean activation at non-anchor unmasked positions (within the same clean masked sequence).
    This identifies latents that specifically detect the anchor feature rather than latents
    that fire broadly at high rates everywhere.

    Uses the same clean masked sequence as the rest of the analysis (same circuit context).
    Non-anchor baseline: all unmasked positions in the clean sequence except the anchor itself.
    """
    print(f"\n=== Part B (differential): anchor vs non-anchor SAE activations at layer {sae_layer} ===")
    sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=sae_layer, device=device)
    sae.eval()

    # Per-protein: anchor activation vector and mean non-anchor activation vector
    per_protein_anchor = {}    # protein -> (4096,) tensor on CPU
    per_protein_nonanchor = {}  # protein -> (4096,) tensor on CPU (mean over non-anchor positions)

    for protein, anchor_pos_0idx in ANCHOR_POSITIONS.items():
        if protein not in protein_configs or protein not in seqs:
            print(f"  Skipping {protein}: missing config or sequence")
            continue
        config = protein_configs[protein]
        sequence = seqs[protein]
        clean_seq, is_unmasked = build_clean_sequence(sequence, config)
        anchor_tok_pos = anchor_pos_0idx + 1  # +1 for BOS

        if not is_unmasked[anchor_pos_0idx]:
            print(f"  WARNING: anchor pos {anchor_pos_0idx} is masked in {protein} — skipping")
            continue

        inputs = tokenizer(clean_seq, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model._model.esm(**inputs, output_hidden_states=True)
        # hidden_states[sae_layer] matches interprot_sae_viz.py convention
        hidden = out.hidden_states[sae_layer]  # (1, seq_len, 1280)

        # Run SAE on all positions at once; get_acts handles arbitrary leading dims
        acts_all = sae.get_acts(hidden)[0].cpu()  # (seq_len, 4096)

        anchor_act = acts_all[anchor_tok_pos]  # (4096,)

        nonanchor_tok_positions = [i + 1 for i, flag in enumerate(is_unmasked)
                                   if flag and i != anchor_pos_0idx]
        if not nonanchor_tok_positions:
            print(f"  WARNING: no non-anchor unmasked positions for {protein} — skipping")
            continue
        nonanchor_mean = acts_all[torch.tensor(nonanchor_tok_positions)].mean(dim=0)  # (4096,)

        n_nonanchor = len(nonanchor_tok_positions)
        anchor_total = anchor_act.sum().item()
        nonanchor_total = nonanchor_mean.sum().item()
        print(f"  {protein}: anchor tok_pos={anchor_tok_pos}, n_nonanchor={n_nonanchor}, "
              f"anchor_sum_act={anchor_total:.1f}, nonanchor_mean_sum_act={nonanchor_total:.1f}")

        per_protein_anchor[protein] = anchor_act
        per_protein_nonanchor[protein] = nonanchor_mean

    proteins_used = list(per_protein_anchor.keys())
    if not proteins_used:
        print("  No valid proteins — skipping differential analysis")
        return {}

    # Average across proteins
    mean_anchor = torch.stack([per_protein_anchor[p] for p in proteins_used]).mean(dim=0)   # (4096,)
    mean_nonanchor = torch.stack([per_protein_nonanchor[p] for p in proteins_used]).mean(dim=0)  # (4096,)
    differential = mean_anchor - mean_nonanchor  # (4096,)

    top_vals, top_idx = differential.topk(top_k)

    print(f"  Top differential latents (anchor_mean - nonanchor_mean):")
    for rank, (idx, val) in enumerate(zip(top_idx.tolist(), top_vals.tolist()), 1):
        anchor_mean_val = mean_anchor[idx].item()
        nonanchor_mean_val = mean_nonanchor[idx].item()
        print(f"    {rank:2d}. latent {idx:4d}: diff={val:.3f}  anchor_mean={anchor_mean_val:.3f}  nonanchor_mean={nonanchor_mean_val:.3f}")

    return {
        "sae_layer": sae_layer,
        "proteins_used": proteins_used,
        "per_protein_anchor": per_protein_anchor,
        "per_protein_nonanchor": per_protein_nonanchor,
        "mean_anchor": mean_anchor,
        "mean_nonanchor": mean_nonanchor,
        "differential": differential,
        "top_idx": top_idx.tolist(),
        "top_vals": top_vals.tolist(),
    }


def write_part_b_differential_report(diff_results: dict, output_dir: Path) -> None:
    if not diff_results:
        return
    sae_layer = diff_results["sae_layer"]
    proteins_used = diff_results["proteins_used"]
    top_idx = diff_results["top_idx"]
    top_vals = diff_results["top_vals"]
    mean_anchor = diff_results["mean_anchor"]
    mean_nonanchor = diff_results["mean_nonanchor"]
    per_protein_anchor = diff_results["per_protein_anchor"]
    per_protein_nonanchor = diff_results["per_protein_nonanchor"]

    lines = []
    lines.append("# Anchor Differential SAE Activation (Part B continued)\n\n")
    lines.append(f"Layer {sae_layer} SAE. For each latent: mean activation at anchor positions "
                 f"(across {len(proteins_used)} proteins) minus mean activation at non-anchor unmasked "
                 f"positions within the same clean masked sequence.\n")
    lines.append("Non-anchor baseline: all unmasked positions in the clean sequence except the anchor itself.\n\n")

    lines.append("## Top 20 differentially active latents\n\n")
    lines.append("| Rank | Latent | Anchor mean | Non-anchor mean | Differential |")
    for p in proteins_used:
        lines.append(f" {p} anchor | {p} non-anchor |")
    lines.append("\n")
    lines.append("|------|--------|-------------|-----------------|--------------|")
    for _ in proteins_used:
        lines.append("---------|---------|")
    lines.append("\n")

    for rank, (idx, diff_val) in enumerate(zip(top_idx, top_vals), 1):
        anchor_mean_val = mean_anchor[idx].item()
        nonanchor_mean_val = mean_nonanchor[idx].item()
        row = f"| {rank} | {idx} | {anchor_mean_val:.3f} | {nonanchor_mean_val:.3f} | {diff_val:.3f} |"
        for p in proteins_used:
            a_val = per_protein_anchor[p][idx].item()
            na_val = per_protein_nonanchor[p][idx].item()
            row += f" {a_val:.3f} | {na_val:.3f} |"
        lines.append(row + "\n")

    out_path = output_dir / "anchor_sae_differential.md"
    with open(out_path, "w") as f:
        f.writelines(lines)
    print(f"  Saved: {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading configs and sequences...")
    protein_configs, seqs = load_configs()

    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    print("Extracting L10H9 weights...")
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    # Compute search direction from 2B61A clean masked sequence
    print(f"Computing search direction from {REFERENCE_PROTEIN}...")
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_config = protein_configs[REFERENCE_PROTEIN]
    ref_clean_seq, _ = build_clean_sequence(ref_seq, ref_config)
    search_dir = compute_search_dir(model, tokenizer, ref_clean_seq, weights, args.device)
    print(f"  Search direction norm: {search_dir.norm().item():.4f}")

    # Part A
    part_a_results, components = part_a_decomposition(
        model, tokenizer, protein_configs, seqs, weights, search_dir, args.device
    )
    plot_part_a(part_a_results, components, REPORT_DIR)
    write_part_a_report(part_a_results, components, REPORT_DIR)

    # Part B — geometric alignment
    sae_results = part_b_sae_alignment(
        model, tokenizer, protein_configs, seqs, search_dir, args.device
    )
    write_part_b_report(sae_results, REPORT_DIR)

    # Part B — differential activation
    diff_results = part_b_differential_activation(
        model, tokenizer, protein_configs, seqs, args.device
    )
    write_part_b_differential_report(diff_results, REPORT_DIR)

    print("\nDone. Outputs written to reports/outputs/multi_protein/")


if __name__ == "__main__":
    main()
