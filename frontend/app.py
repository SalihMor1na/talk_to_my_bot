import streamlit as st
import requests


BACKEND_URL = "http://localhost:8000"


st.set_page_config(
    page_title="CV Chatbot",
    layout="wide"
)


st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Upload CV", "Profile", "Chat"])


if page == "Upload CV":
    st.title("Upload CV")
    st.write("Upload a CV (PDF or DOCX) to get started")
    

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help="Upload a CV in PDF or DOCX format"
    )
    
    
    if uploaded_file is not None:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.write(f"File size: {uploaded_file.size} bytes")
        st.write(f"File type: {uploaded_file.type}")
         
        if st.button("Upload to Backend"):
            st.info("Will send to backend in next step...")
    
elif page == "Profile":
    st.title("Profile")
    st.write("View your CV summary")
    
elif page == "Chat":
    st.title("Chat with CV Bot")
    st.write("Ask questions about the CV")