import streamlit as st
import pandas as pd
# might need to add to environment.yml
import requests
from io import StringIO

# Page setup
st.set_page_config(page_title = "Washington Landmarks Search", page_icon = ":mag_right:", layout = "wide")
st.title("Washington Landmarks Search")

# Connect to data for search
# should I do a try catch here? do we want the exception to go to streamlit or terminal
response = requests.get('https://raw.githubusercontent.com/Ivaldivi/DATA515-Image-Classification/refs/heads/main/data/landmarks_washington_full.csv')
if response.status_code == 200:
    landmarks_df = pd.read_csv(StringIO(response.text), sep=',')
    print("Data loaded successfully!")
else:
    print(f"Failed to fetch data: {response.status_code}")

text_search = st.text_input("Search for a landmark by name", "")
search_results = landmarks_df[landmarks_df['name'].str.contains(text_search, case=False, na=False)]

if text_search:
    st.write(search_results)
else:
    st.write("Enter a landmark name to search for it.")