"""Loads settings from the .env file in one place."""
import os
from dotenv import load_dotenv

load_dotenv()

LLM_BASE_URL = os.environ["LLM_BASE_URL"]
LLM_API_KEY = os.environ["LLM_API_KEY"]
MODEL_FAST = os.environ["MODEL_FAST"]
MODEL_JUDGE = os.environ.get("MODEL_JUDGE") or MODEL_FAST
MODEL_VISION = os.environ.get("MODEL_VISION", "")

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
SAFE_BROWSING_API_KEY = os.environ.get("SAFE_BROWSING_API_KEY", "")

# Budget guards
MAX_TAVILY_SEARCHES = 3
