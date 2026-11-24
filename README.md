# Simple Introduction to LLM Chatbots

This repo started in April 2024 as a basic Gradio front end for a Llama 2 model I deployed on Baseten, with chat history as the planned next step. The Baseten deployment has since been retired, so in November 2026 both apps were rebuilt on Groq and redeployed:

| App | Folder | Live demo |
|---|---|---|
| **LLM prompt playground**: one prompt, adjustable temperature, top-p and length, with latency and token usage | [`app.py`](app.py) | [CourseWork Space](https://huggingface.co/spaces/Rishabh12j/CourseWork) |
| **Streaming chatbot with history** (the "next step" from the original version), plus an API-only `/ask` endpoint | [`chat/`](chat) | [Gradio Chat Space](https://huggingface.co/spaces/Rishabh12j/Gradio_chat) |

## How it works

- Both apps call Groq through its OpenAI-compatible API with the official `openai` Python SDK.
- The playground sends a single chat-completion request with your sampling settings and reports latency and token counts from the response.
- The chatbot uses `gr.ChatInterface` with `stream=True`, yielding the reply as tokens arrive; `gr.api()` adds a one-shot `/ask` endpoint without history.

## Run locally

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here      # from console.groq.com
python app.py                          # prompt playground
python chat/app.py                     # chatbot (run from the repo root or chat/)
```

Optional settings: `GROQ_MODEL` (chatbot model, default `openai/gpt-oss-120b`) and `GROQ_MODELS` (comma-separated models for the playground dropdown).

## History

- **2024:** Llama 2 on Baseten behind a single Gradio textbox.
- **2026:** rebuilt on Groq after the Baseten deployment was retired; chat history and streaming added in `chat/`.

---

**Author:** Rishabh Jain · [Hugging Face](https://huggingface.co/Rishabh12j) · [Portfolio](https://rishabh12j.github.io)
