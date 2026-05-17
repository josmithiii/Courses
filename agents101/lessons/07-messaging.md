# Lesson 07 — Messaging Gateways

## Objective

Wire Telegram into your fleet so you can:

- Send messages out from any script (`hermes notify`).
- Receive messages and have an agent reply (gateway running).

Understand the asymmetry: outbound is easy and standalone;
inbound requires the gateway daemon.

---

## The two directions

| Direction | Needs gateway? | How |
|---|---|---|
| Hermes → you | No | One-shot HTTPS to Telegram Bot API |
| You → Hermes (DM the bot) | **Yes** | Gateway polls for inbound updates |

Why? The bot API is request/response for sending — any process can
POST a message. For receiving, somebody has to be running long-poll
or hosting a webhook. That's the gateway.

If you only ever need outbound (cron alerts, scripts pinging you),
you don't need the gateway. If you want to chat with your agent in
Telegram, you do.

---

## Configure Telegram

You already have a bot token and your user ID from lesson 00.
Put them in `~/.hermes/.env`:

```bash
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_HOME_CHANNEL=123456789       # your user ID = chat ID for the bot's DM
```

`TELEGRAM_HOME_CHANNEL` is where outbound messages go when no
explicit target is given. For DMing the bot, this is your Telegram
user ID (numeric, positive).

To find your ID:

- DM `@userinfobot` and it tells you, OR
- After sending the bot a message, `curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates" | jq '.result[-1].message.chat.id'`

---

## Outbound: `hermes notify`

```bash
hermes notify "hello from the shell"
```

Goes to `TELEGRAM_HOME_CHANNEL`. You can also:

```bash
hermes notify --to -1001234567890 "to a specific group"
hermes notify --to -1001234567890:42 "to topic 42 in a forum supergroup"
echo "$(date)" | hermes notify -          # body from stdin
```

This is the cleanest path for cron alerts, post-build hooks,
"something interesting happened" pings. No agent, no gateway, no
session record — just a message.

Under the hood it's a wrapper around the existing
`tools.send_message_tool._send_telegram` helper that the gateway
itself uses; same MarkdownV2 / HTML formatting.

---

## Inbound: starting the gateway

```bash
hermes gateway install        # install as user service (macOS launchd / systemd)
hermes gateway start          # start it
hermes gateway status
```

On macOS, this creates `~/Library/LaunchAgents/ai.hermes.gateway.plist`
and registers it. The gateway:

- Connects to every enabled platform in `.env` (Telegram, Slack,
  Discord, etc.)
- Polls for inbound messages and dispatches them to the agent
- Runs the embedded kanban dispatcher (every 60 s)
- Runs the cron ticker (every 60 s)

Once it's running, DM your bot:

> What can you do?

The bot replies. It's a Hermes agent over Telegram. Tool calls,
streaming, the whole deal.

---

## Telegram slash commands

The gateway registers Hermes's slash commands with Telegram so
they appear in the bot's `/` menu (up to Telegram's 100-command
limit). `/help`, `/model`, `/skills`, etc. work in Telegram the
same as in the TUI.

---

## Other platforms

Slack:

```bash
# .env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
SLACK_HOME_CHANNEL=C012345678
```

Setup involves creating a Slack app with the right scopes
(`chat:write`, `app_mentions:read`, etc.). `hermes slack manifest`
prints a manifest you can paste into the Slack app creator. After
that, restart the gateway; Slack appears in the connected platforms.

Other adapters in `gateway/platforms/`: discord, signal, whatsapp,
matrix, email, sms, bluebubbles (iMessage on macOS), feishu,
mattermost, dingtalk, qqbot, weixin, yuanbao, wecom, … you get
the idea. All optional — pick what you actually use.

---

## Identity and permissions

By default, anyone who messages your bot can talk to your agent.
You probably don't want that. Restrict via:

```bash
# .env
TELEGRAM_ALLOWED_USERS=123456789,987654321     # comma-separated user IDs
TELEGRAM_ALLOWED_USERS=*                       # allow anyone (default if unset)
```

For Slack, similar `SLACK_ALLOWED_USERS=U012,U034` works.

For shared bots with multiple authorized users, Hermes will
isolate sessions per user (lesson 09 has the dashboard view).

---

## Streaming reasoning into chat

Hermes can mirror the agent's thinking (tool calls, intermediate
steps) into chat as it happens. Configure via `~/.hermes/config.yaml`:

```yaml
display:
  show_reasoning: true
  streaming: true
```

In Telegram this manifests as message edits — the bot posts a
placeholder, then keeps editing it as the agent makes progress.
Telegram has a rate limit on message edits, so very long agent
turns will slow down. For most cases it works well.

---

## The `send_message` tool (from inside the agent)

When the agent itself wants to message someone (not just respond
to its current chat), it uses the `send_message` tool:

```
> Tell jos that the build is done via telegram.
```

The agent calls `send_message(target="telegram", message="...")`
internally. Target syntax is the same as `hermes notify --to`.
Useful for tasks like "ping me when the test suite finishes."

---

## Pitfalls

- **`hermes notify` works even when the gateway is down.** It
  doesn't need the gateway at all. Useful for paging *about*
  the gateway being down.
- **The gateway is a single instance.** Two gateways for the
  same Telegram bot will both try to long-poll and Telegram
  will reject one. The `--replace` flag in `hermes gateway run`
  handles the takeover.
- **"Bot can't initiate DMs."** Telegram requires the user to
  message the bot first. If you've never sent your bot a
  message, even outbound `hermes notify` to your user ID will
  fail with "chat not found." Send `/start` once.
- **Markdown vs HTML vs MarkdownV2.** Telegram has three. Hermes
  auto-detects HTML tags and otherwise uses MarkdownV2. Don't
  send raw `*` characters thinking they'll bold; they won't —
  use `**bold**` markdown and let Hermes convert.
- **iMessage requires a macOS-side bridge.** Use BlueBubbles
  (`gateway/platforms/bluebubbles.py`) and run the BlueBubbles
  server on a Mac that's always on.

---

## Further reading

- `gateway/platforms/` — every adapter, ~25 of them
- `tools/send_message_tool.py` — outbound surface
- `hermes_cli/notify.py` — the standalone CLI we built in lesson 08

---

Next: [08-oversight.md](08-oversight.md) — building a watchdog.
