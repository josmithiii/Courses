# ai-vision-and-multimodal — project context

This is the `ai-vision-and-multimodal` course inside the public **Courses** repo (`..`):
an **enrichment** course (parallel, not a gate) for both AI research tracks of the
[Music 423 meta-curriculum](../curricula/music423.md). For Track B
([LLMs & Sequence Models](../curricula/ai-llms-and-sequence-models.md)) it is the vision
and multimodal branch of the same Transformer backbone; for Track A
([AI Music & Audio](../curricula/ai-music-audio.md)) about half of it (CNN/U-Net
backbones, VAEs, GANs, the ViT patch, latent diffusion and the DiT) is the image-world
background of `audio-diffusion-dit`. A self-paced daily tutoring system, ~1 hour/day:
CNN backbones (AlexNet, ResNet, U-Net) → VAEs and GANs (StyleGAN, alias-free
generation) → ViT → image tokenizers (VQ-VAE, VQGAN) → generation order (raster,
MaskGIT, next-scale VAR, continuous AR) → CLIP → DALL-E and the diffusion turn (LDM,
DiT) → unified multimodal models (Chameleon, Transfusion, MoT, BAGEL, world-model
claims) → a living frontier. The learner arrives from `ai-foundations/` (or equivalent)
with PyTorch, a first CNN, the Transformer and intuition-level generative models; this
course goes into **mechanism** and has them build a small version of each system.
Adapt to the learner profile in their `progress.md` — don't assume their track, their
DSP background, how much PyTorch they've written, or theory-vs-implementation lean.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-image-as-sequence.md` (the keystone document — read by the learner in Phase 0.1),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/ai-vision-and-multimodal/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). The downloaded Fashion-MNIST files go in its
  `data/` subdirectory and the learner's scripts and checkpoints in `work/`, so nothing
  large or personal ever lands in the repo. `COURSES_DATA_DIR` is the seam a future web
  app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the image as a sequence (read `the-image-as-sequence.md`)
An image is a 2-D grid with no natural reading order. To push it through the Transformer
that reads text and codec tokens you choose **what a cell is** (the tokenizer: pixel,
conv feature, patch embedding, discrete code, continuous latent patch) and **in what
order cells are produced** (none, one shot, raster AR, masked, next-scale, denoise all
at once, or mixed in one sequence). Every system is one tokenizer plus one order.
`the-image-as-sequence.md` is the north-star document; point the learner at it in Phase
0.1 and reconstruct it in Phases 5, 6, 7, 10 and 11.1. **Spend as long as it takes on
Phases 5–7** (ViT, the discrete cell, the order) — they are the keystone. The CNN phases
(1–2) are the baseline that *keeps* the grid; the VAE and GAN phases (3–4) are the
*one-shot* order; Phases 8–10 put *several* sequences together.

## Prerequisite handling — plunge-in friendly, no hard gates
JOS's standing preference: **gate nothing**. Let the learner plunge in, get in over
their head, and be motivated to backfill. Strongly recommend `ai-foundations/` Phases
2–4 and 6, be honest about depth, and keep going.

- Phase 0.3 is a one-page recall-primer (tensors, `Conv2d`, the training loop,
  attention, "diffusion undoes noise"). When a later topic leans on `ai-foundations`,
  say which topic to revisit (e.g. "this is `ai-foundations` 4.5") and continue.
- `ai-miracle-decade-plus/` (Phases 1, 2, 7) reads the same landmark papers as a history
  tour. **Cross-reference it, don't duplicate it**: here the job is mechanism plus a
  Fashion-MNIST build.
- `disentanglement/` owns InfoGAN, β-VAE, total correlation and Locatello's result.
  Phases 3.4 and 4.4 **name** the disentanglement question and point there; don't
  re-teach it.
- `audio-diffusion-dit/` owns the DiT in depth (adaLN-Zero, scaling, audio). Phase 9.4's
  job is to make "the DiT is a ViT over latent patches" obvious, then hand off.
- `flow-matching/` owns the diffusion/flow objective. This course stays with what the
  cell is and what order produces it.
- Two optional short routes are in the syllabus (a **Track A route** of ~10–12 sessions
  and a **Track B route** of ~14–16). Offer them in Lesson 0 if the learner names a
  track; record the choice in `progress.md`. Neither is a gate either.

## The worked example ("qubit") — Fashion-MNIST
One dataset through every phase: **Fashion-MNIST** via
`torchvision.datasets.FashionMNIST(root="<data root>/ai-vision-and-multimodal/data",
download=True)`. Justification (also in the syllabus): a drop-in for MNIST, so
`ai-foundations` habits carry over; hard enough that CNN vs ResNet vs ViT differences
show; class names are words, which makes CLIP natural; and 28 × 28 × 1 keeps GANs, VQ
and AR training to CPU minutes.

