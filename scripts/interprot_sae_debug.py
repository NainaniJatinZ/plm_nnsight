"""
Diagnostic: compare SAE activations across different layer indices and token handling
to find what matches the InterProt website (846 activating features, top: 844, 513, 2071).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
from transformers import AutoTokenizer, EsmForMaskedLM

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from helpers.utils import load_sae_prot

WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
DATA_PATH = PROJECT_ROOT / "data" / "full_seq_dict.json"
PROTEIN = "2B61A"

device = "cuda" if torch.cuda.is_available() else "cpu"

# 1. Load sequence
with open(DATA_PATH) as f:
    seq = json.load(f)[PROTEIN]
print(f"Protein: {PROTEIN}  |  Sequence length: {len(seq)}")

# 2. Get ALL hidden states from ESM2
import os
os.environ["TORCH_HOME"] = WEIGHTS_DIR
os.environ["HF_HOME"] = WEIGHTS_DIR

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR)
model = EsmForMaskedLM.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR).to(device)
model.eval()

inputs = tokenizer(seq, return_tensors="pt").to(device)
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
print(f"Tokens: {len(tokens)} (including CLS/EOS)")
print(f"First 5 tokens: {tokens[:5]}")
print(f"Last 5 tokens: {tokens[-5:]}")

with torch.no_grad():
    out = model.esm(**inputs, output_hidden_states=True)

print(f"Number of hidden states: {len(out.hidden_states)}")
print(f"hidden_states[0] shape: {out.hidden_states[0].shape}  (embedding output)")

# 3. Load SAE
sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=24, device=device)
sae.eval()

# 4. Test multiple layer indices
print("\n" + "="*80)
print("HYPOTHESIS 1: Layer index off-by-one")
print("="*80)

for layer_idx in [23, 24, 25]:
    h = out.hidden_states[layer_idx]  # (1, L, 1280)
    acts = sae.get_acts(h)  # (1, L, 4096) with top-k=128
    acts_2d = acts[0]  # (L, 4096)

    # Count unique activating features
    n_activating = (acts_2d > 0).any(dim=0).sum().item()

    # Top 5 by max activation
    max_per_latent = acts_2d.max(dim=0).values
    top5_idx = max_per_latent.argsort(descending=True)[:5]
    top5 = [(idx.item(), max_per_latent[idx].item()) for idx in top5_idx]

    print(f"\nhidden_states[{layer_idx}]:")
    print(f"  Unique activating features: {n_activating}")
    print(f"  Top 5 by max act: {top5}")

# 5. Test with CLS/EOS excluded
print("\n" + "="*80)
print("HYPOTHESIS 2: CLS/EOS token exclusion")
print("="*80)

for layer_idx in [23, 24, 25]:
    h = out.hidden_states[layer_idx]
    h_no_special = h[:, 1:-1, :]  # strip CLS and EOS
    acts = sae.get_acts(h_no_special)
    acts_2d = acts[0]

    n_activating = (acts_2d > 0).any(dim=0).sum().item()
    max_per_latent = acts_2d.max(dim=0).values
    top5_idx = max_per_latent.argsort(descending=True)[:5]
    top5 = [(idx.item(), max_per_latent[idx].item()) for idx in top5_idx]

    print(f"\nhidden_states[{layer_idx}] (no CLS/EOS):")
    print(f"  Unique activating features: {n_activating}")
    print(f"  Top 5 by max act: {top5}")

# 6. Test using encode() instead of get_acts() — pre-activations with ReLU, no top-k
print("\n" + "="*80)
print("HYPOTHESIS 3: Using encode() (pre-activations) instead of get_acts() (top-k)")
print("="*80)

for layer_idx in [23, 24, 25]:
    h = out.hidden_states[layer_idx]
    pre_acts, mu, std = sae.encode(h)  # (1, L, 4096) — raw pre-activations
    pre_acts_2d = pre_acts[0]

    # Apply ReLU but NOT top-k
    relu_acts = torch.relu(pre_acts_2d)
    n_activating_relu = (relu_acts > 0).any(dim=0).sum().item()
    max_per_latent = relu_acts.max(dim=0).values
    top5_idx = max_per_latent.argsort(descending=True)[:5]
    top5 = [(idx.item(), max_per_latent[idx].item()) for idx in top5_idx]

    print(f"\nhidden_states[{layer_idx}] encode() + ReLU (no top-k):")
    print(f"  Unique activating features (ReLU > 0): {n_activating_relu}")
    print(f"  Top 5 by max act: {top5}")

# Also try encode without CLS/EOS
for layer_idx in [23, 24, 25]:
    h = out.hidden_states[layer_idx][:, 1:-1, :]
    pre_acts, mu, std = sae.encode(h)
    pre_acts_2d = pre_acts[0]
    relu_acts = torch.relu(pre_acts_2d)
    n_activating_relu = (relu_acts > 0).any(dim=0).sum().item()
    max_per_latent = relu_acts.max(dim=0).values
    top5_idx = max_per_latent.argsort(descending=True)[:5]
    top5 = [(idx.item(), max_per_latent[idx].item()) for idx in top5_idx]

    print(f"\nhidden_states[{layer_idx}] encode() + ReLU, no CLS/EOS:")
    print(f"  Unique activating features (ReLU > 0): {n_activating_relu}")
    print(f"  Top 5 by max act: {top5}")

print("\n" + "="*80)
print("TARGET: 846 activating features, top 3 = [844, 513, 2071]")
print("="*80)
