# Music 423 — AI for Music & Audio (meta-curriculum)

**Status:** 🟡 Partial — Tracks A and C complete, Track B started.

This is the umbrella over the paper collection in JOS's
[`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023) repo (Stanford
Music 423 reading list): ~300 PDFs in ~25 topic directories, each with an AI-generated
wiki. Where an ordinary curriculum is *one* ordered sequence of courses, this file is a
**map of parallel tracks** — pick the one that matches your interest, or run two side by
side. Every track is a curriculum of its own (linked below); this page only says what
the tracks are, what each assumes, and which topic directories each one covers.

## Goal

Bring a CCRMA-style learner — musician, engineer, or DSP person — to the point of
**reading the primary papers in the collection fluently** and running the systems they
describe. The collection has several lineages that only partly overlap: audio *generation*
(codecs → codec-LMs and continuous-VAE → diffusion/DiT), *language models and sequence
models* (attention → Transformers → LLMs → Mamba-era state-space models), and
*differentiable / physical audio DSP* (DDSP, synth and effect parameter estimation,
physics-informed models). Most people at CCRMA arrive with interest in one lineage, not
all three, so the tracks are **parallel choices, not a required order**.

**Who it's for.** Anyone from "never trained a network" to "reads arXiv daily". The
on-ramps below are for the first group; experienced readers skip straight to a track.

## On-ramps (take what you need, skip what you have)

Two independent kinds of background, each with a self-paced route:

| You need… | Route | Notes |
|---|---|---|
| **Machine-learning background** (MLP, backprop, PyTorch, CNNs, attention, Transformers, LLMs, diffusion) | [`../ai-foundations/`](../ai-foundations/) | Beginner-friendly, intuition first; Python taught just-in-time. Exactly the entry frontier every track below assumes. |
| **Audio / spectral signal-processing background** (DFT, STFT, windows, filters, spectral models, physical models) | JOS's four online books, in order: [*Mathematics of the DFT*](https://ccrma.stanford.edu/~jos/mdft/) → [*Introduction to Digital Filters*](https://ccrma.stanford.edu/~jos/filters/) → [*Spectral Audio Signal Processing*](https://ccrma.stanford.edu/~jos/sasp/) → [*Physical Audio Signal Processing*](https://ccrma.stanford.edu/~jos/pasp/) | Each book is a self-paced online course in its own right (worked examples, exercises, code). *MDFT* and *SASP* are also tutored courses here: [`../mdft/`](../mdft/) → [`../sasp/`](../sasp/). The audio tracks link into them for depth rather than re-deriving DSP. ML-first learners can read *MDFT* and the first chapters of *SASP* and move on. |

Neither on-ramp is a gate. `ai-foundations` is the *recommended* first course for anyone
with little or no ML background; the books are the recommended background for the
DSP-heavy track and for anyone who wants to know what an STFT actually is.

## Tracks (parallel choices)

| # | Track | Curriculum | Status | Interest served | Topic directories in `music423-2023` |
|---|---|---|---|---|---|
| A | **AI Music & Audio Generation** — codecs, codec-LMs, diffusion/DiT, resynthesis | [`ai-music-audio.md`](ai-music-audio.md) | 🟢 Complete | Diffusion, neural codecs, VAEs, DiTs, self-supervised audio, disentanglement — the "how do modern generators actually work" lineage. | `ai-audio-codecs/`, `ai-music-audio-gen/`, `diffusion/`, `diffusion-vocoders/`, `wavenet/`, `disentanglement/`, `images/` (VAE, GAN, U-Net, DiT backbones), `ai-scores/` (planned enrichment) |
| B | **LLMs & Sequence Models** — attention → Transformers → LLMs → state-space models | [`ai-llms-and-sequence-models.md`](ai-llms-and-sequence-models.md) | 🟡 Partial | Language models, attention, long-context and Mamba-era architectures, RL and alignment, multimodal — the "general AI backbone" lineage. | `attention/`, `natural-language-processing/`, `mamba/`, `rwkv/`, `gated-recurrence/`, `hybrid/`, `reinforcement-learning/`, `multimodal/`, `images-ar/`, `double-descent/` |
| C | **Differentiable & Physical Audio DSP** — DDSP, synth/effect matching, physics-informed | [`audio-differentiable-dsp.md`](audio-differentiable-dsp.md) | 🟢 Complete | Signal-processing people who want ML *inside* the DSP: differentiable filters/synths, inverting effects and synthesizers, modal and physical models with learned parts. Leans on JOS's books. | `ddsp/`, `synth-effect-matching/`, `modal-synthesis/`, `pinn/`, `DRC/`, `ai-misc/` (spectrogram inversion etc.) |

**Cross-cutting companion (any track):**
[`../ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) — the paper-by-paper history
of the field, DBN 2006 → GPT-4 2023, read from the
[`ai-2012-to-2023/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-2012-to-2023)
and [`history/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/history)
directories. It is not a track; it is the timeline every track sits on, and it runs
comfortably alongside any of them.

### Choosing

- Interested in **generating or editing audio** with neural nets → Track A. This is the
  most complete track and has a capstone (`neural-audio-resynthesis`).
- Interested in **how LLMs and their successors work**, or want to read the attention /
  Mamba / RWKV papers → Track B.
- A **DSP or acoustics person** who wants neural methods to fit *your* toolbox (filters,
  synthesizers, effects, physical models) → Track C, with the books as the base.
- **Unsure** → `ai-foundations` first; its last phase touches all three lineages and you
  will know which one pulled you.

Two tracks in parallel is normal — A and C share the DSP books and the `ddsp/`
material; A and B share the Transformer / codec-LM material.

## Through-line

There is no single worked example across tracks (each track has its own — Track A's
shared piano clip, Track B's small language model, Track C's one plucked-string note).
What the tracks share is the **collection itself**: every course teaches *from* a
`music423-2023` topic wiki and links back into the PDFs there, so a learner on any
track ends up able to open any directory in the repo and read it.

## Source of truth

The [`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023) repo — its
per-topic `wiki/` directories are the canonical record; the courses are the front-end.
The repo's own README carries the same track map from the papers' side.

## Not covered (deliberately)

Courses in this repo outside the collection's scope — `crypto-foundations`,
`quantum-states`, the Buddhism curriculum, `agents101`, `room-acoustics` — are not part
of this meta-curriculum. `room-acoustics` is a good side course for Track C people but
teaches from its own sources, not the collection.
