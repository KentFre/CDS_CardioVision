import streamlit as st
import pandas as pd
import numpy as np
import base64
import json
from datetime import datetime, timedelta
import time
import plotly.express as px


# Function to load and encode the image as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Define if risk has been calculated and store in session state
if 'risk_calculated' not in st.session_state:
    st.session_state['risk_calculated'] = False

# Thresholds for the patient data
thresholds = {
    "resting_heart_rate": (60, 100),
    "max_heart_rate": (60, 170),
    "serum_cholesterol": (120, 240),
}

# Function to determine text color based on value and thresholds
def get_color(value, range):
    min_val, max_val = range
    if value < min_val or value > max_val:
        return "red"
    return "black"

# Check boolean and other conditions for additional fields
def get_condition_color(value, condition=True):
    return "red" if value == condition else "black"

# Load the doctor profile image from session state
doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state.get('doctor_image_base64', '')

# CSS styling for patient pane
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
        line-height: 1.2; /* Reduced line spacing */
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

    .metric-pane p {
        font-size: 16px;
    }
    </style>
    """
)

with st.expander("❗Medical Problem and End Users"):
    col1, col2 = st.columns(2)

    # Left column for Identified Medical Problem
    with col1:
        st.markdown("""
        ### **Identified Medical Problem**
        Heart attacks are a major cause of death in Sweden and many parts of the world. 
        In 2022, Sweden alone reported over 23,000 cases of AMI. Early detection and prevention of heart attack risk can save lives and reduce healthcare costs.
        CardioVision applies AI and machine learning to improve heart attack risk prediction, helping healthcare providers make more timely and informed decisions for patient care.
        """)          

    # Right column for End Users
    with col2:
        st.markdown("""
        ### **End Users**
        CardioVision is designed for clinicians focusing on predicting heart attack risk in patients who do not show signs of an acute heart attack on ECG or through elevated troponin levels. 
        It helps clinicians identify high-risk patients by analyzing factors such as age, cholesterol, and blood pressure, and assists in reducing risk through early prevention strategies.
        """)

    # References in two columns
    st.markdown("### **References**")
    ref_col1, ref_col2 = st.columns(2)

    # Left column for two references
    with ref_col1:
        st.markdown("""
        - World Health Organization. Cardiovascular diseases (CVDs). *WHO*, 2021.
        - National Board of Health and Welfare. Statistics on Myocardial Infarctions 2022. *Socialstyrelsen*, 2023.
        """)

    # Right column for two references
    with ref_col2:
        st.markdown("""
        - Oude Wolcherink MJ et al. Early Detection of Cardiovascular Disease: *PharmacoEconomics*, 2023.
        - Rojek I et al. AI-Based Heart Attack Risk Prediction: *Electronics*, 2024.
        """)

# Display doctor profile
with st.container():
    r1, r2 = st.columns([2, 1])

    with r1:
        r1.title("Patient Data Overview")

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


# Instructions expander
with st.expander("Instruction", icon=":material/info:"):
    st.write(
        """
        **Welcome to the Patient Data Analysis and Risk Prediction Page**
        
        Here you can simulate the process of Electronic Health Record (EHR) data transfer for a patient by uploading a JSON file. 
        Once uploaded, you can verify the patient data, which includes essential details like personal information, core complaints, and patient parameters. 
        Additionally, this section provides insight into various health metrics and ECG results that are crucial for the heart attack risk prediction process.
        
        **Steps:**
        1. Upload a JSON file containing patient data or choose a predefined patient to simulate the EHR connection.
        2. Review the displayed patient information to ensure accuracy.
        3. Observe the health metrics tiles and ECG details for additional insights.
        4. Use the provided features for an in-depth risk analysis on the next pages.
        """
    )

with st.expander("Simulate EHR Data Transfer", icon=":material/publish:"):
    
    # Creating the column layout
    upload_col1, upload_col2 = st.columns([1, 1])
    
    with upload_col1:
        # File uploader in expander
        uploaded_file = st.file_uploader("Upload a JSON file for new patient data", type="json")
        # Upload JSON area    
        if uploaded_file:
            with st.spinner("Loading patient data..."):
                # Reset specific session state values when a new file is uploaded
                st.session_state['risk_calculated'] = False
                st.session_state['risk_result'] = None
                st.session_state['risk_explanation'] = None
                st.session_state['shap_values'] = None
                
                # Load JSON content into session_state immediately
                st.session_state['patient_data'] = json.load(uploaded_file)
                time.sleep(1)  # Simulating processing delay if needed
                st.success("Patient data loaded successfully!")

    with upload_col2:
        # Dropdown for predefined patients
        selected_patient = st.selectbox(
            "Or choose a predefined patient from the list to simulate EHR data transfer.",
            ("Patient_1", "Patient_2", "Patient_3"),  # Add empty option for default
            index=None,  # Start with the empty option
            placeholder="Select a predefined patient...",
        )
        
        if not selected_patient == None:
            with st.spinner("Loading patient data..."):
                # Reset specific session state values when a new patient is selected
                st.session_state['risk_calculated'] = False
                st.session_state['risk_result'] = None
                st.session_state['risk_explanation'] = None
                st.session_state['shap_values'] = None
                
                # Load JSON content into session_state immediately
                patient_file_path = f"Patient_Simulation_Data/{selected_patient}.json"
                
                try:
                    with open(patient_file_path) as f:
                        st.session_state['patient_data'] = json.load(f)
                    time.sleep(1)  # Simulating processing delay if needed
                    st.success("Patient data loaded successfully!")
                except FileNotFoundError:
                    st.error(f"Data for {selected_patient} not found.")

# Access patient data from session state for the rest of the app
patient_data = st.session_state.get('patient_data', {})
data_available = bool(patient_data)


# Layout columns for displaying patient details
col1, col2 = st.columns([1, 3])

# Column 1: Basic patient info
with col1:

    # Patient pane with default text if no data uploaded
    patient_info = patient_data.get("PatientInfo", {})
    image_path = patient_info.get("patient_photo_link", "visualization/assets/CardioVision.svg")
    image_base64 = get_image_as_base64(image_path)
    # Display the patient pane 
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


    # Cardiologist's Notes popover
    with st.popover("Cardiologist's Notes", use_container_width=True):
        # Retrieve notes from the patient_data if available
        notes = patient_data.get("CardiologistNotes", "No notes available.")
        st.write(notes)

    # Load and display ECG image in a popover
    ecg_image_path = "visualization/assets/12leadecg.svg"
    ecg_image_base64 = get_image_as_base64(ecg_image_path)

    with st.popover("12-lead ECG", use_container_width=True):
        # Display the ECG image in a scrollable container
        st.html(
            f"""
            <div style="overflow-y: auto; max-height: 500px; text-align: center;">
                <img src="data:image/svg+xml;base64,{ecg_image_base64}" alt="12-lead ECG" style="width: 100%; height: auto;">
            </div>
            """
        )

# Column 2: Last Patient Data and Trend Analysis
with col2:

    # Define a function to generate the tile content dynamically
    def display_tile(label, value, color="black"):
        return f"""
            <div class="data-tile" style="width: 20%; margin: 5px; padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); text-align: center;">
                <p style="margin: 0; font-weight: bold; color: #333;">{label}</p>
                <p style="margin: 5px 0; color: {color}; font-size: 18px;">{value}</p>
            </div>
        """

    # Define a function to generate the HTML for complaints dynamically
    def display_complaint(complaint):
        return f"""
            <div class="complaint-box" style="background-color: #f1f3f5; padding: 15px; border-radius: 8px; text-align: center; width: calc(33.33% - 10px); margin-bottom: 10px; box-sizing: border-box; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                <p>{complaint}</p>
            </div>
        """

    # CSS for grid layout
    st.html(
        """
        <style>
        .tile-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: flex-start;
        }
        .data-tile {
            flex: 1 1 calc(25% - 10px);
        }
        .complaints-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: flex-start;
            box-sizing: border-box;
        }
        </style>
        """
    )

    if data_available:
        # Display warning message and red "Calculate Risk" button if the risk is not calculated
        if not st.session_state['risk_calculated']:
            st.html(
                """
                <div style="display: flex; align-items: center; padding: 10px; background-color: #f8d7da; border: 1px solid #f5c6cb; border-radius: 5px; margin-bottom: 15px;">
                    <p style="margin: 0; color: #721c24; flex: 1;">⚠️ No Heart Attack Risk has been calculated.</p>
                </div>
                """
            )
        
        # Core Complaints
        st.subheader("Core Complaints")
        if data_available:
            core_complaints = patient_data.get("CoreComplaints", [])
            
            # Create a container for core complaints in boxes next to each other (3 per row)
            complaints_html = '<div class="complaints-container">'
            for complaint in core_complaints[:9]:  # Adjust number of complaints as needed
                complaints_html += display_complaint(complaint)
            complaints_html += '</div>'
            st.html(complaints_html)
        else:
            st.write("No data available.")

        # Core Complaints
        st.subheader("Patient Evaluation Data")
        # Generate the HTML content for the tiles
        tile_content = f"""
            <div class="tile-container">
                {display_tile("Resting Heart Rate (bpm)", patient_data["VitalParameters"].get("resting_heart_rate", ""), get_color(patient_data["VitalParameters"].get("resting_heart_rate", ""), thresholds.get("resting_heart_rate")))}
                {display_tile("Max Heart Rate (bpm)", patient_data["VitalParameters"].get("max_heart_rate", ""), get_color(patient_data["VitalParameters"].get("max_heart_rate", ""), thresholds.get("max_heart_rate")))}
                {display_tile("Serum Cholesterol (mg/dL)", patient_data["LaboratoryValues"].get("serum_cholesterol", ""), get_color(patient_data["LaboratoryValues"].get("serum_cholesterol", ""), thresholds.get("serum_cholesterol")))}
                {display_tile("Cigarettes per Day", patient_data["SocialFactors"].get("cigarettes_per_day", ""))}
                {display_tile("Has Hypertension", "Yes" if patient_data["VitalParameters"].get("has_hypertension", 0) == 1 else "No", get_condition_color(patient_data["VitalParameters"].get("has_hypertension", 0), 1))}
                {display_tile("ST Depression", patient_data["LaboratoryValues"].get("st_depression", ""), "red" if patient_data["LaboratoryValues"].get("st_depression", 0) > 0 else "black")}
                {display_tile("Exercise Induced Angina", "Yes" if patient_data["SymptomsObservations"].get("exercise_induced_angina", False) else "No", get_condition_color(patient_data["SymptomsObservations"].get("exercise_induced_angina", False), True))}
                {display_tile("Resting ECG Results", patient_data["ECGResults"].get("resting_ecg_results", ""), "red" if patient_data["ECGResults"].get("resting_ecg_results", "").lower() != "normal" else "black")}
            </div>
        """

        # Display the tiles
        st.html(tile_content)

        # Trend Analysis section
        with st.expander("Trend Analysis"):
            date_range = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30)
            trend_data = pd.DataFrame({
                'Date': date_range,
                'Blood Pressure': np.random.randint(110, 140, size=len(date_range)),
                'Cholesterol': np.random.randint(150, 240, size=len(date_range)),
                'FBS': np.random.randint(70, 130, size=len(date_range)),
                'Heart Rate': np.random.randint(60, 100, size=len(date_range)),
            })

            # Define units for each feature
            units = {
                'Blood Pressure': 'mmHg',
                'Cholesterol': 'mg/dL',
                'FBS': 'mg/dL',
                'Heart Rate': 'bpm'
            }

            row1_col1, row1_col2, row1_col3 = st.columns(3)
            with row1_col1:
                feature = st.selectbox('Select feature', ['Blood Pressure', 'Cholesterol', 'FBS', 'Heart Rate'])
            with row1_col2:
                start_date = st.date_input('Start Date', value=datetime.now() - timedelta(days=30))
            with row1_col3:
                end_date = st.date_input('End Date', value=datetime.now())

            if start_date <= end_date:
                filtered_data = trend_data[(trend_data['Date'] >= pd.to_datetime(start_date)) & 
                                        (trend_data['Date'] <= pd.to_datetime(end_date))]
                
                # Plotly line chart with custom y-axis label based on selected feature
                fig = px.line(
                    filtered_data,
                    x='Date',
                    y=feature,
                    title=f'{feature} Over Time',
                    labels={feature: f'{feature} ({units[feature]})', 'Date': 'Date'}
                )

                # Show the plot
                st.plotly_chart(fig)
            else:
                st.error('End date must fall after start date.')


    else:
        st.warning("No patient data uploaded.")