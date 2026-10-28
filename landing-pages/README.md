# Landing pages

Public "first impression" pages for promoting the courses: pages to link from email,
from the online books, or from a course announcement. They are marketing, not course
content, so the course tools ignore this directory (`./take` and `tools/build_plugin.py`
only treat a directory as a course if it has `.claude/commands/lesson.md`).

The whole directory is published to CCRMA as one site, served at
**https://ccrma.stanford.edu/~jos/landing-pages/**. Each page is an `index.html` in its own
subdirectory; they share `assets/landing.css` (the look: tokens, track colors, components)
and `assets/landing.js` (copy buttons), and otherwise load only Google Fonts.

| Page | Source | URL |
|---|---|---|
| JOS Courses: the three tracks (AI, spectral, physical) | [`index.html`](index.html) | `~jos/landing-pages/` |
| Music Signal Processing Series: the four book courses | [`book-series/index.html`](book-series/index.html) | `~jos/landing-pages/book-series/` |
| AI Foundations | [`ai-foundations/index.html`](ai-foundations/index.html) | `~jos/landing-pages/ai-foundations/` |
| AI Miracle Decade+ | [`ai-miracle-decade-plus/index.html`](ai-miracle-decade-plus/index.html) | `~jos/landing-pages/ai-miracle-decade-plus/` |

Track colors: AI = ochre (`.track-ai`), spectral = blue (`.track-spec`), physical = green
(`.track-phys`). A page or section sets its track with one of those classes.

## Editing

- Edit the page's `index.html` (or `assets/` for anything shared), then run
  `uvx pytest tests/` from the repo root. `tests/test_landing_pages.py` checks every page:
  well-formed standalone HTML; loads only Google Fonts or files in this directory; links
  only to expected hosts, with every relative link, `#` anchor and GitHub repo path
  resolving; every course named in it exists; the install command matches the top-level
  `README.md`. It also checks the facts that go stale: the book-series cards' exercise
  counts against each course's generated bank, the AI pages' phase lists against their
  syllabi, and the AI Miracle timeline's 40 dots against the syllabus's paper stops.
- Preview locally with `open index.html` (relative links work from disk).

## Publishing

```bash
landing-pages/publish -n   # dry run: show what would change on CCRMA
landing-pages/publish      # publish
```

`publish` runs the landing-page tests, then mirrors this directory with `rsync --delete`
to `jos@ccrma-gate.stanford.edu:/user/j/jos/Web/landing-pages/` (override with
`$LANDING_PAGES_DEST`), leaving out `README.md` and `publish` itself. Check the live pages
in a browser (light and dark mode, phone width) before announcing a link.
