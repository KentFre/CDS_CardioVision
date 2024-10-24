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

        If you are unfamiliar with **CardioVision**, please study this page first:""")

        # Learn more about CardioVision button
    st.page_link("visualization/Subpages/5_About.py", label="Learn more about CardioVision", icon=":material/help:")
    st.write(
        """
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
            
            if core_complaints:
                # Create a container for core complaints in boxes next to each other (3 per row)
                complaints_html = '<div class="complaints-container">'
                for complaint in core_complaints[:9]:  # Adjust number of complaints as needed
                    complaints_html += display_complaint(complaint)
                complaints_html += '</div>'
                st.html(complaints_html)
            else:
                st.info("No core complaints recorded.")
        else:
            st.info("No data available.")

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
        st.error("No patient data received from Electronic Health Record (EHR) System!")
        # Popover to modify patient data

        # Default values for form inputs (this won't change st.session_state)
        default_patient_data = {
            "PatientInfo": {
                "patient_id": "Enter ID",
                "age": 50,
                "gender": "Male"
            },
            "SymptomsObservations": {
                "chest_pain_type": "Typical Angina",
                "exercise_induced_angina": False
            },
            "VitalParameters": {
                "resting_heart_rate": 60.0,
                "max_heart_rate": 150.0,
                "has_hypertension": False  # Set as False for default
            },
            "LaboratoryValues": {
                "serum_cholesterol": 200.0,
                "high_fasting_blood_sugar": False,
                "st_depression": 1.0
            },
            "ECGResults": {
                "resting_ecg_results": "Normal"
            },
            "SocialFactors": {
                "cigarettes_per_day": 0.0,
                "years_smoking": 0.0,
                "family_history_cad": False
            }
        }

        # Popover to modify patient data
        with st.popover(" 📝 Manually add Patient Data", use_container_width=True):
            with st.form("modify_patient_data"):
                # Create two columns
                col1, col2 = st.columns(2)

                # Column 1: Patient Info, Symptoms Observations, Vital Parameters
                with col1:
                    st.subheader("Patient Info")
                    patient_id = st.text_input("Patient ID", value=default_patient_data['PatientInfo']['patient_id'])
                    age = st.number_input("Age", value=default_patient_data['PatientInfo']['age'])
                    gender = st.selectbox("Gender", options=["Male", "Female"], index=0 if default_patient_data['PatientInfo']['gender'] == "Male" else 1)

                    st.subheader("Symptoms & Observations")
                    chest_pain_type = st.selectbox(
                        "Chest Pain Type", 
                        options=["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"],
                        index=["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"].index(default_patient_data['SymptomsObservations']['chest_pain_type'])
                    )
                    exercise_induced_angina = st.checkbox("Exercise Induced Angina", value=default_patient_data['SymptomsObservations']['exercise_induced_angina'])

                    st.subheader("Vital Parameters")
                    resting_heart_rate = st.number_input("Resting Heart Rate (bpm)", value=int(default_patient_data['VitalParameters']['resting_heart_rate']), step=1)
                    max_heart_rate = st.number_input("Maximum Heart Rate (bpm)", value=int(default_patient_data['VitalParameters']['max_heart_rate']), step=1)
                    has_hypertension = st.checkbox("Has Hypertension", value=default_patient_data['VitalParameters']['has_hypertension'])

                # Column 2: Laboratory Values, ECG Results, Social Factors
                with col2:
                    st.subheader("Laboratory Values")
                    serum_cholesterol = st.number_input("Serum Cholesterol (mg/dL)", value=int(default_patient_data['LaboratoryValues']['serum_cholesterol']), step=1)
                    high_fasting_blood_sugar = st.checkbox("High Fasting Blood Sugar", value=default_patient_data['LaboratoryValues']['high_fasting_blood_sugar'])
                    
                    st.subheader("ECG Results")
                    resting_ecg_results = st.selectbox(
                        "Resting ECG Results", 
                        options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"],
                        index=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(default_patient_data['ECGResults']['resting_ecg_results'])
                    )
                    st_depression = st.number_input("ST Depression", value=default_patient_data['LaboratoryValues']['st_depression'], step=0.1, format="%.1f")


                    st.subheader("Social Factors")
                    cigarettes_per_day = st.number_input("Cigarettes Per Day", value=int(default_patient_data['SocialFactors']['cigarettes_per_day']), step=1)
                    years_smoking = st.number_input("Years Smoking", value=int(default_patient_data['SocialFactors']['years_smoking']), step=1)
                    family_history_cad = st.checkbox("Family History of CAD", value=default_patient_data['SocialFactors']['family_history_cad'])

                # Submit button to update data
                submitted = st.form_submit_button("Update Data")

                if submitted:
                    # After submission, update st.session_state (or save to JSON file)
                    st.session_state['patient_data'] = {
                        "PatientInfo": {
                            "patient_id": patient_id,
                            "age": age,
                            "gender": gender
                        },
                        "SymptomsObservations": {
                            "chest_pain_type": chest_pain_type,
                            "exercise_induced_angina": exercise_induced_angina
                        },
                        "VitalParameters": {
                            "resting_heart_rate": resting_heart_rate,
                            "max_heart_rate": max_heart_rate,
                            "has_hypertension": 1 if has_hypertension else 0
                        },
                        "LaboratoryValues": {
                            "serum_cholesterol": serum_cholesterol,
                            "high_fasting_blood_sugar": high_fasting_blood_sugar,
                            "st_depression": round(st_depression,1)
                        },
                        "ECGResults": {
                            "resting_ecg_results": resting_ecg_results
                        },
                        "SocialFactors": {
                            "cigarettes_per_day": cigarettes_per_day,
                            "years_smoking": years_smoking,
                            "family_history_cad": family_history_cad
                        }
                    }

                    st.success("Patient data updated successfully!")
                    st.rerun()