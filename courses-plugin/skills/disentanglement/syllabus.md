# Disentangled Representation Learning — One Factor per Axis, and Why That's Hard

**Learner profile:** Knows **VAEs** — encoder `q(z|x)`, decoder `p(x|z)`, the ELBO, the KL
term, the reparameterisation trick — at the level of `ai-foundations/`. Comfortable with
PyTorch and basic probability (KL divergence, mutual information by name). No prior exposure
to disentanglement assumed. This is a focused, **~15–18 session** course on one idea and its
sober limits. ~1 hour per day, one concept at a time, every concept checked with a small
exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The topic
numbers below are *topics*, not days. `progress.md` tracks the real position.

**Prerequisite:** VAEs (`ai-foundations/` Phase on autoencoders/VAEs, or equivalent). If the
ELBO and its KL term are shaky, rebuild them in Phase 0.2 before going on — the entire course
is an argument about *what that one KL term does*.

**Where it sits:** a **standalone** course, and an **enrichment** for the
[AI Music & Audio](../curricula/ai-music-audio.md) curriculum — it answers *what a VAE latent
encodes*, the question lurking behind that curriculum's continuous-VAE branch. It pairs with
[`flow-matching/`](../flow-matching/) (the decoder/generator side) the way disentanglement is
the representation side.

**The keystone — read [`the-decomposition.md`](the-decomposition.md) in Phase 0.1.** This
course has a **two-part keystone**: *(1) the decomposition* — the VAE's KL term splits exactly
into three pieces, and only the **total correlation (TC)** drives disentanglement (so that's
what to penalize); *(2) the impossibility* — Locatello proved the objective **alone** cannot
identify the factors without an **inductive bias**. Together: *every method = drive TC→0 +
supply an inductive bias.* We spend as long as it takes on **Phase 5** (the decomposition) and
**Phase 7** (the impossibility).

**The qubit (worked example):** **dSprites** — the field-standard synthetic benchmark with
**known ground-truth factors** (shape, scale, orientation, x, y). You *need* labelled factors
to teach and measure disentanglement, so dSprites leads: train VAEs on it, do **latent
traversals**, and compute **MIG**. The **payoff** is audio: **pitch ↔ timbre** (Luo 2019) — the
editing goal that motivates the whole curriculum (change the through-line clip's pitch without
its timbre). Same idea, synthetic to teach, audio to want.

**End state:** by the last lesson the learner can: define disentanglement and run a **latent
traversal**; explain **InfoGAN**'s mutual-information route and the **β-VAE** knob and its
reconstruction tax; explain **Burgess**'s information-bottleneck account and the **capacity
ramp**; *write the three-term KL decomposition from memory* and say why **TC** is the
disentanglement driver and **FactorVAE** / **β-TCVAE** isolate it; compute and compare
**β-VAE / FactorVAE / MIG** metrics and explain *why they disagree*; state **Locatello**'s
**impossibility theorem** and the >12,000-model findings, and what they demand (inductive
bias, many seeds, several metrics); and explain how **Luo** disentangles **pitch/timbre** with
**label supervision** — and why the self-supervised full-recording case is still open.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one frame.** The promise — **controllable, editable**
  generation, one factor per latent axis — and the two-part catch. Read
  [`the-decomposition.md`](the-decomposition.md): TC is *what to penalize*; Locatello is *why
  that's not enough*. Everything hangs between these two.
- **0.2** **Recap the VAE (from `ai-foundations`).** `q(z|x)`, `p(x|z)`, the ELBO =
  reconstruction − `D_KL(q(z|x) ‖ p(z))`, isotropic Gaussian prior `p(z)=N(0,I)`. **The whole
  course is about that one KL term** — what it costs, what it splits into, what it can't do.
  If it's shaky, rebuild it here.
- **0.3** **Tools.** `torch` + the **dSprites** dataset (737,280 binary 64×64 images,
  5 known factors). Confirm you can train a tiny VAE on dSprites and decode a reconstruction.
