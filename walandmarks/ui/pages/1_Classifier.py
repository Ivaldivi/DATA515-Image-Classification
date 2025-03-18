"""
This file contains the code for the Classifier page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import streamlit as st

from walandmarks.helpers.get_landmark_details import get_landmark_details
from walandmarks.helpers.load_landmarks import load_landmarks
from walandmarks.helpers.load_model import load_model
from walandmarks.helpers.process_image_input import process_image_input
from walandmarks.helpers.make_prediction import make_prediction

st.set_page_config(
    page_title="Classifier - Cascadia Classifier",
    page_icon="🔎",
)

st.title("Cascadia Classifier")

st.markdown(
    """
    Welcome to the Cascadia Classifier. To classify
    your image, upload it using the button below.
    """
)

image = st.file_uploader(label=
                         "Upload your image here. Must be a .png or "+ 
                         ".jpg file that is 200MB or less.",
                         type=["png", "jpg", "jpeg"],
                         accept_multiple_files=False,
                         help="Image must be a .png, .jpg, or .jpeg file that is 200MB or less.")

if image is not None:
    with st.spinner("Predicting..."):
        model_path = "walandmarks/model/final_EfficientNetb0_WA_landmarks_model.keras"
        landmark_classes_path = "walandmarks/data/landmark_classes.csv"
        model = load_model(model_path)
        landmarks = load_landmarks(landmark_classes_path)

        processed_image = process_image_input(image)
        output = model.predict(processed_image)[0]

        predictions = make_prediction(output, confidence_threshold=0.50)

    message = st.success("Successfully processed your image.")
    st.markdown(
        """
        ### Results
        Our prediction:
        """
    )

    for index, prediction in enumerate(predictions):
        landmark_index, confidence = prediction
        landmark_name = landmarks[landmark_index]

        st.markdown(f"<b>{index + 1}. {landmark_name}</b> "
                    f"<b>({confidence * 100:.2f}% confidence)</b>\n", unsafe_allow_html=True
            )
        st.markdown(f"Location: {get_landmark_details(landmark_name)['location'].title()}")
        st.markdown(f"Category: {get_landmark_details(landmark_name)['category'].title()}")

    st.markdown("Your image:")
    st.image(image)
