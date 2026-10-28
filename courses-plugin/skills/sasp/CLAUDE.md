# sasp -- project context

This is the `sasp` course inside the public **Courses** repo (`..`). It's a self-paced daily
tutoring course on JOS's book *Spectral Audio Signal Processing* (SASP), free online at
**https://ccrma.stanford.edu/~jos/sasp/**. It's Book IV of the series and the second half
of its spectral track, after `../mdft/` (*Mathematics of the DFT*). It starts at `mdft`'s
end state (complex numbers, the DFT as projection, the
Fourier theorems, a first numpy spectrum analysis) and climbs as high as each of the
book's topics reaches, ending at the current research literature (Phase 12). There's no
hard prerequisite gate. When a learner hits an `mdft` gap, name the exact `mdft` topic and
backfill it briefly, then return. The same goes for the little SASP borrows from
`../filters/` (convolution and frequency response). Adapt to the learner profile recorded in their
`progress.md` -- don't assume their level. A student fresh from `mdft` needs every new
tool (integrals, probability, linear programming, multirate notation) built; a working
audio engineer may want to jump to Phases 7-10 and the frontier.

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

**This course** is the second half of the spectral track, after `mdft`. When a
filters idea comes up (convolution, frequency response), backfill it from `filters`.

## Content vs. learner state (architecture)
Shipped course **content** is this skill's folder and is read-only at runtime.
Personal **learner state** (`progress.md` and `lessons/YYYY-MM-DD.md`) lives in the
learner's data root, resolved as described in `SKILL.md` under "Content vs.
learner state". Never write personal progress into this folder.

## The book is the textbook
Each syllabus topic names its book page(s) as `Page_Name`. The URL is
`https://ccrma.stanford.edu/~jos/sasp/Page_Name.html`. Give the learner the link for the
topic at hand. Don't paste or paraphrase whole pages: teach the idea in conversation and
let the book be the reference they reread. The book's Matlab runs in Octave (with the
`signal` package); numpy/scipy ports are the default here. For `mdft` backfill, link
`https://ccrma.stanford.edu/~jos/mdft/` pages the same way.

## The exercise bank (`exercises/`)
712 multiple-choice exercises from the online edition, one file per chapter
(`exercises/index.md` maps chapter → file), grouped under the book page they belong to.
Each has an id, difficulty (1-3), concept tags, hints, the answer and an explanation.
**Generated** by `../tools/build_book_exercises.py sasp` from the book's
`course/data/exercises/sasp-exercises.json`: never hand-edit. Fix an exercise in the book
repo and regenerate.

