#!/usr/bin/env python3
"""
Analyze ESM2 attention heads responsible for contact prediction flank sensitivity.

This script:
1. Computes attention for clean/corrupt flank sequences (with caching)
2. Performs attention patching to identify important heads
3. Exports visualization data for interactive HTML viewer
"""

from __future__ import annotations
import argparse
import gc
import gzip
import json
import os
from dataclasses import dataclass
from typing import Any

import numpy as np
import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer


# =============================================================================
# Configuration
# =============================================================================
PROTEINS = {
    "2B61A": {"contact_pair": (182, 316), "clean_flank": 44, "corrupt_flank": 43},
    "1PVGA": {"contact_pair": (101, 202), "clean_flank": 65, "corrupt_flank": 63},
}
SEGMENT_RADIUS = 5


# =============================================================================
# Data Structures
# =============================================================================
@dataclass
class ContactSegment:
    ss1_start: int
    ss1_end: int
    ss2_start: int
    ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int = SEGMENT_RADIUS):
        return cls(pos1 - radius, pos1 + radius + 1, pos2 - radius, pos2 + radius + 1)


# =============================================================================
# Utilities
# =============================================================================
def log_memory(label: str = ""):
    if torch.cuda.is_available():
        alloc = torch.cuda.memory_allocated() / 1e9
        resv = torch.cuda.memory_reserved() / 1e9
        print(f"[Memory - {label}] Allocated: {alloc:.2f} GB, Reserved: {resv:.2f} GB")


def clear_memory():
    gc.collect()
    torch.cuda.empty_cache()


def get_cache_path(protein: str, clean_flank: int, corrupt_flank: int, cache_dir: str) -> str:
    os.makedirs(cache_dir, exist_ok=True)
    return f"{cache_dir}/{protein}_c{clean_flank}_x{corrupt_flank}_metrics.pt"


def save_metrics_cache(
    protein: str,
    clean_flank: int,
    corrupt_flank: int,
    metrics: dict[str, torch.Tensor],
    cache_dir: str,
) -> None:
    cache_path = get_cache_path(protein, clean_flank, corrupt_flank, cache_dir)
    cache_data = {
        "protein": protein,
        "clean_flank": clean_flank,
        "corrupt_flank": corrupt_flank,
        "metrics": metrics,
    }
    torch.save(cache_data, cache_path)
    print(f"Saved metrics cache to {cache_path}")
    print(f"  Cached metrics: {', '.join(metrics.keys())}")


def load_metrics_cache(
    protein: str, clean_flank: int, corrupt_flank: int, cache_dir: str
) -> dict[str, torch.Tensor] | None:
    cache_path = get_cache_path(protein, clean_flank, corrupt_flank, cache_dir)

    if not os.path.exists(cache_path):
        return None

    try:
        cache_data = torch.load(cache_path)
        print(f"Loaded metrics cache from {cache_path}")
        print(f"  Cached metrics: {', '.join(cache_data['metrics'].keys())}")
        return cache_data["metrics"]
    except Exception as e:
        print(f"Failed to load cache: {e}")
        return None


# =============================================================================
# Sequence Masking
# =============================================================================
def mask_with_flanks(seq_S: str, segment: ContactSegment, flank_size: int) -> str:
    """Mask sequence except for contact segments and flanking regions."""
    seq_len = len(seq_S)
    masked_L: list[str] = ["<mask>"] * seq_len

    # Unmask contact segments
    masked_L[segment.ss1_start : segment.ss1_end] = list(
        seq_S[segment.ss1_start : segment.ss1_end]
    )
    masked_L[segment.ss2_start : segment.ss2_end] = list(
        seq_S[segment.ss2_start : segment.ss2_end]
    )

    # Unmask flanks
    left_flank_idxs = range(max(0, segment.ss1_start - flank_size), segment.ss1_start)
    right_flank_idxs = range(segment.ss2_end, min(seq_len, segment.ss2_end + flank_size))
    for i in left_flank_idxs:
        masked_L[i] = seq_S[i]
    for i in right_flank_idxs:
        masked_L[i] = seq_S[i]

    return "".join(masked_L)


