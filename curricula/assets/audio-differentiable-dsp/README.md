# Differentiable & Physical Audio DSP — through-line asset

This directory holds the **shared through-line note** for the
[`audio-differentiable-dsp`](../../audio-differentiable-dsp.md) curriculum: one short
**plucked-string note** carried, unchanged, across all three courses — resynthesized by a
learned harmonic+noise model (`audio-ddsp`), inverted to synthesizer and effect parameters
(`audio-synth-effect-matching`), and modeled as a physical object (`audio-physics-informed`).
See the curriculum's **Through-line** section for how each course uses it.

## The note (spec)

| Field | Value |
|-------|-------|
| Filename | `note.wav` |
| Content | One plucked nylon-string guitar note, open A (A2, f₁ ≈ 110 Hz), attack included, ~1.5 s, natural decay, no reverb |
| Format | Mono, 44.1 kHz, 16-bit PCM WAV (44.1 kHz keeps the full partial series a DSP learner expects; the ML-first curricula use 24 kHz) |
| License | Must be **CC0 1.0** or recorded by us — freely redistributable, provenance recorded in `SOURCE.md` |

Why a plucked string: it is harmonic enough for a harmonic+noise model (course 1),
simple enough for a two-parameter toy synth (course 2), and governed by the 1-D damped
stiff-string equation the physics course derives (course 3). One note, three models.

## Status

⚪ **Real recording not yet chosen.** Until it is, a deterministic **synthetic
placeholder** can be generated on demand:

```bash
python3 make_note.py            # writes note-placeholder.wav (Karplus–Strong, A2, 44.1 kHz, 1.5 s)
```

The placeholder is a Karplus–Strong plucked string (extended with a one-pole loop
filter and a fixed random seed, so every learner gets the *same* file). It is **labelled
as a placeholder** by its filename. The courses' tutors must **never** silently treat
`note-placeholder.wav` as `note.wav`: if `note.wav` is missing, the tutor says so, offers
the placeholder explicitly (a legitimate Phase 0.2 task is to generate it and listen to
what a synthetic pluck lacks), or helps the learner record/select a real note. Course 3
in particular should note that fitting a physical model to a *synthetic* string is a
sanity check, not the real exercise.

When a real recording is chosen: trim to ~1.5 s from just before the attack, convert to
mono 44.1 kHz 16-bit, normalize to −1 dBFS peak, save as `note.wav`, and record the
source, license text, and exact commands in `SOURCE.md` (mirror
[`../ai-music-audio/SOURCE.md`](../ai-music-audio/SOURCE.md)).
