# Self-Supervised Audio Representations — Learning What a Recording *Is*, Without Labels

**Learner profile:** Knows modern deep learning — **CNNs, Transformers/attention, masked
language modeling (BERT) by name**, and the idea of an **embedding / representation** — at the
level of `ai-foundations/`. Has met **mel-spectrograms, the STFT, and a neural codec
(EnCodec/RVQ)** at the level of [`audio-codecs/`](../audio-codecs/) (recommended, not strictly
required — Phase 0.3 recaps the audio front-end). No prior exposure to self-supervised learning
assumed. This is a focused **~18–22 session** course on one idea — *manufacture supervision from
unlabeled audio, and the representation is a shadow of the target you chose* — and its sober
limit (the representation is neither invertible nor disentangled). ~1 hour/day, one concept at a
time, every concept checked with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisite:** Transformers + masked language modeling (BERT-style) and the notion of an
embedding. If "mask a token and predict it" and "an embedding is an intermediate activation you
reuse" are not solid, rebuild them in Phase 0.2 — the entire course is a variation on that one
move applied to audio. A neural-codec/RVQ mental model (`audio-codecs/`) makes Phase 5's
EnCodec teacher land faster; if absent, Phase 0.3 sketches it.

**Where it sits:** a **standalone** course, and the **encoder-side enrichment** for the
[AI Music & Audio](../curricula/ai-music-audio.md) curriculum. It is the sibling of
[`disentanglement/`](../disentanglement/): disentanglement asks *what a latent encodes and
whether you can control it*; this course asks *how you learn a representation without labels, and
what — given the target you picked — it ends up encoding*. Together they are the **representation
side** of the curriculum's continuous-VAE branch; [`audio-diffusion-dit/`](../audio-diffusion-dit/)
is the **decoder side**. All three feed the capstone meta-course
[`neural-audio-resynthesis/`](../neural-audio-resynthesis/).

**The keystone — read [`the-pretext-task.md`](the-pretext-task.md) in Phase 0.1.** This course
has a **two-part keystone**: *(1) the pretext task* — there are no labels and no waveform loss;
you hide part of the signal and predict it in latent space, and you keep the **intermediate
representation**, not the pretext output; *(2) the target shapes the representation* — the
network encodes whatever its **prediction target** rewards, so a representation excellent at
music understanding is **neither invertible to audio nor disentangled** into named factors.
Together: *SSL grows a shadow of its target; resynthesis must bolt invertibility and
disentanglement on top.* We spend as long as it takes on **Phase 4** (the target *is* the
representation) and **Phase 7** (the gap to resynthesis).

**The qubit (worked example):** the curriculum's shared **~2-second solo-piano clip**, run
through a **pretrained SSL encoder** (default **MERT-95M-public**; a base **wav2vec 2.0** or
**HuBERT** from Hugging Face also works). The recurring move is to **probe** the per-frame,
per-**layer** embeddings — train a tiny **linear probe** for pitch, for instrument, for
genre/beat — and read the **layer-specialization curve** (acoustic content peaks in low/mid
layers, musical/structural content in high layers). The **payoff** is to *try to invert* a
frozen SSL representation back to audio and **listen** to what survives — making the
"understanding ≠ invertible" half of the keystone audible. The oracle is the **probe** (a number
per layer) and, for the payoff, the **ear**.

**End state:** by the last lesson the learner can: distinguish **supervised / unsupervised /
self-supervised** and explain the **pretext task**; describe **wav2vec 2.0**'s contrastive
InfoNCE objective and its **learned product quantizer**, and **HuBERT**'s **masked prediction of
k-means cluster IDs** with its **consistency-over-correctness** iteration; state *why the
prediction target determines what the representation encodes* (data2vec / w2v-BERT / BEST-RQ as
evidence); explain **MERT** as "HuBERT for music" with its **EnCodec + CQT** teachers and its
**layer specialization**; run and read a **linear probe** (and say why one probe number doesn't
settle "which representation is better"); and explain precisely why SSL features are **not
invertible** and **not disentangled**, what that costs the **neural-audio-resynthesis** paradigm,
and which two pieces (a decoder; an inductive bias for factors) must be added.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one frame.** The two epistemologies of synthesis —
  **parametric** (FM, wavetable, physical modeling, spectral, DDSP: human-defined parameters,
  *legible but bounded*) vs **learned-representation** (encode a corpus; *expressive but
  implicit*). SSL lives in the second column. Read [`the-pretext-task.md`](the-pretext-task.md):
  the pretext task is *where supervision comes from*; the target is *what gets encoded*.