# =============================================================================
# Contact Prediction
# =============================================================================
def compute_contact_map(model, tokenizer, sequence_S: str, device: str) -> torch.Tensor:
    """Compute contact predictions for a sequence."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        contacts_AA = model.predict_contacts(
            inputs_BL["input_ids"], inputs_BL["attention_mask"]
        )[0].cpu()
    return contacts_AA


def compute_contacts_from_attention(
    attn_list_BHLL: list[torch.Tensor],
    tokens_BL: torch.Tensor,
    attention_mask_BL: torch.Tensor,
    contact_head,
    device: str = "cuda",
) -> torch.Tensor:
    """Manually compute contacts from attention (enables interventions)."""
    attn_list_BHLL = [a.to(device) for a in attn_list_BHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)

    attns_BLHLL = torch.stack(attn_list_BHLL, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns_BLHLL = attns_BLHLL * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)

    return contact_head(tokens_BL, attns_BLHLL)


def patching_metric(
    pred_contacts_AA: torch.Tensor, orig_contacts_AA: torch.Tensor, segment: ContactSegment
) -> float:
    """Compute overlap metric between predicted and original contacts in segment."""
    pred_seg = pred_contacts_AA[
        segment.ss1_start : segment.ss1_end, segment.ss2_start : segment.ss2_end
    ]
    orig_seg = orig_contacts_AA[
        segment.ss1_start : segment.ss1_end, segment.ss2_start : segment.ss2_end
    ]
    return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()


# =============================================================================
# Attention Caching
# =============================================================================
def cache_attention(
    model, tokenizer, sequence_S: str, num_layers: int, device: str
) -> tuple[list[torch.Tensor], dict]:
    """Cache attention weights from all layers for a sequence."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    inputs_with_attn = {**inputs_BL, "output_attentions": True}

    with model.trace() as tracer:
        with tracer.invoke(**inputs_with_attn):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )

    attn_list_BHLL = []
    for layer_idx in range(num_layers):
        key = f"model.esm.encoder.layer.{layer_idx}.attention.self"
        attn_list_BHLL.append(attn_cache[key].output[1].detach().cpu())

    return attn_list_BHLL, inputs_BL


