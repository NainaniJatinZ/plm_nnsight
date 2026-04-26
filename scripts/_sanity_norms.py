"""Measure residual stream norms and d-projection at anchor positions to understand intervention scale."""
import json, torch, numpy as np, os, sys, warnings
warnings.filterwarnings("ignore")

os.environ["HF_HOME"] = "/work/pi_jensen_umass_edu/jnainani_umass_edu/ESM_Interp/weights/"
from nnsight import NNsight
from transformers import EsmForMaskedLM, EsmTokenizer

model_name = "facebook/esm2_t33_650M_UR50D"
cache_dir = os.environ["HF_HOME"]
tokenizer = EsmTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
esm_model = EsmForMaskedLM.from_pretrained(model_name, cache_dir=cache_dir, attn_implementation="eager").cuda().eval()
model = NNsight(esm_model)
contact_head = esm_model.esm.contact_head

seqs = json.load(open("data/full_seq_dict.json"))

NUM_HEADS, HEAD_DIM, HIDDEN_DIM = 20, 64, 1280
TARGET_LAYER, TARGET_HEAD = 10, 9
NUM_LAYERS = 33

attn_mod = model._model.esm.encoder.layer[TARGET_LAYER].attention
W_K = attn_mod.self.key.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
b_K = attn_mod.self.key.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)
W_Q = attn_mod.self.query.weight.data.cpu().reshape(NUM_HEADS, HEAD_DIM, HIDDEN_DIM)
b_Q = attn_mod.self.query.bias.data.cpu().reshape(NUM_HEADS, HEAD_DIM)

# Compute d_unit from 2B61A
ref_seq = seqs["2B61A"]
inputs = tokenizer(ref_seq, return_tensors="pt").to("cuda")
ln_module = model.esm.encoder.layer[TARGET_LAYER].attention.LayerNorm
with model.trace() as tracer:
    with tracer.invoke(**inputs):
        cache = tracer.cache(modules=[ln_module])
ln_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.LayerNorm"
x_ln = cache[ln_key].output.detach().cpu()[0]
q_all = x_ln @ W_Q[TARGET_HEAD].T + b_Q[TARGET_HEAD]
q_res = q_all[1:-1]
q_unit = q_res / q_res.norm(dim=-1, keepdim=True).clamp(min=1e-8)
q_mean = q_unit.mean(dim=0)
q_mean_norm = q_mean / q_mean.norm().clamp(min=1e-8)
search_dir = W_K[TARGET_HEAD].T @ q_mean_norm
d_unit = (search_dir / search_dir.norm().clamp(min=1e-8)).cuda()

print(f"d_unit norm: {d_unit.norm().item():.4f}")
print(f"search_dir (pre-normalization) norm: {search_dir.norm().item():.4f}")
print()

# -------------------------------------------------------------------
# Part 1: Measure norms and projections
# -------------------------------------------------------------------
test_proteins = ["2B61A", "1PVGA", "3CSSA", "1A8LA", "1B63A", "1BYIA", "1C3PA", "1COJA", "1DPGA", "1EKEA"]
test_proteins = [p for p in test_proteins if p in seqs]

print("=" * 80)
print("PART 1: Scale of intervention relative to residual stream")
print("=" * 80)
print(f'{"protein":>8}  {"anchor":>6}  {"||x_ln||":>8}  {"x·d":>6}  {"mean||x||":>10}  {"x·d/||x||":>10}')
print("-" * 65)

all_anchor_norms = []
all_anchor_projs = []

for pkey in test_proteins:
    seq = seqs[pkey]
    inp = tokenizer(seq, return_tensors="pt").to("cuda")
    attn_module = model.esm.encoder.layer[TARGET_LAYER].attention.self
    with model.trace() as tracer:
        with tracer.invoke(**inp, output_attentions=True):
            attn_cache = tracer.cache(modules=[attn_module])
            ln_cache = tracer.cache(modules=[ln_module])

    attn_key = f"model.esm.encoder.layer.{TARGET_LAYER}.attention.self"
    attn_HLL = attn_cache[attn_key].output[1].detach().cpu()[0]
    attn_AA = attn_HLL[TARGET_HEAD, 1:-1, 1:-1].numpy()
    key_mass = attn_AA.mean(axis=0)
    anchor = int(np.argmax(key_mass))

    x_ln_all = ln_cache[ln_key].output.detach().cpu()[0]
    x_ln_res = x_ln_all[1:-1]

    anchor_vec = x_ln_res[anchor]
    anchor_norm = anchor_vec.norm().item()
    anchor_proj = (anchor_vec @ d_unit.cpu()).item()
    mean_norm = x_ln_res.norm(dim=-1).mean().item()

    all_anchor_norms.append(anchor_norm)
    all_anchor_projs.append(anchor_proj)

    print(f"{pkey:>8}  {anchor:>6}  {anchor_norm:>8.2f}  {anchor_proj:>6.2f}  {mean_norm:>10.2f}  {anchor_proj/anchor_norm:>10.4f}")

