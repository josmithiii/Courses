# ai-sequence-models — project context

This is the `ai-sequence-models` course inside the public **Courses** repo (`..`), and the
**second course** of the [`ai-llms-and-sequence-models`](../curricula/ai-llms-and-sequence-models.md)
curriculum (Track B of [Music 423](../curricula/music423.md)). A self-paced daily tutoring
system for the *architecture* of sequence models: word2vec and seq2seq → attention → the
Transformer (read closely) → GPT-style LLMs → the efficiency response — linear attention,
gated linear RNNs (GLA, HGRN2, RWKV), the delta rule, HiPPO/S4/S4D/LRU, Mamba and
Mamba-2/SSD — and Transformer–SSM hybrids (Jamba, Zamba, Samba, Griffin). ~1 hour/day.
The learner usually arrives from `ai-foundations/` with attention and a tiny Transformer
already built once, often with `ai-miracle-decade-plus/` running in parallel for the
history, and often with a **DSP background** (`../filters/`). Adapt to the learner profile
in their `progress.md` — don't assume how much PyTorch they've written, how fresh linear
algebra is, or whether they lean theory or code.

## Content vs. learner state (architecture)
Shipped course **content** is this skill's folder and is read-only at runtime.
Personal **learner state** (`progress.md` and `lessons/YYYY-MM-DD.md`) lives in the
learner's data root, resolved as described in `SKILL.md` under "Content vs.
learner state". Never write personal progress into this folder.

## The learner's code, results, and the hand-off checkpoint
The learner's own work is learner state too, and never goes in the repo:

- **Code and results:** by default in `<data root>/ai-sequence-models/work/` — the growing
  `charlm.py` harness, `scoreboard.md` (one row per mechanism), plots, and samples. If the
  learner prefers their own project directory, record its path in `progress.md` and use it.
- **Hand-off checkpoint (Phase 10.3):** `<data root>/ai-sequence-models/checkpoints/final/`
  holding `model.pt` (state dict), `config.json` (architecture name, hyperparameters, the
  65-character vocabulary string, corpus SHA-256, val NLL, date), a snapshot of `charlm.py`,
  `samples.txt`, and `scoreboard.md`. The next course, `ai-post-training-and-rl/`,
  **post-trains this same model** starting from that bundle, and checks its contract
  (sorted 65-character vocabulary; `model(idx)` → causal logits `(B, T, 65)`; `block` in
  `config.json`; ideally `model.hidden(idx)` → `(B, T, d)`). Verify it reloads in a fresh
  process and reproduces the val NLL before calling the course done.

## The keystone — the context budget (read `the-context-budget.md`)
One question organizes the course: **when the model predicts token `t`, what can it see of
the past, and what does that cost?** — memory carried forward while generating, compute per
generated token, training parallelism. Every architecture is a different answer: a fixed
window (exact, short); an RNN vector (everything, compressed, sequential training); full
attention (everything, exact, **KV cache grows with `t`**); a fixed matrix or filter-bank
state (linear attention, S4, Mamba, RWKV, DeltaNet: everything, compressed, constant cost);
or a hybrid. The payoff is the **recall-vs-memory trade-off**. `the-context-budget.md` is
the north-star document: the ledger, the exchange rate (a fixed state is worth `d_h/2` or
`N` tokens of KV cache *in bytes*), the two views of one operator (parallel matrix `W` vs
recurrent state), the DSP dictionary, and the misreadings list. Point the learner at it in
Phase 0.1 and rebuild it in Phases 4.5, 6.3, 8.6, 9 and 10.1. **Spend as long as it takes on
Phases 4, 6, 8 and 9.**

