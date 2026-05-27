# Course template

Canonical starting point for a new course in this repo. Copy this folder, fill in
the placeholders, and you have a working course skeleton. Adapted from
`ai-foundations/` — the original and minimal reference course.

## How to use

```bash
cp -r course-template <new-course-id>     # e.g. cp -r course-template music-theory
cd <new-course-id>
rm README.md                              # this file is authoring instructions, not learner content
```

Then do these things — that's the whole authoring checklist:

1. **Find/replace authoring placeholders** in every remaining file in the new folder:
   - `{{COURSE-ID}}` → your course slug, e.g. `quantum-states`
   - `{{COURSE TITLE}}` → readable title, e.g. `Quantum States`
   - `{{ONE-LINE SCOPE}}` → one-sentence pitch (the same line you'll put in the top-level README row)
2. **Rewrite `curriculum.md`** with your phases/topics. Keep the *Pace philosophy*
   and *Teaching method* sections at the bottom — they apply to every course.
3. **Adjust `progress.template.md`** Learner-profile fields and Environment-status
   checkboxes for the subject (what background to ask about, what tools to install).
4. **Tune `CLAUDE.md`** and `.claude/commands/lesson.md` only if the subject needs
   a different start-of-session flow (e.g. paper-reading mode, side-quests as in
   `ai-miracle-decade-plus/`). Most courses need nothing here beyond step 1.
5. **Add a row** to the top-level `README.md` *Courses* table.

`{{...}}` markers are *authoring-time* placeholders for find/replace. The
angle-bracket markers like `<data root>` are *runtime* placeholders resolved by
the tutor at lesson time — leave those alone.

## What each file is

- `curriculum.md` — full syllabus and teaching method (shipped, read-only at runtime).
- `progress.template.md` — seed tracker; copied to the learner's data dir on first run.
- `CLAUDE.md` — context for any Claude Code session launched in this course folder.
- `.claude/commands/lesson.md` — the `/lesson` slash command that runs the live session.

The separation of shipped content vs. learner state, and the `COURSES_DATA_DIR`
seam, are documented in the top-level `README.md`.
