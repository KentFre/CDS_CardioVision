"""
model_utils.py
--------------
This module provides utility functions for data preprocessing and machine learning model usage.

"""

# Import libraries
import pickle
import pandas as pd
import numpy as np

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
def process_and_predict(preprocessor, model, json_file):
    try:
        # Load JSON file
        data = pd.read_json(json_file)
        
        # Extract data from nested JSON structure
        try:
            personal_data = data['PersonalData']
            vital_parameters = data['VitalParameters']
            laboratory_values = data['LaboratoryValues']
            ecg_results = data['ECGResults']
            symptoms_observations = data['SymptomsObservations']
            social_factors = data['SocialFactors']
        except KeyError:
            raise ValueError("JSON structure is incorrect or missing required sections.")
        
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
            'resting_ecg_results': ecg_results.get('resting_ecg_results')
        }
        
        # Check for missing values
        if any(value is None for value in flat_data.values()):
            missing_fields = [key for key, value in flat_data.items() if value is None]
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")
        
        # Convert to DataFrame for processing
        input_df = pd.DataFrame([flat_data])
        
        # Preprocess the data
        processed_data = preprocessor.transform(input_df)
        
        # Get column names for transformed data
        feature_names = preprocessor.get_feature_names_out()
        
        # Convert transformed data to DataFrame
        transformed_df = pd.DataFrame(processed_data, columns=feature_names)
        
        # Set the display option for maximum columns
        pd.set_option('display.max_columns', None)
        
        # Print the column names and transformed data
        print("Transformed Data with Column Names:")
        print(transformed_df)
        
        # Make a prediction
        prediction = model.predict(transformed_df)
        
        return prediction

    except ValueError as e:
        # Handle validation errors or other exceptions
        return str(e)
    except Exception as e:
        # Handle any other unexpected errors
        return f"An error occurred: {e}"
