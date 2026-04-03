#!/usr/bin/env python3
"""3D structure viewer: color residues by projection score, highlight anchor/SS1/SS2.

Generates a single HTML with a 3Dmol.js viewer and a protein selector dropdown.
Each protein's PDB is embedded in the HTML along with projection scores.

Usage:
    uv run python scripts/anchor_structure_viewer.py --device cuda
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONFIG_DIR = ROOT / "configs"
REPORT_DIR = ROOT / "reports" / "outputs" / "multi_protein"
WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
sys.path.insert(0, str(ROOT))

NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280
TARGET_LAYER = 10
TARGET_HEAD = 9
SEGMENT_RADIUS = 5
REFERENCE_PROTEIN = "2B61A"

ANCHOR_POSITIONS = {
    "1BRTA": 220, "1PVGA": 101, "2B61A": 315, "2DPMA": 39, "2PKEA": 131,
    "2QY6A": 64, "2YHWA": 287, "3CSSA": 40, "3HO7A": 63, "3OKPA": 200,
    "3QDLA": 114, "3WJPA": 94, "4EHUA": 100, "4EX6A": 124, "4EZIA": 310,
    "4ME3A": 75, "4N9WA": 194, "4OY3A": 193,
}


def load_configs():
    with open(CONFIG_DIR / "proteins.json") as f:
        protein_configs = json.load(f)
    with open(DATA_DIR / "full_seq_dict.json") as f:
        seqs = json.load(f)
    with open(DATA_DIR / "ss_dict.json") as f:
        ss_raw = json.load(f)
    ss_dict = {}
    for k, v in ss_raw.items():
        ss_dict[k.replace(".pdb", "")] = v.replace("-", "C")
    return protein_configs, seqs, ss_dict


def _find_pdb(protein):
    ev_dir = DATA_DIR / f"{protein}_EV"
    if not ev_dir.exists():
        return None
    candidates = sorted(ev_dir.glob("TARGET_b*/*.pdb"))
    candidates = [c for c in candidates if "compare" not in str(c) and "aux" not in str(c)]
    return candidates[0] if candidates else None


def _align_pdb_to_seq(pdb_residues, full_seq):
    resids = [r[0] for r in pdb_residues]
    n_seq = len(full_seq)
    best_offset, best_matches = 0, 0
    for offset in range(-max(resids), n_seq - min(resids) + 1):
        matches = sum(1 for resid, aa in pdb_residues
                      if 0 <= resid + offset < n_seq and full_seq[resid + offset] == aa)
        if matches > best_matches:
            best_offset, best_matches = offset, matches
    mapping = {}
    for i, (resid, aa) in enumerate(pdb_residues):
        seq_pos = resid + best_offset
        if 0 <= seq_pos < n_seq and full_seq[seq_pos] == aa:
            mapping[resid] = seq_pos
    return mapping


def get_pdb_resids_and_text(protein, full_seq):
    """Return (pdb_text, resid_to_seqpos_mapping) or (None, None)."""
    from Bio.PDB import PDBParser
    from Bio.Data.IUPACData import protein_letters_3to1

    def three_to_one(name):
        return protein_letters_3to1.get(name.lower().capitalize(), "X")

    pdb_path = _find_pdb(protein)
    if pdb_path is None:
        return None, None

    parser = PDBParser(QUIET=True)
    structure = parser.get_structure(protein, str(pdb_path))
    chain = list(structure[0])[0]

    pdb_tuples = []
    for residue in chain:
        if residue.get_id()[0] != " ":
            continue
        resid = residue.get_id()[1]
        aa = three_to_one(residue.get_resname())
        if aa != "X":
            pdb_tuples.append((resid, aa))

    if not pdb_tuples:
        return None, None

    mapping = _align_pdb_to_seq(pdb_tuples, full_seq)
    if len(mapping) < len(pdb_tuples) * 0.5:
        return None, None

    with open(pdb_path) as f:
        pdb_text = f.read()

    return pdb_text, mapping


def load_model(device):
    from nnsight import NNsight
    from transformers import EsmForMaskedLM, EsmTokenizer
    os.environ["HF_HOME"] = WEIGHTS_DIR
    model_name = "facebook/esm2_t33_650M_UR50D"
    tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=WEIGHTS_DIR)
    esm_model = EsmForMaskedLM.from_pretrained(
        model_name, cache_dir=WEIGHTS_DIR, attn_implementation="eager"
    ).to(device).eval()
    return NNsight(esm_model), tokenizer


def extract_head_weights(model, layer, head):
    attn = model._model.esm.encoder.layer[layer].attention
    W_Q = attn.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_Q = attn.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    W_K = attn.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_K = attn.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    return {"W_Q_hd": W_Q[head].clone(), "b_Q_d": b_Q[head].clone(),
            "W_K_hd": W_K[head].clone(), "b_K_d": b_K[head].clone()}


def compute_search_dir(model, tokenizer, ref_clean, weights, device):
    inputs = tokenizer(ref_clean, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    W_Q, b_Q, W_K = weights["W_Q_hd"], weights["b_Q_d"], weights["W_K_hd"]
    q_all = x_ln @ W_Q.T + b_Q
    q_res = q_all[1:-1]
    q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
    q_mean = q_unit.mean(dim=0)
    q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
    search_dir = W_K.T @ q_mean_norm
    return (search_dir / search_dir.norm().clamp(min=1e-8)).to(device)


def capture_projection_scores(model, tokenizer, sequence, search_dir_unit, device):
    inputs = tokenizer(sequence, return_tensors="pt").to(device)
    ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
    with model.trace() as tracer:
        with tracer.invoke(**inputs):
            cache = tracer.cache(modules=[ln_module])
    key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
    x_ln = cache[key].output.detach().cpu()[0]
    return (x_ln[1:-1] @ search_dir_unit.cpu()).numpy()


def build_clean_sequence(sequence, config):
    pos1, pos2 = config["contact_pair"]
    flank = config.get("clean_flank", 44)
    n = len(sequence)
    ss1_s, ss1_e = pos1 - SEGMENT_RADIUS, pos1 + SEGMENT_RADIUS + 1
    ss2_s, ss2_e = pos2 - SEGMENT_RADIUS, pos2 + SEGMENT_RADIUS + 1
    masked = ["<mask>"] * n
    for i in range(ss1_s, ss1_e):
        masked[i] = sequence[i]
    for i in range(ss2_s, ss2_e):
        masked[i] = sequence[i]
    for i in range(max(0, ss1_s - flank), ss1_s):
        masked[i] = sequence[i]
    for i in range(ss2_e, min(n, ss2_e + flank)):
        masked[i] = sequence[i]
    return "".join(masked)


def score_to_color(score, vmin, vmax):
    """Map score to blue-white-red color. Low=blue, 0=white, high=red."""
    if vmax == vmin:
        return "0xFFFFFF"
    t = (score - vmin) / (vmax - vmin)  # 0..1
    t = max(0, min(1, t))
    # blue (0) -> white (0.5) -> red (1)
    if t < 0.5:
        s = t * 2  # 0..1
        r = int(100 + 155 * s)
        g = int(100 + 155 * s)
        b = 255
    else:
        s = (t - 0.5) * 2  # 0..1
        r = 255
        g = int(255 * (1 - s))
        b = int(255 * (1 - s))
    return f"0x{r:02x}{g:02x}{b:02x}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading...")
    protein_configs, seqs, ss_dict = load_configs()
    model, tokenizer = load_model(args.device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    ref_seq = seqs[REFERENCE_PROTEIN]
    ref_clean = build_clean_sequence(ref_seq, protein_configs[REFERENCE_PROTEIN])
    search_dir_unit = compute_search_dir(model, tokenizer, ref_clean, weights, args.device)

    # Collect per-protein data
    protein_data = {}  # protein -> {pdb_text, scores_by_resid, anchor_resid, ss1_resids, ss2_resids}

    for protein, anchor_pos in ANCHOR_POSITIONS.items():
        sequence = seqs[protein]
        config = protein_configs[protein]
        pdb_text, resid_to_seqpos = get_pdb_resids_and_text(protein, sequence)
        if pdb_text is None:
            print(f"  {protein}: skipped (no PDB)")
            continue

        proj_scores = capture_projection_scores(model, tokenizer, sequence, search_dir_unit, args.device)
        print(f"  {protein}: {len(sequence)} residues")

        # Reverse mapping: seqpos -> resid
        seqpos_to_resid = {v: k for k, v in resid_to_seqpos.items()}

        # Map projection scores to PDB resids
        scores_by_resid = {}
        for resid, seqpos in resid_to_seqpos.items():
            if seqpos < len(proj_scores):
                scores_by_resid[resid] = float(proj_scores[seqpos])

        # Anchor resid
        anchor_resid = seqpos_to_resid.get(anchor_pos)

        # SS1 and SS2 resids
        pos1, pos2 = config["contact_pair"]
        ss1_resids = []
        ss2_resids = []
        for d in range(-SEGMENT_RADIUS, SEGMENT_RADIUS + 1):
            r1 = seqpos_to_resid.get(pos1 + d)
            if r1 is not None:
                ss1_resids.append(r1)
            r2 = seqpos_to_resid.get(pos2 + d)
            if r2 is not None:
                ss2_resids.append(r2)

        # resid -> seqpos mapping for hover display
        resid_to_seqpos_dict = {str(k): v for k, v in resid_to_seqpos.items()}
        # resid -> AA for hover
        resid_to_aa = {}
        for resid, seqpos in resid_to_seqpos.items():
            if seqpos < len(sequence):
                resid_to_aa[str(resid)] = sequence[seqpos]

        # SSE per resid
        sse_str = ss_dict.get(protein, "C" * len(sequence))
        if len(sse_str) != len(sequence):
            sse_str = sse_str[:len(sequence)].ljust(len(sequence), "C")
        resid_to_sse = {}
        for resid, seqpos in resid_to_seqpos.items():
            if seqpos < len(sse_str):
                resid_to_sse[str(resid)] = sse_str[seqpos]

        protein_data[protein] = {
            "pdb_text": pdb_text,
            "scores_by_resid": scores_by_resid,
            "anchor_resid": anchor_resid,
            "anchor_seqpos": anchor_pos,
            "ss1_resids": ss1_resids,
            "ss2_resids": ss2_resids,
            "ss1_center": pos1,
            "ss2_center": pos2,
            "n_residues": len(sequence),
            "resid_to_seqpos": resid_to_seqpos_dict,
            "resid_to_aa": resid_to_aa,
            "resid_to_sse": resid_to_sse,
        }

    print(f"\nProteins with PDB: {len(protein_data)}")

    # Build HTML
    protein_list = sorted(protein_data.keys())

    # Serialize data for JS
    js_data = {}
    for protein in protein_list:
        d = protein_data[protein]
        js_data[protein] = {
            "pdb": d["pdb_text"],
            "scores": d["scores_by_resid"],
            "anchor_resid": d["anchor_resid"],
            "anchor_seqpos": d["anchor_seqpos"],
            "ss1_resids": d["ss1_resids"],
            "ss2_resids": d["ss2_resids"],
            "ss1_center": d["ss1_center"],
            "ss2_center": d["ss2_center"],
            "n_residues": d["n_residues"],
            "resid_to_seqpos": d["resid_to_seqpos"],
            "resid_to_aa": d["resid_to_aa"],
            "resid_to_sse": d["resid_to_sse"],
        }

    # Remove pdb text from json, embed separately to avoid escaping issues
    js_meta = {}
    pdb_texts = {}
    for protein in protein_list:
        pdb_texts[protein] = js_data[protein].pop("pdb")
        js_meta[protein] = js_data[protein]

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html><head>")
    html.append("<title>Anchor Structure Viewer - Projection Score Coloring</title>")
    html.append('<script src="https://3Dmol.org/build/3Dmol-min.js"></script>')
    html.append("<style>")
    html.append("body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 0; padding: 20px; background: #1e1e1e; color: #d4d4d4; }")
    html.append("#controls { display: flex; gap: 20px; align-items: center; margin-bottom: 10px; flex-wrap: wrap; }")
    html.append("select, button { padding: 8px 16px; font-size: 14px; border-radius: 4px; border: 1px solid #555; background: #2d2d2d; color: #d4d4d4; cursor: pointer; }")
    html.append("select:hover, button:hover { border-color: #888; }")
    html.append("#viewer-container { position: relative; }")
    html.append("#viewer { width: 100%; height: 700px; position: relative; border: 1px solid #444; border-radius: 4px; }")
    html.append("#hover-tooltip { position: absolute; top: 10px; right: 10px; background: rgba(30,30,30,0.92); color: #eee; padding: 8px 14px; border-radius: 6px; font-size: 13px; font-family: monospace; pointer-events: none; z-index: 100; display: none; border: 1px solid #666; line-height: 1.5; }")
    html.append("#info { margin-top: 10px; font-size: 13px; line-height: 1.6; }")
    html.append("#colorbar { display: flex; align-items: center; gap: 8px; font-size: 12px; }")
    html.append("#colorbar-gradient { width: 200px; height: 16px; border-radius: 2px; border: 1px solid #555; }")
    html.append(".legend-item { display: inline-flex; align-items: center; gap: 4px; margin-right: 16px; font-size: 12px; }")
    html.append(".legend-dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }")
    html.append("</style>")
    html.append("</head><body>")
    html.append("<h2 style='margin-top:0'>L10H9 Projection Score on 3D Structure</h2>")

    html.append("<div id='controls'>")
    html.append("<label>Protein: <select id='protein-select'>")
    for p in protein_list:
        selected = " selected" if p == "2B61A" else ""
        html.append(f"  <option value='{p}'{selected}>{p}</option>")
    html.append("</select></label>")
    html.append("<label>Style: <select id='style-select'>")
    html.append("  <option value='cartoon' selected>Cartoon</option>")
    html.append("  <option value='stick'>Stick</option>")
    html.append("  <option value='sphere'>Sphere</option>")
    html.append("</select></label>")
    html.append("<button onclick='toggleHighlights()'>Toggle SS1/SS2/Anchor</button>")
    html.append("</div>")

    html.append("<div id='legend' style='margin-bottom:8px;'>")
    html.append("<span class='legend-item'><span class='legend-dot' style='background:#ffff00;border:2px solid #000'></span> Anchor</span>")
    html.append("<span class='legend-item'><span class='legend-dot' style='background:#ff8c00'></span> SS1 segment</span>")
    html.append("<span class='legend-item'><span class='legend-dot' style='background:#9932cc'></span> SS2 segment</span>")
    html.append("</div>")

    html.append("<div id='colorbar'>")
    html.append("<span>Low proj</span>")
    html.append("<div id='colorbar-gradient' style='background: linear-gradient(to right, #6464ff, #ffffff, #ff4444);'></div>")
    html.append("<span>High proj</span>")
    html.append("</div>")

    html.append("<div id='viewer-container'>")
    html.append("<div id='viewer'></div>")
    html.append("<div id='hover-tooltip'></div>")
    html.append("</div>")
    html.append("<div id='info'></div>")

    html.append("<script>")

    # Embed PDB texts as JS object with template literals
    html.append("var pdbTexts = {};")
    for protein in protein_list:
        # Escape backticks and backslashes in PDB text
        pdb_escaped = pdb_texts[protein].replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
        html.append(f"pdbTexts['{protein}'] = `{pdb_escaped}`;")

    # Embed metadata as JSON
    html.append(f"var proteinMeta = {json.dumps(js_meta)};")

    html.append("""
