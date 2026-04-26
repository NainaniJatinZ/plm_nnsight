"""Check which heads in layers 9-15 have vertical attention patterns (anchor-like behavior).

For each head, computes verticality metrics across a sample of proteins:
- top1_mass: fraction of mean-key attention on the single top residue
- top3_mass: fraction on top 3 residues
- keys_50pct: how many keys needed to cover 50% of attention mass
- eff_keys: effective number of attended keys (exp of entropy)

Usage:
    uv run python scripts/_multi_head_vertical_audit.py --device cuda
"""

import argparse
import json
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"

NUM_LAYERS = 33
NUM_HEADS = 20
LAYERS_TO_CHECK = list(range(9, 16))  # layers 9-15


def load_model(device):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager").to(device).eval()
    model = NNsight(esm_model)
    return model, tokenizer


def compute_verticality(attn_AA: np.ndarray) -> dict:
    """Compute verticality metrics from a (n_res, n_res) attention matrix."""
    n_res = attn_AA.shape[0]
    mean_key_dist = attn_AA.mean(axis=0)
    sorted_dist = np.sort(mean_key_dist)[::-1]

    top1_mass = float(sorted_dist[0])
    top3_mass = float(sorted_dist[:min(3, n_res)].sum())

    p = mean_key_dist / (mean_key_dist.sum() + 1e-12)
    entropy = -float(np.sum(p * np.log(p + 1e-12)))
    eff_keys = float(np.exp(entropy))

    cumsum = np.cumsum(sorted_dist)
    total = cumsum[-1]
    keys_50pct = int(np.searchsorted(cumsum, total * 0.5) + 1)

    return {
        "top1_mass": top1_mass,
        "top3_mass": top3_mass,
        "eff_keys": eff_keys,
        "keys_50pct": keys_50pct,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--n-proteins", type=int, default=200, help="Number of proteins to sample")
    args = parser.parse_args()

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)

    # Filter to 100-500 residues, sample
    eligible = [(k, v) for k, v in all_seqs.items() if 100 <= len(v) <= 500]
    rng = np.random.RandomState(42)
    indices = rng.choice(len(eligible), size=min(args.n_proteins, len(eligible)), replace=False)
    sample = [eligible[i] for i in indices]
    print(f"Sampling {len(sample)} proteins from {len(eligible)} eligible (100-500 res)")

    print(f"Loading model on {args.device}...")
    model, tokenizer = load_model(args.device)

    # For each layer in 9-15, cache all heads' attention
    # Accumulate per-head metrics across proteins
    # head_stats[(layer, head)] = list of metric dicts
    head_stats = {}
    for layer in LAYERS_TO_CHECK:
        for head in range(NUM_HEADS):
            head_stats[(layer, head)] = []

    attn_modules = {}
    for layer in LAYERS_TO_CHECK:
        attn_modules[layer] = model.esm.encoder.layer[layer].attention.self

    print(f"Processing {len(sample)} proteins across layers {LAYERS_TO_CHECK}...")
    for idx, (pkey, seq) in enumerate(sample):
        inputs = tokenizer(seq, return_tensors="pt").to(args.device)
        modules_list = [attn_modules[l] for l in LAYERS_TO_CHECK]

        with model.trace() as tracer:
            with tracer.invoke(**inputs, output_attentions=True):
                cache = tracer.cache(modules=modules_list)

        for layer in LAYERS_TO_CHECK:
            key = f"model.esm.encoder.layer.{layer}.attention.self"
            attn_HLL = cache[key].output[1].detach().cpu()[0]  # (H, L, L)
            for head in range(NUM_HEADS):
                attn_AA = attn_HLL[head, 1:-1, 1:-1].numpy()
                metrics = compute_verticality(attn_AA)
                head_stats[(layer, head)].append(metrics)

        if (idx + 1) % 50 == 0:
            print(f"  [{idx + 1}/{len(sample)}]")

    # Aggregate and rank heads
    print("\n" + "=" * 90)
    print(f"VERTICAL ATTENTION HEAD AUDIT (layers {LAYERS_TO_CHECK[0]}-{LAYERS_TO_CHECK[-1]}, {len(sample)} proteins)")
    print("Ranked by median top-3 key mass (higher = more vertical/anchor-like)")
    print("=" * 90)

    summary = []
    for (layer, head), stats_list in head_stats.items():
        top3_vals = [s["top3_mass"] for s in stats_list]
        top1_vals = [s["top1_mass"] for s in stats_list]
        eff_keys_vals = [s["eff_keys"] for s in stats_list]
        keys50_vals = [s["keys_50pct"] for s in stats_list]
        summary.append({
            "layer": layer,
            "head": head,
            "top3_mass_median": np.median(top3_vals),
            "top3_mass_mean": np.mean(top3_vals),
            "top1_mass_median": np.median(top1_vals),
            "eff_keys_median": np.median(eff_keys_vals),
            "keys50_median": np.median(keys50_vals),
            "pct_top3_gt_0.5": np.mean([v > 0.5 for v in top3_vals]) * 100,
        })

    summary.sort(key=lambda x: x["top3_mass_median"], reverse=True)

    print(f"\n{'Rank':>4}  {'Head':>8}  {'top3 med':>9}  {'top3 mean':>9}  {'top1 med':>9}  {'eff_keys':>9}  {'keys50':>7}  {'%prot>0.5':>10}")
    print("-" * 85)
    for rank, s in enumerate(summary):
        label = f"L{s['layer']}H{s['head']}"
        marker = " ***" if s["top3_mass_median"] > 0.5 else ""
        print(f"{rank+1:>4}  {label:>8}  {s['top3_mass_median']:>9.4f}  {s['top3_mass_mean']:>9.4f}  {s['top1_mass_median']:>9.4f}  {s['eff_keys_median']:>9.1f}  {s['keys50_median']:>7.0f}  {s['pct_top3_gt_0.5']:>9.1f}%{marker}")

    # Also print just the clearly vertical heads (top3 > 0.5 in majority of proteins)
    vertical_heads = [s for s in summary if s["pct_top3_gt_0.5"] > 50]
    print(f"\n{'=' * 90}")
    print(f"CLEARLY VERTICAL HEADS (top-3 mass > 0.5 in >50% of proteins): {len(vertical_heads)}")
    print("=" * 90)
    for s in vertical_heads:
        label = f"L{s['layer']}H{s['head']}"
        print(f"  {label:>8}  top3_median={s['top3_mass_median']:.4f}  top1_median={s['top1_mass_median']:.4f}  eff_keys={s['eff_keys_median']:.1f}  {s['pct_top3_gt_0.5']:.0f}% proteins")


if __name__ == "__main__":
    main()
