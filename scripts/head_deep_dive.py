#!/usr/bin/env python3
# %% [markdown]
# # Head Deep Dive: Per-Head Analysis Across All Proteins
#
# Given a specific (layer, head), this notebook:
# 1. Discovers all proteins with cached data
# 2. Loads indirect effects, cell attributions, and attention patterns for that head
# 3. Runs anchor analysis (from anchor_interp) scoped to that head
# 4. Shows top attention weights and cell-level patterns
#
# Usage (as script):
#   python scripts/head_deep_dive.py --layer 6 --head 3
#
# Or open in VS Code / Jupyter and set TARGET_LAYER / TARGET_HEAD below.

# %% ── Imports ────────────────────────────────────────────────────────────────

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "reports" / "cache"
REPORT_DIR = ROOT / "reports" / "outputs"
CONFIG_DIR = ROOT / "configs"

NUM_LAYERS = 33
NUM_HEADS = 20

# %% ── Configuration ─────────────────────────────────────────────────────────

import argparse as _ap

_p = _ap.ArgumentParser()
_p.add_argument("--layer", type=int, default=10)
_p.add_argument("--head", type=int, default=9)
_args, _ = _p.parse_known_args()

TARGET_LAYER = _args.layer
TARGET_HEAD = _args.head

print(f"=== Head Deep Dive: L{TARGET_LAYER}H{TARGET_HEAD} ===\n")

# %% ── Load configs ──────────────────────────────────────────────────────────

with open(CONFIG_DIR / "common.json") as f:
    COMMON_CFG = json.load(f)

with open(CONFIG_DIR / "proteins.json") as f:
    PROTEIN_CONFIGS = json.load(f)

FAITH_TARGET = COMMON_CFG["faith_target"]
SEGMENT_RADIUS = COMMON_CFG.get("segment_radius", 5)

# %% ── Discover available proteins ───────────────────────────────────────────

def discover_proteins() -> list[str]:
    """Find proteins that have all required cached files."""
    available = []
    for d in sorted(CACHE_DIR.iterdir()):
        if not d.is_dir():
            continue
        has_ie = (d / "indirect_effects.pt").exists()
        has_cell = (d / "cell_attr.pt").exists()
        has_attn = (d / "full_seq_attn_cache.pt").exists()
        if has_ie and has_cell:
            available.append(d.name)
    return available

ALL_PROTEINS = discover_proteins()
print(f"Found {len(ALL_PROTEINS)} proteins with cached data")

# proteins that also have full attention cached
PROTEINS_WITH_ATTN = [p for p in ALL_PROTEINS if (CACHE_DIR / p / "full_seq_attn_cache.pt").exists()]
print(f"  {len(PROTEINS_WITH_ATTN)} have full_seq_attn_cache.pt")

# %% ── Load indirect effects for target head across proteins ─────────────────

def load_indirect_effect(protein: str) -> float | None:
    path = CACHE_DIR / protein / "indirect_effects.pt"
    d = torch.load(path, map_location="cpu", weights_only=False)
    ie_LH = d["indirect_effects_LH"]
    return ie_LH[TARGET_LAYER, TARGET_HEAD].item()

ie_by_protein = {}
for p in ALL_PROTEINS:
    ie = load_indirect_effect(p)
    if ie is not None:
        ie_by_protein[p] = ie

print(f"\nIndirect effect of L{TARGET_LAYER}H{TARGET_HEAD} across {len(ie_by_protein)} proteins:")
for p in sorted(ie_by_protein, key=lambda x: -ie_by_protein[x]):
    print(f"  {p}: IE = {ie_by_protein[p]:.4f}")

# %% ── Determine circuit membership ──────────────────────────────────────────
# For each protein, check if this head is in the circuit (top pos_k heads).

