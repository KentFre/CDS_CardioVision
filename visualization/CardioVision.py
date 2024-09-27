

import streamlit as st

# Set the page configuration

st.set_page_config(
    page_title="CardioVision",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="assets/CardioVision_Icon.png",
)



patient_details_page = st.Page("pages/1_Patient_Details.py", title = "Patient Details", icon=":material/dashboard:")
risk_assessment_page = st.Page("pages/2_Risk_Assessment.py", title="Risk Assessment", icon=":material/dashboard:", default=True)
diagnostic_page = st.Page("pages/3_Diagnostic_Analysis.py", title="Diagnostic Analysis", icon=":material/dashboard:")
about_page = st.Page("pages/4_About.py", title="About", icon=":material/dashboard:")

pg = st.navigation(
    {
        "Patient": [patient_details_page],
        "Insights": [risk_assessment_page, diagnostic_page],
        "Others": [about_page],
    }
    
)

pg.run()


