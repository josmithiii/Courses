# AI Sequence Models — What a Token Can See, and at What Cost

**Learner profile:** Arrives from `ai-foundations/` (or equivalent) with an MLP, backprop,
PyTorch, and a first pass at attention and the Transformer (its Phases 4–5, including the
4.7 mini-project: a tiny character-level Transformer). May be running
`ai-miracle-decade-plus/` in parallel for the history. Many learners here have a **DSP
background** (`../filters/`, `../pasp/`): state space, z-transforms, IIR vs FIR, convolution
vs recursion — this course uses that vocabulary on purpose. So: intuition first, one
mechanism at a time, every mechanism built and measured on the same tiny model before
moving on. ~1 hour per day.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisites — plunge in.** `ai-foundations` Phases 4–5 are the entry frontier, but
nothing here is gated. A learner who has never built a Transformer can start at Phase 0 and
will build one from scratch in Phases 3–4; the tutor backfills (an `ai-foundations` topic,
a `filters` chapter) when a gap actually bites, not before. A learner who did
`ai-foundations` 4.7 moves fast through Phase 3 and spends the time in Phase 4's
measurements instead. `ai-miracle-decade-plus` is the *history* companion: this course
cross-references its stops (word2vec, seq2seq, the Transformer, GPT, scaling) rather than
re-telling them.

**The keystone — read [`the-context-budget.md`](the-context-budget.md) in Phase 0.1.** One
question organizes the whole field: ***when the model predicts token `t`, what can it see of
the past, and what does that cost?*** — in memory carried forward while generating, compute
per generated token, and training parallelism. Every architecture is a different answer:
a fixed window (exact, short), a recurrent vector (everything, compressed), full attention
(everything, exact, with a **KV cache that grows**), a fixed matrix or filter-bank state
(linear attention, S4, Mamba, RWKV, DeltaNet — everything, compressed, constant cost), or a
hybrid. The **recall-vs-memory trade-off** is the payoff. We spend as long as it takes on
Phases 4, 6, 8 and 9.

