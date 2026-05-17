# Lesson 05 — Kanban: Multi-Agent Coordination

## Objective

Spawn a background worker agent via Hermes's kanban. Understand
the task lifecycle (ready → running → done/blocked) and the
claim-lock that prevents two workers from grabbing the same task.

---

## Why a task board?

When you want more than one agent doing more than one thing, you
need somewhere to put the work. You have three rough choices:

1. **A queue.** Workers pop, do the thing, push results. Good for
   throughput, bad for visibility ("what's actually running right
   now?") and resumability ("worker died — what was it doing?").

2. **A workflow engine.** Airflow, Temporal, Prefect. Excellent
   for known DAGs, overkill for "agent, go do this thing."

3. **A kanban.** Tasks have *status* (todo, running, done, blocked)
   and *assignees*. Workers claim a task, work it, update status.
   You see the full state at a glance.

Hermes picks the kanban for agents. It maps onto the human mental
model and gives you observability for free.

---

## The schema

`~/.hermes/kanban.db` (SQLite) has these tables:

| Table | Purpose |
|---|---|
| `tasks` | The work items themselves |
| `task_runs` | History of attempts (a task can be retried) |
| `task_events` | Audit log: created, claimed, completed, blocked |
| `task_links` | Parent → child task relationships |
| `task_comments` | Free-form annotations |
| `kanban_notify_subs` | Subscribers to event notifications |

Status values for a task: `triage, todo, ready, running, blocked,
done, archived`.

A task can be claimed by exactly one worker at a time, via a
`claim_lock` column with a `claim_expires` timestamp. If a worker
dies, the lock expires and the dispatcher can reclaim.

---

## Create a task

```bash
hermes kanban create "Write a haiku about agents" \
  --body "Three lines. 5/7/5. Topic: AI agents in a Docker container." \
  --max-runtime 5m
```

Output: `Created t_<hash> (ready, assignee=-)`.

Show it:

```bash
hermes kanban ls
hermes kanban show t_<hash>
```

It's `ready` but unassigned — the dispatcher won't claim
unassigned tasks. Assign:

```bash
hermes kanban assignees           # see available profiles
hermes kanban assign t_<hash> default
```

Dispatch:

```bash
hermes kanban dispatch
```

One sweep. Output tells you what was spawned, reclaimed, crashed,
etc. The worker is a separate process — `hermes -p default
--skills kanban-worker chat -q work kanban task t_<hash>` (look
for it in `ps -ef`).

Watch progress:

```bash
hermes kanban watch              # live event tail
hermes kanban show t_<hash>      # snapshot
```

When the worker is done it calls `kanban_complete` (or
`kanban_block` if it can't proceed), the dispatcher records the
result, and the task transitions to `done` (or `blocked`).

---

## The dispatcher

`hermes kanban dispatch` is one sweep. To make it continuous:

```bash
hermes kanban daemon             # foreground
# OR
hermes gateway run               # the gateway embeds the dispatcher
```

The gateway version runs every 60 s by default and is what you'll
typically use in practice. The standalone daemon is useful when
you don't want the rest of the gateway (Telegram polling, etc.)
running.

Per pass the dispatcher does:

1. Reclaim tasks whose worker died (PID gone or claim expired).
2. Spawn new workers for ready+assigned tasks, up to a concurrency
   cap.
3. Mark crashed/timed-out tasks; increment `consecutive_failures`.
4. Auto-block tasks that exceed the failure circuit breaker
   (default: 2 consecutive non-successes).

---

## Workspaces

Each task gets a workspace directory. Three modes via
`--workspace`:

- `scratch` (default): ephemeral dir under
  `~/.hermes/kanban/workspaces/t_<hash>/`. Cleaned on archive.
- `worktree`: a fresh git worktree of the current repo. Use for
  parallel branches.
- `dir:<path>`: a specific directory. Be careful — two workers
  in the same dir will clobber each other.

---

## Multi-step work via parent/child tasks

```bash
# Parent
parent=$(hermes kanban create "Implement feature X" --json | jq -r .id)

# Children
hermes kanban create "Design the API"          --parent $parent
hermes kanban create "Write the tests"         --parent $parent
hermes kanban create "Implement it"            --parent $parent
hermes kanban create "Update docs"             --parent $parent
```

`hermes kanban show $parent` shows the tree. The parent
auto-completes when all children are done.

---

## Heartbeats

A long-running task periodically writes `last_heartbeat_at` so an
oversight system can tell "this is still alive" vs "this is hung."
The worker calls `kanban_heartbeat` on its own schedule (typically
every 30–60 s).

In lesson 08 we'll build a watchdog that pages you when a task's
heartbeat goes stale.

---

## A real session example

```bash
$ hermes kanban create "Sieve of Eratosthenes demo" \
    --body "Print primes <= 1000. Call kanban_complete when done." \
    --max-runtime 5m
Created t_f859a729  (ready, assignee=-)

$ hermes kanban assign t_f859a729 default
Assigned t_f859a729 to default

$ hermes kanban dispatch
Spawned: 1
  - t_f859a729  ->  default  @ /Users/jos/.hermes/kanban/workspaces/t_f859a729

$ sleep 30 && hermes kanban show t_f859a729 | grep status
  status:    running

$ sleep 120 && hermes kanban show t_f859a729 | grep status
  status:    done
```

That's the full happy path.

---

## Pitfalls

- **Unassigned tasks never run.** The dispatcher only spawns
  assigned + ready tasks. New users hit this immediately.
- **One MLX server = one inference at a time.** Spawning N
  workers against the same local model server serializes them.
  Plan accordingly; if you need parallelism, you need parallel
  model servers (or a cloud model).
- **Tasks that never heartbeat aren't easy to monitor.** The
  schema allows `last_heartbeat_at IS NULL`. A worker that dies
  before its first heartbeat looks the same as a worker that
  legitimately hasn't started. Lesson 08 addresses this.
- **`--max-runtime` is your friend.** Without it, a runaway
  worker keeps the task `running` until you intervene. Pick a
  generous-but-finite cap.
- **The dispatcher runs reclaim only when invoked.** No daemon
  = no automatic recovery. The gateway runs it for you; if you
  don't run the gateway, you need `hermes kanban daemon`.

---

## Further reading

- `hermes_cli/kanban_db.py` — the schema and CAS logic
- `hermes kanban --help` — every subcommand
- Lesson 08 builds a watchdog that probes this DB

---

Next: [06-cron-and-scheduling.md](06-cron-and-scheduling.md) —
make agents run on a schedule.
