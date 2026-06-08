# New Courses — Plan and Progress

A working roadmap for courses being added to this repo. Two
independent threads in play: a **wisdom-traditions** thread
(Buddhism, Vedānta) and a **modern-ML topics** thread (flow
matching, …). Each course is scoped to a single coherent subject;
philosophy and practice are split where they'd otherwise blur.

## Status snapshot (2026-06-07)

| Course | Status | Notes |
|--------|--------|-------|
| `buddhism-early-philosophy/` | 🟢 **Active** | Just landed (commit `6210570`). Pali Canon doctrinal foundations: Four Noble Truths → Three Marks → Five Aggregates → Dependent Origination → *nibbāna*. ~40 sessions, 10 phases. Philosophy only. |
| `flow-matching/` | 🟢 **Active** | Just landed (this commit). From ODEs as generative models through Lipman 2023 (CFM), Liu 2023 (Rectified Flow), Tong 2024 (OT-CFM). ~25 sessions, 8 phases. 2-D toy distributions as the worked example throughout; PyTorch as oracle. Source PDFs at `/l/dttd/FlowStuff/`. |
| `room-acoustics/` | 🟢 **Active** | Just landed. From "what is a pressure wave?" to evaluating real performance/speech spaces. ~30 sessions, 9 phases. Keystone = the **Schroeder frequency** (wave-below / ray-above). Pinned to one shoebox room (5×4×3 m) analyzed both ways + a concert-hall foil. Born from a real *Treble-vs-Odeon* question (`motivating-question.md`) — earns every term in that answer, then goes further to RT60/C80/STI measurement. Capstone a/b/c (Python from scratch / REW / dataset). |
| `audio-codecs/` | 🟢 **Active** | Just landed. Course 1 of the **AI Music & Audio** curriculum (`curricula/ai-music-audio.md`). Raw waveforms → tokens & latents: brisk DSP → autoencoders → VQ-VAE → RVQ → SoundStream/EnCodec/DAC → **the discrete-token vs continuous-VAE fork** (keystone, `the-fork.md`) → semantic/acoustic tokens + eval. ~20 sessions, 8 phases (0–7). Pinned to the curriculum's shared ~2 s solo-piano clip, *heard* at every stage. Capstone a/b/c (CPU pretrained / Colab / local-GPU tiny-VQ-VAE). Next: `audio-codec-lms`, then `audio-diffusion-dit`. |
| `audio-codec-lms/` | 🟢 **Active** | Just landed. Course 2 of the **AI Music & Audio** curriculum — the discrete-token (language-model) branch of course 1's fork. WaveNet → Jukebox → AudioLM (semantic+acoustic) → MusicLM (MuLan) → MusicGen (single-stage codebook patterns) → VampNet/MAGNeT (masked/NAR) → VALLE/MIDI-VALLE (codec-LM, *not* a DiT). ~25 sessions, 9 phases (0–8). Keystone = the **RVQ token grid** (`the-token-grid.md`). Continue/infill/condition the shared piano clip; tiered MusicGen/audiocraft capstone. Next: `audio-diffusion-dit`. |
| `audio-diffusion-dit/` | 🟢 **Active** | Just landed. Course 3 (final) of the **AI Music & Audio** curriculum — the continuous-VAE (diffusion) branch of course 1's fork, **completing the curriculum**. Latent diffusion (AudioLDM → Tango → AudioLDM 2) → **the DiT** (patchify + adaLN-Zero) → Stable Audio (continuous-VAE + timing, *still a U-Net*) → **the U-Net→DiT swap** (Long-Form Latent Diffusion / Stable Audio Open) → rectified-flow MM-DiT (FluxMusic) → DiffRhythm / ACE-Step (LM-planner + DiT-renderer). ~25 sessions, 9 phases (0–8). Keystone = the **latent canvas** (`the-latent-canvas.md`); ships a self-contained `rectified-flow-primer.md` linking to `flow-matching/`. *Denoise* the shared piano clip; tiered Stable-Audio-Open/DiffRhythm capstone (a/b/c). |
| `buddhism-mahayana-philosophy/` | ⚪ Planned | Direct sequel — Phase 8 of the early course (Abhidhamma sketch) sets up Nāgārjuna's critique. Mainstream Mahāyāna is the **largest** branch of Buddhism by adherents (East Asian + Tibetan). |
| `buddhism-sutra-readings/` | 💭 Candidate | Close-reading course (Heart, Diamond, Lotus, Vimalakīrti, Laṅkāvatāra). Probably comes *after* the two philosophy courses. |
| `buddhism-practices/` | 💭 Candidate (deferred) | Meditation, *śīla*, the Eightfold Path as instruction. JOS prefers philosophy first. Rajayana / Nanjō / "5 basic practices" thread fits here. |
| `hindu-philosophy/` (working title) | 💭 Candidate | Upaniṣads + Advaita Vedānta (Śaṅkara). Home for "we are all eyes of God" (*ātman = Brahman*) and "God playing hide-and-seek with himself" (*līlā*). JOS is interested. |
| `disentanglement/` | 🟢 **Active** | Just landed. Disentangled representation learning: InfoGAN → β-VAE → Burgess (information bottleneck) → FactorVAE / β-TCVAE (**isolating total correlation**) → **Locatello's impossibility result** → pitch/timbre audio (Luo). ~15–18 sessions, 9 phases (0–8). Two-part keystone = **the decomposition & the impossibility** (`the-decomposition.md`): TC is the disentanglement driver, but the objective alone can't identify factors without an inductive bias. Pinned to **dSprites** (latent traversals + MIG) with an audio pitch/timbre payoff; tiered a/b/c capstone (CPU dSprites / Colab multi-seed / local-GPU audio swap). Standalone; **enrichment** for the AI Music & Audio curriculum. Source of truth: new `music423-2023/disentanglement/` wiki. |
| `audio-ssl-representations/` | 🟢 **Active** | Just landed. The **encoder side** the AI Music & Audio curriculum only ever treated *instrumentally* (as the source of "semantic tokens"). Self-supervised audio representation learning as a subject in its own right: contrastive (**wav2vec 2.0**) → masked prediction (**HuBERT**) → *the target shapes the representation* (data2vec / w2v-BERT / **BEST-RQ**) → music (**MERT**: EnCodec + CQT teachers) → **probing** → the resynthesis gap (not invertible, not disentangled). ~18–22 sessions, 8 phases (0–7). Two-part keystone = **the pretext task & the target** (`the-pretext-task.md`): SSL grows a *shadow of its prediction target*, so an understanding-grade encoder is neither invertible nor factor-disentangled. Pinned to the curriculum's shared **piano clip**, probed **layer by layer** (specialization curve as oracle); tiered a/b/c capstone (CPU probes / Colab two-encoder / local-GPU invert-and-listen). Standalone; **encoder-side enrichment** for AI Music & Audio and **sibling of `disentanglement/`**. Source of truth: `music423-2023/ai-music-audio-gen/` wiki. |
| `neural-audio-resynthesis/` | 🟢 **Active** (capstone **meta-course**) | Just landed. The **integration course** — not a new body of theory but a *survey + drill-down* that ties the prerequisites/enrichments together for one express purpose: **creating and editing audio with neural methods.** Surveys the field (parametric/DDSP → codec-LM → continuous-VAE/DiT → resynthesis-as-editing), then **drills the load-bearing survivors** into the **encode→steer→decode** loop: a self-supervised conditioning representation (`audio-ssl-representations/`) + a disentangling inductive bias (`disentanglement/`) + a rectified-flow-DiT decoder (`flow-matching/` + `audio-diffusion-dit/`) = **the neural-audio-resynthesis paradigm** (static recording → steerable object), closing with the **no-reference evaluation challenge** and the open frontier. ~20–25 sessions, 9 phases (0–8), three acts (survey → drill-down → evaluation). Two-part keystone = **the resynthesis loop & the control problem** (`the-resynthesis-loop.md`): the latent is expressive but illegible; the game is winning back legible control. Pinned to the shared **piano clip** — *resynthesize a variation that preserves identity*, A/B listen (ear-first oracle); tiered a/b/c capstone (**RAVE on CPU** / Colab flow-conditioning / local-GPU MERT-latent DiT). **Plunge-in friendly — no hard prereq gates** (strong recommendations + recall-primers); **capstone enrichment** for AI Music & Audio. Source of truth: `music423-2023/ai-music-audio-gen/` wiki (+ diffusion, disentanglement, ddsp). Design spec: [`NeuralAudioResynthesisPlan.md`](NeuralAudioResynthesisPlan.md). |