**The worked example — one model, rebuilt eight ways.** The curriculum's shared corpus,
**Tiny Shakespeare** (`assets/ai-llms-and-sequence-models/tinyshakespeare.txt`:
1,115,394 characters, vocabulary **65**, first 90% train / last 10% validation, SHA-256
`86c4e6aa…565ed`; see that directory's `README.md`). The learner trains **one small
character-level language model from scratch** and re-implements its sequence-mixing layer
with each mechanism: **bigram → fixed-window MLP → GRU → attention → small Transformer →
linear / gated linear attention → diagonal SSM (S4D-style) → selective SSM (Mamba-style) →
hybrid.** Everything else (embedding, MLP, norm, optimizer, data, budget) stays fixed, so
the **scoreboard** isolates the mechanism: validation perplexity, usable context, and speed
(training throughput; generation cost per token and memory growth with `t`). The exact
baselines every row is read against: **uniform ppl 65** (ln 65 = 4.174 nats/char),
**unigram 28.4** (3.347), **bigram 12.0** (2.482); and the empirical reference point
**nanoGPT "baby GPT" ≈ 1.47 nats** (≈ 4.4 ppl; 6 layers × 384, context 256, GPU minutes). A
CPU-sized model lands between the bigram and that line — where each mechanism lands is what
the learner measures.

> **Fail fast:** if the corpus file is missing or its SHA-256 is not
> `86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`, the tutor says so and
> stops. Never substitute another corpus.

**The hand-off.** The next course, `ai-post-training-and-rl/`, **post-trains this same
model** (supervised fine-tuning, a reward model, RLHF-style and DPO-style preference
tuning). This course ends (Phase 10.3) by saving a reloadable checkpoint bundle for it.

**End state:** by the last lesson the learner can: state, for any architecture, what token
`t` can see and what it costs (memory at step `t`, compute per token, training
parallelism); compute perplexity and read it against the exact baselines; explain why
nonlinear RNNs lost on training parallelism and how linear recurrences got it back (the
scan); read the Transformer paper closely and implement its decoder with a **KV cache**,
verifying that the parallel and step-by-step forms agree; explain GQA, FlashAttention and
sliding windows as cheaper *exact* attention; derive linear attention's RNN form and read
its state as an associative memory with finite capacity; explain the delta rule as LMS;
explain HiPPO → S4 → S4D → LRU as **state-space filters** (modal representation, stability
by parameterization, FFT convolution vs scan); explain Mamba's selection as an **LTV
filter** and Mamba-2/SSD as one operator with two algorithms; state the recall-vs-memory
trade-off in its theorem, empirical and engineering registers and measure it with MQAR;
design and justify a hybrid; and hand a trained checkpoint to the post-training course.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture.** One question (what can token `t` see, at
  what cost?), one corpus, one model rebuilt eight ways, one scoreboard. Read
  [`the-context-budget.md`](the-context-budget.md). Where it sits: `ai-foundations`
  introduced attention and the Transformer; `ai-miracle-decade-plus` tells the history;
  this course takes the mechanism apart and rebuilds it with each successor; the next
  course post-trains the result.
- **0.2** **Tools and the corpus.** A uv environment (`.venv`) with `torch` (CPU is enough;
  Apple MPS or CUDA optional), `numpy`, `matplotlib`. Load the corpus, **verify its
  SHA-256** (fail fast), build the vocabulary (`sorted(set(text))` → 65 characters), encode,
  and split at `int(0.9 · 1,115,394)` = **1,003,854** train / **111,540** val characters.
  **Exercise:** compute the three exact baselines yourself — uniform 4.174 nats (ppl 65),
  add-one unigram 3.347 (28.4), add-one bigram 2.482 (12.0) — and match them to three
  decimals. This is the harness's first test.
- **0.3** **The harness and the scoreboard.** One file, `charlm.py`, that grows all course.
  A **`Mixer`** interface with *two* forms: `forward(x[B,T,d]) → y[B,T,d]` (parallel, for
  training) and `step(x_t[B,d], state) → (y_t, state)` (recurrent, for generation), plus
  `state_bytes(t)` (memory carried at step `t`). A shared pre-norm residual block
  (`x + mixer(norm(x))`, `x + mlp(norm(x))`), one training loop, one evaluator, one
  sampler, and the probes: **loss vs position** (usable context), the **repeat probe**
  (Phase 4.6), **generation cost vs `t`**, and **MQAR** (Phase 9.2). Default CPU config:
  `d_model = 128`, 4 layers, `n_ctx = 128`, batch 32, ~3000 AdamW steps (≈12M training
  characters), fixed seed. **Fairness rules:** parameter counts matched within ~10%, the
  same tokens seen, the same optimizer and schedule; val NLL is the mean over every
  position of non-overlapping `n_ctx` windows of the whole val split. Speeds are reported
  as *slopes* (how cost grows with `T` and `t`), because absolute CPU timings measure the
  implementation more than the idea. **Exercise:** write the `Mixer` interface and a
  check that `forward` and repeated `step` give the same outputs (to ~1e-5) — every
  mechanism must pass it.

## Phase 1 — Prediction, Perplexity, and the Fixed Window
- **1.1** **A language model is a conditional distribution.** The chain rule
  `p(x_1 … x_T) = Π_t p(x_t | x_<t)`; generation = repeated sampling of the next character.
  Shannon's 1951 guessing game as the original version of the experiment we'll run eight
  times. Every architecture in the course is a different way to compute `p(x_t | x_<t)` —
  the keystone question is how much of `x_<t` it gets to use.
- **1.2** **Cross-entropy, bits, perplexity.** Mean negative log-likelihood in nats;
  bits/char = nats / ln 2; perplexity = `exp(NLL)`, the geometric-mean "effective number of
  choices" per character. **Exercise:** why is the uniform model's perplexity *exactly* 65?
  Say in plain words what baby-GPT's ≈ 4.4 means, and what the gap from the bigram's 12.0
  is worth in bits per character.
- **1.3** **The bigram as a learned table.** `nn.Embedding(65, 65)` read as logits, trained
  by gradient descent; it lands on the count bigram (val ≈ 2.48). First scoreboard row. Its
  keystone answer: it sees one character; memory `O(1)`.
- **1.4** **The fixed window (Bengio et al. 2003).** Concatenate the last `k` character
  embeddings, apply an MLP, predict. `k = 8` is a good first try (the val NLL is yours to
  measure). DSP view: an **FIR filter in token space** — exact memory of `k` taps, nothing
  beyond, and parameters grow with `k` because each slot has its own weights. Contrast with
  convolution's weight sharing; WaveNet's dilated causal convolutions are this idea scaled up
  (`audio-codec-lms` Phase 1). Scoreboard row.
- **1.5** **Reading samples.** Temperature and top-k; the **legibility ladder** — spelling →
  words → speaker names and line breaks → verse — as a qualitative probe of how much
  structure a model has. Log one sample with every scoreboard row from now on.

## Phase 2 — Embeddings and Recurrence: the Whole Past Through One Vector
- **2.1** **Embeddings and word2vec (Mikolov et al. 2013).** One-hot → dense vectors; the
  distributional hypothesis; skip-gram and CBOW; negative sampling (Mikolov et al. 2013b) as
  logistic regression on (word, context) pairs; skip-gram-with-negative-sampling as implicit
  factorization of a shifted PMI matrix (Levy & Goldberg 2014). **Exercise:** inspect the
  65 × `d` embedding table from 1.4 — nearest neighbors by cosine similarity (do vowels
  cluster? case pairs?). Optional: a skip-gram on Shakespeare *words* in a few CPU minutes.
  (History: `ai-miracle-decade-plus` 2.1.)
- **2.2** **The vanilla RNN.** `h_t = tanh(W h_{t−1} + U x_t + b)`: a nonlinear state-space
  system whose `d` floats carry the entire past. Backprop through time; vanishing and
  exploding gradients as a product of Jacobians. DSP view: linearize, and the eigenvalues of
  the Jacobian act as poles — `|λ| < 1` forgets exponentially with time constant
  `≈ −1/ln|λ|` steps, `|λ| > 1` explodes. **Exercise:** time constants for `|λ| = 0.9` and
  `0.99` (≈ 9.5 and ≈ 99.5 steps).
- **2.3** **Gating: LSTM and GRU.** GRU's `h_t = (1 − z_t) ⊙ h_{t−1} + z_t ⊙ h̃_t` is a
  **one-pole leaky integrator whose pole `(1 − z_t)` is chosen every step** — by the input
  *and* the state. Hold this thought: Mamba will keep the input-chosen pole and drop the
  dependence on the state (Phase 8.2), and that single change is what makes parallel
  training possible.
- **2.4** **Train a GRU on the corpus.** Truncated BPTT with the state carried across
  windows; matched parameters. Measure val NLL, train throughput (sequential in `T`!),
  generation cost (flat in `t`) and memory (`d` floats per layer). **Exercise:** time one
  training step at `T = 64, 128, 256` and explain the slope. Scoreboard row.
- **2.5** **Seq2seq and the bottleneck (Sutskever et al. 2014).** Encoder RNN → one vector
  → decoder RNN. The keystone stated for the first time: *the entire source squeezed
  through `d` floats*. The reversed-source trick as evidence — it shortens the path between
  related tokens. ELMo (2018) in one line: contextual embeddings from bidirectional LSTM
  LMs, the last major RNN-era result. (History: `ai-miracle-decade-plus` 2.4, 5.1.)

## Phase 3 — Attention: Look Back Instead of Remembering
- **3.1** **Additive attention (Bahdanau et al. 2014).** The decoder looks at *all* encoder
  states, weighted by a learned alignment; the alignment-matrix picture. The bottleneck is
  solved by **keeping every state** — the first appearance of memory that grows with the
  sequence.
- **3.2** **Attention as a soft dictionary lookup.** Query, keys, values; softmax as a
  differentiable argmax; dot-product vs additive scoring. **Exercise (by hand):** three keys,
  one query — compute the weights and the output; then sharpen the query and watch the
  lookup become hard.
- **3.3** **Why `√d_k`.** For keys and queries with independent zero-mean unit-variance
  components, `q·k` has variance `d_k` (a two-line derivation — a fact under that
  assumption); unscaled, the softmax saturates and its gradients vanish. **Exercise:** verify
  numerically with random vectors at `d_k = 4, 64, 1024`.
- **3.4** **Causal self-attention on the corpus.** The causal mask; all `T` positions trained
  in one matmul — *the* reason Transformers out-trained RNNs. Build a one-layer, single-head,
  attention-only model with no position information. **Exercise:** predict first — a single
  such layer sees its past as an unordered **set** (its output at `t` is invariant to
  permuting positions `1 … t−1`); then measure. (Deeper stacks can recover some position from
  prefix length — an empirical effect, not a guarantee.)
- **3.5** **Multi-head attention and the bill.** `h` heads of size `d_h = d/h`: several
  lookups in parallel, same total cost. The attention line of the ledger: training
  `O(T²·d)`; generation needs every past key and value — the KV cache, built next phase.

## Phase 4 — The Transformer, Read Closely (full attention's answer)
> Spend the time. This phase sets the reference every later mechanism is measured against.
- **4.1** **Read Vaswani et al. (2017), Section 3, slowly.** Encoder–decoder, then the
  decoder-only variant we use (the GPT line). Map every box in Figure 1 and every equation
  to a line of `charlm.py`. (`ai-miracle-decade-plus` 4.2 gives the context; here the reading
  is mechanical: reproduce each equation in code.)
- **4.2** **The block.** The residual stream as a **summing bus** every layer reads and
  writes; LayerNorm placement — the paper's post-LN vs modern pre-LN / RMSNorm (pre-LN
  trains more stably without warmup: Xiong et al. 2020, analysis plus experiment); the MLP
  as per-position compute (about two thirds of the parameters at 4× width); tied input and
  output embeddings. **Exercise:** count the parameters of our 4 × 128 model by hand
  (≈ 12·d² per layer) and check against `sum(p.numel())`.
