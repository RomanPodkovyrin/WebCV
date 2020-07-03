from django.urls import path
from . import views

# url pattern
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('cv/', views.cv_page, name='cv_page'),
    path('cv/edit/', views.cv_edit, name='cv_edit'),
]