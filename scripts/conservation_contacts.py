"""
Experiment: do ESM2 contact predictions struggle more on conserved residue pairs?

Steps:
  1. Extract ground-truth contacts from PDB (CB-CB < 8 Å, |i-j| >= 6)
  2. Get ESM2 contact predictions on the full 2B61A sequence
  3. Bin contact pairs by conservation and compare prediction accuracy
"""

# %%  Imports
import json
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from Bio.PDB import PDBParser, is_aa
from transformers import EsmForMaskedLM, EsmTokenizer

# %%  Paths
PDB_PATH = "data/TARGET_b0.3/2b61.pdb"
FREQ_CSV = "data/TARGET_b0.3/align/TARGET_b0.3_frequencies.csv"
SEQ_JSON = "data/full_seq_dict.json"
CHAIN_ID = "A"
CUTOFF = 8.0
MIN_SEQ_SEP = 6

# %%  1.  Ground-truth contacts from PDB

AA3TO1 = {
    "ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F",
    "GLY": "G", "HIS": "H", "ILE": "I", "LYS": "K", "LEU": "L",
    "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R",
    "SER": "S", "THR": "T", "VAL": "V", "TRP": "W", "TYR": "Y",
}

parser = PDBParser(QUIET=True)
structure = parser.get_structure("2b61", PDB_PATH)

pdb_coords = []
pdb_resnums = []
pdb_seq = []

for model in structure:
    for chain in model:
        if chain.id != CHAIN_ID:
            continue
        for res in chain:
            if not is_aa(res, standard=True):
                continue
            resname = res.get_resname()
            atom_name = "CA" if resname == "GLY" else "CB"
            if atom_name not in res:
                continue
            pdb_coords.append(res[atom_name].get_coord())
            pdb_resnums.append(res.id[1])
            pdb_seq.append(AA3TO1[resname])
    break

pdb_coords = np.array(pdb_coords)
n_pdb = len(pdb_coords)
print(f"PDB chain {CHAIN_ID}: {n_pdb} residues, resnums {pdb_resnums[0]}-{pdb_resnums[-1]}")

# Pairwise distances and contacts
diff = pdb_coords[:, None, :] - pdb_coords[None, :, :]
distances = np.sqrt(np.sum(diff * diff, axis=-1))
gt_contacts = (distances <= CUTOFF).astype(np.uint8)
np.fill_diagonal(gt_contacts, 0)
for i in range(n_pdb):
    for j in range(n_pdb):
        if abs(i - j) < MIN_SEQ_SEP:
            gt_contacts[i, j] = 0

n_gt_pairs = gt_contacts.sum() // 2
print(f"Ground-truth contacts (CB-CB <= {CUTOFF} Å, |i-j| >= {MIN_SEQ_SEP}): {n_gt_pairs}")

# %%  2.  Map PDB residues to full-sequence positions

with open(SEQ_JSON) as f:
    full_seq = json.load(f)["2B61A"]

# Verify alignment: PDB sequence should appear in full_seq
pdb_seq_str = "".join(pdb_seq)

# Find start: first 10 chars of PDB seq in full seq
match_idx = full_seq.find(pdb_seq_str[:10])
if match_idx < 0:
    raise ValueError("Could not find PDB sequence start in full sequence")

# Greedy forward match: for each PDB residue, find the next matching
# character in full_seq. This handles insertions in full_seq (residues
# disordered in PDB) and single-residue mismatches gracefully.
pdb_to_fullseq = {}
full_pos = match_idx
mismatches = 0
for pdb_idx in range(n_pdb):
    # Look ahead up to 5 positions for a match
    found = False
    for offset in range(5):
        if full_pos + offset < len(full_seq) and full_seq[full_pos + offset] == pdb_seq[pdb_idx]:
            pdb_to_fullseq[pdb_idx] = full_pos + offset
            full_pos = full_pos + offset + 1
            found = True
            break
    if not found:
        # Accept a mismatch at current position (mutation between construct and crystal)
        pdb_to_fullseq[pdb_idx] = full_pos
        mismatches += 1
        full_pos += 1

if mismatches > 0:
    print(f"Warning: {mismatches} mismatches during PDB-to-sequence alignment")

