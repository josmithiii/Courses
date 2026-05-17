# Lesson 08 — Oversight

## Objective

Build a polling watchdog that paged us during the very day this
course was written: when a kanban task crashes, blocks, or stalls,
the operator gets a Telegram alert. Understand what kanban
*doesn't* tell you, and how to fill that gap with ~200 lines of
Python.

This lesson is the most "real" in the course. It documents the
artifact the student is about to build, along with the bugs and
holes we hit on the way.

---

## The problem

Dashboards are pull-only. You have to remember to look. When
something silently breaks at 3am, you find out at 9am — if you're
lucky.

What we want: **a push channel that pages us when something is
wrong, and stays silent when it isn't**.

What we have:

- Kanban DB (`~/.hermes/kanban.db`) with tasks, statuses, events.
- Docker (`docker ps -a`) showing container lifecycles.
- A working outbound `hermes notify` (lesson 07).

What we need: a loop that combines those into alerts.

---

## The watchdog pattern (recap)

From lesson 06: a `--no-agent` Hermes-cron job runs a shell script
every N minutes. **Empty stdout = silent.** Stdout with content gets
delivered to Telegram.

So our overseer becomes: "a script that prints alert lines when
something is wrong, prints nothing otherwise."

---

## What to alert on

Three kinds of anomaly, in order of how easy they are to detect:

1. **Container exited non-zero recently.** `docker ps -a` plus
   `docker inspect --format '{{.State.FinishedAt}}'` for the
   timestamp.
2. **Kanban task with stale heartbeat.** Task is `running` but
   `last_heartbeat_at` is older than N minutes — worker is
   probably hung.
3. **Kanban task is `blocked`.** The circuit breaker tripped or
   something explicitly blocked it. You should know.

Each anomaly becomes an `Alert(kind, subject, summary)`.

---

## Dedup

Run the loop every 5 minutes and a stuck task will alert you
60 times in 5 hours. We don't want that.

Solution: a tiny JSON file at `~/.hermes/overseer-seen.json`
mapping `SHA1(kind|subject)` → last-paged epoch. Skip alerts
where last_paged is within a configurable window (default 6 h).

This is a stateless watchdog *almost*. The only state is "have I
recently paged about this exact incident."

---

## The script

The full script is in the Hermes repo at
`scripts/agent_overseer.py` — ~200 lines, stdlib-only (no extra
deps). The shape:

```python
@dataclass(frozen=True)
class Alert:
    kind: str           # "container_exit" | "stale_heartbeat" | "blocked_task"
    subject: str
    summary: str
    def dedup_key(self) -> str: ...

def probe_docker() -> Iterable[Alert]: ...
def probe_kanban() -> Iterable[Alert]: ...
def page(alerts: list[Alert]) -> None: ...

def main() -> int:
    seen = load_seen()
    fresh = [a for a in (*probe_docker(), *probe_kanban())
             if a.dedup_key() not in seen]
    page(fresh)
    save_seen(seen | {a.dedup_key(): now() for a in fresh})
```

Read the full source. It's deliberately boring code.

---

## Wire it into Hermes cron

```bash
# Wrapper that runs in stdout-only mode (so cron delivers via Telegram)
cat > ~/.hermes/scripts/overseer_watchdog.sh <<'EOF'
#!/bin/bash
export OVERSEER_DRY_RUN=1
exec python3 /path/to/Hermes/scripts/agent_overseer.py 2>&1 \
    | grep -v 'kanban db missing' || true
EOF
chmod +x ~/.hermes/scripts/overseer_watchdog.sh

hermes cron create --name overseer --no-agent --deliver telegram \
  --script overseer_watchdog.sh "*/5 * * * *"
```

`OVERSEER_DRY_RUN=1` makes the script print alerts to stdout
instead of trying to call `hermes notify` itself (Hermes cron is
already taking care of delivery).

The `grep -v` filters a benign "kanban db missing" message that
fires before you've created any tasks. The `|| true` makes empty
output exit 0 (otherwise grep returns 1 when nothing matches).

---

## Tunables (all env vars)

