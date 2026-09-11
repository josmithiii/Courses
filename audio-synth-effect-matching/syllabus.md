# Synthesizer & Effect Parameter Estimation — Sound Matching as an Inverse Problem

**Learner profile:** Comfortable with the material in JOS's *Introduction to Digital
Filters* (`ccrma.stanford.edu/~jos/filters/`) and *Spectral Audio Signal Processing*
(`ccrma.stanford.edu/~jos/sasp/`): knows what a one-pole, a biquad, an STFT and a mel
spectrogram are and can read a transfer function. Has `ai-foundations/` through Phase 2
(PyTorch tensors, autograd, the training loop) — and ideally `audio-ddsp/` (course 1 of
this curriculum), though this course re-introduces what it needs. CNNs and Transformers
appear only as *encoders* and are introduced just-in-time. The learner is DSP-first: they
already know what a synthesizer *does*; what is new is running it **backwards** — from a
sound to the parameters that made it — and everything that goes wrong when you try.
~1 hour per day. One concept at a time. Every concept verified with a small exercise
before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**The keystone — read [`the-inverse-problem.md`](the-inverse-problem.md) in Phase 0.1.**
This course has one organizing idea, the analogue of audio-codecs' fork: **many
parameters, one sound.** The map from synthesizer parameters `θ` to audio `g(θ)` is
many-to-one, so its inverse is not a function — the answer is a *valley* (or a set of
symmetric copies) in parameter space, parameter distance is not perceptual distance, and
most synthesizers give you no gradient to descend anyway. Every method in the field —
supervised CNNs, genetic search, white-box differentiation, DDSP reimplementation,
neural proxies, generative flows, reinforcement learning — is a different response to
those three facts. We spend as long as it takes on Phases 1.4, 4 and 6.

