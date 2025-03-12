# DATA515-Landmark-Classification
Team members: Sarah Innis, Anthony Nguyen, Annie Staker, Izzy Valdivia

![Build/Test Workflow](https://github.com/Ivaldivi/Data515-Image-Classification/actions/workflows/build_test.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/Ivaldivi/DATA515-Image-Classification/badge.svg?branch=main)](https://coveralls.io/github/Ivaldivi/DATA515-Image-Classification?branch=main)

## The Project Type:
Web-based tool

## Questions of Interest: 
* How accurately can we classify landmarks?
* Can we distinguish between similar-appearing landmarks (e.g. same area)?
* Can we identify landmarks through different environments and lighting conditions?
* Can we identify landmarks if given a low-quality image input?
* Can we identify landmarks that we have not trained our model upon?
* Can we provide further information about a landmark?

## Goal for project output: 
Create a multiclass image classification tool that can correctly identify landmarks (tentatively within Washington state) if given an image. 

## Data Sources: 
* Images of Landmarks across the world, provided by [Google](https://github.com/cvdfoundation/google-landmark?tab=readme-ov-file)
  * More than 4 million labeled landmark photos
* [Wikimedia](https://www.wikimedia.org/) 
  * (specifically, the Wikimedia link for a given landmark)
  * Determine location information about a landmark
  * Provide additional information about a landmark
* User-taken Photos of Landmarks in Washington
  * Use to validate model & demonstrate model accuracy and precision


## Streamlit
After cloning this repo, run the Streamlit app using this command:
streamlit run walandmarks/ui/Home.py

## How To Use Conda Environment: 
In order to create a conda environment from the current environment.yml file, run the following line:\
conda env create -f environment.yml

To activate the environment run:\
conda activate landmarks_classification_env

## Unit testing:
Our unit tests can be found at walandmarks/test.

To run all unit tests:\
python -m unittest discover

To see code coverage:\
coverage run -m unittest discover