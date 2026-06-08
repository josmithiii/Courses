# Neural Audio Codecs — From Waveforms to Tokens and Latents

**Learner profile:** Has finished `ai-foundations/` (or equivalent): comfortable
with MLPs, backprop, PyTorch, CNNs, attention/Transformers, LLMs, and *basic*
diffusion. **No DSP background assumed** — sampling, the spectrogram, and the mel
scale are taught briskly, intuition-first, with links out to JOS's DSP books for
depth. The learner is ML-first: they know what an autoencoder is, so we move fast to
the part that's new — how audio becomes the discrete tokens and continuous latents
that *every* modern audio generator consumes. ~1 hour per day. One concept at a
time. Every concept verified with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one topic. The
topic numbers below are *topics*, not days. `progress.md` tracks the real position.

**The keystone — read [`the-fork.md`](the-fork.md) in Phase 0.1.** This course has one
organizing idea, the analogue of room-acoustics' Schroeder frequency: a neural audio
codec can hand its downstream model either **discrete RVQ tokens** (which feed a
*language model*) or a **continuous VAE latent** (which feeds a *diffusion
transformer*). That single representational choice **forks the entire field** into the
two paradigms taught in courses 2 and 3 of this curriculum. Everything here builds
toward making that fork legible. We spend as long as it takes on Phase 5.

**The qubit (worked example):** the curriculum's shared **~2-second solo-piano clip**
(`../curricula/assets/ai-music-audio/through-line.wav`, mono 24 kHz). We carry *this
one clip* through every representation — waveform → mel → continuous latent → VQ
tokens → RVQ codebooks — and **listen** to it reconstructed at each stage. Same clip,
every box in the pipeline. (Courses 2 and 3 pick it up from here: continue/infill its
tokens, denoise its latent.)

**End state:** by the last lesson the learner can: explain why audio is sampled and
quantized, and read a waveform / spectrogram / mel-spectrogram; explain what an
autoencoder bottleneck is and why a *VAE* gives a smooth continuous latent; explain
vector quantization, the straight-through estimator, and codebook collapse; explain
residual VQ and compute a codec's bitrate from (N_q, codebook size, frame rate);
place SoundStream / EnCodec / DAC on a quality–bitrate map and say what each added;
**state the discrete-token-vs-continuous-VAE fork and predict which downstream
paradigm each feeds**; distinguish semantic vs acoustic tokens; name the right
evaluation metric for a given question; and run a real pretrained codec to encode,
inspect, and reconstruct the clip.

---

## Phase 0 — Orientation
- **0.1** **The whole course in one picture**, no notation yet: raw audio is a
  firehose of samples; modern generators don't model samples directly, they model a
  *compressed representation* a neural codec produces. Read [`the-fork.md`](the-fork.md)
  — the discrete-token vs continuous-VAE fork is the destination. Where this course
  sits in the `ai-music-audio` curriculum (foundation for courses 2 and 3).
- **0.2** **Tools.** `torch` + `torchaudio` installed and importable; load the
  through-line clip, print its shape and sample rate, play it, plot the waveform.
  Confirm matplotlib works. (Optional: `IPython.display.Audio` in a notebook so
  reconstructions are audible inline.)
- **0.3** **Crash-start audio intuition.** A sound is air-pressure-over-time; a digital
  audio signal is that pressure *sampled* at a fixed rate into an array of numbers.
  That's the only mental model needed to start Phase 1. Listen to the clip; look at
  its raw sample array.

## Phase 1 — Digital Audio & Time–Frequency (brisk, intuition-first)
> One phase. Enough DSP to understand what a codec's encoder eats and decoder emits.
> Depth lives in JOS's DSP books (linked below) — we build intuition and move on.
- **1.1** **Sampling.** Continuous pressure → discrete samples at rate `fs` (24 kHz =
  24000 numbers/second). The sample rate sets the highest representable frequency
  (`fs/2`, the Nyquist frequency) — one sentence on why, no proof. Why audio codecs
  pick rates like 16 / 24 / 44.1 kHz. Inspect: the clip is ~48000 samples.
- **1.2** **Quantization.** Each sample is a real number stored in finite bits
  (16-bit PCM = 65536 levels). This is *scalar* quantization — preview that the whole
  course is about doing this *better* with *vectors* (Phase 3). Rounding error = noise.
- **1.3** **From time to frequency.** The waveform hides structure; the **STFT**
  (short-time Fourier transform) slices it into overlapping frames and shows, per
  frame, how much energy sits at each frequency → the **spectrogram**. Intuition:
  "a piano roll the computer can see." Compute and plot the clip's spectrogram with
  `torchaudio`.
