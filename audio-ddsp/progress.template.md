# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- DSP background (JOS's *Filters* / *SASP* or equivalent): _(knows biquads & the STFT cold / has seen them, rusty / weaker than assumed — slow Phase 1 down)_
- Has written a synthesizer or effect by hand before? _(no / a few / many — which language?)_
- PyTorch comfort (from `ai-foundations` Phase 2 or equivalent): _(beginner / comfortable / strong)_
- Autograd understanding: _(has called `.backward()` and looked at a gradient / only used `optimizer.step()` / never)_
- Math comfort (complex exponentials, `z`-transform, a little calculus): _(rusty / comfortable / fluent)_
- Why they're here / goal: _(make my own DSP learnable / read the DDSP papers / build toward synth matching (course 2) or physical models (course 3) / curiosity)_
- Lean: _(hands-on — write blocks & fit the note / conceptual — understand losses, gradients & the trade-offs)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Can play audio on their machine / using a notebook with inline audio? _(yes / no — affects the "listen" exercises)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **listen-first**, respectful of the DSP already known, every
  term defined on first use, every block pinned to the one through-line note and *heard*
  before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-differentiable-block.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` + `torchaudio` importable
- [ ] `numpy` + `matplotlib` importable (plots, FFT peak-picking)
- [ ] Can **play audio** — `IPython.display.Audio` in a notebook, or write+play a WAV
- [ ] The through-line note resolves at `../curricula/assets/audio-differentiable-dsp/note.wav`
      — or the labelled placeholder was generated with `make_note.py` and the learner
      *knows* it is synthetic (see CLAUDE.md build-time note)
- [ ] `the-differentiable-block.md` read (the keystone — the block and the loss)
- [ ] A scratch `.py` file or notebook open and used during sessions
- [ ] (capstone tier b/c) Colab or local GPU confirmed; a pretrained DDSP checkpoint or `dasp-pytorch` installed if used

## The note & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Through-line note: plucked string, mono, 44.1 kHz, ~1.5 s → ~66150 samples; `f₀` ≈ 110 Hz (A2).
  Real recording or placeholder? _(state which)_
- First ~10 partials (Phase 0.3): frequencies / amplitudes / rough T60s: _(table)_
- Inharmonicity coefficient `B` from `f_n = n·f₁·√(1 + B·n²)` (Phase 5.2): _(value)_
- Multi-scale spectral loss config: FFT sizes _(e.g. 64, 128, 256, 512, 1024, 2048)_, hop = size/4, L1 on magnitude + L1 on log-magnitude.
- Copy-synthesis fit (Phase 2.6): loss at iteration 0 / 50 / 500: _(values)_

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has computed/heard themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-differentiable-block.md`). The tutor
> watches for these, notes when one comes up, and revisits later to make sure it has stuck.

- "DDSP is a neural synthesizer" — no, **classical DSP is the output layer**; the net predicts parameters
- "just minimize waveform MSE" — phase- and cents-sensitive; use the **multi-scale spectral loss**
- "differentiable ⇒ easy to train" — frequency gradients oscillate, IIR recursion is unstable, FM has local minima
- "FIR approximation makes IIR problems vanish" — trades recursion for **memory and exactness**
- "parameter loss is fine when I have parameters" — perception is **many-to-one** in θ
- "spectral loss is a perceptual metric" — magnitude-only, weak on transients / inharmonic / noisy sounds
- "the learned model is a black box" — every learned quantity is a **named DSP parameter** you can read and edit
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 6.2) — tiered, no GPU required
> Picked partway through Phase 4 so it can shape the last few lessons.

- _(a) **CPU** — hand-built harmonic+noise+reverb model; gradient-descent copy synthesis of the note with the spectral loss; edit the learned parameters and A/B listen; one-page block report_
- _(b) **Colab GPU** — tier a, plus train a small DDSP autoencoder on a few minutes of monophonic audio and timbre-transfer the note through it_
- _(c) **Local GPU** — tier a, plus fit a grey-box effect (learnable biquad cascade or the Wright compressor) to the note; compare IIR-BPTT vs frequency-domain vs FIR-approximation training_
- Choice: _(not yet)_
