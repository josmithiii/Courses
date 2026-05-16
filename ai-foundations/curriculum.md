# AI Curriculum — Complete Beginner → Modern LLMs

**Learner profile:** New to ML, new to Python, math is rusty. So: intuition first,
visuals and analogies before notation, Python and math taught *just-in-time* as each
concept needs them. ~1 hour per day. One concept at a time. Every concept is checked
with a small exercise before moving on.

**Pace philosophy:** It is completely fine to spend multiple days on one lesson.
The lesson numbers below are *topics*, not days. `progress.md` tracks the real position.

---

## Phase 0 — Orientation
- **0.1** What AI / ML / deep learning actually are (no math). Where LLMs, image
  generators fit. What we'll build toward.
- **0.2** Set up tools: Python, a code editor, install PyTorch, run "hello tensor".
- **0.3** Python crash-start I: variables, numbers, strings, lists, printing.
- **0.4** Python crash-start II: functions, loops, `if`, importing libraries.

## Phase 1 — The Core Idea of Learning from Data
- **1.1** What a "model" is: input → prediction. Data, features, labels.
- **1.2** Math intuition: a number line, a vector as a list of numbers, a matrix as a grid.
- **1.3** The artificial neuron: weighted sum + bias. Hand-compute one by hand.
- **1.4** Activation functions: why we need a "bend" (ReLU, sigmoid) — intuition.
- **1.5** A layer of neurons; stacking layers → the **Multi-Layer Perceptron (MLP)**.
- **1.6** Loss: measuring how wrong a prediction is (MSE; cross-entropy intuition).
- **1.7** Gradient descent: rolling downhill to reduce loss. Learning rate intuition.
- **1.8** Backpropagation: how blame flows backward to each weight (intuition + tiny worked example).
- **1.9** The training loop: epochs, batches, iterations — the whole picture.

## Phase 2 — PyTorch For Real
- **2.1** Tensors: creating, shapes, indexing, math on them.
- **2.2** Autograd: PyTorch computes gradients for you.
- **2.3** `nn.Module`: build an MLP in code.
- **2.4** Optimizers + a full training loop you write yourself.
- **2.5** Datasets & DataLoaders; batching real data.
- **2.6** Train/validation/test split; overfitting; what it looks like.
- **2.7** Regularization, dropout, early stopping — keeping models honest.
- **2.8** Mini-project: train an MLP to classify handwritten digits (MNIST).

## Phase 3 — Convolutional Neural Networks (Images)
- **3.1** Images as tensors (height × width × channels).
- **3.2** Convolution: sliding filters, what a filter "detects" — intuition.
- **3.3** Feature maps, stride, padding, pooling.
- **3.4** Build a small CNN; train on MNIST/CIFAR-10.
- **3.5** Why CNNs beat MLPs on images. Receptive fields.
- **3.6** Transfer learning: reuse a pretrained vision model.

## Phase 4 — Sequences, Attention, Transformers
- **4.1** Sequence data; turning words into numbers (embeddings).
- **4.2** RNNs/LSTMs — the older way to handle sequences (brief, historical, intuition only).
- **4.3** The attention mechanism: "what should I focus on?" — core intuition.
- **4.4** Self-attention and multi-head attention.
- **4.5** Positional encoding; residual connections; layer norm; feed-forward block.
- **4.6** The full **Transformer** block assembled.
- **4.7** Mini-project: build & train a tiny character-level Transformer.

## Phase 5 — Large Language Models
- **5.1** Tokenization (how text becomes tokens).
- **5.2** The language modeling objective: predict the next token.
- **5.3** Pretraining vs fine-tuning; what "scale" buys you.
- **5.4** Instruction tuning and preference tuning (RLHF) — intuition.
- **5.5** Inference: temperature, sampling, context window, prompting.
- **5.6** Mini-project: load and use a small pretrained LLM (Hugging Face).

## Phase 6 — Diffusion & Generative Models
- **6.1** What "generative" means; quick tour of VAEs and GANs (intuition).
- **6.2** Diffusion intuition: destroy an image with noise, learn to undo it.
- **6.3** Forward/reverse process; the denoising network (U-Net) — intuition.
- **6.4** Text-to-image conditioning; how prompts steer generation.
- **6.5** Mini-project: run a small diffusion model and generate images.

## Phase 7 — Putting It Together
- **7.1** How modern systems combine these pieces (multimodal, agents — overview).
- **7.2** Capstone: pick a small project and build it with guidance.
- **7.3** Where to go next: papers, courses, communities, staying current.

---

### Teaching method (applies every lesson)
1. **Recap** the previous concept in 2–3 sentences; ask one quick recall question.
2. **Introduce one new concept** with an analogy/visual before any notation or code.
3. **Show**, then have the learner **do** a tiny exercise (by hand or a few lines of code).
4. **Verify** understanding from their answer; if shaky, re-explain a different way —
   do not advance until it's solid.
5. **Log** what was covered, the exercise, their answer, and a mastery note to
   `progress.md` and the day's `lessons/` file.
6. Keep each session ~1 hour. End with a one-sentence preview of next time.