Legend: 🟢 active · ⚪ planned · 💭 candidate (not committed)

## Buddhism — what we decided

- **Philosophy and practice split into separate courses.** JOS is
  interested in philosophy teachings, not (yet) practices.
- **Early Buddhism first, then Mahāyāna.** The Mahāyāna course
  assumes the early doctrines as its starting point — Nāgārjuna's
  Madhyamaka critique is *aimed at* the Abhidhamma reification of
  *dhammas*, which the early-philosophy course's Phase 8 introduces
  for exactly this reason.
- **Texts and tooling.** Pali Canon via **SuttaCentral**
  (suttacentral.net, Bhikkhu Sujato translations) primary; **Access
  to Insight** (Ṭhānissaro et al.) secondary. Browser only — no
  software install needed.
- **Pedagogical "qubit" of the Buddhism courses:** a 10-second
  introspectable moment of ordinary experience (hearing a sound,
  tasting tea, a flash of irritation), decomposed through whichever
  doctrine is in play. Returned to relentlessly, the way the
  quantum-states course returns to the qubit.
- **Standard misreadings flagged from day one** so they don't take
  root: *anattā* as annihilationism; *nibbāna* as a place or as
  non-existence; *kamma* as cosmic justice. The CLAUDE.md tells the
  tutor to correct on the spot and add to a running "misreading
  file" in the worked-example bank.
