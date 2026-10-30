# The Through-Line Lab — Recipes and Canonical Numbers

The tutor's reference for the worked example: **one small character-level language model
on Tiny Shakespeare, post-trained by hand.** The code below was smoke-tested on a laptop
CPU (PyTorch 2.7, Apple silicon, 8 threads) on 2026-10-29. **Don't paste it at the
learner** — build each piece *with* them, a few lines at a time, in the phase where it is
earned; this file keeps the definitions identical across sessions so the numbers below
stay comparable. Keep the learner's code and checkpoints in their own working directory
(recorded in `progress.md`), never in this repo.

Every number marked *(measured)* is from one seed on one machine: expect the same
**shape**, not the same third decimal. Re-measure and record the learner's own values in
`progress.md` under "Numbers we reuse".

---

## 1. The corpus — fail fast

```python
import hashlib, sys
from pathlib import Path
CORPUS = Path("../curricula/assets/ai-llms-and-sequence-models/tinyshakespeare.txt")
SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"

def load_corpus(path: Path = CORPUS) -> str:
    if not path.is_file():
        sys.exit(f"FATAL: corpus not found at {path}")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA256:
        sys.exit(f"FATAL: SHA-256 mismatch for {path}")
    return raw.decode("ascii")
```

The corpus ships with the course (in the repo, and bundled into the plugin), so a
missing file or a mismatch is a stop, never a substitution: say so and let the learner
fix the install.

```python
import torch
text = load_corpus()
chars = sorted(set(text)); assert len(chars) == 65         # \n, space, !$&',-.3:;?, A-Z, a-z
stoi = {c: i for i, c in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda ids: "".join(chars[i] for i in ids)
data = torch.tensor(encode(text), dtype=torch.long)
n_train = int(0.9 * len(data))                              # 1,003,854 train / 111,540 val
train_data, val_data = data[:n_train], data[n_train:]
```

## 2. The starting model

### 2a. The checkpoint contract (course 2's model)

Post-training needs only two operations — **sample**, and **score `log π(y_t | y_<t)`** —
so any architecture from `ai-sequence-models` works (Transformer, Mamba, hybrid). Check:

1. **Vocabulary:** the same 65 characters in `sorted(set(text))` order. If the checkpoint
   stores a different order, build the index remap explicitly; if it has a different
   character set, stop and say so.
2. **Interface:** a module mapping a `LongTensor (B, T)` to causal logits `(B, T, 65)`,
   with a known maximum context (`block`). Wrap it if needed so `model(idx)` does exactly
   this.
