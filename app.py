import gradio as gr
import os, tempfile
from yt_dlp import YoutubeDL
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path

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

user_download_dir = Path('/tmp/yt_dlp_downloads')
user_download_dir.mkdir(exist_ok=True)


def get_dir_file_names_as_list(suffix):
    return list([str(e.name) for e in user_download_dir.glob('*') if e.suffix == suffix])

def get_dir_contents_as_list():
    return list([str(e) for e in user_download_dir.glob('*')])

def download_fn(url):
    # with tempfile.Tem() as f:
    with cwd(user_download_dir):
        with YoutubeDL() as ydl:
            ydl.download(url)
    result = str(list(Path(user_download_dir).glob('*'))[0])
    folder_contents = list(Path(user_download_dir).glob('*'))
    return result, folder_contents

with gr.Blocks() as demo:
    gr.Markdown("## Download youtube video and process it")
    with gr.Tab("Download"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Video/Playlist URL")
                video_url = gr.Textbox(lines=1, max_lines=1, show_label=False, value="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            with gr.Column():
                gr.Markdown("### Misc controls")
                extract_audio = gr.Checkbox(label="Extract Audio")
        gr.Markdown('### Video preview')
        with gr.Accordion(label="", open=False):
            video = gr.Video()
        download = gr.Button()
        gr.Markdown('###  Download files')
        download_files = gr.File(file_count="multiple")
    with gr.Tab("Postprocess"):
        with gr.Tab("Audio files (MP3)"):
            with gr.Row():
                postprocess_files = gr.CheckboxGroup(choices=get_dir_file_names_as_list('.mp3'), file_count="multiple")
            with gr.Row():
                postprocess = gr.Button()
        with gr.Tab("Video files (MP4)"):
            with gr.Row():
                postprocess_files = gr.CheckboxGroup(choices=get_dir_file_names_as_list('.mp4'), file_count="multiple")
            with gr.Row():
                postprocess = gr.Button()
    with gr.Tab("Save"):
        with gr.Row():
            download_files = gr.File(
                    value=get_dir_contents_as_list, file_count="multiple")
    download.click(download_fn, 
            inputs=[video_url],
            outputs=[video, download_files]
        )
    # text_button.click(flip_text, inputs=text_input, outputs=text_output)

demo.launch()