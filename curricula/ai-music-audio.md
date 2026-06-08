# AI Music & Audio

**Status:** 🟢 Complete — the spine is fixed and all three courses are authored
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
| 1 | [`../audio-codecs/`](../audio-codecs/) | 🟢 Active | The shared foundation: how raw audio becomes tokens and latents — and **the discrete-RVQ vs continuous-VAE fork** that splits the whole field downstream. |
| 2 | [`../audio-codec-lms/`](../audio-codec-lms/) | 🟢 Active | The first paradigm: generate audio by *language-modeling* codec tokens (AudioLM → MusicGen → VALLE/MIDI-VALLE). |
| 3 | [`../audio-diffusion-dit/`](../audio-diffusion-dit/) | 🟢 Active | The second paradigm: generate audio by *diffusion/flow* in a continuous VAE latent (AudioLDM → DiT → Stable Audio → DiffRhythm/ACE-Step). |

The codec/LM vs diffusion/DiT split is *the* organizing idea, so it is the **seam
between courses 2 and 3** — the structure teaches the distinction.

## Enrichment / co-requisites (parallel, not gates)

- [`../flow-matching/`](../flow-matching/) — its conditional-flow-matching / rectified-flow
  spine is the training objective behind FluxMusic and modern audio DiTs. Recommended
  *before or alongside* course 3, which ships a self-contained primer and links here for depth.
- [`../disentanglement/`](../disentanglement/) — *what a VAE latent encodes.* The representation
  side of the continuous-VAE branch (course 3's `latent canvas`): total correlation, the
  impossibility result, and pitch/timbre audio disentanglement. Any time after a VAE is
  understood; deepens *why* the latent is the thing we generate.
- [`../audio-ssl-representations/`](../audio-ssl-representations/) — *how a representation is
  learned without labels, and what it encodes.* The **encoder-side sibling** of `disentanglement/`:
  the pretext task and *the target shapes the representation* (wav2vec 2.0 → HuBERT → MERT),
  probing, and why an understanding-grade SSL encoder is **neither invertible nor disentangled**
  — the gap the resynthesis paradigm must close. The curriculum otherwise treats SSL only
  instrumentally (as the source of course 1/2's "semantic tokens"); this makes it a subject.
  Any time after the codecs course; pairs with `disentanglement/`.
- [`../ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) — a survey companion that
  can run in parallel; it already links the `music423-2023` meta-wiki.

### Capstone (the destination the thread feeds)

- [`../neural-audio-resynthesis/`](../neural-audio-resynthesis/) — the **capstone meta-course**:
  *creating and editing audio with neural methods.* Not a new body of theory but an **integration
  course** — it **surveys** the field (parametric/DDSP → codec-LM → continuous-VAE/DiT →
  resynthesis-as-editing), then **drills the load-bearing survivors** into the **encode→steer→decode**
  loop: an SSL conditioning latent (`audio-ssl-representations/`) + a disentangling inductive bias
  (`disentanglement/`) + a rectified-flow-DiT decoder (`flow-matching/` + course 3) = the
  resynthesis paradigm (static recording → **steerable object**), closing on the **no-reference
  evaluation** problem and the open frontier. Where the enrichment courses each teach **one box** of
  the loop, this **assembles the loop** and asks what it would take to *steer* it. **Plunge-in
  friendly — no hard prereq gates** (strong recommendations + recall-primers). Pinned to the shared
  piano clip — *resynthesize a variation that preserves identity, A/B listen.* The curriculum is
  complete; this is the capstone it points to.

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
