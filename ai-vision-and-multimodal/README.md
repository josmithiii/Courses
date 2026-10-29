# AI Vision & Multimodal
*Enrichment for both AI research tracks of [Music 423](../curricula/music423.md):
[LLMs & Sequence Models](../curricula/ai-llms-and-sequence-models.md) and
[AI Music & Audio](../curricula/ai-music-audio.md).*

The vision branches of the same backbone: CNNs (AlexNet → **ResNet** → **U-Net**) → VAEs
and GANs (StyleGAN, alias-free generation) → **ViT** → image tokenizers (VQ-VAE, VQGAN)
→ generation order (raster, MaskGIT, **next-scale VAR**, continuous AR) → **CLIP** →
DALL-E and the diffusion turn (LDM, DiT) → unified multimodal models (Chameleon →
**Transfusion** → MoT → BAGEL, world-model claims) → a living frontier. Built on
**Fashion-MNIST**, one dataset classified, autoencoded, GAN'd, patchified, tokenized,
generated three ways and aligned with text, ending in a mini-DALL-E; plus the Track A
piano clip's mel spectrogram as the bridge to audio.

**Keystone:** the image as a sequence: every system is a choice of **tokenizer** (what
a cell is) and **generation order** (how cells are produced). See
[`the-image-as-sequence.md`](the-image-as-sequence.md).

**Prerequisites:** none required (plunge-in friendly). Strongly recommended:
[`ai-foundations`](../ai-foundations/) Phases 2–4 and 6. Pairs with
[`ai-miracle-decade-plus`](../ai-miracle-decade-plus/) (the same papers as a reading
tour) and hands off to [`audio-diffusion-dit`](../audio-diffusion-dit/) and
[`disentanglement`](../disentanglement/).

**Format:** ~1 hr/day, ~22–26 sessions (Track A and Track B short routes ~10–16);
tiered a/b/c capstone (mini-DALL-E on CPU, no GPU for tier a); living frontier phase.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take ai-vision-and-multimodal` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
