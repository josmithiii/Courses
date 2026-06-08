# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- VAE background (encoder/decoder, ELBO, KL term, reparameterisation): _(shaky — rebuild in 0.2 / comfortable / strong)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- Comfort with KL divergence / mutual information (by name): _(shaky / comfortable / strong)_
- Why they're here / goal: _(understand disentanglement / build a controllable VAE / the audio editing angle / research)_
- Lean: _(hands-on — train VAEs, render traversals, compute MIG / conceptual — the decomposition & the impossibility)_
- Interested in the audio payoff (pitch/timbre)? _(yes — do tier c / not especially)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c — note: dSprites tier-a runs on CPU)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **diagnostic-first**, every term defined on first use, every
  claim about a model pinned to a rendered latent traversal (and, on the audio tier, heard)

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one frame + read `the-decomposition.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` importable
- [ ] The **dSprites** dataset fetched (737,280 binary 64×64 images, 5 known factors)
- [ ] A tiny VAE trains on dSprites and reconstructs (the foundation)
- [ ] Can render a **latent traversal** grid (sweep one z_i, decode a row of images)
- [ ] (capstone tier c, optional) a small labelled monophonic-audio set for pitch/timbre + can play audio
- [ ] `the-decomposition.md` read (the keystone — the TC decomposition & the impossibility)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The objects & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- dSprites factors: shape (3), scale (6), orientation (40), x-position (32), y-position (32).
- `q(z|x)` encoder, `p(x|z)` decoder, `p(z)=N(0,I)` prior, `β` = KL weight, `q(z)` = aggregate posterior.
- **TC** = `D_KL(q(z) ‖ Πⱼ q(zⱼ))` — dependence among latent dims (the disentanglement driver).
- The exact KL split: `E_x[KL(q(z|x)‖p(z))] = I_q(z;x) + TC + Σⱼ KL(q(zⱼ)‖p(zⱼ))`.
- **MIG** = normalized gap between the two highest-MI latent dims per factor (the robust metric).
- Latent size `K` = _(e.g. 10)_; chosen β values tried = _(e.g. 1, 4, 10)_.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has produced themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-decomposition.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "β-VAE / β-TCVAE disentangle for free, unsupervised" — no, **inductive bias required** (Locatello)
- "total correlation = the whole KL penalty" — TC is **one of three** terms
- "more β = strictly more disentanglement" — β trades reconstruction; seeds can dominate
- "a high MIG (or any one metric) proves disentanglement" — metrics disagree; average over seeds
- "the aggregate-posterior TC predicts disentanglement" — not a reliable post-hoc predictor
- "InfoGAN/β-VAE codes map to the same factors every run" — **not identifiable**
- "disentanglement reliably improves downstream tasks" — Locatello found no such evidence
- "disentanglement is unsupervised by definition" — the working audio systems (Luo) use labels
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.5) — tiered, no GPU required (dSprites is CPU-trainable)
> Picked partway through Phase 5 so it can shape the last few lessons.

- _(a) **CPU / default** — train a β-VAE on dSprites (or a subset); latent traversals at β = 1/4/10; compute MIG; one-page disentanglement report_
- _(b) **Colab GPU** — tier a, plus β-TCVAE (and optionally FactorVAE) at matched reconstruction, a multi-seed run to witness Locatello's seed variance, and the capacity ramp_
- _(c) **Local GPU / audio** — reproduce a pitch/timbre split on monophonic notes with label supervision; do a timbre/pitch swap and listen_
- Choice: _(not yet)_
