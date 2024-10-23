import streamlit as st
from streamlit_lottie import st_lottie
import json
import time
import base64
import pandas as pd

# Function to load and encode the image as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Load data and store in cache
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('data/02_processed_data/complete_case_machine_learning_data.csv')
        raw_data = pd.read_csv('data/02_processed_data/complete_case_data.csv')
        return data, raw_data
    except FileNotFoundError:
        st.error("Error loading dataset. Please check the file path.")
        return pd.DataFrame(), pd.DataFrame()

# Check if the image is already encoded and stored in session state
if 'doctor_image_base64' not in st.session_state:
    doctor_image_path = "visualization/assets/stone_profile_picture.png"
    st.session_state['doctor_image_base64'] = get_image_as_base64(doctor_image_path)

if 'patient_image_base64' not in st.session_state:
    patient_image_path = "visualization/assets/Patient.svg"
    st.session_state['patient_image_base64'] = get_image_as_base64(patient_image_path)

# Set the page configuration
st.set_page_config(
    page_title="CardioVision",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="visualization/assets/CardioVision_icon.png",
)

# Load your Lottie JSON file
def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

if 'lottie' not in st.session_state:
    st.session_state.lottie = False


if not st.session_state.lottie:
    lottfinder = load_lottie_file("visualization/assets/CardioVision_Loader_H.json")
    st_lottie(lottfinder, speed=1, loop=True)

    print("Loading data")
    # Load the dataset and store it in session state
    df, raw_df = load_data()
    st.session_state['df'] = df
    st.session_state['raw_df'] = raw_df

    # Continue with lottie for the effect    
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
        '**IMPORTANT NOTICE**: By proceeding, you affirm that you meet the following conditions:'
    )
    st.markdown(' ')

    # 1) Trained medical professional
    st.markdown(
        '<strong>Trained Medical Professional</strong>: You confirm that you are a trained medical professional with the expertise to interpret and use CardioVision correctly. ',
        unsafe_allow_html=True
    )

    # 2) Target patient groups
    st.markdown(
        '<strong>Target Patient Groups</strong>: CardioVision is intended only for use on cardiology patients who have accurate, complete data and show no signs of acute myocardial infarction.',
        unsafe_allow_html=True
    )

    # 3) Patient data accuracy
    st.markdown(
        '<strong>Data Accuracy</strong>: You agree to verify the accuracy of the patient data entered, as the predictions rely on correct input.',
        unsafe_allow_html=True
    )

    # 4) Non-medical product
    st.markdown(
        '<strong>Non-Medical Product</strong>: This tool is for educational purposes only and is not a certified medical device. It should not be solely relied upon for clinical decisions.',
        unsafe_allow_html=True
    )

    # 5) Final decision responsibility
    st.markdown(
        '<strong>Final Decision</strong>: As the healthcare provider, you are fully responsible for all clinical decisions. CardioVision serves as a decision aid, not a substitute.',
        unsafe_allow_html=True
    )

    # 6) University project disclaimer
    st.markdown(
        '<strong>University Project</strong>: This tool is part of a university project and should not be used for real-world patient care.',
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
    "visualization/assets/CardioVision_Full_Logo.svg"
)

# Define pages
patient_data_page = st.Page("visualization/Subpages/1_Patient_Data.py", title="Patient Data", icon=":material/personal_injury:", default=True)
risk_assessment_page = st.Page("visualization/Subpages/2_Risk_Calculation.py", title="Risk Calculation", icon=":material/recent_patient:")
descriptive_analytics_page = st.Page("visualization/Subpages/3_Descriptive_Analytics.py", title="Descriptive Analytics", icon=":material/monitor_heart:")
diagnostic_analytics_page = st.Page("visualization/Subpages/4_Diagnostic_Analytics.py", title="Diagnostic Analytics", icon=":material/quick_reference_all:")
about_page = st.Page("visualization/Subpages/5_About.py", title="About", icon=":material/help:")
technical_information_page = st.Page("visualization/Subpages/6_Technical_Information.py", title="Technical Information", icon=":material/manufacturing:")
pg = st.navigation(
    {
        "Patient": [patient_data_page, risk_assessment_page],
        "Department Insights": [descriptive_analytics_page, diagnostic_analytics_page],
        "Others": [technical_information_page, about_page],
    }
)
# Run the navigation pages
pg.run()
