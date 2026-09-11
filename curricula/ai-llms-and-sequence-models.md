# LLMs & Sequence Models

**Status:** 🟡 Partial — the on-ramp and the paper-history course are active; the
architecture and post-training courses are planned. Track B of the
[Music 423 meta-curriculum](music423.md).

## Goal

Take a learner from "what is attention?" to reading the current sequence-model
literature fluently: the Transformer and its LLM descendants, the long-context and
efficiency responses (linear attention, state-space models, Mamba, RWKV, hybrids), and
the post-training layer that turns a language model into an assistant (RL, RLHF,
alignment). Also the vision and multimodal branches that reuse the same backbone
(autoregressive image generation, unified text+image models), since those are where
the audio codec-LMs of Track A borrowed their ideas.

**Who it's for.** Anyone who wants the *general* AI backbone rather than the audio
specialization — or an audio person who wants to understand the Transformer well enough
to read the codec-LM and DiT papers in Track A as an insider.

## Prerequisite

- [`../ai-foundations/`](../ai-foundations/) **(required unless equivalent)** — its
  Phases 4–5 (attention, Transformers, LLMs) are the entry frontier here.

## Ordered course list

| # | Course | Status | Why here |
|---|--------|--------|----------|
| 1 | [`../ai-miracle-decade-plus/`](../ai-miracle-decade-plus/) | 🟢 Active | The timeline: 40 landmark papers DBN → GPT-4, with concept-page stops. Gives the *history* the rest of the track fills in. Can also run in parallel with course 2. |
| 2 | `../ai-sequence-models/` | ⚪ Planned | The *architecture* course: word2vec and seq2seq → attention → the Transformer (read closely) → GPT-style LLMs → the efficiency response: linear attention, HiPPO/S4 → Mamba, RWKV, gated linear RNNs (HGRN2), and Transformer–SSM hybrids (Jamba, Zamba, Samba). Keystone = **what a token can attend to, and at what cost** — every architecture is a different answer. Pinned to one tiny language model trained from scratch on a small corpus, re-implemented with each mechanism. |
| 3 | `../ai-post-training-and-rl/` | ⚪ Planned | From a pretrained LM to an assistant: deep RL landmarks (DQN → AlphaGo/AlphaZero) as the language of the field, then RLHF (InstructGPT), Constitutional AI, and tool use (Toolformer). Also the learning-theory sidebar: scaling laws and double descent — why bigger keeps working. |

## Enrichment / co-requisites (parallel, not gates)

- `../ai-vision-and-multimodal/` ⚪ Planned — the vision branches of the same backbone:
  CNN backbones (AlexNet, ResNet, U-Net), VAEs and GANs, ViT and autoregressive image
  generation, DALL-E and unified multimodal models. Half of it is *also* background for
  Track A's diffusion course, so it is listed in both.
- [`../audio-codec-lms/`](../audio-codec-lms/) — the audio application of course 2:
  language-modeling codec tokens (AudioLM → MusicGen → MIDI-VALLE). The natural bridge to
  Track A for anyone who finishes this track.

## Through-line

One **small language model trained from scratch** on a small text corpus, revisited with
every architecture (RNN → attention → Transformer → Mamba → hybrid) so the learner *sees*
what each mechanism buys in perplexity, context length, and speed. Post-training then
fine-tunes that same model with preference data.

## Source of truth

Topic directories in
[`music423-2023`](https://cm-gitlab.stanford.edu/jos/music423-2023), each with a wiki:

- [`attention/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/attention) —
  Transformer and successors (the largest directory in the track).
- [`natural-language-processing/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/natural-language-processing) —
  word2vec, seq2seq, and pre-Transformer contextual representations.
- [`mamba/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/mamba),
  [`rwkv/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/rwkv),
  [`gated-recurrence/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/gated-recurrence),
  [`hybrid/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/hybrid) —
  the state-space / linear-RNN / hybrid response to quadratic attention.
- [`reinforcement-learning/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/reinforcement-learning),
  [`double-descent/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/double-descent) —
  course 3.
- [`images-ar/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/images-ar),
  [`multimodal/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/multimodal),
  [`images/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/images) —
  the vision/multimodal enrichment.
- [`ai-2012-to-2023/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-2012-to-2023) —
  course 1 (the landmark list).
