# Generated by Django 3.0.7 on 2020-09-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0009_auto_20200905_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Advanced', 'Advanced')], default='Beginner', max_length=50),
        ),
    ]