#!/usr/bin/env python3
# %% [markdown]
# # ESM2 3B Loader
#
# Minimal notebook-style loader for `facebook/esm2_t36_3B_UR50D` with NNsight.
# The cache is forced into `/project/pi_annagreen_umass_edu/jatin/plm_circuits/models/`
# so it does not spill into the default home-directory cache.

# %% ── Cache configuration ──────────────────────────────────────────────────

from __future__ import annotations

import os
from pathlib import Path

MODEL_NAME = "facebook/esm2_t36_3B_UR50D"
CACHE_ROOT = Path("/project/pi_annagreen_umass_edu/jatin/plm_circuits/models")
HF_CACHE_DIR = CACHE_ROOT / "huggingface"
HF_HUB_CACHE_DIR = HF_CACHE_DIR / "hub"
TORCH_CACHE_DIR = CACHE_ROOT / "torch"

for cache_dir in (
    CACHE_ROOT,
    HF_CACHE_DIR,
    HF_HUB_CACHE_DIR,
    TORCH_CACHE_DIR,
):
    cache_dir.mkdir(parents=True, exist_ok=True)

# Set every relevant cache env var before loading to avoid writes under /home.
os.environ["HF_HOME"] = str(HF_CACHE_DIR)
os.environ["HF_HUB_CACHE"] = str(HF_HUB_CACHE_DIR)
os.environ["HUGGINGFACE_HUB_CACHE"] = str(HF_HUB_CACHE_DIR)
os.environ["TORCH_HOME"] = str(TORCH_CACHE_DIR)

print(f"Model: {MODEL_NAME}")
print(f"Cache root: {CACHE_ROOT}")
print(f"HF_HOME={os.environ['HF_HOME']}")
print(f"TORCH_HOME={os.environ['TORCH_HOME']}")


# %% ── Imports ──────────────────────────────────────────────────────────────

import torch
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer


# %% ── Load model + tokenizer ───────────────────────────────────────────────

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = EsmTokenizer.from_pretrained(
    MODEL_NAME,
    cache_dir=str(HF_CACHE_DIR),
)

esm_model = EsmForMaskedLM.from_pretrained(
    MODEL_NAME,
    cache_dir=str(HF_CACHE_DIR),
    attn_implementation="eager",
).to(device).eval()

model = NNsight(esm_model)

print(f"Device: {device}")
print(f"NNsight model ready: {type(model).__name__}")