- **1.4** **The mel spectrogram.** Human pitch perception is roughly logarithmic, so we
  warp the frequency axis onto the **mel** scale and keep ~80–128 bands. Why nearly
  every audio model uses **mel** as a front-end or training target. Plot the clip's
  mel-spectrogram next to its linear one.
- **1.5** **Two reconstruction routes back to sound** (preview of the whole field):
  (i) invert the STFT (needs phase → Griffin–Lim or a neural **vocoder**);
  (ii) a learned decoder. Flag now: *mel throws away phase* — recovering listenable
  audio from mel is itself a learned problem. This is part of why codecs exist.

## Phase 2 — Autoencoders & the Bottleneck (the continuous latent)
- **2.1** **Autoencoder recap (fast — they know this).** Encoder `E` squeezes input to
  a low-dim **latent** `z`; decoder `D` reconstructs; train on reconstruction loss.
  The **bottleneck** forces compression. Frame a codec as *an autoencoder for audio*.
- **2.2** **A convolutional audio autoencoder.** A 1-D conv encoder downsamples the
  waveform in time (stride) into a sequence of latent vectors — one latent *frame* per
  chunk of samples. Define the **frame rate** (latents/second) vs the sample rate; the
  ratio is the **downsampling / stride factor**. Pin to the clip: 24 kHz audio → e.g.
  75 Hz latent frames is a 320× time compression.
- **2.3** **Why reconstruction loss alone isn't enough** (preview of Phase 4's GAN
  ingredient). L2 on the waveform → blurry / buzzy audio; the ear hears artifacts L2
  doesn't penalize. Name the fix now (spectral losses + adversarial training), detail
  it in Phase 4.
- **2.4** **AE → VAE: the continuous latent.** The plain AE latent is an arbitrary
  point cloud; a **VAE** regularizes it toward a smooth, well-behaved distribution
  (encoder outputs a mean+variance, KL pulls it toward a prior). *That smoothness is
  exactly what a diffusion model needs to denoise in.* **Flag the fork here for the
  first time:** keep the latent **continuous** (VAE) → it will feed diffusion (course
  3); make it **discrete** (next phase) → it will feed a language model (course 2).

## Phase 3 — Discrete Representations: VQ-VAE
- **3.1** **The idea.** Replace the continuous latent with the **nearest entry in a
  learned codebook** of `K` vectors. Now each latent frame is an *index* (a token) —
  audio has become a sequence of discrete symbols, like text. (van den Oord et al.
  2017, VQ-VAE.)
- **3.2** **The straight-through estimator.** `argmin`-over-codebook has zero gradient;
  the **STE** copies the decoder's gradient straight past the quantizer to the encoder
  so the whole thing trains end-to-end. Derive why this is needed and what it
  approximates.
- **3.3** **The VQ losses.** Reconstruction + **codebook loss** (move codes toward
  encoder outputs) + **commitment loss** (keep the encoder from running away from its
  chosen codes). EMA codebook updates as the common alternative. Write the three terms.
- **3.4** **Codebook collapse** — the central failure mode. Only a few codes ever get
  used; the rest die. Why it happens and the standard fixes (k-means init, EMA, code
  re-seeding, **factorized / low-dim codebook lookup** à la DAC, and **FSQ** which drops
  the learned codebook entirely for fixed scalar rounding). A "common misreading"
  magnet — see [`the-fork.md`](the-fork.md)'s list.
- **3.5** **Pin to the clip.** Encode the clip to VQ tokens; visualize the index
  sequence and a histogram of code usage (watch for collapse); reconstruct and listen.

## Phase 4 — Residual VQ & Real Neural Codecs
- **4.1** **One codebook is too coarse.** A single VQ stage at a usable bitrate sounds
  bad. **Residual VQ (RVQ):** quantize, take the *residual* (what the first codebook
  missed), quantize *that* with a second codebook, repeat for `N_q` stages. Each stage
  refines the last. (Misreading to kill: more codebooks is **residual refinement**, not
  independent "more quality knobs"; the stages are interdependent and ordered.)
- **4.2** **The bitrate formula.** `bitrate = N_q × log₂(K) × frame_rate`. Work it by
  hand for the clip: e.g. `N_q=8`, `K=1024`, `frame_rate=75 Hz` → `8 × 10 × 75 = 6000`
  bits/s = 6 kbps. Change each knob, predict the effect on bitrate *and* on quality.
- **4.3** **Bitrate flexibility from one model.** **Quantizer dropout** trains the codec
  so you can use the first `n < N_q` codebooks at inference for a lower bitrate (the
  RVQ prefix property). One model, a whole bitrate curve.
