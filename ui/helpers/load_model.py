import streamlit as st
import tensorflow as tf

MODEL_PATH = "./model/224x224 image classification EfficientNetB0.keras"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)