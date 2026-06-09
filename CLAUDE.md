# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is a **content repository**, not a software project: a collection of self-paced,
tutor-style courses run through Claude. There is **no build, test, or lint step** — the
"code" is Markdown course content plus one Bash launcher (`take`). Don't go looking for a
test suite or package manifest. See [`README.md`](./README.md) for the full course list and
the user-facing overview; this file is the operator's guide for acting inside the repo.

## The one rule that matters most

**Course content and learner state are separate, and learner state never enters this repo.**

- **Content** (in the repo, versioned, read-only at runtime): each course's `syllabus.md`,
  `progress.template.md`, `.claude/commands/lesson.md`, and `CLAUDE.md`.
- **Learner state** (outside the repo, per-user, never committed): resolved as
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/<course>/`, containing `progress.md`
  (durable tracker) and `lessons/YYYY-MM-DD.md` (per-day logs).

`COURSES_DATA_DIR` is the single seam for going multi-user (a web app repoints it per user).
When running a lesson you READ and WRITE learner state under the data dir; you NEVER write a
learner's progress into the repo. The exact read/seed/write steps live in each course's
`lesson.md`.

## Running a course (any Claude front-end)

To run a course, read `<course>/.claude/commands/lesson.md` and follow it exactly, using the
learner-state location described above. In Claude Code this is the `/lesson` slash command (or
`./take <course>` from the repo root, which `cd`s in and launches it); in Claude Cowork (which
auto-loads this file but not the per-course files) a cue like "let's do today's <course>
lesson" is enough to start.

`./take` with no arguments lists the available courses. A course is any top-level directory
with a `.claude/commands/lesson.md` (except `course-template`).

## Repository layout

- `<course>/` — one self-contained course per directory. Standard files: `syllabus.md`
  (syllabus + teaching method), `progress.template.md` (seed copied to the data dir on first
  run), `.claude/commands/lesson.md` (the live-session command), `CLAUDE.md` (course-specific
  tutor context). Some courses add a keystone/motivating-question file (e.g.
  `room-acoustics/motivating-question.md`, `audio-codecs/*.md` keystones).
- `course-template/` — copy this to author a new course; follow its `README.md` checklist.
  Not a runnable course (the launcher skips it).
- `curricula/` — thin declarative overlays that order independent courses into a program of
  study (`curricula/<name>.md`). Shared through-line assets live under `curricula/assets/`.
  See `curricula/README.md`.
- `take` — Bash launcher (`cd` into a course + run `/lesson`).
- `*.md` plan files at root (`AiMusicAudioPlan.md`, etc.) — authoring/design notes, not
  learner content.

**Per-course `CLAUDE.md` files carry the real teaching guidance** — keystone concepts,
canonical worked-example numbers, common misreadings to pre-empt, tone. When working on or
running a specific course, that course's `CLAUDE.md` is authoritative over this root file.

## Conventions

- **Math rendering (JOS standing preference):** in live chat, default to Unicode + CS-style
  identifiers (`f_s`, `RT60`, `alpha`, `lambda`); reach for LaTeX only when genuinely clearer.
  LaTeX is welcome in `lessons/` logs, `progress.md`, and `curricula/` files.
- **Editing content between sessions:** if a course needs a topic expanded or a convention
  changed, edit the versioned content (`syllabus.md`, and `lesson.md`/`CLAUDE.md` for
  structural changes) and commit. Never edit the template's placeholders (`{{COURSE-ID}}`,
  `{{COURSE TITLE}}`, `{{ONE-LINE SCOPE}}`) outside `course-template/`.
- **Adding a course:** `cp -r course-template <new-course-id>`, delete the copied
  `README.md`, find/replace the `{{...}}` placeholders, rewrite `syllabus.md`, then add a row
  to the *Courses* table in the top-level `README.md`.
- **Frontier (living) sections — reach SOTA and keep it current.** A fast-moving technical
  course should end with a *living frontier* phase (after "Putting It Together") that carries
  the learner to the current state of the art, explicitly marked as revised-as-the-field-moves
  and depth-on-demand (never a gate). `flow-matching/`'s **Phase 9** is the reference pattern:
  each frontier topic is a reuse of the course's keystone, pinned to the same worked example,
  with a companion "Frontier sources" list of precise citations and an honest flag on which
  claims are empirical/fast-moving. Updating these between sessions is expected, not
  exceptional — when a new SOTA method lands, add it to the frontier phase and its source list
  (keep `syllabus.md` and the course `CLAUDE.md` in sync), and commit. `course-template/`
  ships a stub frontier phase so new courses inherit the habit.

## Teaching loop (when acting as tutor)

Intuition and analogy first; introduce notation/code only when needed and name every new
symbol on first use. One concept at a time; never advance past a concept until a small
exercise confirms understanding. Adapt depth to the learner profile recorded in `progress.md`
(read it — don't assume). Keep sessions to ~1 hour. Always end by appending to the day's
lesson log and updating `progress.md` in the data dir.
