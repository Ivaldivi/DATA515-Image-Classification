import numpy as np

def get_top_predictions(model_output, top_k=5):
    # argsort() does ascending order, so this reverses it
    top_predictions_indices = np.argsort(model_output)[::-1]

    return [(index, model_output[index]) for index in top_predictions_indices[:top_k]]

def make_prediction(model_output, confidence_threshold=0.4):
    top_prediction = get_top_predictions(model_output, top_k=1)[0]

    if top_prediction[1] > confidence_threshold:
        return [top_prediction]
    else:
        return get_top_predictions(model_output, top_k=5)