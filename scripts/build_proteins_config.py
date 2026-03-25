"""
Merge jump_details_esm_650.json + reproduce_pair_recovery_100_w_bos_eos.json
into a single configs/proteins.json.

Only includes proteins present in BOTH files (jump_details defines the set of
proteins with a confirmed flank jump; reproduce_pair gives contact_pair).

For proteins with multiple contact pairs in reproduce_pair, the first is used.

Usage:
    uv run python scripts/build_proteins_config.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

with open(ROOT / "data" / "jump_details_esm_650.json") as f:
    jump = json.load(f)

with open(ROOT / "data" / "reproduce_pair_recovery_100_w_bos_eos.json") as f:
    pairs = json.load(f)

proteins = {}
missing_pair = []

for protein, info in jump.items():
    if protein not in pairs:
        missing_pair.append(protein)
        continue
    contact_pairs = pairs[protein]  # list of [pos1, pos2]
    proteins[protein] = {
        "contact_pair": contact_pairs[0],   # take first pair
        "clean_flank": info["clean_flank_length"],
        "corrupt_flank": info["corrupted_flank_length"],
    }

out_path = ROOT / "configs" / "proteins.json"
with open(out_path, "w") as f:
    json.dump(proteins, f, indent=2)

print(f"Written {len(proteins)} proteins to {out_path}")
if missing_pair:
    print(f"Skipped (no contact_pair in reproduce_pair file): {missing_pair}")
