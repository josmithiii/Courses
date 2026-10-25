# Neural Audio Resynthesis — Turning Recordings into Steerable Objects

**Learner profile:** Knows modern deep learning and has met the **AI Music & Audio** stack — a
**continuous-VAE latent + diffusion/DiT** picture (`audio-diffusion-dit/`) and **neural codecs**
(`audio-codecs/`) — at least by name. Ideally has also seen the three enrichment courses this
capstone integrates: **self-supervised audio representations** (`audio-ssl-representations/`),
**disentanglement** (`disentanglement/`), and **flow matching** (`flow-matching/`). **None of
these is a hard gate** (see *Prerequisites* below) — this is a course you can **plunge into**. It
is the **capstone meta-course** of the thread: *not a new body of theory* but an **integration
course** whose express purpose is **creating and editing audio with neural methods**. ~1 hour/day,
**~20–25 sessions** across **9 phases (0–8)** in **three acts** — *survey the field, drill the
load-bearing survivors, then confront evaluation and the frontier.*

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The phase numbers
below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisites — strongly recommended, none gated.** You can plunge in and try; the course is
honest about depth and hands you **1-page recall-primers** that *link back* to a feeder rather
than re-teach it ("you met this in X; here's the one slide we need"). Plunging in and getting in
over your head is the *intended* on-ramp — it is what motivates the trip back to the feeder you
now know you need.
- **Most load-bearing:** `ai-foundations/` + the **AI Music & Audio core** (`audio-codecs/`,
  `audio-diffusion-dit/`) — the continuous-VAE-latent + DiT picture is the loop's decode box.
- **Then:** `audio-ssl-representations/` (the *encode* box), `disentanglement/` (the *steer*
  box), `flow-matching/` (the *decode* objective). The drill-down phases each open with a recall-
  primer to the matching feeder.
- **Never re-taught from scratch.** The primer + a pointer is the contract; this course stays
  **integration**, not review.

**Where it sits:** the **capstone enrichment** of the [AI Music & Audio](../curricula/ai-music-audio.md)
curriculum — the **destination** the rest of the thread feeds. `flow-matching/` + `audio-codecs/`
+ `audio-diffusion-dit/` (the **generator**), `audio-ssl-representations/` (the
**representation**), `disentanglement/` (the **inductive bias**) all converge here. It is the
sibling-capstone of those enrichment courses, one level up: where they each teach **one box**,
this course **assembles the loop** and asks what it would take to *steer* it.

**The keystone — read [`the-resynthesis-loop.md`](the-resynthesis-loop.md) in Phase 0.** This
course has a **two-part keystone**: *(1) the resynthesis loop* — every system is one diagram,
**encode → (disentangle / steer) → decode**, and a recording becomes a **steerable object** when
you can run it; *(2) the control problem* — a learned latent is **expressive but illegible**, and
the whole course is the quest to win back **parametric-grade, legible control** over it. Together:
*resynthesis = the encode→steer→decode loop, and the whole game is winning back legible control
over the latent you steer.* We spend as long as it takes on **Phase 4** (the steer box — where the
control problem bites) and **Phase 6** (the loop assembled).

**The qubit (worked example):** the curriculum's shared **~2-second solo-piano clip** (carried
across courses 1–3 and `audio-ssl-representations/`), run through a **pretrained
resynthesis-capable model**. The recurring move is **"resynthesize a variation that preserves
identity while exploring around it"** — encode the clip, perturb in the latent, decode, then **A/B
listen**: *is it recognizably the same source, yet genuinely different?* The **stretch task** (the
editing payoff) is a **single-attribute edit** — change the **room** (reverb / space) *or* the
**timbre** while leaving the performance intact — the "steerable object" made audible, and the
direct tie to `disentanglement/`. The oracle is the **ear** (A/B), backed by an **identity /
similarity** number (embedding cosine / CLAP to the source) and a **distribution** number (FAD to
a reference set); the ear leads, the numbers corroborate.