- **Out of scope (deliberately).** Meditation instructions, monastic
  rules (*Vinaya*), *Jātaka* folklore, devotional material. Each has
  (or will have) its own home; the philosophy courses stay focused.

## Hindu / Vedānta — where it fits

JOS resonates with several ideas that are precisely located in the
Indian tradition:

- **"We are all eyes of God"** ≈ *ātman = Brahman* — the
  Upaniṣadic / Advaita claim that the individual self is identical
  with the universal Self (Śaṅkara, ~8th c. CE).
- **"God likes to hide from himself"** ≈ *līlā* (divine play) — the
  One becomes the many in order to experience itself. Alan Watts
  popularized this exact phrasing in English; the roots are
  Upaniṣadic.

A future `hindu-philosophy/` (or `vedanta/`) course would start from
the major Upaniṣads (Bṛhadāraṇyaka, Chāndogya, Kaṭha, Īśa, Muṇḍaka)
and move through Śaṅkara's Advaita Vedānta, optionally touching the
Bhagavad Gītā as a synthesis text.

**A note on the original list:** "Ramayana" (Vālmīki's epic) is
*Hindu*, not Buddhist — it would belong in a Hindu/Indian-literature
course, not a Buddhist one. The recommendation from JOS's colleague
seems to mix both traditions, which is normal: they share a milieu
but disagree sharply on metaphysics (the *ātman/Brahman* identity is
exactly what early Buddhism rejects with *anattā*). The two
traditions' disagreement is worth meeting head-on, not blurred.

## Flow Matching — what we decided

- **Three foundational papers as the spine.** The course follows
  the historical and conceptual arc: Lipman 2023 (CFM) → Liu 2023
  (Rectified Flow) → Tong 2024 (OT-CFM). The PDFs at
  `/l/dttd/FlowStuff/` are the canonical sources; the curriculum
  pulls figures and derivations from them as needed.
- **The conditional-expectation identity is the whole course.**
  $u_t(x) = \mathbb{E}[u_t(x \mid x_1) \mid x_t = x]$ is what makes
  "simulation-free" training possible. Topic 4.3 spends as long as
  it takes to make this land — everything later (rectified flow,
  OT-CFM, generalized CFM) is a different choice of path or coupling
  sitting on top of this same identity.
- **Pedagogical "qubit" of the flow-matching course:** a 2-D toy
  distribution (two-moons / two-Gaussians / checkerboard) that the
  learner trains on, plots samples from, and quiver-plots the
  learned vector field over. Returned to relentlessly, the way the
  quantum-states course returns to the qubit and the Buddhism
  courses return to a 10-second moment of experience.
- **Standard misreadings flagged from day one:** confusing the
  *marginal* path/velocity with the *conditional* one (the CFM
  trick lives on this distinction); confusing the learned velocity
  $u_t$ with the score $\nabla\log p_t$ (related via the
  probability-flow ODE, not equal in general). The CLAUDE.md tells
  the tutor to correct on the spot.
- **Theory-lean vs. implementation-lean** is the analogue of the
  quantum-states "physics vs. quantum-information" split. Same core
  curriculum, different exercise depth; the lean is recorded in
  `progress.md`.

## Room Acoustics — what we decided

- **Born from a real question, not a syllabus.** A student asked an
  expert *"when should I use Treble Tech vs. Odeon?"* and got an
  answer dense with unexplained terms (Schroeder frequency, wave vs.
  geometrical solvers, RIRs, the f⁴ cost scaling, C80/STI). The
  course's mandate is to **earn every term in that answer and then
  go further** — to where she can evaluate a real room herself. The
  verbatim exchange is preserved as `motivating-question.md` and
  used as the course's north star (read in Phase 0, reconstructed in
  Phases 4.4 and 5.4).
