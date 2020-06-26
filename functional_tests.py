from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from datetime import datetime
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
        
        header = self.browser.find_element_by_tag_name('h1')
        self.assertIn('WebCV', header.text)

        # In the homepage he can see posts

        # He can see tabs for posts, cv and contact

        ###############Posts##################
        # He can see a post called "Using Django" and a part of the text with the date it was published

        # He clicks it to read more about it

        # There is no way of editing this blog post so he can only read it
        self.fail('Finish blog test')

    def test_cannot_add_new_post(self):
        self.fail('Finish visitor add new post test')

    def test_cannot_edit_post(self):
        self.fail('Finish visitor edit post test')

    def test_can_open_web_cv(self):
        ###############cv##################
        # Bob then clicks "cv" the website load a new page with roman's CV
        self.fail('Finish CV test')

    def test_can_open_contacts(self):
        ###############contact##################
        # Bob then clicks "contact" the website loads a new page with contact information
        self.fail('Finish contacts test')


class AdminControlTest(unittest.TestCase):

    def setUp(self):
        # Beth is the administrator of the site
        self.browser = webdriver.Firefox()

        # She go to the website
        self.browser.get('http://localhost:8000/admin')

        # logs into the site by using admin credentials
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys('roman')
        password.send_keys('1234')

        # She then hits enter to login
        password.send_keys(Keys.ENTER)
        time.sleep(1)

    def tearDown(self):
        # Beth is done with the account, therefore she logs off
        self.browser.get('http://localhost:8000/admin/logout/')
        # and quits the browser
        self.browser.quit()
    
    def test_admin_add_new_post(self):
        # Beth goes to posts
        self.browser.get('http://localhost:8000/')

        # She clicks on the add new post sign
        add_new_post = self.browser.find_element_by_id('add_new_post')
        self.assertNotEqual(None,add_new_post)
        add_new_post.click()

        current_date_and_time = str(datetime.now())
        
        # Beth adds title
        title = self.browser.find_element_by_id('id_title')
        title.send_keys('Admin test title ' + current_date_and_time)

        # Beth adds contents
        contents = self.browser.find_element_by_id('id_text')
        contents.send_keys('Admin test text for a post ' + current_date_and_time)

        # Beth submits new posts
        save = self.browser.find_element_by_id('id_save_button')
        save.click()

        # Beth checks that the post has been added to the website
        self.browser.get('http://localhost:8000/')
        table = self.browser.find_element_by_id('id_post_list_table')
        rows = table.find_elements_by_class_name('post')
        self.assertTrue(
            any('Admin test title ' + current_date_and_time in row.text and 'Admin test text for a post ' + current_date_and_time in row.text for row in rows)
        )


    
    def test_admin_add_new_post_retain(self):
        self.fail('Finish new post retain test')



if __name__ == '__main__':
    unittest.main(warnings='ignore')
