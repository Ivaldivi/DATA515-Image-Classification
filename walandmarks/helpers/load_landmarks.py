import streamlit as st

from walandmarks.helpers.get_data_from_csv import get_data_from_csv

@st.cache_resource
def load_landmarks(landmark_classes_path):
    landmarks_data = get_data_from_csv(landmark_classes_path)
    landmarks = landmarks_data['landmark_name']

    return landmarks