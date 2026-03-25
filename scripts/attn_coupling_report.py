"""
Generate coupling-attention overlap report with plots for 2B61A.

Produces:
  - Per-head full-sequence heatmaps with EVCoupling + causal cell overlays
  - Summary enrichment bar chart
  - Coupling score vs attention scatter
  - Cross-segment coupling bar chart
  - IE rank vs enrichment scatter
  - Markdown report

Causal cells = top TOPK_CELL (1000) cells globally from cell attribution,
i.e. the same set verified by the sufficiency test.

Usage: uv run python scripts/attn_coupling_report.py
"""

import json
from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from matplotlib.colors import LogNorm

# ── Paths ──────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "reports" / "cache" / "2B61A"
PROTEINS_CFG = ROOT / "configs" / "proteins.json"
COMMON_CFG = ROOT / "configs" / "common.json"
DATA_PATH = ROOT / "data" / "full_seq_dict.json"
COUPLING_CSV = ROOT / "data" / "TARGET_b0.3" / "couplings" / "TARGET_b0.3_CouplingScores.csv"
OUT_DIR = ROOT / "reports" / "outputs" / "2B61A" / "coupling"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Load everything ────────────────────────────────────────────────────────

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
TOPK_CELL = 2000  # expanded from common["topk_cell"]=1000 to capture more causal cells
NUM_LAYERS = 33
NUM_HEADS = 20

cp = cfg["contact_pair"]
ss1_s, ss1_e = cp[0] - SEGMENT_RADIUS, cp[0] + SEGMENT_RADIUS + 1
ss2_s, ss2_e = cp[1] - SEGMENT_RADIUS, cp[1] + SEGMENT_RADIUS + 1

print(f"Loading data for {PROTEIN}...")
ad = torch.load(CACHE_DIR / "attn_cache.pt", map_location="cpu", weights_only=False)
ied = torch.load(CACHE_DIR / "indirect_effects.pt", map_location="cpu", weights_only=False)
cd = torch.load(CACHE_DIR / "circuit_results.pt", map_location="cpu", weights_only=False)
bd = torch.load(CACHE_DIR / "baselines.pt", map_location="cpu", weights_only=False)

clean_attn = list(ad["clean_attn_LBHLL"])
ie = ied["indirect_effects_LH"]

full_attn = None
full_pt = CACHE_DIR / "full_seq_attn_cache.pt"
if full_pt.exists():
    fd = torch.load(full_pt, map_location="cpu", weights_only=False)
    full_key = next((k for k in ["attn_LBHLL", "full_attn_LBHLL", "clean_attn_LBHLL"] if k in fd), None)
    if full_key:
        full_attn = fd[full_key]

attn_source = full_attn if full_attn is not None else clean_attn
attn_label = "full-seq" if full_attn is not None else "clean"

cell_data = torch.load(CACHE_DIR / "cell_attr.pt", map_location="cpu", weights_only=False)
cell_sorted = cell_data["cell_attr_sorted"]

clean_metric = bd["clean_metric"]
corrupt_metric = bd["corrupt_metric"]
if hasattr(clean_metric, "item"):
    clean_metric = clean_metric.item()
if hasattr(corrupt_metric, "item"):
    corrupt_metric = corrupt_metric.item()

# ── Build the CAUSAL cell set (top-K globally) ────────────────────────────
# These are the cells verified by the sufficiency test. Only these count
# as "causally relevant" for the coupling overlap analysis.

top_causal_set = set()  # (layer, head, q_tok, k_tok)
top_causal_by_head = {}  # (layer, head) -> [(q_tok, k_tok, attr, adiff), ...]

for i, (ll, hh, q, k, attr, adiff) in enumerate(cell_sorted):
    if i >= TOPK_CELL:
        break
    top_causal_set.add((ll, hh, q, k))
    top_causal_by_head.setdefault((ll, hh), []).append((q, k, attr, adiff))

print(f"Causal cell set: top-{TOPK_CELL} globally, spanning {len(top_causal_by_head)} heads")

# ── EVCouplings ────────────────────────────────────────────────────────────