- **0.4** **The qubit.** dSprites (known factors, to teach/measure) + the audio payoff
  (pitch/timbre; the curriculum's editing goal). Why synthetic must lead: you can't *measure*
  disentanglement without ground-truth factors.

## Phase 1 — What "Disentangled" Even Means
- **1.1** **Factors of variation.** dSprites is generated from 5 independent factors (shape,
  scale, orientation, x, y). "Disentangled" = each latent dimension tracks **one** factor —
  **axis-alignment**. Draw the generative-factor picture.
- **1.2** **The latent traversal — the basic diagnostic.** Hold all but one `z_i` fixed, sweep
  `z_i`, decode, and *watch*. One thing changes → that axis is clean; two things change →
  entangled. This is the course's recurring picture; **run it today** on a quick VAE.
- **1.3** **Why we want it.** Editing/control, interpretability, claimed sample-efficiency.
  Keep "claimed" in scope — Phase 7 tests it.
- **1.4** **The slippery part.** There is **no single agreed formal definition** of
  disentanglement. Flag now that this vagueness bites hard later (it's half of why Locatello's
  result stings).

## Phase 2 — The GAN Precursor: InfoGAN
- **2.1** **InfoGAN (2016): the earliest scalable method**, from the **GAN** side. Split the
  generator input into noise `z` + a structured code `c`. Problem: a plain GAN can **ignore**
  `c`.
- **2.2** **The fix — maximize mutual information.** Add `−λ·I(c; G(z,c))` to the GAN objective
  so `c` must drive the output. `I` is intractable → maximize a **variational lower bound** with
  an auxiliary network **Q(c|x)** (sharing conv layers with the discriminator, so it's nearly
  free). Codes can be **categorical** or **continuous**.
- **2.3** **Results.** Unsupervised, the codes line up with semantics: MNIST **digit** (categorical)
  + **rotation**/**width** (continuous); faces pose/lighting. MI-maximization is the **ancestor**
  of the TC penalties in Phase 5 (all are MI-based).
- **2.4** **The caveats that foreshadow everything.** GAN instability; the number/type of codes
  is hand-chosen; and **which code grabs which factor is not identifiable** — the unsupervised
  limitation Phase 7 proves is fundamental.

## Phase 3 — The β Knob: β-VAE
- **3.1** **β-VAE (2017).** Weight the KL term by **β**: `L = E_q[log p(x|z)] − β·D_KL(q(z|x)‖p(z))`.
  With `p(z)=N(0,I)`, larger β pressures the posterior toward the **factorised** prior →
  axis-aligned factors. The foundational knob.
- **3.2** **The trade-off — the central tension.** β buys disentanglement but **costs
  reconstruction** (too-large β blurs). Phase 5 explains *why* and fixes it.
- **3.3** **The first metric.** The **β-VAE metric**: fix one factor, vary the others, encode
  pairs, train a **low-capacity linear classifier** to predict which factor was fixed. (Brittle
  — Phase 6 returns to this.) Note: a paper introducing a method *and* its own metric is a
  pattern worth distrusting.
- **3.4** **Pin to dSprites.** Train at **β = 1, 4, 10**; traverse each; watch clean axes emerge
  *and* reconstructions blur. The trade-off, seen.

## Phase 4 — Why β Works: the Information Bottleneck (Burgess)
- **4.1** **β-VAE as rate–distortion.** Read the KL term as a **rate** — bits the latent encodes
  about the input. Large β **constricts the bottleneck**.
- **4.2** **Capacity allocation.** A tight, gradually-filled bottleneck makes the encoder spend
  its limited rate where it most cuts reconstruction error — and since natural factors are
  roughly independent, it encodes **one factor at a time**. **Disentanglement is a byproduct of
  a tight bottleneck**, not magic in β.
- **4.3** **The fix — controlled capacity increase (AnnealedVAE).** Instead of clamping a fixed
  high β, target a capacity **C** (nats) and **ramp C up** from 0:
  `L = E_q[log p(x|z)] − γ·|D_KL(q(z|x)‖p(z)) − C|`. Adds factors into **new** dimensions as C
  grows — axis-alignment kept, reconstruction restored.
- **4.4** **Pin to dSprites.** Capacity ramp vs fixed-β: cleaner traversals *and* sharper
  reconstructions. (This is the **rate-distortion** explanation of β; Phase 5 gives the
  *KL-decomposition* explanation — two lenses on the same knob.)

## Phase 5 — Isolating Total Correlation (keystone)
> Spend as long as it takes. This is *what to penalize*. Re-read [`the-decomposition.md`](the-decomposition.md).
- **5.1** **The question.** What part of β-VAE's KL penalty actually disentangles — and what
  part just hurts reconstruction?
- **5.2** **The decomposition (the keystone equation).** The expected KL splits **exactly**:
  `E_x[D_KL(q(z|x)‖p(z))] = I_q(z;x) + D_KL(q(z)‖Πⱼq(zⱼ)) + Σⱼ D_KL(q(zⱼ)‖p(zⱼ))` —
  **index-code MI** + **total correlation (TC)** + **dimension-wise KL**. **TC** = dependence
  among latent dims = the disentanglement driver. Derive/parse each term until the learner can
  *write it from memory*.
- **5.3** **Why β-VAE over-penalizes.** A single β raises **all three** — including index-code
  MI, which you *need* for reconstruction. That's the reconstruction tax, explained.
- **5.4** **FactorVAE (2018): TC via a discriminator.** Penalize **TC only**:
  `L = ELBO − γ·TC(q(z))`, with TC estimated by a **density-ratio discriminator** (tell real
  `q(z)` from dimension-**shuffled** samples `≈ Πⱼ q(zⱼ)`). Adversarial; noisy in high dim.
- **5.5** **β-TCVAE (2018): TC via sampling.** Same TC target, estimated by **minibatch-weighted
  sampling** — **no extra network**, a drop-in objective change. (Two papers, same month, same
  insight, different estimator.)
- **5.6** **The payoff.** **Equal disentanglement at better reconstruction** than β-VAE — because
  you stopped penalizing the index-code MI. **TC is the operative quantity.**
- **5.7** **Pin to dSprites.** β-TCVAE vs β-VAE at *matched* reconstruction; the TC penalty
  separates what β had entangled.

## Phase 6 — Measuring It (and Why Metrics Disagree)
- **6.1** **The metric zoo.** **β-VAE metric** (linear classifier — brittle); **FactorVAE
  metric** (majority-vote over the lowest-variance latent dim for a fixed factor — fewer
  hyperparameters); **MIG** (Mutual Information Gap — the robust, classifier-free standard).
- **6.2** **MIG in detail.** For each factor, the **normalized gap between the two highest-MI
  latent dimensions**. **Classifier-free** (no metric-side training), axis-aligned. Why that
  robustness matters.
- **6.3** **They all need ground-truth factors.** Every metric assumes a labelled synthetic
  generator (dSprites). Real recordings (room, channel, performer) have **no labels** — the
  metrics don't transfer. (Phase 8's open problem.)
- **6.4** **Pin to dSprites.** Compute **MIG** on your β-VAE and β-TCVAE models; see MIG track TC
  across models — supporting "TC is the operative quantity."

## Phase 7 — The Reality Check: Locatello (keystone)
> Spend as long as it takes. This is *why the objective isn't enough* — the second half.
- **7.1** **The impossibility theorem.** A factorised prior `N(0,I)` is **rotation-invariant**:
  rotate the latent axes and the marginal is unchanged. So for any disentangled model there are
  **infinitely many entangled** ones (rotations) with the **same marginal** — indistinguishable
  to an unsupervised objective. **You cannot identify the factors without an inductive bias.**
- **7.2** **The >12,000-model study.** 6 methods × 6 metrics × 7 datasets × many seeds
  (~10,000 GPU-hours): **metrics disagree** (weakly correlated); aggregate-posterior **TC is not
  post-hoc predictive**; **random seeds dominate** method choice; **no evidence** disentanglement
  improves downstream sample-efficiency.
- **7.3** **What the paper urges.** Be **explicit** about inductive bias / (weak) supervision;
  report **distributions over seeds**, not best runs; never equate one metric with
  "disentanglement." This reframes the field: not "which loss" but "**which inductive bias**."
- **7.4** **The misreading to kill.** "β-VAE/β-TCVAE disentangle for free, unsupervised." No —
  they're inductive biases, not guarantees; seeds can dominate β. State it in your own words.

## Phase 8 — Into Audio, and the Open Frontier
- **8.1** **Luo et al. (2019): pitch ↔ timbre.** Two VAEs over spectrogram frames, each with a
  **pitch latent** and a **timbre latent** — one using a **Gaussian-mixture** pitch latent (one
  component per pitch class), one adding **skip connections + adversarial** training. Crucially
  **supervised by frame-level pitch + instrument labels** — *the inductive bias Locatello
  demands*, supplied in practice.
- **8.2** **The editing payoff.** Recombine one note's **pitch** code with another's **timbre**
  code → **swap/transfer** (pitch-shift without changing instrument; timbre transfer). Downstream
  wins: instrument classification, music segmentation. *This* is why the curriculum cares — edit
  the through-line clip's pitch without its timbre.
- **8.3** **Two routes for audio.** **Explicit/parametric** ([DDSP](https://magenta.tensorflow.org/ddsp):
  pitch/loudness/timbre by construction — legible but bounded) vs **learned latent** (this
  course — expressive but needs a bias for identifiability). Resynthesis wants both: learned
  expressivity, parametric control.
- **8.4** **The open frontier.** **Self-supervised, decodable, attribute-disentangled**
  representations of **full recordings** — separating room / channel / performer from composition,
  *without labels* — is **unsolved**. The decoder side (rectified-flow DiT, RAVE) is mature; the
  disentangled-representation side is not. The missing inductive bias is the whole game.
- **8.5** **Capstone — disentangle and diagnose.** Tiered a/b/c, no GPU required (dSprites VAEs
  are small):
  - **(a) CPU / default.** Train a **β-VAE** on dSprites (or a subset); latent traversals at
    **β = 1, 4, 10**; compute **MIG**; write a one-page "disentanglement report" — which axes
    are clean, what the trade-off looks like.
  - **(b) Colab GPU.** Add **β-TCVAE** (and optionally FactorVAE); compare at matched
    reconstruction; run **multiple seeds** to *witness Locatello's seed variance*; try the
    **capacity ramp**.
  - **(c) Local GPU / audio.** Reproduce a **pitch/timbre** split on monophonic notes
    (NSynth-style or the Luo setup) with label supervision; do a **timbre/pitch swap** and
    **listen** — the ear as oracle, the curriculum payoff made audible.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If shaky,
   re-teach before continuing.
2. **Introduce one new concept** with a picture *before* notation. The recurring picture is the
   **latent traversal** (`the-decomposition.md`): sweep one `z_i`, decode, watch. Draw on it
   constantly.
3. **Pin it to dSprites.** Train, traverse, measure. The **traversal** (a plot) and **MIG** (a
   number) are this course's oracle — and for the audio tier, the **ear** (swap and listen).
4. **Tiny exercise** to verify: predict a traversal ("raise β — disentanglement and
   reconstruction go which way?"), write the three-term KL decomposition, or run a few lines
   that compute MIG. The exercise *is* the check.
5. **Common misreadings** when relevant — keep [`the-decomposition.md`](the-decomposition.md)'s
   list live; flag and correct on the spot, note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to `progress.md` and
   the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in one or two sentences ("TC is the dependence among latent dims; penalizing
   only TC disentangles *without* taxing reconstruction the way β-VAE's whole-KL penalty does").
2. Carry out the small task: run a latent traversal, write the KL decomposition, compute/compare
   MIG, or reason about seed variance — and explain it.
3. Spot a deliberately wrong claim ("β-TCVAE disentangles for free, unsupervised" — no, it's an
   inductive bias; "high MIG proves disentanglement" — no, metrics disagree, average over seeds).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wiki this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Read / link these on JOS's machine:

- **[`disentanglement/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/disentanglement/wiki)** — the home wiki. Concept pages:
  `overview.md` (the 2016→2019 arc), **`vae-disentanglement-methods.md`** (the β-VAE → TC line +
  the key identity), **`disentanglement-metrics.md`** (β-VAE / FactorVAE / MIG, and why they
  disagree), **`audio-disentanglement.md`** (the music-domain instance + resynthesis frontier).
  Source summaries: `infogan-chen-2016`, `beta-vae-higgins-2017`,
  `burgess-understanding-beta-vae-2018`, `factorvae-kim-2018`, `beta-tcvae-chen-2018`,
  `locatello-2019`, `timbre-pitch-luo-2019`.
- **[`ai-music-audio-gen/wiki/`](https://cm-gitlab.stanford.edu/jos/music423-2023/-/tree/master/ai-music-audio-gen/wiki)** — for the audio bridge:
  `concepts/self-supervised-audio-representations.md` (resynthesis, the open frontier) and
  `sources/rave.md` (the β knob in a real audio VAE).
- Keep the course in sync if the wiki gains papers; the wiki is canonical, the course is the
  lesson plan over it.

### Source papers (the lineage this course tracks)
- **Chen et al. (2016)** — *InfoGAN*. arXiv:1606.03657.
- **Higgins et al. (2017)** — *β-VAE*. ICLR 2017 (OpenReview `Sy2fzU9gl`).
- **Burgess et al. (2018)** — *Understanding Disentangling in β-VAE*. arXiv:1804.03599.
- **Kim & Mnih (2018)** — *FactorVAE (Disentangling by Factorising)*. arXiv:1802.05983.
- **Chen et al. (2018)** — *β-TCVAE (Isolating Sources of Disentanglement)*. arXiv:1802.04942.
- **Locatello et al. (2019)** — *Challenging Common Assumptions in the Unsupervised Learning of
  Disentangled Representations* (ICML best paper). arXiv:1811.12359.
- **Luo et al. (2019)** — *Disentangled Representations for Timbre and Pitch in Music Audio*
  (ISMIR). arXiv:1811.03271.
