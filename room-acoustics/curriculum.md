# Room Acoustics — From a Pressure Wave to Evaluating a Concert Hall

**Learner profile:** Technically comfortable and curious, but **new
to acoustics as a field.** May know a little signal processing (the
word "convolution" isn't scary, has perhaps heard of impulse
responses or reverb) but has *not* been taught room modes, the
Schroeder frequency, reverberation theory, or the standardized
parameters (RT60, C80, STI) that acoustic consultants report. The
motivating moment: she asked an expert *"when should I use Treble
Tech vs. Odeon?"* and got an answer dense with terms —
**Schroeder frequency, wave vs. geometrical solvers, modal
behavior, RIRs, C80, STI, the f⁴ cost scaling** — that assumed
background she doesn't yet have. This course builds exactly that
background, and then keeps going until she can evaluate a real
space herself. So: intuition and a picture first, every abstract
quantity pinned to **one shoebox room she can actually compute**,
notation and Python introduced just-in-time. ~1 hour/day, one
concept at a time, each checked with a small exercise before
moving on.

**Pace philosophy:** It is completely fine to spend multiple days on
one topic. The topic numbers below are *topics*, not days.
`progress.md` tracks the real position.

**The pedagogical "qubit" — one shoebox room, analyzed two ways.**
The way the flow-matching course returns relentlessly to a 2-D
toy distribution and the quantum course to a single qubit, this
course returns to **one small room: 5.0 m × 4.0 m × 3.0 m
(volume V = 60 m³, surface S = 94 m²)**, plus a **concert-hall
foil (V ≈ 15 000 m³)**. We compute the shoebox's discrete room
modes (the *wave* picture), its Sabine reverberation time (the
*statistical/ray* picture), and the **Schroeder frequency where
the two pictures meet** (≈ 180 Hz for the shoebox; ≈ 23 Hz for
the hall — which is why the whole audible range of a big hall is
"above Schroeder"). Every formula in the course is first evaluated
on these two rooms before it's trusted.

**The north-star question** (`motivating-question.md` in this
folder is the verbatim Treble-vs-Odeon exchange that motivated the
course). By Phase 5 the learner can reconstruct that entire answer
from first principles; by Phase 8 she can go further and produce
the measured numbers a consultant would.

**End state:** by the last lesson the learner can: explain what a
room impulse response (RIR) is and read its three parts (direct,
early reflections, late tail); compute the low room modes of a
shoebox and explain why low frequencies are "lumpy"; compute a
reverberation time with Sabine's and Eyring's equations and say
when each applies; compute the Schroeder frequency and use it to
decide whether a job is "wave" or "ray"; explain what geometrical
(image-source + ray tracing) and wave-based (FEM/BEM/FDTD) solvers
actually do, why wave solvers cost ~f⁴, and therefore *exactly*
why Treble (hybrid wave+GA) and Odeon (pure GA) sit where they do;
explain how two ears and the precedence effect turn physics into
the sensations of clarity, reverberance, and spaciousness; define
and interpret the ISO 3382 / STI parameter battery (EDT, T30, C80,
C50, D50, Ts, G, LF, IACC, STI) with their good ranges and
just-noticeable-differences; and **measure or simulate a real
room and write a one-page acoustic report.**

---

## Phase 0 — Orientation
- **0.1** What this course covers, in one picture: the question
  *"is the physics I care about below or above the Schroeder
  frequency?"* is the hinge the whole course (and the whole
  Treble-vs-Odeon answer) turns on. No formulas yet — just the
  story: small rooms ring with discrete modes (a wave problem);
  big rooms wash sound into a diffuse decay (a ray/energy problem);
  one number, the Schroeder frequency, tells you which regime
  you're in. Read `motivating-question.md` together; promise that
  every term in it will be earned.
- **0.2** Set up tools (the lean is chosen later — see capstone).
  Python with `numpy`, `scipy`, `matplotlib`; for the hands-on
  track also `sounddevice` (audio I/O) and `pyroomacoustics` (a
  small image-source room simulator + RT estimators). Optionally
  install **Room EQ Wizard (REW)**, the standard free measurement
  GUI. Verify: plot a sine, play/record one second of audio,
  `import pyroomacoustics`.
- **0.3** Two numbers that scaffold everything: the speed of sound
  **c ≈ 343 m/s** (at 20 °C) and wavelength **λ = c/f**. Compute λ
  at 50 Hz (≈ 6.9 m — *room-sized*, the seed of why low
  frequencies behave as waves) and at 5 kHz (≈ 6.9 cm — *tiny*,
  the seed of why high frequencies behave as rays). This single
  contrast is the physical reason the Schroeder frequency exists.

