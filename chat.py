import config
from prompts import SYSTEM_MESSAGE, TOPIC_CONTEXT
from rag import retrieve
from tools import TOOLS, handle_tool_call


def content_to_text(content) -> str:
    """Gradio messages may store content as a string or a list of parts."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                parts.append(part.get("text") or part.get("content") or "")
            else:
                parts.append(str(part))
        return " ".join(parts).strip()
    return str(content)


def build_system_prompt(latest_user_message: str) -> str:
    system = SYSTEM_MESSAGE

    context, metadatas = retrieve(latest_user_message)
    if context:
        system += f"\n\nContext:\n\n{context}"

    if config.RAG_DEBUG and metadatas:
        print("retrieved chunks:")
        for meta in metadatas:
            print(f"  {meta['source']} — chunk {meta['chunk_index']}")

    lowered = latest_user_message.lower()
    for keyword, extra in TOPIC_CONTEXT.items():
        if keyword in lowered:
            system += f"\n\n{extra}"
    return system


def response_ai(history: list[dict]) -> str:
    """history: list of {role, content} chat messages; returns the assistant reply text."""
    config.ensure_clients()
    client = config.ensure_openai_client()
    msgs = [{"role": m["role"], "content": content_to_text(m["content"])} for m in history]
    system = build_system_prompt(msgs[-1]["content"])
    messages = [{"role": "system", "content": system}] + msgs

    reply = client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=messages,
        tools=TOOLS,
    ).choices[0].message

    while reply.tool_calls:
        messages.append(reply)
        messages.extend(handle_tool_call(reply.tool_calls))
        reply = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
        ).choices[0].message

    return reply.content
