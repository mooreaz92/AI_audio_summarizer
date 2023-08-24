import streamlit as st
import whisper
import tempfile
import os
from time import sleep
from stqdm import stqdm
from transformers import GPT2LMHeadModel, GPT2Tokenizer

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

# Load GPT-2 model and tokenizer

model_name = "gpt2-large" 
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

### Function Definitions

# Transcription function 
def transcribe_audio(audio_file_path):
    global transcription_in_progress, transcript_cached
    transcription_in_progress = True
    transcription = transcription_model.transcribe(audio_file_path, verbose=True)
    transcription_in_progress = False
    transcript_cached = True
    return transcription

# Function to generate a summary using GPT-2
def generate_summary(context, requirements, transcript_text):
    # Create a prompt for the GPT-2 model
    prompt = f"Context: {context}\nRequirements: {requirements}\nTranscription: {transcript_text}\nFufill the requirements stated"

    # Encode the prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt")

    # Generate a summary using the model
    summary_ids = model.generate(input_ids, max_length=100, num_return_sequences=1)

    # Decode the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

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
    st.subheader("AI Summarization")

    st.subheader("Transcript Status")

    # Show if a transcript has been loaded in the session state

    if st.session_state["transcript_text"] != '':
        st.success("Transcript loaded successfully")

    else:
        st.error("No transcript loaded")

    # Input fields for context, requirements, and transcript
    context = st.text_area("Context (e.g., 'This recording was a Dungeons and Dragons session'):")
    requirements = st.text_area("Requirements (e.g., 'Please print out the characters in the session as well as the key events'):")
    transcript_text = st.session_state["transcript_text"]

    # Button to generate summary
    if st.button("Generate Summary"):
        if context and requirements and transcript_text:
            summary = generate_summary(context, requirements, transcript_text)
            st.subheader("Generated Summary:")
            st.write(summary)
        else:
            st.warning("Please fill in all input fields before generating a summary.")
