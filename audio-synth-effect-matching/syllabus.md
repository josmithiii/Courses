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
(`../curricula/assets/audio-differentiable-dsp/note.wav`, mono 44.1 kHz, ~6 s). Course 1
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
and explain why *classification* of the compressor profile beats regression; read a
loss landscape for its *ridges* as well as its valleys; and place any 2024–2026 paper in
the collection — including the DAFx26 papers and the plate-reverb challenge entries — on
the method map in `the-inverse-problem.md`.

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
  renders on the toy synth and compare to Phase 1.5's gradient descent. **Not a relic:**
  in the DAFx26 plate-reverb challenge (Phase 9.1) a training-free **CMA-ES** search
  recovered six physical parameters to NMSE ≈ 2e-11 — "search is slow" assumes a slow
  renderer and a high-dimensional space; a cheap GPU simulator in 6-D removes both.
  Swap random search for `cma` (or a 20-line evolution strategy) on the toy synth and
  count renders-to-convergence.
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
- **4.6** **Ridges, not just valleys — loss-landscape geometry (DAFx26).** Phase 1.4's
  valleys are where the loss *can't decide*; ridges are where its *gradient breaks*.
  Tabata, Iwaya & Kondo (Yamaha, DAFx26) map the 1-D Wasserstein-1 loss for 2-op FM
  over `(f_c, f_m)`: far smoother than spectral MSE, but with non-differentiable
  **ridges on rational ratios** `f_m/f_c = m/n` — negative-frequency **folding** of the
  lower sidebands (a cusp at `ω = 1/n`) and **ordering swaps** of folded sidebands
  (`ω = 2/3, 2/5, …`). Ridge positions are independent of the modulation index `β`;
  their height grows with it. The fix is DSP-literate, not neural: run Adam in parallel
  inside each **wedge** between low-order rationals, keep the best (success 68 % → 97 %;
  the remaining failures sit exactly *on* a ridge). Two more DAFx26 warnings about the
  ruler: in a resonant recursive decoder SOT turns out **blind to `f_0`** (Tablas de
  Paula, 5.7), and **log-magnitude compression in the standard MR-STFT loss collapses
  recovery** of plate-reverb parameters under CMA-ES (Park, Yi et al., challenge
  entry 83; uncompressed L1 on STFT magnitude converges every time). Exercise: on the
  toy synth, plot the MR-STFT surface with and without the `log`, then a 2-op FM `W_1`
  slice along `ω` at fixed `f_c` — find the cusp at `ω = 1/2` by eye before computing
  it. Kill misreading #9 here.

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
- **5.7** **A differentiable Karplus–Strong — the through-line note's own model
  (Tablas de Paula et al., DAFx26).** The decoder is the *extended* Karplus–Strong of
  Jaffe & Smith (loop filter reparameterised so DC gain `g` sets decay and `a_1` sets
  damping independently; pluck-position comb; dynamics filter), made differentiable;
  an encoder emits a *set* of pluck **events** (onset, `f_0`, decay, damping, pluck
  position, level), Hungarian-matched to ground truth. The DSP results are worth the
  session on their own: **delay-line length is differentiable in the time domain** with
  an order-5 Lagrange fractional delay — as accurate as the frequency-sampling version
  and with none of its time-aliasing (a KS loop at `g = 0.999` rings for tens of
  seconds at low `f_0`, so *no* FFT size avoids wrap-around). The learning results
  sharpen the keystone: (i) **no spectral or OT loss supervises onset time** — a third
  axis, beside parameter-vs-audio, of what the loss cannot see; (ii) joint
  parameter + audio training **collapses** (F1 0.01) unless the onset head is detached;
  (iii) parameter loss on synthetic plucks wins in-domain and **does not transfer** to
  real guitar — Phase 3.4's gap, measured on a physical model; (iv) a harmonic-plus-noise
  DDSP baseline still wins most fidelity metrics, because a single KS loop has no body,
  hand or fret. Exercise: write a 1-pluck tKSA in `torch` (integer delay + Lagrange
  fractional delay + one-pole loop filter), set `f_0` from Phase 0.2's measurement, fit
  `(g, a_1)` to the note by gradient descent, A/B, and plot the residual — then try to
  fit the onset time with MR-STFT and watch the gradient do nothing.

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
- **6.7** **Matching by retrieval in a shared audio–preset embedding (Braun &
  Finkelstein, DAFx26 — "SynAPSE").** Don't predict, optimise or sample `θ` — embed
  every preset and every sound in one space and *look up* the nearest preset. The
  preset encoder (**DX7-GNN**) is the synth's own signal flow: six operators as nodes,
  the algorithm's modulation routing as edges, feedback as a learned-attenuation edge,
  silent operators sending exactly zero; weights are shared across nodes, so **unseen
  routing algorithms** can be encoded. Trained jointly with an audio encoder (SLAP, a
  non-contrastive BYOL-style objective) on DX7 presets: R@1 ≈ 86 % when all 32
  algorithms are seen — encoder choice barely matters — but on 8 *held-out* algorithms
  the 3.4 M-parameter GNN reaches 52 % R@1 vs 35 % for a 57 M-parameter Transformer.
  **Operator-swapping augmentation** is essential (52 % → 13.5 % without): the
  symmetry of 6.2, handled by data rather than by an equivariant flow. Gradient-free by
  construction, so immune to 4.6's FM ridges; the price is that the answer is limited
  to the gallery. Compare 6.5's neural proxies (a flat-vector preset encoder, a frozen
  audio model). Exercise: embed 200 toy-synth renders by their log-mel mean, retrieve
  the nearest render to the note, and compare its `(a, f_c)` with 1.5's estimate.
  Place all of Phase 6 on the method map — retrieval is a new row.

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
- **7.7** **Supervise what defines the effect: the gain trajectory (Thompson &
  Heilemann, DAFx26).** A compressor *is* its gain trajectory `g_dB[k]`, but hardware
  output is `y = g·(h ⊛ x) + N`, so `y/x` is an ill-conditioned inverse problem and
  waveform losses inherit sensitivity to inaudible filtering and noise. With a measured
  **SSL G384 bus-compressor dataset** that records the VCA's gain-reduction **control
  voltage** alongside the audio (19 710 clips × switch settings), fitting a grey-box
  `torchcomp` model under three losses shows gain-trajectory error separating the
  models by 86 % while waveform `L1` spreads 2.8 % and Wright & Välimäki's MSTE 13 %:
  **proxy losses give near-identical scores to clearly different compressors.** This
  sits *against* Peladeau 2024 (optimise audio, not parameters) — both reject waveform
  `L1`, for opposite goals: perceptual match vs device emulation. Parameter *recovery*
  from this dataset is left open — the Sun 2024 experiment, now with ground-truth gain.
  Exercise: with your 7.3 compressor, train two parameter sets that differ in attack
  but match `L1(y)` to within 3 %, then plot their gain curves.
