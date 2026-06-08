# The Latent Canvas — This Course's Keystone

Course 1 had **the fork**; course 2 had **the token grid**; this course has **the
latent canvas**. Course 1 stopped at the moment a neural codec turns the through-line
clip into a bottleneck — and showed that bottleneck can be *either* discrete RVQ
tokens *or* a **continuous VAE latent**. Course 2 walked the discrete branch
(language-model the tokens). **This course walks the other branch:** take the
*continuous* latent and **denoise it** out of pure noise with a **Diffusion
Transformer (DiT)**.

> **You have a continuous VAE latent — a grid of *real-valued* vectors, not symbol
> indices. A language model can't predict a real vector from a finite vocabulary. So
> how do you generate a *new* latent? Start from pure Gaussian noise and *denoise* the
> whole thing at once, over a few dozen steps, with a transformer over latent
> patches — conditioned on text (and timing).**

Every system in this course is a variation on that one move. Read this in Phase 0.1,
then return to it in **Phase 3** (the DiT — *how* you denoise), **Phase 5** (the
U-Net→DiT swap that scaled it to full songs), and **Phase 8.1** (where you place every
system on the map).

Every term in **bold** is earned somewhere in the syllabus; the phase is in brackets.

---

## The canvas

```
   pure-noise latent              denoised latent            waveform
   z_T  (Gaussian)     ──DiT──▶   z_0 (continuous)  ──VAE──▶   ♪ ♪ ♪
   ┌──┬──┬──┬──┬──┐    ~50        ┌──┬──┬──┬──┬──┐  decoder
   │▓▓│▓▓│▓▓│▓▓│▓▓│   steps       │░░│▒▒│██│▒▒│░░│
   │▓▓│▓▓│▓▓│▓▓│▓▓│  ─────────▶   │▒▒│██│░░│██│▒▒│
   │▓▓│▓▓│▓▓│▓▓│▓▓│  conditioned  │██│░░│▒▒│░░│██│
   └──┴──┴──┴──┴──┘  (text+time)  └──┴──┴──┴──┴──┘
   each cell = a real-valued PATCH (a vector), NOT a token index [Phase 3.2]
   the WHOLE canvas is denoised GLOBALLY at once — not filled cell-by-cell
```

- A cell here is a **patch** of the continuous latent — a *real-valued vector*
  [Phase 0.2]. Compare the **token grid** of course 2, whose cells were *integer
  codebook indices*. Same encoder/decoder skeleton from course 1; the thing in the
  middle is the **continuous** side of the fork.
- "Generate audio" = "**denoise a plausible latent**" out of noise, which the VAE
  decoder turns into a waveform. That is the entire job.
- **The decoding axis is the sharp contrast with course 2.** An autoregressive
  token-LM fills its grid **cell-by-cell, left to right**; a masked model fills it
  **by confidence**. Diffusion starts with the *whole* noisy canvas and refines **all
  of it simultaneously**, step after step. Global, not sequential. That is why it is
  called **full-context generation** [Phase 5.2] — and why, the field discovered, it
  doesn't need a semantic-token stage to stay coherent.

## The two halves of the keystone

### Half 1 — *how* you denoise: the DiT [Phase 3]

Early audio diffusion denoised the latent with a **U-Net** [Phase 1.2] — the
convolutional backbone inherited from image diffusion. **Peebles & Xie (2022)**
[Phase 3.2] showed you can throw the U-Net away and use a **plain transformer over
latent patches** instead:

- **Patchify** the latent into a sequence of patch tokens, embed them, run standard
  transformer blocks [Phase 3.2].
- Inject the **timestep** `t` and the **condition** `c` not by cross-attention but by
  **adaptive layer norm** — **adaLN-Zero**, the scale/shift on each LayerNorm computed
  from `(t, c)`, with the residual scale *zero-initialized* so training starts as the
  identity [Phase 3.3]. Cheapest mechanism, best FID.
- **It scales like a transformer:** more Gflops (smaller patch → more tokens, or
  deeper/wider) → **monotonically lower FID** [Phase 3.4]. The transformer scaling
  story, brought to diffusion.

The DiT is **not a diffusion-specific architecture** — it's an ordinary transformer
with timestep/condition conditioning via adaLN-Zero. That is the whole trick.

### Half 2 — *what* you denoise: a continuous VAE latent [Phases 4–5]

The object on the canvas is a **continuous VAE latent**, *not* the discrete RVQ tokens
of course 2. This is the single most-confused point in the field, and the cleanest
test of whether course 1's **fork** truly landed:

