# Flow Matching — From ODEs to Rectified and OT Flows

**Learner profile:** Comfortable with ODEs, vector fields, and basic
probability (densities, change of variables, expectation). Some
exposure to neural networks (knows what a loss is, what
backpropagation does, has seen PyTorch). Has heard of diffusion
models and normalizing flows but the *training objective* of modern
flow-matching methods hasn't quite clicked — why is it
"simulation-free," and what exactly is being regressed onto what?
So: every new object pinned to a 2-D toy distribution (Gaussian →
two-moons, or a checkerboard) the learner can actually plot, every
loss derived from the same conditional-expectation identity, and
PyTorch used as the oracle the moment a derivation feels abstract.
~1 hour per day. One concept at a time. Every concept verified with
a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on
one topic. The topic numbers below are *topics*, not days.
`progress.md` tracks the real position.

**End state:** by the last lesson, the learner can: write down a
probability path $p_t(x)$ and the velocity field $u_t(x)$ that
transports it; explain why training a CNF by simulating its ODE is
expensive and how Flow Matching makes it simulation-free; derive
the conditional flow-matching loss and show it has the same gradient
as the (intractable) marginal one; train a small flow-matching model
on a 2-D toy distribution from scratch in PyTorch; explain Rectified
Flow's "reflow" procedure and why it enables one-step generation;
explain OT-CFM's minibatch-OT coupling and what it buys over
independent coupling; and read the three foundational papers
(Lipman 2023, Liu 2023, Tong 2024) without the notation being an
obstacle.

---

## Phase 0 — Orientation
- **0.1** The generative-modeling landscape in one picture. Where
  flow matching sits relative to VAEs, GANs, normalizing flows,
  score-based / diffusion models. The "simulation-free" promise in
  one sentence: *regress a network onto a known target vector field,
  then integrate at sample time.*
- **0.2** Math toolkit refresher (just-in-time): vector fields and
  flows of ODEs, change-of-variables for densities, expectations,
  conditional expectation as the $L^2$ projection (this last identity
  is the workhorse of the whole course — preview only here).
- **0.3** Tooling. PyTorch + `torchdiffeq` (or `scipy.integrate`)
  installed. A 2-D toy data-loader (two Gaussians, then two-moons).
  A short script that samples and scatter-plots — confirm
  matplotlib is wired up.

## Phase 1 — ODEs as Generative Models
- **1.1** A vector field $u_t(x)$ on $\mathbb{R}^d$ and its flow
  $\phi_t$: $\frac{d}{dt}\phi_t(x) = u_t(\phi_t(x))$, $\phi_0(x) = x$.
  Push-forward of a density along the flow. Pin to 1-D: $u_t(x) = a$
  is a translation; $u_t(x) = -x$ is contraction to the origin.
- **1.2** The continuity equation
  $\partial_t p_t + \nabla\cdot(p_t u_t) = 0$. Intuition: "probability
  mass is a fluid; the velocity field tells it where to go." Verify
  by hand on a 1-D Gaussian whose variance shrinks linearly in $t$.
- **1.3** Sampling as ODE integration. Pick $p_0 = \mathcal{N}(0,I)$,
  pick a $u_t$, integrate forward, plot samples at $t = 0, 0.5, 1$.
  This is the *runtime* picture; the rest of the course is about
  how to *learn* the $u_t$ that takes noise to data.
- **1.4** Instantaneous change-of-variables:
  $\frac{d}{dt}\log p_t(\phi_t(x)) = -\nabla\cdot u_t(\phi_t(x))$.
  Why exact likelihoods come for free in CNFs but cost a divergence
  trace.

## Phase 2 — Continuous Normalizing Flows and the Cost Problem
- **2.1** CNFs (Chen et al. 2018, "Neural ODEs"). Parametrize $u_t$
  with a neural network; train by maximum likelihood on data
  $x_1 \sim q$, with $p_0 = \mathcal{N}(0,I)$. The likelihood term
  needs the flow integrated all the way through, plus a Jacobian
  trace.
