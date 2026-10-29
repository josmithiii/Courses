# The Context Budget — This Course's Keystone

Every sequence model in this course answers the same question, and the answers are the
whole subject:

> **When the model predicts token `t`, what can it see of tokens `1 … t−1` — and what does
> that cost?** Cost in three currencies: the **memory carried forward** while generating
> (the state), the **compute per generated token**, and how **parallel training** can be
> across the sequence.

A bigram sees one character. A Transformer sees every past token *exactly* — and pays for
it with a **KV cache** that grows with `t`. A recurrent model (GRU, linear attention, S4,
Mamba, RWKV, DeltaNet) sees *everything*, but only through a **fixed-size state** — a lossy
summary that costs the same at token 10 and token 10 million. Hybrids spend exact memory in a
few layers and summaries in the rest. That is the **recall-vs-memory trade-off**, and it is
the spine of the course.

Read this in Phase 0.1. Return to it in **Phase 4.5** (the KV cache made measurable),
**Phase 6.3** (the fixed state as an associative memory), **Phase 8.6** (one operator, two
algorithms), **Phase 9** (the trade-off measured), and **Phase 10.1** (you fill in the
ledger below with your own numbers). Every term in **bold** is earned somewhere in the
syllabus; the phase is in brackets.

---

## The ledger (per layer; `d` = `d_model`, `d_h` = head dim, `N` = SSM state per channel, `w` = window)

| Mechanism [phase] | What token `t` can see | Memory carried at step `t` | Compute per generated token | Training across `T` | Mixing depends on content? |
|---|---|---|---|---|---|
| **Bigram** [1.3] | token `t−1` only | one token | `O(1)` lookup | trivial | — |
| **Fixed window** (Bengio MLP) [1.4] | last `k` tokens, exactly | `k` tokens | `O(k·d·d_ff)` | parallel | no (fixed per-slot weights) |
| **RNN / GRU** [2.2–2.4] | everything, through `h ∈ R^d` | `d` floats | `O(d²)` | **sequential** (gates read the state) | yes |
| **Full causal attention** [3–4] | every past token, exactly (within `n_ctx`) | **KV cache `2·d·t` floats — grows** | `O(t·d + d²)` | parallel, `O(T²·d)` | fully |
| **Sliding window** [5.5] | last `w` tokens, exactly | `2·d·w` floats | `O(w·d + d²)` | parallel, `O(T·w·d)` | fully, within `w` |
| **Linear attention** [6.1–6.3] | everything, through matrix state `S` | `d·d_h` floats | `O(d·d_h)` | parallel (chunkwise) | `q, k, v` yes; no normalization, no forgetting |
| **Gated linear / RetNet / GLA / HGRN2 / RWKV-5,6** [6.4] | everything, with decay | `d·d_h` floats | `O(d·d_h)` | chunkwise | yes, via decay `α_t` |
| **DeltaNet / Gated DeltaNet** [6.5] | everything; state *edited*, not just added to | `d·d_h` floats | `O(d·d_h)` | chunkwise | yes, decay + erase |
| **LTI SSM** (S4, S4D, LRU) [7] | everything, through **fixed filters** | `d·N` (complex) | `O(d·N)` | parallel: FFT convolution or scan | **no** — same filter for every input |
| **Selective SSM** (Mamba) [8.1–8.5] | everything, through **input-steered filters** | `2d·N` floats (expand 2) | `O(d·N)` | parallel scan | yes, via `Δ_t, B_t, C_t` |
| **Mamba-2 / SSD** [8.6] | as Mamba, scalar decay per head | `2d·N` floats, with larger `N` (64–256) | `O(d·N)` | chunkwise (tensor cores) | yes |
| **Hybrid** (e.g. 3 recurrent : 1 attention) [9] | exact in the attention layers, summaries elsewhere | KV cache in ¼ of layers + fixed states | mixed | mixed | yes |

**The exchange rate** [6.3, 8.3]. How many tokens of KV cache is a fixed state *worth* in
bytes? A token costs `2·d` floats of cache per layer. Linear attention with `h` heads of
size `d_h` (`h·d_h = d`) carries `d·d_h` floats, so its state is worth **`d_h/2` tokens** of
cache. Mamba with expand 2 carries `2d·N` floats: worth **`N` tokens**. For this course's
default model (`d = 128`, `d_h = 32`, `N = 16`) both are worth **16 tokens**. This is
arithmetic, not an empirical claim — and it is *not* a statement that the state remembers
only 16 tokens (see misreading 2).

