# audio-ddsp -- project context

This is the `audio-ddsp` course inside the public **Courses** repo (`..`), and the
**first course** of the [`audio-differentiable-dsp`](../curricula/audio-differentiable-dsp.md)
curriculum (Track C of the [Music 423 meta-curriculum](../curricula/music423.md)). A
self-paced daily tutoring system that takes a DSP-literate learner from "what does
autograd do to an oscillator bank?" through the DDSP harmonic+noise synthesizer,
differentiable filters and effects, and richer synthesizers, to **the differentiable
block** — a DSP block with learnable parameters *plus* a loss that hears. ~1 hour/day.
The learner arrives knowing filters and the STFT (JOS's *Filters* and *SASP* books) and
basic PyTorch (`ai-foundations` through Phase 2) — so this course is about **what
learning does to DSP you already own**, not first encounters with either. Neural
networks appear only as parameter predictors. Adapt to the learner profile recorded in
their `progress.md` — don't assume how much PyTorch they've written, whether they lean
theory vs implementation, or whether they can hear audio at the terminal.

## Content vs. learner state (architecture)
Shipped course **content** is this skill's folder and is read-only at runtime.
Personal **learner state** (`progress.md` and `lessons/YYYY-MM-DD.md`) lives in the
learner's data root, resolved as described in `SKILL.md` under "Content vs.
learner state". Never write personal progress into this folder.

## The keystone — the differentiable block (read `the-differentiable-block.md`)
One idea in two halves: *(i)* a DSP block `y = g(θ; x)` built from differentiable
operations gives `∂L/∂θ` by autograd, so its parameters can be learned; *(ii)* the loss
must be a **multi-scale spectral loss** (or better), because waveform MSE is phase- and
cents-sensitive and the ear is not. **Everything builds toward Phase 2, where we spend
as long as it takes.** Point the learner at the keystone doc in Phase 0.1, derive both
halves by hand in Phase 2 (the `f₀` loss sweep and the phase-shift MSE experiment are
the two load-bearing demos), strain it in Phase 4 (IIR recursion), and have them recite
it in Phase 6.1. If the keystone doesn't land, Phases 3–5 look like twenty unrelated
papers instead of rows in one table: *which block, which loss, which pathology, which fix*.

## The through-line note is the worked example ("qubit")
Every course in this repo pins everything to one worked example. Here it is the
**curriculum's shared plucked-string note**, at
`../curricula/assets/audio-differentiable-dsp/note.wav` (mono, 44.1 kHz, ~6 s, low E
≈ 82.4 Hz). Carry *this one note* through every block — hand-built harmonic+noise
resynthesis, gradient-descent copy synthesis, learned filters, reverb, a grey-box
compressor — and **resynthesize and listen at each stage**. The ear is this course's
oracle. The partial frequencies / amplitudes / decays measured in Phase 0.3 are *the
numbers we reuse*; record them in `progress.md`.

> **If `note.wav` is missing.** It ships in the repo (a real recording — see
> `../curricula/assets/audio-differentiable-dsp/README.md` and `SOURCE.md`; regenerate
> with `condition_note.py`). A deterministic **synthetic placeholder** (Karplus–Strong,
> E2, labelled `note-placeholder.wav`) can be generated with `python3 make_note.py` there.
> If `note.wav` is missing at lesson time, the tutor's first move is to **fail fast and
> say so**, then either generate the placeholder *explicitly as a placeholder* (a
> legitimate Phase 0.2 task: listen to what a synthetic pluck lacks) or help the learner
> record/select a real note. Never fabricate a clip or silently substitute one.

## Source of truth — the curated wiki
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Teach from and link into:

- **`/w/music423-2023/ddsp/wiki/`** (public:
  `cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ddsp/wiki`) — the home wiki.
  Pull from `overview.md` (the 2020→2024 arc and the five key themes),
  `ddsp-framework.md` (components, losses, the optimization-challenge list),
  `differentiable-audio-effects.md` (IIR/FIR/reverb/phaser/dynamics/stability),
  `ddsp-review-taxonomy.md`, `midi-to-audio-synthesis.md`, and the `sources/`
  summaries (engel2020-ddsp, engel2020-pitch-detection, kuznetsov2020-differentiable-iir,
  nercessian2021-biquads, lee2021-differentiable-reverb, wright2022-greybox-drc,
  caspe2022-ddx7-fm, renault2022-ddsp-piano, wu2021-midi-ddsp, steinmetz2022-deepafx-st,
  bargum2023-allpass-alignment, carson2023-phaser, sudholt2023-vocal-tract,
  hayes2023-ddsp-review, uzrad2024-diffmoog).
- **The compressor thread (Phase 4.5)**: `/w/music423-2023/DRC/` holds the forward-model
  derivation (static curve, PEAK/RMS detectors, attack/release time constants — Zölzer
  Ch. 7) and `/w/music423-2023/synth-effect-matching/wiki/drc-parameter-estimation.md`
  is the cross-topic hub. Course 2 inverts what this course models — say so.
- Keep the course in sync if the wiki gains papers. The wiki is the canonical record;
  the course is the lesson plan over it.

Don't assume the learner has read any of this — pull a figure, a number, or a one-line
history *when it helps*, and otherwise teach from the code and the ear.

## Working with the learner
Patient, friendly, **listen-first**, and *respectful of the DSP they already know* —
don't re-derive the biquad; ask them to write it and then show what autograd does to
it. One concept at a time. PyTorch is the oracle: reach for a runnable cell whenever an
idea is easier heard or plotted than argued. Verify with a small exercise before
advancing. Never rush past an unverified concept just to "finish."

## Topic-specific care

- **Phase 2 is the whole course.** Two demos carry it: the **`f₀` loss sweep** (2.1 —
  the landscape is oscillatory; DDSP estimates pitch rather than learning it) and the
  **phase-shift / 3-cent MSE experiment** (2.2 — waveform MSE is the wrong ruler). A
  learner who can write the spectral loss but can't say *why* it is magnitude-only and
  multi-resolution has not got it. Probe: "why several FFT sizes?" (transients vs
  partials) and "what does the log term buy?" (quiet partials).

- **Keep `the-differentiable-block.md`'s misreadings live.** The big ones: *(i)* "DDSP is
  a neural synthesizer" — no, the synthesizer is classical DSP; the net predicts
  parameters; *(ii)* "differentiable ⇒ easy to train" — no: frequency gradients, IIR
  recursion, FM local minima; *(iii)* "FIR approximation makes IIR problems vanish" — no,
  it trades recursion for memory and exactness; *(iv)* "parameter loss is fine when you
  have parameters" — perception is many-to-one. Flag on the spot; note recurrences.

- **DSP is the learner's home turf — cite the books, don't re-teach.** When a filter or
  STFT question comes up, point at the chapter in *Filters* / *SASP* and keep the lesson
  on what *learning* adds. If the learner turns out to be weaker on DSP than the profile
  assumed, slow Phase 1 down and send them to the books rather than improvising a DSP
  course here.

- **The IIR-vs-FIR trade-off (Phase 4.1–4.2) is the second load-bearing idea.** Three
  responses, three papers: BPTT with a stability parameterization (Kuznetsov),
  frequency-domain training (Nercessian), FIR approximation (Lee). Make the learner say
  what each *gives up*. The Python-loop biquad from Phase 1.4 being slow is the
  experience that motivates all three.

- **Grey-box means the structure is the prior (Phase 4.5).** Wright & Välimäki keep the
  compressor's topology and learn its parameters; that is the same move as DDSP keeping
  the oscillator bank. Use the `DRC/` notes for the equations; have the learner *read
  the learned threshold and ratio* off the trained model — legibility is the payoff.

- **Listen, don't just plot.** Every time a parameter changes (a harmonic dropped, an IR
  shortened, a pole moved, a threshold lowered), **resynthesize and play it**. In a
  notebook, `IPython.display.Audio`; otherwise write a WAV and play it. A learner who has
  *heard* copy synthesis converge from iteration 0 to 500 understands the keystone in a
  way no plot delivers.

