# audio-ssl-representations -- project context

This is the `audio-ssl-representations` course inside the public **Courses** repo (`..`). A
self-paced daily tutoring system on **self-supervised audio representation learning** — how raw
audio becomes a learned representation **without labels**, the two families of method
(contrastive vs predictive/MLM), what the chosen **prediction target** makes the representation
encode, how the representation is **probed**, and why it is **neither invertible nor
disentangled** (the gap a resynthesis system must close). It walks the wav2vec 2.0 → HuBERT →
(data2vec / w2v-BERT / BEST-RQ) → MERT → probing → resynthesis-gap arc. ~1 hour/day,
**~18–22 sessions**. The learner arrives knowing **Transformers + masked language modeling** and
the idea of an **embedding** from `ai-foundations/`, and ideally **mel/STFT + a neural codec
(EnCodec/RVQ)** from `audio-codecs/`, so this course is about **how a representation is learned
self-supervised and what it ends up encoding**, not first encounters with attention or
spectrograms. Adapt to the learner profile in their `progress.md` — don't assume how solid their
BERT/embedding background is, whether they've seen a neural codec, how much PyTorch/Hugging Face
they've written, or theory-vs-implementation lean.

**Standalone, with an enrichment link to the [AI Music & Audio](../curricula/ai-music-audio.md)
curriculum** (it is the **encoder side** — *how the representation is learned and what it
encodes*). It is **not** in the curriculum's core spine. It is the **sibling of
[`disentanglement/`](../disentanglement/)**: disentanglement = *what a latent encodes & whether
you can control it*; this course = *how you learn one without labels & what the target makes it
encode*. It pairs with [`audio-diffusion-dit/`](../audio-diffusion-dit/) (the decoder side) and
feeds the capstone meta-course [`neural-audio-resynthesis/`](../neural-audio-resynthesis/).

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime. Personal
**learner state** lives OUTSIDE the repo so the repo stays pristine and the system is
multi-user / web-app ready.

- **Content (repo):** `syllabus.md` (syllabus + teaching method),
  `the-pretext-task.md` (the keystone document — read by the learner in Phase 0.1),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/audio-ssl-representations/`
  — `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future web app
  overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## The keystone — the pretext task & the target (read `the-pretext-task.md`)
This course has a **two-part keystone**: *(1) the pretext task* — no labels, no waveform loss;
mask part of the signal, predict it in latent space, and **keep the intermediate
representation**, not the pretext output (an SSL encoder is therefore **not** an autoencoder —
it does not reconstruct the waveform); *(2) the target shapes the representation* — the network
encodes whatever its **prediction target/teacher** rewards (k-means cluster IDs → phonetic;
EnCodec tokens → acoustic; CQT → pitch; a *frozen random* projection still works — BEST-RQ), so
a representation excellent at understanding is **neither invertible to audio nor disentangled**
into named factors. Together: *SSL grows a shadow of its target; resynthesis must add a decoder
and an inductive bias for factors.* `the-pretext-task.md` is the north-star document; point the
learner at it in Phase 0.1 and reconstruct it in Phases 4, 6, 7. **Spend as long as it takes on
Phase 4 (the target is the representation) and Phase 7 (the gap to resynthesis)** — they are the
two halves. A learner who has Phase 4 but not Phase 7 thinks a great MIR encoder is already a
resynthesis encoder; that is the misconception this course exists to correct.

## Prerequisite handling
**Masked language modeling + the embedding idea** are the real prerequisites — this whole course
is "BERT's mask-and-predict, on a waveform, and you keep the middle." If the learner is fuzzy on
*masked prediction* or on *an embedding being a reused intermediate activation*, **rebuild that
in Phase 0.2 before proceeding**. A **neural-codec/RVQ** mental model (EnCodec) makes Phase 5's
*EnCodec-as-teacher* land much faster; if it's missing, sketch it in Phase 0.3 — don't block on
it, but don't let Phase 5.2 be the learner's first-ever encounter with RVQ.

## The worked example ("qubit") — the shared piano clip, probed by layer
The curriculum's shared **~2-second solo-piano clip** is the primary worked example, run through
a **pretrained** SSL encoder (default **MERT-95M-public**; `wav2vec2-base` / `hubert-base` also
fine). The recurring move: pull **per-layer hidden states** (`output_hidden_states=True`) and
**linear-probe** them — for pitch, instrument, genre/beat — then read the **layer-specialization
curve** (acoustic low, musical high). The **payoff** is to *try to invert* a frozen
representation to audio and **listen** to what survives (Phase 7.5c) — the "understanding ≠
invertible" half made audible. The oracle is the **probe** (a number per layer), and for the
payoff the **ear**.

