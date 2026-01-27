"""
Simon et al. https://github.com/ElanaPearl/InterPLM
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import torch as t
import torch.nn as nn
import torch.nn.init as init

import warnings
from pathlib import Path
from typing import List, Optional, Union

import numpy as np
import pandas as pd
import torch
from huggingface_hub import hf_hub_download
from torch import Tensor
from tqdm import tqdm

warnings.filterwarnings("ignore", message="TypedStorage is deprecated")

def get_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

class Dictionary(ABC):
    """
    A dictionary consists of a collection of vectors, an encoder, and a decoder.
    """

    dict_size: int  # number of features in the dictionary
    activation_dim: int  # dimension of the activation vectors

    @abstractmethod
    def encode(self, x):
        """
        Encode a vector x in the activation space.
        """
        pass

    @abstractmethod
    def decode(self, f):
        """
        Decode a dictionary vector f (i.e. a linear combination of dictionary elements)
        """
        pass


class AutoEncoder(Dictionary, nn.Module):
    """
    A one-layer autoencoder.
    """

    def __init__(self, activation_dim, dict_size):
        super().__init__()
        self.activation_dim = activation_dim
        self.dict_size = dict_size
        self.bias = nn.Parameter(t.zeros(activation_dim))
        self.encoder = nn.Linear(activation_dim, dict_size, bias=True)

        # rows of decoder weight matrix are unit vectors
        self.decoder = nn.Linear(dict_size, activation_dim, bias=False)
        dec_weight = t.randn_like(self.decoder.weight)
        dec_weight = dec_weight / dec_weight.norm(dim=0, keepdim=True)
        self.decoder.weight = nn.Parameter(dec_weight)

    def encode(self, x):
        return nn.ReLU()(self.encoder(x - self.bias))

    def decode(self, f):
        return self.decoder(f) + self.bias

    def forward(self, x, output_features=False, ghost_mask=None):
        """
        Forward pass of an autoencoder.
        x : activations to be autoencoded
        output_features : if True, return the encoded features as well as the decoded x
        ghost_mask : if not None, run this autoencoder in "ghost mode" where features are masked
        """
        if ghost_mask is None:  # normal mode
            f = self.encode(x)
            x_hat = self.decode(f)
            if output_features:
                return x_hat, f
            else:
                return x_hat

        else:  # ghost mode
            f_pre = self.encoder(x - self.bias)
            f_ghost = t.exp(f_pre) * ghost_mask.to(f_pre)
            f = nn.ReLU()(f_pre)

            x_ghost = self.decoder(
                f_ghost
            )  # note that this only applies the decoder weight matrix, no bias
            x_hat = self.decode(f)
            if output_features:
                return x_hat, x_ghost, f
            else:
                return x_hat, x_ghost

    def from_pretrained(path, device=None):
        """
        Load a pretrained autoencoder from a file.
        """
        state_dict = t.load(path)
        dict_size, activation_dim = state_dict["encoder.weight"].shape
        autoencoder = AutoEncoder(activation_dim, dict_size)
        autoencoder.load_state_dict(state_dict)
        if device is not None:
            autoencoder.to(device)
        return autoencoder


class IdentityDict(Dictionary, nn.Module):
    """
    An identity dictionary, i.e. the identity function. This is useful for treating neurons as features.
    """

    def __init__(self, activation_dim=None):
        super().__init__()
        self.activation_dim = activation_dim
        self.dict_size = activation_dim

    def encode(self, x):
        return x

    def decode(self, f):
        return f

    def forward(self, x, output_features=False, ghost_mask=None):
        if output_features:
            return x, x
        else:
            return x


pretrained_models = ["esm2-8m", "esm2-650m"]
pretrained_layers = {
    "esm2-8m": [1, 2, 3, 4, 5, 6],
    "esm2-650m": [1, 9, 18, 24, 30, 33],
}


def load_sae(model_path: Union[str, Path], device: Optional[str] = None) -> AutoEncoder:
    """
    Load a pretrained AutoEncoder model in inference mode.

    :param model_path: Path to the saved model state dictionary
    :param device: Target device for model computation ('cpu', 'cuda', etc.).
                  If None, automatically determines the best available device
    :return: Loaded AutoEncoder model in eval mode with gradients disabled

    This function:
    1. Loads the model state from disk
    2. Reconstructs the AutoEncoder architecture based on the saved weights
    3. Moves the model to the specified device
    4. Sets the model to evaluation mode
    5. Disables gradient computation for all parameters
    """
    if device is None:
        device = get_device()

    # Load state dict to the target device
    state_dict = torch.load(
        model_path, map_location=torch.device(device), weights_only=True
    )

    # Extract architecture dimensions from the encoder weights
    dict_size, activation_dim = state_dict["encoder.weight"].shape

    # Initialize and configure the model
    autoencoder = AutoEncoder(activation_dim, dict_size)
    autoencoder.load_state_dict(state_dict)
    autoencoder.to(device)
    autoencoder.eval()

    # Disable gradient computation for inference
    for param in autoencoder.parameters():
        param.requires_grad = False

    return autoencoder


def load_sae_from_hf(plm_model: str, plm_layer: str, download_dir: str = None) -> AutoEncoder:
    """
    Load a pretrained PLM SAE from Hugging Face.

    :param plm_model: ESM2 model name [options = "esm2-8m" or "esm2-650m"]
    :param plm_layer: Layer to use for encoding [options = 1-6 if esm_model = "esm2-8m", or 1,9,18,24,30,33 if esm_model = "esm2-650m"]
    :param download_dir: Directory where the SAE model should be downloaded. Defaults to the Hugging Face cache directory.
    :return: Loaded SAE model
    """

    # Convert to lowercase and replace underscores with hyphens
    plm_model = plm_model.lower().replace("_", "-")
    plm_layer = int(plm_layer)

    if plm_model not in pretrained_models:
        raise ValueError(
            f"Invalid ESM model: {plm_model}, options: {pretrained_models}"
        )
    if plm_layer not in pretrained_layers[plm_model]:
        raise ValueError(
            f"Invalid ESM layer for {plm_model}: {plm_layer}, options: {pretrained_layers[plm_model]}"
        )

    # Download the SAE weights from Hugging Face with the specified directory
    weights_path = hf_hub_download(
        repo_id=f"Elana/InterPLM-{plm_model}",
        filename=f"layer_{plm_layer}/ae_normalized.pt",
        cache_dir=download_dir  # Specify download directory
    )

    # Load the SAE model
    sae = load_sae(weights_path)

    return sae