- **4.4** **The adversarial ingredient.** Why real codecs add **discriminators** (MSD /
  MPD / MS-STFT) plus feature-matching + spectral losses on top of reconstruction —
  this is what turns "buzzy" into "transparent." (Lineage: HiFi-GAN / MelGAN
  discriminators → codecs.) Intuition only; no GAN training from scratch.
- **4.5** **The three reference codecs.** **SoundStream** (2021, first end-to-end RVQ
  codec) → **EnCodec** (2022, MS-STFT discriminator, gradient balancer, transformer
  entropy coding for 25–40% fewer bits) → **DAC / Improved RVQGAN** (2023, Snake
  activation, factorized codebooks fixing collapse, ~90× compression at 8 kbps). Place
  each on a quality–bitrate map; say in one line what each *added*.
- **4.6** **Pin to the clip.** Sweep the clip through `N_q = 1, 2, 4, 8` codebooks of a
  real codec and **listen to the quality climb**; plot bitrate vs a quality proxy.

## Phase 5 — The Fork (the keystone — spend as long as it takes)
> The seam of the whole curriculum. Re-read [`the-fork.md`](the-fork.md) here.
- **5.1** **State it precisely.** A trained audio autoencoder's bottleneck is *either* a
  stack of **discrete RVQ token indices** *or* a **continuous VAE latent tensor**.
  These are not interchangeable details — they are two different *kinds* of object.
- **5.2** **Why discrete tokens → a language model.** Tokens are symbols in a finite
  vocabulary, exactly what a Transformer LM predicts. "Generate audio" becomes "predict
  the next codec token." This is the **AudioLM → MusicGen → VALLE** lineage = **course
  2** (`audio-codec-lms`).
- **5.3** **Why a continuous latent → diffusion.** Diffusion / flow denoise *continuous*
  vectors. "Generate audio" becomes "denoise a VAE latent." This is the **AudioLDM →
  Stable Audio → DiT** lineage = **course 3** (`audio-diffusion-dit`), and it's why
  course 3 leans on `flow-matching/`.
- **5.4** **Kill the conflations head-on** (the misreadings that motivate the whole
  course): "a neural codec is *just* a VAE" (no — discrete-RVQ vs continuous-VAE *is*
  the fork); "audio codec → DiT uses the discrete codec tokens" (no — it's the
  continuous VAE latent); "more RVQ codebooks = independent quality"; "discrete codec
  tokens are lossless." The learner should be able to *predict the downstream paradigm*
  from the representation, and *catch* each wrong claim.

