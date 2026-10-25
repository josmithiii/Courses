# Physics-Informed Audio Modeling
*Course 3 (final) of the [Differentiable & Physical Audio DSP](../curricula/audio-differentiable-dsp.md) curriculum.*

Physics plus learning, for one plucked note: **modal synthesis as a learnable model**
(eigenmodes → a bank of 2-pole resonators → fit its frequencies, decays, and amplitudes
by gradient descent), **physics-informed neural networks** (a network that *is* the
solution of the damped stiff-string equation, trained on the PDE residual), and **hybrid
physical/neural models** (a waveguide or modal core with a learned excitation or
residual). The same note is modeled all three ways and compared by ear and by spectral
error, so the learner can answer the course's one question: *where does the network go?*

**Keystone:** the physical prior as inductive bias — what the equations give you for
free, what the network must learn — see [`the-physical-prior.md`](the-physical-prior.md).

**Prerequisites:** JOS's *Introduction to Digital Filters* and the waveguide / modal
chapters of *Physical Audio Signal Processing* (ccrma.stanford.edu/~jos/); PyTorch +
autograd (`ai-foundations` through Phase 2). [`audio-ddsp`](../audio-ddsp/) recommended.
ODE/PDE comfort helps; the 1-D wave equation is derived briskly here.

**Format:** ~1 hr/day, ~18–22 sessions; tiered CPU / Colab / GPU capstone.

**Honesty note:** the physics-informed-network literature *for audio* is thin and
fast-moving; the course says so and leans on PASP for derivations.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-physics-informed` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
