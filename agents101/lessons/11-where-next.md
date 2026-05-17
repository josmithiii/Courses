# Lesson 11 — Where Next

## What you can now do

If you worked through this course (not just read it):

- Run a local model server and talk to it from Python.
- Run a Hermes agent in a terminal, on Telegram, or in a container.
- Write tools and skills to extend agent capability.
- Spawn coordinated worker agents via the kanban.
- Schedule recurring jobs, both LLM and watchdog flavors.
- Page yourself on Telegram when the fleet misbehaves.
- Debug a stuck or misbehaving agent across seven layers of state.
- Reason about what your monitoring doesn't catch.

That's not "hello world." That's an operator-level competency. You
can join an agent-ops conversation and follow what's happening.

What's NOT in this course:

- LLM internals (training, fine-tuning, quantization details).
- RLHF or other alignment techniques.
- Agent benchmarks and evaluation.
- Multi-modal (vision/audio/video) agents.
- Distributed / multi-machine fleets.
- Tool-use security at scale (sandboxing, capability systems).

Below: where to go for each.

---

## Other agent frameworks worth knowing

Take what you learned about Hermes and try one of these so you
internalize the *pattern* not the *implementation*:

- **[Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)**
  — Anthropic's framework. Smaller, focused on building specific
  agents rather than a general fleet. The skills concept comes
  from here.
- **[Claude Code](https://claude.ai/code)** — Anthropic's
  interactive coding agent. CLI / IDE plugin / web. Closest to
  Hermes in spirit (terminal-first, real codebase work).
- **[Open Claw](https://github.com/josmithiii/openclaw)** —
  JOS's personal assistant framework. Node-based. Multi-platform
  out of the box (WhatsApp, Telegram, Discord, Slack). Sub-agents
  via a hooks API.
- **[Pi Agent](https://github.com/josmithiii/pi)** — JOS's
  experimental agent at `/l/pi`. Worth a look for ideas, currently
  research-grade.
- **[smolagents](https://huggingface.co/docs/smolagents)** — HF's
  minimalist framework. Read for clarity, not for production.
- **[OpenHands](https://github.com/All-Hands-AI/OpenHands)** (was
  OpenDevin) — Software-engineering agent specifically. Strong
  benchmark numbers on SWE-Bench.
- **[AutoGen](https://github.com/microsoft/autogen)** — Microsoft's
  multi-agent framework. Heavy abstractions; worth seeing the
  alternative.

For each, look at: how is the agent loop implemented? where does
state live? how are tools registered? where's the message
gateway? You'll see the four pieces from lesson 01 in every one.

---

## Going deeper on the model side

You've been treating the model as a black box. If you want to
open it:

- **[A Hackers' Guide to Language Models](https://www.youtube.com/watch?v=jkrNMKz9pWU)** —
  Jeremy Howard, 90 min. Best practical intro to *what's actually
  happening* inside a chat completion.
- **[Karpathy's nanoGPT walkthrough](https://www.youtube.com/watch?v=kCc8FmEb1nY)** —
  build GPT from scratch in 2 hours.
- **[LLM Visualization](https://bbycroft.net/llm)** — interactive
  visualization of inference. Click through it once; you'll never
  forget what an attention head is.
- **MLX-LM source** — small, readable PyTorch-like code. Read
  `mlx_lm/server.py` to see what your `/v1/chat/completions`
  endpoint actually does.

---

## Reinforcement learning for agents

Hermes-agent has hooks for RL training (see the
`tinker-atropos/` and adjacent directories). The field is moving
fast:

- **Nous Research** publishes regularly; the Hermes line of
  models is theirs. Their X feed and blog are the easiest way to
  stay current.
- **DeepSeek-R1** and the broader o1/R1 family — "reasoning"
  models trained with RL. Read the DeepSeek-R1 paper for the
  recipe.
- **DSPy** (Stanford) — programs that include LLM calls as
  primitives, with optimization. Conceptually adjacent to RL.

---

## Practical extensions to *this* setup

Pick one or two and build them next month:

1. **The `stuck_running` overseer probe** (lesson 08, "what
   this misses"). 20 lines. Catches the silent-death case.
2. **Slack outbound for `hermes notify`** (one branch in
   `notify.py`). Mechanical extension of the lesson-07 work.
3. **An incident-log JSONL** appended in `page()` for post-hoc
   analysis ("how many times did X happen this week?").
4. **A web push for the dashboard** — replace the cached
   `gateway_state.json` heartbeat with a real SSE stream so the
   dashboard's status badge isn't bugged.
5. **A skill of your own** — codify a recurring task you do.
   The standup-summary in lesson 04 is the template.
6. **A custom tool** that wraps an API you already use (Linear,
   GitHub Issues, your CMS). Now your agent can act on it.

---

## Reading list (papers, not blogs)

- *Building effective agents* — Anthropic, 2024.
  https://www.anthropic.com/research/building-effective-agents
- *ReAct: Synergizing Reasoning and Acting* — Yao et al., 2022.
  https://arxiv.org/abs/2210.03629
- *Toolformer* — Schick et al., 2023. Teaching models to use
  tools without supervision. https://arxiv.org/abs/2302.04761
- *SWE-bench* — Jimenez et al., 2023. The standard benchmark
  for software-engineering agents. https://arxiv.org/abs/2310.06770
- *Reflexion* — Shinn et al., 2023. Agents that learn from
  failure within a session. https://arxiv.org/abs/2303.11366

---

## Community

- **[Nous Research Discord](https://discord.gg/jqVphNsB4H)** —
  where Hermes lives.
- **[r/LocalLLaMA](https://reddit.com/r/LocalLLaMA)** — the
  practical local-models community.
- **[/r/LangChain](https://reddit.com/r/LangChain)** despite its
  name covers the whole agent space.
- The repo's own issues — read the closed ones. You'll learn the
  most about the system by seeing how problems were diagnosed
  and fixed.

---

## When you're ready to teach

This course is short. Many things are skimmed (skills composition,
streaming UIs, security, multi-tenancy, the gateway internals).
Each one could be its own course.

If you write Lesson 12 on a topic you cared about, drop a PR
against `/w/Courses/agents101/`. The course gets better.

---

## Final note from the maintainer

This course was distilled from a single afternoon's collaboration
between JOS and Claude Code, with the artifact (the watchdog,
the notify CLI, the supporting commit) sitting in the Hermes
repo as concrete proof that the lessons land in real code.

The agent ecosystem is moving fast. The specific commands here
will drift; the *patterns* won't. Local model + agent loop +
tools + persistent state + delivery surface + watchdog — that
recipe has been stable for a while and is likely to stay so.

Build something. The best way to keep learning is to be on the
hook for a system you care about.

— And now, go run `hermes` and try something.
