#####################################################################################
# model_utils.py                                                                    #
#                                                                                   #
# This is a helper function collection for handling the machine learning models     #
#                                                                                   #
# - Prepare raw patient data for ml                                                 #
# - load ml models                                                                  #
# - predict target value for new data                                               #
# - generate SHAP values                                                            #
# - generate SHAP explanation and risk explanation                                  #
#####################################################################################

# Import needed libraries
import os
import streamlit as st
import pandas as pd
import pickle
from tensorflow.keras.models import load_model as keras_load_model
import tensorflow as tf
import shap
import numpy as np

# Dictionary to map original feature names to more understandable names
feature_name_mapping = {
    'age': 'Age',
    'gender': 'Gender',
    'chest_pain_type': 'Chest Pain Type',
    'family_history_cad': 'Family History of CAD',
    'resting_heart_rate': 'Resting Heart Rate',
    'max_heart_rate': 'Maximum Heart Rate',
    'has_hypertension': 'Has Hypertension',
    'exercise_induced_angina': 'Exercise-Induced Angina',
    'serum_cholesterol': 'Serum Cholesterol',
    'high_fasting_blood_sugar': 'High Fasting Blood Sugar',
    'st_depression': 'ST Depression',
    'cigarettes_per_day': 'Cigarettes per Day',
    'years_smoking': 'Years of Smoking',
    'resting_ecg_results': 'Resting ECG Results',
}

# Dictionary for feature units
feature_units = {
    'age': 'years',
    'resting_heart_rate': 'bpm',
    'max_heart_rate': 'bpm',
    'serum_cholesterol': 'mg/dL',
    'st_depression': 'mm',
    'cigarettes_per_day': 'cigarettes/day',
    'years_smoking': 'years'
}


#####################################################################################
### Import trained models                                                         ###
#####################################################################################

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


#####################################################################################
### Prepare Data, Predict Risk                                                    ###
#####################################################################################

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

        # Save the flattened dictionary to access it later
        st.session_state['flat_patient_data'] = flat_data

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
        pd.set_option('display.max_columns', None)  # To display all columns
        print(transformed_df)

        # Save the date to cache
        st.session_state['patient_data_processed'] = transformed_df
        
        # Make a prediction
        prediction = model.predict(transformed_df)
        
        return prediction[0], transformed_df

    except ValueError as e:
        # Handle validation errors
        return None, str(e)
    except Exception as e:
        # Handle other unexpected errors
        return None, f"An error occurred: {e}"

#####################################################################################
### Wrapper Calculate Risk Function                                               ###
#####################################################################################
def calculate_risk(preprocessor, model):
    prediction, transformed_df = process_and_predict(preprocessor, model)

    if prediction is not None:
        risk_level = "High Risk" if prediction > 0.5 else "Low Risk"

        # Convert transformed_df to NumPy array for the SHAP explainer
        transformed_array = transformed_df.to_numpy()

        # Use a background dataset of 200 random samples from the df in session state
        background_data = st.session_state['df'].sample(200, random_state=22)
        
        # Drop the target column (e.g., 'Has_heart_disease') if it's present
        if 'Has_heart_disease' in background_data.columns:
            background_data = background_data.drop(columns=['Has_heart_disease'])
        
        background_data_np = background_data.to_numpy().astype(np.float32)

        print("Model input shape:", model.input_shape)
        print("Transformed array shape:", transformed_array.shape)

        # Detect if the model is a Keras model
        if isinstance(model, tf.keras.Model):
            # Use DeepExplainer for Keras models
            explainer = shap.DeepExplainer(model, background_data_np)
            print(transformed_array)
            shap_values = explainer.shap_values(transformed_array, check_additivity=False)
        else:
            # Use TreeExplainer for tree-based models or KernelExplainer for others
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(transformed_array)

        feature_names = [
            'num__age', 'num__serum_cholesterol', 'num__max_heart_rate', 
            'num__st_depression', 'num__has_hypertension', 'num__cigarettes_per_day', 
            'num__years_smoking', 'num__resting_heart_rate', 'cat__gender_Female', 
            'cat__gender_Male', 'cat__chest_pain_type_Asymptomatic', 
            'cat__chest_pain_type_Atypical Angina', 'cat__chest_pain_type_Non-Anginal Pain', 
            'cat__chest_pain_type_Typical Angina', 'cat__resting_ecg_results_Left Ventricular Hypertrophy', 
            'cat__resting_ecg_results_Normal', 'cat__resting_ecg_results_ST-T Wave Abnormality', 
            'bin__high_fasting_blood_sugar', 'bin__exercise_induced_angina', 'bin__family_history_cad'
        ]
        # Flatten the SHAP values array (from (20, 1) to (20,))
        shap_values_flat = shap_values[0].flatten()

        # Create a DataFrame where each SHAP value corresponds to a feature name
        shap_df = pd.DataFrame([shap_values_flat], columns=feature_names)

        # Convert expected_value Tensor to a scalar if needed
        expected_value_scalar = explainer.expected_value.numpy()[0] if isinstance(explainer.expected_value, tf.Tensor) else explainer.expected_value

        # Return risk level and SHAP values for use in the Streamlit app
        return f"{risk_level}", shap_values, expected_value_scalar, prediction
    else:
        return "", "", None
    

