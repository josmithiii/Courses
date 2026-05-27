# New Courses — Plan and Progress

A working roadmap for wisdom-tradition courses in this repo. Course
content is separated by **scope** (single coherent subject) and by
**philosophy vs. practice** so each course stays well-focused.

## Status snapshot (2026-05-27)

| Course | Status | Notes |
|--------|--------|-------|
| `buddhism-early-philosophy/` | 🟢 **Active** | Just landed (commit `6210570`). Pali Canon doctrinal foundations: Four Noble Truths → Three Marks → Five Aggregates → Dependent Origination → *nibbāna*. ~40 sessions, 10 phases. Philosophy only. |
| `buddhism-mahayana-philosophy/` | ⚪ Planned | Direct sequel — Phase 8 of the early course (Abhidhamma sketch) sets up Nāgārjuna's critique. Mainstream Mahāyāna is the **largest** branch of Buddhism by adherents (East Asian + Tibetan). |
| `buddhism-sutra-readings/` | 💭 Candidate | Close-reading course (Heart, Diamond, Lotus, Vimalakīrti, Laṅkāvatāra). Probably comes *after* the two philosophy courses. |
| `buddhism-practices/` | 💭 Candidate (deferred) | Meditation, *śīla*, the Eightfold Path as instruction. JOS prefers philosophy first. Rajayana / Nanjō / "5 basic practices" thread fits here. |
| `hindu-philosophy/` (working title) | 💭 Candidate | Upaniṣads + Advaita Vedānta (Śaṅkara). Home for "we are all eyes of God" (*ātman = Brahman*) and "God playing hide-and-seek with himself" (*līlā*). JOS is interested. |

Legend: 🟢 active · ⚪ planned · 💭 candidate (not committed)

## Buddhism — what we decided

- **Philosophy and practice split into separate courses.** JOS is
  interested in philosophy teachings, not (yet) practices.
- **Early Buddhism first, then Mahāyāna.** The Mahāyāna course
  assumes the early doctrines as its starting point — Nāgārjuna's
  Madhyamaka critique is *aimed at* the Abhidhamma reification of
  *dhammas*, which the early-philosophy course's Phase 8 introduces
  for exactly this reason.
- **Texts and tooling.** Pali Canon via **SuttaCentral**
  (suttacentral.net, Bhikkhu Sujato translations) primary; **Access
  to Insight** (Ṭhānissaro et al.) secondary. Browser only — no
  software install needed.
- **Pedagogical "qubit" of the Buddhism courses:** a 10-second
  introspectable moment of ordinary experience (hearing a sound,
  tasting tea, a flash of irritation), decomposed through whichever
  doctrine is in play. Returned to relentlessly, the way the
  quantum-states course returns to the qubit.
- **Standard misreadings flagged from day one** so they don't take
  root: *anattā* as annihilationism; *nibbāna* as a place or as
  non-existence; *kamma* as cosmic justice. The CLAUDE.md tells the
  tutor to correct on the spot and add to a running "misreading
  file" in the worked-example bank.
- **Out of scope (deliberately).** Meditation instructions, monastic
  rules (*Vinaya*), *Jātaka* folklore, devotional material. Each has
  (or will have) its own home; the philosophy courses stay focused.

## Hindu / Vedānta — where it fits

JOS resonates with several ideas that are precisely located in the
Indian tradition:

- **"We are all eyes of God"** ≈ *ātman = Brahman* — the
  Upaniṣadic / Advaita claim that the individual self is identical
  with the universal Self (Śaṅkara, ~8th c. CE).
- **"God likes to hide from himself"** ≈ *līlā* (divine play) — the
  One becomes the many in order to experience itself. Alan Watts
  popularized this exact phrasing in English; the roots are
  Upaniṣadic.

A future `hindu-philosophy/` (or `vedanta/`) course would start from
the major Upaniṣads (Bṛhadāraṇyaka, Chāndogya, Kaṭha, Īśa, Muṇḍaka)
and move through Śaṅkara's Advaita Vedānta, optionally touching the
Bhagavad Gītā as a synthesis text.

**A note on the original list:** "Ramayana" (Vālmīki's epic) is
*Hindu*, not Buddhist — it would belong in a Hindu/Indian-literature
course, not a Buddhist one. The recommendation from JOS's colleague
seems to mix both traditions, which is normal: they share a milieu
but disagree sharply on metaphysics (the *ātman/Brahman* identity is
exactly what early Buddhism rejects with *anattā*). The two
traditions' disagreement is worth meeting head-on, not blurred.

## Original seed (from colleague, in `/l/dttd/FlowStuff/`)

```
ramayana
mahayana
rajayana - nanjou - 5 basic practices
wikipedia
go thru the sutras
experience it
```

How each thread is being routed:

- **ramayana** → Hindu / Indian-literature material (future
  `hindu-philosophy/` or its own epics course)
- **mahayana** → `buddhism-mahayana-philosophy/` (planned)
- **rajayana — nanjō — 5 basic practices** → unusual term;
  possibly Nanjō Bunyū's classification (the 19th-c. Japanese
  Buddhologist who indexed the Chinese Tripiṭaka), or a specific
  teacher's framing of Mahāyāna practice. Practice-flavored — fits
  the deferred `buddhism-practices/` candidate. Worth asking the
  colleague to clarify the source.
- **wikipedia / go thru the sutras / experience it** →
  `buddhism-sutra-readings/` candidate (close-reading course)

## Next likely move

`buddhism-mahayana-philosophy/` is the natural next build — it has
the strongest internal continuation from what's just shipped, and
Mahāyāna is mainstream enough to be worth a dedicated course. The
Hindu philosophy course is interesting and on the list; the
philosophical-comparison value goes up sharply *after* the early-
Buddhism course exists (so that "early Buddhism vs. Advaita Vedānta"
becomes a live comparison rather than a wash).
