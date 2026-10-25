# Physics-Informed Audio Modeling — Modal, PINN, and Hybrid Models of One Plucked Note

**Learner profile:** Comfortable with JOS's *Introduction to Digital Filters* (poles,
biquads, stability) and the digital-waveguide / modal chapters of *Physical Audio Signal
Processing* (ccrma.stanford.edu/~jos/pasp/). Has `ai-foundations/` through Phase 2
(PyTorch tensors, autograd, the training loop) and ideally `audio-ddsp/` (course 1 —
spectral loss, gradients through DSP blocks). ODE/PDE comfort helps; the 1-D wave
equation is derived briskly with PASP as the reference. The learner is a DSP or
acoustics person who wants to know **where a neural network belongs inside a physical
model** — not a first encounter with either physics or networks. ~1 hour per day. One
concept at a time. Every concept verified with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**The keystone — read [`the-physical-prior.md`](the-physical-prior.md) in Phase 0.1.**
This course has one organizing idea: **the physical prior as inductive bias.** The
equations of motion fix the *form* of a vibrating object's response (modes with
constrained frequencies, decays, and shapes); a network learns only what the equations
leave out (excitation, nonlinearity, unmodeled losses, coupling). The design decision is
**where the network goes** — parameter-level, structure-level, residual-level,
loss-level, or architecture-level. Everything here builds toward being able to make that
decision for a new problem. We spend as long as it takes on Phases 3–5.

**The qubit (worked example):** the curriculum's shared **single plucked-string note**
(`../curricula/assets/audio-differentiable-dsp/note.wav`, mono 44.1 kHz, ~6 s). The
note is modeled **three ways** — (1) a modal resonator bank fitted to its measured
partials, (2) a PINN for the damped stiff-string equation compared against it, (3) a
hybrid physical core plus a learned excitation/residual — and all three are compared
**by ear and by spectral error**. The measured partials (`f_k`, `T60_k`, `a_k`) from
Phase 0.3 are the numbers every later phase reuses.

