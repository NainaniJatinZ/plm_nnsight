from __future__ import annotations

import argparse, json, os, pickle, random, sys, time
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass

import numpy as np
import torch
import matplotlib.pyplot as plt

from datasets import load_dataset
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, top_k_accuracy_score
from sklearn.preprocessing import normalize as l2_normalize
from sklearn.model_selection import StratifiedShuffleSplit
from transformers import EsmForMaskedLM, EsmTokenizer


# =============================================================================
# Pfam Probe v2 — sequence-level Pfam family detection
# Linear probe on frozen ESM2-650M hidden states
#
# Changes from v1:
#   - Use all classes with >= min_class_count examples (default ~700 classes)
#     instead of top-100, so the task is non-trivial and target proteins'
#     actual Pfam families are included
#   - L2-normalize embeddings before probing
#   - Stratified train/val/test splits
#   - Regularization sweep on validation set
#   - Separate cache directory (v2) to avoid stale cache conflicts
#
# Run on all proteins:  uv run python pfam_probe.py
# Run on one protein:   uv run python pfam_probe.py --protein 2B61A
# =============================================================================


# ── Config ────────────────────────────────────────────────────────────────────

_SCRIPT_DIR   = Path(__file__).resolve().parent
_PROTEINS_CFG = _SCRIPT_DIR / "configs" / "proteins.json"
_COMMON_CFG   = _SCRIPT_DIR / "configs" / "common.json"

_p = argparse.ArgumentParser()
_p.add_argument("--protein", default=None,
                help="Protein ID to run (default: all proteins in configs/proteins.json)")
_p.add_argument("--train_n", type=int, default=50000,
                help="Max training sequences for Pfam probe")
_p.add_argument("--val_n", type=int, default=5000,
                help="Max validation sequences for Pfam probe")
_p.add_argument("--test_n", type=int, default=5000,
                help="Max test sequences for Pfam probe")
_p.add_argument("--min_class_count", type=int, default=80,
                help="Minimum examples per Pfam class to keep")
_p.add_argument("--max_length", type=int, default=1022,
                help="Max ESM sequence length excluding BOS/EOS")
_p.add_argument("--top_k", type=int, default=5,
                help="Top-k for reporting full-sequence Pfam predictions")
_p.add_argument("--batch_size", type=int, default=8,
                help="Batch size for embedding extraction")
_args, _ = _p.parse_known_args()

with open(_PROTEINS_CFG) as _f:
    PROTEINS: dict = json.load(_f)

with open(_COMMON_CFG) as _f:
    _common_cfg = json.load(_f)

MODEL_NAME     = _common_cfg.get("model",          "facebook/esm2_t33_650M_UR50D")
DATA_PATH      = _common_cfg.get("data_path",      "data/full_seq_dict.json")
SEGMENT_RADIUS = _common_cfg.get("segment_radius", 5)
_REPORT_BASE   = Path(_common_cfg.get("report_dir", "reports/outputs"))

if _args.protein is not None:
    if _args.protein not in PROTEINS:
        raise KeyError(f"Protein '{_args.protein}' not found in configs/proteins.json.")
    _run_proteins = [_args.protein]
else:
    _run_proteins = list(PROTEINS.keys())

PROBE_CACHE_DIR = "reports/cache/pfam_probe_v2"
os.makedirs(PROBE_CACHE_DIR, exist_ok=True)


# ── ContactSegment ────────────────────────────────────────────────────────────

@dataclass
class ContactSegment:
    ss1_start: int; ss1_end: int
    ss2_start: int; ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int = SEGMENT_RADIUS):
        return cls(pos1 - radius, pos1 + radius + 1,
                   pos2 - radius, pos2 + radius + 1)


# ── Device + Model ────────────────────────────────────────────────────────────

device    = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}", flush=True)

esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
esm_model.eval()


# ── Sequence dict ─────────────────────────────────────────────────────────────

with open(DATA_PATH) as f:
    seq_dict = json.load(f)


# ── Helper functions ──────────────────────────────────────────────────────────

def mask_with_flanks(seq_S: str, seg: ContactSegment, flank: int) -> str:
    """Replace non-segment non-flank residues with <mask>."""
    n = len(seq_S)
    masked: list[str] = ["<mask>"] * n

    s1_lo = max(0, seg.ss1_start)
    s1_hi = min(n, seg.ss1_end)
    s2_lo = max(0, seg.ss2_start)
    s2_hi = min(n, seg.ss2_end)

    masked[s1_lo:s1_hi] = list(seq_S[s1_lo:s1_hi])
    masked[s2_lo:s2_hi] = list(seq_S[s2_lo:s2_hi])

    for i in range(max(0, s1_lo - flank), s1_lo):
        masked[i] = seq_S[i]
    for i in range(s2_hi, min(n, s2_hi + flank)):
        masked[i] = seq_S[i]

    return "".join(masked)


