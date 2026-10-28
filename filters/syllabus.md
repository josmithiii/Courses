# Introduction to Digital Filters — From y(n) = x(n) + x(n−1) to the Research Frontier

**The book:** Julius O. Smith III, *Introduction to Digital Filters with Audio
Applications*, free online at **https://ccrma.stanford.edu/~jos/filters/**. Each topic below
names its book page(s) as `Page_Name`, and the full URL is
`https://ccrma.stanford.edu/~jos/filters/Page_Name.html`. The course follows the book's
chapter order and weaves the appendices in where they're needed, so the learner can read
the matching page before or after the session.

**Learner profile:** someone at the level of the `mdft` course's end state (the first book
in the series, *Mathematics of the DFT*, https://ccrma.stanford.edu/~jos/mdft/). That means
complex numbers and Euler's identity, sinusoids and phasors, the DFT and its theorems
(especially convolution), and a little numpy. **No hard gate:** a learner can plunge in and
backfill from `mdft` when a gap shows (the tutor names the exact `mdft` topic). From there
the course builds the whole of digital filter theory, introducing new mathematics just in
time: the z transform, partial fractions, the Laplace transform, circuits (capacitors and
inductors), matrices and state space. It ends at the current research literature on
filters (Phase 12). ~1 hour per day. One concept at a time. Every concept is checked with
a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position. Expect
~40-50 sessions for Phases 0-11, plus whatever of Phase 12 the learner wants.

**The keystone — the z-plane picture.** A linear time-invariant (LTI) filter can only
*scale and delay* each sinusoid passing through it; it can't create new frequencies.
So a filter is completely described by what it does to each frequency (its frequency
response). The z transform turns the filter's difference equation into a ratio of
polynomials H(z) = B(z)/A(z), and the roots of those polynomials, the **zeros** and
**poles**, decide everything:
- the frequency response is H(z) evaluated on the unit circle z = e^(jωT)
- the gain at a frequency is (product of distances to the zeros) ÷ (product of distances to
  the poles), measured from that point on the unit circle
- stability is "all poles strictly inside the unit circle"
- a pole's radius sets its bandwidth and decay time
- a zero's side of the unit circle sets minimum vs maximum phase
Every chapter from 6 on reads off this one picture; Phases 1-5 earn it.

**The pinned worked examples — four filters at f_s = 44100 Hz.** The way `mdft` returns
to one quarter-rate cosine and `sasp` to one A440 tone, this course returns to four small
filters:
- **The simplest lowpass** y(n) = x(n) + x(n−1) (chapter 1). One zero at z = −1. Gain
  2cos(πfT): 2 at DC, √2 (−3 dB) at f_s/4, 0 at f_s/2. Half a sample of delay.
- **The comb** (chapter 3) with M = 100 samples. Feedforward, y(n) = x(n) + x(n−100), has
  teeth every 441 Hz. Feedback, y(n) = x(n) + 0.9·y(n−100), has +20 dB peaks every 441 Hz
  and echoes that die away in ≈ 149 ms (the seed of plucked-string synthesis).
- **The A440 resonator:** two poles at 440 Hz with 20 Hz bandwidth, so R = e^(−πBT)
  ≈ 0.998576, decay time constant ≈ 15.9 ms and T60 ≈ 110 ms. It's the same A440 as the
  `sasp` course.
- **A Butterworth lowpass:** second order, f_c = 1 kHz, made from an analog prototype by
  the bilinear transform (appendix I).

The full canonical numbers are in `CLAUDE.md`. Every filter is *heard*: white noise,
clicks and a short music clip go through each one.

**The exercise bank:** `exercises/` holds 490 multiple-choice exercises from the
interactive online edition, one file per chapter, grouped by book page, each with hints,
answer and explanation (`exercises/index.md` lists them). They complement the tutor's own
derivations and numpy experiments. They never replace them.

**End state:** by the last core lesson the learner can:
- tell linear, time-invariant, causal and stable filters from the rest, and say why LTI
  filters only scale and delay sinusoids
