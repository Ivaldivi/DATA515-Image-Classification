import unittest
from ui.Home import get_title

class TestUi(unittest.TestCase):

    def test_get_title(self):
        expected = 'Washington State Landmark Classifier'
        actual = get_title()
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()