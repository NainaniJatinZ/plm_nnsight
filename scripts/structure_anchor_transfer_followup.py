#!/usr/bin/env python3
"""Follow-up checks on anchor transfer results.

1. Local sequence identity around the anchor column — is the region conserved
   even though global identity is low?
2. What's happening at column 493 (3cwv-assembly2's anchor) — do other proteins
   have high projection scores there too?
3. Top-5 projection score columns for each protein — are there secondary peaks?
"""

import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.structure_anchor_transfer import (
    parse_fasta_alignment, build_alignment_mappings, compute_pairwise_identity,
    extract_pdb_id, load_model, extract_head_weights, compute_search_dir_from_full_seq,
    analyze_protein, FOLDMASON_DIR, DATA_DIR, WEIGHTS_DIR,
    TARGET_LAYER, TARGET_HEAD, REFERENCE_PROTEIN,
)


def local_identity_around_column(aligned_seqs, names, center_col, window):
    """For each pair of proteins, compute sequence identity in [center_col - window, center_col + window]."""
    results = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a = aligned_seqs[names[i]]
            b = aligned_seqs[names[j]]
            aligned_count = 0
            match_count = 0
            for col in range(max(0, center_col - window), min(len(a), center_col + window + 1)):
                ca, cb = a[col], b[col]
                if ca != "-" and cb != "-":
                    aligned_count += 1
                    if ca == cb:
                        match_count += 1
            ident = match_count / max(aligned_count, 1)
            results[(names[i], names[j])] = (ident, aligned_count, match_count)
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    # Parse alignment
    aligned_seqs = parse_fasta_alignment(FOLDMASON_DIR / "foldmason_aa.fa")
    names = list(aligned_seqs.keys())
    ungapped_seqs, col_to_pos, pos_to_col = build_alignment_mappings(aligned_seqs)

    pvg_name = [n for n in names if n.startswith("1pvg")][0]
    anchor_col = 98  # from the main experiment

    # ===================================================================
    # Check 1: Local sequence identity around anchor column
    # ===================================================================
    print("=" * 60)
    print("Check 1: Local vs global sequence identity around anchor col 98")
    print("=" * 60)

    global_idents = compute_pairwise_identity(ungapped_seqs, aligned_seqs)

    # Show the actual residues at and around column 98
    print("\nResidues at alignment columns 88-108 (anchor col = 98):")
    print(f"{'Protein':<30}", end="")
    for col in range(88, 109):
        marker = "*" if col == 98 else " "
        print(f"{col:>4}{marker}", end="")
    print()
    for n in names:
        pdb = extract_pdb_id(n)
        print(f"{pdb + ' ' + n.split('-')[1][:8]:<30}", end="")
        a = aligned_seqs[n]
        for col in range(88, 109):
            print(f"  {a[col]:>2} ", end="")
        print()

    print("\n\nLocal identity (window=5, 10, 20) vs global, pairs involving 1pvg:")
    print(f"{'Pair':<25} {'Global':>8} {'W=5':>8} {'W=10':>8} {'W=20':>8}  W=5 detail")
    for n in names:
        if n == pvg_name:
            continue
        pdb = extract_pdb_id(n)
        glob = global_idents.get((pvg_name, n), 0.0)
        loc5 = local_identity_around_column(aligned_seqs, [pvg_name, n], anchor_col, 5)
        loc10 = local_identity_around_column(aligned_seqs, [pvg_name, n], anchor_col, 10)
        loc20 = local_identity_around_column(aligned_seqs, [pvg_name, n], anchor_col, 20)
        key = (pvg_name, n)
        id5, aln5, match5 = loc5[key]
        id10, _, _ = loc10[key]
        id20, _, _ = loc20[key]
        print(f"1pvg vs {pdb:<15} {glob:>7.1%} {id5:>7.1%} {id10:>7.1%} {id20:>7.1%}  ({match5}/{aln5} matches)")

    # Also check all non-duplicate pairs
    print("\n\nLocal identity (window=5) for all unique protein pairs:")
    # Deduplicate: pick one representative per cluster
    representatives = [pvg_name, "1ei1-assembly1cifgz", "1mx0-assembly1cifgz", "7cmp-assembly2cifgz",
                       "3zkb-assembly8cifgz", "3cwv-assembly1cifgz", "1b62-assembly1cifgz"]
    reps_in_data = [n for n in representatives if n in names]
    print(f"{'Pair':<35} {'Global':>8} {'Local W=5':>10}  Detail")
    for i in range(len(reps_in_data)):
        for j in range(i + 1, len(reps_in_data)):
            na, nb = reps_in_data[i], reps_in_data[j]
            glob = global_idents.get((na, nb), 0.0)
            loc = local_identity_around_column(aligned_seqs, [na, nb], anchor_col, 5)
            ident, aln_ct, match_ct = loc[(na, nb)]
            print(f"{extract_pdb_id(na)} vs {extract_pdb_id(nb):<20} {glob:>7.1%} {ident:>9.1%}  ({match_ct}/{aln_ct})")

    # ===================================================================
    # Check 2: What's at column 493? Projection scores for all proteins
    # ===================================================================
    print("\n" + "=" * 60)
    print("Check 2: Column 493 (3cwv-assembly2 anchor) — projection scores")
    print("=" * 60)

    # We need to run the model to get projection scores
    print("\nLoading model...")
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)

    with open(DATA_DIR / "full_seq_dict.json") as f:
        all_seqs = json.load(f)
    ref_seq = all_seqs[REFERENCE_PROTEIN]
    d_ref = compute_search_dir_from_full_seq(model, tokenizer, ref_seq, weights, args.device)
    d_ref_unit = (d_ref / d_ref.norm().clamp(min=1e-8)).to(args.device)

    print("\nAnalyzing proteins...")
    results = {}
    for n in names:
        seq = ungapped_seqs[n]
        r = analyze_protein(model, tokenizer, n, seq, d_ref_unit, weights, args.device)
        if r is not None:
            results[n] = r

    # For each protein, what's the projection score at the residue corresponding to col 493?
    print("\nProjection score at alignment column 493 (3cwv-asm2 anchor):")
    print(f"{'Protein':<30} {'Residue at col493':>20} {'Proj score':>12} {'Proj rank':>12} {'n_res':>8}")
    col_target = 493
    for n in names:
        r = results[n]
        proj = r["proj_scores"]
        if col_target < len(col_to_pos[n]):
            seq_pos = col_to_pos[n][col_target]
            if seq_pos != -1 and seq_pos < len(proj):
                proj_rank = int(np.argsort(np.argsort(-proj))[seq_pos])
                aa = ungapped_seqs[n][seq_pos]
                print(f"{extract_pdb_id(n) + ' ' + n.split('-')[1][:8]:<30} pos={seq_pos:>3} AA={aa}        {proj[seq_pos]:>10.4f} {proj_rank:>10}/{r['n_res']}")
            else:
                print(f"{extract_pdb_id(n) + ' ' + n.split('-')[1][:8]:<30} {'GAP at col 493':>20}")
        else:
            print(f"{extract_pdb_id(n) + ' ' + n.split('-')[1][:8]:<30} {'col 493 out of range':>20}")

    # ===================================================================
    # Check 3: Top-5 projection score positions for each protein, mapped to aln cols
    # ===================================================================
    print("\n" + "=" * 60)
    print("Check 3: Top-5 projection score positions -> alignment columns")
    print("=" * 60)
    print(f"\n{'Protein':<25} {'Top-1 (pos->col)':>20} {'Top-2':>20} {'Top-3':>20} {'Top-4':>20} {'Top-5':>20}")
    for n in names:
        r = results[n]
        proj = r["proj_scores"]
        top5_idx = np.argsort(-proj)[:5]
        parts = []
        for idx in top5_idx:
            col = pos_to_col[n][idx] if idx < len(pos_to_col[n]) else -1
            aa = ungapped_seqs[n][idx]
            parts.append(f"{idx}({aa})->c{col}")
        pdb = extract_pdb_id(n)
        print(f"{pdb + ' ' + n.split('-')[1][:8]:<25} ", "  ".join(f"{p:>18}" for p in parts))

    # ===================================================================
    # Check 4: Residues at columns 88-108, showing the actual amino acids
    # for the anchor flanking region — is there a conserved motif?
    # ===================================================================
    print("\n" + "=" * 60)
    print("Check 4: Amino acid conservation at anchor column 98 +/- 5")
    print("=" * 60)
    for col in range(93, 104):
        residues = []
        for n in names:
            a = aligned_seqs[n]
            if a[col] != "-":
                residues.append(a[col])
        if residues:
            unique = set(residues)
            conservation = max(residues.count(r) for r in unique) / len(residues)
            most_common = max(unique, key=residues.count)
            print(f"  Col {col}: {' '.join(residues):<50} most_common={most_common} conservation={conservation:.0%} ({'ANCHOR' if col == 98 else ''})")


if __name__ == "__main__":
    main()