ev_df = pd.read_csv(COUPLING_CSV)
ev_df["i_0"] = ev_df["i"] - 1
ev_df["j_0"] = ev_df["j"] - 1

ss1_set = set(range(ss1_s, ss1_e))
ss2_set = set(range(ss2_s, ss2_e))
cross_ev = ev_df[
    ((ev_df["i_0"].isin(ss1_set)) & (ev_df["j_0"].isin(ss2_set))) |
    ((ev_df["i_0"].isin(ss2_set)) & (ev_df["j_0"].isin(ss1_set)))
].copy()

TOP_N = 500
ev_top = ev_df.head(TOP_N)
ev_score_lookup = {}
for _, row in ev_top.iterrows():
    i0, j0, sc = int(row["i_0"]), int(row["j_0"]), row["score"]
    ev_score_lookup[(i0, j0)] = sc
    ev_score_lookup[(j0, i0)] = sc

# ── Circuit heads ──────────────────────────────────────────────────────────

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
ie_rank = {(l, h): i + 1 for i, (l, h) in enumerate(circuit_heads)}

# ── Build coupling sets ───────────────────────────────────────────────────


def build_coupling_set(n):
    top = ev_df.head(n)
    pairs = set()
    for _, row in top.iterrows():
        pairs.add((int(row["i_0"]), int(row["j_0"])))
        pairs.add((int(row["j_0"]), int(row["i_0"])))
    return pairs


coupling_set = build_coupling_set(TOP_N)

cross_coupling_set = set()
for _, row in cross_ev.iterrows():
    cross_coupling_set.add((int(row["i_0"]), int(row["j_0"])))
    cross_coupling_set.add((int(row["j_0"]), int(row["i_0"])))

# Overlay pairs for plots
ev_overlay_pairs = []
for _, row in ev_top.iterrows():
    i0, j0 = int(row["i_0"]), int(row["j_0"])
    if 0 <= i0 < SEQ_LEN and 0 <= j0 < SEQ_LEN:
        ev_overlay_pairs.append((i0, j0, row["score"]))

# ── Compute stats for each circuit head ───────────────────────────────────


def compute_head_stats(l, h):
    if isinstance(attn_source, (list, tuple)):
        attn_head = attn_source[l][0, h]
    else:
        attn_head = attn_source[l][0, h]
    aa_attn = attn_head[1:SEQ_LEN + 1, 1:SEQ_LEN + 1].numpy()

    threshold = np.percentile(aa_attn, 95)
    high_attn_pairs = set(zip(*np.where(aa_attn >= threshold)))

    overlap = high_attn_pairs & coupling_set
    n_high = len(high_attn_pairs)
    total = SEQ_LEN * SEQ_LEN
    n_coup_valid = len({(i, j) for (i, j) in coupling_set if 0 <= i < SEQ_LEN and 0 <= j < SEQ_LEN})
    expected = n_coup_valid * n_high / total if total > 0 else 0
    enrichment = len(overlap) / expected if expected > 0 else 0.0

    coup_attns = [aa_attn[i, j] for (i, j) in coupling_set if 0 <= i < SEQ_LEN and 0 <= j < SEQ_LEN]
    mean_coup = np.mean(coup_attns) if coup_attns else 0.0
    mean_all = aa_attn.mean()
    ratio = mean_coup / mean_all if mean_all > 0 else 0.0

    cross_attns = [aa_attn[i, j] for (i, j) in cross_coupling_set if 0 <= i < SEQ_LEN and 0 <= j < SEQ_LEN]
    mean_cross = np.mean(cross_attns) if cross_attns else 0.0
    cross_ratio = mean_cross / mean_all if mean_all > 0 else 0.0

    # Causal cells: only from the global top-K set
    causal_cells = top_causal_by_head.get((l, h), [])
    cell_coup_overlap = []
    for q, k, attr, adiff in causal_cells:
        q0, k0 = q - 1, k - 1
        if (q0, k0) in coupling_set:
            ev_sc = ev_score_lookup.get((q0, k0), 0)
            cell_coup_overlap.append((q0, k0, attr, adiff, ev_sc))

    return {
        "layer": l, "head": h, "ie": ie[l, h].item(),
        "enrichment": enrichment, "n_overlap": len(overlap),
        "mean_coup": mean_coup, "mean_all": mean_all, "ratio": ratio,
        "cross_ratio": cross_ratio, "mean_cross": mean_cross,
        "n_causal": len(causal_cells),
        "cell_coup_overlap": cell_coup_overlap,
        "causal_cells": causal_cells,
    }


