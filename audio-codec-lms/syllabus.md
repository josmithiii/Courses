# Audio Codec Language Models — Generating Audio by Predicting Tokens

**Learner profile:** Has finished `audio-codecs/` (course 1 of this curriculum) — so
they know how a neural codec turns audio into a **codebook × frame grid of discrete
RVQ tokens**, what the discrete-vs-continuous **fork** is, and they've encoded and
heard the through-line clip. They arrive from `ai-foundations/` with Transformers and
LLMs already in hand. This course is the **left branch of the fork**: take those
tokens and *language-model* them. ML-first; no new DSP. ~1 hour per day, one concept
at a time, every concept checked with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisite:** `audio-codecs/` (the discrete-token branch of its fork is this
course's starting line). If a learner skipped it, spend Phase 0 reconstructing "what a
codec token *is*" before going on — nothing here makes sense without the token grid.

**The keystone — read [`the-token-grid.md`](the-token-grid.md) in Phase 0.1.** This
course has one organizing object, the analogue of course 1's fork: the **RVQ token
grid** (K codebooks × T frames) and the one question that organizes the whole field —
***how do you model K parallel token streams over T time steps?*** Every system here
is a different answer: a **hierarchical cascade** (AudioLM/MusicLM), a **codebook
pattern** in a single model (MusicGen flat/delay; Stack-and-Delay), or **masked
parallel** decoding (VampNet/MAGNeT). Plus AudioLM's **semantic→acoustic** split for
long-range coherence. We spend as long as it takes on Phases 3 and 5.

**The qubit (worked example):** the curriculum's shared **~2-second solo-piano clip**
(`../curricula/assets/ai-music-audio/through-line.wav`, mono 24 kHz). Course 1 *encoded*
it; here we *generate* from it. Carry its token grid through every paradigm:
**continue** it (autoregressive), **infill / vamp** it (masked), and **condition** a
generation with text. Same clip, three generation modes.

**End state:** by the last lesson the learner can: explain why sample-level AR
(WaveNet/SampleRNN) was too slow and what token-level modeling bought; read an RVQ
token grid and explain the **multi-stream challenge**; explain the **semantic vs
acoustic** token hierarchy and why it buys coherence; explain how **MusicGen** made one
single-stage Transformer enough via **codebook patterns** (flat / delay / stack-delay);
contrast **autoregressive** vs **masked (NAR)** generation and place VampNet/MAGNeT;
explain how text conditioning works (MuLan/CLAP joint embeddings vs T5 cross-attention)
and why it sidesteps paired-data scarcity; explain that **VALLE/MIDI-VALLE are codec-LMs,
not DiTs**; and *run a real codec-LM* (MusicGen/AudioCraft) to generate, continue, and
infill the clip.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture**, and where it sits: course 1 built the
  codec and stopped at the **fork**; this course walks the **discrete-token branch** —
  audio generation = **next-token (or masked-token) prediction over codec tokens**.
  Read [`the-token-grid.md`](the-token-grid.md). The other branch (continuous latent →
  diffusion) is course 3.
- **0.2** **Recap codec tokens (from course 1).** Reload the through-line clip, encode
  it with the same codec, and look hard at the **token grid**: shape `[N_q, T]`,
  what a row (one codebook level) is, what a column (one frame, all levels) is. This
  grid is the object the entire course generates.
- **0.3** **Tools.** `torch` + the codec from course 1, plus (capstone-tier-aware) a
  pretrained generator: `audiocraft` (MusicGen) on CPU for small models, Colab GPU for
  larger. Confirm you can encode→decode the clip round-trip before generating anything.

## Phase 1 — Where It Started: Autoregressive Raw Audio
- **1.1** **The autoregressive idea.** Factorize a sequence as `p(x) = Π p(xₜ | x_<t)`
  and predict one step at a time, left to right. (They know this from LLMs — name it,
  connect it.) Generation = repeated next-step sampling.
- **1.2** **WaveNet (2016).** Dilated causal convolutions model raw audio *sample by
  sample*. Astonishing quality for its day — but at 16–24 kHz, one forward pass *per
  sample* means minutes of compute per second of audio. The lesson: sample-level AR
  works but doesn't scale.
- **1.3** **SampleRNN (2016) & NSynth (2017).** Hierarchical multi-rate RNNs as an
  alternative; NSynth wraps WaveNet in an autoencoder for timbre interpolation (the
  first "latent for control" hint). Same wall: sample-level is too slow, and there's no
  good handle on long-range structure.
- **1.4** **The takeaway that sets up the whole course.** If we first *compress* audio
  to a **short sequence of tokens** (course 1's codec: 24 kHz → ~75 Hz of frames), then
  AR prediction becomes tractable — thousands of tokens, not hundreds of thousands of
  samples. *Tokenize, then language-model.* That is the pivot.

## Phase 2 — Tokens + Transformers: Jukebox
- **2.1** **Jukebox (2020).** A hierarchical **VQ-VAE** compresses raw audio to discrete
  tokens at three resolution levels; **Sparse Transformers** model them
  autoregressively. The first system to generate **multi-minute, multi-instrument music
  with vocals**. The proof of concept for "audio as a token language."
- **2.2** **What worked and what hurt.** Coarse-to-fine hierarchy gave structure;
  enormous compute and occasional long-range drift were the costs. Conditioning was
  coarse — **artist / genre / unaligned lyrics** (preview Phase 4's conditioning thread).
- **2.3** **Pin to the clip.** Sketch the clip as a multi-level token hierarchy
  (coarse tokens = "what notes / structure," fine tokens = "exact timbre"); relate it
  to the RVQ levels the learner saw in course 1.

## Phase 3 — AudioLM & the Semantic→Acoustic Hierarchy (keystone)
> Spend as long as it takes. Re-read [`the-token-grid.md`](the-token-grid.md).
- **3.1** **The coherence problem.** Acoustic codec tokens reconstruct beautifully but,
  modeled alone, wander — they carry little long-range structure. Pure acoustic-token AR
  drifts.
- **3.2** **AudioLM's insight (2022): two kinds of token.** **Semantic** tokens (from a
  self-supervised model, w2v-BERT) capture structure — melody, rhythm, "syntax" — but
  reconstruct poorly. **Acoustic** tokens (from a SoundStream/EnCodec RVQ) capture
  fidelity but lack structure. Use **both**.
- **3.3** **The hierarchical pipeline.** Generate **semantic tokens first** (structure),
  then **acoustic tokens conditioned on the semantics** (fidelity), coarse RVQ levels
  before fine. Why this beats either token type alone — the result is coherent *and*
  high-fidelity (AudioLM's speech continuations fool raters ~half the time; it also does
  coherent piano with no score).
- **3.4** **The classic conflation to kill.** Semantic ≠ acoustic; "semantic tokens" are
  *not* the codec's tokens. Carried over from course 1's misreadings list — make the
  learner state the difference in their own words. *(Also flag the live debate: course 3
  will show long-form diffusion challenging "semantic tokens are **required**.")*
- **3.5** **Pin to the clip.** Map the clip onto the two token types conceptually:
  semantic = "the tune and where it's going," acoustic = "this exact piano sound."

## Phase 4 — Text Conditioning: MusicLM & the Joint-Embedding Trick
- **4.1** **Why text-to-music is hard.** A single caption must steer minutes of evolving
  audio; descriptions are ambiguous; **aligned text–music data is scarce** (much rarer
  than text–image).
- **4.2** **MuLan (MusicLM, 2023): the contrastive bypass.** Train a **joint music–text
  embedding** contrastively; condition on the *audio* embedding at training time (no
  captions needed), substitute the *text* embedding at inference. This trains
  text-to-music on **audio-only** corpora — the key trick. MuLan embeddings act as
  conditioning "semantic" tokens over AudioLM's hierarchy.
- **4.3** **The conditioning menu (survey).** Metadata IDs (Jukebox) → joint embeddings
  (MuLan, CLAP) → **text-encoder cross-attention** (T5/FLAN-T5, as in MusicGen) →
  **melody conditioning** (chromagram) → **LM-as-planner** (ACE-Step — preview, it's a
  course-3 hybrid). Which need paired data, which don't.
- **4.4** **Pin to the clip.** Take a short text tag ("solo piano, gentle, minor key")
  and reason about how each strategy would push generation toward the clip's character.

## Phase 5 — One Model Is Enough: MusicGen & Codebook Patterns (keystone)
> The other half of the keystone. The **multi-stream challenge** made practical.
- **5.1** **The multi-stream challenge, stated.** RVQ gives `N_q` **parallel** token
  streams per frame. A plain LM predicts *one* stream. How do you model `N_q` streams ×
  `T` frames with one Transformer? (The menu lives in `the-token-grid.md`.)
- **5.2** **MusicGen (2023): single-stage with codebook patterns.** *One* Transformer,
  no cascade. The trick is the **pattern** that serializes/aligns the `N_q` streams:
  - **Flat** — all `N_q` tokens of a frame inlined: best quality, ~`N_q`× slower.
  - **Delay** — stream `k` offset by `k` steps: most of the quality, far faster.
  - **Parallel** — predict all streams per step: fastest, lower quality.
  - **The misreading to kill:** *"MusicGen is multi-stage."* It is **single-stage**; the
    cascades were AudioLM/MusicLM. The pattern is what makes one model sufficient.
- **5.3** **Stack-and-Delay (2023).** Group + offset streams to get **near-flat quality
  at near-delay speed** — codebook-pattern engineering as a first-class quality–speed
  dial.
- **5.4** **Text + melody in MusicGen.** T5 text embeddings via cross-attention;
  optional chromagram melody conditioning. Open-sourced as **AudioCraft** — the codec-LM
  the learner will actually run in the capstone.
- **5.5** **Pin to the clip.** Predict, then *hear*: continue the clip with MusicGen;
  compare a delay-pattern vs flat-pattern generation if compute allows.

## Phase 6 — Beyond Autoregression: Masked Token Modeling
- **6.1** **AR's two limits.** Sequential decoding is `O(T)` slow, and left-to-right
  **can't infill** — no editing, no "fill the gap between these two bars."
- **6.2** **Masked / non-autoregressive (NAR) generation.** Borrow **MaskGIT/BERT**:
  start from a fully-masked grid, predict all tokens in parallel, keep the most
  confident, **re-mask and re-predict** over ~10–40 iterations. Bidirectional attention
  sees past *and* future context.
- **6.3** **VampNet (2023): masked acoustic tokens for editing.** Flexible prompting →
  **inpainting, outpainting, "vamping"** (variations). The first natural fit for music
  *co-creation* — fill in the blanks. (Runs on DAC tokens.)
- **6.4** **MAGNeT (2024): NAR done fast.** Span-masking + rescoring → **~7× faster than
  MusicGen**; a **hybrid** mode opens autoregressively (strong intro) then switches to
  masked parallel. SoundStorm is the speech-side cousin (course 1 saw it).
- **6.5** **The misreading to kill:** *"masked NAR generation = diffusion."* Both are
  iterative and non-left-to-right, but masked models predict **discrete tokens** by
  confidence-based unmasking; diffusion denoises **continuous latents** (course 3).
  Different objects, different math.
- **6.6** **Pin to the clip.** **Infill** a middle slice of the clip's token grid
  (VampNet/MAGNeT-style) and listen; contrast with the Phase 5 AR *continuation*.

## Phase 7 — Codec-LMs Beyond Music: VALLE → MIDI-VALLE
- **7.1** **The recipe travels.** The codec-LM machinery was born in **speech**: **VALLE**
  (zero-shot TTS) language-models EnCodec tokens with an **AR + NAR over RVQ** design —
  exactly AudioLM's shape. The same idea keeps migrating between speech and music.
- **7.2** **MIDI-VALLE (2025): expressive performance synthesis.** Render *performance
  MIDI* → expressive piano audio by swapping VALLE's **text prompt → MIDI prompt** and
  **speaker prompt → 3-second reference-audio style prompt**. Both MIDI (Octuple + IOI)
  and audio (a Piano-EnCodec RVQ) become **discrete tokens**; the AR+NAR-over-RVQ
  backbone is unchanged. Cuts FAD >75% vs the M2A baseline on classical piano; weaker on
  jazz; needs tight MIDI↔audio alignment.
- **7.3** **The headline misreading to kill:** *"MIDI-VALLE / VALLE are DiTs."* They are
  **codec language models** (the VALLE lineage) — discrete tokens, next/masked-token
  prediction. *Not* a diffusion transformer over a continuous latent. This is the cleanest
  test of whether the **fork** truly landed: same task (audio from a condition), opposite
  branch from course 3. Our through-line clip is *solo piano* — MIDI-VALLE's home turf —
  so this lands concretely.

## Phase 8 — Putting It Together
- **8.1** **The map.** Lay out the codec-LM family on two axes: **conditioning** (none /
  audio-prompt / metadata / joint-embedding / text-encoder / MIDI) × **decoding**
  (AR-flat / AR-delay / stack-delay / masked-NAR / hybrid). Place WaveNet, Jukebox,
  AudioLM, MusicLM, MusicGen, VampNet, MAGNeT, VALLE, MIDI-VALLE. Recite which token
  grid each models and how.
- **8.2** **Capstone — run a real codec-LM on the clip.** Tiered like room-acoustics'
  a/b/c, no GPU required:
  - **(a) CPU / pretrained inference (default).** `pip install audiocraft`; load the
    smallest **MusicGen**. **Generate** from a text prompt; **continue** the through-line
    clip (audio prompt); inspect the generated **token grid** and decode. Write a
    one-page "codec-LM report."
  - **(b) Colab GPU.** Larger MusicGen; add a **VampNet/MAGNeT-style infill** of the
    clip's middle; A/B **delay vs flat** patterns; try **melody (chromagram)**
    conditioning toward the clip.
  - **(c) Local GPU.** Additionally fine-tune or prompt-engineer toward the clip's
    style, or run **MIDI-VALLE** on a performance-MIDI rendering of the clip to *hear*
    the codec-LM-vs-DiT distinction before course 3.
- **8.3** **Where to go next.** You can now read AudioLM, MusicGen, VampNet, MAGNeT, and
  VALLE/MIDI-VALLE. The **other branch of the fork** is course 3
  (`audio-diffusion-dit`): same clip, *continuous* latent, *denoised* instead of
  predicted — with `flow-matching/` as enrichment.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. The
   recurring picture here is the **token grid** (`N_q` rows × `T` columns) — draw on it
   constantly: AR fills it column-by-column, masked fills it by confidence, patterns
   re-order how columns are read.
3. **Pin it to the clip.** The clip's token grid is the worked example. Generate from it
   — continue, infill, condition — and **listen**. The ear is this course's oracle; a
   decoded generation beats a diagram.
4. **Tiny exercise** to verify: predict the next concept's behavior ("delay pattern vs
   flat — which is faster, which is better, why?"), trace a few tokens through a pattern,
   or run a few lines of `audiocraft`. The exercise *is* the check.
5. **Common misreadings** when relevant — keep [`the-token-grid.md`](the-token-grid.md)'s
   list live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences ("MusicGen is single-stage; a codebook pattern
   serializes the `N_q` RVQ streams so one Transformer suffices").
2. Carry out the small task: trace tokens through a pattern, run `audiocraft` to
   continue/infill the clip, or place a system on the conditioning×decoding map — and
   explain it.
3. Spot a deliberately wrong claim ("MIDI-VALLE is a DiT" — no, it's a codec-LM;
   "MusicGen is multi-stage" — no, single-stage with patterns).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wiki this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Read / link these on JOS's machine:

- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — the home wiki (codec-LM half).
  Concept pages: `concepts/generation-paradigms.md` (AR vs masked vs diffusion),
  `concepts/codec-based-generation.md` (the two-stage pipeline + multi-stream table),
  `concepts/text-to-music-conditioning.md`. Source summaries: `wavenet`, `samplernn`,
  `nsynth`, `jukebox`, `audiolm`, `musiclm`, `musicgen`, `vampnet`, `stack-and-delay`,
  `magnet`, `midi-valle` (and `overview.md` for the arc).
- **`/w/music423-2023/ai-audio-codecs/wiki/`** — course 1's wiki, for codec/token recall
  (SoundStream, EnCodec, DAC, SoundStorm).
- Keep the course in sync if the wiki gains papers; the wiki is canonical, the course is
  the lesson plan over it.

### Source papers (the codec-LMs this course tracks)
- **van den Oord et al. (2016)** — *WaveNet*. arXiv:1609.03499.
- **Mehri et al. (2016)** — *SampleRNN*. arXiv:1612.07837.
- **Dhariwal et al. (2020)** — *Jukebox*. arXiv:2005.00341.
- **Borsos et al. (2022)** — *AudioLM*. arXiv:2209.03143.
- **Agostinelli et al. (2023)** — *MusicLM*. arXiv:2301.11325.
- **Copet et al. (2023)** — *MusicGen / Simple and Controllable Music Generation*
  (AudioCraft). arXiv:2306.05284.
- **Garcia et al. (2023)** — *VampNet*. arXiv:2307.04686.
- **Ziv et al. (2024)** — *MAGNeT (Masked Audio Generation)*. arXiv:2401.04577.
- **Wang et al. (2023)** — *VALL-E (Neural Codec Language Models are Zero-Shot TTS)*.
  arXiv:2301.02111.
- **MIDI-VALLE (2025)** — expressive piano performance synthesis (QMUL/NII, ISMIR 2025).
