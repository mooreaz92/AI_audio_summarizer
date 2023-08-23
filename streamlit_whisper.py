import streamlit as st
import whisper
import tempfile
import os

### Formatting

# Create title and sidebar for navigation
st.title("AI Auto Summarization")
st.sidebar.title("Navigation")
selected_section = st.sidebar.radio("Workflow", ["Transcription", "Summarize"])

### Variables and Model Loading

# Global variables

saved_text_transcription = None

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
    transcription = transcription_model.transcribe(audio_file_path)
    transcription_in_progress = False
    transcript_cached = True
    return transcription

### Transcription Section

if selected_section == "Transcription":
    st.subheader("Transcription")
    
    # Button to upload audio file
    audio_file = st.file_uploader("Upload audio file for transcription", type=["mp3", "wav", "m4a"])

    # Processing the audio file and creating a temporary file path for transcribing
    @st.cache_data
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

    if audio_file and transcript_cached == False:
        pseudo_file_path = process_audio_file(audio_file)
        st.success(f"File processed successfully. Please press 'Transcribe Audio' to begin transcription.")

    # Button to transcribe audio file
    if audio_file is not None and not transcription_in_progress:
        if st.button("Transcribe Audio"):
            cached_transcript = transcribe_audio(pseudo_file_path)
            st.success("Transcription Complete")
            transcript_cached = True

    # Display a truncated version of the transcript only when the transcribe button has been pressed

    if transcript_cached:
        st.subheader("Transcription Sample")
        st.write(cached_transcript["text"][:1000])

    # Making a button that clears the audio file and stores the transcript

    @st.cache_data
    def clear_audio():
        temp_file = None
        temp_file_path = None

    def store_transcript():
        global cached_transcript
        return cached_transcript['text']

    if audio_file is not None and transcript_cached == True:
        if st.button("Clear Audio and Save Transcript"):
            clear_audio()
            st.success("Audio file cleared and transcript saved")


### Summarization Section

if selected_section == "Summarize":
    st.text(cached_transcript)