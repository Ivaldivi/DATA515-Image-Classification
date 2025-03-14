"""
Test the load_landmarks module.
"""

import os
import unittest

import pandas as pd

from walandmarks.helpers.load_landmarks import load_landmarks

class TestLoadLandmarks(unittest.TestCase):
    """
    This class contains the unit tests for the load_landmarks function 
    in the helpers/load_landmarks.py file.
    """

    def test_load_landmarks(self):
        """
        function to test the load_landmarks function
        """
        landmark_classes_path = "walandmarks/data/test.csv"

        # create csv
        data = {"landmark_name": ["landmark 1", "landmark 2", "landmark 3"]}
        df = pd.DataFrame(data)
        df.to_csv(landmark_classes_path, index=False)

        # run test case
        landmarks = load_landmarks(landmark_classes_path)
        self.assertListEqual(["landmark 1", "landmark 2", "landmark 3"], landmarks.to_list())

        # delete csv
        if os.path.exists(landmark_classes_path):
            os.remove(landmark_classes_path)

    def test_load_landmarks_length(self):
        """
        test the length of the landmarks
        """
        landmark_classes_path = "walandmarks/data/landmark_classes.csv"
        landmarks = load_landmarks(landmark_classes_path)
        self.assertEqual(296, len(landmarks))

    def test_load_landmarks_bad_path(self):
        """
        test the load_landmarks function with a bad path
        """
        landmark_classes_path = "walandmarks/bad-folder/doesnt-exist.txt"
        with self.assertRaises(TypeError):
            load_landmarks(landmark_classes_path)

    def test_load_landmarks_wrong_filetype(self):
        """
        test the load_landmarks function with the wrong file type passed in
        """
        landmark_classes_path = "walandmarks/images/seattle-skyline.jpg"
        with self.assertRaises(UnicodeDecodeError):
            load_landmarks(landmark_classes_path)
