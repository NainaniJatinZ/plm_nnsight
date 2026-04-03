# Expanded Anchor Feature Regression (experiments/3_25_anchor_regression_v2.md)

## Context

From v1 regression we know (script scripts/anchor_regression.py, output reports/outputs/multi_protein/anchor_regression.md):
- Key-side search direction (W_K^T @ q_mean for L10H9) correctly ranks anchor #1.
- SSE (strand+), conservation, and hydrophobic AA identity explain R²=0.25.
- Anchors are 5–8σ outliers even after full biological model — 75% unexplained.
- Plot D shows sharp spikes at specific beta-strand positions, not all strands.
- Layer-wise decomposition shows the feature is built contextually in layers 7–9.

**Goal:** Push R² higher with structural features computable from PDB coordinates.
Test hypotheses: solvent accessibility, local hydrophobic context, 3D contact number,
and nonlinear interaction effects.

## Previous experiments (reference these)

- `scripts/anchor_regression.py` — v1 regression. Has the search direction computation,
  projection score calculation, and full regression pipeline. **Extend this script.**
  Key variables to reuse:
  - `key_search_dir`: the 1280-dim key-side search direction (W_K^T @ q_mean_unit)
  - `proj_scores`: per-residue projection scores on full sequence
  - The existing feature matrix (SSE, AA identity, conservation, position features)
- `scripts/anchor_interp_v2.py` — model loading, residual stream capture
- PDB files: check `data/` directory or wherever PDBs are stored. The user has ~15
  proteins with PDB files now.

## Data available

- Original 5 proteins with full pipeline: 1BRTA, 1PVGA, 2B61A, 2DPMA, 2PKEA
- ~10 additional proteins with PDB files but NO conservation scores yet
- PDB structures: locate in project directory (check `data/pdbs/` or similar)
- Sequences: `data/full_seq_dict.json`
- SSE: `data/ss_dict.json`
- Anchor positions for L10H9 — discover from summary CSVs as before

## New features to compute

### Feature 1: Relative Solvent Accessibility (RSA)

Compute per-residue RSA from PDB using DSSP.

```python
from Bio.PDB import PDBParser, DSSP

parser = PDBParser(QUIET=True)
structure = parser.get_structure(protein_id, pdb_path)
model = structure[0]
dssp = DSSP(model, pdb_path, dssp='mkdssp')  # or dssp='dssp'

# dssp returns: (index, AA, SSE, RSA, phi, psi, ...)
# RSA = relative solvent accessibility (0-1 scale, 0=fully buried, 1=fully exposed)
for key in dssp:
    residue_index = key[1][1]  # residue sequence number
    rsa = dssp[key][3]         # relative ASA
```

**Important:** Map DSSP residue numbering to your 0-indexed sequence positions.
PDB residue numbering may not start at 0 or 1 — align by matching amino acid
sequences. Use a simple sequence alignment or match by AA identity.

**Install if needed:** `pip install biopython mkdssp` or check if dssp binary is
available. If DSSP is not installable, use the simpler Shrake-Rupley method:
```python
from Bio.PDB import ShrakeRupley
sr = ShrakeRupley()
sr.compute(structure[0], level="R")
# Then normalize by max ASA per residue type (Tien et al. 2013 values)
```

### Feature 2: Local Hydrophobic Context

For each residue at position i, compute:

