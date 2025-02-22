## Author: Izzy Valdivia 
## Date: 2/21/2025
## Script to download and preprocess images for use in the CNN
import os

# Grab one image and save it into the "Data" folder
### Create one directory using the landmark name
### Get image URL from landmarks_cleaned.csv
### Capture image from wikimedia


def create_directory(landmark_name): 
    """Create new directory using landmark_name, if one exists
    
    Return: nothing
    """
    directory_path = "../data/Images/" + landmark_name
    if os.path.isdir(landmark_name):
        print(f"The directory '{directory_path}' exists.")
    else:
        print("missing")
        return "Missing Directory"



if __name__ == '__main__':
    create_directory("Test")