3. **Quality:** measure val NLL on the split above (§2c's `val_nll`) and record it. Any
   value well below the bigram's 2.48 nats/char is fine.
4. **Hidden state (for the reward model in Phase 5):** a `model.hidden(idx) → (B, T, d)`
   method, or a forward hook on the last block. If that is awkward for the learner's
   architecture, train the reward model on the fallback Transformer and say so.

### 2b. The fallback model (stated explicitly to the learner, never silently)

A nanoGPT-style character Transformer: 4 layers, 4 heads, width 128, context 128 —
**826,433 parameters**.

```python
import torch.nn as nn, torch.nn.functional as F

class Block(nn.Module):
    def __init__(self, d: int, h: int):
        super().__init__()
        self.h = h
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(self, x):
        B, T, C = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(C, dim=2)
        q, k, v = (t.view(B, T, self.h, C // self.h).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.proj(y.transpose(1, 2).reshape(B, T, C))
        return x + self.mlp(self.ln2(x))

class TinyGPT(nn.Module):
    def __init__(self, vocab=65, block=128, d=128, layers=4, heads=4):
        super().__init__()
        self.block = block
        self.tok, self.pos = nn.Embedding(vocab, d), nn.Embedding(block, d)
        self.blocks = nn.Sequential(*[Block(d, heads) for _ in range(layers)])
        self.ln, self.head = nn.LayerNorm(d), nn.Linear(d, vocab)
    def hidden(self, idx):                                   # (B, T) -> (B, T, d)
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        return self.ln(self.blocks(x))
    def forward(self, idx):                                  # (B, T) -> (B, T, 65) logits
        return self.head(self.hidden(idx))
```

### 2c. Pretraining (Phase 0.2 fallback; also Phase 9.3's scaling sweep)

```python
def batch(d, B=32, T=128):
    ix = torch.randint(len(d) - T - 1, (B,))
    return torch.stack([d[i:i + T] for i in ix]), torch.stack([d[i + 1:i + T + 1] for i in ix])

@torch.no_grad()
def val_nll(model, d=None, iters=50):
    d = val_data if d is None else d
    model.eval(); tot = 0.0
    for _ in range(iters):
        x, y = batch(d); tot += F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train(); return tot / iters

torch.manual_seed(1337)
model = TinyGPT(); opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
for it in range(3001):
    x, y = batch(train_data)
    loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
    opt.zero_grad(); loss.backward(); opt.step()
torch.save({"model": model.state_dict(), "chars": chars,
            "config": dict(vocab=65, block=128, d=128, layers=4, heads=4)}, "base.pt")
```

*(measured)* val NLL 4.32 → 2.05 (500 steps) → 1.82 (1000) → 1.64 (2000) → **1.58**
(3000), about **3 minutes**. Samples spell most words, keep speaker headers and line
breaks, and make no sense — perfect: the structure we are about to reward is visible.

## 3. Plumbing (Phase 0.3)

```python
@torch.no_grad()
def sample(model, prompt_ids, n_new=96, temp=1.0):
    idx = prompt_ids.clone()
    for _ in range(n_new):
        logits = model(idx[:, -model.block:])[:, -1] / temp
        idx = torch.cat([idx, torch.multinomial(F.softmax(logits, -1), 1)], 1)
    return idx

def completion_logps(model, seq, P):
    """Per-token log pi(y_t | y_<t) of the completion seq[:, P:], and the full
    log-softmax rows (B, n, 65). Assumes seq fits in model.block (7 + 96 < 128 here)."""
    lp = F.log_softmax(model(seq)[:, P - 1:-1], -1)
    return lp.gather(-1, seq[:, P:].unsqueeze(-1)).squeeze(-1), lp

def exact_kl(lp, ref_lp):
    """Exact KL(pi || pi_ref) per sequence along the sampled path: sum over steps of the
    full 65-way sum. Its expectation over samples is the sequence-level KL."""
    return (lp.exp() * (lp - ref_lp)).sum(-1).sum(-1)
```

Prompts: one speaker header per batch, e.g. `torch.tensor([encode("ROMEO:\n")] * 32)`
(`P = 7`), alternating `ROMEO`/`JULIET` between batches so prompts in a batch share a
length.

## 4. The meter reward — the gold reward (Phases 2.6, 5)

A deliberately simple syllable counter: vowel groups per word, minus a silent final `e`.
Cheap, legible, and **hackable** on purpose.

```python
import re
SPEAKER = re.compile(r"^[A-Z][A-Za-z ']*:$")               # e.g. "ROMEO:", "KING RICHARD III:"

def syllables(word: str) -> int:
    w = word.lower()
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee")): n -= 1
    return max(n, 1)

def line_syllables(line: str) -> int:
    return sum(syllables(w) for w in re.findall(r"[A-Za-z']+", line))

def line_score(line: str) -> float:                          # 1 at ten syllables, 0 at <=5 or >=15
    return 1 - min(abs(line_syllables(line) - 10), 5) / 5

def meter_reward_v0(completion: str) -> float:               # NAIVE: scores speaker headers too
    lines = [l for l in completion.split("\n")[:-1] if l.strip()]
    return sum(map(line_score, lines)) / len(lines) if lines else 0.0

def meter_reward(completion: str) -> float:                  # v1: complete speech lines only
    lines = completion.split("\n")[:-1]
    body = [l for l in lines if l.strip() and not SPEAKER.match(l.strip())]
    return sum(map(line_score, body)) / len(body) if body else 0.0
```

`v0` is the Phase 5.4 misspecification exhibit: a header like `ROMEO:` scores 0.0 (two
syllables), so a `v0`-optimized policy learns to stop naming speakers. `v1` is the
course's gold reward from then on. (`v0` itself was not run in the smoke test; predict,
then run.)

*(measured, by this counter)* Of the corpus's 25,555 speech lines, **41.0%** have exactly
ten syllables and **68.3%** have nine to eleven (mean 9.73, median 10) — Shakespeare's
pentameter shows through even a crude counter. Mean `meter_reward` over two-line turns in
the val region: **0.667**. Rhymed consecutive lines (same last two letters, different
word): 3.2%.

