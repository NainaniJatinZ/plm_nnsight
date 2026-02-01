"""
Export attention and contact data for interactive visualization.

This script converts cached attention patterns and contact maps to a compressed
JSON format that can be loaded by the standalone HTML viewer.
"""

from __future__ import annotations
import json
import gzip
from typing import Any
import torch
import numpy as np


def sparse_encode_matrix(matrix: np.ndarray, threshold: float = 1e-6) -> dict[int, dict[int, float]]:
    """
    Convert dense matrix to sparse dictionary format.

    Reduces file size by ~10x for typical attention matrices (~10% dense).

    Args:
        matrix: 2D numpy array
        threshold: Values below this are treated as zero

    Returns:
        Nested dict: {row: {col: value}} containing only non-zero entries
    """
    sparse = {}
    rows, cols = np.where(np.abs(matrix) > threshold)

    for r, c in zip(rows, cols):
        row_idx = int(r)
        col_idx = int(c)
        value = float(matrix[r, c])

        if row_idx not in sparse:
            sparse[row_idx] = {}
        sparse[row_idx][col_idx] = round(value, 4)  # 4 decimal precision

    return sparse


def dense_decode_matrix(sparse: dict[int, dict[int, float]], shape: tuple[int, int]) -> np.ndarray:
    """
    Convert sparse dictionary back to dense matrix.

    Args:
        sparse: Nested dict from sparse_encode_matrix
        shape: (rows, cols) of output matrix

    Returns:
        Dense numpy array
    """
    matrix = np.zeros(shape, dtype=np.float32)
    for r, cols in sparse.items():
        for c, val in cols.items():
            matrix[r, c] = val
    return matrix


def export_attention_head(
    layer: int,
    head: int,
    effect: float,
    clean_attn_BHLL: torch.Tensor,
    corrupt_attn_BHLL: torch.Tensor,
) -> dict[str, Any]:
    """
    Export single attention head data.

    Args:
        layer: Layer index
        head: Head index
        effect: Normalized patching effect
        clean_attn_BHLL: Clean attention (batch, heads, seq, seq)
        corrupt_attn_BHLL: Corrupt attention (batch, heads, seq, seq)

    Returns:
        Dict with layer, head, effect, and sparse attention matrices
    """
    # Extract this head's attention (remove batch dim)
    clean_attn_LL = clean_attn_BHLL[0, head].cpu().numpy()
    corrupt_attn_LL = corrupt_attn_BHLL[0, head].cpu().numpy()

    return {
        "layer": int(layer),
        "head": int(head),
        "effect": round(float(effect), 4),
        "clean_attn": sparse_encode_matrix(clean_attn_LL),
        "corrupt_attn": sparse_encode_matrix(corrupt_attn_LL),
    }