var viewer = null;
var showHighlights = true;

function scoreToColor(score, vmin, vmax) {
    if (vmax === vmin) return 0xffffff;
    var t = (score - vmin) / (vmax - vmin);
    t = Math.max(0, Math.min(1, t));
    var r, g, b;
    if (t < 0.5) {
        var s = t * 2;
        r = Math.round(100 + 155 * s);
        g = Math.round(100 + 155 * s);
        b = 255;
    } else {
        var s = (t - 0.5) * 2;
        r = 255;
        g = Math.round(255 * (1 - s));
        b = Math.round(255 * (1 - s));
    }
    return (r << 16) | (g << 8) | b;
}

function loadProtein(protein) {
    var container = document.getElementById('viewer');
    // Clear and recreate viewer
    container.innerHTML = '';
    viewer = $3Dmol.createViewer(container, {backgroundColor: '0x1e1e1e'});

    var pdb = pdbTexts[protein];
    var meta = proteinMeta[protein];
    var scores = meta.scores;

    viewer.addModel(pdb, 'pdb');

    // Compute score range
    var vals = Object.values(scores);
    var vmin = Math.min.apply(null, vals);
    var vmax = Math.max.apply(null, vals);

    // Color by projection score
    var style = document.getElementById('style-select').value;
    var styleSpec = {};
    styleSpec[style] = {
        colorfunc: function(atom) {
            var resid = atom.resi;
            if (scores.hasOwnProperty(resid)) {
                return scoreToColor(scores[resid], vmin, vmax);
            }
            return 0x666666;  // gray for unmapped
        }
    };
    viewer.setStyle({}, styleSpec);

    if (showHighlights) {
        applyHighlights(meta, style);
    }

    // Hover: show residue info on mouseover
    var tooltip = document.getElementById('hover-tooltip');
    var curProtein = protein;
    viewer.setHoverable({}, true,
        function(atom, viewer, event, container) {
            if (!atom) return;
            var m = proteinMeta[curProtein];
            var resid = atom.resi;
            var seqpos = m.resid_to_seqpos[resid];
            var aa = m.resid_to_aa[resid] || atom.resn;
            var sse = m.resid_to_sse[resid] || '?';
            var sseLabel = sse === 'E' ? 'strand' : (sse === 'H' ? 'helix' : 'coil');
            var proj = m.scores[resid];
            var projStr = (proj !== undefined) ? proj.toFixed(3) : 'N/A';
            var isAnchor = (resid === m.anchor_resid);
            var isSS1 = m.ss1_resids.indexOf(resid) >= 0;
            var isSS2 = m.ss2_resids.indexOf(resid) >= 0;
            var tags = [];
            if (isAnchor) tags.push('<span style="color:#ffff00">ANCHOR</span>');
            if (isSS1) tags.push('<span style="color:#ff8c00">SS1</span>');
            if (isSS2) tags.push('<span style="color:#9932cc">SS2</span>');
            var tagStr = tags.length ? ' [' + tags.join(', ') + ']' : '';
            tooltip.innerHTML = '<b>' + aa + seqpos + '</b> (PDB ' + resid + ')' + tagStr + '<br>' +
                'Proj: <b>' + projStr + '</b> | SSE: ' + sseLabel;
            tooltip.style.display = 'block';
        },
        function(atom) {
            tooltip.style.display = 'none';
        }
    );

    viewer.zoomTo();
    viewer.render();

    // Update info
    var anchorScore = meta.anchor_resid ? (scores[meta.anchor_resid] || 'N/A') : 'N/A';
    if (typeof anchorScore === 'number') anchorScore = anchorScore.toFixed(3);
    var info = '<b>' + protein + '</b> | ' +
        meta.n_residues + ' residues | ' +
        'Anchor: pos ' + meta.anchor_seqpos + ' (PDB resid ' + meta.anchor_resid + ', proj=' + anchorScore + ') | ' +
        'SS1 center: pos ' + meta.ss1_center + ' | SS2 center: pos ' + meta.ss2_center + ' | ' +
        'Score range: [' + vmin.toFixed(3) + ', ' + vmax.toFixed(3) + ']';
    document.getElementById('info').innerHTML = info;

    // Update colorbar labels
    document.querySelector('#colorbar span:first-child').textContent = vmin.toFixed(2);
    document.querySelector('#colorbar span:last-child').textContent = vmax.toFixed(2);
}

