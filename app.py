import pandas as pd
import matplotlib.pyplot as plt
import openai
import streamlit as st
import requests

# Set OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to fetch economic data from World Bank API
def fetch_economic_data(indicator, country="USA", start_year=2015, end_year=2023):
    url = f"http://api.worldbank.org/v2/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 1:
            return [(entry['date'], entry['value']) for entry in data[1] if entry['value'] is not None]
    return []

# Function to generate economic insights using OpenAI
def generate_insights(data, indicator):
    prompt = f"Analyze the following economic data for {indicator} and provide insights:\n{data}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert economic analyst."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Streamlit App
st.title("AI-Powered Economic Report Generator")

indicator_mapping = {
    "GDP Growth (%)": "NY.GDP.MKTP.KD.ZG",
    "Inflation Rate (%)": "FP.CPI.TOTL.ZG",
    "Unemployment Rate (%)": "SL.UEM.TOTL.ZS"
}

selected_indicator = st.selectbox("Select an Economic Indicator", list(indicator_mapping.keys()))
country_code = st.text_input("Enter Country Code (e.g., USA, IND, CHN)", "USA")

if st.button("Generate Report"):
    data = fetch_economic_data(indicator_mapping[selected_indicator], country_code)
    if data:
        df = pd.DataFrame(data, columns=["Year", "Value"])
        df = df.sort_values(by="Year")

        # Generate Insights
        insights = generate_insights(df.to_string(index=False), selected_indicator)

        # Plot Data
        fig, ax = plt.subplots()
        ax.plot(df["Year"], df["Value"], marker="o", linestyle="-")
        ax.set_xlabel("Year")
        ax.set_ylabel(selected_indicator)
        ax.set_title(f"{selected_indicator} Trend in {country_code}")
        st.pyplot(fig)

        # Display Insights
        st.subheader("AI-Generated Insights")
        st.write(insights)
    else:
        st.error("No data available for the selected indicator and country.")

st.markdown("Developed by **Saurabh Chhatwal**")
