# Scam Guardian 🛡️

A real-time scam shield for families, built with NVIDIA Nemotron models on Nebius Token Factory, LangGraph, and Tavily.

> Starter version: Telegram bot + LangGraph investigation graph (triage → parallel link check and web research → judge → reply).

## Quick start

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # then fill in your keys

python -m scripts.test_connection   # 1. model works?
python -m scripts.try_message       # 2. full graph works?
python -m channels.telegram_bot     # 3. bot is live
```

## How it works

1. **Triage** (Nemotron Nano) extracts links, phone numbers, emails, the brand being impersonated, and red flags.
2. **Link check** and **Web research** run in parallel. Links are never opened; they're checked for lookalike domains and against Google Safe Browsing. Tavily searches the sender and the brand's official warnings.
3. **Judge** (Nemotron Ultra in production) weighs all the evidence and gives a verdict.
4. **Reply** sends a plain-language verdict and next steps.

## License

MIT