## Phase 1 — The Room Impulse Response (the central object)
- **1.1** Sound is a pressure wave in air; loudness in decibels.
  Sound pressure level $\text{SPL} = 20\log_{10}(p/p_0)$,
  $p_0 = 20\,\mu\text{Pa}$. Why dB (the ear is logarithmic; "60 dB
  of decay" is a factor of 1000 in pressure, 10⁶ in energy).
- **1.2** A room is a **linear time-invariant (LTI) system.** Clap
  your hands → the room answers with its **impulse response**
  $h(t)$. Any sound you make comes out **convolved** with $h$:
  $y(t) = (x * h)(t)$. *Auralization preview:* convolve an
  anechoic clip with a hall's RIR and you "teleport" the source
  into the hall. This is what every simulator is ultimately
  computing.
- **1.3** Anatomy of an RIR / **echogram**: the **direct sound**
  (first arrival), **early reflections** (discrete, from nearby
  surfaces, first ~80 ms), and the **late reverberant tail**
  (dense, statistical decay). Plot a real or simulated RIR and
  label the three regions by eye. This three-part split is the
  thread tying Phases 4–7 together (early vs. late is where
  clarity, the precedence effect, and C80/C50 all live).
- **1.4** **Reverberation time RT60** = time for the sound energy
  to drop 60 dB after the source stops. We don't measure 60 dB of
  clean decay directly — we use **Schroeder backward integration**
  of the RIR to get a smooth **energy-decay curve**, then fit a
  line over a cleaner range and extrapolate: **T20** (−5 to
  −25 dB) and **T30** (−5 to −35 dB). *(Flag the name clash now:
  this "Schroeder integration" and the "Schroeder frequency" of
  Phase 4 are two different ideas from the same person, Manfred
  Schroeder.)*

## Phase 2 — The Wave Picture (below Schroeder): Room Modes
- **2.1** Standing waves in 1-D. Between two hard walls a distance
  $L$ apart, only wavelengths that "fit" survive:
  $f_n = n\,c/(2L)$, $n = 1, 2, \dots$ — pressure **antinodes** at
  the walls, **nodes** in between. Compute the lowest mode of the
  shoebox's 5 m length: $343/(2\cdot5) = 34.3$ Hz.
- **2.2** A 3-D shoebox has modes indexed by $(n_x, n_y, n_z)$:
  $$f = \tfrac{c}{2}\sqrt{(n_x/L_x)^2 + (n_y/L_y)^2 + (n_z/L_z)^2}.$$
  **Axial** (one index nonzero), **tangential** (two), **oblique**
  (three). Compute and *list the lowest ~10 modes of our shoebox*
  in a table — they are sparse and unevenly spaced down low. **This
  is why a sub in a small room is boomy at some notes and weak at
  others.**
- **2.3** Modal **density** (modes per Hz) grows like $f^2$, while
  each mode has a fixed **bandwidth** $\Delta f \approx 2.2/\text{RT60}$.
  So as frequency rises, modes get closer together *and* fatter —
  eventually they overlap into a smooth response. Below that, the
  response is "lumpy"; this lumpiness is the wave regime. (We
  quantify the crossover in Phase 4 — this is its setup.)
- **2.4** What rays *cannot* capture and waves can: **diffraction**
  (sound bending around/through obstacles when λ ≳ obstacle),
  **interference** (two paths add by phase, not just energy), and
  **phase** itself. Below Schroeder these dominate — which is the
  whole reason a wave solver is needed there. A 2-D `pyroomacoustics`
  or analytic demo of two reflections cancelling at one frequency
  and reinforcing at another.

## Phase 3 — The Statistical Picture (above Schroeder): Reverberation
- **3.1** The **diffuse-field** assumption: high up, so many
  overlapping modes that energy is uniform and arrives equally
  from all directions. Now sound is bookkept as **energy**, not
  pressure-with-phase. **Mean free path** between reflections
  $= 4V/S$ (compute for the shoebox: $4\cdot60/94 \approx 2.55$ m).
- **3.2** **Sabine's equation:** $\text{RT60} = 0.161\,V/A$ (SI;
  $V$ in m³, total absorption $A = \sum_i S_i \alpha_i$ in m²
  sabins; the constant is 0.161 in metric, 0.049 in feet).
  Absorption coefficient $\alpha \in [0,1]$ is **per octave band**
  and per material. Pick plausible $\alpha$'s for the shoebox's
  surfaces and compute RT60 at 500 Hz (target ≈ 0.5 s — this fixes
  the number we reuse everywhere).
