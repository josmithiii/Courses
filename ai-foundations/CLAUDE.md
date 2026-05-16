# ai-foundations — project context

This is the `ai-foundations` course inside the public **Courses** repo
(`~/Documents/GitHub/Courses`). It is a personal daily AI tutoring system for a **complete beginner**
(also new to Python, rusty math). Goal: go from the MLP up to modern LLMs, CNNs,
Transformers, and Diffusion, using Python/PyTorch, ~1 hour/day, intuition-first.

## How it works
- `curriculum.md` — the full syllabus and the teaching method.
- `progress.md` — durable state; **read this first**, update it at the end of every lesson.
- `lessons/YYYY-MM-DD.md` — one log per day (lesson content, exercises, answers).
- `/lesson` — the interactive command the learner runs to do a live session.
- Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM)
  only *nudge* the learner to run `/lesson`; the `/lesson` command itself reads
  `progress.md` and builds that day's lesson — no pre-drafting by the schedulers.

## Working with the learner
Be patient, friendly, analogy-first. One concept at a time. Always verify a concept
with a small exercise before advancing. Never rush past something unverified.
Keep sessions ~1 hour. Always update `progress.md` and the day's lesson file at the end.
