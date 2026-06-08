# Neural Audio Resynthesis — Design-Decisions Skeleton (DRAFT for review)

**Status:** ✅ Design session complete — all 9 decisions resolved with JOS on 2026-06-08.
Each numbered **DECISION** kept its recommendation unless a resolution note says otherwise;
two were refined (DECISION 3 → *plunge-in, no hard gates*; DECISION 5 → *both tools, RAVE
main*). The consolidated resolutions are at the bottom
([§ Decisions resolved](#decisions-resolved-2026-06-08)). Next step: author the course
(house five-file anatomy).

Companion to [`NewCoursesPlan.md`](NewCoursesPlan.md) (where this course is the
`neural-audio-resynthesis/` 💭-candidate meta-course row) and
[`AiMusicAudioPlan.md`](AiMusicAudioPlan.md) (the curriculum it caps).

---

## What this course is (the one paragraph)

The **capstone meta-course** of the AI-music/audio thread. *Not a new body of theory* —
an **integration course** whose express purpose is **creating and editing audio with
neural methods**, in JOS's words: *"tie all that stuff together … survey the field and
drill down on the load-bearing survivors for the meat of the course."* It **surveys** the
landscape of neural audio generation, then **drills down** on the few techniques that
actually compose into the **resynthesis paradigm** — encode a recording to a learned
latent, steer within that latent, decode coherent variations — turning *static recordings
into fluid, steerable objects*. It closes on the **evaluation problem** (how do you score
a "coherent variation" with no ground-truth target?) and the **open frontier**
(self-supervised + decodable + disentangled representations of full recordings).

It is the **destination** the rest of the thread feeds:
`flow-matching/` + `audio-codecs/` + `audio-diffusion-dit/` (the generator),
`audio-ssl-representations/` (the representation), `disentanglement/` (the inductive
bias) — all converge here.

---

## DECISION 1 — The keystone / north-star

Every course in this repo has one load-bearing idea (room-acoustics: the Schroeder
frequency; flow-matching: the conditional-expectation identity; disentanglement: the
decomposition & the impossibility; audio-ssl-representations: the pretext task & the
target). A meta-course needs one too, or it sprawls.

**Recommended (two-part, mirroring the other courses):**

1. **The resynthesis loop** *(the apparatus)* — every system is one diagram:
   `encode → (disentangle / steer) → decode`. A recording becomes a *steerable object*
   exactly when you can (a) **encode** it to a latent that captures its full complexity,
   (b) **move** within that latent in a way that means something, and (c) **decode** back
   to coherent audio. Survey systems are *instances* of this loop; the drill-down is its
   three boxes.
2. **The control problem** *(the question)* — the loop is easy to draw and hard to
   *steer*: a learned latent is **expressive but illegible**. The whole course is the
   quest to recover **parametric-grade, legible control over a learned representation** —
   learned expressivity *with* knob-like steerability. This is the talk's "two
   epistemologies" tension (parametric = legible-but-bounded vs learned =
   expressive-but-implicit), made into the course's spine.

> Together: *resynthesis = the encode→steer→decode loop, and the whole game is winning
> back legible control over the latent you steer.* The drill-down chapters each attack one
> box of the loop; the frontier is the box we can't yet steer (disentangled control).

**Alternatives to weigh:**
- **(A) "Three knobs, one pipeline"** — keystone = the taxonomy *representation ×
  inductive-bias × generator*; every system is a choice of the three. Cleaner as a map,
  weaker as a *question* (less tension to drive the course).
- **(B) The epistemology shift alone** — parametric→learned as the single thesis. Elegant
  and straight from the abstract, but more essay than apparatus; the loop gives the
  hands-on spine the others have.
- **(C) "Load-bearing survivors" as the keystone** — make *reading a fast field* the
  central skill. Good as a **secondary** goal (see § Meta-skill), too thin as the only one.

*Recommendation: the two-part loop+control keystone, with (C) as an explicit secondary
meta-skill.*

---

## DECISION 2 — The qubit (recurring worked example)

The curriculum's shared **~2-second solo-piano clip** is the obvious through-line (it's
*already* carried across courses 1–3 and used in `audio-ssl-representations/`). The
question is the **recurring task** performed on it.

**Recommended:** the recurring move is **"resynthesize a variation that preserves identity
while exploring around it"** — encode the clip, perturb in latent, decode, then **A/B
listen**: *is it recognizably the same source, yet genuinely different?* The **stretch
task** (the editing payoff) is a **single-attribute edit** — change the **room** (reverb /
space) *or* the **timbre** while leaving the performance/composition intact — the
"steerable object" made audible, and the direct tie to `disentanglement/`.

