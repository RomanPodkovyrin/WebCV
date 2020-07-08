from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from datetime import datetime

class NewBlogVisitorTest(unittest.TestCase):

    def setUp(self):
        # Ben is an employer of Google, he want to look at roman's cv
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # Bob likes Roman's cv, so he is going to hire him
        self.browser.quit()

    def test_can_see_and_read_blog(self):
        # He goes to the homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention web cv
        self.assertIn('WebCV', self.browser.title)
        
        headers = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(
            any('Blog' in header.text for header in headers),
            "Did't find Blog in header"
        )

    def test_cannot_add_new_post_with_button(self):

        self.browser.get("http://localhost:8000/")
        # test that user cannot click on the button to add
        try:
            add_post = self.browser.find_element_by_id("add_new_post")
            add_post.click()
            self.fail("Visitor is not ment to be able to add a new post")
        except:
            pass

    
    def test_cannot_add_new_post_with_url(self):
        self.browser.get("http://localhost:8000/post/new/")
        self.assertEqual(self.browser.current_url,"http://localhost:8000/")

    def test_cannot_edit_post_with_button(self):

        self.browser.get("http://localhost:8000/post/1/")
        # test that user cannot click on the button to edit
        try:
            edit_post = self.browser.find_element_by_id("id_edit_post_button")
            edit_post.click()
            self.fail("Visitor is not supposed to be able to edit a post")
        except:
            pass


    def test_cannot_edit_post_with_url(self):
        self.browser.get("http://localhost:8000/post/new/")
        self.assertEqual(self.browser.current_url,"http://localhost:8000/")




class AdminBlogControlTest(unittest.TestCase):

    def setUp(self):
        # Beth is the administrator of the site
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

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
            any('Admin test title ' + current_date_and_time in row.text and 'Admin test text for a post ' + current_date_and_time in row.text for row in rows),
            "New Post did not appear in the blog"
        )

########## CV ##########

class NewCVVisitorTest(unittest.TestCase):

    # James is an employer, who want's too look at roman's cv
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
    
    def test_can_see_and_read_cv(self):
        # James loads the website
        self.browser.get('http://localhost:8000/')

        # James clicks the "CV" in the menu option
        cv_button = self.browser.find_element_by_id('id_cv_link_button')
        cv_button.click()

        # james is redirected to a cv webpage
        self.assertEqual(self.browser.current_url, 'http://localhost:8000/cv/', "wasn't redirected to a cv url")
        self.assertIn('WebCV', self.browser.title)
        headers = self.browser.find_elements_by_tag_name('h1')
        self.assertTrue(
            any('CV' in header.text for header in headers),
            "Did't find CV in header"
        )


        # James can see the correct cv items
        page_source = self.browser.page_source
        for item in ['id_name','id_personal_statement','id_education','id_work_experience','id_skills', 'id_phone', 'id_email']:
            self.assertIn(item, page_source)

        
    def test_visitor_cannot_edit_cv_with_button(self):

        # James tries to edit the cv
        self.browser.get('http://localhost:8000/cv')
        

        # he looks for the button
        try:
            edit_cv = self.browser.find_element_by_id("id_edit_cv_button")
        except:
            edit_cv = None

        # But there is no button 
        self.assertIsNone(edit_cv)
        
        # So he cannot click the booton 
        try:
            edit_cv.click()
            self.fail("normal user was not supposed to click edit button")
        except:
            pass

        # Therefore he stays on the root page
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/")

        

    def test_visitor_cannot_edit_cv_with_url(self):

        # James tries to go to the url directly to edit cv
        self.browser.get('http://localhost:8000/cv/edit')

        # But that does not work
        self.assertEqual(self.browser.current_url,"http://localhost:8000/cv/")


class AdminCVTests(unittest.TestCase):
    # Roman is the administrator

    def setUp(self):
        # He logins as an administrator
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        # He go to the website
        self.browser.get('http://localhost:8000/admin')

        # Enters his credentials
        username = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys('roman')
        password.send_keys('1234')

        
        password.send_keys(Keys.ENTER)
        time.sleep(1)

    def tearDown(self):
        self.browser.quit()

    def test_can_edit_cv(self):

        # Roman goes to cv url
        self.browser.get('http://localhost:8000/cv/')

        # He clicks edit button
        edit_cv = self.browser.find_element_by_id("id_edit_cv_button")
        edit_cv.click()
        time.sleep(1)
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/edit/")

        current_date_and_time = str(datetime.now())
        
        # Adds his name
        name = self.browser.find_element_by_id('id_name')
        nametext = 'Roman ' + current_date_and_time
        name.clear()
        name.send_keys(nametext)

        # adds his personal statement
        personal_statement = self.browser.find_element_by_id('id_personal_statement')
        personal_statement_text = 'Roman ' + current_date_and_time
        personal_statement.clear()
        personal_statement.send_keys(personal_statement_text)

        # adds skills
        skills = self.browser.find_element_by_id('id_skills')
        skills_text = 'Java, Python ' + current_date_and_time
        skills.clear()
        skills.send_keys(skills_text)

        # add phone
        phone = self.browser.find_element_by_id('id_phone')
        phone_text = '0000000 ' + current_date_and_time
        phone.clear()
        phone.send_keys(phone_text)

        # add email
        email = self.browser.find_element_by_id('id_email')
        email_text = 'example@email.com '+ current_date_and_time
        email.clear()
        email.send_keys(email_text)

        # Saved his edits
        save_button = self.browser.find_element_by_id("id_save_button")
        save_button.click()

        time.sleep(3)
        # gets redirected
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/")

        # checks

        # name
        self.assertEqual(self.browser.find_element_by_id("id_name").text,nametext)
        # personal statement
        self.assertEqual(self.browser.find_element_by_id("id_personal_statement").text,personal_statement_text)
        # skills
        self.assertEqual(self.browser.find_element_by_id("id_skills").text,skills_text)
        # phone
        self.assertEqual(self.browser.find_element_by_id("id_phone").text,phone_text)
        # email
        self.assertEqual(self.browser.find_element_by_id("id_email").text,email_text)

        



if __name__ == '__main__':
    unittest.main(warnings='ignore')
