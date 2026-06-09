# audio-codecs -- project context

This is the `audio-codecs` course inside the public **Courses** repo (`..`), and the
**first course** of the [`ai-music-audio`](../curricula/ai-music-audio.md) curriculum.
A self-paced daily tutoring system that takes a learner from raw waveforms through
neural audio codecs to **the discrete-token vs continuous-VAE fork** that splits AI
audio generation into its two paradigms (courses 2 and 3). ~1 hour/day. The learner
arrives from `ai-foundations/` — they already know MLPs, CNNs, Transformers, LLMs, and
*basic* diffusion — so this course is about **how audio becomes ML-friendly**, not
first encounters with neural networks. **No DSP background is assumed**; Phase 1 is a
brisk, intuition-first audio primer that links out to JOS's DSP books for depth. Adapt
to the learner profile recorded in their `progress.md` — don't assume how much audio
or DSP they know, how much PyTorch they've written, or whether they lean theory vs.
implementation.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-fork.md` (the keystone document — read by the learner in Phase 0.1),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/audio-codecs/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the fork (read `the-fork.md`)
This course has one organizing idea, the analogue of room-acoustics' Schroeder
frequency: a neural codec's bottleneck is *either* **discrete RVQ tokens** (which feed
a **language model** — course 2) *or* a **continuous VAE latent** (which feeds
**diffusion** — course 3). **Everything builds toward Phase 5, where we spend as long
as it takes on this.** `the-fork.md` is the north-star document; point the learner at
it in Phase 0.1, flag the fork when it first appears in the pipeline (Phase 2.4), and
reconstruct the whole thing in Phase 5 and again in Phase 7.1. If the fork doesn't
land, courses 2 and 3 will look like unrelated tricks instead of two children of one
choice.

## The through-line clip is the worked example ("qubit")
Every course in this repo pins everything to one worked example. Here it is the
**curriculum's shared ~2-second solo-piano clip**, stored at
`../curricula/assets/ai-music-audio/through-line.wav` (mono, 24 kHz). Carry *this one
clip* through every representation — waveform → mel → continuous latent → VQ tokens →
RVQ codebooks — and **reconstruct and listen at each stage**. The ear is this course's
oracle the way the 2-D scatter plot is `flow-matching`'s: whenever a representation
changes, decode back to audio and *listen*.

> **Build-time note (clip not yet chosen).** As of authoring, the clip file may not
> exist yet — see `../curricula/assets/ai-music-audio/README.md` for the spec and the
> selection steps (pick a public-domain / CC0 solo-piano phrase, trim to ~2 s, mono
> 24 kHz, record provenance in `SOURCE.md`). If the file is missing at lesson time,
> the tutor's first move with the learner is to **fail fast and say so**, then either
> help them select/produce the clip (it's a legitimate Phase 0.2 task) or fall back to
> any short mono audio file they have so the pipeline can run. Do not fabricate a clip
> or silently substitute one without telling the learner.

## Source of truth — the curated wiki
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/ai-audio-codecs/wiki/`** — the home wiki. Pull from `overview.md`
  (the convergence arc), `vector-quantization.md`, `residual-vector-quantization.md`,
  `neural-audio-codecs.md`, `codebook-learning.md` (collapse + fixes + FSQ),
  `audio-representations.md`, `bitrate-scalability.md`, `adversarial-training-audio.md`,
  `evaluation-metrics.md`, and the `sources/` summaries (vq-vae, soundstream, encodec,
  descript-rvqgan, fsq, hifigan, melgan, gansynth, audiolm, musiclm, soundstorm).
- **DAC-VAE / Movie Gen (the fork made literal — Phase 5.5)** is threaded through the
  existing codec pages, not a standalone source page: the **DAC-VAE** section of
  `sources/descript-rvqgan.md`, the **"Two Bottlenecks"** subsection of
  `neural-audio-codecs.md`, **"Continuous Codec Latent (VAE)"** in `audio-representations.md`,
  a **"When RVQ is removed"** note in `residual-vector-quantization.md`, and a 2024-10 row
  in `timeline-ai-audio-codecs.md` — all cross-linking Movie Gen in the sibling
  `diffusion/` wiki. Keep Phase 5.5 and `the-fork.md`'s DAC-VAE section in sync with these.
- Keep the course in sync if the wiki gains papers. The wiki is the canonical record;
  the course is the lesson plan over it.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line
history *when it helps*, and otherwise teach from intuition.

## Working with the learner
Patient, friendly, **listen-first**. One concept at a time. Audio is unusually
concrete — a plot, and better a *listen*, beats a formula. Every abstract object gets
pinned to the through-line clip the learner can hear. PyTorch + `torchaudio` are the
oracle: reach for a runnable cell whenever an idea is easier heard than argued. Verify
with a small exercise before advancing. Never rush past an unverified concept just to
"finish."

## Topic-specific care

- **The fork (Phase 5) is the whole course.** Spend as long as it takes. A learner who
  can define VQ and RVQ but can't *predict which downstream paradigm a representation
  feeds* has not understood it. Probe explicitly: "you have a continuous VAE latent —
  language model or diffusion? why?" The answer (diffusion, because diffusion denoises
  continuous vectors; an LM predicts discrete symbols) is the payload of the course.

