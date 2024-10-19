# This file will cover the about tab

import streamlit as st
import streamlit.components.v1 as components
import base64
import pandas as pd

# Helper function to load and encode images as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the images
cardiologist_image = get_image_as_base64("visualization/assets/team/Cardiologist.svg")
data_scientist_image = get_image_as_base64("visualization/assets/team/Data_Scientist.svg")
architect_image = get_image_as_base64("visualization/assets/team/SW_Arch.svg")
uiuxdesigner_image = get_image_as_base64("visualization/assets/team/UIUX_Designer.svg")
mlengineer_image = get_image_as_base64("visualization/assets/team/ML_Engineer.svg")
xaiengineer_image = get_image_as_base64("visualization/assets/team/XAI_Engineer.svg")
patient_management_image_base64 = get_image_as_base64("visualization/assets/Patient_Management.svg")
risk_prediction_image_base64 = get_image_as_base64("visualization/assets/Risk_Prediction.svg")
xai_image_base64 = get_image_as_base64("visualization/assets/XAI.svg")

doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state['doctor_image_base64']

with st.container():
    r1, r2 = st.columns([2, 1])

    with r1:
        # Display the title in the first column
        r1.title("About")

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

# Overview Section
st.header("Overview")
st.markdown(
    """
    **_CardioVision_** is an advanced medical dashboard specifically designed to assist **cardiologists** in predicting heart attack risks and providing **real-time**, **data-driven** insights into a patient’s cardiovascular health. Leveraging a combination of **key health metrics** such as **chest pain type**, **cholesterol levels**, **heart rate**, and **lifestyle factors**, CardioVision supports more accurate **risk assessment**.

    With its user-friendly interface and powerful analytics, **CardioVision** enhances decision-making and facilitates **holistic** patient care.
    """
)
        


# Features Section
st.header("Key Features")
cols = st.columns(3)

# Feature 1: Patient Management
with cols[0]:
    st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{patient_management_image_base64}" 
             alt="Patient Management" 
             style="width: 190px; height: auto;" />
        <h5>Patient Management</h5>
        <p>Easily access patient details and history.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Feature 2: Risk Assessment
with cols[1]:
    st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{risk_prediction_image_base64}" 
             alt="Heart Attack Risk Assessment" 
             style="width: 190px; height: auto;" />
        <h5>Heart Attack Risk Assessment</h5>
        <p>Assess patients' heart attack risk & risk factors using advanced algorithms.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Feature 3: Diagnostic Insights
with cols[2]:
    st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{xai_image_base64}" 
             alt="Diagnostic Insights" 
             style="width: 190px; height: auto;" />
        <h5>Diagnostic Insights</h5>
        <p>Generate insights from department patient history.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Columns for dataset statistics
col1, col2 = st.columns(2)



# Dataset Overview
st.header("Dataset Overview")
st.write("For CardioVision, we utilized the **Cleveland** and **Long Beach** datasets. These datasets were selected due to their completeness and relevance to cardiovascular health metrics.")

# Dataset Details Expander
with st.expander("Dataset Details and References"):
    
    st.subheader("Original Data Collection and Authors")
    st.markdown("""
    These datasets were collected as part of research studies conducted by the following institutions and authors:
    - **Cleveland Clinic Foundation**: Collected by Dr. Robert Detrano, M.D., Ph.D.
    - **Hungarian Institute of Cardiology**: Collected by Dr. Andras Janosi, M.D.
    - **University Hospital, Zurich, Switzerland**: Collected by Dr. William Steinbrunn, M.D.
    - **University Hospital, Basel, Switzerland**: Collected by Dr. Matthias Pfisterer, M.D.
    
    **Reference Publication**:
    Detrano, R., Janosi, A., Steinbrunn, W., Pfisterer, M., Schmid, J., Sandhu, S., et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease.* *American Journal of Cardiology, 64*(5):304-310.
    """)
    
    st.markdown("""
    > _Note: The authors have requested that any publications using this data include the names of the principal investigators responsible for the data collection at each institution._
    """)

# Expander for Dataset Details
with st.expander("View Dataset Details"):
    st.subheader("Selected Datasets")
    st.write("We have carefully selected **feature rich** datasets that have a very **quality**, are **reliable** and known to contain valuable information.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Cleveland Dataset")
        st.markdown("""
        - **Records:** 303
        - **Features:** 14
        - **Institution:** Cleveland Clinic Foundation
        """)

    with col2:
        st.subheader("Long Beach Dataset")
        st.markdown("""
        - **Records:** 200
        - **Features:** 14
        - **Institution:** Long Beach VA Medical Center
        """)

    st.subheader("Features Used in Analysis")

    # Define the features in categories for the table
    features_data = {
    "Category": ["Personal Data"] * 3 + ["Observations"] + ["Vital Parameters"] * 3 + ["Laboratory Values"] * 3 + ["ECG Results"] * 2 + ["Social Factors"] * 2,
    "Feature": [
        "Age", "Gender", "Family History of CAD",
        "Chest Pain Type", "Exercise-Induced Angina",
        "Resting Heart Rate", "Maximum Heart Rate", "Has Hypertension",
        "Serum Cholesterol", "High Fasting Blood Sugar", "ST Depression",
        "Resting ECG Results",
        "Cigarettes per Day", "Years Smoking"
    ],
    "Description": [
        "Age of the patient in years", "Gender (Male or Female)", "Family history of coronary artery disease",
        "Type of chest pain (e.g., Typical Angina)", "Occurrence of angina during exercise (Yes or No)",
        "Heart rate measured at rest (bpm)", "Maximum heart rate achieved during test (bpm)", "1 if the patient has hypertension, 0 otherwise",
        "Cholesterol levels in mg/dL", "Indicates high fasting blood sugar (Yes or No)", "Depression in the ST segment of the ECG",
        "Electrocardiographic results at rest (e.g., Normal)",
        "Number of cigarettes smoked per day", "Number of years the patient has been smoking"
    ]
    }

    # Create a DataFrame
    df_features = pd.DataFrame(features_data)

    # Display the DataFrame as a table
    st.table(df_features)


