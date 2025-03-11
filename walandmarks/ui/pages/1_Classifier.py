"""
This file contains the code for the Classifier page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import time

import streamlit as st

from helpers.load_landmarks import load_landmarks
from helpers.load_model import load_model
from helpers.process_image_input import process_image_input
from helpers.make_prediction import make_prediction

st.set_page_config(
    page_title="Classifier - WA Landmark Classifier",
    page_icon="🔎",
)

model = load_model()
landmarks = load_landmarks()

st.title('Classifier')

st.markdown(
    '''
    Welcome to the Washington State Landmark Classifier. To classify
    your image, upload it using the button below. We will give 
    you the top five most likely places your image depicts.
    '''
)

image = st.file_uploader(label=
                         'Upload your image here. Must be a .png or '+ 
                         '.jpg file that is 200MB or less.',
                         type=['png', 'jpg', 'jpeg'],
                         accept_multiple_files=False,
                         help='Image must be a .png, .jpg, or .jpeg file that is 200MB or less.')

if image is not None:
    message = st.success('Image successfully uploaded. Processing your image...')
    time.sleep(3)
    message.empty()
    time.sleep(1)
    message = st.success("Successfully processed your image.")
    st.image('walandmarks/images/space-needle.jpg', width=200)
    st.markdown(
        '''
        ### Results
        Our prediction:
        '''
    )

    with st.spinner("Predicting..."):
        processed_image = process_image_input(image)
        output = model.predict(processed_image)[0]

        predictions = make_prediction(output, confidence_threshold=0.45)

        for index, prediction in enumerate(predictions):
            landmark_index, confidence = prediction

            st.write(f"{index + 1}: {landmarks[landmark_index]} "
                     f"({confidence * 100:.2f}% confidence)\n"
             )

    st.write('Your image:')
    st.image(image)