def load_circuit_membership(protein: str) -> dict:
    """Check if target head is in this protein's circuit. Returns metadata."""
    cr_d = torch.load(CACHE_DIR / protein / "circuit_results.pt", map_location="cpu", weights_only=False)
    ie_d = torch.load(CACHE_DIR / protein / "indirect_effects.pt", map_location="cpu", weights_only=False)

    ie_LH = ie_d["indirect_effects_LH"]
    cr = cr_d["circuit_results"]

    # Find pos_k (crossing threshold)
    pos_entry = cr["pos"]
    pos_k = None
    for k_val, f_val in zip(pos_entry["k"], pos_entry["faith"]):
        if f_val >= FAITH_TARGET:
            pos_k = k_val
            break
    if pos_k is None:
        pos_k = COMMON_CFG["topk_heads"]

    # Rank of this head
    flat = ie_LH.flatten()
    sorted_idx = flat.argsort(descending=True)
    rank = None
    for i, idx in enumerate(sorted_idx):
        l = idx.item() // NUM_HEADS
        h = idx.item() % NUM_HEADS
        if l == TARGET_LAYER and h == TARGET_HEAD:
            rank = i
            break

    in_circuit = rank is not None and rank < pos_k
    return {"pos_k": pos_k, "rank": rank, "in_circuit": in_circuit, "ie": ie_LH[TARGET_LAYER, TARGET_HEAD].item()}

circuit_info = {}
for p in ALL_PROTEINS:
    try:
        circuit_info[p] = load_circuit_membership(p)
    except Exception as e:
        print(f"  {p}: SKIPPED ({e})")

n_in_circuit = sum(1 for v in circuit_info.values() if v["in_circuit"])
print(f"\nL{TARGET_LAYER}H{TARGET_HEAD} is in the circuit for {n_in_circuit}/{len(circuit_info)} proteins")
print(f"{'Protein':>8} {'Rank':>5} {'pos_k':>5} {'In Circuit':>10} {'IE':>8}")
print("-" * 42)
for p in sorted(circuit_info, key=lambda x: circuit_info[x]["rank"]):
    ci = circuit_info[p]
    marker = "YES" if ci["in_circuit"] else ""
    print(f"{p:>8} {ci['rank']:>5} {ci['pos_k']:>5} {marker:>10} {ci['ie']:>8.4f}")

# %% ── Load cell attributions for target head ────────────────────────────────
# Cell attribution tuples: (layer, head, row_pos, col_pos, attr_value, raw_grad)

def load_cells_for_head(protein: str, topk: int = 50) -> list[dict]:
    """Load top-k cells (by attribution) for the target head in this protein."""
    d = torch.load(CACHE_DIR / protein / "cell_attr.pt", map_location="cpu", weights_only=False)
    cells = d["cell_attr_sorted"]

    head_cells = []
    for layer, head, row, col, attr, raw in cells:
        if layer == TARGET_LAYER and head == TARGET_HEAD:
            head_cells.append({"row": row, "col": col, "attr": attr, "raw": raw})
        if len(head_cells) >= topk:
            break

    return head_cells

cells_by_protein = {}
for p in ALL_PROTEINS:
    try:
        cells = load_cells_for_head(p, topk=100)
        if cells:
            cells_by_protein[p] = cells
    except Exception as e:
        print(f"  {p}: cell load failed ({e})")

print(f"\nCell attributions found for {len(cells_by_protein)} proteins")
for p in sorted(cells_by_protein, key=lambda x: -len(cells_by_protein[x])):
    c = cells_by_protein[p]
    total_attr = sum(x["attr"] for x in c)
    print(f"  {p}: {len(c)} cells, total_attr = {total_attr:.4f}, top_attr = {c[0]['attr']:.4f}")

# %% ── Classify cells by region ──────────────────────────────────────────────

def classify_cell_position(row: int, col: int, config: dict) -> str:
    """Classify a cell (row, col) in token space (1-indexed with BOS offset) into region labels."""
    pos1, pos2 = config["contact_pair"]
    r = SEGMENT_RADIUS
    ss1_start, ss1_end = pos1 - r, pos1 + r + 1
    ss2_start, ss2_end = pos2 - r, pos2 + r + 1
    clean_f = config["clean_flank"]

    # Convert from token space (includes BOS at 0) to sequence space
    row_seq = row - 1
    col_seq = col - 1

    def region_of(p):
        if ss1_start <= p < ss1_end:
            return "ss1"
        if ss2_start <= p < ss2_end:
            return "ss2"
        if max(0, ss1_start - clean_f) <= p < ss1_start or ss1_end <= p < ss1_end + clean_f:
            return "flkL"
        if max(0, ss2_start - clean_f) <= p < ss2_start or ss2_end <= p < ss2_end + clean_f:
            return "flkR"
        return "other"

    r_row = region_of(row_seq)
    r_col = region_of(col_seq)
    if r_row == r_col:
        return f"INTRA:{r_row}"
    return f"{r_row}\u2192{r_col}"