def compute_contact_map(sequence_S: str) -> torch.Tensor:
    """Returns (A, A) contact map on CPU."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        return esm_model.predict_contacts(
            inputs_BL["input_ids"], inputs_BL["attention_mask"]
        )[0].cpu()


def patching_metric(pred_AA: torch.Tensor, orig_AA: torch.Tensor,
                    seg: ContactSegment) -> float:
    pred  = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig  = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = (orig * orig).sum()
    return ((pred * orig).sum() / denom).item() if denom > 1e-12 else 0.0


def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    p = np.clip(p, eps, 1.0)
    q = np.clip(q, eps, 1.0)
    p = p / p.sum()
    q = q / q.sum()
    return float(np.sum(p * np.log(p / q)))


def allowed_seq(seq: str) -> bool:
    aa = set("ACDEFGHIKLMNPQRSTVWYBXZOUJ")
    return isinstance(seq, str) and len(seq) > 0 and set(seq).issubset(aa)


# =============================================================================
# 1. Dataset — probe training (protein-independent)
# =============================================================================

print("\nLoading DanielHesslow/SwissProt-Pfam ...")
ds = load_dataset("DanielHesslow/SwissProt-Pfam")
data = ds["train"]

# Keep single-label sequences with valid amino acid content
rows_all = []
for r in data:
    seq = r.get("seq") or r.get("sequence") or r.get("protein_sequence")
    if not seq or not allowed_seq(seq):
        continue
    labels = r.get("labels", [])
    if len(labels) != 1:
        continue
    rows_all.append({"sequence": seq, "label": labels[0]})

# Drop rare classes
from collections import Counter
counts = Counter(r["label"] for r in rows_all)
rows_all = [r for r in rows_all if counts[r["label"]] >= _args.min_class_count]

label_list = sorted(set(r["label"] for r in rows_all))
label_to_idx = {lab: i for i, lab in enumerate(label_list)}
idx_to_label = {i: lab for lab, i in label_to_idx.items()}

# Build a Pfam accession lookup from the dataset for reporting
pfam_accession_map: dict[int, str] = {}
for r in data:
    labels = r.get("labels", [])
    labels_str = r.get("labels_str", "")
    if len(labels) == 1 and labels[0] in label_to_idx:
        if "Pfam:" in labels_str:
            acc = labels_str.split("Pfam:")[1].split("'")[0].split("]")[0].strip()
            if acc and labels[0] not in pfam_accession_map:
                pfam_accession_map[labels[0]] = acc

print(f"Total filtered rows: {len(rows_all):,}")
print(f"Num classes        : {len(label_list):,}")

# Stratified split
all_labels_arr = np.array([label_to_idx[r["label"]] for r in rows_all])

# First split: train vs (val+test)
n_val_test = min(_args.val_n + _args.test_n, len(rows_all) // 5)  # at most 20% for val+test
n_train_target = min(_args.train_n, len(rows_all) - n_val_test)
train_frac = n_train_target / len(rows_all)
val_test_frac = n_val_test / len(rows_all)

splitter1 = StratifiedShuffleSplit(n_splits=1, test_size=val_test_frac, random_state=42)
train_idx, val_test_idx = next(splitter1.split(rows_all, all_labels_arr))

# Second split: val vs test (50/50 of the val_test portion)
val_test_labels = all_labels_arr[val_test_idx]
splitter2 = StratifiedShuffleSplit(n_splits=1, test_size=0.5, random_state=42)
val_sub_idx, test_sub_idx = next(splitter2.split(val_test_idx, val_test_labels))
val_idx = val_test_idx[val_sub_idx]
test_idx = val_test_idx[test_sub_idx]

# Cap sizes
if len(train_idx) > _args.train_n:
    rng = np.random.RandomState(42)
    train_idx = rng.choice(train_idx, size=_args.train_n, replace=False)
if len(val_idx) > _args.val_n:
    rng = np.random.RandomState(42)
    val_idx = rng.choice(val_idx, size=_args.val_n, replace=False)
if len(test_idx) > _args.test_n:
    rng = np.random.RandomState(42)
    test_idx = rng.choice(test_idx, size=_args.test_n, replace=False)

train_rows = [rows_all[i] for i in train_idx]
val_rows   = [rows_all[i] for i in val_idx]
test_rows  = [rows_all[i] for i in test_idx]

print(f"Unique labels — train: {len(set(r['label'] for r in train_rows))}, "
      f"val: {len(set(r['label'] for r in val_rows))}, "
      f"test: {len(set(r['label'] for r in test_rows))}")
print(f"Sizes — train: {len(train_rows):,}, val: {len(val_rows):,}, test: {len(test_rows):,}")


# =============================================================================
# 2. Extract pooled sequence embeddings (with L2 normalization)
# =============================================================================

def extract_sequence_embeddings(
    rows: list[dict],
    split_name: str = "unknown",
    layer: int = -1,
    cache_path: str | None = None,
    max_length: int = 1022,
    batch_size: int = 8,
) -> tuple[np.ndarray, np.ndarray]:
    if cache_path and os.path.exists(cache_path):
        print(f"  [{split_name}] Loading from cache: {cache_path}", flush=True)
        d = np.load(cache_path, allow_pickle=True)
        return d["embs"], d["labels"]

    esm_model.eval()
    all_embs, all_labels = [], []
    n_batches = (len(rows) + batch_size - 1) // batch_size
    t0 = time.time()

    print(f"  [{split_name}] Extracting {len(rows):,} sequences in {n_batches:,} batches (batch_size={batch_size})", flush=True)

    for batch_idx, i in enumerate(range(0, len(rows), batch_size)):
        batch = rows[i:i+batch_size]
        seqs = [r["sequence"] for r in batch]
        labs = [label_to_idx[r["label"]] for r in batch]

        enc = tokenizer(seqs, return_tensors="pt", truncation=True, max_length=max_length, padding=True).to(device)
        with torch.no_grad():
            out = esm_model.esm(**enc, output_hidden_states=True)
            hidden = out.hidden_states[layer]  # [B, L, D]

        attn_mask = enc["attention_mask"]  # [B, L]
        for j in range(len(batch)):
            seq_len = int(attn_mask[j].sum()) - 2  # exclude BOS/EOS
            h = hidden[j, 1:seq_len+1]  # [seq_len, D]
            pooled = h.mean(dim=0)
            all_embs.append(pooled.cpu().float().numpy())
            all_labels.append(labs[j])

        done = batch_idx + 1
        if done % 100 == 0 or done == n_batches:
            elapsed = time.time() - t0
            rate = done / elapsed
            eta = (n_batches - done) / rate if rate > 0 else 0
            pct = 100.0 * done / n_batches
            print(f"  [{split_name}] {done}/{n_batches} batches ({pct:.1f}%)  elapsed={elapsed:.0f}s  ETA={eta:.0f}s  ({rate:.1f} batch/s)", flush=True)

    elapsed_total = time.time() - t0
    print(f"  [{split_name}] Done in {elapsed_total:.0f}s", flush=True)

    embs   = np.stack(all_embs, axis=0)
    labels = np.array(all_labels, dtype=np.int32)

    # L2 normalize
    embs = l2_normalize(embs, axis=1)

    if cache_path:
        np.savez(cache_path, embs=embs, labels=labels)
        print(f"  [{split_name}] Saved to {cache_path}  ({embs.shape[0]:,} seqs)", flush=True)

    return embs, labels


print("\nExtracting pooled sequence embeddings (L2-normalized)...", flush=True)
train_embs, train_labels = extract_sequence_embeddings(
    train_rows, split_name="train", cache_path=f"{PROBE_CACHE_DIR}/train_seq.npz", max_length=_args.max_length, batch_size=_args.batch_size)
val_embs, val_labels = extract_sequence_embeddings(
    val_rows, split_name="val", cache_path=f"{PROBE_CACHE_DIR}/val_seq.npz", max_length=_args.max_length, batch_size=_args.batch_size)
test_embs, test_labels = extract_sequence_embeddings(
    test_rows, split_name="test", cache_path=f"{PROBE_CACHE_DIR}/test_seq.npz", max_length=_args.max_length, batch_size=_args.batch_size)

print(f"\nSequences — train: {len(train_labels):,}, val: {len(val_labels):,}, test: {len(test_labels):,}")


# =============================================================================
# 3. Train linear probe with regularization sweep
# =============================================================================

print(f"\nRegularization sweep on validation set ({len(train_labels):,} train, {len(val_labels):,} val)...", flush=True)
C_values = [0.001, 0.01, 0.1, 1.0, 10.0]
best_C, best_val_acc = None, -1.0

for ci, C in enumerate(C_values):
    t_c = time.time()
    probe = LogisticRegression(max_iter=500, C=C, solver="lbfgs", class_weight="balanced", verbose=0)
    probe.fit(train_embs, train_labels)
    val_preds = probe.predict(val_embs)
    acc = accuracy_score(val_labels, val_preds)
    print(f"  [{ci+1}/{len(C_values)}] C={C:<8}  val_acc={acc:.4f}  ({time.time()-t_c:.0f}s)", flush=True)
    if acc > best_val_acc:
        best_val_acc = acc
        best_C = C

print(f"\nBest C={best_C}  (val_acc={best_val_acc:.4f})", flush=True)
print("Training final probe with best C...", flush=True)

pfam_probe = LogisticRegression(max_iter=1000, C=best_C, solver="lbfgs", class_weight="balanced", verbose=1)
pfam_probe.fit(train_embs, train_labels)

val_preds  = pfam_probe.predict(val_embs)
test_preds = pfam_probe.predict(test_embs)

val_probs  = pfam_probe.predict_proba(val_embs)
test_probs = pfam_probe.predict_proba(test_embs)

all_class_ids = np.arange(len(label_list))

for k in [1, 3, 5]:
    if val_probs.shape[1] >= k:
        val_topk = top_k_accuracy_score(val_labels, val_probs, k=k, labels=all_class_ids)
        test_topk = top_k_accuracy_score(test_labels, test_probs, k=k, labels=all_class_ids)
        print(f"  Val top-{k}  : {val_topk:.4f}")
        print(f"  Test top-{k} : {test_topk:.4f}")

val_acc  = accuracy_score(val_labels,  val_preds)
test_acc = accuracy_score(test_labels, test_preds)
print(f"\nPfam Probe accuracy:")
print(f"  Val  : {val_acc:.4f}")
print(f"  Test : {test_acc:.4f}")

# Train-val gap as overfitting diagnostic
train_preds = pfam_probe.predict(train_embs)
train_acc = accuracy_score(train_labels, train_preds)
print(f"  Train: {train_acc:.4f}")
print(f"  Train-Val gap: {train_acc - val_acc:.4f}")
print(f"  Val-Test gap : {val_acc - test_acc:.4f}")

with open(f"{PROBE_CACHE_DIR}/pfam_probe.pkl", "wb") as f:
    pickle.dump(pfam_probe, f)

with open(f"{PROBE_CACHE_DIR}/label_mapping.json", "w") as f:
    json.dump({
        "label_to_idx": {str(k): v for k, v in label_to_idx.items()},
        "idx_to_label": {str(k): v for k, v in idx_to_label.items()},
        "pfam_accessions": {str(k): v for k, v in pfam_accession_map.items()},
        "best_C": best_C,
        "n_classes": len(label_list),
        "train_acc": train_acc,
        "val_acc": val_acc,
        "test_acc": test_acc,
    }, f, indent=2)

print("Probe saved.")


# =============================================================================
# 4. Per-protein helper functions
# =============================================================================

def _get_hidden_states(sequence_S: str, max_length: int = 1022, layer: int = -1) -> torch.Tensor:
    enc = tokenizer(sequence_S, return_tensors="pt", truncation=True, max_length=max_length).to(device)
    actual_len = enc["input_ids"].shape[1] - 2
    with torch.no_grad():
        out = esm_model.esm(**enc, output_hidden_states=True)
        h = out.hidden_states[layer][0, 1:actual_len+1]
    return h


def get_sequence_embedding(sequence_S: str, max_length: int = 1022) -> np.ndarray:
    h = _get_hidden_states(sequence_S, max_length=max_length)
    pooled = h.mean(dim=0).cpu().float().numpy()
    pooled = l2_normalize(pooled.reshape(1, -1))[0]
    return pooled


def _segment_bounds(n: int, seg: ContactSegment, flank: int = 0) -> tuple[tuple[int, int], tuple[int, int]]:
    s1_lo = max(0, seg.ss1_start - flank)
    s1_hi = min(n, seg.ss1_end + flank)
    s2_lo = max(0, seg.ss2_start - flank)
    s2_hi = min(n, seg.ss2_end + flank)
    return (s1_lo, s1_hi), (s2_lo, s2_hi)


def get_segment_embedding(
    sequence_S: str,
    seg: ContactSegment,
    flank: int = 0,
    max_length: int = 1022,
    layer: int = -1,
    merge_overlaps: bool = True,
) -> np.ndarray:
    h = _get_hidden_states(sequence_S, max_length=max_length, layer=layer)
    n = h.shape[0]
    (s1_lo, s1_hi), (s2_lo, s2_hi) = _segment_bounds(n, seg, flank=flank)

    spans = [(s1_lo, s1_hi), (s2_lo, s2_hi)]
    spans = [(lo, hi) for lo, hi in spans if hi > lo]

    if not spans:
        pooled = h.mean(dim=0)
    else:
        if merge_overlaps:
            spans = sorted(spans)
            merged = [list(spans[0])]
            for lo, hi in spans[1:]:
                if lo <= merged[-1][1]:
                    merged[-1][1] = max(merged[-1][1], hi)
                else:
                    merged.append([lo, hi])
            spans = [(lo, hi) for lo, hi in merged]
        region_h = torch.cat([h[lo:hi] for lo, hi in spans], dim=0)
        pooled = region_h.mean(dim=0)

    out = pooled.cpu().float().numpy()
    out = l2_normalize(out.reshape(1, -1))[0]
    return out


def get_masked_segment_embedding(
    sequence_S: str,
    seg: ContactSegment,
    mask_flank: int,
    pool_flank: int,
    max_length: int = 1022,
    layer: int = -1,
) -> np.ndarray:
    masked_seq = mask_with_flanks(sequence_S, seg, mask_flank)
    return get_segment_embedding(masked_seq, seg=seg, flank=pool_flank, max_length=max_length, layer=layer)


def pfam_probe_predict(sequence_S: str) -> dict:
    x = get_sequence_embedding(sequence_S, max_length=_args.max_length)[None, :]
    probs = pfam_probe.predict_proba(x)[0]
    pred_idx = int(np.argmax(probs))
    pred_lab = idx_to_label[pred_idx]
    pred_prob = float(probs[pred_idx])
    uniform = 1.0 / len(probs)
    pred_log_enrichment = float(np.log(pred_prob / uniform))

    topk = min(_args.top_k, len(probs))
    top_idx = np.argsort(probs)[::-1][:topk]

    return {
        "pred_idx": pred_idx,
        "pred_label": pred_lab,
        "pred_prob": pred_prob,
        "probs": probs,
        "top_idx": top_idx.tolist(),
        "top_labels": [idx_to_label[int(i)] for i in top_idx],
        "top_probs": [float(probs[int(i)]) for i in top_idx],
        "pred_log_enrichment": pred_log_enrichment,
    }


def pfam_probe_predict_local(
    sequence_S: str,
    seg: ContactSegment,
    mask_flank: int,
    pool_flank: int | None = None,
) -> dict:
    if pool_flank is None:
        pool_flank = mask_flank

    x = get_masked_segment_embedding(sequence_S, seg=seg, mask_flank=mask_flank, pool_flank=pool_flank, max_length=_args.max_length)[None, :]

    probs = pfam_probe.predict_proba(x)[0]
    pred_idx = int(np.argmax(probs))
    pred_lab = idx_to_label[pred_idx]
    pred_prob = float(probs[pred_idx])

    uniform = 1.0 / len(probs)
    pred_log_enrichment = float(np.log(pred_prob / uniform))

    topk = min(_args.top_k, len(probs))
    top_idx = np.argsort(probs)[::-1][:topk]

    return {
        "pred_idx": pred_idx,
        "pred_label": pred_lab,
        "pred_prob": pred_prob,
        "pred_log_enrichment": pred_log_enrichment,
        "probs": probs,
        "top_idx": top_idx.tolist(),
        "top_labels": [idx_to_label[int(i)] for i in top_idx],
        "top_probs": [float(probs[int(i)]) for i in top_idx],
    }


def _label_display(numeric_label) -> str:
    """Return 'PFxxxxx (id)' if we have the accession, else just the id."""
    acc = pfam_accession_map.get(numeric_label, None)
    if acc:
        return f"{acc} ({numeric_label})"
    return str(numeric_label)


# =============================================================================
# 5. Per-protein loop
# =============================================================================

print(f"\n{'='*60}")
print(f"Running Pfam probe sweep on {len(_run_proteins)} protein(s)")
print(f"{'='*60}")

for protein in _run_proteins:
    prot_cfg      = PROTEINS[protein]
    CONTACT_PAIR  = tuple(prot_cfg["contact_pair"])
    CLEAN_FLANK   = prot_cfg["clean_flank"]
    CORRUPT_FLANK = prot_cfg["corrupt_flank"]

    FLANK_START = max(0, CORRUPT_FLANK - 20)
    FLANK_END   = CLEAN_FLANK + 20

    REPORT_DIR = _REPORT_BASE / protein
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if protein not in seq_dict:
        print(f"\n[{protein}] Not found in {DATA_PATH}, skipping.")
        continue

    sequence_S = seq_dict[protein]
    segment    = ContactSegment.from_contact_pair(*CONTACT_PAIR)

    print(f"\nProtein : {protein}  (len={len(sequence_S)})")
    print(f"Segment : ss1=[{segment.ss1_start}:{segment.ss1_end}]  ss2=[{segment.ss2_start}:{segment.ss2_end}]")
    print(f"Flanks  : corrupt={CORRUPT_FLANK}  clean={CLEAN_FLANK}  sweep=[{FLANK_START}, {FLANK_END}]")

    # ── Original contact map ──────────────────────────────────────────────
    print("  Computing original contact map...")
    orig_contacts_AA = compute_contact_map(sequence_S)

    # ── Full-sequence Pfam reference ──────────────────────────────────────
    print("  Computing full-sequence Pfam reference...")
    full_pfam = pfam_probe_predict(sequence_S)
    full_ref_idx   = full_pfam["pred_idx"]
    full_ref_label = full_pfam["pred_label"]
    full_ref_prob  = full_pfam["pred_prob"]
    full_ref_probs = full_pfam["probs"]

    print(f"  Full-seq top Pfam: {_label_display(full_ref_label)}  p={full_ref_prob:.4f}  log_enrich={full_pfam['pred_log_enrichment']:.3f}")
    print("  Full-seq top predictions:")
    for lab, prob in zip(full_pfam["top_labels"], full_pfam["top_probs"]):
        print(f"    {_label_display(lab):>25}   {prob:.4f}")

    print("  Computing local-region Pfam reference...")
    local_full_pfam = pfam_probe_predict_local(sequence_S, seg=segment, mask_flank=CLEAN_FLANK, pool_flank=CLEAN_FLANK)
    local_ref_idx   = local_full_pfam["pred_idx"]
    local_ref_label = local_full_pfam["pred_label"]
    local_ref_prob  = local_full_pfam["pred_prob"]
    local_ref_probs = local_full_pfam["probs"]

    print(f"  Local top Pfam   : {_label_display(local_ref_label)}  p={local_ref_prob:.4f}  log_enrich={local_full_pfam['pred_log_enrichment']:.3f}")
    print("  Local top predictions:")
    for lab, prob in zip(local_full_pfam["top_labels"], local_full_pfam["top_probs"]):
        print(f"    {_label_display(lab):>25}   {prob:.4f}")

    # ── Flank sweep ───────────────────────────────────────────────────────
    print(f"\n  Flank sweep ({FLANK_START} -> {FLANK_END}):")
    print(f"  {'─'*170}")
    print(
        f"  {'flank':>6}  {'contact':>9}  "
        f"{'full_ref_p':>10}  {'full_same':>9}  {'KL_full':>10}  "
        f"{'local_ref_p':>11}  {'local_same':>10}  {'KL_local':>10}  "
        f"{'top1_prob':>10}  {'margin':>8}"
    )
    print(f"  {'─'*170}")

    pfam_results = []
    n_flanks = FLANK_END - FLANK_START + 1
    t_sweep = time.time()

    for fi, flank in enumerate(range(FLANK_START, FLANK_END + 1)):
        masked_seq  = mask_with_flanks(sequence_S, segment, flank)
        contacts_AA = compute_contact_map(masked_seq)
        contact_val = patching_metric(contacts_AA, orig_contacts_AA, segment)

        mk_pfam = pfam_probe_predict(masked_seq)
        mk_probs = mk_pfam["probs"]

        mk_local_pfam = pfam_probe_predict_local(sequence_S, seg=segment, mask_flank=flank, pool_flank=flank)
        mk_local_probs = mk_local_pfam["probs"]

        full_ref_pfam_prob = float(mk_probs[full_ref_idx])
        full_same_top1 = int(mk_pfam["pred_idx"] == full_ref_idx)
        kl_full_masked = kl_divergence(full_ref_probs, mk_probs)

        local_ref_pfam_prob = float(mk_local_probs[local_ref_idx])
        local_same_top1 = int(mk_local_pfam["pred_idx"] == local_ref_idx)
        kl_local_masked = kl_divergence(local_ref_probs, mk_local_probs)

        top1_prob = float(mk_pfam["pred_prob"])

        sorted_probs = np.sort(mk_probs)[::-1]
        margin = float(sorted_probs[0] - sorted_probs[1]) if len(sorted_probs) >= 2 else float(sorted_probs[0])

        pfam_results.append({
            "flank": flank,
            "contact": contact_val,
            "full_ref_pfam_prob": full_ref_pfam_prob,
            "full_same_top1": full_same_top1,
            "kl_full_masked": kl_full_masked,
            "local_ref_pfam_prob": local_ref_pfam_prob,
            "local_same_top1": local_same_top1,
            "kl_local_masked": kl_local_masked,
            "top1_idx": int(mk_pfam["pred_idx"]),
            "top1_label": mk_pfam["pred_label"],
            "top1_prob": top1_prob,
            "margin": margin,
            "local_top1_idx": int(mk_local_pfam["pred_idx"]),
            "local_top1_label": mk_local_pfam["pred_label"],
            "local_top1_prob": float(mk_local_pfam["pred_prob"]),
        })

        sweep_elapsed = time.time() - t_sweep
        sweep_rate = (fi + 1) / sweep_elapsed if sweep_elapsed > 0 else 0
        sweep_eta = (n_flanks - fi - 1) / sweep_rate if sweep_rate > 0 else 0
        print(
            f"  {flank:>6}  {contact_val:>9.4f}  "
            f"{full_ref_pfam_prob:>10.4f}  {full_same_top1:>9d}  {kl_full_masked:>10.4f}  "
            f"{local_ref_pfam_prob:>11.4f}  {local_same_top1:>10d}  {kl_local_masked:>10.4f}  "
            f"{top1_prob:>10.4f}  {margin:>8.4f}"
            f"  [{fi+1}/{n_flanks} ETA={sweep_eta:.0f}s]",
            flush=True,
        )

    print(f"  {'─'*170}")

    # ── Summary stats ────────────────────────────────────────────────────
    flanks_arr    = np.array([r["flank"] for r in pfam_results])
    contact_arr   = np.array([r["contact"] for r in pfam_results])
    full_refprob_arr   = np.array([r["full_ref_pfam_prob"] for r in pfam_results])
    full_same_arr      = np.array([r["full_same_top1"] for r in pfam_results])
    local_refprob_arr  = np.array([r["local_ref_pfam_prob"] for r in pfam_results])
    local_same_arr     = np.array([r["local_same_top1"] for r in pfam_results])
    top1prob_arr       = np.array([r["top1_prob"] for r in pfam_results])
    kl_full_arr        = np.array([r["kl_full_masked"] for r in pfam_results])
    kl_local_arr       = np.array([r["kl_local_masked"] for r in pfam_results])
    margin_arr         = np.array([r["margin"] for r in pfam_results])

    corr_contact_full_refprob = float(np.corrcoef(contact_arr, full_refprob_arr)[0, 1]) if len(contact_arr) > 1 else float("nan")
    corr_contact_local_refprob = float(np.corrcoef(contact_arr, local_refprob_arr)[0, 1]) if len(contact_arr) > 1 else float("nan")
    corr_contact_full_kl = float(np.corrcoef(contact_arr, -kl_full_arr)[0, 1]) if len(contact_arr) > 1 else float("nan")
    corr_contact_local_kl = float(np.corrcoef(contact_arr, -kl_local_arr)[0, 1]) if len(contact_arr) > 1 else float("nan")

    print(f"\n  Corr(contact, full_ref_pfam_prob):  {corr_contact_full_refprob:.4f}")
    print(f"  Corr(contact, local_ref_pfam_prob): {corr_contact_local_refprob:.4f}")
    print(f"  Corr(contact, -KL_full):            {corr_contact_full_kl:.4f}")
    print(f"  Corr(contact, -KL_local):           {corr_contact_local_kl:.4f}")

    # ── Plot ──────────────────────────────────────────────────────────────
    fig, axes = plt.subplots(4, 1, figsize=(12, 13), sharex=True)

    axes[0].plot(flanks_arr, contact_arr, "o-", lw=2, label="contact metric")
    axes[0].axvline(CORRUPT_FLANK, color="red", ls="--", alpha=0.6, label=f"corrupt ({CORRUPT_FLANK})")
    axes[0].axvline(CLEAN_FLANK, color="green", ls="--", alpha=0.6, label=f"clean ({CLEAN_FLANK})")
    axes[0].set_ylabel("Contact metric")
    axes[0].set_title(f"{protein} — Pfam probe v2 vs contact recovery")
    axes[0].legend(fontsize=8)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(flanks_arr, full_refprob_arr, "s-", lw=2, label=f"whole: p(ref = {_label_display(full_ref_label)})")
    axes[1].plot(flanks_arr, top1prob_arr, "^-", lw=2, alpha=0.8, label="whole: masked top-1 prob")
    axes[1].plot(flanks_arr, full_same_arr, "D:", lw=1.5, alpha=0.8, label="whole: same top-1 as full")
    axes[1].set_ylabel("Whole-seq probe")
    axes[1].set_ylim(-0.05, 1.05)
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(flanks_arr, local_refprob_arr, "s-", lw=2, label=f"local: p(ref = {_label_display(local_ref_label)})")
    axes[2].plot(flanks_arr, local_same_arr, "D:", lw=1.5, alpha=0.8, label="local: same top-1 as local ref")
    axes[2].set_ylabel("Local probe")
    axes[2].set_ylim(-0.05, 1.05)
    axes[2].legend(fontsize=8)
    axes[2].grid(True, alpha=0.3)

    axes[3].plot(flanks_arr, kl_full_arr, "o-", lw=2, label="KL(full whole || masked whole)")
    axes[3].plot(flanks_arr, kl_local_arr, "s-", lw=2, label="KL(full local || masked local)")
    axes[3].plot(flanks_arr, margin_arr, "^--", lw=1.5, alpha=0.8, label="whole top-1 margin")
    axes[3].set_ylabel("Distribution shift")
    axes[3].set_xlabel("Flank size")
    axes[3].legend(fontsize=8)
    axes[3].grid(True, alpha=0.3)

    if len(contact_arr) > 1:
        jump_idx   = int(np.argmax(np.diff(contact_arr)))
        jump_flank = flanks_arr[jump_idx]
        for ax in axes:
            ax.axvspan(jump_flank - 0.5, jump_flank + 1.5, alpha=0.12)

    plt.tight_layout()
    outpath = str(REPORT_DIR / f"{protein}_pfam_sweep.png")
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved to {outpath}")

    # ── Markdown report ───────────────────────────────────────────────────
    def _make_pfam_report() -> str:
        lines: list[str] = []
        a = lines.append

        a(f"# Pfam Probe v2 Analysis: {protein}")
        a("")
        a(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   Model: {MODEL_NAME}")
        a("")

        a("## Configuration")
        a("")
        a("| Parameter | Value |")
        a("|-----------|-------|")
        a(f"| Protein | {protein} |")
        a(f"| Contact pair | {CONTACT_PAIR} |")
        a(f"| ss1 | [{segment.ss1_start}, {segment.ss1_end}) |")
        a(f"| ss2 | [{segment.ss2_start}, {segment.ss2_end}) |")
        a(f"| Clean flank | {CLEAN_FLANK} |")
        a(f"| Corrupt flank | {CORRUPT_FLANK} |")
        a(f"| Segment radius | {SEGMENT_RADIUS} |")
        a(f"| Flank sweep | [{FLANK_START}, {FLANK_END}] |")
        a(f"| Train sequences | {len(train_rows):,} |")
        a(f"| Val sequences | {len(val_rows):,} |")
        a(f"| Test sequences | {len(test_rows):,} |")
        a(f"| Num Pfam classes | {len(label_list):,} |")
        a(f"| Best C (regularization) | {best_C} |")
        a(f"| L2 normalization | yes |")
        a(f"| Stratified splits | yes |")
        a("")

        a("## Pfam Probe Performance")
        a("")
        a("| Split | Accuracy | Top-5 Accuracy |")
        a("|-------|----------|----------------|")
        top5_k = min(5, val_probs.shape[1])
        train_probs_for_report = pfam_probe.predict_proba(train_embs[:1000])
        train_labels_for_report = train_labels[:1000]
        a(f"| Train | {train_acc:.4f} | - |")
        a(f"| Val   | {val_acc:.4f} | {top_k_accuracy_score(val_labels, val_probs, k=top5_k, labels=all_class_ids):.4f} |")
        a(f"| Test  | {test_acc:.4f} | {top_k_accuracy_score(test_labels, test_probs, k=top5_k, labels=all_class_ids):.4f} |")
        a("")
        a(f"Train-Val gap: {train_acc - val_acc:.4f}")
        a("")

        a("## Full-sequence Pfam reference")
        a("")
        a("| Rank | Pfam | Prob |")
        a("|------|------|------|")
        for i, (lab, prob) in enumerate(zip(full_pfam["top_labels"], full_pfam["top_probs"]), start=1):
            a(f"| {i} | {_label_display(lab)} | {prob:.4f} |")
        a("")

        a("## Flank Sweep Results")
        a("")
        a("| flank | contact | whole_ref_p | whole_same | KL_full | local_ref_p | local_same | KL_local | top1_label | top1_prob | margin |")
        a("|-------|---------|-------------|------------|---------|-------------|------------|----------|------------|-----------|--------|")
        for r in pfam_results:
            a(
                f"| {r['flank']} | {r['contact']:.4f} | "
                f"{r['full_ref_pfam_prob']:.4f} | {r['full_same_top1']} | {r['kl_full_masked']:.4f} | "
                f"{r['local_ref_pfam_prob']:.4f} | {r['local_same_top1']} | {r['kl_local_masked']:.4f} | "
                f"{_label_display(r['top1_label'])} | {r['top1_prob']:.4f} | {r['margin']:.4f} |"
            )
        a("")

        a("## Summary")
        a("")
        a(f"- Corr(contact, whole_ref_pfam_prob) = {corr_contact_full_refprob:.4f}")
        a(f"- Corr(contact, local_ref_pfam_prob) = {corr_contact_local_refprob:.4f}")
        a(f"- Corr(contact, -KL_full) = {corr_contact_full_kl:.4f}")
        a(f"- Corr(contact, -KL_local) = {corr_contact_local_kl:.4f}")
        a("")

        a("## Plot")
        a("")
        a(f"![Pfam sweep]({protein}_pfam_sweep.png)")
        a("")

        return "\n".join(lines)

    report_path = REPORT_DIR / f"{protein}_pfam_report.md"
    report_path.write_text(_make_pfam_report())
    print(f"  Report written to: {report_path}")

print(f"\nDone. Processed {len(_run_proteins)} protein(s).")
