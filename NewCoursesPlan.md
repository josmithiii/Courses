# New Courses — Plan and Progress

A working roadmap for courses being added to this repo. Two
independent threads in play: a **wisdom-traditions** thread
(Buddhism, Vedānta) and a **modern-ML topics** thread (flow
matching, …). Each course is scoped to a single coherent subject;
philosophy and practice are split where they'd otherwise blur.

## Status snapshot (2026-05-27)

| Course | Status | Notes |
|--------|--------|-------|
| `buddhism-early-philosophy/` | 🟢 **Active** | Just landed (commit `6210570`). Pali Canon doctrinal foundations: Four Noble Truths → Three Marks → Five Aggregates → Dependent Origination → *nibbāna*. ~40 sessions, 10 phases. Philosophy only. |
| `flow-matching/` | 🟢 **Active** | Just landed (this commit). From ODEs as generative models through Lipman 2023 (CFM), Liu 2023 (Rectified Flow), Tong 2024 (OT-CFM). ~25 sessions, 8 phases. 2-D toy distributions as the worked example throughout; PyTorch as oracle. Source PDFs at `/l/dttd/FlowStuff/`. |
| `room-acoustics/` | 🟢 **Active** | Just landed. From "what is a pressure wave?" to evaluating real performance/speech spaces. ~30 sessions, 9 phases. Keystone = the **Schroeder frequency** (wave-below / ray-above). Pinned to one shoebox room (5×4×3 m) analyzed both ways + a concert-hall foil. Born from a real *Treble-vs-Odeon* question (`motivating-question.md`) — earns every term in that answer, then goes further to RT60/C80/STI measurement. Capstone a/b/c (Python from scratch / REW / dataset). |
| `audio-codecs/` | 🟢 **Active** | Just landed. Course 1 of the **AI Music & Audio** curriculum (`curricula/ai-music-audio.md`). Raw waveforms → tokens & latents: brisk DSP → autoencoders → VQ-VAE → RVQ → SoundStream/EnCodec/DAC → **the discrete-token vs continuous-VAE fork** (keystone, `the-fork.md`) → semantic/acoustic tokens + eval. ~20 sessions, 8 phases (0–7). Pinned to the curriculum's shared ~2 s solo-piano clip, *heard* at every stage. Capstone a/b/c (CPU pretrained / Colab / local-GPU tiny-VQ-VAE). Next: `audio-codec-lms`, then `audio-diffusion-dit`. |
| `buddhism-mahayana-philosophy/` | ⚪ Planned | Direct sequel — Phase 8 of the early course (Abhidhamma sketch) sets up Nāgārjuna's critique. Mainstream Mahāyāna is the **largest** branch of Buddhism by adherents (East Asian + Tibetan). |
| `buddhism-sutra-readings/` | 💭 Candidate | Close-reading course (Heart, Diamond, Lotus, Vimalakīrti, Laṅkāvatāra). Probably comes *after* the two philosophy courses. |
| `buddhism-practices/` | 💭 Candidate (deferred) | Meditation, *śīla*, the Eightfold Path as instruction. JOS prefers philosophy first. Rajayana / Nanjō / "5 basic practices" thread fits here. |
| `hindu-philosophy/` (working title) | 💭 Candidate | Upaniṣads + Advaita Vedānta (Śaṅkara). Home for "we are all eyes of God" (*ātman = Brahman*) and "God playing hide-and-seek with himself" (*līlā*). JOS is interested. |

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
- **Modern-ML thread successors to `flow-matching/`** — natural
  candidates if the thread continues: a Schrödinger-bridge course
  (DSBM, SB-CFM), a flow-on-manifolds course, or pulling the
  trigger on `claude-code-and-tools/` and `claude-app/` (already
  ⚪ planned in the top-level README).
