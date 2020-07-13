from django.contrib import admin
from .models import Post, CV, Work, Education

admin.site.register(Post) # makes the model visible in the admin page
admin.site.register(CV)
admin.site.register(Work)
admin.site.register(Education)
# Register your models here.
