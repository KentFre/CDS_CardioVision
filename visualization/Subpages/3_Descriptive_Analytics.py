import streamlit as st
import pandas as pd
import plotly.express as px
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

# Sample data for demonstration purposes
def load_data():
    data = pd.read_csv('visualization/assets/heart_disease_data.csv')
    return data

# Load the dataset
data = load_data()

# Convert to DataFrame
df = pd.DataFrame(data)

# Descriptive statistics calculations
total_patients = len(df)
total_risk_patients = df['heart_disease_diagnosis'].sum()  
average_age = df['age'].mean()

# Gender distribution
gender_distribution = df['gender'].value_counts()

# Create two columns with specified ratios
r1, r2 = st.columns((0.1, 1))

# Display the logo in the first column
r1.image("visualization/assets/CardioVision_icon.png", width=60)

# Set the title in the second column
r2.title("Descriptive Analytics ")

m1, m2, m3 = st.columns((1,1,1))

# Display empty columns for formatting
m1.metric(label='Number of Patients', value=total_patients)
m2.metric(label='Patients with Heart Attack', value=total_risk_patients)
m3.metric(label='Average Age of Patients', value=round(average_age, 2))

# Now, let's add graphs in a column layout for visualizations
g1, g2 = st.columns((1, 1))

# Gender Distribution Pie Chart using Plotly
fig1 = px.pie(df, names='gender', title='Gender Distribution', template='seaborn')
fig1.update_traces(marker=dict(colors=['skyblue', 'lightcoral']))
fig1.update_layout(title_x=0.1, margin=dict(l=0, r=0, b=10, t=30), showlegend=True)
g1.plotly_chart(fig1, use_container_width=True)

# Age Distribution Histogram using Plotly
fig2 = px.histogram(df, x='age', nbins=10, title='Age Distribution of Patients', template='seaborn')
fig2.update_traces(marker_color='#2a9d8f')
fig2.update_layout(
    title_x=0.1,
    margin=dict(l=0, r=0, b=10, t=30),
    xaxis_title='Age of Patients',     
    yaxis_title='Number of Patients'   
)
g2.plotly_chart(fig2, use_container_width=True)

h1, h2 = st.columns((1, 1))

# Heart Attack Risk by Gender Bar Chart using Plotly
risk_by_gender = df[df['heart_disease_diagnosis'] == True]['gender'].value_counts()
risk_df = pd.DataFrame({'gender': risk_by_gender.index, 'Count': risk_by_gender.values})
fig3 = px.bar(risk_df, x='gender', y='Count', title='Heart Attack Risk by Gender', template='seaborn')
fig3.update_traces(marker_color='#264653')
fig3.update_layout(
    title_x=0.1,
    margin=dict(l=0, r=0, b=10, t=30),
    xaxis_title='Gender',             # X-axis label
    yaxis_title='Number of Patients at Risk'  # Y-axis label
)
h1.plotly_chart(fig3, use_container_width=True)


# Count the number of patients with and without heart attack 
risk_distribution = df['heart_disease_diagnosis'].value_counts().reset_index()
risk_distribution.columns = ['Heart Attack Risk', 'Number of Patients']

# Heart Attack Distribution Bar Chart using Plotly
fig3 = px.bar(risk_distribution, x='Heart Attack Risk', y='Number of Patients',
              title='Distribution of Heart Attacks', template='seaborn')
fig3.update_traces(marker_color='#234973')
fig3.update_layout(
    title_x=0.1,
    margin=dict(l=0, r=0, b=10, t=30),
    xaxis_title='Heart Attack Diagnosis',  # X-axis label
    yaxis_title='Number of Patients'        # Y-axis label
)
h2.plotly_chart(fig3, use_container_width=True)

# User selection for features to visualize
st.subheader("Data Visualisation")

# Options for the user to choose from
visual_options = [
    'Heart Attacks Distribution by Gender and Age',
    'Heart Attacks Relationship with Exercise Induced Angina',
    'Assessing Chest Pain Types',
    'High Sugar Levels and Heart Attacks',
    'Cholesterol Levels Analysis',
    'Heart Rate Measurements Distribution'
]
selected_features = st.multiselect('Choose the visualizations you want to see:', visual_options)

# 1. Heart Attacks Distribution by Gender and Age 
if 'Heart Attacks Distribution by Gender and Age' in selected_features:
    # Define bins and labels for age groups
    bins = [0, 40, 50, 60, 70, 80, float('inf')]
    labels = ['<40', '40-50', '50-60', '60-70', '70-80', '>80']

    # Create age_group column in the dataframe
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    # Filter high-risk patients
    high_risk_patients = df[df['heart_disease_diagnosis'] == True]

    # Group by gender and age group
    heart_attack_distribution = high_risk_patients.groupby(['gender', 'age_group']).size().unstack(fill_value=0)

    # Create a bar plot for heart attack distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    heart_attack_distribution.loc['Male'].plot(kind='bar', color='blue', alpha=0.7, label='Male', position=0, width=0.4, ax=ax)
    heart_attack_distribution.loc['Female'].plot(kind='bar', color='red', alpha=0.7, label='Female', position=1, width=0.4, ax=ax)

    ax.set_xlabel('Age Groups')
    ax.set_ylabel('Number of Heart Attacks')
    ax.set_title('Distribution of Heart Attacks by Age Group and Gender')
    ax.legend()
    ax.set_xticklabels(labels, rotation=45)
    st.pyplot(fig)

    
