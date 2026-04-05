#!/usr/bin/env python3
"""Anchor local flank v2: flank pattern discovery and window-based classification.

Tests whether anchorhood is encoded in a local window motif around the residue
rather than only in properties of the center residue itself.

Part A: Flank pattern discovery (AA-class and SSE logos for anchor vs control windows)
Part B: Window-level anchor classification with leave-one-protein-out evaluation,
        testing multiple radii and center-censor variants.

Usage:
    uv run python scripts/anchor_local_flank_v2.py --device cuda
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

AUDIT_CSV = REPORT_DIR / "anchor_behavior_audit.csv"
V3_FEATURES_CSV = REPORT_DIR / "anchor_regression_v3_features.csv"
V3_MATCHES_CSV = REPORT_DIR / "anchor_regression_v3_matches.csv"

TOP_N_VIZ = 50
TOP_N_CLASS = 500
RADII = [5, 10, 15, 20, 25, 30, 40]
CONTROLS_PER_ANCHOR = 5
MAX_POSITIONAL_FEATURES_RADIUS = 999  # use per-position features at all radii
MIN_EDGE_DISTANCE = 5  # anchor must be at least this far from sequence edges
CONTROLS_PER_ANCHOR_V3 = 5  # how many of the 10 v3 controls to use per anchor

AA_ORDER = list("ACDEFGHIKLMNPQRSTVWY")

AA_CLASS = {}
for aa in "AILMV":
    AA_CLASS[aa] = "hydrophobic"
for aa in "FWY":
    AA_CLASS[aa] = "aromatic"
for aa in "STNQ":
    AA_CLASS[aa] = "polar"
for aa in "RKH":
    AA_CLASS[aa] = "positive"
for aa in "DE":
    AA_CLASS[aa] = "negative"
AA_CLASS["G"] = "glycine"
AA_CLASS["P"] = "proline"
AA_CLASS["C"] = "polar"  # cysteine grouped with polar

AA_CLASS_ORDER = ["hydrophobic", "aromatic", "polar", "positive", "negative", "glycine", "proline"]
AA_CLASS_COLORS = {
    "hydrophobic": "#4575b4",
    "aromatic": "#fee090",
    "polar": "#91bfdb",
    "positive": "#d73027",
    "negative": "#fc8d59",
    "glycine": "#999999",
    "proline": "#542788",
}

SSE_ORDER = ["H", "E", "C"]
SSE_COLORS = {"H": "#e06c75", "E": "#61afef", "C": "#98c379"}

KD = {"A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5,
      "Q": -3.5, "E": -3.5, "G": -0.4, "H": -3.2, "I": 4.5,
      "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6,
      "S": -0.8, "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data():
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        protein = k.replace(".pdb", "")
        ss_dict[protein] = v.replace("-", "C")
    return seqs, ss_dict


def select_proteins(seqs, ss_dict, n):
    """Select top N proteins by top3_mass from the audit, requiring seq + SSE with matching lengths."""
    rows = []
    with open(AUDIT_CSV) as f:
        for r in csv.DictReader(f):
            pid = r["protein"]
            if pid not in seqs or pid not in ss_dict:
                continue
            if len(seqs[pid]) != len(ss_dict[pid]):
                continue
            anchor_pos = int(r["top_key_idx"])
            n_res = len(seqs[pid])
            if anchor_pos < MIN_EDGE_DISTANCE or anchor_pos >= n_res - MIN_EDGE_DISTANCE:
                continue
            rows.append({
                "protein": pid,
                "top3_mass": float(r["top3_mass"]),
                "anchor_pos": anchor_pos,
                "n_res": n_res,
            })
    rows.sort(key=lambda x: x["top3_mass"], reverse=True)
    return rows[:n]


# ---------------------------------------------------------------------------
# Matched control selection (SSE-only matching for broad coverage)
# ---------------------------------------------------------------------------

def build_matched_controls_sse(proteins, seqs, ss_dict, controls_per_anchor=CONTROLS_PER_ANCHOR):
    """For each anchor, find matched non-anchor controls from the same protein.

    Matching: same SSE type, at least 10 residues away from anchor,
    not in the top 5% of the protein by some proxy (we use distance from anchor as tiebreaker).
    """
    all_matches = []
    rng = np.random.RandomState(42)

    for pinfo in proteins:
        pid = pinfo["protein"]
        anchor = pinfo["anchor_pos"]
        seq = seqs[pid]
        sse = ss_dict[pid]
        n = len(seq)
        anchor_sse = sse[anchor]

        # Candidates: same SSE, at least 10 residues away, not at edges
        candidates = []
        for j in range(MIN_EDGE_DISTANCE, n - MIN_EDGE_DISTANCE):
            if abs(j - anchor) < 10:
                continue
            if sse[j] != anchor_sse:
                continue
            candidates.append(j)

        if len(candidates) == 0:
            continue

        if len(candidates) <= controls_per_anchor:
            selected = candidates
        else:
            idx = rng.choice(len(candidates), controls_per_anchor, replace=False)
            selected = [candidates[i] for i in idx]

        for ctrl_pos in selected:
            all_matches.append({
                "protein": pid,
                "anchor_pos": anchor,
                "control_pos": ctrl_pos,
                "anchor_sse": anchor_sse,
            })

    return all_matches


def load_v3_matched_controls(seqs, ss_dict, max_controls=CONTROLS_PER_ANCHOR_V3):
    """Load structurally-matched controls from v3 (matched on SSE + RSA + contacts_8A).

    Returns (proteins_list, matches_list) in the same format as the SSE-only pipeline.
    """
    matches_raw = []
    with open(V3_MATCHES_CSV) as f:
        for r in csv.DictReader(f):
            matches_raw.append(r)

    # Group by (protein, anchor_pos)
    grouped = defaultdict(list)
    for r in matches_raw:
        grouped[(r["protein"], int(r["anchor_pos"]))].append(int(r["control_pos"]))

    proteins_list = []
    matches_list = []
    seen_proteins = set()
    rng = np.random.RandomState(42)

    for (pid, anchor_pos), ctrl_positions in grouped.items():
        if pid not in seqs or pid not in ss_dict:
            continue
        seq = seqs[pid]
        sse = ss_dict[pid]
        if len(seq) != len(sse):
            continue
        if anchor_pos < MIN_EDGE_DISTANCE or anchor_pos >= len(seq) - MIN_EDGE_DISTANCE:
            continue

        if pid not in seen_proteins:
            seen_proteins.add(pid)
            proteins_list.append({"protein": pid, "anchor_pos": anchor_pos, "n_res": len(seq)})

        # Subsample controls if needed
        if len(ctrl_positions) > max_controls:
            ctrl_positions = [ctrl_positions[i] for i in rng.choice(len(ctrl_positions), max_controls, replace=False)]

        anchor_sse = sse[anchor_pos] if anchor_pos < len(sse) else "C"
        for cp in ctrl_positions:
            if cp < MIN_EDGE_DISTANCE or cp >= len(seq) - MIN_EDGE_DISTANCE:
                continue
            matches_list.append({
                "protein": pid,
                "anchor_pos": anchor_pos,
                "control_pos": cp,
                "anchor_sse": anchor_sse,
            })

    return proteins_list, matches_list


# ---------------------------------------------------------------------------
# Window extraction
# ---------------------------------------------------------------------------

def extract_window(seq, sse, center, radius):
    """Extract a symmetric window [center-R, ..., center+R] from seq and sse.

    Returns (window_seq, window_sse) as strings, or None if window extends beyond edges.
    """
    n = len(seq)
    lo = center - radius
    hi = center + radius
    if lo < 0 or hi >= n:
        return None, None
    return seq[lo:hi + 1], sse[lo:hi + 1]


# ---------------------------------------------------------------------------
# Part A: Logo computation
# ---------------------------------------------------------------------------

def compute_positional_frequencies(windows, alphabet, order):
    """Compute per-position frequency matrix from a list of window strings.

    Returns array of shape (n_categories, window_len) with frequencies.
    """
    if not windows:
        return None
    wlen = len(windows[0])
    cat_to_idx = {c: i for i, c in enumerate(order)}
    counts = np.zeros((len(order), wlen))
    for w in windows:
        for j, ch in enumerate(w):
            idx = cat_to_idx.get(ch, -1)
            if idx >= 0:
                counts[idx, j] += 1
    totals = counts.sum(axis=0, keepdims=True)
    totals[totals == 0] = 1
    return counts / totals


def compute_aa_class_windows(windows_seq):
    """Convert AA windows to AA-class windows."""
    result = []
    for w in windows_seq:
        cls_w = "".join(AA_CLASS.get(aa, "polar")[0].upper() for aa in w)
        result.append(cls_w)
    return result


def compute_class_freq_matrix(windows_seq, order=AA_CLASS_ORDER):
    """Compute per-position AA-class frequency matrix."""
    if not windows_seq:
        return None
    wlen = len(windows_seq[0])
    cat_to_idx = {c: i for i, c in enumerate(order)}
    counts = np.zeros((len(order), wlen))
    for w in windows_seq:
        for j, aa in enumerate(w):
            cls = AA_CLASS.get(aa, "polar")
            idx = cat_to_idx.get(cls, -1)
            if idx >= 0:
                counts[idx, j] += 1
    totals = counts.sum(axis=0, keepdims=True)
    totals[totals == 0] = 1
    return counts / totals


def compute_sse_freq_matrix(windows_sse, order=SSE_ORDER):
    """Compute per-position SSE frequency matrix."""
    return compute_positional_frequencies(windows_sse, SSE_ORDER, order)


# ---------------------------------------------------------------------------
# Part A: Logo plotting
# ---------------------------------------------------------------------------

def plot_stacked_logo(freq_matrix, order, colors, positions, title, ax):
    """Plot a stacked bar logo on the given axes."""
    n_cats, wlen = freq_matrix.shape
    x = np.arange(wlen)
    bottom = np.zeros(wlen)
    for i, cat in enumerate(order):
        ax.bar(x, freq_matrix[i], bottom=bottom, color=colors[cat], label=cat, width=0.9, edgecolor="none")
        bottom += freq_matrix[i]
    ax.set_xticks(x[::5])
    ax.set_xticklabels([str(p) for p in positions[::5]], fontsize=7)
    ax.set_ylim(0, 1.05)
    ax.set_title(title, fontsize=9)
    ax.set_ylabel("Frequency", fontsize=8)


def plot_enrichment_heatmap(anchor_freq, control_freq, order, positions, title, ax):
    """Plot anchor-minus-control enrichment heatmap."""
    diff = anchor_freq - control_freq
    vmax = max(abs(diff.min()), abs(diff.max()), 0.1)
    im = ax.imshow(diff, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax,
                   interpolation="nearest")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=7)
    tick_positions = list(range(0, len(positions), 5))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([str(positions[i]) for i in tick_positions], fontsize=7)
    ax.set_title(title, fontsize=9)
    plt.colorbar(im, ax=ax, shrink=0.6, label="Anchor - Control")


def generate_logos(anchor_windows_seq, control_windows_seq,
                   anchor_windows_sse, control_windows_sse,
                   radius, output_path):
    """Generate the full logo figure for a given radius."""
    wlen = 2 * radius + 1
    positions = list(range(-radius, radius + 1))

    anchor_class_freq = compute_class_freq_matrix(anchor_windows_seq)
    control_class_freq = compute_class_freq_matrix(control_windows_seq)
    anchor_sse_freq = compute_sse_freq_matrix(anchor_windows_sse)
    control_sse_freq = compute_sse_freq_matrix(control_windows_sse)

    if anchor_class_freq is None or control_class_freq is None:
        return

    fig, axes = plt.subplots(3, 2, figsize=(14, 10))

    plot_stacked_logo(anchor_class_freq, AA_CLASS_ORDER, AA_CLASS_COLORS, positions,
                      f"Anchor AA-class (R={radius})", axes[0, 0])
    plot_stacked_logo(control_class_freq, AA_CLASS_ORDER, AA_CLASS_COLORS, positions,
                      f"Control AA-class (R={radius})", axes[0, 1])

    if anchor_sse_freq is not None and control_sse_freq is not None:
        plot_stacked_logo(anchor_sse_freq, SSE_ORDER, SSE_COLORS, positions,
                          f"Anchor SSE (R={radius})", axes[1, 0])
        plot_stacked_logo(control_sse_freq, SSE_ORDER, SSE_COLORS, positions,
                          f"Control SSE (R={radius})", axes[1, 1])

        plot_enrichment_heatmap(anchor_class_freq, control_class_freq, AA_CLASS_ORDER, positions,
                                f"AA-class enrichment (R={radius})", axes[2, 0])
        plot_enrichment_heatmap(anchor_sse_freq, control_sse_freq, SSE_ORDER, positions,
                                f"SSE enrichment (R={radius})", axes[2, 1])

    # Add legend to first plot
    axes[0, 0].legend(loc="upper left", fontsize=6, ncol=2)
    axes[1, 0].legend(loc="upper left", fontsize=6)

    fig.suptitle(f"Anchor vs Control Local Window Logos (R={radius})", fontsize=12, y=1.01)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved logo: {output_path}")


# ---------------------------------------------------------------------------
# Part B: Feature extraction for classification
# ---------------------------------------------------------------------------

def extract_window_features_seq(seq_window, sse_window, include_center=True, include_center_identity=True, use_positional=True):
    """Extract sequence and SSE features from a window for classification.

    Args:
        seq_window: AA string of length 2R+1
        sse_window: SSE string of length 2R+1
        include_center: if False, zero out ALL center-position features
        include_center_identity: if False, zero out only center AA identity/class (keep SSE/structural)
        use_positional: if True, include per-position features; if False, summary only
    """
    wlen = len(seq_window)
    center_idx = wlen // 2
    features = {}

    # Determine which positions to include for counting
    def _include(j):
        if j == center_idx and not include_center:
            return False
        if j == center_idx and not include_center_identity:
            return False
        return True

    # --- Per-position features (only for small windows) ---
    if use_positional:
        for j in range(wlen):
            pos_label = j - center_idx
            if not _include(j):
                for cls in AA_CLASS_ORDER:
                    features[f"aaclass_{pos_label}_{cls}"] = 0.0
                for s in SSE_ORDER:
                    features[f"sse_{pos_label}_{s}"] = 0.0
            else:
                aa = seq_window[j]
                cls = AA_CLASS.get(aa, "polar")
                for c in AA_CLASS_ORDER:
                    features[f"aaclass_{pos_label}_{c}"] = 1.0 if c == cls else 0.0
                s = sse_window[j]
                for ss in SSE_ORDER:
                    features[f"sse_{pos_label}_{ss}"] = 1.0 if ss == s else 0.0

    # --- Summary features (always included) ---

    # AA-class counts (left flank, right flank, total)
    left_cls = Counter()
    right_cls = Counter()
    for j in range(wlen):
        if not _include(j):
            continue
        cls = AA_CLASS.get(seq_window[j], "polar")
        if j < center_idx:
            left_cls[cls] += 1
        elif j > center_idx:
            right_cls[cls] += 1
    for cls in AA_CLASS_ORDER:
        features[f"count_{cls}"] = float(left_cls[cls] + right_cls[cls])
        features[f"count_left_{cls}"] = float(left_cls[cls])
        features[f"count_right_{cls}"] = float(right_cls[cls])

    # Hydrophobicity: mean, left mean, right mean, center value
    left_hydro = [KD.get(seq_window[j], 0.0) for j in range(center_idx) if _include(j)]
    right_hydro = [KD.get(seq_window[j], 0.0) for j in range(center_idx + 1, wlen) if _include(j)]
    features["mean_hydro"] = float(np.mean(left_hydro + right_hydro)) if (left_hydro or right_hydro) else 0.0
    features["left_hydro"] = float(np.mean(left_hydro)) if left_hydro else 0.0
    features["right_hydro"] = float(np.mean(right_hydro)) if right_hydro else 0.0
    if include_center and include_center_identity:
        features["center_hydro"] = KD.get(seq_window[center_idx], 0.0)
    else:
        features["center_hydro"] = 0.0

    # Glycine / proline / aromatic counts
    features["count_gly"] = sum(1 for j in range(wlen) if seq_window[j] == "G" and _include(j))
    features["count_pro"] = sum(1 for j in range(wlen) if seq_window[j] == "P" and _include(j))
    features["count_aromatic"] = sum(1 for j in range(wlen) if seq_window[j] in "FWY" and _include(j))

    # SSE counts
    sse_counts = Counter()
    for j in range(wlen):
        if j == center_idx and not include_center:
            continue
        sse_counts[sse_window[j]] += 1
    for s in SSE_ORDER:
        features[f"sse_count_{s}"] = float(sse_counts.get(s, 0))

    # SSE transitions
    n_trans = 0
    prev_valid = None
    for j in range(wlen):
        if j == center_idx and not include_center:
            prev_valid = None
            continue
        if prev_valid is not None and sse_window[j] != prev_valid:
            n_trans += 1
        prev_valid = sse_window[j]
    features["sse_transitions"] = float(n_trans)

    # Center SSE segment length
    if include_center:
        center_sse = sse_window[center_idx]
        seg_len = 1
        for j in range(center_idx - 1, -1, -1):
            if sse_window[j] == center_sse:
                seg_len += 1
            else:
                break
        for j in range(center_idx + 1, wlen):
            if sse_window[j] == center_sse:
                seg_len += 1
            else:
                break
        features["center_sse_seg_len"] = float(seg_len)
        features[f"center_sse_H"] = 1.0 if center_sse == "H" else 0.0
        features[f"center_sse_E"] = 1.0 if center_sse == "E" else 0.0
    else:
        features["center_sse_seg_len"] = 0.0
        features["center_sse_H"] = 0.0
        features["center_sse_E"] = 0.0

    # Center AA class (if allowed)
    if include_center and include_center_identity:
        center_cls = AA_CLASS.get(seq_window[center_idx], "polar")
        for c in AA_CLASS_ORDER:
            features[f"center_{c}"] = 1.0 if c == center_cls else 0.0
    else:
        for c in AA_CLASS_ORDER:
            features[f"center_{c}"] = 0.0

    return features


# ---------------------------------------------------------------------------
# Part B: LOPO classification
# ---------------------------------------------------------------------------

def run_lopo_elastic_net(X, y, protein_ids, feature_names, n_splits=10):
    """Grouped k-fold logistic regression with protein-level held-out groups.

    Uses GroupKFold so no protein appears in both train and test within a fold.
    Returns dict with metrics and per-fold details.
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score
    from sklearn.model_selection import GroupKFold

    proteins = sorted(set(protein_ids))
    if len(proteins) < 3:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "n_folds": 0, "coefs": None}

    le = LabelEncoder()
    groups = le.fit_transform(protein_ids)
    actual_splits = min(n_splits, len(proteins))
    gkf = GroupKFold(n_splits=actual_splits)

    all_probs = np.full(len(y), np.nan)
    coef_accum = []
    fold_count = 0

    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        if y_test.sum() == 0 or y_test.sum() == len(y_test):
            continue
        if y_train.sum() == 0 or (y_train == 0).sum() == 0:
            continue

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        clf = LogisticRegression(
            penalty="l1", solver="liblinear",
            max_iter=1000, class_weight="balanced", random_state=42, C=1.0
        )
        clf.fit(X_train_s, y_train)
        probs = clf.predict_proba(X_test_s)[:, 1]
        all_probs[test_idx] = probs
        coef_accum.append(clf.coef_[0] / scaler.scale_)
        fold_count += 1

    valid = ~np.isnan(all_probs)
    if valid.sum() == 0 or y[valid].sum() == 0:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan, "n_folds": 0, "coefs": None}

    probs_valid = all_probs[valid]
    labels_valid = y[valid]

    try:
        overall_auroc = roc_auc_score(labels_valid, probs_valid)
    except ValueError:
        overall_auroc = np.nan
    try:
        overall_auprc = average_precision_score(labels_valid, probs_valid)
    except ValueError:
        overall_auprc = np.nan

    bal_acc = balanced_accuracy_score(labels_valid, (probs_valid >= 0.5).astype(int))
    mean_coefs = np.mean(coef_accum, axis=0) if coef_accum else None

    return {
        "auroc": float(overall_auroc),
        "auprc": float(overall_auprc),
        "bal_acc": float(bal_acc),
        "n_folds": fold_count,
        "n_pos": int(labels_valid.sum()),
        "n_neg": int((1 - labels_valid).sum()),
        "coefs": mean_coefs,
        "feature_names": feature_names,
    }


