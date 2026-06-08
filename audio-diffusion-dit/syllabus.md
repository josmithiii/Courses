# Audio Diffusion & the DiT — Generating Audio by Denoising a Latent

**Learner profile:** Has finished `audio-codecs/` (course 1) and `audio-codec-lms/`
(course 2) of this curriculum — so they know the discrete-vs-continuous **fork**, what
a **continuous VAE latent** is, the **token grid** the language-model branch generates,
and they've encoded, heard, continued, and infilled the through-line clip. They arrive
from `ai-foundations/` with Transformers, LLMs, and *basic* diffusion already in hand.
This course is the **right branch of the fork**: take the continuous latent and
**denoise it** with a Diffusion Transformer. ML-first; no new DSP. ~1 hour per day, one
concept at a time, every concept checked with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisites:** `audio-codecs/` (the **continuous-VAE branch** of its fork is this
course's starting line) and `audio-codec-lms/` (so the *contrast* — predict discrete
tokens vs denoise a continuous latent — lands). `ai-foundations/` Phase 6 supplies
basic diffusion; this course re-grounds it in Phase 0.2 and goes far past it.
**Enrichment (not a gate):** `flow-matching/` — recommended before or alongside Phase 6,
which ships a self-contained [`rectified-flow-primer.md`](rectified-flow-primer.md) and
links there for depth.

**The keystone — read [`the-latent-canvas.md`](the-latent-canvas.md) in Phase 0.1.**
This course has one organizing object, the analogue of course 1's fork and course 2's
token grid: the **latent canvas** — a *continuous* VAE latent denoised out of pure
noise — and one question, *how do you generate a new latent when its cells are real
vectors, not symbols?* The answer has two halves we spend as long as it takes on:
**how** you denoise (**Phase 3**, the **DiT**: transformer over patches + **adaLN-Zero**)
and **what** you denoise (**Phases 4–5**, the **continuous VAE latent**, and the
**U-Net → DiT swap** that scaled it to full songs).

**The qubit (worked example):** the curriculum's shared **~2-second solo-piano clip**
(`../curricula/assets/ai-music-audio/through-line.wav`, mono 24 kHz). Course 1 *encoded*
it; course 2 *predicted* from its token grid; **here we *denoise* it.** Carry its
**continuous VAE latent** through every system: watch noise resolve into the clip's
latent step-by-step, generate variations, and (warm-up) denoise `flow-matching`'s 2-D
two-moons before lifting to the audio latent. Same clip, the third paradigm — *heard*.

**End state:** by the last lesson the learner can: explain why we diffuse a **compressed
continuous latent** rather than raw audio; lay out the **audio-LDM family** (AudioLDM →
Tango → AudioLDM 2 → Noise2Music/Moûsai) and what each fixed; explain the **DiT** —
patchify, **adaLN-Zero**, and why it scales — and state precisely that it denoises a
**continuous VAE latent, not discrete tokens**; explain **Stable Audio**'s continuous
VAE + **timing conditioning** and why **v1 is a U-Net, not a DiT**; explain the **U-Net →
DiT swap** (Long-Form Latent Diffusion / Stable Audio Open) and the claim that
**semantic tokens are not required for long-range coherence**; explain **rectified flow**
and **MM-DiT** (FluxMusic) as an objective+architecture variant; place **DiffRhythm**
(fast full-song DiT) and **ACE-Step** (LM-planner + DiT-renderer hybrid) on the map; and
*run a real latent-diffusion model* (Stable Audio Open / DiffRhythm) to generate and to
**denoise the clip's own latent**, inspecting it at every step.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture**, and where it sits: course 1 built the
  codec and stopped at the **fork**; course 2 walked the **discrete-token branch**
  (predict tokens with a language model); **this course walks the other branch** —
  audio generation = **denoise a continuous VAE latent** with a **Diffusion
  Transformer**. Read [`the-latent-canvas.md`](the-latent-canvas.md). The contrast with
  course 2 *is* the lesson: predict-symbols vs denoise-a-vector.
