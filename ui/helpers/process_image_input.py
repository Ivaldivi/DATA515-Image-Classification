import numpy as np
from PIL import Image
from skimage.transform import resize

def read_image_data(image):
    pil_image = Image.open(image).convert("RGB")
    image_data = np.asarray(pil_image)

    return image_data

def resize_image(image, image_dimension=(224, 224, 3)):
    IMAGE_SCALAR = 255

    resized_image = resize(np.array(image), image_dimension, anti_aliasing=True)
    resized_image = (resized_image * IMAGE_SCALAR).astype(int)

    return resized_image

def process_image_input(image):
    image_data = read_image_data(image)
    resized_image = resize_image(image_data)
    image_input = np.expand_dims(resized_image, axis=0)

    return image_input