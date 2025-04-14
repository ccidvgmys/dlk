import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# --- Load Station Data ---
sheet_station = client.open_by_url("https://docs.google.com/spreadsheets/d/1dQudJMakV3M1qCGN3_iVvue2nFIt5v1q1y_08wpUvFg/edit")
worksheet_station = sheet_station.worksheet("Stations")
station_data = pd.DataFrame(worksheet_station.get_all_records())
station_data.columns = station_data.columns.str.strip()

# --- Load Norms Data ---
sheet_norms = client.open_by_url("https://docs.google.com/spreadsheets/d/1cLQrVAqs1jY2dpiCqG29zTQy8Y44ROWiANbjsz3hQe8/edit")
worksheet_norms = sheet_norms.worksheet("Copy of Norms")
norms_data = pd.DataFrame(worksheet_norms.get_all_records())
norms_data.columns = norms_data.columns.str.strip()

# --- Streamlit UI ---
st.title("Station Amenities & Norms Viewer")

# Dropdown for station selection
station_codes = station_data['Station Code'].unique()
selected_code = st.selectbox("Select Station Code", station_codes)

# Show selected station info
station_info = station_data[station_data['Station Code'] == selected_code].iloc[0]
station_name = station_info['Station Name']
category = station_info['Category'].strip()

st.markdown(f"### Station Name: {station_name}")
st.markdown(f"**Category:** {category}")

# Filter norms data based on station category
norms_data['Category'] = norms_data['Category'].str.strip()
filtered_norms = norms_data[norms_data['Category'] == category]

# --- Group by Type ---
amenity_types = ["MEA", "RECOMMENDED", "DESIRABLE", "Divyangjan"]

for amenity_type in amenity_types:
    sub_df = filtered_norms[filtered_norms['AMENITY'].str.upper() == amenity_type.upper()]
    if not sub_df.empty:
        st.markdown(f"## {amenity_type}")
        st.dataframe(sub_df.reset_index(drop=True))

