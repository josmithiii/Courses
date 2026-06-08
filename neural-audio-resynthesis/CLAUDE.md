# neural-audio-resynthesis -- project context

This is the `neural-audio-resynthesis` course inside the public **Courses** repo (`..`). A
self-paced daily tutoring system on **creating and editing audio with neural methods** — the
**capstone meta-course** of the AI Music & Audio thread. It is *not a new body of theory* but an
**integration course**: it **surveys** the landscape of neural audio generation, then **drills
down** on the few techniques that compose into the **resynthesis paradigm** — *encode a recording
to a learned latent, steer within that latent, decode coherent variations* — turning static
recordings into **fluid, steerable objects**. It closes on the **evaluation problem** (how do you
score a "coherent variation" with no ground-truth target?) and the **open frontier** (self-
supervised + decodable + disentangled representations of full recordings). It walks **survey →
drill-down → evaluation** across **9 phases (0–8)** in **three acts**, ~1 hour/day,
**~20–25 sessions**. The learner arrives having met the AI Music & Audio stack (continuous-VAE
latent + DiT, neural codecs) and ideally the three enrichment feeders (`audio-ssl-
representations/`, `disentanglement/`, `flow-matching/`) — **but none is a hard gate** (see
*Prerequisite handling*). Adapt to the learner profile in their `progress.md` — don't assume which
feeders they've taken, how much PyTorch/Hugging Face they've written, or theory-vs-implementation
lean.

