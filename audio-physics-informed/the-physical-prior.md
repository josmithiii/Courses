# The Physical Prior — This Course's Keystone

Room-acoustics has the Schroeder frequency; audio-codecs has the fork; audio-ddsp has
the gradient through a DSP block. **This course has the physical prior as inductive
bias.** Every model in this course is the same bargain: *the equations of motion give
you part of the answer for free, and a network learns whatever the equations leave out.*
The only design question that matters is **where the network goes** — and the answer
depends on what you know, what you can measure, and what you want to control. Read this
in Phase 0.1, return to it in **Phase 3** (learnable modal models), **Phase 4** (PINNs),
**Phase 5** (hybrids), and recite it from memory in **Phase 6.1**.

Every term in **bold** is earned somewhere in the syllabus; the phase that earns it is
noted in brackets.

---

## The prior, in one sentence

> A vibrating object is a **linear system** whose free response is a sum of **modes** —
> decaying sinusoids whose **frequencies**, **decay rates**, and **shapes** are fixed by
> geometry, material, and boundary conditions [Phase 1] — so a physical model *knows*
> the note's partials and their decays before hearing a sample, and the network only
> has to learn what the physics does not fix: the **excitation**, **nonlinearity**,
> **unmodeled losses**, and **coupling** [Phase 3–5].

## What the physics gives you for free

| Physical fact | What it fixes in the model | Earned in |
|---|---|---|
| Eigenproblem `K φ = ω² M φ` | The mode **frequencies** `f_k` and **shapes** `φ_k`; for a string `f_n = n f_1`, with stiffness `f_n = n f_1 √(1 + B n²)` | Phase 1.1, 1.4 |
| Proportional (Rayleigh) damping `C = αM + βK` | Per-mode **decay rate** `d_k = (α + β ω_k²)/2`, hence `T60_k = 6.91 / d_k` | Phase 1.2 |
| Modal superposition (orthogonality) | The response is **N decoupled 2nd-order ODEs** → N parallel **2-pole resonators** | Phase 1.3 |
| Excitation / pickup mode-shape values `φ_k(r_e) φ_k(r_p)` | The mode **amplitudes** `a_k` — move the mic, only `a_k` change | Phase 1.3, 2.3 |
| Material `E, ρ, η` and geometry scale `s` | `f_k ∝ √(E/ρ)/L`, `f_k ∝ 1/s`; damping harder to predict than frequency | Phase 1.4 |
| Wave equation (string, membrane, plate) | The same modes, now in **traveling-wave** coordinates — the **waveguide** | Phase 1.5 |
| Source–filter decomposition | Excitation and resonator are **separable**; commuted synthesis | Phase 1.5, 5.2 |

## What the network must learn

Everything the linear, proportionally-damped, perfectly-known model leaves out:

- **The excitation.** A real pluck or strike is not an impulse: finite contact time
  (**Hertz contact**, force `F ∝ δ^{3/2}`) low-passes the modes it excites [Phase 2.3].
- **The damping detail.** Frequency-dependent, non-proportional, boundary and radiation
  losses — measured per mode in practice, not predicted [Phase 1.2, 2.1].
- **Nonlinearity.** Friction/bowing (stick–slip feedback), large-amplitude string
  behavior, contact — the linear prior is silent here [Phase 2.4].
- **Coupling and radiation.** Body resonances, sympathetic strings, directional
  radiation — the part that makes a guitar sound like *that* guitar [Phase 5].
- **Whatever you couldn't measure.** Geometry mismatch, surface imperfections, the
  parameter you don't know — exactly the **inverse-problem** setting where PINNs earn
  their keep [Phase 4.3].

## The note, modeled three ways

```
   the plucked note  x(t)   (mono, 44.1 kHz, ~6 s — measured partials f_k, T60_k, a_k in Phase 0.3)
          │
          ├─(1) MODAL BANK ──────────── Σ_k a_k e^{-d_k t} sin(2π f_k t)   ▶ N biquads, params FITTED
          │        physics fixes: the FORM (decaying sinusoids, one resonator per mode)
          │        network/optimizer learns: f_k, d_k, a_k  (Diaz & Hayes 2023 — Phase 3)
          │
          ├─(2) PINN ────────────────── u_θ(x, t)  with  loss = ‖PDE residual‖² + ‖BC/IC‖² + ‖data‖²
          │        physics fixes: the EQUATION (damped stiff string), enforced in the loss
          │        network learns: the SOLUTION FIELD — and, in inverse mode, unknown B, damping (Phase 4)
          │
          └─(3) HYBRID ──────────────── physical core (modal / waveguide)  +  learned excitation / residual
                   physics fixes: the STRUCTURE (source → resonator → radiation)
                   network learns: what the structure leaves out (Phase 5)
```

