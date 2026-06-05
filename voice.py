import tempfile
import time

from config import deepgram_client, ensure_clients


def transcribe_audio(audio_path: str) -> str:
    """Speech-to-text with Deepgram Nova."""
    ensure_clients()
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    response = deepgram_client.listen.v1.media.transcribe_file(
        request=audio_bytes,
        model="nova-3",
        smart_format=True,
        punctuate=True,
    )
    return response.results.channels[0].alternatives[0].transcript.strip()


def speak_text(text: str) -> str:
    """Text-to-speech with Deepgram Aura; returns a unique WAV path (helps autoplay)."""
    ensure_clients()
    text = text[:2000]
    stream = deepgram_client.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
        encoding="linear16",
        container="wav",
    )
    audio_bytes = b"".join(stream)
    out = tempfile.NamedTemporaryFile(delete=False, suffix=f"_reply_{time.time_ns()}.wav")
    out.write(audio_bytes)
    out.close()
    return out.name
