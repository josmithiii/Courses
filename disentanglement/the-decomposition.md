# The Decomposition & the Impossibility — This Course's Keystone

Room-acoustics has the Schroeder frequency; flow-matching has the conditional-expectation
identity. **This course has two halves of one keystone**, and you need both:

1. **The decomposition** — *what to penalize.* The VAE's KL term splits **exactly** into
   three pieces, and only one of them — the **total correlation (TC)** — drives
   disentanglement. This tells you the *mechanism*.
2. **The impossibility** — *why the mechanism isn't enough.* Locatello et al. proved that
   minimizing TC (or any unsupervised objective) **cannot identify** the true factors
   without an **inductive bias**. This tells you the *limit*.

Put them together and the whole field collapses to one sentence:

> **Every disentanglement method = an objective that drives total correlation toward zero,
> *plus* an inductive bias (architecture, supervision, or data structure) that picks *which*
> factorisation you get — because the objective alone can't.**

Read this in Phase 0.1, then return to it in **Phase 5** (the decomposition — spend as long
as it takes), **Phase 7** (the impossibility — spend as long as it takes), and **Phase 8**
(where audio supplies the inductive bias with labels). Every term in **bold** is earned
somewhere in the syllabus; the phase is in brackets.

---

## The recurring picture: a code, a traversal, a correlation

```
        a single image x  ──encoder──▶   z = (z₁, z₂, …, z_K)   ──decoder──▶  x̂
   (dSprites: a shape at                  a latent CODE; we WANT
    some scale/rotation/x/y) [Phase 1.1]  one dim per factor [Phase 1.1]

   the basic diagnostic — a LATENT TRAVERSAL [Phase 1.2]:
        hold z₂…z_K fixed, sweep z₁  ──▶  ▢  ▢  ▢  ▢  ▢   (only SCALE changes?  ✓ disentangled)
        hold z₁,z₃… fixed, sweep z₂  ──▶  ◰  ◳  ◲  ◱  ◰   (only ROTATION changes? ✓)
                                                          (two things change at once? ✗ entangled)
```

The course's oracle is this **traversal** (a picture) plus one **number** — the
**Mutual Information Gap (MIG)** [Phase 6]. For the audio payoff, the oracle becomes the
**ear** (swap pitch and timbre, then listen) [Phase 8].

---

## Half 1 — the decomposition: total correlation is what disentangles [Phase 5]

A plain VAE's training loss is the **ELBO**: a reconstruction term minus
`D_KL(q(z|x) ‖ p(z))` [Phase 0.2]. **β-VAE** [Phase 3] just multiplies that KL by **β > 1**
to pressure the code toward the factorised prior — and it *works*, but it also wrecks
reconstruction. **Why?** Because **β-TCVAE** [Phase 5.2] showed the expected KL splits
**exactly** into three interpretable pieces:

```
  E_x[ D_KL( q(z|x) ‖ p(z) ) ]  =   I_q(z; x)                  ← index-code MI  (info z carries
                                                                  about x — NEEDED to reconstruct)
                                +   D_KL( q(z) ‖ Πⱼ q(zⱼ) )    ← TOTAL CORRELATION (TC):
                                                                  dependence among latent dims —
                                                                  THIS is the disentanglement driver
                                +   Σⱼ D_KL( q(zⱼ) ‖ p(zⱼ) )   ← dimension-wise KL
```

- **TC** measures how far the aggregate posterior `q(z)` is from a product of its marginals
  — i.e. how *statistically dependent* the latent dimensions are. Drive TC→0 and the code
  **factorises**. [Phase 5.2]
- **Index-code MI** `I_q(z;x)` is the information the latent keeps about the input — you
  *need* it to reconstruct.
- **β-VAE's mistake:** a single β raises **all three** terms, so it buys factorisation
  (↓TC) only by also throwing away reconstruction (↓ index-code MI). [Phase 5.3]
- **The fix:** penalize **TC alone**. **FactorVAE** [Phase 5.4] estimates TC with a
  **density-ratio discriminator** (real `q(z)` vs dimension-shuffled samples); **β-TCVAE**
  [Phase 5.5] estimates it with **minibatch-weighted sampling** (no extra network). Same TC
  target, two estimators — **equal disentanglement at better reconstruction.** [Phase 5.6]

That is the whole mechanism. **TC is the operative quantity.**

