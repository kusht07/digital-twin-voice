import tempfile
import time

import config


def transcribe_audio(audio_path: str) -> str:
    """Speech-to-text with Deepgram Nova."""
    config.ensure_clients()
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    response = config.deepgram_client.listen.v1.media.transcribe_file(
        request=audio_bytes,
        model=config.DEEPGRAM_STT_MODEL,
        smart_format=True,
        punctuate=True,
    )
    return response.results.channels[0].alternatives[0].transcript.strip()


def speak_text(text: str) -> str:
    """Text-to-speech with Deepgram Aura; returns a unique WAV path (helps autoplay)."""
    config.ensure_clients()
    text = text[:2000]
    stream = config.deepgram_client.speak.v1.audio.generate(
        text=text,
        model=config.DEEPGRAM_TTS_MODEL,
        encoding="linear16",
        container="wav",
    )
    audio_bytes = b"".join(stream)
    out = tempfile.NamedTemporaryFile(delete=False, suffix=f"_reply_{time.time_ns()}.wav")
    out.write(audio_bytes)
    out.close()
    return out.name
