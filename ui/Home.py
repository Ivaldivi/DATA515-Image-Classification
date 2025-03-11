"""
This file contains the code for the Home page of the Streamlit app.
"""
# pylint: disable=invalid-name
# Pylint attribute disabled due to Streamlit multi-page naming conventions

import streamlit as st

st.set_page_config(
    page_title="Home - WA Landmark Classifier",
    page_icon="🔎",
)

st.title("Washington State Landmark Classifier")

st.image("images/seattle-skyline.jpg")

st.markdown(
    """
    ## About
    Welcome to the Washington State Landmark Classifier! Perfect for 
    Washington state enthusiasts, we provide a tool for 
    determining what that cool building is. Just take a picture and upload to
    our tool! See the Classifier page for more information.

    Our code is open source! Our repository is 
    [here](https://github.com/Ivaldivi/DATA515-Image-Classification).

    ## Bios
    This page was made by four students of the Master"s of Data Science
    program at the University of Washington.
    """
)

st.image("images/sarah-innis.jpg", width=150)

st.markdown(
    """
    Sarah Innis (she/her) is a current UW MSDS student and a very smart 
    person! She took organic chemistry in undergrad!!! She
    did the prereqs to go to med school!!! She works at a startup as the 
    resident data genius!!!
    """
)

st.image("images/anthony-nguyen.jpg", width=150)

st.markdown(
    """
    Anthony Nguyen (he/him) is a smarty smarty smarty. He tuned like 4 models 
    over the weekend and is very motivated. He is also 
    a great teammember and a nice friend. In his free time, you can catch him 
    having a Celsius and getting work done.
    """
)

st.image("images/annie-staker.jpg", width=150)

st.markdown(
    """
    Annie Staker (she/they) is a current UW MSDS student and a graduate
    research assistant in the University of Washington Dept. 
    of Genome Sciences. Before coming to UW she worked for three years
    as a mathematician/data scientist in the biotech industry. 
    Besides data science, Annie enjoys hiking, watching women's sports,
    and exploring Seattle with their friends.
    """
)

st.image("images/izzy-valdivia.jpg", width=150)

st.markdown(
    """
    Izzy Valdivia (she/they) is a highly motivated learner. Besides being
    an MSDS student, she does research at Fred Hutch Cancer 
    Center. In their free time, they fly to Minnesota to taste food.
    She also has an adorable dog.
    """
)