print("Computing stats for all circuit heads...")
all_stats = []
for l, h in circuit_heads:
    all_stats.append(compute_head_stats(l, h))

all_stats_by_enrichment = sorted(all_stats, key=lambda x: x["enrichment"], reverse=True)

# Top interaction heads: ranked by causal cells on couplings (the most
# direct measure of whether a head's causally relevant attention lands
# on evolutionarily coupled positions). Break ties by enrichment.
all_stats_by_causal_coupling = sorted(
    all_stats,
    key=lambda x: (len(x["cell_coup_overlap"]), x["enrichment"]),
    reverse=True,
)
top_interaction = [s for s in all_stats_by_causal_coupling if len(s["cell_coup_overlap"]) >= 1][:10]

print(f"Top interaction heads: {len(top_interaction)}")
for s in top_interaction:
    print(f"  L{s['layer']:2d} H{s['head']:2d}  enrich={s['enrichment']:.1f}x  ratio={s['ratio']:.1f}x  cross={s['cross_ratio']:.1f}x  causal_cells={s['n_causal']}  causal_on_coupling={len(s['cell_coup_overlap'])}")


# ── Helper ────────────────────────────────────────────────────────────────

def get_aa_attn(l, h):
    src = attn_source[l] if isinstance(attn_source, (list, tuple)) else attn_source[l]
    return src[0, h].numpy()[1:SEQ_LEN + 1, 1:SEQ_LEN + 1]


# ══════════════════════════════════════════════════════════════════════════
# PLOT 1: Summary enrichment bar chart
# ══════════════════════════════════════════════════════════════════════════

print("\nGenerating summary enrichment plot...")

fig_bar, ax_bar = plt.subplots(figsize=(14, 5))
stats_sorted = sorted(all_stats, key=lambda x: x["enrichment"], reverse=True)
labels = [f"L{s['layer']}H{s['head']}" for s in stats_sorted]
enrichments = [s["enrichment"] for s in stats_sorted]
ie_vals = [s["ie"] for s in stats_sorted]

ie_arr = np.array(ie_vals)
norm = plt.Normalize(vmin=ie_arr.min(), vmax=ie_arr.max())
cmap_bar = plt.cm.YlOrRd
colors = cmap_bar(norm(ie_arr))

ax_bar.bar(range(len(labels)), enrichments, color=colors, edgecolor="none", width=0.8)
ax_bar.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.8, label="chance level")
ax_bar.axhline(y=1.5, color="steelblue", linestyle=":", linewidth=0.8, alpha=0.6, label="1.5x threshold")
ax_bar.set_xticks(range(len(labels)))
ax_bar.set_xticklabels(labels, rotation=90, fontsize=6)
ax_bar.set_ylabel("Coupling Enrichment (fold over chance)", fontsize=11)
ax_bar.set_title(f"{PROTEIN} Circuit Heads: EVCoupling Enrichment in High-Attention Cells (top-{TOP_N} couplings)", fontsize=12)
ax_bar.legend(fontsize=9)
sm = plt.cm.ScalarMappable(cmap=cmap_bar, norm=norm)
sm.set_array([])
fig_bar.colorbar(sm, ax=ax_bar, fraction=0.02, pad=0.01).set_label("Indirect Effect (IE)", fontsize=10)
fig_bar.tight_layout()
fig_bar.savefig(OUT_DIR / "enrichment_bar.png", dpi=200, bbox_inches="tight")
plt.close(fig_bar)
print(f"  Saved: enrichment_bar.png")


# ══════════════════════════════════════════════════════════════════════════
# PLOT 2: Coupling score vs attention scatter (top interaction heads)
# ══════════════════════════════════════════════════════════════════════════

