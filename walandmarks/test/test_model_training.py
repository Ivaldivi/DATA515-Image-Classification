"""
This file is used to test 
landmark_classification_model_training.py file.
"""

# pylint: disable=too-many-public-methods
# disabling too many public methods because there are more than 20
# tests needed to test the functions in the file.

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

import keras
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

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

    def test_cma_dropout_above_one_raises_value_error(self):
        """
        Function that tests if a value error is raised if the
        dropout rate is above 1.0.
        """
        with self.assertRaises(ValueError):
            cm.create_model_architecture(4, 2.0, (224,224,3))

    def test_cma_dropout_below_zero_raises_value_error(self):
        """
        Function that tests if a value error is raised if the
        dropout rate is below 0.0.
        """
        with self.assertRaises(ValueError):
            cm.create_model_architecture(4,-1.0, (224,224,3))


    # Tests for load_model_data():
    def test_load_model_returns_pd_dataframe(self):
        """
        Function to check that load_model_data
        returns a pandas DataFrame.
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
        self.assertListEqual(expected_columns, actual_columns)

    # Tests for create_train_test_val_split():
    def test_train_test_val_split_returns_six_items(self):
        """
        Function to check that create_train_test_split
        returns six lists.
        """
        washington_data_cleaned = cm.load_model_data()[['name', 'image_id', 'image_data']]
        encoder = OneHotEncoder(handle_unknown='ignore').fit(
        pd.DataFrame(washington_data_cleaned['name'])
        )

        actual = cm.create_train_test_val_split(
        np.stack(washington_data_cleaned['image_data'], axis=0), encoder.transform(
            pd.DataFrame(washington_data_cleaned['name'])
        ).toarray()
        )
        self.assertEqual(len(actual), 6)

    def test_train_test_val_split_returns_ndarrays(self):
        """
        Function to check that create_train_test_val
        split returns numpy nd arrays.
        """
        washington_data_cleaned = cm.load_model_data()[['name', 'image_id', 'image_data']]
        encoder = OneHotEncoder(handle_unknown='ignore').fit(
        pd.DataFrame(washington_data_cleaned['name'])
        )

        actual = cm.create_train_test_val_split(
        np.stack(washington_data_cleaned['image_data'], axis=0), encoder.transform(
            pd.DataFrame(washington_data_cleaned['name'])
        ).toarray()
        )
        for item in actual:
            self.assertEqual(type(item), np.ndarray)

    # Tests for train_model():
    def test_non_keras_model_raises_type_error(self):
        """
        Function that checks train_model raises type error
        if model is not a keras model
        """
        x_train, y_train, x_val, y_val = [np.ndarray(3) for i in range(4)]

        with self.assertRaises(TypeError):
            cm.train_model("not a keras model", x_train, y_train, x_val, y_val)

    def test_train_model_raises_type_error_for_non_ndarray_input(self):
        """
        Function that checks train_model raises a type error 
        if x_train is not an np.ndarray
        """
        mocked_model = keras.Model()
        x_train = "Not an ndarray"
        y_train, x_val, y_val = [np.ndarray(3) for i in range(3)]
        with self.assertRaises(TypeError):
            cm.train_model(mocked_model, x_train, y_train, x_val, y_val)

    def test_size_of_data_augmentation_(self):
        """
        Function that checks that create_data_augmentation
        has 6 layers. 
        """
        actual = cm.create_data_augmentation()
        self.assertEqual(len(actual.layers), 6)

    def test_create_data_augmentation_returns_keras_sequential(self):
        """
        Function to check that create_data_augmentation
        returns keras.Sequential object.
        """
        actual = cm.create_data_augmentation()
        self.assertIsInstance(actual, keras.Sequential)

    def test_train_model_returns_tuple(self):
        """
        Function that checks that train_model returns a tuple.
        """
        x_train, y_train, x_val, y_val = [np.ndarray(3) for i in range(4)]
        mocked_model = MagicMock(spec=keras.Model)
        actual = cm.train_model(mocked_model, x_train, y_train, x_val, y_val)
        self.assertIsInstance(actual, tuple)

    # Tests for plot_model_metric():
    def test_plot_model_metric_raises_type_error_if_metric_not_str(self):
        """
        Function that checks plot_model_metric raises a type error
        if metric is not a string. 
        """
        with self.assertRaises(TypeError):
            cm.plot_model_metric(keras.callbacks.History, 5,
                                 "./path/to/save/plot.png")

    def test_plot_model_metric_raises_type_error_if_history_not_keras_history(self):
        """
        Function that checks plot_model_metric raises a type error
        if history is not a keras history object. 
        """
        with self.assertRaises(TypeError):
            cm.plot_model_metric("not a keras history object", "accuracy",
                                 "./path/to/save/plot.png")

    def test_plot_model_metric_raises_value_error_if_metric_not_allowed(self):
        """
        Function that checks plot_model_metric raises a value error 
        if the metric chosen isn't 'loss', 'accuracy' or 'auc'.
        """
        with self.assertRaises(ValueError):
            cm.plot_model_metric(keras.callbacks.History(), "a string, but not"
            "a valid metric", "./path/to/save/plot.png")

    @patch('matplotlib.pyplot.show')
    def test_plot_model_metric_calls_plt_show(self, mock_show):
        """
        Check that plt.show() is called in plot_model_metric.
        If the inputs are valid, then it plt.show() should be called 
        only once.
        """
        mocked_model_history = MagicMock(spec=keras.callbacks.History)
        mocked_model_history.history = {"accuracy": [.12,.32,.34,.44],
                                        "val_accuracy": [.12,.34,.54,.55]}
        cm.plot_model_metric(mocked_model_history, "accuracy",
                             "walandmarks/test/outputs/plot.png")
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.xlabel')
    def test_plot_metric_accuracy_x_axis_label(self, mock_x_label):
        """
        Function to check that the plot x-axis label is 'Epoch'
        """
        mocked_model_history = MagicMock(spec=keras.callbacks.History)
        mocked_model_history.history = {"accuracy": [.12,.32,.34,.44],
                                        "val_accuracy": [.12,.34,.54,.55]}
        cm.plot_model_metric(mocked_model_history, "accuracy",
                             "walandmarks/test/outputs/plot.png")
        mock_x_label.assert_called_once_with('Epoch')

    # Tests for save_model():
    def test_save_model_raises_type_error_if_model_path_not_string(self):
        """
        Check if save_model raises a TypeError if model_path
        is not a string.
        """
        with self.assertRaises(TypeError):
            cm.save_model(5, keras.Model())

    def test_save_model_raises_type_error_if_model_not_keras_object(self):
        """
        Check save_model raises TypeError if model is not a keras object.
        """
        with self.assertRaises(TypeError):
            cm.save_model("string", "Not a keras model...")

    # tests for load_image():
    def test_load_image_raises_type_error_if_path_not_string(self):
        """
        Function that checks load_image raises a TypeError
        if the image_path provided is not a string.
        """
        with self.assertRaises(TypeError):
            cm.load_image(23)

    # tests for test_model_on_test_data():
    def test_test_model_on_test_data_raises_type_error_if_model_not_keras_model(self):
        """
        Function that checks test_model_on_test_data raises a
        TypeError if the model provided is not a keras model.
        """
        with self.assertRaises(TypeError):
            cm.test_model_on_test_data("not a keras model", np.ndarray(3), np.ndarray(3))

    def test_test_model_on_test_data_raises_type_error_if_x_test_not_ndarray(self):
        """
        Function that checks test_model_on_test_data raises a
        TypeError if x_test is not a numpy ndarray.
        """
        with self.assertRaises(TypeError):
            cm.test_model_on_test_data(keras.Model(), "not an ndarray", np.ndarray(3))

    def test_test_model_on_test_data_raises_type_error_if_y_test_not_ndarray(self):
        """
        Check test_model_on_test_data raises a TypeError if y_test is not a numpy ndarray.
        """
        with self.assertRaises(TypeError):
            cm.test_model_on_test_data(keras.Model(), np.ndarray(3), "not an ndarray")

    @patch('keras.Model.evaluate')
    def test_test_model_on_test_data_retruns_tuple(self, mock_evaluate):
        """
        Function that checks test_model_on_test_data returns tuple.
        """
        mock_evaluate.return_value = (0.5,0.5,0.5,0.5)
        actual = cm.test_model_on_test_data(keras.Model(), np.ndarray(3), np.ndarray(3))
        self.assertEqual(type(actual), tuple)

    # Tests for create_train_analyze_model:
    def test_create_train_analyze_model_raises_type_error_if_save_model_flag_not_bool(self):
        """ 
        Check create_train_analyze raises type error if save_model flag is not boolean
        """
        with self.assertRaises(TypeError):
            cm.create_train_analyze_model("not a boolean", "walandmarks/model/test.keras")

    def test_create_train_analyze_model_raises_type_error_if_save_model_pathname_not_str(self):
        """
        Check create_train_analyze_model raises a TypeError
        if path to save model is not a string. 
        """
        with self.assertRaises(TypeError):
            cm.create_train_analyze_model(False, 5, 'loss/path', 'accuracy/path', 'auc/path')

    def test_create_train_analyze_model_raises_type_error_if_loss_pathname_not_str(self):
        """
        Check create_train_analyze_model raises a TypeError
        if path to save loss plot is not a string. 
        """
        with self.assertRaises(TypeError):
            cm.create_train_analyze_model(False, 'model/path', 5,
                                          'accuracy/path', 'auc/path')

    def test_create_train_analyze_model_raises_type_error_if_accuracy_pathname_not_str(self):
        """
        Check create_train_analyze_model raises a TypeError
        if path to save accuracy plot is not a string. 
        """
        with self.assertRaises(TypeError):
            cm.create_train_analyze_model(False, 'model/path', 'loss/path',
                                          5, 'auc/path')

    def test_create_train_analyze_model_raises_type_error_if_auc_pathname_not_str(self):
        """
        Check create_train_analyze_model raises a TypeError
        if path to save AUC plot is not a string. 
        """
        with self.assertRaises(TypeError):
            cm.create_train_analyze_model(False, 'model/path', 'loss/path',
                                          'accuracy/path', 5)
