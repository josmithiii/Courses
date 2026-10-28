# Mathematics of the DFT — From the Quadratic Formula to Spectrum Analysis

**The book:** Julius O. Smith III, *Mathematics of the Discrete Fourier Transform (DFT),
with Audio Applications*, 2nd ed. It's free online at
**https://ccrma.stanford.edu/~jos/mdft/**. Each topic below names its book page(s) as
`Page_Name`, and the full URL is `https://ccrma.stanford.edu/~jos/mdft/Page_Name.html`. The
course follows the book's own path, so the learner can read the matching page before or
after the session.

**Learner profile:** a **high-school student who is good at math**, or any adult with that
background. Assume algebra and some trigonometry (sine, cosine, the unit circle). Assume
**no** calculus, complex numbers, linear algebra or signal processing. The book was written
to be self-contained from that level, and the course keeps that promise: every idea beyond
high-school algebra is built here, just in time. So: a picture or analogy first, notation
named the moment it appears, and every abstract object tried out on a tiny example small
enough to do by hand. ~1 hour per day. One concept at a time. Every concept is checked with
a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position. Expect
~35-45 sessions for Phases 0-9.

**The keystone — the DFT is a change of coordinates.** A list of N numbers (a signal) is a
vector, an arrow in N-dimensional space. The N sampled complex sinusoids
s_k(n) = e^(j2πkn/N) are N mutually perpendicular (orthogonal) arrows. The DFT value X(k) is
the inner product ⟨x, s_k⟩, which measures *how much of sinusoid k is in x* (the
coefficient of projection, times N). The inverse DFT rebuilds x by adding those projections
back up. Everything in Phases 1-3 is built to make "sampled complex sinusoid" mean
something. Phase 4 (geometry) and Phase 5 (the DFT derived) are the heart of the course.
Everything after (the theorems, spectrum analysis, the FFT) applies this one picture.

**The pinned worked example — one cosine at a quarter of the sampling rate.** The way
other courses here return to one qubit or one shoebox room, this course returns to
**x(n) = cos(2π n/4)**, a cosine that completes one cycle every 4 samples:

- **N = 2** (the geometry warm-up, Phase 4): the signal x = [3, 1] as an arrow in the
  plane, projected onto [1, 1] and [1, −1]: x = 2·[1, 1] + 1·[1, −1]. That *is* the
  length-2 DFT: X = [x0 + x1, x0 − x1] = [4, 2].
- **N = 4** (by hand, Phase 5): the DFT sinusoids are built from powers of j, so there are
  no messy decimals. x = [1, 0, −1, 0] gives **X = [0, 2, 0, 2]**: one cosine, *two* peaks
  (positive and negative frequency).
- **N = 64** (numpy, Phase 7): the book's first spectrum-analysis example. Peaks of
  **32 = N/2** at bins 16 and 48. Then the cosine is nudged half a bin off
  (f = 0.25 + 0.5/64) and *leakage* appears.

The full canonical numbers are in `CLAUDE.md`.

**The exercise bank:** `exercises/` holds 425 multiple-choice exercises from the
interactive online edition, one file per chapter, grouped by book page, each with hints,
answer and explanation (`exercises/index.md` lists them). They complement the tutor's own
by-hand and coding exercises. They never replace them.

**End state:** by the last lesson the learner can:
- do arithmetic with complex numbers in both rectangular and polar form, and prove (not
  just quote) Euler's identity e^(jθ) = cos θ + j sin θ
- describe any sinusoid by amplitude, frequency and phase, explain why a real cosine is
  the sum of two counter-rotating complex sinusoids, and read a decay time in dB
- treat signals as vectors: norms, inner products, orthogonality, projection, and
  reconstruction from projections
- derive the DFT from the orthogonality of sampled complex sinusoids, compute small DFTs
  by hand, and convert between bin number k and frequency in Hz
- state and use the main Fourier theorems (shift, convolution, correlation, power/Parseval,
  stretch, aliasing, zero padding) and say why DFT shifts and convolutions are *circular*
- run a practical spectrum analysis in numpy (or Octave), with windowing, zero padding and
  a dB scale, and interpret the result honestly