**Known hacks** (what the learner should find, not be told): repeat one high-scoring
line; pad with monosyllables (`and the and the …`); drop speakers under `v0`; under a
tool (Phase 11.4), copy corpus lines.

## 5. SFT — the two-line reply convention (Phase 4.2)

```python
def two_line_turns(region: str) -> str:
    out = []
    for b in region.split("\n\n"):
        ls = b.strip("\n").split("\n")
        if len(ls) >= 3 and SPEAKER.match(ls[0]):
            out.append("\n".join(ls[:3]))                    # header + first two lines
    return "\n\n".join(out) + "\n\n"

sft_train = torch.tensor(encode(two_line_turns(text[:n_train])))   # 339,521 chars
sft_val   = torch.tensor(encode(two_line_turns(text[n_train:])))   # 39,850 chars (446 turns)
# fine-tune base.pt: AdamW lr 3e-4, 600 steps of batch(sft_train) -> save "sft.pt"
```

Format metric: of 64 samples after `ROMEO:\n`, the fraction whose reply is exactly two
non-empty lines, a blank line, then a speaker header.

*(measured)* format rate **0.17 → ≈ 0.60** (noisy at 64 samples: 0.48–0.63 over steps
300–600); two-line val NLL 1.62 → 1.56; general val NLL 1.58 → 1.61 (the alignment tax).
SFT samples' mean meter reward: **0.60**.

Why this slice and not, say, Romeo's lines: one speaker's turns (≈ 40k characters) are
too few to fine-tune on without immediate over-fitting, and they sit inside the base
model's training region, so a "held-out" score would leak. A *convention* applied to
separate train and val regions is clean.

## 6. Best-of-n (Phase 6.3; frontier 11.3)

Sample `n` completions from `π_ref = sft.pt`, keep the highest meter reward. KL from
`π_ref` is at most `log n − (n−1)/n`.

| n | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|
| mean best reward *(measured, 256 samples)* | 0.60 | 0.73 | 0.87 | 0.91 | 0.94 |
| KL bound (nats) | 0 | 0.19 | 0.64 | 1.20 | 1.84 |

## 7. REINFORCE → PPO-lite with the leash (Phases 2.6, 6.4)

```python
ref = TinyGPT(); ref.load_state_dict(torch.load("sft.pt")["model"]); ref.eval()
for p in ref.parameters(): p.requires_grad_(False)
pol = TinyGPT(); pol.load_state_dict(torch.load("sft.pt")["model"])
opt = torch.optim.Adam(pol.parameters(), lr=1e-4)      # PPO-lite: 5e-5
beta, ppo_epochs, eps = 0.03, 4, 0.2                   # REINFORCE: ppo_epochs = 1, no clip

def rl_step(step: int):
    P_ids = torch.tensor([encode(("ROMEO", "JULIET")[step % 2] + ":\n")] * 32); P = P_ids.shape[1]
    seq = sample(pol, P_ids)
    r = torch.tensor([meter_reward(decode(s[P:].tolist())) for s in seq])
    with torch.no_grad():
        old_tok, _ = completion_logps(pol, seq, P)
        ref_tok, _ = completion_logps(ref, seq, P)
    R = r - beta * (old_tok - ref_tok).sum(-1)          # InstructGPT eq. 2, sample estimate
    A = (R - R.mean()) / (R.std() + 1e-6)               # batch baseline (a control variate)
    for _ in range(ppo_epochs):
        tok, _ = completion_logps(pol, seq, P)
        if ppo_epochs == 1:                             # REINFORCE
            loss = -(A * tok.sum(-1)).mean()
        else:                                           # PPO clipped surrogate, per token
            ratio = (tok - old_tok).exp()
            loss = -torch.min(ratio * A[:, None], ratio.clamp(1 - eps, 1 + eps) * A[:, None]).mean()
        opt.zero_grad(); loss.backward()
        torch.nn.utils.clip_grad_norm_(pol.parameters(), 1.0); opt.step()
```

Log every 50 steps: mean meter reward, mean `exact_kl` to `ref`, distinct-4-gram rate,
and **one sample, read aloud**.

*(measured, 300 steps × 32 completions from `sft.pt`; ≈ 2–4 s/step on CPU, so ~15
minutes a run — start one, then teach while it runs)*. Start: reward **0.60**, KL 0,
distinct-4 0.73.