print(f"\nCell region breakdown per protein:")
for p in sorted(cells_by_protein):
    if p not in PROTEIN_CONFIGS:
        continue
    cfg = PROTEIN_CONFIGS[p]
    region_counts = Counter()
    for c in cells_by_protein[p]:
        region_counts[classify_cell_position(c["row"], c["col"], cfg)] += 1
    top_regions = region_counts.most_common(5)
    region_str = ", ".join(f"{r}={n}" for r, n in top_regions)
    print(f"  {p}: {region_str}")

# %% ── Anchor analysis for target head ────────────────────────────────────────
# Reuses logic from anchor_interp.py, but filters to only the target head.

def load_summary_rows_for_head(protein: str) -> list[dict]:
    """Load summary CSV rows that match the target head."""
    csv_path = REPORT_DIR / protein / f"{protein}_summary.csv"
    if not csv_path.exists():
        return []
    rows = []
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if int(row["layer"]) == TARGET_LAYER and int(row["head"]) == TARGET_HEAD:
                rows.append(row)
    return rows


def parse_anchor_label(label: str) -> list[tuple[str, int]]:
    if not label or not label.strip():
        return []
    result = []
    for p in label.split("/"):
        p = p.strip()
        m = re.match(r"([A-Z])(\d+)", p)
        if m:
            result.append((m.group(1), int(m.group(2))))
    return result


def extract_anchors_for_head(rows: list[dict]) -> dict:
    """Extract anchor residues from summary rows for the target head only."""
    anchors = defaultdict(lambda: {"aa_from_label": None, "k_type": None, "q_type": None, "ranks": []})
    for row in rows:
        rank = int(row["rank"])
        k_type = row["k_anchor"].strip()
        q_type = row["q_anchor"].strip()

        if k_type in ("SINGLE-ANCHOR", "DUAL-ANCHOR", "MULTI-ANCHOR"):
            for aa, pos in parse_anchor_label(row["k_label"]):
                anchors[pos]["aa_from_label"] = aa
                anchors[pos]["k_type"] = k_type
                anchors[pos]["ranks"].append(rank)

        if q_type in ("SINGLE-ANCHOR", "DUAL-ANCHOR", "MULTI-ANCHOR"):
            for aa, pos in parse_anchor_label(row["q_label"]):
                anchors[pos]["aa_from_label"] = aa
                anchors[pos]["q_type"] = q_type
                anchors[pos]["ranks"].append(rank)

    return dict(anchors)


def load_sequence(protein: str) -> str:
    with open(DATA_DIR / "full_seq_dict.json") as _f:
        seqs = json.load(_f)
    return seqs.get(protein, "")


def load_sse(protein: str) -> str:
    with open(DATA_DIR / "ss_dict.json") as _f:
        ss = json.load(_f)
    return ss.get(f"{protein}.pdb", "")


def load_conservation(protein: str) -> dict:
    ev_dir = DATA_DIR / f"{protein}_EV"
    candidates = sorted(ev_dir.glob("TARGET_b*/align/TARGET_b*_frequencies.csv"))
    if not candidates:
        return {}
    cons = {}
    with open(candidates[0]) as _f:
        for row in csv.DictReader(_f):
            cons[int(row["i"]) - 1] = float(row["conservation"])
    return cons


anchor_data_by_protein = {}
for p in ALL_PROTEINS:
    rows = load_summary_rows_for_head(p)
    if not rows:
        continue
    anchors = extract_anchors_for_head(rows)
    if anchors:
        anchor_data_by_protein[p] = {"rows": rows, "anchors": anchors}

print(f"\nAnchor analysis for L{TARGET_LAYER}H{TARGET_HEAD}:")
print(f"  Found anchor data in {len(anchor_data_by_protein)} proteins\n")

# Collect all anchor positions across proteins with annotations
all_anchor_records = []

