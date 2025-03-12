"""
This file contains the unit tests for the 2_Search_Page.py streamlit page 
"""
import unittest

import numpy as np
from streamlit.testing.v1 import AppTest

from walandmarks.ui.helpers.get_data_from_csv import get_data_from_csv

class TestSearchPage(unittest.TestCase):
    """
    This class contains the unit tests for the getDataFromCSV function
    """
    def setUp(self):
        self.at = AppTest.from_file("walandmarks/ui/pages/2_Search_Page.py").run()

    def test_display_title(self):
        """
        function to test the title of the search page
        """
        self.assertEqual(self.at.title[0].value, "Washington Landmarks Search")

    def test_display_text_input(self):
        """
        function to test the appearance of text input of the search page
        """
        self.assertEqual(self.at.text_input[0].label, "Search for a landmark by name")

    def test_if_no_text_input(self):
        """
        function to test the message when no text is input
        """
        self.assertEqual(self.at.markdown[0].value, "Enter a landmark name to search for it.")

    def test_if_text_input_and_no_match(self):
        """
        function to test the message when text is input but no match is found
        """
        self.at.text_input[0].set_value("University of Virginia").run()
        self.assertEqual(self.at.markdown[0].value, "No landmarks found. Try another search.")

    def test_if_text_input_and_exact_match(self):
        """
        function to test the display of an exact match
        """
        search_string = "Mount Rainier"
        self.at.text_input[0].set_value(search_string).run()
        landmarks_df = get_data_from_csv('walandmarks/data/landmarks_washington_full.csv')
        pics_df = get_data_from_csv('walandmarks/data/landmarks_washington_clean_images.csv')
        landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')
        search_results = landmarks_df_join[landmarks_df_join['name'] == search_string].iloc[0]
        expected_name = search_results['name']
        expected_category = search_results['supercategory']
        expected_location = search_results['location']
        expected_image = search_results['url']
        self.assertEqual(self.at.header[0].value, expected_name)
        self.assertEqual(self.at.markdown[0].value, f"<b>Category:</b> {expected_category}")
        self.assertEqual(self.at.markdown[1].value, f"<b>Location:</b> {expected_location}")
        cur_image_url = self.at.get('imgs')[0].proto.imgs[0].url
        self.assertEqual(cur_image_url, expected_image)

    def test_if_text_input_and_partial_match_button_display(self):
        """
        function to test the display of a partial match
        """
        search_string = "Mount"
        self.at.text_input[0].set_value(search_string).run()
        landmarks_df = get_data_from_csv('walandmarks/data/landmarks_washington_full.csv')
        pics_df = get_data_from_csv('walandmarks/data/landmarks_washington_clean_images.csv')
        landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')
        search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                        search_string, case=False, na=False, regex = True)]
        expected_names = np.sort(search_results['name'].unique())
        for i in enumerate(self.at.button):
            self.assertEqual(i[1].label, expected_names[i[0]])

    def test_if_text_input_and_partial_match_button_function(self):
        """
        function to test clicking a partial match button changes the text input
        """
        search_string = "Mount"
        self.at.text_input[0].set_value(search_string).run()
        landmarks_df = get_data_from_csv('walandmarks/data/landmarks_washington_full.csv')
        pics_df = get_data_from_csv('walandmarks/data/landmarks_washington_clean_images.csv')
        landmarks_df_join = landmarks_df.merge(pics_df, how='right', on='landmark_id')
        search_results = landmarks_df_join[landmarks_df_join['name'].str.contains(
                        search_string, case=False, na=False, regex = True)]
        expected_names = np.sort(search_results['name'].unique())
        self.at.button[0].click().run()
        self.assertEqual(self.at.text_input[0].value, expected_names[0])
        self.assertEqual(self.at.header[0].value, expected_names[0])

if __name__ == '__main__':
    unittest.main()