- **0.2** **Recap diffusion (from `ai-foundations` Phase 6).** Forward **noising** vs
  reverse **denoising**; the network predicts the **noise** `ε` (equivalently the
  **score** `∇ log p_t`); sampling = repeated denoising over `T` steps. Re-anchor on the
  through-line clip's **continuous VAE latent** from course 1 — *that* real-valued grid
  is what we denoise. (And the contrast with course 2: masked NAR unmasks **discrete
  tokens** by confidence; diffusion denoises a **continuous latent** — not the same.)
- **0.3** **Tools.** `torch` + a pretrained latent-diffusion generator (tier-aware):
  `diffusers` and/or **Stable Audio Open** via `stable-audio-tools`. Confirm you can
  encode→VAE-latent→decode the clip round-trip before denoising anything.

## Phase 1 — Latent Diffusion for Audio
- **1.1** **Why not diffuse the waveform.** Raw audio is hundreds of thousands of
  dimensions per second; mel-spectrograms are smaller but still large. **Latent
  Diffusion** (Rombach 2022): compress to a **continuous VAE latent** first, diffuse
  *there*, decode back. 10–100× cheaper, and the VAE handles fine texture. Exactly
  course 1's continuous bottleneck, now put to work.
- **1.2** **AudioLDM (2023): the first audio LDM.** Pipeline = **mel-VAE latent** +
  **U-Net** denoiser + **CLAP** conditioning + **HiFi-GAN** vocoder. Trainable on a
  *single GPU*. Note the backbone here is a **U-Net** (the DiT comes in Phase 3).
- **1.3** **The CLAP trick.** **CLAP** is a joint audio–text embedding (course 2's MuLan
  cousin). Condition on the **audio** embedding at train time, substitute the **text**
  embedding at inference → train text-to-audio on **audio-only** data. Same
  paired-data bypass the learner met in course 2.
- **1.4** **Classifier-free guidance.** The one knob everyone turns: mix the
  conditional and unconditional predictions, `ε̂ = ε(∅) + w·[ε(c) − ε(∅)]`, with guidance
  scale `w` (~3–15) trading diversity for prompt adherence.
- **1.5** **Pin to the clip.** Encode the clip to its mel/VAE latent; conceptually run
  the forward noising on it and picture the reverse denoising bringing it back.

## Phase 2 — The Audio-LDM Family
- **2.1** **Tango (2023): the text encoder matters.** Swap CLAP → a **frozen,
  instruction-tuned Flan-T5**. Result: **63× less training data**, *better* benchmarks.
  The lesson that generalized across the field — the conditioning encoder, not raw data
  volume, often dominates. (Flan-T5 is *frozen*, not fine-tuned.)
- **2.2** **AudioLDM 2 (2023): the "language of audio."** A self-supervised **AudioMAE**
  feature (the **LOA**) is the universal target; a **GPT-2** bridges *any* condition
  (text, phonemes, image) into LOA, and a **latent-diffusion** model renders audio from
  it. **Any-to-audio.** *Misreading to flag:* the GPT-2 inside does **not** make it a
  codec-LM — the renderer is still continuous-latent diffusion (a hybrid; see Phase 7).
- **2.3** **Going long via cascading.** **Noise2Music (2023):** cascaded U-Nets, 30 s at
  24 kHz, with **LLM-pseudo-labeled** training data (MuLaMCap). **Moûsai (2023):** a
  **diffusion-autoencoder** latent (not a VAE), *minutes* of 48 kHz stereo, real-time on
  one GPU. Both reach length by stacking models — Phase 5 will reach it differently.
