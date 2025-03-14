"""
for loading tensorflow model
"""

import streamlit as st
import keras

@st.cache_resource
def load_model(model_path):
    """
    load tensorflow model given the path
    """
    return keras.models.load_model(model_path)
