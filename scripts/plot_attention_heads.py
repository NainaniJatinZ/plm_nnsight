"""Generate presentation-quality attention heatmaps for all ESM2 heads.

Produces one PDF/PNG per layer (4x5 grid of 20 heads) and one all-layers
summary grid. Uses the cached attention from reports/cache/2B61A/.
"""

import sys
from pathlib import Path
import torch
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.gridspec as gridspec

CACHE_DIR = Path("reports/cache/2B61A")
OUT_DIR = Path("reports/outputs/2B61A/attention_heads")

NUM_LAYERS = 33
NUM_HEADS = 20


def load_data():
    cache = torch.load(CACHE_DIR / "attn_cache.pt", map_location="cpu", weights_only=False)
    ie = torch.load(CACHE_DIR / "indirect_effects.pt", map_location="cpu", weights_only=False)

    clean_attn = []
    for layer_idx in range(NUM_LAYERS):
        attn = cache["clean_attn_LBHLL"][layer_idx][0]  # remove batch dim -> (H, L, L)
        clean_attn.append(attn.numpy())
    clean_attn = np.stack(clean_attn)  # (33, 20, L, L)

    effects = ie["indirect_effects_LH"].numpy()  # (33, 20)
    return clean_attn, effects


def plot_layer(attn_HLL, effects_H, layer_idx, out_path):
    """Plot a single layer as a 4x5 grid of head heatmaps."""
    fig, axes = plt.subplots(4, 5, figsize=(20, 16))
    fig.suptitle(f"Layer {layer_idx}", fontsize=20, fontweight="bold", y=0.98)

    seq_len = attn_HLL.shape[1]

    for head_idx in range(NUM_HEADS):
        row, col = divmod(head_idx, 5)
        ax = axes[row, col]

        attn = attn_HLL[head_idx]  # (L, L)
        vmin = max(attn[attn > 0].min(), 1e-6) if (attn > 0).any() else 1e-6
        vmax = attn.max()
        if vmax <= vmin:
            vmax = vmin * 10

        im = ax.imshow(attn, aspect="equal", cmap="inferno", norm=LogNorm(vmin=vmin, vmax=vmax), interpolation="nearest")

        effect = effects_H[head_idx]
        effect_color = "#e74c3c" if effect > 0.05 else ("#3498db" if effect < -0.05 else "#95a5a6")
        ax.set_title(f"H{head_idx}  ({effect:+.3f})", fontsize=11, color=effect_color, fontweight="bold" if abs(effect) > 0.05 else "normal")

        ax.set_xticks([0, seq_len // 4, seq_len // 2, 3 * seq_len // 4, seq_len - 1])
        ax.set_yticks([0, seq_len // 4, seq_len // 2, 3 * seq_len // 4, seq_len - 1])
        ax.tick_params(labelsize=7, length=2)

    fig.subplots_adjust(left=0.03, right=0.92, top=0.93, bottom=0.03, wspace=0.15, hspace=0.25)
    cbar_ax = fig.add_axes([0.93, 0.15, 0.015, 0.65])
    fig.colorbar(im, cax=cbar_ax, label="Attention weight")

    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_summary(clean_attn, effects, out_path):
    """Plot all 33x20 heads as small multiples in one figure."""
    fig = plt.figure(figsize=(40, 66))
    gs = gridspec.GridSpec(NUM_LAYERS, NUM_HEADS, figure=fig, wspace=0.05, hspace=0.15)

    seq_len = clean_attn.shape[2]

    for layer_idx in range(NUM_LAYERS):
        for head_idx in range(NUM_HEADS):
            ax = fig.add_subplot(gs[layer_idx, head_idx])
            attn = clean_attn[layer_idx, head_idx]

            vmin = max(attn[attn > 0].min(), 1e-6) if (attn > 0).any() else 1e-6
            vmax = attn.max()
            if vmax <= vmin:
                vmax = vmin * 10

            ax.imshow(attn, aspect="equal", cmap="inferno", norm=LogNorm(vmin=vmin, vmax=vmax), interpolation="nearest")

            effect = effects[layer_idx, head_idx]
            if layer_idx == 0:
                ax.set_title(f"H{head_idx}", fontsize=6, pad=2)
            if head_idx == 0:
                ax.set_ylabel(f"L{layer_idx}", fontsize=6, rotation=0, labelpad=12, va="center")

            if abs(effect) > 0.05:
                border_color = "#e74c3c" if effect > 0 else "#3498db"
                for spine in ax.spines.values():
                    spine.set_edgecolor(border_color)
                    spine.set_linewidth(2)

            ax.set_xticks([])
            ax.set_yticks([])

    fig.suptitle("ESM2 Attention Heads — 2B61A (Clean)", fontsize=28, fontweight="bold", y=0.995)
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading cached attention data...")
    clean_attn, effects = load_data()
    print(f"Attention shape: {clean_attn.shape}, effects shape: {effects.shape}")

    # Per-layer plots
    for layer_idx in range(NUM_LAYERS):
        out_path = OUT_DIR / f"layer_{layer_idx:02d}.png"
        plot_layer(clean_attn[layer_idx], effects[layer_idx], layer_idx, out_path)
        print(f"  Layer {layer_idx:02d} -> {out_path}")

    # Summary grid
    print("Generating summary grid (this may take a moment)...")
    summary_path = OUT_DIR / "all_heads_summary.png"
    plot_summary(clean_attn, effects, summary_path)
    print(f"  Summary -> {summary_path}")

    print("Done.")


if __name__ == "__main__":
    main()
