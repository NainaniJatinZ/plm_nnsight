#!/usr/bin/env python3
"""Run the 2026-04-26 anchor HMM / locality experiment suite.

This script materializes the shared P50 set, then runs any subset of:
  - Experiment 0: exhaustive anchor-projection flank sweep
  - Experiment 1: Pfam/HMM mapping + within-family entropy analysis
  - Experiment 2: paired local masking ablations
  - Experiment 3: 3Di / AA anchor-window clustering

The implementation reuses the existing repo conventions and outputs, but keeps
the heavy stages cacheable and independently runnable.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import math
import os
import shutil
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-plm-nnsight")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import torch
from scipy.stats import binomtest, wilcoxon
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.metrics.pairwise import cosine_distances
from transformers import EsmForMaskedLM, EsmTokenizer

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REPORT_ROOT = ROOT / "reports" / "out2"
OUTPUT_DIR = REPORT_ROOT / "anchor_hmm"
PDB_DIR = DATA_DIR / "pdb"
FOLDSEEK_FA = DATA_DIR / "foldseek" / "all_3di.fa"
FOLDSEEK_TRANSFER_FA = DATA_DIR / "foldseek" / "v2" / "v2_3di.fa"
FOLDSEEK_BIN = ROOT / "foldseek" / "bin" / "foldseek"
AUDIT_CSV = ROOT / "reports" / "outputs" / "multi_protein" / "anchor_behavior_audit.csv"
SWEEP3B_CSV = REPORT_ROOT / "esm2_3b_flank_sweep" / "esm2_3b_flank_sweep_summary.csv"
INTERPRO_CACHE_DIR = REPORT_ROOT / "interpro_hmm"
STRUCT_TRANSFER_DIR = REPORT_ROOT / "structure_anchor_transfer_v2"
SEQ_JSON = DATA_DIR / "full_seq_dict.json"
SS_JSON = DATA_DIR / "ss_dict.json"
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
TARGET_LAYER = 10
TARGET_HEAD = 9
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
REFERENCE_PROTEIN = "2B61A"
MASK_TOKEN = "<mask>"
STANDARD_AA = "ACDEFGHIKLMNPQRSTVWY"
AA_TO_IDX = {aa: i for i, aa in enumerate(STANDARD_AA)}
DI_ALPHABET = STANDARD_AA
DI_TO_IDX = {c: i for i, c in enumerate(DI_ALPHABET)}
SIFTS_URL = "https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb}"
INTERPRO_ENTRIES_URL = (
    "https://www.ebi.ac.uk/interpro/api/entry/all/protein/uniprot/{acc}/?page_size=200"
)
INTERPRO_HMM_URL = "https://www.ebi.ac.uk/interpro/api/entry/{db}/{acc}?annotation=hmm"
HMM_DBS = {"pfam"}
BURIAL_RSA_TOL = 0.10

# Max ASA for RSA (Tien et al. 2013)
MAX_ASA = {
    "A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225, "G": 104,
    "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240, "P": 159, "S": 155,
    "T": 172, "W": 285, "Y": 263, "V": 174,
}

OUTCOME_MAP_MD = """# Outcome Map

## Experiment 1

- `H_anchor < H_random_in_domain` and below both matched controls in most Pfams:
  genuine domain-coordinate signal beyond burial/SSE.
- `H_anchor < H_random_in_domain` but approximately equals buried/SSE-matched:
  structural-feature / burial-class explanation.
- `H_anchor ≈ H_random_in_domain`:
  no strong Pfam-coordinate alignment.

## Experiment 2

- `|Δα_norm(C7)|` exceeds `C4/C5/C8`:
  high-IC amino-acid identities inside the local window matter.
- `C7 ≈ C4` or `C7 ≈ C5`:
  class-level structural feature explanation.
- `C7 ≈ C8`:
  no privileged role for high-IC residues.
- `C_anchor` should collapse the anchor signal; `C_far` should leave it close to baseline.

## Experiment 3

- `R_3Di` tracks structural labels and outperforms `R_AA`:
  structural-window signature supports the structural-feature story.
- both fail:
  window token information is insufficient.
- `R_AA` tracks Pfam strongly:
  amino-acid motif story resurfaces.
- `L_col` recovery in the 1PVGA / 2B61A homolog sets:
  consistency check with the prior structure-transfer result.
"""

RADIUS_SELECTION_NOTE_MD = """# Radius Selection Note

## Why `R=0` can look artificially good

In the fine-grained anchor-projection sweep, we found at least one protein
(`2QM0A`) where the projection curve is non-monotonic:

- `R=0`: anchor-position `alpha_norm` is already moderately high.
- `R=1..33`: the anchor-position projection drops sharply and stays low.
- `R=33->34`: the main recovery jump occurs.
- `R>=35`: the anchor projection recovers toward the full-sequence value.

This means the old `first radius where alpha_norm >= 0.5` summary can report
`R50 = 0` even when the meaningful local-window recovery happens much later.

Working hypothesis:

- with only the anchor residue left unmasked, attention and downstream
  projection can be artificially concentrated onto that lone visible residue;
- this inflates the anchor-position projection without implying that the true
  local context is unnecessary.

Operational change:

- keep `r50_first_crossing` as a diagnostic only;
- use `selected_radius`, defined from the recovery jump instead:
  first `delta alpha_norm >= jump_threshold`, otherwise the `argmax delta`
  fallback.

