# =============================================================================
# SSE Circuit Ablation — test hypothesis that INTRA heads carry SSE info
#                        while CROSS heads bridge contact sides
#
# For each protein, runs 4 conditions (full circuit, -INTRA, -CROSS, -OTHER)
# through the sufficiency-style nnsight trace, then measures both:
#   - contact metric (from attention via contact head)
#   - SSE accuracy   (from final-layer hidden states via linear probe)
#
# Run:  uv run python sse_circuit_ablation.py --protein 2B61A
#       uv run python sse_circuit_ablation.py   # all ready proteins
# =============================================================================
from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import json
import os
import pickle
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np
import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

# ── Configuration ────────────────────────────────────────────────────────────

_SCRIPT_DIR   = Path(__file__).resolve().parent
_COMMON_CFG   = _SCRIPT_DIR / "configs" / "common.json"
_PROTEINS_CFG = _SCRIPT_DIR / "configs" / "proteins.json"

with open(_PROTEINS_CFG) as _f:
    PROTEINS: dict = json.load(_f)

with open(_COMMON_CFG) as _f:
    _common_cfg = json.load(_f)


def load_config(protein: str) -> dict:
    cfg: dict = {}
    cfg.update(_common_cfg)
    cfg.update(PROTEINS[protein])
    return cfg


_p = argparse.ArgumentParser()
_p.add_argument("--protein", default=None,
                help="Protein ID (default: all proteins with required caches)")
_args, _ = _p.parse_known_args()

MODEL_NAME     = _common_cfg.get("model", "facebook/esm2_t33_650M_UR50D")
DATA_PATH      = _common_cfg.get("data_path", "data/full_seq_dict.json")
SEGMENT_RADIUS = _common_cfg.get("segment_radius", 5)
TOPK_CELL      = _common_cfg.get("topk_cell", 1000)
CACHE_BASE     = Path(_common_cfg.get("cache_dir", "reports/cache"))
REPORT_BASE    = Path(_common_cfg.get("report_dir", "reports/outputs"))
PROBE_PATH     = CACHE_BASE / "sse_probe" / "sse_probe.pkl"

# ── Helpers (copied from contact_pattern_v2.py — do NOT import) ─────────────

SS8_TO_SS3 = {"H": 0, "G": 0, "I": 0,
              "E": 1, "B": 1,
              "T": 2, "S": 2, "C": 2, "L": 2, "-": 2}

HEC = "HEC"


@dataclass
class ContactSegment:
    ss1_start: int; ss1_end: int
    ss2_start: int; ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int = SEGMENT_RADIUS):
        return cls(pos1 - radius, pos1 + radius + 1,
                   pos2 - radius, pos2 + radius + 1)


