# Generated by Django 3.0.7 on 2020-09-27 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learners', '0004_certificate_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learners',
            name='Bio',
        ),
    ]
