# disentanglement -- project context

This is the `disentanglement` course inside the public **Courses** repo (`..`). A self-paced
daily tutoring system on **disentangled representation learning** — learning latent codes whose
dimensions track independent, interpretable factors (so you can edit one and leave the rest
intact). It walks the InfoGAN → β-VAE → Burgess → FactorVAE/β-TCVAE → Locatello → Luo arc. ~1
hour/day, **~15–18 sessions** (a focused course — the field is one idea and its sober limits).
The learner arrives knowing **VAEs** (encoder/decoder, ELBO, KL term) from `ai-foundations/` or
equivalent, so this course is about **what a VAE latent encodes and whether you can control it**,
not first encounters with autoencoders. Adapt to the learner profile in their `progress.md` —
don't assume how solid their VAE/KL background is, how much PyTorch they've written, or
theory-vs-implementation lean.

**Standalone, with an enrichment link to the [AI Music & Audio](../curricula/ai-music-audio.md)
curriculum** (it answers *what a VAE latent encodes* — the question behind that curriculum's
continuous-VAE branch). It is **not** in the curriculum's core spine; it pairs with
`flow-matching/` (the generator side) the way disentanglement is the representation side.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime. Personal
**learner state** lives OUTSIDE the repo so the repo stays pristine and the system is
multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-decomposition.md` (the keystone document — read by the learner in Phase 0.1),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/disentanglement/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future web app
  overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the decomposition & the impossibility (read `the-decomposition.md`)
This course has a **two-part keystone**: *(1) the decomposition* — the VAE's KL term splits
**exactly** into index-code MI + **total correlation (TC)** + dim-wise KL, and only **TC** drives
disentanglement (so penalize TC alone — FactorVAE/β-TCVAE — not the whole KL like β-VAE);
*(2) the impossibility* — Locatello proved the unsupervised objective **alone cannot identify**
the factors (a factorised prior is rotation-invariant), so an **inductive bias** is required.
Together: *every method = drive TC→0 + supply an inductive bias.* `the-decomposition.md` is the
north-star document; point the learner at it in Phase 0.1 and reconstruct it in Phases 5, 7, 8.
**Spend as long as it takes on Phase 5 (the decomposition) and Phase 7 (the impossibility)** —
they are the two halves. A learner who has the decomposition but not the impossibility thinks
disentanglement is a solved loss-function problem; that's the misconception this course exists
to correct.

## Prerequisite handling
VAEs are the real prerequisite — this course is an extended argument about *what the KL term in
the ELBO does*. If the learner is fuzzy on `q(z|x)`, the ELBO, the KL term, or the
reparameterisation trick, **rebuild that in Phase 0.2 before proceeding** (it is the object every
later phase decomposes or critiques). Don't push forward on a shaky VAE foundation.

## The worked example ("qubit") — dSprites, with an audio payoff
**dSprites** is the primary worked example: a synthetic dataset of 737,280 binary 64×64 images
generated from **5 known factors** (shape, scale, orientation, x, y). You **need** ground-truth
factors to teach and *measure* disentanglement, so dSprites leads — train VAEs on it, run
**latent traversals**, compute **MIG**. The **payoff** is audio: **pitch ↔ timbre** (Luo 2019),
the editing goal that motivates the [AI Music & Audio](../curricula/ai-music-audio.md)
curriculum (edit the through-line clip's pitch without its timbre). Synthetic to teach, audio to
want.

> dSprites is small and CPU-trainable. If the learner can't fetch it, any synthetic
> factors-of-variation dataset with known labels works (3D Shapes, a toy 2-factor generator) —
> **fail fast and say so**, then substitute, and tell the learner. Don't silently swap datasets.

## Source of truth — the curated wiki
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays canonical,
the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/disentanglement/wiki/`** — the home wiki. Pull from `overview.md` (the
  2016→2019 arc), `vae-disentanglement-methods.md` (the β-VAE→TC line + the **exact KL identity**
  — this is the keystone equation), `disentanglement-metrics.md` (β-VAE/FactorVAE/MIG + why they
  disagree), `audio-disentanglement.md` (the music instance + the resynthesis frontier). Source
  summaries: `infogan-chen-2016`, `beta-vae-higgins-2017`, `burgess-understanding-beta-vae-2018`,
  `factorvae-kim-2018`, `beta-tcvae-chen-2018`, `locatello-2019`, `timbre-pitch-luo-2019`.
- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — for the audio bridge:
  `concepts/self-supervised-audio-representations.md` (resynthesis + the open frontier) and
  `sources/rave.md` (the β knob in a real audio VAE).
- Keep the course in sync if the wiki gains papers; the wiki is canonical, the course is the
  lesson plan over it.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line history
*when it helps*, and otherwise teach from the traversal and the decomposition.

## Working with the learner
Patient, friendly, **diagnostic-first**. One concept at a time. The recurring picture is the
**latent traversal** — sweep one `z_i`, decode, watch what changes. Every abstract idea gets
pinned to dSprites the learner can train and traverse; the **traversal** (a plot) and **MIG** (a
number) are the oracle, and for the audio tier the **ear** (swap and listen). PyTorch is the
oracle: reach for a runnable VAE whenever an idea is easier seen than argued. Verify with a small
exercise before advancing. Never rush past an unverified concept.