**End state:** by the last lesson the learner can: derive one mode from the eigenproblem
and implement it as a 2-pole resonator; state why a resonator bank and a waveguide are
the same linear system; explain how `E`, `ρ`, geometry, and stiffness `B` set the
partials and why damping is measured rather than predicted; fit a differentiable modal
bank to a recording with spectral loss and know what that fit does *not* guarantee;
write a PINN's loss for the damped stiff string and say precisely when a PINN beats and
loses to FEM; place a hybrid model's network at the right level and defend the choice;
and **compare the three models of the note by ear, by spectral error, and by what each
had to learn.**

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture**, no notation yet: a plucked string rings
  at partials the physics predicts; three ways to model it — a bank of resonators, a
  network trained on the wave equation, a physical core with a learned remainder. Read
  [`the-physical-prior.md`](the-physical-prior.md) — *where the network goes* is the
  destination. Where this course sits in the `audio-differentiable-dsp` curriculum (the
  physics end of Track C; the parametric/legible pole of Track A's resynthesis capstone).
- **0.2** **Tools.** `torch`, `numpy`, `scipy`, `matplotlib` importable; load the note,
  print shape and sample rate, **play it**, plot the waveform. If the note file is
  missing, **fail fast and say so** (see `CLAUDE.md`); the placeholder generator in
  `../curricula/assets/audio-differentiable-dsp/` is the sanctioned stand-in.
- **0.3** **Measure the partials — the numbers we reuse.** FFT of the note (and of
  successive 100 ms windows): peak-pick the first ~10–20 partials → `f_k`; fit each
  peak's decay across windows → `d_k` and `T60_k = 6.91 / d_k`; read `a_k` from the
  first window. Tabulate in `progress.md`. Check: is `f_k / f_1` an integer? (If not,
  that's stiffness — Phase 1.4 explains it.)

## Phase 1 — Modal Synthesis Fundamentals (PASP as the reference)
- **1.1** **Eigenmodes.** A linear vibrating system `M ẍ + C ẋ + K x = f`; drop damping,
  seek `x = φ e^{jωt}` → the generalized eigenproblem `K φ = ω² M φ`. Solutions:
  `(ω_k, φ_k)` pairs — natural frequencies and **mode shapes**. Orthogonality
  `φ_iᵀ M φ_j = 0`. For a 1-D ideal string: `φ_n(x) = sin(nπx/L)`, `f_n = n f_1`.
  Exercise: two masses + three springs, solve the 2×2 eigenproblem by hand.
- **1.2** **Damping.** Proportional (Rayleigh) damping `C = αM + βK` keeps the shapes
  real and gives each mode `d_k = (α + β ω_k²)/2`, `Q_k = ω_k / (2 d_k)`,
  `T60_k = 6.91 / d_k` (60 dB = 6.91 nepers). Non-proportional damping → complex modes;
  in practice **decay rates are measured per mode.** Why frequency is predictable and
  damping is not (material, boundary, radiation, thermoelastic losses; Q from ~5 for
  rubber to ~10⁴ for steel). Compare with the note's measured `T60_k`.
- **1.3** **Modal superposition → the resonator bank.** `x(t) = Σ_k q_k(t) φ_k`, each
  `q_k` obeying a decoupled 2nd-order ODE → **one mode = one decaying sinusoid = one
  2-pole resonator.** Digital form: pole angle `θ_k = 2π f_k / f_s`, pole radius
  `R_k = e^{-d_k / f_s}` (stable iff `d_k > 0`), gain `a_k = φ_k(r_excite) φ_k(r_pickup)`.
  N modes = N parallel biquads ≈ 5 MACs each per sample. **Pin to the note:** build a
  bank from the Phase 0.3 table in `numpy`, impulse it, **listen** next to the recording.
- **1.4** **Material and geometry → the partials.** `f_k ∝ √(E/ρ) / L`; scale the object
  by `s` → `f_k ∝ 1/s`. Stiffness makes the string **inharmonic**:
  `f_n = n f_1 √(1 + B n²)` — the piano/guitar stretch; fit `B` to the note's measured
  `f_k`. Material table (steel / aluminum / spruce / glass / rubber: `E, ρ, η`) and the
  perceptual map (hardness ↔ centroid and attack; size ↔ `f_1`; damping ↔ `T60`;
  inharmonicity ↔ "metallic"). Link out to PASP for the stiff-string derivation.
- **1.5** **Waveguide vs modal — one system, two coordinates.** Traveling waves (delay
  lines + loop filter) vs standing waves (resonator sum). For a lossless string they are
  *exactly* equivalent (Karplus–Strong = an N-mode sum); they differ in cost (`O(L)` vs
  `O(N)`), what is natural to control (pitch by delay length vs scaling `f_k`), and where
  nonlinearity is easy (at a junction vs in a feedback loop). **Commuted synthesis** as the
  source–filter shortcut: precompute `h(t) = Σ a_k e^{-d_k t} sin(2π f_k t)`, convolve.
  Exercise: run the note's Karplus–Strong placeholder and the modal bank side by side;
  match their pitch and decay; listen.

## Phase 2 — Where the Mode Parameters Come From
- **2.1** **Measure them: experimental modal analysis.** Impact hammer / shaker →
  accelerometer, laser vibrometer, or mic → FRF `H(f) = S_xy / S_xx` (H1 estimator) →
  fit `(f_k, d_k, a_k)`: peak picking + −3 dB bandwidth (crude), circle fitting, rational
  fraction polynomial / PolyMAX, and the signal-processing family (Prony, ESPRIT, MUSIC,
  sinusoidal modeling as in SMS). Model-order selection is the hard part. Above ~6–8 kHz
  modes are too dense → statistical energy analysis. Our Phase 0.3 peak-pick was the
  crude version; upgrade one partial's `d_k` with a proper decay fit.
- **2.2** **Compute them: FEM / BEM.** Mesh the object (≥ 6 elements per wavelength —
  millions of DOF for audio bandwidth in steel), assemble `M, K`, solve for the first N
  eigenpairs (Arnoldi/Lanczos, `O(N·DOF)`); BEM for radiation → **precomputed acoustic
  transfer** (James, Barbič & Pai 2006): per-mode, per-vertex transfer stored offline,
  `O(N_modes)` per sample at runtime. Reduced-order models: ~100–500 modes suffice.
  Tools named (FEniCS, Elmer, Bempp) — no install required; the point is the pipeline
  CAD + material → `{f_k, d_k, a_k}` → resonator bank.
- **2.3** **Excite them: impact.** Contact is not an impulse: **Hertz contact**
  `F = k_h δ^{3/2}`, a half-sine force pulse of duration `T_c` that **low-passes** the
  modes it excites (hard → short `T_c` → bright; rubber → long → dull). Modal response =
  each mode convolved with `F(t)`. Mode shapes at the contact point set `a_k`. Pin: shape
  the modal bank's excitation with a short raised-cosine pulse; hear the brightness change.
- **2.4** **Excite them: friction (preview of nonlinearity).** Bowing/rubbing is a
  velocity-dependent force fed *back* into the bank (Stribeck curve
  `μ_k F_N tanh(v/v_s) − b v`) → stick–slip → self-sustained oscillation. This is where
  the linear prior stops and why waveguides host bows more naturally. Intuition only.
- **2.5** **Data: RealImpact.** ~150 000 impact recordings, 50 objects, calibrated hammer
  force, mic-position sweeps, 3-D scans, impact-position labels (CC-BY 4.0,
  arXiv:2206.08524). What it enables (learn geometry+material → modes; evaluate synthesis
  against recordings) and its limits (50 objects; impact only; scan ≠ real surface). The
  capstone tier (c) can use it.

## Phase 3 — Learnable Physical Models (parameter-level prior)
> The prior lives in the *form*; the optimizer or a network supplies the parameters.
- **3.1** **The differentiable resonator bank.** Make `f_k, d_k, a_k` (or `θ_k, R_k, a_k`)
  `torch` parameters; run the bank; take a multi-scale spectral loss against the note
  (course 1's keystone reused). Stability by construction: parametrize `R_k = σ(·)` or
  `e^{-softplus(·)/f_s}`. IIR recursion is sequential — run it in the frequency domain
  (`H_k(e^{jω})` on an FFT grid) for GPU-friendly training, as the differentiable-IIR
  and grey-box literature does.
- **3.2** **Diaz, Hayes et al. 2023 — rigid-body synthesis with differentiable modal
  resonators.** A network maps a 2-D shape + material → a modal resonator bank (differentiable
  IIR filter bank), trained end-to-end in the audio domain; the first end-to-end
  "learn a physically-informed synthesizer from recordings" framework. Read its pipeline
  against the decision table. Companion: **DDSP-Piano** (Renault et al. 2022) puts the
  stiffness stretch `f_n = n f_1 √(1+Bn²)` and sympathetic-resonance extended pitch *into*
  a DDSP model — acoustic knowledge as architecture, fewer parameters, less data.
- **3.3** **The inverse direction — wav2shape** (Han & Lostanlen 2020): recover shape and
  material from drum-machine waveforms via time-frequency scattering + supervised
  regression; **Han's 2025 thesis** extends physical-parameter extraction to plucked
  strings with sim-to-real transfer. The precursors: Su & Liang 2002 (physical-model
  recurrent networks for plucked strings, parameters estimated from recordings) and
  Sterling & Bocko 2010 (empirical violin: waveguide string + measured bridge admittance
  + radiation; control estimation left open).
- **3.4** **What the fit does not guarantee.** Spectral loss has many-to-one valleys
  (course 2's keystone); gradient descent finds *a* bank matching the note, not the
  eigenmodes. Initialize from Phase 0.3's measured peaks; watch for mode swapping,
  dead modes, and `R_k → 1`. Compare fitted vs measured `f_k, T60_k` in a table.
- **3.5** **Pin to the note.** Fit the differentiable bank (N = 10–20 modes) to the note;
  **listen** to the resynthesis; plot fitted vs measured partials; record the numbers.

## Phase 4 — Physics-Informed Neural Networks (loss-level prior)
> The prior lives in the *loss*; the network is the solution.
- **4.1** **The idea (Raissi, Perdikaris & Karniadakis 2017/2019).** A network
  `u_θ(x, t)` takes coordinates in and gives the field out; **automatic differentiation**
  supplies `∂u/∂t, ∂²u/∂x²`; the loss is the **PDE residual** at collocation points plus
  boundary/initial-condition residuals:
  `L = (1/N_d) Σ ‖PDE(u_θ)‖² + (1/N_b) Σ ‖BC/IC‖² (+ data term)`. Mesh-free;
  resolution-independent inference. Raissi's numbers: 5–9 layers, 20–100 tanh units,
  Latin-hypercube collocation, L-BFGS.
- **4.2** **The damped stiff string as a PINN.** Write the PDE (PASP):
  `ρA u_tt = T u_xx − EI u_xxxx − 2ρA d u_t` with fixed ends; nondimensionalize; a
  plucked-triangle initial condition. Implement the residual in `torch` with
  `autograd.grad`; train; compare the PINN's `u(x_pickup, t)` spectrum with the note's
  measured `f_k` — do the partials and the stretch `B` come out? (Honest note: PINNs are
  known to struggle with oscillatory, multi-scale solutions — expect to need Fourier
  features / scaling tricks; record what it took.)
- **4.3** **Forward vs inverse.** Forward: known PDE, find `u` — **classical solvers win**
  on accuracy and usually speed; no convergence guarantees for PINNs. Inverse: unknown
  coefficients (here `B`, `d`), sparse/noisy data — jointly learn `u_θ` *and* the
  coefficients ("discovery"); this is where PINNs uniquely earn their keep. Pin: hide `B`
  and `d`, give the PINN the note's measured pickup signal as data, recover them.
- **4.4** **When to reach for a PINN, honestly.** Incomplete models, irregular or moving
  domains, parametric/multi-query settings (amortized cost), inverse problems. When not:
  a well-posed forward simulation you could run in FEM/FDTD. Gradient pathologies and
  the thinness of the audio PINN literature (one CCRMA survey in our wiki; "sound field
  simulation via PINNs" 2022) — say so.
- **4.5** **Neural operators — mention only.** Fourier Neural Operators (Li et al. 2020)
  put the prior in the *architecture* (learn the solution operator from data), the
  complement of the PINN's loss-level prior. One slide; Phase 7 returns to it.

## Phase 5 — Hybrid Physical / Neural Models (structure- and residual-level prior)
> The prior lives in the *structure*; the network fills in what the structure omits.
- **5.1** **A differentiable waveguide — vocal-tract area estimation by gradient descent**
  (Sudholt et al. 2023). Kelly–Lochbaum tract as a differentiable model; articulatory
  parameters → area function → frequency response; gradient descent on spectral
  distance to a recorded vowel; beats evolutionary and black-box-NN baselines. The
  cleanest "structure-level" example: the physics is the model, the network is the
  optimizer's target parametrization.
- **5.2** **Neural source–filter models** (Wang, Takaki & Yamagishi 2019). Keep the
  classical source–filter split; make the *filter* a network driven by a physical
  excitation (sine + noise source). One-shot (non-autoregressive) waveform generation —
  the residual-level pattern: physics supplies the excitation and the decomposition,
  the network supplies the rest.
- **5.3** **Grey-box modelling — the effects analogue** (Wright & Välimäki 2022). A
  compressor's *topology* (gain computer → level detector → make-up gain) fixed; the
  threshold/ratio/knee and attack/release ballistics learned end-to-end on LA-2A audio;
  interpretable after training and < 10 % of a black-box GRU's operations. Same bargain,
  different physics; ties to course 2's DRC thread.
- **5.4** **Learned prior + physical renderer — FDN reverb matching** (Götz et al. 2025).
  A learned room-acoustic embedding estimates parameters for a **feedback delay network**
  that reproduces frequency-dependent decay and direct-to-reverberant ratio in real time.
  The network *listens*; the physics *renders*.
- **5.5** **The decision — where does the network go?** Rebuild the decision table from
  memory with these five systems placed on it. Then design the note's hybrid: modal or
  waveguide core (Phase 1) + a learned excitation (short network output convolved in) +
  optionally a learned residual filter. Argue the level choice before building it.
- **5.6** **Pin to the note.** Build the hybrid; train excitation/residual against the
  note with the core's `f_k, d_k` frozen at measured values; **listen**; inspect what the
  network learned (is it a Hertz-like pulse? a body resonance?).

## Phase 6 — Putting It Together
- **6.1** **The note three ways, side by side.** Modal bank (form-prior), PINN
  (loss-prior), hybrid (structure-prior): for each, what the physics fixed, what was
  learned, spectral error vs the recording, and an A/B **listen**. Recite the keystone
  and the decision table from memory.
- **6.2** **Capstone — model the plucked note.** Tiered like room-acoustics' a/b/c so it
  runs with or without a GPU. **Fail fast, no fallbacks:** if an import, download, or
  dataset is missing, surface the real error and stop — never paper over it.
  - **(a) CPU (default).** Fit a differentiable modal bank to the note (Diaz–Hayes
    style, N ≈ 10–20 modes, multi-scale spectral loss, initialized from Phase 0.3 peaks).
    Resynthesize, A/B listen, and report a per-mode table of `f_k`, `T60_k`, `a_k`
    (fitted vs measured) plus the spectral error. One-page "modal report."
  - **(b) Colab GPU.** Tier (a), plus train a small PINN for the damped stiff string
    using the note's measured `f_1` and `B`; compare its pickup-signal spectrum with the
    note; then run it in **inverse mode** to recover `B` and `d` from the recording.
    Report what training tricks were needed and where accuracy fell short.
  - **(c) Local GPU.** Tier (a), plus the hybrid: frozen modal/waveguide core + learned
    excitation/residual network, trained on the note *or* on a RealImpact object (CC-BY
    4.0). Show what the residual learned (plot it, listen to it alone), and how much
    spectral error it removed relative to the pure modal fit.
- **6.3** **Where to go next.** You can now read Diaz & Hayes, Raissi, Sudholt, and
  Wright as an insider. Forward: Track A's `neural-audio-resynthesis` capstone (this
  course is its *legible* pole); `room-acoustics/` for the acoustics side; Han's 2025
  thesis for physical-parameter extraction at scale.

## Phase 7 — The Frontier (a living section)
> Revised as the field moves; depth-on-demand, never a gate. Each topic reuses the
> keystone (where does the prior go?) and pins to the note. **Honesty flag:** PINNs and
> neural operators *for musical acoustics* are thinly published as of authoring; most
> claims below are empirical and likely to move.
- **7.1** **Massive modal synthesis on GPU.** One thread per mode, tree reduction; ~60 000
  modes real-time on 2006 hardware, ~10⁵–10⁶ today; amplitude culling (95 %+ of modes
  inaudible at any instant); latency budget 0.5–2 ms. The form-prior at scale.
- **7.2** **Physicality of timbre — Han 2025.** PNP loss (100× speedup of perceptual
  loss), sim-to-real plucked-string parameter extraction, gesture–sound datasets. The
  parameter-level prior meeting real recordings.
- **7.3** **Neural operators for wave equations.** FNO and successors as
  architecture-level priors; open question from the `pinn` wiki: what role they play
  beside loss-level PINNs for instrument bodies and rooms.
- **7.4** **Open questions (from the `pinn` wiki).** Can PINNs reach classical accuracy
  on well-posed audio problems? How to scale to long, high-bandwidth simulations?
  Mesh-free geometry (bodies, halls) as the actual payoff.
- **Frontier sources:** `modal-synthesis/wiki/concepts/gpu-modal-synthesis.md`;
  `synth-effect-matching/wiki/sources/han-thesis-2025.md`;
  `pinn/wiki/overview.md` (open questions; FNO — Li et al. 2020; "sound field simulation
  via PINNs," Springer 2022).

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with a picture or a physical analogy *before* notation
   (a mode is a standing wave you can see on a string; damping is how long the bell
   rings). When notation lands, name it, say what it is in plain English, then say what
   it lets us compute.
3. **Pin it to the note.** Nearly every object here can be heard or plotted on the one
   plucked note: a mode, a decay, a stretch, a fitted bank, a PINN solution, a learned
   residual. Resynthesize and **listen** whenever a model changes — the ear is the
   oracle, with the spectral-error number as its witness.
4. **Tiny exercise** to verify: a hand eigenproblem, a `T60` from a decay rate, a
   `numpy` resonator, a `torch` residual, or a prediction ("stiffer string → ?") checked
   against a runnable cell.
5. **Common misreadings** when relevant — keep [`the-physical-prior.md`](the-physical-prior.md)'s
   list live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in their own words in one or two sentences ("a mode is a decoupled
   2nd-order ODE, so it's one 2-pole resonator with `R = e^{-d/f_s}`").
2. Carry out the small computation: a `T60` from `d_k`, a stiffness `B` from two
   partials, a resonator bank that plays, a PINN residual that runs — and explain each step.
3. Spot a deliberately wrong claim ("a PINN will out-simulate FEM on this string" — no,
   not for a well-posed forward problem; "modal = additive" — no, the eigenproblem
   constrains the sinusoids).
4. **Place a new system on the decision table** and defend the level.

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wikis this course teaches from
This course is the *pedagogical* front-end of curated knowledge bases; the wikis stay
canonical, the course stays pedagogical. **Honesty about the sources:** the
`modal-synthesis` wiki contains **concept pages only — no PDFs** (it was generated by an
agent and edited by JOS); the `pinn` wiki has **a single source**, Soohyun Kim's CCRMA
survey presentation (Dec 2023). The derivations this course relies on live in JOS's
*Physical Audio Signal Processing*; the learnable/hybrid papers live in the sibling
`synth-effect-matching` and `ddsp` wikis. Read / link (public prefix
`https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/`):

- **`modal-synthesis/wiki/`** — Phases 1–2, 7.1. Key pages: `concepts/modal-synthesis-overview.md`,
  `concepts/mode-shapes-and-eigenvalues.md`, `concepts/resonator-bank-implementation.md`,
  `concepts/material-properties-and-modes.md`, `concepts/modal-analysis-measurement.md`,
  `concepts/fem-bem-for-modal-synthesis.md`, `concepts/impact-synthesis.md`,
  `concepts/friction-synthesis.md`, `concepts/rigid-body-sound-synthesis.md`,
  `concepts/gpu-modal-synthesis.md`, `comparisons/waveguide-vs-modal.md`,
  `entities/realimpact-dataset.md`.
- **`pinn/wiki/`** — Phase 4, 7.3–7.4: `overview.md`, `physics-informed-neural-networks.md`,
  `sources/pinn-soohyun-kim.md`.
- **`synth-effect-matching/wiki/sources/`** — Phases 3, 5, 7.2: `diaz-hayes-rigid-body-icassp23`,
  `wav2shape-2020`, `su-rnn-strings-2002`, `sterling-bowed-string-2010`,
  `neural-source-filter-2019`, `fdn-reverb-matching-2025`, `han-thesis-2025`.
- **`ddsp/wiki/sources/`** — Phases 3.2, 5.1, 5.3: `sudholt2023-vocal-tract`,
  `renault2022-ddsp-piano`, `wright2022-greybox-drc`.
- **JOS's books** — *Physical Audio Signal Processing* (ccrma.stanford.edu/~jos/pasp/):
  digital waveguides, the stiff string and inharmonicity, modal synthesis, commuted
  synthesis; *Introduction to Digital Filters* (ccrma.stanford.edu/~jos/filters/): poles,
  resonators, stability. Cited, not re-derived.

### Source papers (the systems this course tracks)
- **Raissi, Perdikaris, Karniadakis (2017)** — *Physics Informed Deep Learning* Parts I & II.
  arXiv:1711.10561, arXiv:1711.10566. **(2019)** — *Physics-informed neural networks*,
  J. Comput. Phys. 378.
- **Kim (2023)** — *PINN*, CCRMA Music 423 presentation (survey; the `pinn` wiki's one source).
- **Diaz, Hayes et al. (2023)** — *Rigid Body Sound Synthesis with Differentiable Modal
  Resonators*, ICASSP 2023.
- **Renault, Mignot, Roebel (2022)** — *Differentiable Piano Model for MIDI-to-Audio
  Performance Synthesis*, DAFx 2022.
- **Han, Lostanlen (2020)** — *wav2shape: Hearing the Shape of a Drum Machine*. arXiv:2007.10299.
- **Han (2025)** — *Unearthing the Physicality of Instrumental Timbre*, Ph.D. thesis, ECN/LS2N.
- **Su, Liang (2002)** — *A Class of Physical Modeling Recurrent Networks for Analysis/Synthesis
  of Plucked String Instruments*, IEEE TNN 13(5).
- **Sterling, Bocko (2010)** — *Empirical Physical Modeling for Bowed String Instruments*, ICASSP 2010.
- **Sudholt, Cámara, Xu, Reiss (2023)** — *Vocal Tract Area Estimation by Gradient Descent*, DAFx 2023.
- **Wang, Takaki, Yamagishi (2019)** — *Neural Source-Filter Waveform Models*. arXiv:1904.12088.
- **Wright, Välimäki (2022)** — *Grey-Box Modelling of Dynamic Range Compression*, DAFx 2022.
- **Götz, Dal Santo, Schlecht, Välimäki, Habets (2025)** — *Matching Reverberant Speech through
  Learned Acoustic Embeddings and Feedback Delay Networks*. arXiv:2510.23158.
- **Georg et al. (2022)** — *RealImpact: A Dataset of Impact Sound Fields for Real Objects*.
  arXiv:2206.08524 (as recorded in the `modal-synthesis` wiki).
- **James, Barbič, Pai (2006)** — *Precomputed Acoustic Transfer*, SIGGRAPH 2006 (Phase 2.2; via the wiki).
- **Li et al. (2020)** — *Fourier Neural Operator* (Phase 4.5, mention only; via the `pinn` wiki).
