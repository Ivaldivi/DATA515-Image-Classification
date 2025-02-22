## Author: Izzy Valdivia 
## Date: 2/21/2025
## Script to download and preprocess images for use in the CNN
import os
import numpy as np
import unittest


# Grab one image and save it into the "Data" folder
### Create one directory using the landmark name
### Get image URL from landmarks_cleaned.csv
### Capture image from wikimedia


def directory_exists(landmark_name): 
    """Create new directory using landmark_name, if one exists
    
    Return: Boolean [True/False]
    """
    directory_path = os.path.abspath(os.path.join("data", "Images", landmark_name))
    if os.path.isdir(directory_path):
        return True
    else:
        print(directory_path)
        return False


def resize_image(): 
    """resize image ndarray 
    Return: ndarray
    """
    
    pass 

def download_image(landmark_name, url, id): 
    """Download image from url 
    
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    
    pass 


if __name__ == '__main__':
    directory_exists("Test")
    unittest.main()
