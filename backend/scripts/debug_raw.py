"""Shows exactly what the model sends back, to debug parsing."""
import config
from llm import client

resp = client.chat.completions.create(
    model=config.MODEL_JUDGE,
    messages=[
        {"role": "system", "content": "Respond with ONLY a JSON object with keys verdict and risk."},
        {"role": "user", "content": "USPS: pay a $1.99 fee now at usps-redelivery-help.top/pay"},
    ],
    max_tokens=700,
)
choice = resp.choices[0]
print("FINISH REASON:", choice.finish_reason)
print("CONTENT:", repr(choice.message.content)[:800])
print("REASONING:", repr(getattr(choice.message, "reasoning_content", None))[:300])