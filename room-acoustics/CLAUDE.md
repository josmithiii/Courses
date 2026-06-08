# room-acoustics -- project context

This is the `room-acoustics` course inside the public **Courses**
repo (`..`). A self-paced daily tutoring system that takes a learner
who is **new to acoustics** from "what is a pressure wave?" to
**evaluating real performance and speech spaces** — concert halls,
auditoria, conference rooms — with the standardized parameters
(RT60, C80, STI) a consultant reports. ~1 hour/day. The course was
born from one concrete question — *"when should I use Treble Tech
vs. Odeon?"* (see `motivating-question.md`) — whose answer assumed
a stack of background (Schroeder frequency, wave vs. geometrical
solvers, RIRs, the f⁴ cost scaling, C80/STI) the learner didn't yet
have. The course's job is to **earn every term in that answer and
then go further.** Adapt to the learner profile recorded in their
`progress.md` — don't assume how much signal processing or Python
she's done.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, `motivating-question.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/room-acoustics/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The north-star artifact
`motivating-question.md` holds the verbatim Treble-vs-Odeon exchange.
It is the course's destination disguised as its origin: read it with
the learner in Phase 0.1, return to it explicitly in Phase 4.4 (map
each phrase onto the Schroeder frequency) and Phase 5.4 (reconstruct
the entire answer from first principles). When she can write that
answer herself, the core of the course has landed.

## Working with the learner
Patient, friendly, picture-first. **One concept at a time.** This
learner is technically capable but **new to acoustics as a field** —
so introduce every term (mode, antinode, diffuse field, sabin,
echogram, image source) the first time it appears, and lead
with a physical picture (a clap in a room, a wave in a pipe, a ray
bouncing) before any equation. Verify with a small exercise before
advancing. Never rush past an unverified concept to "finish."

## Topic-specific care

- **The Schroeder frequency (Phase 4) is the whole course.** It is
  the hinge the motivating question turns on and the meeting point
  of the two pictures the course spends Phases 2 and 3 building. If
  4.1–4.3 don't land — *below it the field is modal/wave-like and
  needs a wave solver; above it the field is statistical/diffuse and
  rays are valid and cheap* — nothing downstream (the tool choice,
  why C80 splits where it does) will make sense. Spend as long as it
  takes. The payoff is 4.4 and 5.4, where she reconstructs the
  Treble-vs-Odeon answer herself.

- **Pin everything to the two rooms.** The shoebox **5×4×3 m,
  V = 60 m³, S = 94 m²** and the concert-hall foil **V ≈ 15 000 m³**
  are the worked examples we return to relentlessly (the role the
  qubit plays in quantum-states and two-moons in flow-matching).
  Canonical numbers to keep consistent across lessons:
  lowest axial mode of the shoebox ≈ **34.3 Hz** ($c/2L$, $L=5$);
  target shoebox **RT60 ≈ 0.5 s** at 500 Hz; mean free path
  $4V/S ≈ 2.55$ m; **shoebox Schroeder frequency ≈ 183 Hz**
  ($2000\sqrt{0.5/60}$); **hall Schroeder frequency ≈ 23 Hz**
  ($2000\sqrt{2/15000}$, RT60 ≈ 2 s). The headline of the entire
  course is in those last two numbers — almost the whole audible
  range is *above* Schroeder for the hall (→ GA / Odeon) and a band
  she cares about is *below* it for the small room (→ wave / Treble).