| run | final reward | final KL (nats/completion) | distinct-4 | what the samples look like |
|---|---|---|---|---|
| REINFORCE, `β = 0` | 0.88 | 34 | 0.63 | invented words creeping in (`proclact`, `mortune-low`) |
| REINFORCE, `β = 0.1` | 0.75 | 2.4 | 0.73 | indistinguishable from SFT samples |
| PPO-lite, `β = 0` | **0.93** | **160** | **0.42** | **the hack:** `For, if ind; if ind, if, by Wick, if.` / `O, sis, if, wid yid, by thy hid, if, Gen yed,` — monosyllable padding to hit ten |
| PPO-lite, `β = 0.03` | 0.78 | 9.3 | 0.69 | Shakespeare-shaped nonsense, as before: `I cannot said, what I will do not ever` |

The `β = 0` PPO trajectory is the keystone exhibit: reward 0.75 / 0.84 / 0.80 / 0.86 /
0.90 / 0.93 at KL 16 / 38 / 65 / 97 / 150 / 160 (steps 50–300) — the last 0.1 of reward
costs 100+ nats and every trace of language. The leashed run's KL levels off near 8–9.
And note, honestly: **best-of-16 (0.94 at KL ≤ 1.84) beats every trained run here** on
the reward-vs-KL plane — best-of-n is a strong baseline, and on a tiny model with a short
budget, sampling is cheaper than learning. Say so; it is a real finding in the literature
too.

## 8. A learned reward model and over-optimization (Phases 5.3, 6.5)

```python
class RewardModel(nn.Module):
    def __init__(self, trunk: TinyGPT):
        super().__init__(); self.trunk = trunk; self.v = nn.Linear(trunk.head.in_features, 1)
    def forward(self, seq):                              # score = head on the last position
        return self.v(self.trunk.hidden(seq)[:, -1]).squeeze(-1)

def label(r_a: float, r_b: float, temp: float = 0.1) -> bool:
    """Simulated labeler: Bradley-Terry with the gold reward, P(a > b) = sigmoid((r_a - r_b)/temp)."""
    return torch.rand(()) < torch.sigmoid(torch.tensor((r_a - r_b) / temp))

# pairs: two samples per prompt from ref (one prompt, e.g. "ROMEO:\n", so lengths match);
# trunk initialized from sft.pt
# loss = -F.logsigmoid(rm(y_w) - rm(y_l)).mean(); report held-out pair accuracy vs gold
```

Then run §7 (REINFORCE, `β = 0`) with `r = rm(seq)` (no grad through the RM) while *also*
logging the gold `meter_reward`. Plot both against `√KL`.

*(measured: 1,536 training pairs, BT label temperature 0.1, AdamW 1e-4, 3 epochs)* The RM
is **weak** — held-out pair accuracy against the gold ordering only **0.57** (noisy labels,
small reward gaps, and counting syllables is hard for an 800k-parameter model). That makes
it a good proxy to over-optimize:

| step | 25 | 50 | 100 | 150 | 200 | 250 |
|---|---|---|---|---|---|---|
| proxy `r_φ` | 0.48 | 0.33 | 0.44 | 0.90 | 1.34 | 1.45 |
| gold meter | 0.67 | 0.72 | 0.69 | 0.65 | 0.74 | 0.73 |
| √KL | 1.7 | 2.7 | 3.5 | 4.8 | 5.9 | 7.2 |

The proxy triples while the gold, measured on 32 samples per point (noisy: ±0.03), gains
nothing after the first ~50 steps; and the policy finds a **proxy-only exploit** the gold
reward ignores entirely — speaker headers mutate into `DUCHINCHINCHINCHFFord`. Exercises:
evaluate gold on 128 samples per point to see the curve properly; train a better RM (more
pairs, lower label noise) and watch the gold peak move right — Gao et al.'s "bigger RM,
later turn" in miniature.

## 9. DPO (Phase 7.3)

```python
def dpo_loss(pol, ref, y_w, y_l, P, beta=0.1):
    with torch.no_grad():
        rw, _ = completion_logps(ref, y_w, P); rl, _ = completion_logps(ref, y_l, P)
    pw, _ = completion_logps(pol, y_w, P); pl, _ = completion_logps(pol, y_l, P)
    h = beta * ((pw.sum(-1) - rw.sum(-1)) - (pl.sum(-1) - rl.sum(-1)))
    return -F.logsigmoid(h).mean()
```

