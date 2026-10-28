# Spectral Audio Signal Processing — From a Windowed DFT to the Research Frontier

**The book:** Julius O. Smith III, *Spectral Audio Signal Processing* (SASP), free online at
**https://ccrma.stanford.edu/~jos/sasp/**. Each topic below names its book page(s) as
`Page_Name`, and the full URL is `https://ccrma.stanford.edu/~jos/sasp/Page_Name.html`. The
course follows the book's chapter order (with a few topics regrouped), so the learner can
read the matching page before or after the session.

**Learner profile:** someone at the level of the `mdft` course's end state (the companion
book *Mathematics of the DFT*, https://ccrma.stanford.edu/~jos/mdft/). That means complex
numbers and Euler's identity, sinusoids, the DFT as projection onto orthogonal sinusoids,
the Fourier theorems (shift, convolution, Parseval, zero padding), and a first numpy
spectrum analysis. **No hard gate:** a learner can plunge in and backfill from `mdft`
when a gap shows (the tutor names the exact `mdft` topic). From there, the course climbs
as high as each of the book's topics reaches: integrals, random processes, linear
programming, multirate systems, and finally the current research literature. Each new
piece of mathematics is introduced just in time, as `mdft` did for complex numbers.
~1 hour per day. One concept at a time. Every concept is checked with a small exercise
before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position. Expect
~50-60 sessions for Phases 0-11, plus whatever of Phase 12 the learner wants.

**The keystone — the window, and the STFT's two views of it.**
1. **The window transform is the shape every sinusoid takes in a spectrum.** Multiplying
   a signal by a window w(n) convolves its spectrum with W(ω). So each sinusoid shows up
   as a copy of W, scaled and shifted to its frequency. Main-lobe width sets
   *resolution* (can two close sinusoids be told apart?). Side-lobe level sets *dynamic
   range* (can a quiet sinusoid be seen next to a loud one?). The two trade off, so no
   window is best for every job, and window design is the art of choosing.
2. **The STFT is one thing seen two ways.** Read along time (overlap-add, OLA), it's a
   sequence of windowed frames, and perfect resynthesis needs the window's shifts by
   the hop R to sum to a constant (**COLA**). Read along frequency (filter-bank
   summation, FBS), it's a bank of bandpass filters, all the same window shape
   modulated to each bin, and perfect resynthesis needs a dual condition on the window's
   *transform* (**Nyquist(N)**). The two conditions are Fourier duals (via the Poisson
   summation formula). Every later topic is a choice inside this picture: FFT
   convolution, the phase vocoder, sinusoidal modeling, the MDCT, the multirate filter
   banks of MP3 and of neural codecs.

**The pinned worked example — the A440 tone.** The way `mdft` returns to one
quarter-rate cosine, this course returns to one musical signal at **f_s = 44100 Hz**:
- **The tone:** a 1-second harmonic tone with f0 = 440 Hz (A4) and five harmonics of
  amplitude 1/h, optionally with an exponential decay and added white noise. It's
  synthesized in numpy, so every number is reproducible and can be *heard*.
- **The neighbor:** a second sinusoid a semitone up, A#4 ≈ 466.16 Hz (Δf ≈ 26.16 Hz).
  It's the resolution test.
- **The default STFT:** periodic Hann window M = 1024 (≈ 23.2 ms), hop R = 512 (COLA),
  FFT size N = 2048 (2× zero padding, ≈ 21.53 Hz per bin).

The full canonical numbers are in `CLAUDE.md`. The book's own recorded example, the
**oboe tone** of chapter 3, is the real-sound companion.

**The exercise bank:** `exercises/` holds 712 multiple-choice exercises from the
interactive online edition, one file per chapter, grouped by book page, each with hints,
answer and explanation (`exercises/index.md` lists them). They complement the tutor's own
derivations and numpy experiments. They never replace them.

**End state:** by the last core lesson the learner can:
- predict, measure and explain a window's main-lobe width, side-lobe level and roll-off,
  and choose a window (rectangular, Hann, Hamming, Blackman-Harris, Kaiser, DPSS,
  Chebyshev, Gaussian) for a job
- size an FFT analysis to resolve given sinusoids (M ≥ K·f_s/Δf), and estimate a peak's
  frequency and amplitude far below bin spacing (quadratic interpolation, least squares,
  maximum likelihood)
- design FIR filters by the window method, least squares, frequency sampling and Remez,
  including Hilbert transformers and minimum-phase filters
- estimate the spectrum of noise properly (periodogram vs Welch), and say what
  processing gain buys
- compute and read an STFT/spectrogram, and do FFT convolution, overlap-add,
  overlap-save and weighted overlap-add processing with perfect reconstruction
- derive COLA and Nyquist(N) conditions and explain their duality
- build an F0 estimator, a spectral-envelope extractor, a sinusoidal (sines+noise)
  analysis/resynthesis, and a phase-vocoder time-scale modifier
- explain polyphase decomposition, perfect-reconstruction and paraunitary filter banks,
  the MPEG (PQMF/MDCT) filter banks and wavelet filter banks
