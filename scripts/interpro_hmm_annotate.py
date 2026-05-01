"""Annotate a PDB chain with InterPro families/domains and align its sequence to each Pfam HMM.

Pipeline:
  1. PDB chain id (e.g. "2B61A") -> sequence from data/full_seq_dict.json
  2. PDB -> UniProt accession via SIFTS (PDBe REST API), filtered by chain
  3. UniProt accession -> InterPro entries (all member DBs) via the InterPro REST API
  4. For each Pfam member-database signature, download the HMM (?annotation=hmm)
  5. hmmalign the query sequence to each HMM with pyhmmer; write Stockholm + A2M outputs

Outputs are written to <out_dir>/<PDB_ID>/:
  - annotations.json     full InterPro REST response (entries & locations)
  - pfam_summary.tsv     one row per Pfam hit (acc, name, start, end, hmm_len)
  - hmms/<pfam>.hmm      decompressed HMM files
  - alignments/<pfam>.sto / .a2m    hmmalign outputs

Usage:
    uv run python scripts/interpro_hmm_annotate.py 2B61A
    uv run python scripts/interpro_hmm_annotate.py 2B61A --out reports/out2/interpro_hmm

Requires: requests, pyhmmer (`uv add pyhmmer`).
"""

from __future__ import annotations

import argparse
import gzip
import io
import json
import sys
import time
from pathlib import Path

import requests

SIFTS_URL = "https://www.ebi.ac.uk/pdbe/api/mappings/uniprot/{pdb}"
INTERPRO_ENTRIES_URL = (
    "https://www.ebi.ac.uk/interpro/api/entry/all/protein/uniprot/{acc}/?page_size=200"
)
INTERPRO_HMM_URL = (
    "https://www.ebi.ac.uk/interpro/api/entry/{db}/{acc}?annotation=hmm"
)

DEFAULT_SEQ_DICT = Path("data/full_seq_dict.json")
DEFAULT_OUT = Path("reports/out2/interpro_hmm")

# Member databases that expose HMMs through the InterPro ?annotation=hmm endpoint.
HMM_DBS = {"pfam", "ncbifam", "sfld", "antifam"}


def split_pdb_chain(pdb_chain: str) -> tuple[str, str]:
    """Split a SIFTS-style id like '2B61A' into ('2b61', 'A')."""
    if len(pdb_chain) < 5:
        raise ValueError(f"Expected 4-char PDB id + chain, got {pdb_chain!r}")
    return pdb_chain[:4].lower(), pdb_chain[4:]


def get_sequence(pdb_chain: str, seq_dict_path: Path) -> str:
    d = json.loads(seq_dict_path.read_text())
    if pdb_chain not in d:
        raise KeyError(f"{pdb_chain} not in {seq_dict_path}")
    return d[pdb_chain]


def sifts_uniprot(pdb_id: str, chain: str) -> str:
    """Return the UniProt accession mapped to the given PDB chain.

    If multiple UniProts cover the chain (chimeric entries), pick the one with the
    largest covered span and warn.
    """
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
        raise RuntimeError(f"No UniProt mapping for {pdb_id} chain {chain}")
    candidates.sort(key=lambda x: -x[1])
    if len({a for a, _ in candidates}) > 1:
        print(f"[warn] multiple UniProts for {pdb_id}{chain}: {candidates} -- using {candidates[0][0]}", file=sys.stderr)
    return candidates[0][0]


def interpro_entries(uniprot_acc: str) -> dict:
    r = requests.get(INTERPRO_ENTRIES_URL.format(acc=uniprot_acc), timeout=60)
    r.raise_for_status()
    return r.json()


def download_hmm(db: str, acc: str) -> bytes:
    """Download and gunzip an HMM file from InterPro. Returns raw HMM bytes."""
    r = requests.get(INTERPRO_HMM_URL.format(db=db, acc=acc), timeout=60)
    r.raise_for_status()
    raw = r.content
    # Endpoint serves gzipped content; tolerate already-decompressed bodies too.
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw


def collect_hmm_signatures(entries: dict) -> list[dict]:
    """Flatten the InterPro response into a list of HMM-bearing signatures.

    Each item: {db, accession, name, locations: [(start, end), ...]}
    InterPro entries themselves don't have HMMs; their member-database signatures do
    (Pfam, NCBIfam, SFLD, AntiFam). For unintegrated member entries the metadata
    sits at the top level instead of under member_databases.
    """
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
            out.append({
                "db": src,
                "accession": meta["accession"],
                "name": meta.get("name") or meta["accession"],
                "interpro_parent": meta.get("integrated"),
                "locations": locations,
            })
        elif src == "interpro":
            # Walk member databases for HMM-bearing children.
            mdbs = meta.get("member_databases") or {}
            for mdb, members in mdbs.items():
                if mdb.lower() not in HMM_DBS:
                    continue
                for macc, mname in members.items():
                    out.append({
                        "db": mdb.lower(),
                        "accession": macc,
                        "name": mname,
                        "interpro_parent": meta["accession"],
                        # Locations on the InterPro entry are an envelope over member
                        # hits; report them as a hint, but hmmalign uses the full seq.
                        "locations": locations,
                    })
    # Deduplicate (db, accession) since a member can be reported both standalone
    # and under its InterPro parent.
    seen = {}
    for s in out:
        key = (s["db"], s["accession"])
        if key not in seen:
            seen[key] = s
        else:
            # Prefer the version with an interpro_parent so we keep that linkage.
            if not seen[key].get("interpro_parent") and s.get("interpro_parent"):
                seen[key] = s
    return list(seen.values())


