import requests
import os
import gradio as gr
import json

# Replace the empty string with your model id below
model_id = "7qrmoo93"

def res(data):
    print(data)
    resp = requests.post("https://model-7qrmoo93.api.baseten.co/production/predict",headers={"Authorization": "Api-Key {Insert_Your_Baseten_API_Key_Here}"},json={'top_p': 0.75, 'prompt': data, 'num_beams': 4, 'temperature': 0.4},)
    print(resp.json()) 
    return resp.json()

def main():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column(scale=3):
                text_input = gr.Textbox(lines=4, placeholder="Input prompt")
        with gr.Row():
            with gr.Column(scale=1):
                text_output = gr.Textbox(lines=4, placeholder="Output prompt")
        with gr.Row():
            text_button = gr.Button("Send")
        text_button.click(res, text_input, text_output)
    demo.launch()

if __name__ == "__main__":
    main()
