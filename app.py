import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.set_page_config(page_title="David & Lucy 💔", page_icon="💔", layout="centered")

st.markdown(
    '<style>body {background-color: #1e1e2f; color: #fce4ec; font-family: "Courier New", monospace;} h1 {color: #ff80ab;} .stButton>button {background-color: #ffb6b9; color: #ffffff; border-radius: 10px; padding: 8px 20px;} .stButton>button:hover {background-color: #f48fb1;}</style>',
    unsafe_allow_html=True
)

st.title("David & Lucy 💔")

image = Image.open('davidlucy.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Neon Love: La historia de David y Lucy")

st.write("En una ciudad donde la esperanza se desintegra tan rápido como las balas, David y Lucy encontraron algo improbable: amor. "
         "Entre implantes y traiciones, ella soñaba con la luna y él con protegerla. Pero el amor en Night City no sobrevive sin cicatrices. "
         "Él eligió el sacrificio. Ella, la soledad estelar. Y así, entre luces rotas, terminó una historia que nunca debió empezar.")

st.markdown("¿Quieres escucharlo? Copia el texto aquí abajo:")

text = st.text_area("Ingresa el texto a escuchar.")

tld = 'com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English"))
if option_lang == "Español":
    lg = 'es'
if option_lang == "English":
    lg = 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
