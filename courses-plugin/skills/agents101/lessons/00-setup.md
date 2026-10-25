# Lesson 00 — Setup

## What you'll have at the end

A working Python 3.11 virtualenv, `uv` for package management,
Docker for the multi-agent labs, and a local model server ready
to talk to. We don't install Hermes itself yet — that's lesson 03.

Skip sections you already have. Do the **smoke tests** at the end
regardless.

---

## 1. Python 3.11 via `uv`

`uv` is a fast, single-binary Python package manager + virtualenv
manager. We use it instead of `pip` + `venv` because it's faster
and produces reproducible environments.

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# verify
uv --version
```

Why 3.11 specifically? Hermes-agent requires it, and most modern
agent frameworks have stopped supporting 3.10. You can have many
Python versions installed alongside; `uv` will pick the right one.

---

## 2. Docker

For lesson 10 (containers) and to run any agent in isolation.

- **macOS**: Install Docker Desktop or [OrbStack](https://orbstack.dev)
  (lighter, faster).
- **Linux**: Your distro's docker package; add yourself to the
  `docker` group so you don't need `sudo` for every command.

```bash
docker --version
docker run --rm hello-world
```

If `hello-world` prints a greeting, Docker is wired up.

---

## 3. A local model server

You need *something* that speaks the OpenAI-compatible HTTP API
(`POST /v1/chat/completions`). Two good options:

### Option A: MLX (Apple Silicon, fastest)

```bash
uv tool install mlx-lm
# Pick a model — start small to verify the path works
mlx_lm.server --model mlx-community/gemma-3-12b-it-4bit \
              --host 0.0.0.0 --port 8765
```

First run downloads the model (~10 GB for 12B 4-bit). Leave it
running in a terminal; we'll connect to it from later lessons.

### Option B: Ollama (cross-platform, easy)

```bash
# macOS
brew install ollama

# Pull a model and start the server
ollama pull gemma2:9b
ollama serve  # runs on http://localhost:11434
```

Ollama uses port `11434` by default; MLX we picked `8765`. Keep
that in mind for lesson 02.

### Smoke test (whichever you chose)

```bash
# MLX
curl -s http://127.0.0.1:8765/v1/models | jq

# Ollama
curl -s http://127.0.0.1:11434/api/tags | jq
```

You should see your model listed. If not, the server isn't up;
debug before continuing.

---

## 4. Make a project directory

```bash
mkdir -p ~/agents101 && cd ~/agents101
uv venv .venv --python 3.11
source .venv/bin/activate    # or activate.csh / activate.fish
```

Whenever a later lesson says "activate the venv," it means run
`source .venv/bin/activate` from this directory.

---

## 5. Telegram bot (skip until lesson 07 if you want)

You'll need this by lesson 07. Doing it now is fine:

1. In Telegram, message `@BotFather`. Send `/newbot`. Follow
   prompts. He gives you a token like `123456:ABC-DEF...`.
2. Save it somewhere — we'll put it in a `.env` file later.
3. Message `@userinfobot` to get your own numeric Telegram user
   ID (positive integer). This will be your `TELEGRAM_HOME_CHANNEL`.
4. Send your bot any message (e.g., `/start`) so the chat
   exists — the bot can't DM you until you've initiated.

---

## Pitfalls

- **`python3` resolves to whatever shows up first in PATH.** If
  you have multiple Pythons installed, things "work" until they
  don't. Always activate the venv before running anything; don't
  rely on global Python.
- **Model downloads can take an hour on a slow connection.** Start
  the download before you go make coffee. Future-you with a 4 G
  upload will laugh at this advice.
- **MLX is Apple-Silicon only.** Intel Mac users should pick Ollama.
- **Don't `pip install` into your system Python.** Always into a
  venv. If anything tells you to `sudo pip install`, ignore it
  and use `uv` instead.

---

## Further reading

- `uv` docs: https://docs.astral.sh/uv/
- MLX: https://github.com/ml-explore/mlx-examples/tree/main/llms
- Ollama: https://ollama.com/library
- Why we use uv (not pip): https://astral.sh/blog/uv

---

Next: [01-what-are-agents.md](01-what-are-agents.md).
