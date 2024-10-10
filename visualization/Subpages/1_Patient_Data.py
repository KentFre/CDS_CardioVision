#This file will cover the patient details

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set the main title of the dashboard
st.title("Patient Data")

st.markdown(
    """
    <style>
    /* Bordered container for panes */
    .pane-container {
        background-color: #ffffff; /* White background for each pane */
        border: 1px solid #e0e0e0; /* Light gray border */
        padding: 15px; /* Padding inside the pane */
        border-radius: 10px; /* Rounded corners */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); /* Subtle shadow for 3D effect */
        margin-bottom: 20px;  /* Space between panes */
    }
    
    /* Patient details pane specific styling */
    .patient-details img {
        width: 80px;  /* Image width for patient picture */
        height: auto;
        border-radius: 50%; /* Circular image */
        margin-right: 10px; /* Space between image and text */
    }
    
    .patient-details h2 {
        color: #333; /* Darker text for patient name */
        font-size: 24px; /* Font size for patient name */
        font-weight: bold; /* Bold patient name */
    }
    
    .patient-details p {
        color: #555; /* Slightly muted color for details */
        font-size: 14px; /* Font size for patient details */
    }

    /* General padding and border for metrics and vitals */
    .metric-pane {
        margin-bottom: 20px;  /* Margin between metric panes */
    }
    </style>
    """, unsafe_allow_html=True
)


# Patient details section
def patient_details():
    st.markdown(
        """
        <div class="details-box">
            <img class="patient-image" src="https://via.placeholder.com/80" alt="Patient Picture">
            <h2>Jose M. Krueger</h2>
            <p><b>Patient ID:</b> 654789</p>
            <p><b>Address:</b> 335 Friendship Lane, Oakland, CA 94612</p>
            <p><b>Phone Number:</b> 408-668-3072</p>
            <p><b>Email ID:</b> josekrueger@teleworm.com</p>
           
        </div>
        """, unsafe_allow_html=True
    )

#Core Complaints section: 
def core_complaints(): 
    st.markdown(
        """
        <div class="details-box">
         <h4>Core Complaints</h4>
            <ul>
                <li>High Blood Pressure</li>
                <li>Severe Chest Pain</li>
                <li>Fatigue</li>
            </ul>
            <a href="https://example.com/cardiologist-notes" target="_blank" style="text-decoration: none; padding: 10px; background-color: #007BFF; color: white; border-radius: 5px; display: inline-block;">Show Cardiologist's Notes</a>
        </div>
        """, unsafe_allow_html=True
    )
    
#Echocardiogram section: 
def ECG(): 
    st.markdown(
        """
        <div class="details-box">
         <h4>ECG Insights</h4>
            <ul>
                <li>Abnormal ECG</li>
                <li>Possible atrial fibrillation</li>
                <li>Possible ST depression</li>
            </ul>
            <a href="https://example.com/ecg-notes" target="_blank" style="text-decoration: none; padding: 10px; background-color: #007BFF; color: white; border-radius: 5px; display: inline-block;">Show ECG Results</a>
        </div>
        """, unsafe_allow_html=True
    )



# Doctor's profile section
doctor_image_url = "https://via.placeholder.com/40"
doctor_name = "Dr. Emily Stone"

# Creating a container for the search bar and doctor profile
with st.container():
    col1, col2 = st.columns([2, 1])  # Adjust column ratio for search and profile

    with col1:
        search_query = st.text_input("Search Patients", placeholder="Search by name or ID", key="search", label_visibility="collapsed")
    
    with col2:
        # Doctor profile with notification bell first
        st.markdown(
            f"""
            <div class="doctor-profile" style="display: flex; align-items: center;">
                <span class="notification-bell" title="Notifications" style="font-size: 15px;">
                    🔔
                </span>
                <h4 style="margin: 0; font-size: 14px;">{doctor_name}</h4>
                <img class="doctor-image" src="{doctor_image_url}" alt="Doctor Picture" style="width: 30px; height: auto;">
            </div>
            """, unsafe_allow_html=True
        )
         

