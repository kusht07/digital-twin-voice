"""Kush Digital Twin — multimodal voice + text chat."""

from config import ensure_clients
from ui import CSS, create_demo

if __name__ == "__main__":
    ensure_clients()
    demo = create_demo()
    demo.launch(inbrowser=True, css=CSS)
