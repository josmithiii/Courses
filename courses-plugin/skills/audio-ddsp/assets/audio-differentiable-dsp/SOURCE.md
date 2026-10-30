# `note.wav` — provenance & license

The shared through-line note for the
[`audio-differentiable-dsp`](../../audio-differentiable-dsp.md) curriculum: one plucked
electric-guitar low-E note carried, unchanged, across all three courses (resynthesize →
invert → model the string).

## Source

- **Recording:** `SingleCoil3-E2-f0-E2-bp06-plectrum-mf.wav` — recorded by **Julius O.
  Smith III (JOS)** as part of his single-coil electric-guitar pickup recordings
  (filename fields: pickup *SingleCoil3*, open low-E string, nominal pitch E2, plectrum,
  *mf* dynamic). Direct pickup signal, no amplifier or effects.
- **Source format:** mono, 44.1 kHz, 35.0 s, peak 0.55 FS, noise floor ≈ −79 dB RMS.
  The raw file is kept in this directory alongside the conditioned `note.wav`.
- **Copied into this repo:** 2026-09-11.

## License

**CC0 1.0 Universal — Public Domain Dedication.** The recording is by Julius O. Smith III,
who dedicates both the raw source file and the conditioned `note.wav` to the public
domain (confirmed 2026-09-11). Learners may copy, modify, redistribute, and include the
note in capstone reports, for any purpose, without permission or attribution. Attribution
is appreciated but not required.

## What we ship vs. the source

`note.wav` is the first 6 s of the source, onset-aligned and conditioned:

| Field | Value |
|-------|-------|
| Duration | 6.000 s (264 600 samples) |
| Channels | mono |
| Sample rate | 44 100 Hz |
| Encoding | 16-bit PCM WAV |
| Level | peak-normalized to −1 dBFS |
| Window | starts 30 ms before the detected pluck onset (source 0.278 s → start 0.248 s); untouched for 5.0 s; then multiplied by `exp(−t/0.15 s)` for the final 1.0 s (≈ −58 dB at the end) |

The exponential tail is a *window*, not a fade-to-cut: the note is still decaying
naturally at 5 s (≈ −40 dB RMS) and the window takes it smoothly to silence.

## Reproduce

```bash
python3 condition_note.py     # reads the source file above, writes note.wav (deterministic)
```

Parameters (pre-onset margin, untouched length, total length, fade time constant, peak
level) are constants at the top of `condition_note.py`; change them there and re-run.