- **2.4** **Pin to the clip.** Pick a text tag for the clip ("solo piano, gentle, minor
  key") and reason which encoder (CLAP / Flan-T5) and which family member would steer a
  generation toward its character.

## Phase 3 — The DiT (keystone)
> Spend as long as it takes. This is *how* you denoise. Re-read [`the-latent-canvas.md`](the-latent-canvas.md).
- **3.1** **The U-Net, and why replace it.** Image and early-audio diffusion denoised
  with a convolutional **U-Net** (multi-resolution, cross-attention for text). It works,
  but its convolutional inductive bias doesn't scale as cleanly as a transformer.
- **3.2** **Peebles & Xie (2022): the Diffusion Transformer.** Throw away the U-Net;
  **patchify** the latent into a sequence of patch tokens, embed, and run **standard
  transformer blocks**. "Generate" is unchanged (denoise); only the backbone is now a
  transformer. *The patches are real-valued vectors — not codebook indices.*
- **3.3** **adaLN-Zero: how the timestep and condition enter.** Not cross-attention —
  **adaptive layer norm**: compute each LayerNorm's scale/shift from `(t, c)`, with the
  block's residual scale **zero-initialized** so training begins at the identity.
  Cheapest of the options Peebles & Xie tried, and the **best FID**. It became the
  default conditioning for every audio/video DiT.
- **3.4** **It scales like a transformer.** More **Gflops** — smaller patch (→ more
  tokens), deeper, or wider — **monotonically lowers FID**. The clean transformer
  scaling law, now driving diffusion. U-Net's convolutional bias turns out to be *not
  essential*.
- **3.5** **The two misreadings to kill.** *(i)* "**DiT is a diffusion-specific
  architecture**" — no, it's a **plain transformer + adaLN-Zero** timestep conditioning.
  *(ii)* "**'audio codec → DiT' uses discrete tokens**" — no, the DiT denoises a
  **continuous VAE latent**; *"diffusion wants a smooth latent."* This is course 1's
  fork on home turf — the field's most common confusion.
- **3.6** **Pin to the clip.** Patchify the clip's VAE latent on paper: choose a patch
  size, count the resulting patch tokens, and note that the DiT denoises *all* of them
  at once (contrast course 2's left-to-right token grid).

## Phase 4 — Stable Audio: Continuous VAE + Timing (still a U-Net)
- **4.1** **Stable Audio (Evans et al. 2024).** Latent diffusion over a
  **fully-convolutional continuous VAE** — *not* a discrete RVQ codec. **44.1 kHz
  stereo**, up to **~95 s**, a **907M-param U-Net** denoiser, CLAP + timing
  conditioning. The recipe that made high-quality, long, stereo generation practical.
- **4.2** **The timing-conditioning trick.** Two timing embeddings —
  **`seconds_start`** and **`seconds_total`** — tell the model *where in the piece* and
  *how long* it is, enabling **variable-length** generation and letting it place
  structure (intro / development / outro) inside a fixed training window.
- **4.3** **The misreading to kill: "Stable Audio is a DiT."** **v1 is a U-Net** (907M),
  in the lineage of Moûsai — it established the **continuous-VAE + timing** recipe but is
  **not yet a transformer**. The **DiT swap comes one paper later** (Phase 5). Getting
  this right is the home-turf test of the fork *and* the backbone.
- **4.4** **Pin to the clip.** Reason about (or, by tier, run) a short generation around
  the clip's ~2 s length using `seconds_total`; predict how the timing embeddings shape
  a longer continuation.

## Phase 5 — The DiT for Music: the U-Net → DiT Swap (keystone)
> Spend as long as it takes. This is *what* you denoise, scaled to full songs.
- **5.1** **Long-Form Latent Diffusion (Evans et al. 2024): the swap.** Replace Stable
  Audio's U-Net with a **DiT** in the same continuous VAE latent — a **21.5 Hz latent
  rate** (≈2000× compression from 44.1 kHz stereo) — and generate **full songs up to
  4m 45s** with coherent structure. This is **Stable Audio Open**'s backbone.
- **5.2** **The bold claim: full-context generation beats the semantic-token premise.**
  AudioLM (course 2) argued **semantic tokens** are *needed* for long-range coherence.
  Long-Form Latent Diffusion shows structure can **emerge from full-context generation**
  — denoise the *whole* multi-minute latent at once, no semantic-token stage. A genuine
  cross-branch dispute, not a footnote.
- **5.3** **Recite the fork, both branches.** Discrete tokens → **language model**
  (course 2: AR/masked, fills a grid cell-by-cell or by confidence) vs continuous VAE
  latent → **DiT** (course 3: denoise the whole canvas globally). *Same through-line
  clip, opposite machinery.* If the learner can say this cleanly, the curriculum landed.
- **5.4** **Pin to the clip.** Run **Stable Audio Open** (a real DiT) to generate a
  short piece in the clip's character, or **denoise the clip's own latent** (img2img-
  style) for a variation; **listen**, and inspect the latent at a few denoising steps.

## Phase 6 — Swapping the Objective: Flow Matching + MM-DiT (FluxMusic)
- **6.1** **Diffusion vs flow.** Classic diffusion predicts **noise/score**; **rectified
  flow** predicts a **straight-line velocity** from noise to data — *same DiT backbone,
  different target.* Read the self-contained
  [`rectified-flow-primer.md`](rectified-flow-primer.md); link to
  [`flow-matching/`](../flow-matching/) for the full derivation.
- **6.2** **FluxMusic (2024): the FLUX / SD3 recipe for music.** A text-to-music **MM-DiT**
  trained with **rectified flow** (not DDPM) in a **mel-VAE** latent, conditioned by
  **T5 + CLAP**. The image world's frontier recipe, ported to audio.
- **6.3** **MM-DiT: multimodal, two-stream.** Text and music tokens first get separate
  (**double-stream**) attention, then are concatenated into a **single joint stream** —
  vs vanilla DiT's single adaLN-Zero stream. The architectural step beyond Phase 3's DiT.
- **6.4** **Two misreadings to kill.** *(i)* "**flow matching is just diffusion**" —
  related but a **different objective**; the `flow-matching` course settles it. *(ii)*
  "**mel-VAE vs waveform-VAE is a paradigm change**" — both are **continuous VAE
  latents**; the **DiT doesn't care**. FluxMusic (mel-VAE) and Stable Audio
  (waveform-VAE) differ in *latent* and *objective*, not in *branch*.
- **6.5** **Pin to the clip.** Reason about (or run) a FluxMusic generation toward the
  clip's character; relate its straight-line velocity field to the two-moons quiver
  plots from `flow-matching`.

## Phase 7 — Full Songs & Hybrids: DiffRhythm, ACE-Step
- **7.1** **DiffRhythm (2025): fast full songs.** The **first end-to-end latent-diffusion
  DiT for full-length songs** — **4m 45s**, **vocals + accompaniment**, generated
  **non-autoregressively in ~10 s**. Reuses **Stable Audio's VAE** and adds a
  **sentence-level lyrics-alignment** mechanism for the ultra-sparse lyrics↔vocal
  problem. The VAE-latent DiT now owns territory that slow AR LM pipelines once held.
- **7.2** **Why diffusion isn't "1000 steps slow."** **DDIM** (~50 steps, deterministic),
  **ODE solvers** (DPM-Solver++, 10–20), and **distillation** (progressive; one-step EMD)
  collapse the step count. This is what makes the next system fast.
- **7.3** **ACE-Step (2026): the hybrid — LM planner + DiT renderer.** A **language model
  plans** the song (lyrics, metadata, captions, via chain-of-thought); a **DiT renders**
  the audio ("a specialized acoustic renderer, freed from semantic ambiguity").
  **Distilled to 4–8 steps** (~100× speedup), **~10 s/song**, **<4 GB VRAM**. The two
  branches of the fork, now *cooperating stages*.
- **7.4** **The misreading to kill.** "**ACE-Step's LM makes it a codec-LM**" — no. The
  **LM plans**; the **DiT (continuous-latent diffusion) renders**. Same shape as
  AudioLDM 2's GPT-2→LOA→LDM (Phase 2.2). A hybrid *uses* both branches; it doesn't
  collapse them.
- **7.5** **Pin to the clip.** Reason about an ACE-Step-style pipeline for the clip: what
  would the LM planner write, what would the DiT renderer denoise?

## Phase 8 — Putting It Together
- **8.1** **The map.** Place every system on two axes: **latent** (mel-VAE /
  waveform-VAE / diffusion-AE) × **backbone + objective** (U-Net-DDPM / DiT-DDPM /
  **MM-DiT-rectified-flow** / **hybrid LM+DiT**). Place AudioLDM, Tango, AudioLDM 2,
  Noise2Music, Moûsai, Stable Audio, Long-Form Latent Diffusion, FluxMusic, DiffRhythm,
  ACE-Step. Recite which latent each denoises and with what backbone.
- **8.2** **Capstone — denoise the clip with a real latent-diffusion model.** Tiered like
  room-acoustics' a/b/c, no GPU required:
  - **(a) CPU / pretrained inference (default).** `diffusers` or `stable-audio-tools`;
    load a small latent-diffusion model (or **Stable Audio Open**, slowly). **Generate**
    from a text prompt; **denoise the clip's own VAE latent** (img2img) for a variation;
    inspect the latent at a few sampler steps and **decode + listen**. Write a one-page
    "diffusion-DiT report." (CPU is slow — small models / few steps.)
  - **(b) Colab GPU.** Full-length generation; **A/B step counts** (DDIM 10 vs 50 — hear
    the quality/speed trade); exercise **timing conditioning**; run **DiffRhythm** for a
    full song; try **DITTO-style** melody/structure control if time allows.
  - **(c) Local GPU.** Additionally run **FluxMusic** (rectified flow / MM-DiT) and/or
    **ACE-Step** (LM-planner + DiT-renderer); prompt toward the clip's style; *hear* the
    objective swap (diffusion vs flow) and the hybrid pipeline.
- **8.3** **The curriculum, closed.** You can now read AudioLDM(2), Tango, the DiT,
  Stable Audio, Long-Form Latent Diffusion, FluxMusic, DiffRhythm, and ACE-Step — and you
  have walked **both branches of course 1's fork** on one solo-piano clip: *predicted* as
  tokens (course 2), *denoised* as a latent (course 3). Where next: `flow-matching/` for
  rectified-flow depth; the curated wikis for new papers; `ai-miracle-decade-plus/` for
  the wider survey.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. The
   recurring picture here is the **latent canvas** (`the-latent-canvas.md`): a continuous
   latent denoised out of noise, *globally*, by a transformer over patches. Contrast it
   constantly with course 2's token grid (predicted cell-by-cell).
3. **Pin it to the clip.** The clip's **continuous VAE latent** is the worked example.
   Denoise it, generate variations, and **listen**. The ear is this course's oracle; a
   decoded denoising beats a diagram.
4. **Tiny exercise** to verify: predict a behavior ("more guidance `w` — more diverse or
   more on-prompt?"; "fewer DDIM steps — faster or higher-quality?"), trace how a
   condition enters a DiT (adaLN-Zero, *not* cross-attention), or run a few lines of
   `diffusers` / `stable-audio-tools`. The exercise *is* the check.
5. **Common misreadings** when relevant — keep [`the-latent-canvas.md`](the-latent-canvas.md)'s
   list live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences ("a DiT is a plain transformer over latent
   patches with adaLN-Zero timestep conditioning; it denoises a *continuous* VAE latent").
2. Carry out the small task: trace how `(t, c)` enter a DiT, A/B step counts or guidance,
   denoise the clip's latent and listen, or place a system on the latent × backbone map —
   and explain it.
3. Spot a deliberately wrong claim ("Stable Audio v1 is a DiT" — no, a U-Net; "the DiT
   denoises codec tokens" — no, a continuous VAE latent; "flow matching is just
   diffusion" — related, different objective).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wikis this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wikis stay
canonical, the course stays pedagogical. Read / link these on JOS's machine:

- **`/w/music423-2023/diffusion/wiki/`** — the diffusion home wiki. Concept pages:
  `diffusion-fundamentals.md` (DDPM / score / SDE — three views of one model),
  `latent-diffusion-models.md` (the VAE + LDM paradigm), `audio-diffusion.md` (the
  audio pipeline), `distillation-fast-sampling.md` (DDIM, ODE solvers, distillation,
  DITTO). Source summaries: `ddpm-ho-2020`, `ddim-song-2020`, `score-sde-song-2020`,
  **`dit-peebles-2022`**, `audioldm-liu-2023`, `audioldm2-liu-2023`, `tango-ghosal-2023`,
  `noise2music-huang-2023`, `mousai-schneider-2023`, `multiband-diffusion-roman-2023`,
  `ditto-novack-2024`, `emd-one-step-2024`.
- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — the generation wiki (diffusion half).
  `overview.md` (Phase 5: the VAE→DiT standard), `concepts/generation-paradigms.md` (AR
  vs masked vs **diffusion** — the comparison table), `concepts/codec-based-generation.md`
  (the continuous-latent alternative + the semantic-token challenge). Source summaries:
  **`dit`**, **`stable-audio`**, **`diffusion-long-form-music`**, **`fluxmusic`**,
  **`diffrhythm`**, **`ace-step`**.
- **`/w/music423-2023/ai-audio-codecs/wiki/`** — course 1's wiki, for the **continuous
  VAE** recall the whole course rests on.
- Keep the course in sync if the wikis gain papers; the wikis are canonical, the course
  is the lesson plan over them.

### Source papers (the diffusion/DiT lineage this course tracks)
- **Sohl-Dickstein et al. (2015)** — *Deep Unsupervised Learning using Nonequilibrium
  Thermodynamics* (diffusion's origin). arXiv:1503.03585.
- **Ho et al. (2020)** — *DDPM (Denoising Diffusion Probabilistic Models)*. arXiv:2006.11239.
- **Song et al. (2020)** — *DDIM (Denoising Diffusion Implicit Models)*. arXiv:2010.02502.
- **Song et al. (2020)** — *Score-Based Generative Modeling through SDEs*. arXiv:2011.13456.
- **Rombach et al. (2022)** — *High-Resolution Image Synthesis with Latent Diffusion
  Models* (Stable Diffusion). arXiv:2112.10752.
- **Peebles & Xie (2022)** — *Scalable Diffusion Models with Transformers (DiT)*.
  arXiv:2212.09748.
- **Liu et al. (2023)** — *AudioLDM*. arXiv:2301.12503.
- **Liu et al. (2023)** — *AudioLDM 2 (Holistic / "language of audio")*. arXiv:2308.05734.
- **Ghosal et al. (2023)** — *Tango (Text-to-Audio with an instruction-tuned LLM)*.
  arXiv:2304.13731.
- **Huang et al. (2023)** — *Noise2Music*. arXiv:2302.03917.
- **Schneider et al. (2023)** — *Moûsai*. arXiv:2301.11757.
- **Evans et al. (2024)** — *Fast Timing-Conditioned Latent Audio Diffusion (Stable
  Audio)*. arXiv:2402.04825.
- **Evans et al. (2024)** — *Long-Form Music Generation with Latent Diffusion* (Stable
  Audio Open backbone). arXiv:2404.10301.
- **Fei et al. (2024)** — *FluxMusic (Text-to-Music with Rectified-Flow MM-DiT)*.
  arXiv:2409.00587.
- **Ning et al. (2025)** — *DiffRhythm (Full-Length Song Generation with Latent
  Diffusion)*. arXiv:2503.01183.
- **Gong et al. (2026)** — *ACE-Step (LM-planner + DiT-renderer)*. arXiv:2602.00744.
