# Lesson 02 — Local Models

## Objective

You'll have a model server running on your machine and you'll talk
to it with `curl`, then with the Python `openai` SDK. By the end
you'll know what "OpenAI-compatible" really means and how to swap
between MLX and Ollama with one line of code.

---

## Why local

- **No per-token bills.** Iterate freely. Don't worry about leaving
  a debug loop running overnight.
- **No data leaves the machine.** Useful for private code, personal
  notes, anything you wouldn't paste into a hosted service.
- **Latency you control.** No retries on rate limits. No "model
  deprecated, please migrate" emails.
- **Offline.** Work on a train.

Downsides:

- Local models are smaller and dumber than frontier hosted models.
  Gemma-3-27B is good. It is not Claude Opus.
- You pay in RAM and electricity, not in dollars.
- You have to keep the server running. It crashes sometimes.

---

## The "OpenAI-compatible" lingua franca

Almost every model server in 2025 speaks an HTTP API that mirrors
OpenAI's `/v1/chat/completions` shape, because the OpenAI Python
SDK is the de-facto client and supporting it gets you all the tools
for free.

That means:

- MLX server speaks it.
- Ollama speaks it (at `/v1`, alongside its native `/api`).
- llama.cpp's server speaks it.
- vLLM speaks it.
- Anthropic, OpenRouter, Together, Groq, Fireworks all speak it.

A "model client" in 2025 is basically: pick a base URL, pick a model
name, you're done.

---

## Hands-on: smoke-test your server

Assuming MLX is running on `8765` per lesson 00. (If Ollama, use
`11434` and the model name you pulled.)

```bash
# List models
curl -s http://127.0.0.1:8765/v1/models | jq

# Chat with one
curl -s http://127.0.0.1:8765/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/gemma-3-12b-it-4bit",
    "messages": [{"role": "user", "content": "What is 1+1? One word."}]
  }' | jq -r '.choices[0].message.content'
```

If you got `2` (or "Two" or similar), the server, the model, and
the HTTP API all work.

---

## Hands-on: the Python SDK

The OpenAI SDK works with any compatible endpoint — you just
override `base_url` and pass any string as `api_key` (local servers
don't check it).

```bash
source ~/agents101/.venv/bin/activate
uv pip install openai
```

```python
# Save as ~/agents101/hello.py
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8765/v1",
    api_key="not-needed",    # local servers ignore this
)

response = client.chat.completions.create(
    model="mlx-community/gemma-3-12b-it-4bit",
    messages=[
        {"role": "system", "content": "You are terse."},
        {"role": "user", "content": "Why is the sky blue?"},
    ],
)
print(response.choices[0].message.content)
```

```bash
python hello.py
```

That's it. You're now using a 12B-parameter language model from
Python, locally, with the same code shape as any commercial agent.

---

## Streaming

For UX you'll want streaming so tokens appear as they're generated:

```python
stream = client.chat.completions.create(
    model="mlx-community/gemma-3-12b-it-4bit",
    messages=[{"role": "user", "content": "Count slowly to ten."}],
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta.content or ""
    print(delta, end="", flush=True)
print()
```

Hermes does this for you in its TUI; you'll rarely have to write
the loop yourself, but it's good to know what's happening.

---

## Choosing a model

| Family | Size | Good for | Notes |
|---|---|---|---|
| Gemma 3 / 4 | 12B–31B | General | Google's open-weights line. 27B-4bit fits in 16GB RAM. |
| Llama 3 / 4 | 8B–70B | General | Meta's. Strong instruction-following. |
| Qwen 2.5 / 3 | 7B–72B | Coding, multilingual | Alibaba's. Excellent on code. |
| Phi-4 | 14B | Reasoning | Microsoft's. Small and surprisingly capable. |
| Mistral / Mixtral | 7B–8x22B | General | Mistral AI. MoE variants are fast. |

For agent work specifically, instruction-tuned variants (the `-it`
suffix in MLX, no suffix in Ollama for the "instruct" version)
matter much more than raw size. A 12B-it can outperform a 70B base
model on tool use.

**4-bit quants** (`-4bit`) trade a small quality hit for ~4× less
RAM. For day-to-day, take the quant. For "I'm doing a benchmark,"
take the bf16.

---

## Tool calling support

Not every local model handles tool calls well. The chat completions
API accepts `tools`, but the model has to be *trained* to emit
tool-call JSON correctly. Test before you build:

```python
response = client.chat.completions.create(
    model="...",
    messages=[{"role": "user", "content": "What is 47 * 89?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Run a Python expression and return the result",
            "parameters": {
                "type": "object",
                "properties": {"expr": {"type": "string"}},
                "required": ["expr"],
            },
        },
    }],
)
print(response.choices[0].message)
```

If the model returns a proper `tool_calls=[...]` field with
`expr="47 * 89"`, you're in business. If it returns a chatty
text answer or malformed JSON, you need a better-trained model.

Gemma 3 27B, Llama 3.1 70B, and Qwen 2.5 32B all handle tool
calls well in our experience. Smaller models are hit-or-miss.

---

## Pitfalls

- **Different ports.** MLX defaults to 8080 in some examples, 8765
  in ours. Ollama is 11434. Always check what your server actually
  bound to.
- **Model name must match exactly.** The server's `/v1/models`
  endpoint shows the canonical name; use that, not an alias from
  the docs.
- **Context length is finite.** A 12B-4bit model might support
  128k tokens of context, but generating responses uses RAM
  *quadratically* in context. Long conversations slow down a lot.
- **Tool-call quality varies wildly across model families.** Always
  test before committing to a model for agent work.
- **One server = one inference at a time.** MLX server and Ollama
  serialize requests. If you spawn 5 agents pointing at the same
  server, they queue. Don't be surprised when "concurrent" agents
  go serial.

---

## Further reading

- OpenAI chat completions API: https://platform.openai.com/docs/api-reference/chat
- Ollama docs: https://github.com/ollama/ollama/blob/main/docs/api.md
- MLX-LM: https://github.com/ml-explore/mlx-examples/tree/main/llms

---

Next: [03-first-conversation.md](03-first-conversation.md) — install
Hermes and have a conversation in your terminal.
