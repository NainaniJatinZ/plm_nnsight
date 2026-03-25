"""
Debug: verify we're getting the correct hidden states for the SAE.
- Compare hidden_states[24] with nnsight hook on layer 23 output
- Compare model() vs model.esm() hidden states
- Check what the SAE's LN does to the hidden states
- Print the sequence we're using for manual comparison with website
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import torch
from nnsight import NNsight
from transformers import AutoTokenizer, EsmForMaskedLM

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from helpers.utils import load_sae_prot

WEIGHTS_DIR = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
MODEL_NAME = "facebook/esm2_t33_650M_UR50D"
DATA_PATH = PROJECT_ROOT / "data" / "full_seq_dict.json"
PROTEIN = "2B61A"

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load sequence
with open(DATA_PATH) as f:
    seq = json.load(f)[PROTEIN]
print(f"Protein: {PROTEIN}")
print(f"Sequence length: {len(seq)}")
print(f"First 20 AA: {seq[:20]}")
print(f"Last 20 AA: {seq[-20:]}")

import os
os.environ["TORCH_HOME"] = WEIGHTS_DIR
os.environ["HF_HOME"] = WEIGHTS_DIR

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR)
esm_model = EsmForMaskedLM.from_pretrained(MODEL_NAME, cache_dir=WEIGHTS_DIR).to(device)
esm_model.eval()

inputs = tokenizer(seq, return_tensors="pt").to(device)

# ── Test 1: model.esm() hidden states ──
print("\n" + "="*80)
print("TEST 1: model.esm() vs model() hidden states")
print("="*80)

with torch.no_grad():
    out_esm = esm_model.esm(**inputs, output_hidden_states=True)
    out_full = esm_model(**inputs, output_hidden_states=True)

h_esm_24 = out_esm.hidden_states[24]
h_full_24 = out_full.hidden_states[24]
print(f"model.esm() hidden_states[24] shape: {h_esm_24.shape}")
print(f"model() hidden_states[24] shape: {h_full_24.shape}")
print(f"Are they identical? {torch.allclose(h_esm_24, h_full_24)}")
print(f"Max diff: {(h_esm_24 - h_full_24).abs().max().item():.2e}")

# ── Test 2: nnsight hook on layer output ──
print("\n" + "="*80)
print("TEST 2: nnsight hook vs hidden_states")
print("="*80)

model = NNsight(esm_model)

# Hook the output of encoder layer 23 (which feeds layer 24)
# In ESM2, each encoder layer output[0] is the hidden state
with model.trace(**inputs) as tracer:
    # EsmLayer has .output remapped to .nns_output by nnsight
    layer23_out = model.esm.encoder.layer[23].nns_output[0].save()
    layer24_out = model.esm.encoder.layer[24].nns_output[0].save()

print(f"nnsight layer[23].nns_output[0] shape: {layer23_out.shape}")
print(f"nnsight layer[24].nns_output[0] shape: {layer24_out.shape}")

# Compare nnsight layer outputs with hidden_states
diff_23_vs_hs24 = (layer23_out - h_esm_24).abs().max().item()
diff_24_vs_hs24 = (layer24_out - h_esm_24).abs().max().item()
diff_23_vs_hs25 = (layer23_out - out_esm.hidden_states[25]).abs().max().item()
diff_24_vs_hs25 = (layer24_out - out_esm.hidden_states[25]).abs().max().item()

print(f"\nnnsight layer[23].output vs hidden_states[24]: max diff = {diff_23_vs_hs24:.2e}")
print(f"nnsight layer[24].output vs hidden_states[24]: max diff = {diff_24_vs_hs24:.2e}")
print(f"nnsight layer[23].output vs hidden_states[25]: max diff = {diff_23_vs_hs25:.2e}")
print(f"nnsight layer[24].output vs hidden_states[25]: max diff = {diff_24_vs_hs25:.2e}")

# ── Test 3: What does the InterProt esm_wrapper do? ──
print("\n" + "="*80)
print("TEST 3: Mapping InterProt layer convention")
print("="*80)
print("""
InterProt esm_wrapper.get_layer_activations(seq, layer_idx=24):
  self.layers[:24]  →  runs layers 0..23  →  output = input to layer 24