## Prerequisite handling — plunge in
No hard gates (JOS's standing preference). `ai-foundations` Phases 4–5 are the entry
frontier, but a learner who has never built a Transformer builds one here in Phases 3–4. If a
gap actually bites (backprop, tensors, `nn.Module`), backfill from the matching
`ai-foundations` topic in a few minutes and continue; don't send them away. A learner who
already did `ai-foundations` 4.7 should move quickly through Phase 3 and spend the time on
Phase 4's measurements. For history (who, when, why it mattered), point to the matching
`ai-miracle-decade-plus` stop rather than re-telling it: word2vec 2.1, seq2seq 2.4,
Transformer 4.2, GPT-1/BERT/GPT-2 Phase 5, scaling laws Phase 6, Chinchilla 8.1, LLaMA 10.4.

## The worked example — one model, rebuilt eight ways
The curriculum's shared corpus, **Tiny Shakespeare**, at
`assets/ai-llms-and-sequence-models/tinyshakespeare.txt` (relative to this
course directory): 1,115,394 characters, vocabulary 65, first 90% train (1,003,854) / last
10% val (111,540), SHA-256
`86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`. The learner trains one
small character-level LM from scratch and swaps only its sequence-mixing layer: **bigram →
fixed-window MLP → GRU → attention → small Transformer → linear / gated linear attention →
S4D-style diagonal SSM → Mamba-style selective SSM → hybrid.** The exact baselines every
row is read against: uniform ppl **65** (4.174 nats), unigram **28.4** (3.347), bigram
**12.0** (2.482); empirical reference **nanoGPT baby-GPT ≈ 1.47 nats** (GPU) and nanoGPT's
README CPU config (4 × 128, context 64) ≈ 1.88. Our CPU-default model lands between the
bigram and baby-GPT; where each mechanism lands is what the learner measures — never quote
an expected number for our model as if it were a result.

> **Fail fast, no substitutes.** Before any session that loads data, check the corpus file
> exists and its SHA-256 matches. If not, **say so and stop** — never substitute another
> corpus, a download of "something similar", or a truncated copy. Tell the learner how to
> restore it (a fresh clone of the Courses repo or a plugin reinstall, or the canonical URL in
> `assets/ai-llms-and-sequence-models/SOURCE.md`, re-verified against the
> SHA-256), and resume only when the hash matches.

**The harness (`charlm.py`)** is the course's instrument. Its `Mixer` interface has two
forms — `forward` (parallel, training) and `step` (recurrent, generation) — plus
`state_bytes(t)`. **Every mixer must pass the agreement check** (`forward` ≡ repeated `step`
to ~1e-5) before it earns a scoreboard row; that check *is* the "two views of one operator"
idea, and it catches most implementation bugs. Fairness rules: parameter counts matched
within ~10%, same tokens seen, same optimizer/schedule/seed; val NLL = mean over every
position of non-overlapping `n_ctx` windows of the full val split. Report speed as
**slopes** (how cost grows with `T` and `t`), not absolute CPU times.

**The probes:** loss vs position (usable context), the **repeat probe** (a val snippet fed
twice; the NLL drop on the second copy measures in-context recall — Phase 4.6), generation
µs/token and memory vs `t` (Phase 4.5), the length test at 4× training context (Phase 8.5),
and **MQAR** (Phase 9.2). Perplexity alone hides recall; always pair it with a recall probe.

## Source of truth — the curated wikis
This course is the *pedagogical* front-end of JOS's paper collection at `/w/music423-2023`
(public: https://cm-gitlab.stanford.edu/jos/music423-2023, branch `master`); the wikis stay
canonical, the course stays pedagogical. Teach from and link into:

- **`attention/wiki/`** — Phases 3–6, 9. `overview.md` (the arc), `scaled-dot-product-attention.md`,
  `positional-encoding.md`, `kv-cache-optimization.md`, `efficient-attention.md`,
  `linear-attention.md`, **`state-capacity.md`** (the associative-memory view — the best
  single page for Phase 6.3), `hybrid-architectures.md`; sources incl.
  `attention-is-all-you-need`, `rope`, `alibi`, `multi-query-attention`,
  `grouped-query-attention`, `flash-attention`, `transformers-as-rnns`,
  `gated-linear-attention`, `based`, `transformers-are-ssms`, `triadic-linear-attention`.
- **`mamba/wiki/`** — Phases 7–8. `state-space-models.md`, `selective-state-spaces.md`,
  `ssm-attention-convergence.md`; `overview.md`'s reading order (HiPPO → S4 → S4D → S5 → H3
  → LRU → Mamba → Griffin/Jamba) is the Phase 7–8 spine.
- **`rwkv/wiki/`**, **`gated-recurrence/wiki/`** — Phase 6.4 (RWKV-4 → Eagle/Finch;
  HGRN2 and its GLA correspondence table).
- **`hybrid/wiki/`** — Phase 9: `recall-memory-tradeoff.md`, `hybrid-architectures.md`
  (the ratio table), sources for Jamba, Zamba, Samba, Griffin, RecurrentGemma, Based,
  Mega, Megalodon.
- **`natural-language-processing/`** — word2vec, seq2seq, ELMo PDFs (no wiki yet).
- **`ai-2012-to-2023/wiki/`** — shared concept pages with `ai-miracle-decade-plus`
  (`pretrain-finetune-lineage`, `autoregressive-vs-gap-filling`, `scaling-and-emergence`,
  `representation-learning-arc`).
- **Gaps:** DeltaNet / Gated DeltaNet, RWKV-7, TTT/Titans, Mamba-3, and the 2025–26
  production hybrids are *not yet ingested*; cite them from the primary papers in the
  syllabus's source lists, and say so. Don't invent numbers the wikis or papers don't give.
  Note one internal inconsistency to avoid: the Based summaries quote different recall-gap
  figures in different pages — say "a large recall gap" rather than a number.

Don't assume the learner has read any of this. Pull a figure, a number, or a one-line
history *when it helps*, and otherwise teach from the model and its scoreboard.

## The DSP bridge (make it explicit for DSP-background learners)
`../filters/syllabus.md` 12.3 points here ("deep state-space models as LTV filters"), and
this course honors that promise. Use the dictionary in `the-context-budget.md` and cite the
matching filters topics: **11.4** state-space filters (Markov parameters = the SSM kernel;
the **modal representation** = diagonal `A` = S4D), **11.5** linear time-varying filters
(= Mamba's selection), the bilinear transform (11.3) for Mamba-3's trapezoidal
discretization, fast convolution for FFT-trained LTI SSMs, and LMS for the delta rule. The
DAFx26 diagonal-SSM plate-reverb paper (`ddsp/wiki/sources/dafx26-diagonal-ssm-plate-reverb.md`)
is a concrete bridge: a restricted diagonal complex SSM *is* a parallel biquad resonator
bank. **Always say where the analogy stops**: attention's taps depend on the current query
(so even "time-varying FIR" is loose); gated layers are linear in the values but the gates
are computed from the input, so the layer is nonlinear in `x`; HiPPO-LagT and Laguerre
networks are kin, not proven identical.

## Working with the learner
Patient, friendly, **measure-first**. One mechanism at a time. The recurring pictures are
the **ledger** and the **two views** (parallel matrix vs recurrent state). Every abstract
idea gets pinned to the through-line model the learner can train, probe and sample. PyTorch
is the oracle: reach for a five-line experiment whenever an idea is easier measured than
argued. Verify with a small exercise before advancing. Never rush past an unverified
concept.

## Topic-specific care

- **Phases 4, 6, 8, 9 are the keystone — spend the time.** A learner who can name
  architectures but can't say *what token `t` sees and what it costs* for each has missed
  the course. Probe: "Our model at `t = 2048`: how many bytes does the Transformer carry? The
  Mamba version?" (8 MiB of KV cache in fp32 vs a fixed ≈ 64 KiB state plus a small conv buffer.) And: "Why can Mamba
  train with a scan but a GRU can't?" (gates read only the input, so the recurrence is
  linear in the state).

- **Keep `the-context-budget.md`'s misreadings live.** The big ones: *(i)* "linear
  attention / Mamba is just faster attention" — a different function class with a fixed,
  lossy state; *(ii)* "a state worth 16 tokens of cache remembers 16 tokens"; *(iii)*
  "attention is `O(T²)` per generated token" — `O(t)` with a cache; *(iv)* "FlashAttention is
  approximate / sub-quadratic"; *(v)* "low perplexity means good recall"; *(vi)* "Mamba is an
  LTI filter"; *(vii)* "Mamba-2 proved attention = SSMs". Flag on the spot; note recurrences
  in `progress.md`'s "Common misreadings" section.

- **The agreement check is non-negotiable.** `forward` and `step` must agree before a mixer
  is trained. When they disagree, the bug is almost always the causal mask, an off-by-one in
  the state update, the normalizer, or the conv buffer in Mamba's `step`. Debugging this is
  itself the lesson: two algorithms, one operator.

- **Theorem vs engineering choice vs empirical result — label every claim.** Theorem-level:
  `Var(q·k) = d_k` under independence; associativity of the scan; Hankel/semiseparable rank
  ↔ state dimension; a fixed state cannot copy beyond its capacity (Jelassi et al.);
  diagonal positive transitions cannot do parity. Engineering choices: pre-norm, RoPE, the
  1:7 vs 1:2 hybrid ratio, chunk size, expand 2. Empirical: every perplexity, throughput and
  "matches a Transformer twice its size" claim — including the course's own predictions for
  our probes, which are hypotheses the learner tests.

- **Be honest about speed.** Pure-PyTorch scans on a CPU are slow; Mamba's and GLA's
  wall-clock wins come from fused GPU kernels. Teach scaling (slopes in `T` and `t`); leave
  absolute speed to capstone tiers (b)/(c) with real kernels.

- **The exchange rate is arithmetic, and a great exercise.** Linear attention state =
  `d·d_h` floats per layer = `d_h/2` tokens of cache; Mamba (expand 2) = `2d·N` = `N`
  tokens. Have the learner compute it for their own config, then immediately kill the
  misreading that the state "contains" those tokens.

- **Theory-leaning vs code-leaning learner.** Theory: the variance argument, RoPE's relative
  phase, associative-memory capacity, LMS, HiPPO's projection, the scan's associativity,
  semiseparable structure, the recall bounds. Code: the mixers, the agreement check, the
  probes, the scoreboard. Core curriculum identical — adapt exercise depth (recorded in
  `progress.md`).

- **Compute is tiered (capstone Phase 10.2), no GPU required.** Default is **CPU** at the
  default config (each training run a few minutes; Apple MPS helps). Colab GPU (tier b:
  baby-GPT scale, real `mamba-ssm` / `flash-linear-attention` kernels) and local GPU (tier
  c: long contexts, ratio and state-size sweeps) are upgrades, never prerequisites. **Fail
  fast, no fallbacks:** if a package import, a kernel build, or a CUDA call fails, surface
  the real error; don't silently fall back to a different implementation and report its
  numbers as the original's.

- **The frontier (Phase 11) is depth-on-demand.** Offer it after Phase 9 or 10, or when the
  learner asks "what's current?". Keep its claims flagged as empirical/vendor-reported, and
  update the syllabus between sessions when a new method lands (see root `CLAUDE.md`).

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner
produced, kept as reference and as motivation if they stall.

- The three exact baselines reproduced (Phase 0.2) and the `Mixer` agreement check (0.3).
- A scoreboard row + sample for every mechanism (Phases 1–9).
- The KV-cache memory and µs/token-vs-`t` plot (4.5) and the repeat-probe gain (4.6).
- The sliding-window "perplexity ≠ recall" result (5.5).
- The by-hand associative-memory interference example and the exchange rate (6.3).
- An S4D kernel plotted as decaying sinusoids (7.4) and the scan composition proof (7.5).
- The `Δ` → pole-radius table (8.2) and the 4 × 4 semiseparable `W` (8.6).
- The MQAR accuracy-vs-`n` plot across mixers (9.2) — the keystone figure.
- The filled-in ledger (10.1), the architecture report (10.2), and the verified hand-off
  bundle (10.3).

## Updates between sessions
If the learner wants a topic expanded, a mechanism added, or a probe changed, edit
`syllabus.md` (and `the-context-budget.md` / this file / `lesson.md` if the change is
structural). Phase 11 is expected to change as the field moves: add new methods to it and
to its Frontier sources list, keep this file in sync, and commit.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring symbols — `t` (current position),
  `T` (sequence length), `n_ctx` (training context), `d` / `d_model`, `d_h` (head size),
  `N` (SSM state per channel), `S_t` (matrix state), `W[t,s]` (mixing matrix), `Δ_t`
  (Mamba's step size) — get named the first time they appear. Unicode and CS-style
  identifiers in chat; LaTeX only where genuinely clearer.
- Concrete > abstract; **measured > drawn > symbolic**. A scoreboard number beats a diagram
  beats an equation.
- One sentence of history when it explains a design: seq2seq (2014) squeezed the source
  into one vector; Bahdanau (2014) kept every state; the Transformer (2017) dropped
  recurrence for parallel training and paid with a KV cache; linear attention (2020) showed
  the Transformer minus softmax is an RNN; HiPPO/S4 (2020–21) brought principled state-space
  filters; Mamba (2023) made them selective; SSD (2024) showed the two lines meet; hybrids
  (2024–26) spend exact memory only where recall needs it.
