# The Image as a Sequence — This Course's Keystone

`ai-sequence-models` asks *what a token can attend to*; the audio courses ask *how a
clip becomes tokens or a latent*. This course asks the vision version of both, and the
whole field turns out to be one question with two halves:

> **An image is a 2-D grid with no natural reading order. To push it through the same
> Transformer that reads text (and codec tokens) you must decide two things: *what is
> a cell?* (the **tokenizer**) and *in what order are cells produced?* (the
> **generation order**). Every vision and multimodal system in this course is one
> choice of tokenizer plus one choice of order.**

Read this in Phase 0.1, then return to it in **Phase 5** (ViT, the moment the grid
becomes a sequence), **Phase 6** (discrete tokenizers), **Phase 7** (generation order),
**Phase 10** (several tokenizers sharing one sequence), and **Phase 11.1** (where you
place every system on the map).

Every term in **bold** is earned somewhere in the syllabus; the phase is in brackets.
The worked example throughout is one **Fashion-MNIST** image: 28 × 28 grayscale, one of
10 clothing classes.

---

## The grid, and five things a cell can be

```
   one Fashion-MNIST image, 28 x 28              the same image, 7 x 7 cells
   ┌────────────────────────────┐                ┌──┬──┬──┬──┬──┬──┬──┐
   │                            │                │  │  │  │  │  │  │  │
   │        ▄▄██████▄▄          │   tokenizer    ├──┼──┼──┼──┼──┼──┼──┤
   │      ▄████████████▄        │  ──────────▶   │  │▒▒│██│██│██│▒▒│  │   each cell = ?
   │     ██████████████         │  (what is a    ├──┼──┼──┼──┼──┼──┼──┤
   │      ▀██████████▀          │     cell?)     │  │  │██│██│██│  │  │
   │         ...                │                └──┴──┴──┴──┴──┴──┴──┘
   └────────────────────────────┘                   49 cells, no reading order
```

| A cell is… | Its value | Who uses it | Earned in |
|---|---|---|---|
| a **pixel** | an intensity, 0..255 | PixelCNN, Image GPT | [7.1] |
| a **conv feature** | a real vector at a grid position, seeing a local receptive field | AlexNet, ResNet, U-Net | [1, 2] |
| a **patch embedding** | a real vector, a learned linear projection of a P × P patch | ViT, AST, CLIP's image tower | [5] |
| a **discrete code** | an integer index 0..K−1 into a learned codebook | VQ-VAE, VQGAN, DALL-E, Chameleon, VAR | [6] |
| a **continuous latent patch** | a real vector from a VAE latent | LDM, DiT, MAR, Transfusion, BAGEL | [3, 9, 10] |

The CNN is the baseline that **keeps the grid**: convolution is the 2-D-native operation
(a learned 2-D FIR filter bank, translation-equivariant), so a CNN never needs a reading
order. **ViT** is the moment the grid is **flattened into a sequence** [5.1], trading the
convolutional prior for the Transformer's generality. Everything after that is about
which kind of cell goes into the sequence and which order comes out.

Three different things get called "image tokens." Keep them apart [5.2, 6.1, 9.4]:
a ViT patch embedding is continuous and *input-only*; a VQ code is a *discrete symbol*
you can predict with cross-entropy; a latent patch is continuous and is *denoised*, not
predicted.

## Seven generation orders

| Order | How cells are produced | Steps for our 7 × 7 grid | Who | Earned in |
|---|---|---|---|---|
| **none** (recognize) | no generation; encode and classify/embed | — | AlexNet, ResNet, ViT, CLIP | [1, 5, 8] |
| **one shot** | one forward pass from a noise vector `z` | 1 | VAE decoder, GAN, StyleGAN | [3, 4] |
| **raster AR** | one discrete code at a time, left→right, top→bottom | 49 | PixelCNN, VQGAN-Transformer, DALL-E, LlamaGen, Chameleon | [7.1–7.2] |
| **masked / confidence** | start all-masked; predict all, keep the most confident, re-mask, repeat | ~8 | MaskGIT, Muse, MAR | [7.3] |
| **next-scale** | a whole resolution at a time, coarse→fine; parallel within a scale | 5 (scales 1,2,3,5,7) | VAR | [7.4–7.5] |
| **denoise all at once** | start from noise over the whole canvas; refine every cell each step | ~20–50 | LDM, Imagen, DALL-E 2's decoder, DiT | [9] |
| **mixed, in one sequence** | AR for the text positions, denoising for the image positions | text: per token; image: ~20–50 | Transfusion, BAGEL | [10.3] |

