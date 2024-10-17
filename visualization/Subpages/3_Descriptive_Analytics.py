import streamlit as st
import pandas as pd
import plotly.express as px
from models.data_utils import load_data, get_summary_statistics, get_gender_distribution

# Doctor Profile and Title
doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state.get('doctor_image_base64', '')

with st.container():
    r1, r2 = st.columns([2, 1])
    with r1:
        r1.title("Descriptive Analytics")
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

# Load and prepare data
data_path = '../visualization/assets/heart_disease_data.csv'
df = load_data(data_path)
total_patients, total_risk_patients, average_age = get_summary_statistics(df)

# Instructions Expander
with st.expander(label="🛈 Instructions"):
    st.write(
        """
        Welcome to the **Descriptive Analytics** page! Here, you can:
        
        - View key statistics about the patient population, including the number of patients, heart attack incidence, and average age.
        - Visualize data distribution and relationships within the population, such as age and gender breakdowns.
        - Customize graphs to explore specific features such as cholesterol levels, heart rate, and heart attack risk factors.
        
        Use the dropdowns in each section to adjust the visualizations based on your preferences.
        """
    )


# Function to generate tile content with HTML
def display_tile(label, value, color="black"):
    return f"""
        <div class="data-tile" style="width: 20%; margin: 5px; padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); text-align: center;">
            <p style="margin: 0; font-weight: bold; color: #333;">{label}</p>
            <p style="margin: 5px 0; color: {color}; font-size: 18px;">{value}</p>
        </div>
    """

# CSS for grid layout
st.markdown(
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
    </style>
    """,
    unsafe_allow_html=True
)

# Display tiles within a container
total_patients = 396
total_risk_patients = 217
average_age = 55.9

# Concatenate all the tiles as a single HTML string
tiles_html = f"""
<div class="tile-container">
    {display_tile("Number of Patients", total_patients)}
    {display_tile("Patients with Heart Attack", total_risk_patients)}
    {display_tile("Average Age of Patients", average_age)}
</div>
"""
# Dropdown for visualization selection
st.subheader("Patient Population Base")

# Pass the concatenated HTML to st.markdown
st.html(tiles_html)



# Expander for Population Visualization
with st.expander("Population Visualization", expanded=True):
    g1, g2 = st.columns((1, 1))

    # Select the graphs to display
    graph_options = ['Gender Distribution', 'Age Distribution of Patients', 'Heart Attack Risk by Gender', 'Distribution of Heart Attacks']
    selected_graph1 = g1.selectbox("Select first graph", graph_options, index=0)
    selected_graph2 = g2.selectbox("Select second graph", graph_options, index=1)
    
    # First Graph Visualization
    if selected_graph1 == 'Gender Distribution':
        fig1 = px.pie(df, names='gender', title='Gender Distribution')
        fig1.update_traces(marker=dict(colors=['skyblue', 'lightcoral']))
        g1.plotly_chart(fig1, use_container_width=True)

    elif selected_graph1 == 'Age Distribution of Patients':
        fig1 = px.histogram(df, x='age', nbins=10, title='Age Distribution of Patients')
        fig1.update_traces(marker_color='#2a9d8f')
        g1.plotly_chart(fig1, use_container_width=True)

    elif selected_graph1 == 'Heart Attack Risk by Gender':
        risk_by_gender = df[df['heart_disease_diagnosis'] == True]['gender'].value_counts()
        fig1 = px.bar(risk_by_gender, x=risk_by_gender.index, y=risk_by_gender.values, title='Heart Attack Risk by Gender')
        fig1.update_traces(marker_color='#264653')
        g1.plotly_chart(fig1, use_container_width=True)

    elif selected_graph1 == 'Distribution of Heart Attacks':
        risk_distribution = df['heart_disease_diagnosis'].value_counts().reset_index()
        risk_distribution.columns = ['Heart Attack Risk', 'Count']
        fig1 = px.bar(risk_distribution, x='Heart Attack Risk', y='Count', title='Distribution of Heart Attacks')
        fig1.update_traces(marker_color='#234973')
        g1.plotly_chart(fig1, use_container_width=True)

    # Second Graph Visualization
    if selected_graph2 == 'Gender Distribution':
        fig2 = px.pie(df, names='gender', title='Gender Distribution')
        fig2.update_traces(marker=dict(colors=['skyblue', 'lightcoral']))
        g2.plotly_chart(fig2, use_container_width=True)

    elif selected_graph2 == 'Age Distribution of Patients':
        fig2 = px.histogram(df, x='age', nbins=10, title='Age Distribution of Patients')
        fig2.update_traces(marker_color='#2a9d8f')
        g2.plotly_chart(fig2, use_container_width=True)

    elif selected_graph2 == 'Heart Attack Risk by Gender':
        risk_by_gender = df[df['heart_disease_diagnosis'] == True]['gender'].value_counts()
        fig2 = px.bar(risk_by_gender, x=risk_by_gender.index, y=risk_by_gender.values, title='Heart Attack Risk by Gender')
        fig2.update_traces(marker_color='#264653')
        g2.plotly_chart(fig2, use_container_width=True)

    elif selected_graph2 == 'Distribution of Heart Attacks':
        risk_distribution = df['heart_disease_diagnosis'].value_counts().reset_index()
        risk_distribution.columns = ['Heart Attack Risk', 'Count']
        fig2 = px.bar(risk_distribution, x='Heart Attack Risk', y='Count', title='Distribution of Heart Attacks')
        fig2.update_traces(marker_color='#234973')
        g2.plotly_chart(fig2, use_container_width=True)

# Dropdown for visualization selection
st.subheader("Data Visualisation")
# Expander for Further Data Description with additional options for deeper analysis
with st.expander("Further Data Description"):
    st.subheader("Custom Data Exploration")
    
    # Choose feature to explore
    feature_options = ['Cholesterol Levels', 'Resting Heart Rate', 'Max Heart Rate']
    selected_feature = st.selectbox('Choose a feature to analyze:', feature_options)
    
    # Display corresponding visualization based on the selection
    if selected_feature == 'Cholesterol Levels':
        fig3 = px.histogram(df, x='serum_cholesterol', title='Cholesterol Level Distribution', nbins=20)
        fig3.update_layout(xaxis_title='Cholesterol (mg/dL)', yaxis_title='Number of Patients')
        st.plotly_chart(fig3, use_container_width=True)

    elif selected_feature == 'Resting Heart Rate':
        fig3 = px.histogram(df, x='resting_heart_rate', title='Resting Heart Rate Distribution', nbins=20)
        fig3.update_layout(xaxis_title='Resting Heart Rate (BPM)', yaxis_title='Number of Patients')
        st.plotly_chart(fig3, use_container_width=True)

    elif selected_feature == 'Max Heart Rate':
        fig3 = px.histogram(df, x='max_heart_rate', title='Max Heart Rate Distribution', nbins=20)
        fig3.update_layout(xaxis_title='Max Heart Rate (BPM)', yaxis_title='Number of Patients')
        st.plotly_chart(fig3, use_container_width=True)
