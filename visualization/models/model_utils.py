import os
import streamlit as st
import pandas as pd
import pickle
from tensorflow.keras.models import load_model as keras_load_model
import tensorflow as tf
import shap
import numpy as np


# Function to load the preprocessor
def load_preprocessor(path):
    with open(path, "rb") as file:
        preprocessor = pickle.load(file)
    return preprocessor

# Function to load the model (handles both .h5 and .pkl)
def load_model(base_path):
    # Define the paths for both the .h5 (Keras) and .pkl (Pickle) models
    keras_model_path = base_path + ".h5"
    pickle_model_path = base_path + ".pkl"
    
    # Check if the Keras model exists
    if os.path.exists(keras_model_path):
        # Load the Keras model
        model = keras_load_model(keras_model_path)
        print(f"Loaded Keras model from {keras_model_path}")
    elif os.path.exists(pickle_model_path):
        # Load the model using pickle if the Keras model does not exist
        with open(pickle_model_path, "rb") as file:
            model = pickle.load(file)
        print(f"Loaded Pickled model from {pickle_model_path}")
    else:
        raise FileNotFoundError(f"No model found at {keras_model_path} or {pickle_model_path}")
    
    return model

# Process, validate, and predict function
def process_and_predict(preprocessor, model):
    try:
        # Access patient data from session state
        patient_data = st.session_state.get('patient_data', {})
        
        # Safely access each nested dictionary
        personal_data = patient_data.get('PatientInfo', {})
        symptoms_observations = patient_data.get('SymptomsObservations', {})
        vital_parameters = patient_data.get('VitalParameters', {})
        laboratory_values = patient_data.get('LaboratoryValues', {})
        ecg_results = patient_data.get('ECGResults', {})
        social_factors = patient_data.get('SocialFactors', {})
        
        # Flatten the extracted data into a dictionary
        flat_data = {
            'age': personal_data.get('age'),
            'gender': personal_data.get('gender'),
            'chest_pain_type': symptoms_observations.get('chest_pain_type'),
            'family_history_cad': personal_data.get('family_history_cad'),
            'resting_heart_rate': vital_parameters.get('resting_heart_rate'),
            'max_heart_rate': vital_parameters.get('max_heart_rate'),
            'has_hypertension': vital_parameters.get('has_hypertension'),
            'exercise_induced_angina': symptoms_observations.get('exercise_induced_angina'),
            'serum_cholesterol': laboratory_values.get('serum_cholesterol'),
            'high_fasting_blood_sugar': laboratory_values.get('high_fasting_blood_sugar'),
            'st_depression': laboratory_values.get('st_depression'),
            'cigarettes_per_day': social_factors.get('cigarettes_per_day'),
            'years_smoking': social_factors.get('years_smoking'),
            'resting_ecg_results': ecg_results.get('resting_ecg_results'),
            'family_history_cad': social_factors.get('family_history_cad')
        }

        # Check for missing values
        missing_fields = [key for key, value in flat_data.items() if value is None]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Convert to DataFrame for processing
        input_df = pd.DataFrame([flat_data])
        
        # Preprocess the data
        processed_data = preprocessor.transform(input_df)
        
        # Convert transformed data to DataFrame with feature names
        feature_names = preprocessor.get_feature_names_out()
        transformed_df = pd.DataFrame(processed_data, columns=feature_names)
        
        # Make a prediction
        prediction = model.predict(transformed_df)
        
        return prediction[0], transformed_df

    except ValueError as e:
        # Handle validation errors
        return None, str(e)
    except Exception as e:
        # Handle other unexpected errors
        return None, f"An error occurred: {e}"


def calculate_risk(preprocessor, model):
    prediction, transformed_df = process_and_predict(preprocessor, model)

    if prediction is not None:
        risk_level = "High Risk" if prediction > 0.5 else "Low Risk"

        # Convert transformed_df to NumPy array for the SHAP explainer
        transformed_array = transformed_df.to_numpy()

        # Use a background dataset of 40 random samples from the df in session state
        background_data = st.session_state['df'].sample(40, random_state=42)
        
        # Drop the target column (e.g., 'Has_heart_disease') if it's present
        if 'Has_heart_disease' in background_data.columns:
            background_data = background_data.drop(columns=['Has_heart_disease'])
        
        background_data_np = background_data.to_numpy().astype(np.float32)

        # Detect if the model is a Keras model
        if isinstance(model, tf.keras.Model):
            # Use DeepExplainer for Keras models
            explainer = shap.DeepExplainer(model, background_data_np)
            shap_values = explainer.shap_values(transformed_array, check_additivity=False)
        else:
            # Use TreeExplainer for tree-based models or KernelExplainer for others
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(transformed_array)

        # Convert expected_value Tensor to a scalar if needed
        expected_value_scalar = explainer.expected_value.numpy()[0] if isinstance(explainer.expected_value, tf.Tensor) else explainer.expected_value

        # Return risk level and SHAP values for use in the Streamlit app
        return f"{risk_level}", shap_values, expected_value_scalar, prediction
    else:
        return "", "", None
    

# Function to generate interpretation text based on SHAP values
def interpret_shap_values(shap_values_patient, feature_names, expected_value):
    # Explanation of color coding in the SHAP plot
    interpretation_text = ""

    # Get the SHAP values for the patient
    shap_values_flat = shap_values_patient[0]

    # Create a DataFrame to sort features by SHAP values
    shap_df = pd.DataFrame({
        'Feature': feature_names,
        'SHAP Value': shap_values_flat
    })

    # Sort features by SHAP values
    positive_contributors = shap_df[shap_df['SHAP Value'] > 0].sort_values(by='SHAP Value', ascending=False).head(3)
    negative_contributors = shap_df[shap_df['SHAP Value'] < 0].sort_values(by='SHAP Value', ascending=True).head(3)

    # Interpret based on the overall SHAP value (risk threshold at 0.5)
    if expected_value > 0.5:
        # High risk interpretation
        interpretation_text += "- These features **increased the risk**:\n"
        for index, row in positive_contributors.iterrows():
            interpretation_text += f"  - **{row['Feature']}**: contributed a SHAP value of {row['SHAP Value']:.4f}\n"

        if not negative_contributors.empty:
            interpretation_text += "\n- While these features **reduced the risk**, they were not enough to bring the risk to a low level:\n"
            for index, row in negative_contributors.iterrows():
                interpretation_text += f"  - **{row['Feature']}**: reduced the risk with a SHAP value of {row['SHAP Value']:.4f}\n"

    else:
        # Low risk interpretation
        interpretation_text += "- These features **reduced the risk** for a heart attack:\n"
        for index, row in negative_contributors.iterrows():
            interpretation_text += f"  - **{row['Feature']}**: contributed a SHAP value of {row['SHAP Value']:.4f}\n"

        if not positive_contributors.empty:
            interpretation_text += "\n- While these features **increased the risk**, they were not enough to result in a high-risk prediction:\n"
            for index, row in positive_contributors.iterrows():
                interpretation_text += f"  - **{row['Feature']}**: increased the risk with a SHAP value of {row['SHAP Value']:.4f}\n"

    return interpretation_text
