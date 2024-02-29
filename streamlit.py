import streamlit as st
import pandas as pd
import requests

# Function to fetch logs from the FastAPI service
def fetch_logs(api_url="http://127.0.0.1:8000/logs/"):
    response = requests.get(api_url)
    if response.status_code == 200:
        logs = response.json()
        return pd.DataFrame(logs)
    else:
        st.error(f"Failed to fetch logs: HTTP {response.status_code}")
        return pd.DataFrame()

# Streamlit UI
def display_logs():
    st.title('Ledger Bot')

    # Specify your FastAPI logs endpoint
    api_url = "http://127.0.0.1:8000/logs/"
    df = fetch_logs(api_url)

    if not df.empty:
        # Convert timestamp column to datetime for better sorting and formatting
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        st.dataframe(df)
    else:
        st.write("No logs available.")

if __name__ == "__main__":
    display_logs()

# start command: streamlit run streamlit.py
