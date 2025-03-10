"""
This file contains the code for the Search page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import streamlit as st
import pandas as pd

from helpers.get_data_from_csv import get_data_from_csv


# Page setup
st.set_page_config(page_title =
                   "Washington Landmarks Search",
                   page_icon = ":mag_right:", layout = "wide")
st.title("Washington Landmarks Search")

# Connect to data for search
landmarks_df = get_data_from_csv('walandmarks/data/landmarks_washington_full.csv')
pics_df = get_data_from_csv('walandmarks/data/landmarks_washington_clean_images.csv')

# right join landmarks_df and pics_df on 'landmark_id' column to remove
# any landmarks that had bad urls
landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')

# initialize session state
if "selected_landmark" not in st.session_state:
    st.session_state.selected_landmark = ""

text_search = st.text_input("Search for a landmark by name", st.session_state.selected_landmark)


search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                    text_search, case=False, na=False)]

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
                st.markdown("**Supercategory:**"+exact_match['supercategory'].iloc[0])
                st.markdown("**Location:**"+exact_match['location'].iloc[0])
                # need to add images here
            with col2:
                #st.map(exact_match)
                df = pd.DataFrame(exact_match[['latitude', 'longitude']])
                df['longitude'] = -df['longitude']
                print(df)
                st.map(df)
        #st.write(exact_match['supercategory'].iloc[0])
    # if there is a partial match provide buttons of the suggested full names
    else:
        # Suggest similar names as clickable buttons
        st.write("Did you mean:")
        for name in search_results['name'].unique():
            if st.button(name):
                st.session_state.selected_landmark = name
                st.rerun()  # Refresh the app with the new selection

    # # Display images
    # N_PICS_PER_ROW = 3
    # # If there has been text input but there are no results, display a message
    # if search_results.empty:
    #     st.write("No landmarks found. Please try again.")
    # else:
    #     # if the search term is exactly the name of a landmark, display landmark facts

    #     # if the search term is a substring of a landmark name, display suggested full landmark names

    #     # if the search term is exactly the name of a landmark, display landmark facts
    #     if search_results['name'].upper() == text_search.upper():
    #         st.write(search_results['name'].iloc[0])
    #         st.write(search_results['description'].iloc[0])
    #         st.image(search_results['url'].iloc[0], width=200, caption=search_results['name'].iloc[0])
    #     elif search_results['name'].str.upper().str.contains(text_search.upper()).any():
    #         st.write("Did you mean:")
    #         st.write(search_results['name'].unique())
        

    #     short_results_list = []

    #     # display at most three images per landmark
    #     # need to resize images so they are same size
    #     # this should probably go into a function that I test
    #     for landmark_id in search_results['landmark_id'].drop_duplicates():
    #         landmark_short = search_results[search_results['landmark_id'] == landmark_id].head(3)
    #         short_results_list.append(landmark_short)

    #     short_results = pd.concat(short_results_list, ignore_index = True)

    #     for i in range(0, len(short_results), N_PICS_PER_ROW):
    #         row = short_results.iloc[i:i + N_PICS_PER_ROW]
    #         st.image(row['url'].tolist(), width=200, caption=row['name'].tolist())