- explain why the FFT is fast, and how the DFT relates to the DTFT, Fourier transform and
  Fourier series, and to sampling

---

## Phase 0 — Orientation

- **0.1** What the DFT is for, as a story with no notation: a chord goes in, the notes in
  it come out. The DFT turns *a list of samples over time* into *a list of how much of each
  frequency*. Show a spectrum of a real sound (a plucked string, a whistle, a chord) and
  point at the peaks. Point to the free online book and how to use its pages alongside the
  course. (book: `Introduction_DFT`, `DFT_Definition`)
- **0.2** Set up the tools. **numpy first**: Python with `numpy` and `matplotlib`, either
  zero-install in **Google Colab** (best for most students) or locally with `uv`
  (`uv venv .venv && uv pip install numpy matplotlib`). **Octave option:** GNU Octave runs
  the book's own Matlab examples unchanged (book appendix I, `Matlab_Octave_Examples`).
  Verify: plot 16 samples of `cos(2*pi*n/4)` as dots. *(Flag on first sight that numpy
  writes the imaginary unit as `1j` and the book writes j.)*
- **0.3** A mystery to earn. Run `np.fft.fft([1, 0, -1, 0])` and get `[0, 2, 0, 2]`. Why
  two 2s for one cosine? Why 2 and not 1? Why is one of them at "bin 3"? Write the
  questions down in `progress.md`. By Phase 5.4 the learner computes this by hand and can
  answer all three. (book: `DFT_Math_Outline` is the route map.)

## Phase 1 — Complex Numbers (book chapter 2)

- **1.1** Why we need them. Factoring a polynomial; the quadratic formula; x² + 1 = 0 has
  no real root, so *invent* one: j with j² = −1 (engineers write j because i means current;
  math class writes i). Complex roots come in conjugate pairs. The Fundamental Theorem of
  Algebra: a degree-N polynomial has exactly N roots, counted in ℂ. (book:
  `Factoring_Polynomial`, `Quadratic_Formula`, `Complex_Roots`,
  `Fundamental_Theorem_Algebra`)
- **1.2** The complex plane. z = x + jy is a point (an arrow) with a real part and an
  imaginary part. Magnitude |z| = √(x² + y²) (Pythagoras) and angle ∠z (use `atan2`, not
  `atan`, so the quadrant comes out right). Polar form z = r(cos θ + j sin θ). (book:
  `Complex_Basics`, `Complex_Plane`, `More_Notation_Terminology`)
- **1.3** Arithmetic. Adding complex numbers adds the arrows. Multiplying them
  *multiplies magnitudes and adds angles*. This one fact is the engine of the whole course,
  so have the learner check it numerically on two examples. Conjugate z̅ = x − jy is the
  mirror image, and z·z̅ = |z|². Division by multiplying through by the conjugate.
  (book: `Elementary_Relationships`)
- **1.4** Euler's identity *stated* (proved in Phase 2) and De Moivre's theorem
  (cos θ + j sin θ)^n = cos nθ + j sin nθ, checked for n = 2 against the double-angle
  formulas the learner already knows. Multiplying by j is a quarter turn. (book:
  `Euler_s_Identity`, `De_Moivre_s_Theorem`)

## Phase 2 — Why e? Proving Euler's Identity (chapter 3, appendix E)

- **2.1** What an exponent *means*, extended step by step: positive integers (repeated
  multiplication) → the rules a^(m+n) = a^m·a^n → forced definitions for 0, negative and
  rational exponents → real exponents by filling in the gaps. The theme: each extension is
  chosen so the rules keep working. That same move gives imaginary exponents in 2.4.
  (book: `Positive_Integer_Exponents`, `Properties_Exponents`, `Exponent_Zero`,
  `Negative_Exponents`, `Rational_Exponents`, `Real_Exponents`)
- **2.2** Just enough calculus: the derivative as the slope of a curve. The derivative of
  a^x is proportional to a^x itself, and e ≈ 2.71828 is the one base where the constant is
  exactly 1. That is why e and not 10. (book: `Derivatives_f_x_power`, `Back_e`)
