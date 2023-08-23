import streamlit as st
import whisper

### Formatting

# Create title and sidebar for navigation
st.title("AI Auto Summarization")
st.sidebar.title("Navigation")
selected_section = st.sidebar.radio("Workflow", ["Transcription", "Summarize"])

### Variables and Model Loading

# Transcription model and variables
transcription_model = whisper.load_model("base")

transcription_text = ""
transcription_in_progress = False
transcript_uploaded = False

# Summarization model and variables

summarization_in_progress = False

### Function Definitions

# Transcription function 
def transcribe_audio(audio_file_path):
    global transcription_in_progress, transcript_uploaded
    transcription_in_progress = True
    transcription = transcription_model.transcribe(audio_file_path)
    transcription_in_progress = False
    transcript_uploaded = True
    return transcription

# Summarization function
def summarize_transcription(transcription_text):
    global summarization_in_progress
    summarization_in_progress = True
    summarized_text = "This is a summary of the transcription.\nIt can be quite long."
    summarization_in_progress = False
    return summarized_text

### Transcription Section

if selected_section == "Transcription":
    st.subheader("Transcription")
    
    # Button to upload audio file
    audio_file = st.file_uploader("Upload audio file for transcription", type=["mp3", "wav", "m4a"])

    # Button to transcribe audio file
    if audio_file is not None and not transcription_in_progress:
        if st.button("Transcribe Audio"):
            cached_transcript = transcribe_audio(audio_file.name)
            st.success("Transcription Complete")
            transcript_uploaded = True

    # Display a truncated version of the transcript only when the transcribe button has been pressed

    if transcript_uploaded:
        st.subheader("Transcription Sample")
        st.write(cached_transcript["text"][:1000])

### Summarization Section


# Summarize section
if selected_section == "Summarize":
    st.subheader("Summarize")
    if st.button("Summarize Transcription") and not summarization_in_progress:
        summarization_text = simulate_summarization(transcription_text)
        st.subheader("Summarized Text")
        st.write(summarization_text)