# =============================================================================
# Attention Patching
# =============================================================================
def compute_diff_metrics_torch(
    clean_attn_LL: torch.Tensor, corrupt_attn_LL: torch.Tensor
) -> dict[str, float | tuple[int, int]]:
    """Compute metrics quantifying attention pattern differences."""
    diff = clean_attn_LL - corrupt_attn_LL
    abs_diff = torch.abs(diff)

    # Find coordinates of max difference
    max_idx = torch.argmax(abs_diff)
    max_row = (max_idx // abs_diff.shape[1]).item()
    max_col = (max_idx % abs_diff.shape[1]).item()

    return {
        "diff_l1": torch.sum(abs_diff).item(),
        "diff_max": torch.max(abs_diff).item(),
        "diff_max_coord": (max_row, max_col),
        "diff_l2": torch.sqrt(torch.sum(diff**2)).item(),
    }


def indirect_effect_single_head(
    nnsight_model,
    clean_inputs_BL: dict,
    corrupt_head_attn_LL: torch.Tensor,
    patch_layer: int,
    patch_head: int,
    num_layers: int,
    num_heads: int,
    head_dim: int,
    B: int,
    L: int,
    device: str,
) -> list[torch.Tensor]:
    """Perform indirect effect patching for a single head in a single trace.

    Accesses V (child) and attention probs (parent) in the same trace,
    patches one head, recomputes context, and captures downstream attention.
    Uses tracer.cache() for reliable downstream capture.
    """
    with nnsight_model.trace() as tracer:
        with tracer.invoke(**{**clean_inputs_BL, "output_attentions": True}):
            # Child module first: get V
            v_raw = nnsight_model.esm.encoder.layer[patch_layer].attention.self.value.output
            v_heads = v_raw.reshape(B, L, num_heads, head_dim).transpose(1, 2)

            # Parent module: patch one head's attention
            orig_attn = nnsight_model.esm.encoder.layer[patch_layer].attention.self.output[1]
            patched_attn = orig_attn.clone()
            patched_attn[:, patch_head, :, :] = corrupt_head_attn_LL.to(device)

            # Recompute context with patched attention
            new_ctx = torch.matmul(patched_attn, v_heads)
            new_ctx = new_ctx.transpose(1, 2).contiguous().reshape(B, L, -1)

            # Set context — propagates through residual stream
            nnsight_model.esm.encoder.layer[patch_layer].attention.self.output[0][:] = new_ctx

            # Capture downstream attention
            downstream_cache = tracer.cache(
                modules=[
                    nnsight_model.esm.encoder.layer[i].attention.self
                    for i in range(patch_layer + 1, num_layers)
                ]
            )

    downstream_attn = []
    for i in range(patch_layer + 1, num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        downstream_attn.append(downstream_cache[key].output[1].detach().cpu())

    return downstream_attn


def compute_head_metrics(
    clean_attn_LBHLL: list[torch.Tensor],
    corrupt_attn_LBHLL: list[torch.Tensor],
    clean_inputs_BL: dict,
    clean_contacts_AA: torch.Tensor,
    corrupt_contacts_AA: torch.Tensor,
    orig_contacts_AA: torch.Tensor,
    segment: ContactSegment,
    contact_head,
    device: str,
    nnsight_model=None,
    head_dim: int = 0,
    force_recalc: bool = False,
    cache_dir: str = "reports/cache",
    protein: str = "",
    clean_flank: int = 0,
    corrupt_flank: int = 0,
) -> dict[str, torch.Tensor]:
    """Compute head metrics with caching support."""
    num_layers = len(clean_attn_LBHLL)
    num_heads = clean_attn_LBHLL[0].shape[1]

    required_metrics = {"effect", "indirect_effect", "diff_l1", "diff_max", "diff_l2"}
    # Note: diff_max_coord is stored separately as it's not a scalar

    # Try to load from cache
    cached_metrics = load_metrics_cache(protein, clean_flank, corrupt_flank, cache_dir)

    if (
        not force_recalc
        and cached_metrics is not None
        and set(cached_metrics.keys()) >= required_metrics
    ):
        print(f"Using all cached metrics: {', '.join(cached_metrics.keys())}")
        return cached_metrics

    # Determine what to calculate
    if cached_metrics is not None and not force_recalc:
        missing_metrics = required_metrics - set(cached_metrics.keys())
        print(f"Cache missing metrics: {', '.join(missing_metrics)}")
        print("  Will calculate missing metrics and merge with cached ones")
        head_metrics = cached_metrics.copy()
    else:
        if force_recalc:
            print("Force recalculation enabled")
        else:
            print("No cache found")
        print(f"  Calculating all metrics: {', '.join(required_metrics)}")
        head_metrics = {}

    to_calculate = (
        required_metrics - set(head_metrics.keys()) if not force_recalc else required_metrics
    )

    # Initialize tensors
    for metric_name in to_calculate:
        head_metrics[metric_name] = torch.zeros(num_layers, num_heads)

    # Initialize coordinate storage (always compute if calculating any cheap metrics)
    if "diff_max_coord" not in head_metrics:
        head_metrics["diff_max_coord"] = {}

    # Separate cheap from expensive metrics
    cheap_metrics = to_calculate & {"diff_l1", "diff_max", "diff_l2"}
    expensive_metrics = to_calculate & {"effect"}
    indirect_metrics = to_calculate & {"indirect_effect"}

    # Calculate cheap metrics
    if cheap_metrics:
        print(f"Calculating cheap metrics from attention: {', '.join(cheap_metrics)}")
        for layer_idx in range(num_layers):
            for head_idx in range(num_heads):
                clean_head_LL = clean_attn_LBHLL[layer_idx][0, head_idx]
                corrupt_head_LL = corrupt_attn_LBHLL[layer_idx][0, head_idx]
                diff_metrics = compute_diff_metrics_torch(clean_head_LL, corrupt_head_LL)

                for metric_name in cheap_metrics:
                    head_metrics[metric_name][layer_idx, head_idx] = diff_metrics[metric_name]

                # Store max diff coordinates
                head_metrics["diff_max_coord"][(layer_idx, head_idx)] = diff_metrics["diff_max_coord"]

            if (layer_idx + 1) % 10 == 0:
                print(f"  Processed {layer_idx + 1}/{num_layers} layers")

    # Compute baseline metrics for normalization (direct + indirect effects)
    if expensive_metrics or indirect_metrics:
        clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, segment)
        corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment)

    # Calculate direct effect metrics
    if expensive_metrics:
        print(f"Calculating direct effect via patching: {', '.join(expensive_metrics)}")
        print(f"  {num_layers * num_heads} contact head passes...")

        for layer_idx in range(num_layers):
            for head_idx in range(num_heads):
                patched_attn_LBHLL = []
                for l in range(num_layers):
                    if l == layer_idx:
                        patched = clean_attn_LBHLL[l].clone()
                        patched[:, head_idx, :, :] = corrupt_attn_LBHLL[l][:, head_idx, :, :]
                        patched_attn_LBHLL.append(patched)
                    else:
                        patched_attn_LBHLL.append(clean_attn_LBHLL[l])

                patched_contacts_AA = compute_contacts_from_attention(
                    patched_attn_LBHLL,
                    clean_inputs_BL["input_ids"],
                    clean_inputs_BL["attention_mask"],
                    contact_head,
                    device=device,
                )[0].detach().cpu()

                patched_metric = patching_metric(patched_contacts_AA, orig_contacts_AA, segment)
                if abs(corrupt_metric - clean_metric) > 1e-6:
                    effect = (patched_metric - clean_metric) / (corrupt_metric - clean_metric)
                else:
                    effect = 0.0
                head_metrics["effect"][layer_idx, head_idx] = effect

            if (layer_idx + 1) % 5 == 0:
                print(f"  Processed layer {layer_idx + 1}/{num_layers}")

    # Calculate indirect effect metrics
    if indirect_metrics:
        print(f"Calculating indirect effect via model traces: {', '.join(indirect_metrics)}")
        print(f"  {num_layers * num_heads} full model forward passes...")

        B = clean_attn_LBHLL[0].shape[0]
        L = clean_attn_LBHLL[0].shape[-1]

        for layer_idx in range(num_layers):
            for head_idx in range(num_heads):
                corrupt_head_attn_LL = corrupt_attn_LBHLL[layer_idx][:, head_idx, :, :]

                downstream_attn = indirect_effect_single_head(
                    nnsight_model,
                    clean_inputs_BL,
                    corrupt_head_attn_LL,
                    layer_idx,
                    head_idx,
                    num_layers,
                    num_heads,
                    head_dim,
                    B,
                    L,
                    device,
                )

                # Build full attention: clean[:layer] + patched_layer + downstream
                patched_full_attn = list(clean_attn_LBHLL[:layer_idx])
                patched_layer_attn = clean_attn_LBHLL[layer_idx].clone()
                patched_layer_attn[:, head_idx, :, :] = corrupt_attn_LBHLL[layer_idx][
                    :, head_idx, :, :
                ]
                patched_full_attn.append(patched_layer_attn)
                patched_full_attn.extend(downstream_attn)

                indirect_contacts_AA = compute_contacts_from_attention(
                    patched_full_attn,
                    clean_inputs_BL["input_ids"],
                    clean_inputs_BL["attention_mask"],
                    contact_head,
                    device=device,
                )[0].detach().cpu()

                indirect_val = patching_metric(
                    indirect_contacts_AA, orig_contacts_AA, segment
                )
                if abs(corrupt_metric - clean_metric) > 1e-6:
                    effect = (indirect_val - clean_metric) / (corrupt_metric - clean_metric)
                else:
                    effect = 0.0
                head_metrics["indirect_effect"][layer_idx, head_idx] = effect

            if (layer_idx + 1) % 5 == 0:
                print(f"  Processed layer {layer_idx + 1}/{num_layers}")

    print("Done")

    # Save updated cache
    save_metrics_cache(protein, clean_flank, corrupt_flank, head_metrics, cache_dir)

    return head_metrics