- **4.3** **Position.** Sinusoidal (the paper), learned absolute (GPT-2), relative (Shaw et
  al. 2018), **RoPE** (rotate each pair of dimensions by `e^{iωp}`; the dot product then
  depends only on `p − q` — a relative *phase*, with geometrically spaced `ω` like a
  filterbank), **ALiBi** (a linear distance penalty: a recency prior). Length extrapolation
  is governed mostly by the position method (ALiBi's empirical result). **Exercise:** show
  by hand in 2-D that RoPE's `q·k` depends only on `p − q`. We use RoPE from here on.
- **4.4** **Build the small Transformer.** 4 layers, `d = 128`, 4 heads, `n_ctx = 128`,
  RoPE, pre-norm. Reference points (empirical, re-measure): nanoGPT's README CPU run
  (4 × 128, context 64, 2000 iterations, ~3 minutes on a laptop) reports val ≈ 1.88;
  baby-GPT on a GPU ≈ 1.47. Scoreboard row and sample.
- **4.5** **The KV cache, implemented and measured.** `step()` for attention: append
  `(k_t, v_t)` and attend over the cache. Check `step` ≡ `forward`. Then measure the
  keystone: cache memory = `2 · n_layer · d · t` floats — for our model 4 KiB per token in
  fp32, 8 MiB at `t = 2048` — and generation cost per token rising linearly with `t`. Plot
  µs/token vs `t` (positions past `n_ctx` are fine for *timing*; quality there is a separate
  question). **Exercise:** also time generation *without* the cache and explain why that
  curve bends upward.
- **4.6** **What the growing memory buys: recall.** Induction heads and in-context copying
  (Olsson et al. 2022). **The repeat probe:** take a val snippet of length `n_ctx/2`, feed
  it twice, compare NLL on the second copy with the first. A model that can look back and
  copy should drop sharply on the second copy (a prediction to check, not a given at this
  size). Record the **repeat-probe gain** (first-copy NLL minus second-copy NLL); every
  later mechanism is judged against this number.

## Phase 5 — GPT-Style LLMs and Cheaper Exact Attention
- **5.1** **The decoder-only lineage.** GPT-1 → GPT-2 → GPT-3: what changed (scale, data,
  context length) and what didn't (the block). In-context learning as recall paid off at
  scale. BERT as the bidirectional fork — no generation, no KV-cache story. Don't re-tell
  the history (`ai-miracle-decade-plus` Phases 5–6; the `pretrain-finetune-lineage` and
  `autoregressive-vs-gap-filling` concept pages); have the learner place our char model on
  that line.
- **5.2** **Tokenization changes the budget.** BPE (Sennrich et al. 2016) merges characters
  into ~4-character tokens in English: the same `n_ctx` covers ~4× more text and the cache
  per character is ~4× cheaper, at the price of a larger vocabulary. **Exercise:** how many
  characters do 128 BPE tokens cover? Why does this course stay character-level? (Legible
  samples, a 65-symbol vocabulary, exact baselines.)
- **5.3** **Scaling laws in one session.** Kaplan et al. (2020); Chinchilla (2022): roughly
  20 training tokens per parameter is compute-optimal. **Exercise:** our ~0.8M-parameter
  model at 20 tokens/parameter wants ~16M characters ≈ 16 passes over the training split;
  the default budget is ~12M. Caveat: the law was fitted far above our scale and on
  non-repeated data (empirical).
- **5.4** **The modern recipe and the KV-cache diet.** LLaMA's RMSNorm, SwiGLU, RoPE, no
  biases; **MQA** (one KV head) and **GQA** (groups of query heads share K, V).
  **Exercise:** KV bytes per token for our model under MHA, GQA-2 and MQA; implement GQA (a
  few lines) and re-measure val NLL and the cache.
- **5.5** **Exact attention, cheaper.** **FlashAttention**: IO-aware tiling, exact, `O(T)`
  memory, still `O(T²)` FLOPs — FLOPs ≠ wall clock (PyTorch's
  `scaled_dot_product_attention` is our stand-in). **Sliding-window attention** (Longformer;
  the local half of later hybrids): cache capped at `w`, recall capped at `w`. Ring
  attention (sequence split across devices), briefly. **Exercise:** give our model a window
  `w = 32`. Predict what happens to val NLL and to the repeat probe at snippet length 64; then
  measure. The expected surprise: NLL barely moves while the repeat-probe gain collapses —
  first sight of *perplexity ≠ recall*.

## Phase 6 — Linear Attention: the Transformer as an RNN (keystone)
- **6.1** **Drop the softmax (Katharopoulos et al. 2020).** Replace `exp(qᵀk)` with
  `φ(q)ᵀφ(k)`; associativity turns `(φ(Q)φ(K)ᵀ)V` into `φ(Q)(φ(K)ᵀV)`: `O(T²·d)` →
  `O(T·d·d_h)`. **Exercise:** verify the associativity numerically and count the FLOPs of
  each order at `T = 128` and `T = 8192`.
- **6.2** **The recurrent form.** `S_t = S_{t−1} + φ(k_t) v_tᵀ`, `o_t = S_tᵀ φ(q_t)` (plus a
  normalizer): a **matrix-valued state**, `O(1)` per generated token. Implement both forms
  and pass the agreement check. DSP view: an **integrator** — a pole at `z = 1`; nothing is
  ever forgotten and the state grows without bound, which is why normalizers, then decays,
  arrive.
- **6.3** **The state is an associative memory.** Correlation-matrix memory (Kohonen 1972),
  fast weights (Schmidhuber 1992; Schlag et al. 2021): write = outer product, read =
  matrix–vector product. Retrieval is exact only for orthogonal keys, so a `d_k × d_v`
  state separates at most **`d_k`** keys; beyond that, crosstalk grows gradually (unlike a
  window, which keeps the last `w` exactly and drops the rest). **Exercise (by hand):** in
  `d_k = 2`, store two pairs under orthogonal keys and retrieve them exactly; add a third and
  watch the interference. Then the **exchange rate**: the state is worth `d_h/2` tokens of KV
  cache — 16 for our model (arithmetic, not memory contents).
- **6.4** **Forgetting: decay and gates.** RetNet (a fixed decay `γ` per head: one-pole leaky
  integrators at several time scales); **GLA** (data-dependent decay `α_t`; reported to beat
  fixed decay clearly); **HGRN2** (the same computation from the gated-RNN side: state
  expanded from `d` to `d²/H` by outer products); **RWKV** — RWKV-4's channel-wise decay, then
  Eagle/Finch (RWKV-5/6): matrix states, data-dependent decay and token shift. Three lineages
  converge on one line, `S_t = diag(α_t) S_{t−1} + k_t v_tᵀ`. **Exercise:** map each
  paper's symbols onto that line (the HGRN2 ↔ GLA table in the gated-recurrence wiki is the
  model answer).
