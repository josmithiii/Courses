# Differentiable & Physical Audio DSP — through-line asset

This directory holds the **shared through-line note** for the
[`audio-differentiable-dsp`](../../audio-differentiable-dsp.md) curriculum: one
**plucked electric-guitar note** carried, unchanged, across all three courses —
resynthesized by a learned harmonic+noise model (`audio-ddsp`), inverted to synthesizer
and effect parameters (`audio-synth-effect-matching`), and modeled as a physical string
(`audio-physics-informed`). See the curriculum's **Through-line** section for how each
course uses it.

## The note (spec)

| Field | Value |
|-------|-------|
| Filename | `note.wav` |
| Content | One plucked **low E** string (E2, `f₁` ≈ 82 Hz) on an electric guitar, **single-coil pickup**, plectrum, *mf*, no amplifier or effects; attack included, natural decay |
| Duration | 6.000 s (264 600 samples): untouched for 5 s, then an exponential fade (τ = 0.15 s) so the tail dies to silence instead of being cut |
| Format | Mono, 44.1 kHz, 16-bit PCM WAV, peak-normalized to −1 dBFS |
| Source | `SingleCoil3-E2-f0-E2-bp06-plectrum-mf.wav` (JOS, 35 s, same format) — kept here as the raw source |
| License | **CC0 1.0** (recorded and dedicated by JOS) — see [`SOURCE.md`](SOURCE.md) |

Why this note: it is a real **stiff steel string** (inharmonicity `B` is measurable —
course 3's equation), harmonic enough for a harmonic+noise model (course 1), and simple
enough for a two-parameter toy synth (course 2). Six seconds rather than two because the
decay carries **interesting modulation in the partials**: the FFT shows *doublets* around
each harmonic (e.g. ≈244/248 Hz, ≈330/331 Hz, ≈410/412/414 Hz), so partials **beat**
against each other as the note decays — the two polarizations of string motion, slightly
detuned, seen through a pickup at one position. That beating, plus the pickup's
position comb-filtering and any magnetic nonlinearity, is exactly the "what the network
must learn" residue the physics courses talk about. A harmonic model with one sinusoid
per harmonic *cannot* reproduce it; let the learner discover that by ear.

Numbers the courses reuse (measure them properly in each course's Phase 0.3; these are
sanity values): `f₁` ≈ 82.1 Hz; the 2nd partial is the strongest; RMS falls from ≈ −16 dB
to ≈ −40 dB over the first 5 s.

## Status

🟢 **Real recording in place** (2026-09-11). Regenerate `note.wav` from the source with:

```bash
python3 condition_note.py       # onset-aligns, trims to 6 s, exponential tail, -1 dBFS → note.wav
```

A deterministic **synthetic placeholder** (Karplus–Strong, E2, 6 s, labelled
`note-placeholder.wav`, gitignored) is still available for the physics course's
"synthetic vs real string" comparison and as a last-resort fallback:

```bash
python3 make_note.py            # writes note-placeholder.wav
```

Tutors must **never** silently treat the placeholder as `note.wav`: if `note.wav` is
missing, say so, and offer the placeholder explicitly as a placeholder.
