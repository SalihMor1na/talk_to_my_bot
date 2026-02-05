import streamlit as st
import requests
import re

BACKEND_URL = "http://localhost:8000"

def parse_experience(text):
    
    match = re.search(r'1[.)]\s*(\d+)', text)
    if match:
        return match.group(1)
    return "--"

def parse_license(text):
    
    match = re.search(r'2[.)]\s*([A-E])', text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "--"

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
                    json={"prompt": "Analyze this CV and provide: 1) Total years of work experience (number only), 2) Driver's license type (letter only), 3) Brief summary of background and skills"}
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
        answer = profile_info.get('answer', '')
        
        years_exp = parse_experience(answer)
        license_type = parse_license(answer)
        
        st.subheader("Basic Information")
        st.write(answer if answer else 'No data available')
        
        st.write("---")
        st.subheader("Key Metrics")
        
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        
        with kpi1:
            st.metric(label="CV File", value=profile_info.get('filename', '--'))
        
        with kpi2:
            st.metric(label="Status", value="Loaded")
        
        with kpi3:
            st.metric(label="Source", value="RAG System")
        
        with kpi4:
            st.metric(label="Years Experience", value=years_exp)
        
        with kpi5:
            st.metric(label="Driver's License", value=license_type)
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