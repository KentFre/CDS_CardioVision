# This file will cover the patient data tab

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import base64

# Function to load and encode the image as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state['doctor_image_base64']

with st.container():
    r1, r2 = st.columns([2, 1])

    with r1:
        # Display the title in the first column
        r1.title("Patient Data")

    with r2:
        # Display the profile information with the image, right-aligned and with reduced whitespace
        st.markdown(
            f"""
            <div class="doctor-profile" style="display: flex; align-items: center; justify-content: flex-end;">
                <span class="notification-bell" title="Notifications" style="font-size: 15px; margin-right: 5px;">
                    🔔
                </span>
                <h4 style="margin: 0; font-size: 14px; margin-right: 0px;">{doctor_name}</h4>
                <img src="data:image/png;base64,{doctor_image_base64}" alt="Doctor Picture" style="width: 35px; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <style>
    /* Bordered container for panes */
    .pane-container {
        background-color: #000000; /* White background for each pane */
        border: 1px solid #000000; /* Light gray border */
        padding: 15px; /* Padding inside the pane */
        border-radius: 15px; /* Rounded corners */
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
        <div class="pane-container">
            <div class="patient-details">
                <img class="patient-image" src="{image}" alt="Patient Picture">
                <h2>{name}</h2>
                <p><b>Patient ID:</b> {patient_id}</p>
                <p><b>Address:</b> {address}</p>
                <p><b>Phone Number:</b> {phone}</p>
                <p><b>Email ID:</b> {email}</p>
            </div>
        </div>
        """.format(**patient_info), unsafe_allow_html=True
    )

# Creating a container for the search bar and doctor profile
with st.container():
    col1, col2 = st.columns([2, 1])  # Adjust column ratio for search and profile

    with col1:
        search_query = st.text_input("Search Patients", placeholder="Search by name or ID", key="search", label_visibility="collapsed")
    
    with col2:
        # Doctor profile with notification bell first
        pass

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
}

# Function to generate trend analysis graph
def generate_trend_analysis(data, feature, start_date, end_date):
    # Convert start_date and end_date to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the data based on the selected date range
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    # Generate the line graph
    fig = px.line(filtered_data, x='Date', y=feature, title=f'{feature} Trend Analysis')
    st.plotly_chart(fig)

# Simulated patient data for trend analysis
def generate_sample_data():
    date_range = pd.date_range(start=datetime.now() - timedelta(days=30), periods=30)
    data = pd.DataFrame({
        'Date': date_range,
        'Blood Pressure': np.random.randint(110, 140, size=len(date_range)),
        'Cholesterol': np.random.randint(150, 240, size=len(date_range)),
        'FBS': np.random.randint(70, 130, size=len(date_range)),
        'Heart Rate': np.random.randint(60, 100, size=len(date_range)),
    })
    return data

# Layout using columns
col1, col2 = st.columns([1, 3])

# Column 1: Patient details
with col1:
    display_patient_details(patient_info)


    # Core Complaints Section
    st.markdown("<h3 style='font-size:18px;'>Core Complaints</h3>", unsafe_allow_html=True)
    core_complaints = """
    - Chest pain
    - Shortness of breath
    - Dizziness
    - Irregular heartbeat
    """
    st.markdown(core_complaints)

# Action button to show cardiologist's notes
    if st.button("Cardiologist's Notes"):
        st.write("Displaying Cardiologist's Notes...")
                
# ECG Section
    st.markdown("<h3 style='font-size:18px;'>Echocardiogram</h3>", unsafe_allow_html=True)
    ecg_results = """
    - Abnormal ECG
    - Possible atrial fibrillation
    - Possible ST Depression
    """
    st.markdown(ecg_results)
    
# Action button to show cardiologist's notes
    if st.button("12 - lead ECG"):
        st.write("Displaying ECG Results...")

            
# Column 2: Action button and trend analysis
    with col2:
        st.markdown('<div class="calculate-risk-button">', unsafe_allow_html=True)
        if st.button("Calculate Risk"):
            st.write("Redirecting to Subpage 2 for Risk Prediction...")
        st.markdown('</div>', unsafe_allow_html=True)

        # Trend analysis section
        st.subheader("Trend Analysis")

        # Simulated data
        data = generate_sample_data()

        # User input for feature and date range
        feature = st.selectbox('Select feature', ['Blood Pressure', 'Cholesterol', 'FBS', 'Heart Rate'])
        start_date = st.date_input('Start Date', value=datetime.now() - timedelta(days=30))
        end_date = st.date_input('End Date', value=datetime.now())

        # Generate trend analysis graph
        if start_date <= end_date:
            generate_trend_analysis(data, feature, start_date, end_date)
        else:
            st.error('End date must fall after start date.')


