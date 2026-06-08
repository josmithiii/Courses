# The Pretext Task & the Target — This Course's Keystone

Room-acoustics has the Schroeder frequency; flow-matching has the conditional-expectation
identity; disentanglement has the TC decomposition & the impossibility. **This course has two
halves of one keystone**, and you need both:

1. **The pretext task** — *where the supervision comes from.* There are no labels and no
   waveform-reconstruction loss. You **manufacture** supervision from the unlabeled audio
   itself: hide part of the signal and predict it (or contrast the true continuation against
   distractors) in a **learned latent space**. What you keep is the **intermediate
   representation**, never the pretext output.
2. **The target shapes the representation** — *what you end up encoding.* The model learns
   exactly what its **prediction target (the "teacher")** rewards. Change the teacher and you
   change the representation. The corollary that lands this whole curriculum:
   **understanding ≠ invertible.** A representation tuned to *predict its target* is not
   automatically **decodable** back to audio, nor **disentangled** into named factors.

Put them together and the field collapses to one sentence:

> **Self-supervised audio learning trains a network to predict a target it built from the data
> itself; the representation it grows is a *shadow of that target* — so a representation that is
> excellent at music understanding is not, by that fact, either invertible to audio or
> disentangled into room / channel / performer / composition. Resynthesis must add both on top.**

Read this in Phase 0.1, then return to it in **Phase 4** (the target *is* the representation —
spend as long as it takes), **Phase 6** (probing — how we read what the target left behind),
and **Phase 7** (the gap to resynthesis — invertibility and disentanglement, both missing).
Every term in **bold** is earned somewhere in the syllabus; the phase is in brackets.

---

## The recurring picture: mask, predict, and keep the middle

```
   waveform ──CNN feature encoder──▶  z₁ z₂ z₃ z₄ z₅ z₆ …    (latent frames) [Phase 2.1]
                                          │  ╲   ╱
                              MASK a span ▼   ✗ ✗            (hide z₃, z₄) [Phase 1.2]
                                      ┌─────────────────┐
                                      │   Transformer   │     ← THIS stack's activations
                                      │  context network│        are the REPRESENTATION
                                      └─────────────────┘        we keep [Phase 1.3]
                                          │
                  predict the TARGET at the masked positions only:
                     • wav2vec 2.0 — CONTRAST true quantized latent vs distractors (InfoNCE) [Phase 2]
                     • HuBERT      — CLASSIFY into k-means cluster IDs (masked prediction) [Phase 3]
                     • MERT        — predict EnCodec tokens (acoustic) + CQT (pitch) [Phase 5]
                                          │
                       ──── the pretext HEAD is thrown away [Phase 1.3] ────
```

The course's oracle is the **linear probe** [Phase 6] — freeze the network, train a *linear*
readout on its frozen features, and the accuracy tells you *what the representation made
linearly available*. Run it **layer by layer** and you get the **specialization curve** (low
layers acoustic, high layers musical) [Phase 5.3, 6.2]. For the resynthesis payoff, the oracle
becomes the **ear**: attach a decoder and listen to how much of the audio is actually
recoverable [Phase 7].

---

## Half 1 — the pretext task: supervision manufactured from the data [Phases 1–3]

There is a clean three-way split the learner must hold from day one [Phase 1.1]:

- **Supervised** — human labels (transcripts, instrument tags).
- **Unsupervised** — no targets at all (clustering, density estimation).
- **Self-supervised** — *no human labels, but a target the model fabricates from the input.*
  Mask a span and predict it; the "label" is the data you hid. This is why it scales to the
  ocean of **unlabeled** audio.

Two branches manufacture that target differently — **this is the structural split of the
field** [Phase 3.4]:

```
  CONTRASTIVE (wav2vec 2.0, 2020) [Phase 2]      PREDICTIVE / MLM (HuBERT, 2021) [Phase 3]
  ───────────────────────────────────────       ──────────────────────────────────────────
  mask latent spans; for each masked step,       offline k-means → a cluster ID per frame
  pick the TRUE quantized latent out of a         (the "hidden unit"); mask spans; CLASSIFY
  set of distractors  →  InfoNCE loss             the masked frames into their cluster IDs
  a Gumbel-softmax product quantizer learns       relies on CONSISTENCY, not label quality:
  the codebook JOINTLY; a diversity loss          crude k-means → re-cluster on the model's
  keeps codebook usage high                       OWN features → repeat (2 iters suffice)
```

