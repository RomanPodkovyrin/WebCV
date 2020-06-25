from selenium import webdriver
import unittest
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        # Ben is an employer of Google, he want to look at roman's cv
        self.browser = webdriver.Firefox()

    def tearDown(self):
        # Bob likes Roman's cv, so he is going to hire him
        self.browser.quit()

    def test_can_see_and_read_blog(self):
        # He goes to the homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention web cv
        self.assertIn('WebCV', self.browser.title)

        # In the homepage he can see posts

        # He can see tabs for posts, cv and contact

        ###############Posts##################
        # He can see a post called "Using Django" and a part of the text with the date it was published

        # He clicks it to read more about it

        # There is no way of editing this blog post so he can only read it
    def test_can_open_web_cv(self):
        ###############cv##################
        # Bob then clicks "cv" the website load a new page with roman's CV
        pass
    def test_can_open_contacts(self):
        ###############contact##################
        # Bob then clicks "contact" the website loads a new page with contact information
        pass
        

if __name__ == '__main__':
    unittest.main(warnings='ignore')

# Roman?