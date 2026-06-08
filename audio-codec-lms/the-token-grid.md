# The Token Grid — This Course's Keystone

Course 1 had **the fork**; this course has **the token grid**. Course 1 stopped at the
moment a neural codec turns the through-line clip into a **grid of discrete RVQ
tokens**. This whole course is one question about that grid:

> **You have `N_q` parallel token streams (codebook levels), each `T` frames long. A
> language model predicts *one* stream of symbols. How do you model `N_q × T` tokens
> with a sequence model — and in what order?**

Every system in the course is a different answer. Read this in Phase 0.1, then return
to it in **Phase 3** (the semantic→acoustic answer), **Phase 5** (the codebook-pattern
answer), and **Phase 8.1** (where you place every system on the map).

Every term in **bold** is earned somewhere in the syllabus; the phase is in brackets.

---

## The grid

```
            t=0   t=1   t=2   t=3   ...   t=T-1        time / frames  (≈75 Hz)
          ┌─────┬─────┬─────┬─────┬─────┬─────┐
  q=0     │  ·  │  ·  │  ·  │  ·  │ ... │  ·  │   coarse RVQ level  (structure-ish)
  q=1     │  ·  │  ·  │  ·  │  ·  │ ... │  ·  │
  q=2     │  ·  │  ·  │  ·  │  ·  │ ... │  ·  │        ↓ each cell = one codebook index
   ...    │ ... │ ... │ ... │ ... │ ... │ ... │          (a token, 0 .. K-1)
  q=Nq-1  │  ·  │  ·  │  ·  │  ·  │ ... │  ·  │   fine RVQ level   (timbre detail)
          └─────┴─────┴─────┴─────┴─────┴─────┘
   codebook levels (N_q)            a COLUMN = one frame, all levels
                                    a ROW    = one codebook level across time
```

- A **column** is one audio frame: `N_q` tokens that *together* reconstruct ~13 ms of
  sound. The levels are **residual** (course 1): `q=0` is coarse, each later level
  refines the leftover. They are **not** independent.
- "Generate audio" = "**produce a plausible grid**" that the codec decodes to a
  waveform. That's the entire job.

## The multi-stream challenge [Phase 5.1]

A vanilla autoregressive LM emits one symbol at a time from one vocabulary. The grid
has `N_q` symbols *per frame*. Three families of answer:

| Answer | What it does | System | Trade-off |
|---|---|---|---|
| **Hierarchical cascade** [Phase 3] | separate models, coarse→fine; semantic tokens then acoustic | **AudioLM**, **MusicLM** | highest coherence, complex multi-model pipeline |
| **Flat pattern** [Phase 5.2] | inline all `N_q` tokens of a frame into one long stream | **MusicGen** (flat) | best single-model quality, ~`N_q`× slower |
| **Delay pattern** [Phase 5.2] | offset stream `k` by `k` steps so one model predicts them staggered | **MusicGen** (delay) | most of the quality, much faster |
| **Stack-and-delay** [Phase 5.3] | group + offset streams | **Stack-and-Delay** | near-flat quality at near-delay speed |
| **Parallel (per-step)** [Phase 5.2] | predict all `N_q` streams at each step | MusicGen (parallel) | fastest, lowest quality |
| **Masked / NAR** [Phase 6] | start all-masked, unmask by confidence over ~10–40 iters, bidirectional | **VampNet**, **MAGNeT** | fast + **infill/editing**, slightly below best AR |

Two orthogonal knobs run through the table:
- **Reading order of the grid** — column-by-column (AR), staggered (delay), or
  confidence-first (masked). This is the *decoding* axis.
- **What conditions it** — nothing, an audio prompt, metadata, a joint text/audio
  embedding, a text-encoder, or a MIDI prompt. This is the *conditioning* axis
  [Phase 4]. Phase 8.1 is the full conditioning × decoding map.

## The other half of the keystone: semantic vs acoustic [Phase 3]

A codec's grid is all **acoustic** tokens — great fidelity, weak long-range structure;
modeled alone they **drift**. **AudioLM** adds a *second* kind of token:

- **Semantic** tokens (from self-supervised w2v-BERT): capture melody / rhythm /
  "syntax" but reconstruct poorly.
- **Acoustic** tokens (from the codec RVQ): capture fidelity but lack structure.

Generate **semantic first, then acoustic conditioned on it** → coherent *and*
high-fidelity. This split is *why* token-LMs achieve long-range structure — and it's
the field's most-conflated pair. (Live debate, settled in course 3: long-form diffusion
later challenged whether semantic tokens are *required*.)

---

## The misreadings this course exists to kill

Curated from the `ai-music-audio-gen` wiki (and the curriculum-wide list in course 1's
`the-fork.md`). The tutor flags each on the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "MusicGen is multi-stage." | **Single-stage.** One Transformer; a **codebook pattern** (flat/delay) serializes the `N_q` RVQ streams. The cascades were AudioLM/MusicLM. | Phase 5.2 |
| "Masked NAR generation = diffusion." | Both iterate non-left-to-right, but masked models predict **discrete tokens** by confidence-based unmasking; diffusion denoises **continuous latents**. Different objects, different math. | Phase 6.5 |
| "MIDI-VALLE / VALL-E are DiTs." | They are **codec language models** (discrete tokens, AR+NAR over RVQ). *Not* a diffusion transformer over a continuous latent. | Phase 7.3 |
| "Semantic tokens are the codec's tokens." | **Semantic** (self-supervised, structure) ≠ **acoustic** (codec RVQ, fidelity). AudioLM uses both, hierarchically. | Phase 3.2–3.4 |
| "More codebook levels are independent quality knobs." | RVQ levels are **residual & ordered** (course 1); a pattern must respect that the fine levels refine the coarse. | Phase 5.1 |
| "Text-to-music needs paired text–audio data." | **MuLan/CLAP** train a joint embedding contrastively and condition on the *audio* embedding at train time, *text* at inference — **audio-only** training. | Phase 4.2 |
| "Semantic tokens are *required* for long-range coherence." | AudioLM argued yes; **long-form latent diffusion** (course 3) showed coherence can emerge from full-context training. Open question, not a law. | Phase 3.4 |

---

## How the course earns the grid

| Piece | Earned in |
|---|---|
| why sample-level AR (WaveNet/SampleRNN) doesn't scale → tokenize first | **Phase 1** |
| tokens + Transformers = multi-minute music (Jukebox) | **Phase 2** |
| semantic→acoustic hierarchy (the coherence answer) | **Phase 3** (keystone) |
| text conditioning without paired data (MuLan/CLAP/T5) | **Phase 4** |
| one model + codebook patterns (MusicGen, Stack-and-Delay) | **Phase 5** (keystone) |
| masked/NAR for speed + infill (VampNet, MAGNeT) | **Phase 6** |
| the recipe travels: VALLE → MIDI-VALLE (codec-LM, *not* DiT) | **Phase 7** |
| the full conditioning × decoding map | **Phase 8.1** |
