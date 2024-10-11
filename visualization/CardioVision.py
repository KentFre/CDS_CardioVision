

import streamlit as st

# Set the page configuration

st.set_page_config(
    page_title="CardioVision",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="assets/CardioVision_icon.png",
)



patient_data_page = st.Page("Subpages/1_Patient_Data.py", title="Patient Data", icon=":material/dashboard:", default=True)
risk_assessment_page = st.Page("Subpages/2_Risk_Calculation.py", title="Risk Calculation", icon=":material/dashboard:")

descriptive_analytics_page = st.Page("Subpages/3_Descriptive_Analytics.py", title="Descriptive Analytics", icon=":material/dashboard:")
diagnostic_analytics_page = st.Page("Subpages/4_Diagnostic_Analytics.py", title="Diagnostic Analytics", icon=":material/dashboard:")

about_page = st.Page("Subpages/5_About.py", title="About", icon=":material/dashboard:")

pg = st.navigation(
    {
        "Patient": [patient_data_page, risk_assessment_page],
        "Department Insights": [ descriptive_analytics_page, diagnostic_analytics_page],
        "Others": [about_page],
    }
    
)

pg.run()