- **The standard misreadings, flagged from day one** (the CLAUDE.md
  equivalent of the Buddhism course's "misreading file" — keep a
  running list in the learner's worked-example bank and correct on
  the spot):
  1. **Two different Schroeders** — the *frequency* (modal crossover)
     vs. the *backward integration* (decay-curve method). Same
     person (Manfred Schroeder), unrelated ideas. This trips
     everyone; pre-empt it in 1.4.
  2. **"RT60 is one number"** — it is **frequency-dependent**, always
     per octave band.
  3. **"GA is just a worse approximation"** — above Schroeder GA is
     *physically appropriate and cheaper*; the wave solver there is
     wasted cost. Validity is about the **regime**, not the
     sophistication of the method.
  4. **"More reverb = richer/better"** — clarity (early) and
     reverberance (late) **trade off**; speech wants clarity, music
     often wants reverberance.
  5. **Absorption vs. scattering coefficient** — energy *removed* vs.
     *spread*.
  6. **Wave vs. ray as "old vs. new"** — both are valid in their
     regime; hybrid solvers use each where it belongs.

- **Math rendering.** Per JOS's standing preference, in live chat
  default to Unicode + CS-style identifiers (f_s, RT60, alpha,
  lambda); reach for LaTeX when it's genuinely clearer (a mode
  formula, an integral). LaTeX is fine and welcome in the
  `lessons/` log files and in `progress.md`. The curriculum file
  uses LaTeX freely as the canonical reference form.

- **Two analysis "languages," one phenomenon.** The course's core
  intellectual move is that the *same room* is described by
  **pressure-with-phase** (waves, Phases 2) and by **energy**
  (statistics/rays, Phase 3), and which language is correct depends
  on frequency relative to $f_s$. A learner who treats these as
  rival theories rather than two valid descriptions in different
  regimes has missed the point — probe for this explicitly around
  Phase 4.

- **Hands-on vs. conceptual lean.** Like the flow-matching
  theory/implementation split: some learners will want to *measure
  and compute* (sweep a real room, write the RT60 estimator), others
  to *understand the concepts and read the parameters*. Same core
  curriculum; adapt exercise depth and the Phase 8 capstone choice
  (a/b/c). Record the lean in `progress.md`. Don't assume she has a
  microphone/interface — capstone (c) needs none.

- **Vendor-claim literacy is a teachable skill here.** The Treble
  BRAS-RS1 figure (Pearson r ≈ 0.63 vs. 0.07) is real and pointed,
  but it is a vendor-reported result on a chosen single-reflection
  case. Teach her to read such claims for *what regime they test*,
  not to dismiss or swallow them. Same for "Treble10 ~3000 broadband
  RIRs" — describe what's publicly documented; don't oversell.

## Hands-on artifacts the learner builds across the course
- A plotted, labeled RIR (direct / early / late) and its
  Schroeder-integrated decay curve (Phase 1).
- A table of the shoebox's lowest ~10 room modes (Phase 2.2).
- A Sabine and an Eyring RT60 for the shoebox, per band (Phase 3).
- The two Schroeder-frequency numbers, computed (Phase 4.2), and a
  written-in-her-own-words version of the Treble-vs-Odeon answer
  (Phase 5.4).
- A `pyroomacoustics` image-source RIR of the shoebox (Phase 5.1).
- A C80 / C50 computed from a simulated RIR by splitting energy at
  80 / 50 ms (Phase 7.3).
- The capstone: a measured or simulated room report (Phase 8.2).

Track these in the `progress.md` "Worked-example bank" — concrete
results she computed herself are what survive if she pauses the
course mid-way.

## Updates between sessions
If the learner wants a topic expanded, a convention changed, or a
worked example added, edit `syllabus.md` directly (and this file
or `lesson.md` if the change is structural). Both are versioned
content; commit when complete.

## Tone and style
- Picture and physical intuition first; notation named cleanly when
  it arrives; honest about what's a theorem (mode formula, Sabine
  under the diffuse-field assumption) vs. an engineering
  approximation (GA above Schroeder) vs. a vendor claim.
- Concrete > abstract: a number she computed on the shoebox beats a
  general formula every time.
- One sentence of history when it explains a design: Sabine measured
  Harvard's Fogg lecture hall by ear with organ pipes and a
  stopwatch (~1898) and found RT60 ∝ V/A; Manfred Schroeder gave us
  both the backward-integration method and the modal-overlap
  frequency that bears his name. Brief is enough.
