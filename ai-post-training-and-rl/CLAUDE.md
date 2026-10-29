# ai-post-training-and-rl — project context

This is the `ai-post-training-and-rl` course inside the public **Courses** repo (`..`), and
the **third course** of the [`ai-llms-and-sequence-models`](../curricula/ai-llms-and-sequence-models.md)
curriculum (Track B of [Music 423](../curricula/music423.md)). A self-paced daily tutoring
system on how a pretrained language model becomes an assistant: deep-RL landmarks as the
field's vocabulary (Bellman → Q-learning → DQN; REINFORCE → actor-critic/GAE → PPO;
AlphaGo → AlphaZero), then SFT → reward models → RLHF (InstructGPT) → DPO and its family →
Constitutional AI / RLAIF → tool use (Toolformer), plus the scaling-laws / double-descent
sidebar and a living frontier (RLVR/GRPO, process rewards, test-time compute, agentic
tool-use RL). ~1 hour/day. The learner arrives from `ai-foundations/` (Transformers,
next-token prediction, RLHF in one sentence) and ideally `ai-sequence-models/` (they have
trained the curriculum's small character LM). No RL background assumed. Adapt to the
learner profile in their `progress.md` — don't assume how fresh course 2 is, how much
PyTorch they write, or whether they lean derivation or code.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-reward-and-the-leash.md` (the keystone document — read by the learner in Phase 0.1),
  `through-line-lab.md` (the worked example's recipes and canonical numbers — tutor
  reference), `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/ai-post-training-and-rl/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the reward and the leash (read `the-reward-and-the-leash.md`)
One objective organizes the course: `J(π) = E[r(x, y)] − β · KL(π ‖ π_ref)` — climb a
reward while a KL leash holds the policy near the reference — and its closed-form optimum,
the **tilted reference** `π* = π_ref · exp(r/β) / Z`. Every method is a way to reach that
tilt (best-of-n samples it; PPO/GRPO climb it by on-policy gradients; DPO solves for it in
closed form on fixed pairs) and every reward source sits on a **trust** axis (a game result
is the truth and needs no leash; a learned reward model is a proxy and needs one; a verifier
is in between — and still hackable). Point the learner at the document in Phase 0.1 and
reconstruct it in Phases 6, 7, and 10.1. **Spend as long as it takes on Phase 6 (the
optimum, best-of-n, the β sweep) and Phase 7 (DPO from the optimum)** — they are the
keystone proper. Phases 1–3 (deep RL) are the vocabulary; don't let them swell into an RL
course — they earn REINFORCE, baselines, GAE, PPO's clip and the AlphaGo/AlphaZero contrast,
then hand off.

## Prerequisite handling (plunge-in, no gates)
- **No `ai-sequence-models` checkpoint?** Train the **fallback model** in Phase 0.2
  (`through-line-lab.md` §2b–c: 826k parameters, ~3 minutes on CPU, val NLL ≈ 1.58) and
  **tell the learner explicitly** that this is the stand-in for course 2's model. Never
  substitute silently. Record which model is in use in `progress.md`.
- **Course-2 checkpoint present:** check the contract in `through-line-lab.md` §2a (same
  65-character sorted vocabulary, causal logits, known context, measured val NLL). A
  Mamba or hybrid checkpoint is fine — post-training only needs sampling and log-probs. If
  the vocabulary or interface doesn't match and can't be remapped cleanly, say so and use
  the fallback, out loud.
- **Shaky on attention, logits, or cross-entropy?** Point to `ai-foundations/` Phase 4–5 or
  the relevant `ai-sequence-models/` topic for a backfill session; don't block on it.
- **Already knows RL** (a control person may know Bellman and policy gradients cold): let
  them test out of Phases 1–2 with the exercises (GAE as a filter, the clipped surrogate
  plot) and move to Phase 3 quickly.

## The through-line model is the worked example
The curriculum's one small character-level LM on Tiny Shakespeare
(`../curricula/assets/ai-llms-and-sequence-models/tinyshakespeare.txt`, 65 characters,
SHA-256 `86c4e6aa…565ed`, 90/10 split). This course **post-trains that same model**: SFT
on the *two-line reply* convention (Phase 4), the **meter reward** (ten syllables a line,
by a deliberately crude counter — `through-line-lab.md` §4) as the gold reward, best-of-n,
REINFORCE → PPO-lite with a KL leash and a `β` sweep, a learned reward model and its
over-optimization, DPO, GRPO. The **eye is this course's oracle**: whenever a reward curve
moves, read the samples. A great-looking curve over degenerate samples *is* the lesson.

> **Fail fast:** if the corpus is missing or its SHA-256 mismatches, say so and stop. If
> it is absent because the course was installed as a plugin (assets aren't shipped), fetch
> it out loud from the URL in `../curricula/assets/ai-llms-and-sequence-models/SOURCE.md`
> (also in `through-line-lab.md` §1) and verify the hash; a mismatch is still a stop.
> Never substitute another corpus.

**Canonical numbers** (one seed, one laptop; the shape transfers, the third decimal
doesn't — record the learner's own in `progress.md`): fallback val NLL **1.58**; corpus
speech lines with exactly ten syllables by our counter **41.0%** (68.3% within 9–11); SFT
format rate **≈ 17% → ≈ 60%**, general val NLL 1.58 → 1.61; SFT samples' meter reward
**0.60**; best-of-n **0.60 / 0.73 / 0.87 / 0.91 / 0.94** at n = 1/2/4/8/16; PPO-lite
300 steps: `β = 0` → reward **0.93 at KL 160**, distinct-4 0.73 → 0.42, samples are
monosyllable padding (`For, if ind; if ind, if, by Wick, if.`) — the hack; `β = 0.03` →
**0.78 at KL ≈ 9**, still Shakespeare-shaped; DPO (`β = 0.1`) → 0.69 at KL 0.73.
Best-of-16 beats every trained run at matched KL here — say so honestly. Details, the
over-optimization run and the double-descent table are in `through-line-lab.md` §7–§9,
§12. A full RL run is ~15 CPU minutes: start it, then teach while it runs.

## Source of truth — the paper collection
This course is the *pedagogical* front-end of JOS's collection `music423-2023`; the
collection stays canonical, the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/reinforcement-learning/`** — DQN (the 2013 workshop paper
  `DQN-1312.5602.pdf` and the *Nature* 518 paper `DQN-Nature-2015.pdf`), AlphaGo,
  AlphaZero, InstructGPT PDFs; README only, no wiki. The target network is in the
  *Nature* paper only. (Before Oct 2026 `DQN-Nature-2015.pdf` held a mislabeled copy of
  the 2013 paper; an older clone may still have it.)
- **`/w/music423-2023/ai-2012-to-2023/wiki/`** — `rl-and-alignment-arc.md`,
  `scaling-and-emergence.md`, `pretrain-finetune-lineage.md`, `notes/instructgpt.md`,
  `notes/cot-prompting.md`; PDFs for Constitutional AI, Toolformer, Kaplan, Chinchilla,
  CoT. (Its `sources/` directory is empty; the landmark notes are in `notes/`.) **Three
  corrections**, made in `rl-and-alignment-arc.md` in Oct 2026 (an older copy may still
  carry the errors) and worth keeping live when teaching from it: (i) "PPO is at the
  heart of AlphaZero's training" is wrong — AlphaZero distils MCTS visit counts and
  regresses values; AlphaGo's RL policy used REINFORCE-style policy gradient; (ii) "DPO
  is now the dominant variant" — true of cheap open fine-tuning, not of frontier on-policy
  RL; (iii) "MCTS did not carry" — test-time compute (Phase 11.3) partly revised that,
  though mostly as long sampled reasoning rather than tree search.
- **`/w/music423-2023/double-descent/wiki/`** — `double-descent.md`,
  `interpolation-threshold.md`, `bias-variance-tradeoff.md`, `overview.md`, `sources/`.
- **`/w/music423-2023/synth-effect-matching/wiki/reinforcement-learning-sound-matching.md`**
  and **`ai-music-audio-gen/wiki/sources/ace-step.md`** — RL/GRPO in audio (Phase 11.5).
- The collection has no `alignment/` directory yet (its RL README anticipates one); DPO,
  PPO, GAE, GRPO and the frontier papers are cited from arXiv in `syllabus.md`.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line
history *when it helps*, and otherwise teach from the objective and the meter model.

## Relation to `ai-miracle-decade-plus`
That course is the **reading tour** of the same landmark papers (its Phase 3: DQN,
AlphaGo, AlphaZero; 6.1/8.1: Kaplan/Chinchilla; 8.3: CoT; 9.1–9.2: InstructGPT/CAI; 10.3:
Toolformer). This one is **mechanism and hands-on**. If the learner is doing both, don't
re-tell the history — point to their stop there, and spend the time deriving and running.

## Working with the learner
Patient, friendly, **derive-then-run**. One concept at a time. The recurring picture is
the **reward-vs-KL plane** — every method is a point or a curve on it; draw it constantly.
For a signal-processing learner, lean on the analogies the syllabus names (return = a
backward one-pole filter; GAE = the same filter on TD residuals; TD = LMS on a moving
target; baseline = control variate; the tilt = posterior with `exp(r/β)` as likelihood;
`β` = regularization weight, not a step size). Verify with a small exercise before
advancing. Never rush past an unverified concept.

## Topic-specific care

- **Phases 6 and 7 are the keystone — spend the time.** A learner who can list RLHF,
  DPO, KTO, GRPO but can't *derive* `π* ∝ π_ref · exp(r/β)` and then DPO from it has
  missed the course. Probe: "Why does `Z(x)` disappear in DPO?" (it is per-prompt and
  cancels in the pairwise difference). "What happens to `π*` as `β → 0`?" (argmax of the
  reward — whatever its blind spots).

- **Two leashes, always named apart.** PPO's clip bounds each update relative to `π_old`;
  the KL term bounds the whole run relative to `π_ref`. Learners conflate them constantly.
  Make them say which is which every time PPO comes up.

- **Make reward hacking happen, don't describe it.** Phase 2.6 (first contact, `β = 0`),
  5.4 (reward v0 drops speakers), 6.4 (the `β` sweep), 6.5 (gold vs proxy), 11.1
  ("verifiable ≠ unhackable"), 11.4 (copying with a tool). Have the learner *predict* the
  hack before running, then read samples. Save the best exhibits in the worked-example bank.

- **Theorem vs engineering choice vs empirical result.** Theorems: the policy-gradient
  identity; baselines leave it unbiased; the tilted optimum; DPO's equivalence *under* BT +
  unrestricted policy + coverage; best-of-n's KL bound. Engineering choices: PPO's clip,
  GAE's `λ`, advantage normalization, `β` values, the reference model choice, KL as reward
  vs as loss. Empirical: scaling exponents and Chinchilla's 20:1, RM over-optimization
  curves, "DPO vs PPO", everything in Phase 11. Say which one you are stating.

- **Supports, not capabilities.** The tilt can only re-weight what `π_ref` already does.
  Use it to explain why SFT comes first, why the base model's quality bounds post-training,
  and as the lens for the 2025 RLVR "new reasoning?" debate (Phase 11.1) — with the caveat
  that finite models and approximate optimization blur the exact statement.

- **Deep-RL phases stay small and concrete.** Gridworld value iteration, tabular Q-learning,
  DQN and PPO on CartPole (`gymnasium`; a hand-written cart-pole ODE is a fine side quest
  for a physics learner), MCTS on tic-tac-toe. Minutes of CPU each. The point is the
  vocabulary and the contrast with language, not Atari.

- **The scaling sidebar is honest about the toy.** The mini scaling sweep (9.3) shows the
  *method* (log-log fit) — its exponent says nothing about frontier models. The
  double-descent demo (9.4, `through-line-lab.md` §12) shows the peak, its dependence on
  label noise, and its removal by ridge — and, honestly, a second descent that doesn't beat
  the classical sweet spot in that toy.

- **Real models are tier b/c, never prerequisites.** TRL's `SFTTrainer`/`DPOTrainer`/
  `GRPOTrainer` on a small open model in Colab; LoRA/QLoRA locally. APIs move fast —
  check current docs. **Fail fast, no fallbacks:** if a download or import fails, surface
  the real error.

- **Safety-adjacent topics** (Constitutional AI, sycophancy, CoT monitoring) are taught as
  mechanism — what the reward is, where the leash is, what gets hacked — not as policy
  debate. Keep it technical.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner
produced themselves, kept as reference and as motivation if they stall mid-course.

- The verified corpus + the starting model (course-2 checkpoint or fallback) with its val
  NLL (Phase 0.2).
- Value iteration and Q-learning on a gridworld; DQN and PPO on CartPole (Phases 1–2).
- GAE written as a reversed one-pole filter (Phase 2.3).
- The first reward-hacking exhibit at `β = 0` (Phase 2.6).
- Tic-tac-toe MCTS beating its prior (Phase 3.3).
- The SFT model: format rate before/after, the alignment tax (Phase 4.2).
- A reward model with held-out pair accuracy; the `v0` speaker-dropping exhibit (Phase 5).
- The **reward-vs-KL plot** with best-of-n, the `β` sweep, and DPO on it (Phases 6.3, 6.4,
  7.3 — the keystone artifact).
- The gold-vs-proxy over-optimization curve (Phase 6.5).
- Toolformer's `L⁻ − L⁺` histogram (Phase 8.4); the double-descent table (Phase 9.4).
- The capstone post-training report (Phase 10.2).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or a different reward
used, edit `syllabus.md` (and `the-reward-and-the-leash.md`, `through-line-lab.md`, this
file, or `lesson.md` if the change is structural). All are versioned content; commit when
complete. Phase 11 is a living section: when a new SOTA post-training method lands, add it
there and to its "Frontier sources" list, keeping this file in sync.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring symbols — `π_θ` / `π` (the
  policy), `π_ref` (the reference, usually the SFT model), `π_old` (the policy that
  sampled the batch), `r` / `r_φ` (gold / learned reward), `β` (leash strength), `A_t`
  (advantage), `γ`, `λ` (discount, GAE), `KL(π ‖ π_ref)`, `Z(x)` (the tilt's normalizer) —
  get named the first time they appear. Unicode + CS-style identifiers in chat; LaTeX
  where genuinely clearer and in the lesson logs.
- Concrete > abstract; **a sample you can read > a curve > an equation**.
- One sentence of history when it explains a design: DQN (2013/2015) made deep Q-learning
  stable with replay and a target net; AlphaGo (2016) was already SFT → RL; AlphaZero (2017)
  replaced human data with search distilled into a network; PPO (2017) made policy
  gradients robust enough to ship; InstructGPT (2022) put PPO and a KL leash on a language
  model; DPO (2023) noticed the leashed optimum has a closed form; R1 (2025) put RL with a
  verifier back at the center.
