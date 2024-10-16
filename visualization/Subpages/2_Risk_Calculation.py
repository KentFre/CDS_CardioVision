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

col1, col2 = st.columns([1, 3])

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

with col1:
    display_patient_details()

@st.fragment
def right_column():
    # Define paths and placeholders
    image_path = "assets/light_out.svg"
    risk_text = "No Risk Calculated"
    text_color = "black"

    # Check if risk has been calculated and set the initial image path and risk text
    if st.session_state['risk_calculated']:
        result = st.session_state.get('risk_result', 'No Risk Calculated')
        explanation = st.session_state.get('risk_explanation', '')
        if result == "Low Risk":
            image_path = "assets/light_green.svg"
            risk_text = "Low Risk"
            text_color = "green"
        elif result == "High Risk":
            image_path = "assets/light_red.svg"
            risk_text = "High Risk"
            text_color = "red"
    
    # Display traffic light image and risk text
    risk_col1, risk_col2 = st.columns([1, 2])

    with risk_col1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-around;">
                <img src="data:image/svg+xml;base64,{get_image_as_base64(image_path)}" alt="{risk_text} Traffic Light" width="100">
            </div>
            """, unsafe_allow_html=True
        )

    with risk_col2:
        # Display status message
        if st.session_state['risk_calculated']:
            st.markdown(
                """
                <div style="padding: 10px; background-color: #d1ecf1; border: 1px solid #bee5eb; border-radius: 5px; margin-bottom: 15px;">
                    <p style="margin: 0; color: #0c5460;">ℹ️ A Heart Attack Risk Score has been recently calculated. You can recalculate if needed.</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; margin-bottom: 15px;">
                    <p style="margin: 0; color: #721c24;">⚠️ No Heart Attack Risk has been calculated.</p>
                </div>
                """, unsafe_allow_html=True
            )

        # Button to calculate the risk
        if st.button("Calculate Risk"):
            if data_available:
                with st.spinner("Calculating risk..."):
                    time.sleep(1)  # Simulate calculation delay
                    result, explanation = calculate_risk(preprocessor, risk_model)
                    st.session_state['risk_calculated'] = True
                    st.session_state['risk_result'] = result
                    st.session_state['risk_explanation'] = explanation

                    # Update image and text based on the calculated risk
                    if st.session_state['risk_result'] == "Low Risk":
                        image_path = "assets/light_green.svg"
                        risk_text = "Low Risk"
                        text_color = "green"
                    elif st.session_state['risk_result'] == "High Risk":
                        image_path = "assets/light_red.svg"
                        risk_text = "High Risk"
                        text_color = "red"
                
                st.rerun()

    # Display the explanation in full width underneath
    if st.session_state.get('risk_calculated', False):
        st.subheader("Explanation of Results")
        st.write(st.session_state['risk_result'])
        st.write(st.session_state['risk_explanation'])

# Run the right column fragment
with col2:
    right_column()