The AR factorization `p(x) = Π p(xᵢ | x_<i)` is **exact for any ordering** of the cells
(the chain rule of probability is a theorem); *which* ordering trains and samples best is
an **empirical engineering choice**. That is why "autoregressive" does not mean "raster"
[7.4]: VAR is autoregressive over **scales**, MaskGIT is close to autoregressive over
**confidence**, RAR trains on **random permutations**.

## The map (filled in by Phase 11.1)

```
                    one shot   raster AR   masked   next-scale   denoise all   mixed
  pixel                        PixelCNN                          Imagen
                               Image GPT                         (pixel cascade)
  conv feature      VAE, GAN
                    StyleGAN
  discrete code                DALL-E      MaskGIT  VAR          (discrete
                               VQGAN-T     Muse                   diffusion)
                               LlamaGen
                               Chameleon
  continuous                               MAR                   LDM, DiT      Transfusion
  latent patch                             (Fluid)                             BAGEL
  patch embedding   (encoders only: ViT, AST, CLIP — they read the sequence, they don't generate it)
```

## The bridge to audio (both tracks lean on this)

| Vision object | Audio counterpart | Earned in |
|---|---|---|
| an image | a **mel spectrogram** is an image too: 2-D, patchable (AST = ViT on mel); but its two axes mean different things and the magnitude has thrown away phase | [5.5] |
| ViT patch tokens (49 per Fashion-MNIST image) | AST patch tokens (104 for the through-line clip at 128 mel × 221 frames, 16 × 16 patches) | [5.5] |
| a VQ code grid `[7, 7]` | an RVQ codec grid `[N_q, T]` (`audio-codec-lms`' token grid) — same VQ-VAE ancestor, which did images *and* audio in one paper | [6.4] |
| VAR's **multi-scale residual** quantizer (residual across *scales*) | **RVQ** (residual across codebook *depth*) — both are multistage VQ; VAR's is a quantized Laplacian pyramid | [7.4] |
| raster AR over image codes | codec-LM AR over audio codes (MusicGen) | [7.7] |
| MaskGIT confidence-unmasking | VampNet / MAGNeT (MaskGIT is their stated ancestor) | [7.3] |
| CLIP (image ↔ text) | CLAP / MuLan (audio ↔ text), and the same "train on one tower, swap in the other at inference" trick | [8.5] |
| U-Net denoiser in LDM | AudioLDM and Stable Audio v1's U-Nets | [2.4, 9.3] |
| DiT over latent patches | audio DiT over a continuous audio-VAE latent (Stable Audio Open, `audio-diffusion-dit`' latent canvas) | [9.4] |
| GAN discriminator as a loss | the adversarial losses in VQGAN, HiFi-GAN, EnCodec, DAC | [4.6] |
| StyleGAN3's alias-free layers | the anti-aliased activations in BigVGAN-style vocoders | [4.5] |

---

## The misreadings this course exists to kill

The tutor flags each on the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "ResNets fixed vanishing gradients." | They fixed the **degradation problem**: deeper *plain* nets had *higher training error* even with BatchNorm, where gradients do not vanish. The clean "+1" gradient path is the follow-up paper's analysis. Both matter; the stated motivation is optimization difficulty. | 1.3–1.4 |
| "U-Net skips are ResNet skips." | ResNet **adds** within a block at one resolution (an optimization aid). U-Net **concatenates** encoder features into the decoder at the matching resolution (restores spatial detail the bottleneck lost). Different jobs. | 2.2 |
| "VAE blurriness is an implementation bug." | It follows from the Gaussian (MSE) decoder: the best guess under uncertainty is the **mean of the plausible images**, and a mean of sharp images is blurry. | 3.3 |
| "GANs are dead." | As standalone image generators they were largely overtaken by diffusion; as a **loss** they are everywhere (VQGAN, HiFi-GAN, EnCodec, adversarial distillation). | 4.6 |
| "ViT has no convolution." | Patch embedding **is** a strided convolution (kernel = stride = P). What ViT drops is the *further* locality and weight-sharing prior of a conv stack. | 5.1 |
| "Transformers beat CNNs on images." | An **empirical, data-dependent** result: ViT trailed comparable ResNets when trained on ImageNet-1k alone and won with very large pretraining; modernized CNNs (ConvNeXt) match it. No theorem picks a winner. | 5.3 |
| "Image tokens = patches." | Three different objects: continuous patch embeddings (ViT input), discrete codes (VQ), continuous latent patches (DiT/Transfusion). Only the second can be predicted with cross-entropy. | 5.2, 6.1 |
| "VQ codes are like words." | They are indices of local patch prototypes, with no built-in meaning; image tokens are far more random than text tokens (ELM's finding). | 6.2 |
| "Autoregressive means raster order." | AR is a factorization, exact for any order. Raster, random (RAR), confidence (MaskGIT), and scale (VAR) are all choices. | 7.4 |
| "Next-scale prediction is diffusion." | Both go coarse-to-fine, but VAR predicts **discrete codes with cross-entropy**, no noise anywhere. Same for MaskGIT: confidence-unmasking of discrete tokens, not denoising. | 7.4–7.5 |
| "CLIP generates images." | CLIP is an aligned **pair of encoders**. Generators use it to condition (unCLIP, SD), to rerank (DALL-E), or to score (CLIP-score). | 8.1 |
| "DALL-E is a diffusion model." | **DALL-E (2021)** is a discrete AR Transformer over dVAE codes. **DALL-E 2 (2022)** is diffusion (unCLIP). Same name, opposite orders. | 9.1–9.2 |
| "A spectrogram is just an image." | It is an image whose axes are **time and frequency**, not two interchangeable space axes: translation in time is natural, in frequency only approximately (and only on a log axis); and the magnitude spectrogram has discarded **phase**, so getting audio back needs a vocoder or phase retrieval. | 5.5 |
| "Unified multimodal = one tokenizer for everything." | Transfusion and BAGEL use **different representations and different losses** per modality inside **one sequence and one backbone**. "Unified" names the backbone, not the tokenizer. | 10.1, 10.3 |
| "MoT is MoE." | MoE routes tokens with a **learned** gate (plus a balancing loss); MoT routes **deterministically by modality** (or role) and keeps attention global. They compose. | 10.4 |
| "BAGEL proved that world models emerge from scale." | A striking **claim from one lab**, measured partly on its own benchmark. Evidence is partial; replication is the open question. | 10.5 |

---

## How the course earns the keystone

| Piece | Earned in |
|---|---|
| the grid kept: convolution as a learned 2-D filter bank; depth made trainable by residuals | **Phase 1** |
| multiresolution: encoder–decoder, U-Net skips, up/downsampling and aliasing | **Phase 2** |
| the continuous latent cell and one-shot sampling (VAE) | **Phase 3** |
| one-shot sampling with a learned loss; style at each scale (GAN, StyleGAN) | **Phase 4** |
| the grid becomes a sequence (ViT; the spectrogram as an image) | **Phase 5** (keystone) |
| the discrete cell (VQ-VAE, VQGAN; the shared ancestor of audio codecs) | **Phase 6** (keystone) |
| the order (raster, masked, next-scale, continuous AR) | **Phase 7** (keystone) |
| two sequences aligned (CLIP) | **Phase 8** |
| text sequence + image sequence (DALL-E) and the diffusion turn (LDM, DiT) | **Phase 9** |
| several tokenizers, one sequence, one backbone (Chameleon → BAGEL) | **Phase 10** |
| the full tokenizer × order map | **Phase 11.1** |
