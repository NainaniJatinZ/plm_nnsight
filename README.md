# NNsight for Protein Language Models: ESM Tutorial

A hands-on tutorial for using [NNsight](https://nnsight.net/) to interpret protein language models (pLMs), specifically ESM2.

## What You'll Learn

- Loading ESM2 with NNsight and understanding the wrapper
- Accessing intermediate activations from any layer
- Visualizing attention patterns
- Using Sparse Autoencoders (SAEs) for interpretability
- Performing interventions on model internals

## Quick Start

### Option 1: Google Colab (Recommended)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/NainaniJatinZ/plm_nnsight/blob/main/plm_nnsight.ipynb)

The notebook auto-detects Colab and installs everything for you.

### Option 2: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/NainaniJatinZ/plm_nnsight.git
   cd plm_nnsight
   ```

2. **Create environment and install dependencies**

   Using uv (recommended):
   ```bash
   uv venv
   source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
   uv pip install nnsight transformers torch matplotlib seaborn huggingface_hub safetensors
   ```

   Or using pip:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install nnsight transformers torch matplotlib seaborn huggingface_hub safetensors
   ```

3. **Run the notebook**
   ```bash
   jupyter notebook plm_nnsight.ipynb
   ```

## Requirements

- Python 3.9+
- CUDA-capable GPU recommended (CPU works but is slow)
- ~4GB GPU memory for ESM2-650M

## Resources

- [NNsight Documentation](https://nnsight.net/)
- [ESM2 on HuggingFace](https://huggingface.co/facebook/esm2_t33_650M_UR50D)
- [pLM Circuits Paper](https://github.com/NainaniJatinZ/plm_circuits)
- [InterProt SAEs](https://huggingface.co/liambai/InterProt-ESM2-SAEs)
- [Interplm SAES](https://interplm.ai/) - we plan to add simple helpers to choose between SAE sources soon



## Citation

If you find this tutorial helpful, consider starring the repo and citing the relevant papers:

```bibtex
@article{lin2023evolutionary,
  title={Evolutionary-scale prediction of atomic-level protein structure with a language model},
  author={Lin, Zeming and others},
  journal={Science},
  year={2023}
}
```

## License

MIT