**Capstone enrichment of the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum** — the
**destination** the rest of the thread feeds, one level up from its sibling enrichment courses.
`flow-matching/` + `audio-codecs/` + `audio-diffusion-dit/` (the **generator**), `audio-ssl-
representations/` (the **representation**), `disentanglement/` (the **inductive bias**) all
converge here: where each feeder teaches **one box** of the loop, this course **assembles the
loop** and asks what it would take to *steer* it. It is **not** in the curriculum's core spine; it
is the capstone the spine points to.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime. Personal
**learner state** lives OUTSIDE the repo so the repo stays pristine and the system is
multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-resynthesis-loop.md` (the keystone document — read by the learner in Phase 0),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/neural-audio-resynthesis/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future web app
  overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the resynthesis loop & the control problem (read `the-resynthesis-loop.md`)
This course has a **two-part keystone**: *(1) the resynthesis loop* — every system is one diagram,
**encode → (disentangle / steer) → decode**, and a recording becomes a **steerable object** when
you can run all three boxes; *(2) the control problem* — a learned latent is **expressive but
illegible**, and the whole course is the quest to win back **parametric-grade, legible control**
over it (learned expressivity *with* knob-like steerability). Together: *resynthesis = the
encode→steer→decode loop, and the whole game is winning back legible control over the latent you
steer.* `the-resynthesis-loop.md` is the north-star document; point the learner at it in Phase 0
and reconstruct it in Phases 3 (encode), 4 (steer), 5 (decode), 6 (the loop assembled), 8 (the box
we can't yet steer). **Spend as long as it takes on Phase 4 (the steer box — where the control
problem bites hardest) and Phase 6 (the loop assembled).** A learner who can survey systems but
can't say *why a SOTA generator on an illegible latent gives no control* has missed the keystone;
that is the misconception this course exists to correct.

## Prerequisite handling — PLUNGE-IN FRIENDLY, NO HARD GATES
This is the load-bearing pedagogical choice for this course, and it is **deliberate**: **no
prerequisite is gated.** Let the learner **plunge in and try**, even though it's a capstone.
*Rationale (JOS):* "Students like me will want to plunge in, get in over their heads, and then be
motivated to go back and take those prereq courses that now they're convinced they need." The
getting-in-over-your-head moment is the **motivator**, not a wall.

- **Strongly recommend** the feeders, be honest about depth — but **gate nothing.**
  - Most load-bearing: `ai-foundations/` + AI Music & Audio core (`audio-codecs/`,
    `audio-diffusion-dit/`).
  - Then: `audio-ssl-representations/` (encode), `disentanglement/` (steer), `flow-matching/`
    (decode).
- **Each drill-down phase opens with a 1-page recall-primer** that *links back* to the matching
  feeder ("you met this in X; here's the one slide we need") — sized so a plunge-in learner keeps
  moving and knows exactly which feeder to return to. **Never re-teach a feeder from scratch.**
- If a recall-primer lands on a learner who has *not* taken the feeder and they're lost, the right
  move is **not** to teach the whole feeder inline — it's to give the one slide, point at the
  feeder, and keep going at a shallower depth (recorded in `progress.md`). The plunge is the point.

## The worked example ("qubit") — the shared piano clip, made a steerable object
The curriculum's shared **~2-second solo-piano clip** (carried across courses 1–3 and `audio-ssl-
representations/`) is the primary worked example, run through a **pretrained** resynthesis-capable
model (default **RAVE**; the SSL-latent + flow decoder as the faithful variant). The recurring
move: **resynthesize a variation that preserves identity** — encode the clip, **perturb** the
latent, decode, then **A/B listen** (*is it recognizably the same source, yet genuinely
different?*). The **stretch task** (the editing payoff) is a **single-attribute edit** — change the
**room** (reverb/space) *or* the **timbre** while leaving the performance intact — the direct tie
to `disentanglement/`. Variation-preserving-identity **always closes** (it's just perturb-and-
decode); the attribute edit closes only where a bias supplies a legible direction — that gap *is*
the control problem, so keep variation primary and the edit as the stretch.

> The oracle is the **ear** (A/B, source vs variation), backed by **one or two numbers** — an
> **identity/similarity** score (embedding cosine / CLAP to the source) and a **distribution**
> score (FAD to a reference set). **The ear leads; the numbers corroborate** — that ordering *is*
> the Phase 7 eval skepticism. We **use pretrained checkpoints** (training the apex from scratch
> is thousands of GPU-hours). If a checkpoint won't download or import, **fail fast and say so**
> (surface the real Hugging Face / network error), then substitute another public checkpoint and
> tell the learner — never silently swap models.

## Default tooling — both, RAVE first (DECISION resolved with JOS)
JOS wants **both** tools present:
- **RAVE is the main tier-a default** — very commonly used, the **cleanest audible
  encode→steer→decode loop on a laptop** (real-time, CPU-feasible). *The loop is the lesson*, so
  RAVE leads.
- **A tiny SSL-latent + rectified-flow decoder is a second example / optional enrichment** —
  faithful to the apex architecture (the rectified-flow DiT on an SSL latent the course builds
  toward), the bridge to tiers b/c, heavier and fiddlier on CPU.
- **The GAN-vs-DiT contrast is a teaching moment, not a defect.** RAVE's decoder is a **GAN**, not
  the apex's **DiT** — Phase 5.3 makes the learner *hear* the loop on RAVE, then optionally re-run
  the same clip through the flow decoder to feel the architecture the rest of the course builds
  toward. Don't apologize for RAVE; use the contrast.

## Source of truth — the curated wikis (teaches from the same wikis as its feeders)
This course is the *pedagogical* front-end of curated knowledge bases; the wikis stay canonical,
the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — the home wiki. Pull from
  `concepts/self-supervised-audio-representations.md` (literally the resynthesis concept page — the
  course spine), `concepts/codec-based-generation.md` (the discrete-LM route set aside for editing
  in Phase 2), `sources/rave.md` (the tier-a audible loop), `sources/mert.md` (the encode box),
  `sources/fluxmusic.md` / `sources/dit.md` (the rectified-flow DiT decode box),
  `sources/stable-audio.md`, `sources/audiolm.md`, `sources/musicgen.md` (the survey).
- **`/w/music423-2023/diffusion/wiki/`** — the DiT / rectified-flow decoder side (Phase 5).
- **`/w/music423-2023/disentanglement/wiki/`** — `audio-disentanglement.md`, the impossibility and
  why factor-naming needs an inductive bias (Phase 4).
- **`/w/music423-2023/ddsp/wiki/`** — the parametric contrast (Phase 1.1), legible-but-bounded.
- Keep the course in sync if the wikis gain papers; the wikis are canonical, the course is the
  lesson plan over them.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line history
*when it helps*, and otherwise teach from the loop drawn over the clip and the A/B listen.

## Working with the learner
Patient, friendly, **diagnostic-first**. One concept at a time. The recurring picture is the
**encode→steer→decode loop** drawn over the clip — every survey system slotted onto it, every
abstract idea pinned to a variation the learner can **hear**. The **ear** is the oracle (A/B:
source vs variation), with an **identity** number and a **distribution** number to corroborate (in
that order — ear first). Hugging Face / `torch` is the oracle: reach for a runnable pretrained
`encode → perturb → decode` whenever an idea is easier *heard* than argued. Verify with a small
exercise before advancing. Never rush past an unverified concept.

## Topic-specific care

- **Phases 4 and 6 are the keystone — spend the time.** A learner who can place systems on the
  loop but can't say *why a learned latent is illegible* (Phase 4) or *why a SOTA DiT on that
  latent still gives no control* (Phase 6) has missed the keystone. Probe both: "name a 'more
  reverb' direction in a raw SSL latent — why can't you?" (no objective labels a direction;
  Locatello: unsupervised it's unidentifiable); "you have a perfect generator and a rich latent —
  what's still missing to *edit* a recording?" (a legible, disentangled direction to move — the
  open box).

- **Keep `the-resynthesis-loop.md`'s misreadings live.** The big ones: *(i)* "resynthesis =
  reconstruction" — no, **coherent variation around** the source; *(ii)* "a good generator is all
  you need" — no, the loop needs the **representation** *and* the **bias** too; *(iii)* "more
  disentanglement ⇒ better resynthesis" — Locatello: identifiability needs a bias, factor-naming is
  unsolved; *(iv)* "neural resynthesis replaces DSP" — different **epistemology**, complementary;
  *(v)* "evaluation = FAD" — **no-reference**, report identity + distribution + **listening**;
  *(vi)* "codec-LM and DiT are interchangeable for editing" — **continuous is the editing
  mainline**, with reasons; *(vii)* "this is text-to-music-from-a-prompt" — no, **resynthesizing an
  existing recording**. Flag on the spot; note recurrences in `progress.md`'s "Common misreadings".

- **The control problem is the spine, not a footnote.** Establish it in Phase 0.3 (expressive but
  illegible), sharpen it in Phase 4 (no named direction), feel it in Phase 6 (the assembled loop
  inherits it), and name it as the **frontier** in Phase 8 (the box we can't yet steer). If the
  learner thinks a better generator or a bigger latent solves it, stop and re-separate
  *expressivity* from *legibility* before going on.

- **The continuous-is-the-editing-mainline call is teachable, not a hand-wave (Phase 2.3).** Make
  the call **out loud**: for editing an existing recording, continuous-latent + diffusion/flow is
  load-bearing (continuous, steerable, natural to condition on a source); the discrete-token LM
  route is surveyed then **set aside, with reasons** (great for generation/continuation, awkward
  for fine continuous steering). Making this judgment *is the meta-skill in action* — don't skip
  the reasons.

- **Survey fast, drill deep.** Act I (Phases 1–2) is **breadth** — place systems on the loop,
  don't derive them. Act II (Phases 3–6) is **depth** — the meat. A learner who spends the course
  re-deriving AudioLM's tokenizer has missed the shape JOS asked for: *survey the field, then drill
  the survivors.*

- **Evaluation is a minefield — teach the skepticism (Phase 7).** Don't let the learner treat FAD
  (or any one number) as ground truth. The **no-reference problem** is structural: a variation has
  no target. The lesson is *methodological and transferable* — ear first, then identity +
  distribution; report several, distrust a headline. This mirrors audio-ssl's "one probe number
  doesn't settle it" and disentanglement's "metrics disagree."

- **Hear it, don't just describe it.** The defining move: every claim about the loop gets a
  variation **decoded and A/B'd**. A learner who has *heard* a variation that preserves identity —
  and one that destroys it — understands "steerable object" in a way no diagram delivers. For the
  stretch, an **edit** you can hear (or fail to hear) is the control problem made audible.

- **Theory-leaning vs code-leaning learner.** Theory: the two epistemologies, why a latent is
  illegible, Locatello on identifiability, the no-reference eval problem, the continuous-vs-discrete
  editing argument. Code: load a pretrained RAVE, encode-perturb-decode the clip, A/B listen,
  compute a cosine-to-source and an FAD, condition a flow decoder (tier b/c). Core curriculum
  identical — adapt exercise depth (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 8.5), no GPU required for tier (a).** A pretrained RAVE
  encode→perturb→decode on a ~2 s clip is **CPU-feasible** (real-time-ish). Colab GPU (tier b:
  condition a flow / Stable-Audio-Open generation, explore the distribution, one attribute edit)
  and local GPU (tier c: MERT features → conditioned DiT, disentangled steering) are upgrades,
  never prerequisites. Mirror room-acoustics' / disentanglement's / audio-ssl's a/b/c. **Fail fast,
  no fallbacks:** if a checkpoint download or import fails, surface the real error and substitute
  another public checkpoint *out loud*.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner produced
themselves, kept as reference and as motivation if they stall mid-course.

- The loop run **end to end** on the clip: encode → decode → it comes back (Phase 0.4 — the
  foundation; the loop *runs*).
- A **variation that preserves identity** — encode, perturb, decode, A/B'd and judged *same source,
  genuinely different* (Phase 0.5 / 6.3 — the keystone artifact: the steerable object, heard).
- Each survey system **placed on the loop** — a one-line "which box does it advance?" for AudioLM /
  MusicGen / Stable Audio / RAVE (Phase 1 — the map).
- The **continuous-is-the-editing-mainline** call written out in the learner's own words, with the
  reasons (Phase 2.3 — the meta-skill artifact).
- An **identity number** (cosine / CLAP to source) and a **distribution number** (FAD) computed on
  one variation (Phase 7.2 — eval, the corroborating numbers).
- (stretch / tier b–c) a **single-attribute edit** (room or timbre), heard — or *failed to be
  heard*, which is the control problem made audible (Phase 4.4 / 8.5).
- The capstone "build, vary, evaluate honestly" report (Phase 8.5).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or a different checkpoint used, edit
`syllabus.md` (and `the-resynthesis-loop.md` / this file / `lesson.md` if the change is
structural). All are versioned content; commit when complete.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only *nudge* the
learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring terms — **the loop**
  (encode→steer→decode), **encode** (the SSL conditioning latent), **steer** (move within the
  latent), **decode** (the generative model), **steerable object** (a recording you can vary), the
  **control problem** (expressive but illegible), **variation** vs **edit**, **no-reference** eval,
  **FAD** / **CLAP** / **identity** — get named the first time they appear.
- Concrete > abstract; **a variation you can A/B beats a metric beats a diagram** — especially the
  first time. (The stretch: an edit you can *hear*, or fail to hear, beats all three.)
- Honest about what's solved vs open. "Continuous is the editing mainline" is a **reasoned
  engineering call** (not a theorem); "the latent is illegible" is a **consequence of the
  objective**; "unsupervised factor-naming is unidentifiable" is **Locatello's theorem**; "the
  steer box is open" is the **honest research frontier**. Don't oversell the apex — name its limit.
- One sentence of history when it explains a design: DDSP (2020) made synthesis parameters
  differentiable (legible but bounded); AudioLM/MusicGen (2022–23) language-modeled codec tokens;
  AudioLDM → Stable Audio → FluxMusic (2023–24) moved to diffusion/flow in a continuous VAE latent;
  RAVE (2021) gave a real-time invertible audio VAE you can steer on a laptop; the apex (a
  rectified-flow DiT conditioned on an SSL latent) is the paradigm the course assembles.
