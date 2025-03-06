"""
This module contains helper functions for handling user feedback form
submissions.
"""

import requests
import streamlit as st

def upload_image_to_imgur(image):
    """
    Function that will host an image on imgur and return the url 
    associated with the image.
    
    Parameters: image (UploadedFile object): The image file to be 
                uploaded to imgur.
    Returns: str: The url of the hosted image.
    """

    client_id = "24ea6736831793f"
    headers = {"Authorization": f"Client-ID {client_id}"}

    # Read the image content from Streamlit file uploader
    img_data = image.read()

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

def verify_form_inputs(name, email, user_feedback):
    """
    Function that checks that the user has entered valid form inputs: 
        including name, email, and feedback.

    Parameters: 
        name (str): The name input from user form.
        email (str): The email input from user form.
        user_feedback (str): The user feedback input from user form. 
            Must be at least 10 characters.
    Returns: bool: True if all fields are filled 
        out correctly, False otherwise.  
    """

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
    
    Parameters:
        name (str): The name input from user form.
        email (str): The email input from user form.
        user_feedback (str): The user feedback input from user form.
        image (UploadedFile object): The image file uploaded by the user.
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
