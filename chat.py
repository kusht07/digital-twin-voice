from config import ensure_clients, openai_client
from prompts import SYSTEM_MESSAGE, TOPIC_CONTEXT
from tools import TOOLS, handle_tool_call

MODEL = "gpt-4.1-mini"


def content_to_text(content) -> str:
    """Gradio messages may store content as a string or a list of parts."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [
            (p.get("text") or p.get("content") or "") if isinstance(p, dict) else str(p)
            for p in content
        ]
        return " ".join(parts).strip()
    return str(content)


def build_system_prompt(latest_user_message: str) -> str:
    system = SYSTEM_MESSAGE
    lowered = latest_user_message.lower()
    for keyword, context in TOPIC_CONTEXT.items():
        if keyword in lowered:
            system += f"\n\n {context}"
    return system


def response_ai(history: list[dict]) -> str:
    """history: list of {role, content} chat messages; returns the assistant reply text."""
    ensure_clients()
    msgs = [{"role": m["role"], "content": content_to_text(m["content"])} for m in history]
    system = build_system_prompt(msgs[-1]["content"])
    messages = [{"role": "system", "content": system}] + msgs

    reply = openai_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
    ).choices[0].message

    while reply.tool_calls:
        messages.append(reply)
        messages.extend(handle_tool_call(reply.tool_calls))
        reply = openai_client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        ).choices[0].message

    return reply.content
