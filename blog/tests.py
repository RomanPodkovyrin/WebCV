from django.test import TestCase, RequestFactory
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import time

from blog.views import post_list, cv_page, post_new


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
    
    def test_post_list_can_remember_post_requests(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='roman', email='example@gmail.com', password='1234')

        request = self.factory.post('/post/new/', data={'title': 'A new list item', 'text': 'hehe'})

        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = post_new(request)
        print(response)

        #############

        # # self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        # self.client.login(username='roman',email='example@gmail.com', password='1234')
        # user = User.objects.create(username='roman',email='example@gmail.com',password='1234')
        # self.client.force_login(user)
        
        # # self.client
        # # self.client.force_authenticate(user=user)
        # response = self.client.post('/post/new/', data={'title': 'A new list item', 'text': 'hehe'})
        # print(response.content.decode())
        # self.assertIn('A new list item', response.content.decode())

        # response = self.client.get('/')
        # self.assertIn('A new list item', response.content.decode())
#########################
        # request = HttpRequest()
        # request.user = User.objects.create(username='roman',password='1234')
        # request.method='POST'
        # request.POST['title'] = 'Test title'
        # request.POST['text'] = 'Test text'
        # response = post_new(request)
        self.fail('Does not work')
        



class CVHomePageTest(TestCase):

    def test_root_url_resolves_to_cv_page_view(self):

        found = resolve('/cv/')
        self.assertEqual(found.func, cv_page)
    
    def test_cv_page_returns_correct_html_template(self):
        
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response,'blog/cv_page.html')
