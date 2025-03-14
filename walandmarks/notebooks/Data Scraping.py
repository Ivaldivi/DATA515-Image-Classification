from bs4 import BeautifulSoup
import numpy as np
from pandarallel import pandarallel
import pandas as pd
import re
import requests

from walandmarks.ui.helpers.get_data_from_csv import get_data_from_csv

def load_landmark_categories(landmark_categories_path):
    landmark_data = get_data_from_csv(landmark_categories_path)

    return landmark_data

def load_all_images(landmark_images_path):
    landmark_images = get_data_from_csv(landmark_images_path)

    return landmark_images

def load_clean_images(landmark_clean_images_path):
    landmark_cleaned_images = get_data_from_csv(landmark_clean_images_path)

    return landmark_cleaned_images

def is_numeric(value):
    """Checks if a given value is numeric (integer or float)"""
    return isinstance(value, (int, float))

def dms_to_dd(degrees=0, minutes=0, seconds=0, direction='N'):
    if not (is_numeric(degrees) and is_numeric(minutes) and is_numeric(seconds)):
        raise TypeError("degrees, minutes, and seconds must be numeric")

    if direction.upper() not in ('N', 'S', 'W', 'E'):
        raise ValueError("direction must be N, S, W, or E")

    dd = float(degrees) + float(minutes) / 60 + float(seconds) / (60 * 60)
    if direction.upper() in ('W', 'S'):
        dd *= -1

    return dd

def parse_dms(dms):
    if dms is None or not isinstance(dms, str):
        return None

    pattern = r"""([+-]?\d{1,3})[°\s]*([\d]{1,2})?[′'´\s]*([\d]{1,2}(?:\.\d+)?)?[″"\s]*([NSEWnsew]?)"""

    match = re.match(pattern, dms.strip())
    if not match:
        return None

    degrees, minutes, seconds, direction = match.groups()

    degrees = float(degrees) if degrees else 0
    minutes = float(minutes) if minutes else 0
    seconds = float(seconds) if seconds else 0

    coords_dd = dms_to_dd(degrees, minutes, seconds, direction)

    return coords_dd

def get_soup_data(landmark_url):
    if not isinstance(landmark_url, str):
        raise TypeError("landmark_url must be a string")

    try:
        html_text = requests.get(landmark_url)
        soup = BeautifulSoup(html_text.content, "html.parser")

        url_if_redirected = soup.find("div", class_="category-redirect-header")

        if url_if_redirected:
            redirected_url_extension = url_if_redirected.find("a")['href']
            base_url = landmark_url.split("/w")[0]
            landmark_url = base_url + redirected_url_extension

            html_text = requests.get(landmark_url)
            soup = BeautifulSoup(html_text.content, "html.parser")

        return (landmark_url, soup)
    except Exception as e:
        return (landmark_url, None)


def get_landmark_name(landmark_url):
    title = None
    try:
        title = landmark_url.split("Category:")[1].replace("_", " ")
    except Exception as e:
        pass

    return title

def get_supercategory_from_soup(soup):
    if not isinstance(soup, BeautifulSoup):
        raise TypeError("soup must be type BeautifulSoup")

    supercategory = None
    supercategory_location = soup.find(string="Instance of")

    if supercategory_location:
        supercategory_tag = supercategory_location.next_element
        supercategory = [supercategory for supercategory in supercategory_tag.stripped_strings][0]

    return supercategory


def get_location_address_from_soup(soup):
    if not isinstance(soup, BeautifulSoup):
        raise TypeError("soup must be type BeautifulSoup")

    location_address = None
    location = soup.find(string="Location")

    if location:
        location_text = location.next_element
        location_address = [
            location.replace(",", "").strip()
            for location
            in location_text.stripped_strings
            if location.replace(",", "").strip()
        ]

        SEPARATOR = ", "
        location_address = SEPARATOR.join(location_address)

    return location_address


def get_location_coords_from_soup(soup):
    if not isinstance(soup, BeautifulSoup):
        raise TypeError("soup must be type BeautifulSoup")

    latitude, longitude = None, None
    coords = [location for location in soup.find_all("a", class_="external text") if "geohack.tool" in location["href"]]
    coords = [coords for coords in coords if coords.text.find(",") != -1]

    if len(coords) != 0:
        coords_expanded = coords[0].text.replace("\xa0", "").split(",")

        try:
            latitude = coords_expanded[0].strip()
            longitude = coords_expanded[1].strip()
        except:
            pass

    return (latitude, longitude)

def get_landmark_data(landmark_url):
    if not isinstance(landmark_url, str):
        raise TypeError("landmark_url must be a string")

    url, soup = get_soup_data(landmark_url)

    title = get_landmark_name(url)
    supercategory = get_supercategory_from_soup(soup)
    location_address = get_location_address_from_soup(soup)
    latitude, longitude = get_location_coords_from_soup(soup)

    return (title, supercategory, location_address, latitude, longitude)

def scrape_landmark_data(LANDMARK_CATEGORIES_PATH):
    if not isinstance(LANDMARK_CATEGORIES_PATH, str):
        raise TypeError("LANDMARK_CATEGORIES_PATH must be a string")

    landmark_data = load_landmark_categories(LANDMARK_CATEGORIES_PATH)

    pandarallel.initialize()
    landmark_data[['name', 'supercategory', 'location', 'latitude', 'longitude']] = (
        landmark_data.parallel_apply(lambda row: get_landmark_data(row['category']), axis='columns', result_type='expand'))

    landmark_data['latitude'] = landmark_data['latitude'].map(parse_dms)
    landmark_data['longitude'] = landmark_data['longitude'].map(parse_dms)

    landmark_full_info = landmark_data.loc[landmark_data['location'].notna()]

    return landmark_full_info

