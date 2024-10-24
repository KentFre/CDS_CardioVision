#####################################################################################
# 5_About.py                                                                        #
#                                                                                   #
# This is the streamlit page showing the information about CardioVision             #
#                                                                                   #
# - Get Information about the product and team                                      #
#####################################################################################

# Import needed libraries
import streamlit as st
import streamlit.components.v1 as components
import base64

#####################################################################################
### File preparation: Functions and Status checks and model import                ###
#####################################################################################

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


#####################################################################################
### Page Title and Doctor Info                                                    ###
#####################################################################################

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


#####################################################################################
### Product Overview, Intended User Group, Patient Group                          ###
#####################################################################################

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
        Cardiovascular disease (CVD) remains leading cause of death [1]. In Europe and Sweden, even though the incidence and mortality rates of ischemic heart disease (IHD) have been decreasing in recent decades, it remains a significant health issue [2][3]. Preventive measures like addressing risk factors are key in reducing the burden of this disease. Early identification of individuals at risk of having a heart attack allows for early intervention enabling to make informed decisions before a major cardiovascular event occurs. Furthermore, current evidence suggests that early CVD detection strategies are predominantly cost effective and may reduce CVD related costs compared with no early detection[4]. 
        """)          

    # Right column for End Users
    with col2:
        st.markdown("""
        ### **End Users**
        Our tool seeks to enhance and support clinicians who assess patients at risk of IHD in the cardiovascular centres in the hospital setting, providing them patient risk stratification so early personalised preventative measures and more targeted management strategies can be adopted. Patients identified as high risk can receive prompt interventions that reduce their chances of suffering a heart attack or consequences of a delayed diagnosis and intervention. 
        Our project aims to design and implement a web-based dashboard that will help clinicians to accurately predict the risk of heart attacks among patients before they are diagnosed with the disease (early detection) and enhance the focus towards the development of a prevention strategies based on modifiable factors supported by employment of artificial intelligence tools [5].
        """)

    # References in two columns
    st.markdown("### **References**")
    ref_col1, ref_col2 = st.columns(2)

    # Left column for two references
    with ref_col1:
        st.markdown("""
        - [1] World Health Organization. Cardiovascular diseases (CVDs). *WHO*, 2021.
        - [2] Vancheri F, Tate AR, Henein M, Backlund L, Donfrancesco C, Palmieri L, et al. Time trends in ischaemic heart disease incidence and mortality over three decades (1990–2019) in 20 Western European countries: systematic analysis of the Global Burden of Disease Study 2019. Eur J Prev Cardiol. 2022 Jan 1;29(2):396–403. 
        """)

    # Right column for two references
    with ref_col2:
        st.markdown("""
        - [3] National Board of Health and Welfare. Statistics on Myocardial Infarctions 2022. *Socialstyrelsen*, 2023.
        - [4] Oude Wolcherink MJ et al. Early Detection of Cardiovascular Disease: *PharmacoEconomics*, 2023.
        - [5] Rojek I et al. AI-Based Heart Attack Risk Prediction: *Electronics*, 2024.
        """)


#####################################################################################
### Feature Section                                                               ###
#####################################################################################
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



#####################################################################################
### Team Section                                                                  ###
#####################################################################################

# Streamlit app layout
st.header("Meet the Team")

# Carousel HTML using SwiperJS with embedded images
components.html(f"""
<link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.min.css" />
<div class="swiper-container" style="width: 80%; margin: auto;">
    <div class="swiper-wrapper">
        <!-- Team Member 1 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{cardiologist_image}" alt="Valentina OM" style="border-radius: 50%; width: 80px;">
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
            <img src="data:image/svg+xml;base64,{uiuxdesigner_image}" alt="Jackline K" style="border-radius: 50%; width: 80px;">
            <h6>Jacky K</h6>
            <p>Lead UI/UX Designer</p>
        </div>

        <!-- Team Member 5 -->
        <div class="swiper-slide" style="text-align: center;">
            <img src="data:image/svg+xml;base64,{mlengineer_image}" alt="Ji Wei Y" style="border-radius: 50%; width: 80px;">
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


#####################################################################################
### Contact Section                                                               ###
#####################################################################################

st.header("Contact Us")
contact_info = """
- Email: [support@example.se](mailto:support@example.se)
- Phone: +46 (123) 456-7890
"""
st.markdown(contact_info)


#####################################################################################
### Others  Section                                                               ###
#####################################################################################
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
st.header("We Value Your Feedback") # No we don't, as it goes nowhere ;-)
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