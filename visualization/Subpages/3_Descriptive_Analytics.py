#####################################################################################
# 3_Descriptive_Analytics.py                                                        #
#                                                                                   #
# This is the streamlit page showing descriptive analysis                           #
#                                                                                   #
# - Perform Descriptive Evaluations                                                 #
#####################################################################################

# Import needed libaries
import streamlit as st
import pandas as pd
from visualization.models.plot_utils import (
    plot_gender_distribution,
    plot_age_distribution,
    plot_risk_by_gender,
    plot_risk_distribution,
    plot_age_distribution_by_gender_and_heart_attack,
    plot_heart_attack_by_age_group_and_gender
)
import plotly.express as px
from visualization.models.data_utils import get_summary_statistics

#####################################################################################
### File preparation: Functions and Status checks and model import                ###
#####################################################################################

# Load and prepare data
# Access data from session state in other subpages
if 'df' in st.session_state:
    df = st.session_state['raw_df']
else:
    st.error("Data not loaded. Please go back to the main page to load the data.")

total_patients, total_risk_patients, average_age = get_summary_statistics(df)


#####################################################################################
### Page Title and Doctor Info                                                    ###
#####################################################################################

# Doctor Profile and Title
doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state.get('doctor_image_base64', '')

with st.container():
    r1, r2 = st.columns([2, 1])
    with r1:
        r1.title("Descriptive Analytics")
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

# Instructions Expander
with st.expander(label="Instructions", icon=":material/info:"):
    st.write(
        """
        Welcome to the **Descriptive Analytics** page! Here, you can:
        
        - View key statistics about the patient population, including the number of patients, heart attack incidence, and average age.
        - Visualize data distribution and relationships within the population, such as age and gender breakdowns.
        - Customize graphs to explore specific features such as cholesterol levels, heart rate, and heart attack risk factors.
        
        Use the dropdowns in each section to adjust the visualizations based on your preferences.
        """
    )

#####################################################################################
### Display the value tiles                                                       ###
#####################################################################################

# Function to generate tile content with HTML
def display_tile(label, value, color="black"):
    return f"""
        <div class="data-tile" style="width: 20%; margin: 5px; padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05); text-align: center;">
            <p style="margin: 0; font-weight: bold; color: #333;">{label}</p>
            <p style="margin: 5px 0; color: {color}; font-size: 18px;">{value}</p>
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
    </style>
    """
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

#####################################################################################
### Expander for population visualizations                                        ###
#####################################################################################

# Expander for Population Visualization with independent filtering for each graph
with st.expander("Population Visualization", expanded=True):
    
    st.info("Choose predefined visualizations to explore key insights into the general patient population used to train the model. You can also filter the data for each graph.")

    # Create two columns for the graphs and their respective filters
    g1, g2 = st.columns((1, 1))

    # First graph filtering and graph options
    with g1:
        # Add a radio button for filtering data for the first graph
        patient_filter1 = st.radio(
            "Select patient group for first graph:",
            ("All Patients", "Only Heart Attack Patients", "Only No Heart Attack Patients")
        )

        # Apply the filtering logic for the first graph
        if patient_filter1 == "Only Heart Attack Patients":
            filtered_df1 = df[df['heart_disease_diagnosis'] == True]
        elif patient_filter1 == "Only No Heart Attack Patients":
            filtered_df1 = df[df['heart_disease_diagnosis'] == False]
        else:
            filtered_df1 = df  # All patients

        # Graph options for the first graph
        graph_options = [
            'Gender Distribution', 
            'Age Distribution of Patients', 
            'Heart Attack Risk by Gender', 
            'Distribution of Heart Attacks',
            'Age Distribution by Gender and Heart Attack Status',
            'Heart Attack Distribution by Age Group and Gender'
        ]
        selected_graph1 = st.selectbox("Select first graph", graph_options, index=0)

        # First Graph Visualization based on filtered data
        if selected_graph1 == 'Gender Distribution':
            fig1 = plot_gender_distribution(filtered_df1)
            st.plotly_chart(fig1, use_container_width=True)

        elif selected_graph1 == 'Age Distribution of Patients':
            fig1 = plot_age_distribution(filtered_df1)
            st.plotly_chart(fig1, use_container_width=True)

        elif selected_graph1 == 'Heart Attack Risk by Gender':
            fig1 = plot_risk_by_gender(filtered_df1)
            st.plotly_chart(fig1, use_container_width=True)

        elif selected_graph1 == 'Distribution of Heart Attacks':
            fig1 = plot_risk_distribution(filtered_df1)
            st.plotly_chart(fig1, use_container_width=True)

        elif selected_graph1 == 'Age Distribution by Gender and Heart Attack Status':
            fig1 = plot_age_distribution_by_gender_and_heart_attack(filtered_df1)
            st.plotly_chart(fig1, use_container_width=True)

        elif selected_graph1 == 'Heart Attack Distribution by Age Group and Gender':
            fig1 = plot_heart_attack_by_age_group_and_gender(filtered_df1)
            st.plotly_chart(fig1, use_container_width=True)

    # Second graph filtering and graph options
    with g2:
        # Add a radio button for filtering data for the second graph
        patient_filter2 = st.radio(
            "Select patient group for second graph:",
            ("All Patients", "Only Heart Attack Patients", "Only No Heart Attack Patients")
        )

        # Apply the filtering logic for the second graph
        if patient_filter2 == "Only Heart Attack Patients":
            filtered_df2 = df[df['heart_disease_diagnosis'] == True]
        elif patient_filter2 == "Only No Heart Attack Patients":
            filtered_df2 = df[df['heart_disease_diagnosis'] == False]
        else:
            filtered_df2 = df  # All patients

        # Graph options for the second graph
        selected_graph2 = st.selectbox("Select second graph", graph_options, index=1)

        # Second Graph Visualization based on filtered data
        if selected_graph2 == 'Gender Distribution':
            fig2 = plot_gender_distribution(filtered_df2)
            st.plotly_chart(fig2, use_container_width=True)

        elif selected_graph2 == 'Age Distribution of Patients':
            fig2 = plot_age_distribution(filtered_df2)
            st.plotly_chart(fig2, use_container_width=True)

        elif selected_graph2 == 'Heart Attack Risk by Gender':
            fig2 = plot_risk_by_gender(filtered_df2)
            st.plotly_chart(fig2, use_container_width=True)

        elif selected_graph2 == 'Distribution of Heart Attacks':
            fig2 = plot_risk_distribution(filtered_df2)
            st.plotly_chart(fig2, use_container_width=True)

        elif selected_graph2 == 'Age Distribution by Gender and Heart Attack Status':
            fig2 = plot_age_distribution_by_gender_and_heart_attack(filtered_df2)
            st.plotly_chart(fig2, use_container_width=True)

        elif selected_graph2 == 'Heart Attack Distribution by Age Group and Gender':
            fig2 = plot_heart_attack_by_age_group_and_gender(filtered_df2)
            st.plotly_chart(fig2, use_container_width=True)


