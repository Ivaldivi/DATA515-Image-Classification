"""
Test the classifier module.
"""
import unittest
from unittest.mock import MagicMock, patch

from streamlit.testing.v1 import AppTest

class TestClassifier(unittest.TestCase):
    """
    This class contains the unit tests for the Classifier page 
    of the Streamlit app. These tests use Streamlit's 
    AppTest class to simulate the Streamlit app. They test the 
    functionality of the UI, not the model itself.
    """

    def setUp(self):
        self.at = AppTest.from_file("walandmarks/ui/pages/1_Classifier.py", default_timeout=10).run()
        return super().setUp()

    def test_display_title(self):
        """
        function to test the title of the home page
        """
        self.assertEqual(self.at.title[0].value, "Classifier")

    def test_markdown_about_section(self):
        """
        function to test that the markdown elements of the about section are 
        as expected, plus or minus whitespace.
        """

        expected_about = """
        Welcome to the Washington State Landmark Classifier. To classify
        your image, upload it using the button below. We will give 
        you the top five most likely places your image depicts.
        """

        expected_about = "".join(expected_about.split()) # remove whitespace
        actual_about = str(self.at.markdown[0].body).strip()
        actual_about = "".join(actual_about.split()) # remove whitespace
        self.assertEqual(expected_about, actual_about)

    def test_file_uploader(self):
        """
        function to test that the file uploader widget is configured 
        correctly.
        """
        file_uploader = self.at.get('file_uploader')[0]
        self.assertEqual(file_uploader.label, 
                         'Upload your image here. Must be a .png or .jpg file that is 200MB or less.')
        self.assertEqual(file_uploader.type, 'file_uploader')
        self.assertEqual(file_uploader.help, 
                         'Image must be a .png, .jpg, or .jpeg file that is 200MB or less.')


if __name__ == '__main__':
    unittest.main()
