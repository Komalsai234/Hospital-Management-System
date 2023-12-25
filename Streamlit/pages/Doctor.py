from streamlit_extras.switch_page_button import switch_page
import base64
import streamlit as st

st.set_page_config(layout="wide")

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'doctor'

# Style setup with a gradient background, professional fonts, and padding for images
st.markdown(
    """
    <style>
    /* Set up a gradient background and use a web-safe font */
    .stApp {
    background-image: linear-gradient(to right top, #657DEB, #4C7BD9, #3280C7, #1A84B5, #0090A1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-attachment: fixed;
    background-size: cover;
    background-repeat: no-repeat;
    min-height: 100vh;
}

    /* Style for the main title */
    h1 {
        color: #ffffff;
        text-align: center;
        font-size: 60px;
        background: linear-gradient(to right, #FF5722, #FFC107);
        -webkit-background-clip: text;
        background-clip: text;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        margin-bottom: 0.5em;
    }

    /* Style for images to make them look like cards with added padding */
    .image-card {
        width: 250px;
        border-radius: 0.5em;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 2em 0.5em;
    }

    .image-card img {
        margin: 0;
        padding: 0;
    }

    
    /* Style for caption buttons */
    .stButton > button {
        color: white;
        font-size: 22px;
        font-weight: bold !important;
        
        background-color: #FF5722;
        border: none;
        border-radius: 0.5em;
        padding: 0.5em 1em;
        margin-top: 0.3em;
        margin-left: 2.0em;
        box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        transition: transform 0.3s, box-shadow 0.3s;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        color: white; /* Maintain text color on hover */
        background-color: #E64A19; /* Slightly darker shade on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1.5, 6, 1.3])
with col2:
    st.markdown("<h1 style='text-align: center;'>Welcome to Doctor Dashboard</h1>",
                unsafe_allow_html=True)

with col3:
    if st.button("Logout"):
        st.session_state['current_page'] = 'home'
        switch_page("app")


def img_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Function to display an image and a caption as a button


def image_with_caption_button(key, image_path, page_name):
    base64_image = img_to_base64(image_path)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{base64_image}" class="image-card">
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(key, key=page_name):
        st.session_state['current_page'] = page_name


# # Layout for clickable images with caption buttons
col1, spacer1, col2, spacer2, col3, spacer3, col4 = st.columns(
    [1, 0.2, 1, 0.2, 1, 0.2, 1])

with col1:
    image_with_caption_button(
        "PATIENT DETAILS", "icons/doctor_patient.png", "get_patient_details")

with col2:
    image_with_caption_button(
        "PATIENT REPORTS", "icons/doctor_reports.png", "get_patient_reports")

with col3:
    image_with_caption_button(
        "PATIENT PRESCRIPTION", "icons/doctor_prescription.png", "get_patient_prescription")

with col4:
    image_with_caption_button(
        "CHECK APPOINMNET", "icons/doctor_appointment.png", "get_doctor_appoinmnets")


if st.session_state['current_page'] == 'get_patient_details':
    switch_page("Doctor_Patient_Info")
elif st.session_state['current_page'] == 'get_patient_reports':
    switch_page("Doctor_Patient_Reports")
elif st.session_state['current_page'] == 'get_doctor_appoinmnets':
    switch_page("Check_Appointment")
elif st.session_state['current_page'] == 'get_patient_prescription':
    switch_page("Patient_Prescription")
# else:
#     ""
