# Audio Diffusion & the DiT
*Course 3 (final) of the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum — the continuous-VAE branch.*

Generate audio by *denoising a continuous VAE latent* with a Diffusion Transformer:
latent diffusion (AudioLDM → Tango → AudioLDM 2) → **the DiT** (patchify + **adaLN-Zero**) →
Stable Audio (continuous-VAE + timing — *still a U-Net*) → **the U-Net→DiT swap**
(Long-Form Latent Diffusion / Stable Audio Open) → rectified-flow MM-DiT (FluxMusic) →
DiffRhythm / ACE-Step. *Denoise* the shared piano clip.

**Keystone:** the latent canvas — see [`the-latent-canvas.md`](the-latent-canvas.md).
Ships a self-contained [`rectified-flow-primer.md`](rectified-flow-primer.md).

**Prerequisites:** [`audio-codecs`](../audio-codecs/) + [`audio-codec-lms`](../audio-codec-lms/);
[`flow-matching`](../flow-matching/) as enrichment.

**Format:** ~1 hr/day, ~25 sessions; tiered Stable-Audio-Open / DiffRhythm capstone.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-diffusion-dit` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
