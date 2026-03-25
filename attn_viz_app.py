"""
Attention Pattern Visualization for Contact Circuits.

Interactive exploration of attention patterns for circuit heads
identified by contact_pattern_v2.py.

Run:  uv run streamlit run attn_viz_app.py
"""

import json
from pathlib import Path

import matplotlib.colors as mcolors
from matplotlib.colors import LogNorm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import torch

st.set_page_config(layout="wide", page_title="Contact Circuit Attention")

# ── Paths ────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent
CACHE_DIR = ROOT / "reports" / "cache"
PROTEINS_CFG = ROOT / "configs" / "proteins.json"
COMMON_CFG = ROOT / "configs" / "common.json"
DATA_PATH = ROOT / "data" / "full_seq_dict.json"

# ── Configs ──────────────────────────────────────────────────────────────────


@st.cache_data
def load_configs():
    with open(PROTEINS_CFG) as f:
        proteins = json.load(f)
    with open(COMMON_CFG) as f:
        common = json.load(f)
    with open(DATA_PATH) as f:
        seq_dict = json.load(f)
    return proteins, common, seq_dict


PROTEINS, COMMON, SEQ_DICT = load_configs()
SEGMENT_RADIUS = COMMON["segment_radius"]
FAITH_TARGET = COMMON["faith_target"]
NUM_LAYERS = 33
NUM_HEADS = 20

AVAILABLE = sorted(
    p for p in PROTEINS if (CACHE_DIR / p / "attn_cache.pt").exists()
)

# ── Data loading ─────────────────────────────────────────────────────────────


@st.cache_resource(max_entries=2)
def load_protein_data(protein):
    cache = CACHE_DIR / protein

    ad = torch.load(cache / "attn_cache.pt", map_location="cpu", weights_only=False)
    bd = torch.load(cache / "baselines.pt", map_location="cpu", weights_only=False)
    cd = torch.load(cache / "circuit_results.pt", map_location="cpu", weights_only=False)
    ied = torch.load(cache / "indirect_effects.pt", map_location="cpu", weights_only=False)

    cell_data = None
    cell_pt = cache / "cell_attr.pt"
    if cell_pt.exists():
        cell_data = torch.load(cell_pt, map_location="cpu", weights_only=False)

    full_attn = None
    full_pt = cache / "full_seq_attn_cache.pt"
    if full_pt.exists():
        try:
            full_attn = torch.load(full_pt, map_location="cpu", weights_only=False)
        except Exception:
            pass

    cm = bd["clean_metric"]
    xm = bd["corrupt_metric"]

    return {
        "clean_attn": list(ad["clean_attn_LBHLL"]),
        "corrupt_attn": list(ad["corrupt_attn_LBHLL"]),
        "orig_contacts": bd["orig_contacts_AA"],
        "clean_contacts": bd["clean_contacts_AA"],
        "corrupt_contacts": bd["corrupt_contacts_AA"],
        "clean_metric": cm.item() if hasattr(cm, "item") else float(cm),
        "corrupt_metric": xm.item() if hasattr(xm, "item") else float(xm),
        "circuit": cd["circuit_results"],
        "ie": ied["indirect_effects_LH"],
        "cell_data": cell_data,
        "full_attn": full_attn,
    }


# ── Helpers ──────────────────────────────────────────────────────────────────


