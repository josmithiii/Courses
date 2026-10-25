# Quantum States — From Bra/Ket Notation to Density Matrices

**Learner profile:** Comfortable with linear algebra (matrices,
eigenvalues, change of basis) and complex numbers (modulus, phase,
complex inner products). Basic Newtonian mechanics and *some* prior
exposure to quantum (has heard "superposition," "wavefunction,"
maybe seen Schrödinger's equation in passing) — but the formalism
has never quite clicked. So: notation introduced cleanly and
deliberately, every abstract object pinned to a concrete two-level
example (spin-½ / qubit) the learner can compute by hand, and every
new piece of math justified by what it lets us *say* physically.
NumPy/SymPy used as a sanity-check oracle when matrices get
non-trivial — the learner verifies their pen-and-paper answer
against a 4-line script. ~1 hour per day. One concept at a time.
Every concept is verified with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on
one topic. The topic numbers below are *topics*, not days.
`progress.md` tracks the real position.

**End state:** by the last lesson, the learner can: write a quantum
state as a ket and as a column vector in a chosen basis; compute
inner products, expectation values, and measurement probabilities;
apply unitary evolution and the Pauli operators; build tensor-product
states and recognize entanglement; convert freely between |ψ⟩⟨ψ| and
the density matrix ρ; compute Tr(ρ), Tr(ρ²), and a partial trace; and
explain *why* decoherence makes ρ look diagonal in the pointer basis.
They will be able to read the first three chapters of Sakurai or
Nielsen & Chuang without the notation being an obstacle.

---

## Phase 0 — Orientation
- **0.1** What a "state" is, classically vs. quantumly. Why a list of
  position+momentum is no longer enough — and what replaces it.
- **0.2** Math toolkit refresher (just-in-time, on demand): complex
  inner product, Hermitian conjugate (dagger), unitary, eigenproblem.
  We'll only go deep where the learner is rusty.
- **0.3** Tooling: NumPy/SymPy as the "oracle" we'll use to check
  by-hand answers. Install, run `np.array([[0,1],[1,0]]) @ ...`, see
  it work.

## Phase 1 — Kets, Bras, Inner Products
- **1.1** The ket |ψ⟩ as a vector in a complex Hilbert space. Why
  "complex" matters: phases carry physics. Column-vector picture.
- **1.2** The bra ⟨φ| as the dual (row vector, conjugate-transposed).
  Why we need the conjugate and not just the transpose.
- **1.3** The inner product ⟨φ|ψ⟩: a complex number. Norm, |⟨φ|ψ⟩|²
  as a probability (foreshadowing Born).
- **1.4** Orthonormal bases; the completeness relation Σ|n⟩⟨n| = I.
  Identity-insertion as the single most useful trick in the formalism.
- **1.5** The qubit. The computational basis |0⟩, |1⟩. Writing a
  general qubit state in two equivalent forms: α|0⟩ + β|1⟩ and the
  Bloch-sphere parametrization (θ, φ). The global-phase irrelevance.
- **1.6** The Bloch sphere as a picture: north = |0⟩, south = |1⟩,
  equator = the four "superposition" states |±⟩, |±i⟩.

## Phase 2 — Operators
- **2.1** Linear operators on kets. The outer product |a⟩⟨b| as a
  rank-1 operator; matrix elements ⟨m|A|n⟩.
- **2.2** Matrix representation in a chosen basis. Change of basis as
  a unitary similarity transform. Worked example: rewriting σ_x in
  the |±⟩ basis.
- **2.3** Hermitian operators (A = A†) = **observables**. Real
  eigenvalues, orthogonal eigenvectors, spectral decomposition
  A = Σ a_n |n⟩⟨n|.
- **2.4** Unitary operators (U† U = I) = **evolutions / gates**.
  Preserve inner products. The exponential map U = exp(iH) for
  Hermitian H.
- **2.5** The Pauli operators σ_x, σ_y, σ_z. Their eigenvectors,
  eigenvalues, anticommutation, σ_i² = I. The whole single-qubit
  story sits here — work it until it's reflex.
- **2.6** Functions of operators via spectral decomposition: how to
  compute exp(-iθ σ_z / 2) without diagonalizing by hand every time.

## Phase 3 — Measurement
- **3.1** Projective measurement on an orthonormal basis {|n⟩}.
  The Born rule: P(n) = |⟨n|ψ⟩|². State collapse |ψ⟩ → |n⟩.
- **3.2** Expectation value ⟨A⟩ = ⟨ψ|A|ψ⟩. Variance and uncertainty
  ΔA. Why ⟨σ_x⟩ on |0⟩ is zero even though every measurement returns
  ±1.
- **3.3** Compatible vs. incompatible observables. The commutator
  [A, B] = AB − BA. Simultaneous eigenstates exist iff [A, B] = 0.
- **3.4** The Heisenberg uncertainty relation in operator form:
  ΔA · ΔB ≥ ½|⟨[A,B]⟩|. Worked example on σ_x and σ_z.
- **3.5** (Optional, on request) Generalized measurements (POVMs)
  intuition: not every measurement is projective.

## Phase 4 — Dynamics
- **4.1** The Schrödinger equation iħ ∂|ψ⟩/∂t = H |ψ⟩. What H is
  (the energy observable, called the Hamiltonian) and why it
  generates time evolution.
- **4.2** The time-evolution operator U(t) = exp(-iHt/ħ). Unitarity
  preserves the norm — probability is conserved.
- **4.3** Stationary states: eigenstates of H evolve by pure phase
  e^(-iE_n t/ħ). Why this makes energy eigenbases so privileged.
- **4.4** Worked example: Larmor precession. A spin-½ in a B-field
  along ẑ has H ∝ σ_z; starting from |+⟩ traces a circle on the
  Bloch equator. Verify with NumPy.
- **4.5** Briefly: Heisenberg picture (operators evolve, states
  don't). One sentence and the conversion formula — we'll come back
  to it if needed.

## Phase 5 — Composite Systems & Entanglement
- **5.1** The tensor product H_A ⊗ H_B. A two-qubit basis: |00⟩,
  |01⟩, |10⟩, |11⟩. Kronecker product on the matrix side.
- **5.2** Product states vs. entangled states. The test: can you
  factor it? The Bell state (|00⟩ + |11⟩)/√2 cannot.
- **5.3** The four Bell states as an orthonormal basis of the
  two-qubit space. Build them from |00⟩ with H ⊗ I followed by CNOT.
- **5.4** Local operators: A ⊗ I acts only on subsystem A. Worked
  example: measuring σ_z on qubit A of a Bell pair instantly fixes
  qubit B.
- **5.5** CHSH inequality at intuition level: why classical local
  hidden variables can't reproduce the Bell-state correlations.
  (Bell's theorem, no proof — just the punchline.)
- **5.6** (Optional, on request) Schmidt decomposition: any bipartite
  pure state has a canonical diagonal form; the number of nonzero
  Schmidt coefficients is one measure of entanglement.

## Phase 6 — Density Matrices (the payoff)
- **6.1** Why kets aren't enough. Two scenarios that give the same
  measurement statistics on every observable but feel different:
  "an electron prepared in |+⟩" vs. "a 50/50 statistical mixture of
  |0⟩ and |1⟩." We need an object that knows the difference.
- **6.2** Definition. For a statistical ensemble {p_i, |ψ_i⟩}, the
  density matrix is ρ = Σ p_i |ψ_i⟩⟨ψ_i|. For a pure state,
  ρ = |ψ⟩⟨ψ|.
- **6.3** Properties: ρ = ρ† (Hermitian), Tr(ρ) = 1, ρ ⪰ 0 (positive
  semidefinite). Any matrix with these three properties *is* a valid
  density matrix.
- **6.4** Pure vs. mixed test: Tr(ρ²) = 1 iff ρ is pure; otherwise
  Tr(ρ²) < 1 (mixedness ≈ 1 − Tr(ρ²)).
- **6.5** Expectation values: ⟨A⟩ = Tr(ρ A). Reproduce ⟨ψ|A|ψ⟩ from
  this for a pure state, and the mixture rule Σ p_i ⟨ψ_i|A|ψ_i⟩ for
  the mixed case.
- **6.6** The Bloch *ball*. ρ = ½(I + r·σ) for a qubit, with |r| ≤ 1.
  Pure states sit on the surface; mixed states are in the interior;
  the maximally mixed state ρ = I/2 sits at the center.
- **6.7** Time evolution: ρ(t) = U(t) ρ(0) U†(t). The
  Liouville–von Neumann equation iħ dρ/dt = [H, ρ]. Reduces to
  Schrödinger for pure states.

## Phase 7 — Reduced States and Decoherence
- **7.1** The partial trace Tr_B. Definition by basis sum; intuition:
  "the part of ρ that subsystem A can ever see, given that B is
  unobserved."
- **7.2** Worked example: Tr_B on a Bell-state |ψ⟩⟨ψ| gives ρ_A = I/2.
  A subsystem of an entangled pure state is mixed — entanglement and
  mixedness are the same phenomenon viewed locally.
- **7.3** Decoherence as entanglement with the environment, then
  forgotten. Off-diagonal elements of ρ (the "coherences") decay; ρ
  becomes diagonal in the pointer basis. Why the cat looks alive *or*
  dead, not both.
- **7.4** (Optional, on request) Open systems briefly: Kraus
  operators, the Lindblad equation, what changes when we admit ρ can
  evolve non-unitarily.

## Phase 8 — Putting It Together
- **8.1** Capstone problem. Pick one (learner's choice):
   - **(a)** Spin-½ in a B-field: write H, propagate |+⟩, compute
     ⟨σ_x(t)⟩ and ⟨σ_y(t)⟩, verify Larmor frequency, then redo it in
     density-matrix language and trace out a "noisy" environment to
     watch the Bloch vector shrink.
   - **(b)** EPR / Bell pair: build the state, compute correlators
     ⟨σ_a ⊗ σ_b⟩ at general angles, partial-trace to get ρ_A = I/2,
     and discuss what locally would and wouldn't change if you didn't
     know B existed.
   - **(c)** One-qubit gate + measurement circuit of the learner's
     design, predicted by hand and run in NumPy or `qutip`.
- **8.2** Where next. Sakurai *Modern Quantum Mechanics* (chapters
  1–3 are now readable), Nielsen & Chuang *Quantum Computation and
  Quantum Information* (chapters 2 and 8), Preskill's lecture notes
  (Caltech Ph 219, free online). Recommend one based on which way the
  learner wants to lean — physics or quantum information.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick
   recall question. If shaky, re-teach before continuing.
2. **Introduce one new concept.** Notation lands cleanly: name it,
   write it, say what it is in plain English, then say what it lets
   us *compute* that we couldn't before.
3. **Pin it to the qubit.** Almost every abstract object in this
   course can be made concrete on a 2-dimensional Hilbert space. Do
   that. The qubit is the worked example we return to relentlessly.
4. **Tiny exercise** to verify: compute by hand (one or two lines of
   matrix algebra) and check against NumPy/SymPy when it isn't
   obvious. The exercise *is* the check that the formalism landed.
5. **Common confusions** when relevant. Single most common in this
   subject: confusing a global phase with a relative phase; confusing
   a *superposition* (a pure state) with a *mixture* (a classical
   ensemble). Flag explicitly.
6. **Log** what was covered, the exercise, their answer, and a
   mastery note to `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of
   next time.

### Mastery criteria

A topic is mastered when the learner can:

1. State the definition in their own words, in one or two sentences,
   without notation cheats ("a density matrix is …, and it's needed
   because …").
2. Carry out the corresponding small computation on a qubit (or a
   two-qubit system, from Phase 5 on) by hand, and explain each step.
3. Spot a deliberately wrong claim about it ("this state is pure
   because Tr ρ = 1" — no; it's normalized).

Record this in the data-dir `progress.md` mastery log.