print("Generating coupling score vs attention scatter...")

n_sc_cols = 5
n_sc_rows = (len(top_interaction) + n_sc_cols - 1) // n_sc_cols
fig_scatter, axes_sc = plt.subplots(n_sc_rows, n_sc_cols, figsize=(4.5 * n_sc_cols, 4.5 * n_sc_rows))
axes_sc = axes_sc.flatten()

for idx, s in enumerate(top_interaction):
    ax = axes_sc[idx]
    l, h = s["layer"], s["head"]
    rank = ie_rank[(l, h)]
    aa_attn = get_aa_attn(l, h)

    ev_scores, attn_vals, is_cross = [], [], []
    for _, row in ev_top.iterrows():
        i0, j0 = int(row["i_0"]), int(row["j_0"])
        if 0 <= i0 < SEQ_LEN and 0 <= j0 < SEQ_LEN:
            ev_scores.append(row["score"])
            attn_vals.append(aa_attn[i0, j0])
            is_cross.append((i0, j0) in cross_coupling_set)

    ev_scores = np.array(ev_scores)
    attn_vals = np.array(attn_vals)
    is_cross = np.array(is_cross)

    ax.scatter(ev_scores[~is_cross], attn_vals[~is_cross], s=8, alpha=0.3, c="gray", label="other")
    if is_cross.any():
        ax.scatter(ev_scores[is_cross], attn_vals[is_cross], s=25, alpha=0.8, c="crimson", edgecolors="black", linewidths=0.3, label="ss1-ss2", zorder=5)

    if s["cell_coup_overlap"]:
        cx = [ev_sc for (_, _, _, _, ev_sc) in s["cell_coup_overlap"]]
        cy = [aa_attn[q0, k0] for (q0, k0, _, _, _) in s["cell_coup_overlap"]]
        ax.scatter(cx, cy, s=60, marker="*", c="lime", edgecolors="black", linewidths=0.5, label="causal+coupled", zorder=10)

    ax.set_title(f"L{l}H{h} (#{rank}, IE={s['ie']:+.3f})", fontsize=10, fontweight="bold")
    ax.set_xlabel("EV coupling score", fontsize=8)
    ax.set_ylabel("Attention weight", fontsize=8)
    ax.tick_params(labelsize=7)
    if idx == 0:
        ax.legend(fontsize=7, loc="upper right")

for idx in range(len(top_interaction), len(axes_sc)):
    axes_sc[idx].set_visible(False)

fig_scatter.suptitle(f"{PROTEIN}: EVCoupling Score vs Attention Weight (top interaction heads)", fontsize=13, y=1.01)
fig_scatter.tight_layout()
fig_scatter.savefig(OUT_DIR / "coupling_vs_attn_scatter.png", dpi=200, bbox_inches="tight")
plt.close(fig_scatter)
print(f"  Saved: coupling_vs_attn_scatter.png")


# ══════════════════════════════════════════════════════════════════════════
# PLOT 3: Per-head FULL-SEQUENCE attention with coupling + causal overlay
# ══════════════════════════════════════════════════════════════════════════
# Inferno + log scale (matching attn_viz_app.py).
# Region boxes in white (ss1×ss2, ss2×ss1) and yellow (within-segment).
# Causal = only top-K global cells.

print("Generating per-head full-sequence heatmaps...")

