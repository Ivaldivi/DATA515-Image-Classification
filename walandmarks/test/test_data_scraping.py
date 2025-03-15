"""
test data_scraping module
"""

import unittest
from unittest import mock

from walandmarks.notebooks.data_scraping import get_landmark_data

class TestDataScraping(unittest.TestCase):
    """
    This class unit tests the functions from the Data_Scraping module
    """
    @mock.patch('requests.get')
    def test_get_landmark_data(self, mock_get):
        """Validates that get_landmark_data correctly parses a link"""
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
