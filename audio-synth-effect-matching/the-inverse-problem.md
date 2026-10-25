# The Inverse Problem — This Course's Keystone

Room-acoustics has the Schroeder frequency; audio-codecs has the fork. **This course
has the inverse problem: many parameters, one sound.** A synthesizer or effect is a
*forward* map from parameters to audio. Sound matching runs it *backwards* — and the
backward direction is not a function. Read this in Phase 0.1, then return to it in
**Phase 1.4** (where you *see* the many-to-one valleys on a 2-D loss surface),
**Phase 4** (where the loss decides what "the same sound" means), **Phase 6** (where
the field stops pretending there is one answer), and **Phase 8.1** (where you recite
the whole map from memory).

Every term in **bold** is earned somewhere in the syllabus; the phase that earns it is
noted in brackets.

---

## The problem, in one line

> Given a **synthesizer** `g` with **parameters** `θ` and a **target sound** `x`, find
> `θ* = argmin_θ L(g(θ), x)` — the parameters whose rendering is closest to the target
> under some **loss** `L` [Phase 1.1].

Three things make this hard, and each one is a phase of the course:

1. **The map is many-to-one** [Phase 1.4]. Different `θ` render to the same (or
   perceptually identical) audio: swap two oscillators, trade filter cutoff against
   oscillator brightness, trade decay rate against release time. So `θ*` is not a point
   but a *set* — often a curved valley in parameter space. This is
   **non-identifiability** (the problem is **ill-posed**).
2. **Perception is not parameter distance** [Phase 4]. Two parameter vectors a tiny
   Euclidean distance apart can sound wildly different (a cutoff crossing a harmonic),
   and two far apart can sound the same (point 1). So **parameter loss** `‖θ̂ − θ‖`
   and **audio loss** `L(g(θ̂), x)` disagree, and only the second one is what a listener
   hears.
3. **Most synthesizers are not differentiable** [Phase 5]. Square waves, categorical
   waveform switches, stateful effects — no gradient flows back from the audio to `θ`.
   Everything from Phase 3 onward is a different way around this wall.

## The estimation loop

```
                       ┌──────────────────────────────────────────────────────┐
                       │                  forward model  g                     │
   parameters  θ ─────▶│  oscillators → filters → envelopes → effects → audio  │─────▶  g(θ)
                       └──────────────────────────────────────────────────────┘           │
        ▲                                                                                 │
        │                          loss  L( g(θ) , x )   ◀───────────── target  x         │
        │                                   │                                              │
        │     ┌─────────────────────────────┴──────────────────────────────┐              │
        │     │  how the loss reaches θ:                                    │              │
        └─────┤   (a) a network predicts θ from x directly  [Phase 3]       │◀─────────────┘
              │   (b) gradients through a differentiable g  [Phase 5]       │
              │   (c) a proxy / stochastic gradient / RL     [Phases 3, 6]  │
              │   (d) a generative model samples θ ~ p(θ|x)  [Phase 6]      │
              │   (e) derivative-free search / retrieval     [Phases 2, 6.7]│
              └────────────────────────────────────────────────────────────┘
```

The loop has only three boxes — `g`, `L`, and *the route by which `L` reaches `θ`* —
and every paper in the collection is a choice for one of the three. Hold that picture
and the 64-paper reading list (41 core + the DAFx26 papers and plate-reverb challenge
entries) becomes a 3-by-N table.

## The two-parameter toy that shows everything [Phase 1.3–1.4]

The course pins the whole problem to a synthesizer with **two knobs**: an exponential
**decay rate** and a **lowpass cutoff** applied to a plucked-string excitation (the same
shape as the "decay rate and wah pedal angle" example in JOS's Neural Spectral Modeling
Template). Two knobs means the loss `L(g(θ), x)` is a **surface** you can plot as an
image. On that image you will see, with your own eyes:

- a **valley, not a point** — a ridge of `(decay, cutoff)` pairs the loss cannot
  distinguish, because a faster decay and a lower cutoff both make the note darker
  (point 1 above);
- the valley **move** when `L` changes from waveform MSE to log-mel to multi-scale
  STFT (point 2 above);
- a **gradient** you can follow only when `g` is written in `torch` (point 3 above).

Everything after Phase 1 is the same three facts at higher dimension.

## The method map [Phases 3–7]

| Route from `L` to `θ` | What it needs | Cross-domain? | Representative papers |
|---|---|---|---|
| **Black-box supervised** — a CNN/AST predicts `θ` from a spectrogram; loss in parameter space | (θ, audio) pairs rendered from the synth | weak (trained in-domain) | Barkan & Tsiris; InverSynth; Sound2Synth; Bruford (AST) |
| **Genetic / derivative-free search** — render, score, mutate (GA, CMA-ES, DE, PSO) | only the synth and a loss | yes, but thousands of renders per target — cheap when `g` is a fast GPU simulator in few dimensions | Shier thesis; Masuda quality-diversity; DAFx26 challenge CMA-ES (Park, Yi et al.) and DE (Lee et al.) |
| **White-box differentiation** — differentiate the synth's *actual code*, discontinuities included (A-delta) | source code | yes; no training at all | Yang et al. 2023 (ISMIR + FM) |
| **DDSP-differentiable** — reimplement `g` in torch, backprop an audio loss | a reimplementation | yes (fine-tune on real sounds) | Masuda & Saito 2021/2023; DiffMoog; PNP (Han); differentiable Karplus–Strong (Tablas de Paula 2026); differentiable modal plate (challenge 77); wedge-constrained FM (Tabata 2026) |
| **Neural proxy / stochastic gradient** — approximate the gradient of a black box | (θ, audio) pairs or perturbation budget | possible | DeepAFx (SPSA); Combes neural proxies; Peladeau hybrid |
| **Generative / distributional** — model `p(θ | x)`, sample many valid `θ` | (θ, audio) pairs | possible | FlowSynth; preset-VAE; Hayes equivariant flow; Peladeau distributions; simulation-based inference (challenge 84) |
| **Retrieval in a shared embedding** — embed presets and sounds jointly, look up the nearest preset | a preset gallery + renders | possible; answer limited to the gallery | SynAPSE / DX7-GNN (Braun & Finkelstein 2026) |
| **Reinforcement learning** — iterative knob-turning, reward = similarity | a reward, no labels, no gradients | yes | SynthRL |
| **Hybrid / model-based** — analytic inversion once `θ` is known; neural estimate feeds the inversion | a known DSP structure | n/a | Gorlow & Reiss DRC; Sun et al. 2024; Wright grey-box; Thompson & Heilemann 2026 (fit to measured gain CV) |
| **Hybrid / learned initialiser + search polish** — a network's guess, refined by PSO, CMA-ES or gradient descent through `g` | training pairs *and* a callable `g` | as good as the polish | DAFx26 challenge winner (Marttila et al., transformer/flow + PSO); band-count + DDSP refinement (Lu & Reiss) |

