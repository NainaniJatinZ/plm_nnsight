"""
Generate per-protein config stubs from data/jump_details_esm_650.json.

Only creates configs for proteins that don't already have one.
Proteins with a known contact_pair should already have a handwritten config;
this script fills in flank info for the rest and leaves contact_pair as null.

Usage:
    uv run python scripts/gen_protein_configs.py
    uv run python scripts/gen_protein_configs.py --overwrite   # overwrite existing
"""
import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
JUMP_JSON = REPO_ROOT / "data" / "jump_details_esm_650.json"
CONFIGS_DIR = REPO_ROOT / "configs"

parser = argparse.ArgumentParser()
parser.add_argument("--overwrite", action="store_true", help="Overwrite existing configs")
args = parser.parse_args()

with open(JUMP_JSON) as f:
    jump_data = json.load(f)

created, skipped = [], []
for protein, info in jump_data.items():
    cfg_path = CONFIGS_DIR / f"{protein}.json"
    if cfg_path.exists() and not args.overwrite:
        skipped.append(protein)
        continue

    cfg = {
        "contact_pair": None,  # fill in manually
        "clean_flank": info["clean_flank_length"],
        "corrupt_flank": info["corrupted_flank_length"],
    }
    with open(cfg_path, "w") as f:
        json.dump(cfg, f, indent=2)
    created.append(protein)

print(f"Created {len(created)} configs: {created}")
print(f"Skipped {len(skipped)} existing: {skipped}")
print(f"\nNote: contact_pair is null for generated configs — fill in manually before running analysis.")