- **2.3** A first look at Taylor series: a smooth function rebuilt from its value and
  slopes at one point. Write out the series for e^x, cos x and sin x; check numerically that
  a few terms already get close. (book: `First_Look_Taylor_Series`, appendix
  `Taylor_Series_Expansions`)
- **2.4** Imaginary exponents. Put jθ into the series for e^x, sort the terms by powers
  of j (which cycle j, −1, −j, 1), and out come the series for cos θ and j sin θ:
  **e^(jθ) = cos θ + j sin θ.** Then e^(jπ) = −1. (book: `Imaginary_Exponents`,
  `e_j_theta`)
- **2.5** Roots of unity: the N solutions of z^N = 1 are e^(j2πk/N), equally spaced
  around the unit circle. **For N = 4 they are 1, j, −1, −j: the DFT's whole alphabet at
  the course's pinned size.** Plot them for N = 4 and N = 8. De Moivre, proved directly from
  Euler. (book: `Back_Mth_Roots`, `Roots_Unity`, `Direct_Proof_De_Moivre_s`)

## Phase 3 — Sinusoids and Exponentials (chapter 4, appendix F)

- **3.1** The sinusoid A cos(ωt + φ): amplitude A, radian frequency ω = 2πf (f in Hz),
  phase φ. Why sinusoids are everywhere: they are what linear time-invariant systems (rooms,
  strings, filters) pass through unchanged in shape. In-phase and quadrature components.
  Two sinusoids at the same frequency add to a third at that frequency
  (constructive/destructive interference). (book: `Sinusoids`, `Example_Sinusoids`,
  `Why_Sinusoids_Important`, `In_Phase_Quadrature_Sinusoidal`,
  `Sinusoids_Same_Frequency`, `Constructive_Destructive_Interference`)
- **3.2** Exponentials and decibels. e^(−t/τ) with time constant τ. Audio decay time T60
  (time to fall 60 dB). Introduce dB here: 20 log10 of an amplitude ratio, so 60 dB is a
  factor of 1000 in amplitude. (book: `Exponentials`, `Audio_Decay_Time_T60`, appendix
  `Logarithms`, `Decibels`, `Properties_DB_Scales`)
- **3.3** Complex sinusoids are circular motion: e^(jωt) goes around the unit circle.
  Its shadow on the real axis is cos ωt; on the imaginary axis, sin ωt. **Positive and
  negative frequencies:** cos ωt = (e^(jωt) + e^(−jωt))/2, two counter-rotating arrows whose
  imaginary parts cancel. *This is the first answer to the 0.3 mystery ("two peaks").*
  Plotting complex sinusoids versus frequency (the first spectrum pictures). (book:
  `Complex_Sinusoids`, `Circular_Motion`, `Projection_Circular_Motion`,
  `Positive_Negative_Frequencies`, `Plotting_Complex_Sinusoids_versus`)
- **3.4** *(depth-on-demand)* AM and FM as sums and wiggles of complex sinusoids; analytic
  signals and the Hilbert transform. Musically motivated (tremolo, vibrato, FM synthesis).
  (book: `Sinusoidal_Amplitude_Modulation_AM`, `Sinusoidal_Frequency_Modulation_FM`,
  `Analytic_Signals_Hilbert_Transform`)
- **3.5** Sampled sinusoids. Sampling at rate f_s means t = nT with T = 1/f_s. A sampled
  complex sinusoid is the sequence of powers z^n, with z = e^(jωT). Generalized complex
  sinusoids (growing and decaying spirals); the analog s-plane versus the digital z-plane;
  phasors and carriers. (book: `Generalized_Complex_Sinusoids`, `Sampled_Sinusoids`,
  `Powers_z`, `Phasor_Carrier_Components_Sinusoids`, `Comparing_Analog_Digital_Complex`)
  *Aliasing preview:* the frequencies f and f + f_s give the *same* samples. Full story in
  8.4; pull it forward if the learner asks.

## Phase 4 — Geometric Signal Theory (chapter 5): the keystone, part 1

