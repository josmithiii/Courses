# The Resynthesis Loop & the Control Problem — This Course's Keystone

Room-acoustics has the Schroeder frequency; flow-matching has the conditional-expectation
identity; disentanglement has the TC decomposition & the impossibility; audio-ssl has the
pretext task & the target. **This capstone has two halves of one keystone**, and you need
both:

1. **The resynthesis loop** — *the apparatus.* Every neural-audio system in this course is one
   diagram: **encode → (disentangle / steer) → decode.** A recording becomes a **steerable
   object** exactly when you can (a) **encode** it to a latent that captures its full
   complexity, (b) **move** within that latent in a way that *means* something, and (c)
   **decode** back to coherent audio. This tells you the *machine*.
2. **The control problem** — *the question.* The loop is easy to draw and hard to *steer*: a
   learned latent is **expressive but illegible.** The whole course is the quest to recover
   **parametric-grade, legible control over a learned representation** — learned expressivity
   *with* knob-like steerability. This tells you the *tension* that drives everything.

Put them together and the field collapses to one sentence:

> **Neural resynthesis turns a static recording into a fluid, steerable object by running it
> through an encode→steer→decode loop over a learned representation — and the entire game is
> winning back *legible control* over a latent that is expressive but, by its nature, illegible.
> The drill-down chapters each attack one box of the loop; the frontier is the box we cannot
> yet steer.**

Read this in Phase 0, then return to it in **Phase 3** (encode — the representation), **Phase
4** (steer — the inductive bias, where the control problem bites hardest), **Phase 5** (decode —
the generator), **Phase 6** (the loop assembled), and **Phase 8** (the box we can't yet steer).
Every term in **bold** is earned somewhere in the syllabus; the phase is in brackets.

---

## The recurring picture: encode, steer, decode — drawn over the clip

```
   a recording x                                        a coherent VARIATION x̃
   (the ~2 s piano clip) [Phase 0.5]                    (same source, genuinely different) [Phase 6]
        │                                                        ▲
        ▼                                                        │
   ┌──────────┐        ┌───────────────────┐        ┌────────────────────┐
   │  ENCODE  │ ─ z ─▶ │   STEER  (move z)  │ ─ z' ─▶│      DECODE        │
   │ a learned│        │  • perturb (vary)  │        │ a GENERATIVE model │
   │  latent  │        │  • edit one factor │        │ samples AROUND z'  │
   └──────────┘        │    (room / timbre) │        └────────────────────┘
   SSL encoder         └───────────────────┘         rectified-flow DiT [Phase 5]
   [Phase 3]            the CONTROL PROBLEM lives here  (or a RAVE decoder, real-time)
                        — expressive but illegible [Phase 4]

   The latent is EXPRESSIVE (captures the recording's full complexity) but ILLEGIBLE
   (no named knobs). Winning back legible control over the STEER box is the whole course.
```

The course's oracle is the **ear** [Phase 7]: A/B the source against the variation — *is it
recognizably the same source, yet genuinely different?* Two numbers corroborate, never lead — an
**identity / similarity** score (embedding cosine, CLAP) and a **distribution** score (FAD to a
reference set). The recurring picture is this loop, and **every survey system gets slotted onto
it** [Phases 1–2]; the recurring task is to **resynthesize a variation that preserves identity
while exploring around the source** [Phase 0.5, 6], with a single-attribute **edit** (change the
*room* or the *timbre*, leave the performance intact) as the stretch.

---

## Half 1 — the loop: three boxes, three feeder courses [Phases 3–6]

The loop is not a metaphor; it is a literal pipeline, and each box is a course this capstone
integrates:

```
   ENCODE  [Phase 3]              STEER  [Phase 4]              DECODE  [Phase 5]
   ─────────────────             ─────────────────             ─────────────────
   a self-supervised             move within the latent        a generative model that
   representation that           so the move MEANS something   samples coherent audio
   "captures the full            — but the latent is           AROUND a conditioning
   complexity of a               entangled BY LAYER, not       latent, not from noise
   recording"                    by NAMED factor               alone
   (audio-ssl-representations)   (disentanglement)             (flow-matching +
   understanding-grade,          the inductive bias the        audio-diffusion-dit)
   NOT invertible                control problem demands       rectified-flow DiT;
                                                               RAVE as the real-time
                                                               counterpoint
```

- **Encode** is `audio-ssl-representations/`'s product: a representation that is *understanding*-
  grade but **not invertible** — so it is the conditioning signal, not the audio itself.
- **Steer** is `disentanglement/`'s problem: legible control needs an **inductive bias**;
  Locatello says unsupervised factor-naming is unidentifiable, so this box is where the control
  problem is hardest and the frontier still open.
- **Decode** is the generator from `flow-matching/` + `audio-diffusion-dit/`: a **rectified-flow
  DiT** that generates *around* a conditioning latent. **RAVE** — a β-VAE-plus-adversarial
  decoder — is the real-time counterpoint you can hear on a laptop (Phase 5, tier a).

Assemble the three [Phase 6] and you have the course's worked apex: **SSL latent → (disentangling
bias) → rectified-flow-DiT decoder → a variation of the clip.** Where each piece's limit lives is
where the *system's* limit lives.

