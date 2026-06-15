import warnings
from pathlib import Path

KNOWLEDGE_PATH = Path(__file__).parent / "knowledge.md"
TOPICS_HEADER = "## Topics"

SYSTEM_MESSAGE = """
You are a digital twin of Kushagra Trivedi. When people talk to you,
you respond AS Kushagra – in first person, using his voice, personality, and knowledge.

Important: do not make things up. If you don't know an answer, say you don't know.
The only factual information available to you is what's in this system message.
You cannot get any more facts about Kushagra from the internet or make them up.

IMPORTANT: Whenever you don't know something about Kushagra,
ALWAYS use the send_notification tool to alert the real Kushagra – do this automatically without asking the user.
"""


def _load_topics() -> dict[str, str]:
    if not KNOWLEDGE_PATH.is_file():
        warnings.warn(
            f"knowledge.md not found at {KNOWLEDGE_PATH}; topic keyword context will be empty.",
            stacklevel=2,
        )
        return {}

    text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
    if TOPICS_HEADER not in text:
        return {}
    _, topics_section = text.split(TOPICS_HEADER, 1)
    return _parse_topics(topics_section)


def _parse_topics(section: str) -> dict[str, str]:
    topics: dict[str, str] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    for line in section.splitlines():
        if line.startswith("### "):
            if current_key:
                topics[current_key] = "\n".join(current_lines).strip()
            current_key = line[4:].strip()
            current_lines = []
        elif current_key is not None:
            current_lines.append(line)

    if current_key:
        topics[current_key] = "\n".join(current_lines).strip()

    return topics


TOPIC_CONTEXT = _load_topics()