#####################################################################################
### Expander for Feature Exploration                                              ###
#####################################################################################

# Expander for Feature Exploration
with st.expander("Feature Exploration", expanded=True):
    st.subheader("Feature Exploration")
    st.info("This section provides a quick summary of key metrics for numerical features in the dataset. Select a patient group, feature, and visualization type.")

    # New row for radio button (left) and feature selection (right)
    row1_col1, row1_col2 = st.columns([1, 2])

    # Radio button for filtering data on the left
    with row1_col1:
        patient_filter_feature = st.radio(
            "Select patient group:",
            ("All Patients", "Only Heart Attack Patients", "Only No Heart Attack Patients")
        )

        # Apply the filtering logic based on the selected option
        if patient_filter_feature == "Only Heart Attack Patients":
            filtered_feature_df = df[df['heart_disease_diagnosis'] == True]
        elif patient_filter_feature == "Only No Heart Attack Patients":
            filtered_feature_df = df[df['heart_disease_diagnosis'] == False]
        else:
            filtered_feature_df = df

    st.divider()
    # Feature selection dropdown on the right
    with row1_col2:
        numerical_features = filtered_feature_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        selected_feature = st.selectbox("Choose a feature to analyze:", numerical_features)

    # Show two columns for tabular data and visualization
    col1, col2 = st.columns(2)

    # Column 1: Display tabular data of the selected feature
    with col1:
        st.write(f"**Tabular Data for {selected_feature}**")
        summary = (filtered_feature_df[[selected_feature]].describe().transpose())
        st.dataframe(summary)

        # Extract summary statistics
        instances = int(summary['count'].values[0])
        average = summary['mean'].values[0]
        min_value = summary['min'].values[0]
        max_value = summary['max'].values[0]

        # Determine the patient group based on the radio button selection
        if patient_filter_feature == "Only Heart Attack Patients":
            population = "patients who had a heart attack"
        elif patient_filter_feature == "Only No Heart Attack Patients":
            population = "patients who did not have a heart attack"
        else:
            population = "all patients"

        # Display a summary text underneath the table
        st.text_area(
            "Summary",
            value=f"For {population}, there were {instances} instances used to train the data for the feature '{selected_feature}'. "
                f"The average value in the data is {average:.2f}, with a minimum of {min_value} and a maximum of {max_value}."
        )

    # Column 2: Visualization options for the filtered data
    with col2:
        st.write(f"**Visualization for {selected_feature}**")
        # Radio button for visualization type
        analysis_type = st.radio("Choose visualization type:", ["Distribution", "Box Plot"])

        if analysis_type == "Distribution":
            # Distribution plot of the selected feature
            fig = px.histogram(filtered_feature_df, x=selected_feature, nbins=20, title=f'Distribution of {selected_feature}')
            fig.update_layout(xaxis_title=selected_feature, yaxis_title='Frequency')
            st.plotly_chart(fig, use_container_width=True)

        elif analysis_type == "Box Plot":
            # Box plot of the selected feature
            fig = px.box(filtered_feature_df, y=selected_feature, title=f'Box Plot of {selected_feature}')
            fig.update_layout(yaxis_title=selected_feature)
            st.plotly_chart(fig, use_container_width=True)