## Two views of one operator [6.2, 7.1, 8.6]

Every mixer above produces `y_t = Σ_{s≤t} W[t,s] · v_s` for a lower-triangular `T × T`
mixing matrix `W` (linear in the values once `W` is fixed; `W` itself is computed from the
input, so the layer as a whole is nonlinear in `x`):

| Mechanism | `W[t,s]` |
|---|---|
| Softmax attention | `softmax_s(q_tᵀk_s / √d_h)` |
| Linear attention | `φ(q_t)ᵀφ(k_s)` |
| RetNet | `γ^(t−s) · q_tᵀk_s` |
| Mamba-2 / GLA-style decay | `(Π_{r=s+1..t} a_r) · C_tᵀB_s` |
| LTI SSM | `K[t−s]` — Toeplitz: a convolution |

The **matrix view** is how you train in parallel. The **recurrent view**
`S_t = A_t S_{t−1} + k_t v_tᵀ` is how you generate in `O(1)` per token. A mixer *has* a
finite-state recurrent view exactly when `W` has low **semiseparable rank** (every block
below the diagonal has rank ≤ `N`); Mamba-2's SSD paper makes this precise: SSMs with state
`N` ⇔ `N`-semiseparable matrices [8.6]. That is the time-varying analogue of a fact DSP
people already know: an impulse response has a finite-order state-space realization iff its
**Hankel matrix has finite rank** (Kronecker; Ho–Kalman), and the rank is the minimal state
dimension. The softmax attention matrix has no such low-rank structure in general — so it
has no finite-state recurrence, and the KV cache is not an implementation detail but a
necessity.

## The DSP dictionary (for learners from `../filters/`)

Analogies, not identities — each one is earned and qualified in its phase.

| Sequence-model idea | DSP kin |
|---|---|
| Fixed-window / n-gram model [1.4] | **FIR** filter in token space: exact memory of `k` taps, nothing beyond |
| KV cache [4.5] | a **delay line that never stops growing**, read by a content-addressed, normalized (softmax), time-varying FIR |
| Sliding-window attention [5.5] | a fixed-length delay line (FIR of length `w`) |
| Linear attention, no decay [6.2] | an **integrator** — pole at `z = 1`; nothing is ever forgotten, so the state grows |
| RetNet / gated decay [6.4] | **one-pole leaky integrators** (fixed pole `γ`, then data-dependent pole `α_t`) |
| DeltaNet [6.5] | **LMS adaptive filter** (Widrow–Hoff): the state is a weight matrix identified online from key→value pairs; `β` is the step size, unit-norm keys give NLMS |
| Chunkwise-parallel training [6.6] | **block processing**: direct computation inside a block, state carried across blocks |
| LTI SSM / S4D [7.1, 7.4] | the **modal representation** (filters 11.4): a bank of parallel complex one-poles = real resonators; the convolution kernel is the impulse response (the Markov parameters) |
| Training an LTI SSM by FFT [7.6] | **fast convolution** (zero-pad to `2T`, multiply spectra) |
| LRU's `λ = exp(−exp(ν) + iθ)` [7.5] | poles kept inside the unit circle **by parameterization** |
| Parallel scan [7.5] | first-order recursions compose associatively: `(a₂,b₂)∘(a₁,b₁) = (a₂a₁, a₂b₁+b₂)` |
| Mamba's selection [8.2] | a **linear time-varying** filter (filters 11.5) whose pole radius `exp(Δ_t A)` the input steers |
| Mamba's short conv before the SSM [8.4] | a tiny FIR in front of an IIR |
| Mamba-3's trapezoidal discretization [11.4] | the trapezoid rule behind the **bilinear transform** |
| Negative / complex eigenvalues for state tracking [11.2] | a real positive pole can only decay; a pole at `−1` can toggle a sign |

---

## The misreadings this course exists to kill

