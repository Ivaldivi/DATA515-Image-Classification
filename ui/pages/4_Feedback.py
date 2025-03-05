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

    if not img_data:
        st.error("No image data found.")
        return None

    url = 'https://api.imgur.com/3/upload'
    file= {'image': img_data}

    response = requests.post(url, headers=headers, files=file)

    if response.status_code == 200:
        # If successful, return the image link
        data = response.json()
        return data['data']['link']
    else:
        # Print out the full response for debugging
        st.error(f"Error uploading image to Imgur: {response.status_code}")
        st.error(f"Response: {response.text}")  # Print the full response body for more insight
        return None


EMAIL_API_URL = "https://api.emailjs.com/api/v1.0/email/send"

def send_email(name, email, user_feedback, image):
    """
    Send an email to the joint inbox with the user's feedback.
    """
    if image is not None:
        image_url = upload_image_to_imgur(image)
        print(image_url)
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

    response = requests.post(EMAIL_API_URL, json=payload, timeout=100)
    print("Testing the print statment...")
    print(response.status_code)
    if name is None:
        st.error("Please enter your name.")
    elif user_feedback is None:
        st.error("Please enter feedback.")
    elif email is None:
        st.error("Please enter your email.")
    elif response.status_code == 200:
        st.success("Feedback sent successfully!")
    else:
        st.error("Failed to send feedback. Please try again later.")

with st.form(key='general_feedback_form', clear_on_submit=True):
    form_name = st.text_input('Name:')
    form_email = st.text_input('Email (optional):')
    form_user_feedback = st.text_area('Please share your feedback:')

    form_image = st.file_uploader(label='Upload relevant files (optional):',
                         accept_multiple_files=False,
                         type=["jpg", "png", "jpeg", "pdf", "docx"],
                         help='''If there is an image that is relevant to
                         your feedback, please provide it here. You may also
                         upload a .docx or pdf file with your feedback.''')
    submitted = st.form_submit_button('Submit')

if submitted:
    st.success('Success. Thank you for your feedback!')
    # send email to joint inbox:
    send_email(form_name, form_name, form_user_feedback, form_image)
