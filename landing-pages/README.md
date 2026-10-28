# Landing pages

Public "first impression" pages for promoting the courses: pages to link from email,
from the online books, or from a course announcement. They are marketing, not course
content, so the course tools ignore this directory (`./take` and `tools/build_plugin.py`
only treat a directory as a course if it has `.claude/commands/lesson.md`).

Each page lives in its own subdirectory as a single self-contained `index.html` (inline CSS
and JS; only Google Fonts loads from elsewhere), so publishing it is a plain copy to a web
directory.

| Page | Source | Intended URL |
|---|---|---|
| Music Signal Processing Series (the four book courses, by track) | [`book-series/index.html`](book-series/index.html) | `https://ccrma.stanford.edu/~jos/courses/` |

## Editing

- Edit the `index.html` directly, then run `uvx pytest tests/` from the repo root.
  `tests/test_landing_pages.py` checks that each page is a well-formed standalone
  document, that it only loads from the allowed hosts, and, for the book-series page, that
  each course card's exercise count matches the course's generated bank and its install
  command matches the top-level `README.md`. When a book's exercises change, regenerate
  the bank (`tools/build_book_exercises.py`) and the test tells you which card to update.
- Preview locally with `open book-series/index.html`.

## Publishing

Copy the page to its web directory; nothing is built. Check the page in a browser
(light and dark mode, and phone width) before announcing the link.
