# This file will cover the about tab

import streamlit as st
import streamlit.components.v1 as components
import base64

# Helper function to load and encode images as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the images
cardiologist_image = get_image_as_base64("assets/team/Cardiologist.svg")
data_scientist_image = get_image_as_base64("assets/team/Data_Scientist.svg")
architect_image = get_image_as_base64("assets/team/SW_Arch.svg")
uiuxdesigner_image = get_image_as_base64("assets/team/UIUX_Designer.svg")
mlengineer_image = get_image_as_base64("assets/team/ML_Engineer.svg")
xaiengineer_image = get_image_as_base64("assets/team/XAI_Engineer.svg")
patient_management_image_base64 = get_image_as_base64("assets/Patient_Management.svg")

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
st.write("A medical dashboard for cardiologists to predict heart attack risk provides real-time, data-driven insights into a patient’s cardiovascular health. It integrates various health metrics such as blood pressure, cholesterol levels, heart rate, and lifestyle factors like smoking and exercise habits.")
st.button("Learn More", key="feature1")
        


# Features Section
st.header("Key Features")
cols = st.columns(3)

# Feature 1: Patient Management
with cols[0]:
    st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/svg+xml;base64,{patient_management_image_base64}" alt="Patient Management" width="80"/>
        <h5>Patient Management</h5>
        <p>Easily manage and access patient details and history.</p>
    </div>
    """,
    unsafe_allow_html=True
    )

# Feature 2: Risk Assessment
with cols[1]:
    st.image("https://img.icons8.com/ios-filled/80/2196F3/heart.png", width=500)  # Heart attack risk assessment icon
    st.markdown("<h5>Heart Attack Risk Assessment</h5>", unsafe_allow_html=True)
    st.write("Assess patients' risk factors using advanced algorithms.")
    st.button("Learn More", key="feature3")

# Feature 3: Diagnostic Insights
with cols[2]:
    st.image("https://img.icons8.com/ios-filled/80/FF9800/analysis.png", width=80)  # Diagnostic insights icon
    st.markdown("<h5>Diagnostic Insights</h5>", unsafe_allow_html=True)
    st.write("Generate insights from patient history and test results.")
    st.button("Learn More", key="feature4")

# Streamlit app layout
st.title("Meet the Team")

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

# Feedback Button
st.header("We Value Your Feedback")
if st.button("Give Feedback"):
    st.write("Thank you for your feedback!")

# Future Enhancements Section
st.header("Future Enhancements")
st.write("Stay tuned for advanced analytics and features to enhance patient care!")
st.button("Learn More", key="feature5")
