import streamlit as st

# Set the page configuration
st.set_page_config(
    page_title="CardioVision",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="👋",
)

risk_stratification_page = st.Page("pages/1_Risk_Stratification.py", title="Risk Stratification", icon=":material/dashboard:", default=True)
historic_page = st.Page("pages/2_Historic_Data.py", title="Historic Data", icon=":material/dashboard:")
diagnostic_page = st.Page("pages/3_Diagnostic_Analysis.py", title="Diagnostic Analysis", icon=":material/dashboard:")
about_page = st.Page("pages/4_About.py", title="About", icon=":material/dashboard:")

pg = st.navigation(
    {
        "Patient": [risk_stratification_page],
        "Historic Analysis": [historic_page, diagnostic_page],
        "Others": [about_page],
    }
)

pg.run()