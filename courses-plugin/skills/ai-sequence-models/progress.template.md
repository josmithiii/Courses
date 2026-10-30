# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Did `ai-foundations/` Phases 4–5 (attention, Transformer, the 4.7 char-Transformer)? _(yes, solid / partly / no — build it here in Phases 3–4)_
- Running `ai-miracle-decade-plus/` in parallel? _(yes — cross-reference its stops / no)_
- DSP background (state space, z-transforms, FIR/IIR, LMS)? _(strong — use the DSP dictionary heavily / some / none — skip the filter asides)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- Linear algebra comfort (outer products, eigenvalues, low rank): _(rusty / comfortable / strong)_
- Lean: _(code — implement and measure every mixer / theory — derivations, bounds, dualities / both)_
- Why they're here / goal: _(read the Mamba/RWKV/hybrid papers / build small LMs / understand LLM inference cost / research)_
- Hardware: _(CPU only / Apple MPS / Colab GPU / local NVIDIA GPU)_ — affects capstone tier a/b/c
- Where their code lives: _(default `<data root>/ai-sequence-models/work/`, or their own path)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **measure-first**, every term defined on first use, every
  mechanism built into the one through-line model and measured before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-context-budget.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] uv environment `.venv` with `torch`, `numpy`, `matplotlib` importable; device noted (CPU / MPS / CUDA)
- [ ] Corpus resolves at `assets/ai-llms-and-sequence-models/tinyshakespeare.txt` **and its SHA-256 matches** `86c4e6aa…565ed`
- [ ] The three exact baselines reproduced (4.174 / 3.347 / 2.482 nats)
- [ ] `charlm.py` harness runs; the `forward` ≡ `step` agreement check passes for the bigram
- [ ] `the-context-budget.md` read (the keystone — the ledger, the exchange rate, the misreadings)
- [ ] (capstone tier b/c) `mamba-ssm` and/or `flash-linear-attention` import on a CUDA GPU

## The numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Corpus: 1,115,394 chars, vocab 65; train 1,003,854 / val 111,540 (first 90% / last 10%).
- Exact baselines (val, nats/char → ppl): uniform 4.174 → 65; unigram 3.347 → 28.4; bigram 2.482 → 12.0.
- Empirical references: nanoGPT CPU config (4 × 128, ctx 64) ≈ 1.88; baby-GPT (6 × 384, ctx 256, GPU) ≈ 1.47 (ppl ≈ 4.4).
- Default config: `d_model` 128, 4 layers, `n_ctx` 128, batch 32, ~3000 steps (≈ 12M chars), seed _( )_.
- KV cache, our Transformer (fp32): 2 · 4 · 128 floats = 4 KiB per token → 8 MiB at `t` = 2048.
- Exchange rate: linear attention state = `d_h/2` tokens of cache (16 at `d_h` = 32); Mamba (expand 2) = `N` tokens (16 at `N` = 16).

## The scoreboard (the through-line results)
> One row per mechanism, same budget. Speeds as slopes; note the device.

| Mechanism | Params | Val NLL | Ppl | Repeat-probe gain | Train tok/s (slope in T) | Gen µs/token @ t=128 / 2048 | Memory @ t=2048 | Sample (1 line) |
|-----------|--------|---------|-----|-------------------|--------------------------|-----------------------------|-----------------|-----------------|
| bigram | | | | | | | | |
| fixed window (k=8) | | | | | | | | |
| GRU | | | | | | | | |
| attention-only (1 layer) | | | | | | | | |
| Transformer | | | | | | | | |
| linear / gated linear attn | | | | | | | | |
| S4D-style SSM | | | | | | | | |
| Mamba-style SSM | | | | | | | | |
| hybrid | | | | | | | | |

MQAR (Phase 9.2): accuracy vs number of pairs `n` per mixer — _(plot path)_

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has produced themselves, kept as reference. Add a one-line
> entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-context-budget.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "Linear attention / Mamba is just faster attention" — a different function class; fixed, lossy state
- "A state worth 16 tokens of KV cache remembers the last 16 tokens" — a lossy summary of the whole past
- "Attention is O(T²) per generated token" — O(t) with a KV cache; O(T²) is the sequence/training total
- "Transformers have unlimited context" — exact only within n_ctx; extrapolation depends on position encoding
- "FlashAttention is approximate / sub-quadratic" — exact, still O(T²) FLOPs; saves memory traffic
- "Low perplexity means good recall" — pair val NLL with the repeat probe and MQAR
- "Mamba is S4 with extra steps" — S4 is LTI (a convolution); Mamba is selective = LTV (a scan)
- "Gates make the recurrence nonlinear in the state" — only if they read the state (GRU), not Mamba/GLA
- "Mamba-2 proved attention and SSMs are the same" — a specific class coincides; softmax is not in it
- "Hybrids are worse at both" — they match or beat pure models in reported studies; the ratio is open
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 10.2) — tiered, no GPU required
> Picked partway through Phase 8 so it can shape the last few lessons.

- _(a) **CPU** — full scoreboard for all eight mechanisms at the default size, MQAR plot, generation-cost and memory plots, one-page architecture report_
- _(b) **Colab GPU** — tier a, plus baby-GPT-scale Transformer (≈ 1.47 target) and real `mamba-ssm` / `flash-linear-attention` kernels; throughput crossover vs FlashAttention as T grows_
- _(c) **Local GPU** — tier a, plus long contexts (1024–4096), a hybrid-ratio sweep and a state-size sweep_
- Choice: _(not yet)_

## Hand-off checkpoint (Phase 10.3) — for `ai-post-training-and-rl`
- Model handed on: _(not yet — default: best val NLL of Transformer / hybrid)_; why: _( )_
- Bundle path: `<data root>/ai-sequence-models/checkpoints/final/` (`model.pt`, `config.json`, `charlm.py`, `samples.txt`, `scoreboard.md`)
- Reload check in a fresh process reproduces val NLL to 1e-4: _(not yet)_