- move freely between the representations of one filter: difference equation, signal
  flow graph, impulse response, transfer function, frequency response, pole-zero plot,
  state-space model
- compute amplitude, phase, phase delay and group delay, and sketch an amplitude response
  from a pole-zero plot by eye
- relate pole radius to bandwidth and decay time, and design resonators, combs, allpass
  filters, DC blockers, shelving filters and peaking equalizers
- choose an implementation structure (four direct forms, series and parallel sections)
  and explain the numerical trade-offs
- explain linear phase, zero phase (forward-backward filtering) and minimum phase, and
  convert a filter to minimum phase
- design IIR filters from analog prototypes (Butterworth via the bilinear transform,
  with prewarping) and by equation-error methods
- write a filter in Python, Octave and Faust (appendix K)
- read a current research paper on virtual-analog, differentiable or state-space
  filters and place it in the z-plane picture (Phase 12)

---

## Phase 0 — Orientation

- **0.1** What a filter is, as a story with no new notation: a tone control, an
  equalizer, the "wah" in a wah pedal, the body of a guitar, a room's echo. They all take
  a signal in and give a signal out, and they all *scale and delay* each frequency. Play
  white noise through a lowpass and a resonator and listen. Point to the free online book.
  (book: `Simplest_Lowpass_Filter`, `Introduction`)
- **0.2** Tools. Python with `numpy`, `scipy.signal` (`lfilter`, `freqz`, `tf2zpk`,
  `group_delay`, `residuez`, `butter`, `bilinear`), `matplotlib`, and a way to *hear*
  (Colab `IPython.display.Audio`, or `soundfile` + `sounddevice` locally in a uv `.venv`).
  **Octave option:** the book's Matlab runs in GNU Octave with the `signal` package (book
  appendix J, `Matlab_Utilities`). **Faust option:** the online Faust IDE needs no install
  (book appendix K). Verify: filter one second of noise with y(n) = x(n) + x(n−1) and hear
  it.
- **0.3** Sign conventions, checked once and for all. The book, Matlab/Octave and scipy
  all write y(n) = Σ b_i x(n−i) − Σ a_j y(n−j) with a_0 = 1, so H(z) = B(z)/A(z). The
  minus sign in front of the feedback terms is the classic trap. (book:
  `Signal_Representation_Notation`)

## Phase 1 — The Simplest Lowpass Filter (chapters 1-2, appendix A)

- **1.1** y(n) = x(n) + x(n−1) by ear and by sinusoid: feed it a sinusoid at frequency f
  and the output is the same sinusoid, scaled by 2cos(πfT) and delayed by half a sample.
  Done by trig identities first, the hard way. (book: `Simplest_Lowpass_Filter_I`,
  `Finding_Frequency_Response`, `Complex_Trigonometric_Identities`)
- **1.2** The easier way: feed it the complex sinusoid e^(jωnT) instead, factor it out,
  and the frequency response H(e^(jωT)) = 1 + e^(−jωT) drops out in one line. Why complex
  sinusoids are the *eigenfunctions* of LTI filters. (book: `Easier_Way`, `Summary`,
  `Sum_Sinusoids_Same_Frequency`, `Background_Fundamentals`)
- **1.3** Measure it numerically: sine-wave analysis in numpy (send sinusoids through
  `lfilter`, measure the output amplitude and phase), complex sine-wave analysis, then
  the practical method (`freqz`). Compare all three to 2cos(πfT). (book:
  `Matlab_Analysis_Simplest_Lowpass`, `Matlab_Filter_Implementation`,
  `Simulated_Sine_Wave_Analysis_Matlab`, `Complex_Sine_Wave_Analysis`,
  `Practical_Frequency_Response_Analysis`)

## Phase 2 — The Comb Filter: the Whole Book in One Example (chapter 3)