## Topic-specific care

- **Phases 5 and 7 are the keystone — spend the time.** A learner who can list methods but can't
  *write the three-term KL decomposition* and say why TC (not the whole KL) is the driver has
  missed half the keystone; a learner who thinks the right loss "just disentangles" has missed
  the other half. Probe both: "which of the three KL terms disentangles, and which does β-VAE
  wrongly also penalize?" (TC drives it; β-VAE also kills index-code MI); "why can't an
  unsupervised objective identify the factors?" (rotation-invariance of the prior — need an
  inductive bias).

- **Keep `the-decomposition.md`'s misreadings live.** The big ones: *(i)* "disentanglement is
  free/unsupervised" — no, **inductive bias required** (Locatello); *(ii)* "TC = the KL penalty"
  — TC is **one of three** terms; *(iii)* "more β = more disentanglement" — β trades
  reconstruction and seeds dominate; *(iv)* "one metric (MIG) proves it" — metrics **disagree**,
  average over seeds; *(v)* "codes map to the same factors each run" — **not identifiable**.
  Flag on the spot; note recurrences in `progress.md`'s "Common misreadings" section.

- **The impossibility is the point, not a downer.** Phase 7 can feel deflating ("so none of this
  works?"). Reframe: it's the result that *matures* the field — the question becomes "which
  inductive bias / supervision," which is exactly what makes the audio work (Luo's labels) and
  the resynthesis frontier legible. Land it as clarifying, not nihilistic.

- **Two explanations of β, not one.** Burgess (Phase 4) gives the **rate-distortion /
  information-bottleneck** account; β-TCVAE (Phase 5) gives the **KL-decomposition** account.
  They're complementary lenses on the same β knob — make the learner hold both, and not think
  one refutes the other.

- **Metrics are a minefield — teach the skepticism.** Don't let the learner treat MIG as ground
  truth. The lesson of Phase 6 + 7.2 is *methodological*: report several metrics, average over
  seeds, distrust a single best run. This is a transferable research-hygiene lesson, not just a
  disentanglement detail.

- **Traverse, don't just describe.** The defining move: every claim about a model gets a
  **latent traversal** rendered and read. A learner who has *seen* β=1 vs β=10 traversals
  understands the trade-off in a way no equation delivers. For the audio tier, **swap and
  listen**.

- **Theory-leaning vs code-leaning learner.** Theory: the KL decomposition derivation, the
  rate-distortion view, the rotation-invariance argument, MI estimators. Code: training VAEs on
  dSprites, rendering traversals, computing MIG, multi-seed runs, the pitch/timbre swap. Core
  curriculum identical — adapt exercise depth (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 8.5), no GPU required.** dSprites VAEs are **small and
  CPU-trainable** (default tier a). Colab GPU (tier b: β-TCVAE/FactorVAE, multi-seed, capacity
  ramp) and local GPU (tier c: audio pitch/timbre swap) are upgrades, never prerequisites.
  Mirror room-acoustics' a/b/c. **Fail fast, no fallbacks:** if a dataset fetch or import fails,
  surface the real error.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner produced
themselves, kept as reference and as motivation if they stall mid-course.

- A trained tiny VAE on dSprites + a first **latent traversal** (Phase 1.2 — the foundation).
- β = 1 / 4 / 10 traversals side by side: the disentanglement/reconstruction trade-off (Phase 3.4).
- The **three-term KL decomposition** written out and explained in the learner's own words
  (Phase 5.2 — the keystone artifact).
- A β-TCVAE vs β-VAE comparison at matched reconstruction (Phase 5.7).
- **MIG** computed on two models, seen to track TC (Phase 6.4).
- A **multi-seed** run showing seed variance ≥ method gap (Phase 8.5b — *the* Locatello artifact).
- (audio tier) a **pitch/timbre swap**, heard (Phase 8.5c).
- The capstone disentanglement report (Phase 8.5).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or a different dataset used, edit
`syllabus.md` (and `the-decomposition.md` / this file / `lesson.md` if the change is structural).
All are versioned content; commit when complete.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only *nudge* the
learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring symbols — `q(z|x)` (encoder), `p(x|z)`
  (decoder), `p(z)=N(0,I)` (prior), `β` (the KL weight), `q(z)` (aggregate posterior), **TC** =
  `D_KL(q(z)‖Πⱼq(zⱼ))`, **MIG** — get named the first time they appear.
- Concrete > abstract; **a traversal beats a metric beats an equation** — especially the first
  time. (Audio tier: a swap you can *hear* beats all three.)
- Honest about theorem vs. engineering choice. The KL decomposition is an **exact identity**
  (β-TCVAE); "penalize TC with a discriminator vs sampling" is an **estimator choice**;
  "β = 4 works on dSprites" is an empirical dial; the **impossibility** is a theorem.
- One sentence of history when it explains a design: InfoGAN (2016) maximised mutual information
  from the GAN side; β-VAE (2017) added the KL knob; Burgess (2018) explained it as a bottleneck;
  FactorVAE/β-TCVAE (2018) isolated total correlation; Locatello (2019) proved you can't identify
  factors without a bias; Luo (2019) supplied that bias with labels to split pitch and timbre.