- **6.5** **The delta rule (DeltaNet).** Instead of adding, *edit*: with `S ∈ R^{d_k × d_v}`,
  `S_t = S_{t−1} + β_t k_t (v_t − S_{t−1}ᵀ k_t)ᵀ = (I − β_t k_t k_tᵀ) S_{t−1} + β_t k_t v_tᵀ`
  — one gradient step on `½‖Sᵀk_t − v_t‖²`. This is **LMS** (Widrow–Hoff 1960); unit-norm
  keys make it NLMS. The state is an adaptive filter's weight matrix, identified online from
  key→value pairs. **Gated DeltaNet** multiplies in a decay `α_t`. **Exercise:** write the
  same key twice with different values; show plain linear attention returns a blend while the
  delta rule returns the latest value.
- **6.6** **Chunkwise-parallel training, and the scoreboard.** Split `T` into chunks of
  length `C`: inside a chunk use the quadratic (attention-like) form; across chunks carry the
  state — **block processing**, cost `O(T·C·d + T·d·d_h)`. Implement linear attention, a
  gated variant (scalar or vector `α_t`), and optionally the delta rule (naive recurrence is
  fine at our size). Scoreboard rows: val NLL, repeat probe, flat generation cost, fixed
  memory. The prediction to test: perplexity not far from the Transformer's at this scale, a
  weaker repeat-probe gain.

## Phase 7 — State-Space Models: HiPPO → S4 → S4D → LRU (the filter phase)
> For DSP learners this is home turf: `../filters/` 11.4 (state-space filters, the modal
> representation) and 11.5 (linear time-varying filters). Lean on it; don't re-derive it.
- **7.1** **The SSM is a filter.** `x'(t) = A x + B u`, `y = C x + D u`; discretize (zero-order
  hold: `Ā = e^{ΔA}`, `B̄ = (ΔA)⁻¹(e^{ΔA} − I) ΔB`; or bilinear); three views — ODE,
  recurrence, and convolution with kernel `K = (C B̄, C Ā B̄, C Ā² B̄, …)`, which are the
  **Markov parameters** of filters 11.4. A deep SSM runs one small SSM per channel and mixes
  channels with ordinary layers between. Keystone answer: state `d·N`, fixed; `O(d·N)` per
  token; and because it is **LTI**, training can be one long convolution.
- **7.2** **HiPPO (Gu et al. 2020): memory as online function approximation.** Project the
  input history onto Legendre polynomials under a chosen measure; the coefficients obey a
  linear ODE with a closed-form `A`. LegT (a sliding window; recovers the Legendre Memory
  Unit), LegS (scaled: all of history), LagT (Laguerre: an exponential measure, which HiPPO
  relates to gating). DSP aside: classical Laguerre / Kautz networks also represent a
  signal's past in an orthonormal basis built from cascaded first-order sections — kin, not
  identical; check the papers before claiming more. **Exercise:** which measure does a
  one-pole lowpass (an EMA) implement?
- **7.3** **S4 (Gu et al. 2021).** HiPPO-LegS made computable: diagonal-plus-low-rank `A`,
  the Woodbury identity, a Cauchy-kernel evaluation — the first model to solve Long Range
  Arena's Path-X (length 16,384). Read for the idea, not the algebra. **SaShiMi** (2022): S4
  on raw audio, the audio-side proof of concept.
- **7.4** **Diagonal is enough: DSS → S4D.** DSS found it empirically; S4D explained it and
  reduced the kernel to two lines: `K_l = 2·Re Σ_n C_n B̄_n Ā_n^l` (a Vandermonde product). A
  diagonal `A` **is the modal representation**: a bank of parallel complex one-poles, i.e.
  real resonators in conjugate pairs. Inits: S4D-Lin `A_n = −½ + iπn`; S4D-Real
  `A_n = −(n+1)`. **Exercise:** for S4D-Lin with `Δ = 0.01`, pole radius `e^{−Δ/2} ≈ 0.995`
  (time constant ≈ 200 steps) and pole angle `πnΔ` rad/sample; plot the kernel — decaying
  sinusoids, a little modal reverb. Bridge: Bittner et al. (DAFx26, in the `ddsp` wiki) show
  a restricted diagonal complex SSM *is* a parallel bank of second-order resonators and fit
  plate-reverb impulse responses with it.
- **7.5** **LRU (Orvieto et al. 2023) and the scan.** Start from a vanilla RNN; linearize,
  diagonalize, parameterize `λ = exp(−exp(ν) + iθ)` — `|λ| < 1` always: **poles kept inside the
  unit circle by parameterization** — initialize on a thin ring near the unit circle,
  normalize. Deep SSMs turn out to be well-initialized linear RNNs. The **parallel scan**
  (Blelloch 1990; Martin & Cundy 2018): affine maps `h ↦ a h + b` compose associatively,
  `(a₂, b₂) ∘ (a₁, b₁) = (a₂a₁, a₂b₁ + b₂)`, so `T` steps take `O(log T)` depth.
  **Exercise:** prove the composition rule; implement a sequential loop and a log-depth scan
  and check they agree.
- **7.6** **Build the S4D-style mixer.** `forward` by **FFT convolution** (zero-pad to `2T`,
  multiply spectra — fast convolution, the DSP lesson), `step` by the recurrence; pass the
  agreement check. Scoreboard row. Then the probes: the keystone answer here is *"sees
  everything, through fixed filters — the same filter for `the` as for `ROMEO`"*, so predict
  the repeat-probe result before you run it (H3's diagnosis: LTI SSMs are weak at recall and
  comparison).

## Phase 8 — Selectivity: Mamba and Mamba-2/SSD (keystone)
- **8.1** **Why LTI can't select.** The **selective-copy** task (from the Mamba paper):
  copy a few tokens scattered at random positions among filler. A fixed kernel can copy at a
  fixed lag but cannot decide *by content* what to keep. **Exercise:** argue why an LTI
  filter solves the fixed-spacing copy task but not selective copy. H3's patch
  (multiplicative interactions) vs Mamba's answer.
- **8.2** **Selection = an input-steered LTV filter (Gu & Dao 2023).**
  `Δ_t = softplus(Linear(x_t))`, `B_t = Linear(x_t)`, `C_t = Linear(x_t)`;
  `Ā_t = exp(Δ_t A)`, `B̄_t ≈ Δ_t B_t`. The input steers the **pole radius**: large `Δ` →
  pole near 0 → reset and absorb this token; small `Δ` → pole near 1 → hold the state and
  ignore it. Back to 2.3: GRU's gate reads input *and* state; Mamba's reads only the input,
  so the recurrence stays **linear in the state** and can be scanned. **Exercise:** with
  `A = −1`, compute `Ā` for `Δ = 0.01, 1, 10` (≈ 0.990, 0.368, 4.5e-5) and say which token
  gets remembered.
