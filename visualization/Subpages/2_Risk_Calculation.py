#####################################################################################
# 2_Risk_Calculation.py                                                             #
#                                                                                   #
# This is the streamlit page showing the risk calculation and SHAP values           #
#                                                                                   #
# - Calculate Heart Attack Risk                                                     #
# - Display SHAP Explanation                                                        #
#####################################################################################

# Import needed libraries
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import base64
import time
import matplotlib.pyplot as plt
import shap
from visualization.models.model_utils import load_preprocessor, load_model, calculate_risk, interpret_shap_values
from visualization.models.data_utils import generate_pdf
from io import BytesIO

#####################################################################################
### File preparation: Functions and Status checks and model import                ###
#####################################################################################

# Function to load and encode the image as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load the model and preprocessor
preprocessor = load_preprocessor("visualization/models/standardizer.pkl")

# Load the risk model but just provide the name, as the util will find out if it is pkl or h5
risk_model = load_model("visualization/models/risk_prediction_model")

# Get patient data form session
patient_data = st.session_state.get('patient_data', {})
data_available = bool(patient_data)

# Risk calculation state
if 'risk_calculated' not in st.session_state:
    st.session_state['risk_calculated'] = False


def calculate_SHAP():
    # Get the SHAP values and expected value from calculate_risk
    result, shap_values, expected_value, prediction = calculate_risk(preprocessor, risk_model)

    # Reshape the SHAP values if needed
    if len(shap_values.shape) == 3:
        shap_values_patient = shap_values.reshape(-1, shap_values.shape[1])
    else:
        shap_values_patient = shap_values

    st.session_state['shap_values_patient'] = shap_values_patient
    st.session_state['expected_value'] = expected_value

    # Display SHAP waterfall plot
    if shap_values is not None:
        feature_names = st.session_state['df'].columns.drop('Has_heart_disease')
        st.session_state['feature_names'] = feature_names

        fig, ax = plt.subplots()
        shap.waterfall_plot(shap.Explanation(
            values=shap_values_patient[0],
            base_values=expected_value,
            feature_names=feature_names
        ))

        # Save the SHAP waterfall plot as an image in memory (BytesIO)
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format='png')
        img_buffer.seek(0)  # Rewind the buffer to the beginning
        st.session_state['shap_image'] = img_buffer  # Save image in session state
        st.session_state['interpretation_text'] = interpret_shap_values(shap_values_patient, feature_names, prediction)

#####################################################################################
### Page Title and Doctor Infor                                                   ###
#####################################################################################

doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state.get('doctor_image_base64', '')

# Define if risk has been calculated and store in session state
if 'patient_data' not in st.session_state:
    st.session_state['patient_data'] = {}
    st.session_state['risk_explanation'] = ""

# Style settings for the patient pane
st.html(
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
    """
)

# Layout for doctor profile and patient title
with st.container():
    r1, r2 = st.columns([2, 1])
    with r1:
        r1.title("Patient Risk Calculation")
    with r2:
        st.html(
            f"""
            <div class="doctor-profile" style="display: flex; align-items: center; justify-content: flex-end;">
                <span class="notification-bell" title="Notifications" style="font-size: 15px; margin-right: 5px;">
                    🔔
                </span>
                <h4 style="margin: 0; font-size: 14px; margin-right: 10px;">{doctor_name}</h4>
                <img src="data:image/png;base64,{doctor_image_base64}" alt="Doctor Picture" style="width: 35px; height: auto;">
            </div>
            """
        )


#####################################################################################
### Expander with Information about the page                                      ###
#####################################################################################

with st.expander(label="Instruction", icon=":material/info:"):
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

#####################################################################################
### Show Patient Detail, Risk Light, Risk Description in Columns                  ###
#####################################################################################

# Three-column layout for patient info, risk calculation light, and result text
pat_info_col, light_column, explain_column = st.columns([1, 1, 2])

# Column 1: Patient details section
def display_patient_details():
    patient_info = patient_data.get("PatientInfo", {})
    image_path = patient_info.get("patient_photo_link", "visualization/assets/CardioVision.svg")
    image_base64 = get_image_as_base64(image_path)
    
    st.html(
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
        """
    )

with pat_info_col:
    display_patient_details()

