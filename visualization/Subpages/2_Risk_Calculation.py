# This file will cover the diagnostic analysis tab
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime

from models.model_utils import load_preprocessor, load_model, process_and_predict
# Load the model and preprocessor once at the start
preprocessor = load_preprocessor("../visualization/models/standardizer.pkl")
risk_model = load_model("../visualization/models/risk_prediction_model.pkl")

# Create two columns with specified ratios
r1, r2 = st.columns((0.1, 1))

# Display the logo in the first column
r1.image("../visualization/assets/CardioVision_icon.png", width=60)

# Set the title in the second column
r2.title("Risk Calculation")

# Sample data for demonstration purposes
def load_data():
    data = pd.read_csv('../visualization/assets/heart_disease_data.csv')
    return data

# Load the dataset
data = load_data()

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
        # File uploader that only accepts JSON files
        uploaded_file = st.file_uploader("Choose a JSON file", type="json")
        if uploaded_file is not None:
            try:
                transformed_df = process_and_predict(preprocessor, risk_model, uploaded_file)
                
                # Display the DataFrame in Streamlit
                st.write("Transformed Data with Column Names:")
                st.dataframe(transformed_df)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    
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


    # HA Risk Section
    st.markdown("<h3 style='font-size:18px;'>Heart Attack Risk</h3>", unsafe_allow_html=True)
    #Prediction model here 
    
                
    # Patiient Risk Summary  Section
    st.markdown("<h3 style='font-size:18px;'>Patient Risk Summary</h3>", unsafe_allow_html=True)
    risk_summary = """
    """
    st.markdown(risk_summary)
    #If prediction is yes, highlight 3 top features causing prediction. If no, mention patient is currently not at risk should continue with diet and excerise etc 


# Column 2: Action button and Result Section
with col2:
    st.markdown('<div class="Save result in EMR">', unsafe_allow_html=True)
    if st.button("Save Result in EMR"):
        st.write("Results saved in EMR...")
    st.markdown('</div>', unsafe_allow_html=True)

    # Results section
    st.subheader("Results")
    #Results from prediction model


    #Results Explanation
    st.subheader ("Results Explanation")

    # Explanation of the SHAP Analysis
    st.markdown("""
    The SHAP (SHapley Additive exPlanations) analysis provides a method for explaining the predictions made.
    It assigns an importance value (SHAP value) to each feature for a particular prediction, indicating how much that feature 
    contributes positively or negatively to the outcome. 
    SHAP ensures that feature contributions are fairly distributed. This allows for transparent, interpretable insights into 
    how individual features influence the prediction, helping the doctor understand why a patient is at a certain risk level 
    """)

    #Code for the SHAP analysis. 

