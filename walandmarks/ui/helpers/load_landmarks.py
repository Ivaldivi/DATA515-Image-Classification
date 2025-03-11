import streamlit as st

from ui.helpers.get_data_from_csv import get_data_from_csv

LANDMARK_CLASSES_PATH = "./../../data/landmark_classes.csv"

@st.cache_resource
def load_landmarks():
    landmarks_data = get_data_from_csv(LANDMARK_CLASSES_PATH)
    landmarks = landmarks_data['landmark_name']

    return landmarks