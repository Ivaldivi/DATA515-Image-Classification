"""
This module contains the unit tests for the feedback form.
"""

import unittest
from unittest.mock import patch, MagicMock

from walandmarks.helpers import form_handler

class TestFeedbackForm(unittest.TestCase):
    """
    This class contains the unit tests for the feedback form.
    """
    # Tests for verify_form_inputs():
    def test_verify_form_inputs_name_is_string(self):
        """
        Test to check non-string name input throws type error
        """
        with self.assertRaises(TypeError):
            form_handler.verify_form_inputs(1,"email", "sufficient feedback")

    def test_verify_form_inputs_email_is_string(self):
        """
        Test to check non-string email input throws type error
        """
        with self.assertRaises(TypeError):
            form_handler.verify_form_inputs("name", 1, "sufficient feedback")

    def test_verify_form_inputs_feedback_is_string(self):
        """
        Test to check non-string feedback throws type error
        """
        with self.assertRaises(TypeError):
            form_handler.verify_form_inputs("Name", "email", 1)

    @patch("streamlit.error")
    def test_verify_form_inputs_name_non_empty(self, mock_st_error):
        """
        Test an empty name raises a st.error
        """
        form_handler.verify_form_inputs("", "email", "sufficient feedback")
        mock_st_error.assert_called()

    @patch("streamlit.error")
    def test_verify_form_input_correct_raises_no_st_error(self, mock_st_error):
        """
        Making sure there are no errors present when valid input is submitted.
        """
        form_handler.verify_form_inputs("valid input", "valid input", "valid input!")
        mock_st_error.assert_not_called()

    @patch("streamlit.error")
    def test_verify_form_input_empty_feedback(self, mock_st_error):
        """
        Test to check empty feedback raises st.error
        """
        form_handler.verify_form_inputs("name", "email", "")
        mock_st_error.assert_called()

    @patch("streamlit.error")
    def test_verify_form_input_short_feedback(self, mock_st_error):
        """
        Test to check that feedback less than 10 chars raises st.error
        """
        form_handler.verify_form_inputs("name", "email", "not ten")
        mock_st_error.assert_called()

    @patch("streamlit.error")
    def test_verify_form_input_empty_email(self, mock_st_error):
        """
        Test to check empty email raises st.error
        """
        form_handler.verify_form_inputs("name", "", "I love giving feedback!")
        mock_st_error.assert_called()

    def test_convert_urls_to_html_list_input(self):
        """
        Test to check non-list input raises type error
        """
        with self.assertRaises(TypeError):
            form_handler.convert_urls_to_html("not a list")

    def test_convert_urls_to_html_empty_list(self):
        """
        Test to check empty list raises value error
        """
        with self.assertRaises(ValueError):
            form_handler.convert_urls_to_html([])

    def test_convert_urls_to_html_valid_input(self):
        """
        Test to check valid input returns correct output
        """
        urls = ["https://izzys_url.com/image.jpg", "https://annies_url.com/image.jpg"]
        expected_output = '<img src="https://izzys_url.com/image.jpg" width=' \
        '"300"><br><img src="https://annies_url.com/image.jpg" width="300"><br>'
        self.assertEqual(form_handler.convert_urls_to_html(urls), expected_output)

    # Tests for send_email():
    @patch("streamlit.error")
    @patch("streamlit.success")
    @patch("requests.post")
    def test_send_email_requests_post_without_photos(
        self, mock_post, mock_st_success, mock_st_error):
        """
        Test to check that valid input attempts to send an email even 
        if there are no photos. 
        Need to inclue mock_st_error and mock_st_success to avoid
        streamlit warnings when running tests. 
        """
        requests_response = MagicMock()
        requests_response.status_code = 200
        mock_post.return_value = requests_response
        form_handler.send_email("name", "email", "feedback is so cool", None)

        mock_post.assert_called_once()
        mock_st_success.assert_called()
        mock_st_error.assert_not_called()

    @patch("streamlit.error")
    @patch("streamlit.success")
    @patch("requests.post")
    def test_send_email_requests_post_unsuccessful(self, mock_post, mock_st_success, mock_st_error):
        """
        Test to check that an unsuccessful post request raises st.error
        """
        requests_response = MagicMock()
        requests_response.status_code = 400
        mock_post.return_value = requests_response
        form_handler.send_email("name", "email", "feedback is so cool", None)

        mock_post.assert_called_once()
        mock_st_success.assert_not_called()
        mock_st_error.assert_called()

    # Tests for upload_image_to_imgur():
    def test_upload_imgur_image_not_uploaded_file(self):
        """
        Test to check non-UploadedFile input raises type error
        """
        with self.assertRaises(TypeError):
            form_handler.upload_image_to_imgur("String, not an UploadedFile")
