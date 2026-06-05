# Digital Twin Voice

A multimodal digital twin chatbot with **text** and **voice** input, powered by OpenAI (LLM + tool calling), Deepgram (speech-to-text and text-to-speech), and Gradio (web UI).

Converted from the `digital-twin-voice2.ipynb` notebook in the AI Engineering course.

## Architecture

See the flow diagram in [`docs/digital-twin-voice-flow.excalidraw`](docs/digital-twin-voice-flow.excalidraw) (open at [excalidraw.com](https://excalidraw.com)).

**High-level flow:**

1. **Text path** — user types → OpenAI chat (with tools) → reply in chat
2. **Voice path** — user records → Deepgram STT → OpenAI chat (with tools) → Deepgram TTS → autoplay reply audio

**Tools available to the LLM:**

- `send_notification` — Pushover alert to your phone (optional)
- `roll_dice` — simulated dice roll

**Dynamic context:** keywords in the user's message (`2011`, `dishes`, `sports`, `vacation`) inject extra persona context into the system prompt.

## Prerequisites

- Python 3.10+
- API keys:
  - [OpenAI](https://platform.openai.com/api-keys) (required)
  - [Deepgram](https://console.deepgram.com/) (required)
  - [Pushover](https://pushover.net/) (optional, for notification tool)

## Quick start

```bash
# Clone or cd into this directory
cd digital-twin-voice

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Run the app
python app.py
```

Gradio opens at `http://127.0.0.1:7860` (port may vary). Use the text box or microphone to chat.

## Project layout

```
digital-twin-voice/
├── app.py              # Entry point
├── config.py           # Environment variables and API clients
├── prompts.py          # System prompt and topic context
├── tools.py            # Pushover + dice tools, tool-call handler
├── chat.py             # OpenAI chat loop with tool calling
├── voice.py            # Deepgram STT / TTS
├── ui.py               # Gradio interface
├── requirements.txt
├── .env.example
└── docs/
    └── digital-twin-voice-flow.excalidraw
```

## Customization

- **Persona:** edit `prompts.py` (`SYSTEM_MESSAGE`, `TOPIC_CONTEXT`)
- **Tools:** add functions in `tools.py` and register them in `TOOLS`
- **Model:** change `MODEL` in `chat.py` (default: `gpt-4.1-mini`)
- **Voice:** change Deepgram models in `voice.py` (`nova-3` for STT, `aura-2-thalia-en` for TTS)

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `DEEPGRAM_API_KEY` | Yes | Deepgram API key |
| `PUSHOVER_USER` | No | Pushover user key (for notification tool) |
| `PUSHOVER_TOKEN` | No | Pushover app token (for notification tool) |

## License

Educational project from the AI Engineering course.