- **3.3** **Eyring–Norris:** $\text{RT60} = 0.161\,V/(-S\ln(1-\bar\alpha))$.
  Why it's preferred when the average absorption $\bar\alpha$ is
  high (Sabine over-predicts a "dead" room because it can't make
  RT60 reach zero); show it reduces to Sabine for small
  $\bar\alpha$. **Air absorption** adds extra high-frequency decay
  that matters in large halls.
- **3.4** **Critical distance** (reverberation radius): the
  distance from the source where the direct field and the
  reverberant field are equal. Closer = you hear the source;
  farther = you hear the room. This is why a talker is intelligible
  up close but mushy at the back of a live hall — and the seed of
  the speech-intelligibility story in Phase 7.

## Phase 4 — The Schroeder Frequency: Where the Two Pictures Meet
> **The keystone of the course.** Spend as long as it takes.
- **4.1** **Modal overlap.** Below: modal spacing > bandwidth →
  isolated resonances (Phase 2). Above: spacing < bandwidth → modes
  blur together → statistical field (Phase 3). The crossover is
  where roughly **3 modes overlap** within one bandwidth.
- **4.2** **The Schroeder frequency:**
  $$f_s \approx 2000\sqrt{\frac{\text{RT60}}{V}}\quad[\text{Hz, RT60 in s, }V\text{ in m}^3].$$
  Derive its *shape* from 4.1 and 2.3 (set modal density × bandwidth
  ≈ 3). **Compute it for both rooms:** shoebox → $2000\sqrt{0.5/60}
  \approx 183$ Hz; concert hall → $2000\sqrt{2/15000} \approx 23$ Hz.
  *The headline of the course lives in those two numbers.*
- **4.3** The organizing sentence, now earned: **below $f_s$ the
  field is modal / wave-like / discrete → a wave solver is needed;
  above $f_s$ it is statistical / diffuse → rays (geometrical
  acoustics) are valid and far cheaper.** Everything before this
  was building the two sides; everything after is consequences.
- **4.4** **Re-read the north-star question.** Map each phrase of
  the Treble-vs-Odeon answer onto $f_s$: "control rooms, studios,
  small critical-listening spaces, anything where the answer below
  ~200–300 Hz matters" → *high $f_s$, the band of interest is
  below it* → wave. "Concert halls, auditoria… where the band of
  interest sits comfortably above Schroeder" → *low $f_s$* → GA.
  The learner should now be able to explain the heuristic in her
  own words. (Full tool reconstruction comes in 5.4.)

## Phase 5 — How the Software Actually Computes This
- **5.1** **Geometrical acoustics (GA).** Treat sound as rays
  (valid when λ ≪ surfaces, i.e. above $f_s$). **Image-Source
  Method** — mirror the source across each wall; exact for specular
  reflections but cost explodes with reflection order, so it's used
  for **early** reflections. **Ray / cone tracing** — shoot many
  rays, tally energy; scales to the **late** tail. **Radiosity** —
  diffuse energy exchange between surface patches. The standard
  architecture is **hybrid: image-source early + ray tracing
  late.** Run a `pyroomacoustics` image-source sim of the shoebox
  and watch an RIR fall out.
- **5.2** **Wave-based numerical methods** — **FEM**, **BEM**,
  **FDTD** (and DG/spectral). They discretize the actual wave
  equation, so they get modes, diffraction, interference, and
  phase right. The price: you need ~6–10 **elements per
  wavelength**, so the number of unknowns scales like $(f/c)^3$ in
  3-D, and total solve cost scales **roughly as $f^4$** (three
  space dimensions + time). Double the top frequency → ~16× the
  cost. **This single scaling law is why wave solvers are
  prohibitive at high frequency in large rooms.**
- **5.3** Two material numbers the solvers need: **absorption
  coefficient** $\alpha$ (how much energy a surface *swallows*) vs.
  **scattering/diffusion coefficient** $s$ (how much it *spreads*
  vs. mirror-reflects). Don't conflate them. Wave solvers also need
  **watertight geometry** (no gaps), an extra modeling burden GA
  tolerates more loosely.
- **5.4** **Reconstruct the whole answer.** **Treble** = hybrid
  *wave below $f_s$* + *GA above*, cloud (the wave part is
  expensive), watertight geometry, broadband RIRs and a Python SDK
  → right when low-frequency/modal fidelity is the product (control
  rooms, device acoustics, ML-RIR datasets, ANC). **Odeon** = pure
  GA, desktop, mature material library and full ISO-3382 + STI
  reporting, seconds-not-hours → right for large-room
  consulting-style work above Schroeder. Discuss validation/benchmark
  literacy: a vendor's "Pearson r = 0.63 vs. 0.07" on the BRAS RS1
  single-reflection case is a *real and pointed* result, but it's a
  vendor-reported figure on a chosen case — read such claims for
  what regime they test. **She can now write the answer herself.**