def run_lopo_gradient_boosting(X, y, protein_ids, n_splits=10):
    """Grouped k-fold gradient boosting (secondary model)."""
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    from sklearn.metrics import roc_auc_score, average_precision_score, balanced_accuracy_score
    from sklearn.model_selection import GroupKFold

    proteins = sorted(set(protein_ids))
    le = LabelEncoder()
    groups = le.fit_transform(protein_ids)
    actual_splits = min(n_splits, len(proteins))
    gkf = GroupKFold(n_splits=actual_splits)

    all_probs = np.full(len(y), np.nan)

    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, y_train = X[train_idx], y[train_idx]
        X_test, y_test = X[test_idx], y[test_idx]

        if y_test.sum() == 0 or y_test.sum() == len(y_test):
            continue
        if y_train.sum() == 0 or (y_train == 0).sum() == 0:
            continue

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        n_pos = y_train.sum()
        n_neg = len(y_train) - n_pos
        w_pos = len(y_train) / (2 * n_pos) if n_pos > 0 else 1.0
        w_neg = len(y_train) / (2 * n_neg) if n_neg > 0 else 1.0
        sample_weights = np.where(y_train == 1, w_pos, w_neg)

        clf = GradientBoostingClassifier(
            n_estimators=100, max_depth=3, learning_rate=0.1, random_state=42
        )
        clf.fit(X_train_s, y_train, sample_weight=sample_weights)
        probs = clf.predict_proba(X_test_s)[:, 1]
        all_probs[test_idx] = probs

    valid = ~np.isnan(all_probs)
    if valid.sum() == 0 or y[valid].sum() == 0:
        return {"auroc": np.nan, "auprc": np.nan, "bal_acc": np.nan}

    probs_valid = all_probs[valid]
    labels_valid = y[valid]

    try:
        auroc = roc_auc_score(labels_valid, probs_valid)
    except ValueError:
        auroc = np.nan
    try:
        auprc = average_precision_score(labels_valid, probs_valid)
    except ValueError:
        auprc = np.nan
    bal_acc = balanced_accuracy_score(labels_valid, (probs_valid >= 0.5).astype(int))

    return {"auroc": float(auroc), "auprc": float(auprc), "bal_acc": float(bal_acc)}


