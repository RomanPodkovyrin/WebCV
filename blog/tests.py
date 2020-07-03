from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import time
from datetime import datetime

from blog.views import post_list, cv_page, post_new, cv_edit
from blog.models import Post, CV, Work, Education


class BlogHomePageTest(TestCase):

    def test_root_url_resolves_to_post_list_view(self):
        found = resolve('/')
        self.assertEqual(found.func, post_list)

    def test_post_list_returns_correct_html_template(self):
        
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_edit_returns_correct_html_template_for_new_post(self):
        response = self.client.get('/post/new/')
        self.assertTemplateUsed(response, 'blog/post_edit.html')
    
    def test_post_list_can_remember_POST_requests(self):

        # self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        self.client.login(username='roman',email='example@gmail.com', password='1234')
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)
        
        # self.client
        # self.client.force_authenticate(user=user)
        date = str(datetime.now())
        title = 'Unittest title test ' + date 
        text = 'Unittest text test ' + date
        self.assertEqual(Post.objects.count(), 0)
        response1 = self.client.post('/post/new/', data={'title': title, 'text': text})

        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()# or Post.objects.all()[0]
        self.assertEqual(title,post.title)
        self.assertEqual(text,post.text)

        
        self.assertEqual(response1.status_code,302)
        self.assertEqual(response1['location'],'/post/1/')

        response2 = self.client.get(response1['location'])
        self.assertIn(title, response2.content.decode())
        self.assertIn(text, response2.content.decode())

        response3 = self.client.get('/')
        self.assertIn(title, response3.content.decode())
        self.assertIn(text, response3.content.decode())



class PostModelTest(TestCase):

    def test_saving_and_retrieving_times(self):

        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')
        self.assertEqual(Post.objects.all().count(), 0)

        Post.objects.create(author=me,title='Sample unit test title', text='Test')

        self.assertEqual(Post.objects.all().count(), 1)

        Post.objects.create(author=me,title='Sample unit test title2', text='Test2')

        self.assertEqual(Post.objects.all().count(), 2)

        saved = Post.objects.all()
        self.assertEqual(saved[0].title, 'Sample unit test title')
        self.assertEqual(saved[0].text, 'Test')

        self.assertEqual(saved[1].title, 'Sample unit test title2')
        self.assertEqual(saved[1].text, 'Test2')






class CVHomePageTest(TestCase):

    def test_root_url_resolves_to_cv_page_view(self):

        found = resolve('/cv/')
        self.assertEqual(found.func, cv_page)
    
    def test_cv_page_returns_correct_html_template(self):
        
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response,'blog/cv_page.html')

    def test_cv_edit_returns_correct_html_template(self):

        response = self.client.get('/cv/edit/')
        self.assertTemplateUsed(response,'blog/cv_edit.html')

    def test_cv_edit_can_remember_POST_requests(self):

        self.client.login(username='roman',email='example@gmail.com', password='1234')
        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        self.client.force_login(user)
        
        date = str(datetime.now())
        name = 'Roman Podkovyrin ' + date 
        personal_statement = 'Personal Statement ' + date
        skills = '["Java", "Python", "Russian"]'
        work_experience = '["company": "Google", "description": "It was good", "duration": 03/19-04/20]'
        education = '["school": "RRS", "grades": "AAA*", "duration": "09/13-05/17"]'
        self.assertEqual(Post.objects.count(), 0)
        response1 = self.client.post('/post/new/', data={'name': name, 'personal_statement': personal_statement,
         "skills": skills, "work_experinece": work_experience, "education": education, "phone": "00000000",
          "email": "email@example.com"})

        # self.assertEqual(Post.objects.count(), 1)
        # post = Post.objects.first()# or Post.objects.all()[0]
        # self.assertEqual(title,post.title)
        # self.assertEqual(text,post.text)

        
        # self.assertEqual(response1.status_code,302)
        # self.assertEqual(response1['location'],'/cv/')

        # response2 = self.client.get(response1['location'])
        # self.assertIn(title, response2.content.decode())
        # self.assertIn(text, response2.content.decode())

        # response3 = self.client.get('/')
        # self.assertIn(title, response3.content.decode())
        # self.assertIn(text, response3.content.decode())

class CVModelTest (TestCase):

    def test_saving_and_retrieving_times(self):

        user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        me = User.objects.get(username='roman')
        self.assertEqual(CV.objects.all().count(), 0)

        Work.objects.create(company="Google", description="Help me", duration="2000-2012")
        Education.objects.create(school="RRS", grade="AAA*", duration="2013-2017")

        CV.objects.create(author=me,name="Roman Podkovyrin", statement="Hello, please hire me",
        skills=["Java", "python","russina"], work=Work.objects.all(),education=Education.objects.all(),phone="0000000",email="email@mail.com")

        self.assertEqual(CV.objects.all().count(), 1)
        self.assertEqual(Work.objects.all().count(), 1)
        self.assertEqual(Education.objects.all().count(), 1)

        savedCV= CV.objects.first
        self.assertEqual(savedCV.name, "Roman Podkovyrin")
        self.assertEqual(savedCV.statement, "Hello, please hire me")
        self.assertEqual(savedCV.phone, "0000000")
        self.assertEqual(savedCV.email, "email@mail.com")

        worktest = savedCV.work
        self.assertEqual(worktest.all().count(), 1)
        worktest=worktest.first()
        self.assertEqual(worktest.company, "Google")
        self.assertEqual(worktest.education, "Help me")
        self.assertEqual(worktest.duration, "2000-2012")

        educationtest = savedCV.education
        self.assertEqual(educationtest.all().count(), 1)
        educationtest = educationtest.first()
        self.assertEqual(educationtest.school, "RRS")
        self.assertEqual(educationtest.grade, "AAA*")
        self.assertEqual(educationtest.duration,"2013-2017" )
        self.fail("Finish check for work and eduation")

        Post.objects.first().update(name="Roman Podkovyrin2", statement="Hello, please hire me2",
        skills=["Java2", "python2","russina2"], work=Work.objects.all(),education=Education.objects.all(),phone="00000002",email="email@mail.com2")

        self.assertEqual(CV.objects.all().count(), 1)
        self.assertEqual(Work.objects.all().count(), 1)
        self.assertEqual(Education.objects.all().count(), 1)

        # saved = Post.objects.all()
        # self.assertEqual(saved[0].title, 'Sample unit test title')
        # self.assertEqual(saved[0].text, 'Test')

        # self.assertEqual(saved[1].title, 'Sample unit test title2')
        # self.assertEqual(saved[1].text, 'Test2')
        self.fail("Finish test")