- read a current research paper in any of these areas and place it in the keystone
  picture (Phase 12)

---

## Phase 0 — Orientation and the Bridge from MDFT

- **0.1** The story, with no new notation: *analyze → modify → resynthesize.* A sound is
  cut into short windowed frames, each frame is FFT'd, the spectra are inspected or
  changed, and the frames are put back together. That one loop (the STFT) is inside
  spectrograms, MP3, noise reduction, time stretching, pitch correction, and today's
  neural vocoders and source separators. Show a spectrogram of a real sound. Point to
  the free online book. (book: `Introduction_Overview`, `Overview`, `Organization`)
- **0.2** Tools. Python with `numpy`, `scipy` (`scipy.signal`), `matplotlib`, and a way
  to *hear* (Colab `IPython.display.Audio`, or `soundfile` + `sounddevice` locally in a
  uv `.venv`). **Octave option:** the book's Matlab examples run in GNU Octave with the
  `signal` package (book appendix F, `Examples_Matlab_Octave`). Verify: synthesize and
  play the A440 tone.
- **0.3** Bridge check, using `mdft`'s last pin: the N = 64 cosine half a bin off
  (f = 0.25 + 0.5/64) gives peaks ≈ 20.4 instead of 32 (−3.9 dB) and nonzero bins
  everywhere. Ask the learner to explain why. If they can't, run a short `mdft` refresher
  (Phases 5-7) before Phase 1. *This course starts by asking what shape that leakage
  has, and how to control it: the window.* (book: `Notation`, `Frequency_Time`,
  `Signal_Notation`, `Fourier_Transform_Notation`)

## Phase 1 — Fourier Transforms and Theorems (chapter 2, appendix B)

- **1.1** From DFT to DTFT. Let N → ∞ in a zero-padded DFT and the bins fill in a
  continuous curve X(ω), the **DTFT**. The Fourier transform (FT) is the same idea for
  continuous time. *Integrals just in time:* an integral is the limit of a sum, ∫ ≈ Σ·Δt.
  When the FT exists. (book: `Fourier_Transforms_Continuous_Discrete_Time_Frequency`,
  `Discrete_Time_Fourier_Transform`, `Fourier_Transform_FT_Inverse`,
  `Existence_Fourier_Transform`)
- **1.2** The DTFT theorems: the `mdft` theorems again, now with continuous frequency.
  Linearity, time reversal, real-signal symmetry, shift, convolution, correlation,
  autocorrelation, power, stretch/repeat, downsampling and aliasing. (book:
  `Fourier_Theorems_DTFT`, `Linearity_DTFT`, `Time_Reversal`,
  `Symmetry_DTFT_Real_Signals`, `Shift_Theorem_DTFT`, `Convolution_Theorem_DTFT`,
  `Correlation_Theorem_DTFT`, `Autocorrelation`, `Power_Theorem_DTFT`,
  `Stretch_Repeat_Scaling_Theorem`, `Downsampling_Aliasing`)
- **1.3** Continuous-time theorems that the windows chapter leans on. The **scaling
  theorem** (shorter in time means wider in frequency) and the **uncertainty principle**.
  The **modulation theorem** (multiplying by a sinusoid shifts the spectrum, which is how
  a window lands on each sinusoid). **Smoothness vs roll-off:** a jump gives −6 dB/octave
  side lobes, a kink −12, and each additional continuous derivative another −6. The
  Gaussian pulse, rectangular pulse, sinc, impulse trains, and the **Poisson summation
  formula** (needed again in Phase 7). (book: `Continuous_Time_Fourier_Theorems`,
  `Scaling_Theorem`, `Spectral_Roll_Off`, `Selected_Continuous_Fourier_Theorems`,
  `Radians_versus_Cycles`, `Modulation_Theorem_Shift_Theorem`, `Uncertainty_Principle`,
  `Relation_Smoothness_Roll_Off_Rate`, `Gaussian_Pulse`, `Rectangular_Pulse`,
  `Sinc_Impulse`, `Impulse_Trains`, `Poisson_Summation_Formula_I`)
- **1.4** Spectral interpolation. Zero padding samples the DTFT more densely
  (interpolation, not resolution: an `mdft` misreading, re-checked here). Zero-phase
  zero padding (center the frame at time 0 so a symmetric window has a real transform).
  (book: `Spectral_Interpolation`, `Ideal_Spectral_Interpolation`, `Interpolating_DFT`,
  `Zero_Padding_Time_Domain`, `Zero_Phase_Zero_Padding`)

## Phase 2 — Spectrum Analysis Windows (chapter 3): keystone, part 1

- **2.1** The rectangular window. Its transform is the *aliased sinc*. Main-lobe width
  2 bins on each side of center (4π/M rad/sample in total). First side lobe −13.3 dB.
  Roll-off −6 dB/octave, from the jump at the window's edges. Multiply the A440 tone by it
  and see one copy of W per harmonic. (book: `Spectrum_Analysis_Windows`,
  `Rectangular_Window`, `Rectangular_Window_Side_Lobes`, `Rectangular_Window_Summary`)
