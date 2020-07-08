from django.contrib import admin
from .models import Post, CV

admin.site.register(Post) # makes the model visible in the admin page
admin.site.register(CV)
# Register your models here.
