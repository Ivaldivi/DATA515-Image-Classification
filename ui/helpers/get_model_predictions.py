"""
This module is used to get predictions from user-input image
"""

import numpy as np
import pandas as pd
from PIL import Image
from skimage.transform import resize
import tensorflow as tf

from ui.helpers.get_data_from_csv import get_data_from_csv

MODEL = tf.keras.models.load_model(
    "./model/224x224 image classification EfficientNetB0.keras"
)

LANDMARK_CLASSES = get_data_from_csv('data/landmark_classes.csv')
CLASSES = LANDMARK_CLASSES['landmark_name']

def read_image_data(image):
    pil_image = Image.open(image).convert("RGB")
    image_data = np.asarray(pil_image)

    return image_data

def resize_image(image):
    IMAGE_DIMENSION_INPUT = (224, 224, 3)
    IMAGE_SCALAR = 255

    resized_image = resize(np.array(image), IMAGE_DIMENSION_INPUT, anti_aliasing=True)
    resized_image = (resized_image * IMAGE_SCALAR).astype(int)

    return resized_image

def predict_from_image(image):
    image_data = read_image_data(image)
    resized_image = resize_image(image_data)

    input = np.expand_dims(resized_image, axis=0)
    output = MODEL.predict(input)

    return output

def interpret_model_output(model_output):
    prediction_index = np.argmax(model_output)
    prediction = CLASSES[prediction_index]

    return (prediction, model_output[0][prediction_index])

def get_top_five_predictions(model_output):
    # indices of top 5 predictions (via confidence)
    # reverse so it's descending order
    top_five_predictions_indices = (np.argsort(model_output[0])[-5:])[::-1]

    # names of the top 5 and their confidences
    top_five_predictions_classes = CLASSES[top_five_predictions_indices.ravel()]
    top_five_prediction_confidences = model_output[0][top_five_predictions_indices.ravel()]

    return list(zip(top_five_predictions_classes, top_five_prediction_confidences))



