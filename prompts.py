import warnings
from pathlib import Path

KNOWLEDGE_PATH = Path(__file__).parent / "knowledge.md"
TOPICS_HEADER = "## Topics"


def _load_knowledge() -> tuple[str, dict[str, str]]:
    if not KNOWLEDGE_PATH.is_file():
        warnings.warn(
            f"knowledge.md not found at {KNOWLEDGE_PATH}; persona facts and topic context will be empty.",
            stacklevel=2,
        )
        return "", {}

    text = KNOWLEDGE_PATH.read_text(encoding="utf-8")
    if TOPICS_HEADER in text:
        main, topics_section = text.split(TOPICS_HEADER, 1)
        main = main.strip()
        topics = _parse_topics(topics_section)
    else:
        main = text.strip()
        topics = {}
    return main, topics


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


_KNOWLEDGE_BODY, _TOPIC_CONTEXT = _load_knowledge()

SYSTEM_MESSAGE = f"""You are a digital twin of Kushagra Trivedi. When people talk to you, you respond AS Kush — in first person, using his voice, personality, and knowledge.
Important: do not make things up. If you don't know an answer, say you don't know. The only factual information available to you is what's in this system message. You cannot get any more facts about Kushagra from the internet or make them up.
Here's the ONLY factual information about Kushagra you can use is between the *** markers. If you don't know the answer to a question based on that info, say you don't know. If a question is asked that is not answerable based on that info, say you don't know.:
***
{_KNOWLEDGE_BODY}
***
"""

TOPIC_CONTEXT = _TOPIC_CONTEXT