# =============================================================================
# Visualization Export
# =============================================================================
def sparse_encode_matrix(
    matrix: np.ndarray, threshold: float = 1e-6
) -> dict[int, dict[int, float]]:
    """Convert dense matrix to sparse dictionary format."""
    sparse = {}
    rows, cols = np.where(np.abs(matrix) > threshold)

    for r, c in zip(rows, cols):
        row_idx = int(r)
        col_idx = int(c)
        value = float(matrix[r, c])

        if row_idx not in sparse:
            sparse[row_idx] = {}
        sparse[row_idx][col_idx] = round(value, 4)

    return sparse


def export_attention_head(
    layer: int,
    head: int,
    metrics: dict[str, float | tuple[int, int]],
    clean_attn_BHLL: torch.Tensor,
    corrupt_attn_BHLL: torch.Tensor,
) -> dict[str, Any]:
    """Export single attention head data."""
    clean_attn_LL = clean_attn_BHLL[0, head].cpu().numpy()
    corrupt_attn_LL = corrupt_attn_BHLL[0, head].cpu().numpy()

    # Separate coordinate metrics from scalar metrics
    rounded_metrics = {}
    for k, v in metrics.items():
        if k == "diff_max_coord":
            rounded_metrics[k] = list(v)  # Convert tuple to list for JSON
        else:
            rounded_metrics[k] = round(float(v), 6)

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
    head_metrics: dict[str, torch.Tensor],
    clean_contacts_AA: torch.Tensor,
    corrupt_contacts_AA: torch.Tensor,
    orig_contacts_AA: torch.Tensor,
    segment: ContactSegment,
    sequences: dict[str, str],
    protein: str,
    config: dict[str, Any],
    output_path: str,
    skip_existing_heads: bool = True,
) -> None:
    """Export visualization data with on-demand loading support."""
    first_metric = next(iter(head_metrics.values()))
    num_layers, num_heads = first_metric.shape
    seq_length = clean_contacts_AA.shape[0]

    # Compute contact prediction metrics
    def compute_metric(pred, orig):
        pred_seg = pred[segment.ss1_start : segment.ss1_end, segment.ss2_start : segment.ss2_end]
        orig_seg = orig[segment.ss1_start : segment.ss1_end, segment.ss2_start : segment.ss2_end]
        return (torch.sum(pred_seg * orig_seg) / torch.sum(orig_seg * orig_seg)).item()

    clean_metric = compute_metric(clean_contacts_AA, orig_contacts_AA)
    corrupt_metric = compute_metric(corrupt_contacts_AA, orig_contacts_AA)

    # Create heads directory
    base_dir = os.path.dirname(output_path)
    heads_dir = os.path.join(base_dir, "heads")
    os.makedirs(heads_dir, exist_ok=True)

    print(f"Exporting {num_layers * num_heads} heads to individual files...")
    print(f"  Heads directory: {heads_dir}/")
    if skip_existing_heads:
        print("  Skipping existing head files")

    # Export each head
    head_list = []
    total_size_bytes = 0
    skipped_count = 0

    for layer in range(num_layers):
        for head in range(num_heads):
            head_filename = f"L{layer:02d}_H{head:02d}.json.gz"
            head_path = os.path.join(heads_dir, head_filename)

            if skip_existing_heads and os.path.exists(head_path):
                skipped_count += 1
                file_size = os.path.getsize(head_path)
                total_size_bytes += file_size
            else:
                # Gather all metrics for this head
                metrics = {}
                for metric_name, metric_value in head_metrics.items():
                    if metric_name == "diff_max_coord":
                        # Coordinates are stored in a dict
                        metrics[metric_name] = metric_value.get((layer, head), (0, 0))
                    else:
                        # Scalar metrics stored in tensors
                        metrics[metric_name] = metric_value[layer, head].item()

                # Export head data
                head_data = export_attention_head(
                    layer=int(layer),
                    head=int(head),
                    metrics=metrics,
                    clean_attn_BHLL=clean_attn_LBHLL[layer],
                    corrupt_attn_BHLL=corrupt_attn_LBHLL[layer],
                )

                # Save individual head file
                head_json = json.dumps(head_data, separators=(",", ":"))
                with gzip.open(head_path, "wt", encoding="utf-8") as f:
                    f.write(head_json)

                file_size = os.path.getsize(head_path)
                total_size_bytes += file_size

            # Store metrics for metadata
            head_entry = {
                "layer": int(layer),
                "head": int(head),
                "filename": head_filename,
            }
            for metric_name, metric_value in head_metrics.items():
                if metric_name == "diff_max_coord":
                    # Coordinates are stored in a dict
                    coord = metric_value.get((layer, head), (0, 0))
                    head_entry[metric_name] = list(coord)
                else:
                    # Scalar metrics stored in tensors
                    head_entry[metric_name] = round(float(metric_value[layer, head].item()), 6)

            head_list.append(head_entry)

            if (layer * num_heads + head + 1) % 50 == 0:
                exported = (layer * num_heads + head + 1) - skipped_count
                print(
                    f"  Processed {layer * num_heads + head + 1}/{num_layers * num_heads} heads ({exported} exported, {skipped_count} skipped)..."
                )

    if skipped_count > 0:
        print(f"  Skipped {skipped_count} existing head files")

    print("Encoding contact maps and writing metadata...")

    # Write metadata file
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
            "heads_dir": "heads",
            "available_metrics": list(head_metrics.keys()),
        },
        "sequences": sequences,
        "contacts": {
            "clean": sparse_encode_matrix(clean_contacts_AA.cpu().numpy()),
            "corrupt": sparse_encode_matrix(corrupt_contacts_AA.cpu().numpy()),
            "original": sparse_encode_matrix(orig_contacts_AA.cpu().numpy()),
        },
        "heads": head_list,
    }

    meta_path = output_path.replace(".json.gz", "_meta.json.gz")
    meta_json = json.dumps(metadata, separators=(",", ":"))
    with gzip.open(meta_path, "wt", encoding="utf-8") as f:
        f.write(meta_json)

    # Report sizes
    meta_size_mb = os.path.getsize(meta_path) / (1024 * 1024)
    total_size_mb = total_size_bytes / (1024 * 1024)
    avg_head_kb = (total_size_bytes / (num_layers * num_heads)) / 1024

    print("\nExport complete")
    print(f"  Metadata: {meta_size_mb:.2f} MB ({meta_path})")
    print(
        f"  Heads: {total_size_mb:.2f} MB in {num_layers * num_heads} files ({avg_head_kb:.1f} KB avg)"
    )
    print(f"  Heads directory: {heads_dir}/")
    print(f"  Sequence length: {seq_length}")
    print(f"  Clean metric: {clean_metric:.4f}")
    print(f"  Corrupt metric: {corrupt_metric:.4f}")
    print(f"  Available metrics: {', '.join(head_metrics.keys())}")

    # Report max values for each metric (skip coordinate metrics)
    for metric_name, metric_tensor in head_metrics.items():
        if metric_name == "diff_max_coord":
            # Skip coordinate metric - it's not a tensor
            continue
        max_idx = int(torch.abs(metric_tensor).flatten().argmax().item())
        max_layer = max_idx // num_heads
        max_head = max_idx % num_heads
        max_val = metric_tensor[max_layer, max_head].item()
        print(f"  Max |{metric_name}|: {max_val:.4f} (L{max_layer}H{max_head})")


