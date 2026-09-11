# Differentiable DSP — Learning the Parameters of the Blocks You Already Know

**Learner profile:** Comfortable with the material in JOS's *Introduction to Digital
Filters* (difference equations, poles and zeros, biquads, stability) and the STFT and
sinusoidal-modeling chapters of *Spectral Audio Signal Processing*; has done
`ai-foundations/` through Phase 2 (PyTorch tensors, autograd, a training loop) or the
equivalent. **The learner is DSP-first:** they know what a filter is, so we move fast to
the part that is new — what happens when autograd meets an oscillator bank, why the
loss must be spectral, and how the 2020–2024 literature turned classical audio blocks
into learnable ones. Neural networks appear only as *parameter predictors* and are
introduced when needed. ~1 hour per day. One concept at a time. Every concept verified
with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**The keystone — read [`the-differentiable-block.md`](the-differentiable-block.md) in
Phase 0.1.** This course has one organizing idea in two halves: a DSP block whose output
is an explicit differentiable function of its parameters can have those parameters
*learned* by gradient descent; and the loss after it must be a **multi-scale spectral
loss** (or better), because sample-wise waveform error does not hear. Every paper in the
`ddsp/` directory is a choice of *which block* and *which loss*. We spend as long as it
takes on Phase 2.

**The qubit (worked example):** the curriculum's shared **plucked-string note**
(`../curricula/assets/audio-differentiable-dsp/note.wav`, mono 44.1 kHz, ~1.5 s; spec and
status in that directory's `README.md`). We carry *this one note* through every block —
resynthesize it with a hand-built harmonic+noise model, fit that model by gradient
descent, pass it through learned filters, reverbs and a grey-box compressor — and
**listen** at each stage. (Courses 2 and 3 pick it up from here: invert it to synth and
effect parameters; model the string that produced it.)

**End state:** by the last lesson the learner can: write a harmonic oscillator bank, a
frequency-sampled FIR noise shaper, and a biquad in PyTorch and get gradients through
each; explain *why* waveform MSE fails and write the multi-scale spectral loss from
memory; explain the frequency-gradient pathology and why DDSP estimates `f₀` rather than
learning it; describe the DDSP autoencoder (encoder → decoder → synthesizer → loss) and
what each output means; state the IIR-vs-FIR trade-off and name the three responses to
it (BPTT, frequency-domain training, FIR approximation); read a grey-box effect paper and
say where the learned part sits; place DDX7, DDSP-Piano, MIDI-DDSP and DiffMoog on the
"which block, which loss" map; and fit a differentiable synthesizer to the note and hear
the result.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture**, no code yet: classical synthesis and
  effects are parameterized DSP graphs; DDSP puts the graph *inside* a training loop and
  learns the parameters from audio. Read [`the-differentiable-block.md`](the-differentiable-block.md).
  Where this course sits in the `audio-differentiable-dsp` curriculum (foundation for
  courses 2 and 3) and how it differs from Track A's learned latents (legible parameters
  vs expressive-but-opaque codes).
- **0.2** **Tools.** `torch`, `torchaudio`, `numpy`, `matplotlib` importable; load the
  through-line note (or generate the labelled placeholder with
  `../curricula/assets/audio-differentiable-dsp/make_note.py` and *say* it is synthetic),
  print shape and sample rate, play it, plot waveform and spectrogram. Confirm audio
  playback works (`IPython.display.Audio` or write-and-play a WAV). **Fail fast:** if an
  import or the note is missing, surface the real error; never substitute silently.
- **0.3** **Measure the note by hand.** FFT peak-pick the first ~10 partials: frequencies,
  amplitudes, and a rough per-partial decay (T60). These are *the numbers we reuse* for
  the rest of the course — write them into `progress.md`.

