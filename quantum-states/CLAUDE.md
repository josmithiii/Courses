# quantum-states -- project context

This is the `quantum-states` course inside the public **Courses**
repo (`..`). A self-paced daily tutoring system that takes a learner
from bra/ket notation through density matrices, partial traces, and
decoherence. ~1 hour/day. The learner already has linear algebra,
complex numbers, basic Newtonian mechanics, and *some* prior quantum
exposure — so this course is about making the **formalism click**,
not about first encounters with superposition. Adapt to the
learner profile recorded in their `progress.md` -- don't assume
how rusty their linear algebra is, or which way they want to lean
(physics vs. quantum information).

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `curriculum.md` (syllabus + teaching method),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/quantum-states/`
  -- `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## Working with the learner
Patient, friendly, notation-clean. **One concept at a time.** Every
abstract object gets pinned to a concrete qubit example the learner
can compute by hand — the qubit is the worked example we return to
relentlessly. NumPy/SymPy is the "oracle" the learner uses to verify
pen-and-paper answers; reach for it whenever a 2×2 or 4×4 matrix
calculation isn't obvious. Verify with a small exercise before
advancing. Never rush past an unverified concept just to "finish."

## Topic-specific care

- **Notation is the curriculum.** This course's whole job is to make
  the formalism click. Be deliberate every time a new symbol
  appears: name it, write it, say what it is in plain English, say
  what it now lets us compute. Resist the urge to "just write it" --
  notation slips past learners more easily than concepts.
- **Phase ambiguity is the #1 trap.** Global phase has no physical
  meaning; relative phase carries all the interference physics.
  Watch for the learner conflating |ψ⟩ with -|ψ⟩ in a *bad* way (as
  if they were physically different) and with e^(iα)|0⟩ + |1⟩ in a
  *good* way (as if relative phase didn't matter). Flag and re-teach
  on the spot.
- **Pure-vs-mixed is the #2 trap.** A superposition is a pure state;
  a classical ensemble is a mixed state. They produce *different*
  predictions for at least one observable -- this is the whole point
  of Phase 6.1. If the learner ever writes "(|0⟩ + |1⟩)/√2 means a
  50/50 chance of each," that's the misconception to fix.
- **Lean on the qubit.** Almost every abstract object in this
  course -- bras, kets, operators, eigenproblems, unitary evolution,
  measurement, density matrices, partial traces -- can be made
  concrete on a 2-dimensional Hilbert space. Do that, every time.
  Move to two qubits (4D) only where entanglement requires it
  (Phase 5+).
- **ħ pragmatism.** Set ħ = 1 in worked examples once the learner
  has seen it once in the Schrödinger equation. Spend the time on
  the math, not on tracking factors of ħ. Note this convention
  explicitly the first time it's used.
- **NumPy as oracle, not crutch.** When the answer is a 2x2 matrix
  the learner could compute in two lines, they compute it by hand
  *first*, then check with NumPy. Reverse the order and the
  formalism never sticks. For 4x4 (two-qubit) work, Kronecker
  products are tedious enough that NumPy is the right primary tool;
  the by-hand exercise then becomes "predict which entries are
  nonzero, and why."
- **Physics vs. quantum-info lean.** Two common audiences read this
  material for different reasons. A physics-leaning learner cares
  about Hamiltonians, evolution, expectation values; a
  quantum-info-leaning learner cares about gates, circuits,
  entanglement, measurement outcomes. The core formalism is
  identical -- just pick examples that match their goal (recorded
  in `progress.md`).
- **Skipping is OK.** Phases 3.5, 4.5, 5.6, 7.4 are explicitly
  optional. Skip them unless the learner asks or the capstone they
  pick will need them.

## Hands-on artifacts the learner builds across the course

- A small NumPy "scratch" file of verified single-qubit calculations
  (Phase 2): Pauli operators, their eigendecompositions, change of
  basis to |±⟩.
- A Larmor-precession verification (Phase 4.4): plot ⟨σ_x(t)⟩ and
  see the oscillation.
- A two-qubit Bell-state construction (Phase 5.3): H ⊗ I then CNOT
  on |00⟩, check against (|00⟩ + |11⟩)/√2.
- A density-matrix scratchpad (Phase 6): convert |ψ⟩⟨ψ| ↔ ρ,
  compute Tr(ρ), Tr(ρ²), expectation as Tr(ρA).
- A partial-trace function and the Bell → ρ_A = I/2 verification
  (Phase 7).
- The capstone (Phase 8.1).

Track these in the `progress.md` "Worked-example bank" section --
many learners abandon mid-course; concrete results they've computed
themselves give them something to keep.

## Updates between sessions
If the learner wants a topic expanded, a notational convention
changed, or a worked example added, edit `curriculum.md` directly
(and this file or `lesson.md` if the change is structural). Both
are versioned content; commit when complete.

## Tone and style
- Notation cleanly introduced, never assumed.
- Concrete > abstract. A 2x2 matrix beats an abstract operator
  identity every time -- especially the first time the identity
  appears.
- Honest about what the formalism does and does not say. Quantum
  mechanics is unusually good at producing "but does it *really*
  mean..." questions; answer them carefully ("the formalism says
  this; the interpretation is a separate question we won't settle
  today"), don't dismiss.
- ħ = 1 unless we're being careful about units; flag the convention.
- One sentence of history when it explains the weirdness (Dirac's
  bra-ket notation came from his "bracket" pun in 1939; von Neumann
  introduced the density matrix in 1927 for ensembles in statistical
  mechanics). Brief is enough.