def mask_with_flanks(seq_S: str, seg: ContactSegment, flank: int) -> str:
    n = len(seq_S)
    masked: list[str] = ["<mask>"] * n
    masked[seg.ss1_start:seg.ss1_end] = list(seq_S[seg.ss1_start:seg.ss1_end])
    masked[seg.ss2_start:seg.ss2_end] = list(seq_S[seg.ss2_start:seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
        masked[i] = seq_S[i]
    return "".join(masked)


def patching_metric(
    pred_AA: torch.Tensor, orig_AA: torch.Tensor, seg: ContactSegment,
) -> float:
    pred = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = (orig * orig).sum()
    return ((pred * orig).sum() / denom).item() if denom > 1e-12 else 0.0


def faithfulness(metric: float, clean_m: float, corrupt_m: float) -> float:
    gap = clean_m - corrupt_m
    return (metric - corrupt_m) / gap if abs(gap) > 1e-6 else 0.0


def compute_contacts_from_attention(
    attn_list_LBHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor,
    attention_mask_BL: torch.Tensor,
    contact_head,
    device: str = "cuda",
) -> torch.Tensor:
    attn_stack = [a.to(device) for a in attn_list_LBHLL]
    tokens_BL         = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_stack, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]
    return contact_head(tokens_BL, attns_BLHLL)


def make_classify_pos(seg: ContactSegment, flank: int):
    ss1   = set(range(seg.ss1_start, seg.ss1_end))
    ss2   = set(range(seg.ss2_start, seg.ss2_end))
    flk_l = set(range(max(0, seg.ss1_start - flank), seg.ss1_start))
    flk_r = set(range(seg.ss2_end, seg.ss2_end + flank))

    def _classify(pos: int) -> str:
        if pos in ss1:   return "ss1"
        if pos in ss2:   return "ss2"
        if pos in flk_l: return "flkL"
        if pos in flk_r: return "flkR"
        return "other"

    return _classify


def clear_memory() -> None:
    gc.collect()
    torch.cuda.empty_cache()


# ── Determine which proteins to run ─────────────────────────────────────────

def _protein_ready(protein: str) -> bool:
    """Check that all required caches exist for a protein."""
    c = CACHE_BASE / protein
    r = REPORT_BASE / protein
    return (
        (c / "attn_cache.pt").exists()
        and (c / "cell_attr.pt").exists()
        and (c / "baselines.pt").exists()
        and (r / f"{protein}_summary.csv").exists()
    )


if _args.protein is not None:
    if _args.protein not in PROTEINS:
        raise KeyError(f"Protein '{_args.protein}' not in configs/proteins.json")
    if not _protein_ready(_args.protein):
        raise FileNotFoundError(
            f"Missing caches for {_args.protein}. Run contact_pattern_v2.py first.")
    run_proteins = [_args.protein]
else:
    run_proteins = [p for p in PROTEINS if _protein_ready(p)]

if not run_proteins:
    raise RuntimeError("No proteins have all required caches.")

print(f"Proteins to run: {run_proteins}")

# ── Check probe exists ───────────────────────────────────────────────────────

if not PROBE_PATH.exists():
    raise FileNotFoundError(
        f"SSE probe not found at {PROBE_PATH}. Run sse_probe.py first.")

# ── Load model + probe ───────────────────────────────────────────────────────

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

esm_model = EsmForMaskedLM.from_pretrained(
    MODEL_NAME, attn_implementation="eager").to(device)
tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
model     = NNsight(esm_model)

NUM_LAYERS = esm_model.config.num_hidden_layers
NUM_HEADS  = esm_model.config.num_attention_heads
HEAD_DIM   = esm_model.config.hidden_size // NUM_HEADS

print(f"Model: {MODEL_NAME}  ({NUM_LAYERS}L x {NUM_HEADS}H, head_dim={HEAD_DIM})")

with open(PROBE_PATH, "rb") as f:
    sse_probe = pickle.load(f)
print("SSE probe loaded.")

with open(DATA_PATH) as f:
    seq_dict = json.load(f)


# ── Head classification from summary CSV ─────────────────────────────────────

_ANCHOR_TYPES = {"SINGLE-ANCHOR", "DUAL-ANCHOR", "MULTI-ANCHOR"}


def load_head_groups(csv_path: Path) -> dict[tuple[int, int], str]:
    """Parse summary CSV → (layer, head) → group.

    Priority: INTRA > CROSS > ANCHOR > OTHER.
    A head is ANCHOR if its k_anchor or q_anchor is SINGLE/DUAL/MULTI-ANCHOR
    but it doesn't already have an INTRA or CROSS region tag.
    """
    mapping: dict[tuple[int, int], str] = {}
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            layer = int(row["layer"])
            head  = int(row["head"])
            region   = row.get("region", "").strip()
            k_anchor = row.get("k_anchor", "").strip()
            q_anchor = row.get("q_anchor", "").strip()
            if region.startswith("INTRA:"):
                mapping[(layer, head)] = "INTRA"
            elif region.startswith("CROSS:"):
                mapping[(layer, head)] = "CROSS"
            elif k_anchor in _ANCHOR_TYPES or q_anchor in _ANCHOR_TYPES:
                mapping[(layer, head)] = "ANCHOR"
            else:
                mapping[(layer, head)] = "OTHER"
    return mapping


# ── Full-sequence SSE ground truth ───────────────────────────────────────────

def get_full_sse_preds(sequence_S: str) -> np.ndarray:
    enc = tokenizer(sequence_S, return_tensors="pt",
                    truncation=True, max_length=1022).to(device)
    actual_len = enc["input_ids"].shape[1] - 2
    with torch.no_grad():
        out = esm_model.esm(**enc, output_hidden_states=True)
        h   = out.hidden_states[-1][0, 1:actual_len + 1]
    return sse_probe.predict(h.cpu().float().numpy())


# ── Run one condition ────────────────────────────────────────────────────────

def run_condition(
    protected_cells: set[tuple[int, int, int, int]],
    clean_inputs_BL: dict,
    corrupt_attn_LBHLL: list[torch.Tensor],
    seg: ContactSegment,
    orig_contacts_AA: torch.Tensor,
    clean_metric: float,
    corrupt_metric: float,
    clean_flank: int,
    sequence_S: str,
    full_sse_A: np.ndarray,
) -> dict:
    """Run sufficiency trace with given protected cells.

    Returns dict with contact metric, faithfulness, SSE accuracy per segment,
    and per-residue SSE predictions.
    """
    B = 1
    L = clean_inputs_BL["input_ids"].shape[1]
    n_seq = len(sequence_S)

    # --- nnsight trace: intervene on attention + capture hidden states ---
    with model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True,
                              "output_hidden_states": True}):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self
                         for i in range(NUM_LAYERS)]
            )

            for layer_idx in range(NUM_LAYERS):
                v_raw = model.esm.encoder.layer[layer_idx].attention.self.value.output
                v_heads = v_raw.reshape(B, L, NUM_HEADS, HEAD_DIM).transpose(1, 2)

                attn_probs = model.esm.encoder.layer[layer_idx].attention.self.output[1]

                patched_attn = corrupt_attn_LBHLL[layer_idx].to(device).clone()

                for head, q, kk in [(h, q, kk) for (l, h, q, kk) in protected_cells
                                     if l == layer_idx]:
                    patched_attn[:, head, q, kk] = attn_probs[:, head, q, kk]

                new_ctx = torch.matmul(patched_attn, v_heads)
                new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)
                model.esm.encoder.layer[layer_idx].attention.self.output[0][:] = new_ctx

            # Capture final hidden states for SSE probe
            # EsmLayer has .output remapped to .nns_output in nnsight
            final_hidden = model.esm.encoder.layer[NUM_LAYERS - 1].nns_output[0].save()

    # --- Contact map from captured attention ---
    attn_list = []
    for i in range(NUM_LAYERS):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        layer_attn = attn_cache[key].output[1].detach().cpu()
        corrupt_layer = corrupt_attn_LBHLL[i].clone()
        for head, q, kk in [(h, q, kk) for (l, h, q, kk) in protected_cells
                             if l == i]:
            corrupt_layer[:, head, q, kk] = layer_attn[:, head, q, kk]
        attn_list.append(corrupt_layer)

    contacts = compute_contacts_from_attention(
        attn_list, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'],
        esm_model.esm.contact_head, device=device,
    )[0].detach().cpu()

    metric      = patching_metric(contacts, orig_contacts_AA, seg)
    faith_score = faithfulness(metric, clean_metric, corrupt_metric)

    # --- SSE probe on final hidden states ---
    h_LD = final_hidden.detach().cpu().float()  # (L, D) — nnsight squeezes batch

    flk_l_start = max(0, seg.ss1_start - clean_flank)
    flk_r_end   = min(n_seq, seg.ss2_end + clean_flank)

    sse_results: dict[str, dict] = {}
    for seg_name, seg_start, seg_end in [
        ("ss1",      seg.ss1_start, seg.ss1_end),
        ("ss2",      seg.ss2_start, seg.ss2_end),
        ("flk_left", flk_l_start,   seg.ss1_start),
        ("flk_right", seg.ss2_end,  flk_r_end),
    ]:
        # token indices: +1 for BOS
        seg_h = h_LD[seg_start + 1: seg_end + 1]
        if seg_h.shape[0] == 0:
            continue
        seg_h_np = seg_h.numpy()
        preds = sse_probe.predict(seg_h_np)
        gt    = full_sse_A[seg_start:seg_end]
        acc   = (preds == gt).mean()
        sse_results[seg_name] = {
            "preds": preds,
            "gt":    gt,
            "acc":   float(acc),
        }

    # Aggregate SSE accuracies
    ss1_acc = sse_results.get("ss1", {}).get("acc", float("nan"))
    ss2_acc = sse_results.get("ss2", {}).get("acc", float("nan"))
    seg_mean = float(np.nanmean([ss1_acc, ss2_acc]))
    flk_l_acc = sse_results.get("flk_left",  {}).get("acc", float("nan"))
    flk_r_acc = sse_results.get("flk_right", {}).get("acc", float("nan"))
    flk_mean  = float(np.nanmean([flk_l_acc, flk_r_acc]))

    return {
        "metric":      metric,
        "faithfulness": faith_score,
        "ss1_acc":     ss1_acc,
        "ss2_acc":     ss2_acc,
        "seg_mean":    seg_mean,
        "flk_l_acc":   flk_l_acc,
        "flk_r_acc":   flk_r_acc,
        "flk_mean":    flk_mean,
        "sse_detail":  sse_results,
    }