```
HERMES_HOME=/Users/you/.hermes
HERMES_KANBAN_DB=$HERMES_HOME/kanban.db
OVERSEER_STALE_HB=900                # 15 min
OVERSEER_DOCKER_LOOKBACK=1800        # 30 min
OVERSEER_DEDUP_WINDOW=21600          # 6 h
OVERSEER_WATCH_PREFIXES=hermes,oc    # container name prefixes
OVERSEER_DRY_RUN=1                   # print, don't notify
```

Override per-job by exporting in the wrapper script. Override per
test by passing them on the command line.

---

## Test it

Force an alert by blocking a task:

```bash
hermes kanban create "Trigger an alert" --max-runtime 1m
# (assign + dispatch — let it run and fail or block manually)
hermes kanban block t_<hash> "deliberate test"

# Run the watchdog manually
~/.hermes/scripts/overseer_watchdog.sh
```

You should see something like:

```
[overseer] 1 new alert(s):
  - task t_xxxx (default) BLOCKED: Trigger an alert — deliberate test
```

…and within 5 minutes (or after the next manual `hermes cron tick`),
that message arrives on Telegram.

Run it a second time immediately — silent. Dedup is working.

---

## What this misses

The blind spots, deliberately exposed:

- **Workers that die before their first heartbeat.** The
  stale-heartbeat probe requires `last_heartbeat_at IS NOT NULL`.
  A worker that crashes on startup never writes a heartbeat,
  stays `running` forever, and the watchdog never alerts. We hit
  this in lesson 09's debugging story.
- **Host-process liveness.** Kanban workers are host processes,
  not containers. `docker ps` doesn't see them. A natural
  extension: a `stuck_running` probe that checks
  `os.kill(worker_pid, 0)` on every `running` task.
- **External services.** Your MLX server crashing isn't on the
  list. Easy fix: add an HTTP probe.
- **Subjective alerts.** "This agent ran but produced nonsense."
  Watchdog can't tell. That's the model's job; LLM-judge a
  sample of outputs in a separate cron if you care.

Each gap is a 20-line addition. The architecture extends cleanly.

---

## Why this is a useful exercise

You learn:

1. **How to read the kanban DB directly.** Operators who can
   write SQL against `kanban.db` debug 10× faster than those who
   only know the CLI.
2. **The `--no-agent` watchdog idiom.** Reusable for any
   "page on anomaly" use case — disk full, CI failing, certs
   expiring.
3. **Dedup discipline.** The window-and-hash pattern is the same
   approach used by PagerDuty, Sentry, every monitoring tool. You
   built a tiny one from scratch.
4. **Failure-mode imagination.** Listing what the watchdog
   *doesn't* catch is half the value. Every monitoring system is
   really a list of "we know about these failures; everything
   else is silent."

---

## Tests

The script ships with `tests/scripts/test_agent_overseer.py`:
11 cases covering every probe, the lookback / prefix / zero-exit
filters, dedup, and bad-env paths. Run them:

```bash
cd ~/agents101/Hermes
pytest tests/scripts/test_agent_overseer.py -v -o addopts=""
```

The tests stub `subprocess.run` (for docker) and use a real on-disk
SQLite (for kanban). They're a good template for any host-side
monitoring script you write.

---

## Pitfalls

- **`docker inspect` timestamps are 9-digit nanoseconds.** Python
  3.10's `datetime.fromisoformat` rejects them; the script
  swallows the parse error and treats the container as
  "unknown age" → silently ignored. Tightened in tests; in
  production you may want to fail-loud here.
- **Sqlite WAL mode is mandatory for concurrent reads.** Default
  Hermes uses WAL. If you don't, your read-only probe can block
  the writer. Don't disable WAL.
- **The watchdog has no idea what *good* looks like.** It only
  knows what *bad* looks like. Keep extending the bad list.
- **One-shot is fine.** Don't turn this into a daemon. A
  stateless 5-minute cron is simpler than a long-running process
  with its own restart story.

---

## Further reading

- `scripts/agent_overseer.py` in the Hermes repo
- `ClaudeCodeOrchestrationGuide.md` in the same repo — the
  setup-narrative companion
- Tests at `tests/scripts/test_agent_overseer.py`

---

Next: [09-debugging.md](09-debugging.md) — when oversight fires
and you have to actually figure out what's wrong.
