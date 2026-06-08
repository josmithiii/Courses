# Courses

A growing collection of self-paced, daily, tutor-style courses run through
[Claude Code](https://claude.com/claude-code). Each course is a self-contained
folder with its own syllabus and a `/lesson` slash command that runs an
interactive ~1-hour session with an AI tutor — teaching one concept at a time and
verifying understanding with small exercises.

**Course content vs. learner state are deliberately separated.** This repo holds
only shipped, version-controlled course content (read-only at runtime). Each
learner's personal progress and lesson journal live *outside* the repo, so the
repo stays pristine and the system is multi-user / web-app ready (a future web app
just repoints the data location per user — see "Architecture" below).

## Curricula

A **curriculum** is an ordered *sequence* of courses sharing a goal (a *syllabus* is one
course; a *curriculum* is a program of study). They're a thin overlay — each course still
stands alone — declared in [`curricula/`](curricula/). See [`curricula/README.md`](curricula/README.md).

| Curriculum | Status | Sequence |
|------------|--------|----------|
| [AI Music & Audio](curricula/ai-music-audio.md) | 🟢 Complete | `ai-foundations` → `audio-codecs` → `audio-codec-lms` → `audio-diffusion-dit` (enrichment: `flow-matching`) |
| [Buddhist Philosophy](curricula/buddhist-philosophy.md) | 🟡 Partial | `buddhism-early-philosophy` → `buddhism-mahayana-philosophy` |

## Courses

| Course | Status | What it covers |
|--------|--------|----------------|
| [`ai-foundations/`](ai-foundations/) | 🟢 Active | From the Multilayer Perceptron up to modern LLMs — backprop, PyTorch, CNNs, Transformers, LLMs, Diffusion. Intuition-first, beginner-friendly. |
| [`agents101/`](agents101/) | 🟢 Active | Operator-level training on local AI agents: run, extend, coordinate, schedule, message, oversee, debug, containerize. Hermes-agent as case study. Hands-on; ~12 sessions. |
| [`crypto-foundations/`](crypto-foundations/) | 🟢 Active | From "what's a public key?" to a hardened personal workflow: GPG, signing, SSH, TLS basics, password hashing, encrypted backups, 2FA, full-disk encryption. Intuition + commands; ~25 sessions. |
| [`ai-miracle-decade-plus/`](ai-miracle-decade-plus/) | 🟢 Active | Self-paced traversal of 40 landmark AI papers (2006 → 2023) — DBN through GPT-4, with cross-cutting concept-page stops. No time budget; side quests first-class. Links to arXiv + the music423-2023 meta-wiki. |
| [`quantum-states/`](quantum-states/) | 🟢 Active | From bra/ket notation to density matrices, partial traces, and decoherence. Assumes linear algebra, complex numbers, basic Newtonian + a little prior QM. Every abstract object pinned to a worked qubit example; NumPy/SymPy as the oracle. ~25 sessions. |
| [`flow-matching/`](flow-matching/) | 🟢 Active | From ODEs as generative models to modern simulation-free training: Lipman's Conditional Flow Matching, Liu's Rectified Flow, Tong's OT-CFM. Assumes ODEs, basic probability, and some PyTorch. Every formalism pinned to a 2-D toy distribution; tracks the three foundational papers in `/l/dttd/FlowStuff/`. ~25 sessions. |
| [`buddhism-early-philosophy/`](buddhism-early-philosophy/) | 🟢 Active | Doctrinal foundations of early (pre-Mahāyāna) Buddhism from the Pali Canon: Four Noble Truths, Three Marks, Five Aggregates, Dependent Origination, *nibbāna*. Philosophy only — practice and devotional material out of scope. Every doctrine pinned to a 10-second moment of experience; named suttas read on SuttaCentral. ~40 sessions. |
| [`room-acoustics/`](room-acoustics/) | 🟢 Active | From "what is a pressure wave?" to evaluating real performance and speech spaces (concert halls, auditoria, conference rooms). The Schroeder frequency — wave-below / ray-above — is the keystone; everything is pinned to one shoebox room analyzed both ways, plus a concert-hall foil. Builds the background behind a real Treble-vs-Odeon question, then goes further to measuring rooms (RT60, C80, STI) in Python / REW. New to acoustics; some signal-processing comfort helps. ~30 sessions. |
| [`audio-codecs/`](audio-codecs/) | 🟢 Active | Course 1 of the [AI Music & Audio](curricula/ai-music-audio.md) curriculum. From raw waveforms to the tokens and latents every modern audio generator consumes: brisk DSP (sampling, STFT, mel) → autoencoders → VQ-VAE → residual VQ → SoundStream/EnCodec/DAC → **the discrete-token vs continuous-VAE fork** (the keystone) → semantic vs acoustic tokens + evaluation. Pinned to one ~2 s solo-piano clip, *heard* at every stage; tiered CPU/Colab/GPU capstone. Assumes `ai-foundations`; no DSP background needed. ~20 sessions. |
| [`audio-codec-lms/`](audio-codec-lms/) | 🟢 Active | Course 2 of the [AI Music & Audio](curricula/ai-music-audio.md) curriculum — the **discrete-token branch** of course 1's fork. Generate audio by *language-modeling* codec tokens: AR raw audio (WaveNet) → Jukebox → AudioLM (**semantic+acoustic** hierarchy) → MusicLM (MuLan text) → MusicGen (**single-stage codebook patterns**) → masked/NAR (VampNet, MAGNeT) → VALLE/**MIDI-VALLE** (codec-LM, *not* a DiT). Keystone = the **RVQ token grid** (`the-token-grid.md`). Continue/infill/condition the shared piano clip; tiered MusicGen capstone. Assumes `audio-codecs`. ~25 sessions. |
| [`audio-diffusion-dit/`](audio-diffusion-dit/) | 🟢 Active | Course 3 (final) of the [AI Music & Audio](curricula/ai-music-audio.md) curriculum — the **continuous-VAE branch** of course 1's fork. Generate audio by *denoising a continuous VAE latent* with a Diffusion Transformer: latent diffusion (AudioLDM → Tango → AudioLDM 2) → **the DiT** (patchify + **adaLN-Zero**, Peebles & Xie) → Stable Audio (continuous-VAE + timing — *still a U-Net*) → **the U-Net→DiT swap** (Long-Form Latent Diffusion / Stable Audio Open) → rectified-flow MM-DiT (FluxMusic) → DiffRhythm / ACE-Step (LM-planner + DiT-renderer). Keystone = the **latent canvas** (`the-latent-canvas.md`); ships a self-contained rectified-flow primer. *Denoise* the shared piano clip; tiered Stable-Audio-Open/DiffRhythm capstone. Assumes `audio-codecs` + `audio-codec-lms`; `flow-matching` enrichment. ~25 sessions. |
| [`disentanglement/`](disentanglement/) | 🟢 Active | Disentangled representation learning: one latent axis per factor of variation, and why that's hard. InfoGAN → β-VAE → the information-bottleneck view (Burgess) → **isolating total correlation** (FactorVAE, β-TCVAE) → **Locatello's impossibility result** → pitch/timbre in audio (Luo). Two-part keystone = **the decomposition & the impossibility** (`the-decomposition.md`): TC is what to penalize, but the objective alone can't identify factors without an inductive bias. Pinned to **dSprites** (latent traversals + MIG) with an audio pitch/timbre payoff; tiered a/b/c capstone. Standalone; **enrichment** for [AI Music & Audio](curricula/ai-music-audio.md). Assumes VAEs. ~15–18 sessions. |
| `buddhism-mahayana-philosophy/` | ⚪ Planned | Mahāyāna view, building on early philosophy: emptiness (*śūnyatā*) via Prajñāpāramitā (Heart, Diamond), Madhyamaka (Nāgārjuna), Yogācāra, Buddha-nature. |
| `claude-code-and-tools/` | ⚪ Planned | Using Claude Code effectively: commands, hooks, skills, MCP, subagents, scheduled/remote agents. |
| `claude-app/` | ⚪ Planned | Getting the most out of the Claude app: projects, connectors, workflows. |
| _more to come_ | ⚪ Planned | |

## Architecture

**Content (this repo — versioned, read-only at runtime).** Each course folder:

- `syllabus.md` — the full syllabus and the teaching method.
- `progress.template.md` — the seed tracker, copied to the learner's data dir on first run.
- `.claude/commands/lesson.md` — the `/lesson` command that runs the live session.
- `CLAUDE.md` — context that tells any Claude Code session how to act as the tutor.

**Learner state (outside the repo — personal, per-user, never committed).**
Resolved as `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/<course>/`:

- `progress.md` — durable state: what's mastered, what's next (the tutor reads this first).
- `lessons/YYYY-MM-DD.md` — one log per day (lesson content, exercises, your answers).

`COURSES_DATA_DIR` is the single seam for going multi-user: a web app sets it to a
per-user directory/object store and nothing else changes. On a fresh machine the
`/lesson` command auto-seeds `progress.md` from `progress.template.md`.

### To take a course

First time on a new machine — clone the repo and drop straight into a course:

```bash
git clone <repo-url> Courses
cd Courses
./take room-acoustics    # cd into the course + launch today's lesson
```

Every day after that, from the repo:

```bash
./take <course-folder>   # e.g. ./take room-acoustics  (run ./take with no args to list courses)
```

`./take` is just a convenience wrapper for the underlying steps, which also work by hand:

```bash
cd Courses/<course-folder>
claude          # start Claude Code in the course folder
/lesson         # begin (or resume) today's ~1-hour session
```

An optional daily 11:00 reminder can be wired up (local macOS notification and/or
a Slack DM) so the day's session is easy to remember — see the course folder.

Built for Claude Code (the `/lesson` command above). It also runs in **Claude
Cowork** — just point it at a course folder and ask it to start a lesson; it reads
the same `lesson.md` directly (there are no slash commands in Cowork). Fork and
adapt for other environments.

## Authoring a new course

Copy [`course-template/`](course-template/) and follow the checklist in its
[`README.md`](course-template/README.md). Short version:

1. `cp -r course-template <new-course-id>` and `cd` into it.
2. Delete the template's `README.md` (it's authoring instructions, not learner content).
3. Find/replace `{{COURSE-ID}}`, `{{COURSE TITLE}}`, and `{{ONE-LINE SCOPE}}` in the new folder.
4. Rewrite `syllabus.md` with your syllabus; adjust `progress.template.md` learner-profile fields and environment checkboxes.
5. Add a row to the *Courses* table above.

No personal state to reset — it never lived in the repo. The `/lesson` command and
teaching loop are reusable as-is.
