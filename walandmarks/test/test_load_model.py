"""
Test the load_model module.
"""
# pylint: disable=no-member
# Pylint attribute disabled because incorrect. It stated:
# "E1101:Module 'tensorflow' has no 'keras' member", but tensorflow does
# have a keras member. Code has been tested and works as expected.

import os
import unittest

import tensorflow as tf

from walandmarks.helpers.load_model import load_model

class TestLoadModel(unittest.TestCase):
    """
    This class contains the unit tests for the load_model function 
    in the helpers/load_model.py file.
    """

    def test_load_model_empty(self):
        """
        function to test the load_model function
        """
        model_path = "walandmarks/model/test_model.keras"

        # create empty model
        model = tf.keras.models.Sequential()
        model.save(model_path)

        # run test
        loaded_model = load_model(model_path)
        self.assertIsInstance(loaded_model, tf.keras.models.Sequential)

        # delete model
        if os.path.exists(model_path):
            os.remove(model_path)

    def test_load_model_full(self):
        """
        function to test the load_model function
        """
        model_path_full = "walandmarks/model/test_model.keras"
        loaded_model = load_model(model_path_full)
        self.assertIsInstance(loaded_model, tf.keras.models.Sequential)

    def test_load_model_bad_path(self):
        """
        function to test passing a bad path into the load_model function
        """
        model_path = "walandmarks/bad-folder/test_model.keras"
        with self.assertRaises(ValueError):
            load_model(model_path)
