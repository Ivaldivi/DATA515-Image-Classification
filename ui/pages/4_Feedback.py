"""
This file contains the code for the Feedback page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import requests

import streamlit as st


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
EMAIL_API_URL = "https://api.emailjs.com/api/v1.0/email/send"

def send_email(name, email, user_feedback):
    """
    Send an email to the joint inbox with the user's feedback.
    """
    payload = {
        "service_id": "walandmark_feedback",
        "template_id": "template_3f5hfpd",
        "user_id": "5caFDMvUBAm_o4TIH",
        "template_params": {
            "name": name,
            "email": email,
            "message": user_feedback
        }
    }

    response = requests.post(EMAIL_API_URL, json=payload)
    print("Testing the print statment...")
    print(response.status_code)
    if response.status_code == 200:
        st.success("Feedback sent successfully!")
    else:
        st.error("Failed to send feedback. Please try again later.")


with st.form(key='general_feedback_form', clear_on_submit=True):
    name = st.text_input('Name (optional):')
    email = st.text_input('Email (optional):')
    user_feedback = st.text_area('Please share your feedback:')

    image = st.file_uploader(label='Upload relevant files (optional):',
                         accept_multiple_files=True,
                         help='''If there is an image that is relevant to
                         your feedback, please provide it here. You may also
                         upload a .docx or pdf file with your feedback.''')
    submitted = st.form_submit_button('Submit')

if submitted:
    st.success('Success. Thank you for your feedback!')
    # send email to joint inbox: 
    send_email(name, email, user_feedback)

