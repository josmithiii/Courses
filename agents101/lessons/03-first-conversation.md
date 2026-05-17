# Lesson 03 — First Conversation with Hermes

## Objective

Install Hermes-agent, point it at your local model, and have a
real conversation in your terminal. Then look at where the state
lives so you'll know in lesson 09 how to debug it.

---

## Install

```bash
git clone https://github.com/NousResearch/Hermes.git
cd Hermes
./setup-hermes.sh
```

The setup script creates `.venv`, installs Hermes plus the `[all,dev]`
extras, creates `~/.hermes/.env` from a template, and symlinks
`hermes` into `~/.local/bin`. About 3–5 minutes.

If `~/.local/bin` isn't on your PATH, the script will tell you.
Add it.

```bash
source .venv/bin/activate    # or .venv/bin/activate.csh
hermes --version
```

You should see a version banner.

---

## Configure the model

Hermes reads `~/.hermes/config.yaml`. Open it and point it at your
local model server:

```yaml
model:
  default: mlx-community/gemma-3-12b-it-4bit
  provider: custom
  context_length: 32768
  base_url: http://127.0.0.1:8765/v1
```

(For Ollama: `base_url: http://127.0.0.1:11434/v1` and use the
Ollama model name like `gemma2:9b`.)

`provider: custom` is Hermes's shorthand for "any
OpenAI-compatible endpoint." There are other provider names for
shortcuts to Anthropic/OpenAI/etc., but `custom` is what you want
for local.

---

## Say hello

```bash
hermes
```

A TUI opens. Type:

```
Hi. What model are you?
```

Press Enter. You'll see the model think, then answer. Congratulations
— you have an agent.

Try:

```
List the files in /tmp.
```

This time the model will call a tool (`shell` or `bash` depending on
the version). Hermes shows you the tool call, runs it, shows the
result, and the model continues from there.

Quit with `Ctrl-D` or `/exit`.

---

## What just happened, in 30 seconds

1. `hermes` started the TUI and opened a new session.
2. It built a system prompt (your config, available tools, any
   skills auto-loaded).
3. Your message was appended; the conversation was sent to your
   local model server.
4. The model decided "this needs the shell tool" and returned a
   tool-call JSON.
5. Hermes dispatched the tool call (ran `ls /tmp`).
6. Result appended to the conversation, model called again.
7. Model returned a final non-tool message ("Here are the files…").
8. TUI rendered the answer.

That's the four-piece loop from lesson 01, in production.

---

## Where the state lives

```bash
ls -la ~/.hermes/
```

Key entries:

| Path | What it is |
|---|---|
| `config.yaml` | Settings (model, provider, etc.) |
| `.env` | Secrets (bot tokens, etc.) |
| `sessions/` | SQLite session storage (full conversation history) |
| `kanban.db` | Task board (lesson 05) |
| `logs/` | Gateway and agent logs |
| `cron/` | Scheduled jobs (lesson 06) |
| `skills/` | User skills (lesson 04) |

Open the sessions DB:

```bash
sqlite3 ~/.hermes/sessions/sessions.db ".tables"
sqlite3 ~/.hermes/sessions/sessions.db \
  "SELECT id, model, created_at FROM sessions ORDER BY created_at DESC LIMIT 5;"
```

Every conversation is in there. Lesson 09 covers searching it with
FTS5.

---

## Slash commands

Inside the TUI:

- `/help` — list all commands
- `/model <alias-or-id>` — switch model mid-conversation
- `/skills` — show loaded skills
- `/save` — persist the conversation right now
- `/new` — start a fresh session
- `/exit` — quit

The slash command registry is the single source of truth (in
`hermes_cli/commands.py`) — the CLI, Telegram menu, Slack, and
dashboard all derive their command lists from the same place.

---

## Model aliases

In `config.yaml` you can define shortcuts:

```yaml
model_aliases:
  fast:
    model: mlx-community/gemma-3-12b-it-4bit
    provider: custom
    base_url: http://127.0.0.1:8765/v1
  big:
    model: mlx-community/gemma-3-27b-it-4bit
    provider: custom
    base_url: http://127.0.0.1:8765/v1
  cloud:
    model: anthropic/claude-sonnet-4.6
    provider: openrouter      # requires API key in .env
```

Then `/model fast` or `/model big` to switch on the fly. Useful for
when you want to A/B a hard prompt between local and cloud.

---

## Pitfalls

- **Wrong interpreter.** If `which hermes` points to something other
  than `~/agents101/.venv/bin/hermes` (or wherever your venv is),
  you'll be running an old install. `pip list | grep hermes` to
  confirm. Symlink or `alias hermes=...` to fix.
- **Forgot to activate the venv.** Same as above. The shebang on
  the `hermes` launcher is `#!/usr/bin/env python3` — whichever
  python is first in PATH wins.
- **Stale `~/.hermes/config.yaml`.** Old configs may reference
  models that no longer exist, or providers you've removed. If
  Hermes complains at startup, this is the first place to look.
- **Tool calls return errors silently in the model output.** If
  you ask "list /nonexistent" the shell tool will return an error
  string; the model has to handle it. If you see weird answers,
  scroll up — the tool may have errored.

---

## Further reading

- `AGENTS.md` in the Hermes repo root — auto-injected into every
  agent's system prompt; defines the contract.
- `hermes_cli/main.py` — the CLI entry point; ~10,000 lines but
  well organized by subcommand.
- `run_agent.py` — the actual agent loop. Maybe 500 lines. Read it.

---

Next: [04-tools-and-skills.md](04-tools-and-skills.md) — give your
agent new abilities.
