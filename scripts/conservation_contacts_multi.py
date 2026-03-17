"""
Multi-protein conservation vs contact prediction experiment.
Runs the ESM2 vs EVcouplings conservation analysis across all available proteins,
then aggregates results.
"""

# %%  Imports
import json
import glob
import os
import numpy as np
import pandas as pd
import torch
from Bio.PDB import PDBParser, is_aa

AA3TO1 = {
    "ALA": "A", "CYS": "C", "ASP": "D", "GLU": "E", "PHE": "F",
    "GLY": "G", "HIS": "H", "ILE": "I", "LYS": "K", "LEU": "L",
    "MET": "M", "ASN": "N", "PRO": "P", "GLN": "Q", "ARG": "R",
    "SER": "S", "THR": "T", "VAL": "V", "TRP": "W", "TYR": "Y",
}

CUTOFF = 8.0
MIN_SEQ_SEP = 6
CHAIN_ID = "A"

# %%  Discover proteins

with open("data/full_seq_dict.json") as f:
    all_seqs = json.load(f)

proteins = []

# 2B61A uses the old directory layout
proteins.append({
    "pid": "2B61A",
    "pdb_path": "data/TARGET_b0.3/2b61.pdb",
    "freq_csv": "data/TARGET_b0.3/align/TARGET_b0.3_frequencies.csv",
    "ev_csv": "data/TARGET_b0.3/couplings/TARGET_b0.3_CouplingScores_longrange.csv",
    "full_seq": all_seqs["2B61A"],
})

# New proteins in {PID}_EV directories
for ev_dir in sorted(glob.glob("data/*_EV/")):
    pid = os.path.basename(ev_dir.rstrip("/")).replace("_EV", "")
    target_dirs = glob.glob(f"{ev_dir}TARGET_b*/")
    if not target_dirs:
        continue
    tdir = target_dirs[0]
    pdb_files = glob.glob(f"{tdir}*.pdb")
    freq_files = glob.glob(f"{tdir}align/*_frequencies.csv")
    ev_files = glob.glob(f"{tdir}couplings/*_CouplingScores_longrange.csv")
    if not pdb_files or not freq_files or not ev_files:
        print(f"Skipping {pid}: missing data")
        continue
    if pid not in all_seqs:
        print(f"Skipping {pid}: no sequence in full_seq_dict.json")
        continue
    proteins.append({
        "pid": pid,
        "pdb_path": pdb_files[0],
        "freq_csv": freq_files[0],
        "ev_csv": ev_files[0],
        "full_seq": all_seqs[pid],
    })

print(f"Found {len(proteins)} proteins: {[p['pid'] for p in proteins]}")

# %%  Load ESM2 model (once)

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "facebook/esm2_t33_650M_UR50D"
print(f"\nLoading ESM2 on {device}...")
from transformers import EsmForMaskedLM, EsmTokenizer
tokenizer = EsmTokenizer.from_pretrained(model_name)
esm_model = EsmForMaskedLM.from_pretrained(model_name, attn_implementation="eager").to(device).eval()
print("Model loaded.")


# %%  Process each protein

