"""
This module contains the unit tests for the feedback form.
"""

import unittest

import ui.helpers.form_handler as form_handler


class TestFeedbackForm(unittest.TestCase):
    """
    This class contains the unit tests for the feedback form.
    """
    def test_upload_image_to_imgur(self):
        """
        Test the upload_image_to_imgur function.
        """
        with self.assertRaises(TypeError):
            form_handler.upload_image_to_imgur('image')

    def test_upload_returns_none_if_no_image(self): 
        """
        Test that the function returns None if no image is uploaded
        """
        actual = form_handler.upload_image_to_imgur("image")
        self.assertIsNone(actual)
        
    @unittest.mock.patch('requests.post')
    def test_upload_returns_none_if_bad_imgur_response(self, mock_post):
        """
        Test that the function returns None if the imgur HTML response is not 200.
        """
        mock_post.return_value.status_code = 400
        actual = form_handler.upload_image_to_imgur("image")
        self.assertIsNone(actual)
        