- **The Schroeder frequency is the keystone** ($f_s \approx
  2000\sqrt{\text{RT60}/V}$). Below it the field is modal / wave-like
  → a wave solver is needed; above it the field is statistical /
  diffuse → rays (geometrical acoustics) are valid and far cheaper.
  This single dichotomy organizes the whole course and the whole
  Treble-vs-Odeon answer — it's the analogue of flow-matching's
  conditional-expectation identity. Phase 4 spends as long as it
  takes to make it land.
- **Pedagogical "qubit": one shoebox room, analyzed two ways.** A
  5×4×3 m room (V=60 m³) whose discrete modes (wave picture) and
  Sabine reverberation (statistical picture) the learner computes
  herself, meeting at its Schroeder frequency (≈183 Hz); plus a
  **concert-hall foil** (V≈15000 m³, f_s≈23 Hz) showing why big
  halls live entirely above Schroeder. Returned to relentlessly, the
  way quantum-states returns to the qubit and flow-matching to
  two-moons.
- **Naming.** Chosen `room-acoustics` over `spatial-acoustics`
  (which reads as spatial *audio* / HRTF / Ambisonics) and
  `architectural-acoustics` (broader/more formal) — narrowest and
  clearest for the music-hall + speech-room culmination.
- **Scope: physics-led, with one psychoacoustics phase.** Core is
  physical room acoustics (modes → reverberation → Schroeder →
  solvers → ISO 3382 / STI parameters); Phase 6 brings in spatial
  hearing (ITD/ILD, the precedence effect) precisely to motivate why
  the parameters split early/late where they do (C80 at 80 ms music,
  C50 at 50 ms speech). Not a spatial-audio / HRTF-reproduction
  course.
- **Standard misreadings flagged from day one:** the two different
  Schroeders (the *frequency* vs. the backward-*integration*
  method); "RT60 is one number" (it's per-band); "GA is just a worse
  approximation" (above Schroeder it's correct *and* cheaper); "more
  reverb = richer" (clarity vs. reverberance trade off; speech vs.
  music differ); absorption vs. scattering coefficient. CLAUDE.md
  tells the tutor to correct on the spot and keep a running list.
- **Hands-on vs. conceptual lean** (analogue of the
  theory/implementation split). Capstone is learner-chosen a/b/c:
  (a) Python from scratch — measure a real room via swept-sine →
  RIR → parameters, or simulate with `pyroomacoustics`; (b) REW +
  light Python; (c) dataset/conceptual — no mic needed. Chosen
  partway through Phase 6.

## Neural audio resynthesis — where it fits

**Neural audio resynthesis is a standing end goal for this thread**
(an upcoming talk was the proximate nudge, but it's one of many): replace
parametric synthesis (FM, wavetable, physical modeling, spectral) with a
**self-supervised learned latent** that captures a recording's tonal
character, room acoustics, signal chain, and performer articulation
*while minimizing entanglement* with the underlying composition, then
resynthesize coherent variations with a **rectified-flow diffusion
transformer** conditioned on that latent — turning static recordings into
"fluid, adaptable, steerable objects." The `neural-audio-resynthesis/`
meta-course is the eventual destination; the courses below are what it
draws on.

**Recommended study sequence (covers the paradigm, all already authored):**

1. **`ai-foundations/`** *(prereq)* — MLP → Transformers → basic diffusion.
2. **`flow-matching/`** — the **rectified-flow** training objective behind
   the resynthesis generator (Liu 2023 is named explicitly there).
3. **`audio-codecs/`** — raw audio → **continuous-VAE latent**; the
   discrete-vs-continuous fork (resynthesis lives on the continuous side);
   semantic-vs-acoustic, which first introduces SSL representations.
4. **`audio-ssl-representations/`** — *how the conditioning representation
   is learned without labels, and why it's neither invertible nor
   disentangled* — the encoder side the paradigm rests on.
5. **`audio-diffusion-dit/`** — the **rectified-flow MM-DiT** conditioned
   on a continuous latent; *exactly* the resynthesis decoder architecture.
6. **`disentanglement/`** — *minimizing the entanglement* between
   attributes and composition. Its **Phase 8.4 ("the open frontier")**
   names the program almost verbatim: self-supervised, decodable,
   attribute-disentangled representations of *full recordings* — decoder
   side (rectified-flow DiT / RAVE) mature, representation side unsolved.

**Holes found → resolution:**

- **`audio-ssl-representations/`** ✅ **built** (🟢 active). The genuine
  gap: the curriculum touched SSL only as *the place semantic tokens come
  from* (w2v-BERT in `audio-codecs`/`audio-codec-lms`) and never taught
  self-supervised audio representation learning as a subject — yet the
  resynthesis paradigm's *entire foundation* is "self-supervised learned
  audio representations." Now a full ~18–22-session course (wav2vec 2.0 → HuBERT
  → *the target shapes the representation* → MERT → probing → the
  resynthesis gap), the **encoder-side sibling of `disentanglement/`**.
  Two-part keystone (`the-pretext-task.md`): SSL grows a *shadow of its
  prediction target*, so a great MIR encoder is **neither invertible nor
  disentangled** — which is exactly what hands off to the meta-course.
