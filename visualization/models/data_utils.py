#####################################################################################
# data_utils.py                                                                     #
#                                                                                   #
# This is a helper function collection for handling the raw data and pdf generation #
#                                                                                   #
# - Load data from file path                                                        #
# - Calculate basic summaries                                                       #
#####################################################################################


import pandas as pd
# For PDF generation
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

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

# Define a custom PDF class to handle headers
class CustomPDF(FPDF):
    def __init__(self, patient_name, patient_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_name = patient_name
        self.patient_id = patient_id

    def header(self):
        # Add the logo on every page
        self.image(r'visualization\assets\CardioVision_Full_Logo.png', x=self.w * 0.3, y=10, w=self.w * 0.5)
        self.ln(30)  # Move to next section after the image

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doctor_name = "Dr. Emily Stone"

        # Set reduced font size for date and doctor's name
        self.set_font('Arial', '', 8)

        # Print date on the left and doctor name on the right
        self.cell(0, 8, txt=f"Date: {current_datetime}", ln=False, align='L')
        self.cell(0, 8, txt=f"Cardiologist: {doctor_name}", ln=True, align='R')

        # Draw a horizontal line
        self.set_draw_color(0, 0, 0)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)  # Line break after the line

        # Add patient name and ID on pages 2 and onward
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f"Patient Name: {self.patient_name} | Patient ID: {self.patient_id}", ln=True, align='C')
            self.ln(5)  # Line break after the patient info

    def footer(self):
        # Position at 15 mm from bottom
        self.set_y(-15)
        # Set the font for the page number
        self.set_font('Arial', 'I', 8)
        # Add the page number on the bottom-right (Page X of Y)
        page_number = f'Page {self.page_no()}'  # Placeholder for total pages
        self.cell(0, 10, page_number, 0, 0, 'R')

