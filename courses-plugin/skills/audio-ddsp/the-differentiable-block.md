# The Differentiable Block — This Course's Keystone

Audio-codecs has the fork; flow-matching has the conditional-expectation identity.
**This course has the differentiable block.** One idea, stated twice: *(i)* a DSP block
whose output is an explicit, differentiable function of its parameters can sit inside a
training loop and have those parameters learned by gradient descent; *(ii)* the loss you
put after it has to be one that *hears* — a **multi-scale spectral loss**, not a
sample-by-sample waveform error — or the gradient points the wrong way. Read this in
Phase 0.1, return to it in **Phase 2** (where we derive both halves by hand), **Phase 4**
(where IIR recursion strains it), and **Phase 6.1** (where you recite it from memory).

Every term in **bold** is earned somewhere in the syllabus; the phase that earns it is
noted in brackets.

---

## The keystone, in one sentence

> A **DSP block** [Phase 1] is a function `y = g(θ; x)` from parameters `θ` (and maybe an
> input `x`) to audio `y`. If `g` is built from differentiable operations — sums of
> sinusoids, linear filters, convolutions, smooth nonlinearities — **autograd** [Phase 2.1]
> gives `∂L/∂θ` for free, and a **spectral loss** `L` [Phase 2.3] that compares
> `g(θ)` to a target by *magnitude spectra at several resolutions* makes that gradient
> point toward what the ear wants.

```
   parameters θ  ──▶  differentiable DSP block  g(θ)  ──▶  audio  y
        ▲                 (oscillator bank, filter,                │
        │                  noise shaper, reverb, …)                ▼
        │                                                 multi-scale spectral loss
        └──────────────── ∂L/∂θ  via autograd ◀────────── L(|STFT(y)|, |STFT(target)|)
```

The **inductive bias** [Phase 3.1] is the point: the block already knows that a plucked
string is quasi-periodic, that a filter has poles inside the unit circle, that a reverb
is a convolution. The network (if any) only has to learn the *parameters* — which is why
DDSP learns a convincing instrument from **13 minutes** of audio where a black-box
waveform model needs hours, and why the result stays legible and editable.

## Half one: what "differentiable" buys — and costs

- **Additive / harmonic oscillator** [Phase 1.2, 3.2]. `y[n] = Σ_k A_k[n] sin(φ_k[n])`,
  `φ_k[n] = φ_k[n-1] + 2π k f₀[n]/f_s`. Differentiable in the amplitudes `A_k` and in
  `f₀`. But the gradient w.r.t. frequency is **oscillatory**: a small `f₀` error produces
  a large waveform difference and a spectral-loss landscape full of local minima (the
  "frequency-estimation problem" the DDSP review names). Practical DDSP therefore
  *estimates* `f₀` with a known extractor (CREPE) and *learns* the amplitudes.
- **Filtered noise via frequency sampling** [Phase 1.3, 3.3]. Predict a magnitude
  response per frame, take its IFFT to get a windowed FIR, overlap-add. FIR by
  construction — trivially differentiable and GPU-parallel.
- **IIR filters** [Phase 4.1]. `y[n] = Σ b_i x[n-i] − Σ a_j y[n-j]` is a **constrained
  RNN**; training is backprop-through-time, sequential, and only stable if the poles stay
  inside the unit circle. Three responses, each a whole paper: *train it anyway with
  truncated BPTT and a stability parameterization* (Kuznetsov 2020), *train in the
  frequency domain by comparing responses* (Nercessian 2021 biquads), or *replace the IIR
  with an FIR approximation by frequency sampling* (Lee 2021 reverb). **The IIR-vs-FIR
  trade-off** — compact and musical vs parallel and memory-hungry — recurs everywhere.
- **Nonlinear and time-varying blocks** [Phase 4.3–4.5]. Waveshapers, compressors
  (gain computer + level detector), phasers (all-pass cascade + LFO): differentiable in
  principle, but each adds its own gradient pathology (saturation flattens gradients; an
  LFO must be learned jointly with the thing it modulates).

