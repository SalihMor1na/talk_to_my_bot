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
    st.write("Upload your CV to get started")
    
elif page == "Profile":
    st.title("Profile")
    st.write("View your CV summary")
    
elif page == "Chat":
    st.title("Chat with CV Bot")
    st.write("Ask questions about the CV")