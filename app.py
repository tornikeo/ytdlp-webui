import gradio as gr
from gradio import components
import os, tempfile
from yt_dlp import YoutubeDL
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from uuid import uuid4
import logging

logger = logging.Logger(__name__, level='DEBUG')

@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

EXTRACT_AUDIO_OPTS = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
    }]
}

def get_dir_file_names_as_list(suffix):
    return list([str(e.name) for e in user_download_dir.glob('*') if e.suffix == suffix])

def get_dir_contents_as_list():
    return list([str(e) for e in user_download_dir.glob('*')])

def get_random_string():
    return str(uuid4()).replace('-','')[:8]

def download_fn(url, extract_audio):
    print("Download triggered, with ", url)
    # with tempfile.Tem() as f:
    download_dir = Path(f'/tmp/yt_dlp_downloads/{get_random_string()}')
    download_dir.mkdir(exist_ok=True)
    params=dict(
        # paths=dict(
            
        # )
        outtmpl=str(download_dir / '%(title)s.%(ext)s'),
        # progress_hooks=[print],
        # postprogress_hooks=[print]
    )
    if extract_audio:
        params.update( EXTRACT_AUDIO_OPTS )
    with YoutubeDL(params) as ydl:
        ydl.download(url)
    folder_contents = list(Path(download_dir).glob('*'))
    print("Downloads complete at: ", download_dir)
    return folder_contents

with gr.Blocks() as demo:
    gr.Markdown("## Download youtube videos")
    with gr.Tab("Download"):
        with gr.Row():
            with gr.Column():   
                gr.Markdown("### Step 1 - Paste URL below")
                video_url = gr.Textbox(lines=1, max_lines=1, label="URL", value="https://www.youtube.com/watch?v=UT5F9AXjwhg&list=PL5v_4vO5F1GUpKg7or5qjeE8gfHgpvLCB") #value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Step 2 - Choose options")
                extract_audio = gr.Checkbox(label="Extract audio (mp3)")
        with gr.Row():
            with gr.Column():   
                gr.Markdown("### Step 3 - Prepare files")
                download = gr.Button(value="Prepare files")
        with gr.Row():
            with gr.Column():   
                gr.Markdown("### Step 4 - Download files")
                download_files = gr.File(label='Downloaded files will appear here', file_count="multiple", interactive=False)
    # with gr.Tab("Postprocess"):
    #     with gr.Tab("Audio files (MP3)"):
    #         with gr.Row():
    #             postprocess_files = gr.CheckboxGroup(choices=get_dir_file_names_as_list('.mp3'), file_count="multiple")
    #         with gr.Row():
    #             postprocess = gr.Button()
    #     with gr.Tab("Video files (MP4)"):
    #         with gr.Row():
    #             postprocess_files = gr.CheckboxGroup(choices=get_dir_file_names_as_list('.mp4'), file_count="multiple")
    #         with gr.Row():
    #             postprocess = gr.Button() 
    download.click(download_fn, 
        inputs=[video_url, extract_audio],
        outputs=[download_files]
    )

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0', server_port=os.environ.get('PORT', 8999), show_error=True, show_tips=False, show_api=False)