- **Oracle:** the **ear** (A/B, source vs variation), backed by one or two numbers —
  an **identity/similarity** score (e.g. CLAP or embedding cosine to the source) and a
  **distribution** score (e.g. FAD to a reference set). The ear leads; the numbers
  corroborate — exactly the eval skepticism Phase III teaches.
- **Recurring picture:** the **encode→steer→decode loop drawn over the clip**, the same
  diagram every survey system gets slotted into.

**Alternative:** make the *attribute edit* the primary recurring task (not the stretch),
i.e. center the course on **editing** rather than **variation**. More aligned with the
talk's "audio editing" title; riskier because clean attribute disentanglement is the
*unsolved* part, so the primary loop might not close on CPU/tier-a. *Recommendation: keep
variation-preserving-identity primary (it always closes), attribute-edit as the stretch.*

---

## DECISION 3 — Prerequisites vs. self-contained primers

A capstone is only a capstone if it *assumes* its feeders. But hard-gating five courses
makes it unreachable.

**✅ RESOLVED — no hard gates; plunge-in friendly, strongly recommended.** JOS's call:
let the student **plunge in and give it a try** without being hard-required to complete
any other course. *Rationale (JOS, in his own words):* "Students like me will want to
plunge in, get in over their heads, and then be motivated to go back and take those prereq
courses that now they're convinced they need." The course **strongly recommends** the
feeders and is honest about the depth, but gates nothing — the *getting-in-over-your-head*
moment is the motivator, and the recall-primers are what you reach for once you're
convinced you need the prereq.

- **Strongly recommended (not gated):** `ai-foundations/` + the **AI Music & Audio core**
  (`audio-codecs/`, `audio-diffusion-dit/`) for the continuous-VAE-latent + DiT picture;
  then `audio-ssl-representations/`, `disentanglement/`, `flow-matching/`.
- **1-page recall primers** that *link back* rather than re-teach — "you met this in X;
  here's the one slide we need" — sized so a plunge-in learner can keep moving and knows
  exactly which feeder to go back for.
- **Never re-teach from scratch.** The primer + a pointer is the contract; the meta-course
  stays *integration*, not review.

*Goes further than the `flow-matching`-as-enrichment precedent in `AiMusicAudioPlan.md`
(decision 6): there enrichment was un-gated; here **all** prereqs are un-gated by design.*

---

## DECISION 4 — Scope boundaries & the misreadings to kill

**In scope:** creating/editing audio by the **encode→steer→decode** loop over learned
representations — resynthesis, variation, attribute editing, timbre/space transfer; the
talk's paradigm (rectified-flow DiT conditioned on an SSL latent) as the worked apex.

**Out of scope (deliberately):** from-scratch DSP/parametric synthesis (JOS's home turf —
referenced as the *contrast*, not taught); pure **text-to-music-from-a-prompt** as the main
event (TTM systems appear in the *survey* and as decoders, but the course is about
*resynthesizing an existing recording*, not prompting from nothing); training large models
from scratch (we **use pretrained checkpoints**, tiered a/b/c).

**Misreadings to kill (the `misreadings` file, per house style):**
- "Resynthesis = reconstruction." No — the goal is *coherent variation around* the source,
  not faithful inversion. (Reconstruction is the floor, not the goal.)
- "A good generator is all you need." No — the loop needs the **representation** *and* the
  **inductive bias** too; a SOTA DiT on an illegible latent gives you no control.
- "More disentanglement ⇒ better resynthesis." Recall **Locatello** (`disentanglement/`):
  identifiability needs an inductive bias; unsupervised factor-naming is unsolved.
- "Neural resynthesis replaces DSP synthesis." Different **epistemology**, complementary —
  legible-but-bounded vs expressive-but-implicit; the course's whole point is wanting *both*.
- "Evaluation = FAD" (or any one number). The **no-reference problem**: a variation has no
  ground-truth target; report identity + distribution + **listening**, never one headline.
- "Codec-LM and diffusion-DiT are interchangeable routes to resynthesis." See DECISION 6 —
  for *editing an existing recording*, the continuous/diffusion route is load-bearing; the
  discrete-token LM route is surveyed but largely set aside, *with reasons*.

---

## Provisional structure — survey → drill-down → evaluation (the three acts)

*Phase numbering provisional; ~9 phases (0–8), ~20–25 sessions, tiered a/b/c capstone.*
JOS wanted exactly this shape: **survey the field, then drill the survivors for the meat.**