**Default tooling — both, RAVE first.** The cleanest audible encode→steer→decode loop on a laptop
is a **pretrained RAVE** model (real-time, CPU-feasible) — *the loop is the lesson*, so RAVE is the
**main** tier-a tool. A **tiny SSL-latent + rectified-flow decoder** is the **second example /
optional enrichment**: faithful to the paradigm's architecture (the apex the course builds toward),
heavier and fiddlier on CPU. RAVE's decoder is a **GAN**, not the apex's DiT — and that contrast is
a *teaching moment* (Phase 5), not a defect.

**End state:** by the last lesson the learner can: **draw the encode→steer→decode loop** and slot
any neural-audio system onto it; **survey** the landscape (DDSP → codec+LM → continuous-VAE+DiT →
resynthesis-as-editing) and say which **box** each system advances; explain why the **continuous/
diffusion** route is the load-bearing one for **editing an existing recording** and why the
**discrete-token LM** route is surveyed then **set aside, with reasons**; state what each box
contributes and where its limit lives (encode: *not invertible*; steer: *not legibly
disentangled — the open box*; decode: *coherent variation, not inversion*); **build a resynthesis
pipeline from pretrained parts** (RAVE on a laptop; an SSL-latent + flow decoder as the faithful
variant) and produce a **variation that preserves identity**; **evaluate it honestly** — name the
**no-reference problem**, report **identity + distribution + listening**, and refuse a single
headline number; and **read a new 2026/2027 system** onto the loop and judge whether it is
load-bearing or a detail.

---

## ACT 0 — Orientation

## Phase 0 — The Loop, the Control Problem, the Tools
- **0.1** **The whole course in one frame.** The two epistemologies of synthesis —
  **parametric** (DDSP, FM, physical modeling: human-defined knobs, *legible but bounded*) vs
  **learned-representation** (encode a corpus; *expressive but implicit*). Read
  [`the-resynthesis-loop.md`](the-resynthesis-loop.md): the **loop** is the apparatus, the
  **control problem** is the question. Resynthesis turns a *static recording into a fluid,
  steerable object.*
- **0.2** **The loop drawn.** **encode → (disentangle / steer) → decode.** A recording is a
  steerable object exactly when you can run all three boxes. Each box is a feeder course; the
  drill-down (Act II) is its three chapters. Draw it; you will draw it every lesson.
- **0.3** **The control problem named.** A learned latent is **expressive but illegible** — it
  can represent the recording's full complexity, but no direction in it is *named*. Wanting
  **learned expressivity with knob-like steerability** is the whole course. This is the
  parametric-vs-learned tension made into a spine, not an essay.
- **0.4** **Tools.** `torch` + Hugging Face; load a **pretrained resynthesis-capable model**
  (default: a **RAVE** checkpoint — real-time, CPU-feasible), **encode** the shared piano clip to
  its latent, and **decode** it back. Confirm the loop runs end to end on a laptop. We **use
  pretrained checkpoints**; if one won't download or import, **fail fast and say so**, then
  substitute another public checkpoint *out loud* — never silently swap.
- **0.5** **The qubit.** The piano clip through the loop; the recurring task is **resynthesize a
  variation that preserves identity** — encode, **perturb** the latent, decode, **A/B listen**
  (*same source, yet different?*). The recurring picture is the encode→steer→decode loop drawn
  over the clip. The stretch (later) is a single-attribute **edit** (room or timbre).

---

## ACT I — THE SURVEY *(breadth, fast — orient and place, don't master)*

## Phase 1 — The Map of Neural Audio Generation
> Fast. Every system gets **placed on the loop**, not derived. The goal is a map, not mastery.
- **1.1** **Parametric / DDSP — the legible-but-bounded column.** Human-defined knobs (f0,
  harmonics, noise, reverb); differentiable DSP. The **contrast** the rest of the course is
  measured against — *referenced, not taught.* It defines what "legible control" even means.
