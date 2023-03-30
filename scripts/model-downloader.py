import os
import gradio as gr
from modules import script_callbacks

def folder(content_type):
    if content_type == "Checkpoint":
       return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Stable-diffusion")
    elif content_type == "Hypernetwork":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/hypernetworks")
    elif content_type == "TextualInversion/Embedding":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/embeddings")
    elif content_type == "AestheticGradient":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/extensions/stable-diffusion-webui-aesthetic-gradients/aesthetic_embeddings")
    elif content_type == "VAE":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/VAE")
    elif content_type == "Lora/LyCORIS(LoCon/LoHA)":
         return gr.Textbox.update(value=" -d /content/stable-diffusion-webui/models/Lora")

def cfn(url, filename1, filename, opt):
    if filename1 == "Use original Filename from the Source":
       return gr.Textbox(opt).update(value=" "),  gr.Textbox(filename).update(value=" ", visible=False)
    elif filename1 == "Create New Filename(Recomended)":
         return gr.Textbox(opt).update(value=" -o "), gr.Textbox(filename).update(value=" ", visible=True)

def combine(cmd, url, content_type1, opt, filename):
    return gr.Textbox.update(cmd + url + content_type1 + opt + filename)

def inf(url, content_type1, filename, info):
    return gr.Textbox(info).update(value="[URL]:  " + url + "     [Folder Path]: " + content_type1 + "     [File Name]:  " + filename)
    
def run(command):
    with os.popen(command) as pipe:
         for line in pipe:
             line = line.rstrip()
             print(line)
             yield line

def on_ui_tabs():
    with gr.Blocks() as downloader:    
         with gr.Row():
              with gr.Column(scale=2):
                   content_type = gr.Radio(label="1. Choose Content type", choices=["Checkpoint","Hypernetwork","TextualInversion/Embedding","AestheticGradient", "VAE", "Lora/LyCORIS(LoCon/LoHA)"])
                   content_type1 = gr.Textbox(visible=False)
                   content_type.change(fn=folder, inputs=content_type, outputs=content_type1)
         with gr.Row():
              url = gr.Textbox(label="2. Put Link Download Below", max_lines=1, placeholder="Type/Paste URL Here")
              opt = gr.Textbox(value=" ", visible=False)
         with gr.Row():
              with gr.Column(scale=2):
                   filename1 = gr.Radio(label="Setting Filename", choices=["Use original Filename from the Source", "Create New Filename(Recomended)"], type="value", value="Use original Filename from the Source")
         with gr.Row():
              filename = gr.Textbox(label="3. Create new Filename", placeholder="Type/Paste Filename.extension Here", visible=False, interactive=True)
              filename1.change(fn=cfn, inputs=[url, filename1, opt, filename], outputs=[opt, filename])
         with gr.Row():
              cmd = gr.Textbox(value="aria2c --console-log-level=error -c -x 16 -s 16 -k 1M ", visible=False)
              commands = gr.Textbox(label="Information Command", visible=False, interactive=False)
              info = gr.Textbox(label="Information", placeholder="Make sure to Check properly whether everything is Correct", interactive=False)
         with gr.Row():
              content_type1.change(fn=combine, inputs=[cmd, url, content_type1, opt, filename], outputs=commands)
              url.change(fn=combine, inputs=[cmd, url, content_type1, opt, filename], outputs=commands)
              filename.change(fn=combine, inputs=[cmd, url, content_type1, opt, filename], outputs=commands)
              content_type1.change(fn=inf, inputs=[url, content_type1, filename], outputs=info)
              url.change(fn=inf, inputs=[url, content_type1, filename], outputs=info)
              filename.change(fn=inf, inputs=[url, content_type1, filename], outputs=info)
         with gr.Row():
              download_btn = gr.Button("Start Download")
              out_text = gr.Textbox(label="Download Result", placeholder="Result", show_progress=True)
              download_btn.click(fn=run, inputs=[commands], outputs=out_text, show_progress=True)

    downloader.queue(concurrency_count=5)
    return (downloader, "Model Downloader", "downloader"),
    
script_callbacks.on_ui_tabs(on_ui_tabs)
