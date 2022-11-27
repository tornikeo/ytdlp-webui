# import gradio as gr
# from gradio import components
import os, tempfile
from yt_dlp import YoutubeDL
from contextlib import contextmanager
from io import BytesIO
from pathlib import Path
from uuid import uuid4
import logging
import shutil
from typing import List
import streamlit as st

logger = logging.Logger(__name__, level='DEBUG')

@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

@contextmanager
def session_state_flag(flagname: str):
    st.session_state[flagname] = True
    try:
        yield
    finally:
        st.session_state[flagname] = False


EXTRACT_AUDIO_OPTS = {
    'format': 'm4a/bestaudio/best',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

def get_random_string():
    return str(uuid4()).replace('-','')[:8]

def dir_contents(dir:Path) -> List:
    folder_contents = list(Path(dir).glob('*'))
    return folder_contents
def trim_with_elipsis(s:str, max_len=24)->str:
    if len(s) < max_len:
        return s
    else:
        return s[:max_len] + '...'

def download_fn(url: str, audio:bool, progbar, progstr):
    with session_state_flag('loading'):
        st.session_state.loading = True
        print("Download triggered, with ", url)
        # with tempfile.Tem() as f:
        session_dir = Path(f'/tmp/yt_dlp_downloads/{get_random_string()}')
        download_dir = session_dir / 'downloads'
        download_dir.mkdir(exist_ok=True, parents=True)


        progbar = progbar.progress(0)
        progstr.write("Process starting...")
        def _increment(state):
            try:
                info_dict = state['info_dict']
                progstr.write("Loading: "+trim_with_elipsis(info_dict['title']))
                if state['status'] == "finished":
                    progbar.progress(float(info_dict['playlist_index'] / info_dict['n_entries']))
            except KeyError as e:
                print("Missing key, ignoring error: ", e)
            

        params=dict(
            # paths=dict(
                
            # )
            playlist_items = f'1-{st.session_state.get("playlist_length", 5)}',
            outtmpl=str(download_dir / '%(title)s.%(ext)s'),
            progress_hooks=[_increment],
            # postprogress_hooks=[print]
        )
        if audio:
            params.update( EXTRACT_AUDIO_OPTS )

        with YoutubeDL(params) as ydl:
            ydl.download(url)
        archive_file = session_dir / 'all_files'
        archive_file = shutil.make_archive(archive_file, 'zip', download_dir)

        print("Downloads complete at: ", download_dir)
        st.session_state.download_file = archive_file

st.header('Download youtube videos')
with st.container():
    with st.container():
        st.subheader('Step 1 - Paste URL below')
        st.text_input(label="URL", 
            value="https://www.youtube.com/watch?v=UT5F9AXjwhg&list=PL5v_4vO5F1GUpKg7or5qjeE8gfHgpvLCB",
            key="url",
        )
    with st.container():
        st.subheader('Step 2 - Choose options')
        with st.container():
            st.radio(
                "What do you need?",
                ["Give me the music 🎵","I want the video 🎥"],
                index=0,
                horizontal=True,
                key="mediatype"
            )
            st.slider(
                "(Playlist) How many videos do you want?",
                1, 20, 2,
                key="playlist_length"
            )
    with st.container():
        st.subheader('Step 3 - Prepare files')
        col1, col2 = st.columns([2,5])
        with col2:
            progstr = st.empty()
            progbar = st.empty()
        with col1:
            st.button(
                label="Prepare files ⚙️",
                on_click=download_fn,
                kwargs=dict(
                    audio="music" in st.session_state.mediatype,
                    url = st.session_state.url, 
                    progbar = progbar,
                    progstr = progstr,
                )
            )
            
    with st.container():
        st.subheader('Step 4 - Download files')

    if 'download_file' in st.session_state:
        st.download_button(
            label=' ⬇️ Download files 📁',
            data=Path(st.session_state.download_file).open('rb'),
            file_name="Youtube_Downloads.zip",
        )   
    else:
        st.button(
            label=' ⬇️ Download files 📁',
            disabled=True,
            help='Psst! Click "Prepare Files" first.'
        )