from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import random

import matplotlib.pyplot as plt
import torch
from transformers import EsmForMaskedLM, EsmTokenizer

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT_DIR = _SCRIPT_DIR.parent
_COMMON_CFG = _ROOT_DIR / "configs" / "common.json"
_PROTEINS_CFG = _ROOT_DIR / "configs" / "proteins.json"


def load_config(protein: str, config_path: str | None) -> dict:
    """Layer: common.json → PROTEINS[protein] → optional --config override."""
    cfg: dict = {}
    with open(_COMMON_CFG) as f:
        cfg.update(json.load(f))
    with open(_PROTEINS_CFG) as f:
        proteins = json.load(f)
    if protein not in proteins:
        raise KeyError(
            f"Protein '{protein}' not found in configs/proteins.json. "
            "Re-run scripts/build_proteins_config.py to rebuild."
        )
    cfg.update(proteins[protein])
    if config_path is not None:
        with open(config_path) as f:
            cfg.update(json.load(f))
    return cfg


@dataclass
class ContactSegment:
    ss1_start: int
    ss1_end: int
    ss2_start: int
    ss2_end: int

    @classmethod
    def from_contact_pair(cls, pos1: int, pos2: int, radius: int) -> "ContactSegment":
        return cls(pos1 - radius, pos1 + radius + 1, pos2 - radius, pos2 + radius + 1)


def mask_with_flanks_tokens(seq_S: str, seg: ContactSegment, flank: int) -> list[str]:
    n = len(seq_S)
    masked = ["<mask>"] * n
    masked[seg.ss1_start:seg.ss1_end] = list(seq_S[seg.ss1_start:seg.ss1_end])
    masked[seg.ss2_start:seg.ss2_end] = list(seq_S[seg.ss2_start:seg.ss2_end])
    for i in range(max(0, seg.ss1_start - flank), seg.ss1_start):
        masked[i] = seq_S[i]
    for i in range(seg.ss2_end, min(n, seg.ss2_end + flank)):
        masked[i] = seq_S[i]
    return masked


def tokens_to_sequence(tokens: Iterable[str]) -> str:
    return "".join(tokens)


def compute_contact_map(
    esm_model: EsmForMaskedLM, tokenizer: EsmTokenizer, sequence_S: str, device: str
) -> torch.Tensor:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    with torch.no_grad():
        return esm_model.predict_contacts(
            inputs_BL["input_ids"], inputs_BL["attention_mask"]
        )[0].cpu()


def patching_metric(
    pred_AA: torch.Tensor, orig_AA: torch.Tensor, seg: ContactSegment
) -> float:
    pred = pred_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    orig = orig_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    denom = (orig * orig).sum()
    return ((pred * orig).sum() / denom).item() if denom > 1e-12 else 0.0


def select_top_contacts(
    contact_map_AA: torch.Tensor, seg: ContactSegment, top_k: int
) -> list[tuple[int, int, float]]:
    seg_map = contact_map_AA[seg.ss1_start:seg.ss1_end, seg.ss2_start:seg.ss2_end]
    flat = seg_map.flatten()
    k = min(top_k, flat.numel())
    values, indices = torch.topk(flat, k=k)
    contacts: list[tuple[int, int, float]] = []
    width = seg_map.shape[1]
    for v, idx in zip(values.tolist(), indices.tolist()):
        r = idx // width
        c = idx % width
        contacts.append(
            (seg.ss1_start + r, seg.ss2_start + c, float(v))
        )
    return contacts


def parse_residue_spec(spec: str, index_base: int) -> tuple[int, str | None]:
    spec = spec.strip()
    if not spec:
        raise ValueError("Empty residue spec")
    if spec[0].isalpha():
        letter = spec[0].upper()
        number = int(spec[1:])
    else:
        letter = None
        number = int(spec)
    return number - index_base, letter


def get_aa_tokens(tokenizer: EsmTokenizer) -> list[str]:
    vocab = tokenizer.get_vocab()
    allowed = list("ACDEFGHIKLMNPQRSTVWY") + ["X", "B", "Z", "U", "O"]
    return [tok for tok in allowed if tok in vocab]