```python
HYDROPHOBIC = set('AILMFWVP')  # or use a continuous scale

# Binary context: count hydrophobic neighbors
n_hydrophobic_pm1 = sum(1 for d in [-1, 1] if seq[i+d] in HYDROPHOBIC)
n_hydrophobic_pm2 = sum(1 for d in [-2, -1, 1, 2] if seq[i+d] in HYDROPHOBIC)
n_hydrophobic_pm3 = sum(1 for d in [-3, -2, -1, 1, 2, 3] if seq[i+d] in HYDROPHOBIC)

# Continuous context: use Kyte-Doolittle hydrophobicity scale
KD = {'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
      'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
      'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
      'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2}

# Local hydrophobicity (window average)
local_hydro_w3 = mean(KD[seq[i+d]] for d in [-1, 0, 1])
local_hydro_w5 = mean(KD[seq[i+d]] for d in [-2, -1, 0, 1, 2])
local_hydro_w7 = mean(KD[seq[i+d]] for d in [-3, -2, -1, 0, 1, 2, 3])

# Self hydrophobicity
self_hydro = KD[seq[i]]

# Beta-strand alternating pattern: same-face neighbors at ±2
# (in beta strands, residues at ±2 point to the same face of the sheet)
same_face_hydro = mean(KD[seq[i+d]] for d in [-2, 0, 2])
```

Handle boundary cases (positions near start/end of sequence) by using only available
neighbors.

### Feature 3: 3D Contact Number

From PDB coordinates, count contacts per residue:

```python
from Bio.PDB import PDBParser, NeighborSearch

parser = PDBParser(QUIET=True)
structure = parser.get_structure(protein_id, pdb_path)
model = structure[0]

# Get all CB atoms (CA for glycine)
atoms = []
res_indices = []
for chain in model:
    for residue in chain:
        if residue.id[0] != ' ':  # skip heteroatoms
            continue
        if 'CB' in residue:
            atoms.append(residue['CB'])
        elif 'CA' in residue:
            atoms.append(residue['CA'])
        res_indices.append(residue.id[1])

ns = NeighborSearch([a for a in atoms])

# Per-residue contact counts at different thresholds
for i, atom in enumerate(atoms):
    contacts_8A = len(ns.search(atom.get_vector(), 8.0, level='R')) - 1
    contacts_10A = len(ns.search(atom.get_vector(), 10.0, level='R')) - 1

# Long-range contacts: |i-j| > 12 in sequence
for i, atom_i in enumerate(atoms):
    neighbors = ns.search(atom_i.get_vector(), 8.0, level='R')
    long_range_contacts = sum(1 for n in neighbors
                              if abs(res_indices[atoms.index(n)] - res_indices[i]) > 12)
```

**Map PDB residue numbers to 0-indexed sequence positions** — same alignment issue as
DSSP. Be careful here.

### Feature 4: Beta-sheet specific features (if DSSP gives sheet info)

DSSP assigns sheet labels (A, B, C...) and bridge partners. If accessible:
- `n_sheet_hbonds`: number of backbone H-bonds to other strands
- `in_interior_strand`: 1 if the strand has strands on both sides (vs edge strand)
- `sheet_size`: number of strands in the sheet this residue belongs to

These may be hard to extract cleanly from DSSP output. Only attempt if the simpler
features don't push R² high enough. Low priority.

## Method

### Step 1: Compute all new features for all available proteins

For each protein with a PDB file:
1. Run DSSP → get per-residue RSA
2. Compute local hydrophobic context from sequence
3. Compute 3D contact numbers from PDB coordinates
4. Align PDB residue numbering to 0-indexed sequence positions

Store as a DataFrame: one row per residue, columns = all features.

### Step 2: Compute projection scores

Same as v1: run forward pass on full unmasked sequence, compute
`proj_score = dot(x_ln_layer10, key_search_dir)` for each position.

For the ~10 new proteins: you need to run the model forward pass to get residual
streams at layer 10. Reuse the capture pattern from anchor_interp_v2.py.

For anchor identification on new proteins: discover from summary CSVs if available,
or identify as the argmax of projection score (since we know the anchor = rank 1).

### Step 3: Expanded linear regression

Run on all proteins combined (those with conservation and those without — handle
missing conservation by running separate models or imputing).

**Model A: v1 baseline (SSE + protein FE)**
R² reference from v1: 0.089

**Model B: + RSA**
```
proj ~ SSE_E + SSE_H + RSA + protein_FE
```

