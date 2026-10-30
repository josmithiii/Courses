# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Finished `ai-sequence-models/` (course 2)? _(yes — checkpoint at: ___ / partly / no — use the Phase 0 fallback model)_
- ML background (Transformers/LLMs from `ai-foundations`): _(shaky / comfortable / strong)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- RL background: _(none / some — Bellman, Q-learning / strong — policy gradients, PPO; can test out of Phases 1–2)_
- Probability comfort (expectations, KL divergence, log-likelihood): _(rusty / comfortable / strong)_
- Signal-processing / control background (analogies to lean on): _(none / some / strong)_
- Why they're here / goal: _(understand how assistants are made / run RLHF/DPO themselves / read the reasoning-model papers / research)_
- Lean: _(derivation-first / code-first / both)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Working directory for their code and checkpoints (never inside the repo): _( )_
- Time budget: ~1 hour/day
- Style: patient, friendly, **derive-then-run**, every symbol defined on first use, every
  method run on the one through-line model and its samples *read* before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-reward-and-the-leash.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `uv` project with a `.venv`; `torch`, `numpy`, `matplotlib` importable
- [ ] `gymnasium` installed (CartPole for Phases 1–2)
- [ ] The corpus resolves at `assets/ai-llms-and-sequence-models/tinyshakespeare.txt` **and its SHA-256 matches**
- [ ] Starting model chosen and recorded: _(course-2 checkpoint — contract checked / fallback model trained, learner told)_
- [ ] Plumbing works: `sample`, `completion_logps`, `exact_kl` (Phase 0.3)
- [ ] `the-reward-and-the-leash.md` read (the keystone)
- [ ] (capstone tier b) Colab with `transformers` + `trl` (+ `peft`) importable
- [ ] A scratch `.py` file or notebook open and used during sessions

## Numbers we reuse
> Filled in as we compute them; keep consistent across lessons. Canonical reference values
> are in `through-line-lab.md`; record the learner's own here.

- Corpus: 1,115,394 chars, 65-char vocabulary, 90/10 split, SHA-256 verified on _( )_.
- Starting model: _(course-2 checkpoint / fallback)_, params _( )_, val NLL _( )_ nats/char.
- Meter reward of SFT samples _( )_; corpus two-line turns 0.667 (reference).
- SFT format rate: before _( )_ → after _( )_; general val NLL before _( )_ → after _( )_.
- Best-of-n mean reward at n = 1/4/16: _( )_.
- `β` sweep endpoints (reward, KL): `β=0` _( )_, `β=0.03` _( )_, `β=0.1` _( )_.
- DPO (reward, KL): _( )_.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has produced themselves, kept as reference. Add a one-line
> entry each session (these are what a stalled learner keeps). Paste the best
> reward-hacking samples verbatim.

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-reward-and-the-leash.md`). The tutor
> watches for these, notes when one comes up, and revisits later to make sure it has stuck.

- "The KL penalty is ordinary regularization against overfitting" — it is a distance from the reference *policy*, on the policy's own samples
- "PPO's clip is the KL leash" — two leashes: clip ↔ `π_old` per update; KL ↔ `π_ref` over the run
- "`β` is a learning rate" — it is the temperature of the tilt `π_ref · exp(r/β)`
- "Higher reward = better model" — against a proxy, gold reward rises then falls (Goodhart)
- "DPO has no reward model, so it can't reward-hack" — it has an implicit one, and only sees its pairs
- "DPO optimizes a different objective" — same objective, closed form, *under assumptions*
- "RLHF teaches new knowledge" — the leashed optimum re-weights `π_ref`; support can't grow
- "Best-of-n isn't alignment" — same tilt, at sampling time, KL ≤ log n − (n−1)/n
- "A verifiable reward can't be hacked" — our meter counter is a verifier
- "AlphaZero used PPO" — it distils MCTS visit counts (the source wiki says otherwise)
- "SFT and RLHF minimize the same KL" — forward (mode-covering) vs reverse (mode-seeking)
- "Scaling laws are laws of nature" — empirical fits over finite ranges
- "Double descent means overfitting is a myth" — the peak is real; noise makes it, ridge removes it
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 10.2) — tiered, no GPU required
> Picked partway through Phase 6 so it can shape the last few lessons.

- _(a) **CPU** — the full pipeline on the character model: SFT → gold reward + learned RM → PPO-lite β sweep with best-of-n (the reward-vs-KL frontier) → DPO at matched KL → gold-vs-proxy over-optimization; one-page post-training report with one annotated reward-hacking exhibit_
- _(b) **Colab GPU** — tier a, plus TRL on a small open model: SFT + DPO on a small public preference set, or GRPO with an exact-match verifier on grade-school math; an instruct LM as the Phase 8.2 judge_
- _(c) **Local GPU** — tier b, plus LoRA/QLoRA on a 1–3B model, an RLVR run with a tool in the loop, RM over-optimization at real scale, or an audio reward (the synth-matching GRPO thread)_
- Choice: _(not yet)_
