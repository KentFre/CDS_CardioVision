import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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


def load_data():
    data = pd.read_csv('C:\\Users\\Admin\\OneDrive\\Documents\\GitHub\\CDS_CardioVision\\visualization\\assets\\heart_disease_data.csv')
    return data

# Load the dataset
data = load_data()

# Convert to DataFrame
df = pd.DataFrame(data)

# Title for the diagnostic analytics page
st.title("Diagnostic Analytics")

# Select only numerical columns for correlation matrix
numerical_cols = df.select_dtypes(include=['float64', 'int64'])

# 1. Correlation Heatmap
correlation_matrix = numerical_cols.corr()  # Calculate the correlation matrix

# Create a heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt='.2f', linewidths=0.5)
plt.title('Correlation Heatmap')
st.pyplot(plt)

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

else:
    st.warning("Please select two different features.")