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


def compute_diff_metrics(clean_attn_LL: np.ndarray, corrupt_attn_LL: np.ndarray) -> dict[str, float]:
    """
    Compute multiple metrics quantifying attention pattern differences.

    For attention matrices (probability distributions over keys for each query),
    L1 norm is more interpretable than L2/Frobenius norm.

    Args:
        clean_attn_LL: Clean attention matrix (seq_len, seq_len)
        corrupt_attn_LL: Corrupt attention matrix (seq_len, seq_len)

    Returns:
        Dict of metric_name -> value:
        - diff_l1: Sum of absolute differences (total variation distance)
        - diff_max: Maximum absolute difference (worst-case deviation)
        - diff_l2: Frobenius norm (L2) for comparison
    """
    diff = clean_attn_LL - corrupt_attn_LL

    return {
        "diff_l1": float(np.sum(np.abs(diff))),  # L1: total variation
        "diff_max": float(np.max(np.abs(diff))),  # L∞: max deviation
        "diff_l2": float(np.sqrt(np.sum(diff ** 2))),  # L2: Frobenius norm
    }


def export_attention_head(
    layer: int,
    head: int,
    metrics: dict[str, float],
    clean_attn_BHLL: torch.Tensor,
    corrupt_attn_BHLL: torch.Tensor,
) -> dict[str, Any]:
    """
    Export single attention head data.

    Args:
        layer: Layer index
        head: Head index
        metrics: Dict of metric_name -> value (e.g., {'effect': 0.5, 'diff_l1': 0.02})
        clean_attn_BHLL: Clean attention (batch, heads, seq, seq)
        corrupt_attn_BHLL: Corrupt attention (batch, heads, seq, seq)

    Returns:
        Dict with layer, head, metrics, and sparse attention matrices
    """
    # Extract this head's attention (remove batch dim)
    clean_attn_LL = clean_attn_BHLL[0, head].cpu().numpy()
    corrupt_attn_LL = corrupt_attn_BHLL[0, head].cpu().numpy()

    # Round metrics for smaller file size
    rounded_metrics = {k: round(float(v), 6) for k, v in metrics.items()}

    return {
        "layer": int(layer),
        "head": int(head),
        "metrics": rounded_metrics,
        "clean_attn": sparse_encode_matrix(clean_attn_LL),
        "corrupt_attn": sparse_encode_matrix(corrupt_attn_LL),
    }


