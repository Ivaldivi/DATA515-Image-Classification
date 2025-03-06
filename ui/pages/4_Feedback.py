"""
This file contains the code for the Feedback page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

from time import sleep

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

def upload_image_to_imgur(image):
    """
    Function that will host an image on imgur and return the url 
    associated with the image.
    
    Parameters: image (UploadedFile object): The image file to be 
                uploaded to imgur.
    """

    client_id = "24ea6736831793f"
    headers = {"Authorization": f"Client-ID {client_id}"}

    # Read the image content from Streamlit file uploader
    img_data = image.read()

    # TODO: add error handling when no image data is found. Value error? #pylint: disable=fixme
    if not img_data:
        st.error("No image data found.")
        return None

    url = 'https://api.imgur.com/3/upload'
    file= {'image': img_data}

    response = requests.post(url, headers=headers, files=file, timeout=100)
    if response.status_code == 200:
        data = response.json()
        return data['data']['link']
    return None

# Initialize session state variables if they don't exist
if "name" not in st.session_state:
    st.session_state.name = ""
if "email" not in st.session_state:
    st.session_state.email = ""
if "user_feedback" not in st.session_state:
    st.session_state.user_feedback = ""

def verify_form_inputs(name, email, user_feedback):
    """Function that checks that the user has entered a name, email, and feedback."""

    if len(name)<1:
        st.error('Please enter name.')
    elif len(email)<1:
        st.error("Please enter email.")
    elif len(user_feedback)<10:
        if len(user_feedback)<1:
            st.error("Please enter feedback.")
        else:
            st.error("Feedback must be at least 10 characters.")
    else:
        return True
    return False

EMAIL_API_URL = "https://api.emailjs.com/api/v1.0/email/send"

def send_email(name, email, user_feedback, image):
    """
    Send an email to the joint inbox with the user's feedback.
    """
    if image is not None:
        image_url = upload_image_to_imgur(image)
        payload = {
            "service_id": "walandmark_feedback",
            "template_id": "template_3f5hfpd",
            "user_id": "5caFDMvUBAm_o4TIH",
            "template_params": {
                "name": name,
                "email": email,
                "message": user_feedback,
                "image": image_url
            }
        }
    else:
        payload = {
            "service_id": "walandmark_feedback",
            "template_id": "template_6h3tppj",
            "user_id": "5caFDMvUBAm_o4TIH",
            "template_params": {
                "name": name,
                "email": email,
                "message": user_feedback
            }
        }

    response = requests.post(EMAIL_API_URL, json=payload, timeout=100)

    if len(name)<1:
        st.error("Please enter your name.")
    elif len(email)<1:
        st.error("Please enter your email.")
    elif len(user_feedback)<10:
        if len(user_feedback)<1:
            st.error("Please enter feedback.")
        else:
            st.error("Feedback must be at least 10 characters.")
    elif response.status_code == 200:
        st.success("Feedback successfully sent. Thank you!")
    else:
        st.error("Failed to send feedback. Please try again later.")

with st.form(key='general_feedback_form', clear_on_submit=True):
    form_name = st.text_input('Name:')
    form_email = st.text_input('Email:')
    form_user_feedback = st.text_area('Please share your feedback:')

    form_image = st.file_uploader(label='Upload relevant files (optional):',
                         accept_multiple_files=False,
                         type=["jpg", "png", "jpeg"],
                         help='''If there is an image that is relevant to
                         your feedback, please provide it here. You may also
                         upload a .docx or pdf file with your feedback.''')

    submitted = st.form_submit_button('Submit')

if submitted:
    # Check that name, email, and user feedback fields are not empty
    if verify_form_inputs(form_name, form_email, form_user_feedback):
        with st.spinner(text = 'Extracting information…'):
            sleep(3)
            # On submission with proper inputs, try to send email with
            # form information to joint inbox:
            send_email(form_name, form_email, form_user_feedback, form_image)
