from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import time
from datetime import datetime

from blog.views import post_list, cv_page, post_new, cv_edit
from blog.models import Post, CV, Work, Education


#################### Blog ####################

class BlogHomePageTest(TestCase):

    def test_root_url_resolves_to_post_list_view(self):
        found = resolve('/')
        self.assertEqual(found.func, post_list)

    def test_post_list_returns_correct_html_template(self):
        
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_edit_returns_correct_html_template_for_new_post(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)

        response = self.client.get('/post/new/')
        self.assertTemplateUsed(response, 'blog/post_edit.html')
    
    def test_post_list_can_remember_POST_requests(self):

        # self.client.login(username='roman',email='example@gmail.com', password='1234')
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)
        
        # Enter data
        date = str(datetime.now())
        title = 'Unittest title test ' + date 
        text = 'Unittest text test ' + date
        self.assertEqual(Post.objects.count(), 0)
        response1 = self.client.post('/post/new/', data={'title': title, 'text': text})

        # Check is was saved in the db
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(title,post.title)
        self.assertEqual(text,post.text)

        # Check got the right redirect
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/post/1/')

        # Content is displayed
        response2 = self.client.get(response1['location'])
        self.assertIn(title, response2.content.decode())
        self.assertIn(text, response2.content.decode())

        # Content is added to the main page
        response3 = self.client.get('/')
        self.assertIn(title, response3.content.decode())
        self.assertIn(text, response3.content.decode())

class PostModelTest(TestCase):

    def test_saving_and_retrieving_times(self):

        # Create temp user
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')


        self.assertEqual(Post.objects.all().count(), 0)

        # First post
        Post.objects.create(author=me,title='Sample unit test title', text='Test')
        self.assertEqual(Post.objects.all().count(), 1)

        # Second post
        Post.objects.create(author=me,title='Sample unit test title2', text='Test2')
        self.assertEqual(Post.objects.all().count(), 2)

        # Verify first and second post
        saved = Post.objects.all()
        self.assertEqual(saved[0].title, 'Sample unit test title')
        self.assertEqual(saved[0].text, 'Test')

        self.assertEqual(saved[1].title, 'Sample unit test title2')
        self.assertEqual(saved[1].text, 'Test2')

#################### CV ####################

## Test Data
# CV
name = 'Roman Podkovyrin'
personal_statement = "Hello, please hire me"
skills = 'Java, Python, Russian'
phone = "00000000"
email = "email@example.com"


name2 = 'Roman Podkovyrin2'
personal_statement2 = "Hello, please hire me2"
skills2 = 'Java, Python, Russian2'
phone2 = "000000002"
email2 = "email@example.com2"


# Project


def check_cv_data(self,modelObject,data):
        # Checks if model object containt the right information as data
        self.assertEqual(modelObject.name, data["name"])
        self.assertEqual(modelObject.personal_statement, data["personal_statement"])
        self.assertEqual(modelObject.phone, data["phone"])
        self.assertEqual(modelObject.email, data["email"])


class CVHomePageTest(TestCase):

    def test_root_url_resolves_to_cv_page_view(self):

        found = resolve('/cv/')
        self.assertEqual(found.func, cv_page)
    
    def test_cv_page_returns_correct_html_template(self):
        
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response,'blog/cv_page.html')

    def test_cv_edit_returns_correct_html_template(self):
        # Login
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)

        response = self.client.get('/cv/edit/')
        self.assertTemplateUsed(response,'blog/cv_edit.html')

    def test_cv_edit_can_remember_POST_requests(self):

        # Login
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)
        
        # Send data
        self.assertEqual(CV.objects.count(), 0)
        response1 = self.client.post('/cv/edit/', data={'name': name, 'personal_statement': personal_statement,
         "email": email, "phone": phone})

        # data was saved into the database
        self.assertEqual(CV.objects.count(),1)
        savedCV= CV.objects.first()
        check_cv_data(self, savedCV, {'name': name, 'personal_statement': personal_statement, "email": email, "phone": phone})
        
        # redirected to the right page
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/cv/')

        # information added is displayed on the page
        response2 = self.client.get(response1['location'])
        self.assertIn(name, response2.content.decode())
        self.assertIn(personal_statement, response2.content.decode())
        self.assertIn(phone, response2.content.decode())
        self.assertIn(email, response2.content.decode())


