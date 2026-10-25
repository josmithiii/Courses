# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Finished `audio-codecs/` (course 1)? _(yes — token grid & fork solid / partly / no — rebuild tokens in Phase 0.2)_
- ML background (Transformers/LLMs from `ai-foundations`): _(comfortable / strong)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- Comfort with autoregressive / next-token modeling: _(shaky / comfortable / strong)_
- Why they're here / goal: _(build a music generator / understand the codec-LM paradigm / contrast with diffusion / research)_
- Lean: _(hands-on — run MusicGen, generate/continue/infill / conceptual — understand the paradigms & the grid)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Can play audio on their machine / using a notebook with inline audio? _(yes / no — affects the "listen" exercises)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **listen-first**, every term defined on first use, every
  generation pinned to the one through-line clip and *heard* before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-token-grid.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` + `torchaudio` importable
- [ ] The course-1 codec importable (EnCodec via `transformers`/`audiocraft`, or DAC) — for re-encoding the clip
- [ ] (capstone tier a) `audiocraft` installed; smallest **MusicGen** loads
- [ ] Can **play audio** — `IPython.display.Audio` in a notebook, or write+play a WAV
- [ ] The through-line clip resolves at `../curricula/assets/ai-music-audio/through-line.wav`
- [ ] `the-token-grid.md` read (the keystone — the RVQ grid & the multi-stream challenge)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The grid & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Through-line clip: solo piano, mono, 24 kHz, ~2 s.
- Clip's token grid (once a codec is loaded): shape `[N_q, T]` = _(e.g. [4, ~150] at 75 Hz)_
- `N_q` = codebook levels / RVQ streams; `T` = frames; a **column** = one frame (all levels),
  a **row** = one codebook level over time.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has generated/heard themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-token-grid.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "MusicGen is multi-stage" — no, **single-stage** with a codebook pattern
- "masked NAR generation = diffusion" — discrete confidence-unmasking vs continuous denoising
- "MIDI-VALLE / VALL-E are DiTs" — no, **codec language models** (the cleanest fork test)
- semantic vs acoustic tokens conflated (structure vs fidelity; AudioLM uses both)
- "more codebook levels = independent quality knobs" — RVQ levels are residual & ordered
- "text-to-music needs paired data" — MuLan/CLAP bypass it with contrastive embeddings
- "semantic tokens are *required* for long-range coherence" — long-form diffusion challenged this (course 3)
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.2) — tiered, no GPU required
> Picked partway through Phase 5 so it can shape the last few lessons.

- _(a) **CPU / pretrained inference** — smallest MusicGen via audiocraft: generate from text, continue the clip (audio prompt), inspect & decode the generated token grid; one-page codec-LM report_
- _(b) **Colab GPU** — tier a, plus a VampNet/MAGNeT-style infill of the clip's middle, an A/B of delay vs flat patterns, and melody (chromagram) conditioning toward the clip_
- _(c) **Local GPU** — tier a, plus a style fine-tune toward the clip, or run MIDI-VALLE on a performance-MIDI rendering to hear the codec-LM-vs-DiT distinction before course 3_
- Choice: _(not yet)_
