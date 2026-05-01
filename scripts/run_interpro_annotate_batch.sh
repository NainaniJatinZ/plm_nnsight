#!/usr/bin/env bash
# Batch-annotate chains from a todo list using interpro_hmm_annotate.py
# Resumable: skips chains that already have a pfam_summary.tsv.
set -u
TODO=${1:-reports/out2/anchor_hmm_v2/annotate_todo.txt}
OUT=${2:-reports/out2/interpro_hmm}
LOG=reports/out2/anchor_hmm_v2/annotate_batch.log
ERR=reports/out2/anchor_hmm_v2/annotate_failed.txt
mkdir -p "$(dirname "$LOG")"
: > "$ERR"
total=$(wc -l < "$TODO")
i=0
while IFS= read -r chain; do
  i=$((i+1))
  [ -z "$chain" ] && continue
  if [ -f "$OUT/$chain/pfam_summary.tsv" ]; then
    echo "[$i/$total] skip $chain (cached)" >> "$LOG"
    continue
  fi
  echo "[$i/$total] $chain" >> "$LOG"
  if ! uv run python scripts/interpro_hmm_annotate.py "$chain" --out "$OUT" >> "$LOG" 2>&1; then
    echo "$chain" >> "$ERR"
  fi
  sleep 0.3
done < "$TODO"
echo "[done] failed: $(wc -l < "$ERR")" >> "$LOG"