def generate_pdf(patient_data, risk_result, shap_image, interpretation_text):
    # Extract and format PatientInfo
    patient_info = patient_data.get('PatientInfo', {})
    patient_name = patient_info.get('name', 'N/A')
    patient_id = patient_info.get('patient_id', 'N/A')
    patient_age = patient_info.get('age', 'N/A')
    patient_gender = patient_info.get('gender', 'N/A')
    patient_address = patient_info.get('address', 'N/A')
    patient_phone = patient_info.get('phone', 'N/A')
    patient_email = patient_info.get('email', 'N/A')

    # Extract patient parameters
    vital_parameters = patient_data.get('VitalParameters', {})
    laboratory_values = patient_data.get('LaboratoryValues', {})
    symptoms_observations = patient_data.get('SymptomsObservations', {})
    ecg_results = patient_data.get('ECGResults', {})
    social_factors = patient_data.get('SocialFactors', {})

    # Create a BytesIO object to save the PDF to
    pdf_buffer = BytesIO()

    # Create an instance of the custom PDF class
    pdf = CustomPDF(patient_name, patient_id)
    pdf.add_page()

    # Add a title to the PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Risk Prediction Report", ln=True, align='C')

    # Add patient information header
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 8, txt="Patient Information", ln=True, align='L')
    pdf.ln(3)  # Reduced space between header and content

    # Set the font size for the patient details and parameters
    pdf.set_font('Arial', '', 10)

    # Create two columns: one for patient details, one for parameters
    left_x = 10   # Left column X coordinate
    right_x = 110  # Right column X coordinate
    start_y = pdf.get_y()  # Starting Y position for both columns
    col_width = 90

    # Left Column: Patient details
    pdf.set_xy(left_x, start_y)
    pdf.cell(col_width, 6, txt=f"Name: {patient_name}", ln=True, align='L')
    pdf.cell(col_width, 6, txt=f"ID: {patient_id}", ln=True, align='L')
    pdf.cell(col_width, 6, txt=f"Age: {patient_age}", ln=True, align='L')
    pdf.cell(col_width, 6, txt=f"Gender: {patient_gender}", ln=True, align='L')
    pdf.cell(col_width, 6, txt=f"Address: {patient_address}", ln=True, align='L')
    pdf.cell(col_width, 6, txt=f"Phone: {patient_phone}", ln=True, align='L')
    pdf.cell(col_width, 6, txt=f"Email: {patient_email}", ln=True, align='L')

    # Right Column: Risk Score (Traffic light and explanation)
    pdf.set_xy(right_x, start_y)  # Move to the right column

    # Display the traffic light image based on the risk score
    if risk_result == "High Risk":
        image = "visualization/assets/light_red.png"
        risk_explanation = f"A heart attack risk score has been calculated based on the provided patient information. {patient_name} has a High Risk of experiencing a heart attack."
    elif risk_result == "Low Risk":
        image = "visualization/assets/light_green.png"
        risk_explanation = f"A heart attack risk score has been calculated based on the provided patient information. {patient_name} has a Low Risk of experiencing a heart attack."
    else:
        image = "visualization/assets/light_red.png"
        risk_explanation = "No risk has been calculated."

    pdf.set_font('Arial', 'B', 14)
    pdf.cell(col_width, 6, text=risk_result, ln=True, align="C")

    start_y = pdf.get_y()

    # Insert the image (traffic light) aligned to the right
    pdf.image(image, x=right_x, y=start_y, w=17)  # Adjust 'w' for size of the image
    pdf.ln(35)  # Adjust spacing after the image (you can modify this based on the image height)

    # Move the cursor below the image
    pdf.set_xy(right_x + 20, start_y)

    # Print the risk explanation below the traffic light
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(col_width-20, 6, txt=risk_explanation, align='L')
    pdf.ln(10)

    pdf.set_font('Arial', '', 10)
    # Move cursor below both columns for the next section
    new_y = max(pdf.get_y(), start_y + len(vital_parameters) * 8)  # Adjust for the larger section
    pdf.set_y(new_y + 5)  # Add space before the next section

    # Vital Parameters
    pdf.ln(10)

    left_x = 10   # Starting x for the left column
    right_x = 110 # Starting x for the right column
    start_y = pdf.get_y()  # Starting y position for both sections

    # Left Column: Vital Parameters
    if vital_parameters:
        pdf.set_xy(left_x, start_y)  # Set starting position for the left column
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, 8, txt="Vital Parameters", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        
        for key, value in vital_parameters.items():
            # Print the key-value pair in the left column
            pdf.cell(col_width, 8, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True, align='L')

    # Right Column: Laboratory Values
    if laboratory_values:
        pdf.set_xy(right_x, start_y)  # Set starting position for the right column
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, 8, txt="Laboratory Values", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        
        for key, value in laboratory_values.items():
            # Reset the x-position to the right column for each new cell
            pdf.set_xy(right_x, pdf.get_y())  # Set x-position to right_x
            pdf.cell(col_width, 8, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True, align='L')


    # Move cursor below both columns for the next section
    new_y = max(pdf.get_y(), start_y + len(vital_parameters) * 8)  # Adjust for the larger section
    pdf.set_y(new_y + 5)  # Add space before the next section

    start_y = pdf.get_y()  # Starting y position for both sections

    # Symptoms Observations
    if symptoms_observations:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, 8, txt="Symptoms Observations", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        for key, value in symptoms_observations.items():
            pdf.cell(col_width, 8, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True, align='L')
        pdf.ln(3)

    # ECG Results
    if ecg_results:
        pdf.set_xy(right_x, start_y)  # Set starting position for the right column
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, 8, txt="ECG Results", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        for key, value in ecg_results.items():
            pdf.set_xy(right_x, pdf.get_y())  # Set x-position to right_x
            pdf.cell(col_width, 8, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True, align='L')
        pdf.ln(3)

    # Move cursor below both columns for the next section
    new_y = max(pdf.get_y(), start_y + len(vital_parameters) * 8)  # Adjust for the larger section
    pdf.set_y(new_y + 5)  # Add space before the next section

    # Social Factors
    if social_factors:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(col_width, 8, txt="Social Factors", ln=True, align='L')
        pdf.set_font('Arial', '', 10)
        for key, value in social_factors.items():
            pdf.cell(col_width, 8, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True, align='L')
        pdf.ln(3)

    # Enforce a page break
    pdf.add_page()

    # Continue with adding SHAP image and risk explanation...
    if shap_image:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(200, 10, txt="Reasoning of Risk Results", ln=True, align='C')
        pdf.ln(5)

        start_y = pdf.get_y()  # Starting y position for both sections

        # Save SHAP image to a temporary file and add to PDF
        with open("shap_plot.png", "wb") as f:
            f.write(shap_image.getbuffer())
        
        # Set the image to be 50% of the page width and aligned left
        image_width = (pdf.w - 20) / 2  # Set image width to half the page width with 10mm margin
        pdf.image("shap_plot.png", x=10, y=pdf.get_y(), w=image_width)  # Align left with x=10
        pdf.ln(10 + image_width / 3)  # Move cursor down after the image


        # Move to the right side for the SHAP interpretation text
        right_x = 10 + image_width + 10  # Right column starts after the image and some padding
        pdf.set_xy(right_x, start_y)  # Align SHAP interpretation text on the right side

        # Add the interpretation text on the right side
        text_width = pdf.w - right_x - 10  # The width of the remaining space on the right
        pdf.set_font('Arial', '', 10)  # Set font size to 10 for the interpretation text
        # Print each line of text while resetting the x-position to the right column after each line
        for line in interpretation_text.split('\n'):
            pdf.set_xy(right_x, pdf.get_y())  # Reset x-position for each new line of text
            pdf.multi_cell(text_width, 8, txt=line, align='L')
        # Adjust y-position after the text to continue rendering further content
        pdf.ln(10)

    # Output the PDF to the buffer
    pdf.output(pdf_buffer)

    # Set the buffer position to the beginning
    pdf_buffer.seek(0)

    return pdf_buffer
