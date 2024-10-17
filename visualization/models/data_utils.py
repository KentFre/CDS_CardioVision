# data_utils.py
import pandas as pd

# Load and process data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to calculate summary statistics
def get_summary_statistics(df):
    total_patients = len(df)
    total_risk_patients = df['heart_disease_diagnosis'].sum()
    average_age = df['age'].mean()
    return total_patients, total_risk_patients, round(average_age, 2)

# Function to get gender distribution
def get_gender_distribution(df):
    return df['gender'].value_counts()

# Other data processing functions as needed...