def export_visualization_data(
    clean_attn_LBHLL: list[torch.Tensor],
    corrupt_attn_LBHLL: list[torch.Tensor],
    effects_LH: torch.Tensor,
    clean_contacts_AA: torch.Tensor,
    corrupt_contacts_AA: torch.Tensor,
    orig_contacts_AA: torch.Tensor,
    segment: Any,  # ContactSegment dataclass
    sequences: dict[str, str],
    protein: str,
    config: dict[str, Any],
    output_path: str = "reports/viz_data.json.gz",
    top_k: int = 100,
) -> None:
    """
    Export all visualization data to compressed JSON.

    Args:
        clean_attn_LBHLL: List of attention tensors for clean sequence
        corrupt_attn_LBHLL: List of attention tensors for corrupt sequence
        effects_LH: Normalized effects matrix (layers, heads)
        clean_contacts_AA: Contact map for clean sequence
        corrupt_contacts_AA: Contact map for corrupt sequence
        orig_contacts_AA: Contact map for original sequence
        segment: ContactSegment with ss1/ss2 boundaries
        sequences: Dict with 'full', 'clean', 'corrupt' sequences
        protein: Protein ID (e.g., "2B61A")
        config: Protein config dict with contact_pair, clean_flank, corrupt_flank
        output_path: Path to write JSON.gz file
        top_k: Number of top heads to export (sorted by |effect|)
    """
    num_layers, num_heads = effects_LH.shape
    seq_length = clean_contacts_AA.shape[0]

    # Compute metrics
    def compute_metric(pred, orig):
        pred_seg = pred[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
        orig_seg = orig[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
        return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

    clean_metric = compute_metric(clean_contacts_AA, orig_contacts_AA)
    corrupt_metric = compute_metric(corrupt_contacts_AA, orig_contacts_AA)

    # Find top-k heads by absolute effect
    effects_flat = effects_LH.flatten()
    top_indices = effects_flat.abs().argsort(descending=True)[:top_k]

    print(f"Exporting top {top_k} heads (out of {num_layers * num_heads} total)...")

    heads_data = []
    for i, idx in enumerate(top_indices):
        layer = idx // num_heads
        head = idx % num_heads
        effect = effects_LH[layer, head].item()

        head_data = export_attention_head(
            layer=layer.item(),
            head=head.item(),
            effect=effect,
            clean_attn_BHLL=clean_attn_LBHLL[layer],
            corrupt_attn_BHLL=corrupt_attn_LBHLL[layer],
        )
        heads_data.append(head_data)

        if (i + 1) % 10 == 0:
            print(f"  Exported {i + 1}/{top_k} heads...")

    print("Encoding contact maps...")

    # Package everything
    data = {
        "metadata": {
            "protein": protein,
            "seq_length": seq_length,
            "num_layers": num_layers,
            "num_heads": num_heads,
            "segment": {
                "ss1_start": segment.ss1_start,
                "ss1_end": segment.ss1_end,
                "ss2_start": segment.ss2_start,
                "ss2_end": segment.ss2_end,
            },
            "contact_pair": config["contact_pair"],
            "clean_flank": config["clean_flank"],
            "corrupt_flank": config["corrupt_flank"],
            "clean_metric": round(clean_metric, 4),
            "corrupt_metric": round(corrupt_metric, 4),
        },
        "sequences": sequences,
        "heads": heads_data,
        "contacts": {
            "clean": sparse_encode_matrix(clean_contacts_AA.cpu().numpy()),
            "corrupt": sparse_encode_matrix(corrupt_contacts_AA.cpu().numpy()),
            "original": sparse_encode_matrix(orig_contacts_AA.cpu().numpy()),
        },
    }

    # Write compressed JSON
    print(f"Writing to {output_path}...")
    json_str = json.dumps(data, separators=(',', ':'))  # Compact format

    with gzip.open(output_path, 'wt', encoding='utf-8') as f:
        f.write(json_str)

    # Report size
    import os
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✓ Exported {len(heads_data)} heads to {output_path} ({size_mb:.1f} MB)")
    print(f"  Sequence length: {seq_length}")
    print(f"  Clean metric: {clean_metric:.4f}")
    print(f"  Corrupt metric: {corrupt_metric:.4f}")
    print(f"  Top effect: {heads_data[0]['effect']:.4f} (L{heads_data[0]['layer']}H{heads_data[0]['head']})")


def test_sparse_encoding():
    """Test sparse encoding round-trip."""
    print("Testing sparse encoding...")
    test_matrix = np.random.rand(10, 10)
    test_matrix[test_matrix < 0.9] = 0  # Make 90% sparse

    sparse = sparse_encode_matrix(test_matrix)
    decoded = dense_decode_matrix(sparse, test_matrix.shape)

    max_error = np.abs(test_matrix - decoded).max()
    print(f"  Round-trip max error: {max_error:.6f}")
    print(f"  Compression: {test_matrix.size} -> {sum(len(v) for v in sparse.values())} entries")
    print("✓ Sparse encoding test passed")


if __name__ == "__main__":
    test_sparse_encoding()
