import streamlit as st
import pandas as pd
# might need to add to environment.yml
import requests
from io import StringIO

# Page setup
st.set_page_config(page_title = "Washington Landmarks Search", page_icon = ":mag_right:", layout = "wide")
st.title("Washington Landmarks Search")

# Connect to data for search
response = requests.get('https://raw.githubusercontent.com/Ivaldivi/DATA515-Image-Classification/refs/heads/main/data/landmarks_washington_full.csv')
if response.status_code == 200:
    landmarks_df = pd.read_csv(StringIO(response.text), sep='\t')
    st.write("Data loaded successfully!")
else:
    st.write(f"Failed to fetch data: {response.status_code}")