def hmmalign_sequence(hmm_bytes: bytes, seq_name: str, seq: str) -> tuple[bytes, bytes, int]:
    """Run hmmalign with pyhmmer. Returns (stockholm_bytes, a2m_bytes, hmm_M)."""
    import pyhmmer

    with pyhmmer.plan7.HMMFile(io.BytesIO(hmm_bytes)) as hf:
        hmm = hf.read()
    alphabet = hmm.alphabet
    digital = pyhmmer.easel.TextSequence(
        name=seq_name.encode(), sequence=seq
    ).digitize(alphabet)
    msa = pyhmmer.hmmer.hmmalign(hmm, [digital])

    sto_buf = io.BytesIO()
    msa.write(sto_buf, format="stockholm")
    a2m_buf = io.BytesIO()
    msa.write(a2m_buf, format="a2m")
    return sto_buf.getvalue(), a2m_buf.getvalue(), int(hmm.M)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pdb_chain", help="PDB id + chain, e.g. 2B61A")
    ap.add_argument("--seq-dict", type=Path, default=DEFAULT_SEQ_DICT)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--databases", nargs="+", default=["pfam"],
                    help=f"Member DBs to fetch HMMs for (subset of {sorted(HMM_DBS)}).")
    ap.add_argument("--skip-align", action="store_true",
                    help="Download HMMs but skip hmmalign.")
    args = ap.parse_args()

    pdb_id, chain = split_pdb_chain(args.pdb_chain)
    seq = get_sequence(args.pdb_chain, args.seq_dict)
    print(f"[info] {args.pdb_chain}: {len(seq)} residues")

    uniprot = sifts_uniprot(pdb_id, chain)
    print(f"[info] SIFTS: {pdb_id}{chain} -> UniProt {uniprot}")

    entries = interpro_entries(uniprot)
    print(f"[info] InterPro: {entries.get('count', 0)} entries")

    out_dir = args.out / args.pdb_chain
    (out_dir / "hmms").mkdir(parents=True, exist_ok=True)
    (out_dir / "alignments").mkdir(parents=True, exist_ok=True)
    (out_dir / "annotations.json").write_text(json.dumps(entries, indent=2))

    sigs = [s for s in collect_hmm_signatures(entries) if s["db"] in args.databases]
    print(f"[info] HMM-bearing signatures ({','.join(args.databases)}): {len(sigs)}")

    summary_rows = ["\t".join([
        "db", "accession", "name", "interpro_parent", "locations", "hmm_M", "align_path",
    ])]
    for sig in sigs:
        tag = sig["accession"]
        hmm_path = out_dir / "hmms" / f"{tag}.hmm"
        try:
            hmm_bytes = download_hmm(sig["db"], sig["accession"])
        except requests.HTTPError as e:
            print(f"[warn] HMM download failed for {sig['db']}:{tag}: {e}", file=sys.stderr)
            continue
        hmm_path.write_bytes(hmm_bytes)
        hmm_M = -1
        align_rel = ""
        if not args.skip_align:
            sto, a2m, hmm_M = hmmalign_sequence(hmm_bytes, args.pdb_chain, seq)
            sto_path = out_dir / "alignments" / f"{tag}.sto"
            a2m_path = out_dir / "alignments" / f"{tag}.a2m"
            sto_path.write_bytes(sto)
            a2m_path.write_bytes(a2m)
            align_rel = str(sto_path.relative_to(out_dir))
            print(f"[ok] {tag} ({sig['name']}): hmm M={hmm_M} -> {align_rel}")
        loc_str = ";".join(f"{a}-{b}" for a, b in sig["locations"]) or "-"
        summary_rows.append("\t".join([
            sig["db"], sig["accession"], sig["name"],
            sig.get("interpro_parent") or "-",
            loc_str, str(hmm_M), align_rel or "-",
        ]))
        time.sleep(0.2)  # be polite to EBI

    (out_dir / "pfam_summary.tsv").write_text("\n".join(summary_rows) + "\n")
    print(f"[done] outputs in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