# =============================================================================
# Main
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Analyze ESM2 attention heads for contact prediction flank sensitivity"
    )
    parser.add_argument(
        "--protein", type=str, default="2B61A", choices=list(PROTEINS.keys()), help="Protein ID"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="facebook/esm2_t33_650M_UR50D",
        help="ESM2 model name",
    )
    parser.add_argument(
        "--data-path",
        type=str,
        default="data/full_seq_dict.json",
        help="Path to sequence JSON",
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="reports/cache",
        help="Directory for metric cache",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="reports/viz_data.json.gz",
        help="Output path for visualization data",
    )
    parser.add_argument(
        "--force-recalc",
        action="store_true",
        help="Force recalculation of all metrics",
    )
    parser.add_argument(
        "--skip-viz-export",
        action="store_true",
        help="Skip visualization export (only compute metrics)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="Device to use (cuda/cpu)",
    )

    args = parser.parse_args()

    print(f"Using device: {args.device}")

    # Load model
    print(f"Loading model: {args.model}")
    esm_model = EsmForMaskedLM.from_pretrained(args.model, attn_implementation="eager").to(
        args.device
    )
    tokenizer = EsmTokenizer.from_pretrained(args.model)
    model = NNsight(esm_model)

    num_layers = esm_model.config.num_hidden_layers
    num_heads = esm_model.config.num_attention_heads
    print(f"Loaded {args.model}: {num_layers} layers, {num_heads} heads")
    log_memory("after model load")

    # Load sequence data
    with open(args.data_path, "r") as f:
        seq_dict = json.load(f)

    protein = args.protein
    config = PROTEINS[protein]
    sequence_S = seq_dict[protein]
    segment = ContactSegment.from_contact_pair(*config["contact_pair"])

    print(f"\nProtein: {protein}, Length: {len(sequence_S)}")
    print(
        f"Contact segment: [{segment.ss1_start}:{segment.ss1_end}] x [{segment.ss2_start}:{segment.ss2_end}]"
    )
    print(f"Flank sizes: clean={config['clean_flank']}, corrupt={config['corrupt_flank']}")

    # Compute contact maps
    print("\nComputing contact maps...")
    orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, args.device)

    clean_seq_S = mask_with_flanks(sequence_S, segment, config["clean_flank"])
    clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_seq_S, args.device)

    corrupt_seq_S = mask_with_flanks(sequence_S, segment, config["corrupt_flank"])
    corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, args.device)

    clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, segment)
    corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, segment)
    print(f"\nBaseline metrics:")
    print(f"  Clean: {clean_metric:.4f}")
    print(f"  Corrupt: {corrupt_metric:.4f}")
    print(f"  Gap: {clean_metric - corrupt_metric:.4f}")

    # Cache attention
    print("\nCaching attention for clean and corrupt sequences...")
    clean_attn_LBHLL, clean_inputs_BL = cache_attention(
        model, tokenizer, clean_seq_S, num_layers, args.device
    )
    corrupt_attn_LBHLL, corrupt_inputs_BL = cache_attention(
        model, tokenizer, corrupt_seq_S, num_layers, args.device
    )
    print(f"  Clean attention: {len(clean_attn_LBHLL)} layers, shape {clean_attn_LBHLL[0].shape}")
    print(
        f"  Corrupt attention: {len(corrupt_attn_LBHLL)} layers, shape {corrupt_attn_LBHLL[0].shape}"
    )

    # Compute head metrics
    head_dim = esm_model.config.hidden_size // num_heads
    print("\nComputing head metrics...")
    head_metrics = compute_head_metrics(
        clean_attn_LBHLL=clean_attn_LBHLL,
        corrupt_attn_LBHLL=corrupt_attn_LBHLL,
        clean_inputs_BL=clean_inputs_BL,
        clean_contacts_AA=clean_contacts_AA,
        corrupt_contacts_AA=corrupt_contacts_AA,
        orig_contacts_AA=orig_contacts_AA,
        segment=segment,
        contact_head=esm_model.esm.contact_head,
        device=args.device,
        nnsight_model=model,
        head_dim=head_dim,
        force_recalc=args.force_recalc,
        cache_dir=args.cache_dir,
        protein=protein,
        clean_flank=config["clean_flank"],
        corrupt_flank=config["corrupt_flank"],
    )

    # Export visualization data
    if not args.skip_viz_export:
        print("\nExporting visualization data...")
        export_visualization_data(
            clean_attn_LBHLL=clean_attn_LBHLL,
            corrupt_attn_LBHLL=corrupt_attn_LBHLL,
            head_metrics=head_metrics,
            clean_contacts_AA=clean_contacts_AA,
            corrupt_contacts_AA=corrupt_contacts_AA,
            orig_contacts_AA=orig_contacts_AA,
            segment=segment,
            sequences={"full": sequence_S, "clean": clean_seq_S, "corrupt": corrupt_seq_S},
            protein=protein,
            config=config,
            output_path=args.output,
            skip_existing_heads=True,
        )

    print("\nAnalysis complete")


if __name__ == "__main__":
    main()
