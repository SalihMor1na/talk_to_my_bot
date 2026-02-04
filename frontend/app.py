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
        files = {"file": uploaded_file}
        response = requests.post(
            f"{BACKEND_URL}/uploadfile/",
            files=files
        )
        st.success("CV uploaded successfully!")
                               
                       

    
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
    
    
        st.write("---")
    
    
    if 'profile_data' in st.session_state:
        profile_info = st.session_state['profile_data']
        
        st.subheader("Basic Information")
        st.write(profile_info.get('answer', 'No data available'))
        
        st.write("---")
        st.subheader("Key Metrics")
        
        kpi1, kpi2, kpi3 = st.columns(3)
        
        with kpi1:
            st.metric(label="CV File", value=profile_info.get('filename', '--'))
        
        with kpi2:
            st.metric(label="Status", value="Loaded")
        
        with kpi3:
            st.metric(label="Source", value="RAG System")
    else:
        st.info("Click 'Load Profile' to view CV information")
    
elif page == "Chat":
    st.title("Chat with CV Bot")
    st.write("Ask questions about the uploaded CV")
    
   
    user_input = st.text_input(
        "Your question:",
        placeholder="e.g., What programming languages do you know?",
        key="chat_input"
    )
        
    col1, col2 = st.columns([1, 5])
    with col1:
        send_button = st.button("Send", use_container_width=True)
        
    st.write("---")
    st.subheader("Conversation")
    
    if send_button and user_input:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/rag/query",
                    json={"prompt": user_input}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("**Bot:**")
                    st.write(data.get('answer', 'No answer available'))
                else:
                    st.error(f"Failed: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")