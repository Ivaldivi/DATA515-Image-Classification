"""
Contains functions for processing image input for model prediction
"""
# pylint: disable=no-name-in-module
# Pylint attribute disabled because incorrect. It stated:
# "E0611: No name 'resize' in module 'skimage.transform'", but
# skimage.transform does have a function named resize. Code has
# been tested and works as expected.

import numpy as np
from PIL import Image
from skimage.transform import resize

def read_image_data(image):
    """
    reads image data from file
    parameters:
        image: image file
    returns:
        image
    """
    pil_image = Image.open(image).convert("RGB")
    image_data = np.asarray(pil_image)

    return image_data

def resize_image(image, image_dimension=(224, 224, 3)):
    """
    resizes image to new dimensions
    parameters:
        image: image data
        image_dimension: new image dimensions
    returns:
        resized_image: resized image data
    """
    image_scalar = 255

    resized_image = resize(np.array(image), image_dimension, anti_aliasing=True)
    resized_image = (resized_image * image_scalar).astype(int)

    return resized_image

def process_image_input(image):
    """
    processes input image for model prediction
    parameters:
        image: image file
    returns:
        image_input: image data for model prediction
    """
    image_data = read_image_data(image)
    resized_image = resize_image(image_data)
    image_input = np.expand_dims(resized_image, axis=0)

    return image_input
