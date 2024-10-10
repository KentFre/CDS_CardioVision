# This file will cover the about tab

import streamlit as st

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

# Create two columns with specified ratios
r1, r2 = st.columns((0.1, 1))

# Display the logo in the first column
r1.image("visualization/assets/CardioVision_icon.png", width=60)

# Set the title in the second column
r2.title("About")

# Overview Section
st.header("Overview")
st.write("A medical dashboard for cardiologists to predict heart attack risk provides real-time, data-driven insights into a patient’s cardiovascular health. It integrates various health metrics such as blood pressure, cholesterol levels, heart rate, and lifestyle factors like smoking and exercise habits.")
st.button("Learn More", key="feature1")
        


# Features Section
st.header("Key Features")
cols = st.columns(3)

# Feature 1: Patient Management
with cols[0]:
    st.image("https://img.icons8.com/ios-filled/80/4CAF50/user-male.png", width=80)  # Patient Management icon
    st.markdown("<h5>Patient Management</h5>", unsafe_allow_html=True)
    st.write("Easily manage and access patient details and history.")
    st.button("Learn More", key="feature2")

# Feature 2: Risk Assessment
with cols[1]:
    st.image("https://img.icons8.com/ios-filled/80/2196F3/heart.png", width=80)  # Heart attack risk assessment icon
    st.markdown("<h5>Heart Attack Risk Assessment</h5>", unsafe_allow_html=True)
    st.write("Assess patients' risk factors using advanced algorithms.")
    st.button("Learn More", key="feature3")

# Feature 3: Diagnostic Insights
with cols[2]:
    st.image("https://img.icons8.com/ios-filled/80/FF9800/analysis.png", width=80)  # Diagnostic insights icon
    st.markdown("<h5>Diagnostic Insights</h5>", unsafe_allow_html=True)
    st.write("Generate insights from patient history and test results.")
    st.button("Learn More", key="feature4")

# Meet the Team Section
st.header("Meet the Team")
team_members = [
    {"name": "Dr. Emily Stone", "role": "Lead Cardiologist", "image": "https://via.placeholder.com/50"},
    {"name": "John Doe", "role": "Data Scientist", "image": "https://via.placeholder.com/50"},
    {"name": "Jane Smith", "role": "UI/UX Designer", "image": "https://via.placeholder.com/50"},
]

# Display Team Members
team_cols = st.columns(len(team_members))
for idx, member in enumerate(team_members):
    with team_cols[idx]:
        st.image(member["image"], width=50)
        st.markdown(f"<h6>{member['name']}</h6>", unsafe_allow_html=True)
        st.write(member["role"])

# Contact Section
st.header("Contact Us")
contact_info = """
- Email: [support@example.com](mailto:support@example.com)
- Phone: +1 (123) 456-7890
"""
st.markdown(contact_info)

# Feedback Button
st.header("We Value Your Feedback")
if st.button("Give Feedback"):
    st.write("Thank you for your feedback!")

# Future Enhancements Section
st.header("Future Enhancements")
st.write("Stay tuned for advanced analytics and features to enhance patient care!")
st.button("Learn More", key="feature5")
