# The Reward and the Leash — This Course's Keystone

A pretrained language model is a *reference distribution* `π_ref(y | x)`: given a prompt
`x`, it puts probability on every possible continuation `y`. Post-training wants to move
that distribution toward continuations people (or a program) prefer — without wrecking
everything the model already knows. The whole course is one objective and one question
about it:

> **Climb a reward `r(x, y)` while a leash keeps the policy near the reference:**
>
> `J(π) = E_{x, y~π(·|x)}[ r(x, y) ]  −  β · KL( π(·|x) ‖ π_ref(·|x) )`
>
> **How much should you trust the reward — and how do you reach the optimum?**

`π` (the **policy**) is the model being post-trained, `r` is the **reward** (a learned
reward model `r_φ`, an AI judge, or a program), `β > 0` is the **leash strength**, and
`KL(π ‖ π_ref) = E_{y~π}[ log π(y|x) − log π_ref(y|x) ]` is the Kullback–Leibler divergence
of the policy *from* the reference, measured on the policy's own samples. Read this in
Phase 0.1, then return to it in **Phase 6** (derive the optimum), **Phase 7** (DPO falls out
of it), and **Phase 10.1** (place every method on the map).

Every term in **bold** is earned somewhere in the syllabus; the phase is in brackets.

---

## The one equation: the optimum is a tilted reference [Phase 6.2]

For each prompt `x`, over *all* distributions on continuations, `J` has a unique maximizer:

```
π*(y | x) = π_ref(y | x) · exp( r(x, y) / β ) / Z(x),      Z(x) = Σ_y π_ref(y | x) · exp( r(x, y) / β )
```

*Proof in one line:* `J(π) = −β · KL(π ‖ π*) + β · log Z(x)`, and KL ≥ 0 with equality
only at `π = π*`. This is a **theorem** (the Gibbs variational principle), exact for any
reward, *provided* the policy can represent any distribution over continuations.

What the equation says, read the way a signal-processing person reads a transfer function:

- **`π*` is a reweighting of `π_ref`.** The reward multiplies the prior; nothing else
  changes. Prior × likelihood ÷ evidence — `π*` is the Bayesian posterior with
  `exp(r/β)` as the likelihood (Korbak, Perez & Buckley 2022).
