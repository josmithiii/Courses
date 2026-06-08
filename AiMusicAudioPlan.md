# AI Music & Audio — Curriculum Plan

**Status:** 🟢 Complete (updated 2026-06-07). All steps done: repo-wide
`curriculum.md → syllabus.md` rename, the **curricula concept** landed
(`curricula/ai-music-audio.md` + assets), the shared **through-line clip** in place
(CC0 Chopin B.150, mono 24 kHz), and **all three courses authored** — course 1
`audio-codecs/` (keystone = the fork), course 2 `audio-codec-lms/` (keystone = the RVQ
token grid), and course 3 `audio-diffusion-dit/` (keystone = the latent canvas; ships a
self-contained rectified-flow primer). **The curriculum is complete.** Rooted in
`/l/cllm/`. Companion to
[`NewCoursesPlan.md`](NewCoursesPlan.md)
(general roadmap); this file is the focused plan for the **AI music/audio
generation** thread *and* for introducing the **curriculum** (course-sequence)
concept the repo doesn't yet have.

This plan turns the knowledge base we curated in
`/w/music423-2023/` (the `ai-audio-codecs`, `ai-music-audio-gen`, and `diffusion`
wikis) into a learner path that starts where [`ai-foundations/`](ai-foundations/)
ends and ends at the 2026 state of the art (DiffRhythm, ACE-Step, MIDI-VALLE).

### ✅ Decisions locked (2026-06-07)

All Part 5 open questions are resolved; this doc is now a build spec.

1. **Terminology** — per-course file = **`syllabus.md`**; top-level sequence =
   **curriculum** (`curricula/<name>.md`). Repo-wide rename pending (Part 1 checklist).
2. **Course count** — **3** (codec→LM vs VAE→DiT fork is the seam between courses).
   4-course split (symbolic/performance) kept as a documented future option.
3. **Course slugs** — **`audio-`-prefixed** for sort-grouping:
   **`audio-codecs`**, **`audio-codec-lms`**, **`audio-diffusion-dit`**.
   (Descriptive titles kept in prose; the slug is the folder name.)
