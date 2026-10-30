# LLMs & Sequence Models — through-line asset

This directory holds the **shared through-line corpus** for the
[`ai-llms-and-sequence-models`](../../ai-llms-and-sequence-models.md) curriculum (Track B):
one small text corpus on which the learner trains **one small character-level language
model from scratch**, rebuilt with each architecture in `ai-sequence-models` (bigram → RNN
→ attention → Transformer → linear attention / SSM / Mamba → hybrid) and then post-trained
in `ai-post-training-and-rl` (supervised fine-tuning, a reward model, policy-gradient /
RLHF-style and DPO-style preference tuning). See the curriculum's **Through-line** section.

## The corpus (spec)

| Field | Value |
|-------|-------|
| Filename | `tinyshakespeare.txt` |
| Content | ~40,000 lines of Shakespeare plays, concatenated (Karpathy's *Tiny Shakespeare*) |
| Size | 1,115,394 characters, 40,000 lines, plain ASCII |
| Vocabulary | **65** characters: `\n`, space, `!$&',-.3:;?`, `A-Z`, `a-z` |
| Split | first 90% train (1,003,854 chars), last 10% validation (111,540 chars) |
| SHA-256 | `86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed` |
| Source | https://github.com/karpathy/char-rnn (`data/tinyshakespeare/input.txt`) — see [`SOURCE.md`](SOURCE.md) |

Why this corpus: it is the standard tiny LM benchmark (char-rnn, nanoGPT, Karpathy's
"makemore" lectures), small enough to train every architecture on a laptop CPU in minutes,
and its output is *legible*: a learner can read a sample and hear in it how much structure
the model has captured (spelling → words → speaker names and line breaks → verse).

## Numbers the courses reuse

Character-level, on the 90/10 split above (perplexity = `exp(mean NLL in nats)`):

| Model | Val NLL (nats/char) | Val perplexity |
|-------|---------------------|----------------|
| Uniform over 65 chars | ln 65 = 4.174 | 65 |
| Unigram (add-one) | 3.347 | 28.4 |
| Bigram (add-one counts) | 2.482 | 12.0 |
| nanoGPT "baby GPT" (6 layers, 384 dim, context 256; GPU minutes) | ≈ 1.47 | ≈ 4.4 |

The first three rows are exact (computed from the file). The last row is Karpathy's
reported number for his tuned small Transformer and is an *empirical reference point*, not
a target: a CPU-sized model in these courses will land between the bigram and that line,
and where each architecture lands is what the learner measures.

Tutors must **fail fast** if `tinyshakespeare.txt` is missing or its SHA-256 differs: say
so and stop. Never silently substitute another corpus.
