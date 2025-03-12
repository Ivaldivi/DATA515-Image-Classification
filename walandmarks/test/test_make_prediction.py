"""
Test the make_prediction module.
"""

import os
import unittest

import numpy as np
import pandas as pd
import tensorflow as tf

from walandmarks.helpers.make_prediction import make_prediction, get_top_predictions

class TestLoadModel(unittest.TestCase):
    """
    This class contains the unit tests for the get_top_predictions 
    and make_prediction functions in the helpers/make_prediction.py file.
    """

    def test_make_prediction_over_threshold(self):
        """
        function to test the make_prediction function when the 
        best guess is above the confidence threshold
        """
        output = np.array([
            0.8,
            0.05,
            0.15,
            0.0,
            0.0
        ])
        confidence_threshold = 0.4

        actual = make_prediction(output, confidence_threshold)
        expected = [(0, 0.8)]
        self.assertListEqual(expected, actual)

    def test_make_prediction_under_threshold(self):
        """
        function to test the make_prediction function
        when the best guess is below the confidence threshold
        """
        output = np.array([
            0.3,
            0.225,
            0.275,
            0.15,
            0.05
        ])
        confidence_threshold = 0.4

        actual = make_prediction(output, confidence_threshold)
        expected = [(0, 0.3), (2, 0.275), (1, 0.225), (3, 0.15), (4, 0.05)]
        self.assertListEqual(expected, actual)

    def test_get_top_prediction_threshold_5(self):
        """
        function to test the make_prediction function
        when the best guess is below the confidence threshold
        """
        output = np.array([
            0.3,
            0.225,
            0.275,
            0.15,
            0.05
        ])
        top_k = 5

        actual = get_top_predictions(output, top_k)
        expected = [(0, 0.3), (2, 0.275), (1, 0.225), (3, 0.15), (4, 0.05)]
        self.assertListEqual(expected, actual)

    def test_get_top_prediction_threshold_2(self):
        """
        function to test the make_prediction function
        when the best guess is below the confidence threshold
        """
        output = np.array([
            0.3,
            0.225,
            0.275,
            0.15,
            0.05
        ])
        top_k = 2

        actual = get_top_predictions(output, top_k)
        expected = [(0, 0.3), (2, 0.275)]
        self.assertListEqual(expected, actual)

    def test_get_top_prediction_threshold_too_high(self):
        """
        function to test the make_prediction function
        when the best guess is below the confidence threshold
        """
        output = np.array([
            0.3,
            0.225,
            0.275,
            0.15,
            0.05
        ])
        top_k = 10

        actual = get_top_predictions(output, top_k)
        expected = [(0, 0.3), (2, 0.275), (1, 0.225), (3, 0.15), (4, 0.05)]
        self.assertListEqual(expected, actual)