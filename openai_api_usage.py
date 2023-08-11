import os
from dotenv import load_dotenv
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Fetch data from the API
@st.cache  # This decorator allows the data to be cached so it's not re-fetched every time the app reruns
def fetch_data(start_date, end_date):
    url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start_date}&end_date={end_date}"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data


# Load and process the data
def load_data(start_date, end_date):
    data = fetch_data(start_date, end_date)

    # Process the data similar to what we did earlier
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)

    # Define a function to flatten the daily_costs column into a new DataFrame
    def flatten_daily_costs(df):
        daily_costs_data = []
        for i in range(df.shape[0]):
            timestamp = df["daily_costs"][i]["timestamp"]
            line_items = df["daily_costs"][i]["line_items"]
            for line_item in line_items:
                name = line_item["name"]
                cost = line_item["cost"]
                daily_costs_data.append([timestamp, name, cost])
        return pd.DataFrame(daily_costs_data, columns=["timestamp", "name", "cost"])

    # Flatten the daily_costs column
    df = flatten_daily_costs(df)

    # Convert the timestamp to a datetime object
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    return df


# Main part of the app
def main():
    # Define a dictionary with the dropdown options
    options = {"Last day": 1, "Last 7 days": 7, "Last 30 days": 30}
    # Create a dropdown in the sidebar and a date input
    period = st.sidebar.selectbox("Select a period:", list(options.keys()))
    start_date = st.sidebar.date_input(
        "Start date:", datetime.now() - timedelta(days=options[period])
    )
    end_date = st.sidebar.date_input("End date:", datetime.now())

    # Get the data for the selected period
    df = load_data(start_date, end_date)

    # Display the DataFrame in the app
    st.dataframe(df)
    # Plot the data in the app using matplotlib and display the plot
    plot = plt.plot(df["timestamp"], df["cost"])

    st.pyplot(plot)


# Run the main part of the app
if __name__ == "__main__":
    main()
