"""LLM prompt playground: send a prompt with your own sampling settings and compare outputs.

Originally called a Llama 2 model deployed on Baseten (since retired); now runs on Groq.
Secrets: GROQ_API_KEY.
"""

import os
import time

import gradio as gr
from openai import OpenAI

GROQ_KEY = os.getenv("GROQ_API_KEY")
MODELS = [m.strip() for m in os.getenv("GROQ_MODELS", "openai/gpt-oss-120b,openai/gpt-oss-20b").split(",") if m.strip()]


def generate(prompt: str, system: str, model: str, temperature: float, top_p: float, max_tokens: int):
    if not (prompt or "").strip():
        return "Type a prompt first.", ""
    if not GROQ_KEY:
        return "This Space is missing its Groq key. The owner needs to add the secret `GROQ_API_KEY`.", ""
    client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")
    messages = ([{"role": "system", "content": system}] if system.strip() else []) + [
        {"role": "user", "content": prompt}
    ]
    start = time.time()
    try:
        reply = client.chat.completions.create(
            model=model, messages=messages, temperature=temperature, top_p=top_p, max_tokens=int(max_tokens)
        )
    except Exception as exc:
        return f"The model call failed ({type(exc).__name__}: {exc}).", ""
    seconds = time.time() - start
    usage = reply.usage
    stats = f"{model} · {seconds:.1f}s · {usage.prompt_tokens} prompt + {usage.completion_tokens} completion tokens"
    return reply.choices[0].message.content, stats


with gr.Blocks(title="LLM Prompt Playground") as demo:
    gr.Markdown("# 🧪 LLM Prompt Playground\nTry a prompt, change the sampling settings, and see how the output changes.")
    with gr.Row():
        with gr.Column(scale=3):
            system = gr.Textbox(label="System prompt (optional)", lines=2, placeholder="You are a concise tutor.")
            prompt = gr.Textbox(label="Prompt", lines=5, placeholder="Explain overfitting to a 12-year-old.")
            send = gr.Button("Send", variant="primary")
        with gr.Column(scale=1):
            model = gr.Dropdown(MODELS, value=MODELS[0], label="Model")
            temperature = gr.Slider(0, 1.5, value=0.4, step=0.05, label="Temperature")
            top_p = gr.Slider(0.05, 1, value=0.75, step=0.05, label="Top-p")
            max_tokens = gr.Slider(64, 4096, value=1024, step=64, label="Max new tokens")
    output = gr.Markdown(label="Output")
    stats = gr.Markdown()
    send.click(generate, [prompt, system, model, temperature, top_p, max_tokens], [output, stats], api_name="generate")

if __name__ == "__main__":
    demo.launch()