# ---------------------------------------------------------------------------
# Part B: Build dataset for a given radius and censor variant
# ---------------------------------------------------------------------------

def build_classification_dataset(proteins, matches, seqs, ss_dict, radius, censor_variant="full"):
    """Build X, y, protein_ids for classification at a given radius and censor variant.

    censor_variant: "full", "censor_identity", "censor_all"
    """
    feature_dicts = []
    labels = []
    pids = []

    # Group matches by protein
    matches_by_protein = defaultdict(list)
    for m in matches:
        matches_by_protein[m["protein"]].append(m)

    protein_set = set(p["protein"] for p in proteins)

    for pid in sorted(protein_set):
        if pid not in matches_by_protein:
            continue
        seq = seqs[pid]
        sse = ss_dict[pid]

        protein_matches = matches_by_protein[pid]
        anchor_pos = protein_matches[0]["anchor_pos"]

        # Extract anchor window
        a_seq, a_sse = extract_window(seq, sse, anchor_pos, radius)
        if a_seq is None:
            continue

        include_center = censor_variant == "full"
        include_center_identity = censor_variant != "censor_identity" and censor_variant != "censor_all"
        if censor_variant == "censor_identity":
            include_center = True  # keep SSE etc at center
            include_center_identity = False
        elif censor_variant == "censor_all":
            include_center = False
            include_center_identity = False

        use_pos = radius <= MAX_POSITIONAL_FEATURES_RADIUS

        feats = extract_window_features_seq(a_seq, a_sse, include_center=include_center, include_center_identity=include_center_identity, use_positional=use_pos)
        feature_dicts.append(feats)
        labels.append(1)
        pids.append(pid)

        # Extract control windows
        for m in protein_matches:
            ctrl_pos = m["control_pos"]
            c_seq, c_sse = extract_window(seq, sse, ctrl_pos, radius)
            if c_seq is None:
                continue
            feats = extract_window_features_seq(c_seq, c_sse, include_center=include_center, include_center_identity=include_center_identity, use_positional=use_pos)
            feature_dicts.append(feats)
            labels.append(0)
            pids.append(pid)

    if not feature_dicts:
        return None, None, None, None

    # Convert to arrays
    all_keys = sorted(feature_dicts[0].keys())
    X = np.array([[fd[k] for k in all_keys] for fd in feature_dicts])
    y = np.array(labels)

    return X, y, pids, all_keys