- **1.2** **Codec + LM — the discrete-token route.** **AudioLM → MusicGen → VALL-E**: tokenize
  audio (RVQ), then **language-model** the tokens. Place it on the loop: a *discrete* encode, a
  *sequence-model* decode. Great for generation/continuation; hold the question of *editing* for
  Phase 2.
- **1.3** **Continuous-VAE + diffusion / DiT — the continuous route.** **AudioLDM → Stable Audio
  → FluxMusic → DiffRhythm / ACE-Step**: encode to a *continuous* VAE latent, **diffuse / flow**
  in it. Place it on the loop: a *continuous, steerable* encode; a generative decode that samples
  *around* a latent. *"A good generator is all you need" is the misreading to flag here* — the
  generator is one box.
- **1.4** **Resynthesis-as-editing — the destination.** **RAVE**, timbre transfer, and the
  course's worked **paradigm** (a rectified-flow DiT conditioned on an SSL latent). These are the
  systems that *run the whole loop on an existing recording.* Each placed on the loop; the rest
  of the course is their three boxes.

## Phase 2 — Reading the Field: Load-Bearing vs. Detail
> The **meta-skill**, taught explicitly. This is where the survivors are *chosen in front of the learner.*
- **2.1** **The load-bearing-survivors skill.** Which ideas survived contact with scale, which
  were dead ends or implementation trivia? Reading a fast-moving field is a *transferable* skill —
  the analogue of the research-hygiene lesson `disentanglement/` teaches with Locatello. Name it;
  it is a graded end-state.
- **2.2** **Three knobs, one taxonomy.** Every system is a choice of **representation × inductive-
  bias × generator** — the three boxes of the loop. Use the taxonomy to *compress* the survey:
  the survivors differ in *which box* they advance.
- **2.3** **The call, made out loud: continuous is the editing mainline.** For **resynthesis-as-
  editing of an existing recording**, the **continuous-latent + diffusion / flow** route is the
  load-bearing one — its latent is *continuous and steerable*, and conditioning on a source is
  natural. The **discrete-token LM** route is **consciously set aside for editing** (excellent for
  generation/continuation, **awkward for fine continuous steering** of a given recording). Making
  this call *out loud* **is the meta-skill in action** — not a hand-wave but a teachable claim
  with reasons.
- **2.4** **What stays in scope.** **Text-to-music-from-a-prompt** appears in the survey and as a
  *decoder*, but the course is about **resynthesizing an existing recording**, not prompting from
  nothing. **From-scratch training** is out — we use **pretrained checkpoints**. Draw the scope
  line clearly; the drill-down (Act II) walks the *continuous editing* mainline only.

---

## ACT II — THE DRILL-DOWN *(depth — the meat; each box of the loop)*