## Phase 1 — The Blocks (forward only; brisk, the learner knows this DSP)
> A fast pass through the blocks we will differentiate, each written in PyTorch as a
> plain forward function. Depth lives in *Filters* and *SASP* — we write code and move on.
- **1.1** **A DSP block as a function.** `y = g(θ; x)`: parameters `θ`, optional input
  `x`, output audio `y`. Frame-rate vs sample-rate parameters; upsampling control
  signals (linear / overlapping-window interpolation) so a network can predict 250
  values/s and the synth can run at 44.1 kHz.
- **1.2** **The harmonic oscillator bank.** `y[n] = Σ_k A_k[n] sin(φ_k[n])`, phase by
  cumulative sum of `2π k f₀[n]/f_s`. Write it; drive it with the note's measured
  partials from 0.3 and *listen* — the first resynthesis. Anti-aliasing: zero any
  harmonic above Nyquist.
- **1.3** **Filtered noise by frequency sampling.** Predict a magnitude response per
  frame; IFFT → window → FIR; overlap-add. FIR by construction. Add a noise layer to
  the resynthesis for the pluck's attack and *listen* to what it adds.
- **1.4** **Filters as we know them.** A biquad `H(z)`; direct-form recursion; poles
  inside the unit circle. Write a biquad forward pass in PyTorch as a Python loop
  (slow — that slowness is Phase 4's whole problem). Frequency response by evaluating
  `H(e^{jω})`.
- **1.5** **Convolutional reverb and the STFT.** Reverb as convolution with an impulse
  response (FIR, differentiable, cheap by FFT). `torch.stft` magnitude at several FFT
  sizes — the object the loss will look at. Plot the note at 64/512/2048-point windows
  and say what each resolution sees (attack vs partials).

## Phase 2 — Autograd Meets DSP (the keystone — spend as long as it takes)
> Re-read [`the-differentiable-block.md`](the-differentiable-block.md) here.
- **2.1** **Gradients through the oscillator.** Make `A_k` and `f₀` `requires_grad`
  tensors; compute a loss; call `.backward()`; inspect `∂L/∂A_k` and `∂L/∂f₀`. Then the
  experiment that teaches the course: sweep `f₀` from 100 to 120 Hz against the
  110 Hz note and plot the loss. The `f₀` landscape is **oscillatory with local
  minima** — the frequency-estimation pathology. Conclusion DDSP draws: *estimate* `f₀`
  (CREPE), *learn* the amplitudes.
- **2.2** **Why waveform MSE is the wrong ruler.** Render the note twice with a
  starting-phase change, and again with partials shifted by 3 cents; compare sample-wise
  MSE (huge) with what you hear (identical). Phase and cents sensitivity in one plot.
- **2.3** **The multi-scale spectral loss.** `L = Σ_s ‖|S_s(y)| − |S_s(t)|‖₁ +
  ‖log|S_s(y)| − log|S_s(t)|‖₁`, FFT sizes 64…2048. Write it. Why magnitude (phase-blind),
  why several sizes (transients vs partials), why the log term (quiet partials count).
  Redo the 2.1 sweep with this loss and see the landscape improve — but not become convex.
- **2.4** **Parameter loss vs audio loss.** With synthetic data you have `θ*`; L2 on
  `θ` is fast. Show two far-apart `θ` that sound the same (swap two partials' amplitude
  ordering; detune a masked partial). Perception is **many-to-one** in `θ` — the seam into
  course 2, where this becomes the whole subject.
- **2.5** **What spectral loss still misses.** Phase coherence between partials,
  transients under long windows, inharmonic and noise-dominated sounds, stereo. Name
  the responses (adversarial loss, JTFS scattering, learned embeddings — course 2 Phase 4)
  and the review's verdict: good default for harmonic sounds, not ground truth.
- **2.6** **Pin to the note: gradient-descent copy synthesis.** Fix `f₀` at the
  measured 110 Hz; initialize `A_k[n]` and the noise magnitudes randomly; optimize with
  Adam against the spectral loss until the resynthesis matches. **Listen** to iterations
  0, 50, 500. The keystone, audible.

## Phase 3 — The DDSP Autoencoder (Engel et al. 2020)
- **3.1** **Inductive bias, stated.** Black-box waveform models (WaveNet, GANSynth)
  must *discover* periodicity and phase coherence from data; a harmonic oscillator bank
  *assumes* them. That is why DDSP trains a convincing violin from 13 minutes of audio
  with no adversarial loss and no autoregression. One sentence of history: additive /
  spectral-modeling synthesis (SASP) is the block; DDSP made it trainable.
- **3.2** **The architecture.** Encoder: `f₀` (CREPE) + loudness (A-weighted log-RMS)
  per frame, optionally a learned timbre `z`. Decoder: MLP/GRU → per-frame harmonic
  amplitudes (an overall amplitude × a normalized harmonic distribution) + noise filter
  magnitudes + a global reverb IR. Synthesizer: Phase 1's blocks. Loss: Phase 2.3.
  Draw it; name every tensor's shape.
- **3.3** **Output parameterizations that keep training sane.** Sigmoid-scaled
  amplitudes (`2·sigmoid(x)^log10 + 1e-7`), softmax harmonic distribution, Nyquist
  masking, control-signal upsampling. Why each is there (gradient range, positivity,
  aliasing).
- **3.4** **What you can do because the parameters have names.** Timbre transfer (feed
  a flute's `f₀`/loudness to the violin model), pitch extrapolation beyond the training
  range, blind dereverberation (drop the learned IR), independent pitch/loudness/timbre
  edits. Contrast with Track A: a codec latent can do more but you cannot *read* it.
- **3.5** **Analysis by synthesis: self-supervised pitch detection** (Engel et al. 2020b).
  Train the *encoder* through the differentiable synthesizer with a reconstruction +
  consistency loss and get an `f₀` estimator with no pitch labels. The differentiable
  forward model turns synthesis into an inverse-problem solver — the bridge to course 2.
- **3.6** **Pin to the note.** Run the DDSP harmonic+noise model on the note (a
  pretrained checkpoint on CPU, or the Phase 2.6 fit): inspect the harmonic distribution
  over time, the noise magnitudes, the IR; edit one harmonic and *listen*.

## Phase 4 — Differentiable Filters and Effects
- **4.1** **IIR as a constrained RNN** (Kuznetsov, Parker, Esqueda 2020). The recursion
  is backprop-through-time; stability needs poles inside the unit circle (parameterize
  radius through a sigmoid). Direct form vs state-variable filter vs lattice — SVF trains
  best. Truncated BPTT for long audio. Fit a single learnable biquad to a target response
  and watch the pole move.
- **4.2** **Two escapes from the recursion.** *Frequency-domain training* — compare
  `H(e^{jω})` of a biquad cascade to a target response, no time loop (Nercessian et al.
  2021: 40 hyperconditioned biquads, 210 parameters, model a distortion pedal).
  *FIR approximation by frequency sampling* — Lee et al. 2021 rebuild artificial reverb
  (filtered velvet noise, delay networks) as FIR so it trains on a GPU. **The IIR-vs-FIR
  trade-off** stated once and for all: compact/musical/sequential vs
  parallel/memory-hungry/approximate.
- **4.3** **All-pass and phase** (Bargum et al. 2023). Neural virtual-analog models learn
  arbitrary phase responses; dry/wet mixing then comb-filters. A differentiable all-pass
  estimates and aligns phase. Why magnitude-only losses let this happen (Phase 2.5).
- **4.4** **Time-varying effects: the phaser** (Carson et al. 2023). Cascaded all-pass
  in the frequency domain per frame; the **LFO** rate/depth learned *jointly* with the
  filter — interpretable knobs survive training.
- **4.5** **Dynamics: the grey-box compressor** (Wright & Välimäki 2022; Nercessian et
  al. 2022 microdynamics). Keep the *structure* — gain computer (threshold/ratio/knee)
  → level detector (one-pole, attack/release) → make-up gain — and learn its
  parameters end-to-end to emulate an LA-2A at under 10% of a black-box GRU's cost.
  Three detector variants (single time-constant in the frequency domain; switching
  attack/release; RNN-modulated per-sample). Use the `DRC/` forward-model notes
  (Zölzer Ch. 7) for the equations. Pin to the note: compress it with the grey-box
  model; read the learned threshold and ratio.
- **4.6** **Chains and style transfer.** A differentiable mixing console (Steinmetz et
  al. 2020); **DeepAFx-ST** (Steinmetz et al. 2022) — an encoder predicts parameters for
  an EQ→compressor chain, trained self-supervised with an audio loss, so a *production
  style* transfers and the result is a readable preset.

## Phase 5 — Richer Synthesizers
- **5.1** **FM: DDX7** (Caspe, Shier, Sandler 2022). A differentiable DX7 patch;
  the parameter→spectrum map is so nonlinear that optimization lands in local minima —
  the price of a richer block. Constraints (fixed frequency ratios, envelope structure)
  as the cure.
- **5.2** **Polyphony and inharmonicity: DDSP-Piano** (Renault, Mignot, Roebel 2022).
  A physics-informed partial model with stiffness inharmonicity `f_n = n f₁ √(1 + B n²)`
  — the first appearance of a *physical* prior inside a DDSP block, and the hand-off to
  course 3. Measure the note's `B` from the Phase 0.3 partials.
- **5.3** **Hierarchy: MIDI-DDSP** (Wu et al. 2021). Notes → expression (a performance
  model predicts per-note controls) → synthesis (DDSP). Three legible levels, each
  editable.
- **5.4** **Physical blocks: the differentiable vocal tract** (Sudholt et al. 2023). A
  Kelly–Lochbaum waveguide with learnable area functions, fitted by gradient descent.
  Preview of course 3's question: *where does the network go?*
- **5.5** **Modular: DiffMoog** (Uzrad et al. 2024). A full differentiable modular
  synthesizer (oscillators, filters, envelopes, modulation) with a *signal-chain loss*
  on intermediate signals — and the bridge into course 2's sound-matching subject.
  Also the ISMIR *intro2ddsp* tutorial and `dasp-pytorch` as the practical toolkits.

## Phase 6 — Putting It Together
- **6.1** **The map, end-to-end**, on the note: every paper in `ddsp/` as a row of
  *(which block, which loss, which pathology, which fix)*. Recite the keystone from
  memory: both halves.
- **6.2** **Capstone — fit a differentiable synthesizer to the note.** Tiered like
  room-acoustics' a/b/c so it runs with or without a GPU:
  - **(a) CPU (default).** Hand-built harmonic+noise+reverb model from Phases 1–2;
    gradient-descent copy synthesis of the note with the multi-scale spectral loss;
    then edit the learned parameters (drop a harmonic, shorten the IR, change `f₀` for
    a transposition) and A/B listen. Write a one-page "block report": parameters,
    loss curve, what the ear says.
  - **(b) Colab GPU.** Train a small DDSP autoencoder (encoder → decoder → synth) on a
    few minutes of monophonic audio you have (or a public solo-instrument set); timbre
    transfer *the note* through it.
  - **(c) Local GPU.** Additionally fit a grey-box effect (a learnable biquad cascade or
    the Wright compressor) to a recorded effect on the note; compare IIR-BPTT,
    frequency-domain, and FIR-approximation training on the same target.
- **6.3** **Where to go next.** You can now read the DDSP review (Hayes et al. 2023)
  as a map. The keystone hands you off: *many parameters, one sound* → **course 2**
  (`audio-synth-effect-matching`); *the physical prior inside the block* → **course 3**
  (`audio-physics-informed`). Track A's `neural-audio-resynthesis` uses what you just
  built as the legible pole against learned latents.

## Phase 7 — The Frontier (a living section)
> **Revised as the field moves** — depth-on-demand, never a gate. Each item reuses the
> keystone (*which block, which loss*) on the same note. Claims here are empirical and
> fast-moving; the "Frontier sources" list below is the citation trail.
- **7.1** **Modulation discovery** (Mitcheltree et al. 2025): learn *interpretable*
  LFO/envelope curves instead of opaque framewise parameters — legibility pushed one
  level up.
- **7.2** **Training stability and symmetric parameter spaces**: gradient clipping for
  DDSP optimization (Han et al. 2025), and inversion as conditional density estimation
  under parameter-permutation symmetry (Hayes, Saitis, Fazekas 2025) — the current state
  of the "differentiable ≠ well-conditioned" story, taken up in full in course 2.
- **7.3** **Toolkits**: `dasp-pytorch` (differentiable audio signal processors) and the
  ISMIR *intro2ddsp* tutorial; what has become standard since Engel 2020.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with a picture or a *listen* before notation. The
   learner knows the DSP — spend the words on what autograd and the loss do to it.
   When notation lands, name it, say what it is in plain English, then say what it lets
   us compute.
3. **Pin it to the note.** Every block and every loss in this course can be run on the
   one through-line note and heard. Do that. Resynthesize and **listen** whenever a
   parameter changes — the ear is the oracle here, the way the 2-D scatter plot is in
   `flow-matching`.
4. **Tiny exercise** to verify: a few lines of `torch` (a forward pass, a `.backward()`,
   a loss sweep), a by-hand gradient or bitrate-style calculation, or a prediction
   ("shift `f₀` by 3 cents → waveform MSE goes ?") checked against a runnable cell.
5. **Common misreadings** when relevant — keep
   [`the-differentiable-block.md`](the-differentiable-block.md)'s list live; flag and
   correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in their own words in one or two sentences ("the spectral loss is
   phase-blind and multi-resolution, which is why the harmonic model trains and why
   waveform MSE doesn't").
2. Carry out the small computation: a forward pass with gradients, the loss sweep, a
   biquad fit, a copy-synthesis run — and explain each step.
3. Spot a deliberately wrong claim ("the DDSP decoder outputs audio samples" — no, it
   outputs *synthesizer parameters*; "make the reverb an FIR and IIR problems vanish" —
   no, you traded recursion for memory).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wiki this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Read / link these:

- **[`ddsp/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ddsp/wiki)** —
  the home wiki. Key pages: `overview.md` (the arc 2020→2024), `ddsp-framework.md`
  (components, losses, optimization challenges), `differentiable-audio-effects.md`
  (IIR/FIR/reverb/phaser/dynamics), `ddsp-review-taxonomy.md`,
  `midi-to-audio-synthesis.md`.
- **Source summaries** under `…/wiki/sources/`: `engel2020-ddsp`,
  `engel2020-pitch-detection`, `kuznetsov2020-differentiable-iir`, `steinmetz2020-automix`,
  `nercessian2021-biquads`, `lee2021-differentiable-reverb`, `wu2021-midi-ddsp`,
  `steinmetz2022-deepafx-st`, `caspe2022-ddx7-fm`, `renault2022-ddsp-piano`,
  `nercessian2022-microdynamics`, `wright2022-greybox-drc`, `bargum2023-allpass-alignment`,
  `carson2023-phaser`, `sudholt2023-vocal-tract`, `hayes2023-ddsp-review`,
  `uzrad2024-diffmoog`.
- **The compressor thread (Phase 4.5)** also lives in
  [`DRC/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/DRC) (the
  forward-model derivation, Zölzer Ch. 7) and the
  [`synth-effect-matching/wiki/drc-parameter-estimation.md`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/synth-effect-matching/wiki/drc-parameter-estimation.md)
  hub — course 2 inverts what this course models.

### DSP depth (the learner's own background — cite, don't re-derive)
JOS's books: [*Introduction to Digital Filters*](https://ccrma.stanford.edu/~jos/filters/)
(biquads, stability, frequency response — Phases 1.4, 4.1–4.3),
[*Spectral Audio Signal Processing*](https://ccrma.stanford.edu/~jos/sasp/) (STFT,
overlap-add, sinusoidal modeling, additive synthesis — Phases 1.2–1.5, 2.3, 3.1),
[*Physical Audio Signal Processing*](https://ccrma.stanford.edu/~jos/pasp/) (waveguides,
inharmonicity — Phases 5.2, 5.4, and all of course 3),
[*Mathematics of the DFT*](https://ccrma.stanford.edu/~jos/mdft/) if the FFT itself needs
a refresher.

### Source papers (the blocks this course tracks)
- **Engel, Hantrakul, Gu, Roberts (2020)** — *DDSP: Differentiable Digital Signal
  Processing*, ICLR 2020. The harmonic+noise synthesizer and multi-scale spectral loss.
- **Engel, Swavely, Roberts, Hantrakul, Hawthorne (2020)** — *Self-supervised Pitch
  Detection by Inverse Audio Synthesis*, ICML 2020 workshop.
- **Kuznetsov, Parker, Esqueda (2020)** — *Differentiable IIR Filters for Machine
  Learning Applications*, DAFx 2020.
- **Steinmetz, Pons, Pascual, Serrà (2020)** — *Automatic Multitrack Mixing with a
  Differentiable Mixing Console of Neural Audio Effects*. arXiv:2010.10291.
- **Nercessian, Sarroff, Werner (2021)** — hyperconditioned differentiable biquads for
  distortion modeling. arXiv:2103.08709.
- **Lee et al. (2021)** — *Differentiable Artificial Reverberation*.
- **Wu, Manilow, Deng, Swavely, Kastner, Cooijmans, Courville, Huang, Engel (2021)** —
  *MIDI-DDSP*, ICLR 2022. arXiv:2112.09312.
- **Steinmetz, Bryan, Reiss (2022)** — *Style Transfer of Audio Effects with
  Differentiable Signal Processing* (DeepAFx-ST). arXiv:2207.08759.
- **Caspe, Shier, Sandler (2022)** — *DDX7: Differentiable FM Synthesis of Musical
  Instrument Sounds*, ISMIR 2022. arXiv:2208.06169.
- **Renault, Mignot, Roebel (2022)** — *Differentiable Piano Model for MIDI-to-Audio
  Performance Synthesis*, DAFx 2022.
- **Nercessian et al. (2022)** — differentiable microdynamics processor, DAFx 2022.
- **Wright & Välimäki (2022)** — *Grey-Box Modelling of Dynamic Range Compression*,
  DAFx 2022.
- **Bargum et al. (2023)** — *Differentiable All-Pass Filters for Phase Response
  Estimation and Automatic Signal Alignment*. arXiv:2306.00860.
- **Carson et al. (2023)** — differentiable grey-box phaser with learned LFO.
  arXiv:2306.01332.
- **Sudholt et al. (2023)** — differentiable waveguide vocal tract. arXiv:2307.04702.
- **Hayes, Shier, Fazekas, McPherson, Saitis (2023)** — *A Review of Differentiable
  Digital Signal Processing for Music & Speech Synthesis*, Frontiers in Signal
  Processing. arXiv:2308.15422. **The map of the field — read last, as a summary.**
- **Uzrad, Barkan et al. (2024)** — *DiffMoog: a Differentiable Modular Synthesizer for
  Sound Matching*. arXiv:2401.12570.

### Frontier sources (Phase 7 — revised as the field moves)
- **Mitcheltree et al. (2025)** — *Modulation Discovery for DDSP*. arXiv:2510.06204.
- **Han et al. (2025)** — *Gradient Clipping for Improved Training in DDSP*, EUSIPCO 2025.
- **Hayes, Saitis, Fazekas (2025)** — *Audio Synthesizer Inversion in Symmetric
  Parameter Spaces with Approximately Equivariant Flow Matching*. arXiv:2506.07199.
- `dasp-pytorch` — github.com/csteinmetz1/dasp-pytorch; *intro2ddsp* —
  intro2ddsp.github.io.