- **7.8** **Beyond one effect: graphs, text, labels (DAFx26).** The effect branch
  widens from one processor to a whole mixing chain. **WildFX** (Yang et al.) renders
  graph-labelled multitrack datasets through *real* plugins in a headless REAPER and
  retrains Lee et al.'s blind graph estimator: connectivity is recovered, but
  **processor-type recognition fails** (node error 57–69 %) — a *categorical* inverse
  problem inside a continuous one. **InstructFX2FX** (Yu et al., demo) makes
  text-to-effect multi-turn: an LLM picks the chain, CLAP-guided descent (or Bayesian
  optimisation for non-differentiable plugins) refines it, and a *directional* CLAP
  objective keeps earlier instructions. **Clean2FX** (Roman & Bombicci Pontelli, demo)
  is a label-conditioned black-box effect U-Net — no parameters at all — whose MSE and
  FAD diverge for reverbs and delays. Place each on the method map: the target `x` is
  now a graph, a sentence or a label rather than a sound.

## Phase 8 — Putting It Together
- **8.1** **The method map, from memory.** Draw `the-inverse-problem.md`'s loop and
  table on a blank page: `g`, `L`, and the route from `L` to `θ`. Place every paper
  from Phases 2–7 in a row. Say which rows survive when (i) you have no source code,
  (ii) you must match a real recording, (iii) you need the whole valley, (iv) the
  simulator is cheap enough to call a million times. Then answer the DAFx26 challenge's
  question: why did *learned initialiser + search polish* win, and which two rows does
  it combine?
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
- **8.3** **Where to go next.** You can now read the 2024–2026 half of the
  `synth-effect-matching` wiki as an insider. Course 3 (`audio-physics-informed`) puts
  physics into `g` and asks whether that makes the inverse problem better posed; Track
  A's `neural-audio-resynthesis` is the *learned-latent* pole this course's parametric
  pole contrasts with.

