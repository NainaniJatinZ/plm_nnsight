"""Cache attention patterns for the full (unmasked) sequence and generate plots.

Usage:
    .plm_nn/bin/python scripts/cache_full_seq_attention.py --protein 2B61A
    .plm_nn/bin/python scripts/cache_full_seq_attention.py --protein 2B61A --plot-only
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


_ROOT = Path(__file__).resolve().parent.parent
NUM_LAYERS = 33
NUM_HEADS = 20


def cache_full_attention(protein: str, device: str) -> Path:
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer

    cache_dir = _ROOT / "reports" / "cache" / protein
    cache_dir.mkdir(parents=True, exist_ok=True)
    out_path = cache_dir / "full_seq_attn_cache.pt"

    with open(_ROOT / "data" / "full_seq_dict.json") as f:
        seqs = json.load(f)
    seq = seqs[protein]
    print(f"Protein {protein}: {len(seq)} residues")

    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device).eval()
    model = NNsight(esm_model)

    inputs = tokenizer(seq, return_tensors="pt").to(device)
    inputs_with_attn = {**inputs, "output_attentions": True}
    print(f"Token count: {inputs['input_ids'].shape[1]} (including BOS/EOS)")

    print("Running forward pass with attention caching...")
    with model.trace() as tracer:
        with tracer.invoke(**inputs_with_attn):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(NUM_LAYERS)]
            )

    attn_LBHLL = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())

    torch.save({
        "attn_LBHLL": attn_LBHLL,
        "sequence": seq,
        "input_ids": inputs["input_ids"].cpu(),
    }, out_path)

    print(f"Saved full-sequence attention to {out_path}")
    return out_path


def load_cached_attention(protein: str):
    cache_path = _ROOT / "reports" / "cache" / protein / "full_seq_attn_cache.pt"
    if not cache_path.exists():
        raise FileNotFoundError(f"No cached attention at {cache_path}. Run without --plot-only first.")
    data = torch.load(cache_path, map_location="cpu", weights_only=False)
    attn = np.stack([data["attn_LBHLL"][i][0].numpy() for i in range(NUM_LAYERS)])  # (33, 20, L, L)
    return attn, data["sequence"]


def plot_single_head(attn_LL, layer, head, seq, out_path):
    """High-quality single-head plot suitable for sharing."""
    fig, ax = plt.subplots(figsize=(10, 10))

    vmin = max(attn_LL[attn_LL > 0].min(), 1e-6) if (attn_LL > 0).any() else 1e-6
    vmax = attn_LL.max()
    if vmax <= vmin:
        vmax = vmin * 10

    im = ax.imshow(attn_LL, aspect="equal", cmap="inferno", norm=LogNorm(vmin=vmin, vmax=vmax), interpolation="nearest")

    ax.set_xlabel("Key position", fontsize=13)
    ax.set_ylabel("Query position", fontsize=13)
    ax.set_title(f"ESM2  Layer {layer}, Head {head}", fontsize=18, fontweight="bold", pad=12)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Attention weight", fontsize=12)
    cbar.ax.tick_params(labelsize=10)
    ax.tick_params(labelsize=10)

    fig.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_layer_grid(attn_HLL, layer, seq, out_path):
    """4x5 grid of all heads in one layer."""
    fig, axes = plt.subplots(4, 5, figsize=(20, 16))
    fig.suptitle(f"Layer {layer}  (full sequence)", fontsize=20, fontweight="bold", y=0.98)

    seq_len = attn_HLL.shape[1]

    for head_idx in range(NUM_HEADS):
        row, col = divmod(head_idx, 5)
        ax = axes[row, col]
        attn = attn_HLL[head_idx]

        vmin = max(attn[attn > 0].min(), 1e-6) if (attn > 0).any() else 1e-6
        vmax = attn.max()
        if vmax <= vmin:
            vmax = vmin * 10

        im = ax.imshow(attn, aspect="equal", cmap="inferno", norm=LogNorm(vmin=vmin, vmax=vmax), interpolation="nearest")
        ax.set_title(f"H{head_idx}", fontsize=11, fontweight="bold")
        ax.set_xticks([0, seq_len // 4, seq_len // 2, 3 * seq_len // 4, seq_len - 1])
        ax.set_yticks([0, seq_len // 4, seq_len // 2, 3 * seq_len // 4, seq_len - 1])
        ax.tick_params(labelsize=7, length=2)

    fig.subplots_adjust(left=0.03, right=0.92, top=0.93, bottom=0.03, wspace=0.15, hspace=0.25)
    cbar_ax = fig.add_axes([0.93, 0.15, 0.015, 0.65])
    fig.colorbar(im, cax=cbar_ax, label="Attention weight")

    fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_summary_grid(attn, seq, out_path):
    """All 33x20 heads as small multiples."""
    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(40, 66))
    gs = gridspec.GridSpec(NUM_LAYERS, NUM_HEADS, figure=fig, wspace=0.05, hspace=0.15)

    for layer_idx in range(NUM_LAYERS):
        for head_idx in range(NUM_HEADS):
            ax = fig.add_subplot(gs[layer_idx, head_idx])
            a = attn[layer_idx, head_idx]

            vmin = max(a[a > 0].min(), 1e-6) if (a > 0).any() else 1e-6
            vmax = a.max()
            if vmax <= vmin:
                vmax = vmin * 10

            ax.imshow(a, aspect="equal", cmap="inferno", norm=LogNorm(vmin=vmin, vmax=vmax), interpolation="nearest")

            if layer_idx == 0:
                ax.set_title(f"H{head_idx}", fontsize=6, pad=2)
            if head_idx == 0:
                ax.set_ylabel(f"L{layer_idx}", fontsize=6, rotation=0, labelpad=12, va="center")
            ax.set_xticks([])
            ax.set_yticks([])

    fig.suptitle(f"ESM2 Attention Heads — Full Sequence", fontsize=28, fontweight="bold", y=0.995)
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protein", default="2B61A")
    parser.add_argument("--device", default=None)
    parser.add_argument("--plot-only", action="store_true", help="Skip forward pass, use existing cache")
    parser.add_argument("--head", nargs=2, type=int, metavar=("LAYER", "HEAD"), help="Also generate a single high-res head plot (e.g. --head 6 11)")
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")

    if not args.plot_only:
        cache_full_attention(args.protein, device)

    print("\nGenerating plots...")
    attn, seq = load_cached_attention(args.protein)
    print(f"Attention shape: {attn.shape}")

    out_dir = _ROOT / "reports" / "outputs" / args.protein / "attention_heads_full"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Per-layer grids
    for layer_idx in range(NUM_LAYERS):
        out_path = out_dir / f"layer_{layer_idx:02d}.png"
        plot_layer_grid(attn[layer_idx], layer_idx, seq, out_path)
        print(f"  Layer {layer_idx:02d} -> {out_path}")

    # Summary grid
    print("Generating summary grid...")
    plot_summary_grid(attn, seq, out_dir / "all_heads_summary.png")
    print(f"  Summary -> {out_dir / 'all_heads_summary.png'}")

    # Single head if requested
    if args.head:
        layer, head = args.head
        out_path = out_dir / f"L{layer}_H{head}.png"
        plot_single_head(attn[layer, head], layer, head, seq, out_path)
        print(f"  Single head -> {out_path}")

    print("Done.")


if __name__ == "__main__":
    main()
