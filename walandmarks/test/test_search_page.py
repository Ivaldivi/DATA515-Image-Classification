"""
This file contains the unit tests for the 2_Search_Page.py streamlit page 
"""

import unittest

import numpy as np
import pandas as pd
from streamlit.testing.v1 import AppTest

from walandmarks.ui.helpers.get_data_from_csv import get_data_from_csv

class TestSearchPage(unittest.TestCase):
    """
    This class contains the unit tests for the getDataFromCSV function
    """

    def test_display_title(self):
        """
        function to test the title of the search page
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        assert at.title[0].value == "Washington Landmarks Search"

    def test_display_text_input(self):
        """
        function to test the appearance of text input of the search page
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        assert at.text_input[0].label == "Search for a landmark by name"
    
    def test_if_no_text_input(self):
        """
        function to test the message when no text is input
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        assert at.markdown[0].value == "Enter a landmark name to search for it."

    def test_if_text_input_and_no_match(self):
        """
        function to test the message when text is input but no match is found
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        at.text_input[0].set_value("University of Virginia").run()
        assert at.markdown[0].value == "No landmarks found. Try another search."

    def test_if_text_input_and_exact_match(self):
        """
        function to test the display of an exact match
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        search_string = "Mount Rainier"
        at.text_input[0].set_value(search_string).run()
        landmarks_df = get_data_from_csv('data/landmarks_washington_full.csv')
        pics_df = get_data_from_csv('data/landmarks_washington_clean_images.csv')
        landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')
        search_results = landmarks_df_join[landmarks_df_join['name'] == search_string].iloc[0]
        expected_name = search_results['name']
        expected_category = search_results['supercategory']
        expected_location = search_results['location']

        assert at.header[0].value == expected_name
        assert at.markdown[0].value == f"<b>Category:</b> {expected_category}"
        assert at.markdown[1].value == f"<b>Location:</b> {expected_location}"

        # add testing for image and map display
    
    def test_if_text_input_and_partial_match_button_display(self):
        """
        function to test the display of a partial match
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        search_string = "Mount"
        at.text_input[0].set_value(search_string).run()
        landmarks_df = get_data_from_csv('data/landmarks_washington_full.csv')
        pics_df = get_data_from_csv('data/landmarks_washington_clean_images.csv')
        landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')
        search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                        search_string, case=False, na=False, regex = True)]
        expected_names = np.sort(search_results['name'].unique())

        for i in range(len(at.button)):
            assert at.button[i].label == expected_names[i]

    def test_if_text_input_and_partial_match_button_function(self):
        """
        function to test clicking a partial match button changes the text input
        """
        at = AppTest.from_file("ui/pages/2_Search_Page.py").run()
        search_string = "Mount"
        at.text_input[0].set_value(search_string).run()
        landmarks_df = get_data_from_csv('data/landmarks_washington_full.csv')
        pics_df = get_data_from_csv('data/landmarks_washington_clean_images.csv')
        landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')
        search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                        search_string, case=False, na=False, regex = True)]
        expected_names = np.sort(search_results['name'].unique())
        at.button[0].click().run()
        assert at.text_input[0].value == expected_names[0]
        assert at.header[0].value == expected_names[0]

if __name__ == '__main__':
    unittest.main()
