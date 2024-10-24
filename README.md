# CardioVision: Advanced Diagnostic Analytics for Cardiovascular Health

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/visualization/assets/CardioVision_Full_Logo.svg" width="600px">

**CardioVision** is an advanced medical dashboard designed to assist cardiologists in predicting heart attack risks and providing **real-time**, **data-driven** insights into patient cardiovascular health. It combines key health metrics like **chest pain type**, **cholesterol levels**, **heart rate**, and **lifestyle factors** to support accurate **risk assessment** and improve patient care. 

This project is part of a **university course project** aimed at enhancing **diagnostic analytics** for cardiovascular health using advanced machine learning techniques and visualization tools.

The resulting app can be accessed here: https://cardiovision.streamlit.app/

---

## Key Features

CardioVision contains a wide range of features that help with diagnosis and patient management:

### 1. **Patient Management**
Easily access patient details and history through an intuitive interface.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/visualization/assets/Patient_Management.svg" width="30%">

### 2. **Heart Attack Risk Assessment**
Assess heart attack risk using advanced algorithms that leverage clinical data.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/visualization/assets/Risk_Prediction.svg" width="30%">

### 3. **Diagnostic Insights**
Generate insights from patient history and clinical test results to support decision-making.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/visualization/assets/XAI.svg" width="30%">

---

## Dataset Overview

The CardioVision project uses the **Cleveland** and **Long Beach** datasets, which contain detailed information on cardiovascular health. These datasets were selected due to their completeness and relevance.

### Dataset Sources:
- **Cleveland Clinic Foundation**: Collected by Dr. Robert Detrano, M.D., Ph.D.
- **Hungarian Institute of Cardiology**: Collected by Dr. Andras Janosi, M.D.
- **University Hospital, Zurich, Switzerland**: Collected by Dr. William Steinbrunn, M.D.
- **University Hospital, Basel, Switzerland**: Collected by Dr. Matthias Pfisterer, M.D.

**Reference Publication**:
Detrano, R., Janosi, A., Steinbrunn, W., Pfisterer, M., Schmid, J., Sandhu, S., et al. (1989). *International application of a new probability algorithm for the diagnosis of coronary artery disease.* *American Journal of Cardiology, 64*(5):304-310.

---

## Pages and Features

### 1. **Patient Information**
The **Patient Information** page allows users to view the relevant patient data and parameters that are used for the heart attack risk prediction.

**Features:**
- Displays key patient data including demographic, clinical, and lifestyle factors.
- Provides an overview of the parameters that feed into the risk prediction model.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/images/Patient_Info_Page.jpg" width="80%">

### 2. **Risk Prediction**
Based on the patient information, the **Risk Prediction** page calculates the likelihood of a heart attack. The page also includes a SHAP visualization to show which factors influence the prediction the most.

**Features:**
- Calculates heart attack risk based on patient data.
- Displays SHAP values to explain the impact of each feature on the prediction.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/images/Risk_Calculation_Page.jpg" width="80%">

### 3. **Descriptive Analytics**
The **Descriptive Analytics** page provides a high-level overview of the dataset, showing summary statistics such as **gender distribution**, **age distribution**, and **heart attack risk factors**.

**Features:**
- Summary of patient data (e.g., number of patients, risk factors).
- Interactive visualizations for demographic and clinical data.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/images/Descriptive_Page.jpg" width="80%">

### 4. **Diagnostic Analytics**
This page helps users explore relationships between variables:
- **Correlation Heatmap**: Visualizes relationships between clinical variables.
- **Feature Comparison**: Allows users to select and compare two features with a regression line and scatter plot.
- **Pair Plot Analysis**: Visualizes distributions and relationships between multiple variables.

**Features:**
- Custom feature selection and comparison.
- Regression line and statistical insights.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/images/Diagnostic_Page.jpg" width="80%">

### 5. **Technical Information**
The **Technical Information** page provides more background about machine learning model used, the evaluation metrics and the dataset used to train it.

**Features:**
- Displays background information about the data.
- Show evaluation metrics of the applied machine learning model.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/images/Technical_Information_Page.jpg" width="80%">


### 6. **About**
The **About** page provides more background about the app, including dataset references, details on the team, and contact information for further inquiries.

**Features:**
- Displays background information about the project.
- Lists references, team members, and contact information.

<img src="https://github.com/KentFre/CDS_CardioVision/blob/main/images/About_Page.jpg" width="80%">


---

## Meet the Team

The **CardioVision** project was developed by an interdisciplinary team of experts in cardiology, data science, machine learning, and software engineering:

| Role                 | Team Member       |
|----------------------|-------------------|
| Lead Cardiologist     | Valentina OM   |
| Lead Data Scientist   | Viktoriia O       |
| Lead SW Architect     | Kent F            |
| Lead UI/UX Designer   | Jacky K           |
| Lead ML Engineer      | JiWei Y           |
| Lead XAI Engineer     | Eranive M         |

---