Both work; both throw away the pretext head and keep the Transformer's activations. The
contrastive-vs-predictive distinction is real (different objective, different failure modes)
but secondary to Half 2: *whatever* the branch, the representation is governed by **what you
ask it to predict.**

## Half 2 — the target shapes the representation [Phase 4], and isn't invertible [Phase 7]

Here is the twist that organizes everything. **The model encodes whatever its target
rewards** [Phase 4.1]:

- k-means on **MFCCs** → a phonetic, speech-recognition-flavored representation (wav2vec2/HuBERT
  target speech; their features are **not invertible** and carry **no pitch/harmony bias**).
- **EnCodec** acoustic tokens as the target → timbre/quality is captured (MERT's acoustic
  teacher).
- A **CQT** reconstruction target → a **pitch/harmonic inductive bias** is injected — the piece
  speech SSL lacks and music needs (MERT's musical teacher) [Phase 5.2].
- Even a **frozen random** projection can be the target (**BEST-RQ**) and still work — proof
  that what matters is a *consistent* target to predict against, not a "correct" one [Phase 4.3].

So the representation is a **shadow of its teacher.** And two properties the resynthesis
paradigm *needs* are exactly the ones the pretext objective does **not** deliver [Phase 7]:

- **Invertibility.** SSL features are optimized to *predict*, not to *reconstruct* — they are
  **not directly decodable to audio.** (This is the bright line between an SSL encoder and an
  autoencoder / neural codec, which *is* trained to invert. [Phase 1.4]) To resynthesize you
  must add a decoder — a **RAVE**-style adversarial decoder, or a **rectified-flow DiT**
  conditioned on the features.
- **Disentanglement.** MERT entangles attributes **by layer** (low = acoustic, high = musical),
  **not** by named factor — it does not separate room / channel / performer from composition.
  Naming and aligning those factors is the open problem the dedicated
  [`disentanglement/`](../disentanglement/) course studies (its Phase 8.4 frontier, seen here
  from the encoder side).

That gap — *understanding-grade representation in hand, decodable + disentangled
representation wanted* — **is** the neural-audio-resynthesis problem [Phase 7.4].

---

## The misreadings this course exists to kill

Curated from the `ai-music-audio-gen/` wiki. The tutor flags each on the spot and logs
recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "Self-supervised = unsupervised." | SSL **manufactures** a target from the data (the pretext task). There *is* supervision — just no *human* label. | Phase 1.1 |
| "The pretext task is the goal." | The pretext head is **discarded**; the **intermediate representation** is the product. You never use the cluster-ID predictor again. | Phase 1.3 |
| "SSL reconstructs the audio, like an autoencoder / codec." | It predicts in **target/latent space**, not waveform space. SSL features are **not invertible to audio** — the opposite design choice from a codec. | Phase 1.4, 7.1 |
| "wav2vec 2.0 and HuBERT are basically the same model." | **Contrastive** (InfoNCE vs distractors) vs **predictive MLM** (classify into cluster IDs) — different objective, different failure modes. The two-branch split. | Phase 2–3 |
| "HuBERT needs a *good* teacher." | It relies on **consistency, not correctness** — a crude k-means bootstraps, then you re-cluster on the model's own features. | Phase 3.2 |
| "A higher linear-probe number means a better representation." | Probe accuracy depends on the **task and the probe's capacity**; a representation is good only **relative to** a downstream use. Report several. | Phase 6.3 |
| "MERT / SSL features are disentangled." | They entangle **by layer**, not by **named factor**; SSL alone gives no room / channel / performer / composition split. | Phase 5.3, 7.2 |
| "Semantic tokens (AudioLM) are a separate thing from SSL." | AudioLM's semantic tokens **come from w2v-BERT**, an SSL model — same family, same pretext lineage. | Phase 4.2 |

---

## How the course earns the keystone

| Piece | Earned in |
|---|---|
| supervised vs unsupervised vs **self-supervised**; the pretext task; representation = kept middle | **Phase 1** |
| the **contrastive** branch (wav2vec 2.0): InfoNCE, learned product quantizer | **Phase 2** |
| the **predictive / MLM** branch (HuBERT): cluster-ID targets, consistency over correctness | **Phase 3** |
| **the target shapes the representation** (data2vec, w2v-BERT, BEST-RQ) | **Phase 4** (keystone) |
| SSL for **music** (MERT): EnCodec + CQT teachers, layer specialization | **Phase 5** |
| **probing & evaluation**: linear probes, the specialization curve, why one number isn't enough | **Phase 6** |
| **the gap to resynthesis**: not invertible, not disentangled — RAVE & the DiT decoder | **Phase 7** (keystone) |
