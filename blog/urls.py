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
    path('cv/work/add/', views.work_add, name='work_add'),
    path('cv/work/edit/<int:pk>/', views.work_edit, name='work_edit'),
    path('cv/education/edit/<int:pk>/', views.education_edit, name='education_edit'),
    path('cv/education/add/', views.education_add, name='education_add'),
    path('cv/skill/add/', views.skill_add, name='skill_add'),
    path('cv/skill/edit/<int:pk>/', views.skill_edit, name='skill_edit'),
]