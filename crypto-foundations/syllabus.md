# Crypto Foundations — Complete Beginner → A Hardened Personal Workflow

**Learner profile:** Comfortable in a terminal, maybe knows what a hash is,
probably hasn't generated a GPG key. Math may be rusty. So: intuition first,
analogies before notation, every concept paired with a concrete command
(`gpg`, `openssl`, `ssh-keygen`) the learner runs and inspects. ~1 hour per
day. One concept at a time. Every concept is verified with a small exercise
before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one
topic. The topic numbers below are *topics*, not days. `progress.md` tracks
the real position.

**End state:** by the last lesson, the learner has a personal GPG key with a
tested backup and revocation certificate, transparently opens `.gpg` files
in their editor, signs git commits, has an SSH key registered with GitHub,
can read a TLS certificate, knows why passwords are hashed (not encrypted),
and has written their own `SecurityChecklist.md` based on a real threat
model of their own life.

---

## Phase 0 — Orientation & Threat Modeling
- **0.1** What "security" actually means: the CIA triad (Confidentiality,
  Integrity, Authenticity) and why most failures are not about algorithms.
- **0.2** Threat modeling for one person: "what am I protecting, from whom,
  with what budget of inconvenience?" -- the question every later answer
  refers back to.
- **0.3** Install the toolkit: `gnupg`, a graphical pinentry,
  `openssl`, `ssh`. Verify each is on the PATH.

## Phase 1 — Symmetric Encryption (the simpler half)
- **1.1** Plaintext, ciphertext, key. The basic encrypt/decrypt picture.
- **1.2** Block vs stream ciphers; AES at intuition level (substitution +
  permutation, repeated). No math required.
- **1.3** Hands-on: `gpg --symmetric` and `openssl enc -aes-256-cbc`. Encrypt
  a file, look at the bytes, decrypt it back.
- **1.4** The key distribution problem: if Alice and Bob both need the key,
  how do they ever share it the first time? (Motivates Phase 2.)

## Phase 2 — Public-Key (Asymmetric) Encryption — the core idea
- **2.1** The mailbox analogy: anyone can drop a letter in; only the owner
  has the key to open it. The "public" key is the mailbox slot; the
  "private" key opens the box.
- **2.2** What "public" and "private" actually are: a pair of huge numbers
  related by a one-way operation. RSA intuition: multiplying two big primes
  is easy; factoring back is (currently) hard. No proofs.
- **2.3** Hands-on: encrypt to your future self. Generate a throwaway GPG
  key; `gpg --encrypt -r you ...`; decrypt; observe.
- **2.4** Hybrid encryption: why every real system uses BOTH. Asymmetric
  encrypts a fresh symmetric "session key"; symmetric encrypts the data.
  Show this in `gpg --list-packets` output.

## Phase 3 — Signing & Verifying — the other half of asymmetric
- **3.1** Hash functions: a short, deterministic fingerprint of any input.
  Properties: deterministic, fast, preimage-resistant, collision-resistant.
  Hands-on with `shasum -a 256`.
- **3.2** Why MD5 and SHA-1 are no longer safe (collisions are now feasible)
  and how to tell from a tutorial that it's stale.
- **3.3** Digital signatures: sign with private, verify with public. The
  inverse direction of encryption, and what that buys you (authenticity +
  integrity, not secrecy).
- **3.4** Hands-on: `gpg --sign`, `gpg --clearsign`, `gpg --verify`. Tamper
  with one byte; see verification fail.
- **3.5** What signatures DON'T prove: the key-to-identity gap. A valid
  signature says "the holder of this private key signed this." It does not
  say "this is who you think it is." Motivates Phase 4.4 (trust models).

## Phase 4 — OpenPGP in Practice
- **4.1** Names: PGP (1991, Zimmermann) vs OpenPGP (the open RFC standard)
  vs GnuPG (the free implementation). One sentence each; helps when reading
  old docs.
- **4.2** Generating a real key: `gpg --full-generate-key`. What each
  prompt means (kind, size, expiration, uid, passphrase).
- **4.3** Subkeys and uids. Why a primary key for certification and a
  subkey for encryption is a useful pattern, and why expiration dates are
  your friend (not a chore).
- **4.4** Trust models: the original PGP "web of trust" vs the practical
  modern default ("trust on first use" + sometimes a directory like
  GitHub). How GitHub's "Verified" badge actually decides.

## Phase 5 — Living with Your Key (operations -- the part most courses skip)
- **5.1** `gpg-agent` and pinentry: where the passphrase actually lives,
  for how long, and how to configure both. macOS `pinentry-mac` vs Linux
  `pinentry-gtk2`.