#####################################################################################
### Explain SHAP values in human readable format                                  ###
#####################################################################################

# Function to generate interpretation text based on SHAP values
def interpret_shap_values(shap_values_patient, feature_names, expected_value):
    
    # Get raw and encoded patient data from session state
    patient_data = st.session_state['flat_patient_data']

    one_hot_mapping = {
        'gender': {
            'gender_F': 'Female',
            'gender_M': 'Male'
        },
        'chest_pain_type': {
            'cp_Asymptomatic': 'Asymptomatic',
            'cp_Atypical_Angina': 'Atypical Angina',
            'cp_Non_Anginal_Pain': 'Non-Anginal Pain',
            'cp_Typical_Angina': 'Typical Angina'
        },
        'resting_ecg_results': {
            'ecg_LVH': 'Left Ventricular Hypertrophy',
            'ecg_Normal': 'Normal',
            'ecg_ST_Abnormality': 'ST Abnormality'
        }
    }

    # Reset Text variable
    interpretation_text = ""

    # Get the SHAP values for the patient
    shap_values_flat = shap_values_patient[0]

    # Create a DataFrame to sort features by SHAP values
    shap_df = pd.DataFrame({
        'Feature': feature_names,
        'SHAP Value': shap_values_flat
    })

    # Define SHAP threshold for feature inclusion
    shap_threshold = 0.05

    # Filter features by SHAP values exceeding the threshold
    positive_contributors = shap_df[shap_df['SHAP Value'] > shap_threshold].sort_values(by='SHAP Value', ascending=False)
    negative_contributors = shap_df[shap_df['SHAP Value'] < -shap_threshold].sort_values(by='SHAP Value', ascending=True)

    # Helper function to get understandable feature name, actual value, and unit
    def get_feature_description(feature):
        if feature in one_hot_mapping['chest_pain_type']:
            # Get the human-readable name for chest pain type
            human_readable_name = "Chest Pain Type"
            actual_value = patient_data.get('chest_pain_type', "Unknown")
        elif feature in one_hot_mapping['resting_ecg_results']:
            # Get the human-readable name for resting ECG results
            human_readable_name = "ECG Result"
            actual_value = patient_data.get('resting_ecg_results', "Unknown")
        else:
            # Default to the feature itself if it's not in the one-hot mappings
            human_readable_name = feature_name_mapping.get(feature, feature)
            actual_value = patient_data.get(feature, "Unknown")

        unit = feature_units.get(feature, "")
        
        if human_readable_name in ['Chest Pain Type', 'ECG Result']:
            return f"The {human_readable_name} was {actual_value}"
        else:
            return f"The {human_readable_name} was {actual_value} {unit}".strip()

    # Begin the interpretation with an overview based on the risk level
    if expected_value > 0.5:
        # High-risk interpretation
        interpretation_text += "According to the input data, the features that raise the risk are more than those that reduce the risk.\n\n"
        
        if not positive_contributors.empty:
            interpretation_text += "- These features **increased the risk**:\n"
            for index, row in positive_contributors.iterrows():
                feature_description = get_feature_description(row['Feature'])
                interpretation_text += f"  - **{feature_description}**\n"
        else:
            interpretation_text += "- No patient data increased the risk significantly.\n"

        if not negative_contributors.empty:
            interpretation_text += "\n- These features **reduced the risk**, but they were not sufficient to lower it to a low risk:\n"
            for index, row in negative_contributors.iterrows():
                feature_description = get_feature_description(row['Feature'])
                interpretation_text += f"  - **{feature_description}**\n"
        else:
            interpretation_text += "- No patient data reduced the risk significantly.\n"

    else:
        # Low-risk interpretation
        interpretation_text += "According to the input data, the features that reduce the risk are more than those that raise the risk.\n\n"

        if not negative_contributors.empty:
            interpretation_text += "- These features **reduced the risk** for a heart attack:\n"
            for index, row in negative_contributors.iterrows():
                feature_description = get_feature_description(row['Feature'])
                interpretation_text += f"  - **{feature_description}**\n"
        else:
            interpretation_text += "- No patient data reduced the risk significantly.\n"

        if not positive_contributors.empty:
            interpretation_text += "\n- These features **increased the risk**, but they did not raise it to a high-risk level:\n"
            for index, row in positive_contributors.iterrows():
                feature_description = get_feature_description(row['Feature'])
                interpretation_text += f"  - **{feature_description}**\n"
        else:
            interpretation_text += "- No patient data increased the risk significantly.\n"

    return interpretation_text