- **8.3** **The price, and the engineering.** No fixed kernel → no FFT. Mamba's selective
  scan fuses discretization, scan and readout in one GPU kernel and keeps the expanded state
  in fast on-chip memory — the same IO-awareness as FlashAttention. State per layer
  `2d·N` (`N = 16` in Mamba-1): worth **`N` tokens** of KV cache. Reported results
  (empirical): ~5× generation throughput vs similar-size Transformers; Mamba-3B on par with
  Transformers twice its size. Honest note: our pure-PyTorch scan on a CPU is slow; compare
  how cost *scales* with `T` and `t`, not absolute times.
- **8.4** **The Mamba block.** In-projection with expand 2 into two branches; one branch:
  causal depthwise conv1d (kernel 4) → SiLU → selective SSM; the other: SiLU gate; multiply;
  out-projection. Mamba stacks only these blocks (no separate MLP). The short conv is a tiny
  **FIR in front of the IIR** — RWKV's token shift and Griffin's conv play the same role.
  Implement it; `step` carries (conv buffer, `h`).
- **8.5** **Train it.** Scoreboard row; repeat probe; and a **length test**: evaluate at 4×
  the training context, carrying the state. Does loss keep improving, plateau, or degrade?
  (The Mamba paper reports improvement with context on DNA and audio; for a tiny char model,
  measure.) Preview MQAR.
- **8.6** **Mamba-2 and SSD (Dao & Gu 2024): one operator, two algorithms.** Restrict `A_t`
  to a scalar per head; then `W[t,s] = (Π_{r=s+1..t} a_r) · C_tᵀ B_s` is a masked attention
  matrix with a **1-semiseparable** mask, and SSMs with state `N` correspond to
  `N`-semiseparable matrices. Compute it as a linear-time recurrence *or* a quadratic
  attention-like product — Mamba-2 uses block decompositions (chunkwise, as in 6.6) to run on
  tensor cores with larger `N`, reported 2–8× faster than Mamba-1. DSP payoff: semiseparable
  rank is the time-varying cousin of **Hankel rank** (a kernel has a finite-state realization
  iff its Hankel matrix has finite rank; Kronecker, Ho–Kalman). Softmax attention has no such
  structure in general — hence the KV cache. **Exercise:** write the 4 × 4 `W` for a
  one-state scalar-decay SSM and check every below-diagonal block has rank ≤ 1. Close with
  the unification table: linear attention (`A_t = I`), RetNet (`γI`), GLA (`diag α_t`),
  Mamba-2 (`a_t I`), RWKV-6, HGRN2, DeltaNet (`I − β kkᵀ`, *not* diagonal) — one recurrence
  `S_t = A_t S_{t−1} + k_t v_tᵀ`, different transitions.

## Phase 9 — Recall vs Memory, and the Hybrids (the keystone payoff)
- **9.1** **The trade-off in three registers.** *(i) Theorem-level:* a fixed state cannot
  return more than it can hold; Jelassi et al. (2024) prove that fixed-state models cannot
  copy strings longer than their state allows, while a 2-layer Transformer can. *(ii)
  Empirical:* Zoology (Arora et al. 2023) finds most of the perplexity gap between attention
  and gated convolutions/recurrences at small scale is associative recall; Based (2024) maps
  the recall–throughput Pareto frontier. *(iii) Engineering:* where to spend memory.
  **Exercise:** our Mamba state is 4 × 256 × 16 = 16,384 floats ≈ 524k bits; a 1000-character
  snippet is ≈ 6k bits raw. So raw bits are not the binding constraint at fp32 — what binds is
  what a *linear readout* can retrieve without interference (≈ `d_k` or `N` separable keys).
  Say why the information bound is loose and the operational bound is tight.
- **9.2** **The keystone experiment: MQAR on every mixer.** Multi-query associative recall:
  sequences of `n` key–value pairs, then queries; 2-layer models, `d = 64`, CPU minutes per
  run. Plot accuracy vs `n` (4 … 64) for attention, sliding window, linear attention, S4D,
  Mamba-style, (gated) delta rule, and the hybrid. Then double the state (`d_h` or `N`) and
  watch the curve move. The curves the papers predict are hypotheses; the learner's plot is
  the result.
- **9.3** **The hybrid design space.** *Global attention in a few layers:* Jamba (1
  attention : 7 Mamba, plus MoE; 256K context), Zamba (one *shared* attention block every 6
  Mamba blocks, input embeddings concatenated in). *Local attention:* Griffin / Hawk (RG-LRU
  + local MQA) and RecurrentGemma; Samba (Mamba–SWA–MLP; trained at 4K, perplexity reported
  to keep improving toward 1M and passkey retrieval at 256K). *Within one layer:* Based
  (linear attention + small window), Mega / Megalodon (EMA + gated attention). The ratio
  question — 1:7 (Jamba), about 1:6 (Zamba), 1:2 (Samba), 1:1 (Griffin), ~25% suggested by
  Poli et al. (2024) as cited in Zamba — is open and empirical.
- **9.4** **Build our hybrid.** For example 3 Mamba-style (or gated-delta) layers + 1 global
  attention layer: the KV cache lives in a quarter of the layers. Scoreboard row; MQAR;
  repeat probe; generation cost. **Exercise:** where should the attention layer go — first,
  middle, last? Predict, run two placements, compare (empirical).
- **9.5** **Two other places to spend memory.** Enlarge the *recurrent state* instead of
  the cache (triadic linear attention, Phase 11.6), or keep full attention and make its
  cache smaller or sparser (Phase 11.5). The keystone, closed: *every architecture is a
  choice of what to keep exactly, what to summarize, and what to forget.*

## Phase 10 — Putting It Together
- **10.1** **The map.** Fill the ledger in `the-context-budget.md` with the learner's own
  scoreboard. Place every mechanism on two axes: memory at step `t` (constant ↔ growing) ×
  how content-dependent the mixing is (none / gates / full). Reconstruct the keystone
  document from memory.
- **10.2** **Capstone — tiered, no GPU required.**
  - **(a) CPU (default).** The complete scoreboard at the default size for all eight
    mechanisms (bigram, fixed window, GRU, Transformer, linear / gated linear attention,
    S4D-style, Mamba-style, hybrid) — val NLL and perplexity, repeat-probe gain, train
    throughput slope, generation µs/token vs `t`, memory vs `t` — plus the MQAR plot and a
    one-page **architecture report** answering the keystone question for each row. Apple
    MPS speeds this up; nothing needs CUDA.
  - **(b) Colab GPU.** Scale the Transformer to baby-GPT size (6 × 384, context 256,
    dropout 0.2) and approach ≈ 1.47; swap our layers for real kernels (`mamba-ssm` for
    Mamba/Mamba-2; `flash-linear-attention` for GLA / DeltaNet / Gated DeltaNet) and measure
    where training throughput crosses FlashAttention as `T` grows (SSD reports ~2K at its
    scale).
  - **(c) Local GPU.** Contexts of 1024–4096; a **hybrid-ratio sweep** (0, ⅛, ¼, ½ attention)
    on val NLL and MQAR; a **state-size sweep**; optionally a 3:1 Gated-DeltaNet : attention
    hybrid in the style of 2025 production models. (The CUDA kernels in (b) and (c) need an
    NVIDIA GPU.)