def filter_washington_location(landmarks_data):
    if not isinstance(landmarks_data, pd.DataFrame):
        raise TypeError("landmarks_data must be a pandas DataFrame")

    if 'location' not in landmarks_data.columns:
        raise ValueError("landmarks_data must have column 'location'")

    landmark_washington = landmarks_data.loc[
        (landmarks_data['location'].str.contains('washington', case = False)) &
        (~landmarks_data['location'].str.contains('washington d.c.', case = False)) &
        (~landmarks_data['location'].str.contains('washington county', case = False))
    ]

    return landmark_washington

def filter_washington_coordinates(landmarks_data):
    if not isinstance(landmarks_data, pd.DataFrame):
        raise TypeError("landmarks_data must be a pandas DataFrame")

    if ['location', 'latitude', 'longitude'] not in landmarks_data.columns:
        raise ValueError("landmarks_data must have columns 'location', 'latitude', and 'longitude'")

    # 1 degree wiggle room
    # accounts for landmarks that go through the border of Washington state
    VARIANCE_CONSTANT = 1.0

    wa_lat1 = parse_dms("45°33′ N") - VARIANCE_CONSTANT
    wa_lat2 = parse_dms("49° N") + VARIANCE_CONSTANT

    wa_long1 = parse_dms("124°46′ W") - VARIANCE_CONSTANT
    wa_long2 = parse_dms("116°55′ W") + VARIANCE_CONSTANT

    # sometimes, a few places in Washington State don't have coordinates on wikimedia
    # the first clause is a "just in cause" one
    landmark_washington = landmarks_data.loc[
        (landmarks_data['location'].str.contains('Washington, Pacific Northwest', case = False)) |
        (
            (landmarks_data['latitude'].between(wa_lat1, wa_lat2)) &
            (landmarks_data['longitude'].between(wa_long1, wa_long2))
        )
    ]

    landmark_washington = landmark_washington[
        [
            'landmark_id', 'name', 'supercategory', 'location',
            'latitude', 'longitude', 'category'
        ]
    ]

    return landmark_washington

def get_washington_full_data(landmarks_data):
    if not isinstance(landmarks_data, pd.DataFrame):
        raise TypeError("landmarks_data must be a pandas DataFrame")

    landmark_washington = filter_washington_location(landmarks_data)
    landmark_washington = filter_washington_coordinates(landmark_washington)

    return landmark_washington

def save_washington_full_data(landmark_washington, file_location):
    if not isinstance(landmark_washington, pd.DataFrame):
        raise TypeError("landmark_washington must be a pandas DataFrame")
    if not isinstance(file_location, str):
        raise TypeError("file_location must be a string")

    landmark_washington.to_csv(file_location, index = False, encoding='utf-8-sig')

def get_washington_clean_images(
        landmark_washington, landmark_images_path, landmark_clean_images_path
    ):

    if not isinstance(landmark_washington, pd.DataFrame):
        raise TypeError("landmark_washington must be a pandas DataFrame")
    if not (isinstance(landmark_images_path, str) and isinstance(landmark_clean_images_path, str)):
        raise TypeError("landmark_images_path and landmark_clean_images_path must be strings")

    landmark_images = load_all_images(landmark_images_path)
    landmark_cleaned_images = load_clean_images(landmark_clean_images_path)

    landmark_washington_ids = landmark_washington['landmark_id'].unique()

    landmark_cleaned_images['images'] = landmark_cleaned_images['images'].str.split(" ")
    landmark_cleaned_images = landmark_cleaned_images.explode('images').reset_index(drop=True)
    landmark_washington_images = landmark_images.loc[
        landmark_images['landmark_id'].isin(landmark_washington_ids)
    ]

    landmark_washington_cleaned_images = landmark_washington_images.loc[
        landmark_washington_images['id'].isin(landmark_cleaned_images['images'])
    ]

    landmark_washington_cleaned_images = landmark_washington_cleaned_images.sort_values('landmark_id')
    landmark_washington_cleaned_images = landmark_washington_cleaned_images.reset_index(drop=True)
    landmark_washington_cleaned_images = landmark_washington_cleaned_images.rename(columns = {
        'id': 'image_id'
    })

    landmark_washington_cleaned_images = landmark_washington_cleaned_images[['landmark_id', 'image_id', 'url']]

    return landmark_washington_cleaned_images

def save_washington_cleaned_images_data(landmark_washington_cleaned_images, file_location):
    if not isinstance(landmark_washington_cleaned_images, pd.DataFrame):
        raise TypeError("landmark_washington must be a pandas DataFrame")
    if not isinstance(file_location, str):
        raise TypeError("file_location must be a string")

    landmark_washington_cleaned_images.to_csv(file_location, index = False, encoding='utf-8-sig')

def main():
    LANDMARK_CATEGORIES_PATH = "../data/Google Landmarks Dataset/train_label_to_category.csv"
    LANDMARK_IMAGES_PATH = "../data/Google Landmarks Dataset/train.csv"
    LANDMARK_CLEAN_IMAGES_PATH = "../data/Google Landmarks Dataset/train_clean.csv"

    landmark_data = scrape_landmark_data(LANDMARK_CATEGORIES_PATH)
    landmark_washington = get_washington_full_data(landmark_data)

    save_washington_full_data(
        landmark_washington,
        "../data/landmarks_washington_full.csv"
    )

    landmark_washington_cleaned_images = get_washington_clean_images(
        landmark_washington, LANDMARK_IMAGES_PATH, LANDMARK_CLEAN_IMAGES_PATH
    )

    save_washington_cleaned_images_data(
        landmark_washington_cleaned_images,
        "../data/landmarks_washington_clean_images.csv"
    )

if __name__ == "__main__":
    main()