import gradio as gr

from chat import response_ai
from voice import speak_text, transcribe_audio

CSS = """
#record-box { background: rgb(39, 39, 42) !important; border-radius: 8px !important; padding: 8px !important; }
#record-box #mic { width: 100% !important; background: transparent !important; }
#record-box #mic .wrap, #record-box #mic .form, #record-box #mic .empty,
#record-box #mic .audio-container { background: transparent !important; }
#record-box #mic .empty, #record-box #mic .audio-container { min-height: 0 !important; }
/* Hide the reply player off-screen but keep it rendered so autoplay works */
#reply-audio { position: absolute !important; width: 1px !important; height: 1px !important;
  overflow: hidden !important; opacity: 0 !important; pointer-events: none !important; }
"""

RESET_AUDIO_JS = """
() => {
  const app = document.querySelector('gradio-app');
  const root = (app && app.shadowRoot) ? app.shadowRoot : document;
  const c = root.querySelector('#reply-audio');
  if (!c) return;
  const m = c.querySelector('audio, video');
  if (!m) return;
  const play = () => { try { m.currentTime = 0; } catch (e) {} const p = m.play(); if (p && p.catch) p.catch(() => {}); };
  if (m.readyState >= 2) play(); else m.addEventListener('loadeddata', play, { once: true });
}
"""


def voice_transcribe(audio, history):
    """Step 1: transcribe speech, show it as the user message, and clear the mic."""
    if audio is None:
        return history, None
    try:
        transcript = transcribe_audio(audio)
    except Exception as e:
        return history + [{"role": "assistant", "content": f"Error: {e}"}], None
    if not transcript:
        return history, None
    return history + [{"role": "user", "content": transcript}], None


def voice_reply(history):
    """Step 2: LLM reply + autoplayed speech."""
    if not history or history[-1]["role"] != "user":
        yield history, None
        return
    try:
        reply = response_ai(history)
        audio_path = speak_text(reply)
    except Exception as e:
        yield history + [{"role": "assistant", "content": f"Error: {e}"}], None
        return

    yield history + [{"role": "assistant", "content": reply}], audio_path


def add_user_message(message, history):
    """Step 1: show the user message and clear the textbox immediately."""
    if not message or not message.strip():
        return history, message
    return history + [{"role": "user", "content": message.strip()}], ""


def bot_reply(history):
    """Step 2: generate the assistant reply in chat only (no TTS)."""
    if not history or history[-1]["role"] != "user":
        yield history
        return
    try:
        reply = response_ai(history)
    except Exception as e:
        yield history + [{"role": "assistant", "content": f"Error: {e}"}]
        return

    yield history + [{"role": "assistant", "content": reply}]


def create_demo() -> gr.Blocks:
    with gr.Blocks(title="Kush Digital Twin — Voice") as demo:
        gr.Markdown("# MultiModal Chat")
        chatbot = gr.Chatbot(show_label=False, height=420, autoscroll=True)
        text_in = gr.Textbox(show_label=False, placeholder="Type a message…", container=False)
        with gr.Column(elem_id="record-box"):
            mic = gr.Audio(
                sources=["microphone"],
                type="filepath",
                show_label=False,
                container=False,
                elem_id="mic",
            )

        audio_out = gr.Audio(autoplay=True, interactive=False, elem_id="reply-audio")

        mic.stop_recording(
            voice_transcribe, [mic, chatbot], [chatbot, mic], queue=False,
        ).then(voice_reply, chatbot, [chatbot, audio_out])

        text_in.submit(
            add_user_message, [text_in, chatbot], [chatbot, text_in], queue=False,
        ).then(bot_reply, chatbot, chatbot)

        audio_out.change(None, None, None, js=RESET_AUDIO_JS)

    demo.queue(default_concurrency_limit=1)
    return demo