**The qubit (worked example):** the curriculum's shared **single plucked-string note**
(`../curricula/assets/audio-differentiable-dsp/note.wav`, mono 44.1 kHz, ~1.5 s). Course 1
resynthesized it; this course **recovers the parameters that reproduce it** — three times,
at increasing difficulty: (1) a **two-knob toy synth** (exponential decay rate + lowpass
cutoff on a plucked excitation — the same shape as the "decay rate and wah pedal angle"
example in JOS's *Neural Spectral Modeling Template*), whose loss surface we can *plot as
an image*; (2) a **differentiable subtractive synth** (oscillators, resonant lowpass,
ADSR) matched with spectral loss; (3) **effects applied to the note** — a compressor and
a reverb — inverted from the wet signal. Same note, every method; the ear and the
residual spectrogram are the oracle.

**End state:** by the last lesson the learner can: write the inverse problem
`θ* = argmin L(g(θ), x)` and explain the three reasons it is hard; plot and *read* a 2-D
loss surface (valleys = non-identifiability); train a small CNN to predict parameters
from spectrograms and say why its in-domain accuracy will not transfer to real
recordings; state the difference between parameter loss, multi-scale spectral loss, JTFS
scattering and PNP, and when each is the right ruler; fine-tune a differentiable
synthesizer on the note with an audio loss and A/B the result; explain why point
estimation is the wrong object under symmetry and what a conditional generative model
returns instead; run the DRC forward model, invert it analytically given parameters,
and explain why *classification* of the compressor profile beats regression; and place
any 2024–2025 paper in the collection on the method map in `the-inverse-problem.md`.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture**, no notation yet: a synthesizer is a
  forward map from knobs to sound; sound matching runs it backwards; running it
  backwards is not a function. Read [`the-inverse-problem.md`](the-inverse-problem.md).
  Where this course sits in the `audio-differentiable-dsp` curriculum (course 2 of 3;
  the inverse of course 1's forward models; course 3 puts *physics* into `g`).
- **0.2** **Tools.** `torch` + `torchaudio` + `matplotlib` importable; load the
  through-line note, print its shape and sample rate, play it, plot the waveform and a
  log-magnitude spectrogram. (Optional: `IPython.display.Audio` in a notebook so renders
  are audible inline.) If the note file is missing, **stop and say so** — produce it
  with `../curricula/assets/audio-differentiable-dsp/make_note.py` or pick a short mono
  plucked/struck note; never silently substitute.
- **0.3** **Crash-start: what a synthesizer parameter is.** Continuous (cutoff in Hz,
  decay in s), discrete-ordinal (16 levels of a knob), categorical (saw / square /
  sine). Why the third kind will matter (no gradient). Look at the note's spectrogram
  and *guess* two parameters that made it — the whole course is making that guess
  rigorous.

## Phase 1 — The Inverse Problem, Stated (the keystone, part one)
- **1.1** **Forward model, target, loss.** `g : θ ↦ audio`; target `x`; loss
  `L(g(θ), x)`; the estimate `θ* = argmin_θ L`. Name every symbol; say what each is in
  plain English. The three difficulties (many-to-one, perception ≠ parameter distance,
  no gradient) — one sentence each, to be earned over the course.
- **1.2** **Analysis-by-synthesis is old.** The loop predates deep learning by decades
  (LPC, sinusoidal modeling, *SASP*'s spectral-modeling chapters are all "fit a model to
  a sound"). What is new is *learning the estimator* and *differentiating the model*.
- **1.3** **Build the two-knob toy synth.** Plucked excitation (a short noise burst, or
  the note's own first 5 ms) → exponential **decay** `a` → one-pole **lowpass** with
  cutoff `f_c`. Write it in `torch` (≈15 lines). Render a few `(a, f_c)` pairs and
  *listen* — darker vs faster-dying.
- **1.4** **See the valley.** Grid `(a, f_c)` on a 50×50 mesh, compute `L(g(θ), note)`
  with waveform MSE, and plot the surface as an image. **There is a valley, not a
  point**: a faster decay and a lower cutoff both darken the note, so the loss cannot
  tell them apart along a ridge. This *is* non-identifiability, in 2-D, on a screen.
  Re-plot with a log-mel loss and watch the valley *move*. (Keystone moment — spend as
  long as it takes.)
- **1.5** **Descend it.** `requires_grad` on `(a, f_c)`, Adam, 200 steps, from three
  random starts. Two starts land in the same valley at *different* points; one gets
  stuck. Play all three renders next to the note: they sound alike. Log the numbers in
  `progress.md`'s "numbers we reuse".

## Phase 2 — Before Deep Learning (2002–2016)
- **2.1** **Handcrafted features + regression.** Itoyama & Okuno (ICMC 2014): extract
  spectral descriptors, regress parameters linearly. Why it works for a few knobs and
  collapses for many (features are not invertible). Do it on the toy synth: regress
  `(a, f_c)` from spectral centroid + decay time — it works, which is the point.
- **2.2** **Genetic / derivative-free search.** Render, score with a spectral fitness,
  mutate, repeat — no gradient, any synth, thousands of renders per target. Where it
  still lives (Shier thesis, quality-diversity in Phase 5.3). Run 300 random-search
  renders on the toy synth and compare to Phase 1.5's gradient descent.
- **2.3** **Fitting physical models.** Su & Liang (2002) fit a recurrent plucked-string
  model; Sterling & Bocko (2010) fit an empirical bowed-string model. The parameters
  are *physical* (loss, stiffness, bow force) — a preview of course 3, and of the
  claim that a physical `g` makes the inverse problem *better posed*.

## Phase 3 — Supervised Parameter Prediction (2017–2024)
- **3.1** **The idea.** Render a large `(θ, g(θ))` dataset, train a network
  `f : spectrogram ↦ θ̂`, loss in *parameter* space. One forward pass at inference.
- **3.2** **Barkan & Tsiris (ICASSP 2019, preprint 2017) → InverSynth (2018).** Strided
  spectrogram CNNs beat handcrafted features; *classification* into 16 levels per
  parameter is easier to optimize than regression (a foreshadowing of Phase 6 —
  discrete targets tolerate many-to-one better); depth matters, width barely. Their
  reconstruction metric (STFT PCC) is an *audio* metric bolted onto a *parameter*-trained
  net — note the mismatch.
- **3.3** **Scaling the data and the encoder.** torchsynth / synth1B1 (Turian, Shier et
  al. 2021): a GPU modular synth rendering at 16 200× real time, a billion-sample
  corpus; Sound2Synth (2022) for a 155-parameter FM synth; Bruford et al. (DAFx 2024)
  swap the CNN for an **Audio Spectrogram Transformer**. The encoder is a commodity;
  the loss and the data domain are the problem.
- **3.4** **The in-domain / cross-domain gap.** Train on synth renders, test on a real
  recording: the note. Build it on the toy synth: render 5 000 `(a, f_c)` examples,
  train a 3-layer CNN on log-mel patches with parameter MSE, evaluate on held-out
  renders (good) and on the *real* note (worse — and the render is *audibly* off even
  when `θ̂` is "close"). This is misreading #1 and #4 of the keystone, measured.

## Phase 4 — Losses & Similarity (the keystone, part two)
- **4.1** **Parameter loss vs audio loss.** `‖θ̂ − θ‖²` is fast and needs labels; it
  weights every knob equally, but the ear does not. `L(Φ(g(θ̂)), Φ(x))` measures what
  is heard but needs a differentiable `g` (or a workaround). Peladeau & Peeters 2024:
  training on log-mel beats parameter MSE for *audio* fidelity even when parameter MSE
  wins on *parameter* numbers.
- **4.2** **Spectral losses.** Multi-scale STFT (L1 on log magnitudes at several window
  sizes — the DDSP standard), mel and MFCC distances, log-magnitude vs linear. Compute
  MR-STFT between the note and three toy-synth renders; rank them by ear first, then by
  loss — do they agree?
- **4.3** **Perceptual representations and PNP.** Joint time-frequency scattering (JTFS)
  captures spectrotemporal modulation but is expensive to backpropagate through. Han et
  al.'s **PNP loss** *linearizes* `Φ∘g` around each training point — precompute the
  Jacobian `J`, use `(θ̂−θ)ᵀ JᵀJ (θ̂−θ)` — so training runs at parameter-loss speed
  (~100× faster) with perceptual weighting. Compute `JᵀJ` for the toy synth at one point
  by finite differences and *look at it*: the ellipse's long axis is the valley of 1.4.
- **4.4** **Beyond microstructure.** Mesostructures (Vahidi, Han et al. 2023): spectral
  losses miss arpeggios and rhythm; differentiable scattering on GPU (Muradeli 2022)
  makes JTFS practical.
- **4.5** **No universal best loss.** Salimi et al. 2025: 4 losses × 4 synths × 300
  trials with listening tests — performance is synthesizer-dependent; parameter error,
  spectral distance and listening scores agree only moderately. Also: MR-STFT is
  non-convex in pitch (two sines a semitone apart have *zero* overlap), which is why
  Peladeau 2025 use **spectral optimal transport**. Kill misreading #5 here.

## Phase 5 — Differentiable Synth Matching (2021–2025)
- **5.1** **Masuda & Saito (ISMIR 2021).** Reimplement a subtractive synth in PyTorch
  (saw/square via additive harmonics; the resonant lowpass as a harmonic-amplitude
  mask so no IIR is needed in the graph); **pre-train with parameter loss in-domain,
  fine-tune with spectral loss on out-of-domain real sounds.** The first method that
  closes Phase 3.4's gap. Build the same synth (≈60 lines), match the note, A/B.
- **5.2** **TASLP 2023 extension.** Add ADSR envelopes and a chorus; train with
  *combined* parameter + spectral loss throughout rather than switching. Why the
  combination matters for effect modules.
- **5.3** **Quality-diversity (Masuda & Saito 2023).** Instead of one match, evolve a
  *population* of perceptually distinct matches — the first hint that the answer is a
  set (bridge to Phase 6).
- **5.4** **DiffMoog (Uzrad, Barkan et al. 2024).** A full differentiable modular synth
  (FM/AM, LFOs, filters, envelopes) with a *signal-chain loss* aware of topology. The
  most complete DDSP research platform; also the tier-c capstone option.
- **5.5** **White-box differentiation (Yang et al., ISMIR 2023 + FM 2023).** Don't
  reimplement — differentiate the *actual* synth code, discontinuities included, by
  borrowing the **A-delta** method from differentiable rendering: each sample is an
  integral over a window, and the integral of a step has a gradient. Categorical
  parameters via continuous relaxation then rounding. No training data at all.
- **5.6** **Optimization pathologies.** Gradient clipping for DDSP (Han et al., EUSIPCO
  2025); IIR instability and the valley's flat floor. Revisit Phase 1.5's stuck start —
  now name why it stuck.

## Phase 6 — Generative, Distributional, and RL (the keystone, part three)
- **6.1** **Latent-space methods.** Flow Synthesizer (Esling, Masuda et al. 2020): a VAE
  over synth audio plus a normalizing flow to parameters — parameter inference,
  macro-controls and preset exploration in one model, and an explicit admission that the
  synth *cannot* make every sound. Preset-generation VAE (Le Vaillant et al. 2021).
- **6.2** **Why point estimates fail under symmetry.** Swap two oscillators and the
  audio is unchanged: `p(θ | x)` has several equal modes, and a regressor trained with
  MSE lands on their *mean* — a preset that sounds like none of them. Show it on a
  two-oscillator toy.
- **6.3** **Inversion as conditional density estimation (Hayes et al., ISMIR 2025).**
  Model `p(θ | x)` with **flow matching**; enforce (approximate, *relaxed*) permutation
  equivariance so the flow discovers the symmetries; evaluated on Surge XT, a production
  synth. Generative beats regression even with permutation-invariant losses. (Bridges to
  `flow-matching/` for the objective.)
- **6.4** **Distributions for effects too (Peladeau et al., DAFx 2025).** Normalizing
  flows + an entropy term return *diverse* valid parameter sets for a compressor rather
  than one point; spectral optimal transport as the audio loss.
- **6.5** **Neural proxies (Combes et al. 2025).** For a black-box commercial synth,
  learn `θ ↦ pretrained-embedding` and optimize through the *proxy*; Peladeau &
  Peeters' hybrid (estimate with a TCN proxy, render with the real DSP).
- **6.6** **Reinforcement learning (SynthRL, IJCAI 2025).** Matching as an MDP: state =
  audio features, action = knob adjustments, reward = spectral similarity; no labels, no
  gradients through `g`, cross-domain by construction; slower and reward-design-heavy.
  Place all of Phase 6 on the method map.

## Phase 7 — Effect Inversion (same loop, different `g`)
- **7.1** **Effects as forward models.** A compressor, a reverb, a distortion are
  synthesizers whose input is audio. DeepAFx (Martínez Ramírez et al. 2021): black-box
  third-party effects as layers, gradients by **SPSA** stochastic approximation; tube
  amp, breath removal, mastering.
- **7.2** **Blind effect estimation (Peladeau & Peeters, ICASSP 2024).** Recover the
  effect's parameters from the *wet* signal alone with an auto-encoder trained on an
  audio loss. DeepAFx-ST (2022): match a *style* (a reference's effect chain) rather
  than a parameter vector.
- **7.3** **The DRC forward model, by hand.** From the collection's `DRC/` notes (Zölzer
  Ch. 7): level detector (PEAK / RMS one-pole) → static curve
  `F = −S(V − L)`, `S = 1 − 1/R` → gain smoother (one-pole, attack/release) →
  broadband multiply. Implement it in `torch` (≈40 lines), compress the note, plot the
  gain curve. Note the **two ballistics pairs** (detector `τ_v`, gain `τ_g`) and the
  quadrature combining rule for the cascade.
- **7.4** **Model-based inversion (Gorlow & Reiss 2013).** Given `θ`, invert the
  compressor sample-by-sample via a root search on the characteristic function. Why
  lookahead and brick-wall limiting are *not* invertible (one-to-many). Invert your
  Phase 7.3 compression and measure the residual.
- **7.5** **Neural-enhanced inversion (Sun, Fourer & Maaref 2024).** Same forward model
  unchanged; an AST **classifies** the compressor *profile* and a regressor estimates
  `θ`, then Gorlow's inversion runs. **Classification beats regression** because the
  inversion amplifies regression error — the keystone again. Threshold `L` dominates
  (`R² = 0.95`); time constants are forgiving.
- **7.6** **Grey-box modelling, reverb, modulation.** Wright & Välimäki (DAFx 2022):
  *fit* the same DRC topology to an LA-2A end-to-end at <10 % of a black-box GRU's cost
  (in the `ddsp` wiki). Götz et al. 2025: match reverberant speech with a learned
  room-acoustic embedding driving an **FDN**. Mitcheltree et al. 2025: **modulation
  discovery** — recover LFO/envelope *shapes* instead of opaque framewise parameters;
  interpretability as a design axis. Pin: estimate a small reverb's decay from the note
  convolved with a synthetic IR.

## Phase 8 — Putting It Together
- **8.1** **The method map, from memory.** Draw `the-inverse-problem.md`'s loop and
  table on a blank page: `g`, `L`, and the route from `L` to `θ`. Place every paper
  from Phases 2–7 in a row. Say which rows survive when (i) you have no source code,
  (ii) you must match a real recording, (iii) you need the whole valley.
- **8.2** **Capstone — recover the note's parameters three ways.** Tiered like
  room-acoustics' a/b/c so it runs with or without a GPU. **Fail fast:** if a package
  import, model download or the note file fails, surface the real error and stop —
  don't paper over it.
  - **(a) CPU (default).** Train a small CNN on log-mel patches of 5 000 two-knob toy
    renders (Phase 3.4), predict `(a, f_c)` for the *real* note, render `g(θ̂)`, plot
    the residual spectrogram, **A/B listen**, and then refine `θ̂` by gradient descent
    on MR-STFT (Phase 1.5). Report: predicted vs refined parameters, both losses, and
    a one-paragraph "why they differ".
  - **(b) Colab GPU.** Tier a, plus the Masuda-style differentiable subtractive synth
    (Phase 5.1): train once with parameter loss only and once with combined parameter +
    spectral loss; match the note with both; compare parameter error *and* audio loss
    *and* your ear — expect them to disagree.
  - **(c) Local GPU.** Tier a, plus DiffMoog (or a small flow-based `p(θ | x)` on the
    two-oscillator toy of 6.2): sample 100 solutions for the note and **plot the
    distribution** — the valley, made visible in high dimension.
- **8.3** **Where to go next.** You can now read the 2024–2025 half of the
  `synth-effect-matching` wiki as an insider. Course 3 (`audio-physics-informed`) puts
  physics into `g` and asks whether that makes the inverse problem better posed; Track
  A's `neural-audio-resynthesis` is the *learned-latent* pole this course's parametric
  pole contrasts with.

## Phase 9 — The Frontier (a living section)
> **This phase tracks the current state of the art and is revised as the field moves** —
> depth-on-demand, never a gate. Each topic reuses the keystone (many parameters, one
> sound) and pins to the same note. *Honesty flag:* everything here is empirical and
> fast-moving; rankings between methods change with each DAFx/ISMIR cycle.
- **9.1** **The 1st DAFx Parameter Estimation Challenge (2025).** A shared benchmark
  for effect parameter estimation (`github.com/LOGUNIVPM/1st-DAFx-Challenge`). Read the
  task definition; ask which row of the method map the winning entries used and why.
- **9.2** **Equivariant and distributional estimation as the default.** Hayes 2025 and
  Peladeau 2025 argue point regression is the wrong object; watch whether 2026 papers
  report *distributions* by default and how they evaluate them (no-reference, multimodal).
- **9.3** **Sound matching at production scale.** Surge XT (Hayes), commercial synths
  via neural proxies (Combes), VST-deployed DDSP synths (Mitcheltree). The open problem
  is hundreds of parameters *with* modulation *on* real recordings.
- **9.4** **JOS's ASA 2025 overheads** (*Neural Parameter Estimation for Musical Sound
  Synthesis*, in the collection) and the *Neural Spectral Modeling Template* — the
  CCRMA-local view of the same map, and the codebase the tier-a capstone mirrors.

### Frontier sources
- Hayes, Saitis, Fazekas (ISMIR 2025) — synthesizer inversion in symmetric parameter
  spaces with approximately equivariant flow matching. arXiv:2506.07199.
- Peladeau, Peeters et al. (DAFx 2025) — audio processor parameters: estimating
  distributions instead of deterministic values.
- Combes, Weinzierl, Obermayer (JAES 2025) — neural proxies for sound synthesizers.
  arXiv:2509.07635.
- Mitcheltree, Tan, Reiss (2025) — modulation discovery with DDSP. arXiv:2510.06204.
- Götz, Dal Santo, Schlecht, Välimäki, Habets (2025) — matching reverberant speech via
  learned acoustic embeddings and FDNs. arXiv:2510.23158.
- Salimi, Hindle, Zaïane (2025) — evaluating sound similarity metrics for
  differentiable iterative sound matching. arXiv:2506.22628.
- Shin & Lee (IJCAI 2025) — SynthRL.
- 1st DAFx Parameter Estimation Challenge (2025) — `github.com/LOGUNIVPM/1st-DAFx-Challenge`.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. This
   subject has an unusually good picture — the **loss surface** — and an unusually good
   oracle — **render and listen**. When notation lands, name it, say what it is in plain
   English, then say what it lets us compute.
3. **Pin it to the note.** Almost every object in this course can be made audible on
   the one through-line note: render `g(θ̂)`, play it next to the target, plot the
   residual spectrogram. Do that. The ear plus the residual is the oracle, the way the
   reconstruction is in `audio-codecs`.
4. **Tiny exercise** to verify: a few lines of `torch`, a by-hand loss evaluation, a
   prediction ("lower the cutoff — which way does the valley move?") checked against a
   runnable cell. The exercise *is* the check that the idea landed.
5. **Common misreadings** when relevant — keep
   [`the-inverse-problem.md`](the-inverse-problem.md)'s list live; flag and correct on
   the spot, and note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in their own words in one or two sentences ("PNP precomputes the
   Jacobian of perception∘synth so parameter error is weighted by what the ear can
   hear").
2. Carry out the small computation: a loss-surface plot, a finite-difference Jacobian,
   a render-and-listen, a DRC gain curve — and explain each step.
3. Spot a deliberately wrong claim ("the CNN's parameter MSE is 0.01, so the match is
   excellent" — not necessarily; render it and listen).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wiki this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Read / link these:

- **[`synth-effect-matching/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/synth-effect-matching/wiki)**
  — the home wiki (41 papers, the largest in the collection). Key pages: `overview.md`
  (the four-phase arc and the five tensions), `synth-parameter-estimation.md` (the
  problem), `sound-matching-approaches.md` (the taxonomy behind the method map),
  `audio-similarity-metrics.md` (the loss `L`), `plug-and-play-priors.md` (PNP),
  `reinforcement-learning-sound-matching.md`, and `drc-parameter-estimation.md` (the
  cross-topic DRC hub).
- **Source summaries** under `…/wiki/sources/`: `itoyama-okuno-icmc14`, `su-rnn-strings-2002`,
  `sterling-bowed-string-2010`, `barkan-deep-synth-pe-2017`, `inversynth-2018`,
  `flowsynth-2020`, `torchsynth-synth1b1-2021`, `masuda-ddsp-ismir21`,
  `masuda-saito-taslp-2023`, `masuda-qd-2023`, `han-pnp-icassp-2023`, `han-pnp-taslp-2024`,
  `mesostructures-2023`, `diff-tf-scattering-2022`, `yang-white-box-ismir23`,
  `yang-white-box-fm-2023`, `diffmoog-2024`, `bruford-ast-dafx-2024`, `sound2synth-2022`,
  `deepafx-2021`, `peladeau-blind-afx-2024`, `peladeau-param-distributions-2025`,
  `gorlow-drc-inversion-2013`, `sun-drc-neural-inversion-2024`, `hayes-equivariant-flow-2025`,
  `neural-proxies-2025`, `synthrl-2025`, `modulation-discovery-2025`,
  `fdn-reverb-matching-2025`, `sound-similarity-metrics-2025`, `han-gradient-clipping-2025`,
  `han-thesis-2025`.
- **The DRC thread (Phase 7.3–7.6)** — the forward-model derivation and the Zölzer ↔
  Gorlow/Sun notation map live in the collection's `DRC/` directory (`DRC.tex` /
  `DRC.pdf`); the grey-box counterpart is `ddsp/wiki/sources/wright2022-greybox-drc.md`.
- **Neighbours:** `ddsp/wiki/` (course 1; Masuda, DiffMoog and DeepAFx-ST appear in
  both wikis) and `attention/wiki/` (the AST encoder used by Bruford and Sun).

### DSP depth (assumed here — this course *uses* it rather than teaching it)
JOS's books: *Introduction to Digital Filters* (one-poles, biquads, stability — Phases
1.3, 7.3), *Spectral Audio Signal Processing* (STFT, spectral modeling,
analysis-by-synthesis — Phases 1.2, 4.2), and *Physical Audio Signal Processing* (the
plucked-string models of Phase 2.3 and course 3). The `ccrma.stanford.edu/~jos/` series.

### Source papers (the ones this course tracks most closely)
- **Itoyama & Okuno (ICMC 2014)** — parameter estimation of virtual instrument
  synthesizers from handcrafted features.
- **Barkan & Tsiris (ICASSP 2019; preprint 2017)** — *Deep Synthesizer Parameter
  Estimation*; **Barkan et al. (2018)** — *InverSynth*. arXiv:1812.06349.
- **Esling, Masuda et al. (2020)** — *Flow Synthesizer*.
- **Turian, Shier et al. (DAFx 2021)** — *One Billion Audio Sounds* / torchsynth.
  arXiv:2104.12922.
- **Martínez Ramírez et al. (2021)** — *DeepAFx*. arXiv:2105.04752.
- **Masuda & Saito (ISMIR 2021; TASLP 2023)** — synthesizer sound matching with
  differentiable DSP; semi-supervised extension.
- **Muradeli et al. (2022)** — differentiable time–frequency scattering. arXiv:2204.08269.
- **Chen et al. (2022)** — *Sound2Synth*. arXiv:2205.03043.
- **Steinmetz et al. (2022)** — *DeepAFx-ST*. arXiv:2207.08759.
- **Vahidi, Han et al. (2023)** — *Mesostructures*. arXiv:2301.10183.
- **Han et al. (ICASSP 2023; TASLP 2024)** — perceptual-neural-physical (PNP) sound
  matching. arXiv:2301.02886; arXiv:2311.14213.
- **Yang, Jin, Barnes, Finkelstein (ISMIR 2023)** — white-box search over synthesizer
  parameters; **Yang et al. (2023)** — white-box FM parameter estimation.
- **Uzrad, Barkan et al. (2024)** — *DiffMoog*. arXiv:2401.12570.
- **Peladeau & Peeters (ICASSP 2024)** — blind estimation of audio effects.
- **Bruford et al. (DAFx 2024)** — sound matching with Audio Spectrogram Transformers.
- **Gorlow & Reiss (2013)**; **Sun, Fourer & Maaref (2024)** — model-based and
  neural-enhanced DRC inversion.
- **Wright & Välimäki (DAFx 2022)** — grey-box DRC (in `ddsp/`).
- The 2025 frontier list above.