**Model C: + RSA + local hydrophobic context**
```
proj ~ SSE_E + SSE_H + RSA + self_hydro + local_hydro_w5 + same_face_hydro
       + protein_FE
```

**Model D: + RSA + local context + 3D contact number**
```
proj ~ SSE_E + SSE_H + RSA + self_hydro + local_hydro_w5 + same_face_hydro
       + contacts_8A + long_range_contacts + protein_FE
```

**Model E: + conservation + AA identity (subset with conservation data)**
```
proj ~ SSE_E + SSE_H + RSA + self_hydro + local_hydro_w5 + same_face_hydro
       + contacts_8A + long_range_contacts + conservation + AA_dummies + protein_FE
```

**Model F: kitchen sink without AA dummies (all proteins)**
```
proj ~ SSE_E + SSE_H + RSA + self_hydro + local_hydro_w5 + same_face_hydro
       + contacts_8A + long_range_contacts + protein_FE
```
This runs on ALL proteins including those without conservation, maximizing N.

### Step 4: Random forest / gradient boosted model

Use the same features as Model D or F but with a nonlinear model to capture
interactions:

```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import cross_val_score

features = ['SSE_E', 'SSE_H', 'RSA', 'self_hydro', 'local_hydro_w5',
            'same_face_hydro', 'contacts_8A', 'long_range_contacts',
            'dist_to_boundary', 'seg_len']

rf = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42)
cv_scores = cross_val_score(rf, X[features], y, cv=5, scoring='r2')
print(f"RF CV R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

# Feature importance
rf.fit(X[features], y)
importances = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
```

If RF R² >> OLS R², interaction effects matter. Report feature importances.

### Step 5: Anchor residual analysis (same as v1)

For the best model, check anchor residuals:
- Are anchors still outliers? By how many sigma?
- If anchors are within 2σ of prediction → the features explain anchor selection
- If anchors are still 4σ+ outliers → model-internal signal beyond these features

### Step 6: Visualization

**Plot E: Projection score vs RSA (scatter)**
- Color by SSE type. If there's a clean negative correlation (buried = high score),
  that's the finding.

**Plot F: Projection score vs 3D contact number (scatter)**
- If positive correlation → structurally central positions score higher.

**Plot G: Updated sequence profile (like Plot D) with RSA overlay**
- Second y-axis showing RSA. Do the projection peaks correspond to RSA valleys
  (buried positions)?

**Plot H: Feature importance bar chart from Random Forest**

## Output

- `reports/outputs/multi_protein/anchor_regression_v2.md` — full regression tables
- `reports/outputs/multi_protein/anchor_regression_v2_*.png` — plots
- Summary: which features explain the most variance? Is the anchor now predicted?

## Execution

```bash
uv run python scripts/anchor_regression_v2.py --device cuda
```

Dependencies: `pip install biopython scikit-learn statsmodels`
For DSSP: `pip install mkdssp` or ensure `dssp` binary is on PATH.
If DSSP installation fails, use Bio.PDB.ShrakeRupley as fallback (see Feature 1).

PDB files: check project directory for PDB locations. May need to download via:
```python
from Bio.PDB import PDBList
pdbl = PDBList()
pdbl.retrieve_pdb_file('2B61', pdir='data/pdbs/', file_format='pdb')
```

Estimated runtime: ~20 min (model forward passes for new proteins + PDB parsing +
regression).

## Verification

1. RSA at anchor positions should be low (buried) if the burial hypothesis is correct.
2. Contact number at anchor positions should be high if the structural hub hypothesis
   is correct.
3. R² should increase monotonically A → B → C → D.
4. RF R² should be ≥ OLS R² (nonlinear model can only do better with same features).
5. If RF R² >> OLS R², report the interaction effects via feature importance.
6. Anchor residuals: the key metric. Report sigma for best linear and best RF model.