The rows are not competitors so much as *answers to different constraints*: do you
have the code? can you render a billion examples? must it match a real recording?
do you need one answer or the whole valley?

---

## The misreadings this course exists to kill

These are the conflations curated out of the `synth-effect-matching` wiki (several
were corrections made during that curation). The tutor flags each on the spot and logs
recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "Parameter MSE measures how good the match sounds." | No. The parameter→sound map is **many-to-one** and perception is nonlinear in `θ`. Peladeau & Peeters 2024: training on a log-mel *audio* loss beats parameter MSE for audio fidelity even when the latter wins on parameter numbers. Accurate `θ̂` does not imply accurate `g(θ̂)`. | Phase 1.4, 4.1 |
| "There is one right answer `θ*`." | No. Non-identifiability means a **set** (a valley, or discrete symmetric copies under oscillator permutation). Hayes 2025 shows point regression degrades even with permutation-invariant losses; the principled object is a **distribution** `p(θ | x)`. Sun 2024 finds DRC profile *classification* beats parameter *regression* for the same reason. | Phase 1.4, 6.3–6.4 |
| "You need a differentiable synthesizer to do sound matching." | No. White-box differentiation of existing code (Yang), neural proxies (Combes), stochastic gradients through black boxes (DeepAFx), RL (SynthRL) and plain genetic search all work without a DDSP reimplementation. DDSP is *one* route, with the best gradients. | Phase 3, 5, 6 |
| "A model that is accurate on synth-rendered data will match real recordings." | No. That is the **in-domain vs cross-domain** gap. Masuda & Saito's whole contribution is *fine-tuning with an audio loss on out-of-domain real sounds*; SynthRL's is a reward that needs no labels. | Phase 3.4, 5.1 |
| "Multi-scale spectral loss is the universal best loss." | No. Salimi et al. 2025 (4 losses × 4 synths × 300 trials, with listening tests): performance is **synthesizer-dependent**; no universal winner; parameter error, spectral distance and listening scores agree only moderately. MR-STFT is also famously non-convex in pitch — hence spectral optimal transport. | Phase 4.5 |
| "PNP is a perceptual loss." | Not quite. **PNP linearizes** the perceptual map `Φ∘g` around each training point and precomputes the Jacobian, giving a quadratic loss `(θ̂−θ)ᵀ M (θ̂−θ)` that runs at parameter-loss speed (~100×) while *weighting parameter error by perceptual sensitivity*. It is a metric on `θ`, not on audio. | Phase 4.3 |
| "Effect inversion and synth matching are different fields." | Same loop, different `g`. A compressor is a forward model with seven knobs; Gorlow inverts it given `θ`, Sun estimates `θ` then inverts, Peladeau estimates `θ` blind, Wright *fits* the model to hardware. | Phase 7 |
| "Framewise parameter prediction that matches well is the goal." | Matching well with opaque per-frame curves is not a *preset* a musician can use. Modulation discovery trades a little accuracy for LFO/envelope structure — **interpretability is a design axis**, not a nicety. | Phase 7.6 |
| "A smoother loss (spectral OT, log-magnitude) makes the landscape safe to descend." | Not globally. Tabata et al. 2026: the Wasserstein loss for FM has non-differentiable **ridges at rational frequency ratios** (sideband folding and ordering swaps). Tablas de Paula et al. 2026: SOT is blind to `f_0` in a resonant Karplus–Strong decoder, and **no** spectral loss supervises onset time. Park, Yi et al. 2026: log compression in MR-STFT collapses plate-reverb recovery. Read the ridges as well as the valleys. | Phase 4.6, 5.7 |
| "Matching the output waveform is the right objective for an effect model." | Depends on the goal. For device emulation, Thompson & Heilemann 2026 show waveform `L1` and MSTE give near-identical scores to compressors whose **gain trajectories** differ by 86 %; supervise the quantity that defines the effect. For a *perceptual* match, Peladeau 2024 still says optimise audio. Both reject sample-wise waveform `L1`. | Phase 7.7 |
| "Search is too slow — learn an estimator instead." | Only when `g` is slow or `θ` is high-dimensional. In the DAFx26 plate-reverb challenge a training-free CMA-ES reached NMSE ≈ 2e-11, and the winner was a *network initialiser polished by search* (≈ 2e-13). Learned and search routes compose. | Phase 2.2, 9.1 |
