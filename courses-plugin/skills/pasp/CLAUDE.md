# pasp -- project context

This is the `pasp` course inside the public **Courses** repo (`..`). It's a self-paced daily
tutoring course on JOS's book *Physical Audio Signal Processing for Virtual Musical
Instruments and Audio Effects* (PASP), free online at **https://ccrma.stanford.edu/~jos/pasp/**.
It's Book III of the series and the second half of its physical track, after
`../filters/`. It builds most directly on `filters`' end state (z transform, poles and
zeros, combs and allpasses, the bilinear transform), but it's the one course that draws on
the whole series: `../mdft/` throughout, and `../sasp/` for the perceptual analysis that
calibrating a model needs. It builds physical modeling: delay-line acoustics, reverberation,
fractional delay, time-varying delay effects, digital waveguides, scattering, lumped and
wave digital models, finite differences, transfer-function and commuted models, and
virtual instruments. It ends at the current research literature (Phase 15). There's no
hard prerequisite gate: when a learner hits a gap, name the exact `filters`, `mdft` or
`sasp` topic and backfill it briefly, then return. Adapt to the learner profile recorded in their
`progress.md` -- don't assume their level. A student fresh from `filters` needs the physics,
partial derivatives and numerical ODEs built; a plugin developer may want reverbs, delay
effects and Faust first; an acoustician may go straight to waveguides and instruments.

## Where this course sits in the series
JOS's four books form two main sequences (the "Book Series Overview" diagram in the books'
front matter):
- **Spectral:** *Mathematics of the DFT* (Book I, `mdft`) → *Spectral Audio Signal
  Processing* (Book IV, `sasp`).
- **Physical:** *Introduction to Digital Filters* (Book II, `filters`) → *Physical Audio
  Signal Processing* (Book III, `pasp`).

