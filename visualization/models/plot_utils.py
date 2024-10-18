import plotly.express as px
import pandas as pd

# Gender Distribution Plot
def plot_gender_distribution(df):
    fig = px.pie(df, names='gender', title='Gender Distribution')
    fig.update_traces(marker=dict(colors=['skyblue', 'lightcoral']))
    return fig

# Age Distribution of Patients Plot
def plot_age_distribution(df):
    fig = px.histogram(df, x='age', nbins=10, title='Age Distribution of Patients')
    fig.update_traces(marker_color='#2a9d8f')
    fig.update_layout(xaxis_title='Age of Patients', yaxis_title='Number of Patients')
    return fig

# Heart Attack Risk by Gender Plot
def plot_risk_by_gender(df):
    risk_by_gender = df[df['heart_disease_diagnosis'] == True]['gender'].value_counts()
    fig = px.bar(risk_by_gender, x=risk_by_gender.index, y=risk_by_gender.values, title='Heart Attack Risk by Gender')
    fig.update_traces(marker_color='#264653')
    fig.update_layout(xaxis_title='Gender', yaxis_title='Number of Patients at Risk')
    return fig

# Distribution of Heart Attacks Plot
def plot_risk_distribution(df):
    risk_distribution = df['heart_disease_diagnosis'].value_counts().reset_index()
    risk_distribution.columns = ['Heart Attack Risk', 'Count']
    fig = px.bar(risk_distribution, x='Heart Attack Risk', y='Count', title='Distribution of Heart Attacks')
    fig.update_traces(marker_color='#234973')
    fig.update_layout(xaxis_title='Heart Attack Diagnosis', yaxis_title='Number of Patients')
    return fig

# Age Distribution by Gender and Heart Attack Status Plot
def plot_age_distribution_by_gender_and_heart_attack(df):
    fig = px.violin(
        df, y="age", x="heart_disease_diagnosis", color="gender", 
        title="Age Distribution by Gender and Heart Attack Status", box=True
    )
    fig.update_layout(xaxis_title="Heart Attack Status", yaxis_title="Age")
    return fig

# Heart Attack Distribution by Age Group and Gender Plot
def plot_heart_attack_by_age_group_and_gender(df):
    bins = [0, 40, 50, 60, 70, 80, float('inf')]
    labels = ['<40', '40-50', '50-60', '60-70', '70-80', '>80']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    high_risk_patients = df[df['heart_disease_diagnosis'] == True]
    heart_attack_distribution = high_risk_patients.groupby(['age_group', 'gender']).size().reset_index(name='count')
    fig = px.bar(
        heart_attack_distribution, x='age_group', y='count', color='gender', 
        barmode='group', title="Distribution of Heart Attacks by Age Group and Gender"
    )
    fig.update_layout(xaxis_title='Age Group', yaxis_title='Number of Heart Attacks')
    return fig
