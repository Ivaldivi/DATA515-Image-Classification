"""
This module is used to fetch data from a CSV file.
"""

import pandas as pd

def get_data_from_csv(file_path):
    """
    Fetches data from a CSV file and returns it as a pandas DataFrame.

    input: file_path (str) - the path to the CSV file
    output: df (pd.DataFrame) - the data in the CSV file as a pandas DataFrame
    edge case: if the file is not found, return None
    """
    try:
        df = pd.read_csv(file_path, sep=',')
        return df
    except FileNotFoundError:
        print(f"Failed to fetch data: {file_path}")
        return None
