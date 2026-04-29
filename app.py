import gradio as gr

def test():
    return "App is LIVE 🚀"

demo = gr.Interface(fn=test, inputs=[], outputs="text")

demo.launch(server_name="0.0.0.0", server_port=7860)
