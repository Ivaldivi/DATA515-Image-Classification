"""
This file contains the unit tests for the getDataFromCSV function 
"""

import unittest

import pandas as pd

from ui.helpers.get_data_from_csv import get_data_from_csv

class TestSearchPage(unittest.TestCase):
    """
    This class contains the unit tests for the getDataFromCSV function
    """

    def test_get_data_from_csv_good_file_path(self):
        """function to test the getDataFromCSV function
        with valid file path
        """

        actual = get_data_from_csv('data/landmarks_washington_full.csv')
        self.assertIsInstance(actual, pd.DataFrame, "Output is not a pandas DataFrame")

    def test_get_data_from_csv_bad_file_path(self):
        """function to test the getDataFromCSV function
        with invalid file path
        """
        actual = get_data_from_csv('../data/landmarks_washington.csv')
        self.assertIsNone(actual, "Output is not None")

if __name__ == '__main__':
    unittest.main()