# 2. Heart Attacks Relationship with Exercise Induced Angina
if 'Heart Attacks Relationship with Exercise Induced Angina' in selected_features:
    angina_patients = df[df['exercise_induced_angina'] == True]
    high_risk_angina_patients = angina_patients[angina_patients['heart_disease_diagnosis'] == True]

    percentage_high_risk = (len(high_risk_angina_patients) / len(angina_patients)) * 100
    percentage_not_high_risk = 100 - percentage_high_risk

    labels = ['High Risk of Heart Attack', 'Not High Risk of Heart Attack']
    sizes = [percentage_high_risk, percentage_not_high_risk]
    colors = ['red', 'green']
    explode = (0.1, 0)  # explode the 'High Risk' slice for emphasis

    fig_angina = plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Percentage of Patients with Exercise-Induced Angina at High Risk of Heart Attack')
    plt.axis('equal')  # Equal aspect ratio ensures that the pie is drawn as a circle.
    st.pyplot(fig_angina)

    
# 3. Assessing Chest Pain Types
if 'Assessing Chest Pain Types' in selected_features:
    chest_pain_heart_attack_count = df.groupby(['chest_pain_type', 'heart_disease_diagnosis']).size().unstack()

    fig_chest_pain = chest_pain_heart_attack_count.plot(kind='bar', stacked=True, color=['green', 'red'], figsize=(10, 6))
    plt.title('Count of Patients by Chest Pain Type and Heart Attack Status')
    plt.xlabel('Chest Pain Type ')
    plt.ylabel('Number of Patients')
    plt.legend(title='Heart Attack', labels=['No', 'Yes'])
    plt.xticks(rotation=0)
    st.pyplot(fig_chest_pain.figure)

    
# 4. High Sugar Levels and Heart Attacks
if 'High Sugar Levels and Heart Attacks' in selected_features:
    heart_attack_patients = df[df['heart_disease_diagnosis'] == True]
    high_fasting_blood_sugar_counts = heart_attack_patients['high_fasting_blood_sugar'].value_counts()
    high_fasting_blood_sugar_percentages = heart_attack_patients['high_fasting_blood_sugar'].value_counts(normalize=True) * 100

    plt.figure(figsize=(8, 6))
    sns.countplot(data=heart_attack_patients, x='high_fasting_blood_sugar')

    for i, count in enumerate(high_fasting_blood_sugar_counts):
        percentage = high_fasting_blood_sugar_percentages[i]
        plt.text(i, count + 1, f'{percentage:.2f}%', ha='center', fontsize=12)

    plt.title('High Fasting Blood Sugar Counts among Heart Attack Patients')
    plt.xlabel('High Fasting Blood Sugar')
    plt.ylabel('Number of Patients')
    st.pyplot(plt.gcf())

    
# 5. Cholesterol Levels Analysis
if 'Cholesterol Levels Analysis' in selected_features:
    heart_disease_patients = df[df['heart_disease_diagnosis'] == True]
    high_cholesterol_patients = heart_disease_patients[heart_disease_patients['serum_cholesterol'] > 200]

    high_cholesterol_count = high_cholesterol_patients.shape[0]
    total_heart_disease_patients = heart_disease_patients.shape[0]

    percentage_high_cholesterol = (high_cholesterol_count / total_heart_disease_patients) * 100

    labels = ['Cholesterol > 200 mg/dL', 'Cholesterol <= 200 mg/dL']
    sizes = [percentage_high_cholesterol, 100 - percentage_high_cholesterol]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # explode the first slice (cholesterol > 200 mg/dL)

    fig_cholesterol = plt.figure(figsize=(6, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title('Percentage of Patients with Serum Cholesterol > 200 mg/dL')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig_cholesterol)

    
# 6. Heart Rate Measurements Distribution
heart_disease_patients = df[df['heart_disease_diagnosis'] == True]

if 'Heart Rate Measurements Distribution' in selected_features:
    resting_heart_rate_stats = {
        'Min Resting Heart Rate': heart_disease_patients['resting_heart_rate'].min(),
        'Average Resting Heart Rate': heart_disease_patients['resting_heart_rate'].mean(),
        'Max Resting Heart Rate': heart_disease_patients['resting_heart_rate'].max()
    }

    max_heart_rate_stats = {
        'Min Max Heart Rate': heart_disease_patients['max_heart_rate'].min(),
        'Average Max Heart Rate': heart_disease_patients['max_heart_rate'].mean(),
        'Max Max Heart Rate': heart_disease_patients['max_heart_rate'].max()
    }

    stats_df = pd.DataFrame({
        'Resting Heart Rate': list(resting_heart_rate_stats.values()),
        'Max Heart Rate': list(max_heart_rate_stats.values())
    }, index=['Min', 'Average', 'Max'])

    plt.figure(figsize=(10, 6))
    stats_df.plot(kind='bar', figsize=(10, 6), color=['blue', 'orange'])
    plt.title('Resting Heart Rate and Max Heart Rate Statistics (Patients with Heart Disease)', fontsize=16)
    plt.xlabel('Statistics', fontsize=14)
    plt.ylabel('Heart Rate (BPM)', fontsize=14)
    plt.xticks(rotation=0)
    plt.legend(title='Heart Rate Type')
    plt.grid(True)
    st.pyplot(plt.gcf())






