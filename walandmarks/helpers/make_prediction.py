"""
This module contains functions to get the top k predictions 
from the model output
"""

import numpy as np

def get_top_predictions(model_output, top_k=5):
    """
    gets the top k predictions from the model output

    Parameters:
        model_output: output from the model
        top_k: number of top predictions to return
    Returns:
        list of top k predictions
    """
    # argsort() does ascending order, so this reverses it
    top_predictions_indices = np.argsort(model_output)[::-1]

    return [(index, model_output[index]) for index in top_predictions_indices[:top_k]]

def make_prediction(model_output, confidence_threshold=0.5):
    """
    make official predictions using output from the model

    Parameters:
        model_output: output from the model
        confidence_threshold: threshold for confidence
    Returns:
        list of top predictions
    """
    top_prediction = get_top_predictions(model_output, top_k=1)[0]

    if top_prediction[1] > confidence_threshold:
        return [top_prediction]
    return get_top_predictions(model_output, top_k=5)
