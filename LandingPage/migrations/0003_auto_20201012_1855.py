# Generated by Django 3.0.8 on 2020-10-12 13:25

import LandingPage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0002_auto_20201012_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursevideo',
            name='thumbnail',
            field=models.ImageField(blank=True, default='default/course.png', null=True, upload_to=LandingPage.models.video_path),
        ),
    ]