- **5.2** Transparent file encryption in your editor: enable Emacs EasyPG
  (or VS Code / Vim equivalents). Open a `.gpg` file, edit, save, watch it
  re-encrypt.
- **5.3** Convenience commands: a one-keystroke "encrypt this file to my
  own key" function in your editor. (We'll write one.)
- **5.4** Encrypted ZIP as a sometimes-alternative: `zip -e`, when it's
  acceptable (sharing with non-GPG users) and when it isn't (real secrets
  -- ZipCrypto is broken; prefer `7z -p -mhe=on` or `.gpg`).
- **5.5** Backups: export secret key, public key, ownertrust, and a
  revocation certificate. Where to put them. **Test the backup** by
  importing into a throwaway `GNUPGHOME`.
- **5.6** Disaster recovery: lost passphrase, suspected compromise, key
  rotation. The role of the revocation cert.

## Phase 6 — Transport: SSH and TLS
- **6.1** SSH keys: the same asymmetric idea, different format and tool.
  `ssh-keygen -t ed25519`. Why Ed25519 over RSA-2048 today.
- **6.2** The SSH agent: `ssh-add`, key forwarding, when to worry about
  it. Configuring an SSH key for GitHub and pushing once.
- **6.3** TLS at 10,000 feet: server presents a certificate; certificate
  is signed by a CA your machine trusts; the chain ends at a root CA your
  OS ships. Let's Encrypt = free, automated.
- **6.4** Hands-on: `openssl s_client -connect example.com:443`. Read the
  certificate. Find the expiration, the subject, the issuer.
- **6.5** What goes wrong: expired certs, hostname mismatch, self-signed
  certs, "ignore the warning" as a security failure mode.

## Phase 7 — Adjacent Essentials (the rest of "be safe")
- **7.1** Password hashing: why we hash passwords instead of encrypting
  them. Salts. Why fast hashes (SHA-256) are the WRONG choice and slow
  ones (bcrypt, scrypt, argon2) are right.
- **7.2** Secrets in code and configs: `.gitignore` hygiene; `gitleaks`
  to scan; "if you ever push it, rotate it" as the unconditional rule.
- **7.3** Two-factor authentication: TOTP apps (Aegis, 1Password) vs SMS
  (don't) vs hardware keys (YubiKey -- best). Where to turn it on first.
- **7.4** Full-disk encryption: FileVault on macOS, LUKS on Linux,
  BitLocker on Windows. Why this is the single most important toggle on
  a personal laptop.
- **7.5** Backups and the 3-2-1 rule: 3 copies, 2 different media, 1
  offsite. Encrypted, tested, and not the same disk as the original.

## Phase 8 — Putting It Together
- **8.1** Revisit threat modeling with everything you now know. Walk
  through a realistic personal threat model end to end.
- **8.2** **Capstone:** harden your own setup. Produce a personal
  `SecurityChecklist.md` (modeled on the course's
  `SecurityBestPractices.md` reference) and execute it: GPG key +
  passphrase + tested backup + revocation cert + Emacs/editor
  integration + git commit signing (optional) + SSH key on GitHub +
  FileVault on + 2FA on the important accounts + secret-scanner in
  your repos.
- **8.3** Where next: recommended reading (Schneier's "Applied
  Cryptography" for breadth, Ferguson/Schneier/Kohno "Cryptography
  Engineering" for depth, "Serious Cryptography" by Aumasson for
  modern). "Don't roll your own" -- when you want to learn more, learn
  *cryptanalysis*, not implementation.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2-3 sentences; ask one quick recall
   question. If shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or picture before any
   notation. The math, if any, comes last and only as far as helps.
3. **Pair with a real command.** Predict what should happen, run it, look
   at the output, explain any surprises. Crypto rewards looking at the
   actual bytes -- `gpg --list-packets`, `openssl asn1parse`, `ssh-keygen
   -y`, `xxd` are friends.
4. **Tiny exercise** to verify: a variation of the command, a "predict
   what this flag changes," or "encrypt this to yourself and decrypt it
   back." Do not advance until it's solid.
5. **Pitfall callout** when relevant -- crypto's failure modes are subtle
   and silent (skipped verification, deprecated algorithm, copy-pasted
   passphrase). One pitfall per lesson is plenty.
6. **Log** what was covered, the exercise, their answer, and a mastery
   note to `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next
   time.

### Mastery criteria

A topic is mastered when the learner can:

1. Explain the concept in their own words (2-3 sentences), including
   *what could go wrong* if it weren't there.
2. Run the relevant command without copy-paste help.
3. Read the command's output and say what each piece means.

Record this in the data-dir `progress.md` mastery log.
