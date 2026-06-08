# audio-codec-lms -- project context

This is the `audio-codec-lms` course inside the public **Courses** repo (`..`), and the
**second course** of the [`ai-music-audio`](../curricula/ai-music-audio.md) curriculum.
A self-paced daily tutoring system that walks the **discrete-token branch** of course
1's fork: generate audio by *language-modeling* a neural codec's tokens — the WaveNet →
Jukebox → AudioLM → MusicLM → MusicGen → VampNet/MAGNeT → VALLE/MIDI-VALLE lineage. ~1
hour/day. The learner arrives from `audio-codecs/` (course 1) knowing the RVQ **token
grid**, the discrete-vs-continuous **fork**, and having encoded/heard the through-line
clip; and from `ai-foundations/` with Transformers and LLMs in hand. So this course is
about **how token sequences become music**, not first encounters with attention or
autoregression. Adapt to the learner profile in their `progress.md` — don't assume how
fresh course 1 is, how much PyTorch they've written, or theory-vs-implementation lean.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-token-grid.md` (the keystone document — read by the learner in Phase 0.1),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/audio-codec-lms/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the token grid (read `the-token-grid.md`)
This course has one organizing object, the analogue of course 1's fork: the **RVQ token
grid** (`N_q` codebooks × `T` frames) and the question *how do you model `N_q` parallel
streams over `T` steps, and in what order?* Every system is a different answer —
**hierarchical cascade** (AudioLM/MusicLM), **codebook pattern** (MusicGen flat/delay,
Stack-and-Delay), or **masked parallel** (VampNet/MAGNeT) — plus AudioLM's
**semantic→acoustic** split for coherence. `the-token-grid.md` is the north-star
document; point the learner at it in Phase 0.1 and reconstruct it in Phases 3, 5, and
8.1. **Spend as long as it takes on Phase 3 (semantic→acoustic) and Phase 5 (codebook
patterns)** — they are the two halves of the keystone.

## Prerequisite handling
Course 1 (`audio-codecs/`) is the real prerequisite — this course *starts* from its
token grid. If the learner is fuzzy on "what a codec token is," `[N_q, T]`, or the
fork, **rebuild that in Phase 0.2 before proceeding** (re-encode the clip, look at the
grid). Don't push forward on a shaky token foundation; nothing here parses without it.

## The through-line clip is the worked example ("qubit")
The curriculum's shared **~2-second solo-piano clip** at
`../curricula/assets/ai-music-audio/through-line.wav` (mono, 24 kHz). Course 1
*encoded* it; **here we *generate* from it** — carry its token grid through every
paradigm: **continue** it (AR, Phase 5), **infill / vamp** it (masked, Phase 6), and
**condition** a generation with text (Phase 4). The ear is this course's oracle the way
the 2-D scatter plot is `flow-matching`'s: whenever you generate, **decode and listen**.
The clip is *solo piano*, which makes Phase 7 (MIDI-VALLE, expressive piano performance
synthesis) land on home turf.

> If the clip file is missing at lesson time, **fail fast and say so** (it should exist
> — committed in `695e72e`); then fall back to any short mono audio so the pipeline can
> run, and tell the learner. Do not silently substitute.

## Source of truth — the curated wiki
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — the home wiki (codec-LM half). Pull
  from `overview.md` (the 2016→2026 arc), `concepts/generation-paradigms.md` (AR vs
  masked vs diffusion — the comparison table is gold), `concepts/codec-based-generation.md`
  (the two-stage pipeline + the multi-stream strategy table), and
  `concepts/text-to-music-conditioning.md`. Source summaries: `wavenet`, `samplernn`,
  `nsynth`, `jukebox`, `audiolm`, `musiclm`, `musicgen`, `vampnet`, `stack-and-delay`,
  `magnet`, `midi-valle`.
- **`/w/music423-2023/ai-audio-codecs/wiki/`** — course 1's wiki, for token/codec recall
  (SoundStream, EnCodec, DAC, SoundStorm).
- Note: the diffusion systems (`stable-audio`, `dit`, `fluxmusic`, `diffrhythm`,
  `ace-step`) in that wiki belong to **course 3** — mention them only as the *other*
  branch; don't teach them here.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line
history *when it helps*, and otherwise teach from the token grid.

## Working with the learner
Patient, friendly, **listen-first**. One concept at a time. The recurring picture is the
**token grid** — draw on it constantly (AR fills it column-by-column; masked fills it by
confidence; patterns re-order how columns are read). Every abstract idea gets pinned to
the through-line clip the learner can generate from and hear. `audiocraft`/PyTorch are
the oracle: reach for a runnable generation whenever an idea is easier heard than argued.
Verify with a small exercise before advancing. Never rush past an unverified concept.

## Topic-specific care