- **2.2** The generalized Hamming family: the window transform as a *sum of three shifted
  aliased sincs* whose side lobes partly cancel. **Hann:** −31.5 dB, −18 dB/octave
  roll-off, main lobe twice as wide. **Hamming:** −42.7 dB, tuned to cancel the first side
  lobe, but only −6 dB/octave far out. The MLT sine window (a preview of the MDCT in
  Phase 10). (book: `Generalized_Hamming_Window_Family`, `Hann_Hanning_Raised_Cosine`,
  `Hamming_Window`, `Summary_Generalized_Hamming_Windows`, `MLT_Sine_Window`)
- **2.3** The Blackman-Harris family: more cosine terms give lower side lobes and wider
  main lobes. Classic Blackman is about −58 dB with a 6-bin-wide main lobe. Frequency-domain
  implementation (windowing as a 3-tap convolution of the FFT). Power-of-cosine windows.
  (book: `Blackman_Harris_Window_Family`, `Blackman_Window_Family`, `Classic_Blackman`,
  `Three_Term_Blackman_Harris_Window`,
  `Frequency_Domain_Implementation_Blackman_Harris_Family`, `Power_of_Cosine_Window_Family`)
- **2.4** A real sound: the book's oboe tone through rectangular, Hamming and Blackman
  windows. Why the quiet high harmonics vanish under the rectangular window's side lobes.
  Repeat with the A440 tone plus a −60 dB partial. (book: `Spectrum_Analysis_Oboe_Tone`,
  `Rectangular_Windowed_Oboe_Recording`, `Hamming_Windowed_Oboe_Recording`,
  `Blackman_Windowed_Oboe_Recording`, `Conclusions`)
- **2.5** Windows with a knob, each optimal in some sense. **Kaiser** (β trades main lobe
  for side lobes; approximates the DPSS). **Slepian/DPSS** (maximum energy in the main
  lobe). **Dolph-Chebyshev** (equiripple side lobes at a chosen level). Bartlett, Poisson
  and Hann-Poisson along the way. (book: `Kaiser_Window`, `Kaiser_Window_Beta_Parameter`,
  `Minimum_Frequency_Separation_vs_Window`, `Kaiser_DPSS_Windows_Compared`,
  `Slepian_DPSS_Window`, `Dolph_Chebyshev_Window`, `Dolph_Chebyshev_Window_Theory`,
  `Bartlett_Triangular_Window`, `Poisson_Window`, `Hann_Poisson_Window`)
- **2.6** The Gaussian window: Gaussian in time is Gaussian in frequency, and nothing
  beats its time-bandwidth product. Appendix D just in time: Gaussians are closed under
  multiplication and convolution, and the complex Gaussian (needed for chirplets, 9.6).
  (book: `Gaussian_Window_Transform`, `Exact_Discrete_Gaussian_Window`,
  `Gaussian_Function_Properties`, `Gaussians_Closed_Multiplication`,
  `Gaussians_Closed_Convolution`, `Why_Gaussian`)
- **2.7** *(depth-on-demand)* Optimized windows: windows for audio coding, and window
  design by **linear programming** (teach LP from scratch: constraints, objective,
  `scipy.optimize.linprog`). (book: `Optimized_Windows`, `Optimal_Windows_Audio_Coding`,
  `General_Rule`, `Window_Design_Linear_Programming`, `Linear_Programming_LP`,
  `LP_Formulation_Chebyshev_Window`, `Remez_Exchange_Algorithm`)

## Phase 3 — FIR Digital Filter Design (chapter 4)

- **3.1** The ideal lowpass filter (a sinc, infinitely long) and real-world specs:
  passband ripple, stopband attenuation, transition width. (book:
  `FIR_Digital_Filter_Design`, `Ideal_Lowpass_Filter`,
  `Lowpass_Filter_Design_Specifications`)
- **3.2** Least-squares FIR design (optimal in L2 but poor if used blindly: Gibbs) and
  frequency-sampling design. (book: `Optimal_but_poor_if`, `Frequency_Sampling_Method_FIR`)
- **3.3** **The window method:** truncate the ideal response with a window, and the
  Phase 2 trade-offs reappear as filter specs (side-lobe level becomes stopband
  attenuation, main-lobe width becomes transition width). Kaiser's design formulas. The
  generalized window method. (book: `Window_Method_FIR_Filter`,
  `Generalized_Window_Method`)
- **3.4** A Hilbert-transform filter design, worked end to end (the analytic signal from
  `mdft` 3.4, now built). (book: `Hilbert_Transform_Design_Example`)
- **3.5** Minimum-phase filters and the **cepstrum** (log-spectrum → inverse FFT → fold
  → back), and optimal Chebyshev design (Parks-McClellan/Remez with
  `scipy.signal.remez`). (book: `Minimum_Phase_Filter_Design`,
  `Minimum_Phase_Causal_Cepstra`, `Optimal_FIR_Digital_Filter`)

## Phase 4 — Spectrum Analysis of Sinusoids (chapter 5)

