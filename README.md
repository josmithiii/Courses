# Courses

A growing collection of self-paced, daily, tutor-style courses run through
[Claude Code](https://claude.com/claude-code). Each course is a self-contained
folder with its own curriculum and a `/lesson` slash command that runs an
interactive ~1-hour session with an AI tutor — teaching one concept at a time and
verifying understanding with small exercises.

**Course content vs. learner state are deliberately separated.** This repo holds
only shipped, version-controlled course content (read-only at runtime). Each
learner's personal progress and lesson journal live *outside* the repo, so the
repo stays pristine and the system is multi-user / web-app ready (a future web app
just repoints the data location per user — see "Architecture" below).

## Courses

| Course | Status | What it covers |
|--------|--------|----------------|
| [`ai-foundations/`](ai-foundations/) | 🟢 Active | From the Multilayer Perceptron up to modern LLMs — backprop, PyTorch, CNNs, Transformers, LLMs, Diffusion. Intuition-first, beginner-friendly. |
| [`agents101/`](agents101/) | 🟢 Active | Operator-level training on local AI agents: run, extend, coordinate, schedule, message, oversee, debug, containerize. Hermes-agent as case study. Hands-on; ~12 sessions. |
| [`ai-miracle-decade-plus/`](ai-miracle-decade-plus/) | 🟢 Active | Self-paced traversal of 40 landmark AI papers (2006 → 2023) — DBN through GPT-4, with cross-cutting concept-page stops. No time budget; side quests first-class. Links to arXiv + the music423-2023 meta-wiki. |
| `claude-code-and-tools/` | ⚪ Planned | Using Claude Code effectively: commands, hooks, skills, MCP, subagents, scheduled/remote agents. |
| `claude-app/` | ⚪ Planned | Getting the most out of the Claude app: projects, connectors, workflows. |
| _more to come_ | ⚪ Planned | |

## Architecture

**Content (this repo — versioned, read-only at runtime).** Each course folder:

- `curriculum.md` — the full syllabus and the teaching method.
- `progress.template.md` — the seed tracker, copied to the learner's data dir on first run.
- `.claude/commands/lesson.md` — the `/lesson` command that runs the live session.
- `CLAUDE.md` — context that tells any Claude Code session how to act as the tutor.

**Learner state (outside the repo — personal, per-user, never committed).**
Resolved as `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/<course>/`:

- `progress.md` — durable state: what's mastered, what's next (the tutor reads this first).
- `lessons/YYYY-MM-DD.md` — one log per day (lesson content, exercises, your answers).

`COURSES_DATA_DIR` is the single seam for going multi-user: a web app sets it to a
per-user directory/object store and nothing else changes. On a fresh machine the
`/lesson` command auto-seeds `progress.md` from `progress.template.md`.

### To take a course

```bash
cd Courses/<course-folder>
claude          # start Claude Code in the course folder
/lesson         # begin (or resume) today's ~1-hour session
```

An optional daily 11:00 reminder can be wired up (local macOS notification and/or
a Slack DM) so the day's session is easy to remember — see the course folder.

## Authoring a new course

Copy an existing course folder, replace `curriculum.md` with the new syllabus,
adjust `progress.template.md` and `CLAUDE.md` for the new subject, and update the
course id used in that course's `.claude/commands/lesson.md`. No personal state to
reset — it never lived in the repo. The `/lesson` command and teaching loop are
reusable as-is.