## Phase 3 — The Representation (ENCODE)
> Recall-primer to `audio-ssl-representations/` first; then apply to the clip.
- **3.1** **Recall-primer: the SSL conditioning latent.** *"You met this in `audio-ssl-
  representations/`."* The pretext task; the representation is a **shadow of its target**;
  **MERT** as "HuBERT for music." One slide, then forward — don't re-teach the whole course.
- **3.2** **"Captures the full complexity of a recording."** What that phrase means: a per-frame,
  per-layer representation rich enough to condition a generator. Pull SSL features for the piano
  clip; this is the **encode** box made concrete.
- **3.3** **Understanding-grade, not invertible.** The representation predicts a *target*, not the
  *waveform* — so it is the **conditioning signal**, not the audio. This is *why* the loop needs a
  separate decode box (Phase 5). The bright line between an SSL encoder and an autoencoder/codec.
- **3.4** **Which layer, for what.** Layer specialization (low = acoustic, high = musical) is the
  *practical* fact for conditioning — you choose **which layer** to read depending on whether you
  want timbre or structure. It is also the precise sense in which the latent is **entangled by
  layer, not by named factor** (carry to Phase 4).

## Phase 4 — The Inductive Bias (STEER) — keystone
> Spend as long as it takes. This is where the **control problem** bites hardest. Recall-primer to `disentanglement/`.
- **4.1** **Recall-primer: legible control needs a bias.** *"You met this in `disentanglement/`."*
  The TC decomposition; **β-VAE**'s knob; **Locatello**'s impossibility — unsupervised factor-
  naming is **unidentifiable**. One slide, then apply.
- **4.2** **Why the latent is illegible.** Which direction is "more reverb"? Nothing in an SSL or
  VAE objective *names* a direction. The latent is **expressive but illegible** — the control
  problem, stated precisely. This is the box the whole course circles.
- **4.3** **The cases that work — and why.** Supervised **pitch / timbre** disentanglement (Luo)
  works precisely because it adds **labels** — the inductive bias Locatello demands. β-VAE's knob
  (in RAVE) buys *less-entangled* dimensions but does **not name** them. *Steerability is exactly
  what's hard* — say so plainly.
- **4.4** **Steering the clip.** On the qubit: a **perturbation** (variation — always available)
  vs a **named edit** (room or timbre — only where a bias supplies the direction). The gap between
  them *is* the control problem; the named edit is the **stretch**, and the unsolved part is why.

## Phase 5 — The Generator (DECODE)
> Recall-primer to `flow-matching/` + `audio-diffusion-dit/`; then the real-time counterpoint.
- **5.1** **Recall-primer: generating *around* a latent.** *"You met this in `flow-matching/` +
  `audio-diffusion-dit/`."* Rectified flow / conditional flow matching; a **DiT** denoises toward
  the data manifold **conditioned on** a signal — not from noise alone. One slide, then forward.
- **5.2** **The apex decoder: rectified-flow DiT on an SSL latent.** Condition the DiT on the
  encode box's representation; **sample coherent variations** around the source. This is the
  course's worked **paradigm** — the faithful architecture the SSL-latent+flow tooling realizes
  (tiers b/c).
- **5.3** **The real-time counterpoint: RAVE.** A **β-VAE-plus-adversarial (GAN)** decoder —
  real-time, 48 kHz, CPU-feasible; timbre transfer by decoding a source latent through a target
  decoder. The **teaching moment**: RAVE's decoder is a **GAN, not the apex's DiT** — same loop,
  different decode box, and you can *hear* it on a laptop (tier a). Run the clip through both.
- **5.4** **Variation, not inversion.** A generative decoder samples *around* z; it does **not**
  faithfully invert. "Resynthesis = reconstruction" is the misreading to kill here —
  reconstruction is the **floor**, coherent variation is the goal.

## Phase 6 — Assembling the System — keystone
> Spend as long as it takes. The three boxes become one machine.
- **6.1** **The loop, built.** **SSL latent → (disentangling bias) → rectified-flow-DiT decoder →
  a variation of the clip.** The course's worked apex, assembled from pretrained parts. Draw the
  full diagram over the clip and run it.
- **6.2** **Where each piece's limit becomes the system's limit.** Encode: *not invertible* (so a
  generative decode is mandatory). Steer: *not legibly disentangled* (so named edits are
  fragile — the open box). Decode: *coherent variation, not inversion* (so eval has no reference —
  Phase 7). The system inherits every box's limit.
- **6.3** **Variation vs edit, on the assembled loop.** Variation-preserving-identity **always
  closes** (perturb-and-decode); the single-attribute **edit** closes only where a bias supplies a
  legible direction. Demonstrate both; be honest about which one is research-grade.
- **6.4** **Reading a new system onto the assembled loop.** Take a 2026/2027 paper and place it:
  which box does it advance? Is it load-bearing or a detail? The meta-skill (Phase 2), now
  exercised on the *assembled* picture.

---

## ACT III — EVALUATION & FRONTIER

## Phase 7 — The Evaluation Problem
> The no-reference challenge — why listening stays the oracle.
- **7.1** **No reference.** A *variation* has **no ground-truth target** — you cannot diff it
  against "the right answer," because there is no right answer. This is the structural difficulty
  that makes audio-resynthesis eval unlike classification or even reconstruction.
- **7.2** **Objective metrics, and what each misses.** **FAD** (distribution distance to a
  reference set), **CLAP / embedding cosine** (identity / similarity to the source), MIDI /
  transcription-based **structure** scores. Each captures *one* axis; none captures "coherent
  variation." Report **identity + distribution**, never one headline — "Evaluation = FAD" is the
  misreading to kill.
- **7.3** **Subjective protocols.** **MOS**, **A/B**, **MUSHRA** — what each does and doesn't
  capture, and why **listening stays the oracle**. The methodological sibling of audio-ssl's "one
  probe number doesn't settle it" and disentanglement's "metrics disagree."
- **7.4** **The eval skepticism, made a habit.** On the qubit: the **ear** leads (A/B: same
  source, genuinely different?), the **numbers corroborate** (cosine to source + FAD to a
  reference set). A pipeline that wins one number and fails the ear has failed. Carry this into the
  capstone.

## Phase 8 — The Open Frontier + Capstone
> The box we cannot yet steer — and the tiered build that takes you as far as you can go.
- **8.1** **The unsolved box, named.** **Self-supervised, decodable, attribute-disentangled**
  representations of **full recordings** — the *steer* box, still open. This is exactly
  `disentanglement/`'s Phase 8.4 frontier ∧ `audio-ssl-representations/`'s Phase 7 frontier, named
  as **one** problem: a representation that is expressive, invertible, *and* legibly steerable.
- **8.2** **Why it's hard, in one breath.** Encode gives expressivity but not invertibility;
  decode gives invertibility (via a generator) but not legible directions; steer wants legible
  directions but Locatello says unsupervised they're unidentifiable. The three boxes pull against
  each other — that tension *is* the frontier.
- **8.3** **Reading the frontier.** What a 2026/2027 paper would have to show to *advance the steer
  box* — and how to tell a genuine advance from a detail. The load-bearing-survivors skill, aimed
  at the open problem.
- **8.4** **Capstone — build, vary, evaluate honestly.** Tiered a/b/c (Phase 8.5). End state: the
  learner can *build a resynthesis pipeline from pretrained parts, produce a variation that
  preserves identity, evaluate it honestly, and read a new system onto the loop.*
- **8.5** **Capstone tiers — no GPU required for (a).**
  - **(a) CPU / default — RAVE, the audible loop.** Load a **pretrained RAVE** model; encode the
    piano clip, **perturb** the latent, decode a **variation**, and **A/B listen** (*same source,
    genuinely different?*). Optionally re-run the clip through the **tiny SSL-latent + flow
    decoder** as a second example — *feel the architecture the apex actually uses.* One-page report:
    *did identity survive? is it genuinely a variation?* — ear first, one number to corroborate.
  - **(b) Colab GPU — condition a flow / Stable-Audio-Open generation.** Condition a **rectified-
    flow / Stable-Audio-Open** generation on the clip's representation; explore the **distribution**
    of variations (FAD to a reference set); attempt **one attribute edit** (room or timbre).
  - **(c) Local GPU — the faithful pipeline.** **MERT** (or another SSL encoder) features →
    conditioned **rectified-flow DiT** decoder; attempt **disentangled steering**; the most
    research-flavored tier, where the open box (Phase 8.1) is felt directly.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If shaky,
   re-teach before continuing.
2. **Introduce one new concept** with the **loop** *before* notation. The recurring picture is the
   **encode→steer→decode loop drawn over the clip** ([`the-resynthesis-loop.md`](the-resynthesis-loop.md)):
   encode to a latent, move within it, decode a coherent variation. Slot every survey system onto
   it; draw on it constantly.
3. **Pin it to the clip.** Encode the **shared piano clip**, perturb, decode, and **A/B listen**.
   The **ear** is this course's oracle (same source, genuinely different?); an **identity** number
   (cosine / CLAP) and a **distribution** number (FAD) corroborate, never lead.
4. **Tiny exercise** to verify: place a named system on the loop ("which box does MusicGen
   advance?"), predict whether an edit will close ("can you name a 'more reverb' direction in a
   raw SSL latent? why not?"), or run a few lines that encode-perturb-decode the clip and judge the
   A/B. The exercise *is* the check.
5. **Common misreadings** when relevant — keep [`the-resynthesis-loop.md`](the-resynthesis-loop.md)'s
   list live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to `progress.md` and the
   day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences ("resynthesis is the encode→steer→decode loop; the
   latent is expressive but illegible; the whole game is winning back legible control").
2. Carry out the small task: place a system on the loop and say which box it advances; encode-
   perturb-decode the clip and judge the A/B; or name *why* a raw latent has no legible "room"
   direction.
3. Spot a deliberately wrong claim ("resynthesis = reconstruction" — no, coherent variation;
   "a good generator is all you need" — no, the loop needs the representation and the bias too;
   "FAD settles it" — no, no-reference, report identity + distribution + listening; "codec-LM and
   DiT are interchangeable for editing" — no, continuous is the editing mainline, with reasons).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wikis this course teaches from
This course is the *pedagogical* front-end of curated knowledge bases; the wikis stay canonical,
the course stays pedagogical. It teaches from the **same wikis as its feeders**. Read / link these
on JOS's machine:

- **[`ai-music-audio-gen/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-music-audio-gen/wiki)** — the home wiki. Concept pages:
  **`concepts/self-supervised-audio-representations.md`** (literally the resynthesis concept page —
  *the* spine), `concepts/codec-based-generation.md` (the discrete-LM route set aside in Phase 2).
  Source summaries: `sources/rave.md` (the tier-a audible loop), `sources/mert.md` (the encode
  box), `sources/fluxmusic.md` / `sources/dit.md` (the rectified-flow DiT decode box),
  `sources/stable-audio.md`, `sources/audiolm.md`, `sources/musicgen.md` (the survey).