- **4.1** The spectrum of a windowed sinusoid *is* the window transform, shifted and
  scaled (the modulation theorem from 1.3 made concrete). Amplitude scaling: a sinusoid of
  amplitude A peaks at A·Σw(n)/2. (book: `Spectrum_Analysis_Sinusoids`,
  `Spectrum_Sinusoid`, `Spectrum_Sampled_Complex_Sinusoid`, `Spectrum_Windowed_Sinusoid`,
  `Effect_Windowing`, `Frequency_Resolution`)
- **4.2** **Resolving sinusoids:** M ≥ K·f_s/Δf, where K is the main-lobe width in bins
  (rectangular 2, Hann/Hamming 4, Blackman 6). On the pin, telling A4 from A#4 needs a
  Hann window of at least ≈ 6742 samples (≈ 153 ms), but separating the A440 tone's
  harmonics needs only M ≥ 401. Hear why a fast melody in the low register is hard to
  analyze. Periodic signals; tighter bounds (K*). (book: `Resolving_Sinusoids`,
  `Other_Definitions_Main_Lobe`, `Simple_Sufficient_Condition_Peak`, `Periodic_Signals`,
  `Tighter_Bounds_Minimum_Window`)
- **4.3** **Peak interpolation:** fit a parabola to the dB magnitudes at the peak bin
  and its two neighbors. On the pin's default STFT, the raw peak bin 20 says 430.7 Hz and
  the interpolated peak says 440.04 Hz. Bias, and the minimum zero padding that keeps it
  small. (book: `Sinusoidal_Peak_Interpolation`, `Quadratic_Interpolation_Spectral_Peaks`,
  `Bias_Parabolic_Peak_Interpolation`, `Minimum_Zero_Padding_High_Frequency_Peaks`,
  `Matlab_Finding_Interpolated_Spectral`)
- **4.4** *(depth-on-demand)* Optimal peak finding: least-squares sinusoidal parameter
  estimation, maximum likelihood, and why the FFT peak *is* the ML frequency estimate for
  one sinusoid in white noise. (book: `Optimal_Peak_Finding_Spectrum`,
  `Least_Squares_Sinusoidal_Parameter`, `Maximum_Likelihood_Sinusoid_Estimation`,
  `Likelihood_Function`, `Generality_Maximum_Likelihood_Least`)

## Phase 5 — Spectrum Analysis of Noise (chapter 6, appendices C-D)

- **5.1** *Probability just in time* (appendix C): random variables, expectation,
  stochastic processes, stationarity. White noise. Why an impulse is *not* white noise,
  even though both have flat spectra. (book: `Beginning_Statistical_Signal_Processing`,
  `Random_Variables_Stochastic`, `Spectrum_Analysis_Noise`, `Introduction_Noise`,
  `Spectral_Characteristics_Noise`, `White_Noise`, `Why_Impulse_Not_White`)
- **5.2** Sample autocorrelation (biased and unbiased), the sample power spectral density,
  and the **periodogram**. Its variance does *not* shrink as N grows. (book:
  `Sample_Autocorrelation`, `Sample_Power_Spectral_Density`,
  `Biased_Sample_Autocorrelation`, `Periodogram`)
- **5.3** **Welch's method:** average windowed periodograms to trade resolution for
  variance. Smoothed PSD; cyclic autocorrelation; the practical bottom line. (book:
  `Welch_s_Method`, `Welch_s_Method_Windows`, `Smoothed_Power_Spectral_Density`,
  `Cyclic_Autocorrelation`, `Practical_Bottom_Line`)
- **5.4** Filtered white noise and **processing gain**: doubling M raises a sinusoid's
  peak 3 dB relative to the noise floor. Add noise to the A440 tone and watch the
  harmonics climb out of it as M grows. The panning problem. (book:
  `Filtered_White_Noise`, `Processing_Gain`, `Panning_Problem`)

## Phase 6 — Time-Frequency Displays (chapter 7)

- **6.1** The STFT: definition, practical computation with FFTs, and the two dual
  interpretations (previewing Phases 7-8). (book: `Time_Frequency_Displays`,
  `Short_Time_Fourier_Transform`, `Mathematical_Definition_STFT`,
  `Practical_Computation_STFT`, `Summary_STFT_Computation_Using`,
  `Two_Dual_Interpretations_STFT`, `STFT_Time_Frequency_Distribution`, `STFT_Matlab`)
- **6.2** Spectrograms. Classic speech spectrograms: wideband (short window, shows
  pitch pulses) vs narrowband (long window, shows harmonics). On the pin, compare
  M = 1024 with M = 8192 and hear and see the attack smear. (book: `Classic_Spectrograms`,
  `Spectrogram_Speech`, `Matlab_Computing_Spectrograms`)
- **6.3** Audio spectrograms that model hearing: auditory filter banks, loudness
  spectrograms, the Bark and ERB scales (appendix E). (book: `Audio_Spectrograms`,
  `Auditory_Filter_Banks`, `Loudness_Spectrogram`, `Bark_Frequency_Scale`,
  `Equivalent_Rectangular_Bandwidth`)

