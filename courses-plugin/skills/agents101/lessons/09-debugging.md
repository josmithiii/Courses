# Lesson 09 — Debugging Agent Systems

## Objective

When something breaks (and it will), know where to look. This
lesson is a tour of the layers, ordered from closest-to-the-symptom
to deepest-in-the-stack.

---

## The seven places state lives

Roughly, in order of where you'll look first:

1. **Dashboard sessions tab** — the rendered conversation.
2. **`~/.hermes/sessions/sessions.db`** — the SQLite source of
   truth for conversations.
3. **`hermes kanban show <task>`** — task lifecycle events.
4. **`~/.hermes/kanban.db`** — the SQLite source of truth for
   tasks.
5. **`~/.hermes/logs/gateway.log` and `gateway.error.log`** —
   gateway-side logs.
6. **`~/.hermes/logs/agent.log` and `errors.log`** — agent-side
   logs (rolled, see `.1`, `.2`, `.3` for history).
7. **`docker logs <container>` or `ps -ef`** — kernel-level
   ground truth.

You'll spend most of your time in 2 (sessions DB) and 5/6 (logs).

---

## "My agent gave a weird answer"

```bash
hermes dashboard         # http://127.0.0.1:9119/sessions
```

Click the most-recent session. You'll see the full conversation
including system prompt, tool calls, and tool results. 90% of
"weird answer" debugging is finding that the model called a
tool and got an unexpected result, and the answer was downstream
of that.

If the dashboard is up but the session isn't showing recent
activity, the session may be cached by your browser. Refresh.

---

## "My agent is silent / hung"

Three possible causes:

1. **Model server unreachable.** Check
   `tail -20 ~/.hermes/logs/agent.log` for retry/timeout lines.
   `curl -s http://127.0.0.1:8765/v1/models` to confirm it's up.
2. **Gateway dispatcher stuck.** `ps -ef | grep gateway` to
   confirm the daemon is alive. `tail ~/.hermes/logs/gateway.log`
   for the last activity timestamp.
3. **Local model is just slow.** 70B-bf16 generating 1000 tokens
   on an M1 takes a while. Patience or use a smaller model.

---

## "Cron isn't firing"

```bash
hermes cron status
```

Almost always: gateway is down. The cron ticker lives inside the
gateway. Start the gateway and the ticker resumes.

If the gateway *is* up and cron still isn't firing:

```bash
hermes cron list        # check next_run
hermes cron tick        # force-fire all due jobs
```

If `cron tick` fires but the job errors, look at
`gateway.error.log` for the traceback.

---

## "Kanban task stuck in `running` with dead worker"

The story from lesson 08:

```bash
# Inspect
sqlite3 ~/.hermes/kanban.db \
  "SELECT id, status, worker_pid, last_heartbeat_at FROM tasks WHERE status='running';"

# For each worker_pid: is it actually alive?
ps -p <worker_pid>
```

If `ps` shows no process for that PID, the worker died. Two
recovery paths:

1. **Run dispatch** — the reclaim step will notice and re-spawn
   (or auto-block after enough failures):
   ```bash
   hermes kanban dispatch
   ```
2. **Manually block** if you know the task will keep failing:
   ```bash
   hermes kanban block t_xxxx "model server unreachable"
   ```

The lesson-08 watchdog won't catch this case unless you add the
`stuck_running` probe (see the "what this misses" section there).

---

## "Two workers, same MLX server, everything times out"

A common foot-gun on local-model setups. MLX serves one inference
at a time. Spawn N concurrent agents and (N-1) of them queue. If
your `OVERSEER_DOCKER_LOOKBACK` is shorter than the queue depth,
you get cascading timeouts.

Diagnostic: `tail -f ~/.hermes/logs/errors.log` while it's
happening — you'll see `APITimeoutError` from multiple threads
with the same `base_url`.

Solutions, in order of effort:

1. **Don't run that many concurrent agents.** Set kanban
   concurrency to 1 if you only have one model server.
2. **Run multiple model servers** on different ports (and different
   models, if you have the RAM).
3. **Use a hosted model** for the housekeeping jobs (chime, cron
   summaries) and reserve local for the heavy work.

---

## "Dashboard says gateway STOPPED but it's running"

Real bug. The dashboard reads `~/.hermes/gateway_state.json` for
status, but the gateway only updates that file on platform-state
*changes* — not as a heartbeat. After 10 minutes of "no news" the
dashboard's "stale-state" threshold considers it stopped.

Verify:

```bash
ps -ef | grep "gateway run" | grep -v grep
tail -5 ~/.hermes/logs/gateway.log
cat ~/.hermes/gateway_state.json | jq .gateway_state
```

If `ps` shows a process and `gateway_state` says "running," the
gateway is fine. The dashboard is just stale.

---

## "The OpenAI-package error in a cron job"

The classic post-venv-migration issue: you set up a `.venv` for
the new Python 3.11, but the gateway daemon (or dashboard) is
still running under the old miniforge3 Python. The cron job tries
`from openai import ...` and the old interpreter doesn't have it.

Fix: restart everything from inside the activated `.venv`:

```bash
source .venv/bin/activate
hermes dashboard --stop && hermes dashboard
hermes gateway restart
```

Always sanity-check the daemon's interpreter with:

```bash
ps -ef | grep "gateway run" | grep -v grep
# Should show .venv/bin/python in the path
```

---

## Searching the session DB

Hermes sessions have FTS5 full-text search:

```bash
sqlite3 ~/.hermes/sessions/sessions.db <<EOF
SELECT session_id, snippet(messages_fts, -1, '[', ']', '...', 8)
FROM messages_fts
WHERE messages_fts MATCH 'kanban_complete'
LIMIT 10;
EOF
```

For when you need to find "that one conversation where the model
got confused about X."

---

## When all else fails: turn up the logs

Hermes uses Python's `logging`. The default is INFO. To get DEBUG
for one module:

```bash
HERMES_LOG_LEVEL=DEBUG hermes gateway run
# or per-logger:
PYTHONPATH=. python -m hermes_cli.main --log-level DEBUG ...
```

`DEBUG` is loud. Pipe through `grep` for the module you care about.

---

## Pitfalls

- **Don't trust badges or summaries.** Always confirm with the
  underlying data (DB, process table, log file).
- **Don't `rm` state directories to "reset."** That kills your
  session history. If you must, copy first.
- **Don't assume errors propagate.** Tool errors often come back
  as ordinary text in the session; the model decides whether to
  retry or give up. Read the messages, not just the dashboard
  state.
- **Don't grep the wrong log.** `agent.log` is per-conversation
  detail. `gateway.log` is daemon lifecycle. `errors.log` is the
  cross-component error sink. Match the right log to the symptom.

---

## Further reading

- `hermes_state/` and `hermes_cli/sessions.py`
- `gateway/run.py` — where most "gateway is up" diagnostics live
- The Python `logging` HOWTO if you've never tuned a log level
  in earnest

---

Next: [10-docker.md](10-docker.md) — running the fleet in
containers.