4. **Through-line clip** — **yes**: one shared ~2-second solo-piano phrase carried
   across all three courses, stored in-repo (it's content). Actual clip TBD at build
   time (see Part 3 note).
5. **Capstone compute** — **CPU/Colab fallbacks throughout**, tiered like
   room-acoustics' a/b/c: tier-a CPU pretrained-checkpoint inference, tier-b Colab
   GPU for the heavy generators, tier-c local GPU.
6. **`flow-matching` dependency** — **enrichment, not a gate**: course 3 ships a
   self-contained rectified-flow primer and links to `flow-matching/` for depth.
7. **Course 1 DSP scope** — **brisk, intuition-first**, one phase; link out to JOS's
   DSP books for depth (learners are ML-first).

---

## Part 1 — Introducing "curricula" (sequences of courses)

### The need

The repo is currently a **flat list** of independent courses. There's no first-class
way to say "take A, then B, then C — together they're one journey." The AI-music/audio
material is naturally 2–3 courses, and it has a hard prerequisite (`ai-foundations`)
and a useful enrichment (`flow-matching`). That ordering should be *expressed*, not
left implicit.

> **A curriculum = an ordered sequence of courses sharing a goal, with declared
> prerequisites and (optionally) a through-line worked example.**

### ⚠️ Naming collision to resolve (top open question)

`curriculum.md` is **already** the filename for each course's *internal syllabus*.
If "curriculum" *also* means "a sequence of courses," the word is overloaded. JOS
proposed the two clean ways out (2026-06-07):

- **Option 1 — call the sequence a "program."** A **program** = an ordered sequence
  of courses; each course keeps its `curriculum.md`. **Zero churn** — nothing in the
  8 existing courses changes. "Program" is the standard term for a course sequence
  (university programs, edX programs). Only cost: `curriculum.md` keeps being used in
  the slightly-loose "really a syllabus" sense.

- **Option 2 — rename the per-course file to `syllabus.md`, and use "curriculum" for
  the sequence.** This is the **textbook-correct** distinction: a *syllabus* is one
  course; a *curriculum* is the whole program of study. Semantically ideal, and it
  *fixes* a latent misnomer (today's `curriculum.md` is really a syllabus). Cost: a
  repo-wide rename — 8 courses + `course-template/` + references in
  `lesson.md`/`CLAUDE.md`/`README.md` (a clean grep-and-replace; JOS upgrades fully,
  no back-comat needed).

**✅ Decision (2026-06-07): Option 2.** Per-course listing → **`syllabus.md`**;
the top-level sequence → **curriculum** (`curricula/<name>.md`). This is the
textbook-correct distinction (a syllabus is one course; a curriculum is the program
of study) and it fixes today's latent misnomer. "Program" (Option 1) was considered
and set aside. The rename is a mechanical repo-wide grep-and-replace — no
back-compat. This doc still writes "curriculum" generically in places; it'll be
normalized to **syllabus**/**curriculum** per this decision when we build.

**Rename checklist (Option 2):** `curriculum.md → syllabus.md` in all 8 courses +
`course-template/`; then grep-and-update references in each
`.claude/commands/lesson.md`, `CLAUDE.md`, `README.md`, `course-template/README.md`,
and `NewCoursesPlan.md` (and the `./take` script if it names the file).

### Proposed representation (Option 2)

```
/l/cllm/
  curricula/
    ai-music-audio.md        # the curriculum: ordered courses + prereqs + through-line
    README.md                # what a curriculum is; index of curricula
  <course-folders>/          # each course's listing renamed curriculum.md → syllabus.md
```

A `curricula/<name>.md` file declares:

- **Goal** (one paragraph) and **who it's for**.
- **Prerequisite course(s)** — links into the repo (e.g. `ai-foundations/`).
- **Ordered course list** with a one-line "why here" for each.
- **Enrichment / co-requisite** courses (optional, parallel — e.g. `flow-matching/`).
- **Through-line** — an optional shared worked example carried across all courses
  (see the curriculum-level "qubit" idea below).
- **Source-of-truth** pointers (the `music423-2023` wikis).

Add a **Curricula** table to the top-level `README.md` (above or beside the Courses
table). Optionally teach `./take` to recognize a curriculum and suggest the next
course when one completes — **future**, not part of v1.

### Curricula already latent in the repo (validates the concept)

Documenting curricula also captures sequences that *already* exist informally:

- **AI Generative Media** (the one this plan builds): `ai-foundations` →
  *[the AI-music/audio courses below]*, with `flow-matching` as enrichment before
  the diffusion course.
- `ai-miracle-decade-plus` is a natural **survey companion** that can run in parallel
  (it already links to the `music423-2023` meta-wiki).
- The Buddhism thread (`buddhism-early-philosophy` → `buddhism-mahayana-philosophy`)
  is another ready-made curriculum once the Mahāyāna course lands.

---

## Part 2 — The AI Music & Audio curriculum

### The spine (where the learner comes from → goes)

```
ai-foundations  ──(required)──▶  audio-codecs  ──────▶  audio-codec-lms
   │  (MLP→CNN→Transformers→LLMs→basic Diffusion)         │ (codec-LM lineage)
   │                                                      ▼
   └──(enrichment)──▶ flow-matching ──────────────▶  audio-diffusion-dit
                       (CFM / rectified flow)          (VAE-latent → DiT lineage)
```

- **Entry frontier (from `ai-foundations`):** the learner knows MLPs, backprop,
  PyTorch, CNNs, attention/Transformers, LLMs, and *basic* diffusion/generative
  models. That is exactly enough to start the codecs course.
- **`flow-matching` as enrichment:** its conditional-flow-matching / rectified-flow
  spine is the training objective behind FluxMusic and modern audio DiTs. Recommended
  *before or alongside* the diffusion course, not strictly required (the diffusion
  course can give a self-contained flow-matching primer and link out for depth).
- **Exit:** the learner can explain, contrast, and run both dominant paradigms —
  **codec → language model** vs **continuous-VAE-latent → diffusion transformer** —
  and place 2024–2026 systems (Stable Audio, FluxMusic, DiffRhythm, ACE-Step,
  MIDI-VALLE) in that map.

### Proposed breakdown — 3 courses (recommended)

The split mirrors the actual thesis of the `ai-music-audio-gen` wiki overview: the
field forks into a **codec-language-model** lineage and a **VAE→diffusion-transformer**
lineage, sitting on a **shared representation** foundation. So:

| # | Course (slug) | Title | Covers | ~Sessions | Source wiki |
|---|---------------|-------|--------|-----------|-------------|
| 1 | `audio-codecs` | Neural Audio Codecs | How raw audio becomes ML-friendly: DSP basics → autoencoders → VQ-VAE → RVQ → EnCodec/SoundStream/DAC → **the discrete-token vs continuous-VAE fork** → semantic vs acoustic tokens | ~20 | `ai-audio-codecs/` |
| 2 | `audio-codec-lms` | Audio Codec Language Models | Generate audio by language-modeling codec tokens: WaveNet/SampleRNN → Jukebox → AudioLM → MusicLM → MusicGen → VampNet/MAGNeT → VALLE/MIDI-VALLE | ~25 | `ai-music-audio-gen/` (codec-LM half) |
| 3 | `audio-diffusion-dit` | Audio Diffusion & the DiT | Generate audio by diffusion/flow in a VAE latent: AudioLDM(2)/Tango → **DiT** → Stable Audio → Long-Form Latent Diffusion → FluxMusic (rectified flow) → DiffRhythm → ACE-Step | ~25 | `diffusion/` + `ai-music-audio-gen/` (diffusion half) |

**Why 3 and not 1:** each is a single coherent subject (the repo's rule), each ends
in a runnable capstone, and the codec/LM vs diffusion/DiT split is *the* organizing
idea — making it the seam between courses teaches the distinction by structure.

**Alternatives to discuss:**
- **2 courses:** fold `neural-audio-codecs` into Phase 0–1 of each downstream course.
  Cheaper, but duplicates the representation material and weakens the shared foundation.
- **4 courses:** peel a `symbolic-and-performance-audio` course off course 2 for the
  MIDI/score thread (MusicVAE, MIDI-VALLE, DDSP-adjacent performance synthesis).
  Worth it only if JOS wants the symbolic/performance angle as a first-class subject.

### The curriculum-level "qubit" (a through-line, proposed)

Every course in this repo pins everything to one worked example (the qubit;
two-moons; the shoebox room; a 10-second moment). For a *curriculum*, propose a
**shared through-line clip** carried across all three courses — e.g. **one ~2-second
solo-piano phrase**:

- **Course 1:** encode it — watch it become waveform → mel → VAE latent → VQ tokens
  → RVQ codebooks, then reconstruct and *listen* to each bitrate.
- **Course 2:** tokenize it into a codebook×frame grid; **continue** it (AR),
  **infill** it (masked, VampNet/MAGNeT-style), **condition** it on text.
- **Course 3:** take its VAE latent and **denoise** it step-by-step; generate a
  variation with Stable Audio Open / DiffRhythm.

Same clip, three paradigms — the through-line *is* the curriculum's spine made
audible. (Per-course qubits can still specialize; the clip is the connective tissue.)

**Decided (2026-06-07): adopt the shared clip.** Storage and selection (build-time):
the clip is *content*, so it lives in-repo under the curriculum, e.g.
`curricula/assets/ai-music-audio/through-line.wav` (mono, 24 kHz to match common
codec sample rates, ~2 s). Pick a **freely licensed** source (public-domain or CC0
solo-piano phrase) so it can ship in the repo — record the source/license alongside
it. Each course's syllabus references this one path.

---

## Part 3 — Per-course design sketches

Each follows the house format (`course-template/`): `syllabus.md` (the renamed
per-course listing), `progress.template.md`, `.claude/commands/lesson.md`,
`CLAUDE.md`. Phase counts are
provisional. Theory-lean vs implementation-lean is recorded per learner in
`progress.md` (as in `quantum-states`/`flow-matching`/`room-acoustics`).

### Course 1 — `audio-codecs` (Neural Audio Codecs)

*One-line scope:* How raw audio is turned into the tokens and latents that every
modern audio generator consumes — and why the discrete-vs-continuous choice splits
the whole field.

- **Keystone (analogue of the Schroeder frequency / CFM identity):** the
  **discrete-codec vs continuous-VAE fork**. Discrete RVQ tokens feed *language
  models*; a continuous VAE latent feeds *diffusion*. Everything downstream hangs
  off this one choice. Spend as long as it takes on it.
- **Qubit:** the through-line clip, carried through every representation.
- **Phase sketch:** 0 Orientation & tools (`torch`, `torchaudio`) · 1 Digital audio &
  time–frequency (sampling, quantization, STFT, mel) · 2 Autoencoders & the
  bottleneck (AE→VAE, continuous latent) · 3 Discrete representations: VQ-VAE
  (codebook, straight-through, codebook collapse) · 4 Residual VQ & neural codecs
  (SoundStream, EnCodec, DAC; bitrate↔quality) · 5 **The fork** (tokens-for-LMs vs
  latent-for-diffusion) · 6 Semantic vs acoustic tokens; evaluation; SoundStorm ·
  7 Capstone: encode/decode the clip through a real codec, inspect the codebooks.
- **Source:** `/w/music423-2023/ai-audio-codecs/wiki/`.

### Course 2 — `audio-codec-lms` (Audio Codec Language Models)

*One-line scope:* Generating audio by predicting codec tokens with Transformers —
the AudioLM/MusicGen lineage — through autoregressive, masked, and performance-synthesis
variants.

- **Keystone:** *tokens + a sequence model = audio generation*; the
  **semantic→acoustic hierarchy** (AudioLM) that buys long-range coherence, and the
  **codebook-pattern** trick (MusicGen) that makes one Transformer enough.
- **Qubit:** the clip's codec-token grid — continued, infilled, text-conditioned.
- **Phase sketch:** 0 Orientation; recap codec tokens · 1 Autoregressive raw audio
  (WaveNet, SampleRNN — why sample-level is slow) · 2 Tokens + Transformers (Jukebox)
  · 3 AudioLM (semantic + acoustic tokens) · 4 Text conditioning (MusicLM / MuLan) ·
  5 Single-stage + codebook patterns (MusicGen delay/parallel; Stack-and-Delay) ·
  6 Beyond AR: masked token modeling (VampNet, MAGNeT/NAR) · 7 Codec-LM beyond music:
  VALLE → **MIDI-VALLE** (performance synthesis; the "this is *not* a DiT" point) ·
  8 Capstone: run MusicGen/AudioCraft — generate, continue, infill.
- **Source:** `/w/music423-2023/ai-music-audio-gen/wiki/` (codec-LM pages).

### Course 3 — `audio-diffusion-dit` (Audio Diffusion & the DiT)

*One-line scope:* Generating audio by diffusion/flow in a continuous VAE latent —
the AudioLDM→Stable-Audio→DiT lineage — up to full-song and hybrid LM-planner systems.

- **Keystone:** **continuous-VAE latent → Diffusion Transformer.** Hammer the point
  that "audio codec → DiT" really means a *continuous VAE* (not discrete RVQ tokens),
  and that the DiT (adaLN-Zero transformer-over-patches) replaced the U-Net.
- **Qubit:** the clip's VAE latent, denoised step-by-step (warm up on `flow-matching`'s
  2-D two-moons before lifting to the audio latent).
- **Phase sketch:** 0 Orientation; recap diffusion from `ai-foundations` Ph6 ·
  1 Latent diffusion for audio (AudioLDM, CLAP, mel-VAE + vocoder) · 2 The audio-LDM
  family (AudioLDM 2 "language of audio", Tango, Moûsai, Noise2Music) · 3 **The DiT**
  (U-Net → transformer-over-patches, adaLN-Zero; Peebles & Xie) · 4 Stable Audio
  (continuous-VAE + timing conditioning — still a U-Net) · 5 DiT for music (Long-Form
  Latent Diffusion, Stable Audio Open; the U-Net→DiT swap) · 6 Flow matching + MM-DiT
  (FluxMusic; rectified flow — bridges to `flow-matching/`) · 7 Full songs & hybrids
  (DiffRhythm; ACE-Step = LM planner + DiT renderer) · 8 Capstone: generate with
  Stable Audio Open / DiffRhythm; inspect the latent.
- **Source:** `/w/music423-2023/diffusion/wiki/` + `ai-music-audio-gen/wiki/`
  (diffusion pages: `dit`, `stable-audio`, `fluxmusic`, `diffrhythm`).

### Standard misreadings to flag from day one (curriculum-wide)

Straight out of the wiki curation (several are corrections we made this week):

- "Discrete codec tokens are lossless" / "more RVQ codebooks just = more quality"
  (it's **residual refinement**, with interdependencies).
- "A neural codec is just a VAE" — **discrete RVQ vs continuous VAE is the fork**, not a detail.
- Conflating AudioLM's **semantic** vs **acoustic** tokens.
- "MusicGen is multi-stage" — it's **single-stage** with codebook patterns.
- "Masked NAR generation = diffusion" (MAGNeT vs diffusion are different).
- "**MIDI-VALLE / VALLE are DiTs**" — they are **codec-LMs** (VALLE lineage).
- "**audio codec → DiT** uses discrete codec tokens" — it's a **continuous VAE latent**.
- "**Stable Audio is a DiT**" — v1 is a **U-Net**; the DiT enters in the long-form follow-up.
- "Flow matching is just diffusion" (related, distinct — the `flow-matching` course settles this).
- "Semantic tokens are *required* for long-range coherence" — long-form latent diffusion challenged this.

The `CLAUDE.md` for each course should tell the tutor to correct these on the spot
and keep a running "misreading file" in the worked-example bank (as the Buddhism /
flow-matching / room-acoustics courses do).

---

## Part 4 — Cross-cutting decisions & conventions

- **Source of truth = the `music423-2023` wikis.** The courses *teach from* and
  *link into* `/w/music423-2023/{ai-audio-codecs,ai-music-audio-gen,diffusion}/wiki/`
  (the way `flow-matching` cites `/l/dttd/FlowStuff/` and `ai-miracle-decade-plus`
  links the meta-wiki). The wiki stays canonical; courses stay pedagogical. Keep
  them in sync when the wiki gains papers.
- **Naming (decided).** `ai-music-audio` is the **curriculum** name (JOS's preference).
  Course **slugs** are **`audio-`-prefixed** for sort-grouping: `audio-codecs`,
  `audio-codec-lms`, `audio-diffusion-dit`. Human-readable titles (Neural Audio Codecs,
  Audio Codec Language Models, Audio Diffusion & the DiT) live in the syllabus + README
  row, not the folder name.
- **Tooling/runtime.** Standard repo machinery (`/lesson`, `./take`, `COURSES_DATA_DIR`
  learner state) is reused as-is. Capstones need `torch`/`torchaudio` and a GPU-or-Colab
  path for the heavier generators (MusicGen, Stable Audio Open, DiffRhythm) — call out
  a no-GPU fallback (pretrained-checkpoint inference / Colab) like room-acoustics'
  a/b/c capstone tiers.
- **Relationship to `flow-matching` and `ai-miracle-decade-plus`.** Enrichment and
  survey companions, not duplicated content; the diffusion course links to
  `flow-matching` for rectified-flow depth rather than re-deriving it.

---

## Part 5 — Open questions — ALL RESOLVED (2026-06-07)

See the **Decisions locked** block near the top for the canonical list. Summary:

1. ~~Sequence terminology~~ → **syllabus** (per course) + **curriculum** (sequence).
   Repo-wide rename `curriculum.md → syllabus.md` pending (Part 1 checklist).
2. ~~Course count~~ → **3** (4-course symbolic/performance split kept as future option).
3. ~~Course slugs~~ → **`audio-`-prefixed**: `audio-codecs`, `audio-codec-lms`,
   `audio-diffusion-dit`.
4. ~~Through-line clip~~ → **yes, shared clip**; in-repo under `curricula/assets/`,
   freely licensed solo-piano ~2 s (final clip chosen at build time).
5. ~~Capstone compute~~ → **CPU/Colab fallbacks throughout**, tiered a/b/c.
6. ~~`flow-matching` dependency~~ → **enrichment, not a gate**: course 3 ships a
   self-contained rectified-flow primer + links to `flow-matching/`.
7. ~~Course 1 DSP scope~~ → **brisk, intuition-first**, one phase, link out to JOS's
   DSP books.

## Part 6 — Build order (decisions locked — executing)

0. ✅ **Repo-wide rename** `curriculum.md → syllabus.md` (8 courses + `course-template/`),
   then grep-and-update references in each `.claude/commands/lesson.md`, `CLAUDE.md`,
   `README.md`, `course-template/README.md`, `NewCoursesPlan.md`, and `./take` if it
   names the file (Part 1 checklist). No back-compat. *(commit `35b5ee6`)*
1. ✅ Land the **curricula concept**: `curricula/README.md`, `curricula/ai-music-audio.md`,
   `curricula/assets/ai-music-audio/`, and a Curricula table in the top-level `README.md`.
   Backfilled latent curricula (AI Generative Media; Buddhism). *(commit `ba11b46`)*
   The **through-line clip** is now in place: CC0 Chopin B.150 opening phrase, mono
   24 kHz 16-bit, ~2.2 s, with `SOURCE.md` provenance *(commit `695e72e`)*.
2. ✅ Author **`audio-codecs`** (shared foundation, brisk DSP phase; keystone =
   `the-fork.md`). *(commit `6d73416`)*
3. ✅ **Author `audio-codec-lms`** (keystone = `the-token-grid.md`; AR/masked codec-LM
   lineage; MusicGen capstone), then ✅ **`audio-diffusion-dit`** (keystone =
   `the-latent-canvas.md`; AudioLDM → DiT → Stable Audio → U-Net→DiT swap → FluxMusic →
   DiffRhythm/ACE-Step; self-contained `rectified-flow-primer.md` + link to
   `flow-matching/`; Stable-Audio-Open/DiffRhythm capstone). **All three courses done —
   curriculum complete.**
4. ✅ Each course ships tiered capstones (CPU/Colab/local-GPU) and wires the through-line
   clip into its qubit. *(all three done)*
5. ✅ Add rows to the top-level Courses table and to `NewCoursesPlan.md`'s status snapshot
   as each lands. *(all three done)*