for p in sorted(anchor_data_by_protein):
    anchors = anchor_data_by_protein[p]["anchors"]
    seq = load_sequence(p)
    sse = load_sse(p)
    cons = load_conservation(p)
    cfg = PROTEIN_CONFIGS.get(p, {})
    pos1, pos2 = cfg.get("contact_pair", (None, None))

    for pos in sorted(anchors):
        info = anchors[pos]
        aa = seq[pos] if pos < len(seq) else "?"
        sse_char = sse[pos] if pos < len(sse) else "?"
        sse_type = sse_char if sse_char in ("H", "E") else "C"
        cons_val = cons.get(pos, None)

        role_parts = []
        if info["k_type"]:
            role_parts.append(f"K({info['k_type'].replace('-ANCHOR', '')})")
        if info["q_type"]:
            role_parts.append(f"Q({info['q_type'].replace('-ANCHOR', '')})")
        role_str = "+".join(role_parts)

        # Relative position to contact pair
        rel = ""
        if pos1 is not None:
            if abs(pos - pos1) <= SEGMENT_RADIUS:
                rel = "ss1"
            elif abs(pos - pos2) <= SEGMENT_RADIUS:
                rel = "ss2"
            elif pos < pos1:
                rel = "flkL"
            elif pos > pos2:
                rel = "flkR"
            else:
                rel = "between"

        all_anchor_records.append({
            "protein": p, "pos": pos, "aa": aa, "role": role_str,
            "sse": sse_type, "conservation": cons_val, "region": rel,
        })

if all_anchor_records:
    print(f"{'Protein':>8} {'Pos':>4} {'AA':>2} {'Role':>20} {'SSE':>3} {'Cons':>6} {'Region':>7}")
    print("-" * 60)
    for r in all_anchor_records:
        cons_str = f"{r['conservation']:.3f}" if r["conservation"] is not None else "N/A"
        print(f"{r['protein']:>8} {r['pos']:>4} {r['aa']:>2} {r['role']:>20} {r['sse']:>3} {cons_str:>6} {r['region']:>7}")

# %% ── Cross-protein anchor recurrence ────────────────────────────────────────
# Which amino acids / SSE types / regions recur as anchors for this head?

if all_anchor_records:
    print(f"\n--- Anchor summary for L{TARGET_LAYER}H{TARGET_HEAD} ---")

    aa_counts = Counter(r["aa"] for r in all_anchor_records)
    sse_counts = Counter(r["sse"] for r in all_anchor_records)
    region_counts = Counter(r["region"] for r in all_anchor_records)
    role_counts = Counter(r["role"] for r in all_anchor_records)

    print(f"\nAA distribution: {dict(aa_counts.most_common())}")
    print(f"SSE distribution: {dict(sse_counts)}")
    print(f"Region distribution: {dict(region_counts)}")
    print(f"Role distribution: {dict(role_counts)}")

    cons_vals = [r["conservation"] for r in all_anchor_records if r["conservation"] is not None]
    if cons_vals:
        print(f"Conservation: mean={np.mean(cons_vals):.3f}, median={np.median(cons_vals):.3f}, range=[{min(cons_vals):.3f}, {max(cons_vals):.3f}]")

# %% ── Top attention weights for target head ──────────────────────────────────
# For each protein with full_seq_attn_cache, extract the top-K attention weights.

def load_top_attn_weights(protein: str, topk: int = 20) -> list[dict]:
    """Load the top-k attention weights (by magnitude) for the target head."""
    path = CACHE_DIR / protein / "full_seq_attn_cache.pt"
    d = torch.load(path, map_location="cpu", weights_only=False)
    attn_LBHLL = d["attn_LBHLL"]
    seq = d.get("sequence", "")

    # attn_LBHLL is a list of tensors, each (B, H, L, L)
    attn_LL = attn_LBHLL[TARGET_LAYER][0, TARGET_HEAD]  # (L, L)
    L = attn_LL.shape[0]

    # Flatten and get top-k (excluding BOS/EOS self-attention)
    flat = attn_LL.flatten()
    topk_vals, topk_idx = flat.topk(min(topk + 10, flat.numel()))  # grab extra to filter specials

    results = []
    for val, idx in zip(topk_vals, topk_idx):
        row = idx.item() // L
        col = idx.item() % L
        # Skip BOS (0) and EOS (L-1) self-loops
        if row == col and (row == 0 or row == L - 1):
            continue
        row_aa = seq[row - 1] if 0 < row < L - 1 and row - 1 < len(seq) else "<special>"
        col_aa = seq[col - 1] if 0 < col < L - 1 and col - 1 < len(seq) else "<special>"
        results.append({
            "row_tok": row, "col_tok": col,
            "row_seq": row - 1, "col_seq": col - 1,
            "row_aa": row_aa, "col_aa": col_aa,
            "weight": val.item(),
        })
        if len(results) >= topk:
            break

    return results


print(f"\nTop attention weights for L{TARGET_LAYER}H{TARGET_HEAD}:")
attn_weights_by_protein = {}