- **4.1** Signals as vectors. A length-N signal is an arrow in N-dimensional space. Start
  at **N = 2** and draw x = [3, 1] in the plane. Vector addition, subtraction, scalar
  multiplication, linear combinations, vector spaces. (book: `Signals_Vectors`,
  `Example_Vector_View`, `Vector_Addition`, `Scalar_Multiplication`,
  `Linear_Combination_Vectors`, `Linear_Vector_Space`)
- **4.2** Signal metrics. Energy Σ|x(n)|², power, RMS, the norm ‖x‖ as arrow length; other
  L_p norms; norm properties. Connect to the audio meaning (loudness, dB of a signal).
  (book: `Signal_Metrics`, `Other_Lp_Norms`, `Norm_Properties`)
- **4.3** The inner product ⟨x, y⟩ = Σ x(n) y̅(n). For real vectors it's the dot product.
  The conjugate is there so that ⟨x, x⟩ = ‖x‖² is real and non-negative. Cauchy-Schwarz,
  the vector cosine, **orthogonality** (⟨x, y⟩ = 0), and the Pythagorean theorem in
  N-space. (book: `Inner_Product`, `Linearity_Inner_Product`,
  `Norm_Induced_Inner_Product`, `Cauchy_Schwarz_Inequality`, `Vector_Cosine`,
  `Orthogonality`, `Pythagorean_Theorem_N_Space`)
- **4.4** **Projection.** The projection of x onto y is (⟨x, y⟩/‖y‖²)·y, "the shadow of x
  along y". It is also the best least-squares approximation of x by a multiple of y. On the
  pin: project [3, 1] onto [1, 1] (coefficient 2) and onto [1, −1] (coefficient 1).
  (book: `Projection`, `Least_Squares_Approximation`)
