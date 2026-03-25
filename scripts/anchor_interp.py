#!/usr/bin/env python3
"""Anchor residue interpretation for contact pattern analysis.

For each residue that acts as an anchor in the circuit heads, collects:
- Which heads use it as anchor (and count)
- Whether it serves as K anchor, Q anchor, or both
- Amino acid identity
- Conservation score
- SSE assignment (H/E/C)
- Position within SSE (boundary vs interior)
- Whether it's a jump residue (at the clean/corrupt flank boundary)
- Solvent accessibility estimate from PDB (contact-number proxy)

Usage:
    python scripts/anchor_interp.py --protein 2B61A
    python scripts/anchor_interp.py --protein 2B61A --no-solvent
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports" / "outputs"
CONFIG_DIR = ROOT / "configs"


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_protein_config(protein: str) -> dict:
    with open(CONFIG_DIR / "proteins.json") as f:
        configs = json.load(f)
    if protein not in configs:
        sys.exit(f"Protein {protein} not found in configs/proteins.json")
    return configs[protein]


def load_sequence(protein: str) -> str:
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    if protein not in seqs:
        sys.exit(f"Protein {protein} not found in data/full_seq_dict.json")
    return seqs[protein]


def load_sse(protein: str) -> str:
    with open(DATA_DIR / "ss_dict.json") as f:
        ss = json.load(f)
    key = f"{protein}.pdb"
    if key not in ss:
        sys.exit(f"{key} not found in data/ss_dict.json")
    return ss[key]


def load_conservation(protein: str) -> dict:
    """Returns dict mapping 0-indexed position -> conservation score."""
    ev_dir = DATA_DIR / f"{protein}_EV"
    candidates = sorted(ev_dir.glob("TARGET_b*/align/TARGET_b*_frequencies.csv"))
    if not candidates:
        sys.exit(f"Conservation file not found under {ev_dir}/TARGET_b*/align/")
    csv_path = candidates[0]
    if not csv_path.exists():
        sys.exit(f"Conservation file not found: {csv_path}")
    cons = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pos_1indexed = int(row["i"])
            cons[pos_1indexed - 1] = float(row["conservation"])
    return cons


def load_summary_csv(protein: str) -> list[dict]:
    csv_path = REPORT_DIR / protein / f"{protein}_summary.csv"
    if not csv_path.exists():
        sys.exit(f"Summary CSV not found: {csv_path}. Run contact_pattern_v2.py first.")
    with open(csv_path) as f:
        return list(csv.DictReader(f))


def load_couplings(protein: str) -> dict:
    """Load pairwise coupling scores.

    Returns dict: (pos_0idx_i, pos_0idx_j) -> score, with both orderings."""
    ev_dir = DATA_DIR / f"{protein}_EV"
    candidates = sorted(ev_dir.glob("TARGET_b*/couplings/TARGET_b*_CouplingScores.csv"))
    if not candidates:
        return {}
    csv_path = candidates[0]
    couplings = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            i_0 = int(row["i"]) - 1
            j_0 = int(row["j"]) - 1
            score = float(row["score"])
            couplings[(i_0, j_0)] = score
            couplings[(j_0, i_0)] = score
    return couplings


# ---------------------------------------------------------------------------
# Parsing anchors from summary CSV
# ---------------------------------------------------------------------------

def parse_anchor_label(label: str) -> list[tuple[str, int]]:
    """Parse anchor label like 'F365/I133' into [(F, 365), (I, 133)].
    Returns empty list for empty labels."""
    if not label or not label.strip():
        return []
    parts = label.split("/")
    result = []
    for p in parts:
        p = p.strip()
        m = re.match(r"([A-Z])(\d+)", p)
        if m:
            result.append((m.group(1), int(m.group(2))))
    return result


def extract_anchors(rows: list[dict]) -> dict:
    """Extract all anchor residues from summary CSV.

    Returns dict: pos -> {
        'aa_from_label': str,
        'k_heads': [(layer, head, anchor_type, rank), ...],
        'q_heads': [(layer, head, anchor_type, rank), ...],
    }
    """
    anchors = defaultdict(lambda: {"aa_from_label": None, "k_heads": [], "q_heads": []})

    for row in rows:
        layer = int(row["layer"])
        head = int(row["head"])
        rank = int(row["rank"])
        k_type = row["k_anchor"].strip()
        q_type = row["q_anchor"].strip()

        if k_type in ("SINGLE-ANCHOR", "DUAL-ANCHOR", "MULTI-ANCHOR"):
            for aa, pos in parse_anchor_label(row["k_label"]):
                anchors[pos]["aa_from_label"] = aa
                anchors[pos]["k_heads"].append((layer, head, k_type, rank))

        if q_type in ("SINGLE-ANCHOR", "DUAL-ANCHOR", "MULTI-ANCHOR"):
            for aa, pos in parse_anchor_label(row["q_label"]):
                anchors[pos]["aa_from_label"] = aa
                anchors[pos]["q_heads"].append((layer, head, q_type, rank))

    return dict(anchors)


# ---------------------------------------------------------------------------
# SSE analysis
# ---------------------------------------------------------------------------

def compute_sse_segments(sse_str: str) -> list[tuple[str, int, int]]:
    """Parse SSE string into segments: [(type, start, end), ...].
    type is 'H', 'E', or 'C' (coil, for '-').
    start/end are 0-indexed, end is inclusive."""
    segments = []
    if not sse_str:
        return segments
    current = sse_str[0]
    start = 0
    for i in range(1, len(sse_str)):
        if sse_str[i] != current:
            seg_type = current if current in ("H", "E") else "C"
            segments.append((seg_type, start, i - 1))
            current = sse_str[i]
            start = i
    seg_type = current if current in ("H", "E") else "C"
    segments.append((seg_type, start, len(sse_str) - 1))
    return segments


def get_sse_position_info(pos: int, sse_str: str, segments: list[tuple[str, int, int]]) -> tuple[str, str, int]:
    """Returns (sse_type, boundary_or_interior, segment_length) for a position.
    boundary = first or last residue of an H or E segment."""
    char = sse_str[pos] if pos < len(sse_str) else "-"
    sse_type = char if char in ("H", "E") else "C"

    if sse_type == "C":
        return sse_type, "-", 0

    for seg_type, seg_start, seg_end in segments:
        if seg_type == sse_type and seg_start <= pos <= seg_end:
            seg_len = seg_end - seg_start + 1
            if pos == seg_start or pos == seg_end:
                return sse_type, "boundary", seg_len
            else:
                return sse_type, "interior", seg_len

    return sse_type, "-", 0


# ---------------------------------------------------------------------------
# Jump residue detection
# ---------------------------------------------------------------------------

def get_jump_residues(config: dict) -> set[int]:
    """Identify the residues at the clean/corrupt flank boundary.

    These are positions included in the clean subsequence but excluded from
    the corrupt subsequence — the ones whose presence/absence causes the
    contact prediction jump."""
    pos1, pos2 = config["contact_pair"]
    clean_f = config["clean_flank"]
    corrupt_f = config["corrupt_flank"]
    radius = 5

    ss1_start = pos1 - radius
    ss1_end = pos1 + radius + 1
    ss2_start = pos2 - radius
    ss2_end = pos2 + radius + 1

    jump = set()

    clean_left_start = ss1_start - clean_f
    corrupt_left_start = ss1_start - corrupt_f
    for p in range(clean_left_start, corrupt_left_start):
        jump.add(p)

    clean_left_end = ss1_end + clean_f
    corrupt_left_end = ss1_end + corrupt_f
    for p in range(corrupt_left_end, clean_left_end):
        jump.add(p)

    clean_right_start = ss2_start - clean_f
    corrupt_right_start = ss2_start - corrupt_f
    for p in range(clean_right_start, corrupt_right_start):
        jump.add(p)

    clean_right_end = ss2_end + clean_f
    corrupt_right_end = ss2_end + corrupt_f
    for p in range(corrupt_right_end, clean_right_end):
        jump.add(p)

    return jump


# ---------------------------------------------------------------------------
# Solvent accessibility (contact-number proxy from PDB)
# ---------------------------------------------------------------------------

def compute_solvent_accessibility(protein: str, seq_len: int) -> dict | None:
    """Compute a contact-number-based proxy for solvent accessibility.

    Uses CA-CA distances: count neighbors within 11A for each residue.
    Fewer neighbors = more exposed (higher accessibility estimate).
    Returns dict: 0-indexed seq pos -> relative_accessibility (0-1 scale),
    or None if PDB cannot be parsed."""
    try:
        from Bio.PDB import PDBParser
        import numpy as np
    except ImportError:
        print("WARNING: BioPython not available, skipping solvent accessibility", file=sys.stderr)
        return None

    pdb_path = DATA_DIR / f"{protein}_EV" / "TARGET_b0.3" / f"{protein.lower()[:4]}.pdb"
    if not pdb_path.exists():
        pdb_candidates = list((DATA_DIR / f"{protein}_EV" / "TARGET_b0.3").glob("*.pdb"))
        if not pdb_candidates:
            print(f"WARNING: No PDB file found for {protein}, skipping solvent accessibility", file=sys.stderr)
            return None
        pdb_path = pdb_candidates[0]

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(protein, str(pdb_path))
    model = structure[0]

    ca_coords = {}
    for chain in model:
        for residue in chain:
            if "CA" in residue:
                resid = residue.get_id()[1]
                ca_coords[resid] = residue["CA"].get_vector().get_array()

    if not ca_coords:
        print("WARNING: No CA atoms found in PDB", file=sys.stderr)
        return None

    pdb_residues = sorted(ca_coords.keys())
    coords = np.array([ca_coords[r] for r in pdb_residues])

    from scipy.spatial.distance import cdist
    dists = cdist(coords, coords)

    threshold = 11.0
    neighbor_counts = (dists < threshold).sum(axis=1) - 1

    max_neighbors = neighbor_counts.max() if len(neighbor_counts) > 0 else 1
    if max_neighbors == 0:
        max_neighbors = 1

    pdb_to_seq_offset = pdb_residues[0] - 1
    accessibility = {}
    for i, resid in enumerate(pdb_residues):
        seq_pos = resid - pdb_to_seq_offset - 1
        if 0 <= seq_pos < seq_len:
            rel_acc = 1.0 - (neighbor_counts[i] / max_neighbors)
            accessibility[seq_pos] = round(rel_acc, 3)

    return accessibility


# ---------------------------------------------------------------------------
# Region classification
# ---------------------------------------------------------------------------

def get_region(pos: int, config: dict) -> str:
    """Classify a position as ss1, ss2, flkL, flkR, or other."""
    pos1, pos2 = config["contact_pair"]
    radius = 5
    ss1_start, ss1_end = pos1 - radius, pos1 + radius + 1
    ss2_start, ss2_end = pos2 - radius, pos2 + radius + 1
    clean_f = config["clean_flank"]

    if ss1_start <= pos < ss1_end:
        return "ss1"
    if ss2_start <= pos < ss2_end:
        return "ss2"

    left_start = ss1_start - clean_f
    left_end = ss1_end + clean_f
    right_start = ss2_start - clean_f
    right_end = ss2_end + clean_f

    if left_start <= pos < ss1_start or ss1_end <= pos < left_end:
        return "flkL"
    if right_start <= pos < ss2_start or ss2_end <= pos < right_end:
        return "flkR"
    return "other"


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def format_heads(head_list: list[tuple]) -> str:
    """Format list of (layer, head, anchor_type, rank) as compact string."""
    if not head_list:
        return "-"
    parts = []
    for layer, head, atype, rank in sorted(head_list, key=lambda x: x[3]):
        short = atype.replace("-ANCHOR", "").lower()[:1]
        parts.append(f"L{layer}H{head}(r{rank},{short})")
    return ", ".join(parts)


def build_anchor_table(
    anchors: dict,
    sequence: str,
    conservation: dict,
    sse_str: str,
    sse_segments: list,
    jump_residues: set,
    config: dict,
    accessibility: dict | None,
) -> list[dict]:
    """Build the per-anchor-residue table."""
    rows = []
    for pos in sorted(anchors.keys()):
        info = anchors[pos]
        aa_seq = sequence[pos] if pos < len(sequence) else "?"
        aa_label = info["aa_from_label"] or "?"

        if aa_seq != aa_label:
            print(f"WARNING: position {pos} has AA mismatch: sequence={aa_seq}, label={aa_label}", file=sys.stderr)

        sse_type, sse_position, seg_len = get_sse_position_info(pos, sse_str, sse_segments)
        cons = conservation.get(pos, None)
        region = get_region(pos, config)
        is_jump = pos in jump_residues

        n_k = len(info["k_heads"])
        n_q = len(info["q_heads"])
        role = []
        if n_k > 0:
            role.append(f"K({n_k})")
        if n_q > 0:
            role.append(f"Q({n_q})")
        role_str = "+".join(role)

        row = {
            "pos": pos,
            "aa": aa_seq,
            "region": region,
            "role": role_str,
            "n_heads": n_k + n_q,
            "conservation": f"{cons:.3f}" if cons is not None else "N/A",
            "sse": sse_type,
            "sse_pos": sse_position,
            "seg_len": seg_len if seg_len > 0 else "",
            "jump": "YES" if is_jump else "",
            "k_heads": format_heads(info["k_heads"]),
            "q_heads": format_heads(info["q_heads"]),
        }
        if accessibility is not None:
            acc = accessibility.get(pos, None)
            row["rel_acc"] = f"{acc:.3f}" if acc is not None else "N/A"
        rows.append(row)
    return rows


def write_report(protein: str, rows: list[dict], config: dict, jump_residues: set, has_acc: bool):
    """Write markdown report."""
    out_dir = REPORT_DIR / protein
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"{protein}_anchor_interp.md"

    pos1, pos2 = config["contact_pair"]
    radius = 5

    with open(report_path, "w") as f:
        f.write(f"# Anchor Residue Interpretation: {protein}\n\n")

        f.write("## Configuration\n\n")
        f.write(f"| Parameter | Value |\n")
        f.write(f"| --- | --- |\n")
        f.write(f"| Protein | {protein} |\n")
        f.write(f"| Contact pair | ({pos1}, {pos2}) |\n")
        f.write(f"| ss1 | [{pos1 - radius}, {pos1 + radius + 1}) |\n")
        f.write(f"| ss2 | [{pos2 - radius}, {pos2 + radius + 1}) |\n")
        f.write(f"| Clean flank | {config['clean_flank']} |\n")
        f.write(f"| Corrupt flank | {config['corrupt_flank']} |\n")
        f.write(f"| Jump residues | {sorted(jump_residues)} |\n\n")

        f.write("## Anchor Residue Table\n\n")
        f.write("Each row is a residue that appears as an anchor (SINGLE/DUAL/MULTI) for at least one circuit head.\n")
        f.write("role: K(n) = key anchor for n heads, Q(n) = query anchor for n heads.\n\n")

        cols = ["pos", "aa", "region", "role", "n_heads", "conservation", "sse", "sse_pos", "seg_len", "jump"]
        if has_acc:
            cols.append("rel_acc")
        headers = {"pos": "pos", "aa": "AA", "region": "region", "role": "role", "n_heads": "n_heads", "conservation": "conservation", "sse": "SSE", "sse_pos": "SSE position", "seg_len": "seg_len", "jump": "jump?", "rel_acc": "rel_acc"}

        f.write("| " + " | ".join(headers[c] for c in cols) + " |\n")
        f.write("| " + " | ".join("---" for _ in cols) + " |\n")
        for row in rows:
            f.write("| " + " | ".join(str(row[c]) for c in cols) + " |\n")

        f.write("\n## Head Assignments per Anchor\n\n")
        for row in rows:
            f.write(f"### Position {row['pos']} ({row['aa']}) — {row['role']}\n\n")
            if row["k_heads"] != "-":
                f.write(f"K anchor for: {row['k_heads']}\n\n")
            if row["q_heads"] != "-":
                f.write(f"Q anchor for: {row['q_heads']}\n\n")

        f.write("## Summary Statistics\n\n")
        n_anchors = len(rows)
        n_jump = sum(1 for r in rows if r["jump"] == "YES")
        n_k_only = sum(1 for r in rows if "K" in r["role"] and "Q" not in r["role"])
        n_q_only = sum(1 for r in rows if "Q" in r["role"] and "K" not in r["role"])
        n_both = sum(1 for r in rows if "K" in r["role"] and "Q" in r["role"])

        sse_counts = defaultdict(int)
        for r in rows:
            sse_counts[r["sse"]] += 1
        region_counts = defaultdict(int)
        for r in rows:
            region_counts[r["region"]] += 1
        boundary_counts = defaultdict(int)
        for r in rows:
            boundary_counts[r["sse_pos"]] += 1

        cons_vals = [float(r["conservation"]) for r in rows if r["conservation"] != "N/A"]

        f.write(f"| Statistic | Value |\n")
        f.write(f"| --- | --- |\n")
        f.write(f"| Total anchor residues | {n_anchors} |\n")
        f.write(f"| K-only anchors | {n_k_only} |\n")
        f.write(f"| Q-only anchors | {n_q_only} |\n")
        f.write(f"| Both K and Q | {n_both} |\n")
        f.write(f"| Jump residues among anchors | {n_jump} |\n")
        f.write(f"| SSE breakdown | H={sse_counts.get('H', 0)}, E={sse_counts.get('E', 0)}, C={sse_counts.get('C', 0)} |\n")
        f.write(f"| Region breakdown | {', '.join(f'{k}={v}' for k, v in sorted(region_counts.items()))} |\n")
        f.write(f"| SSE position | {', '.join(f'{k}={v}' for k, v in sorted(boundary_counts.items()) if k != '-')} |\n")
        if cons_vals:
            f.write(f"| Conservation (mean) | {sum(cons_vals)/len(cons_vals):.3f} |\n")
            f.write(f"| Conservation (range) | [{min(cons_vals):.3f}, {max(cons_vals):.3f}] |\n")

    print(f"Report written to {report_path}")
    return report_path


def write_csv(protein: str, rows: list[dict], has_acc: bool):
    """Write CSV output."""
    out_dir = REPORT_DIR / protein
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / f"{protein}_anchor_interp.csv"

    cols = ["pos", "aa", "region", "role", "n_heads", "conservation", "sse", "sse_pos", "seg_len", "jump", "k_heads", "q_heads"]
    if has_acc:
        cols.append("rel_acc")

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV written to {csv_path}")


# ---------------------------------------------------------------------------
# Coupling analysis: flank anchors vs non-anchors
# ---------------------------------------------------------------------------

def get_flank_positions(config: dict, seq_len: int) -> set[int]:
    """Return all flank positions (inside unmasked region, outside SS1/SS2)."""
    pos1, pos2 = config["contact_pair"]
    radius = 5
    clean_f = config["clean_flank"]

    ss1_start, ss1_end = pos1 - radius, pos1 + radius + 1
    ss2_start, ss2_end = pos2 - radius, pos2 + radius + 1

    left_start = max(0, ss1_start - clean_f)
    left_end = min(seq_len, ss1_end + clean_f)
    right_start = max(0, ss2_start - clean_f)
    right_end = min(seq_len, ss2_end + clean_f)

    flank = set()
    for p in range(left_start, ss1_start):
        flank.add(p)
    for p in range(ss1_end, left_end):
        flank.add(p)
    for p in range(right_start, ss2_start):
        flank.add(p)
    for p in range(ss2_end, right_end):
        flank.add(p)
    return flank


def run_coupling_analysis(protein: str, config: dict, anchors: dict, couplings: dict, seq_len: int):
    """Compare coupling-to-contact scores for flank anchor vs non-anchor residues."""
    from scipy.stats import mannwhitneyu

    pos1, pos2 = config["contact_pair"]
    flank_positions = get_flank_positions(config, seq_len)
    flank_anchor_pos = {p for p in anchors if p in flank_positions}
    flank_nonanchor_pos = flank_positions - flank_anchor_pos

    def max_coupling_to_contact(pos):
        scores = []
        for cp in [pos1, pos2]:
            s = couplings.get((pos, cp), None)
            if s is not None:
                scores.append(s)
        return max(scores) if scores else None

    anchor_scores = []
    nonanchor_scores = []
    anchor_details = []

    for p in sorted(flank_anchor_pos):
        s = max_coupling_to_contact(p)
        if s is not None:
            anchor_scores.append(s)
            n_heads = len(anchors[p]["k_heads"]) + len(anchors[p]["q_heads"])
            anchor_details.append((p, s, n_heads))

    for p in sorted(flank_nonanchor_pos):
        s = max_coupling_to_contact(p)
        if s is not None:
            nonanchor_scores.append(s)

    all_flank_scores = sorted(anchor_scores + nonanchor_scores, reverse=True)
    n_total = len(all_flank_scores)
    q75_threshold = all_flank_scores[n_total // 4] if n_total >= 4 else 0

    n_anchor_top_q = sum(1 for s in anchor_scores if s >= q75_threshold)

    print(f"\n=== Coupling Analysis (flank only) ===")
    print(f"Contact pair (0-indexed): ({pos1}, {pos2})")
    print(f"Flank residues: {len(flank_positions)} total, {len(flank_anchor_pos)} anchor, {len(flank_nonanchor_pos)} non-anchor")

    if anchor_scores:
        print(f"Anchor coupling scores:     mean={sum(anchor_scores)/len(anchor_scores):.2f}, median={sorted(anchor_scores)[len(anchor_scores)//2]:.2f}, range=[{min(anchor_scores):.2f}, {max(anchor_scores):.2f}]")
    if nonanchor_scores:
        print(f"Non-anchor coupling scores: mean={sum(nonanchor_scores)/len(nonanchor_scores):.2f}, median={sorted(nonanchor_scores)[len(nonanchor_scores)//2]:.2f}, range=[{min(nonanchor_scores):.2f}, {max(nonanchor_scores):.2f}]")

    print(f"Top quartile threshold: {q75_threshold:.2f}")
    print(f"Anchors in top quartile: {n_anchor_top_q}/{len(anchor_scores)}")

    if len(anchor_scores) >= 2 and len(nonanchor_scores) >= 2:
        stat, pval = mannwhitneyu(anchor_scores, nonanchor_scores, alternative="greater")
        print(f"Mann-Whitney U (anchor > non-anchor): U={stat:.1f}, p={pval:.4f}")
    else:
        pval = None
        print("Too few samples for statistical test")

    print(f"\nFlank anchor details (sorted by coupling):")
    print(f"{'pos':>4} {'n_heads':>7} {'coupling':>8} {'top_q?':>6}")
    print("-" * 30)
    for p, s, nh in sorted(anchor_details, key=lambda x: -x[1]):
        tq = "YES" if s >= q75_threshold else ""
        print(f"{p:>4} {nh:>7} {s:>8.2f} {tq:>6}")

    out_dir = REPORT_DIR / protein
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"{protein}_anchor_interp.md"
    with open(report_path, "a") as f:
        f.write(f"\n## Coupling Analysis (flank anchors vs non-anchors)\n\n")
        f.write(f"Hypothesis: flank anchor residues have higher evolutionary coupling scores with the contact pair residues than non-anchor flank residues.\n\n")
        f.write(f"| Parameter | Value |\n")
        f.write(f"| --- | --- |\n")
        f.write(f"| Contact pair (0-indexed) | ({pos1}, {pos2}) |\n")
        f.write(f"| Total flank residues | {len(flank_positions)} |\n")
        f.write(f"| Flank anchors | {len(flank_anchor_pos)} |\n")
        f.write(f"| Flank non-anchors | {len(flank_nonanchor_pos)} |\n")
        if anchor_scores:
            f.write(f"| Anchor coupling (mean) | {sum(anchor_scores)/len(anchor_scores):.2f} |\n")
        if nonanchor_scores:
            f.write(f"| Non-anchor coupling (mean) | {sum(nonanchor_scores)/len(nonanchor_scores):.2f} |\n")
        f.write(f"| Top quartile threshold | {q75_threshold:.2f} |\n")
        f.write(f"| Anchors in top quartile | {n_anchor_top_q}/{len(anchor_scores)} |\n")
        if pval is not None:
            f.write(f"| Mann-Whitney U p-value (anchor > non-anchor) | {pval:.4f} |\n")
        f.write(f"\n### Flank Anchor Coupling Details\n\n")
        f.write(f"| pos | AA | n_heads | max_coupling_to_contact | top quartile? |\n")
        f.write(f"| --- | --- | --- | --- | --- |\n")
        for p, s, nh in sorted(anchor_details, key=lambda x: -x[1]):
            aa = anchors[p]["aa_from_label"] or "?"
            tq = "YES" if s >= q75_threshold else ""
            f.write(f"| {p} | {aa} | {nh} | {s:.2f} | {tq} |\n")

    print(f"\nCoupling analysis appended to {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Anchor residue interpretation")
    parser.add_argument("--protein", required=True, help="Protein ID (e.g., 2B61A)")
    parser.add_argument("--no-solvent", action="store_true", help="Skip solvent accessibility computation")
    args = parser.parse_args()

    protein = args.protein
    print(f"=== Anchor Interpretation: {protein} ===\n")

    config = load_protein_config(protein)
    sequence = load_sequence(protein)
    sse_str = load_sse(protein)
    conservation = load_conservation(protein)
    summary_rows = load_summary_csv(protein)

    print(f"Sequence length: {len(sequence)}")
    print(f"SSE string length: {len(sse_str)}")
    print(f"Conservation entries: {len(conservation)}")
    print(f"Circuit heads in summary: {len(summary_rows)}")

    if len(sequence) != len(sse_str):
        print(f"WARNING: sequence/SSE length mismatch ({len(sequence)} vs {len(sse_str)})", file=sys.stderr)
    if len(sequence) != len(conservation):
        print(f"WARNING: sequence/conservation length mismatch ({len(sequence)} vs {len(conservation)})", file=sys.stderr)

    anchors = extract_anchors(summary_rows)
    print(f"Unique anchor residues: {len(anchors)}")

    sse_segments = compute_sse_segments(sse_str)
    jump_residues = get_jump_residues(config)
    print(f"Jump residues: {sorted(jump_residues)}")

    accessibility = None
    if not args.no_solvent:
        print("\nComputing solvent accessibility from PDB...")
        accessibility = compute_solvent_accessibility(protein, len(sequence))
        if accessibility is not None:
            print(f"Accessibility computed for {len(accessibility)} residues")
        else:
            print("Solvent accessibility not available")

    has_acc = accessibility is not None

    rows = build_anchor_table(anchors, sequence, conservation, sse_str, sse_segments, jump_residues, config, accessibility)

    print()
    print(f"{'pos':>4} {'AA':>2} {'region':>6} {'role':>10} {'cons':>6} {'SSE':>3} {'SSE_pos':>9} {'segL':>4} {'jump':>4}", end="")
    if has_acc:
        print(f" {'rel_acc':>7}", end="")
    print()
    print("-" * (55 + (8 if has_acc else 0)))
    for r in rows:
        seg_str = str(r['seg_len']) if r['seg_len'] else "-"
        print(f"{r['pos']:>4} {r['aa']:>2} {r['region']:>6} {r['role']:>10} {r['conservation']:>6} {r['sse']:>3} {r['sse_pos']:>9} {seg_str:>4} {r['jump']:>4}", end="")
        if has_acc:
            print(f" {r.get('rel_acc', 'N/A'):>7}", end="")
        print()

    write_report(protein, rows, config, jump_residues, has_acc)
    write_csv(protein, rows, has_acc)

    # Coupling analysis
    couplings = load_couplings(protein)
    if couplings:
        print(f"\nCoupling pairs loaded: {len(couplings) // 2}")
        run_coupling_analysis(protein, config, anchors, couplings, len(sequence))
    else:
        print("\nNo coupling data available, skipping coupling analysis")


if __name__ == "__main__":
    main()
