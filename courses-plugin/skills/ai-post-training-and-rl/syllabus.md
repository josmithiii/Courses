# Post-Training & RL — From a Language Model to an Assistant

**Learner profile:** Has `ai-foundations/` (Transformers, next-token prediction, what
RLHF is *in one sentence*) and ideally `ai-sequence-models/` (course 2 of this curriculum),
so they have trained a small character-level language model on Tiny Shakespeare and can
read a PyTorch training loop. No RL background is assumed. Signal-processing and control
analogies are welcome and used throughout: a discounted return is a one-pole filter run
backward in time, TD learning is LMS on a bootstrapped target, a baseline is a control
variate, the KL leash is regularization toward a prior. ~1 hour per day, one concept at a
time, every concept checked with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisites (no hard gates):** `ai-foundations/` Phases 4–5. `ai-sequence-models/` is
the natural predecessor: its saved checkpoint is this course's starting model. A learner
who arrives without it trains the **Phase 0 fallback model** (about 3 minutes on a laptop
CPU), and the tutor says so explicitly. JOS's standing preference holds: plunge in, get
motivated, backfill. If a learner is shaky on attention or on what a logit is, point them
at `ai-foundations/` Phase 4 or `ai-sequence-models/` for that topic and keep going.

**Companion course:** [`ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) reads the
same landmark papers as a *history tour* (its Phase 3: DQN, AlphaGo, AlphaZero; 6.1 and
8.1: Kaplan, Chinchilla; 8.3: CoT; 9.1–9.2: InstructGPT, Constitutional AI; 10.3:
Toolformer). This course goes *under the hood*: derive the objective, write the loss, run
it on our model. Don't re-teach the history; point to the tour for it.

**The keystone — read [`the-reward-and-the-leash.md`](the-reward-and-the-leash.md) in
Phase 0.1.** One objective organizes the course:
`J(π) = E[r(x, y)] − β · KL(π ‖ π_ref)` — climb a reward while a KL leash keeps the policy
near the reference model — and its closed-form optimum, the **tilted reference**
`π* ∝ π_ref · exp(r/β)`. Every method is a different way to reach that tilt (sampling,
on-policy gradients, or closed-form reparameterization), and every reward source sits
somewhere on a *trust* axis (a game result is the truth; a learned reward model is a
proxy). Deep RL (Phases 1–3) supplies the optimizer vocabulary; Phases 6 and 7 are the
keystone proper. We spend as long as it takes there.

**The worked example (through-line):** the curriculum's **one small character-level
language model**, trained on `../curricula/assets/ai-llms-and-sequence-models/tinyshakespeare.txt`
(65 characters, 1,115,394 chars, SHA-256
`86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`; see that directory's
`README.md`). This course **post-trains that same model**: SFT on a formatting
convention (*two-line replies*), a CPU-cheap, legible, **hackable** programmatic reward
(the **meter reward**: ten syllables a line), best-of-n, REINFORCE → PPO-lite with a KL
leash, a learned reward model and its over-optimization, DPO, and (frontier) GRPO. The
recipes and the canonical numbers live in [`through-line-lab.md`](through-line-lab.md).
Deep-RL landmarks get their own tiny exercises (gridworld, CartPole, tic-tac-toe). Real
models (a small open instruct model with TRL) are an optional upper capstone tier.

> **Fail fast:** if the corpus file is missing or its SHA-256 differs, the tutor says so
> and stops. If it is merely absent (e.g. the course was installed as a plugin, which
> ships no assets), fetch it from the URL in that directory's `SOURCE.md` *out loud* and
> verify the hash before using it. Never silently substitute another corpus.

**End state:** by the last lesson the learner can: state the RL problem (policy, return,
value, Bellman equation) and explain DQN's two stabilizers; derive the REINFORCE
gradient, explain baselines, GAE and PPO's clip; explain how AlphaGo → AlphaZero turn
search into a policy-improvement operator, and why games need no leash; explain the
InstructGPT pipeline (SFT → reward model → PPO with a KL penalty) and each stage's job;
**derive the closed-form optimum of the KL-regularized objective and DPO from it**, and
say exactly which assumptions the equivalence needs; diagnose reward hacking on a
reward-vs-KL plot; explain Constitutional AI / RLAIF and Toolformer's self-supervised
filtering; read the scaling-law and double-descent curves and say which parts are
empirical; place RLVR / GRPO, process rewards and test-time compute on the same map; and
**run the whole pipeline on their own model**.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture.** A pretrained LM is a *distribution*
  `π_ref(y | x)` over continuations; post-training reshapes it. Three stages (pretrain →
  SFT → preference optimization) and one objective. Read
  [`the-reward-and-the-leash.md`](the-reward-and-the-leash.md). Preview the experiment
  that runs through the course: make a Shakespeare model write ten-syllable lines, watch it
  cheat, and stop the cheating with a leash.
- **0.2** **The corpus and the starting model.** Verify the corpus SHA-256 (fail fast).
  Then *either* load the learner's `ai-sequence-models` checkpoint (check the **contract**
  in `through-line-lab.md`: same 65-character vocabulary in sorted order, causal logits
  `(B, T) → (B, T, 65)`, a known context length; measure its validation NLL on the 90/10
  split) *or* — **stated explicitly to the learner, never silently** — train the **fallback
  model**: a 4-layer, 4-head, 128-wide character Transformer, context 128, ~826k
  parameters, 3,000 AdamW steps, about 3 minutes on a laptop CPU, val NLL ≈ 1.58 nats/char
  (between the bigram's 2.48 and nanoGPT's tuned ≈ 1.47). Any architecture works for
  post-training — Transformer, Mamba, hybrid — because every method here needs only two
  things: **sample** from the model, and score **log π(y_t | y_<t)**.
- **0.3** **The three plumbing functions.** `sample()`, `completion_logps()` (sum of
  per-token log-probs of a continuation), and the **exact per-token KL** to a reference
  (a 65-character vocabulary makes the full sum over the alphabet cheap — no estimator
  needed). Tools: `uv` with a `.venv`, `torch`, `numpy`, `matplotlib`, `gymnasium` (for
  CartPole). Exercise: compute `KL(π ‖ π_ref)` between the model at temperature 1 and at
  temperature 0.7 along a few samples, and explain its sign and size.

## Phase 1 — The Language of RL: Values, Q-Learning, DQN
- **1.1** **Agent, environment, reward, policy.** The Markov decision process `(S, A, P,
  r, γ)`. The LM-as-policy dictionary: state = prefix, action = next character, episode =
  one completion, reward usually only at the end (so most LM post-training is a
  **contextual bandit** over whole continuations, with token-level structure inside).
  Exercise: write the dictionary for the meter task.
- **1.2** **Return and discount.** `G_t = r_t + γ · G_{t+1}` — a one-pole recursion run
  *backward* in time, pole at `γ`. The effective horizon `1/(1 − γ)`. Exercise: compute
  `G_t` for a 5-step reward sequence by hand and by a reversed `scipy.signal.lfilter`.
- **1.3** **Value functions and the Bellman equation.** `V^π(s)`, `Q^π(s, a)`; the
  Bellman expectation and optimality equations; **value iteration** as a fixed-point
  iteration that converges because the Bellman operator is a `γ`-contraction (loop gain
  less than one). Exercise: value iteration on a 4×4 gridworld; plot `V` after 1, 5, 50
  sweeps.
- **1.4** **Q-learning and TD error.** Sample-based Bellman updates without a model:
  `Q(s,a) ← Q(s,a) + α · δ`, `δ = r + γ · max_a' Q(s', a') − Q(s, a)` — LMS on a
  **bootstrapped** target. ε-greedy exploration. Exercise: tabular Q-learning on the same
  gridworld; compare to value iteration.
- **1.5** **DQN (Mnih et al. 2013; *Nature* 2015).** A CNN approximates `Q` from Atari
  pixels; function approximation + bootstrapping + off-policy data (the "deadly triad")
  diverge, so two stabilizers: **experience replay** (break sample correlation) and a
  slowly updated **target network** (hold the regression target still — the *Nature*
  paper's addition). Exercise: DQN on CartPole on CPU, with and without the target
  network; plot episode return.
- **1.6** **What did and didn't carry to language models.** Value-based control over a
  65-way action per step is possible, but credit assignment over a 100-character
  completion and a reward only at the end favour **policy-gradient** methods; what carried
  is the **critic** (a learned value baseline) and the habit of stabilizing a moving
  target. Exercise: one-paragraph answer to "why isn't ChatGPT trained with DQN?"

## Phase 2 — Policy Gradients: REINFORCE → Actor-Critic → PPO
- **2.1** **The score-function gradient (REINFORCE; Williams 1992).**
  `∇_θ E_{y~π_θ}[R(y)] = E[ R(y) · ∇_θ log π_θ(y) ]` — the likelihood-ratio trick. You
  never differentiate the reward; you sample and reweight. This is how we will climb a
  syllable counter. Derive it together by hand (three lines).
- **2.2** **Baselines are control variates.** Subtracting any `b` independent of the
  action leaves the gradient unbiased and can cut its variance enormously; the batch-mean
  baseline, leave-one-out (RLOO). Exercise: estimate the gradient variance with and
  without a baseline on a 3-armed bandit.
- **2.3** **Actor-critic, advantage, GAE.** Learn `V_ψ` as a baseline; the advantage
  `A_t = Q − V`; TD residual `δ_t = r_t + γ · V(s_{t+1}) − V(s_t)`; **GAE**:
  `A_t = Σ_l (γλ)^l · δ_{t+l}` — an anticausal one-pole filter on TD residuals, `λ`
  trading bias (λ → 0) for variance (λ → 1). Exercise: implement GAE as a reversed
  first-order IIR filter and check it against the loop.
- **2.4** **Trust regions: TRPO → PPO.** Big policy steps on noisy gradients destroy the
  policy. TRPO constrains `KL(π_old ‖ π_θ)` per update; **PPO** clips the probability
  ratio `ρ = π_θ/π_old` to `[1 − ε, 1 + ε]` in a pessimistic surrogate. **This clip is a
  leash to `π_old`, per update — not the keystone's leash to `π_ref`.** Name both, now.
  Exercise: plot the clipped surrogate vs `ρ` for `A > 0` and `A < 0`.
- **2.5** **PPO on CartPole.** Small actor-critic with GAE + clip on CPU; compare
  learning curves with REINFORCE from 2.1–2.2.
- **2.6** **Pin: first contact with the meter reward — no leash.** REINFORCE with a batch
  baseline on the Phase 0 model (base or course-2 checkpoint; SFT comes in Phase 4)
  against the meter reward, `β = 0`. Watch reward rise — then read the samples. Keep the
  degenerate ones: they are the course's first **reward-hacking exhibit**, and the
  motivation for everything in Phase 6.

## Phase 3 — Search and Self-Play: AlphaGo → AlphaZero
- **3.1** **AlphaGo (2016) is an SFT → RL pipeline.** A policy net trained by supervised
  learning on 30 million expert positions (57.0% move accuracy) → an RL policy initialized
  from it and improved by policy-gradient self-play against earlier versions (it beats the
  SL policy >80% of the time) → a value net → Monte Carlo tree search at play time. The
  same three-stage shape InstructGPT will have six years later. And the 2016 diversity
  observation: the *SL* policy made the better prior for search, "presumably because humans
  select a diverse beam of promising moves, whereas RL optimizes for the single best move."
- **3.2** **MCTS as a policy-improvement operator; AlphaZero (2017).** PUCT selection;
  visit counts as an improved policy. AlphaZero drops human data: self-play, MCTS
  (800 simulations per move in training), and one loss `l = (z − v)² − πᵀ log p + c‖θ‖²`
  — regress the value on game outcomes, distil the **search's** visit distribution into
  the policy (expert iteration). *Correction to carry:* this is **not PPO** (the
  `ai-2012-to-2023` wiki says otherwise).
- **3.3** **Tic-tac-toe MCTS.** Exercise: MCTS with random rollouts; show the visit-count
  policy beats the raw prior; (optional) close the loop with a tiny policy-value net.
- **3.4** **Why games need no leash, and what carried.** In Go the reward is the rules —
  unhackable — and a perfect simulator is free; neither holds for language. What carried:
  the SFT-then-RL shape, best-of-n and rejection sampling (search distilled into a model),
  and, after 2024, search at decision time again (Phase 11.3). MuZero (2019) — planning
  in a *learned* model — as the bridge to world models (pointer only).

## Phase 4 — Supervised Fine-Tuning: Building the Anchor
- **4.1** **Base model vs assistant.** A base model continues documents; an assistant
  follows a convention. SFT = maximum likelihood on demonstrations = minimizing forward
  `KL(p_demo ‖ π)` — mode-covering. Exercise: say what SFT can and cannot teach.
- **4.2** **Pin: SFT the two-line reply convention.** Rebuild every speech in the corpus's
  *train* region as "header + exactly two lines + blank line" (and the val region
  separately, so nothing leaks); fine-tune 600 steps. Canonical result: the fraction of
  samples that answer `ROMEO:` with exactly two lines and hand off to a new speaker goes
  from **≈ 17% to ≈ 60%**, two-line val NLL **1.62 → 1.56**, general val NLL
  **1.58 → 1.61** (a small *alignment tax*).
- **4.3** **The SFT model becomes `π_ref`.** Why the leash attaches to the SFT model, not
  the base; InstructGPT's PPO-ptx (mix pretraining gradients back in) as the fix for the
  alignment tax. Aside: LoRA / parameter-efficient fine-tuning as a low-rank update
  `W + BA` (what tier-b capstones use). Exercise: predict what happens to the format rate
  if we RL against the meter reward with `β = 0` (answer in Phase 6.4).

## Phase 5 — Rewards From Preferences
- **5.1** **Why comparisons, not scores.** People are inconsistent at absolute scores and
  much better at "A or B?". **Bradley–Terry** (1952; Elo's cousin):
  `P(a ≻ b) = σ(r(a) − r(b))`; one scalar utility, transitive preferences — an assumption
  to remember. InstructGPT ranks K = 4–9 outputs per prompt (all `K(K−1)/2` pairs); its
  labelers agree with each other 72.6 ± 1.5% of the time.
- **5.2** **Training a reward model.** Initialize from the SFT model, put a scalar head on
  the last hidden state, minimize `−log σ(r_φ(y_w) − r_φ(y_l))`. Exercise: show the loss
  is logistic regression on reward differences, and that `r_φ` is only identified up to a
  per-prompt constant.
- **5.3** **Pin: a simulated labeler and a learned RM.** Our "human" is a Python
  function: the **meter reward** (the *gold* reward). Sample pairs from `π_ref`, label them
  Bradley–Terry-style from the gold reward (with label noise), train `r_φ` from the SFT
  trunk; report held-out pair accuracy. Same design as Gao et al. (2022), who used a large
  "gold" RM in place of humans.
- **5.4** **Reward misspecification and Goodhart.** The naive meter reward v0 also scores
  speaker headers as lines (two syllables, so "bad") — predict and then watch the policy
  stop naming speakers. Reward hacking vs specification gaming; proxy vs gold; Goodhart's
  law ("when a measure becomes a target, it ceases to be a good measure"). Exercise: list
  three ways to hit ten syllables without writing verse, then check which ones the model
  found in 2.6.

## Phase 6 — RLHF: The Reward and the Leash (keystone)
> Spend as long as it takes. Re-read [`the-reward-and-the-leash.md`](the-reward-and-the-leash.md).
- **6.1** **The InstructGPT objective.** `E[r_θ(x, y)] − β · log(π^RL/π^SFT) + γ ·
  E_pretrain[log π^RL]` (their eq. 2; `β = 0.02`, `γ = 27.8` for PPO-ptx). The per-token
  KL folded into the reward. What the KL measures (distribution distance on the policy's own
  samples), and what it doesn't (it is not weight decay, not dropout).
- **6.2** **The closed-form optimum: the tilted reference.** Derive
  `π* = π_ref · exp(r/β)/Z` by completing the KL (`J = −β·KL(π ‖ π*) + β·log Z`). Read it:
  posterior = prior × likelihood; `β` as temperature; the support cannot grow; every policy
  is an implicit reward. **Derive this together by hand** — it is the central proof of the
  course. Exercise: on a 3-continuation toy, compute `π*` for `β = 10, 1, 0.1`.
- **6.3** **Best-of-n: the tilt without training.** Sample `n` from `π_ref`, keep the
  highest reward; its KL from `π_ref` is at most `log n − (n−1)/n`. Pin: canonical curve
  on the SFT model — mean meter reward **0.60 (n=1) → 0.73 (2) → 0.87 (4) → 0.91 (8) →
  0.94 (16)**, for at most 0.19, 0.64, 1.20, 1.84 nats. Exercise: plot reward vs the KL
  bound; this is the frontier any trained method must beat.
- **6.4** **Pin: PPO-lite with the leash; the `β` sweep.** REINFORCE → PPO-lite (4 clipped
  epochs per batch, batch-normalized advantages) on the SFT model, reward
  `r − β · Σ_t log(π/π_ref)`, for `β ∈ {0, 0.01, 0.03, 0.1}`. Plot **reward vs measured KL**
  for each run, with best-of-n on the same axes. Canonical (300 steps): PPO-lite `β = 0`
  reaches reward **0.93 at KL 160 nats**, distinct-4-grams 0.73 → 0.42, and the samples
  have become monosyllable padding (`For, if ind; if ind, if, by Wick, if.`) — the hack,
  caught; `β = 0.03` levels off at **0.78, KL ≈ 9**, still Shakespeare-shaped. And,
  honestly: best-of-16 (0.94 at ≤ 1.84 nats) beats every trained run on this plane — a
  real finding, not an embarrassment. *This plot is the keystone artifact.*
- **6.5** **Over-optimization: gold vs proxy.** RL against the learned RM `r_φ` from 5.3
  while logging the gold meter reward: the proxy keeps rising while the gold stalls or
  falls as `√KL` grows — Gao et al.'s (2022) picture on a laptop. Canonical: a weak RM
  (held-out accuracy 0.57) is pushed from 0.48 to 1.45 while gold stays near 0.7, and
  the policy finds a proxy-only exploit (speaker headers mutate into
  `DUCHINCHINCHINCH…`). Their fitted functional forms are **empirical**; the qualitative
  shape is the lesson.
- **6.6** **What RLHF costs.** Diversity loss (mode-seeking reverse KL; AlphaGo's 2016
  observation again), the alignment tax and PPO-ptx, length and sycophancy as real-world
  reward hacks (pointers). Exercise: measure distinct-4-grams across the `β` sweep.

## Phase 7 — Direct Preference Optimization and Its Family (keystone, part two)
- **7.1** **DPO from the closed form (Rafailov et al. 2023).** Invert 6.2:
  `r = β·log(π/π_ref) + β·log Z`; substitute into Bradley–Terry; `Z` cancels;
  `L_DPO = −E log σ(β · [Δ_w − Δ_l])`. No reward model, no sampling during training.
  **Derive it together** from 6.2 in four lines.
- **7.2** **What the equivalence does and doesn't promise.** It holds *under* BT
  preferences, an unrestricted policy class, and data that cover the relevant
  continuations. DPO is **offline** (fixed pairs) where PPO is **on-policy**; DPO's
  implicit reward over-optimizes too; the chosen response's likelihood can *fall* during
  training (both log-probs drop, the loser's faster). Exercise: show the DPO gradient
  weights each pair by `σ(−h)` — how wrong the implicit reward currently is.
- **7.3** **Pin: DPO on our model.** Pairs sampled from `π_ref`, labelled by the gold
  meter reward; train with `β = 0.1`; place the result on the 6.4 reward-vs-KL plot next
  to PPO-lite and best-of-n at matched KL. Canonical: 1,375 pairs, two epochs, reward
  0.60 → 0.69 at KL 0.73 — well leashed, but below best-of-n at that KL. Why (offline
  pairs with small reward gaps), and what would help (iterative DPO on fresh pairs).
- **7.4** **The family, briefly.** IPO (Azar et al. 2023: DPO over-fits deterministic
  preferences; a squared loss fixes it), KTO (Ethayarajh et al. 2024: unpaired
  thumbs-up/down), ORPO and SimPO (2024: no reference model at all — the leash moved or
  removed), online / iterative DPO. *Honest status:* DPO-style methods dominate cheap open
  fine-tuning; on-policy RL (PPO, GRPO and kin) remains central at the frontier; the
  head-to-head comparisons are mixed and **empirical**.

## Phase 8 — Where the Reward Comes From: AI Feedback and Tools
- **8.1** **Constitutional AI (Bai et al. 2022).** SL-CAI: the model critiques and revises
  its own outputs against written principles; fine-tune on the revisions. RL-CAI: an AI
  judge compares pairs against the principles → a preference model → RL. RLAIF in general
  (Lee et al. 2023). Same objective, new reward source — move it on the trust axis.
- **8.2** **Pin: a constitution for the meter model.** Write three principles ("lines of
  six to fourteen syllables", "every reply names its speaker", "no word three times in a
  line"); implement the critic as code; do SL-CAI as best-of-k-then-fine-tune and RL-CAI
  as RL against the critic. *Honest gap:* in CAI the critic is a language model *reading*
  natural-language principles; ours is code. We reproduce the **structure**, not the
  language understanding (tier b swaps in a small instruct LM as the judge).
- **8.3** **Toolformer (Schick et al. 2023).** The model inserts API calls (calculator,
  Q&A, Wikipedia search, translation, calendar) into its own pretraining text and keeps a
  call only if the result lowers the loss on what follows by at least `τ_f`:
  `L⁻ − L⁺ ≥ τ_f`. Self-supervised — no human labels, no RL. Then ReAct-style reasoning +
  acting, and function calling as product convention (pointers).
- **8.4** **Pin: Toolformer's filter on our model.** A "search" tool that returns the
  training-corpus line best matching the current line's opening; insert `[S: …]` results
  into validation text and compute `L⁻ − L⁺` per position. Where does retrieval help
  (names, stock phrases) and where not? *Honest scope:* an 800k-parameter char model is not
  a tool user; we reproduce the *filtering criterion*, not emergent tool use.

## Phase 9 — Sidebar: Why Bigger Keeps Working (scaling laws, double descent)
> Independent of Phases 1–8 — can be taken any time after Phase 0.
- **9.1** **Kaplan et al. (2020).** Loss falls as a power law in parameters `N`, data `D`
  and compute `C ≈ 6ND`: `L(N) = (N_c/N)^{α_N}` with `α_N ≈ 0.076`, `α_D ≈ 0.095`,
  compute-optimal `N ∝ C^{0.73}`. On log-log axes, a straight line. **Empirical fits**
  over finite ranges, not laws of nature.
- **9.2** **Chinchilla (Hoffmann et al. 2022).** `L(N, D) = E + A/N^α + B/D^β`, fitted
  `E = 1.69, A = 406.4, B = 410.7, α = 0.34, β = 0.28`; compute-optimal `N` and `D` grow
  about equally with `C` — roughly 20 tokens per parameter (70B parameters on 1.4T tokens
  beats the 280B Gopher). Kaplan undertrained; the disagreement is partly fitting method.
  Exercise: by the 20:1 rule, what model size is compute-optimal for our 1M-character
  corpus *in one epoch*? (About 50k parameters — so our 826k-parameter model lives in the
  many-epoch, data-limited regime.)
- **9.3** **Pin: a mini scaling sweep.** Train four widths of the fallback model for a fixed
  budget; fit a line to log val NLL vs log `N`. Discuss why our exponent says little about
  frontier models (tiny range, one corpus, many epochs).
- **9.4** **Bias–variance, the interpolation threshold, double descent.** Zhang et al.
  (2016): networks memorize random labels, so classical capacity bounds are vacuous.
  Belkin et al. (2019): the U-curve is the left half; test error **peaks at the
  interpolation threshold** (`N ≈ n`) and descends again beyond it, as the learning
  algorithm picks the minimum-norm interpolant. Nakkiran et al. (2019): model-wise,
  epoch-wise, sample-wise. Exercise (CPU, 20 lines of numpy): random-features regression
  with the pseudoinverse; sweep the feature count through `n`; see the peak — the
  ill-conditioned square system — and watch label noise make it taller.
- **9.5** **What it means for post-training.** Why "bigger keeps working" let base models
  get good enough that post-training could be mostly *selection* (the tilt); reward-model
  over-optimization has its own fitted scaling forms (Gao et al.); test-time compute is a
  new axis (Phase 11.3).

## Phase 10 — Putting It Together
- **10.1** **The map.** Two axes: **trust** (where the reward comes from: game outcome,
  verifier, AI judge, learned RM, demonstrations only) × **optimizer** (sampling /
  best-of-n, on-policy PG — REINFORCE, PPO, GRPO — closed-form offline — DPO family —
  search + distillation). Place DQN, AlphaGo, AlphaZero, InstructGPT, CAI, DPO, IPO,
  KTO, Toolformer, best-of-n and GRPO, and say where each one's leash is.
- **10.2** **Capstone — post-train the through-line model.** Tiered, no GPU required:
  - **(a) CPU (default).** The full pipeline on the character model: SFT (two-line
    convention) → gold meter reward and a learned RM → PPO-lite `β` sweep (the
    reward-vs-KL frontier, with best-of-n) → DPO at matched KL → over-optimization curve
    (gold vs proxy). One-page "post-training report" with the frontier plot and one
    reward-hacking exhibit, annotated.
  - **(b) Colab GPU.** Tier a, plus a real model with Hugging Face **TRL**: SFT and DPO on
    a small open model (a few hundred million parameters) with a small public preference
    set, or GRPO with an exact-match verifier on grade-school math. Use an instruct LM as
    the Phase 8.2 judge. (Check the current TRL docs; the API moves fast.)
  - **(c) Local GPU.** Tier b, plus LoRA/QLoRA on a 1–3B model; an RLVR run with a tool
    in the loop; or reward-model over-optimization at real scale; or a music/audio reward
    (the synth-matching GRPO papers in Phase 11.5).
- **10.3** **Where to go next.** You can now read InstructGPT §3, the DPO derivation, the
  PPO and GAE papers, DeepSeekMath's GRPO section and the R1 report. Sutton & Barto for
  RL depth; [`ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) for the history;
  [`audio-synth-effect-matching/`](../audio-synth-effect-matching/) for RL inside audio
  inverse problems.

## Phase 11 — The Frontier (a living section)
> **This phase tracks the moving edge of the field and is revised as it moves** — treat it
> as depth-on-demand, not a gate. Everything here still sits on the keystone: the same
> objective, a different reward source (a verifier), a different optimizer (critic-free
> group baselines), or a different place to spend compute (test time). Pin each to the
> same meter model. Be honest that the empirical claims below are young, often from
> single labs' reports, and contested — when in doubt, read the linked paper, and update
> this section.

- **11.1** **RL with verifiable rewards (RLVR) and GRPO.** Replace the learned RM with a
  program that checks the answer (math exact-match, unit tests): the trust axis moves
  toward "game". **GRPO** (DeepSeekMath, Shao et al. 2024) drops PPO's critic: sample a
  *group* of `G` completions per prompt, advantage `A_i = (r_i − mean)/std` within the
  group, PPO clip, KL to `π_ref` as a loss term — REINFORCE with a group baseline (compare
  RLOO, Ahmadian et al. 2024). **DeepSeek-R1** (2025): R1-Zero runs RLVR straight from a
  base model and long chains of thought lengthen on their own; R1 adds a cold-start SFT.
  "RLVR" as a name: Tülu 3 (Lambert et al. 2024). Recipe refinements: DAPO (2025:
  decoupled clip, dynamic sampling, token-level loss, **no KL term** — the leash removed
  because the reward is trusted). **Pin:** turn PPO-lite into GRPO (G = 8 completions per
  prompt) on the meter reward — and note that our verifier *is* hackable: **verifiable ≠
  unhackable**. *Flags:* the "aha moment" framing is contested (Liu et al. 2025 find
  self-reflection already in base models and a length bias in GRPO's normalization);
  whether RLVR teaches new reasoning or re-weights what the base model already samples is
  debated (Yue et al. 2025 report base models catch up at large pass@k) — the keystone's
  "support cannot grow" theorem is the right lens, with its caveats.
- **11.2** **Process vs outcome rewards.** Reward the final answer (outcome) or each step
  (process). Uesato et al. (2022) and Lightman et al. (2023, *Let's Verify Step by Step*,
  PRM800K): process supervision helps reliability on math. But the R1 report found
  learned PRMs hard to scale and prone to hacking, and outcome-reward RLVR won out there.
  **Pin:** per-line meter reward (process) vs whole-completion reward (outcome) — which
  learns faster, and why? (Credit assignment again: Phase 2.3's variance story.)
- **11.3** **Test-time compute.** Spend compute at inference instead of in parameters:
  chain of thought (Wei et al. 2022), self-consistency (Wang et al. 2022), best-of-n with a
  verifier, sequential revision; Snell et al. (2024) on when test-time compute beats a
  bigger model; OpenAI's o1 (2024) and R1-style long reasoning; s1's budget forcing
  (Muennighoff et al. 2025). Search at decision time returns — AlphaZero's lesson (Phase
  3.4), though mostly as long sampled reasoning rather than MCTS (R1 reports MCTS attempts
  did not pan out). **Pin:** best-of-n vs `n` for the meter model is a test-time-scaling
  curve; extend 6.3 to `n = 64` and fit reward vs `log n`.
- **11.4** **Agentic tool-use RL.** Toolformer (8.3) was self-supervised; 2025 systems put
  the tool *inside* the RL rollout — search engines (Search-R1), code interpreters
  (ReTool), software-engineering environments scored by tests (SWE-bench as the yardstick,
  Jimenez et al. 2023) — and the reward is the task outcome over a multi-turn episode: the
  MDP of Phase 1 for real. New hacks: special-casing tests, editing the grader; monitoring
  the chain of thought for them (Baker et al. 2025) and the risk that penalizing such
  thoughts teaches concealment. **Pin:** let the meter model call the 8.4 search tool
  during RL rollouts; does the policy learn to copy ten-syllable lines from the corpus? (It
  should — and that is reward hacking with a tool.)
- **11.5** **RL post-training reaches audio (cross-track).** The same machinery in the
  `music423-2023` collection: GRPO-fine-tuned synth inverters scored on rendered audio
  (DDSynth-RL, ISMIR 2026; AutoSynth, 2026), SynthRL's REINFORCE (2025), and ACE-Step 1.5's
  "intrinsic" GRPO for controllability (2026). Reward = an audio-similarity metric; the
  trust axis and the hacks (metric gaming, in-domain degradation) are the same story.
  *Flag:* recent, single-group results.

### Frontier sources (Phase 11 — a living list, updated as the field moves)

These track the current edge and *will* be added to / reordered as the field moves;
treat them as the reading behind Phase 11, not a fixed canon. Items without an arXiv ID
are cited by title, authors and year only.

- **11.1 — RLVR / GRPO.** Shao et al. (2024), *DeepSeekMath: Pushing the Limits of
  Mathematical Reasoning in Open Language Models* (introduces GRPO), arXiv:2402.03300;
  DeepSeek-AI (2025), *DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via
  Reinforcement Learning*, arXiv:2501.12948; Lambert et al. (2024), *Tülu 3: Pushing
  Frontiers in Open Language Model Post-Training*, arXiv:2411.15124; Ahmadian et al.
  (2024), *Back to Basics: Revisiting REINFORCE-Style Optimization for Learning from Human
  Feedback in LLMs* (RLOO), arXiv:2402.14740; Yu et al. (2025), *DAPO: An Open-Source LLM
  Reinforcement Learning System at Scale*, arXiv:2503.14476; Liu et al. (2025),
  *Understanding R1-Zero-Like Training: A Critical Perspective* (Dr. GRPO),
  arXiv:2503.20783; Yue et al. (2025), *Does Reinforcement Learning Really Incentivize
  Reasoning Capacity in LLMs Beyond the Base Model?*, arXiv:2504.13837.
- **11.2 — process vs outcome.** Uesato et al. (2022), *Solving Math Word Problems with
  Process- and Outcome-Based Feedback*, arXiv:2211.14275; Lightman et al. (2023), *Let's
  Verify Step by Step*, arXiv:2305.20050.
- **11.3 — test-time compute.** Wei et al. (2022), *Chain-of-Thought Prompting Elicits
  Reasoning in Large Language Models*, arXiv:2201.11903; Wang et al. (2022),
  *Self-Consistency Improves Chain of Thought Reasoning in Language Models*,
  arXiv:2203.11171; Snell et al. (2024), *Scaling LLM Test-Time Compute Optimally Can Be
  More Effective than Scaling Model Parameters*, arXiv:2408.03314; Muennighoff et al.
  (2025), *s1: Simple Test-Time Scaling*, arXiv:2501.19393; OpenAI (2024), *Learning to
  Reason with LLMs* (o1; blog post and system card).
- **11.4 — agentic tool-use RL.** Yao et al. (2022), *ReAct: Synergizing Reasoning and
  Acting in Language Models*, arXiv:2210.03629; Jimenez et al. (2023), *SWE-bench: Can
  Language Models Resolve Real-World GitHub Issues?*, arXiv:2310.06770; Jin et al. (2025),
  *Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement
  Learning*, arXiv:2503.09516; Feng et al. (2025), *ReTool: Reinforcement Learning for
  Strategic Tool Use in LLMs*, arXiv:2504.11536; Baker et al. (2025), *Monitoring
  Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation* (OpenAI),
  arXiv:2503.11926.
- **11.5 — audio.** Wu et al. (2026), *DDSynth-RL: Audio Synthesizer Inversion via
  Discrete Diffusion with Reinforcement Learning*, ISMIR 2026, arXiv:2608.03032; Wu et al.
  (2026), *AutoSynth: Learning to Generate Editable Synthesizer Programs from Audio and
  Text*, arXiv:2610.10774; Shin & Lee (2025), *SynthRL: Cross-domain Synthesizer Sound
  Matching via Reinforcement Learning*, IJCAI 2025 (no arXiv); Gong et al. (2026),
  *ACE-Step 1.5*, arXiv:2602.00744. (Summaries in the collection's
  `synth-effect-matching/wiki/` and `ai-music-audio-gen/wiki/sources/ace-step.md`.)

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. The
   recurring picture is the **reward-vs-KL plane**: every method is a point or a curve on
   it, and the leash is how far right you are allowed to go. The recurring analogy for a
   DSP learner: the tilt `π_ref · exp(r/β)` is posterior = prior × likelihood; `β` is the
   regularization weight; RL is a noisy stochastic-gradient loop that needs the same care
   as an adaptive filter.
3. **Pin it to the model.** The meter model is the worked example. Every method is run on
   it, and the learner **reads the samples** — the eye is this course's oracle: a reward
   curve that looks great with degenerate samples underneath is the lesson, not a bug.
4. **Tiny exercise** to verify: derive a line, predict a curve before running it, compute
   a KL by hand, or run a few lines of PyTorch. The exercise *is* the check.
5. **Common misreadings** when relevant — keep
   [`the-reward-and-the-leash.md`](the-reward-and-the-leash.md)'s list live; flag and
   correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences ("the leashed optimum is the reference tilted
   by `exp(r/β)`; DPO is that statement substituted into Bradley–Terry").
2. Carry out the small task: derive the gradient or the optimum, run the method on the
   meter model, or place it on the reward-vs-KL plot — and explain the result.
3. Spot a deliberately wrong claim ("PPO's clip is the KL penalty" — no, a different
   leash; "DPO can't reward-hack" — it has an implicit reward; "AlphaZero used PPO" — it
   distils MCTS).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the paper collection this course teaches from
This course is the *pedagogical* front-end of JOS's curated paper collection
[`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023) (branch `master`); the
collection stays canonical, the course stays pedagogical. Read / link these on JOS's
machine (`/w/music423-2023/`):

- **[`reinforcement-learning/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/reinforcement-learning)**
  — the RL papers (DQN: the 2013 workshop paper `DQN-1312.5602.pdf` and the 2015 *Nature*
  paper `DQN-Nature-2015.pdf`; AlphaGo, AlphaZero, InstructGPT); a README, no wiki. The
  target network is in the *Nature* paper only.
- **[`ai-2012-to-2023/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-2012-to-2023/wiki)**
  — concept pages `rl-and-alignment-arc.md` (games → alignment), `scaling-and-emergence.md`
  (Kaplan → GPT-3 → Chinchilla → emergence debate), `pretrain-finetune-lineage.md` (the
  three-stage stack); landmark notes `notes/instructgpt.md`, `notes/cot-prompting.md`.
  The directory also holds the Constitutional AI, Toolformer, Kaplan, Chinchilla and CoT
  PDFs. `rl-and-alignment-arc.md` was corrected in Oct 2026 on three points worth keeping
  live: AlphaZero was not trained with PPO; DPO's wide adoption is in cheap open
  fine-tuning, not frontier on-policy RL; "MCTS did not carry" is partly revised by
  test-time compute. An older copy may still carry the original errors.
- **[`double-descent/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/double-descent/wiki)**
  — `overview.md`, `double-descent.md`, `interpolation-threshold.md`,
  `bias-variance-tradeoff.md`, and `sources/` (Zhang 2016/2021, Belkin, Nakkiran).
- **[`synth-effect-matching/wiki/reinforcement-learning-sound-matching.md`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/synth-effect-matching/wiki/reinforcement-learning-sound-matching.md)**
  — the audio-side RL / GRPO thread (Phase 11.5).
- Keep the course in sync if the collection gains papers (an `alignment/` directory is
  anticipated in its README); the collection is canonical, the course is the lesson plan
  over it.

### Source papers (the landmarks this course tracks)
- **Sutton & Barto (2018)** — *Reinforcement Learning: An Introduction*, 2nd ed. (free
  online). The textbook for Phases 1–2.
- **Williams (1992)** — *Simple Statistical Gradient-Following Algorithms for
  Connectionist Reinforcement Learning* (REINFORCE). *Machine Learning* 8:229–256.
- **Mnih et al. (2013)** — *Playing Atari with Deep Reinforcement Learning*.
  arXiv:1312.5602. **Mnih et al. (2015)** — *Human-Level Control through Deep
  Reinforcement Learning*. *Nature* 518:529–533.
- **Schulman et al. (2015)** — *Trust Region Policy Optimization*. arXiv:1502.05477.
- **Schulman et al. (2015)** — *High-Dimensional Continuous Control Using Generalized
  Advantage Estimation*. arXiv:1506.02438.
- **Mnih et al. (2016)** — *Asynchronous Methods for Deep Reinforcement Learning* (A3C).
  arXiv:1602.01783.
- **Schulman et al. (2017)** — *Proximal Policy Optimization Algorithms*.
  arXiv:1707.06347.
- **Silver et al. (2016)** — *Mastering the Game of Go with Deep Neural Networks and Tree
  Search* (AlphaGo). *Nature* 529:484–489.
- **Silver et al. (2017)** — *Mastering Chess and Shogi by Self-Play with a General
  Reinforcement Learning Algorithm* (AlphaZero). arXiv:1712.01815.
- **Schrittwieser et al. (2020)** — *Mastering Atari, Go, Chess and Shogi by Planning
  with a Learned Model* (MuZero). arXiv:1911.08265.
- **Bradley & Terry (1952)** — *Rank Analysis of Incomplete Block Designs*. *Biometrika*
  39:324–345.
- **Christiano et al. (2017)** — *Deep Reinforcement Learning from Human Preferences*.
  arXiv:1706.03741.
- **Ziegler et al. (2019)** — *Fine-Tuning Language Models from Human Preferences*.
  arXiv:1909.08593.
- **Stiennon et al. (2020)** — *Learning to Summarize from Human Feedback*.
  arXiv:2009.01325.
- **Ouyang et al. (2022)** — *Training Language Models to Follow Instructions with Human
  Feedback* (InstructGPT). arXiv:2203.02155.
- **Bai et al. (2022)** — *Training a Helpful and Harmless Assistant with Reinforcement
  Learning from Human Feedback*. arXiv:2204.05862.
- **Bai et al. (2022)** — *Constitutional AI: Harmlessness from AI Feedback*.
  arXiv:2212.08073.
- **Lee et al. (2023)** — *RLAIF vs. RLHF: Scaling Reinforcement Learning from Human
  Feedback with AI Feedback*. arXiv:2309.00267.
- **Gao, Schulman & Hilton (2022)** — *Scaling Laws for Reward Model Overoptimization*.
  arXiv:2210.10760.
- **Korbak, Perez & Buckley (2022)** — *RL with KL Penalties is Better Viewed as Bayesian
  Inference* (the tilt as a posterior). arXiv:2205.11275.
- **Rafailov et al. (2023)** — *Direct Preference Optimization: Your Language Model is
  Secretly a Reward Model*. arXiv:2305.18290.
- **Azar et al. (2023)** — *A General Theoretical Paradigm to Understand Learning from
  Human Preferences* (IPO). arXiv:2310.12036.
- **Ethayarajh et al. (2024)** — *KTO: Model Alignment as Prospect Theoretic
  Optimization*. arXiv:2402.01306.
- **Hong et al. (2024)** — *ORPO: Monolithic Preference Optimization without Reference
  Model*, arXiv:2403.07691; **Meng et al. (2024)** — *SimPO: Simple Preference
  Optimization with a Reference-Free Reward*, arXiv:2405.14734.
- **Schick et al. (2023)** — *Toolformer: Language Models Can Teach Themselves to Use
  Tools*. arXiv:2302.04761.
- **Kaplan et al. (2020)** — *Scaling Laws for Neural Language Models*. arXiv:2001.08361.
- **Hoffmann et al. (2022)** — *Training Compute-Optimal Large Language Models*
  (Chinchilla). arXiv:2203.15556.
- **Zhang et al. (2016)** — *Understanding Deep Learning Requires Rethinking
  Generalization*. arXiv:1611.03530.
- **Belkin et al. (2019)** — *Reconciling Modern Machine-Learning Practice and the
  Classical Bias–Variance Trade-Off*. arXiv:1812.11118.
- **Nakkiran et al. (2019)** — *Deep Double Descent: Where Bigger Models and More Data
  Hurt*. arXiv:1912.02292.