- **0.2** **Recap the move you already know.** BERT masks a token and predicts it; the embedding
  you reuse is an **intermediate activation**, not the prediction head. SSL on audio is *that
  move on a waveform*. If masked-prediction / "an embedding is a kept activation" is shaky,
  rebuild it here — it is the object every later phase varies.
- **0.3** **Recap the audio front-end (light).** Waveform → CNN feature encoder → ~20 ms latent
  frames; mel/STFT and a neural codec (EnCodec/RVQ) by name (from `audio-codecs/`). Just enough
  that "a frame sequence" and "EnCodec tokens" are concrete — Phase 5 needs EnCodec as a
  *teacher*.
- **0.4** **Tools.** `torch` + Hugging Face `transformers`; load a **pretrained** SSL model
  (MERT-95M-public, or `wav2vec2-base` / `hubert-base`), feed the **shared piano clip**, and pull
  out **per-layer hidden states** (`output_hidden_states=True`). Confirm you can get a
  `[layers × frames × dim]` tensor — the object every probe reads.
- **0.5** **The qubit.** The piano clip through an SSL encoder; the recurring picture is the
  **mask-and-predict** diagram and the **layer-wise linear probe**. Why a *pretrained* model
  leads: training one of these costs thousands of GPU-hours — we *use* the representation and
  interrogate it.

## Phase 1 — What "Self-Supervised" Even Means
- **1.1** **Three regimes.** **Supervised** (human labels) / **unsupervised** (no targets) /
  **self-supervised** (a target *fabricated from the input*). SSL's "label" is the data you hid.
  This is what lets it consume the **ocean of unlabeled audio** — the whole reason it exists.
- **1.2** **The pretext task.** Mask a span of the signal (or its latent frames) and predict it.
  The supervision is free and infinite. Contrast **what** is predicted — that choice (the
  *target*) is Phase 4's keystone.
- **1.3** **The representation is the kept middle.** You train the pretext head, then **throw it
  away** and keep the Transformer's **intermediate activations** as the representation. Drive
  this home now — half the misreadings come from confusing the pretext output with the product.
- **1.4** **SSL is not an autoencoder.** A neural codec / autoencoder (`audio-codecs/`) is trained
  to **reconstruct the waveform** — invertible by construction. An SSL encoder is trained to
  **predict a target** — *not* invertible. Flag this bright line on day one; it is half of the
  Phase 7 payoff.

## Phase 2 — The Contrastive Branch: wav2vec 2.0 (2020)
- **2.1** **The architecture.** Waveform → **CNN feature encoder** → latent frames → **mask**
  spans → **Transformer context network**. Targets live at the masked positions.
- **2.2** **The contrastive objective (InfoNCE).** For each masked step, the context vector must
  pick the **true quantized latent** out of a set of **distractors** (other masked steps).
  Contrastive, not reconstructive — pull the true pair together, push distractors away.
- **2.3** **The learned product quantizer.** A **Gumbel-softmax product quantizer** learns the
  discrete codebook **jointly** with the encoder (the contrastive target is *itself* learned); a
  **diversity loss** keeps codebook usage high so it doesn't collapse.
- **2.4** **Why it mattered.** Pre-train on 53k h unlabeled + fine-tune on tiny labeled sets:
  **10 minutes** of labels → ~4.8/8.2 WER on LibriSpeech — ~100× label efficiency. The result
  that made audio SSL a paradigm. *(What it encodes: phonetic, speech-flavored — not music,
  not invertible.)*

## Phase 3 — The Predictive / MLM Branch: HuBERT (2021)
- **3.1** **The swap.** Replace wav2vec2's contrastive task with **BERT-style masked prediction
  of discrete cluster IDs** ("hidden units") — a **classification** loss at masked positions
  only. Closer to BERT than to wav2vec2.
