# Audio Codecs
*Course 1 of the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum.*

From raw waveforms to the tokens and latents every modern audio generator consumes:
brisk DSP (sampling, STFT, mel) → autoencoders → VQ-VAE → residual VQ →
SoundStream / EnCodec / DAC → **the discrete-token vs continuous-VAE fork** →
semantic vs acoustic tokens + evaluation. Pinned to one ~2 s solo-piano clip, *heard*
at every stage.

**Keystone:** the discrete-token vs continuous-VAE fork — see [`the-fork.md`](the-fork.md).

**Prerequisites:** [`ai-foundations`](../ai-foundations/) (or equivalent ML background).
No DSP background needed — the course builds the audio intuition briskly.

**Format:** ~1 hr/day, ~20 sessions; tiered CPU / Colab / GPU capstone.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-codecs` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
