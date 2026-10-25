# courses - a Claude plugin

Self-paced, tutor-style courses run by Claude. Each course is a Skill: Claude acts
as a patient tutor, teaches one concept at a time, checks understanding with a
small exercise before moving on, and keeps your progress and per-day lesson logs
in a folder **you** own.

**Generated** from the course directories of
[josmithiii/Courses](https://github.com/josmithiii/Courses) by
`tools/build_plugin.py` - edit the courses there, not these files.

## Install

**Claude desktop app (Cowork):** Customize -> add marketplace
`josmithiii/Courses`, then install the `courses` plugin. Start a Cowork task
in a folder of your choice (say `~/Documents/Courses`) - your progress is saved in
`Courses-data/` inside it.

**Claude Code:**

```
/plugin marketplace add josmithiii/Courses
/plugin install courses@josmithiii-courses
```

## Courses

| Course | To start, say |
|---|---|
| `agents101` | "let's do today's agents101 lesson" |
| `ai-foundations` | "let's do today's ai-foundations lesson" |
| `ai-miracle-decade-plus` | "let's do today's ai-miracle-decade-plus lesson" |
| `audio-codec-lms` | "let's do today's audio-codec-lms lesson" |
| `audio-codecs` | "let's do today's audio-codecs lesson" |
| `audio-ddsp` | "let's do today's audio-ddsp lesson" |
| `audio-diffusion-dit` | "let's do today's audio-diffusion-dit lesson" |
| `audio-physics-informed` | "let's do today's audio-physics-informed lesson" |
| `audio-ssl-representations` | "let's do today's audio-ssl-representations lesson" |
| `audio-synth-effect-matching` | "let's do today's audio-synth-effect-matching lesson" |
| `buddhism-early-philosophy` | "let's do today's buddhism-early-philosophy lesson" |
| `crypto-foundations` | "let's do today's crypto-foundations lesson" |
| `disentanglement` | "let's do today's disentanglement lesson" |
| `flow-matching` | "let's do today's flow-matching lesson" |
| `neural-audio-resynthesis` | "let's do today's neural-audio-resynthesis lesson" |
| `quantum-states` | "let's do today's quantum-states lesson" |
| `room-acoustics` | "let's do today's room-acoustics lesson" |

## Your progress

Each course keeps `progress.md` (what you've mastered, what's next) and
`lessons/YYYY-MM-DD.md` (a record of each session) under a data root, chosen in
this order: `$COURSES_DATA_DIR`; `Courses-data/` in your workspace folder;
`~/Documents/Courses-data/`. On your first lesson Claude asks where to put it.
Nothing is ever written into the plugin itself.
