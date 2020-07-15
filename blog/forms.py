from django import forms
from .models import Post, CV, Work, Education

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ('name', 'personal_statement', 'phone', 'email' ,)

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ('company', 'job_title', 'description', 'start', 'finish',)

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('school', 'grade','start','finish')