# Curricula

A **curriculum** is an *ordered sequence of courses* that share a goal, with
declared prerequisites and (optionally) a through-line worked example carried
across all of them. Where a **`syllabus.md`** describes *one* course, a curriculum
describes a *program of study* spanning several.

> **syllabus** = one course (the per-course `syllabus.md`).
> **curriculum** = an ordered sequence of courses (a file here in `curricula/`).

This separation is deliberate: the courses stay independent and self-contained,
while a curriculum is a thin, declarative overlay that *expresses an ordering* the
flat course list can't. Taking the courses in curriculum order is a recommendation,
not a gate — each course still stands alone.

## Index of curricula

| Curriculum | Status | Sequence |
|------------|--------|----------|
| [`ai-music-audio.md`](ai-music-audio.md) | 🟢 Complete | `ai-foundations` → `audio-codecs` → `audio-codec-lms` → `audio-diffusion-dit` (enrichment: `flow-matching`, `disentanglement`) |
| [`buddhist-philosophy.md`](buddhist-philosophy.md) | 🟡 Partial | `buddhism-early-philosophy` → `buddhism-mahayana-philosophy` |

## What a `curricula/<name>.md` file declares

- **Goal** (one paragraph) and **who it's for**.
- **Prerequisite course(s)** — links into the repo (e.g. [`../ai-foundations/`](../ai-foundations/)).
- **Ordered course list** with a one-line "why here" for each, and each course's status.
- **Enrichment / co-requisite** courses (optional, run in parallel).
- **Through-line** — an optional shared worked example carried across every course.
- **Source-of-truth** pointers (the wikis or papers the courses teach from).

## Assets

Shared through-line material that belongs to a curriculum (not to any single course)
lives under [`assets/<curriculum>/`](assets/). It's content, so it's versioned here.

## Adding a curriculum

1. Create `curricula/<name>.md` following the section list above.
2. Add a row to the index table here and to the **Curricula** table in the top-level
   [`README.md`](../README.md).
3. If it has a through-line worked example, add `curricula/assets/<name>/` with a
   `README.md` describing the asset (source + license) and the asset itself.
