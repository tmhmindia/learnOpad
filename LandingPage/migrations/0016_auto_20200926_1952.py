# Generated by Django 3.0.7 on 2020-09-26 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandingPage', '0015_auto_20200926_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='days',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='months',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]