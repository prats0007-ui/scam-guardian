"""Thin wrapper around the OpenAI-compatible API (Token Factory or NVIDIA)."""
import json
import re

from openai import OpenAI

import config

client = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)


def chat(model: str, system: str, user: str, max_tokens: int = 600) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0.2,
    )
    text = resp.choices[0].message.content or ""
    # Some reasoning models include their thinking; drop it.
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def chat_json(model: str, system: str, user: str, max_tokens: int = 600) -> dict:
    """Ask for JSON and parse it robustly. Returns {} if parsing fails."""
    text = chat(model, system + "\nRespond with ONLY a JSON object.", user, max_tokens)
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        return {}
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return {}
