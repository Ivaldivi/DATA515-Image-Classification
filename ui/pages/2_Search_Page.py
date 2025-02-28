"""
This file contains the code for the Search page of the Streamlit app.
"""
import streamlit as st
import pandas as pd

from ui.helpers.get_data_from_csv import get_data_from_csv


# Page setup
st.set_page_config(page_title =
                   "Washington Landmarks Search",
                   page_icon = ":mag_right:", layout = "wide")
st.title("Washington Landmarks Search")

# Connect to data for search
landmarks_df = get_data_from_csv('../data/landmarks_washington_full.csv')
pics_df = get_data_from_csv('../data/landmarks_washington_clean_images.csv')

# right join landmarks_df and pics_df on 'landmark_id' column to remove
# any landmarks that had bad urls
landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')

text_search = st.text_input("Search for a landmark by name", "")


search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                    text_search, case=False, na=False)]


if not text_search:
    st.write("Enter a landmark name to search for it.")

# Display images
N_PICS_PER_ROW = 3
if text_search:
    short_results_list = []

    # display at most three images per landmark
    # need to resize images so they are same size
    # this should probably go into a function that I test
    for landmark_id in search_results['landmark_id'].drop_duplicates():
        landmark_short = search_results[search_results['landmark_id'] == landmark_id].head(3)
        short_results_list.append(landmark_short)

    short_results = pd.concat(short_results_list, ignore_index = True)

    for i in range(0, len(short_results), N_PICS_PER_ROW):
        row = short_results.iloc[i:i + N_PICS_PER_ROW]
        st.image(row['url'].tolist(), width=200, caption=row['name'].tolist())