## Half two: the loss must hear

- **Waveform L2 is the wrong ruler** [Phase 2.2]. Two renderings of the same note with
  partials shifted by a few cents, or with a different starting phase, are
  perceptually identical and *maximally* far apart in sample-wise error. The gradient of
  waveform-MSE w.r.t. `f₀` is essentially noise.
- **Multi-scale spectral loss** [Phase 2.3]. `L = Σ_s ( ‖|S_s(y)| − |S_s(t)|‖₁ +
  ‖log|S_s(y)| − log|S_s(t)|‖₁ )` over FFT sizes `s ∈ {64, 128, …, 2048}`. Magnitude
  only (phase-blind, so phase differences don't count), several resolutions (short
  windows see transients, long windows resolve partials), log term (quiet partials
  matter). This is the default DDSP objective and the reason the harmonic model trains.
- **Parameter loss vs audio loss** [Phase 2.4]. If you *have* ground-truth parameters
  (synthetic data), L2 on `θ` is fast — but perception is **many-to-one** in `θ`, so
  audio-domain loss wins whenever it can be computed. This is the seam into course 2.
- **What spectral loss still misses** [Phase 2.5]. Phase coherence between partials,
  stereo, transients under long windows, inharmonic and noisy material. Adversarial,
  scattering (JTFS), and learned-embedding losses are the responses (course 2, Phase 4).

## Why this is *the* keystone

Every paper in the `ddsp/` directory is a choice of **which block** to make
differentiable and **which loss** to put after it. Engel 2020 = harmonic oscillator +
filtered noise + convolutional reverb, multi-scale spectral loss. Kuznetsov 2020 = IIR
as RNN, BPTT. Nercessian 2021 = biquad cascade, frequency-domain loss. Lee 2021 = reverb
as FIR-approximated velvet noise. Caspe 2022 = FM operators (and the local-minima price).
Wright 2022 = the *structure* of a compressor with a learned one-pole detector. Get the
keystone and each paper is one row in a table; miss it and they are twenty unrelated
tricks.

---

## The misreadings this course exists to kill

Curated from the `ddsp/` and `synth-effect-matching/` wikis. The tutor flags each on
the spot and logs recurrences in `progress.md`.

| Misreading | The correction | Earned in |
|---|---|---|
| "DDSP is a neural synthesizer." | DDSP is **classical DSP as the output layer**; the network (if any) only predicts *parameters*. The synthesizer is an oscillator bank and filters you could write by hand. | Phase 0.1, 3.1 |
| "Just minimize waveform MSE." | Waveform error is **phase- and cents-sensitive**; the ear is not. Use a **multi-scale spectral loss** (or better). | Phase 2.2–2.3 |
| "Everything differentiable is easy to train." | Oscillator **frequency** gradients are oscillatory (local minima); **IIR** recursion is sequential and unstable; **FM** parameters are a minefield. Differentiable ≠ well-conditioned. | Phase 2.1, 4.1, 5.1 |
| "Make the IIR an FIR and the problem disappears." | FIR approximation buys parallelism at the cost of **memory** for long responses and of exactness; it is one of three trade-offs, not a free lunch. | Phase 4.1–4.2 |
| "Parameter loss is fine if I have the parameters." | Perception is **many-to-one** in parameter space; two far-apart `θ` can sound alike. Audio-domain loss whenever possible. | Phase 2.4 |
| "Spectral loss is a perceptual metric." | It is a **magnitude** metric at a few resolutions — blind to phase coherence, weak on transients and inharmonic/noisy sounds. Good default, not ground truth. | Phase 2.5 |
| "The learned model is a black box like WaveNet." | Every learned quantity is a **DSP parameter with a name** (harmonic amplitude, cutoff, IR, threshold) you can read, plot, and edit after training — that legibility is the whole reason to use DDSP. | Phase 3.4, 6.1 |
