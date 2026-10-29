# AI Sequence Models
*Course 2 of the [LLMs & Sequence Models](../curricula/ai-llms-and-sequence-models.md) curriculum — the architecture course.*

word2vec and seq2seq → attention → the **Transformer** (read closely, KV cache measured) →
GPT-style LLMs → the efficiency response: **linear attention** and the delta rule, gated
linear RNNs (GLA, HGRN2, RWKV), **HiPPO → S4 → S4D → LRU**, **Mamba** and Mamba-2/SSD, and
Transformer–SSM **hybrids** (Jamba, Zamba, Samba, Griffin), with a living frontier phase
(Gated DeltaNet, RWKV-7, Mamba-3, test-time training, 2025–26 production hybrids). One
character-level model, trained from scratch on Tiny Shakespeare, rebuilt with each mechanism
and scored on perplexity, recall, and cost. DSP readers: state-space filters, LTV filters
and LMS all reappear.

**Keystone:** what a token can see, and at what cost — see [`the-context-budget.md`](the-context-budget.md).

**Prerequisites:** [`ai-foundations`](../ai-foundations/) Phases 4–5 recommended, not
required (plunge in). [`ai-miracle-decade-plus`](../ai-miracle-decade-plus/) runs in
parallel for the history. Hands its checkpoint to `ai-post-training-and-rl`.

**Format:** ~1 hr/day, ~30–35 sessions; tiered CPU / Colab / local-GPU capstone.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take ai-sequence-models` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
