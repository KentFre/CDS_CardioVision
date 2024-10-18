import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Function to load the preprocessor
def load_preprocessor(path):
    with open(path, "rb") as file:
        preprocessor = pickle.load(file)
    return preprocessor

# Function to load the model
def load_model(path):
    with open(path, "rb") as file:
        model = pickle.load(file)
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
        
        # Generate an explanation for the prediction
        explanation = "The prediction for heart attack risk is based on factors such as age, cholesterol level, and ECG results."
        
        return prediction[0], explanation

    except ValueError as e:
        # Handle validation errors
        return None, str(e)
    except Exception as e:
        # Handle other unexpected errors
        return None, f"An error occurred: {e}"

# Function to calculate risk
def calculate_risk(preprocessor, model):
    prediction, explanation = process_and_predict(preprocessor, model)
    if prediction is not None:
        risk_level = "High Risk" if prediction == 1 else "Low Risk"
        return f"{risk_level}", explanation
    else:
        return explanation, ""
