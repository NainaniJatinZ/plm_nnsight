"""Rebuild pairs.csv on the full n=129 corpus (no audit filter), writing to pairs_all.csv.

Imports stage_pairs from anchor_cath_transfer with audit_only=False, then renames
the output so the existing audit-only pairs.csv is preserved.
"""
from pathlib import Path
import shutil, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import anchor_cath_transfer as act
import pandas as pd

# Build manifest the same way the cath_transfer main does
manifest_path = act.OUT_DIR / "manifest.csv"
if manifest_path.exists():
    manifest = pd.read_csv(manifest_path)
else:
    # Reconstruct from anchors.csv (it has set, pfam, hsf, pdb, chain)
    a = pd.read_csv(act.ANCHOR_FILE)
    manifest = a[["chain_key","set","pfam_id","hsf","pdb","chain"]].copy()
    manifest = manifest.rename(columns={"pfam_id":"pfam"})

# Move existing pairs.csv aside, run, rename output
audit_pairs = act.OUT_DIR / "pairs.csv"
backup = act.OUT_DIR / "pairs_audit.csv"
if audit_pairs.exists() and not backup.exists():
    shutil.copy(audit_pairs, backup)
    print(f"backed up {audit_pairs.name} -> {backup.name}")

act.stage_pairs(manifest, audit_only=False)

# stage_pairs always writes to pairs.csv; rename it to pairs_all.csv and restore audit
new_path = act.OUT_DIR / "pairs_all.csv"
shutil.move(str(audit_pairs), str(new_path))
shutil.copy(backup, audit_pairs)
print(f"wrote full-corpus -> {new_path}")
print(f"restored audit-only -> {audit_pairs}")
