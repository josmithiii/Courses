# AI Music & Audio — through-line asset

This directory holds the **shared through-line clip** for the
[`ai-music-audio`](../../ai-music-audio.md) curriculum: one short solo-piano phrase
carried, unchanged, across all three courses (encode → tokenize → denoise). See the
curriculum's **Through-line** section for how each course uses it.

## The clip (spec)

| Field | Value |
|-------|-------|
| Filename | `through-line.wav` *(to add)* |
| Content | A single solo-piano phrase, ~2 seconds |
| Format | Mono, 24 kHz, 16-bit PCM WAV (24 kHz matches common neural-codec sample rates) |
| License | **Must be freely redistributable** — public domain or CC0 — so it can ship in this repo |

## Status

⚪ **Clip not yet chosen.** Selection is a build-time task for course 1. When adding it:

1. Pick a public-domain / CC0 solo-piano source (or record an original and dedicate it CC0).
2. Trim to ~2 s, convert to mono 24 kHz, save as `through-line.wav` here.
3. Record provenance in `SOURCE.md` next to it: where it came from, the exact license,
   and the trim/convert command used (so it's reproducible).
