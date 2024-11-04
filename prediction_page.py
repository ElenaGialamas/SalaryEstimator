import streamlit as st
import pickle
import numpy as np
import pandas as pd

def load_pipeline():
    with open("saved_rfr_pipeline.pkl", "rb") as file:
        data = pickle.load(file)
    return data

pipeline = load_pipeline()

def show_prediction_page():
    st. title("Software Developer Salary Prediction")

    st. write("""### Please enter the following data for the salary prediciton""")

    # Get the available countries from the cleaned dataset
    countries = (     
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Ukraine",
        "India",
        "France",
        "Canada",
        "Brazil",
        "Spain",
        "Italy",
        "Netherlands",
        "Australia",
        "Other",
    )

    educationLevel = (
        "Less than a Bachelors",
        "Bachelor's degree",
        "Master's degree",
        "Post grad",
    )

    devType = (
        "Software Developer",
        "Manager",
        "Software Engineer",
        "Data Specialist",
        "Research & Academic",
        "Administrator",
        "Executive",
        "Other"
    )

    orgSize = (
        'Just me - I am a freelancer, sole proprietor, etc.',
        '2 to 9 employees',
        '10 to 19 employees',
        '20 to 99 employees',
        '100 to 499 employees',
        '500 to 999 employees',
        '1,000 to 4,999 employees',
        '5,000 to 9,999 employees',
        '10,000 or more employees',
    )

    industryType = (
        'Manufacturing', 'Software Development', 'Energy',
       'Banking/Financial Services', 'Healthcare',
       'Retail and Consumer Services', 'Transportation, or Supply Chain',
       'Computer Systems Design and Services', 'Insurance', 'Fintech',
       'Higher Education', 'Internet, Telecomm or Information Services',
       'Media & Advertising Services', 'Government'
    )

    column_names = ['Country', 'DevType', 'Industry', 'EdLevel', 'OrgSize', 'YearsCodePro', 'WorkExp']


    country = st.selectbox("Country", countries)
    developerType = st.selectbox("DeveloperType", devType)
    education = st.selectbox("Education Level", educationLevel)
    industry = st.selectbox("Industry", industryType)
    organizationSize = st.selectbox("Organization Size", orgSize)
    
    codePro = st.slider("Years Coding Professionally", 0, 50, 3)
    experience = st.slider("Years of General Work Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = pd.DataFrame([[country, developerType, industry, education, organizationSize, experience, codePro]],
                              columns=column_names)

        salary = pipeline.predict(X)
        formatted_salary = f"{salary[0]:,.2f}€  ".replace(',', 'X').replace('.', ',').replace('X', '.')
        st.subheader(f"The estimated salary is {formatted_salary}")