print(f"Mapped {len(pdb_to_fullseq)} PDB residues to full-seq positions")
print(f"Full-seq range: {pdb_to_fullseq[0]}-{pdb_to_fullseq[n_pdb-1]}")

# %%  3.  Load conservation scores

freq_df = pd.read_csv(FREQ_CSV)
# freq_df column "i" is 1-indexed into full_seq
# conservation column has the score
conservation = freq_df["conservation"].values  # length 377, indexed 0..376
# freq_df row 0 = position 1 (1-indexed) = full_seq[0]
# So conservation[k] = conservation of full_seq[k]

print(f"Conservation scores: {len(conservation)} positions")
print(f"Range: [{conservation.min():.3f}, {conservation.max():.3f}], mean={conservation.mean():.3f}")

# Map conservation to PDB residues
pdb_conservation = np.array([conservation[pdb_to_fullseq[i]] for i in range(n_pdb)])

# %%  4.  ESM2 contact predictions on full sequence

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "facebook/esm2_t33_650M_UR50D"
print(f"\nLoading ESM2 model on {device}...")
tokenizer = EsmTokenizer.from_pretrained(model_name)
esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device).eval()

inputs = tokenizer(full_seq, return_tensors="pt").to(device)
with torch.no_grad():
    pred_contacts_AA = esm_model.predict_contacts(
        inputs["input_ids"], inputs["attention_mask"]
    )[0].cpu().numpy()

print(f"Predicted contact map shape: {pred_contacts_AA.shape}")
# pred_contacts_AA is (L_aa, L_aa) where L_aa = len(full_seq) = 377

# %%  5.  Extract predictions for PDB contact pairs and analyze

# Build predicted contact sub-matrix for PDB residues
# For each PDB pair (i,j), get predicted contact score at full-seq positions
pred_for_pdb = np.zeros((n_pdb, n_pdb))
for i in range(n_pdb):
    for j in range(n_pdb):
        fi, fj = pdb_to_fullseq[i], pdb_to_fullseq[j]
        pred_for_pdb[i, j] = pred_contacts_AA[fi, fj]

# Evaluate: for each pair, record ground truth, prediction, and conservation
rows = []
for i in range(n_pdb):
    for j in range(i + MIN_SEQ_SEP, n_pdb):
        gt = gt_contacts[i, j]
        pred_score = pred_for_pdb[i, j]
        cons_i = pdb_conservation[i]
        cons_j = pdb_conservation[j]
        pair_cons = min(cons_i, cons_j)  # conservation of less-conserved partner
        mean_cons = (cons_i + cons_j) / 2
        rows.append({
            "i": i, "j": j,
            "pdb_resnum_i": pdb_resnums[i], "pdb_resnum_j": pdb_resnums[j],
            "gt_contact": gt,
            "pred_score": pred_score,
            "cons_i": cons_i, "cons_j": cons_j,
            "pair_cons_min": pair_cons,
            "pair_cons_mean": mean_cons,
        })

df = pd.DataFrame(rows)
print(f"\nTotal pairs (|i-j| >= {MIN_SEQ_SEP}): {len(df)}")
print(f"Ground-truth contacts: {df['gt_contact'].sum()}")
print(f"Non-contacts: {(df['gt_contact'] == 0).sum()}")

# %%  5b. Save computed data for plotting
df.to_csv("reports/cache/2B61A/conservation_pairs.csv", index=False)
print(f"Saved pair data to reports/cache/2B61A/conservation_pairs.csv")

# %%  6.  Bin by conservation and compute precision/recall

# Use mean conservation of the pair
n_bins = 5
df["cons_bin"] = pd.qcut(df["pair_cons_mean"], q=n_bins, duplicates="drop")

# For each bin, compute:
# - number of true contacts
# - mean predicted score for true contacts vs non-contacts
# - precision at top-L (standard metric: pick top L predictions, count how many are true contacts)

