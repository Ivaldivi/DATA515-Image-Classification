"""
This module contains unit tests for the Model Analysis page of the
Streamlit app.
"""

import unittest

from streamlit.testing.v1 import AppTest

class TestModelAnalysis(unittest.TestCase):
    """
    This class contains the unit tests for the Model Analysis page 
    of the Streamlit app. These tests use Streamlit's 
    AppTest class to simulate the Streamlit app.
    """

    def setUp(self):
        path = "walandmarks/ui/pages/3_Model_Analysis.py"
        self.at = AppTest.from_file(path, default_timeout=10).run()
        return super().setUp()

    def test_display_title(self):
        """
        function to test the title
        """
        self.assertEqual(self.at.title[0].value, "Model Analysis")

    def test_subheader_intro(self):
        """
        function to test the intro subheader
        """
        self.assertEqual("Intro", self.at.subheader[0].value)

    def test_markdown_motivation(self):
        """
        function to test the markdown motivation
        """
        expected_motivation = """
        On this page, we will discuss our model implementation and analyze the 
        performance of our model. We will discuss our data sources, our data
        augmentation techniques, and our model architecture. We will also
        show our training and validation loss, accuracy, and AUROC curves, and we will
        discuss our choice of test accuracy metrics and averaging strategy.
        Finally, we will discuss our manual testing process and our confidence cutoff.
        """
        actual_motivation = str(self.at.markdown[0].body).strip()
        expected_motivation = "".join(expected_motivation.split())
        actual_motivation = "".join(actual_motivation.split())
        self.assertEqual(expected_motivation, actual_motivation)

    def test_markdown_intro(self):
        """
        function to test the markdown intro
        """
        expected_intro = """
        Cascadia Classifier is a multiclass image classification model that is
        designed to classify images of landmarks in Washington state. It is backed
        by a convolutional neural network that leverages transfer learning
        to increase the overall accuracy of the classifier.
        """
        actual_intro = str(self.at.markdown[1].body).strip()
        expected_intro = "".join(expected_intro.split())
        actual_intro = "".join(actual_intro.split())
        self.assertEqual(expected_intro, actual_intro)

    def test_subheader_data(self):
        """
        function to test the data subheader
        """
        self.assertEqual("Data", self.at.subheader[1].value)

    def test_markdown_data(self):
        """
        function to test the markdown in the data section
        """
        expected_data = """
        We trained, validated, and tested our model using the Google Landmarks
        dataset, which contains over 2 million images
        of landmarks from around the world. We used the subset of these images that
        were of locations in Washington state. We split this
        data into train, validation, and test sets. We used 64% of the data for
        training, 16% for validation, and 20% for testing.

        We used data augmentation techniques to improve the
        performance of our model. After normalizing our data to a common image
        dimenstion 224x224x3, we utilized flipping, rotation,
        zoom, translation, brightness adjustment, and contrast adjustment
        to increase the diversity of our dataset and
        to improve the generalizability of our model. 

        Finally, we used one-hot encoding to convert the labels into a format
        that could be used by our model. This allowed us to train our model
        using the categorical cross-entropy loss function, which is commonly used
        for multiclass classification problems.
        """
        actual_data = str(self.at.markdown[2].body).strip()
        expected_data = "".join(expected_data.split())
        actual_data = "".join(actual_data.split())
        self.assertEqual(expected_data, actual_data)

    def test_subheader_model_implementation(self):
        """
        function to test the model implementation subheader
        """
        self.assertEqual("Model Implementation", self.at.subheader[2].value)

    def test_markdown_model_implementation(self):
        """
        function to test the markdown in the model implementation section
        """
        expected_model_implementation = """
        We implemented a convolutional neural network using transfer learning.
        We used the EfficientNet B0 model pre-trained on the ImageNet dataset as our
        base model. We then added a global average pooling layer, a batch
        normalization layer, a dropout layer, and a final dense layer with a softmax
        activation function to classify the images into one of the 296 classes.
        We used the Adam optimizer with a learning rate of 0.001 and a batch size
        of 64. We trained our model for 10 epochs, and we used a validation set
        to monitor the performance of our model during training. We utilized early
        stopping to prevent overfitting and
        the categorical cross-entropy loss function to calculate the loss during
        training. We used the TensorFlow and Keras
        libraries to implement our model.

        Our loss, accuracy, and AUROC curves for both training and validation sets are
        given below.
        """
        actual_model_implementation = str(self.at.markdown[3].body).strip()
        expected_model_implementation = "".join(expected_model_implementation.split())
        actual_model_implementation = "".join(actual_model_implementation.split())
        self.assertEqual(expected_model_implementation, actual_model_implementation)

    def test_subheader_test_accuracy(self):
        """
        function to test the test accuracy subheader
        """
        self.assertEqual("Test Accuracy Metrics", self.at.subheader[3].value)

    def test_markdown_test_accuracy(self):
        """
        function to test the markdown in the test accuracy section
        """
        expected_test_accuracy = """
        Finally, we evaluated our model on the test set. We used the following
        metrics to evaluate the performance of our model:
        - Accuracy: The overall accuracy of the model on the test set.
        - Precision: The weighted precision over all classes.
        - Recall: The weighted recall over all classes.
        - Sensitivity: The weighted sensitivity over all classes.
        - Specificity: The weighted specificity over all classes.
        - Balanced Accuracy: The balanced accuracy of the model.

        We used a weighted average to calculate the overall metrics, which takes
        into account the class imbalance in our dataset. We also calculated the
        confusion matrix to visualize the performance of our model for each class.

        The overall accuracy of our model on the test set was 87.0%.

        The accuracy metrics are given below.
        """
        actual_test_accuracy = str(self.at.markdown[4].body).strip()
        expected_test_accuracy = "".join(expected_test_accuracy.split())
        actual_test_accuracy = "".join(actual_test_accuracy.split())
        self.assertEqual(expected_test_accuracy, actual_test_accuracy)

    def test_subheader_manual_testing(self):
        """
        function to test the manual testing subheader
        """
        self.assertEqual("Manual Testing", self.at.subheader[4].value)

    def test_markdown_manual_testing(self):
        """
        function to test the markdown in the manual testing section
        """
        expected_manual_testing = """
        Next, we manually tested our model by providing it images of landmarks
        that were not part of the test set. We were interested in whether the model
        generalized well to images taken by our target users, people attempting to
        classify photos they took of Washington landmarks themselves. We used images
        we had taken for this testing.

        The images were of the Space Needle, the Chinatown gate, Suzzallo library
        at UW, and Drumheller fountain at UW. The model correctly identified the
        Space Needle and Drumheller fountain with high confidence (0.996 and 0.974,
        respectively).
        However, it struggled to identify the Chinatown gate and Suzzallo library. It
        classified the Chinatown gate as
        Pioneer Square with confidence 0.308. Its fourth most likely prediction
        was the Chinatown gate with confidence 0.046. It classified the Suzzallo
        library as Smith Tower with confidence 0.12. The correct prediction was not in
        the top five predictions.

        The images we used are shown below.
        """
        actual_manual_testing = str(self.at.markdown[5].body).strip()
        expected_manual_testing = "".join(expected_manual_testing.split())
        actual_manual_testing = "".join(actual_manual_testing.split())
        self.assertEqual(expected_manual_testing, actual_manual_testing)

    def test_subheader_confidence(self):
        """
        function to test the confidence cutoff subheader
        """
        self.assertEqual("Confidence Cutoff", self.at.subheader[5].value)

    def test_markdown_confidence(self):
        """
        function to test the markdown in the confidence cutoff section
        """
        expected_conf_cutoff = """
        Our manual testing motivated us to consider how we wanted to display
        the model predictions to our user. When the model was confident, we wanted
        to display only the top prediction. However, when the model was not confident,
        we wanted to display the top five predictions. We decided to create a boxplot
        of the confidence of the top prediction for each incorrectly classified image
        in the test set. This boxplot had a median of 0.421 and a mean of 0.439. We
        wanted to err on the side of displaying the top five predictions when the top
        prediction was correct over displaying only one incorrect prediction. We
        decided to use a confidence threshold of 0.5. The boxplot is given below.
        """
        actual_conf_cutoff = str(self.at.markdown[6].body).strip()
        expected_conf_cutoff = "".join(expected_conf_cutoff.split())
        actual_conf_cutoff = "".join(actual_conf_cutoff.split())
        self.assertEqual(expected_conf_cutoff, actual_conf_cutoff)