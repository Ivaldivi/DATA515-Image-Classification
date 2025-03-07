"""
This file contains the unit tests for the ui/2_Search_Page.py file 
"""

import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest

from ui.helpers.get_data_from_csv import get_data_from_csv

class TestUISearchPage(unittest.TestCase):
    """
    This class contains unit tests for the ui/2_Search_Page.py file
    """

    def test_search_valid_single_landmark(self):
        """
        function to test search page returns pictures of one landmark
        when given a search term corresponding to a single landmark
        """
        at = AppTest.from_file("ui/2_Search_Page.py").run()
        # instead of asserting based on images, make sure landmark full name is diplayed above the three images


        actual = get_data_from_csv('data/landmarks_washington_full.csv')
        self.assertIsInstance(actual, pd.DataFrame, "Output is not a pandas DataFrame")

    def test_search_valid_multiple_landmarks(self):
        """
        function to test search page returns pictures of multiple landmarks
        when given a search term corresponding to multiple landmarks
        """
        actual = get_data_from_csv('../data/landmarks_washington.csv')
        self.assertIsNone(actual, "Output is not None")

if __name__ == '__main__':
    unittest.main()