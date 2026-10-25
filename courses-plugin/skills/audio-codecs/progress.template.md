# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- ML background (from `ai-foundations` or equivalent): _(MLPs/CNNs only / + Transformers & LLMs / + basic diffusion — all of it)_
- PyTorch comfort: _(beginner / comfortable / strong)_
- Audio / DSP background: _(none — never touched a spectrogram / hobbyist musician / knows "sample rate" & "FFT" / strong DSP)_
- Math comfort (logs, vectors, a little probability): _(rusty / comfortable / fluent)_
- Why they're here / goal: _(want to build audio generators / understand the codec→LM vs VAE→DiT fork / general curiosity / research)_
- Lean: _(hands-on — load codecs & A/B reconstructions / conceptual — understand the representations & the fork)_
- Has a GPU? Colab access? _(affects capstone tier a/b/c)_
- Can play audio on their machine / using a notebook with inline audio? _(yes / no — affects the "listen" exercises)_
- Time budget: ~1 hour/day
- Style: patient, friendly, **listen-first**, every term defined on first use, every
  representation pinned to the one through-line clip and *heard* before moving on

## Status
- **Current phase:** 0 — Orientation
- **Next topic:** 0.1 — The whole course in one picture + read `the-fork.md`, after the Lesson 0 interview
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `torch` + `torchaudio` importable
- [ ] `matplotlib` importable (for waveform / spectrogram plots)
- [ ] Can **play audio** — `IPython.display.Audio` in a notebook, or write+play a WAV
- [ ] The through-line clip resolves at `../curricula/assets/ai-music-audio/through-line.wav`
      (or a short mono fallback clip is in hand — see CLAUDE.md build-time note)
- [ ] (capstone tier a) a pretrained codec installed — EnCodec (`transformers`/`audiocraft`) or DAC
- [ ] `the-fork.md` read (the keystone — the discrete-token vs continuous-VAE fork)
- [ ] A scratch `.py` file or notebook open and used during sessions

## The clip & numbers we reuse
> Filled in as we compute them; keep consistent across lessons.

- Through-line clip: solo piano, mono, 24 kHz, ~2 s → ~48000 samples.
- Latent frame rate (once a codec is loaded): _(e.g. 75 Hz → 320× time downsampling)_
- Reference bitrate calc: `bitrate = N_q · log₂(K) · frame_rate`
  (e.g. `N_q=8, K=1024, frame_rate=75 Hz` → `8·10·75 = 6000` bits/s = **6 kbps**).

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Worked-example bank (built across the course)
> Concrete results the learner has computed/heard themselves, kept as reference. Add a
> one-line entry each session (these are what a stalled learner keeps).

- (none yet)

## Common misreadings to revisit
> The perennial traps in this subject (from `the-fork.md`). The tutor watches for these,
> notes when one comes up, and revisits later to make sure it has stuck.

- "audio codec → DiT uses the discrete codec tokens" — no, it's the **continuous VAE latent**
- "a neural codec is *just* a VAE" — discrete-RVQ vs continuous-VAE **is the fork**
- "more RVQ codebooks = independent quality knobs" — it's **residual refinement**, ordered & interdependent
- "discrete codec tokens are lossless" — they're a **lossy** quantization
- semantic vs acoustic tokens conflated (structure-vs-fidelity; AudioLM uses both)
- "waveform-L2 measures quality" — use spectral/perceptual metrics + adversarial training
- "VQ trains like any layer" — `argmin` has zero gradient; the **straight-through estimator** is the trick
- (add others as they appear)

## Open questions / things to revisit
- (none yet)

## Capstone choice (Phase 7.2) — tiered, no GPU required
> Picked partway through Phase 4 so it can shape the last few lessons.

- _(a) **CPU / pretrained inference** — load EnCodec or DAC, encode the clip, inspect the codes (`[N_q,T]`, usage histogram), decode, A/B at `N_q=1,2,4,8` and two bitrates; write a one-page codec report_
- _(b) **Colab GPU** — tier a, plus a second codec at a different sample rate compared on the same clip, with ViSQOL/mel-distance_
- _(c) **Local GPU** — tier a, plus train a tiny VQ-VAE from scratch and watch codebook collapse (and a fix) live_
- Choice: _(not yet)_