Same note, three places to put the prior: in the **form**, in the **loss**, or in the
**structure**. Phase 6 puts all three side by side and *listens*.

## Where the network goes — the decision table

| Level | The prior lives in… | The network learns… | Examples (this course) | Earned in |
|---|---|---|---|---|
| **Parameter-level** | The synthesis *form* (resonator bank, harmonic-plus-noise) | The parameters `f_k, d_k, a_k`, or a map from shape/material → parameters | Differentiable modal resonators (Diaz & Hayes 2023); DDSP-Piano inharmonicity (Renault 2022); wav2shape (Han & Lostanlen 2020) | Phase 3 |
| **Structure-level** | A differentiable *physical model* (waveguide, Kelly–Lochbaum tract, DRC topology) | Its physical controls (area function, glottal source; threshold/ratio/ballistics) | Vocal-tract area estimation by gradient descent (Sudholt 2023); grey-box DRC (Wright & Välimäki 2022) | Phase 5.1, 5.3 |
| **Residual-level** | A physical *source–filter* split | The excitation, or the residual the physics can't explain | Neural source–filter models (Wang 2019); learned embeddings + FDN (Götz 2025) | Phase 5.2, 5.4 |
| **Loss-level** | The *PDE residual* as a loss term | The solution field `u(x,t)` and, jointly, unknown coefficients | PINNs (Raissi et al. 2017/2019; Kim's CCRMA survey 2023) | Phase 4 |
| **Architecture-level** | The *operator* (Fourier-space layers) | The PDE's solution operator, from data | Fourier Neural Operators (Li et al. 2020) — *mentioned only* | Phase 4.5, 7 |

Rule of thumb the course drives toward: **put the prior as low in the table as the
physics is trustworthy, and no lower.** Known linear resonator? Parameter-level. Known
topology but unknown controls? Structure-level. Known equation, unknown coefficients or
geometry? Loss-level. No trustworthy equation? Then you're back in Track A's learned
latents — and that's a legitimate answer too.

---

## The misreadings this course exists to kill

Curated from the `modal-synthesis`, `pinn`, `ddsp`, and `synth-effect-matching` wikis.
The tutor flags each on the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "A PINN is a faster PDE solver." | For **well-posed forward problems** classical FEM/FDM/FVM are still **more accurate** and usually faster per solve; PINNs have no convergence guarantees. Their value is **inverse / incomplete-model** problems, noisy data, and being **mesh-free** — plus cheap inference once trained. | Phase 4.3–4.4 |
| "Modal synthesis is just additive synthesis." | The sinusoids are not free: their frequencies, damping, and amplitudes come from an **eigenproblem** with physically constrained relations (`f_n = n f_1 √(1+Bn²)`, `d_k` from material, `a_k` from mode shapes at excitation/pickup). Change the material and *every* mode moves together. | Phase 1.1–1.4 |
| "Waveguide and modal synthesis are different physics." | The **same linear system** in different coordinates — traveling waves vs standing waves. For a lossless string they are exactly equivalent (Karplus–Strong = an N-mode sum). They differ in cost, control, and where nonlinearity is easy. | Phase 1.5 |
| "More modes = better." | Cost is `O(N)` per sample; above ~5 kHz modes are too dense to fit individually; 95%+ of modes are below audibility at any instant (amplitude culling). Perceptual relevance, not count. | Phase 1.3, 2.2, 7 |
| "A physics prior removes the need for data." | It **reduces** the data needed and constrains the solution; the network still fits the excitation, damping detail, and residual — and a wrong prior (bad geometry scan, wrong boundary condition) fits the residual with garbage. | Phase 3, 5, 6 |
| "Damping is as predictable as frequency." | Frequency follows from `E, ρ`, geometry; **damping** mixes material, boundary, and radiation losses and is usually **measured per mode** (Q from 5 to 10 000). | Phase 1.2, 2.1 |
| "The inharmonic partials mean the model is wrong." | Stiffness makes `f_n = n f_1 √(1+Bn²)` — inharmonicity **is** the physics (piano, guitar); a model that can't stretch partials is the wrong one. | Phase 1.4, 3.2 |
| "The differentiable modal fit will find the true modes." | Spectral loss has **many-to-one** valleys (course 2's keystone); a fit finds *a* bank that matches the note, not necessarily the eigenmodes. Initialize from measured peaks. | Phase 3.4, 6.2 |
