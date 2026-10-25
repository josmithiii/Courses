# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- DSP background (JOS's *Filters* / *SASP* or equivalent): _(can read a transfer function & an STFT / knows the words / strong DSP)_
- Synthesizer / effect programming experience: _(none / hobbyist patch-tweaker / builds synths or plugins)_
- ML background: _(ai-foundations through Phase 2 / all of ai-foundations / research-level)_
- Took `audio-ddsp` (course 1)? _(yes / no — affects how much of Phase 5.1 needs re-teaching)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- Math comfort (gradients, a little linear algebra, a little probability): _(rusty / comfortable / fluent)_
- Why they're here / goal: _(match real sounds with a synth / invert effects (DRC, reverb) / research / general curiosity)_
- Lean: _(hands-on — render, match, listen / conceptual — the inverse problem and the method map)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Can play audio on their machine / notebook with inline audio? _(yes / no — affects the "render and listen" exercises)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **render-and-listen first**, every term defined on first
  use, every estimate pinned to the one through-line note and *heard* before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-inverse-problem.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` + `torchaudio` importable
- [ ] `matplotlib` importable (loss-surface images, spectrograms, residuals)
- [ ] Can **play audio** — `IPython.display.Audio` in a notebook, or write+play a WAV
- [ ] The through-line note resolves at `../curricula/assets/audio-differentiable-dsp/note.wav`
      (or was produced with `make_note.py` there, or a short mono plucked/struck note is in hand — see CLAUDE.md build-time note)
- [ ] The two-knob toy synth (`decay`, `cutoff`) written and rendering (Phase 1.3)
- [ ] (capstone tier b/c) Colab or local GPU confirmed; DiffMoog cloned if tier c
- [ ] `the-inverse-problem.md` read (the keystone — many parameters, one sound)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The note & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Through-line note: electric guitar, single-coil pickup, plectrum, low E, mono, 44.1 kHz, ~6 s → 264 600 samples; fundamental ≈ _(Hz, measured in 0.2)_.
- Toy synth `g(a, f_c)`: excitation → exponential decay `a` (per-sample, or as T60 in s) → one-pole lowpass at `f_c` Hz.
- Loss-surface grid (Phase 1.4): `a ∈ [_, _]`, `f_c ∈ [_, _]` Hz, 50×50; valley direction: _(e.g. faster decay ⇔ lower cutoff)_.
- Gradient-descent estimates (Phase 1.5), three starts: `(a, f_c)` = _, _, _ ; losses = _.
- CNN in-domain vs real-note parameter MSE (Phase 3.4): _ vs _ ; audio (MR-STFT) loss on the real note: _.
- Finite-difference `JᵀJ` at the toy optimum (Phase 4.3): long-axis direction = _ (should align with the valley).
- Differentiable KS fit to the note (Phase 5.7): `f_0` = _, `g` = _, `a_1` = _ ; MR-STFT loss = _ ; onset-gradient result: _.
- DRC forward-model parameters used on the note (Phase 7.3): `L` (threshold dB) = _, `R` = _, `τ_att/τ_rel` (detector, gain) = _ ; inversion residual (Phase 7.4) = _.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has computed/heard themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-inverse-problem.md`). The tutor watches
> for these, notes when one comes up, and revisits later to make sure it has stuck.

- "parameter MSE measures how good the match sounds" — no, the map is **many-to-one** and perception is nonlinear in θ; render and listen
- "there is one right answer θ*" — no, a **valley / a set of symmetric copies**; the object is a distribution `p(θ | x)`
- "you need a differentiable synth" — no: white-box, proxies, SPSA, RL, genetic search all exist; DDSP just has the best gradients
- "in-domain accuracy transfers to real recordings" — no, that is the **cross-domain gap**; fine-tune with an audio loss on real sounds
- "multi-scale spectral loss is the universal best" — no, **synthesizer-dependent** (Salimi 2025); MR-STFT is non-convex in pitch
- "PNP is a perceptual loss" — it is a **linearized** one: a quadratic on θ weighted by the perceptual Jacobian
- "effect inversion is a different field" — same loop, different `g` (the DRC thread)
- "a framewise match that sounds right is the goal" — interpretable modulation structure is a design axis
- "a smoother loss (OT, log-magnitude) makes descent safe" — no: FM **ridges** at rational ratios (Tabata 2026); no spectral loss sees KS onsets (Tablas de Paula 2026); log-MR-STFT collapses plate recovery
- "match the output waveform" — for device emulation, supervise what defines the effect (the compressor's **gain trajectory**, Thompson & Heilemann 2026)
- "search is too slow — learn an estimator" — not when `g` is cheap; the DAFx26 challenge was won by **learned initialiser + search polish**
- "RL here is an agent turning knobs step by step" — no: SynthRL is a one-shot policy trained by **policy gradient against a rendered-audio reward** (a contextual bandit)
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.2) — tiered, no GPU required
> Picked partway through Phase 5 so it can shape the last few lessons.

- _(a) **CPU** — train a small CNN on 5 000 two-knob toy renders, predict `(a, f_c)` for the real note, render, residual spectrogram, A/B listen, then refine by gradient descent on MR-STFT; report predicted vs refined and why they differ_
- _(b) **Colab GPU** — tier a, plus the Masuda-style differentiable subtractive synth trained with parameter loss only vs combined parameter + spectral loss; compare parameter error, audio loss, and ear on the note_
- _(c) **Local GPU** — tier a, plus DiffMoog or a small flow-based `p(θ | x)`; sample 100 solutions for the note and plot the distribution_
- Choice: _(not yet)_
