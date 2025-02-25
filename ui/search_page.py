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

response = requests.get('https://raw.githubusercontent.com/Ivaldivi/DATA515-Image-Classification/refs/heads/main/data/landmarks_washington_clean_images.csv')
if response.status_code == 200:
    pics_df = pd.read_csv(StringIO(response.text), sep=',')
    print("Data loaded successfully!")
else:
    print(f"Failed to fetch data: {response.status_code}")

# left join landmarks_df and pics_df on 'landmark_id' column
landmarks_df_join = landmarks_df.merge(pics_df, how='left', on='landmark_id')

text_search = st.text_input("Search for a landmark by name", "")

# this gives me multiple rows per landmarks as there are multiple images. Think about whether you want this or not
search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(text_search, case=False, na=False)]


if text_search:
    st.write(search_results)
else:
    st.write("Enter a landmark name to search for it.")

# Display images
n_pics_per_row = 3
if text_search:
    for i in range(0, len(search_results), n_pics_per_row):
        row = search_results.iloc[i:i + n_pics_per_row]
        st.image(row['url'].tolist(), width=200, caption=row['name'].tolist())