# Column 2: Traffic light and button
with light_column:
    # Set initial image and text based on risk status
    image_path = "visualization/assets/light_out.svg"
    risk_text = "No Risk Calculated"
    text_color = "black"

    if st.session_state['risk_calculated']:
        result = st.session_state.get('risk_result', 'No Risk Calculated')
        if result == "Low Risk":
            image_path = "visualization/assets/light_green.svg"
            risk_text = "Low Risk"
            text_color = "green"
        elif result == "High Risk":
            image_path = "visualization/assets/light_red.svg"
            risk_text = "High Risk"
            text_color = "red"
    
    col_light_left, col_light_middle, col_light_right = st.columns([1, 2, 1])
    with col_light_middle:
        st.html(
            f"""
            <div style="display: flex; align-items: center; justify-content: center; margin: 30px 0 10px 0;">
                <img src="data:image/svg+xml;base64,{get_image_as_base64(image_path)}" alt="{risk_text} Traffic Light" width="110" style="padding: 10px;">
            </div>
            """
        )
        # Check if patient data exists
        if st.session_state['patient_data'] != {}:
            # Show the "Calculate Risk" button if the risk has not been calculated yet
            if not st.session_state.get('risk_calculated', False):
                if st.button("Calculate Risk", type="primary"):
                    if data_available:
                        with st.spinner("Calculating risk..."):
                            result, explanation, shap_values, prediction = calculate_risk(preprocessor, risk_model)
                            st.session_state['risk_calculated'] = True
                            st.session_state['risk_result'] = result
                            st.session_state['risk_explanation'] = explanation
                            st.session_state['shap_values'] = shap_values
                            calculate_SHAP()
                            st.rerun()  # Refresh the page after calculation

            # If risk is already calculated, show the download button
            else:
                if st.session_state['interpretation_text']:
                    st.download_button(
                        label="Download Risk Report",
                        file_name="risk_report.pdf",
                        mime="application/pdf",
                        data=generate_pdf(st.session_state['patient_data'], st.session_state['risk_result'], st.session_state['shap_image'], st.session_state['interpretation_text']),
                        type="primary"
                    )

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


#####################################################################################
### SHAP Values Diagram and Explanation                                           ###
#####################################################################################

st.subheader("Explanation of Results")

with st.expander("What are SHAP Values?", expanded=False):
    st.write(
        """
        **SHAP (SHapley Additive exPlanations)** values help explain how machine learning models make decisions for individual predictions. 
        Each feature's SHAP value represents its contribution to pushing the model's prediction toward either a positive or negative outcome.

        - **Red-colored features**: These features contributed to **increasing the risk** of a heart attack for this patient.
        - **Blue-colored features**: These features contributed to **decreasing the risk** of a heart attack.
        - The longer the bar, the **greater the influence** of that feature on the final prediction.

        In the SHAP waterfall plot, you can clearly see how each feature impacts the overall risk score for the patient, helping interpret the model's decision in a transparent way.
        """
    )

# Create two columns for SHAP plot and explanation
shap_col, explanation_col = st.columns([1.5, 2])

if st.session_state['risk_calculated']:
    # Get the SHAP values and expected value from calculate_risk
    result, shap_values, expected_value, prediction = calculate_risk(preprocessor, risk_model)

    # Reshape the SHAP values if needed
    if len(shap_values.shape) == 3:
        shap_values_patient = shap_values.reshape(-1, shap_values.shape[1])
    else:
        shap_values_patient = shap_values

    # Display SHAP waterfall plot
    if shap_values is not None:

        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display SHAP waterfall plot directly as matplotlib figure
            fig, ax = plt.subplots()
            shap.waterfall_plot(shap.Explanation(
                values=st.session_state['shap_values_patient'][0],
                base_values=st.session_state['expected_value'],
                feature_names=st.session_state['feature_names']
            ))
            st.pyplot(fig)

        with col2:
            # Show the interpretation text of the SHAP results
            st.markdown(st.session_state['interpretation_text'])
                
    else:
        st.write("SHAP values not available.")

# Add a small information text at the bottom
st.markdown("---")
st.markdown("If you want to learn more about the prediction model, data used, and quality of our predictions:")

# Use st.page_link to link to the Technical Information page
st.page_link("visualization/Subpages/6_Technical_Information.py", label="Open Technical Information Page", icon=":material/manufacturing:")