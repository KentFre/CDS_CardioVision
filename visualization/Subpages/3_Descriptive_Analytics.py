import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# Doctor's profile section
doctor_image_url = "https://via.placeholder.com/40"
doctor_name = "Dr. Emily Stone"

# Creating a container for the search bar and doctor profile
with st.container():
    col1, col2 = st.columns([2, 1])  # Adjust column ratio for search and profile

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

# Sample data for demonstration purposes
data = {
    'Gender': ['Male', 'Female', 'Female', 'Male', 'Male', 'Female'],
    'Age': [45, 50, 34, 67, 29, 58],
    'Heart Attack Risk': [True, False, True, True, False, False]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Descriptive statistics calculations
total_patients = len(df)
total_risk_patients = df['Heart Attack Risk'].sum()
average_age = df['Age'].mean()

# Gender distribution
gender_distribution = df['Gender'].value_counts()

# Streamlit layout
st.title("Descriptive Analytics ")

m1, m2, m3 = st.columns((1,1,1))

# Display empty columns for formatting
m1.metric(label='Number of Patients', value=total_patients)
m2.metric(label='Patients with Heart Attack Risk', value=total_risk_patients)
m3.metric(label='Average Age of Patients', value=round(average_age, 2))


# Now, let's add graphs in a column layout for visualizations
g1, g2 = st.columns((1, 1))

# Gender Distribution Pie Chart using Plotly
fig1 = px.pie(df, names='Gender', title='Gender Distribution', template='seaborn')
fig1.update_traces(marker=dict(colors=['skyblue', 'lightcoral']))
fig1.update_layout(title_x=0.1, margin=dict(l=0, r=0, b=10, t=30), showlegend=True)
g1.plotly_chart(fig1, use_container_width=True)

# Age Distribution Histogram using Plotly
fig2 = px.histogram(df, x='Age', nbins=10, title='Age Distribution of Patients', template='seaborn')
fig2.update_traces(marker_color='#2a9d8f')
fig2.update_layout(
    title_x=0.1,
    margin=dict(l=0, r=0, b=10, t=30),
    xaxis_title='Age of Patients',     
    yaxis_title='Number of Patients'   
)
g2.plotly_chart(fig2, use_container_width=True)


h1, h2 = st.columns((1, 1))

# Heart Attack Risk by Gender Bar Chart using Plotly
risk_by_gender = df[df['Heart Attack Risk'] == True]['Gender'].value_counts()
risk_df = pd.DataFrame({'Gender': risk_by_gender.index, 'Count': risk_by_gender.values})
fig3 = px.bar(risk_df, x='Gender', y='Count', title='Heart Attack Risk by Gender', template='seaborn')
fig3.update_traces(marker_color='#264653')
fig3.update_layout(
    title_x=0.1,
    margin=dict(l=0, r=0, b=10, t=30),
    xaxis_title='Gender',             # X-axis label
    yaxis_title='Number of Patients at Risk'  # Y-axis label
)
h1.plotly_chart(fig3, use_container_width=True)

# User selection for features to visualize
st.subheader("Data Visualisation")

# Options for the user to choose from
visual_options = ['Gender Distribution', 'Age Distribution', 'Heart Attack Risk by Gender']
selected_features = st.multiselect('Choose the visualizations you want to see:', visual_options)

