"""
This file contains the unit tests for the helpers/get_landmark_details function 
"""

import unittest

import pandas as pd

from walandmarks.helpers.get_landmark_details import get_landmark_details

class TestGetLandmarkDetails(unittest.TestCase):
    """
    This class contains the unit tests for the helpers/get_landmark_details function
    """

    def test_get_location_from_valid_landmark_id(self):
        """function to test location return of the get_landmark_details
        with valid landmark_id
        """
        details_dict = get_landmark_details(2509)
        details_dict_location_actual = details_dict['location']
        details_dict_location_expected = 'Washington, King County, United States'
        self.assertEqual(details_dict_location_actual, details_dict_location_expected, "Location is not as expected")
    
    def test_get_category_from_valid_landmark_id(self):
        """function to category return of the get_landmark_details
        with valid landmark_id
        """
        details_dict = get_landmark_details(2509)
        details_dict_category_actual = details_dict['category']
        details_dict_category_expected = 'mountain'
        self.assertEqual(details_dict_category_actual, details_dict_category_expected, "Category is not as expected")


if __name__ == '__main__':
    unittest.main()