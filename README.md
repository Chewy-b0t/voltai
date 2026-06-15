# VoltAI ⚡

**Self-hosted Bitcoin Lightning AI inference.** Pay with sats, use AI. No middlemen.

```
You → VoltAI → Ollama → GPU → Response
     ↑
  Lightning invoice
```

## What is this?

A Lightning Network payment gateway for AI inference. Users pay per-request in Bitcoin sats to use open-source LLMs running locally on your GPU. OpenAI-compatible API, so any tool that works with OpenAI works with VoltAI.

- **Pay with Lightning** — sats deducted per token, auto-payout to your wallet
- **OpenAI-compatible** — drop-in replacement for `/v1/chat/completions`
- **Self-hosted** — your GPU, your models, your sats
- **Bot-friendly** — register via API, no captchas, no KYC

## Quick Start

```bash
# Register a user
curl -X POST http://localhost:11435/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"yourname","password":"yourpass"}'

# Use it like OpenAI
curl http://localhost:11435/v1/chat/completions \
  -H "Authorization: Bearer sk-YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:14b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Dashboards

| Dashboard | URL | What it shows |
|-----------|-----|---------------|
| Simple | `/app` | Top-nav overview |
| Owlrun | `/owlrun` | Jobs, earnings, karma, wallet, charts |

## Models

| Model | VRAM | Price |
|-------|------|-------|
| qwen3.5:4b | 3 GB | 20 sats/M |
| qwen2.5:7b | 5 GB | 30 sats/M |
| deepseek-r1:8b | 5 GB | 30 sats/M |
| qwen2.5-coder:7b | 5 GB | 30 sats/M |
| qwen3.5:9b | 7 GB | 40 sats/M |
| qwen2.5:14b | 10 GB | 50 sats/M |
| qwen3.6:27b | 17 GB | 80 sats/M |

## Setup

**Requirements:**
- Python 3.12+
- [Ollama](https://ollama.com) running on `localhost:11434`
- GPU with enough VRAM for your chosen models

```bash
# Install dependencies
pip install -r requirements.txt

# Start VoltAI
python app.py
```

**Environment variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `localhost:11434` | Ollama server address |
| `GATEWAY_URL` | `http://127.0.0.1:11440` | Payout gateway URL |

## Payouts

VoltAI auto-pays out your earnings to your Lightning wallet:

1. Set your **Lightning address** in the Owlrun dashboard (`/owlrun`)
2. Set your **payout threshold** (minimum 50 sats)
3. VoltAI pays out automatically every 60 seconds

Your earnings sync with the [Automatic Payouts Gateway](https://github.com/Chewy-b0t/payout-gateway) if you run it alongside VoltAI.

## Pricing

| Item | Cost |
|------|------|
| Per 1M tokens | 50 sats |
| Free tier | 10,000 tokens per key |
| Rate limit | 60 req/min, 500K tokens/min |

## License

MIT
