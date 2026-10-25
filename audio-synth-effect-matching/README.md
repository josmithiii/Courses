# Synthesizer & Effect Parameter Estimation
*Course 2 of the [Differentiable & Physical Audio DSP](../curricula/audio-differentiable-dsp.md) curriculum.*

Sound matching as an inverse problem: from a target sound to the synthesizer or effect
parameters that reproduce it. Handcrafted features and genetic search → supervised CNN /
AST parameter prediction and the in-domain gap → the loss question (parameter vs spectral
vs JTFS vs **PNP**; no universal best) → differentiable synth matching (Masuda & Saito,
DiffMoog, white-box differentiation) → generative and distributional estimation
(FlowSynth, equivariant flow matching, parameter distributions, neural proxies, RL) →
effect inversion (DeepAFx, blind estimation, the **DRC** forward model inverted
analytically and neurally, grey-box, FDN reverb, modulation discovery, gain-trajectory
supervision, effect graphs). DAFx26 (2026) adds loss-landscape *ridges* (FM), a
differentiable Karplus–Strong for the course's own plucked note, retrieval in a shared
audio–preset embedding, and the plate-reverb parameter-estimation challenge as a
head-to-head of every method family; the 2026 wave adds joint-distribution flow
matching, renderer-free embedding search, GRPO-trained generative inverters, and
prediction + search for effect chains. Pinned to one
plucked-string note whose parameters the learner recovers three ways, *rendered and
heard* at every step.

**Keystone:** many parameters, one sound — see
[`the-inverse-problem.md`](the-inverse-problem.md).

**Prerequisites:** JOS's *Introduction to Digital Filters* and *Spectral Audio Signal
Processing*; [`ai-foundations`](../ai-foundations/) through Phase 2 (PyTorch, autograd,
the training loop). `audio-ddsp` (course 1) recommended, not required.

**Format:** ~1 hr/day, ~25–30 sessions; tiered CPU / Colab / GPU capstone; living
frontier phase.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-synth-effect-matching` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
