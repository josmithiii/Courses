# AI Music & Audio

**Status:** 🟡 Building — the spine is fixed; the three courses are authored in order
(see [`../AiMusicAudioPlan.md`](../AiMusicAudioPlan.md) for the full design spec).

## Goal

Take a learner who knows modern deep learning *in general* (MLPs, CNNs, Transformers,
LLMs, basic diffusion) and bring them to the **2026 state of the art in AI music and
audio generation** — able to explain, contrast, and *run* both dominant paradigms:

- **codec → language model** (discrete tokens + a sequence model), and
- **continuous-VAE latent → diffusion transformer** (DiT),

and to place 2024–2026 systems (Stable Audio, FluxMusic, DiffRhythm, ACE-Step,
MusicGen, MIDI-VALLE) on that map.

**Who it's for.** Anyone who has finished [`../ai-foundations/`](../ai-foundations/)
(or has equivalent ML background) and wants the audio-generation specialization.
No DSP background assumed — the first course builds the needed audio intuition briskly.

## Prerequisite

- [`../ai-foundations/`](../ai-foundations/) **(required)** — MLP → backprop → PyTorch →
  CNNs → attention/Transformers → LLMs → *basic* diffusion. That is exactly the entry
  frontier for the codecs course.

## Ordered course list

| # | Course | Status | Why here |
|---|--------|--------|----------|
| 1 | [`../audio-codecs/`](../audio-codecs/) | ⚪ Planned | The shared foundation: how raw audio becomes tokens and latents — and **the discrete-RVQ vs continuous-VAE fork** that splits the whole field downstream. |
| 2 | [`../audio-codec-lms/`](../audio-codec-lms/) | ⚪ Planned | The first paradigm: generate audio by *language-modeling* codec tokens (AudioLM → MusicGen → VALLE/MIDI-VALLE). |
| 3 | [`../audio-diffusion-dit/`](../audio-diffusion-dit/) | ⚪ Planned | The second paradigm: generate audio by *diffusion/flow* in a continuous VAE latent (AudioLDM → DiT → Stable Audio → DiffRhythm/ACE-Step). |

The codec/LM vs diffusion/DiT split is *the* organizing idea, so it is the **seam
between courses 2 and 3** — the structure teaches the distinction.

## Enrichment / co-requisites (parallel, not gates)

- [`../flow-matching/`](../flow-matching/) — its conditional-flow-matching / rectified-flow
  spine is the training objective behind FluxMusic and modern audio DiTs. Recommended
  *before or alongside* course 3, which ships a self-contained primer and links here for depth.
- [`../ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) — a survey companion that
  can run in parallel; it already links the `music423-2023` meta-wiki.

## Through-line

One shared **~2-second solo-piano phrase** is carried across all three courses (per-course
worked examples can still specialize):

- **Course 1** — *encode* it: waveform → mel → VAE latent → VQ tokens → RVQ codebooks,
  then reconstruct and **listen** at each bitrate.
- **Course 2** — *tokenize* it into a codebook×frame grid; **continue** it (AR),
  **infill** it (masked), **condition** it on text.
- **Course 3** — take its VAE latent and **denoise** it step-by-step; generate a variation.

Same clip, three paradigms — the through-line *is* this curriculum's spine made audible.
The clip and its license live in [`assets/ai-music-audio/`](assets/ai-music-audio/).

## Source of truth

The courses *teach from* and *link into* the curated wikis (canonical) while staying
pedagogical themselves. Keep courses in sync when the wikis gain papers.

- `/w/music423-2023/ai-audio-codecs/wiki/` — course 1.
- `/w/music423-2023/ai-music-audio-gen/wiki/` — courses 2 & 3 (codec-LM and diffusion halves).
- `/w/music423-2023/diffusion/wiki/` — course 3.
