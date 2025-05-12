import streamlit as st
from azure.data.tables import TableServiceClient
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import timedelta

load_dotenv()
STORAGE_CONN = os.getenv("AZURE_STORAGE_CONN")
table_service = TableServiceClient.from_connection_string(STORAGE_CONN)
table_client = table_service.get_table_client("SensorData")

entities = list(table_client.list_entities())
df = pd.DataFrame(entities)

df['RowKey'] = pd.to_datetime(df['RowKey'], errors='coerce', utc=True)
df = df.dropna(subset=['RowKey'])
df['Temperature'] = df['Temperature'].astype(float)
df['Humidity'] = df['Humidity'].astype(float)

df = df.sort_values(by='RowKey')
df.set_index('RowKey', inplace=True)

st.title("MT10 Temperature & Humidity Dashboard")
hours = st.slider("Show readings from the last N hours", 1, 48, 12)
cutoff = pd.Timestamp.now(tz="UTC") - timedelta(hours=hours)
filtered_df = df[df.index > cutoff]

if not filtered_df.empty:
    st.metric("Latest Temperature (°F)", f"{filtered_df['Temperature'].iloc[-1]:.1f}")
    st.metric("Latest Humidity (%)", f"{filtered_df['Humidity'].iloc[-1]:.1f}")
else:
    st.warning("No data available in the selected time range.")

st.subheader("Temperature (°F)")
st.line_chart(filtered_df[['Temperature']])

st.subheader("Humidity (%)")
st.line_chart(filtered_df[['Humidity']])