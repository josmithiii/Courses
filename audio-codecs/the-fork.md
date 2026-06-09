# The Fork — This Course's Keystone

Room-acoustics has the Schroeder frequency; flow-matching has the
conditional-expectation identity. **This course has the fork.** One representational
choice, made inside a neural audio codec, splits the entire field of AI audio
generation into the two paradigms taught next in this curriculum. Read this in
Phase 0.1, then return to it in **Phase 2.4** (where the fork first appears in the
pipeline), **Phase 5** (where we spend as long as it takes), and **Phase 7.1**
(where you recite both branches from memory).

Every term in **bold** is earned somewhere in the syllabus; the phase that earns it
is noted in brackets.

---

## The fork, in one sentence

> A neural audio codec compresses a **waveform** [Phase 1] through a **convolutional
> encoder** [Phase 2.2] into a **bottleneck** [Phase 2.1], and that bottleneck is
> *either* a stack of **discrete RVQ token indices** [Phase 4] *or* a **continuous VAE
> latent** [Phase 2.4] — and which one you choose **determines the entire downstream
> generation paradigm.**

```
                                            ┌── discrete RVQ tokens ──▶ a LANGUAGE MODEL
   waveform ──▶ conv encoder ──▶ bottleneck │      (symbols → next-token prediction)
                                            │      AudioLM → MusicGen → VALLE
                                            │      = course 2  (audio-codec-lms)
                                            │
                                            └── continuous VAE latent ──▶ DIFFUSION / FLOW
                                                   (vectors → denoise)
                                                   AudioLDM → Stable Audio → DiT
                                                   = course 3  (audio-diffusion-dit)
```

## Why this is *the* keystone

The same encoder–decoder skeleton serves both branches. The *only* thing that
changes is the shape of the thing in the middle:

- **Discrete** → each latent frame is rounded to the nearest entry of a learned
  **codebook** [Phase 3], so it's an **integer index** — a *symbol*. A sequence of
  symbols from a finite vocabulary is exactly what a **Transformer language model**
  consumes. So "generate audio" becomes "**predict the next codec token**" [Phase 5.2].
  Residual VQ [Phase 4.1] stacks several codebooks so the symbol grid is rich enough
  to reconstruct well.

- **Continuous** → the latent frame stays a **real-valued vector**, regularized by a
  **VAE** [Phase 2.4] into a smooth distribution. Smooth continuous vectors are exactly
  what **diffusion / flow** denoise. So "generate audio" becomes "**denoise a VAE
  latent**" [Phase 5.3].

Get the fork, and the rest of the curriculum is two elaborations of it. Miss it, and
courses 2 and 3 look like unrelated bags of tricks instead of the two children of one
choice.

## The reconstruction route doesn't change — only the generator does

Crucially, **both** branches still *decode* the same way: latent (tokens or vector)
→ decoder → waveform. The fork is about how you **generate** a *new* bottleneck, not
about how you turn a bottleneck back into sound. Course 1 builds the encoder/decoder
and the bottleneck; courses 2 and 3 each build a different *generator* for the
bottleneck.

## The fork made literal: DAC → DACVAE

The fork is not just a teaching abstraction — someone shipped *both sides of it on the
same codebase*. **DAC** [Phase 4.5] is the discrete branch: DAC's encoder → **RVQ**
[Phase 4.1] → decoder. **DACVAE** (Meta, in *Movie Gen*, Polyak et al. 2024) is the
*same DAC encoder/decoder and the same multi-scale STFT discriminators + Snake
activation* — with **one change at the bottleneck: the RVQ is deleted and replaced by a
VAE objective with KL regularization** [Phase 2.4]. Same skeleton, forked at the middle:

```
   DAC      :  enc ──▶ [ RVQ codebooks ]  ──▶ dec      ▶ discrete tokens  → language model (course 2)
   DACVAE   :  enc ──▶ [ VAE  +  KL    ]  ──▶ dec      ▶ continuous latent → diffusion/flow (course 3)
              └────────── identical ──────────┘
                         (only the box in brackets differs)
```

