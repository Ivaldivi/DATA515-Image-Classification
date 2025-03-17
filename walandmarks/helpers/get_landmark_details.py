"""
Given landmark index get landmark details
"""

import streamlit as st

from walandmarks.helpers.get_data_from_csv import get_data_from_csv

def get_landmark_details(landmark_id):
    """
    Given landmark index get landmark location and category

    Parameters:
        landmark_id (int): landmark index
    Returns:
        landmark_details (dict): landmark location and category
    """
    landmarks_df = get_data_from_csv('walandmarks/data/landmarks_washington_full.csv')
    landmarks_df_select = landmarks_df[landmarks_df['landmark_id'] == landmark_id]
    landmark_details = {"location": landmarks_df_select['location'].values[0],
                        "category": landmarks_df_select['supercategory'].values[0]}

    return landmark_details