print("\n=== Per-bin analysis (bins by mean pair conservation) ===\n")
bin_stats = []
for bin_label, grp in df.groupby("cons_bin", observed=True):
    n_total = len(grp)
    n_true = grp["gt_contact"].sum()
    n_neg = n_total - n_true
    mean_pred_pos = grp.loc[grp["gt_contact"] == 1, "pred_score"].mean() if n_true > 0 else float("nan")
    mean_pred_neg = grp.loc[grp["gt_contact"] == 0, "pred_score"].mean() if n_neg > 0 else float("nan")

    # Precision at top-K where K = number of true contacts in this bin
    if n_true > 0:
        top_k = grp.nlargest(int(n_true), "pred_score")
        precision_at_k = top_k["gt_contact"].mean()
    else:
        precision_at_k = float("nan")

    bin_stats.append({
        "bin": str(bin_label),
        "n_pairs": n_total,
        "n_contacts": int(n_true),
        "mean_pred_contacts": mean_pred_pos,
        "mean_pred_noncontacts": mean_pred_neg,
        "precision_at_K": precision_at_k,
    })
    print(f"Bin {bin_label}:")
    print(f"  pairs={n_total}, contacts={n_true}")
    print(f"  mean pred (contacts)={mean_pred_pos:.4f}, (non-contacts)={mean_pred_neg:.4f}")
    print(f"  precision@K={precision_at_k:.4f}")
    print()

# %%  7.  Overall metrics

# Top-L precision (standard ESM benchmark metric)
L = len(full_seq)
n_structured = n_pdb
# Use top-L/5 long-range contacts
for divisor, label in [(1, "L"), (2, "L/2"), (5, "L/5")]:
    k = n_structured // divisor
    top_k_global = df.nlargest(k, "pred_score")
    prec = top_k_global["gt_contact"].mean()
    print(f"Precision @ top {label} ({k}): {prec:.4f}")

# %%  8.  Visualization

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 8a: Conservation distribution of true contacts vs non-contacts
ax = axes[0]
ax.hist(df.loc[df["gt_contact"] == 1, "pair_cons_mean"], bins=30, alpha=0.6, label="True contacts", density=True)
ax.hist(df.loc[df["gt_contact"] == 0, "pair_cons_mean"], bins=30, alpha=0.6, label="Non-contacts", density=True)
ax.set_xlabel("Mean pair conservation")
ax.set_ylabel("Density")
ax.set_title("Conservation distribution: contacts vs non-contacts")
ax.legend()

# 8b: Precision@K by conservation bin
ax = axes[1]
stats_df = pd.DataFrame(bin_stats)
x_labels = [s["bin"] for s in bin_stats]
x_pos = range(len(x_labels))
ax.bar(x_pos, [s["precision_at_K"] for s in bin_stats], color="steelblue")
ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Precision @ K")
ax.set_title("Contact prediction precision by conservation bin")
ax.set_ylim(0, 1)

# 8c: Mean predicted score for contacts by conservation bin
ax = axes[2]
ax.bar(x_pos, [s["mean_pred_contacts"] for s in bin_stats], color="coral")
ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, rotation=45, ha="right", fontsize=8)
ax.set_ylabel("Mean predicted contact score")
ax.set_title("Mean ESM2 contact score (true contacts) by conservation bin")

plt.tight_layout()
plt.savefig("reports/outputs/2B61A/2B61A_conservation_contacts.png", dpi=150)
print("\nSaved figure to reports/outputs/2B61A/2B61A_conservation_contacts.png")

# %%  9.  Correlation analysis

from scipy import stats as sp_stats

# Among true contacts only: correlation between conservation and predicted score
contacts_only = df[df["gt_contact"] == 1]
r_min, p_min = sp_stats.pearsonr(contacts_only["pair_cons_min"], contacts_only["pred_score"])
r_mean, p_mean = sp_stats.pearsonr(contacts_only["pair_cons_mean"], contacts_only["pred_score"])

print(f"\nCorrelation (true contacts only):")
print(f"  pred_score vs pair_cons_min:  r={r_min:.4f}, p={p_min:.2e}")
print(f"  pred_score vs pair_cons_mean: r={r_mean:.4f}, p={p_mean:.2e}")

# Among all pairs: does conservation predict whether ESM gets it right?
# Define "correct" as: contact predicted in top-K, or non-contact not in top-K
k_global = n_pdb  # top-L
threshold = df["pred_score"].nlargest(k_global).iloc[-1]
df["pred_contact"] = (df["pred_score"] >= threshold).astype(int)
df["correct"] = (df["pred_contact"] == df["gt_contact"]).astype(int)

