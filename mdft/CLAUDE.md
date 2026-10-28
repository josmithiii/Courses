# mdft -- project context

This is the `mdft` course inside the public **Courses** repo (`..`). It's a self-paced daily
tutoring course on JOS's book *Mathematics of the Discrete Fourier Transform (DFT), with
Audio Applications* (2nd ed.), free online at **https://ccrma.stanford.edu/~jos/mdft/**.
It takes a **high-school student who is good at math** from the quadratic formula to
practical spectrum analysis. The book was written to be self-contained from that level, and
in years of teaching from it JOS held to that. The course holds to it too: nothing beyond
high-school algebra and trigonometry is assumed. Calculus, complex numbers, linear algebra
and signal processing are all built here, just in time. Adapt to the learner profile
recorded in their `progress.md` -- don't assume their level. A strong student may race
through Phases 1-3; an adult engineer may only want Phases 4-8.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `progress.template.md` (seed copied on first run), `.claude/commands/lesson.md`,
  `exercises/` (the generated exercise bank), this file.
- **Learner state (NOT in repo):** under `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/mdft/`
  -- `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The book is the textbook
Each syllabus topic names its book page(s) as `Page_Name`. The URL is
`https://ccrma.stanford.edu/~jos/mdft/Page_Name.html`. Give the learner the link for the
topic at hand ("read this before next time" or "this is where today's idea lives"). Don't
paste or paraphrase whole pages: teach the idea in conversation, and let the book be the
reference they can reread. Quote a formula or a short passage when it helps. The book's
Matlab code runs unchanged in Octave; numpy ports are the default in this course.

## The exercise bank (`exercises/`)
425 multiple-choice exercises from the online edition, one file per chapter
(`exercises/index.md` maps chapter → file). Within a file they're grouped under the book
page they belong to, and each has an id, difficulty (1-3), concept tags, hints, the answer
and an explanation. **Generated** by `../tools/build_book_exercises.py mdft` from the book's
`course/data/exercises/mdft-exercises.json`: never hand-edit. Fix an exercise in the book
repo and regenerate.

How to use them:
- **Read only the chapter file you need** (search it for the current page's heading). Don't
  load the whole bank.
- Present the question and options **without** the answer. Ask the learner to commit to
  a choice *and say why*. Multiple choice can be guessed; the reason can't.
- If they're wrong, give Hint 1, then Hint 2, then re-teach. Show the explanation only
  after they've committed.
- Prefer difficulty 1 on first contact with a concept and 2-3 to confirm mastery.
- Record the ids used in `progress.md` ("Exercise bank used") so they aren't repeated,
  and reuse missed ones a few sessions later as spaced review.
- The bank complements the tutor's own exercises (by-hand on the pins, small numpy
  experiments, "explain it back"). It never replaces them, especially in Phases 4-5.

## Topic-specific care

- **The keystone is Phases 4-5: the DFT is a change of coordinates onto orthogonal
  sinusoids.** X(k) = ⟨x, s_k⟩ is "how much of sinusoid k is in x", and the inverse DFT
  adds the projections back up. Phases 1-3 exist to make "sampled complex sinusoid" mean
  something. Everything after Phase 5 applies the picture. If 4.4-5.4 don't land, nothing
  downstream will make sense; spend as long as it takes. The proof that it landed: in 5.4
  the learner computes the N = 4 DFT of the pin by hand and answers the 0.3 mystery
  questions themselves.

