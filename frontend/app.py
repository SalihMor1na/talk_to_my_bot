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
    """Parse licenses including ranges like A1-4, B1-4, D1"""
    licenses = []

    if re.search(r'\bB\b.*?(?:driver|körkort)', text, re.IGNORECASE):
        licenses.append('B')

    range_matches = re.findall(
        r'\b([ABCD])(\d)[-–](\d)\b',
        text,
        re.IGNORECASE
    )
    
    for letter, start, end in range_matches:
        letter = letter.upper()
        for num in range(int(start), int(end) + 1):
            licenses.append(f"{letter}{num}")

    individual_matches = re.findall(
        r'\b([ABCD])(\d)\b',
        text,
        re.IGNORECASE
    )
    
    for letter, num in individual_matches:
        licenses.append(f"{letter.upper()}{num}")

    return sorted(set(licenses)) if licenses else ["--"]

def format_licenses_readable(licenses):
    if not licenses or licenses == ["--"]:
        return "--"

    output = []

    if "B" in licenses:
        output.append("B Driver's License")

    truck_groups = {
        "A": [],
        "B": [],
        "D": []
    }

    for lic in licenses:
        if len(lic) == 2 and lic[0] in truck_groups:
            truck_groups[lic[0]].append(int(lic[1]))

    for group in ["A", "B", "D"]:
        numbers = truck_groups[group]
        if numbers:
            numbers = sorted(set(numbers))
            if len(numbers) > 1:
                output.append(f"Forklift Certificate {group}{numbers[0]}-{numbers[-1]}")
            else:
                output.append(f"Forklift Certificate {group}{numbers[0]}")

    return ", ".join(output)

def extract_summary_text(text):
    """Extract only the professional summary (item 3) from the response"""
    match = re.search(r'3[.)]\s*(.+?)(?:\n|$)', text, re.DOTALL)
    if match:
        summary = match.group(1).strip()
        summary = re.sub(r'\n\d+[.)]\s*.+', '', summary).strip()
        return summary
    
    return text

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
                    json={
                        "prompt": (
                            "Analyze this CV and provide in english only:\n"
                            "1) Total years of work experience (number only)\n"
                            "2) ALL licenses and certificates the person has "
                            "(e.g. B driver's license, truck license A1–A4, B1, D1, etc.)\n"
                            "3) Brief professional summary of all my work including name and age first"
                        )
                    }
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
        licenses = parse_license(answer)
        licenses_display = format_licenses_readable(licenses)
        summary_text = extract_summary_text(answer)

        st.subheader("Short Summary")
        st.write(summary_text if summary_text else 'No data available')
        
        st.write("---")
        st.subheader("Key Metrics")
        
        kpi1, kpi2 = st.columns(2)
        
        with kpi1:
              st.metric(
                label="Years of Work Experience", 
                value=f"{years_exp} Years" if years_exp != "--" else "--"
            )
        
        with kpi2:
            st.markdown("**Licenses & Certificates**")
            st.markdown(
                f"<div style='font-size: 1.5rem; font-weight: 600;'>{licenses_display}</div>", 
                unsafe_allow_html=True
            )
    else:
        st.info("Click 'Load Profile' to view CV information")
    
elif page == "Chat":
    st.title("Chat with CV Bot")
    st.write("Ask questions about the uploaded CV")
    
   
    user_input = st.text_input(
        "Your question:",
        placeholder="e.g., What work experience do you have?",
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