function applyHighlights(meta, style) {
    // SS1 segment - orange
    if (meta.ss1_resids.length > 0) {
        var ss1Spec = {};
        ss1Spec[style] = {color: '0xff8c00'};
        viewer.setStyle({resi: meta.ss1_resids}, ss1Spec);
    }

    // SS2 segment - purple
    if (meta.ss2_resids.length > 0) {
        var ss2Spec = {};
        ss2Spec[style] = {color: '0x9932cc'};
        viewer.setStyle({resi: meta.ss2_resids}, ss2Spec);
    }

    // Anchor - yellow, shown as sphere regardless of style
    if (meta.anchor_resid) {
        viewer.setStyle({resi: [meta.anchor_resid]}, {
            sphere: {color: '0xffff00', radius: 0.8},
            stick: {color: '0xffff00'}
        });
        // Add label
        viewer.addLabel(
            'ANCHOR',
            {
                backgroundColor: '0x333333',
                fontColor: '0xffff00',
                fontSize: 12,
                backgroundOpacity: 0.8,
                position: {resi: meta.anchor_resid}
            },
            {resi: [meta.anchor_resid], atom: 'CA'}
        );
    }
}

function toggleHighlights() {
    showHighlights = !showHighlights;
    var protein = document.getElementById('protein-select').value;
    loadProtein(protein);
}

document.getElementById('protein-select').addEventListener('change', function() {
    loadProtein(this.value);
});
document.getElementById('style-select').addEventListener('change', function() {
    var protein = document.getElementById('protein-select').value;
    loadProtein(protein);
});

// Initial load
loadProtein(document.getElementById('protein-select').value);
""")

    html.append("</script>")
    html.append("</body></html>")

    out_path = REPORT_DIR / "anchor_structure_viewer.html"
    with open(out_path, "w") as f:
        f.write("\n".join(html))
    print(f"Saved: {out_path}")
    print(f"File size: {out_path.stat().st_size / 1024 / 1024:.1f} MB")
    print("Done.")


if __name__ == "__main__":
    main()
