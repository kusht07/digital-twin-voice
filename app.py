"""Kush Digital Twin — multimodal voice + text chat with RAG."""

from config import ensure_clients, ensure_openai_client
from rag import ensure_index
from ui import CSS, create_demo


def startup() -> None:
    """Warm up the RAG index (OpenAI only — voice keys load on first mic use)."""
    ensure_openai_client()
    ensure_index()


demo = create_demo(on_load=startup)

# Hugging Face Spaces looks for `demo`, `app`, or `interface`.
app = demo


if __name__ == "__main__":
    ensure_clients()
    startup()
    demo.launch(inbrowser=True, css=CSS)