def process_protein(prot):
    pid = prot["pid"]
    full_seq = prot["full_seq"]
    print(f"\n{'='*60}")
    print(f"Processing {pid} (seq len {len(full_seq)})")
    print(f"{'='*60}")

    # 1. Ground-truth contacts from PDB
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(pid, prot["pdb_path"])

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
    print(f"  PDB chain {CHAIN_ID}: {n_pdb} residues")

    # Contacts
    diff = pdb_coords[:, None, :] - pdb_coords[None, :, :]
    distances = np.sqrt(np.sum(diff * diff, axis=-1))
    gt_contacts = (distances <= CUTOFF).astype(np.uint8)
    np.fill_diagonal(gt_contacts, 0)
    for i in range(n_pdb):
        for j in range(n_pdb):
            if abs(i - j) < MIN_SEQ_SEP:
                gt_contacts[i, j] = 0
    n_gt = gt_contacts.sum() // 2
    print(f"  Ground-truth contacts: {n_gt}")

    # 2. Map PDB to full sequence
    pdb_seq_str = "".join(pdb_seq)
    match_idx = full_seq.find(pdb_seq_str[:10])
    if match_idx < 0:
        print(f"  ERROR: could not align PDB to sequence, skipping")
        return None

    pdb_to_fullseq = {}
    full_pos = match_idx
    for pdb_idx in range(n_pdb):
        found = False
        for offset in range(5):
            if full_pos + offset < len(full_seq) and full_seq[full_pos + offset] == pdb_seq[pdb_idx]:
                pdb_to_fullseq[pdb_idx] = full_pos + offset
                full_pos = full_pos + offset + 1
                found = True
                break
        if not found:
            pdb_to_fullseq[pdb_idx] = full_pos
            full_pos += 1

    # 3. Conservation
    freq_df = pd.read_csv(prot["freq_csv"])
    conservation = freq_df["conservation"].values

    pdb_conservation = np.array([conservation[pdb_to_fullseq[i]] for i in range(n_pdb)])

    # 4. ESM2 predictions
    inputs = tokenizer(full_seq, return_tensors="pt").to(device)
    with torch.no_grad():
        pred_AA = esm_model.predict_contacts(
            inputs["input_ids"], inputs["attention_mask"]
        )[0].cpu().numpy()

    # 5. Build pair dataframe
    pred_for_pdb = np.zeros((n_pdb, n_pdb))
    for i in range(n_pdb):
        for j in range(n_pdb):
            fi, fj = pdb_to_fullseq[i], pdb_to_fullseq[j]
            pred_for_pdb[i, j] = pred_AA[fi, fj]

    rows = []
    for i in range(n_pdb):
        for j in range(i + MIN_SEQ_SEP, n_pdb):
            rows.append({
                "protein": pid,
                "i": i, "j": j,
                "gt_contact": gt_contacts[i, j],
                "pred_score": pred_for_pdb[i, j],
                "cons_i": pdb_conservation[i],
                "cons_j": pdb_conservation[j],
                "pair_cons_min": min(pdb_conservation[i], pdb_conservation[j]),
                "pair_cons_mean": (pdb_conservation[i] + pdb_conservation[j]) / 2,
            })

    df = pd.DataFrame(rows)

    # 6. EVcouplings
    ev_df = pd.read_csv(prot["ev_csv"])
    fullseq_to_pdb = {v: k for k, v in pdb_to_fullseq.items()}

    ev_rows = []
    for _, row in ev_df.iterrows():
        fi = int(row["i"]) - 1
        fj = int(row["j"]) - 1
        if fi in fullseq_to_pdb and fj in fullseq_to_pdb:
            pi = fullseq_to_pdb[fi]
            pj = fullseq_to_pdb[fj]
            if pi > pj:
                pi, pj = pj, pi
            if pj - pi >= MIN_SEQ_SEP:
                ev_rows.append({"i": pi, "j": pj, "ev_score": row["score"]})

    ev_pair_df = pd.DataFrame(ev_rows).drop_duplicates(subset=["i", "j"])
    df = df.merge(ev_pair_df, on=["i", "j"], how="left")

    n_with_ev = df["ev_score"].notna().sum()
    n_contacts = int(df["gt_contact"].sum())
    print(f"  Pairs: {len(df)}, contacts: {n_contacts}, with EV: {n_with_ev}")

    # 7. Per-protein summary stats
    summary = {"protein": pid, "n_residues": n_pdb, "n_contacts": n_contacts, "n_pairs": len(df)}
    for divisor, label in [(1, "L"), (2, "L/2"), (5, "L/5")]:
        k = n_pdb // divisor
        summary[f"esm_prec_{label}"] = df.nlargest(k, "pred_score")["gt_contact"].mean()
        df_ev_only = df.dropna(subset=["ev_score"])
        if len(df_ev_only) >= k:
            summary[f"ev_prec_{label}"] = df_ev_only.nlargest(k, "ev_score")["gt_contact"].mean()
        else:
            summary[f"ev_prec_{label}"] = float("nan")

    for label, val in summary.items():
        if "prec" in label:
            print(f"  {label}: {val:.4f}")

    return df, summary


