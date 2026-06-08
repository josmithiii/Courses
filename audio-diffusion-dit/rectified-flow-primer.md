# A Self-Contained Rectified-Flow Primer

*Read this in Phase 6.1.* It is **enrichment, not a gate**: everything you need to
understand FluxMusic's training objective is here. For the full treatment — Lipman's
conditional flow matching, Liu's rectified flow, Tong's OT-CFM, all pinned to a 2-D toy
distribution you train from scratch — take the [`flow-matching/`](../flow-matching/)
course, which this primer is a two-page trailer for.

The one thing to carry away: **a DiT can be trained as a *diffusion* model or as a
*flow* model with almost no architectural change — only the *target* the network
regresses onto changes.** FluxMusic chooses flow.

---

## 1. Both diffusion and flow connect noise to data along a path

Pick a data latent `z₁` (a clean VAE latent — from the through-line clip, say) and a
noise sample `z₀ ∼ N(0, I)`. Define a **path** `z_t` that interpolates between them as
`t` runs from 0 (pure noise) to 1 (clean data). Diffusion and flow differ only in
*which path* and *what the network learns about it*.

- **Diffusion (DDPM/score)** uses a curved, noise-adding path and trains the network to
  predict the **noise** `ε` added at each level (equivalently the **score**
  `∇ log p_t`, course 0.2). Sampling integrates a stochastic or probability-flow
  trajectory backward.
- **Flow matching / rectified flow** uses the **straight line**
  `z_t = (1 − t) · z₀ + t · z₁` and trains the network to predict the constant
  **velocity** that walks along it.

## 2. Rectified flow: the straight-line velocity

On the straight-line path, the velocity is trivially the displacement:

```
   z_t = (1 − t)·z₀ + t·z₁        ⇒        dz_t/dt = z₁ − z₀   (constant in t)
```

So the training target is just **`z₁ − z₀`**: "from this noise sample, head straight
toward this data sample." The network `v_θ(z_t, t, c)` (a **DiT**, conditioned on text
`c`) regresses onto that velocity:

```
   L = E_{t, z₀, z₁} ‖ v_θ(z_t, t, c) − (z₁ − z₀) ‖²
```

That's the whole objective. Compare diffusion's `L = E‖ε_θ(z_t, t, c) − ε‖²` — *same
shape, different target* (`z₁ − z₀` instead of `ε`). The backbone, the patchify, the
adaLN-Zero conditioning — all identical. This is why porting a DiT from diffusion to
flow is an objective swap, not a redesign.

## 3. Sampling: integrate the velocity field

To generate, start at noise `z₀ ∼ N(0, I)` and integrate the learned velocity forward
with an ODE solver:

```
   z_{t+Δt} = z_t + Δt · v_θ(z_t, t, c)     for t = 0 → 1
```

Because the target paths are *straight*, the learned field tends to be nearly straight
too — so **few solver steps** suffice (and Liu's "reflow" procedure straightens it
further, toward one-step generation). This is the flow analogue of the DDIM/distillation
speedups in Phase 7.2.

## 4. Why "flow matching is just diffusion" is wrong (and why it feels right)

They are genuine cousins — both learn to transport a Gaussian to the data distribution
along a time-indexed path, and the probability-flow ODE view of diffusion makes the
kinship exact. But they are **not the same**:

| | Diffusion (DDPM) | Rectified flow |
|---|---|---|
| Path | curved, variance-preserving noising | **straight line** `(1−t)z₀ + t z₁` |
| Network target | noise `ε` / score `∇ log p_t` | **velocity** `z₁ − z₀` |
| Sampling | reverse SDE / prob-flow ODE | integrate velocity ODE |
| Typical steps | ~50 (DDIM) | few (paths are straight) |

The DiT doesn't change; the *target* does. The [`flow-matching/`](../flow-matching/)
course settles the precise relationship (its keystone is the conditional-expectation
identity `u_t(x) = E[u_t(x∣x₁) ∣ x_t = x]` that makes this trainable without simulating
the path).

## 5. Where this lands in the course

- **FluxMusic** [Phase 6.2] trains its **MM-DiT** with exactly this rectified-flow
  objective in a mel-VAE latent — the FLUX / Stable-Diffusion-3 recipe ported to music.
- The takeaway for the keystone: the **latent canvas** [`the-latent-canvas.md`](the-latent-canvas.md)
  is denoised *either* by a noise-predicting diffusion DiT *or* a velocity-predicting
  flow DiT. Same canvas, same backbone — a swapped objective.

> **Notation note.** Conventions vary: some papers run `t` from 0 (data) to 1 (noise),
> the reverse of the convention used here. The flow-matching course standardizes on
> `t = 0` noise → `t = 1` data, which this primer follows. Always check a paper's
> direction before reading its equations.
