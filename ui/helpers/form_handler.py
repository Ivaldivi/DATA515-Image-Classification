"""
This module contains helper functions for handling user feedback form
submissions.
"""

import requests
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

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

    if not isinstance(image, UploadedFile):
        raise TypeError("Image must be a Streamlit UploadedFile object.")
    # Read the image content from Streamlit file uploader
    img_data = image.read()

    if not img_data:
        st.error("One of your images is empty.")

    url = 'https://api.imgur.com/3/upload'
    file= {'image': img_data}

    response = requests.post(url, headers=headers, files=file, timeout=100)
    print(url)
    print(response)
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
    if not isinstance(name, str) or not isinstance(email, str):
        raise TypeError("Name and email must be strings.")

    if not isinstance(user_feedback, str):
        raise TypeError("Form feedback must be a string.")

    if len(name)<1 and len(email)<1 and len(user_feedback)<1:
        raise ValueError("Feedback form inputs cannot be empty.")

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

def convert_urls_to_html(urls):
    """
    Function that converts a list of image urls to a string of HTML
    image tags.
    
    Parameters:
        urls (list): A list of image urls.
    Returns:
        str: A string consisting of the image html elements.
    """
    if not isinstance(urls, list):
        raise TypeError("Input must be a list of image urls.")
    if len(urls) == 0:
        raise ValueError("List of image urls cannot be empty.")

    images_in_html_tags = ""
    for url in urls:
        images_in_html_tags += f'<img src="{url}" width="300"><br>'
    return images_in_html_tags


EMAIL_API_URL = "https://api.emailjs.com/api/v1.0/email/send"

def send_email(name, email, user_feedback, images):
    """
    Send an email to the joint inbox with the user's feedback.
    
    Parameters:
        name (str): The name input from user form.
        email (str): The email input from user form.
        user_feedback (str): The user feedback input from user form.
        image (UploadedFile object): The image file uploaded by the user.
    """

    if images is not None:
        list_of_urls = []
        for image in images:
            image_url = upload_image_to_imgur(image)
            list_of_urls.append(image_url)
        images_in_html_tags = convert_urls_to_html(list_of_urls)
        payload = {
            "service_id": "walandmark_feedback",
            "template_id": "template_3f5hfpd",
            "user_id": "5caFDMvUBAm_o4TIH",
            "template_params": {
                "name": name,
                "email": email,
                "message": user_feedback,
                "image": images_in_html_tags
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

    if response.status_code == 200:
        st.success("Feedback successfully sent. Thank you!")
    else:
        st.error("Failed to send feedback. Please try again later.")