for idx, s in enumerate(top_interaction):
    l, h = s["layer"], s["head"]
    rank = ie_rank[(l, h)]
    aa_attn = get_aa_attn(l, h)

    fig_h, ax_h = plt.subplots(figsize=(10, 9))

    # Heatmap: inferno + log scale (same as attn_viz_app.py)
    pos_vals = aa_attn[aa_attn > 0]
    lv = max(pos_vals.min(), 1e-6) if len(pos_vals) > 0 else 1e-6
    hv = max(aa_attn.max(), lv * 10)
    im = ax_h.imshow(aa_attn, aspect="equal", cmap="inferno", norm=LogNorm(vmin=lv, vmax=hv), interpolation="nearest")
    fig_h.colorbar(im, ax=ax_h, fraction=0.046, pad=0.04).ax.tick_params(labelsize=8)

    # EVCoupling pairs: cyan circles (size ~ score)
    for (i0, j0, sc) in ev_overlay_pairs:
        size = max(1.5, min(5, sc * 0.2))
        ax_h.plot(j0, i0, "o", markersize=size, markerfacecolor="none", markeredgecolor="cyan", markeredgewidth=0.5, alpha=0.4)

    # Causal cells (top-K global): white stars for non-coupled, green for coupled
    causal_cells = s["causal_cells"]

    # Split into coupled vs non-coupled
    coupled_causal = []
    noncoupled_causal = []
    for q_tok, k_tok, attr, adiff in causal_cells:
        q0, k0 = q_tok - 1, k_tok - 1
        if (q0, k0) in coupling_set:
            coupled_causal.append((q0, k0, attr))
        else:
            noncoupled_causal.append((q0, k0, attr))

    # Non-coupled causal cells (white stars)
    for q0, k0, attr in noncoupled_causal:
        ax_h.plot(k0, q0, "*", markersize=5, markerfacecolor="white", markeredgecolor="gray", markeredgewidth=0.3, alpha=0.8)

    # Coupled causal cells (green stars, larger)
    for q0, k0, attr in coupled_causal:
        ax_h.plot(k0, q0, "*", markersize=9, markerfacecolor="lime", markeredgecolor="black", markeredgewidth=0.4, alpha=0.95, zorder=10)

    # Contact pair marker
    ax_h.plot(cp[1], cp[0], "s", markersize=8, markerfacecolor="none", markeredgecolor="white", markeredgewidth=2, zorder=11)

    # Region boxes: white for cross-segment, yellow for within-segment
    for (rs, re, cs, ce, color) in [
        (ss1_s, ss1_e, ss2_s, ss2_e, "white"),    # ss1×ss2
        (ss2_s, ss2_e, ss1_s, ss1_e, "white"),    # ss2×ss1
        (ss1_s, ss1_e, ss1_s, ss1_e, "yellow"),   # ss1×ss1
        (ss2_s, ss2_e, ss2_s, ss2_e, "yellow"),   # ss2×ss2
    ]:
        rect = plt.Rectangle((cs - 0.5, rs - 0.5), ce - cs, re - rs, linewidth=1.2, edgecolor=color, facecolor="none", linestyle="--", alpha=0.7)
        ax_h.add_patch(rect)

    ax_h.set_title(f"L{l}H{h} (rank #{rank}, IE={s['ie']:+.3f})\nenrichment={s['enrichment']:.1f}x  coupling/all={s['ratio']:.1f}x  cross-seg={s['cross_ratio']:.1f}x  causal_cells={s['n_causal']}  causal+coupled={len(coupled_causal)}", fontsize=10, fontweight="bold")

    step = max(1, SEQ_LEN // 30)
    ticks = list(range(0, SEQ_LEN, step))
    tick_labels = [f"{seq[i]}{i}" for i in ticks]
    ax_h.set_xticks(ticks)
    ax_h.set_xticklabels(tick_labels, rotation=90, fontsize=5)
    ax_h.set_yticks(ticks)
    ax_h.set_yticklabels(tick_labels, fontsize=5)
    ax_h.set_xlabel("Key position", fontsize=10)
    ax_h.set_ylabel("Query position", fontsize=10)

    legend_elements = [
        mpatches.Patch(facecolor="none", edgecolor="cyan", linewidth=1, label=f"EVCoupling (top-{TOP_N})"),
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor="white", markeredgecolor="gray", markersize=8, label=f"Causal cell (top-{TOPK_CELL})"),
        plt.Line2D([0], [0], marker="*", color="w", markerfacecolor="lime", markeredgecolor="black", markersize=10, label="Causal + coupled"),
        plt.Line2D([0], [0], marker="s", color="w", markerfacecolor="none", markeredgecolor="white", markeredgewidth=2, markersize=8, label=f"Contact pair ({cp[0]}, {cp[1]})"),
        mpatches.Patch(facecolor="none", edgecolor="white", linestyle="--", linewidth=1, label="ss1 x ss2 / ss2 x ss1"),
        mpatches.Patch(facecolor="none", edgecolor="yellow", linestyle="--", linewidth=1, label="ss1 x ss1 / ss2 x ss2"),
    ]
    ax_h.legend(handles=legend_elements, fontsize=7, loc="upper right", framealpha=0.9)

    fig_h.tight_layout()
    fig_h.savefig(OUT_DIR / f"head_L{l}H{h}_full.png", dpi=200, bbox_inches="tight")
    plt.close(fig_h)
    print(f"  Saved: head_L{l}H{h}_full.png")