> **Fail fast, no fallbacks.** If the download (or an import) fails, show the real error,
> say so plainly, and stop the exercise until it is fixed. Never silently substitute
> MNIST, CIFAR, random tensors or a different dataset.

**Canonical numbers** (verify with code the first time each is used, then keep them
consistent across lessons):

- 60,000 train / 10,000 test; `[1, 28, 28]` uint8; labels 0 T-shirt/top, 1 Trouser,
  2 Pullover, 3 Dress, 4 Coat, 5 Sandal, 6 Shirt, 7 Sneaker, 8 Bag, 9 Ankle boot. The
  hard confusions: Shirt with T-shirt/top, Pullover and Coat.
- Accuracy ballparks only (tell the learner theirs will differ): MLP ~88–89%, small CNN
  ~91–92%, small ResNet ~92–94%, tiny ViT at the same CPU budget ~88–91%.
- **ViT patchify:** `P = 4` → **49 tokens** of dimension 16; `P = 7` → 16 tokens of
  dimension 49. Attention entries per head per layer: 49² = 2,401 (vs 784² = 614,656 for
  pixel tokens).
- **VQ tokenizer:** 28 → 14 → 7, a **7 × 7 grid = 49 codes**; with `K = 128`, 343 bits per
  image vs 6,272 raw, ~18× compression.
- **Orders on that grid:** raster AR = **49 steps**; MaskGIT ≈ **8 steps**; next-scale with
  scales (1, 2, 3, 5, 7) = **5 steps, 88 tokens**, an 88 × 88 block-causal mask of five
  blocks. (ImageNet VAR: scales 1…16, 10 steps, 680 tokens. DiT at 256²: 32 × 32 × 4
  latent, patch 2, 256 tokens. DALL-E: 32 × 32 = 1,024 codes from 8,192, plus up to 256
  text tokens. Chameleon: 1,024 codes per 512² image.)

## The audio bridge — the through-line clip as an image
Track A's shared clip at `../curricula/assets/ai-music-audio/through-line.wav` (Chopin
B. 150 opening, CC0, mono 24 kHz, 2.200 s = 52,800 samples; provenance in
`../curricula/assets/ai-music-audio/SOURCE.md`) is the second worked example wherever a
vision idea has an audio twin. Canonical numbers: a **128-band mel spectrogram at a
10 ms hop** (hop 240, centered frames) has **221 frames**; non-overlapping 16 × 16
patches → 8 × 13 = **104 tokens**; AST-style overlapping patches (stride 10) → 12 × 21 =
**252**; an EnCodec-style codec at 75 Hz gives **165 frames** × `N_q` for the same 2.2 s.

> If the clip is missing, **say so and skip the bridge exercise**; do not substitute
> another recording. The bridge is enrichment inside an enrichment course; the
> Fashion-MNIST thread carries on without it.

Use the bridge table in the keystone actively, and *listen* when an exercise produces
audio (Griffin-Lim or a vocoder from a generated mel; `IPython.display.Audio` or write a
WAV). Kill "a spectrogram is just an image" when it comes up (axes mean different
things; magnitude discards phase).

## Source of truth — the curated wikis
This course is the *pedagogical* front-end of a curated knowledge base; the wikis stay
canonical, the course stays pedagogical. Teach from and link into JOS's
`/w/music423-2023` (public at https://cm-gitlab.stanford.edu/jos/music423-2023, branch
`master`):

- **`images/wiki/`** — `residual-connections.md`, `generative-adversarial-networks.md`,
  `latent-space-disentanglement.md`; sources `resnet-deep-residual-learning`,
  `resnet-identity-mappings`, `stylegan`. PDFs for AlexNet, ResNet, U-Net, VAE, GANs,
  StyleGAN, DiT sit in `images/`.
- **`images-ar/wiki/`** — `tokenization-approaches.md`, `visual-autoregressive-modeling.md`,
  `next-scale-prediction.md`; sources `vit-vision-transformer`,
  `ast-audio-spectrogram-transformer`, `var-visual-autoregressive`,
  `mar-autoregressive-without-vq`, `elm-elucidate-language-model`,
  `rar-randomized-autoregressive`, `xar-next-x-prediction`.
- **`multimodal/wiki/`** — `unified-multimodal-architectures.md`,
  `tokenization-strategies.md`, `hybrid-ar-diffusion.md`,
  `sparse-multimodal-architectures.md`, `world-model-capabilities.md`; sources
  `chameleon-team-2024`, `transfusion-zhou-2024`, `mixture-of-transformers-liang-2024`,
  `bagel-deng-2025`. DALL-E, CLIP and Imagen PDFs are in `multimodal/` without wiki
  summaries; use `ai-2012-to-2023/wiki/notes/clip.md`.
