"""
Attention–EVCoupling overlap analysis for 2B61A circuit heads.

For each circuit head, compares its attention pattern (clean, full-seq, and
causally relevant cells) against the top EVCouplings to identify "interaction
heads" whose attention aligns with evolutionary couplings.

Usage: uv run python scripts/attn_coupling_analysis.py
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch

# ── Paths ──────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "reports" / "cache" / "2B61A"
PROTEINS_CFG = ROOT / "configs" / "proteins.json"
COMMON_CFG = ROOT / "configs" / "common.json"
DATA_PATH = ROOT / "data" / "full_seq_dict.json"
COUPLING_CSV = ROOT / "data" / "TARGET_b0.3" / "couplings" / "TARGET_b0.3_CouplingScores.csv"

# ── Load configs ───────────────────────────────────────────────────────────

with open(PROTEINS_CFG) as f:
    proteins = json.load(f)
with open(COMMON_CFG) as f:
    common = json.load(f)
with open(DATA_PATH) as f:
    seq_dict = json.load(f)

PROTEIN = "2B61A"
cfg = proteins[PROTEIN]
seq = seq_dict[PROTEIN]
SEQ_LEN = len(seq)
SEGMENT_RADIUS = common["segment_radius"]
FAITH_TARGET = common["faith_target"]
NUM_LAYERS = 33
NUM_HEADS = 20

cp = cfg["contact_pair"]
ss1_start = cp[0] - SEGMENT_RADIUS
ss1_end = cp[0] + SEGMENT_RADIUS + 1
ss2_start = cp[1] - SEGMENT_RADIUS
ss2_end = cp[1] + SEGMENT_RADIUS + 1

print(f"Protein: {PROTEIN}, seq length: {SEQ_LEN}")
print(f"Contact pair: {cp}")
print(f"ss1: [{ss1_start}, {ss1_end})  ss2: [{ss2_start}, {ss2_end})")

# ── Load EVCouplings ───────────────────────────────────────────────────────

ev_df = pd.read_csv(COUPLING_CSV)
# EVCouplings uses 1-indexed positions; convert to 0-indexed
ev_df["i_0"] = ev_df["i"] - 1
ev_df["j_0"] = ev_df["j"] - 1

# Verify indexing
for _, row in ev_df.head(5).iterrows():
    expected = row["A_i"]
    actual = seq[int(row["i_0"])]
    assert actual == expected, f"Indexing mismatch at i={row['i']}: expected {expected}, got {actual}"

print(f"EVCouplings: {len(ev_df)} pairs loaded, indexing verified")

# Use top couplings by score (EVCouplings are already sorted by score descending)
# We'll use several thresholds
TOP_N_COUPLINGS = [50, 100, 200, 500]

# ── Load cached data ───────────────────────────────────────────────────────

print("Loading cached attention and circuit data...")
ad = torch.load(CACHE_DIR / "attn_cache.pt", map_location="cpu", weights_only=False)
ied = torch.load(CACHE_DIR / "indirect_effects.pt", map_location="cpu", weights_only=False)
cd = torch.load(CACHE_DIR / "circuit_results.pt", map_location="cpu", weights_only=False)

clean_attn = list(ad["clean_attn_LBHLL"])
ie = ied["indirect_effects_LH"]

# Load full-seq attention if available
full_attn = None
full_pt = CACHE_DIR / "full_seq_attn_cache.pt"
if full_pt.exists():
    fd = torch.load(full_pt, map_location="cpu", weights_only=False)
    full_key = next((k for k in ["attn_LBHLL", "full_attn_LBHLL", "clean_attn_LBHLL"] if k in fd), None)
    if full_key is not None:
        full_attn = fd[full_key]
        print("Full-sequence attention loaded")

# Load cell attributions
cell_data = None
cell_pt = CACHE_DIR / "cell_attr.pt"
if cell_pt.exists():
    cell_data = torch.load(cell_pt, map_location="cpu", weights_only=False)
    print(f"Cell attributions loaded: {len(cell_data['cell_attr_sorted'])} cells")

# ── Get circuit heads ──────────────────────────────────────────────────────

flat = ie.flatten()
sorted_idx = flat.argsort(descending=True)
all_heads = [(idx.item() // NUM_HEADS, idx.item() % NUM_HEADS) for idx in sorted_idx]

cr = cd["circuit_results"]["pos"]
crossed_k = None
for k_val, f_val in zip(cr["k"], cr["faith"]):
    if f_val >= FAITH_TARGET:
        crossed_k = k_val
        break
if crossed_k is None:
    crossed_k = common["topk_heads"]

circuit_heads = all_heads[:crossed_k]
print(f"Circuit size: {crossed_k} heads")

# ── Build coupling sets at different thresholds ────────────────────────────

def build_coupling_set(n):
    """Build set of (i_0, j_0) pairs from top-n couplings (0-indexed, symmetric)."""
    top = ev_df.head(n)
    pairs = set()
    for _, row in top.iterrows():
        i0, j0 = int(row["i_0"]), int(row["j_0"])
        pairs.add((i0, j0))
        pairs.add((j0, i0))
    return pairs


# ── Analysis functions ─────────────────────────────────────────────────────

def attn_coupling_overlap(attn_matrix_LL, coupling_set, threshold_percentile=95):
    """
    Compute overlap between attention pattern and coupling pairs.

    attn_matrix_LL: (L_tok, L_tok) attention matrix in token space (BOS at idx 0).
    coupling_set: set of (i_0, j_0) pairs in 0-indexed sequence space.

    Returns dict with overlap statistics.
    """
    # Convert to sequence space: attn[q+1, k+1] corresponds to (q, k) in seq space
    # We only look at actual amino acid positions (skip BOS/EOS)
    seq_len = attn_matrix_LL.shape[0] - 2  # subtract BOS and EOS
    if seq_len <= 0:
        return {"n_coupling_pairs": 0, "overlap": 0, "mean_attn_coupling": 0, "mean_attn_noncoupling": 0}

    # Extract AA-only submatrix (skip BOS=0, keep positions 1..seq_len)
    aa_attn = attn_matrix_LL[1:seq_len+1, 1:seq_len+1].numpy()

    # Threshold for "high attention" cells
    threshold = np.percentile(aa_attn, threshold_percentile)
    high_attn_mask = aa_attn >= threshold

    # Get positions of high-attention cells as (row, col) = (q_seq, k_seq) in 0-indexed
    high_attn_pairs = set(zip(*np.where(high_attn_mask)))

    # Count overlap
    overlap = high_attn_pairs & coupling_set
    n_coupling = len(coupling_set)
    n_high_attn = len(high_attn_pairs)
    n_overlap = len(overlap)

    # Mean attention on coupling vs non-coupling pairs
    coupling_attns = []
    non_coupling_attns = []
    for (i0, j0) in coupling_set:
        if 0 <= i0 < seq_len and 0 <= j0 < seq_len:
            coupling_attns.append(aa_attn[i0, j0])
    # Sample non-coupling for comparison (all cells minus coupling)
    non_coupling_attns = aa_attn.flatten().tolist()

    mean_coupling = np.mean(coupling_attns) if coupling_attns else 0.0
    mean_all = np.mean(non_coupling_attns) if non_coupling_attns else 0.0

    # Enrichment: ratio of coupling pairs found in high-attn vs expected by chance
    # Expected: (n_coupling / total_pairs) * n_high_attn
    total_pairs = seq_len * seq_len
    expected_overlap = (len(coupling_set & {(i, j) for i in range(seq_len) for j in range(seq_len) if (i, j) in coupling_set})) * n_high_attn / total_pairs if total_pairs > 0 else 0
    enrichment = n_overlap / expected_overlap if expected_overlap > 0 else 0.0

    return {
        "n_coupling_in_range": len([1 for (i, j) in coupling_set if 0 <= i < seq_len and 0 <= j < seq_len]) // 2,
        "n_high_attn": n_high_attn,
        "n_overlap": n_overlap,
        "enrichment": enrichment,
        "mean_attn_coupling": mean_coupling,
        "mean_attn_all": mean_all,
        "ratio_coupling_vs_all": mean_coupling / mean_all if mean_all > 0 else 0.0,
    }


def cell_coupling_overlap(head_cells, coupling_set):
    """
    Check how many causally relevant cells (from cell attribution) overlap with couplings.

    head_cells: list of (q_tok, k_tok, attr, adiff) — token-indexed (BOS=0).
    coupling_set: set of (i_0, j_0) in 0-indexed sequence space.
    """
    n_total = len(head_cells)
    if n_total == 0:
        return {"n_cells": 0, "n_overlap": 0, "overlap_frac": 0.0, "overlapping_pairs": []}

    overlapping = []
    for q_tok, k_tok, attr, adiff in head_cells:
        q_seq = q_tok - 1  # token to 0-indexed seq
        k_seq = k_tok - 1
        if (q_seq, k_seq) in coupling_set:
            overlapping.append((q_seq, k_seq, attr, adiff))

    return {
        "n_cells": n_total,
        "n_overlap": len(overlapping),
        "overlap_frac": len(overlapping) / n_total if n_total > 0 else 0.0,
        "overlapping_pairs": overlapping,
    }


# ── Run analysis ───────────────────────────────────────────────────────────

print(f"\n{'='*80}")
print(f"ATTENTION–COUPLING OVERLAP ANALYSIS: {PROTEIN}")
print(f"{'='*80}")

# Determine which attention source to use
attn_source_label = "full-seq" if full_attn is not None else "clean (masked)"
attn_source = full_attn if full_attn is not None else clean_attn
print(f"Attention source: {attn_source_label}")

for top_n in TOP_N_COUPLINGS:
    coupling_set = build_coupling_set(top_n)

    print(f"\n{'─'*80}")
    print(f"TOP {top_n} EVCouplings ({len(coupling_set)//2} unique pairs, {len(coupling_set)} directed)")
    print(f"{'─'*80}")

    # Show some of the top couplings for reference
    if top_n == TOP_N_COUPLINGS[0]:
        print("\nTop 10 couplings (0-indexed):")
        for _, row in ev_df.head(10).iterrows():
            print(f"  ({int(row['i_0']):3d}, {int(row['j_0']):3d})  "
                  f"{seq[int(row['i_0'])]}{int(row['i_0'])}–{seq[int(row['j_0'])]}{int(row['j_0'])}  "
                  f"score={row['score']:.2f}  cn={row['cn']:.4f}")

    results = []

    for rank_i, (l, h) in enumerate(circuit_heads):
        ie_val = ie[l, h].item()

        # Get attention matrix
        if isinstance(attn_source, (list, tuple)):
            attn_head = attn_source[l][0, h]
        else:
            attn_head = attn_source[l][0, h]

        # Attention overlap
        overlap = attn_coupling_overlap(attn_head, coupling_set)

        # Cell attribution overlap (if available)
        cell_overlap = None
        if cell_data is not None:
            head_cells = [(q, k, attr, adiff) for (ll, hh, q, k, attr, adiff)
                          in cell_data["cell_attr_sorted"]
                          if ll == l and hh == h]
            cell_overlap = cell_coupling_overlap(head_cells, coupling_set)

        results.append({
            "rank": rank_i + 1,
            "layer": l,
            "head": h,
            "ie": ie_val,
            "enrichment": overlap["enrichment"],
            "n_overlap": overlap["n_overlap"],
            "mean_attn_coupling": overlap["mean_attn_coupling"],
            "mean_attn_all": overlap["mean_attn_all"],
            "ratio": overlap["ratio_coupling_vs_all"],
            "cell_n": cell_overlap["n_cells"] if cell_overlap else 0,
            "cell_overlap": cell_overlap["n_overlap"] if cell_overlap else 0,
            "cell_frac": cell_overlap["overlap_frac"] if cell_overlap else 0.0,
            "cell_pairs": cell_overlap["overlapping_pairs"] if cell_overlap else [],
        })

    # Sort by enrichment to find the best coupling heads
    results_by_enrichment = sorted(results, key=lambda x: x["enrichment"], reverse=True)

    print(f"\nAll circuit heads ranked by coupling enrichment (top-{top_n} couplings):")
    print(f"{'rank':>5} {'L':>3} {'H':>3} {'IE':>8} {'enrich':>8} {'overlap':>8} {'attn_coup':>10} {'attn_all':>10} {'ratio':>7} {'cells':>6} {'cell_ov':>8}")
    print("─" * 90)
    for r in results_by_enrichment:
        cell_str = f"{r['cell_overlap']}/{r['cell_n']}" if r['cell_n'] > 0 else "—"
        print(f" #{r['rank']:2d}   L{r['layer']:2d} H{r['head']:2d}  {r['ie']:>+7.4f}  {r['enrichment']:>7.2f}x  {r['n_overlap']:>6d}  {r['mean_attn_coupling']:>10.6f}  {r['mean_attn_all']:>10.6f}  {r['ratio']:>6.2f}x  {cell_str:>8}")

    # Identify heads with notable enrichment (> 1.5x = more coupling overlap than chance)
    enriched = [r for r in results_by_enrichment if r["enrichment"] > 1.5]
    if enriched:
        print(f"\nHeads with >1.5x enrichment for coupling pairs in high-attention cells:")
        for r in enriched:
            print(f"  L{r['layer']} H{r['head']} (IE rank #{r['rank']}): {r['enrichment']:.2f}x enrichment, "
                  f"ratio(coupling/all)={r['ratio']:.2f}x")
            if r["cell_pairs"]:
                print(f"    Causal cells overlapping with couplings:")
                for q, k, attr, adiff in r["cell_pairs"][:5]:
                    ev_row = ev_df[(ev_df["i_0"] == q) & (ev_df["j_0"] == k) | (ev_df["i_0"] == k) & (ev_df["j_0"] == q)]
                    ev_score = ev_row["score"].values[0] if len(ev_row) > 0 else "?"
                    print(f"      ({q}, {k}) {seq[q]}{q}–{seq[k]}{k}  attr={attr:+.4f}  ev_score={ev_score}")
    else:
        print(f"\nNo heads with >1.5x enrichment at top-{top_n} coupling threshold.")

    # Also check: do any heads have attention-on-coupling >> attention-on-average?
    high_ratio = [r for r in results if r["ratio"] > 2.0]
    if high_ratio:
        print(f"\nHeads where mean attention on coupling pairs > 2x average:")
        for r in sorted(high_ratio, key=lambda x: x["ratio"], reverse=True):
            print(f"  L{r['layer']} H{r['head']} (IE rank #{r['rank']}): "
                  f"coupling_attn={r['mean_attn_coupling']:.6f} vs all={r['mean_attn_all']:.6f} "
                  f"({r['ratio']:.2f}x)")

# ── Focused analysis: coupling pairs involving contact residues ────────────

print(f"\n{'='*80}")
print(f"COUPLING PAIRS INVOLVING CONTACT RESIDUES ({cp[0]}, {cp[1]})")
print(f"{'='*80}")

contact_couplings = ev_df[
    (ev_df["i_0"] == cp[0]) | (ev_df["j_0"] == cp[0]) |
    (ev_df["i_0"] == cp[1]) | (ev_df["j_0"] == cp[1])
].head(20)

print(f"\nTop couplings involving contact pair residues (0-indexed):")
for _, row in contact_couplings.iterrows():
    i0, j0 = int(row["i_0"]), int(row["j_0"])
    print(f"  ({i0:3d}, {j0:3d})  {seq[i0]}{i0}–{seq[j0]}{j0}  score={row['score']:.2f}  cn={row['cn']:.4f}")

# For these specific pairs, check which circuit heads attend to them
print(f"\nCircuit heads attending to contact-residue couplings:")
contact_coupling_set = set()
for _, row in contact_couplings.iterrows():
    i0, j0 = int(row["i_0"]), int(row["j_0"])
    contact_coupling_set.add((i0, j0))
    contact_coupling_set.add((j0, i0))

for rank_i, (l, h) in enumerate(circuit_heads):
    if isinstance(attn_source, (list, tuple)):
        attn_head = attn_source[l][0, h].numpy()
    else:
        attn_head = attn_source[l][0, h].numpy()

    hits = []
    for (i0, j0) in contact_coupling_set:
        if i0 < 0 or j0 < 0:
            continue
        tok_q, tok_k = i0 + 1, j0 + 1
        if tok_q < attn_head.shape[0] and tok_k < attn_head.shape[1]:
            attn_val = attn_head[tok_q, tok_k]
            if attn_val > 0.01:  # non-trivial attention
                hits.append((i0, j0, attn_val))

    if hits:
        hits.sort(key=lambda x: x[2], reverse=True)
        print(f"  L{l:2d} H{h:2d} (rank #{rank_i+1}, IE={ie[l,h].item():+.4f}):")
        for i0, j0, attn_val in hits[:5]:
            print(f"    ({i0}, {j0}) {seq[i0]}{i0}→{seq[j0]}{j0}  attn={attn_val:.4f}")

# ── Coupling pairs in the segment regions ─────────────────────────────────

print(f"\n{'='*80}")
print(f"COUPLING PAIRS WITHIN/ACROSS CONTACT SEGMENTS")
print(f"{'='*80}")

ss1_range = set(range(ss1_start, ss1_end))
ss2_range = set(range(ss2_start, ss2_end))

# Cross-segment couplings: one residue in ss1 region, other in ss2 region
cross_segment = ev_df[
    ((ev_df["i_0"].isin(ss1_range)) & (ev_df["j_0"].isin(ss2_range))) |
    ((ev_df["i_0"].isin(ss2_range)) & (ev_df["j_0"].isin(ss1_range)))
]
print(f"\nCross-segment couplings (ss1 x ss2): {len(cross_segment)}")
for _, row in cross_segment.head(10).iterrows():
    i0, j0 = int(row["i_0"]), int(row["j_0"])
    print(f"  ({i0:3d}, {j0:3d})  {seq[i0]}{i0}–{seq[j0]}{j0}  score={row['score']:.2f}  cn={row['cn']:.4f}")

# Build set of cross-segment coupling pairs for targeted overlap
if len(cross_segment) > 0:
    cross_coupling_set = set()
    for _, row in cross_segment.iterrows():
        i0, j0 = int(row["i_0"]), int(row["j_0"])
        cross_coupling_set.add((i0, j0))
        cross_coupling_set.add((j0, i0))

    print(f"\nCircuit heads with attention on cross-segment coupling pairs:")
    for rank_i, (l, h) in enumerate(circuit_heads):
        if isinstance(attn_source, (list, tuple)):
            attn_head = attn_source[l][0, h].numpy()
        else:
            attn_head = attn_source[l][0, h].numpy()

        total_cross_attn = 0.0
        n_pairs = 0
        for (i0, j0) in cross_coupling_set:
            tok_q, tok_k = i0 + 1, j0 + 1
            if tok_q < attn_head.shape[0] and tok_k < attn_head.shape[1]:
                total_cross_attn += attn_head[tok_q, tok_k]
                n_pairs += 1

        mean_cross = total_cross_attn / n_pairs if n_pairs > 0 else 0.0
        mean_all = attn_head[1:-1, 1:-1].mean()

        if mean_cross > mean_all * 1.5:
            print(f"  L{l:2d} H{h:2d} (rank #{rank_i+1}): cross-segment coupling attn={mean_cross:.6f} vs all={mean_all:.6f} ({mean_cross/mean_all:.2f}x)")
else:
    print("No cross-segment coupling pairs found.")

print(f"\n{'='*80}")
print("DONE")
print(f"{'='*80}")
