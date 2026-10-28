# filters -- project context

This is the `filters` course inside the public **Courses** repo (`..`). It's a self-paced
daily tutoring course on JOS's book *Introduction to Digital Filters with Audio
Applications*, free online at **https://ccrma.stanford.edu/~jos/filters/**. It's Book II of
the series and the start of its physical track (`filters` → `../pasp/`). Like the book (a
first course in DSP), it's self-contained from high-school algebra and trigonometry: it
builds the whole of digital filter theory, from y(n) = x(n) + x(n−1) to state-space
filters and IIR design, and ends at the current research literature (Phase 12).
`../mdft/` is the recommended companion, not a prerequisite: when a learner wants more
depth on complex numbers, sinusoids or the DFT, name the exact `mdft` topic and draw on
it briefly, then return. Adapt to the learner profile recorded in their `progress.md` --
don't assume their level. A student new to complex numbers needs them built in Phase 1
(appendix A); a student fresh from `mdft` can move quickly to the z transform, partial
fractions, Laplace and circuits; an audio developer may want Phases 7-9 and 12 (and the
Faust track) right away.

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
all three for its complete development: `mdft` throughout, `sasp` lightly.

**This course** starts the physical track. `mdft` alongside it is helpful but not
required.

## Content vs. learner state (architecture)
Shipped course **content** is this skill's folder and is read-only at runtime.
Personal **learner state** (`progress.md` and `lessons/YYYY-MM-DD.md`) lives in the
learner's data root, resolved as described in `SKILL.md` under "Content vs.
learner state". Never write personal progress into this folder.

## The book is the textbook
Each syllabus topic names its book page(s) as `Page_Name`. The URL is
`https://ccrma.stanford.edu/~jos/filters/Page_Name.html`. Give the learner the link for the
topic at hand. Don't paste or paraphrase whole pages: teach the idea in conversation and
let the book be the reference they reread. The book's Matlab runs in Octave (with the
`signal` package); numpy/scipy ports are the default here, and the book's Faust examples
(chapter 3, appendix K) run in the online Faust IDE. For `mdft` backfill, link
`https://ccrma.stanford.edu/~jos/mdft/` pages the same way.

## The exercise bank (`exercises/`)
490 multiple-choice exercises from the online edition, one file per chapter
(`exercises/index.md` maps chapter → file), grouped under the book page they belong to.
Each has an id, difficulty (1-3), concept tags, hints, the answer and an explanation.
**Generated** by `../tools/build_book_exercises.py filters` from the book's
`course/data/exercises/filters-exercises.json`: never hand-edit. Fix an exercise in the
book repo and regenerate.

