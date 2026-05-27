# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Generative-model background: _(none / heard of diffusion / read a DDPM tutorial / trained one / actively use them)_
- ODEs and vector fields: _(rusty / comfortable basics / strong)_
- Probability (densities, expectations, change of variables): _(rusty / comfortable / fluent)_
- PyTorch: _(none / beginner / comfortable / strong)_
- Optimal transport: _(never heard of it / heard the word / used POT or Sinkhorn before)_
- Goal lean: _(theory track — proofs and derivations / implementation track — reproduce paper figures / "I just want the simulation-free trick to click")_
- Time budget: ~1 hour/day
- Style: patient, friendly, derivation introduced cleanly, every abstract
  object pinned to a 2-D toy distribution, PyTorch as the oracle

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The generative-modeling landscape (after the Lesson 0 interview)
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] Python + PyTorch importable (CPU is fine; CUDA optional)
- [ ] `torchdiffeq` or `scipy.integrate` available for ODE solves
- [ ] matplotlib working (we plot samples + vector fields every phase)
- [ ] (Optional) `POT` (`pip install POT`) — used in Phase 7 for OT couplings
- [ ] A scratch `.py` file or notebook open and being used during sessions
- [ ] Source PDFs accessible (`/l/dttd/FlowStuff/` on JOS's machine, or downloaded from arXiv)

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has computed by hand and runnable scripts
> they've written, kept as reference for later lessons. Add a one-line
> entry each session.

- (none yet)

## Common confusions to revisit
> The two perennial traps in this subject. The tutor watches for these and
> notes when one comes up; we revisit later to make sure it has stuck.

- Marginal $u_t(x)$ vs. conditional $u_t(x \mid x_1)$ (the CFM trick)
- Velocity $u_t$ vs. score $\nabla\log p_t$ (related but not equal in general)
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.2)
> Picked partway through Phase 6 so it can shape the last few lessons.

- _(a) MNIST/CIFAR FM (UNet sketch + sampling loop)_
- _(b) 2-D audio-flavored: distribution of pitch/loudness/timbre vectors or spectral envelopes_
- _(c) Three-way comparison: independent CFM vs. reflow-RF vs. OT-CFM on a single dataset, one figure_
- Choice: _(not yet)_
