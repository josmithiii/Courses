# Lesson 04 — Tools and Skills

## Objective

Add a custom tool to Hermes. Bundle related instructions and
tools into a skill. Understand when to reach for each.

---

## Tools vs skills — the distinction

A **tool** is a single capability — one Python function exposed
to the model with a JSON schema. Examples: `read_file`,
`send_telegram`, `query_database`. Tools are about *what the
agent can DO*.

A **skill** is a bundle: instructions + (optionally) tools +
(optionally) sub-prompts, organized around a *task pattern*.
Examples: "review a pull request," "translate a document,"
"write a commit message." Skills are about *how the agent should
APPROACH something*.

Rule of thumb: if you find yourself writing the same paragraph
of instructions into many prompts, make it a skill. If you find
yourself wanting the model to call out to code, make it a tool.
Skills can include tools.

---

## Writing a tool

Hermes tools live in `tools/*.py`. Each file registers itself
at import time. Here's a minimal one:

```python
# ~/agents101/Hermes/tools/joke_tool.py
"""A tool that returns a joke. Demonstrates the registration shape."""

import json
import random

from tools.registry import register

_JOKES = [
    "Why did the agent cross the road? To call the chicken tool.",
    "I told a SQL query to JOIN the chickens. They CROSSed by the road.",
    "There are 10 kinds of people in the world: those who use OOP and " 
      "those who use Lisp and those who can't count.",
]


def joke_handler(_args: dict) -> str:
    """Return a randomly selected joke."""
    return json.dumps({"joke": random.choice(_JOKES)})


register(
    name="joke",
    description="Return a random programming joke. Takes no arguments.",
    parameters={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=joke_handler,
)
```

That's it. Restart `hermes` and ask:

```
Tell me a joke using your tools.
```

The model will call `joke`, see the result, and present it to
you. You just extended a 3000-commit agent with 30 lines.

---

## Tool design principles

1. **Handlers return JSON strings.** Not dicts. Not Python
   objects. `json.dumps(...)` everywhere. The runtime expects
   it; the model parses it as text.

2. **The description is the API to the model.** It's how the
   model decides whether to call your tool. "Read a file" is
   bad; "Read a UTF-8 text file from local disk; returns first
   2000 lines unless `lines` is specified" is good. Be specific
   about constraints.

3. **Validate at the boundary.** If the model passes a path
   outside an allowed directory, reject it explicitly. Don't
   trust tool inputs just because they came from "the model" —
   they're coming through a network call.

4. **Errors are also JSON.** `json.dumps({"error": "file not
   found", "path": path})`. The model will see this and can
   recover (try a different path, ask the user, etc.).

5. **Side effects: log them.** A future you will need to know
   what your agent did, when, and why.

---

## Writing a skill

Skills live in:

- `skills/` (bundled with Hermes; ~28 categories)
- `optional-skills/` (in-repo but off by default)
- `~/.hermes/skills/` (your personal ones)

A skill is a directory with a `SKILL.md`:

```bash
mkdir -p ~/.hermes/skills/standup-summary
cat > ~/.hermes/skills/standup-summary/SKILL.md <<'EOF'
---
name: standup-summary
description: |
  Summarize a list of yesterday's git commits into a short
  standup message. Use when the user asks for "standup",
  "yesterday's work", or similar.
---

# Standup summary

When invoked:

1. Run `git log --since="yesterday" --author="$(git config user.email)"
   --oneline` via the bash tool.
2. Group commits by repo if you see multiple.
3. Produce a 3-bullet summary, then 1 bullet on what's blocking,
   then 1 bullet on today's plan.
4. Don't list every commit; pick the meaningful ones.
5. Keep total length under 200 words.
EOF
```

Restart Hermes, type `/skills` — you should see `standup-summary`.
Trigger it:

```
Give me my standup summary.
```

The model reads the SKILL.md (Hermes auto-injects it because the
description matches the request), follows the steps, and produces
the summary.

---

## The frontmatter

`SKILL.md` files have YAML frontmatter:

- `name`: short slug, used in `/skills` listing
- `description`: tells the model *when to use this skill* —
  similar to a tool description, but for a whole behavior

The skill is only injected when its description seems relevant to
the user's request. The model handles that matching, mostly via
the system prompt. Your skill is invisible cost until activated.

---

## Built-in skills worth knowing

```bash
ls ~/agents101/Hermes/skills/
```

Notable ones:

- `git-commit` — write a structured commit message
- `init` — generate a CLAUDE.md for a new repo
- `merge-upstream` — pull upstream main and report changes
- `security-review` — audit pending changes
- `nb` — append a note to long-term memory

Try `/git-commit` from inside a repo with uncommitted changes.

---

## Skill composition

A skill can `require` other skills:

```yaml
---
name: ship-it
description: Build, test, commit, push, and open a PR. Use for "ship".
requires:
  - git-commit
  - commit-commands:commit-push-pr
---
```

The `requires` skills are loaded into context. You're composing
behaviors, not just instructions.

---

## When to write a tool vs a skill

| You want… | Write a… |
|---|---|
| The agent to call your Python code | Tool |
| The agent to follow a specific multi-step recipe | Skill |
| To expose a new API (Slack, your DB, etc.) | Tool |
| To codify "for this kind of task, do these steps" | Skill |
| To give the agent a new piece of factual knowledge | Skill (or memory) |
| To give the agent a new piece of *executable* knowledge | Tool |

Often the answer is both: a skill that *uses* a tool you also wrote.

---

## Pitfalls

- **Don't over-tool.** Each tool you register goes into the
  system prompt. 40 tools = a lot of tokens. Hermes has tool
  groupings (`toolsets.py`) for this reason.
- **Tool name clashes.** First registration wins. If you have
  two `joke` tools, only one survives.
- **Skill descriptions are not free.** Long descriptions inflate
  the system prompt. Keep them focused and short.
- **Don't put secrets in tool source.** Tools are shipped in
  the system prompt. Read secrets from env vars inside the
  handler.
- **`json.dumps` defaults to ASCII.** If you have UTF-8 content,
  pass `ensure_ascii=False` or the model sees `\uXXXX` escapes.

---

## Further reading

- `tools/registry.py` — how registration works
- `tools/` — 40-ish examples
- `skills/` — bundled skills as templates
- Anthropic skills design: https://www.anthropic.com/news/agent-skills

---

Next: [05-kanban.md](05-kanban.md) — many agents, one board.