- **2.1** The comb y(n) = x(n) + g1·x(n−M1) − g2·y(n−M2) in all its representations:
  difference equation, signal flow graph, and code in Python, C++ and Faust. (book:
  `Analysis_Digital_Comb_Filter`, `Difference_Equation`, `Signal_Flow_Graph`,
  `Software_Implementation_Matlab`, `Software_Implementation_C`,
  `Software_Implementation_Faust`)
- **2.2** Its impulse response, transfer function, frequency, amplitude and phase
  response, and a first pole-zero analysis. On the pin (M = 100), the feedforward comb has
  teeth every 441 Hz and nulls at odd multiples of 220.5 Hz. The feedback comb with
  y(n) = x(n) + 0.9·y(n−100) peaks at +20 dB every 441 Hz. Hear both (flanging and a
  pitched buzz). *This chapter is a preview: every term gets a full treatment in Phases
  3-7.* (book: `Impulse_Response`, `Transfer_Function`, `Frequency_Response`,
  `Amplitude_Response_I`, `Phase_Response_I`, `Pole_Zero_Analysis`,
  `Alternative_Realizations`, `Summary_I`)

## Phase 3 — Linear Time-Invariant Filters (chapter 4)

- **3.1** Definitions of a signal and a filter, with examples of digital filters.
  **Linearity** (superposition and scaling) and **time invariance** (a delayed input gives
  a delayed output), and how to show each, or show it fails. (book:
  `Linear_Time_Invariant_Digital_Filters`, `Definition_Signal`, `Definition_Filter`,
  `Examples_Digital_Filters`, `Linear_Filters`, `Time_Invariant_Filters`,
  `Showing_Linearity_Time_Invariance`)
- **3.2** Filters that break the rules, on purpose: dynamic range compression (nonlinear)
  and a musical time-varying filter (a swept resonator). Why nonlinear filters are hard to
  analyze, and why this book stays LTI. (book: `Nonlinear_Filter_Example_Dynamic`,
  `Musical_Time_Varying_Filter_Example`, `Analysis_Nonlinear_Filters`, `Conclusions`)

## Phase 4 — Time-Domain Representations (chapter 5)

- **4.1** The difference equation, signal flow graphs, causal recursive filters, filter
  order, and the direct-form-I implementation (code it with a loop, then check it against
  `lfilter`). (book: `Time_Domain_Digital_Filter`, `Difference_Equation_I`,
  `Signal_Flow_Graph_I`, `Causal_Recursive_Filters`, `Filter_Order`,
  `Direct_Form_I_Implementation`)
- **4.2** The impulse response as a complete description, and **stability**: bounded
  input gives bounded output. Impulse response of the A440 resonator: a decaying 440 Hz
  ring. (book: `Impulse_Response_Representation`, `Filter_Stability`,
  `Impulse_Response_Example`)
- **4.3** What LTI implies: the output is the **convolution** of the input with the
  impulse response (`mdft` 6.5, now as a linear rather than circular sum). FIR filters,
  and transient vs steady-state response (the frequency response describes only the
  steady state). (book: `Implications_Linear_Time_Invariance`,
  `Convolution_Representation`, `Finite_Impulse_Response_Digital`,
  `Transient_Response_Steady_State`, `Summary_Conclusions`)