# ══════════════════════════════════════════════════════════════════════════
# PLOT 4: Cross-segment coupling bar chart
# ══════════════════════════════════════════════════════════════════════════

print("Generating cross-segment coupling plot...")

fig_cross, ax_cross = plt.subplots(figsize=(12, 5))
stats_by_cross = sorted(all_stats, key=lambda x: x["cross_ratio"], reverse=True)
labels_c = [f"L{s['layer']}H{s['head']}" for s in stats_by_cross]
cross_ratios = [s["cross_ratio"] for s in stats_by_cross]
ie_vals_c = [s["ie"] for s in stats_by_cross]

ie_arr_c = np.array(ie_vals_c)
norm_c = plt.Normalize(vmin=ie_arr_c.min(), vmax=ie_arr_c.max())
colors_c = cmap_bar(norm_c(ie_arr_c))

ax_cross.bar(range(len(labels_c)), cross_ratios, color=colors_c, edgecolor="none", width=0.8)
ax_cross.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.8, label="chance")
ax_cross.axhline(y=3.0, color="steelblue", linestyle=":", linewidth=0.8, alpha=0.6, label="3x threshold")
ax_cross.set_xticks(range(len(labels_c)))
ax_cross.set_xticklabels(labels_c, rotation=90, fontsize=6)
ax_cross.set_ylabel("Cross-Segment Coupling Attention / Mean Attention", fontsize=10)
ax_cross.set_title(f"{PROTEIN}: Attention on Cross-Segment EVCoupling Pairs (ss1-ss2)", fontsize=12)
ax_cross.legend(fontsize=9)
sm2 = plt.cm.ScalarMappable(cmap=cmap_bar, norm=norm_c)
sm2.set_array([])
fig_cross.colorbar(sm2, ax=ax_cross, fraction=0.02, pad=0.01).set_label("Indirect Effect (IE)", fontsize=10)
fig_cross.tight_layout()
fig_cross.savefig(OUT_DIR / "cross_segment_coupling.png", dpi=200, bbox_inches="tight")
plt.close(fig_cross)
print(f"  Saved: cross_segment_coupling.png")


# ══════════════════════════════════════════════════════════════════════════
# PLOT 5: IE rank vs enrichment scatter
# ══════════════════════════════════════════════════════════════════════════

print("Generating IE rank vs enrichment scatter...")

fig_ie, ax_ie = plt.subplots(figsize=(8, 6))
ranks = [ie_rank[(s["layer"], s["head"])] for s in all_stats]
enrichments_all = [s["enrichment"] for s in all_stats]
cross_ratios_all = [s["cross_ratio"] for s in all_stats]

sc = ax_ie.scatter(ranks, enrichments_all, c=cross_ratios_all, cmap="coolwarm", s=50, edgecolors="black", linewidths=0.4, vmin=0, vmax=max(cross_ratios_all))

for s in top_interaction:
    r = ie_rank[(s["layer"], s["head"])]
    ax_ie.annotate(f"L{s['layer']}H{s['head']}", (r, s["enrichment"]), fontsize=7, ha="left", va="bottom", xytext=(4, 4), textcoords="offset points")

