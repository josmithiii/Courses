# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- AI Music & Audio core (`audio-codecs/`, `audio-diffusion-dit/` — continuous-VAE latent + DiT): _(not taken — recall-primer / comfortable / strong)_
- `audio-ssl-representations/` (the **encode** box): _(not taken — recall-primer in 3.1 / comfortable / strong)_
- `disentanglement/` (the **steer** box): _(not taken — recall-primer in 4.1 / comfortable / strong)_
- `flow-matching/` + DiT (the **decode** box): _(not taken — recall-primer in 5.1 / comfortable / strong)_
- DSP / parametric synthesis background (the contrast): _(this is JOS's home turf / some / little)_
- PyTorch + Hugging Face comfort: _(beginner / comfortable / strong)_
- Why they're here / goal: _(create variations / edit recordings / survey the field / the research frontier)_
- Lean: _(hands-on — encode-perturb-decode, A/B listen, compute metrics / conceptual — the loop & the control problem)_
- Interested in the attribute-edit stretch (room/timbre)? _(yes — try tier b/c / variation-preserving is enough)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c — note: tier a runs on CPU via RAVE)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **diagnostic-first**, every term defined on first use, every claim
  about the loop pinned to a variation the learner can **hear** (A/B: source vs variation)

> **Plunge-in is fine and intended.** No feeder is a hard gate. If a recall-primer (Phases 3.1 /
> 4.1 / 5.1) lands on a learner who hasn't taken that feeder, give the one slide, point at the
> feeder, and continue at a shallower depth — don't re-teach the whole feeder inline. Getting in
> over your head is the on-ramp that motivates the trip back.

## Status
- **Current phase:** 0 — The Loop, the Control Problem, the Tools
- **Next topic:** 0.1 — The two epistemologies + read `the-resynthesis-loop.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` importable
- [ ] Hugging Face `transformers` (and/or the RAVE package) importable
- [ ] A **pretrained RAVE checkpoint** loads (the tier-a audible loop)
- [ ] Can **encode → decode** the piano clip through RAVE (the loop runs end to end)
- [ ] Can **perturb** the latent and decode a **variation** (encode-perturb-decode)
- [ ] Can play audio / render an A/B (source vs variation) to **listen**
- [ ] The shared **~2 s solo-piano clip** resolves at `../curricula/assets/ai-music-audio/through-line.wav`
- [ ] (eval) Can compute an **identity** number (embedding cosine / CLAP to source)
- [ ] (eval) Can compute a **distribution** number (FAD to a small reference set)
- [ ] (tier b/c, optional) Can condition a **rectified-flow / Stable-Audio-Open / MERT-latent DiT** decoder
- [ ] `the-resynthesis-loop.md` read (the keystone — the loop & the control problem)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The objects & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Tier-a model = _(e.g. a pretrained RAVE checkpoint)_; latent dim = _( )_; sample rate ≈ _( ) Hz_.
- **The loop** = encode → (steer / perturb) → decode; a recording is a **steerable object** when all three run.
- **The control problem** = the latent is **expressive** (full complexity) but **illegible** (no named direction).
- **Variation** = perturb-and-decode (always closes). **Edit** = move a *named* direction (room/timbre — needs a bias).
- **Identity number** = embedding cosine / CLAP to the source (did it stay the same source?).
- **Distribution number** = FAD to a reference set (is it in-distribution audio?).
- Variations made = _( )_; best A/B judgment so far = _(same source, genuinely different? )_.
- Edit attempted (room / timbre)? = _(not yet)_; did it close? = _( )_.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has produced themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-resynthesis-loop.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "Resynthesis = reconstruction" — no, the goal is **coherent variation around** the source; reconstruction is the floor
- "A good generator is all you need" — no, the loop needs the **representation** *and* the **inductive bias** too
- "More disentanglement ⇒ better resynthesis" — Locatello: identifiability needs a **bias**; factor-naming is unsolved
- "Neural resynthesis replaces DSP synthesis" — different **epistemology**, complementary (legible-bounded vs expressive-implicit)
- "Evaluation = FAD (or any one number)" — **no-reference**: report identity + distribution + **listening**, ear first
- "Codec-LM and diffusion-DiT are interchangeable for editing" — **continuous is the editing mainline**, with reasons
- "This is text-to-music-from-a-prompt" — no, it's **resynthesizing an existing recording**
- "We train these models" — no, we **use pretrained checkpoints**, tiered a/b/c
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 8.5) — tiered, no GPU required for tier (a)
> Picked partway through Act II so it can shape the last few lessons.

- _(a) **CPU / default — RAVE, the audible loop.** Pretrained RAVE; encode the piano clip, perturb the latent, decode a variation, A/B listen (same source, genuinely different?). Optionally re-run through the tiny SSL-latent+flow decoder as a second example. One-page report: did identity survive? is it genuinely a variation? — ear first, one number to corroborate_
- _(b) **Colab GPU — condition a flow / Stable-Audio-Open generation** on the clip's representation; explore the distribution of variations (FAD); attempt one attribute edit (room or timbre)_
- _(c) **Local GPU — the faithful pipeline.** MERT (or another SSL encoder) features → conditioned rectified-flow DiT decoder; attempt disentangled steering; the research-flavored tier where the open box is felt directly_
- Choice: _(not yet)_
