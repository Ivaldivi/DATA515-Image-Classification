import streamlit as st
import tensorflow as tf
import os

@st.cache_resource
def load_model(model_path):
    return tf.keras.models.load_model(model_path)