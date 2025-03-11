"""Test the UI module.
"""

import unittest
from ui.Home import get_title

from streamlit.testing.v1 import AppTest

from ui.helpers.get_data_from_csv import get_data_from_csv

class TestUi(unittest.TestCase):
    """
    This class contains the unit tests for the Home page 
    of the Streamlit app. These tests use Streamlit's 
    AppTest class to simulate the Streamlit app.
    """

    def setUp(self):
        self.at = AppTest.from_file("ui/Home.py").run()
        return super().setUp()

    def test_display_title(self):
        """
        function to test the title of the home page
        """
        assert self.at.title[0].value == "Washington State Landmark Classifier"

    def test_image_seattle_skyline(self):
        """
        function to test the appearance of text input of the search page
        """
        assert self.at.image[0].label == "images/seattle-skyline.jpg"


if __name__ == '__main__':
    unittest.main()
