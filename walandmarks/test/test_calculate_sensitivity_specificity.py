"""
Tests for the calculate_sensitivity_specificity function.
"""

import unittest

import numpy as np

from walandmarks.helpers.calculate_sensitivity_specificity import weighted_sensitivity_specificity

class TestCalculateSensitivitySpecificity(unittest.TestCase):
    """
    This class contains the unit tests for the
    calculate_sensitivity_specificity function.
    """

    def test_calculate_sensitivity_specificity(self):
        """
        Test the function with a 2x2 confusion matrix.
        """
        confusion = [[5, 1],
                     [0, 3]]
        expected_sensitivity = 8 / 9
        expected_specificity = 17 / 18
        sensitivity, specificity = weighted_sensitivity_specificity(confusion)
        self.assertAlmostEqual(sensitivity, expected_sensitivity)
        self.assertAlmostEqual(specificity, expected_specificity)

    def test_calculate_sensitivity_specificity_zero(self):
        """
        Test with all zeros in the confusion matrix.
        """
        confusion = np.array([[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]])
        expected_sensitivity = 0
        expected_specificity = 0
        sensitivity, specificity = weighted_sensitivity_specificity(confusion)
        self.assertEqual(sensitivity, expected_sensitivity)
        self.assertEqual(specificity, expected_specificity)

    def test_calculate_sensitivity_specificity_single_element(self):
        """
        Test with a single element in the confusion matrix.
        """
        confusion = [[5]]
        expected_sensitivity = 1
        expected_specificity = 0
        sensitivity, specificity = weighted_sensitivity_specificity(confusion)
        self.assertEqual(sensitivity, expected_sensitivity)
        self.assertEqual(specificity, expected_specificity)

    def test_calculate_sensitivity_specificity_invalid_input(self):
        """
        Ensure an error is called when the confusion matrix is not a matrix.
        """
        confusion = [[5, 1],
                     [0, 3, 1]]
        with self.assertRaises(ValueError):
            weighted_sensitivity_specificity(confusion)


if __name__ == '__main__':
    unittest.main()
