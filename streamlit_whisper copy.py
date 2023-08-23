### Importing Libraries

import streamlit as st
import whisper

### Setting up title

st.title("Whisper App")

### Adding a subheader for 'Transcription', loading model, and prompting user to upload a file

st.subheader("Transcription")
model = whisper.load_model("base")
st.text("Transcription Model Loaded!")
audio_file = st.file_uploader("Upload audio file for transcription", type=["mp3", "wav", "m4a"])


### Transcription - Aaking the button

if st.button("Transcribe Audio"):
    if audio_file is not None:
        st.success("Transcribing Audio")
        transcription = model.transcribe(audio_file.name)
        st.success("Transcription Complete")
        
    else:
        st.error("Please Upload Audio File")