- **10.3** **The hand-off checkpoint.** Choose the model to hand on (default: the best val
  NLL among the Transformer and the hybrid; record why in `progress.md`) and save the bundle
  to `<data root>/ai-sequence-models/checkpoints/final/`: `model.pt` (state dict),
  `config.json` (architecture name, hyperparameters, the 65-character vocabulary string,
  corpus SHA-256, val NLL, date), a snapshot of `charlm.py`, `samples.txt`, and
  `scoreboard.md`. The code snapshot matters: a state dict is not a model, and without the
  class that built it the next course cannot reload it. **The contract** the next course
  checks (its `through-line-lab.md` §2a): the 65 characters in `sorted(set(text))` order;
  `model(idx)` maps a `LongTensor (B, T)` to causal logits `(B, T, 65)`; the maximum
  context `block` is in `config.json`; and ideally `model.hidden(idx) → (B, T, d)` (the
  last block's output, for its reward model). **Exercise:** reload the bundle in
  a fresh process and reproduce the val NLL to 1e-4. `ai-post-training-and-rl` starts from
  exactly this bundle.
- **10.4** **Where to go next.** Every paper in the five wikis below is now readable.
  `ai-post-training-and-rl` (the same model, post-trained); `audio-codec-lms` (the same
  language models over audio codec tokens); `filters` / `pasp` for the DSP side; and Phase 11.

## Phase 11 — The Frontier (a living section)
> **This phase tracks the current state of the art and is revised as the field moves.** It
> is depth-on-demand, never a gate. Each topic re-asks the keystone question (what can token
> `t` see, at what cost?), pins to the same corpus and scoreboard where possible (often via
> MQAR or the repeat probe), and ends by reading one paper from the Frontier sources
> together. Claims marked *(empirical)* are benchmark results that later work may overturn;
> production-model claims are vendor-reported and largely unreplicated. Last surveyed:
> **October 2026**.

- **11.1** **The delta-rule family at scale** (extends 6.5). **Gated DeltaNet** (decay +
  delta; reported to beat Mamba-2 and DeltaNet at 1.3B, *empirical*); **RWKV-7 "Goose"** (a
  generalized delta rule with vector-valued gates and in-context learning rates);
  **Kimi Delta Attention** (Gated DeltaNet with channel-wise gates). DSP kin: per-coefficient
  step sizes are the idea behind proportionate-type NLMS. **Pin:** give our delta-rule mixer
  vector-valued `α_t` and `β_t` and re-run MQAR.
- **11.2** **State tracking and the transition matrix** (extends 8.6). Diagonal transitions
  with eigenvalues in `[0, 1]` cannot track parity (Merrill et al. 2024, *The Illusion of
  State*; Grazzi et al. 2024–25: allow negative eigenvalues); DeltaProduct (several delta
  steps per token: products of Householder-like transitions); Mamba-3's complex-valued state.
  **Exercise:** solve parity with a one-state linear recurrence `h_t = a_t h_{t−1}`,
  `a_t = (−1)^{x_t}` — and say why a real positive pole cannot do it. (Theorem-level for the
  idealized models; how much it matters for language is *empirical*.)
- **11.3** **Test-time training and learned memories** (extends 6.5). TTT layers (Sun et al.
  2024): the state is the weights of an inner model, updated by a gradient step per token on
  a self-supervised loss — the delta rule is the case of a linear inner model and one SGD
  step. Titans (Behrouz et al. 2025): a neural long-term memory with momentum and forgetting,
  combined with attention. DSP kin: from LMS to nonlinear adaptive filters; momentum is the
  heavy-ball method. Caution from the triadic paper: some TTT gains may simply be larger state
  *(empirical)*.
- **11.4** **Mamba-3** (extends 8.2–8.6; ICLR 2026). Three changes: a more expressive
  discretization built on the **trapezoidal rule** (the integrator behind the bilinear
  transform — check the paper's exact scheme), a complex-valued state update for state
  tracking, and a MIMO formulation that raises hardware utilization at decode. Reported
  *(empirical)*: +0.6 average downstream accuracy over Gated DeltaNet at 1.5B; Mamba-2-level
  perplexity with half the state. **Exercise:** derive the trapezoidal update for a one-pole
  `x' = a x + b u` and recognize the bilinear transform.
- **11.5** **Production hybrids and shrinking full attention's budget** (extends 5.4–5.5,
  9.3). Hybrids: Nemotron-H (most attention layers replaced by Mamba-2; up to ~3× faster
  inference reported at long inputs), MiniMax-01 (lightning attention with periodic softmax
  layers; 1M-token training context), Qwen3-Next (Gated DeltaNet : gated attention ≈ 3:1),
  Kimi Linear (Kimi Delta Attention : MLA = 3:1; up to 75% less KV cache and ~6× decode
  throughput at 1M reported). The pattern so far *(empirical, fast-moving)*: roughly 3:1 to
  7:1 linear : full, with full attention kept for retrieval. Keeping full attention but
  cutting its cost: **MLA** (DeepSeek-V2: cache a low-rank latent per token), **Native Sparse
  Attention** (compressed + selected + sliding branches, trained end to end), attention
  sinks and StreamingLLM (keep the first few tokens plus a window), KV eviction (H2O),
  paged KV memory (vLLM), RoPE scaling for context extension (YaRN), FlashAttention-2/3.
  **Pin:** add attention-sink + window to our Transformer and compare its repeat probe with
  the plain window from 5.5.
- **11.6** **State size as the axis** (extends 6.3, 9.5). Triadic linear attention (Sieberling
  et al. 2026, in the collection): a third-order state `k ⊗ k′ ⊗ v` with a small second key of
  size `E` multiplies capacity by `E` for ~1% more parameters; triadic Gated DeltaNet at 1.3B
  out-predicts a Transformer on PG19 to 64K tokens, and in a 3:1 hybrid an enlarged recurrent
  state beat a doubled KV cache at about half the memory. One recent preprint — *(empirical,
  single source)*. **Pin:** add a second key to our linear-attention mixer and re-run MQAR at
  matched state.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If shaky,
   re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. The
   recurring pictures are the **ledger** (what token `t` sees, at what cost) and the **two
   views** (parallel matrix `W` vs recurrent state). For DSP learners, name the filter kin
   (FIR, integrator, one-pole, modal bank, LTV, LMS) — and say where the analogy stops.
3. **Pin it to the model.** Every mechanism is implemented as a `Mixer` in `charlm.py`,
   passes the `forward` ≡ `step` check, is trained under the same budget, and gets a
   scoreboard row and a sample. A measured number beats a diagram beats an equation.
4. **Tiny exercise** to verify: predict a probe result before running it, compute a cost by
   hand, map one paper's symbols onto the course's notation, or write a few lines. The
   exercise *is* the check.
5. **Common misreadings** when relevant — keep [`the-context-budget.md`](the-context-budget.md)'s
   list live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, the scoreboard row, and a mastery
   note to `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the mechanism's keystone answer in one or two sentences ("Mamba sees the whole past
   through a fixed `2d·N` state whose pole radius the input steers; `O(1)` per token; trained
   by a scan because it is linear in the state").
2. Carry out the small task: implement the mixer and pass the agreement check, compute its
   memory at step `t`, or predict and then measure a probe — and explain the result.
3. Spot a deliberately wrong claim ("FlashAttention is sub-quadratic" — no, exact and still
   `O(T²)` FLOPs; "Mamba is an LTI filter" — no, selective means time-varying; "a state worth
   16 tokens of cache remembers 16 tokens" — no, a lossy summary of everything).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wikis this course teaches from
This course is the *pedagogical* front-end of JOS's paper collection
[`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023) (branch `master`); the
wikis stay canonical, the course stays pedagogical. Read / link these:

- **[`attention/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/attention/wiki)** —
  the home wiki for Phases 3–6 and 9. Concept pages: `scaled-dot-product-attention.md`,
  `positional-encoding.md`, `kv-cache-optimization.md`, `efficient-attention.md`,
  `linear-attention.md`, **`state-capacity.md`** (the associative-memory view — Phase 6.3),
  `hybrid-architectures.md`. Source summaries: `additive-attention`,
  `attention-is-all-you-need`, `self-attention-relative-position`, `rope`, `alibi`,
  `multi-query-attention`, `grouped-query-attention`, `flash-attention`, `longformer`,
  `ring-attention`, `transformers-as-rnns`, `attention-free-transformer`,
  `gated-linear-attention`, `based`, `jamba`, `transformers-are-ssms`,
  `triadic-linear-attention`, `transformer-catalogue`.
- **[`mamba/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/mamba/wiki)** —
  Phases 7–8. Concept pages: `state-space-models.md`, `selective-state-spaces.md`,
  `ssm-attention-convergence.md`; source summaries `hippo`, `s4`, `sashimi`, `dss`, `s4d`,
  `s5`, `h3`, `lru`, `ls-rnn`, `mamba`, `retnet`, `rwkv`, `griffin`, `jamba`, `mamba360`.
  Its `overview.md` reading order is the Phase 7–8 spine.
- **[`rwkv/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/rwkv/wiki)** and
  **[`gated-recurrence/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/gated-recurrence/wiki)** —
  Phase 6.4: `rwkv-architecture.md`, sources `rwkv`, `eagle-finch`; `gated-linear-rnns.md`,
  source `hgrn2` (with the HGRN2 ↔ GLA correspondence table).
- **[`hybrid/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/hybrid/wiki)** —
  Phase 9: `recall-memory-tradeoff.md`, `hybrid-architectures.md`; sources `based`, `mega`,
  `megalodon`, `griffin`, `recurrentgemma`, `jamba`, `zamba`, `samba`, `mambaformer`.
- **[`natural-language-processing/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/natural-language-processing)** —
  Phase 2: the word2vec, seq2seq and ELMo PDFs (no wiki yet).