- **2.2** Why this is slow. Every gradient step backprops through an
  ODE solve. Trace estimators (Hutchinson) help but the
  "simulation in the inner loop" is the bottleneck. *This is the
  problem flow matching solves.*
- **2.3** A different idea: what if we knew the *target* vector
  field $u_t^\star(x)$ analytically, and just regressed onto it?
  Then training would be a vanilla MSE — no ODE solves during
  training. Preview the recipe.

## Phase 3 — Score-Based / Diffusion Background (one lesson, on demand)
- **3.1** The forward noising process $x_t = \alpha_t x_1 + \sigma_t \epsilon$
  with $\epsilon \sim \mathcal{N}(0,I)$. The marginal $p_t$ is a
  Gaussian convolution of the data. Score $s_t(x) = \nabla\log p_t(x)$.
- **3.2** The probability-flow ODE: every SDE has a deterministic
  ODE with the same marginals, with velocity
  $u_t(x) = f_t(x) - \frac{1}{2}g_t^2 s_t(x)$. So diffusion is *also*
  an ODE generator — flow matching and diffusion are cousins, not
  rivals. (We'll come back to this in Phase 8.)
- **3.3** (Optional) Denoising score matching as a prequel to CFM:
  the same conditional-expectation trick, used for the score
  instead of the velocity.

## Phase 4 — Flow Matching (Lipman et al. 2023)
- **4.1** Probability paths $p_t(x)$ interpolating $p_0$ (noise) to
  $p_1 = q$ (data). The marginal flow-matching loss
  $\mathcal{L}_{\text{FM}}(\theta) = \mathbb{E}_{t,x\sim p_t}
   \|v_\theta(t,x) - u_t(x)\|^2$. The catch: we know neither $p_t$ nor
  $u_t$ in closed form for the marginals.
- **4.2** The conditioning trick. Define a *conditional* path
  $p_t(x \mid x_1)$ that's easy (e.g. Gaussian), with a known
  conditional velocity $u_t(x \mid x_1)$. The marginal is
  $p_t(x) = \int p_t(x\mid x_1) q(x_1)\, dx_1$.
- **4.3** The key identity (this is the whole course in one line):
  $u_t(x) = \mathbb{E}[u_t(x\mid x_1) \mid x_t = x]$.
  Therefore the marginal MSE and the conditional MSE have the same
  *gradient*. Train on the conditional loss; sample using the
  network as if it were the marginal field. **Derive this together
  by hand** — it's the central proof of the course.
- **4.4** The Conditional Flow Matching (CFM) loss:
  $\mathcal{L}_{\text{CFM}}(\theta) = \mathbb{E}_{t,x_1,x\sim p_t(\cdot\mid x_1)}
   \|v_\theta(t,x) - u_t(x\mid x_1)\|^2$. No ODE solve, no score
  estimator, just a regression. Sample one $t$, one data point $x_1$,
  one noisy point $x_t$ — that's a training step.
- **4.5** Gaussian conditional paths. Choose
  $p_t(x\mid x_1) = \mathcal{N}(\mu_t(x_1), \sigma_t^2 I)$ with
  endpoints $\mu_0 = 0, \sigma_0 = 1$ and $\mu_1 = x_1, \sigma_1 = 0$
  (or $\sigma_{\min}$). The conditional velocity has a closed form
  ($u_t(x\mid x_1)$ in terms of $\mu_t', \sigma_t'$). Derive it.
- **4.6** Two important special cases of Gaussian paths:
  (i) **Variance-preserving / DDPM-equivalent** paths recover the
  diffusion probability-flow ODE up to time-reparametrization;
  (ii) **Optimal-transport (straight-line) paths**:
  $x_t = (1-t) x_0 + t x_1$ with $x_0 \sim \mathcal{N}(0,I)$, whose
  conditional velocity is the *constant* $u_t(x\mid x_0, x_1) = x_1 - x_0$.
  This is the path that gives Lipman's "OT-CFM" headline result
  and is the one used by Rectified Flow.

## Phase 5 — Implementing Flow Matching on a 2-D Toy
- **5.1** Set up: target $q$ is two-moons in 2-D. Train a tiny MLP
  $v_\theta(t,x): \mathbb{R}^3 \to \mathbb{R}^2$ with the
  straight-line CFM loss. ~200 lines of PyTorch.
- **5.2** Sampling. Integrate $dx/dt = v_\theta(t,x)$ from $t=0$ to
  $t=1$ with a fixed-step Euler solver (or `torchdiffeq`). Compare
  to data. *First "it works" moment* of the course.
- **5.3** Diagnostics. Plot the learned vector field at $t=0.25,
  0.5, 0.75$. Watch the field rotate from "noise-pointing-everywhere"
  to "data-pointing." Visualize a few sample trajectories.
- **5.4** Failure modes. Too-small network → blurry samples;
  too-few timesteps in the solver → distorted samples; bad time
  sampling (only uniform $t$) → poor coverage near the data
  endpoint. Try each, see what breaks.

## Phase 6 — Rectified Flow (Liu et al. 2023)
- **6.1** The "straight" idea. Independent coupling
  $(x_0, x_1) \sim \pi_0 \otimes \pi_1$ + linear interpolation
  $x_t = (1-t)x_0 + t x_1$ is a valid CFM target, but the resulting
  *learned* marginal trajectories cross each other and curve. A
  perfectly straight, non-crossing flow would be integrable in **one
  Euler step**.
- **6.2** Rectify: after training a flow $v^{(1)}$, define a *new*
  coupling by pairing $x_0$ with the model's own deterministic
  output $\hat{x}_1 = \phi^{(1)}_1(x_0)$. Train $v^{(2)}$ on this
  new coupling with the same linear interpolation. The paths are
  now straighter.
- **6.3** Reflow as fixed-point iteration. Each rectification step
  reduces transport cost monotonically. After 1–2 reflows, the
  flow is straight enough that a single Euler step is a good
  generator.
- **6.4** Distillation. With a near-straight flow,
  $\hat{x}_1 \approx x_0 + v_\theta(0, x_0)$. Distill into a
  one-step generator $G_\phi(x_0)$ trained to match $\hat{x}_1$ in
  $L^2$. This is the bridge from "minutes per sample" (multistep
  diffusion) to "one forward pass."
- **6.5** Implement reflow on the two-moons model from Phase 5. Plot
  trajectories before and after — they should visibly straighten.

## Phase 7 — Optimal Transport CFM (Tong et al. 2024)
- **7.1** The free choice in CFM is the *coupling* $\pi(x_0, x_1)$.
  Independent coupling (Phase 5) is what Lipman uses; Rectified
  Flow's reflow tries to drive it toward the OT coupling
  iteratively. Tong's idea: just *use* an OT coupling directly,
  computed per-minibatch.
- **7.2** Discrete OT in 60 seconds. Given a batch of noise points
  and a batch of data points, the OT plan is a permutation (or
  doubly-stochastic matrix) minimizing $\sum \pi_{ij} \|x_0^i -
  x_1^j\|^2$. Solve with `POT` or the Sinkhorn algorithm.
- **7.3** OT-CFM: sample a minibatch, solve OT to get matched
  pairs, then train with the straight-line CFM loss on those pairs.
  Same training cost per step (the OT solve is small batch-vs-batch),
  much straighter learned trajectories than independent coupling.
- **7.4** Generalized CFM. Tong's framework unifies independent
  coupling, OT coupling, and Schrödinger-bridge couplings inside
  one CFM objective. Read the paper's Table 1 — recognize each row.
- **7.5** Implement OT-CFM on two-moons. Compare integration steps
  needed for good samples: independent CFM vs. OT-CFM vs.
  reflow-rectified. Plot side-by-side.

## Phase 8 — Putting It Together
- **8.1** The unifying picture. Score-based diffusion, Lipman's
  flow matching with VP paths, and rectified flow all live in the
  same family: a probability path + a regressed velocity field
  trained by conditional expectation. The differences are
  (i) which path, (ii) which coupling, (iii) what you do
  post-training (sample directly vs. reflow vs. distill).
- **8.2** Capstone — pick one (learner's choice):
  - **(a)** A small image FM on MNIST or CIFAR (sketch only — the
    UNet architecture, the loss, the sampling loop; full training is
    a multi-day GPU job we'll set up but not necessarily finish).
  - **(b)** A 2-D *audio*-flavored capstone JOS-style: model a
    distribution of short pitch/loudness/timbre vectors (or
    spectral envelopes) with FM, and sample new ones. Connects to
    his sound-synthesis work.
  - **(c)** Build all three trainers (independent CFM, reflow-RF,
    OT-CFM) on the same 2-D dataset and produce a single figure
    that shows trajectory straightness vs. sample quality vs.
    solver steps.
- **8.3** Where next. The three foundational papers
  ([Lipman 2023](https://arxiv.org/abs/2210.02747),
   [Liu 2023](https://arxiv.org/abs/2209.03003),
   [Tong 2024](https://arxiv.org/abs/2302.00482))
  are now readable. Suggested followups: Stable Diffusion 3 (uses
  rectified flow); Meta's `flow_matching` library; the
  Schrödinger-bridge variants (DSBM, SB-CFM); flow matching on
  non-Euclidean spaces (manifolds, discrete data).

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick
   recall question. If shaky, re-teach before continuing.
2. **Introduce one new concept.** Notation lands cleanly: name it,
   write it, say what it is in plain English, then say what it lets
   us *compute* or *avoid* that we couldn't before.
3. **Pin it to the 2-D toy.** Almost every object in this course —
   probability paths, vector fields, conditional expectations,
   couplings, reflows — can be made concrete on 2-D points the
   learner plots. Do that. The two-moons dataset is the worked
   example we return to relentlessly.
4. **Tiny exercise** to verify: derive a line of algebra by hand, or
   write/modify five lines of PyTorch, and check against a runnable
   script when it isn't obvious. The exercise *is* the check that
   the formalism landed.
5. **Common confusions** when relevant. The two big ones in this
   subject: (i) confusing the *marginal* path/velocity with the
   *conditional* one — the whole CFM trick lives on this distinction;
   (ii) confusing the learned vector field with a score (they're
   related but not equal in general). Flag explicitly.
6. **Log** what was covered, the exercise, the answer, and a mastery
   note to `progress.md` and the day's `lessons/` file.
7. Keep each session ~1 hour. End with a one-sentence preview of
   next time.

### Mastery criteria

A topic is mastered when the learner can:

1. State the definition in their own words, in one or two sentences,
   without notation cheats ("the CFM loss is …, and it works because
   …").
2. Carry out the corresponding small computation: a derivation, a
   plot, or a short PyTorch modification — and explain each step.
3. Spot a deliberately wrong claim about it ("we need to integrate
   the ODE during training to compute the FM loss" — no, that's the
   point of conditioning).

Record this in the data-dir `progress.md` mastery log.

---

### Source papers (the three foundational papers this course tracks)

The PDFs live in `/l/dttd/FlowStuff/` on JOS's machine:

- **Lipman, Chen, Ben-Hamu, Nickel, Le (2023).** *Flow Matching for
  Generative Modeling.* ICLR 2023. arXiv:2210.02747. — introduces
  CFM and Gaussian conditional probability paths; identifies the
  OT-style straight-line path as a special case.
- **Liu, Gong, Liu (2023).** *Flow Straight and Fast: Learning to
  Generate and Transfer Data with Rectified Flow.* ICLR 2023.
  arXiv:2209.03003. — introduces reflow as a path-straightening
  procedure and one-step distillation.
- **Tong, Fatras, Malkin, Huguet, Zhang, Rector-Brooks, Wolf, Bengio
  (2024).** *Improving and Generalizing Flow-Based Generative Models
  with Minibatch Optimal Transport.* TMLR 2024. arXiv:2302.00482.
  — introduces minibatch-OT couplings and the unifying generalized
  CFM framework.
