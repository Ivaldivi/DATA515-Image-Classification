"""
This file contains the unit tests for the 2_Search_Page.py streamlit page 
"""

import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest

from ui.helpers.get_data_from_csv import get_data_from_csv

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



if __name__ == '__main__':
    unittest.main()
