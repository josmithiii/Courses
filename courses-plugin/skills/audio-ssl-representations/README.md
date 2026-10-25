# Self-Supervised Audio Representations
*Encoder-side enrichment for the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum; sibling of [`disentanglement`](../disentanglement/).*

How raw audio becomes a learned representation **without labels**: wav2vec 2.0
(contrastive InfoNCE) → HuBERT (masked prediction of k-means cluster IDs) →
data2vec / w2v-BERT / BEST-RQ → MERT ("HuBERT for music"; EnCodec + CQT teachers;
layer specialization) → probing → the resynthesis gap. Pinned to the shared piano
clip, *probed per layer*.

**Keystone:** the pretext task & the target — see [`the-pretext-task.md`](the-pretext-task.md).
The representation is a *shadow of its target*, so an understanding-grade SSL encoder is
**neither invertible nor disentangled** — the gap a resynthesis system must close.

**Prerequisites:** Transformers + masked language modeling and the embedding idea (from
[`ai-foundations`](../ai-foundations/)); a neural codec ([`audio-codecs`](../audio-codecs/)) helps.

**Format:** ~1 hr/day, ~18–22 sessions; tiered a/b/c capstone (CPU probes, no GPU for tier a).

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take audio-ssl-representations` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
