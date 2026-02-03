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
            with st.spinner("Uploading..."):
                try:
                    files = {"file": uploaded_file}
                    response = requests.post(
                        f"{BACKEND_URL}/uploadfile/",
                        files=files
                    )
                    
                    if response.status_code == 200:
                        st.success("CV uploaded successfully!")
                    else:
                        st.error(f"Upload failed: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
elif page == "Profile":
    st.title("Profile Summary")
    
    
    if st.button("Load Profile"):
        with st.spinner("Loading profile..."):
            try:
                
                response = requests.post(
                    f"{BACKEND_URL}/rag/query",
                    json={"prompt": "Give me a brief summary of this person's background, including name, contact info, and key skills"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state['profile_data'] = data
                    st.success("Profile loaded!")
                else:
                    st.error(f"Failed to load profile: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    
    st.divider()
    
   
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Name:**")
        st.write("**Email:**")
        st.write("**Phone:**")
    
    with col2:
        st.write("Data will load here")
        st.write("Data will load here")
        st.write("Data will load here")
    
    
    st.divider()
    st.subheader("Key Metrics")
    
    
    kpi1, kpi2, kpi3 = st.columns(3)
    
    with kpi1:
        st.metric(label="Years of Experience", value="--")
    
    with kpi2:
        st.metric(label="Skills", value="--")
    
    with kpi3:
        st.metric(label="Education Level", value="--")
    
elif page == "Chat":
    st.title("Chat with CV Bot")
    st.write("Ask questions about the CV")