# ---------------------------------------------------------------------------
# Plotting: radius-performance curve
# ---------------------------------------------------------------------------

def plot_radius_curve(results_by_radius, output_path):
    """Plot AUROC and AUPRC vs flank radius for all variants."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for metric_idx, metric_name in enumerate(["auroc", "auprc"]):
        ax = axes[metric_idx]
        for variant in ["full", "censor_identity", "censor_all"]:
            radii_vals = []
            metric_vals = []
            for r in RADII:
                key = f"enet_{variant}"
                if r in results_by_radius and key in results_by_radius[r]:
                    val = results_by_radius[r][key].get(metric_name, np.nan)
                    if not np.isnan(val):
                        radii_vals.append(r)
                        metric_vals.append(val)
            label_map = {"full": "Full window", "censor_identity": "Center AA censored", "censor_all": "Center fully censored"}
            style_map = {"full": "-o", "censor_identity": "--s", "censor_all": "-.^"}
            if radii_vals:
                ax.plot(radii_vals, metric_vals, style_map[variant], label=label_map[variant], markersize=6)

        ax.set_xlabel("Flank radius R")
        ax.set_ylabel(metric_name.upper())
        ax.set_title(f"{metric_name.upper()} vs Flank Radius (Elastic Net)")
        ax.legend(fontsize=8)
        ax.set_xticks(RADII)
        ax.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5, label="chance" if metric_name == "auroc" else None)
        ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved radius curve: {output_path}")


def plot_center_ablation(results_by_radius, output_path):
    """Bar chart comparing full vs center-censored at each radius."""
    fig, ax = plt.subplots(figsize=(10, 5))

    radii_with_data = [r for r in RADII if r in results_by_radius]
    if not radii_with_data:
        return

    x = np.arange(len(radii_with_data))
    width = 0.25

    for i, variant in enumerate(["full", "censor_identity", "censor_all"]):
        vals = []
        for r in radii_with_data:
            key = f"enet_{variant}"
            v = results_by_radius[r].get(key, {}).get("auroc", np.nan)
            vals.append(v)
        label_map = {"full": "Full window", "censor_identity": "Center AA censored", "censor_all": "Center fully censored"}
        color_map = {"full": "#4575b4", "censor_identity": "#fc8d59", "censor_all": "#d73027"}
        ax.bar(x + i * width, vals, width, label=label_map[variant], color=color_map[variant], alpha=0.85)

    ax.set_xlabel("Flank radius R")
    ax.set_ylabel("AUROC")
    ax.set_title("Center-Censor Ablation: AUROC by Radius and Censor Variant")
    ax.set_xticks(x + width)
    ax.set_xticklabels([str(r) for r in radii_with_data])
    ax.legend(fontsize=8)
    ax.axhline(y=0.5, color="gray", linestyle=":", alpha=0.5)
    ax.grid(True, alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved center ablation: {output_path}")


def plot_top_features(coefs, feature_names, output_path, top_n=30):
    """Plot top elastic-net coefficients."""
    if coefs is None:
        return

    abs_coefs = np.abs(coefs)
    top_idx = np.argsort(abs_coefs)[-top_n:][::-1]

    fig, ax = plt.subplots(figsize=(8, max(6, top_n * 0.25)))
    y_pos = np.arange(len(top_idx))
    colors = ["#d73027" if coefs[i] > 0 else "#4575b4" for i in top_idx]
    ax.barh(y_pos, coefs[top_idx], color=colors, alpha=0.8)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([feature_names[i] for i in top_idx], fontsize=7)
    ax.set_xlabel("Elastic-net coefficient (scaled)")
    ax.set_title(f"Top {top_n} Features for Anchor Classification")
    ax.invert_yaxis()
    ax.axvline(x=0, color="black", linewidth=0.5)
    ax.grid(True, alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved top features: {output_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cpu", help="Not used (no model needed)")
    parser.add_argument("--controls", choices=["sse", "structural", "both"], default="both",
                        help="Control matching: 'sse' (SSE-only, 500 proteins), 'structural' (RSA+contacts+SSE, ~17 proteins from v3), 'both' (run both)")
    args = parser.parse_args()

    os.makedirs(REPORT_DIR, exist_ok=True)
    t0 = time.time()

    # --- Load data ---
    print("Loading data...")
    seqs, ss_dict = load_data()

    control_sets = {}

    if args.controls in ("sse", "both"):
        print("\n--- SSE-only matched controls (broad, 500 proteins) ---")
        viz_proteins = select_proteins(seqs, ss_dict, TOP_N_VIZ)
        class_proteins_sse = select_proteins(seqs, ss_dict, TOP_N_CLASS)
        viz_matches = build_matched_controls_sse(viz_proteins, seqs, ss_dict, controls_per_anchor=CONTROLS_PER_ANCHOR)
        class_matches_sse = build_matched_controls_sse(class_proteins_sse, seqs, ss_dict, controls_per_anchor=CONTROLS_PER_ANCHOR)
        n_viz_anchors = len(set((m["protein"], m["anchor_pos"]) for m in viz_matches))
        n_class_anchors = len(set((m["protein"], m["anchor_pos"]) for m in class_matches_sse))
        print(f"  Viz: {n_viz_anchors} anchors with {len(viz_matches)} total control pairs")
        print(f"  Class: {n_class_anchors} anchors with {len(class_matches_sse)} total control pairs")
        control_sets["sse"] = {"class_proteins": class_proteins_sse, "class_matches": class_matches_sse,
                               "viz_proteins": viz_proteins, "viz_matches": viz_matches, "suffix": ""}

    if args.controls in ("structural", "both"):
        print("\n--- Structurally matched controls (RSA+contacts+SSE, v3 subset) ---")
        v3_proteins, v3_matches = load_v3_matched_controls(seqs, ss_dict)
        n_v3_anchors = len(set((m["protein"], m["anchor_pos"]) for m in v3_matches))
        print(f"  {len(v3_proteins)} proteins, {n_v3_anchors} anchors, {len(v3_matches)} total control pairs")
        # For viz, use the same v3 proteins
        control_sets["structural"] = {"class_proteins": v3_proteins, "class_matches": v3_matches,
                                       "viz_proteins": v3_proteins, "viz_matches": v3_matches, "suffix": "_structural"}

    # ===================================================================
    # Run Part A + Part B for each control set
    # ===================================================================
    all_results = {}  # control_name -> {results_by_radius, all_metrics_rows, best_coefs, ...}

    for ctrl_name, ctrl_data in control_sets.items():
        suffix = ctrl_data["suffix"]
        class_proteins = ctrl_data["class_proteins"]
        class_matches = ctrl_data["class_matches"]
        viz_matches_set = ctrl_data["viz_matches"]

        matching_label = "SSE-only" if ctrl_name == "sse" else "structural (SSE+RSA+contacts_8A)"
        print(f"\n{'='*70}")
        print(f"  Control set: {matching_label}")
        print(f"{'='*70}")

        # ---------------------------------------------------------------
        # Part A: Flank pattern discovery
        # ---------------------------------------------------------------
        print(f"\n  === Part A: Flank Pattern Discovery ({ctrl_name}) ===")

        for radius in [10, 20, 30]:
            anchor_windows_seq = []
            anchor_windows_sse = []
            control_windows_seq = []
            control_windows_sse = []

            seen_anchors = set()
            for m in viz_matches_set:
                akey = (m["protein"], m["anchor_pos"])
                if akey in seen_anchors:
                    continue
                seen_anchors.add(akey)
                seq = seqs[m["protein"]]
                sse = ss_dict[m["protein"]]
                ws, we = extract_window(seq, sse, m["anchor_pos"], radius)
                if ws is not None:
                    anchor_windows_seq.append(ws)
                    anchor_windows_sse.append(we)

            for m in viz_matches_set:
                seq = seqs[m["protein"]]
                sse = ss_dict[m["protein"]]
                ws, we = extract_window(seq, sse, m["control_pos"], radius)
                if ws is not None:
                    control_windows_seq.append(ws)
                    control_windows_sse.append(we)

            print(f"    R={radius}: {len(anchor_windows_seq)} anchor, {len(control_windows_seq)} control windows")

            if anchor_windows_seq and control_windows_seq:
                out_path = REPORT_DIR / f"anchor_local_flank_v2_logos_R{radius}{suffix}.png"
                generate_logos(anchor_windows_seq, control_windows_seq, anchor_windows_sse, control_windows_sse, radius, out_path)

        # ---------------------------------------------------------------
        # Part B: Classification
        # ---------------------------------------------------------------
        print(f"\n  === Part B: Classification ({ctrl_name}) ===")

        results_by_radius = {}
        all_metrics_rows = []
        best_coefs = None
        best_feature_names = None
        best_radius_for_coefs = None

        for radius in RADII:
            print(f"\n    Radius R={radius}:")
            results_by_radius[radius] = {}

            for variant in ["full", "censor_identity", "censor_all"]:
                X, y, pids, feat_names = build_classification_dataset(class_proteins, class_matches, seqs, ss_dict, radius, censor_variant=variant)

                if X is None or len(y) < 10:
                    print(f"      {variant}: insufficient data")
                    continue

                n_pos = int(y.sum())
                n_neg = int((1 - y).sum())
                print(f"      {variant}: {len(y)} samples ({n_pos} pos, {n_neg} neg), {X.shape[1]} features")

                enet_result = run_lopo_elastic_net(X, y, pids, feat_names)
                results_by_radius[radius][f"enet_{variant}"] = enet_result
                print(f"        L1 LR: AUROC={enet_result['auroc']:.3f}, AUPRC={enet_result['auprc']:.3f}, bal_acc={enet_result['bal_acc']:.3f} ({enet_result['n_folds']} folds)")

                all_metrics_rows.append({
                    "control_set": ctrl_name,
                    "radius": radius,
                    "variant": variant,
                    "model": "l1_logistic",
                    "auroc": enet_result["auroc"],
                    "auprc": enet_result["auprc"],
                    "bal_acc": enet_result["bal_acc"],
                    "n_folds": enet_result["n_folds"],
                    "n_pos": enet_result["n_pos"],
                    "n_neg": enet_result["n_neg"],
                })

                if variant == "full" and enet_result["coefs"] is not None:
                    if best_coefs is None or enet_result["auroc"] > (results_by_radius.get(best_radius_for_coefs, {}).get("enet_full", {}).get("auroc", 0)):
                        best_coefs = enet_result["coefs"]
                        best_feature_names = enet_result["feature_names"]
                        best_radius_for_coefs = radius

                if variant == "full":
                    gb_result = run_lopo_gradient_boosting(X, y, pids)
                    results_by_radius[radius][f"gb_{variant}"] = gb_result
                    print(f"        GB:    AUROC={gb_result['auroc']:.3f}, AUPRC={gb_result['auprc']:.3f}")
                    all_metrics_rows.append({
                        "control_set": ctrl_name,
                        "radius": radius,
                        "variant": variant,
                        "model": "gradient_boosting",
                        "auroc": gb_result["auroc"],
                        "auprc": gb_result["auprc"],
                        "bal_acc": gb_result["bal_acc"],
                        "n_folds": "",
                        "n_pos": n_pos,
                        "n_neg": n_neg,
                    })

        # ---------------------------------------------------------------
        # Plots for this control set
        # ---------------------------------------------------------------
        plot_radius_curve(results_by_radius, REPORT_DIR / f"anchor_local_flank_v2_radius_curve{suffix}.png")
        plot_center_ablation(results_by_radius, REPORT_DIR / f"anchor_local_flank_v2_center_ablation{suffix}.png")
        if best_coefs is not None:
            plot_top_features(best_coefs, best_feature_names, REPORT_DIR / f"anchor_local_flank_v2_top_features{suffix}.png")

        all_results[ctrl_name] = {
            "results_by_radius": results_by_radius,
            "all_metrics_rows": all_metrics_rows,
            "best_coefs": best_coefs,
            "best_feature_names": best_feature_names,
            "best_radius_for_coefs": best_radius_for_coefs,
            "class_proteins": class_proteins,
            "class_matches": class_matches,
        }

    # ===================================================================
    # Save combined outputs
    # ===================================================================
    print("\n=== Saving Outputs ===")

    # Combined metrics CSV
    all_rows = []
    for ctrl_name, data in all_results.items():
        all_rows.extend(data["all_metrics_rows"])

    metrics_path = REPORT_DIR / "anchor_local_flank_v2_metrics.csv"
    with open(metrics_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["control_set", "radius", "variant", "model", "auroc", "auprc", "bal_acc", "n_folds", "n_pos", "n_neg"])
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)
    print(f"  Saved metrics: {metrics_path}")

    # Coefficients for each control set
    for ctrl_name, data in all_results.items():
        suffix = "_structural" if ctrl_name == "structural" else ""
        if data["best_coefs"] is not None:
            coef_path = REPORT_DIR / f"anchor_local_flank_v2_coefficients{suffix}.csv"
            abs_coefs = np.abs(data["best_coefs"])
            order = np.argsort(abs_coefs)[::-1]
            with open(coef_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["rank", "feature", "coefficient", "abs_coefficient"])
                for rank, idx in enumerate(order):
                    writer.writerow([rank + 1, data["best_feature_names"][idx], f"{data['best_coefs'][idx]:.6f}", f"{abs_coefs[idx]:.6f}"])
            print(f"  Saved coefficients ({ctrl_name}): {coef_path} (radius={data['best_radius_for_coefs']})")

    # Windows CSV
    for ctrl_name, data in all_results.items():
        suffix = "_structural" if ctrl_name == "structural" else ""
        windows_path = REPORT_DIR / f"anchor_local_flank_v2_windows{suffix}.csv"
        with open(windows_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["protein", "anchor_pos", "n_controls", "anchor_sse"])
            seen = set()
            for m in data["class_matches"]:
                key = (m["protein"], m["anchor_pos"])
                if key not in seen:
                    seen.add(key)
                    n_ctrl = sum(1 for mm in data["class_matches"] if mm["protein"] == m["protein"] and mm["anchor_pos"] == m["anchor_pos"])
                    writer.writerow([m["protein"], m["anchor_pos"], n_ctrl, m["anchor_sse"]])
        print(f"  Saved windows ({ctrl_name}): {windows_path}")

    # ===================================================================
    # Report
    # ===================================================================
    print("\n=== Writing Report ===")
    report_path = REPORT_DIR / "anchor_local_flank_v2.md"
    with open(report_path, "w") as f:
        f.write("# Anchor Local Flank v2: Results\n\n")

        for ctrl_name, data in all_results.items():
            matching_label = "SSE-only matched (500 proteins)" if ctrl_name == "sse" else "Structurally matched (SSE+RSA+contacts_8A, v3 subset)"
            suffix = "_structural" if ctrl_name == "structural" else ""
            results_by_radius = data["results_by_radius"]
            best_coefs = data["best_coefs"]
            best_feature_names = data["best_feature_names"]
            best_radius_for_coefs = data["best_radius_for_coefs"]

            f.write(f"## {matching_label}\n\n")

            n_proteins = len(data["class_proteins"])
            n_anchors = len(set((m["protein"], m["anchor_pos"]) for m in data["class_matches"]))
            n_controls = len(data["class_matches"])
            f.write(f"Proteins: {n_proteins}, Anchors: {n_anchors}, Control pairs: {n_controls}\n\n")

            f.write("### Radius-Performance Table (L1 Logistic Regression)\n\n")
            f.write("| Radius | Full AUROC | Full AUPRC | Censor-ID AUROC | Censor-ID AUPRC | Censor-All AUROC | Censor-All AUPRC |\n")
            f.write("|--------|-----------|-----------|----------------|----------------|-----------------|----------------|\n")
            for r in RADII:
                vals = []
                for variant in ["full", "censor_identity", "censor_all"]:
                    key = f"enet_{variant}"
                    d = results_by_radius.get(r, {}).get(key, {})
                    auroc = d.get("auroc", np.nan)
                    auprc = d.get("auprc", np.nan)
                    vals.append(f"{auroc:.3f}" if not np.isnan(auroc) else "N/A")
                    vals.append(f"{auprc:.3f}" if not np.isnan(auprc) else "N/A")
                f.write(f"| {r} | {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} | {vals[4]} | {vals[5]} |\n")

            f.write("\n### Gradient Boosting Comparison (Full Window Only)\n\n")
            f.write("| Radius | GB AUROC | GB AUPRC | LR AUROC | LR AUPRC |\n")
            f.write("|--------|---------|---------|---------|--------|\n")
            for r in RADII:
                gb = results_by_radius.get(r, {}).get("gb_full", {})
                en = results_by_radius.get(r, {}).get("enet_full", {})
                gb_auroc = gb.get("auroc", np.nan)
                gb_auprc = gb.get("auprc", np.nan)
                en_auroc = en.get("auroc", np.nan)
                en_auprc = en.get("auprc", np.nan)
                f.write(f"| {r} | {gb_auroc:.3f} | {gb_auprc:.3f} | {en_auroc:.3f} | {en_auprc:.3f} |\n")

            if best_coefs is not None:
                f.write(f"\n### Top Features (L1 LR, R={best_radius_for_coefs})\n\n")
                abs_c = np.abs(best_coefs)
                top_idx = np.argsort(abs_c)[-20:][::-1]
                f.write("| Rank | Feature | Coefficient |\n")
                f.write("|------|---------|------------|\n")
                for rank, idx in enumerate(top_idx):
                    f.write(f"| {rank + 1} | {best_feature_names[idx]} | {best_coefs[idx]:.4f} |\n")

            f.write("\n---\n\n")

    print(f"  Saved report: {report_path}")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