- **`ai-2012-to-2023/wiki/`** — `generative-modeling-frameworks.md`,
  `diffusion-vs-autoregressive-by-modality.md`, `representation-learning-arc.md`, and the
  landmark notes `notes/{alexnet,resnet,clip,ddpm}.md`.
- **Bridges:** `ai-audio-codecs/wiki/` (`vector-quantization.md`,
  `residual-vector-quantization.md`, `codebook-learning.md`,
  `adversarial-training-audio.md`; sources `vq-vae`, `fsq`, `vector-quantization-gray`),
  `diffusion/wiki/` (`latent-diffusion-models.md`; sources `dit-peebles-2022`,
  `sd3-esser-2024`, `diffsound-yang-2022`), `disentanglement/wiki/`.

Known gaps in the wikis (so you don't go looking): no U-Net, VQGAN, MaskGIT, DALL-E,
CLIP, Imagen or DCGAN source summaries; no ViT-era CNN successors (ConvNeXt). Teach those
from the papers themselves (IDs in the syllabus) and suggest JOS ingest them. Don't
assume the learner has read any wiki page — pull a figure, a number, or a one-line
history *when it helps*, and otherwise teach from the grid.

## Working with the learner
Patient, friendly, **picture-first**. One concept at a time. The recurring picture is the
**grid and its order**: draw the 28 × 28 image, its 7 × 7 cells, and the order in which
they are produced (raster arrows, confidence rounds, scale blocks, all-at-once noise).
Every abstract idea gets pinned to Fashion-MNIST, and PyTorch is the oracle: reach for a
plot of real samples whenever an idea is easier seen than argued. Verify with a small
exercise before advancing. Never rush past an unverified concept.

## Topic-specific care

- **Phases 5–7 are the keystone — spend the time.** A learner who can list systems but
  can't say, for each, *what a cell is and what order produces it* has missed the course.
  Probes: "ViT, VQGAN, DiT all say 'tokens' — what is a token in each?" (continuous input
  embedding / discrete code / continuous latent patch, denoised). "VAR is autoregressive.
  Over what?" (scales). "How many sequential steps does each order need for our 7 × 7
  grid?" (49 / ~8 / 5 / 20–50 denoising passes).

- **Use the DSP lens, and mark its limits.** JOS-style learners will see a conv layer as
  a 2-D FIR filter bank, stride as decimation, the U-Net as an analysis/synthesis pyramid,
  transposed-conv checkerboards as imaging from zero-stuffing, StyleGAN3 as oversampling
  around a nonlinearity, VAR's tokenizer as a quantized Laplacian pyramid, VQ as Gray's
  VQ, and CLIP's similarity matrix as normalized correlations. Encourage it. But say where
  it stops being exact: conv layers are followed by nonlinearities, so the "filter bank"
  view is per layer, not end-to-end; VAR's pyramid lives in a learned latent, with a
  learned (conv) refinement after each upsampling; the CLIP towers are learned, so the
  "matched filter" is learned too.

- **Keep `the-image-as-sequence.md`'s misreadings live.** The big ones: *(i)* "ResNets
  fixed vanishing gradients" (degradation, an optimization problem); *(ii)* "ViT has no
  convolution" (the patch embedding is one); *(iii)* "image tokens = patches" (three
  different objects); *(iv)* "autoregressive means raster"; *(v)* "next-scale / masked =
  diffusion" (discrete codes, cross-entropy, no noise); *(vi)* "DALL-E is a diffusion
  model" (DALL-E 1 is AR; DALL-E 2 is diffusion); *(vii)* "a spectrogram is just an
  image"; *(viii)* "MoT is MoE". Flag on the spot; note recurrences in `progress.md`'s
  "Common misreadings" section.

- **Theorem vs engineering choice vs empirical result — say which, every time.** The ELBO
  bound, the GAN optimum `p_G = p_data` (in function space, unlimited capacity) and the
  AR chain rule for *any* order are theorems. Patch size, the choice of order, commitment
  β, temperature τ and the attention mask are engineering. "ViT beats ResNet," every FID
  in the course, MoT's FLOP ratios, Transfusion's ⅓, and BAGEL's emergence story are
  empirical, often from a single lab. The frontier phase flags this explicitly; do the
  same everywhere.

