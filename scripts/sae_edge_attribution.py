"""
SAE Edge Attribution: upstream SAE latents -> target head Q/K, and target head output -> downstream SAE latents.

For a target attention head (e.g., L10H9), this script computes:
  1. Upstream: which (position, SAE-latent) pairs at a given upstream layer drive the head's Q/K inputs
  2. Downstream: which (position, SAE-latent) pairs at a given downstream layer are written to by the head's output

Two backward targets are supported:
  - head_local: y = sum(cell_weights * attn[target_head]) — focused on what drives the head's attention
  - contact: full contact prediction metric — end-to-end attribution

Usage:
    uv run python scripts/sae_edge_attribution.py --protein 2B61A --target-layer 10 --target-head 9
    uv run python scripts/sae_edge_attribution.py --protein 2B61A --target-layer 10 --target-head 9 --metric head_local
    uv run python scripts/sae_edge_attribution.py --protein 2B61A --target-layer 10 --target-head 9 --exact-ln
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from helpers.utils import load_sae_prot

WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"

# =============================================================================
# Utilities (copied from contact_pattern_v2.py — cannot import from # %% scripts)
# =============================================================================

def log_memory(label: str = "") -> None:
    if torch.cuda.is_available():
        alloc = torch.cuda.memory_allocated() / 1e9
        resv = torch.cuda.memory_reserved() / 1e9
        print(f"[Memory {label}] alloc={alloc:.2f}GB  resv={resv:.2f}GB")


def clear_memory() -> None:
    gc.collect()
    torch.cuda.empty_cache()


@dataclass
class ContactSegment:
    ss1_start: int; ss1_end: int
    ss2_start: int; ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int = 5):
        return cls(pos1 - radius, pos1 + radius + 1, pos2 - radius, pos2 + radius + 1)


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


def compute_contact_map(esm_model, tokenizer, sequence_S, device):
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        return esm_model.predict_contacts(inputs_BL["input_ids"], inputs_BL["attention_mask"])[0].cpu()


def compute_contacts_from_attention(attn_list_LBHLL, tokens_BL, attention_mask_BL, contact_head, device="cuda"):
    attn_stack = [a.to(device) for a in attn_list_LBHLL]
    tokens_BL = tokens_BL.to(device)
    attention_mask_BL = attention_mask_BL.to(device)
    attns_BLHLL = torch.stack(attn_stack, dim=1)
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, :, None]
    attns_BLHLL = attns_BLHLL * attention_mask_BL[:, None, None, None, :]
    return contact_head(tokens_BL, attns_BLHLL)


def patching_metric(pred_AA, orig_AA, seg):
    pred = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = (orig * orig).sum()
    return ((pred * orig).sum() / denom).item() if denom > 1e-12 else 0.0


def differentiable_contact_metric(attn_proxies, tokens_BL, attention_mask_BL, eos_idx, regression_weight, regression_bias, orig_seg, segment):
    """Differentiable contact metric from attention weight tensors (supports autograd)."""
    attns = torch.stack(attn_proxies, dim=1)
    attns = attns * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(3)
    attns = attns * attention_mask_BL.unsqueeze(1).unsqueeze(2).unsqueeze(4)
    eos_mask = tokens_BL.ne(eos_idx).float()
    eos_mask_2d = eos_mask.unsqueeze(1) * eos_mask.unsqueeze(2)
    attns = attns * eos_mask_2d[:, None, None, :, :]
    attns = attns[..., :-1, :-1]
    attns = attns[..., 1:, 1:]
    batch_size, layers, heads, seqlen, _ = attns.shape
    attns = attns.reshape(batch_size, layers * heads, seqlen, seqlen)
    attns = attns + attns.transpose(-1, -2)
    a1 = attns.sum(-1, keepdim=True)
    a2 = attns.sum(-2, keepdim=True)
    a12 = attns.sum(dim=(-1, -2), keepdim=True)
    avg = a1 * a2 / a12
    attns = attns - avg
    attns = attns.permute(0, 2, 3, 1)
    contacts = torch.sigmoid(torch.nn.functional.linear(attns, regression_weight, regression_bias))
    contacts = contacts.squeeze(3)
    pred_seg = contacts[0, segment.ss1_start:segment.ss1_end, segment.ss2_start:segment.ss2_end]
    metric = (pred_seg * orig_seg).sum() / (orig_seg * orig_seg).sum()
    return metric


def make_classify_pos(seg, flank):
    ss1 = set(range(seg.ss1_start, seg.ss1_end))
    ss2 = set(range(seg.ss2_start, seg.ss2_end))
    flk_l = set(range(max(0, seg.ss1_start - flank), seg.ss1_start))
    flk_r = set(range(seg.ss2_end, seg.ss2_end + flank))
    def _classify(pos):
        if pos in ss1: return "ss1"
        if pos in ss2: return "ss2"
        if pos in flk_l: return "flkL"
        if pos in flk_r: return "flkR"
        return "other"
    return _classify


# =============================================================================
# Hook helpers
# =============================================================================

def register_hooks_for_backward(esm_model, target_layer, num_layers, mode="head_local"):
    """Register forward hooks for gradient-based attribution.

    For head_local mode: hooks Q, K, attention.self, and LayerNorm at target_layer only.
    For contact mode: additionally hooks attention.self at ALL layers for the differentiable metric.
    Returns (save_dict, hooks_list).
    """
    saved = {}
    hooks = []

    # Q at target layer
    def q_hook(module, input, output, l=target_layer):
        output.retain_grad()
        saved['q'] = output
    hooks.append(esm_model.esm.encoder.layer[target_layer].attention.self.query.register_forward_hook(q_hook))

    # K at target layer
    def k_hook(module, input, output, l=target_layer):
        output.retain_grad()
        saved['k'] = output
    hooks.append(esm_model.esm.encoder.layer[target_layer].attention.self.key.register_forward_hook(k_hook))

    # Self-attention at target layer (context + attn_probs)
    def self_hook(module, input, output, l=target_layer):
        context, attn_weights = output
        context.retain_grad()
        attn_weights.retain_grad()
        saved['context'] = context
        saved['attn'] = attn_weights
    hooks.append(esm_model.esm.encoder.layer[target_layer].attention.self.register_forward_hook(self_hook))

    # LayerNorm input at target layer
    def ln_hook(module, input, output, l=target_layer):
        saved['ln_input'] = input[0]
    hooks.append(esm_model.esm.encoder.layer[target_layer].attention.LayerNorm.register_forward_hook(ln_hook))

    # For contact mode: hook attention.self at all layers (except target, which is already hooked)
    if mode == "contact":
        for layer_idx in range(num_layers):
            if layer_idx == target_layer:
                # Target layer's attn is already captured by self_hook above as saved['attn']
                # Just alias it for the contact metric
                continue
            def attn_hook(module, input, output, l=layer_idx):
                _, attn_weights = output
                attn_weights.retain_grad()
                saved[f'attn_{l}'] = attn_weights
            hooks.append(esm_model.esm.encoder.layer[layer_idx].attention.self.register_forward_hook(attn_hook))

    return saved, hooks


def register_hooks_capture_only(esm_model, target_layer, num_layers):
    """Register forward hooks to capture activations (no gradients). For clean pass."""
    saved = {}
    hooks = []

    def self_hook(module, input, output, l=target_layer):
        saved['context'] = output[0]
        saved['attn'] = output[1]
    hooks.append(esm_model.esm.encoder.layer[target_layer].attention.self.register_forward_hook(self_hook))

    return saved, hooks


# =============================================================================
# LN Jacobian
# =============================================================================

def apply_ln_correction(grad_resid, ln_input, exact=False, eps=1e-5):
    """Apply LayerNorm Jacobian correction to gradients.

    Args:
        grad_resid: (B, L, D) gradient in post-LN space
        ln_input: (B, L, D) input to LayerNorm (pre-normalization)
        exact: if True, apply full Jacobian; if False, use diagonal 1/std approximation
        eps: LayerNorm epsilon
    Returns:
        (B, L, D) gradient corrected for LayerNorm
    """
    mu = ln_input.mean(dim=-1, keepdim=True)
    centered = ln_input - mu
    std = centered.std(dim=-1, unbiased=False, keepdim=True)

    if not exact:
        # Diagonal approximation: standard in EAP literature
        # This ignores the mean-subtraction and variance-normalization cross-terms
        return grad_resid / (std + eps)
    else:
        # Full linearized LN Jacobian: J_ij = (1/std) * (delta_ij - 1/D - x_hat_i * x_hat_j / D)
        # where x_hat = (x - mu) / std (centered and normalized)
        D = ln_input.shape[-1]
        x_hat = centered / (std + eps)  # (B, L, D)
        # grad_out . J = (1/std) * (grad - mean(grad) - x_hat * mean(x_hat * grad))
        g_mean = grad_resid.mean(dim=-1, keepdim=True)
        xg_mean = (x_hat * grad_resid).mean(dim=-1, keepdim=True)
        corrected = (grad_resid - g_mean - x_hat * xg_mean) / (std + eps)
        return corrected


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="SAE edge attribution for ESM2 attention heads")
    parser.add_argument("--protein", default="2B61A")
    parser.add_argument("--target-layer", type=int, default=10)
    parser.add_argument("--target-head", type=int, default=9)
    parser.add_argument("--upstream-sae-layer", type=int, default=8)
    parser.add_argument("--downstream-sae-layer", type=int, default=12)
    parser.add_argument("--metric", choices=["head_local", "contact", "both"], default="both")
    parser.add_argument("--exact-ln", action="store_true", help="Use full LN Jacobian instead of diagonal 1/std approximation")
    parser.add_argument("--causal-cells", type=str, default=None, help="Path to circuit JSON (from contact_pattern_v2) for explicit causal cells; falls back to diff-based weights if not provided")
    parser.add_argument("--cell-attr-cache", type=str, default=None, help="Path to cell_attr.pt cache for loading per-head causal cells")
    parser.add_argument("--top-k-validate", type=int, default=10, help="Number of top upstream/downstream latents to validate with actual patches")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    device = args.device
    target_layer = args.target_layer
    target_head = args.target_head
    up_sae_layer = args.upstream_sae_layer
    down_sae_layer = args.downstream_sae_layer
    run_head_local = args.metric in ("head_local", "both")
    run_contact = args.metric in ("contact", "both")

    print(f"=== SAE Edge Attribution ===")
    print(f"Protein: {args.protein}  Target: L{target_layer}H{target_head}")
    print(f"Upstream SAE: layer {up_sae_layer}  Downstream SAE: layer {down_sae_layer}")
    print(f"Metric: {args.metric}  Exact LN: {args.exact_ln}")

    # ── Load config ──
    proteins_cfg = json.load(open(PROJECT_ROOT / "configs" / "proteins.json"))
    common_cfg = json.load(open(PROJECT_ROOT / "configs" / "common.json"))
    pcfg = proteins_cfg[args.protein]
    contact_pair = tuple(pcfg["contact_pair"])
    clean_flank = pcfg["clean_flank"]
    corrupt_flank = pcfg["corrupt_flank"]
    segment_radius = common_cfg.get("segment_radius", 5)

    seq_dict = json.load(open(PROJECT_ROOT / "data" / "full_seq_dict.json"))
    sequence_S = seq_dict[args.protein]
    seg = ContactSegment.from_contact_pair(*contact_pair, radius=segment_radius)

    clean_seq_S = mask_with_flanks(sequence_S, seg, clean_flank)
    corrupt_seq_S = mask_with_flanks(sequence_S, seg, corrupt_flank)

    classify_pos = make_classify_pos(seg, clean_flank)

    print(f"Segment: ss1=[{seg.ss1_start}:{seg.ss1_end}] ss2=[{seg.ss2_start}:{seg.ss2_end}]")
    print(f"Flanks: clean={clean_flank} corrupt={corrupt_flank}")

    # ── Load model ──
    os.environ["TORCH_HOME"] = WEIGHTS_DIR
    os.environ["HF_HOME"] = WEIGHTS_DIR
    MODEL_NAME = common_cfg.get("model", "facebook/esm2_t33_650M_UR50D")
    esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, attn_implementation="eager", cache_dir=WEIGHTS_DIR).to(device)
    tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR)
    esm_model.eval()
    nnsight_model = NNsight(esm_model)

    NUM_LAYERS = esm_model.config.num_hidden_layers
    NUM_HEADS = esm_model.config.num_attention_heads
    HEAD_DIM = esm_model.config.hidden_size // NUM_HEADS
    HIDDEN_DIM = esm_model.config.hidden_size
    LN_EPS = esm_model.config.layer_norm_eps

    print(f"Model: {MODEL_NAME} ({NUM_LAYERS}L x {NUM_HEADS}H, dim={HIDDEN_DIM})")
    log_memory("after model load")

    # ── Tokenize ──
    clean_inputs_BL = tokenizer(clean_seq_S, return_tensors="pt").to(device)
    corrupt_inputs_BL = tokenizer(corrupt_seq_S, return_tensors="pt").to(device)
    B = 1
    L = clean_inputs_BL["input_ids"].shape[1]
    print(f"Tokenized length (with special tokens): {L}")

    # ── Baselines ──
    print("\nComputing baselines...")
    orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)

    # Cache attention for clean and corrupt (needed for cell_weights and contact metric)
    clean_attn_LBHLL, _ = cache_attention_all_layers(nnsight_model, tokenizer, clean_seq_S, device, NUM_LAYERS)
    corrupt_attn_LBHLL, _ = cache_attention_all_layers(nnsight_model, tokenizer, corrupt_seq_S, device, NUM_LAYERS)

    clean_contacts_AA = compute_contacts_from_attention(clean_attn_LBHLL, clean_inputs_BL['input_ids'], clean_inputs_BL['attention_mask'], esm_model.esm.contact_head, device=device)[0].detach().cpu()
    corrupt_contacts_AA = compute_contacts_from_attention(corrupt_attn_LBHLL, corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'], esm_model.esm.contact_head, device=device)[0].detach().cpu()

    clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, seg)
    corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)
    metric_gap = clean_metric - corrupt_metric

    print(f"Clean metric:   {clean_metric:.4f}")
    print(f"Corrupt metric: {corrupt_metric:.4f}")
    print(f"Gap:            {metric_gap:.4f}")

    if metric_gap < 0.05:
        print("WARNING: metric gap is very small, attribution may be noisy")

    # ── Cell weights for head-local target ──
    print("\nPreparing cell weights...")
    clean_attn_head_LL = clean_attn_LBHLL[target_layer][0, target_head].cpu()  # (L, L)
    corrupt_attn_head_LL = corrupt_attn_LBHLL[target_layer][0, target_head].cpu()

    # Try loading explicit causal cells from cell_attr cache
    cell_weights_LL = None
    if args.cell_attr_cache is not None:
        cache_path = Path(args.cell_attr_cache)
        if cache_path.exists():
            print(f"Loading causal cells from {cache_path}...")
            cell_cache = torch.load(cache_path, map_location="cpu", weights_only=False)
            cell_list = cell_cache.get("cell_attr_sorted", cell_cache.get("cell_attributions", []))
            # Filter for target head and build weight matrix from attributions
            cell_weights_LL = torch.zeros(L, L)
            n_cells = 0
            for entry in cell_list:
                layer, head, q_tok, k_tok, attr, abs_diff = entry
                if layer == target_layer and head == target_head:
                    cell_weights_LL[q_tok, k_tok] = abs(attr)
                    n_cells += 1
            if n_cells > 0:
                print(f"  Loaded {n_cells} causal cells for L{target_layer}H{target_head} from cache")
            else:
                print(f"  WARNING: No cells found for L{target_layer}H{target_head} in cache, falling back to diff-based weights")
                cell_weights_LL = None

    if cell_weights_LL is None:
        if args.causal_cells is not None:
            print(f"  NOTE: --causal-cells was provided but does not contain per-cell attributions.")
            print(f"  The circuit JSON only has head-level data. Falling back to diff-based weights.")
        # Fallback: diff-based weights on contact segment
        diff_LL = (clean_attn_head_LL - corrupt_attn_head_LL).abs()
        cell_weights_LL = torch.zeros_like(diff_LL)
        # Restrict to contact segment cross-region (ss1 x ss2 and ss2 x ss1)
        # Token indices: BOS offset means seq position p -> token index p+1
        s1s, s1e = seg.ss1_start + 1, seg.ss1_end + 1  # +1 for BOS
        s2s, s2e = seg.ss2_start + 1, seg.ss2_end + 1
        cell_weights_LL[s1s:s1e, s2s:s2e] = diff_LL[s1s:s1e, s2s:s2e]
        cell_weights_LL[s2s:s2e, s1s:s1e] = diff_LL[s2s:s2e, s1s:s1e]
        print(f"  Using diff-based cell weights (proxy for causal cells)")
        print(f"  Non-zero cells: {(cell_weights_LL > 0).sum().item()}")

    # ── Capture hidden states for SAE ──
    print("\nCapturing hidden states for SAE...")
    with torch.no_grad():
        clean_out = esm_model.esm(**clean_inputs_BL, output_hidden_states=True)
        h_up_clean = clean_out.hidden_states[up_sae_layer].detach().cpu()
        h_down_clean = clean_out.hidden_states[down_sae_layer].detach().cpu()

    with torch.no_grad():
        corrupt_out = esm_model.esm(**corrupt_inputs_BL, output_hidden_states=True)
        h_up_corr = corrupt_out.hidden_states[up_sae_layer].detach().cpu()
        h_down_corr = corrupt_out.hidden_states[down_sae_layer].detach().cpu()

    del clean_out, corrupt_out
    clear_memory()

    # ── Load SAEs ──
    print(f"Loading SAEs (upstream layer {up_sae_layer}, downstream layer {down_sae_layer})...")
    sae_up = load_sae_prot(ESM_DIM=HIDDEN_DIM, SAE_DIM=4096, LAYER=up_sae_layer, device="cpu")
    sae_up.eval()
    sae_down = load_sae_prot(ESM_DIM=HIDDEN_DIM, SAE_DIM=4096, LAYER=down_sae_layer, device="cpu")
    sae_down.eval()

    # ── SAE activations and LN stats ──
    print("Computing SAE activations...")
    with torch.no_grad():
        z_up_clean = sae_up.get_acts(h_up_clean)  # (B, L, 4096)
        z_up_corr = sae_up.get_acts(h_up_corr)
        _, mu_up_corr, std_up_corr = sae_up.LN(h_up_corr)  # std: (B, 1, 1) or (B, L, 1) depending on implementation

        z_down_clean = sae_down.get_acts(h_down_clean)
        z_down_corr = sae_down.get_acts(h_down_corr)
        _, mu_down_corr, std_down_corr = sae_down.LN(h_down_corr)

    # Squeeze batch dim for simplicity (B=1)
    z_up_clean = z_up_clean[0]      # (L, 4096)
    z_up_corr = z_up_corr[0]
    std_up_corr = std_up_corr[0]    # (L, 1) or (1, 1)
    z_down_clean = z_down_clean[0]
    z_down_corr = z_down_corr[0]
    std_down_corr = std_down_corr[0]

    delta_z_up = z_up_clean - z_up_corr  # (L, 4096)

    print(f"  Upstream SAE: {(z_up_clean > 0).any(dim=0).sum().item()} active latents (clean), delta_z nonzero: {(delta_z_up.abs() > 1e-8).sum().item()}")
    print(f"  Downstream SAE: {(z_down_clean > 0).any(dim=0).sum().item()} active latents (clean)")

    # ── Reconstruction check ──
    print("\nReconstruction check (upstream SAE)...")
    with torch.no_grad():
        recon_delta = delta_z_up @ sae_up.w_dec * std_up_corr  # (L, 1280)
        actual_delta = (h_up_clean - h_up_corr)[0]  # (L, 1280)
        # Per-position R^2
        ss_res = ((actual_delta - recon_delta) ** 2).sum(dim=-1)
        ss_tot = ((actual_delta - actual_delta.mean(dim=-1, keepdim=True)) ** 2).sum(dim=-1)
        r2_per_pos = 1 - ss_res / (ss_tot + 1e-12)
        # Overall R^2
        ss_res_total = ss_res.sum()
        ss_tot_total = ss_tot.sum()
        r2_overall = (1 - ss_res_total / (ss_tot_total + 1e-12)).item()
        # Cosine similarity
        cos_sim = torch.nn.functional.cosine_similarity(actual_delta, recon_delta, dim=-1)
        cos_sim_mean = cos_sim[actual_delta.norm(dim=-1) > 1e-6].mean().item()

    print(f"  Overall R^2: {r2_overall:.4f}")
    print(f"  Mean cosine sim (nonzero positions): {cos_sim_mean:.4f}")

    # ── Extract model weights for target head ──
    W_Q = esm_model.esm.encoder.layer[target_layer].attention.self.query.weight.detach().cpu()  # (D, D)
    W_K = esm_model.esm.encoder.layer[target_layer].attention.self.key.weight.detach().cpu()
    W_O = esm_model.esm.encoder.layer[target_layer].attention.output.dense.weight.detach().cpu()  # (D, D)

    # Per-head slices
    W_Q_head = W_Q.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)[target_head]  # (64, 1280)
    W_K_head = W_K.reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)[target_head]
    # W_O is (D_out, D_in) where D_in is concatenated head outputs
    # Per-head: columns for this head
    W_O_head = W_O[:, target_head * HEAD_DIM:(target_head + 1) * HEAD_DIM]  # (1280, 64)

    # Contact head params (for differentiable metric)
    contact_head_module = esm_model.esm.contact_head
    eos_idx = contact_head_module.eos_idx
    regression_weight = contact_head_module.regression.weight.detach()
    regression_bias = contact_head_module.regression.bias.detach()
    orig_seg_tensor = orig_contacts_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end].to(device)

    # ==========================================================================
    # STEP 4: Upstream Attribution — SAE latents -> head Q/K
    # ==========================================================================
    results = {}

    def compute_upstream_scores(mode_label, saved):
        """Extract grad_resid_Q, grad_resid_K and compute upstream scores."""
        print(f"  Computing upstream scores ({mode_label})...")

        # Gradients at Q and K (full hidden dim, all heads concatenated)
        grad_Q_full = saved['q'].grad.detach().cpu()  # (B, L, D)
        grad_K_full = saved['k'].grad.detach().cpu()

        # Per-head gradients
        grad_Q_head_BLD = grad_Q_full.reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, target_head, :]  # (B, L, 64)
        grad_K_head_BLD = grad_K_full.reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, target_head, :]

        # Project back to residual stream: grad_Q_h @ W_Q_h -> (B, L, 1280)
        grad_resid_Q = torch.einsum('bld, dD -> blD', grad_Q_head_BLD, W_Q_head)
        grad_resid_K = torch.einsum('bld, dD -> blD', grad_K_head_BLD, W_K_head)

        # LN correction
        ln_input = saved['ln_input'].detach().cpu()
        grad_resid_Q = apply_ln_correction(grad_resid_Q, ln_input, exact=args.exact_ln, eps=LN_EPS)
        grad_resid_K = apply_ln_correction(grad_resid_K, ln_input, exact=args.exact_ln, eps=LN_EPS)

        # Upstream scores: position-aware (latent at pos p affects Q[p] and K[p])
        # score_q[p,f] = delta_z_up[p,f] * (grad_resid_Q[0,p] . w_dec[f]) * std_up_corr[p]
        # Vectorized: proj_Q[p,f] = grad_resid_Q[0,p] @ w_dec[f]^T
        proj_Q = grad_resid_Q[0] @ sae_up.w_dec.T  # (L, 4096)
        proj_K = grad_resid_K[0] @ sae_up.w_dec.T  # (L, 4096)

        score_q = delta_z_up * proj_Q * std_up_corr  # (L, 4096)
        score_k = delta_z_up * proj_K * std_up_corr  # (L, 4096)

        return score_q, score_k

    # ── Head-local backward ──
    if run_head_local:
        print("\n--- Upstream: head-local backward ---")
        saved_hl, hooks_hl = register_hooks_for_backward(esm_model, target_layer, NUM_LAYERS, mode="head_local")
        esm_model.zero_grad()
        esm_model(**{**corrupt_inputs_BL, "output_attentions": True})

        attn_H = saved_hl['attn'][:, target_head, :, :]  # (B, L, L)
        y_head = (cell_weights_LL.to(device) * attn_H).sum()
        y_head.backward()

        score_q_hl, score_k_hl = compute_upstream_scores("head_local", saved_hl)
        results["score_q_head_local"] = score_q_hl
        results["score_k_head_local"] = score_k_hl

        for h in hooks_hl:
            h.remove()
        del saved_hl
        esm_model.zero_grad()
        clear_memory()

    # ── Contact metric backward ──
    if run_contact:
        print("\n--- Upstream: contact metric backward ---")
        saved_cm, hooks_cm = register_hooks_for_backward(esm_model, target_layer, NUM_LAYERS, mode="contact")
        esm_model.zero_grad()
        esm_model(**{**corrupt_inputs_BL, "output_attentions": True})

        # Build attention proxy list from hooks
        # Target layer's attention is stored as 'attn' (from self_hook), others as 'attn_{l}'
        attn_proxies = []
        for l in range(NUM_LAYERS):
            if l == target_layer:
                attn_proxies.append(saved_cm['attn'])
            else:
                attn_proxies.append(saved_cm[f'attn_{l}'])

        y_contact = differentiable_contact_metric(
            attn_proxies, corrupt_inputs_BL['input_ids'], corrupt_inputs_BL['attention_mask'],
            eos_idx, regression_weight, regression_bias, orig_seg_tensor, seg,
        )
        y_contact.backward()

        score_q_cm, score_k_cm = compute_upstream_scores("contact", saved_cm)
        results["score_q_contact"] = score_q_cm
        results["score_k_contact"] = score_k_cm

        for h in hooks_cm:
            h.remove()
        del saved_cm
        esm_model.zero_grad()
        clear_memory()

    # ==========================================================================
    # STEP 5: Direct Downstream Write Attribution — head output -> SAE latents
    # ==========================================================================
    print("\n--- Downstream: direct write attribution ---")

    # Get head context from clean and corrupt (need fresh forward passes to capture context)
    saved_clean_ctx, hooks_c = register_hooks_capture_only(esm_model, target_layer, NUM_LAYERS)
    with torch.no_grad():
        esm_model(**{**clean_inputs_BL, "output_attentions": True})
    context_clean = saved_clean_ctx['context'].detach().cpu()  # (B, L, 1280)
    for h in hooks_c:
        h.remove()

    saved_corr_ctx, hooks_cc = register_hooks_capture_only(esm_model, target_layer, NUM_LAYERS)
    with torch.no_grad():
        esm_model(**{**corrupt_inputs_BL, "output_attentions": True})
    context_corr = saved_corr_ctx['context'].detach().cpu()
    for h in hooks_cc:
        h.remove()

    # Per-head context difference -> project through W_O to residual stream
    diff_ctx = (context_clean - context_corr).reshape(B, L, NUM_HEADS, HEAD_DIM)[:, :, target_head, :]  # (B, L, 64)
    delta_hout = diff_ctx @ W_O_head.T  # (B, L, 1280) — head's contribution to residual stream difference

    # Downstream scores via SAE encoder directions
    # The direct residual path means delta_hout at position p arrives at the downstream layer's LN input at position p
    # score_down[p,f] = (delta_hout[0,p] / std_down_corr[p]) . w_enc[:, f]
    delta_hout_normed = delta_hout[0] / (std_down_corr + 1e-5)  # (L, 1280), approximate LN correction
    if args.exact_ln:
        # For exact: need the downstream layer's LN input
        # The delta_hout propagates through the residual stream to the downstream layer's LN
        # For the approximate version, we just use 1/std; for exact, we'd need the full Jacobian
        # which requires the actual LN input at the downstream layer (h_down_corr)
        mu_down = h_down_corr[0].mean(dim=-1, keepdim=True)
        centered_down = h_down_corr[0] - mu_down
        std_down_full = centered_down.std(dim=-1, unbiased=False, keepdim=True)
        x_hat_down = centered_down / (std_down_full + 1e-5)
        # Apply full Jacobian: J @ delta = (delta - mean(delta) - x_hat * mean(x_hat * delta)) / std
        d_mean = delta_hout[0].mean(dim=-1, keepdim=True)
        xd_mean = (x_hat_down * delta_hout[0]).mean(dim=-1, keepdim=True)
        delta_hout_normed = (delta_hout[0] - d_mean - x_hat_down * xd_mean) / (std_down_full + 1e-5)

    score_downstream = delta_hout_normed @ sae_down.w_enc  # (L, 4096)
    results["score_downstream"] = score_downstream

    # Save additional tensors
    results["delta_hout"] = delta_hout[0]  # (L, 1280)
    results["delta_z_up"] = delta_z_up
    results["z_up_clean"] = z_up_clean
    results["z_up_corr"] = z_up_corr
    results["z_down_clean"] = z_down_clean
    results["z_down_corr"] = z_down_corr

    # ==========================================================================
    # STEP 6: Causal Validation Patches (top-K spot checks)
    # ==========================================================================
    top_k_val = args.top_k_validate
    validation_results = {}

    if top_k_val > 0:
        print(f"\n--- Validation patches (top-{top_k_val}) ---")

        # Pick the primary upstream scores for validation
        if run_contact:
            val_score_q = results["score_q_contact"]
            val_score_k = results["score_k_contact"]
        else:
            val_score_q = results["score_q_head_local"]
            val_score_k = results["score_k_head_local"]

        # Top-K upstream Q-side
        q_flat = val_score_q.abs().flatten()
        q_top_idx = q_flat.argsort(descending=True)[:top_k_val]
        q_top_positions = [(idx.item() // 4096, idx.item() % 4096) for idx in q_top_idx]

        # Validate upstream: add delta_resid to corrupt hidden state via forward hooks, measure attention change
        print("  Validating upstream Q-side...")
        baseline_attn_head = corrupt_attn_LBHLL[target_layer][0, target_head].cpu()
        val_up_q = []
        for pos, latent_f in q_top_positions:
            predicted_score = val_score_q[pos, latent_f].item()
            delta_resid_vec = (delta_z_up[pos, latent_f] * sae_up.w_dec[latent_f] * std_up_corr[pos]).to(device)  # (1280,)

            # Use a pre-hook on the layer AFTER the upstream SAE layer to add perturbation
            # (modifying the hidden_states input tensor is simpler than modifying outputs)
            patched_attn_container = {}

            def add_perturbation_pre(module, args, p=pos, dv=delta_resid_vec):
                # Pre-hook: args[0] is hidden_states (B, L, D)
                hs = args[0]
                hs = hs.clone()
                hs[:, p, :] = hs[:, p, :] + dv
                return (hs,) + args[1:]

            def capture_target_attn(module, input, output):
                patched_attn_container['attn'] = output[1].detach().cpu()

            h1 = esm_model.esm.encoder.layer[up_sae_layer + 1].register_forward_pre_hook(add_perturbation_pre)
            h2 = esm_model.esm.encoder.layer[target_layer].attention.self.register_forward_hook(capture_target_attn)
            with torch.no_grad():
                esm_model(**{**corrupt_inputs_BL, "output_attentions": True})
            h1.remove()
            h2.remove()

            patched_attn_head = patched_attn_container['attn'][0, target_head]
            actual_effect = (cell_weights_LL * (patched_attn_head - baseline_attn_head)).sum().item()
            val_up_q.append({"pos": pos, "latent": latent_f, "predicted": predicted_score, "actual": actual_effect})

        validation_results["upstream_q"] = val_up_q

        # Validate downstream: compare predicted score direction with actual SAE activation difference
        print("  Validating downstream...")
        d_flat = score_downstream.abs().flatten()
        d_top_idx = d_flat.argsort(descending=True)[:top_k_val]
        d_top_positions = [(idx.item() // 4096, idx.item() % 4096) for idx in d_top_idx]

        val_down = []
        for pos, latent_f in d_top_positions:
            predicted_score = score_downstream[pos, latent_f].item()
            actual_delta = (z_down_clean[pos, latent_f] - z_down_corr[pos, latent_f]).item()
            val_down.append({"pos": pos, "latent": latent_f, "predicted": predicted_score, "actual_delta_z": actual_delta})

        validation_results["downstream"] = val_down
        results["validation"] = validation_results

    # ==========================================================================
    # STEP 7: Output and Reporting
    # ==========================================================================
    print("\n--- Saving results ---")
    report_dir = PROJECT_ROOT / "reports" / "outputs" / args.protein
    report_dir.mkdir(parents=True, exist_ok=True)

    # Save .pt file
    pt_path = report_dir / f"{args.protein}_L{target_layer}H{target_head}_sae_edge_attr.pt"
    save_dict = {
        "config": {
            "protein": args.protein, "target_layer": target_layer, "target_head": target_head,
            "upstream_sae_layer": up_sae_layer, "downstream_sae_layer": down_sae_layer,
            "metric": args.metric, "exact_ln": args.exact_ln,
            "contact_pair": list(contact_pair), "clean_flank": clean_flank, "corrupt_flank": corrupt_flank,
            "clean_metric": clean_metric, "corrupt_metric": corrupt_metric,
            "recon_r2": r2_overall, "recon_cos_sim": cos_sim_mean,
        },
    }
    for key, val in results.items():
        if isinstance(val, torch.Tensor):
            save_dict[key] = val.cpu()
        else:
            save_dict[key] = val

    torch.save(save_dict, pt_path)
    print(f"Saved tensors: {pt_path}")

    # ── Markdown report ──
    report_lines = []
    report_lines.append(f"# SAE Edge Attribution: {args.protein} L{target_layer}H{target_head}")
    report_lines.append("")
    report_lines.append(f"Upstream SAE: layer {up_sae_layer} | Downstream SAE: layer {down_sae_layer}")
    report_lines.append(f"Metric: {args.metric} | LN correction: {'exact' if args.exact_ln else 'approximate (1/std diagonal)'}")
    report_lines.append(f"Clean metric: {clean_metric:.4f} | Corrupt metric: {corrupt_metric:.4f} | Gap: {metric_gap:.4f}")
    report_lines.append(f"SAE reconstruction R^2: {r2_overall:.4f} | Cosine sim: {cos_sim_mean:.4f}")
    report_lines.append("")

    # Helper to format top entries
    def format_top_entries(score_tensor, label, top_n=30):
        lines = []
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"| Rank | Pos | SeqPos | Region | Latent | Score | AA |")
        lines.append(f"|------|-----|--------|--------|--------|-------|----|")
        flat = score_tensor.flatten()
        top_idx = flat.abs().argsort(descending=True)[:top_n]
        for rank, idx in enumerate(top_idx):
            pos = idx.item() // 4096
            latent_f = idx.item() % 4096
            score_val = score_tensor[pos, latent_f].item()
            seq_pos = pos - 1  # token to seq position (BOS offset)
            region = classify_pos(seq_pos) if 0 <= seq_pos < len(sequence_S) else "special"
            aa = sequence_S[seq_pos] if 0 <= seq_pos < len(sequence_S) else "?"
            lines.append(f"| {rank+1} | {pos} | {seq_pos} | {region} | {latent_f} | {score_val:+.6f} | {aa} |")
        lines.append("")
        return lines

    # Upstream scores
    for metric_label in (["head_local"] if run_head_local else []) + (["contact"] if run_contact else []):
        sq = results.get(f"score_q_{metric_label}")
        sk = results.get(f"score_k_{metric_label}")
        if sq is not None:
            report_lines.extend(format_top_entries(sq, f"Upstream Q-side ({metric_label})"))
            report_lines.extend(format_top_entries(sk, f"Upstream K-side ({metric_label})"))

    # Downstream scores
    report_lines.extend(format_top_entries(score_downstream, "Downstream (direct write attribution)"))

    # Active-latent only downstream
    active_mask = (z_down_clean > 0) | (z_down_corr > 0)  # (L, 4096)
    score_down_active = score_downstream.clone()
    score_down_active[~active_mask] = 0
    report_lines.extend(format_top_entries(score_down_active, "Downstream (active latents only)"))

    # Validation results
    if validation_results:
        report_lines.append("## Validation Patches")
        report_lines.append("")

        if "upstream_q" in validation_results:
            report_lines.append("### Upstream Q-side validation")
            report_lines.append("")
            report_lines.append("| Pos | Latent | Predicted | Actual | Match |")
            report_lines.append("|-----|--------|-----------|--------|-------|")
            for v in validation_results["upstream_q"]:
                match = "Y" if (v["predicted"] > 0) == (v["actual"] > 0) else "N"
                report_lines.append(f"| {v['pos']} | {v['latent']} | {v['predicted']:+.6f} | {v['actual']:+.6f} | {match} |")
            report_lines.append("")

        if "downstream" in validation_results:
            report_lines.append("### Downstream validation")
            report_lines.append("")
            report_lines.append("| Pos | Latent | Predicted | Actual delta_z | Match |")
            report_lines.append("|-----|--------|-----------|----------------|-------|")
            for v in validation_results["downstream"]:
                match = "Y" if (v["predicted"] > 0) == (v["actual_delta_z"] > 0) else "N"
                report_lines.append(f"| {v['pos']} | {v['latent']} | {v['predicted']:+.6f} | {v['actual_delta_z']:+.6f} | {match} |")
            report_lines.append("")

    # Head-local vs contact comparison
    if run_head_local and run_contact:
        report_lines.append("## Head-local vs Contact metric comparison")
        report_lines.append("")
        # Rank correlation (Spearman) for Q-side
        sq_hl = results["score_q_head_local"].flatten()
        sq_cm = results["score_q_contact"].flatten()
        # Simple rank correlation: use top-100 by contact metric
        top100 = sq_cm.abs().argsort(descending=True)[:100]
        hl_vals = sq_hl[top100]
        cm_vals = sq_cm[top100]
        # Pearson correlation as a simple proxy
        corr = torch.corrcoef(torch.stack([hl_vals, cm_vals]))[0, 1].item()
        report_lines.append(f"Pearson correlation (top-100 Q-side by contact): {corr:.4f}")
        report_lines.append("")

    md_path = report_dir / f"{args.protein}_L{target_layer}H{target_head}_sae_edge_attr.md"
    with open(md_path, "w") as f:
        f.write("\n".join(report_lines))
    print(f"Saved report: {md_path}")

    # ── CSV summary ──
    csv_path = report_dir / f"{args.protein}_L{target_layer}H{target_head}_sae_edge_attr.csv"
    with open(csv_path, "w", newline="") as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(["direction", "metric_type", "qk_side", "rank", "token_pos", "seq_pos", "region", "aa", "latent_idx", "score"])

        for metric_label in (["head_local"] if run_head_local else []) + (["contact"] if run_contact else []):
            for side in ["q", "k"]:
                s = results.get(f"score_{side}_{metric_label}")
                if s is None:
                    continue
                flat = s.flatten()
                top_idx = flat.abs().argsort(descending=True)[:50]
                for rank, idx in enumerate(top_idx):
                    pos = idx.item() // 4096
                    latent_f = idx.item() % 4096
                    seq_pos = pos - 1
                    region = classify_pos(seq_pos) if 0 <= seq_pos < len(sequence_S) else "special"
                    aa = sequence_S[seq_pos] if 0 <= seq_pos < len(sequence_S) else "?"
                    writer.writerow(["upstream", metric_label, side, rank + 1, pos, seq_pos, region, aa, latent_f, f"{s[pos, latent_f].item():.8f}"])

        flat = score_downstream.flatten()
        top_idx = flat.abs().argsort(descending=True)[:50]
        for rank, idx in enumerate(top_idx):
            pos = idx.item() // 4096
            latent_f = idx.item() % 4096
            seq_pos = pos - 1
            region = classify_pos(seq_pos) if 0 <= seq_pos < len(sequence_S) else "special"
            aa = sequence_S[seq_pos] if 0 <= seq_pos < len(sequence_S) else "?"
            writer.writerow(["downstream", "direct_write", "-", rank + 1, pos, seq_pos, region, aa, latent_f, f"{score_downstream[pos, latent_f].item():.8f}"])

    print(f"Saved CSV: {csv_path}")
    print("\nDone.")


def cache_attention_all_layers(model, tokenizer, sequence_S, device, num_layers):
    """Traced forward; returns (list of (B,H,L,L) per layer on CPU, tokenizer inputs)."""
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with model.trace() as tracer:
        with tracer.invoke(**inputs_BL, output_attentions=True):
            attn_cache = tracer.cache(
                modules=[model.esm.encoder.layer[i].attention.self for i in range(num_layers)]
            )
    attn_LBHLL = []
    for i in range(num_layers):
        key = f"model.esm.encoder.layer.{i}.attention.self"
        attn_LBHLL.append(attn_cache[key].output[1].detach().cpu())
    return attn_LBHLL, inputs_BL


if __name__ == "__main__":
    main()