- **Pin everything to the quarter-rate cosine** x(n) = cos(2πn/4). Canonical numbers, kept
  consistent across lessons (all verified numerically):
  - **N = 2 geometry pin:** x = [3, 1] = 2·[1, 1] + 1·[1, −1]. Projection coefficients 2
    and 1. Length-2 DFT X = [x0 + x1, x0 − x1] = [4, 2], and the coefficients are X(k)/N.
  - **N = 4 DFT sinusoids:** s_0 = [1, 1, 1, 1], s_1 = [1, j, −1, −j],
    s_2 = [1, −1, 1, −1], s_3 = [1, −j, −1, j]. Each has ‖s_k‖ = 2 = √N.
  - **N = 4 pin:** x = [1, 0, −1, 0] gives **X = [0, 2, 0, 2]**, and
    x = (s_1 + s_3)/2 = (e^(jθ) + e^(−jθ))/2 = cos θ. The complex sinusoid s_1 alone gives
    X = [0, 4, 0, 0]. Parseval: Σ x² = 2 = (1/4)(2² + 2²).
  - **N = 4 shift:** a one-sample delay gives [0, 1, 0, −1] (that's sin(2πn/4)) with
    X = [0, −2j, 0, 2j]: each X(k) is multiplied by (−j)^k = e^(−j2πk/4).
  - **N = 64 pin (book ch. 8):** f = 0.25 cycles/sample gives |X| = **32 = N/2** at bins 16
    and 48, zero elsewhere. A cosine of amplitude A peaks at A·N/2.
  - **Half a bin off:** f = 0.25 + 0.5/64 gives peaks ≈ **20.4** at bins 16 and 17
    (≈ −3.9 dB re 32), and every bin is nonzero (≈ −26 dB at the far bins). That's leakage.
  - **Bookkeeping:** f_s = 44100 Hz, N = 1024 gives ≈ 43.07 Hz per bin. T60 = ln(1000)·τ
    ≈ 6.91 τ. ≈ 6.02 dB per bit.
  - **Echo comb:** h = δ(n) + γδ(n − τ) has |H(k)|² = 1 + γ² + 2γ cos(2πkτ/N).

- **The standard misreadings, flagged from day one.** Correct them on the spot and note
  them in `progress.md`:
  1. **i vs j vs `1j`.** Math class says i, the book says j, numpy says `1j`, Octave
     accepts both. Same number.
  2. **"Two peaks for one cosine — the second one is an error."** It's the negative
     frequency: bin N − k is bin −k. Real signals always give mirror-image (Hermitian)
     spectra.
  3. **Bin number is not Hz.** Bin k is k·f_s/N Hz. And bins above N/2 are negative
     frequencies, not "high" frequencies.
  4. **"The peak height is the amplitude."** The unnormalized DFT of a cosine of amplitude
     A peaks at A·N/2 (A·N for a complex sinusoid). numpy's `fft` doesn't normalize, and
     its `ifft` divides by N.
  5. **DFT shifts and convolutions are circular**, not linear (modulo-N indexing).
     Zero-pad when you need linear convolution.
  6. **"Zero padding increases resolution."** It interpolates the same underlying
     spectrum more densely. Only a longer window resolves two close sinusoids.
  7. **"Leakage means the FFT made a mistake."** The signal isn't periodic in N samples;
     the DFT is exactly right about the periodic extension it sees.
  8. **Phase of a numerical zero.** `np.angle` of a 1e-16 leftover looks like random
     phase (and numpy prints `-0.`). Threshold the magnitude before plotting phase.
  9. **0- vs 1-based indexing.** In numpy X[0] is DC; in the book's Matlab/Octave code
     it's X(1). Flag it whenever porting book code.
  10. **The minus sign in e^(−j2πkn/N)** isn't arbitrary: it is the conjugate in the inner
      product ⟨x, s_k⟩.

- **High-school bridges, built just in time and briefly.** The book builds these, and so
  does the course, only where the next idea needs them: the derivative as a slope (2.2,
  for "why e"), Taylor series (2.3, for Euler), logs and dB (3.2), vectors in N dimensions
  (4.1), matrix multiplication (5.6). Don't front-load them, and don't skip them for a
  student who hasn't seen them.

- **Math rendering.** Per JOS's standing preference, in live chat default to Unicode +
  CS-style identifiers (f_s, X(k), s_k(n), e^(j2πkn/N), omega or ω); reach for LaTeX only
  when it's genuinely clearer. LaTeX is welcome in the `lessons/` logs and `progress.md`.

- **Hands-on vs. by-hand lean.** Some learners will want to *compute* (numpy, plots,
  sound), others to *derive* (paper and pencil, proofs). The core is the same; adapt the
  exercise mix and the Phase 9 capstone (a/b/c). Record the lean in `progress.md`. Hearing
  the signals (`IPython.display.Audio` in Colab, `sounddevice` locally) makes Phases 3 and
  7 land for most students.

- **Phase 10 is a living bridge, not a SOTA phase.** The DFT is settled mathematics.
  Phase 10 maps where it goes next: the STFT and everything built on it (the sequel course
  `../sasp/`, on *Spectral Audio Signal Processing*, https://ccrma.stanford.edu/~jos/sasp/),
  the MDCT (`audio-codecs/`), spectral losses (`audio-ddsp/`) and convolution reverb
  (`room-acoustics/`). A learner who finishes `mdft` is ready to start `sasp`.

## Updates between sessions
If the learner wants a topic expanded, a convention changed, or a worked example added,
edit `syllabus.md` directly (and this file or `lesson.md` if the change is structural).
Exercise fixes go in the book repo, then `../tools/build_book_exercises.py mdft`. All of it is
versioned content; commit when complete.

## Tone and style
- Picture first (an arrow, a spinning wheel, a shadow), then the plain-words idea, then
  the symbol. A high-school student should never meet an unexplained symbol.
- Concrete beats abstract: a DFT they computed by hand at N = 4 beats the general formula.
- Honest about what's a definition (j² = −1), what's a theorem (orthogonality, Parseval),
  and what's a practical judgment (which window, how much zero padding).
- One sentence of history when it helps: Euler found e^(jθ) = cos θ + j sin θ in the
  1740s; Gauss had an FFT in 1805, decades before Fourier's work was published; Cooley and
  Tukey rediscovered it in 1965, and that's why spectrum analysis is cheap today.