# Among true contacts: is high conservation associated with more errors?
contacts_correct = contacts_only.merge(df[["i", "j", "correct"]], on=["i", "j"])
for cons_col in ["pair_cons_min", "pair_cons_mean"]:
    correct_cons = contacts_correct.loc[contacts_correct["correct"] == 1, cons_col].mean()
    incorrect_cons = contacts_correct.loc[contacts_correct["correct"] == 0, cons_col].mean()
    print(f"\n  {cons_col}:")
    print(f"    correctly predicted contacts: mean conservation = {correct_cons:.4f}")
    print(f"    missed contacts:              mean conservation = {incorrect_cons:.4f}")

# %%  10.  EVcouplings comparison

import os
from scipy import stats as sp_stats2

ev_long = "data/TARGET_b0.3/couplings/TARGET_b0.3_CouplingScores_longrange.csv"
if not os.path.exists(ev_long):
    print("EVcouplings file not found, skipping.")
else:
    ev_df = pd.read_csv(ev_long)
    # EVcouplings positions are 1-indexed into full_seq (same as freq_df)
    # Build fullseq_to_pdb mapping (inverse of pdb_to_fullseq)
    fullseq_to_pdb = {v: k for k, v in pdb_to_fullseq.items()}

    # Merge EV scores into main df
    # EV positions are 1-indexed; our df uses pdb_index pairs
    ev_rows = []
    for _, row in ev_df.iterrows():
        fi = int(row["i"]) - 1  # convert to 0-indexed full_seq position
        fj = int(row["j"]) - 1
        if fi in fullseq_to_pdb and fj in fullseq_to_pdb:
            pi = fullseq_to_pdb[fi]
            pj = fullseq_to_pdb[fj]
            if pi > pj:
                pi, pj = pj, pi
            if pj - pi >= MIN_SEQ_SEP:
                ev_rows.append({"i": pi, "j": pj, "ev_score": row["score"], "ev_cn": row["cn"]})

    ev_pair_df = pd.DataFrame(ev_rows).drop_duplicates(subset=["i", "j"])
    df2 = df.merge(ev_pair_df, on=["i", "j"], how="inner")
    df2.to_csv("reports/cache/2B61A/conservation_pairs_with_ev.csv", index=False)
    print(f"\n=== EVcouplings analysis ===")
    print(f"Pairs with both ESM and EV scores: {len(df2)}")
    print(f"True contacts in overlap: {df2['gt_contact'].sum()}")

    # Overall EV precision
    for divisor, label in [(1, "L"), (2, "L/2"), (5, "L/5")]:
        k = n_pdb // divisor
        top_k_ev = df2.nlargest(k, "ev_score")
        prec = top_k_ev["gt_contact"].mean()
        print(f"EV Precision @ top {label} ({k}): {prec:.4f}")

    # Per-bin analysis for EV
    df2["cons_bin"] = pd.qcut(df2["pair_cons_mean"], q=n_bins, duplicates="drop")

    print(f"\n=== EV per-bin analysis (bins by mean pair conservation) ===\n")
    ev_bin_stats = []
    for bin_label, grp in df2.groupby("cons_bin", observed=True):
        n_total = len(grp)
        n_true = grp["gt_contact"].sum()
        n_neg = n_total - n_true
        mean_ev_pos = grp.loc[grp["gt_contact"] == 1, "ev_score"].mean() if n_true > 0 else float("nan")
        mean_ev_neg = grp.loc[grp["gt_contact"] == 0, "ev_score"].mean() if n_neg > 0 else float("nan")
        mean_esm_pos = grp.loc[grp["gt_contact"] == 1, "pred_score"].mean() if n_true > 0 else float("nan")

        if n_true > 0:
            top_k = grp.nlargest(int(n_true), "ev_score")
            ev_prec = top_k["gt_contact"].mean()
            top_k_esm = grp.nlargest(int(n_true), "pred_score")
            esm_prec = top_k_esm["gt_contact"].mean()
        else:
            ev_prec = float("nan")
            esm_prec = float("nan")

        ev_bin_stats.append({
            "bin": str(bin_label),
            "n_pairs": n_total,
            "n_contacts": int(n_true),
            "ev_mean_score_contacts": mean_ev_pos,
            "ev_mean_score_noncontacts": mean_ev_neg,
            "ev_precision_at_K": ev_prec,
            "esm_precision_at_K": esm_prec,
            "esm_mean_score_contacts": mean_esm_pos,
        })
        print(f"Bin {bin_label}:")
        print(f"  pairs={n_total}, contacts={n_true}")
        print(f"  EV:  mean score (contacts)={mean_ev_pos:.4f}, (non-contacts)={mean_ev_neg:.4f}, precision@K={ev_prec:.4f}")
        print(f"  ESM: mean score (contacts)={mean_esm_pos:.4f}, precision@K={esm_prec:.4f}")
        print()

    # Correlation: EV score vs conservation among true contacts
    ev_contacts = df2[df2["gt_contact"] == 1]
    if len(ev_contacts) > 10:
        r_ev, p_ev = sp_stats2.pearsonr(ev_contacts["pair_cons_mean"], ev_contacts["ev_score"])
        r_esm, p_esm = sp_stats2.pearsonr(ev_contacts["pair_cons_mean"], ev_contacts["pred_score"])
        print(f"Correlation with conservation (true contacts only):")
        print(f"  EV score  vs pair_cons_mean: r={r_ev:.4f}, p={p_ev:.2e}")
        print(f"  ESM score vs pair_cons_mean: r={r_esm:.4f}, p={p_esm:.2e}")

    # Visualization: side-by-side ESM vs EV by conservation bin
    fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))

    ev_stats_df = pd.DataFrame(ev_bin_stats)
    x_labels2 = ev_stats_df["bin"].tolist()
    x_pos2 = np.arange(len(x_labels2))
    width = 0.35

    # Panel 1: Precision@K comparison
    ax = axes2[0]
    ax.bar(x_pos2 - width/2, ev_stats_df["esm_precision_at_K"], width, label="ESM2", color="steelblue")
    ax.bar(x_pos2 + width/2, ev_stats_df["ev_precision_at_K"], width, label="EVcouplings", color="coral")
    ax.set_xticks(x_pos2)
    ax.set_xticklabels(x_labels2, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Precision @ K")
    ax.set_title("Precision by conservation bin")
    ax.set_ylim(0, 1)
    ax.legend()

    # Panel 2: Mean score for true contacts (both methods, normalized to [0,1] range)
    ax = axes2[1]
    # Normalize EV scores to [0,1] for visual comparison
    ev_min, ev_max = df2["ev_score"].min(), df2["ev_score"].max()
    ev_contacts_norm = ev_stats_df["ev_mean_score_contacts"].apply(lambda x: (x - ev_min) / (ev_max - ev_min))
    ax.bar(x_pos2 - width/2, ev_stats_df["esm_mean_score_contacts"], width, label="ESM2 (raw)", color="steelblue")
    ax.bar(x_pos2 + width/2, ev_contacts_norm, width, label="EV (normalized)", color="coral")
    ax.set_xticks(x_pos2)
    ax.set_xticklabels(x_labels2, rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("Mean score (true contacts)")
    ax.set_title("Confidence on true contacts by conservation")
    ax.legend()

    # Panel 3: Scatter of ESM vs EV scores colored by conservation
    ax = axes2[2]
    sc = ax.scatter(df2.loc[df2["gt_contact"] == 1, "ev_score"],
                    df2.loc[df2["gt_contact"] == 1, "pred_score"],
                    c=df2.loc[df2["gt_contact"] == 1, "pair_cons_mean"],
                    cmap="viridis", alpha=0.6, s=15, edgecolors="none")
    plt.colorbar(sc, ax=ax, label="Mean pair conservation")
    ax.set_xlabel("EVcouplings score")
    ax.set_ylabel("ESM2 contact score")
    ax.set_title("ESM vs EV scores (true contacts only)")

    plt.tight_layout()
    plt.savefig("reports/outputs/2B61A/2B61A_conservation_ev_vs_esm.png", dpi=150)
    print(f"\nSaved figure to reports/outputs/2B61A/2B61A_conservation_ev_vs_esm.png")

print("\n=== Done ===")
