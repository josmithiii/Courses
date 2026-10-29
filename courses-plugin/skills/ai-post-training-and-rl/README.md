# Post-Training & RL — From a Language Model to an Assistant
*Course 3 of the [LLMs & Sequence Models](../curricula/ai-llms-and-sequence-models.md) curriculum (Track B of [Music 423](../curricula/music423.md)).*

How a pretrained next-token predictor becomes an assistant. Deep-RL landmarks as the
field's vocabulary (MDPs and Bellman → Q-learning → **DQN**; REINFORCE → actor-critic/GAE →
**PPO**; **AlphaGo → AlphaZero** search and self-play) → **SFT** → reward models from
pairwise preferences → **RLHF** (InstructGPT: PPO with a KL penalty to the reference) →
**DPO** and its family → Constitutional AI / RLAIF → tool use (Toolformer) → the
learning-theory sidebar (**scaling laws**, **double descent**) → a living frontier (RL with
verifiable rewards and GRPO, process vs outcome rewards, test-time compute, agentic
tool-use RL).

**Keystone:** the reward and the leash — see
[`the-reward-and-the-leash.md`](the-reward-and-the-leash.md). Every method either climbs
`r` while a KL leash `β · KL(π ‖ π_ref)` holds it near the reference, or reaches the same
tilted distribution `π_ref · exp(r/β)` another way.

**Through-line:** the curriculum's one small character-level LM on Tiny Shakespeare,
post-trained by hand: SFT on a two-line-reply convention, a CPU-cheap **meter reward**
(ten syllables a line), REINFORCE → PPO-lite, best-of-n, DPO, GRPO — and reward hacking
caught in the act. Recipes in [`through-line-lab.md`](through-line-lab.md).

**Prerequisites:** [`ai-foundations`](../ai-foundations/) (Phases 4–5); ideally
[`ai-sequence-models`](../ai-sequence-models/) (its checkpoint is this course's starting
model; a self-contained fallback is in Phase 0). No hard gates; plunge in and backfill.
Pairs with [`ai-miracle-decade-plus`](../ai-miracle-decade-plus/) (the reading tour of the
same landmark papers).

**Format:** ~1 hr/day, ~30–35 sessions; CPU-first, tiered a/b/c capstone (CPU / Colab GPU /
local GPU).

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take ai-post-training-and-rl` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
