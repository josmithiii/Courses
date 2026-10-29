# AI Vision & Multimodal — How an Image Becomes a Sequence

**Learner profile:** Arrives from `ai-foundations/` (or equivalent) with MLPs, backprop,
PyTorch, a first CNN on MNIST, attention and the Transformer block, next-token LLMs,
and *intuition-level* VAEs, GANs and diffusion. This course **picks up where
`ai-foundations` Phases 3 and 6 stop** and goes into mechanism: the vision branches of
the same Transformer backbone that LLMs and audio codec-LMs use. It is an
**enrichment** course for both AI research tracks of Music 423: Track B (*LLMs &
Sequence Models*), where it is the vision/multimodal branch of the backbone, and Track
A (*AI Music & Audio*), where roughly half of it (CNN/U-Net backbones, VAEs, GANs, the
ViT patch, latent diffusion and the DiT) is the image-world background of
`audio-diffusion-dit`. DSP people are especially welcome: convolution, filter banks,
decimation and aliasing, multiresolution pyramids and vector quantization all appear,
and the tutor uses them. ~1 hour per day, one concept at a time, every concept checked
with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisites — plunge-in friendly, no hard gates.** Strongly recommended:
[`ai-foundations/`](../ai-foundations/) Phases 2–4 (PyTorch, CNNs, Transformers) and
Phase 6 (generative intuition). A learner who skips it can still start here; Phase 0.3
is a one-page recall-primer, and each phase that leans on `ai-foundations` says which
topic to go back to. [`ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) covers
AlexNet, the VAE, GANs, U-Net, ResNet, ViT, DALL-E, CLIP, LDM and Imagen as a *reading
tour* (its Phases 1, 2 and 7); this course goes deeper into how each one works and has
the learner build a small version. Run them side by side if you like.

**The keystone — read [`the-image-as-sequence.md`](the-image-as-sequence.md) in Phase
0.1.** An image is a 2-D grid with no natural reading order. To push it through the
same Transformer that reads text and codec tokens you must choose **what a cell is**
(the **tokenizer**: pixel, conv feature, patch embedding, discrete code, continuous
latent patch) and **in what order cells are produced** (the **generation order**: none,
one shot, raster AR, masked, next-scale, denoise-all-at-once, or mixed in one
sequence). Every system in the course is one tokenizer plus one order. We spend as long
as it takes on **Phases 5–7**, the three keystone phases.

**The worked example — Fashion-MNIST.** One small, standard, CPU-friendly dataset is
carried through every phase: **Fashion-MNIST** (Xiao, Rasul & Vollgraf 2017), 60,000
training and 10,000 test images, 28 × 28 grayscale, 10 clothing classes (T-shirt/top,
Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot), downloaded by
`torchvision`. Why it and not MNIST: it is a drop-in replacement with the same shape, so
every `ai-foundations` MNIST habit carries over; it is **hard enough that architectures
separate** (MNIST is saturated near 99%, so a ResNet and a plain CNN look the same; on
Fashion-MNIST the gaps show, and the Shirt / T-shirt / Pullover / Coat confusions are
visible and interesting); and its labels are **words**, which makes the CLIP-style
alignment in Phase 8 natural ("a photo of a sneaker"). Why not CIFAR-10: three color
channels at 32 × 32 make the GAN, VQ and AR phases too slow for a CPU hour. The same
28 × 28 image is classified (CNN, ResNet, ViT), autoencoded (AE, VAE), generated (GAN),
denoised (U-Net), patchified (ViT: 49 patches of 4 × 4), tokenized (VQ: a 7 × 7 grid of
codes), generated autoregressively (raster: 49 steps; next-scale: 5 steps), aligned with
text (CLIP), and generated from text (a mini-DALL-E). **Fail fast:** if the download
fails, the tutor says so and stops; it never substitutes MNIST or another dataset
silently.

**The audio bridge — the through-line clip as an image.** Track A's shared ~2.2 s
solo-piano clip (`../curricula/assets/ai-music-audio/through-line.wav`, mono 24 kHz)
appears as a second worked example wherever the vision idea has an audio twin: its mel
spectrogram (128 mel bands × 221 frames at a 10 ms hop) *is* an image, patchified as AST
does (Phase 5.5), tokenized the way a codec does (Phase 6.4), and generated the way a
codec-LM or an audio DiT does (Phases 7.7, 9.4). If the file is missing, the tutor says
so and skips the bridge exercise; it never substitutes another clip.

**End state:** by the last lesson the learner can: read a convolution as a learned 2-D
filter bank and a strided convolution as decimation (with the aliasing that implies);
explain AlexNet's recipe and the **degradation problem** ResNet solved, and why the
residual stream is now in every network; explain the U-Net as an analysis/synthesis
pyramid with skip connections, and why it became the diffusion backbone; derive the
VAE's ELBO and reparameterization trick and say why VAE samples blur; explain the GAN
game, mode collapse, FID, and StyleGAN's mapping network and per-scale styles (and point
to `disentanglement/` for what "disentangled" really costs); **patchify** an image (and
a spectrogram) for a ViT and say what the Transformer gives up and gains relative to a
CNN; train a **VQ** tokenizer and explain the straight-through estimator, commitment
loss and codebook collapse; generate the same 7 × 7 code grid in **raster**, **masked**
and **next-scale** order and explain why VAR's multi-scale residual quantizer is a
quantized Laplacian pyramid; train a tiny **CLIP** and do zero-shot classification with
prompts; explain DALL-E (AR over dVAE codes), DALL-E 2 / Imagen / LDM (diffusion), and
the DiT as a ViT over latent patches; explain the three designs of unified multimodal
models (quantized AR, external diffuser, integrated Transformer), Transfusion's two
losses and attention mask, MoT vs MoE, and judge the world-model claims honestly; place
every system on the **tokenizer × order** map; and follow the living frontier (Phase 12)
as it moves.

**Two short routes, if a learner wants one** (both optional, neither a gate):
- **Track A route** (background for `audio-diffusion-dit`): 0 → 1.4–1.6 → 2 → 3 → 4.1,
  4.6 → 5.1–5.5 → 9.3–9.5 → 11.1. About 10–12 sessions.
- **Track B route** (the sequence-model branch): 0 → 1.1, 1.4 → 5 → 6 → 7 → 8 → 9.1 →
  10 → 11.1. About 14–16 sessions.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture.** An image is a grid; a Transformer reads a
  sequence. Read [`the-image-as-sequence.md`](the-image-as-sequence.md): the five kinds of
  cell, the seven generation orders, the empty map we fill in by Phase 11, and the audio
  bridge table. Where this sits: the vision branches of the same backbone the LLM track
  studies, and the image-world ancestors of the audio track's codecs, codec-LMs and DiTs.
- **0.2** **Tools and the worked example.** `torch`, `torchvision`, `matplotlib` (and,
  for the audio bridge, `torchaudio` or `librosa`). Download Fashion-MNIST with
  `torchvision.datasets.FashionMNIST(root=<data dir>, download=True)`. **If the download
  fails, stop and report the real error.** Check the canonical numbers: 60,000 / 10,000
  images, shape `[1, 28, 28]`, 10 classes. Plot one image of each class, and name the
  hard pairs by eye (Shirt vs T-shirt vs Pullover vs Coat).
- **0.3** **Recall-primer (one page; from `ai-foundations` 2.8, 3.1–3.5, 4.3–4.6, 6.1–6.3).**
  A tensor `[B, C, H, W]`; `nn.Conv2d`; a training loop; cross-entropy; self-attention
  `softmax(QKᵀ/√d)V`; the Transformer block; "diffusion = learn to undo noise." If any of
  these is shaky, note which `ai-foundations` topic to revisit, and keep going.

## Phase 1 — CNN Backbones: AlexNet → ResNet
- **1.1** **Convolution through DSP eyes.** A conv layer is a **bank of learned 2-D FIR
  filters**, `C_in → C_out`, each output channel summing `C_in` filtered maps. Stride 2 is
  **decimation by 2 without an anti-aliasing filter**; max-pooling is a crude nonlinear
  lowpass-and-decimate. Receptive fields grow linearly through stride-1 layers and
  geometrically once you decimate, like an octave-band analysis. Exercise: compute the output shape and receptive field of a
  3-layer stack on a 28 × 28 input; then shift a Fashion-MNIST image by one pixel and
  watch a stride-2 network's output change (Zhang 2019's "shift-invariance" observation,
  by hand).
- **1.2** **AlexNet (2012): the recipe.** Five conv + three fully connected layers,
  ~60M parameters, trained on two GTX 580 GPUs. What survived: **ReLU**, **dropout**,
  **data augmentation**, **GPU training**, and end-to-end learning on a big benchmark
  (ILSVRC-2012 top-5 test error 15.3% vs 26.2% for the runner-up). What did not:
  local response normalization and the two-GPU split. History and verdict:
  `ai-miracle-decade-plus` 1.2 and the wiki's AlexNet note.
- **1.3** **The degradation problem.** Stack more plain conv layers and *training* error
  goes **up** (ResNet's Fig. 1: a 56-layer plain net trains worse than a 20-layer one on
  CIFAR-10). Not overfitting (training error, not test), and not simply vanishing
  gradients (BatchNorm keeps signals alive): an **optimization** difficulty. A deeper net
  could copy the shallow one and set the extra layers to identity, but SGD does not find
  that solution.
- **1.4** **The residual block (He et al. 2015).** `y = x + F(x)`: learn the *residual*
  `F`, so identity is the default (zero `F` passes the signal through, like a dry/wet mix
  starting fully dry). Projection shortcuts (1 × 1 conv) when shapes change; bottleneck
  blocks (1 × 1 → 3 × 3 → 1 × 1) for depth. **Pre-activation** (He et al. 2016): BN-ReLU
  before the conv keeps the skip path a pure identity, so the gradient from layer `L` to
  layer `l` contains an additive **1**, and 1001-layer nets train. Kill the misreading
  "ResNets fixed vanishing gradients" (see the keystone list).
- **1.5** **Pin to Fashion-MNIST.** Train a small plain CNN and a small ResNet of equal
  depth (widths 16/32/64, a 10k-image subset, an epoch or two on CPU). Compare **training
  loss** curves, then test accuracy. Ballpark only (your numbers will differ): an MLP
  reaches ~88–89%, a small CNN ~91–92%, a small ResNet ~92–94%. Make the confusion matrix
  and find the Shirt row. If the degradation gap does not show in so short a run, say why
  (BatchNorm and short training can mask it) — that is itself the lesson in 1.3. Keep
  this ResNet: it becomes the feature extractor for the FID-like score in Phase 4.3.
- **1.6** **The residual stream is everywhere.** Every Transformer sublayer is
  `x + Sublayer(x)`; U-Nets, diffusion backbones, codecs and WaveNet are built of
  residual blocks. One idea, used across all three tracks.

## Phase 2 — Encoder–Decoders and the U-Net
- **2.1** **The hourglass.** An encoder downsamples (28 → 14 → 7) while widening
  channels; a decoder upsamples back. The bottleneck holds *context* (what is in the
  image), and has thrown away *detail* (exactly where the edges are). This is an
  analysis/synthesis **pyramid**.
- **2.2** **U-Net (Ronneberger, Fischer & Brox 2015).** Add **skip connections that
  concatenate** each encoder level into the decoder level of matching resolution. The
  coarse path supplies context, the skips supply detail, like recombining subbands in a
  Laplacian pyramid (Burt & Adelson 1983) or a filter-bank synthesis stage. Built for
  biomedical segmentation from very few images. Contrast with ResNet's *additive*,
  same-resolution skips.
- **2.3** **Upsampling and its artifacts.** A transposed convolution is **zero-stuffing
  followed by a learned interpolation filter**. When the kernel size is not divisible by
  the stride, the kernel's polyphase components have unequal gains, so even a constant
  input comes out with a periodic pattern: **checkerboard artifacts**, the image-domain
  version of an interpolator that fails to reject the spectral images of zero-stuffing
  (Odena, Dumoulin & Olah 2016, Distill). Learned kernels can drift into it even when the
  sizes divide. Fix: resize (nearest/bilinear) then convolve. Phase 4.5
  returns to aliasing at the scale of a whole generator.
- **2.4** **Pin to Fashion-MNIST: a tiny U-Net denoiser.** Add Gaussian noise (σ = 0.5)
  to images and train a two-level U-Net to remove it; then ablate the skips and look at
  what goes missing (edges, the bag's handle, the sandal's straps). This is the network
  that **diffusion** reuses: Phase 9.3 and `audio-diffusion-dit` Phase 1.2 (AudioLDM) and
  Phase 4 (Stable Audio v1, a U-Net) take it from here.

## Phase 3 — The VAE: a Continuous Latent Cell
- **3.1** **Autoencoders.** Train a plain autoencoder with a **2-D bottleneck** on
  Fashion-MNIST and scatter the codes colored by class. Clusters appear without labels;
  footwear lands near footwear. But sample a random point between clusters and decode it:
  garbage. A plain AE has no notion of where valid codes live.
- **3.2** **The VAE (Kingma & Welling 2013).** The encoder outputs a **distribution**
  `q(z|x) = N(μ(x), diag σ²(x))`; the decoder models `p(x|z)`; the prior is `p(z) =
  N(0, I)`. Maximize the **ELBO** = `E_q[log p(x|z)] − KL(q(z|x) ‖ p(z))`
  (reconstruction minus a pull toward the prior). The **reparameterization trick**
  `z = μ + σ ⊙ ε`, `ε ~ N(0, I)`, moves the randomness out of the path so gradients flow.
  The ELBO is a **theorem** (a lower bound on `log p(x)` by Jensen's inequality).
- **3.3** **Sampling, interpolation, and blur.** Sample `z ~ N(0, I)`, decode; walk a
  straight line between a sneaker and an ankle boot. Then ask why samples are **blurry**:
  a Gaussian decoder means MSE, and the MSE-optimal output under uncertainty is the
  *mean* of the plausible images. This is not a bug; it motivates the GAN (Phase 4) and
  the adversarial/perceptual losses in VQGAN (Phase 6.3).
- **3.4** **What the latent encodes, and the disentanglement question.** Traverse one
  latent axis at a time. Do axes line up with "sleeve length" or "heel height"? Mostly
  not, and **why not** is a whole course: [`disentanglement/`](../disentanglement/)
  (β-VAE → total correlation → Locatello's impossibility result). Here we only name the
  question; Phase 4.4 shows StyleGAN's answer from the GAN side.
- **3.5** **The VAE as a continuous tokenizer.** Keep the encoder, throw away the prior
  sampling, and the VAE becomes a **compressor**: its latent is the canvas that latent
  diffusion denoises (Phase 9.3). Same role as the continuous branch of `audio-codecs`'
  fork and the "latent canvas" of `audio-diffusion-dit`. On the keystone map: a
  continuous-latent cell.

## Phase 4 — GANs: a Learned Loss
- **4.1** **The game (Goodfellow et al. 2014).** A generator `G(z)` and a discriminator
  `D(x)`; `min_G max_D E[log D(x)] + E[log(1 − D(G(z)))]`. **Theorem:** for the optimal
  `D`, the generator's objective is `−log 4 + 2·JSD(p_data ‖ p_G)`, minimized when
  `p_G = p_data`; this holds in function space with unlimited capacity. **Practice:** the
  saturating loss stalls early, so `G` maximizes `log D(G(z))` instead (the paper's own
  heuristic). The discriminator is a **loss function that is learned**.
- **4.2** **DCGAN on Fashion-MNIST.** Strided convs, BatchNorm, no fully connected
  layers, LeakyReLU in `D` (Radford, Metz & Chintala 2015). Train for a few CPU minutes;
  watch samples sharpen past the VAE's, then watch for **mode collapse** (every sample a
  sneaker) and oscillation. Sharp but unstable: the GAN trade-off in one run.
- **4.3** **Measuring a generator.** **FID** (Heusel et al. 2017): fit a Gaussian to deep
  features of real and of generated images and take the Fréchet distance,
  `‖μ_r − μ_g‖² + Tr(Σ_r + Σ_g − 2(Σ_r Σ_g)^{1/2})`. Compute a **Fashion-FID** using your
  Phase 1.5 ResNet's penultimate features in place of Inception. Honest caveat: it is
  self-consistent only, not comparable to published FIDs, and FID itself is a convention,
  not a theorem about perceptual quality.
- **4.4** **StyleGAN (Karras, Laine & Aila 2018): style at each scale.** A **mapping
  network** (an 8-layer MLP) sends `z` to an intermediate `w`; **AdaIN** injects `w` as a
  per-layer style; per-layer **noise** supplies stochastic detail; the synthesis network
  starts from a learned constant. Style mixing shows **coarse** (pose, shape), **middle**
  and **fine** (color, texture) styles live at different resolutions: multiresolution
  again. `W` is measurably more disentangled than `Z` (perceptual path length, linear
  separability). For what "disentangled" costs and why it cannot be had for free, see
  [`disentanglement/`](../disentanglement/) (InfoGAN is its Phase 2); don't duplicate it
  here.
- **4.5** **Alias-free generation (StyleGAN3, Karras et al. 2021) — a DSP paper in
  disguise.** "Texture sticking" (details glued to pixel coordinates while the object
  moves) is **aliasing**. The fix treats feature maps as samples of **bandlimited
  continuous signals**: proper lowpass filters at every up/downsampling, and each
  nonlinearity applied at a temporarily **higher sample rate** then lowpassed and
  decimated, exactly as one oversamples around a nonlinearity in virtual-analog audio.
  The same concern shows up in anti-aliased activations in neural vocoders (BigVGAN).
- **4.6** **The GAN's afterlife.** Diffusion largely took over standalone image
  generation, but the adversarial **loss** survived everywhere: VQGAN's patch
  discriminator (Phase 6.3), HiFi-GAN and MelGAN vocoders, EnCodec's and DAC's
  multi-scale STFT discriminators, adversarial distillation of diffusion models. Kill
  "GANs are dead."

## Phase 5 — The Grid Becomes a Sequence: ViT (keystone)
> Spend as long as it takes. Re-read [`the-image-as-sequence.md`](the-image-as-sequence.md).
- **5.1** **Patchify (Dosovitskiy et al. 2020, "An Image is Worth 16x16 Words").** Cut
  the image into non-overlapping `P × P` patches, flatten each, project linearly to
  dimension `D`. That projection **is** `Conv2d(C, D, kernel_size=P, stride=P)`, a
  critically sampled block transform with a learned basis (JPEG's 8 × 8 DCT is the fixed
  analogue). Token count `N = (H/P)(W/P)`. Fashion-MNIST with `P = 4`: **49 tokens of
  dimension 16**; with `P = 7`: 16 tokens of dimension 49. ViT-B/16 at 224 × 224: 196
  patches (+1 `[CLS]` = 197 tokens).
- **5.2** **The rest of ViT.** Prepend a learnable `[CLS]` token, add learnable position
  embeddings, run a standard Transformer **encoder** (bidirectional; nothing is
  generated), classify from `[CLS]`. Note what kind of "token" this is: a **continuous
  patch embedding**, input-only. Not a codebook index (Phase 6), not a denoised latent
  patch (Phase 9.4). Attention cost grows as `N²`: 49² = 2,401 entries per head per
  layer here, versus 784² = 614,656 if every pixel were a token.
- **5.3** **Inductive bias vs data.** A CNN *assumes* locality and translation
  equivariance; a ViT must *learn* them. Empirically, ViT trailed comparable ResNets when
  trained on ImageNet-1k alone and overtook them with JFT-300M-scale pretraining; DeiT
  (Touvron et al. 2020) closed the small-data gap with strong augmentation and
  distillation; ConvNeXt (Liu et al. 2022) showed a modernized CNN matches. All empirical
  and data-dependent. No theorem crowns either.
- **5.4** **Pin to Fashion-MNIST: a tiny ViT.** `P = 4`, `D = 64`, 4 layers, 4 heads (a
  few hundred thousand parameters). Train for the same CPU budget as the Phase 1.5 CNN and
  ResNet. Expect it to land at or a little below the CNN at this scale (ballpark ~88–91%).
  That gap **is** 5.3, measured on your own machine. Plot one attention map from `[CLS]`.
- **5.5** **The spectrogram is an image (the audio bridge).** Load the through-line clip
  (fail fast if missing), compute a **128-band mel spectrogram at a 10 ms hop** (hop 240
  at 24 kHz): **221 frames**. Non-overlapping 16 × 16 patches give 8 × 13 = **104 patch
  tokens**; AST's overlapping patches (stride 10) give 12 × 21 = **252**. AST (Gong,
  Chung & Glass 2021) starts from ImageNet-pretrained ViT weights and was state of the
  art on AudioSet. Then kill "a spectrogram is just an image": its axes are time and
  frequency, so translation is natural in time and only roughly so in (log-)frequency,
  and the magnitude has discarded phase (getting audio back needs a vocoder or phase
  retrieval; JOS's *SASP* covers the latter).
- **5.6** *(Optional.)* **Masking patches to learn without labels.** MAE (He et al.
  2021) hides 75% of the patches and reconstructs them; the encoder becomes a strong
  backbone. AudioMAE (Huang et al. 2022) does the same on spectrogram patches, and the
  idea runs through `audio-ssl-representations/`. One topic, pointer only.

## Phase 6 — The Discrete Cell: VQ-VAE → VQGAN (keystone)
> Spend as long as it takes. This is the image half of every codec in Track A.
- **6.1** **Vector quantization.** Replace each encoder output vector `z_e` by its
  nearest **codebook** entry `e_k`, emit the index `k`. This is classical VQ (Gray 1984;
  the codebook as a learned k-means/LBG design), now trained end-to-end. The argmin has
  no gradient, so the **straight-through estimator** copies the decoder's gradient back
  to `z_e` (Bengio, Léonard & Courville 2013).
- **6.2** **VQ-VAE (van den Oord, Vinyals & Kavukcuoglu 2017).** Loss = reconstruction +
  `‖sg[z_e] − e‖²` (move codes toward encoder outputs) + `β‖z_e − sg[e]‖²` (the
  **commitment** loss, β = 0.25 in the paper), with `sg` = stop-gradient; EMA codebook
  updates as an alternative. **Pin to Fashion-MNIST:** two stride-2 convs, 28 → 14 → 7,
  so each image becomes a **7 × 7 grid of 49 codes**; with `K = 128` codes that is
  49 × 7 = 343 bits versus 784 × 8 = 6,272 bits of raw pixels, about **18×**
  compression. Plot the **codebook usage** histogram; meet **codebook collapse** (most
  codes never chosen) and the fixes (k-means init, dead-code restarts, lower-dimensional
  codes). Decode a grid, then edit one code by hand and decode again.
- **6.3** **VQGAN (Esser, Rombach & Ommer 2021, "Taming Transformers").** Pixel MSE
  makes codes reconstruct blurry (Phase 3.3), so add a **perceptual** loss (LPIPS) and a
  **patch-based adversarial** loss (Phase 4.6). Codes become sharp at much higher
  compression (e.g. a 256 × 256 image → 16 × 16 = 256 codes), which is what makes
  Transformer priors over them practical. VQ-VAE-2 (Razavi et al. 2019) had earlier used
  a two-level, coarse/fine code hierarchy: multiresolution again.
- **6.4** **The shared ancestor of audio codecs (the bridge).** The VQ-VAE paper tokenized
  **images and speech** in one paper; its audio branch is the root of SoundStream,
  EnCodec and DAC. One VQ stage gives a `[7, 7]` grid here; **residual** VQ (multistage
  VQ) gives the codec's `[N_q, T]` grid in `audio-codecs`. Optionally train the same small
  VQ on 16 × 16 patches of the clip's mel spectrogram (a "spectrogram VQGAN," as in the
  Diffsound line of text-to-sound work) and compare its code grid with a codec's: 165
  frames at 75 Hz for 2.2 s of audio.
- **6.5** **Discrete or continuous? The fork, in vision.** A discrete code can be
  predicted with cross-entropy by any LM; a continuous latent keeps more information but
  needs a different generator (diffusion, or a diffusion head). This is `audio-codecs`'
  fork exactly, and Phases 7.6, 9 and 10 are the vision field choosing sides. Preview the
  simpler quantizers the frontier uses: **FSQ** (Mentzer et al. 2023: round each
  dimension to a few levels; implicit codebook, no collapse) and lookup-free / binary
  codes (MAGVIT-v2, ELM's BAE).

## Phase 7 — The Order: Raster, Masked, Next-Scale (keystone)
> Spend as long as it takes. Same 7 × 7 code grid, four ways to produce it.
- **7.1** **The AR factorization on a grid.** `p(x) = Π p(xᵢ | x_<i)` is exact for
  **any** ordering of the 49 cells; choosing one is engineering. Historical root: PixelCNN
  (van den Oord et al. 2016), raster AR over **pixels**, with masked convolutions. Too
  slow and too local; moving to a code grid (Phase 6) cuts 784 steps to 49.
- **7.2** **Raster AR over codes.** VQGAN's Transformer, DALL-E (Phase 9.1), Parti and
  LlamaGen (Sun et al. 2024: a plain Llama over VQ codes, FID ≈ 2.2 on ImageNet 256)
  all read the grid left→right, top→bottom. **Pin:** train a tiny GPT over the 49 codes,
  conditioned on a class token in front (`[sneaker] c₁ … c₄₉`); sample, decode, look. 49
  sequential steps per image. Inspect the failure the order invites: the top rows are
  committed before the bottom is known.
- **7.3** **Masked / confidence order: MaskGIT (Chang et al. 2022).** Bidirectional
  Transformer trained BERT-style on randomly masked codes; at sampling time start fully
  masked, predict every cell, **keep the most confident**, re-mask the rest on a cosine
  schedule, repeat (~8 iterations instead of 49). **Pin:** retrain the Phase 7.2 model with
  a masking objective and sample in 8 steps; compare. Muse (Chang et al. 2023) scales it
  to text-to-image. Audio twin: **VampNet and MAGNeT** are MaskGIT on codec tokens
  (`audio-codec-lms` Phase 6). Masked decoding is **not** diffusion: discrete tokens,
  confidence-based unmasking.
- **7.4** **Next-scale prediction: VAR (Tian et al. 2024).** Redefine "next" as the next
  **resolution**. A multi-scale residual tokenizer quantizes the residual at scales
  1 × 1, 2 × 2, …, with one shared codebook: quantize the coarsest map, upsample its
  embedding, subtract, quantize the residual at the next scale, and so on. That is a
  **quantized Laplacian pyramid**, and residual quantization across *scales* is the
  vision cousin of RVQ's residual across *codebook depth*. The Transformer predicts a whole
  scale in parallel, with a **block-causal** mask (each scale sees itself and all coarser
  scales). VAR was the first AR model to beat a DiT on ImageNet 256 (FID 1.73 vs DiT-XL/2's
  2.27) and showed LLM-like power-law scaling. ImageNet scales (1,2,3,4,5,6,8,10,13,16)
  give **10 steps for 680 tokens**.
- **7.5** **Pin to Fashion-MNIST: next-scale vs raster.** Scales **(1, 2, 3, 5, 7)**:
  **5 AR steps** producing 1 + 4 + 9 + 25 + 49 = **88 tokens**, versus raster's 49 steps
  for 49 tokens. Draw the block-causal mask by hand first (an 88 × 88 matrix of five
  blocks). Then train the multi-scale tokenizer and the scale-wise Transformer (CPU-
  feasible at this size with patience, ~10–20 minutes; or Colab), sample, and compare
  samples, step counts and Fashion-FID with 7.2 and 7.3. Kill "next-scale is diffusion":
  no noise, cross-entropy over discrete codes.
- **7.6** **AR without a codebook, and other orders.** **MAR** (Li et al. 2024): continuous
  tokens, with a small per-token **diffusion loss** head modeling `p(x | z)`, in a masked
  random order (FID 1.55). **RAR** (Yu et al. 2024): keep raster at inference but train on
  random permutations, annealed back to raster (FID 1.48). **xAR** (Ren et al. 2025):
  generalize "next" to any entity X (cell, subsample, scale, image), regress it with flow
  matching, and train on noisy context to fight exposure bias (FID 1.24, the AR leader in
  the wiki as of early 2025). **ELM** (Liu et al. 2024): binary/lookup-free tokenizers beat
  VQGAN; AR beats masked LMs. Honest flag: these FIDs are each paper's own ImageNet-256
  numbers under its own setup, and the ranking moves.
- **7.7** **AR images ↔ codec-LMs (the bridge).** Raster AR over image codes ↔ MusicGen
  over codec tokens; MaskGIT ↔ VampNet/MAGNeT; VAR's scale residual ↔ RVQ's depth residual
  (and MusicGen's codebook *patterns* are another answer to "what order for a multi-stream
  grid"); MAR's diffusion head ↔ the continuous branch. A learner who can fill this table
  has the keystone.

## Phase 8 — Aligning Two Sequences: CLIP
- **8.1** **Contrastive alignment (Radford et al. 2021).** Two towers, an image encoder
  and a text encoder, each ending in a unit-norm embedding. For a batch of `N` matched
  pairs form the `N × N` matrix of cosine similarities (a table of normalized
  correlations), divide by a temperature τ (learnable, initialized to 0.07), and apply
  cross-entropy along rows and along columns: the diagonal should win. This is
  **InfoNCE** (van den Oord, Li & Vinyals 2018) at web scale: 400M image–text pairs. CLIP
  does not generate anything; it is an aligned pair of encoders.
- **8.2** **Zero-shot classification by prompt.** Embed `"a photo of a {class}"` for
  every class, embed the image, pick the most similar prompt: a bank of text-defined
  templates, matched-filter style. CLIP's best model matched a supervised ResNet-50 on
  ImageNet without training on it.
- **8.3** **Pin to Fashion-MNIST: a tiny CLIP.** Image tower = your Phase 1 CNN or Phase
  5 ViT; text tower = a small bag-of-words or tiny Transformer over templated captions
  with synonyms ("a photo of a sneaker", "a running shoe", "a pair of trousers",
  "pants", "a handbag"). Train on the training split. Then zero-shot classify the test
  split with **held-out templates and synonyms**, and compare with your supervised
  classifier. Optional and honest: hold out one class (Sandal) entirely, keep shared
  words ("shoe", "footwear") in other captions, and test whether "an open shoe, a sandal"
  retrieves sandals. Expect it to work poorly with ten labels' worth of language. That
  is why CLIP needed the web.
- **8.4** **Successors.** **SigLIP** (Zhai et al. 2023) replaces the batch softmax with an
  independent **sigmoid** per pair, which decouples the loss from batch size; SigLIP-family
  towers are now the usual vision encoders inside multimodal LLMs (Phase 10). Encoders
  learned without language (DINOv2, Oquab et al. 2023) are the other camp: a live
  question, revisited in Phase 12.
- **8.5** **CLIP ↔ CLAP / MuLan (the bridge).** The same recipe on audio–text pairs gives
  CLAP and MuLan. The trick both audio tracks use: train a generator conditioned on the
  **audio** embedding (no captions needed), then swap in the **text** embedding at
  inference; unCLIP (Phase 9.2) does the image version. `audio-codec-lms` Phase 4 and
  `audio-diffusion-dit` Phase 1.3 rely on it.

## Phase 9 — Text to Image: DALL-E, and the Diffusion Turn
- **9.1** **DALL-E (Ramesh et al. 2021): one sequence, raster AR.** A **discrete VAE**
  (trained with a Gumbel-softmax relaxation, not straight-through VQ) turns a 256 × 256
  image into **32 × 32 = 1,024 codes** from an 8,192-entry codebook; up to **256 BPE text
  tokens** go in front; one **12B-parameter** sparse Transformer models the concatenated
  sequence autoregressively, trained on 250M image–text pairs. Sample many, **rerank with
  CLIP**. On the keystone map: discrete codes, raster order, text as a prefix.
- **9.2** **DALL-E 2 and Imagen (2022): the turn to diffusion.** **unCLIP** (Ramesh et al.
  2022): text → CLIP text embedding → a *prior* → a CLIP image embedding → a **diffusion
  decoder**. **Imagen** (Saharia et al. 2022): a frozen **T5-XXL** text encoder conditions a
  cascade of pixel-space diffusion U-Nets (64 → 256 → 1024); scaling the text encoder
  helped more than scaling the U-Net. Audio echo: Tango's frozen Flan-T5
  (`audio-diffusion-dit` 2.1). Kill "DALL-E is a diffusion model": the first one is not.
- **9.3** **Latent diffusion (Rombach et al. 2021).** Compress with an autoencoder (Phase
  3.5, downsampling by 4–8), run a **U-Net** denoiser (Phase 2) in the latent, inject text
  by **cross-attention**. Recall-primer: `ai-foundations` 6.2–6.4 (forward noise, reverse
  denoise, the network predicts the noise). For the training objective in depth, see
  [`flow-matching/`](../flow-matching/) and `audio-diffusion-dit`'s primer; this course
  stays with what the cell is and what order produces it.
- **9.4** **The DiT is a ViT over latent patches (Peebles & Xie 2022).** Patchify the
  latent (Phase 5.1 again: a 256 × 256 image → a 32 × 32 × 4 latent → patch 2 → **256
  tokens**), run Transformer blocks, inject timestep and class by **adaLN-Zero**. These
  tokens are **continuous latent patches**, denoised all at once. `audio-diffusion-dit`
  Phase 3 takes this to audio; this topic's job is to make "it's a ViT" obvious so that
  course can go fast.
- **9.5** **Pin to Fashion-MNIST.** Tier-aware: either (a) by hand, put a tiny
  label-conditioned DiT on the map (cells = 4 × 4 pixel patches, 49 tokens; order =
  denoise all; condition = label embedding via adaLN) and contrast its 20–50 denoising
  passes with VAR's 5 and raster's 49; or (b) train it with a flow-matching loss for a few
  CPU or Colab minutes and compare samples and Fashion-FID with Phase 7.
- **9.6** **Why diffusion won images and AR won text (an honest hypothesis).** The wiki's
  "decision vs resolution" argument: text is a sequence of discrete decisions, an image is
  progressive refinement of a fixed-size canvas, and audio sits between (codec-LMs for
  composition, diffusion for rendering). Informal, not a theorem, and VAR/xAR (Phase 7)
  are live counterevidence on ImageNet. Read
  `ai-2012-to-2023/wiki/diffusion-vs-autoregressive-by-modality.md`.

## Phase 10 — Unified Multimodal Models
- **10.1** **Three design points (as BAGEL names them).** **Quantized AR**: discretize
  every modality, one LM over a joint vocabulary (Chameleon). **External diffuser**: an
  LLM emits a small latent that conditions a separate diffusion model (common in 2023-era
  production systems). **Integrated Transformer**: one Transformer, LM loss on text,
  diffusion/flow loss on image latents, in one sequence (Transfusion, BAGEL). Place each on
  the keystone map.
- **10.2** **Chameleon (Meta 2024): discretize everything.** An image tokenizer with an
  8,192-entry codebook maps a 512 × 512 image to **1,024 codes**, merged into a 65,536-entry
  vocabulary with text; one decoder-only Transformer, early fusion, trained to 34B
  parameters on ~10T tokens. The contribution beyond feasibility is the **stability
  recipe**: QK-Norm, careful norm placement, z-loss. The cost: the VQ bottleneck caps image
  quality.
- **10.3** **Transfusion (Meta 2024): two losses, one sequence.** Keep images as
  continuous VAE-latent patches; text positions get next-token cross-entropy, image
  positions get a diffusion loss, summed every step. The attention mask is **causal over
  text and bidirectional within each image**. Reported: about **⅓ of Chameleon's FLOPs**
  for matched image quality, and gains on text too. **Pin:** draw the mask for
  `<bos> a sneaker <boi> p₁ … p₄₉ <eoi>` on Fashion-MNIST (count the positions; shade
  which attend to which). Tier b: train the toy (one tiny Transformer, LM loss on the
  caption, flow loss on 49 patches) so the same model both captions and generates.
  Honest flag: the FLOP ratios come from one lab's matched-compute study.
- **10.4** **Sparse multimodal: MoE and MoT.** **MoE recap** (Shazeer et al. 2017; Switch,
  Fedus et al. 2021): a learned router sends each token to its top-k expert FFNs, with a
  load-balancing loss. **MoT** (Liang et al. 2024): give each modality its own FFNs,
  attention projections and norms, keep **self-attention global**, route
  **deterministically by modality**: no router, no auxiliary loss. Reported: Chameleon-
  setting quality at 55.8% of dense FLOPs; Transfusion-setting image quality at ~33%. The
  two compose. **BAGEL** (ByteDance 2025, 14B total / 7B active) splits by **role**
  instead (an understanding expert and a generation expert) and feeds them **two
  encoders**: a semantic ViT for understanding, a VAE for generation, because
  understanding wants invariant features and generation wants reconstructable ones.
- **10.5** **World-model capabilities: read the claim carefully.** BAGEL reports staged
  emergence (understanding and generation first, then editing, then long-context
  compositional "world modeling": future-frame prediction, 3D manipulation, navigation)
  that appears only with large interleaved video + web data. Why video might matter
  (pixel, conceptual, temporal and physical continuity). And the honest summary: striking
  qualitative samples, a benchmark (IntelligentBench) from the same team, and "emergence"
  that can be a metric artifact (Schaeffer et al. 2023). Replication is the open
  question.
- **10.6** **The bridge.** The three design points in audio: **quantized AR** is the
  codec-LM (MusicGen, AudioLM; speech-text models like Moshi); the **external diffuser**
  shape is AudioLDM 2's GPT-2 → LOA → LDM and ACE-Step's LM-planner → DiT-renderer
  (`audio-diffusion-dit` 2.2, 7.3); the **integrated Transformer** for audio is rarer.
  MoT's three-modality experiments add speech as a third parameter pool.

## Phase 11 — Putting It Together
- **11.1** **The map.** Fill in the keystone's tokenizer × order map with every system in
  the course: AlexNet, ResNet, U-Net, VAE, DCGAN, StyleGAN, ViT, AST, VQ-VAE, VQGAN,
  PixelCNN, LlamaGen, MaskGIT, Muse, VAR, MAR, RAR, xAR, CLIP, SigLIP, DALL-E, DALL-E 2,
  Imagen, LDM, DiT, Chameleon, Transfusion, MoT, BAGEL, and your own Fashion-MNIST
  models. Then fill the audio-bridge table from memory.
- **11.2** **Capstone — a mini-DALL-E on Fashion-MNIST.** Tiered like room-acoustics'
  a/b/c, no GPU required:
  - **(a) CPU (default).** Build the whole 2021 recipe at toy scale: your **7 × 7 VQ
    tokenizer** (Phase 6), a tiny **raster-AR Transformer** over `[caption tokens; 49
    codes]` (Phase 7.2), and your **tiny CLIP** (Phase 8.3) to **rerank** samples, as
    DALL-E did. Prompt with held-out phrasings ("a running shoe"); report Fashion-FID,
    the accuracy of your Phase 1.5 classifier on the generated images, and a one-page
    "tokenizer × order report" placing your system on the map.
  - **(b) Colab GPU.** Tier a, plus the **next-scale** (scales 1,2,3,5,7) and **MaskGIT**
    orders over the same tokenizer, compared at matched compute on steps, samples and
    Fashion-FID; or the **Transfusion toy** (one Transformer that both captions and
    generates).
  - **(c) Local GPU.** Tier a or b, plus *either* the **spectrogram bridge** at scale
    (a VQGAN-style tokenizer on mel patches of piano audio, AR or next-scale generation
    of the code grid, and audio back by Griffin-Lim or a pretrained vocoder, then
    *listen*), *or* run a small open pretrained system (for example a public VAR
    checkpoint, or a ~1B unified model such as Janus-Pro-1B) and inspect its real token
    grid and order. Fail fast if a checkpoint or download is unavailable; do not swap in
    a different model silently.
- **11.3** **Where to go next.** You can now read the ViT, VQGAN, MaskGIT, VAR, CLIP,
  DALL-E, LDM, DiT, Chameleon, Transfusion and BAGEL papers. Track A:
  `audio-diffusion-dit` (the DiT on audio), `audio-codec-lms` (the codec-LM side of Phase
  7), `disentanglement` (Phase 3.4 and 4.4 in depth). Track B: `ai-sequence-models` (what
  a token can attend to, and at what cost: the attention side of Phases 5 and 10) and
  `ai-post-training-and-rl`. Both: `flow-matching` for the objective behind modern DiTs;
  the curated wikis for new papers; Phase 12 for the edge.

## Phase 12 — The Frontier (a living section)
> **This phase tracks the moving edge of the field and is revised as it moves**
> (last revised 2026-10-29). Treat it as depth-on-demand, never a gate. Every topic is
> still the keystone, a new choice of **tokenizer** or **order**, and each is pinned to
> the same Fashion-MNIST grid. Be honest that the rankings here change between sessions:
> the music423-2023 wikis' newest image-generation entries are xAR (Feb 2025) and BAGEL
> (May 2025), so items below that postdate them come from outside the collection and
> should be ingested into the wikis when they prove durable. When in doubt, read the
> linked paper and update this section.

- **12.1** **The tokenizer frontier.** Three moves. *(i) Simpler quantizers:* FSQ
  (round each dimension to a few levels; no codebook to collapse), lookup-free and
  bitwise codes (MAGVIT-v2's LFQ; Infinity's bitwise tokens with an effectively unbounded
  vocabulary). *(ii) Fewer, 1-D tokens:* TiTok represents an image with as few as **32**
  tokens in a 1-D sequence, abandoning the grid entirely; the order question changes
  shape when there is no grid. *(iii) The reconstruction-vs-generation dilemma:* a latent
  that reconstructs best is not the one that is easiest to *generate*. Aligning the
  latent (or the denoiser's features) with a pretrained vision encoder speeds diffusion
  training dramatically (REPA; VA-VAE), and 2025 work goes further, using a frozen
  representation encoder (DINOv2/SigLIP-style) itself as the autoencoder's encoder (RAE).
  **Pin:** swap your 7 × 7 VQ for FSQ with levels (8, 5, 5) = 200 implicit codes; compare
  codebook usage and reconstruction. *Honest flag:* "which tokenizer is best" is
  unsettled; every paper's FID comes with its own decoder, data and budget.

- **12.2** **The order frontier: continuous AR and scale-wise everything.** The 2024–25
  pattern is AR over **continuous** tokens with a small diffusion or flow head (MAR,
  Fluid, xAR), with **random or scale-wise** orders rather than raster, and bitwise
  next-scale models (Infinity) pushing VAR to high-resolution text-to-image. Meanwhile
  diffusion keeps borrowing AR's strengths (and vice versa): the boundary between "order"
  and "noise schedule" is blurring (see 12.4's diffusion forcing). **Pin:** give your
  Phase 7.2 model a tiny MLP flow head over continuous 4 × 4 patches instead of codes,
  sample in random order, and compare with the discrete version. *Honest flag:* AR vs
  diffusion on *text-to-image* (not just ImageNet) is still contested.

- **12.3** **Unified models: decouple the encoders, share the backbone.** The Chameleon →
  Transfusion → BAGEL line keeps moving. **Janus / Janus-Pro** decouple the visual
  encoder for understanding (a SigLIP-style tower) from the one for generation (a VQ
  tokenizer) inside one AR Transformer; **Show-o** mixes AR text with discrete-diffusion
  (masked) image generation in one model; **Emu3** argues next-token prediction over
  discrete tokens is enough for images *and* video; another 2025 line bolts a frozen LLM
  to a diffusion decoder through learnable query tokens (MetaQueries, BLIP3-o), a modern
  "external diffuser." Closed systems (native image generation in GPT-4o and Gemini) are
  strong but architecturally undocumented: say so rather than guess. **Pin:** for each,
  name the tokenizer per modality and the order per modality, then place it on the map.
  *Honest flag:* the leaderboards here change monthly and many evaluations are in-house.

- **12.4** **World models: video as the next sequence.** A video is a 3-D grid, so the
  keystone applies with time as a third axis. **Genie** (Bruce et al. 2024) learns an
  interactive environment from unlabeled video with a video tokenizer, a latent-action
  model and a **MaskGIT-style** dynamics model: Phase 7.3, now over time. **Diffusion
  forcing** (Chen et al. 2024) gives each token its own noise level, interpolating
  between next-token prediction and full-sequence diffusion: order and noise as one
  knob. **Cosmos** (NVIDIA 2025) ships both diffusion and AR world models over both
  continuous and discrete video tokenizers, which is the tokenizer × order map applied to
  physical-AI video. Predictive non-generative models (V-JEPA 2, Meta 2025) argue you
  should predict in representation space, not pixels. **Pin:** extend the Fashion-MNIST
  grid with a time axis (a shirt sliding one pixel per frame) and count tokens per
  second under raster, next-frame and next-scale orders. *Honest flag:* "world model"
  is used loosely; separate demo videos from measured capability, as in 10.5.

- **12.5** **Back to audio.** The vision frontier keeps landing in audio a year or two
  later: FSQ and lookup-free codes in codecs, continuous-token AR with diffusion heads
  for speech and music, representation-aligned latents for audio DiTs, and unified
  any-to-any models that include speech. When a vision idea above shows up in an audio
  paper, add it to the bridge table in the keystone and tell the learner which Track A
  course it touches.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. The
   recurring picture is the **grid and its order**: draw the 28 × 28 image, the 7 × 7
   grid of cells, and the order in which they are produced. For DSP-fluent learners, use
   the DSP picture (filter bank, decimation, pyramid, VQ) and say where it is exact and
   where it is only an analogy.
3. **Pin it to Fashion-MNIST.** The same images, the same 49 cells, every phase. A plot
   of real samples beats a diagram; a confusion matrix beats an accuracy number. Where the
   idea has an audio twin, pin it also to the through-line clip's mel spectrogram.
4. **Tiny exercise** to verify: count tokens and steps, trace an attention mask, predict
   a behavior ("ViT or CNN on 10k images?"), or run a few lines of PyTorch. Keep CPU
   training runs to a few minutes. The exercise *is* the check.
5. **Common misreadings** when relevant: keep
   [`the-image-as-sequence.md`](the-image-as-sequence.md)'s list live; flag and correct on
   the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences, in keystone terms ("VAR keeps discrete codes
   but changes the order: one whole scale per step, coarse to fine, with a residual
   quantizer that is a quantized Laplacian pyramid").
2. Carry out the small task: count the tokens and steps for an image or a spectrogram,
   draw the mask, train the toy on Fashion-MNIST, or place a system on the tokenizer ×
   order map, and explain each step.
3. Spot a deliberately wrong claim ("DALL-E 1 is a diffusion model" — no, discrete AR;
   "ViT has no convolution" — the patch embedding is one; "next-scale prediction is
   diffusion" — no noise, cross-entropy over codes).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wikis this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wikis stay
canonical, the course stays pedagogical. The collection is JOS's
[`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023) (branch `master`;
local clone `/w/music423-2023`):

