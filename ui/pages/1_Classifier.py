"""
This file contains the code for the Classifier page of the Streamlit app.
"""
# pylint: disable=invalid-name

import time

import streamlit as st

from ui.helpers.get_model_predictions import predict_from_image, interpret_model_output

st.set_page_config(
    page_title="Classifier - WA Landmark Classifier",
    page_icon="🔎",
)

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
    st.image('images/space-needle.jpg', width=200)
    st.markdown(
        '''
        ### Results
        Our prediction:
        1. The Space Needle (90% confidence)
        2. The Columbia Center (5% confidence)
        3. A really tall tree (3% confidence)
        4. Other (2% confidence)
        '''
    )
    st.write('Your image:')
    st.image(image)

    with st.spinner("Predicting..."):
        output = predict_from_image(image)
        landmark_name, confidence = interpret_model_output(output)

        st.write(f"We predict that this landmark is \"{landmark_name}\" with {confidence * 100:.2f}% confidence!")


