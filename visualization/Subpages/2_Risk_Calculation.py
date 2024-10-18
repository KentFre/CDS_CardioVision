import streamlit as st
import pandas as pd
import numpy as np
import base64
import time
from models.model_utils import load_preprocessor, load_model, calculate_risk  # Update this path based on your utils location

# Function to load and encode the image as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the model and preprocessor
preprocessor = load_preprocessor("../visualization/models/standardizer.pkl")
risk_model = load_model("../visualization/models/risk_prediction_model.pkl")

doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state.get('doctor_image_base64', '')

# Define if risk has been calculated and store in session state
if 'patient_data' not in st.session_state:
    st.session_state['patient_data'] = {}
    st.session_state['risk_explanation'] = ""

patient_data = st.session_state.get('patient_data', {})
data_available = bool(patient_data)

# Risk calculation state
if 'risk_calculated' not in st.session_state:
    st.session_state['risk_calculated'] = False

# Style settings for the patient pane
st.markdown(
    """
    <style>
    .pane-container {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        line-height: 1.2;
    }
    .patient-details img {
        width: 80px;
        height: auto;
        border-radius: 50%;
        margin-right: 10px;
    }
    .patient-details h2 {
        color: #333;
        font-size: 24px;
        font-weight: bold;
    }
    .patient-details p {
        color: #555;
        font-size: 14px;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True
)

# Layout for doctor profile and patient title
with st.container():
    r1, r2 = st.columns([2, 1])
    with r1:
        r1.title("Patient Risk Calculation")
    with r2:
        st.markdown(
            f"""
            <div class="doctor-profile" style="display: flex; align-items: center; justify-content: flex-end;">
                <span class="notification-bell" title="Notifications" style="font-size: 15px; margin-right: 5px;">
                    🔔
                </span>
                <h4 style="margin: 0; font-size: 14px; margin-right: 0px;">{doctor_name}</h4>
                <img src="data:image/png;base64,{doctor_image_base64}" alt="Doctor Picture" style="width: 35px; height: auto;">
            </div>
            """, unsafe_allow_html=True
        )

with st.expander(label="🛈 Instruction"):
    st.write(
        """
        This page allows you to calculate the heart attack risk score for a patient and view an explanation of the contributing factors.

        ### Risk Calculation
        1. **Upload Patient Data**: First, upload a JSON file with the patient's medical information, which includes vital signs, lab results, and any relevant symptoms. [This will be automatically performed by the EHR in the final implementation.]
        2. **Calculate Risk**: Click on the "Calculate Risk" button to analyze the patient’s data. The system will generate a risk score:
           - A **Green Light** indicates a **Low Risk**.
           - A **Red Light** indicates a **High Risk**.
        3. **Review Results**: The calculated risk level will be displayed along with a brief message summarizing the outcome.

        ### SHAP Evaluation
        After calculating the risk, the SHAP evaluation will provide an explanation of the factors that contributed to the patient's risk level:
        - This analysis helps clarify how each feature (such as age, cholesterol level, or heart rate) influenced the risk score.
        - Understanding these factors can support informed decision-making and personalized patient care.
        
        **Note**: You may re-upload or update patient data at any time to reassess the risk or view different results.
        """
    )

# Three-column layout for patient info, risk calculation light, and result text
pat_info_col, light_column, explain_column = st.columns([1, 1, 2])

# Column 1: Patient details section
def display_patient_details():
    patient_info = patient_data.get("PatientInfo", {})
    image_path = patient_info.get("patient_photo_link", "assets/CardioVision.svg")
    image_base64 = get_image_as_base64(image_path)
    
    st.markdown(
        f"""
        <div class="pane-container">
            <div class="patient-details">
                <img src="data:image/svg+xml;base64,{image_base64}" alt="Patient Picture" style="width:100px;height:auto;">
                <h2>{patient_info.get('name', 'N/A')}</h2>
                <p><b>ID:</b> {patient_info.get('patient_id', 'N/A')}</p>
                <p><b>Age:</b> {patient_info.get('age', 'N/A')}</p>
                <p><b>Gender:</b> {patient_info.get('gender', 'N/A')}</p>
                <p><b>Address:</b> {patient_info.get('address', 'N/A')}</p>
                <p><b>Phone:</b> {patient_info.get('phone', 'N/A')}</p>
                <p><b>Email:</b> {patient_info.get('email', 'N/A')}</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

with pat_info_col:
    display_patient_details()

# Column 2: Traffic light and button
with light_column:
    # Set initial image and text based on risk status
    image_path = "assets/light_out.svg"
    risk_text = "No Risk Calculated"
    text_color = "black"

    if st.session_state['risk_calculated']:
        result = st.session_state.get('risk_result', 'No Risk Calculated')
        if result == "Low Risk":
            image_path = "assets/light_green.svg"
            risk_text = "Low Risk"
            text_color = "green"
        elif result == "High Risk":
            image_path = "assets/light_red.svg"
            risk_text = "High Risk"
            text_color = "red"
    
    col_light_left, col_light_middle, col_light_right = st.columns([1, 2, 1])
    with col_light_middle:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: center; margin: 30px 0 10px 0;">
                <img src="data:image/svg+xml;base64,{get_image_as_base64(image_path)}" alt="{risk_text} Traffic Light" width="110" style="padding: 10px;">
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.session_state['patient_data'] != {}:
            if st.button("Calculate Risk", type="primary"):
                if data_available:
                    with st.spinner("Calculating risk..."):
                        time.sleep(1)  # Simulate calculation delay
                        result, explanation = calculate_risk(preprocessor, risk_model)
                        st.session_state['risk_calculated'] = True
                        st.session_state['risk_result'] = result
                        st.session_state['risk_explanation'] = explanation
                        st.rerun()  # Refresh the app with updated session state

# Column 3: Risk calculation result text
with explain_column:
    st.subheader("Risk Calculation Result")
    
    # Display risk result with either success or error formatting
    patient_name = patient_data.get('PatientInfo', {}).get('name', 'the patient')
    risk_result = st.session_state.get('risk_result', 'No Risk Calculated')
    if not st.session_state['patient_data'] == {}:
        if not st.session_state['risk_calculated']:
            st.error("⚠️ No Heart Attack Risk has been calculated.")
        else:
            if risk_result == "High Risk":
                st.error(f"A heart attack risk score has been calculated based on the provided patient information. {patient_name} has a **High Risk** of experiencing a heart attack.")
            elif risk_result == "Low Risk":
                st.success(f"A heart attack risk score has been calculated based on the provided patient information. {patient_name} has a **Low Risk** of experiencing a heart attack.")
    else:
        st.error("⚠️ No Patient Data uploaded. Reload Patient data from EHR or enter manually!")

# Full-width section below the columns for SHAP explanation
st.subheader("Explanation of Results")
st.write(st.session_state['risk_explanation'])