# Streamlit app layout
st.header("Meet the Team")

# Carousel HTML using SwiperJS with embedded images
components.html(f"""
<link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />
<div class="swiper-container" style="width: 80%; margin: auto;">
    <div class="swiper-wrapper">
        <!-- Team Member 1 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{cardiologist_image}" alt="Dr. Valentina OM" style="border-radius: 50%; width: 80px;">
            <h6>Dr. Valentina OM</h6>
            <p>Lead Cardiologist</p>
        </div>
        
        <!-- Team Member 2 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{data_scientist_image}" alt="Viktoriia O" style="border-radius: 50%; width: 80px;">
            <h6>Viktoriia O</h6>
            <p>Lead Data Scientist</p>
        </div>
        
        <!-- Team Member 3 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{architect_image}" alt="Kent F" style="border-radius: 50%; width: 80px;">
            <h6>Kent F</h6>
            <p>Lead SW Architect</p>
        </div>

        <!-- Team Member 4 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{uiuxdesigner_image}" alt="Jacky K" style="border-radius: 50%; width: 80px;">
            <h6>Jacky K</h6>
            <p>Lead UI/UX Designer</p>
        </div>

        <!-- Team Member 5 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{mlengineer_image}" alt="JiWei Y" style="border-radius: 50%; width: 80px;">
            <h6>JiWei Y</h6>
            <p>Lead ML Engineer</p>
        </div>

        <!-- Team Member 6 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{xaiengineer_image}" alt="Eranive M" style="border-radius: 50%; width: 80px;">
            <h6>Eranive M</h6>
            <p>Lead XAI Engineer</p>
        </div>
    </div>
    
    <!-- Add Pagination -->
    <div class="swiper-pagination"></div>

    <!-- Add Navigation Buttons -->
    <div class="swiper-button-next"></div>
    <div class="swiper-button-prev"></div>
</div>

<script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
<script>
    const swiper = new Swiper('.swiper-container', {{
        slidesPerView: 3,
        spaceBetween: 20,
        pagination: {{
            el: '.swiper-pagination',
            clickable: true,
        }},
        navigation: {{
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        }},
        loop: true
    }});
</script>
""", height=300)

# Contact Section
st.header("Contact Us")
contact_info = """
- Email: [support@example.com](mailto:support@example.com)
- Phone: +1 (123) 456-7890
"""
st.markdown(contact_info)

# Future Enhancements Section
st.header("Future Enhancements")
st.markdown(
    """
    **CardioVision** is constantly evolving with a vision to transform cardiovascular care through cutting-edge technology. In the future, we aim to:

    - **_Expand Predictive Capabilities_**: Enhancing the accuracy and scope of health predictions.
    - **_Deepen Personalization_**: Offering tailored insights that support individualized patient care.
    - **_Integrate Seamlessly with Emerging Technologies_**: Enabling better monitoring and data collection.
    - **_Enhance Visual Analytics_**: Providing more intuitive and engaging ways to understand patient health data.

    Stay tuned as we work to make **CardioVision** an even more powerful tool for improving patient outcomes.
    """
)
st.link_button(
    label="Visit our GitHub", 
    url="https://github.com/KentFre/CDS_CardioVision"
)

# Feedback Button Section
st.header("We Value Your Feedback")
st.write(
    """
    Your insights are crucial to us! Whether you have suggestions for improvements, have encountered any technical issues, 
    or simply want to share your experience using **CardioVision**, we’d love to hear from you.
    """
)

if st.button("Give Feedback"):
    # Display a modal for feedback
    @st.dialog("Your Feedback", width="large")
    def feedback_modal():
        st.write("Please let us know your thoughts and suggestions.")
        
        # Feedback text area
        feedback_text = st.text_area("Your feedback:")
        
        # Send button to submit feedback
        if st.button("Send"):
            if feedback_text:
                st.success("Thank you for your feedback!")
                st.session_state.feedback_sent = True
            else:
                st.warning("Please enter some feedback before sending.")
    
    # Call the modal function to open it
    feedback_modal()