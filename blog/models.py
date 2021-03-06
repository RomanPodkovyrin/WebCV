from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title



class CV(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='')#models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    personal_statement = models.TextField(default='')
    # skills = models.CharField(max_length=200, default='')
    phone = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=200, default='')

    # def set_skills(self, x):
    #     self.skills = json.dumps(x)

    # def get_skills(self):
    #     return json.load(self.skills)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name


class Work(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=200, default='')
    job_title = models.CharField(max_length=200, default='')
    description = models.TextField(default='')
    start = models.CharField(max_length=200, default='')
    finish = models.CharField(max_length=200, default='')

    def publish(self):
        self.save()

    def __str__(self):
        return self.company


class Education(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.CharField(max_length=200, default='')
    grade = models.CharField(max_length=200, default='')
    start = models.CharField(max_length=200, default='')
    finish = models.CharField(max_length=200, default='')

class Skill(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill = models.CharField(max_length=200, default='')