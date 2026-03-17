"""
Polished figures for the conservation-vs-contact-prediction experiment.
Reads cached data from reports/cache/2B61A/.
Protein: 2B61A (homoserine O-acetyltransferase, H. influenzae), N=349 structured residues.
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

ESM_COLOR = "#3274A1"   # muted blue
EV_COLOR  = "#E1812C"   # muted orange
ACCENT    = "#3A923A"   # green for annotations
GRAY      = "#888888"

OUT_DIR = "reports/outputs/2B61A"
N_PDB = 349  # structured residues in 2B61A
N_BINS = 5

# ── Load data ────────────────────────────────────────────────────────────────
df_all = pd.read_csv("reports/cache/2B61A/conservation_pairs.csv")
df_ev  = pd.read_csv("reports/cache/2B61A/conservation_pairs_with_ev.csv")

contacts_all = df_all[df_all["gt_contact"] == 1]
contacts_ev  = df_ev[df_ev["gt_contact"] == 1]


# ── Helper: bin labels ───────────────────────────────────────────────────────
def make_bins(df, col="pair_cons_mean", n=N_BINS):
    df = df.copy()
    df["cons_bin"] = pd.qcut(df[col], q=n, duplicates="drop")
    return df

def bin_precision(df, score_col, n=N_BINS):
    df = make_bins(df)
    rows = []
    for label, grp in df.groupby("cons_bin", observed=True):
        n_true = int(grp["gt_contact"].sum())
        if n_true == 0:
            continue
        top_k = grp.nlargest(n_true, score_col)
        rows.append({
            "bin": label,
            "bin_mid": label.mid,
            "n_contacts": n_true,
            "n_pairs": len(grp),
            "precision": top_k["gt_contact"].mean(),
            "mean_score_contacts": grp.loc[grp["gt_contact"] == 1, score_col].mean(),
        })
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Overall precision comparison (bar chart)
# ══════════════════════════════════════════════════════════════════════════════
fig1, ax = plt.subplots(figsize=(5, 4))

metrics = []
for divisor, label in [(1, "L"), (2, "L/2"), (5, "L/5")]:
    k = N_PDB // divisor
    esm_prec = df_ev.nlargest(k, "pred_score")["gt_contact"].mean()
    ev_prec  = df_ev.nlargest(k, "ev_score")["gt_contact"].mean()
    metrics.append({"k_label": label, "ESM2": esm_prec, "EVcouplings": ev_prec})

mdf = pd.DataFrame(metrics)
x = np.arange(len(mdf))
w = 0.32
bars1 = ax.bar(x - w/2, mdf["ESM2"], w, label="ESM2", color=ESM_COLOR, zorder=3)
bars2 = ax.bar(x + w/2, mdf["EVcouplings"], w, label="EVcouplings", color=EV_COLOR, zorder=3)

for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels([f"Top-{l}" for l in mdf["k_label"]])
ax.set_ylabel("Precision")
ax.set_ylim(0, 1.05)
ax.set_title("Contact prediction accuracy\n(2B61A, 805 true contacts)")
ax.legend(frameon=False)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
ax.grid(axis="y", alpha=0.3, zorder=0)

fig1.savefig(f"{OUT_DIR}/fig1_overall_precision.png")
print(f"Saved {OUT_DIR}/fig1_overall_precision.png")
plt.close(fig1)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Correlation: conservation vs predicted score (true contacts)
#             Side-by-side: ESM2 (left) and EVcouplings (right)
# ══════════════════════════════════════════════════════════════════════════════
fig2, (ax_esm, ax_ev) = plt.subplots(1, 2, figsize=(10, 4.5))

for ax, score_col, color, method_name, data in [
    (ax_esm, "pred_score", ESM_COLOR, "ESM2", contacts_ev),
    (ax_ev, "ev_score", EV_COLOR, "EVcouplings", contacts_ev),
]:
    x_vals = data["pair_cons_mean"].values
    y_vals = data[score_col].values

    ax.scatter(x_vals, y_vals, c=color, alpha=0.35, s=12, edgecolors="none", zorder=2)

    # Regression line
    slope, intercept, r, p, _ = sp_stats.linregress(x_vals, y_vals)
    x_fit = np.linspace(x_vals.min(), x_vals.max(), 100)
    ax.plot(x_fit, slope * x_fit + intercept, color="black", lw=1.5, ls="--", zorder=3)

    # Annotation
    p_str = f"p = {p:.1e}" if p < 0.01 else f"p = {p:.3f}"
    ax.text(0.97, 0.97, f"r = {r:.3f}\n{p_str}\nn = {len(data)}",
            transform=ax.transAxes, ha="right", va="top", fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, alpha=0.9))

    ax.set_xlabel("Mean pair conservation")
    ax.set_ylabel(f"{method_name} contact score")
    ax.set_title(f"{method_name}")
    ax.grid(alpha=0.2, zorder=0)

fig2.suptitle("Score vs conservation for true contacts", fontsize=14, y=1.02)
fig2.tight_layout()
fig2.savefig(f"{OUT_DIR}/fig2_correlation_scatter.png")
print(f"Saved {OUT_DIR}/fig2_correlation_scatter.png")
plt.close(fig2)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Precision@K by conservation bin (grouped bar)
# ══════════════════════════════════════════════════════════════════════════════
esm_bins = bin_precision(df_ev, "pred_score")
ev_bins  = bin_precision(df_ev, "ev_score")

fig3, ax = plt.subplots(figsize=(7, 4.5))
x = np.arange(len(esm_bins))
w = 0.35

bars1 = ax.bar(x - w/2, esm_bins["precision"], w, label="ESM2", color=ESM_COLOR, zorder=3)
bars2 = ax.bar(x + w/2, ev_bins["precision"], w, label="EVcouplings", color=EV_COLOR, zorder=3)

# Value labels
for bars in [bars1, bars2]:
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

# X labels: conservation range
bin_labels = [f"{b.left:.2f}-{b.right:.2f}" for b in esm_bins["bin"]]
ax.set_xticks(x)
ax.set_xticklabels(bin_labels, fontsize=9)
ax.set_xlabel("Mean pair conservation (quintile)")
ax.set_ylabel("Precision @ K")
ax.set_ylim(0, 0.85)
ax.set_title("Contact precision by conservation bin")
ax.legend(frameon=False, loc="upper right")
ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=0))
ax.grid(axis="y", alpha=0.3, zorder=0)

# Annotate contact counts
for i, row in esm_bins.iterrows():
    ax.text(x[i], -0.06, f"n={row['n_contacts']}", ha="center", va="top",
            fontsize=8, color=GRAY, transform=ax.get_xaxis_transform())

fig3.tight_layout()
fig3.savefig(f"{OUT_DIR}/fig3_precision_by_conservation.png")
print(f"Saved {OUT_DIR}/fig3_precision_by_conservation.png")
plt.close(fig3)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Mean confidence on true contacts by conservation bin (grouped bar)
# ══════════════════════════════════════════════════════════════════════════════
fig4, (ax_esm, ax_ev) = plt.subplots(1, 2, figsize=(10, 4.5), sharey=False)

# ESM panel
ax_esm.bar(x, esm_bins["mean_score_contacts"], 0.55, color=ESM_COLOR, zorder=3)
for i, v in enumerate(esm_bins["mean_score_contacts"]):
    ax_esm.text(i, v + 0.005, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
ax_esm.set_xticks(x)
ax_esm.set_xticklabels(bin_labels, fontsize=9)
ax_esm.set_xlabel("Mean pair conservation (quintile)")
ax_esm.set_ylabel("Mean ESM2 score (true contacts)")
ax_esm.set_title("ESM2")
ax_esm.grid(axis="y", alpha=0.3, zorder=0)

# EV panel
ax_ev.bar(x, ev_bins["mean_score_contacts"], 0.55, color=EV_COLOR, zorder=3)
for i, v in enumerate(ev_bins["mean_score_contacts"]):
    ax_ev.text(i, v + 0.05, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
ax_ev.set_xticks(x)
ax_ev.set_xticklabels(bin_labels, fontsize=9)
ax_ev.set_xlabel("Mean pair conservation (quintile)")
ax_ev.set_ylabel("Mean EV score (true contacts)")
ax_ev.set_title("EVcouplings")
ax_ev.grid(axis="y", alpha=0.3, zorder=0)

fig4.suptitle("Confidence on true contacts by conservation", fontsize=14, y=1.02)
fig4.tight_layout()
fig4.savefig(f"{OUT_DIR}/fig4_confidence_by_conservation.png")
print(f"Saved {OUT_DIR}/fig4_confidence_by_conservation.png")
plt.close(fig4)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Caveat: true contacts are enriched at higher conservation
#             (confound plot)
# ══════════════════════════════════════════════════════════════════════════════
fig5, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))

# Panel A: Conservation density for contacts vs non-contacts
cons_contact = df_all.loc[df_all["gt_contact"] == 1, "pair_cons_mean"]
cons_noncontact = df_all.loc[df_all["gt_contact"] == 0, "pair_cons_mean"]
ax1.hist(cons_contact, bins=35, alpha=0.65, label=f"True contacts (n={len(cons_contact)})",
         density=True, color=ACCENT, edgecolor="white", lw=0.5, zorder=3)
ax1.hist(cons_noncontact, bins=35, alpha=0.45, label=f"Non-contacts (n={len(cons_noncontact)})",
         density=True, color=GRAY, edgecolor="white", lw=0.5, zorder=2)
ax1.axvline(cons_contact.median(), color=ACCENT, ls="--", lw=1, alpha=0.8)
ax1.axvline(cons_noncontact.median(), color=GRAY, ls="--", lw=1, alpha=0.8)
ax1.set_xlabel("Mean pair conservation")
ax1.set_ylabel("Density")
ax1.set_title("Contacts are enriched at higher conservation")
ax1.legend(frameon=False, fontsize=9)
ax1.grid(axis="y", alpha=0.2, zorder=0)

# Panel B: Contact density (fraction of pairs that are contacts) by bin
df_binned = make_bins(df_all)
density_rows = []
for label, grp in df_binned.groupby("cons_bin", observed=True):
    n_true = grp["gt_contact"].sum()
    density_rows.append({
        "bin": label, "bin_mid": label.mid,
        "contact_rate": n_true / len(grp),
        "n_contacts": int(n_true),
    })
ddf = pd.DataFrame(density_rows)

ax2.bar(np.arange(len(ddf)), ddf["contact_rate"] * 100, 0.55, color=ACCENT, zorder=3, alpha=0.8)
for i, row in ddf.iterrows():
    ax2.text(i, row["contact_rate"] * 100 + 0.02,
             f"{row['n_contacts']}", ha="center", va="bottom", fontsize=9, color=GRAY)
bin_labels_all = [f"{b.left:.2f}-{b.right:.2f}" for b in ddf["bin"]]
ax2.set_xticks(np.arange(len(ddf)))
ax2.set_xticklabels(bin_labels_all, fontsize=9)
ax2.set_xlabel("Mean pair conservation (quintile)")
ax2.set_ylabel("Contact rate (%)")
ax2.set_title("Contact density increases with conservation")
ax2.grid(axis="y", alpha=0.3, zorder=0)

fig5.suptitle("Caveat: conserved residues have more contacts (core enrichment)",
              fontsize=13, y=1.02)
fig5.tight_layout()
fig5.savefig(f"{OUT_DIR}/fig5_confound_conservation_density.png")
print(f"Saved {OUT_DIR}/fig5_confound_conservation_density.png")
plt.close(fig5)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — ESM2 vs EVcouplings scatter (true contacts), colored by conservation
# ══════════════════════════════════════════════════════════════════════════════
fig6, ax = plt.subplots(figsize=(6, 5))

sc = ax.scatter(
    contacts_ev["ev_score"], contacts_ev["pred_score"],
    c=contacts_ev["pair_cons_mean"], cmap="RdYlGn_r",
    alpha=0.55, s=18, edgecolors="none", zorder=2,
    vmin=contacts_ev["pair_cons_mean"].quantile(0.05),
    vmax=contacts_ev["pair_cons_mean"].quantile(0.95),
)
cbar = plt.colorbar(sc, ax=ax, pad=0.02)
cbar.set_label("Mean pair conservation", fontsize=10)

# Quadrant lines at medians
ev_med = contacts_ev["ev_score"].median()
esm_med = contacts_ev["pred_score"].median()
ax.axvline(ev_med, color=GRAY, ls=":", lw=0.8, alpha=0.6)
ax.axhline(esm_med, color=GRAY, ls=":", lw=0.8, alpha=0.6)

# Correlation
r, p = sp_stats.pearsonr(contacts_ev["ev_score"], contacts_ev["pred_score"])
ax.text(0.03, 0.97, f"r = {r:.3f}, p = {p:.1e}", transform=ax.transAxes,
        ha="left", va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, alpha=0.9))

ax.set_xlabel("EVcouplings score")
ax.set_ylabel("ESM2 contact score")
ax.set_title("ESM2 vs EVcouplings (true contacts only)")
ax.grid(alpha=0.15, zorder=0)

fig6.tight_layout()
fig6.savefig(f"{OUT_DIR}/fig6_esm_vs_ev_scatter.png")
print(f"Saved {OUT_DIR}/fig6_esm_vs_ev_scatter.png")
plt.close(fig6)


# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 7 — "Where do methods disagree?" — contacts that one gets right
#             and the other misses, binned by conservation
# ══════════════════════════════════════════════════════════════════════════════
# Rank all pairs, define "predicted contact" as being in top-L
k = N_PDB
esm_threshold = df_ev["pred_score"].nlargest(k).iloc[-1]
ev_threshold  = df_ev["ev_score"].nlargest(k).iloc[-1]

df_ev_c = df_ev.copy()
df_ev_c["esm_pred"] = (df_ev_c["pred_score"] >= esm_threshold).astype(int)
df_ev_c["ev_pred"]  = (df_ev_c["ev_score"] >= ev_threshold).astype(int)

true_contacts = df_ev_c[df_ev_c["gt_contact"] == 1].copy()
true_contacts["esm_hit"] = true_contacts["esm_pred"]
true_contacts["ev_hit"]  = true_contacts["ev_pred"]

both_hit  = true_contacts[(true_contacts["esm_hit"] == 1) & (true_contacts["ev_hit"] == 1)]
esm_only  = true_contacts[(true_contacts["esm_hit"] == 1) & (true_contacts["ev_hit"] == 0)]
ev_only   = true_contacts[(true_contacts["esm_hit"] == 0) & (true_contacts["ev_hit"] == 1)]
both_miss = true_contacts[(true_contacts["esm_hit"] == 0) & (true_contacts["ev_hit"] == 0)]

fig7, ax = plt.subplots(figsize=(6, 4.5))

categories = ["Both hit", "ESM2 only", "EV only", "Both miss"]
counts = [len(both_hit), len(esm_only), len(ev_only), len(both_miss)]
mean_cons = [both_hit["pair_cons_mean"].mean(), esm_only["pair_cons_mean"].mean(),
             ev_only["pair_cons_mean"].mean(), both_miss["pair_cons_mean"].mean()]
colors_cat = [ACCENT, ESM_COLOR, EV_COLOR, GRAY]

bars = ax.bar(np.arange(4), counts, 0.55, color=colors_cat, zorder=3, alpha=0.85)
for i, (bar, mc) in enumerate(zip(bars, mean_cons)):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
            f"n={counts[i]}\ncons={mc:.3f}", ha="center", va="bottom", fontsize=9)

ax.set_xticks(np.arange(4))
ax.set_xticklabels(categories, fontsize=10)
ax.set_ylabel("Number of true contacts")
ax.set_title("Agreement between methods (top-L predictions)")
ax.grid(axis="y", alpha=0.3, zorder=0)

fig7.tight_layout()
fig7.savefig(f"{OUT_DIR}/fig7_method_agreement.png")
print(f"Saved {OUT_DIR}/fig7_method_agreement.png")
plt.close(fig7)

print("\nAll figures saved.")