- **4.5** **Reconstruction from projections.** When the basis arrows are mutually
  orthogonal, adding the projections gives back x exactly: [3, 1] = 2·[1, 1] + 1·[1, −1].
  Changing coordinates. Show it *fails* for linearly dependent or non-orthogonal vectors
  (that's why orthogonality matters). Gram-Schmidt is depth-on-demand. **Reveal: the
  N = 2 case just done is the length-2 DFT.** (book: `Signal_Reconstruction_Projections`,
  `Changing_Coordinates`, `Projection_onto_Linearly_Dependent`,
  `Projection_onto_Non_Orthogonal_Vectors`, `General_Conditions`,
  `Gram_Schmidt_Orthogonalization`)

## Phase 5 — The DFT Derived (chapter 6): the keystone, part 2

- **5.1** The geometric series 1 + z + … + z^(N−1) = (1 − z^N)/(1 − z), for z ≠ 1. Derive
  it (multiply by z and subtract). It's the one tool the orthogonality proof needs.
  (book: `Geometric_Series`)
- **5.2** The DFT sinusoids s_k(n) = e^(j2πkn/N), k = 0 … N−1, built from the Nth roots of
  unity. **At N = 4, write all four out:** s_0 = [1, 1, 1, 1], s_1 = [1, j, −1, −j],
  s_2 = [1, −1, 1, −1], s_3 = [1, −j, −1, j]. Point out that s_3 is s_1 running backwards
  around the circle (a negative frequency). (book: `Orthogonality_Sinusoids`,
  `Nth_Roots_Unity`, `DFT_Sinusoids`)
- **5.3** They are orthogonal (prove it with the geometric series, then check
  ⟨s_1, s_3⟩ = 0 by hand at N = 4), each has norm √N, and dividing by √N makes them an
  orthonormal set. (book: `Orthogonality_DFT_Sinusoids`, `Norm_DFT_Sinusoids`,
  `Orthonormal_Sinusoidal_Set`)
- **5.4** **The DFT.** X(k) = ⟨x, s_k⟩ = Σ x(n) e^(−j2πkn/N). The minus sign comes from
  the conjugate in the inner product. The inverse x(n) = (1/N) Σ X(k) e^(j2πkn/N) is the sum
  of projections. **Compute X for x = [1, 0, −1, 0] by hand: [0, 2, 0, 2].** Now answer all
  three 0.3 questions: two peaks = ±frequency; 2 = A·N/2; bin 3 = bin −1 (indices wrap mod
  N). Check the inverse rebuilds x. (book: `Discrete_Fourier_Transform_DFT`)
- **5.5** Frequency bookkeeping. Bin k means frequency k·f_s/N Hz. Bins above N/2 are
  negative frequencies. Example: f_s = 44100 Hz, N = 1024 gives ≈ 43.07 Hz per bin. A
  sinusoid "in the cracks" between bins spreads over all bins (a preview of leakage, 7.2).
  The Fourier series as a special case. (book: `Frequencies_Cracks`,
  `Spectral_Bin_Numbers`, `Fourier_Series_Special_Case`)
- **5.6** The normalized DFT (1/√N on both sides keeps lengths equal), the length-2 DFT
  revisited, and the DFT as a matrix-times-vector product. Teach just enough matrix
  multiplication first (appendix H) and build the 4×4 DFT matrix by hand. (book:
  `Normalized_DFT`, `Length_2_DFT`, `Matrix_Formulation_DFT`, appendix `Matrices`)

## Phase 6 — Fourier Theorems for the DFT (chapter 7)

- **6.1** The DFT restated; notation; **modulo indexing and periodic extension.** To the
  DFT a length-N signal is one period of a repeating signal, so index −1 *is* index N−1.
  This is why DFT shifts and convolutions are circular. (book: `DFT_Inverse_Restated`,
  `Notation_Terminology`, `Modulo_Indexing_Periodic_Extension`)
- **6.2** Signal operators: flip, (circular) shift, **convolution**, correlation, stretch,
  zero padding (and causal zero padding), repeat, downsample, alias. Do each on a length-4
  example by hand. (book: `Signal_Operators`, `Operator_Notation`, `Flip_Operator`,
  `Shift_Operator`, `Convolution`, `Correlation`, `Stretch_Operator`, `Zero_Padding`,
  `Causal_Zero_Padding`, `Repeat_Operator`, `Downsampling_Operator`, `Alias_Operator`)
- **6.3** Even and odd functions; symmetry. A real signal has a **Hermitian** spectrum,
  X(−k) = X̅(k). That's why [0, 2, 0, 2] is mirror-symmetric, and why audio spectra are
  usually plotted from 0 to f_s/2 only. (book: `Even_Odd_Functions`, `Symmetry`)
- **6.4** Linearity, conjugation and reversal, and the **shift theorem**: delaying x by Δ
  samples multiplies X(k) by e^(−j2πkΔ/N), a linear phase. On the pin: delay [1, 0, −1, 0]
  by one sample to get [0, 1, 0, −1], whose DFT is [0, −2j, 0, 2j]. Same magnitudes, rotated
  phases. (book: `Fourier_Theorems`, `Linearity`, `Conjugation_Reversal`, `Shift_Theorem`)
- **6.5** The **convolution theorem**: circular convolution in time equals multiplication
  of spectra. This is the most-used theorem in practice. Its dual: multiplication in time
  is convolution in frequency (the seed of windowing, 7.4). (book: `Convolution_Theorem`,
  `Dual_Convolution_Theorem`)
- **6.6** Correlation theorem; power theorem; **Rayleigh/Parseval**: energy in time equals
  energy in frequency (divided by N). On the pin: Σ x² = 2 and (1/4)(2² + 2²) = 2.
  (book: `Correlation_Theorem`, `Power_Theorem`, `Rayleigh_Energy_Theorem_Parseval_s`)
- **6.7** Stretch/repeat, downsampling/aliasing, and **zero padding = ideal spectral
  interpolation**: more points on the *same* underlying curve, not more resolution.
  Interpolation theorems. (book: `Stretch_Theorem_Repeat_Theorem`,
  `Downsampling_Theorem_Aliasing_Theorem`, `Zero_Padding_Theorem_Spectral`,
  `Ideal_Spectral_Interpolation`, `Interpolation_Operator`,
  `Periodic_Interpolation_Spectral_Zero`)

## Phase 7 — DFT Applications (chapter 8)

- **7.1** Spectrum analysis of the pin at N = 64 (the book's first example, ported to
  numpy): f = 0.25 cycles/sample gives peaks of **32 = N/2** at bins 16 and 48, zero
  elsewhere. Linear and dB plots. Why "a DFT is usually called an FFT in practice."
  (book: `Why_DFT_usually_called`, `Spectrum_Analysis_Sinusoid_Windowing`,
  `FFT_Simple_Sinusoid`)
- **7.2** The not-so-simple sinusoid: f = 0.25 + 0.5/64 sits halfway between bins 16 and
  17. Now the peaks are ≈ 20.4 (−3.9 dB) and *every* bin is nonzero (≈ −26 dB far away).
  **Leakage is not an FFT error**: the cosine doesn't complete a whole number of cycles in
  N samples, so its periodic extension has a jump. (book: `FFT_Not_So_Simple_Sinusoid`)
- **7.3** Zero padding to see the underlying continuous spectrum (the DTFT samples
  between bins). Zero padding interpolates; it does not resolve two close sinusoids.
  (book: `FFT_Zero_Padded_Sinusoid`)
- **7.4** Windows. Multiply by a Blackman or Hann window: much lower side lobes (leakage)
  at the price of a wider main lobe. That's the dual convolution theorem at work. (book:
  `Use_Blackman_Window`, `Hann_Windowed_Complex_Sinusoid`)
