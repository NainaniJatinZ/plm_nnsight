#!/bin/bash
#SBATCH -c 4
#SBATCH --mem=100GB
#SBATCH -p gpu
#SBATCH -G 1
#SBATCH -t 4:00:00
#SBATCH --constraint=vram40
#SBATCH --output=esm2_3b_flank_sweep_%j.out
#SBATCH --error=esm2_3b_flank_sweep_%j.err
#SBATCH -A pi_annagreen_umass_edu

# Usage:
#   sbatch scripts/run_esm2_3b_flank_sweep.sh
#   sbatch scripts/run_esm2_3b_flank_sweep.sh --proteins 1BRTA 1BS0A
#   sbatch scripts/run_esm2_3b_flank_sweep.sh --max-flank 80 --stop-threshold 0.4
#
# By default this runs all proteins and writes:
#   data/jump_details_esm_3b.json
#   reports/out2/esm2_3b_flank_sweep/

echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "GPUs: $CUDA_VISIBLE_DEVICES"
echo "Start time: $(date)"
echo ""

cd "$SLURM_SUBMIT_DIR" || { echo "ERROR: could not cd to $SLURM_SUBMIT_DIR"; exit 1; }
echo "Working directory: $(pwd)"
echo "Args: $@"
echo ""

.venv/bin/python -u scripts/esm2_3b_flank_sweep.py \
  --all-proteins \
  --max-flank 60 \
  --stop-threshold 0.5 \
  --extra-after-hit 2 \
  --batch-size 4 \
  "$@"
STATUS=$?

echo ""
echo "Exit code: $STATUS"
echo "End time: $(date)"
exit $STATUS
