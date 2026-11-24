import os

from openai import OpenAI

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
SYSTEM = "You are a helpful, concise assistant."
MISSING_KEY = "This Space is missing its Groq key. The owner needs to add the secret `GROQ_API_KEY`."


def _client() -> OpenAI | None:
    key = os.getenv("GROQ_API_KEY") or os.getenv("use_auth_token")
    return OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1") if key else None


def _messages(message: str, history: list) -> list[dict]:
    msgs = [{"role": "system", "content": SYSTEM}]
    for turn in history or []:
        if isinstance(turn, dict) and turn.get("role") in {"user", "assistant"}:
            content = turn.get("content")
            if isinstance(content, list):  # Gradio 6 can send content parts
                content = " ".join(p.get("text", "") for p in content if isinstance(p, dict))
            msgs.append({"role": turn["role"], "content": str(content)})
    msgs.append({"role": "user", "content": message})
    return msgs


def stream_reply(message: str, history: list):
    client = _client()
    if client is None:
        yield MISSING_KEY
        return
    try:
        stream = client.chat.completions.create(
            model=MODEL, messages=_messages(message, history), temperature=0.5, stream=True
        )
        text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta.content if chunk.choices else None
            if delta:
                text += delta
                yield text
    except Exception as exc:
        yield f"Sorry, the model call failed ({type(exc).__name__}: {exc})."


def chat_once(message: str) -> str:
    client = _client()
    if client is None:
        return MISSING_KEY
    reply = client.chat.completions.create(model=MODEL, messages=_messages(message, []), temperature=0.5)
    return reply.choices[0].message.content