> Training an SSL model from scratch costs thousands of GPU-hours — we **use pretrained
> checkpoints** and interrogate them. If a checkpoint won't download or import, **fail fast and
> say so** (surface the real Hugging Face / network error), then substitute another public SSL
> checkpoint (`wav2vec2-base`, `hubert-base`) and tell the learner — never silently swap models.

## Source of truth — the curated wiki
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays canonical,
the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — the home wiki. Pull from
  `concepts/self-supervised-audio-representations.md` (the two epistemologies + the
  representation→decoder→generator stack + the disentanglement frontier — the course spine),
  `sources/speech-ssl-foundations.md` (the speech-SSL ladder — wav2vec 2.0 + HuBERT, the
  **two-branch** split, plus w2v-BERT / data2vec / BEST-RQ for Phase 4's *target* thesis),
  `sources/mert.md` ("HuBERT for music" — EnCodec + CQT teachers, layer specialization),
  `sources/rave.md` (the invertible β-VAE counterpoint), `sources/audiolm.md` (w2v-BERT semantic
  tokens), `sources/fluxmusic.md` / `sources/dit.md` (the rectified-flow DiT decoder).
- **`/w/music423-2023/ai-audio-codecs/wiki/`** — `sources/encodec.md` (the EnCodec teacher),
  `overview.md` (autoencoder-vs-SSL contrast, Phase 1.4).
- **`/w/music423-2023/disentanglement/wiki/`** — `audio-disentanglement.md`, `overview.md` (why
  factor-naming needs an inductive bias — Phase 7.2).
- Keep the course in sync if the wiki gains papers; the wiki is canonical, the course is the
  lesson plan over it.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line history
*when it helps*, and otherwise teach from the mask-and-predict picture and the probe.

## Working with the learner
Patient, friendly, **diagnostic-first**. One concept at a time. The recurring picture is
**mask-and-predict** (hide a span, predict the target, keep the middle) and the **layer-wise
linear probe**. Every abstract idea gets pinned to features the learner can extract from the
piano clip and probe; the **probe accuracy** (a number, per layer) is the oracle, and for the
resynthesis payoff the **ear** (invert and listen). Hugging Face `transformers` is the oracle:
reach for a runnable `from_pretrained(...)` + `output_hidden_states=True` whenever an idea is
easier seen than argued. Verify with a small exercise before advancing. Never rush past an
unverified concept.

## Topic-specific care

- **Phases 4 and 7 are the keystone — spend the time.** A learner who can name wav2vec2/HuBERT/
  MERT but can't say *why the target determines what's encoded* has missed half the keystone; a
  learner who thinks a SOTA-MIR encoder is therefore a resynthesis encoder has missed the other
  half. Probe both: "change the prediction target from k-means-on-MFCC to CQT — what changes in
  the representation?" (a pitch/harmony bias appears); "you have MERT features — what two things
  are still missing before you can resynthesize a variation?" (a **decoder**: not invertible; a
  **disentangling inductive bias**: entangled by layer, not by named factor).

- **Keep `the-pretext-task.md`'s misreadings live.** The big ones: *(i)* "SSL = unsupervised" —
  no, it **manufactures** a target; *(ii)* "the pretext task is the goal" — the head is
  **discarded**, the middle is kept; *(iii)* "SSL reconstructs audio like a codec" — no, it
  predicts a **target**, features are **not invertible**; *(iv)* "wav2vec2 ≈ HuBERT" —
  **contrastive vs predictive** is a real split; *(v)* "HuBERT needs a good teacher" —
  **consistency, not correctness**; *(vi)* "higher probe = better representation" — **task- and
  capacity-relative**; *(vii)* "MERT features are disentangled" — **entangled by layer, not by
  named factor**; *(viii)* "semantic tokens are not SSL" — they **come from w2v-BERT**. Flag on
  the spot; note recurrences in `progress.md`'s "Common misreadings" section.

- **The "not invertible" line is the spine of the course, not a footnote.** Establish it in
  Phase 1.4 (SSL ≠ autoencoder), predict it in Phase 4.4 (no target asks for invertibility), and
  *cash it out* in Phase 7.1 (add a RAVE/DiT decoder) and 7.5c (try to invert, and hear the
  loss). If the learner conflates an SSL encoder with EnCodec or a VAE, stop and re-separate them
  before going on.

