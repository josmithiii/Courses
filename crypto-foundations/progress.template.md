# Learning Progress Tracker — TEMPLATE

> This file is the **seed** shipped with the course. It is copied into the learner's
> private data directory on first run and then lived-in there. The repo copy stays
> pristine. Do not edit this template with personal data — edit the copy in the
> data directory (see CLAUDE.md / the /lesson command for the resolved path).

## Learner profile
- Crypto background: _(none / used HTTPS without thinking / used GPG / built with crypto libs)_
- Shell / Unix: _(beginner / intermediate / power user)_
- Math comfort (modular arithmetic, big numbers): _(rusty / OK / strong)_
- Existing keys: _(none / SSH only / GPG too / not sure)_
- Editor of choice: _(Emacs / Vim / VS Code / other)_  ← affects Phase 5.2 integration
- OS: _(macOS / Linux / Windows + WSL)_
- Threat model in one sentence: _(e.g., "personal laptop, casual snoopers and lost-laptop risk; no nation-state in scope")_
- Time budget: ~1 hour/day
- Style: patient, friendly, analogy-first, every concept paired with a real command

## Status
- **Current phase:** 0 — Orientation & Threat Modeling
- **Next topic:** 0.1 — What "security" actually means (after the Lesson 0 interview)
- **Last session date:** (none yet)
- **Lessons completed:** 0

## Environment status
- [ ] `gpg --version` works
- [ ] `pinentry` installed and configured in `~/.gnupg/gpg-agent.conf`
- [ ] `openssl version` works
- [ ] `ssh -V` works
- [ ] Personal GPG key generated (`gpg --list-secret-keys` shows it)
- [ ] Secret key + ownertrust + revocation cert backed up to offline storage
- [ ] Backup verified by importing into a throwaway `GNUPGHOME`
- [ ] Editor opens `.gpg` files transparently (Phase 5.2)
- [ ] SSH key registered with GitHub (Phase 6.2)
- [ ] FileVault / LUKS / BitLocker enabled on this machine
- [ ] 2FA enabled on the most important accounts (email, GitHub, password mgr)

## Artifacts built so far
- (none yet)

(As the course progresses, list what they built: "have personal GPG key
0xABCD…, backed up to USB stick + 1Password," "Emacs auto-decrypts .gpg
files," "SSH key on GitHub," "shipped my own SecurityChecklist.md," etc.)

## Mastery log
| Date | Topic | Concept | Exercise | Result | Notes |
|------|-------|---------|----------|--------|-------|
|      |       |         |          |        |       |

## Open questions / things to revisit
- (none yet)

## Personal threat model (revisited in Phase 8.1)
> Filled in lightly at Lesson 0.2 and revisited at the capstone.
> "What am I protecting, from whom, with how much budget of inconvenience?"

- **Assets:** _(what's valuable: source code, financial accounts, private writing, identity, ...)_
- **Adversaries in scope:** _(opportunistic thieves, scammers, ex-colleagues, ...)_
- **Adversaries out of scope:** _(nation-states, targeted APTs, ...)_
- **Inconvenience budget:** _(low — only essentials / medium / high — willing to use a YubiKey)_
