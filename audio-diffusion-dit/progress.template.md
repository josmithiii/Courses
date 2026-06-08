# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Finished `audio-codecs/` (course 1)? _(yes — continuous VAE latent & fork solid / partly / no — rebuild in Phase 0.2)_
- Finished `audio-codec-lms/` (course 2)? _(yes — token grid & the contrast solid / partly / no)_
- Diffusion background (`ai-foundations` Phase 6): _(shaky — re-ground in 0.2 / comfortable / strong)_
- ML background (Transformers/LLMs from `ai-foundations`): _(comfortable / strong)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- Taken / taking `flow-matching/`? _(yes / no — affects how deep Phase 6 goes)_
- Why they're here / goal: _(build a music generator / understand the diffusion-DiT paradigm / contrast with codec-LMs / research)_
- Lean: _(hands-on — run Stable Audio Open / DiffRhythm, denoise the clip's latent / conceptual — understand the paradigms & the canvas)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Can play audio on their machine / using a notebook with inline audio? _(yes / no — affects the "listen" exercises)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **listen-first**, every term defined on first use, every
  denoising pinned to the one through-line clip and *heard* before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-latent-canvas.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` + `torchaudio` importable
- [ ] The course-1 codec / VAE importable (for re-encoding the clip to its continuous latent)
- [ ] (capstone tier a) `diffusers` and/or `stable-audio-tools` installed; a small latent-diffusion model (or **Stable Audio Open**) loads
- [ ] Can **play audio** — `IPython.display.Audio` in a notebook, or write+play a WAV
- [ ] The through-line clip resolves at `../curricula/assets/ai-music-audio/through-line.wav`
- [ ] `the-latent-canvas.md` read (the keystone — the continuous latent & the DiT)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The canvas & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Through-line clip: solo piano, mono, 24 kHz, ~2 s.
- Clip's **continuous VAE latent** (once a VAE is loaded): shape `[C, T]` = _(channels × latent frames)_
- `z` = latent; `z_t` = noised latent at step `t`; `ε` = noise; `∇ log p_t` = score;
  `v_θ` = velocity (Phase 6); `w` = guidance scale; `(t, c)` = timestep + condition into adaLN-Zero.
- Reference specs met along the way: Stable Audio 44.1 kHz stereo, ~95 s, 907M U-Net;
  Long-Form 21.5 Hz latent rate, full songs to 4m45s (DiT); DiffRhythm ~10 s/song.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has generated/heard themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-latent-canvas.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "'audio codec → DiT' uses discrete tokens" — no, a **continuous VAE latent** (the field's #1 confusion)
- "Stable Audio is a DiT" — no, **v1 is a U-Net**; the DiT swap is one paper later
- "DiT is a diffusion-specific architecture" — no, a **plain transformer + adaLN-Zero**
- "flow matching is just diffusion" — related, but a different objective (velocity vs noise/score)
- "semantic tokens are *required* for long-range coherence" — long-form diffusion challenged this
- "an LM inside (AudioLDM 2 / ACE-Step) makes it a codec-LM" — no, **hybrid**: LM plans, DiT renders
- "masked NAR = diffusion" (from course 2) — discrete confidence-unmasking vs continuous denoising
- "diffusion needs 1000 steps / is slow" — DDIM ~50, ODE solvers 10–20, distillation 4–8
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.2) — tiered, no GPU required
> Picked partway through Phase 5 so it can shape the last few lessons.

- _(a) **CPU / pretrained inference** — small latent-diffusion model (or Stable Audio Open, slowly): generate from text, denoise the clip's own VAE latent (img2img) into a variation, inspect the latent at a few steps, decode & listen; one-page diffusion-DiT report_
- _(b) **Colab GPU** — tier a, plus full-length generation, an A/B of DDIM step counts (10 vs 50), timing conditioning, a DiffRhythm full song, and (time permitting) DITTO-style melody/structure control_
- _(c) **Local GPU** — tier a, plus FluxMusic (rectified flow / MM-DiT) and/or ACE-Step (LM-planner + DiT-renderer); prompt toward the clip's style; hear the objective swap and the hybrid pipeline_
- Choice: _(not yet)_