- **3.2** **Consistency over correctness (the clever part).** The targets come from **offline
  k-means** on features — start crude (e.g. 100 clusters on MFCCs), train, then **re-cluster on
  the model's *own* learned features** and repeat. **Two iterations suffice.** It works because
  the cluster *assignment is consistent*, not because it's "right" — a key, counterintuitive
  point.
- **3.3** **Results.** Matches/beats wav2vec 2.0 on LibriSpeech; a 1B model gives up to ~19%/13%
  relative WER reduction on hard sets. Its masked-discrete-target recipe is **exactly what MERT
  lifts into music** (Phase 5).
- **3.4** **The two-branch split.** **Contrastive** (wav2vec2: InfoNCE vs distractors) vs
  **predictive/MLM** (HuBERT: classify cluster IDs). Both discard the head and keep the middle;
  the music-understanding and resynthesis-conditioning encoders descend from the **predictive**
  branch. Name the split; don't let the learner blur the two.

## Phase 4 — The Target Shapes the Representation (keystone)
> Spend as long as it takes. This is *what gets encoded, and why*. Re-read [`the-pretext-task.md`](the-pretext-task.md).
- **4.1** **The thesis.** The network encodes **whatever its prediction target rewards.** k-means
  on MFCCs → phonetic features; a richer target → richer features. The representation is a
  **shadow of its teacher** — the single most useful sentence in the course.
- **4.2** **Variations on the target.** **data2vec** — predict your *own* latent representation
  (self-distillation, an EMA teacher), one recipe across speech/vision/text. **w2v-BERT** — a
  wav2vec2 + BERT hybrid; *this is where AudioLM's **semantic tokens** come from* (so "semantic
  tokens" are an SSL product, not a separate species).
- **4.3** **The target can be almost anything (BEST-RQ).** A **frozen random-projection
  quantizer** as the target — no learned codebook, no teacher network — still trains a strong
  encoder. The lesson: what matters is a **consistent target to predict against**, not a
  "correct" one. The strongest evidence for the thesis.
- **4.4** **The corollary to carry into Phase 7.** Nothing in any of these targets asks for
  **invertibility** or **factor-disentanglement**. So we should *expect* the representation to be
  neither — and Phase 7 confirms it. State this as a prediction now.

## Phase 5 — Self-Supervised Learning for Music: MERT (2023)
- **5.1** **"HuBERT for music."** Same masked-prediction MLM recipe (Phase 3), but the speech
  teachers are replaced by a **music-tailored teacher pair**. SOTA across **14 MIR tasks** at
  only **95M–330M params** — including pitch detection, beat tracking, source separation, key,
  genre, tagging, emotion.
- **5.2** **The two teachers (the design that makes it *music*).** **Acoustic teacher:
  EnCodec RVQ-VAE** (8-codebook, 24 kHz) → discrete acoustic pseudo-labels (timbre/quality).
  **Musical teacher: Constant-Q Transform (CQT)** reconstruction → a **pitch/harmonic inductive
  bias**, the piece speech SSL lacks and music needs. *Two targets → a representation that is a
  shadow of both* (keystone, made concrete).
- **5.3** **Layer specialization.** Different Transformer layers specialize — **low = local
  acoustic, high = musical/structural.** This is *the* practical fact for conditioning a
  generator: you choose **which layer** to read depending on whether you want timbre or
  structure. It is also the precise sense in which MERT is **entangled by layer, not by named
  factor** (carry to Phase 7.2).
- **5.4** **Scaling and the public checkpoint.** A handful of **stability tricks** (Pre-LN over
  Post-LN, attention-relax) let acoustic SSL scale to 330M without gradient blow-ups; a
  copyright-clean **MERT-95M-public** is released — the model the capstone uses. *(History in one
  line: speech SSL 2020–21 → music SSL 2023; MERT is the open, efficient successor to JukeMIR /
  Jukebox probes.)*

## Phase 6 — Reading the Representation: Probing & Evaluation
- **6.1** **Linear probing — the basic diagnostic.** **Freeze** the SSL model; train a **linear**
  classifier/regressor on its frozen features for a task (pitch, instrument, genre). Linear on
  purpose: it measures what the representation made **linearly available**, not what a deep head
  can extract. This course's **oracle**.
