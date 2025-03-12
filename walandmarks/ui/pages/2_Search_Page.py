"""
This file contains the code for the Search page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import re

import numpy as np
import streamlit as st

from walandmarks.ui.helpers.get_data_from_csv import get_data_from_csv

# initialize session state
if "selected_landmark" not in st.session_state:
    st.session_state.selected_landmark = ""

# Page setup
st.set_page_config(page_title =
                   "Washington Landmarks Search",
                   page_icon = ":mag_right:", layout = "wide")
st.title("Washington Landmarks Search")
# Connect to data for search
landmarks_df = get_data_from_csv('data/landmarks_washington_full.csv')
pics_df = get_data_from_csv('data/landmarks_washington_clean_images.csv')
# right join landmarks_df and pics_df on 'landmark_id' column to remove
# any landmarks that had bad urls
landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')

text_search = st.text_input("Search for a landmark by name", st.session_state.selected_landmark)
search_term_escaped = re.escape(text_search)
search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                    search_term_escaped, case=False, na=False, regex = True)]
# if no text has been submitted display a message
if not text_search:
    st.write("Enter a landmark name to search for it.")
# when text has been submitted do the following
else:
    exact_match = search_results[search_results['name'].str.upper() == text_search.upper()]
    # if there is an exact match display the landmark images and facts
    if not exact_match.empty:
        st.header(exact_match['name'].iloc[0])
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"<b>Category:</b> {exact_match['supercategory'].iloc[0]}",
                            unsafe_allow_html=True)
                st.markdown(f"<b>Location:</b> {exact_match['location'].iloc[0]}",
                            unsafe_allow_html=True)
                st.image(exact_match['url'].iloc[0], width=300)
            with col2:
                map_container = st.empty()
                map_container.map(exact_match.iloc[:1])
    # if there is a partial match provide buttons of the suggested full names
    else:
        # Suggest similar names as clickable buttons
        if search_results.empty:
            st.write("No landmarks found. Try another search.")
        else:
            st.write("Did you mean:")
            for name in np.sort(search_results['name'].unique()):
                if st.button(name):
                    st.session_state.selected_landmark = name
                    st.rerun()  # Refresh the app with the new selection
