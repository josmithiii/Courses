# Lesson 10 — Docker for Agents

## Objective

Understand why agents run in containers, how to configure
Hermes's `docker-compose.yml`, and the host-vs-container path
gotcha that bites everyone exactly once.

---

## Why containers

Three reasons, in order of importance:

1. **Isolation of side effects.** An agent with shell access can
   `rm -rf`. In a container it can only `rm -rf` what you mount in.
2. **Reproducible environment.** "Works on my machine" disappears.
   The image declares its Python version, system packages,
   everything. Pull, run, identical behavior.
3. **Lifecycle hygiene.** `docker stop` always works. No
   leaked PIDs, no stuck pyenv shims, no half-killed daemons.

You can run Hermes on bare metal — most of this course did —
but for a production fleet, containers.

---

## Hermes's docker-compose

The repo ships `docker-compose.yml`. Three services:

```
hermes        # the agent runtime
gateway       # the messaging gateway (telegram/slack/etc.)
dashboard     # the web UI
```

A typical bring-up:

```bash
cd ~/agents101/Hermes
docker compose pull           # grab the latest images
docker compose up -d          # detached
docker compose ps             # confirm all healthy
```

Each container mounts `~/.hermes` → `/opt/data` so they all share
config, session DB, kanban DB, logs. From outside the containers
you read/write the same files on the host.

---

## The host-vs-container path trap

The number-one foot-gun. Your agent's shell tool runs *inside the
container*. Paths in tool calls are container paths, not host paths.

Example:

```
> Save a summary to /Users/me/notes.md
```

The agent calls `write_file("/Users/me/notes.md", ...)`. Inside
the container, `/Users/me` doesn't exist. The write fails.

Fix: either tell the agent to use container paths
(`/opt/data/notes.md`, which maps to `~/.hermes/notes.md` on the
host), or mount `/Users/me` into the container in compose:

```yaml
services:
  hermes:
    volumes:
      - $HOME:/host-home:ro       # host home, read-only, for context
```

Then the agent can read `/host-home/notes.md` and you read
`/Users/me/notes.md` — same file, two paths.

---

## Workspace mount

For multi-task work (lesson 05's kanban worktrees), mount a
dedicated workspace dir:

```yaml
services:
  hermes:
    environment:
      HERMES_WORKSPACE_DIR: /opt/workspace
    volumes:
      - ./.workspace:/opt/workspace
```

Now `--workspace dir:/opt/workspace/foo` in `hermes kanban create`
gives the worker a dir at `./.workspace/foo` on the host. You can
inspect what it's doing in real time with your normal file
browser.

---

## Talking to the host's MLX server

A container can't see `127.0.0.1:8765` on the host — that's a
different network namespace. Use the special hostname
`host.docker.internal` (Docker Desktop) or
`172.17.0.1` (Linux default bridge):

```yaml
services:
  hermes:
    environment:
      OPENAI_BASE_URL: http://host.docker.internal:8765/v1
```

If the MLX server is bound to `127.0.0.1`, you'll also need to
rebind it to `0.0.0.0` so containers can reach it. The mlx_lm.server
command for this:

```bash
mlx_lm.server --host 0.0.0.0 --port 8765 --model ...
```

That makes it reachable from any container on the host.

---

## Building your own image

If you want to add system packages or vendor a tool:

```dockerfile
# Dockerfile.custom
FROM nousresearch/hermes-agent:latest

# Add system packages
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Add a custom skill
COPY my-skills/ /opt/hermes/skills/custom/
USER hermes

# Keep the upstream entrypoint
```

```bash
docker build -f Dockerfile.custom -t my-hermes .
```

Then point compose at your image:

```yaml
services:
  hermes:
    image: my-hermes
```

---

## Volume permissions

The container runs as user `hermes` (UID 1000 by default). If you
mount a host dir owned by your user (UID 501 on macOS), writes
from the container may fail with permission errors.

Fix on macOS: Docker Desktop translates these automatically;
usually fine. On Linux: either run the container as your UID
(`user: 1000:1000`) or `chown` the mount.

---

## `docker logs` vs Hermes logs

Two layers:

- `docker logs -f hermes-agent-hermes-1` — the container's
  stdout/stderr. Useful for crashes or import errors.
- `tail -f ~/.hermes/logs/*.log` — Hermes's own log files,
  written *inside* the container but to the mounted volume, so
  visible from the host.

Both are useful, for different things. Container logs for
"the process died." Hermes logs for "the agent failed a tool
call."

---

## Restarting one service

If only the gateway is misbehaving:

```bash
docker compose restart gateway
docker compose logs -f gateway        # watch it come back
```

vs full bounce:

```bash
docker compose down
docker compose up -d
```

`down` removes containers (state survives in mounts). `restart`
keeps the container, just bounces the process.

---

## Pitfalls

- **Path mismatch (above).** The #1 cause of "the agent wrote
  the file but I can't find it."
- **Forgetting `--remove-orphans`.** When you delete a service
  from compose, the old container hangs around. `docker compose
  up -d --remove-orphans` cleans up.
- **Stale image.** `docker compose pull` pulls latest tags. If
  your compose specifies `image: ...:1.2.3`, you have to bump
  the tag manually.
- **`docker compose exec` runs as root by default.** Use
  `--user hermes` if you want to test as the agent's user.
- **Container UIDs vs host UIDs.** Permission errors on mounts
  usually trace here.
- **Docker on macOS uses a VM under the hood.** I/O is slower
  than bare metal. For dev loops with lots of file reads, the
  bare-metal Hermes setup may feel snappier.

---

## Further reading

- `docker-compose.yml` in the Hermes repo
- `docker/entrypoint.sh` — what runs when the container starts
- Docker volumes deep-dive:
  https://docs.docker.com/storage/volumes/

---

Next: [11-where-next.md](11-where-next.md) — where to go from
here.
