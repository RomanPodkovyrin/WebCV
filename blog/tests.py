from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import time
from datetime import datetime

from blog.views import post_list, cv_page, post_new, cv_edit
from blog.models import Post, CV


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

    def test_work_list_returns_correct_html_template(self):
        response = self.client.get('/cv/work/')
        self.assertTemplateUsed(response, 'blog/work_list.html')

    def test_work_add_returns_correct_html_template(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)

        response = self.client.get('/cv/work/add/')
        self.assertTemplateUsed(response, 'blog/work_edit.html')


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

# Work Experience
company = "Google"
description = "It was good"
duration = "03/19-04/20"

# Education
school = "RRS"
grades = "AAA*"
duration = "09/13-05/17"
# Project


def check_cv_data(self,modelObject,data):
        # Checks if model object containt the right information as data

        self.assertEqual(modelObject.name, data["name"])
        self.assertEqual(modelObject.personal_statement, data["personal_statement"])
        self.assertEqual(modelObject.phone, data["phone"])
        self.assertEqual(modelObject.email, data["email"])
        self.assertEqual(modelObject.skills, data["skills"])


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
         "skills": skills, "email": email, "phone": phone})

        # data was saved into the database
        self.assertEqual(CV.objects.count(),1)
        savedCV= CV.objects.first()
        check_cv_data(self, savedCV, {'name': name, 'personal_statement': personal_statement,"skills": skills, "email": email, "phone": phone})
        
        # redirected to the right page
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/cv/')

        # information added is displayed on the page
        response2 = self.client.get(response1['location'])
        self.assertIn(name, response2.content.decode())
        self.assertIn(personal_statement, response2.content.decode())
        self.assertIn(phone, response2.content.decode())
        self.assertIn(email, response2.content.decode())
        self.assertIn(skills, response2.content.decode())

class CVModelTest (TestCase):

    def test_saving_and_retrieving_times(self):
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')

        # Add data to the model
        self.assertEqual(CV.objects.all().count(), 0)
        CV.objects.create(author=me, name=name, personal_statement=personal_statement, skills=skills,phone=phone,email=email)

        # Check data is saved
        self.assertEqual(CV.objects.all().count(), 1)
        savedCV= CV.objects.first()
        check_cv_data(self,savedCV, {'name': name, 'personal_statement': personal_statement,"skills": skills, "email": email, "phone": phone})
        
        # Update model
        CV.objects.all().update(name=name2, personal_statement=personal_statement2, skills=skills2,phone=phone2,email=email2)
        self.assertEqual(CV.objects.all().count(), 1)

        # Check data was updated
        savedCV2 = CV.objects.first()
        check_cv_data(self,savedCV2, {'name': name2, 'personal_statement': personal_statement2,"skills": skills2, "email": email2, "phone": phone2})
        
