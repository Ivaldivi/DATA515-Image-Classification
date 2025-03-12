"""
for loading tensorflow model
"""
# pylint: disable=no-member
# Pylint attribute disabled because incorrect. It stated:
# "E1101:Module 'tensorflow' has no 'keras' member", but tensorflow does
# have a keras member. Code has been tested and works as expected.

import streamlit as st
import tensorflow as tf

@st.cache_resource
def load_model(model_path):
    """
    load tensorflow model given the path
    """
    return tf.keras.models.load_model(model_path)
