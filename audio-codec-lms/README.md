# Audio Codec LMs
*Course 2 of the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum — the discrete-token branch.*

Generate audio by *language-modeling* codec tokens: AR raw audio (WaveNet) → Jukebox →
AudioLM (**semantic + acoustic** hierarchy) → MusicLM (MuLan text) → MusicGen
(**single-stage codebook patterns**) → masked / NAR (VampNet, MAGNeT) →
VALL-E / **MIDI-VALLE**. Continue, infill, and condition the shared piano clip.

**Keystone:** the RVQ token grid — see [`the-token-grid.md`](the-token-grid.md).

**Prerequisites:** [`audio-codecs`](../audio-codecs/) (this is the discrete branch of its fork).

**Format:** ~1 hr/day, ~25 sessions; tiered MusicGen capstone.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-codec-lms` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