mean_proj = np.mean(all_anchor_projs)
mean_norm = np.mean(all_anchor_norms)
print()
print(f"Mean anchor ||x_ln||: {mean_norm:.2f}")
print(f"Mean anchor x·d:      {mean_proj:.2f}")
print()
print("What alpha means in context:")
for alpha in [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]:
    overshoot = alpha / mean_proj
    frac_of_norm = alpha / mean_norm * 100
    print(f"  alpha={alpha:5.1f}  |  {overshoot:.1f}x the d-component  |  {frac_of_norm:.1f}% of ||x_ln||")

# -------------------------------------------------------------------
# Part 2: Random direction control
# -------------------------------------------------------------------
print()
print("=" * 80)
print("PART 2: Random direction control")
print("Subtract alpha * r_unit (random) at anchor, compare contact prediction to d_unit")
print("=" * 80)

sys.path.insert(0, os.path.dirname(__file__))
from anchor_contact_steering import (
    cache_attention_with_steering, compute_contacts_from_attention,
    parse_pdb_contacts, precision_at_k, identify_anchors,
)

test_alphas = [0.0, 1.0, 4.0, 8.0, 16.0, 32.0]
n_random_dirs = 5

# Pick a few proteins with PDBs
pdb_dir = "data/pdb"
pdb_set = {f[:-4] for f in os.listdir(pdb_dir) if f.endswith(".pdb")}
pdb_proteins = [p for p in test_proteins if p[:4] in pdb_set and 100 <= len(seqs[p]) <= 500][:5]

for pkey in pdb_proteins:
    seq = seqs[pkey]
    seq_len = len(seq)
    gt = parse_pdb_contacts(pkey, seq)
    if gt is None:
        continue
    n_lr = np.triu(gt, k=24).sum()
    if n_lr < 10:
        continue

    anchors = identify_anchors(model, tokenizer, seq, "cuda", top_k=1)
    print(f"\n  {pkey} ({seq_len} res, {n_lr} LR contacts, anchor={anchors[0]})")
    print(f"  {'alpha':>6}  |  {'d_unit P@L/5':>12}  |  {'random P@L/5 (mean of 5)':>25}  |  {'random std':>10}")

    for alpha in test_alphas:
        # d_unit steering
        attn_d, inp_d = cache_attention_with_steering(model, tokenizer, seq, anchors, d_unit, alpha, "cuda")
        pred_d = compute_contacts_from_attention(attn_d, inp_d["input_ids"], inp_d["attention_mask"], contact_head, "cuda")
        pred_d = pred_d[0].detach().cpu().numpy()
        p_d = precision_at_k(pred_d, gt, max(1, seq_len // 5))

        # Random directions
        p_randoms = []
        for seed in range(n_random_dirs):
            torch.manual_seed(seed + 42)
            r_unit = torch.randn(1280, device="cuda")
            r_unit = r_unit / r_unit.norm()
            attn_r, inp_r = cache_attention_with_steering(model, tokenizer, seq, anchors, r_unit, alpha, "cuda")
            pred_r = compute_contacts_from_attention(attn_r, inp_r["input_ids"], inp_r["attention_mask"], contact_head, "cuda")
            pred_r = pred_r[0].detach().cpu().numpy()
            p_randoms.append(precision_at_k(pred_r, gt, max(1, seq_len // 5)))

        r_mean = np.mean(p_randoms)
        r_std = np.std(p_randoms)
        print(f"  {alpha:6.1f}  |  {p_d:>12.4f}  |  {r_mean:>25.4f}  |  {r_std:>10.4f}")

print()
print("=" * 80)
print("If d_unit and random collapse at the same alpha, the effect is nonspecific.")
print("If d_unit collapses earlier/harder, suppressing d specifically matters.")
print("=" * 80)