## Phase 6 — Semantic vs Acoustic Tokens; Evaluation
- **6.1** **Two kinds of token.** **Acoustic** tokens (from a codec's RVQ) carry
  fidelity but little long-range structure; **semantic** tokens (from self-supervised
  models like w2v-BERT) carry structure / melody but not fine audio detail. AudioLM's
  insight: use *both*, hierarchically. (Detailed in course 2; introduced here because
  it's a *representation* distinction — and a classic conflation to flag.)
- **6.2** **Parallel decoding preview — SoundStorm.** Codec token grids can be decoded
  non-autoregressively (mask-and-fill) far faster than left-to-right. Why the
  *codebook × frame grid* shape makes this possible (bridges to course 2's masked
  models).
- **6.3** **Evaluation — picking the right ruler.** Reconstruction fidelity vs
  perceptual quality vs generation quality need *different* metrics: **ViSQOL / PESQ /
  SI-SDR / mel-distance** for reconstruction, **MUSHRA / MOS** (human) for perceptual,
  **FAD / FID** for generation. Which question each answers; why waveform-L2 is a poor
  ear.
- **6.4** **Pin to the clip.** Compute a couple of reconstruction metrics on the clip at
  two bitrates; confirm the numbers track what the ear reports.

## Phase 7 — Putting It Together
- **7.1** **The pipeline end-to-end**, on the clip: waveform → (STFT / mel view) →
  conv-encoder → bottleneck → **fork** (RVQ tokens *or* VAE latent) → decoder →
  waveform. Recite which 2024–2026 systems sit on each branch.
- **7.2** **Capstone — encode/decode the clip through a real codec and inspect the
  codebooks.** Tiered like room-acoustics' a/b/c so it runs with or without a GPU:
  - **(a) CPU / pretrained-checkpoint inference (default).** `pip install` a pretrained
    codec (EnCodec via `transformers` / `audiocraft`, or **DAC**). Encode the
    through-line clip → inspect the discrete codes (shape `[N_q, T]`, code-usage
    histogram) → decode → A/B the reconstruction at `N_q = 1, 2, 4, 8` and a couple of
    bitrates. Write a one-page "codec report" on the clip.
  - **(b) Colab GPU.** Same, plus run a *second* codec at a *different* sample rate and
    compare reconstructions and bitrates on the same clip; add ViSQOL / mel-distance.
  - **(c) Local GPU.** Additionally train a *tiny* VQ-VAE on a small audio set from
    scratch and watch codebook collapse (and a fix) happen live.
- **7.3** **Where to go next.** You can now read SoundStream / EnCodec / DAC and the
  AudioLM intro. The fork hands you off: **discrete tokens → course 2**
  (`audio-codec-lms`); **continuous latent → course 3** (`audio-diffusion-dit`, with
  `flow-matching/` as enrichment).

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question. If
   shaky, re-teach before continuing.
2. **Introduce one new concept** with an analogy or a picture *before* notation. Audio
   is unusually concrete — a plot or, better, a *listen* beats a formula. When notation
   lands, name it, say what it is in plain English, then say what it lets us compute.
3. **Pin it to the clip.** Almost every object in this course can be made audible or
   plottable on the one through-line clip. Do that. Reconstruct and **listen** whenever
   a representation changes — the ear is the oracle here, the way the 2-D scatter plot
   is in `flow-matching`.
4. **Tiny exercise** to verify: a few lines of `torch` / `torchaudio`, a by-hand
   bitrate calculation, or a prediction ("more codebooks → ?") checked against a
   runnable cell. The exercise *is* the check that the idea landed.
5. **Common misreadings** when relevant — keep [`the-fork.md`](the-fork.md)'s list live;
   flag and correct on the spot, and note recurrences in `progress.md`.
6. **Log** what was covered, the exercise, the answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of next time.

### Mastery criteria
A topic is mastered when the learner can:
1. State the idea in their own words in one or two sentences ("RVQ refines the residual
   stage by stage; the bitrate is `N_q·log₂K·frame_rate`").
2. Carry out the small computation: a bitrate calc, a `torchaudio` plot, an encode /
   decode-and-listen, or a code-usage histogram — and explain each step.
3. Spot a deliberately wrong claim ("audio codec → DiT means the DiT consumes the
   discrete RVQ tokens" — no, it's the *continuous VAE latent*).

Record this in the data-dir `progress.md` mastery log.

---

### Source of truth — the curated wiki this course teaches from
This course is the *pedagogical* front-end of a curated knowledge base; the wiki stays
canonical, the course stays pedagogical. Read / link these on JOS's machine:

- **`/w/music423-2023/ai-audio-codecs/wiki/`** — the home wiki for this course.
  Key pages: `overview.md` (the convergence arc), `vector-quantization.md`,
  `residual-vector-quantization.md`, `neural-audio-codecs.md`, `codebook-learning.md`
  (collapse + fixes + FSQ), `audio-representations.md`, `bitrate-scalability.md`,
  `adversarial-training-audio.md`, `evaluation-metrics.md`, and
  `timeline-ai-audio-codecs.md`.
- **Source summaries** under `…/wiki/sources/`: `vq-vae`, `soundstream`, `encodec`,
  `descript-rvqgan` (DAC), `fsq`, `hifigan`, `melgan`, `gansynth`, `audiolm`,
  `musiclm`, `soundstorm`.

### DSP depth (Phase 1 links out here — ML-first learners don't need it to proceed)
JOS's books, for any learner who wants the signal-processing under the hood:
*Mathematics of the DFT*, *Spectral Audio Signal Processing*, and *Introduction to
Digital Filters* (the `ccrma.stanford.edu/~jos/` series). Phase 1 cites them and
moves on.

### Source papers (the codecs this course tracks)
- **Gray (1984)** — VQ theory / LBG (the foundation Phase 3 stands on).
- **van den Oord, Vinyals, Kavukcuoglu (2017)** — *Neural Discrete Representation
  Learning* (VQ-VAE). arXiv:1711.00937.
- **Zeghidour et al. (2021)** — *SoundStream*. arXiv:2107.03312.
- **Défossez et al. (2022)** — *EnCodec* (*High Fidelity Neural Audio Compression*).
  arXiv:2210.13438.
- **Kumar et al. (2023)** — *Improved RVQGAN / DAC*. arXiv:2306.06546.
- **Mentzer et al. (2023)** — *Finite Scalar Quantization*. arXiv:2309.15505.
- **Borsos et al. (2022)** — *AudioLM* (semantic + acoustic tokens; the bridge to
  course 2). arXiv:2209.03143.
