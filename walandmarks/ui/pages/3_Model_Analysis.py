"""
This file contains the code for the Model Analysis page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Model Analysis - WA Landmark Classifier",
    page_icon="🔎",
)

st.title("Model Analysis")

st.image("walandmarks/images/great-wheel-wide.png", width=800,
         caption="""The Great Wheel in Seattle, WA. Photo by Chris Yang on
         Seattle Pacific University website.""")

st.subheader("Intro")
motivation = """
On this page, we will discuss our model implementation and analyze the 
performance of our model. We will discuss our data sources, our data
augmentation techniques, and our model architecture. We will also
show our training and validation loss, accuracy, and AUROC curves, and we will
discuss our choice of test accuracy metrics and averaging strategy.
Finally, we will discuss our manual testing process and our confidence cutoff.
"""
st.markdown(motivation)

intro = """
Cascadia Classifier is a multiclass image classification model that is
designed to classify images of landmarks in Washington state. It is backed
by a convolutional neural network that leverages transfer learning
to increase the overall accuracy of the classifier.
"""
st.markdown(intro)

st.subheader("Data")
data = """
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
st.markdown(data)

st.subheader("Model Implementation")
model_implementation = """
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
st.markdown(model_implementation)
st.image("walandmarks/model/Loss.png", width=800,
         caption="Training and Validation Loss by Epoch")
st.image("walandmarks/model/Accuracy.png", width=800,
         caption="Training and Validation Accuracy by Epoch")
st.image("walandmarks/model/AUC.png", width=800,
         caption="Training and Validation AUROC by Epoch")

st.subheader("Test Accuracy Metrics")
test_accuracy = """
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
st.markdown(test_accuracy)
test_accuracy_table = pd.DataFrame({
    "Metric": ["Accuracy", "Precision", "Recall", "Sensitivity", 
               "Specificity", "Balanced Accuracy"],
    "Value": [0.8703, 0.8606, 0.8703, 0.8703, 0.9979, 0.9341]
})
st.table(test_accuracy_table)

st.subheader("Manual Testing")
manual_testing = """
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
st.markdown(manual_testing)
st.image("walandmarks/notebooks/personal_test_images/space_needle_1.jpg",
         width=300, caption="Space Needle")
st.image("walandmarks/notebooks/personal_test_images/suzzalo.jpg",
         width=300, caption="Suzzallo Library")
st.image("walandmarks/notebooks/personal_test_images/fountain.jpg",
         width=300, caption="Drumheller Fountain")
st.image("walandmarks/notebooks/personal_test_images/Chinatown_gate.jpg",
         width=300, caption="Chinatown Gate")

st.subheader("Confidence Cutoff")
confidence_cutoff = """
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
st.markdown(confidence_cutoff)
st.image("walandmarks/model/DistIncorrectTopGuessConfidence.png", width=800,
         caption="""Boxplot of the confidence of the top prediction for each
                    incorrectly classified image in the test set.""")
