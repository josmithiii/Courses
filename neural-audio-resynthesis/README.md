# Neural Audio Resynthesis
*Capstone of the [AI Music & Audio](../curricula/ai-music-audio.md) thread — creating and editing audio with neural methods.*

Turn a static recording into a **steerable object**: encode it to a learned latent, steer
within that latent, decode a coherent variation. This course *surveys* the field
(parametric/DDSP → codec-LM → continuous-VAE/DiT → resynthesis-as-editing), then *drills*
the load-bearing survivors into the **encode → steer → decode** loop and asks what it
takes to steer it.

**Keystone:** the resynthesis loop + the control problem — see
[`the-resynthesis-loop.md`](the-resynthesis-loop.md). A learned latent is *expressive but
illegible*; the whole game is winning back legible control.

**Prerequisites:** none required — **plunge-in friendly**. Strongly recommended: the
AI Music & Audio core ([`audio-codecs`](../audio-codecs/), [`audio-diffusion-dit`](../audio-diffusion-dit/))
and the encode/steer/decode feeders ([`audio-ssl-representations`](../audio-ssl-representations/),
[`disentanglement`](../disentanglement/), [`flow-matching`](../flow-matching/)) — the course
gives 1-page recall-primers and links back.

**Format:** ~1 hr/day, ~20–25 sessions; tiered a/b/c capstone (RAVE on CPU, no GPU for tier a).

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take neural-audio-resynthesis` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
