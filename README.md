# Courses

A growing collection of self-paced, daily, tutor-style courses run through
[Claude Code](https://claude.com/claude-code). Each course is a self-contained
folder with its own curriculum, progress tracker, daily lesson logs, and a
`/lesson` slash command that runs an interactive ~1-hour session with an AI tutor
that teaches one concept at a time and verifies understanding with small exercises.

## Courses

| Course | Status | What it covers |
|--------|--------|----------------|
| [`ai-foundations/`](ai-foundations/) | 🟢 Active | From the Multilayer Perceptron up to modern LLMs — backprop, PyTorch, CNNs, Transformers, LLMs, Diffusion. Intuition-first, beginner-friendly. |
| `claude-code-and-tools/` | ⚪ Planned | Using Claude Code effectively: commands, hooks, skills, MCP, subagents, scheduled/remote agents. |
| `claude-app/` | ⚪ Planned | Getting the most out of the Claude app: projects, connectors, workflows. |
| _more to come_ | ⚪ Planned | |

## How a course works

Each course folder contains:

- `curriculum.md` — the full syllabus and the teaching method.
- `progress.md` — durable state: what's mastered, what's next (the tutor reads this first).
- `lessons/YYYY-MM-DD.md` — one log per day (lesson content, exercises, your answers).
- `.claude/commands/lesson.md` — the `/lesson` command that runs the live session.
- `CLAUDE.md` — context that tells any Claude Code session how to act as the tutor.

### To take a course

```bash
cd Courses/<course-folder>
claude          # start Claude Code in the course folder
/lesson         # begin (or resume) today's ~1-hour session
```

An optional daily 11:00 reminder can be wired up (local macOS notification and/or
a Slack DM) so the day's session is easy to remember — see the course folder.

## Authoring a new course

Copy an existing course folder as a template, replace `curriculum.md` with the new
syllabus, reset `progress.md`, empty `lessons/`, and adjust `CLAUDE.md` for the new
subject. The `/lesson` command and teaching loop are reusable as-is.
