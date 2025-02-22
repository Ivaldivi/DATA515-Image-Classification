import unittest
from notebooks.image_processing import directory_exists

# EXECUTE USING: 
# python -m unittest test.image_processing_test

class TestImageProcessing(unittest.TestCase):

    def test_existing_directory_name(self):
        actual = directory_exists("Test")
        self.assertTrue(actual)

    def test_missing_directory_name(self): 
        actual2 = directory_exists("Izzys silly directory --> this doesn't exist")
        self.assertFalse(actual2)


if __name__ == '__main__':
    unittest.main()