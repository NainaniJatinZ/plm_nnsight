"""
InterProt SAE forward pass + top-latent heatmap visualization.

Loads ESM2-650M, extracts hidden states at a target layer, runs the InterProt SAE,
and visualizes the top activating latents as heatmaps over the sequence.

Usage:
    uv run python scripts/interprot_sae_viz.py --protein 2B61A --layer 24
    uv run python scripts/interprot_sae_viz.py --protein 2B61A --layer 8
    uv run python scripts/interprot_sae_viz.py --sequence MKTL... --layer 24
    uv run python scripts/interprot_sae_viz.py --protein 2B61A --layer 24 --latents 80 513 844
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import torch
from transformers import AutoTokenizer, EsmForMaskedLM

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from helpers.utils import load_sae_prot

WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
DATA_PATH = PROJECT_ROOT / "data" / "full_seq_dict.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_sequence(protein: str) -> str:
    with open(DATA_PATH) as f:
        seq_dict = json.load(f)
    if protein not in seq_dict:
        raise KeyError(f"Protein '{protein}' not found in {DATA_PATH}")
    return seq_dict[protein]


def get_hidden_states(sequence: str, layer: int, device: str) -> tuple[torch.Tensor, list[str]]:
    """Run ESM2 and return (hidden_BLD, token_strings) at the given layer."""
    os.environ["TORCH_HOME"] = WEIGHTS_DIR
    os.environ["HF_HOME"] = WEIGHTS_DIR

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR)
    model = EsmForMaskedLM.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR).to(device)
    model.eval()

    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    with torch.no_grad():
        out = model.esm(**inputs, output_hidden_states=True)

    return out.hidden_states[layer], tokens


def run_sae(hidden_BLD: torch.Tensor, layer: int, device: str) -> torch.Tensor:
    """Run InterProt SAE and return top-k activations (L, 4096)."""
    sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=layer, device=device)
    sae.eval()
    return sae.get_acts(hidden_BLD)[0]  # (L, 4096)


def top_latents(acts_LH: torch.Tensor, top_n: int = 20) -> list[dict]:
    """Rank latents by max activation across all positions."""
    max_per_latent, max_pos_per_latent = acts_LH.max(dim=0)
    mean_per_latent = acts_LH.mean(dim=0)
    num_active = (acts_LH > 0).sum(dim=0)

    sorted_idx = max_per_latent.argsort(descending=True)
    results = []
    for rank, idx in enumerate(sorted_idx[:top_n]):
        i = idx.item()
        results.append({
            "rank": rank + 1,
            "latent_idx": i,
            "max_act": max_per_latent[i].item(),
            "max_pos": max_pos_per_latent[i].item(),
            "mean_act": mean_per_latent[i].item(),
            "num_active": num_active[i].item(),
        })
    return results


# ---------------------------------------------------------------------------
# Heatmap
# ---------------------------------------------------------------------------

def plot_latent_heatmap(
    acts_LH: torch.Tensor,
    tokens: list[str],
    latent_idx: int,
    label: str = "",
    layer: int = 24,
    output_dir: Path | None = None,
):
    """Single-row heatmap of one latent's activations over the sequence (no CLS/EOS)."""
    seq_tokens = tokens[1:-1]
    act_vec = acts_LH[1:-1, latent_idx].cpu().numpy()
    n_pos = len(seq_tokens)
    chars_per_line = 80
    n_lines = int(np.ceil(n_pos / chars_per_line))

    max_act = act_vec.max()
    n_active = int((act_vec > 0).sum())

    fig, axes = plt.subplots(n_lines, 1, figsize=(min(chars_per_line * 0.3, 24), 0.8 * n_lines + 1.2), squeeze=False)
    fig.suptitle(f"{label} | Layer {layer} | Latent {latent_idx} (max={max_act:.2f}, active@{n_active} positions)", fontsize=10)

    vmax = max_act if max_act > 0 else 1.0
    cmap = plt.cm.Reds

    for row_i in range(n_lines):
        ax = axes[row_i, 0]
        start = row_i * chars_per_line
        end = min(start + chars_per_line, n_pos)
        for j, (tok, val) in enumerate(zip(seq_tokens[start:end], act_vec[start:end])):
            color = cmap(val / vmax) if vmax > 0 else (1, 1, 1, 1)
            ax.add_patch(plt.Rectangle((j, 0), 1, 1, facecolor=color, edgecolor="none"))
            ax.text(j + 0.5, 0.5, tok, ha="center", va="center", fontsize=5, fontfamily="monospace")
        ax.set_xlim(0, chars_per_line)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylabel(f"{start}", fontsize=6)
        for spine in ax.spines.values():
            spine.set_visible(False)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=mcolors.Normalize(vmin=0, vmax=vmax))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=axes.ravel().tolist(), orientation="horizontal", fraction=0.03, pad=0.08)
    cbar.set_label("Activation", fontsize=8)
    cbar.ax.tick_params(labelsize=6)

    if output_dir:
        safe_label = label.replace(" ", "_") if label else "seq"
        out_path = output_dir / f"{safe_label}_layer{layer}_latent{latent_idx}.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {out_path}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="InterProt SAE forward pass + visualization")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--protein", help="Protein ID from full_seq_dict.json")
    group.add_argument("--sequence", help="Raw amino acid sequence string")
    parser.add_argument("--layer", type=int, default=24, help="ESM2 layer for SAE (available: 4, 8, 12, 16, 20, 24, 28, 32)")
    parser.add_argument("--top-n", type=int, default=20, help="Number of top latents to print")
    parser.add_argument("--top-k-viz", type=int, default=5, help="Number of top latents to visualize (ignored if --latents is set)")
    parser.add_argument("--latents", type=int, nargs="+", help="Specific latent indices to visualize")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    label = args.protein or "custom"
    output_dir = PROJECT_ROOT / "reports" / "outputs" / label
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load sequence
    if args.protein:
        seq = load_sequence(args.protein)
    else:
        seq = args.sequence
    print(f"Input: {label}  |  Sequence length: {len(seq)}  |  Layer: {args.layer}")

    # 2. ESM2 forward pass
    print("Running ESM2 forward pass...")
    hidden_BLD, tokens = get_hidden_states(seq, layer=args.layer, device=args.device)

    # 3. SAE forward pass
    print(f"Running InterProt SAE (layer {args.layer})...")
    acts_LH = run_sae(hidden_BLD, layer=args.layer, device=args.device)
    n_activating = (acts_LH > 0).any(dim=0).sum().item()
    print(f"SAE activations: {acts_LH.shape[0]} positions x {acts_LH.shape[1]} latents, {n_activating} activating features")

    # 4. Top latents table
    top = top_latents(acts_LH, top_n=args.top_n)
    print(f"\nTop {args.top_n} latents by max activation:")
    print(f"{'Rank':>4}  {'Latent':>6}  {'MaxAct':>8}  {'MaxPos':>6}  {'MeanAct':>8}  {'#Active':>7}")
    for e in top:
        print(f"{e['rank']:4d}  {e['latent_idx']:6d}  {e['max_act']:8.3f}  {e['max_pos']:6d}  {e['mean_act']:8.4f}  {e['num_active']:7d}")

    # 5. Heatmaps
    if args.latents:
        viz_latents = args.latents
    else:
        viz_latents = [e["latent_idx"] for e in top[:args.top_k_viz]]

    print(f"\nGenerating heatmaps for latents: {viz_latents}")
    for latent_idx in viz_latents:
        plot_latent_heatmap(acts_LH, tokens, latent_idx, label=label, layer=args.layer, output_dir=output_dir)

    print("Done.")


if __name__ == "__main__":
    main()
