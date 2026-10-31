# The Diagram Atlas

Every architecture buzzword in this course has a famous picture: the one an image search
turns up, and the one a paper, slide deck or blog post will assume you can read. **By the end
of the course, the learner should be able to look at any of these, name it, and trace what
flows through it.** The picture is taught along with the concept, not as decoration.

Entries are ordered by syllabus topic; the number in each heading is the topic that teaches
it. A topic may have several entries, and most topics have none.

## How to use an entry (tutor)

The analogy still comes first. Then, for each entry headed with today's topic number:

1. **Show the course figure.** Follow the **Figures** preference in the learner's
   `progress.md`. If it is unset, this is their first figure: ask whether they want you to open
   figures for them, which moves focus to their browser or image viewer, or to get the command
   and open them themselves. Record the answer there straight away, so it is asked only once.
   Skip the offer if you can't run commands; they open the file themselves. Either way, give
   the full command in chat (`open <absolute path>` on macOS, `xdg-open` on Linux), so a
   blocked call still leaves them a way forward. Name the figure's grammar (below). Every figure
   is also in `figures/gallery.html`, which has a size slider. Draw the ASCII sketch in chat
   when the entry has one, or when they can't open files.
2. **Show the famous picture.** Give the learner a clickable image search built from the
   entry's **Search** phrase, `https://www.google.com/search?tbm=isch&q=<phrase, spaces as +>`,
   plus the **Source** link when there is one. This is the version they will meet elsewhere.
   You cannot see what the search returns, so ask what they see and never describe it as if
   you could. If they have no browser to hand, note in the log that it is still owed.
3. **Read it together** using **Read it**, tracing one input all the way through.
4. **Pre-empt the Trap.** Image searches mix styles, and many pictures are redrawn loosely, so
   expect variations. Spotting how two versions differ is a good exercise. When they disagree,
   the Source wins.
5. **Do the Check**, and log the result in the Mastery log like any other exercise.

The **Figure** files are this course's own, in one visual language: teal is data, orange has
trained weights, gray is a fixed operation, purple is model output. Figures from other authors
are linked, never copied.

## The five grammars

Most confusion comes from assuming every diagram uses the same visual language. There are
five, and the first question for any new picture is **which one is this?**

