"""
This module contains the unit tests for the feedback form.
"""

import unittest
from unittest.mock import patch, MagicMock
import ui.helpers.form_handler as form_handler
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


class TestFeedbackForm(unittest.TestCase):
    """
    This class contains the unit tests for the feedback form.
    """

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