How to use them:
- **Read only the chapter file you need** (search it for the current page's heading). Don't
  load the whole bank.
- Present the question and options **without** the answer. Ask the learner to commit to
  a choice *and say why*.
- If they're wrong, give Hint 1, then Hint 2, then re-teach. Show the explanation only
  after they've committed.
- Prefer difficulty 1 on first contact with a concept and 2-3 to confirm mastery.
- Record the ids used in `progress.md` ("Exercise bank used") so they aren't repeated,
  and reuse missed ones later as spaced review.
- The bank complements derivations, pole-zero sketches and numpy experiments on the pins.
  It never replaces them, especially for the keystone (Phase 7).

## Topic-specific care

- **The keystone is the z-plane picture (Phase 7), earned by Phases 1-6.** LTI filters
  only scale and delay sinusoids (complex sinusoids are their eigenfunctions), so the
  frequency response says everything. H(z) = B(z)/A(z) on the unit circle *is* the
  frequency response. Gain = distances to zeros ÷ distances to poles. Stable = poles
  inside. Pole radius ↔ bandwidth and decay. Zero placement ↔ minimum/maximum phase. The
  proof that it landed: the learner sketches the amplitude response of a filter they've
  never seen from its pole-zero plot alone, then checks it with `freqz`.

- **Pin everything to four filters** at f_s = 44100 Hz (T = 1/f_s; all numbers verified
  numerically):
  - **Simplest lowpass** y(n) = x(n) + x(n−1): H(z) = 1 + z^(−1), zero at z = −1.
    G(f) = 2cos(πfT): 2 at DC, √2 (−3.01 dB re DC) at f_s/4 = 11025 Hz, 0 at f_s/2. Phase
    −πfT, so phase delay = group delay = half a sample.
  - **Comb, M = 100** (book form y(n) = x(n) + g1·x(n−M1) − g2·y(n−M2)):
    feedforward (g1 = 1, g2 = 0) has gain-2 teeth every f_s/M = 441 Hz and nulls at odd
    multiples of 220.5 Hz. Feedback y(n) = x(n) + 0.9·y(n−100) (so g2 = −0.9, the sign trap)
    has peaks of 10 (+20 dB) every 441 Hz and troughs of 0.526 (−5.6 dB). Each 100-sample
    (2.27 ms) round trip loses 0.915 dB, so T60 ≈ 149 ms.
  - **A440 resonator**, B = 20 Hz: R = e^(−πBT) ≈ 0.998576, θ = 2π·440·T, so
    A(z) = 1 − 2R cos θ z^(−1) + R² z^(−2), with a1 ≈ −1.993229 and a2 ≈ 0.997155.
    τ = −T/ln R = 1/(πB) ≈ 15.92 ms (approximation T/(1−R) ≈ 15.93 ms). T60 ≈ 6.91τ
    ≈ 110 ms. Measured −3 dB bandwidth 20.0 Hz. The peak sits at ≈ 439.9 Hz, slightly below
    the pole angle, and the *unnormalized* peak gain is ≈ +75 dB, so normalize before
    listening.
  - **Butterworth lowpass**, second order, f_c = 1 kHz (`scipy.signal.butter(2, 1000,
    fs=44100)`, bilinear with prewarping): b ≈ [0.004604, 0.009208, 0.004604],
    a ≈ [1, −1.799096, 0.817512]. Exactly −3.01 dB at 1 kHz. Poles at radius ≈ 0.9042.

- **The standard misreadings, flagged from day one.** Correct them on the spot and note
  them in `progress.md`:
  1. **The feedback sign.** y(n) = Σ b x − Σ a y with a_0 = 1, so H = B/A. To *add*
     0.9·y(n−1) you set a_1 = −0.9. scipy, Octave and the book agree; many web examples
     don't.
  2. **"The frequency response is H(z)."** It's H(z) *on the unit circle*. A pole makes a
     peak only if it's close to the unit circle.
  3. **Stability is about poles only** (for causal filters): every pole strictly inside
     the unit circle. Zeros anywhere are fine.
  4. **Phase delay ≠ group delay.** Phase delay is how far a sinusoid moves; group delay is
     how far a narrowband envelope moves. They coincide only for linear phase.
  5. **Linear phase isn't zero phase.** Linear phase = constant delay (causal possible).
     Zero phase needs a noncausal (even) impulse response or forward-backward filtering.
  6. **Wrapped phase.** Unwrap before differentiating, or group delay comes out as
     garbage spikes.
  7. **The resonator peaks at its pole angle, at the gain you expect.** It peaks slightly
     off it (439.9 vs 440 Hz), and the raw peak gain is enormous for poles near the unit
     circle, so normalize.
  8. **The frequency response describes the steady state.** Transients (start-up ringing)
     are extra, and long for poles near the unit circle.
  9. **Filter order isn't the number of coefficients.** It's the maximum delay in the
     difference equation (the transfer function's order).
  10. **The bilinear transform warps frequency.** An analog cutoff maps to a different
      digital cutoff unless you prewarp.
  11. **"Stable coefficients stay stable when they move."** A time-varying direct-form
      filter can blow up even if every frozen-in-time setting is stable. That's why
      sweeps and virtual-analog filters use other structures (8.4, 12.1).
  12. **Pole-zero cancellation in practice.** Canceling a pole with a zero rarely works
      under roundoff, and never try to cancel an *unstable* pole.

- **New mathematics, built just in time.** If they're new: complex numbers and Euler's
  identity (1.2, appendix A; `mdft` Phases 1-3 for depth). Then, for everyone: the z
  transform and region of convergence (5.1), polynomial roots and partial fractions
  (5.2-5.3), derivatives for group delay (6.2), the Laplace transform and capacitor/inductor
  circuit laws (11.1-11.2), and matrices and eigenvalues for state space (4.4, 11.4). Build
  each one where it's first needed, briefly; don't front-load.

- **Math rendering.** Per JOS's standing preference, in live chat default to Unicode +
  CS-style identifiers (f_s, T, H(z), z^(−1), B(z)/A(z), R, theta or θ); reach for LaTeX
  only when it's genuinely clearer. LaTeX is welcome in the `lessons/` logs and
  `progress.md`.

- **Hear everything.** Every filter in the course gets white noise, an impulse train and a
  short music clip through it. The comb and resonator are unmistakable by ear, and that
  makes the pole-zero picture stick.

- **The frontier (Phase 12) is living.** Keep it current between sessions: when a new
  method lands in virtual-analog filtering, differentiable IIR filters, deep state-space
  models or neural circuit modeling, add it to Phase 12 *and* its "Frontier sources" list
  in `syllabus.md`, tie it to the chapter it extends, and commit. Be honest about what's a
  theorem (stability ⇔ poles inside, for causal LTI filters), what's an engineering
  judgment (which structure, which design method), and what's an *(empirical)* benchmark
  claim. Entries flagged "check" haven't been read in full; read them before teaching from
  them.

## Updates between sessions
If the learner wants a topic expanded, a convention changed, or a worked example added,
edit `syllabus.md` directly (and this file or `lesson.md` if the change is structural).
Exercise fixes go in the book repo, then `../tools/build_book_exercises.py filters`. All of
it is versioned content; commit when complete.

## Tone and style
- Picture first (the unit circle with poles and zeros on it, a ruler measuring distances
  from a point walking around it), then the plain-words idea, then the symbol.
- Concrete beats abstract: a pole radius computed for the A440 resonator beats a general
  formula.
- Audio first: if a filter can be heard, make the learner hear it.
- One sentence of history when it explains a design: Karplus and Strong's 1983 plucked
  string is a feedback comb with a lowpass in the loop; the biquad peaking EQ descends
  from analog parametric equalizers; the bilinear transform is the trapezoidal rule from
  numerical integration.
