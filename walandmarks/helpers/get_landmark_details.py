"""
Given landmark name get landmark details
"""

from walandmarks.helpers.get_data_from_csv import get_data_from_csv

def get_landmark_details(landmark_name):
    """
    Given landmark name get landmark location and category

    Parameters:
        landmark_name (str): landmark name
    Returns:
        landmark_details (dict): landmark location and category
    """
    landmarks_df = get_data_from_csv('walandmarks/data/landmarks_washington_full.csv')
    landmarks_df_select = landmarks_df[landmarks_df['name'] == landmark_name]

    try:
        if landmarks_df_select.empty:
            raise ValueError(f"Landmark name: {landmark_name} is not in the dataset")
        landmark_details = {"location": landmarks_df_select['location'].values[0],
                            "category": landmarks_df_select['supercategory'].values[0]}
        return landmark_details
    except ValueError as e:
        print(f"Error: {e}")
        return None