## Half 2 — the impossibility: the objective can't pick the factors [Phase 7]

Here is the twist that reframes everything. **Locatello et al. (2019, ICML best paper)**
[Phase 7] proved an **impossibility theorem**:

- The factorised prior `p(z) = N(0, I)` is **rotation-invariant** — rotate the latent axes
  and the marginal is unchanged. So for any "disentangled" model there exist **infinitely
  many entangled** models (rotations of it) that are **indistinguishable** from it — same
  data marginal, same loss. [Phase 7.1]
- Therefore an **unsupervised objective + a rotation-invariant prior cannot identify** the
  true factors. **Some inductive bias is required** — architecture, (weak) supervision, or
  data structure.

And the empirical half — **>12,000 models** (6 methods × 6 metrics × 7 datasets × many
seeds, ~10,000 GPU-hours) [Phase 7.2]:

- **Metrics disagree** (only weakly correlated) — a model can ace one and fail another.
- **Random seeds dominate** — seed variance for one method *exceeds* the gap between methods.
- **TC of the aggregate posterior is not predictive** of metric scores after the fact.
- **No evidence** that better disentanglement improves downstream sample-efficiency.

The field's question is therefore **not** "which loss disentangles" but "**which inductive
bias / supervision**." TC tells you the lever; Locatello tells you the lever alone won't
land you on the *right* factorisation.

## Together — and why audio closes the loop [Phase 8]

The audio work makes the abstraction concrete: **Luo et al. (2019)** split monophonic music
into separate **pitch** and **timbre** latents — and they get away with it precisely because
they add **frame-level pitch + instrument labels** (the inductive bias Locatello demands),
not by an unsupervised objective alone. The curriculum payoff (editing the through-line clip's
pitch without touching its timbre) lives here — and the open frontier (separating room,
channel, performer from composition, *self-supervised*, on full recordings) is exactly the
case where the inductive bias is still missing.

---

## The misreadings this course exists to kill

Curated from the `disentanglement/` wiki. The tutor flags each on the spot and logs
recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "β-VAE / β-TCVAE disentangle *for free*, unsupervised." | They are **inductive biases, not guarantees.** Locatello: identifiability needs bias, and random **seeds can dominate** β's effect. | Phase 7 |
| "Total correlation *is* the KL penalty." | TC is **one of three** exact terms (index-code MI + **TC** + dim-wise KL). β-VAE over-penalizes by raising **all three**. | Phase 5.2–5.3 |
| "More β = strictly more disentanglement." | β trades away **reconstruction** (↓ index-code MI), and seed variance can swamp β's effect. | Phase 3.2, 7.2 |
| "A high MIG (or any one metric) proves disentanglement." | Metrics **disagree**; report **several** and average over **seeds**. No single number settles it. | Phase 6, 7.2 |
| "The aggregate-posterior TC predicts how disentangled a model is." | Locatello: TC is **not a reliable post-hoc predictor** of metric scores. | Phase 7.2 |
| "InfoGAN / β-VAE codes map to the same factors every run." | Which code grabs which factor is **not identifiable** — the unsupervised limitation, formalised by Locatello. | Phase 2.4, 7.1 |
| "Disentanglement reliably improves downstream tasks." | Locatello found **no evidence** of better sample-efficiency from disentanglement. | Phase 7.2 |
| "Disentanglement is unsupervised by definition." | The methods that actually work on audio (**Luo**) use **label supervision** — exactly the inductive bias the impossibility result requires. | Phase 8.1 |

---

## How the course earns the keystone

| Piece | Earned in |
|---|---|
| what "disentangled" means; the latent traversal diagnostic | **Phase 1** |
| the MI ancestor on the GAN side (InfoGAN) | **Phase 2** |
| the β knob and its reconstruction tax (β-VAE) | **Phase 3** |
| *why* β works: the information-bottleneck view + capacity ramp (Burgess) | **Phase 4** |
| **the decomposition: TC is the driver** (FactorVAE, β-TCVAE) | **Phase 5** (keystone) |
| how it's measured, and why metrics disagree (β-VAE/FactorVAE/MIG) | **Phase 6** |
| **the impossibility: identifiability needs inductive bias** (Locatello) | **Phase 7** (keystone) |
| audio supplies the bias with labels (Luo); the open frontier | **Phase 8** |
