"""Thin wrapper around the OpenAI-compatible API (Token Factory or NVIDIA)."""
import json
import re

from openai import OpenAI

import config

client = OpenAI(base_url=config.LLM_BASE_URL, api_key=config.LLM_API_KEY)


def chat(model: str, system: str, user: str, max_tokens: int = 600,
         thinking: bool = False) -> str:
    # Thinking off by default: much cheaper, and simple steps don't need it.
    extra = None if thinking else {"chat_template_kwargs": {"enable_thinking": False}}
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
        temperature=0,
        extra_body=extra,
    )
    choice = resp.choices[0]
    if choice.finish_reason == "length":
        print(f"⚠️ Model ran out of tokens (max_tokens={max_tokens})")
    text = choice.message.content or ""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def chat_json(model: str, system: str, user: str, max_tokens: int = 600,
              thinking: bool = False) -> dict:
    """Ask for JSON and parse it robustly. Returns {} if parsing fails."""
    text = chat(model, system + "\nRespond with ONLY a JSON object.", user,
                max_tokens, thinking)
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        print("⚠️ No JSON found in model output:", repr(text)[:300])
        return {}
    try:
        return json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON from model:", repr(text)[:300])
        return {}