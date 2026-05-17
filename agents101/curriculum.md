# agents101 — Curriculum

A practical course on building, running, and overseeing a fleet of
local AI agents. Distilled from a real day-long session where Claude
Code and JOS wired up Telegram oversight for the Hermes agent fleet —
every topic is grounded in something built, broken, and fixed.

## Course goals

By the end the learner can:

- Run a local LLM and have a real conversation with an agent on
  their own machine.
- Extend the agent with new tools and skills.
- Coordinate multiple agents via a task board.
- Schedule recurring agent and non-agent jobs.
- Wire Telegram (or another platform) for bidirectional comms.
- Build a polling watchdog that pages on fleet anomalies.
- Debug a stuck/misbehaving agent across logs, DBs, processes.
- Run the whole thing in containers.

## Audience and prerequisites

A technical reader (engineer, scientist, hobbyist) who can:

- Read Python.
- Use a Unix shell.
- Edit YAML and JSON.

They do NOT need:

- Prior ML / LLM internals knowledge.
- A cloud API key (everything runs locally).
- Prior agent-framework experience.

## Stack assumed

- macOS (Apple Silicon strongly preferred) or Linux with a GPU
- Python 3.11 via `uv`
- Docker (for the multi-agent and container topics)
- A local model server: MLX (Apple) or Ollama (cross-platform)
- A Telegram bot (created via @BotFather; used from topic 7 on)

## Teaching method

- **Intuition + command, paired every time.** Explain the concept in
  plain words, then have the learner run the actual command and
  observe the output.
- **One concept per session.** ~1 hour. Better to teach one thing
  well than three things shallowly.
- **Verify with a small exercise** before advancing. The exercise is
  usually "now do the same thing with a different input" or "add a
  flag and predict what changes."
- **Pitfalls are first-class content.** Every topic has a real-world
  failure mode the learner will hit. Cover it before they hit it.
- **Reference depth in `lessons/NN-*.md`.** The tutor draws on these
  for examples, but the live session is the primary surface — don't
  just have the learner read.

## Syllabus

The 12 topics, in suggested order. Each ~1 session, but some
(especially 5, 8) may warrant 2 if the learner is going deep.

| # | Topic | Reference | Learner outcome |
|---|---|---|---|
| 0 | **Orientation + Setup** — install Python 3.11/uv, Docker, a local model server | `lessons/00-setup.md` | Smoke-test passes: `curl /v1/models` returns a model |
| 1 | **What is an Agent?** — agents vs LLMs vs chatbots; tool use; the loop | `lessons/01-what-are-agents.md` | Can explain the four pieces of an agent runtime |
| 2 | **Local Models** — MLX/Ollama; OpenAI-compatible HTTP; SDK basics | `lessons/02-local-models.md` | Sends a chat completion from Python; understands tool-call support varies |
| 3 | **First Conversation** — install Hermes; configure to local model; talk in TUI | `lessons/03-first-conversation.md` | Has a real agent reply in a terminal; sees a tool call |
| 4 | **Tools and Skills** — write a custom tool; write a skill; understand when to use each | `lessons/04-tools-and-skills.md` | Has a tool they wrote being invoked by the agent |
| 5 | **Kanban: Multi-Agent Coordination** — task board, claim locks, dispatch, heartbeats | `lessons/05-kanban.md` | Spawns a worker that completes a task end-to-end |
| 6 | **Cron and Scheduling** — Hermes cron; `--no-agent` watchdogs; LLM vs script | `lessons/06-cron-and-scheduling.md` | Has a scheduled job firing; understands `--no-agent` |
| 7 | **Messaging Gateways** — Telegram setup; outbound vs inbound; gateway daemon | `lessons/07-messaging.md` | Receives a Telegram message from `hermes notify`; chats with the bot |
| 8 | **Oversight** — building a polling watchdog; what kanban doesn't tell you | `lessons/08-oversight.md` | Has the overseer running and paging Telegram on simulated failure |
| 9 | **Debugging Agent Systems** — seven layers of state; tour of where to look | `lessons/09-debugging.md` | Can find any stuck task / silent error within a minute |
| 10 | **Docker for Agents** — compose; mounts; host vs container paths | `lessons/10-docker.md` | Runs Hermes via compose; understands the path trap |
| 11 | **Where Next** — other frameworks; deeper model side; community | `lessons/11-where-next.md` | Has a concrete next-month plan to build something |

Topics 0–3 are foundational (run them in order). Topics 4–10 can be
re-ordered if a learner has a specific project they want to build.
Topic 11 is the wrap-up.

## Session shape

Default ~1-hour structure the tutor follows:

1. **Recap (5 min)** — friendly two-sentence summary of last
   session; one quick recall question. If the learner is shaky,
   re-teach before continuing.
2. **New concept (15 min)** — explain in plain words; show one
   small example.
3. **Hands-on (30 min)** — learner runs commands. Tutor pairs:
   predict, run, observe, explain. Adjust depth based on errors.
4. **Pitfall walk-through (5 min)** — surface one real pitfall
   from the topic's `lessons/NN-*.md`. Demonstrate it if quick.
5. **Wrap (5 min)** — what was learned; what's next; preview.

If the learner is short on time, do steps 1, 2, and a smaller 3.
Never rush past an unverified concept just to "finish."

## Mastery criteria

A topic is mastered when the learner can:

1. Explain the concept in their own words (2–3 sentences).
2. Run the relevant command without copy-paste help.
3. Predict what one common variation does without running it.

Record this in the data-dir `progress.md` mastery log.

## Where the case study lives

The Hermes-agent repo this course uses as a worked example:

```bash
git clone https://github.com/NousResearch/Hermes.git
```

In particular, the artifacts from the day this course was born are
worth reading once the learner gets to topic 8:

- `hermes_cli/notify.py` — outbound CLI
- `scripts/agent_overseer.py` — the watchdog
- `tests/scripts/test_agent_overseer.py` — how to test the watchdog
- `ClaudeCodeOrchestrationGuide.md` — the operator's-eye companion

These are real production-shape code, not toys. Read for style and
defensive habits as much as for the concrete logic.
