# =============================================================================
# SSE Probe — per-residue secondary structure (H/E/C)
# Token-level linear probe on frozen ESM2-650M hidden states
#
# Flanking sweep with masking approach:
#   run masked sequence through ESM2, extract hidden states at segment
#
# Run on all proteins:  .plm_nn/bin/python sse_probe.py
# Run on one protein:   .plm_nn/bin/python sse_probe.py --protein 2B61A
# =============================================================================
from __future__ import annotations

import argparse, json, os, pickle, random
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
import matplotlib.pyplot as plt
from dataclasses import dataclass
from datasets import load_dataset
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from transformers import EsmForMaskedLM, EsmTokenizer

# ── Config ────────────────────────────────────────────────────────────────────

_SCRIPT_DIR   = Path(__file__).resolve().parent
_PROTEINS_CFG = _SCRIPT_DIR / "configs" / "proteins.json"
_COMMON_CFG   = _SCRIPT_DIR / "configs" / "common.json"

_p = argparse.ArgumentParser()
_p.add_argument("--protein", default=None,
                help="Protein ID to run (default: all proteins in configs/proteins.json)")
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

PROBE_CACHE_DIR = "reports/cache/sse_probe"
os.makedirs(PROBE_CACHE_DIR, exist_ok=True)

# DSSP3 mapping — covers both 3-class and 8-class labels
SS8_TO_SS3 = {"H": 0, "G": 0, "I": 0,
               "E": 1, "B": 1,
               "T": 2, "S": 2, "C": 2, "L": 2, "-": 2}

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
print(f"Device: {device}")

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
    masked[seg.ss1_start:seg.ss1_end] = list(seq_S[seg.ss1_start:seg.ss1_end])
    masked[seg.ss2_start:seg.ss2_end] = list(seq_S[seg.ss2_start:seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
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

# =============================================================================
# 1. Dataset — probe training (protein-independent)
# =============================================================================

N_TRAIN = 1_000
N_VAL   =   100
N_TEST  =   100

print("\nLoading lamm-mit/protein_secondary_structure_from_PDB ...")
ds   = load_dataset("lamm-mit/protein_secondary_structure_from_PDB")
data = ds["train"].shuffle(seed=42)
n    = len(data)
train_ds = data.select(range(0,          int(0.8 * n)))
val_ds   = data.select(range(int(0.8*n), int(0.9 * n)))
test_ds  = data.select(range(int(0.9*n), n))

def _to_rows(hf_ds) -> list[dict]:
    return [{"sequence": r["Sequence"], "secondary_structure": r["Secondary_structure"]}
            for r in hf_ds if r["Sequence"] and r["Secondary_structure"]]

random.seed(42)
train_rows = random.sample(_to_rows(train_ds), N_TRAIN)
val_rows   = random.sample(_to_rows(val_ds),   N_VAL)
test_rows  = random.sample(_to_rows(test_ds),  N_TEST)

print(f"Sizes — train: {len(train_rows):,}, val: {len(val_rows):,}, test: {len(test_rows):,}")


def row_to_ss3(row: dict) -> tuple[str, list[int]]:
    seq = row["sequence"]
    ss8 = row["secondary_structure"]
    min_len = min(len(seq), len(ss8))
    return seq[:min_len], [SS8_TO_SS3.get(c, 2) for c in ss8[:min_len]]


def extract_residue_embeddings(
    rows: list[dict], layer: int = -1, cache_path: str | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    if cache_path and os.path.exists(cache_path):
        print(f"  Loading from cache: {cache_path}")
        d = np.load(cache_path)
        return d["embs"], d["labels"]

    esm_model.eval()
    all_embs, all_labels = [], []
    for i, row in enumerate(rows):
        seq, labs_full = row_to_ss3(row)
        enc = tokenizer(seq, return_tensors="pt", truncation=True, max_length=1022).to(device)
        actual_len = enc["input_ids"].shape[1] - 2
        with torch.no_grad():
            out = esm_model.esm(**enc, output_hidden_states=True)
            h   = out.hidden_states[layer][0, 1:actual_len+1]
        all_embs.append(h.cpu().float().numpy())
        all_labels.extend(labs_full[:actual_len])
        if i % 100 == 0:
            print(f"  {i}/{len(rows)}", end="\r")
    print()
    embs   = np.concatenate(all_embs, axis=0)
    labels = np.array(all_labels, dtype=np.int32)
    if cache_path:
        np.savez(cache_path, embs=embs, labels=labels)
        print(f"  Saved to {cache_path}  ({embs.shape[0]:,} residues)")
    return embs, labels


print("\nExtracting per-residue embeddings...")
train_embs, train_labels = extract_residue_embeddings(
    train_rows, cache_path=f"{PROBE_CACHE_DIR}/train.npz")
val_embs,   val_labels   = extract_residue_embeddings(
    val_rows,   cache_path=f"{PROBE_CACHE_DIR}/val.npz")
test_embs,  test_labels  = extract_residue_embeddings(
    test_rows,  cache_path=f"{PROBE_CACHE_DIR}/test.npz")

print(f"\nResidues — train: {len(train_labels):,}, val: {len(val_labels):,}, "
      f"test: {len(test_labels):,}")

# =============================================================================
# 2. Train linear probe (protein-independent)
# =============================================================================

print("\nTraining SSE linear probe...")
sse_probe = LogisticRegression(
    max_iter=500, C=1.0, solver="lbfgs",
    class_weight="balanced", n_jobs=-1, verbose=1,
)
sse_probe.fit(train_embs, train_labels)

val_preds  = sse_probe.predict(val_embs)
test_preds = sse_probe.predict(test_embs)
print(f"\nSSE Probe accuracy:")
print(f"  Val  : {accuracy_score(val_labels,  val_preds):.4f}")
print(f"  Test : {accuracy_score(test_labels, test_preds):.4f}")
print(classification_report(test_labels, test_preds,
      target_names=["H", "E", "C"], zero_division=0))

with open(f"{PROBE_CACHE_DIR}/sse_probe.pkl", "wb") as f:
    pickle.dump(sse_probe, f)
print("Probe saved.")

# =============================================================================
# 3. Mean activation (protein-independent)
# =============================================================================

_mean_act_cache = f"{PROBE_CACHE_DIR}/mean_activation.pt"
_pfam_mean_act  = "reports/cache/probe/mean_activation.pt"

if os.path.exists(_mean_act_cache):
    print("Loading mean activation from SSE cache.")
    mean_act_D = torch.load(_mean_act_cache, weights_only=True).to(device)
elif os.path.exists(_pfam_mean_act):
    print("Reusing mean activation from Pfam probe cache.")
    mean_act_D = torch.load(_pfam_mean_act, weights_only=True).to(device)
else:
    print("Computing mean activation from SSE train sequences...")
    all_h = []
    for row in train_rows[:100]:
        enc = tokenizer(row["sequence"], return_tensors="pt",
                        truncation=True, max_length=1022).to(device)
        with torch.no_grad():
            out = esm_model.esm(**enc, output_hidden_states=True)
        all_h.append(out.hidden_states[-1][0, 1:-1].cpu())
    mean_act_D = torch.cat(all_h, dim=0).mean(0).to(device)
    torch.save(mean_act_D, _mean_act_cache)
print(f"Mean activation shape: {mean_act_D.shape}")

# =============================================================================
# 4. Per-protein helper functions
# =============================================================================

def get_full_sse_preds(sequence_S: str) -> np.ndarray:
    enc = tokenizer(sequence_S, return_tensors="pt",
                    truncation=True, max_length=1022).to(device)
    actual_len = enc["input_ids"].shape[1] - 2
    with torch.no_grad():
        out = esm_model.esm(**enc, output_hidden_states=True)
        h   = out.hidden_states[-1][0, 1:actual_len+1]
    return sse_probe.predict(h.cpu().float().numpy())


def sse_probe_segment_masking(sequence_S: str, seg: ContactSegment,
                              flank_size: int) -> dict:
    n          = len(sequence_S)
    masked_seq = mask_with_flanks(sequence_S, seg, flank_size)
    enc        = tokenizer(masked_seq, return_tensors="pt",
                           truncation=True, max_length=1022).to(device)
    with torch.no_grad():
        out  = esm_model.esm(**enc, output_hidden_states=True)
        h_LD = out.hidden_states[-1][0]

    flk_l_start = max(0, seg.ss1_start - flank_size)
    flk_r_end   = min(n, seg.ss2_end + flank_size)

    results = {}
    for seg_name, seg_start, seg_end in [
        ("ss1",       seg.ss1_start, seg.ss1_end),
        ("ss2",       seg.ss2_start, seg.ss2_end),
        ("flk_left",  flk_l_start,   seg.ss1_start),
        ("flk_right", seg.ss2_end,   flk_r_end),
    ]:
        seg_h = h_LD[seg_start+1 : seg_end+1]
        if seg_h.shape[0] == 0:
            continue
        seg_h_np = seg_h.cpu().float().numpy()
        results[seg_name] = {
            "preds": sse_probe.predict(seg_h_np),
            "probs": sse_probe.predict_proba(seg_h_np),
        }
    return results

# =============================================================================
# 5. Per-protein loop
# =============================================================================

print(f"\n{'='*60}")
print(f"Running SSE probe sweep on {len(_run_proteins)} protein(s)")
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
    print(f"Segment : ss1=[{segment.ss1_start}:{segment.ss1_end}]  "
          f"ss2=[{segment.ss2_start}:{segment.ss2_end}]")
    print(f"Flanks  : corrupt={CORRUPT_FLANK}  clean={CLEAN_FLANK}  "
          f"sweep=[{FLANK_START}, {FLANK_END}]")

    # ── Original contact map ──────────────────────────────────────────────
    print("  Computing original contact map...")
    orig_contacts_AA = compute_contact_map(sequence_S)

    # ── Full-sequence SSE ground truth ────────────────────────────────────
    print("  Computing full-sequence SSE ground truth...")
    full_sse_preds_A = get_full_sse_preds(sequence_S)
    gt_ss1 = full_sse_preds_A[segment.ss1_start:segment.ss1_end]
    gt_ss2 = full_sse_preds_A[segment.ss2_start:segment.ss2_end]
    print(f"  SS1: {''.join('HEC'[p] for p in gt_ss1)}")
    print(f"  SS2: {''.join('HEC'[p] for p in gt_ss2)}")

    # ── Flank sweep ───────────────────────────────────────────────────────
    print(f"\n  Flank sweep ({FLANK_START} → {FLANK_END}):")
    print(f"  {'─'*106}")
    print(f"  {'flank':>6}  {'contact':>9}  "
          f"{'mk_ss1':>8}  {'mk_ss2':>8}  {'mk_mean':>8}  "
          f"{'mk_flkL':>8}  {'mk_flkR':>8}  {'mk_flk':>8}")
    print(f"  {'─'*106}")

    sse_results  = []
    all_mk_preds = {}

    for flank in range(FLANK_START, FLANK_END + 1):
        masked_seq  = mask_with_flanks(sequence_S, segment, flank)
        contacts_AA = compute_contact_map(masked_seq)
        contact_val = patching_metric(contacts_AA, orig_contacts_AA, segment)

        mk_preds = sse_probe_segment_masking(sequence_S, segment, flank)
        all_mk_preds[flank] = mk_preds

        mk_ss1  = accuracy_score(gt_ss1, mk_preds["ss1"]["preds"]) if "ss1" in mk_preds else 0.0
        mk_ss2  = accuracy_score(gt_ss2, mk_preds["ss2"]["preds"]) if "ss2" in mk_preds else 0.0
        mk_mean = (mk_ss1 + mk_ss2) / 2

        gt_flk_left  = full_sse_preds_A[max(0, segment.ss1_start - flank) : segment.ss1_start]
        gt_flk_right = full_sse_preds_A[segment.ss2_end : min(len(sequence_S), segment.ss2_end + flank)]

        mk_flkL = (accuracy_score(gt_flk_left,  mk_preds["flk_left"]["preds"])
                   if "flk_left"  in mk_preds and len(gt_flk_left)  > 0 else float("nan"))
        mk_flkR = (accuracy_score(gt_flk_right, mk_preds["flk_right"]["preds"])
                   if "flk_right" in mk_preds and len(gt_flk_right) > 0 else float("nan"))
        mk_flk  = float(np.nanmean([mk_flkL, mk_flkR]))

        sse_results.append({
            "flank": flank, "contact": contact_val,
            "mk_ss1": mk_ss1, "mk_ss2": mk_ss2, "mk_mean": mk_mean,
            "mk_flkL": mk_flkL, "mk_flkR": mk_flkR, "mk_flk": mk_flk,
        })

        def _fmt(v): return f"{v:>8.3f}" if not np.isnan(v) else f"{'nan':>8}"
        print(f"  {flank:>6}  {contact_val:>9.4f}  "
              f"{mk_ss1:>8.3f}  {mk_ss2:>8.3f}  {mk_mean:>8.3f}  "
              f"{_fmt(mk_flkL)}  {_fmt(mk_flkR)}  {_fmt(mk_flk)}")

    print(f"  {'─'*106}")

    # ── Residue-level changes near clean flank ────────────────────────────
    _HEC      = "HEC"
    _FOCUS_LO = max(FLANK_START, CLEAN_FLANK - 2)
    _FOCUS_HI = min(FLANK_END,   CLEAN_FLANK + 2)

    print(f"\n{'═'*78}")
    print(f"  Residue-level prediction changes  "
          f"(clean={CLEAN_FLANK}, focus flanks {_FOCUS_LO}–{_FOCUS_HI})")
    print(f"{'═'*78}")
    print(f"  {'Seg':<7} {'Direction':<14} {'Pos':>5}   gt  prev  now")

    for _flank in range(_FOCUS_LO, _FOCUS_HI + 1):
        _prev = _flank - 1
        if _prev not in all_mk_preds:
            continue
        _curr_mk = all_mk_preds[_flank]
        _prev_mk = all_mk_preds[_prev]

        print(f"\n  ── {_prev} → {_flank} {'─'*58}")
        _any = False

        for _key, _seg_start, _gt_arr, _lbl in [
            ("ss1", segment.ss1_start, gt_ss1, "SS1"),
            ("ss2", segment.ss2_start, gt_ss2, "SS2"),
        ]:
            if _key not in _curr_mk or _key not in _prev_mk:
                continue
            for _i, (_gt, _p, _c) in enumerate(
                    zip(_gt_arr, _prev_mk[_key]["preds"], _curr_mk[_key]["preds"])):
                _pos = _seg_start + _i
                if _p != _gt and _c == _gt:
                    print(f"  {_lbl:<7} {'incorr→corr':<14} {_pos:>5}   "
                          f"{_HEC[_gt]}   {_HEC[_p]}     {_HEC[_c]}")
                    _any = True
                elif _p == _gt and _c != _gt:
                    print(f"  {_lbl:<7} {'corr→incorr':<14} {_pos:>5}   "
                          f"{_HEC[_gt]}   {_HEC[_p]}     {_HEC[_c]}")
                    _any = True

        for _key, _lbl in [("flk_left", "flk_L"), ("flk_right", "flk_R")]:
            if _key not in _curr_mk or _key not in _prev_mk:
                continue
            _pc = _curr_mk[_key]["preds"]
            _pp = _prev_mk[_key]["preds"]
            if _key == "flk_left":
                _abs_c = max(0, segment.ss1_start - _flank)
                if len(_pc) > len(_pp):
                    _pc = _pc[1:]; _abs_c += 1
            else:
                _abs_c = segment.ss2_end
                if len(_pc) > len(_pp):
                    _pc = _pc[:-1]
            _gt_ov = full_sse_preds_A[_abs_c : _abs_c + len(_pc)]
            for _i, (_gt, _p, _c) in enumerate(zip(_gt_ov, _pp, _pc)):
                _pos = _abs_c + _i
                if _p != _gt and _c == _gt:
                    print(f"  {_lbl:<7} {'incorr→corr':<14} {_pos:>5}   "
                          f"{_HEC[_gt]}   {_HEC[_p]}     {_HEC[_c]}")
                    _any = True
                elif _p == _gt and _c != _gt:
                    print(f"  {_lbl:<7} {'corr→incorr':<14} {_pos:>5}   "
                          f"{_HEC[_gt]}   {_HEC[_p]}     {_HEC[_c]}")
                    _any = True

        if not _any:
            print("  (no prediction changes in any segment)")

    print()

    # ── Plot ──────────────────────────────────────────────────────────────
    flanks_arr  = np.array([r["flank"]   for r in sse_results])
    contact_arr = np.array([r["contact"] for r in sse_results])
    mk_ss1_arr  = np.array([r["mk_ss1"]  for r in sse_results])
    mk_ss2_arr  = np.array([r["mk_ss2"]  for r in sse_results])
    mk_mean_arr = np.array([r["mk_mean"] for r in sse_results])
    mk_flkL_arr = np.array([r["mk_flkL"] for r in sse_results], dtype=float)
    mk_flkR_arr = np.array([r["mk_flkR"] for r in sse_results], dtype=float)
    mk_flk_arr  = np.array([r["mk_flk"]  for r in sse_results], dtype=float)

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    axes[0].plot(flanks_arr, contact_arr, "o-", color="steelblue", lw=2, label="contact metric")
    axes[0].axvline(CORRUPT_FLANK, color="red",   ls="--", alpha=0.6, label=f"corrupt ({CORRUPT_FLANK})")
    axes[0].axvline(CLEAN_FLANK,   color="green", ls="--", alpha=0.6, label=f"clean ({CLEAN_FLANK})")
    axes[0].set_ylabel("Contact metric")
    axes[0].set_title(f"{protein} — SSE probe (masking): segments + flanks")
    axes[0].legend(fontsize=8); axes[0].grid(True, alpha=0.3)

    axes[1].plot(flanks_arr, mk_ss1_arr,  "s-",  color="steelblue",   lw=2,
                 label=f"SS1 [{segment.ss1_start}:{segment.ss1_end}]")
    axes[1].plot(flanks_arr, mk_ss2_arr,  "^-",  color="mediumpurple", lw=2,
                 label=f"SS2 [{segment.ss2_start}:{segment.ss2_end}]")
    axes[1].plot(flanks_arr, mk_flkL_arr, "s--", color="darkorange",   lw=2,
                 label="flk_left  (left of SS1)")
    axes[1].plot(flanks_arr, mk_flkR_arr, "^--", color="forestgreen",  lw=2,
                 label="flk_right (right of SS2)")
    axes[1].plot(flanks_arr, mk_mean_arr, "D:",  color="saddlebrown",  lw=1.5, alpha=0.6,
                 label="mean(ss1, ss2)")
    axes[1].set_ylabel("SSE accuracy (masking)")
    axes[1].set_xlabel("Flank size")
    axes[1].set_ylim(0, 1.05); axes[1].legend(fontsize=7); axes[1].grid(True, alpha=0.3)

    if len(contact_arr) > 1:
        jump_idx   = int(np.argmax(np.diff(contact_arr)))
        jump_flank = flanks_arr[jump_idx]
        for ax in axes:
            ax.axvspan(jump_flank - 0.5, jump_flank + 1.5, alpha=0.12, color="red")

    plt.tight_layout()
    outpath = str(REPORT_DIR / f"{protein}_sse_sweep.png")
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved to {outpath}")

    # ── Markdown report ───────────────────────────────────────────────────
    def _make_sse_report() -> str:
        lines: list[str] = []
        a = lines.append

        a(f"# SSE Probe Analysis: {protein}")
        a(f"")
        a(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   Model: {MODEL_NAME}")
        a(f"")

        a(f"## Configuration")
        a(f"")
        a(f"| Parameter | Value |")
        a(f"|-----------|-------|")
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
        a(f"")

        a(f"## SSE Probe Performance")
        a(f"")
        a(f"| Split | Accuracy |")
        a(f"|-------|----------|")
        a(f"| Val   | {accuracy_score(val_labels, val_preds):.4f} |")
        a(f"| Test  | {accuracy_score(test_labels, test_preds):.4f} |")
        a(f"")
        a(f"**Test classification report:**")
        a(f"")
        a(f"```")
        a(classification_report(test_labels, test_preds,
                                target_names=["H", "E", "C"], zero_division=0))
        a(f"```")
        a(f"")

        a(f"## Ground-Truth SSE (full-sequence probe)")
        a(f"")
        a(f"| Segment | Sequence |")
        a(f"|---------|----------|")
        a(f"| SS1 [{segment.ss1_start}:{segment.ss1_end}] | `{''.join('HEC'[p] for p in gt_ss1)}` |")
        a(f"| SS2 [{segment.ss2_start}:{segment.ss2_end}] | `{''.join('HEC'[p] for p in gt_ss2)}` |")
        a(f"")

        a(f"## Flank Sweep Results")
        a(f"")
        a(f"| flank | contact | mk_ss1 | mk_ss2 | mk_mean | mk_flkL | mk_flkR | mk_flk |")
        a(f"|-------|---------|--------|--------|---------|---------|---------|--------|")
        for r in sse_results:
            def _fv(v): return f"{v:.3f}" if not np.isnan(v) else "nan"
            a(f"| {r['flank']} | {r['contact']:.4f} | {r['mk_ss1']:.3f} | {r['mk_ss2']:.3f} "
              f"| {r['mk_mean']:.3f} | {_fv(r['mk_flkL'])} | {_fv(r['mk_flkR'])} "
              f"| {_fv(r['mk_flk'])} |")
        a(f"")

        a(f"## Residue-Level Prediction Changes (clean={CLEAN_FLANK}, focus ±2)")
        a(f"")
        _HEC_r      = "HEC"
        _focus_lo_r = max(FLANK_START, CLEAN_FLANK - 2)
        _focus_hi_r = min(FLANK_END,   CLEAN_FLANK + 2)

        for _flank in range(_focus_lo_r, _focus_hi_r + 1):
            _prev = _flank - 1
            if _prev not in all_mk_preds:
                continue
            _curr_mk = all_mk_preds[_flank]
            _prev_mk = all_mk_preds[_prev]
            _rows = []

            for _key, _seg_start, _gt_arr, _lbl in [
                ("ss1", segment.ss1_start, gt_ss1, "SS1"),
                ("ss2", segment.ss2_start, gt_ss2, "SS2"),
            ]:
                if _key not in _curr_mk or _key not in _prev_mk:
                    continue
                for _i, (_gt, _p, _c) in enumerate(
                        zip(_gt_arr, _prev_mk[_key]["preds"], _curr_mk[_key]["preds"])):
                    _pos = _seg_start + _i
                    if _p != _gt and _c == _gt:
                        _rows.append((_lbl, "incorr→corr", _pos,
                                      _HEC_r[_gt], _HEC_r[_p], _HEC_r[_c]))
                    elif _p == _gt and _c != _gt:
                        _rows.append((_lbl, "corr→incorr", _pos,
                                      _HEC_r[_gt], _HEC_r[_p], _HEC_r[_c]))

            for _key, _lbl in [("flk_left", "flk_L"), ("flk_right", "flk_R")]:
                if _key not in _curr_mk or _key not in _prev_mk:
                    continue
                _pc = _curr_mk[_key]["preds"]
                _pp = _prev_mk[_key]["preds"]
                if _key == "flk_left":
                    _abs_c = max(0, segment.ss1_start - _flank)
                    if len(_pc) > len(_pp):
                        _pc = _pc[1:]; _abs_c += 1
                else:
                    _abs_c = segment.ss2_end
                    if len(_pc) > len(_pp):
                        _pc = _pc[:-1]
                _gt_ov = full_sse_preds_A[_abs_c : _abs_c + len(_pc)]
                for _i, (_gt, _p, _c) in enumerate(zip(_gt_ov, _pp, _pc)):
                    _pos = _abs_c + _i
                    if _p != _gt and _c == _gt:
                        _rows.append((_lbl, "incorr→corr", _pos,
                                      _HEC_r[_gt], _HEC_r[_p], _HEC_r[_c]))
                    elif _p == _gt and _c != _gt:
                        _rows.append((_lbl, "corr→incorr", _pos,
                                      _HEC_r[_gt], _HEC_r[_p], _HEC_r[_c]))

            a(f"### Flank {_prev} → {_flank}")
            a(f"")
            if _rows:
                a(f"| Seg | Direction | Pos | gt | prev | now |")
                a(f"|-----|-----------|-----|----|------|-----|")
                for _seg, _dir, _pos, _gt_c, _prev_c, _now_c in _rows:
                    a(f"| {_seg} | {_dir} | {_pos} | {_gt_c} | {_prev_c} | {_now_c} |")
            else:
                a(f"_(no prediction changes)_")
            a(f"")

        a(f"## Plot")
        a(f"")
        a(f"![SSE sweep]({protein}_sse_sweep.png)")
        a(f"")

        return "\n".join(lines)

    report_path = REPORT_DIR / f"{protein}_sse_report.md"
    report_path.write_text(_make_sse_report())
    print(f"  Report written to: {report_path}")

print(f"\nDone. Processed {len(_run_proteins)} protein(s).")