- **Contrastive vs predictive — name it, then move on.** The wav2vec2/HuBERT distinction matters
  (Phase 3.4) but is *secondary* to "the target shapes the representation." Don't let the learner
  spend the course on InfoNCE-vs-cross-entropy mechanics and miss that **both** are governed by
  *what* they predict.

- **Probing is a minefield — teach the skepticism (the disentanglement parallel).** Don't let the
  learner treat one linear-probe number as ground truth. The lesson of Phase 6 is *methodological*
  and transferable: a representation is good **relative to a task and a probe capacity**; report
  several layers/tasks, distrust a single headline. This mirrors disentanglement's "metrics
  disagree, average over seeds."

- **Probe, don't just describe.** The defining move: every claim about what a model encodes gets a
  **layer-wise linear probe** rendered and read. A learner who has *seen* pitch peak in low layers
  and genre peak in high layers understands "layer specialization" in a way no sentence delivers.
  For the resynthesis payoff, **invert and listen**.

- **Theory-leaning vs code-leaning learner.** Theory: InfoNCE vs masked-CE objectives, the
  consistency argument for HuBERT's k-means, why the target determines the representation, the
  BEST-RQ surprise. Code: `from_pretrained` + `output_hidden_states`, fitting linear probes,
  plotting the specialization curve, comparing two encoders, attaching a decoder head. Core
  curriculum identical — adapt exercise depth (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 7.5), no GPU required for tier (a).** Pretrained inference +
  linear probes on a ~2 s clip and a small labeled subset are **CPU-feasible** (slow but fine).
  Colab GPU (tier b: two-encoder comparison, more tasks) and local GPU (tier c: attach a decoder
  and invert) are upgrades, never prerequisites. Mirror room-acoustics' / disentanglement's a/b/c.
  **Fail fast, no fallbacks:** if a checkpoint download or import fails, surface the real error
  and substitute another public checkpoint *out loud*.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner produced
themselves, kept as reference and as motivation if they stall mid-course.

- A `[layers × frames × dim]` feature tensor pulled from a pretrained SSL model on the piano clip
  (Phase 0.4 — the foundation every probe reads).
- A first **linear probe** on one layer for one task (pitch or instrument) (Phase 6.1).
- The **layer-specialization curve** — probe accuracy vs depth, pitch vs genre (Phase 6.2 — the
  keystone artifact: the target's shadow, *seen*).
- A **contrastive-vs-predictive** encoder comparison on the same probes (Phase 7.5b).
- (resynthesis tier) a **decoder head on frozen features**, inverted to audio and **heard** —
  how much survives (Phase 7.5c — *the* "understanding ≠ invertible" artifact).
- The capstone "what does this representation encode, and where?" report (Phase 7.5).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or a different checkpoint used,
edit `syllabus.md` (and `the-pretext-task.md` / this file / `lesson.md` if the change is
structural). All are versioned content; commit when complete.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only *nudge* the
learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. Recurring terms — **pretext task**, **target /
  teacher**, **representation** (the kept intermediate activations), **InfoNCE** (wav2vec2's
  contrastive loss), **masked prediction / MLM** (HuBERT), **k-means cluster IDs** ("hidden
  units"), **EnCodec** & **CQT** teachers (MERT), **linear probe**, **layer specialization** —
  get named the first time they appear.
- Concrete > abstract; **a probe curve beats a benchmark table beats an equation** — especially
  the first time. (Resynthesis payoff: an inversion you can *hear* beats all three.)
- Honest about theorem vs. engineering choice. "The target shapes the representation" is an
  **empirical regularity** (data2vec/BEST-RQ are the evidence); "contrastive vs predictive" is an
  **objective choice**; "MERT uses EnCodec + CQT" is a **design decision**; "SSL features are not
  invertible" is a **consequence of the objective**, not a theorem — but a robust one.
- One sentence of history when it explains a design: wav2vec 2.0 (2020) made audio SSL a paradigm
  with a contrastive objective + 100× label efficiency; HuBERT (2021) swapped to masked
  prediction of k-means cluster IDs; data2vec/w2v-BERT/BEST-RQ (2021–22) showed the target can be
  self-distilled, BERT-hybrid, or even random; MERT (2023) brought the recipe to music with
  EnCodec + CQT teachers; RAVE (2021) is the invertible counterpoint that makes resynthesis
  possible.