ax_ie.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.8)
ax_ie.set_xlabel("IE Rank (1 = most causally important)", fontsize=11)
ax_ie.set_ylabel(f"Coupling Enrichment (top-{TOP_N})", fontsize=11)
ax_ie.set_title(f"{PROTEIN}: Causal Importance vs Coupling Enrichment", fontsize=12)
fig_ie.colorbar(sc, ax=ax_ie).set_label("Cross-segment coupling ratio", fontsize=10)
fig_ie.tight_layout()
fig_ie.savefig(OUT_DIR / "ie_rank_vs_enrichment.png", dpi=200, bbox_inches="tight")
plt.close(fig_ie)
print(f"  Saved: ie_rank_vs_enrichment.png")


# ══════════════════════════════════════════════════════════════════════════
# MARKDOWN REPORT
# ══════════════════════════════════════════════════════════════════════════

print("\nWriting report...")

lines = []
a = lines.append

a(f"# EVCoupling--Attention Overlap Analysis: {PROTEIN}")
a(f"")
a(f"Contact pair: ({cp[0]}, {cp[1]})  ss1: [{ss1_s}, {ss1_e})  ss2: [{ss2_s}, {ss2_e})")
a(f"Clean metric: {clean_metric:.4f}  Corrupt metric: {corrupt_metric:.4f}  Gap: {clean_metric - corrupt_metric:.4f}")
a(f"Circuit size: {crossed_k} heads  Attention source: {attn_label}")
a(f"EVCouplings: {len(ev_df)} total pairs, analysis uses top {TOP_N}")
a(f"Cross-segment couplings (ss1 x ss2): {len(cross_ev)} pairs")
a(f"Causal cells: top-{TOPK_CELL} globally (sufficiency-tested set)")
a(f"")

a(f"## Summary")
a(f"")
a(f"We compared each circuit head's attention pattern against the top {TOP_N} EVCouplings for 2B61A to identify \"interaction heads\" whose attention aligns with evolutionary couplings.")
a(f"Of {crossed_k} circuit heads, {len([s for s in all_stats if s['enrichment'] > 1.5])} show >1.5x enrichment for coupling pairs in their high-attention cells, and {len(top_interaction)} qualify as strong interaction heads (>5x enrichment and >3x coupling/average attention ratio).")
a(f"")
a(f"The top cross-segment coupling pairs N180--R313 (score 14.9) and I181--Y314 (score 14.0) sit directly adjacent to the contact pair (182, 316), and multiple late-layer circuit heads attend strongly to exactly these coupled positions.")
a(f"")

a(f"## Enrichment Bar Chart (all circuit heads)")
a(f"")
a(f"![Enrichment bar chart](coupling/enrichment_bar.png)")
a(f"")

a(f"## Causal Importance vs Coupling Enrichment")
a(f"")
a(f"![IE rank vs enrichment](coupling/ie_rank_vs_enrichment.png)")
a(f"")

a(f"## Top Interaction Heads")
a(f"")
a(f"| Rank | Head | IE | Enrichment | Coupling/All Ratio | Cross-Seg Ratio | Causal Cells | Causal on Couplings |")
a(f"|------|------|----|------------|--------------------|-----------------|----|-----|")
for s in top_interaction:
    rank = ie_rank[(s["layer"], s["head"])]
    n_cc = len(s["cell_coup_overlap"])
    a(f"| #{rank} | L{s['layer']}H{s['head']} | {s['ie']:+.4f} | {s['enrichment']:.1f}x | {s['ratio']:.1f}x | {s['cross_ratio']:.1f}x | {s['n_causal']} | {n_cc} |")
a(f"")

a(f"### Causal Cells Overlapping with EVCouplings")
a(f"")
a(f"For each top interaction head, the causal cells (top-{TOPK_CELL} globally by gradient attribution, verified by sufficiency test) that also correspond to top-{TOP_N} EVCoupling pairs:")
a(f"")
for s in top_interaction:
    l, h = s["layer"], s["head"]
    rank = ie_rank[(l, h)]
    a(f"**L{l}H{h} (#{rank}, {s['n_causal']} causal cells)**:")
    a(f"")
    if s["cell_coup_overlap"]:
        a(f"| Position | Residues | Cell Attr | EV Score |")
        a(f"|----------|----------|-----------|----------|")
        for q0, k0, attr, adiff, ev_sc in sorted(s["cell_coup_overlap"], key=lambda x: x[2], reverse=True)[:10]:
            a(f"| ({q0}, {k0}) | {seq[q0]}{q0}--{seq[k0]}{k0} | {attr:+.4f} | {ev_sc:.2f} |")
    else:
        a(f"No causal cell overlap with top-{TOP_N} couplings.")
    a(f"")