- **6.2** **The layer-specialization curve.** Probe **each layer** and plot accuracy vs depth.
  Pitch peaks low/mid; genre/structure peaks high (Phase 5.3, *seen*). The recurring picture —
  run it today on the piano clip + a small labeled set.
- **6.3** **Why one number can't settle it (teach the skepticism).** A probe score depends on the
  **task** and the **probe's capacity**; "best representation" is **task-relative** — MERT may win
  MIR while a speech model wins phonetics. Report **several tasks/layers**, never a single
  headline number. *(The methodological sibling of disentanglement's "metrics disagree.")*
- **6.4** **Benchmarks in the wild.** MARBLE / the MIR task suite by name — tagging, key, beat,
  pitch, emotion, segmentation. How "general-purpose representation" is *operationalized* as a
  battery of frozen-feature probes, and the eval challenges that come with no ground-truth
  "meaning."

## Phase 7 — The Gap to Resynthesis (keystone)
> Spend as long as it takes. This is *why an understanding-grade representation isn't enough* — the second half.
- **7.1** **Not invertible.** SSL features are optimized to **predict a target**, not to
  **reconstruct audio** — there is no decoder, and the features don't cleanly invert. To
  *resynthesize* you must **add** one: a **RAVE**-style β-VAE-plus-adversarial decoder (real-time,
  48 kHz; timbre transfer by decoding a source latent through a target decoder), or — the modern
  move — a **rectified-flow diffusion transformer** ([`audio-diffusion-dit/`](../audio-diffusion-dit/))
  **conditioned on** the SSL features, sampling coherent variations around the source.
- **7.2** **Not disentangled.** MERT entangles **by layer**, not by **named factor**; nothing
  separates **room acoustics / signal chain / performer articulation** from the underlying
  **composition**. Naming and aligning those factors needs an **inductive bias** — exactly
  [`disentanglement/`](../disentanglement/)'s lesson (its Phase 8.4 *open frontier*, here from the
  encoder side). β-VAE's knob (in RAVE) buys *less-entangled* dimensions but does **not** name
  them.
- **7.3** **The resynthesis stack, assembled.** **(1)** a self-supervised representation that
  "implicitly captures the full complexity of a recording" (this course); **(2)** a generative
  decoder over it — a **rectified-flow DiT** ([`flow-matching/`](../flow-matching/) +
  [`audio-diffusion-dit/`](../audio-diffusion-dit/)); **(3)** an inductive bias that
  **disentangles** attributes from composition ([`disentanglement/`](../disentanglement/)). The
  **neural-audio-resynthesis** paradigm is exactly this assembly — and **(3)** is the unsolved part.
- **7.4** **The frontier, named.** **Self-supervised, decodable, attribute-disentangled**
  representations of **full recordings** — the encoder side this course can take you to, the
  decoder side that is mature, and the disentanglement side that is **open**. Hand-off: the
  capstone meta-course [`neural-audio-resynthesis/`](../neural-audio-resynthesis/) ties the three
  strands together and surveys the load-bearing survivors.
- **7.5** **Capstone — extract, probe, and try to invert.** Tiered a/b/c, **no GPU required for
  (a)** (pretrained inference + linear probes are cheap):
  - **(a) CPU / default.** Load **MERT-95M-public** (or `wav2vec2-base`/`hubert-base`); extract
    **per-layer** features for the **piano clip** + a small labeled set (a NSynth pitch/instrument
    subset, or a few GTZAN genre clips). Train **linear probes per layer**; plot the
    **layer-specialization curve**; write a one-page report — *what does this representation
    encode, and where?*
  - **(b) Colab GPU.** Compare a **contrastive** encoder (`wav2vec2`) against a **predictive** one
    (`hubert`/`MERT`) on the *same* probes — watch the target-family difference; add tasks (beat,
    key); sanity-check the **BEST-RQ** intuition (a random-projection target still probes well).
  - **(c) Local GPU / resynthesis bridge.** Attach a small **decoder head** to *frozen* SSL
    features (or condition a tiny RAVE/flow decoder) and **try to invert to audio** — **listen**
    to how much is recoverable. The "understanding ≠ invertible" lesson made audible, and the
    on-ramp to [`neural-audio-resynthesis/`](../neural-audio-resynthesis/).

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If shaky,
   re-teach before continuing.