## Half 2 — the control problem: expressive but illegible [Phase 4], and the two epistemologies

Here is the twist that organizes everything. There are **two epistemologies of synthesis**, and
the course is the tension between them [Phase 0, 1.1]:

```
   PARAMETRIC (DDSP, FM, physical modeling)      LEARNED-REPRESENTATION (this course)
   ──────────────────────────────────────       ──────────────────────────────────────
   human-defined knobs: f0, brightness,          a latent encoded from a corpus:
   decay, position                               every dimension matters, none is named
   LEGIBLE but BOUNDED                            EXPRESSIVE but ILLEGIBLE
   you know exactly what each knob does,          it can represent anything in the corpus,
   and exactly what it CAN'T reach                but you don't know which way to push
```

The parametric column is JOS's home turf and the course's **contrast, not its content** — it is
referenced to sharpen the question, never taught. The learned column is **expressive** (it
captures the recording's full complexity) but **illegible** (no knob is named). So two properties
the editing paradigm *needs* are exactly the ones a learned latent does **not** hand you:

- **Legible direction.** Which way in the latent is "more reverb"? "Brighter timbre"? Nothing in
  an SSL or VAE objective labels a direction — the latent entangles **by layer**, not by **named
  factor** (audio-ssl Phase 7.2). Naming a direction needs an **inductive bias** (disentanglement)
  — and unsupervised, it is **unidentifiable** (Locatello). This is the open box [Phase 8].
- **Coherent decode.** Move in the latent and the decoder must still produce *audio that holds
  together* — not a faithful inversion of the source (that's the floor) but a **coherent
  variation around** it. That is what a generative decoder buys you over a deterministic one
  [Phase 5].

That gap — *an expressive latent in hand, legible control over it wanted* — **is** the neural-
audio-resynthesis problem [Phase 8]. The course's secondary, transferable skill is **reading the
load-bearing survivors**: take a new 2026/2027 audio-gen paper and (1) place it on the
encode→steer→decode loop, (2) say which box it advances, (3) judge whether it is structural or a
detail.

---

## The misreadings this course exists to kill

Curated from the `ai-music-audio-gen/` wiki. The tutor flags each on the spot and logs
recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "Resynthesis = reconstruction." | The goal is **coherent variation around** the source, not faithful inversion. Reconstruction is the **floor**, not the goal. | Phase 0, 6 |
| "A good generator is all you need." | The loop needs the **representation** *and* the **inductive bias** too — a SOTA DiT on an **illegible** latent gives you no control. | Phase 1.3, 6 |
| "More disentanglement ⇒ better resynthesis." | Recall **Locatello**: identifiability needs an **inductive bias**; unsupervised factor-naming is **unsolved**. The steer box is the open one. | Phase 4, 8 |
| "Neural resynthesis replaces DSP synthesis." | Different **epistemology**, complementary — legible-but-bounded vs expressive-but-implicit. The course's whole point is wanting **both**. | Phase 1.1 |
| "Evaluation = FAD (or any one number)." | The **no-reference problem**: a variation has no ground-truth target. Report identity **+** distribution **+** **listening**; never one headline. | Phase 7 |
| "Codec-LM and diffusion-DiT are interchangeable routes to resynthesis." | For **editing an existing recording**, the **continuous/diffusion** route is load-bearing (continuous, steerable, natural to condition on a source); the **discrete-token LM** route is surveyed then **set aside, with reasons**. | Phase 2, 5 |
| "Text-to-music-from-a-prompt is what this course is about." | TTM appears in the **survey** and as a **decoder**; the course is about **resynthesizing an existing recording**, not prompting from nothing. | Phase 1, 4 (scope) |
| "We train these models." | We **use pretrained checkpoints**, tiered a/b/c. Training the apex from scratch is thousands of GPU-hours. | Phase 0.4, 8.5 |

---

## How the course earns the keystone

| Piece | Earned in |
|---|---|
| the **loop** drawn; the **control problem** named; the two epistemologies; the loop runs end-to-end on the clip | **Phase 0** |
| the **map** of neural audio generation — every system *placed on the loop* | **Phase 1** |
| **reading the field**: load-bearing vs detail; codec-LM **consciously set aside for editing** | **Phase 2** |
| **encode** — the SSL conditioning latent: full complexity, not invertible | **Phase 3** |
| **steer** — the inductive bias: why legible control is hard (the control problem, sharpest) | **Phase 4** (keystone) |
| **decode** — the rectified-flow DiT generating *around* a latent; RAVE the real-time counterpoint | **Phase 5** |
| **the loop assembled** — SSL latent → bias → DiT decoder → a variation of the clip | **Phase 6** (keystone) |
| **the evaluation problem** — no reference; identity + distribution + listening | **Phase 7** |
| **the open frontier** — self-supervised, decodable, attribute-disentangled; the box we can't steer | **Phase 8** |