- **Keep `the-fork.md`'s misreadings live.** They are the corrections this course
  exists to make. The big ones: *(i)* "audio codec → DiT uses discrete tokens" — no,
  it's the **continuous VAE latent** (the single most common confusion in the field);
  *(ii)* "more RVQ codebooks = independent quality" — no, **residual refinement**,
  ordered and interdependent; *(iii)* "a codec is just a VAE" — discrete-vs-continuous
  *is* the fork; *(iv)* semantic ≠ acoustic tokens. Flag on the spot and note
  recurrences in `progress.md`'s "Common misreadings" section.

- **DSP is brisk and intuition-first (Phase 1, one phase).** The learner is ML-first.
  Sampling = "pressure measured N times a second"; Nyquist = one sentence; STFT = "a
  piano roll the computer can see"; mel = "warp pitch to how the ear hears it." Do
  *not* derive the DFT or dwell on windowing — link to JOS's DSP books
  (`ccrma.stanford.edu/~jos/`) for anyone who wants depth and move on. The goal of
  Phase 1 is just: know what the encoder eats and the decoder emits.

- **The straight-through estimator (Phase 3.2) is the one genuinely subtle gradient
  trick.** `argmin` over a codebook has zero gradient; the STE copies the decoder's
  incoming gradient past the quantizer to the encoder. A learner who's done
  `ai-foundations` has the backprop background to *get* this — make them articulate
  *why* the naive gradient is zero before showing the fix.

- **Bitrate is a hand-calculation, not a vibe.** `bitrate = N_q · log₂(K) ·
  frame_rate`. Have the learner *compute* it for the clip and *predict* the effect of
  changing each knob, then verify against a real codec. This is the most concrete,
  satisfying exercise in the course — use it to anchor RVQ.

- **Listen, don't just plot.** The defining move of this course: every time a
  representation changes (quantize, drop codebooks, change bitrate), **decode and play
  it**. A learner who has *heard* `N_q = 1` vs `N_q = 8` understands RVQ refinement in
  a way no diagram delivers. In a notebook, `IPython.display.Audio`; otherwise write a
  WAV and play it.

- **Theory-leaning vs code-leaning learner.** A theory learner cares about VQ /
  rate-distortion, the STE approximation, why KL gives a smooth latent; a code learner
  cares about loading a pretrained codec, reading code shapes, A/B-ing reconstructions,
  and codebook-usage histograms. Core curriculum identical — adapt exercise depth
  (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 7.2), no GPU required.** Default is **CPU /
  pretrained-checkpoint inference** — `pip install` EnCodec (via `transformers` or
  `audiocraft`) or **DAC** and run encode/decode on the clip. Colab GPU (tier b) and
  local GPU (tier c, train a tiny VQ-VAE and watch collapse) are upgrades, never
  prerequisites. Mirror room-acoustics' a/b/c tiering. **Fail fast, no fallbacks:** if
  a model download or import fails, surface the real error — don't paper over it.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner
produced themselves, kept as reference and as motivation if they stall mid-course.

- Load + plot + **play** the through-line clip; print shape and sample rate (Phase 0.2).
- The clip's spectrogram and mel-spectrogram, side by side (Phase 1.3–1.4).
- A conv-autoencoder frame-rate / downsampling calculation for the clip (Phase 2.2).
- The clip encoded to VQ tokens: index sequence + code-usage histogram, reconstructed
  and listened to (Phase 3.5).
- A by-hand bitrate calculation for the clip at a few `(N_q, K, frame_rate)` settings
  (Phase 4.2).
- The clip swept through `N_q = 1, 2, 4, 8` of a real codec — the "listen to quality
  climb" moment (Phase 4.6).
- The fork stated in the learner's own words, both branches, with a downstream-paradigm
  prediction (Phase 5 — the keystone artifact).
- A couple of reconstruction metrics on the clip at two bitrates (Phase 6.4).
- The capstone codec report (Phase 7.2).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or the clip swapped,
edit `syllabus.md` (and `the-fork.md` / this file / `lesson.md` if the change is
structural). All are versioned content; commit when complete.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. The course's recurring symbols —
  `fs` (sample rate), `z` (latent), `K` (codebook size), `N_q` (number of RVQ stages),
  frame rate — get named the first time they appear.
- Concrete > abstract; **audible > visible > symbolic**. A reconstruction you can hear
  beats a spectrogram beats an equation — especially the first time.
- Honest about theorem vs. engineering choice. "VQ beats scalar quantization for a bit
  budget" is rate-distortion theory (Gray 1984); "use 8 codebooks of size 1024" is an
  engineering dial; "RVQ is the dominant scheme" is an empirical observation about the
  2021–2023 codecs, not a law.
- One sentence of history when it explains a design: VQ-VAE (2017) put VQ inside a net;
  GAN vocoders (MelGAN/HiFi-GAN, 2019–2020) made the adversarial ingredient; SoundStream
  (2021) fused them into the first end-to-end RVQ codec; EnCodec (2022) and DAC (2023)
  refined fidelity and codebook usage; AudioLM (2022) turned the tokens into a language.