for p in PROTEINS_WITH_ATTN:
    try:
        weights = load_top_attn_weights(p, topk=20)
        if weights:
            attn_weights_by_protein[p] = weights
    except Exception as e:
        print(f"  {p}: attn load failed ({e})")

for p in sorted(attn_weights_by_protein):
    cfg = PROTEIN_CONFIGS.get(p, {})
    pos1, pos2 = cfg.get("contact_pair", (None, None))
    weights = attn_weights_by_protein[p]

    print(f"\n  {p} (contact pair: {pos1}, {pos2}):")
    print(f"    {'row':>4} {'col':>4} {'row_AA':>6} {'col_AA':>6} {'weight':>8} {'region':>12}")
    print(f"    " + "-" * 48)
    for w in weights[:10]:
        region = ""
        if pos1 is not None:
            region = classify_cell_position(w["row_tok"], w["col_tok"], cfg)
        print(f"    {w['row_seq']:>4} {w['col_seq']:>4} {w['row_aa']:>6} {w['col_aa']:>6} {w['weight']:>8.4f} {region:>12}")

# %% ── Attention pattern statistics ───────────────────────────────────────────
# For each protein, compute summary stats of the attention distribution.

def compute_attn_stats(protein: str) -> dict | None:
    """Compute attention pattern statistics for the target head."""
    path = CACHE_DIR / protein / "full_seq_attn_cache.pt"
    d = torch.load(path, map_location="cpu", weights_only=False)
    attn_LBHLL = d["attn_LBHLL"]

    attn_LL = attn_LBHLL[TARGET_LAYER][0, TARGET_HEAD]  # (L, L)
    L = attn_LL.shape[0]

    # Trim BOS/EOS for stats on actual residue attention
    attn_AA = attn_LL[1:-1, 1:-1]  # (A, A) where A = seq_len
    A = attn_AA.shape[0]

    # Entropy per query position (how spread is attention from each position)
    eps = 1e-10
    entropy_per_query = -(attn_AA * (attn_AA + eps).log()).sum(dim=-1)  # (A,)

    # Max attention per query (how peaked is attention)
    max_per_query = attn_AA.max(dim=-1).values  # (A,)

    # Fraction of attention on contact pair region
    cfg = PROTEIN_CONFIGS.get(protein, {})
    pos1, pos2 = cfg.get("contact_pair", (None, None))
    contact_frac = None
    if pos1 is not None:
        r = SEGMENT_RADIUS
        ss1_slice = slice(max(0, pos1 - r), min(A, pos1 + r + 1))
        ss2_slice = slice(max(0, pos2 - r), min(A, pos2 + r + 1))
        contact_mass = attn_AA[:, ss1_slice].sum() + attn_AA[:, ss2_slice].sum()
        contact_frac = (contact_mass / attn_AA.sum()).item()

    return {
        "seq_len": A,
        "mean_entropy": entropy_per_query.mean().item(),
        "std_entropy": entropy_per_query.std().item(),
        "mean_max_attn": max_per_query.mean().item(),
        "median_max_attn": max_per_query.median().item(),
        "global_max": attn_AA.max().item(),
        "contact_region_frac": contact_frac,
    }


print(f"\nAttention pattern statistics for L{TARGET_LAYER}H{TARGET_HEAD}:")
print(f"{'Protein':>8} {'SeqLen':>6} {'MeanEnt':>8} {'MeanMax':>8} {'MedMax':>8} {'GlobMax':>8} {'ContactFrac':>11}")
print("-" * 70)

attn_stats_by_protein = {}
for p in PROTEINS_WITH_ATTN:
    try:
        stats = compute_attn_stats(p)
        if stats:
            attn_stats_by_protein[p] = stats
            cf_str = f"{stats['contact_region_frac']:.3f}" if stats["contact_region_frac"] is not None else "N/A"
            print(f"{p:>8} {stats['seq_len']:>6} {stats['mean_entropy']:>8.3f} {stats['mean_max_attn']:>8.4f} {stats['median_max_attn']:>8.4f} {stats['global_max']:>8.4f} {cf_str:>11}")
    except Exception as e:
        print(f"{p:>8} FAILED: {e}")

# %% ── Cross-protein attention target recurrence ──────────────────────────────
# Which sequence positions receive the most attention from this head across proteins?
# We look at this in relative terms: position relative to contact pair.

