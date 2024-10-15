import streamlit as st
from streamlit_lottie import st_lottie
import json
import time
import base64

# Function to load and encode the image as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Check if the image is already encoded and stored in session state
if 'doctor_image_base64' not in st.session_state:
    doctor_image_path = "assets/stone_profile_picture.png"
    st.session_state['doctor_image_base64'] = get_image_as_base64(doctor_image_path)

if 'patient_image_base64' not in st.session_state:
    patient_image_path = "assets/Patient.svg"
    st.session_state['patient_image_base64'] = get_image_as_base64(patient_image_path)

# Set the page configuration
st.set_page_config(
    page_title="CardioVision",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="assets/CardioVision_icon.png",
)

# Load your Lottie JSON file
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

if 'lottie' not in st.session_state:
    st.session_state.lottie = False

if not st.session_state.lottie:
    lottfinder = load_lottie_file("assets/CardioVision_Loader_H.json")
    st_lottie(lottfinder, speed=1, loop=True)
    time.sleep(2)
    st.session_state.lottie = True
    st.rerun()

# Define the dialog for legal text/verification
@st.dialog("Patient Data Verification", width="large")
def legal_verification():
    # Scrollable content styling with inline CSS
    scrollable_content_style = """
        <style>
        .scrollable-modal-content {
            max-height: 150px; /* Adjust the max height as needed */
            overflow-y: auto;
            padding-right: 15px;
        }
        </style>
        <div class="scrollable-modal-content">
    """
    st.markdown(scrollable_content_style, unsafe_allow_html=True)
    
    # Modal content with the applied scrollable class
    st.markdown(
        '**IMPORTANT NOTICE**: By proceeding, you affirm that the patient data entered is accurate and that you understand the following:'
    )
    st.markdown(' ')
    st.markdown(
        '<strong>Accuracy of Data</strong>: It is your responsibility to ensure the patient data entered into this system is accurate and up-to-date. The reliability of the prediction depends heavily on the quality of the data provided.',
        unsafe_allow_html=True
    )
    st.markdown(
        '<strong>Non-Medical Product</strong>: This prediction tool is not a certified medical product. It is designed for informational and educational purposes only. It should not be used as a sole basis for medical decision-making. Any clinical decisions should be based on professional judgment and verified through other medical resources.',
        unsafe_allow_html=True
    )
    st.markdown(
        '<strong>User Responsibility</strong>: You agree to use this tool responsibly and acknowledge that it is not a substitute for professional medical advice. The developers of this tool disclaim any liability for its usage outside of its intended purpose.',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Confirmation button
    if st.button("I Understand and Confirm"):
        st.session_state.popup_closed = True
        st.rerun()

# Only show the modal if it hasn't been closed
if 'popup_closed' not in st.session_state:
    st.session_state.popup_closed = False

# Show the dialog function if the popup hasn't been closed
if not st.session_state.popup_closed:
    legal_verification()

# Workaround to set the logo size using st.html
st.markdown(
    """
    <style>
        [alt="Logo"] {
            height: 3rem; /* Adjust this value as needed */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display your logo at the top
st.logo(
    "assets/CardioVision_Full_Logo.svg"
)

# Define pages
patient_data_page = st.Page("Subpages/1_Patient_Data.py", title="Patient Data", icon=":material/personal_injury:", default=True)
risk_assessment_page = st.Page("Subpages/2_Risk_Calculation.py", title="Risk Calculation", icon=":material/recent_patient:")
descriptive_analytics_page = st.Page("Subpages/3_Descriptive_Analytics.py", title="Descriptive Analytics", icon=":material/monitor_heart:")
diagnostic_analytics_page = st.Page("Subpages/4_Diagnostic_Analytics.py", title="Diagnostic Analytics", icon=":material/quick_reference_all:")
about_page = st.Page("Subpages/5_About.py", title="About", icon=":material/help:")

pg = st.navigation(
    {
        "Patient": [patient_data_page, risk_assessment_page],
        "Department Insights": [descriptive_analytics_page, diagnostic_analytics_page],
        "Others": [about_page],
    }
)
# Run the navigation pages
pg.run()
