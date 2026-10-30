# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Which track brought them here? _(Track A — AI Music & Audio / Track B — LLMs & Sequence Models / both / neither, just curious)_
- Route: _(full course / Track A route / Track B route — see syllabus; none is a gate)_
- Finished `ai-foundations/`? _(yes / partly — which phases / no — use the Phase 0.3 recall-primer and backfill as needed)_
- CNN comfort (`Conv2d`, pooling, a trained MNIST classifier): _(new / comfortable / strong)_
- Transformer comfort (attention, masks, the block): _(new / comfortable / strong)_
- Generative-model background (VAE, GAN, diffusion): _(intuition only / some / strong)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- DSP background (filters, sampling and aliasing, filter banks, VQ): _(none / some / expert — use the DSP lens heavily)_
- Taken `ai-miracle-decade-plus`, `disentanglement`, `audio-codecs`, `audio-diffusion-dit`, `ai-sequence-models`? _(list — affects which cross-references land)_
- Why they're here / goal: _(understand ViT/DiT before the audio DiT course / understand multimodal LLMs / build a small generator / research)_
- Lean: _(hands-on — build each toy on Fashion-MNIST / conceptual — the tokenizer × order map and the papers)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Can play audio (for the spectrogram bridge)? _(yes / no)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **picture-first**, every term defined on first use, every idea
  pinned to the same Fashion-MNIST grid (and, where it has an audio twin, to the
  through-line clip's mel spectrogram)

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-image-as-sequence.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` + `torchvision` importable (version noted)
- [ ] `matplotlib` importable; can show or save a figure
- [ ] Fashion-MNIST downloaded to `<data root>/ai-vision-and-multimodal/data/` (60,000 / 10,000, `[1, 28, 28]`) — fail fast if not
- [ ] A scratch `work/` directory (scripts, checkpoints) under the data dir, or a notebook, used during sessions
- [ ] (audio bridge) `torchaudio` or `librosa` importable; the through-line clip resolves at `assets/ai-music-audio/through-line.wav`
- [ ] (audio bridge) Can play audio — `IPython.display.Audio` or write+play a WAV
- [ ] `the-image-as-sequence.md` read (the keystone — tokenizer × order)
- [ ] (capstone tier b/c) Colab or local GPU confirmed

## The grid & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Fashion-MNIST: 60,000 train / 10,000 test, 28 × 28 × 1, 10 classes
  (0 T-shirt/top, 1 Trouser, 2 Pullover, 3 Dress, 4 Coat, 5 Sandal, 6 Shirt, 7 Sneaker, 8 Bag, 9 Ankle boot).
- Learner's own accuracies (CPU budget noted): MLP _(…)_, CNN _(…)_, ResNet _(…)_, ViT _(…)_
- ViT patchify: `P = 4` → 49 tokens of dim 16; `P = 7` → 16 tokens of dim 49.
- VQ grid: 7 × 7 = 49 codes; `K` = _(e.g. 128)_; bits per image _(e.g. 343 vs 6,272 raw)_.
- Steps for the 7 × 7 grid: raster 49; masked ~8; next-scale (1,2,3,5,7) = 5 steps / 88 tokens.
- Through-line clip mel: 128 bands × 221 frames (10 ms hop); 16 × 16 patches → 104 tokens (AST stride 10 → 252); codec at 75 Hz → 165 frames.
- Fashion-FID reference: _(real-vs-real split value, so later numbers have a floor)_

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has built and looked at themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## The tokenizer × order map (filled in as systems are met)
> One line per system: *name — what a cell is — what order produces it — phase met.*

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-image-as-sequence.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "ResNets fixed vanishing gradients" — they fixed **degradation**, an optimization difficulty
- "U-Net skips are ResNet skips" — concatenate across the hourglass vs add within a block
- "VAE blur is a bug" — the MSE-optimal output is the mean of plausible images
- "GANs are dead" — as a **loss** they're everywhere (VQGAN, HiFi-GAN, EnCodec)
- "ViT has no convolution" — the patch embedding is a strided conv
- "Transformers beat CNNs on images" — empirical and data-dependent
- "image tokens = patches" — patch embedding vs discrete code vs latent patch
- "autoregressive means raster" — AR is exact for any order
- "next-scale / masked prediction is diffusion" — discrete codes, cross-entropy, no noise
- "CLIP generates images" — an aligned pair of encoders
- "DALL-E is a diffusion model" — DALL-E 1 is discrete AR; DALL-E 2 is diffusion
- "a spectrogram is just an image" — axes mean different things; phase is gone
- "unified = one tokenizer" — one backbone and sequence, different representations and losses
- "MoT is MoE" — deterministic modality routing vs a learned router
- "BAGEL proved world models emerge" — one lab's claim, partial evidence
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 11.2) — tiered, no GPU required
> Picked partway through Phase 7 so it can shape the last few lessons.

- _(a) **CPU** — a mini-DALL-E on Fashion-MNIST: 7 × 7 VQ tokenizer + tiny raster-AR Transformer over [caption; codes] + tiny CLIP reranker; Fashion-FID, classifier accuracy on samples, one-page tokenizer × order report_
- _(b) **Colab GPU** — tier a, plus next-scale and MaskGIT orders compared at matched compute, or the Transfusion toy (one Transformer that captions and generates)_
- _(c) **Local GPU** — tier a or b, plus the spectrogram bridge at scale (tokenize and generate mel patches of piano, vocode, listen), or a small pretrained open model's token grid and order inspected_
- Choice: _(not yet)_