def masked_token_probs(
    esm_model: EsmForMaskedLM,
    tokenizer: EsmTokenizer,
    sequence_S: str,
    mask_index: int,
    device: str,
    aa_tokens: list[str],
) -> dict[str, float]:
    inputs_BL = tokenizer(sequence_S, return_tensors="pt").to(device)
    input_ids = inputs_BL["input_ids"]
    mask_token_id = tokenizer.mask_token_id
    token_index = mask_index + 1  # offset for CLS
    if token_index >= input_ids.shape[1]:
        raise IndexError(f"Token index {token_index} out of range for sequence length.")
    if input_ids[0, token_index].item() != mask_token_id:
        raise ValueError(
            f"Expected <mask> at token index {token_index}, "
            f"found id={input_ids[0, token_index].item()}."
        )
    with torch.no_grad():
        logits = esm_model(**inputs_BL).logits[0, token_index]
    probs = torch.softmax(logits, dim=-1).detach().cpu()
    aa_ids = tokenizer.convert_tokens_to_ids(aa_tokens)
    return {tok: probs[idx].item() for tok, idx in zip(aa_tokens, aa_ids)}


def top_k_probs(prob_map: dict[str, float], top_k: int) -> list[tuple[str, float]]:
    return sorted(prob_map.items(), key=lambda kv: kv[1], reverse=True)[:top_k]