- **4.4** *(depth-on-demand)* Filters as matrices: causal and LTI filter matrices, the
  cyclic convolution matrix (the DFT diagonalizes it, which is `mdft`'s keystone again),
  inverse filters, and time-domain filter estimation by least squares (appendix F). (book:
  `Matrix_Filter_Representations`, `General_Causal_Linear_Filter`,
  `General_LTI_Filter_Matrix`, `Cyclic_Convolution_Matrix`, `Inverse_Filters`,
  `Time_Domain_Filter_Estimation`)

## Phase 5 — Transfer Function Analysis (chapter 6)

- **5.1** The **z transform** X(z) = Σ x(n) z^(−n): the DTFT with e^(jωT) replaced by any
  complex z. When it exists (region of convergence). The shift theorem (a delay of one
  sample is a multiplication by z^(−1)) and the convolution theorem. (book:
  `Transfer_Function_Analysis`, `Z_Transform`, `Existence_Z_Transform`,
  `Shift_Convolution_Theorems`, `Z_Transform_Convolution`)
- **5.2** The z transform of a difference equation gives H(z) = B(z)/A(z) in one step.
  Factored form, which names the poles and zeros (`np.roots`, `scipy.signal.tf2zpk`). Series
  and parallel combinations of transfer functions. (book:
  `Z_Transform_Difference_Equations`, `Factored_Form`, `Series_Parallel_Transfer_Functions`)
- **5.3** **Partial fraction expansion:** a recursive filter is a sum of one-pole (or
  two-pole) filters in parallel, each with an exponential impulse response
  (`scipy.signal.residuez`). Repeated poles. (book: `Partial_Fraction_Expansion`,
  `Partial_Fraction_Expansion_residuez_m`)

## Phase 6 — Frequency Response Analysis (chapter 7)

- **6.1** Frequency response = H(z) on the unit circle. Amplitude response G(ω) = |H|
  and phase response Θ(ω) = ∠H (unwrap before using it). The polar form. Frequency
  response as a ratio of DTFTs (and why measuring it that way needs care). (book:
  `Frequency_Response_Analysis`, `Frequency_Response_I`, `Amplitude_Response_I_I`,
  `Phase_Response_I_I`, `Polar_Form_Frequency_Response`, `Frequency_Response_Ratio_DTFTs`)
- **6.2** **Phase delay** (−Θ(ω)/ω, how far a sinusoid is delayed) vs **group delay**
  (−dΘ/dω, how far the *envelope* of a narrowband signal is delayed). The simplest
  lowpass has both equal to half a sample. The resonator's group delay peaks near 440 Hz.
  (book: `Phase_Group_Delay`, `Group_Delay_Computation_grpdelay_m`)

## Phase 7 — Pole-Zero Analysis (chapter 8): the keystone

- **7.1** Filter order = transfer function order. **Graphical amplitude response:** walk
  around the unit circle; gain = product of distances to zeros ÷ product of distances to
  poles. Sketch the four pins by eye, then check with `freqz`. **Graphical phase:** add the
  zero angles and subtract the pole angles. (book: `Pole_Zero_Analysis_I`,
  `Filter_Order_Transfer`, `Graphical_Amplitude_Response`,
  `Graphical_Phase_Response_Calculation`)
- **7.2** Stability revisited: causal and stable means every pole strictly inside the unit
  circle. Unstable poles, seen from the unit circle. (book: `Stability_Revisited`,
  `Unstable_Poles_Unit_Circle`)
- **7.3** **Bandwidth and time constant of one pole:** R = e^(−πBT), so B = −ln(R)/(πT),
  and τ ≈ T/(1−R) exactly −T/ln(R). Design the A440 resonator from (440 Hz, 20 Hz) to
  coefficients, then measure: −3 dB bandwidth 20.0 Hz, τ ≈ 15.9 ms, T60 ≈ 110 ms. Relate to
  `mdft`'s T60 and `sasp`'s A440. (book: `Bandwidth_One_Pole`, `Time_Constant_One_Pole`,
  `Relating_Pole_Radius_Bandwidth`)
- **7.4** *(depth-on-demand)* Poles and zeros of the cepstrum, conversion to minimum phase
  (reflect zeros inside the unit circle), and the Hilbert-transform relations between log
  magnitude and phase. (book: `Poles_Zeros_Cepstrum`, `Conversion_Minimum_Phase`,
  `Hilbert_Transform_Relations`)

## Phase 8 — Elementary Audio Filters (appendices B, C)

- **8.1** Elementary filter sections: one-zero, one-pole, two-pole, two-zero, and the
  **biquad** (two poles + two zeros, the workhorse of audio EQ). (book:
  `Elementary_Audio_Digital_Filters`, `Elementary_Filter_Sections`)
- **8.2** Allpass sections: unity gain at every frequency, but frequency-dependent delay
  (poles and zeros are mirror images about the unit circle). Phasers. Allpass examples,
  paraunitary and MIMO allpass filters (depth-on-demand). (book: `Allpass_Filter_Sections`,
  `Allpass_Filters`, `Allpass_Examples`, `Paraunitary_FiltersC_3`,
  `Multi_Input_Multi_Output_MIMO_Allpass`)
- **8.3** The DC blocker, low and high shelving filters, and **peaking equalizers**. Build
  a three-band EQ and hear it on music. (book: `DC_Blocker`, `Low_High_Shelf_Filters`,
  `Peaking_Equalizers`)
- **8.4** Time-varying two-pole filters: sweep the A440 resonator's frequency (a wah) and
  hear when coefficient changes click or misbehave. (book: `Time_Varying_Two_Pole_Filters`)

## Phase 9 — Implementation Structures (chapter 9, appendix K)

- **9.1** The four direct forms (DF-I, DF-II and their transposes): same transfer
  function, different internal signals, memory and roundoff behavior. (book:
  `Implementation_Structures_Recursive_Digital`, `Four_Direct_Forms`)
- **9.2** Series and parallel second-order sections (why high-order filters are never
  run as one big polynomial; `scipy.signal.sos`), parallel SOS back to a transfer function.
  (book: `Series_Parallel_Filter_Sections`, `Parallel_SOS_Transfer_Function`)
- **9.3** *(hands-on option)* The comb or biquad in **Faust**: a simple program, block
  diagrams, testing a filter section, the generated C++, and plugins. (book:
  `Digital_Filtering_Faust_PD`, `Simple_Faust_Program`, `Generating_Faust_Block_Diagrams`,
  `Testing_Faust_Filter_Section`, `Look_Generated_C_code`)

## Phase 10 — Phase: Linear, Zero and Minimum (chapters 10-11)

- **10.1** Linear-phase filters (symmetric impulse responses give constant delay) and
  zero-phase filters (even impulse responses, which are noncausal). Odd impulse
  responses; symmetric and antisymmetric linear-phase FIR filters. (book:
  `Filters_Preserving_Phase`, `Linear_Phase_Filters_Symmetric_Impulse`,
  `Zero_Phase_Filters_Even_Impulse`, `Odd_Impulse_Responses`,
  `Symmetric_Linear_Phase_Filters`, `Antisymmetric_Linear_Phase_Filters`)
- **10.2** **Forward-backward filtering** (`scipy.signal.filtfilt`): zero phase from any
  filter, offline only. Phase distortion at passband edges. (book:
  `Forward_Backward_Filtering`, `Phase_Distortion_Passband_Edges`)
- **10.3** Minimum-phase filters: all zeros inside the unit circle, and "minimum phase
  means fastest decay" (energy is packed into the start of the impulse response). Maximum
  phase. Minimum-phase/allpass decomposition. Linear-phase audio filters and when they're
  really ideal (pre-ringing). Creating minimum phase. (book: `Minimum_Phase_Filters`,
  `Definition_Minimum_Phase_Filters`, `Minimum_Phase_Polynomials`, `Maximum_Phase_Filters`,
  `Minimum_Phase_Means_Fastest`, `Minimum_Phase_Allpass_Decomposition`,
  `Linear_Phase_Really_Ideal`, `Creating_Minimum_Phase_Filters`)

## Phase 11 — Analog Roots, State Space and Design (appendices D, E, G, H, I)

- **11.1** *Calculus just in time:* the Laplace transform (the continuous-time z
  transform), its existence, analytic continuation, relation to the z transform (z = e^(sT)),
  theorems, and analysis of linear systems. (book: `Introduction_Laplace_Transform_Analysis`,
  `Existence_Laplace_Transform`, `Relation_z_Transform`, `Laplace_Transform_Theorems`,
  `Laplace_Analysis_Linear_Systems`)
- **11.2** Analog filters as circuits: capacitors, inductors, RC and RLC filter analysis,
  pole radius vs bandwidth, the quality factor Q, analog allpass filters. (book:
  `Analog_Filters`, `Example_Analog_Filter`, `Capacitors`, `Inductors`,
  `RC_Filter_Analysis`, `RLC_Filter_Analysis`, `Quality_Factor_Q`, `Analog_Allpass_Filters`)
- **11.3** **Recursive filter design:** lowpass specs, the Butterworth lowpass, and the
  **bilinear transform** s = (2/T)(1 − z^(−1))/(1 + z^(−1)) with frequency prewarping.
  Design the pin's 1 kHz second-order Butterworth and check −3 dB at 1 kHz. Equation-error
  design (fit a filter to a desired response by least squares). (book:
  `Recursive_Digital_Filter_Design`, `Lowpass_Filter_Design`, `Butterworth_Lowpass_Design`,
  `Digitizing_Analog_Filters_Bilinear`, `Filter_Design_Minimizing_L2`)
- **11.4** **State-space filters:** x(n+1) = A x(n) + B u(n), y(n) = C x(n) + D u(n). Markov
  parameters, response from initial conditions, transfer function, transposition, poles
  as eigenvalues of A, difference equations to state space, similarity transformations,
  the **modal representation** (diagonalize A to get parallel one-pole filters, which is
  partial fractions again), repeated poles, and the digital waveguide oscillator. (book:
  `State_Space_Filters`, `Markov_Parameters`, `Response_Initial_Conditions`,
  `Transfer_Function_State_Space`, `Transposition_State_Space_Filter`,
  `Poles_State_Space_Filter`, `Difference_Equations_State_Space`,
  `Similarity_Transformations`, `Modal_Representation`, `Repeated_Poles_I`,
  `State_Space_Analysis_Example_The`, `State_Space_Realization`)
- **11.5** *(depth-on-demand)* Linear time-varying filters (appendix H): what survives of
  the transfer-function picture when coefficients change with time. (book:
  `View_Linear_Time_Varying`, `Derivation`)
- **11.6** Putting it together. Re-derive the keystone unprompted: difference equation →
  z transform → poles and zeros → frequency response on the unit circle → stability,
  bandwidth, decay, phase type. Capstone (pick one; record the choice in `progress.md`):
  - **(a) A parametric EQ plugin:** low shelf + peaking + high shelf, as biquads in second-order
    sections, in Python and optionally in Faust, tested on music with plotted responses.
  - **(b) A plucked string from a comb:** the feedback comb with a lowpass in the loop
    (Karplus-Strong), tuned to A440, with decay times predicted from the pole radii and
    then measured. (A bridge to the PASP book.)
  - **(c) A filter-analysis report:** take a filter you didn't design (a guitar pedal tone
    stack's published circuit, or a `scipy` design) and present every representation
    from difference equation to state space, with pole-zero reasoning for each feature
    of its response.

## Phase 12 — The Frontier (a living section)

> **This phase tracks the current state of the art and is revised as the field moves.**
> It is depth-on-demand, never a gate. Each frontier topic is one session or more: it
> starts from the chapter it extends, reuses the keystone (poles and zeros relative to
> the unit circle), runs on a pin where possible, and ends by reading one paper from the
> sources list together. Claims marked *(empirical)* are benchmark results that later
> work may overturn. Last surveyed: **October 2026**.

- **12.1 Virtual-analog filters** (extends 11.2-11.3, 8.4). Zero-delay-feedback /
  topology-preserving-transform (TPT) design: apply the bilinear transform to each
  integrator of the analog circuit, not to the whole transfer function, so the digital
  filter keeps the circuit's structure and stays well behaved when its knobs move. The
  trapezoidal state-variable filter. Why a time-varying direct-form filter can go unstable
  even when every frozen-in-time version is stable.
- **12.2 Differentiable IIR filters** (extends 5-8). Make biquad coefficients (or pole
  and zero positions) trainable parameters, and fit them by gradient descent through a
  frequency-sampled or time-domain loss. This is neural EQ matching and filter design by
  learning. Parameterizing in the z-plane keeps stability by construction. → `audio-ddsp/`.
- **12.3 Filters as sequence models** (extends 11.4-11.5). Deep state-space models
  (S4, the Linear Recurrent Unit) are stacks of linear state-space filters whose poles are
  learned and kept inside the unit circle by parameterization (the LRU's diagonal complex
  poles are 11.4's modal representation exactly). Mamba makes the state-space filter
  *input-dependent*: a linear time-varying filter (11.5). → planned `ai-sequence-models`.
  *(empirical: which architecture wins depends on task and scale.)*
- **12.4 Grey-box and neural models of analog filter circuits** (extends 11.2, 11.4).
  State-space and recurrent networks trained to reproduce real analog filters and
  effects, and hybrids that keep a physical filter structure with learned nonlinear
  parts. → `audio-synth-effect-matching/`, `audio-physics-informed/`.
- **12.5 Toward physical models** (extends 2, 8.2, 11.6b). Wave digital filters
  (circuit-structured digital filters with guaranteed passivity) and digital waveguides
  (the feedback comb grown into strings and tubes). This is the subject of the next book
  in the series, *Physical Audio Signal Processing*
  (https://ccrma.stanford.edu/~jos/pasp/), and of the `pasp/` course, which starts where
  this one ends.

### Frontier sources
- Zavalishin, V. *The Art of VA Filter Design.* Native Instruments, online book (revised
  editions 2012-2020). *(Check the current revision before citing specifics.)*
- Laroche, J. (2007). On the stability of time-varying recursive filters. *J. Audio Eng.
  Soc.*, 55(6).
- Wishnick, A. (2014). Time-varying filters for musical applications. *DAFx-14.*
  *(Check the paper before teaching from it.)*
- Kuznetsov, B., Parker, J. D., & Esqueda, F. (2020). Differentiable IIR filters for
  machine learning applications. *DAFx2020.*
- Nercessian, S. (2020). Neural parametric equalizer matching using differentiable
  biquads. *DAFx2020.*
- Colonel, J. T., Steinmetz, C. J., Michelen, M., & Reiss, J. D. (2022). Direct design of
  biquad filter cascades with deep learning by sampling random polynomials. *ICASSP
  2022.*
- Gu, A., Goel, K., & Ré, C. (2022). Efficiently modeling long sequences with structured
  state spaces (S4). *ICLR 2022.*
- Orvieto, A., Smith, S. L., Gu, A., Fernando, A., Gulcehre, C., Pascanu, R., & De, S.
  (2023). Resurrecting recurrent neural networks for long sequences (LRU). *ICML 2023.*
- Gu, A., & Dao, T. (2023). Mamba: Linear-time sequence modeling with selective state
  spaces. arXiv:2312.00752.
- Wright, A., Damskägg, E.-P., & Välimäki, V. (2019). Real-time black-box modelling with
  recurrent neural networks. *DAFx-19.*
- Parker, J. D., Esqueda, F., & Bergner, A. (2019). Modelling of nonlinear state-space
  systems using a deep neural network. *DAFx-19.*
- Fettweis, A. (1986). Wave digital filters: Theory and practice. *Proc. IEEE*, 74(2),
  270-327.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question (a bank
   exercise from an earlier chapter makes good spaced review).
2. **Introduce one new concept** with an analogy/visual before any notation or code.
3. **Show**, then have the learner **do** a tiny exercise: a derivation, a pole-zero
   sketch, a few lines of numpy/scipy on a pin (and *listen* to it), or a bank exercise
   from `exercises/` for the current page.
4. **Verify** understanding from their answer; if shaky, re-explain a different way —
   do not advance until it's solid.
5. **Log** what was covered, the exercise, their answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
6. Keep each session ~1 hour. End with a one-sentence preview of next time, and point to
   the book page(s) to read before it.