## Phase 9 — The Frontier (a living section)
> **This phase tracks the current state of the art and is revised as the field moves** —
> depth-on-demand, never a gate. Each topic reuses the keystone (many parameters, one
> sound) and pins to the same note. *Honesty flag:* everything here is empirical and
> fast-moving; rankings between methods change with each DAFx/ISMIR cycle.
- **9.1** **The 1st DAFx Parameter Estimation Challenge — results (DAFx26).** The
  field's first head-to-head of the method-map rows on one hidden-ground-truth inverse
  problem: invert a damped Kirchhoff–Love **plate reverb** (a modal bank of thousands of
  biquads) from one impulse response. Task A: six identifiable physical parameters
  (scored by NMSE). Task B: the unknown number of modal `(frequency, decay, gain)`
  triples. 13 teams, 22 methods, overview + 15 entry papers in the collection
  (`DAFx26Challenge-76…91`; wiki hub `plate-reverb-parameter-estimation-challenge.md`).
  What it taught, keystone by keystone:
  - **Learned initialiser + search polish wins.** QMUL's AST regressor / flow-matching
    sampler (Hayes' estimator, minus equivariance) gets NMSE ~1e-4; PSO or gradient
    polish through the simulator takes it to **~2e-13**. A **training-free CMA-ES**
    (UIUC) is a close second (2e-11); staged differential evolution (MIT/CCRMA) third.
    When `g` is cheap and low-dimensional, search is not the slow row.
  - **Pure DDSP is bimodal.** The differentiable modal plate either nails it (median
    6e-6) or falls into a wrong basin (mean 0.018) — one scalar loss per full synthesis
    is little information per evaluation. Phase 1.5's stuck start, at scale.
  - **The ruler decides.** Log compression in MR-STFT kills CMA-ES recovery (4.6);
    peak-normalisation discards the cue to surface density, so it needs its own stage.
  - **Formulation beats architecture.** In Task B a 3 M-parameter U-Net and a ~100 M
    complex transformer share a **per-bin mode-*density*** target and tie for first,
    0.2 ahead of everyone: regressing a density sidesteps the unknown-cardinality
    problem that peak pickers and subspace methods fight.
  - **Metrics decide winners — and non-identifiability is visible.** Above the
    modal-overlap crossover (~250 Hz–1.4 kHz) no unique set of triples exists, so
    **no entry recovers modal gains**; the organisers' `log|H(f)|` re-evaluation
    reorders Task B (a 30 dB bulk gain bias was invisible to the per-mode metric).
    Only one entry (simulation-based inference) returns a calibrated posterior.
  - **Untested:** real plates, noise, out-of-range parameters, listening tests — the
    benchmark cannot yet tell interpolation from general inverse solving.

  Pin: run CMA-ES and 1.5's gradient descent on the toy synth from the *same* CNN
  initialisation (3.4) and compare final losses and render counts.
- **9.2** **Equivariant and distributional estimation as the default.** Hayes 2025 and
  Peladeau 2025 argue point regression is the wrong object; watch whether 2026 papers
  report *distributions* by default and how they evaluate them (no-reference,
  multimodal). DAFx26 scorecard: the challenge's SBI entry and QMUL's flow sampler use
  posteriors, but mostly as initialisers for a point polish; SynAPSE (6.7) sidesteps
  the question with retrieval.
- **9.3** **Sound matching at production scale.** Surge XT (Hayes), commercial synths
  via neural proxies (Combes), VST-deployed DDSP synths (Mitcheltree), real-plugin
  effect graphs (WildFX), topology-general FM retrieval (SynAPSE). The open problem is
  hundreds of parameters *with* modulation *on* real recordings.
- **9.5** **Physical decoders and the sim-to-real gap.** DAFx26 gave opposite answers
  to "does a physical `g` beat a harmonic-plus-noise DDSP decoder?": a single KS loop
  loses on real guitar (Tablas de Paula, 5.7) while a Kelly–Lochbaum vocal tract wins
  on biphonic singing (Camara et al., in the `ddsp` wiki). The difference is what the
  physical model *omits* (body, hand, fret). This is course 3's question, asked from
  the inverse side.

> **9.6–9.8 are newer than the curated wiki** (preprints and ISMIR/ICASSP 2026 papers
> found by web search, Oct 2026). They are **not yet in the paper collection or the
> wiki**, and are summarised from their abstracts only — treat details as provisional
> until ingested.

- **9.6** **Closing the cross-domain gap inside the generative route (Hayes 2026).**
  *Off-manifold robustness … with joint distribution flow matching* (Hayes, preprint):
  model the **joint** `p(audio, θ)` with a multimodal flow and *independent* noise
  schedules per modality, so **unlabelled real recordings** can train the audio
  marginal — Masuda's "fine-tune on real sounds" (5.1), rebuilt for 6.3's flow;
  partially noising the reference at inference helps further (Surge XT, Dexed).
  *Synth-JEPA* (Hayes, Tian, Lattner, preprint): learn audio and parameter embeddings
  that *predict each other*, then **search** presets scored in that space **without
  rendering** — 6.7's retrieval and 9.1's search, fused; quality grows with test-time
  search budget; listeners preferred it in 85 % of pairwise trials. Ask: which method-map
  rows does each combine?
- **9.7** **Discrete generation, RL fine-tuning, editable programs.** *DDSynth-RL*
  (Wu, Chin, … Xia, ISMIR 2026): inversion as **masked discrete diffusion** over
  quantised parameters (echoing 3.2's classification into levels), then GRPO-style
  RL with rewards on the *rendered* audio — no gradient through the black-box Dexed;
  RL improves out-of-domain matching (6.6 meets 6.3). *AutoSynth* (same group,
  preprint): one autoregressive sequence of MIDI events + synth settings +
  **variable-length modulation routes**, so text-to-synth becomes text → audio
  generator → inversion → an *editable* program. Liu et al. (Dolby, submitted to ICASSP
  2027) extend modulation discovery (7.6): first find **which destinations** are
  modulated, then each LFO shape; a Gammatone loss + CQT discriminator beats MR-STFT.
  Takemoto, Nakamura, Saruwatari (APSIPA 2026): a diffusion prior over parameter
  *trajectories*, guided by a DDSP mixture's reconstruction error, estimates each
  source's parameters in a polyphonic ensemble.
- **9.8** **Effects and the loss question, 2026.** The DRC thread continues: Sun,
  Fourer, Maaref (preprint) replace their 2024 neural estimator with **black-box
  optimisation in a perceptual feature space** (non-differentiable, histogram-based
  descriptors allowed) for blind compressor estimation and dry-signal recovery.
  Okita & Katayose (ICASSP 2026): **predict which effects are present, then search
  their order and parameters** — 9.1's "learn, then search" lesson in the effect
  branch. Effect *chains* go generative and agentic: StemFX (Cheng … Yang, ISMIR 2026;
  autoregressive per-stem FX-chain tokens, >4000× faster style transfer than iterative
  optimisation); LLM2Fx-Tools (Doh … Mitsufuji, ICLR 2026; a multimodal LLM emits an
  executable effect chain by tool calling); PEACE (Braun & Finkelstein, ISMIR 2026;
  SynAPSE's joint embedding between **Faust effect code** and wet audio). The loss
  question: Salimi et al.'s follow-up to 4.5 (preprint) handles *out-of-domain*
  matching with a **partial parameter distance** over the knobs two synths share —
  still no universal loss (SIMSE on spectra for cutoff, DTW on envelopes for AM, JTFS
  for smooth pitch), and its top loss agrees with blind listening in 5 of 7 scenarios.
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
- **DAFx26 (Cambridge MA, 1–4 Sept 2026)** — PDFs in the collection, summaries in the
  wiki's "DAFx26 (2026)" index section:
  - Tablas de Paula, Marttila, Díaz, Román, Benetos, Reiss — sound matching with a
    differentiable Karplus–Strong algorithm (paper 38).
    `ptablasdpaula.github.io/DAFx26-Karplus/`
  - Tabata, Iwaya, Kondo (Yamaha) — FM parameter estimation with low-order rational
    constraints on the Wasserstein loss landscape (paper 37).
  - Braun & Finkelstein — FM synthesizer audio–parameter shared embeddings
    (SynAPSE / DX7-GNN) (paper 33). `github.com/DBraun/SynAPSE`
  - Thompson & Heilemann — evaluating DRC models using control-voltage measurements:
    an approach and dataset (paper 30). `doi.org/10.60593/ur.d.31892026`
  - Yang, Berg-Kirkpatrick, McAuley, Novack — WildFX: a DAW-powered pipeline for
    in-the-wild audio FX graph modeling (paper 56). `github.com/IsaacYQH/WildFX`
  - Yu et al. — InstructFX2FX: multi-turn text-to-effect (demo 74).
  - Román & Bombicci Pontelli — Clean2FX: label-conditioned clean-to-effect guitar
    transformations (demo 58).
- **1st DAFx Parameter Estimation Challenge** (Gabrielli & Ducceschi; results at DAFx26)
  — `github.com/LOGUNIVPM/1st-DAFx-Challenge`; organisers' overview (76) and 15 entry
  papers (77–91), notably 82 (Marttila et al., transformer/flow + PSO), 83 (Park, Yi et
  al., two-stage CMA-ES), 79 (Lee et al., ALAMODE differential evolution), 84 (Sechet
  et al., simulation-based inference), 77 (Garofalo et al., differentiable modal
  plate), 87 (Díaz et al., count-density networks), 90 (Lu & Reiss, band-count +
  differentiable resonator refinement).
- Camara et al. (DAFx26, paper 39) — differentiable articulatory copy-synthesis of
  biphonic singing (in the `ddsp` wiki; the physical-decoder counterpoint of 9.5).
- **Post-DAFx26 (not yet in the collection; abstracts verified on arXiv, Oct 2026):**
  - Hayes (2026) — off-manifold robustness in synthesizer inversion with joint
    distribution flow matching. arXiv:2609.29320.
  - Hayes, Tian, Lattner (2026) — Synth-JEPA: joint embedding prediction for
    renderer-free synthesizer parameter search. arXiv:2609.31024.
  - Wu, Chin, Zhang, Jiang, Jing, Xia (ISMIR 2026) — DDSynth-RL: synthesizer inversion
    via discrete diffusion with reinforcement learning. arXiv:2608.03032.
  - Wu, Chin, Lin, Zhang, Xia (2026) — AutoSynth: generating editable synthesizer
    programs from audio and text. arXiv:2610.10774.
  - Liu, Cengarle, Cooper, Vinton, Yang (submitted to ICASSP 2027) — interpretable
    destination-aware synthesizer modulation recovery. arXiv:2610.00642.
  - Takemoto, Nakamura, Saruwatari (APSIPA 2026) — DDSP mixture-model-guided diffusion
    for synthesis parameter estimation from harmonic sound mixtures. arXiv:2609.14427.
  - Salimi, Penner, Eng, Hindle, Zaïane (2026) — loss functions in differentiable
    out-of-domain sound matching with partial parameter distance. arXiv:2608.27698.
  - Sun, Fourer, Maaref (2026) — black-box optimization for identifying and inverting
    audio dynamic range control effects. arXiv:2607.19645.
  - Okita & Katayose (ICASSP 2026) — audio effect estimation with DNN-based prediction
    and search. arXiv:2604.22276.
  - Cheng, Wu, Chen, Yeh, Chen, Yang (ISMIR 2026) — StemFX: mixing-style
    representations via autoregressive FX-chain prediction. arXiv:2607.15634.
  - Doh, Koo, Martínez-Ramírez, Choi, Liao, Wu, Nam, Mitsufuji (ICLR 2026) —
    LLM2Fx-Tools: tool calling for music post-production. arXiv:2512.01559.
  - Braun & Finkelstein (ISMIR 2026) — PEACE: joint embeddings of DSP effects code and
    audio. `github.com/DBraun/PEACE` (no arXiv ID found; venue from the ISMIR
    accepted-papers list, not independently checked).
  - Also noted, smaller: Bogdan (2026), INSTRUMENTAL — CMA-ES on a 28-parameter
    subtractive synth (arXiv:2603.15905); Ki et al. (2025), FxSearcher — CLAP-scored
    Bayesian optimisation for text-to-effect (arXiv:2511.14138).

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
  — the home wiki (64 papers: 41 core, 7 DAFx26, 16 plate-reverb challenge — the
  largest in the collection). Key pages: `overview.md` (the four-phase arc, the
  "DAFx26: what shifted" paragraph, and the tensions), `synth-parameter-estimation.md`
  (the problem), `sound-matching-approaches.md` (the taxonomy behind the method map),
  `audio-similarity-metrics.md` (the loss `L`, incl. "Loss Landscape Geometry"),
  `plug-and-play-priors.md` (PNP), `reinforcement-learning-sound-matching.md`,
  `audio-effect-estimation.md` (the effects branch: inversion, blind/distributional,
  graphs, text, device-internal supervision), `drc-parameter-estimation.md` (the
  cross-topic DRC hub), and `plate-reverb-parameter-estimation-challenge.md`.
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
  `han-thesis-2025`; DAFx26: `tablas-diff-karplus-strong-dafx26`,
  `fm-wasserstein-landscape-dafx26`, `fm-shared-embeddings-dafx26`,
  `drc-control-voltage-dataset-dafx26`, `wildfx-fx-graph-dafx26`,
  `instructfx2fx-dafx26`, `clean2fx-dafx26`, and `dafx26-challenge-76…91-*`.
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
- **Tablas de Paula et al.; Tabata et al.; Braun & Finkelstein; Thompson & Heilemann
  (DAFx26)** — taught in Phases 5.7, 4.6, 6.7 and 7.7.
- The 2025–2026 frontier list above.
