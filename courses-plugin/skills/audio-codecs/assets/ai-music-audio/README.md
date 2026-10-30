# AI Music & Audio — through-line asset

This directory holds the **shared through-line clip** for the
[`ai-music-audio`](../../ai-music-audio.md) curriculum: one short solo-piano phrase
carried, unchanged, across all three courses (encode → tokenize → denoise). See the
curriculum's **Through-line** section for how each course uses it.

## The clip (spec)

| Field | Value |
|-------|-------|
| Filename | `through-line.wav` |
| Content | Opening phrase of Chopin's *Waltz in A minor*, B. 150, solo piano (~2.2 s) |
| Format | Mono, 24 kHz, 16-bit PCM WAV (24 kHz matches common neural-codec sample rates) |
| License | **CC0 1.0** (public-domain dedication of both composition and recording) — freely redistributable |

## Status

🟢 **Clip chosen and in place** (2026-06-07). A CC0 solo-piano phrase from a Wikimedia
Commons recording (Aya Higuchi performing Chopin's B. 150), trimmed to ~2 s and
conditioned to spec. Full provenance, the verbatim license, and the exact
trim/convert/normalize commands are in [`SOURCE.md`](SOURCE.md).
