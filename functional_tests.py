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
        for item in ['id_name','id_personal_statement','id_skills', 'id_phone', 'id_email']:
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

    def test_visitor_cannot_add_work_with_url(self):

        self.browser.get('http://localhost:8000/cv/work/add')
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/", "User was meant to be redirected to the cv page")

    def test_can_see_work_experience(self):

        # James loads the website
        self.browser.get('http://localhost:8000/')

        # James clicks the "CV" in the menu option
        cv_button = self.browser.find_element_by_id('id_cv_link_button')
        cv_button.click()

        # James can see the correct work items
        work_id = self.browser.find_elements_by_id('id_work')
        self.assertGreater(len(work_id), 0, "There are no work posts")
        for work in work_id:
            for item in ['id_company', 'id_job_title', 'id_description', 'id_start','id_finish']:
                work.find_element_by_id(item)

    def test_visitor_cannot_edit_work_with_url(self):
        self.browser.get('http://localhost:8000/cv/work/edit/1')
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/", "User was meant to be redirected to the cv page")

    def test_visitor_cannot_add_education_with_url(self):
        self.browser.get('http://localhost:8000/cv/education/add')
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/", "User was meant to be redirected to the cv page")
    
    def test_can_see_education(self):
        self.fail("Finish")

    def test_visitor_cannont_edit_education_with_url(self):
        self.browser.get('http://localhost:8000/cv/education/edit/1')
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/", "User was meant to be redirected to the cv page")


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

    def test_cv_has_no_new_post_button(self):
        self.browser.get('http://localhost:8000/cv/')

        try:
            newPost = self.browser.find_element_by_id("add_new_post")
            newPost.click()
        except:
            return

        self.fail("There should be no add new post button")

        # time.sleep(2)
        # self.assertEqual(self.browser.current_url,"http://localhost:8000/cv/", "there should be no new post button")

    def test_can_add_work(self):
        self.browser.get("http://localhost:8000/cv/")

        new_work = self.browser.find_element_by_id("add_new_work")
        new_work.click()
        self.assertEqual(self.browser.current_url,"http://localhost:8000/cv/work/add/")

        dateandtime = str(datetime.now())

        company = self.browser.find_element_by_id("id_company")
        company_text = "Google " + dateandtime
        company.send_keys(company_text)

        job = self.browser.find_element_by_id("id_job_title")
        job_text = "CEO " + dateandtime
        job.send_keys(job_text)

        description = self.browser.find_element_by_id("id_description")
        description_text = "Sold users data, just for fun " + dateandtime
        description.send_keys(description_text)

        date_from = self.browser.find_element_by_id("id_start")
        date_from_text ="1. " + dateandtime
        date_from.send_keys(date_from_text)

        date_to = self.browser.find_element_by_id("id_finish")
        date_to_text = "2. " + dateandtime
        date_to.send_keys(date_to_text)

        save = self.browser.find_element_by_id('id_save_button')
        save.click()

        time.sleep(1)
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/")

        work_list_table = self.browser.find_elements_by_class_name("work")
        # works = work_list_table.find_elements_by_id("id_work")
        # for tag in [company_text, job_text, description_text, date_from_text, date_to_text]:
        #     self.assertIn(tag, work_list_table.text)

        for work_item in work_list_table:
            for x in [company_text, job_text, description_text, date_from_text, date_to_text]:
                self.assertIn(x in work_item.text)

    def test_can_edit_work(self):
        self.browser.get("http://localhost:8000/cv/")
        work = self.browser.find_elements_by_id("work_edit_button")
        work[0].click()

        self.assertEqual(self.browser.current_url,"http://localhost:8000/cv/work/edit/1/")

        dateandtime = str(datetime.now())

        company = self.browser.find_element_by_id("id_company")
        company_text = "Google " + dateandtime
        company.clear()
        company.send_keys(company_text)

        job = self.browser.find_element_by_id("id_job_title")
        job_text = "CEO " + dateandtime
        job.clear()
        job.send_keys(job_text)

        description = self.browser.find_element_by_id("id_description")
        description_text = "Sold users data, just for fun " + dateandtime
        description.clear()
        description.send_keys(description_text)

        date_from = self.browser.find_element_by_id("id_start")
        date_from_text ="1. " + dateandtime
        date_from.clear()
        date_from.send_keys(date_from_text)

        date_to = self.browser.find_element_by_id("id_finish")
        date_to_text = "2. " + dateandtime
        date_to.clear()
        date_to.send_keys(date_to_text)

        save = self.browser.find_element_by_id('id_save_button')
        save.click()

        time.sleep(1)
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/")

        work_list_table = self.browser.find_elements_by_class_name("work")
        # works = work_list_table.find_elements_by_id("id_work")
        # for tag in [company_text, job_text, description_text, date_from_text, date_to_text]:
        #     self.assertIn(tag, work_list_table.text)

        self.assertEqual(self.browser.find_element_by_id("id_company").text,company_text)
        self.assertEqual(self.browser.find_element_by_id("id_job_title").text,job_text)
        self.assertEqual(self.browser.find_element_by_id("id_description").text,description_text)
        self.assertEqual(self.browser.find_element_by_id("id_start").text,date_from_text)
        self.assertEqual(self.browser.find_element_by_id("id_finish").text,date_to_text)

        for work_item in work_list_table:
            for x in [company_text, job_text, description_text, date_from_text, date_to_text]:
                self.assertIn(x in work_item.text)

    def test_can_add_education(self):
        self.browser.get("http://localhost:8000/cv/")

        new_education = self.browser.find_element_by_id("add_education")
        new_education.click()
        self.assertEqual(self.browser.current_url,"http://localhost:8000/cv/education/add/")

        dateandtime = str(datetime.now())

        school = self.browser.find_element_by_id("id_school")
        school_text = "Google " + dateandtime
        school.send_keys(school_text)

        grade = self.browser.find_element_by_id("id_grade")
        grade_text = "Sold users data, just for fun " + dateandtime
        grade.send_keys(grade_text)

        date_from = self.browser.find_element_by_id("id_start")
        date_from_text ="1. " + dateandtime
        date_from.send_keys(date_from_text)

        date_to = self.browser.find_element_by_id("id_finish")
        date_to_text = "2. " + dateandtime
        date_to.send_keys(date_to_text)

        save = self.browser.find_element_by_id('id_save_button')
        save.click()

        time.sleep(1)
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/")

        education_list_table = self.browser.find_elements_by_class_name("education")

        for education_item in education_list_table:
            for x in [school_text, grade_text, date_from_text, date_to_text]:
                self.assertIn(x in education_item.text)
    
    def test_can_edit_education(self):
        self.browser.get("http://localhost:8000/cv/")
        work = self.browser.find_elements_by_id("education_edit_button")
        work[0].click()

        self.assertEqual(self.browser.current_url,"http://localhost:8000/cv/education/edit/1/")

        dateandtime = str(datetime.now())

        school = self.browser.find_element_by_id("id_school")
        school_text = "Google " + dateandtime
        school.clear()
        school.send_keys(school_text)

        grade = self.browser.find_element_by_id("id_grade")
        grade_text = "Sold users data, just for fun " + dateandtime
        grade.clear()
        grade.send_keys(grade_text)

        date_from = self.browser.find_element_by_id("id_start")
        date_from_text ="1. " + dateandtime
        date_from.clear()
        date_from.send_keys(date_from_text)

        date_to = self.browser.find_element_by_id("id_finish")
        date_to_text = "2. " + dateandtime
        date_to.clear()
        date_to.send_keys(date_to_text)

        save = self.browser.find_element_by_id('id_save_button')
        save.click()

        time.sleep(1)
        self.assertEqual(self.browser.current_url, "http://localhost:8000/cv/")

        education_list_table = self.browser.find_elements_by_class_name("education")
        # works = work_list_table.find_elements_by_id("id_work")
        # for tag in [company_text, job_text, description_text, date_from_text, date_to_text]:
        #     self.assertIn(tag, work_list_table.text)

        self.assertEqual(self.browser.find_element_by_id("id_school").text,school_text)
        self.assertEqual(self.browser.find_element_by_id("id_grade").text,grade_text)
        self.assertEqual(self.browser.find_element_by_id("id_start").text,date_from_text)
        self.assertEqual(self.browser.find_element_by_id("id_finish").text,date_to_text)

        for education_item in education_list_table:
            for x in [school_text, grade_text, date_from_text, date_to_text]:
                self.assertIn(x in education_item.text)
        self.fail("Finish")




if __name__ == '__main__':
    unittest.main(warnings='ignore')
