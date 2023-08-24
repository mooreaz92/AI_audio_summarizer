import streamlit as st
import whisper
import tempfile
import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from secret_api_key import API_KEY

os.environ['OPENAI_API_KEY'] = API_KEY

# Create title and sidebar for navigation
st.title("AI Audio File Summarizer")
st.sidebar.title("Navigation")
selected_section = st.sidebar.radio("Workflow", ["Transcription", "AI Summarizer"])

# Session state variables
if "transcript_text" not in st.session_state:
    st.session_state["transcript_text"] = ''

# Transcription model and variables
transcription_model = whisper.load_model("base")
transcription_in_progress = False
transcript_cached = False
transcript_saved = False

# Function to handle audio file processing
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

# Function for transcription
def transcribe_audio(audio_file_path):
    global transcription_in_progress, transcript_cached
    transcription_in_progress = True
    transcription = transcription_model.transcribe(audio_file_path, verbose=True)
    transcription_in_progress = False
    transcript_cached = True
    return transcription

# Function to call the OpenAI API with a prompt

llm = OpenAI(temperature=0.9)

# Transcription Section
if selected_section == "Transcription":
    st.subheader("Transcription")
    
    # Button to upload audio file
    audio_file = st.file_uploader("Upload audio file for transcription", type=["mp3", "wav", "m4a"])

    # Button to transcribe audio file and display a progress bar
    if audio_file is not None and not transcription_in_progress:
        if st.button("Transcribe Audio"):
            with st.spinner(text="Transcribing audio..."):
                pseudo_file_path = process_audio_file(audio_file)
                transcript_cached = transcribe_audio(pseudo_file_path)
                st.session_state["transcript_text"] = transcript_cached["text"]
                st.success("Transcription Complete")

    # Display a truncated version of the transcript only when the transcribe button has been pressed
    if transcript_cached:
        st.subheader("Transcription Sample")
        st.write(transcript_cached["text"][:500])

# Summarization Section
if selected_section == "AI Summarizer":
    st.subheader("AI Summarizer")
    st.subheader("Transcript Status")

    # Show if a transcript has been loaded in the session state
    if st.session_state["transcript_text"]:
        st.success("Transcript loaded successfully")
    else:
        st.error("No transcript loaded")

    # Input fields for context, requirements, and transcript
    context = st.text_area("Context (e.g., 'This recording was a quick call between friends'):")
    requirements = st.text_area("Requirements (e.g., 'Give me a summary of the action items from this call'):")
    transcript_text = st.session_state["transcript_text"]


    # Check if all required inputs are provided show a button to submit to the OpenAI API. Then use a LangChain PromptTemplate and LLMChain to generate a summary

    if context and requirements and transcript_text:
        if st.button("Submit to OpenAI"):
            with st.spinner(text="Generating summary..."):
                prompt_template = PromptTemplate(
                    input_variables = ['context', 'requirements', 'transcript_text'],
                    template= """
                    Act like a personal assistant who is transcribing an audio file. 
                    The user has provided the following: {context} and defined the following requirements: {requirements} 
                    The transcript is found here: {transcript_text}
                    """
                )
                llm_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True, output_key='summary')
                summary = llm_chain.run(context=context, requirements=requirements, transcript_text=transcript_text)
                st.success("Summary generated successfully")
                st.subheader("Summary")
                st.write(summary)