- **Pin every phase to Fashion-MNIST, with CPU-sized runs.** Keep training runs to a few
  minutes on CPU (subsets of 10k images, widths 16/32/64, an epoch or two). If a result
  doesn't show in so short a run (the degradation gap is the usual one), say why rather
  than pretending; that is still a lesson. Reuse the learner's own models: the Phase 1.5
  ResNet is the feature extractor for Fashion-FID, the Phase 6 tokenizer feeds Phase 7,
  the Phase 8 CLIP reranks the Phase 11 mini-DALL-E.

- **Honest Fashion-FID.** It is FID computed with the learner's own ResNet features
  instead of Inception: self-consistent across their models, **not** comparable to
  published numbers. Say so whenever it is reported.

- **Track-aware emphasis.** A Track A learner heading to `audio-diffusion-dit` needs
  Phases 1.4–1.6, 2, 3, 4.1/4.6, 5.1–5.5 and 9.3–9.5 solid; lean on the bridge table and
  the through-line clip. A Track B learner needs 5–8 and 10 solid; lean on the sequence
  view (masks, orders, token counts, MoE). Same core curriculum; adapt exercise depth
  (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 11.2), no GPU required.** Default is **CPU**: the
  whole mini-DALL-E (VQ tokenizer + raster AR + tiny CLIP reranker) fits in CPU minutes
  at 28 × 28. Colab GPU (tier b: next-scale and MaskGIT orders compared, or the
  Transfusion toy) and local GPU (tier c: the spectrogram bridge at scale, or a small
  pretrained open model) are upgrades, never prerequisites. Mirror room-acoustics' a/b/c.
  **Fail fast:** if a model download or import fails, surface the real error; don't swap
  models.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner
produced themselves, kept as reference and as motivation if they stall mid-course.

- One image per class plotted, hard pairs named (Phase 0.2).
- Plain CNN vs ResNet training curves and a confusion matrix (Phase 1.5) — the model kept
  for Fashion-FID.
- U-Net denoiser with and without skips (Phase 2.4).
- 2-D AE/VAE latent scatter, samples, and a sneaker→boot interpolation (Phase 3).
- DCGAN samples, a mode-collapse sighting, and a Fashion-FID (Phase 4).
- A tiny ViT vs the CNN at equal CPU budget, plus one attention map (Phase 5.4).
- The through-line clip's mel spectrogram patchified: 104 / 252 tokens (Phase 5.5).
- The 7 × 7 VQ tokenizer, its codebook-usage histogram, and a hand-edited code (Phase 6.2).
- The same grid generated raster / masked / next-scale, with step counts and the
  hand-drawn 88 × 88 mask (Phase 7).
- A tiny CLIP and its zero-shot accuracy on held-out prompts (Phase 8.3).
- The Transfusion attention mask for `<bos> a sneaker <boi> p₁ … p₄₉ <eoi>` (Phase 10.3).
- The tokenizer × order map with every system placed (Phase 11.1 — the keystone artifact).
- The capstone mini-DALL-E report (Phase 11.2).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or a different dataset
used, edit `syllabus.md` (and `the-image-as-sequence.md` / this file / `lesson.md` if the
change is structural). All are versioned content; commit when complete. **Phase 12 is a
living frontier**: when a new tokenizer, order or unified model lands, add it to Phase 12
and its "Frontier sources" list (precise citations; flag empirical claims), keep the
keystone's bridge table current when a vision idea reaches audio, and update the
"last revised" date. Suggest that durable additions be ingested into the music423-2023
wikis.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring symbols — `[B, C, H, W]`, `P`
  (patch size), `N = (H/P)(W/P)` (token count), `D` (embedding width), `K` (codebook
  size), `z_e`, `e_k`, `sg[·]` (stop-gradient), `p(x) = Π p(xᵢ | x_<i)`, τ (CLIP
  temperature) — get named the first time they appear. Unicode and CS-style identifiers
  in chat; LaTeX in the lesson logs is fine.
- Concrete > abstract; **seen > symbolic** (and **heard**, on the audio bridge). A grid of
  generated samples beats an architecture diagram beats an equation.
- Honest about theorem vs engineering choice vs empirical result (see above).
- One sentence of history when it explains a design: AlexNet (2012) cashed out GPUs +
  ReLU + data; ResNet (2015) made depth free; U-Net (2015) gave dense prediction a
  pyramid with skips; the VAE (2013) and GAN (2014) were the two one-shot generators;
  StyleGAN (2018) put style at each scale; ViT (2020) turned the grid into a sequence;
  VQ-VAE (2017) and VQGAN (2021) made images discrete; DALL-E (2021) read text and image
  codes as one sequence; CLIP (2021) aligned the two; LDM (2021) and the DiT (2022) moved
  diffusion into a latent and onto a Transformer; VAR (2024) changed the order to scales;
  Chameleon, Transfusion, MoT and BAGEL (2024–25) put every modality into one backbone.
