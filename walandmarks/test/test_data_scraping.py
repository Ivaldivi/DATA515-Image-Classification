"""
test data_scraping module
"""

# pylint: disable=too-many-public-methods
# Pylint attribute disabled due using many public methods for comprehensive unit testings

import os
import unittest
from unittest import mock

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

from walandmarks.notebooks.data_scraping import (
    get_landmark_data,
    load_landmark_categories,
    load_all_images,
    load_clean_images,
    is_numeric,
    dms_to_dd,
    parse_dms,
    get_soup_data,
    get_landmark_name,
    get_supercategory_from_soup,
    get_location_address_from_soup,
    get_location_coords_from_soup
)

class TestDataScraping(unittest.TestCase):
    """
    This class unit tests the functions from the Data_Scraping module
    """
    def test_load_landmark_categories(self):
        """
        function to test the load_landmarks_category function
        """
        landmark_categories_path = "walandmarks/data/test_categories.csv"

        # create csv
        data = {
            "landmark_id": [0, 1, 2],
            "category": ["link_1", "link_2", "link_3"]
        }
        df = pd.DataFrame(data)
        df.to_csv(landmark_categories_path, index=False)

        landmarks = load_landmark_categories(landmark_categories_path)
        self.assertListEqual([0, 1, 2], landmarks['landmark_id'].to_list())
        self.assertListEqual(["link_1", "link_2", "link_3"], landmarks['category'].to_list())

        if os.path.exists(landmark_categories_path):
            os.remove(landmark_categories_path)

    def test_load_all_images(self):
        """
        function to test the load_all_images function
        """
        landmark_all_images_path = "walandmarks/data/test_all_images.csv"

        # create csv
        data = {
            "id": ["abc1", "def2", "ghi3"],
            "url": ["link_1", "link_2", "link_3"],
            "landmark_id": [0, 1, 2]
        }
        df = pd.DataFrame(data)
        df.to_csv(landmark_all_images_path, index=False)

        landmark_all_images = load_all_images(landmark_all_images_path)
        self.assertListEqual(["abc1", "def2", "ghi3"], landmark_all_images['id'].to_list())
        self.assertListEqual(["link_1", "link_2", "link_3"], landmark_all_images['url'].to_list())
        self.assertListEqual([0, 1, 2], landmark_all_images['landmark_id'].to_list())

        if os.path.exists(landmark_all_images_path):
            os.remove(landmark_all_images_path)

    def test_load_clean_images(self):
        """
        function to test the load_clean_images function
        """
        landmark_clean_images_path = "walandmarks/data/test_clean_images.csv"

        # create csv
        data = {
            "landmark_id": [0, 1, 2],
            "images": ["abc1 def2", "ghi3", "lmn4 opq5 rst6"]
        }
        df = pd.DataFrame(data)
        df.to_csv(landmark_clean_images_path, index=False)

        landmark_clean_images = load_clean_images(landmark_clean_images_path)
        self.assertListEqual([0, 1, 2], landmark_clean_images['landmark_id'].to_list())
        self.assertListEqual(
            ["abc1 def2", "ghi3", "lmn4 opq5 rst6"],
            landmark_clean_images['images'].to_list()
        )

        if os.path.exists(landmark_clean_images_path):
            os.remove(landmark_clean_images_path)

    def test_is_numeric_true(self):
        """
        function to test the is_numeric function if True
        """
        test_input = 123.45
        self.assertTrue(is_numeric(test_input))

    def test_is_numeric_false(self):
        """
        function to test the is_numeric function if True
        """
        test_input = "test"
        self.assertFalse(is_numeric(test_input))

    def test_dms_to_dd_default(self):
        """
        function to test the dms_to_dd function on default inputs
        """
        expected = 0.0
        actual = dms_to_dd()
        self.assertTrue(np.isclose(expected, actual, atol = 1e-08))

    def test_dms_to_dd_normal(self):
        """
        function to test the dms_to_dd function on normal input
        """
        expected = 22.2728
        actual = dms_to_dd(22, 16, 22.08, 'N')
        self.assertTrue(np.isclose(expected, actual, atol = 1e-08))

    def test_dms_to_dd_partial(self):
        """
        function to test the dms_to_dd function on partial input
        """
        expected = -22.0000
        actual = dms_to_dd(degrees=22, direction='W')
        self.assertTrue(np.isclose(expected, actual, atol = 1e-08))

    def test_dms_to_dd_invalid_type(self):
        """
        edge case test for dms_to_dd invalid type input
        """
        with self.assertRaises(TypeError):
            dms_to_dd("test")

    def test_dms_to_dd_invalid_direction(self):
        """
        edge case test for dms_to_dd invalid value for direction
        """
        with self.assertRaises(ValueError):
            dms_to_dd(direction="test")

    def test_parse_dms(self):
        """
        function to test the parse_dms function
        """
        test_input = "114°10′55.2″E"
        expected = 114.1820
        actual = parse_dms(test_input)
        self.assertTrue(np.isclose(expected, actual, atol = 1e-08))

    def test_parse_dms_none(self):
        """
        edge case test for parse_dms function if input is None
        """
        self.assertIsNone(parse_dms(None))

    def test_parse_dms_non_string(self):
        """
        edge case test for parse_dms function if input is not a string
        """
        self.assertIsNone(parse_dms(12345))

    def test_parse_dms_bad_input(self):
        """
        edge case test for parse_dms function if input is a bad string
        """
        self.assertIsNone(parse_dms("test"))

    @mock.patch('requests.get')
    def test_get_soup_data(self, mock_get):
        """
        function to test the get_soup_data function
        """
        mock_response = mock.Mock(status_code=200)
        mock_response.content = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>Category:Happy Valley Racecourse - Wikimedia Commons</title>
            </head>
            <body>
                <div
                    class="mw-body-content"
                    id="mw-content-text"
                >
                    <div
                        class="mw-content-ltr mw-parser-output"
                        dir="ltr"
                        lang="en"
                    >
                        <table class="fileinfotpl-type-information vevent infobox mw-collapsible" dir="ltr" id="wdinfobox"><caption class="fn org" id="wdinfoboxcaption"><b>Happy Valley Racecourse </b></caption><tbody><tr><td class="wdinfo_nomobile" colspan="2" style="text-align:center"><div>Racecourse in Hong Kong</div><div class="switcher-container"><div class="center"><span class="wpImageAnnotatorControl wpImageAnnotatorCaptionOff"><span typeof="mw:File"><a class="mw-file-description" href="/wiki/File:Happy_Valley_Racecourse_1.jpg"><img class="mw-file-element" data-file-height="1536" data-file-width="2048" decoding="async" height="173" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/230px-Happy_Valley_Racecourse_1.jpg" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/345px-Happy_Valley_Racecourse_1.jpg 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/460px-Happy_Valley_Racecourse_1.jpg 2x" width="230"/></a></span></span></div></div></td></tr><tr><td colspan="2" style="text-align:center"><b><a class="external text" href="https://commons.wikimedia.org/w/index.php?title=Special%3AUploadWizard&amp;categories=Happy+Valley+Racecourse">Upload media</a></b></td></tr><tr><td colspan="2" style="text-align:center; font-weight:bold"><div><span typeof="mw:File"><span><img alt="" class="mw-file-element" data-file-height="94" data-file-width="103" decoding="async" height="15" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/16px-Wikipedia-logo-v2.svg.png" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/24px-Wikipedia-logo-v2.svg.png 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/32px-Wikipedia-logo-v2.svg.png 2x" width="16"/></span></span> <a class="extiw" href="https://en.wikipedia.org/wiki/Happy_Valley_Racecourse" title="en:Happy Valley Racecourse">Wikipedia</a></div></td></tr><tr><th class="wikidatainfobox-lcell">Instance of</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Racecourses" title="Category:Racecourses">horse racing venue</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Location</th><td><a href="/wiki/Category:Happy_Valley" title="Category:Happy Valley">Happy Valley</a>, <a href="/wiki/Category:Wan_Chai_District" title="Category:Wan Chai District">Wan Chai District</a>, <a href="/wiki/%E9%A6%99%E6%B8%AF" title="香港">Hong Kong</a>, PRC</td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Operator</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Hong_Kong_Jockey_Club" title="Category:Hong Kong Jockey Club">Hong Kong Jockey Club</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Inception</th><td><div class="plainlist"><ul><li>1846</li></ul></div></td></tr><tr class="wdinfo_nomobile"><td colspan="2" style="text-align:center"><a class="mw-kartographer-map notheme mw-kartographer-container center" data-height="250" data-lang="en" data-mw-kartographer="mapframe" data-overlays='["_66eb5e2878172cb2a4d22abdf02918d64a0c6752"]' data-style="osm-intl" data-width="250" style="width: 250px; height: 250px;"><img alt="Map" decoding="async" height="250" src="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752" srcset="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250@2x.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752 2x" width="250"/></a><small><span class="plainlinksneverexpand"><a class="external text" href="https://geohack.toolforge.org/geohack.php?pagename=Category:Happy_Valley_Racecourse&amp;params=22.2728_N_114.182_E_globe:Earth_&amp;language=en">22° 16′ 22.08″ N, 114° 10′ 55.2″ E</a></span></small></td></tr></tbody></table>
                    </div>
                </div>
            </body>
        </html>
        """
        mock_get.return_value = mock_response

        test_url = "https://commons.wikimedia.org/wiki/Category:Happy_Valley_Racecourse"
        expected_url = test_url
        expected_soup_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>Category:Happy Valley Racecourse - Wikimedia Commons</title>
            </head>
            <body>
                <div
                    class="mw-body-content"
                    id="mw-content-text"
                >
                    <div
                        class="mw-content-ltr mw-parser-output"
                        dir="ltr"
                        lang="en"
                    >
                        <table class="fileinfotpl-type-information vevent infobox mw-collapsible" dir="ltr" id="wdinfobox"><caption class="fn org" id="wdinfoboxcaption"><b>Happy Valley Racecourse </b></caption><tbody><tr><td class="wdinfo_nomobile" colspan="2" style="text-align:center"><div>Racecourse in Hong Kong</div><div class="switcher-container"><div class="center"><span class="wpImageAnnotatorControl wpImageAnnotatorCaptionOff"><span typeof="mw:File"><a class="mw-file-description" href="/wiki/File:Happy_Valley_Racecourse_1.jpg"><img class="mw-file-element" data-file-height="1536" data-file-width="2048" decoding="async" height="173" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/230px-Happy_Valley_Racecourse_1.jpg" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/345px-Happy_Valley_Racecourse_1.jpg 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/460px-Happy_Valley_Racecourse_1.jpg 2x" width="230"/></a></span></span></div></div></td></tr><tr><td colspan="2" style="text-align:center"><b><a class="external text" href="https://commons.wikimedia.org/w/index.php?title=Special%3AUploadWizard&amp;categories=Happy+Valley+Racecourse">Upload media</a></b></td></tr><tr><td colspan="2" style="text-align:center; font-weight:bold"><div><span typeof="mw:File"><span><img alt="" class="mw-file-element" data-file-height="94" data-file-width="103" decoding="async" height="15" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/16px-Wikipedia-logo-v2.svg.png" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/24px-Wikipedia-logo-v2.svg.png 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/32px-Wikipedia-logo-v2.svg.png 2x" width="16"/></span></span> <a class="extiw" href="https://en.wikipedia.org/wiki/Happy_Valley_Racecourse" title="en:Happy Valley Racecourse">Wikipedia</a></div></td></tr><tr><th class="wikidatainfobox-lcell">Instance of</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Racecourses" title="Category:Racecourses">horse racing venue</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Location</th><td><a href="/wiki/Category:Happy_Valley" title="Category:Happy Valley">Happy Valley</a>, <a href="/wiki/Category:Wan_Chai_District" title="Category:Wan Chai District">Wan Chai District</a>, <a href="/wiki/%E9%A6%99%E6%B8%AF" title="香港">Hong Kong</a>, PRC</td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Operator</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Hong_Kong_Jockey_Club" title="Category:Hong Kong Jockey Club">Hong Kong Jockey Club</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Inception</th><td><div class="plainlist"><ul><li>1846</li></ul></div></td></tr><tr class="wdinfo_nomobile"><td colspan="2" style="text-align:center"><a class="mw-kartographer-map notheme mw-kartographer-container center" data-height="250" data-lang="en" data-mw-kartographer="mapframe" data-overlays='["_66eb5e2878172cb2a4d22abdf02918d64a0c6752"]' data-style="osm-intl" data-width="250" style="width: 250px; height: 250px;"><img alt="Map" decoding="async" height="250" src="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752" srcset="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250@2x.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752 2x" width="250"/></a><small><span class="plainlinksneverexpand"><a class="external text" href="https://geohack.toolforge.org/geohack.php?pagename=Category:Happy_Valley_Racecourse&amp;params=22.2728_N_114.182_E_globe:Earth_&amp;language=en">22° 16′ 22.08″ N, 114° 10′ 55.2″ E</a></span></small></td></tr></tbody></table>
                    </div>
                </div>
            </body>
        </html>
        """
        expected_soup = BeautifulSoup(expected_soup_content, "html.parser")

        actual_url, actual_soup = get_soup_data(test_url)
        self.assertEqual(expected_url, actual_url)
        self.assertEqual(expected_soup, actual_soup)

    @mock.patch('requests.get')
    def test_get_soup_data_timeout(self, mock_get):
        """
        edge case test for get_soup_data function to catch timeout exception
        """
        mock_get.side_effect = requests.exceptions.Timeout

        test_url = "https://commons.wikimedia.org/wiki/Category:Happy_Valley_Racecourse"
        expected_url = test_url

        actual_url, actual_soup = get_soup_data(test_url)
        self.assertEqual(expected_url, actual_url)
        self.assertIsNone(actual_soup)

    @mock.patch('requests.get')
    def test_get_soup_data_requests_exception(self, mock_get):
        """
        edge case test for get_soup_data function to catch request exception
        """
        mock_get.side_effect = requests.exceptions.RequestException

        test_url = "https://commons.wikimedia.org/wiki/Category:Happy_Valley_Racecourse"
        expected_url = test_url

        actual_url, actual_soup = get_soup_data(test_url)
        self.assertEqual(expected_url, actual_url)
        self.assertIsNone(actual_soup)

    @mock.patch('requests.get')
    def test_get_landmark_data(self, mock_get):
        """
        function to test that get_landmark_data function correctly parses a link
        """
        mock_response = mock.Mock(status_code=200)
        mock_response.content = """
           <!DOCTYPE html>
           <html>
               <head>
                   <meta charset="utf-8"/>
                   <title>Category:Happy Valley Racecourse - Wikimedia Commons</title>
               </head>
               <body>
                   <div
                       class="mw-body-content"
                       id="mw-content-text"
                   >
                       <div
                           class="mw-content-ltr mw-parser-output"
                           dir="ltr"
                           lang="en"
                       >
                           <table class="fileinfotpl-type-information vevent infobox mw-collapsible" dir="ltr" id="wdinfobox"><caption class="fn org" id="wdinfoboxcaption"><b>Happy Valley Racecourse </b></caption><tbody><tr><td class="wdinfo_nomobile" colspan="2" style="text-align:center"><div>Racecourse in Hong Kong</div><div class="switcher-container"><div class="center"><span class="wpImageAnnotatorControl wpImageAnnotatorCaptionOff"><span typeof="mw:File"><a class="mw-file-description" href="/wiki/File:Happy_Valley_Racecourse_1.jpg"><img class="mw-file-element" data-file-height="1536" data-file-width="2048" decoding="async" height="173" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/230px-Happy_Valley_Racecourse_1.jpg" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/345px-Happy_Valley_Racecourse_1.jpg 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/460px-Happy_Valley_Racecourse_1.jpg 2x" width="230"/></a></span></span></div></div></td></tr><tr><td colspan="2" style="text-align:center"><b><a class="external text" href="https://commons.wikimedia.org/w/index.php?title=Special%3AUploadWizard&amp;categories=Happy+Valley+Racecourse">Upload media</a></b></td></tr><tr><td colspan="2" style="text-align:center; font-weight:bold"><div><span typeof="mw:File"><span><img alt="" class="mw-file-element" data-file-height="94" data-file-width="103" decoding="async" height="15" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/16px-Wikipedia-logo-v2.svg.png" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/24px-Wikipedia-logo-v2.svg.png 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/32px-Wikipedia-logo-v2.svg.png 2x" width="16"/></span></span> <a class="extiw" href="https://en.wikipedia.org/wiki/Happy_Valley_Racecourse" title="en:Happy Valley Racecourse">Wikipedia</a></div></td></tr><tr><th class="wikidatainfobox-lcell">Instance of</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Racecourses" title="Category:Racecourses">horse racing venue</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Location</th><td><a href="/wiki/Category:Happy_Valley" title="Category:Happy Valley">Happy Valley</a>, <a href="/wiki/Category:Wan_Chai_District" title="Category:Wan Chai District">Wan Chai District</a>, <a href="/wiki/%E9%A6%99%E6%B8%AF" title="香港">Hong Kong</a>, PRC</td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Operator</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Hong_Kong_Jockey_Club" title="Category:Hong Kong Jockey Club">Hong Kong Jockey Club</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Inception</th><td><div class="plainlist"><ul><li>1846</li></ul></div></td></tr><tr class="wdinfo_nomobile"><td colspan="2" style="text-align:center"><a class="mw-kartographer-map notheme mw-kartographer-container center" data-height="250" data-lang="en" data-mw-kartographer="mapframe" data-overlays='["_66eb5e2878172cb2a4d22abdf02918d64a0c6752"]' data-style="osm-intl" data-width="250" style="width: 250px; height: 250px;"><img alt="Map" decoding="async" height="250" src="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752" srcset="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250@2x.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752 2x" width="250"/></a><small><span class="plainlinksneverexpand"><a class="external text" href="https://geohack.toolforge.org/geohack.php?pagename=Category:Happy_Valley_Racecourse&amp;params=22.2728_N_114.182_E_globe:Earth_&amp;language=en">22° 16′ 22.08″ N, 114° 10′ 55.2″ E</a></span></small></td></tr></tbody></table>
                       </div>
                   </div>
               </body>
           </html>
        """
        mock_get.return_value = mock_response

        test_url = "https://commons.wikimedia.org/wiki/Category:Happy_Valley_Racecourse"
        expected_title = "Happy Valley Racecourse"
        expected_supercategory = "horse racing venue"
        expected_location = "Happy Valley, Wan Chai District, Hong Kong, PRC"
        expected_latitude = "22° 16′ 22.08″ N"
        expected_longitude = "114° 10′ 55.2″ E"

        actual_title, actual_supercategory, actual_location, actual_latitude, actual_longitude = (
            get_landmark_data(test_url)
        )

        self.assertEqual(expected_title, actual_title)
        self.assertEqual(expected_supercategory, actual_supercategory)
        self.assertEqual(expected_location, actual_location)
        self.assertEqual(expected_latitude, actual_latitude)
        self.assertEqual(expected_longitude, actual_longitude)

    def test_get_landmark_name(self):
        """
        function to test the get_landmark_name function
        """
        test_url = "https://commons.wikimedia.org/wiki/Category:Happy_Valley_Racecourse"
        expected_title = "Happy Valley Racecourse"

        actual_title = get_landmark_name(test_url)
        self.assertEqual(expected_title, actual_title)

    def test_get_landmark_name_invalid_type(self):
        """
        function to test the get_landmark_name function if landmark_url isn't string
        """
        with self.assertRaises(TypeError):
            get_landmark_name(123)

    def test_get_landmark_name_bad_string(self):
        """
        function to test the get_landmark_name function if landmark_url is bad string
        """
        self.assertIsNone(get_landmark_name("test"))

    def test_get_supercategory_from_soup(self):
        """
        function to test the get_supercategory_from_soup function
        """
        test_soup_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>Category:Happy Valley Racecourse - Wikimedia Commons</title>
            </head>
            <body>
                <div
                    class="mw-body-content"
                    id="mw-content-text"
                >
                    <div
                        class="mw-content-ltr mw-parser-output"
                        dir="ltr"
                        lang="en"
                    >
                        <table class="fileinfotpl-type-information vevent infobox mw-collapsible" dir="ltr" id="wdinfobox"><caption class="fn org" id="wdinfoboxcaption"><b>Happy Valley Racecourse </b></caption><tbody><tr><td class="wdinfo_nomobile" colspan="2" style="text-align:center"><div>Racecourse in Hong Kong</div><div class="switcher-container"><div class="center"><span class="wpImageAnnotatorControl wpImageAnnotatorCaptionOff"><span typeof="mw:File"><a class="mw-file-description" href="/wiki/File:Happy_Valley_Racecourse_1.jpg"><img class="mw-file-element" data-file-height="1536" data-file-width="2048" decoding="async" height="173" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/230px-Happy_Valley_Racecourse_1.jpg" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/345px-Happy_Valley_Racecourse_1.jpg 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/460px-Happy_Valley_Racecourse_1.jpg 2x" width="230"/></a></span></span></div></div></td></tr><tr><td colspan="2" style="text-align:center"><b><a class="external text" href="https://commons.wikimedia.org/w/index.php?title=Special%3AUploadWizard&amp;categories=Happy+Valley+Racecourse">Upload media</a></b></td></tr><tr><td colspan="2" style="text-align:center; font-weight:bold"><div><span typeof="mw:File"><span><img alt="" class="mw-file-element" data-file-height="94" data-file-width="103" decoding="async" height="15" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/16px-Wikipedia-logo-v2.svg.png" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/24px-Wikipedia-logo-v2.svg.png 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/32px-Wikipedia-logo-v2.svg.png 2x" width="16"/></span></span> <a class="extiw" href="https://en.wikipedia.org/wiki/Happy_Valley_Racecourse" title="en:Happy Valley Racecourse">Wikipedia</a></div></td></tr><tr><th class="wikidatainfobox-lcell">Instance of</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Racecourses" title="Category:Racecourses">horse racing venue</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Location</th><td><a href="/wiki/Category:Happy_Valley" title="Category:Happy Valley">Happy Valley</a>, <a href="/wiki/Category:Wan_Chai_District" title="Category:Wan Chai District">Wan Chai District</a>, <a href="/wiki/%E9%A6%99%E6%B8%AF" title="香港">Hong Kong</a>, PRC</td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Operator</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Hong_Kong_Jockey_Club" title="Category:Hong Kong Jockey Club">Hong Kong Jockey Club</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Inception</th><td><div class="plainlist"><ul><li>1846</li></ul></div></td></tr><tr class="wdinfo_nomobile"><td colspan="2" style="text-align:center"><a class="mw-kartographer-map notheme mw-kartographer-container center" data-height="250" data-lang="en" data-mw-kartographer="mapframe" data-overlays='["_66eb5e2878172cb2a4d22abdf02918d64a0c6752"]' data-style="osm-intl" data-width="250" style="width: 250px; height: 250px;"><img alt="Map" decoding="async" height="250" src="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752" srcset="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250@2x.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752 2x" width="250"/></a><small><span class="plainlinksneverexpand"><a class="external text" href="https://geohack.toolforge.org/geohack.php?pagename=Category:Happy_Valley_Racecourse&amp;params=22.2728_N_114.182_E_globe:Earth_&amp;language=en">22° 16′ 22.08″ N, 114° 10′ 55.2″ E</a></span></small></td></tr></tbody></table>
                    </div>
                </div>
            </body>
        </html>
        """
        test_soup = BeautifulSoup(test_soup_content, "html.parser")
        expected_supercategory = "horse racing venue"

        actual_supercategory = get_supercategory_from_soup(test_soup)

        self.assertEqual(expected_supercategory, actual_supercategory)

    def test_get_supercategory_from_soup_invalid_type(self):
        """
        function to test the get_supercategory_from_soup function if invalid type
        """
        with self.assertRaises(TypeError):
            get_supercategory_from_soup("test")

    def test_get_supercategory_from_soup_bad_soup(self):
        """
        function to test the get_supercategory_from_soup function if bad soup
        """
        test_soup_content = "test"
        test_soup = BeautifulSoup(test_soup_content, "html.parser")

        self.assertIsNone(get_supercategory_from_soup(test_soup))

    def test_get_location_address_from_soup(self):
        """
        function to test the get_location_address_from_soup function
        """
        test_soup_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>Category:Happy Valley Racecourse - Wikimedia Commons</title>
            </head>
            <body>
                <div
                    class="mw-body-content"
                    id="mw-content-text"
                >
                    <div
                        class="mw-content-ltr mw-parser-output"
                        dir="ltr"
                        lang="en"
                    >
                        <table class="fileinfotpl-type-information vevent infobox mw-collapsible" dir="ltr" id="wdinfobox"><caption class="fn org" id="wdinfoboxcaption"><b>Happy Valley Racecourse </b></caption><tbody><tr><td class="wdinfo_nomobile" colspan="2" style="text-align:center"><div>Racecourse in Hong Kong</div><div class="switcher-container"><div class="center"><span class="wpImageAnnotatorControl wpImageAnnotatorCaptionOff"><span typeof="mw:File"><a class="mw-file-description" href="/wiki/File:Happy_Valley_Racecourse_1.jpg"><img class="mw-file-element" data-file-height="1536" data-file-width="2048" decoding="async" height="173" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/230px-Happy_Valley_Racecourse_1.jpg" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/345px-Happy_Valley_Racecourse_1.jpg 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/460px-Happy_Valley_Racecourse_1.jpg 2x" width="230"/></a></span></span></div></div></td></tr><tr><td colspan="2" style="text-align:center"><b><a class="external text" href="https://commons.wikimedia.org/w/index.php?title=Special%3AUploadWizard&amp;categories=Happy+Valley+Racecourse">Upload media</a></b></td></tr><tr><td colspan="2" style="text-align:center; font-weight:bold"><div><span typeof="mw:File"><span><img alt="" class="mw-file-element" data-file-height="94" data-file-width="103" decoding="async" height="15" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/16px-Wikipedia-logo-v2.svg.png" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/24px-Wikipedia-logo-v2.svg.png 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/32px-Wikipedia-logo-v2.svg.png 2x" width="16"/></span></span> <a class="extiw" href="https://en.wikipedia.org/wiki/Happy_Valley_Racecourse" title="en:Happy Valley Racecourse">Wikipedia</a></div></td></tr><tr><th class="wikidatainfobox-lcell">Instance of</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Racecourses" title="Category:Racecourses">horse racing venue</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Location</th><td><a href="/wiki/Category:Happy_Valley" title="Category:Happy Valley">Happy Valley</a>, <a href="/wiki/Category:Wan_Chai_District" title="Category:Wan Chai District">Wan Chai District</a>, <a href="/wiki/%E9%A6%99%E6%B8%AF" title="香港">Hong Kong</a>, PRC</td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Operator</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Hong_Kong_Jockey_Club" title="Category:Hong Kong Jockey Club">Hong Kong Jockey Club</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Inception</th><td><div class="plainlist"><ul><li>1846</li></ul></div></td></tr><tr class="wdinfo_nomobile"><td colspan="2" style="text-align:center"><a class="mw-kartographer-map notheme mw-kartographer-container center" data-height="250" data-lang="en" data-mw-kartographer="mapframe" data-overlays='["_66eb5e2878172cb2a4d22abdf02918d64a0c6752"]' data-style="osm-intl" data-width="250" style="width: 250px; height: 250px;"><img alt="Map" decoding="async" height="250" src="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752" srcset="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250@2x.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752 2x" width="250"/></a><small><span class="plainlinksneverexpand"><a class="external text" href="https://geohack.toolforge.org/geohack.php?pagename=Category:Happy_Valley_Racecourse&amp;params=22.2728_N_114.182_E_globe:Earth_&amp;language=en">22° 16′ 22.08″ N, 114° 10′ 55.2″ E</a></span></small></td></tr></tbody></table>
                    </div>
                </div>
            </body>
        </html>
        """
        test_soup = BeautifulSoup(test_soup_content, "html.parser")
        expected_location = "Happy Valley, Wan Chai District, Hong Kong, PRC"

        actual_location = get_location_address_from_soup(test_soup)

        self.assertEqual(expected_location, actual_location)

    def test_get_location_address_from_soup_invalid_type(self):
        """
        function to test the get_location_address_from_soup function if invalid type
        """
        with self.assertRaises(TypeError):
            get_location_address_from_soup("test")

    def test_get_location_address_from_soup_bad_soup(self):
        """
        function to test the get_location_address_from_soup function if bad soup
        """
        test_soup_content = "test"
        test_soup = BeautifulSoup(test_soup_content, "html.parser")

        self.assertIsNone(get_location_address_from_soup(test_soup))

    def test_get_location_coords_from_soup(self):
        """
        function to test the get_location_coords_from_soup function
        """
        test_soup_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8"/>
                <title>Category:Happy Valley Racecourse - Wikimedia Commons</title>
            </head>
            <body>
                <div
                    class="mw-body-content"
                    id="mw-content-text"
                >
                    <div
                        class="mw-content-ltr mw-parser-output"
                        dir="ltr"
                        lang="en"
                    >
                        <table class="fileinfotpl-type-information vevent infobox mw-collapsible" dir="ltr" id="wdinfobox"><caption class="fn org" id="wdinfoboxcaption"><b>Happy Valley Racecourse </b></caption><tbody><tr><td class="wdinfo_nomobile" colspan="2" style="text-align:center"><div>Racecourse in Hong Kong</div><div class="switcher-container"><div class="center"><span class="wpImageAnnotatorControl wpImageAnnotatorCaptionOff"><span typeof="mw:File"><a class="mw-file-description" href="/wiki/File:Happy_Valley_Racecourse_1.jpg"><img class="mw-file-element" data-file-height="1536" data-file-width="2048" decoding="async" height="173" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/230px-Happy_Valley_Racecourse_1.jpg" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/345px-Happy_Valley_Racecourse_1.jpg 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Happy_Valley_Racecourse_1.jpg/460px-Happy_Valley_Racecourse_1.jpg 2x" width="230"/></a></span></span></div></div></td></tr><tr><td colspan="2" style="text-align:center"><b><a class="external text" href="https://commons.wikimedia.org/w/index.php?title=Special%3AUploadWizard&amp;categories=Happy+Valley+Racecourse">Upload media</a></b></td></tr><tr><td colspan="2" style="text-align:center; font-weight:bold"><div><span typeof="mw:File"><span><img alt="" class="mw-file-element" data-file-height="94" data-file-width="103" decoding="async" height="15" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/16px-Wikipedia-logo-v2.svg.png" srcset="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/24px-Wikipedia-logo-v2.svg.png 1.5x, https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/32px-Wikipedia-logo-v2.svg.png 2x" width="16"/></span></span> <a class="extiw" href="https://en.wikipedia.org/wiki/Happy_Valley_Racecourse" title="en:Happy Valley Racecourse">Wikipedia</a></div></td></tr><tr><th class="wikidatainfobox-lcell">Instance of</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Racecourses" title="Category:Racecourses">horse racing venue</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Location</th><td><a href="/wiki/Category:Happy_Valley" title="Category:Happy Valley">Happy Valley</a>, <a href="/wiki/Category:Wan_Chai_District" title="Category:Wan Chai District">Wan Chai District</a>, <a href="/wiki/%E9%A6%99%E6%B8%AF" title="香港">Hong Kong</a>, PRC</td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Operator</th><td><div class="plainlist"><ul><li><a href="/wiki/Category:Hong_Kong_Jockey_Club" title="Category:Hong Kong Jockey Club">Hong Kong Jockey Club</a></li></ul></div></td></tr><tr class="wdinfo_nomobile"><th class="wikidatainfobox-lcell">Inception</th><td><div class="plainlist"><ul><li>1846</li></ul></div></td></tr><tr class="wdinfo_nomobile"><td colspan="2" style="text-align:center"><a class="mw-kartographer-map notheme mw-kartographer-container center" data-height="250" data-lang="en" data-mw-kartographer="mapframe" data-overlays='["_66eb5e2878172cb2a4d22abdf02918d64a0c6752"]' data-style="osm-intl" data-width="250" style="width: 250px; height: 250px;"><img alt="Map" decoding="async" height="250" src="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752" srcset="https://maps.wikimedia.org/img/osm-intl,a,a,a,250x250@2x.png?lang=en&amp;domain=commons.wikimedia.org&amp;title=Category%3AHappy_Valley_Racecourse&amp;revid=510586893&amp;groups=_66eb5e2878172cb2a4d22abdf02918d64a0c6752 2x" width="250"/></a><small><span class="plainlinksneverexpand"><a class="external text" href="https://geohack.toolforge.org/geohack.php?pagename=Category:Happy_Valley_Racecourse&amp;params=22.2728_N_114.182_E_globe:Earth_&amp;language=en">22° 16′ 22.08″ N, 114° 10′ 55.2″ E</a></span></small></td></tr></tbody></table>
                    </div>
                </div>
            </body>
        </html>
        """
        test_soup = BeautifulSoup(test_soup_content, "html.parser")
        expected_latitude = "22° 16′ 22.08″ N"
        expected_longitude = "114° 10′ 55.2″ E"

        actual_latitude, actual_longitude = get_location_coords_from_soup(test_soup)

        self.assertEqual(expected_latitude, actual_latitude)
        self.assertEqual(expected_longitude, actual_longitude)

    def test_get_location_coords_from_soup_invalid_type(self):
        """
        function to test the get_location_coords_from_soup function if invalid type
        """
        with self.assertRaises(TypeError):
            get_location_address_from_soup("test")

    def test_get_location_coords_from_soup_bad_soup(self):
        """
        function to test the get_location_coords_from_soup function if bad soup
        """
        test_soup_content = "test"
        test_soup = BeautifulSoup(test_soup_content, "html.parser")

        actual_latitude, actual_longitude = get_location_coords_from_soup(test_soup)

        self.assertIsNone(actual_latitude)
        self.assertIsNone(actual_longitude)
