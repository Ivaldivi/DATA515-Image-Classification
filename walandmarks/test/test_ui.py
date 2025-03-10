"""Test the UI module.
"""

import unittest
from walandmarks.ui.Home import get_title

class TestUi(unittest.TestCase):
    """
    This class contains the unit tests for the UI module.
    """
    def test_get_title(self):
        """
        Test the get_title function.
        """
        expected = 'Washington State Landmark Classifier'
        actual = get_title()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