## Phase 6 — How Rooms *Sound*: Spatial Hearing (physics-led)
- **6.1** **Two ears.** **Interaural time difference (ITD)** — sound
  reaches the near ear up to ~0.6–0.7 ms sooner; dominant for
  localization below ~1.5 kHz. **Interaural level difference (ILD)**
  — the head shadows the far ear; dominant at high frequency. The
  **duplex theory** = ITD low + ILD high. One paragraph on the
  **HRTF** (the ear/head/torso filter that lets us externalize and
  place sounds in 3-D).
- **6.2** The **precedence (Haas) effect.** The **first wavefront
  wins** localization; reflections arriving within ~1–40 ms are
  *fused* with the direct sound (they add loudness and richness,
  not separate echoes); past a ~50 ms **echo threshold** (speech) a
  reflection is heard as a distinct echo. **This is why "early" vs.
  "late" is a perceptual boundary, not just a clock reading.**
- **6.3** That boundary is exactly why the clarity parameters split
  where they do: **C80** (music) integrates energy before/after
  **80 ms**, **C50** and **D50** (speech) at **50 ms**. Early energy
  → **clarity / intelligibility**; late energy → **reverberance /
  fullness**. **The central design tension:** speech wants high
  clarity (low RT, high C50); music often wants more reverberance —
  "more reverb = better" is *false in general* and depends on use.
- **6.4** **Spaciousness has two parts.** **ASW** (apparent source
  width) is driven by **early lateral** reflections; **LEV**
  (listener envelopment) by **late lateral** energy. Both are why
  great concert halls are *narrow* (shoebox halls deliver strong
  early lateral reflections) and why **IACC** (interaural
  cross-correlation) and **LF** (lateral energy fraction) are
  measured at all.

## Phase 7 — The Evaluation Toolkit (the consultant's parameters)
- **7.1** The **ISO 3382** family and the measurement protocol:
  an **omnidirectional source** (dodecahedron loudspeaker) at
  source positions, calibrated mics at receiver positions, an
  **exponential sine sweep** deconvolved to the RIR (Phase 8 does
  this for real). Parameters are reported **per octave band**, then
  often averaged (e.g. 500 Hz + 1 kHz).
- **7.2** **Reverberation parameters:** **EDT** (early decay time,
  0 to −10 dB ×6 — tracks *perceived* reverberance better than
  T30), **T20**, **T30**. Always frequency-dependent — plot RT vs.
  band for the shoebox.
- **7.3** **Clarity / definition / strength:** **C80**, **C50**,
  **D50** (= early/total energy ratio, %), **Ts** (centre time, the
  energy "centre of gravity" in ms), **G** (sound strength,
  loudness relative to the same source at 10 m in free field).
  Compute C80 from a (simulated) RIR by splitting its energy at
  80 ms.
- **7.4** **Speech intelligibility: STI** (and the portable
  **STIPA**), 0–1, rated Bad/Poor/Fair/Good/Excellent. It's built
  from how well the room preserves the **modulation** of the
  speech envelope across bands (the modulation transfer function) —
  reverberation and noise both smear modulation and pull STI down.
  This is the headline number for **conference rooms, auditoria,
  classrooms, transit announcements.**
- **7.5** **Spatial parameters & JNDs:** **LF/LFC** and **IACC** for
  spaciousness. Then the practical question *"is a change audible?"*
  — **just-noticeable-differences**: EDT/T30 ≈ 5%, C80 ≈ 1 dB,
  G ≈ 1 dB. A report that moves a number by less than its JND has
  changed nothing a listener can hear.

## Phase 8 — Putting It Together
- **8.1** **The tool-choice decision tree**, assembled from the
  whole course: (volume → $f_s$) → is the band of interest below or
  above it? → modal/wave vs. statistical/ray → is the deliverable a
  *physically-faithful broadband RIR / low-frequency truth* (Treble)
  or *standardized large-room parameters, fast and cheap* (Odeon /
  GA)? Sketch the **Schroeder crossover as a function of $V$ and
  RT60** — the "quick rule for which tool wins" the original answer
  offered to draw. She draws it.
