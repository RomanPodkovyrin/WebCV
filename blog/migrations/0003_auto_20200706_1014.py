# Generated by Django 2.2.13 on 2020-07-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_cv_education_work'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Education',
        ),
        migrations.DeleteModel(
            name='Work',
        ),
        migrations.AddField(
            model_name='cv',
            name='education',
            field=models.CharField(default='[]', max_length=400),
        ),
        migrations.AddField(
            model_name='cv',
            name='skills',
            field=models.CharField(default='[]', max_length=200),
        ),
        migrations.AddField(
            model_name='cv',
            name='work',
            field=models.CharField(default='[]', max_length=500),
        ),
    ]
