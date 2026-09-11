# Differentiable & Physical Audio DSP

**Status:** 🟢 Complete — all three courses authored (2026-09-11), sharing one plucked-string
through-line note. Track C of the [Music 423 meta-curriculum](music423.md).

## Goal

For the signal-processing person who wants neural methods *inside* the DSP rather than
replacing it: make classical audio building blocks (oscillators, filters, reverbs,
compressors, physical models) **differentiable**, so their parameters can be learned
from audio; **invert** synthesizers and effects (sound → the parameters that made it);
and combine **physics** with learned components (modal synthesis, physics-informed
networks, hybrid physical/neural models). This is the lineage where the DSP books do the
heavy lifting and the neural part is a thin, legible layer on top — the *parametric /
legible-but-bounded* pole that Track A's capstone contrasts with learned latents.

**Who it's for.** Anyone comfortable with the material in *Introduction to Digital
Filters* and *Spectral Audio Signal Processing* who wants to read the DDSP, synth-matching,
and physics-informed papers and build small differentiable models in PyTorch. Also the
best entry for acousticians and instrument builders.

## Prerequisites

- **Audio DSP** — JOS's online books, which are self-paced courses in their own right:
  [*Mathematics of the DFT*](https://ccrma.stanford.edu/~jos/mdft/) →
  [*Introduction to Digital Filters*](https://ccrma.stanford.edu/~jos/filters/) →
  [*Spectral Audio Signal Processing*](https://ccrma.stanford.edu/~jos/sasp/) →
  [*Physical Audio Signal Processing*](https://ccrma.stanford.edu/~jos/pasp/).
  The first two are required background for course 1; *SASP* for course 1's spectral
  losses and course 2; *PASP* for course 3. Read as far as you need and return.
- **Machine learning** — [`../ai-foundations/`](../ai-foundations/) through Phase 2
  (PyTorch, autograd, the training loop). CNNs and Transformers appear only as encoders
  here and are introduced when needed.

## Ordered course list

| # | Course | Status | Why here |
|---|--------|--------|----------|
| 1 | [`../audio-ddsp/`](../audio-ddsp/) | 🟢 Active | Differentiable DSP: harmonic-plus-noise synthesis with learned control (DDSP), differentiable IIR filters and biquads, differentiable reverb and mixing consoles, MIDI-DDSP. Keystone = **the spectral loss and the gradient through a DSP block** — what makes a filter "differentiable" and what it costs. Pinned to one instrument note resynthesized by a learned harmonic+noise model. |
| 2 | [`../audio-synth-effect-matching/`](../audio-synth-effect-matching/) | 🟢 Active | Inverse problems: from a sound to the synthesizer or effect parameters that produce it — classical estimation (bowed-string, Bayesian) → learned reverse controls (InverSynth, DeepSynthPE) → DDSP-based matching → effect inversion (dynamic range compression, model-based and neural). Keystone = **many parameters, one sound** (non-identifiability) and how differentiable synthesis sidesteps it. Pinned to one synth patch recovered from audio. |
| 3 | [`../audio-physics-informed/`](../audio-physics-informed/) | 🟢 Active | Physics + learning: modal synthesis as a learnable model, physics-informed neural networks (PINNs) for wave and string equations, and hybrid physical/neural instrument models. Keystone = **the physical prior as inductive bias** — what the equations give you for free and what the network must learn. Pinned to one struck/plucked object modeled three ways (modes, PINN, hybrid). |

## Enrichment / co-requisites (parallel, not gates)

- [`../neural-audio-resynthesis/`](../neural-audio-resynthesis/) — Track A's capstone
  uses DDSP as the *legible* contrast to learned resynthesis; taking it after course 1
  here shows both poles.
- [`../audio-codecs/`](../audio-codecs/) — its Phase 1 is the brisk ML-first version of
  the DSP this track assumes; useful as a check on what ML people consider "enough DSP".
- [`../room-acoustics/`](../room-acoustics/) — not part of the collection, but the
  natural acoustics companion for course 3.

## Through-line

One **instrument recording** (a single plucked or struck note) carried through all
three courses: course 1 resynthesizes it with a learned harmonic+noise model; course 2
recovers synthesizer and effect parameters for it; course 3 models the physical object
that produced it. The note and its license live in
[`assets/audio-differentiable-dsp/`](assets/audio-differentiable-dsp/) (spec, status, and a
labelled synthetic placeholder generator until a real recording is chosen).

## Source of truth

Topic directories in
[`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023):

- [`ddsp/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ddsp) — course 1.
- [`synth-effect-matching/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/synth-effect-matching)
  (the largest wiki in the repo) and
  [`DRC/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/DRC) — course 2.
- [`modal-synthesis/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/modal-synthesis),
  [`pinn/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/pinn) — course 3.
- [`ai-misc/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-misc) —
  spectrogram inversion and other one-offs that fit course 1.
- JOS's books (above) for every derivation the courses cite rather than repeat.
