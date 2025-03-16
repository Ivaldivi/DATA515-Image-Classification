"""
Test the Homepage module.
"""
import unittest

from streamlit.testing.v1 import AppTest

class TestHome(unittest.TestCase):
    """
    This class contains the unit tests for the Home page 
    of the Streamlit app. These tests use Streamlit's 
    AppTest class to simulate the Streamlit app.
    """

    def setUp(self):
        self.at = AppTest.from_file("walandmarks/ui/Home.py").run()
        return super().setUp()

    def test_display_title(self):
        """
        function to test the title of the home page
        """
        self.assertEqual(self.at.title[0].value, "Washington State Landmark Classifier")

    def test_markdown_about_section(self):
        """
        function to test that the markdown elements of the about section are 
        as expected, plus or minus whitespace.
        """

        expected_about = """
        ## About
        Welcome to the Washington State Landmark Classifier! Perfect for 
        Washington state enthusiasts, we provide a tool for 
        determining what that cool building is. Just take a picture and 
        upload to
        our tool! See the Classifier page for more information.

        Our code is open source! Our repository is 
        [here](https://github.com/Ivaldivi/DATA515-Image-Classification).

        ## Bios
        This page was made by four students of the Master's of Data Science
        program at the University of Washington.
        """

        expected_about = "".join(expected_about.split()) # remove whitespace\
        markdown_elt_num = 0
        actual_about = str(self.at.markdown[markdown_elt_num].body).strip()
        actual_about = "".join(actual_about.split()) # remove whitespace
        self.assertEqual(expected_about, actual_about)

    def test_markdown_sarah_bio(self):
        """
        function to test that the markdown elements of Sarah's bio are as 
        expected, plus or minus whitespace.
        """
        expected_bio = """
        Sarah Innis (she/her) is a current UW MSDS student and a very smart 
        person! She took organic chemistry in undergrad!!! She
        did the prereqs to go to med school!!! She works at a startup as the 
        resident data genius!!!
        """
        expected_bio = "".join(expected_bio.split()) # remove whitespace
        markdown_elt_num = 1
        actual_bio = str(self.at.markdown[markdown_elt_num].body).strip()
        actual_bio = "".join(actual_bio.split()) # remove whitespace
        self.assertEqual(expected_bio, actual_bio)

    def test_markdown_anthony_bio(self):
        """
        function to test that the markdown elements of Anthony's bio are as 
        expected, plus or minus whitespace.
        """
        expected_bio = """
        Anthony Nguyen (he/him) is a smarty smarty smarty. He tuned like 4 models 
        over the weekend and is very motivated. He is also 
        a great teammember and a nice friend. In his free time, you can catch him 
        having a Celsius and getting work done.
        """
        expected_bio = "".join(expected_bio.split()) # remove whitespace
        markdown_elt_num = 2
        actual_bio = str(self.at.markdown[markdown_elt_num].body).strip()
        actual_bio = "".join(actual_bio.split()) # remove whitespace
        self.assertEqual(expected_bio, actual_bio)

    def test_markdown_annie_bio(self):
        """
        function to test that the markdown elements of Annie's bio are as 
        expected, plus or minus whitespace.
        """
        expected_bio = """
        Annie Staker (she/they) is a current UW MSDS student and a graduate
        research assistant in the University of Washington Dept. 
        of Genome Sciences. Before coming to UW she worked for three years
        as a mathematician/data scientist in the biotech industry. 
        Besides data science, Annie enjoys hiking, watching women's sports,
        and exploring Seattle with their friends.
        """
        expected_bio = "".join(expected_bio.split()) # remove whitespace
        markdown_elt_num = 3
        actual_bio = str(self.at.markdown[markdown_elt_num].body).strip()
        actual_bio = "".join(actual_bio.split()) # remove whitespace
        self.assertEqual(expected_bio, actual_bio)

    def test_markdown_izzy_bio(self):
        """
        function to test that the markdown elements of Izzy's bio are as 
        expected, plus or minus whitespace.
        """
        expected_bio = """
        Izzy Valdivia (she/they) is a highly motivated learner. Besides being
        an MSDS student, she does research at Fred Hutch Cancer 
        Center. In their free time, they fly to Minnesota to taste food.
        She also has an adorable dog.
        """
        expected_bio = "".join(expected_bio.split()) # remove whitespace
        markdown_elt_num = 4
        actual_bio = str(self.at.markdown[markdown_elt_num].body).strip()
        actual_bio = "".join(actual_bio.split()) # remove whitespace
        self.assertEqual(expected_bio, actual_bio)


if __name__ == '__main__':
    unittest.main()