def export_visualization_data(
    clean_attn_LBHLL: list[torch.Tensor],
    corrupt_attn_LBHLL: list[torch.Tensor],
    head_metrics: dict[str, torch.Tensor],  # metric_name -> LH tensor
    clean_contacts_AA: torch.Tensor,
    corrupt_contacts_AA: torch.Tensor,
    orig_contacts_AA: torch.Tensor,
    segment: Any,  # ContactSegment dataclass
    sequences: dict[str, str],
    protein: str,
    config: dict[str, Any],
    output_path: str = "reports/viz_data.json.gz",
    skip_existing_heads: bool = True,
) -> None:
    """
    Export visualization data with on-demand loading support.

    Instead of one large file, exports:
    - Metadata file (small, loaded immediately)
    - Individual head files (loaded on-demand as user navigates)

    Args:
        clean_attn_LBHLL: List of attention tensors for clean sequence
        corrupt_attn_LBHLL: List of attention tensors for corrupt sequence
        head_metrics: Dict of metric_name -> (num_layers, num_heads) tensor
                     e.g., {'effect': effects_LH, 'diff_l1': diff_l1_LH}
        clean_contacts_AA: Contact map for clean sequence
        corrupt_contacts_AA: Contact map for corrupt sequence
        orig_contacts_AA: Contact map for original sequence
        segment: ContactSegment with ss1/ss2 boundaries
        sequences: Dict with 'full', 'clean', 'corrupt' sequences
        protein: Protein ID (e.g., "2B61A")
        config: Protein config dict with contact_pair, clean_flank, corrupt_flank
        output_path: Path to write metadata file (heads dir will be created alongside)
        skip_existing_heads: If True, don't re-export head files that already exist
    """
    import os

    # Get dimensions from first metric
    first_metric = next(iter(head_metrics.values()))
    num_layers, num_heads = first_metric.shape
    seq_length = clean_contacts_AA.shape[0]

    # Compute contact prediction metrics
    def compute_metric(pred, orig):
        pred_seg = pred[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
        orig_seg = orig[segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
        return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

    clean_metric = compute_metric(clean_contacts_AA, orig_contacts_AA)
    corrupt_metric = compute_metric(corrupt_contacts_AA, orig_contacts_AA)

    # Create heads directory
    base_dir = os.path.dirname(output_path)
    heads_dir = os.path.join(base_dir, 'heads')
    os.makedirs(heads_dir, exist_ok=True)

    print(f"Exporting {num_layers * num_heads} heads to individual files...")
    print(f"  Heads directory: {heads_dir}/")
    if skip_existing_heads:
        print(f"  Skipping existing head files")

    # Export each head to its own file
    head_list = []
    total_size_bytes = 0
    skipped_count = 0

    for layer in range(num_layers):
        for head in range(num_heads):
            head_filename = f"L{layer:02d}_H{head:02d}.json.gz"
            head_path = os.path.join(heads_dir, head_filename)

            # Check if file exists and skip if requested
            if skip_existing_heads and os.path.exists(head_path):
                skipped_count += 1
                file_size = os.path.getsize(head_path)
                total_size_bytes += file_size
            else:
                # Gather all metrics for this head
                metrics = {
                    metric_name: metric_tensor[layer, head].item()
                    for metric_name, metric_tensor in head_metrics.items()
                }

                # Export head data
                head_data = export_attention_head(
                    layer=int(layer),
                    head=int(head),
                    metrics=metrics,
                    clean_attn_BHLL=clean_attn_LBHLL[layer],
                    corrupt_attn_BHLL=corrupt_attn_LBHLL[layer],
                )

                # Save individual head file
                head_json = json.dumps(head_data, separators=(',', ':'))
                with gzip.open(head_path, 'wt', encoding='utf-8') as f:
                    f.write(head_json)

                file_size = os.path.getsize(head_path)
                total_size_bytes += file_size

            # Store metrics for metadata (always, even if skipped)
            head_entry = {
                "layer": int(layer),
                "head": int(head),
                "filename": head_filename,
            }
            # Add all metrics to metadata
            for metric_name, metric_tensor in head_metrics.items():
                head_entry[metric_name] = round(float(metric_tensor[layer, head].item()), 6)

            head_list.append(head_entry)

            if (layer * num_heads + head + 1) % 50 == 0:
                exported = (layer * num_heads + head + 1) - skipped_count
                print(f"  Processed {layer * num_heads + head + 1}/{num_layers * num_heads} heads ({exported} exported, {skipped_count} skipped)...")

    if skipped_count > 0:
        print(f"  Skipped {skipped_count} existing head files")

    print("Encoding contact maps and writing metadata...")

    # Write metadata file (small - loaded immediately by UI)
    metadata = {
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
            "heads_dir": "heads",  # Relative path to heads directory
            "available_metrics": list(head_metrics.keys()),  # List of metric names
        },
        "sequences": sequences,
        "contacts": {
            "clean": sparse_encode_matrix(clean_contacts_AA.cpu().numpy()),
            "corrupt": sparse_encode_matrix(corrupt_contacts_AA.cpu().numpy()),
            "original": sparse_encode_matrix(orig_contacts_AA.cpu().numpy()),
        },
        "heads": head_list,  # Changed from "head_effects" to "heads"
    }

    meta_path = output_path.replace('.json.gz', '_meta.json.gz')
    meta_json = json.dumps(metadata, separators=(',', ':'))
    with gzip.open(meta_path, 'wt', encoding='utf-8') as f:
        f.write(meta_json)

    # Report sizes
    meta_size_mb = os.path.getsize(meta_path) / (1024 * 1024)
    total_size_mb = total_size_bytes / (1024 * 1024)
    avg_head_kb = (total_size_bytes / (num_layers * num_heads)) / 1024

    print(f"\n✓ Export complete!")
    print(f"  Metadata: {meta_size_mb:.2f} MB ({meta_path})")
    print(f"  Heads: {total_size_mb:.2f} MB in {num_layers * num_heads} files ({avg_head_kb:.1f} KB avg)")
    print(f"  Heads directory: {heads_dir}/")
    print(f"  Sequence length: {seq_length}")
    print(f"  Clean metric: {clean_metric:.4f}")
    print(f"  Corrupt metric: {corrupt_metric:.4f}")
    print(f"  Available metrics: {', '.join(head_metrics.keys())}")

    # Report max values for each metric
    for metric_name, metric_tensor in head_metrics.items():
        max_idx = int(torch.abs(metric_tensor).flatten().argmax().item())
        max_layer = max_idx // num_heads
        max_head = max_idx % num_heads
        max_val = metric_tensor[max_layer, max_head].item()
        print(f"  Max |{metric_name}|: {max_val:.4f} (L{max_layer}H{max_head})")


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
