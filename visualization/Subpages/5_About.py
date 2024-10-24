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

# Overview Section
st.header("Overview")
st.markdown(
    """
    **_CardioVision_** is an advanced medical dashboard specifically designed to assist **cardiologists** in predicting heart attack risks and providing **real-time**, **data-driven** insights into a patient’s cardiovascular health. Leveraging a combination of **key health metrics** such as **chest pain type**, **cholesterol levels**, **heart rate**, and **lifestyle factors**, CardioVision supports more accurate **risk assessment**.

    With its user-friendly interface and powerful analytics, **CardioVision** enhances decision-making and facilitates **holistic** patient care.
    """
)
        
with st.expander("❗Medical Problem and End Users", expanded=True):
    col1, col2 = st.columns(2)

    # Left column for Identified Medical Problem
    with col1:
        st.markdown("""
        ### **Identified Medical Problem**
        Heart attacks are a major cause of death in Sweden and many parts of the world. 
        In 2022, Sweden alone reported over 23,000 cases of AMI. Early detection and prevention of heart attack risk can save lives and reduce healthcare costs.
        CardioVision applies AI and machine learning to improve heart attack risk prediction, helping healthcare providers make more timely and informed decisions for patient care.
        """)          

    # Right column for End Users
    with col2:
        st.markdown("""
        ### **End Users**
        CardioVision is designed for clinicians focusing on predicting heart attack risk in patients who do not show signs of an acute heart attack on ECG or through elevated troponin levels. 
        It helps clinicians identify high-risk patients by analyzing factors such as age, cholesterol, and blood pressure, and assists in reducing risk through early prevention strategies.
        """)

    # References in two columns
    st.markdown("### **References**")
    ref_col1, ref_col2 = st.columns(2)

    # Left column for two references
    with ref_col1:
        st.markdown("""
        - World Health Organization. Cardiovascular diseases (CVDs). *WHO*, 2021.
        - National Board of Health and Welfare. Statistics on Myocardial Infarctions 2022. *Socialstyrelsen*, 2023.
        """)

    # Right column for two references
    with ref_col2:
        st.markdown("""
        - Oude Wolcherink MJ et al. Early Detection of Cardiovascular Disease: *PharmacoEconomics*, 2023.
        - Rojek I et al. AI-Based Heart Attack Risk Prediction: *Electronics*, 2024.
        """)


# Features Section
st.header("Key Features")
cols = st.columns(3)

# Feature 1: Patient Management
with cols[0]:
    st.html(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{patient_management_image_base64}" 
             alt="Patient Management" 
             style="width: 190px; height: auto;" />
        <h5>Patient Management</h5>
        <p>Easily access patient details and history.</p>
    </div>
    """
    )

# Feature 2: Risk Assessment
with cols[1]:
    st.html(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{risk_prediction_image_base64}" 
             alt="Heart Attack Risk Assessment" 
             style="width: 190px; height: auto;" />
        <h5>Heart Attack Risk Assessment</h5>
        <p>Assess patients' heart attack risk & risk factors using advanced algorithms.</p>
    </div>
    """
    )

# Feature 3: Diagnostic Insights
with cols[2]:
    st.html(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{xai_image_base64}" 
             alt="Diagnostic Insights" 
             style="width: 190px; height: auto;" />
        <h5>Diagnostic Insights</h5>
        <p>Generate insights from department patient history.</p>
    </div>
    """
    )




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