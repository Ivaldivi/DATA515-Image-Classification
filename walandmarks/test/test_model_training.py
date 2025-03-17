"""
This file is used to test 
landmark_classification_model_training.py file.
"""

import unittest

import keras
import pandas as pd

import walandmarks.helpers.landmark_classification_model_training as cm

class TestLandmarkClassificationModelTraining(unittest.TestCase):
    """
    This class contains the unit tests for the landmark classification
    model training functions in the 
    landmarks_classification_model_training.py file.
    """
    # Tests for create_model_architecture:
    def test_model_architecture_num_classes_not_int(self):
        """
        Function to test create_model_architecture
        when num_classes is not an integer
        """
        with self.assertRaises(TypeError):
            cm.create_model_architecture("number of classes", 0.5, (1,1,1))
    def test_model_architecture_dropout_rate_not_float(self):
        """
        Function to test create_model_architecture
        when dropout_rate is not a float
        """
        with self.assertRaises(TypeError):
            cm.create_model_architecture(5, "dropout rate", (1,1,1))
    def test_model_architecture_input_shape_not_tuple(self):
        """
        Function to test create_model_architecture
        raises value error when input_shape is not a tuple
        """
        with self.assertRaises(TypeError):
            cm.create_model_architecture(5, 0.5, "not a tuple")

    def test_model_architecture_returns_keras_model(self):
        """
        Function to check that create_model_architecture 
        returns a keras model
        """
        actual = cm.create_model_architecture(300, 0.5, (224, 224, 3))
        self.assertIsInstance(actual, keras.Model)

    # Tests for load_model_data():
    def test_load_model_returns_pd_dataframe(self):
        """
        Function to check that load_model_data
        returns a pandas DataFrame
        """
        actual = cm.load_model_data()
        self.assertIsInstance(actual, pd.DataFrame)

    def test_load_model_data_columns(self):
        """
        Function to check that the datafram that's returned
        has the correct columns. 
        """
        actual = cm.load_model_data()
        expected_columns = ['file_path', 'parent_file_path', 'name', 'image_id', 'image_data']
        actual_columns = list(actual.columns)
        print(f'actual_columns: {actual_columns}')
        self.assertListEqual(expected_columns, actual_columns)