## Phase 7 — Overlap-Add STFT Processing (chapter 8): keystone, part 2a

- **7.1** FFT convolution. Cyclic vs acyclic, zero padding to make it acyclic, and when
  FFT beats direct convolution. (book: `Overlap_Add_OLA_STFT_Processing`,
  `Convolution_Short_Signals`, `Cyclic_FFT_Convolution`, `Acyclic_FFT_Convolution`,
  `FFT_versus_Direct_Convolution`)
- **7.2** Overlap-add for long signals and the **COLA** condition. On the pin, periodic
  Hann at R = M/2 sums to exactly 1, a *symmetric* Hann (`np.hanning`) does not, and a
  rectangular window needs R = M. (book: `Convolving_Long_Signals`,
  `Overlap_Add_Decomposition`, `COLA_Examples`, `STFT_COLA_Decomposition`,
  `Example_Overlap_Add_Convolution`, `Summary_Overlap_Add_FFT_Processing`)
- **7.3** The dual of COLA: the Poisson summation formula turns the time-domain COLA
  condition into a condition on the window transform at multiples of 2π/R. (book:
  `Dual_Constant_Overlap_Add`, `Poisson_Summation_Formula`,
  `Frequency_Domain_COLA_Constraints`, `PSF_Dual_Graphical_Equalizers`)
- **7.4** Overlap-save. Time-varying modifications. **Weighted overlap-add** (WOLA),
  with an analysis window and a synthesis window whose *product* is COLA (√Hann twice),
  which is what makes spectral modifications safe. (book: `Overlap_Save_Method`,
  `Time_Varying_OLA_Modifications`, `Weighted_Overlap_Add`, `WOLA_Processing_Steps`,
  `PSF_Weighted_Overlap_Add`, `Example_COLA_Windows_WOLA`)

## Phase 8 — Filter Bank View of the STFT (chapter 9): keystone, part 2b

- **8.1** Dual views. The same STFT array read by column (frames, OLA) and by row
  (channels, FBS). (book: `Filter_Bank_Summation_FBS`, `Dual_Views_Short_Time`,
  `Overlap_Add_OLA_Interpretation_STFT`, `Filter_Bank_Summation_FBS_Interpretation`,
  `FBS_Perfect_Reconstruction`)
- **8.2** The DFT filter bank: a running-sum lowpass filter, modulated to every bin by a
  complex sinusoid, gives a bank of bandpass filters. (book: `STFT_Filter_Bank`,
  `DFT_Filter_Bank`, `Running_Sum_Lowpass_Filter`, `Modulation_Complex_Sinusoid`,
  `Making_Bandpass_Filter_Lowpass`, `Uniform_Running_Sum_Filter_Banks`)
- **8.3** FBS window constraints, **Nyquist(N)** windows, and the **duality of COLA and
  Nyquist(N)**: the keystone's second half, derived. Portnoff windows. (book:
  `FBS_Window_Constraints_R_1`, `Nyquist_N_Windows`, `Duality_COLA_Nyquist_Conditions`,
  `Portnoff_Windows`)
- **8.4** Downsampled STFT filter banks (hop R > 1 is downsampling each channel, with
  aliasing that must cancel), and modifications in the FBS view. (book:
  `Downsampled_STFT_Filter_Banks`, `Downsampling_Anti_Aliasing`,
  `Constant_Overlap_Add_COLA_Cases`, `STFT_Modifications`, `FBS_Fixed_Modifications`,
  `Time_Varying_Modifications_FBS`, `STFT_Summary_Conclusions`)

## Phase 9 — Applications of the STFT (chapter 10, appendices E, H)

- **9.1** F0 estimation from spectral peaks: find the harmonics of the A440 tone and
  recover 440 Hz; preprocessing; getting closer to maximum likelihood. (book:
  `Fundamental_Frequency_Estimation_Spectral`, `Useful_Preprocessing`,
  `Getting_Closer_Maximum_Likelihood`, `Fundamental_Frequency_Estimation`)
- **9.2** Spectral envelopes by cepstral windowing and linear prediction; cross-synthesis
  (the vocoder effect: one sound's envelope on another's fine structure). (book:
  `Spectral_Envelope_Extraction`, `Cepstral_Windowing`,
  `Linear_Prediction_Spectral_Envelope`, `Spectral_Envelope_Examples`, `Cross_Synthesis`)
- **9.3** **Sinusoidal modeling:** peak finding, peak tracking across frames, additive
  resynthesis (the PARSHL program, appendix H). Then **sines + noise** (SMS) and sines
  + noise + transients. Resynthesize the pin from its tracked peaks and listen to the
  residual. (book: `Spectral_Modeling_Synthesis`, `Additive_Synthesis_Early_Sinusoidal`,
  `Additive_Synthesis_Analysis`, `Sinusoidal_Peak_Finding`,
  `Tracking_Sinusoidal_Peaks_Sequence`, `PARSHL_Program`, `Peak_Detection_Steps_3`,
  `Peak_Matching_Step_5`, `Synthesis_Step_7`, `Sines_Noise_Modeling`,
  `Sines_Noise_Analysis`, `S_N_Synthesis`, `Sines_Noise`, `S_N_T_Sound_Examples`)
