# Flow Matching
*Enrichment for the [AI Music & Audio](../curricula/ai-music-audio.md) curriculum — the training objective behind modern audio DiTs.*

From ODEs as generative models to modern simulation-free training: Lipman's
**Conditional Flow Matching**, Liu's **Rectified Flow**, Tong's **OT-CFM**. Every
formalism is pinned to a 2-D toy distribution (Gaussian → two-moons / checkerboard) you
can actually plot, with PyTorch as the oracle the moment a derivation feels abstract.

**Keystone:** the conditional-expectation identity (syllabus Phase 4.3) —
`u_t(x) = E[u_t(x | x₁) | x_t = x]`: why regressing on the *conditional* velocity gives
the same gradient as the intractable *marginal* one. Every later method sits on top of it.

**Prerequisites:** ODEs and vector fields, basic probability (densities, change of
variables, expectation), and some PyTorch.

**Format:** ~1 hr/day, ~25 sessions.

**Start:** clone **[Courses](https://github.com/josmithiii/Courses)**, then
`./take flow-matching` (launches the daily lesson in
[Claude Code](https://claude.com/claude-code)). Full detail in [`syllabus.md`](syllabus.md).
