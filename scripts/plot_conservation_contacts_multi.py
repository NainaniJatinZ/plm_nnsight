"""
Polished multi-protein figures for conservation vs contact prediction.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy import stats as sp_stats

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 200,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "axes.spines.top": False,
    "axes.spines.right": False,
})

ESM_COLOR = "#3274A1"
EV_COLOR  = "#E1812C"
ACCENT    = "#3A923A"
GRAY      = "#888888"

OUT_DIR = "reports/outputs/multi_protein"
import os
os.makedirs(OUT_DIR, exist_ok=True)

N_BINS = 5
PROTEIN_ORDER = ["1BRTA", "1IN4A", "1PVGA", "1YKIA", "2B61A", "2DPMA", "2EK8A", "2FBQA"]

# ── Load data ────────────────────────────────────────────────────────────────
combined = pd.read_csv("reports/cache/multi_protein/conservation_pairs_all.csv")
summary = pd.read_csv("reports/cache/multi_protein/protein_summaries.csv")
corr_df = pd.read_csv("reports/cache/multi_protein/per_protein_correlations.csv")

combined_ev = combined.dropna(subset=["ev_score"]).copy()
contacts_all = combined[combined["gt_contact"] == 1]
contacts_ev = combined_ev[combined_ev["gt_contact"] == 1]

n_proteins = len(summary)
n_contacts_total = int(combined["gt_contact"].sum())


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Overall precision per protein (grouped bar: ESM vs EV)
# ══════════════════════════════════════════════════════════════════════════════
fig1, axes1 = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)

for ax, metric_label in zip(axes1, ["L", "L/2", "L/5"]):
    sdf = summary.sort_values("protein")
    x = np.arange(len(sdf))
    w = 0.35
    bars1 = ax.bar(x - w/2, sdf[f"esm_prec_{metric_label}"], w, label="ESM2", color=ESM_COLOR, zorder=3)
    bars2 = ax.bar(x + w/2, sdf[f"ev_prec_{metric_label}"], w, label="EVcouplings", color=EV_COLOR, zorder=3)

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            if not np.isnan(h):
                ax.text(bar.get_x() + bar.get_width()/2, h + 0.008,
                        f".{int(h*100):02d}", ha="center", va="bottom", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels(sdf["protein"], rotation=45, ha="right", fontsize=9)
    ax.set_title(f"Top-{metric_label}")
    ax.set_ylim(0, 1.1)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
    ax.grid(axis="y", alpha=0.3, zorder=0)
    if metric_label == "L":
        ax.set_ylabel("Precision")
        ax.legend(frameon=False, loc="lower left")

fig1.suptitle(f"Contact prediction accuracy across {n_proteins} proteins", fontsize=14, y=1.02)
fig1.tight_layout()
fig1.savefig(f"{OUT_DIR}/fig1_overall_precision.png")
print(f"Saved {OUT_DIR}/fig1_overall_precision.png")
plt.close(fig1)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Correlation scatter: conservation vs score (pooled, true contacts)
#             Side-by-side: ESM2 (left) and EVcouplings (right)
# ══════════════════════════════════════════════════════════════════════════════
fig2, (ax_esm, ax_ev) = plt.subplots(1, 2, figsize=(11, 5))

# Normalize scores within each protein for pooling
contacts_all_c = contacts_all.copy()
contacts_all_c["esm_norm"] = contacts_all_c.groupby("protein")["pred_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
contacts_ev_c = contacts_ev.copy()
contacts_ev_c["ev_norm"] = contacts_ev_c.groupby("protein")["ev_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
contacts_ev_c["esm_norm"] = contacts_ev_c.groupby("protein")["pred_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)

for ax, score_col, color, method_name, data in [
    (ax_esm, "esm_norm", ESM_COLOR, "ESM2", contacts_ev_c),
    (ax_ev, "ev_norm", EV_COLOR, "EVcouplings", contacts_ev_c),
]:
    # Color by protein
    for pid in PROTEIN_ORDER:
        mask = data["protein"] == pid
        if mask.sum() == 0:
            continue
        ax.scatter(data.loc[mask, "pair_cons_mean"], data.loc[mask, score_col],
                   alpha=0.25, s=10, edgecolors="none", zorder=2, label=pid)

    # Overall regression line
    x_vals = data["pair_cons_mean"].values
    y_vals = data[score_col].values
    slope, intercept, r, p, _ = sp_stats.linregress(x_vals, y_vals)
    x_fit = np.linspace(x_vals.min(), x_vals.max(), 100)
    ax.plot(x_fit, slope * x_fit + intercept, color="black", lw=2, ls="--", zorder=5)

    p_str = f"p = {p:.1e}" if p < 0.01 else f"p = {p:.3f}"
    ax.text(0.97, 0.97, f"r = {r:.3f}\n{p_str}\nn = {len(data)}",
            transform=ax.transAxes, ha="right", va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, alpha=0.9))

    ax.set_xlabel("Mean pair conservation")
    ax.set_ylabel(f"{method_name} score (z-normalized per protein)")
    ax.set_title(f"{method_name}")
    ax.grid(alpha=0.15, zorder=0)

ax_esm.legend(fontsize=7, frameon=False, loc="lower left", ncol=2, markerscale=1.5)
fig2.suptitle(f"Score vs conservation for true contacts ({n_proteins} proteins pooled)", fontsize=14, y=1.02)
fig2.tight_layout()
fig2.savefig(f"{OUT_DIR}/fig2_correlation_scatter.png")
print(f"Saved {OUT_DIR}/fig2_correlation_scatter.png")
plt.close(fig2)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Precision@K by conservation bin (pooled across proteins)
#             Uses within-protein ranking to avoid scale differences
# ══════════════════════════════════════════════════════════════════════════════

# For pooled precision by conservation bin:
# Within each protein, rank pairs. For each conservation bin (pooled), compute
# precision at top-K where K = number of true contacts in that bin.
combined_c = combined.copy()
combined_c["esm_rank"] = combined_c.groupby("protein")["pred_score"].rank(pct=True)
combined_ev_c2 = combined_ev.copy()
combined_ev_c2["ev_rank"] = combined_ev_c2.groupby("protein")["ev_score"].rank(pct=True)
combined_ev_c2["esm_rank"] = combined_ev_c2.groupby("protein")["pred_score"].rank(pct=True)

combined_ev_c2["cons_bin"] = pd.qcut(combined_ev_c2["pair_cons_mean"], q=N_BINS, duplicates="drop")

fig3, ax = plt.subplots(figsize=(7, 4.5))

esm_precs = []
ev_precs = []
bin_labels = []
bin_n_contacts = []

for label, grp in combined_ev_c2.groupby("cons_bin", observed=True):
    n_true = int(grp["gt_contact"].sum())
    if n_true == 0:
        continue
    esm_top = grp.nlargest(n_true, "esm_rank")
    ev_top = grp.nlargest(n_true, "ev_rank")
    esm_precs.append(esm_top["gt_contact"].mean())
    ev_precs.append(ev_top["gt_contact"].mean())
    bin_labels.append(f"{label.left:.2f}-{label.right:.2f}")
    bin_n_contacts.append(n_true)

x = np.arange(len(bin_labels))
w = 0.35

bars1 = ax.bar(x - w/2, esm_precs, w, label="ESM2", color=ESM_COLOR, zorder=3)
bars2 = ax.bar(x + w/2, ev_precs, w, label="EVcouplings", color=EV_COLOR, zorder=3)

for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.008,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

for i, nc in enumerate(bin_n_contacts):
    ax.text(x[i], -0.06, f"n={nc}", ha="center", va="top",
            fontsize=8, color=GRAY, transform=ax.get_xaxis_transform())

ax.set_xticks(x)
ax.set_xticklabels(bin_labels, fontsize=9)
ax.set_xlabel("Mean pair conservation (quintile)")
ax.set_ylabel("Precision @ K")
ax.set_ylim(0, 0.85)
ax.set_title(f"Contact precision by conservation ({n_proteins} proteins pooled)")
ax.legend(frameon=False, loc="upper right")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
ax.grid(axis="y", alpha=0.3, zorder=0)

fig3.tight_layout()
fig3.savefig(f"{OUT_DIR}/fig3_precision_by_conservation.png")
print(f"Saved {OUT_DIR}/fig3_precision_by_conservation.png")
plt.close(fig3)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Confidence on true contacts by conservation bin
#             Separate panels for ESM2 and EVcouplings, using z-normalized scores
# ══════════════════════════════════════════════════════════════════════════════
contacts_ev_binned = contacts_ev.copy()
contacts_ev_binned["esm_norm"] = contacts_ev_binned.groupby("protein")["pred_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
contacts_ev_binned["ev_norm"] = contacts_ev_binned.groupby("protein")["ev_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
contacts_ev_binned["cons_bin"] = pd.qcut(contacts_ev_binned["pair_cons_mean"], q=N_BINS, duplicates="drop")

fig4, (ax_esm, ax_ev) = plt.subplots(1, 2, figsize=(11, 4.5))

esm_means = []
ev_means = []
labels4 = []
for label, grp in contacts_ev_binned.groupby("cons_bin", observed=True):
    esm_means.append(grp["esm_norm"].mean())
    ev_means.append(grp["ev_norm"].mean())
    labels4.append(f"{label.left:.2f}-{label.right:.2f}")

x4 = np.arange(len(labels4))

ax_esm.bar(x4, esm_means, 0.55, color=ESM_COLOR, zorder=3)
for i, v in enumerate(esm_means):
    ax_esm.text(i, v + 0.02 * (1 if v >= 0 else -1), f"{v:.2f}", ha="center",
                va="bottom" if v >= 0 else "top", fontsize=9)
ax_esm.set_xticks(x4)
ax_esm.set_xticklabels(labels4, fontsize=9)
ax_esm.set_xlabel("Mean pair conservation (quintile)")
ax_esm.set_ylabel("Mean z-score (true contacts)")
ax_esm.set_title("ESM2")
ax_esm.axhline(0, color=GRAY, lw=0.8, ls="-", alpha=0.5)
ax_esm.grid(axis="y", alpha=0.3, zorder=0)

ax_ev.bar(x4, ev_means, 0.55, color=EV_COLOR, zorder=3)
for i, v in enumerate(ev_means):
    ax_ev.text(i, v + 0.02 * (1 if v >= 0 else -1), f"{v:.2f}", ha="center",
               va="bottom" if v >= 0 else "top", fontsize=9)
ax_ev.set_xticks(x4)
ax_ev.set_xticklabels(labels4, fontsize=9)
ax_ev.set_xlabel("Mean pair conservation (quintile)")
ax_ev.set_ylabel("Mean z-score (true contacts)")
ax_ev.set_title("EVcouplings")
ax_ev.axhline(0, color=GRAY, lw=0.8, ls="-", alpha=0.5)
ax_ev.grid(axis="y", alpha=0.3, zorder=0)

fig4.suptitle(f"Confidence on true contacts by conservation ({n_proteins} proteins)", fontsize=14, y=1.02)
fig4.tight_layout()
fig4.savefig(f"{OUT_DIR}/fig4_confidence_by_conservation.png")
print(f"Saved {OUT_DIR}/fig4_confidence_by_conservation.png")
plt.close(fig4)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Caveat: contact density increases with conservation (pooled)
# ══════════════════════════════════════════════════════════════════════════════
fig5, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

# Panel A: Conservation density: contacts vs non-contacts (pooled)
cons_c = combined.loc[combined["gt_contact"] == 1, "pair_cons_mean"]
cons_nc = combined.loc[combined["gt_contact"] == 0, "pair_cons_mean"]
ax1.hist(cons_c, bins=40, alpha=0.65, label=f"True contacts (n={len(cons_c)})",
         density=True, color=ACCENT, edgecolor="white", lw=0.5, zorder=3)
ax1.hist(cons_nc, bins=40, alpha=0.45, label=f"Non-contacts",
         density=True, color=GRAY, edgecolor="white", lw=0.5, zorder=2)
ax1.axvline(cons_c.median(), color=ACCENT, ls="--", lw=1, alpha=0.8, label=f"Contact median ({cons_c.median():.2f})")
ax1.axvline(cons_nc.median(), color=GRAY, ls="--", lw=1, alpha=0.8, label=f"Non-contact median ({cons_nc.median():.2f})")
ax1.set_xlabel("Mean pair conservation")
ax1.set_ylabel("Density")
ax1.set_title("Contacts are enriched at higher conservation")
ax1.legend(frameon=False, fontsize=8)
ax1.grid(axis="y", alpha=0.2, zorder=0)

# Panel B: Contact rate by conservation bin
combined_binned = combined.copy()
combined_binned["cons_bin"] = pd.qcut(combined_binned["pair_cons_mean"], q=N_BINS, duplicates="drop")

rates = []
for label, grp in combined_binned.groupby("cons_bin", observed=True):
    n_true = grp["gt_contact"].sum()
    rates.append({"bin": label, "rate": n_true / len(grp) * 100, "n_contacts": int(n_true)})

rates_df = pd.DataFrame(rates)
x5 = np.arange(len(rates_df))
ax2.bar(x5, rates_df["rate"], 0.55, color=ACCENT, zorder=3, alpha=0.8)
for i, row in rates_df.iterrows():
    ax2.text(i, row["rate"] + 0.03, f"{int(row['n_contacts'])}", ha="center", va="bottom", fontsize=9, color=GRAY)

bin_labels5 = [f"{b.left:.2f}-{b.right:.2f}" for b in rates_df["bin"]]
ax2.set_xticks(x5)
ax2.set_xticklabels(bin_labels5, fontsize=9)
ax2.set_xlabel("Mean pair conservation (quintile)")
ax2.set_ylabel("Contact rate (%)")
ax2.set_title("Contact density increases with conservation")
ax2.grid(axis="y", alpha=0.3, zorder=0)

fig5.suptitle("Caveat: conserved residues have more contacts (core enrichment)", fontsize=13, y=1.02)
fig5.tight_layout()
fig5.savefig(f"{OUT_DIR}/fig5_confound_conservation_density.png")
print(f"Saved {OUT_DIR}/fig5_confound_conservation_density.png")
plt.close(fig5)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — ESM2 vs EVcouplings scatter (true contacts, pooled)
# ══════════════════════════════════════════════════════════════════════════════
fig6, ax = plt.subplots(figsize=(6.5, 5.5))

# Normalize within protein for fair pooling
contacts_ev_plot = contacts_ev.copy()
contacts_ev_plot["esm_norm"] = contacts_ev_plot.groupby("protein")["pred_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)
contacts_ev_plot["ev_norm"] = contacts_ev_plot.groupby("protein")["ev_score"].transform(
    lambda s: (s - s.mean()) / s.std() if s.std() > 0 else 0
)

sc = ax.scatter(
    contacts_ev_plot["ev_norm"], contacts_ev_plot["esm_norm"],
    c=contacts_ev_plot["pair_cons_mean"], cmap="RdYlGn_r",
    alpha=0.4, s=12, edgecolors="none", zorder=2,
    vmin=contacts_ev_plot["pair_cons_mean"].quantile(0.05),
    vmax=contacts_ev_plot["pair_cons_mean"].quantile(0.95),
)
cbar = plt.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label("Mean pair conservation", fontsize=10)

r, p = sp_stats.pearsonr(contacts_ev_plot["ev_norm"], contacts_ev_plot["esm_norm"])
ax.text(0.03, 0.97, f"r = {r:.3f}, p = {p:.1e}\nn = {len(contacts_ev_plot)} contacts\n{n_proteins} proteins",
        transform=ax.transAxes, ha="left", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, alpha=0.9))

ax.axhline(0, color=GRAY, lw=0.5, ls=":", alpha=0.5)
ax.axvline(0, color=GRAY, lw=0.5, ls=":", alpha=0.5)
ax.set_xlabel("EVcouplings score (z-normalized)")
ax.set_ylabel("ESM2 score (z-normalized)")
ax.set_title(f"ESM2 vs EVcouplings (true contacts, {n_proteins} proteins)")
ax.grid(alpha=0.15, zorder=0)

fig6.tight_layout()
fig6.savefig(f"{OUT_DIR}/fig6_esm_vs_ev_scatter.png")
print(f"Saved {OUT_DIR}/fig6_esm_vs_ev_scatter.png")
plt.close(fig6)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 — Per-protein correlation forest plot
#             Shows r(conservation, score) for each protein, both methods
# ══════════════════════════════════════════════════════════════════════════════
fig7, ax = plt.subplots(figsize=(6, 5))

corr_sorted = corr_df.sort_values("protein")
y_pos = np.arange(len(corr_sorted))

ax.barh(y_pos + 0.18, corr_sorted["r_esm"], height=0.32, color=ESM_COLOR, label="ESM2", zorder=3, alpha=0.85)
ax.barh(y_pos - 0.18, corr_sorted["r_ev"], height=0.32, color=EV_COLOR, label="EVcouplings", zorder=3, alpha=0.85)

# Add significance markers
for i, (_, row) in enumerate(corr_sorted.iterrows()):
    for r_col, p_col, offset in [("r_esm", "p_esm", 0.18), ("r_ev", "p_ev", -0.18)]:
        r_val = row[r_col]
        p_val = row[p_col]
        if pd.isna(r_val):
            continue
        marker = ""
        if p_val < 0.001:
            marker = "***"
        elif p_val < 0.01:
            marker = "**"
        elif p_val < 0.05:
            marker = "*"
        if marker:
            x_offset = 0.01 if r_val >= 0 else -0.01
            ha = "left" if r_val >= 0 else "right"
            ax.text(r_val + x_offset, y_pos[i] + offset, marker, ha=ha, va="center", fontsize=8, color="black")

    # Contact count annotation
    ax.text(-0.42, y_pos[i], f"n={int(row['n_contacts'])}", ha="right", va="center", fontsize=8, color=GRAY)

ax.axvline(0, color="black", lw=0.8, zorder=4)
ax.set_yticks(y_pos)
ax.set_yticklabels(corr_sorted["protein"], fontsize=10)
ax.set_xlabel("Pearson r (score vs mean pair conservation)")
ax.set_title("Per-protein correlation\n(true contacts only)")
ax.legend(frameon=False, loc="lower right")
ax.grid(axis="x", alpha=0.3, zorder=0)
ax.set_xlim(-0.42, 0.42)

fig7.tight_layout()
fig7.savefig(f"{OUT_DIR}/fig7_per_protein_correlation.png")
print(f"Saved {OUT_DIR}/fig7_per_protein_correlation.png")
plt.close(fig7)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 8 — Method agreement: pooled across proteins
# ══════════════════════════════════════════════════════════════════════════════
# Within each protein, define top-L predictions as "predicted contact"
combined_ev_agree = combined_ev.copy()

all_cats = []
for pid, grp in combined_ev_agree.groupby("protein"):
    n_res = len(grp["i"].unique()) + 6  # approximate
    # Use per-protein percentile threshold: top fraction = n_contacts / n_pairs
    n_true = int(grp["gt_contact"].sum())
    esm_thresh = grp["pred_score"].nlargest(n_true * 2).iloc[-1] if n_true > 0 else 0
    ev_thresh = grp["ev_score"].nlargest(n_true * 2).iloc[-1] if n_true > 0 else 0

    grp = grp.copy()
    # Use top-L as threshold (L = number of structured residues for this protein)
    n_struct = summary.loc[summary["protein"] == pid, "n_residues"].values[0]
    esm_thresh = grp["pred_score"].nlargest(n_struct).iloc[-1]
    ev_thresh = grp["ev_score"].nlargest(n_struct).iloc[-1]
    grp["esm_hit"] = (grp["pred_score"] >= esm_thresh).astype(int)
    grp["ev_hit"] = (grp["ev_score"] >= ev_thresh).astype(int)
    all_cats.append(grp[grp["gt_contact"] == 1][["protein", "pair_cons_mean", "esm_hit", "ev_hit"]])

agree_df = pd.concat(all_cats, ignore_index=True)

both_hit  = agree_df[(agree_df["esm_hit"] == 1) & (agree_df["ev_hit"] == 1)]
esm_only  = agree_df[(agree_df["esm_hit"] == 1) & (agree_df["ev_hit"] == 0)]
ev_only   = agree_df[(agree_df["esm_hit"] == 0) & (agree_df["ev_hit"] == 1)]
both_miss = agree_df[(agree_df["esm_hit"] == 0) & (agree_df["ev_hit"] == 0)]

fig8, ax = plt.subplots(figsize=(7, 5))

categories = ["Both hit", "ESM2 only", "EV only", "Both miss"]
counts = [len(both_hit), len(esm_only), len(ev_only), len(both_miss)]
mean_cons = [g["pair_cons_mean"].mean() for g in [both_hit, esm_only, ev_only, both_miss]]
colors_cat = [ACCENT, ESM_COLOR, EV_COLOR, GRAY]

bars = ax.bar(np.arange(4), counts, 0.55, color=colors_cat, zorder=3, alpha=0.85)
for i, (bar, mc, c) in enumerate(zip(bars, mean_cons, counts)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
            f"n = {c}\ncons = {mc:.3f}", ha="center", va="bottom", fontsize=9)

ax.set_xticks(np.arange(4))
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylabel("Number of true contacts")
ax.set_title(f"Method agreement on true contacts (top-L, {n_proteins} proteins)")
ax.grid(axis="y", alpha=0.3, zorder=0)

fig8.tight_layout()
fig8.savefig(f"{OUT_DIR}/fig8_method_agreement.png")
print(f"Saved {OUT_DIR}/fig8_method_agreement.png")
plt.close(fig8)


print(f"\nAll {n_proteins}-protein figures saved to {OUT_DIR}/")