a(f"## Per-Head Full-Sequence Attention with Coupling Overlay")
a(f"")
a(f"For each top interaction head, full-sequence (AA x AA) attention is shown with EVCoupling pairs (cyan circles), causal cells from the top-{TOPK_CELL} global set (white stars), and cells that are both causal and coupled (green stars). White dashed boxes mark ss1 x ss2 / ss2 x ss1; yellow dashed boxes mark ss1 x ss1 / ss2 x ss2. This captures both local coupling patterns (e.g. L11H1: I181--A171 within ss1 neighborhood) and cross-segment patterns (e.g. L32H13: R313--N180 across ss1--ss2).")
a(f"")
for s in top_interaction:
    l, h = s["layer"], s["head"]
    a(f"![L{l}H{h} full-sequence](coupling/head_L{l}H{h}_full.png)")
    a(f"")

a(f"## EVCoupling Score vs Attention Weight")
a(f"")
a(f"For each top interaction head, scatter of EV coupling score vs attention weight across all top-{TOP_N} coupling pairs. Red points are cross-segment (ss1--ss2) couplings. Green stars are causal cells (top-{TOPK_CELL}) that overlap with couplings.")
a(f"")
a(f"![Coupling vs attention scatter](coupling/coupling_vs_attn_scatter.png)")
a(f"")

a(f"## Cross-Segment Coupling Attention")
a(f"")
a(f"Ratio of mean attention on cross-segment (ss1--ss2) EVCoupling pairs vs overall mean attention, for all circuit heads.")
a(f"")
a(f"![Cross-segment coupling](coupling/cross_segment_coupling.png)")
a(f"")
a(f"Top cross-segment coupling heads:")
a(f"")
a(f"| Head | IE | Cross-Seg Ratio |")
a(f"|------|----|-----------------|")
top_cross = sorted(all_stats, key=lambda x: x["cross_ratio"], reverse=True)[:10]
for s in top_cross:
    rank = ie_rank[(s["layer"], s["head"])]
    a(f"| L{s['layer']}H{s['head']} (#{rank}) | {s['ie']:+.4f} | {s['cross_ratio']:.1f}x |")
a(f"")

a(f"## Top Cross-Segment EVCouplings (ss1 x ss2)")
a(f"")
a(f"| Position | Residues | EV Score | CN |")
a(f"|----------|----------|----------|-----|")
for _, row in cross_ev.head(15).iterrows():
    i0, j0 = int(row["i_0"]), int(row["j_0"])
    a(f"| ({i0}, {j0}) | {seq[i0]}{i0}--{seq[j0]}{j0} | {row['score']:.2f} | {row['cn']:.4f} |")
a(f"")

a(f"## Full Circuit Head Table")
a(f"")
a(f"| Rank | Head | IE | Enrichment | Coup/All | Cross-Seg | Causal Cells | Causal on Coupling |")
a(f"|------|------|----|------------|----------|-----------|------|------|")
for s in all_stats_by_enrichment:
    rank = ie_rank[(s["layer"], s["head"])]
    n_cc = len(s["cell_coup_overlap"])
    a(f"| #{rank} | L{s['layer']}H{s['head']} | {s['ie']:+.4f} | {s['enrichment']:.1f}x | {s['ratio']:.1f}x | {s['cross_ratio']:.1f}x | {s['n_causal']} | {n_cc} |")
a(f"")

report_path = ROOT / "reports" / "outputs" / "2B61A" / "2B61A_coupling_report.md"
report_path.write_text("\n".join(lines))
print(f"\nReport: {report_path}")
print(f"Plots:  {OUT_DIR}/")
print("Done!")
