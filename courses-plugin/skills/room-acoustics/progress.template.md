# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Acoustics background: _(none / hobbyist / some physics of sound / worked with reverb or RIRs)_
- Signal processing: _(none / knows "convolution" and "impulse response" / comfortable / strong DSP)_
- Python: _(none / beginner / comfortable / strong)_
- Math comfort (logs, sqrt, simple integrals): _(rusty / comfortable / fluent)_
- Why she's here / goal: _(understand the Treble-vs-Odeon answer / evaluate a specific room / general curiosity / ML-RIR & ANC work)_
- Lean: _(hands-on — measure & compute / conceptual — understand & interpret)_
- Has a mic + audio interface for real measurement? _(yes / no — affects capstone choice)_
- Time budget: ~1 hour/day
- Style: patient, picture-first, every term defined on first use, every quantity
  pinned to the shoebox room (5×4×3 m, V=60 m³) and the concert-hall foil (V≈15000 m³)

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The one-picture story (below vs. above Schroeder), after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] Python + `numpy` + `scipy` + `matplotlib` importable
- [ ] `pyroomacoustics` importable (image-source sim + RT/parameter estimators)
- [ ] (hands-on track) `sounddevice` working — can play and record audio
- [ ] (optional) Room EQ Wizard (REW) installed
- [ ] A scratch `.py` file or notebook open and used during sessions
- [ ] `motivating-question.md` read (the north-star Treble-vs-Odeon exchange)

## The two reference rooms (numbers we reuse)
> Filled in as we compute them; keep consistent across lessons.

- Shoebox: 5.0 × 4.0 × 3.0 m, V = 60 m³, S = 94 m². Lowest axial mode ≈ 34.3 Hz.
  Target RT60 ≈ 0.5 s @ 500 Hz. Mean free path 4V/S ≈ 2.55 m.
  **Schroeder frequency ≈ 183 Hz.**
- Concert-hall foil: V ≈ 15 000 m³, RT60 ≈ 2 s. **Schroeder frequency ≈ 23 Hz.**

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has computed by hand or in Python, kept as
> reference for later lessons. Add a one-line entry each session.

- (none yet)

## Common confusions to revisit
> The perennial traps in this subject. The tutor watches for these, notes when one
> comes up, and revisits later to make sure it has stuck.

- Two different Schroeders: the *frequency* (modal crossover) vs. the *backward integration* (decay-curve method)
- "RT60 is one number" — it's frequency-dependent (per octave band)
- "GA is just a worse approximation" — above Schroeder it's correct *and* cheaper
- "More reverb = richer" — clarity (early) vs. reverberance (late) trade off; speech vs. music differ
- Absorption coefficient (energy removed) vs. scattering coefficient (energy spread)
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.2)
> Picked partway through Phase 6 so it can shape the last few lessons.

- _(a) Python from scratch — measure a real room (sine sweep → RIR → parameters) or simulate one with pyroomacoustics; write a one-page room report_
- _(b) REW + light Python — measure in REW, reproduce a couple of parameters in Python_
- _(c) Dataset / conceptual — analyze a simulated "control room" vs. "hall", tie every difference back to Schroeder_
- Choice: _(not yet)_
