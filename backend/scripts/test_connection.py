"""Step 1: check that your model provider works."""
import config
from llm import chat

msg = "Your bank account is locked. Verify now: http://secure-bank-verify.co"
print(chat(config.MODEL_FAST, "You are a scam detector.",
           f"Is this a scam? Answer in one sentence: {msg}", 100))
