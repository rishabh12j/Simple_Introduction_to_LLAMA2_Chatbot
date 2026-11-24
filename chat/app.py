"""Streaming chatbot on Groq, plus an API-only endpoint for one-shot replies.

Originally called a Llama 2 model deployed on Baseten (since retired).
Secrets: GROQ_API_KEY.
"""

import gradio as gr

from chatbot import MODEL, chat_once, stream_reply

with gr.Blocks(title="Gradio Chat") as demo:
    gr.ChatInterface(
        stream_reply,
        title="💬 Gradio Chat",
        description=(
            f"A streaming chatbot running on Groq (`{MODEL}`). Developers can also call the "
            "`/ask` API endpoint for a single reply (see *Use via API* at the bottom of the page)."
        ),
        examples=["Explain RAG in two sentences.", "Give me three interview questions about Python generators."],
        cache_examples=False,
        api_name="chat",
    )

    def ask(message: str) -> str:
        """One-shot reply without chat history."""
        return chat_once(message)

    gr.api(ask, api_name="ask")

if __name__ == "__main__":
    demo.launch()