- **7.5** Spectrograms: a DFT of each short windowed slice, stacked over time. Make one of
  speech or a melody. *(This is the doorway to the STFT; see Phase 10.)* (book:
  `Spectrograms`, `Spectrogram_Speech`)
- **7.6** Filters and convolution: frequency response H(k) = Y(k)/X(k), amplitude and
  phase response. Worked case: the echo h = δ(n) + γ δ(n − τ) has
  |H(k)|² = 1 + γ² + 2γ cos(2πkτ/N), a **comb filter**. Hear it. (book:
  `Filters_Convolution`, `Frequency_Response`, `Amplitude_Response`, `Phase_Response`)
- **7.7** Correlation analysis: cross-correlation (and its unbiased form), autocorrelation,
  matched filtering (finding a known pattern in noise), FIR system identification. (book:
  `Correlation_Analysis`, `Cross_Correlation`, `Unbiased_Cross_Correlation`,
  `Autocorrelation`, `Matched_Filtering`, `FIR_System_Identification`)
- **7.8** *(depth-on-demand)* Power spectral density estimation (averaging periodograms)
  and the coherence function. (book: `Power_Spectral_Density_Estimation`,
  `Coherence_Function`, `Coherence_Function_Matlab`)

## Phase 8 — Around the DFT (appendices A-D, G)

- **8.1** The FFT. A direct DFT costs N² multiplies. Splitting even and odd samples
  (decimation in time) costs about N log2 N. Do the radix-2 split of the N = 4 pin by hand,
  then time a naive DFT against `np.fft.fft` at N = 4096. Depth-on-demand: mixed radix,
  prime factor, Rader, Bluestein, fixed-point FFTs, the DCT, number-theoretic transforms,
  FFT software (FFTW). (book: `Fast_Fourier_Transform_FFT`, `Decimation_Time`,
  `Radix_2_FFT`, `Mixed_Radix_Cooley_Tukey_FFT`, `Related_Transforms`,
  `Discrete_Cosine_Transform_DCT`, `FFT_Software`)
- **8.2** The four Fourier cases: DFT (discrete and finite), DTFT (discrete time,
  continuous frequency), Fourier series (periodic continuous time), Fourier transform
  (continuous both). The DFT is the DTFT sampled at N points; the impulse. (book:
  `Fourier_Transforms_Continuous_Discrete_Time_Frequency`,
  `Discrete_Time_Fourier_Transform`, `Fourier_Transform_FT_Inverse`,
  `Continuous_Time_Impulse`, `Fourier_Series_FS_Relation`, `Relation_DFT_Fourier_Series`)
- **8.3** Continuous Fourier theorems: differentiation, scaling, and the **uncertainty
  principle** (short in time means wide in frequency), tied back to window length in 7.4.
  (book: `Selected_Continuous_Time_Fourier_Theorems`, `Differentiation_Theorem`,
  `Scaling_Theorem`, `Uncertainty_Principle`)