class CVModelTest (TestCase):

    def test_saving_and_retrieving_times(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        # Add data to the model
        self.assertEqual(CV.objects.all().count(), 0)
        CV.objects.create(author=me, name=name, personal_statement=personal_statement,phone=phone,email=email)

        # Check data is saved
        self.assertEqual(CV.objects.all().count(), 1)
        savedCV= CV.objects.first()
        check_cv_data(self,savedCV, {'name': name, 'personal_statement': personal_statement, "email": email, "phone": phone})
        
        # Update model
        CV.objects.all().update(name=name2, personal_statement=personal_statement2,phone=phone2,email=email2)
        self.assertEqual(CV.objects.all().count(), 1)

        # Check data was updated
        savedCV2 = CV.objects.first()
        check_cv_data(self,savedCV2, {'name': name2, 'personal_statement': personal_statement2, "email": email2, "phone": phone2})


# Test data
# Work Experience

company = "Google"
job_title = "CEO"
description = "It was good"
start = "03/19"
finish = "04/20"

company2 = "Google2"
job_title2 = "CEO2"
description2 = "It was good2"
start2 = "03/192"
finish2 = "04/202"

def check_work_data(self,modelObject,data):
        # Checks if model object containt the right information as data

        self.assertEqual(modelObject.company, data["company"])
        self.assertEqual(modelObject.job_title, data["job_title"])
        self.assertEqual(modelObject.description, data["description"])
        self.assertEqual(modelObject.start, data["start"])
        self.assertEqual(modelObject.finish, data["finish"])

class CVWorkTest (TestCase):

    def test_work_add_returns_correct_html_template(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)

        response = self.client.get('/cv/work/add/')
        self.assertTemplateUsed(response, 'blog/work_edit.html')
    
    def test_work_add_can_remember_POST_request(self):
        # Login
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)
        
        # Send data
        self.assertEqual(Work.objects.count(), 0)
        response1 = self.client.post('/cv/work/add/', data={'company':company, 'job_title':job_title,
          'description':description, 'start':start, 'finish':finish})

        # data was saved into the database
        self.assertEqual(Work.objects.count(),1)
        savedCV= Work.objects.first()
        check_work_data(self, savedCV, {'company':company, 'job_title':job_title,  'description':description, 'start':start, 'finish':finish})
        
        # redirected to the right page
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/cv/')

        # information added is displayed on the page
        response2 = self.client.get(response1['location'])
        self.assertIn(company, response2.content.decode())
        self.assertIn(job_title, response2.content.decode())
        self.assertIn(description, response2.content.decode())
        self.assertIn(start, response2.content.decode())
        self.assertIn(finish, response2.content.decode())

    def test_work_edit_returns_correct_html_response(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        Work.objects.create(author=me, company=company, job_title=job_title,  description=description, start=start, finish=finish )

        self.client.force_login(user)

        response = self.client.get('/cv/work/edit/1/')
        self.assertTemplateUsed(response, 'blog/work_edit.html')

    def test_work_edit_can_remember_POST_request(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        Work.objects.create(author=me, company=company, job_title=job_title,  description=description, start=start, finish=finish )

        self.client.force_login(user)


        # Send data
        self.assertEqual(Work.objects.count(), 1)
        response1 = self.client.post('/cv/work/edit/1/', data={'company':company2, 'job_title':job_title2,
          'description':description2, 'start':start2, 'finish':finish2})

        # data was saved into the database
        self.assertEqual(Work.objects.count(),1)
        savedCV= Work.objects.first()
        check_work_data(self, savedCV, {'company':company2, 'job_title':job_title2,  'description':description2, 'start':start2, 'finish':finish2})
        
        # redirected to the right page
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/cv/')

        # information added is displayed on the page
        response2 = self.client.get(response1['location'])
        self.assertIn(company2, response2.content.decode())
        self.assertIn(job_title2, response2.content.decode())
        self.assertIn(description2, response2.content.decode())
        self.assertIn(start2, response2.content.decode())
        self.assertIn(finish2, response2.content.decode())
        

class CVWorkModelTest(TestCase):

    def test_saving_and_retrieving_times(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        # Add data to the model
        self.assertEqual(Work.objects.all().count(), 0)

        Work.objects.create(author=me, company=company, job_title=job_title,  description=description, start=start, finish=finish )

        # Check data is saved
        self.assertEqual(Work.objects.all().count(), 1)
        savedWork= Work.objects.first()
        check_work_data(self,savedWork, {'company':company, 'job_title':job_title,  'description':description, 'start':start, 'finish':finish})
        
        # add Second work
        Work.objects.create(author=me, company=company2, job_title=job_title2,  description=description2, start=start2, finish=finish2 )

        # Check data is saved
        self.assertEqual(Work.objects.all().count(), 2)
        savedWork= Work.objects.first()
        check_work_data(self,savedWork, {'company':company, 'job_title':job_title,  'description':description, 'start':start, 'finish':finish})
        savedWork= Work.objects.all()[1]
        check_work_data(self,savedWork, {'company':company2, 'job_title':job_title2,  'description':description2, 'start':start2, 'finish':finish2})


# Education
school = "RRS"
grade = "AAA*"
start = "09/13"
finish = "05/17"

school2 = "RRS2"
grade2 = "AAA*2"
start2 = "09/132"
finish2 = "05/172"

def check_education_data(self,modelObject,data):
        # Checks if model object containt the right information as data

        self.assertEqual(modelObject.school, data["school"])
        self.assertEqual(modelObject.grade, data["grade"])
        self.assertEqual(modelObject.start, data["start"])
        self.assertEqual(modelObject.finish, data["finish"])


class CVEducationTest(TestCase):

    def test_education_add_returns_correct_html_template(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)

        response = self.client.get('/cv/education/add/')
        self.assertTemplateUsed(response, 'blog/education_edit.html')
    
    def test_education_add_can_remember_POST_request(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        self.client.force_login(user)


        # Send data
        self.assertEqual(Education.objects.count(), 0)
        response1 = self.client.post('/cv/education/add/', data={'school':school, 'grade':grade, 'start':start, 'finish':finish})

        # data was saved into the database
        self.assertEqual(Education.objects.count(),1)
        savedEducation= Education.objects.first()
        check_education_data(self, savedEducation, {'school':school, 'grade':grade, 'start':start, 'finish':finish})
        
        # redirected to the right page
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/cv/')

        # information added is displayed on the page
        response2 = self.client.get(response1['location'])
        self.assertIn(school, response2.content.decode())
        self.assertIn(grade, response2.content.decode())
        self.assertIn(start, response2.content.decode())
        self.assertIn(finish, response2.content.decode())
    
    def test_education_edit_returns_correct_html_response(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)
        Education.objects.create(author=User.objects.get(username='roman'), school=school, grade=grade, start=start, finish=finish )

        response = self.client.get('/cv/education/edit/1/')
        self.assertTemplateUsed(response, 'blog/education_edit.html')

    def test_education_edit_can_remember_POST_request(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        Education.objects.create(author=me, school=school, grade=grade, start=start, finish=finish )

        self.client.force_login(user)


        # Send data
        self.assertEqual(Education.objects.count(), 1)
        response1 = self.client.post('/cv/education/edit/1/', data={'school':school2, 'grade':grade2, 'start':start2, 'finish':finish2})

        # data was saved into the database
        self.assertEqual(Education.objects.count(),1)
        savedEducation= Education.objects.first()
        check_education_data(self, savedEducation, {'school':school2, 'grade':grade2, 'start':start2, 'finish':finish2})
        
        # redirected to the right page
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/cv/')

        # information added is displayed on the page
        response2 = self.client.get(response1['location'])
        self.assertIn(school2, response2.content.decode())
        self.assertIn(grade2, response2.content.decode())
        self.assertIn(start2, response2.content.decode())
        self.assertIn(finish2, response2.content.decode())
        

class CVEducationModelTest(TestCase):

    def test_saving_and_retrieving_times(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        # Add data to the model
        self.assertEqual(Education.objects.all().count(), 0)

        Education.objects.create(author=me, school=school, grade=grade, start=start, finish=finish )

        # Check data is saved
        self.assertEqual(Education.objects.all().count(), 1)
        savedEducation= Education.objects.first()
        check_education_data(self,savedEducation, {'school':school, 'grade':grade, 'start':start, 'finish':finish})
        
        # add Second work
        Education.objects.create(author=me, school=school2, grade=grade2, start=start2, finish=finish2 )

        # Check data is saved
        self.assertEqual(Education.objects.all().count(), 2)
        savedEducation= Education.objects.first()
        check_education_data(self,savedEducation, {'school':school, 'grade':grade, 'start':start, 'finish':finish})
        savedEducation= Education.objects.all()[1]
        check_education_data(self,savedEducation, {'school':school2,  'grade':grade2, 'start':start2, 'finish':finish2})


class CVSkillTest(TestCase):

    def test_skill_add_returns_correct_html_template(self):
        self.fail("Finish")

    def test_skill_add_can_remember_POST_request(self):
        self.fail("Finish")

    def test_skill_edit_returns_correct_html_response(self):
        self.fail("Finish")
    
    def test_skill_edit_can_remember_POST_request(self):
        self.fail("Finish")

class CVSkillModelTest(TestCase):

    def test_saving_and_retrieving_times(self):
        self.fail("Finish")