# Generated by Django 3.0.7 on 2020-09-18 07:03

import LandingPage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0011_auto_20200918_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=LandingPage.models.video_course_path),
        ),
        migrations.AddField(
            model_name='coursevideo',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to=LandingPage.models.video_path),
        ),
    ]
