"""
This file contains the code for the Feedback page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

from time import sleep

import streamlit as st

from walandmarks.helpers.form_handler import verify_form_inputs, send_email

st.set_page_config(
    page_title="Feedback - WA Landmark Classifier",
    page_icon="🔎",
)

st.title('Feedback')

st.markdown(
    "### What landmarks are we missing? Did we misclassify your landmark? "
    "Let us know! Please fill out the form below to let us know what we can "
    "do to improve. If you have an image of a misclassified or missing "
    "landmark, please include it in the form.",
    unsafe_allow_html = True
)

with st.form(key='general_feedback_form', clear_on_submit=True):
    form_name = st.text_input('Name:')
    form_email = st.text_input('Email:')
    form_user_feedback = st.text_area('Please share your feedback:')

    form_image = st.file_uploader(label='Upload relevant files (optional):',
                         accept_multiple_files=False,
                         type=["jpg", "png", "jpeg"],
                         help='''If there is an image that is relevant to
                         your feedback, please provide it here.''')

    submitted = st.form_submit_button('Submit')

if submitted:
    # Check that name, email, and user feedback fields are not empty
    if verify_form_inputs(form_name, form_email, form_user_feedback):
        with st.spinner(text = 'Extracting information…'):
            sleep(3)
            # On submission with proper inputs, try to send email with
            # form information to joint inbox:
            send_email(form_name, form_email, form_user_feedback, form_image)
