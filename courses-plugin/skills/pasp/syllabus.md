# Physical Audio Signal Processing — From a Delay Line to Virtual Instruments and the Frontier

**The book:** Julius O. Smith III, *Physical Audio Signal Processing for Virtual Musical
Instruments and Audio Effects* (PASP), free online at **https://ccrma.stanford.edu/~jos/pasp/**.
Each topic below names its book page(s) as `Page_Name`, and the full URL is
`https://ccrma.stanford.edu/~jos/pasp/Page_Name.html`. The course follows the book's chapter
order, but brings the theory appendices (physics, waveguide theory, wave digital filters,
finite differences) in where they're needed. The learner can read the matching page before
or after the session.

**Learner profile:** someone at the level of the `filters` course's end state (Book II,
*Introduction to Digital Filters*, https://ccrma.stanford.edu/~jos/filters/). This course is
the second half of the series' *physical* track (`filters` → `pasp`), and it builds most
directly on `filters`: the z transform, poles and zeros, comb and allpass filters, the
bilinear transform, a little state space. For its complete development PASP draws on the
whole series, though: `mdft` throughout (complex sinusoids, the DFT, spectra), and `sasp`
lightly (windowed-sinc interpolation, FFT-based analysis for loop-filter
identification). **No hard gate:** a learner can plunge in and backfill from `filters`,
`mdft` or `sasp` when a gap shows (the tutor names the exact topic). From there the course builds what physical modeling needs, just in
time: Newtonian mechanics, the wave equation and partial derivatives, impedance and
circuit analogies, numerical integration of ODEs and PDEs. It ends at the current
research literature (Phase 15). ~1 hour per day. One concept at a time. Every concept is
checked with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position. This is the
largest book in the series; expect ~70-90 sessions for Phases 0-14, plus whatever of
Phase 15 the learner wants. Phases 3, 5, 13 and the instrument sections of Phase 13 are
natural places to go by interest.