Why Meta did it, in their words: *discrete tokens are not necessary for diffusion-style
models*, so they removed the RVQ and trained the same backbone with a VAE objective —
which **improves reconstruction**, especially at an aggressively compressed frame rate.
In *Movie Gen* the resulting continuous latent is then denoised by a **flow-matching**
generator (course 3's paradigm, and exactly why course 3 leans on `flow-matching/`).

Concrete numbers worth carrying: DACVAE in *Movie Gen* encodes **48 kHz** audio to a
**25 Hz**, **128-dim** continuous latent — vs the EnCodec [Phase 4.5] continuous-feature
baseline of **75 Hz / 128-dim at 24 kHz**. So DACVAE is *lower frame rate, higher sample
rate, higher fidelity* — a continuous latent built specifically to be a good diffusion
substrate. (The numbers are config-dependent; these are the *Movie Gen* settings.)

DACVAE is the cleanest possible refutation of the field's most common confusion: *"audio
codec → diffusion must mean the diffusion model consumes the discrete codec tokens."* No
— Meta **explicitly removed** the discrete quantizer precisely *because* the diffusion
model wants the continuous latent. The codec and the fork are one `git diff` apart.

> *Canonical wiki:* the `ai-audio-codecs` wiki threads DAC-VAE through its existing codec
> pages — the **DAC-VAE** section of `sources/descript-rvqgan.md` (the 48 kHz / 25 Hz /
> 128-d config and why the RVQ is dropped), the **"Two Bottlenecks: Discrete RVQ vs.
> Continuous VAE"** subsection of `neural-audio-codecs.md`, and a **"Continuous Codec
> Latent (VAE)"** representation in `audio-representations.md` — each cross-linked to
> Meta's *Movie Gen* page in the sibling `diffusion/` wiki.

---

## The misreadings this course exists to kill

These are the conflations curated out of the `ai-audio-codecs` /
`ai-music-audio-gen` wikis (several were corrections made during that curation). The
tutor flags each on the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "A neural codec is *just* a VAE." | **Discrete RVQ vs continuous VAE is the fork**, not a detail. They feed different paradigms. | Phase 2.4, 5 |
| "More RVQ codebooks just = more quality knobs." | RVQ is **residual refinement** — each stage quantizes the *previous stage's leftover*; the stages are ordered and interdependent. | Phase 4.1 |
| "Discrete codec tokens are lossless." | They're a **lossy** quantization; more codebooks reduce but never eliminate the loss. | Phase 4.1–4.2 |
| "'audio codec → DiT' uses the discrete codec tokens." | The DiT denoises a **continuous VAE latent**, *not* discrete RVQ tokens. This is the single most common confusion in the field. **DACVAE** is the proof: Meta *deleted* DAC's RVQ and trained a VAE bottleneck precisely so a diffusion/flow model could use the continuous latent. | Phase 5.3–5.5 |
| "Semantic and acoustic tokens are the same thing." | **Semantic** tokens (self-supervised, structure/melody) vs **acoustic** tokens (codec RVQ, fidelity) carry complementary information; AudioLM uses both. | Phase 6.1 |
| "Waveform-L2 (MSE) measures audio quality." | The ear hears artifacts L2 doesn't penalize; use **spectral / perceptual** metrics (ViSQOL, MUSHRA), and **adversarial** training to fix what L2 misses. | Phase 2.3, 4.4, 6.3 |
| "VQ trains end-to-end like any layer." | `argmin` over a codebook has **zero gradient**; the **straight-through estimator** is what makes it trainable. | Phase 3.2 |
| "A bigger codebook always helps." | Bigger codebooks invite **collapse** (most codes unused); the fixes (EMA, k-means init, factorized lookup, FSQ) are a whole subtopic. | Phase 3.4 |

---

## How the course earns the fork

| Piece of the fork | Earned in |
|---|---|
| waveform, sampling, mel | **Phase 1** |
| encoder / decoder, bottleneck, frame rate | **Phase 2** |
| continuous VAE latent (the diffusion-feeding branch) | **Phase 2.4** |
| discrete tokens, codebook, straight-through, collapse | **Phase 3** |
| residual VQ, bitrate, real codecs (SoundStream/EnCodec/DAC) | **Phase 4** |
| **the fork stated precisely + both downstream paradigms** | **Phase 5** (the keystone) |
| **DAC → DACVAE: the fork as one bottleneck swap on one codebase** | **Phase 5.5** |
| semantic vs acoustic tokens; the right metric | **Phase 6** |
| reciting both branches end-to-end on the clip | **Phase 7.1** |