- **[`ai-2012-to-2023/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-2012-to-2023/wiki)** —
  cross-cutting concept pages shared with `ai-miracle-decade-plus`:
  `pretrain-finetune-lineage.md`, `autoregressive-vs-gap-filling.md`,
  `scaling-and-emergence.md`, `representation-learning-arc.md` (Phases 2 and 5).
- DSP bridge: [`ddsp/wiki/sources/dafx26-diagonal-ssm-plate-reverb.md`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ddsp/wiki/sources/dafx26-diagonal-ssm-plate-reverb.md)
  (Phase 7.4).
- Known gaps in the collection: DeltaNet / Gated DeltaNet, RWKV-7, TTT and the 2025–26
  production hybrids are *not yet ingested*; Phases 6.5 and 11 cite them from the primary
  papers below. Keep the course in sync as the wikis grow.

### Source papers (in the collection unless marked)
- **Shannon (1951)** — *Prediction and Entropy of Printed English*. Bell Syst. Tech. J. *(not in collection)*
- **Bengio et al. (2003)** — *A Neural Probabilistic Language Model*. JMLR 3. *(not in collection)*
- **Mikolov et al. (2013)** — *word2vec: Efficient Estimation of Word Representations*. arXiv:1301.3781.
  Negative sampling: Mikolov et al. (2013b), arXiv:1310.4546 *(not in collection)*.
- **Levy & Goldberg (2014)** — *Neural Word Embedding as Implicit Matrix Factorization*. NeurIPS 2014. *(not in collection)*
- **Hochreiter & Schmidhuber (1997)** — *Long Short-Term Memory*. Neural Computation. *(not in collection)*
- **Cho et al. (2014)** — GRU / RNN encoder–decoder. arXiv:1406.1078. *(not in collection)*
- **Sutskever, Vinyals & Le (2014)** — *Sequence to Sequence Learning*. arXiv:1409.3215.
- **Bahdanau, Cho & Bengio (2014)** — *Jointly Learning to Align and Translate*. arXiv:1409.0473.
- **Peters et al. (2018)** — *ELMo*. arXiv:1802.05365.
- **Vaswani et al. (2017)** — *Attention Is All You Need*. arXiv:1706.03762.
- **Shaw et al. (2018)** — *Relative Position Representations*. arXiv:1803.02155.
- **Radford et al. (2018, 2019)** — GPT-1, GPT-2 (OpenAI reports); **Brown et al. (2020)** — GPT-3, arXiv:2005.14165.
- **Devlin et al. (2018)** — *BERT*. arXiv:1810.04805.
- **Sennrich et al. (2016)** — BPE subword units. arXiv:1508.07909. *(not in collection)*
- **Kaplan et al. (2020)** — *Scaling Laws*. arXiv:2001.08361; **Hoffmann et al. (2022)** — Chinchilla, arXiv:2203.15556.
- **Touvron et al. (2023)** — *LLaMA*. arXiv:2302.13971.
- **Xiong et al. (2020)** — *On Layer Normalization in the Transformer Architecture* (pre-LN). arXiv:2002.04745. *(not in collection)*
- **Su et al. (2021)** — *RoFormer / RoPE*. arXiv:2104.09864; **Press et al. (2021)** — *ALiBi*, arXiv:2108.12409.
- **Shazeer (2019)** — *MQA*. arXiv:1911.02150; **Ainslie et al. (2023)** — *GQA*, arXiv:2305.13245.
- **Dao et al. (2022)** — *FlashAttention*. arXiv:2205.14135.
- **Beltagy et al. (2020)** — *Longformer*. arXiv:2004.05150; **Liu et al. (2023)** — *Ring Attention*, arXiv:2310.01889.
- **Olsson et al. (2022)** — *In-context Learning and Induction Heads*. arXiv:2209.11895. *(not in collection)*
- **Katharopoulos et al. (2020)** — *Transformers are RNNs* (linear attention). arXiv:2006.16236.
- **Schlag, Irie & Schmidhuber (2021)** — *Linear Transformers Are Secretly Fast Weight Programmers*. arXiv:2102.11174. *(not in collection)*
- **Zhai et al. (2021)** — *An Attention Free Transformer*. arXiv:2105.14103.
- **Sun et al. (2023)** — *RetNet*. arXiv:2307.08621.
- **Yang et al. (2023)** — *Gated Linear Attention*. arXiv:2312.06635.
- **Yang et al. (2024)** — *Parallelizing Linear Transformers with the Delta Rule over Sequence Length* (DeltaNet). arXiv:2406.06484. *(not in collection)*
- **Peng et al. (2023)** — *RWKV*. arXiv:2305.13048; **Peng et al. (2024)** — *Eagle and Finch* (RWKV-5/6), arXiv:2404.05892.
- **Qin et al. (2024)** — *HGRN2*. arXiv:2404.07904.
- **Gu et al. (2020)** — *HiPPO*. arXiv:2008.07669.
- **Gu, Goel & Ré (2021)** — *S4*. arXiv:2111.00396; **Goel et al. (2022)** — *SaShiMi*, arXiv:2202.09729.
- **Gupta et al. (2022)** — *DSS*. arXiv:2203.14343; **Gu et al. (2022)** — *S4D*, arXiv:2206.11893;
  **Smith et al. (2022)** — *S5*, arXiv:2208.04933.
- **Fu et al. (2022)** — *H3 (Hungry Hungry Hippos)*. arXiv:2212.14052.
- **Orvieto et al. (2023)** — *LRU*. arXiv:2303.06349; **Martin & Cundy (2018)** — parallel linear RNNs, arXiv:1709.04057.
- **Blelloch (1990)** — *Prefix Sums and Their Applications* (CMU tech report). *(not in collection)*
- **Gu & Dao (2023)** — *Mamba*. arXiv:2312.00752; **Dao & Gu (2024)** — *Transformers are SSMs* (Mamba-2 / SSD), arXiv:2405.21060.
- **Patro & Agneeswaran (2024)** — *Mamba-360* survey. arXiv:2404.16112.
- **Arora et al. (2023)** — *Zoology* (MQAR). arXiv:2312.04927. *(not in collection)*
- **Arora et al. (2024)** — *Based*. arXiv:2402.18668.
- **Jelassi et al. (2024)** — *Repeat After Me: Transformers are Better than State Space Models at Copying*. arXiv:2402.01032. *(not in collection)*
- **De et al. (2024)** — *Griffin / Hawk*. arXiv:2402.19427; **Botev et al. / Google DeepMind (2024)** — *RecurrentGemma*, arXiv:2404.07839.
- **Lieber et al. (2024)** — *Jamba*. arXiv:2403.19887; **Glorioso et al. (2024)** — *Zamba*, arXiv:2405.16712;
  **Ren et al. (2024)** — *Samba*, arXiv:2406.07522.
- **Ma et al. (2023)** — *Mega*. arXiv:2209.10655; **Ma et al. (2024)** — *Megalodon*, arXiv:2404.08801.
- **Karpathy** — *char-rnn* (2015) and *nanoGPT* (GitHub): the corpus and the reference numbers. *(not in collection)*

### Frontier sources (Phase 11 — a living list, updated as the field moves)
These track the current edge and *will* be added to and reordered; treat them as the
reading behind Phase 11, not a fixed canon. None except the triadic paper is in the
collection yet.

- **11.1 — delta-rule family.** Yang, Kautz & Hatamizadeh (2024), *Gated Delta Networks:
  Improving Mamba2 with Delta Rule*, arXiv:2412.06464; Peng et al. (2025), *RWKV-7 "Goose"
  with Expressive Dynamic State Evolution*, arXiv:2503.14456; Kimi Team (2025), *Kimi Linear:
  An Expressive, Efficient Attention Architecture*, arXiv:2510.26692.
- **11.2 — state tracking.** Merrill, Petty & Sabharwal (2024), *The Illusion of State in
  State-Space Models*, arXiv:2404.08819; Grazzi et al. (2024), *Unlocking State-Tracking in
  Linear RNNs Through Negative Eigenvalues*, arXiv:2411.12537 (cite the latest version — its
  theorems were corrected after v1); Siems et al. (2025), *DeltaProduct: Improving
  State-Tracking in Linear RNNs via Householder Products*, arXiv:2502.10297.
- **11.3 — test-time training.** Sun et al. (2024), *Learning to (Learn at Test Time): RNNs
  with Expressive Hidden States*, arXiv:2407.04620; Behrouz, Zhong & Mirrokni (2025),
  *Titans: Learning to Memorize at Test Time*, arXiv:2501.00663.
- **11.4 — Mamba-3.** Lahoti et al. (2026), *Mamba-3: Improved Sequence Modeling using State
  Space Principles*, ICLR 2026, arXiv:2603.15569.
- **11.5 — production hybrids and long-context attention.** NVIDIA (2025), *Nemotron-H: A
  Family of Accurate and Efficient Hybrid Mamba-Transformer Models*, arXiv:2504.03624;
  MiniMax (2025), *MiniMax-01: Scaling Foundation Models with Lightning Attention*,
  arXiv:2501.08313; Qwen Team (2025), *Qwen3-Next* model release (blog and model card, no
  paper at last survey — verify details against the official card); Kimi Linear (above);
  DeepSeek-AI (2024), *DeepSeek-V2* (MLA), arXiv:2405.04434; Yuan et al. (2025), *Native
  Sparse Attention*, arXiv:2502.11089; Xiao et al. (2023), *Efficient Streaming Language
  Models with Attention Sinks*, arXiv:2309.17453; Zhang et al. (2023), *H2O: Heavy-Hitter
  Oracle*, arXiv:2306.14048; Kwon et al. (2023), *PagedAttention / vLLM*, arXiv:2309.06180;
  Peng et al. (2023), *YaRN*, arXiv:2309.00071; Dao (2023), *FlashAttention-2*,
  arXiv:2307.08691; Shah et al. (2024), *FlashAttention-3*, arXiv:2407.08608.
- **11.6 — state size.** Sieberling et al. (2026), *Triadic Linear Attention:
  Three-Dimensional Recurrent States for Long-Context Sequence Modeling*, arXiv:2609.36529
  (in `attention/`; wiki summary `sources/triadic-linear-attention.md`).