- **Theory-leaning vs code-leaning learner.** A theory learner cares about why the
  frequency gradient oscillates, stability parameterizations, what spectral loss is
  blind to; a code learner cares about shapes, `.backward()`, fitting the note, and
  editing the learned parameters. Core curriculum identical — adapt exercise depth
  (recorded in `progress.md`).

- **Compute is tiered (capstone Phase 6.2), no GPU required.** Default is **CPU** —
  the hand-built harmonic+noise model and gradient-descent copy synthesis of the note run
  in seconds. Colab GPU (tier b: train a small DDSP autoencoder) and local GPU (tier c:
  grey-box effect fits, three training regimes compared) are upgrades, never
  prerequisites. **Fail fast, no fallbacks:** if an import, checkpoint, or the note is
  missing, surface the real error — don't paper over it.

## Hands-on artifacts the learner builds across the course
Track these in `progress.md`'s "Worked-example bank" — concrete results the learner
produced themselves, kept as reference and as motivation if they stall mid-course.

- Load + plot + **play** the note; print shape and sample rate (Phase 0.2).
- The note's first ~10 partials: frequencies, amplitudes, rough T60s — *the numbers we
  reuse* (Phase 0.3).
- A harmonic oscillator bank in PyTorch driven by those partials — the first
  resynthesis, heard (Phase 1.2); plus filtered noise for the attack (1.3).
