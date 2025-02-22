import unittest
from notebooks.image_processing import create_directory

# EXECUTE USING: 
# python -m unittest test.image_proessing_test

class TestUi(unittest.TestCase):

    def test_print_directory_name(self):
        expected = "The directory Test exists"
        actual = create_directory("Test")
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()