# Function to create a line chart
def plot_vitals(data, label, color):
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.plot(data, color=color, marker='o')
    ax.set_title(label, fontsize=9)
    ax.grid(True)
    ax.tick_params(axis='both', which='major', labelsize=6)
    return fig

# Function to display patient details
def display_patient_details(patient_info):
    st.markdown(
        f"""
        <div class="patient-details">
            <img class="patient-image" src="{patient_info['image']}" alt="Patient Picture">
            <h2>{patient_info['name']}</h2>
            <p><b>Patient ID:</b> {patient_info['patient_id']}</p>
            <p><b>Address:</b> {patient_info['address']}</p>
            <p><b>Phone Number:</b> {patient_info['phone']}</p>
            <p><b>Email ID:</b> {patient_info['email']}</p>
            <h4>Core Complaints</h4>
            <ul>
                {"".join(f"<li>{complaint}</li>" for complaint in patient_info['complaints'])}
            </ul>
            <a href="{patient_info['notes_url']}" target="_blank" style="text-decoration: none; padding: 10px; background-color: #007BFF; color: white; border-radius: 5px; display: inline-block;">Show Cardiologists Notes</a>
        </div>
        """, unsafe_allow_html=True
    )

# Patient data
patient_info = {
    "image": "https://via.placeholder.com/80",
    "name": "Jose M. Krueger",
    "address": "335 Friendship Lane, Oakland, CA 94612",
    "patient_id": "654789",
    "phone": "408-668-3072",
    "email": "josekrueger@teleworm.com",
    "risk": "High",
    "complaints": ["High Blood Pressure", "Severe Chest Pain", "Fatigue"],
    "notes_url": "https://example.com/cardiologist-notes"
}

# Layout using columns
col1, col2 = st.columns([1, 3])

# Column 1: Patient details
with col1:
    display_patient_details(patient_info)


# Mock data for vitals
bp_values = np.random.randint(110, 160, size=3)
hr_values = np.random.randint(60, 100, size=3)
fbs_values = np.random.randint(70, 150, size=3)
cholesterol_values = np.random.randint(150, 300, size=3)

# Column 2: Vitals and metrics section
with col2:
    st.markdown("### HA Risk Calculator")
        # Action button for HA Risk Calculation
    if st.button("Calculate Risk"):
        # Save any necessary session data if required
        st.session_state['patient_info'] = patient_info  # Example of storing patient info
        # Navigate to 2_Risk_Calculation.py
        st.query_params(subpage="2_Risk_Calculation")
        st.experimental_rerun()

    # Blood Pressure and Heart Rate
    col21, col22 = st.columns(2)
    with col21:
        st.markdown("<h5 style='color: red;'>Blood Pressure</h5>", unsafe_allow_html=True)
        st.metric(label="Blood Pressure", value="120/80 mmHg", label_visibility="collapsed")
        st.pyplot(plot_vitals(bp_values, "Blood Pressure (mmHg)", "red"))
    
    with col22:
        st.markdown("<h5 style='color: purple;'>Heart Rate</h5>", unsafe_allow_html=True)
        st.metric(label="Heart Rate", value="80 bpm", label_visibility="collapsed")
        st.pyplot(plot_vitals(hr_values, "Heart Rate (bpm)", "purple"))

    # FBS and Cholesterol
    col23, col24 = st.columns(2)
    with col23:
        st.markdown("<h5 style='color: blue;'>Fasting Blood Sugar (FBS)</h5>", unsafe_allow_html=True)
        st.metric(label="FBS", value="100 mg/dL", label_visibility="collapsed")
        st.pyplot(plot_vitals(fbs_values, "FBS (mg/dL)", "blue"))
    
    with col24:
        st.markdown("<h5 style='color: orange;'>Cholesterol</h5>", unsafe_allow_html=True)
        st.metric(label="Cholesterol", value="200 mg/dL", label_visibility="collapsed")
        st.pyplot(plot_vitals(cholesterol_values, "Cholesterol (mg/dL)", "orange"))

