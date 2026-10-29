# LLMs & Sequence Models

**Status:** 🟢 Complete — the paper-history, architecture and post-training courses and the
vision/multimodal enrichment are all active. Track B of the
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
| 2 | [`../ai-sequence-models/`](../ai-sequence-models/) | 🟢 Active | The *architecture* course: word2vec and seq2seq → attention → the Transformer (read closely, KV cache measured) → GPT-style LLMs and cheaper exact attention → the efficiency response: linear attention and the delta rule, gated linear RNNs (GLA, HGRN2, RWKV), HiPPO/S4/S4D/LRU as state-space filters → Mamba and Mamba-2/SSD, and Transformer–SSM hybrids (Jamba, Zamba, Samba, Griffin); living frontier. Keystone = **what a token can see, and at what cost** ([`the-context-budget.md`](../ai-sequence-models/the-context-budget.md)) — every architecture is a different answer. The through-line model, rebuilt eight ways; ends by handing its checkpoint to course 3. |
| 3 | [`../ai-post-training-and-rl/`](../ai-post-training-and-rl/) | 🟢 Active | From a pretrained LM to an assistant: deep RL landmarks (DQN, PPO, AlphaGo/AlphaZero) as the language of the field, then SFT, reward models, RLHF (InstructGPT), DPO and its family, Constitutional AI, and tool use (Toolformer); living frontier (RLVR/GRPO, process rewards, test-time compute). Also the learning-theory sidebar: scaling laws and double descent — why bigger keeps working. Keystone = **the reward and the leash** ([`the-reward-and-the-leash.md`](../ai-post-training-and-rl/the-reward-and-the-leash.md)). Post-trains the course-2 checkpoint (fallback model in its Phase 0). |

## Enrichment / co-requisites (parallel, not gates)

- [`../ai-vision-and-multimodal/`](../ai-vision-and-multimodal/) 🟢 Active — the vision branches of the same backbone:
  CNN backbones (AlexNet, ResNet, U-Net), VAEs and GANs, ViT and autoregressive image
  generation, DALL-E and unified multimodal models. Half of it is *also* background for
  Track A's diffusion course, so it is listed in both.
- [`../audio-codec-lms/`](../audio-codec-lms/) — the audio application of course 2:
  language-modeling codec tokens (AudioLM → MusicGen → MIDI-VALLE). The natural bridge to
  Track A for anyone who finishes this track.

## Through-line

One **small character-level language model trained from scratch** on *Tiny Shakespeare*
([`assets/ai-llms-and-sequence-models/`](assets/ai-llms-and-sequence-models/README.md):
1.1 M characters, 65-character vocabulary, 90/10 split; baselines uniform 65, unigram 28.4,
bigram 12.0 perplexity). Course 2 rebuilds it with every architecture (bigram → GRU →
attention → Transformer → linear attention → S4 → Mamba → hybrid) so the learner *sees*
what each mechanism buys in perplexity, recall, and cost per token, and saves the winner
as a checkpoint bundle. Course 3 post-trains that same model: SFT, a ten-syllable meter
reward, best-of-n, PPO with a KL leash (and reward hacking without one), a learned reward
model, and DPO. The vision enrichment has its own worked example (Fashion-MNIST).

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