How to use them:
- **Read only the chapter file you need** (search it for the current page's heading). Don't
  load the whole bank; it's large.
- Present the question and options **without** the answer. Ask the learner to commit to
  a choice *and say why*.
- If they're wrong, give Hint 1, then Hint 2, then re-teach. Show the explanation only
  after they've committed.
- Prefer difficulty 1 on first contact with a concept and 2-3 to confirm mastery.
- Record the ids used in `progress.md` ("Exercise bank used") so they aren't repeated,
  and reuse missed ones later as spaced review.
- The bank complements derivations and numpy experiments on the pin. It never replaces
  them, especially for the keystone (Phases 2, 7, 8).

## Topic-specific care

- **The keystone has two halves; teach both until they're automatic.**
  1. *The window transform is the shape every sinusoid takes in a spectrum* (Phase 2,
     applied in 3 and 4): main-lobe width ↔ resolution, side-lobe level ↔ dynamic range,
     roll-off ↔ smoothness of the window's edges. No window is best for everything.
  2. *The STFT is one array read two ways* (Phases 7-8): by frames (OLA, COLA in time) or
     by channels (FBS, Nyquist(N) on the window transform), dual via Poisson summation.
     Phases 9-10 (phase vocoder, SMS, MDCT, PR filter banks) are choices inside this
     picture, and Phase 12 is the research literature on those choices.

  The proof that it landed: in 11.1 the learner explains, unprompted, why a phase
  vocoder uses Hann at 75% overlap, why SMS uses a long Blackman-Harris window plus zero
  padding, and why MP3 uses a critically sampled cosine-modulated bank.

- **Pin everything to the A440 tone** at f_s = 44100 Hz (all numbers verified
  numerically):
  - **The tone:** f0 = 440 Hz, harmonics h = 1..5 with amplitude 1/h, 1 s. Optional
    exponential decay, added white noise, or a −60 dB extra partial (for dynamic range).
  - **The neighbor:** A#4 = 440·2^(1/12) ≈ 466.16 Hz, so Δf ≈ 26.16 Hz.
  - **Resolution rule** M ≥ K·f_s/Δf, with K = main-lobe width in bins (rectangular 2,
    Hann 4, Hamming 4, Blackman 6). For A4 vs A#4: rectangular ≈ 3371 samples (76 ms),
    **Hann ≈ 6742 (153 ms)**, Blackman ≈ 10113 (229 ms). For the tone's own harmonics
    (440 Hz apart) Hann needs only M ≥ 401.
  - **Peak side lobes** (measured): rectangular −13.3 dB, Hann −31.5, Hamming −42.7,
    Blackman −58.1. Asymptotic roll-off: rectangular −6 dB/oct, Hann −18, Hamming −6,
    Blackman −18.
  - **Default STFT:** periodic Hann M = 1024 (≈ 23.2 ms), R = 512, N = 2048 (bin
    ≈ 21.53 Hz). 440 Hz lies at bin ≈ 20.43. The raw peak bin 20 says 430.7 Hz;
    quadratic (dB-parabola) interpolation gives p ≈ 0.435 and **≈ 440.04 Hz**.
  - **COLA:** periodic Hann (`scipy.signal.get_window('hann', M)`, or
    `np.hanning(M+1)[:M]`) at R = M/2 sums to exactly 1. Symmetric `np.hanning(M)` does
    not.
  - **Bridge from `mdft`:** the N = 64 cosine half a bin off peaks at ≈ 20.4 (−3.9 dB),
    which is the rectangular window's worst-case *scalloping loss*.
  - **Processing gain:** doubling M raises a sinusoid's peak ≈ 3 dB above a white-noise
    floor.

- **The standard misreadings, flagged from day one.** Correct them on the spot and note
  them in `progress.md`:
  1. **"Longer window = better."** Longer M buys frequency resolution and processing
     gain, and it costs time resolution (attack smear, pre-echo). There's always a
     trade-off.
  2. **Resolution depends on the window length M, not the FFT size N.** Zero padding (N > M)
     interpolates the spectrum (good for peak interpolation) but never separates two
     close sinusoids.
  3. **"There's a best window."** Main-lobe width vs side-lobe level is a trade-off;
     choose by the job (resolution, dynamic range, amplitude accuracy, COLA).
  4. **Symmetric vs periodic windows.** `np.hanning(M)` is symmetric (for filter
     design); STFT/COLA work needs the periodic form. This silently breaks perfect
     reconstruction.
  5. **Not every hop is COLA.** Hann: R = M/2, M/3, M/4, … ; rectangular: R = M (or divisors
     of M). Check the overlap-add sum numerically before trusting a resynthesis.
  6. **The periodogram doesn't get less noisy with longer data.** Its variance stays put;
     averaging (Welch) is what reduces it.
  7. **Peak height ≠ amplitude.** A sinusoid of amplitude A peaks at A·Σw(n)/2, so normalize
     by the window sum. dB of amplitude is 20 log10, of power 10 log10.
  8. **"Magnitude is the spectrum; phase is noise."** Modifying magnitudes and keeping
     the old phases (or random ones) is what causes phasiness and smearing. The phase
     vocoder, PGHI and iSTFT vocoders are all about getting phase right.
  9. **Critically sampled ≠ oversampled.** An STFT with R < M is redundant (easy PR,
     robust to modification). The MDCT/PQMF are critically sampled: PR relies on alias
     *cancellation* between channels, which modifications can break.
  10. **An impulse is not white noise** (book 6.10). Same flat magnitude spectrum, but it's
      a deterministic signal, not a random process.

- **New mathematics, built just in time.** The book needs more than `mdft`: integrals
  (1.1), the Poisson summation formula (1.3, 7.3), probability and stochastic processes
  (5.1, appendix C), Gaussian integrals (2.6, appendix D), linear programming (2.7),
  maximum likelihood (4.4), polyphase/multirate notation (10.1). Build each one where it's
  first needed, from the `mdft` level, briefly; don't front-load.

- **Math rendering.** Per JOS's standing preference, in live chat default to Unicode +
  CS-style identifiers (f_s, M, R, N, W(ω), X_m(ω_k)); reach for LaTeX only when it's
  genuinely clearer. LaTeX is welcome in the `lessons/` logs and `progress.md`.

- **Hear everything.** SASP is an *audio* book: every phase on the pin should end with
  listening (the windowed tone, the resynthesis, the stretched result, the residual,
  the quantized subbands). A spectrogram plus the sound beats either alone.

- **The frontier (Phase 12) is living.** Keep it current between sessions: when a new
  method lands in phase retrieval, TSM, time-frequency analysis, differentiable
  sinusoidal modeling, spectral losses or neural filter banks, add it to Phase 12 *and*
  its "Frontier sources" list in `syllabus.md`, tie it to the chapter it extends, and
  commit. Be honest about what's a theorem (COLA/Nyquist duality, PR conditions), what's
  an engineering judgment (window choice), and what's an *(empirical)* benchmark claim
  that may not last. Entries flagged "check the paper" were found in a quick survey and
  haven't been read in full. Read the paper before teaching from it.

## Updates between sessions
If the learner wants a topic expanded, a convention changed, or a worked example added,
edit `syllabus.md` directly (and this file or `lesson.md` if the change is structural).
Exercise fixes go in the book repo, then `../tools/build_book_exercises.py sasp`. All of it
is versioned content; commit when complete.

## Tone and style
- Picture first (a window's transform sliding along the spectrum, a stack of frames, a
  bank of filters), then the plain-words idea, then the symbol.
- Concrete beats abstract: a number measured on the A440 pin beats a general formula.
- Audio first: if a concept can be heard, make the learner hear it.
- One sentence of history when it explains a design: Dudley's 1939 channel vocoder was
  a filter bank; Flanagan and Golden's 1966 phase vocoder added the phase; McAulay-Quatieri
  and Smith-Serra (PARSHL, 1985-87) turned it into sinusoidal modeling; Princen and
  Bradley's 1986 TDAC gave MP3 and AAC their MDCT.
