# Generated by Django 3.0.7 on 2020-08-11 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilitators', '0002_applicants_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicants',
            name='added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='applicants',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='facilitator',
            name='added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='facilitator',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]