### Act 0 — Orientation
- **Phase 0** — the **resynthesis loop** drawn; the **control problem** named; the two
  epistemologies; read the keystone doc; tools (load a pretrained resynthesis-capable model,
  encode the piano clip, decode it back — confirm the loop runs end to end).

### Act I — The Survey *(breadth, fast — orient and place, don't master)*
- **Phase 1 — the map of neural audio generation.** Parametric/**DDSP** (legible, bounded)
  → **codec + LM** (AudioLM → MusicGen → VALL-E) → **continuous-VAE + diffusion/DiT**
  (AudioLDM → Stable Audio → FluxMusic → DiffRhythm/ACE-Step) → **resynthesis-as-editing**
  (RAVE, timbre transfer, the talk). Each system gets *placed on the loop*, not derived.
- **Phase 2 — reading the field: what's load-bearing vs. what's a detail.** The **meta-skill**
  (see below): which ideas survived contact with scale, which were dead ends or
  implementation trivia. Sets up the drill-down by *choosing the survivors* in front of the
  learner. **(This is where codec-LM is consciously set aside for editing — DECISION 6.)**

### Act II — The Drill-Down *(depth — the meat; each box of the loop)*
- **Phase 3 — the representation (encode).** The **SSL conditioning latent**
  (`audio-ssl-representations/`): what "captures the full complexity of a recording" means,
  why it's understanding-grade but **not invertible**. Recall-primer + apply to the clip.
- **Phase 4 — the inductive bias (steer).** **Disentanglement** (`disentanglement/`): why
  legible control needs a bias; β-VAE/TC, the impossibility, supervised pitch/timbre as the
  case that *works*. The latent's **steerability** is exactly what's hard.
- **Phase 5 — the generator (decode).** The **rectified-flow DiT** (`flow-matching/` +
  `audio-diffusion-dit/`): generating *around* a conditioning latent, not from noise alone;
  RAVE's adversarial decoder as the real-time counterpoint.
- **Phase 6 — assembling the system.** Put the three boxes together: SSL latent →
  (disentangling bias) → rectified-flow-DiT decoder → a **variation** of the clip. The
  talk's paradigm, built. Where each piece's limits become the *system's* limits.

### Act III — Evaluation & Frontier
- **Phase 7 — the evaluation problem.** The **no-reference** challenge; objective metrics
  (FAD, CLAP-similarity/identity, MIDI/transcription-based structure scores) vs subjective
  (MOS, A/B, MUSHRA); what each does and doesn't capture; why **listening stays the oracle**.
- **Phase 8 — the open frontier + capstone.** **Self-supervised, decodable,
  attribute-disentangled** representations of full recordings — the unsolved box of the
  loop (`disentanglement/` 8.4 ∧ `audio-ssl-representations/` 7 named as one). Tiered
  capstone (DECISION 5). End state: the learner can *build a resynthesis pipeline from
  pretrained parts, evaluate it honestly, and read a new 2026/2027 system onto the map.*

---

## DECISION 5 — Capstone tooling & tiers (no GPU required for tier a)

Mirror the house a/b/c. **Default tooling TBD** — three viable spines:

- **(a) CPU / default.** Encode the piano clip and decode a **variation**, A/B listen.
  Lightest reliable path is a **pretrained RAVE** model (real-time, CPU-feasible) — the
  cleanest "encode→steer→decode loop you can hear" on a laptop. *(Alt: Stable Audio Open
  audio-to-audio at low steps, but heavier.)*
- **(b) Colab GPU.** Condition a **rectified-flow / Stable-Audio-Open** generation on the
  clip's representation; explore the distribution of variations; attempt **one attribute
  edit** (room or timbre).
- **(c) Local GPU.** Fuller pipeline — **MERT** (or another SSL encoder) features →
  conditioned decoder; attempt **disentangled steering**; the most research-flavored tier.

**✅ RESOLVED — both, RAVE as the main tier-a path.** JOS wants *both* tools present:
**RAVE** is the **main** tier-a default (very commonly used, cleanest audible
encode→steer→decode on a laptop — *the loop is the lesson*), and a **tiny SSL-latent + flow
decoder** is a **second example / optional enrichment** (faithful to the paradigm's
architecture, the bridge to tiers b/c). So the GAN-decoder caveat becomes a *teaching
moment*: tier a hears the loop on RAVE, then optionally re-runs the same clip through the
flow decoder to feel the architecture the rest of the course actually builds toward.

---

## The "load-bearing survivors" meta-skill (secondary goal)

A distinctive thing JOS asked for: *survey, then drill the survivors.* That implies a
**transferable meta-skill** — reading a fast-moving field and judging what's structural vs
ephemeral (the analogue of the *research-hygiene* lesson `disentanglement/` teaches with
Locatello). Make it explicit: by the end, the learner can take a **new** audio-gen paper
(2026/2027) and (1) place it on the encode→steer→decode loop, (2) say which box it advances,
(3) judge whether it's load-bearing or a detail. Worth a named end-state criterion.

---

## DECISION 6 — Two paradigms, or one mainline for editing?

The curriculum teaches **both** generation paradigms (codec→LM = course 2; diffusion→DiT =
course 3). But for **resynthesis-as-editing of an existing recording**, are both
load-bearing, or is one the mainline?

**Recommended stance (and a teachable claim, not a hand-wave):** the **continuous-latent +
diffusion/flow** route is the load-bearing one for *editing* — its latent is continuous and
steerable, and conditioning-on-a-source is natural; the **discrete-token LM** route is
surveyed and then *consciously set aside for editing* (great for generation/continuation,
awkward for fine continuous steering of a given recording). Making this call **out loud**
in Phase 2 *is* the meta-skill in action. **Flag for JOS:** agree, soften ("both, with
trade-offs"), or invert?

---

## Source of truth (teaches from the same canonical wikis as its feeders)

- **`/w/music423-2023/ai-music-audio-gen/wiki/`** — esp.
  `concepts/self-supervised-audio-representations.md` (literally the resynthesis concept
  page — *the* spine), `concepts/codec-based-generation.md`, and the `sources/` for
  RAVE, MERT, FluxMusic, DiT, Stable Audio, AudioLM, MusicGen.
- **`/w/music423-2023/diffusion/wiki/`** — the DiT / rectified-flow decoder side.
- **`/w/music423-2023/disentanglement/wiki/`** — the inductive-bias / control side
  (`audio-disentanglement.md`, the impossibility).
- **`/w/music423-2023/ddsp/wiki/`** — the parametric contrast (legible-but-bounded).
- Same contract as the other courses: the wiki stays canonical, the course stays the
  pedagogical front-end; keep in sync as wikis gain papers.

---

## Decisions resolved (2026-06-08)

All nine settled with JOS in the design session. Recommendations adopted except where a
**↻ refined** note appears.

1. **Keystone** (DECISION 1) — ✅ **two-part *resynthesis loop + control problem***, with
   *load-bearing survivors* as the explicit secondary meta-skill.
2. **Qubit** (DECISION 2) — ✅ **variation-preserving-identity** as the primary recurring
   task; **attribute-edit** (room/timbre) as the stretch.
3. **Prereq hardness** (DECISION 3) — ↻ **refined: no hard gates.** Plunge-in friendly,
   *strongly recommended* feeders + recall-primers; getting-in-over-your-head is the
   motivator to go back for prereqs. (Recommendation had been hard-gate-core-only.)
4. **Scope line** (DECISION 4) — ✅ **as written**: exclude text-to-music-from-prompt as a
   main event; DDSP/parametric as *contrast* only; pretrained checkpoints, no from-scratch
   training.
5. **Codec-LM stance** (DECISION 6) — ✅ **continuous/diffusion is the editing mainline**;
   the discrete-token LM route is surveyed then consciously **set aside for editing, with
   reasons** (the meta-skill in action, in Phase 2).
6. **Tier-a tooling** (DECISION 5) — ↻ **refined: both.** **RAVE** is the main tier-a path;
   the **tiny SSL-latent+flow decoder** is a second example / optional enrichment and the
   bridge to tiers b/c.
7. **Length / phase count** (DECISION 7) — ✅ **~9 phases (0–8) / ~20–25 sessions**, three
   acts (survey → drill-down → evaluation) as sketched.
8. **Slug & placement** (DECISION 8) — ✅ **capstone enrichment** of the AI Music & Audio
   curriculum (4th slot, like `disentanglement`/`audio-ssl`); slug stays
   `neural-audio-resynthesis/`.
9. **Talk-centricity** (DECISION 9) — ✅ **generic, no citation.** Worked apex presented as
   the rectified-flow-DiT-on-SSL-latent paradigm with *no* talk citation, consistent with
   the framing scrub.

---

*Now settled — authoring follows the house five-file anatomy
(`syllabus.md`, `CLAUDE.md`, keystone doc, `progress.template.md`,
`.claude/commands/lesson.md`) — same as `disentanglement/` and
`audio-ssl-representations/`.*