- **9.4** **Time-scale modification and the phase vocoder.** Resample the STFT across
  time, then fix the phases (phase continuation: advance each bin's phase by its
  measured frequency × the synthesis hop). Relative-phase preservation and SOLA-FS.
  Stretch the pin by 2× and hear "phasiness". Pitch shifting = TSM + resampling.
  History: Dudley's channel vocoder, Flanagan and Golden's phase vocoder. (book:
  `Time_Scale_Modification`, `TSM_S_N_T`, `TSM_Resampling_STFTs_Across`,
  `Phase_Continuation`, `Phase_Continued_STFT_TSM`, `Relative_Phase_Preserving_STFT_TSM`,
  `SOLA_FS_TSM`, `TSM_Examples`, `Phase_Vocoder`, `Dudley_s_Channel_Vocoder`,
  `Matlab_Unwrapping_Spectral_Phase`)
- **9.5** FFT filter banks: summing STFT bins into wider channels, fast octave filter
  banks, spectral rotation. Bilinear frequency warping to approximate Bark (appendix E).
  (book: `FFT_Filter_Banks`, `Audio_Filter_Banks`, `Summing_STFT_Bins`,
  `Inverse_Transforming_STFT_Bin`, `Fast_Octave_Filter_Banks`,
  `FFT_Filter_Bank_Summary_Fourier`, `Bilinear_Frequency_Warping_Audio_Spectrum`,
  `Bilinear_Transform`, `Optimal_Bilinear_Bark_Warping`)
- **9.6** *(depth-on-demand)* Gaussian-windowed chirps (chirplets): a linear frequency
  sweep under a Gaussian window stays Gaussian, and its chirp rate can be read off the
  spectrum. (book: `Gaussian_Windowed_Chirps_Chirplets`, `Chirplet_Fourier_Transform`,
  `Identifying_Chirp_Rate`)

## Phase 10 — Multirate Filter Banks (chapter 11)

- **10.1** Upsampling, downsampling and filtering; **polyphase decomposition** and the
  noble identities (filter at the low rate, which is where the speed comes from). (book:
  `Multirate_Filter_Banks`, `Upsampling_Downsampling`, `Upsampling_Stretch_Operator`,
  `Downsampling_Decimation_Operator`, `Filtering_Downsampling`, `Polyphase_Decomposition`,
  `Two_Channel_Case`, `N_Channel_Polyphase_Decomposition`, `Multirate_Noble_Identities`)
- **10.2** Critically sampled perfect-reconstruction (PR) filter banks, two channels
  first. The Haar example; QMF; conjugate quadrature filters; orthogonal two-channel
  banks. Aliasing in each channel *cancels* across channels. (book:
  `Critically_Sampled_Perfect_Reconstruction`, `Two_Channel_Critically_Sampled_Filter`,
  `Haar_Example`, `Quadrature_Mirror_Filters_QMF`, `Conjugate_Quadrature_Filters_CQF`,
  `Orthogonal_Two_Channel_Filter_Banks`)
- **10.3** N-channel PR conditions in polyphase form; the polyphase view of the STFT
  (OLA and WOLA, so the keystone reappears); paraunitary (lossless) filter banks. (book:
  `Perfect_Reconstruction_Filter_Banks`, `Sufficient_Condition_Perfect_Reconstruction`,
  `Necessary_Sufficient_Conditions_Perfect`, `Polyphase_View_STFT`,
  `Paraunitary_Filter_Banks`, `Lossless_Filters`, `Filter_Banks_Equivalent_STFTs`)
