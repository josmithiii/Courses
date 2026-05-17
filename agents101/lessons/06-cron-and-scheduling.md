# Lesson 06 — Cron and Scheduling

## Objective

Schedule an agent to run on a recurring basis. Then learn when
*not* to involve an LLM at all — the `--no-agent` watchdog
pattern that runs a shell script and delivers its output.

---

## Two cron systems

Be aware of two distinct schedulers in this world:

1. **System cron / launchd.** OS-level. Survives reboots,
   doesn't care about Hermes.
2. **Hermes cron.** Lives in `~/.hermes/cron/`, runs inside the
   gateway daemon. Survives gateway restarts (if persisted) but
   *requires the gateway to be running*.

For agent jobs (prompts that produce model responses), use Hermes
cron — it knows how to deliver the result to Telegram, log it as
a session, etc.

For low-level system tasks (rotate logs, sync files), use system
cron.

---

## Schedule a Hermes job

```bash
hermes cron create --name hourly-chime --deliver telegram \
  "0 * * * *" "Print BONG once per hour."
```

Cron expression first, then the prompt. The job is now in
`~/.hermes/cron/`. Verify:

```bash
hermes cron list
```

You'll see `Next run` and the schedule. When the gateway's cron
ticker fires (every 60 s), it checks for due jobs and runs them.

The agent gets the prompt as a fresh conversation; the response
gets delivered to whatever `--deliver` says (`local`, `telegram`,
`discord`, `slack`, etc.).

---

## Trigger manually

Don't wait for the next tick:

```bash
hermes cron run <job_id>            # queue for next tick
hermes cron tick                    # fire all due jobs now
```

The `run` form is what the dashboard's lightning-bolt button does.

---

## The `--no-agent` pattern

Sometimes you don't want an LLM at all — you want a shell script
that produces stdout, delivered as a message. Examples:

- "How much disk free?" — `df -h | tail -1`
- "Any failed CI runs?" — `gh run list --status failed`
- "Fleet status?" — your custom oversight script (lesson 08)

For these, an LLM is wasteful (cost, latency, non-determinism).
The `--no-agent` flag tells Hermes: skip the LLM, just run this
script, deliver its stdout.

```bash
mkdir -p ~/.hermes/scripts
cat > ~/.hermes/scripts/disk_check.sh <<'EOF'
#!/bin/bash
df -h / | awk 'NR==2 {
  used=$5; gsub("%","",used);
  if (used+0 > 80) printf "DISK ALERT: / at %s%% full\n", used;
}'
EOF
chmod +x ~/.hermes/scripts/disk_check.sh

hermes cron create --name disk-check --deliver telegram \
  --no-agent --script disk_check.sh "*/30 * * * *"
```

Every 30 minutes, the script runs. **Empty stdout = silent.** Only
when disk exceeds 80% does anything go to Telegram.

This is the classic watchdog pattern: page on anomaly, silent on
normal. It's how lesson 08's overseer runs.

---

## Script semantics

Per `hermes cron create --help`:

> .sh/.bash files run via bash, everything else via Python.

So `disk_check.py` would run with `python3`. Convenient: write
your watchdog logic in whichever you prefer.

The script's `stdout` is the message. `stderr` is logged but not
delivered. `exit 0` is success regardless of output.

---

## Delivery targets

`--deliver` accepts:

| Target | What happens |
|---|---|
| `local` (default) | Stored in the session DB; visible in dashboard |
| `telegram` | Posted to `TELEGRAM_HOME_CHANNEL` |
| `discord` | Posted to your configured Discord channel |
| `slack` | Posted to your Slack home channel |
| `<platform>:<chat_id>` | Specific target |

You can also configure multiple deliveries by stacking jobs, or
write a wrapper script that itself fans out.

---

## The gateway must be running

`hermes cron list` will warn you if it isn't:

> ⚠  Gateway is not running — jobs won't fire automatically.

Start it:

```bash
hermes gateway start         # service install (recommended)
# OR
hermes gateway run           # foreground, see logs live
```

If the gateway is down, scheduled jobs sit idle. The dashboard's
"SCHEDULED" badge can be misleading — it just means "configured,"
not "actively ticking."

---

## A realistic schedule

A solo dev's Hermes-cron config might look like:

```bash
hermes cron create --name standup --deliver telegram \
  "0 9 * * 1-5" "Generate my standup using the standup-summary skill."

hermes cron create --name overseer --deliver telegram \
  --no-agent --script overseer_watchdog.sh "*/5 * * * *"

hermes cron create --name backup --deliver local \
  --no-agent --script backup.sh "0 3 * * *"

hermes cron create --name daily-review --deliver telegram \
  "0 18 * * 1-5" "Summarize what I did today based on git log."
```

A real LLM call at the bookends of the day, watchdog scripts in
between.

---

## Pitfalls

- **Stale state in the dashboard.** Cron list output and the
  dashboard's cron tab can show old "last error" lines until the
  job actually re-runs. Don't trust the badge; trust `cron list`
  output after a fresh tick.
- **`local` delivery means *not Telegram*.** A job that says
  "BONG" to local goes into the session DB and nowhere else.
  Newcomers expect "everything goes to Telegram"; it doesn't.
- **Cron jobs run as agents by default.** The LLM gets the
  *prompt* you wrote and produces a response. If the model is
  unavailable (server down, timed out), the job fails. Use
  `--no-agent` to avoid this entirely.
- **One model server, many cron jobs.** If five agent-based jobs
  fire simultaneously and your local model is single-threaded,
  most will time out. Stagger schedules (use minute offsets:
  `5 * * * *`, `15 * * * *`).
- **System cron and Hermes cron are independent.** Don't double-
  schedule the same task in both. The system-cron version would
  bypass Hermes entirely, missing the session logging and
  delivery niceties.

---

## Further reading

- `hermes cron --help` and `hermes cron create --help`
- `cron/scheduler.py` in the Hermes repo
- Lesson 08 builds the overseer that uses this pattern

---

Next: [07-messaging.md](07-messaging.md) — bidirectional Telegram
and friends.
