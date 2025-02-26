import streamlit as st

st.set_page_config(
    page_title="Feedback - WA Landmark Classifier",
    page_icon="🔎",
)

st.title('Feedback')

st.markdown(
    '''
    ### What landmarks are we missing? Did we misclassify your landmark? Let us know!
    Please fill out the form below to let us know what we can do to improve. If you have an image of a misclassified or missing 
    landmark, please include it in the form.
    '''
)

with st.form(key='feedback_form', clear_on_submit=True):
    user_feedback = st.text_area('Please share your feedback:')
    image = st.file_uploader(label='Upload relevant files (optional):',
                         accept_multiple_files=True,
                         help='''If there is an image that is relevant to your feedback, please provide it here. You may also
                         upload other types of files.''')
    submitted = st.form_submit_button('Submit')

if submitted:
    st.success('Success. Thank you for your feedback!')
    # Send an email with user feedback