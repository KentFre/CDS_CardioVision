import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state['doctor_image_base64']

with st.container():
    r1, r2 = st.columns([2, 1])

    with r1:
        # Display the title in the first column
        r1.title("Technical Information")

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

# Machine Learning & Neural Networks Section
st.header("Machine Learning & Neural Networks")
st.markdown(
    """
    **Machine Learning (ML)** is a field of artificial intelligence that enables computers to learn from data without being explicitly programmed. In the context of CardioVision, ML helps identify patterns in cardiovascular health data, improving prediction accuracy for heart attack risk.

    **Neural Networks (NN)**, particularly in **deep learning**, are models inspired by the structure of the human brain. These networks consist of multiple layers of neurons that process input data, identifying complex patterns and making predictions. Neural networks are highly effective in medical applications where subtle data patterns can inform critical decisions.

    In our model training, we focused on **maximizing recall**. Recall is critical in this context because we aim to identify **as many patients at risk of cardiac arrest as possible**, even at the cost of a higher number of false positives. By prioritizing recall, we ensure that fewer patients with a real risk of cardiac arrest are missed.
    """
)

# Model Performance Justification in two columns inside an expander
with st.expander("Model Performance Justification"):
    st.subheader("Model Performance Justification")

    # Create two columns, with the left column being 1.5 times larger than the right column
    col1, col2 = st.columns([1, 1])

    # Define performance data for the table
    performance_data = {
        "Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "AUC", "Training Time", "Prediction Time"],
        "Value": [0.798, 0.789, 0.862, 0.824, 0.792, 57, 0.18],
        "Justification": [
            "Overall correctness of the model's predictions.",
            "Proportion of true positive predictions among all positive predictions.",
            "Critical measure ensuring most at-risk patients are identified, even at the cost of false positives.",
            "Balance between precision and recall, ensuring good overall performance.",
            "Ability to distinguish between patients at risk and not at risk.",
            "Duration it took to train the model with the existing data.",
            "Duration each new prediction takes."
        ]
    }

    # Display the table in the left column
    with col1:
        df_performance = pd.DataFrame(performance_data)
        df_performance['Value'] = df_performance['Value'].apply(lambda x: f"{x:.3f}")
        st.table(df_performance)

    # Explain the performance results in the right column
    with col2:
        st.markdown(
            """
            The model has performed very well in identifying heart attack risk patients, especially with a **recall** of **0.86**. This is crucial because our priority is ensuring that nearly all high-risk patients are correctly flagged, even at the cost of false positives. The balance between recall and precision is reflected in the **F1 Score** of **0.82**, indicating robust overall performance.

            Furthermore, the **AUC** score of **0.79** demonstrates the model's strong ability to differentiate between at-risk and non-at-risk patients, giving us confidence in the model's effectiveness.

            The model took **57 seconds** to train, and each prediction takes an average of **0.18 seconds**, making it efficient for clinical use in real-time scenarios.
            """
        )
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

# Expander for Dataset Details
with st.expander("View Dataset Details"):
    st.subheader("Selected Datasets")
    st.write("We have carefully selected **feature rich** datasets that have a very **high quality**, are **reliable** and known to contain valuable information.")

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