- **[`images/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/images/wiki)**
  (Phases 1–4). Concept pages: `residual-connections.md`,
  `generative-adversarial-networks.md`, `latent-space-disentanglement.md`. Source
  summaries: `resnet-deep-residual-learning`, `resnet-identity-mappings`, `stylegan`.
  PDFs in [`images/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/images):
  AlexNet, ResNet (both), U-Net, VAE, GANs, StyleGAN, DiT.
- **[`images-ar/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/images-ar/wiki)**
  (Phases 5–7). Concept pages: `tokenization-approaches.md` (VQ vs continuous, the
  comparison table), `visual-autoregressive-modeling.md` (the ordering problem),
  `next-scale-prediction.md`. Source summaries: `vit-vision-transformer`,
  `ast-audio-spectrogram-transformer`, `var-visual-autoregressive`,
  `mar-autoregressive-without-vq`, `elm-elucidate-language-model`,
  `rar-randomized-autoregressive`, `xar-next-x-prediction`.
- **[`multimodal/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/multimodal/wiki)**
  (Phases 8–10). Concept pages: `unified-multimodal-architectures.md`,
  `tokenization-strategies.md`, `hybrid-ar-diffusion.md`,
  `sparse-multimodal-architectures.md`, `world-model-capabilities.md`. Source summaries:
  `chameleon-team-2024`, `transfusion-zhou-2024`, `mixture-of-transformers-liang-2024`,
  `bagel-deng-2025`. PDFs in
  [`multimodal/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/multimodal)
  also include DALL-E, CLIP and Imagen (no wiki summaries yet; use the CLIP landmark note
  below).
- **[`ai-2012-to-2023/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-2012-to-2023/wiki)**
  (cross-cutting). `generative-modeling-frameworks.md` (VAE / GAN / AR / VQ-VAE /
  diffusion), `diffusion-vs-autoregressive-by-modality.md` (Phase 9.6),
  `representation-learning-arc.md` (CLIP's place), and the landmark notes
  `notes/alexnet.md`, `notes/resnet.md`, `notes/clip.md`, `notes/ddpm.md`.
- **Bridges into Track A's wikis:**
  [`ai-audio-codecs/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-audio-codecs/wiki)
  (`vector-quantization.md`, `residual-vector-quantization.md`, `codebook-learning.md`,
  `adversarial-training-audio.md`; sources `vq-vae`, `fsq`, `vector-quantization-gray`,
  `ast-audio-spectrogram-transformer`),
  [`diffusion/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/diffusion/wiki)
  (`latent-diffusion-models.md`; sources `dit-peebles-2022`, `sd3-esser-2024`,
  `diffsound-yang-2022`), and
  [`disentanglement/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/disentanglement/wiki)
  (Phases 3.4 and 4.4 point there).
- Keep the course in sync if the wikis gain papers; the wikis are canonical, the course
  is the lesson plan over them.

### Source papers (the vision and multimodal lineage this course tracks)
*Phases 1–4: backbones and one-shot generators*
- **Krizhevsky, Sutskever & Hinton (2012)** — *ImageNet Classification with Deep
  Convolutional Neural Networks* (AlexNet). NeurIPS 2012 (no arXiv).
- **He, Zhang, Ren & Sun (2015)** — *Deep Residual Learning for Image Recognition*.
  arXiv:1512.03385.
- **He, Zhang, Ren & Sun (2016)** — *Identity Mappings in Deep Residual Networks*.
  arXiv:1603.05027.
- **Ronneberger, Fischer & Brox (2015)** — *U-Net*. arXiv:1505.04597.
- **Kingma & Welling (2013)** — *Auto-Encoding Variational Bayes* (VAE). arXiv:1312.6114.
- **Goodfellow et al. (2014)** — *Generative Adversarial Nets*. arXiv:1406.2661.
- **Radford, Metz & Chintala (2015)** — *DCGAN*. arXiv:1511.06434.
- **Heusel et al. (2017)** — *GANs Trained by a Two Time-Scale Update Rule…* (FID).
  arXiv:1706.08500.
- **Karras, Laine & Aila (2018)** — *A Style-Based Generator Architecture for GANs*
  (StyleGAN). arXiv:1812.04948.
- **Karras et al. (2021)** — *Alias-Free Generative Adversarial Networks* (StyleGAN3).
  arXiv:2106.12423.
- **Zhang (2019)** — *Making Convolutional Networks Shift-Invariant Again*.
  arXiv:1904.11486.
- **Xiao, Rasul & Vollgraf (2017)** — *Fashion-MNIST*. arXiv:1708.07747.

*Phases 5–7: the image as a sequence*
- **Dosovitskiy et al. (2020)** — *An Image is Worth 16x16 Words* (ViT). arXiv:2010.11929.
- **Gong, Chung & Glass (2021)** — *AST: Audio Spectrogram Transformer*. arXiv:2104.01778.
- **Touvron et al. (2020)** — *Training data-efficient image transformers & distillation
  through attention* (DeiT). arXiv:2012.12877.
- **Liu et al. (2022)** — *A ConvNet for the 2020s* (ConvNeXt). arXiv:2201.03545.
- **He et al. (2021)** — *Masked Autoencoders Are Scalable Vision Learners* (MAE).
  arXiv:2111.06377.
- **van den Oord, Vinyals & Kavukcuoglu (2017)** — *Neural Discrete Representation
  Learning* (VQ-VAE). arXiv:1711.00937.
- **Razavi, van den Oord & Vinyals (2019)** — *Generating Diverse High-Fidelity Images
  with VQ-VAE-2*. arXiv:1906.00446.
- **Esser, Rombach & Ommer (2021)** — *Taming Transformers for High-Resolution Image
  Synthesis* (VQGAN). arXiv:2012.09841.
- **Gray (1984)** — *Vector Quantization*, IEEE ASSP Magazine (no arXiv; PDF in
  `ai-audio-codecs/`).
- **Bengio, Léonard & Courville (2013)** — *Estimating or Propagating Gradients Through
  Stochastic Neurons* (straight-through estimator). arXiv:1308.3432.
- **van den Oord et al. (2016)** — *Conditional Image Generation with PixelCNN Decoders*.
  arXiv:1606.05328.
- **Chang et al. (2022)** — *MaskGIT: Masked Generative Image Transformer*.
  arXiv:2202.04200.
- **Chang et al. (2023)** — *Muse: Text-To-Image Generation via Masked Generative
  Transformers*. arXiv:2301.00704.
- **Sun et al. (2024)** — *Autoregressive Model Beats Diffusion: Llama for Scalable Image
  Generation* (LlamaGen). arXiv:2406.06525.
- **Tian et al. (2024)** — *Visual Autoregressive Modeling: Scalable Image Generation via
  Next-Scale Prediction* (VAR). arXiv:2404.02905.
- **Li et al. (2024)** — *Autoregressive Image Generation without Vector Quantization*
  (MAR). arXiv:2406.11838.
- **Liu et al. (2024)** — *Elucidating the Design Space of Language Models for Image
  Generation* (ELM). arXiv:2410.16257.
- **Yu et al. (2024)** — *Randomized Autoregressive Visual Generation* (RAR).
  arXiv:2411.00776.
- **Ren et al. (2025)** — *Beyond Next-Token: Next-X Prediction for Autoregressive Visual
  Generation* (xAR). arXiv:2502.20388.
- **Mentzer et al. (2023)** — *Finite Scalar Quantization: VQ-VAE Made Simple* (FSQ).
  arXiv:2309.15505.

*Phases 8–10: alignment, text-to-image, unified models*
- **van den Oord, Li & Vinyals (2018)** — *Representation Learning with Contrastive
  Predictive Coding* (InfoNCE). arXiv:1807.03748.
- **Radford et al. (2021)** — *Learning Transferable Visual Models From Natural Language
  Supervision* (CLIP). arXiv:2103.00020.
- **Zhai et al. (2023)** — *Sigmoid Loss for Language Image Pre-Training* (SigLIP).
  arXiv:2303.15343.
- **Oquab et al. (2023)** — *DINOv2: Learning Robust Visual Features without
  Supervision*. arXiv:2304.07193.
- **Ramesh et al. (2021)** — *Zero-Shot Text-to-Image Generation* (DALL-E).
  arXiv:2102.12092.
- **Ramesh et al. (2022)** — *Hierarchical Text-Conditional Image Generation with CLIP
  Latents* (DALL-E 2 / unCLIP). arXiv:2204.06125.
- **Saharia et al. (2022)** — *Photorealistic Text-to-Image Diffusion Models with Deep
  Language Understanding* (Imagen). arXiv:2205.11487.
- **Rombach et al. (2021)** — *High-Resolution Image Synthesis with Latent Diffusion
  Models* (LDM). arXiv:2112.10752.
- **Peebles & Xie (2022)** — *Scalable Diffusion Models with Transformers* (DiT).
  arXiv:2212.09748.
- **Chameleon Team (2024)** — *Chameleon: Mixed-Modal Early-Fusion Foundation Models*.
  arXiv:2405.09818.
- **Zhou et al. (2024)** — *Transfusion: Predict the Next Token and Diffuse Images with
  One Multi-Modal Model*. arXiv:2408.11039.
- **Shazeer et al. (2017)** — *Outrageously Large Neural Networks: The Sparsely-Gated
  Mixture-of-Experts Layer*. arXiv:1701.06538.
- **Fedus, Zoph & Shazeer (2021)** — *Switch Transformers*. arXiv:2101.03961.
- **Liang et al. (2024)** — *Mixture-of-Transformers: A Sparse and Scalable Architecture
  for Multi-Modal Foundation Models*. arXiv:2411.04996.
- **Deng et al. (2025)** — *Emerging Properties in Unified Multimodal Pretraining*
  (BAGEL). arXiv:2505.14683.
- **Schaeffer, Miranda & Koyejo (2023)** — *Are Emergent Abilities of Large Language
  Models a Mirage?* arXiv:2304.15004.

### Frontier sources (Phase 12 — a living list, updated as the field moves)
These track the current edge and *will* be added to and reordered as the field moves;
treat them as the reading behind Phase 12, not a fixed canon. Where an arXiv ID is not
given, cite by title and authors and look it up before quoting it.

- **12.1 — tokenizers.** Mentzer et al. (2023), *FSQ*, arXiv:2309.15505; Yu et al. (2023),
  *Language Model Beats Diffusion: Tokenizer is Key to Visual Generation* (MAGVIT-v2,
  LFQ), arXiv:2310.05737; Yu et al. (2024), *An Image is Worth 32 Tokens for
  Reconstruction and Generation* (TiTok), arXiv:2406.07550; Han et al. (2024),
  *Infinity: Scaling Bitwise AutoRegressive Modeling for High-Resolution Image Synthesis*,
  arXiv:2412.04431; Yu et al. (2024), *Representation Alignment for Generation: Training
  Diffusion Transformers Is Easier Than You Think* (REPA), arXiv:2410.06940; Yao et al.
  (2025), *Reconstruction vs. Generation: Taming Optimization Dilemma in Latent Diffusion
  Models* (VA-VAE), arXiv:2501.01423; Zheng et al. (2025), *Diffusion Transformers
  with Representation Autoencoders* (RAE) (look up the ID).
- **12.2 — continuous and scale-wise AR.** Li et al. (2024), *MAR*, arXiv:2406.11838; Fan
  et al. (2024), *Fluid: Scaling Autoregressive Text-to-image Generative Models with
  Continuous Tokens*, arXiv:2410.13863; Ren et al. (2025), *xAR*, arXiv:2502.20388; Han et
  al. (2024), *Infinity*, arXiv:2412.04431.
- **12.3 — unified models.** Wu et al. (2024), *Janus: Decoupling Visual Encoding for
  Unified Multimodal Understanding and Generation*, arXiv:2410.13848; Chen et al. (2025),
  *Janus-Pro: Unified Multimodal Understanding and Generation with Data and Model
  Scaling*, arXiv:2501.17811; Xie et al. (2024), *Show-o: One Single Transformer to Unify
  Multimodal Understanding and Generation*, arXiv:2408.12528; Wang et al. (2024), *Emu3:
  Next-Token Prediction is All You Need*, arXiv:2409.18869; Deng et al. (2025), *BAGEL*,
  arXiv:2505.14683; Pan et al. (2025), *Transfer between Modalities with MetaQueries*
  (look up the ID); Chen et al. (2025), *BLIP3-o: A Family of Fully Open Unified
  Multimodal Models* (look up the ID); Tschannen et al. (2025), *SigLIP 2*,
  arXiv:2502.14786.
- **12.4 — world models.** Bruce et al. (2024), *Genie: Generative Interactive
  Environments*, arXiv:2402.15391; Chen et al. (2024), *Diffusion Forcing: Next-token
  Prediction Meets Full-Sequence Diffusion*, arXiv:2407.01392; NVIDIA (2025), *Cosmos World
  Foundation Model Platform for Physical AI*, arXiv:2501.03575; Assran et al. (2025),
  *V-JEPA 2* (Meta; look up the ID); OpenAI (2024), *Video generation models as world
  simulators* (Sora technical report, no arXiv).
- **12.5 — audio echoes.** Keep in sync with the Track A courses' own frontier lists
  (`flow-matching/` Phase 9; `audio-diffusion-dit` frontier notes) rather than
  duplicating them here.
