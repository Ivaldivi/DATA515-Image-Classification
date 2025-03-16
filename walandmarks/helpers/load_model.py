"""
for loading tensorflow model
"""

import keras
import streamlit as st

@st.cache_resource
def load_model(model_path):
    """
    load tensorflow model given the path
    """
    return keras.models.load_model(model_path)