- **10.4** The MPEG filter banks. Pseudo-QMF cosine modulation (MP3's 32 bands), PR cosine
  modulation, and the MDCT/MLT with the sine window from 2.2 (critically sampled, with
  time-domain aliasing cancellation). (book: `MPEG_Filter_Banks`,
  `Pseudo_QMF_Cosine_Modulation_Filter`, `PR_Cosine_Modulated_Filter`,
  `MPEG_Layer_III_Filter`, `Review_STFT_Filterbanks`)
- **10.5** Wavelet filter banks. The DFT, DTFT, STFT and wavelet transforms as choices of
  basis (`mdft`'s keystone at full generality); dyadic (octave) filter banks; the
  generalized STFT. (book: `Wavelet_Filter_Banks`, `Geometric_Signal_Theory`,
  `Normalized_STFT_Basis`, `Continuous_Wavelet_Transform`, `Discrete_Wavelet_Transform`,
  `Dyadic_Filter_Banks`, `Generalized_STFT`, `Conclusions_I_I`)

## Phase 11 — Putting It Together

- **11.1** Re-derive the keystone unprompted: windowing theorem → main lobe vs side lobes
  → M ≥ K·f_s/Δf → STFT → COLA ⇔ Nyquist(N) → why the phase vocoder, SMS and the MDCT
  each pick the window and hop they do.
- **11.2** Capstone (pick one; record the choice in `progress.md`):
  - **(a) A phase-vocoder time stretcher:** WOLA analysis and resynthesis with phase
    continuation (and optional phase locking), tested on the pin and on a real recording
    at 0.5×, 1.5× and 2×.
  - **(b) A sines+noise analysis/resynthesis:** PARSHL-style peak tracking plus a
    filtered-noise residual, run on a real instrument note. Transform it (pitch shift,
    stretch, cross-synthesis).
  - **(c) A perfect-reconstruction filter bank:** an MDCT with the sine window, or a
    PQMF bank, verified to reconstruct to numerical precision, then used for crude
    subband coding (quantize the bands; hear the artifacts).
- **11.3** History as a map (appendix G): Bernoulli's modes → Telharmonium → Hammond →
  vocoder → phase vocoder → additive and FM synthesis → SMS → perceptual coding. Each
  is a keystone choice. (book: `History_Spectral_Audio_Signal`,
  `Daniel_Bernoulli_s_Modal_Decomposition`, `Telharmonium`, `Hammond_Organ`,
  `Additive_Synthesis`, `Frequency_Modulation_FM_Synthesis`,
  `Phase_Vocoder_Sinusoidal_Modeling`, `Perceptual_audio_coding`, `Future_Prospects`,
  `Summary_Conclusions`)

## Phase 12 — The Frontier (a living section)

> **This phase tracks the current state of the art and is revised as the field moves.**
> It is depth-on-demand, never a gate. Each frontier topic is one session or more: it
> starts from the chapter it extends, reuses the keystone (the window and the STFT's two
> views), runs on the A440 pin where possible, and ends by reading one paper from the
> sources list below together. Claims marked *(empirical)* are benchmark results that
> later work may overturn. Last surveyed: **October 2026**.

- **12.1 Phase from magnitude** (extends 9.4). A magnitude-only STFT doesn't determine
  a signal until phase is recovered. Griffin-Lim (iterative projection between "is a
  valid STFT" and "has this magnitude": `mdft`'s projection keystone again). Phase
  Gradient Heap Integration (non-iterative: integrate the phase derivatives that a
  Gaussian window ties to the magnitude, chapter 2.6). Then neural vocoders that predict
  STFT coefficients and resynthesize by iSTFT/OLA: iSTFTNet, Vocos, and complex-valued
  networks. *(empirical: quality rankings vs time-domain vocoders shift
  benchmark-to-benchmark.)*
- **12.2 The phase vocoder done right** (extends 9.4). Phase locking (Laroche & Dolson)
  and phase-gradient-integration TSM (Průša & Holighaus), heard against the 9.4 baseline
  on the pin. Neural TSM by latent interpolation as a contrast.
- **12.3 Sharper time-frequency pictures** (extends 6, 2.5). Reassignment and
  synchrosqueezing move energy to where the phase says it belongs, which beats the
  window's uncertainty smear for isolated components (and fails gracefully elsewhere).
  Multitaper spectra: averaging over the DPSS windows of 2.5 for low variance (5.3)
  without losing resolution.
- **12.4 Nonuniform, invertible time-frequency** (extends 8, 10.5). Nonstationary Gabor
  frames and the invertible constant-Q transform: windows whose length varies with
  frequency, with perfect reconstruction kept by a generalized COLA/frame condition.
- **12.5 Sinusoidal modeling goes differentiable** (extends 9.3). DDSP's harmonic
  oscillator bank plus filtered noise is SMS with a neural network choosing the
  parameters, and sines+transients+noise neural models of piano notes follow the same
  route. → `audio-ddsp/`.
- **12.6 Spectra as training losses and learned front ends** (extends 6, 7). Multi-
  resolution STFT losses (several M at once, which is the resolution trade-off of 4.2
  turned into a loss), scattering and joint time-frequency scattering, and learnable
  filter banks (SincNet, LEAF) that make the window itself a trained parameter. →
  `audio-ddsp/`, `audio-synth-effect-matching/`.
- **12.7 Filter banks inside neural codecs and separators** (extends 10). PQMF
  multiband decomposition in Multi-band MelGAN and RAVE (critically sampled PR banks
  from 10.2-10.4 used to cut the network's work), the MDCT inside Opus/AAC vs learned
  codec latents, and band-split source separation (a learned nonuniform filter bank over
  the STFT). → `audio-codecs/`, `neural-audio-resynthesis/`.
- **12.8 F0 estimation since the spectral-peak method** (extends 9.1). YIN and pYIN (the
  autocorrelation route) and CREPE (a network on raw frames), benchmarked against the
  9.1 estimator on the pin plus noise. *(empirical.)*

### Frontier sources
- Griffin, D. W., & Lim, J. S. (1984). Signal estimation from modified short-time Fourier
  transform. *IEEE Trans. ASSP*, 32(2), 236-243.
- Průša, Z., Balazs, P., & Søndergaard, P. L. (2017). A noniterative method for
  reconstruction of phase from STFT magnitude. *IEEE/ACM Trans. ASLP*, 25(5), 1154-1164.
- Kaneko, T., Tanaka, K., Kameoka, H., & Seki, S. (2022). iSTFTNet: Fast and lightweight
  mel-spectrogram vocoder incorporating inverse short-time Fourier transform. *ICASSP
  2022*. arXiv:2203.02395.
- Siuzdak, H. (2023). Vocos: Closing the gap between time-domain and Fourier-based neural
  vocoders for high-quality audio synthesis. arXiv:2306.00814 (ICLR 2024).
- ComVo, a complex-valued iSTFT vocoder. arXiv:2603.11589 (ICLR 2026). *(Recent; check
  the paper for authors and claims before teaching from it.)*
- Laroche, J., & Dolson, M. (1999). Improved phase vocoder time-scale modification of
  audio. *IEEE Trans. Speech and Audio Processing*, 7(3), 323-332.
- Průša, Z., & Holighaus, N. (2017). Phase vocoder done right. *EUSIPCO 2017*.
- Audio time-scale modification with temporal compressing networks. arXiv:2210.17152
  (ACM MMAsia 2023).
- Auger, F., & Flandrin, P. (1995). Improving the readability of time-frequency and
  time-scale representations by the reassignment method. *IEEE Trans. Signal Processing*,
  43(5), 1068-1089.
- Daubechies, I., Lu, J., & Wu, H.-T. (2011). Synchrosqueezed wavelet transforms: An
  empirical mode decomposition-like tool. *Applied and Computational Harmonic Analysis*,
  30(2), 243-261.
- Thomson, D. J. (1982). Spectrum estimation and harmonic analysis. *Proc. IEEE*, 70(9),
  1055-1096.
- Balazs, P., Dörfler, M., Jaillet, F., Holighaus, N., & Velasco, G. (2011). Theory,
  implementation and applications of nonstationary Gabor frames. *J. Computational and
  Applied Mathematics*, 236(6), 1481-1496.
- Holighaus, N., Dörfler, M., Velasco, G. A., & Grill, T. (2013). A framework for
  invertible, real-time constant-Q transforms. *IEEE Trans. ASLP*, 21(4), 775-785.
- Engel, J., Hantrakul, L., Gu, C., & Roberts, A. (2020). DDSP: Differentiable digital
  signal processing. *ICLR 2020*.
- Simionato, R., & Fasciani, S. (2025). Sines, transient, noise neural modeling of piano
  notes. *Frontiers in Signal Processing*. doi:10.3389/frsip.2024.1494864
  (arXiv:2409.06513).
- Yamamoto, R., Song, E., & Kim, J.-M. (2020). Parallel WaveGAN (multi-resolution STFT
  loss). *ICASSP 2020*.
- Andén, J., & Mallat, S. (2014). Deep scattering spectrum. *IEEE Trans. Signal
  Processing*, 62(16), 4114-4128.
- Andén, J., Lostanlen, V., & Mallat, S. (2019). Joint time-frequency scattering. *IEEE
  Trans. Signal Processing*, 67(14), 3704-3718.
- Ravanelli, M., & Bengio, Y. (2018). Speaker recognition from raw waveform with SincNet.
  *IEEE SLT 2018*.
- Zeghidour, N., Teboul, O., de Chaumont Quitry, F., & Tagliasacchi, M. (2021). LEAF: A
  learnable frontend for audio classification. *ICLR 2021*.
- Yang, G., Yang, S., Liu, K., Fang, P., Chen, W., & Xie, L. (2021). Multi-band MelGAN.
  *IEEE SLT 2021*.
- Caillon, A., & Esling, P. (2021). RAVE: A variational autoencoder for fast and
  high-quality neural audio synthesis. arXiv:2111.05011.
- Lu, W.-T., Wang, J.-C., Kong, Q., & Hung, Y.-N. (2024). Music source separation with
  band-split RoPE transformer. *ICASSP 2024*.
- de Cheveigné, A., & Kawahara, H. (2002). YIN, a fundamental frequency estimator for
  speech and music. *JASA*, 111(4), 1917-1930.
- Mauch, M., & Dixon, S. (2014). pYIN: A fundamental frequency estimator using
  probabilistic threshold distributions. *ICASSP 2014*.
- Kim, J. W., Salamon, J., Li, P., & Bello, J. P. (2018). CREPE: A convolutional
  representation for pitch estimation. *ICASSP 2018*.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question (a bank
   exercise from an earlier chapter makes good spaced review).
2. **Introduce one new concept** with an analogy/visual before any notation or code.
3. **Show**, then have the learner **do** a tiny exercise: a derivation, a few lines of
   numpy/scipy on the A440 pin (and *listen* to it), or a bank exercise from
   `exercises/` for the current page.
4. **Verify** understanding from their answer; if shaky, re-explain a different way —
   do not advance until it's solid.
5. **Log** what was covered, the exercise, their answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
6. Keep each session ~1 hour. End with a one-sentence preview of next time, and point to
   the book page(s) to read before it.