- **[`diffusion/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/diffusion/wiki)** — the **DiT / rectified-flow decoder** side (Phase 5).
- **[`disentanglement/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/disentanglement/wiki)** — the **inductive-bias / control** side (Phase 4):
  `audio-disentanglement.md`, the impossibility result and why factor-naming needs a bias.
- **[`ddsp/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ddsp/wiki)** — the **parametric contrast** (Phase 1.1), legible-but-bounded.
- Same contract as the other courses: the wikis stay canonical, the course stays the pedagogical
  front-end; keep in sync as wikis gain papers.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line history
*when it helps*, and otherwise teach from the loop drawn over the clip and the A/B listen.

### Source systems (the survivors this course tracks)
- *The encode box:* **MERT** (Li, Yuan, Zhang, Ma et al. 2023, arXiv:2306.00107) and the
  speech-SSL lineage behind it (wav2vec 2.0, HuBERT) — via `audio-ssl-representations/`.
- *The steer box:* **Luo et al. (2019)** supervised pitch/timbre disentanglement; **Locatello et
  al. (2019)** the impossibility — via `disentanglement/`.
- *The decode box:* **rectified flow / conditional flow matching** (Liu et al. 2022; Lipman et al.
  2022) and the **audio DiT** line (**Stable Audio**, **FluxMusic**) — via `flow-matching/` +
  `audio-diffusion-dit/`. **RAVE** (Caillon & Esling 2021, arXiv:2111.05011) — the real-time
  adversarial counterpoint, the tier-a tool.
- *The survey (placed, not drilled):* **AudioLM**, **MusicGen**, **VALL-E** (codec→LM);
  **AudioLDM**, **DiffRhythm**, **ACE-Step** (continuous→diffusion); **DDSP** (Engel et al. 2020)
  the parametric contrast.