all_dfs = []
all_summaries = []

for prot in proteins:
    result = process_protein(prot)
    if result is not None:
        df, summary = result
        all_dfs.append(df)
        all_summaries.append(summary)

# %%  Combine and save

combined = pd.concat(all_dfs, ignore_index=True)
summary_df = pd.DataFrame(all_summaries)

os.makedirs("reports/cache/multi_protein", exist_ok=True)
combined.to_csv("reports/cache/multi_protein/conservation_pairs_all.csv", index=False)
summary_df.to_csv("reports/cache/multi_protein/protein_summaries.csv", index=False)

print(f"\n{'='*60}")
print(f"AGGREGATE RESULTS")
print(f"{'='*60}")
print(f"Proteins: {len(summary_df)}")
print(f"Total pairs: {len(combined)}")
print(f"Total contacts: {int(combined['gt_contact'].sum())}")
print(f"\nPer-protein summary:")
print(summary_df.to_string(index=False))

# %%  Aggregate precision by conservation bin

from scipy import stats as sp_stats

combined_ev = combined.dropna(subset=["ev_score"])
n_bins = 5

# Normalize scores within each protein so they're comparable across proteins
combined["esm_rank"] = combined.groupby("protein")["pred_score"].rank(pct=True)
combined_ev_c = combined_ev.copy()
combined_ev_c["ev_rank"] = combined_ev_c.groupby("protein")["ev_score"].rank(pct=True)
combined_ev_c["esm_rank"] = combined_ev_c.groupby("protein")["pred_score"].rank(pct=True)

# Correlation across all proteins
contacts_all = combined[combined["gt_contact"] == 1]
contacts_ev_all = combined_ev_c[combined_ev_c["gt_contact"] == 1]

print(f"\n=== Aggregate correlations (true contacts, all proteins pooled) ===")
r_esm, p_esm = sp_stats.pearsonr(contacts_all["pair_cons_mean"], contacts_all["pred_score"])
print(f"  ESM raw score vs conservation:  r={r_esm:.4f}, p={p_esm:.2e}")
r_esm_rank, p_esm_rank = sp_stats.pearsonr(contacts_all["pair_cons_mean"], contacts_all["esm_rank"])
print(f"  ESM rank vs conservation:       r={r_esm_rank:.4f}, p={p_esm_rank:.2e}")
r_ev, p_ev = sp_stats.pearsonr(contacts_ev_all["pair_cons_mean"], contacts_ev_all["ev_score"])
print(f"  EV raw score vs conservation:   r={r_ev:.4f}, p={p_ev:.2e}")
r_ev_rank, p_ev_rank = sp_stats.pearsonr(contacts_ev_all["pair_cons_mean"], contacts_ev_all["ev_rank"])
print(f"  EV rank vs conservation:        r={r_ev_rank:.4f}, p={p_ev_rank:.2e}")

# Per-protein correlations
print(f"\n=== Per-protein correlations (ESM score vs conservation, true contacts) ===")
per_protein_corr = []
for pid, grp in contacts_all.groupby("protein"):
    if len(grp) < 20:
        continue
    r, p = sp_stats.pearsonr(grp["pair_cons_mean"], grp["pred_score"])
    per_protein_corr.append({"protein": pid, "r_esm": r, "p_esm": p, "n_contacts": len(grp)})

for pid, grp in contacts_ev_all.groupby("protein"):
    if len(grp) < 20:
        continue
    r, p = sp_stats.pearsonr(grp["pair_cons_mean"], grp["ev_score"])
    for row in per_protein_corr:
        if row["protein"] == pid:
            row["r_ev"] = r
            row["p_ev"] = p

corr_df = pd.DataFrame(per_protein_corr)
print(corr_df.to_string(index=False))
corr_df.to_csv("reports/cache/multi_protein/per_protein_correlations.csv", index=False)

print("\n=== Done ===")
