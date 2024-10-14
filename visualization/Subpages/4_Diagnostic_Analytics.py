import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

doctor_name = "Dr. Emily Stone"
doctor_image_base64 = st.session_state['doctor_image_base64']

with st.container():
    r1, r2 = st.columns([2, 1])

    with r1:
        # Display the title in the first column
        r1.title("Diagnostic Analytics")

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


def load_data():
    try:
        data = pd.read_csv('../visualization/assets/heart_disease_data.csv')  # Relative path for portability
        return data
    except FileNotFoundError:
        st.error("Error loading dataset. Please check the file path.")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Load the dataset
data = load_data()

# Check if data was loaded
if not data.empty:
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Select only numerical columns for correlation matrix
    numerical_cols = df.select_dtypes(include=['float64', 'int64'])

    if not numerical_cols.empty:
        # 1. Correlation Heatmap
        st.subheader("Correlation Heatmap")
        correlation_matrix = numerical_cols.corr()  # Calculate the correlation matrix

        # Create a heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
        plt.title('Correlation Heatmap')
        st.pyplot(plt)
        plt.clf()  # Clear the plot to avoid overlap

        # 2. Feature Selection for Custom Correlation
        st.subheader("Custom Correlation Analysis")

        # Allow the user to select two features
        features = numerical_cols.columns.tolist()
        feature_1 = st.selectbox('Choose the first feature', features)
        feature_2 = st.selectbox('Choose the second feature', features)

        # Show the correlation between the selected features
        if feature_1 != feature_2:
            correlation_value = df[feature_1].corr(df[feature_2])
            st.write(f"The correlation between {feature_1} and {feature_2} is: {correlation_value:.2f}")

            # 3. Scatter plot to visualize the correlation
            st.subheader(f"Scatter Plot: {feature_1} vs {feature_2}")
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=df[feature_1], y=df[feature_2])
            plt.xlabel(feature_1)
            plt.ylabel(feature_2)
            st.pyplot(plt)
            plt.clf()  # Clear the plot after displaying
        else:
            st.warning("Please select two different features.")

        # 4. Pairplot Analysis
        st.subheader("Pairplot Analysis")

        # Explanation of the pairplot analysis
        st.markdown("""
        The **Pairplot Analysis** provides a visual exploration of relationships between key numerical features. 
        Each plot compares two variables, revealing trends and potential correlations, while the diagonal shows the distribution of individual features. 
        The plots are color-coded based on the presence or absence of heart disease, allowing you to easily observe how different features interact and how they differ between patient groups. 
        This helps identify patterns that may be relevant for diagnosis and further analysis.
        """)

        # Check if 'heart_disease_diagnosis' column exists
        if 'heart_disease_diagnosis' in df.columns:
            numerical_features = numerical_cols.columns.tolist()
            
            # Create the pairplot
            plt.figure()
            sns.pairplot(df[numerical_features + ['heart_disease_diagnosis']], hue='heart_disease_diagnosis')
            st.pyplot(plt)
            plt.clf()  # Clear the plot after displaying
        else:
            st.warning("The 'heart_disease_diagnosis' column is not available in the dataset.")

    else:
        st.warning("No numerical columns available for correlation analysis.")
else:
    st.error("Dataset could not be loaded.")