def plot_distributions(
    residue_label: str,
    seq_label: str,
    probs: dict[str, float],
    top_k: int,
    out_path: Path,
) -> None:
    top_items = top_k_probs(probs, top_k)
    labels = [k for k, _ in top_items]
    values = [v for _, v in top_items]
    plt.figure(figsize=(6, 3))
    plt.bar(labels, values, color="#2f6f9f")
    plt.title(f"{residue_label} - {seq_label}")
    plt.ylabel("Probability")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def plot_distributions_stacked(
    residue_label: str,
    seq_probs: dict[str, dict[str, float]],
    top_k: int,
    out_path: Path,
    seq_order: list[str],
) -> None:
    fig, axes = plt.subplots(
        nrows=len(seq_order), ncols=1, figsize=(6, 2.5 * len(seq_order)),
        sharex=False, sharey=True
    )
    if len(seq_order) == 1:
        axes = [axes]
    for ax, seq_label in zip(axes, seq_order):
        probs = seq_probs[seq_label]
        top_items = top_k_probs(probs, top_k)
        labels = [k for k, _ in top_items]
        values = [v for _, v in top_items]
        ax.bar(labels, values, color="#2f6f9f")
        ax.set_title(seq_label)
        ax.set_ylabel("Prob")
    axes[-1].set_xlabel("Token")
    fig.suptitle(residue_label)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_native_prob_summary(
    residue_labels: list[str],
    results: dict[str, dict[str, dict[str, float]]],
    out_path: Path,
) -> None:
    seq_labels = ["full", "clean", "corrupt"]
    x = list(range(len(residue_labels)))
    width = 0.25
    plt.figure(figsize=(max(6, len(residue_labels) * 0.6), 3.5))
    for i, seq_label in enumerate(seq_labels):
        values = []
        for label in residue_labels:
            native = label[0]
            prob = results[label][seq_label].get(native, 0.0)
            values.append(prob)
        positions = [v + (i - 1) * width for v in x]
        plt.bar(positions, values, width=width, label=seq_label)
    plt.xticks(x, residue_labels, rotation=45, ha="right")
    plt.ylabel("Native residue probability")
    plt.title("Native residue prob by context (contact residues)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def prob_vector(prob_map: dict[str, float], aa_tokens: list[str], eps: float = 1e-9) -> torch.Tensor:
    vals = torch.tensor([prob_map.get(tok, 0.0) for tok in aa_tokens], dtype=torch.float32)
    vals = vals + eps
    return vals / vals.sum()


def js_divergence(
    p_map: dict[str, float],
    q_map: dict[str, float],
    aa_tokens: list[str],
) -> float:
    p = prob_vector(p_map, aa_tokens)
    q = prob_vector(q_map, aa_tokens)
    m = 0.5 * (p + q)
    kl_pm = torch.sum(p * torch.log(p / m))
    kl_qm = torch.sum(q * torch.log(q / m))
    return float(0.5 * (kl_pm + kl_qm))


def plot_divergence_summary(
    contact_labels: list[str],
    control_labels: list[str],
    divergences: dict[str, dict[str, float]],
    out_path: Path,
) -> None:
    labels = contact_labels + control_labels
    x = list(range(len(labels)))
    width = 0.35
    fc = [divergences[label]["full_clean"] for label in labels]
    fx = [divergences[label]["full_corrupt"] for label in labels]
    plt.figure(figsize=(max(6, len(labels) * 0.5), 3.5))
    plt.bar([v - width / 2 for v in x], fc, width=width, label="full vs clean")
    plt.bar([v + width / 2 for v in x], fx, width=width, label="full vs corrupt")
    plt.xticks(x, labels, rotation=45, ha="right")
    plt.ylabel("JS divergence")
    plt.title("Distribution shift summary")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protein", default="2B61A")
    parser.add_argument("--config", default=None)
    parser.add_argument("--output-dir", default="reports/outputs/mutation")
    parser.add_argument("--top-k", type=int, default=15)
    parser.add_argument("--top-contact-k", type=int, default=4)
    parser.add_argument("--extra-residues", default="")
    parser.add_argument("--jump-residues", default="")
    parser.add_argument("--index-base", type=int, default=1)
    parser.add_argument(
        "--control-n",
        type=int,
        default=0,
        help="Number of flank control residues. 0 means match contact count.",
    )
    parser.add_argument(
        "--allow-online",
        action="store_true",
        help="Allow Hugging Face to reach the network if cache is missing.",
    )
    args = parser.parse_args()

    cfg = load_config(args.protein, args.config)
    model_name = cfg.get("model", "facebook/esm2_t33_650M_UR50D")
    data_path = Path(cfg.get("data_path", "data/full_seq_dict.json"))
    if not data_path.is_absolute():
        data_path = _ROOT_DIR / data_path
    clean_flank = cfg["clean_flank"]
    corrupt_flank = cfg["corrupt_flank"]
    contact_pair = tuple(cfg["contact_pair"])
    segment_radius = cfg["segment_radius"]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    local_only = not args.allow_online
    esm_model = EsmForMaskedLM.from_pretrained(
        model_name, attn_implementation="eager", local_files_only=local_only
    ).to(device)
    esm_model.eval()
    tokenizer = EsmTokenizer.from_pretrained(
        model_name, local_files_only=local_only
    )

    with open(data_path) as f:
        seq_dict = json.load(f)
    if args.protein not in seq_dict:
        raise KeyError(f"Protein '{args.protein}' not found in {data_path}.")
    sequence_S = seq_dict[args.protein]

    seg = ContactSegment.from_contact_pair(*contact_pair, radius=segment_radius)
    clean_tokens = mask_with_flanks_tokens(sequence_S, seg, clean_flank)
    corrupt_tokens = mask_with_flanks_tokens(sequence_S, seg, corrupt_flank)
    clean_seq_S = tokens_to_sequence(clean_tokens)
    corrupt_seq_S = tokens_to_sequence(corrupt_tokens)

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = _ROOT_DIR / out_dir
    out_dir = out_dir / args.protein
    out_dir.mkdir(parents=True, exist_ok=True)

    orig_contacts_AA = compute_contact_map(esm_model, tokenizer, sequence_S, device)
    clean_contacts_AA = compute_contact_map(esm_model, tokenizer, clean_seq_S, device)
    corrupt_contacts_AA = compute_contact_map(esm_model, tokenizer, corrupt_seq_S, device)
    clean_metric = patching_metric(clean_contacts_AA, orig_contacts_AA, seg)
    corrupt_metric = patching_metric(corrupt_contacts_AA, orig_contacts_AA, seg)

    top_contacts = select_top_contacts(clean_contacts_AA, seg, args.top_contact_k)
    contact_indices = sorted({idx for pair in top_contacts for idx in pair[:2]})

    residue_indices = set(contact_indices)

    extra_specs = [s for s in args.extra_residues.split(",") if s.strip()]
    extra_residues: list[tuple[str, int, str | None]] = []
    for spec in extra_specs:
        idx, letter = parse_residue_spec(spec, args.index_base)
        extra_residues.append((spec, idx, letter))
    for spec, idx, letter in extra_residues:
        if 0 <= idx < len(sequence_S):
            residue_indices.add(idx)
            if letter is not None and sequence_S[idx] != letter:
                print(
                    f"Warning: residue {spec} expected {letter} but found {sequence_S[idx]}."
                )

    residue_indices = sorted(residue_indices)

    aa_tokens = get_aa_tokens(tokenizer)
    results: dict[str, dict[str, dict[str, float]]] = {}
    result_meta: dict[str, dict] = {}

    for idx in residue_indices:
        base_label = f"{sequence_S[idx]}{idx + args.index_base}"
        results[base_label] = {}
        result_meta[base_label] = {
            "seq_index": idx,
            "display_index": idx + args.index_base,
        }
        for seq_label, base_tokens in [
            ("full", list(sequence_S)),
            ("clean", clean_tokens),
            ("corrupt", corrupt_tokens),
        ]:
            tokens = list(base_tokens)
            tokens[idx] = "<mask>"
            seq = tokens_to_sequence(tokens)
            results[base_label][seq_label] = masked_token_probs(
                esm_model,
                tokenizer,
                seq,
                idx,
                device,
                aa_tokens,
            )

    flank_candidates = []
    for i, tok in enumerate(clean_tokens):
        if tok == "<mask>":
            continue
        if seg.ss1_start <= i < seg.ss1_end:
            continue
        if seg.ss2_start <= i < seg.ss2_end:
            continue
        if i in residue_indices:
            continue
        flank_candidates.append(i)
    random.seed(0)
    control_n = args.control_n or len(contact_indices)
    control_indices = sorted(random.sample(flank_candidates, k=min(control_n, len(flank_candidates))))
    control_labels = []
    for idx in control_indices:
        label = f"{sequence_S[idx]}{idx + args.index_base}"
        control_labels.append(label)
        results[label] = {}
        result_meta[label] = {
            "seq_index": idx,
            "display_index": idx + args.index_base,
            "control": True,
        }
        for seq_label, base_tokens in [
            ("full", list(sequence_S)),
            ("clean", clean_tokens),
            ("corrupt", corrupt_tokens),
        ]:
            tokens = list(base_tokens)
            tokens[idx] = "<mask>"
            seq = tokens_to_sequence(tokens)
            results[label][seq_label] = masked_token_probs(
                esm_model,
                tokenizer,
                seq,
                idx,
                device,
                aa_tokens,
            )

    jump_specs = [s for s in args.jump_residues.split(",") if s.strip()]
    jump_results: dict[str, dict[str, dict[str, float]]] = {}
    jump_meta: dict[str, dict] = {}
    for spec in jump_specs:
        idx, letter = parse_residue_spec(spec, args.index_base)
        if not (0 <= idx < len(sequence_S)):
            continue
        label = f"{sequence_S[idx]}{idx + args.index_base}"
        jump_results[label] = {}
        jump_meta[label] = {"seq_index": idx, "display_index": idx + args.index_base}
        if letter is not None and sequence_S[idx] != letter:
            print(
                f"Warning: jump residue {spec} expected {letter} but found {sequence_S[idx]}."
            )
        for seq_label, base_tokens in [
            ("full", list(sequence_S)),
            ("corrupt", corrupt_tokens),
        ]:
            tokens = list(base_tokens)
            tokens[idx] = "<mask>"
            seq = tokens_to_sequence(tokens)
            jump_results[label][seq_label] = masked_token_probs(
                esm_model,
                tokenizer,
                seq,
                idx,
                device,
                aa_tokens,
            )

    summary_path = out_dir / "summary.txt"
    with summary_path.open("w") as f:
        f.write(f"Protein: {args.protein}\n")
        f.write(f"Model: {model_name}\n")
        f.write(f"Contact pair: {contact_pair}\n")
        f.write(
            f"Flanks: clean={clean_flank} corrupt={corrupt_flank}\n"
        )
        f.write(f"Clean metric: {clean_metric:.4f}\n")
        f.write(f"Corrupt metric: {corrupt_metric:.4f}\n")
        f.write(f"Gap: {clean_metric - corrupt_metric:.4f}\n\n")
        f.write("Top contacts (clean segment):\n")
        for i, j, v in top_contacts:
            f.write(f"  {i}->{j}: {v:.4f}\n")
        f.write("\nResidues analyzed:\n")
        for label in results:
            meta = result_meta[label]
            f.write(
                f"  {label} (seq_index={meta['seq_index']}, display_index={meta['display_index']})\n"
            )
        if control_labels:
            f.write("\nControl residues:\n")
            for label in control_labels:
                meta = result_meta[label]
                f.write(
                    f"  {label} (seq_index={meta['seq_index']}, display_index={meta['display_index']})\n"
                )
        if jump_results:
            f.write("\nJump residues:\n")
            for label in jump_results:
                meta = jump_meta[label]
                f.write(
                    f"  {label} (seq_index={meta['seq_index']}, display_index={meta['display_index']})\n"
                )

    residue_check_path = out_dir / "residue_check.txt"
    with residue_check_path.open("w") as f:
        f.write("Residue letter checks (sequence index -> amino acid)\n")
        for label in results:
            meta = result_meta[label]
            idx = meta["seq_index"]
            f.write(f"{idx}: {sequence_S[idx]}\n")
        for label in jump_results:
            meta = jump_meta[label]
            idx = meta["seq_index"]
            f.write(f"{idx}: {sequence_S[idx]}\n")

    divergences: dict[str, dict[str, float]] = {}
    for label, seq_map in results.items():
        divergences[label] = {
            "full_clean": js_divergence(seq_map["full"], seq_map["clean"], aa_tokens),
            "full_corrupt": js_divergence(seq_map["full"], seq_map["corrupt"], aa_tokens),
        }

    divergence_path = out_dir / "divergence_summary.txt"
    with divergence_path.open("w") as f:
        f.write("JS divergence summary\n")
        for label in results:
            d = divergences[label]
            f.write(
                f"{label}: full_clean={d['full_clean']:.4f}, full_corrupt={d['full_corrupt']:.4f}\n"
            )

    probs_txt_path = out_dir / "masked_token_probs.txt"
    with probs_txt_path.open("w") as f:
        f.write("Masked token probabilities (top-k)\n\n")
        for label, seq_map in results.items():
            f.write(f"{label}\n")
            for seq_label, probs in seq_map.items():
                top_items = top_k_probs(probs, args.top_k)
                f.write(f"  {seq_label}: ")
                f.write(", ".join([f"{tok} {p:.4f}" for tok, p in top_items]))
                f.write("\n")
            f.write("\n")
        if jump_results:
            f.write("Jump residues (full vs corrupt)\n\n")
            for label, seq_map in jump_results.items():
                f.write(f"{label}\n")
                for seq_label, probs in seq_map.items():
                    top_items = top_k_probs(probs, args.top_k)
                    f.write(f"  {seq_label}: ")
                    f.write(", ".join([f"{tok} {p:.4f}" for tok, p in top_items]))
                    f.write("\n")
                f.write("\n")

    json_path = out_dir / "masked_token_probs.json"
    with json_path.open("w") as f:
        json.dump(
            {
                "protein": args.protein,
                "contact_pair": contact_pair,
                "clean_flank": clean_flank,
                "corrupt_flank": corrupt_flank,
                "top_contacts": top_contacts,
                "residue_meta": result_meta,
                "results": results,
                "control_labels": control_labels,
                "divergences": divergences,
                "jump_meta": jump_meta,
                "jump_results": jump_results,
            },
            f,
            indent=2,
        )

    for label, seq_map in results.items():
        plot_path = out_dir / f"{label}_stacked_top{args.top_k}.png"
        plot_distributions_stacked(
            label, seq_map, args.top_k, plot_path, ["full", "clean", "corrupt"]
        )
    for label, seq_map in jump_results.items():
        plot_path = out_dir / f"{label}_jump_stacked_top{args.top_k}.png"
        plot_distributions_stacked(
            label, seq_map, args.top_k, plot_path, ["full", "corrupt"]
        )

    contact_labels = []
    for idx in sorted({i for pair in top_contacts for i in pair[:2]}):
        label = f"{sequence_S[idx]}{idx + args.index_base}"
        if label in results:
            contact_labels.append(label)
    if contact_labels:
        summary_plot_path = out_dir / "contact_native_prob_summary.png"
        plot_native_prob_summary(contact_labels, results, summary_plot_path)
        divergence_plot_path = out_dir / "divergence_summary.png"
        plot_divergence_summary(contact_labels, control_labels, divergences, divergence_plot_path)

    print(f"Saved outputs to {out_dir}")


if __name__ == "__main__":
    main()
