"""
Test the process_image_input module.
"""

import unittest

import numpy as np
from PIL import UnidentifiedImageError

from walandmarks.helpers.process_image_input import read_image_data, \
    resize_image, process_image_input

class TestProcessImageInput(unittest.TestCase):
    """
    This class contains the unit tests for the read_image_data, 
    resize_image, and process_image_input functions in the 
    helpers/process_image_input.py file.
    """

    def test_read_image_data(self):
        """
        function to test the read_image_data function
        """
        path = """walandmarks/data/images/Alki Beach/0b03aafd371bb518.jpg"""
        image_data = read_image_data(path)
        self.assertIsInstance(image_data, np.ndarray)

    def test_read_image_data_not_an_image(self):
        """
        function to test the read_image_data function
        """
        image_path = "walandmarks/data/landmark_classes.csv"
        with self.assertRaises(UnidentifiedImageError):
            read_image_data(image_path)

    def test_resize_image(self):
        """
        function to test the resize_image function
        """
        image_data = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        resized_image = resize_image(image_data)
        self.assertEqual(224, resized_image.shape[0])
        self.assertEqual(224, resized_image.shape[1])

    def test_resize_image_new_dimension(self):
        """
        function to test the resize_image function
        """
        image_data = np.asarray([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        dimension = (50, 50, 3)
        resized_image = resize_image(image_data, dimension)
        self.assertEqual(50, resized_image.shape[0])
        self.assertEqual(50, resized_image.shape[1])

    def test_resize_image_filepath(self):
        """
        function to test the resize_image function
        """
        image_data = "walandmarks/data/images/Alki Beach/0b03aafd371bb518.jpg"
        with self.assertRaises(TypeError):
            resize_image(image_data, 50)

    def test_process_image_input(self):
        """
        function to test the process_image_input function
        """
        image_path = "walandmarks/data/images/Alki Beach/0b03aafd371bb518.jpg"
        image_data = process_image_input(image_path)
        self.assertIsInstance(image_data, np.ndarray)

    def test_process_image_input_bad_path(self):
        """
        function to test the process_image_input function
        """
        image_path = "walandmarks/data/landmark_classes.csv"
        with self.assertRaises(UnidentifiedImageError):
            process_image_input(image_path)
