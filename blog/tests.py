from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from blog.views import post_list, cv_page


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


class CVHomePageTest(TestCase):

    def test_root_url_resolves_to_cv_page_view(self):

        found = resolve('/cv/')
        self.assertEqual(found.func, cv_page)
    
    def test_cv_page_returns_correct_html_template(self):
        
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response,'blog/cv_page.html')