For `2QM0A`, this changes the interpretation from `R50 = 0` to
`selected_radius = 34`, which matches the visible recovery jump much better.
"""


@dataclass
class P50Row:
    protein: str
    anchor_pos: int
    top3_mass: float
    max_jump_delta: float
    jump_found: bool
    n_res: int


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    path.write_text(text)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def safe_read_csv(path: Path, **kwargs) -> pd.DataFrame:
    try:
        return pd.read_csv(path, **kwargs)
    except (pd.errors.EmptyDataError, FileNotFoundError):
        return pd.DataFrame()


def summarize_recovery_curve(norms: Iterable[float], jump_threshold: float) -> dict[str, float | int | str | None]:
    arr = np.array(list(norms), dtype=float)
    deltas = np.diff(arr)
    first_cross = next((r for r, value in enumerate(arr) if value >= 0.5), None)
    if len(deltas):
        jump_idx = int(np.nanargmax(deltas))
        jump_from = jump_idx
        jump_to = jump_idx + 1
        jump_delta = float(deltas[jump_idx])
        threshold_hits = np.flatnonzero(deltas >= jump_threshold)
        if len(threshold_hits):
            selected_radius = int(threshold_hits[0] + 1)
            selection_method = "first_delta_ge_threshold"
        else:
            selected_radius = jump_to
            selection_method = "argmax_delta_fallback"
    else:
        jump_from = jump_to = 0
        jump_delta = 0.0
        selected_radius = first_cross
        selection_method = "no_jump_available"
    return {
        "r50_first_crossing": first_cross,
        "jump_from_r": jump_from,
        "jump_to_r": jump_to,
        "jump_delta": jump_delta,
        "selected_radius": selected_radius,
        "selection_method": selection_method,
        "jump_threshold": jump_threshold,
        "alpha_norm_at_max_r": float(arr[-1]) if len(arr) else np.nan,
    }


def load_sequences() -> dict[str, str]:
    return load_json(SEQ_JSON)


def load_ss_dict() -> dict[str, str]:
    raw = load_json(SS_JSON)
    return {k.replace(".pdb", ""): v.replace("-", "C") for k, v in raw.items()}


def split_pdb_chain(pdb_chain: str) -> tuple[str, str]:
    if len(pdb_chain) < 5:
        raise ValueError(f"Expected 4-char PDB id + chain, got {pdb_chain!r}")
    return pdb_chain[:4].lower(), pdb_chain[4:]


def select_p50(limit: int = 50, top3_floor: float = 0.8) -> list[P50Row]:
    audit = pd.read_csv(AUDIT_CSV)
    seqs = load_sequences()
    audit = audit[audit["protein"].isin(seqs.keys())]
    filt = audit[audit["top3_mass"] >= top3_floor].copy()
    filt = filt.sort_values("top3_mass", ascending=False).head(limit)
    out = [
        P50Row(
            protein=row.protein,
            anchor_pos=int(row.top_key_idx),
            top3_mass=float(row.top3_mass),
            max_jump_delta=float("nan"),
            jump_found=False,
            n_res=int(row.n_res),
        )
        for row in filt.itertuples(index=False)
    ]
    return out


def save_p50_manifest(p50: list[P50Row], out_dir: Path) -> Path:
    ensure_dir(out_dir)
    path = out_dir / "p50_manifest.csv"
    pd.DataFrame([r.__dict__ for r in p50]).to_csv(path, index=False)
    return path


def load_model(device: str) -> tuple[EsmForMaskedLM, EsmTokenizer]:
    os.environ["HF_HOME"] = WEIGHTS_DIR
    tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR, local_files_only=True)
    model = EsmForMaskedLM.from_pretrained(
        MODEL_NAME,
        cache_dir=WEIGHTS_DIR,
        attn_implementation="eager",
        local_files_only=True,
    ).to(device).eval()
    return model, tokenizer


def extract_head_weights(model: EsmForMaskedLM, layer: int, head: int) -> dict[str, torch.Tensor]:
    attn = model.esm.encoder.layer[layer].attention
    w_q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    w_k = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_k = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    return {
        "W_Q_hd": w_q[head].clone(),
        "b_Q_d": b_q[head].clone(),
        "W_K_hd": w_k[head].clone(),
        "b_K_d": b_k[head].clone(),
    }


def capture_layernorm_outputs(
    model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    sequences: list[str],
    device: str,
    batch_size: int,
) -> list[torch.Tensor]:
    layernorm = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    outputs: list[torch.Tensor] = []
    captured: list[torch.Tensor] = []

    def hook(_module, _inp, out):
        captured.append(out.detach().cpu())

    handle = layernorm.register_forward_hook(hook)
    try:
        for i in range(0, len(sequences), batch_size):
            batch = sequences[i:i + batch_size]
            captured.clear()
            inputs = tokenizer(batch, return_tensors="pt", padding=True).to(device)
            with torch.no_grad():
                _ = model(**inputs)
            batch_ln = captured[-1][:, 1:-1, :]
            outputs.extend([batch_ln[j] for j in range(batch_ln.shape[0])])
    finally:
        handle.remove()
    return outputs


def compute_search_dir(
    model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    sequence: str,
    weights: dict[str, torch.Tensor],
    device: str,
) -> torch.Tensor:
    x_ln = capture_layernorm_outputs(model, tokenizer, [sequence], device=device, batch_size=1)[0]
    q_all = x_ln @ weights["W_Q_hd"].T + weights["b_Q_d"]
    q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean = q_mean / q_mean.norm().clamp(min=1e-8)
    return weights["W_K_hd"].T @ q_mean


def build_masked_sequence(sequence: str, anchor_pos: int, radius: int) -> str:
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = [sequence[i] if lo <= i <= hi else MASK_TOKEN for i in range(n)]
    return " ".join(chars)


def project_batch_at_positions(
    model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    sequences: list[str],
    positions: list[int],
    d_unit: torch.Tensor,
    device: str,
    batch_size: int,
) -> tuple[list[float], list[int]]:
    ln_outputs = capture_layernorm_outputs(model, tokenizer, sequences, device=device, batch_size=batch_size)
    scores = []
    argmax_pos = []
    d_cpu = d_unit.cpu()
    for x_ln, pos in zip(ln_outputs, positions):
        proj = x_ln @ d_cpu
        scores.append(float(proj[pos]))
        argmax_pos.append(int(torch.argmax(proj).item()))
    return scores, argmax_pos


def run_experiment_0(
    p50: list[P50Row],
    seqs: dict[str, str],
    out_dir: Path,
    model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    d_unit: torch.Tensor,
    device: str,
    max_flank: int,
    batch_size: int,
    jump_threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_dir(out_dir)
    rows: list[dict] = []
    summary_rows: list[dict] = []
    for i, p in enumerate(p50, start=1):
        seq = seqs[p.protein]
        full_seq = " ".join(seq)
        masked = [build_masked_sequence(seq, p.anchor_pos, r) for r in range(max_flank + 1)]
        alpha_full = project_batch_at_positions(
            model, tokenizer, [full_seq], [p.anchor_pos], d_unit, device=device, batch_size=1
        )[0][0]
        alpha_vals, argmax_positions = project_batch_at_positions(
            model,
            tokenizer,
            masked,
            [p.anchor_pos] * len(masked),
            d_unit,
            device=device,
            batch_size=batch_size,
        )
        norms = []
        for r, alpha_r in enumerate(alpha_vals):
            alpha_norm = alpha_r / alpha_full if abs(alpha_full) > 1e-8 else np.nan
            norms.append(alpha_norm)
            rows.append(
                {
                    "protein": p.protein,
                    "anchor_pos": p.anchor_pos,
                    "radius": r,
                    "alpha": alpha_r,
                    "alpha_full": alpha_full,
                    "alpha_norm": alpha_norm,
                    "argmax_pos": argmax_positions[r],
                }
            )
        curve_summary = summarize_recovery_curve(norms, jump_threshold=jump_threshold)
        summary_rows.append(
            {
                "protein": p.protein,
                "anchor_pos": p.anchor_pos,
                "alpha_full": alpha_full,
                **curve_summary,
            }
        )
        print(
            f"[exp0 {i}/{len(p50)}] {p.protein}: alpha_full={alpha_full:.4f}, "
            f"first_cross={curve_summary['r50_first_crossing']}, "
            f"selected_radius={curve_summary['selected_radius']}, "
            f"jump={curve_summary['jump_from_r']}->{curve_summary['jump_to_r']} "
            f"({curve_summary['jump_delta']:.4f})",
            flush=True,
        )

    per_protein = pd.DataFrame(rows)
    summary = pd.DataFrame(summary_rows)
    per_protein.to_csv(out_dir / "per_protein.csv", index=False)
    summary.to_csv(out_dir / "summary.csv", index=False)

    n_plot = min(12, len(summary_rows))
    if n_plot:
        fig, axes = plt.subplots(n_plot, 1, figsize=(8, max(3.0 * n_plot, 4.0)), sharex=True)
        if n_plot == 1:
            axes = [axes]
        for ax, protein in zip(axes, summary["protein"].head(n_plot)):
            sub = per_protein[per_protein["protein"] == protein]
            ax.plot(sub["radius"], sub["alpha_norm"], marker="o", ms=2.5, lw=1.5)
            ax.axhline(0.5, color="#999999", ls="--", lw=0.8)
            ax.set_title(protein)
            ax.set_ylabel("alpha_norm")
            ax.grid(alpha=0.2)
        axes[-1].set_xlabel("radius")
        fig.tight_layout()
        fig.savefig(out_dir / "alpha_norm_curves.png", dpi=180, bbox_inches="tight")
        plt.close(fig)
    return per_protein, summary


def sifts_uniprot(pdb_id: str, chain: str) -> str:
    r = requests.get(SIFTS_URL.format(pdb=pdb_id), timeout=30)
    r.raise_for_status()
    data = r.json().get(pdb_id, {}).get("UniProt", {})
    candidates: list[tuple[str, int]] = []
    for acc, info in data.items():
        for m in info.get("mappings", []):
            if m.get("chain_id") == chain:
                span = max(0, int(m["unp_end"]) - int(m["unp_start"]) + 1)
                candidates.append((acc, span))
    if not candidates:
        raise RuntimeError(f"No UniProt mapping for {pdb_id}{chain}")
    candidates.sort(key=lambda x: -x[1])
    return candidates[0][0]


def interpro_entries(uniprot_acc: str) -> dict:
    r = requests.get(INTERPRO_ENTRIES_URL.format(acc=uniprot_acc), timeout=60)
    r.raise_for_status()
    return r.json()


def download_hmm(db: str, acc: str) -> bytes:
    r = requests.get(INTERPRO_HMM_URL.format(db=db, acc=acc), timeout=60)
    r.raise_for_status()
    raw = r.content
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def collect_hmm_signatures(entries: dict) -> list[dict]:
    out: list[dict] = []
    for entry in entries.get("results", []):
        meta = entry["metadata"]
        proteins = entry.get("proteins", [])
        if not proteins:
            continue
        locations = []
        for loc in proteins[0].get("entry_protein_locations", []) or []:
            for frag in loc.get("fragments", []):
                locations.append((int(frag["start"]), int(frag["end"])))
        src = meta["source_database"].lower()
        if src in HMM_DBS:
            out.append(
                {
                    "db": src,
                    "accession": meta["accession"],
                    "name": meta.get("name") or meta["accession"],
                    "interpro_parent": meta.get("integrated"),
                    "locations": locations,
                }
            )
        elif src == "interpro":
            for mdb, members in (meta.get("member_databases") or {}).items():
                if mdb.lower() not in HMM_DBS:
                    continue
                for macc, mname in members.items():
                    out.append(
                        {
                            "db": mdb.lower(),
                            "accession": macc,
                            "name": mname,
                            "interpro_parent": meta["accession"],
                            "locations": locations,
                        }
                    )
    deduped = {}
    for sig in out:
        deduped.setdefault((sig["db"], sig["accession"]), sig)
    return list(deduped.values())


def hmmalign_sequence(hmm_bytes: bytes, seq_name: str, seq: str) -> tuple[bytes, bytes, int]:
    import pyhmmer

    with pyhmmer.plan7.HMMFile(io.BytesIO(hmm_bytes)) as hf:
        hmm = hf.read()
    digital = pyhmmer.easel.TextSequence(name=seq_name.encode(), sequence=seq).digitize(hmm.alphabet)
    msa = pyhmmer.hmmer.hmmalign(hmm, [digital])
    sto_buf = io.BytesIO()
    msa.write(sto_buf, format="stockholm")
    a2m_buf = io.BytesIO()
    msa.write(a2m_buf, format="a2m")
    return sto_buf.getvalue(), a2m_buf.getvalue(), int(hmm.M)


def read_hmm_state_ic(hmm_path: Path) -> dict[int, float]:
    from pyhmmer.plan7 import HMMFile

    with HMMFile(hmm_path) as hf:
        hmm = hf.read()
    me = hmm.match_emissions
    out = {}
    log20 = math.log2(20.0)
    for state in range(1, int(hmm.M) + 1):
        probs = np.array(list(me[state]), dtype=float)
        probs = probs[probs > 0]
        entropy = float(-(probs * np.log2(probs)).sum())
        out[state] = log20 - entropy
    return out


def parse_stockholm_mapping(sto_path: Path) -> tuple[dict[int, int], list[str]]:
    lines = sto_path.read_text().splitlines()
    seq_parts: list[str] = []
    rf_parts: list[str] = []
    for line in lines:
        if not line or line.startswith("# STOCKHOLM") or line == "//":
            continue
        if line.startswith("#=GC RF"):
            rf_parts.append(line.split(None, 2)[-1].strip())
        elif line.startswith("#"):
            continue
        else:
            toks = line.split()
            if len(toks) >= 2:
                seq_parts.append(toks[1].strip())
    aligned_seq = "".join(seq_parts)
    rf = "".join(rf_parts)
    mapping: dict[int, int] = {}
    seq_pos = 0
    hmm_state = 0
    aligned_chars: list[str] = []
    for char, rf_char in zip(aligned_seq, rf):
        is_match = rf_char != "."
        if is_match:
            hmm_state += 1
        if char != "-":
            if is_match:
                mapping[seq_pos] = hmm_state
            seq_pos += 1
            aligned_chars.append(char)
    return mapping, aligned_chars


def parse_pfam_summary(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rows.append(row)
    return rows


def maybe_run_interpro_annotation(protein: str, sequence: str, out_root: Path) -> Path:
    out_dir = out_root / protein
    hmms_dir = out_dir / "hmms"
    aln_dir = out_dir / "alignments"
    summary_path = out_dir / "pfam_summary.tsv"
    if summary_path.exists() and any(aln_dir.glob("*.sto")) and any(hmms_dir.glob("*.hmm")):
        return out_dir

    ensure_dir(hmms_dir)
    ensure_dir(aln_dir)
    pdb_id, chain = split_pdb_chain(protein)
    uniprot = sifts_uniprot(pdb_id, chain)
    entries = interpro_entries(uniprot)
    write_text(out_dir / "annotations.json", json.dumps(entries, indent=2))
    sigs = [s for s in collect_hmm_signatures(entries) if s["db"] == "pfam"]
    summary_rows = [[
        "db", "accession", "name", "interpro_parent", "locations", "hmm_M", "align_path", "uniprot",
    ]]
    for sig in sigs:
        hmm_bytes = download_hmm(sig["db"], sig["accession"])
        hmm_path = hmms_dir / f"{sig['accession']}.hmm"
        hmm_path.write_bytes(hmm_bytes)
        sto, _a2m, hmm_m = hmmalign_sequence(hmm_bytes, protein, sequence)
        sto_path = aln_dir / f"{sig['accession']}.sto"
        sto_path.write_bytes(sto)
        loc_str = ";".join(f"{a}-{b}" for a, b in sig["locations"]) or "-"
        summary_rows.append(
            [
                sig["db"],
                sig["accession"],
                sig["name"],
                sig.get("interpro_parent") or "-",
                loc_str,
                str(hmm_m),
                str(sto_path.relative_to(out_dir)),
                uniprot,
            ]
        )
        time.sleep(0.2)
    with summary_path.open("w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(summary_rows)
    return out_dir


def read_structure(parser_kind: str, path: Path):
    if parser_kind == "pdb":
        from Bio.PDB import PDBParser

        parser = PDBParser(QUIET=True)
    else:
        from Bio.PDB import MMCIFParser

        parser = MMCIFParser(QUIET=True)
    return parser.get_structure(path.stem, str(path))


def get_structure_chain(protein_or_pdb: str, chain_id: str | None = None):
    if len(protein_or_pdb) >= 5 and chain_id is None:
        pdb4 = protein_or_pdb[:4].lower()
        chain_id = protein_or_pdb[4]
    else:
        pdb4 = protein_or_pdb[:4].lower()
    pdb_candidates = [
        PDB_DIR / f"{pdb4}.pdb",
        PDB_DIR / f"{pdb4.upper()}.pdb",
    ]
    cif_candidates = [
        PDB_DIR / f"{pdb4}.cif",
        PDB_DIR / f"{pdb4.upper()}.cif",
    ]
    pdb_path = next((path for path in pdb_candidates if path.exists()), None)
    cif_path = next((path for path in cif_candidates if path.exists()), None)
    if pdb_path is not None:
        structure = read_structure("pdb", pdb_path)
    elif cif_path is not None:
        structure = read_structure("cif", cif_path)
    else:
        raise FileNotFoundError(f"No PDB/CIF for {pdb4}")
    model = next(structure.get_models())
    if chain_id is not None and chain_id in model:
        chain = model[chain_id]
    else:
        chain = next(model.get_chains())
    return structure, chain


def get_struct_seq(pdb4: str, chain_id: str) -> str:
    from Bio import PDB

    structure, chain = get_structure_chain(pdb4, chain_id)
    seq = []
    for res in chain:
        if PDB.is_aa(res, standard=True):
            try:
                from Bio.PDB.Polypeptide import index_to_one, three_to_index

                seq.append(index_to_one(three_to_index(res.get_resname())))
            except Exception:
                seq.append("X")
    return "".join(seq)


def build_full_to_struct_map(full_seq: str, struct_seq: str) -> dict[int, int]:
    from Bio.Align import PairwiseAligner

    aligner = PairwiseAligner()
    aligner.mode = "global"
    aligner.open_gap_score = -5.0
    aligner.extend_gap_score = -0.5
    aln = aligner.align(full_seq, struct_seq)[0]
    coords = aln.coordinates
    mapping = {}
    for k in range(coords.shape[1] - 1):
        f0, f1 = int(coords[0, k]), int(coords[0, k + 1])
        s0, s1 = int(coords[1, k]), int(coords[1, k + 1])
        if f1 - f0 == s1 - s0 > 0:
            for df, ds in zip(range(f0, f1), range(s0, s1)):
                mapping[df] = ds
    return mapping


def compute_rsa_map(protein: str, full_seq: str) -> dict[int, float] | None:
    from Bio import PDB
    from Bio.PDB import ShrakeRupley

    try:
        structure, chain = get_structure_chain(protein)
    except Exception:
        return None
    struct_seq = []
    ordered_res = []
    for res in chain:
        if PDB.is_aa(res, standard=True):
            try:
                from Bio.PDB.Polypeptide import index_to_one, three_to_index

                aa = index_to_one(three_to_index(res.get_resname()))
            except Exception:
                aa = "X"
            struct_seq.append(aa)
            ordered_res.append(res)
    struct_seq_s = "".join(struct_seq)
    try:
        mapping = build_full_to_struct_map(full_seq, struct_seq_s)
    except Exception:
        return None
    if not mapping:
        return None
    sr = ShrakeRupley()
    try:
        sr.compute(next(structure.get_models()), level="R")
    except Exception:
        return None
    rsa_map = {}
    rev = {v: k for k, v in mapping.items()}
    for struct_pos, res in enumerate(ordered_res):
        seq_pos = rev.get(struct_pos)
        if seq_pos is None:
            continue
        aa = full_seq[seq_pos]
        max_asa = MAX_ASA.get(aa, 200.0)
        sasa = float(getattr(res, "sasa", 0.0))
        rsa_map[seq_pos] = min(sasa / max_asa, 1.0) if max_asa > 0 else 0.0
    return rsa_map


def entropy_metrics(states: list[int], m_states: int) -> dict[str, float]:
    if not states or m_states <= 1:
        return {"entropy": np.nan, "h_norm": np.nan, "top1_conc": np.nan, "top3_conc": np.nan}
    counts = np.bincount(np.array(states, dtype=int), minlength=m_states + 1)[1:]
    total = counts.sum()
    probs = counts[counts > 0] / max(total, 1)
    entropy = float(-(probs * np.log(probs)).sum())
    top = np.sort(counts)[::-1]
    return {
        "entropy": entropy,
        "h_norm": entropy / math.log(m_states),
        "top1_conc": float(top[:1].sum() / total),
        "top3_conc": float(top[:3].sum() / total),
    }


def sample_control_states(
    positions: list[int],
    state_by_pos: dict[int, int],
    rsa_map: dict[int, float] | None,
    sse_str: str | None,
    anchor_pos: int,
    anchor_rsa: float | None,
    anchor_sse: str | None,
    mode: str,
    rng: np.random.Generator,
) -> int | None:
    candidates: list[int] = []
    for pos in positions:
        if pos == anchor_pos or pos not in state_by_pos:
            continue
        if mode == "random_in_domain":
            candidates.append(pos)
        elif mode == "buried_matched":
            if rsa_map is not None and anchor_rsa is not None and pos in rsa_map and abs(rsa_map[pos] - anchor_rsa) <= BURIAL_RSA_TOL:
                candidates.append(pos)
        elif mode == "sse_matched":
            if sse_str is not None and anchor_sse is not None and pos < len(sse_str) and sse_str[pos] == anchor_sse:
                candidates.append(pos)
        else:
            raise ValueError(mode)
    if not candidates:
        return None
    choice = int(rng.choice(candidates))
    return state_by_pos[choice]


def build_anchor_pfam_label(mapping_df: pd.DataFrame) -> pd.DataFrame:
    if mapping_df.empty:
        return pd.DataFrame(columns=["protein", "anchor_pfam"])
    anchor_hits = mapping_df[mapping_df["is_anchor"] == True].copy()
    if anchor_hits.empty:
        return pd.DataFrame(columns=["protein", "anchor_pfam"])
    anchor_hits["span_len"] = anchor_hits["loc_end"] - anchor_hits["loc_start"]
    anchor_hits = anchor_hits.sort_values(["protein", "span_len", "pfam_acc"])
    best = anchor_hits.groupby("protein", as_index=False).first()
    return best[["protein", "pfam_acc"]].rename(columns={"pfam_acc": "anchor_pfam"})


def run_experiment_1(
    p50: list[P50Row],
    seqs: dict[str, str],
    ss_dict: dict[str, str],
    out_dir: Path,
    annotation_root: Path,
    n_control_resamples: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_dir(out_dir)
    mapping_rows: list[dict] = []
    rsa_cache: dict[str, dict[int, float] | None] = {}
    failures: list[dict[str, str]] = []
    for i, p in enumerate(p50, start=1):
        seq = seqs[p.protein]
        try:
            ann_dir = maybe_run_interpro_annotation(p.protein, seq, annotation_root)
        except Exception as exc:
            failures.append({"protein": p.protein, "error": f"{type(exc).__name__}: {exc}"})
            print(f"[exp1 annotate {i}/{len(p50)}] {p.protein}: FAILED: {exc}", flush=True)
            continue
        rsa_cache[p.protein] = compute_rsa_map(p.protein, seq)
        summary_rows = parse_pfam_summary(ann_dir / "pfam_summary.tsv")
        for srow in summary_rows:
            pfam_acc = srow["accession"]
            sto_path = ann_dir / srow["align_path"]
            hmm_path = ann_dir / "hmms" / f"{pfam_acc}.hmm"
            if not sto_path.exists() or not hmm_path.exists():
                continue
            state_map, _aligned = parse_stockholm_mapping(sto_path)
            state_ic = read_hmm_state_ic(hmm_path)
            loc_tokens = [] if srow["locations"] == "-" else srow["locations"].split(";")
            bounds = []
            for token in loc_tokens:
                if "-" in token:
                    a, b = token.split("-", 1)
                    bounds.append((int(a) - 1, int(b) - 1))
            loc_start = min((a for a, _ in bounds), default=None)
            loc_end = max((b for _, b in bounds), default=None)
            anchor_inside = False
            for seq_pos, hmm_state in state_map.items():
                in_span = loc_start is not None and loc_end is not None and loc_start <= seq_pos <= loc_end
                is_anchor = seq_pos == p.anchor_pos
                if is_anchor and hmm_state is not None:
                    anchor_inside = True
                mapping_rows.append(
                    {
                        "protein": p.protein,
                        "pfam_acc": pfam_acc,
                        "pfam_name": srow["name"],
                        "uniprot": srow.get("uniprot", ""),
                        "seq_pos": seq_pos,
                        "aa": seq[seq_pos],
                        "hmm_state": hmm_state,
                        "state_ic": state_ic.get(hmm_state, np.nan),
                        "anchor_pos": p.anchor_pos,
                        "is_anchor": is_anchor,
                        "anchor_inside_pfam": anchor_inside,
                        "loc_start": loc_start,
                        "loc_end": loc_end,
                        "in_span": in_span,
                    }
                )
        print(f"[exp1 annotate {i}/{len(p50)}] {p.protein}", flush=True)

    mapping_df = pd.DataFrame(mapping_rows)
    mapping_tsv = out_dir / "anchor_hmm_mapping.tsv"
    mapping_df.to_csv(mapping_tsv, sep="\t", index=False)
    if failures:
        pd.DataFrame(failures).to_csv(out_dir / "annotation_failures.csv", index=False)

    per_pfam_rows: list[dict] = []
    plots_dir = out_dir / "plots"
    ensure_dir(plots_dir)
    grouped = mapping_df.groupby("pfam_acc")
    for pfam_acc, g in grouped:
        anchor_states = []
        proteins = []
        m_states = int(g["hmm_state"].max()) if not g["hmm_state"].isna().all() else 0
        for protein, gp in g.groupby("protein"):
            anchor_row = gp[gp["is_anchor"] == True]
            if anchor_row.empty:
                continue
            state = int(anchor_row["hmm_state"].iloc[0])
            if state <= 0:
                continue
            anchor_states.append(state)
            proteins.append(protein)
        if len(anchor_states) < 5:
            continue
        anchor_metrics = entropy_metrics(anchor_states, m_states)
        control_stats: dict[str, list[float]] = defaultdict(list)
        control_top1: dict[str, list[float]] = defaultdict(list)
        control_top3: dict[str, list[float]] = defaultdict(list)
        usable_counts: dict[str, list[int]] = defaultdict(list)
        rng = np.random.default_rng(42)
        for mode in ("random_in_domain", "buried_matched", "sse_matched"):
            for _ in range(n_control_resamples):
                sampled_states = []
                for protein in proteins:
                    gp = g[g["protein"] == protein]
                    state_by_pos = {int(r.seq_pos): int(r.hmm_state) for r in gp.itertuples(index=False)}
                    positions = [int(x) for x in gp["seq_pos"].tolist()]
                    anchor_pos = int(gp["anchor_pos"].iloc[0])
                    anchor_rsa = rsa_cache.get(protein, {}).get(anchor_pos) if rsa_cache.get(protein) else None
                    sse_str = ss_dict.get(protein)
                    anchor_sse = sse_str[anchor_pos] if sse_str and anchor_pos < len(sse_str) else None
                    sampled = sample_control_states(
                        positions=positions,
                        state_by_pos=state_by_pos,
                        rsa_map=rsa_cache.get(protein),
                        sse_str=sse_str,
                        anchor_pos=anchor_pos,
                        anchor_rsa=anchor_rsa,
                        anchor_sse=anchor_sse,
                        mode=mode,
                        rng=rng,
                    )
                    if sampled is not None:
                        sampled_states.append(sampled)
                usable_counts[mode].append(len(sampled_states))
                metrics = entropy_metrics(sampled_states, m_states)
                control_stats[mode].append(metrics["h_norm"])
                control_top1[mode].append(metrics["top1_conc"])
                control_top3[mode].append(metrics["top3_conc"])

        row = {
            "pfam_acc": pfam_acc,
            "pfam_name": g["pfam_name"].iloc[0],
            "n_anchor_proteins": len(anchor_states),
            "m_states": m_states,
            "anchor_entropy": anchor_metrics["entropy"],
            "anchor_h_norm": anchor_metrics["h_norm"],
            "anchor_top1_conc": anchor_metrics["top1_conc"],
            "anchor_top3_conc": anchor_metrics["top3_conc"],
        }
        for mode, prefix in {
            "random_in_domain": "random",
            "buried_matched": "buried",
            "sse_matched": "sse",
        }.items():
            vals = np.array(control_stats[mode], dtype=float)
            row[f"{prefix}_h_norm_mean"] = float(np.nanmean(vals)) if len(vals) else np.nan
            row[f"{prefix}_h_norm_ci_lo"] = float(np.nanpercentile(vals, 2.5)) if len(vals) else np.nan
            row[f"{prefix}_h_norm_ci_hi"] = float(np.nanpercentile(vals, 97.5)) if len(vals) else np.nan
            row[f"{prefix}_top1_conc_mean"] = float(np.nanmean(control_top1[mode])) if len(control_top1[mode]) else np.nan
            row[f"{prefix}_top3_conc_mean"] = float(np.nanmean(control_top3[mode])) if len(control_top3[mode]) else np.nan
            row[f"{prefix}_n_mean"] = float(np.mean(usable_counts[mode])) if usable_counts[mode] else np.nan
            row[f"{prefix}_empirical_p"] = float(np.mean(vals <= anchor_metrics["h_norm"])) if len(vals) else np.nan
        per_pfam_rows.append(row)

        fig, ax = plt.subplots(figsize=(7, 4))
        labels = ["anchor", "random", "buried", "sse"]
        means = [
            anchor_metrics["h_norm"],
            row["random_h_norm_mean"],
            row["buried_h_norm_mean"],
            row["sse_h_norm_mean"],
        ]
        errs_lo = [
            0.0,
            row["random_h_norm_mean"] - row["random_h_norm_ci_lo"],
            row["buried_h_norm_mean"] - row["buried_h_norm_ci_lo"],
            row["sse_h_norm_mean"] - row["sse_h_norm_ci_lo"],
        ]
        errs_hi = [
            0.0,
            row["random_h_norm_ci_hi"] - row["random_h_norm_mean"],
            row["buried_h_norm_ci_hi"] - row["buried_h_norm_mean"],
            row["sse_h_norm_ci_hi"] - row["sse_h_norm_mean"],
        ]
        means = [0.0 if m is None or (isinstance(m, float) and np.isnan(m)) else m for m in means]
        errs_lo = [max(0.0, 0.0 if e is None or (isinstance(e, float) and np.isnan(e)) else e) for e in errs_lo]
        errs_hi = [max(0.0, 0.0 if e is None or (isinstance(e, float) and np.isnan(e)) else e) for e in errs_hi]
        ax.bar(labels, means, color=["#4c78a8", "#9ecae9", "#59a14f", "#e15759"])
        ax.errorbar(labels[1:], means[1:], yerr=[errs_lo[1:], errs_hi[1:]], fmt="none", color="black", lw=1)
        ax.set_ylim(0, 1.05)
        ax.set_ylabel("normalized entropy")
        ax.set_title(f"{pfam_acc}: anchor vs controls")
        fig.tight_layout()
        fig.savefig(plots_dir / f"{pfam_acc}_entropy.png", dpi=160, bbox_inches="tight")
        plt.close(fig)

    per_pfam_df = pd.DataFrame(per_pfam_rows)
    if not per_pfam_df.empty and "n_anchor_proteins" in per_pfam_df.columns:
        per_pfam_df = per_pfam_df.sort_values("n_anchor_proteins", ascending=False)
    per_pfam_df.to_csv(out_dir / "per_pfam_entropy.csv", index=False)

    meta_rows = []
    for control_prefix in ("random", "buried", "sse"):
        needed_cols = {"anchor_h_norm", f"{control_prefix}_h_norm_mean"}
        if needed_cols.issubset(per_pfam_df.columns):
            valid = per_pfam_df.dropna(subset=list(needed_cols))
        else:
            valid = pd.DataFrame()
        if len(valid):
            wins = int((valid["anchor_h_norm"] < valid[f"{control_prefix}_h_norm_mean"]).sum())
            meta_p = binomtest(wins, n=len(valid), p=0.5).pvalue
        else:
            wins = 0
            meta_p = np.nan
        meta_rows.append(
            {
                "control": control_prefix,
                "n_pfams": int(len(valid)),
                "anchor_lower_count": wins,
                "sign_test_p": meta_p,
            }
        )
    pd.DataFrame(meta_rows).to_csv(out_dir / "meta_sign_test.csv", index=False)
    return mapping_df, per_pfam_df


def choose_top_k_positions(
    candidates: list[tuple[int, float]],
    k: int,
    reverse: bool = True,
) -> list[int]:
    ordered = sorted(candidates, key=lambda x: x[1], reverse=reverse)
    return [pos for pos, _score in ordered[:k]]


def build_local_window_sequence(
    sequence: str,
    anchor_pos: int,
    radius: int,
    unmask_far_positions: set[int] | None = None,
    extra_mask_positions: set[int] | None = None,
) -> str:
    n = len(sequence)
    lo = max(0, anchor_pos - radius)
    hi = min(n - 1, anchor_pos + radius)
    chars = []
    extra_mask_positions = extra_mask_positions or set()
    unmask_far_positions = unmask_far_positions or set()
    for i in range(n):
        keep = lo <= i <= hi or i in unmask_far_positions
        if i in extra_mask_positions:
            keep = False
        chars.append(sequence[i] if keep else MASK_TOKEN)
    return " ".join(chars)


def derive_selected_radius_for_condition(
    sequence: str,
    anchor_pos: int,
    base_radius: int,
    unmask_far_positions: set[int],
    extra_mask_positions: set[int],
    model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    d_unit: torch.Tensor,
    alpha_full: float,
    device: str,
    batch_size: int,
    jump_threshold: float,
) -> tuple[int | None, int | None]:
    lo = max(0, base_radius - 5)
    hi = base_radius + 5
    seqs = [
        build_local_window_sequence(
            sequence,
            anchor_pos=anchor_pos,
            radius=r,
            unmask_far_positions=unmask_far_positions,
            extra_mask_positions={pos for pos in extra_mask_positions if abs(pos - anchor_pos) <= r},
        )
        for r in range(lo, hi + 1)
    ]
    alpha_vals, _argmax = project_batch_at_positions(
        model,
        tokenizer,
        seqs,
        [anchor_pos] * len(seqs),
        d_unit,
        device=device,
        batch_size=batch_size,
    )
    norms = [alpha / alpha_full if abs(alpha_full) > 1e-8 else np.nan for alpha in alpha_vals]
    summary = summarize_recovery_curve(norms, jump_threshold=jump_threshold)
    first_cross = summary["r50_first_crossing"]
    selected_local = summary["selected_radius"]
    absolute_selected = None if selected_local is None else int(lo + int(selected_local))
    absolute_first_cross = None if first_cross is None else int(lo + int(first_cross))
    return absolute_selected, absolute_first_cross


def run_experiment_2(
    p50: list[P50Row],
    seqs: dict[str, str],
    mapping_df: pd.DataFrame,
    exp0_summary: pd.DataFrame,
    ss_dict: dict[str, str],
    out_dir: Path,
    model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    d_unit: torch.Tensor,
    device: str,
    batch_size: int,
    n_random_resamples: int,
    jump_threshold: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_dir(out_dir)
    anchor_label_df = build_anchor_pfam_label(mapping_df)
    mapping_df = mapping_df.merge(anchor_label_df, on="protein", how="left")
    exp0_lookup = {row.protein: row for row in exp0_summary.itertuples(index=False)}
    rows: list[dict] = []
    for i, p in enumerate(p50, start=1):
        if p.protein not in exp0_lookup:
            continue
        seq = seqs[p.protein]
        exp0_row = exp0_lookup[p.protein]
        radius = getattr(exp0_row, "selected_radius", None)
        if radius is None or pd.isna(radius):
            radius = 30
        radius = int(radius)
        window = [pos for pos in range(max(0, p.anchor_pos - radius), min(len(seq), p.anchor_pos + radius + 1))]
        k = min(8, max(1, int(0.25 * len(window))))
        full_seq = " ".join(seq)
        alpha_full = project_batch_at_positions(
            model, tokenizer, [full_seq], [p.anchor_pos], d_unit, device=device, batch_size=1
        )[0][0]
        c0_seq = build_local_window_sequence(seq, p.anchor_pos, radius, set(), set())
        c0_alpha, c0_argmax = project_batch_at_positions(
            model, tokenizer, [c0_seq], [p.anchor_pos], d_unit, device=device, batch_size=1
        )
        c0_alpha = c0_alpha[0]
        c0_argmax = c0_argmax[0]
        c0_alpha_norm = c0_alpha / alpha_full if abs(alpha_full) > 1e-8 else float("nan")
        if not (c0_alpha_norm >= 0.5 and c0_argmax == p.anchor_pos):
            print(f"[exp2 {i}/{len(p50)}] {p.protein} SKIP: C0 alpha_norm={c0_alpha_norm:.3f}, argmax={c0_argmax} (anchor={p.anchor_pos}), radius={radius}", flush=True)
            continue
        protein_map = mapping_df[
            (mapping_df["protein"] == p.protein)
            & (mapping_df["anchor_pfam"] == mapping_df["pfam_acc"])
        ].copy()
        state_ic_by_pos = {int(r.seq_pos): float(r.state_ic) for r in protein_map.itertuples(index=False)}
        mapped_window = [pos for pos in window if pos in state_ic_by_pos and pos != p.anchor_pos]
        if not mapped_window:
            continue
        state_ic_vals = [state_ic_by_pos[pos] for pos in mapped_window]
        median_ic = float(np.median(state_ic_vals))
        rsa_map = compute_rsa_map(p.protein, seq)
        c7 = choose_top_k_positions([(pos, state_ic_by_pos[pos]) for pos in mapped_window], k=k, reverse=True)
        buried_low = [
            (pos, state_ic_by_pos[pos]) for pos in mapped_window
            if rsa_map and pos in rsa_map and rsa_map[pos] < 0.05 and state_ic_by_pos[pos] <= median_ic
        ]
        exposed_low = [
            (pos, state_ic_by_pos[pos]) for pos in mapped_window
            if rsa_map and pos in rsa_map and rsa_map[pos] > 0.25 and state_ic_by_pos[pos] <= median_ic
        ]
        c4 = choose_top_k_positions(buried_low, k=k, reverse=False)
        c5 = choose_top_k_positions(exposed_low, k=k, reverse=False)
        far_positions = [pos for pos in range(len(seq)) if abs(pos - p.anchor_pos) > radius]
        c_far = far_positions[:k]
        conditions: list[tuple[str, list[int], set[int], int]] = [
            ("C0", [], set(), 0),
            ("C7", c7, set(), 0),
            ("C4", c4, set(), 0),
            ("C5", c5, set(), 0),
            ("C_anchor", [p.anchor_pos], set(), 0),
            ("C_far", [], set(c_far), 0),
        ]
        if c7 and rsa_map:
            bin_edges = [0.0, 0.05, 0.25, 10.0]
            target_bins = Counter(np.digitize([rsa_map.get(pos, 0.0) for pos in c7], bin_edges, right=False))
            rng = np.random.default_rng(42 + i)
            random_pool = [pos for pos in window if pos != p.anchor_pos and pos in rsa_map]
            for rep in range(n_random_resamples):
                sampled = []
                pool_by_bin: dict[int, list[int]] = defaultdict(list)
                for pos in random_pool:
                    pool_by_bin[int(np.digitize([rsa_map[pos]], bin_edges, right=False)[0])].append(pos)
                for bin_id, count in target_bins.items():
                    pool = pool_by_bin.get(bin_id, [])
                    if not pool:
                        continue
                    sampled.extend(rng.choice(pool, size=min(count, len(pool)), replace=len(pool) < count).tolist())
                conditions.append(("C8", sampled[:k], set(), rep))

        batch_sequences = []
        batch_positions = []
        meta = []
        for cond, mask_positions, far_unmask, rep in conditions:
            batch_sequences.append(
                build_local_window_sequence(
                    seq,
                    anchor_pos=p.anchor_pos,
                    radius=radius,
                    unmask_far_positions=far_unmask,
                    extra_mask_positions=set(mask_positions),
                )
            )
            batch_positions.append(p.anchor_pos)
            meta.append((cond, mask_positions, far_unmask, rep))
        alphas, argmax_positions = project_batch_at_positions(
            model,
            tokenizer,
            batch_sequences,
            batch_positions,
            d_unit,
            device=device,
            batch_size=batch_size,
        )
        for alpha, argmax_pos, (cond, mask_positions, far_unmask, rep) in zip(alphas, argmax_positions, meta):
            alpha_norm = alpha / alpha_full if abs(alpha_full) > 1e-8 else np.nan
            delta = alpha_norm - (c0_alpha / alpha_full if abs(alpha_full) > 1e-8 else np.nan)
            cond_selected_radius, cond_first_cross = derive_selected_radius_for_condition(
                sequence=seq,
                anchor_pos=p.anchor_pos,
                base_radius=radius,
                unmask_far_positions=far_unmask,
                extra_mask_positions=set(mask_positions),
                model=model,
                tokenizer=tokenizer,
                d_unit=d_unit,
                alpha_full=alpha_full,
                device=device,
                batch_size=batch_size,
                jump_threshold=jump_threshold,
            )
            rows.append(
                {
                    "protein": p.protein,
                    "anchor_pos": p.anchor_pos,
                    "radius": radius,
                    "k": k,
                    "condition": cond,
                    "repeat": rep,
                    "alpha": alpha,
                    "alpha_full": alpha_full,
                    "alpha_norm": alpha_norm,
                    "delta_alpha_norm": delta,
                    "c0_alpha_norm": c0_alpha / alpha_full if abs(alpha_full) > 1e-8 else np.nan,
                    "argmax_pos": argmax_pos,
                    "anchor_argmax_preserved": int(argmax_pos == p.anchor_pos),
                    "condition_selected_radius": cond_selected_radius,
                    "condition_r50_first_crossing": cond_first_cross,
                    "perturbed_positions": ";".join(map(str, mask_positions)),
                    "far_positions": ";".join(map(str, sorted(far_unmask))),
                }
            )
        print(f"[exp2 {i}/{len(p50)}] {p.protein}", flush=True)

    results_df = pd.DataFrame(rows)
    results_df.to_csv(out_dir / "condition_results.csv", index=False)

    summary_rows = []
    if not results_df.empty:
        pivot_base = results_df[results_df["condition"].isin(["C7", "C4", "C5", "C_anchor", "C_far"])]
        agg = pivot_base.groupby(["protein", "condition"], as_index=False)["delta_alpha_norm"].mean()
        wide = agg.pivot(index="protein", columns="condition", values="delta_alpha_norm")
        for a, b in [("C7", "C4"), ("C7", "C5")]:
            if a in wide.columns and b in wide.columns:
                paired = wide[[a, b]].dropna()
                if len(paired):
                    stat = wilcoxon(paired[a], paired[b], zero_method="wilcox", alternative="two-sided")
                    hl = float(np.median(paired[a] - paired[b]))
                else:
                    stat = None
                    hl = np.nan
                summary_rows.append(
                    {
                        "comparison": f"{a}_vs_{b}",
                        "n": len(paired),
                        "wilcoxon_p": (stat.pvalue if stat else np.nan),
                        "median_delta_diff": hl,
                    }
                )
        c8 = results_df[results_df["condition"] == "C8"].groupby("protein", as_index=False)["delta_alpha_norm"].mean()
        if "C7" in wide.columns and not c8.empty:
            merged = wide[["C7"]].reset_index().merge(c8, on="protein", how="inner", suffixes=("_c7", "_c8"))
            if len(merged):
                stat = wilcoxon(merged["C7"], merged["delta_alpha_norm"], zero_method="wilcox", alternative="two-sided")
                summary_rows.append(
                    {
                        "comparison": "C7_vs_C8",
                        "n": len(merged),
                        "wilcoxon_p": stat.pvalue,
                        "median_delta_diff": float(np.median(merged["C7"] - merged["delta_alpha_norm"])),
                    }
                )
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(out_dir / "condition_summary.csv", index=False)
    return results_df, summary_df


def load_3di_fasta(path: Path) -> dict[str, str]:
    seqs = {}
    name = None
    chunks: list[str] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name is not None:
                    seqs[name] = "".join(chunks)
                name = line[1:].split()[0]
                chunks = []
            else:
                chunks.append(line)
    if name is not None:
        seqs[name] = "".join(chunks)
    return seqs


def encode_window_onehot(window: str, alphabet: str, mapping: dict[str, int]) -> np.ndarray:
    arr = np.zeros((len(window), len(alphabet)), dtype=np.float32)
    for i, char in enumerate(window):
        if char in mapping:
            arr[i, mapping[char]] = 1.0
    return arr.reshape(-1)


def fixed_window(seq: str, center: int, half_width: int) -> str:
    chars = []
    for pos in range(center - half_width, center + half_width + 1):
        if 0 <= pos < len(seq):
            chars.append(seq[pos])
        else:
            chars.append("X")
    return "".join(chars)


def parse_group_anchor_columns(group_name: str) -> dict[str, int]:
    path = STRUCT_TRANSFER_DIR / f"{group_name}_concordance.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path)
    if group_name == "1pvg":
        ref = "1pvg-assembly1cifgz"
    else:
        ref = "2b61-assembly1cifgz"
    out = {}
    for row in df.itertuples(index=False):
        if row.protein_a == ref:
            out[row.protein_b] = int(row.anchor_col_b)
        elif row.protein_b == ref:
            out[row.protein_a] = int(row.anchor_col_a)
    out[ref] = 122 if group_name == "1pvg" else 64
    return out


def collect_cluster_samples(
    p50: list[P50Row],
    seqs: dict[str, str],
    mapping_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    anchor_label_df = build_anchor_pfam_label(mapping_df)
    anchor_label = {row.protein: row.anchor_pfam for row in anchor_label_df.itertuples(index=False)}
    three_di = load_3di_fasta(FOLDSEEK_FA)
    for p in p50:
        pdb4 = p.protein[:4].upper()
        chain = p.protein[4]
        di_key = f"{pdb4}_{chain}" if f"{pdb4}_{chain}" in three_di else pdb4
        if di_key not in three_di:
            continue
        try:
            struct_seq = get_struct_seq(pdb4, chain)
        except Exception:
            continue
        full_seq = seqs[p.protein]
        if not struct_seq:
            continue
        try:
            mapping = build_full_to_struct_map(full_seq, struct_seq)
        except Exception:
            continue
        if p.anchor_pos not in mapping:
            continue
        struct_anchor = mapping[p.anchor_pos]
        aa_win = fixed_window(struct_seq, struct_anchor, 15)
        di_win = fixed_window(three_di[di_key], struct_anchor, 15)
        rows.append(
            {
                "sample_id": p.protein,
                "protein": p.protein,
                "pdb_id": pdb4.lower(),
                "anchor_pos_struct": struct_anchor,
                "aa_window": aa_win,
                "di_window": di_win,
                "pfam_label": anchor_label.get(p.protein),
                "source": "p50",
                "col_equiv": np.nan,
            }
        )

    for group in ("1pvg", "2b61a"):
        audit_path = STRUCT_TRANSFER_DIR / f"{group}_audit.csv"
        if not audit_path.exists():
            continue
        audit_df = pd.read_csv(audit_path)
        anchor_cols = parse_group_anchor_columns(group)
        dominant_col = 122 if group == "1pvg" else 64
        for row in audit_df.itertuples(index=False):
            pdb4 = str(row.pdb_id).upper()
            di_key = None
            for candidate in (f"{pdb4}_A", pdb4):
                if candidate in three_di:
                    di_key = candidate
                    break
            if di_key is None:
                continue
            try:
                aa_seq = get_struct_seq(pdb4, "A")
            except Exception:
                continue
            di_seq = three_di[di_key]
            anchor_pos = int(row.anchor_pos)
            if not aa_seq or anchor_pos >= len(aa_seq) or anchor_pos >= len(di_seq):
                continue
            aa_win = fixed_window(aa_seq, anchor_pos, 15)
            di_win = fixed_window(di_seq, anchor_pos, 15)
            col = anchor_cols.get(row.protein)
            rows.append(
                {
                    "sample_id": row.protein,
                    "protein": row.protein,
                    "pdb_id": pdb4.lower(),
                    "anchor_pos_struct": anchor_pos,
                    "aa_window": aa_win,
                    "di_window": di_win,
                    "pfam_label": np.nan,
                    "source": group,
                    "col_equiv": float(col == dominant_col) if col is not None else np.nan,
                }
            )
    return pd.DataFrame(rows).drop_duplicates(subset=["sample_id"])


def run_foldseek_struct_clusters(samples: pd.DataFrame, out_dir: Path) -> dict[str, str]:
    if not FOLDSEEK_BIN.exists():
        return {pdb_id: pdb_id for pdb_id in samples["pdb_id"].unique()}
    run_dir = out_dir / "foldseek_cluster"
    query_dir = run_dir / "inputs"
    tmp_dir = run_dir / "tmp"
    ensure_dir(query_dir)
    ensure_dir(tmp_dir)
    for pdb_id in samples["pdb_id"].unique():
        src = PDB_DIR / f"{pdb_id}.pdb"
        if not src.exists():
            src = PDB_DIR / f"{pdb_id}.cif"
        if not src.exists():
            continue
        dst = query_dir / src.name
        if not dst.exists():
            shutil.copy2(src, dst)
    prefix = run_dir / "struct_tm05"
    cmd = [
        str(FOLDSEEK_BIN),
        "easy-cluster",
        str(query_dir),
        str(prefix),
        str(tmp_dir),
        "--tmscore-threshold",
        "0.5",
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception:
        return {pdb_id: pdb_id for pdb_id in samples["pdb_id"].unique()}
    cluster_tsv = Path(f"{prefix}_cluster.tsv")
    if not cluster_tsv.exists():
        return {pdb_id: pdb_id for pdb_id in samples["pdb_id"].unique()}
    struct_label = {}
    with cluster_tsv.open() as f:
        for line in f:
            rep, member = line.strip().split("\t")[:2]
            rep_id = Path(rep).stem[:4].lower()
            member_id = Path(member).stem[:4].lower()
            struct_label[member_id] = rep_id
    return struct_label


def hdbscan_labels_from_cosine(embeddings: np.ndarray) -> np.ndarray:
    import hdbscan

    dist = cosine_distances(embeddings).astype(np.float64, copy=False)
    clusterer = hdbscan.HDBSCAN(min_cluster_size=max(3, len(embeddings) // 12), min_samples=2, metric="precomputed")
    return clusterer.fit_predict(dist)


def loo_knn_accuracy(embeddings: np.ndarray, labels: list[str | float]) -> float:
    valid_idx = [i for i, label in enumerate(labels) if pd.notna(label)]
    if len(valid_idx) < 2:
        return np.nan
    emb = embeddings[valid_idx]
    labs = [labels[i] for i in valid_idx]
    dist = cosine_distances(emb)
    correct = 0
    for i in range(len(valid_idx)):
        dist[i, i] = np.inf
        nn = int(np.argmin(dist[i]))
        correct += int(labs[nn] == labs[i])
    return correct / len(valid_idx)


def label_metrics(cluster_labels: np.ndarray, labels: list[str | float]) -> tuple[float, float]:
    valid_idx = [i for i, label in enumerate(labels) if pd.notna(label)]
    if len(valid_idx) < 2:
        return np.nan, np.nan
    y_true = [str(labels[i]) for i in valid_idx]
    y_pred = [str(cluster_labels[i]) for i in valid_idx]
    return normalized_mutual_info_score(y_true, y_pred), adjusted_rand_score(y_true, y_pred)


def run_experiment_3(
    p50: list[P50Row],
    seqs: dict[str, str],
    mapping_df: pd.DataFrame,
    out_dir: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    ensure_dir(out_dir)
    samples = collect_cluster_samples(p50, seqs, mapping_df)
    if samples.empty:
        samples.to_csv(out_dir / "labels.csv", index=False)
        metrics_df = pd.DataFrame(columns=["representation", "label", "nmi", "ari", "loo_knn_acc"])
        metrics_df.to_csv(out_dir / "metrics.csv", index=False)
        np.save(out_dir / "embeddings_aa.npy", np.zeros((0, 31 * len(STANDARD_AA)), dtype=np.float32))
        np.save(out_dir / "embeddings_3di.npy", np.zeros((0, 31 * len(DI_ALPHABET)), dtype=np.float32))
        return samples, metrics_df
    struct_label = run_foldseek_struct_clusters(samples, out_dir)
    samples["struct_label"] = samples["pdb_id"].map(struct_label)
    emb_aa = np.stack([encode_window_onehot(w, STANDARD_AA, AA_TO_IDX) for w in samples["aa_window"]], axis=0)
    emb_di = np.stack([encode_window_onehot(w, DI_ALPHABET, DI_TO_IDX) for w in samples["di_window"]], axis=0)
    np.save(out_dir / "embeddings_aa.npy", emb_aa)
    np.save(out_dir / "embeddings_3di.npy", emb_di)
    labels_path = out_dir / "labels.csv"
    samples.to_csv(labels_path, index=False)

    cluster_aa = hdbscan_labels_from_cosine(emb_aa)
    cluster_di = hdbscan_labels_from_cosine(emb_di)
    metric_rows = []
    label_specs = [
        ("pfam_label", "L_Pfam"),
        ("struct_label", "L_struct"),
        ("col_equiv", "L_col"),
    ]
    for emb_name, emb, cluster_labels in [
        ("AA", emb_aa, cluster_aa),
        ("3Di", emb_di, cluster_di),
    ]:
        for label_col, label_name in label_specs:
            nmi, ari = label_metrics(cluster_labels, samples[label_col].tolist())
            acc = loo_knn_accuracy(emb, samples[label_col].tolist())
            metric_rows.append(
                {
                    "representation": emb_name,
                    "label": label_name,
                    "nmi": nmi,
                    "ari": ari,
                    "loo_knn_acc": acc,
                }
            )
    metrics_df = pd.DataFrame(metric_rows)
    metrics_df.to_csv(out_dir / "metrics.csv", index=False)

    try:
        import umap

        for emb_name, emb in [("aa", emb_aa), ("3di", emb_di)]:
            reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine", random_state=42)
            proj = reducer.fit_transform(emb)
            for label_col in ("pfam_label", "struct_label", "col_equiv"):
                fig, ax = plt.subplots(figsize=(6, 5))
                labels = samples[label_col].fillna("NA").astype(str)
                uniq = list(dict.fromkeys(labels))
                cmap = plt.cm.get_cmap("tab20", len(uniq))
                for idx, label in enumerate(uniq):
                    mask = labels == label
                    ax.scatter(proj[mask, 0], proj[mask, 1], s=22, alpha=0.85, label=label, color=cmap(idx))
                ax.set_title(f"{emb_name.upper()} UMAP by {label_col}")
                ax.set_xlabel("UMAP-1")
                ax.set_ylabel("UMAP-2")
                if len(uniq) <= 12:
                    ax.legend(fontsize=7, loc="best")
                fig.tight_layout()
                fig.savefig(out_dir / f"umap_{emb_name}_{label_col}.png", dpi=160, bbox_inches="tight")
                plt.close(fig)
    except Exception as exc:
        write_text(out_dir / "umap_error.txt", f"{type(exc).__name__}: {exc}\n")
    return samples, metrics_df


def materialize_outcome_map(out_dir: Path) -> None:
    write_text(out_dir / "outcome_map.md", OUTCOME_MAP_MD)
    write_text(out_dir / "radius_selection_note.md", RADIUS_SELECTION_NOTE_MD)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--experiments", nargs="+", default=["0", "1", "2", "3"])
    p.add_argument("--p50-limit", type=int, default=200)
    p.add_argument("--device", type=str, default="cpu")
    p.add_argument("--exp0-max-flank", type=int, default=40)
    p.add_argument("--jump-threshold", type=float, default=0.4)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--control-resamples", type=int, default=200)
    p.add_argument("--random-resamples", type=int, default=200)
    p.add_argument("--skip-existing", action="store_true")
    p.add_argument("--annotation-root", type=Path, default=INTERPRO_CACHE_DIR)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dir(OUTPUT_DIR)
    materialize_outcome_map(OUTPUT_DIR)
    seqs = load_sequences()
    ss_dict = load_ss_dict()
    p50 = select_p50(limit=args.p50_limit)
    save_p50_manifest(p50, OUTPUT_DIR)
    need_model = any(exp in {"0", "2"} for exp in args.experiments)
    model = tokenizer = d_unit = None
    if need_model:
        t0 = time.time()
        print(f"Loading {MODEL_NAME} on {args.device}", flush=True)
        model, tokenizer = load_model(args.device)
        weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
        d = compute_search_dir(model, tokenizer, " ".join(seqs[REFERENCE_PROTEIN]), weights, device=args.device)
        d_unit = d / d.norm().clamp(min=1e-8)
        print(f"Model + search dir ready in {time.time() - t0:.1f}s", flush=True)

    exp0_dir = OUTPUT_DIR / "anchor_flank_sweep_step1"
    exp1_dir = OUTPUT_DIR
    exp2_dir = OUTPUT_DIR / "paired_masking"
    exp3_dir = OUTPUT_DIR / "anchor_window_cluster"

    exp0_df = exp0_summary = None
    mapping_df = per_pfam_df = None

    if "0" in args.experiments:
        exp0_df, exp0_summary = run_experiment_0(
            p50=p50,
            seqs=seqs,
            out_dir=exp0_dir,
            model=model,
            tokenizer=tokenizer,
            d_unit=d_unit,
            device=args.device,
            max_flank=args.exp0_max_flank,
            batch_size=args.batch_size,
            jump_threshold=args.jump_threshold,
        )
    else:
        per_path = exp0_dir / "per_protein.csv"
        summary_path = exp0_dir / "summary.csv"
        if per_path.exists():
            exp0_df = pd.read_csv(per_path)
        if summary_path.exists():
            exp0_summary = pd.read_csv(summary_path)

    if "1" in args.experiments:
        mapping_df, per_pfam_df = run_experiment_1(
            p50=p50,
            seqs=seqs,
            ss_dict=ss_dict,
            out_dir=exp1_dir,
            annotation_root=args.annotation_root,
            n_control_resamples=args.control_resamples,
        )
    else:
        mapping_path = exp1_dir / "anchor_hmm_mapping.tsv"
        entropy_path = exp1_dir / "per_pfam_entropy.csv"
        if mapping_path.exists():
            mapping_df = safe_read_csv(mapping_path, sep="\t")
        if entropy_path.exists():
            per_pfam_df = safe_read_csv(entropy_path)

    if "2" in args.experiments:
        if exp0_summary is None or mapping_df is None:
            raise RuntimeError("Experiment 2 requires Experiment 0 summary and Experiment 1 mapping outputs.")
        run_experiment_2(
            p50=p50,
            seqs=seqs,
            mapping_df=mapping_df,
            exp0_summary=exp0_summary,
            ss_dict=ss_dict,
            out_dir=exp2_dir,
            model=model,
            tokenizer=tokenizer,
            d_unit=d_unit,
            device=args.device,
            batch_size=args.batch_size,
            n_random_resamples=args.random_resamples,
            jump_threshold=args.jump_threshold,
        )

    if "3" in args.experiments:
        if mapping_df is None:
            raise RuntimeError("Experiment 3 requires Experiment 1 mapping outputs.")
        run_experiment_3(
            p50=p50,
            seqs=seqs,
            mapping_df=mapping_df,
            out_dir=exp3_dir,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