| Grammar | A shape means | A line or arrow means | Examples |
|---|---|---|---|
| **Graph** | one number (a neuron's value) | one weight | MLP, dropout |
| **Block** | an operation | a tensor flowing between operations | Transformer, LSTM, ResNet block |
| **Slab** | a tensor itself; size drawn to scale-ish | (the gap between slabs) an operation | LeNet-5, AlexNet, U-Net |
| **Probabilistic** | a random variable | a conditional distribution | DDPM, the VAE paper |
| **Plot** | nothing: axes carry data | a measured or computed curve | loss curves, attention heatmaps |

So a line in an MLP is a single number, while an arrow in a Transformer is an entire tensor of
millions of numbers. That difference is the single most useful thing in this file.

## Phase 1 - Learning from data

### 1.3 Artificial neuron (perceptron)
- **Grammar:** Graph
- **Figure:** [`figures/neuron.svg`](figures/neuron.svg)
- **Search:** artificial neuron perceptron diagram
- **Source:** No single origin; the picture is folklore.
- **Read it:** Inputs on the left, each multiplied by its weight; a sum (plus bias); a squashing
  function, which topic 1.4 teaches; one output.
- **Trap:** The one circle hides two steps, the weighted sum and the activation. The side-by-side
  biological neuron is a loose inspiration, not a working model.
- **Check:** With x = (1, 2), w = (0.5, -1), b = 1, what is the weighted sum plus bias? (-0.5.)

```
x1 --w1--\
x2 --w2---( sum + b )--[ activation ]--> y
x3 --w3--/
```

### 1.4 Activation function curves
- **Grammar:** Plot
- **Figure:** [`figures/activation-functions.svg`](figures/activation-functions.svg)
- **Search:** activation functions ReLU sigmoid tanh plot
- **Source:** No single origin; these are plots of formulas.
- **Read it:** The horizontal axis is the neuron's weighted sum; the vertical axis is its output.
- **Trap:** The horizontal axis is not time and not the raw input. The bend is the whole point:
  a straight line here would make stacked layers collapse into one.
- **Check:** The neuron in the 1.3 check has a weighted sum plus bias of -0.5. What does ReLU
  output? (0, since ReLU turns negatives into 0.) Where on the sigmoid is the slope nearly zero,
  and what might that do to learning? (Far from 0 on either side; the gradient nearly vanishes.)

```
sigmoid:      ______        ReLU:           /
             /                             /
      ______/                      _______/
```

### 1.5 Multi-layer perceptron (MLP, fully connected network)
- **Grammar:** Graph
- **Figure:** [`figures/mlp.svg`](figures/mlp.svg)
- **Search:** multilayer perceptron fully connected network diagram
- **Source:** Interactive: [TensorFlow Playground](https://playground.tensorflow.org/).
- **Read it:** Columns are layers. Every circle connects to every circle in the next column.
- **Trap:** Each line is one weight, and each circle is one value at run time, not a stored
  object. Authors disagree about whether the input column counts as a layer.
- **Check:** Count the parameters in a 3-4-2 network, biases included. (3*4 + 4*2 = 20 weights,
  plus 4 + 2 = 6 biases, for 26.)

```
input   hidden   output
  o
          o
  o                o
          o
  o                o
          o

(each column is fully connected to the next)
```

### 1.6 Universal approximation (steps, bumps and curves)
- **Grammar:** Plot
- **Figure:** [`figures/universal-approximation.svg`](figures/universal-approximation.svg)
- **Search:** universal approximation theorem neural network bump functions
- **Source:** Nielsen, [A visual proof that neural nets can compute any function](http://neuralnetworksanddeeplearning.com/chap4.html),
  Ch. 4 of *Neural Networks and Deep Learning* (2015), whose sliders are worth playing with. The
  theorems are Cybenko (1989) and Hornik, Stinchcombe & White (1989).
- **Read it:** Left: raising the weight w steepens a sigmoid into a step at x = -b/w. Middle: a
  step up and a step down, joined by output weights +h and -h, make a bump of height h. Right:
  bumps side by side trace a target curve, and more neurons give narrower bumps and a closer fit.
- **Trap:** The theorem says a network exists, not that training will find it or that it is
  small. It also promises approximation, not an exact match, and only for continuous functions on
  a bounded range. "One hidden layer is enough" does not mean one hidden layer is a good design.
- **Check:** With w = 100, design a bump of height 0.8 from x = 0.4 to x = 0.6. What are the two
  biases and the two output weights? (b = -40 and -60; +0.8 and -0.8.) What comes out at x = 0.5
  and at x = 0.7? (About 0.8 and about 0.) How many hidden neurons do 5 bumps take? (10.)

```
step up       +  step down     =  bump
      ______                        ___
     |           ______|           |   |
_____|                 |______  ___|   |___
```

### 1.8 Loss landscape and gradient descent
- **Grammar:** Plot
- **Figure:** [`figures/loss-landscape.svg`](figures/loss-landscape.svg)
- **Search:** gradient descent loss landscape contour plot
- **Source:** Li et al., [Visualizing the Loss Landscape of Neural Nets](https://arxiv.org/abs/1712.09913) (2018), Fig. 1.
- **Read it:** Horizontal position is a choice of weights; height is the loss there. The contour
  view is the same thing as a topographic map, seen from above.
- **Trap:** The axes are weights, not inputs. Real models have millions of weights, so every such
  picture is a low-dimensional slice, which can flatter or mislead.
- **Check:** On a contour plot, sketch the path for a learning rate that is too large. (It
  zig-zags across the valley or leaves it altogether.)

### 1.9 Computational graph and backpropagation
- **Grammar:** Block
- **Figure:** [`figures/computational-graph.svg`](figures/computational-graph.svg)
- **Search:** computational graph backpropagation diagram
- **Source:** Olah, [Calculus on Computational Graphs: Backpropagation](https://colah.github.io/posts/2015-08-Backprop/) (2015).
- **Read it:** Forward arrows carry values. Backward arrows carry each output's sensitivity to
  that node, multiplied along the path by the chain rule.
- **Trap:** The backward pass is not a second network and has no weights of its own. It is the
  same graph traversed in reverse.
- **Check:** For L = (w*x - t)^2 with w = 2, x = 3, t = 5, what is dL/dw? (The error is 1, so
  2 * 1 * 3 = 6.)

```
w --\
     (*)--> y --(- t)--> e --(^2)--> L     forward: values
x --/
     <--------- dL/dw --------------       backward: gradients
```

## Phase 2 - PyTorch for real

### 2.6 Learning curves and overfitting
- **Grammar:** Plot
- **Figure:** [`figures/learning-curves.svg`](figures/learning-curves.svg)
- **Search:** training validation loss curves overfitting
- **Source:** No single origin; every learner should produce their own in 2.8.
- **Read it:** Epochs across, loss up. Training loss keeps falling; validation loss falls, then
  turns back up.
- **Trap:** A low training curve alone says nothing. The widening gap is the symptom, and a
  rising validation curve is what signals overfitting.
- **Check:** Point to where early stopping would stop. (The validation minimum.)

```
loss
 |\  \___         ____ validation
 | \     \_______/
 |  \___
 |      \_________ training
 +--------------------- epochs
```

### 2.7 Dropout
- **Grammar:** Graph
- **Figure:** [`figures/dropout.svg`](figures/dropout.svg)
- **Search:** dropout neural network diagram
- **Source:** Srivastava et al., [Dropout](https://jmlr.org/papers/volume15/srivastava14a/srivastava14a.pdf) (2014), Fig. 1.
- **Read it:** The same network twice, the second with some units crossed out.
- **Trap:** The thinned network exists only during training, and a different one is drawn for
  each batch. At test time all units are on.
- **Check:** Why should dropout be off when you evaluate? (Otherwise predictions are randomly
  noisy, and you are testing a random subnetwork.)

## Phase 3 - Image models

### 3.1 An image as a tensor of channels
- **Grammar:** Slab
- **Figure:** [`figures/rgb-channels.svg`](figures/rgb-channels.svg)
- **Search:** RGB image channels tensor diagram
- **Source:** No single origin.
- **Read it:** Three grids stacked: red, green, blue. Together they form a 3-D block of numbers.
- **Trap:** Pictures usually show height x width x channels, while PyTorch stores channels x
  height x width.
- **Check:** What is the PyTorch shape of a batch of 8 CIFAR-10 images? (8 x 3 x 32 x 32.)

### 3.2 Convolution: a filter sliding over a grid
- **Grammar:** Slab
- **Figure:** [`figures/convolution.svg`](figures/convolution.svg)
- **Search:** convolution kernel sliding over image diagram
- **Source:** Dumoulin & Visin, [A guide to convolution arithmetic](https://arxiv.org/abs/1603.07285) (2016), Fig. 1.1, with [animations](https://github.com/vdumoulin/conv_arithmetic). Interactive: [CNN Explainer](https://poloclub.github.io/cnn-explainer/).
- **Read it:** A small window of weights slides over the input. At each stop, multiply overlapping
  numbers and add them up to get one output cell.
- **Trap:** The output is smaller or the same size, not a copy. Deep learning's "convolution" does
  not flip the kernel, so a signal-processing reader would call it correlation.
- **Check:** Apply kernel [[1, 0], [0, -1]] to patch [[3, 1], [2, 5]]. (3 - 5 = -2.)

```
input            kernel        output
3 1 0 2          1  0          -2  .  .
2 5 1 1    *     0 -1          .   .  .
0 4 2 3                        .   .  .
1 0 3 1
```

### 3.3 Stride, padding and pooling
- **Grammar:** Slab
- **Figure:** [`figures/stride-padding-pooling.svg`](figures/stride-padding-pooling.svg)
- **Search:** CNN stride padding pooling diagram
- **Source:** Dumoulin & Visin (2016), Fig. 1.5 (average pooling), Fig. 1.6 (max pooling), and Ch. 2.
- **Read it:** Stride is how far the window hops. Padding is the border added first. Pooling is
  a window with no weights that keeps a summary, such as the maximum.
- **Trap:** Each output channel comes from its own filter, so the depth of the slab is the number
  of filters, not anything about the input.
- **Check:** Input size 5, kernel 3, padding 1, stride 2. What is the output size, using
  floor((in + 2*pad - kernel) / stride) + 1? (3.)

### 3.4 LeNet-5 and the CNN pipeline
- **Grammar:** Slab
- **Figure:** [`figures/lenet-5.svg`](figures/lenet-5.svg)
- **Search:** LeNet-5 architecture diagram
- **Source:** LeCun et al., [Gradient-based learning applied to document recognition](http://yann.lecun.com/exdb/publis/pdf/lecun-98.pdf) (1998), Fig. 2.
- **Read it:** Left to right: images get smaller and deeper, then flatten into plain vectors.
  Read "6@28x28" as 6 feature maps, each 28 by 28.
- **Trap:** Each plane is a feature map, not a layer. The slanted stripes at the end are the
  fully connected layers. Nearly every later CNN picture copies this layout.
- **Check:** A 5x5 kernel with no padding turns 32x32 into what? (28x28.)

```
32x32 -> 6@28x28 -> 6@14x14 -> 16@10x10 -> 16@5x5 -> 120 -> 84 -> 10
         conv       subsample  conv        subsample full   full  Gaussian
```

### 3.5 Receptive field
- **Grammar:** Slab
- **Figure:** [`figures/receptive-field.svg`](figures/receptive-field.svg)
- **Search:** receptive field CNN layers diagram
- **Source:** Zeiler & Fergus, [Visualizing and Understanding Convolutional Networks](https://arxiv.org/abs/1311.2901) (2014), Fig. 2, for what each depth responds to.
- **Read it:** Pick one cell in a deep layer and trace back the cone of input pixels that can
  affect it. Each layer widens the cone.
- **Trap:** Receptive field grows with depth even when every kernel stays small. That is why deep
  layers can respond to whole objects.
- **Check:** What is the receptive field of three stacked 3x3 layers with stride 1? (7x7.)

### 3.6 AlexNet and VGG
- **Grammar:** Slab
- **Figure:** [`figures/alexnet-vgg.svg`](figures/alexnet-vgg.svg)
- **Search:** AlexNet architecture diagram, VGG16 architecture diagram
- **Source:** Krizhevsky et al., [ImageNet Classification with Deep CNNs](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) (2012), Fig. 2; Simonyan & Zisserman, [Very Deep Convolutional Networks](https://arxiv.org/abs/1409.1556) (2015), Table 1.
- **Read it:** The LeNet recipe, made much deeper and wider. VGG repeats plain 3x3 blocks.
- **Trap:** AlexNet's two parallel streams reflect two GPUs, not a design idea. The colorful VGG
  pictures online are redrawn; the paper itself gives a table.
- **Check:** Why are stacked 3x3 layers attractive? (Same receptive field as one large kernel,
  fewer weights, and more bends.)

### 3.6 Inception module
- **Grammar:** Block
- **Figure:** [`figures/inception.svg`](figures/inception.svg)
- **Search:** Inception module GoogLeNet diagram
- **Source:** Szegedy et al., [Going deeper with convolutions](https://arxiv.org/abs/1409.4842) (2015), Fig. 2 (module), Fig. 3 (full network).
- **Read it:** Several filter sizes run side by side on the same input, and their outputs are
  concatenated.
- **Trap:** A 1x1 convolution is not a no-op: it mixes channels and shrinks the depth cheaply.
- **Check:** Why put a 1x1 before a 5x5? (To reduce channels, and so reduce computation.)

### 3.6 ResNet and the residual block
- **Grammar:** Block
- **Figure:** [`figures/resnet-block.svg`](figures/resnet-block.svg)
- **Search:** ResNet residual block skip connection diagram
- **Source:** He et al., [Deep Residual Learning](https://arxiv.org/abs/1512.03385) (2016), Fig. 2 (block), Fig. 3 (network); Li et al. (2018), Fig. 1, for the landscape with and without skips.
- **Read it:** Input splits in two: one path through layers, one straight across. The two are added.
- **Trap:** The layers learn the correction F(x), not the full output. The curved arrow is an
  addition, not a bypass that turns the layers off.
- **Check:** If the layers learn F(x) = 0, what does the block output? (x, unchanged, which is why
  adding depth stops hurting.)

```
x ---+--> [ layer ] -> [ layer ] --(+)--> F(x) + x
     |                              ^
     +------------------------------+
```

## Phase 4 - Sequences, attention, Transformers

### 4.1 Word embedding space
- **Grammar:** Plot
- **Figure:** [`figures/word-embeddings.svg`](figures/word-embeddings.svg)
- **Search:** word embedding vector space king queen diagram
- **Source:** Mikolov et al., [Efficient Estimation of Word Representations](https://arxiv.org/abs/1301.3781) (2013), Fig. 1, shows the separate CBOW and skip-gram block pictures.
- **Read it:** Each word is a point. Nearby points mean similar usage, and some directions carry
  meaning.
- **Trap:** The 2-D plot is a projection of hundreds of dimensions, so distances are distorted,
  and the tidy king-queen parallelogram is a best case.
- **Check:** What does king - man + woman land near? (queen, approximately.)

### 4.2 RNN, folded and unrolled
- **Grammar:** Block
- **Figure:** [`figures/rnn.svg`](figures/rnn.svg)
- **Search:** RNN unrolled diagram
- **Source:** Olah, [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/) (2015).
- **Read it:** The loop on the left and the chain on the right are the same network, drawn two ways.
- **Trap:** The repeated boxes are one box seen at different times, with shared weights. They are
  not layers.
- **Check:** How many separate sets of weights does a 5-step unrolled RNN have? (One.)

```
  +---+           x1      x2      x3
  |   |            |       |       |
x->[A]-> y   =   [A] --> [A] --> [A] -->
  ^___|            |       |       |
                  y1      y2      y3
```

### 4.2 LSTM cell
- **Grammar:** Block
- **Figure:** [`figures/lstm.svg`](figures/lstm.svg)
- **Search:** LSTM cell diagram
- **Source:** Olah (2015).
- **Read it:** The line along the top is the cell state, a conveyor belt of memory. Gates below
  decide what to forget, what to add, and what to output.
- **Trap:** This is the scariest picture in the course and it is not worth memorizing here: 4.2
  is historical. Get the conveyor belt and the three gates. The GRU picture is a simplified cousin.
- **Check:** Which part lets information pass many steps nearly unchanged? (The cell state line.)

### 4.3 Seq2seq (encoder-decoder)
- **Grammar:** Block
- **Figure:** [`figures/seq2seq.svg`](figures/seq2seq.svg)
- **Search:** seq2seq encoder decoder RNN diagram
- **Source:** Cho et al., [Learning Phrase Representations using RNN Encoder-Decoder](https://arxiv.org/abs/1406.1078) (2014), Fig. 1.
- **Read it:** An encoder reads the input into one summary vector, which a decoder expands into
  the output.
- **Trap:** The bottleneck is the point: everything must squeeze through one fixed-size vector,
  which is exactly the problem attention was invented to fix.
- **Check:** Why would a 50-word sentence suffer more than a 5-word one? (Same-sized summary.)

### 4.3 Attention as a heatmap
- **Grammar:** Plot
- **Figure:** [`figures/attention-heatmap.svg`](figures/attention-heatmap.svg)
- **Search:** attention alignment heatmap translation
- **Source:** Bahdanau et al., [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) (2015), Fig. 3; Fig. 1 is the matching block diagram.
- **Read it:** Source words across, output words down. A bright cell means that output word looked
  at that source word.
- **Trap:** The bright diagonal isn't a rule: off-diagonal patches appear exactly where the two
  languages order words differently. The picture is a result, not an architecture.
- **Check:** What do the weights in one output word's row add up to? (1.)

### 4.4 Scaled dot-product attention
- **Grammar:** Block
- **Figure:** [`figures/scaled-dot-product.svg`](figures/scaled-dot-product.svg)
- **Search:** scaled dot-product attention query key value diagram
- **Source:** Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (2017), Fig. 2 (left). Explained: Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/).
- **Read it:** **Bottom to top.** Queries meet keys to give scores, softmax turns scores into
  weights, and those weights mix the values.
- **Trap:** Transformer diagrams flow upward. In self-attention, Q, K and V all come from the same
  input through different learned transforms.
- **Check:** If a query matches key 2 far better than the others, what does the output mostly
  contain? (Value 2.)

```
         output
           ^
        [ MatMul ] <------ V
           ^
        [ SoftMax ]
           ^
        [ Scale ]
           ^
        [ MatMul ] <------ Q, K
```

### 4.4 Multi-head attention
- **Grammar:** Block
- **Figure:** [`figures/multi-head-attention.svg`](figures/multi-head-attention.svg)
- **Search:** multi-head attention diagram
- **Source:** Vaswani et al. (2017), Fig. 2 (right).
- **Read it:** Several small attention units run in parallel on projected inputs. Their outputs
  are concatenated and projected again.
- **Trap:** The stacked, shadowed boxes mean parallel copies, not depth.
- **Check:** With d_model = 512 and 8 heads, how wide is each head? (64.)

### 4.5 Positional encoding
- **Grammar:** Plot
- **Figure:** [`figures/positional-encoding.svg`](figures/positional-encoding.svg)
- **Search:** positional encoding heatmap transformer
- **Source:** Vaswani et al. (2017), Section 3.5, for the formula; Alammar's post above for the picture.
- **Read it:** One row per position and one column per embedding dimension. Each column is a sine
  or cosine at its own frequency, so each row is a unique fingerprint.
- **Trap:** The stripes look like signals over time, but they are a lookup table of positions,
  closer in spirit to a binary counter with fast and slow bits.
- **Check:** Why is attention alone unable to tell word order? (It treats its inputs as a set.)

### 4.5 Normalization: batch vs layer
- **Grammar:** Slab
- **Figure:** [`figures/normalization.svg`](figures/normalization.svg)
- **Search:** batch norm layer norm group norm cube diagram
- **Source:** Wu & He, [Group Normalization](https://arxiv.org/abs/1803.08494) (2018), Fig. 2.
- **Read it:** Each cube is a tensor with axes for batch, channels and spatial position. The
  shaded cells are the ones normalized together.
- **Trap:** The methods differ only in which axes get averaged over. Batch norm crosses examples
  in the batch; layer norm stays within one example.
- **Check:** Which one still works with a batch of size 1? (Layer norm.)

### 4.6 The Transformer
- **Grammar:** Block
- **Figure:** [`figures/transformer.svg`](figures/transformer.svg)
- **Search:** transformer architecture diagram attention is all you need
- **Source:** Vaswani et al. (2017), Fig. 1. Explained: Alammar's post above.
- **Read it:** **Bottom to top.** Left tower is the encoder, right tower the decoder, "Nx" means
  stacked N times. The arrow from left to right is cross-attention. Every arrow around an
  "Add & Norm" box is a ResNet skip.
- **Trap:** The output sits at the top, not on the right. "Outputs (shifted right)" at the bottom
  are the words produced so far. Modern LLMs keep only a version of the right tower.
- **Check:** Trace one word from Inputs to Output Probabilities and name each box it passes.

```
                        Output Probabilities
                                 ^
                       [ Linear + Softmax ]
                                 ^
 Nx +----------------+    Nx +-------------------+
    | Feed Forward   |       | Feed Forward      |
    | Multi-Head     |---+-->| Cross-Attention   |
    | Attention      |       | Masked Attention  |
    +----------------+       +-------------------+
            ^                         ^
    Inputs + position          Outputs (shifted right) + position
```

## Phase 5 - Large language models

### 5.2 Decoder-only stack and the causal mask (GPT)
- **Grammar:** Block
- **Figure:** [`figures/gpt-stack.svg`](figures/gpt-stack.svg)
- **Search:** GPT decoder only architecture causal attention mask diagram
- **Source:** Alammar, [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/); Vaswani et al. (2017), Fig. 1, right tower.
- **Read it:** The Transformer's right tower without its cross-attention. The triangular grid shows
  which earlier tokens each position may attend to.
- **Trap:** Masking is why training can show the model a whole sentence without letting it peek at
  the answer. The grid belongs to the model's training, not to the text.
- **Check:** In the mask below, which tokens can position 3 see? (Tokens 1 to 3.)

```
       1 2 3 4
pos 1  x . . .
pos 2  x x . .
pos 3  x x x .
pos 4  x x x x
```

### 5.4 The RLHF pipeline
- **Grammar:** Block
- **Figure:** [`figures/rlhf-pipeline.svg`](figures/rlhf-pipeline.svg)
- **Search:** RLHF pipeline diagram supervised fine-tuning reward model PPO
- **Source:** Ouyang et al., [Training language models to follow instructions](https://arxiv.org/abs/2203.02155) (2022), Fig. 2.
- **Read it:** Three stages in order: supervised fine-tuning, reward model training, then
  reinforcement learning against that reward model.
- **Trap:** This is a training pipeline, not a network architecture. Boxes are stages and models.
- **Check:** What trains the reward model? (Humans ranking the model's answers.)

## Phase 6 - Diffusion and generative models

### 6.1 Autoencoder
- **Grammar:** Slab
- **Figure:** [`figures/autoencoder.svg`](figures/autoencoder.svg)
- **Search:** autoencoder bottleneck diagram
- **Source:** No single origin.
- **Read it:** Input narrows to a small code, then widens back to a reconstruction.
- **Trap:** The hourglass drawing shows vector sizes, not a physical shape. The middle is the
  whole point: it must keep only what matters.
- **Check:** What would an autoencoder with no bottleneck learn? (To copy, and nothing useful.)

```
input -> [#####] -> [###] -> [#] -> [###] -> [#####] -> reconstruction
          encoder            code    decoder
```

### 6.1 Variational autoencoder (VAE)
- **Grammar:** Probabilistic
- **Figure:** [`figures/vae.svg`](figures/vae.svg)
- **Search:** variational autoencoder diagram mean variance sampling
- **Source:** Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114) (2013), Fig. 1.
- **Read it:** The usual picture: the encoder outputs a mean and a spread, a code is sampled from
  them, and the decoder reconstructs.
- **Trap:** That popular hourglass is not in the paper. The paper's Fig. 1 is a small probabilistic
  graph, and the difference shows why grammars matter.
- **Check:** How does a VAE's middle differ from a plain autoencoder's? (A distribution rather
  than a single point.)

### 6.1 Generative adversarial network (GAN)
- **Grammar:** Block
- **Figure:** [`figures/gan.svg`](figures/gan.svg)
- **Search:** GAN generator discriminator diagram
- **Source:** Goodfellow et al., [Generative Adversarial Nets](https://arxiv.org/abs/1406.2661) (2014), Fig. 1.
- **Read it:** Noise feeds a generator to make a fake. A discriminator judges fakes and real
  samples, and its verdict trains both.
- **Trap:** The popular block picture is not in the paper either. The paper's Fig. 1 is a set of
  one-dimensional distribution plots showing the fake distribution moving toward the real one.
- **Check:** Which network ever sees real data directly? (Only the discriminator.)

```
noise -> [ Generator ] -> fake --\
                                  [ Discriminator ] -> real or fake?
                    real data ---/
```

### 6.2 The diffusion chain
- **Grammar:** Probabilistic
- **Figure:** [`figures/diffusion-chain.svg`](figures/diffusion-chain.svg)
- **Search:** denoising diffusion forward reverse process diagram
- **Source:** Ho et al., [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) (2020), Fig. 2.
- **Read it:** A chain of images from pure noise to a clean picture. One direction adds noise on
  a fixed recipe; the other removes it with a learned network.
- **Trap:** Each arrow is a probability distribution for one small step, not a network layer, and
  one single network is reused at every step.
- **Check:** Which direction needs no learning? (Adding noise.)

```
x_T  <-> ... <-> x_t  <-> x_(t-1) <-> ... <-> x_0
noise                                         image
     -- p: learned, removes noise  -->
     <-- q: fixed, adds noise       --
```

### 6.3 U-Net
- **Grammar:** Slab
- **Figure:** [`figures/u-net.svg`](figures/u-net.svg)
- **Search:** U-Net architecture diagram
- **Source:** Ronneberger et al., [U-Net](https://arxiv.org/abs/1505.04597) (2015), Fig. 1.
- **Read it:** Down the left side, images shrink and channels grow (64 up to 1024). Up the right
  side, they grow back. Gray arrows across the U copy fine detail over.
- **Trap:** The U is just a page layout. The horizontal skips are concatenated, unlike ResNet's
  addition. U-Net began in biomedical segmentation, not generation.
- **Check:** Why does the denoiser need the skips? (The bottom has context but has lost pixel
  detail, and a denoised image needs that detail.)

```
64 ---------------- copy ---------------> 64
   128 ------------ copy -----------> 128
      256 --------- copy --------> 256
         512 ------ copy -----> 512
                  1024
```

### 6.4 Latent diffusion (Stable Diffusion)
- **Grammar:** Block
- **Figure:** [`figures/latent-diffusion.svg`](figures/latent-diffusion.svg)
- **Search:** latent diffusion stable diffusion architecture diagram
- **Source:** Rombach et al., [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) (2022), Fig. 3. Explained: Alammar, [The Illustrated Stable Diffusion](https://jalammar.github.io/illustrated-stable-diffusion/).
- **Read it:** Three regions: pixel space (a VAE encoder and decoder at the edges), latent space
  (diffusion with a U-Net in the middle), and conditioning (the text encoder feeding in).
- **Trap:** Diffusion happens in the compressed latent, never on pixels. Text enters through
  cross-attention, the same mechanism as the Transformer's left-to-right arrow.
- **Check:** Which of the earlier diagrams appear inside this one? (VAE, U-Net, the diffusion
  chain, attention.)

## Phase 7 - Putting it together

### 7.1 Vision Transformer (ViT)
- **Grammar:** Block
- **Figure:** [`figures/vit.svg`](figures/vit.svg)
- **Search:** Vision Transformer ViT architecture diagram
- **Source:** Dosovitskiy et al., [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) (2021), Fig. 1.
- **Read it:** An image is cut into patches, each flattened and embedded like a word, and a standard
  Transformer encoder reads the sequence.
- **Trap:** The extra token marked 0 at the start is not a patch: it is the summary used for the
  final classification.
- **Check:** How many 16x16 patches fit in a 224x224 image? (14 * 14 = 196.)

### 7.1 CLIP
- **Grammar:** Block
- **Figure:** [`figures/clip.svg`](figures/clip.svg)
- **Search:** CLIP contrastive image text encoder diagram
- **Source:** Radford et al., [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) (2021), Fig. 1.
- **Read it:** An image encoder and a text encoder feed a grid of similarity scores. Training
  makes the diagonal, the true pairs, score highest.
- **Trap:** The grid is a similarity table for one batch, not an attention map.
- **Check:** In a batch of 4 pairs, how many cells should score low? (12.)

### 7.1 Agent loop
- **Grammar:** Block
- **Figure:** [`figures/agent-loop.svg`](figures/agent-loop.svg)
- **Search:** autonomous AI agent loop LLM tools diagram
- **Source:** Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (2024), the autonomous agent figure.
- **Read it:** An LLM chooses an action, a tool or environment responds, the result returns to the
  LLM, and the loop continues until it stops.
- **Trap:** This is a system diagram around a model. Nothing inside the LLM box has changed, and
  every box from Phase 5 is still inside it.
- **Check:** What decides when the loop ends? (The LLM, or a limit set around it.)

## Final review (topic 7.4)

The diagram wall: show the Search images for ten or more entries, across all phases, with no
labels visible if possible. For each, the learner names it, states its grammar, and traces one
input through. Reteach any that fall short and record them in Open questions.
