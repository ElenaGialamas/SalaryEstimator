import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# First clean the data as done in the notebook for a compareable display

def clean_country(categories, cutoff):
    category_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            category_map[categories.index[i]] = categories.index[i]
    return category_map

def extract_currency_code(currency_string):
    # Use regex to extract the first 3-4 uppercase letters (assuming ISO currency codes)
    match = re.match(r'([A-Z]{3,4})', currency_string.strip().upper())
    return match.group(1) if match else None

# Define static exchange rates from 2024 (so that it matches with when the survey took place)
conversion_rates = {
    'USD': 1.0825,   # United States dollar
    'SEK': 11.4475,  # Swedish krona
    'INR': 91.027,  # Indian rupee
    'EUR': 1.0,    # European Euro (already in EUR)
    'UAH': 44.7537,  # Ukrainian hryvnia
    'CHF': 0.9382,   # Swiss franc
    'CAD': 1.4989,   # Canadian dollar
    'BRL': 6.142,   # Brazilian real
    'GBP': 0.8336,   # Pound sterling
    'AUD': 1.6311,   # Australian dollar
    'PLN': 4.3478,   # Polish zloty
    'CZK': 25.25,   # Czech koruna
    'GGP': 0.8336,   # Guernsey Pound
    'AED': 3.9668,   # United Arab Emirates dirham
    'FKP': 0.8264,   # Falkland Islands pound
    'NZD': 1.8025,   # New Zealand dollar
    'FJD': 2.4281,   # Fijian dollar
    'BSD': 1.0822,   # Bahamian dollar
    'NAD': 19.1047,   # Namibian dollar
    'DKK': 7.4609,   # Danish krone
    'AMD': 418.8346, # Armenian dram
    'UZS': 13869.9635,# Uzbekistani som
    'UGX': 3969.3804,# Ugandan shilling
    'BGN': 1.9558,   # Bulgarian lev
    'CLP': 1023.7092, # Chilean peso
    'XPF': 119.2425, # CFP franc
    'EGP': 52.6484,  # Egyptian pound
    'RON': 4.9733,    # Romanian leu
    'GEL': 2.9379,   # Georgian lari
    'ETB': 131.6047,   # Ethiopian birr
    'NOK': 11.8195,  # Norwegian krone
    'KRW': 1504.09,# South Korean won
    'VES': 3912253.2522, # Venezuelan bolivar
}

devtype_mapping = {
    'Developer, full-stack': 'Software Developer',
    'Developer, back-end': 'Software Developer',
    'Developer, front-end': 'Software Developer',
    'Developer, mobile': 'Software Developer',
    'Developer, desktop or enterprise applications': 'Software Developer',
    'Developer, embedded applications or devices': 'Software Developer',
    'Developer, game or graphics': 'Software Developer',
    'Developer, AI': 'Software Developer',
    'Developer, QA or test': 'Software Developer',
    'Developer Advocate': 'Software Developer',
    'Developer Experience': 'Software Developer',
    
    'Engineering manager': 'Manager',
    'Project manager': 'Manager',
    'Product manager': 'Manager',
    
    'Security professional': 'Software Engineer',
    'Cloud infrastructure engineer': 'Software Engineer',
    'Engineer, site reliability': 'Software Engineer',
    'Hardware Engineer': 'Software Engineer',
    
    'Data engineer': 'Data Specialist',
    'Data scientist or machine learning specialist': 'Data Specialist',
    'Data or business analyst': 'Data Specialist',
    
    'Academic researcher': 'Research & Academic',
    'Research & Development role': 'Research & Academic',
    'Educator': 'Research & Academic',
    'Scientist': 'Research & Academic',
    'Student': 'Research & Academic',
    
    'System administrator': 'Administrator',
    'Database administrator': 'Administrator',
    
    'Senior Executive (C-Suite, VP, etc.)': 'Executive',
    
    'Designer': 'Other',
    'Blockchain': 'Other',
    'Other (please specify):': 'Other',
    'Marketing or sales professional': 'Other',
}

def shorten_categories(categories, cutoff):
    category_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            category_map[categories.index[i]] = categories.index[i]
        else:
            category_map[categories.index[i]] = 'Other'
    return category_map


def clean_yearsCodePro(x):
    if x == "Less than 1 year":
        return 0
    if x == "More than 50 years":
        return 51
    return float(x)


def group_education_levels(x):
    if "Bachelor’s degree" in x:
        return "Bachelor's degree"
    if "Master’s degree" in x:
        return "Master's degree"
    if "Professional degree" in x:
        return "Post grad"
    return "Less than a Bachelors"

@st.cache_data
def load_data():
    data_part1 = pd.read_csv("survey_results_part1.csv")
    data_part2 = pd.read_csv("survey_results_part2.csv")
    df = pd.concat([data_part1, data_part2], ignore_index=True)
    
    df = df[df["CompTotal"].notnull()]

    country_map = clean_country(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df.dropna(subset=["Country"])

    df['CompTotal']
    df['Currency_Code'] = df['Currency'].apply(extract_currency_code)
    df["CompTotalEUR"] = df.apply(
        lambda row: row["CompTotal"] / conversion_rates.get(row["Currency_Code"], 1),
        axis=1)
    df.drop(columns=["Currency_Code", "CompTotal", "ConvertedCompYearly", "Currency"], inplace=True)
    df = df[df["CompTotalEUR"] <= 250000]
    df = df[df["CompTotalEUR"] >= 10000]
    df = df[[ "CompTotalEUR", "Country", "EdLevel", "YearsCodePro", "Employment", 
                "OrgSize", "LanguageHaveWorkedWith",  "DevType", "Industry", "WorkExp"]]
    
    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_yearsCodePro)

    df['EdLevel'] = df['EdLevel'].apply(group_education_levels)

    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop(columns="Employment")

    df["DevType"] = df['DevType'].map(devtype_mapping)

    df = df.drop(columns="LanguageHaveWorkedWith")
    return df


df = load_data()

def show_explore_data_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2024

    Explore the data the prediction model is based on.
    """)

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["CompTotalEUR"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["CompTotalEUR"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write(
        """
    #### Mean Salary Based On Industry
    """
    )

    data = df.groupby(["Industry"])["CompTotalEUR"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Developer Type
    """
    )

    data = df.groupby(["DevType"])["CompTotalEUR"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Organization Size
    """
    )

    data = df.groupby(["OrgSize"])["CompTotalEUR"].mean().sort_values(ascending=False)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Education Level
    """
    )

    data = df.groupby("EdLevel")["CompTotalEUR"].mean().sort_values(ascending=False).reset_index()
    st.bar_chart(data.set_index("EdLevel"))