# =============================================================================
# Main loop
# =============================================================================

print(f"\n{'='*70}")
print(f"SSE Circuit Ablation — {len(run_proteins)} protein(s)")
print(f"{'='*70}")

for protein in run_proteins:
    cfg       = load_config(protein)
    seg       = ContactSegment.from_contact_pair(*cfg["contact_pair"])
    clean_flk = cfg["clean_flank"]
    corrupt_flk = cfg["corrupt_flank"]
    topk      = cfg.get("topk_cell", TOPK_CELL)

    cache_dir  = CACHE_BASE / protein
    report_dir = REPORT_BASE / protein
    report_dir.mkdir(parents=True, exist_ok=True)

    if protein not in seq_dict:
        print(f"\n[{protein}] Not in {DATA_PATH}, skipping.")
        continue

    sequence_S = seq_dict[protein]
    clean_seq  = mask_with_flanks(sequence_S, seg, clean_flk)

    print(f"\n{'─'*60}")
    print(f"Protein: {protein}  len={len(sequence_S)}  topk={topk}")
    print(f"  ss1=[{seg.ss1_start}:{seg.ss1_end}]  "
          f"ss2=[{seg.ss2_start}:{seg.ss2_end}]  "
          f"clean_flank={clean_flk}  corrupt_flank={corrupt_flk}")

    # ── Load caches ──────────────────────────────────────────────────────
    baselines = torch.load(cache_dir / "baselines.pt",
                           map_location="cpu", weights_only=False)
    orig_contacts_AA = baselines["orig_contacts_AA"]
    clean_metric_val = baselines["clean_metric"]
    corrupt_metric_val = baselines["corrupt_metric"]

    attn_data = torch.load(cache_dir / "attn_cache.pt",
                           map_location="cpu", weights_only=False)
    clean_attn_LBHLL   = attn_data["clean_attn_LBHLL"]
    corrupt_attn_LBHLL = attn_data["corrupt_attn_LBHLL"]
    clean_inputs_cpu   = attn_data["clean_inputs_cpu"]

    clean_inputs_BL = {k: v.to(device) for k, v in clean_inputs_cpu.items()}

    cell_data = torch.load(cache_dir / "cell_attr.pt",
                           map_location="cpu", weights_only=False)
    cell_attr_sorted = cell_data["cell_attr_sorted"]

    print(f"  Baselines: clean={clean_metric_val:.4f}  corrupt={corrupt_metric_val:.4f}")
    print(f"  Total cells: {len(cell_attr_sorted):,}")

    # ── Head classification ──────────────────────────────────────────────
    csv_path = report_dir / f"{protein}_summary.csv"
    head_groups = load_head_groups(csv_path)

    # ── Build cell sets from top-K ───────────────────────────────────────
    topk_cells = cell_attr_sorted[:topk]

    all_cells:    set[tuple[int, int, int, int]] = set()
    intra_cells:  set[tuple[int, int, int, int]] = set()
    cross_cells:  set[tuple[int, int, int, int]] = set()
    anchor_cells: set[tuple[int, int, int, int]] = set()
    other_cells:  set[tuple[int, int, int, int]] = set()

    for layer, head, q, kk, attr, adiff in topk_cells:
        cell = (layer, head, q, kk)
        all_cells.add(cell)
        group = head_groups.get((layer, head), "OTHER")
        if group == "INTRA":
            intra_cells.add(cell)
        elif group == "CROSS":
            cross_cells.add(cell)
        elif group == "ANCHOR":
            anchor_cells.add(cell)
        else:
            other_cells.add(cell)

    print(f"  Top-{topk} cells partitioned: "
          f"INTRA={len(intra_cells)}  CROSS={len(cross_cells)}  "
          f"ANCHOR={len(anchor_cells)}  OTHER={len(other_cells)}  "
          f"total={len(all_cells)}")

    # Count unique heads per group
    intra_heads  = set((l, h) for l, h, _, _ in intra_cells)
    cross_heads  = set((l, h) for l, h, _, _ in cross_cells)
    anchor_heads = set((l, h) for l, h, _, _ in anchor_cells)
    other_heads  = set((l, h) for l, h, _, _ in other_cells)
    print(f"  Unique heads: INTRA={len(intra_heads)}  "
          f"CROSS={len(cross_heads)}  ANCHOR={len(anchor_heads)}  "
          f"OTHER={len(other_heads)}")

    # ── SSE ground truth ─────────────────────────────────────────────────
    print("  Computing full-sequence SSE ground truth...")
    full_sse_A = get_full_sse_preds(sequence_S)

    # ── Run conditions ───────────────────────────────────────────────────
    empty_cells: set[tuple[int, int, int, int]] = set()

    conditions = {
        # Sanity
        "none":            empty_cells,
        "full_circuit":    all_cells,
        # Ablate one group (keep rest)
        "–INTRA":          all_cells - intra_cells,
        "–CROSS":          all_cells - cross_cells,
        "–ANCHOR":         all_cells - anchor_cells,
        "–OTHER":          all_cells - other_cells,
        # Only one group (ablate rest)
        "only_INTRA":      intra_cells,
        "only_CROSS":      cross_cells,
        "only_ANCHOR":     anchor_cells,
        "only_OTHER":      other_cells,
    }

    results: dict[str, dict] = {}

    for cond_name, protected in conditions.items():
        print(f"\n  [{cond_name}] protected={len(protected)} cells ...")
        res = run_condition(
            protected_cells=protected,
            clean_inputs_BL=clean_inputs_BL,
            corrupt_attn_LBHLL=corrupt_attn_LBHLL,
            seg=seg,
            orig_contacts_AA=orig_contacts_AA,
            clean_metric=clean_metric_val,
            corrupt_metric=corrupt_metric_val,
            clean_flank=clean_flk,
            sequence_S=sequence_S,
            full_sse_A=full_sse_A,
        )
        results[cond_name] = res
        print(f"    contact={res['metric']:.4f}  faith={res['faithfulness']:.2%}  "
              f"sse_seg={res['seg_mean']:.3f}  sse_flk={res['flk_mean']:.3f}")

    clear_memory()

    # ── Summary table ────────────────────────────────────────────────────
    print(f"\n  {'='*92}")
    print(f"  SUMMARY — {protein}")
    print(f"  {'='*92}")
    print(f"  {'Condition':<16} {'#cells':>7} {'contact':>9} {'faith':>8} "
          f"{'ss1':>7} {'ss2':>7} {'seg_μ':>7} {'flkL':>7} {'flkR':>7} {'flk_μ':>7}")
    print(f"  {'─'*92}")

    # Print with visual separators between groups
    _groups = [
        ["none", "full_circuit"],
        ["–INTRA", "–CROSS", "–ANCHOR", "–OTHER"],
        ["only_INTRA", "only_CROSS", "only_ANCHOR", "only_OTHER"],
    ]
    for gi, group in enumerate(_groups):
        if gi > 0:
            print(f"  {'─'*92}")
        for cond_name in group:
            protected = conditions[cond_name]
            r = results[cond_name]
            def _fv(v): return f"{v:.3f}" if not np.isnan(v) else "  nan"
            print(f"  {cond_name:<16} {len(protected):>7} "
                  f"{r['metric']:>9.4f} {r['faithfulness']:>7.2%} "
                  f"{_fv(r['ss1_acc']):>7} {_fv(r['ss2_acc']):>7} {_fv(r['seg_mean']):>7} "
                  f"{_fv(r['flk_l_acc']):>7} {_fv(r['flk_r_acc']):>7} {_fv(r['flk_mean']):>7}")

    # ── Per-residue SSE comparison ───────────────────────────────────────
    print(f"\n  Per-residue SSE changes (full_circuit vs ablations):")

    _compare_conds = [c for c in conditions if c not in ("none", "full_circuit")]
    for cond_name in _compare_conds:
        full_detail = results["full_circuit"]["sse_detail"]
        abl_detail  = results[cond_name]["sse_detail"]
        flips = []

        for seg_name in ["ss1", "ss2", "flk_left", "flk_right"]:
            if seg_name not in full_detail or seg_name not in abl_detail:
                continue
            full_p = full_detail[seg_name]["preds"]
            abl_p  = abl_detail[seg_name]["preds"]
            gt     = full_detail[seg_name]["gt"]

            if seg_name == "ss1":
                base_pos = seg.ss1_start
            elif seg_name == "ss2":
                base_pos = seg.ss2_start
            elif seg_name == "flk_left":
                base_pos = max(0, seg.ss1_start - clean_flk)
            else:
                base_pos = seg.ss2_end

            for i in range(min(len(full_p), len(abl_p))):
                if full_p[i] != abl_p[i]:
                    pos = base_pos + i
                    flips.append((seg_name, pos, int(gt[i]),
                                  int(full_p[i]), int(abl_p[i])))

        if flips:
            lbl = {"flk_left": "flkL", "flk_right": "flkR"}.get
            print(f"\n    {cond_name}: {len(flips)} residue(s) changed")
            print(f"    {'Seg':<8} {'Pos':>5}  gt  full  abl")
            for seg_name, pos, gt_v, full_v, abl_v in flips[:20]:
                sn = lbl(seg_name, seg_name)
                print(f"    {sn:<8} {pos:>5}   "
                      f"{HEC[gt_v]}    {HEC[full_v]}     {HEC[abl_v]}")
            if len(flips) > 20:
                print(f"    ... and {len(flips) - 20} more")
        else:
            print(f"\n    {cond_name}: no SSE prediction changes")

    # ── Markdown report ──────────────────────────────────────────────────
    def _make_report() -> str:
        lines: list[str] = []
        a = lines.append

        a(f"# SSE Circuit Ablation: {protein}")
        a(f"")
        a(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}   "
          f"Model: {MODEL_NAME}")
        a(f"")

        a(f"## Hypothesis")
        a(f"")
        a(f"INTRA heads gather local SSE information within regions. "
          f"CROSS heads bridge the two contact sides. Ablating INTRA heads "
          f"should drop both contact and SSE accuracy. Ablating CROSS heads "
          f"should drop contact accuracy but preserve SSE accuracy.")
        a(f"")

        a(f"## Configuration")
        a(f"")
        a(f"| Parameter | Value |")
        a(f"|-----------|-------|")
        a(f"| Protein | {protein} |")
        a(f"| Contact pair | {tuple(cfg['contact_pair'])} |")
        a(f"| ss1 | [{seg.ss1_start}, {seg.ss1_end}) |")
        a(f"| ss2 | [{seg.ss2_start}, {seg.ss2_end}) |")
        a(f"| Clean flank | {clean_flk} |")
        a(f"| Corrupt flank | {corrupt_flk} |")
        a(f"| Top-K cells | {topk} |")
        a(f"")

        a(f"## Cell Partition")
        a(f"")
        a(f"| Group | Cells | Heads |")
        a(f"|-------|-------|-------|")
        a(f"| INTRA | {len(intra_cells)} | {len(intra_heads)} |")
        a(f"| CROSS | {len(cross_cells)} | {len(cross_heads)} |")
        a(f"| ANCHOR | {len(anchor_cells)} | {len(anchor_heads)} |")
        a(f"| OTHER | {len(other_cells)} | {len(other_heads)} |")
        a(f"| **Total** | **{len(all_cells)}** | "
          f"**{len(intra_heads | cross_heads | anchor_heads | other_heads)}** |")
        a(f"")

        # List which heads are in each group
        for grp_name, grp_heads in [("INTRA", intra_heads),
                                     ("CROSS", cross_heads),
                                     ("ANCHOR", anchor_heads),
                                     ("OTHER", other_heads)]:
            if grp_heads:
                sorted_h = sorted(grp_heads)
                a(f"**{grp_name} heads**: "
                  + ", ".join(f"L{l}H{h}" for l, h in sorted_h))
                a(f"")

        a(f"## Results")
        a(f"")
        a(f"### Baselines")
        a(f"")
        a(f"| | Value |")
        a(f"|---|---|")
        a(f"| Clean metric | {clean_metric_val:.4f} |")
        a(f"| Corrupt metric | {corrupt_metric_val:.4f} |")
        a(f"| Gap | {clean_metric_val - corrupt_metric_val:.4f} |")
        a(f"")

        a(f"### Ablation Conditions")
        a(f"")
        a(f"| Condition | #cells | contact | faith | "
          f"ss1 | ss2 | seg_mean | flkL | flkR | flk_mean |")
        a(f"|-----------|--------|---------|-------|"
          f"-----|-----|----------|------|------|----------|")
        for cond_name, protected in conditions.items():
            r = results[cond_name]
            def _fv(v): return f"{v:.3f}" if not np.isnan(v) else "nan"
            a(f"| {cond_name} | {len(protected)} | "
              f"{r['metric']:.4f} | {r['faithfulness']:.2%} | "
              f"{_fv(r['ss1_acc'])} | {_fv(r['ss2_acc'])} | "
              f"{_fv(r['seg_mean'])} | {_fv(r['flk_l_acc'])} | "
              f"{_fv(r['flk_r_acc'])} | {_fv(r['flk_mean'])} |")
        a(f"")

        a(f"### SSE Ground Truth")
        a(f"")
        gt_ss1 = full_sse_A[seg.ss1_start:seg.ss1_end]
        gt_ss2 = full_sse_A[seg.ss2_start:seg.ss2_end]
        a(f"| Segment | SSE |")
        a(f"|---------|-----|")
        a(f"| SS1 [{seg.ss1_start}:{seg.ss1_end}] | "
          f"`{''.join(HEC[p] for p in gt_ss1)}` |")
        a(f"| SS2 [{seg.ss2_start}:{seg.ss2_end}] | "
          f"`{''.join(HEC[p] for p in gt_ss2)}` |")
        a(f"")

        a(f"### Per-Residue SSE Changes")
        a(f"")
        _report_conds = [c for c in conditions if c not in ("none", "full_circuit")]
        for cond_name in _report_conds:
            a(f"#### {cond_name}")
            a(f"")

            full_detail = results["full_circuit"]["sse_detail"]
            abl_detail  = results[cond_name]["sse_detail"]
            flips = []

            for seg_name in ["ss1", "ss2", "flk_left", "flk_right"]:
                if seg_name not in full_detail or seg_name not in abl_detail:
                    continue
                full_p = full_detail[seg_name]["preds"]
                abl_p  = abl_detail[seg_name]["preds"]
                gt     = full_detail[seg_name]["gt"]

                if seg_name == "ss1":
                    base_pos = seg.ss1_start
                elif seg_name == "ss2":
                    base_pos = seg.ss2_start
                elif seg_name == "flk_left":
                    base_pos = max(0, seg.ss1_start - clean_flk)
                else:
                    base_pos = seg.ss2_end

                for i in range(min(len(full_p), len(abl_p))):
                    if full_p[i] != abl_p[i]:
                        pos = base_pos + i
                        flips.append((seg_name, pos, int(gt[i]),
                                      int(full_p[i]), int(abl_p[i])))

            if flips:
                lbl = {"flk_left": "flkL", "flk_right": "flkR"}
                a(f"| Seg | Pos | gt | full | abl |")
                a(f"|-----|-----|----|------|-----|")
                for seg_name, pos, gt_v, full_v, abl_v in flips:
                    sn = lbl.get(seg_name, seg_name)
                    a(f"| {sn} | {pos} | {HEC[gt_v]} | "
                      f"{HEC[full_v]} | {HEC[abl_v]} |")
            else:
                a(f"_(no SSE prediction changes)_")
            a(f"")

        a(f"## Interpretation")
        a(f"")

        # Auto-generate drop table for "remove one" conditions
        fc = results["full_circuit"]
        a(f"### Effect of removing each group (drop from full_circuit)")
        a(f"")
        a(f"| Removed | Contact drop | SSE seg drop |")
        a(f"|---------|-------------|-------------|")
        for grp in ["INTRA", "CROSS", "ANCHOR", "OTHER"]:
            r = results[f"–{grp}"]
            cd = fc["metric"]   - r["metric"]
            sd = fc["seg_mean"] - r["seg_mean"]
            a(f"| {grp} | {cd:+.4f} | {sd:+.3f} |")
        a(f"")

        a(f"### Sufficiency of each group alone (only_X)")
        a(f"")
        a(f"| Kept | Contact | Faith | SSE seg |")
        a(f"|------|---------|-------|---------|")
        for grp in ["INTRA", "CROSS", "ANCHOR", "OTHER"]:
            r = results[f"only_{grp}"]
            a(f"| {grp} | {r['metric']:.4f} | {r['faithfulness']:.2%} | "
              f"{r['seg_mean']:.3f} |")
        a(f"")

        # Hypothesis check
        sse_drop_intra = fc["seg_mean"] - results["–INTRA"]["seg_mean"]
        sse_drop_cross = fc["seg_mean"] - results["–CROSS"]["seg_mean"]
        if sse_drop_intra > sse_drop_cross + 0.05:
            a(f"**Consistent with hypothesis**: removing INTRA causes larger SSE "
              f"drop ({sse_drop_intra:+.3f}) than removing CROSS ({sse_drop_cross:+.3f}).")
        elif abs(sse_drop_intra - sse_drop_cross) <= 0.05:
            a(f"**Inconclusive**: removing INTRA and CROSS cause similar SSE drops "
              f"({sse_drop_intra:+.3f} vs {sse_drop_cross:+.3f}).")
        else:
            a(f"**Against hypothesis**: removing CROSS causes larger SSE drop "
              f"({sse_drop_cross:+.3f}) than removing INTRA ({sse_drop_intra:+.3f}).")
        a(f"")

        return "\n".join(lines)

    report_path = report_dir / f"{protein}_sse_circuit_ablation.md"
    report_path.write_text(_make_report())
    print(f"\n  Report: {report_path}")

print(f"\nDone. Processed {len(run_proteins)} protein(s).")
