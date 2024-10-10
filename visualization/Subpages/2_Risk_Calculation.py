# This file will cover the diagnostic analysis tab

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime


# Set the main title of the dashboard
st.title("Risk Calculation")

# Sample DataFrame for Patients Risk Summary
data = {
    "Month": pd.date_range(start="2023-01-01", periods=12, freq='ME'),
    "cp": [1, 2, 3, 2, 1, 3, 1, 2, 3, 1, 2, 3],
    "trestbps": [130, 140, 125, 138, 132, 145, 128, 130, 135, 120, 142, 135],
    "chol": [250, 240, 260, 255, 245, 270, 230, 220, 255, 240, 275, 265],
    "fbs": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "restecg": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "thalach": [150, 160, 165, 158, 155, 170, 145, 150, 160, 165, 168, 175],
    "exang": [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
    "oldpeak": [1.2, 2.3, 1.1, 2.5, 1.6, 2.7, 1.0, 1.8, 2.2, 1.5, 2.1, 1.9],
    "slope": [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
    "ca": [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2],
    "thal": [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
    "risk score": [7, 8, 6, 7, 8, 9, 6, 7, 8, 5, 9, 7]
}

# Convert dictionary to a DataFrame
df = pd.DataFrame(data)

# Create a function to generate hyperlinks
def create_hyperlink(text, url):
    return f'<a href="{url}" target="_blank">{text}</a>'

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

# Layout using columns
col1, col2 = st.columns([1, 3])

# Column 1: Patient details
with col1:
    display_patient_details(patient_info)


