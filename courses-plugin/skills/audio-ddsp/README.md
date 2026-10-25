# Differentiable DSP (DDSP)
*Course 1 of the [Differentiable & Physical Audio DSP](../curricula/audio-differentiable-dsp.md) curriculum.*

Make the classical audio building blocks you already know — oscillators, filters, noise
generators, reverbs, compressors — **differentiable**, so their parameters can be learned
from audio by gradient descent. From "what does autograd do to a biquad?" through the
DDSP harmonic+noise synthesizer (Engel et al. 2020), differentiable IIR / FIR / all-pass
filters and effects, grey-box compressors and phasers, to FM, piano, MIDI-DDSP and
modular synths. Pinned to one plucked-string note, *heard* at every stage.

**Keystone:** the spectral loss and the gradient through a DSP block — see
[`the-differentiable-block.md`](the-differentiable-block.md).

**Prerequisites:** JOS's [*Introduction to Digital Filters*](https://ccrma.stanford.edu/~jos/filters/)
and the STFT / sinusoidal-modeling parts of [*Spectral Audio Signal Processing*](https://ccrma.stanford.edu/~jos/sasp/)
(or equivalent DSP); [`ai-foundations`](../ai-foundations/) through Phase 2 (PyTorch,
autograd, the training loop). Neural nets appear only as parameter predictors.

**Format:** ~1 hr/day, ~20–25 sessions; tiered CPU / Colab / GPU capstone.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-ddsp` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