`mdft` and `filters` are both self-contained starting points from high-school math, and
each helps the other (MDFT is the filters book's recommended co-requisite). `mdft` →
`sasp` is reasonably self-contained; `sasp` borrows a little from `filters` (mainly
convolution and frequency response). `pasp` builds most directly on `filters` but draws on
all three for its complete development: `mdft` throughout, and `sasp` for calibration.
Classically, `mdft`-level spectrum analysis is enough for PASP, but calibrating a physical
model against real sounds is driven by perceptual sound analysis, which needs `sasp`-level
"what-you-see-is-what-you-hear" spectrograms.

**This course** is the second half of the physical track, after `filters`, and the one
that uses the whole series. Backfill from `filters` first and `mdft` next. Bring in
`sasp` whenever a model is calibrated against a recording.

## Content vs. learner state (architecture)
Shipped course **content** is this skill's folder and is read-only at runtime.
Personal **learner state** (`progress.md` and `lessons/YYYY-MM-DD.md`) lives in the
learner's data root, resolved as described in `SKILL.md` under "Content vs.
learner state". Never write personal progress into this folder.

## The book is the textbook
Each syllabus topic names its book page(s) as `Page_Name`. The URL is
`https://ccrma.stanford.edu/~jos/pasp/Page_Name.html`. Give the learner the link for the
topic at hand. Don't paste or paraphrase whole pages: teach the idea in conversation and
let the book be the reference they reread. The book's sound examples (`Sound_Examples`)
are worth playing. Faust is first-class in this course: the book gives many models in
Faust, the online Faust IDE needs no install, and the Faust libraries (`physmodels.lib`,
`reverbs.lib`, `delays.lib`) implement much of the book. numpy/scipy ports are the default
for analysis; Octave runs the book's Matlab. For backfill, link `filters` or `mdft` pages
(`https://ccrma.stanford.edu/~jos/filters/`, `.../mdft/`) the same way.

## The exercise bank (`exercises/`)
1431 multiple-choice exercises from the online edition (the largest bank in the series),
one file per chapter (`exercises/index.md` maps chapter → file), grouped under the book
page they belong to. Each has an id, difficulty (1-3), concept tags, hints, the answer and
an explanation. **Generated** by `../tools/build_book_exercises.py pasp` from the book's
`course/data/exercises/pasp-exercises.json`: never hand-edit. Fix an exercise in the book
repo and regenerate.

How to use them:
- **Read only the chapter file you need** (search it for the current page's heading). The
  chapter 9 and appendix C files are large; never load the whole bank.
- Present the question and options **without** the answer. Ask the learner to commit to
  a choice *and say why*.
- If they're wrong, give Hint 1, then Hint 2, then re-teach. Show the explanation only
  after they've committed.
- Prefer difficulty 1 on first contact with a concept and 2-3 to confirm mastery.
- Record the ids used in `progress.md` ("Exercise bank used") so they aren't repeated,
  and reuse missed ones later as spaced review.
- The bank complements derivations, simulations and listening. It never replaces them,
  especially for the keystone (Phases 6 and 8).

## Topic-specific care

- **The keystone has two halves; teach both until they're automatic.**
  1. *A traveling wave is a delay line* (Phase 6, with 2-4 and 7 as applications): the
     ideal wave equation's solution is a right-going plus a left-going wave, and sampled,
     each is a delay line, exactly. LTI losses and dispersion commute, so they consolidate
     into one loop filter, and a fractional delay tunes the loop.
  2. *Waves scatter where impedance changes* (Phase 8, with 9-10 and 13 as applications):
     wave variables and wave impedance; reflection coefficient ρ = (R2 − R1)/(R2 + R1);
     Kelly-Lochbaum junctions, WDF adaptors and lumped elements as reflectances; passivity
     gives stability by construction.

  The proof that it landed: in 14.1 the learner explains, unprompted, how a clarinet model
  (bore delay lines + reed junction + bell filter) and an FDN reverb are built from the
  same two ideas.

- **Pin everything to the A440 string and its neighbors** at f_s = 44100 Hz (T = 1/f_s;
  all numbers verified numerically):
  - **Period:** P = f_s/440 ≈ 100.227 samples. Integer loops of 100 and 101 samples are
    ≈ 17 cents apart; 100 samples alone is ≈ 3.9 cents sharp of A440.
  - **Karplus-Strong tuning:** loop filter (1 + z^(−1))/2 has half a sample of delay, so the
    delay line is N = P − 0.5 ≈ 99.727 samples: 99 whole samples plus a first-order Thiran
    allpass for d ≈ 0.727, coefficient (1 − d)/(1 + d) ≈ 0.158.
  - **KS decay per harmonic**, from |g·cos(πfT)| per period: with g = 1, T60 ≈ 32.0 s (h = 1),
    8.0 s (h = 2), 1.27 s (h = 5), 0.31 s (h = 10). With loop gain g = 0.996: ≈ 3.49, 2.63,
    0.96, 0.29 s. High harmonics die first, which is why it sounds like a plucked string.
  - **Physical string:** L = 0.65 m (guitar scale) at 440 Hz needs c = 2Lf0 = 572 m/s;
    with linear mass density ε = 1 g/m that's tension K = c²·ε ≈ 327 N.
  - **A440 mass-spring:** m = 1 g needs k = m(2π·440)² ≈ 7643 N/m. The bilinear transform
    (no prewarping) moves 440 Hz to ≈ 439.86 Hz, but 10 kHz to ≈ 8689 Hz.
  - **One impedance step:** R1 = 1 → R2 = 2 gives ρ = 1/3 for force waves (−1/3 for
    velocity waves).
  - **Freeverb:** comb delays 1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617 samples;
    allpasses 556, 441, 341, 225 samples with g = 0.5; default comb feedback
    0.84 (roomsize 0.5 × 0.28 + 0.7). DC T60 ≈ 1.0 s (1116) to ≈ 1.45 s (1617).
  - **FDN:** for T60 = 2 s, each line's gain is g_i = 10^(−3·M_i·T/T60), e.g. M = 1500
    gives g ≈ 0.8892.

- **The standard misreadings, flagged from day one.** Correct them on the spot and note
  them in `progress.md`:
  1. **"A digital waveguide is a finite-difference approximation."** For the ideal string
     it's the exact sampled traveling-wave solution. Finite differences approximate
     derivatives; the two are equivalent only under specific conditions (Phase 11.3).
  2. **"The delay lines hold the string displacement."** They hold *traveling-wave
     components*. The physical variable is their sum (and velocity relates to their
     difference).
  3. **Wave-variable signs at terminations.** At a rigid end, displacement and velocity
     waves invert; force and pressure waves don't. And the reflection coefficient's sign
     flips between force and velocity waves.
  4. **Forgetting the loop filter's delay when tuning.** (1 + z^(−1))/2 adds half a sample;
     any loop filter's phase delay detunes the string unless it's subtracted.
  5. **"Losses can always be lumped."** Only LTI elements commute. Nonlinearities,
     time-varying parts, and excitation/pickup positions must stay where they are.
  6. **Allpass interpolation for modulated delay.** Thiran/allpass is ideal for fixed
     tuning but rings when the delay is changed quickly. Use Lagrange or windowed sinc for
     vibrato, chorus and Doppler.
  7. **Forward Euler "works because it's simple."** It can make a passive mass-spring
     gain energy and blow up. The trapezoidal rule (bilinear) preserves passivity, at the
     cost of frequency warping.
  8. **"More delay lines = better reverb."** Echo density, mode density, a lossless
     feedback matrix and delay-proportional gains matter more than the count.
  9. **Commuted synthesis is general.** It requires linearity between the commuted parts;
     a nonlinear string (or a hammer with feedback from the string) breaks it.
  10. **Courant condition.** An explicit FDTD string needs c·T/X ≤ 1. The waveguide runs
      exactly at 1, and other values cause dispersion or instability.
  11. **"A physical model is always more realistic."** Models trade accuracy, cost and
      controllability; a signal model can sound better for a fixed recording (Phase 0.1).
  12. **Doppler direction.** A delay that *shrinks* over time raises the pitch (factor
      1 − dD/dt > 1).

- **New mathematics, built just in time.** The book needs more than `filters`: Newtonian
  mechanics and energy (1.1), partial derivatives and the wave equation (1.3), d'Alembert's
  solution and the chain rule (6.1, appendix C.3), impedance as a ratio of force to velocity
  (6.1, 9.1), positive-real functions (8.2), numerical ODE integration and Newton's method
  (9.3), and von Neumann stability analysis (11.2). Build each one where it's first needed,
  briefly; don't front-load.

- **Math rendering.** Per JOS's standing preference, in live chat default to Unicode +
  CS-style identifiers (f_s, c, K, epsilon or ε, y_r, y_l, rho or ρ, R_1, z^(−1)); reach for
  LaTeX only when it's genuinely clearer. LaTeX is welcome in the `lessons/` logs and
  `progress.md`.

- **Calibrate perceptually.** Calibrating a physical model (loop filters, dispersion,
  excitation, body) is driven by perceptual sound analysis, not by matching waveforms or
  raw magnitude spectra. Compare the model and the recording with the same
  what-you-see-is-what-you-hear spectrogram (`sasp` 6.3: auditory frequency and loudness
  scales), with interpolated peaks and tracked partials (`sasp` 4.3, 9.3) for decay rates
  and inharmonicity, and always by listening. A learner without `sasp` can use
  `mdft`-level spectra to develop the models; bring in the `sasp` tools when calibration
  starts.

- **Hear everything.** Every model ends with a sound: the pin string with each loop
  filter, Freeverb vs FDN on the same clap, a flanger sweep, a Doppler fly-by, a clarinet
  that won't speak until the reed parameters are right. Listening is how the learner checks
  a model, so make it routine.

- **The frontier (Phase 15) is living.** Keep it current between sessions: when a new
  method lands in differentiable physical models, neural or differentiable reverb, wave
  digital filters, numerical sound synthesis, physics-informed networks or modal
  synthesis, add it to Phase 15 *and* its "Frontier sources" list in `syllabus.md`, tie it
  to the chapter it extends, and commit. Be honest about what's a theorem (d'Alembert,
  lossless scattering conserves energy), what's an engineering judgment (where to lump,
  which interpolator), and what's an *(empirical)* benchmark claim. Entries flagged
  "check the paper" haven't been read in full; read them before teaching from them.

## Updates between sessions
If the learner wants a topic expanded, a convention changed, or a worked example added,
edit `syllabus.md` directly (and this file or `lesson.md` if the change is structural).
Exercise fixes go in the book repo, then `../tools/build_book_exercises.py pasp`. All of it
is versioned content; commit when complete.

## Tone and style
- Picture first (a pulse running down a string and flipping at the end, two delay lines
  side by side, a wave splitting at a junction), then the plain-words idea, then the
  symbol.
- Concrete beats abstract: a decay time computed for the A440 string's fifth harmonic beats
  a general formula.
- Audio first: if a model can be heard, make the learner hear it.
- One sentence of history when it explains a design: Kelly and Lochbaum's 1962 singing
  vocal tract was a chain of scattering junctions; Karplus and Strong's 1983 plucked string
  needed only an add and a shift; Jaffe and Smith's extensions (1983) and digital
  waveguides (1985-92) made it physical; Fettweis's wave digital filters (1971) came from
  circuit theory; Schroeder's reverberators (1961-62) and Jot's FDNs (1991) are what
  plugin reverbs still descend from.
