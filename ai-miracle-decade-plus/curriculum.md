# AI Miracle Decade Plus — Curriculum

**Live orientation page:** <https://josmithiii.github.io/ai-miracle-decade-plus/>
— a one-screen visual overview of the 12 phases with every paper linked.

A self-paced traversal of 40 landmark AI papers from 2006 → 2023. Read every
"miracle decade" landmark in roughly the order the field experienced it, with
cross-cutting concept-page stops that connect papers across lineages.

**Learner profile:** comfortable reader, technical (engineering / science /
DSP / hobbyist), wants to read the actual papers rather than secondhand
summaries. Math is welcomed but explained when load-bearing. No assumed
PyTorch fluency — runnable bits are optional sidecars.

**Where the papers live.** PDF links below point to **arXiv abstract pages**
when available (which give you the PDF, HTML, BibTeX, and v-history in one
place) and to the original publisher otherwise (OpenAI's CDN for GPT-1/2,
Nature for AlphaGo / AlphaFold 2 / DQN, JMLR for Dropout, NeurIPS for
AlexNet, Hinton's lab page for DBN). Cross-cutting **concept pages** live
in JOS's `music423-2023` repo and are linked via the public CCRMA GitLab
mirror — read them in-browser or save offline; there's nothing to install.

## Pace philosophy — read this first

- **No time constraints.** Topic numbers are *stops*, not days. Spend an
  hour on one or three weeks on another — both are fine.
- **Side quests are encouraged.** When a paper hooks you, follow your
  curiosity: read citing work, watch a Karpathy/3Blue1Brown lecture, run a
  small model, dig through references. Tell the tutor; it gets logged as a
  side-quest so you (and the tutor) remember why you detoured and can
  return intact.
- **The roadmap pulls you back.** The tutor's job is to make sure that
  however long the side quests last, you eventually return to the main
  spine and don't quietly skip a landmark. `progress.md` is the ground
  truth for "what's the next required stop."
- **Reading order is suggested, not enforced.** Skip ahead if a stop is
  already familiar — but mark it `[~] skimmed (known)` in `progress.md`
  rather than `[x] completed` so the tutor knows it can be revisited.

## What each "stop" looks like

A stop on the main spine is usually one paper plus its concept-page context.
A typical session covers:

1. **Frame.** Why this paper, what came before, what tension it tried to
   resolve. (Tutor talks, ~5–10 min.)
2. **Read.** The learner reads the paper (or the relevant section). Default
   to arXiv's HTML view for fast skimming, the PDF for serious reading.
   If you want a text dump for grep/notes,
   `curl -O https://arxiv.org/pdf/<arxiv-id>.pdf && pdf2txt.py <id>.pdf > /tmp/paper.txt`.
3. **Discuss.** Tutor asks one or two checking questions — not a quiz,
   more "what surprised you?" / "what's the load-bearing claim?"
4. **Place.** Tutor situates the paper on its concept-page thread
   (e.g. *pretrain-finetune-lineage*, *scaling-and-emergence*).
5. **Optional do.** A small exercise, a runnable demo (Hugging Face
   `transformers` is the easy on-ramp), or a "what's dead / what's alive"
   prompt — whichever the learner picks.
6. **Log.** Mastery note + open questions → `progress.md`; full record →
   today's lesson file.

## The route

Each phase ends with a **concept-page stop** — a cross-cutting essay from
the [`ai-2012-to-2023` meta-wiki](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/index.md)
that ties the phase's papers together. Read these as lecture-ready essays;
they're the seams the roadmap is built around.

---

### Phase 0 — Orientation & on-ramp

- **0.1** The 17-year arc in one sitting. Read
  [the meta-wiki overview](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/overview.md)
  and [the chronological README](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/README.md).
- **0.2** How to read an AI paper without drowning. Three-pass strategy
  (skim → structure → detail); when figures and equations matter; when to
  defer to a topic-wiki summary first.
- **0.3** Tools: arXiv's per-paper HTML view, `curl` + `pdf2txt.py` for
  text dumps, a Hugging Face account for the optional runnable sidecars.
  Optional: PyTorch + a Jupyter scratchpad.

### Phase 1 — The restart and the cash-out (2006 → 2012)

- **1.1** [DBN — Hinton, Osindero, Teh 2006](https://www.cs.toronto.edu/~hinton/absps/fastnc.pdf).
  Layer-wise unsupervised pretraining. Read alongside the landmark
  ["what's dead / what's alive" note](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/notes/dbn.md).
- **1.2** [AlexNet — Krizhevsky, Sutskever, Hinton 2012](https://papers.nips.cc/paper_files/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html).
  GPUs + ImageNet + ReLU + dropout = the cash-out.
- **★ Concept stop:**
  [pretrain-finetune-lineage](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/pretrain-finetune-lineage.md)
  (first half — DBN's 12-year dormancy before BERT and GPT-1).

### Phase 2 — The machinery years (2013 → 2015)

These "training tools + generative scaffolding" papers are what made
deep learning industrially reliable. Order is flexible inside the phase.

- **2.1** [word2vec — Mikolov et al. 2013](https://arxiv.org/abs/1301.3781).
  Geometry encodes meaning.
- **2.2** [VAE — Kingma & Welling 2013](https://arxiv.org/abs/1312.6114).
  Variational lower bound; latent generative models.
- **2.3** [GANs — Goodfellow et al. 2014](https://arxiv.org/abs/1406.2661).
  Adversarial two-player training.
- **2.4** [Seq2Seq — Sutskever, Vinyals, Le 2014](https://arxiv.org/abs/1409.3215).
  Encoder–decoder pattern.
- **2.5** [Adam — Kingma & Ba 2014](https://arxiv.org/abs/1412.6980).
  Adaptive moments; today's default optimizer.
- **2.6** [Batch Normalization — Ioffe & Szegedy 2015](https://arxiv.org/abs/1502.03167).
  Internal covariate shift; making deep nets trainable.
- **2.7** [Dropout — Srivastava et al. 2014 (JMLR 15)](https://jmlr.org/papers/v15/srivastava14a.html).
  Cheap implicit ensembling.
- **2.8** [U-Net — Ronneberger, Fischer, Brox 2015](https://arxiv.org/abs/1505.04597).
  Encoder–decoder with skips. Comes back as the diffusion backbone in Phase 7.
- **2.9** [ResNet — He et al. 2015](https://arxiv.org/abs/1512.03385).
  Residual connections; depth becomes unbounded.
- **★ Concept stop:**
  [representation-learning-arc](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/representation-learning-arc.md)
  (first half — word2vec's geometry thesis, before ELMo and CLIP take it
  further).

### Phase 3 — Deep RL comes of age (2013 → 2017)

- **3.1** [DQN — Mnih et al. 2015 (*Nature* 518)](https://www.nature.com/articles/nature14236).
  Experience replay + target network + CNN over pixels. The earlier
  [workshop predecessor (arXiv 2013)](https://arxiv.org/abs/1312.5602) is
  open-access if the Nature link is paywalled.
- **3.2** [AlphaGo — Silver et al. 2016 (*Nature* 529)](https://www.nature.com/articles/nature16961).
  Policy + value + MCTS; the human supervision still mattered.
- **3.3** [AlphaZero — Silver et al. 2017](https://arxiv.org/abs/1712.01815).
  Self-play from scratch; the supervision is removed.
- **★ Concept stop:**
  [rl-and-alignment-arc](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/rl-and-alignment-arc.md)
  (first half — game-RL boom; the alignment half waits for Phase 9).

### Phase 4 — Sequences, audio, and the attention turn (2016 → 2017)

- **4.1** [WaveNet — van den Oord et al. 2016](https://arxiv.org/abs/1609.03499).
  Causal dilated convolutions; exponential receptive field on raw audio.
- **4.2** [Transformer — Vaswani et al. 2017](https://arxiv.org/abs/1706.03762).
  Attention reorganizes sequence modeling. Read carefully — almost every
  later paper assumes you've internalized this one.
- **4.3** [VQ-VAE — van den Oord, Vinyals, Kavukcuoglu 2017](https://arxiv.org/abs/1711.00937).
  Discrete latents; the audio-codec ancestor of AudioLM / MusicLM.

### Phase 5 — Pretrain & fine-tune crystallizes (2018 → 2019)

The hinge of the entire decade. Read GPT-1 first so BERT's framing-against-it
lands.

- **5.1** [ELMo — Peters et al. 2018](https://arxiv.org/abs/1802.05365).
  Contextual word embeddings via bi-LSTM.
- **5.2** [GPT-1 — Radford et al. 2018](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf).
  Generative pretraining + discriminative fine-tune. (OpenAI report, no arXiv.)
- **5.3** [BERT — Devlin et al. 2018](https://arxiv.org/abs/1810.04805).
  Bidirectional masked LM. Note that BERT's paper explicitly positions
  itself *against* GPT-1.
- **5.4** [GPT-2 — Radford et al. 2019](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf).
  Unsupervised multitask via scale. (OpenAI report, no arXiv.)
- **★ Concept stops:**
  - [autoregressive-vs-gap-filling](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/autoregressive-vs-gap-filling.md)
    — the 2018 fork and the historical irony: BERT won 2018's leaderboards,
    GPT's autoregressive bet won the next five years.
  - [pretrain-finetune-lineage](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/pretrain-finetune-lineage.md)
    (full).

### Phase 6 — Scaling and emergence (2020)

- **6.1** [Scaling Laws — Kaplan et al. 2020](https://arxiv.org/abs/2001.08361).
  Loss as a smooth power law in parameters, data, compute.
- **6.2** [GPT-3 — Brown et al. 2020](https://arxiv.org/abs/2005.14165).
  Few-shot in-context learning — *not* predicted by the scaling laws.
- **★ Concept stop:**
  [scaling-and-emergence](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/scaling-and-emergence.md)
  (first half — Kaplan's predictable side; Chinchilla's revision waits
  for Phase 8).

### Phase 7 — Diffusion, ViT, and the text-to-image boom (2020 → 2022)

- **7.1** [DDPM — Ho, Jain, Abbeel 2020](https://arxiv.org/abs/2006.11239).
  Denoising diffusion as a tractable generative framework.
- **7.2** [ViT — Dosovitskiy et al. 2020](https://arxiv.org/abs/2010.11929).
  Images as token sequences for a Transformer.
- **7.3** [DALL-E — Ramesh et al. 2021](https://arxiv.org/abs/2102.12092).
  Autoregressive text-to-image over discrete tokens.
- **7.4** [CLIP — Radford et al. 2021](https://arxiv.org/abs/2103.00020).
  Contrastive text-image embedding — the multimodal substrate.
- **7.5** [LDM / Stable Diffusion — Rombach et al. 2021](https://arxiv.org/abs/2112.10752).
  Diffusion in a learned latent — practical, open, viral.
- **7.6** [Imagen — Saharia et al. 2022](https://arxiv.org/abs/2205.11487).
  Cascaded super-resolution diffusion + frozen text encoder.
- **★ Concept stops:**
  - [generative-modeling-frameworks](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/generative-modeling-frameworks.md)
    — five paradigms (VAE / GAN / autoregressive / VQ-VAE / diffusion),
    when each wins.
  - [diffusion-vs-autoregressive-by-modality](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/diffusion-vs-autoregressive-by-modality.md)
    — why autoregressive won text, diffusion won images, audio is contested.

### Phase 8 — Post-Chinchilla LLM era (2022)

- **8.1** [Chinchilla — Hoffmann et al. 2022](https://arxiv.org/abs/2203.15556).
  Revises Kaplan: data and parameters scale together.
- **8.2** [PaLM — Chowdhery et al. 2022](https://arxiv.org/abs/2204.02311).
  Pathways; 540B; the closed-frontier high-water mark before LLaMA opens
  the floodgates.
- **8.3** [CoT prompting — Wei et al. 2022](https://arxiv.org/abs/2201.11903).
  Reasoning by prompting — capability that *emerges* with scale.
- **8.4** [RAG — Lewis et al. 2020](https://arxiv.org/abs/2005.11401).
  Retrieval-augmented generation. (Earlier date but lands pedagogically
  here, next to CoT and Toolformer as the "what to bolt onto an LLM"
  thread.)
- **★ Concept stop:**
  [scaling-and-emergence](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/scaling-and-emergence.md)
  (full).

### Phase 9 — Alignment (2022)

- **9.1** [InstructGPT — Ouyang et al. 2022](https://arxiv.org/abs/2203.02155).
  RLHF as the alignment layer; the recipe behind ChatGPT.
- **9.2** [Constitutional AI — Bai et al. 2022](https://arxiv.org/abs/2212.08073).
  AI feedback replacing some of the human labels.
- **★ Concept stop:**
  [rl-and-alignment-arc](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/rl-and-alignment-arc.md)
  (full — the same machinery that solved Go now solves "be helpful and
  harmless").

### Phase 10 — Capabilities and the post-2022 frontier (2022 → 2023)

- **10.1** [Whisper — Radford et al. 2022](https://arxiv.org/abs/2212.04356).
  680K hours of weak-labeled audio + a transformer encoder = robust ASR.
- **10.2** [AlphaFold 2 — Jumper et al. 2021 (*Nature* 596)](https://www.nature.com/articles/s41586-021-03819-2).
  A science breakout — what "AI for X" looks like when X is taken seriously.
- **10.3** [Toolformer — Schick et al. 2023](https://arxiv.org/abs/2302.04761).
  Self-supervised tool use; the agent-runtime seed.
- **10.4** [LLaMA — Touvron et al. 2023](https://arxiv.org/abs/2302.13971).
  Open-weights, Chinchilla-compute-optimal. The open ecosystem starts here.
- **10.5** [GPT-4 Technical Report](https://arxiv.org/abs/2303.08774).
  Read as a *report*, not a paper — the new normal of closed frontier
  models.

### Phase 11 — Synthesis & where to go next

- **11.1** Re-read the [meta-wiki overview](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/overview.md).
  It should now feel like a memoir, not a syllabus.
- **11.2** "What's dead / what's alive" — pick a landmark from the route
  and write your own dead-vs-alive note in the style of
  [the DBN note](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/notes/dbn.md).
  The tutor reviews.
- **11.3** Pick a post-2023 frontier paper — multimodal foundation models
  (Chameleon, Transfusion, BAGEL — all in the [`multimodal/` topic
  dir](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/multimodal))
  or a recent audio/music model. Read it freely; report back.
- **11.4** Optional capstone: a replication, a teaching writeup, or a
  project that uses one of the techniques you read.

---

## Side-quest protocol

When a stop sparks a tangent — a citation chain, a Karpathy video, a
runnable demo, a topic deep-dive — *take it*. The tutor will:

1. **Name and log** the side quest in `progress.md` ("Side quests"
   section), with a one-line description and a link if useful.
2. **Mark the main-spine stop "paused for side quest <name>"** so the
   roadmap state is preserved.
3. **When you return**, the tutor reads the side-quest entry and asks
   what you learned before resuming the spine. Side-quest learnings are
   logged like main-spine learnings — they're real progress, not detour.

## Resuming after a long break

`progress.md` is the single source of truth. The tutor reads it first every
session and resumes from "Next stop." No penalty for gaps — the route is
patient.

## Teaching method (every stop)

1. **Frame** the paper: why now, what's its tension with what came before.
2. **Read together.** The tutor sketches the structure first, then you read
   the section that matters. Defer figures unless they're load-bearing.
3. **Probe** with one or two open questions — not a quiz. ("What's the
   load-bearing claim? What survives today?")
4. **Place** on the concept-page thread.
5. **Optional sidecar** — a runnable demo, an audio callout, a citation
   chase, or "what's dead / what's alive."
6. **Log** mastery + open questions to `progress.md`; full record to today's
   lesson file. End with a one-sentence preview of the next stop, and
   permission to take as long as you want before that next stop.