Pairs: two samples per prompt from `ref`, winner by the gold reward (drop ties), batches
grouped by prompt length; Adam lr 1e-5, two epochs. Report reward and `exact_kl` on fresh
samples and place the point on the §7 plot.

*(measured, 1,375 pairs from 1,536 samples, `β = 0.1`)* loss 0.69 → 0.61; reward
**0.60 → 0.68 → 0.69** at KL **0.36 → 0.73** after epochs 1 and 2; distinct-4 unchanged
(0.74). A modest, well-leashed move. It lies *below* best-of-n at the same KL (best-of-2
is 0.73 at ≤ 0.19 nats): offline DPO only sees pairs from `π_ref`, mostly with small
reward gaps. Exercises: more epochs, larger `β`, on-policy (iterative) DPO with fresh pairs
from the current policy.

## 10. GRPO (Phase 11.1)

Change §7 in two places: sample `G = 8` completions for each of 4 prompts (still 32 per
step), and normalize advantages **within each group**:

```python
r = r.view(4, 8); A = ((r - r.mean(1, keepdim=True)) / (r.std(1, keepdim=True) + 1e-6)).view(-1)
```

and move the leash from the reward into the loss (DeepSeekMath's `k3` estimator per
token, `exp(ref − pol) − (ref − pol) − 1`, which is ≥ 0), or drop it (`β = 0`, DAPO-style)
and watch what happens. *(Not separately smoke-tested; it is a two-line change to the
tested §7 loop.)*

## 11. Toolformer's filter (Phase 8.4)

A "search" tool: given the first 12 characters of the current line, return the
training-region line that contains them (first match, else nothing). For a val position
`i` at a line start, compare the loss on the next line with and without
`"[S: " + result + "]\n"` inserted before it (`L⁺`), and with the call but an empty
result (`L⁻` is the min of no-call and empty-call). Keep positions with
`L⁻ − L⁺ ≥ τ_f` (Toolformer's ablations try `τ_f` = 0.5, 1 and 2 in its own weighted-loss
units; pick yours from the histogram). *Not yet smoke-tested — build it with the learner.*

## 12. Double descent in 20 lines (Phase 9.4)

Random ReLU features, minimum-norm least squares (`pinv`), `n = 40` noisy samples of a
sine; sweep the feature count `N` through `n`.

```python
import numpy as np
n, Ns = 40, (10, 20, 30, 40, 50, 100, 400, 4000)
def test_mse(N, noise, lam=0.0, seeds=50):
    e = []
    for seed in range(seeds):
        rng = np.random.default_rng(seed)
        x = rng.uniform(-1, 1, n); y = np.sin(2*np.pi*x) + noise*rng.standard_normal(n)
        xt = np.linspace(-1, 1, 400); yt = np.sin(2*np.pi*xt)
        c, s = rng.uniform(-1, 1, N), rng.choice([-1.0, 1.0], N)
        Phi = lambda x: np.maximum(0, s * (x[:, None] - c)) / np.sqrt(N)
        A = Phi(x)
        w = np.linalg.pinv(A) @ y if lam == 0 else np.linalg.solve(A.T @ A + lam*np.eye(N), A.T @ y)
        e.append(np.mean((Phi(xt) @ w - yt)**2))
    return float(np.median(e))
```

*(measured, median of 50 seeds)*

| N | 10 | 20 | 30 | 40 | 50 | 100 | 400 | 4000 |
|---|---|---|---|---|---|---|---|---|
| noise 0.2, `pinv` | 0.11 | 0.20 | 0.74 | 2.58 | **2.98** | 2.60 | 1.06 | 0.96 |
| noise 0, `pinv` | 0.10 | 0.04 | 0.02 | 0.008 | 0.004 | 0.001 | 0.000 | 0.000 |
| noise 0.2, ridge `λ = 1e-3` | 0.12 | 0.06 | 0.04 | 0.04 | 0.04 | 0.03 | 0.03 | 0.03 |

Read it honestly: the **peak at the interpolation threshold** (`N ≈ n`) and the **second
descent** are there; **label noise makes the peak** (none without noise); a little
**ridge removes it**. In this toy the second descent does *not* get back below the
classical sweet spot (`N = 10`) — whether it does depends on the problem (in Belkin et
al.'s experiments it does). DSP reading: at `N = n` the system is square and
ill-conditioned; the pseudoinverse amplifies noise along tiny singular values.