- **`neural-audio-resynthesis/`** — 🟢 **authored** as the **capstone meta-course**
  (JOS's framing): not new theory but a *survey + drill-down* whose express
  purpose is **creating and editing audio with neural methods.** It surveys the
  field, then drills the **load-bearing survivors** into the **encode→steer→decode**
  loop, composing them into the neural-audio-resynthesis paradigm: SSL conditioning
  representation (`audio-ssl-representations/`) + disentangling inductive bias
  (`disentanglement/`) + rectified-flow-DiT decoder (`flow-matching/` +
  `audio-diffusion-dit/`), closing on the no-reference evaluation problem and the
  open frontier. Two-part keystone (`the-resynthesis-loop.md`): the latent is
  *expressive but illegible*; the game is winning back legible control. **Plunge-in
  friendly — no hard prereq gates** (strong recommendations + recall-primers). Design
  spec and resolved decisions: [`NeuralAudioResynthesisPlan.md`](NeuralAudioResynthesisPlan.md).

**The dependency picture (what feeds the meta-course):**

```
  ai-foundations ─┬─▶ audio-codecs ─┬─▶ audio-codec-lms        (codec→LM paradigm)
                  │                 └─▶ audio-diffusion-dit ──┐ (continuous-VAE→DiT paradigm)
                  │                                            │
  flow-matching ──┴──────────────────────────────────────────┤ (rectified-flow objective)
                                                              │
  disentanglement ──────────────── (what a latent encodes) ──┤
  audio-ssl-representations ─────── (how it's learned) ───────┤
                                                              ▼
                                          neural-audio-resynthesis  (meta-course:
                                          survey + drill-down → the neural-audio-resynthesis paradigm)
```

## Wisdom-traditions seed (from colleague)

These are the original notes JOS jotted down, separate from the
flow-matching prompt:

```
ramayana
mahayana
rajayana - nanjou - 5 basic practices
wikipedia
go thru the sutras
experience it
```

How each thread is being routed:

- **ramayana** → Hindu / Indian-literature material (future
  `hindu-philosophy/` or its own epics course)
- **mahayana** → `buddhism-mahayana-philosophy/` (planned)
- **rajayana — nanjō — 5 basic practices** → unusual term;
  possibly Nanjō Bunyū's classification (the 19th-c. Japanese
  Buddhologist who indexed the Chinese Tripiṭaka), or a specific
  teacher's framing of Mahāyāna practice. Practice-flavored — fits
  the deferred `buddhism-practices/` candidate. Worth asking the
  colleague to clarify the source.
- **wikipedia / go thru the sutras / experience it** →
  `buddhism-sutra-readings/` candidate (close-reading course)

## Next likely moves

- **`buddhism-mahayana-philosophy/`** is the natural next
  wisdom-traditions build — it has the strongest internal
  continuation from what's shipped, and Mahāyāna is mainstream
  enough to be worth a dedicated course.
- **`hindu-philosophy/`** is interesting and on the list; the
  philosophical-comparison value goes up sharply *after* the
  early-Buddhism course exists (so that "early Buddhism vs. Advaita
  Vedānta" becomes a live comparison rather than a wash).
- **Modern-ML thread successors to `flow-matching/`** — ✅
  **`disentanglement/`** just landed (the representation side — what a VAE
  latent encodes — enriching the AI Music & Audio curriculum). Remaining
  candidates if the thread continues: a Schrödinger-bridge course (DSBM,
  SB-CFM); a flow-on-manifolds course; or pulling the trigger on
  `claude-code-and-tools/` and `claude-app/` (already ⚪ planned in the
  top-level README).
  *(Note: `flow-matching/` now links forward to `audio-diffusion-dit/`
  — SD3 → FluxMusic's rectified-flow MM-DiT is where the thread lands in
  audio, tracked in the `music423-2023/diffusion/` wiki — and to
  `disentanglement/` for the representation side.)*
