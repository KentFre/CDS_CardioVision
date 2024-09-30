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


# Function to apply custom borders to panes
def bordered_pane(content, pane_title):
    st.markdown(f"""
        <div style="
            border: 2px solid #4CAF50;  /* Green border */
            border-radius: 8px;         /* Rounded corners */
            padding: 15px;              /* Padding inside the pane */
            margin-bottom: 20px;        /* Spacing between panes */
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Optional: shadow effect */
        ">
        <h3 style='font-size:18px;'>{pane_title}</h3>
        {content}
        </div>
    """, unsafe_allow_html=True)

# Create three columns for layout
col1, col2, col3 = st.columns([1, 1, 1])

# First Column: Risk Score and Critical Alerts side by side
with col1:
    # Create two sub-columns within the first column
    sub_col1, sub_col2 = st.columns(2)
    
    with sub_col1:
        # Smaller subheader using HTML/CSS style in markdown
        st.markdown("<h3 style='font-size:18px;'>RISK SCORE</h3>", unsafe_allow_html=True)  # Heading size reduced
        
        # Slider for Risk Score
        risk_score = st.slider("Select Risk Score", 0, 10, 5, label_visibility="collapsed")  # Default value is 5
        
        # Smaller font for the current risk score display
        st.markdown(f"<p style='font-size:14px;'>Current Risk Score: {risk_score}</p>", unsafe_allow_html=True)  # Smaller text for risk score

        # Pie chart displaying the percentage of the risk
        #risk_data = [risk_score, 10 - risk_score]  # Risk vs No Risk
        #pie_colors = ['red', 'green']  # Red for risk, green for no risk
        
        #fig, ax = plt.subplots()
        #ax.pie(risk_data, colors=pie_colors, startangle=90)  # No labels, no percentages
        #ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.

        #st.pyplot(fig)  # Display the pie chart"


    with sub_col2:
        st.button(" CRITICAL ALERTS", key="feature1")

with col1:
    st.markdown("<h3 style='font-size:18px;'>ACTIONABLE INSIGHTS</h3>", unsafe_allow_html=True)  # Heading size reduced
    st.write("Content for Actionable Insights Pane")  # Replace with actual content based of the ML Algorithm
    st.button(" Appointments", key="feature2")


    st.markdown("<h3 style='font-size:18px;'>PATIENT RISK SUMMARY</h3>", unsafe_allow_html=True)  # Heading size reduced
    # Create date inputs for filtering the data
    start_date = st.date_input("Start Date:", df['Month'].min())
    end_date = st.date_input("End Date:", df['Month'].max())

    # Filter the data based on the selected date range
    filtered_df = df[(df['Month'] >= pd.Timestamp(start_date)) & (df['Month'] <= pd.Timestamp(end_date))]

    # Display the filtered DataFrame as a table
    st.dataframe(filtered_df)
   
    

# Second Column (Col 2 and Col 3 for Row 1)
# Second Column: Diagnostic Imaging
with col2:
    st.markdown("<h3 style='font-size:18px;'>DIAGNOSTIC IMAGING</h3>", unsafe_allow_html=True)

    # Date range selection for diagnostic imaging
    diag_start_date = st.date_input("Start Date;", df['Month'].min())
    diag_end_date = st.date_input("End Date;", df['Month'].max())

    # Sample diagnostic imaging data with specified tests
    diagnostic_data = {
        "Month": pd.date_range(start="2023-01-01", periods=7, freq='ME'),
        "Tests": ["X-Ray", "CT Scan", "Chest X-Ray", "Echocardiogram", "Angiogram", 
                  "CT Angiography", "MRI Angiography"],
        "Links": [
            "http://emr.example.com/xray", "http://emr.example.com/ctscan", 
            "http://emr.example.com/chestxray", "http://emr.example.com/echocardiogram",
            "http://emr.example.com/angiogram", "http://emr.example.com/ctangiography",
            "http://emr.example.com/mriangiography"
        ]
    }

    diag_df = pd.DataFrame(diagnostic_data)

    # Filter diagnostic imaging data based on selected date range
    filtered_diag_df = diag_df[(diag_df['Month'] >= pd.Timestamp(diag_start_date)) & 
                                (diag_df['Month'] <= pd.Timestamp(diag_end_date))]

    # Display diagnostic imaging data in a table with hyperlinks
    if not filtered_diag_df.empty:
        filtered_diag_df['Links'] = filtered_diag_df.apply(
            lambda row: create_hyperlink(row['Tests'], row['Links']), axis=1
        )
        st.write(filtered_diag_df[['Month', 'Links']].to_html(escape=False), unsafe_allow_html=True)
    else:
        st.write("No diagnostic imaging tests found for the selected date range.")



with col3:
    # Key Lab Results Pane with border
    st.markdown("<h3 style='font-size:18px;'>KEY LAB RESULTS</h3>", unsafe_allow_html=True)  # Heading size reduced
    
    # Sample DataFrame for Key Lab Results
    lab_data = {
        "Date": pd.date_range(start="2023-01-01", periods=5, freq='ME'),
        "Tests": ["Cholesterol", "Blood Pressure", "Fasting Blood Sugar", "Electrocardiogram", "Heart Rate"],
        "Normal Values": ["<200 mg/dL", "120/80 mmHg", "<100 mg/dL", "Normal", "60-100 bpm"]
    }
    
    lab_df = pd.DataFrame(lab_data)

    # Date range selection for lab results
    lab_start_date = st.date_input("Start Date", lab_df['Date'].min())
    lab_end_date = st.date_input("End Date", lab_df['Date'].max())

    # Filter lab results based on the selected date range
    filtered_lab_df = lab_df[(lab_df['Date'] >= pd.Timestamp(lab_start_date)) & 
                              (lab_df['Date'] <= pd.Timestamp(lab_end_date))]

    # Display filtered lab results
    if not filtered_lab_df.empty:
        st.write(filtered_lab_df[['Date', 'Tests', 'Normal Values']])
    else:
        st.write("No lab results found for the selected date range.")







# Create a new section for Trend Analysis directly below the first row of col2 and col3
st.markdown("<h3 style='font-size:18px; text-align:center;'>TREND ANALYSIS</h3>", unsafe_allow_html=True)

# Create two sub-columns for the Trend Analysis graphs
trend_col1, trend_col2 = st.columns(2)

# First graph: Chest pain vs BP vs Time
with trend_col1:
    fig1 = px.line(df, x='Month', y='trestbps', color='cp', title='Chest Pain vs BP vs Time')
    st.plotly_chart(fig1)

# Second graph: Cholesterol vs BP vs Time
with trend_col2:
    fig2 = px.line(df, x='Month', y='chol', color='chol', title='Cholesterol vs BP vs Time')
    st.plotly_chart(fig2)

# Customize button below both graphs
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Customize"):
    st.write("Customization options would go here.")
st.markdown("</div>", unsafe_allow_html=True)