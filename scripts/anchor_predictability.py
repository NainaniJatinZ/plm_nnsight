#!/usr/bin/env python3
"""Test: is the anchor the most predictable position from local context?

For each protein, mask each position individually, run ESM2 forward, measure:
  - Prediction entropy at the masked position
  - Log-probability of the true amino acid
  - Rank of the true AA in the predicted distribution

Compare anchors vs structurally matched controls and vs all positions.

Usage:
    PYTHONUNBUFFERED=1 uv run python scripts/anchor_predictability.py --device cuda --n-proteins 30
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
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PDB_DIR = DATA_DIR / "pdb"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

AUDIT_CSV = REPORT_DIR / "anchor_behavior_audit.csv"

TARGET_LAYER = 10
TARGET_HEAD = 9
MASK_TOKEN_STR = "<mask>"


def flush_print(*args, **kwargs):
    print(*args, **kwargs, flush=True)


def load_model_and_tokenizer(device: str):
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    model = EsmForMaskedLM.from_pretrained(
        model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager"
    ).to(device).eval()
    return model, tokenizer


def select_proteins(seqs, ss_dict, n):
    """Select top-n confident proteins by top1_mass."""
    rows = []
    with open(AUDIT_CSV) as f:
        for r in csv.DictReader(f):
            pid = r["protein"]
            if pid not in seqs or pid not in ss_dict:
                continue
            if len(seqs[pid]) != len(ss_dict[pid]):
                continue
            mass = float(r["top1_mass"])
            if mass < 0.5:
                continue
            anchor_pos = int(r["top_key_idx"])
            rows.append({"protein": pid, "anchor_pos": anchor_pos, "top1_mass": mass})
    rows.sort(key=lambda x: x["top1_mass"], reverse=True)
    return rows[:n]


@torch.no_grad()
def measure_predictability(model, tokenizer, sequence: str, device: str, batch_size: int = 8):
    """Mask each position individually, measure prediction entropy and log-prob of true AA.

    Returns:
        entropy: (n_res,) prediction entropy at each position when masked
        logprob: (n_res,) log-probability of the true AA at each position when masked
        true_rank: (n_res,) rank of the true AA (0 = top prediction)
    """
    n_res = len(sequence)
    mask_token_id = tokenizer.mask_token_id

    # Tokenize the original sequence to get true token IDs
    orig_tokens = tokenizer(sequence, return_tensors="pt")["input_ids"][0]  # includes BOS/EOS
    # Positions 1..n_res are the residue tokens (0=BOS, n_res+1=EOS)

    entropy = np.zeros(n_res)
    logprob = np.zeros(n_res)
    true_rank = np.zeros(n_res, dtype=int)

    # Process in batches: each batch masks a different set of positions
    for batch_start in range(0, n_res, batch_size):
        batch_end = min(batch_start + batch_size, n_res)
        batch_positions = list(range(batch_start, batch_end))
        bs = len(batch_positions)

        # Create batch: repeat original tokens, mask one position per copy
        input_ids = orig_tokens.unsqueeze(0).repeat(bs, 1).to(device)  # (bs, L)
        for i, pos in enumerate(batch_positions):
            input_ids[i, pos + 1] = mask_token_id  # +1 for BOS offset

        attention_mask = torch.ones_like(input_ids)
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits  # (bs, L, vocab)

        for i, pos in enumerate(batch_positions):
            token_logits = logits[i, pos + 1]  # logits at the masked position
            probs = F.softmax(token_logits, dim=-1)
            log_probs = F.log_softmax(token_logits, dim=-1)

            # Entropy
            ent = -(probs * log_probs).sum().item()
            entropy[pos] = ent

            # Log-prob of true AA
            true_token_id = orig_tokens[pos + 1].item()
            logprob[pos] = log_probs[true_token_id].item()

            # Rank of true AA
            sorted_indices = torch.argsort(probs, descending=True)
            rank = (sorted_indices == true_token_id).nonzero(as_tuple=True)[0].item()
            true_rank[pos] = rank

    return entropy, logprob, true_rank


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--n-proteins", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    flush_print("Loading data...")
    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")

    seqs = {k: v for k, v in all_seqs.items() if 100 <= len(v) <= 500}
    proteins = select_proteins(seqs, ss_dict, args.n_proteins)
    flush_print(f"  {len(proteins)} proteins selected")

    flush_print(f"Loading model on {args.device}...")
    model, tokenizer = load_model_and_tokenizer(args.device)

    # PDB features for structural matching
    from scripts.qk_space_decomposition import compute_pdb_features
    MAX_ASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}

    # -----------------------------------------------------------------------
    # Process each protein
    # -----------------------------------------------------------------------
    results = []
    t0 = time.time()

    for i, pinfo in enumerate(proteins):
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        n_res = len(seq)
        sse = ss_dict.get(pid, "C" * n_res)

        flush_print(f"\n  [{i+1}/{len(proteins)}] {pid} (n_res={n_res}, anchor={anchor})")

        entropy, logprob, true_rank = measure_predictability(model, tokenizer, seq, args.device, args.batch_size)

        # Anchor stats
        anchor_entropy = entropy[anchor]
        anchor_logprob = logprob[anchor]
        anchor_true_rank = true_rank[anchor]

        # Rank of anchor among all positions (by entropy ascending = most predictable first)
        entropy_rank_order = np.argsort(entropy)  # sorted by ascending entropy
        anchor_entropy_rank = int(np.where(entropy_rank_order == anchor)[0][0])  # 0 = lowest entropy

        # Rank by log-prob descending (most confident first)
        logprob_rank_order = np.argsort(-logprob)
        anchor_logprob_rank = int(np.where(logprob_rank_order == anchor)[0][0])

        # Percentile (0 = most predictable)
        anchor_entropy_pctile = anchor_entropy_rank / n_res
        anchor_logprob_pctile = anchor_logprob_rank / n_res

        flush_print(f"    Anchor entropy={anchor_entropy:.4f} (rank {anchor_entropy_rank}/{n_res}, pctile {anchor_entropy_pctile:.3f})")
        flush_print(f"    Anchor logprob={anchor_logprob:.4f} (rank {anchor_logprob_rank}/{n_res}, pctile {anchor_logprob_pctile:.3f})")
        flush_print(f"    Anchor true_rank={anchor_true_rank}")

        # Compare to same-SSE positions
        anchor_sse = sse[anchor] if anchor < len(sse) else "C"
        same_sse_mask = np.array([sse[j] == anchor_sse for j in range(n_res)])
        same_sse_mask[anchor] = False  # exclude anchor itself
        if same_sse_mask.sum() > 0:
            same_sse_entropy_mean = entropy[same_sse_mask].mean()
            same_sse_logprob_mean = logprob[same_sse_mask].mean()
        else:
            same_sse_entropy_mean = np.nan
            same_sse_logprob_mean = np.nan

        # Compare to buried positions (if PDB available)
        pdb_feats = compute_pdb_features(pid, seq)
        buried_entropy_mean = np.nan
        buried_logprob_mean = np.nan
        n_buried = 0
        if pdb_feats is not None:
            buried_mask = np.zeros(n_res, dtype=bool)
            for pos, feats in pdb_feats.items():
                if isinstance(pos, int) and 0 <= pos < n_res and feats["rsa"] < 0.05:
                    buried_mask[pos] = True
            buried_mask[anchor] = False
            n_buried = buried_mask.sum()
            if n_buried > 0:
                buried_entropy_mean = entropy[buried_mask].mean()
                buried_logprob_mean = logprob[buried_mask].mean()

        results.append({
            "protein": pid,
            "n_res": n_res,
            "anchor_pos": anchor,
            "anchor_sse": anchor_sse,
            "anchor_entropy": float(anchor_entropy),
            "anchor_logprob": float(anchor_logprob),
            "anchor_true_rank": int(anchor_true_rank),
            "anchor_entropy_rank": anchor_entropy_rank,
            "anchor_logprob_rank": anchor_logprob_rank,
            "anchor_entropy_pctile": float(anchor_entropy_pctile),
            "anchor_logprob_pctile": float(anchor_logprob_pctile),
            "all_entropy_mean": float(entropy.mean()),
            "all_entropy_std": float(entropy.std()),
            "all_logprob_mean": float(logprob.mean()),
            "same_sse_entropy_mean": float(same_sse_entropy_mean),
            "same_sse_logprob_mean": float(same_sse_logprob_mean),
            "buried_entropy_mean": float(buried_entropy_mean),
            "buried_logprob_mean": float(buried_logprob_mean),
            "n_buried": n_buried,
            # Store full arrays for plotting
            "_entropy": entropy,
            "_logprob": logprob,
        })

    elapsed = time.time() - t0
    flush_print(f"\nProcessed {len(results)} proteins in {elapsed:.0f}s")

    # ===================================================================
    # Aggregate analysis
    # ===================================================================
    flush_print("\n=== Aggregate results ===")

    entropy_pctiles = [r["anchor_entropy_pctile"] for r in results]
    logprob_pctiles = [r["anchor_logprob_pctile"] for r in results]
    entropy_ranks = [r["anchor_entropy_rank"] for r in results]

    flush_print(f"  Anchor entropy percentile: mean={np.mean(entropy_pctiles):.3f}, median={np.median(entropy_pctiles):.3f}")
    flush_print(f"  Anchor logprob percentile: mean={np.mean(logprob_pctiles):.3f}, median={np.median(logprob_pctiles):.3f}")
    flush_print(f"  (0.0 = most predictable position, 0.5 = median, 1.0 = least predictable)")

    # How often is the anchor in top-5%, top-10%, top-25%?
    for threshold in [0.01, 0.05, 0.10, 0.25]:
        frac_entropy = np.mean([p <= threshold for p in entropy_pctiles])
        frac_logprob = np.mean([p <= threshold for p in logprob_pctiles])
        flush_print(f"  Anchor in top-{threshold:.0%} most predictable: {frac_entropy:.0%} (by entropy), {frac_logprob:.0%} (by logprob)")

    # Anchor vs same-SSE
    ent_diffs_sse = [(r["anchor_entropy"] - r["same_sse_entropy_mean"]) for r in results if not np.isnan(r["same_sse_entropy_mean"])]
    lp_diffs_sse = [(r["anchor_logprob"] - r["same_sse_logprob_mean"]) for r in results if not np.isnan(r["same_sse_logprob_mean"])]
    if ent_diffs_sse:
        flush_print(f"\n  Anchor entropy - same-SSE mean: {np.mean(ent_diffs_sse):.4f} (negative = anchor more predictable)")
        flush_print(f"  Anchor logprob - same-SSE mean: {np.mean(lp_diffs_sse):.4f} (positive = anchor more confident)")
        t_stat, p_val = sp_stats.ttest_1samp(ent_diffs_sse, 0)
        flush_print(f"  t-test (entropy diff): t={t_stat:.3f}, p={p_val:.4e}")

    # Anchor vs buried
    ent_diffs_buried = [(r["anchor_entropy"] - r["buried_entropy_mean"]) for r in results if not np.isnan(r["buried_entropy_mean"])]
    lp_diffs_buried = [(r["anchor_logprob"] - r["buried_logprob_mean"]) for r in results if not np.isnan(r["buried_logprob_mean"])]
    if ent_diffs_buried:
        flush_print(f"\n  Anchor entropy - buried mean: {np.mean(ent_diffs_buried):.4f}")
        flush_print(f"  Anchor logprob - buried mean: {np.mean(lp_diffs_buried):.4f}")
        t_stat, p_val = sp_stats.ttest_1samp(ent_diffs_buried, 0)
        flush_print(f"  t-test (entropy diff vs buried): t={t_stat:.3f}, p={p_val:.4e}")

    # ===================================================================
    # Figures
    # ===================================================================
    flush_print("\nGenerating figures...")

    fig, axes = plt.subplots(2, 3, figsize=(15, 9))

    # Panel A: Histogram of anchor entropy percentiles
    ax = axes[0, 0]
    ax.hist(entropy_pctiles, bins=20, color="#5B7FA3", edgecolor="white", linewidth=0.5)
    ax.axvline(0.5, color="gray", ls=":", lw=0.7)
    ax.axvline(np.median(entropy_pctiles), color="#D64550", ls="--", lw=1.5, label=f"median={np.median(entropy_pctiles):.3f}")
    ax.set_xlabel("Anchor entropy percentile (0 = most predictable)")
    ax.set_ylabel("Count")
    ax.set_title("A. Anchor predictability rank (entropy)")
    ax.legend(fontsize=8)

    # Panel B: Histogram of anchor logprob percentiles
    ax = axes[0, 1]
    ax.hist(logprob_pctiles, bins=20, color="#6BBF8A", edgecolor="white", linewidth=0.5)
    ax.axvline(0.5, color="gray", ls=":", lw=0.7)
    ax.axvline(np.median(logprob_pctiles), color="#D64550", ls="--", lw=1.5, label=f"median={np.median(logprob_pctiles):.3f}")
    ax.set_xlabel("Anchor logprob percentile (0 = most confident)")
    ax.set_ylabel("Count")
    ax.set_title("B. Anchor predictability rank (logprob)")
    ax.legend(fontsize=8)

    # Panel C: Anchor entropy vs mean entropy
    ax = axes[0, 2]
    all_means = [r["all_entropy_mean"] for r in results]
    anchor_ents = [r["anchor_entropy"] for r in results]
    ax.scatter(all_means, anchor_ents, s=30, c="#5B7FA3", edgecolors="white", linewidths=0.3)
    lims = [min(min(all_means), min(anchor_ents)) - 0.1, max(max(all_means), max(anchor_ents)) + 0.1]
    ax.plot(lims, lims, "k--", lw=0.7, alpha=0.5)
    ax.set_xlabel("Mean entropy (all positions)")
    ax.set_ylabel("Anchor entropy")
    ax.set_title("C. Anchor vs population entropy")
    n_below = sum(1 for a, m in zip(anchor_ents, all_means) if a < m)
    ax.text(0.05, 0.95, f"{n_below}/{len(results)} below diagonal\n(anchor more predictable)", transform=ax.transAxes, va="top", fontsize=8)

    # Panel D: Example protein -- entropy across sequence
    ax = axes[1, 0]
    # Pick protein with median anchor percentile for representative example
    sorted_by_pctile = sorted(results, key=lambda r: r["anchor_entropy_pctile"])
    mid = sorted_by_pctile[len(sorted_by_pctile) // 2]
    ent = mid["_entropy"]
    pos = np.arange(len(ent))
    ax.plot(pos, ent, "-", color="#AAAAAA", lw=0.5)
    ax.scatter(pos, ent, s=2, c="#AAAAAA")
    ax.scatter(mid["anchor_pos"], ent[mid["anchor_pos"]], s=80, c="#D64550", zorder=5, marker="v", label=f"anchor (pos {mid['anchor_pos']})")
    ax.set_xlabel("Residue position")
    ax.set_ylabel("Prediction entropy (lower = more predictable)")
    ax.set_title(f"D. Example: {mid['protein']} (pctile={mid['anchor_entropy_pctile']:.3f})")
    ax.legend(fontsize=8)

    # Panel E: anchor entropy vs same-SSE mean
    ax = axes[1, 1]
    sse_means = [r["same_sse_entropy_mean"] for r in results if not np.isnan(r["same_sse_entropy_mean"])]
    sse_anchors = [r["anchor_entropy"] for r in results if not np.isnan(r["same_sse_entropy_mean"])]
    ax.scatter(sse_means, sse_anchors, s=30, c="#E07B54", edgecolors="white", linewidths=0.3)
    lims2 = [min(min(sse_means), min(sse_anchors)) - 0.1, max(max(sse_means), max(sse_anchors)) + 0.1]
    ax.plot(lims2, lims2, "k--", lw=0.7, alpha=0.5)
    ax.set_xlabel("Mean entropy (same-SSE positions)")
    ax.set_ylabel("Anchor entropy")
    ax.set_title("E. Anchor vs same-SSE entropy")
    n_below_sse = sum(1 for a, m in zip(sse_anchors, sse_means) if a < m)
    ax.text(0.05, 0.95, f"{n_below_sse}/{len(sse_anchors)} below diagonal", transform=ax.transAxes, va="top", fontsize=8)

    # Panel F: anchor entropy vs buried mean
    ax = axes[1, 2]
    bur_means = [r["buried_entropy_mean"] for r in results if not np.isnan(r["buried_entropy_mean"])]
    bur_anchors = [r["anchor_entropy"] for r in results if not np.isnan(r["buried_entropy_mean"])]
    if bur_means:
        ax.scatter(bur_means, bur_anchors, s=30, c="#2C5F8A", edgecolors="white", linewidths=0.3)
        lims3 = [min(min(bur_means), min(bur_anchors)) - 0.1, max(max(bur_means), max(bur_anchors)) + 0.1]
        ax.plot(lims3, lims3, "k--", lw=0.7, alpha=0.5)
        n_below_bur = sum(1 for a, m in zip(bur_anchors, bur_means) if a < m)
        ax.text(0.05, 0.95, f"{n_below_bur}/{len(bur_anchors)} below diagonal", transform=ax.transAxes, va="top", fontsize=8)
    ax.set_xlabel("Mean entropy (buried positions, RSA<0.05)")
    ax.set_ylabel("Anchor entropy")
    ax.set_title("F. Anchor vs buried-position entropy")

    for ax in axes.flat:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    plt.tight_layout()
    out_path = REPORT_DIR / "anchor_predictability.png"
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    flush_print(f"  Saved: {out_path}")

    # ===================================================================
    # Save CSV (without the full arrays)
    # ===================================================================
    csv_path = REPORT_DIR / "anchor_predictability.csv"
    csv_fields = [k for k in results[0].keys() if not k.startswith("_")]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        for r in results:
            writer.writerow({k: v for k, v in r.items() if not k.startswith("_")})
    flush_print(f"  Saved: {csv_path}")

    flush_print("\nDone.")


# Need this import for the t-test
from scipy import stats as sp_stats

if __name__ == "__main__":
    main()