**The keystone — traveling waves in delay lines, scattering where impedance changes.**
1. **A traveling wave is a delay line.** Every solution of the ideal 1-D wave equation
   (string, tube) is a right-going wave plus a left-going wave (d'Alembert). Sample it,
   and each traveling wave is just a **delay line**. That's a *digital waveguide*: exact
   at the sample points, not an approximation. The losses and dispersion spread along a
   real string are linear and time-invariant, so they **commute** and can be lumped into
   one **loop filter**, and a fractional delay tunes the loop. A string is two delay lines
   and a filter, and Karplus-Strong is the simplest case. Reverberators (combs, allpasses,
   feedback delay networks) are networks of the same parts.
2. **Waves scatter where impedance changes.** Express the waves as physical *wave
   variables* (force and velocity, or pressure and volume velocity) related by the **wave
   impedance**. Where impedance changes (a junction, a bridge, a tonehole, a bell), a
   fraction ρ = (R2 − R1)/(R2 + R1) of the wave reflects and the rest transmits. Kelly-Lochbaum
   junctions, wave digital filter adaptors, and lumped masses, springs and dashpots seen
   as reflectances are all this one idea. Built from lossless scattering and passive
   elements, the model conserves (or loses) energy, which makes it **stable by
   construction**.

Every instrument in Phase 13 (and every reverb in Phase 3) is these two ideas combined.

**The pinned worked examples — the A440 string and its neighbors, at f_s = 44100 Hz.** The
way `mdft` returns to one quarter-rate cosine and `filters` to its four filters, this course
returns to:
- **The A440 string:** a rigidly terminated string tuned to 440 Hz, whose period is
  P = 100.227 samples. As **Karplus-Strong**, the loop delay plus the half-sample delay of
  the (1 + z^(−1))/2 loop filter must equal P, so the delay line is 99.727 samples: 99
  whole samples plus a Thiran allpass for the 0.727 fraction. Each harmonic decays at its
  own rate, which can be predicted from the loop filter and then heard. As a **physical
  string:** a 0.65 m guitar-scale string needs wave speed c = 2Lf0 = 572 m/s.
- **The A440 mass-spring:** a 1 g mass on a spring tuned to 440 Hz, digitized by the
  bilinear transform (warping measured).
- **One impedance step:** R1 = 1 to R2 = 2 gives ρ = 1/3. It's the smallest scattering
  junction.
- **Two reverberators:** Freeverb (8 lowpass-feedback combs + 4 allpasses) and a
  feedback delay network (FDN) tuned for T60 = 2 s.

The full canonical numbers are in `CLAUDE.md`. Everything is *heard*: the course is about
making sound.

**The exercise bank:** `exercises/` holds 1431 multiple-choice exercises from the
interactive online edition, one file per chapter, grouped by book page, each with hints,
answer and explanation (`exercises/index.md` lists them). They complement the tutor's own
derivations, simulations and listening tests. They never replace them.

**End state:** by the last core lesson the learner can:
- explain the difference between signal models and physical models, and when each wins
- derive the wave equation for a string from Newton's second law, and its traveling-wave
  solution
- build delay-line models of propagation, combs, allpasses and feedback delay networks,
  and design Schroeder, Freeverb and FDN reverberators for a target T60
- implement fractional delay (linear, allpass, Lagrange, Thiran, windowed sinc) and the
  time-varying delay effects (flanger, phaser, chorus, vibrato, Doppler, Leslie)
- build digital waveguide strings and tubes with consolidated loss and dispersion filters,
  and Karplus-Strong / extended Karplus-Strong guitars
- work with wave variables, wave impedance and scattering junctions (Kelly-Lochbaum,
  loaded junctions, coupled strings, meshes)
- model lumped mechanical systems as impedances and one-ports, digitize them (finite
  differences, bilinear transform, wave digital filters), and handle nonlinear ODEs
- analyze finite-difference schemes (convergence, von Neumann stability) and relate them
  to digital waveguides
- use transfer-function methods (impulse invariance, matched z, modal expansion, commuted
  synthesis) for bodies and resonators
- assemble virtual instruments: electric and acoustic guitars, piano, single reeds,
  bowed strings, brasses, voice
- read a current research paper on differentiable physical models, neural reverb,
  wave digital filters or numerical sound synthesis and place it in the keystone picture
  (Phase 15)

---

## Phase 0 — Orientation

- **0.1** What a model is, and what kind. *Signal models* describe the sound (spectral
  modeling, sampling); *physical models* describe the thing that makes it (the string,
  the tube, the room), and get expressive control and realistic transients almost free.
  "But how does it sound?" Listen to a plucked-string model next to a recording. Point to
  the free online book and its sound examples. (book: `Introduction_Physical_Signal_Models`,
  `But_How_Does_It`, `What_Model`, `Overview_Model_Types`, `Signal_Models`,
  `Physical_Models`, `Our_Plan`, `Sound_Examples`)
- **0.2** Tools. Python with `numpy`, `scipy`, `matplotlib`, and a way to *hear* (Colab
  `IPython.display.Audio`, or `soundfile` + `sounddevice` locally in a uv `.venv`).
  **Faust is first-class here:** many of the book's models come as Faust code, the online
  Faust IDE needs no install, and the Faust libraries (`physmodels`, `reverbs`,
  `delays`) implement much of the book. **Octave option** for the book's Matlab. Verify:
  a 1-second noise burst into a 100-sample feedback comb, heard as a pitched buzz.
- **0.3** Bridge from `filters`: the feedback comb y(n) = x(n) + g·y(n−M) is already a
  string (a delay line closed on itself). What's missing is a loop filter, exact tuning,
  and a physical reading of the delay line. Elementary physical-modeling problems as a
  route map. (book: `Elementary_Physical_Modeling_Problems`)

## Phase 1 — Physics Just in Time (appendix B)

- **1.1** Newton's laws, work and energy, momentum. Mass, spring and dashpot as the three
  elementary mechanical elements (f = m·a, f = k·x, f = μ·v). *Calculus just in time:*
  derivatives as rates, and the second derivative as acceleration. (book:
  `Elementary_Physics_Mechanics_Acoustics`, `Newton_s_Laws_Motion`, `Work_Force_times`,
  `Momentum`)
- **1.2** Rigid bodies and elastic solids (stress, strain, Young's modulus), enough to
  say why strings, bars and plates vibrate differently. (book: `Rigid_Body_Dynamics`,
  `Properties_Elastic_Solids`)
- **1.3** **The wave equation for the vibrating string**, derived from Newton's second
  law on a small piece of string: K·y'' = ε·ÿ (tension K, linear mass density ε), so the
  wave speed is c = √(K/ε). *Partial derivatives just in time.* On the pin: a 0.65 m
  string at 440 Hz needs c = 572 m/s. (book: `Wave_Equation_Vibrating_String`)
- **1.4** Gases: pressure, the speed of sound, the acoustic wave equation, and waves in
  higher dimensions (plane and spherical waves, 1/r spreading). (book: `Properties_Gases`,
  `Wave_Equation_Higher_Dimensions`)

## Phase 2 — Acoustic Modeling with Delay (chapter 2)

- **2.1** Delay lines (circular buffers) as acoustic propagation: a sound traveling d
  meters arrives d/c seconds later. Lossy propagation: 1/r spreading and frequency-
  dependent air absorption, each a gain or a filter on the delay line. (book:
  `Acoustic_Modeling_Digital_Delay`, `Delay_Lines`, `Acoustic_Wave_Propagation_Simulation`,
  `Lossy_Acoustic_Propagation`)
- **2.2** A first look at digital waveguides (two delay lines, one each way). Tapped
  delay lines and multiple echoes. (book: `Digital_Waveguides`, `Tapped_Delay_Line_TDL`)
- **2.3** Comb filters again (`filters` 2.2), now as acoustic echoes between two walls.
  Feedback delay networks: several delay lines mixed through a feedback matrix. (book:
  `Comb_Filters`, `Feedback_Delay_Networks_FDN`)
- **2.4** Allpass filters as delay-line structures (Schroeder allpass), and allpass
  digital waveguide networks. (book: `Allpass_Filters`, `Allpass_Digital_Waveguide_Networks`)

## Phase 3 — Artificial Reverberation (chapter 3)

- **3.1** The reverberation problem: an exact room impulse response is expensive (and,
  in a real room, ever-changing), so we want a *perceptually* convincing one cheaply.
  Echo density and mode density; perceptual metrics. (book: `Artificial_Reverberation`,
  `Reverberation_Problem`, `Complexity_Exact_Reverberation`,
  `Perceptual_Aspects_Reverberation`, `Perception_Echo_Density_Mode`,
  `Perceptual_Metrics_Ideal_Reverberation`)
- **3.2** Early reflections (tapped delays, image sources) and late-reverberation
  approximations: Schroeder allpass sections and nested allpass filters. (book:
  `Early_Reflections`, `Late_Reverberation_Approximations`,
  `Desired_Qualities_Late_Reverberation`, `Schroeder_Allpass_Sections`,
  `Nested_Allpass_Filters_I`)
- **3.3** Schroeder reverberators, then **Freeverb** in detail: 8 lowpass-feedback combs
  (1116-1617 samples) in parallel, then 4 Schroeder allpasses (556, 441, 341, 225 samples,
  g = 0.5). Predict its T60 from the comb lengths and feedback, then measure it. (book:
  `Schroeder_Reverberators`, `Example_Schroeder_Reverberators`, `Freeverb`,
  `Freeverb_Main_Loop`, `Lowpass_Feedback_Comb_Filter`, `Freeverb_Allpass_Approximation`)
- **3.4** **FDN reverberation:** a lossless (orthogonal) feedback matrix, mutually prime
  delay lengths, and a per-line gain g_i = 10^(−3·M_i·T/T60), so every line decays at
  the same rate. Delay-line damping filters for frequency-dependent T60, and a tonal
  correction filter. FDNs in Faust and Zita-Rev1. Scattering delay networks. (book:
  `FDN_Reverberation`, `History_FDNs_Artificial_Reverberation`,
  `Choice_Lossless_Feedback_Matrix`, `Choice_Delay_Lengths`,
  `Achieving_Desired_Reverberation_Times`, `Delay_Line_Damping_Filter_Design`,
  `Tonal_Correction_Filter`, `FDN_Reverberators_Faust`, `Zita_Rev1`,
  `Scattering_Delay_Networks`)
  *(Room acoustics behind all this, i.e. RT60, modes and the Schroeder frequency, is the
  `room-acoustics` course.)*

## Phase 4 — Delay-Line Interpolation (chapter 4)

- **4.1** Why fractional delay: an integer delay line tunes the A440 string to
  100 or 101 samples, which are 17 cents apart. Linear interpolation, first-order allpass
  interpolation, and interpolation as resampling. Large delay changes. (book:
  `Delay_Line_Signal_Interpolation`, `Delay_Line_Interpolation`, `Linear_Interpolation`,
  `First_Order_Allpass_Interpolation`, `Linear_Interpolation_Resampling`,
  `Large_Delay_Changes`)
- **4.2** **Lagrange interpolation:** maximally flat fractional-delay FIR filters. Explicit
  coefficients, symmetry, frequency responses, and avoiding discontinuities when the delay
  changes. Relation to sinc interpolation. (book: `Lagrange_Interpolation`,
  `Fractional_Delay_Filters`, `Explicit_Lagrange_Coefficient_Formulas`,
  `Lagrange_Frequency_Response_Examples`, `Avoiding_Discontinuities_When_Changing`,
  `Relation_Lagrange_Sinc_Interpolation`)
- **4.3** **Thiran allpass interpolation:** maximally flat group delay with unity gain,
  ideal for tuning a fixed string loop. On the pin, a first-order Thiran for d = 0.727 has
  coefficient (1 − d)/(1 + d) ≈ 0.158. Its group delay. (book: `Thiran_Allpass_Interpolators`,
  `Thiran_Allpass_Interpolation_Matlab`, `Group_Delays_Thiran_Allpass`)
- **4.4** Windowed sinc interpolation: the ideal bandlimited interpolator made practical
  (and the `sasp` window trade-offs again). (book: `Windowed_Sinc_Interpolation`,
  `Theory_Ideal_Bandlimited_Interpolation`, `Theory_Practice`,
  `Summary_Windowed_Sinc_Interpolation`, `Delay_Line_Interpolation_Summary`)

## Phase 5 — Time-Varying Delay Effects (chapter 5)

- **5.1** Variable delay lines; doubling and slap-back. (book: `Time_Varying_Delay_Effects`,
  `Variable_Delay_Lines`, `Doubling_Slap_Back`)
- **5.2** Flanging (a swept feedforward comb) vs phasing (swept allpass notches); vibrato
  (a modulated delay *is* frequency modulation); chorus. (book: `Flanging`, `Phasing`,
  `Vibrato_Simulation`, `Chorus_Effect`)
- **5.3** The Doppler effect and its simulation (a delay that changes at rate dD/dt
  scales frequency by 1 − dD/dt), and the Leslie rotating speaker as Doppler plus
  amplitude modulation. (book: `Doppler_Effect`, `Doppler_Simulation`, `Leslie`)

## Phase 6 — Digital Waveguide Models (chapter 6, appendix C.1-C.7): keystone, part 1

- **6.1** The ideal vibrating string: the wave equation, its applications, and the
  **traveling-wave solution** y(t, x) = y_r(t − x/c) + y_l(t + x/c) (d'Alembert, derived
  in appendix C). **Sampled**, each traveling wave is a delay line: the digital waveguide.
  Wave impedance. (book: `Digital_Waveguide_Models`, `Ideal_Vibrating_String`,
  `Wave_Equation`, `Traveling_Wave_Solution`, `Sampled_Traveling_Wave_Solution`,
  `Wave_Impedance`, `Digital_Waveguide_Theory`, `Traveling_Wave_Solution_I`,
  `D_Alembert_Derived`, `Sampled_Traveling_Waves`, `Digital_Waveguide_Model`)
- **6.2** The ideal acoustic tube (pressure and volume-velocity waves); rigid
  terminations (velocity and displacement waves invert, force and pressure waves don't);
  a moving rigid termination; equivalent circuits. (book: `Ideal_Acoustic_Tube`,
  `Rigid_Terminations`, `Velocity_Waves_Rigid_Termination`, `Force_Pressure_Waves_Rigid`,
  `Moving_Rigid_Termination`, `Digital_Waveguide_Equivalent_Circuits`)
- **6.3** The ideal plucked string (initial displacement) and struck string (initial
  velocity), converting any string state into traveling waves. Animate them. (book:
  `Ideal_Plucked_String`, `Ideal_Struck_String`, `Converting_Any_String_State`)
- **6.4** **The damped plucked string:** losses at every sample along the string commute
  and **consolidate** into one gain per round trip, and frequency-dependent damping into one
  loop filter. That's huge computational savings, and well-posed damped-string PDEs.
  (book: `Damped_Plucked_String`, `Computational_Savings`, `Frequency_Dependent_Damping`,
  `Lossy_1D_Wave_Equation`, `Loss_Consolidation`, `Frequency_Dependent_Losses`,
  `Well_Posed_PDEs_Modeling`, `Digital_Filter_Models_Damped`)
- **6.5** The stiff string: stiffness makes high frequencies travel faster (dispersion),
  so the partials go sharp, and an allpass dispersion filter in the loop models it. The
  dispersive wave equation. (book: `Stiff_String`, `Stiff_String_Synthesis_Models`,
  `Dispersive_1D_Wave_Equation`)
- **6.6** The externally excited string; loop-filter identification from a recording
  (damping filter, dispersion filter, F0 estimation, EDR-based design). (book:
  `Externally_Excited_String`, `Loop_Filter_Identification`, `General_Loop_Filter_Design`,
  `Damping_Filter_Design`, `Dispersion_Filter_Design`, `EDR_Based_Loop_Filter_Design`)
- **6.7** String coupling effects (horizontal and vertical polarizations, coupled strings,
  longitudinal waves) and nonlinear elements. (book: `String_Coupling_Effects`,
  `Horizontal_Vertical_Transverse_Waves`, `Coupled_Horizontal_Vertical_Waves`,
  `Coupled_Strings`, `Longitudinal_Waves`, `Nonlinear_Elements`, `Memoryless_Nonlinearities`)
- **6.8** Alternative wave variables: displacement, velocity, slope, force, power, root-power
  waves, and energy in a terminated string. Choosing the variable is a modeling decision.
  (book: `Alternative_Wave_Variables`, `Force_Waves`, `Wave_Impedance_I`,
  `State_Conversions`, `Power_Waves`, `Root_Power_Waves`, `Total_Energy_Rigidly_Terminated`)

## Phase 7 — Karplus-Strong and the Electric Guitar (chapter 9.1, appendix A.8)

- **7.1** **Karplus-Strong:** a noise-filled delay line closed through (1 + z^(−1))/2.
  Build the A440 pin: 99 samples + Thiran(0.727). Predict each harmonic's T60 from
  |cos(πfT)| per period (ideal loop: ≈ 32 s at h = 1, 8 s at h = 2, 1.3 s at h = 5, 0.31 s at
  h = 10), then add a loop gain of 0.996 (≈ 3.5, 2.6, 0.96, 0.29 s) and *listen*. (book:
  `Karplus_Strong_Algorithm`, `Karplus_Strong_Algorithms`, `String_Models`)
- **7.2** The extended Karplus-Strong algorithm: pick position (a feedforward comb),
  dynamics (excitation lowpass), brightness and sustain (length-three FIR and one-zero
  loop filters). (book: `Extended_Karplus_Strong_Algorithm`, `Length_Three_FIR_Loop`,
  `Length_FIR_Loop_Filter`, `One_Zero_Loop_Filter`)
- **7.3** The electric guitar: nonlinear distortion, amplifier feedback, cabinet
  filtering, duty-cycle modulation, vacuum-tube modeling. (book: `Electric_Guitars`,
  `Nonlinear_Distortion`, `Amplifier_Feedback`, `Cabinet_Filtering`,
  `Duty_Cycle_Modulation`, `Vacuum_Tube_Modeling`)

## Phase 8 — Scattering and Waveguide Networks (appendix C.8-C.18): keystone, part 2

- **8.1** **Scattering at impedance changes:** plane-wave scattering (head-on and at an
  angle), longitudinal waves in rods, and the **Kelly-Lochbaum scattering junction**. On the
  pin, R1 = 1 → R2 = 2 gives ρ = 1/3: a third of the force wave reflects. Check energy
  conservation. (book: `Scattering_Impedance_Changes`, `Plane_Wave_Scattering`,
  `Plane_Wave_Scattering_Angle`, `Longitudinal_Waves_Rods`,
  `Kelly_Lochbaum_Scattering_Junctions`)
- **8.2** Digital waveguide filters (lattice and ladder forms), "traveling waves" in lumped
  systems, and properties of passive impedances (positive real functions). (book:
  `Digital_Waveguide_Filters`, `_Traveling_Waves_Lumped_Systems`,
  `Properties_Passive_Impedances`)
- **8.3** Loaded waveguide junctions (a mass or spring where strings meet), two coupled
  strings, and the **digital waveguide mesh** for 2-D and 3-D waves. (book:
  `Loaded_Waveguide_Junctions`, `Two_Coupled_Strings`, `Digital_Waveguide_Mesh`)
- **8.4** FDNs as digital waveguide networks (Phase 3 seen through the keystone);
  waveguide transformers and gyrators; the digital waveguide oscillator; non-cylindrical
  (conical, flared) acoustic tubes. (book: `FDNs_Digital_Waveguide_Networks_I`,
  `Waveguide_Transformers_Gyrators`, `Digital_Waveguide_Oscillator`,
  `Non_Cylindrical_Acoustic_Tubes`)

## Phase 9 — Lumped Models (chapter 7)

- **9.1** Impedance: dashpot (μ), ideal mass (m·s) and ideal spring (k/s), from the force
  and velocity relations. One-port network theory: series and parallel combinations, the
  mass-spring-wall and spring-mass systems, mechanical impedance analysis, general and
  passive one-ports. On the pin: a 1 g mass on a spring of k ≈ 7643 N/m resonates at 440 Hz.
  (book: `Lumped_Models`, `Impedance`, `Dashpot`, `Ideal_Mass`, `Ideal_Spring`,
  `One_Port_Network_Theory`, `Series_Combination_One_Ports`, `Mass_Spring_Wall_System`,
  `Parallel_Combination_One_Ports`, `Spring_Mass_System`, `Mechanical_Impedance_Analysis`,
  `General_One_Ports`, `Passive_One_Ports`)
- **9.2** Digitizing lumped models: finite-difference approximation vs the **bilinear
  transformation** (passivity preserved, frequency warped). On the pin, the bilinear 440 Hz
  resonance lands at ≈ 439.86 Hz, but 10 kHz lands at ≈ 8689 Hz. Limitations of lumped-element
  digitization. (book: `Digitization_Lumped_Models`, `Finite_Difference_Approximation`,
  `Bilinear_Transformation`, `Application_Bilinear_Transform`,
  `Limitations_Lumped_Element_Digitization`)
- **9.3** *Numerical ODEs just in time:* forward Euler (can go unstable), backward Euler,
  the trapezoidal rule (= bilinear), Newton's method for the implicit nonlinear step, and
  semi-implicit methods. (book: `More_General_Finite_Difference_Methods`,
  `General_Nonlinear_ODE`, `Forward_Euler_Method`, `Backward_Euler_Method`,
  `Trapezoidal_Rule`, `Newton_s_Method_Nonlinear_Minimization`, `Semi_Implicit_Methods`,
  `Summary_Lumped_Modeling`)

## Phase 10 — Wave Digital Filters (appendix F)

- **10.1** Wave digital elements: each lumped element (mass, spring, dashpot, source)
  becomes a reflectance in wave variables, digitized by the bilinear transform. (book:
  `Wave_Digital_Filters_I`, `Wave_Digital_Elements`)
- **10.2** **Adaptors:** series and parallel junctions of wave digital elements, the
  two-port parallel adaptor with ρ = (R2 − R1)/(R2 + R1) (the keystone's scattering again),
  and how port resistances are chosen to avoid delay-free loops. (book:
  `Adaptors_Wave_Digital_Elements`)
- **10.3** Wave digital modeling examples: build the A440 mass-spring as a WDF and compare
  it with 9.2. History of WDF models. (book: `Wave_Digital_Modeling_Examples`,
  `Wave_Digital_Filter_Models`)

## Phase 11 — Finite Differences and Their Equivalence to Waveguides (appendices C.2, D, E)

- **11.1** The finite-difference approximation of the ideal string, and its relation to
  the digital waveguide recursion. (book: `Finite_Difference_Approximation_I`,
  `FDA_Ideal_String`, `Relation_Finite_Difference_Recursion`,
  `Lossy_Finite_Difference_Recursion`)
- **11.2** Finite-difference schemes in general: convergence, the characteristic
  polynomial, and **von Neumann stability analysis** (the Courant condition c·T/X ≤ 1;
  the waveguide sits exactly at 1). (book: `Finite_Difference_Schemes`,
  `Finite_Difference_Schemes_I`, `Convergence`, `Characteristic_Polynomial_Equation`,
  `Von_Neumann_Analysis`)
- **11.3** Waveguide and FDTD equivalence: state transformations between the two,
  excitation examples, the state-space formulation, and computational complexity. When to
  use which. (book: `Equivalence_Digital_Waveguide_Finite`, `State_Transformations`,
  `Excitation_Examples`, `State_Space_Formulation`, `Computational_Complexity`)

## Phase 12 — Transfer-Function Models (chapter 8)

- **12.1** Digitizing an analog or measured response: sampling the impulse response, the
  impulse-invariant method, the matched z transformation, pole mapping with optimal
  zeros. (book: `Transfer_Function_Models`, `Outline`, `Sampling_Impulse_Response`,
  `Impulse_Invariant_Method`, `Matched_Z_Transformation`, `Pole_Mapping_Optimal_Zeros`)
- **12.2** **Modal expansion:** a resonating body as a sum of decaying sinusoids (two-pole
  resonators in parallel: `filters`' A440 resonator, many times over). General filter
  design by frequency-response matching. History of modal expansion. (book:
  `Modal_Expansion`, `Frequency_Response_Matching_Using_Digital`, `History_Modal_Expansion`,
  `Mass_Spring_Resonators`)
- **12.3** **Commuted synthesis:** because the string-body-room chain is linear, the body
  and room responses can be moved *before* the string and stored as the excitation. A
  whole guitar body for the price of a wavetable. Resonator factoring. A virtual-analog
  phaser example. (book: `Commuted_Synthesis`,
  `Extracting_Parametric_Resonators_Nonparametric`, `Virtual_Analog_Example_Phasing`)

## Phase 13 — Virtual Musical Instruments (chapter 9, appendix A)

- **13.1** Acoustic guitars: bridge and body modeling (commuted). String excitation: an
  ideal string struck by a mass, piano-hammer modeling, pluck modeling. (book:
  `Acoustic_Guitars`, `Bridge_Modeling`, `Body_Modeling`, `String_Excitation`,
  `Ideal_String_Struck_Mass`, `Piano_Hammer_Modeling`, `Pluck_Modeling`)
- **13.2** Piano synthesis: stiff and nonlinear piano strings, high-accuracy string
  modeling, commuted piano synthesis, and the piano literature. (book: `Piano_Synthesis`,
  `Stiff_Piano_Strings`, `Nonlinear_Piano_Strings`, `High_Accuracy_Piano_String_Modeling`,
  `Commuted_Piano_Synthesis`, `Literature_Piano_Acoustics_Synthesis`)
- **13.3** Woodwinds: single-reed instruments (the reed as a nonlinear valve driving a
  bore, i.e. a scattering junction with a pressure-dependent reflection coefficient), and
  tonehole modeling. (book: `Woodwinds`, `Single_Reed_Instruments`,
  `View_Single_Reed_Oscillation`, `Single_Reed_Theory`, `Tonehole_Modeling`)
- **13.4** Bowed strings: the bow-string scattering junction (stick-slip friction as a
  nonlinear reflection), extensions, and linear commuted bowed strings. (book:
  `Bowed_Strings`, `Digital_Waveguide_Bowed_String`, `Bow_String_Scattering_Junction`,
  `Bowed_String_Synthesis_Extensions`, `Linear_Commuted_Bowed_Strings`)
- **13.5** Brasses (lips and mouthpiece, bell models) and other instruments: the singing
  voice (the Kelly-Lochbaum vocal tract), flutes, recorders and pipe organs, percussion.
  (book: `Brasses`, `Modeling_Lips_Mouthpiece`, `Bell_Models`, `Other_Instruments`,
  `Singing_Voice`, `Singing_Kelly_Lochbaum_Vocal_Tract`, `Flutes_Recorders_Pipe_Organs`,
  `Percussion_Instruments`)
- **13.6** History as a map: early musical acoustics, analog computers, vocoders and
  vocal-tract models, Karplus-Strong, digital waveguides. Each step is a keystone choice.
  (book: `History_Enabling_Ideas_Leading`, `Early_Musical_Acoustics`, `Physical_Digital_Filters`,
  `Analog_Computers`, `Voice_Synthesis`, `Vocal_Tract_Analog_Models`,
  `Digital_Waveguide_Models_I`)

## Phase 14 — Putting It Together

- **14.1** Re-derive the keystone unprompted: Newton → wave equation → d'Alembert →
  delay lines → loss consolidation → loop filter + fractional delay → wave variables →
  scattering → passivity → stability, and say where each Phase 13 instrument and each
  Phase 3 reverb uses each step.
- **14.2** Capstone (pick one; record the choice in `progress.md`):
  - **(a) A virtual instrument:** an extended Karplus-Strong or waveguide guitar (pick
    position, dispersion, commuted body), or a clarinet (bore + reed junction + bell), in
    Python and Faust, played from a MIDI file and compared with a recording.
  - **(b) A reverberator:** an FDN with frequency-dependent T60 (damping filters + tonal
    correction), matched to a measured room's T60 per octave band (`room-acoustics`
    tie-in).
  - **(c) A circuit or mechanism as a WDF:** a passive tone stack, an RLC filter, or a
    mass-spring-damper chain, built from wave digital adaptors, checked against an analytic
    or SPICE response, then driven by a nonlinear element.
- **14.3** Where next: the Faust physical-modeling libraries, the book's sound examples
  and resources, the other courses, and Phase 15. (book: `Resources_Internet`)

## Phase 15 — The Frontier (a living section)

> **This phase tracks the current state of the art and is revised as the field moves.**
> It is depth-on-demand, never a gate. Each frontier topic is one session or more: it
> starts from the chapter it extends, reuses the keystone (traveling waves in delay lines;
> scattering at impedance changes; passivity), runs on a pin where possible, and ends by
> reading one paper from the sources list together. Claims marked *(empirical)* are
> benchmark results that later work may overturn. Last surveyed: **October 2026**.

- **15.1 Differentiable physical models** (extends 6, 7, 12). Karplus-Strong loops,
  waveguides and modal resonators written in a differentiable framework, so their
  parameters (loop filter, dispersion, mode frequencies and decays) are fitted to
  recordings by gradient descent, alone or controlled by a network (differentiable piano
  and string models). Stability is kept by parameterizing in the z-plane (poles inside) or
  by passivity. → `audio-ddsp/`, `audio-physics-informed/`.
- **15.2 Differentiable and neural reverberation** (extends 3). FDNs and filtered-velvet-
  noise reverbs whose matrices, delays and damping filters are optimized for colorless
  decay or to match a measured room, and networks that estimate reverb parameters from
  audio. → `room-acoustics/`, `audio-synth-effect-matching/`.
- **15.3 Wave digital filters for real circuits** (extends 10). Adaptors for arbitrary
  topologies and multiport elements (R-type adaptors), so any analog circuit (not just
  series-parallel ones) can be built as a WDF; open-source WDF libraries; diode and other
  nonlinearities modeled by networks inside an otherwise physical WDF.
- **15.4 Numerical sound synthesis at scale** (extends 11). Large finite-difference and
  finite-volume models of plates, membranes, rooms and whole instruments, run on GPUs, with
  energy methods to guarantee stability. The waveguide-FDTD trade-off of 11.3 at
  full scale.
- **15.5 Physics-informed and neural PDE solvers** (extends 1, 11). Networks trained to
  satisfy the wave equation (PINNs) or to learn its solution operator (neural operators),
  and where they stand against the classical schemes of this course. *(empirical: accuracy
  and speed claims vary widely by problem.)* → `audio-physics-informed/`.
- **15.6 Modal synthesis from data** (extends 12.2). Differentiable modal resonators for
  rigid-body impact sounds, and modal parameters estimated from shape or from recordings.
  → `audio-physics-informed/`.

### Frontier sources
- Renault, L., Mignot, R., & Roebel, A. (2022). Differentiable piano model for MIDI-to-audio
  performance synthesis. *DAFx 2022.*
- Lee, J. W., Park, J., Choi, M. J., & Lee, K. (2024). Differentiable modal synthesis for
  physical modeling of planar string sound and motion simulation. *NeurIPS 2024.*
  *(Check the paper before teaching from it.)*
- Lee, S., Choi, H.-S., & Lee, K. (2022). Differentiable artificial reverberation.
  *IEEE/ACM Trans. ASLP*, 30.
- Dal Santo, G., Prawda, K., Schlecht, S. J., & Välimäki, V. (2023). Differentiable feedback
  delay network for colorless reverberation. *DAFx 2023.*
- Välimäki, V., Holm-Rasmussen, B., Alary, B., & Lehtonen, H.-M. (2017). Late reverberation
  synthesis using filtered velvet noise. *Applied Sciences*, 7(5).
- Werner, K. J., Smith, J. O., & Abel, J. S. (2015). Wave digital filter adaptors for
  arbitrary topologies and multiport linear elements. *DAFx-15.*
- Werner, K. J. (2016). *Virtual Analog Modeling of Audio Circuitry Using Wave Digital
  Filters.* Ph.D. thesis, Stanford University (CCRMA).
- Chowdhury, J., & Clarke, C. J. (2022). chowdsp_wdf: An advanced C++ library for wave
  digital circuit modelling. *DAFx20in22.* arXiv:2210.12554.
- Chowdhury, J., & Clarke, C. J. (2022). Emulating diode circuits with differentiable wave
  digital filters. *SMC 2022.* *(Check the paper before teaching from it.)*
- Bilbao, S. (2009). *Numerical Sound Synthesis: Finite Difference Schemes and Simulation
  in Musical Acoustics.* Wiley.
- Raissi, M., Perdikaris, P., & Karniadakis, G. E. (2019). Physics-informed neural
  networks. *J. Computational Physics*, 378, 686-707.
- Li, Z., Kovachki, N., Azizzadenesheli, K., Liu, B., Bhattacharya, K., Stuart, A., &
  Anandkumar, A. (2021). Fourier neural operator for parametric partial differential
  equations. *ICLR 2021.*
- Diaz, R., Hayes, B., Saitis, C., Fazekas, G., & Sandler, M. (2023). Rigid-body sound
  synthesis with differentiable modal resonators. *ICASSP 2023.*

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question (a bank
   exercise from an earlier chapter makes good spaced review).
2. **Introduce one new concept** with an analogy/visual before any notation or code.
3. **Show**, then have the learner **do** a tiny exercise: a derivation, a few lines of
   numpy or Faust on a pin (and *listen* to it), or a bank exercise from `exercises/` for
   the current page.
4. **Verify** understanding from their answer; if shaky, re-explain a different way —
   do not advance until it's solid.
5. **Log** what was covered, the exercise, their answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
6. Keep each session ~1 hour. End with a one-sentence preview of next time, and point to
   the book page(s) to read before it.