def get_circuit_heads(data):
    ie = data["ie"]
    flat = ie.flatten()
    sorted_idx = flat.argsort(descending=True)
    all_heads = [
        (idx.item() // NUM_HEADS, idx.item() % NUM_HEADS) for idx in sorted_idx
    ]
    cr = data["circuit"]["pos"]
    crossed_k = None
    for k_val, f_val in zip(cr["k"], cr["faith"]):
        if f_val >= FAITH_TARGET:
            crossed_k = k_val
            break
    if crossed_k is None:
        crossed_k = COMMON["topk_heads"]
    return all_heads[:crossed_k], crossed_k


def get_segment(cfg):
    cp = cfg["contact_pair"]
    r = SEGMENT_RADIUS
    return {
        "ss1_start": cp[0] - r,
        "ss1_end": cp[0] + r + 1,
        "ss2_start": cp[1] - r,
        "ss2_end": cp[1] + r + 1,
        "contact_pair": cp,
        "clean_flank": cfg["clean_flank"],
        "corrupt_flank": cfg["corrupt_flank"],
    }


def get_regions(seg, seq_len):
    ss1_s, ss1_e = seg["ss1_start"], seg["ss1_end"]
    ss2_s, ss2_e = seg["ss2_start"], seg["ss2_end"]
    flank = seg["clean_flank"]
    flkL_s = max(0, ss1_s - flank)
    flkL_e = ss1_s
    flkR_s = ss2_e
    flkR_e = min(seq_len, ss2_e + flank)
    # "flank" regions include the adjacent SS segment
    leftL_s, leftL_e = flkL_s, ss1_e   # [flankL, ss1]
    rightR_s, rightR_e = ss2_s, flkR_e  # [ss2, flankR]
    return {
        "Full sequence": ((0, seq_len), (0, seq_len)),
        "ss1 × ss2": ((ss1_s, ss1_e), (ss2_s, ss2_e)),
        "ss2 × ss1": ((ss2_s, ss2_e), (ss1_s, ss1_e)),
        "flankL × flankR": ((leftL_s, leftL_e), (rightR_s, rightR_e)),
        "flankR × flankL": ((rightR_s, rightR_e), (leftL_s, leftL_e)),
        "flankL × flankL": ((leftL_s, leftL_e), (leftL_s, leftL_e)),
        "flankR × flankR": ((rightR_s, rightR_e), (rightR_s, rightR_e)),
    }


def classify_pos(pos, seg):
    if seg["ss1_start"] <= pos < seg["ss1_end"]:
        return "ss1"
    if seg["ss2_start"] <= pos < seg["ss2_end"]:
        return "ss2"
    flkL_s = max(0, seg["ss1_start"] - seg["clean_flank"])
    if flkL_s <= pos < seg["ss1_start"]:
        return "flkL"
    if seg["ss2_end"] <= pos < seg["ss2_end"] + seg["clean_flank"]:
        return "flkR"
    return "other"


def make_seq_labels(seq, start, end):
    end = min(end, len(seq))
    return [f"{seq[i]}{i}" for i in range(start, end)]


def make_single_heatmap(matrix, title, row_labels, col_labels, cmap="inferno", vmin=None, vmax=None, diverging=False, log_scale=False, figsize=(8, 7), causal_cells=None):
    """Create a standalone figure for one heatmap. Returns the figure.

    causal_cells: optional set of (row_idx, col_idx) tuples (0-based into the matrix) to highlight with a border.
    """
    fig, ax = plt.subplots(figsize=figsize)

    if diverging:
        abs_max = max(abs(np.nanmin(matrix)), abs(np.nanmax(matrix)), 1e-10)
        norm = mcolors.TwoSlopeNorm(vmin=-abs_max, vcenter=0, vmax=abs_max)
        im = ax.imshow(matrix, aspect="equal", cmap=cmap, norm=norm, interpolation="nearest")
    elif log_scale:
        pos_vals = matrix[matrix > 0]
        lv = max(pos_vals.min(), 1e-6) if len(pos_vals) > 0 else 1e-6
        hv = matrix.max()
        if hv <= lv:
            hv = lv * 10
        im = ax.imshow(matrix, aspect="equal", cmap=cmap, norm=LogNorm(vmin=lv, vmax=hv), interpolation="nearest")
    else:
        im = ax.imshow(matrix, aspect="equal", cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=10)
    n_rows, n_cols = matrix.shape

    if n_cols <= 40:
        ax.set_xticks(range(n_cols))
        ax.set_xticklabels(col_labels[:n_cols], rotation=90, fontsize=7)
    else:
        step = max(1, n_cols // 20)
        ticks = list(range(0, n_cols, step))
        ax.set_xticks(ticks)
        ax.set_xticklabels([col_labels[i] if i < len(col_labels) else "" for i in ticks], rotation=90, fontsize=7)

    if n_rows <= 40:
        ax.set_yticks(range(n_rows))
        ax.set_yticklabels(row_labels[:n_rows], fontsize=7)
    else:
        step = max(1, n_rows // 20)
        ticks = list(range(0, n_rows, step))
        ax.set_yticks(ticks)
        ax.set_yticklabels([row_labels[i] if i < len(row_labels) else "" for i in ticks], fontsize=7)

    if causal_cells:
        for (r, c) in causal_cells:
            if 0 <= r < matrix.shape[0] and 0 <= c < matrix.shape[1]:
                rect = mpatches.Rectangle((c - 0.5, r - 0.5), 1, 1, linewidth=1.2, edgecolor="cyan", facecolor="none")
                ax.add_patch(rect)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(labelsize=9)
    ax.set_xlabel("Key (k)", fontsize=11)
    ax.set_ylabel("Query (q)", fontsize=11)
    ax.tick_params(labelsize=8)
    fig.tight_layout()
    return fig


# ── Sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.title("Circuit Attention Explorer")

protein = st.sidebar.selectbox(
    "Protein", AVAILABLE,
    index=AVAILABLE.index("2B61A") if "2B61A" in AVAILABLE else 0,
)

with st.spinner(f"Loading {protein}..."):
    data = load_protein_data(protein)

cfg = PROTEINS[protein]
seq = SEQ_DICT[protein]
seg = get_segment(cfg)
regions = get_regions(seg, len(seq))
circuit_heads, crossed_k = get_circuit_heads(data)
ie = data["ie"]

head_labels = [
    f"#{i+1}: L{l} H{h} (IE={ie[l, h].item():+.4f})"
    for i, (l, h) in enumerate(circuit_heads)
]

selected_idx = st.sidebar.selectbox(
    "Circuit Head", range(len(head_labels)),
    format_func=lambda i: head_labels[i],
)

region_name = st.sidebar.selectbox(
    "Region (query × key)", list(regions.keys()), index=1,
)

has_full = data["full_attn"] is not None
show_full = has_full and st.sidebar.checkbox("Include full-sequence attention", value=False)
show_causal = data["cell_data"] is not None and st.sidebar.checkbox("Highlight causal cells", value=True)

st.sidebar.markdown("---")
flkL_s = max(0, seg["ss1_start"] - seg["clean_flank"])
flkR_e = seg["ss2_end"] + seg["clean_flank"]
st.sidebar.markdown(
    f"**Segment info**\n\n"
    f"- Contact pair: {tuple(cfg['contact_pair'])}\n"
    f"- ss1: [{seg['ss1_start']}, {seg['ss1_end']})\n"
    f"- ss2: [{seg['ss2_start']}, {seg['ss2_end']})\n"
    f"- flankL: [{flkL_s}, {seg['ss1_start']})\n"
    f"- flankR: [{seg['ss2_end']}, {flkR_e})\n"
    f"- flankL+ss1: [{flkL_s}, {seg['ss1_end']})\n"
    f"- ss2+flankR: [{seg['ss2_start']}, {flkR_e})\n"
    f"- Clean flank: {seg['clean_flank']}\n"
    f"- Corrupt flank: {seg['corrupt_flank']}\n"
    f"- Seq length: {len(seq)}\n"
    f"- Circuit size: {crossed_k} heads"
)

# ── Header ───────────────────────────────────────────────────────────────────

l, h = circuit_heads[selected_idx]

st.header(f"{protein} — L{l} H{h} (IE rank #{selected_idx + 1})")

mc, mx = data["clean_metric"], data["corrupt_metric"]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Clean Metric", f"{mc:.4f}")
c2.metric("Corrupt Metric", f"{mx:.4f}")
c3.metric("Gap", f"{mc - mx:.4f}")
c4.metric("IE Score", f"{ie[l, h].item():+.4f}")

# ── Region extraction ────────────────────────────────────────────────────────

(row_s, row_e), (col_s, col_e) = regions[region_name]
row_labels = make_seq_labels(seq, row_s, row_e)
col_labels = make_seq_labels(seq, col_s, col_e)

# Attention: token space = seq_pos + 1 (BOS at index 0)
clean_attn_head = data["clean_attn"][l][0, h].numpy()
corrupt_attn_head = data["corrupt_attn"][l][0, h].numpy()

clean_region = clean_attn_head[row_s + 1 : row_e + 1, col_s + 1 : col_e + 1]
corrupt_region = corrupt_attn_head[row_s + 1 : row_e + 1, col_s + 1 : col_e + 1]
diff_region = clean_region - corrupt_region

# ── Causal cell set for this head and region ─────────────────────────────────

causal_cells_region = None
if show_causal and data["cell_data"] is not None:
    cell_sorted = data["cell_data"]["cell_attr_sorted"]
    topk = COMMON.get("topk_cell", 2000)
    causal_cells_region = set()
    for i, (ll, hh, q, k, attr, adiff) in enumerate(cell_sorted):
        if i >= topk:
            break
        if ll == l and hh == h:
            # q, k are in token space (BOS offset); convert to sequence position
            qp, kp = q - 1, k - 1
            # Convert to matrix-local indices for the current region
            r_idx = qp - row_s
            c_idx = kp - col_s
            if 0 <= r_idx < (row_e - row_s) and 0 <= c_idx < (col_e - col_s):
                causal_cells_region.add((r_idx, c_idx))
    if not causal_cells_region:
        causal_cells_region = None

# ── Attention heatmaps (each as separate figure for zoom) ────────────────────

st.subheader(f"Attention — {region_name}")

col_clean, col_corrupt = st.columns(2)
with col_clean:
    fig = make_single_heatmap(clean_region, "Clean Attention", row_labels, col_labels, log_scale=True, causal_cells=causal_cells_region)
    st.pyplot(fig)
    plt.close(fig)
with col_corrupt:
    fig = make_single_heatmap(corrupt_region, "Corrupt Attention", row_labels, col_labels, log_scale=True, causal_cells=causal_cells_region)
    st.pyplot(fig)
    plt.close(fig)

col_diff, col_full = st.columns(2)
with col_diff:
    fig = make_single_heatmap(diff_region, "Diff (Clean − Corrupt)", row_labels, col_labels, cmap="RdBu_r", diverging=True, causal_cells=causal_cells_region)
    st.pyplot(fig)
    plt.close(fig)
with col_full:
    if show_full:
        fd = data["full_attn"]
        full_key = next((k for k in ["attn_LBHLL", "full_attn_LBHLL", "clean_attn_LBHLL"] if k in fd), None)
        if full_key is not None:
            full_list = fd[full_key]
            if isinstance(full_list, (list, tuple)):
                full_head = full_list[l][0, h].numpy()
            else:
                full_head = full_list[l][0, h].numpy()
            full_region = full_head[row_s + 1 : row_e + 1, col_s + 1 : col_e + 1]
            fig = make_single_heatmap(full_region, "Full-Seq Attention", row_labels, col_labels, log_scale=True, causal_cells=causal_cells_region)
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Unknown full-sequence cache format.")
    else:
        st.caption("Enable 'Include full-sequence attention' in sidebar to see the fourth panel.")

# ── Contact maps ─────────────────────────────────────────────────────────────

orig_c = data["orig_contacts"].numpy()[row_s:row_e, col_s:col_e]
clean_c = data["clean_contacts"].numpy()[row_s:row_e, col_s:col_e]
corrupt_c = data["corrupt_contacts"].numpy()[row_s:row_e, col_s:col_e]

ct_col1, ct_col2, ct_col3 = st.columns(3)
with ct_col1:
    fig = make_single_heatmap(orig_c, "Original Contacts", row_labels, col_labels, cmap="Greens", vmin=0, vmax=1, figsize=(6, 5), causal_cells=causal_cells_region)
    st.pyplot(fig)
    plt.close(fig)
with ct_col2:
    fig = make_single_heatmap(clean_c, "Clean Contacts", row_labels, col_labels, cmap="Greens", vmin=0, vmax=1, figsize=(6, 5), causal_cells=causal_cells_region)
    st.pyplot(fig)
    plt.close(fig)
with ct_col3:
    fig = make_single_heatmap(corrupt_c, "Corrupt Contacts", row_labels, col_labels, cmap="Greens", vmin=0, vmax=1, figsize=(6, 5), causal_cells=causal_cells_region)
    st.pyplot(fig)
    plt.close(fig)

# ── Cell attribution table ───────────────────────────────────────────────────

if data["cell_data"] is not None:
    cell_sorted = data["cell_data"]["cell_attr_sorted"]
    topk = COMMON.get("topk_cell", 2000)
    top_cells_set = set()
    for i, (ll, hh, q, k, attr, adiff) in enumerate(cell_sorted):
        if i >= topk:
            break
        top_cells_set.add((ll, hh, q, k))

    head_cells = [
        (q, k, attr, adiff)
        for (ll, hh, q, k, attr, adiff) in cell_sorted
        if ll == l and hh == h
    ]
    head_in_top = sum(1 for (q, k, attr, adiff) in head_cells if (l, h, q, k) in top_cells_set)

    if head_cells:
        st.subheader(f"Cell Attributions — L{l} H{h} ({head_in_top} of top-{topk} circuit cells)")

        rows = []
        for q, k, attr, adiff in head_cells[:100]:
            qp, kp = q - 1, k - 1
            rows.append({
                "q_pos": qp,
                "q_aa": seq[qp] if 0 <= qp < len(seq) else "?",
                "q_region": classify_pos(qp, seg),
                "k_pos": kp,
                "k_aa": seq[kp] if 0 <= kp < len(seq) else "?",
                "k_region": classify_pos(kp, seg),
                "attr": round(attr, 6),
                "|diff|": round(adiff, 6),
                "offset(q-k)": qp - kp,
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=False, hide_index=True, height=400)
    else:
        st.info(f"No cells for L{l} H{h} in top-{topk} attributed cells.")
else:
    st.warning("No cell attribution data for this protein.")

# ── Compare top heads (diff patterns) ────────────────────────────────────────

with st.expander("Compare top circuit heads (diff patterns for selected region)"):
    n_show = min(16, len(circuit_heads))
    n_grid_cols = 4
    n_grid_rows = (n_show + n_grid_cols - 1) // n_grid_cols

    fig_grid, axes_grid = plt.subplots(
        n_grid_rows, n_grid_cols,
        figsize=(4 * n_grid_cols, 3.5 * n_grid_rows),
        squeeze=False,
    )

    for i in range(n_show):
        li, hi = circuit_heads[i]
        c_i = data["clean_attn"][li][0, hi].numpy()
        x_i = data["corrupt_attn"][li][0, hi].numpy()
        d_i = c_i - x_i
        d_sub = d_i[row_s + 1 : row_e + 1, col_s + 1 : col_e + 1]

        ax = axes_grid[i // n_grid_cols][i % n_grid_cols]
        abs_max = max(abs(d_sub.min()), abs(d_sub.max()), 1e-10)
        ax.imshow(
            d_sub, aspect="equal", cmap="RdBu_r",
            norm=mcolors.TwoSlopeNorm(vmin=-abs_max, vcenter=0, vmax=abs_max),
            interpolation="nearest",
        )
        ie_i = ie[li, hi].item()
        ax.set_title(f"#{i+1} L{li}H{hi} ({ie_i:+.3f})", fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])

    for i in range(n_show, n_grid_rows * n_grid_cols):
        axes_grid[i // n_grid_cols][i % n_grid_cols].set_visible(False)

    fig_grid.suptitle(f"Diff Patterns (Clean − Corrupt) — {region_name}", fontsize=12)
    fig_grid.tight_layout()
    st.pyplot(fig_grid)
    plt.close(fig_grid)

# ── IE heatmap ───────────────────────────────────────────────────────────────

with st.expander("Indirect Effect Heatmap (all 660 heads)"):
    ie_np = ie.numpy()
    fig_ie, ax_ie = plt.subplots(figsize=(14, 6))
    abs_max = max(abs(ie_np.min()), abs(ie_np.max()), 1e-10)
    im = ax_ie.imshow(
        ie_np.T, aspect="auto", cmap="RdBu_r",
        norm=mcolors.TwoSlopeNorm(vmin=-abs_max, vcenter=0, vmax=abs_max),
        interpolation="nearest",
    )
    ax_ie.set_xlabel("Layer")
    ax_ie.set_ylabel("Head")
    ax_ie.set_title("Indirect Effects (red = positive/helpful, blue = negative)")
    plt.colorbar(im, ax=ax_ie)

    for ci, (cl, ch) in enumerate(circuit_heads):
        marker = "w*" if ci < 5 else "k."
        ax_ie.plot(cl, ch, marker, markersize=6 if ci < 5 else 3)

    fig_ie.tight_layout()
    st.pyplot(fig_ie)
    plt.close(fig_ie)
