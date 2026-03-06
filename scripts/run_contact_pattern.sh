#!/bin/bash
#SBATCH -c 4
#SBATCH --mem=100GB
#SBATCH -p gpu-preempt
#SBATCH -G 1
#SBATCH -t 3:00:00
#SBATCH --constraint=vram40
#SBATCH --output=contact_pattern_%j.out
#SBATCH --error=contact_pattern_%j.err
#SBATCH -A pi_annagreen_umass_edu

# Usage (submit from project root):
#   sbatch --export=START=0,END=10 scripts/run_contact_pattern.sh
#   sbatch --export=START=10,END=20 scripts/run_contact_pattern.sh
#
# START and END are 0-based indices into the proteins.json key list (END exclusive).
# Omit END to run to the end of the list.
#
# Note: --output and --error are relative to the submission directory,
# so log files land in the project root. Move them to logs/ after if needed.

echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start time: $(date)"

# SLURM_SUBMIT_DIR is always set to where sbatch was called from
cd "$SLURM_SUBMIT_DIR" || { echo "ERROR: could not cd to $SLURM_SUBMIT_DIR"; exit 1; }
echo "Working directory: $(pwd)"

START=${START:-0}
END=${END:-""}

PROTEINS=$(.plm_nn/bin/python -c "
import json
with open('configs/proteins.json') as f:
    keys = list(json.load(f).keys())
start = int('$START')
end   = int('$END') if '$END' else len(keys)
print(' '.join(keys[start:end]))
")

echo "Proteins to run (index ${START}–${END:-end}): $PROTEINS"
echo ""

for PROTEIN in $PROTEINS; do
    echo "========================================"
    echo "Running protein: $PROTEIN  ($(date))"
    echo "========================================"
    .plm_nn/bin/python -u contact_pattern_v2.py --protein "$PROTEIN"
    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "ERROR: $PROTEIN failed with exit code $STATUS" >&2
    else
        echo "Done: $PROTEIN"
    fi
    echo ""
done

echo "All done. End time: $(date)"