- **Stable Audio** [Phase 4] established the recipe — latent diffusion over a
  **fully-convolutional continuous VAE** (44.1 kHz stereo, up to ~95 s), with a
  **timing-conditioning** trick (`seconds_start`, `seconds_total`) for variable
  length — **but it is still a U-Net** (907M params), *not* a DiT.
- **Long-Form Latent Diffusion** [Phase 5.1] is the **U-Net → DiT swap**: a DiT in the
  continuous VAE latent (21.5 Hz latent rate), generating **full songs to 4m 45s**.
  This is **Stable Audio Open**'s backbone. It also made the field's boldest claim —
  see below.

## Diffusion vs flow — one objective swap [Phase 6]

The denoiser can be trained two closely-related ways. Classic **DDPM/score** diffusion
predicts the noise `ε` (equivalently the **score** `∇ log p`). **Rectified flow** /
flow matching instead learns a **straight-line velocity** from noise to data. Same
backbone (a DiT), different *target* — and the modern music DiTs (**FluxMusic**) use
rectified flow. The self-contained [`rectified-flow-primer.md`](rectified-flow-primer.md)
makes this precise and links to the [`flow-matching/`](../flow-matching/) course for
depth. "Flow matching is just diffusion" is the misreading to retire here [Phase 6.4].

---

## The misreadings this course exists to kill

Curated from the `diffusion/` and `ai-music-audio-gen/` wikis, and the
curriculum-wide list in course 1's [`the-fork.md`](../audio-codecs/the-fork.md). The
tutor flags each on the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "'audio codec → DiT' uses the discrete codec tokens." | The DiT denoises a **continuous VAE latent**, *not* discrete RVQ tokens — *"diffusion wants a smooth latent."* This is course 1's fork on home turf and the field's single most common confusion. | Phase 3.5, 4.1 |
| "Stable Audio is a DiT." | Stable Audio **v1 is a U-Net** (907M params) over a continuous VAE; the **DiT swap came one paper later** (Long-Form Latent Diffusion = Stable Audio Open's backbone). | Phase 4.3, 5.1 |
| "DiT is a diffusion-specific architecture." | A DiT is a **standard transformer** over latent patches with **adaLN-Zero** timestep/condition conditioning. Nothing about it is intrinsically "diffusion." | Phase 3.3, 3.5 |
| "Masked NAR generation = diffusion." | (Course 2's misreading, from the other side.) Masked models unmask **discrete tokens** by confidence; diffusion denoises a **continuous latent**. Different objects, different math. | Phase 0.2, 5.3 |
| "Semantic tokens are *required* for long-range coherence." | AudioLM (course 2) argued yes; **Long-Form Latent Diffusion** showed structure emerges from **full-context generation** with no semantic-token stage. The fork's branches reach coherence differently. | Phase 5.2 |
| "Flow matching is just diffusion." | Related (both transport noise → data) but a **different objective** — a straight-line **velocity** target, not noise/score. Same DiT backbone; FluxMusic uses rectified flow. | Phase 6.1, 6.4 |
| "Mel-VAE vs waveform-VAE is a paradigm change." | Both are **continuous VAE latents**; FluxMusic uses a mel-VAE, Stable Audio a waveform-VAE. The **DiT doesn't care** — it's a latent choice, not a fork. | Phase 6.4 |
| "AudioLDM 2 / ACE-Step have an LM inside, so they're codec-LMs." | They are **hybrids**: an LM **plans** (LOA features / lyrics + metadata), a **latent-diffusion DiT renders**. The renderer is still continuous-latent diffusion — the right branch of the fork. | Phase 2.2, 7.4 |
| "Diffusion needs 1000 steps, so it's hopelessly slow." | **DDIM** (~50 steps), ODE solvers (10–20), and **distillation** (4–8) collapse it; ACE-Step renders a full song in ~10 s. Step count is a sampler choice, not a law. | Phase 7.2 |

---

## How the course earns the canvas

| Piece | Earned in |
|---|---|
| diffuse in a *compressed continuous latent*, not raw audio (the LDM idea) | **Phase 1** |
| the audio-LDM family: text encoders, "language of audio," cascading long-form | **Phase 2** |
| *how* you denoise: U-Net → **transformer over patches + adaLN-Zero** (DiT) | **Phase 3** (keystone) |
| *what* you denoise: **continuous VAE** + timing conditioning (still a U-Net) | **Phase 4** |
| the **U-Net → DiT swap** + "semantic tokens not required" (full songs) | **Phase 5** (keystone) |
| swapping the objective: **rectified flow** + **MM-DiT** (FluxMusic) | **Phase 6** |
| full songs and the **LM-planner + DiT-renderer** hybrid (DiffRhythm, ACE-Step) | **Phase 7** |
| the full latent × backbone+objective map; both branches of the fork, closed | **Phase 8.1** |
