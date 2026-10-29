# courses - a Claude plugin

Self-paced, tutor-style courses run by Claude. Each course is a Skill: Claude acts
as a patient tutor, teaches one concept at a time, checks understanding with a
small exercise before moving on, and keeps your progress and per-day lesson logs
in a folder **you** own.

**Generated** from the course directories of
[josmithiii/Courses](https://github.com/josmithiii/Courses) by
`tools/build_plugin.py` - edit the courses there, not these files. In the Claude
desktop app it is listed (and searchable) as **JOS Courses**.

## Install

**Recommended - one line in a terminal** (needs Claude Code installed). It covers
both Claude Code and the Claude desktop app's Code tab, which share one setup:

```bash
claude plugin marketplace add https://github.com/josmithiii/Courses && claude plugin install courses@josmithiii-courses
```

Then start a session in any folder (a terminal, or the desktop app's Code tab) and
name a course. Always use the full URL: the desktop app stores that form, and Claude
Code refuses the same marketplace under a second form.

**Point-and-click (unreliable as of Oct 2026):** the desktop app's Code tab ->
Customize -> Plugins -> + Add -> Add marketplace accepts the URL, but in testing the
plugin ("JOS Courses") never appeared under Discover, even after Check for
updates. If it isn't listed, run the one-liner - it then shows up in the app at once.

## Courses

| Course | To start, say |
|---|---|
| `agents101` | "let's do today's agents101 lesson" |
| `ai-foundations` | "let's do today's ai-foundations lesson" |
| `ai-miracle-decade-plus` | "let's do today's ai-miracle-decade-plus lesson" |
| `ai-post-training-and-rl` | "let's do today's ai-post-training-and-rl lesson" |
| `ai-sequence-models` | "let's do today's ai-sequence-models lesson" |
| `ai-vision-and-multimodal` | "let's do today's ai-vision-and-multimodal lesson" |
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
| `filters` | "let's do today's filters lesson" |
| `flow-matching` | "let's do today's flow-matching lesson" |
| `mdft` | "let's do today's mdft lesson" |
| `neural-audio-resynthesis` | "let's do today's neural-audio-resynthesis lesson" |
| `pasp` | "let's do today's pasp lesson" |
| `quantum-states` | "let's do today's quantum-states lesson" |
| `room-acoustics` | "let's do today's room-acoustics lesson" |
| `sasp` | "let's do today's sasp lesson" |

## Your progress

Each course keeps `progress.md` (what you've mastered, what's next) and
`lessons/YYYY-MM-DD.md` (a record of each session) under a data root, chosen in
this order: `$COURSES_DATA_DIR`; `Courses-data/` in your workspace folder;
`~/Documents/Courses-data/`. On your first lesson Claude asks where to put it.
Nothing is ever written into the plugin itself.
