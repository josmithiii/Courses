# ai-miracle-decade-plus — project context

This is the `ai-miracle-decade-plus` course inside the public **Courses**
repo (`..`) — a **self-paced** traversal of 40 landmark AI papers (2006 →
2023).  No time budget; topic numbers are stops on a roadmap, not days.

The reading list and the cross-cutting concept pages are curated in JOS's
`music423-2023` repo, mirrored to the public CCRMA GitLab at
<https://cm-gitlab.stanford.edu/jos/music423-2023>.  This course directory
is the **standalone tutor-driven** companion: papers are linked to arXiv
(or the original publisher when arXiv isn't available); the cross-cutting
concept pages are linked to the GitLab tree.  There is nothing to clone
or install.

## Course shape

A consistent road map across all the landmark papers, with explicit
encouragement for **side quests**: when a stop sparks a tangent, the
learner is invited to take it, the tutor logs it, and the spine resumes
when they return.  The roadmap's job is to make sure that however long
the detours last, no landmark gets quietly skipped.

Phases 0 → 11 in `curriculum.md`; concept-page stops (★) connect papers
across the seven lineages described in
[the meta-wiki overview](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/overview.md).

## Content vs. learner state (architecture)

Shipped course **content** is versioned in this repo and read-only at
runtime.  Personal **learner state** lives OUTSIDE the repo so the repo
stays pristine and the system is multi-user / web-app ready.

- **Content (repo):** `curriculum.md` (syllabus + teaching method),
  `progress.template.md` (seed copied on first run),
  `.claude/commands/lesson.md`, this file.
- **Learner state (NOT in repo):** under
  `${COURSES_DATA_DIR:-$HOME/Documents/Courses-data}/ai-miracle-decade-plus/`
  — `progress.md` (durable tracker; read first, updated every session) and
  `lessons/YYYY-MM-DD.md` (per-day logs).
  `COURSES_DATA_DIR` is the seam a future web app overrides to point at a
  per-user store.

Never write personal progress into the repo.  The `/lesson` command has
the exact read/seed/write steps.

## Working with the learner

- **Patient, paper-respecting, analogy-first when math is load-bearing.**
  This learner is reading the actual papers; don't simplify away the
  load-bearing technical claims, but do unpack jargon and notation on
  first use.
- **One stop at a time.** A stop is usually one paper plus a concept-page
  beat.  Sessions vary wildly in length — that's fine.
- **Verify lightly, not as a quiz.** Open questions like "what's the
  load-bearing claim?" / "what surprised you?" beat checklist-style
  comprehension checks.
- **Side quests are first-class.** When the learner detours, log it in
  `progress.md` under "Side quests" with a one-line description and the
  spine stop it paused.  On return, ask what they learned and resume.
- **Reading the papers.** Default to arXiv's HTML view for fast skimming
  and the PDF for deep reads.  When the learner wants a text dump for
  grep/notes, suggest:
  `curl -OL https://arxiv.org/pdf/<arxiv-id>.pdf && pdf2txt.py <arxiv-id>.pdf > /tmp/paper.txt`
  (any equivalent `pdf2txt` / `pdftotext` works).  For the few non-arXiv
  papers (DBN, AlexNet, GPT-1, GPT-2, AlphaGo, AlphaFold 2), the
  curriculum link goes straight to the publisher.
- **Cross-link to the meta-wiki, don't recapitulate it.** The seven
  cross-cutting concept pages
  ([meta-wiki index](https://cm-gitlab.stanford.edu/jos/music423-2023/-/blob/master/ai-2012-to-2023/wiki/index.md))
  are the connective tissue between the papers.  Point the learner
  there; don't re-narrate.

## Reminders

This course is intentionally **un-reminded**: no daily macOS dialog, no
Slack ping.  The learner returns when they return; the roadmap is
patient by design.

## Cross-repo sync

This course exists in **two parallel copies** that intentionally diverge
in link style but should stay in step on substance:

- **GitHub (this repo, `josmithiii/Courses/ai-miracle-decade-plus`, fork
  of GinaGu)** — external links to arXiv (papers) and to the
  music423-2023 GitLab mirror (concept pages, landmark notes).  Designed
  to run standalone as a CoursesGinaGu course.
- **GitLab (`cm-gitlab.stanford.edu/jos/music423-2023/ai-miracle-decade-plus`)**
  — local relative paths (`../ai-2012-to-2023/...`) into the paper
  collection and meta-wiki that live in that same repo.

When changing `curriculum.md`, `progress.template.md`,
`.claude/commands/lesson.md`, `README.md`, or this file: **also apply
the change in the other copy** with the correct link-style adaptation.
Periodically (every few months, or after meaningful Phase content
changes), `diff -u` the two course directories to catch drift:

```bash
diff -u /w/CoursesGinaGu/ai-miracle-decade-plus /w/music423-2023/ai-miracle-decade-plus
```

Substantive content (phase structure, stops, pedagogy, side-quest
protocol) should be identical; differences should be confined to the
link-style adaptations.
