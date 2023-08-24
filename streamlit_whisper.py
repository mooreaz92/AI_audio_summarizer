import streamlit as st
import whisper
import tempfile
import os
from time import sleep
from stqdm import stqdm

### Formatting

# Create title and sidebar for navigation
st.title("AI Audio File Summarizer")
st.sidebar.title("Navigation")
selected_section = st.sidebar.radio("Workflow", ["Transcription", "AI Summarization"])

### Variables and Model Loading

# Session state variables

if "transcript_text" not in st.session_state:
    st.session_state["transcript_text"] = ''

# Transcription model and variables
transcription_model = whisper.load_model("base")

transcription_in_progress = False
transcript_cached = False
transcript_saved = False

### Function Definitions

# Transcription function 
def transcribe_audio(audio_file_path):
    global transcription_in_progress, transcript_cached
    transcription_in_progress = True
    transcription = transcription_model.transcribe(audio_file_path, verbose=True)
    transcription_in_progress = False
    transcript_cached = True
    return transcription

### Transcription Section

if selected_section == "Transcription":
    st.subheader("Transcription")
    
    # Button to upload audio file
    audio_file = st.file_uploader("Upload audio file for transcription", type=["mp3", "wav", "m4a"])

    # Processing the audio file and creating a temporary file path for transcribing
    def process_audio_file(audio_file):
        if audio_file is not None:
            # Create a temporary directory to store the file
            temp_dir = tempfile.mkdtemp()
            
            # Create a temporary file
            temp_file_path = os.path.join(temp_dir, audio_file.name)
            
            # Write the uploaded data to the temporary file
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(audio_file.read())
            
            return temp_file_path

    if audio_file is not None and transcript_cached is not None:
        pseudo_file_path = process_audio_file(audio_file)

    # Button to transcribe audio file and display a progress bar
    if audio_file is not None and not transcription_in_progress:
        if st.button("Transcribe Audio"):
            with st.spinner(text = "Transcribing audio..."):
                transcript_cached = transcribe_audio(pseudo_file_path)
                st.session_state["transcript_text"] = transcript_cached["text"]
                st.success("Transcription Complete")

    # Display a truncated version of the transcript only when the transcribe button has been pressed

    if transcript_cached:
        st.subheader("Transcription Sample")
        st.write(transcript_cached["text"][:500])

### Summarization Section

if selected_section == "AI Summarization":
    st.subheader("Transcript Status")

    # Show if a transcript has been loaded in the session state

    if st.session_state["transcript_text"] != '':
        st.success("Transcript loaded successfully")

    else:
        st.error("No transcript loaded")

   # Load the LLM  