2. **Introduce one new concept** with a picture *before* notation. The recurring picture is the
   **mask-and-predict** diagram and the **layer-wise linear probe**
   ([`the-pretext-task.md`](the-pretext-task.md)): hide a span, predict the target, keep the
   middle, then probe each layer. Draw on it constantly.
3. **Pin it to the clip.** Extract features from the **shared piano clip** and probe them. The
   **probe accuracy** (a number, per layer) is this course's oracle — and for the resynthesis
   payoff, the **ear** (invert and listen).
4. **Tiny exercise** to verify: predict a probe curve ("which layer best predicts pitch — low or
   high?"), state the difference between InfoNCE and cluster-ID prediction, or run a few lines
   that pull `hidden_states` and fit a linear probe. The exercise *is* the check.
5. **Common misreadings** when relevant — keep [`the-pretext-task.md`](the-pretext-task.md)'s list
   live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to `progress.md` and the
   day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences ("SSL fabricates a target from the data; the
   representation is whatever predicting that target rewards — so it's understanding-grade, not
   invertible or disentangled").
2. Carry out the small task: pull per-layer `hidden_states`, fit a linear probe, read a
   specialization curve, or contrast InfoNCE with cluster-ID prediction — and explain it.
3. Spot a deliberately wrong claim ("SSL is unsupervised" — no, it *manufactures* a target;
   "MERT features are disentangled" — no, entangled by layer, not by named factor; "higher probe
   accuracy = strictly better representation" — no, it's task- and capacity-relative).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wiki this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays canonical,
the course stays pedagogical. Read / link these on JOS's machine:

- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — the home wiki. Concept page:
  **`concepts/self-supervised-audio-representations.md`** (the two epistemologies, the
  representation→decoder→generator stack, and the disentanglement frontier — this course's
  spine). Source summaries: **`sources/speech-ssl-foundations.md`** (the speech-SSL ladder —
  wav2vec 2.0 → HuBERT → w2v-BERT → data2vec → BEST-RQ; the canonical backing for Phases 2–4),
  **`sources/mert.md`** (HuBERT-for-music), `sources/rave.md` (the invertible β-VAE counterpoint),
  `sources/audiolm.md` (w2v-BERT semantic tokens), `sources/fluxmusic.md` / `sources/dit.md`
  (the rectified-flow DiT decoder).
- **`/w/music423-2023/ai-audio-codecs/wiki/`** — for the **EnCodec** teacher (Phase 5.2) and the
  autoencoder-vs-SSL contrast (Phase 1.4): `sources/encodec.md`, `overview.md`.
- **`/w/music423-2023/disentanglement/wiki/`** — for Phase 7.2: `audio-disentanglement.md`,
  `overview.md` (the impossibility result and why factor-naming needs an inductive bias).
- Keep the course in sync if the wiki gains papers; the wiki is canonical, the course is the
  lesson plan over it.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line history
*when it helps*, and otherwise teach from the mask-and-predict picture and the probe.

### Source papers (the lineage this course tracks)
- **Baevski et al. (2020)** — *wav2vec 2.0: A Framework for Self-Supervised Learning of Speech
  Representations*. NeurIPS 2020. arXiv:2006.11477.
- **Hsu et al. (2021)** — *HuBERT: Self-Supervised Speech Representation Learning by Masked
  Prediction of Hidden Units*. IEEE/ACM TASLP. arXiv:2106.07447.
- **Li, Yuan, Zhang, Ma et al. (2023)** — *MERT: Acoustic Music Understanding Model with
  Large-Scale Self-Supervised Training*. ICLR 2024. arXiv:2306.00107.
- *Extensions (named in Phase 4, optional depth):* **data2vec** (Baevski et al. 2022,
  arXiv:2202.03555); **w2v-BERT** (Chung et al. 2021, arXiv:2108.06209 — AudioLM's semantic-token
  encoder); **BEST-RQ** (Chiu et al. 2022, arXiv:2202.01855 — random-projection target).
- *The invertible counterpoint (Phase 7.1):* **RAVE** (Caillon & Esling 2021, arXiv:2111.05011).