- **8.4** Sampling theory: reconstruction from samples with sinc functions, aliasing of
  sampled signals, the **sampling theorem** (band-limited below f_s/2 means perfectly
  recoverable). (book: `Sampling_Theory`, `Introduction_Sampling`,
  `Reconstruction_Samples_Pictorial_Version`, `Sinc_Function`,
  `Aliasing_Sampled_Signals`, `Sampling_Theorem`)
- **8.5** *(depth-on-demand)* Digital audio number systems: PCM, fixed point, two's
  complement, floating point, μ-law, and how many bits are enough (≈ 6.02 dB per bit, so
  16 bits ≈ 96 dB). (book: `Number_Systems_Digital_Audio`, appendix G pages)

## Phase 9 — Putting It Together

- **9.1** Re-derive the whole chain in one session, unprompted: complex numbers → Euler →
  sampled complex sinusoids → orthogonality → DFT as projection → [1, 0, −1, 0] ↦
  [0, 2, 0, 2]. If any link is shaky, go back to it.
- **9.2** Capstone (pick one; record the choice in `progress.md`):
  - **(a) Analyze a real sound.** Record or download an instrument note or chord. Window
    it, zero-pad it, plot its dB spectrum, identify the partials and their frequencies in
    Hz, and name the notes.
  - **(b) Build it from scratch.** Write a naive DFT and a recursive radix-2 FFT, check
    both against `np.fft.fft`, then build a small spectrogram tool on top.
  - **(c) Explain it.** Write a two-page explanation of the DFT as projection for a
    classmate, with the N = 2 and N = 4 pins worked out in full.
- **9.3** Where to go next: the companion books in the same series
  (*Introduction to Digital Filters*, *Spectral Audio Signal Processing*, *Physical Audio
  Signal Processing*, all free at https://ccrma.stanford.edu/~jos/), the first two of which
  are tutored courses here (`filters/`, `sasp/`), and Phase 10.

## Phase 10 — Where the DFT Goes Next (a living bridge)

> **This phase is revised as the follow-on courses land.** It is depth-on-demand, never a
> gate. Each topic is one session that reuses the keystone (DFT = projection onto
> sinusoids) on the pinned cosine, then hands the learner to the course that goes deeper.
> The DFT itself is settled mathematics, so this isn't a SOTA phase; it's a map of where the
> mathematics is put to work, and *that* part moves.

- **10.1** The **short-time Fourier transform (STFT)**: the spectrogram of 7.5 made into
  an invertible transform (overlap-add and filter-bank views), with window design as a
  real engineering choice. → the sequel course **`sasp/`**, built on *Spectral Audio
  Signal Processing* (https://ccrma.stanford.edu/~jos/sasp/). It starts at this course's
  end state and climbs to the research frontier: windows, sinusoidal modeling, the phase
  vocoder, multirate filter banks, and modern spectral methods.
- **10.2** The MDCT: the DCT's overlapped cousin that every perceptual audio codec (MP3,
  AAC, Opus) and many neural codecs use. → `audio-codecs/`.
- **10.3** The DFT in neural audio: multi-scale spectral losses, mel spectrograms,
  differentiable filters (the convolution theorem as a training trick). →
  `audio-ddsp/`.
- **10.4** Convolution reverb: a room's impulse response applied with FFT convolution
  (the convolution theorem at work). → `room-acoustics/`.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question (a bank
   exercise from an earlier chapter makes good spaced review).
2. **Introduce one new concept** with an analogy/visual before any notation or code.
3. **Show**, then have the learner **do** a tiny exercise: by hand on the N = 2 / N = 4 pin,
   a few lines of numpy, or a bank exercise from `exercises/` for the current page.
4. **Verify** understanding from their answer; if shaky, re-explain a different way —
   do not advance until it's solid.
5. **Log** what was covered, the exercise, their answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
6. Keep each session ~1 hour. End with a one-sentence preview of next time, and point to
   the book page(s) to read before it.
