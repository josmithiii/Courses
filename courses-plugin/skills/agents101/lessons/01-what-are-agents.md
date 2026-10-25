# Lesson 01 — What Is an Agent?

## Objective

By the end of this lesson you can answer, on the spot:

1. How an agent differs from a chatbot.
2. What "tool use" means in concrete API terms.
3. Why the agent loop is the thing, not the model.

No code in this lesson. Mostly mental model. Lesson 03 onward
gets your hands on a real agent.

---

## Three things that all use LLMs

| | Chatbot | Workflow | Agent |
|---|---|---|---|
| Who decides what step is next? | User | The programmer (hard-coded) | The LLM, every turn |
| Side effects? | None — just text | Pre-defined, narrow | Open-ended via tools |
| Loop until done? | No — one turn | Bounded | Yes — until LLM says "done" |

A **chatbot** is a thin UI over `POST /chat/completions`. The model
generates text; the user reads it; repeat.

A **workflow** (think: LangChain "chain", n8n flow) is a fixed
DAG of LLM calls and code. The model fills in slots; the *programmer*
decides the next step.

An **agent** is the model itself deciding what to do next. The
program offers it *tools* — file I/O, shell, HTTP, custom Python
functions — and the model picks which tool to call, with what
arguments, on each turn. The loop keeps going until the model
returns a final answer without calling any tool.

Hermes-agent is agents. Claude Code is agents. AutoGPT was an
early, rough, agent. ChatGPT-with-a-browse-button is a thin agent
over one tool.

---

## Tool use, concretely

Modern chat APIs let you send a `tools` parameter alongside the
conversation:

```json
POST /v1/chat/completions
{
  "model": "...",
  "messages": [...],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "read_file",
        "description": "Read text from a file on disk",
        "parameters": {
          "type": "object",
          "properties": {"path": {"type": "string"}},
          "required": ["path"]
        }
      }
    },
    {"type": "function", "function": {"name": "write_file", ...}},
    ...
  ]
}
```

The model can reply with either:

- **A normal message** (we're done, here's the answer), OR
- **A tool call** (`{"name": "read_file", "arguments": {"path": "/etc/hosts"}}`).

Your runtime sees the tool call, **actually runs it**, and appends
the result back into the conversation. Then it asks the model again.
Repeat until the model returns a normal message.

That's the agent loop. It's about 100 lines of Python plus a `while`.

---

## The four pieces of an agent runtime

Every agent framework — Hermes, LangChain, Claude Agent SDK, your
weekend project — has the same four pieces:

1. **The model client.** A wrapper around `POST /v1/chat/completions`.
   Knows the URL, the model name, the API key. Maybe handles
   retries and streaming.

2. **The tool registry.** A list of available tools, each with its
   JSON schema (for the model) and its Python implementation (for
   the runtime). The registry generates the `tools: [...]` payload
   and dispatches tool calls.

3. **The conversation state.** A list of messages: system prompt,
   user turns, assistant turns, tool calls, tool results. Stored in
   memory or persisted (Hermes uses SQLite — we'll see in lesson 09).

4. **The loop.** Take the state, call the model, see what comes
   back, dispatch any tool calls, append results, repeat. Stop when
   the model returns a non-tool message OR when a turn limit is hit.

If you internalize those four pieces you can read any agent
framework's source code in an evening.

---

## Where Hermes adds value

Hermes-agent is "what the four pieces look like when you take them
seriously for ~3000 commits of seriousness." Specifically:

- Tools are auto-discovered from `tools/*.py` (one file per tool).
- Skills are reusable *bundles* of instructions + tools (lesson 04).
- Sessions are persisted to SQLite and searchable via FTS5.
- Multiple delivery surfaces (terminal, Telegram, Slack, web
  dashboard) share the same agent core.
- A "gateway" daemon handles inbound messaging across platforms
  and dispatches conversations to the agent.
- A "kanban" supports multi-agent work-stealing (lesson 05).

You could build all of this yourself in a few weeks. We use Hermes
because the wiring is already done and the corners are debugged.

---

## Common confusions

**"Is an agent just GPT-with-tools?"** Almost. The model is just
predicting next tokens; the tool-use loop is what turns "predict
next tokens" into "take actions in the world." Same model, very
different system behavior.

**"Why can't I just call the LLM in a `while` loop myself?"** You
can! Many people do. Frameworks exist because (a) the boilerplate
adds up (tool dispatch, error handling, session storage, multiple
LLM providers), and (b) shared infrastructure lets you swap models,
add observability, etc., without rewriting your prompts.

**"Why are some 'agents' just one tool?"** Marketing. If the loop
runs once and only calls one tool, you have a workflow with extra
steps. That's fine — but call it what it is.

**"My agent does dumb things — is the model bad?"** Maybe. More
often the model is fine and the *instructions* (system prompt,
tool descriptions) are too vague. Lesson 04 covers this.

---

## Pitfalls

- **Conflating the model with the agent.** "Claude" is a model.
  "Claude Code" is an agent built on Claude. Confusing the two
  leads to expectations like "Claude can browse my filesystem" —
  no, Claude *Code* has a file-read tool wired up.
- **Assuming the model executes code.** It doesn't. It outputs
  text that *looks like* a tool call, and your runtime is the
  thing that actually runs it. The model can lie about having
  done something; the runtime should never lie about whether it
  did.
- **Forgetting that every turn is a fresh forward pass.** The
  model has no memory between turns except what's in the
  conversation history you send. State lives in your runtime,
  not in the model.

---

## Further reading

- Anthropic on building effective agents:
  https://www.anthropic.com/research/building-effective-agents
- ReAct (the foundational "reason+act" agent paper):
  https://arxiv.org/abs/2210.03629
- OpenAI function calling docs (the API shape of tool use):
  https://platform.openai.com/docs/guides/function-calling

---

Next: [02-local-models.md](02-local-models.md) — get an actual
model on the line.
