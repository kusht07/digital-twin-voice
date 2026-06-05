import os

from dotenv import load_dotenv
from deepgram import DeepgramClient
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

openai_client: OpenAI | None = None
deepgram_client: DeepgramClient | None = None


def ensure_clients() -> None:
    """Validate env vars and initialize API clients (called at app startup)."""
    global openai_client, deepgram_client

    if OPENAI_API_KEY is None:
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and add your key.")
    if DEEPGRAM_API_KEY is None:
        raise RuntimeError("DEEPGRAM_API_KEY is missing. Copy .env.example to .env and add your key.")

    if openai_client is None:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    if deepgram_client is None:
        deepgram_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
