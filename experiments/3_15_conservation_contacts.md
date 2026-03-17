
Hypotheses: plms struggle to predict contacts between conserved residue pairs 

this has `data/TARGET_b0.3/align/TARGET_b0.3_frequencies.csv` a conservation column for each residue in 2b61a

have structure files downloaded in `data/TARGET_b0.3` - we have .cif, and .pdb 

this snippet can convert the structure file to contacts i think: 

```
import numpy as np
from Bio.PDB import PDBParser, is_aa

def pdb_to_contact_matrix(
    pdb_path,
    chain_id=None,
    cutoff=8.0,
    min_seq_sep=0,
):
    """
    Build a residue-residue contact matrix from a PDB file.

    Contact definition:
      - use CB atom for each residue
      - use CA for glycine
      - residues are in contact if distance <= cutoff

    Args:
        pdb_path: path to PDB file
        chain_id: optional chain ID, e.g. "A". If None, uses all protein residues.
        cutoff: distance threshold in Angstroms
        min_seq_sep: optional minimum |i-j| sequence separation to count as contact

    Returns:
        contacts: (N, N) uint8 matrix with 1 for contact, 0 otherwise
        distances: (N, N) float matrix of anchor-atom distances
        residue_labels: list like ["A:GLY:42", ...]
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_path)

    residues = []
    coords = []
    residue_labels = []

    for model in structure:
        for chain in model:
            if chain_id is not None and chain.id != chain_id:
                continue

            for res in chain:
                if not is_aa(res, standard=True):
                    continue

                resname = res.get_resname()
                # glycine has no CB, so fall back to CA
                atom_name = "CA" if resname == "GLY" else "CB"

                if atom_name not in res:
                    # skip residues with missing anchor atom
                    continue

                coord = res[atom_name].get_coord()
                resid = res.id[1]   # residue number
                label = f"{chain.id}:{resname}:{resid}"

                residues.append(res)
                coords.append(coord)
                residue_labels.append(label)

        # only first model by default
        break

    coords = np.asarray(coords, dtype=float)
    n = len(coords)

    if n == 0:
        raise ValueError("No usable amino-acid residues found in the PDB.")

    # pairwise Euclidean distances
    diff = coords[:, None, :] - coords[None, :, :]
    distances = np.sqrt(np.sum(diff * diff, axis=-1))

    contacts = (distances <= cutoff).astype(np.uint8)

    # remove self-contacts
    np.fill_diagonal(contacts, 0)

    # optionally exclude nearby sequence neighbors
    if min_seq_sep > 0:
        for i in range(n):
            for j in range(n):
                if abs(i - j) < min_seq_sep:
                    contacts[i, j] = 0

    return contacts, distances, residue_labels


if __name__ == "__main__":
    contacts, distances, labels = pdb_to_contact_matrix(
        "example.pdb",
        chain_id="A",      # or None
        cutoff=8.0,
        min_seq_sep=6,     # often useful if you care about nonlocal contacts
    )

    print("Matrix shape:", contacts.shape)
    print("Number of contacts:", contacts.sum() // 2)

    # Example: list contacting pairs
    pairs = np.argwhere(np.triu(contacts, k=1) == 1)
    for i, j in pairs[:20]:
        print(labels[i], labels[j], f"{distances[i, j]:.2f} Å")
```

we also have the couplings from EVcouplings in data/TARGET_b0.3/couplings/TARGET_b0.3_CouplingScores_longrange.csv and data/TARGET_b0.3/couplings/TARGET_b0.3_CouplingScores.csv

we also have the contact calc from esm in `contact_pattern_v2.py` 

1. get the ground truth contacts from pdb
2. get esm contact predictions on the full sequence and show how good it is
3. for the predictions, is it harder to predict the contacts between conserved pairs? 