- **`β` is a temperature, not a learning rate.** `β → ∞`: `π* → π_ref` (the leash wins;
  nothing moves). `β → 0`: `π*` collapses onto `argmax_y r` (the reward wins; whatever the
  reward's blind spots are, the policy finds them). In between, `β` sets how far the
  reward is allowed to drag the model.
- **The support cannot grow.** Where `π_ref(y|x) = 0`, `π*(y|x) = 0`. The optimal leashed
  policy can only *re-weight* behaviours the reference already produces. (How this exact
  statement softens in practice — finite models, approximate optimization, and the 2025
  debate over whether RL "teaches new reasoning" — is a Phase 11 topic.)
- **Any policy defines an implicit reward.** Invert the equation:
  `r(x, y) = β · log[ π*(y|x) / π_ref(y|x) ] + β · log Z(x)`. Every fine-tuned model *is*
  a reward model, up to a prompt-dependent constant. This is the door DPO walks through.
- **The best achievable value is a soft-max.** `J(π*) = β · log E_{y~π_ref}[ exp(r/β) ]` —
  between the mean reward under the reference (`β → ∞`) and its maximum (`β → 0`).

## Why a leash at all? Because the reward is a proxy [Phases 3, 5, 6]

In **Go** the reward is the rules of the game: a win is a win. AlphaZero needs no leash —
there is nothing to hack [Phase 3]. In language the reward is a **proxy**: a reward model
fit to a few tens of thousands of human comparisons, an AI judge reading a constitution,
or a program that checks something checkable. Push hard enough on any proxy and the policy
finds the places where the proxy and the truth disagree — **reward hacking**, Goodhart's
law in action [Phase 5.4]. The leash is how much you *distrust* the reward:

| Reward source | How hackable | Typical leash |
|---|---|---|
| Game outcome (AlphaZero) | not at all — it *is* the goal | none |
| Learned reward model from human preferences (InstructGPT) | very — finite data, off-distribution errors | explicit `β · KL` to the SFT model (InstructGPT: `β = 0.02`) |
| AI feedback against a constitution (CAI / RLAIF) | about as much as the judge's blind spots | same as RLHF |
| Program / verifier (math answers, unit tests — RLVR) | less, **but not zero** | often small; some recipes drop the KL term entirely |
| Our meter counter (this course) | very, and visibly — that is the point | the `β` sweep is the experiment |

## Every method is a way to reach (or approximate) the tilt [the map]

| Method | Where `r` comes from | How it gets to `π_ref · exp(r/β)` | Where the leash lives |
|---|---|---|---|
| **SFT** [Phase 4] | no reward — demonstrations | it doesn't: it *moves `π_ref` itself* (max likelihood = minimize forward `KL(p_demo ‖ π)`) | it *builds* the anchor the later leash attaches to |
| **Best-of-n** [Phase 6.3] | any scorer | at sampling time: draw `n` from `π_ref`, keep the best | implicit; `KL ≤ log n − (n−1)/n` |
| **REINFORCE / PPO (RLHF)** [Phases 2, 6] | learned RM `r_φ` | stochastic-gradient ascent on `J` (score-function gradients through samples) | `−β · log(π/π_ref)` folded into the reward |
| **PPO's clip** [Phase 2.4] | — | — | a *second, different* leash: each update stays near `π_old` (a trust region), not near `π_ref` |
| **DPO / IPO / KTO …** [Phase 7] | preference pairs, no explicit RM | closed-form: substitute the implicit reward into Bradley–Terry; `Z(x)` cancels → a classification loss | `β` inside the loss; offline data only |
| **Constitutional AI / RLAIF** [Phase 8] | an AI judge + written principles | same as RLHF (or DPO) | same |
| **RLVR / GRPO** [Phase 11] | a verifier (program) | group-relative policy gradient, no critic | small or zero `β`; the clip remains |
| **AlphaGo / AlphaZero** (contrast) [Phase 3] | the game result | search (MCTS) proposes a better policy; the net distils it | none needed |

Two orthogonal knobs run through the table:
- **Where the reward comes from** — humans, an AI judge, a program, the world. This is the
  *trust* axis; it sets how long the leash should be.
- **How the optimum is reached** — sampling (best-of-n), on-policy gradients (PPO, GRPO),
  or closed-form reparameterization on fixed data (DPO). This is the *optimizer* axis.

## DPO in four lines [Phase 7.1]

1. Bradley–Terry preferences: `P(y_w ≻ y_l | x) = σ( r(x, y_w) − r(x, y_l) )`.
2. Implicit reward of a policy: `r = β · log(π/π_ref) + β · log Z(x)`.
3. Substitute — `Z(x)` cancels in the *difference*:
   `P(y_w ≻ y_l | x) = σ( β · [log π(y_w|x)/π_ref(y_w|x) − log π(y_l|x)/π_ref(y_l|x)] )`.
4. Maximize the likelihood of the observed preferences over `π` directly:
   `L_DPO = −E log σ( β · [Δ_w − Δ_l] )`, with `Δ = log π − log π_ref` summed over the
   continuation's tokens.

**What is a theorem and what is not.** *If* preferences really are Bradley–Terry in some
reward, *if* the policy class is unrestricted, and *if* the data cover the relevant
continuations, then the DPO minimizer equals the RLHF optimum `π*` for the reward that best
explains the data. In practice DPO trains **offline** on fixed pairs while PPO samples
**on-policy**; finite data and coverage break the equivalence, and which works better is an
**empirical, still-moving** question [Phase 7.4].

## The two KLs (and why RLHF loses diversity) [Phases 4, 6]

- **SFT** minimizes the *forward* KL `KL(p_demo ‖ π)`: it must cover every demonstration,
  so it is **mode-covering**.
- The **RLHF objective** uses the *reverse* KL `KL(π ‖ π_ref)`, evaluated on the policy's
  own samples: the policy is free to drop modes of `π_ref` as long as what it keeps is
  likely under `π_ref`. It is **mode-seeking** — and the reward pushes it toward the
  highest-scoring modes. Lost diversity is the expected result, not a bug.
- **AlphaGo saw this in 2016**: its stronger RL policy made a *worse* prior for tree
  search than the supervised one, "presumably because humans select a diverse beam of
  promising moves, whereas RL optimizes for the single best move" [Phase 3.1].

---

## The misreadings this course exists to kill

The tutor flags each on the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "The KL penalty is ordinary regularization against overfitting the training set." | It is a distance **in distribution space** from the reference policy, measured on the policy's own samples. It protects against exploiting the reward's errors and keeps fluency and diversity. | Phase 6.1 |
| "PPO's clipping *is* the KL leash." | Two leashes. The clip keeps each update near `π_old` (optimizer stability, a trust region). The KL keeps the whole run near `π_ref` (part of the objective). Remove one and you get a different failure. | Phase 2.4, 6.4 |
| "`β` is a learning rate." | `β` is the **temperature** of the tilt `π_ref · exp(r/β)`: it changes the *target*, not the step size. | Phase 6.2 |
| "Higher reward means a better model." | Only if the reward is the truth. Against a proxy, **gold reward rises then falls** as the policy moves away from the reference (Gao et al. 2022) — reward hacking. | Phase 5.4, 6.5 |
| "DPO has no reward model, so it cannot reward-hack." | DPO has an **implicit** reward `β · log(π/π_ref)`; it over-optimizes too, and it only ever sees the pairs in its data. | Phase 7.2 |
| "DPO optimizes a different objective from RLHF." | Same KL-regularized Bradley–Terry objective, solved in closed form — **under assumptions** (BT, unrestricted policy, coverage). The practical differences (offline vs on-policy, finite data) are where they part. | Phase 7.1–7.2 |
| "RLHF teaches the model new knowledge." | The leashed optimum is a **re-weighting** of `π_ref`; it cannot put mass where the reference has none. Post-training mostly selects behaviours the base model can already produce. (The RLVR "new reasoning?" debate is Phase 11.) | Phase 6.2 |
| "Best-of-n isn't alignment — nothing is trained." | It is the same tilt approximated at sampling time, a strong baseline, with a known KL cost `≤ log n − (n−1)/n`. | Phase 6.3 |
| "A verifiable reward can't be hacked." | Our meter counter is a verifier and is hacked within minutes; code RL special-cases unit tests. **Verifiable ≠ unhackable.** | Phase 5.4, 11.1 |
| "AlphaZero was trained with PPO." | No (and the `ai-2012-to-2023` wiki says otherwise — correct it). AlphaZero distils **MCTS visit counts** into the policy (cross-entropy) and regresses the value on game outcomes. AlphaGo's RL policy used a REINFORCE-style policy gradient. PPO (2017) is OpenAI's — OpenAI Five, InstructGPT. | Phase 3.2 |
| "The reward model *is* human judgment." | It is a learned **proxy** fit to finite comparisons under a Bradley–Terry assumption (one scalar utility, transitive preferences). InstructGPT's own labelers agreed with each other only 72.6 ± 1.5% of the time (held-out labelers 77.3 ± 1.3%). | Phase 5.2 |
| "SFT and RLHF minimize the same KL." | SFT: forward `KL(p_demo ‖ π)`, mode-covering. RLHF: reverse `KL(π ‖ π_ref)` plus reward, mode-seeking. Hence RLHF's diversity loss. | Phase 4.1, 6.6 |
| "Scaling laws are laws of nature." | **Empirical power-law fits** over finite ranges. Kaplan and Chinchilla disagree on the compute-optimal ratio partly because of fitting methodology. | Phase 9.1–9.2 |
| "Double descent means overfitting is a myth." | The test-error **peak at the interpolation threshold is real**; label noise amplifies it and regularization can remove it. Over-parameterization helps *past* the peak. | Phase 9.4 |

---

## How the course earns the leash

| Piece | Earned in |
|---|---|
| the RL vocabulary: policy, return, value, Bellman, Q-learning → DQN | **Phase 1** |
| policy gradients through samples: REINFORCE, baselines, GAE, PPO's clip | **Phase 2** |
| search as policy improvement; a reward you can't hack (AlphaGo → AlphaZero) | **Phase 3** |
| SFT builds the anchor `π_ref` | **Phase 4** |
| rewards from preferences (Bradley–Terry); reward hacking | **Phase 5** |
| the KL-regularized objective, its closed-form optimum, best-of-n, PPO-lite, the `β` sweep | **Phase 6** (keystone) |
| DPO as the closed form of the same objective; its family | **Phase 7** (keystone) |
| where the reward comes from: AI feedback; tools in the loop | **Phase 8** |
| why bigger keeps working: scaling laws, double descent | **Phase 9** (sidebar) |
| the full trust × optimizer map | **Phase 10.1** |
| verifiable rewards, GRPO, process rewards, test-time compute | **Phase 11** (frontier) |
