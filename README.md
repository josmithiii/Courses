# Courses

A growing collection of self-paced, daily, tutor-style courses run by Claude. Each
course runs an interactive ~1-hour session with an AI tutor — teaching one concept at
a time and verifying understanding with small exercises — and remembers where you left
off. Take them either way (see [Taking a course](#taking-a-course)):

- **As a Claude plugin — nothing to clone.** Install the `courses` plugin in the
  Claude desktop app or Claude Code and say *"let's do today's room-acoustics lesson"*.
- **From a clone of this repo** with [Claude Code](https://claude.com/claude-code):
  `./take <course>` runs the course's `/lesson` slash command.

**Course content vs. learner state are deliberately separated.** This repo holds
only shipped, version-controlled course content (read-only at runtime). Each
learner's personal progress and lesson journal live *outside* the repo, so the
repo stays pristine and the system is multi-user / web-app ready (a future web app
just repoints the data location per user — see "Architecture" below).

## Taking a course

| | Claude plugin | Clone the repo |
|---|---|---|
| **Runs in** | Claude desktop app (Code tab), or Claude Code in a terminal | Claude Code in a terminal |
| **Setup** | Add a marketplace, install one plugin | `git clone`, then `./take` |
| **Start a lesson** | Say *"let's do today's room-acoustics lesson"* | `./take room-acoustics` |
| **Your progress** | `~/Documents/Courses-data/`, or a folder you choose | `~/Documents/Courses-data/` |
| **Course updates** | Update the plugin | `git pull` |
| **Best for** | Learners who don't want a terminal | Course authors, or terminal users |

Both run the same course content and the same teaching loop, and both keep the same
files of progress — `progress.md` (what's mastered, what's next) and
`lessons/YYYY-MM-DD.md` (a record of each session) per course.

### Option 1: the `courses` Claude plugin (no clone needed)

Every course ships as a Skill in the **`courses` plugin**, installable straight from
this GitHub repo.

**Quickest, if you're comfortable in a terminal** — one line installs it for both
Claude Code and the desktop app's Code tab:

```bash
claude plugin marketplace add https://github.com/josmithiii/Courses && claude plugin install courses@josmithiii-courses
```

**In the Claude desktop app** (no terminal needed):

1. In the **Code** tab, open **Customize** → **Plugins**, click **+ Add** → **Add
   marketplace**, enter `https://github.com/josmithiii/Courses`, and click **Sync**.
2. **Easy to miss:** the plugin list starts on **Yours**, which shows only plugins
   you have *already installed* — so **courses** isn't there yet. Click **Discover**
   (in the **Yours | Discover** toggle, off to the right of the **Plugins** tab), search
   for **JOS Courses** (by Julius O. Smith III), and install it — searching just
   "courses" buries it under dozens of course-platform connectors. Afterwards it is
   listed under **Yours** → *From marketplaces you added*.
3. Start a session in any folder and say *"let's do today's room-acoustics lesson"*
   (any course name from the [Courses](#courses) table works).

On your first lesson Claude asks where to keep your progress; `~/Documents/Courses-data`
is a good choice. The Code tab works directly on your own computer, so progress saved
anywhere you choose stays put. Plugins installed in the Code tab also show up in Claude
Code in a terminal — the two share one setup.

Some versions of the desktop app also have a **Cowork** tab, which keeps its own
separate plugin list; the same steps should work there. Cowork can only save inside
the folder you selected for the task, so accept `Courses-data/` inside that folder
and start every later lesson in the same folder.

*Troubleshooting:* if **Add marketplace** just says "Failed to add marketplace", the
marketplace is probably already declared in your Claude Code settings in another
form — typically the short `josmithiii/Courses` form, added earlier in a terminal.
The desktop app always stores the full URL, and Claude Code refuses a second source
for the same marketplace name. (That's why every command here uses the full URL.) Run
`claude plugin marketplace remove josmithiii-courses` in a terminal, then add it again.
On a Mac, the real error is in `~/Library/Logs/Claude/main.log`.

**Inside a Claude Code session** (same as the one-liner above):

```
/plugin marketplace add https://github.com/josmithiii/Courses
/plugin install courses@josmithiii-courses
```

Then, in any folder, say *"let's do today's room-acoustics lesson"* or run the skill
directly as `/courses:room-acoustics`. To pick up course revisions later:
`claude plugin update courses@josmithiii-courses`.

**Where the plugin keeps your progress** — the first of these that exists:

1. `$COURSES_DATA_DIR`, if set;
2. `Courses-data/` in the workspace folder (the folder you started the session in);
3. `~/Documents/Courses-data/` — so progress from a cloned-repo setup carries over
   automatically.

If none exists, Claude asks you where to put it rather than guessing. Nothing is ever
written into the plugin itself.

### Option 2: clone the repo (Claude Code)

First time on a new machine — clone the repo and drop straight into a course:

```bash
git clone https://github.com/josmithiii/Courses.git
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

Progress goes to `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/<course>/`.

An optional daily 11:00 reminder can be wired up (local macOS notification and/or
a Slack DM) so the day's session is easy to remember — see the course folder.

A cloned course also runs in **Cowork** without the plugin: point a Cowork task at
the course folder and ask it to start a lesson; it reads the same `lesson.md`
directly (there are no slash commands in Cowork). Fork and adapt for other
environments.

## Curricula

A **curriculum** is an ordered *sequence* of courses sharing a goal (a *syllabus* is one
course; a *curriculum* is a program of study). They're a thin overlay — each course still
stands alone — declared in [`curricula/`](curricula/). See [`curricula/README.md`](curricula/README.md).

| Curriculum | Status | Sequence |
|------------|--------|----------|
| [AI Music & Audio](curricula/ai-music-audio.md) | 🟢 Complete | `ai-foundations` → `audio-codecs` → `audio-codec-lms` → `audio-diffusion-dit` (enrichment: `flow-matching`, `disentanglement`, `audio-ssl-representations`; capstone: `neural-audio-resynthesis`) |
| [Buddhist Philosophy](curricula/buddhist-philosophy.md) | 🟡 Partial | `buddhism-early-philosophy` → `buddhism-mahayana-philosophy` |
| [Music 423 (meta)](curricula/music423.md) | 🟡 Partial | **Map of parallel tracks** over JOS's `music423-2023` paper collection: on-ramps (`ai-foundations`; JOS's four DSP books) + Track A [AI Music & Audio](curricula/ai-music-audio.md), Track B [LLMs & Sequence Models](curricula/ai-llms-and-sequence-models.md), Track C [Differentiable & Physical Audio DSP](curricula/audio-differentiable-dsp.md); `ai-miracle-decade-plus` runs alongside any track |
| [LLMs & Sequence Models](curricula/ai-llms-and-sequence-models.md) | 🟡 Partial | `ai-foundations` → `ai-miracle-decade-plus` → `ai-sequence-models` → `ai-post-training-and-rl` (enrichment: `ai-vision-and-multimodal`, `audio-codec-lms`) |
| [Differentiable & Physical Audio DSP](curricula/audio-differentiable-dsp.md) | 🟢 Complete | JOS's DSP books → `audio-ddsp` → `audio-synth-effect-matching` → `audio-physics-informed` (enrichment: `neural-audio-resynthesis`, `room-acoustics`) |

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
| [`audio-ssl-representations/`](audio-ssl-representations/) | 🟢 Active | Self-supervised audio representation learning — how raw audio becomes a learned representation **without labels**. wav2vec 2.0 (contrastive InfoNCE) → HuBERT (masked prediction of k-means cluster IDs) → data2vec / w2v-BERT / BEST-RQ → MERT ("HuBERT for music"; EnCodec + CQT teachers; layer specialization) → probing. Two-part keystone = **the pretext task & the target** (`the-pretext-task.md`): you manufacture supervision and keep the intermediate representation, and the target shapes what it encodes — so an understanding-grade SSL encoder is **neither invertible nor disentangled**. Pinned to the shared piano clip, **probed per layer**; tiered a/b/c capstone. Standalone; **enrichment** for [AI Music & Audio](curricula/ai-music-audio.md). Assumes Transformers + masked LM. ~18–22 sessions. |
| [`neural-audio-resynthesis/`](neural-audio-resynthesis/) | 🟢 Active | **Capstone meta-course** of the [AI Music & Audio](curricula/ai-music-audio.md) thread — *creating and editing audio with neural methods.* Surveys the field (parametric/DDSP → codec-LM → continuous-VAE/DiT → resynthesis-as-editing), then **drills the load-bearing survivors** into the **encode→steer→decode** loop: an SSL conditioning latent (`audio-ssl-representations/`) + a disentangling inductive bias (`disentanglement/`) + a rectified-flow-DiT decoder (`flow-matching/` + `audio-diffusion-dit/`) = the resynthesis paradigm (static recording → **steerable object**), closing on the **no-reference evaluation** problem and the open frontier. Two-part keystone = **the resynthesis loop & the control problem** (`the-resynthesis-loop.md`): the latent is expressive but illegible; the game is winning back legible control. Pinned to the shared piano clip — **resynthesize a variation that preserves identity**, A/B listen; tiered a/b/c capstone (RAVE on CPU). **Plunge-in friendly — no hard prereq gates**; capstone enrichment for AI Music & Audio. ~20–25 sessions. |
| `buddhism-mahayana-philosophy/` | ⚪ Planned | Mahāyāna view, building on early philosophy: emptiness (*śūnyatā*) via Prajñāpāramitā (Heart, Diamond), Madhyamaka (Nāgārjuna), Yogācāra, Buddha-nature. |
| `ai-sequence-models/` | ⚪ Planned | Course 2 of [LLMs & Sequence Models](curricula/ai-llms-and-sequence-models.md). The architecture course: word2vec/seq2seq → attention → the Transformer → GPT-style LLMs → the efficiency response (linear attention, S4 → Mamba, RWKV, gated linear RNNs, Transformer–SSM hybrids). Keystone = what a token can attend to, and at what cost. Pinned to one tiny LM trained from scratch, re-implemented per mechanism. Sources: `music423-2023/{attention,natural-language-processing,mamba,rwkv,gated-recurrence,hybrid}/`. |
| `ai-post-training-and-rl/` | ⚪ Planned | Course 3 of [LLMs & Sequence Models](curricula/ai-llms-and-sequence-models.md). Pretrained LM → assistant: deep-RL landmarks (DQN, AlphaGo/AlphaZero) → RLHF (InstructGPT) → Constitutional AI → tool use; plus the scaling-laws / double-descent sidebar. Sources: `music423-2023/{reinforcement-learning,double-descent,ai-2012-to-2023}/`. |
| `ai-vision-and-multimodal/` | ⚪ Planned | Enrichment for both AI tracks. CNN backbones (AlexNet, ResNet, U-Net) → VAEs and GANs → ViT and autoregressive image generation → DALL-E and unified multimodal models. Sources: `music423-2023/{images,images-ar,multimodal}/`. |
| [`audio-ddsp/`](audio-ddsp/) | 🟢 Active | Course 1 of [Differentiable & Physical Audio DSP](curricula/audio-differentiable-dsp.md). Make the audio blocks you already know **differentiable**: harmonic oscillator bank + filtered noise + reverb (Engel 2020) → why waveform MSE fails and the **multi-scale spectral loss** → the `f₀`-gradient pathology → differentiable IIR (BPTT), frequency-domain biquads, FIR-approximated reverb — **the IIR-vs-FIR trade-off** → all-pass/phaser/grey-box compressor → DDX7, DDSP-Piano, MIDI-DDSP, DiffMoog. Keystone = **the differentiable block** (`the-differentiable-block.md`): which block, which loss. Pinned to the shared plucked-string note, resynthesized and *heard* at every stage; tiered a/b/c capstone; living frontier. Assumes JOS's *Filters* + *SASP* and `ai-foundations` Phase 2. ~20–25 sessions. |
| [`audio-synth-effect-matching/`](audio-synth-effect-matching/) | 🟢 Active | Course 2 of [Differentiable & Physical Audio DSP](curricula/audio-differentiable-dsp.md). Sound matching as an inverse problem: handcrafted features → supervised CNN/AST prediction and the in-domain gap → the loss question (parameter vs spectral vs JTFS vs PNP; no universal best) → differentiable synth matching (Masuda & Saito, DiffMoog, white-box) → distributional / generative / RL estimation (equivariant flow matching, neural proxies, SynthRL) → effect inversion (DeepAFx, blind estimation, the DRC forward model inverted analytically and neurally, grey-box, FDN reverb, modulation discovery, gain-trajectory supervision) → DAFx26 (2026): FM loss-landscape ridges, a differentiable Karplus–Strong, retrieval in shared audio–preset embeddings, and the plate-reverb parameter-estimation challenge → the 2026 wave (joint-distribution flow matching, renderer-free embedding search, GRPO-trained generative inverters, prediction + search for effect chains). Keystone = **many parameters, one sound** (`the-inverse-problem.md`). Pinned to the shared plucked-string note, parameters recovered three ways and heard; tiered a/b/c capstone; living frontier. Assumes JOS's *Filters* + *SASP* and `ai-foundations` Phase 2. ~25–30 sessions. |
| [`audio-physics-informed/`](audio-physics-informed/) | 🟢 Active | Course 3 (final) of [Differentiable & Physical Audio DSP](curricula/audio-differentiable-dsp.md). Physics + learning on one plucked note, modeled three ways: a **learnable modal resonator bank** (eigenmodes → biquads, fitted by spectral loss — Diaz & Hayes 2023), a **PINN** for the damped stiff string (PDE residual as loss; honest about forward-vs-inverse), and **hybrid physical/neural** models (differentiable waveguide, neural source–filter, grey-box). Keystone = **the physical prior as inductive bias** — *where does the network go?* (`the-physical-prior.md`). Assumes JOS's *Filters* + *PASP* chapters and PyTorch; leans on PASP since the `pinn`/`modal-synthesis` wikis are thin. ~18–22 sessions; tiered a/b/c capstone. |
| `audio-neural-vocoders/` | ⚪ Planned | Enrichment for [AI Music & Audio](curricula/ai-music-audio.md). Waveform generation from spectral or latent conditioning: WaveNet and fast/parallel variants → flow vocoders (WaveGlow, WaveFlow) → diffusion vocoders (DiffWave, WaveGrad and successors). Sources: `music423-2023/{wavenet,diffusion-vocoders}/`. |
| `audio-symbolic-music/` | ⚪ Planned | Enrichment for [AI Music & Audio](curricula/ai-music-audio.md). Sequence models at the score/MIDI level: Music Transformer → TonicNet → Anticipatory Music Transformer → LLM-era symbolic music. Sources: `music423-2023/ai-scores/`. |
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
`/lesson` command auto-seeds `progress.md` from `progress.template.md`. (The plugin
resolves the data root a little differently — see
[Option 1](#option-1-the-courses-claude-plugin-no-clone-needed).)

### The `courses` plugin (generated)

`courses-plugin/` holds one Skill per course and is served by the root
`.claude-plugin/marketplace.json`, which makes this repo a plugin marketplace
(`josmithiii-courses`). It is a **generated build output**, committed so GitHub
installs work — never edit it by hand. After editing any course, rebuild it:

```bash
tools/build_plugin.py --all            # or name specific courses: tools/build_plugin.py room-acoustics
tools/build_plugin.py --check          # fails if courses-plugin/ is stale (also run by tests/)
uvx pytest tests/
claude plugin validate --strict courses-plugin
```

When publishing content changes, also bump `PLUGIN_VERSION` in
`tools/build_plugin.py` so installed copies see a new version to update to.

The generator copies each course's Markdown into `skills/<course>/`, turns
`lesson.md` into `SKILL.md`, and swaps the "Content vs. learner state" sections of
`lesson.md` and `CLAUDE.md` for a plugin version: in the plugin the content is the
skill's own read-only folder (replaced on every update), and the data root resolves
as described above.

## Authoring a new course

Copy [`course-template/`](course-template/) and follow the checklist in its
[`README.md`](course-template/README.md). Short version:

1. `cp -r course-template <new-course-id>` and `cd` into it.
2. Delete the template's `README.md` (it's authoring instructions, not learner content).
3. Find/replace `{{COURSE-ID}}`, `{{COURSE TITLE}}`, and `{{ONE-LINE SCOPE}}` in the new folder.
4. Rewrite `syllabus.md` with your syllabus; adjust `progress.template.md` learner-profile fields and environment checkboxes.
5. Add a row to the *Courses* table above.
6. Rebuild the plugin so the new course ships there too: `tools/build_plugin.py --all`
   (see [The `courses` plugin](#the-courses-plugin-generated)).

No personal state to reset — it never lived in the repo. The `/lesson` command and
teaching loop are reusable as-is.