- **Phases 3 and 5 are the keystone — spend the time.** A learner who can list systems
  but can't say *how each models the `N_q × T` grid* has missed the course. Probe: "RVQ
  gives 4 streams per frame; MusicGen is one Transformer — how?" (a codebook *pattern*
  serializes/staggers the streams). And: "why does AudioLM split semantic vs acoustic?"
  (acoustic-only drifts; semantic carries structure).

- **Keep `the-token-grid.md`'s misreadings live.** The big ones: *(i)* "MusicGen is
  multi-stage" — **single-stage** with patterns; *(ii)* "masked NAR = diffusion" —
  discrete confidence-unmasking vs continuous denoising; *(iii)* "MIDI-VALLE/VALL-E are
  DiTs" — **codec-LMs**, the cleanest test of whether the fork landed; *(iv)* semantic ≠
  acoustic tokens; *(v)* "text-to-music needs paired data" — MuLan/CLAP bypass it. Flag
  on the spot; note recurrences in `progress.md`'s "Common misreadings" section.

- **The fork is the spine across courses 2–3.** This course is the *language-model*
  branch; course 3 is the *diffusion* branch. Use Phase 7 (MIDI-VALLE is **not** a DiT)
  as the hinge: same task as a diffusion model (audio from a condition), opposite
  machinery. A learner who gets why MIDI-VALLE is a codec-LM is ready for course 3.

- **AR vs masked is a *decoding-order* distinction, not a quality verdict.** AR fills the
  grid left-to-right (slow, can't infill); masked fills by confidence over ~10–40 passes
  (fast, bidirectional, enables editing). Both model **discrete tokens**. Make the
  learner articulate the two limits of AR (O(T) speed; no infill) before VampNet/MAGNeT —
  the motivation *is* the understanding.

- **Codebook patterns are concrete — trace them.** Don't leave flat/delay/parallel
  abstract. Sketch a 4-stream × few-frame grid and have the learner *number the order*
  each pattern reads cells. That five-minute exercise makes MusicGen click harder than
  any paragraph.

- **Listen, don't just describe.** The defining move: every generation (continue,
  infill, condition) gets **decoded and played**. A learner who has *heard* the clip
  continued vs infilled understands AR-vs-masked viscerally. In a notebook,
  `IPython.display.Audio`; otherwise write a WAV and play it.

- **Theory-leaning vs code-leaning learner.** Theory: the AR factorization, why
  semantic+acoustic helps, the contrastive-embedding trick, masking schedules. Code:
  loading `audiocraft`, prompting MusicGen, reading generated token grids, A/B-ing
  patterns, infilling with a masked model. Core curriculum identical — adapt exercise
  depth (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 8.2), no GPU required.** Default is **CPU /
  pretrained inference** — the smallest MusicGen via `audiocraft` runs on CPU (slowly);
  generate and continue the clip. Colab GPU (tier b: larger model, infill, pattern A/B,
  melody conditioning) and local GPU (tier c: style fine-tune, or run MIDI-VALLE) are
  upgrades, never prerequisites. Mirror room-acoustics' a/b/c. **Fail fast, no
  fallbacks:** if a model download or import fails, surface the real error.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner
produced themselves, kept as reference and as motivation if they stall mid-course.

- Re-encode the clip and read its token grid `[N_q, T]` (Phase 0.2 — the foundation).
- A hand-traced flat / delay / parallel pattern over a small grid (Phase 5.2).
- The clip **continued** with MusicGen, decoded and heard (Phase 5.5).
- The clip's middle slice **infilled** (VampNet/MAGNeT-style), heard, and contrasted
  with the AR continuation (Phase 6.6).
- A reasoned text prompt for the clip's character + which conditioning strategy fits
  (Phase 4.4).
- The conditioning × decoding map with every system placed (Phase 8.1 — the keystone
  artifact).
- The capstone codec-LM report (Phase 8.2).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or a different generator
used, edit `syllabus.md` (and `the-token-grid.md` / this file / `lesson.md` if the
change is structural). All are versioned content; commit when complete.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring symbols — `N_q` (codebook
  levels / RVQ streams), `T` (frames), the **token grid** `[N_q, T]`, `p(xₜ | x_<t)`
  (the AR factorization) — get named the first time they appear.
- Concrete > abstract; **audible > visible > symbolic**. A generation you can hear beats
  a token diagram beats an equation.
- Honest about theorem vs. engineering choice. "Tokenize then language-model" is a
  pipeline choice; "delay beats flat on speed" is an empirical pattern result; "masked
  ≠ diffusion" is a definitional fact.
- One sentence of history when it explains a design: WaveNet (2016) proved AR audio but
  sample-level was too slow; Jukebox (2020) tokenized it; AudioLM (2022) added the
  semantic hierarchy; MusicLM (2023) added contrastive text; MusicGen (2023) collapsed
  the cascade into one model via codebook patterns; VampNet/MAGNeT (2023–24) went masked
  for speed and editing; VALLE→MIDI-VALLE carried the recipe back from speech to piano.
