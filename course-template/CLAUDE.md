# {{COURSE-ID}} -- project context

This is the `{{COURSE-ID}}` course inside the public **Courses** repo (`..`).
{{ONE-LINE SCOPE}}
Adapt to the learner profile recorded in their `progress.md` -- don't assume their level.

## Content vs. learner state (architecture)
Shipped course **content** is versioned in this repo and is read-only at runtime.
Personal **learner state** lives OUTSIDE the repo so the repo stays pristine and the
system is multi-user / web-app ready.

- **Content (repo):** `curriculum.md` (syllabus + teaching method),
  `progress.template.md` (seed copied on first run), `.claude/commands/lesson.md`,
  this file.
- **Learner state (NOT in repo):** under `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/{{COURSE-ID}}/`
  -- `progress.md` (durable tracker, read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs). `COURSES_DATA_DIR` is the seam a future
  web app overrides to point at a per-user store.

Never write personal progress into the repo. The `/lesson` command has the exact
read/seed/write steps.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Working with the learner
Be patient, friendly, analogy-first. One concept at a time. Always verify a concept
with a small exercise before advancing. Never rush past something unverified.
Keep sessions ~1 hour. Always update the data-dir `progress.md` and the day's
lesson file at the end.