def get_relative_attn_profile(protein: str) -> dict | None:
    """Get attention mass in each region for the target head."""
    path = CACHE_DIR / protein / "full_seq_attn_cache.pt"
    d = torch.load(path, map_location="cpu", weights_only=False)
    attn_LBHLL = d["attn_LBHLL"]
    attn_LL = attn_LBHLL[TARGET_LAYER][0, TARGET_HEAD]
    attn_AA = attn_LL[1:-1, 1:-1]
    A = attn_AA.shape[0]

    cfg = PROTEIN_CONFIGS.get(protein, {})
    if "contact_pair" not in cfg:
        return None
    pos1, pos2 = cfg["contact_pair"]
    r = SEGMENT_RADIUS
    clean_f = cfg["clean_flank"]

    ss1_start, ss1_end = pos1 - r, pos1 + r + 1
    ss2_start, ss2_end = pos2 - r, pos2 + r + 1

    # Attention received by each region (summed over all query positions)
    col_sums = attn_AA.sum(dim=0)  # (A,) — total attention received by each key position

    region_mass = defaultdict(float)
    for j in range(A):
        if ss1_start <= j < ss1_end:
            region = "ss1"
        elif ss2_start <= j < ss2_end:
            region = "ss2"
        elif max(0, ss1_start - clean_f) <= j < ss1_start or ss1_end <= j < ss1_end + clean_f:
            region = "flkL"
        elif max(0, ss2_start - clean_f) <= j < ss2_start or ss2_end <= j < ss2_end + clean_f:
            region = "flkR"
        else:
            region = "other"
        region_mass[region] += col_sums[j].item()

    total = sum(region_mass.values())
    if total > 0:
        for k in region_mass:
            region_mass[k] /= total

    return dict(region_mass)


print(f"\nAttention mass by region (fraction of total key-side attention received):")
print(f"{'Protein':>8} {'ss1':>6} {'ss2':>6} {'flkL':>6} {'flkR':>6} {'other':>6}")
print("-" * 42)

region_profiles = {}
for p in PROTEINS_WITH_ATTN:
    try:
        profile = get_relative_attn_profile(p)
        if profile:
            region_profiles[p] = profile
            print(f"{p:>8} {profile.get('ss1', 0):>6.3f} {profile.get('ss2', 0):>6.3f} {profile.get('flkL', 0):>6.3f} {profile.get('flkR', 0):>6.3f} {profile.get('other', 0):>6.3f}")
    except Exception as e:
        print(f"{p:>8} FAILED: {e}")

if region_profiles:
    print(f"\nMean across {len(region_profiles)} proteins:")
    for region in ["ss1", "ss2", "flkL", "flkR", "other"]:
        vals = [profile.get(region, 0) for profile in region_profiles.values()]
        print(f"  {region}: {np.mean(vals):.3f} +/- {np.std(vals):.3f}")

# %% ── Summary ────────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"Summary for L{TARGET_LAYER}H{TARGET_HEAD}")
print(f"{'='*60}")

# Circuit membership
in_circuit_proteins = [p for p, ci in circuit_info.items() if ci["in_circuit"]]
print(f"\nCircuit membership: {len(in_circuit_proteins)}/{len(circuit_info)} proteins")
if in_circuit_proteins:
    ranks = [circuit_info[p]["rank"] for p in in_circuit_proteins]
    print(f"  Rank when in circuit: mean={np.mean(ranks):.1f}, range=[{min(ranks)}, {max(ranks)}]")

# IE stats
ie_vals = list(ie_by_protein.values())
print(f"\nIndirect effect: mean={np.mean(ie_vals):.4f}, std={np.std(ie_vals):.4f}, range=[{min(ie_vals):.4f}, {max(ie_vals):.4f}]")

# Anchor summary
if all_anchor_records:
    n_proteins_with_anchor = len(set(r["protein"] for r in all_anchor_records))
    print(f"\nAnchor residues: {len(all_anchor_records)} across {n_proteins_with_anchor} proteins")
else:
    print(f"\nNo anchor data found for this head")

# Attention pattern
if attn_stats_by_protein:
    mean_ent = np.mean([s["mean_entropy"] for s in attn_stats_by_protein.values()])
    mean_max = np.mean([s["mean_max_attn"] for s in attn_stats_by_protein.values()])
    print(f"\nAttention: mean_entropy={mean_ent:.3f}, mean_max_attn={mean_max:.4f}")

print()

# %%