- **8.2** **Capstone — pick one** (chosen partway through Phase 6 so
  it shapes the last lessons):
  - **(a) Python from scratch.** *Measure* a real room: play an
    exponential sine sweep through a speaker, record it, deconvolve
    to the RIR (Farina's method), Schroeder-integrate, and compute
    **RT60/EDT/C80/C50/D50** (and STI if a calibrated speech path is
    available) — all in `numpy`/`scipy`. Or *simulate* a room with
    `pyroomacoustics` if no mic/interface. Output: a one-page room
    report. (Matches JOS's build-it-yourself house style.)
  - **(b) REW + light Python.** Measure a real room in **Room EQ
    Wizard**, read off RT/EDT/C50, export the RIR, and reproduce one
    or two parameters in Python to prove you understand the math
    behind the GUI's numbers.
  - **(c) Dataset / conceptual.** Analyze provided or synthesized
    RIRs — e.g. a small `pyroomacoustics` "control room" vs. a large
    "hall" — compute the parameter battery for each, and tie every
    difference back to the Schroeder frequency and the early/late
    split.
- **8.3** **Where to go next.** Standards & books: **ISO 3382-1/2/3**
  (performance / RT / open-plan), **IEC 60268-16** (STI),
  **Kuttruff, *Room Acoustics***, **Beranek, *Concert Halls and
  Opera Houses***. Software: `pyroomacoustics`, **REW**, the
  **Treble SDK**, **Odeon/CATT-Acoustic** (GA). Open threads that
  connect to her interests: low-frequency control and modal EQ,
  variable/active acoustics, **ML-based RIR generation and ANC**
  (where the Treble10-style broadband-RIR datasets come from).

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick
   recall question. If shaky, re-teach before continuing.
2. **Introduce ONE new concept.** A picture or physical analogy
   first (a clap in a room, a wave in a pipe, a ray bouncing), then
   the plain-English meaning, then — only when needed — the
   notation, naming every new symbol the first time it appears.
3. **Pin it to the shoebox (and the hall foil).** Almost every
   quantity in this course — modes, RT60, the Schroeder frequency,
   C80, the mean free path — can be computed on the 5×4×3 m room
   and contrasted with the 15 000 m³ hall. Do that. A number she
   computed herself beats a formula she read.
4. **Tiny exercise** to verify: a hand computation, a plot, or a few
   lines of Python (`numpy`/`pyroomacoustics`). The exercise *is*
   the check that the idea landed.
5. **Common confusions** when relevant (see the list below) —
   flag and correct on the spot; don't let a misreading set.
6. **Log** what was covered, the exercise, the answer, and a mastery
   note to `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of
   next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State it in her own words in a sentence or two, no notation
   crutch ("the Schroeder frequency is where modes start
   overlapping, so below it you need a wave solver and above it rays
   are fine").
2. Carry out the matching small computation — a mode, an RT60, a
   C80, a plot — and explain each step.
3. Spot a deliberately wrong claim ("geometrical acoustics is just a
   worse approximation that's always less accurate than a wave
   solver" — no: above Schroeder it's *physically appropriate* and
   far cheaper; the wave solver there is wasted cost).

### Common confusions to flag from day one
- **Two different Schroeders.** The **Schroeder frequency** (modal
  crossover, Phase 4) vs. **Schroeder backward integration** (the
  decay-curve method, Phase 1.4). Same person, unrelated ideas.
- **"RT60 is one number."** It is **frequency-dependent** — always
  per octave band; a room can be live in the bass and dead in the
  treble.
- **"GA is wrong / just an approximation."** Above Schroeder GA is
  the *physically correct and economical* choice; below it, it
  misses modes, diffraction, and phase. The tool's validity is a
  function of the **regime**, not its sophistication.
- **"More reverberation is richer/better."** Clarity (early energy)
  and reverberance (late energy) **trade off**, and the right
  balance differs for **speech (wants clarity)** vs. **music (often
  wants reverberance).**
- **Absorption vs. scattering coefficient** — energy *removed* vs.
  energy *spread*; different inputs to a solver.
- **Wave vs. ray as "old vs. new."** Neither is obsolete; **hybrid**
  solvers (Treble) use *each where it's valid*. That's the point.

### Source / reference materials
- **`motivating-question.md`** (this folder) — the verbatim
  Treble-vs-Odeon exchange the course is built to make fully legible.
- Kuttruff, *Room Acoustics* (the standard text); Beranek, *Concert
  Halls and Opera Houses*; **ISO 3382-1/2/3**, **IEC 60268-16 (STI)**.
- Software the course touches: `pyroomacoustics` (image-source sim +
  RT/parameter estimators), **Room EQ Wizard (REW)**, **Treble SDK**
  (hybrid wave+GA, cloud), **Odeon** / **CATT-Acoustic** (GA).
