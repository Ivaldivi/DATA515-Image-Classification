import unittest
from ui.helpers.getDataFromCSV import getDataFromCSV
import pandas as pd

class TestSearchPage(unittest.TestCase):

    def test_getDataFromCSV_goodURL(self):
        actual = getDataFromCSV('https://raw.githubusercontent.com/Ivaldivi/DATA515-Image-Classification/refs/heads/main/data/landmarks_washington_full.csv')
        self.assertIsInstance(actual, pd.DataFrame, "Output is not a pandas DataFrame")

    def test_getDataFromCSV_badURL(self):
        actual = getDataFromCSV('https://raw.githubusercontent.com/Ivaldivi/DATA515-Image-Classification/refs/heads/main/data/landmarks_washington.csv')
        self.assertIsNone(actual, "Output is not None")

if __name__ == '__main__':
    unittest.main()