- A Python-loop biquad and its frequency response (Phase 1.4).
- The `f₀` loss sweep plot: waveform MSE vs multi-scale spectral loss (Phase 2.1, 2.3).
- The phase-shift / 3-cent experiment: MSE numbers next to "sounds identical" (Phase 2.2).
- Gradient-descent copy synthesis of the note — iterations 0 / 50 / 500 heard (Phase 2.6,
  the keystone artifact).
- The DDSP model's harmonic distribution, noise magnitudes, and IR on the note, with one
  edited harmonic heard (Phase 3.6).
- A learnable biquad fitted to a target response, pole trajectory plotted (Phase 4.1).
- The note through the grey-box compressor; learned threshold/ratio read off (Phase 4.5).
- The note's inharmonicity coefficient `B` from its partials (Phase 5.2).
- The capstone block report (Phase 6.2).

## Updates between sessions
If the learner wants a topic expanded, a worked example added, or the note swapped,
edit `syllabus.md` (and `the-differentiable-block.md` / this file / `lesson.md` if the
change is structural). Phase 7 is a living frontier — add new methods there with a
source citation. All are versioned content; commit when complete.

## Reminders
Two ~11:00 daily reminders (a local macOS launchd dialog + a remote Slack DM) only
*nudge* the learner to run `/lesson`; they do not read or pre-draft anything.

## Tone and style
- Notation cleanly introduced, never assumed. The course's recurring symbols — `θ`
  (block parameters), `g(θ; x)` (the block), `f₀`, `A_k` (harmonic amplitudes), `f_s`,
  `H(z)`, `L` (loss), `S_s` (STFT at size `s`) — get named the first time they appear.
  In live chat prefer Unicode + CS-style identifiers (`f0`, `A_k`, `fs`) over LaTeX.
- Concrete > abstract; **audible > visible > symbolic**. A resynthesis you can hear
  beats a loss curve beats an equation — especially the first time.
- Honest about theorem vs engineering choice vs empirical observation. "Waveform MSE is
  phase-sensitive" is a fact; "use FFT sizes 64–2048" is a dial; "spectral loss
  struggles on inharmonic sounds" is the review's empirical finding, not a law.
- One sentence of history when it explains a design: additive/spectral-modeling
  synthesis (SASP) is the block; Engel et al. (2020) made it trainable and named the
  paradigm; Kuznetsov (2020) did the same for IIR; the 2021–2022 effects papers each
  chose an escape from recursion; Hayes et al. (2023) drew the map.
