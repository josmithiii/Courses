# Disentanglement
*Enrichment for the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum — what a VAE latent encodes.*

Disentangled representation learning — one latent axis per factor of variation, and why
that's hard: InfoGAN → β-VAE → the information-bottleneck view (Burgess) →
**isolating total correlation** (FactorVAE, β-TCVAE) → **Locatello's impossibility
result** → pitch/timbre in audio (Luo). Pinned to **dSprites** (latent traversals + MIG)
with an audio pitch/timbre payoff.

**Keystone:** the decomposition & the impossibility — see [`the-decomposition.md`](the-decomposition.md).
TC is what to penalize, but the objective alone can't identify factors without an inductive bias.

**Prerequisites:** VAEs (encoder/decoder, ELBO, the KL term) — from
[`ai-foundations`](../ai-foundations/) or equivalent.

**Format:** ~1 hr/day, ~15–18 sessions; tiered a/b/c capstone (CPU dSprites, no GPU for tier a).

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take disentanglement` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
