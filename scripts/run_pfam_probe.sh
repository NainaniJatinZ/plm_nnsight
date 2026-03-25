#!/bin/bash
#SBATCH -c 4
#SBATCH --mem=100GB
#SBATCH -p gpu
#SBATCH -G 1
#SBATCH -t 6:00:00
#SBATCH --constraint=vram40
#SBATCH --output=pfam_probe_%j.out
#SBATCH --error=pfam_probe_%j.err
#SBATCH -A pi_annagreen_umass_edu

# Usage (submit from project root):
#   sbatch scripts/run_pfam_probe.sh                         # all proteins
#   sbatch scripts/run_pfam_probe.sh --protein 2B61A         # single protein
#
# Extra args are forwarded to pfam_probe.py, e.g.:
#   sbatch scripts/run_pfam_probe.sh --protein 2B61A --train_n 20000 --batch_size 16
#
# Log files land in the project root (pfam_probe_<jobid>.out/.err).

echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "GPUs: $CUDA_VISIBLE_DEVICES"
echo "Start time: $(date)"
echo ""

cd "$SLURM_SUBMIT_DIR" || { echo "ERROR: could not cd to $SLURM_SUBMIT_DIR"; exit 1; }
echo "Working directory: $(pwd)"
echo "Args: $@"
echo ""

# -u = unbuffered stdout/stderr so progress appears in real time in the log
.venv/bin/python -u pfam_probe.py "$@"
STATUS=$?

echo ""
echo "Exit code: $STATUS"
echo "End time: $(date)"
exit $STATUS