Curated from the `attention/`, `mamba/`, and `hybrid/` wikis. The tutor flags each on the
spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "Linear attention / Mamba is just faster attention." | A **different function class**. A fixed state is a lossy summary; exact recall of arbitrary past tokens is lost. That a fixed state cannot hold more than it has room for is a theorem-level fact; *how big* the gap is at a given scale is empirical. | 6.3, 9.1 |
| "A state worth 16 tokens of KV cache remembers the last 16 tokens." | It holds a lossy summary of the **whole** past, typically fading with distance. The exchange rate compares bytes, not contents. | 6.3, 8.3 |
| "Attention is `O(T²)` per generated token." | With a KV cache, each new token costs `O(t·d)`; `O(T²)` is the total over a sequence (and the training cost). Without a cache, naive recomputation is what's quadratic per token. | 4.5 |
| "Transformers have unlimited context." | Exact access only within the trained `n_ctx`; beyond it, behavior depends on the **position encoding** (length extrapolation is empirical and method-dependent). Memory and per-token compute grow linearly with `t`. | 4.3, 4.5 |
| "FlashAttention approximates attention / makes it sub-quadratic." | **Exact**; still `O(T²)` FLOPs. It saves memory traffic and keeps memory `O(T)` by tiling. FLOPs ≠ wall clock. | 5.5 |
| "Low perplexity means good recall." | On Tiny Shakespeare most of the loss is local structure. A sliding-window or fixed-state model can nearly tie on val NLL and still fail the **repeat probe** and **MQAR**. Measure both. | 5.5, 9.2 |
| "Mamba is S4 with extra steps." | S4 is **LTI** (a fixed filter: trainable as a convolution). Mamba is **selective = LTV**: `Δ, B, C` depend on the input, which kills the convolution view and needs a scan. | 8.1–8.3 |
| "Gates make a recurrence nonlinear in the state." | GRU/LSTM gates read `h_{t−1}`, so the recurrence is nonlinear and **sequential**. Mamba/GLA/RWKV gates read only the input, so the recurrence stays **linear in the state** and can be scanned in parallel. That is the price of parallel training. | 2.3, 8.2 |
| "RNNs lost because they can't learn long dependencies." | Vanishing gradients mattered, but the decisive loss was **training parallelism**: a nonlinear recurrence is sequential in `T`. Linear recurrences got parallelism back through the scan. | 2.4, 7.5 |
| "State-space models are new." | State space is Kalman-era (1960); digital filters have had it forever. New: deep stacks, **initialization** (HiPPO), **selectivity**, and hardware-aware kernels. | 7.1 |
| "Mamba-2 proved attention and SSMs are the same thing." | SSD shows a **specific** class coincides: scalar-decay SSMs ⇔ masked linear attention with a 1-semiseparable mask. Softmax attention is not in that class. | 8.6 |
| "Hybrids are a compromise, worse at both." | In the reported studies, hybrids match or beat pure models at equal compute. The **best ratio** of attention to recurrence is open and empirical. | 9.3 |
| "My CPU timing of a pure-PyTorch Mamba shows Mamba is slow." | Absolute speed is dominated by implementation (Mamba's speed is a fused GPU kernel). What transfers is **scaling with `t` and `T`** — measure slopes, not intercepts. | 8.3 |

---

## How the course earns the budget

| Piece | Earned in |
|---|---|
| prediction, perplexity, the exact baselines (65 / 28.4 / 12.0), the fixed window | **Phase 1** |
| the whole past through one vector: RNN, GRU, the seq2seq bottleneck | **Phase 2** |
| look back instead of remembering: attention as soft lookup | **Phase 3** |
| full attention read closely; the KV cache measured; the repeat probe | **Phase 4** (keystone) |
| GPT-style scale, and cheaper *exact* attention (GQA, FlashAttention, windows) | **Phase 5** |
| drop the softmax → an RNN with a matrix state; decay; the delta rule | **Phase 6** (keystone) |
| LTI state-space filters: HiPPO, S4, S4D, LRU, the scan | **Phase 7** |
| selection (LTV) and the SSD duality | **Phase 8** (keystone) |
| the recall-vs-memory trade-off measured; hybrids | **Phase 9** |
| the full ledger, filled in with your own scoreboard | **Phase 10.1** |
