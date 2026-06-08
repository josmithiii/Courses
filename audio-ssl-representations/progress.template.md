# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Transformers / masked language modeling (BERT) background: _(shaky — rebuild in 0.2 / comfortable / strong)_
- "An embedding is a reused intermediate activation": _(shaky / comfortable / strong)_
- Neural-codec / RVQ (EnCodec) background, from `audio-codecs/`: _(none — sketch in 0.3 / comfortable / strong)_
- Audio front-end (mel / STFT / frames): _(shaky / comfortable / strong)_
- PyTorch + Hugging Face `transformers` comfort: _(beginner / comfortable / strong)_
- Why they're here / goal: _(understand audio SSL / pick a conditioning encoder / the resynthesis angle / research)_
- Lean: _(hands-on — extract features, fit probes, plot specialization / conceptual — pretext task & the target)_
- Interested in the resynthesis payoff (invert & listen)? _(yes — do tier c / not especially)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c — note: tier a runs on CPU)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **diagnostic-first**, every term defined on first use, every claim
  about what a model encodes pinned to a rendered **layer-wise linear probe** (and, on the
  resynthesis tier, heard)

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The two epistemologies + read `the-pretext-task.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` importable
- [ ] Hugging Face `transformers` importable
- [ ] A **pretrained SSL checkpoint** loads (`MERT-95M-public`, or `wav2vec2-base` / `hubert-base`)
- [ ] Can extract **per-layer hidden states** for the piano clip (`output_hidden_states=True` → `[layers × frames × dim]`)
- [ ] The shared **~2 s solo-piano clip** is available (from `assets/ai-music-audio/`)
- [ ] A small **labeled** probe set fetched (NSynth pitch/instrument subset, or a few GTZAN genre clips)
- [ ] Can fit a **linear probe** (e.g. `sklearn` LogisticRegression / Ridge) on frozen features
- [ ] (capstone tier c, optional) can attach a decoder head / tiny RAVE-or-flow decoder and play audio
- [ ] `the-pretext-task.md` read (the keystone — the pretext task & the target)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The objects & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Encoder used: _(e.g. MERT-95M-public)_; hidden dim = _( )_; number of layers = _( )_; frame rate ≈ _( ) Hz_.
- **Pretext task** = mask a span, predict a target in latent space; **representation** = the kept Transformer activations.
- **wav2vec 2.0** target = contrastive **InfoNCE** (true quantized latent vs distractors), learned product quantizer.
- **HuBERT** target = **masked prediction of k-means cluster IDs** ("hidden units"); consistency, not correctness.
- **MERT** teachers = **EnCodec** RVQ-VAE (acoustic) + **CQT** reconstruction (pitch/harmony).
- **Linear probe** = frozen features → linear classifier/regressor; accuracy = what's *linearly* available.
- Probe tasks tried = _(e.g. pitch, instrument, genre)_; best layer per task = _( )_.

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has produced themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-pretext-task.md`). The tutor watches for
> these, notes when one comes up, and revisits later to make sure it has stuck.

- "Self-supervised = unsupervised" — no, SSL **manufactures** a target from the data (no *human* label)
- "The pretext task is the goal" — the pretext head is **discarded**; the **intermediate representation** is the product
- "SSL reconstructs the audio, like an autoencoder / codec" — it predicts a **target**; features are **not invertible**
- "wav2vec 2.0 ≈ HuBERT" — **contrastive** (InfoNCE) vs **predictive** (cluster-ID MLM) is a real split
- "HuBERT needs a *good* teacher" — **consistency, not correctness**; crude k-means bootstraps, then re-cluster
- "A higher linear-probe number = a strictly better representation" — **task- and probe-capacity-relative**; report several
- "MERT / SSL features are disentangled" — entangled **by layer**, not by **named factor** (room/channel/performer)
- "Semantic tokens (AudioLM) are not SSL" — they **come from w2v-BERT**, an SSL model
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 7.5) — tiered, no GPU required for tier (a)
> Picked partway through Phase 5 so it can shape the last few lessons.

- _(a) **CPU / default** — load MERT-95M-public (or wav2vec2/hubert base); per-layer features for the piano clip + a small labeled set; linear probes per layer; plot the layer-specialization curve; one-page "what does it encode, and where?" report_
- _(b) **Colab GPU** — compare a contrastive (wav2vec2) vs predictive (hubert/MERT) encoder on the same probes; add tasks (beat, key); sanity-check the BEST-RQ random-target intuition_
- _(c) **Local GPU / resynthesis bridge** — attach a small decoder head to frozen SSL features (or condition a tiny RAVE/flow decoder); try to invert to audio and listen — "understanding ≠ invertible," heard_
- Choice: _(not yet)_
