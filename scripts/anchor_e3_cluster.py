"""Unsupervised cluster structure of anchor windows and K vectors on CATH corpus.

See experiments/5_01_anchor_window_kanchor_cluster.md for the full spec.

Stages:
    load_anchors   -> read anchors.csv + 3Di per-chain strings
    build_windows  -> 31-residue AA and 3Di windows around top-1 anchor
    extract_kqv    -> L10H9 K, Q, V at anchor position via batched ESM2 forward pass
    foldseek_cl    -> foldseek easy-cluster (--tmscore-threshold 0.5) on chain PDBs
    cluster        -> HDBSCAN(precomputed cosine, mcs=max(3, n//12), ms=2) on each rep
    metrics        -> NMI(adjusted), ARI, LOO k=3 kNN accuracy per (rep x label)
    composition    -> cluster x label cross-tabs and dominant-label purity
    null           -> shuffled chain->window NMI null (200 perms, AA and 3Di only)
    plots          -> UMAP grid + bar chart of metrics
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from anchor_e3_cath_repl import (  # noqa: E402
    AA_ALPHABET,
    DI_ALPHABET,
    GAP,
    SETS,
    CATH_DIR,
    WINDOW_HALF,
    load_anchors,
    onehot,
    read_fasta,
    slice_window,
    stage_extract_3di,
)

OUT_DIR = ROOT / "reports" / "out2" / "anchor_e3_cluster"
FOLDSEEK = ROOT / "foldseek" / "bin" / "foldseek"

TARGET_LAYER = 10
TARGET_HEAD = 9
NUM_HEADS = 20
HEAD_DIM = 64
HIDDEN_DIM = 1280


# ---------------------------------------------------------------------------
# Stage: build_windows
# ---------------------------------------------------------------------------

def stage_build_windows(anchors: pd.DataFrame, threed: dict[str, str]) -> pd.DataFrame:
    chain_seqs = json.load(open(CATH_DIR / "chain_seqs.json"))
    rows = []
    for _, r in anchors.iterrows():
        ch = r["chain_key"]
        if ch not in chain_seqs or ch not in threed:
            continue
        aa_seq = chain_seqs[ch]
        di_seq = threed[ch]
        pos = int(r["attn_anchor"])
        rows.append({
            "chain_key": ch,
            "set": r["set"],
            "pfam_id": r["pfam_id"],
            "hsf": r["hsf"],
            "audit_pass": bool(r["audit_pass"]),
            "anchor_pos": pos,
            "n_res": len(aa_seq),
            "aa_seq": aa_seq,
            "w_aa": slice_window(aa_seq, pos),
            "w_3di": slice_window(di_seq, pos),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Stage: extract_kqv (L10H9 K, Q, V at anchor)
# ---------------------------------------------------------------------------

def stage_extract_kqv(windows: pd.DataFrame, device: str, batch_size: int = 4) -> dict:
    from anchor_hmm_experiment import load_model, extract_head_weights, capture_layernorm_outputs

    model, tokenizer = load_model(device)
    weights = extract_head_weights(model, TARGET_LAYER, TARGET_HEAD)
    W_K = weights["W_K_hd"]; b_K = weights["b_K_d"]
    W_Q = weights["W_Q_hd"]; b_Q = weights["b_Q_d"]

    # V slice
    attn = model.esm.encoder.layer[TARGET_LAYER].attention
    W_V_full = attn.self.value.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
    b_V_full = attn.self.value.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
    W_V = W_V_full[TARGET_HEAD].clone()
    b_V = b_V_full[TARGET_HEAD].clone()

    seqs = [" ".join(s) for s in windows["aa_seq"].tolist()]
    anchor_positions = windows["anchor_pos"].tolist()

    # Run in batches; capture_layernorm_outputs returns list of per-sequence tensors
    # batch_size=1 is safest given variable lengths and to avoid padding artefacts at anchor.
    # We still batch by building per-call lists; capture_layernorm_outputs handles padding.
    K = np.zeros((len(seqs), HEAD_DIM), dtype=np.float32)
    Q = np.zeros((len(seqs), HEAD_DIM), dtype=np.float32)
    V = np.zeros((len(seqs), HEAD_DIM), dtype=np.float32)
    Q_mean = np.zeros((len(seqs), HEAD_DIM), dtype=np.float32)
    LN10 = np.zeros((len(seqs), HIDDEN_DIM), dtype=np.float32)
    LN10_rand = np.zeros((len(seqs), HIDDEN_DIM), dtype=np.float32)
    LN10_mean = np.zeros((len(seqs), HIDDEN_DIM), dtype=np.float32)
    rng = np.random.default_rng(0)

    print(f"[extract_kqv] running ESM2 forward on {len(seqs)} chains, bs={batch_size}")
    for start in range(0, len(seqs), batch_size):
        batch = seqs[start:start + batch_size]
        positions = anchor_positions[start:start + batch_size]
        ln_outputs = capture_layernorm_outputs(model, tokenizer, batch, device=device, batch_size=len(batch))
        for j, x_ln in enumerate(ln_outputs):
            pos = positions[j]
            x_anchor = x_ln[pos]  # (1280,)
            k_v = (x_anchor @ W_K.T + b_K).numpy()
            q_v = (x_anchor @ W_Q.T + b_Q).numpy()
            v_v = (x_anchor @ W_V.T + b_V).numpy()
            # Q_mean across all residues of this chain (excluding padding by trimming to n_res)
            n_res = windows["n_res"].iloc[start + j]
            x_full = x_ln[:n_res]
            q_all = (x_full @ W_Q.T + b_Q)
            q_unit = q_all / q_all.norm(dim=-1, keepdim=True).clamp(min=1e-8)
            q_mean = q_unit.mean(dim=0).numpy()
            K[start + j] = k_v
            Q[start + j] = q_v
            V[start + j] = v_v
            Q_mean[start + j] = q_mean
            LN10[start + j] = x_anchor.numpy()
            # random non-anchor position (avoid pos itself; if n_res<=1 fallback to 0)
            x_chain = x_ln[:n_res]
            if n_res > 1:
                cand = list(range(n_res))
                cand.remove(pos)
                rand_pos = int(rng.choice(cand))
            else:
                rand_pos = 0
            LN10_rand[start + j] = x_chain[rand_pos].numpy()
            LN10_mean[start + j] = x_chain.mean(dim=0).numpy()
        if (start // batch_size) % 10 == 0:
            print(f"  {start + len(batch)}/{len(seqs)}")

    return {"K": K, "Q": Q, "V": V, "Q_mean": Q_mean,
            "LN10": LN10, "LN10_rand": LN10_rand, "LN10_mean": LN10_mean}


# ---------------------------------------------------------------------------
# Stage: foldseek easy-cluster
# ---------------------------------------------------------------------------

def stage_foldseek_cluster(chain_keys: list[str]) -> dict[str, str]:
    cache = OUT_DIR / "foldseek_cluster.tsv"
    if cache.exists():
        out = {}
        with cache.open() as f:
            for line in f:
                rep, member = line.strip().split("\t")[:2]
                out[member] = rep
        return out
    if not FOLDSEEK.exists():
        print("[foldseek_cluster] foldseek binary missing; identity-cluster fallback")
        return {ch: ch for ch in chain_keys}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    run_dir = OUT_DIR / "_foldseek_run"
    query_dir = run_dir / "inputs"
    tmp_dir = run_dir / "tmp"
    query_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    src_dir = CATH_DIR / "chain_pdb"
    for ch in chain_keys:
        src = src_dir / f"{ch}.pdb"
        if not src.exists():
            continue
        dst = query_dir / src.name
        if not dst.exists():
            shutil.copy2(src, dst)
    prefix = run_dir / "struct_tm05"
    cmd = [
        str(FOLDSEEK), "easy-cluster", str(query_dir), str(prefix), str(tmp_dir),
        "--tmscore-threshold", "0.5", "--min-seq-id", "0", "-c", "0.0", "--cov-mode", "0",
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    cluster_tsv = Path(f"{prefix}_cluster.tsv")
    out = {}
    with cluster_tsv.open() as f:
        rows = []
        for line in f:
            rep, member = line.strip().split("\t")[:2]
            rep_id = Path(rep).stem
            member_id = Path(member).stem
            out[member_id] = rep_id
            rows.append((rep_id, member_id))
    with cache.open("w") as f:
        for rep_id, member_id in rows:
            f.write(f"{rep_id}\t{member_id}\n")
    return out


# ---------------------------------------------------------------------------
# Stage: cluster + metrics
# ---------------------------------------------------------------------------

def cosine_distance_matrix(X: np.ndarray) -> np.ndarray:
    Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
    sim = Xn @ Xn.T
    sim = np.clip(sim, -1.0, 1.0)
    return (1.0 - sim).astype(np.float64)


def run_hdbscan(D: np.ndarray, n: int) -> np.ndarray:
    import hdbscan
    mcs = max(3, n // 12)
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=mcs, min_samples=2, metric="precomputed",
    )
    return clusterer.fit_predict(D)


def loo_knn_accuracy(D: np.ndarray, labels: np.ndarray, k: int = 3) -> float:
    n = len(labels)
    Dc = D.copy()
    np.fill_diagonal(Dc, np.inf)
    correct = 0
    for i in range(n):
        nn_idx = np.argsort(Dc[i])[:k]
        votes = Counter(labels[nn_idx])
        pred = votes.most_common(1)[0][0]
        correct += int(pred == labels[i])
    return correct / n


def stage_cluster_metrics(reps: dict[str, np.ndarray],
                          labels_df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

    label_cols = ["L_Pfam", "L_HSF", "L_fold", "L_foldseek_cluster"]
    label_arrays = {c: labels_df[c].astype("category").cat.codes.values for c in label_cols}

    rows = []
    cluster_assigns: dict[str, np.ndarray] = {}
    for rep_name, X in reps.items():
        n = X.shape[0]
        D = cosine_distance_matrix(X)
        pred = run_hdbscan(D, n)
        cluster_assigns[rep_name] = pred
        n_clusters = int(len(set(pred)) - (1 if -1 in pred else 0))
        n_noise = int((pred == -1).sum())
        for label_name, lbl in label_arrays.items():
            knn3 = loo_knn_accuracy(D, lbl, k=3)
            mask = (pred != -1)
            if mask.sum() < 2 or len(set(pred[mask])) < 2 or len(set(lbl[mask])) < 2:
                nmi = ari = float("nan")
            else:
                nmi = float(normalized_mutual_info_score(
                    lbl[mask], pred[mask], average_method="arithmetic"))
                ari = float(adjusted_rand_score(lbl[mask], pred[mask]))
            rows.append({
                "rep": rep_name, "label": label_name, "n": n,
                "mcs": max(3, n // 12),
                "n_clusters": n_clusters, "n_noise": n_noise,
                "nmi_hdbscan": nmi, "ari_hdbscan": ari,
                "loo_knn3_acc": knn3,
            })
    return pd.DataFrame(rows), cluster_assigns


def stage_compositions(cluster_assigns: dict[str, np.ndarray],
                       labels_df: pd.DataFrame, out_dir: Path) -> None:
    label_cols = ["L_Pfam", "L_HSF", "L_fold", "L_foldseek_cluster"]
    for rep_name, pred in cluster_assigns.items():
        df = labels_df.copy()
        df["cluster"] = pred
        rows = []
        for cid, sub in df.groupby("cluster"):
            row = {"cluster": int(cid), "n_chains": len(sub)}
            for lbl in label_cols:
                vc = sub[lbl].value_counts()
                if len(vc) == 0:
                    row[f"{lbl}_dom"] = None
                    row[f"{lbl}_purity"] = float("nan")
                else:
                    row[f"{lbl}_dom"] = vc.index[0]
                    row[f"{lbl}_purity"] = float(vc.iloc[0]) / len(sub)
                row[f"{lbl}_n_unique"] = int(sub[lbl].nunique())
            rows.append(row)
        comp = pd.DataFrame(rows).sort_values("cluster")
        comp.to_csv(out_dir / f"composition_{rep_name}.csv", index=False)


# ---------------------------------------------------------------------------
# Stage: shuffled null
# ---------------------------------------------------------------------------

def stage_shuffled_null(reps: dict[str, np.ndarray], labels_df: pd.DataFrame,
                        n_perms: int = 200, seed: int = 0) -> pd.DataFrame:
    from sklearn.metrics import normalized_mutual_info_score
    rng = np.random.default_rng(seed)
    label_cols = ["L_Pfam", "L_HSF"]
    rows = []
    for rep_name in ("R_AA", "R_3Di"):
        X = reps[rep_name]
        n = X.shape[0]
        D = cosine_distance_matrix(X)
        pred = run_hdbscan(D, n)
        mask = pred != -1
        if mask.sum() < 2 or len(set(pred[mask])) < 2:
            continue
        for label_name in label_cols:
            lbl = labels_df[label_name].astype("category").cat.codes.values
            nulls = []
            for _ in range(n_perms):
                perm = rng.permutation(n)
                lbl_p = lbl[perm]
                if len(set(lbl_p[mask])) < 2:
                    continue
                nulls.append(float(normalized_mutual_info_score(
                    lbl_p[mask], pred[mask], average_method="arithmetic")))
            nulls = np.array(nulls)
            rows.append({
                "rep": rep_name, "label": label_name, "n_perms": len(nulls),
                "null_mean": float(nulls.mean()),
                "null_p95": float(np.percentile(nulls, 95)) if len(nulls) else float("nan"),
                "null_max": float(nulls.max()) if len(nulls) else float("nan"),
            })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def stage_plots(reps: dict[str, np.ndarray], labels_df: pd.DataFrame,
                metrics: pd.DataFrame, cluster_assigns: dict[str, np.ndarray],
                out_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # UMAP grid: 4 reps x 4 colorings
    try:
        import umap
        umap_ok = True
    except Exception as e:
        print(f"[plots] UMAP unavailable ({e}); skipping fig_umap")
        umap_ok = False

    label_cols = ["L_Pfam", "L_HSF", "L_fold", "L_foldseek_cluster"]
    rep_order = ["R_AA", "R_3Di", "R_K", "R_Q", "R_LN10", "R_LN10_rand", "R_LN10_mean"]

    if umap_ok:
        fig, axes = plt.subplots(len(rep_order), len(label_cols),
                                 figsize=(4 * len(label_cols), 3.2 * len(rep_order)))
        for ri, rep_name in enumerate(rep_order):
            X = reps[rep_name]
            try:
                emb = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine",
                                random_state=0).fit_transform(X)
            except Exception as e:
                print(f"[plots] UMAP failed for {rep_name}: {e}")
                continue
            for ci, lbl in enumerate(label_cols):
                ax = axes[ri, ci]
                codes = labels_df[lbl].astype("category").cat.codes.values
                ax.scatter(emb[:, 0], emb[:, 1], c=codes, s=10, cmap="tab20", alpha=0.85)
                ax.set_title(f"{rep_name} | {lbl}", fontsize=9)
                ax.set_xticks([]); ax.set_yticks([])
        fig.tight_layout()
        fig.savefig(out_dir / "fig_umap.png", dpi=140)
        plt.close(fig)

    # Bar chart: kNN acc and NMI per (rep x label)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    width = 0.18
    xs = np.arange(len(label_cols))
    for ri, rep_name in enumerate(rep_order):
        sub = metrics[metrics["rep"] == rep_name].set_index("label").reindex(label_cols)
        offset = (ri - (len(rep_order) - 1) / 2) * width
        axes[0].bar(xs + offset, sub["loo_knn3_acc"].values, width, label=rep_name)
        axes[1].bar(xs + offset, sub["nmi_hdbscan"].values, width, label=rep_name)
    for ax, ttl, ylim in [(axes[0], "LOO k=3 NN accuracy", (0, 1.0)),
                           (axes[1], "HDBSCAN NMI (adjusted)", (0, 1.0))]:
        ax.set_xticks(xs); ax.set_xticklabels(label_cols, rotation=20, fontsize=8)
        ax.set_ylim(*ylim)
        ax.set_title(ttl, fontsize=10)
        ax.axhline(0.50, color="grey", lw=0.5, ls="--")
        ax.axhline(0.75, color="red", lw=0.5, ls="--")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "fig_metrics.png", dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def derive_labels(windows: pd.DataFrame, foldseek_clusters: dict[str, str]) -> pd.DataFrame:
    df = windows[["chain_key", "set", "pfam_id", "hsf", "audit_pass"]].copy()
    df["L_Pfam"] = df["pfam_id"].astype(str)
    df["L_HSF"] = df["hsf"].astype(str)
    fold_map = {
        "A_3.40.50.720": "alpha_beta",
        "B_3.40.50.1820": "alpha_beta",
        "C_2.60.40.10": "all_beta",
    }
    df["L_fold"] = df["set"].map(fold_map).fillna("other")
    df["L_foldseek_cluster"] = df["chain_key"].map(foldseek_clusters).fillna(df["chain_key"])
    return df.reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--audit-only", action="store_true",
                    help="Subset to audit-pass chains (supplementary; primary is full corpus)")
    ap.add_argument("--n-perm", type=int, default=200)
    ap.add_argument("--skip-perm", action="store_true")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tag = "audit" if args.audit_only else "all"

    print(f"[main] tag={tag} device={args.device}")

    print("[main] loading anchors and 3Di strings")
    anchors = load_anchors()
    threed = stage_extract_3di()

    if args.audit_only:
        anchors = anchors[anchors["audit_pass"]].copy()

    print("[main] building windows")
    windows = stage_build_windows(anchors, threed)
    print(f"  windows: n={len(windows)}")

    print("[main] foldseek easy-cluster")
    foldseek_clusters = stage_foldseek_cluster(windows["chain_key"].tolist())
    n_fs_unique = len(set(foldseek_clusters.values()))
    print(f"  foldseek clusters: {n_fs_unique} unique reps for {len(foldseek_clusters)} chains")

    labels_df = derive_labels(windows, foldseek_clusters)

    print("[main] one-hot encoding windows")
    R_AA = onehot(windows["w_aa"].tolist(), AA_ALPHABET)
    R_3Di = onehot(windows["w_3di"].tolist(), DI_ALPHABET)

    print("[main] extracting K/Q/V at anchor")
    kqv = stage_extract_kqv(windows, args.device, batch_size=args.batch_size)

    np.save(OUT_DIR / f"windows_aa_{tag}.npy", R_AA)
    np.save(OUT_DIR / f"windows_3di_{tag}.npy", R_3Di)
    np.save(OUT_DIR / f"k_anchor_{tag}.npy", kqv["K"])
    np.save(OUT_DIR / f"q_anchor_{tag}.npy", kqv["Q"])
    np.save(OUT_DIR / f"v_anchor_{tag}.npy", kqv["V"])
    np.save(OUT_DIR / f"q_mean_{tag}.npy", kqv["Q_mean"])
    np.save(OUT_DIR / f"ln10_anchor_{tag}.npy", kqv["LN10"])
    np.save(OUT_DIR / f"ln10_rand_{tag}.npy", kqv["LN10_rand"])
    np.save(OUT_DIR / f"ln10_mean_{tag}.npy", kqv["LN10_mean"])
    labels_df.to_csv(OUT_DIR / f"labels_{tag}.csv", index=False)
    windows[["chain_key", "set", "pfam_id", "hsf", "audit_pass",
             "anchor_pos", "n_res", "w_aa", "w_3di"]].to_csv(
        OUT_DIR / f"windows_{tag}.csv", index=False)

    reps = {
        "R_AA": R_AA,
        "R_3Di": R_3Di,
        "R_K": kqv["K"],
        "R_Q": kqv["Q"],
        "R_LN10": kqv["LN10"],
        "R_LN10_rand": kqv["LN10_rand"],
        "R_LN10_mean": kqv["LN10_mean"],
    }

    print("[main] clustering and metrics")
    metrics, cluster_assigns = stage_cluster_metrics(reps, labels_df)
    metrics.to_csv(OUT_DIR / f"metrics_{tag}.csv", index=False)
    print(metrics.to_string(index=False))

    ca_df = pd.DataFrame({"chain_key": labels_df["chain_key"].values})
    for k, v in cluster_assigns.items():
        ca_df[f"hdbscan_{k}"] = v
    ca_df.to_csv(OUT_DIR / f"cluster_assignments_{tag}.csv", index=False)

    print("[main] cluster compositions")
    stage_compositions(cluster_assigns, labels_df, OUT_DIR)
    for k in cluster_assigns:
        src = OUT_DIR / f"composition_{k}.csv"
        dst = OUT_DIR / f"composition_{k}_{tag}.csv"
        if src.exists():
            shutil.move(src, dst)

    if not args.skip_perm:
        print(f"[main] shuffled null ({args.n_perm} perms)")
        null = stage_shuffled_null(reps, labels_df, n_perms=args.n_perm)
        null.to_csv(OUT_DIR / f"shuffled_null_{tag}.csv", index=False)
        print(null.to_string(index=False))

    print("[main] plotting")
    stage_plots(reps, labels_df, metrics, cluster_assigns, OUT_DIR)
    for fname in ("fig_umap.png", "fig_metrics.png"):
        src = OUT_DIR / fname
        if src.exists():
            dst = OUT_DIR / f"{fname.rsplit('.', 1)[0]}_{tag}.png"
            shutil.move(src, dst)

    print(f"[main] done. outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
