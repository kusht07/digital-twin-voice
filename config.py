import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ROOT = Path(__file__).parent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
DEEPGRAM_STT_MODEL = os.getenv("DEEPGRAM_STT_MODEL", "nova-3")
DEEPGRAM_TTS_MODEL = os.getenv("DEEPGRAM_TTS_MODEL", "aura-2-thalia-en")

RAG_N_RESULTS = int(os.getenv("RAG_N_RESULTS", "3"))
RAG_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "500"))
RAG_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "50"))
RAG_DEBUG = os.getenv("RAG_DEBUG", "").lower() in ("1", "true", "yes")

_default_chroma = "chroma_db_twin"
if os.getenv("SPACE_ID") and not os.getenv("CHROMA_PATH"):
    _default_chroma = "/tmp/chroma_db_twin"
CHROMA_PATH = Path(os.getenv("CHROMA_PATH", _default_chroma))
if not CHROMA_PATH.is_absolute():
    CHROMA_PATH = ROOT / CHROMA_PATH

openai_client: OpenAI | None = None
deepgram_client = None


def ensure_openai_client() -> OpenAI:
    global openai_client
    if OPENAI_API_KEY is None:
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and add your key.")
    if openai_client is None:
        openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return openai_client


def ensure_deepgram_client():
    global deepgram_client
    if DEEPGRAM_API_KEY is None:
        raise RuntimeError("DEEPGRAM_API_KEY is missing. Copy .env.example to .env and add your key.")
    if deepgram_client is None:
        from deepgram import DeepgramClient

        deepgram_client = DeepgramClient(api_key=DEEPGRAM_API_KEY)
    return deepgram_client


def ensure_clients() -> None:
    """Validate env vars and initialize API clients (called at app startup)."""
    ensure_openai_client()
    ensure_deepgram_client()