HuggingFace hidden_states indexing:
  hidden_states[0]  = embedding (pre any transformer layer)
  hidden_states[i]  = output of encoder.layer[i-1]
  hidden_states[24] = output of encoder.layer[23] = input to encoder.layer[24]

So hidden_states[24] should match InterProt's layer_idx=24.
""")

# ── Test 4: SAE with nnsight-hooked hidden states ──
print("="*80)
print("TEST 4: SAE activations using nnsight-hooked hidden states")
print("="*80)

sae = load_sae_prot(ESM_DIM=1280, SAE_DIM=4096, LAYER=24, device=device)
sae.eval()

# Try the nnsight layer[23] output (= hidden_states[24] = input to layer 24)
acts_from_hs24 = sae.get_acts(h_esm_24)
acts_from_nnsight = sae.get_acts(layer23_out.to(device))

print(f"SAE acts from hidden_states[24] vs nnsight layer[23].output identical? {torch.allclose(acts_from_hs24, acts_from_nnsight)}")

# ── Test 5: Inspect what LN + encode does ──
print("\n" + "="*80)
print("TEST 5: Hidden state statistics (are they reasonable?)")
print("="*80)

for idx in [23, 24, 25]:
    h = out_esm.hidden_states[idx]
    print(f"hidden_states[{idx}]: mean={h.mean().item():.4f}, std={h.std().item():.4f}, min={h.min().item():.4f}, max={h.max().item():.4f}")

# ── Test 6: Count total unique activating features properly ──
print("\n" + "="*80)
print("TEST 6: Activating feature counts (all positions including CLS/EOS)")
print("="*80)

acts_2d = acts_from_hs24[0]  # (L, 4096)
n_unique = (acts_2d > 0).any(dim=0).sum().item()
print(f"Unique activating features (top-k=128, all tokens): {n_unique}")

# Per-token stats
per_pos = (acts_2d > 0).sum(dim=1)
print(f"Active features per position: min={per_pos.min().item()}, max={per_pos.max().item()}, mean={per_pos.float().mean().item():.1f}")

# What if the website counts differently? Maybe they count features where max > some threshold?
pre_acts, mu, std = sae.encode(h_esm_24)
pre_acts_2d = pre_acts[0]
relu_pre = torch.relu(pre_acts_2d)

for thresh in [0.0, 0.1, 0.5, 1.0, 2.0]:
    n = (relu_pre.max(dim=0).values > thresh).sum().item()
    print(f"  Features with max ReLU activation > {thresh}: {n}")

# ── Test 7: His-tag stripping ──
print("\n" + "="*80)
print("TEST 7: Sequence starts with His-tag — try stripping it")
print("="*80)

# The sequence starts with GSSHHHHHHSSGLVPRGSHM — His-tag + thrombin site
# Try finding where the real protein starts
# Common His-tag pattern: GSSHHHHHH followed by thrombin site LVPRGS
# After that, the real protein begins
his_tag_end = seq.find("LVPRGS")
if his_tag_end >= 0:
    clean_start = his_tag_end + len("LVPRGS") + 2  # skip "HM" after LVPRGS too
    # Actually let's be more careful — print around the tag
    print(f"Full seq first 30 chars: {seq[:30]}")
    print(f"LVPRGS found at position {his_tag_end}")

    # Try multiple possible clean starts
    for tag_end_pos in [20, his_tag_end + 6, his_tag_end + 8]:
        clean_seq = seq[tag_end_pos:]
        print(f"\nStripping first {tag_end_pos} chars (clean seq starts: {clean_seq[:15]}...):")
        clean_inputs = tokenizer(clean_seq, return_tensors="pt").to(device)
        with torch.no_grad():
            clean_out = esm_model.esm(**clean_inputs, output_hidden_states=True)
        clean_h = clean_out.hidden_states[24]
        clean_acts = sae.get_acts(clean_h)[0]
        n_activating = (clean_acts > 0).any(dim=0).sum().item()
        max_per = clean_acts.max(dim=0).values
        top5_idx = max_per.argsort(descending=True)[:5]
        top5 = [(idx.item(), max_per[idx].item()) for idx in top5_idx]
        print(f"  Seq length: {len(clean_seq)}, Activating features: {n_activating}")
        print(f"  Top 5: {top5}")
else:
    print("No His-tag pattern found")

print("\n" + "="*80)
print("TARGET: 846 activating features, top 3 = [844, 513, 2071]")
print("="*80)
