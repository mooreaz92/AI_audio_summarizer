import streamlit as st
from streamlit.server.server import Server

def get_session_id():
    # This function generates a unique session ID for the current session.
    session_id = id(Server.get_current()._session_info.session)
    return session_id

# Function to initialize SessionState
def init_session_state():
    session_id = get_session_id()
    if not hasattr(st, 'session_state'):
        st.session_state[session_id] = {}

init_session_state()

# File Upload
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])

# Store the uploaded file in the session_state
if uploaded_file is not None:
    session_id = get_session_id()
    st.session_state[session_id]['file'] = uploaded_file
    st.write("File uploaded successfully!")

# Access the uploaded file in your transcriber function
session_id = get_session_id()
if 'file' in st.session_state[session_id]:
    uploaded_file = st.session_state[session_id]['file']
    # Now you can pass `uploaded_file` to your transcriber function
